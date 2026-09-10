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
| C | 0cd5ff2 | Opus-class | **All six V-properties PRESENT [orchestrator greps, verified]**: V1 orientation scene + completion criterion (L3); V2 heavy-setup inline (store, web-search, local-model option); V3 "Model names rot: pick the current model at gate time via your (Recommended) flag" in D4 + CTX-D request-parameter entry (L1200, notes the course passes no temperature); V4 `^[0-9a-f]{8}$` + "alphabet is part of the contract" (L157-158) — **G4 2/2**; V5 five importable fixture modules; V6 D12 scope row (contradicted route). P1 PARTIAL: 12 rows — augmentation folded (residual class, same subject as prior pass); init-semantics correctly baked into R1 with the warned-failure litmus stated |
| B | 0cd5ff2 | Opus-class | **30/30 PRESENT, 0 PARTIAL, 0 ABSENT [full scorer + 6-verdict orchestrator spot-audit, verified]** — all six V-properties (V4 hex contract `^[0-9a-f]{8}$` + "alphabet is part of the contract"); T1-T3/L1/P2 near-exact incl. step-4 fix; **P1 EXACT 13/13** — the first regen in any pass with zero judgment-boundary deviation; P7 label band and P11 question-guarantee (prior partials elsewhere) both explicitly present |

## CONFIRMATION VERDICT (2026-09-09): the batch's guide rules PASS

All six V-properties present in **3/3 Opus-class regens** [A and C orchestrator-grep verified;
B full-scored 30/30 with spot audits]. **G4 closed the id-alphabet cross-model gap 3/3** (was
0/3 pre-fix). **G6 held the scope row in 3/3** (D14/D12/D13). Stage-1 gate probe PASSED with
the new blockquote. Carried set: P1 exact in B; A +1 (init-mode row), C -1 (augmentation fold)
— the documented judgment-boundary residual, expressing at the known rate; all other carried
properties present in every sample scored.

**New finding (queued for the next pass — guide half of the AC21 fix):** harness-known
identities are injected, never model-guessed. The live AC21 run caught the build exposing
`thread_id` as a model-supplied tool argument; the model, never told its thread, guessed
"current_thread" and the tool honestly consolidated nothing. Fixed in the spec (R11 sentence,
commit on this branch) + the run-09 build; the course-agnostic guide rule is recorded here,
unapplied, per fix-and-test-travel-together.

## Live-AC run (run-09, owner-supplied key)

First full keyed run in the lab: **AC4, AC9, AC19, AC22, AC24 PASSED live** [pytest -rA,
verified]. AC21 failed deterministically (2/2) on the thread-identity gap above → spec + build
fix → offline suite re-green (21/21) → AC21 rerun: **PASSED** (1 passed, 6m17s) — the live suite is 6/6; the course's headline
cross-session continuity demo is demonstrated end-to-end for the first time [verified].

## Post-validation addendum (2026-09-10): trial-driven fixes, added to the open PR

Third evidence source this pass: a **disposable-clone trial** — the PR-#25 spec copied alone into
an empty folder, built by a fresh session with zero project context (`~/learner-test`). Result:
build green (**50 passed / 6 skipped**, live skips honest), independent eval **9/10**, exact-string
contracts all character-correct, §5 fixtures byte-identical. Two defects in our owned assets
surfaced, both fixed on this branch:

**Fix A — R11 generalized (commit `eb953a0`).** The 2026-09-09 wording named `summarize_and_store`
inside the normative clause; the trial built the general injection mechanism (schema-stripping +
harness override) but applied it to that one tool, leaving `expand_summary` unscoped and weakening
D13's isolation. Wording-discipline violation #2 (course specific instead of concept). Now: every
thread-scoped agent-triggered operation, parameter absent from the model-facing schema, with
genuinely model-held identifiers (summary ids) explicitly still model-supplied.

**Fix B — the gate checklist becomes a durable artifact.** §0 said *print*; §7 cited "the printed
checklist" as evidence — durable proof demanded of ephemeral output. Provenance: printed checklist
is old (`e934873`), §7's citation arrived with `98d8815`, F12 only added deviation marks. Evidence
of the resulting drift: the checklist landed in `resolved-decisions.md` (probe-2, spontaneously),
inside `BUILD-REPORT.md` (run-09), and partially inside `README.md` (the trial) — three builds,
three places, two of them files no spec mentions, so no eval could ever find it.

**Owner decisions logged:** (i) the checklist is printed **and** written to a fixed-name file
`resolved-decisions.md` in the build folder; (ii) it is a **record, never an input** — no build
reads a previous checklist to resume; a new or resumed build re-runs the gate from the spec, and
each gate run overwrites the file (no accumulation, no version-control noise: build folders are
already gitignored).

**Conscious property update (template-conformance, per the skill's verbatim-template rule):** the
§0 property in the P2/T3 family now requires the emitted step 5 to carry the write-to-file
requirement, the fixed filename, and the record-not-input clause. Not carried forward silently.

**Accepted residual:** the *behavioral* test — does a build actually write the file — rides the
next disposable-clone trial rather than a paid probe build. Prior evidence the behavior is
natural: probe-2 wrote exactly `resolved-decisions.md` unprompted; the trial wrote a variant.

**Deferred to the next pass (from the same trial):** D10's augmentation default ships untested
(the offline stub cannot return augmentation JSON, and no live AC registers through a real model);
AC7/AC11 depend on a "scripted summarizer stub" §5 never declares — **2/2 builds invented it**,
so a share of the offline oracle rests on builder-authored fixture content; two §3/§4 prose
constraints (summary-description minimum length, R6's 8-12-word band) have no AC behind them; and
the guide-level generalization of R11 (harness-known identities are injected, never model-guessed).

| Regen | Guide | Model | Result |
|---|---|---|---|
| D | (post-Fix-B guide commit) | Opus-class | _(running — template-conformance greps only, N=1 per the cost policy)_ |
