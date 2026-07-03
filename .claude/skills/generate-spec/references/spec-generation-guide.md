# Spec Generation Guide

**Self-contained, prescriptive guide for generating a learner's takeaway `spec.md` from course materials.** Feed *this guide + the course's concatenated notebook dump + the concatenated transcripts* to a capable model, and it produces the spec. Nothing else is required — the framing, the inputs, the generation procedure, the deterministic output format, and the self-check are all here. **Learner intake is not a generation input**: one `spec.md` is generated for many learners, so intake can't be collected here. Each learner-specific value is emitted as a `[slot]` carrying a course-derived default, and the learner substitutes their own at *build* time.

This guide stands in for three things at once: the **product framing** for the takeaway feature, the **"reusable context package, not snippet reassembly"** idea, and the **spec-quality standard**. Where it says MUST, it is not a preference.

## Contents
1. The framing — what you're making, and why
2. The spec-quality bar — right altitude
3. Inputs & the ground-truth rule
4. Procedure A — mine the materials (two passes)
5. Procedure B — derive the build
6. Required section template (§1–§7 + Course Context Pack)
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

**Learner intake is a build-time input, not a generation input.** One `spec.md` is generated and delivered to many learners; the learner supplies their own project when they build. So the generator **never has intake, must not ask for it, and must not block on it**. Instead:
- Emit each learner-specific value as a `[slot]` (§9 labels it *learner intake*). The intake dimensions a learner may later fill are: *Project* (what they're building); *Data/inputs* (what it operates on, where that lives); *Goal* (what "working" means — what retrieval should find, what the output must guarantee); *Model/provider* preference; *Environment* (where it runs, constraints); *Out of scope* (anything explicitly unwanted).
- **Every `[slot]` MUST carry a course-derived default** so the spec is buildable and evaluatable *as-is*, with zero intake.
- The default MUST be **self-contained inside `spec.md`** — resolvable at build time without reading anything else. During a build, course `materials/` are off-limits (hook-enforced), so a default that points back at the course cannot be resolved. Bake it in.

### The deterministic course-default (the fallback that fixes inconsistent builds)

A build-from-spec run with **no intake MUST resolve to exactly one target, every time** — the generator decides it, not the building agent. Never leave the default ambiguous between "the course's own example" and "some agnostic project"; that ambiguity is precisely what makes builds diverge run to run. Resolve the default with this precedence:

1. **Prefer the course's example scenario shape** — when the materials clearly afford a concrete example, re-express *its shape* on the self-contained synthetic fixture corpus (§5). Recognizably the course's example, but with facts *you* author (no course data copied — §11, §12.6).
2. **Else, a generic minimal instantiation** — when the course has no clean toy example, default to the smallest domain-neutral instantiation of the central pattern (§5), still on the synthetic fixture corpus.

Either way, name **one** buildable target. State which precedence branch you used in the slot's default note.

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
2. **Instantiate the pattern on the course-default** (§3), and mark the intake seams as `[slots]`. Because the generator has no learner intake, build the spec's skeleton on the deterministic default — the pattern instantiated with the default's data, goal, and model choices (on the synthetic fixture corpus), the course's pitfalls to avoid, and the course's API assumptions. Then mark exactly where a learner substitutes their own at build time: `[project]`, `[data]`, `[goal]`, `[model/provider]`, `[environment]`, `[out of scope]` — each with its course-derived default. That mapping is the spec's skeleton. (This is the difference between "here are some course snippets" and "use pattern A; data is B (default: fixture corpus); retrieval goal C; embedding D; chunking must consider E; avoid mistakes F/G/H; here are the course's API assumptions" — buildable as-is, with `[slots]` a learner can swap.)
3. **Convert every demonstrated failure mode into a numbered business rule, and every rule into ≥1 acceptance criterion.** A failure mode without a rule is wasted curriculum; a rule without an AC is unverifiable.
4. **Design a fixture corpus**: small synthetic inputs whose facts *you* author, including one deliberate instance of *each* demonstrated failure mode, so the acceptance criteria run on day one before the learner wires in real data.
5. **Decide the stack**: pin modern versions as *this build's* choice; record course-era API names separately as perishable search keywords (CTX-D). Carry the pattern forward, not the era's call signatures.

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
     course-derived knowledge and [brackets] mark learner-intake values, and every
     [slot] carries a course-derived default so the spec builds as-is with no intake;
     (c) provenance line: generated from <course> notebooks + transcripts on <date>. -->

## Complete before handoff (optional — the spec builds as-is)
<!-- ALWAYS the first section, NEVER a blocker. A table of the learner-intake [slots],
     each with a course-derived Default (§3). Lead with: "These are optional learner
     substitutions. Every slot has a default, so this spec is buildable and evaluatable
     as-is; replace a slot only when applying to a real project."
     | Slot | Default (course-derived) | Note |
     Unfilled slots do NOT block handoff — the defaults ARE the build target. -->

## 1. Objective
<One sentence: what it does, for whom, with what guarantee.> (pattern: CTX-A)
### Not Included            ★
<Explicit out-of-scope list: the learner's exclusions + everything past course scope.
 Without this, the agent adds plausible features nobody asked for.>

## 2. Tech Stack & Versions
<Table: component | pinned choice | note. Mark [learner choice] where intake decided.
 Exactly one row's note MUST state the course's actual install/pin situation honestly
 and point era-specific names to CTX-D. Secrets handling stated here, never hardcoded.>

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
### CTX-C. Decision guides
### CTX-D. Perishable assumptions
### CTX-E. Provenance map
```

End the spec with a status footer: version · course · learner project · the living-document instruction (when the building agent produces something unexpected, add the missing constraint here and re-run).

**Optional sections** — add only when the feature demands it, placed between §7 and the Course Context Pack: performance targets (measurable thresholds), migration notes (before/after + rollback), UI state definitions (loading/error/empty/partial), error-handling taxonomy, compliance constraints (PII/payments/regulated data). Because the Context Pack is referenced by name (CTX-*) not by number, adding these never breaks a cross-reference.

---

## 7. The Course Context Pack (CTX-A…CTX-E)

This section is the embedded eighth section of the generated spec — the part that makes it self-contained, carrying the course's transferable knowledge as patterns and decision rules. **Deliberately no code**: concepts outlive any library version while copied cells go stale. Five subsections, always, addressed by stable `CTX-*` anchors:

- **CTX-A. The pattern** — the course's central pipeline with a one-line reason each stage exists.
- **CTX-B. Failure-mode catalog** — one entry per demonstrated failure, each as: *symptom → cause → fix → "enforced by R#/AC#"*. Prose, no code.
- **CTX-C. Decision guides** — numbered trade-offs: parameters **with provenance** (which config, which lesson); technique selection ("use X when…"); composition/strategy choices stated with the course's *observed* results, not generic advice.
- **CTX-D. Perishable assumptions** — era-specific class/model/library names as a list, with the instruction: *treat these as search keywords against current docs, not guaranteed imports.* State plainly that the concepts in CTX-A…CTX-C are durable; only these names are perishable.
- **CTX-E. Provenance map** — lesson titles in **transcript numbering** → which CTX-A/B/C items came from each. State explicitly: nothing in the spec requires platform access.

> **Note on the name.** The Context Pack is the eighth section, extending the standard seven-section spec anatomy. It is referenced by the position-independent prefix **CTX-** rather than a section number, so the cross-references survive any reordering or insertion of optional sections.

---

## 8. Contracts & acceptance-criteria format

**Contracts (§3)** are schemas, never prose. Use JSON Schema (or Zod/OpenAPI) in a code block. Push invariants into the schema (conditional `if/then`, `minItems`, enums) so the contract self-enforces rather than relying on a sentence the agent might miss.

**Acceptance criteria (§5)** define the **fixture corpus first** — name each synthetic file and quote the exact facts it contains, including one deliberate instance of every demonstrated failure mode. Then a Given/When/Then table with concrete inputs and asserted outputs. Each AC traces back to a business rule; each business rule reaches ≥1 AC. The fixtures make the oracle runnable before the learner has real data, and the building agent MUST NOT modify fixtures to make a test pass.

---

## 9. Provenance labels

Apply throughout the spec so course-derived content is never confused with your additions:
- **Course-demonstrated** — traceable to the supplied materials; carries a `(CTX-X)` anchor whose entry traces to the ledger.
- **Project hardening** — a constraint you added that the course did *not* demonstrate (e.g. idempotent re-ingest when the course wipes and rebuilds). Say so explicitly. The takeaway's credibility depends on never putting words in the course's mouth.
- **Learner intake** — `[bracketed]`. Never left empty at generation: every slot carries a course-derived default (§3) so the spec builds as-is; the brackets mark where a learner *may* substitute, not a gap that blocks handoff.

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
7. **Ambiguous default → inconsistent builds.** A spec that leaves the no-intake target unresolved — readable as either "build the course's own carried-in example" or "build some agnostic project" — makes the coding agent pick differently run to run. Fix: resolve **one** deterministic course-default per slot (§3) and bake it in, so every build-from-spec run with no intake lands on the same target.

---

## 13. The Regeneration Test

Before delivering, ask: *could an agent rebuild behaviorally-equivalent output from this spec alone* — no course access, no chat history? Use divergence as a diagnostic that points to the exact missing constraint:
- output shape changes between runs → the §3 contract is too vague;
- scope grows with unrequested features → the §1 "Not Included" boundary is incomplete;
- an edge case handled once but not next time → the §5 acceptance criteria don't cover it;
- the built *project* changes between no-intake runs (course example one run, agnostic the next) → the §3 course-default is ambiguous; resolve it to one target.

There is no oracle for spec *correctness* except the user; executable acceptance criteria are the practical proxy. Without them, this is prompt-driven development with extra steps.

---

## 14. Pre-handoff checklist

Fix, don't annotate.

**Provenance**
- [ ] Every course-attributed claim traces to a ledger entry in the supplied files; anything that doesn't is removed or relabeled as project hardening.
- [ ] CTX-E lesson numbering matches the transcripts, not notebook filenames or memory.
- [ ] Parameter values cite the exact config they came from; no "course defaults" hand-waving.
- [ ] Version claims match the notebooks' actual install lines; era stated honestly if unpinned.

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

Deliver exactly one file named `spec.md` — the learner's only download. The "Complete before handoff" slots-and-defaults table is always the first section; because every slot carries a course-derived default, the spec is buildable as-is and unfilled slots never block handoff. Do **not** deliver the provenance ledger, mining notes, or any companion file: the single self-contained spec is the product.
