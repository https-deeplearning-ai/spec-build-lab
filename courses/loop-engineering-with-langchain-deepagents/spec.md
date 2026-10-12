# Spec: Requirements Review Agent with Four Loops — Standalone Takeaway

> **What you're building:** a local requirements-review agent app with four loops around it — it reviews, gets graded, runs on events, learns. You create a ticket in the simulated tracker; the ticket flips to "Analysis Ready" and a report page appears listing the facts, the ambiguities (each with what would resolve it and what could go wrong), the questions and the assumptions. You then run five tickets as a batch, read the analyst's proposal, approve it, and watch the re-run pass every rubric criterion on the first attempt. Answering the gate's first question with the recommended baseline builds it end-to-end; the build is complete when the offline suite passes — an API key unlocks only the `live` tests and live use of the finished app.
>
> This file is self-contained: the Course Context Pack at the end replaces every external course reference, so nothing here requires access to the course, its notebooks, or its platform.
>
> `(CTX-X)` anchors mark course-derived knowledge. The Decision Ledger below holds every point where the build could diverge, each pinned to one course-derived default, so the spec builds as-is with no intake.
>
> Generated from the *Loop Engineering with LangChain DeepAgents* notebooks + transcripts + slides on 2026-10-13, guide @ 11b3673.

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

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option. Rows are grouped learner → design → realization (no row entered through the contradicted route; the mined contradictions all failed the stakes test and resolved as body levers, provenance notes, or — for the course's offline/live switch — by the realization row RR1, see CTX-C). Row ids: `L<n>` learner, `D<n>` design, `RR<n>` realization; business rules are `R<n>` and are never confused with rows.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L1 | learner | **Project** — what the four loops are built around. The Default is the course's *example realization* (a requirements-review agent on a ticket tracker) and is expected to be swapped when your project differs; the loops, not the review task, are what must survive. | — | A requirements-review agent: given a ticket id, it fetches the requirement text and writes a five-section analysis file (Confirmed Facts, Ambiguities, Clarification Questions, Assumptions, Summary); the four loops of §1 are built around it, on the synthetic fixture tickets of §5. Branch: course-example shape re-expressed on authored fixtures (the course's demo is a requirements reviewer over a simulated ticket tracker). | [project]: the requirements-review agent (course default); any other single-deliverable agent task whose output is a file a grader can read (a docs-writer that opens a pull request, a report generator, a code-change agent) | Swapping the task re-authors the instructions file, the rubric (row L3) and the fixtures; the loop machinery (grader, triggers, batch, analyst, apply, compare) is unchanged. | learner |
| L2 | learner | **Data / inputs** — where the requirement text lives and how the agent reaches it. | The agent is never handed the document: its opening message names only an identifier, and the text is obtained through a tool call that can return an error observation instead of a result. | A keyless in-process ticket store seeded from a JSON file of ticket-id → requirement-text pairs (§5 `fixtures/tickets.json`), fronted by one `fetch_requirement` tool. Branch: the course's own realization is already keyless (a fake tracker seeded from a JSON file), so it is reproduced as-is. | [data]: in-process JSON-seeded ticket store (course default); the simulated tracker's page store of the event loop (same shape, versioned pages; available only while row D1 keeps the event loop); a real issue tracker's REST API (heavy setup: account + API token; named by the course as the next step, never built) | A real tracker adds credentials and network failures that the simulated transient-failure demo (R4) stands in for; the agent's behavior does not change because it never sees which backend answered. | learner |
| L3 | learner | **Goal** — what "a good analysis" means. | Done is defined by a rubric of named pass/fail criteria evaluated over the finished file; every criterion must pass in the same grading pass; each failure carries a gap stating what is missing. | The three-criterion rubric of R11: *completeness* (every clause of the requirement is addressed), *clarity* (every Ambiguities bullet has an indented `Resolved by:` line), *depth* (every Ambiguities bullet has an indented `Edge case:` line). | [goal]: the three-criterion rubric (course default); any rubric of labelled pass/fail criteria over the output file (the course's own other example: links resolve and CI passes for a docs pull request) | Changing a criterion changes what the grader sends back and therefore what the learning loop diagnoses; the course's whole Lesson 6 result (first-attempt clarity/depth 0/5 → 5/5) is specific to these criteria. Rubric text is a §6 Ask-First item. | learner |
| L4 | learner | **Model / provider** for the three model roles (reviewer, grader, analyst). | Reviewer and grader: native tool calling. Analyst: schema-constrained (structured) output. | Reviewer and grader on the course's `openai:gpt-5.4-mini`; analyst on the course's `openai:gpt-5.5` (provider prefix `openai:` as the course wrote it). These are the course's own models, named as provenance; which model is current when you build is the gate-time "(Recommended)" judgment, not this cell's. | [model]: the course's models above (course default — heavy setup: provider API key, paid usage); any provider's tool-calling model for reviewer/grader and, for the analyst, a *capable* structured-output model (the course found its cheaper model unreliable at reading traces, so the analyst is not the place to economize); a separate (cheaper or stronger) grader model — the course used the same model for both and called a separate grader "a common production choice" (Lesson 5) | The course argues cost against capability: a cheaper model for simple tasks, a capable one for complex, and the verification loop as what makes a cheaper model viable on a hard task (Lesson 2); the analyst runs on the stronger model because reading five traces and finding what recurs is the job the cheaper model did unreliably (course README). Changing any role's model changes behavior no offline test sees — §6 Ask First. | learner |
| L5 | learner | **Environment** — where the loops run. | The agent's file tools reach only its own per-run workspace directory, which it sees as `/`; nothing above that root is reachable; its instructions file lives inside that root. | One local machine, Python ≥ 3.12, one virtual environment; per-run workspace directories on the local filesystem; the event loop's tracker simulation as a local web app on `localhost:5050` backed by three flat JSON files; secrets in a local `.env`. | [environment]: local machine as above (course default); a container or CI runner with the same layout; a hosted deployment of the same layout (the tracker simulation then needs a persistent volume for its three JSON files and the per-run workspaces) | Nothing in the pattern depends on where it runs, but the per-run workspace confinement is what keeps a run from reading a previous run's analysis or the repository's `.env` (R8); any environment must preserve it. | learner |
| L6 | learner | **Scope boundary** — at the gate, read the §1 "Not Included" list aloud *inside this question*, item by item with its handling tag, then ask whether anything should come back. | — | Keep as-is: every §1 exclusion stands and the full acceptance set is built. | keep the exclusions as-is (course default); bring an item back — name it from the §1 list (or add an exclusion of your own via free text, naming the acceptance criteria it retires) | Handling rules, applied by tag: `[restorable]` — additive and owned by no other row: build it on request; `[named, never built]` — the course mentioned it and built nothing: buildable, but this spec supplies no parameters and no acceptance criteria for it; `[owned by row X]` — defer to that row, never decide twice; `[unavailable]` — outside the delivered build mode. | learner |
| D1 | design-structural | **Loop composition** — which of the four loops wrap the agent loop. | The agent loop is always present. Each built loop attaches to the ones inside it as the course wires them: grader feedback re-enters the agent loop; an event invokes the verification loop (the agent loop alone when no grader is built); the learning loop sits outside the others, reading the records of completed runs and feeding an approved change back into the agent's instructions, which every later run of the inner loops then loads. | All four: agent loop + verification loop + event-driven loop (the simulated tracker) + learning loop. Branch: the course's own final form (Lessons 4, 5, the event app, 6). | all four loops (course default); drop the event-driven loop — invoke the verification loop directly (the Lesson 5 form; retires AC19–AC24); drop the learning loop (retires AC25–AC32, AC34 and AC37); drop both outer loops (agent + grader only; retires AC19–AC32, AC34 and AC37); agent loop only (the Lesson 4 form; retires AC12–AC34 and AC37, and rows L3/D2 become moot). Retired criteria are removed from the offline suite AC35 runs, and row RR1's end-to-end invariant then covers the stages that remain built. The learning loop presupposes the verification loop — its signal is the grader's first-attempt verdict — so no option keeps the learning loop without the grader | Litmus: **row** — structural: removing a loop removes a box and an arrow from the diagram; the course demonstrates each reduced form working (Lesson 4 without a grader, Lesson 5 without triggers) before adding the next, and never shows one *failing*, so the reduced forms are legitimate stepping stones, not anti-patterns (Lesson 2: "you don't need the verification loop per se … they're all composable"). The cost of dropping a loop is the course's stated gain from it: the grader buys reliability (and makes a cheaper model viable), events buy "agents actually get used", the learning loop buys improvement across runs. | course+learner |
| D2 | design-structural | **Grader ownership** — who decides whether the analysis is good enough. | After the agent declares itself done, something *other than the agent's own claim* scores the finished file against every criterion of row L3, returns pass/fail per criterion with a gap on each failure, and can send the work back with that feedback. | An LLM grader that reads the file with a read-only file tool, is told to quote the satisfying line verbatim with its line number before passing a criterion, and applies labelled-line criteria literally (R10, R11). Branch: the course's own realization, keyless beyond the model row. | LLM grader with file access as above (course default); a deterministic checker in code — only when every criterion of the rubric in force (row L3) is mechanically checkable; the default rubric's completeness criterion is not, so with the default rubric this option is not available (the course names "deterministic" graders as a type, Lesson 2 slide; the course's other example — links resolve, CI passes — is one; retires AC12, since a checker makes no tool call, and AC33; every other grader criterion is kept: the checker must produce the same per-criterion verdicts and gaps the scripted grader of §5 declares and expose the same two test modes, `error_on` and `fail_completeness_first_pass_on`); a human grader — a person records pass/fail and gaps per criterion (the course's second human-oversight point, Lesson 2; retires AC12 and AC33; in the offline suite the person is driven by the scripted grader's rules as a stand-in, so row RR1's end-to-end run still holds for every stage that wraps a model, and the automatic retry of R12 becomes a person's send-back) | Litmus: **row** — structural: ownership of the verdict moves between model, harness code and a person; the course demonstrates the LLM grader and names the other two as types without showing either failing. A code checker cannot judge an open criterion like completeness; a human grader removes the automatic retry. The course's spoken failure of the LLM grader — passing by resemblance when it grades the transcript instead of the file — is baked into R10, not offered as an option. | course+learner |
| RR1 | realization | **Model the acceptance suite runs against.** | The offline suite drives the real pipeline of every loop built under row D1 end to end — tool calls, the grader's file read and verdict, the event triggers, the batch, the analyst's structured proposal, apply and compare — with no network call; the scripted stand-in and this offline suite remain the completion gate whatever else is chosen. | The scripted model of §5 (`fixtures/scripted_model.py`): a fake chat model standing in for the provider, one instance per role, whose responses this spec declares. Branch: the course's model is a keyed dependency (API key, paid account), so the honest stand-in is the default; it is the only way the loops stay exercisable in an as-is offline build. The course itself ships an offline path (pre-captured traces replayed when its live switch is off), which is the precedent. | scripted model per role only (honestly labelled a stand-in, see §5); scripted model per role **plus** running the suite a second time against the live models of row L4 — the live models being what the course ran (course default — heavy setup: provider API key, paid usage); the `live`-tagged criteria run, and the non-`live` criteria are re-run against the live model as a non-gating smoke pass whose numeric assertions may differ — the offline pass stays the gate) | A scripted reviewer reproduces the course's *observed* dynamics (first attempt lacks the two labelled lines, revises on feedback) rather than a model's judgment; a live run may need more turns, may phrase gaps differently, and is non-deterministic — which is exactly why the course captured traces. | course |
| RR2 | realization | **Run observability** — where a run's trace is kept. | Every run records a step-by-step trace (model turns and tool results, in order), its turn count, and — under a grader — every grading pass with the file as that pass saw it. | The course's own local trace capture: the trace rows and run records of §3, written to disk per run. Branch: keyless and the course's own, so no substitution; the hosted tracer is the optional extra, not the carrier of the behavior. | local trace records as above (course default — the course's notebooks build their trace tables from this); plus hosted tracing with LangSmith (optional in the course, off by default — heavy setup: account + API key, env-var switch; the course notes everything works without it) | Hosted tracing adds shareable, hosted views of each model call; it never changes what the agent does. It is forced off (its env-var switch unset) whenever the offline suite runs, so row RR1's no-network invariant and AC35 hold with either option. Enabling it is a §6 Ask-First item because it sends every prompt and tool result to a third party. | course+learner |

## 1. Objective

A local Python application in which a requirements-review agent turns a ticket id into a five-section analysis file, a grader sends that file back with per-criterion gaps until a three-criterion rubric passes, a simulated ticket-and-page tracker runs the review automatically whenever a ticket is created or its requirement page changes, and a learning step reads a batch of recorded runs, proposes one instruction change for a human to approve, applies it in code, and proves the improvement by re-running the batch — the guarantee being that every loop's outcome is recorded (trace, verdicts, run history, proposal, comparison) so nothing the system decides is invisible (pattern: CTX-A).

### Not Included

Each item carries the handling tag row L6 applies when the gate reads this list.

1. Integration with a real issue tracker or wiki (REST APIs, webhooks, API tokens) — the course names this as the next step and builds only the simulation; swap the simulation's lookups at its one trigger seam when you do. `[owned by row L2]`
2. A scheduled trigger (an agent that runs on a timer, e.g. a morning summary) — named in the course's overview as the other kind of trigger; only event triggers are built. `[named, never built]`
3. Memory consolidation across runs (learning user preferences, e.g. "be more formal with my boss") — the course's second category of learning-loop improvement, described, never built; the learning loop here edits the instructions file only. `[named, never built]`
4. Replaying the course's pre-captured traces as an offline mode — the course's own offline path when its live switch is off; this build's offline path executes the loops with the scripted model instead; replay would need the course's captured traces, which this file cannot carry. `[unavailable]`
5. Human approval on individual tool calls (sensitive actions) — the course's first human-oversight point; the course names the point but builds no approval gate, and this agent has no sensitive tool to gate. `[named, never built]`
6. Skills with progressive disclosure (per-task instruction files loaded on demand) — shown in the course's harness primer on a different toy agent; the review agent uses one always-loaded instructions file. `[restorable]`
7. Subagent delegation, a code interpreter or sandbox, and context summarization — harness features the course lists and does not use. `[named, never built]`
8. Hosted tracing (LangSmith) — `[owned by row RR2]`.
9. A live-model run of the acceptance suite — `[owned by row RR1]`; the `live`-tagged criteria exist for it.
10. Token and cost estimates for a batch (the course prints an approximate cost per batch from a price table) — the price table is perishable (CTX-D); the comparison reports attempts, not cost. `[restorable]`
11. Notebook-style HTML/plot rendering of traces, grids and diffs — presentation only; the app exposes the same facts as records and plain text. `[restorable]`
12. Grafting these loops onto an existing codebase — `[unavailable]` (this spec builds the standalone takeaway only).

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python ≥ 3.12 | The course's lock file and README require 3.12 or newer (its numeric dependencies do not build below it). |
| Agent harness | `deepagents` 0.7.11 | Course-pinned: the lock file resolves exactly 0.7.11 (floor `>=0.7.11`). The harness supplies the agent loop, file tools over a confined backend, the always-loaded instructions file, write permissions, and the rubric grader middleware. Era-specific names → CTX-D. |
| Agent framework | `langchain` 1.3.18, `langchain-core` 1.6.1, `langgraph` 1.2.11 | Course-pinned via the lock file (floors `>=1.3.14`, `>=1.5.0`, `>=1.2.9`). **Install situation, honestly:** the course ships a `pyproject.toml` of version *floors* plus a `uv.lock` of exact resolutions; the notebooks themselves install nothing. Pin the lock's versions; the floors are the course's minimums. |
| Provider client | `langchain-openai` 1.6.0, `openai` 3.6.0 | Course-pinned via the lock file; used only on the `live` path (row RR1) and by the finished app with a key. The provider is row L4's business. |
| Structured output | `pydantic` 2.13.5 | Course-pinned via the lock file; the analyst's proposal is a schema-constrained response (§3 `HarnessChange`). |
| Web app (event loop) | `flask` ≥ 3.1.3 — current release | The course lists Flask as a floor only and its lock file has no entry for it; this is the one dependency the course left unpinned, so a current 3.x release is used. |
| Config / secrets | `python-dotenv` 1.2.3 | Course-pinned via the lock file. `OPENAI_API_KEY` (and the optional `LANGSMITH_*` variables, row RR2) are read from a gitignored `.env`; never hardcoded, never committed, never written into any record, trace or report. |
| Token estimate (optional) | `tiktoken` 0.14.0 | Course-pinned via the lock file; only needed if Not-Included item 10 is restored. |
| Test runner | `pytest` — current release | Project hardening: the course runs its checks in notebooks; the §7 commands need a runner. |
| Storage | Local filesystem + three JSON files | Per-run workspace directories; the tracker simulation's `pages.json`, `tickets.json`, `analysis_runs.json`; the batch's `run_history/<label>/` directory. No database. |

Not carried from the course environment (declared drop, presentation only): `pandas`, `matplotlib`, `seaborn`, `jupyter`, `ipykernel`, `numpy`, `mistune` — they render notebook tables, plots and HTML cards and change nothing the agent does.

## 3. Input/Output Contracts

The core objects, as one JSON Schema document. Every record a loop produces validates against the matching definition; the acceptance criteria assert these fields.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "loop-engineering-takeaway",
  "$defs": {
    "TicketId": { "type": "string", "pattern": "^[A-Z]{2,8}-[0-9]{1,6}$" },
    "TicketStore": {
      "type": "object",
      "description": "ticket id -> requirement text; the fetch tool's only source",
      "propertyNames": { "$ref": "#/$defs/TicketId" },
      "additionalProperties": { "type": "string", "minLength": 1 }
    },
    "SectionName": { "enum": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"] },
    "AnalysisFile": {
      "type": "object",
      "description": "/analysis.md parsed: the five '## ' headings in this fixed order; list sections hold bullets, Summary holds prose",
      "properties": {
        "sections": { "type": "array", "items": { "$ref": "#/$defs/SectionName" }, "minItems": 5, "maxItems": 5, "uniqueItems": true },
        "bullets": {
          "type": "object",
          "properties": {
            "Confirmed Facts": { "type": "array", "items": { "type": "string" } },
            "Ambiguities": { "type": "array", "items": { "$ref": "#/$defs/AmbiguityBullet" } },
            "Clarification Questions": { "type": "array", "items": { "type": "string" } },
            "Assumptions": { "type": "array", "items": { "type": "string" } }
          },
          "required": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions"]
        },
        "summary_words": { "type": "integer", "minimum": 0 },
        "complete": { "type": "boolean", "description": "true iff every list section has >= 1 bullet AND summary_words > 0" }
      },
      "required": ["sections", "bullets", "summary_words", "complete"]
    },
    "AmbiguityBullet": {
      "type": "object",
      "properties": {
        "clause": { "type": "string", "minLength": 1, "description": "the exact clause, quoted verbatim from the requirement" },
        "reason": { "type": "string", "minLength": 1 },
        "resolved_by": { "type": ["string", "null"], "description": "text of the indented 'Resolved by:' line, null when absent" },
        "edge_case": { "type": ["string", "null"], "description": "text of the indented 'Edge case:' line, null when absent" }
      },
      "required": ["clause", "reason", "resolved_by", "edge_case"]
    },
    "Counts": {
      "type": "object",
      "description": "bullets per list section of the analysis file (Summary is prose, excluded)",
      "properties": {
        "Confirmed Facts": { "type": "integer", "minimum": 0 },
        "Ambiguities": { "type": "integer", "minimum": 0 },
        "Clarification Questions": { "type": "integer", "minimum": 0 },
        "Assumptions": { "type": "integer", "minimum": 0 }
      },
      "required": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions"]
    },
    "TraceStep": {
      "type": "object",
      "properties": {
        "step": { "type": "integer", "minimum": 1 },
        "actor": { "enum": ["Model reasoning", "Tool"] },
        "action": { "type": "string", "minLength": 1 },
        "detail": { "type": "string", "maxLength": 221 }
      },
      "required": ["step", "actor", "action", "detail"]
    },
    "ReviewRun": {
      "type": "object",
      "properties": {
        "requirement_doc": { "type": "string" },
        "trace": { "type": "array", "items": { "$ref": "#/$defs/TraceStep" }, "minItems": 1 },
        "analysis_markdown": { "type": "string" },
        "instructions": { "type": "string", "minLength": 1 },
        "stage_order": { "type": "array", "items": { "$ref": "#/$defs/SectionName" } },
        "turns": { "type": "integer", "minimum": 1 },
        "workspace": { "type": "string", "minLength": 1 },
        "stopped_by": { "enum": ["finished", "turn_limit"] },
        "counts": { "$ref": "#/$defs/Counts" },
        "complete": { "type": "boolean" }
      },
      "required": ["requirement_doc", "trace", "analysis_markdown", "instructions", "stage_order", "turns", "workspace", "stopped_by", "counts", "complete"],
      "if": { "properties": { "stopped_by": { "const": "turn_limit" } } },
      "then": { "properties": { "trace": { "contains": { "properties": { "action": { "pattern": "^Stops: turn limit of [0-9]+ reached$" } } } } } }
    },
    "CriterionVerdict": {
      "type": "object",
      "properties": {
        "name": { "type": "string", "minLength": 1 },
        "passed": { "type": "boolean" },
        "gap": { "type": ["string", "null"] }
      },
      "required": ["name", "passed"],
      "if": { "properties": { "passed": { "const": false } } },
      "then": { "properties": { "gap": { "type": "string", "minLength": 1 } }, "required": ["gap"] }
    },
    "GradingPass": {
      "type": "object",
      "properties": {
        "iteration": { "type": "integer", "minimum": 1 },
        "result": { "enum": ["satisfied", "needs_revision", "failed", "grader_error"] },
        "explanation": { "type": "string" },
        "criteria": { "type": "array", "items": { "$ref": "#/$defs/CriterionVerdict" } },
        "analysis_markdown": { "type": "string", "description": "the file exactly as this pass saw it" }
      },
      "required": ["iteration", "result", "explanation", "criteria", "analysis_markdown"],
      "allOf": [
        { "if": { "properties": { "result": { "const": "satisfied" } } },
          "then": { "properties": { "criteria": { "minItems": 1, "items": { "properties": { "passed": { "const": true } } } } } } },
        { "if": { "properties": { "result": { "const": "needs_revision" } } },
          "then": { "properties": { "criteria": { "contains": { "properties": { "passed": { "const": false } } } } } } },
        { "if": { "properties": { "result": { "const": "grader_error" } } },
          "then": { "properties": { "criteria": { "maxItems": 0 } } } }
      ]
    },
    "VerificationRun": {
      "type": "object",
      "properties": {
        "requirement_doc": { "type": "string" },
        "rubric": { "type": "string" },
        "trace": { "type": "array", "items": { "$ref": "#/$defs/TraceStep" } },
        "grading": { "type": "array", "items": { "$ref": "#/$defs/GradingPass" } },
        "analysis_markdown": { "type": "string" },
        "instructions": { "type": "string" },
        "status": { "enum": ["satisfied", "failed", "grader_error", "max_iterations_reached"] },
        "turns": { "type": "integer", "minimum": 1 },
        "workspace": { "type": "string", "minLength": 1 },
        "counts": { "$ref": "#/$defs/Counts" }
      },
      "required": ["requirement_doc", "rubric", "trace", "grading", "analysis_markdown", "instructions", "status", "turns", "workspace", "counts"],
      "allOf": [
        { "if": { "properties": { "status": { "const": "satisfied" } } },
          "then": { "properties": { "grading": { "minItems": 1 } } } },
        { "if": { "properties": { "status": { "const": "max_iterations_reached" } } },
          "then": { "properties": { "grading": { "minItems": 2 } } } }
      ]
    },
    "RunRecord": {
      "type": "object",
      "description": "one document of a batch, with everything kept",
      "properties": {
        "run_id": { "type": "integer", "minimum": 1 },
        "doc_name": { "type": "string", "minLength": 1 },
        "label": { "type": "string", "minLength": 1 },
        "model": { "type": "string", "minLength": 1 },
        "requirement_doc": { "type": "string" },
        "instructions": { "type": "string", "minLength": 1 },
        "messages": { "type": "array", "items": { "$ref": "#/$defs/Message" }, "minItems": 2 },
        "grading": { "type": "array", "items": { "$ref": "#/$defs/GradingPass" } },
        "analysis_markdown": { "type": "string" },
        "status": { "type": "string" },
        "started_at": { "type": "string", "format": "date-time" },
        "workspace": { "type": "string", "minLength": 1 }
      },
      "required": ["run_id", "doc_name", "label", "model", "requirement_doc", "instructions", "messages", "grading", "analysis_markdown", "status", "started_at", "workspace"]
    },
    "Message": {
      "type": "object",
      "properties": {
        "type": { "enum": ["system", "human", "ai", "tool"] },
        "content": { "type": "string" },
        "tool_calls": { "type": "array", "items": { "type": "object", "properties": { "name": { "type": "string" }, "args": { "type": "object" } }, "required": ["name", "args"] } },
        "tool_call_id": { "type": ["string", "null"] },
        "status": { "type": ["string", "null"] }
      },
      "required": ["type", "content", "tool_calls"]
    },
    "CriterionRate": {
      "type": "object",
      "properties": { "passed": { "type": "integer", "minimum": 0 }, "total": { "type": "integer", "minimum": 0 }, "pass_rate": { "type": ["number", "null"], "minimum": 0, "maximum": 1 } },
      "required": ["passed", "total", "pass_rate"]
    },
    "BatchSummary": {
      "type": "object",
      "properties": {
        "label": { "type": "string" },
        "model": { "type": "string" },
        "runs": { "type": "integer", "minimum": 1 },
        "graded": { "type": "integer", "minimum": 0 },
        "grader_errors": { "type": "integer", "minimum": 0 },
        "first_attempt": { "type": "object", "additionalProperties": { "$ref": "#/$defs/CriterionRate" }, "minProperties": 1 },
        "revisions_needed": { "type": "integer", "minimum": 0 },
        "documents": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["label", "model", "runs", "graded", "grader_errors", "first_attempt", "revisions_needed", "documents"]
    },
    "HarnessChange": {
      "type": "object",
      "properties": {
        "target": { "enum": ["prompt", "tool", "grader", "configuration"] },
        "issue": { "type": "string", "minLength": 1 },
        "recurrence": { "type": "string", "minLength": 1 },
        "evidence": { "type": "array", "items": { "type": "string", "minLength": 1 }, "minItems": 1 },
        "section": { "type": "string" },
        "change": { "type": "string", "minLength": 1, "description": "literal text to insert, not a description" },
        "rejected": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["target", "issue", "recurrence", "evidence", "section", "change", "rejected"],
      "if": { "properties": { "target": { "const": "prompt" } } },
      "then": { "properties": { "section": { "pattern": "^#{1,6} .+" } } }
    },
    "Comparison": {
      "type": "object",
      "properties": {
        "verdict": { "enum": ["regression", "success", "partial", "no effect"] },
        "criteria": { "type": "object", "additionalProperties": { "type": "array", "items": { "type": "integer", "minimum": 0 }, "minItems": 2, "maxItems": 2 } },
        "runs": { "type": "integer" },
        "revisions_needed": { "type": "array", "items": { "type": "integer" }, "minItems": 2, "maxItems": 2 },
        "attempts": { "type": "array", "items": { "type": "integer" }, "minItems": 2, "maxItems": 2 },
        "improved": { "type": "array", "items": { "type": "string" } },
        "regressed": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["verdict", "criteria", "runs", "revisions_needed", "attempts", "improved", "regressed"],
      "allOf": [
        { "if": { "properties": { "verdict": { "const": "regression" } } }, "then": { "properties": { "regressed": { "minItems": 1 } } } },
        { "if": { "properties": { "regressed": { "minItems": 1 } } }, "then": { "properties": { "verdict": { "const": "regression" } } } }
      ]
    },
    "PageVersion": {
      "type": "object",
      "properties": { "n": { "type": "integer", "minimum": 1 }, "author": { "type": "string", "minLength": 1 }, "timestamp": { "type": "string" }, "body": { "type": "string" } },
      "required": ["n", "author", "timestamp", "body"]
    },
    "Page": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "pattern": "^page-[a-z0-9-]+$" },
        "kind": { "enum": ["requirement", "analysis_report"] },
        "title": { "type": "string", "minLength": 1 },
        "linked_ticket": { "oneOf": [ { "$ref": "#/$defs/TicketId" }, { "type": "null" } ] },
        "versions": { "type": "array", "items": { "$ref": "#/$defs/PageVersion" } }
      },
      "required": ["id", "kind", "title", "linked_ticket", "versions"],
      "allOf": [
        { "if": { "properties": { "kind": { "const": "requirement" } } }, "then": { "properties": { "linked_ticket": { "type": "null" }, "versions": { "minItems": 1 } } } },
        { "if": { "properties": { "kind": { "const": "analysis_report" } } }, "then": { "properties": { "linked_ticket": { "$ref": "#/$defs/TicketId" }, "versions": { "items": { "properties": { "author": { "const": "Requirements Analysis Agent (bot)" } } } } } } }
      ]
    },
    "Ticket": {
      "type": "object",
      "properties": {
        "key": { "$ref": "#/$defs/TicketId" },
        "title": { "type": "string", "minLength": 1 },
        "description": { "type": "string" },
        "linked_page_id": { "type": "string", "pattern": "^page-[a-z0-9-]+$" },
        "assignee": { "type": "string", "minLength": 1 },
        "status": { "enum": ["Open", "Analysis Ready", "Done"] },
        "comments": { "type": "array", "items": { "type": "object", "properties": { "author": { "type": "string" }, "text": { "type": "string" }, "timestamp": { "type": "string" } }, "required": ["author", "text", "timestamp"] } },
        "created_at": { "type": "string" },
        "last_analyzed_version": { "type": ["integer", "null"] },
        "last_run_id": { "type": ["string", "null"] }
      },
      "required": ["key", "title", "description", "linked_page_id", "assignee", "status", "comments", "created_at", "last_analyzed_version", "last_run_id"],
      "if": { "properties": { "status": { "const": "Analysis Ready" } } },
      "then": { "properties": { "last_analyzed_version": { "type": "integer" }, "last_run_id": { "type": "string" } } }
    },
    "AutomationRun": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "pattern": "^[0-9a-f]{8}$" },
        "ticket_key": { "$ref": "#/$defs/TicketId" },
        "requirement_page_id": { "type": "string" },
        "requirement_version": { "type": "integer", "minimum": 1 },
        "report_page_id": { "type": "string" },
        "report_version": { "type": "integer", "minimum": 1 },
        "status": { "type": "string" },
        "turns": { "type": "integer" },
        "counts": { "$ref": "#/$defs/Counts" },
        "trace": { "type": "array", "items": { "$ref": "#/$defs/TraceStep" } },
        "grading": { "type": "array", "items": { "$ref": "#/$defs/GradingPass" } },
        "timestamp": { "type": "string" }
      },
      "required": ["id", "ticket_key", "requirement_page_id", "requirement_version", "report_page_id", "report_version", "status", "turns", "counts", "trace", "grading", "timestamp"]
    }
  }
}
```

Each of the three store files is a JSON **array** of its objects (`pages.json` of `Page`, `tickets.json` of `Ticket`, `analysis_runs.json` of `AutomationRun`); the ticket store seed `tickets.json` of §5 is a `TicketStore` object. Identifier formats are part of the contract: ticket ids are an uppercase project prefix, a hyphen, and digits (the course's `AUTH-142`, `NOTIF-205`, `REQ-104` shape); automation run ids and per-run workspace names are **8 lowercase hex characters** (alphabet and length both binding); report page ids are `page-analysis-<ticket key lower-cased>`; requirement page ids are `page-` plus a lower-case slug of the title (non-alphanumerics to `-`, runs collapsed, `-2`/`-3`… appended on collision) for pages created through the form, while the seed page's id is the fixed constant `page-req-catalog-search`.

The **report page banner**: every version of an analysis-report page begins with three quote lines — `> Generated automatically from <ticket key> on <timestamp>.`, `> Source requirement: version <n>.`, `> Verification status: **<status>** after <k> grading pass(es).` — followed by a blank line and the analysis file verbatim.

The **grader's rubric** is a string of lines, each `- <criterion name>: <criterion text>`; criterion names are read from the rubric (text before the first colon), never from the grader's echo, and verdicts are matched to criteria by *position*, because the grader paraphrases names.

## 4. Business Rules

Each rule: the behavior, the failure it prevents (CTX-B anchor where the course demonstrated it), a provenance label, and the acceptance criteria that cite it. Parameter values name the exact config they came from. "Course-demonstrated" = traceable to the supplied materials; "project hardening" = this spec's own addition.

**Agent loop**

1. **R1 — Fetch by identifier.** The agent is never handed the requirement text. Its opening message is the sentence `The requirement document is tracked in Jira as ticket <id>. Fetch it to begin.` and the only way to obtain the text is the `fetch_requirement` tool, which resolves the id against the ticket store at call time (row L2). Prevents: an agent that "reviews" text pasted into its prompt and never exercises the tool path the event loop depends on (CTX-A). *Course-demonstrated* (the course's run helpers seed the store and pass only the id). → AC2, AC20
2. **R2 — The analysis is a file, built stage by stage.** The deliverable is `/analysis.md` in the run's workspace, holding exactly the five `## ` headings `Confirmed Facts`, `Ambiguities`, `Clarification Questions`, `Assumptions`, `Summary` in that order. It is created by one write (the skeleton with only Confirmed Facts filled) and each later section is filled by one edit that touches only that section; one stage per tool call, in order. A run is **complete** when every list section has ≥ 1 bullet and Summary has ≥ 1 word; the record's `stage_order` lists the sections in the order they were actually filled (only writes the tool accepted count). Prevents: output that must be parsed out of a chat message and cannot be read by a grader or opened by a person (CTX-A, CTX-C). *Course-demonstrated* (the course's instructions file; its harness module states "the analysis is a file"). → AC3, AC4, AC36
3. **R3 — Bullet shapes.** Confirmed Facts: one bullet per fact the document states directly, no inference. Ambiguities: one bullet per under-specified clause, in the shape `- **"<exact clause>"**` followed by an indented `Reason:` line; when the instructions in force ask for them, two further indented lines `Resolved by:` and `Edge case:` follow the Reason line. The clause is quoted verbatim from the requirement. Clarification Questions and Assumptions: one bullet each. Summary: two or three sentences. Prevents: a report whose ambiguities cannot be matched back to the requirement or graded for a labelled line (CTX-B7). *Course-demonstrated* (the course's instructions file and rubric). → AC4, AC14
4. **R4 — Transient tool failure → retry the same call.** The fetch tool returns an error *observation* (never raises) on a transient failure; the agent retries the exact same tool with the exact same arguments until it succeeds. The simulated failure count is deterministic: **2 failures before success for the plain review run** — the value the Lesson 4 narration states aloud ("simulating two times of failure"); the course's module constant is `0` and its notebook table says two, a contradiction resolved by the narration branch of the lever rule (CTX-C) — and **0 wherever a grader is attached** (the course's batch and automation code set `0` there: "the retry only adds turns and noise"). The two error observations, in order, are `Error fetching ticket from Jira: 503 Service Unavailable. The Jira API is temporarily unreachable, please retry.` and `Error fetching ticket from Jira: request timed out after 10s. Please retry.`; an unknown id returns `Error fetching ticket from Jira: no ticket '<id>' found.` An observation is an error when its tool status is error or its text starts, case-insensitively, with `error`. Both counts are post-build levers. Prevents: a run that dies on the first flaky external call (CTX-B1). *Course-demonstrated*. → AC1, AC5, AC6
5. **R5 — The turn cap is a safety net, not the normal stop.** The normal stop is the agent's own final message after the Summary. A model-call cap ends the run cleanly (no exception) when the model keeps going past the point where it makes sense: **12 turns for the plain review run** (course Lesson 4 config `MAX_TURNS = 12`, also the module default) and **40 with a grader attached** (course Lesson 5 config, batch and automation code — more passes cost more turns). When the cap stops a run whose file is incomplete, the harness appends one final trace row (actor `Model reasoning`, action `Stops: turn limit of <cap> reached`) that records the stop and is not a model turn, and sets `stopped_by = turn_limit`, never confused with a finished review. Both caps are post-build levers. Prevents: an agent retrying an unknown ticket forever (CTX-B2). *Course-demonstrated* (narration: "max_turns matters when that path fails"). → AC1, AC6
6. **R6 — Instructions are a file loaded at the start of every run, and its absence is loud.** The agent's instructions live at `/memories/AGENTS.md` inside its workspace and are loaded into its context at the start of every run (the system prompt only points at them). Building an agent whose workspace lacks that file **fails with an error naming the missing path** — the harness's memory loader ignores a missing file silently, which would produce a plausible bad review on the system prompt alone. Prevents: CTX-B3. *Course-demonstrated* (the course's `require_agents_file` guard). → AC1, AC7
7. **R7 — The agent never writes its own instructions.** Writes under `/memories/` are denied by permission, not by asking nicely: a write or edit there returns an error observation and the file is byte-identical afterwards. Instruction changes come only from the learning loop's apply step (R20). Prevents: CTX-B4. *Course-demonstrated* (the course's write-deny permission). → AC8
8. **R8 — One confined, fresh workspace per run.** The agent's file tools see the run's workspace directory as `/`; any path that resolves above it is unreachable (error observation, content never enters the conversation). No `/analysis.md` exists when the first model call is made: a run deletes any leftover before invoking the agent, and the event loop and the batch give every run its own directory (the event loop removes it after the run). Prevents: an agent reading a previous run's finished analysis and skipping stages, or reading the repository's `.env` (CTX-B5). *Course-demonstrated* (virtual-mode backend; per-run workspaces; the unlink before each run). → AC1, AC9, AC10, AC24
9. **R9 — Every run is traced.** A run record holds a trace of alternating `Model reasoning` / `Tool` steps (one row per model turn and per tool result, in order; a model row's action names the tools it calls and the sections those calls fill, e.g. `Calls edit_file: Ambiguities`, and the final tool-free model message is the row `Finishes the review`; a tool row carries the result text with whitespace runs collapsed to single spaces and truncated to 220 characters plus `…`), the turn count (= number of model messages), the file as produced, the instructions as loaded, `stage_order`, and the workspace path. An edit the tool rejects (for example a non-unique `old_string`) is recorded as an error result and does not count toward `stage_order`; the agent recovers by reading the file and retrying. Prevents: a run whose story is invisible (CTX-A — "for agents, the story is in the traces"; CTX-B12). *Course-demonstrated* (the course's trace capture) with one hardening addition: the `workspace` and `stopped_by` fields. → AC11, AC36

