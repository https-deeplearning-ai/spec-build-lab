# guide-scope-and-residuals — promotion-pass matrix

**Course:** agent-memory-building-memory-aware-agents · **Guide under test:** `195a94d`
**Pass bar:** every property present in every confirmation regen (S3 at N=3); evidence labels on
all claims. **Adoption intent (owner):** replace `spec.md` with the passing confirmation regen;
adoption additionally gated on a green build (buildability is the praised quality to preserve).

## Decision log (Phase 1, owner-confirmed)

| Candidate | Verdict | Notes |
|---|---|---|
| PR #17 scope-boundary row | guide-only | branch merged before triage (ordering exception, plan-approved); wording-discipline review found one rule-3 violation (§14 line restated mechanics) — rewritten reference-style |
| #18 F7 constants→CTX | promote | fixture edit skipped: current spec exhibits the constants as a §2 binding block; the property targets the regen's CTX form. Contract-participating constants (e.g. entity-type enum) stay binding |
| #18 F6 route closure | guide-only | known coin-flip (3/6 founding-pass regens) → confirm-N=3 on S3 |
| #18 F8 fixture churn | **deferred** | stays open in #18; no rule |
| #19 recording | routed out | lab tooling, not guide territory |
| Preservation focus | buildability | carried P10/P12/P13 + green-build adoption gate; no soft properties added |

## Core properties (carried from guide-pins-v2, updated per owner decisions)

