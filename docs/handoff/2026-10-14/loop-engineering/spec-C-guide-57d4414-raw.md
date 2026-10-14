# Spec: Requirements Review Agent with Four Loops — Coding-Agent-Lab Build

> **What you're building:** a web app — a simulated ticket tracker and wiki with a requirements-review agent behind them that checks and improves its own work. You open the tracker in the preview, create a ticket against a vague requirement page, and watch the agent write a five-section analysis, see the grader send it back once and then pass it, and mark the ticket Done yourself; then you run the same agent over five requirement documents, read the analyst's one proposed instruction change, approve it, and watch the re-run pass every criterion on the first attempt. Answering the gate's first question with the recommended baseline builds all of this end to end; the build is complete when the offline suite passes — the lab's ambient platform key unlocks only the live tests and live use of the finished app.
>
> This file is self-contained: the Course Context Pack at the end replaces every external course reference, and nothing here requires platform access.
>
> `(CTX-X)` anchors mark course-derived knowledge. The Decision Ledger below holds every point where the build could diverge, each pinned to one course-derived default, so the spec builds as-is with no intake. `[environment]` marks facts the lab contributes, never the course.
>
> Generated from the Loop Engineering with LangChain DeepAgents notebooks + transcripts + slides on 2026-10-13, guide @ `57d4414`, coding-agent-lab overlay @ `b5be7fb`.

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

   *[environment] In this lab the structured question tool is a fenced `choices` block: explain in prose above it, put the fence last in the message with one option per line, and precede it with a line `**Question N of M — <decision>**` so both of you can see nothing was skipped. A click sends the option line verbatim, and a typed answer naming an option counts identically. Only the latest message's buttons stay live, so never ask the person to go back and change an earlier answer — re-ask it as a new question.*

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

   *[environment] Each row is one `choices` fence, last in its own message, headed `**Question N of M — <decision>**`. Click and typed answers are equivalent. Only the latest message's buttons stay live: if an answer must change, ask the row again as a new question rather than pointing back at an earlier one.*

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

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option.

Row ids: `L` learner-context, `D` design (argued or structural), `RR` realization. Business rules are `R<n>` and are a different namespace. Terms used in the notes (litmus branch, lever, tier, substitution row, heavy bar) are defined in CTX-C's opening paragraph.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L1 | learner | **Scope boundary.** Present the §1 "Not Included" list, item by item with its handling tag, *inside this question*; ask whether to keep it as-is or bring an item back. | — | Keep as-is: every §1 exclusion stands and the full acceptance set is built. | (a) keep the §1 list as-is; (b) bring something back — name it in free text; a `restorable` item is built as described, a `never built` item is built with no parameters or acceptance criteria supplied here, an `owned by row` item is decided on that row instead, an `unavailable` item cannot be restored in this lab. A genuine *additional* exclusion also goes in free text and must name the acceptance criteria it retires. | Restoring an item adds unspecified work; excluding more retires criteria that the completion gate (§7) would otherwise require. | learner |
| D1 | design-argued | **Instruction placement** for the review agent. | The review guidance the learning loop edits lives in a file loaded into the agent's context at the start of every run, editable from outside the agent and never writable by the agent itself (R6, R7, R22). | One always-on instructions file (`memories/AGENTS.md` inside the run workspace) holding Procedure and Review guidance, loaded on every run; no skills. This is the course's own review-agent realization. | (a) one always-on instructions file only (course default for the review agent); (b) the always-on file plus a skills directory whose per-procedure files carry a one-line frontmatter description and are read only when the agent decides they apply (the course built this for its primer agent, Lesson 3). | Lesson 3 argues the split: the always-on file costs context on every call and must stay short; a skill costs one description line until it is read, so a large library stays cheap. Litmus: both sides shown working (primer with skills, review agent without) and they differ in a component → row. Switching to (b) moves per-section review guidance into skill files; the learning loop's insertion target then needs a section heading inside a skill file, not only in the always-on file. | course+learner |
| D2 | design-argued | **Verification loop** around the agent loop. | The agent loop's deliverable is one file; when a grader is present it reads that file, judges every rubric criterion pass/fail with a gap on failure, and a failing verdict is fed back into the same run until it passes or the revision budget is spent (R10–R12). | Grader present: a rubric grader wraps the agent loop and may send the work back; the budget value is a body lever pinned at R11. | (a) grader present, sends work back within a revision budget (course default); (b) plain agent loop — the grader removed, which is the course's own "set the budget to 0 and you have the basic agent loop" (Lesson 5). | Lesson 5: "If you set this to 0, you will have the same basic agent loop you built in the last lesson." Litmus: a limit value that removes a component is a component choice, not a knob; the course built the plain loop first (Lesson 4) and showed it working, then wrapped it — so a row, not a bake-in. Choosing (b) retires AC11–AC15 and, because the learning loop reads grader verdicts, leaves the learning loop with no signal (AC22–AC30 cannot run); Lesson 2 argues the grader is what makes a cheaper model viable on a hard task. | course+learner |
| D3 | design-structural | **Grader realization.** | A grader distinct from the agent judges the finished file against the rubric and returns per-criterion pass/fail with a short gap text on each failure (R10, R11). | Agentic grader: a model, given a read-file tool and the grader instructions, reads the file and returns the verdict (the course's rubric middleware). | (a) agentic grader — a model reads the file and judges (course default); (b) deterministic grader — code checks each criterion (the course names this kind for mechanical criteria such as "links resolve, CI passes", Lesson 2); (c) hybrid — code for the labelled-line criteria, a model for coverage. | Structural litmus: the grader box changes owner (model → code). A deterministic grader cannot judge the coverage criterion semantically; the course's two labelled-line criteria are mechanical and a code grader passes them exactly. In the offline suite the scripted grader (RR1) behaves deterministically either way. | course+learner |
| RR1 | realization | **Model the acceptance suite runs against.** | The offline suite drives the real pipeline end to end — agent loop, grader, event trigger, batch, analyst, apply, compare — with every model role filled by a stand-in whose responses the spec declares (§5), so the suite passes with no key. | Scripted model stand-in (`fixtures/scripted_model.py`, an honestly-labelled fake declared in §5) for all three roles; selected by `REVIEW_MODEL_BACKEND=scripted`. Branch: the model is a keyed dependency, so the lightest invariant-preserving realization is the default — tier 1, a module in the app, no install. | (a) scripted stand-in for the suite, live platform model for use; (b) live platform model for the suite too (course default — the course ran every lesson live; in this lab the key is ambient, so choosing this costs no setup, but the suite then depends on a non-deterministic model and criteria tagged `live` are the only ones that can be asserted). | Lesson 4 warns "LLMs do not always produce the same results"; a scripted stand-in makes the fixture outcomes exact. Switching the suite to live loses determinism on every count-based assertion. | course+learner |
| RR2 | realization | **Event source — what triggers the loop.** Default is the course's example realization (a simulated ticket tracker and wiki); expected to be swapped when the learner's project has a real tracker. | An external event — a ticket created, or a linked requirement page saved while a ticket is open — starts the verification loop without a person invoking the agent, and the result lands back in the system that raised the event (R14–R16). | The simulated ticket tracker + wiki the course shipped as code: tickets with statuses, pages with version history, all in local files served by this app. Branch: the course's demonstrated real integrations are keyed; the course's own shipped simulation is the keyless stand-in, and it is the only carrier of the trigger behaviour that needs no credential, so it is the default. | (a) simulated tracker + wiki served by this app (course default — the course's shipped code); (b) omit the event-driven layer — tickets and pages removed, the loop invoked only through the review and batch endpoints. | Lesson 6 demonstrates the same agent on a real chat workspace and a real issue tracker/wiki pair, which need an app token, an API token and a public tunnel; those options are **unavailable in this lab** (no credential is supplied) and are listed in §1 with the seam the course names: the single trigger function that a real webhook would call. Choosing (b) retires AC16–AC21. | course+learner |

## Environment Resolutions (coding-agent-lab)

This spec is built inside the **coding-agent-lab** environment: the six learner-context dimensions were derived from the course first and then resolved against the lab, not skipped. `[environment]`

| Dimension | Resolution | Where the Invariant lives now |
|---|---|---|
| project | **ANSWERED** — the lab fixes the assignment | spec §1 Objective. Invariant empty. |
| data/inputs | **ANSWERED** — inputs are seeded into the workspace | spec §5 fixture corpus. Derived Invariant (documents are plain text reachable by an identifier through a fetch tool at run time, never handed to the agent directly) lives in R1, exercised by AC1. |
| goal | **ANSWERED** — the lab fixes what "working" means | spec §1 + the acceptance criteria. Invariant empty. |
| model/provider | **CONSTRAINED** — the built app needs an LLM, so platform models only, keys and base URL read from the environment, never asked for | spec §2 (model rows) + R25, exercised by AC31; CTX-D carries the course's own model ids as provenance. Derived Invariant (native tool calling and a structured typed response for the analyst) lives in R25. The course's argued model tiering per role is a body lever at R25 with an Ask-First entry. |
| environment | **ANSWERED** — the container | spec §2 + the Runtime (lab) section. Derived capability invariants: the agent's filesystem is confined to a per-run workspace (R7, R8 → AC8, AC9); records survive process restarts (R18 → AC21). |
| scope-boundary | **KEPT** | Ledger row L1. |
| hosted tracing (course-owned realization row, retired) | **ANSWERED — every alternative unavailable here.** The course's optional hosted trace viewer needs an account and API key the lab does not supply; the only remaining option (the course's own local trace capture) is pinned in §2 and R9. | §2 "tracing" row + R9, exercised by AC10; §1 lists hosted tracing as `unavailable` with its seam. |

## 1. Objective

A served web app in which a requirements-review agent turns a vague requirement document into a five-section analysis (confirmed facts, ambiguities, clarification questions, assumptions, summary), a grader sends the analysis back until it meets a three-criterion rubric, events in a simulated ticket tracker and wiki trigger that loop and receive its report, and a learning loop reads a batch of graded runs, proposes one instruction change for a human to approve, applies it, and proves by re-running that first-attempt pass rates rose without regression. (pattern: CTX-A)

**Deliverable shape** `[environment]`: one server on port 4000 serving both a page and its API — the preview pane is the learner's only view. The page has three surfaces: the tracker (board, ticket, run detail), the wiki (page list, page at a version, compare), and the learning view (batch, proposal, apply, compare). The course's own artifacts (notebooks and a separate local web app) are never the deliverable.

**Adapting this beyond the lab** `[environment]`: the project and goal now live in this section and in §5's acceptance criteria; the data lives in §5's fixture corpus (replace the seeded documents with your own, keeping R1); the model/provider constraint lives in §2's model rows and R25 (outside the lab, that becomes a Ledger row with the course's provider as its default); the container facts live in §2 and the Runtime (lab) section; hosted tracing can be restored at the seam named below.

### Not Included

Each item carries its handling tag for the L1 gate question.