**Verification loop**

10. **R10 — The grader judges the file, not the conversation.** When the agent declares itself done, a grader (row D2) receives the rubric and the transcript, is given a **read-only** file tool, and **must read `/analysis.md` before passing any criterion**; a criterion passes only if the grader can quote the satisfying text verbatim with its line number; otherwise it fails with a gap. Its verdict is `satisfied` (every criterion passes), `needs_revision` (≥ 1 fails, each failure carries a gap), or `failed` (the rubric is malformed or impossible to evaluate — e.g. it contains no criterion line). If the grader itself errors, the harness records a pass with result `grader_error` and no criteria, and the run ends with that status (R12); such a run counts as *ungraded* (R18). Each pass is recorded with the file exactly as the grader saw it. Prevents: a grader that passes criteria the file does not satisfy because the conversation *reads* as if they were met (CTX-B6). *Course-demonstrated* (the course's grader prompt additions and its reasons). → AC12, AC13, AC17, AC18, AC38
11. **R11 — The rubric, applied literally.** The default rubric (row L3) is exactly these three lines: `- completeness: every clause of the requirement document is addressed somewhere in the analysis`, `- clarity: every bullet in the Ambiguities section has an indented "Resolved by:" line naming the specific fact or decision that would settle it`, `- depth: every bullet in the Ambiguities section has an indented "Edge case:" line naming a concrete production failure that ambiguity could cause`. Where a criterion names a labelled line, only that exact label satisfies it — a `Reason:` line is not a `Resolved by:` line however similar its content; coverage criteria check every item, never a sample. All three must pass **in the same pass** for the loop to stop. Prevents: CTX-B7 (the course's first attempts always lacked the two lines). *Course-demonstrated* (the course's rubric constant and grader prompt). → AC13, AC14
12. **R12 — Retry with feedback, bounded.** On `needs_revision` the gaps are injected into the agent's conversation and the agent revises the file; the loop ends when a pass is `satisfied`, when the revision budget is spent, or when a pass is `failed` or `grader_error` (no feedback exists to revise on; the run ends after that single pass with that result as its status). Budget: **3** — the Lesson 5 narration states "MAX_RUBRIC_ITERATIONS to 3" and the batch code uses 3; the event app's trigger uses 2 (a contradiction resolved by the narration branch; post-build lever, CTX-C). This spec's reading of "the number of times the grader may send work back": at most N grading passes are made; if the N-th is still `needs_revision` the run's terminal status is `max_iterations_reached` and no further revision is attempted (generator's reading of the course's words — post-build lever). Budget 0 removes the grader entirely: the same agent runs as the plain agent loop. Prevents: an endless grade-revise cycle, and a "done" that is only the agent's own claim (CTX-B7). *Course-demonstrated*. → AC14, AC15, AC16, AC33
13. **R13 — Verdicts match criteria by position.** Criterion names are read from the rubric lines (text before the first colon); a grader's per-criterion verdicts are matched to those names by position, never by the grader's wording, because the grader paraphrases names. Prevents: one recurring criterion splitting into several under different spellings (CTX-C, row L3 background). *Course-demonstrated*. → AC13, AC14, AC26

**Event-driven loop**

14. **R14 — Events trigger the review; nothing else does.** Two events run the verification loop for a ticket: (a) a ticket is created linked to a requirement page; (b) a new version of a requirement page is saved while ≥ 1 ticket linked to it is not `Done` — every such ticket is re-run. A ticket whose status is `Done` is never re-triggered. A "Re-run analysis now" action on a ticket not `Done` runs it against the page's current version. A run raises (no partial state) if the ticket or its linked page is missing. Prevents: an analysis that silently goes stale when the requirement changes (CTX-B8). *Course-demonstrated* (the course's automation trigger). → AC19, AC20, AC21, AC22, AC24
15. **R15 — Source of truth is never edited by the agent.** The requirement page is only ever edited by a person; the agent's findings are written as a **new version** of a separate agent-owned page titled `Analysis Report — <ticket key>` (id `page-analysis-<key lower-cased>`, author `Requirements Analysis Agent (bot)`), whose body is the §3 banner followed by the analysis file verbatim, so the page's own version history shows every past analysis and a diff between any two. Prevents: the agent overwriting the document it is supposed to review (CTX-A). *Course-demonstrated*. → AC20, AC21
16. **R16 — Ticket lifecycle; a human closes.** A completed run sets the ticket to `Analysis Ready`, records `last_analyzed_version` and `last_run_id`, and adds a bot comment of the form `Analysis complete (<status>), requirement version <n>. See "<report page title>".` Only a person's explicit action moves a ticket to `Done`; the agent never closes its own work. Statuses: `Open` → `Analysis Ready` → `Done`. Prevents: automation that declares its own work finished (CTX-A — the course's third human-oversight point, approval of the artifact). *Course-demonstrated*. → AC20, AC22
17. **R17 — Change is shown two ways.** Every automation run is recorded (§3 `AutomationRun`) and a ticket with ≥ 2 runs shows, under the heading "What changed since the previous run", side by side for the previous and latest run, the requirement version analyzed, the verification status, and the bullet count of each list section; the report page offers a line diff between any two of its versions, shown together with the two underlying runs' statuses and bullet counts. Prevents: the course's observed trap — bullet counts often look the same before and after while the content changed completely, so neither counts nor diff alone tells the story (CTX-C). *Course-demonstrated*. → AC23

