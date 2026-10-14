# Audit 2 findings (Opus 5.5) — lab spec E after repair pass 1

HARD
1. (k) L76 RR1 Invariant "The offline suite drives the real pipeline end to end … against a stand-in whose per-role responses are declared in §5" vs option (b) live models; (b) breaks its own row's Invariant and can never satisfy AC44.   [ORCHESTRATOR: SKIP — owner decision, issue #38 item 2; RR1 Options/Invariant untouched]
2. (q)/(n) L76 RR1 (b) list "Exact-value criteria that exercise only the scripted Default …" leaves out AC8 (call counter 0), AC12 (first file tool call is write_file), AC15, AC16 (scripted grader verdicts), AC31 ("Analysis complete (satisfied)"), AC50 (Given needs compare = success).
3. (n) L74 D2 (b) list "Criteria that apply only under (a): AC13–AC17, AC19, AC20, AC28, AC31–AC35, AC39, AC46–AC48": AC50's Given ("after AC46 … compare(v1, v2) = success", L513) can never be true under (b), yet AC50 is not listed.
4. (q)/(f) L73 D1 (b) vs scripted review role (L454) "If the instruction text in its context contains Resolved by: … from the first attempt": under (b) the guidance lives in skill files read on demand and the scripted model is never declared to read a skill, so AC46 (L509 "every run has one grading pass, satisfied") cannot pass under (b); D1's list does not mention AC46.
5. (k) L73 D1 Invariant "the agent itself is denied writes to it (R6, R7)"; option (b) adds a skills directory with no path; R7 (L387) denies only writes under /memories/**; the builder must guess whether skill files are write-protected.
6. (f) L395 R12 "turns count model messages that call tools plus the final answer": the default run has 7 tool-calling messages + 1 final answer = 8; AC19 (L482) asserts turns = 9 (counting both completion sentences); AC18 (L481) turns = 7 follows the rule; AC19's number does not.
7. (f) L409 R20 "runs every document in sorted filename order"; fixtures/requirements/ also holds UPL-310.md (L433) → 6 files; AC33 (L496) asserts five run files and AC20 says "over the five batch documents"; nothing says the batch set leaves out UPL-310.md.
8. (f)/(m) L455 scripted grader: "completeness passes when the Confirmed Facts bullet count is at least the requirement's clause count" and "raises an exception on the document titled Report Export"; the grader has only a file-read tool and /analysis.md (R10, L393); nowhere does the spec say how the grader receives the requirement's text, clause count or title; AC15 (L478), AC20 and every completeness verdict depend on it.
9. (f)/(j) CTX-B1 L382 R2 "the offline fixture plants two failures (a 503-style message, then a timeout message)": the failure texts are not declared in §5.1; R2 detects an error only when "status is error, or its text begins with 'error'"; AC3's "tool rows 2 and 4 are errors" depends on wording the builder must invent.
10. (j) CTX-B7 L615 "Stale analysis from a previous run … Enforced by R9, AC12": no fixture plants a stale /analysis.md; AC12's "first file tool call is write_file" holds under the scripted model whether or not the workspace is shared.
11. (r) L638 T10 "lever R18 — a spoken heuristic quantified (generator's reading …)": names no tie-breaker.

SOFT
12. (r) L632 T4 "lever R22 — attached to the constrained model/provider dimension; Ask First": cites the overlay route, names no tie-breaker.
13. (r)/(g) L625 introduces the table as "every one the course argued"; L633 T5 says "no trade-off argued, so not design-argued": heading and entry contradict.
14. (f) Test hooks not declared in §5.1 next to SCRIPTED_MODEL/SCRIPTED_VARIANT (L452): the call counter AC8 relies on (L471); the settings for budget, turn cap, simulated fetch failures, grader-off and rubric file that AC3, AC7, AC16, AC17, AC18 rely on.
15. (j) CTX-B5: AC8's planted state "a workspace with no /memories/AGENTS.md" (L471) not declared in the §5 fixture corpus.
16. (g) Provenance terms used but undefined in the "How to read" paragraph (L623): "generator's quantification"/"generator's reading" (L407, L638); "Example-realization note" (L73).
17. (m) L396 R13 "the run is ungraded" vs AC20 (L483) status grader_error; the schema (L248) reserves ungraded for "no grader configured".
18. (n) "Default run" definition (L460) "cap 40"; AC18 (L481) uses the default run with budget 0, but R5 (L385) says the cap is 12 without a grader.
19. (m) Formats asserted only in ACs: AC34 "passed/4 rounded to 3 places" (L497); AC28 "three banner lines … 'after 2 grading pass(es)'" (L491); AC31 "Analysis complete (satisfied)" (L494).
20. (m) R20 (L409) "every message untruncated" and the schema's messages field (L210): no AC asserts it.
21. (f) L440 "the batch runner seeds each document under the default key UPL-310" in the fixtures/tickets.json map: never says this seeding stays in memory; if written to the file, AC44's fixtures hash check fails.
22. (f) L455 passing criterion "carries evidence = L<line>: <that line verbatim> (the first qualifying line)" is undefined for the count-based completeness criterion, which AC13 asserts (L476).
