---
name: promote-to-guide
description: Runs a promotion pass in the spec-build-lab — triages a course spec's hand edits and filed observations, promotes the universal ones into the spec-generation guide, validates the amended guide with clean-room regenerations, and optionally re-baselines the course spec. Use this skill ANY time the user wants spec improvements carried into the guide or future courses — including phrasings like "promote these spec edits", "make the guide learn this", "run a guide pass", "evolve the guide", "the next guide pass", "implement the residuals from issue #NN", "carry this principle to future specs", "co-evolve the spec and the guide", or "/promote-to-guide". Do NOT use it to generate a spec (/generate-spec), to hand-edit a course spec (just edit it — that's Loop A, no skill), or for lab tooling/skill changes (those are ordinary code work).
---

# promote-to-guide

Move improvements from one course's spec into the universal spec-generation
guide — selectively, validated, and without breaking the pinning doctrine.

## Doctrine (why this skill is shaped the way it is)

- **Two loops.** Loop A: a course's `spec.md` is the primary, living artifact —
  hand-edit it freely, commit the edits, keep the provenance line honest
  ("generated from guide @ <hash>; hand-evolved since"). Loop A is deliberately
  not a skill: editing must stay frictionless. Loop B — this skill — runs
  occasionally to decide which accumulated improvements the guide should learn.
- **Not every spec edit becomes a guide rule.** Course-specific edits stay in
  that spec forever; that is legitimate, because every spec is *pinned* to the
  guide version that generated it and is never silently regenerated.
- **Regenerations are evidence, not replacements.** A clean-room regeneration
  tests whether the amended guide reproduces the promoted principles. Adopting
  a regeneration as the course's new spec is a separate, explicit owner
  decision with a precondition (below) — never an automatic pipeline step.
- **Whatever the guide doesn't pin, regeneration reproduces only by luck**
  (the lab's founding observation). A promoted principle therefore needs three
  things together: a guide rule, a §14 audit line, and a validated regen
  property. **Fix and test travel together** — never ship an untested rule,
  never leave a tested fix unshipped.

## Inputs

- **Course** — infer from cwd if inside `courses/<name>/`; otherwise ask.
  Never default silently.
- **Candidates** (optional) — issue numbers or free-text improvements. If not
  given, enumerate them yourself in Phase 0.
- Run from the repo root on a fresh branch: `git checkout -b guide-<passname>`
  (pick a short slug for the pass; it names the branch, matrix, and evidence dirs).

## Phase 0 — Enumerate candidates

1. Hand edits: `git log -p --follow -- courses/<course>/spec.md` since the
   commit named in the spec's provenance line (`guide @ <hash>` or the last
   adoption). Each distinct change is a candidate.
2. Filed observations: open issues that propose guide rules or record
   generation-variance findings.
3. Anything the user handed you directly.

Present the combined list. Route out anything that isn't guide territory
(lab tooling, skill bugs, build defects) to its own issue — say where it went.

## Phase 1 — Triage with the owner (before touching any file)

Walk every candidate with the owner (use a structured question tool, batched).
Exactly one verdict each:

