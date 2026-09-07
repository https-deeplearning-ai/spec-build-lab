# guide-pins-v2 convergence property matrix

**Purpose:** score the two clean-room regenerations (`experiments/agent-memory/guide-pins-v2/regen-A|B/spec.md`)
against the hand-evolved fixture (`courses/agent-memory-building-memory-aware-agents/spec.md` @ guide-pins-v2).
Pass bar: **every property present in BOTH regenerations; no prior property lost.** Compare
property-wise, never diff-wise (regeneration is not byte-deterministic). Guide under test: `408a0fe`.

## Prior properties (from the PR #9 three-version comparison, carried forward)

| # | Property |
|---|---|
| P1 | **(re-targeted after round 1, owner decision)** Ledger covers exactly 12 subjects: the 6 learner rows + context-reduction strategy + tool-description augmentation + memory-core topology + deterministic/agent-triggered split + persistent store + acquisition toolset. Learner rows first, fixed group order |
| P2 | §0 gate: as-is/customize express lane; one question per row; no numeric cap; hard stop; printed resolved-decision checklist |
| P3 | "(course default)" labeling correct, incl. substitution rows (Oracle store, Tavily) tagged in Options |
| P4 | Restart AC: a new OS process reopens the same stores (headline invariant tested) |
| P5 | Keyless arXiv toolset is the default (ACs tagged live); Tavily (keyed) is an Option only |
| P6 | Store realization = SQLite via §3 branch-1 substitution; Oracle in Options as course default |
| P7 | Mined parameters all land: 256k budget + 128k fallback; chars//4; 50/80 thresholds; chunk 1,500/200; per-segment ks (KB 3, workflow 3, entity 5, summary 10, toolbox 5); 10-iteration cap; 3,000-char excerpt; 2,000-byte preview; 200-char answer excerpt; 500-char entity clip; 6,000-char summary input; PERSON/PLACE/SYSTEM enum; four summary headings; 8-char hex ids; 8–12-word labels |
| P8 | D4 model-name/token-map contradiction carried in-row |
| P9 | D8 classification-table-vs-loop contradiction carried in-row |
| P10 | Rules↔ACs bidirectional; offline/scripted/live split; per-AC evidence-reporting requirement |
| P11 | Recoverable consolidation intact: `# Question` never summarized; summary_id write-back; expand path |
| P12 | Fixture corpus authored (no course data); scripted LLM stand-in; fixture-mutation ban |
| P13 | Self-contained: CTX-A…E present; transcript-authoritative lesson numbering; no external references needed |

## New properties (the fixes under test)

| # | Property | Fixes |
|---|---|---|
| N1 | Ask First contains a deterministic/agent-triggered-line entry cross-referencing the D8-equivalent row | #8 core |
| N2 | Ask First is derived-complete: all six qualifying mined trade-off subjects appear (embedding model; distance/index after data; toolbox count / pass-all-tools; summarization prompt structure; store swap / Tavily; the D8 line) | #8 core |
| N3 | A fresh-init existence AC covers all seven declared stores/schemas | #8 residual |
| N4 | Distance = cosine as a body default (no Ledger row), contradiction noted in place with the §5.5 selection stated; consistency rule + AC retained | #8 residual / #11 Rule A |
| N5 | No contradicted Ledger rows for distance / index type / toolbox k; k carried as body default with its contradiction note | #11 Rule A |
| N6 | No tool-exposure Ledger row; semantic retrieval is a business rule; pass-all-tools appears only as the warned anti-pattern in narrative | #11 Rule B |
| N7 | Substitution default note states how "lightest" was determined; same realization in both regens | #8 residual |
| N8 | §6 titled "Standing Permissions (in force for the entire build)", three tiers populated | reframing |
| N9 | Provenance header carries the guide commit (`guide @ 408a0fe`) | pinning |
| N10 | Stability: every P/N property holds in BOTH regens of a round | the "luck" claim |
| N11 | **(round 2)** Partitioned context, tool-result flow, and search-and-store are business rules with ACs — not Ledger rows; their warned alternatives appear only as cited anti-patterns in narrative | consistent Rule B (owner decision) |
| N12 | **(round 2)** Keyed web-search row: Options = real Tavily "(course default)" / honestly-labeled local stand-in / omit; Default = omit (the keyless arXiv tool already carries search-and-store); no fake tool anywhere without an explicit stand-in label | keyed-tool rule (owner decision) |

## Scoring

One row per property per regen: `present / absent / partial (note)`. Any `absent`/`partial` →
tighten the specific guide rule, regenerate; never hand-patch the regen output.

## Round 1 (guide `408a0fe`; regen-A 15 rows / regen-B 13 rows)

