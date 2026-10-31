#!/usr/bin/env python3
"""ledger_review.py — the deterministic half of /ledger-review.

  skeleton <spec.md> --out DIR [--path P] [--name NAME] [--link-base URL] [--previous FILE]
      (--path: the spec's repo-relative path, recorded in the hidden marker so `previous` finds it)
      Writes DIR/skeleton.md (every fixed and factual part of the review comment, with ⟦…⟧ slots
      for the plain-language wording) and DIR/sources.md (the spec text each slot is written from).
      Sections whose source is unchanged since --previous (an earlier review comment) are copied
      from it verbatim and carry no slots.
  check <skeleton.md> <draft.md> [--allow-unmarked]
      Fails unless the draft matches the skeleton line for line: every fixed part identical, every
      slot filled, no internal term in any slot. --allow-unmarked skips the hidden <!-- --> markers
      (only for comparing against a comment written before the markers existed).
  previous <repo-relative spec path> [--exclude-pr N]
      Prints the most recent earlier review for this spec file (one PR comment, or the review
      comments of one review joined in order), found through the merged PRs that touched it;
      prints nothing if there is none.
  split <draft.md> <spec.md> --path P --commit SHA --diff PR.diff --out DIR
      Turns a checked draft into what gets posted. When the Ledger table's header lines and every
      row line are in the PR's diff: DIR/review.json, one review with the header comment on the
      table's header lines and one comment per decision on its row (a second spec file appends to
      the same review.json). Otherwise: DIR/file-comment-<file>.json, the whole draft as one comment
      on the file.
  verify <PR> <review id> <review.json>
      Fails unless every comment of the review sits as a thread on the lines review.json asked for.
  questions <spec.md> --path P --commit SHA --diff PR.diff --out DIR [--name NAME] [--link-base URL] [--pr-body FILE]
      For a guide-v2 spec ("## 1. Questions" with "### Cn." questions): the whole review, written by
      the script alone in the spec's own words. DIR/review.md is the review to show; it is posted
      like `split`'s output (DIR/review.json: an overview comment on the "## 1. Questions" line and
      one comment per question on its lines; or DIR/file-comment-<file>.json when those lines are
      not all in the diff).

Stdlib only. Parsing follows the spec-generation guide's Decision Ledger and §7 "Tests by option"
formats, or guide v2's Questions section; it degrades loudly (exit 2) when a spec has neither.
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

*Reviewers: reply in the thread on each decision's row (for example under {example}); use this thread for the review as a whole.*"""
FILE_FOOTER = '*Reviewers: reply in this thread, starting with the Ref (for example "{example}: …").*'


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
    out = [f"<!-- ledger-review v1 file={args.path or args.spec} -->", HEADER.format(name=name, file=d["file"]).rstrip("\n"), ""]
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


def reviews_path(body: str, path: str) -> bool:
    """Whether a review comment (its text after the v1 marker's "file=") is about the spec at `path`.
    Older comments recorded the scratch copy's path in the marker, so their row links decide."""
    return body.startswith(path + " ") or f"/{path}#L" in body


def previous(args) -> None:
    log = subprocess.run(["git", "log", "--first-parent", "--merges", "--format=%s", "--", args.path], capture_output=True, text=True).stdout
    for pr in re.findall(r"Merge pull request #(\d+)", log):
        if args.exclude_pr and pr == str(args.exclude_pr):
            continue
        res = subprocess.run(["gh", "api", f"repos/{{owner}}/{{repo}}/pulls/{pr}/comments", "--paginate",
                              "-q", f'.[] | select(.path == "{args.path}" and .in_reply_to_id == null) | [.pull_request_review_id, .id, .body]'],
                             capture_output=True, text=True)
        found = [json.loads(l) for l in res.stdout.splitlines() if l.strip()]
        found = [c for c in found if "<!-- ledger-review " in c[2]]
        if found:
            last = max(c[0] for c in found)
            # "---" between comments ends each row's section, as in a single PR comment
            print("\n\n---\n\n".join(c[2].rstrip() for c in sorted(c for c in found if c[0] == last)))
            return
        res = subprocess.run(["gh", "api", f"repos/{{owner}}/{{repo}}/issues/{pr}/comments", "--paginate",
                              "-q", ".[].body"], capture_output=True, text=True)
        for body in res.stdout.split("<!-- ledger-review v1 file=")[1:]:
            if reviews_path(body, args.path):
                print("<!-- ledger-review v1 file=" + body.rstrip())
                return


