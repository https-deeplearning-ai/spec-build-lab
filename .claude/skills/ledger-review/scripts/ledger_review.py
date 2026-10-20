#!/usr/bin/env python3
"""ledger_review.py — the deterministic half of /ledger-review.

  skeleton <spec.md> --out DIR [--name NAME] [--link-base URL] [--previous FILE]
      Writes DIR/skeleton.md (every fixed and factual part of the review comment, with ⟦…⟧ slots
      for the plain-language wording) and DIR/sources.md (the spec text each slot is written from).
      Sections whose source is unchanged since --previous (an earlier review comment) are copied
      from it verbatim and carry no slots.
  check <skeleton.md> <draft.md> [--allow-unmarked]
      Fails unless the draft matches the skeleton line for line: every fixed part identical, every
      slot filled, no internal term in any slot. --allow-unmarked skips the hidden <!-- --> markers
      (only for comparing against a comment written before the markers existed).
  previous <repo-relative spec path> [--exclude-pr N]
      Prints the most recent earlier review comment for this spec file, found through the merged
      PRs that touched it; prints nothing if there is none.

Stdlib only. Parsing follows the spec-generation guide's Decision Ledger and §7 "Tests by option"
formats; it degrades loudly (exit 2) when a spec does not have them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

CATS = ("learner", "design-argued", "design-structural", "realization", "contradicted")
ROW_RE = re.compile(r"^\|\s*\**([A-Z][A-Z-]*\d+)\**\s*\|\s*\**(" + "|".join(CATS) + r")\**\s*\|")
SLOT = re.compile(r"⟦[^⟧]*⟧")
MARK = re.compile(r"^<!-- ledger-review .*-->$")
BANNED = [r"\binvariant", r"\blitmus", r"\bstand-in", r"\brealization\b", r"\bacceptance criteri",
          r"\btie-breaker", r"\bdisposition", r"\bnarrative\b", r"\bbake-in", r"\bLedger\b",
          r"(?<![A-Za-z])R\d+\b", r"(?<![A-Za-z-])AC\d+\b", r"§"]

HEADER = """## Decision Ledger for review: {name}

A plain-language version of the spec's Decision Ledger, for review. Each heading links to its row in this PR's `{file}`.

**How to read it.** Before building, the build agent asks the learner one question per decision below. Each table lists the answers they can pick.
- ✅ **Recommended**: what the default build uses (chosen when the spec was written, not tailored to the learner).
- 📘 **Course used**: what the course itself did.
- **If chosen**: what the build leaves out or changes. "—" means nothing.

Some questions are asked only after a certain earlier answer; they say so.

---
"""
TABLE_HEAD = "| Ref | Option | Setup | Labels | If chosen |\n|---|---|---|---|---|"
FOOTER = """---

### Known open points (⟦OPEN-NOTE: e.g. already flagged; tracked on #N⟧)
⟦OPEN: numbered list, one point per line⟧

