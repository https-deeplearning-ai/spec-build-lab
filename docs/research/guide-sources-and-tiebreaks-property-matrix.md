# guide-sources-and-tiebreaks property matrix

**Purpose:** score the first generation of the loop-engineering course spec — agnostic `spec.md`
and the `--env=coding-agent-lab` variant — against the guide and overlay changes made on branch
`course/loop-engineering-with-langchain-deepagents` (base guide `f1ab452`, overlay `a63e0e5`).
This pass differs from earlier ones: the validation regen is a **new course's first generation**,
not a regeneration of a course with a known-good spec. So "no prior property lost" has no anchor
here, and one generation per mode is one regen, not two. The guide changes ship validated by a
single run; a second confirmation regen is owed (see "Status").

Compare property-wise, never diff-wise.

## Properties under test — base guide (apply to both specs)

| # | Property | Source |
|---|---|---|
| S1 | Slides were read: CTX-E lists the slides consulted and marks each video-shown or deck-only | #29, §3/§4 |
| S2 | At least one slide-only fact (absent from notebooks and transcripts) lands in the spec, cited to the slide | #29, §4 |
| S3 | Where a deck-only slide conflicts with code or narration, the spec records the conflict in CTX-C and the code/narration side wins | #29, §4 |
| S4 | Deck lesson numbering did not leak: CTX-E uses transcript numbering (1–7) | §12.1 |
| V1 | §2 pins the course's own versions for every dependency the course pinned, and says so; no "modern" version replaces a course pin | #28 F4, §5 step 5 |
| V2 | A dependency the course left unpinned (if any) is the only place a modern version appears, with the case stated | #28 F4 |
| O1 | Ledger row order: learner → design (argued and structural interleaved by pipeline position, no sub-blocks) → realization → contradicted | #28 F3, §5.5 |
| T1 | Every `design-argued` subject — row, bake-in, or lever — records which litmus branch decided it | #28 F1 (c) |
| T2 | No Ledger row offers an alternative the course showed failing | #28 F1 tie-breaker 1 |
| T3 | No Ledger row's sides differ only in a value; such subjects are body defaults with an Ask-First entry | #28 F1 tie-breaker 2 |
| P1 | Every §14 line added this pass is discharged (slides weighting, version pins, row order, branch record) | §14 |

## Properties under test — overlay (lab variant only)