def diff_lines(diff: str, path: str) -> set[int]:
    """New-side line numbers of `path` that the PR diff shows (added or context): the lines a review comment can sit on."""
    out, cur, n = set(), None, 0
    for l in diff.splitlines():
        if l.startswith("diff --git "):
            cur = l.split(" b/", 1)[1] if " b/" in l else None
        elif cur == path and l.startswith("@@"):
            n = int(re.match(r"@@ -\S+ \+(\d+)", l).group(1))
        elif cur == path and n and l[:1] in (" ", "+") and not l.startswith("+++"):
            out.add(n)
            n += 1
    return out


def split(args) -> None:
    draft = Path(args.draft).read_text().rstrip("\n").split("\n")
    spec = Path(args.spec).read_text(encoding="utf-8").splitlines()
    rows = parse(Path(args.spec))["rows"]
    head = rows[0]["line"] - 1
    while head > 1 and spec[head - 2].lstrip().startswith("|"):
        head -= 1
    anchors = [head, head + 1] + [r["line"] for r in rows]
    shown = diff_lines(Path(args.diff).read_text(), args.path)
    o = Path(args.out)
    o.mkdir(parents=True, exist_ok=True)
    missing = [a for a in anchors if a not in shown]
    if missing:
        body = "\n".join(re.sub(r"^\*Reviewers: .*\(for example under (\S+)\);.*$",
                                lambda m: FILE_FOOTER.format(example=m.group(1)), l) for l in draft)
        out = o / f"file-comment-{Path(args.path).name}.json"
        out.write_text(json.dumps({"body": body, "commit_id": args.commit, "path": args.path, "subject_type": "file"}))
        print(f"split: file comment ({len(missing)} of {len(anchors)} Ledger lines not in the diff, e.g. line {missing[0]}) -> {out}")
        return
    marks = [i for i, l in enumerate(draft) if l.startswith("<!-- ledger-review row=")]
    sep = max(i for i, l in enumerate(draft) if l == "---")
    header = "\n".join(draft[:marks[0]]).rstrip("-\n ") + "\n\n" + "\n".join(draft[sep + 1:]).strip()
    comments = [{"path": args.path, "start_line": head, "start_side": "RIGHT", "line": head + 1, "side": "RIGHT", "body": header}]
    for k, m in enumerate(marks):
        body = "\n".join(draft[m:marks[k + 1] if k + 1 < len(marks) else sep]).strip()
        rid, line = re.search(r"^### \[(\S+?)\]\([^)]*#L(\d+)\)", body, re.M).groups()
        if not spec[int(line) - 1].startswith(f"| {rid} |") and not spec[int(line) - 1].startswith(f"| **{rid}** |"):
            sys.exit(f"split: {rid}'s link points at line {line}, which is not its row")
        comments.append({"path": args.path, "line": int(line), "side": "RIGHT", "body": body})
    out = o / "review.json"
    review = json.loads(out.read_text()) if out.exists() else {"commit_id": args.commit, "comments": []}
    if review["commit_id"] != args.commit:
        sys.exit(f"split: {out} is for commit {review['commit_id']}, not {args.commit}")
    review["comments"] += comments
    out.write_text(json.dumps(review))
    print(f"split: threads, {len(comments)} comments for {args.path} (lines {head}-{rows[-1]['line']}) -> {out}")


