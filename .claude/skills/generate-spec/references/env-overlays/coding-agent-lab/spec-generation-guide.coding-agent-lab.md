# Spec Generation Guide — `coding-agent-lab` overlay

**Applies only when `/generate-spec` is invoked with `--env=coding-agent-lab`.** Without that
flag this file is not read and the base guide governs alone.

Written against base guide **`901c80c`**. This file carries the **rules**; its companion
`spec-generation-guide.coding-agent-lab.runtime.md` carries the environment's **facts**, and is
opened later, at OVERRIDE 2 Phase 2. Both are distilled from `environments/coding-agent-lab.md`.

---

## How to read this file

Read the base guide first, in full:
`.claude/skills/generate-spec/references/spec-generation-guide.md`. Then read this file — all of
it. **Do not open the `.runtime.md` companion yet**; OVERRIDE 2 says when, and the facts it holds
must not be in play while the six learner-context dimensions are being derived.

**Precedence**

1. Where this file quotes a base passage under **OVERRIDE**, this file wins.
2. **Everywhere else the base guide wins** — including any tension this file did not anticipate.
3. An unanticipated conflict is **never resolved silently.** Follow the base rule, finish the
   spec, and report the tension to the user as an *overlay gap*. It gets fixed in this file,
   not judged at generation time. (This rule exists because the first lab-targeted spec was
   produced by exactly such silent judgments, and none of them was recoverable afterwards.)

**`environments/coding-agent-lab.md` is provenance, not an input.** Do not open it during
generation. The two overlay files are its complete distillation for this pipeline. If a fact
seems to be missing, that is an overlay bug to report as an *overlay gap* (precedence rule 3),
not a gap to fill by reading around it.

**Staleness check — do this before generating.** Each OVERRIDE below quotes the base text it
replaces. Confirm each quoted passage still appears verbatim in the base guide. If one does
not, this overlay was written against an older base: **stop, say which quote no longer matches,
and do not generate.**

---

## Why this mode exists

The base guide produces a takeaway a learner downloads and builds **against their own project,
on their own machine, with their own coding agent**. Six of its Decision Ledger rows exist to
absorb what the generator cannot know: the learner's project, data, goal, model/provider and
environment, plus how much scope they want.

This mode produces a spec built **inside a known lab**: the agent, the container, the model set
and the assignment are all fixed before generation starts. The difference between the two modes
is entirely in *what is unknown at generation time* — not in what a good spec contains. Every
rule about mining, contracts, acceptance criteria, the Course Context Pack, failure encoding
and the pre-build gate applies unchanged.

---

## OVERRIDE 1 — §3, the input gate

Base guide `11b3673` §3 reads, verbatim:

> Generation is gated on **two inputs**. Verify each is actually present before generating.

**Replaced by:** generation is gated on **two required inputs plus this overlay**. The notebook
dump and transcripts remain required and remain the *only* course evidence. This overlay is a
third input describing the build target.

This overlay is **never course evidence.** Nothing traceable to it may carry a
*course-demonstrated* label, appear in CTX-A or CTX-B, or be attributed to the course in any
way. It gets its own label (see ADD 2) and its own row in CTX-E.

---

## OVERRIDE 2 — §5.5, procedure step (f)

Base guide `11b3673` §5.5 **Procedure** reads, verbatim:

> (f) add the six §3 learner-context rows, each Invariant holding only the pattern's capability requirements on that dimension (empty when none) — learner rows still get a course-derived default (e.g. project defaults to the §3 example-shape target);

**Replaced by a two-phase step. Both phases are mandatory and their order is load-bearing.**

**Phase 1 — derive all six, exactly as the base guide requires.** Project, data/inputs, goal,
model/provider, environment, scope-boundary. Each gets its Invariant (the pattern's capability
requirements on that dimension, empty when the pattern demands nothing) and its course-derived
default. **Do all of this before opening `spec-generation-guide.coding-agent-lab.runtime.md`.**
A dimension you have not written down cannot be resolved, and an unresolved dimension disappears
without trace — that is the exact failure this ordering prevents. The facts live in a separate
file precisely so this ordering is enforceable: you cannot un-read a section of a file you were
told to read in full.

