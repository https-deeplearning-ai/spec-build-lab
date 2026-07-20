# Spec Generation Guide

**Self-contained, prescriptive guide for generating a learner's takeaway `spec.md` from course materials.** Feed *this guide + the course's concatenated notebook dump + the concatenated transcripts* to a capable model, and it produces the spec. Nothing else is required — the framing, the inputs, the generation procedure, the deterministic output format, and the self-check are all here. **Learner intake is not a generation input**: one `spec.md` is generated for many learners, so intake can't be collected here. Each learner-specific value is emitted as a `[slot]` carrying a course-derived default, and the learner substitutes their own at *build* time.

This guide stands in for three things at once: the **product framing** for the takeaway feature, the **"reusable context package, not snippet reassembly"** idea, and the **spec-quality standard**. Where it says MUST, it is not a preference.

## Contents
1. The framing — what you're making, and why
2. The spec-quality bar — right altitude
3. Inputs & the ground-truth rule
4. Procedure A — mine the materials (two passes)
5. Procedure B — derive the build (incl. §5.5 Derive the Decision Ledger)
6. Required section template (Decision Ledger + §1–§7 + Course Context Pack)
7. The Course Context Pack (CTX-A…CTX-E)
8. Contracts & acceptance-criteria format
9. Provenance labels
10. The four-way failure encoding (+ worked example)
11. Anti-patterns to avoid
12. Known traps
13. The Regeneration Test
14. Pre-handoff checklist

---

## 1. The framing — what you're making, and why

Read this once; it drives a hundred small judgment calls.

**The problem.** Learners finish a course with an invisible bump in knowledge and a certificate, but no path from what they learned into their own, messier projects — practice tasks feel too simple to reuse on real work, and unapplied knowledge is quickly forgotten. The takeaway spec bridges that transfer gap.

**The trap to avoid.** The naive takeaway staples together code snippets from the course notebooks — some already stale the day the course ships. That produces a brittle reassembly, not a transferable asset. Avoiding this is the entire point.

**The synthesis (why the output is shaped the way it is).** The spec is two things at once:
- A **build brief** — *"what should be built?"* — objective, contracts, constraints, acceptance criteria for the learner's project.
- An embedded **reusable context package** — *"what does an agent need to know to apply this course's pattern correctly?"* — the pattern, working parameters, gotchas, assumptions, expressed as durable concepts rather than copied cells.

The spec is **both**: a normal spec body (§1–§7) plus an embedded, agent-readable **Course Context Pack** (§7 below). The body says what to build; the Context Pack means the building agent applies the course's pattern correctly instead of falling back on model memory, noisy web search, or stale recall. This is why the deliverable is a single self-contained file — the course knowledge travels *inside* the spec.

**The positioning — spec-guided building, not spec-driven development.** Claims that specs guarantee better velocity or product quality are conditional and contested; do not inherit them. The learner's final build can't be evaluated from our side and varies per learner. So the value is **better guidance at the moment of application**, not a guaranteed product. Tune every choice toward learner guidance and correct transfer.

**Audience.** A working software engineer applying the course to a real project. Write for *their agent*: precise, outcome-oriented, no hand-holding on basics — and no assumed access to anything outside the delivered file.

---

## 2. The spec-quality bar — right altitude

Specify **outcomes, contracts, and constraints; leave implementation to the agent.** Two failure modes bound the target:
- **Underspecify** → the agent fills gaps with statistically plausible guesses that break at integration. Every omitted constraint becomes a hallucinated assumption.
- **Overspecify** (pseudo-code, class hierarchies, "use a HashMap") → you've hand-written the code and locked the agent out of a better, codebase-consistent solution.

Aim for the smallest set of high-signal instructions that pin the behavior. The spec says **what** and **why**, never **how** — point to outcomes and acceptance tests, not code structure. If a sentence describes how the code is organized, it's in the wrong document.

**Load-bearing sections (★).** Three sections prevent the most failures; never ship without them: an explicit **"Not Included"** boundary (§1), **Input/Output Contracts as schemas** (§3), and **Acceptance Criteria with concrete in→out cases** (§5). They are the spec's oracle.

---

## 3. Inputs & the ground-truth rule

Generation is gated on **two inputs**. Verify each is actually present before generating.

1. **Notebook dump** (required) — notebooks concatenated to Markdown, cell by cell. Source of truth for **parameters, API surface, prompts, configs**.
2. **Transcripts** (required) — lesson transcripts. Source of truth for **lesson numbering and titles, rationale, spoken trade-offs, failure narration**.

**Learner intake is a build-time input, not a generation input.** One `spec.md` is generated and delivered to many learners; the learner supplies their own project when they build. So the generator **never has intake, must not ask for it, and must not block on it**. Instead, every point where a build could diverge — including the learner-context dimensions — becomes a **Decision Ledger** row (§5.5), each carrying a course-derived default. Specifically:
- The learner-context dimensions are Ledger rows whose Invariant carries only the pattern's *capability requirements* on that dimension — empty when the pattern demands nothing (typically project, data, goal, out-of-scope), a small capability contract when it does (e.g. Model/provider: *must support native tool calling*; Environment: *memory must survive process restarts*), always derived from the materials, never invented. The course has no opinion on the learner's *selection*, only on what the selection must be capable of. The dimensions: *Project* (what they're building); *Data/inputs* (what it operates on, where that lives); *Goal* (what "working" means — what retrieval should find, what the output must guarantee); *Model/provider* preference; *Environment* (where it runs, constraints); *Out of scope* (anything explicitly unwanted). These are marked `[bracketed]` in the spec body (§9 labels them *learner intake*).
- **Every Ledger row — learner-context or otherwise — MUST carry a course-derived default** so the spec is buildable and evaluatable *as-is*, with zero intake.
- The default MUST be **self-contained inside `spec.md`** — resolvable at build time without reading anything else. During a build, course `materials/` are off-limits (hook-enforced), so a default that points back at the course cannot be resolved. Bake it in.

### The deterministic default (the fallback that fixes inconsistent builds)

A build-from-spec run with **no intake MUST resolve to exactly one target, every time** — the generator decides it, not the building agent. This applies to **every Decision Ledger row** (§5.5), not just the project: each row names exactly one buildable default. Never leave a default ambiguous between "the course's own example" and "some agnostic project", and **never emit a contract or a menu in place of a default** — "any store meeting the invariant" or "e.g. X / Y / Z" is not a default; it is the ambiguity that makes builds diverge run to run (§12.8).

**For the *project* row**, resolve the default with this precedence:

1. **Prefer the course's example scenario shape** — when the materials clearly afford a concrete example, re-express *its shape* on the self-contained synthetic fixture corpus (§5). Recognizably the course's example, but with facts *you* author (no course data copied — §11, §12.6).
2. **Else, a generic minimal instantiation** — when the course has no clean toy example, default to the smallest domain-neutral instantiation of the central pattern (§5), still on the synthetic fixture corpus.

**For a *technique* or *dependency* row whose course realization is a heavy dependency** (a cloud DB, a hosted service, a keyed API, a GPU-class model — anything that cannot be baked into `spec.md` and run without external setup), resolve with this precedence.

**The heavy bar, precisely:** a realization is heavy only if it needs a credential/key, a paid account, admin- or container-level setup, or special hardware. **Mere network access is NOT heavy** — a keyless, setup-free public API stays the default; mark the acceptance criteria that need it `live` (excluded from the offline run) so the fixture-based acceptance tests still run on day one. Fixtures substitute for *data*; they do not displace the course's own *tools*. (Left unstated, this bar made two generations of the same course resolve the same row differently — one kept the course's keyless API tools, the other substituted local stand-ins.)