| Prop | regen-A | regen-B | Note |
|---|---|---|---|
| P1 | partial | partial | Both drop fixture D9/D12/D13 (Rule B applied consistently — see F3); A adds a maturity-level row; acquisition-toolset row framed 3 ways across fixture/A/B |
| P2–P13 | present | present | Spot-checked: gate, labeling, restart AC, params, model-contradiction carry, self-containment all present in both |
| N1 | present | present | Both derived the det/agent Ask-First entry, cross-referenced |
| N2 | present | present | A: 8 entries; B: 9 (both supersets of the six fixture subjects; B's §14 self-check *caught and fixed* a missing entry — the audit mechanism worked) |
| N3 | present | present | Both AC1 = fresh-init existence of all seven stores |
| N4 | absent | absent | **F1**: both made distance a `contradicted` row, both citing "changing after data forces rework" as stakes-passing — Rule A never pinned WHEN stakes are evaluated |
| N5 | partial | partial | Index/toolbox-k correctly body defaults in both; distance row remains (F1) |
| N6 | absent | present | **F2**: A kept a tool-exposure row (sanitized options — no pass-all option); B baked it fully ("Never: passing the full tool registry") |
| N7 | present | present | Both SQLite stdlib, tier named — the tier rule converged the flagship variance case |
| N8, N9 | present | present | Title + guide pin in both |
| N10 | **fail** | **fail** | Row-set variance A↔B (15 vs 13; maturity row; tool-exposure row; web-search row framing) |

## Round 2 (guide `e2db8be`; regen-A2 12 rows / regen-B2 13 rows)

Two-for-two on everything except two complementary wobbles:
- A2: **exact 12-row target** (N6 ✓, N4/N5 ✓ zero contradicted rows, N11 ✓, N12 ✓ Tavily omitted w/ honest stand-in + "(course default)" in Options) — but store = SQLite + Chroma (tier 2 for vectors): **N7 ✗** (judged "satisfies" at aspirational scale).
- B2: store = SQLite-only tier 1 ✓, N4/N5/N11/N12 ✓, existence AC-1 ✓ — but kept a sanitized tool-exposure row (13 rows): **N6 ✗** (Rule B's litmus counted "static toolset when small" — the taught mechanism's degenerate case — as a second side).
- N10 ✗ (the two wobbles). Round-3 guide fixes: degenerate-case clause on Rule B's litmus; "judge tiers at declared default scale" clause on the §3 tier rule.

## Round 3 (guide `73c37ef`; regen-A3 13 rows / regen-B3 12 rows) — FINAL

- **B3: full pass, 25/25.** ~20 properties file-verified in-session (ledger shape, existence AC1,
  restart rule, cosine+euclidean dual citation, k=5 branch-2 lever, 256k/128k, chars÷4,
  max_iterations 10, 3,000/2,000 bounds, 6,000/4,000 caps, 8-hex ids, 8–12-word labels,
  PERSON/PLACE/SYSTEM schema enum, four headings, Tavily omit + "(course default)" + honest fake,
  tier-1 store with declared-scale reasoning, AF1–AF8 incl. AF4/AF5, gate hard-stop + one-per-row,
  CTX-A–E, transcript-authoritative numbering, `73c37ef` pin, "Standing Permissions", fixture ban,
  rule↔AC bidirectional refs); remainder verified by targeted grep this round. **Scoring note (N2):**
  two fixture Ask-First subjects are covered by stronger mechanisms in the 12-row shape —
  pass-all-tools is rule-forbidden (outranks Ask First); no index exists at tier 1 (entry moot;
  destructive resets = AF7). Judged pass.
- **A3: 24/25** — the tool-exposure subject re-entered as a `design-structural` row (file-verified),
  its third distinct route across rounds (A1 argued-sanitized → B2 argued → A3 structural) → residual
  F6; A3 otherwise converged (tier-1 store, zero contradicted rows, Tavily omit) [report].
- **Outcome:** owner accepted one-full-pass + residuals-filed (pass bar relaxed from two-for-two,
  2026-09-07); **B3 adopted** as the course spec.

**Evidence discipline:** claims above are [verified] (file/git checked this session) unless marked
[report] (subagent self-report). A2's properties rest on its report only; A1/B1/B2/A3/B3 ledgers and
key rows were file-verified.

### Findings
- **F1 (both; guide defect):** Rule A's stakes test lacks a timing anchor — "forces rework" was read as *any later change* forces rework, which every data-touching lever satisfies, so nothing demotes. Fix: evaluate stakes at initial choice time; later-change cost is §6's business.
- **F2 (A; two seeds):** the §5.5 procedure's "architecture-maturity progression" example seeded a row the course argues only as narrative; and Rule B's litmus ("shown working as an acceptable alternative") let a sanitized tool-exposure row back in via "static toolset viable when small".
- **F3 (both agree, against the fixture; DESIGN DECISION):** consistently applied, Rule B also demotes the fixture's D9 (partitioned context), D12 (tool-result flow), D13 (search-and-store) — rows PR #10 kept. The guide and the current spec now disagree beyond the four PR #10 removals. Needs an owner decision before round 2.
- **B quirk:** B realized web search as a fixture-backed `search_web`, brushing against §3's "fixtures substitute for data, not tools"; A omitted it (arXiv carries the invariant). One-of-two divergence ⇒ the wording leaves room.

## Addendum (2026-09-08) — adoption reverted; PR #20 reshaped to guide-only

Two post-hoc discoveries changed the shipping decision:
1. The session's baseline was **stale local main** — PRs #15/#16 (scope-boundary D6 row, merged
   2026-07-28) were missing from it. Every "current spec" comparison above, including P1's
   subject list, was measured against a spec without that merged improvement.
2. Regen-B3 therefore **regresses the merged #15 shape** (its row 6 is the pre-#15 single-option
   form), because the guide-side rule (PR #17) never merged — the guide could not reproduce what
   it never learned.
3. The owner also reports strong positive field feedback on the shipped spec.

Owner decision: PR #20 ships the **guide evolution only** (validated by the six regens recorded
above; closes #8/#11). B3 is retained under `experiments/agent-memory/guide-pins-v2/` as the
guide's validation evidence, not adopted. Spec replacement is deferred to the shakedown promotion
pass, whose confirmation regen will additionally carry the #17 scope-boundary rule, F6, and F7 —
strictly dominating B3, with no regression window.
