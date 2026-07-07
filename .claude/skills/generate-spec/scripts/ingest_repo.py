#!/usr/bin/env python3
"""ingest_repo.py — build a course "context" markdown from a git repo.

Usage:
    python3 ingest_repo.py <repo> --out <path.md> [--ref <branch/tag/sha>]
                           [--title <str>] [--helper-name helper.py] [--keep-clone]

Clones <repo> (SSH URL, https, or a local path / file:// for testing) over the
caller's git credentials, then renders every notebook (.ipynb) cell-by-cell into
the same shape as a hand-downloaded course context dump, followed by a
de-duplicated "Helper Module Context" section built from the repo's helper.py
module(s).

The generated markdown is written to --out, which MUST live under a course's
materials/notebooks/ directory. transcripts/ are never touched — they remain a
manual drop.

De-dup rule: each unique top-level def (function/class) appears once; identical
copies (including symlinks) collapse; a same-name-but-different-body collision
keeps BOTH variants, flagged inline so nothing is silently dropped.

Lesson numbering is inferred from sorted notebook order — it is a convenience
label, NOT authentic platform numbering (the transcripts are authoritative for
that). The output says so.

Stdlib only. Idempotent: overwrites --out cleanly.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ── Cloning ──────────────────────────────────────────────────────────────

_SHA_RE = re.compile(r"^[0-9a-fA-F]{7,40}$")


def is_local_repo(repo: str) -> Path | None:
    """Return a Path if `repo` is an existing local dir (skip cloning)."""
    raw = repo[len("file://"):] if repo.startswith("file://") else repo
    p = Path(raw).expanduser()
    return p if p.is_dir() else None


def clone_repo(repo: str, ref: str | None, dest: Path) -> Path:
    """Clone `repo` into `dest`. A local dir is copied, not cloned.

    Shallow-clones by default. When `ref` looks like a commit SHA we do a full
    clone then checkout, since --depth 1 can't resolve an arbitrary SHA.
    """
    local = is_local_repo(repo)
    if local is not None:
        # Copy the working tree (incl. symlinks) so tests don't need a remote.
        shutil.copytree(local, dest, symlinks=True, dirs_exist_ok=True)
        if ref:
            _run_git(["git", "-C", str(dest), "checkout", ref], repo)
        return dest

    ref_is_sha = bool(ref and _SHA_RE.match(ref))
    if ref and not ref_is_sha:
        cmd = ["git", "clone", "--depth", "1", "--branch", ref, repo, str(dest)]
    elif not ref:
        cmd = ["git", "clone", "--depth", "1", repo, str(dest)]
    else:
        cmd = ["git", "clone", repo, str(dest)]
    _run_git(cmd, repo)
    if ref_is_sha:
        _run_git(["git", "-C", str(dest), "checkout", ref], repo)
    return dest


def _run_git(cmd: list[str], repo: str) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-4:]
        detail = "\n  ".join(tail)
        sys.exit(
            f"error: git failed for {repo!r}:\n  {detail}\n"
            f"hint: is your SSH key authorized for this repo, and the ref valid?"
        )


# ── Discovery ────────────────────────────────────────────────────────────

def _skip(path: Path) -> bool:
    parts = set(path.parts)
    return ".git" in parts or ".ipynb_checkpoints" in parts


def find_notebooks(root: Path) -> list[Path]:
    """All *.ipynb under root, sorted by relative path, excluding junk dirs."""
    return sorted(
        (p for p in root.rglob("*.ipynb") if not _skip(p)),
        key=lambda p: p.relative_to(root).as_posix(),
    )


def find_helpers(root: Path, name: str) -> list[Path]:
    """All files named `name` under root, symlink/duplicate-collapsed.

    Collapses by resolved realpath so a single file symlinked from N locations
    is processed once. Keeps the shortest relative path as the canonical label.
    """
    by_real: dict[Path, Path] = {}
    for p in root.rglob(name):
        if _skip(p):
            continue
        real = p.resolve()
        prev = by_real.get(real)
        if prev is None or len(p.relative_to(root).as_posix()) < len(
            prev.relative_to(root).as_posix()
        ):
            by_real[real] = p
    return sorted(by_real.values(), key=lambda p: p.relative_to(root).as_posix())


# ── Notebook rendering ───────────────────────────────────────────────────

def cell_source(cell: dict) -> str:
    """nbformat `source` is a list of line-strings or one string."""
    src = cell.get("source", "")
    text = "".join(src) if isinstance(src, list) else str(src)
    return text.rstrip("\n")


def notebook_title(cells: list[dict], fallback: str) -> str:
    """First markdown H1 (`# ...`) if present, else the fallback (file stem)."""
    for cell in cells:
        if cell.get("cell_type") == "markdown":
            for line in cell_source(cell).splitlines():
                m = re.match(r"\s*#\s+(.+?)\s*$", line)
                if m:
                    return m.group(1).strip()
    return fallback


def read_cells(path: Path) -> list[dict]:
    """Parse an .ipynb; return its cells. Warn + skip on bad JSON."""
    try:
        obj = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError as exc:
        print(f"warning: skipping unreadable notebook {path}: {exc}", file=sys.stderr)
        return []
    cells = obj.get("cells")
    return cells if isinstance(cells, list) else []


def render_notebook(rel_path: str, title: str, lesson_no: int, cells: list[dict]) -> str:
    """Emit one `## Lesson N: <title> — <rel_path>` section, cells fence-less."""
    out = [f"## Lesson {lesson_no}: {title} — {rel_path}", ""]
    for i, cell in enumerate(cells):
        kind = "code" if cell.get("cell_type") == "code" else "markdown"
        body = cell_source(cell)
        if not body.strip():
            continue
        out.append(f"[{kind}] cell {i}")
        out.append("")
        out.append(body)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ── Helper extraction + dedup ────────────────────────────────────────────

class Def:
    __slots__ = ("name", "kind", "source", "file", "hash")

    def __init__(self, name: str, kind: str, source: str, file: str):
        self.name = name
        self.kind = kind
        self.source = source
        self.file = file
        self.hash = hashlib.sha1(source.encode("utf-8")).hexdigest()


def extract_defs(path: Path, label: str) -> list[Def]:
    """Top-level functions/classes with exact source. Warn + skip on SyntaxError."""
    source = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        print(f"warning: skipping unparseable {label}: {exc}", file=sys.stderr)
        return []
    kinds = {
        ast.FunctionDef: "def",
        ast.AsyncFunctionDef: "def",
        ast.ClassDef: "class",
    }
    defs: list[Def] = []
    for node in tree.body:
        kind = kinds.get(type(node))
        if kind is None:
            continue
        seg = ast.get_source_segment(source, node)
        if seg is None:
            continue
        defs.append(Def(node.name, kind, seg, label))
    return defs


def dedup_defs(defs: list[Def]) -> tuple[list[Def], set[str]]:
    """Collapse identical defs; keep all variants of a name that conflict.

    Returns (kept_defs_in_discovery_order, conflicting_names). A name is a
    conflict when it has >1 distinct source hash. Identical copies (same hash),
    including those reached via symlink, appear once.
    """
    by_name: dict[str, list[Def]] = {}
    for d in defs:
        by_name.setdefault(d.name, []).append(d)

    conflicts: set[str] = set()
    kept_by_key: dict[tuple[str, str], Def] = {}
    order: list[tuple[str, str]] = []
    for d in defs:
        distinct_hashes = {x.hash for x in by_name[d.name]}
        if len(distinct_hashes) > 1:
            conflicts.add(d.name)
        key = (d.name, d.hash)
        if key not in kept_by_key:
            kept_by_key[key] = d
            order.append(key)
    return [kept_by_key[k] for k in order], conflicts


def render_helpers(defs: list[Def], conflicts: set[str], labels: list[str],
                   symlinks_collapsed: int) -> str:
    """Emit the `## Helper Module Context` section, or "" if no defs."""
    if not defs:
        return ""
    provenance = ", ".join(labels)
    note = f"_Extracted from: {provenance}._"
    if symlinks_collapsed:
        note = note[:-1] + f" ({symlinks_collapsed} symlink(s) collapsed)._"
    out = [
        "## Helper Module Context",
        "",
        note,
        "",
        "_Top-level functions and classes, de-duplicated across helper files. "
        "Module-level constants are not included._",
        "",
    ]
    emitted_conflict_header: set[str] = set()
    for d in defs:
        if d.name in conflicts:
            if d.name not in emitted_conflict_header:
                variant_files = [x.file for x in defs
                                 if x.name == d.name and x.name in conflicts]
                out.append(
                    f"> ⚠️ CONFLICT: `{d.name}` has differing definitions across "
                    f"{', '.join(variant_files)} — all variants shown below."
                )
                out.append("")
                emitted_conflict_header.add(d.name)
            out.append(f"> from `{d.file}`:")
            out.append("")
        out.append("```python")
        out.append(d.source)
        out.append("```")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ── Document assembly ────────────────────────────────────────────────────

_MAP_NOTE = (
    "> Generated from a git repo by ingest_repo.py. Lesson numbers are inferred "
    "from notebook order and are a convenience label only — the transcripts under "
    "materials/transcripts/ are authoritative for lesson numbering and titles."
)


def build_markdown(title: str, notebooks: list[tuple[str, str, int, list[dict]]],
                   helper_section: str) -> str:
    """Assemble title → Lesson Map → notebook sections → helper section."""
    parts = [f"# {title}", "", "---", "", "## Lesson Map", ""]
    if notebooks:
        for rel, ntitle, no, _cells in notebooks:
            parts.append(f"- {rel} → Lesson {no}: {ntitle}")
    else:
        parts.append("- (no .ipynb files found)")
    parts += ["", _MAP_NOTE, ""]
    for rel, ntitle, no, cells in notebooks:
        parts.append("---")
        parts.append("")
        parts.append(render_notebook(rel, ntitle, no, cells))
    if helper_section:
        parts.append("---")
        parts.append("")
        parts.append(helper_section)
    return "\n".join(parts).rstrip() + "\n"


def derive_title(out: Path) -> str:
    """Heuristic doc title from the --out filename (strip trailing -context)."""
    stem = out.stem
    stem = re.sub(r"[-_]context$", "", stem)
    return stem.replace("-", " ").replace("_", " ").strip().title() or stem


# ── Output-safety guard ──────────────────────────────────────────────────

def check_out_path(out: Path) -> None:
    parts = out.as_posix()
    if "materials/notebooks" not in parts:
        sys.exit(
            f"error: --out must live under a course's materials/notebooks/ "
            f"(got {out})"
        )
    if "transcripts" in out.parts:
        sys.exit(f"error: refusing to write into a transcripts path ({out})")


# ── Main ─────────────────────────────────────────────────────────────────

def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build a course context md from a repo.")
    p.add_argument("repo", help="git SSH/https URL, or a local path / file:// dir")
    p.add_argument("--out", "-o", required=True, type=Path,
                   help="destination .md under a course's materials/notebooks/")
    p.add_argument("--ref", default=None, help="branch/tag/commit (default: repo default)")
    p.add_argument("--title", default=None, help="document H1 (default: from --out name)")
    p.add_argument("--helper-name", default="helper.py",
                   help="filename treated as a helper module (default: helper.py)")
    p.add_argument("--keep-clone", action="store_true",
                   help="don't delete the temp clone (debugging)")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    out: Path = args.out.resolve()
    check_out_path(out)
    out.parent.mkdir(parents=True, exist_ok=True)

    tmp = Path(tempfile.mkdtemp(prefix="ingest-repo-"))
    try:
        root = clone_repo(args.repo, args.ref, tmp / "repo")

        nb_paths = find_notebooks(root)
        notebooks: list[tuple[str, str, int, list[dict]]] = []
        total_cells = 0
        for i, path in enumerate(nb_paths, start=1):
            rel = path.relative_to(root).as_posix()
            cells = read_cells(path)
            total_cells += len(cells)
            title = notebook_title(cells, path.stem)
            notebooks.append((rel, title, i, cells))

        helper_paths = find_helpers(root, args.helper_name)
        raw_hits = [p for p in root.rglob(args.helper_name) if not _skip(p)]
        symlinks_collapsed = max(0, len(raw_hits) - len(helper_paths))
        all_defs: list[Def] = []
        labels: list[str] = []
        for path in helper_paths:
            label = path.relative_to(root).as_posix()
            labels.append(label)
            all_defs.extend(extract_defs(path, label))
        kept, conflicts = dedup_defs(all_defs)
        helper_section = render_helpers(kept, conflicts, labels, symlinks_collapsed)

        if not nb_paths and not kept:
            sys.exit(
                f"error: nothing to ingest — no .ipynb or {args.helper_name} "
                f"found in {args.repo}"
            )

        title = args.title or derive_title(out)
        title_note = "" if args.title else " (heuristic)"
        document = build_markdown(title, notebooks, helper_section)
        out.write_text(document, encoding="utf-8")
    finally:
        if not args.keep_clone:
            shutil.rmtree(tmp, ignore_errors=True)

    print(
        f"Wrote {out} — {len(nb_paths)} notebook(s) ({total_cells} cells), "
        f"{len(helper_paths)} helper file(s) → {len(kept)} unique def(s) "
        f"({len(conflicts)} name-conflict(s), {symlinks_collapsed} symlink(s) "
        f"collapsed), title {title!r}{title_note}, "
        f"from {args.repo}@{args.ref or 'default'}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
