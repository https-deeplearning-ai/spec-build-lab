# Fix log — lab spec, audit 2 (21 items)

Spec: courses/loop-engineering-with-langchain-deepagents/spec.coding-agent-lab.md
No Ledger row, Options entry, Default, "(course default)" label, trade-off disposition or rule meaning changed.

1. SKIPPED (orchestrator) — RR1 (b) vs the Invariant's "model responses the suite controls"; owner decision, issue #38 item 2. RR1 Options/Invariant untouched.
2. First half SKIPPED (orchestrator) — RR1 (b) vs R24 / §6 Always; R24 and the Always entry untouched, AC34 named in neither list. Second half APPLIED — RR1 (b) now lists, in D2's form, the criteria that exercise only the scripted Default (AC2 step-1, AC3, AC4, AC5, AC6, AC7, AC9, AC12–AC14, AC15, AC16, AC18 banner, AC20 count, AC22 tallies, AC24, AC26, AC27, AC29, AC30, AC41, AC42) and the ones that stand (AC1, AC8, AC10, AC11, AC17, AC19, AC21, AC23, AC25, AC28, AC31–AC33, AC35–AC37, AC39, AC40, plus AC38's structural assertions).
3. APPLIED — D2 (b)'s does-not-apply list gains "AC16 entirely" (scripted grader raising on the `(GRADER-ERROR)` title; a code grader never errors; R10 reached via the `batch_with_error` fixture, AC17). Option kept.
4. APPLIED — AC22 now states the exact 16-row trace of AC12's run (rows 1–12 alternating for fetch/write/4 edits, row 13 turn-7 `Finishes the review` with no tool row, rows 14–15 revision edit + result, row 16 turn-9 `Finishes the review`; no two Tool rows adjacent). R14's parenthetical reworded from "alternating" to the same property. Run unchanged.
5. APPLIED — dropped the `status: satisfied → missing maxItems 0 / in_order const true` branch from the `AnalysisRun` schema; R5 gains the sentence that no contract constraint ties `in_order`/`missing` to a grading status and that AC7 asserts the scripted run's values. "Recorded, never enforced" wins.
6. APPLIED — §5 Scripted models: "Recorded model string" — scripted mode records `model` = `scripted` on every run record and batch summary whatever the role variables hold; live mode records `REVIEW_MODEL`; `scripted` is not in R19's table. AC30's cost assertion now cites it.
7. APPLIED (re-target option) — new §5 paragraph "Denied file operations in the trace": the app's trace writer records a file-tool call the app's own permission rules deny as a `Tool` row with action `Denied by permission: <path>`; detail stays the harness text, never asserted. AC9 asserts action `Denied by permission: /memories/AGENTS.md`; AC27 asserts `Denied by permission: /oneoff/summary.json`.
8. APPLIED — `FIXTURE_BATCHES` copies each directory into the batch store `data/batches/<label>/` at registration (replacing an earlier copy) and serves the copy; fixture directories are never written to; the computed `summary.json` goes into the copy. R16 names `data/batches/<label>/` as the batch directory, R17 says the proposal files go to the copy for a registered fixture batch, §2 store row names the path. AC17 Given and AC27 Then re-targeted at the copy; AC27 adds "fixtures/batch_one_off/ gained no file".
9. APPLIED — Environment Resolutions: "R12 (AC18–AC20)" → "R12 (AC3, AC19, AC20)".
10. APPLIED — "How to read the provenance notes" defines `narrative` (framing/taxonomy a course never argued as a builder's choice; not a disposition; carried so the omission is visible).
11. SKIPPED (orchestrator) — the tie-breaker-2/degenerate-case wording on the verification row; open owner decision, not reworded, relabelled or moved.
12. APPLIED — removed "turn caps 12/40 (R3)" from the §4 body-levers list (table disposition bake-in R3 unchanged).
13. APPLIED — EF4 ends "Enforced by R25, AC40 (the floor); the batched, announced install is a §6 Always entry that no criterion checks."
14. APPLIED — §14 contradictions: memory file name → `AGENTS.md`, lever branch (2) (narration conflicts with itself — transcripts carry both spellings — so the application's config decides; contract-participating via R6); batch-document count → five, lever branch (2) (introducing narration states both values).
15. APPLIED — §1 item 13 kept its `unavailable` tag: L1's stated meaning "cannot be restored in this lab" is exactly the item's reason (the lab fixes the assignment); wording now says "`unavailable` in row L1's sense (cannot be restored in this lab)" and "no gate answer can bring it back". Item not deleted.
16. APPLIED — §1 items 6, 8, 9 end with "Buildable, but this spec supplies no parameters and no acceptance criteria for it/them."
17. APPLIED — R15 anchored "(CTX-B12, CTX-C)".
18. APPLIED — M defined once in the step-2 paragraph: the Ledger's row count plus one (M = 5), step-2 question is "Question 1 of 5", baseline path ends after Question 1; step-3 paragraph refers to that M, rows are Questions 2 … M.
19. APPLIED — R1: "stores the provenance of that text as `requirement_page_id` + `requirement_version` (the text itself survives as the fetch tool's result among `messages`, R14)"; `requirement_doc` removed.
20. APPLIED — §2: the harness row's note now states the course's install situation (floors in project file / exact resolutions in uv.lock; this spec pins the lock) AND points era-specific names to CTX-D; the companions row says "pinned by the harness row's rule" and no longer restates it.
21. APPLIED — new §5 paragraph "Fixture run file": every `run_*.json` under fixtures/ is a complete, schema-valid `AnalysisRun` (fields listed; a `needs_revision` first pass is followed by one `satisfied` pass so status follows R9; `grader_error` when the only pass errors); `FIXTURE_BATCHES` registration validates each against the schema and refuses the label naming the file. Compare, grader-error and one-off fixtures now say "fixture run file".

## Checker
python3 .claude/skills/generate-spec/scripts/check_spec.py <spec>
→ spec.coding-agent-lab.md: 0 finding(s); rules=25 ACs=42 rows=4

Check (a) rule↔AC reciprocity (own script): rules=25 acs=42 reciprocity violations=0

## Citation counts (occurrences of each id in the spec)
AC1:6 AC2:5 AC3:7 AC4:4 AC5:9 AC6:3 AC7:4 AC8:7 AC9:4 AC10:6 AC11:6 AC12:15 AC13:5 AC14:4 AC15:6 AC16:5 AC17:6 AC18:4 AC19:6 AC20:10 AC21:4 AC22:4 AC23:4 AC24:9 AC25:3 AC26:7 AC27:4 AC28:6 AC29:7 AC30:3 AC31:3 AC32:2 AC33:4 AC34:6 AC35:5 AC36:3 AC37:5 AC38:8 AC39:4 AC40:5 AC41:4 AC42:8
R1:3 R2:8 R3:7 R4:5 R5:4 R6:14 R7:7 R8:9 R9:19 R10:6 R11:5 R12:14 R13:12 R14:11 R15:6 R16:13 R17:17 R18:15 R19:17 R20:15 R21:10 R22:4 R23:4 R24:2 R25:4