1. **Real chat-workspace bot** (the course's Lesson 6 demo of the agent answering in a chat channel) — `unavailable`: needs an app-level token and a bot token the lab does not supply. Seam: the single trigger function that receives an event and runs the loop (R14); a real integration calls it from a webhook instead of a form submit.
2. **Real issue-tracker and wiki integration** (the course's Lesson 6 demo over an Atlassian-style site, with automation rules and a public tunnel) — `unavailable`: needs an API token, a site URL and a tunnel. Same seam as item 1.
3. **Hosted trace viewer** (the course's optional trace-sharing service) — `unavailable`: needs an account and API key. Seam: tracing is driven by environment variables in the course; the local trace capture (R9) is complete without it.
4. **Scheduled triggers** (a timer that runs the agent on a schedule; Lesson 2 names it beside event triggers) — `never built`: the course named it and never built it; this spec supplies no parameters and no acceptance criteria for it.
5. **Memory consolidation / per-user preferences as a learning-loop target** (Lesson 2) — `never built`.
6. **Subagents, planning, summarization, context offloading, prompt caching, a code sandbox** (deep-agent pillars named in Lesson 3) — `never built`.
7. **A human acting as the grader, or human approval before individual tool calls** (Lesson 2's oversight points 1 and 2) — `never built`; the two the course did build — a human marks the ticket Done (R16) and a human approves the harness change (R22) — are rules.
8. **Applying analyst proposals that target tools, the grader or configuration** — `never built`: the course makes such proposals expressible and refuses to apply them automatically (R22); applying them is never built, and this spec supplies no parameters and no acceptance criteria for doing so.
9. **Skills directory for the review agent** — `owned by row` D1.
10. **Live-model acceptance assertions beyond the `live` tagged criteria** — `owned by row` RR1.
11. **Cost tracking against real billing** — `never built`: the course prints an estimate from a fixed price table (CTX-D); nothing reads a bill.

## 2. Tech Stack & Versions

Secrets are read from environment variables only — never hardcoded, never written to any file in the workspace, never asked for.

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python ≥ 3.12 | Course requirement (its project file and README; two of its pinned libraries do not build below 3.12). `[environment]` The container's Python minor version is not stated: the build agent runs `python3 --version` first, records it in `resolved-decisions.md`, and stops with a report if any course-pinned package below refuses the interpreter. |
| Virtual environment | `python3 -m venv --system-site-packages .venv` | `[environment]` Reuses the preinstalled stack for unpinned packages. Where a course pin below differs from a preinstalled copy, **the course pin wins inside the venv**. |
| Agent harness | `deepagents==0.7.11` | **Course pin situation, honestly:** the course's project file sets floors (`>=`) and its lock file resolves exact versions; this spec pins the lock-file versions and records them as provenance. The harness is the course's own and is not a Ledger row. Era-specific names are search keywords in CTX-D. |
| Agent framework | `langchain==1.3.18`, `langchain-core==1.6.1`, `langgraph==1.2.11` | Course lock-file pins. |
| Provider client | `langchain-openai==1.6.0`, `openai==3.6.0` | Course lock-file pins. `[environment]` `openai` is preinstalled; the course pin wins inside the venv. |
| Structured output | `pydantic==2.13.5` | Course lock-file pin (the analyst's typed proposal). |
| Config loading | `python-dotenv==1.2.3` | Course lock-file pin; preinstalled copy yields to it. |
| Token estimate | `tiktoken==0.14.0` | Course lock-file pin; used only for the batch cost estimate (R23), with the course's fallback of length ÷ 4 when unavailable. |
| Web server | `flask` (modern 3.x; the course left it unpinned — a floor only, no lock entry) | The course's own web framework for its simulated tools. `[environment]` `fastapi`/`uvicorn` are preinstalled and unused; this is an install. Bound per R26. |
| Install cost | one `pip install` of the rows above | `[environment]` Everything beyond `openai` and `python-dotenv` is an install; batch it in one command at the start of the build and announce its wall-clock cost before running it. |
| Persistent record store | JSON files under `data/` (`pages.json`, `tickets.json`, `runs.json`, plus one directory per batch label under `data/batches/`) via the standard library | The course's own choice. Tier 1 (ships with the language's standard distribution); it meets R18 at the declared scale, so no higher tier is taken. `[environment]` `sqlite3` is available but not needed; scaling realizations are not a Ledger row because the course never argued the store and it is not heavy. |
| Tracing | Local trace capture only (R9) | The course also offered an optional hosted viewer; `unavailable` here (§1 item 3, Environment Resolutions). The variables that would enable it are not read. |
| Model backend switch | `REVIEW_MODEL_BACKEND` = `scripted` or `live`; `scripted` when unset | RR1. |
| Model roles (live) | `REVIEW_AGENT_MODEL`, `REVIEW_GRADER_MODEL`, `REVIEW_ANALYST_MODEL` | `[environment]` One variable per role; the build agent sets them when it writes `resolved-decisions.md` (one "model roles" line carrying its "(Recommended)" platform model per role; the learner's confirmation of the checklist confirms them). Values are platform model ids; the course's own ids are provenance only (CTX-D) and are never asserted to be served here. |
| Provider key + base URL | `OPENAI_API_KEY`, `OPENAI_BASE_URL` (read); `ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL` (present, never read) | `[environment]` The app reads exactly the first pair (the course's provider); the second pair is named here as present and unread (R25). |
| Fixture corpus | `fixtures/` as declared in §5 | Seeded into the record store on first start (R18). |

## 3. Input/Output Contracts

All URLs are relative to the served page (`api/...`, never `/api/...`) — R26 `[environment]`. Every endpoint returns JSON matching the schemas below; the page renders the same objects.

### 3.1 API surface

| Method + path | Body / query | Returns |
|---|---|---|
| `POST api/review` | `{ticket_key, max_turns?, simulated_failures?, rubric_iterations?, rubric?, instructions_version?}` | `RunRecord` — runs the loop once against a ticket (`rubric_iterations` 0 = plain agent loop, R11) |
| `GET api/runs/{run_id}` | — | `RunRecord` |
| `GET api/tickets` · `POST api/tickets` | POST: `{title, description, linked_page_id, assignee}` | `Ticket` / `Ticket` (creation triggers a run, R14) |
| `GET api/tickets/{key}` | — | `{ticket, runs: RunRecord[], changed: ChangeSummary|null}` |
| `POST api/tickets/{key}/rerun` · `POST api/tickets/{key}/close` | — | `Ticket` |
| `GET api/pages` · `POST api/pages` | POST: `{title, body, author}` | `Page[]` / `Page` |
| `GET api/pages/{id}?v=` · `POST api/pages/{id}/versions` | POST: `{body, author}` (requirement pages only) | `Page` / `{page, retriggered: string[]}` |
| `GET api/pages/{id}/compare?a=&b=` | — | `{a, b, diff: string[], run_a: RunRecord|null, run_b: RunRecord|null}` |
| `POST api/batches` | `{label, instructions_version: "v1"|"v2"|string, simulated_failures?}` | `BatchSummary` |
| `GET api/batches/{label}` | — | `{summary: BatchSummary, runs: RunRecord[]}` |
| `POST api/batches/{label}/propose` | — | `{change: HarnessChange, proposal_markdown: string}` |
| `POST api/proposals/{label}/apply` | `{approved: true}` | `{instructions_version: string, diff: string[]}` or HTTP 409 with `{error}` when the target is not `prompt` (R22) |
| `GET api/compare?before=&after=` | — | `Comparison` |
| `GET api/health` | — | `{status: "ok"}` |

### 3.2 Schemas (JSON Schema, draft 2020-12)

```json
{
  "$defs": {
    "Sections": { "type": "array", "const": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"] },

    "AnalysisReport": {
      "type": "object", "required": ["markdown", "counts", "summary_words", "complete"],
      "properties": {
        "markdown": { "type": "string", "description": "the file /analysis.md verbatim" },
        "counts": { "type": "object",
          "required": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions"],
          "additionalProperties": false,
          "properties": { "Confirmed Facts": {"type":"integer","minimum":0}, "Ambiguities": {"type":"integer","minimum":0},
                          "Clarification Questions": {"type":"integer","minimum":0}, "Assumptions": {"type":"integer","minimum":0} } },
        "summary_words": { "type": "integer", "minimum": 0 },
        "complete": { "type": "boolean", "description": "every list section has ≥1 bullet and summary_words > 0" }
      },
      "if": { "properties": { "complete": { "const": true } } },
      "then": { "properties": { "summary_words": { "minimum": 1 },
                "counts": { "properties": { "Confirmed Facts": {"minimum":1}, "Ambiguities": {"minimum":1},
                                            "Clarification Questions": {"minimum":1}, "Assumptions": {"minimum":1} } } } }
    },

    "TraceStep": {
      "type": "object", "required": ["step", "actor", "action", "detail"],
      "properties": { "step": {"type":"integer","minimum":1}, "actor": {"enum": ["Model reasoning", "Tool"]},
                      "action": {"type":"string","minLength":1}, "detail": {"type":"string","maxLength":221} }
    },

    "Criterion": {
      "type": "object", "required": ["name", "passed"],
      "properties": { "name": {"type":"string"}, "passed": {"type":"boolean"}, "gap": {"type":"string"} },
      "if": { "properties": { "passed": { "const": false } } },
      "then": { "required": ["gap"], "properties": { "gap": { "minLength": 1 } } }
    },

    "GradingPass": {
      "type": "object", "required": ["iteration", "result", "explanation", "criteria", "analysis_markdown"],
      "properties": {
        "iteration": {"type":"integer","minimum":1},
        "result": { "enum": ["satisfied", "needs_revision", "failed", "grader_error"] },
        "explanation": {"type":"string"},
        "criteria": { "type":"array", "items": {"$ref":"#/$defs/Criterion"} },
        "analysis_markdown": {"type":"string","description":"the file as this pass saw it"},
        "grader_actions": { "type":"array", "items": {"type":"string"}, "description":"the grader's tool calls in order, e.g. read_file:/analysis.md" }
      },
      "allOf": [
        { "if": { "properties": { "result": { "const": "satisfied" } } },
          "then": { "properties": { "criteria": { "minItems": 1, "items": { "properties": { "passed": { "const": true } } } } } } },
        { "if": { "properties": { "result": { "const": "needs_revision" } } },
          "then": { "properties": { "criteria": { "contains": { "properties": { "passed": { "const": false } } } } } } },
        { "if": { "properties": { "result": { "enum": ["failed", "grader_error"] } } },
          "then": { "properties": { "criteria": { "maxItems": 0 } } } }
      ]
    },

    "RunRecord": {
      "type": "object",
      "required": ["run_id", "ticket_key", "requirement_doc", "instructions", "instructions_version", "rubric", "trace", "grading",
                   "analysis", "stage_order", "status", "turns", "max_turns", "model_backend", "started_at"],
      "properties": {
        "run_id": { "type":"string", "pattern":"^[0-9a-f]{8}$", "description":"8 lowercase hex chars (course id format)" },
        "ticket_key": { "type":"string", "pattern":"^[A-Z]+-[0-9]+$" },
        "requirement_doc": {"type":"string","minLength":1},
        "instructions": {"type":"string","minLength":1,"description":"the instructions file the run was given, verbatim"},
        "instructions_version": {"type":"string"},
        "rubric": {"type":"string","description":"empty when rubric_iterations was 0"},
        "trace": { "type":"array", "items": {"$ref":"#/$defs/TraceStep"} },
        "grading": { "type":"array", "items": {"$ref":"#/$defs/GradingPass"} },
        "analysis": {"$ref":"#/$defs/AnalysisReport"},
        "stage_order": { "type":"array", "items": {"enum": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"]} },
        "status": { "enum": ["finished", "turn_limit_reached", "satisfied", "max_iterations_reached", "failed", "grader_error"] },
        "turns": {"type":"integer","minimum":0}, "max_turns": {"type":"integer","minimum":1},
        "model_backend": { "enum": ["scripted", "live"] },
        "started_at": {"type":"string"},
        "requirement_version": {"type":"integer","minimum":1}, "report_page_id": {"type":"string"}, "report_version": {"type":"integer","minimum":1}
      },
      "allOf": [
        { "if": { "properties": { "rubric": { "const": "" } } },
          "then": { "properties": { "grading": { "maxItems": 0 }, "status": { "enum": ["finished", "turn_limit_reached"] } } },
          "else": { "properties": { "status": { "enum": ["satisfied", "max_iterations_reached", "failed", "grader_error", "turn_limit_reached"] } } } },
        { "if": { "properties": { "status": { "const": "satisfied" } } },
          "then": { "properties": { "grading": { "minItems": 1 } } } }
      ]
    },

    "Ticket": {
      "type": "object", "required": ["key", "title", "description", "linked_page_id", "assignee", "status", "comments", "created_at", "last_analyzed_version", "last_run_id"],
      "properties": {
        "key": { "type":"string", "pattern":"^REQ-[0-9]+$" },
        "status": { "enum": ["Open", "Analysis Ready", "Done"] },
        "assignee": {"type":"string","minLength":1},
        "comments": { "type":"array", "items": { "type":"object", "required":["author","text","timestamp"] } },
        "last_analyzed_version": { "type": ["integer","null"] }, "last_run_id": { "type": ["string","null"] }
      }
    },

    "PageVersion": { "type":"object", "required":["n","author","timestamp","body"], "properties": { "n": {"type":"integer","minimum":1} } },
    "Page": {
      "type": "object", "required": ["id", "kind", "title", "linked_ticket", "versions"],
      "properties": {
        "id": {"type":"string","pattern":"^page-[a-z0-9-]+$"},
        "kind": { "enum": ["requirement", "analysis_report"] },
        "linked_ticket": { "type": ["string","null"] },
        "versions": { "type":"array", "items": {"$ref":"#/$defs/PageVersion"}, "description": "append-only; n strictly increasing from 1" }
      },
      "if": { "properties": { "kind": { "const": "analysis_report" } } },
      "then": { "properties": { "linked_ticket": { "type":"string" }, "id": { "pattern": "^page-analysis-req-[0-9]+$" } } },
      "else": { "properties": { "linked_ticket": { "const": null }, "versions": { "minItems": 1 } } }
    },

    "ChangeSummary": {
      "type":"object", "required":["previous_run_id","latest_run_id","requirement_version","status","counts"],
      "properties": {
        "requirement_version": { "type":"array", "prefixItems":[{"type":"integer"},{"type":"integer"}], "minItems":2, "maxItems":2 },
        "status": { "type":"array", "minItems":2, "maxItems":2 },
        "counts": { "type":"object", "required":["Confirmed Facts","Ambiguities","Clarification Questions","Assumptions"],
                    "additionalProperties": { "type":"array", "minItems":2, "maxItems":2, "items": {"type":"integer"} } }
      }
    },

    "HarnessChange": {
      "type": "object", "required": ["target", "issue", "recurrence", "evidence", "section", "change", "rejected"],
      "properties": {
        "target": { "enum": ["prompt", "tool", "grader", "configuration"] },
        "issue": {"type":"string","minLength":1}, "recurrence": {"type":"string","minLength":1},
        "evidence": { "type":"array", "items": {"type":"string","minLength":1} },
        "section": {"type":"string"}, "change": {"type":"string"},
        "rejected": { "type":"array", "items": {"type":"string"} }
      },
      "if": { "properties": { "target": { "const": "prompt" } } },
      "then": { "properties": { "section": { "pattern": "^#{1,6} .+" }, "change": { "minLength": 1 }, "evidence": { "minItems": 2 } } }
    },

    "CriterionRate": { "type":"object", "required":["passed","total","pass_rate"],
      "properties": { "passed": {"type":"integer","minimum":0}, "total": {"type":"integer","minimum":0}, "pass_rate": { "type": ["number","null"] } } },
    "BatchSummary": {
      "type": "object", "required": ["label", "model_backend", "instructions_version", "runs", "graded", "grader_errors", "first_attempt", "revisions_needed", "documents"],
      "properties": {
        "runs": {"type":"integer","minimum":1}, "graded": {"type":"integer","minimum":0}, "grader_errors": {"type":"integer","minimum":0},
        "first_attempt": { "type":"object", "required":["completeness","clarity","depth"],
          "properties": { "completeness": {"$ref":"#/$defs/CriterionRate"}, "clarity": {"$ref":"#/$defs/CriterionRate"}, "depth": {"$ref":"#/$defs/CriterionRate"} } },
        "revisions_needed": {"type":"integer","minimum":0},
        "documents": { "type":"array", "items": {"type":"string"} }
      },
      "description": "graded + grader_errors == runs; every CriterionRate.total == graded; pass_rate is null when graded == 0; revisions_needed <= graded"
    },

    "Comparison": {
      "type": "object", "required": ["verdict", "criteria", "runs", "revisions_needed", "attempts", "input_tokens", "output_tokens", "cost_usd", "improved", "regressed"],
      "properties": {
        "verdict": { "enum": ["regression", "success", "partial", "no effect"] },
        "criteria": { "type":"object", "additionalProperties": { "type":"array", "minItems":2, "maxItems":2, "items": {"type":"integer"} } },
        "revisions_needed": { "type":"array", "minItems":2, "maxItems":2 }, "attempts": { "type":"array", "minItems":2, "maxItems":2 },
        "improved": { "type":"array", "items": {"type":"string"} }, "regressed": { "type":"array", "items": {"type":"string"} }
      },
      "allOf": [
        { "if": { "properties": { "verdict": { "const": "regression" } } }, "then": { "properties": { "regressed": { "minItems": 1 } } } },
        { "if": { "properties": { "verdict": { "enum": ["success", "partial", "no effect"] } } }, "then": { "properties": { "regressed": { "maxItems": 0 } } } },
        { "if": { "properties": { "verdict": { "const": "partial" } } }, "then": { "properties": { "improved": { "minItems": 1 } } } },
        { "if": { "properties": { "verdict": { "const": "no effect" } } }, "then": { "properties": { "improved": { "maxItems": 0 } } } }
      ]
    }
  }
}
```

### 3.3 The analysis file (course-declared constants, binding)

`/analysis.md` inside the run workspace, five `##` headings in the `Sections` order above, exactly once each. Confirmed Facts, Ambiguities, Clarification Questions and Assumptions are bullet lists (`- `); Summary is prose of two or three sentences. An Ambiguities bullet is `- **"<the exact clause>"**` followed by an indented `Reason:` line; under the improved instructions it also carries indented `Resolved by:` and `Edge case:` lines (R4, R22). Counts are bullets per list section; Summary is counted in words (R4).

### 3.4 The rubric (course-declared, binding)

Three criteria in this order, each pass/fail: **completeness** — every clause of the requirement is addressed somewhere in the analysis; **clarity** — every Ambiguities bullet has an indented `Resolved by:` line naming the fact or decision that would settle it; **depth** — every Ambiguities bullet has an indented `Edge case:` line naming a concrete production failure the ambiguity could cause. Criteria are identified by **position** (rubric order), never by the grader's echoed name (R20).

## 4. Business Rules

Labels: *course-demonstrated* (CTX anchor), *project hardening* (added here, not shown by the course), `[environment]` (lab-imposed). Values cite their exact source config; a **lever** is a post-build value the gate never asks about.

**Agent loop (CTX-A stage 1–3)**

- **R1 — Fetch by identifier.** The agent is built without any document; a run's opening message names only a ticket key, and the agent obtains the text by calling a `fetch_requirement` tool that resolves the key against the ticket store at call time. The requirement is never placed in the agent's context by the harness. *Course-demonstrated* (CTX-A; CTX-C name-map: the course's instructions file names the tool `fetch_requirement` in its tracked copy and `fetch_requirement_from_jira` in two batch snapshots — near-equivalent name, lever-value branch 1, the Lesson 4 narration says `fetch_requirement`). → AC1
- **R2 — Retry transient fetch failures.** A fetch result that is an error message (text beginning `Error`) is retried with the exact same tool and arguments until it succeeds; the trace records every attempt. The fake fetch tool fails a configurable number of times before succeeding — **lever**, `simulated_failures`: 2 for the agent-loop demonstration (Lesson 4 narration: "simulating two times of failure"; the notebook's tool table and its saved trace agree; the helper module's own default is 0, "a clean fetch" — lever-value branch 1, narration), 0 for ticket-triggered and batch runs (the course's automation and batch configs set 0: "only adds turns and noise"). Prevents CTX-B1. *Course-demonstrated.* → AC2
- **R3 — One file, built stage by stage, in order.** The deliverable is `/analysis.md` with the §3.3 skeleton. The agent is instructed to work one stage per tool call: `write_file` once (skeleton + Confirmed Facts), then one `edit_file` per remaining section, Summary last, then one short completion sentence with no tool call. The harness requests this order; it does not enforce it, so every run records `stage_order` — the sections each successful write actually filled — and a run is `complete` only when every list section has ≥1 bullet and the Summary has ≥1 word. Filling two sections in one edit is not a violation; filling one out of order, or leaving one empty, is reported. Prevents CTX-B2. *Course-demonstrated* (helper docstrings "Stage ordering is requested, not guaranteed"). → AC3, AC4
- **R4 — Report shape.** Ambiguities bullets quote the exact clause and give a Reason line; Confirmed Facts record only what the document states; Clarification Questions ask what a reviewer needs answered before work starts; Assumptions state what a developer would assume if nobody answered; Summary is two or three sentences. Counts per list section and Summary word count are computed from the file. *Course-demonstrated* (the course's instructions file, Lesson 4). → AC5
- **R5 — Turn cap is the backstop, not the stopping rule.** A run normally ends when the agent replies without a tool call after the Summary; a model-call limit ends it otherwise. **Lever**: 12 model turns for a plain agent-loop run (Lesson 4 notebook `MAX_TURNS = 12`; helper comment: six stages plus headroom for retries and the closing message), 40 when a grader is present (Lesson 5 notebook, the automation module and the batch runner all set 40: "several verification passes cost more turns than one review"). When the cap ends the run, the last trace action reads `Stops: turn limit of <N> reached` and `status` is `turn_limit_reached`, never `finished`. Prevents CTX-B3. *Course-demonstrated.* → AC6
- **R6 — Instructions are a file, loaded every run, required.** The agent's system prompt only points at `/memories/AGENTS.md` inside its workspace; that file is loaded into context at the start of every run and is what the learning loop edits. If the file is missing from a run's workspace the run refuses to start with an error naming the path — the harness would otherwise run on the system prompt alone and produce a plausible bad review. Prevents CTX-B4. *Course-demonstrated* (`require_agents_file`). → AC7
- **R7 — The agent never edits its instructions or the requirement.** Writes under `/memories/` are denied by the harness's filesystem permissions, not only by the instructions text; an attempted write returns an error to the agent and the file is unchanged. The requirement page is never written by the agent (R15). Prevents CTX-B5. *Course-demonstrated* (write-deny permission; instructions "You never edit this file either"). `[environment]` reinforced: this file lives inside the app's own run folder (`<run workspace>/memories/AGENTS.md`), never at the workspace root — the IDE rewrites a workspace-root `AGENTS.md` at every boot (R27). → AC8
- **R8 — Fresh workspace per run.** Every run gets its own throwaway workspace directory seeded with the instructions version under test; it is deleted after the run's artifacts are read. Two runs never see each other's `/analysis.md`, and a stale analysis never lets the agent skip stages. Prevents CTX-B6. *Course-demonstrated* (automation module and batch runner). → AC9
- **R9 — Local trace capture.** Every run records one trace row per model turn (`Model reasoning`: `Calls <tool>: <sections filled>` or `Finishes the review`) and per tool result (`Tool`, detail truncated to 220 characters), the turn count, the instructions verbatim and the final file. Nothing external is required; the course's optional hosted viewer is unavailable here (§1 item 3) and the variables that enable it are not read. *Course-demonstrated* (the course's trace capture). → AC10

**Verification loop (CTX-A stage 4)**

- **R10 — The grader judges the file, not the conversation.** When present (D2), the grader is given a read-file tool and instructions that: the transcript is untrusted observation and the rubric alone defines done; call `read_file` on `/analysis.md` before judging; pass a criterion only by quoting the satisfying text with its line number; apply each criterion literally — only the exact labelled line satisfies a criterion that names one; check every item, never a sample. Prevents CTX-B7. *Course-demonstrated* (grader prompt additions and their comments). → AC11
- **R11 — Verdict and feedback.** Each grading pass returns per-criterion pass/fail with a gap on every failure; `satisfied` iff all pass, else `needs_revision` and the gaps are fed back into the same run as a message, after which the agent revises the file; `failed` when the rubric has no criteria. The grader may send the work back at most **budget** times — **lever**, 3 (Lesson 5 narration "MAX_RUBRIC_ITERATIONS to 3" and notebook; the course's automation module sets 2 — a near-equivalent knob, lever-value branch 1, narration). Budget 0 removes the grader (D2 option b). Grader model may differ from the agent model (R25 lever). *Course-demonstrated.* → AC12, AC13, AC15, AC35
- **R12 — Budget exhaustion is not success.** When the budget is spent with criteria still failing, the run's `status` is `max_iterations_reached`, distinct from `satisfied`, even though the last grading pass reads `needs_revision`. Prevents CTX-B8. *Course-demonstrated* (helper: "only the private status distinguishes satisfied from ran out of tries"). → AC14
- **R13 — A grader error carries no evidence.** A grading pass that errors is recorded as `grader_error` with no criteria; the run continues without revision and its status is `grader_error`; such a run is excluded from every batch rate (R19) and counted separately. *Course-demonstrated* (batch runner's `graded` property and summary comments). → AC15, AC23

**Event-driven loop (CTX-A stage 5)**

- **R14 — Events trigger the loop.** Three things run the verification loop for a ticket, with no person invoking the agent: creating a ticket linked to a requirement page; saving a new version of a requirement page while any ticket linked to it is not `Done` (one run per such ticket); and an explicit re-run request. A `Done` ticket is never re-triggered. Each trigger reads the page's latest version at trigger time. *Course-demonstrated* (Lesson 6 app). → AC16, AC17, AC19
- **R15 — The report is a separate, agent-owned page.** Each run's result is written as a new version of one page per ticket, `kind: analysis_report`, titled `Analysis Report — <ticket key>`, authored by `Requirements Analysis Agent (bot)`, whose body opens with a banner naming the ticket, the requirement version analyzed, the verification status and the number of grading passes, followed by the analysis file verbatim. The requirement page is the source of truth and is never written by a run. Page versions are append-only. *Course-demonstrated.* → AC18
- **R16 — The ticket records the run; a human closes it.** After a run the ticket status becomes `Analysis Ready`, `last_analyzed_version` and `last_run_id` are set, and a bot comment names the status, the requirement version and the report page. Only a person's explicit close request moves a ticket to `Done`; no run ever does. Ticket keys are `REQ-<n>`, `n` starting at 100 and incrementing. *Course-demonstrated* (README: "the agent never closes its own work"). → AC16, AC17, AC19
- **R17 — What changed since the previous run.** When a ticket has two or more runs, the ticket view shows, side by side for the previous and latest run: requirement version analyzed, verification status, and bullet counts for the four list sections; and the report page's version compare returns a unified text diff plus the two runs' status and counts. Both are shown together because counts can look alike while content changed completely. *Course-demonstrated* (README walkthrough step 8). → AC20
- **R18 — Records persist.** Pages, tickets, runs and batches are written to the §2 record store on every change; a restarted server serves the same records; first start on an empty store seeds the §5 scenario (one requirement page, one open ticket, no runs) and never re-seeds over existing data. *Project hardening* for the restart assertion; the seed-once behaviour is *course-demonstrated*. `[environment]` This also discharges the environment dimension's "records survive process restarts" invariant. → AC21

**Learning loop (CTX-A stage 6–8)**

- **R19 — A batch is one instructions version over every document.** `POST api/batches` runs the verification loop (budget per R11, 40-turn cap per R5, fetch failures 0) over every document in `fixtures/requirements/` in filename order, each in its own workspace seeded with the named instructions version, records every run (full messages with tool-call arguments, every grading pass with the file as it saw it, final file, instructions snapshot, status) under `data/batches/<label>/` as `run_NN_<doc>.json` plus the instructions snapshot and `summary.json`. The summary's first-attempt rate per criterion uses **graded runs as the denominator**; grader errors are counted in `grader_errors`; `revisions_needed` counts graded runs whose first attempt failed any criterion. *Course-demonstrated.* → AC22, AC23, AC36
- **R20 — Criteria by position.** First-attempt failures are recorded as criterion indexes in rubric order, and summaries and gap groupings key on `criterion_labels` parsed from the rubric text, never on the grader's echoed wording. Prevents CTX-B9. *Course-demonstrated.* → AC24
- **R21 — The analyst reads, reasons, and proposes exactly one change.** The analyst is an agent rooted at the batch directory, allowed to write only `/proposal.md` and nothing else; it reads `summary.json` first, then individual runs for quoted evidence, then the batch's instructions snapshot so the addition fits; it returns one structured `HarnessChange`. A criterion failing in **more than half** of graded runs is a property of the agent; a problem seen in fewer runs is not acted on and goes to `rejected`. Evidence is quoted, not paraphrased; the change is literal insertable text. `proposal.md` carries: summary signal, evidence across runs, current instruction gap, proposed insertion, rejected observations. Prevents CTX-B10. *Course-demonstrated* (analyst prompt and module docstring). → AC25, AC26, AC36
- **R22 — Proposals are applied by code, after human approval, prompt-target only.** Nothing is applied until a person approves the proposal. Applying inserts the literal change text at the end of the section whose heading `section` names (the section ends at the next heading of equal or shallower depth) and stores the result as a new instructions version; nothing is removed or reworded. A `HarnessChange` whose target is not `prompt` is refused with an error telling the person to read the proposal and decide. The analyst never writes the traces it reads, and never writes instructions. Prevents CTX-B11. *Course-demonstrated* (module docstring "The agent proposes and does not apply"; Lesson 2 oversight point 4). → AC27, AC28
- **R23 — Prove it with a re-run and a verdict.** After applying, a second batch under the new version is compared with the first: per criterion the first-attempt pass counts (before, after); `regression` if any criterion's count fell; else `success` if the after-batch needed no revisions; else `partial` if any criterion rose; else `no effect`. The comparison also reports revisions needed, total grading attempts, estimated input/output tokens (running-context estimate; token counter from §2 with length ÷ 4 fallback) and estimated cost from a fixed price table (CTX-D; the table is perishable, the computation is not). A `regression` verdict means the change must not be kept. *Course-demonstrated* (Lesson 2: "run your eval suite and make sure there are no regressions"; Lesson 7 `compare`). → AC29, AC30
- **R24 — Batch state is reproducible.** A batch label is a directory; re-running a label overwrites it; the two course-shaped labels `v1` (baseline instructions) and `v2` (after the approved change) are what the learning view compares by default. *Project hardening* (the course wrote labels but did not define overwrite). → AC22

**Environment** `[environment]`

- **R25 — Platform models only; keys from the environment.** In `live` mode the app reads `OPENAI_API_KEY` and `OPENAI_BASE_URL` and nothing else for credentials; `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL` are present in the container and are not read. Model ids come from the three role variables in §2; the app never asks a person for a key, never hardcodes one, never probes a listing endpoint, and never assumes a course model id is served. If a required variable is absent in `live` mode the request fails with an error naming the variable. The chosen models must support native tool calling, and the analyst's must return a typed structured response. **Lever** (model tiering per role, Ask First): the course argues a cheaper model for the review agent and grader and a stronger one for the analyst, "the one job the cheaper model does unreliably" (Lesson 2, Lesson 7, README), and names a separate grader model as "a common production choice" (Lesson 5) while using the same model for both. → AC31, AC35, AC36
- **R26 — One server, relative URLs, HTTP only.** One process serves page and API on port 4000 bound to `0.0.0.0`. Every URL the page emits (links, fetches, form actions, assets) is relative — `api/tickets`, never `/api/tickets` — because the preview is reverse-proxied under a path prefix and a root-absolute path resolves against the IDE. No WebSocket; long operations respond over plain HTTP (streaming allowed). See Runtime (lab) failure mode E1. → AC32, AC33
- **R27 — Harness instructions never at the workspace root.** The only `AGENTS.md` files this build authors are the instructions versions under `fixtures/instructions/` and the per-run copies at `<run workspace>/memories/AGENTS.md`; the build never creates or edits a workspace-root `AGENTS.md`. *Course-demonstrated, reinforced `[environment]`*: the course keeps the file inside the agent's workspace because the memory loader reads from the agent's own filesystem root; the lab forbids the root file because the IDE rewrites it. One rule, both citations. → AC34

## 5. Acceptance Criteria

### 5.1 Fixture corpus (declared first; every fact is authored here, none copied from the course)

All fixtures live under `fixtures/` and are read-only for the build agent (§6 Never). Module filenames are importable identifiers.

**F1 — `fixtures/requirements/` — five requirement documents for the batch.** Each is a title line `REQUIREMENT: <name>` followed by blank-line-separated clauses; the clauses are every non-empty line after the title. Vague words are in *italics* here for the reader only; the files contain plain text.

| File | Clauses (verbatim) | Vague clauses |
|---|---|---|
| `01_session_timeout.md` | REQUIREMENT: Session Timeout · The system shall end idle sessions after a *reasonable* period. · Users must be warned *appropriately* before a session ends. · Active downloads should not be interrupted. · The system shall record every forced logout. | 2 |
| `02_export_scheduling.md` | REQUIREMENT: Report Export Scheduling · Users shall be able to schedule report exports. · Exports must run at a *sensible* time for the user's region. · Large exports should be handled *efficiently*. · Users must be notified when an export is ready. | 2 |
| `03_api_rate_limits.md` | REQUIREMENT: API Rate Limits · The API shall limit requests per client. · Limits must be *generous* enough for normal use. · Clients should be told *clearly* when a limit is hit. · The system shall log rate-limited requests. | 2 |
| `04_search_relevance.md` | REQUIREMENT: Search Relevance · Search shall return the most *relevant* results first. · Recent documents should be favoured *appropriately*. · The system must respond *quickly* even for broad queries. · Users shall be able to filter results by owner. | 3 |
| `05_backup_retention.md` | REQUIREMENT: Backup Retention · Backups shall be taken *regularly*. · Old backups must be removed after a *reasonable* time. · Restores should complete *promptly*. · The system shall verify backups *periodically*. | 4 |

**F2 — `fixtures/seed/` — the tracker/wiki starting scenario** (seeded on first start, R18): one requirement page `id: page-shared-calendar-invitations`, title `Shared Calendar Invitations — Requirements`, author `Ana (Product Manager)`, version 1 body of three clauses (no title line): `Users shall be able to invite teammates to a calendar event.` · `Invitations should be delivered promptly.` · `The system should support common calendar formats.` (vague clauses: 2). One ticket `REQ-100`, title `Review requirements: Shared Calendar Invitations`, description `Please review the linked requirement for ambiguity before implementation starts.`, `linked_page_id: page-shared-calendar-invitations`, assignee `Theo (Eng Lead)`, status `Open`, no comments, no runs. The fixed cast for assignee/author pickers: `Ana (Product Manager)`, `Theo (Eng Lead)`, `Mei (QA Lead)`, `Rafael (Backend Engineer)`, `Ines (Frontend Engineer)`. The bot author is `Requirements Analysis Agent (bot)`.

**F3 — `fixtures/instructions/v1/AGENTS.md` and `fixtures/instructions/v2/AGENTS.md` — the two instruction versions.** Written by the build agent to these facts (course structure, this spec's wording): a `# Requirements Review Agent` title; a `## Procedure` section asking for one tool call per stage in R3's order with the §3.3 skeleton, the retry rule of R2, a ban on modifying the requirement or this file, and a one-sentence completion reply; a `## Review guidance` section with `### Confirmed facts`, `### Ambiguities`, `### Clarification questions`, `### Assumptions` giving R4's guidance. **v1** describes an Ambiguities bullet as the quoted clause plus an indented `Reason:` line and contains the string `Resolved by:` nowhere. **v2** is byte-for-byte v1 with this insertion at the end of `### Ambiguities` (the exact text the scripted analyst proposes, I1 below). The seven-line insertion **I1**:

```
For every ambiguity bullet, add two more indented labelled lines after the Reason line:

  Resolved by: the specific fact or decision that would settle the ambiguity
  Edge case: a concrete production failure that could happen if it stays unresolved
```

**F4 — `fixtures/scripted_model.py` — the scripted model, an honestly-labelled stand-in** for the live model in all three roles (RR1); its registered description says it is a fake. It is selected by `REVIEW_MODEL_BACKEND=scripted`, reports model id `scripted` in every record, and behaves exactly as follows. A *clause* is a non-empty line of the fetched document other than a leading `REQUIREMENT:` line; a clause is *vague* when it contains one of: reasonable, reasonably, appropriate, appropriately, sensible, sensibly, efficiently, clearly, generous, quickly, promptly, common, regularly, periodically, relevant, timely, properly, securely, easily, aggressively.

- **Agent role**, each turn: (1) if no fetch result that is not an error exists yet → call `fetch_requirement(<ticket key from the opening message>)`; (2) else if `/analysis.md` has not been written → `write_file` with the §3.3 skeleton and Confirmed Facts = one bullet per clause quoting it verbatim — except that on the run's first attempt, when the document's key or filename stem is listed in `SCRIPTED_SKIP_CLAUSE_DOCS`, the **last** clause is omitted; (3) then one `edit_file` per remaining section in order: Ambiguities = one bullet per vague clause, `- **"<clause>"**` then `  Reason: "<word>" is not defined` and, **only if** the instructions text in its context contains `Resolved by:` or a grader feedback message is in the conversation, `  Resolved by: a stated value for "<word>"` and `  Edge case: a build that guesses "<word>" wrong fails in production`; Clarification Questions = one bullet `- What does "<word>" mean in "<clause>"?` per ambiguity; Assumptions = one bullet `- Assume "<word>" means the team's usual default until confirmed.` per ambiguity; Summary = exactly two sentences: `The document has <n> clauses and <m> ambiguities. Clarify the ambiguities before building.`; (4) then reply `Review complete.` with no tool call. **On grader feedback** it issues one `edit_file` per failing criterion in the feedback (completeness → rewrite Confirmed Facts with every clause; clarity and/or depth → one rewrite of Ambiguities with both labelled lines) and then replies `Revised.` Modes via `SCRIPTED_MODE`: `normal` (above); `stall` — every turn calls `fetch_requirement` again, forever; `rogue` — its second turn is `write_file("/memories/AGENTS.md", "tampered")`, then it continues as `normal`; `stubborn` — ignores feedback: on feedback it replies `Done.` with no edit.
- **Grader role**: first calls `read_file("/analysis.md")`; then returns `failed` if the rubric has no `- ` criterion lines; otherwise per criterion, in rubric order: completeness passes iff every clause appears verbatim in the file (gap `<k> clause(s) not addressed`); clarity passes iff every Ambiguities bullet has an indented line starting `Resolved by:` (gap `missing indented "Resolved by:" line on <k> ambiguity bullet(s)`); depth likewise for `Edge case:` (gap `missing indented "Edge case:" line on <k> ambiguity bullet(s)`); result `satisfied` iff all pass, else `needs_revision`; explanation is the gaps joined by `; `. When the document's stem or key is listed in `SCRIPTED_GRADER_ERROR_DOCS` (or that variable is `*`), the grader raises instead of answering. Mode `SCRIPTED_GRADER_NAMES=paraphrase` echoes criterion names as `Completeness of coverage`, `Clarity of resolution`, `Depth of consequence`.
- **Analyst role**: reads `/<label>/summary.json`, then every `/<label>/run_*.json`, then `/<label>/AGENTS.md`; writes `/proposal.md` with the five `##` sections of R21; returns: if clarity **and** depth each fail on the first attempt in more than half of graded runs → `target: prompt`, `section: ### Ambiguities`, `change: I1`, `issue` naming the two missing labelled lines, `recurrence: "<n>/<graded> runs: <run ids>"`, `evidence` = one quoted first-attempt gap string per failing run, `rejected` = every distinct first-attempt gap string that occurs in fewer than half of graded runs (as `"<gap>" — seen in <k>/<graded> runs, not a pattern`); otherwise `target: configuration`, `section: ""`, `change: "No criterion fails on a majority of first attempts; nothing to insert."`, `evidence: []`. `SCRIPTED_ANALYST_TARGET=tool|grader` forces that target with the same non-prompt fields.

**F5 — the live backend** (`REVIEW_MODEL_BACKEND=live`): the real platform model per R25. Only criteria tagged `live` use it.

**Replay note.** Every count below was replayed by hand over F1–F4: a `normal` agent run with `simulated_failures = s` takes `7 + s` model turns and `13 + 2s` trace steps; a feedback round adds `1 + <edits>` turns.

### 5.2 Criteria

Unless stated, Given includes: a fresh checkout, `REVIEW_MODEL_BACKEND=scripted`, `SCRIPTED_MODE=normal`, all `SCRIPTED_*` list variables unset, the server started on port 4000 against an empty `data/` directory. `review(...)` means `POST api/review` with the stated body and `instructions_version` defaulting to `v1`.

| AC | Given | When | Then | Rules |
|---|---|---|---|---|
| AC1 | fresh | `review({ticket_key: "REQ-100", rubric_iterations: 0})` | the record's trace step 1 is `Model reasoning` / `Calls fetch_requirement`, step 2 is `Tool` with the seed page body; the opening user message in the recorded conversation contains `REQ-100` and none of the page's clauses; `requirement_doc` equals the seed page v1 body | R1 |
| AC2 | fresh | `review({ticket_key: "REQ-100", rubric_iterations: 0, simulated_failures: 2})` | trace steps 1–6 are three `fetch_requirement` calls and their results, the first two results begin `Error`, the third is the document; `turns == 9`, `len(trace) == 17`; `status == "finished"`; `analysis.complete == true` | R2 |
| AC3 | fresh | the AC2 run | `stage_order == ["Confirmed Facts","Ambiguities","Clarification Questions","Assumptions","Summary"]`; the last trace action is `Finishes the review`; `/analysis.md` has the five `##` headings once each in that order | R3 |
| AC4 | fresh | `review({ticket_key: "REQ-100", rubric_iterations: 0})` with `SCRIPTED_MODE=stall` | `analysis.complete == false`, every count 0, and the run reports the missing sections `["Confirmed Facts","Ambiguities","Clarification Questions","Assumptions","Summary"]` and `in_order == true` (an empty order is in order) in its stage check | R3 |
| AC5 | fresh | `review({ticket_key: "REQ-100", rubric_iterations: 0})` | `counts == {"Confirmed Facts": 3, "Ambiguities": 2, "Clarification Questions": 2, "Assumptions": 2}`, `summary_words == 13`; each Ambiguities bullet is `- **"<clause>"**` with an indented `Reason:` line and no `Resolved by:` line; `complete == true` | R4 |
| AC6 | fresh | `review({ticket_key: "REQ-100", rubric_iterations: 0, max_turns: 12})` with `SCRIPTED_MODE=stall` | `turns == 12`, `status == "turn_limit_reached"`, last trace action `Stops: turn limit of 12 reached`, `analysis.markdown == ""` | R5 |
| AC7 | fresh | `review({ticket_key: "REQ-100", instructions_version: "nonexistent"})` | HTTP 400, `error` contains `memories/AGENTS.md`; no run record is stored; no model turn ran | R6 |
| AC8 | fresh | `review({ticket_key: "REQ-100", rubric_iterations: 0})` with `SCRIPTED_MODE=rogue` | trace step 4 is a `Tool` row whose detail begins `Error` (the denied write); `instructions` in the record equals `fixtures/instructions/v1/AGENTS.md` byte for byte; `turns == 8`; `complete == true`; the seed page still has exactly 1 version | R7 |
| AC9 | fresh | two consecutive `review({ticket_key: "REQ-100", rubric_iterations: 0})` calls | each record's `run_id` differs; the second run's trace step 3 is `write_file` (not a read of a leftover file); after both, no directory under the run-workspace root remains | R8 |
| AC10 | fresh | the AC2 run, with `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY=junk` exported | the run succeeds identically; `run_id` matches `^[0-9a-f]{8}$`; trace actors alternate `Model reasoning`/`Tool` for every tool call; every `detail` ≤ 221 characters; a source search of the app for `LANGSMITH` finds nothing | R9 |
| AC11 | fresh | `review({ticket_key: "REQ-100", rubric_iterations: 1})` | grading pass 1's `grader_actions[0] == "read_file:/analysis.md"`; grading pass 1 `criteria[1].gap == 'missing indented "Resolved by:" line on 2 ambiguity bullet(s)'` and `criteria[2].gap == 'missing indented "Edge case:" line on 2 ambiguity bullet(s)'` — the grader judged the file, which lacked the lines | R10 |
| AC12 | fresh | the AC11 run | `grading[0].result == "needs_revision"`, `criteria` passed flags `[true, false, false]`, both failing criteria carry a non-empty `gap`; `grading[0].analysis_markdown` contains no `Resolved by:`; a feedback message containing both gaps appears in the conversation after pass 1 | R11 |
| AC13 | fresh | `review({ticket_key: "REQ-100", rubric_iterations: 3})` | `len(grading) == 2`; pass 2 result `satisfied` with all three `passed == true`; `status == "satisfied"`; `turns == 9`; final file's two Ambiguities bullets each have indented `Resolved by:` and `Edge case:` lines; `counts` unchanged from AC5 | R11 |
| AC14 | fresh | `review({ticket_key: "REQ-100", rubric_iterations: 3})` with `SCRIPTED_MODE=stubborn` | `len(grading) == 4`, every pass `needs_revision`, `status == "max_iterations_reached"` (not `satisfied`) | R12 |
| AC15 | fresh | (a) `review({ticket_key: "REQ-100", rubric_iterations: 1, rubric: ""})`; (b) `review({ticket_key: "REQ-100", rubric_iterations: 1})` with `SCRIPTED_GRADER_ERROR_DOCS=REQ-100` | (a) one grading pass with `result == "failed"`, `criteria == []`, `status == "failed"`, no revision turn; (b) one pass `result == "grader_error"`, `criteria == []`, `status == "grader_error"`, `turns == 7` | R11, R13 |
| AC16 | fresh | `POST api/tickets/REQ-100/rerun` | the ticket becomes `Analysis Ready` with `last_analyzed_version == 1` and `last_run_id` set; one run exists with `status == "satisfied"`, `len(grading) == 2`; a comment by `Requirements Analysis Agent (bot)` names `satisfied`, `version 1` and `Analysis Report — REQ-100` | R14, R16 |
| AC17 | after AC16 | `POST api/tickets/REQ-100/close`; then `POST api/tickets {title: "Review requirements: calendar invites v2", description: "", linked_page_id: "page-shared-calendar-invitations", assignee: "Mei (QA Lead)"}`; then `POST api/pages/page-shared-calendar-invitations/versions {body: <seed body> + "\n\nInvitations expire after 7 days.", author: "Ana (Product Manager)"}` | the new ticket is `REQ-101` and creation ran it once; the page save returns `retriggered == ["REQ-101"]` (REQ-100 is `Done` and untouched); REQ-101 now has 2 runs, the latest with `requirement_version == 2` | R14, R16 |
| AC18 | after AC17 | `GET api/pages/page-analysis-req-101` and `GET api/pages/page-shared-calendar-invitations` | the report page has `kind == "analysis_report"`, `linked_ticket == "REQ-101"`, versions `n == [1, 2]`, both authored by the bot; version 2's body begins with a banner containing `REQ-101`, `version 2`, `satisfied` and `2 grading pass(es)` and then the analysis file verbatim; the requirement page has exactly 2 versions, both human-authored | R15 |
| AC19 | after AC17 | `GET api/tickets/REQ-101` | key matches `^REQ-[0-9]+$` and is `REQ-101`; status `Analysis Ready` (no run closed it); `POST api/tickets/REQ-101/close` → `Done`; a further `POST api/pages/page-shared-calendar-invitations/versions` returns `retriggered == []` | R16, R14 |
| AC20 | after AC17 | `GET api/tickets/REQ-101` and `GET api/pages/page-analysis-req-101/compare?a=1&b=2` | `changed.requirement_version == [1, 2]`, `changed.status == ["satisfied","satisfied"]`, `changed.counts == {"Confirmed Facts": [3, 4], "Ambiguities": [2, 2], "Clarification Questions": [2, 2], "Assumptions": [2, 2]}`; the compare `diff` contains a line beginning `+` that contains `Invitations expire after 7 days.`; `run_a` and `run_b` are the two runs | R17 |
| AC21 | fresh, then after AC17 | (a) first start on empty `data/`; (b) stop and restart the server | (a) `data/pages.json`, `data/tickets.json`, `data/runs.json` exist; `GET api/pages` returns exactly the F2 page with 1 version; `GET api/tickets` returns exactly `REQ-100` `Open`; `GET api/batches/v1` → 404; (b) `GET api/tickets/REQ-101` still has 2 runs and the ticket count is unchanged (no re-seed) | R18 |
| AC22 | fresh, `SCRIPTED_SKIP_CLAUSE_DOCS=01_session_timeout` | `POST api/batches {label: "v1", instructions_version: "v1"}` | `data/batches/v1/` holds `AGENTS.md` (== v1 fixture), `run_01_01_session_timeout.json` … `run_05_05_backup_retention.json`, `summary.json`; summary: `runs 5, graded 5, grader_errors 0`, `first_attempt == {completeness: {passed 4, total 5, pass_rate 0.8}, clarity: {0, 5, 0.0}, depth: {0, 5, 0.0}}`, `revisions_needed == 5`, `documents` in filename order; every run `status == "satisfied"` with 2 grading passes; run 01's first pass fails all three, runs 02–05 fail exactly clarity and depth; re-posting label `v1` overwrites the directory | R19, R24 |
| AC23 | fresh | (a) `POST api/batches {label: "v1err", instructions_version: "v1"}` with `SCRIPTED_GRADER_ERROR_DOCS=03_api_rate_limits`; (b) label `allerr` with `SCRIPTED_GRADER_ERROR_DOCS=*` | (a) `graded 4, grader_errors 1`, every `total == 4`, completeness `passed 4`, clarity `0`, depth `0`, `revisions_needed 4`; run 03 `status == "grader_error"`; (b) `graded 0, grader_errors 5`, every `pass_rate == null`, `revisions_needed 0` | R13, R19 |
| AC24 | fresh | the AC22 batch with `SCRIPTED_GRADER_NAMES=paraphrase` | `summary.first_attempt` keys are exactly `completeness, clarity, depth` with the AC22 values, although every recorded criterion `name` is the paraphrase | R20 |
| AC25 | after AC22 | `POST api/batches/v1/propose` | `change.target == "prompt"`, `change.section == "### Ambiguities"`, `change.change == I1`, `len(evidence) == 5` and each is one of the two labelled-line gap strings, `recurrence` begins `5/5 runs`; `proposal_markdown` has the five `##` sections of R21; `data/batches/proposal.md` exists and the batch's run files and `AGENTS.md` are byte-identical to before | R21 |
| AC26 | after AC25 | inspect `change.rejected` | exactly one entry, containing `1 clause(s) not addressed` and `1/5` | R21 |
| AC27 | after AC25 | `POST api/proposals/v1/apply {approved: true}` | returns `instructions_version == "v2"` and a `diff` whose non-header lines are all additions; the stored v2 text equals `fixtures/instructions/v2/AGENTS.md` byte for byte; the v1 text is unchanged; before approval, `GET api/batches/v1` shows no applied version | R22 |
| AC28 | fresh batch `v2` (AC29) | `POST api/batches/v2/propose` → `change.target == "configuration"`; then `POST api/proposals/v2/apply {approved: true}`; repeat with `SCRIPTED_ANALYST_TARGET=tool` and `=grader` | each apply returns HTTP 409 with an `error` telling the person to read the proposal and decide; no instructions version is created | R22 |
| AC29 | after AC27, `SCRIPTED_SKIP_CLAUSE_DOCS` unset | `POST api/batches {label: "v2", instructions_version: "v2"}`; `GET api/compare?before=v1&after=v2` | v2 summary: every criterion `passed 5 / total 5`, `revisions_needed 0`, every run 1 grading pass; comparison `criteria == {completeness: [4, 5], clarity: [0, 5], depth: [0, 5]}`, `revisions_needed == [5, 0]`, `attempts == [10, 5]`, `improved == ["completeness","clarity","depth"]`, `regressed == []`, `verdict == "success"`, `input_tokens` both > 0, `cost_usd == [0.0, 0.0]` (model `scripted` has no price) | R23 |
| AC30 | after AC29 | (a) `POST api/batches {label: "v3", instructions_version: "v2"}` with `SCRIPTED_SKIP_CLAUSE_DOCS=01_session_timeout`, then `compare?before=v2&after=v3`; (b) `compare?before=v1&after=v3`; (c) `POST api/batches {label: "v1b", instructions_version: "v1"}` with the same skip variable, then `compare?before=v1&after=v1b` | (a) `criteria.completeness == [5, 4]`, `regressed == ["completeness"]`, `verdict == "regression"`; (b) `criteria == {completeness: [4, 4], clarity: [0, 5], depth: [0, 5]}`, `revisions_needed == [5, 1]`, `verdict == "partial"`; (c) `improved == []`, `regressed == []`, `verdict == "no effect"` | R23 |
| AC31 | fresh | (a) all of `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL` unset, scripted backend: run AC13; (b) `REVIEW_MODEL_BACKEND=live` with `OPENAI_API_KEY` unset: `review({ticket_key: "REQ-100"})`; (c) source search of the app | (a) passes unchanged; (b) HTTP 503 with `error` naming `OPENAI_API_KEY`, no model call, no prompt to the user; (c) no literal key, no read of `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`, no base URL other than the value of `OPENAI_BASE_URL`, no model id other than the three role variables' values | R25 |
| AC32 | server running | fetch the page HTML and every script/stylesheet it references | no `href`, `src`, `action`, `fetch(`, `XMLHttpRequest` open, or `location` assignment uses a root-absolute path (none begins with `/`), and every API call the page makes resolves relative to the page URL | R26 |
| AC33 | server running | `GET http://127.0.0.1:4000/api/health`; inspect the listening socket (or the startup log line) | `{status: "ok"}`; the server is bound to `0.0.0.0:4000`; no second port is opened; no route upgrades to WebSocket | R26 |
| AC34 | after the whole suite | list every file named `AGENTS.md` under the workspace | only `fixtures/instructions/<version>/AGENTS.md` and `data/batches/<label>/AGENTS.md` exist; none at the workspace root; no run-workspace copy survives | R27 |
| AC35 `live` | `REVIEW_MODEL_BACKEND=live`, the lab's `OPENAI_API_KEY`/`OPENAI_BASE_URL` present, the three role variables set from `resolved-decisions.md` | `review({ticket_key: "REQ-100", rubric_iterations: 3})` | a `RunRecord` validating against §3 with `status` in `satisfied | max_iterations_reached`, `analysis.complete == true`, and every grading pass's `criteria` of length 3 | R25, R11 |
| AC36 `live` | as AC35 | `POST api/batches {label: "live1", instructions_version: "v1"}` then `POST api/batches/live1/propose` | a summary with `runs 5` and a `HarnessChange` validating against §3; if `target == "prompt"`, `change` is non-empty and `section` is a heading present in the v1 instructions | R19, R21, R25 |

Reciprocity: R1→AC1; R2→AC2; R3→AC3, AC4; R4→AC5; R5→AC6; R6→AC7; R7→AC8; R8→AC9; R9→AC10; R10→AC11; R11→AC12, AC13, AC15, AC35; R12→AC14; R13→AC15, AC23; R14→AC16, AC17, AC19; R15→AC18; R16→AC16, AC17, AC19; R17→AC20; R18→AC21; R19→AC22, AC23, AC36; R20→AC24; R21→AC25, AC26, AC36; R22→AC27, AC28; R23→AC29, AC30; R24→AC22; R25→AC31, AC35, AC36; R26→AC32, AC33; R27→AC34.

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the offline suite (§7) with the scripted backend before claiming any criterion, and cite its output per criterion.
- Keep every URL the page emits relative (R26) and every secret in environment variables (§2, R25).
- Write decisions, resolved values and results to files in the workspace — `resolved-decisions.md` first, then the §7 evidence report — because in this lab the workspace is the record: a new chat starts with no memory of this one and the grader sees only what is on disk. `[environment]`
- Record the Python version and the install's wall-clock cost in `resolved-decisions.md` before installing (§2). `[environment]`
- Seed the record store from `fixtures/seed/` on first start and never re-seed over data (R18).

**Ask First** — derived from the course's spoken trade-offs (CTX-C table); each either forces rework or changes a behaviour guarantee no criterion catches.
- Changing the **revision budget** (R11 lever, 3): changes how many times work is sent back without failing a criterion; the course set it 3 in the notebook and 2 in its automation module.
- Changing the **turn caps** (R5 lever, 12 / 40): a lower cap can end runs early without any criterion naming it.
- Changing the **simulated fetch-failure counts** (R2 lever, 2 for the demo / 0 elsewhere): adds turns and noise to batches (course's reason for 0 there).
- Changing **model tiering per role** in live mode (R25 lever: same model for agent and grader, a stronger one for the analyst): the course argues cost against capability; a weaker analyst "does the job unreliably", a stronger agent changes cost; no offline criterion observes it.
- Adding a **skills directory** or moving guidance between the always-on file and skills (row D1): moves the learning loop's insertion target.
- Switching the **grader realization** between agentic and deterministic (row D3): changes who judges coverage without failing the scripted suite.
- Making the analyst's proposal **auto-apply** or widening apply beyond `prompt` targets (R22): removes the human approval step silently.

**Never**
- Read, copy or paraphrase anything under the course's `materials/` while building; this spec is the only course source.
- Invent provenance: never label a choice course-derived unless this spec says so; never cite a lesson this spec does not cite.
- Let a run claim `satisfied` when a criterion failed, or `finished` when the turn cap ended it (R5, R12).
- Mutate `fixtures/` (documents, seed, instruction versions, the scripted model) to make a criterion pass; a failing criterion is a defect in the build.
- Ask the person for an API key, hardcode one, read the Anthropic pair, or guess at other variable names (R25). `[environment]`
- Write to any file in the `data/` store from a test fixture to fake a result; results come from runs.
- Author or edit a workspace-root `AGENTS.md` — the IDE rewrites it at every boot and the guidance is silently lost (R27). `[environment]`
- Use a root-absolute URL in the page, open a second port, or use WebSockets (R26). `[environment]`
- Commit, print or log a secret; never write `.env` contents into any file or report.

## 7. Test Plan & Self-Verification

```bash
python3 --version                                   # record it in resolved-decisions.md first
python3 -m venv --system-site-packages .venv && source .venv/bin/activate
pip install -r requirements.txt                     # the §2 pins; announce the cost before running
export REVIEW_MODEL_BACKEND=scripted
python -m app.server &                              # one server, 0.0.0.0:4000, background
curl -s http://127.0.0.1:4000/api/health            # {"status":"ok"}
python -m pytest tests -q -m "not live"             # the offline suite: AC1–AC34, one test function per AC, named test_ac<N>
python -m pytest tests -q -m live                   # AC35–AC36 only; needs the lab's ambient OPENAI_* and the three role variables
```

The build is **complete when the offline suite passes** with zero failures and zero skips among AC1–AC34. The `live` tests are additional; a failing live test is reported, never hidden, and never blocks completion.

**Evidence report, required.** After the suite, write `evidence.md` in the workspace with one line per acceptance criterion: `AC<N>: PASS|FAIL — <test name> — <file path of the artifact or the asserted value quoted from test output>`. "Should pass", "looks correct" and an untested criterion are all treated as FAIL — they mean it was not run. Every test asserts the concrete values in §5.2; a test that relaxes an asserted value is a defect, not a fix.

## Runtime (lab)

Everything in this section is `[environment]`: facts of the lab, never the course.

**Container.** Debian, non-root user; Node 22 and Python 3 with venv, sqlite3, git and build tooling present. Preinstalled Python: `fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`; preinstalled Node: `express`, `cors`, `better-sqlite3`, `vite`, `nodemon`. Nothing else — no vector stores, embedding models or ML frameworks. Outbound network works, so the §2 installs succeed, but each costs wall-clock time inside the session: batch the install once, early, and announce its cost. Create the venv with `--system-site-packages`; where a course pin conflicts with a preinstalled copy the course pin wins inside the venv (§2). The Python minor version tracks the image and is not stated: run `python3 --version`, record it, and stop with a report if a course pin refuses it. Memory is finite and shared with the agent's own process; this pipeline loads no local models, so no release-before-load rule is needed.

**Preview.** One server, port 4000, bound to `0.0.0.0`, serving the page and the API; nothing else is previewable. The preview is reverse-proxied under a path prefix, so every URL in the page must be relative. HTTP only: WebSocket upgrades are not proxied; streaming responses work. Long-running servers run in the background and every tool call is visible to the learner.

**Workspace.** The workspace is the record: a new chat has no memory of an earlier one and the grader sees only what is on disk, so `resolved-decisions.md` (§0 step 5) and `evidence.md` (§7) are load-bearing here, not formalities. The workspace-root `AGENTS.md` is rewritten by the IDE at every boot and is never authored; harness instruction files of that name live only inside app-owned folders (R27).

**Model / provider.** The lab fixes the model the coding agent itself runs on and exports `OPENAI_API_KEY`/`OPENAI_BASE_URL` and `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`, each base URL pointing at the platform proxy. The built app reads only the first pair (R25). Model ids are chosen at gate time through the "(Recommended)" flag and recorded in `resolved-decisions.md` as the three role variables; this spec never names a current model.

**Question mechanism.** The structured question tool is the fenced `choices` block described in §0's `[environment]` paragraphs.

**Environment failure modes** (enforced by the rules and criteria named; these never appear in CTX-B, which is the course's):

- **E1 — Root-absolute URL under the proxied preview.** *Symptom:* the page loads but every API call 404s or returns the IDE's HTML. *Cause:* a URL beginning `/` resolves against the IDE's root, not the app's prefix. *Fix:* relative URLs everywhere. Enforced by R26, AC32.
- **E2 — Wrong port or interface.** *Symptom:* "working" server, blank preview. *Cause:* bound to `127.0.0.1` or a port other than 4000. *Fix:* `0.0.0.0:4000`. Enforced by R26, AC33.
- **E3 — Guidance lost at reboot.** *Symptom:* instructions written to the workspace root vanish. *Cause:* the IDE rewrites the root `AGENTS.md`. *Fix:* keep harness files inside app folders. Enforced by R27, AC34.
- **E4 — Decisions left in chat.** *Symptom:* a later session cannot tell what was built from what. *Cause:* nothing written. *Fix:* `resolved-decisions.md` and `evidence.md`. Enforced by §0 step 5 and §7.
- **E5 — Key prompt or guessed variable.** *Symptom:* the app asks for a key, or reads a variable the container does not set. *Fix:* read exactly the named pair; fail with the variable's name. Enforced by R25, AC31.
- **E6 — Interpreter mismatch.** *Symptom:* a course-pinned package refuses to install. *Fix:* record the version first; stop with a report rather than loosening a pin silently. Enforced by §2.

## Course Context Pack (embedded — agent-readable)

Concepts only; no code from the course. Referenced by the position-independent `CTX-*` anchors.

### CTX-A. The pattern

`fetch(id) → agent loop → one analysis file → grader (rubric) ⟲ feedback → event trigger wraps it → batch of runs → analyst over traces → human-approved harness change → re-run and compare`

1. **Fetch by identifier** — the agent is built knowing only how to look a document up; the document enters at run time through a tool, as it would from a real tracker, and the tool can fail transiently, so the loop must retry (R1, R2).
2. **Agent loop** — a model repeatedly chooses a tool, observes the result, and continues until it decides it is done; the harness's file tools are the agent's hands, and its instructions arrive from a file loaded on every run (R3–R7).
3. **One file as the deliverable** — the analysis is a file the agent writes stage by stage, not a message; a file can be opened, counted, diffed and graded (R3, R4).
4. **Verification loop** — done is not good enough: a grader with a rubric reads the finished file, passes or fails each criterion, and sends specific gaps back so the same run revises; a budget bounds the retries; a cap on model turns is the backstop (R5, R10–R13). The course's point: explicit criteria raise reliability and let a cheaper model handle a harder task.
5. **Event-driven loop** — the agent is looped into the system where the work already happens: a created ticket or an edited requirement triggers the verification loop, the report lands back as a versioned page, and a human — never the agent — decides when the ticket is done (R14–R18).
6. **Traces as evidence** — agents are non-deterministic, so the story is in the traces: every message, tool call, grading pass and the file at each pass are recorded per run (R9, R19).
7. **Learning (hill-climbing) loop** — across many runs the same correction recurs; an analyst agent reads the batch summary, the runs and the current instructions, and proposes one literal change, rejecting what is not a pattern (R20, R21).
8. **Human review, then measure** — the change is applied by code only after approval, the batch is re-run, and a verdict says whether first-attempt pass rates rose without regression (R22–R24).

### CTX-B. Failure-mode catalog

- **CTX-B1 — Transient fetch failure.** *Symptom:* the fetch tool returns an error (service unavailable, timeout). *Cause:* an external system is briefly unreachable. *Fix:* retry the identical call until it succeeds; expected and normal. Enforced by R2, AC2. (Lesson 4.)
- **CTX-B2 — Stage skipped or reordered.** *Symptom:* a section left empty or filled out of order. *Cause:* the order is requested by instructions, not enforced by the harness. *Fix:* record the order each write actually filled and report incompleteness. Enforced by R3, AC3, AC4. (Helper docstrings.)
- **CTX-B3 — Retrying past the point of sense.** *Symptom:* a run that never finishes. *Cause:* the model keeps retrying or looping. *Fix:* a model-turn cap that ends the run and is reported distinctly from finishing. Enforced by R5, AC6. (Lesson 4: "max_turns matters when that path fails".)
- **CTX-B4 — Instructions silently missing.** *Symptom:* a plausible but bad review. *Cause:* the memory loader ignores a missing file without warning, so the agent runs on the system prompt alone. *Fix:* refuse to run when the file is absent. Enforced by R6, AC7.
- **CTX-B5 — Agent edits its own instructions.** *Symptom:* guidance drifts during a run. *Cause:* the instructions file sits in the same writable filesystem as the analysis. *Fix:* harness-level write denial on the instructions directory, not just a sentence in the prompt. Enforced by R7, AC8.
- **CTX-B6 — Stale analysis from a previous run.** *Symptom:* the agent reads a finished file and skips stages. *Cause:* a shared workspace across runs. *Fix:* a fresh workspace per run, deleted afterwards. Enforced by R8, AC9.
- **CTX-B7 — Grader judges by resemblance.** *Symptom:* criteria pass that the file does not satisfy. *Cause:* the grader reads the conversation, which can make a criterion look satisfied, or judges that the file "looks like" one that would pass. *Fix:* read the file, quote the satisfying text with its line number, apply labels literally, check every item. Enforced by R10, AC11.
- **CTX-B8 — Budget exhaustion read as success.** *Symptom:* a run that ran out of tries looks the same as one that passed. *Cause:* the last grading pass says `needs_revision` either way. *Fix:* a distinct terminal status. Enforced by R12, AC14.
- **CTX-B9 — Criteria matched by name.** *Symptom:* one recurring criterion split into several. *Cause:* the grader paraphrases criterion names run to run. *Fix:* key on position in rubric order. Enforced by R20, AC24.
- **CTX-B10 — Acting on a one-off.** *Symptom:* an instruction change for a problem one document had. *Cause:* a single occurrence mistaken for a pattern. *Fix:* majority threshold; minority observations recorded as rejected. Enforced by R21, AC26.
- **CTX-B11 — Analyst applies its own change (or edits the evidence).** *Symptom:* unreviewable, non-deterministic or half-applied harness edits. *Cause:* letting the agent write what it reasons from, or apply what it proposes. *Fix:* read-only traces, proposal only, human approval, plain-code insertion, non-prompt targets refused. Enforced by R22, AC27, AC28.
- **CTX-B12 — Grader error counted as a pass.** *Symptom:* inflated pass rates. *Cause:* a grading pass that errored carries no criteria. *Fix:* exclude from denominators and report the error count. Enforced by R13, R19, AC23.

### CTX-C. Decision background

**How to read the provenance notes.** A *litmus branch* is how an argued subject was resolved: a **row** (both sides shown working, differing in a component, identity or role), a **bake-in** (the course showed the other side failing, so the taught side is a rule), or a **lever** (the sides differ only in a value, so the value is a body default with an Ask-First entry). A *lever's value* is selected by: (1) the value the lesson's narration states aloud; else (2) the end-to-end application's config; else (3) the most frequent value, earliest-taught on ties. A *post-build lever* is a value the gate never asks about and the learner may change later. *Stakes* means whether choosing the other side up front changes structure, semantics or a guarantee; a contradiction that fails stakes is a lever, not a row. A *substitution row* is one whose Default departs from the course's own technology because that technology is *heavy* — the *heavy bar*: it needs a credential, a paid account, admin- or container-level setup, or special hardware (mere network access is not heavy). *Tiers* rank realizations by weight: (1) ships with the language's standard distribution, (2) an embedded library, (3) a locally served process; the lightest tier meeting the invariant at the fixture scale is taken.

**Mined spoken trade-offs and their dispositions** (every subject the course argued as a builder's choice; `narrative` only for framing the course did not argue as a choice):

| Subject | Lesson | Disposition |
|---|---|---|
| Instruction placement: always-on file vs skills behind a description (context cost vs always-on) | 3 | row D1 — both shown working, differ in component |
| Verification loop present vs "budget 0 is the basic agent loop" | 5 (and 2: loops are composable) | row D2 — limit value removes a component; course built the plain loop first and showed it working |
| Grader type: deterministic vs agentic (LLM as judge) | 2 (slide, narrated) | row D3 — presented, not argued, so not design-argued; admitted by the structural litmus (grader box changes owner) |
| Model tiering: cheaper model for simple tasks, stronger for the analyst; separate grader model | 2, 5, 7 (+README) | lever (tie-breaker 2: a choice of value within a lab-constrained dimension) → R25, Ask First |
| Revision budget 3 vs 2 | 5 narration/notebook vs automation module | lever (tie-breaker 2: value); branch 1 → 3 |
| Simulated fetch failures 2 vs 0 | 4 narration/notebook table/saved trace vs helper default | lever (tie-breaker 2: value); branch 1 → 2 for the demo, 0 for automation and batches by their own configs |
| Turn cap 12 vs 40 | 4 vs 5/6/7 | lever (tie-breaker 2: value); two configs for two modes, each cited at R5 |
| Analyst proposes, code applies after human approval vs agent applies/edits evidence | 7 module docstring; 2 oversight point 4 | bake-in R22 (tie-breaker 1: the other side described as "not analyzing anything" and "half-applied") |
| Grader judges the file vs the transcript | helper comments (Lesson 5 code) | bake-in R10 (tie-breaker 1: shown passing criteria the file does not satisfy) |
| Real chat/tracker integrations vs the shipped simulation | 6 | row RR2 (realization; real options unavailable in this lab, §1) |
| Hosted trace viewer vs local trace capture ("won't require a login") | 3 | retired realization row — every alternative unavailable here (Environment Resolutions); pinned §2, R9 |
| Scheduled vs event-driven triggers | 2 | narrative — presented as two kinds, no trade-off argued; §1 item 4 |
| Human at sensitive tool calls / as grader / on outputs / on harness changes | 2 | narrative framing; the two built points are rules R16, R22; the others §1 item 7 |
| Learning-loop targets: procedural (prompts, tools, skills) vs memory | 2 | narrative; prompt target built (R22), memory §1 item 5 |
| Fetch tool name `fetch_requirement` vs `fetch_requirement_from_jira` | 4 vs batch snapshots | contradiction failing stakes → body default at R1 (branch 1: narration) |
| Analysis counts vs text diff for "what changed" | 6 README | bake-in R17 (course shows counts alone misleading: "the content changed completely even though the shape didn't") |

**Background per row.**
- **D1.** The course's primer shows one always-on file (role, procedure, rules) and per-form skill files loaded by progressive disclosure: only name and description are in context until the agent reads the body. The review agent uses only the always-on file, whose Procedure half is fixed and whose Review guidance half is what the learning loop revises. The course's own file name is `AGENTS.md` under `memories/` (a slide also writes `Agent.md`; the code name is binding).
- **D2.** Lesson 4 builds the plain loop and shows it producing a complete report; Lesson 5 adds the grader and shows the first draft failing clarity and depth, then passing after feedback. The revision budget is "the number of times the grader may send work back"; the course names it 3 in the lesson and 2 in its automation module.
- **D3.** The course's grader is a model with a read-file tool and a system prompt that restates the harness's default grading rules (verdict definitions; the transcript is untrusted) and adds the file-first, quote-with-line-number, literal-label and check-every-item rules because the model otherwise "judges by resemblance". The course's docs-writer example names a mechanical grader ("links resolve, CI passes").
- **RR1.** Every course lesson ran live on the course's provider; the notebooks also replay saved traces when a flag is off. The scripted model replaces both: it drives the real pipeline rather than replaying a recording.
- **RR2.** The course's simulation: a ticket has a key, title, description, linked page, assignee from a fixed cast, status Open → Analysis Ready → Done, comments; a page has a kind, title, linked ticket and append-only versions; runs link a ticket, a requirement version and a report version. The course names the seam for a real integration explicitly: one trigger function a webhook would call, with page/ticket lookups swapped for the real APIs.
- **Model/provider (resolved).** The course used one small model for the agent and grader and a larger one for the analyst, with a price table for a cost estimate. Why tiering: the analyst "reads five full run traces and finds what recurs", the one job the cheaper model did unreliably.
- **Persistent store (§2).** Three plain JSON lists the course describes as a "database" a learner can open directly; seeded once on first import.
- **Course-declared constants kept as name-map** (not binding unless in §3): ticket ids in the course's fake tracker were `AUTH-142` (the default), `AUTH-101`, `NOTIF-205`, `PAY-310`, `ACCESS-118`, `ALERT-227`; the simulation's seed ticket `REQ-104` and page `page-req-upload`; batch labels `v1`/`v2` (kept); workspace dir `workspace`; analysis path `/analysis.md` and instructions path `/memories/AGENTS.md` (binding, §3.3/R6); trace labels `Model reasoning`/`Tool`, `Finishes the review`, `Stops: turn limit of N reached` (binding); status strings `satisfied`/`needs_revision`/`failed`/`grader_error` (binding); ticket statuses `Open`/`Analysis Ready`/`Done` (binding); report title `Analysis Report — <key>` and bot author (binding); the course's five requirement topics (authentication, notifications, payment retry, access control, alert escalation) and its file-upload example — replaced by F1/F2; the server port 5050 — replaced by 4000 `[environment]`; the course's run names/tags for its hosted tracer — dropped (presentation-only). Lesson 4's saved run reported 9 model turns and 17 steps with two simulated failures; the fixture replay reproduces the same counts from this spec's own fixtures.
- **Narrated outcomes the fixtures mirror.** Lesson 7: before the change, clarity and depth failed first attempt on most documents and completeness on one; after the change every document passed every criterion first attempt, with no revisions. F4's skip-clause knob reproduces that shape (4/5, 0/5, 0/5 → 5/5, 5/5, 5/5).

### CTX-D. Perishable assumptions

The concepts in CTX-A–C are durable. Treat these names as **search keywords against current documentation, not guaranteed imports or served models**:

- Harness: `deepagents` 0.7.11 — `create_deep_agent`, `FilesystemBackend(root_dir, virtual_mode=True)`, `FilesystemMiddleware`, `FilesystemPermission(operations, paths, mode)`, `RubricMiddleware(model, max_iterations, tools, system_prompt, on_evaluation)` (flagged beta in the course era; its default grader prompt must be restated when replaced), `memory=[...]`, `skills=[...]`, `permissions=[...]`, `response_format=`, invocation state key `rubric`, private status `_rubric_status`; file tools `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`, `delete`.
- Framework: `langchain` 1.3.x — `create_agent`, `langchain.agents.middleware.ModelCallLimitMiddleware(run_limit, exit_behavior="end")`, `langchain.tools.tool`; `langgraph` 1.2.x — `InMemorySaver`; model strings in `provider:model` form (`openai:…`); `stream_mode="updates"`.
- Course model ids (provenance only, never asserted served): `openai:gpt-5.4-mini` (agent, grader, batches), `openai:gpt-5.5` (analyst). Course price table per million tokens, short context: gpt-5.5 (5.00 in, 30.00 out), gpt-5.4-mini (0.75 in, 4.50 out); token counter `tiktoken` `o200k_base`.
- **Request-parameter compatibility:** message content may arrive as a list of content blocks on current models and a plain string on older ones (the course's helpers handle both); structured output and tool calling are required of any chosen model; do not assume sampling parameters are accepted by every platform model — a rejected parameter surfaces as a live API error on the first keyed run.
- Tracing: `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` (unused here).
- Web: `flask` 3.x; the course's simulation ran on port 5050 under `app.run(debug=True)`.

### CTX-E. Provenance map

Lesson numbering follows the transcripts (the course's folders and README each use a different numbering; the transcripts win). Nothing in this spec requires platform access.

| Lesson (transcript) | Contributed |
|---|---|
| 1 Introduction | the four-loop framing and the requirement-review agent as the running example (CTX-A) |
| 2 Overview of Loop Engineering | loop taxonomy and reasons (CTX-A 2, 4, 5, 7); model tiering (R25 lever); deterministic vs agentic graders (D3); composability (D2); human oversight points (R16, R22, §1 item 7); regressions check (R23); scheduled triggers and memory targets (§1 items 4, 5). Slides 2.2–2.13 read, all narrated |
| 3 Deep Agent Primer | always-on instructions file vs skills with progressive disclosure (D1); filesystem confinement (R7); local trace vs hosted viewer (R9, §1 item 3). Slides 3.2–3.5 narrated; 3.1 deck-only (title) |
| 4 Agent Loop | fetch by id, retry on transient failure, one file built stage by stage, turn cap, the five sections (R1–R5, CTX-B1–B3); instructions file and write denial (R6, R7); simulated failures 2 (lever); Slides 4.2–4.5 narrated; 4.1 deck-only |
| 5 Verification Loop | the three-criterion rubric, per-criterion pass/fail with gaps, feedback and revision, budget 3, cap 40, grader model may differ (R10–R13, D2, CTX-B7, B8); Slides 5.2–5.4 narrated; 5.1 deck-only |
| 6 Event-Driven Loop | triggers, separate report page, human closes, what-changed counts + diff, fresh workspace, budget 2 in automation (R8, R14–R18, RR2, §1 items 1–2); Slides 6.2–6.4, 6.6 narrated; 6.1, 6.5 deck-only |
| 7 Learning loop | batch runs, summary by first-attempt rate, criteria by position, analyst reads/proposes, rejected observations, human approval, code apply, re-run and compare, grader errors excluded (R19–R24, CTX-B9–B12, F3's two versions). Slide 7.2 narrated; 7.1 deck-only |
| 8 Conclusion | nothing beyond recap |
| Code-side evidence (helper modules, READMEs, docstrings, lock file) | parameters and constants in R2, R5, R9, R13, R19–R23; §2 pins; CTX-D names |
| **Environment (coding-agent-lab)** `[environment]` | deliverable shape (§1); container, venv, install cost, preinstalled set (§2, Runtime); platform model constraint and key variables (R25); port 4000, relative URLs, HTTP only (R26); workspace-root `AGENTS.md` ban (R27); workspace-is-the-record (§6, §7); the `choices` question mechanism (§0); failure modes E1–E6. None of these is attributed to any lesson |

---

*Status: v1 · course: Loop Engineering with LangChain DeepAgents · learner project: [the course's example shape — a requirements-review agent with four loops, on the §5 fixture corpus] · This is a living document: when the building agent produces something unexpected, add the missing constraint here and re-run.*