P1 (updated): Ledger covers 12 subjects — 6 learner rows with **scope-boundary** as the sixth
dimension (per merged #15/#17 rename), + context-reduction, tool-description augmentation,
memory-core topology, deterministic/agent-triggered split, persistent store, acquisition toolset.
P2–P13: as in `guide-pins-v2-property-matrix.md` (gate mechanics, labeling, restart AC, keyless
arXiv default, mined parameters, contradiction carries, rules↔ACs, recoverable consolidation,
fixtures authored, self-containment).
N-series (guide-pins-v2 N1–N9): Ask-First derivation incl. the op-split entry; fresh-init
existence AC; zero contradicted rows with lever-branch citations; no tool-exposure row; tier-1
store with declared-scale reasoning; keyed-tool three-option shape with omit default; §6
"Standing Permissions" title; guide-commit provenance pin (`195a94d`).

## Pass properties

| # | Property (checkable, quotable) | Type | Candidate | Flakiness → confirm-N |
|---|---|---|---|---|
| S1 | The learner scope-boundary row meets §5.5's four requirements: Decision cell instructs presenting the §1 list inside the question; Default = keep-as-is; ≥2 Options offering restoration without pre-naming items; each §1 item carries a handling rule | content-presence | #17 | unknown → N=2 |
| S2 | CTX carries a name-map of course-declared non-contract constants (the seven store names) as provenance; the entity-type enum (contract-participating) remains binding in the schema | content-presence | F7 | unknown → N=2 |
| S3 | No non-decision row: no Ledger row whose alternatives are all course-warned or degenerate (tool-exposure remains a business rule; per-property check across all rows) | content-presence | F6 | **known 50% coin-flip → N=3** |

## Property-wording corrections (scorer-facing, logged)

- S1: "≥2 Options offering restoration" → **"≥2 Options total, restoration available without
  pre-named items"** — matches §5.5's own text ("two options … plus free-text is enough").
- S2: reworded to the rule's conditional — **"course-declared constants are carried: each either
  contract-participating-and-binding or in CTX provenance; none dropped."** Regen-A bound the
  seven store names into its contracts (AC1 tests them by name) — the binding branch, legitimately.

## Rounds

### Round 1 (guide `195a94d`; regen-A, scored by isolated scorer + 6-verdict spot-audit)
- S1 PRESENT [verified] · S2 PRESENT via binding branch [verified] · S3 PRESENT [reported, per-row
  listing quoted] · P1–P6, P8–P13 PRESENT [reported; P-series spot-checks verified] ·
  N1–N9 PRESENT [N4/N8/N9 verified] · **P7 PARTIAL** [verified: 0 hits for the 8–12-word label
  band] — everything else in P7 lands.
- Failure→fix trace: P7's miss = §4 Pass-A "working parameter" under-defined for prompt-imposed
  output-shape constraints (label word band). Fix: Pass-A clause added (output-shape constraints
  are working parameters). Round 2 regen against the new hash.

### Round 2 (guide `797ad42` — the final guide under test; regen-B) — PASS
- **25/25 PRESENT** (isolated scorer with quotes; 6-verdict spot-audit [verified]: P7 label band
  ×3 hits incl. schema, S1 in-question presentation, S2 name-map + binding enum, N6
  degenerate-case disarm in R11's own text, N9 pins `797ad42`, no tool-exposure row).
- N2 via the covered-by-stronger-mechanism precedent (summarization-prompt structure is a binding
  §3 contract — stronger than an Ask-First entry). N9 read as "pins the generating guide commit".
- P7's round-1 gap closed in both R7 and the §3 SummaryRecord schema.
- **New unpinned-variance observation** (not a property): regen-A pinned a single model for all
  LLM roles; regen-B kept the course's gpt-5-mini/gpt-5 split as the model-row default. Candidate
  for a future pass (deterministic model-role pinning rule).

### Confirmation set 1 (guide `797ad42`): regen-B 25/25 · regen-C 25/25 · regen-D 24/25 — **FAIL on P1**
- D's Ledger has 11 rows: the memory-core topology subject was baked into R1 + a binding §3
  StoreName contract, with no fewer-store alternative available anywhere [verified by scorer with
  quotes]. A/B/C all surfaced it as a row → 1-in-4 flake.
- Failure→fix trace: the design-argued bake-in litmus ("shown working as an acceptable
  alternative") lacked its evaluation frame — the course demonstrates the conversational-only
  baseline working (Lesson 2) then declares it insufficient for long-horizon goals; D read
  "insufficient for the goal" as a warning. Fix: litmus now distinguishes outgrown baselines
  (reduced-scope legitimate → row stays) from warned failures (errors/degradation → bake-in).
- Also logged: D split P8's contradiction across D4 + R5 (scored PRESENT — carry is what matters);
  D numbered the op-split row D7 (subject-scored, not number-scored).

### Confirmation set 2 (guide `a7de8ef`): regen-E · regen-F · regen-G
(First launch of E/F/G was killed mid-run by a session usage limit — external, not the pass;
partial draft discarded, identical relaunch. Scoring per the owner's cost decision: one full
scorer on the adoption candidate; targeted orchestrator greps on the other two.)

- **regen-F: 25/25 PRESENT [full scorer + grep spot-audit, verified]** — exact 12-subject P1
  (topology row D7 present with the outgrown-baseline alternative — the litmus fix working),
  S1 four requirements, S2 via the binding branch, S3 clean, label band in R6+AC10, pins `a7de8ef`.
- regen-E: **fails P1** — 11 rows, topology folded into binding contract again [grep-verified:
  0 topology rows]; S3/S1/P7/N9 hold [grep-verified].
- regen-G: **fails P1** — 13 rows, an extra partitioned-context row promoted via the structural
  route [report + grep count]; S3/S1/P7/N9 hold [grep-verified].

### Residual finding (to #18): Ledger row-set boundary variance (±1 row)

Across 9 regens over three guide hashes, the row *set* wobbles at exactly the judgment-boundary
subjects: the topology row is folded into the binding contract in ~2/9 samples (D, E — both
directions of the litmus were fixed, one recurrence after the fix), and the partitioned-context
subject was promoted once via the structural route (G). All other 24 properties are stable
across all 9 samples. Two targeted wording fixes (stakes-timing frame; outgrown-baseline litmus)
each reduced but did not eliminate the variance — assessed as residual generation variance, not
rule ambiguity (the guide's design-structural route even names "store topology" as an explicit
example and E still folded it). Owner policy applies: adopted specs are matrix-verified
individually; the flake affects only future regenerations, which are checked by this matrix.
Wording iteration stopped at diminishing returns per the owner's cost decision.
