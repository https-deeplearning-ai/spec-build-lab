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

_(filled after generation)_

| # | spec.md | spec.coding-agent-lab.md | Evidence |
|---|---|---|---|

## Findings

_(filled after generation)_

## Status

- Regen 1 (agnostic): pending.
- Regen 1 (lab): pending.
- Confirmation regen: **owed**. Run later, in a worktree, on this course or on Qdrant (which
  has slides, speech input, and pinned deps). Until then the guide changes are validated by one
  run per mode.