def verify(args) -> int:
    q = ('query($n:Int!){repository(owner:"%s",name:"%s"){pullRequest(number:$n){reviewThreads(first:100){nodes'
         '{path startLine line comments(first:1){nodes{pullRequestReview{databaseId}}}}}}}}')
    repo = subprocess.run(["gh", "repo", "view", "--json", "owner,name", "-q", '.owner.login + " " + .name'],
                          capture_output=True, text=True).stdout.split()
    res = subprocess.run(["gh", "api", "graphql", "-F", f"n={args.pr}", "-f", "query=" + q % tuple(repo)],
                         capture_output=True, text=True)
    nodes = json.loads(res.stdout)["data"]["repository"]["pullRequest"]["reviewThreads"]["nodes"]
    got = sorted((t["path"], t["startLine"] or t["line"], t["line"]) for t in nodes
                 if t["comments"]["nodes"] and (t["comments"]["nodes"][0]["pullRequestReview"] or {}).get("databaseId") == args.review)
    want = sorted((c["path"], c.get("start_line", c["line"]), c["line"]) for c in json.loads(Path(args.plan).read_text())["comments"])
    for w in want:
        if w not in got:
            print(f"FAIL no thread at {w[0]} lines {w[1]}-{w[2]}")
    for g in got:
        if g not in want:
            print(f"FAIL unexpected thread at {g[0]} lines {g[1]}-{g[2]}")
    ok = got == want
    print(f"verify: {'PASS' if ok else 'FAIL'} ({sum(w in got for w in want)} of {len(want)} threads in place)")
    return 0 if ok else 1


Q_HEAD = re.compile(r"^### (C\d+)\.\s+(.*)$")
OPT = re.compile(r"^- \*\*(C\d+[a-z])\b")
ASK = re.compile(r"\s*(?:—\s*)?\*Ask only when (.*?)\*\s*$")
# Where the spec's own wording of an option starts each part: (column, the spec's words for it)
PARTS = [("when", r"\*?Pick this when\*?:?"), ("setup", r"\*?Setup(?: cost)?:\*?"), ("cost", r"\*?Cost:\*?"),
         ("check", r"\*?What to check:\*?")]
Q_INTRO = """## Questions for review: {name}

The questions the build agent asks the learner before building, copied from this PR's `{file}` in the spec's own words. Each question has its own thread on its lines; reply there.

- ✅ **Recommended**: what the default build uses.
- 📘 **Course default**: what the course itself did.
- **What to check**: how the build proves an option other than the recommended one works.
"""


def flat(text: str) -> list[str]:
    """The words of a piece of spec text, sorted, without punctuation or markdown: to prove no word was dropped."""
    return sorted(re.findall(r"\w+", text))


def parse_questions(spec: Path) -> list[dict]:
    lines = spec.read_text(encoding="utf-8").splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if re.match(r"^## 1\. Questions\b", l))
    except StopIteration:
        sys.exit(f"questions: {spec} has no '## 1. Questions' section")
    qs, cur, opt = [], None, None
    for i in range(start + 1, len(lines)):
        l = lines[i]
        if l.startswith("## ") or l.strip() == "---":
            break
        m = Q_HEAD.match(l)
        if m:
            ask = ASK.search(m.group(2))
            cur = {"id": m.group(1), "title": m.group(2)[:ask.start()] if ask else m.group(2), "ask": ask.group(1) if ask else "",
                   "line": i + 1, "end": i + 1, "options": []}
            qs.append(cur)
            opt = None
            continue
        if cur is None or not l.strip():
            continue
        if OPT.match(l):
            opt = {"id": OPT.match(l).group(1), "text": l[2:].strip()}
            cur["options"].append(opt)
        elif opt is None and ASK.fullmatch(l):
            cur["ask"] = ASK.fullmatch(l).group(1)
        elif opt is not None and l.startswith(" "):
            opt["text"] += " " + re.sub(r"^-\s+", "", l.strip())
        else:
            sys.exit(f"questions: line {i + 1} of {spec} is neither an option nor part of one: {l[:80]}")
        cur["end"] = i + 1
    if not qs or any(not q["options"] for q in qs):
        sys.exit(f"questions: no questions, or a question without options, in {spec}")
    for q in qs:
        for o in q["options"]:
            o.update(split_option(o["text"]))
    return qs


