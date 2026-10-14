# Fix log — lab spec E, audit 2 (repair pass 2)

Spec: courses/loop-engineering-with-langchain-deepagents/spec.coding-agent-lab.md
Applied 21 / skipped 1. No Decision Ledger row, Option, Default, "(course default)" label, Invariant or trade-off disposition was added, removed, renamed or relabelled.

1. SKIPPED — orchestrator instruction (owner decision, issue #38 item 2); RR1 Options/Invariant untouched.
2. applied — RR1 (b) exact-value list now: AC1, AC3, AC4, AC7, AC8, AC10–AC20, AC22, AC28, AC30–AC35, AC45–AC47, AC50, AC51 (added on replay: AC8, AC15, AC16, AC30, AC31, AC34, AC50, AC51; AC12 was already inside AC10–AC14).
3. applied — D2 (b) (a)-only list adds AC50 (its Given presupposes AC46's `success`); AC51 joins the "keep trace/workspace assertions, status `ungraded`" group with its grading clause dropped; AC12's and AC41's batch `v1` noted as running ungraded.
4. applied — chose replayability over restricting AC46: D1 (b) now states the §5.1 scripted review role reads `/skills/ambiguities/SKILL.md` with one extra `read_file` turn immediately before its first Ambiguities edit and keys its labelled lines on `Resolved by:` in that body; AC46 holds under (b); AC18 `turns` +1 and AC19 rows +2 under (b). Mirrored in the §5.1 review-role text.
5. applied — D1 (b) declares the skills directory as `/skills/<section>/SKILL.md` in the run workspace (`confirmed_facts`, `ambiguities`, `clarification_questions`, `assumptions`), write-denied like `/memories/**`; R7 now denies writes under `/skills/**` under D1 (b).
6. applied — R12 redefines `turns` as every model message (tool-calling and completion sentences, one per `Model reasoning` row) with the derivation 7 + 2 = 9 for the default run and 6 + 1 = 7 without a grader; AC19 keeps 9 and states the derivation; AC18 keeps 7 and states it; AC7 asserts `turns` = 12. R12 → AC18, AC19.
7. applied — §5.1 and R20 declare the batch documents as exactly the five numbered files `01_…`–`05_…`; `UPL-310.md` is never a batch document; AC33 says "none for `UPL-310.md`".
8. applied — R10: the grader receives the rubric text and the requirement text the run fetched (`requirement_doc`) in its own prompt, never through the agent's conversation; the scripted grader takes the title from the `REQUIREMENT:` line and the clause count from the following lines; AC15 invokes the grader with `fixtures/rubric.txt` and the requirement text of `UPL-310.md` (and asserts completeness passed, 3 facts / 3 clauses); AC20 names where the title came from.
9. applied — §5.1 declares failure text 1 `Error: 503 Service Unavailable — the tracker is busy, retry` and failure text 2 `Error: request timed out after 30 s`, returned in order for the first N calls under `FETCH_FAILURES`; AC3 asserts rows 2 and 4 begin with those texts; R2 points at them.
10. applied — new fixture `fixtures/stale_workspace/` (`analysis.md` = `complete_v2.md`, `memories/AGENTS.md` = `instructions_v1.md`); new AC51 copies it to `<WORKSPACE_ROOT>/stale/`, runs a direct run, asserts a different workspace, first file call `write_file`, stale copy untouched, grading pass 1 `needs_revision`. R9 → AC12, AC51; CTX-B7 "Enforced by R9, AC12, AC51. Planted instance: fixtures/stale_workspace/".
11. applied — T10 names the rule: generator's reading (spoken heuristic quantified → post-build lever, never a row); disposition unchanged (lever R18).
12. applied — T4 names the rule: constrained-dimension lever (model/provider CONSTRAINED → body lever with Ask-First entry); disposition unchanged (lever R22).
13. applied — table intro now "Mined spoken trade-offs and named alternatives (every subject the course raised as a choice — argued, or named without argument — with its disposition)"; T5's entry unchanged.
14. applied — §5.1 "Run settings (test hooks)": `RUN_BUDGET` (default 3; 0 = D2 (b)), `RUN_TURN_CAP` (40 when budget > 0, 12 when 0), `FETCH_FAILURES` (0), `RUBRIC_PATH` (`fixtures/rubric.txt`), each an env var and a keyword argument of the one-analysis function; `SCRIPTED_MODEL`/`SCRIPTED_VARIANT` named there; `WORKSPACE_ROOT` declared; scripted stand-in exposes `call_count`. AC3, AC7, AC8, AC16, AC17, AC18 use those names; "Default run" definition lists the defaults.
15. applied — §5.1 "Planted workspace states": the missing-instructions workspace (empty dir handed to `build_review_agent(workspace_root)`), the sample workspace `<name>` (AC15, AC21), and `fixtures/stale_workspace/` (AC51); AC8, AC15, AC21 use those names.
16. applied — "How to read" paragraph defines *Generator's reading* (also "generator's quantification"), *Constrained-dimension lever*, *Example-realization note*.
17. applied — R13 now says the run's status is `grader_error` (not `ungraded`, which §3.2 reserves for a run with no grader); exclusion semantics unchanged.
18. applied — R5 states a budget-0 run takes the 12 unless its Given names a cap; §5.2's Default-run text says a Given setting `RUN_BUDGET=0` takes cap 12; AC18's Given says so.
19. applied — formats moved into owning rules: R20 (`pass_rate` = passed/total rounded to 3 decimal places, `null` when total 0), R15 (three banner lines `Ticket: <key>` / `Requirement version <n> analyzed` / `Verification: <status> after <n> grading pass(es)`), R16 (bot comment `Analysis complete (<status>): requirement version <n>, report: <report page title>`); AC28, AC31, AC34, AC17 assert those exact forms (AC17 now also cites R16; R16 → AC17).
20. applied — R20 says `messages` carries full tool-call arguments, never the 220-character trace cut; AC33 asserts each run file's `messages` holds the `write_file` call with a `content` argument longer than 221 characters and a tool message with `tool_call_id` and `status`.
21. applied — §5.1: both seedings (batch and event) are in memory only, replacing the fetch tool's in-process map entry and never writing `fixtures/tickets.json` (AC44's hash).
22. applied — scripted grader's `evidence` defined per criterion: completeness → first Confirmed Facts bullet; clarity → first indented `Resolved by:` line; depth → first indented `Edge case:` line; completeness `gap` = `only <m> of <n> clauses addressed`.

Side fixes forced by the checker: AC7/AC18/AC20 prose mentions of R5/R12/R10 reworded (the checker reads any `R<n>` in an AC row as a citation); AC18 cites R12 and AC17 cites R16 with reciprocal arrows added; §7 reporting duty now AC1–AC51.

## Checker output (final)

```
$ python3 .claude/skills/generate-spec/scripts/check_spec.py courses/loop-engineering-with-langchain-deepagents/spec.coding-agent-lab.md
spec.coding-agent-lab.md: 0 finding(s); rules=29 ACs=51 rows=5
```

## Reciprocity check (a) — independent script (Rules column only vs rule → lists)

```
rules=29 ACs=51 missing-rule-arrows=[] reciprocity-violations=0
rule->AC counts: R1:2 R2:1 R3:2 R4:2 R5:1 R6:2 R7:1 R8:1 R9:2 R10:3 R11:4 R12:2 R13:2 R14:5 R15:3 R16:4 R17:2 R18:3 R19:2 R20:4 R21:3 R22:3 R23:1 R24:1 R25:2 R26:1 R27:2 R28:1 R29:1
AC->rule counts: every AC cites 1–2 rules (AC5, AC12, AC14, AC17, AC18, AC27, AC33–AC36, AC46, AC47 cite 2; all others 1)
total rule->AC citations: 63; total AC->rule citations: 63
```