**Phase 2 — now open `spec-generation-guide.coding-agent-lab.runtime.md`**, then resolve each of
the six against the Resolutions in ADD 1 and emit the resolution table into the spec. A dimension is resolved in one of three ways:

- **ANSWERED** — the lab fixes it. The row leaves the Ledger, and **its Invariant must land
  somewhere named**: a spec section, a business rule, or another Ledger row's Invariant. An
  ANSWERED dimension whose Invariant goes nowhere is a defect, not a simplification.
- **CONSTRAINED** — the lab narrows it without fixing it. The row leaves the Ledger and the
  constraint becomes a business rule or a §2 entry, with at least one acceptance criterion.
- **KEPT** — the lab has no opinion. The row stays in the Ledger exactly as the base guide
  derived it.

**Course-owned rows are never silently dropped by this mode.** A `design-argued`,
`design-structural`, `realization` or `contradicted` row is never merged or silently defaulted
here, and the "(course default)" label never moves. But an Option the learner **cannot take in
this lab** is not presented as a choice. Untakeable means: it needs a credential or account the
runtime file says the lab does not supply and the spec may never ask for; or it makes the offline
suite — the completion gate — wait on a person. Two cases:

- **Some alternatives remain takeable:** the untakeable Option leaves the Options cell; its
  substance stays in the Trade-off cell as narrative, and §1 Not Included carries it as
  `unavailable`, naming the seam a standalone build would use to restore it. Never tag that §1
  item `owned-by-row`: the row no longer offers it.
- **No alternative remains takeable:** the row is not asked. Its Default and Invariant are
  pinned in §2 (or in the owning rule) with the course's provenance; the alternative goes to
  §1 Not Included as `unavailable` with the seam stated; and the Environment Resolutions table
  (ADD 1) gets one extra row for it, resolution **ANSWERED — every alternative unavailable
  here**, so the removal is visible rather than implied.

The standalone takeaway is unaffected: there the same Option stays in its cell, because the
learner can obtain the credential. (Left unstated, this paragraph's first version — "mark the
Option in its cell, never delete it" — produced a gate question whose only second answer needed
an Atlassian token the lab does not have.)

**Resolving a dimension fixes what is built, never which course-argued choices the learner is
asked.** No course-owned row is retired by the resolution of a learner dimension; a row that
such a resolution makes moot is still presented, answered, and recorded in the
resolved-decisions checklist. (A row that leaves because every one of its *own* alternatives
is untakeable here is the separate case above, and it leaves through the table, not silently.) A **lever attached to
a CONSTRAINED dimension** — a trade-off the course argued about the resolved subject (a model
tiering, a provider feature) — becomes a body lever with a §6 Ask-First entry; it does not vanish
with the row. (Left unstated, one lab-mode generation surfaced half the course-owned rows its
standalone twin did.)

---

## OVERRIDE 3 — §6, the title line

Base guide `11b3673` §6's section template opens, verbatim:

> # Spec: <Project> — Standalone Takeaway

**Replaced by:** `# Spec: <Project> — Coding-Agent-Lab Build`. Nobody takes this spec away:
the lab fixes the assignment and the learner builds it there. Everything else in the §6
template stands.

---

## OVERRIDE 4 — §6, the gate template's verbatim rule

Base guide `11b3673` §6's anatomy note reads, verbatim:

