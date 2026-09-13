# Spec Generation Guide — `coding-agent-lab` overlay

**Applies only when `/generate-spec` is invoked with `--env=coding-agent-lab`.** Without that
flag this file is not read and the base guide governs alone.

Source of the facts below: `environments/coding-agent-lab.md` §4, §5.1, §6, §9.
Written against base guide **`8e44ecb`**.

---

## How to read this file

Read the base guide first, in full:
`.claude/skills/generate-spec/references/spec-generation-guide.md`. Then read this file.

**Precedence**

1. Where this file quotes a base passage under **OVERRIDE**, this file wins.
2. **Everywhere else the base guide wins** — including any tension this file did not anticipate.
3. An unanticipated conflict is **never resolved silently.** Follow the base rule, finish the
   spec, and report the tension to the user as an *overlay gap*. It gets fixed in this file,
   not judged at generation time. (This rule exists because the first lab-targeted spec was
   produced by exactly such silent judgments, and none of them was recoverable afterwards.)

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

Base guide `8e44ecb` §3 reads, verbatim:

> Generation is gated on **two inputs**. Verify each is actually present before generating.

**Replaced by:** generation is gated on **two required inputs plus this overlay**. The notebook
dump and transcripts remain required and remain the *only* course evidence. This overlay is a
third input describing the build target.

This overlay is **never course evidence.** Nothing traceable to it may carry a
*course-demonstrated* label, appear in CTX-A or CTX-B, or be attributed to the course in any
way. It gets its own label (see ADD 2) and its own row in CTX-E.

---

## OVERRIDE 2 — §5.5, procedure step (f)

Base guide `8e44ecb` §5.5 **Procedure** reads, verbatim:

> (f) add the six §3 learner-context rows, each Invariant holding only the pattern's capability requirements on that dimension (empty when none) — learner rows still get a course-derived default (e.g. project defaults to the §3 example-shape target);

**Replaced by a two-phase step. Both phases are mandatory and their order is load-bearing.**

**Phase 1 — derive all six, exactly as the base guide requires.** Project, data/inputs, goal,
model/provider, environment, scope-boundary. Each gets its Invariant (the pattern's capability
requirements on that dimension, empty when the pattern demands nothing) and its course-derived
default. **Do this before reading the RUNTIME FACTS section of this file.** A dimension you have
not written down cannot be resolved, and an unresolved dimension disappears without trace — that
is the exact failure this ordering prevents.

**Phase 2 — resolve each of the six** against the Resolutions below, and emit the resolution
table into the spec (ADD 1). A dimension is resolved in one of three ways:

- **ANSWERED** — the lab fixes it. The row leaves the Ledger, and **its Invariant must land
  somewhere named**: a spec section, a business rule, or another Ledger row's Invariant. An
  ANSWERED dimension whose Invariant goes nowhere is a defect, not a simplification.
- **CONSTRAINED** — the lab narrows it without fixing it. The row leaves the Ledger and the
  constraint becomes a business rule or a §2 entry, with at least one acceptance criterion.
- **KEPT** — the lab has no opinion. The row stays in the Ledger exactly as the base guide
  derived it.

**Course-owned rows are untouched by this mode.** A `design-argued`, `design-structural`,
`realization` or `contradicted` row is never removed, merged or silently defaulted here. Where
the environment makes one of its Options impractical, mark that Option in its own cell with the
reason — never delete it, and never move the "(course default)" label.

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
| model/provider | **CONSTRAINED** — see RUNTIME FACTS | spec §2 (+ CTX-D) |
| environment | **ANSWERED** — the container | spec §2 + the Runtime section; capability invariants move to the rows that need them |
| scope-boundary | **KEPT** | stays a Ledger row |

The generated spec must also carry a short *"Adapting this beyond the lab"* note in §1, naming
where each ANSWERED or CONSTRAINED dimension now lives, so a reader taking the spec elsewhere
knows what to change.

---

## ADD 2 — a fourth provenance label (extends base §9)

- **Environment-imposed** — `[environment]`. A fact or constraint contributed by this overlay,
  never by the course. Requires this mode. It must never also carry a *course-demonstrated*
  label, and CTX-E must carry one row attributing these facts to the environment rather than
  to any lesson.

---

