# Fix log — lab spec E, audit 1 (29 items)

Spec: courses/loop-engineering-with-langchain-deepagents/spec.coding-agent-lab.md (678 → 689 lines). Backup of the pre-repair file: scratchpad/spec-lab6-before-audit1.md. No decision changed: no Ledger row, Option, Default, "(course default)" label or trade-off disposition added, removed, renamed or relabelled.

## Per item

1. applied — §5.1 fake-tracker paragraph now declares that an event run seeds the linked page's current body (latest version, rendered as `REQUIREMENT: <title>` + one clause per line) under `UPL-310` immediately before the run, so the opening message names `UPL-310` and the fetch returns the page as it stands (3 clauses at seed, 4 after AC25).
2. applied — AC25 now declares the extra state the fixture forces: the save re-runs both open linked tickets (`REV-101` and seed `REV-100`); `REV-100` becomes `Analysis Ready` with `page-analysis-rev-100` v1; the message names both. AC26 Given: both tickets closed (`POST api/tickets/<key>/close`); Then adds "the page has version 3". AC41 updated to the three event runs and both report pages.
3. applied — AC19 states the exact 16-row actor sequence: (Model, Tool) ×6 for rows 1–12, Model row 13, Model+Tool rows 14–15, Model row 16.
4. applied — `after_partial.json` revisions 4 → 5; `after_regression.json` revisions 0 → 1; sentence added that each `revisions_needed` is R20's count from its own numbers. AC40 verdicts unchanged (partial/regression still follow R21); AC40 now also asserts `revisions_needed = [5, after]`.
5. applied — AC12 asserts the re-run record's `trigger` is `manual_rerun` (now cites R14; R14's text says the record's `trigger` names the trigger); AC23 asserts the seed page's `kind` = `requirement`, `linked_ticket` null.
6. applied — Environment Resolutions environment row: "R6–R9 (AC10–AC15)" → "R6–R9 (AC8–AC12)".
7. applied — R22 text now states the derived capability (native tool calling for every role; a structured typed final response for the analyst, the §3.4 change). New AC48 `live` exercises the analyst's typed response on a live batch `live1`; the row says only a `live` criterion can exercise a real model's typed response and AC33 covers the scripted path. R22 → AC38, AC39, AC48; Env Resolutions model/provider row updated.
8. applied — new rule R29 `[environment]` (build-workspace and interpreter discipline: (i) baseline instruction file under the app's data dir, no source touches the build-root `AGENTS.md`; (ii) interpreter check recorded, refused pin stops with a report; (iii) course pins win in the venv, verified) → AC49. Each of the three Runtime failure modes now ends "Enforced by R29 (i/ii/iii), AC49". CTX-E environment row lists R29.
9. applied — "How to read the provenance notes" defines *Tie-breaker 1* (demonstrated failure wins; warned-against-as-failure counts, outgrown does not) and *Tie-breaker 2* (a value trade-off is a lever; a limit value that removes a component escapes it).
10. applied — D2 Option (b) lists the criteria that apply only under (a) (AC13–AC17, AC19, AC20, AC28, AC31–AC35, AC39, AC46–AC48), the four whose status becomes `ungraded` (AC3, AC10, AC11, AC22), and that AC18 exercises (b). D3 Invariant prefixed "Under D2 (a),"; RR1 Invariant "grader" → "grader (when D2 = (a))". Options text untouched.
11. applied — D1 Option (b) states what switching alters (R6 heading home, R17–R19 proposal target and apply site, the scripted analyst's target) and what retires (AC9 byte-identity, AC35 equality with v2, AC37 — each replaced by the same assertion against skill files). No skill content authored.
12. applied — D3 Option (b) lists what does not apply: AC13 (no tool call, no `L<n>:` evidence) and AC20's injected grader exception; every other grader criterion is verdict-shape only.
13. first part SKIPPED by orchestrator note (RR1 (b) vs R26/AC44 offline gate — owner decision, issue #38 item 2; Options/Invariant untouched on that point). Second part applied — RR1 Option (b) lists the exact-value criteria that exercise only the scripted Default: AC1, AC3, AC4, AC7, AC10–AC14, AC17–AC20, AC22, AC28, AC32, AC33, AC35, AC45–AC47.
14. applied — §1 item 8 retagged: "Multiple analyses per ticket in parallel, a real database" stays `buildable, unparameterized` (named by the course, never built); "Authentication and user accounts" moved to new §1 item 11 tagged `restorable` (additive, owned by no row, not named by the course). No item removed.
15. applied — event-source row: "R14–R16 (AC24–AC31)" → "(AC24–AC32)".
16. SKIPPED by orchestrator note (hosted-tracing collapse is an owner decision; not reworded).
17. applied — T6, T7, T8 reasons restated accurately under tie-breaker 1 as defined in item 9 (the course warns against the other side as a failure and never shows it working); dispositions unchanged (bake-in R17/R21, R15, R16).
18. applied — T14 disposition "folded into T2" → "narrative — framing of how loops compose…; the one composition built both ways is T2, row D2".
19. applied — CTX-E: T2 added to lessons 2 and 5; T6 to lesson 2; T7, T8 to lesson 6; C9 to lesson 4 and the shipped-code row.
20. applied — R8 anchored (CTX-A: confined workspace), R12 (CTX-C11), R25 (CTX-C10).
21. applied — R25 co-label reason reworded to a restart-persistence fact: only the workspace disk persists between lab sessions, so records held in process memory are lost at every restart.
22. applied — §3.4 `section` description: "required non-empty when target is prompt, carried but ignored by the apply step for any other target" (fixtures unchanged; the if/then already matched).
23. applied — v2 insertion text restated as five exact lines (named "the v2 insertion text", which the scripted analyst and change_prompt.json already reference).
24. applied — R4 defines a sentence (ends at `.`, `!`, `?` followed by whitespace or section end; the summary check reports the count); AC6 asserts summary sentences 2.
25. applied — R21 defines "not kept": comparison `keep` false iff `regression` (new required boolean in the §3.4 comparison schema with an if/then/else), and on `regression` the Learning page offers a human-triggered **Revert** that restores the before batch's snapshot as baseline — labelled project hardening inside R21. AC40 asserts `keep`; new AC50 asserts no Revert control on the `success` comparison and that the revert function restores `v1/AGENTS.md` as baseline.
26. applied — AC38 scan scope = every file under `app/` excluding `tests/` and `fixtures/`; the canary is set by the test process on both `ANTHROPIC_*` variables before config load, and the assertion is on the app's resolved configuration (no `CANARY` value, no `ANTHROPIC_` key) plus the source scan.
27. applied — §7 offline command now `env -u` all four key variables (OPENAI_* and ANTHROPIC_*), with a comment that AC38 sets its own canary in-process. Reporting duty: AC1 through AC50.
28. applied — §3.2 gains optional `workspace` (absolute path of the run's workspace root, recorded for every run including discarded event workspaces); AC12 asserts the two records' `workspace` values differ.
29. applied — §5.2 header defines "Direct run on `<key>`" (R14's one-analysis function invoked directly with that fetch key, no ticket); AC7 uses it; AC18 re-targeted to "the default run with budget 0".

Applied: 27 (item 13 counted as applied for its second part). Skipped: 2 (item 13 first part, item 16) — both by orchestrator note.

## Checker

```
$ python3 .claude/skills/generate-spec/scripts/check_spec.py courses/loop-engineering-with-langchain-deepagents/spec.coding-agent-lab.md
spec.coding-agent-lab.md: 0 finding(s); rules=29 ACs=50 rows=5
$ python3 scratchpad/recip.py <spec>      # check (a): rule → AC lists vs AC (R…) cells, both directions
rules 29 ACs 50 uncited rules [] problems 0
```

## Citation counts

- Rules 29 (was 28; +R29 `[environment]`); ACs 50 (was 47; +AC48 `live`, AC49, AC50); Ledger rows 5 (unchanged).
- Course-demonstrated rules 23, every one carrying a `(CTX-…)` anchor (R8, R12, R25 newly anchored); `[environment]` rules 5 (R22, R23, R24, R29 + the R25 co-label); project hardening 2 (R26, R28) + the revert clause in R21.
- `live` ACs 2 (AC39, AC48). Blockquote 231 words (unchanged; §0 and header byte-identical to before).
