# Spec: Requirements Review Agent with Four Engineered Loops — Standalone Takeaway

> **What you're building.** A requirements-review web app whose agent grades its own reports and improves from a batch of them. You open a ticket that points at a vague requirement document; a few seconds later the ticket reads "Analysis Ready" and a separate, agent-authored report page lists the document's confirmed facts, ambiguities (each with what would resolve it and what breaks if it isn't), clarification questions, assumptions and a short summary — a grader having already sent the first draft back once for missing those "resolved by / edge case" lines. Editing the requirement while the ticket is open re-runs the analysis as a new report version you can diff against the old one. After a batch of such runs, an analyst agent reads the traces, finds that the same correction recurred in most runs, proposes one change to the agent's instruction file, a human approves it, and the next batch passes on the first attempt. **Fastest path:** answer the §0 gate's first question with the recommended baseline build and the whole thing builds end-to-end; the build is **complete when the offline acceptance suite passes** (§5, §7) — an API key unlocks only the `live`-tagged criteria and live use of the finished app.
>
> This file is self-contained: the embedded **Course Context Pack** (last section) replaces every reference to the course. `(CTX-X)` anchors mark course-derived knowledge. The **Decision Ledger** below holds every point where the build could diverge, each pinned to one course-derived default, so the spec builds as-is with no intake.
>
> Generated from the *Loop Engineering with LangChain DeepAgents* notebooks + transcripts + slides on 2026-10-11 · spec-generation-guide commit `f1ab452`. Hand-evolved since 2026-10-11.

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
2. **First question — recommended baseline build, or customize?** Ask exactly one question with
   two options: the **recommended baseline build** — every Ledger row resolves to its Default:
   mostly the course's own choices, with a lighter stand-in wherever the course's choice needs
   setup you may not have (a paid API key, an admin-provisioned service); the step-5 checklist
   marks exactly where the baseline differs from the course — or **customize** the decisions row
   by row. If the user chooses the baseline, skip step 3 — go straight to the step-5 checklist
   and build. If the user chooses customize, continue with step 3.
3. **Present the Ledger ONE ROW AT A TIME — one question per row.** For each row ask a single
   question: the **Decision** as the prompt, its **Options** as the choices. Append
   "(course default)" to the option the course actually used — on a substitution row that is
   the course-faithful Options entry, not the Ledger Default. You may also mark an option
   "(Recommended)" — your judgment for THIS person's context, made now, at gate time; with no
   contextual reason to depart, recommend the row's Default. When your recommended option IS
   the course's actual choice, merge the labels into "(Recommended - course default)". A
   recommendation never removes or moves the "(course default)" label, and no option is ever
   labeled with a bare "(default)" — these two labels and their merged form are the only
   option labels. Use the answers already given (project, data, goal, …) to frame
   later questions and describe options in the person's own terms — but never skip a row, drop
   or alter an Option, or move the "(course default)" label because of an earlier answer. Put
   any realizations beyond the tool's option slots (or the free-form case) under the tool's
   "Other"/free-text. Ask about **every** row. A per-call item limit is NEVER a reason to drop,
   skip, merge, or silently default a row — make as many separate calls as there are rows.
4. **Presenting any of these questions ENDS YOUR TURN — stop here; write no code, create or edit
   no file, take no other build action.** Keep asking, one row at a time, until **every** row has
   an answer (a chosen option, an explicit "use the course default", or the step-2 baseline answer,
   which resolves every row at once). Answers to *some* rows do NOT release the build; "no reply
   yet" is not an answer — wait for the user.
5. **Before the first line of code, print a resolved-decision checklist and write it to
   `resolved-decisions.md`** — every Ledger row with its final value (the user's choice, or its
   Ledger default), each line carrying a deviation mark: `= course choice`, or
   `≠ course choice (course used: <option>)`. The file records what this build was built from;
   nothing reads it back — a later build re-runs this gate. If the baseline path was chosen,
   walk the person through every `≠` row — the course's actual choice, and why this build's
   default substitutes it (the row's Trade-off/branch note says why) — before building. Begin
   implementation ONLY after this checklist is shown and written; if any row is unresolved you
   are not done — return to step 3. Build on the checklist's values.

## Decision Ledger (§0 above requires the build agent to present these before building)

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option. Rows are grouped learner → design (argued and structural interleaved, pipeline order) → realization → contradicted; there are **no contradicted rows** — both course contradictions (§4 R1, R6) are numeric levers and resolve as body defaults. Default-column values are the *generator's* zero-setup recommendation fixed at generation time; the build agent's "(Recommended)" flag is its own gate-time judgment. On the one substitution row (RR1) the baseline departs from the course by construction.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L1 | learner | **Project** — what the four loops wrap. `[project]` | — | A **Requirements Review Agent**: turns a requirement document into a structured five-section review report (CTX-A). Branch: the course's example scenario shape, re-expressed on the authored synthetic fixture corpus (§5) rather than a generic instantiation; **this is the course's example realization and is expected to be swapped** when the learner's project differs — the invariants in the other rows, not the review task, are what must survive. | (a) Requirements Review Agent on the fixture corpus (course default); (b) your own task — any agent whose deliverable is a file a grader can read, e.g. the course's own docs-writer example (CTX-C1). | Swapping the task re-authors the instruction file, the rubric and every fixture; the loop machinery (rows D1–D6, RR1–RR2) carries over unchanged. | learner |
| L2 | learner | **Data / inputs** — where requirement documents come from. `[data]` | The agent is **never handed the document directly**: its opening message names only an identifier, and the document reaches the agent through a tool call that can fail transiently (CTX-A stage 1, CTX-B1). | A local ticket store seeded from `fixtures/tickets.json` (five synthetic requirements keyed by ticket ID, §5), queried by the `fetch_requirement` tool. Default ticket for single-run criteria: `INV-301`. **This store shape is the course's example realization and is expected to be swapped** when the project (row L1) changes; the invariant is what must survive. | (a) local JSON ticket store (course default — the course's fake-Jira map loaded from a JSON file); (b) a real tracker's REST lookup behind the same tool (heavy setup: a tracker account + API token, and network latency on every run; realization: row RR2); (c) documents passed as text and seeded into the store at run time (the course's one-off path). | A real tracker adds a key and network latency to every run and makes the retry demonstration (CTX-B1) real rather than simulated; seeding at run time keeps the agent's behavior identical because it cannot see which path was taken (CTX-C2). | learner |
| L3 | learner | **Goal** — what "working" means. `[goal]` | "Done" must be expressible as **per-criterion pass/fail rubric text** that a grader applies to the finished artifact; all criteria must pass in the same grading pass (CTX-A stage 3). | Every run ends `satisfied` against the three-criterion rubric (completeness, clarity, depth — §4 R6); after one learning-loop cycle the batch's **first-attempt** pass rate reaches 5/5 on every criterion (the course's closing demo, CTX-C8). **The three-criterion rubric is the course's example realization and is expected to be swapped** when the project (row L1) changes; the pass/fail-rubric shape is what must survive. | (a) the three-criterion rubric (course default); (b) your own rubric lines — same shape, same all-must-pass rule. | A rubric edit invalidates comparability with every earlier batch (Ask First, §6). | learner |
| L4 | learner | **Model / provider** preference. `[model]` | Every model used must support **native tool calling**; the analyst's model must additionally return a **structured response** matching the HarnessChange contract (§3); the model is **injected at build time**, never hardcoded in the loop code, so a scripted stand-in (RR1) can replace it. | Provider-prefixed model strings via LangChain's OpenAI integration; the course's own models: `openai:gpt-5.4-mini` for review and grading, `openai:gpt-5.5` for analysis (CTX-D). Key read from `.env` (`OPENAI_API_KEY`). No "current best" model is baked in — the build agent recommends what is current at gate time. | (a) the course's models above (course default — heavy setup: a paid OpenAI API key); (b) any other provider whose models meet the invariant, via the same provider-prefix mechanism. | Changing the model after a batch exists makes before/after comparisons (CTX-A stage 5) incomparable — re-run the baseline batch. Cost: the course priced analysis at roughly 6–7× the review model per token (CTX-D). | learner |
| L5 | learner | **Environment** — where it runs. `[environment]` | The agent's filesystem must be **scoped to one root directory** that the agent sees as `/`, with paths above it unreachable (the repo holds a real `.env`, CTX-B5); the instruction file must sit under that root; each automation run and each batch run gets a **fresh workspace** (CTX-B5). | Local machine, Python ≥ 3.12, local-filesystem backend in virtual mode, secrets in `.env`; event store and its web UI: row RR2. | (a) local machine as described (course default); (b) a container/server with the same layout; (c) a persistent-database filesystem backend (named by the course as supported, never shown). | Nothing in the pattern depends on where it runs; only the root-scoping and fresh-workspace invariants must survive. | learner |
| L6 | learner | **Scope boundary** — present §1 "Not Included" *inside this question*, one line per item with its handling rule (restorable / buildable-unspecified / deferred-to-row / unavailable), and ask whether to keep the list as-is or bring an item back. | — | Keep as-is: every §1 exclusion stands; the full acceptance set (§5) is built. | (a) keep the list as-is (course default); (b) bring an item back — name it; a *restorable* item is added to the build, a *buildable-unspecified* item is added with the caveat that this spec supplies no parameters or acceptance criteria for it, a *deferred* item is decided on its owning row, an *unavailable* item cannot be added. A further exclusion goes in free text and must name the acceptance criteria it retires. | Restoring a keyed item (LangSmith tracing) would add `live` criteria that this spec does not supply; restoring an unspecified item leaves it unverified by §5. | learner |
| D1 | design-argued | **Instruction placement** — how the agent's standing instructions reach it. | The standing instructions are a **recorded file loaded into context at the start of every run**, outside the agent's write permission, so the learning loop can edit it between runs and a saved run can record exactly what the agent was told; further instruction bodies may load on demand (a skills directory) provided they are also files under the same write-denied root and the run records them (CTX-A stage 2, CTX-B6). | One always-loaded instruction file (`/memories/AGENTS.md`) holding the fixed procedure and the review guidance; no skills directory. | (a) one always-loaded memory file (course default); (b) memory file + a skills directory whose bodies load by progressive disclosure (the course's primer agent). | Litmus: **row** — the course showed both (a) and (b) working (poet agent, Lesson 3; review agent, Lessons 4–6) and argued the trade-off aloud: an always-loaded file "costs context on every call, so it should stay short", while skills cost one description line each until read (Lesson 3, CTX-C3). The course's third channel — everything in the build-time system prompt (Lesson 3, CTX-C3) — is not an option on this row: it loses the recorded-instructions property the invariant requires. Switching to (b) moves the learning loop's edit target across files — Ask First (§6). | course+learner |
| D2 | design-argued | **Grader type** — what judges the finished artifact. | A grader **reads the deliverable file itself** (not the conversation), returns **pass/fail per criterion with a `gap` on each failure**, and the run only ends `satisfied` when every criterion passes in one pass (CTX-B2, CTX-B3). | An LLM-as-judge grader given a read-only file tool, instructed to quote verbatim evidence with line numbers and apply labels literally (§4 R7). | (a) LLM-as-judge over the file (course default); (b) deterministic checks (the course's docs-agent example: "links resolve, CI passes"); (c) a human acting as grader. | Litmus: **row** — Lesson 2 (slide 2.6, narrated) states graders "can either be deterministic or agentic", and the docs-writer example runs deterministic checks while the course's own build uses an LLM judge; the human-grader option is the course's second oversight placement (slide 2.12). Deterministic graders are cheaper and exact but only for mechanically checkable criteria; an LLM judge handles prose criteria but "judges by resemblance" unless forced to quote (CTX-B3). | course+learner |
| D3 | design-argued | **Model per role** — one model or several across agent, grader and analyst. | Each role's model meets row L4's invariant; the analyst's role may be assigned independently of the review role. | Agent and grader **share one model**; the analyst runs on a **separate, more capable model** (identities: row L4). | (a) shared agent/grader model + stronger analyst (course default); (b) a separate grader model as well ("a common production choice"). | Litmus: **row** — Lesson 5 narrates both sides as acceptable ("we are using the same model for both of them, but having a different model for grader is a common production choice"); Lesson 2 argues verification "is particularly powerful when you want to use a cheaper model on challenging tasks". One model for all three roles is not offered as an option: the course warns against it for the analyst, because reading several full traces "is the one job the cheaper model does unreliably" (CTX-C4). Changing a grader model changes verdicts without failing any test — Ask First (§6). | course+learner |
| D4 | design-argued | **Trigger kind** — what starts a run. | A run is started by **something other than a person running a cell**, and the trigger records which input version it ran against (CTX-A stage 4). | Event-driven: a ticket is created, or a requirement page linked to an open ticket is saved (§4 R14). | (a) event-driven triggers (course default); (b) scheduled runs (e.g. a morning sweep over all open tickets); (c) both. | Litmus: **row** — Lesson 2 presents triggers as "scheduled, or … ad hoc and event-driven" and gives a working example of each (a morning calendar summary; an email-triggered assistant); slide 2.8 (narrated) lists "a new document lands / a schedule triggers / a webhook arrives". The course built only (a). A schedule changes *when* reports appear without failing any criterion — Ask First (§6). | course+learner |
| D5 | design-structural | **Loop nesting under the trigger** — which loops a triggered run contains. | A triggered run must reach a **terminal status** that the event system records with the run (CTX-A stage 4): under (a) a verification status (`satisfied`, or an explicit exhausted/failed status); under (b) `finished` or `turn_cap` (§3.3). | Trigger → verification loop → agent loop (every automated run is graded; iteration budget: §4 R6). | (a) trigger wraps verification + agent loops (course default); (b) trigger wraps the agent loop only, no grader — the run records `finished` / `turn_cap` and an empty grading list (§3.3, §3.7). | Litmus: **row** — Lesson 2 states the nesting is composable: "You could just nest a core agent loop in with an event-driven loop. You don't need the verification loop per se" — (b) is endorsed, not shown failing. Redrawing the diagram removes the grader box and the retry arrow, so this is structural. Dropping the grader removes a behavior guarantee silently — Ask First (§6). | course+learner |
| D6 | design-structural | **Learning-loop change target** — what the analyst may propose and what gets applied mechanically. | The analyst **reads traces it cannot write**, **proposes without applying**, and every proposal names one of {prompt, tool, grader, configuration} and carries quoted evidence plus a recurrence count (CTX-B7). | Analysis scoped to the **prompt** (the instruction file): a prompt-target proposal is applied by plain string insertion under the named section after human approval; any other target is read and decided by a human, never auto-applied (§4 R19–R21). | (a) prompt-only mechanical application (course default); (b) also allow tool-description or configuration changes to be applied after approval. | Structural: each added target gives the apply step a new owner and a new artifact to version. Lesson 2 names prompts, tools, skills and memory as improvable and memory consolidation (persisted per-user preferences) as a job of the loop; the code scopes to the prompt "because that is what the current evidence implicates" and keeps the other targets expressible (CTX-C7). Memory consolidation is the course-named fifth target this build excludes: it is outside the invariant's target set and the §3.5 enum, so it is not an option on this row (§1 #7). Widening the target widens what a bad proposal can break — Ask First (§6). | course+learner |
| RR1 | realization | **Model access for the acceptance suite** — which model the loops run against. | The suite drives the **real harness end to end** (file tools, permissions, turn cap, grader middleware, trigger, apply/compare logic); the model is the **only component that may be substituted**, and when it is, the substitution is honestly labelled as a fake. Exercised by every offline criterion that runs a loop or the apply/compare step: AC2–AC5, AC7–AC10, AC12–AC15, AC17–AC18, AC21–AC29. | A **scripted replay model** — an honest fake that returns a predetermined sequence of tool calls / verdicts / structured responses per role from `fixtures/replay/*.json` (§5). Branch: the live model is a keyed dependency (heavy) and the only carrier of every taught behavior, so the honest stand-in is the Default and the suite runs on day one, while the real model stays an Option; the stand-in is tier 2 (an in-process fake, no separate service). Its registered description must say it is a fake. | (a) scripted replay model (stand-in for the live model); (b) the live keyed model (course default — heavy setup: paid OpenAI key; used by the `live` criteria). | A replay model proves the harness, not the model: every behavior that depends on model judgment (what counts as an ambiguity, whether the grader's verdict is right) is covered only by the `live` criteria. A third path — replaying saved traces without running the loop, the course's notebook `USE_LIVE_LLM = False` path — is not an option on this row: it shows results but exercises no loop machinery, which the invariant requires; it is what the course shipped for offline use and is why its notebooks could run without a key (CTX-C9). | course+learner |
| RR2 | realization | **Event-system realization** — the ticket tracker and document store the trigger connects to. | Two stores with these semantics: a **ticket** (status, linked requirement page, run history, comments) and a **versioned page** (every save is a new numbered version; the agent's report is a separate agent-authored page, never the requirement page); a human, not the agent, closes a ticket (CTX-A stage 4, CTX-B9). | The course's **local simulation**: one small web app serving a Jira-like board and a Confluence-like page space over three JSON files. Branch: the lightest self-contained realization that preserves the invariant — the course's own realization is already keyless (tier 3: a locally served component, no credential), so it is the Default with no substitution; the real tracker is listed because the course names it as the "next step (not built here)". | (a) local simulated tracker + page store (course default); (b) real Jira + Confluence via their REST APIs and a webhook endpoint (heavy setup: Atlassian account + API token; the course's named next step). | (b) is a drop-in at the automation function — "nothing about the agent or the loop changes" (CTX-C10) — but every trigger criterion becomes `live`. Omitting the event layer and triggering runs from a script is not an option on this row: it leaves no stores to satisfy the invariant and removes rows D4/D5 from the build (the nesting Lesson 2 calls composable, CTX-C6, is row D5's subject, not this row's). | course+learner |

## 1. Objective

Build a requirements-review agent whose deliverable is a single structured report file, then wrap it in three further loops — a grader that sends inadequate reports back with specific feedback, an event layer that runs the agent when a ticket is created or its requirement changes, and a learning loop that mines a batch of graded runs for a recurring correction and proposes one human-approved change to the agent's instruction file — such that, on the fixture corpus, a corrected instruction file raises the batch's first-attempt pass rate from failing on most runs to passing on all of them (pattern: CTX-A).

### Not Included            ★

Each item carries its handling rule for the L6 gate question.

1. **Real Jira / Confluence integration** (REST lookups, a webhook endpoint, Atlassian credentials). *Deferred to row RR2.*
2. **Human approval on individual tool calls inside the agent loop** (interrupt-before-tool). Named by the course as the first oversight placement; never built. *Buildable-unspecified — this spec supplies no parameters and no acceptance criteria for it.*
3. **A human acting as the grader.** *Deferred to row D2.*
4. **Subagents / delegation, a code interpreter or sandbox, summarization and context offloading.** Named as deep-agent pillars; never exercised. *Buildable-unspecified.*
5. **A skills directory with progressive disclosure for the review agent.** *Deferred to row D1.*
6. **Scheduled triggers.** *Deferred to row D4.*
7. **Memory consolidation / per-user preference memory as a learning-loop target.** Named by the course as a job of the loop; never built (row D6's Trade-off). *Buildable-unspecified.*
8. **Hosted tracing (LangSmith).** The course wired it as an optional, key-gated add-on; nothing in the pattern depends on it. *Restorable — requires a tracing API key; would add `live` criteria that this spec does not supply.*
9. **The poet / skills primer agent** the course used to introduce the harness (Lesson 3) — a separate toy agent; its skills mechanism is row D1 option (b); §5 supplies no criteria for it. *Restorable.*
10. **Dollar-cost estimates in the batch comparison.** The course computed them from a hardcoded per-model price table that is perishable; token estimates stay in scope (§4 R22); §5 supplies no criteria for it. *Restorable.*
11. **Notebook visualizations** (HTML cards, pass-rate plots, trace tables rendered for a notebook). The web UI's tables are in scope (§4 R17); notebook rendering is not; §5 supplies no criteria for it. *Restorable.*
12. **Authentication, multi-user access, deployment, or any persistence beyond flat JSON files** for the event layer. Past course scope; §5 supplies no criteria for any of it. *Restorable.*
13. **Grafting the loops onto an existing codebase.** *Unavailable — outside the standalone build mode.*

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language / runtime | Python ≥ 3.12 (course kernel: 3.12.10) | Course-pinned floor: `requires-python = ">=3.12"`; the course notes its numeric dependencies fail to build below 3.12. |
| Agent harness | `deepagents` **0.7.11** | **Course-pinned** — this is the exact version resolved in the course's lock file, and its grader prompt is stated to be copied from 0.7.11; pin the same. The pattern (CTX-A) is harness-independent; the names in CTX-D are this era's. |
| Agent framework | `langchain` **1.3.18**, `langchain-core` **1.6.1**, `langgraph` **1.2.11** | Course-pinned (lock-file resolutions). Provides the model-call-limit middleware, the tool decorator and the in-memory checkpointer the course used. |
| Model provider client | `langchain-openai` **1.6.0**, `openai` **3.6.0** | Course-pinned (lock file). The provider itself is row L4; the model used by the offline suite is row RR1. |
| Structured output | `pydantic` **2.13.5** | Course-pinned. The HarnessChange contract (§3) is enforced as a structured model response. |
| Secrets | `python-dotenv` **1.2.3**; `.env` with `OPENAI_API_KEY`; optional `LANGSMITH_TRACING`/`LANGSMITH_API_KEY`/`LANGSMITH_PROJECT` | Course-pinned. `.env` is gitignored; ship `.env.example` with placeholders only. **Never hardcode a key.** |
| Event-layer web app | `flask` **≥ 3.1.3** (floor only) | **Install-pin honesty line:** the course set floors (`>=`) in `pyproject.toml`/`requirements.txt` and pinned exact versions only through a `uv.lock`; `flask` is the one dependency with a floor but **no lock entry**, so it is the only unpinned component here — choose a current 3.x release and record it in your own lock file. Era-specific names (provider prefixes, middleware class names, grader response fields) are listed in CTX-D as search keywords, not guaranteed imports. |
| Token estimate | `tiktoken` **0.14.0** (encoding `o200k_base`), with a `len(text) // 4` fallback when unavailable | Course-pinned; the fallback is the course's own. |
| Event store | Three JSON files (`data/pages.json`, `data/tickets.json`, `data/analysis_runs.json`) | Row RR2's Default; learners change it there, not here. |
| Agent filesystem | Local-filesystem backend in virtual mode, one root per run | Row L5's Default. |
| Test runner | `pytest` (current release — the course has no test suite; **unpinned by the course**, your choice) | Project hardening (not demonstrated by the course): the course verified by inspection in notebooks. |

## 3. Input/Output Contracts            ★

Schemas are JSON Schema (draft 2020-12). The report file is Markdown; its *parsed* form is the contract the grader and the counting helpers depend on.

### 3.1 Requirement document and ticket store

```json
{
  "$id": "ticket_store",
  "type": "object",
  "description": "fixtures/tickets.json, the fetch tool's ticket store: ticket id -> requirement text. The event store's ticket (3.7) carries no text; its requirement lives on the linked page.",
  "propertyNames": { "pattern": "^[A-Z]{2,6}-[0-9]{3}$" },
  "additionalProperties": { "type": "string", "minLength": 1,
    "pattern": "(?s)^\\s*REQUIREMENT: .+" },
  "minProperties": 1
}
```

Identifier alphabet is part of the contract: 2–6 upper-case ASCII letters, a hyphen, exactly three digits (course form `AUTH-142`; tracker-generated keys `REQ-104`, `REQ-105`, …).

### 3.2 The analysis report (parsed form of `/analysis.md`)

```json
{
  "$id": "analysis_report",
  "type": "object",
  "required": ["title", "confirmed_facts", "ambiguities", "clarification_questions", "assumptions", "summary"],
  "properties": {
    "title": { "const": "Requirements Analysis" },
    "confirmed_facts": { "type": "array", "items": { "type": "string", "minLength": 1 } },
    "ambiguities": { "type": "array", "items": { "$ref": "#/$defs/ambiguity" } },
    "clarification_questions": { "type": "array", "items": { "type": "string", "minLength": 1 } },
    "assumptions": { "type": "array", "items": { "type": "string", "minLength": 1 } },
    "summary": { "type": "string", "description": "prose, 2-3 sentences; counted in words, never in bullets" }
  },
  "$defs": {
    "ambiguity": {
      "type": "object",
      "required": ["clause", "reason"],
      "properties": {
        "clause": { "type": "string", "minLength": 1, "description": "verbatim quote of the under-specified clause" },
        "reason": { "type": "string", "minLength": 1 },
        "resolved_by": { "type": "string", "minLength": 1, "description": "the indented line labelled exactly 'Resolved by:'" },
        "edge_case": { "type": "string", "minLength": 1, "description": "the indented line labelled exactly 'Edge case:'" }
      }
    }
  }
}
```

Invariants carried by the file form: the five `##` headings appear **exactly once each, in this order** — Confirmed Facts, Ambiguities, Clarification Questions, Assumptions, Summary; a report is **complete** only when each of the four list sections has ≥ 1 bullet and the summary has ≥ 1 word (§4 R3). The labels `Resolved by:` and `Edge case:` are **binding constants**: a differently-labelled line is a different line for the grader (§4 R6).

### 3.3 Grading pass and verification run

```json
{
  "$id": "grading_pass",
  "type": "object",
  "required": ["iteration", "result", "explanation", "criteria", "analysis_markdown"],
  "properties": {
    "iteration": { "type": "integer", "minimum": 1 },
    "result": { "enum": ["satisfied", "needs_revision", "failed", "grader_error"] },
    "explanation": { "type": "string" },
    "criteria": { "type": "array", "items": {
      "type": "object", "required": ["name", "passed"],
      "properties": { "name": { "type": "string" }, "passed": { "type": "boolean" }, "gap": { "type": "string" } },
      "if": { "properties": { "passed": { "const": false } } },
      "then": { "required": ["gap"], "properties": { "gap": { "minLength": 1 } } } } },
    "analysis_markdown": { "type": "string", "description": "the file exactly as this pass saw it" }
  },
  "allOf": [
    { "if": { "properties": { "result": { "const": "satisfied" } } },
      "then": { "properties": { "criteria": { "items": { "properties": { "passed": { "const": true } } } } } } },
    { "if": { "properties": { "result": { "const": "needs_revision" } } },
      "then": { "properties": { "criteria": { "contains": { "properties": { "passed": { "const": false } } } } } } },
    { "if": { "properties": { "result": { "const": "grader_error" } } },
      "then": { "properties": { "criteria": { "maxItems": 0 } } } }
  ]
}
```

```json
{
  "$id": "verification_run",
  "type": "object",
  "required": ["requirement_doc", "rubric", "trace", "grading", "analysis_markdown", "instructions", "status", "turns"],
  "properties": {
    "requirement_doc": { "type": "string" },
    "rubric": { "type": "string" },
    "trace": { "type": "array", "items": { "$ref": "#/$defs/trace_step" } },
    "grading": { "type": "array", "items": { "$ref": "grading_pass" } },
    "analysis_markdown": { "type": "string" },
    "instructions": { "type": "string", "description": "the instruction file the run was given, verbatim" },
    "status": { "enum": ["satisfied", "max_iterations_reached", "failed", "grader_error", "needs_revision"],
                "description": "the first four are terminal (R8); needs_revision is the in-flight value between grading passes and never appears on a finished run" },
    "turns": { "type": "integer", "minimum": 0 }
  },
  "$defs": { "trace_step": {
    "type": "object", "required": ["step", "actor", "action"],
    "properties": {
      "step": { "type": "integer", "minimum": 1 },
      "actor": { "enum": ["Model reasoning", "Tool"] },
      "action": { "type": "string" },
      "detail": { "type": "string", "maxLength": 221 } } } }
}
```

A plain review run (no grader) is the same object without `rubric`, `grading` and `status`, plus `stage_order` (the list-section names in the order they were actually filled) — the last trace step's `action` is `Finishes the review` when the report is complete and `Stops: turn limit of <N> reached` otherwise (§4 R4). When a trigger records a plain run (row D5 option (b)), the §3.7 `run` carries the terminal status `finished` (report complete, model's own final message) or `turn_cap` (cap reached), mirroring that last trace step, and an empty `grading` list.

### 3.4 Batch record and summary (learning loop input)

```json
{
  "$id": "batch_summary",
  "type": "object",
  "required": ["label", "model", "runs", "graded", "grader_errors", "first_attempt", "revisions_needed", "documents"],
  "properties": {
    "label": { "type": "string" },
    "model": { "type": "string" },
    "runs": { "type": "integer", "minimum": 1 },
    "graded": { "type": "integer", "minimum": 0 },
    "grader_errors": { "type": "integer", "minimum": 0, "description": "runs - graded; never averaged away" },
    "first_attempt": { "type": "object", "additionalProperties": {
      "type": "object", "required": ["passed", "total", "pass_rate"],
      "properties": { "passed": { "type": "integer" }, "total": { "type": "integer", "description": "= graded" },
                      "pass_rate": { "type": ["number", "null"] } } } },
    "revisions_needed": { "type": "integer", "description": "graded runs whose first attempt failed any criterion" },
    "documents": { "type": "array", "items": { "type": "string" } }
  }
}
```

Each run in a batch is stored as `run_history/<label>/run_NN_<doc>.json` with: `run_id`, `doc_name`, `label`, `model`, `requirement_doc`, `instructions`, `messages` (every message untruncated, with full tool-call args and tool results), `grading` (list of `grading_pass`), `analysis_markdown`, `status`, `started_at`. The batch directory also holds `AGENTS.md` (the instruction snapshot the batch ran under) and `summary.json`.

### 3.5 Harness change proposal (learning loop output)

```json
{
  "$id": "harness_change",
  "type": "object",
  "required": ["target", "issue", "recurrence", "evidence", "section", "change", "rejected"],
  "properties": {
    "target": { "enum": ["prompt", "tool", "grader", "configuration"] },
    "issue": { "type": "string", "minLength": 1, "description": "a property of the agent, not of one document" },
    "recurrence": { "type": "string", "minLength": 1, "description": "how many runs show it, and which" },
    "evidence": { "type": "array", "minItems": 1, "items": { "type": "string" }, "description": "verbatim quotations from the runs" },
    "section": { "type": "string", "description": "exact heading in the instruction file; empty unless target = prompt" },
    "change": { "type": "string", "minLength": 1, "description": "literal text to insert, not a description" },
    "rejected": { "type": "array", "items": { "type": "string" } }
  },
  "if": { "properties": { "target": { "const": "prompt" } } },
  "then": { "properties": { "section": { "pattern": "^#{1,6} .+" } } },
  "else": { "properties": { "section": { "const": "" } } }
}
```

### 3.6 Batch comparison

```json
{
  "$id": "comparison",
  "type": "object",
  "required": ["verdict", "criteria", "runs", "revisions_needed", "attempts", "input_tokens", "output_tokens", "improved", "regressed"],
  "properties": {
    "verdict": { "enum": ["regression", "success", "partial", "no effect"] },
    "criteria": { "type": "object", "additionalProperties": { "type": "array", "prefixItems": [{ "type": "integer" }, { "type": "integer" }], "minItems": 2, "maxItems": 2 } },
    "runs": { "type": "integer" },
    "revisions_needed": { "type": "array", "prefixItems": [{ "type": "integer" }, { "type": "integer" }] },
    "attempts": { "type": "array", "prefixItems": [{ "type": "integer" }, { "type": "integer" }] },
    "input_tokens": { "type": "array", "prefixItems": [{ "type": "integer" }, { "type": "integer" }] },
    "output_tokens": { "type": "array", "prefixItems": [{ "type": "integer" }, { "type": "integer" }] },
    "improved": { "type": "array", "items": { "type": "string" } },
    "regressed": { "type": "array", "items": { "type": "string" } }
  }
}
```

### 3.7 Event store (tracker + page space)

```json
{
  "$id": "event_store",
  "$defs": {
    "ticket": { "type": "object",
      "required": ["key", "title", "description", "linked_page_id", "assignee", "status", "comments", "created_at", "last_analyzed_version", "last_run_id"],
      "properties": {
        "key": { "type": "string", "pattern": "^[A-Z]{2,6}-[0-9]{3}$" },
        "status": { "enum": ["Open", "Analysis Ready", "Done"] },
        "linked_page_id": { "type": "string" },
        "comments": { "type": "array", "items": { "type": "object", "required": ["author", "text", "timestamp"] } },
        "last_analyzed_version": { "type": ["integer", "null"] },
        "last_run_id": { "type": ["string", "null"] } } },
    "page": { "type": "object",
      "required": ["id", "kind", "title", "linked_ticket", "versions"],
      "properties": {
        "kind": { "enum": ["requirement", "analysis_report"] },
        "linked_ticket": { "type": ["string", "null"] },
        "versions": { "type": "array", "items": { "type": "object",
          "required": ["n", "author", "timestamp", "body"],
          "properties": { "n": { "type": "integer", "minimum": 1 } } } } },
      "allOf": [
        { "if": { "properties": { "kind": { "const": "requirement" } } }, "then": { "properties": { "linked_ticket": { "const": null } } } },
        { "if": { "properties": { "kind": { "const": "analysis_report" } } }, "then": { "properties": { "linked_ticket": { "type": "string" } } } } ] },
    "run": { "type": "object",
      "required": ["id", "ticket_key", "requirement_page_id", "requirement_version", "report_page_id", "report_version", "status", "turns", "counts", "trace", "grading", "timestamp"],
      "properties": {
        "id": { "type": "string", "pattern": "^[0-9a-f]{8}$" },
        "status": { "enum": ["satisfied", "needs_revision", "failed", "max_iterations_reached", "grader_error", "finished", "turn_cap"],
                    "description": "verification statuses under row D5 (a); finished / turn_cap only for a no-grader run under D5 (b)" },
        "counts": { "type": "object", "required": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions"], "additionalProperties": { "type": "integer" } } } }
  }
}
```

Version numbers within a page are consecutive from 1; run ids are 8 lower-case hex characters (alphabet is part of the value); the agent-authored report page for ticket `<KEY>` has id `page-analysis-<key lower-cased>` and title `Analysis Report — <KEY>`.

## 4. Business Rules

Numbered; each = behavior + the failure it prevents (CTX-B anchor, where the course demonstrated the failure; a rule with no anchor prevents no catalogued failure) + → AC#. Labels: **[C]** course-demonstrated, **[H]** project hardening (not demonstrated by the course — says so). Parameter values cite their exact source.

**Agent loop**

- **R1 — Fetch by identifier, retry on error.** [C] The run's opening message names only a ticket ID; the agent obtains the document through a `fetch_requirement` tool that looks the ID up in the ticket store. A transient failure is returned as an **error string, not an exception**, and the agent calls the **same tool with the same arguments** until it succeeds; an unknown ID returns an error string naming the ID. Prevents CTX-B1. The fixture fetch tool simulates **2** failures (first a "503 Service Unavailable", then a "timed out after 10s" text) before succeeding — *post-build lever*: the course set this both ways (narration and the notebook's tool table / prebaked trace: two failures; the helper module's default constant: 0, "a clean fetch"); a value-only contradiction with no structural stakes is a body lever, not a Ledger row, so the lever-value rule picks the value the lesson narration states aloud (2) for the retry fixture; on the trigger path (R14) and in batches (R18) the count is **0** by default (CTX-C11; switching it on is Ask First, §6). → AC2, AC3.
- **R2 — The deliverable is a file, built stage by stage.** [C] The report is `/analysis.md` in the agent's scoped filesystem, created by one `write_file` call that lays down the title line `# Requirements Analysis` and the full five-heading skeleton with only Confirmed Facts filled, then completed by one `edit_file` call per remaining section (Ambiguities, Clarification Questions, Assumptions, Summary) — one tool call per stage, in order, as *requested* by the instruction file and *measured* by the harness (`stage_order`), not enforced. An `edit_file` whose target string is not unique in the file returns an error; the agent recovers by re-reading and retrying. Prevents CTX-B10. Litmus (design-argued): the "report as a returned message" alternative is never shown for this agent — single-sided → bake-in, not a row (CTX-C2). → AC4, AC5, AC21 (the error-and-retry).
- **R3 — Completeness is mechanical.** [C] A report opens with the title line `# Requirements Analysis` (the course's report template; §3.2 `title` — a shape constraint asserted by AC5, not a completeness condition) and is complete only when the five `##` headings each appear exactly once, in order, each of the four list sections has ≥ 1 bullet, and Summary has ≥ 1 word. Section counts are **bullets per list section**; Summary is counted in **words** and never reported as a bullet count. Output-shape constraints the instructions impose: one bullet per confirmed fact (stated directly, never inferred), one ambiguity bullet per under-specified clause quoting the **exact clause in bold** followed by an indented `Reason:` line, one bullet per question / assumption, Summary of **two or three sentences**, and a closing reply of one short sentence with no further tool calls. Prevents CTX-B10 (duplicated headings). → AC5, AC6.
- **R4 — Turn cap ends, finish is the norm.** [C] A model-call limit ends the run (exit behavior "end", not an error) when the model never finishes; the normal stop is the model's own final message after the Summary stage. The saved trace's last step reads `Finishes the review` only when the report is complete (R3); otherwise `Stops: turn limit of <N> reached`. Values, by source: **12** for an ungraded single review (Lesson 4 notebook config and the helper's `MAX_TURNS`, "six stages plus headroom for retries and the closing message"); **40** whenever a grader is attached (Lesson 5 notebook config; the automation trigger; the batch runner; also the analyst agent); 30 in the primer. Prevents CTX-B12. → AC7.
- **R5 — Trace rows.** [C] Every run records one row per model turn (`actor: Model reasoning`, action `Calls <tool>[: <sections filled>]`) and one per tool result (`actor: Tool`, detail truncated to 220 characters plus an ellipsis — the course helper module `deepagent_helpers.py`'s `_truncate` default, `limit=220`); a tool row names the sections its call actually filled (a heading counts only when text follows it in the same call). → AC4.

**Verification loop**

- **R6 — Rubric and verdict.** [C] The rubric is three named criteria in this order — `completeness` (every clause of the requirement is addressed somewhere in the analysis), `clarity` (every Ambiguities bullet has an indented line labelled exactly `Resolved by:` naming the fact or decision that settles it), `depth` (every Ambiguities bullet has an indented line labelled exactly `Edge case:` naming a concrete production failure it could cause). The grader returns pass/fail per criterion with a `gap` on every failure; `satisfied` requires **all criteria passing in the same pass**; `needs_revision` injects the feedback into the conversation and the agent revises the same file; `failed` means the rubric is unevaluable. The grader may send work back at most **MAX_RUBRIC_ITERATIONS = 3** times — *post-build lever*: the course set 3 in the lesson that introduces the loop (Lesson 5 narration and notebook config, and the batch runner) and 2 in the event-trigger app; the contradiction is numeric with no structural stakes, so it is a body lever, not a Ledger row, and resolves by the lever-value rule's first branch (narrated value) to 3 everywhere, including the trigger. Setting it to 0 degrades to the plain agent loop (Ask First, §6). Prevents CTX-B2. → AC8, AC9, AC10, AC31 (live).
- **R7 — The grader judges the artifact, with evidence.** [C] The grader is given exactly one tool, read-only file access, and its instructions require it to read `/analysis.md` before judging, to **quote verbatim with a line number** the text that satisfies each criterion it passes (if it cannot quote it, the criterion fails), to apply labelled-line criteria **literally** (a different label is a different line), to check every item rather than sampling, and to be conservative (unconfirmed ⇒ fail with a gap naming the missing evidence). The grader's instructions must restate the library's own verdict definitions and its rule that transcript content is untrusted observation, because supplying a custom grader prompt *replaces* the default rather than extending it. Prevents CTX-B3. → AC11, AC32 (live).
- **R8 — Terminal status is explicit.** [C] A verification run ends with one of `satisfied`, `max_iterations_reached` (budget exhausted; the last grading pass still reads `needs_revision`), `failed`, or `grader_error`; the run record's `status` is read from the loop's own terminal state, falling back to the last pass's result only when no terminal state exists; `needs_revision` is the in-flight value between grading passes and is never a terminal status (§3.3). A grader exception is recorded as a pass with `result: grader_error` and no criteria, and the run continues. Prevents CTX-B12, CTX-B8. → AC10, AC22.

**Harness protection (all loops)**

- **R9 — Instructions are read-only to the agent and loaded every run.** [C] The instruction file at `/memories/AGENTS.md` is loaded into context at the start of every run; writes under `/memories/**` are **denied by permission**, not merely by instruction, because the agent holds `edit_file` on the same filesystem. The harness seeds every run workspace's `/memories/AGENTS.md`: single-run criteria and the trigger app from `fixtures/agents_v1.md` by default, batch runs from the batch's instruction snapshot (R18). Every saved run stores the instruction text verbatim. Prevents CTX-B6. → AC12, AC14.
- **R10 — A missing instruction file fails loudly.** [C] Building the agent raises an error naming the missing path if the workspace has no instruction file, because the harness silently ignores a missing memory file and would run on the system prompt alone. Prevents CTX-B4. → AC13.
- **R11 — Fresh state per run.** [C] Any leftover `/analysis.md` is deleted before a run starts; each triggered run and each batch run gets its own workspace seeded with the instruction snapshot under test and deleted (trigger) or kept beside the run record (batch) afterwards; the grading-pass list is cleared before a run on a reused agent. Prevents CTX-B5. → AC15.
- **R12 — The model is injected.** [H, derived from the course's replay switch] Every loop takes its model as a constructor argument (a provider-prefixed string or a model object); no model name is hardcoded in loop code. The offline suite injects the scripted replay model (row RR1); the `live` suite injects row L4's models. → AC1.
- **R13 — Secrets.** [C] API keys and tracing settings are read from the environment via `.env`; `.env` is gitignored; `.env.example` ships placeholders only; tracing is off unless `LANGSMITH_TRACING` is the string `true`. → AC30.

**Event-driven loop**

- **R14 — Triggers.** [C] Creating a ticket that links to a requirement page runs the verification loop at once; saving a new version of a requirement page re-runs it for **every ticket linked to that page whose status is not `Done`** and reports which were re-triggered (or that none were); "Re-run analysis now" on an open ticket is a manual trigger; a `Done` ticket is never re-triggered. Before every triggered run starts, the trigger **registers the linked page's current version text under the ticket key in the fetch store** (§3.1), so the run's `fetch_requirement` serves exactly that version and the run record's `requirement_version` names it; the trigger path runs with simulated fetch failures off (0, R1). Prevents CTX-B9. → AC16, AC17, AC18.
- **R15 — Write-back to a separate, agent-owned page.** [C] The agent never edits the requirement page; its report is appended as a **new numbered version** of a page of kind `analysis_report` (one per ticket, created on first run, authored by the bot identity), prefixed with a banner stating the ticket key, the requirement version analyzed, the verification status and the number of grading passes. The run is recorded (§3.7 `run`), the ticket moves to `Analysis Ready` with `last_analyzed_version` and `last_run_id` set, and a bot comment names the status, requirement version and report page. Prevents CTX-B9. → AC17, AC19.
- **R16 — A human closes.** [C] Only a human action moves a ticket to `Done`; no code path in the automation does. Prevents CTX-B9. → AC18.
- **R17 — Change is shown two ways.** [C] When a ticket has ≥ 2 runs, its page shows a "what changed since the previous run" table (requirement version, status, bullets per list section, previous vs latest) and a run history; the page-space compare view shows a unified diff of any two versions and, for report pages, the two runs' status and counts beside it — because counts often look alike while the text changed completely. Prevents CTX-B11. → AC20.

**Learning loop**

- **R18 — A batch is one instruction version over every document.** [C] A batch runs every `*.md` in the documents directory under one instruction snapshot (copied into the batch directory as `AGENTS.md`), with the verification loop (R6, budget 3) and simulated fetch failures off (0 — "it only adds turns and noise" here), recording the full conversation, every grading pass and the final file per run, then writes `summary.json` (§3.4). First-attempt failures are keyed by **criterion position in the rubric**, not by the grader's wording; runs with `grader_error` are excluded from every denominator and counted in `grader_errors`; `revisions_needed` counts graded runs whose first attempt failed any criterion. Prevents CTX-B8. → AC21, AC22, AC33 (live).
- **R19 — The analyst proposes; it cannot touch the evidence.** [C] The analyst agent runs in a filesystem rooted **above** the batch directories with write permission on `/proposal.md` only and a blanket write-deny elsewhere; its tools are exactly `ls`, `read_file`, `glob`, `grep`, `write_file` (the course helper module `hill_climbing.py`'s analyst filesystem middleware); it reads the summary first, then runs, then the batch's instruction snapshot; it returns a `harness_change` (§3.5) whose `evidence` entries are verbatim quotations and whose `change` is literal insertable text; a problem seen in **one run of the batch is not a pattern** — it goes under `rejected`, never into `change`. After the analyst returns, the **harness** (not the analyst) persists both halves keyed by batch label at the history root — `run_history/proposal_<label>.md`, a copy of the analyst's `/proposal.md`, and `run_history/proposal_<label>.json`, the `harness_change` serialized (§3.5) — as the course helper module `hill_climbing.py` does; `/proposal.md` stays the analyst's own scratch file. Prevents CTX-B7, CTX-B10 (the one-off edit error goes under `rejected`). → AC23, AC24, AC33 (live).
- **R20 — Human approval before any change.** [C] Nothing is applied until a person has reviewed `proposal.md` (summary signal, current gap, evidence per run, proposed insertion, rejected observations) and explicitly approved; the apply step takes that approval as an argument/flag and refuses without it. Litmus (design-argued): the course warns against unreviewed harness changes and never shows auto-apply working — single-sided → bake-in, not a row (CTX-C7). → AC25, AC33 (live).
- **R21 — Mechanical apply, prompt target only.** [C] Applying a `prompt`-target change inserts `change` at the **end of the section named by `section`**, by this exact algorithm (the course helper module `hill_climbing.py`'s `apply_change`): the section runs from the heading line to the line before the next heading of equal or shallower depth (or end of file); the section body's trailing blank lines are trimmed; `change` is stripped of leading/trailing whitespace and split into lines; the output is the lines before the section, the trimmed body, **one blank line, the change lines, one blank line**, then the rest of the file unchanged, ending with exactly one newline. Every other line is untouched; any other `target` raises an error telling the human to read the proposal and decide; a `section` not present in the file raises an error. Prevents CTX-B2 (the across-runs fix). → AC26, AC27, AC33 (live).
- **R22 — Re-batch and verdict.** [C] After applying, a second batch runs under the new snapshot and the two summaries are compared per criterion on **first-attempt passes**: `regression` if any criterion fell; else `success` if the after-batch needed zero revisions; else `partial` if any criterion rose; else `no effect`. The comparison also carries attempts (grading passes summed), and token estimates: for each AI message, input = instruction-file tokens + 120 (the per-call overhead literal in the course helper module `hill_climbing.py`'s `usage()`) + the running size of all earlier messages, output = that message's size (content plus serialized tool-call args), counted with `tiktoken` `o200k_base` or `len // 4` when unavailable. Prevents CTX-B2 (measures the fix). → AC28, AC29, AC33 (live).

## 5. Acceptance Criteria                ★  (the oracle)

### 5.1 Fixture corpus (synthetic — every fact below is authored for this spec, none is course data)

All fixtures live under `fixtures/`; Python fixture modules use underscore names so they import. The building agent MUST NOT modify fixtures to make a test pass.

**`fixtures/tickets.json`** — five tickets (§3.1). Default single-run ticket: `INV-301`.

| Ticket | Title line | Clauses (one paragraph each, verbatim) |
|---|---|---|
| `INV-301` | `REQUIREMENT: Inventory Restock Alerts` | Stock levels shall be monitored continuously. / Managers must be alerted when stock runs low. / Alerts should not be too frequent. / Restock orders may be created automatically for popular items. |
| `EXP-412` | `REQUIREMENT: Scheduled Data Export` | Users shall be able to export their data. / Exports should complete in a reasonable time. / Large exports must not slow down the system. / Exported files should be kept for a while. |
| `SEC-118` | `REQUIREMENT: Session Timeout` | Sessions shall expire after a period of inactivity. / Users should be warned before expiry. / Sensitive operations require a recent login. / Expired sessions must be cleaned up. |
| `BIL-207` | `REQUIREMENT: Overdue Invoice Reminders` | Customers with overdue invoices shall be reminded. / Reminders must escalate in tone. / Reminders should stop once the invoice is paid. / Very old invoices need manual handling. |
| `SRCH-509` | `REQUIREMENT: Search Autocomplete` | The search box shall suggest completions as the user types. / Suggestions must appear quickly. / Popular queries should rank higher. / Offensive suggestions must never be shown. |

**`fixtures/requirements/`** — the same five texts as files, for the batch runner: `01_inventory_restock.md`, `02_data_export.md`, `03_session_timeout.md`, `04_invoice_reminders.md`, `05_search_autocomplete.md`.

**`fixtures/agents_v1.md`** — the instruction file baseline (D1). Required content, in your own words: a title naming the Requirements Review Agent; a **Procedure** section stating the six stages of R2 in order, one tool call per stage, no skipping or combining; the retry rule of R1 (an error result ⇒ call the same tool with the same arguments; expected and normal); the two read-only rules (never modify the requirement document; never edit this file); the finish rule (after Summary, reply with one short sentence and call no further tools); the R3 shape rules (skeleton with the `# Requirements Analysis` title line and the five headings; one bullet per item; ambiguity bullet = bold-quoted exact clause then an indented `Reason:` line; Summary two or three sentences); and a **Review guidance** section with four `###` sub-sections in this order — `### Confirmed facts` (record only what the document states; do not infer), `### Ambiguities` (quote the exact clause, then the reason it is under-specified — **and nothing about `Resolved by:` or `Edge case:` lines: this omission is the planted gap, CTX-B2**), `### Clarification questions` (what a reviewer needs answered before work starts), `### Assumptions` (what a developer would assume if nobody answered). Layout facts the apply oracle depends on: every section body is followed by exactly one blank line before the next heading, and the file ends with exactly one newline.

**`fixtures/agents_v2_expected.md`** — the result of applying the five-line `change` text (defined under `analyst_v1.json` below) to `agents_v1.md` by the R21 algorithm. Concretely: `agents_v1.md` with its `### Ambiguities` body's single trailing blank line trimmed and these seven lines placed before `### Clarification questions` — a blank line, the five `change` lines, a blank line. Since the trimmed blank is re-emitted, v2 is v1 plus exactly **six** lines — the five `change` lines and one blank line — so a line diff against v1 shows six added lines and no removals; the file still ends with exactly one newline. This is the oracle for AC26.

**`fixtures/rubric.md`** — the three criterion lines of R6, one bullet each, in the order completeness, clarity, depth.

**`fixtures/scripted_model.py`** — the replay stand-in (row RR1): loads a replay file and serves, per role (`agent`, `grader`, `analyst`), a fixed sequence of responses; each response is either a set of tool calls, a final text, or a structured object; its model name is `scripted-replay/<file>` and its description states it is a fake for tests. The real harness tools execute the scripted calls, so file contents, permissions and middleware are exercised for real. **Per-document selection in batches:** the batch runner is handed a script *directory* (`batch_v1/`, `batch_v1_grader_error/`, `batch_v2/`) and constructs one scripted model per document from `<dir>/<nn>.json`, keyed by the document filename's two-digit prefix (`01_inventory_restock.md` → `01.json`); the batch summary's `model` records the directory form, `scripted-replay/<dir>`. **Sequencing across runs:** each new run (a fresh invocation of a loop — a triggered run, a batch document, a repeated verification run) restarts every role's sequence from its first response, so one script serves any number of runs; the per-role call counters (AC1) accumulate across runs and are never reset.

**`fixtures/replay/*.json`** — the scripts. What each makes happen:

| File | Role(s) | Facts the script produces |
|---|---|---|
| `review_clean.json` | agent | 6 tool calls in R2 order on `INV-301`, then the sentence `Review complete.` The draft (v1 shape): Confirmed Facts — `Stock levels are monitored continuously.`, `Managers are alerted when stock runs low.`, `Restock orders may be created automatically for popular items.`; Ambiguities — **"runs low"** / Reason: no threshold is given; **"not be too frequent"** / Reason: no rate or window is given; **"popular items"** / Reason: popularity is undefined; Clarification Questions — `What stock level counts as low?`, `What is the maximum alert frequency per item?`, `How is popularity measured?`; Assumptions — `Low means below 10 units.`, `At most one alert per item per day.`; Summary — two sentences, 25 words total. |
| `review_retry.json` | agent | As `review_clean`, but the first two fetch results are errors and the agent repeats the identical call: three `fetch_requirement` calls before the write. |
| `review_never_finishes.json` | agent | Fetches, writes the skeleton, then issues `edit_file` with an `old_string` of `## Nowhere` forever (every result is an error); never emits a final message. |
| `verify_two_pass.json` | agent + grader | Agent produces the `review_clean` draft; grader pass 1: completeness pass; clarity fail, gap `each ambiguity bullet is missing the required indented 'Resolved by:' line`; depth fail, gap `each ambiguity bullet is missing the required indented 'Edge case:' line`; agent then edits Ambiguities so each of the three bullets gains `  Resolved by: …` and `  Edge case: …` lines (authored text); grader pass 2: all three pass, `satisfied`. |
| `verify_exhausted.json` | agent + grader | Agent produces the draft and, on every feedback, re-edits without adding the labelled lines; grader returns `needs_revision` on every pass. |
| `verify_grader_error.json` | agent + grader | Agent produces the draft; the grader script raises on its first call. |
| `verify_escape.json` | agent | Agent attempts `read_file` on `/../.env` and `../.env`, `write_file` on `/memories/AGENTS.md`, `edit_file` on `/memories/AGENTS.md`, then completes the `review_clean` sequence. |
| `batch_v1/01..05.json` | agent + grader | One script per fixture document, selected by the document's two-digit prefix (see `scripted_model.py`). First-attempt grading: docs 01–04 pass completeness and fail clarity + depth with gaps quoting the missing labels (each doc's gap wording differs slightly — e.g. doc 02 says `lacks the required indented "Resolved by:" and "Edge case:" lines` — so position, not text, must group them); doc 05 passes all three on the first attempt. Doc 04's agent additionally makes one `edit_file` call with a non-unique `old_string` (error) and recovers by `read_file` then a corrected edit — the one-off observation. Docs 01–04 pass on their second attempt. |
| `batch_v1_grader_error/` | agent + grader | As `batch_v1`, except doc 03's grader raises on its first call. |
| `analyst_v1.json` | analyst | Calls `read_file /v1/summary.json`, `glob /v1/run_*.json`, `read_file` on each run, `read_file /v1/AGENTS.md`, `write_file /proposal.md` (a markdown proposal with headings Summary signal, Current instruction gap, Evidence across runs, Proposed insertion, Rejected observations), then returns the structured change: `target: prompt`, `issue: Ambiguity bullets quote the clause and give a reason but never say what would resolve the ambiguity or what breaks if it stays unresolved, so clarity and depth fail on the first attempt.`, `section: ### Ambiguities`, `recurrence: 4/5 runs: 01_inventory_restock, 02_data_export, 03_session_timeout, 04_invoice_reminders`, four `evidence` strings each a verbatim gap from those runs, `change` = exactly five lines with no leading or trailing blank line: one sentence instructing that every ambiguity bullet carries two additional indented labelled lines after `Reason:`, then a fenced block — opening fence, `  Resolved by: <what settles it>`, `  Edge case: <what breaks if unresolved>`, closing fence (this is the text whose application yields `agents_v2_expected.md`), `rejected` = one entry about run 04's single edit-file error. |
| `analyst_bad_write.json` | analyst | As `analyst_v1` but first attempts `write_file /v1/summary.json` with the body `{}`. |
| `analyst_tool_target.json` | analyst | Returns a change with `target: tool`, `section: ""`, `change: Rename the fetch tool.`. |
| `batch_v2/01..05.json` | agent + grader | Every doc's first draft already carries both labelled lines under every ambiguity; every grader pass 1 is `satisfied`. |

Derived first-attempt facts for `batch_v1`: completeness 5/5, clarity 1/5, depth 1/5, `revisions_needed` 4, grading passes total 9. For `batch_v2`: 5/5 on all three, `revisions_needed` 0, passes total 5.

**`fixtures/summaries/`** — three authored pairs of §3.4 summaries (`before`, `after`; each with `runs: 5`, `graded: 5`, `grader_errors: 0`, the five document stems, label `a`/`b`, model `authored`) for AC29: `regression.json` — before completeness 5/5, clarity 5/5, depth 5/5, `revisions_needed` 0; after completeness **4/5**, clarity 5/5, depth 5/5, `revisions_needed` 1. `partial.json` — before completeness 5/5, clarity 1/5, depth 1/5, `revisions_needed` 4; after completeness 5/5, clarity **3/5**, depth 3/5, `revisions_needed` **2** (still needed). `no_effect.json` — `before` and `after` identical: completeness 5/5, clarity 3/5, depth 3/5, `revisions_needed` **2** — nonzero on purpose, since an identical pair with zero revisions would be `success` under R22, not `no effect`.

**Event-store seed** (fresh initialization): one requirement page `page-req-inventory` titled `Inventory Restock Alerts — Requirements`, version 1, author `Dana (Product Manager)`, body = the `INV-301` clauses; one ticket `INV-301`, status `Open`, linked to that page, assignee `Jordan (Eng Lead)`; an empty runs list. The fixed people list: `Dana (Product Manager)`, `Jordan (Eng Lead)`, `Priya (QA Lead)`, `Sam (Backend Engineer)`, `Morgan (Frontend Engineer)`. Bot author: `Requirements Analysis Agent (bot)`. New tracker-created keys: `REQ-<max numeric suffix across all tickets + 1>`, `REQ-100` when there are none.

### 5.2 Criteria

`offline` runs with the scripted model and no key; `live` needs `OPENAI_API_KEY` and is excluded from the offline run. Every AC traces to a rule; every rule has ≥ 1 AC.

| AC | Tag | Rule / row | Given | When | Then |
|---|---|---|---|---|---|
| AC1 | offline | R12; L4, RR1, D3 (existence) | a fresh checkout, `fixtures/` present | each loop (review, verification, automation, batch, analyst) is constructed with a scripted model object, with the verification loop given a **distinct** grader model object | construction succeeds with no key in the environment; the loop package's source contains no literal matching `gpt-`; the grader's calls are served by the grader object and the agent's by the agent object (call counts > 0 on each after AC8) |
| AC2 | offline | R1 | `review_retry.json`, fetch tool set to 2 simulated failures, ticket `INV-301` | the review loop runs | trace steps 1–6 are three `fetch_requirement` model/tool pairs; tool rows 2 and 4 have details beginning `Error fetching ticket` containing `503 Service Unavailable` and `timed out after 10s` respectively; tool row 6's detail contains `REQUIREMENT: Inventory Restock Alerts`; the report is complete |
| AC3 | offline | R1; L2 invariant | the fetch tool, no simulated failures | called with `ZZZ-999`; and separately a review run starts on `INV-301` | the result is a string beginning `Error fetching ticket` containing `ZZZ-999`, no exception; the run's first message contains `INV-301` and does not contain the word `monitored` |
| AC4 | offline | R2, R5 | `review_clean.json`, cap 12 | the review loop runs | exactly 6 tool rows, in order labelled `fetch_requirement`, `write_file: Confirmed Facts`, `edit_file: Ambiguities`, `edit_file: Clarification Questions`, `edit_file: Assumptions`, `edit_file: Summary`; `turns == 7`; `stage_order == [Confirmed Facts, Ambiguities, Clarification Questions, Assumptions, Summary]`; last action `Finishes the review`; every `detail` ≤ 221 characters |
| AC5 | offline | R2, R3 | the file written in AC4 | parsed | the first line is `# Requirements Analysis`; headings appear once each in order; counts `{Confirmed Facts: 3, Ambiguities: 3, Clarification Questions: 3, Assumptions: 2}`; `summary_words == 25`; complete |
| AC6 | offline | R3 | three authored texts: (a) a complete report with `## Assumptions` twice; (b) one with an empty Clarification Questions section; (c) one whose Summary is `Two sentences. Here.` | the completeness check runs | (a) and (b) are incomplete; (c) is complete, `Summary` is absent from the counts dict and `summary_words == 3` |
| AC7 | offline | R4 | `review_never_finishes.json`, cap 12 | the review loop runs | no exception; `turns == 12`; last action `Stops: turn limit of 12 reached`; report incomplete |
| AC8 | offline | R6; L3, D2 invariants | `verify_two_pass.json`, `fixtures/rubric.md`, budget 3, cap 40 | the verification loop runs on `INV-301` | `grading` has 2 passes; pass 1 `needs_revision` with criteria `[completeness: true, clarity: false, depth: false]`, both failing gaps non-empty and containing `Resolved by:` / `Edge case:` respectively; pass 1's `analysis_markdown` contains no `Resolved by:`; pass 2 `satisfied`, all true; `status == satisfied`; the final file has an indented `Resolved by:` and `Edge case:` line under each of the 3 ambiguity bullets |
| AC9 | offline | R6 (degenerate bound) | `review_clean.json`, budget 0 | the loop runs | zero grading passes; behavior identical to AC4 |
| AC10 | offline | R6, R8; D5 invariant | `verify_exhausted.json`, budget 3; and `verify_grader_error.json` | each runs | exhausted: 4 grading passes, every one `needs_revision`, `status == max_iterations_reached`; grader error: a pass with `result == grader_error` and `criteria == []`, the run returns a record |
| AC11 | offline | R7 | the verification loop as built | its grader configuration is inspected | the grader's tools are exactly `[read_file]`; its instructions contain `read_file`, `/analysis.md`, `line number`, `verbatim`, `satisfied`, `needs_revision`, `failed`, and `untrusted` |
| AC12 | offline | R9; L5 invariant | `verify_escape.json` | the run executes | all four escape/write attempts return error results; `/memories/AGENTS.md` is byte-identical before and after; no file outside the workspace root was read or written; the run still completes |
| AC13 | offline | R10 | an empty workspace directory | the agent is built against it | an exception is raised whose message contains `memories/AGENTS.md` |
| AC14 | offline | R9; D1 invariant | `review_clean.json` | the run record is saved to JSON | `instructions` equals the bytes of `fixtures/agents_v1.md` |
| AC15 | offline | R11 | a workspace whose `/analysis.md` contains `STALE`, run on `review_clean.json`; the same verification agent run twice on `verify_two_pass.json`; two automation triggers back to back, both served by `verify_two_pass.json` | each case runs | final report contains no `STALE`; second run's `grading` has 2 passes, not 4; the two automation runs used different workspace paths and neither path exists afterwards |
| AC16 | offline | R14; RR2 (existence) | no `data/` directory | the event app initializes | `data/pages.json` holds exactly the seed page (id `page-req-inventory`, kind `requirement`, 1 version, `linked_ticket: null`); `data/tickets.json` holds exactly `INV-301` (`Open`, linked to it, `last_analyzed_version: null`); `data/analysis_runs.json == []`; the app serves `/`, `/jira`, `/confluence` with HTTP 200 |
| AC17 | offline | R14, R15; D4, D5 invariants | the seeded app, `verify_two_pass.json` | `POST /jira/tickets` with title, `linked_page_id = page-req-inventory`, assignee `Priya (QA Lead)` | redirect to `/jira/REQ-302`; ticket `REQ-302` has `status: Analysis Ready`, `last_analyzed_version: 1`, `last_run_id` 8 hex chars; page `page-analysis-req-302` exists, kind `analysis_report`, title `Analysis Report — REQ-302`, 1 version by the bot author whose body starts with a banner containing `REQ-302`, `version 1`, `satisfied`, `2 grading pass`; one run record with `status: satisfied`, `requirement_version: 1`, counts for the four list sections, and a trace whose `fetch_requirement` tool row's detail contains `REQUIREMENT: Inventory Restock Alerts` and `Managers must be alerted when stock runs low.` (the registered version-1 body, R14); one bot comment on the ticket containing `satisfied` and `version 1` |
| AC18 | offline | R14, R16 | the state after AC17 — two tickets not `Done`, both linked to `page-req-inventory`: `INV-301` (`Open`) and `REQ-302` (`Analysis Ready`); every triggered run served by `verify_two_pass.json` | (1) `POST /confluence/page-req-inventory/save` with the version-1 body whose second clause now reads `Managers must be alerted within five minutes when stock runs low.`; (2) `POST /jira/REQ-302/close`; (3) save the page again (any further change) | (1) exactly two new runs, one per linked ticket not `Done`, each with `requirement_version == 2` and a `fetch_requirement` trace row whose detail contains `within five minutes` (the registered current version, R14), and the flash names both `REQ-302` and `INV-301`; `page-analysis-req-302` has 2 versions and `REQ-302.last_analyzed_version == 2`; `INV-301` is now `Analysis Ready` with `last_analyzed_version == 2` and a new page `page-analysis-inv-301` with 1 version; (2) `REQ-302` status `Done`; (3) exactly one further run, for `INV-301` only (`page-analysis-inv-301` now has 2 versions); `page-analysis-req-302` still has 2 versions and the flash does not name `REQ-302`; at no point did automation set `Done` |
| AC19 | offline | R15; RR2 invariant | the state after AC18 | the requirement page is read | it has exactly 3 versions, all human-authored (none by the bot); every report version's author is the bot identity |
| AC20 | offline | R17 | the state after AC18 | `GET /jira/REQ-302`; `GET /confluence/page-analysis-req-302/compare?a=1&b=2` | the ticket page contains `What changed since the previous run`, a row per list section with previous and latest counts, and a `Run history` with 2 rows; the compare page contains `--- version 1`, `+++ version 2`, and the two runs' status and counts |
| AC21 | offline | R18 (existence + summary), R2 | `fixtures/requirements/`, `agents_v1.md`, `batch_v1/` | the batch runs with label `v1` | `run_history/v1/` contains `AGENTS.md` (== `agents_v1.md`), `run_01_01_inventory_restock.json` … `run_05_05_search_autocomplete.json`, `summary.json`, `ws_01/`…`ws_05/`; each run JSON has the §3.4 keys; `summary.json` has exactly the §3.4 keys, with `model` beginning `scripted-replay/` and the other values `{label: v1, runs: 5, graded: 5, grader_errors: 0, first_attempt: {completeness: 5/5 1.0, clarity: 1/5 0.2, depth: 1/5 0.2}, revisions_needed: 4, documents: [the five stems]}`; doc 04's run record's `messages` contain an `edit_file` tool result that is an error (non-unique `old_string`), followed by a `read_file` result and then a successful `edit_file` result (R2, CTX-B10) |
| AC22 | offline | R18, R8 | `batch_v1_grader_error/` | the batch runs as `v1e` | `graded == 4`, `grader_errors == 1`, every criterion `total == 4`, `clarity.passed == 1`; doc 03's run has a `grader_error` pass and an empty first-pass failure list; doc 02's criterion is counted under `clarity` despite its differently worded gap |
| AC23 | offline | R19; D6 invariant | `run_history/v1/` from AC21, `analyst_v1.json` | the analyst runs on `v1` | `run_history/proposal.md` (the analyst's own file) exists, and the harness-written `run_history/proposal_v1.md` (byte-equal to it) and `run_history/proposal_v1.json` (R19) exist; the returned change and the parsed `proposal_v1.json` both validate against §3.5; `target == prompt`, `section == ### Ambiguities`, `evidence` has 4 entries each found verbatim in a `v1` run's grading gaps, `recurrence` contains `4/5`, `rejected` has 1 entry mentioning run 04's edit error |
| AC24 | offline | R19; D6 invariant | `run_history/v1/` from AC21, `analyst_bad_write.json` | the analyst runs on `v1` | the write to `/v1/summary.json` returns an error and the file is unchanged; `/proposal.md` is written; the analyst's tools are exactly `ls, read_file, glob, grep, write_file` |
| AC25 | offline | R20 | the AC23 change | apply is invoked without approval; then with approval | without: refused (error) and `agents_v1.md` content unchanged; with: applied |
| AC26 | offline | R21 | the AC23 change, `agents_v1.md` text | apply with approval | the result equals `fixtures/agents_v2_expected.md` byte for byte; a line diff against v1 shows exactly six added lines (the five `change` lines and one blank line) and no removals |
| AC27 | offline | R21 | `analyst_tool_target.json`'s change; and a prompt change with `section: ### Nonexistent` | apply with approval | each raises an error — the first mentioning `tool`, the second mentioning `### Nonexistent`; the file is unchanged |
| AC28 | offline | R22; L3 default | the applied v2 instruction text, `batch_v2/` | the batch runs as `v2`; `compare(v1, v2)` | v2 summary: all criteria 5/5, `revisions_needed == 0`; comparison `verdict == success`, `criteria == {completeness: [5,5], clarity: [1,5], depth: [1,5]}`, `improved == [clarity, depth]`, `regressed == []`, `revisions_needed == [4, 0]`, `attempts == [9, 5]`, both token pairs positive integers |
| AC29 | offline | R22 | the three pairs in `fixtures/summaries/`: (a) `regression.json` (completeness drops 5→4); (b) `partial.json` (clarity rises 1→3, `revisions_needed` still 2); (c) `no_effect.json` (identical summaries, `revisions_needed` 2 on both sides) | each pair is compared | verdicts `regression`, `partial`, `no effect` respectively; (a) lists `completeness` in `regressed`; (c) has empty `improved` and `regressed` |
| AC30 | offline | R13 | the repository | inspected; tracing status queried with `LANGSMITH_TRACING` unset | `.env.example` exists with placeholder values for `OPENAI_API_KEY`, `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`; `.gitignore` lists `.env`; no tracked file contains a string matching `sk-[A-Za-z0-9_-]{20,}`; the status reports tracing off |
| AC31 | live | L4 invariant, D3, R6 | `OPENAI_API_KEY` set, row L4's models, `INV-301` | the verification loop runs with budget 3 | `status == satisfied`; `turns ≤ 40`; the final report has `Resolved by:` and `Edge case:` lines under every ambiguity bullet |
| AC32 | live | R7 | a planted `/analysis.md` whose three ambiguity bullets carry only `Reason:` lines; a second one carrying all three lines | the live grader evaluates each against `fixtures/rubric.md` | first: `clarity` and `depth` fail with gaps naming the missing labels, `completeness` is not asserted; second: all three pass |
| AC33 | live | R18–R22; D6, L3 | the live model, `fixtures/requirements/`, `agents_v1.md` | batch `v1_live` → analyst → human-approved apply → batch `v2_live` → compare | the change has `target == prompt` and `section == ### Ambiguities`; `verdict != regression`; `v2_live` `revisions_needed ≤ v1_live` |

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the offline suite (`pytest -m "not live"`) after every change to loop code, fixtures excluded; report per-AC evidence (§7).
- Keep the instruction file write-denied to the agent (R9) and the analyst write-denied everywhere except `/proposal.md` (R19), by permission configuration, in every loop you construct.
- Record every run's instruction text, every grading pass and the file as each pass saw it (R9, R18).
- Read secrets from `.env` only (R13).
- Snapshot the instruction file into each batch directory before the batch starts (R18).

**Ask First** — derived by walking the course's spoken trade-offs (CTX-C); each either forces rework (a) or changes a behavior guarantee without failing a criterion (b):
- Changing **MAX_RUBRIC_ITERATIONS** (R6), above all setting it to 0 — (b): removes the verification guarantee from triggered runs while the offline suite still passes when run with budget 3.
- Assigning a **separate grader model** or changing any role's model (D3, L4) — (b) and (a): verdicts shift silently; every existing batch becomes incomparable, so re-run the baseline batch.
- Changing the **grader type** (D2) — to deterministic checks or a human grader — (b) and (a): the definition of "done" changes with no failing test (an LLM judge and a deterministic check can disagree on the same file), and every existing batch summary becomes incomparable.
- Editing the **rubric text** or the criterion order (L3, R6) — (a): all batch summaries become incomparable; (b) the grader's definition of "done" changes.
- Editing the **instruction file outside the learning loop** (R18–R21) — (a): a batch's `AGENTS.md` snapshot no longer matches the baseline; before/after verdicts become meaningless.
- **Auto-applying** a proposal, or applying a non-`prompt` target (R20, R21, D6) — (b): the human-review guarantee disappears with no failing test.
- **Dropping the grader under the trigger** or adding a **scheduled trigger** (D5, D4) — (b): runs complete without grading, or appear on a schedule nobody asked for.
- Moving instructions into a **skills directory** (D1) — (a): the learning loop's edit target and every snapshot change shape.
- Changing the **turn caps** (R4) — (b): a lower cap silently truncates reviews on long documents while fixtures still pass.
- Switching **simulated fetch failures** on for live or batch runs, or on the trigger path (R1, R14, R18) — (b): adds turns and cost, and may push a run into the cap.
- Enabling **LangSmith tracing** or any external telemetry (R13, Not Included #8) — sends run content off-machine.
- Replacing the **flat-JSON event store** or the **simulated tracker** with a real one (RR2) — (a): every trigger criterion becomes `live`.

**Never**
- Invent provenance: never attribute a value, a quotation or a verdict to the course or to a run that did not produce it; never fabricate `evidence` strings.
- Let the grader pass a criterion it cannot quote (R7), or let the agent answer when the fetch failed (R1).
- Modify fixtures, replay scripts or `agents_v2_expected.md` to make a test pass.
- Commit `.env`, a key, or any live run's raw output containing a key.
- Let any automated path set a ticket to `Done` (R16), edit a requirement page (R15), or write into batch evidence (R19).
- Hardcode a model name in loop code (R12) or bake "current best" model names into the spec's defaults.

## 7. Test Plan & Self-Verification

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e . && pip install pytest
cp .env.example .env                      # placeholders only; offline needs no key
pytest -m "not live" -v                   # offline oracle: AC1–AC30, must all pass
pytest -m live -v                         # only with OPENAI_API_KEY set: AC31–AC33
python -m app                             # event layer on http://localhost:5050 (live model)
python -m batch --label v1                # batch over fixtures/requirements/ (live model)
python -m analyst --label v1              # proposal for a batch (live model)
python -m analyst --compare v1 v2         # verdict between two batches
```

Mark every test with `offline` or `live` (`pytest.mark.live`); the offline suite must not import anything that needs a key. Scripted-model tests must run the real file tools, permissions and middleware — a test that stubs the loop itself proves nothing (row RR1).

**Reporting duty.** The building agent MUST report results per acceptance criterion — `AC1 … AC33`, each with cited evidence: the pytest node id and its pass/fail line, the path of any artifact asserted (e.g. `run_history/v1/summary.json`, `data/tickets.json`), and the exact assertion for byte-equality checks (AC14, AC26). `live` criteria not run are reported as **not run (no key)**, never as passed. "Should pass" / "looks correct" / "expected to work" are treated as failures — they mean the test was not run.

**Closing instruction.** When the offline suite passes, conclude with an infra/structure diagram of the built app — the four nested loops, the stores, the file layout and which process owns each — and end with the phrase **"This is the infra/structure diagram of this app"**.

## Course Context Pack (embedded — agent-readable)

Concepts only; no course code. The concepts in CTX-A…CTX-C are durable; only the names in CTX-D are perishable. Nothing here requires platform access.

### CTX-A. The pattern

Four loops, each wrapping the previous ("Russian-doll" nesting is the course's picture, but every loop is composable — row D5):

1. **Fetch** — the agent is told an identifier, never the document; a tool fetches it and can fail transiently, so the loop's first behavior is retry-on-error. *Exists* so the agent behaves identically against a real tracker and a seeded fake.
2. **Agent loop** (model ↔ tools, repeat until done) — the model receives context, calls tools, observes results and continues until it decides it is finished; a model-call cap exists only for the case where that decision never comes. The deliverable is a **file** built stage by stage in a scoped filesystem; standing instructions come from a file loaded every run. *Exists* to do the work; what you engineer here is model choice, tool choice and tool descriptions.
3. **Verification loop** (agent run ↔ grader) — a grader scores the finished artifact against explicit pass/fail criteria, sends specific feedback back on failure, and the agent revises; bounded by an iteration budget. *Exists* because "finished" is not "good enough", and because explicit criteria let a cheaper model handle harder work.
4. **Event-driven loop** (event ↔ execution) — something in a real system (a ticket created, a page edited, a schedule, a webhook) starts the nested loops; the result is written back to that system as an agent-owned artifact; a human still approves/closes. *Exists* so the agent gets used where the work happens and the system improves with each run.
5. **Learning (hill-climbing) loop** (traces ↔ harness) — a batch of graded runs is recorded in full; an analyst agent reads the batch, finds a correction that recurs across most runs, proposes one literal change to the harness; a human approves; the change is applied mechanically; a second batch measures whether first-attempt pass rates rose. *Exists* because agents are non-deterministic — "the story is in the traces" — and a per-run fix is forgotten tomorrow unless it is ported back into the harness.

Human oversight placements the course names, one per loop: approve sensitive tool calls; a human as grader; approve artifacts before delivery; review harness changes before deployment.

### CTX-B. Failure-mode catalog

- **B1 — Transient fetch failure.** Symptom: the external lookup returns an error ("service unavailable", "timed out"). Cause: real trackers are sometimes unreachable. Fix: the tool returns the error as a result string and the instructions say to repeat the identical call until it succeeds; the trace shows the repeated calls. Enforced by R1, AC2–AC3.
- **B2 — First draft fails clarity and depth.** Symptom: ambiguity bullets quote the clause and give a reason but say nothing about what would resolve it or what breaks if it isn't; the grader fails two of three criteria with gaps naming the missing labelled lines; the second attempt passes. Cause: the instruction file never asked for those lines — a systematic instruction gap, not a per-document problem. Fix: within a run, the grader's feedback; across runs, the learning loop's insertion into the instruction file. Enforced by R6, R21–R22, AC8, AC21, AC26, AC28.
- **B3 — Grader judges by resemblance.** Symptom: the grader passes criteria the file does not satisfy. Cause: it is handed the conversation transcript, which can read as if the work was done; it judges from the transcript, or from how the file "looks". Fix: give the grader a read-only file tool, require it to read the deliverable, quote verbatim with a line number before passing anything, apply labels literally, check every item. Enforced by R7, AC11, AC32.
- **B4 — Missing instruction file is silently ignored.** Symptom: a plausible but bad review. Cause: the harness treats a missing memory file as "no memory" without warning, so the agent runs on the system prompt alone. Fix: fail loudly at build time when the file is absent. Enforced by R10, AC13.
- **B5 — Stale state between runs.** Symptom: the agent reads a finished report left by the previous run and skips stages; a second run's grading passes pile onto the first's; two tickets analyzed back to back see each other's file. Fix: delete the report before a run, clear the pass list, give every triggered/batch run its own workspace seeded from the instruction snapshot; keep the agent's filesystem root-scoped so it cannot reach the repository's secrets. Enforced by R11, L5, AC12, AC15.
- **B6 — The agent could edit its own instructions.** Symptom/cause: the instruction file sits in the same writable filesystem as the report and the agent holds an edit tool. Fix: deny writes to the instruction directory by permission, not by asking nicely; changes are proposed and applied from outside. Enforced by R9, AC12.
- **B7 — A one-off becomes a "pattern"; the analyst edits its evidence.** Symptom: a change proposed from one run's quirk (a duplicate heading, one failed edit); or traces altered by the thing reasoning over them. Fix: the analyst must quote evidence, state recurrence, and park single occurrences under `rejected`; its filesystem write permission covers only its proposal file. Enforced by R19, AC23–AC24.
- **B8 — Grader errors counted as passes.** Symptom: a batch looks better than it is. Cause: a grader exception yields a pass with no criteria; naive counting treats "no failures" as "passed". Fix: a run without criteria is ungraded, excluded from denominators, and reported as an error count. Enforced by R8, R18, AC22.
- **B9 — The agent closes its own work / edits the source.** Fix: the requirement page is the source of truth the agent only reads; the report is a separate agent-authored page with its own version history; only a human marks a ticket Done; re-triggers apply only to tickets not yet Done. Enforced by R14–R16, AC17–AC19.
- **B10 — Non-unique edit target; duplicated headings.** Symptom: an edit tool call fails because its target string occurs more than once; some drafts end up with two `## Assumptions` headings. Fix: the tool rejects the edit, the agent re-reads and retries; completeness requires each heading exactly once; this is also the course's canonical *rejected* observation in the learning loop. Enforced by R2–R3, R19, AC6, AC21, AC23.
- **B11 — Counts look alike, content changed completely.** Symptom: a re-run after a requirement edit shows roughly the same bullet counts. Fix: show the counts table and the full text diff together, never one alone. Enforced by R17, AC20.
- **B12 — Finished and exhausted print the same.** Symptom: a run that hit its model-call cap reads like a completed review. Fix: the trace's last step names the cap when the report is incomplete; a verification run exposes `max_iterations_reached` distinctly from `satisfied` even though its last grading pass still says `needs_revision`. Enforced by R4, R8, AC7, AC10.

### CTX-C. Decision background (reference only; decisions are made in the Ledger)

**How to read the provenance notes** (the vocabulary used in the Ledger and §4): (i) *Litmus: row / bake-in / lever* records why a course-argued subject became a Ledger row, a business rule, or a body value — **row** when the course showed the alternative working as an acceptable choice; **bake-in** when it showed the alternative only failing or warned against it (the taught side becomes a rule, the warned side stays narrative); **lever** when the two sides differ only in a number. (ii) A *lever value* is picked by three branches in order: (1) the value the lesson's narration states aloud when it introduces the concept; (2) failing that, the end-to-end application's config; (3) failing that, the value used most often across the materials, earliest-taught on ties — each lever names the branch that decided it. (iii) A *post-build lever* is a value you may change after the build without re-asking at the §0 gate; every one is listed in §6 Ask First. (iv) *Realization tiers* rank how light a realization is: tier 1 ships with the language's standard distribution; tier 2 is an embedded library (package install, no separate process); tier 3 is a locally served component (own process, still credential-free); anything needing a key, paid account, admin setup or special hardware is *heavy*. (v) *Stakes* is the structural test applied to a contradiction or an argued subject: would choosing the other side up front change a box, an arrow, an owner or a guarantee in the architecture — or only a number inside a box? Only the former has stakes and can earn a Ledger row; a value-only difference is a lever. (vi) A Default cell's *Branch:* names which precedence branch chose the default: for the project row, the course's example scenario shape (re-expressed on the authored fixture corpus) or, failing a usable example, a generic minimal instantiation; for a realization row, the lightest self-contained tier that preserves the invariant, or — when the course's realization is keyed and the only carrier of a taught behavior — an honestly-labelled stand-in with the course's realization kept as an Option. (vii) A *substitution row* is a row whose Default is not the course's own realization (RR1 here): the course's realization stays in its Options tagged "(course default)", and the §0 checklist marks the row `≠ course choice`.

- **C1 — The course's running example beyond the build.** Lesson 2 illustrates every loop with a docs-writer agent: request → sandbox tools (clone/read/write) → pull request; grader checks "links resolve, CI passes"; trigger is a Slack message in a channel; the learning agent ("Engine") files prompt/tool changes from traces. It is the shape to imitate when swapping the project (→ Ledger L1).
- **C2 — Why the deliverable is a file and the document is fetched.** A file "is something you can open rather than something you have to parse out of a message", and stage-by-stage edits make the loop visible one turn per section. The agent is built with no document; seeding the store at run time keeps its turn-by-turn behavior identical to a real lookup. Litmus: no two-sided argument in the materials → business rules R1–R2, not rows (→ L2).
- **C3 — Instruction placement (→ D1).** Three channels: the build-time system prompt (every call), a memory file loaded every run ("what is always true… costs context on every call, so it should stay short"), and skills with progressive disclosure (only name + description up front; the body read when it applies, "so twenty skills cost twenty lines of context"). The course notes coding assistants organize instructions the same way. The review agent uses the memory file alone because the learning loop needs one editable, recorded file; the primer agent shows skills working (Lesson 3).
- **C4 — Model per role (→ D3, L4).** "Match the model intelligence to the complexity of the incoming task to optimize cost" (Lesson 2); verification "can make cheaper models viable for harder tasks" (slide 2.6); the course ran agent and grader on the same model and called a separate grader model "a common production choice" (Lesson 5); the analyst ran on a more capable model because reading several full traces is "the one job the cheaper model does unreliably". Course-era prices put the analyst's model at ~6–7× the review model per token — perishable, see CTX-D.
- **C5 — Grader type (→ D2).** "Graders can either be deterministic or agentic (LLM as a judge is a classic example)" (slide 2.6, narrated). The course's own grader is an LLM judge whose default library prompt was restated and extended (B3) because passing a custom prompt replaces the default. Course-provided grader facts: result enum `satisfied / needs_revision / failed`; an extra `grader_error` is recorded by the loop when the grader throws; a checkpointer was attached "to match the shape the docs show" and is not required for revisions.
- **C6 — Trigger kind and nesting (→ D4, D5).** Triggers "can be scheduled, or ad hoc and event-driven"; examples: a morning calendar summary; an email-triggered assistant; a Slack channel. Nesting is composable — the verification loop is optional under a trigger. The course built an event trigger (ticket created / linked page saved) wrapping verification + agent, with the loop's status, turns, counts, trace and grading passes stored per run.
- **C7 — Learning-loop target and human review (→ D6, R20).** The harness has four improvable parts (prompt, tools, grader, configuration); the course scoped analysis to the prompt "because that is what the current evidence implicates", kept the other targets expressible, and applied prompt changes with plain string insertion "so deciding where it lands is not also a model call". Lesson 2 lists tool descriptions, prompts, skills and memory (preference consolidation) as targets and warns it is "hard to have confidence merging changes to your core harness if you don't have good evals" — the before/after batch is that eval. Litmus for human approval: the course never shows unreviewed application working → bake-in.
- **C8 — The closing demo (→ L3).** Baseline batch: completeness passed on most/all runs, clarity and depth failed on most ("four out of five" narrated; 5/5 in the committed batch); one proposal; re-batch: 5/5 on all three criteria, zero revisions. The spec's fixture batch reproduces the 4-of-5 narrated shape.
- **C9 — Replay versus live (→ RR1).** The course's notebooks carried a `USE_LIVE_LLM` switch: off, they replayed committed traces and batches and needed no key; on, they called the model. Replaying a trace shows results but exercises no loop machinery; the spec's scripted model keeps the machinery live and only fakes the model's decisions.
- **C10 — Event-system realization (→ RR2).** The course simulated both tools with one small web app over three JSON lists "so this lesson runs with no Atlassian account and no API tokens", and named the real integration as the next step: swap the store lookups for the REST APIs and call the automation function from a webhook.
- **C11 — Levers and their provenance.** Rubric iteration budget: 3 (Lesson 5 narration/config; batch runner) vs 2 (trigger app) → 3 by the narrated-value branch. Simulated fetch failures: 2 (Lesson 4 narration, notebook tool table, prebaked trace) vs 0 (helper constant: "a clean fetch") → 2 for the retry fixture, 0 in batches ("only adds turns and noise") and 0 on the trigger path (the helper default; R1, R14). Turn caps: 12 (single review), 40 (with grader; trigger; batch; analyst), 30 (primer). Trace detail truncation: 220 characters (helper module `deepagent_helpers.py`, `_truncate` default `limit=220`). Token-estimate overhead constant: 120 (helper module `hill_climbing.py`, the `+ 120` literal in `usage()`).
- **C12 — Naming drift to expect in course artifacts.** The fetch tool is `fetch_requirement` in the shipped instruction file and `fetch_requirement_from_jira` in the two committed batch snapshots and on slide 3.5; the memory file is `AGENTS.md` in code and "Agent.md" on slide 3.4 — code wins, recorded here. The fourth loop is called hill-climbing, learning and self-improvement interchangeably; the third loop is once labelled "application loop" (slide 2.12). The course's own requirement wording differs between slides and narration — irrelevant here, since no course data is used.

### CTX-D. Perishable assumptions

Treat these as **search keywords against current docs, not guaranteed imports**; the concepts above are durable, these names are not.

- Harness: `deepagents` (`create_deep_agent`, `FilesystemBackend(root_dir, virtual_mode=True)`, `FilesystemMiddleware`, `FilesystemPermission(operations, paths, mode)`, `RubricMiddleware(model, max_iterations, tools, system_prompt, on_evaluation)`, `memory=`, `skills=`, `permissions=`, `response_format=`, `checkpointer=`); grader response fields `result`, `explanation`, `criteria[{name, passed, gap}]`; loop state key `_rubric_status`; file tools `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`, `delete`.
- Framework: `langchain` `create_agent`; `langchain.agents.middleware.ModelCallLimitMiddleware(run_limit, exit_behavior="end")`; middleware hook names `before_agent/after_agent`, `before_model/after_model`, `wrap_model_call/wrap_tool_call` (slide 3.3); `langchain.tools.tool`; `langgraph.checkpoint.memory.InMemorySaver`; stream mode `updates`; run `config` keys `run_name`, `tags`, `configurable.thread_id`.
- Models and provider strings: `openai:gpt-5.4-mini`, `openai:gpt-5.5` (course era); provider-prefix syntax `provider:model`. **Request-parameter compatibility:** the course's helper notes message content is "a list of content blocks on current models, and a plain string on older ones" — normalize both; verify which sampling parameters (e.g. `temperature`) the chosen family accepts before the first live run.
- Prices used by the course's cost estimate (USD per million tokens, input/output): 5.00/30.00 for the analysis model, 0.75/4.50 for the review model — already stale; excluded from scope (§1 #10).
- Tokenizer: `tiktoken` encoding `o200k_base`.
- Tracing: `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` (older aliases `LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`).
- Web: `flask` (`render_template`, `flash`, `redirect`, `url_for`), default port 5050.

### CTX-E. Provenance map

Lesson numbering follows the transcripts (the repo folders run one lower for each notebook; the README uses a third numbering). Nothing in this spec requires platform access.

| Transcript lesson | Contributed |
|---|---|
| 1 — Introduction | CTX-A overview; the requirement-review agent as the course's running project (L1). |
| 2 — Overview of Loop Engineering | CTX-A stages 2–5 and human-oversight placements; C1, C4, C6, C7; rows D2–D6 arguments; Ask-First list. Slides 2.1–2.13 read (all narrated except the title card); slide 2.6 supplied the deterministic-vs-agentic grader statement, slide 2.8 the webhook trigger kind, slide 2.12 the oversight wording. |
| 3 — Deep Agent Primer | C3 (instruction channels, progressive disclosure), L5 root-scoping, turn cap 30, CTX-D harness/middleware names. Slides 3.1–3.5 read (3.2–3.5 narrated); slide 3.3 supplied the hook names; slides 3.4/3.5 are deck-sourced for "Agent.md" / `fetch_requirement_from_jira` naming (C12). |
| 4 — Agent Loop | R1–R5, B1, B4–B6, B10, B12; caps 12; retry narration (C11); report shape (§3.2). Slides 4.1–4.5 read (4.2–4.5 narrated). |
| 5 — Verification Loop | R6–R8, B2, B3, B5; budget 3 and cap 40 (C11); C4 (grader model), C5. Slides 5.1–5.4 read (5.2–5.4 narrated). |
| (no lesson) — event-driven app in the course repo | R14–R17, B9, B11, RR2, C10; budget 2 contradiction (C11); §3.7. Deck-only slides A.1–A.2 (Tall deck 15–16) read; they rank below the code and add nothing beyond slide 2.8. |
| 6 — Learning loop | R18–R22, B7, B8, D6, C7, C8, L3 default; §3.4–3.6. Slides 6.1–6.2 read (6.2 narrated). |
| 7 — Conclusion | Recap only. |

Slide conflicts recorded (not resolved silently): requirement wording (slides 4.4/5.4 vs Lesson 4 narration; code matches the slides) — unused; "Agent.md" (slide 3.4) vs `AGENTS.md` (code) — code wins; `gpt-5.5` in slide 3.2's generic example vs `gpt-5.4-mini` in the course's agent — code wins; two requirement placeholders on slide 6.2 vs five documents in the batch — code wins; an "Event driven loop" title card with no transcript lesson — sourced from Lesson 2 narration plus the repo app.

---

*Spec v1 · course: Loop Engineering with LangChain DeepAgents · learner project: `[project]` = Requirements Review Agent on the fixture corpus, the course-derived default · Living document: when the building agent produces something unexpected, add the missing constraint here and re-run.*
