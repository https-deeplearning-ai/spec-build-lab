# Audit 1 findings (Opus 5.5) — lab spec regenerated on guide 4e1b71e / overlay bb420fa

HARD
1. (f) L366: "Paging shall pause during planned maintenance." [2 of 5]. `planned` is in VAGUE_WORDS (L374), so 05_incident_paging.md has 3 vague clauses of 5, not 2. The declared fixture fact is wrong.
2. (f) Several ACs depend on test hooks or planted states that §5 never declares: L411 AC10 "a run workspace prepared without memories/AGENTS.md … the review run is started on it directly"; L418 AC17 "the batch summariser runs over it"; L428 AC27 "fixtures/batch_one_off/ registered as batch oneoff"; L432 AC31 "summary pair registered as batches"; L429 AC28 "a stored change whose target is each of tool, grader, configuration; then one whose section is ### Missing". No entry point, no registration mechanism and no fixture for these; the builder has to guess.
3. (f) L384 scripted analyst: "evidence = the first-pass gap text of every run that failed a recurring criterion". Each v1 run fails two criteria → two gaps per run. L427 AC26 asserts "evidence has 5 entries". Replay gives 5 or 10 depending on reading.
4. (f/n) R17 (L327) and L384 root the analyst at the batch history: it reads /<label>/summary.json and writes /proposal.md, so proposal.md lands one level above the batch directory. L427 AC26 says "the batch directory gains proposal.md".
5. (m) L427 AC26: "gains proposal.md, proposal_v1.md and proposal_v1.json". No rule or contract tells the app to write proposal_<label>.md/.json; only the CTX-C name map at L595 mentions them.
6. (m) L413 AC12 "the grader's own tool calls include read_file"; L428 AC27 "the analyst's own trace shows a denied write_file". Neither GradingPass (L211–225) nor the propose response {change, proposal_markdown} (L159) records grader or analyst tool calls; nothing for these assertions to read.
7. (m) L406 AC5: "the last trace row's action is Finishes the review". No rule defines this string; R3 defines only "Stops: turn limit of <cap> reached".
8. (m) L431 AC30: "attempts [10, 5]". R19 (L329) never defines attempts; it sits in the CompareResult schema with no meaning.
9. (m) L253 else-branch (rubric_iterations ≠ 0) status enum ["satisfied","max_iterations_reached","grader_error"] vs R3 (L313) "When the cap ends the run with the report incomplete … the status is turn_limit_reached", which applies under the 40 cap too. A manual rerun with {fetch_failures: 99} and the default budget reaches a status the schema forbids.
10. (n) L421 AC20: "a second save with no open linked ticket returns a message that nothing was re-triggered". After the first save REQ-101 is still Analysis Ready (open), so a second save to the same page would re-run REQ-101 and make 3 seed-page versions, but L438 AC37 asserts "the seed page has 2 versions". No other page is declared for that second save.
11. (p / ADD 3) L87 Environment row: "the course's Python floor (§2 interpreter row, checked at build start)" is a capability invariant of an ANSWERED dimension; no AC exercises it (AC34 never asserts python_version ≥ 3.12) and the table does not say why not.
12. (g) Terms used in the provenance notes not defined in the "How to read the provenance notes" paragraph (L549): "tie-breaker 1"/"tie-breaker 2" (L555–565); "keyed-tool rule" (L566); "degenerate case" (L556); the Category names design-argued, design-structural, realization (L557, L72–75); "lever-value rule" (L312, L319) — the paragraph calls it "value-selection branches".
13. (k) RR1's Invariant (L75) requires "model responses the suite controls"; option (b) the live platform model does not meet it; choosing it makes the exact-count ACs unreproducible and contradicts AC34/R24.   [ORCHESTRATOR: SKIP — owner decision, issue #38 item 2]
14. (k) D2 option (b) deterministic grader: its own Trade-off (L74) says it "cannot judge coverage", yet the Invariant requires judging "against the three named criteria", completeness included; choosing it makes R8 and AC12/AC13 unpassable and nothing says which ACs it retires.
15. (k) D1 option (b) "the always-on file plus a skills/ directory" (L73) contradicts R7 (L317): "seeded only with the instructions file". No resolution and no skill content.
16. (i/q) L116: "The poet agent of the primer … — owned-by-row D1". D1 only offers a skills layout for the review agent, so the item points at a row that does not offer it.
17. (g) CTX anchors point at the wrong failure modes: R11 (L321) cites (CTX-B15) "Re-running work nobody asked for" — the source-of-truth failure is B14; R13 (L323) cites (CTX-B14) — human-closes-Done is B13.
18. (j) L533 B4 "Grading by resemblance": no §5 fixture plants this failure (no near-miss label, no report that looks right while the file falls short); only the rule, the AC and the CTX entry exist.

SOFT
19. (j) L541 B12 "counts look alike although the content changed": the only fixture (edited seed body L392) changes the counts (Confirmed Facts 3→4), so the failure is never planted.
20. (p) R6 (L316) labelled "course-demonstrated, reinforced [environment]" but the environment part is a different constraint (workspace-root AGENTS.md never authored), not the course's constraint independently required; co-label misused.
21. (p) L86: "The course's two argued model-tiering trade-offs … become body levers under R9/R17" — there are three: REVIEW_MODEL (L336, L555) is left out.
22. §2 L130: "This is the one row stating the course's install situation honestly" — the Agent harness row (L129) and the tiktoken row (L131) also state lock/pin situations.
23. RR1 Default (L75): "tier 1 — in-process, no install beyond the harness"; CTX-C defines tier 1 as "ships with the language's standard distribution"; stand-ins built on the harness's chat-model interface are not stdlib.
24. (OVERRIDE 2) L74: D2's Options cell carries "A human grader … is not offered here"; that narrative belongs in the Trade-off cell.
25. (f) L416 AC15: "grading has at least 2 and at most 4 passes"; under R9 (budget 3) the replay is exactly 4; the range is looser than the rule.
26. L423 AC22: "a tool row's detail is ≤ 221 characters" vs R14 (L324) "truncated to 220 characters".
27. (f) L382: "the 'vague word' of a clause is its first such entry" — unclear whether "first" means clause order or list order; for "Large exports should be handled efficiently." the two readings give different words.
28. L435 AC34: "every non-live criterion passes" — the criterion asserts the whole suite, including itself.
29. (§8 enum coverage) L169/L344: Person enum value "Unassigned" is never reached by any AC.
30. (c) L137: "MODEL_MODE = scripted (default) or live" — a bare "(default)" label.
31. (r) L561–562: "lever (overlay: a model-tiering trade-off …)" and "lever (same overlay rule)" cite the overlay instead of naming a tie-breaker.
32. (g) L588: "(the guide's scripted-model rule)" — a pointer to the guide a reader holding only the spec cannot resolve.
