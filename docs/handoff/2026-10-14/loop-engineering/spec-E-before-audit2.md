# Spec: Requirements Review Loops app — Coding-Agent-Lab Build

> **What you're building:** a web app with a simulated issue tracker and a simulated wiki in which a requirements-review agent runs, gets graded, is triggered by events, and learns from its own run history. You open the tracker in the preview pane, create a ticket that links to a vague requirement page, and watch the agent fetch the page, write a five-section analysis, get sent back by a grader until the rubric passes, and post the report as a new page version; you then edit the requirement and see the open ticket re-analyzed automatically. On the Learning page you run a batch of five documents, read the analyst's proposal, approve it, and see the re-run pass every criterion on the first attempt. Answering the gate's first question with the recommended baseline builds all of this end-to-end; the build is COMPLETE when the offline suite passes — the ambient platform keys unlock only the `live` tests and live use of the finished app.
>
> This file is self-contained: the Course Context Pack at the end replaces every external course reference.
>
> `(CTX-X)` anchors mark course-derived knowledge; the Decision Ledger below holds every point where the build could diverge, each pinned to one course-derived default, so the spec builds as-is with no intake.
>
> Generated from the *Loop Engineering with LangChain DeepAgents* notebooks + transcripts + slides on 2026-10-13, guide @ `b03ddc9`, coding-agent-lab overlay @ `184a0ed`.

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

   *`[environment]` In this lab the structured question tool is a fenced `choices` block: explain in prose above the fence, put the fence last in the message with one option per line, and precede it with a line `**Question 1 of M — <decision>**` so nothing skipped goes unseen. A click sends the option line verbatim; a typed answer naming an option counts identically. Only the latest message's buttons stay live, so a changed answer is re-asked as a new question — never ask anyone to go back and change an earlier one.*

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

   *`[environment]` Each row is one message ending in its own `choices` fence, headed `**Question N of M — <decision>**` with M the number of Ledger rows plus one. A click and a typed answer naming an option are equivalent. Because only the latest message's buttons stay live, an answer the person wants to change is re-asked as a new question, never edited in place.*

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

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option. Row ids: `L<n>` learner, `D<n>` design, `RR<n>` realization — never a bare `R<n>`, which names a business rule. Rows are in gate order: learner → design (argued and structural interleaved by pipeline position) → realization. The learner-context rows the lab resolved are listed in the Environment Resolutions table that follows, not here.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L6 | learner | **Scope boundary** — present the §1 "Not Included" list, item by item with its handling tag, *inside this question*, and ask whether every item stays out. | — | Keep as-is: every §1 exclusion stands; the full acceptance set is built. | (a) keep every exclusion; (b) bring something back — name the item in free text; items tagged `restorable` are added to the build, `buildable, unparameterized` are added with no spec parameters or criteria, `owned-by-row` defer to that row, `unavailable` cannot be taken here (the seam is stated). A genuine new exclusion is also free text and must name the acceptance criteria it retires. | Bringing an item back adds work the acceptance suite does not cover; retiring criteria removes verification. | learner |
| D1 | design-argued | **Instruction placement** — how the review agent's standing instructions reach it. | The agent's instructions exist as a file loaded into context at the start of every run, readable and editable from outside the agent (the learning loop edits it), and the agent itself is denied writes to it (R6, R7). | Always-on instruction file only: a memory file loaded every run, with a one-line system prompt that points at it (what the course's review agent uses in Lessons 4–7). Example-realization note: the file's *content* is the course's example procedure and is expected to be swapped when the project differs; the invariant is what survives. | (a) memory file + pointer system prompt (course default); (b) memory file **plus a skills directory** read by progressive disclosure — one description line per skill always in context, the full procedure read only when the agent decides it applies (built and shown working in the course's poet primer, Lesson 3). Under (b) the memory file keeps `Procedure` and the four `Review guidance` level-3 sections become one skill file each with a one-line description; this alters R6 (the level-3 headings are required in the skill files, not the memory file), R17–R19 (a proposal's `section` names a skill file and apply inserts at the end of that file) and the scripted analyst's target, and retires AC9's byte-identity to `instructions_v1.md`, AC35's equality with `instructions_v2.md` and AC37 — each replaced by the same assertion against the skill files. This spec authors no skill content. | Lesson 3 argues both sides: the always-on file "costs context on every call, so it should stay short"; skills cost "twenty lines of context, not twenty documents" and the agent pulls detail only for the one it needs. Litmus branch: a **row** — both sides built and shown working (primer with skills, review agent without); the sides differ in a component (a skills directory), not a value. Switching to (b) moves the per-section review guidance into skill files and changes what the learning loop's proposal targets (CTX-C1). | course+learner |
| D2 | design-argued | **Verification stage present** — does a grader wrap the agent loop and send work back? | When present, a grader stage separate from the agent judges the finished file against the rubric after the agent declares completion, and can return it with per-criterion feedback (R10, R11). The learning loop's signal (first-attempt verdicts) exists only when the grader exists. | Grader on, with a revision budget — the course's Lesson 5–7 configuration. The budget *value* is a post-build lever pinned in R11, not part of this row. | (a) grader wraps the agent loop with a revision budget (course default); (b) agent loop alone — revision budget 0, exactly the Lesson 4 build (the course: "if you set this to 0, you will have the same basic agent loop you built in the last lesson"). Criteria that apply only under (a): AC13–AC17, AC19, AC20, AC28, AC31–AC35, AC39, AC46–AC48 (every assertion of a grading pass, a `satisfied` status or a first-attempt pass rate); AC3, AC10, AC11 and AC22 keep their trace assertions but their run status is `ungraded`; AC18 exercises (b). | Lesson 5: "just because the agent says it is done, is the analysis actually good enough? In the agent loop, nothing is checking for this"; Lesson 2: verification "adds reliability" and "you don't need the verification loop per se" when composing loops. Litmus branch: a **row** — the course built the bare loop first (Lesson 4), showed it working at reduced scope, then wrapped it; a budget of 0 removes a component (the grader box), so this is a component choice, not a knob. A first draft the grader later rejects is the reason the grader is added, not the bare loop failing. Choosing (b) retires every grader AC and leaves the learning loop with no first-attempt pass-rate signal (CTX-C2). | course+learner |
| D3 | design-structural | **Grader kind** — what judges the file against the rubric. | Under D2 (a), the grader stage judges the *file the agent wrote*, never the conversation, criterion by criterion as pass/fail, returns a gap per failed criterion, and never edits the file (R10). | A model-driven judge that reads the file with a read tool and must quote line-numbered evidence for every pass (the course's review-agent grader, Lessons 5–7). | (a) model-as-judge with mandatory file read and verbatim quotes (course default); (b) a deterministic code grader that checks each criterion mechanically — the course's docs-writer example grader ("links resolve, CI passes", Lesson 2) and the narrated Lesson 2 slide: "graders can either be deterministic or agentic". Does not apply under (b): AC13 (a code grader makes no tool call and quotes no `L<n>:` evidence) and AC20's injected grader exception (the `grader_error_doc02` variant belongs to the scripted model's grader role; a code grader needs its own fault injection to reach `grader_error`); every other grader criterion asserts only the verdict shape, which (b) must produce identically. | Lesson 2 names both kinds; the course argues no trade-off between them, so this row enters on structure alone: the grader box's owner moves from the model to harness code. (a) can judge "every clause addressed" semantically but is prone to passing by resemblance — the failure the course's quote-with-line-number rule exists to stop (CTX-B4); (b) is reproducible and free but can only check what a label or regex can see. Redraw the diagram: the grader box changes owner. | course+learner |
| RR1 | realization | **Acceptance-suite model** — which model the offline acceptance suite runs the pipeline against. | The offline suite drives the real pipeline end to end — tool calls, grader (when D2 = (a)), event trigger, batch, analyst, apply, compare — against a stand-in whose per-role responses are declared in §5; criteria needing a real model are tagged `live`. | The **scripted model** stand-in declared in §5 (`scripted_model.py`) — an honestly-labelled fake standing in for the live model, so the suite runs with zero setup. Branch: substitution (the model is the keyed dependency); tier 1 — a module in the build itself, no package, no process. | (a) scripted stand-in (fake; see §5); (b) the course's live models through the platform proxy (course default — the lab exports the keys, so choosing it costs no setup here; it makes the suite non-deterministic and slow, and R22 governs which variables are read). Exact-value criteria that exercise only the scripted Default — under (b) each becomes a shape assertion like AC39's: AC1, AC3, AC4, AC7, AC10–AC14, AC17–AC20, AC22, AC28, AC32, AC33, AC35, AC45–AC47. | Lesson 4's notebook note: "LLMs do not always produce the same results … the agent behavior you experience may differ from the video." The scripted model is deterministic by construction; the live path is what the finished app uses. | course+learner |

## Environment Resolutions

This spec was generated for the **coding-agent-lab** environment. The six learner-context dimensions below were derived from the course first and then resolved against the lab, not skipped; two course-owned rows also left the Ledger through this table because every alternative to their default is untakeable here.

| Dimension | Resolution | Where the Invariant lives now |
|---|---|---|
| project | **ANSWERED** — the lab fixes the assignment: the served requirements-review loops app described in §1 (the course's example scenario shape on the synthetic fixture corpus). | spec §1 Objective. Invariant empty — owes no AC. |
| data/inputs | **ANSWERED** — inputs are seeded into the workspace as the §5 fixture corpus. Derived Invariant: a requirement is text addressed by an identifier the agent is handed; the agent fetches it through a tool at run time and is never handed the text in its opening message. | spec §5 fixture corpus + business rule R1 (AC1, AC2). |
| goal | **ANSWERED** — the lab fixes what "working" means: §1's objective and the acceptance criteria. | spec §1 + §5. Invariant empty — owes no AC. |
| model/provider | **CONSTRAINED** — the built app needs an LLM (the review agent, the grader when D3 = (a), the analyst). Platform models only; keys and base URLs read from the environment; the learner is never asked for a key. Derived Invariant: the models must support native tool calling, and the analyst's model must support a structured (typed) final response; models are addressed through a `provider:model` string. | spec §2 (model-role variables) + business rule R22 (AC38, AC39, AC48) + CTX-D. The course's model-tiering argument becomes a body lever (R22) with an Ask-First entry. |
| environment | **ANSWERED** — the container. Derived Invariants: the agent's file tools are confined to a per-run workspace root; the instruction file is loaded every run and editable from outside the agent; pages, tickets, runs and batches survive a process restart. | spec §2 + `## Runtime (lab)`; capability invariants moved to R6–R9 (AC8–AC12) and R25 (AC41). |
| scope-boundary | **KEPT** | Ledger row L6. |
| event-source surfaces (course-owned realization row) | **ANSWERED — every alternative unavailable here.** The course demonstrated the same agent inside real Slack and real Jira/Confluence; those need a Slack workspace with app tokens or an Atlassian site with an API token and a public tunnel — credentials the lab does not supply and this spec may never ask for. The only takeable realization is the course's own shipped keyless one: the simulated tracker and wiki. | Pinned in §2 ("event surfaces") with the course's provenance; §1 Not Included carries the real integrations as `unavailable` with the seam named. Invariant (an event in the surface where work happens triggers the loop and the result is written back there) lives in R14–R16 (AC24–AC32). |
| hosted tracing (course-owned realization row) | **ANSWERED — every alternative unavailable here.** The course's optional hosted tracing needs an account and an API key the lab does not supply. The keyless local trace capture the course uses from Lesson 4 on carries the whole taught behavior. | Pinned in §2 ("trace capture"); §1 carries hosted tracing as `unavailable` with the seam named. Invariant (every model turn and tool result of a run is recorded and viewable) lives in R12 (AC19). |

## 1. Objective

A single web app, served by one process, in which an engineering team's requirement documents are reviewed by an agent that fetches a requirement by ticket id, writes a structured analysis file (confirmed facts, ambiguities, clarification questions, assumptions, summary), is graded against a three-criterion rubric and sent back with feedback until it passes, is triggered automatically by events in a simulated issue tracker and wiki, and is improved across runs by an analyst that reads a batch's run history and proposes one instruction change for a human to approve — with the guarantee that every grader verdict is about the file on disk, every record of a run survives a restart, and nothing in the harness is changed without a human approving it (pattern: CTX-A).

**Deliverable shape** `[environment]`: one server on port 4000 serving both the pages and their API, because the preview pane is the learner's only view of the running app. The course's own artifacts — notebooks and a local Flask demo on port 5050 — are not the deliverable; this served app embodies the same pattern. The app has three surfaces: **Tracker** (tickets), **Wiki** (requirement pages and agent-authored report pages, with version history and diffs), and **Learning** (run a batch, view the summary and recurring gaps, read the proposal, approve and apply, re-run and compare).

**Adapting this beyond the lab.** The project, data and goal dimensions are fixed in this section and in §5's fixture corpus — replace the fixture documents with your own tracker's and change the objective. The model/provider dimension is constrained to the platform proxy in R22 and §2 — outside the lab, R22's variables become your own provider's, and the course's models (CTX-D) are a starting point. The environment dimension lives in §2 and `## Runtime (lab)` — port, URL form and the venv rule are the lab's; the capability invariants (R6–R9, R25) are the course's and travel with you. The two realization rows the lab retired (event surfaces, hosted tracing) are pinned in §2 and listed below as `unavailable` with their seams; outside the lab they become gate questions again.

### Not Included

Each item carries its handling tag so the L6 gate question is determinate.

1. **Real Slack bot** (the course demonstrated the agent answering direct messages and channel mentions) — `unavailable`: needs a Slack workspace, an app-level token and a bot token the lab does not supply. Seam: the function the Tracker's "create ticket" and the Wiki's "save page" call to run one analysis (R14) is what a Slack event handler would call; the report body is what it would post back.
2. **Real Jira and Confluence** (the course demonstrated tracker automation rules calling the agent through a tunnel) — `unavailable`: needs an Atlassian site, an API token and a public tunnel. Seam: the simulated tracker's ticket lookup and the simulated wiki's page lookup/version-append are the calls a REST client would replace; the trigger function stays the same.
3. **Hosted trace viewer** (the course's optional LangSmith tracing) — `unavailable`: needs an account and an API key. Seam: tracing in the course's framework is switched on by environment variables alone; the local trace table (R12) remains the record.
4. **Scheduled triggers** (the course names "a schedule triggers" as an event kind and a morning-calendar agent as an example) — `buildable, unparameterized`: the course built only event and manual triggers; the spec supplies no schedule parameters and no acceptance criteria for one.
5. **Human approval at sensitive tool calls inside the agent loop** (named in Lesson 2's oversight list) — `buildable, unparameterized`: the review agent has no sensitive tools; the course built no interrupt. Human approval of the harness change (R17) and of ticket closure (R16) *are* built.
6. **A code interpreter or sandbox, subagents, summarization or context offloading** (deep-agent pillars the course lists but never uses in this agent) — `buildable, unparameterized`.
7. **Token and cost accounting per batch** (the course prints an estimated cost next to the comparison) — `restorable`: additive, owned by no row; if restored, it is informational only and never changes a verdict.
8. **Multiple analyses per ticket in parallel, a real database** — `buildable, unparameterized`: named by the course (concurrent runs; database-backed filesystems, CTX-C10) but never built; the spec supplies no parameters and no acceptance criteria for either.
9. **A hand-built skills directory for the review agent** — `owned-by-row` D1(b).
10. **Running the course's notebooks or the Flask demo as shipped** — `unavailable` in this build mode: the deliverable is the served app.
11. **Authentication and user accounts** — `restorable`: additive, owned by no row and not named by the course; if restored, no spec parameter or criterion covers them and no existing criterion may change.

## 2. Tech Stack & Versions

Secrets are read from the environment only — never hardcoded, never written to any file, never asked for.

| Component | Pinned choice | Note |
|---|---|---|
| Language / runtime | Python 3 — the container's interpreter | `[environment]` Run `python3 --version` first, record it in `resolved-decisions.md`, and stop with a report if a course-pinned package refuses the interpreter. The course requires Python ≥3.12 (its project file; its notebooks ran 3.12.10). Never assume the floor is met. |
| Virtual environment | `venv` created with `--system-site-packages` | `[environment]` The preinstalled stack (`fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`) stays reusable for packages the course left unpinned. Where a course pin and a preinstalled copy differ, **the course pin wins inside the venv** (this applies to `openai` and `python-dotenv` below). Batch every install into one early step and announce its wall-clock cost before running it. |
| Agent harness | `deepagents` **0.7.11** | **Course install situation, stated honestly:** the course's project file sets floors (`deepagents>=0.7.11`, `langchain>=1.3.14`, `langchain-core>=1.5.0`, `langchain-openai>=1.4.0`, `langgraph>=1.2.9`, `openai>=2.47.0`, `pydantic>=2.13.4`, `python-dotenv>=1.2.2`) and its lock file resolves exact versions; §2 pins the lock's exact versions as provenance. The course's grader prompt was copied from this exact version's default and the course warns to compare before upgrading. Era-specific class and parameter names are perishable: see CTX-D. |
| LangChain core | `langchain` **1.3.18**, `langchain-core` **1.6.1**, `langgraph` **1.2.11** | Course lock pins. |
| Provider client | `langchain-openai` **1.6.0**, `openai` **3.6.0** | Course lock pins; `openai` pin wins over the preinstalled copy inside the venv. The provider is addressed by the `provider:model` string form; which models, see R22. |
| Structured output | `pydantic` **2.13.5** | Course lock pin; the analyst's typed change object (§3). |
| Env loading | `python-dotenv` **1.2.3** | Course lock pin; reads only the variables R22 names. |
| Web framework | Flask, newest release ≥ 3.1.3 | The course's demo used Flask with floor `>=3.1.3` and **no lock entry** — unpinned, so a modern version is chosen (that is the one unpinned course dependency). Serves pages and API on one port (R23). |
| Persistent store | JSON files on local disk — three record lists (pages, tickets, runs) plus one directory per batch holding one JSON per run, a summary and an instructions snapshot | The course's own realization (flat JSON lists "so a learner can open any of these files directly"). Not a Ledger row: it is keyless, never argued, and structurally identical across alternatives. Tier reasoning: among realizations satisfying R25 (records survive restart; a page's versions, a ticket's status and a run's grading passes are recoverable) at the fixture scale (six documents, tens of runs), tier 1 — the language's standard library (`json` + the filesystem) — meets the contract exactly, so no embedded database (tier 2, e.g. the container's sqlite3) is stepped up to. Scaling realizations are a later concern, not a row. |
| Event surfaces | Simulated tracker + wiki inside the app | Pinned by the Environment Resolutions table (course default — the course's shipped code; the real integrations are §1 `unavailable`). |
| Trace capture | Local, in-app: one trace row per model turn and tool result, stored on the run record | Pinned by the Environment Resolutions table (course default from Lesson 4 on; hosted tracing is §1 `unavailable`). |
| Model-role variables | `REVIEW_MODEL`, `GRADER_MODEL`, `ANALYST_MODEL` | `[environment]` One variable per model role, each holding a `provider:model` string for a platform model. The build agent sets them when it writes `resolved-decisions.md` — that file carries one "model roles" line with the agent's "(Recommended)" platform model per role, and the person's confirmation of the checklist confirms them; no extra gate question. The course's own ids are provenance only (CTX-D) and are never asserted to be served by the proxy. |
| Key variables | `OPENAI_API_KEY` + `OPENAI_BASE_URL` (read); `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL` (present, unread) | `[environment]` The app reads exactly the first pair (the course's provider); the second pair is present in the container and must not be read (R22). Never hardcoded, never guessed, never asked for. |
| Token counting | `tiktoken` 0.14.0 (course lock pin) | Only if §1 item 7 is restored; otherwise not installed. |
| Test runner | `pytest`, newest release | Project hardening: the course had no test suite; the offline suite in §5/§7 is this spec's addition. |

## 3. Input/Output Contracts

All four objects are JSON Schema (draft 2020-12). Field names that the course declared are binding (CTX-C name-map); the schemas push behavior into constraints so they self-enforce.

### 3.1 Analysis file (`/analysis.md` inside the run workspace) — parsed form

The file is Markdown; this is the shape the parser must recover from it, and the shape the grader and the counts are computed over.

```json
{
  "$id": "analysis",
  "type": "object",
  "required": ["confirmed_facts", "ambiguities", "clarification_questions", "assumptions", "summary"],
  "properties": {
    "confirmed_facts": { "type": "array", "items": { "type": "string", "minLength": 1 } },
    "ambiguities": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["clause", "reason"],
        "properties": {
          "clause": { "type": "string", "minLength": 1, "description": "the exact clause, quoted" },
          "reason": { "type": "string", "minLength": 1 },
          "resolved_by": { "type": "string", "minLength": 1, "description": "the indented 'Resolved by:' line; required by the clarity criterion, not by the file format" },
          "edge_case": { "type": "string", "minLength": 1, "description": "the indented 'Edge case:' line; required by the depth criterion, not by the file format" }
        }
      }
    },
    "clarification_questions": { "type": "array", "items": { "type": "string", "minLength": 1 } },
    "assumptions": { "type": "array", "items": { "type": "string", "minLength": 1 } },
    "summary": { "type": "string", "description": "prose, two or three sentences; counted in words, never in bullets" }
  }
}
```

Section headings, in order and binding: `Confirmed Facts`, `Ambiguities`, `Clarification Questions`, `Assumptions`, `Summary` (each a level-2 heading). An ambiguity bullet is a bold quoted clause followed by an indented `Reason:` line; `Resolved by:` and `Edge case:` are additional indented labelled lines, exactly those labels. "Counts" means bullets per list section — the four list sections only; "complete" means every list section has at least one bullet and the summary has at least one word.

### 3.2 Run record (one per analysis run; event runs and batch runs share it)

```json
{
  "$id": "run",
  "type": "object",
  "required": ["id", "trigger", "requirement_doc", "instructions", "trace", "grading", "analysis_markdown", "status", "turns", "counts", "started_at"],
  "properties": {
    "id": { "type": "string", "pattern": "^[0-9a-f]{8}$", "description": "8 lowercase hex characters (the course's id alphabet and length)" },
    "trigger": { "type": "string", "enum": ["ticket_created", "page_saved", "manual_rerun", "batch"] },
    "ticket_key": { "type": "string", "pattern": "^[A-Z]+-[0-9]+$" },
    "requirement_page_id": { "type": "string" },
    "requirement_version": { "type": "integer", "minimum": 1 },
    "report_page_id": { "type": "string" },
    "report_version": { "type": "integer", "minimum": 1 },
    "doc_name": { "type": "string", "description": "batch runs only" },
    "label": { "type": "string", "description": "batch runs only: the batch label" },
    "model": { "type": "string", "description": "the provider:model string the review role ran on, or the scripted stand-in's name" },
    "workspace": { "type": "string", "minLength": 1, "description": "absolute path of the run's workspace root at run time; recorded for every run, including event runs whose directory R9 discards afterwards" },
    "requirement_doc": { "type": "string", "minLength": 1 },
    "instructions": { "type": "string", "minLength": 1, "description": "the instruction file this run was given, verbatim" },
    "trace": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["step", "actor", "action"],
        "properties": {
          "step": { "type": "integer", "minimum": 1 },
          "actor": { "type": "string", "enum": ["Model reasoning", "Tool"] },
          "action": { "type": "string", "minLength": 1 },
          "detail": { "type": "string", "maxLength": 221, "description": "tool result text, whitespace-collapsed, cut at 220 characters plus an ellipsis" }
        }
      }
    },
    "messages": { "type": "array", "description": "batch runs only: every message untruncated — type, content, tool_calls with full args, tool_call_id, status" },
    "grading": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["iteration", "result", "explanation", "criteria", "analysis_markdown"],
        "properties": {
          "iteration": { "type": "integer", "minimum": 1 },
          "result": { "type": "string", "enum": ["satisfied", "needs_revision", "failed", "grader_error"] },
          "explanation": { "type": "string" },
          "criteria": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["name", "passed"],
              "properties": {
                "name": { "type": "string" },
                "passed": { "type": "boolean" },
                "gap": { "type": "string" },
                "evidence": { "type": "string", "description": "verbatim quote with its line number; required when passed is true under D3 option (a)" }
              },
              "if": { "properties": { "passed": { "const": false } } },
              "then": { "required": ["gap"] }
            }
          },
          "analysis_markdown": { "type": "string", "description": "the file exactly as this pass saw it" }
        },
        "allOf": [
          { "if": { "properties": { "result": { "const": "satisfied" } } },
            "then": { "properties": { "criteria": { "minItems": 1, "items": { "properties": { "passed": { "const": true } } } } } } },
          { "if": { "properties": { "result": { "const": "needs_revision" } } },
            "then": { "properties": { "criteria": { "contains": { "properties": { "passed": { "const": false } } } } } } },
          { "if": { "properties": { "result": { "const": "grader_error" } } },
            "then": { "properties": { "criteria": { "maxItems": 0 } } } }
        ]
      }
    },
    "analysis_markdown": { "type": "string" },
    "status": { "type": "string", "enum": ["satisfied", "max_iterations_reached", "failed", "grader_error", "ungraded"], "description": "ungraded = no grader configured (D2 option b)" },
    "turns": { "type": "integer", "minimum": 0 },
    "counts": {
      "type": "object",
      "required": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions"],
      "additionalProperties": false,
      "properties": {
        "Confirmed Facts": { "type": "integer", "minimum": 0 },
        "Ambiguities": { "type": "integer", "minimum": 0 },
        "Clarification Questions": { "type": "integer", "minimum": 0 },
        "Assumptions": { "type": "integer", "minimum": 0 }
      }
    },
    "started_at": { "type": "string", "description": "UTC timestamp" }
  }
}
```

### 3.3 Tracker and wiki records

```json
{
  "$id": "surfaces",
  "$defs": {
    "ticket": {
      "type": "object",
      "required": ["key", "title", "description", "linked_page_id", "assignee", "status", "comments", "created_at", "last_analyzed_version", "last_run_id"],
      "properties": {
        "key": { "type": "string", "pattern": "^[A-Z]+-[0-9]+$" },
        "title": { "type": "string", "minLength": 1 },
        "description": { "type": "string" },
        "linked_page_id": { "type": "string", "minLength": 1 },
        "assignee": { "type": "string", "minLength": 1 },
        "status": { "type": "string", "enum": ["Open", "Analysis Ready", "Done"] },
        "comments": { "type": "array", "items": { "type": "object", "required": ["author", "text", "timestamp"] } },
        "created_at": { "type": "string" },
        "last_analyzed_version": { "type": ["integer", "null"] },
        "last_run_id": { "type": ["string", "null"] }
      }
    },
    "page": {
      "type": "object",
      "required": ["id", "kind", "title", "linked_ticket", "versions"],
      "properties": {
        "id": { "type": "string", "pattern": "^page-[a-z0-9-]+$" },
        "kind": { "type": "string", "enum": ["requirement", "analysis_report"] },
        "title": { "type": "string", "minLength": 1 },
        "linked_ticket": { "type": ["string", "null"] },
        "versions": {
          "type": "array",
          "items": { "type": "object", "required": ["n", "author", "timestamp", "body"],
            "properties": { "n": { "type": "integer", "minimum": 1 }, "author": { "type": "string" }, "timestamp": { "type": "string" }, "body": { "type": "string" } } }
        }
      },
      "allOf": [
        { "if": { "properties": { "kind": { "const": "requirement" } } }, "then": { "properties": { "linked_ticket": { "type": "null" }, "versions": { "minItems": 1 } } } },
        { "if": { "properties": { "kind": { "const": "analysis_report" } } }, "then": { "properties": { "linked_ticket": { "type": "string" } } } }
      ]
    }
  }
}
```

Version numbers are contiguous from 1 in append order. A report page's every version is authored by the bot author string; a requirement page's versions are authored by a person from the fixed cast (§5).

### 3.4 Batch summary and harness change

```json
{
  "$id": "learning",
  "$defs": {
    "summary": {
      "type": "object",
      "required": ["label", "model", "runs", "graded", "grader_errors", "first_attempt", "revisions_needed", "documents"],
      "properties": {
        "label": { "type": "string", "minLength": 1 },
        "model": { "type": "string" },
        "runs": { "type": "integer", "minimum": 0 },
        "graded": { "type": "integer", "minimum": 0 },
        "grader_errors": { "type": "integer", "minimum": 0 },
        "first_attempt": {
          "type": "object",
          "required": ["completeness", "clarity", "depth"],
          "additionalProperties": { "type": "object", "required": ["passed", "total", "pass_rate"],
            "properties": { "passed": { "type": "integer" }, "total": { "type": "integer" }, "pass_rate": { "type": ["number", "null"] } } }
        },
        "revisions_needed": { "type": "integer", "minimum": 0 },
        "documents": { "type": "array", "items": { "type": "string" } }
      }
    },
    "harness_change": {
      "type": "object",
      "required": ["target", "issue", "recurrence", "evidence", "section", "change", "rejected"],
      "properties": {
        "target": { "type": "string", "enum": ["prompt", "tool", "grader", "configuration"] },
        "issue": { "type": "string", "minLength": 1 },
        "recurrence": { "type": "string", "minLength": 1 },
        "evidence": { "type": "array", "minItems": 1, "items": { "type": "string", "minLength": 1 } },
        "section": { "type": "string", "description": "exact heading line in the instruction file; required non-empty when target is prompt, carried but ignored by the apply step for any other target" },
        "change": { "type": "string", "minLength": 1, "description": "literal text to insert, not a description" },
        "rejected": { "type": "array", "items": { "type": "string" } }
      },
      "if": { "properties": { "target": { "const": "prompt" } } },
      "then": { "properties": { "section": { "minLength": 1 } } }
    },
    "comparison": {
      "type": "object",
      "required": ["verdict", "keep", "criteria", "runs", "revisions_needed", "improved", "regressed"],
      "properties": {
        "verdict": { "type": "string", "enum": ["success", "partial", "regression", "no effect"] },
        "keep": { "type": "boolean", "description": "false iff verdict is regression — the change is not kept (R21)" },
        "criteria": { "type": "object", "additionalProperties": { "type": "array", "minItems": 2, "maxItems": 2, "items": { "type": "integer" } } },
        "runs": { "type": "integer" },
        "revisions_needed": { "type": "array", "minItems": 2, "maxItems": 2, "items": { "type": "integer" } },
        "improved": { "type": "array", "items": { "type": "string" } },
        "regressed": { "type": "array", "items": { "type": "string" } }
      },
      "allOf": [
        { "if": { "properties": { "verdict": { "const": "regression" } } }, "then": { "properties": { "keep": { "const": false } } }, "else": { "properties": { "keep": { "const": true } } } }
      ]
    }
  }
}
```

The rubric is a text value supplied per run, one criterion per line in the form `- <name>: <threshold>`; criterion names are read from the rubric in order, and first-attempt failures are recorded by **position**, never by the grader's echoed name.

## 4. Business Rules

Each rule: behavior + the failure it prevents + provenance label + its acceptance criteria. "Course-demonstrated" rules trace to the materials via their CTX anchor; "project hardening" is this spec's own addition; `[environment]` is the lab's.

**Agent loop**

- **R1 — Fetch by identifier.** A run's opening message to the review agent names only a ticket key ("the requirement is tracked as ticket `<key>`; fetch it to begin"); the agent obtains the text by calling the fetch tool, and a fetch for an unknown key returns an error message, never raises. Prevents the agent being built around one document (CTX-A, CTX-C3). *Course-demonstrated.* → AC1, AC2
- **R2 — Retry transient tool errors with identical arguments.** When a tool returns an error — its result status is `error`, or its text begins with "error" ignoring case — the agent calls the same tool again with the same arguments until it succeeds; the trace records each failed attempt as its own tool row. The fetch tool's simulated outage is configurable and the offline fixture plants **two** failures (a 503-style message, then a timeout message) before success — the value the Lesson 4 narration states aloud; the course's helper default is 0 (a clean fetch) and its lesson text and pre-baked trace say two, a contradiction resolved by the lever-value rule's first branch (narration); it is a post-build lever (CTX-B1, CTX-C4). *Course-demonstrated.* → AC3
- **R3 — Six stages, one tool call per turn, in order.** The instruction file directs: fetch; write the file with the skeleton and only the Confirmed Facts section filled; then one edit each for Ambiguities, Clarification Questions, Assumptions, Summary; then one short completion sentence and no further tools. The order is *requested, not enforced*: a stage-order check reports `in_order` (the sections filled, in file order), `missing`, and `complete`; filling two sections in one edit is not a violation, filling one out of order or leaving one empty is (CTX-B2). *Course-demonstrated.* → AC4, AC5
- **R4 — Analysis file contract.** The file matches §3.1; the Summary is two or three sentences (a sentence ends at `.`, `!` or `?` followed by whitespace or the end of the section, and the summary check reports the count); counts cover the four list sections and never the Summary; "complete" is as §3.1 defines (CTX-A). *Course-demonstrated.* → AC5, AC6
- **R5 — Turn cap is a safety stop, not the normal stop.** The model-call cap is **12** for a run without a grader (the Lesson 4 notebook and helper constant: six stages plus headroom for retries and the closing message) and **40** for a run with a grader (the Lesson 5 notebook, the event demo and the batch runner: several verification passes cost more turns). Both are single-valued body defaults, not a contradiction. When the cap ends a run and the file is not complete, the trace's final action reports the cap ("Stops: turn limit of N reached"), never "Finishes the review" (CTX-B3). *Course-demonstrated.* → AC7
- **R6 — Instructions are a file, loaded every run, and their absence fails loudly.** The agent's standing instructions live at `/memories/AGENTS.md` inside the run workspace and are loaded into context at the start of every run; the system prompt only points at them. If the file is missing when the agent is built, the build raises before any model call — a missing memory file is otherwise ignored silently and the agent produces a plausible bad review (CTX-B5). The file must contain, as level-2 headings, `Procedure` and `Review guidance`, and under the latter the level-3 headings `Confirmed facts`, `Ambiguities`, `Clarification questions`, `Assumptions` — the learning loop targets these headings. *Course-demonstrated.* → AC8, AC9
- **R7 — The agent never edits its own instructions.** Writes under `/memories/**` are denied by a harness permission, not by instruction text alone; a write attempt returns a denial and the file is unchanged. Changes to the instructions are proposed and applied only from outside the agent (R17–R19) (CTX-B6). *Course-demonstrated.* → AC10
- **R8 — Workspace confinement.** The agent's file tools see the run workspace as `/`; a path above it is unreachable and a read of one returns an error, not the file (the course notes the repository holds a real `.env`) (CTX-A). *Course-demonstrated.* → AC11
- **R9 — Fresh workspace per run.** Every run gets a new workspace seeded with the instruction file under test (the baseline, or a batch's snapshot); two runs never see each other's analysis file. Event-triggered runs discard the workspace afterwards; batch runs keep each run's workspace beside its record. Prevents a stale analysis file being read and stages skipped (CTX-B7). *Course-demonstrated.* → AC12

**Verification loop** (in force when D2 = (a))

- **R10 — The grader judges the file, not the conversation.** Under D3 option (a) the grader is a separate model role given one tool, a file read; before any verdict it reads `/analysis.md`; for every criterion it passes it records a verbatim quote with its line number as `evidence`, and a criterion it cannot quote fails with a `gap`; criteria are applied literally — a line with a different label than the one named does not satisfy it, and coverage criteria check every item, never a sample; the grader is conservative and never edits the file. Under D3 option (b) the same verdict shape is produced by code (CTX-B4). *Course-demonstrated.* → AC13, AC14, AC15
- **R11 — Rubric, verdict and revision budget.** The rubric has three pass/fail criteria named in order `completeness` (every clause of the requirement is addressed somewhere), `clarity` (every Ambiguities bullet has an indented `Resolved by:` line naming the fact or decision that settles it) and `depth` (every Ambiguities bullet has an indented `Edge case:` line naming a concrete production failure). A pass is `satisfied` only when every criterion passes in that same pass; otherwise `needs_revision`, and the per-criterion gaps are injected into the agent's conversation as feedback for another attempt; a malformed or contradictory rubric yields `failed`. The grader may send work back at most **MAX_RUBRIC_ITERATIONS = 3** times — the Lesson 5 narration's value; the course set it to 3 in the notebook and the batch runner and to **2** in the event demo, a contradiction resolved by the lever-value rule's first branch (narration states 3); it is a post-build lever (§6 Ask First), never a gate question. When the budget is exhausted the run's status is `max_iterations_reached` even though the last pass says `needs_revision` (CTX-A, CTX-C2). *Course-demonstrated.* → AC14, AC16, AC17, AC18
- **R12 — Every run is recorded as §3.2.** One trace row per model turn and per tool result (turns count model messages that call tools plus the final answer), every grading pass with the file as that pass saw it (the grader's own tool calls are recorded on its grading pass, not in the agent trace), the instructions verbatim, the status and the counts; the record is viewable in the app. This is the local trace capture the course uses from Lesson 4 on (CTX-C11). *Course-demonstrated.* → AC19
- **R13 — A grader error is not a verdict.** If the grader stage raises, the pass is recorded with `result: grader_error` and no criteria, the run continues, and the run is *ungraded*: it is excluded from every pass-rate denominator and counted under `grader_errors` in the batch summary — never averaged away as a pass or a fail (CTX-B8). *Course-demonstrated.* → AC20, AC34

**Event-driven loop**

- **R14 — Events trigger the loop.** Three triggers run one analysis for a ticket: creating a ticket, saving a new version of a requirement page (which re-runs the loop for **every** ticket linked to that page whose status is not `Done`, and nothing when none is open), and a manual re-run on a ticket that is not `Done`. A `Done` ticket is never re-triggered. Each trigger calls the same single function a real tracker webhook would call, and the run record's `trigger` names which one fired (CTX-A, CTX-C5). *Course-demonstrated.* → AC12, AC24, AC25, AC26, AC27
- **R15 — The report is written next to the requirement, never into it.** A run's result is appended as a new version of an agent-owned report page (kind `analysis_report`, one per ticket, created on first use with id `page-analysis-<ticket key lower-cased>` and title "Analysis Report — <key>"), authored by the fixed bot author string, whose body opens with a banner naming the ticket, the requirement version analyzed and the verification status with the number of grading passes, followed by the analysis. The requirement page is the source of truth: the agent never writes to it, and the app rejects (HTTP 400) an edit to any page that is not a requirement page. Any two versions of any page can be compared as a unified diff; for a report page the comparison also shows the two runs' status and counts (CTX-C5). *Course-demonstrated.* → AC28, AC29, AC30
- **R16 — Ticket lifecycle; a human closes.** A new ticket is `Open`; a completed run sets it to `Analysis Ready`, records `last_analyzed_version` and `last_run_id`, and adds a bot comment naming the status, the requirement version and the report page; only a human action moves a ticket to `Done` — the agent never closes its own work. When a ticket has more than one run, the ticket page shows a "what changed since the previous run" table: requirement version, status, and the four section counts side by side, plus the run history (CTX-C5). *Course-demonstrated.* → AC27, AC31, AC32

**Learning loop**

- **R17 — The analyst proposes; a human approves; code applies; only the instruction file is auto-applied.** The analyst returns a typed change (§3.4) and writes a human-readable proposal file; nothing is applied until a human takes an explicit approve action in the app; applying inserts the change with plain string work, no model call; a change whose target is `tool`, `grader` or `configuration` is expressible but refused by the apply step with a message to read the proposal and decide. The course argues one side only — confidence in merging harness changes comes from human review plus a regression check — so this is baked in, not a row (CTX-C6). *Course-demonstrated.* → AC35, AC36
- **R18 — Analyst evidence discipline and read-only access.** The analyst is rooted at the batch history, may read anything there and write exactly one file, `/proposal.md` (every other write is denied); it starts from the batch summary's first-attempt pass rates to pick the criterion to investigate, reads individual runs for evidence and the batch's instruction snapshot so its addition fits the file and repeats nothing already there; evidence is quoted, not paraphrased; the `change` is literal insertable text with the exact label when a labelled line is needed; a problem appearing in a minority of runs is not a pattern and goes under `rejected`. **Recurrence threshold** (generator's reading of the course's "most runs" / "one run out of five is not a pattern"): a criterion is systemic when it fails first attempt in **more than half** of graded runs — a post-build lever (§6 Ask First). (CTX-B9, CTX-C6). *Course-demonstrated; threshold value is the generator's quantification.* → AC33, AC35, AC47
- **R19 — Applying a change.** The change text is inserted at the end of the section whose heading line the change names (the section ends at the next heading of the same or shallower depth; trailing blank lines of the section are trimmed; one blank line precedes and follows the inserted text; the file ends with a newline); a heading not found is an error and nothing is written. The applied file becomes the new baseline for subsequent runs and is snapshotted into the next batch (CTX-C6). *Course-demonstrated.* → AC36, AC37
- **R20 — A batch is one run per document under one instruction version.** A batch has a label; it snapshots the instruction file under test into its directory, runs every document in sorted filename order with a fresh workspace each (R9), the grader on (budget per R11), a cap of 40, and no simulated fetch failures (the retry demonstration belongs to the agent-loop lesson; here it only adds turns); each run is written as its own JSON record with every message untruncated, and the batch writes a summary (§3.4) whose denominators are graded runs only and whose `revisions_needed` counts graded runs with any first-attempt failure (CTX-A). *Course-demonstrated.* → AC33, AC34, AC46, AC47
- **R21 — Compare two batches.** Per criterion, first-attempt passes before vs after; verdict `regression` if any criterion's passes fell, else `success` if the after batch needed zero revisions, else `partial` if any criterion rose, else `no effect`; `improved` and `regressed` list the criteria that moved. A regression means the change is not kept: the comparison carries `keep: false` (every other verdict `keep: true`), and on a `regression` the Learning page offers a **Revert** action that restores the before batch's instruction snapshot as the baseline — a human action like approval (R17), never automatic; no other verdict offers it (CTX-C6). *Course-demonstrated; the revert action is project hardening.* → AC40, AC46, AC50

**Environment and hardening**

- **R22 — LLM access and model roles** `[environment]`. The app reads exactly `OPENAI_API_KEY` and `OPENAI_BASE_URL` (the course's provider through the platform proxy) and the three model-role variables of §2; it never reads `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL` (present in the container, unread), never hardcodes a key or model id, never probes a model-listing endpoint, and never asks the person for a key. Every model filling a role must support native tool calling, and the analyst's model must additionally return a structured (typed) final response — the §3.4 harness change — because the apply step reads fields, not prose. **Model tiering lever** (the course's argument, carried from the constrained model/provider dimension): match model capability to each role's task — the course ran the review agent and grader on its cheaper model and the analyst on its stronger one "because reading five full run traces and finding what recurs is the one job the cheaper model does unreliably", and notes a different grader model is "a common production choice"; which platform model fills each role is set at gate time through the "(Recommended)" flag and changed only through §6 Ask First. *Environment-imposed (the lever's argument is course-demonstrated, CTX-C7).* → AC38, AC39, AC48
- **R23 — One server, port 4000** `[environment]`. One process serves the three surfaces and their API on port 4000 bound to `0.0.0.0`; nothing else is previewable; HTTP only (no WebSocket upgrades); long-running analyses complete within one HTTP request or are polled over plain HTTP. *Environment-imposed.* → AC42
- **R24 — Every URL inside a page is relative** `[environment]`. Links, form actions, fetch calls and asset references use relative paths (`api/tickets`, never `/api/tickets`), because the preview is reverse-proxied under a path prefix and a root-absolute path resolves against the IDE. *Environment-imposed.* → AC43
- **R25 — Records survive a restart.** Pages with all versions, tickets with status and comments, runs with grading passes, and batches with their summaries are persisted on local disk as they are written and are intact after the server process is stopped and started again; a fresh start with no data seeds the §5 starting scenario exactly once (CTX-C10). *Course-demonstrated (flat JSON store, seeded on first start), reinforced `[environment]` (only the workspace disk persists between lab sessions, so any record held in process memory is lost at every restart).* → AC41, AC23
- **R26 — Offline acceptance suite on the scripted model.** The suite runs the real pipeline against the scripted stand-in (RR1) with no network and no key; fixtures are never modified to make a test pass; criteria tagged `live` are skipped offline and run only when the keys are present. *Project hardening.* → AC44
- **R27 — Edit tool rejects a non-unique anchor.** The file edit tool replaces exactly one occurrence of its anchor string; an anchor that occurs more than once (or not at all) returns an error and leaves the file unchanged, and the agent recovers by reading the file and retrying — the course saw duplicate headings and edit errors in some runs and the analyst correctly rejected them as non-patterns (CTX-B10). *Course-demonstrated.* → AC21, AC22
- **R28 — No scripted or hosted dependency is mislabelled.** The scripted model's registered name and description say it is a fake stand-in; the simulated tracker and wiki say so in their page titles. *Project hardening.* → AC45
- **R29 — Build-workspace and interpreter discipline** `[environment]`. Three lab pitfalls, one rule: (i) the review agent's baseline instruction file lives under the app's data directory and no source file reads or writes the build-root `AGENTS.md`, which the lab's IDE rewrites at every boot; (ii) `python3 --version` runs before any install and is recorded in `resolved-decisions.md`, and a course pin the interpreter refuses stops the build with a report naming the pin and the recorded version — never a silently substituted version; (iii) inside the venv the course pins win over the preinstalled copies (`openai` 3.6.0, `python-dotenv` 1.2.3), verified by the installed version, not assumed. *Environment-imposed.* → AC49

## 5. Acceptance Criteria

### 5.1 Fixture corpus (declared before any criterion uses it)

All fixtures live under `fixtures/` in the build folder; every filename is an importable identifier where it is a module. The facts below are the authoritative content — the builder writes the files to match them, and the suite never modifies them (R26). No text here is copied from the course; the course's own documents and ids are provenance only (CTX-C name-map).

**Requirement documents** — `fixtures/requirements/`. Each file's first line is `REQUIREMENT: <title>`; every following non-empty line is one clause. A clause is *vague* when it contains one of exactly these words, whole-word, case-insensitive: `securely`, `common`, `reasonable`, `appropriately`, `quickly`, `sensible`, `easily`. The scripted review role (below) keys its output on clauses and vague words, so these counts are what the criteria assert.

| File | Title | Clauses (in order) | Vague clauses |
|---|---|---|---|
| `UPL-310.md` (the seed scenario's requirement; also the default ticket) | Profile Avatar Upload | 1 "Users shall be able to upload an avatar image to their profile." · 2 "Uploaded images must be stored securely." · 3 "The feature should accept all common image formats." | 2 (clauses 2, 3) |
| `01_session_timeout.md` | Session Timeout | "Sessions shall expire after a reasonable period of inactivity." · "Users must be warned before expiry." · "Expired sessions should be handled appropriately." · "The system shall log every expiry." | 2 |
| `02_export_reports.md` | Report Export | "Users shall be able to export reports." · "Exports must complete quickly." · "Exported files should use common formats." · "The system shall record each export." | 2 |
| `03_rate_limiting.md` | API Rate Limiting | "The API shall limit request rates per client." · "Limits must be sensible for normal usage." · "Clients exceeding limits should be notified appropriately." · "The system shall record rejected requests." | 2 |
| `04_audit_logging.md` | Audit Logging | "The system shall log privileged actions." · "Logs must be retained for a reasonable period." · "Logs should be searchable easily." · "Log access shall itself be logged." | 2 |
| `05_search_relevance.md` | Search | "Search shall return matching items." · "Results must load quickly." · "Common misspellings should be tolerated." · "The system shall record search queries." | 2 |

**Fake tracker seed** — `fixtures/tickets.json`: a map from ticket key to the document text above: `UPL-310`, `SESS-101` (01), `EXP-202` (02), `RATE-303` (03), `AUD-404` (04), `SRCH-505` (05). The fetch tool resolves a key against this map at call time (R1); the batch runner seeds each document under the default key `UPL-310` before each run, exactly as the course's runner does, so the opening message is identical for every run. An event run (ticket created, page saved, manual re-run — R14) does the same: immediately before the run it seeds the linked requirement page's *current* body (its latest version, rendered as `REQUIREMENT: <title>` plus one clause per line) under `UPL-310`, so its opening message names `UPL-310` and the fetch returns the page as it stands at trigger time — three clauses for the seed page, four after AC25's save, which is what AC25 and AC32 see.

**Starting scenario** (seeded on first start, R25): one requirement page `page-req-avatar-upload`, title "Profile Avatar Upload — Requirements", version 1 authored by "Avery (Product Manager)", body = the three clauses of `UPL-310.md`; one ticket `REV-100`, title "Review requirements: Profile Avatar Upload", status `Open`, assignee "Blake (Eng Lead)", linked to that page, no comments, no runs; zero report pages; zero batches. The fixed cast of people: "Avery (Product Manager)", "Blake (Eng Lead)", "Casey (QA Lead)", "Devon (Backend Engineer)", "Emery (Frontend Engineer)". Bot author string: `Review Agent (bot)`. New ticket keys are `REV-<n>` with n = highest existing + 1, starting at 100.

**Instruction files** — `fixtures/instructions_v1.md` is the review agent's baseline instruction file. Facts: it contains level-2 headings `Procedure` and `Review guidance`, and under the latter level-3 headings `Confirmed facts`, `Ambiguities`, `Clarification questions`, `Assumptions`; its Procedure names the fetch tool `fetch_requirement` and the six stages of R3 with the five-section skeleton and the ambiguity bullet shape (bold quoted clause, indented `Reason:` line), the retry-with-identical-arguments rule, "never modify the requirement; never edit this file", and the closing one-sentence completion; its Review guidance says facts are only what the document states (no inference), ambiguities quote the exact clause and give the reason, questions are what a reviewer needs answered before work starts, assumptions are what a developer would assume if nobody answered. **It contains neither the string `Resolved by:` nor `Edge case:`.** `fixtures/instructions_v2.md` is byte-identical to v1 except that the **v2 insertion text** is inserted at the end of the `### Ambiguities` section (one blank line before, one after). The v2 insertion text is exactly five lines, in order: (1) `Under every ambiguity bullet, add two more indented labelled lines after the Reason line:`; (2) a line of three backticks; (3) `  Resolved by: the fact or decision that would settle it` (two leading spaces); (4) `  Edge case: a concrete production failure if it stays unresolved` (two leading spaces); (5) a line of three backticks. `fixtures/changes/change_prompt.json` is a §3.4 harness change with `target: "prompt"`, `section: "### Ambiguities"` and `change` equal to that inserted text; `change_tool.json`, `change_grader.json`, `change_config.json` are the same object with target `tool`, `grader`, `configuration`; `change_missing_section.json` has target `prompt` and `section: "### Nonexistent"`.

**Rubrics** — `fixtures/rubric.txt`: three lines in R11's order and wording (`- completeness: …`, `- clarity: …`, `- depth: …`). `fixtures/rubric_malformed.txt`: two lines both named `clarity`, one demanding an indented `Resolved by:` line under every ambiguity and one forbidding any such line.

**Analysis samples** — `fixtures/analysis_samples/`: `complete_v1.md` — a full §3.1 file for `UPL-310` with 3 facts, 2 ambiguity bullets each with only a `Reason:` line, 2 questions, 2 assumptions, a two-sentence summary (31 words); `missing_assumptions.md` — same but the Assumptions section is empty; `wrong_label.md` — same as `complete_v1.md` but each ambiguity bullet carries an indented `Resolved: …` line (label without "by") and an indented `Edge case: …` line; `complete_v2.md` — same as `complete_v1.md` with indented `Resolved by:` and `Edge case:` lines under both bullets; `duplicate_heading.md` — a file in which the line `## Notes` occurs exactly twice and the line `## Never` not at all.

**Batch summaries for the comparison** — `fixtures/summaries/`: five §3.4 summaries over 5 runs, 5 graded, 0 grader errors, documents 01–05: `before.json` completeness 5 / clarity 0 / depth 0, revisions 5; `after_success.json` 5/5/5, revisions 0; `after_partial.json` 5/3/0, revisions 5 (every run failed depth first time); `after_regression.json` 4/5/5, revisions 1 (the one run that failed completeness); `after_noeffect.json` 5/0/0, revisions 5. Each `revisions_needed` is the count R20 computes from its own first-attempt numbers.

**The scripted model** — `fixtures/scripted_model.py` (RR1): a fake standing in for the live model, registered under the name `scripted-stand-in` with the description "scripted stand-in for the live model — a fake that returns declared responses". It is selected when `SCRIPTED_MODEL=1`; it never opens a socket. It picks its role from the system prompt it receives and its variant from `SCRIPTED_VARIANT` (unset = default). Declared behavior:

- *Role `review`* (system prompt points at `/memories/AGENTS.md`). Turn 1: call `fetch_requirement` with the key named in the opening message. Turn 2: `write_file` `/analysis.md` with the skeleton and Confirmed Facts = one bullet per clause (the clause text). Turns 3–6: one `edit_file` each filling Ambiguities (one bullet per vague clause: the clause in bold quotes, then an indented `Reason: the word "<vague word>" is not defined`), Clarification Questions (one per vague clause: `What does "<vague word>" mean for clause <n>?`), Assumptions (one per vague clause: `Assume the narrowest reading of "<vague word>" until confirmed.`), Summary (exactly two sentences: "The document states <facts> facts and leaves <k> clauses under-specified. Clarification is needed before implementation."). Turn 7: the completion sentence "Review complete.", no tool call. **If the instruction text in its context contains `Resolved by:`** (the v2 file), every ambiguity bullet also carries indented `Resolved by: a definition of "<vague word>" for clause <n>` and `Edge case: an unhandled "<vague word>" case in production for clause <n>` lines from the first attempt. **When grader feedback has been injected**, it makes one `edit_file` replacing the Ambiguities section with the full bullets (both lines), then the completion sentence. When a tool result is an error (R2's test), it repeats the same call with the same arguments. For the document whose title is `API Rate Limiting`, its first Ambiguities edit uses the anchor `## ` (non-unique) and, on the error, it calls `read_file /analysis.md` and retries with the correct anchor. Variants: `loop_forever` — every turn calls `fetch_requirement` again; `self_edit` — turn 2 first attempts `write_file /memories/AGENTS.md` with the text "hacked", then continues normally; `escape` — turn 2 first attempts `read_file ../fixtures/tickets.json`, then continues normally; `never_fixes` — after feedback, emits the completion sentence with no edit.
- *Role `grader`* (the grader system prompt). First call: `read_file /analysis.md`. Then, per rubric line in order: `completeness` passes when the Confirmed Facts bullet count is at least the requirement's clause count; `clarity` passes when every Ambiguities bullet has an indented line starting exactly `Resolved by:`; `depth` likewise for `Edge case:`. A passing criterion carries `evidence` = `L<line>: <that line verbatim>` (the first qualifying line); a failing one carries `gap` = `missing indented '<label>' line under ambiguity bullet <k>`. Result `satisfied` iff all pass, else `needs_revision` with `explanation` listing the failed names. If two rubric lines share a name, result `failed` with no criteria passed. Variant `grader_error_doc02` — raises an exception on the document titled `Report Export`.
- *Role `analyst`* (the analyst system prompt). Calls, in order: `read_file /<label>/summary.json`, `read_file /<label>/AGENTS.md`, `ls /<label>`, `read_file` on every `run_*.json`; then `write_file /proposal.md` with headings `## Summary signal`, `## Evidence across runs`, `## Proposed insertion`, `## Rejected observations`; returns a §3.4 change with target `prompt`, section `### Ambiguities`, change = the v2 insertion text, evidence = the first `gap` of each run that failed first attempt (quoted), recurrence = "<n>/<graded> runs", rejected = one entry naming the single run with an edit-tool error. Before the proposal write it attempts `write_file /<label>/summary.json` with the text "tamper" and expects a denial (R18's test).

### 5.2 Criteria

Offline unless tagged `live`. "Default run" = create ticket `REV-101` linked to the seed page through the app with `SCRIPTED_MODEL=1`, default variant, grader on, budget 3, cap 40, simulated fetch failures 0. "Direct run on `<key>`" = the one-analysis function every trigger calls (R14), invoked directly with that fetch key and no ticket, under the same settings unless the Given says otherwise.

| AC | Given | When | Then | Rules |
|---|---|---|---|---|
| AC1 | the default run | the first trace rows are inspected | row 1 is actor `Model reasoning`, action names `fetch_requirement` with argument `UPL-310`… (the key seeded for the ticket's page); the run's opening message contains the key and none of the page's three clauses | (R1) |
| AC2 | the fetch tool and key `NOPE-1` | the tool is called directly | it returns a string beginning `Error fetching ticket` naming `NOPE-1`; no exception | (R1) |
| AC3 | the default run with simulated fetch failures = 2 | the trace is inspected | the first six rows alternate Model/Tool; tool rows 2 and 4 are errors (a 503-style text, then a timeout text), row 6 is the document; all three fetch calls carry identical arguments; the run still ends `satisfied` | (R2) |
| AC4 | the default run | the stage-order check runs over the first attempt | `in_order` true, `missing` empty, `complete` true, order = Confirmed Facts, Ambiguities, Clarification Questions, Assumptions, Summary | (R3) |
| AC5 | `analysis_samples/missing_assumptions.md` | the stage-order check and completeness run over it | `missing` = `["Assumptions"]`, `complete` false; `complete_v1.md` is complete | (R3, R4) |
| AC6 | `analysis_samples/complete_v1.md` | counts and summary words are computed | counts = Confirmed Facts 3, Ambiguities 2, Clarification Questions 2, Assumptions 2; summary words 31 and summary sentences 2; the counts object has no `Summary` key | (R4) |
| AC7 | variant `loop_forever`, grader off, cap 12 | a direct run on `UPL-310` | the run stops after exactly 12 model turns; the last trace action is `Stops: turn limit of 12 reached`; the analysis file is not complete | (R5) |
| AC8 | a workspace with no `/memories/AGENTS.md` | the agent is built | building raises an error naming the missing path; the scripted model's call counter is 0 | (R6) |
| AC9 | a fresh checkout | the baseline instruction file is read | it is byte-identical to `fixtures/instructions_v1.md`, contains the six required headings, and contains neither `Resolved by:` nor `Edge case:` | (R6) |
| AC10 | variant `self_edit` | the default run | the trace contains a `write_file` tool row whose result is a denial mentioning `/memories/AGENTS.md`; the workspace's instruction file is unchanged; the run still ends `satisfied` | (R7) |
| AC11 | variant `escape` | the default run | the `read_file ../fixtures/tickets.json` tool row's result is an error and contains none of the ticket keys; the run still ends `satisfied` | (R8) |
| AC12 | the default run followed by `POST api/tickets/REV-101/rerun` | the second run's record is inspected | its `trigger` is `manual_rerun`; its first file tool call is `write_file` (no prior `read_file` of an existing analysis); the two run records' `workspace` values differ; after batch `v1` (AC33) directories `ws_01`…`ws_05` exist inside the batch directory, each holding an `analysis.md` | (R9, R14) |
| AC13 | the default run | grading pass 1 is inspected | the grader's first tool call, recorded on the pass, is `read_file /analysis.md`, before the verdict; the `completeness` criterion (passed) carries `evidence` matching `^L\d+: ` | (R10) |
| AC14 | the default run (instructions v1) | the run completes | grading has 2 passes: pass 1 `needs_revision` with completeness passed, clarity failed (`gap` names `Resolved by:`), depth failed (`gap` names `Edge case:`); pass 2 `satisfied` with all three passed; run status `satisfied`; the final file's two ambiguity bullets each carry both labelled lines | (R10, R11) |
| AC15 | a workspace containing `analysis_samples/wrong_label.md` as `/analysis.md` and the requirement `UPL-310` | the grader stage is invoked directly with `rubric.txt` | result `needs_revision`; clarity failed with a gap naming `Resolved by:`; depth passed | (R10) |
| AC16 | the default run with `rubric_malformed.txt` | the run completes | grading pass 1 result `failed`; run status `failed` | (R11) |
| AC17 | variant `never_fixes`, budget 3 | the default run | 4 grading passes, every result `needs_revision`; run status `max_iterations_reached`; the ticket's run record and bot comment carry that status | (R11) |
| AC18 | the default run with budget 0 (D2 option b) | the run completes | grading is empty, status `ungraded`, the file is complete, turns = 7 | (R11) |
| AC19 | the default run | the run record is validated | it satisfies §3.2; `turns` = 9; `trace` has 16 rows whose actors in order are `Model reasoning`, `Tool` six times over (rows 1–12: the fetch, the write, the four edits), then `Model reasoning` (row 13, the first completion sentence), then `Model reasoning`, `Tool` (rows 14–15, the post-feedback edit), then `Model reasoning` (row 16, the second completion sentence); `id` matches `^[0-9a-f]{8}$`; no trace `detail` exceeds 221 characters, and the trace recorder given a tool result of the letter `x` repeated 300 times produces a `detail` of exactly 221 characters ending with `…`; the record is returned by `GET api/runs/<id>` and rendered on the ticket page | (R12) |
| AC20 | variant `grader_error_doc02` | batch `v1err` over the five batch documents | run 02's grading = one pass with `result: grader_error` and empty criteria, status `grader_error`; summary: runs 5, graded 4, grader_errors 1, every criterion's `total` 4, completeness passed 4, clarity 0, depth 0, revisions_needed 4 | (R13) |
| AC21 | a workspace whose `/analysis.md` is `analysis_samples/duplicate_heading.md` | the edit tool is called with anchor `## Notes` | it returns an error naming a non-unique anchor; the file is byte-identical afterwards; an anchor that occurs zero times also errors | (R27) |
| AC22 | batch `v1` | run 03's trace | contains an `edit_file` tool row whose result is an error, followed by a `read_file /analysis.md` row and a successful `edit_file`; run 03 still ends `satisfied` with 4/2/2/2 counts | (R27) |
| AC23 | an empty data directory | the server starts | the pages, tickets, runs and batches stores exist as declared; pages = exactly the seed page, `kind` = `requirement`, `linked_ticket` null, with one version by "Avery (Product Manager)"; tickets = exactly `REV-100` (`Open`, assignee "Blake (Eng Lead)", `last_run_id` null); runs and batches empty; starting the server again does not duplicate the seed | (R25) |
| AC24 | the seed scenario | `POST api/tickets` with title, description, `linked_page_id` = seed page, assignee "Casey (QA Lead)" | the ticket `REV-101` is created `Open`, a run with trigger `ticket_created` completes, the ticket is `Analysis Ready` with `last_analyzed_version` 1 and `last_run_id` set, and report page `page-analysis-rev-101` exists with version 1 | (R14) |
| AC25 | after AC24 | `POST api/pages/page-req-avatar-upload/save` with a body adding a fourth clause "Avatars must be smaller than 2 MB." by "Avery (Product Manager)" | the page has version 2; a run with trigger `page_saved` completes for each of the two open tickets linked to the page, `REV-101` and the seed ticket `REV-100`; `REV-101`'s `last_analyzed_version` = 2 and `page-analysis-rev-101` has version 2 whose banner names requirement version 2; `REV-100` becomes `Analysis Ready` and `page-analysis-rev-100` has version 1; the response message names both `REV-101` and `REV-100` as re-triggered | (R14) |
| AC26 | after AC25, `REV-101` and `REV-100` both marked Done (each by `POST api/tickets/<key>/close`) | the page is saved again | the page has version 3; no new run is recorded; the response message says nothing was re-triggered | (R14) |
| AC27 | `REV-101` is `Done` | `POST api/tickets/REV-101/rerun` | HTTP 409, no run recorded; the ticket page shows no re-run or Mark Done control | (R14, R16) |
| AC28 | after AC24 | the report page is read | `kind` = `analysis_report`, `linked_ticket` = `REV-101`, title `Analysis Report — REV-101`, every version's author = `Review Agent (bot)`; version 1's body starts with three banner lines naming `REV-101`, "version 1", and `satisfied` "after 2 grading pass(es)", followed by a §3.1 file | (R15) |
| AC29 | after AC24 | `POST api/pages/page-analysis-rev-101/save` | HTTP 400; the report page's versions are unchanged; the requirement page's body is byte-identical to the seed body | (R15) |
| AC30 | after AC25 | `GET api/pages/page-analysis-rev-101/compare?a=1&b=2` | a unified diff with `fromfile` "version 1" and `tofile` "version 2" containing at least one `+` line mentioning "2 MB"; the response carries both runs' status and counts | (R15) |
| AC31 | after AC24 | the ticket's comments and status are read; then `POST api/tickets/REV-101/close` | one bot comment by `Review Agent (bot)` containing `Analysis complete (satisfied)`, `requirement version 1` and `Analysis Report — REV-101`; the status becomes `Done` only after the close call; no run ever sets `Done` | (R16) |
| AC32 | after AC25 | the ticket page is rendered | a "what changed since the previous run" table shows requirement version 1 vs 2, status `satisfied` vs `satisfied`, and Confirmed Facts 3 vs 4; the run history lists two runs | (R16) |
| AC33 | instructions v1 as baseline | batch `v1` is run from the Learning page over the five batch documents, then the analyst runs on it | `v1/AGENTS.md` is byte-identical to `instructions_v1.md`; five run files `run_01_01_session_timeout.json`…`run_05_05_search_relevance.json` each with trigger `batch`, label `v1` and 2 grading passes; `v1/summary.json` = completeness 5/5, clarity 0/5, depth 0/5, revisions_needed 5, documents in order; the analyst's trace shows `read_file /v1/summary.json` first, then `/v1/AGENTS.md`, then at least one run file; its attempted write to `/v1/summary.json` is denied and that file is unchanged; `/proposal.md` exists with the four headings; the returned change validates against §3.4 with target `prompt`, section `### Ambiguities`, a `change` containing both `Resolved by:` and `Edge case:`, five evidence quotes, and one `rejected` entry naming run 03's edit error | (R18, R20) |
| AC34 | batch `v1err` (AC20) | `summary.json` is validated | it satisfies §3.4 and `pass_rate` for each criterion is `passed/4` rounded to 3 places | (R13, R20) |
| AC35 | the AC33 proposal is shown on the Learning page | before and after the person clicks **Approve and apply** | before: the baseline instruction file is unchanged and the page shows the proposal with its evidence and rejected list; after: the baseline equals `instructions_v2.md` and the page shows a v1→v2 diff | (R17, R18) |
| AC36 | `change_tool.json`, `change_grader.json`, `change_config.json` | each is submitted to the apply step | each is refused with a message containing "read the proposal"; the baseline is unchanged after all three | (R17, R19) |
| AC37 | `instructions_v1.md` and `change_prompt.json` | the apply function runs | the output is byte-identical to `instructions_v2.md`; with `change_missing_section.json` it raises naming `### Nonexistent` and writes nothing | (R19) |
| AC38 | the app's source files — every file under the server package `app/`, excluding `tests/` and `fixtures/` — and the test process setting `ANTHROPIC_API_KEY=CANARY` and `ANTHROPIC_BASE_URL=CANARY` before the app loads its configuration | the source is scanned and the app's resolved configuration is read | no scanned file contains the string `ANTHROPIC_`, a literal key or a literal model id; the resolved configuration contains no value `CANARY` and no key beginning `ANTHROPIC_`; the model-role variables are read from the environment; with `OPENAI_API_KEY` unset and `SCRIPTED_MODEL` unset, starting a run returns an error naming `OPENAI_API_KEY` and never prompts | (R22) |
| AC39 `live` | the container's `OPENAI_API_KEY`/`OPENAI_BASE_URL` and the three model-role variables set to platform models | the default run executes without the scripted model | a run record valid per §3.2 with status `satisfied` or `max_iterations_reached`, at least one grading pass with three criteria, and a report page version written | (R22) |
| AC40 | `summaries/before.json` and each `after_*.json` | compare runs | `after_success` → `success`, improved = [clarity, depth]; `after_partial` → `partial`, improved = [clarity]; `after_regression` → `regression`, regressed = [completeness], `keep` false; `after_noeffect` → `no effect`, improved and regressed empty; `keep` is true for the other three; each result's `revisions_needed` = [5, <the after file's value>] | (R21) |
| AC41 | after AC25 and AC33 | the server process is stopped and started again | `REV-101` and `REV-100` with status and comments, the seed page with 2 versions, `page-analysis-rev-101` with 2 versions, `page-analysis-rev-100` with 1, all three event runs, and batch `v1` with its summary are all present and identical; no reseed occurred | (R25) |
| AC42 | the server started | `GET` of the index and `GET api/tickets` | the socket is bound to `0.0.0.0:4000`; both return 200; the second returns JSON listing `REV-100` | (R23) |
| AC43 | every HTML page and script the server serves | all `href`, `src`, `action` and fetch/XHR URL literals are collected | none begins with `/` and none carries a scheme or host of its own; every API route is reachable through the index page's own links | (R24) |
| AC44 | network disabled and all key variables unset | `pytest` runs the offline suite | every non-`live` criterion passes; `live` criteria are reported skipped; a hash of `fixtures/` taken before the run equals the hash after | (R26) |
| AC45 | the registered scripted model and the surface page titles | inspected | the model's name is `scripted-stand-in` and its description contains "stand-in" and "fake"; the Tracker and Wiki index titles contain "simulated" | (R28) |
| AC46 | the applied baseline (`instructions_v2.md`) | batch `v2` runs and is compared with `v1` | `v2/summary.json` = 5/5, 5/5, 5/5, revisions 0; every run has one grading pass, `satisfied`; compare(v1, v2) verdict `success`; the Learning page shows the before/after per-criterion counts and the verdict | (R20, R21) |
| AC47 | batch `v1` | the Learning page's recurring-gaps view | gaps are grouped by criterion position: clarity 5 entries, depth 5, completeness 0, each entry naming its document | (R18, R20) |
| AC48 `live` | the container's keys and the three model-role variables set to platform models; batch `live1` run over the five batch documents without the scripted model (only a `live` criterion can exercise a real model's typed response; AC33 covers the scripted path) | the analyst runs on `live1` | every run's trace contains at least one `Tool` row (native tool calling); the analyst's returned change validates against §3.4 (`target` one of the four enum values, `evidence` non-empty) and `/proposal.md` exists in the analyst's workspace | (R22) |
| AC49 | the completed build, inside its venv | `resolved-decisions.md`, the installed packages and the source are inspected | the file records the `python3 --version` output; the installed `openai` reports 3.6.0 and `python-dotenv` 1.2.3 (the course pins, not the preinstalled copies); the baseline instruction file's path is under the app's data directory; no file under `app/` contains the string `AGENTS.md` as a path at the build root | (R29) |
| AC50 | after AC46 (baseline = `instructions_v2.md`, compare(v1, v2) = `success`) | the Learning page's comparison view is read, then the revert function is invoked directly with before batch `v1` | the view shows no Revert control; after the call the baseline is byte-identical to `v1/AGENTS.md` (= `instructions_v1.md`); `keep` on compare(v1, v2) is true | (R21) |

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the offline suite with the scripted model before claiming any criterion passes; cite the test output.
- Record the Python version, every install and its wall-clock cost, and every resolved decision in `resolved-decisions.md` — the workspace is the record `[environment]`.
- Keep the review agent's instruction file inside the run workspace's `memories/` folder (the app's own convention), never at the workspace root.
- Seed the fake tracker and the starting scenario from the fixtures exactly as declared.

**Ask First** (derived from the course's spoken trade-offs — each cross-referenced; changing any of these silently alters a behavior guarantee or forces re-running batches)
- Changing the revision budget (R11; the course's 3 vs 2) — changes how many send-backs a run may take and invalidates comparison across batches run with different budgets.
- Changing the turn caps (R5; 12 / 40) — a lower cap turns finishing runs into cap stops.
- Changing the recurrence threshold (R18; "more than half of graded runs") — changes which observations become proposals and which are rejected.
- Changing which platform model fills a role, or running the grader on a different model than the agent (R22 lever; CTX-C7) — the course's cost-vs-capability argument; every batch must then be re-run before a comparison means anything.
- Moving from the model-as-judge grader to a deterministic one or back after builds exist (Ledger D3) — changes what "pass" can mean.
- Turning the grader off (Ledger D2 option b) once batches exist — removes the learning loop's signal.
- Moving review guidance into skills (Ledger D1 option b) after a proposal has been applied — changes where the learning loop's proposal must target.
- Restoring §1 item 7 (cost accounting) or adding any trigger kind the course did not build.
- Running anything `live` while a batch is in progress, or deleting a batch directory.

**Never**
- Author or edit the workspace-root `AGENTS.md` — the IDE rewrites it at every boot and whatever is placed there is silently lost `[environment]`.
- Ask the person for an API key, hardcode one, read the `ANTHROPIC_*` pair, or guess at other variable names `[environment]`.
- Use a root-absolute URL in any page, bind to a port other than 4000, or start a second server `[environment]`.
- Invent evidence: a grader pass without a quoted line, an analyst proposal without run quotes, or a test result without output.
- Let the agent write to its own instructions, to the requirement page, or to any trace it is analyzing.
- Mutate fixtures to make a test pass; commit secrets; report "should pass" or "looks correct" as a result.
- Mark a ticket Done from automation, or apply a harness change without the explicit approve action.

## 7. Test Plan & Self-Verification

Create the venv and install the course pins in one early step, announcing the cost first:

```bash
python3 --version
python3 -m venv .venv --system-site-packages && source .venv/bin/activate
pip install "deepagents==0.7.11" "langchain==1.3.18" "langchain-core==1.6.1" "langgraph==1.2.11" \
            "langchain-openai==1.6.0" "openai==3.6.0" "pydantic==2.13.5" "python-dotenv==1.2.3" \
            "flask>=3.1.3" pytest
```

Run the offline suite with no keys and the scripted model, then the live criteria only when the container's keys are present:

```bash
env -u OPENAI_API_KEY -u OPENAI_BASE_URL -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL \
    SCRIPTED_MODEL=1 pytest -q -m "not live" tests/     # all four key variables unset (AC44); AC38's test sets its own canary in-process
pytest -q -m live tests/          # only with the platform keys and the three model-role variables set
```

Start the app for the preview pane (background process):

```bash
SCRIPTED_MODEL=1 python -m app --host 0.0.0.0 --port 4000
```

(the live app is the same command without `SCRIPTED_MODEL`, using the platform keys and the model-role variables from `resolved-decisions.md`).

**Reporting duty.** The build agent MUST report results per acceptance criterion, AC1 through AC50, each with cited evidence: the test name and its pass/skip/fail output line, and the file paths it exercised. A criterion reported as "should pass", "looks correct" or "not run" is a failure. The report is written to `acceptance-report.md` in the build folder as well as printed, because the workspace is the record.

## Runtime (lab)

Everything in this section is `[environment]` — contributed by the coding-agent-lab environment, not by the course.

**Container.** Debian, non-root user, Node 22, Python 3 with venv, sqlite3, git, build tooling. Preinstalled Python: `fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`; Node: `express`, `cors`, `better-sqlite3`, `vite`, `nodemon`. Nothing else is preinstalled. Outbound network works; every install costs the learner wall-clock time inside the session, so §7 batches the course pins into one announced step. Venvs are created with `--system-site-packages`; where the course pinned a version and a preinstalled copy differs (`openai`, `python-dotenv`), the course pin wins inside the venv. The Python minor version tracks the image: the build agent runs `python3 --version`, records it, and stops with a report if a course-pinned package refuses the interpreter. Memory is finite and shared with the agent's own process — this pipeline holds no local model resident (every model role is a remote call through the proxy), so no release-before-load rule is needed; say so in the report if that ever changes.

**Models.** The container exports `OPENAI_API_KEY`/`OPENAI_BASE_URL` and `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`, each base URL pointing at the platform proxy. The app reads the first pair only (R22). The platform's model set is not enumerated here because it changes; the three model-role variables are set when `resolved-decisions.md` is written, on the "(Recommended)" line, and are never probed from a listing endpoint.

**Preview.** One server, port 4000, bound to `0.0.0.0`, serving both pages and API; HTTP only (no WebSocket upgrades; streaming responses work); every in-page URL relative (R23, R24).

**Workspace.** The workspace is the record: a new chat starts with no memory of an earlier one and the grader sees only what is on disk, which is why `resolved-decisions.md` and `acceptance-report.md` are written, not just printed. The workspace-root `AGENTS.md` is never authored — the IDE rewrites that file at every boot. The course's own `AGENTS.md` convention (the review agent's instruction file) lives inside each run's `memories/` folder under the app, which is unaffected. Every tool call is visible to the learner; long-running servers run in the background.

**Environment failure modes** (written like a failure catalog entry; never part of CTX-B, which is the course's):
- *Root-absolute URL under the proxied preview.* Symptom: the index loads but every link, form or API call 404s or lands on the IDE. Cause: a `/api/...` path resolves against the proxy root, not the app. Fix: relative paths everywhere. Enforced by R24, AC43.
- *Second port or second server.* Symptom: the app runs but the preview pane shows nothing. Cause: only port 4000 on one process is previewable. Fix: one server serving pages and API. Enforced by R23, AC42.
- *Guidance lost at boot.* Symptom: instructions placed in the workspace-root `AGENTS.md` vanish on the next session. Cause: the IDE rewrites that file. Fix: §6 Never; the review agent's own instruction file lives under the app. Enforced by R29 (i), AC49.
- *Pin refused by the image's interpreter.* Symptom: `pip install` of a course pin fails to build. Cause: the image's Python minor version is below the course's floor. Fix: stop and report with the recorded version (§2 row 1) rather than silently choosing a different version. Enforced by R29 (ii), AC49.
- *Course pin shadowed by a preinstalled copy.* Symptom: an import resolves to the preinstalled `openai` rather than the pinned one. Cause: `--system-site-packages`. Fix: the pin wins inside the venv (§2); verify with the installed version in the report. Enforced by R29 (iii), AC49.

## Course Context Pack (embedded — agent-readable)

Concepts only; no code from the course appears here. Anchors are position-independent.

### CTX-A. The pattern

Four nested loops around one agent, each existing for one reason:

1. **Agent loop** — the model receives a task and context, calls a tool, observes the result, and repeats until it declares the task done. Exists because one model call is rarely enough for multi-step work. Here: fetch the requirement by id → write the analysis skeleton with facts → fill ambiguities, questions, assumptions, summary one edit at a time → finish. The agent's standing instructions are a file loaded every run (procedure + review guidance); its deliverable is a file in a confined workspace, not a chat message; a turn cap is the safety stop, not the normal one.
2. **Verification loop** — when the agent says it is done, a separate grader checks the finished file against a rubric of pass/fail criteria and either accepts or sends it back with per-criterion feedback, up to a budget. Exists because "done" is not "good enough", and because explicit criteria make cheaper models viable on harder tasks.
3. **Event-driven loop** — an event in the system where the work already happens (a ticket created, a requirement page edited, a message) triggers the verification-wrapped agent, and the result is written back into that system. Exists because an agent that must be opened, pasted into and asked is not used; one that lives where the conversation is becomes part of the workflow. The loops nest like Russian dolls but compose freely.
4. **Hill-climbing / learning loop** — across many completed runs, an analyst reads the traces (every message, every grader verdict and gap) and finds what the agent keeps being corrected on; it proposes one change to the harness (here: the instruction file), a human approves, code applies it, and a re-run of the same batch is compared for improvement or regression. Exists because an agent corrected one run at a time starts from the same place tomorrow; the story of a non-deterministic system is in its traces.

Human oversight sits at each level: sensitive tool calls, the grader, approval of outputs before delivery (a human closes the ticket), and approval of harness changes.

### CTX-B. Failure-mode catalog

- **B1 — Transient external failure.** Symptom: the fetch returns a service-unavailable or timeout message. Cause: an external system is busy. Fix: the agent retries the same tool with the same arguments until it succeeds; the course planted two such failures. Enforced by R2, AC3.
- **B2 — Stage skipped or reordered.** Symptom: a section left empty or filled out of order. Cause: ordering is requested by instructions, not enforced by the harness. Fix: a stage-order check reports it so a bad run is never accepted as a reference. Enforced by R3, AC4, AC5.
- **B3 — Cap stop mistaken for completion.** Symptom: a run that exhausted its turn budget prints the same "finished" line as a real finish. Cause: the loop ends either way. Fix: when the cap ends an incomplete run the trace says so. Enforced by R5, AC7.
- **B4 — Grader passes by resemblance.** Symptom: the grader passes criteria the file does not satisfy. Cause: it reads the file and still judges by how the conversation reads or how the file "looks". Fix: read the file before judging, quote a line number for every pass, apply labels literally, check every item. Enforced by R10, AC13, AC15.
- **B5 — Missing instructions ignored silently.** Symptom: a plausible but bad review. Cause: a missing memory file is skipped without warning, so the agent runs on the system prompt alone. Fix: fail loudly before any model call. Enforced by R6, AC8.
- **B6 — The agent edits its own instructions.** Symptom: review guidance drifts mid-run. Cause: the instruction file sits in the same writable filesystem as the analysis. Fix: a harness-level write denial on the instructions path, not a prompt sentence. Enforced by R7, AC10.
- **B7 — Stale analysis from a previous run.** Symptom: the agent reads an old analysis and skips stages. Cause: a shared workspace keeps the last file. Fix: a fresh workspace per run (the course deletes the file before each notebook run and gives each automated run its own directory). Enforced by R9, AC12.
- **B8 — A grader error counted as a verdict.** Symptom: pass rates computed over runs that received no verdict. Cause: the grader raised, the run continued. Fix: record a `grader_error` pass with no criteria; exclude the run from denominators; report the count. Enforced by R13, AC20, AC34.
- **B9 — A single occurrence acted on as a pattern.** Symptom: an instruction change that fixes one document. Cause: the analyst treated one run's problem as systemic. Fix: start from first-attempt pass rates across the batch; note one-offs under `rejected`. Enforced by R18, AC33.
- **B10 — Edit anchor not unique.** Symptom: an edit error, or duplicated headings in the file. Cause: the anchor string occurs more than once. Fix: the edit tool rejects it; the agent reads the file and retries; the analyst does not promote this one-off. Enforced by R27, AC21, AC22.
- **B11 — Recurring first-attempt failure = instruction gap.** Symptom: the same two criteria fail on the first attempt for every document and are fixed on the second. Cause: the rubric asks for labelled lines the instructions never mention. Fix: the learning loop proposes the missing instruction under the right heading; after approval and apply, every document passes first time. Enforced by R17–R21, AC33, AC46. Planted instance: `instructions_v1.md` lacks both labels.

### CTX-C. Decision background

**How to read the provenance notes.** *Litmus branch* — how an argued subject was resolved: a **row** (both sides shown working and differing in a component, identity or role), a **bake-in** (the course showed the other side failing, so the taught side is a business rule), or a **lever** (the sides differ only in a value, so it is a body default plus an Ask-First entry). *Tie-breaker 1* — a demonstrated failure wins: the course showed the other side failing, or warned against it as a failure (errors, degradation, broken behavior — not merely a side it outgrew), so the subject is a bake-in however many earlier lessons showed that side working. *Tie-breaker 2* — a trade-off about a value is a lever: the argued sides differ only in a numeric knob, not in a component, identity or role; a limit value that removes a component (a budget of 0) is a component choice and escapes this tie-breaker. *Lever-value branches* — how a contradicted lever's value was picked: (1) the value the narration states aloud in the lesson that introduces the concept; (2) the end-to-end application's configuration; (3) the value used most often, earliest-taught on ties. *Post-build lever* — a value you may change after the build, by asking first, never a gate question. *Stakes* — whether picking the other side of a contradiction up front changes structure, semantics or a guarantee; only then does a contradiction become a row. *Substitution row* — a row whose Default departs from the course's own technology because that technology needs setup the build cannot assume; the course's technology stays in Options tagged "(course default)". *Heavy bar* — a realization is heavy only if it needs a credential, a paid account, admin-level setup or special hardware; network access alone is not heavy. *Realization tiers* — among realizations meeting an invariant at the fixture scale, the lightest wins: (1) the language's standard library, (2) an embedded library, (3) a locally served process.

**Mined spoken trade-offs** (every one the course argued, with its disposition):

| # | Subject | Lesson | Disposition |
|---|---|---|---|
| T1 | Always-on instruction file vs skills by progressive disclosure | 3 | row D1 |
| T2 | Verification loop vs bare agent loop (budget 0 "is the same basic agent loop") | 2, 5 | row D2 — litmus: bare loop built first and shown working, then wrapped; budget 0 removes a component |
| T3 | Revision budget value (3 in notebook/batch runner vs 2 in event demo) | 5 (narration says 3) | lever R11 — tie-breaker 2: sides differ only in a value; lever-value branch 1 |
| T4 | Match model capability to task; cheaper models viable with verification; different grader model "a common production choice"; stronger model for the analyst | 2, 5, 7 (+ README) | lever R22 — attached to the constrained model/provider dimension; Ask First |
| T5 | Deterministic vs model-as-judge grader | 2 (narrated slide) | row D3 — enters on structure (owner moves from model to code); no trade-off argued, so not design-argued |
| T6 | Human approval of harness changes vs auto-apply; "hard to have confidence merging without evals" | 2, 7 | bake-in R17, R21 — tie-breaker 1: the course warns against unreviewed auto-apply as a failure ("hard to have confidence merging without evals" — a change that regressed would be merged unnoticed) and builds only the approved path |
| T7 | Report written to a separate agent-owned page vs into the requirement page | 6 (shipped code README) | bake-in R15 — tie-breaker 1: the course warns against writing into the requirement page as a failure (the source of truth is overwritten and its history lost), never shows it as a working alternative |
| T8 | A human closes the ticket vs the agent closing its own work | 6 | bake-in R16 — tie-breaker 1: the course warns against the agent closing its own ticket as an oversight failure (output delivered with no human approval), never shows it as a working alternative |
| T9 | Only the instruction file is auto-applied; tool/grader/configuration changes are read and decided by a person | 7 (module docstring) | bake-in R17 — tie-breaker 1: a half-applied non-prompt change is the named failure |
| T10 | "Most runs" is a pattern; one in five is not | 7 | lever R18 — a spoken heuristic quantified (generator's reading: more than half of graded runs) |
| T11 | Grader must read the file, not the transcript, and quote line numbers | 5 (helper comments) | bake-in R10 — tie-breaker 1: the course states the grader passed by resemblance without it |
| T12 | Scheduled vs event-triggered runs | 2 | narrative — framing of trigger kinds, not argued as a builder's choice; schedules are §1 item 4 |
| T13 | Where loop engineering sits among prompt, context and harness engineering; "levels" vs "loops" naming | 2 | narrative — taxonomy, not a decision |
| T14 | Composability: not every loop must nest every other | 2 | narrative — framing of how loops compose, not argued as a builder's choice; the one composition the course built both ways (grader on/off) is T2, row D2 |

- **C1 — Instruction placement (→ Ledger D1).** The course's primer shows three ways to instruct an agent: a system prompt string, a memory file loaded every run, and skill files whose description is always in context but whose body is read only on demand. The review agent uses the memory file with a pointer system prompt because the learning loop needs a file it can read and edit from outside, and because instructions placed there "carry the same weight" as the system prompt. The primer's skills (four poem forms) show progressive disclosure working: the trace reads each skill body only when writing that form. Choosing skills for the review guidance moves the proposal target from a heading in one file to a skill file.
- **C2 — Verification present and the budget (→ Ledger D2, lever in R11).** The grader is added in Lesson 5 after the bare loop works in Lesson 4; the first draft lacks the two labelled lines and is sent back; the second passes. The budget value appears as 3 in the Lesson 5 notebook and the batch runner and as 2 in the event demo's automation; narration says 3. The run status distinguishes "satisfied" from "ran out of tries" because the last grading pass reads `needs_revision` either way.
- **C3 — Fetch by identifier (→ R1).** The agent is built with no document; its opening message names only a ticket id and it must call the fetch tool, "exactly as it would against a real tracker ticket it doesn't already have open". The fake tracker is seeded at run time; the agent cannot tell a seeded document from a pre-existing one.
- **C4 — Simulated failures (→ R2, contradiction).** The course's helper defaults the fetch tool to zero simulated failures (a clean fetch); the Lesson 4 lesson text, the narration ("simulating two times of failure") and the pre-baked trace (a 503 message, then a timeout) show two. The narration value governs the fixture; the app default stays a clean fetch, as the batch runner comments that retries "only add turns and noise" there.
- **C5 — Event surfaces and the report page (pinned in §2; → R14–R16).** The course demonstrated the agent in Slack (direct message and channel mention, returning the report and its raw markdown) and in Jira/Confluence through automation rules and a tunnel, and shipped a keyless simulated tracker + wiki as the only code: creating a ticket or editing a linked requirement page while a ticket is open triggers the loop; the report is a new version of an agent-owned page so the wiki's own history shows every analysis and a diff between any two; counts often look similar before and after while the content changed completely, which is why both the counts table and the text diff are shown. The real integrations are untakeable in this lab (no credentials), so the row left the Ledger through the Environment Resolutions table; outside the lab they are Options tagged heavy.
- **C6 — The learning loop's design (→ R17–R21).** The harness has four improvable parts — prompt, tools, grader, configuration — and the course scoped the analysis to the prompt "because that is what the current evidence implicates", keeping the other targets expressible. Two properties the course says to keep: the analyst reads the traces and cannot write them ("an agent able to edit the evidence it is reasoning from is not analyzing anything"), and the analyst proposes but does not apply — plain code inserts the text so the edit is reviewable and deterministic. The committed result: before, completeness 5/5, clarity 0/5, depth 0/5, five revisions; after one approved insertion, 5/5 on all three with no revisions. The batch snapshots the instruction file it ran under so a saved run says what produced it. First-attempt failures are indexed by position because the grader paraphrases criterion names.
- **C7 — Model tiering (→ R22 lever).** The course runs the agent and grader on its cheaper model and the analyst on its stronger one, states that reading five full traces to find what recurs "is the one job the cheaper model does unreliably", and notes that a different grader model is a common production choice. The lab constrains *which* models are available (platform models through the proxy), not the tiering argument, which stays a lever.
- **C8 — Grader kind (→ Ledger D3).** The narrated Lesson 2 slide says graders "can either be deterministic or agentic (LLM as a judge is a classic example)"; the docs-writer example's grader is mechanical ("links resolve, CI passes"); the review agent's grader is a model with a read tool whose prompt restates the harness's default grading rules and adds three disciplines (read the file first; quote with line numbers; apply labels literally and check every item).
- **C9 — Acceptance-suite model (→ Ledger RR1).** The course's notebooks run live by default but ship pre-baked traces and committed batches so lessons replay without a key, and warn that live results vary between runs. This spec's scripted stand-in is its own realization of that idea for the test suite; the live models remain the course's choice and the finished app's.
- **C10 — Persistent store (pinned in §2).** The course's event demo keeps three plain JSON lists on disk, seeded once with the starting scenario, so a learner can open the files and see exactly what the app sees; batches are a directory of JSON run files plus a summary and the instruction snapshot. Tier 1 (standard library) satisfies R25 at the fixture scale; the framework also supports database-backed filesystems, named but never argued, so no row.
- **C11 — Hosted tracing (pinned in §2).** Optional in the course, switched on by environment variables alone; "everything works without it"; from Lesson 4 the course builds its own local trace table from the agent's stream, which is what R12 keeps.
- **C12 — Name-map and discrepancies (provenance only, never binding).** The course's default ticket id was `AUTH-142` ("User Profile File Upload"); its other tickets `AUTH-101`, `NOTIF-205`, `PAY-310`, `ACCESS-118`, `ALERT-227`; its event-demo seed ticket `REQ-104` with keys from `REQ-100`; its bot author "Requirements Analysis Agent (bot)"; its cast Dana/Jordan/Priya/Sam/Morgan; its batch labels `v1`/`v2`; its workspace folder `workspace/`, analysis path `/analysis.md`, instructions path `/memories/AGENTS.md`, proposal path `/proposal.md`; its event demo on port 5050. Contract-binding constants kept as-is: the five section headings, the labels `Reason:` / `Resolved by:` / `Edge case:`, the rubric names, ticket statuses `Open` / `Analysis Ready` / `Done`, page kinds, grading results, run statuses, harness-change targets, comparison verdicts, summary fields, the 8-hex-character run id. Discrepancies recorded, none binding: the fetch tool is named `fetch_requirement` in the root instruction file, the helper and the Lesson 4 narration, and `fetch_requirement_from_jira` in the batch snapshots and a Lesson 3 slide (narration branch picks the former); the memory file is `AGENTS.md` in code and narration, `Agent.md` on one slide; the learning-loop batch is "four documents" early in the Lesson 7 narration and five in the notebook and later narration (the application's five governs); the fourth loop is called hill-climbing, learning and self-improvement loop; one slide titles the third loop "application loop"; the course README promises an automatic offline fallback when the key is absent that the shipped code does not implement; the course's requirement text differs slightly between slide and narration (this spec authors its own). Presentation-only constants dropped by declaration: notebook styling, chart colors, tracing run names and tags, the LangSmith project names.

### CTX-D. Perishable assumptions

The concepts in CTX-A to CTX-C are durable. Only the names below are perishable — treat them as search keywords against current documentation, never as guaranteed imports or served models.

- Harness: `deepagents` 0.7.11 — `create_deep_agent`, `FilesystemBackend(root_dir, virtual_mode=True)`, `FilesystemMiddleware`, `FilesystemPermission(operations, paths, mode)`, `RubricMiddleware(model, max_iterations, tools, system_prompt, on_evaluation)` (flagged beta in this era; its default grader prompt was copied by the course and "replaces rather than extends"), `memory=`, `skills=`, `permissions=`, `response_format=`, a private `_rubric_status` state key, `checkpointer=InMemorySaver()` (the course notes it is not required for the rubric loop).
- LangChain: `langchain` 1.3.18 — `create_agent`, `langchain.agents.middleware.ModelCallLimitMiddleware(run_limit, exit_behavior="end")`, `langchain.tools.tool`; `langchain-core` 1.6.1 message types (`tool_calls`, `type`, `status`); `langgraph` 1.2.11 `stream(..., stream_mode="updates")`, `get_state(config)`.
- Model strings in the course's era: `openai:gpt-5.4-mini` (agent, grader, batches) and `openai:gpt-5.5` (analyst, and one slide's base-agent example) — provenance only; never asserted to be served by the platform proxy. **Request-parameter compatibility:** the course never passes `temperature` or other sampling parameters and relies on native tool calling and a typed structured response; whether a given platform model accepts a parameter is as perishable as its name, so send none the role needs not.
- Provider client: `langchain-openai` 1.6.0 / `openai` 3.6.0 (`OPENAI_API_KEY`, `OPENAI_BASE_URL`); `tiktoken` `o200k_base` encoding for the optional cost estimate.
- Web: Flask ≥3.1.3 (unpinned by the course); the course's demo bound port 5050.
- Tracing: `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` (and older `LANGCHAIN_*` aliases) — unavailable here.
- File-tool error text: a tool result with status `error` or text starting with "Error" — the detection the course's trace capture used.

### CTX-E. Provenance map

Lesson numbering follows the transcripts (the repo folders are one lower for each notebook; the course README uses a third numbering). Nothing in this spec requires platform access.

| Lesson (transcript) | Title | Contributed |
|---|---|---|
| 1 | Introduction | CTX-A framing of the four loops and the requirement-review agent |
| 2 | Overview of Loop Engineering | CTX-A (loops, nesting, human oversight), CTX-C T2 (the verification loop as a wrapper)/T4/T5/T6 (confidence without evals)/T12/T13/T14, C7, C8, §1 items 4–5 |
| 3 | Deep Agent Primer | CTX-C T1/C1 (→ D1), the filesystem confinement (R8), instruction placement, progressive disclosure |
| 4 | Agent Loop | R1–R5 (cap 12), CTX-B1/B2/B3/B5/B6/B7, C3, C4, C9 (the notebook note that live results vary; pre-baked traces) |
| 5 | Verification Loop | R10–R13 (cap 40, budget 3), CTX-B4/B8, C2, T2 (budget 0 "is the same basic agent loop"), T3, T11 |
| 6 | Event-Driven Loop | R14–R16, R25 (store), C5, C10, T7 (report page, shipped code README), T8 (a human closes), §1 items 1–2 |
| 7 | Learning loop | R17–R21, R27, CTX-B9/B10/B11, C6, T6, T9, T10 |
| 8 | Conclusion | none |
| Shipped code (helpers, runner, analyst module, event demo, data files, project and lock files) | — | parameter values and pins in §2, the schemas in §3, the grader disciplines, the name-map C12, C11, C9 (committed batches replay without a key) |
| Slides read | Overview deck (13 slides, all narrated except the title card), lesson deck (18 slides; 6 title cards deck-only, the rest narrated), event-driven deck (4 slides; title card deck-only, 3 narrated) | narrated slides rank with their lesson's transcript (slide 2.6 grader kinds → D3; slide 3.5 cap 12; slide 4.4 the four output sections; slide 5.3 the rubric flow); deck-only slides are title cards and contributed nothing; no deck-only slide conflicts with code or narration — the slide-vs-narration wording differences are recorded in C12 |
| `[environment]` coding-agent-lab | — | §0's two italic paragraphs, the Environment Resolutions table, §1 deliverable shape and adapting note, §2 rows marked `[environment]`, R22–R24, R29, the `[environment]` reinforcement of R25, §6 entries marked `[environment]`, the `## Runtime (lab)` section — none of it attributed to any lesson |

---

*Status footer* — version 1 · course: Loop Engineering with LangChain DeepAgents · learner project: the coding-agent-lab assignment (§1) · This is a living document: when the building agent produces something unexpected, add the missing constraint here and re-run.