## ADD 3 — checklist items (extends base §14)

Run the base §14 checklist in full, then these:

- [ ] The Environment Resolutions table is present and accounts for **all six** dimensions.
- [ ] Every ANSWERED or CONSTRAINED dimension's Invariant is exercised by ≥1 acceptance
      criterion at its new home, or the table states why it cannot be.
- [ ] No course-owned row was removed by this mode; an Option the environment makes impractical
      is marked in its own cell, not deleted.
- [ ] Every constraint traceable to this overlay carries `[environment]`, and none is labelled
      course-demonstrated.
- [ ] CTX-E carries an environment row separate from the lesson rows.
- [ ] The provenance header pins **both** the base guide's commit and this overlay's.
- [ ] §1 carries the "Adapting this beyond the lab" note.

---

## RUNTIME FACTS

**Do not read this section until Phase 1 of OVERRIDE 2 is complete** — all six dimensions
derived and written down.

Distilled from `environments/coding-agent-lab.md`. Everything here is `[environment]`.

### The question mechanism — feeds base §6.0 unchanged

Base §6.0 already requires a structured question tool "if you have one". This environment has
one, so **this is an input to that rule, not an override of it.** The mechanism is a fenced
` ```choices ` block:

- Explanation in prose *above* the fence; the fence is **last** in the message; one option per
  line; the turn ends there.
- A line `**Question N of M — <decision>**` before the fence renders a question box. Use it, so
  learner and agent can both see nothing was skipped.
- A click sends the option line verbatim; a typed answer naming an option counts identically.
  The generated spec must say so.
- Only the **latest** assistant message's buttons stay live. A spec must never ask anyone to go
  back and change an earlier answer — re-ask as a new question.
- Never put a `choices` fence inside the spec's own examples in a way that implies the learner
  brief carries one; the fence is parsed only in assistant chat messages.

### The container — feeds spec §2

Debian, non-root user, Node 22, Python 3 with venv, sqlite3, git, build tooling.
**Preinstalled:** `fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`; Node `express`,
`cors`, `better-sqlite3`, `vite`, `nodemon`. **Nothing else** — no vector stores, no embedding
models, no ML frameworks.

Outbound network works, so installs and one-time model downloads succeed, but each costs the
learner wall-clock time inside the session. A spec whose stack needs anything beyond the
preinstalled set must say so in §2 and tell the build agent to batch the install early and
announce its cost. Create venvs with `--system-site-packages` so the preinstalled stack is
reusable.

Memory is finite and shared with the agent's own process. A spec whose pipeline can hold several
models resident at once must carry a business rule releasing one before loading the next.

### Model / provider — the CONSTRAINED resolution

The learner picks the *agent's* model per conversation from the platform's set; a spec must work
across all of them, or say in its own text which it assumes. **Never bake a "current best" model
name into the spec** — base §6.0's gate-time "(Recommended)" flag already owns model currency.

The container exports provider API keys and their base URLs. If the built app needs an LLM, the
spec says: read keys and base URLs from the environment, use a platform model, **never ask the
learner for a key**. If the course's pipeline needs no LLM, the spec says that plainly and adds
a rule that the ambient keys are not to be read.

### The app preview — feeds spec §4 business rules

- **One server, port 4000, bound to `0.0.0.0`**, serving both the page and the API. Nothing
  else is previewable.
- **Every URL inside the page must be relative** (`api/thing`, never `/api/thing`). The preview
  is reverse-proxied under a path prefix, so a root-absolute path resolves against the IDE.
  This is the single most common way a working app appears broken; it belongs in the spec as a
  numbered business rule with an acceptance criterion, not as a note.
- HTTP only — WebSocket upgrades are not proxied. Streaming responses work.

### The workspace — feeds spec §6 permissions

- **The workspace is the record.** A new chat starts with no memory of an earlier one, and the
  grader sees only what is on disk. Decisions, resolved values and results must be written to
  files, not left in chat. Base §6.0 already requires `resolved-decisions.md`; state *why* it is
  load-bearing here.
- **Never author `AGENTS.md`** in the workspace — the IDE rewrites it at every boot, so guidance
  placed there is silently lost. This belongs in the spec's **Never** tier.
- Every tool call is visible to the learner, and long-running servers run in the background.

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