| # | Property | Source |
|---|---|---|
| G1 | §1 states the deliverable's shape (one server on port 4000 serving page + API, or the library-plus-tests escape with its reason), labelled `[environment]` | #30 G1, ADD 4 |
| G2 | A constraint both the course and the environment require is one rule labelled "course-demonstrated, reinforced `[environment]`", not two rules | #30 G2, ADD 2 |
| G3 | The Environment Resolutions table says "Invariant empty" for dimensions whose Invariant is empty, instead of inventing an AC or an excuse | #30 G3, ADD 3 |
| G4 | Title line reads `# Spec: <Project> — Coding-Agent-Lab Build` | #30 G4, OVERRIDE 3 |
| G5 | Provenance header pins base `f1ab452` and the overlay commit obtained per ADD 3 | #30 G5 |
| G6 | `environments/coding-agent-lab.md` was not opened during generation (generator's own report) | #30 G6 |
| G7 | Staleness check passed: all three OVERRIDE quotes matched the base verbatim | overlay header |

## Prior properties carried forward

The P-series from `guide-pins-v2-property-matrix.md` and the gate-semantics properties still
apply (gate shape, one question per row, deterministic defaults, fixtures authored, rules↔ACs
bidirectional, provenance labels). Spot-check them; a regression there is a finding even though
this pass did not touch those rules.

## Results

Lab run: clean-room subagent, 2026-10-11, base `f1ab452`, overlay `a63e0e5`; output 1052 lines /
14,123 words. Report: scratchpad `gen-report-lab.md` (not committed). File-verified unless marked
[report].

Agnostic run: clean-room subagent, same day, base `f1ab452`; output 588 lines / 14,240 words;
14 Ledger rows (6 learner, 4 design-argued, 2 design-structural, 2 realization, 0 contradicted).
Report: scratchpad `gen-report-agnostic.md` (not committed).

| # | spec.md | spec.coding-agent-lab.md | Evidence (lab; agnostic where it differs) |
|---|---|---|---|
| S1 | PASS | PASS | CTX-E lists Wide 1–13, Tall 1–18 by lesson; title cards and Tall 15–16 marked deck-only (both) |
| S2 | PASS | PASS | Slide 2.6 "deterministic or agentic" is the only source of the deterministic-grader Option (both: lab D-S1, agnostic D2); agnostic also took the webhook trigger (2.8) and middleware hook names (3.3) from slides |
| S3 | PASS | PASS | CTX-C: slide 3.4 "Agent.md" vs code `AGENTS.md` → code wins; slide 3.5 `fetch_requirement_from_jira` vs narration → narration wins; slide 6.2 two placeholders vs five → five. No slide fact overrode code or narration (both) |
| S4 | PASS | PASS | CTX-E uses transcript lessons 1–7; the no-lesson event app is its own row (both) |
| V1 | PASS | PASS | §2 pins the `uv.lock` versions (deepagents 0.7.11, langchain 1.3.18, langgraph 1.2.11, openai 3.6.0, pydantic 2.13.5 …) and states the floors-vs-lock situation (both; identical pin set) |
| V2 | PASS | PASS | flask: floor only, absent from the lock, stated unpinned (both); agnostic keeps it with a "choose a current 3.x" note, lab swaps to preinstalled FastAPI `[environment]`; agnostic adds `pytest` as hardening |
| O1 | PASS | PASS | Lab: D-L1, D-A1, D-A2, D-S1, D-A3. Agnostic: L1–L6, D1–D4 (argued), D5–D6 (structural), R1–R2 — design group in pipeline order, argued rows happen to precede structural ones; no sub-block split |
| T1 | PASS | PASS | "Litmus: row" in all six agnostic design rows; "Litmus branch:" in all five lab rows; levers recorded beside the value and in CTX-C (both) |
| T2 | PASS | PASS, with a tension (F1) | No row offers a demonstrated-failure side (both); agnostic keeps the warned "analyst on the cheaper model" out of Options and in the Trade-off |
| T3 | **SPLIT** | PASS | Model-per-role: lab → lever (tie-breaker 2, "sides differ only in a model id"); agnostic → design-argued row D3 (one model vs several across roles). See X1 |
| P1 | **FAIL** | **FAIL** | Originally recorded PASS on the generators' word. An independent §14 audit (same day, fresh subagents, read-only) found 14 hard / 10 soft defects in spec.md and 8 hard / 13 soft in the lab spec. Agnostic: a systematic rule-renumbering slip (nine citations point at the wrong R-n), rows and rules both named `R1`/`R2`, one AC citing no rule, a scope tag outside the four classes. Lab: AC28 unsatisfiable (its fixtures cannot produce the "regression" it asserts), two ACs needing fake-model scripts no fixture declares, references to the guide's own sections leaking into the spec, four ACs citing no rule, one failure mode without fixture or AC. None touches the properties above; all are consistency defects the generator's self-audit should have caught. Hand-fixed per Loop A, then re-audited — see "Audit and repair" below. |

**Cross-run comparison (the point of running two modes on one course).** Subjects below are
course-owned, so the mode should not change them.

| Subject | spec.md | spec.coding-agent-lab.md | Read |
|---|---|---|---|
| Grader realization | D2 `design-argued` | D-S1 `design-structural` | Same row, different Category — F2 |
| Trigger kind | D4 `design-argued` | D-A2 `design-argued` | Agree |
| Loop composition / nesting | D5 `design-structural` (self-flagged: should be argued by precedence) | D-A1 `design-argued` | Same decision, Category split; both chose *row* on the Lesson 5 borderline — F1 wording still worth tightening, but the tie did not bite |
| Model per role | D3 row | lever (R20 + Ask First) | **Split** — X1 |
| Instruction placement (memory file vs skills vs system prompt) | D1 row (Lesson 3 argues it) | no row; skills → Not Included #3 | **Split** — X2 |
| Learning-loop change target (prompt vs tools/grader/config/memory) | D6 `design-structural` row | no row; bake-in (prompt-only change, R18) | **Split** — X3 |
| Human oversight points | bake-in (R20) | D-A3 row + bake-ins R14/R18 | Partial split — X4 |
| Send-back budget 3 vs 2; simulated failures 2 vs 0 | levers, branch (1) | levers, branch (1) | Agree |
| LLM for the offline suite | R1 realization row (scripted stand-in) | CONSTRAINED by the lab; scripted model as hardening R24 | Mode-consistent; both report the guide silent — F5 |
| G1 | n/a | PASS | §1 "Deliverable shape `[environment]`: one server on port 4000 serving both the page and its API"; escape explicitly not taken, reason given |
| G2 | n/a | PASS | R15 "every run is written to disk" carries "Course-demonstrated, reinforced `[environment]`", one rule, both citations |
| G3 | n/a | PASS | Resolutions table, project row: "derived Invariant empty — no AC owed" |
| G4 | n/a | PASS | Line 1: `# Spec: Requirements Review Loops — Coding-Agent-Lab Build` |
| G5 | n/a | PASS | Header pins base `f1ab452` and overlay `a63e0e5`; overlay hash obtained per ADD 3 [report] |
| G6 | n/a | PASS [report] | `environments/coding-agent-lab.md` not opened |
| G7 | n/a | PASS [report] | All three OVERRIDE quotes matched with `grep -F` |

## Findings

**Base guide**

- **F1 (T2 tension, loop composition).** The generator found the new tie-breaker (1) "a demonstrated
  failure wins" and the older "moves beyond" clause pulling against each other on whether the
  agent-loop-only configuration is a legitimate subset or the failure case Lesson 5 shows. It chose
  *row*, citing Lesson 2's explicit endorsement of subsets, and recorded the branch. Reading: the
  tie-breaker's "shows Y failing" needs one more word — the course must show Y failing *as Y*, i.e.
  attribute the failure to the alternative. Lesson 5's first attempt fails the rubric, but the course
  frames that as "finished isn't good enough", a reason to add a loop, not as the agent loop breaking.
  Candidate wording: *"shows Y failing — the failure attributed to Y itself, not to the absence of a
  later addition"*. Not applied; wait for the agnostic run to see whether it split the same way.
- **F2 (route precedence when an alternative is presented but not argued).** Slide 2.6 presents a
  deterministic grader with no trade-off argued. The generator put the row under `design-structural`
  and said why. The guide's precedence rule assumes `design-argued` requires an *argued* trade-off;
  it never says what "presented, not argued" is. Candidate: one sentence — *presentation without a
  trade-off does not trigger design-argued; the subject may still enter through another route*.
- **F3 (README shipped with code).** The course's README and the event app's README carry rationale
  that no transcript lesson does. The guide weights notebooks, transcripts, and now slides; it is
  silent on READMEs inside the notebook dump. The generator treated them as notebook-dump evidence.
  Candidate: say so in §4 Pass A.
- **F4 (quantifying a spoken heuristic).** "Most runs" became "more than half", labelled as the
  generator's reading. No guide rule covers turning a heuristic into a threshold.
- **F5 (offline testing of an LLM-driven loop).** The keyed-tool rule produces stand-ins for tools;
  here the LLM itself is the dependency and the course's offline path replays recorded results. The
  generator added a scripted model as project hardening (R24). The guide is silent on this shape.

**Overlay** (all reported by the generator as overlay gaps, per precedence rule 3)

- **O1 `AGENTS.md` collision.** The runtime's "never author `AGENTS.md`" meets a course whose agent
  instructions file *is* `AGENTS.md` (a deepagents convention the learning loop edits). The
  generator kept the course path inside the run workspace and put only the root file in Never. The
  overlay must say the ban is the workspace-root file only.
- **O2 key / base-URL variable names.** Never given; the spec tells the build agent to discover them.
  The overlay (or runtime) should name them.
- **O3 "the Runtime section".** ADD 1 refers to a section the base template does not define. The
  generator added "Runtime (lab)" between §7 and the Context Pack. Name and place it in the overlay.
- **O4 verbatim §6.0 vs the `choices` fence facts.** The runtime says the spec "must say so" about
  click/typed equivalence, but no overlay text sanctions adding to the verbatim §6.0 block. The
  generator appended an italic `[environment]` paragraph. Sanction it explicitly.
- **O5 `--system-site-packages` vs course pins.** The runtime recommends the flag; §5 step 5 pins
  the course's `openai==3.6.0`; the preinstalled `openai` version is unstated. Resolved base-wins.
  Say which wins, or state the preinstalled versions.
- **O6 levers attached to a CONSTRAINED row.** Removing the model/provider row left the course's
  model-tiering trade-off with no gate home; it went to R20 + Ask First. Say where such levers go.

**Cross-run splits (both runs, same materials, same guide)**

- **X1 tie-breaker (2) over-reaches on identities.** The guide says "differ only in a number (a
  threshold, a `k`, a fetch depth)". The lab run applied it to model *identities* (shared vs separate
  models per role); the agnostic run did not, and Lesson 5 argues that choice aloud as a production
  decision. By the letter the agnostic reading is right. Candidate: add "— a numeric knob; not an
  identity, an assignment of roles, or a choice of component".