def split_option(text: str) -> dict:
    """An option's own text cut into its parts at the spec's own words ("Pick this when", "Setup:"...).
    Exits if the parts, put back together, are not exactly the option's words."""
    m = re.match(r"\*\*(C\d+[a-z])\s*(.*?)\*\*\s*(.*)$", text)
    oid, bold, rest = m.groups()
    tags = re.search(r"\(([^)]*(?:Recommended|course default)[^)]*)\)", bold + " " + rest[:80])
    lab = tags.group(1) if tags else ""
    labels = (["✅ Recommended"] if "Recommended" in lab else []) + (["📘 Course default"] if "course default" in lab.lower() else [])
    gist = bold + ("" if re.match(r"[,.;:]", rest) else " ") + rest
    gist = gist.replace(f"({lab})", "", 1) if tags else gist
    gist = re.sub(r"^\s*[—:–-]\s*", "", gist.strip())
    cuts = sorted((mm.start(), mm.end(), col) for col, pat in PARTS for mm in re.finditer(r"(?<![\w(])" + pat, gist))
    pieces = [("gist", gist[:cuts[0][0]] if cuts else gist)]
    pieces += [(col, gist[e:cuts[k + 1][0] if k + 1 < len(cuts) else len(gist)]) for k, (_, e, col) in enumerate(cuts)]
    out = {"labels": labels}
    for col, piece in pieces:
        out[col] = (out.get(col, "") + " " + piece.strip()).strip()
    # Put back together, the parts must be the option's words, minus only its id, labels and the part names
    words = flat(f"{oid} " + f"({lab}) " * bool(tags) + " ".join(p for _, p in pieces))
    origin = flat(re.sub(r"(?<![\w(])(?:" + "|".join(p for _, p in PARTS) + ")", "", text))
    if words != origin:
        sys.exit(f"questions: could not split option {oid} without losing words:\n  {text}")
    return out


def cell(s: str) -> str:
    return s.replace("|", "\\|").strip() or "—"


def question_body(q: dict, link: str) -> str:
    head = f"### [{q['id']}. {q['title'].strip()}]({link}#L{q['line']})" if link else f"### {q['id']}. {q['title'].strip()}"
    out = [f"<!-- ledger-review q={q['id']} -->", head]
    if q["ask"]:
        out.append(f"*Asked only when {q['ask']}*")
    out += ["", "| Option | What you get | Pick this when | Setup and cost | What to check |", "|---|---|---|---|---|"]
    for o in q["options"]:
        setup = o.get("setup", "") + (f" Cost: {o['cost']}" if o.get("cost") else "")
        out.append(f"| **{o['id']}**{'<br>' + '<br>'.join(o['labels']) if o['labels'] else ''} | {cell(o['gist'])} | "
                   f"{cell(o.get('when', ''))} | {cell(setup)} | {cell(o.get('check', ''))} |")
    return "\n".join(out)