1. **Substitute the lightest self-contained realization that preserves the row's invariant** — e.g. an embedded local store standing in for a cloud vector DB, when the course teaches a *pattern* that the dependency merely happens to realize. The course's actual technology is still listed among the row's **Options**, never erased.
2. **UNLESS the specific technology *is* the taught subject** — a course *about* that exact product (e.g. "Building on Oracle Vector Search") — in which case reproduce it as the default, with baked-in setup instructions, and note the setup cost.

Either way — project, technique, or dependency — name **one** buildable target and **state which precedence branch you took, and why, in the row's default note.** (This is the branch that, left unstated, made two generations of the same course diverge: one substituted a local store, the other emitted a menu.)

**Ground-truth rule (hard gate).** Only the supplied materials count as course evidence. If you recognize the course from training, that memory is **not** a citable source — courses get refreshed, and recalled lesson numbers, parameters, and library versions are confidently wrong in exactly the ways that matter here. Anything you cannot point to in the supplied files is dropped or relabeled as your own addition (§9). **No files, no generation.**

---

## 4. Procedure A — mine the materials (two passes; neither substitutes for the other)

Notebooks give you *what and how-configured*; transcripts give you *why and what-it-trades-off*. Mine both.

**Pass A — Notebooks.** Extract:
- Every working parameter (chunk sizes, overlaps, k-values, temperatures, paths) **with its exact location**, distinguishing exploratory-notebook configs from the course's end-to-end *application* config. When both exist, the app config is the recommended starting point; record the rest as alternatives with their context. Never call a value "the default" if the materials contain more than one config.
- The API surface actually used: namespaces, class/function names, model names — and whether installs are **version-pinned**. State the era honestly (e.g. "installs unpinned, pre-1.0 namespace"). Never invent pins the notebook doesn't contain.
- Deliberately planted failure demonstrations (a duplicated input file, a query designed to fail) — these are curriculum, not accidents → they become rules.
- Behavior-encoding prompts (e.g. a grounding instruction like "if you don't know, say you don't know") → become business rules, expressed as the *behavior*, not the prompt text.

**Pass B — Transcripts.** Extract:
- **Lesson numbering and titles exactly as the transcripts state them.** Platform numbering frequently differs from notebook filenames (e.g. an "Introduction" counted as Lesson 1 shifts everything by one). Transcripts win; the CTX-E provenance map uses their numbering.
- The *why*: rationale, analogies, intuition (why overlap exists; why a failure happens mechanistically).
- **Trade-offs spoken aloud that never appear in code** (e.g. "this method ran slower *and* answered worse here"). These become Ask-First boundaries.
- Instructor heuristics and parameter guidance (e.g. how results degrade as k grows).

Keep a scratch **provenance ledger**: each extracted fact → where it came from (file, lesson/cell). You won't ship it; §14's audit depends on it.

---

## 5. Procedure B — derive the build

1. **Name the course's central buildable pattern** as one pipeline (e.g. `load → split → embed+store → retrieve → generate → converse`), with a one-line reason each stage exists.
2. **Derive the Decision Ledger from the pattern** (§5.5), and instantiate the pattern on each row's default (§3). Because the generator has no learner intake, build the spec's skeleton on the deterministic defaults — the pattern instantiated with the default project, data, goal, and model choices (on the synthetic fixture corpus), the course's pitfalls to avoid, and the course's API assumptions. The Ledger *is* the spec's skeleton: it names every point where the build could diverge, each pinned to one default a learner may swap. (This is the difference between "here are some course snippets" and "use pattern A; data is B (default: fixture corpus); retrieval goal C; embedding D; chunking must consider E; avoid mistakes F/G/H; here are the course's API assumptions" — buildable as-is, with the Ledger's rows a learner can swap.)
3. **Convert every demonstrated failure mode into a numbered business rule, and every rule into ≥1 acceptance criterion.** A failure mode without a rule is wasted curriculum; a rule without an AC is unverifiable.
4. **Design a fixture corpus**: small synthetic inputs whose facts *you* author, including one deliberate instance of *each* demonstrated failure mode, so the acceptance criteria run on day one before the learner wires in real data.
5. **Decide the stack**: pin modern versions as *this build's* choice; record course-era API names separately as perishable search keywords (CTX-D). Carry the pattern forward, not the era's call signatures.

### 5.5 Derive the Decision Ledger

The **Decision Ledger** is the spec's second section (§6, right after the §0 pre-build gate) and its skeleton: every point where a build could legitimately diverge, each pinned to exactly one default. It replaces the old fixed "learner-intake slots" list — those six dimensions are still present, but as *rows*, not as the whole structure. The Ledger's shape is course-independent; its rows are course-specific, derived from the pattern (step 1).

