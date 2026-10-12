#!/usr/bin/env python3
"""check_spec.py — mechanical consistency checks for a generated spec.

Usage:
    python3 check_spec.py <spec.md> [--quiet]

Exit status 0 when no finding, 1 otherwise. Prints one finding per line:
    <line>: <CHECK> <message>

Checks (all over the whole file, by regex over Markdown — tolerant, not a parser):
  CITE-AC      every AC row cites >=1 business rule as (R<n>…)
  CITE-RULE    every business rule is cited by >=1 AC
  RECIP        every rule's trailing "→ AC…" list is reciprocated by those ACs, and every
               AC citation appears in that rule's list
  XREF         every R<n>, AC<n>, CTX-<x><n>, and Ledger-row reference names something that
               exists
  ROWID        no Ledger row id is a bare R<n> (rows and rules must not share a prefix)
  GUIDE-SECT   no §<n> reference that is not a section of this spec (guide sections leak)
  GUIDE-VOCAB  provenance vocabulary (litmus, lever, stakes, tier, substitution row, heavy
               bar, Never tier) is defined in a "How to read the provenance notes" paragraph
  FIXTURE      every fixtures/<path> an AC relies on is declared in §5 before the AC table
  NI-TAG       every "Not Included" handling tag is a class the scope-boundary row defines

Stdlib only. Written for the spec-build-lab guide's section template; it degrades to fewer
checks (never false confidence) when a section is missing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RULE_HEAD = re.compile(r"^\s*(?:\d+\.\s*|[-*]\s*)?\*{0,2}(R\d+)\b")
AC_ROW = re.compile(r"^\|\s*\**(AC[-A-Z]*\d+)\**(?=[\s*|(`])")
R_TOKEN = re.compile(r"(?<![A-Za-z])R(\d+)(?!\d)")
AC_TOKEN = re.compile(r"(?<![A-Za-z-])AC(?:-([A-Z]+))?(\d+)(?!\d)")
AC_RANGE = re.compile(r"AC(?:-([A-Z]+))?(\d+)\s*[–-]\s*(?:AC(?:-[A-Z]+)?)?(\d+)")
R_RANGE = re.compile(r"(?<![A-Za-z])R(\d+)\s*[–-]\s*R?(\d+)")
CTX_TOKEN = re.compile(r"CTX-([A-E])(\d*)")
SECT_TOKEN = re.compile(r"§\s*(\d+(?:\.\d+)?)")
HEADING = re.compile(r"^(#{1,4})\s+(.*)$")
FIXTURE_TOKEN = re.compile(r"`?(fixtures/[\w./-]+?)`?(?=[\s,;:)`|]|$)")
ROW_ID_CELL = re.compile(r"^\|\s*\**([A-Z][A-Z-]*\d+)\**\s*\|\s*\**([a-z-]+)\**\s*\|")
NI_TAG = re.compile(r"(?<!\*)\*([A-Z][^*\n]{2,80}?)\*(?!\*)")
TAG_WORDS = ("restorable", "buildable", "deferred", "defer", "unavailable", "keep")
VOCAB = ["litmus", "lever", "stakes", "tier", "substitution row", "heavy bar", "never tier"]


def expand_ac(text: str) -> set[str]:
    found: set[str] = set()
    for m in AC_RANGE.finditer(text):
        pre = f"AC-{m.group(1)}" if m.group(1) else "AC"
        a, b = int(m.group(2)), int(m.group(3))
        if a <= b <= a + 60:
            found.update(f"{pre}{i}" for i in range(a, b + 1))
    for m in AC_TOKEN.finditer(text):
        pre = f"AC-{m.group(1)}" if m.group(1) else "AC"
        found.add(f"{pre}{m.group(2)}")
    return found


def expand_r(text: str) -> set[int]:
    found: set[int] = set()
    for m in R_RANGE.finditer(text):
        a, b = int(m.group(1)), int(m.group(2))
        if a <= b <= a + 60:
            found.update(range(a, b + 1))
    for m in R_TOKEN.finditer(text):
        found.add(int(m.group(1)))
    return found


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    path = Path(argv[1])
    quiet = "--quiet" in argv
    lines = path.read_text(encoding="utf-8").splitlines()
    findings: list[tuple[int, str, str]] = []

    def add(ln: int, check: str, msg: str) -> None:
        findings.append((ln, check, msg))

    # ---- headings and section numbers of THIS spec ---------------------------------
    sections: set[str] = set()
    heading_lines: list[tuple[int, str]] = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING.match(line)
        if m:
            title = m.group(2).strip()
            heading_lines.append((i, title))
            sm = re.match(r"(\d+(?:\.\d+)?)[.\s]", title)
            if sm:
                sections.add(sm.group(1))

    def section_range(prefix_regex: str) -> tuple[int, int]:
        """Line range [start, end) of the first H2 heading matching the regex."""
        start = end = -1
        for idx, (ln, title) in enumerate(heading_lines):
            if start < 0 and re.match(prefix_regex, title):
                start = ln
                for ln2, t2 in heading_lines[idx + 1:]:
                    if lines[ln2 - 1].startswith("## "):
                        end = ln2
                        break
                if end < 0:
                    end = len(lines) + 1
                break
        return start, end

    # ---- business rules ------------------------------------------------------------
    rules_start, rules_end = section_range(r"4\.\s")
    rule_lines: dict[int, int] = {}
    rule_ptrs: dict[int, set[str]] = {}
    if rules_start > 0:
        current = None
        buf: list[str] = []

        def flush() -> None:
            if current is not None:
                text = " ".join(buf)
                tail = text.rsplit("→", 1)
                rule_ptrs[current] = expand_ac(tail[1]) if len(tail) == 2 else set()

        for i in range(rules_start, rules_end - 1):
            line = lines[i]
            m = RULE_HEAD.match(line)
            if m:
                flush()
                current = int(m.group(1)[1:])
                rule_lines[current] = i + 1
                buf = [line]
            elif current is not None:
                buf.append(line)
        flush()
    rules = set(rule_lines)

    # ---- acceptance criteria -------------------------------------------------------
    ac_start, ac_end = section_range(r"5\.\s")
    ac_lines: dict[str, int] = {}
    ac_cites: dict[str, set[int]] = {}
    ac_fixtures: dict[str, set[str]] = {}
    first_ac_line = len(lines) + 1
    for i in range(max(ac_start, 1), ac_end - 1):
        line = lines[i]
        m = AC_ROW.match(line)
        if m:
            ac = m.group(1)
            ac_lines[ac] = i + 1
            first_ac_line = min(first_ac_line, i + 1)
            # citations: everything in parentheses that contains R<n>, plus bare R<n> tokens
            ac_cites[ac] = expand_r(line)
            ac_fixtures[ac] = {f.strip("`") for f in FIXTURE_TOKEN.findall(line)}
    acs = set(ac_lines)

    # ---- CITE-AC / CITE-RULE / RECIP ------------------------------------------------
    cited_rules: set[int] = set()
    for ac, cites in ac_cites.items():
        valid = {r for r in cites if r in rules}
        if rules and not valid:
            add(ac_lines[ac], "CITE-AC", f"{ac} cites no business rule")
        cited_rules |= valid
    for r in sorted(rules - cited_rules):
        add(rule_lines[r], "CITE-RULE", f"R{r} is cited by no AC")
    for r, ptrs in rule_ptrs.items():
        for ac in sorted(ptrs):
            if ac not in acs:
                add(rule_lines[r], "XREF", f"R{r} points at {ac}, which does not exist")
            elif r not in ac_cites.get(ac, set()):
                add(rule_lines[r], "RECIP", f"R{r} → {ac}, but {ac} does not cite R{r}")
    for ac, cites in ac_cites.items():
        for r in sorted(cites):
            if r in rules and ac not in rule_ptrs.get(r, set()):
                add(ac_lines[ac], "RECIP", f"{ac} cites R{r}, but R{r}'s → list omits {ac}")

    # ---- Ledger rows ---------------------------------------------------------------
    ledger_start, ledger_end = section_range(r"Decision Ledger")
    row_ids: dict[str, int] = {}
    scope_row_text = ""
    if ledger_start > 0:
        for i in range(ledger_start, ledger_end - 1):
            m = ROW_ID_CELL.match(lines[i])
            if m:
                row_ids[m.group(1)] = i + 1
                if re.search(r"scope", lines[i], re.I) and "Not Included" in lines[i]:
                    scope_row_text = lines[i]
                if re.fullmatch(r"R\d+", m.group(1)):
                    add(i + 1, "ROWID", f"Ledger row id {m.group(1)} collides with the rule namespace")

    # ---- XREF over the whole file --------------------------------------------------
    ctx_entries: set[str] = set()
    for i, line in enumerate(lines):
        for m in re.finditer(r"\*\*(?:CTX-)?([BC])(\d+)\b", line):
            ctx_entries.add(f"{m.group(1)}{m.group(2)}")
        for m in re.finditer(r"^-\s*\*\*(?:CTX-)?([BC]\d+)", line):
            ctx_entries.add(m.group(1))
    max_rule = max(rules) if rules else 0
    for i, line in enumerate(lines, 1):
        if lines[i - 1].startswith("#"):
            continue
        for m in R_TOKEN.finditer(line):
            n = int(m.group(1))
            if rules and n > max_rule:
                add(i, "XREF", f"R{n} does not exist (rules run R1–R{max_rule})")
        for ac in expand_ac(line):
            if acs and ac not in acs:
                add(i, "XREF", f"{ac} does not exist")
        for m in CTX_TOKEN.finditer(line):
            letter, num = m.group(1), m.group(2)
            if num and letter in "BC" and f"{letter}{num}" not in ctx_entries and ctx_entries:
                add(i, "XREF", f"CTX-{letter}{num} has no entry")
        for m in re.finditer(r"(?:rows?|→)\s+((?:D-[A-Z]\d+|D\d+|L\d+|RR\d+|C\d+)(?:\s*[,/]\s*(?:D-[A-Z]\d+|D\d+|L\d+|RR\d+|C\d+))*)", line):
            for tok in re.split(r"\s*[,/]\s*", m.group(1)):
                if row_ids and tok not in row_ids:
                    add(i, "XREF", f"Ledger row {tok} does not exist")

    # ---- GUIDE-SECT ----------------------------------------------------------------
    for i, line in enumerate(lines, 1):
        for m in SECT_TOKEN.finditer(line):
            s = m.group(1)
            if s not in sections and s.split(".")[0] not in sections:
                add(i, "GUIDE-SECT", f"§{s} is not a section of this spec")

    # ---- GUIDE-VOCAB ---------------------------------------------------------------
    text_lower = "\n".join(lines).lower()
    howto = re.search(r"how to read the provenance notes(.{0,4000})", text_lower, re.S)
    for term in VOCAB:
        if term in text_lower:
            if not howto:
                add(0, "GUIDE-VOCAB", f'"{term}" is used but no "How to read the provenance notes" paragraph defines it')
            elif term not in howto.group(1):
                add(0, "GUIDE-VOCAB", f'"{term}" is used but not defined in the provenance-notes paragraph')

    # ---- FIXTURE -------------------------------------------------------------------
    if ac_start > 0 and first_ac_line <= len(lines):
        corpus = "\n".join(lines[ac_start - 1:first_ac_line - 1])
        declared = {f.strip("`") for f in FIXTURE_TOKEN.findall(corpus)}
        declared_names = {Path(d).name for d in declared} | {d.rstrip("/").split("/")[-1] for d in declared}
        for ac, fx in ac_fixtures.items():
            for f in sorted(fx):
                name = Path(f).name or f.rstrip("/").split("/")[-1]
                if f not in declared and name not in declared_names:
                    add(ac_lines[ac], "FIXTURE", f"{ac} relies on {f}, not declared in the §5 fixture corpus")

    # ---- NI-TAG --------------------------------------------------------------------
    ni_start, ni_end = -1, -1
    for idx, (ln, title) in enumerate(heading_lines):
        if "Not Included" in title:
            ni_start = ln
            ni_end = heading_lines[idx + 1][0] if idx + 1 < len(heading_lines) else len(lines) + 1
            break
    if ni_start > 0 and scope_row_text:
        classes = {c.lower()[:5] for c in re.findall(r"(?<!\*)\*([a-z][a-z -]+?)\*(?!\*)", scope_row_text)}
        classes = {c for c in classes if any(c.startswith(w[:5]) for w in TAG_WORDS)}
        for i in range(ni_start, ni_end - 1):
            for m in NI_TAG.finditer(lines[i]):
                tag = m.group(1).strip()
                head = tag.lower().split(";")[0].split("(")[0].split(",")[0].strip().rstrip(".")
                is_tag = any(head.startswith(w) for w in TAG_WORDS) or (
                    tag.endswith(".") and len(tag.split()) <= 6 and tag[0].isupper())
                if not is_tag:
                    continue
                if classes and not any(head.startswith(c) for c in classes):
                    add(i + 1, "NI-TAG", f'tag "{tag}" is not a class the scope-boundary row defines')

    findings.sort()
    if not quiet:
        for ln, check, msg in findings:
            print(f"{ln}: {check} {msg}")
    print(f"{path.name}: {len(findings)} finding(s); rules={len(rules)} ACs={len(acs)} rows={len(row_ids)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
