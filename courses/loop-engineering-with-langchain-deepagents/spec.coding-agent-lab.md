# Spec: Requirements Review Loops — Coding-Agent-Lab Build

> **What you're building:** a requirements-review web app whose agent gets better from its own runs. You open the tracker page, create a ticket against a deliberately vague requirement page, and watch the agent fetch the requirement, draft a five-section analysis, get sent back by the grader with a named gap, revise, and pass. You edit the requirement page and the review re-runs on its own, with a before/after table. Then you run the five-document batch, read the analyst's proposal, approve it, re-run the batch, and see every criterion pass on the first attempt. Answering the gate's first question with the recommended baseline builds all of this end to end; the build is **complete when the offline suite passes** — the platform keys unlock only the `live` tests and live use of the finished app.
>
> This file is self-contained: the Course Context Pack at the end replaces every external course reference, and nothing here needs platform or course access.
>
> `(CTX-X)` anchors mark course-derived knowledge. The Decision Ledger below holds every point where the build could diverge, each pinned to one course-derived default, so the spec builds as-is with no intake; the Environment Resolutions table under it shows which learner dimensions the lab already answered.
>
> Generated from the *Loop Engineering with LangChain DeepAgents* notebooks + transcripts + slides on 2026-10-13, guide @ `11b3673`, `coding-agent-lab` overlay @ `adeff70`.

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

   *`[environment]` In this lab the structured question tool is a fenced `choices` block: explain in prose above the fence, put the fence last in the message with one option per line, and precede it with a line `**Question N of M — <decision>**` so both of you can see nothing was skipped. Here the express-lane question is Question 1 of M+1, where M = the number of Ledger rows; the row questions of the next step are 2 … M+1. A click sends the option line verbatim; a typed answer naming an option counts identically. Only the latest message's buttons stay live, so never ask the person to go back and change an earlier answer — re-ask it as a new question.*

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

   *`[environment]` Each row is one message ending in its own `choices` fence, numbered `**Question N of M+1 — <decision>**`, N = 2 … M+1, with M = the number of Ledger rows (Question 1 is the express-lane question). Clicked and typed answers are equivalent. Because only the latest message's buttons stay live, a changed answer is re-asked as a new question rather than edited in place.*

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

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option. Rows are grouped learner → design → realization (pipeline order within a group). Five of the six learner-context dimensions, and one course-owned realization row, were resolved by the lab environment and leave the Ledger through the Environment Resolutions table that follows — they were derived, not skipped.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L1 | learner | **Scope boundary.** Present the §1 "Not Included" list *inside this question*, item by item with its handling tag, and ask whether every exclusion stands or something should come back. | — | Keep as-is: every §1 exclusion stands; the full acceptance set (§5) is built. | (a) keep every exclusion; (b) bring something back — name it in free text; the item's §1 handling tag says what the agent may do (`restorable` → add it; `named-not-built` → buildable but with no parameters or acceptance criteria from this spec; `owned-by-row` → defer to that row; `unavailable` → cannot be restored in this lab, seam stated). A further exclusion may also be added in free text and must name the acceptance criteria it retires. | Restoring an item adds unverified surface; adding an exclusion retires criteria. Nothing about the taught pattern changes either way. | learner |
| D1 | design-structural | **Grader realization** (verification loop, CTX-A stage 3). | A grader exists that scores every rubric criterion pass/fail on the *finished analysis file* (not on the conversation), returns a short `gap` for each failing criterion, sends that feedback back for another attempt while the revision budget lasts, and ends the loop successfully only when all criteria pass in the same grading pass (CTX-C3); otherwise the loop also ends, unsuccessfully, when the revision budget is spent, when a pass returns `failed`, or when a pass is a grader error (R10). | **Model-driven grader** reading the analysis file (course's realization): the grader role of the acceptance-suite model (RR1) in the offline run; a platform model in live use. The course's grader is given a read-file tool and is required to quote the satisfying line before passing a criterion (R11). | (1) Model-driven grader with mandatory file read and verbatim quoting (course default). (2) Deterministic checker in harness code: literal label checks for clarity/depth plus a rule for completeness (e.g. every requirement clause quoted). (3) Hybrid: deterministic label checks, model judgment for completeness only. | Structural litmus: the grader box's *owner* moves between model and harness, so this is a row, not a lever. Course argument (Lesson 2 slides: graders are "deterministic or agentic"; Lesson 5 code notes): a model grader judges nuance like completeness but, left unconstrained, "passes criteria the file does not satisfy" by resemblance (CTX-B4); a deterministic checker never drifts but cannot judge completeness semantically. Switching re-shapes grader feedback text, which the learning loop mines (CTX-C5). | course+learner |
| D2 | design-structural | **What an event trigger runs** (event-driven loop, CTX-A stage 4). | Every trigger (ticket created; linked requirement page edited while a ticket is open) produces exactly one run record linked to one new version of the agent-owned report page, and sets the ticket's status (R13). | **The verified loop**: trigger → agent loop → grader → revision budget (course's shipped automation ran the grader inside the trigger). | (1) Triggered run is the verified loop — grader + revision budget (course default). (2) Triggered run is the bare agent loop — the Lesson 4 form, revision budget 0, no grading passes recorded. | Structural litmus: option (2) removes the grader box from the triggered path, so it is a row. Lesson 2 narration: loops are composable — "you could just nest a core agent loop in with an event-driven loop; you don't need the verification loop per se" — but the verification loop "improves quality, especially in cases where models aren't as individually powerful". With (2), triggered runs carry no first-attempt verdicts, so only the batch runner (R16) feeds the learning loop. The revision-budget *value* is a separate lever (R10). | course+learner |
| RR1 | realization | **Which model the acceptance suite runs against.** | The offline suite drives the *real* pipeline end to end — the agent's tool calls, the grader, the event trigger, the batch runner, the analyst's structured proposal, the apply step and the comparison — with no network access, against a stand-in whose per-role behavior is declared in §5. | **Scripted stand-in** (`scripted_model.py`, §5): a fake chat model, honestly labeled as a stand-in for the platform model, with declared agent/grader/analyst roles. Branch taken: the model is the keyed dependency, so the stand-in is the default and criteria needing a real model are tagged `live`. | (1) Scripted stand-in for every role (offline). (2) The course's live model path — course ran `openai:gpt-5.4-mini` for agent and grader and `openai:gpt-5.5` for the analyst (course default); in this lab the platform supplies the key and base URL, so choosing it costs no setup, and the suite's `live` criteria then run too. | Keyed-tool rule: the stand-in keeps the pattern exercisable offline. Live runs are non-deterministic ("LLMs do not always produce the same results", every notebook) and cost wall-clock time; the course bounded cost by turn caps and the revision budget (CTX-D). | course+learner |

### Environment Resolutions

This spec targets the **`coding-agent-lab`** environment. The six learner-context dimensions below were each derived from the course materials first (invariant and course-derived default), and then resolved against the lab — resolved, not skipped. One course-owned realization row joins them because every alternative it offered is untakeable here.