**A decision is not "learner" *or* "course".** Every design-critical decision has two roles at once: the **course** owns the *invariant* (what must stay true for the build to still embody the taught pattern) and a *course-derived default* (factual provenance — what the course did — not advice about the learner's project); the **learner** owns the *selection* among realizations that satisfy the invariant. "Should the store be online (a cloud DB) or offline (a local equivalent)?" is the canonical example — the course fixes the invariant ("a semantic-similarity store AND an exact-key store must both exist") and defaults to one; the learner picks the realization. So the Ledger does not sort decisions into "learner" vs "course" buckets; it records **who owns the answer** as a label (§9), which never changes how the row behaves.

**Each row carries seven fields:**
- **Category** — the §5.5 entry route that admitted the row (`design-argued | design-structural | realization | contradicted | learner`). Exactly one label, chosen by the precedence in the surfacing bar below; it determines the row's position in the fixed row order.
- **Decision** — short name (e.g. "persistent store", "memory-core topology", "project").
- **Invariant** — what MUST hold to preserve the taught pattern. For learner-context rows it carries only the pattern's capability requirements on that dimension (§3) — typically empty for project/data/goal/out-of-scope, never invented. Write it precisely: this field doubles as the contract a future integration must satisfy.
- **Options** — realizations that satisfy the invariant, from course-faithful to tech-agnostic. The course's own technology always appears here even when it is not the default — and when it is not the default (a §3 branch-1 substitution), tag that entry **"(course default)"** in the cell text, so the §6.0 gate's labeling duty is deterministic: the build agent must never have to infer which option the course actually used.
- **Default (course-derived)** — **exactly one** buildable target (§3). For heavy-dependency rows, resolved by the §3 dependency precedence, with the branch stated. When the default is the course's *example realization* — a domain-specific instantiation (its demo data, its example tools) rather than the pattern itself — the Decision or Default cell must say so and mark it as expected to be swapped when the learner's project (the project row) differs: the invariant, not the example, is what must survive.
- **Trade-off** — what switching costs (carries the course's *spoken* trade-offs: re-embedding, re-tuning, lateral-or-worse results).
- **Owner** — a label only: `learner`, `course`, or `course+learner` (§9). Metadata; never gates behavior.

**No cross-row restating.** A row's Default or Invariant must never restate another row's decided value (a `k`, a distance strategy) — cross-reference the owning row instead ("k: pinned in row N"). A restated value makes two rows read as the same question when the §0 gate presents them one at a time, and the copies drift when one row changes.

**Procedure:** (a) walk each stage of the pattern (step 1); (b) list its decision points; (c) sweep Pass B's mined trade-offs for course-argued decisions that are not tied to a single stage (e.g. an architecture-maturity progression or a taxonomy the course argues through); (d) for each surfaced decision (see the bar below) write the seven fields; (e) apply the §3 dependency precedence for any heavy-dependency row; (f) add the six §3 learner-context rows, each Invariant holding only the pattern's capability requirements on that dimension (empty when none) — learner rows still get a course-derived default (e.g. project defaults to the §3 example-shape target); (g) assign each row's Category and sort the table into the fixed row order (see the bar below).

**Surfacing bar — which decisions become Ledger rows.** Five entry routes admit a decision; every row records the route that admitted it in its **Category** field:

- **`design-structural`** (pattern-structural) — choosing differently changes the system's *structure or semantics*: a pipeline stage added/removed/reordered, ownership moved between harness and model, a guarantee changed (reversibility, consistency), the data model or an interface reshaped. Litmus test: *redraw the architecture diagram after the change — did a box, arrow, owner, or guarantee change, or only a number inside a box?* Examples: store topology, the deterministic-vs-agent-triggered operation split, recoverable-compaction vs lossy-summarization. Counter-example: a retrieval `k` is load-bearing — set it absurdly and the pattern degrades — but no box, arrow, or guarantee changes; **sensitivity alone does NOT qualify** (such a value stays a body default unless another route admits it).
- **`design-argued`** (course-argued) — the transcripts/slides explicitly present an alternative and argue a trade-off ("you could do X, but we do Y because Z"). Detection source: Pass B's mined spoken trade-offs (§4) — what the instructor argued about is what the course teaches *as a decision*. This route applies **even when the course's choice would otherwise be encoded as an invariant**: weaken the Invariant field to what must truly hold, make the argued position the Default, and carry the course's narrated argument — with its lesson citation — in the Trade-off cell. The default is always the course's argued position, so no-intake determinism (§3, §12.7/§12.8) is unaffected.
- **`contradicted`** (course-contradicted) — the course itself set it inconsistently across lessons or between signature/docstring/call site (e.g. cosine in one lesson, euclidean in another; `k=3` in a signature but `5` in the call). Self-contradiction is the strongest signal a human should see the choice, even if the stakes look low.
- **`realization`** — a heavy-dependency decision surfaced by the §3 dependency precedence (the row states which branch was taken and why).
- **`learner`** — the learner-context dimensions (§3): project, data/inputs, goal, model/provider, environment, out-of-scope.

When several routes apply, Category records the highest-precedence one: `design-argued > design-structural > realization > contradicted` (learner-context rows are always `learner`). Lower-precedence evidence is never dropped: if a design row's value is also course-contradicted, the contradiction — with both citations — still appears in that row's Default note or Trade-off cell.

Everything else — a single-valued parameter the course sets once, never varies, and never argues (a chunk size, a token-estimate heuristic, a max-iteration cap) — stays a **defaulted value in the spec body**, not a Ledger row. It still carries its value and provenance; it is simply not promoted. Do not drown the Ledger in low-stakes rows; do not bury a design or contradicted decision in prose (that is the failure §12.9 and the old CTX-C mis-home caused).

**Row order (fixed).** The table is grouped by Category — **`learner` → design (`design-argued`, `design-structural`) → `realization` → `contradicted`** — with pattern-pipeline order within each group. This is presentation order only (the derivation procedure may construct rows in any sequence). The ordering principle is **context first, dependents after**: the §0 gate presents rows in table order, so the learner's project/data/goal answers exist in the conversation before the design and realization rows whose right answer for *this* learner depends on them (a store choice depends on the environment; a toolset on the project; seed data on the learner's data), and the build agent can frame those later questions in the learner's own terms (§6.0). Contradicted rows come last because they depend on realization choices (an index type depends on the chosen store). Ordering by importance instead ("highest-judgment first") buys nothing here — the gate hard-requires every row answered and checklist-echoed, so coverage never depends on position; position should buy context.

---

## 6. Required section template (§1–§7 + Course Context Pack)

The spec MUST contain these core sections, in this order (this is the seven-section anatomy), followed by the embedded **Course Context Pack**. Sections marked ★ are load-bearing. Use this skeleton:

```markdown
# Spec: <Project> — Standalone Takeaway
<!-- Title the default target, not a per-learner project the generator can't know:
     e.g. "<course-example-shape> chatbot" (precedence 1) or "<central-pattern> app"
     (precedence 2). A learner retitles when they fill [project]. -->

<!-- Opening blockquote MUST state: (a) the file is self-contained — the Course
     Context Pack replaces external course references; (b) (CTX-X) anchors mark
     course-derived knowledge; the Decision Ledger below holds every point where the
     build could diverge, each pinned to one course-derived default so the spec builds
     as-is with no intake; (c) provenance line: generated from <course> notebooks +
     transcripts on <date>. -->

## 0. Before you build — REQUIRED (do this first)
<!-- ALWAYS the very first section, ahead of the Decision Ledger. The pre-build gate (§6.0):
     an imperative, build-agent-addressed instruction that presents every Ledger row ONE
     QUESTION PER ROW via a structured question tool (required if the environment has one, e.g.
     AskUserQuestion; else plain-text list) — never depending on a per-call item cap — then
     HARD STOPS: write no code until every row is answered AND a resolved-decision checklist is
     printed. No "proceed if no response" escape (§12.10); no partial-present build (§12.11).
     Portable across Claude Code / claude.ai / OpenAI Codex / Cursor / a custom harness. Emit
     the §6.0 template verbatim (fill in this course's specifics). -->

## Decision Ledger (§0 above requires the build agent to present these before building)
<!-- The second section (after §0). ONE table holding every design-critical
     decision (§5.5): the learner-context dimensions (project/data/goal/out-of-scope) AND
     the design (structural/argued), realization, and contradicted technique & dependency
     decisions. This REPLACES the old fixed six-slot list. Lead with: "These are the points
     where this build could diverge. Every row has a course-derived default, so the spec is
     buildable and evaluatable as-is; change a row only when applying to a real project or
     when you have reason to prefer another option."
     Columns: | # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement, §3) | Default (course-derived) | Options | Trade-off | Owner |
     - Category is the §5.5 entry route (design-argued | design-structural | realization |
       contradicted | learner) — one label, highest precedence when several apply.
     - Rows are grouped in the fixed §5.5 row order: learner → design → realization →
       contradicted, pipeline order within each group (context first, dependents after).
     - Default names EXACTLY ONE buildable target (§3) — never a menu or "any X" (§12.8).
     - Heavy-dependency rows state which §3 precedence branch was taken and why; on a
       substitution row, the course's own technology in Options carries the literal tag
       "(course default)".
     - design-argued rows carry the course's narrated argument + lesson citation in Trade-off.
     - Owner is a label only (learner / course / course+learner, §9); it never changes behavior.
     - Unfilled rows do NOT block handoff — the defaults ARE the build target. -->

## 1. Objective
<One sentence: what it does, for whom, with what guarantee.> (pattern: CTX-A)
### Not Included            ★
<Explicit out-of-scope list: the learner's exclusions + everything past course scope.
 Without this, the agent adds plausible features nobody asked for.>

## 2. Tech Stack & Versions
<Table: component | pinned choice | note. Where a component's choice is a Decision Ledger
 row (e.g. the persistent store), the pinned choice is that row's Default, and the note
 points to the Ledger row (learners change it there, not here). Exactly one row's note MUST
 state the course's actual install/pin situation honestly and point era-specific names to
 CTX-D. Secrets handling stated here, never hardcoded.>

## 3. Input/Output Contracts            ★
<Machine-readable schema (JSON Schema, or Zod/OpenAPI) for the core I/O object —
 agents hallucinate shapes from prose, so this is NOT prose. Encode invariants in the
 schema itself (e.g. "ungrounded ⇒ zero citations" as a conditional constraint).>

## 4. Business Rules
<Numbered. Each rule = behavior + the failure it prevents (CTX-B anchor) + "→ AC#".
 Each rule tagged with a provenance label (§9). Parameter values cite their exact
 source config — never "course default" when multiple configs exist.>

## 5. Acceptance Criteria                ★  (the oracle)
<Fixture corpus defined FIRST (file names + the exact facts each contains), then a
 Given/When/Then table. Concrete inputs and asserted outputs only — no "typically".>

## 6. Boundaries
**Always** / **Ask First** / **Never**
<All three tiers populated. Ask First is mandatory and carries the course's spoken
 trade-offs: anything forcing rework (re-embedding, re-tuning) or that the course
 showed to be lateral-or-worse. Never MUST include: inventing provenance/citations;
 answering when the system should abstain; mutating fixtures to pass a test;
 committing secrets.>

## 7. Test Plan & Self-Verification
<Real, runnable commands. Then an instruction: the building agent MUST report results
 per acceptance criterion with cited evidence (test output, file paths).
 "Should pass" / "looks correct" are treated as failures — they mean it wasn't run.>

## Course Context Pack (embedded — agent-readable)
<!-- The 8th section, extending the seven-section anatomy. See §7 of THIS guide.
     Concepts only — NO code copied from the notebooks. Referenced by CTX-* anchors,
     which are position-independent: inserting optional sections never breaks them. -->
### CTX-A. The pattern
### CTX-B. Failure-mode catalog
### CTX-C. Decision background   <!-- reference for Decision Ledger rows; NOT where decisions are made (§5.5) -->
### CTX-D. Perishable assumptions
### CTX-E. Provenance map
```

End the spec with a status footer: version · course · learner project · the living-document instruction (when the building agent produces something unexpected, add the missing constraint here and re-run).

**Optional sections** — add only when the feature demands it, placed between §7 and the Course Context Pack: performance targets (measurable thresholds), migration notes (before/after + rollback), UI state definitions (loading/error/empty/partial), error-handling taxonomy, compliance constraints (PII/payments/regulated data). Because the Context Pack is referenced by name (CTX-*) not by number, adding these never breaks a cross-reference.

### 6.0 The pre-build gate (spec §0 — REQUIRED)

A Decision Ledger that no one is shown is worthless. A build agent's default behavior is *"build as-is; only stop for what blocks"* — and because every Ledger row carries a complete default, **nothing blocks, so nothing gets surfaced** and the learner never sees the decisions (the failure in §12.10). The fix is a **gate**: the generated spec's very first section (`## 0`) is an instruction to the *build* agent to present the Ledger before writing any code.

**This gate is the only portable surfacing mechanism.** The spec is delivered as a single file to an unknown environment — the learner may build with Claude Code, claude.ai, OpenAI Codex, Cursor, or a custom harness. A hook could *enforce* the gate but is not portable (Claude Code CLI only). Prose in the spec cannot *guarantee* the step, but a maximally-structured prose gate is the strongest lever that travels everywhere. Write it for that job:

- **Imperative and build-agent-addressed.** "You are the build agent. Before writing ANY code, you MUST…" — not a passive "review before build" header (which reads as a note to a human skimming and gets skipped).
- **First.** It is spec section `## 0`, ahead of everything including the Decision Ledger, visually isolated.
- **An express lane for the as-is builder, asked first.** The gate's FIRST question offers exactly two paths: build the course-default takeaway **as-is** (every Ledger row resolves to its Default), or **customize** the decisions row by row. Choosing as-is skips the per-row questions entirely — the agent prints the full resolved-decision checklist (every row = its Ledger default) and begins building; choosing customize enters the one-question-per-row loop. This is NOT an escape clause (§12.10): the user gave an explicit answer that covers every row — the same "defaults are fine" reply the determinism argument already sanctions — and the printed checklist still makes completeness visible. What stays forbidden is proceeding on *silence*.
- **Presents EVERY Ledger row.** Do not have the gate re-filter or tier rows — the §5.5 surfacing bar already decided what became a row, so every row is by construction worth showing. (Never key the gate on row numbers; row identities are course-specific.)
- **One question per row — do not depend on a channel's item cap.** Interactive question tools cap how many questions fit in one call (Claude Code's `AskUserQuestion` allows at most a few), and a Ledger can have many rows. If the gate says "present every row" without saying *how*, the agent improvises — batching inconsistently, or (worse) presenting a first batch, getting a reply, and treating the build as unblocked while the rest are never asked (§12.11). Fix the mechanism deterministically: **one row = one question**, looped until every row is asked. One-per-row has no batch boundary to mis-track and its completeness is a plain count (N rows ⇒ N questions). **Never hardcode a numeric cap** ("4") into the gate — that is one environment's limit; state the capacity-relative rule instead so it holds for an uncapped or plain-text channel too.
- **Checklist-echo gates the build, not "a reply happened".** Keying resumption on "the user replied" fails the moment many rows exist: a reply to *some* rows satisfies it, and the rest are buried. Require a **visible artifact** instead — before any code, the agent prints a checklist of every row with its resolved value. A completion-driven agent cannot produce that checklist without having resolved every row, and the user/reviewer can *see* completeness. A printed artifact beats an internal "did I ask N times?" count precisely because the same agent that skips rows is the one that would judge the count.
- **Labels the course's actual choice "(course default)"; the build agent's own "(Recommended)" flag may coexist.** "(course default)" is factual provenance — what the course actually did — and must always mark the option the course actually used. On a **substitution row** (§3 dependency-precedence branch 1) that is the course-faithful **Options** entry, NOT the substituted Ledger Default: labeling the substitute "(course default)" misattributes it (observed in real learner feedback — a SQLite+Chroma default presented as the course's choice when the course ran Oracle). Separately, the build agent may mark an option "(Recommended)" per its own judgment or its question tool's convention (Claude Code's `AskUserQuestion` suggests exactly this) — that is advice about *this* learner's project, a different claim from provenance, and it is allowed. The two labels compose: when the agent's recommended option differs from the course's choice, both labels appear, each on its own option; when the recommended option IS the course's choice, use the single combined label **"(Recommended - course default)"**. A recommendation never removes or moves the "(course default)" label.
- **A hard stop, with no escape clause.** Presenting the decisions must end the agent's turn: it stops and waits for the user's reply before writing any code or touching any file. Do **not** give it a "proceed if there's no response" release valve — that is the loophole that re-opens §12.10: the agent *always* trivially has "no response" the instant it finishes presenting, so it reads the valve as immediate permission and the ask becomes theater. A narrower "proceed if launched non-interactively" escape is the same hole, smaller — drop it too; a completion-driven agent steers into whatever escape exists. Determinism is **not** at risk from waiting: it comes from every row having one course-derived default (§3, Known-Trap #7), so a user who replies "defaults are fine" lands on the identical target. Waiting changes *when* the agent proceeds, never *what* it builds. (If a genuinely headless harness cannot answer, the absent reply stalls that build — the harness's constraint to resolve by pre-answering, not a hole the spec should pre-drill.)
- **Structured tool required when available; still portable.** If the environment has an interactive structured-question tool (Claude Code's `AskUserQuestion` or an equivalent), the gate MUST require using it — it is the reliability lever, not a mere suggestion. Name specific tools only as *examples* of the class, never as a hard dependency: a non-Claude agent (Codex, Cursor, plain chat) with no such tool must still comply by listing the rows in its reply and asking. So the rule is "use a structured question tool **if you have one**, else ask in plain text" — mechanism-*required* where possible, mechanism-*agnostic* in fallback.

Emit it using this course-independent template (fill the bracketed bits; the Ledger row list is whatever this course produced):

```markdown
## 0. Before you build — REQUIRED (do this first)

You are the build agent. Before writing ANY code, you MUST surface the design decisions
in the Decision Ledger (next section) to the person you are building for. Do **not** skip
this because the defaults look complete — the defaults exist so the build is *reproducible*,
not because they are the right choice for this person's project.

1. **Use a structured question tool if you have one.** If your environment offers an
   interactive structured-question tool (e.g. Claude Code's `AskUserQuestion`, or the equivalent
   in yours), you MUST use it for the questions below — do not paraphrase them into a prose
   paragraph. Only if no such tool exists, list the rows in your reply and ask the user to
   respond to each.
2. **First question — build as-is, or customize?** Ask exactly one question with two options:
   build the course-default takeaway **as-is** (every Ledger row resolves to its Default), or
   **customize** the decisions row by row. If the user chooses as-is, skip step 3 — go straight
   to the step-5 checklist and build. If the user chooses customize, continue with step 3.
3. **Present the Ledger ONE ROW AT A TIME — one question per row.** For each row ask a single
   question: the **Decision** as the prompt, its **Options** as the choices. Append
   "(course default)" to the option the course actually used — on a substitution row that is
   the course-faithful Options entry, not the Ledger Default. You may also mark an option
   "(Recommended)" per your own judgment or your question tool's convention; when your
   recommended option IS the course's actual choice, merge the labels into
   "(Recommended - course default)". A recommendation never removes or moves the
   "(course default)" label. Use the answers already given (project, data, goal, …) to frame
   later questions and describe options in the person's own terms — but never skip a row, drop
   or alter an Option, or move the "(course default)" label because of an earlier answer. Put
   any realizations beyond the tool's option slots (or the free-form case) under the tool's
   "Other"/free-text. Ask about **every** row. A per-call item limit is NEVER a reason to drop,
   skip, merge, or silently default a row — make as many separate calls as there are rows.
4. **Presenting any of these questions ENDS YOUR TURN — stop here; write no code, create or edit
   no file, take no other build action.** Keep asking, one row at a time, until **every** row has
   an answer (a chosen option, an explicit "use the course default", or the step-2 as-is answer,
   which resolves every row at once). Answers to *some* rows do NOT release the build; "no reply
   yet" is not an answer — wait for the user.
5. **Before the first line of code, print a resolved-decision checklist** — every Ledger row
   with its final value (the user's choice, or its Ledger default). Begin implementation ONLY
   after this complete checklist is shown; if any row is unresolved you are not done — return to
   step 3. Build on the checklist's values.
```

---

## 7. The Course Context Pack (CTX-A…CTX-E)

This section is the embedded eighth section of the generated spec — the part that makes it self-contained, carrying the course's transferable knowledge as patterns and decision rules. **Deliberately no code**: concepts outlive any library version while copied cells go stale. Five subsections, always, addressed by stable `CTX-*` anchors:

- **CTX-A. The pattern** — the course's central pipeline with a one-line reason each stage exists.
- **CTX-B. Failure-mode catalog** — one entry per demonstrated failure, each as: *symptom → cause → fix → "enforced by R#/AC#"*. Prose, no code.
- **CTX-C. Decision background** — **reference only, not where decisions are made.** Every design-critical decision (design-structural, course-argued, or course-contradicted) is surfaced as a **Decision Ledger** row (§5.5); the Ledger is where a decision is presented, defaulted, and chosen. CTX-C holds the *durable background* a builder needs to understand those rows: the mechanism behind a trade-off, why the course observed what it did, and the provenance (which config, which lesson) behind a Ledger row's default. Each CTX-C entry that backs a Ledger row cross-references it (e.g. "→ Ledger D<n>"). Do **not** park a live decision here as prose — if a builder must *choose*, it belongs in the Ledger. (This mis-home is the failure §12.9 records: contradicted decisions like cosine/euclidean and `k` buried in CTX-C where no one is asked to decide.)
- **CTX-D. Perishable assumptions** — era-specific class/model/library names as a list, with the instruction: *treat these as search keywords against current docs, not guaranteed imports.* State plainly that the concepts in CTX-A…CTX-C are durable; only these names are perishable.
- **CTX-E. Provenance map** — lesson titles in **transcript numbering** → which CTX-A/B/C items came from each. State explicitly: nothing in the spec requires platform access.

> **Note on the name.** The Context Pack is the eighth section, extending the standard seven-section spec anatomy. It is referenced by the position-independent prefix **CTX-** rather than a section number, so the cross-references survive any reordering or insertion of optional sections.

### Integration mode (deferred — but write the invariants ready for it)

A learner may eventually use the spec not to build a standalone takeaway but to **graft the taught pattern onto their own existing project** ("does my codebase still embody this pattern? what must I preserve?"). That second build mode is **not designed yet** — the current deliverable is the standalone takeaway (default) only. **Do not add an integration section or a second template.**

But author each Decision Ledger row's **Invariant** field so it can *become* that mode's contract later: state what must hold in terms of the pattern's behavior, not the fixture's implementation ("a semantic-similarity store AND an exact-key store must both exist", not "use SQLite"). Written that way, the invariants already answer "what must my integration preserve?" when the mode is built. This costs nothing now and avoids a rewrite later.

---

## 8. Contracts & acceptance-criteria format

**Contracts (§3)** are schemas, never prose. Use JSON Schema (or Zod/OpenAPI) in a code block. Push invariants into the schema (conditional `if/then`, `minItems`, enums) so the contract self-enforces rather than relying on a sentence the agent might miss.

**Acceptance criteria (§5)** define the **fixture corpus first** — name each synthetic file and quote the exact facts it contains, including one deliberate instance of every demonstrated failure mode. Then a Given/When/Then table with concrete inputs and asserted outputs. Each AC traces back to a business rule; each business rule reaches ≥1 AC. The fixtures make the oracle runnable before the learner has real data, and the building agent MUST NOT modify fixtures to make a test pass.

**Invariants must be tested too.** Every Decision Ledger row with a non-empty Invariant must be exercised by ≥1 AC — through the row's default realization is fine (e.g. an "all memory survives process restarts" invariant needs an AC that actually starts a new process against the same stores). A row whose invariant genuinely cannot be tested states why in the row itself. An invariant with no AC is an untested guarantee: a build can violate the spec's central promise while passing every test.

---

## 9. Provenance labels

Apply throughout the spec so course-derived content is never confused with your additions:
- **Course-demonstrated** — traceable to the supplied materials; carries a `(CTX-X)` anchor whose entry traces to the ledger.
- **Project hardening** — a constraint you added that the course did *not* demonstrate (e.g. idempotent re-ingest when the course wipes and rebuilds). Say so explicitly. The takeaway's credibility depends on never putting words in the course's mouth.
- **Learner intake** — `[bracketed]`. Never left empty at generation: every value carries a course-derived default (§3) so the spec builds as-is; the brackets mark where a learner *may* substitute, not a gap that blocks handoff.
- **Owner** (the Decision Ledger's owner column, §5.5) — `learner` (the course has no opinion; pure context, e.g. project/data), `course` (the course fixes it; a technique the learner rarely overrides), or `course+learner` (the course sets the invariant + default; the learner selects a realization, e.g. online-vs-offline store). This is **metadata about who owns the answer, not a behavior switch**: every row carries a default and is surfaced the same way regardless of owner. Owner never decides whether a row gets a default or whether it is shown.

---

## 10. The four-way failure encoding (+ worked example)

**Every demonstrated failure mode MUST appear in all four places**: a business rule, a fixture, an acceptance criterion, and a CTX-B entry. A failure mode missing any of the four is a defect.

**Worked example.**
*Course shows:* a deliberately duplicated PDF makes top-k retrieval return identical chunks; the transcript explains the second copy adds zero value and crowds out a distinct chunk; a diversity-aware method fixes it.
*Spec encodes:*
- **Rule (§4):** "Ingestion is content-deduplicated, and retrieval must not return chunks with identical text (CTX-B1). Use a diversity-aware method or equivalent (CTX-C3). → AC3" — tagged *course-demonstrated*.
- **Fixture (§5):** `expenses-copy.md` — byte-identical copy of `expenses.md`.
- **AC3 (§5):** "Given the corpus includes the duplicate file, when retrieving top-4 for the test query, then no two retrieved chunks have identical content."
- **CTX-B1:** symptom / cause / fix / "enforced by R3, AC3" — prose, no code.

That four-way pattern is the target for *every* failure the course planted.

---

## 11. Anti-patterns to avoid

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Implementation hints ("use a HashMap") | blocks a better/consistent solution | specify the outcome ("lookup must be O(1)") |
| Pseudo-code | the agent copies the flawed structure literally | describe behavior + acceptance criteria |
| Prescriptive architecture (class hierarchies, DI) | forces inconsistency with the learner's codebase | name an outcome; let the agent fit its code |
| Vague quality words ("fast", "secure", "clean", "robust") | no verifiable target | replace with a measurable condition |
| Restating notebook code/docs verbatim | tokens wasted; stale immediately | express as behavior/constraint, not a copied cell |
| Contradictions across sections | the agent silently drops one constraint, invisibly | cross-check schema ↔ rules ↔ ACs ↔ boundaries |
| "should pass" / "looks correct" | "should" means it wasn't verified | require cited evidence (test output, file paths) |

---

## 12. Known traps

Each occurred in a real run; check for them explicitly.

1. **Lesson-numbering drift.** Notebook files numbered 01–06 while the platform counts the Introduction as Lesson 1 — every reference off by one. Transcripts are authoritative.
2. **"Course defaults" that aren't.** An exploratory notebook used one config while the end-to-end app used another; attributing either as "the default" misleads. Cite each config's exact home.
3. **Invented version pins.** If the notebooks installed everything unpinned, an instruction to "pin exact versions from requirements" can only be hallucinated into compliance. State what the materials actually contain.
4. **Over-attribution.** A hardening choice (e.g. idempotent re-ingest) read as course-taught when the course did the opposite. Label hardening as hardening (§9).
5. **Memory leakage.** Recognizing the course from training and generating "from it" without the files present produces plausible, wrong, unverifiable output. Enforce the ground-truth gate (§3).
6. **Snippet reassembly.** The failure this guide exists to prevent: the Context Pack carries concepts, mechanisms, decisions. If a fenced code block from the notebooks appears anywhere in the spec, delete it and write the behavior it implemented.
7. **Ambiguous default → inconsistent builds.** A spec that leaves the no-intake target unresolved — readable as either "build the course's own carried-in example" or "build some agnostic project" — makes the coding agent pick differently run to run. Fix: resolve **one** deterministic default per Decision Ledger row (§3, §5.5) and bake it in, so every build-from-spec run with no intake lands on the same target.
8. **Contract-instead-of-default.** A Ledger row whose "default" is actually a *contract* ("any store that supports vector similarity and exact lookup") or a *menu* ("e.g. SQLite / pgvector / Oracle") names no single target — so the build agent picks, and two builds diverge. This is the exact failure observed when one generation baked a concrete local store and another wrote a menu. Fix: a default is **one buildable target**; the alternatives live in the **Options** column, not the Default. For a heavy-dependency row, apply the §3 dependency precedence and state the branch.
9. **Live decision buried as prose.** A design-structural, course-argued, or course-contradicted decision (store type, a narrated architecture trade-off, a contradicted metric or `k`) written only as a CTX-C paragraph is never *surfaced* — no one is asked to decide, and the generator silently resolves it (often inconsistently run to run). Fix: promote it to a Decision Ledger row (§5.5 surfacing bar); leave only the durable background in CTX-C, cross-referenced to the row.
10. **Silent-default build.** Even a perfect Decision Ledger is never shown to the learner if nothing tells the *build* agent to present it. Because every row carries a complete default, the build never *blocks*, so a build agent proceeds silently on defaults and the learner sees no decision at all — the worst failure, since the decisions are on the page and still invisible. Fix: the spec MUST open with the §0 pre-build gate (§6.0) — an imperative, build-agent-addressed instruction to present every Ledger row and then **hard stop** (end the turn; write no code and touch no file until the user replies). **The gate MUST NOT carry a "proceed if there's no response" escape** — that re-opens this very trap: the agent *always* trivially has "no response" the moment it finishes presenting, so it reads the escape as immediate permission and the ask becomes theater. A narrower "proceed if launched non-interactively" escape is the same hole, smaller; omit it. The §6.0 express lane is NOT such an escape: choosing "build as-is" is an explicit user reply that resolves every row to its default — the trap is proceeding on *silence*, never proceeding on an answer. A visible Ledger without the §0 hard-stop gate — or a gate with an escape clause — is a defect.
11. **Partial-present build.** A distinct failure from §12.10, triggered by *many* rows plus a
    per-call-capped question tool (e.g. Claude Code's `AskUserQuestion` takes only a few
    questions per call; a Ledger may have a dozen-plus rows). The agent presents a first batch,
    the user answers it, and the agent treats that reply as release — building while the
    remaining rows are never surfaced (observed on a 14-row Ledger). Two compounding causes: the
    gate didn't say *how* to present more rows than fit one call, and it keyed resumption on "a
    reply happened." Fix (both required): present **one question per row**, looped until every
    row is asked — never hardcode the cap — and gate the build on a **printed checklist of every
    row's resolved value**, not on the first reply (§6.0). "Asked some, then built" is a defect.

---

## 13. The Regeneration Test

Before delivering, ask: *could an agent rebuild behaviorally-equivalent output from this spec alone* — no course access, no chat history? Use divergence as a diagnostic that points to the exact missing constraint:
- output shape changes between runs → the §3 contract is too vague;
- scope grows with unrequested features → the §1 "Not Included" boundary is incomplete;
- an edge case handled once but not next time → the §5 acceptance criteria don't cover it;
- the built *project* changes between no-intake runs (course example one run, agnostic the next) → the §3 default is ambiguous; resolve it to one target.
- the build's *stack or store* changes between no-intake runs (local one run, cloud the next) → a Decision Ledger row's Default is a menu or contract, not one target; fix per §12.8.

There is no oracle for spec *correctness* except the user; executable acceptance criteria are the practical proxy. Without them, this is prompt-driven development with extra steps.

---

## 14. Pre-handoff checklist

Fix, don't annotate.

**Provenance**
- [ ] Every course-attributed claim traces to a ledger entry in the supplied files; anything that doesn't is removed or relabeled as project hardening.
- [ ] CTX-E lesson numbering matches the transcripts, not notebook filenames or memory.
- [ ] Parameter values cite the exact config they came from; no "course defaults" hand-waving.
- [ ] Every working parameter mined in Pass A lands somewhere in the spec (a Ledger default, a body value, or CTX-C) — walk the scratch provenance ledger; none silently dropped.
- [ ] Version claims match the notebooks' actual install lines; era stated honestly if unpinned.

**Decision Ledger**
- [ ] The spec opens with the `## 0. Before you build — REQUIRED` gate (§6.0), positioned **before** the Decision Ledger.
- [ ] The gate is imperative and addressed to the build agent, and instructs it to present **every** Ledger row, labeling the option the course actually used **"(course default)"** — on a substitution row the course-faithful Options entry, never the substituted Default — with the agent's own "(Recommended)" flag allowed and merged into "(Recommended - course default)" when both land on the same option (§6.0).
- [ ] The gate opens with the **as-is / customize express-lane question** (§6.0); the as-is path skips the per-row questions but still prints the full resolved-decision checklist.
- [ ] The gate is a **hard stop**: it tells the build agent that presenting the decisions ends its turn — write no code and touch no file — with **no "proceed if there's no response" (or "proceed if non-interactive") escape clause** (§12.10).
- [ ] The gate requires a **structured question tool when the environment has one** (e.g. `AskUserQuestion`), named as an example of the class, not a hard dependency; a non-Claude agent (Codex, Cursor, plain chat) can still comply by listing rows in its reply.
- [ ] The gate presents **one question per Ledger row** and states that a per-call item limit is never a reason to drop/merge/default a row — **no numeric cap is hardcoded** (§12.11).
- [ ] The gate gates the build on a **printed resolved-decision checklist covering every row**, not on a single reply — answers to *some* rows do not release the build (§12.11).
- [ ] Every Decision Ledger row names **exactly one** buildable default — no menu, no "any X meeting the invariant" masquerading as a default (§12.8).
- [ ] Every design-structural, course-argued, or course-contradicted decision (§5.5 bar) is a Ledger row; none is left buried as CTX-C prose (§12.9). Conversely, single-valued, never-argued, uncontradicted params are body defaults, not rows.
- [ ] Every row's Category field carries exactly one valid value (design-argued / design-structural / realization / contradicted / learner), chosen by the §5.5 precedence.
- [ ] Every `design-argued` row cites, in its Trade-off cell, the lesson whose narration argued the trade-off.
- [ ] Row order follows the fixed grouping (learner → design → realization → contradicted; pipeline order within groups).
- [ ] Each heavy-dependency row records which §3 dependency-precedence branch was taken and why; the course's own technology appears in that row's Options, tagged "(course default)" when it is not the Default.
- [ ] Every row whose Default is the course's example realization (demo data, example tools) says so in its Decision/Default cell and marks it as expected to be swapped when the learner's project differs.
- [ ] No row's Default or Invariant restates another row's decided value; cross-references only (§5.5).
- [ ] Each row's Invariant is written precisely enough to serve as an integration contract (§ Integration note); learner-context rows carry only the pattern's §3 capability requirements (empty when the pattern demands nothing, never invented).
- [ ] Every non-empty row Invariant is exercised by ≥1 AC, or the row states why it cannot be (§8).
- [ ] Where several §5.5 routes applied to one row, the lower-precedence evidence (e.g. a contradiction behind a design-argued row) is still carried in that row's Default note or Trade-off — never dropped (§5.5).
- [ ] Owner labels are present and used only as metadata — no row's default or surfacing depends on its owner.

**Anatomy**
- [ ] Single clear objective; "Not Included" present (learner exclusions + past-course-scope).
- [ ] §3 contracts are schemas; schema invariants are internally consistent with the ACs.
- [ ] Every business rule → ≥1 AC, and every AC → a rule; every demonstrated failure mode appears in all four places (§10).
- [ ] Always / Ask First / Never all populated; Ask First carries the course's spoken trade-offs.
- [ ] §7 test plan has real commands + the evidence-citation requirement.
- [ ] No copied code anywhere (incl. the Context Pack); no pseudo-code; no vague adjectives; no implementation hints where an outcome would do.
- [ ] No contradictions (check schema ↔ rules ↔ ACs ↔ boundaries pairwise).

**Regeneration**
- [ ] An agent could build behaviorally-equivalent output from the delivered spec alone. Any external dependency is now embedded.

---

## Output

Deliver exactly one file named `spec.md` — the learner's only download. It opens with the `## 0. Before you build — REQUIRED` gate (§6.0), immediately followed by the **Decision Ledger** (§5.5, §6); because every row carries a course-derived default, the spec is buildable as-is and unfilled rows never block handoff, while the §0 gate ensures the decisions are surfaced to a human who is present. Do **not** deliver the provenance ledger, mining notes, or any companion file: the single self-contained spec is the product.