*Reviewers: comment with the Ref (for example "{example}: …").*"""


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def expand_ac(text: str) -> set[str]:
    out: set[str] = set()
    for a, b in re.findall(r"AC(\d+)\s*[–-]\s*(?:AC)?(\d+)", text):
        if int(a) <= int(b) <= int(a) + 80:
            out.update(f"AC{i}" for i in range(int(a), int(b) + 1))
    out.update(re.findall(r"(?<![A-Za-z-])AC\d+\b", text))
    return out


def parse(spec: Path) -> dict:
    lines = spec.read_text(encoding="utf-8").splitlines()
    rows = []
    for n, line in enumerate(lines, 1):
        m = ROW_RE.match(line)
        if not m:
            continue
        c = cells(line)
        if len(c) < 7:
            continue
        rid = m.group(1)
        parts = [p.strip().rstrip(";").removesuffix("<br>").strip()
                 for p in re.split(rf"(?=(?<![A-Za-z0-9-]){re.escape(rid)}[a-z] — )", c[5]) if p.strip()]
        options = []
        for p in parts:
            om = re.match(rf"({re.escape(rid)}[a-z]) — (.*)$", p, re.S)
            if not om:
                continue
            text = om.group(2)
            status = ""
            if re.search(r"no code shipped", text, re.I):
                status = "shown in the course, no code shipped"
            elif re.search(r"never built", text, re.I):
                status = "never built by the course; the spec gives no tests for it"
            options.append({"id": om.group(1), "text": text,
                            "recommended": "(Recommended" in text,
                            "course": "course default" in text, "status": status})
        cond = re.search(r"Applies only when\s+`?([A-Z][A-Z-]*\d+)`?\s+is\s+(.*)", c[2])
        rows.append({"id": rid, "line": n, "raw": line, "decision": c[2], "invariant": c[3],
                     "default": c[4], "tradeoff": c[6], "options": options,
                     "cond_row": cond.group(1) if cond else None,
                     "cond_ids": re.findall(rf"{cond.group(1)}[a-z]\b", cond.group(2)) if cond else []})
    if not rows:
        sys.exit("ledger_review: no Decision Ledger rows found")
    t = next((i for i, l in enumerate(lines) if "Tests by option" in l and not l.lstrip().startswith(">")
              and any(lines[j].lstrip().startswith("| Option") for j in range(i, min(i + 12, len(lines))))), None)
    tests = {}
    if t is None:
        sys.exit("ledger_review: no §7 'Tests by option' table found")
    for l in lines[t:]:
        m = re.match(r"^\|\s*\**([A-Z][A-Z-]*\d+[a-z])\**\s*\|", l)
        if m:
            c = cells(l)
            tests[m.group(1)] = {"raw": l, "retired": sorted(expand_ac(c[1]), key=lambda x: int(x[2:])),
                                 "changed": c[2] if len(c) > 2 else ""}
        elif tests and l.strip() and not l.lstrip().startswith("|"):
            break
    return {"rows": rows, "tests": tests, "file": spec.name}


def skipped_by(rows: list[dict], opt: str, row_id: str) -> list[str]:
    """Rows the gate skips when `opt` is chosen on `row_id` (directly or through a skipped row)."""
    skipped: list[str] = []
    for r in rows:
        if r["cond_row"] == row_id and opt not in r["cond_ids"]:
            skipped.append(r["id"])
        elif r["cond_row"] in skipped:
            skipped.append(r["id"])
    return skipped


def fact_sentence(n_retired: int, skips: list[str]) -> str:
    parts = []
    if n_retired:
        parts.append(f"{n_retired} test{'s' if n_retired > 1 else ''} no longer appl{'y' if n_retired > 1 else 'ies'}")
    if skips:
        k = len(skips)
        parts.append(f"**Skips {k} later question{'s' if k > 1 else ''}** ({', '.join(skips)})")
    return ". ".join(parts)


def labels(o: dict) -> str:
    marks = " ".join(x for x, on in (("✅", o["recommended"]), ("📘", o["course"])) if on)
    return " · ".join(x for x in (marks, o["status"]) if x)


def row_hash(r: dict, tests: dict) -> str:
    src = r["raw"] + "".join(tests.get(o["id"], {}).get("raw", "") for o in r["options"])
    return hashlib.sha1(src.encode()).hexdigest()[:12]


def previous_sections(text: str) -> dict:
    out, cur, buf = {}, None, []
    for l in text.splitlines():
        m = re.match(r"^<!-- ledger-review row=(\S+) src=(\S+) -->$", l)
        if m:
            if cur:
                out[cur] = buf
            cur, buf = (m.group(1), m.group(2)), [l]
        elif cur and (l.startswith("---") and buf and buf[-1] == ""):
            out[cur], cur, buf = buf, None, []
        elif cur:
            buf.append(l)
    if cur:
        out[cur] = buf
    return {k: "\n".join(v).rstrip("\n") for k, v in out.items()}


def skeleton(args) -> None:
    spec = Path(args.spec)
    d = parse(spec)
    rows, tests = d["rows"], d["tests"]
    prev = previous_sections(Path(args.previous).read_text()) if args.previous else {}
    name = args.name or spec.parent.name
    out = [f"<!-- ledger-review v1 file={args.spec} -->", HEADER.format(name=name, file=d["file"]).rstrip("\n"), ""]
    src = [f"# Sources for the slots — {args.spec}\n"]
    example = None
    for r in rows:
        h = row_hash(r, tests)
        if (r["id"], h) in prev:
            link = f"[{r['id']}]({args.link_base}#L{r['line']})" if args.link_base else r["id"]
            sec = re.sub(r"^### (?:\[[^\]]+\]\([^)]*\)|\S+) · ", f"### {link} · ", prev[(r["id"], h)], count=1, flags=re.M)
            out += [sec, ""]
            src.append(f"## {r['id']} — reused unchanged from the previous review\n")
            continue
        link = f"[{r['id']}]({args.link_base}#L{r['line']})" if args.link_base else r["id"]
        out.append(f"<!-- ledger-review row={r['id']} src={h} -->")
        out.append(f"### {link} · ⟦S1 {r['id']}: title⟧")
        asked = ""
        if r["cond_row"]:
            ids = r["cond_ids"]
            joined = ids[0] if len(ids) == 1 else ", ".join(ids[:-1]) + " or " + ids[-1]
            asked = f"*Asked only if {r['cond_row']} = {joined}.* "
        out.append(f"{asked}**The learner is asked:** ⟦S2 {r['id']}: question⟧ **Why it's a choice:** ⟦S3 {r['id']}: why⟧")
        out += ["", TABLE_HEAD]
        src += [f"## {r['id']}", f"- Decision cell: {r['decision']}", f"- Default cell: {r['default']}",
                f"- Trade-off cell: {r['tradeoff']}"]
        if r["cond_row"]:
            src.append(f"- Asked only if {r['cond_row']} is one of {', '.join(r['cond_ids'])}")
        for o in r["options"]:
            t = tests.get(o["id"])
            skips = skipped_by(rows, o["id"], r["id"])
            fact = fact_sentence(len(t["retired"]) if t else 0, skips)
            is_default = r["default"].startswith(o["id"]) or (not t)
            chosen = "—" if is_default and not fact else (f"⟦S5 {o['id']}: what it leaves out or changes⟧" + (f"; {fact}" if fact else ""))
            if not is_default:
                rank = (len(skips), len(t["retired"]) if t else 0)
                if example is None or rank > example[0]:
                    example = (rank, o["id"])
            out.append(f"| {o['id']} | ⟦S4 {o['id']}: option⟧ | ⟦S6 {o['id']}: setup⟧ | {labels(o)} | {chosen} |".replace("|  |", "| |"))
            src.append(f"- {o['id']} option cell: {o['text']}")
            if t:
                src.append(f"  - {o['id']} §7 line — no longer apply: {', '.join(t['retired']) or '—'}; changes: {t['changed']}")
            if fact:
                src.append(f"  - {o['id']} fixed sentence (the skeleton already holds it): {fact}")
        out.append("")
        src.append("")
    out.append(FOOTER.format(example=example[1] if example else rows[0]["options"][0]["id"]))
    o = Path(args.out)
    o.mkdir(parents=True, exist_ok=True)
    (o / "skeleton.md").write_text("\n".join(out) + "\n")
    (o / "sources.md").write_text("\n".join(src) + "\n")
    (o / "facts.json").write_text(json.dumps({"rows": [{k: v for k, v in r.items() if k != "raw"} for r in rows],
                                              "tests": {k: {"retired": v["retired"]} for k, v in tests.items()}}, indent=1))
    n_slots = sum(len(SLOT.findall(l)) for l in out)
    print(f"skeleton: {len(rows)} decisions, {sum(len(r['options']) for r in rows)} options, {n_slots} slots to fill -> {o}")


def check(args) -> int:
    sk = Path(args.skeleton).read_text().rstrip("\n").splitlines()
    dr = Path(args.draft).read_text().rstrip("\n").splitlines()
    if args.allow_unmarked:
        sk = [l for l in sk if not MARK.match(l)]
        dr = [l for l in dr if not MARK.match(l)]
    errors, i, j = [], 0, 0
    while i < len(sk) and j < len(dr):
        s, d = sk[i], dr[j]
        if s.startswith("⟦OPEN"):
            while j < len(dr) and not dr[j].startswith("*Reviewers:"):
                if dr[j].strip() and not re.match(r"^\d+\. ", dr[j]):
                    errors.append(f"draft line {j+1}: open points must be a numbered list")
                j += 1
            i += 1
            while i < len(sk) and sk[i] == "":
                i += 1
            continue
        pat = "^" + "".join("(.+?)" if SLOT.fullmatch(p) else re.escape(p) for p in re.split(r"(⟦[^⟧]*⟧)", s) if p) + "$"
        m = re.match(pat, d)
        if not m:
            errors.append(f"draft line {j+1} does not match skeleton line {i+1}:\n    expected: {s[:160]}\n    got:      {d[:160]}")
        else:
            for g in m.groups():
                if "⟦" in g or not g.strip():
                    errors.append(f"draft line {j+1}: a slot is empty or unfilled")
                for b in BANNED:
                    if re.search(b, g, re.I if b[0] == "\\" and b[1] == "b" else 0):
                        errors.append(f"draft line {j+1}: internal term /{b}/ in: {g[:80]}")
        i += 1
        j += 1
    if i < len(sk):
        errors.append(f"draft ends early; skeleton line {i+1} not reached: {sk[i][:100]}")
    if j < len(dr):
        errors.append(f"draft has extra lines from line {j+1}: {dr[j][:100]}")
    for e in errors:
        print("FAIL", e)
    print(f"check: {'PASS' if not errors else f'{len(errors)} problem(s)'}")
    return 1 if errors else 0


def previous(args) -> None:
    log = subprocess.run(["git", "log", "--first-parent", "--merges", "--format=%s", "--", args.path], capture_output=True, text=True).stdout
    for pr in re.findall(r"Merge pull request #(\d+)", log):
        if args.exclude_pr and pr == str(args.exclude_pr):
            continue
        res = subprocess.run(["gh", "api", f"repos/{{owner}}/{{repo}}/issues/{pr}/comments", "--paginate",
                              "-q", ".[].body"], capture_output=True, text=True)
        for body in res.stdout.split("<!-- ledger-review v1 file=")[1:]:
            if body.startswith(args.path + " "):
                print("<!-- ledger-review v1 file=" + body.rstrip())
                return


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("skeleton"); a.add_argument("spec"); a.add_argument("--out", required=True)
    a.add_argument("--name"); a.add_argument("--link-base"); a.add_argument("--previous")
    b = sub.add_parser("check"); b.add_argument("skeleton"); b.add_argument("draft"); b.add_argument("--allow-unmarked", action="store_true")
    c = sub.add_parser("previous"); c.add_argument("path"); c.add_argument("--exclude-pr", type=int)
    args = ap.parse_args()
    if args.cmd == "skeleton":
        skeleton(args)
        return 0
    if args.cmd == "check":
        return check(args)
    previous(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