| Dimension | Resolution | Where the Invariant lives now |
|---|---|---|
| project | **ANSWERED** — the lab fixes the assignment: the course's example shape (a requirements-review service: simulated tracker + versioned requirement pages, event-triggered verified reviews, a learning-loop panel) re-expressed on the synthetic fixture corpus. | spec §1 Objective. Invariant empty. |
| data/inputs | **ANSWERED** — inputs are seeded into the workspace: one seed requirement page, one open seed ticket, five batch requirement documents. | spec §5 fixture corpus. Invariant empty. |
| goal | **ANSWERED** — the lab fixes what "working" means: every triggered run yields a five-section, three-criterion-graded analysis; the learning loop lifts first-attempt clarity and depth from 0/5 to 5/5 on the batch with no criterion regressing. | spec §1 + the acceptance criteria (AC12, AC26–AC27). Invariant empty. |
| model/provider | **CONSTRAINED** — the built app needs an LLM for three roles, so: platform models only, keys and base URLs read from the environment, never asked for. Derived invariant: the model must support native tool calling (the agent loop is tool-call driven) and structured output (the analyst returns a typed proposal); the three roles — agent, grader, analyst — are independently assignable (the course argues model tiering). | spec §2 (model-roles table, key variables) + R20 + CTX-D. Exercised by AC30 (variables read, key never hardcoded, base URL honored), AC31 (three roles independently assignable); the platform model's own capabilities (native tool calling, structured output) are exercised by the `live`-tagged criterion AC22 and §7's live smoke run, while offline the scripted roles (RR1) stand in for them. The course's tiering trade-offs became body levers with Ask-First entries (§6). |
| environment | **ANSWERED** — the container. Derived invariants: a per-run writable filesystem the agent is confined to (R7, AC6); a durable store for pages, tickets, runs and run history that survives a process restart (R21, AC29); the agent's instructions file is editable from outside the agent and never by it (R5, R18, AC5, AC25). | spec §2 + `## Runtime (lab)`. |
| scope-boundary | **KEPT** | Ledger row L1. Invariant empty. |
| event source and record system (course-owned realization row: real Slack bot / real Atlassian Jira + Confluence / the course's shipped simulated tracker) | **ANSWERED — every alternative unavailable here.** The real integrations need a Slack workspace with app-level and bot tokens, or an Atlassian Cloud site with an API token, automation rules and a public tunnel — credentials this lab does not supply and this spec may never ask for. The only takeable realization is the course's own shipped stand-in, so the row is not asked. | Pinned in §2 (simulated tracker + flat-file JSON store, tier 1) with the course's provenance; the integrations are §1 `unavailable` items with their seams stated; invariant (every trigger yields one run record + one report version, R13) exercised by AC12–AC15. |

## 1. Objective

A served web app in which a requirements-review agent turns a vague requirement into a five-section analysis, a grader sends it back until three rubric criteria pass, tracker events run that verified review automatically and record every run, and a learning loop reads a batch of runs, proposes one change to the agent's instructions, applies it only after a human approves, and proves the improvement by re-running the batch — guaranteeing that every run's verdict, trace and report version are on disk and that no instruction change reaches the agent unreviewed. (pattern: CTX-A)

**Deliverable shape `[environment]`.** One server on port 4000 serving both the page and its API — the preview pane is the only view of the running app. The course's own artifacts (four notebooks and a two-surface demo app on port 5050) are not the deliverable; this app embodies the same four loops behind one page.

**Adapting this beyond the lab.** *Project* and *goal* are fixed in this section; a standalone build re-opens them as Ledger rows. *Data/inputs* is the §5 fixture corpus; swap it for your own requirement documents. *Model/provider* lives in §2's model-roles table and R20 (platform models via `OPENAI_API_KEY` / `OPENAI_BASE_URL`); elsewhere, supply your own provider and keys and restore the model/provider row. *Environment* lives in §2 and `## Runtime (lab)` (port 4000, relative URLs, venv rules); elsewhere, pick your own port and drop the proxy rules. The *event source* is pinned in §2 to the simulated tracker; elsewhere, the real integrations below become Ledger options again.

### Not Included

Each item carries its handling tag for the L1 gate question: `restorable` (additive, owned by no row — may be added at the gate), `named-not-built` (the course named it but never built it — buildable, but this spec supplies no parameters and no acceptance criteria for it), `owned-by-row` (decided by the named Ledger row; never decide it twice), `unavailable` (cannot be restored in this lab; the seam a standalone build would use is stated).

1. **Real Slack bot** (the course's Lesson 6 demo: a bot that reviews a requirement pasted in a direct message or a channel mention) — `unavailable`: needs a Slack workspace plus app-level and bot tokens. Seam: the trigger entry point of R13 (the function a webhook would call) invoked from a Slack event handler.
2. **Real Atlassian Jira + Confluence integration** (API token, automation rules, public tunnel) — `unavailable`. Seam: replace the store's page and ticket lookups with the vendor REST APIs and call the R13 trigger from a webhook endpoint; nothing about the agent or the loop changes (the course's own stated next step).
3. **Hosted tracing** (the course's optional LangSmith tracing via `LANGSMITH_*` variables) — `unavailable`: needs an API key. The local per-run trace table (R9) carries the same information; the seam is the tracing library's environment variables, read by nothing in this build.
4. **The primer's skill library** (progressive-disclosure `SKILL.md` folders, demonstrated on a poet agent in Lesson 3) — `named-not-built`: the review agent carries all its instructions in one always-loaded file (CTX-C9).
5. **Scheduled triggers** (a timer or calendar-style trigger, Lesson 2) — `named-not-built`: only event triggers (ticket created, requirement edited) are built.
6. **Memory consolidation / user-preference memory** (Lesson 2's second hill-climbing category) — `named-not-built`: the learning loop improves procedural instructions only.
7. **Subagent delegation, code interpreter / sandbox, context summarization** (deep-agent pillars named in Lesson 3) — `named-not-built`.
8. **Human approval inside the agent loop** (interrupting before a sensitive tool call, Lesson 2) — `named-not-built`: the build's human gates are at the artifact (R14) and at the harness change (R18).
9. **USD cost estimates** in the batch comparison (the course priced its own two models) — `restorable` at the gate by supplying prices for the platform models; token estimates stay (R19).
10. **Notebook plots and pandas grids** — `restorable`; the page renders the same facts as tables (a declared drop of presentation-only output).
11. **User accounts and authentication** — `restorable`: the course's fixed cast of five people stands in for an account directory (§5).
12. **Live push (WebSockets)** — `unavailable` in the lab (HTTP only); the page polls or reloads.
13. **Live-model runs inside the offline suite** — `owned-by-row` RR1.
14. **Integration into an existing codebase** — `unavailable` (outside the delivered build mode).
15. **A human acting as the grader** (Lesson 2 names the grader as one of the places a human may sit, CTX-C6) — `unavailable`: the offline suite, which is the completion gate, cannot wait on a person. Seam: the grader box of row D1 — a standalone build would take a person's pass/fail verdict per criterion, with a `gap` per failure, where the grader's `GradingPass` is produced.

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python 3 (the container's interpreter) `[environment]` | The course requires Python ≥ 3.12 (its pyproject and README; numpy/pandas fail to build on 3.11, but this build installs neither). **Step 1 of the build:** run `python3 --version`, record the result in `resolved-decisions.md`, and **stop with a report** if any course-pinned package below refuses the interpreter — never assume the course's floor is met. |
| Virtual environment | `python3 -m venv .venv --system-site-packages` `[environment]` | Reuses the preinstalled stack (`fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`). Where a course pin below differs from a preinstalled copy, **the course pin wins inside the venv**. Batch every install into one early step and announce its wall-clock cost before running it. |
| Agent harness | `deepagents==0.7.11` | **Course pin situation, stated honestly:** the course's `pyproject.toml` sets floors (`>=`), and its `uv.lock` resolves exact versions; §2 pins the lock's versions for every package the lock contains. The course's harness is a §2 pin, not a Ledger row — swapping it is a different course. Era-specific class and parameter names → CTX-D. |
| Agent framework | `langchain==1.3.18`, `langchain-core==1.6.1`, `langgraph==1.2.11` | Lock pins. The grader middleware the course uses is flagged beta in this era (CTX-D). |
| Provider client | `langchain-openai==1.6.0`, `openai==3.6.0` | Lock pins; `openai` is preinstalled in the lab at an unstated version — the course pin wins in the venv. The client must honor `OPENAI_BASE_URL` (R20). |
| Structured output | `pydantic==2.13.5` | Lock pin; the analyst's proposal is a typed object (§3). |
| Token estimate | `tiktoken==0.14.0` (optional) | Lock pin; the course falls back to a characters-÷-4 estimate when it is unavailable (R19). Install it only if it builds cleanly for the recorded interpreter. |
| Config loading | `python-dotenv==1.2.3` (lock pin; preinstalled at an unstated version — the course pin wins in the venv) | `.env` is optional; the lab exports the variables directly. |
| Web server | `fastapi` + `uvicorn` (preinstalled) `[environment]` | The course's demo used Flask (floor `>=3.1.3`, **no lock entry** — unpinned), on port 5050 with two separately styled surfaces. The lab serves one page and its API from one process on port 4000; FastAPI is chosen because it is preinstalled, and the web layer is not the taught subject. |
| Event source & record system | **The course's simulated tracker, in-process** (pinned here via the Environment Resolutions table) | Realization branch: the course's real tools (Slack; Atlassian Jira + Confluence) are keyed and untakeable here; the course itself shipped this stand-in, so no lighter substitute was needed. |
| Persistent store | **Flat JSON files**, one list per collection: `data/pages.json`, `data/tickets.json`, `data/analysis_runs.json`; run history as `run_history/<label>/` (one JSON file per run, `summary.json`, and the instructions snapshot) | Lightest by tier: tier 1 (ships with the standard library). Both the course's flat files and the container's `sqlite3` are tier 1; the course's own realization is kept because it satisfies the invariant (survives restarts, keeps every page version and links runs to report versions, R21) at the declared fixture scale (one seed page, a handful of tickets, batches of five runs). Scaling realizations (SQLite, a document DB) are alternatives, not defaults. |
| Agent workspace | `harness/` inside the app folder: `harness/memories/AGENTS.md` (the live instructions), one throwaway `harness/runs/<run-id>/` per run; the analyst is rooted at the app-root `run_history/` (the persistent-store row above — the one run-history location) | Course-demonstrated: the course keeps the instructions file inside the agent's own virtual root (CTX-C8). `[environment]` The lab forbids authoring the *workspace-root* `AGENTS.md` (the IDE rewrites it, R24); the app's file lives only under `harness/`. |
| Model roles | Three environment variables, set by the build agent **when it writes `resolved-decisions.md`**: `REVIEW_AGENT_MODEL`, `REVIEW_GRADER_MODEL`, `REVIEW_ANALYST_MODEL`. Each holds a platform model id, or the literal `scripted` to select the §5 stand-in for that role. | `[environment]` The platform's model set is not enumerated here because it changes. The checklist carries one **"model roles"** line with the build agent's "(Recommended)" platform model per role; the person's confirmation of the checklist confirms them — no extra gate question. Course-derived tiering (body levers, §6 Ask First): grader = the agent's model (course ran both on one model, "a different model for the grader is a common production choice"); analyst = a more capable tier than the agent ("the one job the cheaper model does unreliably"). The course's own ids (`openai:gpt-5.4-mini`, `openai:gpt-5.5`) are provenance only (CTX-D); the spec never asserts the proxy serves them. |
| Key variables | `OPENAI_API_KEY` + `OPENAI_BASE_URL` (**read** — the course's provider is OpenAI-compatible); `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL` (**present, never read**) `[environment]` | Exactly these four names exist in the container. Never hardcode a key, never ask the person for one, never guess at other variable names (R20). |
| Secrets handling | Environment variables only; `.env` (if used) is git-ignored and never committed. | Listed under **Never** in §6. |
| Tests | `pytest` (install into the venv; unpinned by the course — choose a current release) | The offline suite runs with every model role set to `scripted` (§7). |

## 3. Input/Output Contracts

All schemas are JSON Schema (draft 2020-12). Identifiers: run ids are 8 lowercase hex characters (course: the first 8 characters of a hex UUID — alphabet is part of the contract); ticket keys match `^[A-Z]+-[0-9]+$` and new keys are `REQ-<n>` with `n` = highest existing number + 1, or 100 when none exists; a page created through `POST api/pages` gets the id `page-<slug>` where the slug is the lowercased title with every non-alphanumeric run collapsed to one hyphen, suffixed `-2`, `-3`, … on collision, while a seeded page keeps the id its fixture declares (`page-shared-document-links`, §5); a report page id is `page-analysis-<ticket key lowercased>`; timestamps are `YYYY-MM-DD HH:MM UTC`.

### 3.1 The analysis file (`/analysis.md` in the run workspace) — text contract

The agent's deliverable is a Markdown file, not a message. Grammar (binding):

- Line 1: `# Requirements Analysis`.
- Exactly five `## ` headings in this order: `Confirmed Facts`, `Ambiguities`, `Clarification Questions`, `Assumptions`, `Summary`.
- The four list sections hold bullets (`- `). An Ambiguities bullet has the shape: a bold quoted clause on the bullet line, then an indented `Reason:` line; a *revised* or *improved* bullet adds an indented `Resolved by:` line and an indented `Edge case:` line (the rubric's two labels, R10). Labels are matched literally — `Resolved by:` and `Edge case:` exactly, indented under their bullet.
- Summary is prose, two or three sentences; its size is a word count, never a bullet count.

Parsed form, as the API returns it:

```json
{
  "$id": "AnalysisReport",
  "type": "object",
  "required": ["markdown", "counts", "summary_words", "complete"],
  "properties": {
    "markdown": { "type": "string", "pattern": "^# Requirements Analysis\\n" },
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
    "summary_words": { "type": "integer", "minimum": 0 },
    "complete": { "type": "boolean", "description": "true iff every list section has >= 1 bullet AND summary_words > 0" },
    "stage_order": { "type": "array", "items": { "enum": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"] }, "description": "each section once, in the order the agent's successful write/edit calls first filled it; a later edit to an already-filled section (a revision after grader feedback) does not append" }
  }
}
```

### 3.2 Trace step, grading pass, run status

```json
{
  "$id": "TraceStep",
  "type": "object",
  "required": ["step", "actor", "action", "detail"],
  "properties": {
    "step": { "type": "integer", "minimum": 1 },
    "actor": { "enum": ["Model reasoning", "Tool"] },
    "action": { "type": "string", "minLength": 1 },
    "detail": { "type": "string", "maxLength": 221, "description": "tool output, whitespace-collapsed, cut to 220 characters plus an ellipsis" }
  }
}
```

```json
{
  "$id": "GradingPass",
  "type": "object",
  "required": ["iteration", "result", "explanation", "criteria", "analysis_markdown"],
  "properties": {
    "iteration": { "type": "integer", "minimum": 1 },
    "result": { "enum": ["satisfied", "needs_revision", "failed", "grader_error"] },
    "explanation": { "type": "string" },
    "criteria": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "passed"],
        "properties": {
          "name": { "type": "string" },
          "passed": { "type": "boolean" },
          "gap": { "type": "string" }
        },
        "if": { "properties": { "passed": { "const": false } } },
        "then": { "required": ["gap"], "properties": { "gap": { "minLength": 1 } } }
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
```

Run `status` (terminal, one per run): `satisfied` (all criteria passed in one pass) · `max_iterations_reached` (budget exhausted, last pass still `needs_revision`) · `failed` (the rubric was malformed or impossible to evaluate) · `grader_error` (the grader itself errored; that pass is the final pass, R10) · `turn_limit_reached` (the model-turn cap stopped the run with an incomplete analysis). A run whose grading list is empty (bare agent loop, D2 option 2) has status `finished` when the analysis is complete, `incomplete` when the model ended its turn with no tool call while the analysis was still incomplete (missing, or a list section or the Summary empty), and `turn_limit_reached` when the cap stopped it (R4). In the verified loop an incomplete file is graded like any other.

### 3.3 Tracker records

```json
{
  "$id": "Ticket",
  "type": "object",
  "required": ["key", "title", "description", "linked_page_id", "assignee", "status", "comments", "created_at", "last_analyzed_version", "last_run_id"],
  "properties": {
    "key": { "type": "string", "pattern": "^[A-Z]+-[0-9]+$" },
    "title": { "type": "string", "minLength": 1 },
    "description": { "type": "string" },
    "linked_page_id": { "type": "string", "pattern": "^page-[a-z0-9-]+$" },
    "assignee": { "enum": ["Dana (Product Manager)", "Jordan (Eng Lead)", "Priya (QA Lead)", "Sam (Backend Engineer)", "Morgan (Frontend Engineer)", "Unassigned"] },
    "status": { "enum": ["Open", "Analysis Ready", "Done"] },
    "comments": { "type": "array", "items": { "type": "object", "required": ["author", "text", "timestamp"], "properties": { "author": { "type": "string" }, "text": { "type": "string" }, "timestamp": { "type": "string" } } } },
    "created_at": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2} UTC$" },
    "last_analyzed_version": { "type": ["integer", "null"], "minimum": 1 },
    "last_run_id": { "type": ["string", "null"], "pattern": "^[0-9a-f]{8}$" }
  },
  "if": { "properties": { "status": { "const": "Analysis Ready" } } },
  "then": { "properties": { "last_run_id": { "type": "string" }, "last_analyzed_version": { "type": "integer" } } }
}
```

```json
{
  "$id": "Page",
  "type": "object",
  "required": ["id", "kind", "title", "linked_ticket", "versions"],
  "properties": {
    "id": { "type": "string", "pattern": "^page-[a-z0-9-]+$" },
    "kind": { "enum": ["requirement", "analysis_report"] },
    "title": { "type": "string", "minLength": 1 },
    "linked_ticket": { "type": ["string", "null"] },
    "versions": {
      "type": "array",
      "items": { "type": "object", "required": ["n", "author", "timestamp", "body"],
        "properties": { "n": { "type": "integer", "minimum": 1 }, "author": { "type": "string" }, "timestamp": { "type": "string" }, "body": { "type": "string" } } }
    }
  },
  "allOf": [
    { "if": { "properties": { "kind": { "const": "requirement" } } },
      "then": { "properties": { "linked_ticket": { "type": "null" }, "versions": { "minItems": 1 } } } },
    { "if": { "properties": { "kind": { "const": "analysis_report" } } },
      "then": { "properties": { "linked_ticket": { "type": "string", "pattern": "^[A-Z]+-[0-9]+$" }, "id": { "pattern": "^page-analysis-[a-z]+-[0-9]+$" } } } }
  ]
}
```

```json
{
  "$id": "AnalysisRun",
  "type": "object",
  "required": ["id", "ticket_key", "requirement_page_id", "requirement_version", "report_page_id", "report_version", "status", "turns", "counts", "complete", "stage_order", "trace", "grading", "timestamp"],
  "properties": {
    "id": { "type": "string", "pattern": "^[0-9a-f]{8}$" },
    "ticket_key": { "type": "string", "pattern": "^[A-Z]+-[0-9]+$" },
    "requirement_page_id": { "type": "string" },
    "requirement_version": { "type": "integer", "minimum": 1 },
    "report_page_id": { "type": "string" },
    "report_version": { "type": "integer", "minimum": 1 },
    "status": { "enum": ["satisfied", "max_iterations_reached", "failed", "grader_error", "turn_limit_reached", "finished", "incomplete"] },
    "turns": { "type": "integer", "minimum": 1 },
    "counts": { "$ref": "AnalysisReport#/properties/counts" },
    "complete": { "$ref": "AnalysisReport#/properties/complete" },
    "stage_order": { "$ref": "AnalysisReport#/properties/stage_order" },
    "trace": { "type": "array", "minItems": 1, "items": { "$ref": "TraceStep" } },
    "grading": { "type": "array", "items": { "$ref": "GradingPass" } },
    "timestamp": { "type": "string" }
  },
  "allOf": [
    { "if": { "properties": { "status": { "const": "satisfied" } } },
      "then": { "properties": { "grading": { "minItems": 1 } } } },
    { "if": { "properties": { "status": { "enum": ["finished", "incomplete"] } } },
      "then": { "properties": { "grading": { "maxItems": 0 } } } }
  ]
}
```

### 3.4 Learning-loop records

```json
{
  "$id": "RunRecord",
  "type": "object",
  "required": ["run_id", "doc_name", "label", "model", "requirement_doc", "instructions", "messages", "grading", "analysis_markdown", "status", "started_at"],
  "properties": {
    "run_id": { "type": "integer", "minimum": 1 },
    "doc_name": { "type": "string" },
    "label": { "type": "string", "pattern": "^[A-Za-z0-9_-]+$" },
    "model": { "type": "string", "description": "the agent role's model id as configured, or 'scripted'" },
    "requirement_doc": { "type": "string" },
    "instructions": { "type": "string", "description": "the instructions file this run was given, verbatim" },
    "messages": { "type": "array", "minItems": 2, "items": { "type": "object", "required": ["type", "content", "tool_calls"], "properties": { "type": { "type": "string" }, "content": { "type": "string" }, "tool_calls": { "type": "array", "items": { "type": "object", "required": ["name", "args"] } }, "tool_call_id": {}, "status": {} } }, "description": "every message, untruncated, full tool-call arguments and full tool results" },
    "grading": { "type": "array", "items": { "$ref": "GradingPass" } },
    "analysis_markdown": { "type": "string" },
    "status": { "type": "string" },
    "started_at": { "type": "string" }
  }
}
```

```json
{
  "$id": "BatchSummary",
  "type": "object",
  "required": ["label", "model", "runs", "graded", "grader_errors", "first_attempt", "revisions_needed", "documents"],
  "properties": {
    "label": { "type": "string" },
    "model": { "type": "string" },
    "runs": { "type": "integer", "minimum": 1 },
    "graded": { "type": "integer", "minimum": 0 },
    "grader_errors": { "type": "integer", "minimum": 0 },
    "first_attempt": {
      "type": "object",
      "required": ["completeness", "clarity", "depth"],
      "additionalProperties": { "type": "object", "required": ["passed", "total", "pass_rate"],
        "properties": { "passed": { "type": "integer" }, "total": { "type": "integer" }, "pass_rate": { "type": ["number", "null"] } } }
    },
    "revisions_needed": { "type": "integer", "minimum": 0, "description": "the number of graded runs whose first grading pass failed at least one criterion" },
    "documents": { "type": "array", "items": { "type": "string" } }
  }
}
```

Invariants (R16): `graded + grader_errors == runs` (a `failed` pass counts as graded; only `grader_error` runs are excluded); `revisions_needed` = graded runs whose first pass failed at least one criterion; every `first_attempt.*.total == graded`; `pass_rate == passed / total` rounded to 3 places, or `null` when `graded == 0`; criteria are matched by **position** in the rubric, never by the grader's echoed name.

```json
{
  "$id": "HarnessChange",
  "type": "object",
  "required": ["target", "issue", "recurrence", "evidence", "section", "change", "rejected"],
  "properties": {
    "target": { "enum": ["prompt", "tool", "grader", "configuration"] },
    "issue": { "type": "string", "minLength": 1 },
    "recurrence": { "type": "string", "minLength": 1 },
    "evidence": { "type": "array", "minItems": 1, "items": { "type": "string", "pattern": "^run_[0-9]{2}_[^:]+: .+", "description": "<run file stem>: <verbatim quote from that run's RunRecord> (R17)" } },
    "section": { "type": "string" },
    "change": { "type": "string", "minLength": 1 },
    "rejected": { "type": "array", "items": { "type": "string" } }
  },
  "if": { "properties": { "target": { "const": "prompt" } } },
  "then": { "properties": { "section": { "pattern": "^#{1,6} " } } }
}
```

```json
{
  "$id": "Comparison",
  "type": "object",
  "required": ["verdict", "criteria", "runs", "revisions_needed", "attempts", "input_tokens", "output_tokens", "improved", "regressed"],
  "properties": {
    "verdict": { "enum": ["regression", "success", "partial", "no effect"] },
    "criteria": { "type": "object", "additionalProperties": { "type": "array", "items": { "type": "integer" }, "minItems": 2, "maxItems": 2 } },
    "runs": { "type": "integer" },
    "revisions_needed": { "type": "array", "items": { "type": "integer" }, "minItems": 2, "maxItems": 2 },
    "attempts": { "type": "array", "items": { "type": "integer" }, "minItems": 2, "maxItems": 2 },
    "input_tokens": { "type": "array", "items": { "type": "integer" }, "minItems": 2, "maxItems": 2 },
    "output_tokens": { "type": "array", "items": { "type": "integer" }, "minItems": 2, "maxItems": 2 },
    "improved": { "type": "array", "items": { "type": "string" } },
    "regressed": { "type": "array", "items": { "type": "string" } }
  },
  "allOf": [
    { "if": { "properties": { "regressed": { "minItems": 1 } } }, "then": { "properties": { "verdict": { "const": "regression" } } } },
    { "if": { "properties": { "verdict": { "const": "success" } } }, "then": { "properties": { "regressed": { "maxItems": 0 }, "revisions_needed": { "prefixItems": [ {}, { "const": 0 } ] } } } }
  ]
}
```

### 3.5 HTTP API (all paths relative to the served page; JSON in and out)

| Method & path | Body → result |
|---|---|
| `GET api/config` | → `{ "models": { "agent", "grader", "analyst" }, "instructions_path", "revision_budget", "turn_cap", "simulated_fetch_failures" }` (R20, R3) |
| `GET api/tickets` · `POST api/tickets` | POST `{title, description, linked_page_id, assignee}` — `title`, `description` (may be empty) and `linked_page_id` required, `assignee` optional and `Unassigned` when omitted → creates the ticket, **runs the trigger synchronously** (R13), returns `{ticket, run_id}` |
| `GET api/tickets/{key}` | → `{ticket, page, report_page, runs[], latest_run, previous_run}` |
| `POST api/tickets/{key}/rerun` · `POST api/tickets/{key}/close` | rerun → `{run_id}` (R13); close → ticket with `status: "Done"` (R14); both `404` for an unknown key, and rerun/close `409` for a `Done` ticket |
| `GET api/runs/{run_id}` | → `AnalysisRun` |
| `GET api/pages` · `POST api/pages` | POST `{title, body, author}` → new requirement page (version 1) |
| `GET api/pages/{id}?v=` · `POST api/pages/{id}/versions` | POST `{body, author}` on a requirement page → new version, then the trigger re-runs for every open linked ticket; returns `{version, retriggered: [keys]}`; `400` for a report page (R13) |
| `GET api/pages/{id}/compare?a=&b=` | → `{diff: [unified diff lines], run_a, run_b}` where `run_a`/`run_b` are the `AnalysisRun`s behind those report versions, `null` for requirement pages (R15) |
| `GET api/instructions` | → `{text, version_label}` of `harness/memories/AGENTS.md` |
| `GET api/history` · `POST api/history/{label}/run` | POST `{instructions: "baseline" \| "<label>"}` → runs the batch (R16) and returns `BatchSummary`. `"baseline"` selects the live instructions file `harness/memories/AGENTS.md` as it stands when the batch starts (so after an applied proposal it is the new text); `"<label>"` selects the snapshot `run_history/<label>/AGENTS.md` an earlier batch stored, `404` when that label has none |
| `GET api/history/{label}/summary` · `GET api/history/{label}/runs` | → `BatchSummary` · `RunRecord[]` |
| `POST api/history/{label}/propose` | → `{change: HarnessChange, proposal_markdown}` (R17) |
| `POST api/history/{label}/apply` | `{approved: true}` → applies the stored proposal to the live instructions (R18), returns `{diff, new_text}`; `{approved: false}` or missing → `409` and nothing changes; `422` when `target != "prompt"` |
| `GET api/history/compare?before=&after=` | → `Comparison` (R19) |

## 4. Business Rules

Provenance labels: **course-demonstrated** (traceable to the materials, with a CTX anchor), **project hardening** (added here), **`[environment]`** (contributed by the lab, never by the course). Parameter values cite their exact source.

**Agent loop**

- **R1 — The agent is told only the ticket id and must fetch the requirement itself.** The run's opening message names the ticket key and nothing else; the agent obtains the text through its `fetch_requirement` tool, which resolves the key against the store at call time (the current version of the linked requirement page, or a batch document seeded under the key). Each batch document is seeded right before its run under the key `BATCH-<n>`, `n` = its 1-based position in sorted order (`BATCH-1` … `BATCH-5`); a batch key is a fetch lookup only, not a tracker ticket — it has no page, no report and no entry in `data/tickets.json`. On success the tool returns the line `REQUIREMENT: <title>`, one blank line, then the body verbatim: for a requirement page, the page's title and its current version's body; for a batch document, the file verbatim (it already opens with that line). A requirement's **clauses** are the non-empty lines after the `REQUIREMENT:` line of that result — the same definition for pages and batch documents. The agent is never handed the document directly. Course-demonstrated (CTX-A, CTX-C1). → AC2, AC12
- **R2 — Staged, file-based analysis.** The agent writes `/analysis.md` (§3.1) in its run workspace: one `write_file` laying down the exact five-section skeleton with only Confirmed Facts filled, then one `edit_file` per remaining section in order (Ambiguities, Clarification Questions, Assumptions, Summary), one tool call per turn; the Ambiguities bullet shape is binding; the Summary is two or three sentences; when the Summary is written the agent ends with one short completion message and no further tool calls. Stage order is *requested by the instructions, not enforced by the harness*: the run records the order the successful writes actually filled sections in (`stage_order`: each section once, at its first fill — a revision edit after grader feedback does not append, §3.1) so a skipped or reordered stage is visible. Course-demonstrated (CTX-A, CTX-C8; the course's instructions file and its stage checker). → AC2, AC3
- **R3 — Transient tool failures are retried with the identical call.** The fetch tool can return an error string instead of a document; on an error result the agent calls the same tool again with the same arguments until it succeeds. The simulated fetch fails a configurable number of times (`REVIEW_FETCH_FAILURES`, §5) before succeeding, deterministically, returning these exact strings, the first two in rotation: `Error: 503 Service Unavailable — the requirement service is temporarily unavailable, please retry.` and `Error: request timed out after 10s — please retry.`; an unknown key returns `Error: no ticket '<key>' found.` Every error result begins with `Error:`, and no successful result does (a success begins `REQUIREMENT:`, R1). **Default count: 2** in event-triggered and manual runs — *contradicted lever*: the Lesson 4 narration, notebook text and committed trace say two failures, while the helper module's code default is 0; value-selection branch 1 (the value the introducing lesson's narration states) picks 2. The batch runner (R16) uses **0** — the course's batch code says the retry "only adds turns and noise" there. **Post-build lever** (§6 Ask First). Course-demonstrated (CTX-B1). → AC4
- **R4 — Model-turn cap, and an honest stop reason.** A run stops when the model has taken the cap's number of turns (`REVIEW_TURN_CAP`, §5): **40** for a verified run (Lesson 5 notebook, the course's automation, the batch runner) and **12** for a bare agent-loop run (Lesson 4 notebook, `MAX_TURNS`; "six stages plus headroom for the retries and the closing message"). The cap is *not* the normal stop — the loop normally ends when the model finishes the Summary — so a run that hits the cap with an incomplete analysis is recorded as `turn_limit_reached`, never as finished; its last trace row reads "Stops: turn limit of <cap> reached". A bare-loop run whose model ends its turn with no tool call while the analysis is still incomplete is recorded as `incomplete` — neither `finished` nor `turn_limit_reached`, since no cap was hit (§3.2). Course-demonstrated (CTX-B2); the `incomplete` status is project hardening. → AC8, AC30, AC34
- **R5 — The agent never edits its own instructions and never edits the requirement.** Writes under `/memories/` in the run workspace are denied by the harness (not merely by instruction); the requirement page is read-only to the agent (its only path to it is the fetch tool). Course-demonstrated (CTX-C8; the course's deny permission). → AC5
- **R6 — Missing instructions fail loudly.** Building a run whose workspace lacks `/memories/AGENTS.md` raises an error before any model call: the course's memory loader ignores a missing file silently, and the agent "would run on the system prompt alone and produce a plausible bad review". Course-demonstrated (CTX-B3). → AC7
- **R7 — One fresh, confined workspace per run.** Every run gets its own throwaway workspace seeded with the current instructions file; any leftover `/analysis.md` is absent at run start (a stale file lets the agent skip stages); the agent sees the workspace as `/` and paths above it are unreachable; the workspace is deleted after its artifacts are recorded. Course-demonstrated (CTX-B5; the course's per-run workspace). → AC6
- **R8 — `edit_file` is exact and refuses ambiguity.** An edit replaces one exact string; when the target string is absent or occurs more than once the tool returns an error and the file is unchanged (the model then re-reads and retries). Course-demonstrated (CTX-B6). → AC9
- **R9 — Trace rows.** A run's trace alternates model turns and tool results: each model turn is one row naming the tools it calls and the sections each call fills; each tool result is one row with its output whitespace-collapsed and cut to 220 characters plus an ellipsis; the closing model message is one row. Course-demonstrated (CTX-A). → AC3

**Verification loop**

- **R10 — Rubric-graded, feedback-driven revision.** After the agent finishes, a grader scores each rubric criterion pass/fail. The default rubric has three criteria in this fixed order: **completeness** (every clause of the requirement, as R1 defines a clause, is addressed somewhere in the analysis), **clarity** (every Ambiguities bullet has an indented `Resolved by:` line naming the fact or decision that would settle it), **depth** (every Ambiguities bullet has an indented `Edge case:` line naming a concrete production failure). The loop ends at the first of: (i) a pass in which every criterion passes — run status `satisfied` (all must pass in the *same* pass); (ii) a pass whose result is `failed` — status `failed`, no send-back, since revising cannot repair the rubric; (iii) a pass recorded as `grader_error` (R12) — status `grader_error`; (iv) a `needs_revision` pass when the budget is spent — status `max_iterations_reached`. Otherwise each failing criterion's `gap` is sent back to the agent as feedback and it revises, up to the **revision budget** (`REVIEW_REVISION_BUDGET`, §5) — **3** send-backs by default (a budget of N allows at most N+1 grading passes) (Lesson 5 narration and notebook `MAX_RUBRIC_ITERATIONS`; the batch runner uses the same 3) — *contradicted lever*: the course's shipped automation used 2; the lever-value rule picks the introducing lesson's narrated value, 3; budget 0 is the bare agent loop (D2 option 2). **Post-build lever** (§6 Ask First). The grader's result is one of `satisfied | needs_revision | failed` (`failed` = the rubric is malformed or impossible to evaluate, e.g. a criterion line with no text after its name); a run whose budget runs out ends `max_iterations_reached` even though its last pass says `needs_revision`. The rubric is read from `REVIEW_RUBRIC_PATH` (§5). Course-demonstrated (CTX-A, CTX-C3). → AC10, AC11, AC13, AC14, AC20, AC34, AC37
- **R11 — The grader judges the finished file, never the conversation.** Whatever D1 realization is chosen, every verdict is computed from `/analysis.md` as it stands when the agent finishes: a model grader (D1's Default) is given a read tool and must read the file through it before judging; a code checker (D1 options 2–3) reads the file directly. A criterion passes only on text quoted verbatim from the file; labelled-line criteria are applied literally (a different label is a different line); every item is checked where a criterion asks for coverage. A transcript that "reads as if" done is never evidence. Course-demonstrated (CTX-B4; the course's grader instructions exist because the unconstrained grader passed criteria the file did not satisfy). → AC10, AC37
- **R12 — Grader failures are recorded, not averaged away.** If the grader errors or returns something unparseable, the pass is recorded with `result: grader_error` and no criteria, the loop ends there (R10 (iii)) with run status `grader_error` while the run, its trace and its report version are still recorded, and such runs are excluded from first-attempt denominators and counted in `grader_errors` (R16). Course-demonstrated (CTX-B7). → AC14
- **R13 — Event triggers run the verified loop and write back where the agent owns the page.** *(a)* Creating a ticket linked to a requirement page runs the loop at once (synchronously in the request); *(b)* saving a new version of a requirement page re-runs it for every ticket linked to that page whose status is not `Done`; *(c)* "re-run now" on an open ticket re-runs it; a `Done` ticket is never re-triggered. Each run: fetches the page's *current* version, runs D2's default, appends the result as a **new version of the agent-owned report page** titled `Analysis Report — <key>` (created on first run, author `Requirements Analysis Agent (bot)`) whose body starts with a banner stating the ticket, the requirement version analyzed, the verification status and the number of grading passes, followed by the analysis; records an `AnalysisRun` linking requirement version and report version; sets the ticket to `Analysis Ready` with `last_analyzed_version` and `last_run_id`; and adds a bot comment naming the status, the version and the report page. The requirement page itself is never written by a run (it is the source of truth). Course-demonstrated (CTX-A, CTX-C4, CTX-C6). → AC12, AC13, AC15, AC16
- **R14 — A human, never the agent, marks a ticket Done.** Only the close action changes status to `Done`; no run does. Course-demonstrated (CTX-C6). → AC16
- **R15 — Show what changed between runs two ways.** A ticket with two or more runs shows a "what changed since the previous run" table (requirement version analyzed, verification status, and bullet counts per list section, previous vs latest); the report page's version history offers a unified text diff between any two versions, with the two runs' status and counts beside it. Both are shown because counts often look alike while the text changed completely. Course-demonstrated (CTX-C7). → AC17

**Learning loop**

- **R16 — A batch is every document once, under one instructions version, with everything kept.** Running a batch with a `label` reviews every fixture document in sorted order under the verified loop (revision budget as R10, fetch failures 0, turn cap 40), each in its own workspace seeded from the instructions under test; snapshots that instructions file beside the batch; writes one `RunRecord` per document (every message untruncated — including the grader's injected feedback — every grading pass with the file as it stood, the final file, the instructions, the status); and writes a `BatchSummary` whose first-attempt pass rate per criterion (matched by position) is the systemic-failure signal, denominators being graded runs only. Course-demonstrated (CTX-A, CTX-C5). → AC18, AC19, AC20, AC26
- **R17 — The analyst reads the batch and proposes; it cannot write evidence or apply.** The analyst is an agent rooted at the run-history folder with list/read/search tools and exactly one writable path, `/proposal.md`; everything else is write-denied. It starts from the batch summary, reads into the runs for evidence and the instructions snapshot to avoid repeating what is there, and returns a `HarnessChange` (§3.4) whose `evidence` entries each read `<run file stem>: <quote>` — the stem names the `RunRecord` file (e.g. `run_01_01_inventory_reorder_alerts`) and the quote is copied verbatim from that record — and whose `change` is literal text ready to insert. Discipline it is instructed in: a criterion failing in most runs is a property of the agent; a problem in one run out of five is not a pattern and goes under `rejected`. The proposal text and the structured change are saved beside the batch as `proposal_<label>.md` / `proposal_<label>.json`. Analyst turn cap 40. Course-demonstrated (CTX-A, CTX-C5). → AC21, AC22 (live)
- **R18 — Apply only after human approval, only to the prompt, in plain code.** A proposal is applied to the live instructions only through an explicit approval action; the insertion is deterministic (the change text appended at the end of the named section, before the next heading of the same or shallower depth, blank-line separated; error if the section is missing); a proposal whose `target` is not `prompt` is shown and **never applied automatically**. Course-demonstrated (CTX-C5; Lesson 2: harness changes "flow through systematic human review"). → AC23, AC24, AC25
- **R19 — Validate the change by re-running and comparing.** After applying, re-run the batch under the new instructions and compare first-attempt passes per criterion: `regression` if any criterion lost passes; else `success` if the after-batch needed no revisions; else `partial` if any criterion gained; else `no effect`. The comparison also reports attempts (total grading passes) and an input/output token estimate per batch (per model message: input = instructions size + 120 + running history; output = the message's size; tokens by a tokenizer when available, else characters ÷ 4). USD cost is out of scope (§1 item 9). Course-demonstrated (CTX-C5; Lesson 2's "make sure there are no regressions"). → AC26, AC27, AC35

**Environment and platform**

- **R20 — Models come from the platform; keys are read, never asked for.** `[environment]` Each model role reads its id from `REVIEW_AGENT_MODEL`, `REVIEW_GRADER_MODEL`, `REVIEW_ANALYST_MODEL`; the provider client reads exactly `OPENAI_API_KEY` and `OPENAI_BASE_URL` and sends every request to that base URL; `ANTHROPIC_API_KEY` / `ANTHROPIC_BASE_URL` are present and never read; no key or model id is hardcoded, and the app never asks the person for one. The literal value `scripted` selects the §5 stand-in for that role; the offline suite runs with every role `scripted` and reaches no network. → AC30, AC31, AC36
- **R21 — The store survives restarts.** `[environment]`-derived from the environment dimension's invariant: pages, tickets, runs and run history are on disk under `data/` and `run_history/` and are intact after the server process restarts; the seed scenario is written only when its file is missing. Project hardening on top of the course (which seeded on first import but never asserted durability). → AC1, AC29
- **R22 — Relative URLs only.** `[environment]` Every URL the page requests or links to is relative (`api/tickets`, never `/api/tickets`), because the preview is reverse-proxied under a path prefix. → AC32
- **R23 — One server, port 4000, HTTP only.** `[environment]` The page and the API are served by one process bound to `0.0.0.0:4000`; no WebSocket upgrades; long runs return over plain HTTP (streaming allowed). → AC28
- **R24 — The workspace-root `AGENTS.md` is never written.** `[environment]` The IDE rewrites the workspace-root file of that name at every boot, so nothing is ever authored there; the app's instructions file is `harness/memories/AGENTS.md` (§2, R5). → AC33

## 5. Acceptance Criteria

### Fixture corpus (declared before use; the build agent MUST NOT modify fixtures to make a test pass)

All fixtures live under `fixtures/`. Every fact below is authored for this spec; none is course data.

- `fixtures/seed_pages.json` — one requirement page: id `page-shared-document-links`, title `Shared Document Links — Requirements`, version 1 by `Dana (Product Manager)`, body of exactly three clauses separated by blank lines: `Users shall be able to share a document by link.` / `Shared links should expire after a reasonable time.` / `The system should support common permission levels.` Its fetch result (R1) is therefore `REQUIREMENT: Shared Document Links — Requirements`, a blank line, and those three lines with their blank separators — three clauses.
- `fixtures/seed_tickets.json` — one ticket: key `REQ-210`, title `Review requirements: Shared Document Links`, description `Please review the attached requirements doc for ambiguity before implementation kicks off.`, linked page `page-shared-document-links`, assignee `Jordan (Eng Lead)`, status `Open`, no comments, `last_analyzed_version` and `last_run_id` null.
- `fixtures/requirement_docs/` — five batch documents, each a first line `REQUIREMENT: <title>` followed by clauses separated by blank lines:
  - `01_inventory_reorder_alerts.md` — `Inventory Reorder Alerts`: `Low-stock items shall trigger a reorder alert.` / `Alerts must reach the right buyer quickly.` / `The threshold should be sensible for each product.` / `Alerts for the same item should not repeat too often.`
  - `02_customer_export_scheduler.md` — `Customer Export Scheduler`: `Users shall be able to schedule recurring data exports.` / `Exports must complete within a reasonable window.` / `Large exports should be handled gracefully.` / `Users must be notified when an export fails.`
  - `03_meeting_room_booking.md` — `Meeting Room Booking`: `Employees shall book meeting rooms from the directory.` / `Double bookings must be prevented.` / `Recurring bookings should be supported where appropriate.` / `Rooms should be released if a meeting does not start on time.`
  - `04_invoice_reminder_emails.md` — `Invoice Reminder Emails`: `Overdue invoices shall trigger reminder emails.` / `Reminders must be spaced out appropriately.` / `The system should stop reminding after a reasonable number of attempts.` / `Customers must be able to opt out easily.`
  - `05_support_ticket_auto_tagging.md` — `Support Ticket Auto-Tagging`: `New support tickets shall be tagged automatically.` / `Tags must be accurate enough to route tickets correctly.` / `Ambiguous tickets should be flagged for a human.` / `Tagging rules must remain manageable as volume grows.`
- `fixtures/rubric.md` — the three-criterion rubric of R10, one `- <name>: <criterion>` line each, in the order completeness, clarity, depth.
- `fixtures/rubric_malformed.md` — three criterion lines `- completeness:`, `- clarity:`, `- depth:` with nothing after the colon (a malformed rubric for AC20, selected with `REVIEW_RUBRIC_PATH`).
- `fixtures/instructions_v1.md` — the baseline instructions file the live `harness/memories/AGENTS.md` is initialized from on fresh init. The build agent authors its text to carry R1–R2's procedure and R10's review guidance as behavior (not copied from anywhere), under these exact headings: `# Requirements Review Agent`, `## Procedure`, `## Review guidance` with `### Confirmed facts`, `### Ambiguities`, `### Clarification questions`, `### Assumptions`. **It MUST NOT contain the strings `Resolved by:` or `Edge case:`** — that absence is the planted systemic failure the learning loop finds.
- `fixtures/expected_change.json` — a `HarnessChange` with `target: "prompt"`, `section: "### Ambiguities"`, `evidence` = five strings, one per batch document in order, each in R17's `<run file stem>: <quote>` form — `run_01_01_inventory_reorder_alerts: missing indented 'Resolved by:' line under every Ambiguities bullet`, and likewise for `run_02_02_customer_export_scheduler`, `run_03_03_meeting_room_booking`, `run_04_04_invoice_reminder_emails`, `run_05_05_support_ticket_auto_tagging` (the quote is the scripted grader's clarity gap, verbatim in each record's grading pass 1), `recurrence: "5/5 runs"`, `rejected: []`, and `change` = the text: `For every ambiguity bullet, add two indented labelled lines after the Reason line: an indented "Resolved by:" line naming the fact or decision that would settle it, and an indented "Edge case:" line naming a concrete production failure if it stays unresolved.`
- `fixtures/scripted_model.py` — **the scripted model stand-in** (RR1): a fake chat model, registered with the description "scripted stand-in for the platform model — not a real LLM", selected per role by the literal `scripted` (R20). Declared behavior:
  - **Agent role**, mode `SCRIPTED_AGENT_MODE=complete` (the mode used unless a criterion says otherwise): turn 1 calls `fetch_requirement` with the key named in the opening message; on any tool result beginning with `Error:` (R3) it repeats the identical call; on success it writes the skeleton with one Confirmed Facts bullet per clause (clauses as R1 defines them, each quoted verbatim); then edits Ambiguities with one bullet per clause (bold quoted clause, indented `Reason: the clause names no measurable value or standard`), **adding the indented `Resolved by: a named limit or standard for this clause` and `Edge case: the feature ships with this undefined and fails in production` lines only if the loaded instructions contain the literal `Resolved by:`**; then Clarification Questions (one per clause), Assumptions (one per clause), Summary (two sentences), then the message `Review complete.` On receiving grader feedback it re-edits the Ambiguities section to add the two labelled lines under every bullet, then ends with `Revision complete.` Mode `no_labels`: identical, but never adds the labelled lines, even after feedback. Mode `claims_labels` (the planted CTX-B4 instance): identical to `no_labels`, but its closing message is `Review complete. Every Ambiguities bullet now has an indented Resolved by: line and an indented Edge case: line.` and, after feedback, `Revision complete. Added Resolved by: and Edge case: under every Ambiguities bullet.` — the conversation claims the labels while the file never carries them. Mode `stall`: repeats the fetch call on every turn forever.
  - **Grader role**, mode `SCRIPTED_GRADER_MODE=literal` (the mode used unless a criterion says otherwise): first calls `read_file` on `/analysis.md`; returns `failed`, with every criterion unpassed and the gap `criterion has no text`, if any rubric criterion line has no text after its name; otherwise, in rubric order, judging only the file text its `read_file` returned: completeness passes iff every clause (R1) of the successful fetch result — the tool result in the transcript beginning `REQUIREMENT:` — appears verbatim in the file; clarity passes iff every Ambiguities bullet in the file has an indented `Resolved by:` line; depth likewise for `Edge case:`; result `satisfied` iff all pass, else `needs_revision` with a gap per failing criterion of the form `missing indented '<label>' line under every Ambiguities bullet`. Mode `error`: raises an exception on every call.
  - **Analyst role**: reads `/<label>/summary.json` and `/<label>/AGENTS.md`, writes `/proposal.md` with the sections `## Summary signal`, `## Evidence across runs`, `## Proposed insertion`, `## Rejected observations`, and returns exactly `fixtures/expected_change.json`.
- `fixtures/planted_summaries.json` — four `BatchSummary` objects for AC35, labelled `p_base` (completeness 5, clarity 3, depth 3 of 5; `revisions_needed` 2), `p_regress` (5, 2, 3; 3), `p_partial` (5, 5, 3; 2) and `p_same` (identical to `p_base`); the test copies each into `run_history/<label>/summary.json` with no run files.
- `fixtures/stub_provider.py` — a minimal local HTTP server that accepts `POST <base>/chat/completions`, records the request's `Authorization` header and path, and answers every request with the same canned completion — the text `Stub reply.` and no tool calls (for AC30 only; declared stand-in, not a model).
- `fixtures/ambiguous_edit.md` — the planted CTX-B6 instance: exactly nine lines — `# Requirements Analysis` / (blank) / `## Ambiguities` / (blank) / `- first` / (blank) / `## Ambiguities` / (blank) / `- second`. The test copies it into a run workspace as `/analysis.md` (AC9).
- `fixtures/nonprompt_changes.json` — three `HarnessChange` objects, each equal to `expected_change.json` except `target`: `tool`, `grader`, `configuration` in that order (AC24).
- `fixtures/prefix_proxy.py` — a minimal local HTTP reverse proxy, a declared stand-in for the lab's preview proxy: it listens on a loopback port, forwards every request under `/preview/abc/` to `http://127.0.0.1:4000/` with that prefix stripped, and answers `404` for any path outside the prefix (AC32).
- `fixtures/network_guard.py` — a pytest plugin that, while active, makes every socket connection to a non-loopback address raise and records each attempt (AC36).

**Test hooks** (environment variables read when each run starts, so a test may set them per criterion; unset = the course-derived value the rule states). The §6 Ask-First entries on these values govern the hooks too.

- `REVIEW_TRIGGER_MODE` — `verified` (unset: D2's Default, the verified loop) or `bare` (D2 option 2: the bare agent loop, revision budget 0, no grading passes). Governs event-triggered and manual runs; a batch always runs the verified loop (R16).
- `REVIEW_REVISION_BUDGET` — integer; unset = 3 (R10).
- `REVIEW_TURN_CAP` — integer; unset = R4's value for the run's form: 40 verified, 12 bare.
- `REVIEW_FETCH_FAILURES` — integer; unset = 2 (R3) for event-triggered and manual runs; a batch always uses 0 (R16).
- `REVIEW_RUBRIC_PATH` — path; unset = `fixtures/rubric.md` (R10). Governs every run, batches included.
- `SCRIPTED_AGENT_MODE` / `SCRIPTED_GRADER_MODE` — the stand-in's modes above; unset = `complete` / `literal`.

**Planted states** (created by the test, never by the app):

- `stale_workspace` (the planted CTX-B5 instance, AC6): before a new run is prepared, the test writes `harness/runs/deadbeef/analysis.md` (a previous run's leftover workspace) containing the two lines `# Requirements Analysis` and `STALE-ANALYSIS-MARKER`, and `harness/runs/outside.txt` — the parent of every run workspace, reached from inside one as `/../outside.txt` — containing `OUTSIDE-MARKER`.
- `missing_instructions` (the planted CTX-B3 instance, AC7): a run workspace prepared normally, from which the test deletes `memories/AGENTS.md` before a run is built against it.
- The fetch-failure instance (the planted CTX-B1 instance, AC4): `REQ-210` fetched with `REVIEW_FETCH_FAILURES` unset (2), which yields R3's 503 string, then its timeout string, then the document.
- `nonprompt_proposals` (AC24): the test saves the stored `run_history/proposal_v1.json`, writes each object of `fixtures/nonprompt_changes.json` over it in turn, and after the third restores the saved file byte for byte.

### Criteria (Given / When / Then)

Offline unless tagged `live`. "Fresh init" = empty `data/`, empty `run_history/`, `harness/memories/AGENTS.md` absent, every model role `scripted`, every test hook unset. "Seed state" = the state AC1 leaves (fresh init, then server start: the seed page at version 1, `REQ-210` open with no runs). "After AC<n>" = the state AC<n> leaves, reached by running AC<n>'s chain from its own start; two criteria after the same AC<n> each start from that state. A test hook or scripted mode a Given does not name is unset.

| # | Given | When | Then | Rules |
|---|---|---|---|---|
| AC1 | Fresh init | The server starts | `data/pages.json` holds exactly the seed page, `data/tickets.json` exactly `REQ-210`, `data/analysis_runs.json` is `[]`, `run_history/` exists and is empty, and `harness/memories/AGENTS.md` equals `fixtures/instructions_v1.md` byte for byte | (R21) |
| AC2 | Seed state, agent mode `complete`, `REVIEW_FETCH_FAILURES=0` | A verified run is triggered for `REQ-210` | The run's first model turn calls `fetch_requirement` with `REQ-210` and no message in the run contains the requirement text before that tool's result; the final file (the report version's body after its banner) matches §3.1 — five headings in order, a non-empty two-or-three-sentence Summary — and the run's `AnalysisRun` (`GET api/runs/{run_id}`) has `counts` = 3/3/3/3 (one bullet per clause of the three-clause seed page) and `complete` true | (R1, R2) |
| AC3 | The run of AC2 | Its `AnalysisRun` is read (`GET api/runs/{run_id}`) | `stage_order` = `["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"]` (the revision edit after grader feedback re-fills Ambiguities and does not append); the trace alternates `Model reasoning` / `Tool` rows, the first model row names `fetch_requirement`, the write row names `write_file: Confirmed Facts`, and every `detail` is ≤ 221 characters | (R2, R9) |
| AC4 | Seed state, `REVIEW_FETCH_FAILURES` unset (2) — the planted fetch-failure instance | A verified run is triggered for `REQ-210` | The trace's first three tool rows are, in order, a row whose `detail` begins `Error: 503 Service Unavailable`, a row whose `detail` begins `Error: request timed out after 10s`, and the document (its `detail` begins `REQUIREMENT: Shared Document Links — Requirements`); both error rows are followed by a model row calling `fetch_requirement` with `REQ-210` again; and `GET api/config` reports `simulated_fetch_failures: 2` | (R3) |
| AC5 | A run workspace with `/memories/AGENTS.md` present | The agent's `write_file` or `edit_file` tool is invoked on `/memories/AGENTS.md` (direct tool invocation in the test) | The call returns an error naming a denied write and the file is unchanged | (R5) |
| AC6 | Seed state plus planted state `stale_workspace` | A new run is prepared in a fresh workspace and the agent's `read_file` tool is invoked on `/../outside.txt` | The new workspace contains no `/analysis.md` before the model's first turn; the probe read returns an error (unreachable path) and its result does not contain `OUTSIDE-MARKER`; after the run completes, its workspace directory no longer exists while its `AnalysisRun` is on disk | (R7) |
| AC7 | Planted state `missing_instructions` | A run is built against that workspace | An error is raised naming the missing instructions file, and the scripted model records zero calls | (R6) |
| AC8 | Seed state, agent mode `stall`, `REVIEW_TRIGGER_MODE=bare` (D2 option 2), `REVIEW_TURN_CAP` unset (R4's bare-loop value, 12) | A run is triggered for `REQ-210` | The run ends with `status: "turn_limit_reached"`, `turns` = 12, the last trace row's action is `Stops: turn limit of 12 reached`, and the report page's new version carries that status in its banner | (R4) |
| AC9 | A run workspace whose `/analysis.md` is a copy of `fixtures/ambiguous_edit.md` (the planted CTX-B6 instance) | `edit_file` is invoked with `old_string: "## Ambiguities"` | It returns an error about a non-unique match and the file is byte-identical to the fixture; a second call with the absent `old_string: "## Not A Heading"` also errors with the file unchanged | (R8) |
| AC10 | Seed state, instructions v1 (no labels), agent `complete`, grader `literal`, `REVIEW_REVISION_BUDGET` unset (3); D1 at its Default (option 1, the model-driven grader — this criterion exercises that realization) | A verified run is triggered for `REQ-210` | Grading pass 1 has `result: needs_revision` with completeness passed and clarity and depth failed, each failing criterion carrying a non-empty `gap`; the grader's first tool call in that pass is `read_file` on `/analysis.md`; pass 2 has `result: satisfied` with all three passed; run `status` = `satisfied`; the final file has `Resolved by:` and `Edge case:` lines under all three Ambiguities bullets | (R10, R11) |
| AC11 | As AC10 but agent mode `no_labels` | A verified run is triggered | Exactly 4 grading passes are recorded (initial + 3 send-backs), every one `needs_revision`, and the run `status` is `max_iterations_reached` | (R10) |
| AC12 | Seed state | `POST api/tickets` with title `Review requirements: Link expiry`, description `Check the link-expiry wording.`, linked page `page-shared-document-links`, and no assignee | The response ticket key is `REQ-211` with assignee `Unassigned`; one `AnalysisRun` exists for it with `requirement_version: 1`, `grading` non-empty and `status: "satisfied"`; a page `page-analysis-req-211` of kind `analysis_report`, title `Analysis Report — REQ-211`, has exactly one version authored by `Requirements Analysis Agent (bot)` whose body begins with a banner naming `REQ-211`, `version 1`, `satisfied` and `2 grading pass(es)` before `# Requirements Analysis`; the ticket is `Analysis Ready` with `last_analyzed_version: 1`, `last_run_id` = that run, and one bot comment naming `satisfied`, version 1 and the report title | (R1, R13) |
| AC13 | After AC12 | `POST api/pages/page-shared-document-links/versions` with a body equal to the version 1 body, a blank line, and the fourth clause `Links shall expire after 14 days.` | The response has `version: 2` and `retriggered` = `["REQ-210", "REQ-211"]` (both open and linked); each ticket gains a new run with `requirement_version: 2`, `status: "satisfied"` and exactly 2 grading passes (pass 1 `needs_revision` with completeness passed and clarity and depth failed); the requirement page has exactly 2 versions, and its version 1 body is unchanged; `page-analysis-req-210` is created with exactly 1 version and `page-analysis-req-211` now has exactly 2 versions | (R10, R13) |
| AC14 | Seed state, grader mode `error` | A verified run is triggered for `REQ-210` | The run has exactly one grading pass, with `result: "grader_error"` and `criteria: []` (the loop ended there), the run `status` is `grader_error`, and the run and report version are still recorded | (R10, R12) |
| AC15 | Seed state | `POST api/tickets/REQ-210/rerun` twice | The ticket has exactly two runs with distinct 8-hex ids, the report page has exactly two versions, and `GET api/tickets/REQ-210` returns `previous_run` and `latest_run` as those two runs in order | (R13) |
| AC16 | After AC13 | `POST api/tickets/REQ-211/close`, then `POST api/pages/page-shared-document-links/versions` with any new body | The ticket is `Done`; the save's `retriggered` list is `["REQ-210"]` and does not contain `REQ-211`; `REQ-211`'s run count is unchanged (2); `POST api/tickets/REQ-211/rerun` returns `409`; the close action added no bot comment; and `REQ-210`, which no person closed, is `Analysis Ready` after its re-triggered run — no run ever produces `Done` | (R13, R14) |
| AC17 | After AC13 | `GET api/tickets/REQ-211` and `GET api/pages/page-analysis-req-211/compare?a=1&b=2` | The ticket response's `previous_run.requirement_version` is 1 and `latest_run.requirement_version` is 2, with `counts` for all four list sections on both; the compare response's `diff` is a non-empty unified diff (first lines `--- version 1` / `+++ version 2`) and `run_a`/`run_b` are the two runs with their statuses | (R15) |
| AC18 | Fresh init (instructions v1) | `POST api/history/v1/run` with `instructions: "baseline"` | `run_history/v1/` contains `AGENTS.md` equal to the live instructions, `run_01_01_inventory_reorder_alerts.json` … `run_05_05_support_ticket_auto_tagging.json`, and `summary.json`; each `RunRecord` validates against §3.4, has ≥ 2 grading passes, `messages` containing a message whose content includes `missing indented 'Resolved by:' line`, and `instructions` equal to the snapshot | (R16) |
| AC19 | After AC18 | `GET api/history/v1/summary` | `{runs: 5, graded: 5, grader_errors: 0, first_attempt: {completeness: {passed: 5, total: 5, pass_rate: 1.0}, clarity: {passed: 0, total: 5, pass_rate: 0.0}, depth: {passed: 0, total: 5, pass_rate: 0.0}}, revisions_needed: 5, documents: [the five doc names in order]}` | (R16) |
| AC20 | Fresh init, `REVIEW_RUBRIC_PATH=fixtures/rubric_malformed.md`, grader `literal` | `POST api/history/bad/run` with `instructions: "baseline"` | Every run's single grading pass (the loop ends on `failed`, R10) has `result: "failed"` with three criteria each `passed: false` and gap `criterion has no text`; run `status` = `failed`; the summary reports `graded: 5`, `grader_errors: 0`, every criterion `passed: 0`, `revisions_needed: 5` | (R10, R16) |
| AC21 | After AC18 | `POST api/history/v1/propose` | The response `change` equals `fixtures/expected_change.json`; `run_history/proposal_v1.md` and `proposal_v1.json` exist; the analyst's recorded tool calls include a read of `/v1/summary.json` and `/v1/AGENTS.md` and exactly one write, to `/proposal.md`; a write attempt by the analyst's tools to `/v1/summary.json` (direct tool invocation) errors and leaves the file unchanged | (R17) |
| AC22 `live` | A real platform model for the analyst role, after AC18 | `POST api/history/v1/propose` | The returned `HarnessChange` validates against §3.4 with `target: "prompt"`, `section: "### Ambiguities"`, every `evidence` string in R17's `<run file stem>: <quote>` form and ≥ 1 of them with a quote that occurs verbatim in the v1 `RunRecord` its stem names, and a `change` containing both `Resolved by:` and `Edge case:` | (R17) |
| AC23 | After AC21 | `POST api/history/v1/apply` with `{approved: false}`, and with no body | Both return `409`; `harness/memories/AGENTS.md` is byte-identical to `fixtures/instructions_v1.md` | (R18) |
| AC24 | After AC23, planted state `nonprompt_proposals` (targets `tool`, `grader`, `configuration` in turn) | `POST api/history/v1/apply` with `{approved: true}` after each plant | Each returns `422`; the instructions are byte-identical to `fixtures/instructions_v1.md` after all three; the stored proposal is restored afterwards (runs before AC25) | (R18) |
| AC25 | After AC24 (stored proposal restored, chain AC18 → AC21 → AC23 → AC24) | `POST api/history/v1/apply` with `{approved: true}` | `harness/memories/AGENTS.md` now contains the expected change's text as the last paragraph of the `### Ambiguities` section (immediately before the `### Clarification questions` heading, blank-line separated), everything else byte-identical to v1; the response `diff` shows only added lines | (R18) |
| AC26 | After AC25 | `POST api/history/v2/run` with `instructions: "baseline"` (the live file, which now carries the applied change) then `GET api/history/v2/summary` | `first_attempt` is `passed: 5, total: 5, pass_rate: 1.0` for all three criteria, `revisions_needed: 0`, every run has exactly one grading pass `satisfied`, and `run_history/v2/AGENTS.md` contains `Resolved by:` | (R16, R19) |
| AC27 | After AC26 | `GET api/history/compare?before=v1&after=v2` | `verdict: "success"`, `criteria` = `{completeness: [5,5], clarity: [0,5], depth: [0,5]}`, `revisions_needed: [5, 0]`, `attempts: [10, 5]`, `improved: ["clarity", "depth"]`, `regressed: []`, and both token arrays hold positive integers | (R19) |
| AC28 | The app started by the §7 command | `GET /` (the page) and `GET api/config` on `http://127.0.0.1:4000` | Both return 200; the page is HTML; nothing listens on any other port opened by the app | (R23) |
| AC29 | Combined state: from fresh init, on one server and store, the chain AC12 → AC13, then the chain AC18 → AC21 → AC23 → AC24 → AC25 (the ticket chain writes `data/`; the learning chain writes `run_history/` and the instructions) | The server process is stopped and started again | `GET api/tickets`, `GET api/pages`, `GET api/history` and `GET api/instructions` return exactly the pre-restart data (same tickets, pages with all versions, runs, batch labels, instructions text) | (R21) |
| AC30 | Seed state, `OPENAI_API_KEY=test-key-123`, `OPENAI_BASE_URL` = the `stub_provider.py` address, `REVIEW_AGENT_MODEL=stubbed-model`, grader/analyst `scripted`, `REVIEW_TRIGGER_MODE=bare` (D2 option 2), `ANTHROPIC_API_KEY=must-not-be-read` | A run is triggered for `REQ-210` | The stub recorded ≥ 1 request on its `chat/completions` path with `Authorization: Bearer test-key-123`; the application source — every `.py`, `.html`, `.js` and `.css` file in the app folder outside `tests/` and `.venv/` (the test suite and the installed packages are excluded) — contains no occurrence of `test-key-123` and no occurrence of the token `ANTHROPIC`; the run ends without the test being asked anything, with `grading: []` and `status: "incomplete"` (the stub's reply has no tool calls, so the model finished with no analysis written) | (R4, R20) |
| AC31 | `REVIEW_AGENT_MODEL=scripted`, `REVIEW_GRADER_MODEL=scripted`, `REVIEW_ANALYST_MODEL=role-c` | `GET api/config` | `models` = `{agent: "scripted", grader: "scripted", analyst: "role-c"}` — each role read from its own variable | (R20) |
| AC32 | The served page's HTML and scripts | Every `href`, `src`, `action` and every URL passed to `fetch` is extracted | None starts with `/` or with `http` (all relative); and `GET api/tickets` requested under a path prefix (via `fixtures/prefix_proxy.py` mounting the app at `/preview/abc/`) still resolves from the page | (R22) |
| AC33 | The build folder | The workspace root is listed and the app's write paths are inspected | No file named `AGENTS.md` at the workspace root was created or modified by the build or by any run; the only `AGENTS.md` files are `harness/memories/AGENTS.md`, per-run `harness/runs/<id>/memories/AGENTS.md`, and `run_history/<label>/AGENTS.md` | (R24) |
| AC34 | Seed state, `REVIEW_TRIGGER_MODE=bare` (D2 option 2), agent `complete`, `REVIEW_FETCH_FAILURES=0` | A run is triggered for `REQ-210` | The run has `grading: []`, `status: "finished"`, `turns` ≤ 12, a complete analysis (`AnalysisRun.complete` true), and its report banner states the status with `0 grading pass(es)` | (R4, R10) |
| AC35 | `fixtures/planted_summaries.json` copied in as four batches | `GET api/history/compare` for `before=p_base` with `after=p_regress`, `after=p_partial`, and `after=p_same` | Verdicts are `regression` (with `regressed: ["clarity"]`), `partial` (with `improved: ["clarity"]`, `regressed: []`), and `no effect` (both lists empty), respectively; each response validates against §3.4 `Comparison` | (R19) |
| AC36 | Fresh init, every model role `scripted`, `OPENAI_API_KEY` unset, `OPENAI_BASE_URL=http://127.0.0.1:9` (a closed port), `fixtures/network_guard.py` active | Every other offline criterion (AC1–AC21, AC23–AC35, AC37) runs in one pytest session | All of them pass; the guard recorded zero connection attempts to a non-loopback address; and the scripted model recorded calls in all three roles — agent, grader and analyst — so the real pipeline (tool calls, grader, trigger, batch runner, analyst's structured proposal, apply step, comparison) drove the stand-in end to end (RR1's invariant) | (R20) |
| AC37 | Seed state, agent mode `claims_labels` (the planted CTX-B4 instance), grader `literal`, D1 at its Default | A verified run is triggered for `REQ-210` | The agent's first closing message (`Review complete. Every Ambiguities bullet now has …`) contains both `Resolved by:` and `Edge case:`, while no grading pass's `analysis_markdown` contains either; every one of the 4 grading passes has clarity and depth `passed: false`; the run `status` is `max_iterations_reached` — the conversation's claim never passes a criterion | (R10, R11) |

Reciprocity index — rule → criteria: R1 → AC2, AC12 · R2 → AC2, AC3 · R3 → AC4 · R4 → AC8, AC30, AC34 · R5 → AC5 · R6 → AC7 · R7 → AC6 · R8 → AC9 · R9 → AC3 · R10 → AC10, AC11, AC13, AC14, AC20, AC34, AC37 · R11 → AC10, AC37 · R12 → AC14 · R13 → AC12, AC13, AC15, AC16 · R14 → AC16 · R15 → AC17 · R16 → AC18, AC19, AC20, AC26 · R17 → AC21, AC22 · R18 → AC23, AC24, AC25 · R19 → AC26, AC27, AC35 · R20 → AC30, AC31, AC36 · R21 → AC1, AC29 · R22 → AC32 · R23 → AC28 · R24 → AC33.

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the offline suite with every model role set to `scripted` and cite its output per criterion (§7).
- Keep `resolved-decisions.md` current with every resolved row and the "model roles" line; the workspace is the record `[environment]` — a new chat starts with no memory of this one, and the grader sees only what is on disk.
- Read the four key/base-URL variables by their exact names (R20); fall back to the scripted stand-in when a role's variable says so.
- Record every run's trace, grading passes and final file before deleting its workspace (R7, R16).
- Install the course pins into the venv in one early, announced batch (§2).

**Ask First** (derived from the course's spoken trade-offs — each cross-referenced to its row or lever)
- Changing the **model roles** after the checklist is written — the agent's tier, giving the grader a different model than the agent, or running the analyst on the same tier as the agent (CTX-C2; body levers in §2). Changes who judges and who diagnoses without failing any offline criterion.
- Changing the **revision budget** (R10's 3), including to 0, which silently turns every triggered run into the bare agent loop (D2 option 2) and starves the learning loop of first-attempt verdicts.
- Changing the **simulated fetch-failure count** (R3's 2 / batch 0): a count of 0 silently stops exercising the retry behavior in triggered runs.
- Changing the **rubric text or criterion order** (R10): it redefines "done", re-labels the analysis format, and re-keys the summary's positional matching, so every batch becomes incomparable with earlier ones (rework).
- Switching the **grader realization** (D1) after runs exist: feedback text changes shape, so the analyst's evidence from earlier batches no longer matches (rework).
- Switching what a **trigger runs** (D2) after runs exist: graded and ungraded run records become incomparable in the "what changed" table.
- Editing `harness/memories/AGENTS.md` **by hand** outside the approve/apply path: it changes the agent's behavior with no proposal, no evidence and no comparison (R18, R19), and no criterion catches it.
- Re-running a batch under a label that already exists (overwrites evidence the analyst may cite).
- Bypassing or replacing the pinned harness framework for any stage (§2).
- Any `live` run — it costs wall-clock time and is non-deterministic (RR1).

**Never**
- Invent provenance: never attribute to the course anything the Course Context Pack does not carry; never claim a course model id is served by the platform.
- Let the grader pass a criterion from the conversation instead of the file, or let the agent be handed the requirement text directly (R1, R11).
- Apply an analyst proposal without the approval action, or auto-apply a non-prompt target (R18).
- Let a run mark a ticket `Done`, or write into a requirement page (R13, R14).
- Mutate fixtures (anything under `fixtures/`) to make a test pass; mutate `expected_change.json` to match an output.
- Hardcode, log, or commit a key; read the Anthropic variables; ask the person for a key (R20).
- Use a root-absolute URL in the page, open a second port, or use WebSockets (R22, R23).
- Author or modify the workspace-root `AGENTS.md` (R24) `[environment]`.
- Report "should pass" or "looks correct": an unrun test is a failed test.

## 7. Test Plan & Self-Verification

Run from the app folder, in order:

```bash
python3 --version                                   # record in resolved-decisions.md (§2 step 1)
python3 -m venv .venv --system-site-packages && . .venv/bin/activate
pip install -r requirements.txt                     # the §2 pins; one announced batch
export REVIEW_AGENT_MODEL=scripted REVIEW_GRADER_MODEL=scripted REVIEW_ANALYST_MODEL=scripted
python -m pytest tests/test_offline.py -q -rA       # every criterion not tagged live
uvicorn app:app --host 0.0.0.0 --port 4000 &        # background; then AC28 and the preview check
unset REVIEW_AGENT_MODEL REVIEW_GRADER_MODEL REVIEW_ANALYST_MODEL   # use the checklist's platform ids
python -m pytest tests/test_live.py -q -rA -m live  # AC22 and a live smoke run; needs the lab keys
```

Offline run check: the untagged suite must also pass with `OPENAI_API_KEY` unset, `OPENAI_BASE_URL=http://127.0.0.1:9` (a closed port) and `fixtures/network_guard.py` active — AC36, proving no criterion reaches the network (RR1's invariant).

**Reporting duty.** The build agent MUST report results per acceptance criterion — `AC<n>: PASS/FAIL` — each with cited evidence: the pytest node id and its captured output, or the file path and the lines that satisfy it. Write the report to `test-report.md` beside `resolved-decisions.md` `[environment]`. "Should pass", "looks correct" and "not run" are failures.

## Runtime (lab)

Everything in this section is `[environment]` provenance — contributed by the `coding-agent-lab` environment, not by the course.

**Container.** Debian, non-root user, Node 22, Python 3 with venv, `sqlite3`, `git`, build tooling. Preinstalled Python: `fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`; preinstalled Node: `express`, `cors`, `better-sqlite3`, `vite`, `nodemon`. Nothing else. The Python minor version is not stated and tracks the image: run `python3 --version` first, record it, and stop with a report if a course-pinned package refuses it (§2). Create the venv with `--system-site-packages`; the course pin wins inside the venv where a preinstalled copy differs. Outbound network works; every install costs wall-clock time, so batch it early and announce it. Memory is finite and shared with the agent's process; this build loads no local models, so no release-before-load rule is needed.

**Keys and models.** `OPENAI_API_KEY` + `OPENAI_BASE_URL` (read) and `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL` (present, unread), each base URL pointing at the platform proxy. Model ids come from `REVIEW_AGENT_MODEL` / `REVIEW_GRADER_MODEL` / `REVIEW_ANALYST_MODEL`, set by the build agent at checklist time from the platform's set with the "(Recommended)" flag; never probe a listing endpoint, never bake a "current best" name into code.

**Preview.** One server, port 4000, bound to `0.0.0.0`, serving the page and the API; HTTP only (no WebSocket upgrades; streaming works); every in-page URL relative. The course's demo ran on port 5050 with two separately styled surfaces; here both surfaces are sections of one page.

**Workspace.** The workspace is the record: `resolved-decisions.md` and `test-report.md` live at the app root because a new chat starts with no memory and the grader sees only what is on disk. The workspace-root `AGENTS.md` is never authored (the IDE rewrites it at boot); the app's instruction file lives at `harness/memories/AGENTS.md`. Every tool call is visible to the learner; the server runs in the background.

**Environment failure modes** (enforced by the rules and criteria named; never part of CTX-A/CTX-B, which are the course's):

| Symptom | Cause | Fix | Enforced by |
|---|---|---|---|
| The page loads but every API call 404s in the preview while working on `localhost` | A root-absolute URL (`/api/...`) resolved against the IDE, because the preview is reverse-proxied under a path prefix | Relative URLs everywhere | R22, AC32 |
| Live updates never arrive | A WebSocket upgrade, which the proxy does not pass | Plain HTTP polling / reload | R23, AC28 |
| Guidance written to the workspace-root `AGENTS.md` vanishes after a restart | The IDE rewrites that file at every boot | Keep the agent's instructions under `harness/` | R24, AC33 |
| A course-pinned package fails to install | The container's Python minor version differs from the course's 3.12 kernel | Record the version; stop with a report rather than loosening a pin silently | §2 step 1 |
| Decisions or results exist only in chat | A new chat has no memory of the old one | `resolved-decisions.md`, `test-report.md`, run records on disk | §6 Always, §7 |
| The app asks for a key, or reads a variable of its own invention | Guessing at credential names | Read exactly the four named variables | R20, AC30 |

## Course Context Pack (embedded — agent-readable)

Concepts only; no code from the course. Anchors are position-independent.

### CTX-A. The pattern

Four loops nested around one agent, each existing for one reason:

1. **Fetch** — the agent is told a ticket id and must look the requirement up through a tool, because an agent built with no knowledge of any document can review any ticket it is pointed at.
2. **Agent loop** — the model repeatedly acts (a tool call), observes (the result), and decides, until it finishes: it fetches, writes a five-section analysis file skeleton, and fills the remaining sections one edit at a time. The file, not a message, is the deliverable. A turn cap exists only for the case where finishing never comes.
3. **Verification loop** — finishing is not the same as good enough: a grader scores the finished file against a rubric (completeness, clarity, depth), passes everything or sends back a named gap per failing criterion, within a revision budget. It raises reliability and lets a cheaper model handle a harder task.
4. **Event-driven loop** — the agent is run by events where the work already happens (a ticket created, a requirement edited while a ticket is open) instead of by a person opening a notebook; its result is written back as a new version of a page the agent owns, and a human keeps the final say (marking Done).
5. **Learning (hill-climbing) loop** — one run's correction is forgotten tomorrow, so a batch of runs is recorded in full; an analyst agent reads the traces, finds what the agent is corrected on *every* time, proposes one literal change to the agent's instructions; a human approves; the change is applied in code; the batch re-runs and a comparison says whether it worked, regressed, or did nothing. The outer loop makes every inner loop better.

The loops are composable (an event loop may wrap a bare agent loop), and a human may sit at any level: a sensitive tool call, the grader, the artifact, or the harness change.

### CTX-B. Failure-mode catalog

- **CTX-B1 — Transient external failure.** *Symptom:* the fetch tool returns an error ("503 Service Unavailable", "request timed out") instead of the document. *Cause:* external systems fail transiently. *Fix:* the agent repeats the identical call until it succeeds; the failure count is deterministic so a trace reproduces. *Enforced by R3, AC4; planted instance: the §5 fetch-failure instance (`REVIEW_FETCH_FAILURES` at its default 2).*
- **CTX-B2 — Retrying past the point of sense.** *Symptom:* a run never finishes. *Cause:* the normal stop (the model finishing the Summary) never comes. *Fix:* a model-turn cap ends the run, and the stop reason is reported as a turn-limit stop, never as a finished review. *Enforced by R4, AC8.*
- **CTX-B3 — Silent missing instructions.** *Symptom:* a plausible but bad review. *Cause:* the memory loader ignores a missing instructions file, so the agent runs on the system prompt alone. *Fix:* fail loudly before any model call when the file is absent. *Enforced by R6, AC7; planted instance: §5 planted state `missing_instructions`.*
- **CTX-B4 — The grader grades by resemblance.** *Symptom:* criteria pass that the file does not satisfy. *Cause:* the grader is handed the whole conversation and judges from how it reads. *Fix:* require the grader to read the file, quote the satisfying text verbatim, apply labels literally, and check every item. *Enforced by R11, AC10, AC37; planted instance: the scripted agent's `claims_labels` mode (§5), whose conversation claims the labels the file lacks.*
- **CTX-B5 — Stale state between runs.** *Symptom:* the agent skips stages. *Cause:* a completed analysis file from an earlier run is still on disk; two tickets analyzed back to back see each other's leftovers. *Fix:* one fresh workspace per run, stale file removed. *Enforced by R7, AC6; planted instance: §5 planted state `stale_workspace`.*
- **CTX-B6 — Ambiguous edit.** *Symptom:* an edit fails or lands in the wrong place. *Cause:* the target string is absent or not unique. *Fix:* the tool refuses with an error and the model re-reads and retries. *Enforced by R8, AC9; planted instance: `fixtures/ambiguous_edit.md`.*
- **CTX-B7 — Grader error counted as a pass.** *Symptom:* pass rates look better than the evidence. *Cause:* a grader exception recorded as a verdict. *Fix:* record it as `grader_error` with no criteria, exclude it from denominators, report the count. *Enforced by R12, R16, AC14.*
- **CTX-B8 — The same correction every run.** *Symptom:* clarity and depth fail on the first attempt of every document for the same reason. *Cause:* the instructions never ask for the two labelled lines the rubric demands. *Fix:* the learning loop: mine the batch, propose the literal insertion, apply after approval, re-run, compare. *Enforced by R16–R19, AC18–AC27.*
- **CTX-B9 — Improvement that regresses something else.** *Symptom:* one criterion rises while another falls. *Cause:* a harness change adopted without an eval. *Fix:* compare first-attempt passes per criterion before and after; a `regression` verdict is surfaced. *Enforced by R19, AC27, AC35.*

### CTX-C. Decision background

**How to read the provenance notes.** A *litmus branch* is how an argued subject was routed: a **row** (a Ledger decision with options), a **bake-in** (the taught side becomes a business rule and the other side is recorded as the warned-against anti-pattern), or a **lever** (the sides differ only in a value, so the value is a body default and a §6 Ask-First entry). A *lever's value-selection branch* says which rule picked the number: (1) the value the narration states in the lesson that introduces it; (2) the end-to-end application's config; (3) the most frequent value, earliest-taught on ties. A *post-build lever* is a value that may be changed after the build without re-opening the gate. *Stakes* is the test a course contradiction must pass to become a row: would choosing the other side up front change the system's structure, semantics or a guarantee? A *substitution row* is one whose Default replaces the course's own technology with a lighter one; the *heavy bar* says when that is allowed (a realization is heavy only when it needs a credential, a paid account, admin-level setup or special hardware — mere network access is not heavy); *realization tiers* rank candidates: (1) standard library, (2) embedded library, (3) locally served process. *Untakeable* (lab mode) means an option needs a credential the lab does not supply or would make the offline suite wait on a person. The *structural litmus* asks: redraw the architecture diagram after the change — if a box, an arrow, an owner or a guarantee changed, the subject is a row; if only a number inside a box changed, it is not. The *keyed-tool rule*: when a course tool — or the model itself — needs a key, its realization offers the course's real tool, an honestly labelled local stand-in and omission, and the stand-in is the Default when that tool is the only carrier of a taught behavior. *Branch taken* names which dependency-precedence branch decided a heavy-dependency Default: (1) substitute the lightest realization that keeps the Invariant, or (2) keep the course's technology because it is the taught subject. A *realization branch* is the same note on a pinned realization (a §2 entry): whether the course's tool was kept, substituted, or — as with the tracker — was already a stand-in the course itself shipped.

- **CTX-C1 — Build with no document, fetch at run time** (→ R1). The course builds the agent knowing only how to look a ticket up; the document is seeded into the store right before the run, exactly as a real document would already exist in a tracker. The agent's turn-by-turn behavior is identical whether the document came from the seed file or a one-off, because it cannot see which.
- **CTX-C2 — Model tiering** (→ §2 model roles; §6 Ask First). Lesson 2: match model intelligence to task complexity to optimize cost — a cheaper, faster model for simple tasks, a slower, more capable one for complex tasks; the verification loop "keeps those core agent loop cycles on track" and makes cheaper models viable on hard tasks. Lesson 5: the course ran agent and grader on one model while calling a separate grader model "a common production choice". Lesson 7 and the course README: the analyst runs on the more capable model because reading five full traces and finding what recurs "is the one job the cheaper model does unreliably". Litmus: these are levers attached to the model/provider dimension, which the lab resolves; their values are the three role variables.
- **CTX-C3 — Three pass/fail criteria, all in one pass** (→ D1, R10). Each criterion carries its own threshold in its text, so "what done means" lives in the rubric rather than in a numeric threshold. Two of three passing is visibly not enough: every criterion must pass in the same grading pass. The course noticed that the grader reads the file and still judges by resemblance unless forced to quote (CTX-B4). Deterministic graders are the course's other named type (Lesson 2: the docs agent's "links resolve, CI passes").
- **CTX-C4 — The report is a page the agent owns** (→ R13). The requirement page is the source of truth and the agent only reads it; findings go to a separate agent-authored page so the tool's own version history shows every past analysis, who (or what) wrote it, and a diff between any two.
- **CTX-C5 — Propose, approve, apply in code, measure** (→ R16–R19). The harness has four improvable parts — prompt, tools, grader, configuration — and the proposal names all four so a non-prompt proposal is expressible rather than reshaped into a prompt edit; only prompt changes are applied, and only by plain string insertion after approval, so the edit stays reviewable and deterministic. The analyst reads the traces and cannot write them ("an agent able to edit the evidence it is reasoning from is not analyzing anything"). The signal is the first-attempt verdict per criterion, matched by position because the grader paraphrases criterion names differently run to run; a criterion failing in most runs is a property of the agent, one run in five is not a pattern. Confidence to merge comes from the before/after comparison (Lesson 2). The course's committed result: before — completeness 5/5, clarity 0/5, depth 0/5, five revisions; after — 5/5 on all three, none. The committed proposal's one insertion added the two labelled lines under the Ambiguities guidance (seven lines).
- **CTX-C6 — Humans keep the final say** (→ R14, R18; §1 items 8, 15). Lesson 2 names four places for a human: before a sensitive tool call, as the grader, on the artifact before delivery, and on harness changes before deployment. The course built the last two: a human marks Done, a human approves the proposal.
- **CTX-C7 — Counts and diff together** (→ R15). Bullet counts often look similar before and after a requirement edit while the content changed completely; showing the counts table and the full text diff together is the point.
- **CTX-C8 — Instructions as a file the agent reads and never writes** (→ R2, R5, R6). The instructions file is loaded into context at every run start, separates a fixed Procedure from the Review guidance that gets revised, and sits inside the agent's own writable filesystem, so writes there are denied by permission rather than by trust. Stage order is requested, not guaranteed; the run records what actually happened. Lesson 7 notes the learning loop's change could equally live in the system prompt; the course puts it in the instructions file.
- **CTX-C9 — Always-on instructions vs progressive disclosure** (→ §1 item 4). Lesson 3's primer: an always-loaded file costs context on every call so it should stay short and hold only what is always true; skill files publish a one-line description each and are read in full only when the agent decides one applies, so a large library stays cheap. The review agent uses only the always-loaded file; a skill library is a named-not-built exclusion.
- **CTX-C10 — Contradictions resolved as levers** (→ R3, R10; `fetch_requirement`). *Fetch failures:* code default 0 vs narration/notebook text/committed trace 2 → 2 (branch 1, Lesson 4 narration), batch 0 (the batch code's own stated reason). *Revision budget:* notebook and batch runner 3 vs shipped automation 2 → 3 (branch 1, Lesson 5 narration). *Tool name:* the shipped instructions and the tool definition say `fetch_requirement`, two batch snapshots and a slide say `fetch_requirement_from_jira` → `fetch_requirement` (code and the live instructions win). *Instructions file name:* one slide says `Agent.md`; code and narration say `AGENTS.md` → `AGENTS.md`. None passes stakes: each is a value or a name, not a structure.
- **CTX-C11 — Keyed integrations** (→ §1 items 1–3; Environment Resolutions). Slack, Jira and Confluence are "examples of integrations"; the course says to connect the agent to any tool in your workflow, and its shipped code is the simulated tracker precisely so the lesson "runs with no Atlassian account and no API tokens". The automation entry point is the seam a real webhook would call.

**Mined spoken trade-offs and their disposition**

| # | Trade-off (as spoken) | Lesson | Disposition |
|---|---|---|---|
| T1 | Cheaper/faster model for simple tasks vs more capable for complex; optimize cost | 2 | lever §2 model roles (Ask First) |
| T2 | Verification makes cheaper models viable on harder tasks | 2, 5 | lever §2 model roles (Ask First); narrative CTX-C2 |
| T3 | Loops are composable; an event loop need not wrap the verification loop | 2 | row D2 |
| T4 | Triggers can be scheduled or ad hoc/event-driven | 2 | narrative; scheduled → §1 item 5 (named-not-built) |
| T5 | Graders can be deterministic or agentic (LLM as judge) | 2 (slide, narrated lesson) | row D1 |
| T6 | Human input at each loop level (tool call / grader / artifact / harness change) | 2 | bake-in R14, R18; §1 item 8 |
| T7 | Hard to merge harness changes confidently without evals; check for regressions | 2 | bake-in R19 |
| T8 | Hill-climbing improves procedural things (prompts, tools, skills) or memory | 2 | bake-in R18 (prompt target applied; others surfaced); §1 item 6 |
| T9 | Always-loaded instructions cost context every call vs skills by progressive disclosure | 3 | narrative CTX-C9; §1 item 4 |
| T10 | The turn cap is not the normal stop; it matters when retrying stops making sense | 4 | lever R4 (not Ask First: a cap change passes or fails the suite outright) |
| T11 | Same model for agent and grader vs a different grader model ("common production choice") | 5 | lever §2 model roles (Ask First) |
| T12 | Revision budget 3; 0 gives the basic agent loop | 5 | lever R10 (Ask First; cross-ref D2) |
| T13 | Analyst on the more capable model: trace analysis is what the cheaper model does unreliably | 7, README | lever §2 model roles (Ask First) |
| T14 | Event-driven reduces friction; integrations are examples, connect any tool | 6 | narrative CTX-C11; realization row resolved via the Environment Resolutions table |
| T15 | Report on a separate agent-authored page, never into the requirement page | 6 (code README) | bake-in R13 |
| T16 | A human, not the agent, decides when a ticket is Done | 6 (code README) | bake-in R14 |
| T17 | Counts look alike while content changed: show counts and diff together | 6 (code README) | bake-in R15 |
| T18 | The analyst proposes and does not apply; reads traces and cannot write them | 7 (module notes) | bake-in R17, R18 |
| T19 | Analysis scoped to the prompt though the target enum names four parts | 7 (module notes) | bake-in R18 |
| T20 | Grader reads the file, quotes verbatim with a line number; never judges from the transcript | 5 (module notes) | bake-in R11 |
| T21 | Stage ordering is requested, not enforced; report what happened | 4 (module notes) | bake-in R2 |
| T22 | Simulated fetch failures are deterministic; the helper module defaults to 0 (raise it to demo retries) while the narration, notebook text and committed trace use 2 | 4 (module notes, narration, notebook) | contradicted lever R3: 2 by value-selection branch 1 (Lesson 4 narration); batch 0 (T23); Ask First |
| T23 | The retry "only adds turns and noise" in the batch | 7 (batch module) | lever R3 (batch value 0) |
| T24 | The instructions change could live in the system prompt; the course edits the instructions file | 7 | narrative CTX-C8 |
| T25 | A checkpointer is not required for the rubric loop ("measured") | 5 (module notes) | narrative CTX-D |
| T26 | Live cost is bounded by caps; a batch costs cents | README | narrative CTX-D; §1 item 9 |
| T27 | A batch with grader errors is a weaker result and must say so | 7 (batch module) | bake-in R12, R16 |
| T28 | Match criteria by position, not by the grader's paraphrased name | 7 (batch module) | bake-in R16 |
| T29 | One run out of five is not a pattern; note it under rejected | 7 | bake-in R17 (AC22 live) |

### CTX-D. Perishable assumptions

Treat these as search keywords against current documentation, not guaranteed imports. The concepts in CTX-A…CTX-C are durable; only these names and versions are perishable.

- Harness: `deepagents` 0.7.11 — `create_deep_agent`, `FilesystemBackend(root_dir, virtual_mode=True)`, `FilesystemMiddleware`, `FilesystemPermission` (first match wins, unmatched allowed), `RubricMiddleware` (flagged **beta** in this era; activates only when a `rubric` key is supplied on invocation; its default grader system prompt is *replaced*, not extended, by a custom one; records a `grader_error` pass on exception; exposes a private `_rubric_status` state value), `ModelCallLimitMiddleware(run_limit, exit_behavior="end")`, `memory=[...]`, `skills=[...]`, `permissions=[...]`, `response_format=` for structured output, `on_evaluation` callback.
- Framework: `langchain` 1.3.18 / `langchain-core` 1.6.1 / `langgraph` 1.2.11 — `create_agent`, middleware hook names (`before_agent/after_agent`, `before_model/after_model`, `wrap_model_call/wrap_tool_call`), `InMemorySaver` checkpointer (the course attached one "to match the shape the docs show"; not required for revision), `stream_mode="updates"`, message content as a list of blocks on current models vs a plain string on older ones.
- Provider: `langchain-openai` 1.6.0 / `openai` 3.6.0; the `openai:<model>` prefix string; course model ids `openai:gpt-5.4-mini` (agent, grader) and `openai:gpt-5.5` (analyst, and one slide's generic example) — provenance only; the course's per-million-token prices for them (`5.00/30.00`, `0.75/4.50`) are era-specific, as is the README's cost note: live cost is bounded by the turn caps and the revision budget, and a batch costs cents at those prices.
- **Request-parameter compatibility:** the course never sets sampling parameters (no `temperature`); model families of this era may reject such parameters — do not add them when wiring a platform model.
- Tokenizer: `tiktoken` 0.14.0 encoding `o200k_base`, with a characters-÷-4 fallback.
- Tracing (not built): `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` (the course's own files disagree on the project name); per-run unique `thread_id` so traces do not chain.
- Course-term name map (provenance, not binding beyond §3): `fetch_requirement` (the fake-Jira tool; `fetch_requirement_from_jira` in two snapshots), `write_file` / `edit_file` / `read_file` / `ls` / `glob` / `grep`, `/analysis.md`, `/memories/AGENTS.md`, `/proposal.md`, `workspace/`, `run_history/<label>/run_NN_<doc>.json`, `summary.json`, `proposal_<label>.md|json`, `_rubric_status`, `ReviewRun` / `VerificationRun` / `GradingPass` / `RunRecord` / `HarnessChange`, tickets `AUTH-142` (the course's default, file upload), `NOTIF-205`, `REQ-104`, page `page-req-upload`, badge classes `badge-open/ready/done/pass/fail`, port 5050, run names and tags with the course's mixed lesson numbering. Dropped as presentation-only: CSS colors, notebook HTML card styles, matplotlib figures, the primer's poems and its turn cap of 30.

### CTX-E. Provenance map

Lesson numbering follows the transcripts (the repo folders and README each use a different numbering). Nothing in this spec requires platform access.

| Lesson (transcript) | Title | Contributed |
|---|---|---|
| 1 | Introduction | CTX-A framing (the four loops; the requirement review agent as the running example). No slides. |
| 2 | Overview of Loop Engineering | CTX-A stages 2–5; CTX-C2, C3, C6; T1–T8; D1, D2; §1 items 5, 6, 8, 15. Slides 2.1–2.13 (Wide deck, all narrated except the title card). |
| 3 | Deep Agent Primer | CTX-C8, C9; T9; CTX-D harness names; §1 items 4, 7. Slides 3.1–3.5 (3.2–3.5 narrated; 3.5 deck-only in its model id and tool name); primer notebook (poet) — not built. |
| 4 | Agent Loop | CTX-A stages 1–2; CTX-B1, B2, B3, B5, B6; R1–R9; T10, T21, T22; §3.1 format; the Lesson 4 notebook, instructions file, helper module and committed trace. Slides 4.1–4.5 (4.2–4.5 narrated). |
| 5 | Verification Loop | CTX-A stage 3; CTX-B4, B7; R10–R12; T11, T12, T20, T25; D1; the Lesson 5 notebook, rubric and grader notes, committed trace. Slides 5.1–5.4 (5.2–5.4 narrated). |
| 6 | Event-Driven Loop | CTX-A stage 4; CTX-C4, C7, C11; R13–R15; T14–T17; §1 items 1–3; the shipped simulated-tracker app (routes, trigger, store, templates) and its README. Slides 6.1–6.6 (6.2–6.4 narrated; 6.5 title card; 6.6 same diagram, deck unknown). |
| 7 | Learning loop | CTX-A stage 5; CTX-B8, B9; CTX-C5; R16–R19; T13, T18, T19, T23, T24, T27–T29; §3.4; the Lesson 7 notebook, batch and analyst modules, committed batches, proposal and summaries. Slides 7.1–7.2 (7.2 narrated). |
| 8 | Conclusion | Nothing beyond the recap. No slides. |
| — | Course repo files outside lessons | `pyproject.toml`, `uv.lock`, `requirements.txt`, `.env.example`, README (pins and era, §2; cost note, T26); the five requirement documents and the ticket seed (shape of the fixture corpus, facts re-authored); the four loop diagrams (CTX-A). |
| — | **Environment (`coding-agent-lab`)** — not a lesson | Everything tagged `[environment]`: the deliverable shape (§1), §2 container/venv/key rows, the model-roles mechanism, R20–R24, the `## Runtime (lab)` section and its failure modes, the §0 `choices`-fence paragraphs, the Environment Resolutions table. |

Slide-weighting record: every slide fact used here is narrated (ranks with its lesson's transcript) except the title cards and three deck-only details — slide 3.5's model id and `fetch_requirement_from_jira` tool name and slide 3.4's `Agent.md` — each of which loses to code and narration (CTX-C10).

---

**Status:** v1 · course: Loop Engineering with LangChain DeepAgents · learner project: the lab's fixed assignment (§1) · environment: `coding-agent-lab`. **Living document:** when the building agent produces something unexpected, add the missing constraint here (a rule, a criterion, or a Not-Included item) and re-run.