> the §6.0 template verbatim (fill in this course's specifics).

**Replaced by:** emit the §6.0 template verbatim, then **append** — under the express-lane
question step and under the one-question-per-row step (the template's steps 2 and 3 as it
stands; identify them by their content, never by number) — one short italic paragraph each, labelled
`[environment]`, stating the `choices`-fence facts the runtime file requires the spec to say
(click and typed answers are equivalent; only the latest message's buttons stay live, so a
changed answer is re-asked as a new question). Nothing else in the template is added, removed,
or reworded; the appended paragraphs are the only sanctioned environment text inside §0.

---

## ADD 1 — the Environment Resolutions table (spec section)

Emit this table into the generated spec **immediately below the Decision Ledger**, before §1.
Lead it with one sentence naming the environment and stating that the rows below were derived
and then resolved, not skipped.

| Dimension | Resolution | Where the Invariant lives now |
|---|---|---|
| project | **ANSWERED** — the lab fixes the assignment | spec §1 Objective |
| data/inputs | **ANSWERED** — inputs are seeded into the workspace | spec §5 fixture corpus |
| goal | **ANSWERED** — the lab fixes what "working" means | spec §1 + the acceptance criteria |
| model/provider | **CONSTRAINED or KEPT** — decide by the test below | spec §2 (+ CTX-D), or a Ledger row |
| environment | **ANSWERED** — the container | spec §2 + the Runtime (lab) section (ADD 5); capability invariants move to the rules, or the rows, that need them |
| scope-boundary | **KEPT** | stays a Ledger row |

**The model/provider row resolves conditionally — do not assume CONSTRAINED.** This environment
fixes the model *the coding agent itself* runs on, and supplies ambient LLM credentials to the
built app. It fixes **nothing** about models the course's own pipeline uses. So apply this test:

- **Does the built app need an LLM?** → **CONSTRAINED.** Platform models only; keys and base URLs
  read from the environment; never ask the learner for one. The row leaves the Ledger and the
  constraint becomes a business rule with ≥1 AC.
- **Does the course's pipeline need no LLM at all?** → the dimension is about the course's *own*
  models — embedding, speech, vision — which this environment does not fix. It stays **KEPT** as
  an ordinary Ledger row with its course-derived default, *plus* a business rule stating that the
  ambient provider keys are present and must not be read.

Getting this wrong deletes a legitimate learner decision: a course whose models are local
encoders has a real choice here, with a real invariant and a real switching cost (changing one
means re-embedding every stored item).

**The acceptance-suite model row is course-owned and stays.** Base §3's "when the model itself
is the keyed dependency" row (which model the *offline acceptance suite* runs against) is a
`realization` row, not the learner's model/provider dimension; CONSTRAINED resolves the latter
only. The row stays in the Ledger with its scripted stand-in Default; its live Option notes that
the lab supplies the key, so choosing it costs no setup here.

**The platform's model set is not enumerated** in the runtime file, because it changes. The spec
declares one environment variable per model role (names of its choosing, listed in §2) and says
the build agent sets them **when it writes the resolved-decisions checklist** (base §6.0's last
step): the base template's step-5 model line names one current platform model per role,
chosen by the agent when it writes the checklist, and the learner's confirmation of the checklist
confirms them — no new gate question is added (OVERRIDE 4 governs §0), and model currency is the
agent's checklist-time choice, as in base §6.0. The spec never
instructs probing a listing endpoint, never asks the learner for a key, carries the course's
own model ids as provenance only, and never asserts that a course model id is served by the
proxy. **Key variables:** §2 names all four the runtime file lists and says which pair the app
reads (the course's provider's); the other pair is named as present and unread.

The generated spec must also carry a short *"Adapting this beyond the lab"* note in §1, naming
where each ANSWERED or CONSTRAINED dimension now lives, so a reader taking the spec elsewhere
knows what to change.

---

## ADD 2 — a fourth provenance label (extends base §9)

- **Environment-imposed** — `[environment]`. A fact or constraint contributed by this overlay,
  never by the course. Requires this mode. It must never also carry a *course-demonstrated*
  label, and CTX-E must carry one row attributing these facts to the environment rather than
  to any lesson.
- **Course-demonstrated, reinforced `[environment]`** — the one sanctioned co-label, for a
  constraint the course demonstrates *and* the environment independently requires (e.g. release
  one model before loading the next: shown by the course's own helper for a memory reason, and
  required by the container's shared memory). Write it as one rule with both citations, never as
  two near-duplicate rules. The ban above is on claiming course provenance for an
  environment-only fact, not on recording that both sources require the same thing.

---

## ADD 3 — checklist items (extends base §14)

Run the base §14 checklist in full, then these:

- [ ] The Environment Resolutions table is present and accounts for **all six** dimensions.
- [ ] Every ANSWERED or CONSTRAINED dimension's Invariant is exercised by ≥1 acceptance
      criterion at its new home, or the table states why it cannot be, or the table says
      "Invariant empty" — a dimension whose derived Invariant is empty (base §3: typically
      project, data, goal, scope-boundary) owes no AC, and that entry discharges it.
- [ ] No course-owned row left the Ledger except through the Environment Resolutions table (every
      alternative untakeable here, pin and `unavailable` entry in place); an untakeable Option
      beside takeable ones has left its cell for the Trade-off narrative and §1; no §1 item tagged
      `owned-by-row` points at a row that no longer offers it (OVERRIDE 2).
- [ ] Every constraint traceable to this overlay carries `[environment]`, and none is labelled
      course-demonstrated.
- [ ] CTX-E carries an environment row separate from the lesson rows.
- [ ] The provenance header pins **both** the base guide's commit and this overlay's. The base
      commit is the one named in this file's "Written against" line; the overlay's own commit is
      obtained with `git log -1 --format=%h -- <path to this file>` from the repo root — or, in
      a clean-room run where git is forbidden, taken as supplied by the invoking prompt — this
      file cannot carry its own hash.
- [ ] §1 carries the "Adapting this beyond the lab" note.
- [ ] The `## Runtime (lab)` section is present where ADD 5 places it, and every environment
      failure mode lives there, none in CTX-A/CTX-B (OVERRIDE 1, ADD 5).
- [ ] A row a resolution made moot is still presented and recorded; every lever attached to a
      CONSTRAINED dimension is a body lever with an Ask-First entry (OVERRIDE 2).
- [ ] The §0 gate's template text is verbatim; the only additions are the `[environment]`
      paragraphs OVERRIDE 4 sanctions.
- [ ] The key and base-URL variables the spec reads are exactly the ones the runtime file names;
      none is hardcoded, asked for, or guessed.
- [ ] Where a course pin and a preinstalled copy conflict, §2 says the course pin wins inside
      the venv (runtime: the container).

**Where base §14's learner-row items apply in this mode.** Two of its lines assume six rows exist
— *"learner-context rows carry only the pattern's §3 capability requirements"* and *"every
non-empty row Invariant is exercised by ≥1 AC"*. With dimensions resolved, read them against the
**Environment Resolutions table** instead: an ANSWERED or CONSTRAINED dimension discharges both
obligations at its **named home**, and a KEPT dimension discharges them as an ordinary Ledger
row. Neither line is waived; only its target moves.

---

## ADD 4 — the deliverable's shape

The base guide never says what artifact a build produces, because in standalone mode the
learner's project decides. In this mode the environment decides: the lab's default artifact is
**one server on port 4000 serving both a page and its API**, because the preview pane is the
learner's only view of the running app. The course's own artifact — a notebook, a script, a
CLI — is never the deliverable, even when the course shipped nothing else; the spec's §1
Objective describes the served app that embodies the course's pattern.

**Escape:** a course whose pattern has no user-facing surface may deliver a library plus its
test suite instead, and §1 must say so with the reason. Either way, the shape is `[environment]`
provenance and is stated in §1, not inferred by each run from the runtime facts.

---

## ADD 5 — the "Runtime (lab)" section (spec section)

The generated spec carries a section titled **`## Runtime (lab)`**, placed **between §7 and the
Course Context Pack**. Everything in it is `[environment]`. It holds: the facts of the container
the build must obey (preinstalled set, venv rule, memory), the preview rules (one server on
port 4000, relative URLs, HTTP only), the workspace rules (the workspace is the record; the
workspace-root `AGENTS.md` is never authored), and **environment failure modes** — the pitfalls
the environment, not the course, creates (a root-absolute URL under the proxied preview). An
environment failure mode is written here with its enforcing rule and criterion, exactly as a
CTX-B entry would be, but it **never appears in CTX-A or CTX-B**, which are the course's.
ADD 1's environment row points at this section.

---

## OUT OF SCOPE

`environments/coding-agent-lab.md` §§1, 2, 3, 7, 8, 10, 11 and 12 describe **lab packaging** —
the instruction artifact (`instructions.md`, `rubric.json`, `resources.json`), the workspace zip
and its step specs, grading, pitfalls for lab authors, and how to test a packaged lab.

**This pipeline's deliverable is the app spec, not the lab package.** Do not read those sections
as instructions and do not add their artifacts to the generated spec. In particular, that
document's §10 ("What a lab spec must decide") is a checklist for *packaging a lab*; the base
guide's §6 section template governs what this spec contains, and it wins.

If a future change makes this pipeline responsible for the lab package too, that is a different
deliverable and needs its own guide — not an extension of this one.
