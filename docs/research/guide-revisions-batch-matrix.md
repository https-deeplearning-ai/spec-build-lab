# guide-revisions-batch — pass matrix

Pass branch: `guide-revisions-batch`. Course: agent-memory-building-memory-aware-agents.
Guide under test: commit `0cd5ff2`. Spec fixture edits: `2835655` (on-ramp/currency),
`809dea8` (D13 row). Option-B delivery: no regen adoption, no rebuild (run-09 stands;
edits are presentation/Ledger-level). Source: issue #24 (tester-feedback triage) + #18's
queued findings.

## Decision log (owner decisions, locked before editing)

| # | Decision |
|---|---|
| 1 | No cost/time/size figures in specs (perishable); the recommended baseline is the minimum-resource path, benchmarked at the scaled test, not promised in text |
| 2 | No build-agent stop rule; replaced by inline heavy-option setup-weight notes (prose in the option entry, NOT a third label — F12's two-label rule intact) |
| 3 | Keyless offline completion is the baseline's completion criterion (the blessing sentence; also resolves skip-read-as-failure) |
| 4 | Orientation lead: user-visible interaction (reader test), merged with the fastest-path sentence into the blockquote; §1 untouched; §0 stays first section |
| 5 | D13 summary-memory scope admitted to canon → **P1 consciously updated to 13 subjects** (owner decision, recorded in the F12 matrix); G6 example stabilizes it |
| 6 | Model currency: providers/protocols + course's own models only; current-model advice = gate-time "(Recommended)"; CTX-D gains parameter-constraint perishables |
| 7 | From #18: id alphabets (G4), importable fixture filenames (G5) promoted; **F8 stays parked**; **#19 excluded from this batch** |
| 8 | Live-AC run added (owner supplies key); model policy continues: regens/scorers/probe on Opus-class |

## Properties

Carried: P2–P13, N1–N9, S1–S3 as previously defined (guide-pins-v2 + guide-scope-and-residuals
+ gate-semantics matrices), plus F12's T1–T3/L1. **P1 (consciously updated): 13 subjects** —
the previous 12 + summary-memory scope (D13-equivalent row, both sides carried, contradicted or
structural route accepted).

New:

| ID | Property | Type |
|---|---|---|
| V1 | Opening blockquote leads with a "what you're building" sentence that is a user-visible interaction (no store counts / taxonomies / algorithm names) + the fastest-path sentence (baseline named; complete when the offline suite passes; keys unlock only live tests/live use) | content-presence w/ reader test; fastest-path half near-verbatim |
| V2 | Every heavy option (course store, keyed web tool) carries an inline setup-weight note in its own Options entry | content-presence |
| V3 | No "current best" model names baked into defaults/Options — providers/protocols + the course's own models only; CTX-D includes a request-parameter-compatibility entry | content-presence |
| V4 | Summary-id format pinned with **alphabet** (hex), not length alone | content-presence (the cross-model gap test) |
| V5 | All fixture module filenames are importable identifiers | content-presence (grep) |
| V6 | D13-equivalent scope row present: both sides cited, thread-scoped default, stakes-test reasoning | content-presence |

Pass bar: all properties present in both confirmation regens, evidence-labeled
[verified]/[reported]; V4 is the watched cross-model item (0/3 on Opus-class pre-G4).

| C | 0cd5ff2 | Opus-class | **All six V-properties PRESENT [orchestrator greps, verified]**: V1 orientation scene + completion criterion (L3); V2 heavy-setup inline (store, web-search, local-model option); V3 "Model names rot: pick the current model at gate time via your (Recommended) flag" in D4 + CTX-D request-parameter entry (L1200, notes the course passes no temperature); V4 `^[0-9a-f]{8}$` + "alphabet is part of the contract" (L157-158) — **G4 2/2**; V5 five importable fixture modules; V6 D12 scope row (contradicted route). P1 PARTIAL: 12 rows — augmentation folded (residual class, same subject as prior pass); init-semantics correctly baked into R1 with the warned-failure litmus stated |

## Probe

Stage-1 only (no new behavioral guard shipped): cold-start Opus build agent on a scratch copy
of the edited spec must still stop at the gate with the new blockquote above §0.

**Result: PASS** [verified from the subject's reply] — stopped with zero files written; presented
baseline/customize across all 13 rows (D13 included); named the two course departures (store,
web search) unprompted in the baseline option; relayed the new completion criterion accurately
("no API key needed to finish — completion is defined by the offline pytest suite") and even
surfaced the one-time embedding-model download. The orientation block does not weaken the gate.

## Rounds

| Regen | Guide | Model | Result |
|---|---|---|---|
| A | 0cd5ff2 | Opus-class | **All six V-properties PRESENT [orchestrator greps, verified]**: V1 orientation lead is a true user-visible scene + fastest-path/completion verbatim-equivalent (L3, echoed §7 L671); V2 heavy-setup inline on 4 options (generalized past the two examples); V3 no current-model names, "model currency is a gate-time judgment" in D4, CTX-D request-parameter entry (L745, mined from materials); **V4 id alphabet pinned `^[0-9a-f]{8}$` + "alphabet is part of the contract" (R13) — G4 closed the 0/3 cross-model gap first try**; V5 all fixture modules importable; V6 D14 scope row, both sides + stakes reasoning — **G6 stabilized the subject**. P1 PARTIAL: 14 rows = all 13 canon subjects + an extra init-mode row (the documented judgment-boundary class; same subject as last pass's regen-C) — residual policy, no fix round |