def questions(args) -> None:
    qs = parse_questions(Path(args.spec))
    spec = Path(args.spec).read_text(encoding="utf-8").splitlines()
    qline = next(i + 1 for i, l in enumerate(spec) if re.match(r"^## 1\. Questions\b", l))
    link = args.link_base or ""
    name = args.name or Path(args.path).parent.name
    def rec(q):
        return ", ".join(o["id"] for o in q["options"] if "✅ Recommended" in o["labels"]) or "—"
    def course(q):
        return ", ".join(o["id"] for o in q["options"] if "📘 Course default" in o["labels"]) or "—"
    over = [f"<!-- ledger-review v2 file={args.path} -->", Q_INTRO.format(name=name, file=Path(args.path).name),
            f"**{len(qs)} questions**, {sum(1 for q in qs if q['ask'])} of them asked only after a certain earlier answer."]
    intro = []
    for l in spec[qline:]:
        if Q_HEAD.match(l):
            break
        intro.append(l)
    if "".join(intro).strip():
        over += ["", "From the spec: " + " ".join(l.strip() for l in intro if l.strip())]
    over += ["",
            "| Question | Options | ✅ Recommended | 📘 Course default | Asked only when |", "|---|---|---|---|---|"]
    for q in qs:
        title = f"[{q['id']}. {q['title'].strip()}]({link}#L{q['line']})" if link else f"{q['id']}. {q['title'].strip()}"
        over.append(f"| {cell(title)} | {len(q['options'])} | {rec(q)} | {course(q)} | {cell(q['ask'])} |")
    if args.pr_body:
        body = Path(args.pr_body).read_text()
        # A heading "… open points …" with the text under it, or a bullet / bold line
        # "Known open points …:" followed by the points on the same line and any indented lines after it.
        m = re.search(r"^#+\s*([^\n]*open (?:point|question)s?[^\n]*)\n(.*?)(?=^#+\s|\Z)", body, re.I | re.M | re.S)
        if m:
            title, text = m.group(1).strip(), m.group(2).strip()
        else:
            b = re.search(r"^[ \t]*(?:[-*]\s+)?\*{0,2}([^\n:]*open (?:point|question)s?[^\n:]*):?\*{0,2}:?\s*([^\n]*)((?:\n[ \t]+\S[^\n]*)*)", body, re.I | re.M)
            title, text = (b.group(1).strip(), (b.group(2) + b.group(3)).strip()) if b else ("", "")
        over += ["", f"### {title} (from the PR description)", text] if text else \
                ["", "### Known open points", "None listed in this PR's description."]
    over += ["", "*Reviewers: reply in the thread on each question's lines (for example under C1); use this thread for the review as a whole.*"]
    overview = "\n".join(over)
    bodies = [question_body(q, link) for q in qs]
    o = Path(args.out)
    o.mkdir(parents=True, exist_ok=True)
    (o / "review.md").write_text(overview + "\n\n---\n\n" + "\n\n---\n\n".join(bodies) + "\n")
    shown = diff_lines(Path(args.diff).read_text(), args.path)
    need = [qline] + [n for q in qs for n in range(q["line"], q["end"] + 1)]
    missing = [n for n in need if n not in shown]
    if missing:
        body = overview.replace(over[-1], '*Reviewers: reply in this thread, starting with the question (for example "C1: …").*') + \
            "\n\n---\n\n" + "\n\n---\n\n".join(bodies)
        out = o / f"file-comment-{Path(args.path).name}.json"
        out.write_text(json.dumps({"body": body, "commit_id": args.commit, "path": args.path, "subject_type": "file"}))
        print(f"questions: file comment ({len(missing)} question lines not in the diff, e.g. line {missing[0]}) -> {out}")
        return
    comments = [{"path": args.path, "line": qline, "side": "RIGHT", "body": overview}]
    for q, b in zip(qs, bodies):
        c = {"path": args.path, "line": q["end"], "side": "RIGHT", "body": b}
        if q["end"] > q["line"]:
            c.update(start_line=q["line"], start_side="RIGHT")
        comments.append(c)
    out = o / "review.json"
    review = json.loads(out.read_text()) if out.exists() else {"commit_id": args.commit, "comments": []}
    if review["commit_id"] != args.commit:
        sys.exit(f"questions: {out} is for commit {review['commit_id']}, not {args.commit}")
    review["comments"] += comments
    out.write_text(json.dumps(review))
    print(f"questions: threads, {len(comments)} comments for {args.path} ({len(qs)} questions, lines {qline}-{qs[-1]['end']}) -> {out}")


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("skeleton"); a.add_argument("spec"); a.add_argument("--out", required=True)
    a.add_argument("--name"); a.add_argument("--link-base"); a.add_argument("--previous"); a.add_argument("--path")
    b = sub.add_parser("check"); b.add_argument("skeleton"); b.add_argument("draft"); b.add_argument("--allow-unmarked", action="store_true")
    c = sub.add_parser("previous"); c.add_argument("path"); c.add_argument("--exclude-pr", type=int)
    d = sub.add_parser("split"); d.add_argument("draft"); d.add_argument("spec"); d.add_argument("--path", required=True)
    d.add_argument("--commit", required=True); d.add_argument("--diff", required=True); d.add_argument("--out", required=True)
    e = sub.add_parser("verify"); e.add_argument("pr", type=int); e.add_argument("review", type=int); e.add_argument("plan")
    f = sub.add_parser("questions"); f.add_argument("spec"); f.add_argument("--path", required=True)
    f.add_argument("--commit", required=True); f.add_argument("--diff", required=True); f.add_argument("--out", required=True)
    f.add_argument("--name"); f.add_argument("--link-base"); f.add_argument("--pr-body")
    args = ap.parse_args()
    if args.cmd == "questions":
        questions(args)
        return 0
    if args.cmd == "skeleton":
        skeleton(args)
        return 0
    if args.cmd == "check":
        return check(args)
    if args.cmd == "split":
        split(args)
        return 0
    if args.cmd == "verify":
        return verify(args)
    previous(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