- **X2 instruction placement.** Lesson 3 argues memory file vs skills (progressive disclosure) and
  shows both working. The agnostic run made it a row; the lab run put skills in Not Included. Not a
  new-rule defect — the design-argued route already admits it — but a composition split on a
  clearly argued subject. Likely cause: the lab's project row is ANSWERED, and the generator read the
  assignment as fixing the instruction channel. Worth an overlay sentence: resolving the project
  dimension does not retire course-argued rows (OVERRIDE 2 already says so; it did not hold).
- **X3 learning-loop change target.** The course names several things the analyst may change and
  builds one. Agnostic: structural row. Lab: bake-in. Same shape as X2.
- **X4 human oversight.** Lab surfaced the *additional* gates as a row; agnostic baked the two
  mandatory gates in and left the optional ones to Trade-off/Ask First. Neither violates the guide;
  the guide does not say whether "optional additions the course lists" earn a row.
- Pattern across X1–X4: the lab run surfaced fewer course-owned rows (4 vs 8). OVERRIDE 2 says
  course-owned rows are untouched by lab mode; one run is not proof, but the direction is the one
  the overlay was written to prevent. Check on the confirmation regen.

**Agnostic-only findings**

- A keyless, non-argued, non-structural stack choice (the harness itself, `deepagents`) fits no
  Ledger route; it is a §2 pin only. The generator asks whether that is a gap. Owner call.