| Verdict | Meaning | What happens |
|---|---|---|
| **promote** | universal principle | guide rule + §14 audit + matrix property (+ spec fixture edit if the spec doesn't yet exhibit it) |
| **keep-local** | course-specific | stays in this spec only; no guide change; excluded from matrix scoring |
| **already-covered** | guide already produces it | nothing; cite the covering rule |
| **guide-only** | the spec is already right, but regeneration reproduces it unreliably | guide rule + audit + matrix property; no spec edit |

Then, still before editing: derive every open **design decision** the promoted
set implies (value choices, naming, precedence rules) and ask them **in one
batch**. Decisions discovered mid-pass cost a regen round each; decisions
captured here cost nothing. Record verdicts and decisions in the matrix's
decision log (Phase 3).

**Presenting the triage table ends your turn.** Wait for the owner's verdicts;
never invent, assume, or default them — an un-answered candidate is not a
"keep-local", it is an open question. (This is the spec §0 gate's
silent-default trap, applied to triage: the moment you finish presenting, you
trivially have "no response yet", and treating that as permission makes the
ask theater.)

## Phase 2 — Edit

**Spec fixture (only for promoted items the spec doesn't yet exhibit):** edit
`courses/<course>/spec.md` to be the target the regen is scored against.
Verify the diff is what triage approved — run `git diff`, confirm every hunk
maps to a verdict, nothing else changed. Update the provenance line's
hand-evolved note. Commit spec edits **separately** from guide edits.

**Guide** (`.claude/skills/generate-spec/references/spec-generation-guide.md`):
read `references/wording-discipline.md` FIRST — every leaked rule in the
pass that created this skill traced to one of its three rules. For each
promoted/guide-only item: one course-agnostic rule in the right section, plus
one §14 checklist line that *references* the rule (never restates its
mechanics). Commit the guide edits on their own, **before any regeneration** —
the regens cite this commit hash in their provenance headers.

## Phase 3 — Matrix

Create `docs/research/<passname>-matrix.md` from
`references/matrix-template.md`: the carried-forward core properties, one
named property per promoted/guide-only item, the decision log, and the
verified/reported evidence convention. The matrix is the pass's single source
of truth — round results, evidence labels, and owner decisions all land here.

Two property types, treated differently:
- **content-presence** (the default): the spec must *contain* the principle —
  scored by finding and quoting the content wherever it lives.
- **template-conformance**: for rules that change guide text which specs emit
  **verbatim** (e.g. the §6.0 gate template). Scored by comparing the spec's
  emitted section against the template's required text, near-exactly. When a
  pass touches a verbatim template, the carried-forward core properties that
  describe that section must be consciously **updated to the new template,
  never copied forward** — log the update as an owner decision.

## Phase 4 — Converge

1. **Regenerate**: spawn a fresh isolated subagent (general-purpose — never a
   fork, which would inherit this conversation and contaminate the clean room)
   using `references/regen-prompt.md` verbatim with its three slots filled
   (course, output path `experiments/<course>/<passname>/regen-<X>/spec.md`,
   guide commit hash). **N=1 while iterating** — a single regen suffices to
   find a leak.
2. **Score**: spawn a fresh scorer subagent per regen (prompt template in
   `references/regen-prompt.md`): it reads only the matrix and the regen
   output, and must return a per-property verdict **with quoted line evidence**.
   Spot-audit at least a fifth of its verdicts yourself against the file.
   Label everything in the matrix [verified] or [reported] — a claim without
   a label is a claim you can't trust later.
3. **On failure**: identify the specific rule sentence the failure traces to
   (every failure in the founding pass traced to exactly one), fix it, log the
   round in the matrix, commit, regenerate. Expect 2–3 rounds; that is the
   loop working, not failing.
4. **Confirm**: when a round passes, run the confirmation set — **N=2** fresh
   regens by default; **N=3 or more when a property's failure mode is a known
   coin-flip** (N=2 detects a 50%-flaky defect only ~75% of the time). Pass
   bar: every property present in every confirmation regen.
5. Cross-course validation is **deferred by owner decision**: the next new
   course's `/generate-spec` is the de-facto test — treat any principle-miss
   there as a trigger for the next promotion pass.

## Phase 5 — Adoption (explicit owner decision, never automatic)

Ask the owner whether to adopt a confirmation regen as the course's new
`spec.md`. Precondition — both must hold:
- the owner wants the course re-baselined to the new guide, AND
- adoption erases no keep-local edits (there are none, or the owner
  explicitly discards them).

**If adopted:** copy the regen over `spec.md` (never hand-patch regen output —
if it's wrong, the guide is wrong; go back to Phase 4), commit separately,
then validate behaviorally: a fresh `/prepare-build` run (never reuse an
allocated run; retire unbuilt ones with a note), build as-is, run the AC
suite, both evals, and a temptation probe per new guard
(`references/probes.md`).

**If not adopted:** the spec keeps its hand-evolved state and pin; the regens
remain as evidence in `experiments/`. Run probes for new guards against the
current spec (scratch copy + fresh subagent) — guards are prompt-enforced, so
the probe is their only behavioral test.

## Phase 6 — Ship

- PRs: guide changes and spec changes as separate commits (separate PRs when
  independent) so each can be reviewed against its own question.
- Close the issues the pass implements; file residuals for anything deferred —
  with their proposed fix text recorded but **not applied** (fix and test
  travel together).
- Finalize the matrix (rounds, evidence labels, adoption decision) — it is the
  pass's permanent record, like PR #9's comparison matrix was.

## Don'ts

- Don't hand-patch a regeneration's output — it defeats the entire experiment.
- Don't regenerate other courses' specs — they are pinned; leave them alone.
- Don't ship a guide rule without its §14 audit and matrix property.
- Don't trust a scorer's (or your own) pass claim without line evidence.
- Don't start regens before the guide edits are committed — the hash is the pin.
- Don't ask design decisions one at a time across the pass — batch them in Phase 1.
