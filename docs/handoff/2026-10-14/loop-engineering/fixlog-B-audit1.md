# Fix log — lab spec audit 1 (32 items)

Spec: courses/loop-engineering-with-langchain-deepagents/spec.coding-agent-lab.md
Applied: 31 · Skipped: 1 (item 13, orchestrator SKIP). No Ledger row, Options entry, Default value or "(course default)" label changed. The one Default-cell text touched is L1's AC range (AC1–AC39 → AC1–AC42) and RR1's tier wording (item 23); neither alters the decision.

1. applied — `05_incident_paging.md` count corrected to [3 of 5] (quickly, aggressively, planned); every other bracketed count re-verified against VAGUE_WORDS.
2. applied — new §5 "Test hooks" paragraph declares `FIXTURE_BATCHES` (env var, `label=directory` pairs registered at startup; a directory without `summary.json` gets one computed), `run_review(ticket_key, *, workspace_dir=None, …)` in `review_runner.py` (AC10), and the stored change `proposal_<label>.json` planted from `fixtures/changes/*.json` (AC28); AC10, AC17, AC27, AC28, AC31–AC33 now use those names.
3. applied — analyst `evidence` defined as one entry per run that failed a recurring criterion (run file name: gap texts joined by `; `), so 5 entries; AC26 asserts 5 entries each mentioning both labels.
4. applied — R17 roots the analyst at a fresh workspace whose `/<label>/` is a copy of the batch; the app copies `/proposal.md` into the batch directory afterwards, so AC26's "gains proposal.md" holds.
5. applied — R17 defines `proposal.md`, `proposal_<label>.md` (= `proposal_markdown`) and `proposal_<label>.json` (the stored change R18 reads); R18 and §3 apply row reference it.
6. applied — `GradingPass.tool_calls` added (required; the grader's own calls in order, meaning stated in R8); propose response gains `trace: TraceStep[]`; AC12 and AC27 re-targeted at those fields.
7. applied — R3 defines the `Finishes the review` action for the model's plain-message row.
8. applied — R19 defines `attempts` (grading passes per batch, first attempt plus revisions) and `runs`.
9. applied — schema else-branch status enum now includes `turn_limit_reached`; R3 states that the cap ends the run with no grading pass under either cap; `turn_limit_reached` ⇒ `grading` empty.
10. applied — AC20's Given is a replayable chain (fresh store, one rerun, AC19's two tickets closed, an `unlinked.md` page); the second save goes to the unlinked page; AC37's seed-page count (2) stays true and the unlinked page's 2 versions are asserted too.
11. applied — new R25 `[environment]` (floor cited from §2/CTX-D, check from EF4) and AC40 (README records `python3 --version`, `api/health.python_version` matches, ≥ 3.12); Environment row cites R25/AC40.
12. applied — "How to read" paragraph now defines tie-breaker 1/2, degenerate case, lever-value rule (= value-selection branches), the four Category names and the keyed-tool rule.
13. skipped — orchestrator SKIP (owner decision, issue #38 item 2); RR1's Options untouched.
14. applied — D2 option (b) lists the Default-only criteria (AC12's `read_file` call, AC13's line number) and says every other grading assertion stands; Trade-off reworded to "checks coverage only literally, never semantically", consistent with the Invariant (no weakening of the Default).
15. applied — R7 seeds the workspace with the instructions file alone under D1 default and with `skills/` under (b); D1 option (b) states no AC retires or changes and that no skill content is authored here.
16. applied — poet item retagged `unavailable` (a different project; the lab fixes the assignment), pointing at D1 (b) only as the layout's origin.
17. applied — R11 → (CTX-B14); R13 → (CTX-B13, CTX-B15); R12 → (CTX-A, CTX-B15, CTX-B16).
18. applied — fixture `nearmiss.md` (scripted review model writes `Resolution:`/`Edge-case risk:` on the first attempt); scripted grader's label check made exact; AC41 (R8); CTX-B4 enforced-by extended.
19. applied — fixture "Same-count seed body" (second clause reworded, counts unchanged); AC42 (R15); CTX-B12 enforced-by extended.
20. applied — R6 labelled *course-demonstrated* with its last sentence tagged `[environment]` as a separate constraint; §4 labels line no longer claims a co-label.
21. applied — "two" → "three" model-tiering levers, under R9, R17 and R20.
22. applied — "the one row stating … honestly" reworded; harness and tiktoken rows named as following the same rule.
23. applied — RR1 Default's tier phrase reworded to "in-process code adding no dependency beyond the §2 pins (lighter than tier 1, which ranks substitute dependencies)".
24. applied — human-grader narrative moved from D2's Options cell to its Trade-off cell.
25. applied — AC15 asserts exactly 4 passes (replay: first attempt + 3 send-backs).
26. applied — AC22: tool-row detail at most 220 characters.
27. applied — "vague word" = the VAGUE_WORDS entry occurring earliest in the clause's own text (declared beside VAGUE_WORDS with the "Large exports…" example).
28. applied — AC34 no longer asserts the whole suite; it asserts health, a `satisfied` offline rerun with no outbound request, and the source search.
29. applied — AC19 creates a second ticket without an assignee → `REQ-103` with `Unassigned` (AC20's chain closes it).
30. applied — `MODEL_MODE` row: "`scripted` or `live`; unset means `scripted`".
31. applied — the two overlay-citing lever rows now name tie-breaker 2 (model tier is a value) in the spec's words.
32. applied — guide pointer replaced by the rule stated inline (scripted stand-ins drive the real harness; a replay is never a test).

## Checker output
```
spec.coding-agent-lab.md: 0 finding(s); rules=25 ACs=42 rows=4
```

## Citation check (a)
```
rules=25 ACs=42 rules-cited=25 problems=0
```