- Presentation-only helper constants (run names, tags, CSS) were dropped and the drop declared,
  against §14's "none silently dropped". Reading: dropping *loudly* is what the line wants; say so.
- SKILL.md's "end with a section" for the diagram bookend conflicts with the guide's anatomy
  (Context Pack last). Both runs put the instruction at the end of §7. Align the skill text.

**Materials**

- The event-driven loop has shipped code and deck-only slides but no transcript lesson. Not a guide
  defect; recorded because it shaped several judgement calls above.

## Audit and repair (2026-10-11, after generation)

Both specs were then put through a loop the lab had not run before: a **fresh, read-only subagent
audits the spec against the full §14 checklist plus mechanical checks** (rule↔AC reciprocity,
cross-reference targets, guide-section leaks, declared fixtures, fixture arithmetic replayed
against the rules, Options-vs-Invariant, Not Included tags vs §5.5 classes); a repair agent fixes
the list under a no-decision-change constraint; a new auditor re-reads. Hand edits are Loop A and
are recorded in each spec's provenance blockquote.

| Round | spec.md hard / soft | spec.coding-agent-lab.md hard / soft |
|---|---|---|
| 1 (as generated) | 14 / 10 | 8 / 13 |
| 2 | 3 / 8 | 4 / 10 |
| 3 | 2 / 12 | 3 / 14 |
| 4 | 2 / 9 | 1 / 10 |
| 5 | 1 / 11 | — |

Each round's one remaining hard item was fixed; the last repairs (agnostic round 5, lab round 4)
were not re-audited. Final sizes: spec.md 594 lines / 16.3k words; lab 1,237 lines / 18.2k words
(from 588 / 14.2k and 1,052 / 14.1k) — growth is missing fixtures, scripts, test hooks and ACs
added rather than assertions dropped. No Ledger row was removed and no default changed in either;
a few rules gained explicit statements of values the course code fixes but the generated text left
implicit, and two rows gained an option each by hand (both recorded).

What the hard defects were, by class (both specs, round 1): wrong cross-reference numbers from
late renumbering (9); ACs citing no rule or rules cited by no AC (6); guide section numbers or
vocabulary leaking into the spec (5); fixtures or scripts an AC relies on but §5 never declares
(3); fixture arithmetic that cannot produce the asserted verdict (1); a failure mode without a
fixture/AC leg (1); identifier collision between rows and rules (1). Roughly two-thirds are
scriptable.

Later rounds found things earlier rounds missed (round 2 caught guide-section leaks in Ledger
notes that round 1 passed over), and repairs introduced knock-on defects (adding an option made
another row's Invariant false). Convergence was real but slow.

**Finding (headline for #33).** The generator's own §14 pass is not a reliable gate: both
generators reported it done. `/generate-spec` needs (1) a mechanical consistency script run on
the output (zero LLM cost) and (2) an independent audit subagent before handoff, with the
generator repairing from its list. Cost of this manual loop: ~3.2M tokens across 18 agent runs;
the script would have removed most of it.

Remaining soft items (not fixed, judgement calls): B3 has no offline fixture (agnostic); tool
names asserted by ACs while CTX-D calls them perishable (agnostic); R20 carries two labels for
two claims (lab); D-A3 option (b) attaches to a tool the build lacks (lab).

Logs: `experiments/loop-engineering/sources-and-tiebreaks/audit/` (local, untracked).

## Status

- Regen 1 (agnostic): done — 10/11 base properties PASS, T3 split (X1).
- Regen 1 (lab): done — 11/11 base, 7/7 overlay PASS; 6 overlay gaps and 5 base ambiguities filed above.
- Findings F1, F2, X1 and the six overlay gaps O1–O6 are candidates for the next pass; none applied
  here (fix and test travel together).
- Confirmation regen: **owed**. Run later, in a worktree, on this course or on Qdrant (which
  has slides, speech input, and pinned deps). Until then the guide changes are validated by one
  run per mode.