**Learning loop**

18. **R18 — A batch is one instruction version, fully recorded.** A batch (`label`) reviews every document in a directory, in filename order, each run seeded from the **same** instructions file (snapshotted as `<label>/AGENTS.md`), in its own workspace `<label>/ws_<NN>`, its text registered in the ticket store under the ticket id `BATCH-<NN>` (NN = the run number, two digits) so the opening message names that id, under the verification loop with budget 3 and 0 simulated failures; each run is written to `<label>/run_<NN>_<doc stem>.json` (§3 `RunRecord`: every message untruncated with full tool-call arguments, every grading pass with the file as it stood). `<label>/summary.json` (§3 `BatchSummary`) reports, per criterion, the number of runs whose **first** grading pass passed it, with the denominator = runs that were actually graded; a `grader_error` run is excluded from denominators and counted in `grader_errors`, never as a pass; `revisions_needed` = graded runs whose first pass failed ≥ 1 criterion. Prevents: an ungraded run averaged in as a success (CTX-B9), and a batch produced by mixed instruction versions. *Course-demonstrated* (the course's batch module). → AC25, AC26, AC27, AC31, AC37
19. **R19 — The analyst reads evidence, cannot alter it, and proposes one change.** An analyst agent (row L4's analyst model) is rooted at the history directory with read tools and a write permission for exactly one path, `/proposal.md`; every other write is denied. It starts from `/<label>/summary.json`, reads into the runs for evidence and reads `/<label>/AGENTS.md` so the addition fits what is already there, and returns one §3 `HarnessChange`: a criterion failing on the first attempt in **most** graded runs is a property of the agent and becomes the change; a problem seen in a minority of runs is not a pattern and goes under `rejected`. "Most" is read as *more than half* of graded runs — the generator's quantification of the course's words ("most runs" / "one run out of five is not a pattern"), a post-build lever. Evidence entries are verbatim quotes from the runs; `change` is the literal text to insert. The proposal is also persisted beside the batch as `proposal_<label>.md` and `proposal_<label>.json`. Prevents: acting on a one-off (CTX-B10) and an analyst that edits the evidence it reasons from. *Course-demonstrated*. → AC28, AC29, AC34, AC37
20. **R20 — Propose, approve, then apply in code.** The analyst never applies. Applying is a separate, human-invoked step over an approved `HarnessChange`: it inserts `change` verbatim at the end of the section whose heading equals `section` (the section ends at the next heading of equal or shallower depth; trailing blank lines are dropped; the insertion is surrounded by one blank line on each side), with no model call. It **refuses** (error naming the target) when `target` is not `prompt`, and refuses (error naming the heading) when the section is not found. Prevents: a half-applied or unreviewable harness change (CTX-B11; the course's fourth human-oversight point, review of harness changes). *Course-demonstrated* (the course's apply function and its stated reasons). → AC28, AC30
21. **R21 — Measure before merging.** After applying, the batch is re-run under the new instructions as a new label and compared with the old: per criterion the two first-attempt pass counts; `verdict` = `regression` if any criterion's count fell, else `success` if the new batch needed 0 revisions, else `partial` if any count rose, else `no effect`; plus `revisions_needed` and `attempts` for both, where a batch's `attempts` is the total number of grading passes across its run files (for the authored summary fixtures of §5, which have no run files, the sibling `attempts.json` supplies the integer). `improved` lists the criteria whose count rose and `regressed` those whose count fell (rubric order); `runs` is the number of runs in the before batch. A `regression` verdict blocks adoption of the change. Prevents: merging a harness change on faith (CTX-B11 — "it's pretty hard to have confidence merging changes … if you don't have good evals"). *Course-demonstrated* (the course's compare function). → AC31, AC32

**Cross-cutting**

22. **R22 — Offline by default; keys unlock only `live`.** The acceptance suite runs end to end with no network and no provider key, using the scripted model of §5 (row RR1); the finished app reads `OPENAI_API_KEY` from `.env` only on the live path; the offline suite unsets every provider and tracing variable before it runs; no secret is ever written into a record, trace, report page or log. Prevents: a build whose tests cannot run on day one, and a leaked key in a run file. *Project hardening*, modelled on the course's own offline replay path (pre-captured traces when its live switch is off). → AC35

## 5. Acceptance Criteria

### 5.1 Fixture corpus (declared first; every fact an AC relies on is here)

All fixtures live under `fixtures/`. Every fact below is authored for this spec — none is course data. The building agent MUST NOT modify a fixture to make a test pass. Module filenames are importable Python identifiers.

**`fixtures/tickets.json`** — the ticket store seed: six ids → requirement text. Each text is a `REQUIREMENT: <title>` line followed by clauses separated by blank lines. The **clauses** (non-title, non-empty lines) and the **vague term** each contains (first match against the scripted reviewer's term list, below) are:

| Ticket id | Title | Clauses (verbatim) | Vague term |
|---|---|---|---|
| `SRCH-12` | Catalog Search | 1 `Shoppers shall be able to search the catalog by keyword.` · 2 `Results should appear quickly.` · 3 `The search should tolerate common misspellings.` · 4 `Out-of-stock items should be handled sensibly.` | — · quickly · common · sensibly |
| `EXP-31` | Account Data Export | 1 `Users shall be able to export all of their account data.` · 2 `Exports must be delivered within a reasonable time.` · 3 `Large exports should be handled appropriately.` · 4 `The export format should be widely compatible.` | — · reasonable · appropriately · widely |
| `BKP-44` | Nightly Backups | 1 `The system shall back up all customer data every night.` · 2 `Backups must be stored securely.` · 3 `Restores should complete quickly.` | — · securely · quickly |
| `SESS-58` | Session Timeout | 1 `Idle sessions shall expire automatically.` · 2 `The timeout should be reasonable for office use.` · 3 `Users must be warned appropriately before expiry.` · 4 `Expired sessions should be cleaned up promptly.` | — · reasonable · appropriately · promptly |
| `INV-63` | Inventory Sync | 1 `Stock levels shall be synchronized between the warehouse and the web store.` · 2 `Sync conflicts must be resolved sensibly.` · 3 `The sync should run regularly.` · 4 `Failures must be reported to operators promptly.` · 5 `The system shall keep a log of every sync.` | — · sensibly · regularly · promptly · — |
| `ONB-77` | Onboarding Checklist | 1 `New employees shall receive an onboarding checklist on their first day.` · 2 `Managers must be able to customize the checklist easily.` | — · easily |

Derived counts the ACs assert (facts = number of clauses; ambiguities = clauses with a vague term): `SRCH-12` 4/3, `EXP-31` 4/3, `BKP-44` 3/2, `SESS-58` 4/3, `INV-63` 5/3, `ONB-77` 2/1. The default ticket id is `SRCH-12`. `NOPE-1` is a well-formed id that is **not** in the store.

**`fixtures/requirement_docs/`** — the batch's five documents, byte-identical to the texts of the first five tickets: `01_catalog_search.md` (= `SRCH-12`), `02_account_data_export.md` (= `EXP-31`), `03_nightly_backups.md` (= `BKP-44`), `04_session_timeout.md` (= `SESS-58`), `05_inventory_sync.md` (= `INV-63`). Document names (file stems, in this order) are the batch's `documents` list.

**`fixtures/rubric.txt`** — exactly the three rubric lines of R11, in that order. **`fixtures/rubric_empty.txt`** — the single line `(no criteria)` — a rubric with no `- name:` line, i.e. malformed.

**`fixtures/agents_v1.md`** — the reviewer's instructions before learning. Exact content:

```markdown
# Requirements Review Agent

You turn one raw requirement document into a structured review held in a single file, `/analysis.md`.

## Procedure

Work through these stages in order, one tool call per turn. Never skip a stage and never combine two stages into one call.

1. Call `fetch_requirement` with the ticket id to get the requirement document.
2. Call `write_file` to create `/analysis.md` with the headings `## Confirmed Facts`, `## Ambiguities`, `## Clarification Questions`, `## Assumptions` and `## Summary`, in that order, filling in only the Confirmed Facts section (one bullet per fact).
3. Call `edit_file` to fill in the Ambiguities section: one bullet per clause, the exact clause quoted in bold, then an indented `Reason:` line.
4. Call `edit_file` to fill in the Clarification Questions section, one bullet each.
5. Call `edit_file` to fill in the Assumptions section, one bullet each.
6. Call `edit_file` to fill in the Summary section with two or three sentences.

A tool call can fail transiently, for example when an external system is unreachable. If a tool call returns an error message instead of a result, call the same tool again with the same arguments, and keep retrying until it succeeds.

You never modify the requirement document; it is the source of truth. You never edit this file either.

Once the Summary is written the review is finished: reply with one short sentence and call no further tools.

## Review guidance

### Confirmed facts

Record only what the document states directly. Do not infer.

### Ambiguities

Quote the exact clause, then give the reason it is under-specified.

### Clarification questions

Ask what a reviewer would need answered before work could start.

### Assumptions

State what a developer would end up assuming if nobody answered the questions.
```

The literal `Resolved by:` does **not** occur in this file; that absence is what the scripted reviewer keys on.

**The insertion text** (`INSERTION`, declared here; the scripted analyst's `change` and the expected apply result both use it verbatim, 4 lines):

```text
For every ambiguity bullet, add two indented labelled lines after the Reason line:

  Resolved by: the specific fact or decision that would settle the ambiguity
  Edge case: a concrete production failure that could happen if the ambiguity remains unresolved
```

**`fixtures/agents_v2_expected.md`** — `agents_v1.md` with `INSERTION` inserted per R20 at the end of the `### Ambiguities` section: i.e. after the line `Quote the exact clause, then give the reason it is under-specified.` come one blank line, the four `INSERTION` lines, one blank line, then `### Clarification questions` and the rest unchanged. Line count: `agents_v1.md` has 38 lines; `agents_v2_expected.md` has 43.

**`fixtures/scripted_model.py`** — the honest stand-in for the provider model (row RR1): a chat-model fake the harness accepts wherever the course passes a model name, with **three roles, one instance per role**, chosen by construction (`ScriptedReviewer()`, `ScriptedGrader()`, `ScriptedAnalyst()`), each counting its calls (`.calls`). Its description, wherever the app lists models, is `scripted stand-in (no provider; deterministic responses declared by the spec)`. Behaviors:

- **Vague-term list** (case-insensitive whole-word match; the first listed term found in a clause is *the* term): `quickly, reasonable, sensibly, appropriately, appropriate, common, securely, promptly, easily, large, widely, efficiently, regularly, timely`.
- **`ScriptedReviewer`** — follows the Procedure on every run: turn 1 calls `fetch_requirement(ticket_id=<the id named in the opening message>)`; while the latest tool observation is an error (R4 definition) it repeats the identical call; on the document it calls `write_file("/analysis.md", …)` with the five headings and Confirmed Facts = one bullet `- <clause>` per clause; then `edit_file` for Ambiguities (one bullet per clause with a vague term, exactly: `- **"<clause>"**` newline `  Reason: "<term>" sets no measurable threshold.`; **plus**, only if the system-role content it receives on that turn (the harness loads the instructions file into the system prompt, R6) contains the literal `Resolved by:`, the two lines `  Resolved by: a stated numeric threshold or named standard for "<term>".` and `  Edge case: without one, two teams implement "<term>" differently and the feature fails acceptance in production.`); then Clarification Questions (`- What measurable threshold does "<term>" require in "<clause>"?` per ambiguity); then Assumptions (`- Until confirmed, "<term>" is read as its narrowest common interpretation.` per ambiguity); then Summary (`The requirement states <facts> facts, of which <amb> are ambiguous. Clarifying the vague terms before implementation would remove the listed assumptions.`); then a final message `Review complete.` with no tool call. Each edit's `old_string` is unique in the file. **Feedback**: if, after its final message, a new message arrives whose text contains `Resolved by:`, it makes one `edit_file` that rewrites the Ambiguities section with the two labelled lines added under every bullet, then sends `Revision complete.`; any other feedback (or none) leaves the file unchanged and it replies `Review complete.` again. **Modes** (constructor flags, default off): `rogue_write` — its first call is `write_file("/memories/AGENTS.md", "pwned")`, then the normal procedure; `escape_read` — its first call is `read_file("/../secret.txt")`, then the normal procedure; `probe_stale` — its first call is `read_file("/analysis.md")`, then the normal procedure; `stubborn` — ignores feedback (always replies `Review complete.` without editing); `dup_edit` — its Ambiguities edit first uses the non-unique `old_string` `"\n\n"`, and on the tool's error reads `/analysis.md` and retries with the unique string; `claim_in_message` — its final message is `Review complete. Every ambiguity bullet has its Resolved by: and Edge case: lines.` even though the file has none (the conversation claims what the file lacks).
- **`ScriptedGrader`** — on every grading pass its first action is the tool call `read_file("/analysis.md")`; it takes the requirement text from the most recent non-error `fetch_requirement` observation in the transcript; it then judges **only the file it read**: *completeness* passes iff every clause of the requirement appears verbatim in the file; *clarity* passes iff every Ambiguities bullet has an indented line starting `Resolved by:`; *depth* likewise for `Edge case:`; the explanation quotes, for each passing criterion, one satisfying line with its 1-based line number; a failing criterion's gap is `Each Ambiguities bullet needs an indented "Resolved by:" line; bullet 1 has none.` (clarity) / `Each Ambiguities bullet needs an indented "Edge case:" line; bullet 1 has none.` (depth) / `Clause "<clause>" is not addressed.` (completeness). Result: `satisfied` iff all pass, else `needs_revision`; if the rubric contains no `- name:` line the result is `failed` with explanation `Rubric has no criteria.` and an empty criteria list. The grader identifies the document by the ticket id named in the transcript's opening message. **Mode** `error_on` (a set of ticket ids, default empty): on those tickets the grader raises `RuntimeError("scripted grader failure")` instead of answering.
- **`ScriptedAnalyst`** — reads `/<label>/summary.json`, then every `/<label>/run_*.json`, then `/<label>/AGENTS.md` (in that order, via `read_file`); a criterion is **systemic** when `passed / total < 0.5` (R19's "more than half fail"). If `clarity` or `depth` is systemic it writes `/proposal.md` with the five headings `## Summary signal`, `## Current instruction gap`, `## Evidence across runs`, `## Proposed insertion`, `## Rejected observations` and returns the structured `HarnessChange`: `target = "prompt"`, `section = "### Ambiguities"`, `change = INSERTION`, `issue = "The agent writes Ambiguities bullets without the indented Resolved by: and Edge case: lines the rubric requires."`, `recurrence = "<k>/<n> runs: <doc stems joined by ', '> failed first attempt on clarity and depth."` where k = runs whose first pass failed clarity, n = graded runs, `evidence` = the first-pass clarity gap string of each of those runs (verbatim, in run order), `rejected` = one entry `"<criterion> failed first attempt in <j> of <n> runs; a minority is not a pattern."` for each criterion with 0 < j ≤ n/2 (empty when there is none). **Mode** `tamper`: its first call is `write_file("/<label>/summary.json", "{}")`, then the normal procedure. (No AC exercises a batch with no systemic criterion.)

**Planted states and test hooks**

- `fixtures/stale_workspace/`: a workspace whose `/memories/AGENTS.md` is `agents_v1.md` and whose `/analysis.md` contains the single line `STALE-MARKER`. Tests that run against a fixture workspace (`stale_workspace/`, `bare_workspace/`) first copy it to a temporary directory and run there, so the fixture itself is never modified.
- `fixtures/bare_workspace/`: an empty directory (no `memories/`).
- `fixtures/secret.txt`: one line `TOP-SECRET-VALUE`, placed **beside** (not inside) the workspace used by AC9.
- `fixtures/harness_change_tool.json`, `fixtures/harness_change_grader.json`, `fixtures/harness_change_configuration.json`: three `HarnessChange` files identical except for `target` (`"tool"`, `"grader"`, `"configuration"`), each with `section = ""`, `change = "Add a glossary lookup tool."`, `issue`/`recurrence` = `"n/a"`, `evidence = ["n/a"]`, `rejected = []`.
- `fixtures/harness_change_badsection.json`: same shape with `target = "prompt"`, `section = "### Glossary"` (a heading `agents_v1.md` does not contain), `change = INSERTION`.
- `fixtures/summaries/`: authored `BatchSummary` files, all with `runs = graded = 5`, `grader_errors = 0`, the five document stems above, `model = "scripted"`: `before.json` — completeness 5/5, clarity 2/5, depth 1/5, `revisions_needed = 4`; `after_regression.json` — completeness 4/5, clarity 5/5, depth 5/5, `revisions_needed = 1`; `after_partial.json` — completeness 5/5, clarity 4/5, depth 1/5, `revisions_needed = 4`; `after_noeffect.json` — identical counts to `before.json`. These summaries have no run files, so for them `attempts` is read from the sibling `fixtures/summaries/attempts.json`, a JSON object keyed by summary file stem: `{"before": 9, "after_regression": 6, "after_partial": 9, "after_noeffect": 9}`.
- **Event-app configuration under test**: data directory = a temporary directory; reviewer and grader = the scripted stand-ins; instructions = `agents_v1.md` copied into each run's fresh workspace; rubric = `rubric.txt`; revision budget 3; 0 simulated failures; cap 40. **Seed** (created when the data directory is empty): one requirement page `id = page-req-catalog-search`, title `Catalog Search — Requirements`, version 1 by `Priya (Product Manager)`, body = `SRCH-12`'s four clauses separated by blank lines (no `REQUIREMENT:` title line); one ticket `REV-200`, title `Review requirements: Catalog Search`, description `Please review the requirement page for ambiguity before implementation starts.`, linked to that page, assignee `Theo (Eng Lead)`, status `Open`, no comments, `last_analyzed_version` and `last_run_id` null; `analysis_runs.json = []`. **People cast** for the form's author/assignee selects: `Priya (Product Manager)`, `Theo (Eng Lead)`, `Mina (QA Lead)`. **Ticket keys**: prefix `REV`; a new ticket's number is the highest existing number + 1 (`REV-200` seeded, so the first created ticket is `REV-201`); a page body registered in the ticket store for a run is keyed by the tracker ticket's key. **Scripted edits used by the criteria**: the ticket created in AC20 is titled `Review: Catalog Search`; page version 2 (AC21) appends the clause `Search results shall be limited to 50 items per page.` (no vague term → facts 5, ambiguities 3); page version 3 (AC22) appends `Typo tolerance should be configurable easily.` (`easily` → facts 6, ambiguities 4).
- `ScriptedGrader(fail_completeness_first_pass_on={...})` — a second grader mode, keyed on ticket ids like `error_on`: on the named tickets, the **first** grading pass additionally marks completeness failed with gap `Clause "<first clause>" is not addressed.` (so that pass fails all three criteria); later passes judge normally.

### 5.2 Replayed expectations (what the fixtures yield; the ACs assert these numbers)

- Plain review run on `SRCH-12`, 2 simulated failures, cap 12: model turns = **9** (3 fetch attempts + 1 write + 4 edits + final), trace steps = **17** (9 model rows + 8 tool rows), `stage_order = [Confirmed Facts, Ambiguities, Clarification Questions, Assumptions, Summary]`, counts 4/3/3/3, summary words = 21, complete = true, `stopped_by = finished`.
- Plain review run on `NOPE-1`, 2 simulated failures, cap 12: the first two fetch results are the two simulated error texts, every later one the not-found error; 12 model turns, all `fetch_requirement`, 24 alternating rows plus the appended stop row = 25 trace rows; no file; last trace action `Stops: turn limit of 12 reached`.
- Verification run on `EXP-31` under `agents_v1.md`, 0 failures, budget 3: grading pass 1 = `needs_revision` with criteria (by position) completeness ✓, clarity ✗, depth ✗; the reviewer revises in one edit; pass 2 = `satisfied`; status `satisfied`; turns = **9** (7 before the first verdict + 2 for the revision); counts 4/3/3/3 before and after.
- Batch `v1` under `agents_v1.md`: every run has 2 passes (`needs_revision`, `satisfied`); summary first-attempt completeness 5/5, clarity 0/5, depth 0/5, `revisions_needed = 5`; attempts total = 10. Batch `v2` under the applied instructions: every run 1 pass `satisfied`; 5/5 on all three; `revisions_needed = 0`; attempts = 5. `compare(v1, v2)`: `success`, improved `[clarity, depth]`, regressed `[]`.
- Batch `v1mix` (`fail_completeness_first_pass_on={"BATCH-03"}`): run 03's first pass fails all three criteria and its second pass is `satisfied`; summary completeness 4/5, clarity 0/5, depth 0/5, `revisions_needed = 5`; the analyst's `rejected` = `["completeness failed first attempt in 1 of 5 runs; a minority is not a pattern."]`, its `change` still `INSERTION`.
- Authored summaries: `before` vs `after_regression` → `regression` (regressed `[completeness]`, improved `[clarity, depth]`); `before` vs `after_partial` → `partial` (improved `[clarity]`); `before` vs `after_noeffect` → `no effect`.

### 5.3 Criteria (Given / When / Then; every AC cites its rules; `live` = needs a provider key and is excluded from the offline run)

| AC | Given | When | Then | Rules |
|---|---|---|---|---|
| AC1 | A fresh checkout; `fixtures/tickets.json`; a new workspace directory seeded with `agents_v1.md` as `/memories/AGENTS.md` | The ticket store is loaded and the review agent is built against that workspace | The store resolves exactly the six ids `SRCH-12, EXP-31, BKP-44, SESS-58, INV-63, ONB-77`; the workspace contains `memories/AGENTS.md` and no `analysis.md`; the build succeeds and exposes its turn cap (12) and simulated-failure count (2) | (R4, R5, R6, R8) |
| AC2 | The agent of AC1 with the scripted reviewer | A plain review run is started for `SRCH-12` | The opening message is `The requirement document is tracked in Jira as ticket SRCH-12. Fetch it to begin.` and contains none of the four clauses; the first model turn calls `fetch_requirement` with `ticket_id = "SRCH-12"` | (R1) |
| AC3 | As AC2 | The run finishes | `trace` has 17 steps; the model rows' tool calls, in order, are `fetch_requirement ×3`, `write_file: Confirmed Facts`, `edit_file: Ambiguities`, `edit_file: Clarification Questions`, `edit_file: Assumptions`, `edit_file: Summary`, then `Finishes the review`; `turns = 9`; `stage_order` equals the five sections in R2's order; `stopped_by = finished`; the record validates against §3 `ReviewRun` | (R2) |
| AC4 | As AC3 | `/analysis.md` is parsed | Headings are exactly the five of R2 in order; Confirmed Facts has 4 bullets equal to the four clauses verbatim; Ambiguities has 3 bullets whose `clause` values are clauses 2, 3, 4 verbatim and whose `reason` lines start `Reason:`; `resolved_by` and `edge_case` are null on all three; Clarification Questions and Assumptions have 3 bullets each; `summary_words = 21`; `complete = true` | (R2, R3) |
| AC5 | As AC3 | The first six trace steps are inspected | They are three `fetch_requirement` calls with identical `args`, whose tool results are, in order, the `503 Service Unavailable` text, the `request timed out after 10s` text, and the `SRCH-12` document; `stage_order` is unaffected; the two error results are recorded as errors | (R4) |
| AC6 | The agent of AC1 (cap 12, 2 failures) | A plain review run is started for `NOPE-1` | Every `fetch_requirement` result after the two simulated errors is `Error fetching ticket from Jira: no ticket 'NOPE-1' found.`; the reviewer re-calls the tool with identical args each turn; the run ends without an exception after `turns = 12`, all of them fetch calls; `trace` has 25 rows — 12 model rows each followed by its tool row, then the appended row `Stops: turn limit of 12 reached`; `stopped_by = turn_limit`; `analysis_markdown = ""`; `complete = false` | (R4, R5) |
| AC7 | `fixtures/bare_workspace/` | The review agent is built against it | The build raises an error whose message contains `memories/AGENTS.md`; no run starts; no file is created in the directory | (R6) |
| AC8 | A workspace as AC1; `ScriptedReviewer(rogue_write=True)` | A plain review run for `ONB-77` | The first tool result is an error; `/memories/AGENTS.md` is byte-identical to `agents_v1.md` after the run; the run then completes with counts 2/1/1/1 and `stopped_by = finished` | (R7) |
| AC9 | A workspace as AC1 with `fixtures/secret.txt` placed in its parent directory; `ScriptedReviewer(escape_read=True)` | A plain review run for `ONB-77` | The first tool result is an error; the string `TOP-SECRET-VALUE` appears in no message, trace row or file inside the workspace; the run completes | (R8) |
| AC10 | `fixtures/stale_workspace/`; `ScriptedReviewer(probe_stale=True)` | A plain review run for `EXP-31` | The probe's `read_file("/analysis.md")` returns an error (file absent at the first model call); the final file contains no `STALE-MARKER`; Confirmed Facts has 4 bullets equal to `EXP-31`'s clauses | (R8) |
| AC11 | The record of AC3 | Its trace is validated | Every step validates against §3 `TraceStep`; actors alternate beginning with `Model reasoning`; every `detail` is ≤ 220 characters or exactly 220 characters followed by `…`; the tool row for the third fetch carries the whole `SRCH-12` document text, whitespace-collapsed (it is under 220 characters); `workspace` names the directory the run used | (R9) |
| AC12 | A workspace as AC1; scripted reviewer + `ScriptedGrader`; `rubric.txt`; budget 3; 0 failures; cap 40 | A verification run for `EXP-31` | The grader's first tool call in pass 1 is `read_file("/analysis.md")` and its observation is byte-identical to the workspace's `analysis.md` at that moment; `grading[0].analysis_markdown` equals that same text | (R10) |
| AC13 | As AC12 | `grading[0]` is inspected | `result = needs_revision`; `criteria` has 3 entries whose positions map to `completeness, clarity, depth` from `rubric.txt`; `[0].passed = true`, `[1].passed = false` with gap `Each Ambiguities bullet needs an indented "Resolved by:" line; bullet 1 has none.`, `[2].passed = false` with gap `Each Ambiguities bullet needs an indented "Edge case:" line; bullet 1 has none.`; the explanation quotes a line with a line number for completeness; every Ambiguities bullet in `grading[0].analysis_markdown` has `resolved_by = null` | (R10, R11, R13) |
| AC14 | As AC12 | The run finishes | `grading` has exactly 2 passes; `grading[1].result = satisfied` with all three `passed = true`; `status = satisfied`; `turns = 9`; the final file's 3 Ambiguities bullets each have non-null `resolved_by` and `edge_case` (lines starting `  Resolved by:` / `  Edge case:`); `counts` = 4/3/3/3, and the counts of `grading[0].analysis_markdown` are the same 4/3/3/3; the record validates against §3 `VerificationRun` | (R3, R11, R12, R13) |
| AC15 | As AC12 but `ScriptedReviewer(stubborn=True)` | A verification run for `EXP-31` | `grading` has exactly 3 passes, all `needs_revision`; `status = max_iterations_reached`; the file is unchanged between passes 1 and 3; the run ends without exception | (R12) |
| AC16 | As AC12 but budget 0 | A run for `EXP-31` | The scripted grader's `.calls = 0`; the run is a plain `ReviewRun` (no grading passes) with counts 4/3/3/3 and `stopped_by = finished` | (R12) |
| AC17 | As AC12 but `ScriptedGrader(error_on={"BKP-44"})` | A verification run for `BKP-44` | The run completes; `grading` has exactly 1 pass with `result = grader_error`, `criteria = []`; `status = grader_error`; the file is complete with counts 3/2/2/2 | (R10) |
| AC18 | As AC12 but `rubric_empty.txt` | A verification run for `SRCH-12` | `grading` has exactly 1 pass with `result = failed`, explanation `Rubric has no criteria.`, `criteria = []`; `status = failed`; the reviewer made no revision edit (the trace's last model action is `Finishes the review` and the file has null `resolved_by` on every bullet) | (R10) |
| AC19 | An empty data directory; the event app configured as in 5.1 | The app starts | `pages.json` holds exactly one page: `id = page-req-catalog-search`, `kind = requirement`, title `Catalog Search — Requirements`, one version `n = 1` by `Priya (Product Manager)` whose body is `SRCH-12`'s four clauses separated by blank lines; `tickets.json` holds exactly one ticket `REV-200` (`status = Open`, `linked_page_id = page-req-catalog-search`, assignee `Theo (Eng Lead)`, `last_run_id = null`); `analysis_runs.json` is `[]`; all three validate against §3 | (R14) |
| AC20 | The app of AC19 | A ticket titled `Review: Catalog Search` is created linked to `page-req-catalog-search` | The new key is `REV-201`; a run executes; afterwards `REV-201` has `status = Analysis Ready`, `last_analyzed_version = 1`, `last_run_id` matching `^[0-9a-f]{8}$`, exactly one comment authored `Requirements Analysis Agent (bot)` containing `satisfied` and `version 1`; a page `page-analysis-rev-201` of `kind = analysis_report`, title `Analysis Report — REV-201`, `linked_ticket = REV-201`, exactly one version by the bot author whose body starts with the three banner lines (`from REV-201`, `version 1.`, `**satisfied** after 2 grading pass(es).`) and then equals the run's `analysis_markdown`; the `AutomationRun` record has `counts` 4/3/3/3 and `requirement_version = 1`; the agent's opening message named `REV-201` and its fetch returned the page body | (R1, R14, R15, R16) |
| AC21 | The app after AC20 | Version 2 of the requirement page is saved by `Mina (QA Lead)` with the extra clause `Search results shall be limited to 50 items per page.` | The page has 2 versions, both authored by people (no bot author ever appears on a `requirement` page); runs execute for **both** `REV-200` and `REV-201` (both not Done); each now has `last_analyzed_version = 2` and `status = Analysis Ready`; `page-analysis-rev-201` has 2 versions; `page-analysis-rev-200` exists with 1 version; both latest runs have `counts` 5/3/3/3 | (R14, R15) |
| AC22 | The app after AC21 | `REV-201` is marked Done by a person; then version 3 of the page is saved with the extra clause `Typo tolerance should be configurable easily.` | `REV-201` has `status = Done`, `last_analyzed_version` still 2 and the same run count as before; `REV-200` is re-run: `last_analyzed_version = 3`, latest `counts` 6/4/4/4; no run record references `REV-201` with `requirement_version = 3` | (R14, R16) |
| AC23 | The app after AC22 | The ticket page for `REV-200` and the compare view of `page-analysis-rev-200` versions 1 and 2 are rendered | The ticket page's "What changed since the previous run" table shows requirement versions `2` and `3`, statuses `satisfied` and `satisfied`, and bullet counts `5 / 3 / 3 / 3` vs `6 / 4 / 4 / 4` for the four list sections; the compare view shows a unified diff containing the added line `- Typo tolerance should be configurable easily.` as an addition and the two runs' statuses and counts | (R17) |
| AC24 | The app after AC23 | "Re-run analysis now" is triggered on `REV-200` | A third run record for `REV-200` exists with `requirement_version = 3`; all run ids in `analysis_runs.json` are distinct 8-hex strings; the app's per-run workspace root contains no run directory after the run; `page-analysis-rev-200` has 3 versions | (R8, R14) |
| AC25 | `fixtures/requirement_docs/`, `agents_v1.md`, `rubric.txt`, scripted reviewer + grader, a temporary history root | Batch `v1` is generated | `v1/AGENTS.md` is byte-identical to `agents_v1.md`; files `run_01_01_catalog_search.json` … `run_05_05_inventory_sync.json` exist, each validating against §3 `RunRecord`, with `instructions` equal to `agents_v1.md`, `label = v1`, exactly 2 grading passes `[needs_revision, satisfied]`, `status = satisfied`, `workspace` ending `ws_01` … `ws_05` respectively; every `messages[]` entry with tool calls carries full `args`; each run's first human message names ticket `BATCH-<NN>` and its `requirement_doc` equals the document file | (R18) |
| AC26 | The batch of AC25 | `v1/summary.json` is read | `runs = 5`, `graded = 5`, `grader_errors = 0`; `first_attempt` keys are exactly `completeness, clarity, depth` (from the rubric, in order) with `passed/total` = `5/5`, `0/5`, `0/5` and `pass_rate` `1.0`, `0.0`, `0.0`; `revisions_needed = 5`; `documents` = the five stems in order | (R13, R18) |
| AC27 | As AC25 but `ScriptedGrader(error_on={"BATCH-03"})` | Batch `v1err` is generated | `run_03_03_nightly_backups.json` has one pass `grader_error`; `summary.json` has `runs = 5`, `graded = 4`, `grader_errors = 1`, every `total = 4`, clarity `passed = 0`, completeness `passed = 4`, `revisions_needed = 4` | (R18) |
| AC28 | The batch of AC25; `ScriptedAnalyst` | The analyst is run over `v1` | It returns a `HarnessChange` with `target = prompt`, `section = ### Ambiguities`, `change` equal to `INSERTION`, `recurrence` = `5/5 runs: 01_catalog_search, 02_account_data_export, 03_nightly_backups, 04_session_timeout, 05_inventory_sync failed first attempt on clarity and depth.`, `evidence` = five entries each equal to the clarity gap string of AC13, `rejected = []`; `<root>/proposal.md` exists with the five headings of 5.1; `proposal_v1.md` and `proposal_v1.json` exist beside `v1/`; every file under `v1/` is byte-identical to before the analyst ran, and so is `agents_v1.md` | (R19, R20) |
| AC29 | As AC28 but `ScriptedAnalyst(tamper=True)` | The analyst is run over `v1` | Its first tool result is an error; `v1/summary.json` is byte-identical to before; the analyst still returns the AC28 `HarnessChange` | (R19) |
| AC30 | `agents_v1.md`; the `HarnessChange` of AC28; `harness_change_tool.json`, `harness_change_grader.json`, `harness_change_configuration.json`; `harness_change_badsection.json` | Apply is invoked five times | (1) applying the AC28 change to `agents_v1.md` yields text byte-identical to `agents_v2_expected.md` (43 lines); (2) each of the `tool`, `grader` and `configuration` changes raises an error whose message contains that target word; (3) the bad-section change raises an error whose message contains `### Glossary`; in (2) and (3) nothing is written | (R20) |
| AC31 | The result of AC30 (1) written to a file; the batch of AC25 | Batch `v2` is generated under the applied instructions and `compare(v1, v2)` is computed | Every `v2` run has exactly 1 pass `satisfied`; `v2/summary.json` has `5/5` for all three criteria and `revisions_needed = 0`; the comparison has `verdict = success`, `criteria` = `completeness [5, 5]`, `clarity [0, 5]`, `depth [0, 5]`, `revisions_needed = [5, 0]`, `attempts = [10, 5]`, `improved = [clarity, depth]`, `regressed = []`; it validates against §3 `Comparison` | (R18, R21) |
| AC32 | `fixtures/summaries/` | `compare` is computed for `before` against each `after_*` | `after_regression` → `verdict = regression`, `regressed = [completeness]`, `improved = [clarity, depth]`, `attempts = [9, 6]`; `after_partial` → `partial`, `improved = [clarity]`, `regressed = []`; `after_noeffect` → `no effect`, `improved = []`, `regressed = []` | (R21) |
| AC33 `live` | `OPENAI_API_KEY` set; row L4's course models; `agents_v1.md`; `rubric.txt`; budget 3; cap 40 | A verification run for `SRCH-12` | The run ends with `status = satisfied` within 40 turns; `grading` has ≥ 1 pass; the final file is complete and every Ambiguities bullet has non-null `resolved_by` and `edge_case` | (R12) |
| AC34 `live` | A live `v1` batch and the course's analyst model | The analyst is run over it | It returns a `HarnessChange` validating against §3 with `target = prompt`, non-empty `change` and ≥ 1 `evidence` entry; `proposal.md` exists; no file under `v1/` changed | (R19) |
| AC35 | `OPENAI_API_KEY` unset and outbound network disabled | The whole offline suite (AC1–AC32, AC36–AC38, minus any criteria retired by a row D1 or D2 choice) is run | Every criterion passes; no provider client is constructed; no file written by any run contains the string `sk-` | (R22) |
| AC36 | A workspace as AC1; `ScriptedReviewer(dup_edit=True)` | A plain review run for `SRCH-12` | The trace contains an `edit_file` tool row recorded as an error, followed by a `read_file` and a successful `edit_file: Ambiguities`; `stage_order` still equals the five sections in order; the run completes with counts 4/3/3/3 | (R2, R9) |
| AC37 | As AC25 but `ScriptedGrader(fail_completeness_first_pass_on={"BATCH-03"})`; `ScriptedAnalyst` | Batch `v1mix` is generated and the analyst is run over it | `run_03_03_nightly_backups.json` has 2 passes, the first with all three `passed = false` (completeness gap `Clause "The system shall back up all customer data every night." is not addressed.`), the second `satisfied`; `v1mix/summary.json` has completeness `4/5`, clarity `0/5`, depth `0/5`, `revisions_needed = 5`; the `HarnessChange` has `change = INSERTION`, `recurrence` naming `5/5 runs`, and `rejected = ["completeness failed first attempt in 1 of 5 runs; a minority is not a pattern."]` | (R18, R19) |
| AC38 | As AC12 but `ScriptedReviewer(claim_in_message=True)` | A verification run for `EXP-31` | `grading[0].result = needs_revision` with clarity and depth `passed = false` and the gaps of AC13, although the transcript's final message claims the lines; the grader's pass-1 explanation quotes no `Resolved by:` line; the run then ends `satisfied` after the revision, as in AC14 | (R10) |

## 6. Standing Permissions (in force for the entire build)

**Always**
- Build on the resolved-decision checklist of §0; every Ledger default not changed there is binding.
- Run the offline suite (§7) before claiming any criterion; cite the test output per AC.
- Keep the agent's instructions, the rubric and the fixtures as declared files; read parameters from them, never duplicate them in code.
- Record every run (trace, grading passes, batch files, automation runs) exactly as §3 declares, including `workspace` on every run record and `stopped_by` on plain review runs.
- Keep `.env` gitignored and read secrets only through it.

**Ask First** — derived from the course's spoken trade-offs (the CTX-C table marks each with its line); each would silently change a behavior guarantee or force rework without failing an offline criterion:
- Changing the model or provider for any of the three roles, including giving the grader a different model from the reviewer (row L4; course: a separate grader is "a common production choice", the analyst needs the stronger model). Changes every verdict and proposal; no offline test sees it.
- Changing the rubric text or adding a criterion (row L3). Changes what "done" means and what the learning loop diagnoses; existing run histories stop being comparable (rework: re-run every batch).
- Changing a post-build lever: the revision budget (3; the course also used 2), the turn caps (12 / 40), the simulated-failure counts (2 / 0), or the "most runs" threshold (> ½). Each moves a safety net or the diagnostic signal without failing an AC.
- Dropping or adding a loop after the gate (row D1), or changing who owns the grader (row D2).
- Turning on hosted tracing (row RR2): it sends every prompt and tool result to a third-party service and needs a key.
- Adding a scheduled trigger or memory consolidation (Not Included 2–3): named by the course, never built, no parameters or criteria here. Switching to a real tracker is row L2's option (Not Included 1 defers to it).
- Applying a proposal whose `target` is not `prompt` by hand (R20 refuses it in code): only a person may decide, and only after the same batch re-run and comparison of R21.

**Never**
- Apply an analyst proposal automatically, without a person's approval, or let the analyst write anything but `/proposal.md` (R19, R20).
- Let the agent write under `/memories/`, edit the requirement page, or mark a ticket Done (R7, R15, R16).
- Grade from the conversation instead of the file, or pass a criterion without a quoted line (R10).
- Count a `grader_error` run as a pass, or hide it from the summary (R18).
- Modify a fixture, the scripted model's declared responses, or an expected file to make a test pass; mark a criterion passed without running it.
- Invent provenance: never attribute to the course anything this spec labels project hardening.
- Commit secrets or write a key into any record, trace, page or log (R22).

## 7. Test Plan & Self-Verification

Commands (from the project root, inside the virtual environment):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # pins of §2
cp .env.example .env                     # placeholders only; leave OPENAI_API_KEY empty for the offline run
pytest -m "not live" -q                  # offline suite: AC1–AC32, AC35–AC38 (AC35 runs the others with the key unset and sockets disabled)
pytest -m live -q                        # AC33–AC34, only with OPENAI_API_KEY set
python -m app.tracker                    # the event-loop simulation on http://localhost:5050 (live model unless the scripted stand-in is selected)
python -m app.batch --label v1 --agents fixtures/agents_v1.md      # generate a batch
python -m app.analyze --label v1                                   # analyst → proposal_v1.md / proposal_v1.json
python -m app.apply --proposal run_history/proposal_v1.json --agents fixtures/agents_v1.md --out workspace/memories/AGENTS.md
python -m app.batch --label v2 --agents workspace/memories/AGENTS.md && python -m app.compare v1 v2
```

Test organisation: one test per AC, named `test_ac<N>_<slug>`, with `@pytest.mark.live` on AC33 and AC34. AC35 wraps the offline suite in a subprocess with `OPENAI_API_KEY` removed from the environment and a socket guard that fails any outbound connection.

**Reporting.** The building agent MUST report results **per acceptance criterion** with cited evidence: the pytest line for that test, and for file-producing criteria the path of the produced record (run JSON, summary, proposal, page store). "Should pass", "looks correct" and "implemented as specified" are treated as failures — they mean the test was not run. A criterion whose test was skipped is reported as not passed, with the reason.

Conclude the build with a short infra/structure diagram of the app as built — the components, the three JSON stores and per-run workspaces, and the four loops with their arrows — ending with the exact sentence "This is the infra/structure diagram of this app".

## Course Context Pack (embedded — agent-readable)

Concepts only; no course code. Referenced by position-independent `CTX-*` anchors.

### CTX-A. The pattern

The course's central buildable pattern is one pipeline of four nested loops around a single agent:

`fetch → draft the analysis file stage by stage → agent declares done` **(agent loop)** `→ grader reads the file and scores each rubric criterion → retry with feedback until all pass or budget spent` **(verification loop)** `→ an event in the surrounding system (ticket created, requirement edited) starts the loops and the result is written back into that system` **(event-driven loop)** `→ many recorded runs → an analyst finds what recurs → one proposed instruction change → human approval → apply → re-run and compare` **(learning loop)**.

Why each stage exists:
- *Fetch by id* — the agent must reach the document the way it would in a real tracker: by identifier, through a tool that can fail; the opening message never carries the text (so the tool path, the retry behavior and the event trigger are all exercised).
- *A file, filled stage by stage* — a file is something a person can open and a grader can read; one stage per call keeps each turn's responsibility visible in the trace. The analysis has four list sections (what the document states; what is under-specified, quoting the clause; what to ask before work starts; what a developer would assume if nobody answers) and a prose summary.
- *An always-loaded instructions file* — the part of the harness that is revisable lives in a file loaded at the start of every run, separate from the fixed procedure; its absence must be loud, and the agent must not be able to write it. The course's harness primer shows three instruction channels — a system prompt (fixed at build), an always-loaded file (what is always true), and skill files loaded on demand by description (progressive disclosure keeps a large library cheap); this agent uses the first two.
- *A turn cap* — the normal stop is the agent's own; the cap exists for the path where the agent keeps retrying past the point where retrying makes sense.
- *A grader that reads the file* — "the agent says it is done" is not "good enough"; a grader with explicit pass/fail criteria is what adds reliability, and is what makes a cheaper model viable on a harder task. Graders may be a model, deterministic code, or a person (row D2).
- *Retry with feedback, bounded* — the gaps go back into the agent's conversation; all criteria must pass in the same pass; a budget bounds the cycle.
- *Event triggers* — agents have little value unless they are easy to use; looping the agent into the system where the work already happens (a ticket created, a page edited) is what gets it used. The agent writes to its own page, never the source document; a person decides when the work is done.
- *Traces* — agents are non-deterministic, so "the story is in the traces"; every run is recorded with every message and every grading pass.
- *The learning loop* — one run's correction is forgotten tomorrow; across many runs the same correction recurring is a property of the agent, not of a document. An analyst reads the batch, proposes one literal change to the instructions, a person approves, code applies it, and the batch is re-run so the change is measured rather than trusted. The course's own result: first-attempt clarity and depth went from 0 of 5 to 5 of 5 after one approved insertion.
- *Human oversight at four points* — sensitive tool calls, the grader, the artifact before delivery, and harness changes; this build has the last two (a person marks Done; a person approves the proposal).

Name-map to the course's own terms (provenance, not binding): the course's example is a "Requirements Review Agent" / "requirements analysis agent"; its instructions file is `AGENTS.md` under `memories/`; its analysis file is `/analysis.md`; its fetch tool is `fetch_requirement` (one of its instruction snapshots says `fetch_requirement_from_jira`); its default ticket is `AUTH-142` ("User Profile File Upload") and its batch documents are five requirement texts (user authentication, notification system, payment retry policy, access control rules, alert escalation rules); its tracker simulation seeds ticket `REQ-104`; its batch labels are `v1`/`v2`; its analyst's structured result is a `HarnessChange`; its loop diagrams colour the agent loop lavender, the grader green, the event loop blue and the analysis orange-red. The course calls the fourth loop the "hill-climbing", "learning" and "self-improvement" loop interchangeably. Presentation-only constants dropped by declaration: the course's fixed cast of five assignee names, its CSS palette, its notebook card styles, and its LangSmith project names.

### CTX-B. Failure-mode catalog

Each entry: symptom → cause → fix → enforced by.

- **CTX-B1 — Transient fetch failure.** Symptom: the first call to the external system returns "503 Service Unavailable", the second "timed out". Cause: external systems are flaky; a tool that raises would end the run. Fix: the tool returns the error as an observation and the instructions say to call the same tool again with the same arguments; the failure count is deterministic so a captured trace reproduces. Enforced by R4, AC5; fixture: the simulated-failure count R4 declares (2 for the plain run), exercised on `SRCH-12`.
- **CTX-B2 — Retrying past the point of sense.** Symptom: a ticket that does not exist is fetched again and again. Cause: "keep retrying until it succeeds" has no exit when the error is permanent. Fix: a model-call cap ends the run cleanly and the record says the cap, not the agent, stopped it. Enforced by R5, AC6; fixture: `NOPE-1`.
- **CTX-B3 — Missing instructions, silently.** Symptom: the agent produces a plausible but wrong review. Cause: the harness's memory loader ignores a missing instructions file, so the agent runs on the one-line system prompt. Fix: refuse to build when the file is absent, naming the path. Enforced by R6, AC7; fixture: `bare_workspace/`.
- **CTX-B4 — The agent rewrites its own instructions.** Symptom: the instructions file changes mid-run. Cause: the agent has an edit tool and the file sits in the same writable filesystem. Fix: deny writes under the instructions directory by permission, not by prompt. Enforced by R7, AC8; fixture: `rogue_write` mode.
- **CTX-B5 — A stale analysis, or an escape from the workspace.** Symptom: a re-run skips stages, or a run reads a file it should not see (the repository holds a real `.env`). Cause: a finished analysis from the previous run is still on disk; a non-confined backend resolves `..`. Fix: delete the leftover before each run, one directory per run, a virtual-root backend that cannot resolve above `/`. Enforced by R8, AC9, AC10, AC24; fixtures: `stale_workspace/`, `secret.txt`, `escape_read` / `probe_stale` modes.
- **CTX-B6 — The grader passes by resemblance.** Symptom: criteria pass that the file does not satisfy. Cause: the grader is handed the transcript, which can read as if the work were done; it judges from how the conversation looks. Fix: give the grader a read-only file tool, require it to read the file first, and to quote the satisfying line with its number before passing anything. Enforced by R10, AC12, AC13, AC38; fixture: `claim_in_message` mode — a transcript that asserts the labelled lines while the file lacks them.
- **CTX-B7 — The first attempt lacks the resolving fact and the consequence.** Symptom: the ambiguity is found and its reason given, but nothing says what would resolve it or what goes wrong if it is not; clarity and depth fail, completeness passes. Cause: the instructions ask only for a quoted clause and a reason; the rubric asks for two labelled lines the instructions never mention; the grader applies labels literally. Fix: feedback names exactly what is missing; the agent revises; across many runs the recurrence becomes the learning loop's proposal. Enforced by R3, R11, R12, AC13, AC14; fixture: `agents_v1.md` without the labels.
- **CTX-B8 — The requirement changes after the analysis.** Symptom: the analysis describes a document nobody uses any more. Cause: nothing re-runs when the source page is edited. Fix: saving a new page version re-runs every linked ticket that is not Done; the report page's version history and the counts table show what changed. Enforced by R14, R17, AC21, AC22, AC23; fixture: the page versions 2 and 3 declared in 5.1.
- **CTX-B9 — A grader error counted as a pass.** Symptom: a batch looks cleaner than it is. Cause: when the grader itself fails, the harness records a pass with no criteria; averaging it in reads as "nothing failed". Fix: an ungraded run is excluded from every denominator and counted separately. Enforced by R18, AC27; fixture: `error_on` mode.
- **CTX-B10 — A one-off treated as a pattern.** Symptom: the instructions grow a rule for something that happened once (the course's analyst noted duplicate headings and edit errors in some runs and rejected them). Cause: anecdote mistaken for signal. Fix: only a criterion failing in most first attempts becomes a change; the rest is listed under `rejected`. Enforced by R19, AC28, AC37; fixture: batch `v1mix`, where completeness fails in one run of five and lands in `rejected`.
- **CTX-B11 — A harness change merged on faith.** Symptom: an instruction edit is applied and nobody knows whether it helped or regressed something. Cause: no eval to validate the change. Fix: the analyst only proposes; a person approves; code applies the literal text at a named section; the batch is re-run and compared per criterion, and a regression blocks adoption. Enforced by R20, R21, AC30, AC31, AC32; fixtures: `harness_change_*.json`, `summaries/`.
- **CTX-B12 — An edit the tool rejects.** Symptom: an `edit_file` fails because its target string is not unique. Cause: the model chose an ambiguous anchor. Fix: the error is an observation; the model reads the file and retries; the trace records the failed edit and the stage counts only on success. Enforced by R9, AC36; fixture: `dup_edit` mode.

### CTX-C. Decision background

**How to read the provenance notes.** *Litmus branch* — every subject the course argued was sorted one of three ways: a **row** (it entered the Decision Ledger because choosing differently changes the system's structure or the course argued two sides); a **bake-in** (it became a business rule, because the course showed the other side only as a failure, or there was no second side); or a **lever** (the sides differ only in a value, so it stays a body default with a §6 Ask-First entry). *Lever* — a value the course set, carried as a body default; a *post-build lever* is one you may change after the build without re-opening the gate. *Lever-value branches* — when the course set a value inconsistently, the value was chosen by, in order: (1) what the narration states aloud in the lesson that introduces it; (2) the end-to-end application's config; (3) the most frequent value, earliest-taught on ties. *Stakes* — a contradiction earns a row only if picking the other side up front would change structure, semantics or a guarantee; otherwise it is a lever. *Substitution row* — a row whose Default departs from what the course ran because the course's choice needs setup you may not have; the course's choice stays in Options tagged "(course default)". *Heavy bar* — a realization is heavy only if it needs a credential, a paid account, admin/container setup, or special hardware; network access alone is not heavy. *Realization tiers* — among realizations satisfying a row's invariant, the lightest is chosen by tier: (1) ships with the language, (2) an embedded library, (3) a locally served process; judged at the fixture scale. *Branch* (in a Ledger Default cell) — which precedence the generator took to pick that default: for the project row, "course-example shape re-expressed on authored fixtures" versus "generic minimal instantiation"; for a dependency row, "reproduce the course's realization" (keyless) versus "substitute the lightest realization" (heavy) versus "the course's technology is the taught subject". *Generator's reading / quantification* — a number this spec assigned to words the course left unquantified ("most runs", "the number of times the grader may send work back"); always a post-build lever. *Course-demonstrated* — a rule or value traceable to the supplied course materials; *project hardening* — this spec's own addition, which the course did not demonstrate. *Narrative* (a disposition in the trade-off table) — a spoken trade-off that produced neither a row, a rule nor a lever and is carried only as background here. *Category values* — `learner` (a learner-context dimension), `design-structural` (choosing differently changes the system's structure: a box, arrow, owner or guarantee), `design-argued` (the course argued two sides; none in this spec), `realization` (a heavy dependency resolved by the branch note), `contradicted` (the course set it both ways and the stakes test passed; none in this spec). *Branch* on a design row — simply which of the course's demonstrated forms the Default is. *Learner intake brackets* (`[project]`, `[data]`, `[goal]`, `[model]`, `[environment]`) — a value a learner may substitute at build time; never empty, since each carries its row's default. *Owner* values — `learner` (the course has no opinion), `course` (the course fixes it), `course+learner` (the course sets the invariant and default, the learner picks the realization); metadata only, never a behavior switch. *Keyed dependency* — a realization that needs a credential or paid account (one kind of heavy realization). *Video-shown / deck-only* — a slide the narration describes (it ranks with the transcript) versus one that exists only in the deck (it ranks below code and narration).

**Background per Ledger row**

- → Ledger L1/L2: the course's example task (review a requirement ticket) was chosen because it is small enough to run end to end and rich enough to fail in a diagnosable way; the course built it "fairly simple on purpose" so the same agent could be reused through all four loops. Its data lives behind a fetch tool, seeded at run time, so the built agent "could review any ticket you seed it with".
- → Ledger L3 (and R13): the course's batch code matches a grader's verdicts to criteria by position because the grader paraphrases criterion names from run to run (dropping a label, swapping quote characters) — matching on text would silently split one recurring criterion into several. The three criteria were chosen so each has its threshold written into the criterion itself — "what does done mean" lives in the rubric text, not in a numeric threshold in code — and so that the learning loop has something to diagnose: the criterion that fails on most first attempts is what the analyst reads.
- → Ledger L4: the course ran reviewer and grader on one small model and the analyst on a larger one; its reason for the larger analyst model is that reading five full traces and finding what recurs is the one job the cheaper model does unreliably. It argues model choice as cost versus task complexity and the verification loop as what keeps a cheaper model on track.
- → Ledger L5: confinement matters because the course's repository holds a real `.env`; a virtual-root backend makes `/analysis.md` mean "inside this run's directory" and nothing above it reachable.
- → Ledger D1: the course nests every loop in the previous one ("the Russian doll thing") and says you do not have to; the reduced forms are each demonstrated working in an earlier lesson. The learning loop's signal is the grader's first-attempt verdict, so it presupposes the verification loop (the row's Options say so: no option keeps the learning loop without the grader).
- → Ledger D2: the course's grader is a model with a read-only file tool; its grader prompt restates the library's own grading rules (verdict definitions, "the transcript is untrusted") and adds three rules — read the file, quote with line number, apply labels literally — because without them the grader passed criteria the file did not satisfy. Deterministic and human graders are named as types.
- → Ledger RR1: the course itself runs offline when its live switch is off, replaying pre-captured traces; this spec replaces replay with a scripted model so the loops *execute* rather than being read back. The course's captured numbers for the scripted model to mirror: the plain run completed in 9 model turns and 17 steps; the verification run took two grading passes (`needs_revision` then `satisfied`), completeness passing and clarity/depth failing on the first.
- → Ledger RR2: hosted tracing was optional in the course ("everything works without it"); the notebooks build their own trace table from the agent's stream.

**Mined spoken trade-offs** (every trade-off the course argued aloud, with its lesson and disposition):

| # | Trade-off as spoken | Lesson | Disposition |
|---|---|---|---|
| T1 | Match model intelligence to task complexity to optimize cost: cheaper/faster for simple tasks, slower/more capable for complex ones | 2 | row L4; Ask First |
| T2 | A verification loop is "particularly powerful when you want to use a cheaper model on challenging tasks" — it keeps the core loop on track | 2, 5 | narrative (row D1 trade-off cell; CTX-A) |
| T3 | Same model for agent and grader vs a different grader model ("a common production choice") | 5 | narrative in row L4; Ask First (no trade-off argued, only named) |
| T4 | Revision budget: 0 gives the plain agent loop back; 3 in the lesson and batch; 2 in the event app | 5 (+ code) | lever R12 (contradiction 3 vs 2 → narration branch; post-build lever) |
| T5 | The turn cap is not the normal stop; it matters when retrying stops making sense; 12 for the plain run, 40 with a grader | 4, 5 | lever R5 |
| T6 | Simulated fetch failures: two in the narration and the captured trace, zero in the module constant and in the batch/event code | 4 (+ code) | lever R4 (contradiction → narration branch for the plain run; 0 where a grader is attached, as the code states) |
| T7 | Loops are composable; you need not nest all four ("you don't need the verification loop per se") | 2 | row D1 (structural litmus) |
| T8 | Triggers can be scheduled or event-driven | 2 | narrative; scheduled trigger → Not Included 2 |
| T9 | Human oversight at four points: sensitive tool calls, the grader, artifacts, harness changes | 2, 6 | bake-in R16, R20 (artifact/harness points); row D2 option (human grader); Not Included 5 (tool-call approval) |
| T10 | "Hard to have confidence merging changes to your core harness if you don't have good evals" | 2 | bake-in R21 |
| T11 | Learning-loop improvements are procedural (prompts, tools, skills) or memory (preferences persisted across runs) | 2 | narrative; memory → Not Included 3 |
| T12 | Graders can be deterministic or agentic (LLM-as-judge) | 2 (video-shown slide) | row D2 |
| T13 | Three instruction channels: system prompt, always-loaded file, skills by progressive disclosure (cheap context for a large library) | 3 | bake-in R6; skills → Not Included 6 |
| T14 | A filesystem makes output "something you can open rather than something you have to parse out of a message" | 3 | bake-in R2 |
| T15 | A problem in one run of five is not a pattern; a criterion failing in most runs is a property of the agent | 6 (+ analyst prompt) | bake-in R19; lever (threshold > ½, generator's reading) |
| T16 | The analyst runs on the stronger model because the cheaper one reads traces unreliably | 6 (README) | row L4 trade-off; Ask First |
| T17 | Grade the file, not the transcript — otherwise the grader passes by resemblance | code (grader prompt comment) | bake-in R10 |
| T18 | The analyst proposes and does not apply; applying in plain code keeps the edit reviewable and deterministic | code (module docstring) | bake-in R20 |
| T19 | The agent writes to its own report page, never the source page; a human marks Done | event app README | bake-in R15, R16 |
| T20 | Bullet counts often look the same while the content changed completely — show counts and the text diff together | event app README | bake-in R17 |
| T21 | A checkpointer is not required for the rubric loop ("it revises correctly without one, measured") but is attached to match the library's documented shape | code comment | narrative (CTX-D) |
| T22 | Offline replay of captured traces vs live runs | notebooks, README | row RR1 |
| T23 | Hosted tracing is optional; everything works without it | 3, README | row RR2 |

**Contradictions mined** (both sides' sources; routed through the stakes test):
- Simulated failures 2 (Lesson 4 narration; notebook tool table; captured trace) vs 0 (module constant; batch and event code). Stakes: a knob → lever; chosen by branch (1) narration for the plain run (R4).
- Revision budget 3 (Lesson 5 narration and notebook; batch module) vs 2 (event app trigger). Stakes: a knob → lever; branch (1) (R12).
- The fetch tool's name in the instructions: `fetch_requirement` (tracked instructions file; the tool's definition; Lesson 4 narration) vs `fetch_requirement_from_jira` (the two batch instruction snapshots; the primer slide's code sample). The tool definition and narration agree, so the spec uses `fetch_requirement` (branch 1); the runs under the other name still succeeded, which is why it fails the stakes test. Recorded here only.
- Lesson numbering: transcripts count seven lessons (CTX-E); the course's folders number notebooks one lower and its README uses a third scheme; the event app has no transcript lesson at all. Transcripts win; the app is placed where the overview describes it.
- The notebook's live switch defaults on while the README says offline by default and promises an automatic fallback that no code implements. Resolved by row RR1: offline is this spec's default, by construction.

**Slide-only evidence**: the "deterministic or agentic grader" line (T12) and the four-point human-oversight slide (T9) are on video-shown slides and rank with their narration; the two event-driven-loop slides exist only in the deck (no transcript lesson) and add nothing beyond the overview's narration and the app's code. No slide conflicts with code or narration except the requirement's wording (the slide and the seed data say "Users shall be able to upload files to their profile. Uploaded files should be stored securely. The system should support common file types."; the narration paraphrases it) — no spec value depends on it.

### CTX-D. Perishable assumptions

Treat these as **search keywords against current documentation, not guaranteed imports**. The concepts in CTX-A…CTX-C are durable; only these names are perishable.

- Harness: `deepagents` 0.7.11 — `create_deep_agent(model, tools, system_prompt, memory=[…], backend, permissions, middleware, checkpointer, response_format)`; `deepagents.backends.FilesystemBackend(root_dir, virtual_mode=True)`; `FilesystemMiddleware(backend, tools=[…])`; `FilesystemPermission(operations=["write"], paths=[…], mode="deny"|"allow")` (first match wins, unmatched allowed); `RubricMiddleware(model, max_iterations, tools, system_prompt, on_evaluation)` — flagged beta in this era and warns on construction; the rubric is supplied per invocation under the state key `rubric`; the terminal status is read from the private state key `_rubric_status`; passing `system_prompt` *replaces* the library's default grader prompt (its verdict definitions and untrusted-transcript rule must be restated). Default file tools: `read_file, write_file, edit_file, ls, glob, grep, delete`.
- Framework: `langchain` 1.3.x — `langchain.agents.create_agent`, `langchain.agents.middleware.ModelCallLimitMiddleware(run_limit, exit_behavior="end")`, `langchain.tools.tool`; `langchain_core.messages.HumanMessage`; `langgraph.checkpoint.memory.InMemorySaver`; streaming with `stream_mode="updates"`; message `content` is a list of content blocks on current models and a plain string on older ones; structured output via `response_format=<pydantic model>` returned under `structured_response`; a compiled agent's state via `get_state(config).values`; `config={"configurable": {"thread_id": …}, "run_name": …, "tags": […]}`.
- Provider: model strings with the `openai:` prefix — the course's `openai:gpt-5.4-mini` (reviewer, grader) and `openai:gpt-5.5` (analyst); `langchain-openai` 1.6.0 / `openai` 3.6.0. **Request-parameter compatibility**: the course never sets sampling parameters (`temperature` etc.) on these families; assume a current family may reject them and leave them unset unless the current docs say otherwise.
- Cost table in the course's analysis module (per million tokens: analyst model 5.00 / 30.00, reviewer model 0.75 / 4.50) and the `o200k_base` tokenizer name — stale the day prices change.
- Hosted tracing: env vars `LANGSMITH_TRACING` (must be the string `true`), `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`; legacy aliases `LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`.
- Web: `flask` 3.x — routes, `flash`, `render_template`, `redirect`/`url_for`; `difflib.unified_diff` for the page diff.
- The checkpointer attached to the rubric-loop agent is not required for revision (course note); it matches the library's documented shape and gives hosted tracing a thread id per run.

### CTX-E. Provenance map

Nothing in this spec requires platform access. Lesson numbering follows the transcripts.

| Lesson (transcript numbering) | Title | Contributed |
|---|---|---|
| 1 | Introduction | CTX-A (the four loops; the review agent as the running example; "four sections" of the analysis) |
| 2 | Overview of Loop Engineering | CTX-A (why each loop exists; human oversight at four points; traces as the story); CTX-C T1, T2, T7–T12; rows D1, D2; Not Included 2, 3, 5 |
| 3 | Deep Agent Primer | CTX-A (instruction channels; filesystem backend; progressive disclosure); CTX-C T13, T14, T23; CTX-D harness names; Not Included 6, 7 |
| 4 | Agent Loop | CTX-A (fetch by id; stage-by-stage file); CTX-B1, B2, B5; CTX-C T5, T6; R1–R9; rows L1, L2, L5 |
| 5 | Verification Loop | CTX-A (grader, retry with feedback); CTX-B6, B7; CTX-C T2, T3, T4, T5; R10–R13; rows L3, D2 |
| (no transcript lesson) | Event-driven loop app (code + README only; the deck has a title card and one diagram) | CTX-A (event triggers; source-of-truth separation); CTX-B8; CTX-C T19, T20; R14–R17 |
| 6 | Learning loop | CTX-A (batch, analyst, propose/approve/apply, measure); CTX-B9–B11; CTX-C T9, T15, T16; R18–R21 |
| 7 | Conclusion | nothing beyond the recap |

Code-side evidence mined as part of the notebook dump: the harness module (review agent, trace capture, rubric, grader prompt and its comments), the batch module, the analysis module, the event app (routes, trigger, data store, README), the environment files (`pyproject.toml`, `uv.lock` resolutions, `.env.example`) and the repository README. CTX-B3, B4, B9, B12 and T17, T18, T21 come from code and its comments.

Slides read: the overview deck (13 slides, all narrated in Lesson 2 — video-shown) and the lesson deck (18 slides: title cards deck-only; the primer, agent-loop, verification-loop and learning-loop content slides narrated — video-shown; the two event-driven-loop slides deck-only). Their contributions are marked in CTX-C.

---

*Spec v1 · course: Loop Engineering with LangChain DeepAgents · learner project: [project] (default: the requirements-review agent with four loops) · Living document: when the building agent produces something unexpected, add the missing constraint here (a rule, a criterion, a fixture fact) and re-run.*
