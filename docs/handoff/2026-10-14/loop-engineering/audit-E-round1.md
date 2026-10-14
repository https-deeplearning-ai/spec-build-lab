# Audit 1 findings (Opus 5.5) — lab spec E on guide b03ddc9 / overlay 184a0ed (raw, 678 lines)

HARD
1. (f) L457 AC1 "action names fetch_requirement with argument UPL-310 … (the key seeded for the ticket's page)". L433 says only the batch runner seeds documents under UPL-310. No rule or fixture says which key an event run (ticket REV-101) puts in its opening message, nor that the linked page's current body is seeded under that key (AC25/AC32 "Confirmed Facts 3 vs 4" need it).
2. (f)/(n) L435 seeds ticket REV-100, status Open, linked to the page. L394 R14: saving a page re-runs every linked ticket not Done. L482 AC26 (only REV-101 Done) asserts "no new run is recorded; the response message says nothing was re-triggered". REV-100 is still Open, so it is re-triggered.
3. (f) L475 AC19 "trace has 16 rows alternating actor between consecutive model and tool rows". Replay: M T M T M T M T M T M T M M T M — the "Review complete." turn is followed by the post-feedback edit turn; 16 rows and 9 turns hold, strict alternation cannot.
4. (f) L443 after_partial.json 5/3/0 revisions 4; after_regression.json 4/5/5 revisions 0. R20 (L403): revisions_needed = graded runs with any first-attempt failure. Depth 0/5 forces 5; completeness 4/5 forces ≥1. The AC40 verdicts survive, the fixtures do not satisfy their own rule.
5. (m) enum values never observed: run trigger value manual_rerun (L184) produced by R14's manual re-run, never asserted (AC12 does not); page kind requirement (L291) asserted by no AC.
6. (g)/(p) L88 "capability invariants moved to R6–R9 (AC10–AC15)". R6's criteria are AC8, AC9; AC13–AC15 belong to R10.
7. (p) L87 derives "models must support native tool calling, and the analyst's model must support a structured (typed) final response", lives in "R22 (AC38, AC39)". R22 (L408) states neither capability; no AC exercises the analyst's typed response; AC39 runs only the review path.
8. (p) ADD 5: L577 "Guidance lost at boot … Fix: §6 Never", L578 "Pin refused by the image's interpreter", L579 "Course pin shadowed by a preinstalled copy" name no rule and no AC.
9. (g) L620–L628 use "tie-breaker 1"/"tie-breaker 2"; the "How to read the provenance notes" paragraph (L612) never defines "tie-breaker".
10. (k) L74 D2 (b) "agent loop alone — revision budget 0" makes D3's unconditional Invariant (L75, "A grader stage judges the file…") false and RR1's Invariant (L76, "drives the real pipeline end to end — tool calls, grader, …") false; "retires every grader AC" names no AC list.   [ORCHESTRATOR: keep every option; add to D2 (b) the explicit list of criteria that apply only under (a); qualify D3's and RR1's Invariants with "under D2 (a)" / "when a grader is present" so they stay true under (b) — wording, not a new decision]
11. (k)/(n) L73 D1 (b) "moves the per-section review guidance into skill files". R6 (L380) requires the Review-guidance level-3 headings the learning loop targets; AC9 requires the baseline byte-identical to v1; AC35/AC37 apply into ### Ambiguities. The row says nothing about which change.   [ORCHESTRATOR: keep the option; state in D1 (b) which rules/ACs are altered or retire, as the earlier generations' D1 (b) did; author no skill content]
12. (k)/(n) L75 D3 (b) deterministic code grader; L469 AC13 asserts the grader's first tool call is read_file /analysis.md; a code grader makes no tool calls; the row does not retire AC13.   [ORCHESTRATOR: keep the option; add the does-not-apply list to D3 (b)]
13. (q) L76 RR1 (b) live models vs R26 (L412) "suite runs … no network and no key" and AC44 (L500) "network disabled and all key variables unset". Choosing (b) leaves the completion gate impossible.   [ORCHESTRATOR: SKIP — owner decision, issue #38 item 2; RR1 Options/Invariant untouched; DO add to RR1 (b) the list of exact-value criteria that exercise only the scripted Default, as earlier generations did]
14. (i) L112 "Multiple analyses per ticket in parallel, authentication, user accounts, a real database — buildable, unparameterized: past course scope". The guide defines that tag as "named by the course but never built"; authentication and user accounts are not named by the course; they are additive and owned by no row → restorable.

SOFT
15. (p) L90 "lives in R14–R16 (AC24–AC31)"; R16 also owns AC32.
16. (q)/(r) L91 hosted tracing "ANSWERED — every alternative unavailable here": under §3 the stand-in and omission are takeable, so the claim does not follow.   [ORCHESTRATOR: SKIP — the collapse is a decision consistent with the last three generations; owner decides; do not reword]
17. (r) L623 T6 "tie-breaker 1: only the approved path is shown", L624 T7 "presented only as the thing never to do", L625 T8 "tie-breaker 1": tie-breaker 1 means a demonstrated failure; these give a one-sided argument.   [ORCHESTRATOR: restate each reason accurately WITHOUT changing the disposition (bake-in stays bake-in); if an accurate reason would require a different disposition, leave the entry and record it under Skipped]
18. (r) L631 T14 "folded into T2" is not one of row / bake-in / lever / narrative.
19. (g) CTX-E rows (L665–L670) do not attribute T2, T7, T8 or C9 to any lesson or source.
20. (g) R8 (L382), R12 (L389), R25 (L411) labelled Course-demonstrated with no (CTX-X) anchor.
21. (p) L411 R25 co-label "reinforced [environment] (the workspace is the record…)": that fact is about the chat record, not restart persistence.
22. (m) L344 section "empty unless target is prompt" vs L437 change_tool.json etc. "the same object with target tool…" carrying section "### Ambiguities".
23. (f) L437 garbled fixture text: "add two more indented labelled lines after ` `` `Reason:` `` `:`" — the exact v2 insertion text cannot be read off the page.
24. (b)/(m) R4 (L378) "the Summary is two or three sentences": no AC asserts the sentence count.
25. (m) R21 (L404) "A regression means the change is not kept": undefined, untested.
26. (f) AC38 (L494) "no source file references ANTHROPIC_": the test sets ANTHROPIC_API_KEY=CANARY itself; scan scope undefined.
27. (f) AC44 (L500) "all key variables unset" vs §7 command (L548) unsetting only the OPENAI_* pair.
28. (m) AC12 (L468) "the two runs' workspace paths differ": R9 discards event workspaces and §3.2 has no workspace-path field.
29. (n) AC7 (L463) "a run on UPL-310": runs are per ticket or batch document, entry point undeclared; AC18 (L474) "a run on REV-101" names no step that creates REV-101.
