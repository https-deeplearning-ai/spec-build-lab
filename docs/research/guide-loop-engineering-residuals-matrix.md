# guide-loop-engineering-residuals — promotion-pass matrix

**Course:** loop-engineering-with-langchain-deepagents (both modes) · **Guide under test:**
base `3584b8f`, overlay `edcfe34` (updated per round) · **Regen model:** Opus 5.5 (skill policy;
orchestrator on Fable 5.1).
**Pass bar:** every property present in every confirmation regen; evidence labels required on
all claims. This pass also pays the confirmation regen owed by `guide-sources-and-tiebreaks`
(its properties are carried forward below).

## Decision log (Phase 1, 2026-10-12)

Owner accepted every proposed verdict and decision D1–D14; S3 resolved "stays a §2 pin".

| Candidate | Verdict | Owner decisions attached |
|---|---|---|
| F1 tie-breaker (1) attribution | guide-only | D1 wording: "the failure attributed to Y itself, not to the absence of something the course adds later" |
| F2 presented-not-argued | guide-only | D3: presentation alone never triggers design-argued; structural route remains open |
| F3 READMEs with code | guide-only | Pass A evidence |
| F4 heuristic → number | guide-only | label + post-build lever |
| F5 scripted model for LLM-driven offline suite | promote | D4: realization row in standalone mode; overlay may resolve; scripted model declared in §5 |
| X1 tie-breaker (2) numeric knobs | promote | D2 wording |
| S2 "none silently dropped" | guide-only | declared drop is compliant |
| S3 harness fits no route | already-covered | stays a §2 pin; one clarifying sentence in §5.5 |
| A2 default exercised (#26) | promote | — |
| A3 fixtures declared first (#26) | promote | — |
| A4 schema constraints tested (#26) | promote | — |
| AU1 self-containment + CTX-C glossary | promote | — |
| AU2 row-id prefixes | promote | D12: never a bare `R`; prefixes free |
| AU3 verdict replay | promote | — |
| AU4 reciprocal citation form | promote | fixed form so the check is mechanical |
| O1 AGENTS.md root-only | promote (overlay) | D5 |
| O2 key variable names | promote (overlay) | D6: the four names from `environments/` §9 |
| O3 Runtime (lab) section | promote (overlay) | D7: ADD 5, between §7 and the Context Pack |
| O4 §0 appended paragraphs | promote (overlay) | D8: OVERRIDE 4 |
| O5 pin vs preinstalled | promote (overlay) | D9: course pin wins inside the venv |
| O6 levers of CONSTRAINED rows | promote (overlay) | D10: body lever + Ask First |
| OBS resolution never retires a course-owned row | promote (overlay) | D11 sentence in OVERRIDE 2 |
| T1 tooling (checker, audit step, SKILL.md bookend, regen-prompt slides/lab) | routed-out → done on this branch as skill work | D13 Opus-class subagents |

## Core properties (carried forward)

From `guide-sources-and-tiebreaks-property-matrix.md`: S1–S4 (slides), V1–V2 (course pins),
O1 (one design group), T1–T3 (litmus branch record, no demonstrated-failure row, value-only →
lever). From earlier passes (guide-pins-v2, gate-semantics): gate shape (express lane, one
question per row, hard stop, no cap, printed+written checklist), deterministic single default
per row, fixtures authored, rules↔ACs bidirectional, provenance labels, CTX-A…E present.

## Pass properties

| # | Property (checkable, quotable) | Type | Candidate |
|---|---|---|---|
| P-F5 | Standalone: a `realization` row "which model the acceptance suite runs against" with a scripted stand-in Default and the live model "(course default)" in Options; lab: a business rule + the scripted model; in both, `scripted_model` (or equivalent) declared in §5 with per-role scripts | content | F5 |
| P-X1 | No Ledger row whose sides differ only in a number; model-per-role (identities) IS a row or is argued-out with a recorded branch — never a lever by tie-breaker (2) | content | X1 |
| P-F2 | The grader-realization subject's Category is `design-structural` (or it is narrative), never `design-argued` on slide 2.6's presentation alone | content | F2 |
| P-A2 | Every behavior-changing Ledger default (augmentation-type, on/off modes) has an AC that runs through that default | content | A2 |
| P-A3 | Every fixture/script/planted state an AC names is declared in §5 — `check_spec.py` FIXTURE = 0 | mechanical | A3 |
| P-A4 | Every `minLength`/enum/band/const in §3 that encodes behavior has an AC | content | A4 |
| P-AU1 | `check_spec.py` GUIDE-SECT = 0 and GUIDE-VOCAB = 0; CTX-C opens with "How to read the provenance notes" | mechanical | AU1 |
| P-AU2 | `check_spec.py` ROWID = 0 | mechanical | AU2 |
| P-AU3 | Every verdict-asserting AC replays correctly against its fixture (auditor check f) | content | AU3 |
| P-AU4 | `check_spec.py` CITE-AC = CITE-RULE = RECIP = 0 | mechanical | AU4 |
| P-O1 | Lab: Never tier names the workspace-root `AGENTS.md` only; the course's `/memories/AGENTS.md` lives in the run folder | content | O1 |
| P-O2 | Lab: the spec names exactly `OPENAI_API_KEY`/`OPENAI_BASE_URL`/`ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`; no discovery instruction | content | O2 |
| P-O3 | Lab: `## Runtime (lab)` present between §7 and the Context Pack; the root-absolute-URL pitfall lives there, not in CTX-B | content | O3 |
| P-O4 | Lab: §0 template verbatim + exactly the two `[environment]` paragraphs | template | O4 |
| P-O5 | Lab: §2 says the course pin wins inside the venv where a preinstalled copy differs | content | O5 |
| P-O6 | Lab: the model-tiering trade-off is a body lever with an Ask-First entry | content | O6 |
| P-OBS | Lab surfaces every course-owned row the agnostic run surfaces (instruction placement, learning-loop change target, model-per-role treated the same way in both) | content | OBS |

## Baseline (mechanical, `check_spec.py`, zero LLM cost)

| Spec | Findings | Classes |
|---|---|---|
| loop-eng `spec.md` as generated (`0f8904e`) | 13 | RECIP 4, ROWID 2, CITE-AC 1, GUIDE-SECT 1, GUIDE-VOCAB 5 |
| loop-eng lab as generated | 43 | RECIP 30, CITE-AC 4, CITE-RULE 1, GUIDE-SECT 1, GUIDE-VOCAB 7 |
| loop-eng `spec.md` after repairs | 0 | — |
| loop-eng lab after repairs | 1 | GUIDE-VOCAB ("substitution row" undefined) |
| Qdrant `spec.md` (previous guide) | 13 | RECIP 7, XREF 3, GUIDE-VOCAB 3 |
| Qdrant lab (previous guide) | 3 | GUIDE-VOCAB 3 (rule did not exist then) |
| agent-memory `spec.md` (previous guide) | 8 | RECIP 4, GUIDE-VOCAB 4 |

Reading: the mechanical defect class is not new to this course; every earlier spec carries
reciprocity failures, and the GUIDE-VOCAB rows are expected (the rule post-dates them). The
loop-engineering lab spec was the worst by far (30 reciprocity failures), consistent with its
size. The script would have caught most of what the audit loop found.

## Rounds

### Round 1 (base `3584b8f`, overlay `edcfe34`; regen-A agnostic, regen-LA lab; both Opus 5.5)

Regens: `experiments/loop-engineering/guide-loop-engineering-residuals/regen-A/spec.md`
(764 lines, 10 rows, 34 rules, 41 ACs, 324k tokens) and `regen-LA/spec.coding-agent-lab.md`
(782 lines, 5 rows, 32 rules, 43 ACs, 349k tokens). **Both arrived with `check_spec.py` = 0
findings** — the first generations in this repo to do so (the as-generated baseline was 13 and
43). Scorers: one Opus 5.5 subagent per regen; orchestrator spot-checked 5 of 23 verdicts on
regen-A by grep (L4 row, D2/D3 route sentences, AC17's phrase, `ungraded` in ACs, CTX-E slides)
— all held.

| Prop | regen-A | regen-LA | Evidence label | Note |
|---|---|---|---|---|
| Core S1–S4, V1–V2, O1, T1–T3 | PRESENT | _(scoring)_ | [verified] S1, T1; rest [reported] | — |
| Core gate / default / fixtures / rules↔ACs / labels / CTX | PRESENT | _(scoring)_ | [reported] | — |
| P-F5 | PRESENT | PRESENT | [verified] RR1 row + F7 per-role scripts | — |
| P-X1 | PRESENT | _(scoring)_ | [verified] L4 row carries model-per-role | — |
| P-F2 | PRESENT | PRESENT | [verified] "the slide alone is presentation, not an argued trade-off" | — |
| P-A2 | PRESENT | _(scoring)_ | [reported] | lever cap 40 untested — lever, not a default |
| P-A3 | PRESENT | PRESENT | [verified] checker FIXTURE = 0 | — |
| P-A4 | **PARTIAL** | _(scoring)_ | [verified] `ungraded` reached by 0 ACs; `failed` never produced | failure→fix below |
| P-AU1 | PRESENT | PRESENT | [verified] checker GUIDE-SECT/VOCAB = 0; CTX-C how-to present | scorer worried about Category names; they are the Ledger's own column vocabulary, not guide jargon |
| P-AU2 | PRESENT | PRESENT | [verified] checker ROWID = 0 | — |
| P-AU3 | **PARTIAL** | _(scoring)_ | [verified] AC17 asserts "Report Export" in a snapshot; the scripted worker writes only clause bullets, none containing it | failure→fix below |
| P-AU4 | PRESENT | PRESENT | [verified] checker RECIP = 0 | — |
| P-O1…P-O6, P-OBS | n/a | _(scoring)_ | — | regen-LA course-owned rows = D1, D2, D3, RR1 = regen-A's (P-OBS looks PRESENT; awaiting quote) |

Failure→fix traces (base guide):
- **P-AU3** failed because §8 "Fixture numbers reproduce the verdict" scoped replay to *values a
  rule computes* ("a pass count, a regression verdict, a threshold crossing"); a content
  assertion produced by the scripted model was outside its words. Fixed: the paragraph now covers
  any asserted outcome that follows from declared fixtures or scripts, content included; §14 line
  aligned.
- **P-A4** failed because "an enum … has ≥1 AC asserting it" was satisfied by one value; two
  values (`ungraded`, `failed`) a rule can produce were reached by no AC. Fixed: every enum value
  a rule can produce is reached by some AC, or removed; decided at handoff.

Overlay gaps regen-LA reported (precedence rule 3), fixed for round 2:
- OVERRIDE 4 named the gate steps by the wrong numbers (1 and 5; the template's are 2 and 3) —
  now identified by content, never by number.
- The scripted-model realization row's status in lab mode was unstated (base: "an overlay may
  resolve the row"; OVERRIDE 2: course-owned rows stay) — now: it stays; its live Option notes
  the lab supplies the key. Owner decision D4 amended accordingly.
- The platform's model set is not enumerated — now stated, with the rule that model ids come
  from environment variables at build time and course ids are provenance only.
- ADD 1 said environment invariants "move to the rows that need them" — now "rules, or rows".

## Confirmation & adoption

- Confirmation set: N=2 per mode after a passing round.
- Adoption decision: deferred (D14).
