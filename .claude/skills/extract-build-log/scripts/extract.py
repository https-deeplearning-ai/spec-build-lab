#!/usr/bin/env python3
"""extract.py — slice a Claude Code session transcript into a build log.

Usage:
    python3 extract.py <evals/run-NN dir> [--until=<regex>] [--from=<regex>]

Reads <eval-dir>/.session (one line: full transcript path, OR session id
that we resolve under ~/.claude/projects/<project-slug>/<id>.jsonl).
Slices the transcript between an opening bookend (default: the
"Run NN — building in builds/run-NN/" announcement) and a closing bookend
(default: a fuzzy diagram/structure phrase, else end-of-transcript).
Writes <eval-dir>/session-log.md.

Idempotent: overwrites cleanly. Re-runnable with different bookends.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


DEFAULT_UNTIL = (
    r"(infra|architecture|structure)\s+(diagram|of (this|your) app)"
    r"|"
    r"(this is|here'?s)\s+the\s+(infra|architecture|structure)"
)


def read_session_breadcrumb(eval_dir: Path) -> Path:
    """Return the absolute path of the transcript JSONL.

    The .session file holds either:
      - an absolute path to the transcript JSONL (preferred — robust to
        Claude Code's projects-dir convention changing), OR
      - a bare session id (we resolve it).
    """
    session_file = eval_dir / ".session"
    if not session_file.is_file():
        sys.exit(f"error: {session_file} is missing")
    raw = session_file.read_text().strip()
    if not raw:
        sys.exit(f"error: {session_file} is empty")

    candidate = Path(raw)
    if candidate.is_absolute() and candidate.is_file():
        return candidate

    # Fallback: treat raw as a session id; derive transcript path.
    project_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if not project_root:
        sys.exit(
            "error: CLAUDE_PROJECT_DIR not set and .session does not contain "
            "an absolute transcript path"
        )
    slug = project_root.replace("/", "-")
    derived = Path.home() / ".claude" / "projects" / slug / f"{raw}.jsonl"
    if not derived.is_file():
        sys.exit(f"error: derived transcript path does not exist: {derived}")
    return derived


def assistant_text(msg: dict) -> str:
    """Join all 'text' content blocks in an assistant message."""
    content = (msg.get("message") or {}).get("content") or []
    if not isinstance(content, list):
        return ""
    parts = [
        c.get("text", "")
        for c in content
        if isinstance(c, dict) and c.get("type") == "text"
    ]
    return "\n".join(p for p in parts if p)


def user_text(msg: dict) -> str:
    """Best-effort user-message rendering. content can be string or list."""
    content = (msg.get("message") or {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                t = c.get("type")
                if t == "text":
                    parts.append(c.get("text", ""))
                elif t == "tool_result":
                    # Tool results round-trip through user role; suppress
                    # bulky output but note their presence.
                    parts.append("> (tool_result, suppressed)")
        return "\n".join(p for p in parts if p)
    return ""


def tool_calls(msg: dict) -> list[tuple[str, str]]:
    """Return [(tool_name, one-line input preview)] for an assistant turn."""
    content = (msg.get("message") or {}).get("content") or []
    if not isinstance(content, list):
        return []
    out = []
    for c in content:
        if not isinstance(c, dict) or c.get("type") != "tool_use":
            continue
        name = c.get("name", "?")
        inp = c.get("input") or {}
        try:
            preview = json.dumps(inp, ensure_ascii=False)
        except Exception:
            preview = str(inp)
        preview = preview.replace("\n", " ")
        if len(preview) > 80:
            preview = preview[:77] + "..."
        out.append((name, preview))
    return out


def materials_hits(turns: list[dict]) -> list[tuple[str, str]]:
    """Return tool calls whose target path mentions materials/.

    Belt-and-suspenders for the PreToolUse hook (.claude/hooks/
    no-materials-during-build.sh): if the hook was bypassed, this catches
    the contamination post-hoc. Returns [(tool_name, candidate_path)].
    """
    hits = []
    for t in turns:
        if t.get("type") != "assistant":
            continue
        content = (t.get("message") or {}).get("content") or []
        if not isinstance(content, list):
            continue
        for c in content:
            if not isinstance(c, dict) or c.get("type") != "tool_use":
                continue
            name = c.get("name", "?")
            inp = c.get("input") or {}
            if not isinstance(inp, dict):
                continue
            target = (
                inp.get("file_path")
                or inp.get("path")
                or inp.get("pattern")
                or inp.get("command")
                or ""
            )
            if not isinstance(target, str):
                continue
            if "materials/" in target:
                hits.append((name, target))
    return hits


def load_turns(transcript: Path) -> list[dict]:
    """Return only assistant + user records, in order."""
    turns = []
    with transcript.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") in ("user", "assistant"):
                turns.append(obj)
    return turns


def find_opening(turns: list[dict], from_re: re.Pattern) -> int:
    """Return the index of the LAST assistant turn whose text matches.

    "Last" so re-runs of /prepare-build pick the most recent.
    Returns 0 (slice from the start) if no match.
    """
    last = -1
    for i, t in enumerate(turns):
        if t.get("type") != "assistant":
            continue
        if from_re.search(assistant_text(t)):
            last = i
    return last if last >= 0 else 0


def find_closing(turns: list[dict], start: int, until_re: re.Pattern) -> int:
    """Return the index of the FIRST assistant turn AFTER `start` matching.

    Returns len(turns) if no match — slice extends to end-of-transcript.
    """
    for i in range(start + 1, len(turns)):
        t = turns[i]
        if t.get("type") != "assistant":
            continue
        if until_re.search(assistant_text(t)):
            return i
    return len(turns)


def render(turns: list[dict], header: dict) -> str:
    hits = header.get("materials_hits") or []
    if hits:
        materials_line = (
            f"- **Materials access**: ⚠️ WARNING — {len(hits)} tool call"
            f"{'s' if len(hits) != 1 else ''} touched `materials/` during the "
            f"build. This run is contaminated; `/eval-materials-vs-build` will "
            f"reflect agent recall, not spec fidelity."
        )
    else:
        materials_line = "- **Materials access**: NONE detected ✓"

    out = [
        "# Session log",
        "",
        f"- **Run**: {header['run']}",
        f"- **Transcript**: `{header['transcript']}`",
        f"- **Opened by**: `{header['from_pattern']}`",
        f"- **Closed by**: `{header['until_pattern']}` "
        f"({'matched' if header['closed_by_match'] else 'end-of-transcript'})",
        f"- **Turns**: {header['turn_count']}",
        materials_line,
    ]
    if hits:
        out.append("")
        out.append("Contaminating tool calls:")
        for name, target in hits:
            preview = target.replace("\n", " ")
            if len(preview) > 100:
                preview = preview[:97] + "..."
            out.append(f"- `{name}` → `{preview}`")
    out.extend(["", "---", ""])
    for t in turns:
        if t.get("type") == "user":
            txt = user_text(t).strip()
            if not txt:
                continue
            out.append("### User")
            out.append("")
            out.append(txt)
            out.append("")
            out.append("---")
            out.append("")
        elif t.get("type") == "assistant":
            txt = assistant_text(t).strip()
            calls = tool_calls(t)
            if not txt and not calls:
                continue
            out.append("### Assistant")
            out.append("")
            if txt:
                out.append(txt)
                out.append("")
            for name, preview in calls:
                out.append(f"> Tool: **{name}** — `{preview}`")
            if calls:
                out.append("")
            out.append("---")
            out.append("")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("eval_dir", type=Path, help="path to evals/run-NN/")
    p.add_argument(
        "--until",
        default=DEFAULT_UNTIL,
        help="regex (case-insensitive) for closing bookend",
    )
    p.add_argument(
        "--from",
        dest="from_pat",
        default=None,
        help="regex (case-insensitive) for opening bookend; "
        "default is built from the run name",
    )
    args = p.parse_args(argv)

    eval_dir: Path = args.eval_dir.resolve()
    if not eval_dir.is_dir():
        sys.exit(f"error: {eval_dir} is not a directory")

    run_name = eval_dir.name  # e.g. "run-03"
    transcript = read_session_breadcrumb(eval_dir)

    from_pat = args.from_pat or rf"Run\s+\d+\s*[—-]\s*building in builds/{run_name}"
    from_re = re.compile(from_pat, re.IGNORECASE)
    until_re = re.compile(args.until, re.IGNORECASE)

    turns = load_turns(transcript)
    if not turns:
        sys.exit(f"error: no user/assistant turns found in {transcript}")

    open_idx = find_opening(turns, from_re)
    close_idx = find_closing(turns, open_idx, until_re)
    closed_by_match = close_idx < len(turns)

    sliced = turns[open_idx:close_idx]
    hits = materials_hits(sliced)
    output = render(
        sliced,
        {
            "run": run_name,
            "transcript": transcript,
            "from_pattern": from_pat,
            "until_pattern": args.until,
            "closed_by_match": closed_by_match,
            "turn_count": len(sliced),
            "materials_hits": hits,
        },
    )

    out_path = eval_dir / "session-log.md"
    out_path.write_text(output)

    contam_msg = (
        f"⚠️  {len(hits)} contaminating tool call(s) touched materials/"
        if hits
        else "no materials/ access detected"
    )
    print(
        f"Wrote {out_path} — {len(sliced)} turns, "
        f"opened by /{from_pat}/ "
        f"({'matched' if open_idx > 0 else 'no match — sliced from start'}), "
        f"closed by /{args.until}/ "
        f"({'matched' if closed_by_match else 'no match — sliced to end-of-transcript'}), "
        f"{contam_msg}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
