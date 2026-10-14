# Spec: Requirements Review Loop App — Coding-Agent-Lab Build

> **What you're building:** a requirements-review web app that grades and improves itself. You open the board in the preview pane, create a ticket against a vague requirement page, and watch the agent fetch the page, write a five-section analysis, get sent back by the grader, pass, and post its report as a new page version. You edit the requirement and the analysis re-runs on its own. After a batch of runs you approve the analyst's proposed instruction change and watch first-attempt pass rates go from 0 of 5 to 5 of 5. Answering the gate's first question with the recommended baseline builds all of this end to end, and the build is COMPLETE when the offline suite passes — the lab's ambient keys unlock only the `live` tests and live use of the finished app.
>
> This file is self-contained: the Course Context Pack at the end replaces every external course reference, and nothing here needs platform, notebook, or repository access.
>
> `(CTX-X)` anchors mark course-derived knowledge; `[environment]` marks facts the lab contributes; *project hardening* marks the generator's own additions. The Decision Ledger below holds every point where the build could diverge, each pinned to one course-derived default, so the spec builds as-is with no intake.
>
> Generated from the Loop Engineering with LangChain DeepAgents notebooks + transcripts + slides on 2026-10-13, guide @ `57d8df0`, overlay (coding-agent-lab) @ `2555fe7`.

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

   *`[environment]` In this lab the structured question tool is a fenced `choices` block placed last in your message, one option per line, preceded by a line `**Question N of M — <decision>**`; a clicked option and a typed answer naming an option count identically. Only the latest message's buttons stay live, so a changed answer is re-asked as a new question — never ask anyone to go back to an earlier one.*

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

   *`[environment]` Each row is one `choices` fence, last in its own message, under its own `**Question N of M — <decision>**` line, so both of you can see nothing was skipped; click and typed answers are equivalent, and because only the latest message's buttons stay live, a changed answer is re-asked as a new question rather than edited in place.*

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

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option. Rows are grouped learner → design → realization → contradicted, in pipeline order within each group. Owner is a label only. Five of the six learner-context dimensions were derived and then resolved by the lab — see the Environment Resolutions table right after this one; only the scope-boundary row stays here.

| # | Category | Decision | Invariant (must hold) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L1 | learner | **Scope boundary.** Gate: present the §1 "Not Included" list *inside this question*, item by item with its handling tag, and ask whether anything should come back or be added. | (empty — the pattern imposes nothing here) | Keep as-is: every §1 exclusion stands; the full acceptance set in §5 is built. | (a) keep the list as-is; (b) bring something back — name the item in free text; the §1 handling tag says what the agent may do with it (`restorable` items are built; `named-never-built` items are built with no spec parameters or criteria; `owned-by-row` items defer to their row; `unavailable` items cannot be restored here and the agent says so). An added exclusion must name the acceptance criteria it retires. | Restoring an item adds scope the acceptance suite does not cover; the §1 tag per item states the cost. | learner |
| D1 | design-argued | **Instruction placement** — where the review agent's standing guidance lives. | The review instructions are a file inside the agent's own filesystem, loaded into context at the start of every run, never writable by the agent, and versioned so the learning loop can revise them in place (R6, R7, R25). | A single always-loaded instructions file (`/memories/AGENTS.md` in each run workspace) carrying both the Procedure and the Review guidance — the course's choice for the review agent (CTX-C2). | (a) a single always-loaded instructions file (course default); (b) a short always-loaded core file plus a `skills/` directory of procedures behind progressive disclosure — the course built this working in its primer (Lesson 3), where each skill's description is loaded up front and its body only on demand. | Lesson 3 argues it aloud: the always-loaded file "costs context on every call, so it should stay short", while skills cost one description line each until used. Litmus branch: **row** — the course showed both sides working (primer with skills; review agent without) and they differ in a component, not a value. Choosing (b) widens what the analyst may propose (procedural things include skills, Lesson 2) and the apply rule R25 must then target the skill file the proposal names. | course+learner |
| D2 | design-argued | **Verification loop present or absent** — does a grader wrap the agent loop? | The agent loop is bounded by a model-turn cap and declares its own completion; the finished review is a file, not a chat message (R3, R5). When a grader is present it judges that file per criterion with a gap on each failure and feeds the gaps back (R11, R12). | Present: a grader scores every finished report against the three-criterion rubric and may send it back; the revision budget is a body lever (R12) — the course's argued position (CTX-C3). | (a) present — grader wraps the agent loop (course default); (b) absent — revision budget 0, the bare agent loop the course built first in Lesson 4 ("if you set this to 0, you will have the same basic agent loop", Lesson 5). | Lesson 5: "just because the agent says it is done, is the analysis actually good enough? In the agent loop, nothing is checking for this." Lesson 2: "you don't need the verification loop per se" — loops compose. Litmus branch: **row** — a limit value that removes a component is a component choice, and the course showed the system working without the grader (Lesson 4) before wrapping it. Choosing (b) removes the first-attempt signal the learning loop mines: AC14–AC17, AC26–AC33 retire and the harness view has nothing to analyse. The turn cap drops from 40 to 12 (R5). | course+learner |
| RR1 | realization | **Acceptance-suite model** — which model the offline acceptance suite drives the pipeline with. | The whole pipeline — fetch tool, staged file writes, grader verdicts and feedback, run records, analyst proposal, apply, compare — runs end to end against a model the harness accepts in place of the live one, with every stage exercised (R28 names the live path). | The **scripted model stand-in** declared in §5 (`scripted_model.py`): a fake chat model, honestly named as a stand-in in its own description, whose per-role responses are fixed by the fixtures. Branch taken: the live model is a keyed dependency, so the lightest invariant-preserving realization substitutes — tier 1 (plain code shipped with the build, no install, no process). The lab supplies a key, but the Default stays scripted so the suite is deterministic and replayable. | (a) scripted stand-in (`scripted_model.py`); (b) live platform models through the lab's proxy (course default — the course ran live OpenAI models; **here the lab supplies the key, so choosing it costs no setup**; criteria tagged `live` are the ones that need it). | Live runs are non-deterministic ("the agent behavior you experience may differ from the video", every notebook) and cost wall-clock per run; the scripted path replays identically. This is a substitution row: the checklist marks it `≠ course choice`. | course+learner |

### Environment Resolutions `[environment]`

This spec was generated for the **coding-agent-lab** environment. All six learner-context dimensions were derived from the course first and then resolved against the lab; the rows below were resolved, not skipped. Two course-owned realization rows follow them because every one of their alternatives is untakeable here.

| Dimension | Resolution | Where the Invariant lives now |
|---|---|---|
| project | **ANSWERED** — the lab fixes the assignment: the course's example shape, a requirements-review agent wrapped in verification, event-driven and learning loops, delivered as one served app | spec §1 Objective. Invariant empty (the pattern imposes nothing on the project choice). |
| data/inputs | **ANSWERED** — inputs are seeded into the workspace: the §5 fixture corpus (five synthetic requirement pages, each with an open ticket) | spec §5 fixture corpus; the derived Invariant (every input is a plain-text requirement addressable by a ticket key from a source the fetch tool queries at run time — the agent is never handed the text) lives in R1 → AC4. |
| goal | **ANSWERED** — the lab fixes what "working" means: a report that satisfies the three-criterion rubric, and a learning loop that raises first-attempt pass rates with no regression | spec §1 + the acceptance criteria; the derived Invariant ("working" is expressible as per-criterion pass/fail on the output *file*, with a gap per failure) lives in R11 and R13 → AC14. |
| model/provider | **CONSTRAINED** — the built app needs an LLM, so platform models only, keys and base URL read from the lab's environment, never asked for | spec §2 (model rows) + R28 → AC34, AC35; the derived Invariant (native tool calling; schema-typed responses for grader verdicts and analyst proposals; a separate model per role allowed) lives in R28. The course's tiering argument is a body lever (R28) with an Ask-First entry. CTX-D carries the course's own model ids as provenance only. |
| environment | **ANSWERED** — the lab container | spec §2 + the `## Runtime (lab)` section; the derived capability invariants moved to the rules that need them: a confinable filesystem with a virtual root → R10 → AC13; run records and page versions survive process restarts → R21, R31 → AC24; Python ≥ 3.12 for the course pins → §2 version check. |
| scope-boundary | **KEPT** | Ledger row L1. Invariant empty. |
| event surfaces (course-owned realization row) | **ANSWERED — every alternative unavailable here.** The course argued real Slack/Jira/Confluence versus its own simulated Jira+Confluence surfaces (Lesson 6). The real surfaces need Slack app tokens, an Atlassian API token and site, and a public tunnel — credentials the lab does not supply and this spec may never ask for. No other alternative remains ("no event layer" was never a side the course argued), so the row is not asked. | Pinned in §2 (event surfaces row) with the course's provenance; §1 carries the real integrations as `unavailable` with the seam named; CTX-C5 holds the argument. |
| hosted tracing (course-owned realization row) | **ANSWERED — every alternative unavailable here.** The course optionally traced live runs to a hosted tracer behind an API key (Lesson 3); the lab supplies no such key. The local run record carries every step the hosted trace would (Lesson 3: "there will also be a local trace. That won't require a login"), so the row collapses to one takeable option and is not asked. | Pinned in §2 (tracing row) and R21; §1 carries hosted tracing as `unavailable` with the seam named; CTX-C6. |

## 1. Objective

Build a single served web app (`[environment]`: one server on port 4000 serving both the page and its API) in which a requirements-review agent turns a plain-text software requirement into a five-section analysis file, a grader scores that file against an explicit rubric and sends it back with feedback until it passes or the revision budget is spent, events in a simulated Jira+Confluence (a ticket created, a linked requirement page edited) trigger the review automatically, and an analyst reads the recorded runs across many requirements, proposes one change to the agent's instructions, and — only after a human approves it — the change is applied as a new instructions version whose effect is measured by re-running the batch and comparing first-attempt pass rates (pattern: CTX-A). For a software team's engineering lead or product manager, with the guarantee that every run is durably recorded with everything it was told and everything it produced, that the agent never edits the requirement or its own instructions, and that no harness change is ever applied without recorded human approval.

The course's own artifacts — Jupyter notebooks, a notebook-driven primer, and a demo web app on port 5050 — are never the deliverable (`[environment]`); the served app above embodies the course's pattern.

### Not Included ★

Each item carries its handling tag for the L1 gate question.

1. **Real Slack, Jira and Confluence integrations** — `unavailable` here (they need Slack app tokens, an Atlassian API token and site URL, and a public tunnel, which the lab does not supply). Seam a standalone build would use: the single automation function that fetches the linked page, runs the loop and writes the report back (R16) — replace the store's page/ticket lookups with the real REST APIs and invoke it from a webhook endpoint; nothing about the agent or the loops changes (CTX-C5).
2. **Hosted tracing of live runs** — `unavailable` here (needs a tracer API key). Seam: three environment variables the course's harness reads with no code change (CTX-D); the local run record (R21) already holds every step.
3. **Scheduled (cron-style) triggers** — `named-never-built`: the course names schedules as a trigger kind (Lesson 2) but built only event and manual triggers; the spec supplies no parameters and no criteria for it.
4. **Human approval before sensitive tool calls, and a human acting as the grader** — `named-never-built` (Lesson 2's four human-oversight points; only "approve harness changes" and "a human marks Done" are built, R18, R24).
5. **Memory consolidation / user-preference memory as a learning-loop target** — `named-never-built` (Lesson 2's second improvement category; the course built only prompt changes).
6. **Automatic application of tool, grader or configuration changes** — `named-never-built`: the proposal schema names all four targets; only `prompt` is ever applied (R25).
7. **Skills behind progressive disclosure for the review agent** — `owned-by-row` D1.
8. **The bare agent loop without a grader** — `owned-by-row` D2.
9. **Subagents and delegation, context summarization and offloading, a code interpreter or sandbox** — `named-never-built` (deep-agent pillars from the primer the review agent does not use).
10. **The poet primer agent and the notebooks' visual renderers (plots, styled HTML cards)** — `unavailable`: outside the delivered build mode; the app's own views (R19, R26) carry the same facts as tables.
11. **Token and dollar cost estimates per batch** — `restorable`: additive and owned by no row; the course's per-million-token prices are perishable (CTX-D), so they are dropped; the compare view reports attempts instead (R26).
12. **Authentication, multi-tenant users, deployment hardening, WebSockets** — `unavailable`: outside the delivered build mode (a single-user lab tool over plain HTTP, `[environment]`).

A genuinely new exclusion given at the gate must name the acceptance criteria it retires.

### Adapting this beyond the lab `[environment]`

Taking this spec elsewhere means re-opening what the lab resolved: **project** and **goal** are fixed in this §1 — swap the requirements-review example for your own task and rewrite the rubric in R13; **data/inputs** are the §5 seeds — replace them with your own requirement source behind the fetch tool (R1); **model/provider** is §2's model rows and R28 — any provider with native tool calling and schema-typed output qualifies, and the model/provider decision becomes a Ledger row again; **environment** is §2 plus the `## Runtime (lab)` section — the port, the relative-URL rule and the workspace rules are the lab's, while the confined filesystem and durable records are the course's and stay; the two **unavailable** rows (event surfaces, hosted tracing) regain their course-faithful options once you hold the credentials.

## 2. Tech Stack & Versions

Secrets are read from the environment only (R28); none are written into any file, and `.env` is never committed.

| component | pinned choice | note |
|---|---|---|
| Python | the container's `python3` | `[environment]` The lab image's minor version is not stated. Before installing, run `python3 --version`, record it in `resolved-decisions.md`, and if any course-pinned package below refuses the interpreter, **stop and report** — the course requires Python ≥ 3.12 (its lock file, its README, its kernels record 3.12.10). Never assume the floor is met. |
| virtual environment | `python3 -m venv --system-site-packages .venv` inside the app folder | `[environment]` Reuses the preinstalled stack for unpinned packages. **Where a course pin and a preinstalled copy conflict, the course pin wins inside the venv.** |
| agent harness | `deepagents==0.7.11` | **Honest pin situation:** the course's `pyproject.toml` sets floors (`>=`) and its `uv.lock` resolves exact versions; this row and the rows marked "course pin" reproduce the lock's resolved versions as provenance. Not preinstalled — batch the install early with the other pins and announce its wall-clock cost (`[environment]`). The course's framework is a pin, not a Ledger row. Era-specific names → CTX-D. |
| LangChain stack | `langchain==1.3.18`, `langchain-core==1.6.1`, `langchain-openai==1.6.0`, `langgraph==1.2.11` | course pins (uv.lock). The provider adapter is the course's (`openai:` prefix); it is pointed at the lab proxy by the variables in the model rows below. |
| OpenAI SDK | `openai==3.6.0` | course pin; the container preinstalls a copy — the course pin wins inside the venv (`[environment]`). |
| pydantic | `pydantic==2.13.5` | course pin; typed schemas for the grader verdict and the harness-change proposal (§3). |
| python-dotenv | `python-dotenv==1.2.3` | course pin; a preinstalled copy exists — the course pin wins inside the venv. Loads a local `.env` if present; the lab's variables are already exported. |
| web server | `fastapi` + `uvicorn`, preinstalled versions | The course left its web framework unpinned (`flask>=3.1.3`, absent from its lock), so a modern choice is allowed; the preinstalled pair avoids an install (`[environment]`). Serves page + API on `0.0.0.0:4000` (R30). |
| persistent store | flat JSON files under the app-owned `data/` directory, read and written with the standard library | Tier 1 — ships with the language's standard distribution — and it is the course's own realization ("three JSON files, each a plain list; a learner can open any of these files directly", Lesson 6 code). Judged at the fixture scale (tens of runs) exact in-process reads meet R21/R31; the lab's `sqlite3` is also tier 1 but adds nothing the invariant needs. Not a Ledger row: keyless, never argued. |
| event surfaces | the app's own simulated Jira (tickets) and Confluence (versioned pages) — the course's shipped keyless realization | Pinned here because the course-faithful alternative (real Slack/Jira/Confluence) is `unavailable` in this lab (Environment Resolutions). Provenance: Lesson 6 code; the lesson video demonstrated the real services. |
| tracing | the local run record (R21) only | Pinned here because hosted tracing is `unavailable` in this lab (Environment Resolutions). The course's optional tracer env vars are perishables (CTX-D). |
| LLM access `[environment]` | the app reads exactly `OPENAI_API_KEY` and `OPENAI_BASE_URL` (the course's provider's pair); `ANTHROPIC_API_KEY` and `ANTHROPIC_BASE_URL` are present in the container and **never read** | R28. Never hardcode, never prompt for, never guess other names. |
| model roles `[environment]` | `REVIEW_AGENT_MODEL`, `REVIEW_GRADER_MODEL`, `REVIEW_ANALYST_MODEL` — one platform model id each | Set by the build agent when it writes `resolved-decisions.md` (§0 step 5): the checklist carries one "model roles" line with the agent's "(Recommended)" platform model per role, confirmed with the checklist — no extra gate question. The course's own ids (CTX-D) are provenance, never asserted to be served by the proxy. The tiering lever (R28) decides whether the three differ. |
| model mode | `REVIEW_MODEL_MODE` = `scripted` (RR1 default) or `live` | The offline suite runs with `scripted`; `live` criteria set `live`. |
| data location | `REVIEW_DATA_DIR` (default `data/`) | Lets §7 run each criterion group against a fresh directory. |
| Node | not used | `[environment]` preinstalled but no part of this build. |

## 3. Input/Output Contracts ★

All objects below are JSON. Identifiers: a ticket key is `^[A-Z]{2,8}-[0-9]{1,6}$` (uppercase letters, a hyphen, digits — the course's ticket-id alphabet); a page id is `^page-[a-z0-9-]+$`; a run id and a proposal id are 8 lowercase hex characters (`^[0-9a-f]{8}$`); an instructions version is `^v[0-9]+$`. Every API path is **relative** (R30); the API lives under `api/`.

### 3.1 The analysis report (the agent's deliverable, `/analysis.md` in its workspace)

Markdown, parsed into this object by the harness. The constraints encode R4 and the rubric R13.

```json
{
  "$id": "AnalysisReport",
  "type": "object",
  "required": ["headings", "sections", "counts", "summary_words"],
  "properties": {
    "headings": {
      "type": "array",
      "const": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"],
      "description": "The five `## ` headings, in this exact order, under the title `# Requirements Analysis`."
    },
    "sections": {
      "type": "object",
      "properties": {
        "Confirmed Facts": {"$ref": "#/$defs/bullets"},
        "Ambiguities": {"type": "array", "items": {"$ref": "#/$defs/ambiguity"}},
        "Clarification Questions": {"$ref": "#/$defs/bullets"},
        "Assumptions": {"$ref": "#/$defs/bullets"},
        "Summary": {"type": "string", "minLength": 1}
      },
      "required": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"]
    },
    "counts": {
      "type": "object",
      "description": "Bullets per list section; Summary is prose and is never counted (course helper).",
      "required": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions"],
      "additionalProperties": {"type": "integer", "minimum": 0}
    },
    "summary_words": {"type": "integer", "minimum": 0}
  },
  "$defs": {
    "bullets": {"type": "array", "items": {"type": "string", "minLength": 1}},
    "ambiguity": {
      "type": "object",
      "required": ["clause", "reason"],
      "properties": {
        "clause": {"type": "string", "minLength": 1, "description": "The exact clause, quoted: the bullet line is `- **\"<clause>\"**`."},
        "reason": {"type": "string", "minLength": 1, "description": "The indented line `  Reason: ...` under the clause."},
        "resolved_by": {"type": "string", "description": "Present only when the indented line `  Resolved by: ...` exists (clarity criterion)."},
        "edge_case": {"type": "string", "description": "Present only when the indented line `  Edge case: ...` exists (depth criterion)."}
      }
    }
  }
}
```

Completeness of a report (used by R5 and the trace): every list section has ≥ 1 bullet and `summary_words > 0`.

### 3.2 Grading pass and run record

```json
{
  "$id": "GradingPass",
  "type": "object",
  "required": ["iteration", "result", "explanation", "criteria", "analysis_markdown"],
  "properties": {
    "iteration": {"type": "integer", "minimum": 1},
    "result": {"enum": ["satisfied", "needs_revision", "grader_error"]},
    "explanation": {"type": "string"},
    "criteria": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "passed"],
        "properties": {
          "name": {"enum": ["completeness", "clarity", "depth"]},
          "passed": {"type": "boolean"},
          "gap": {"type": "string", "minLength": 1}
        },
        "if": {"properties": {"passed": {"const": false}}}, "then": {"required": ["gap"]}
      }
    },
    "analysis_markdown": {"type": "string", "description": "The file exactly as this pass saw it."}
  },
  "allOf": [
    {"if": {"properties": {"result": {"const": "satisfied"}}}, "then": {"properties": {"criteria": {"minItems": 3, "items": {"properties": {"passed": {"const": true}}}}}}},
    {"if": {"properties": {"result": {"const": "needs_revision"}}}, "then": {"properties": {"criteria": {"minItems": 3, "contains": {"properties": {"passed": {"const": false}}}}}}},
    {"if": {"properties": {"result": {"const": "grader_error"}}}, "then": {"properties": {"criteria": {"maxItems": 0}}}}
  ]
}
```

```json
{
  "$id": "RunRecord",
  "type": "object",
  "required": ["id", "ticket_key", "requirement_page_id", "requirement_version", "instructions_version", "instructions",
               "requirement_doc", "model_mode", "model", "messages", "trace", "stage_order", "turns", "grading",
               "analysis_markdown", "counts", "status", "report_page_id", "report_version", "started_at", "timestamp"],
  "properties": {
    "id": {"type": "string", "pattern": "^[0-9a-f]{8}$"},
    "ticket_key": {"type": "string", "pattern": "^[A-Z]{2,8}-[0-9]{1,6}$"},
    "requirement_page_id": {"type": "string", "pattern": "^page-[a-z0-9-]+$"},
    "requirement_version": {"type": "integer", "minimum": 1},
    "instructions_version": {"type": "string", "pattern": "^v[0-9]+$"},
    "instructions": {"type": "string", "minLength": 1, "description": "The instructions file this run was seeded with, verbatim."},
    "requirement_doc": {"type": "string", "minLength": 1},
    "model_mode": {"enum": ["scripted", "live"]},
    "model": {"type": "string", "description": "`scripted` in scripted mode; otherwise the agent-role model id."},
    "messages": {
      "type": "array",
      "description": "Every message of the conversation, untruncated, including grader feedback injected between attempts.",
      "items": {
        "type": "object",
        "required": ["type", "content", "tool_calls"],
        "properties": {
          "type": {"enum": ["system", "human", "ai", "tool"]},
          "content": {"type": "string"},
          "tool_calls": {"type": "array", "items": {"type": "object", "required": ["name", "args"],
                          "properties": {"name": {"type": "string"}, "args": {"type": "object"}}}},
          "tool_call_id": {"type": ["string", "null"]},
          "status": {"type": ["string", "null"]}
        }
      }
    },
    "trace": {
      "type": "array",
      "items": {"type": "object", "required": ["step", "actor", "action", "detail"],
                "properties": {"step": {"type": "integer", "minimum": 1},
                               "actor": {"enum": ["Model reasoning", "Tool"]},
                               "action": {"type": "string"},
                               "detail": {"type": "string", "maxLength": 221, "description": "Tool result preview, cut at 220 chars plus an ellipsis (display only; `messages` holds the full text)."}}}
    },
    "stage_order": {"type": "array", "items": {"enum": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"]},
                    "description": "Sections in the order a tool call actually wrote them; a call whose result is an error adds nothing."},
    "turns": {"type": "integer", "minimum": 0, "description": "Model turns (messages of type `ai`)."},
    "grading": {"type": "array", "items": {"$ref": "GradingPass"}},
    "analysis_markdown": {"type": "string", "description": "`/analysis.md` at the end of the run ('' if never written)."},
    "counts": {"type": "object", "additionalProperties": {"type": "integer"}},
    "status": {"enum": ["satisfied", "max_iterations_reached", "grader_error", "turn_limit_reached"]},
    "report_page_id": {"type": ["string", "null"]},
    "report_version": {"type": ["integer", "null"]},
    "started_at": {"type": "string"},
    "timestamp": {"type": "string"},
    "workspace_path": {"type": "string", "description": "The fresh per-run workspace directory, removed after the run (R8)."}
  },
  "allOf": [
    {"if": {"properties": {"status": {"const": "satisfied"}}}, "then": {"properties": {"grading": {"minItems": 1}}}},
    {"if": {"properties": {"status": {"const": "turn_limit_reached"}}}, "then": {"properties": {"grading": {"maxItems": 0}}}}
  ]
}
```

### 3.3 Tickets, pages, versions

```json
{
  "$id": "Ticket",
  "type": "object",
  "required": ["key", "title", "description", "linked_page_id", "assignee", "status", "comments", "created_at", "last_analyzed_version", "last_run_id"],
  "properties": {
    "key": {"type": "string", "pattern": "^REQ-[0-9]+$", "description": "Keys the app mints are REQ-<n>, n = highest existing + 1."},
    "title": {"type": "string", "minLength": 1},
    "description": {"type": "string"},
    "linked_page_id": {"type": "string", "pattern": "^page-[a-z0-9-]+$"},
    "assignee": {"type": "string"},
    "status": {"enum": ["Open", "Analysis Ready", "Done"]},
    "comments": {"type": "array", "items": {"type": "object", "required": ["author", "text", "timestamp"]}},
    "created_at": {"type": "string"},
    "last_analyzed_version": {"type": ["integer", "null"]},
    "last_run_id": {"type": ["string", "null"]}
  }
}
```

```json
{
  "$id": "Page",
  "type": "object",
  "required": ["id", "kind", "title", "linked_ticket", "versions"],
  "properties": {
    "id": {"type": "string", "pattern": "^page-[a-z0-9-]+$"},
    "kind": {"enum": ["requirement", "analysis_report"]},
    "title": {"type": "string", "minLength": 1},
    "linked_ticket": {"type": ["string", "null"], "description": "Set only on analysis_report pages: the ticket whose runs write here."},
    "versions": {
      "type": "array",
      "items": {"type": "object", "required": ["n", "author", "timestamp", "body"],
                "properties": {"n": {"type": "integer", "minimum": 1}, "author": {"type": "string"}, "timestamp": {"type": "string"}, "body": {"type": "string"}}},
      "description": "n is 1 for the first version and increases by exactly 1 per save; versions are never rewritten."
    }
  },
  "allOf": [
    {"if": {"properties": {"kind": {"const": "requirement"}}}, "then": {"properties": {"linked_ticket": {"const": null}, "versions": {"minItems": 1}}}},
    {"if": {"properties": {"kind": {"const": "analysis_report"}}}, "then": {"properties": {"linked_ticket": {"type": "string"}, "title": {"pattern": "^Analysis Report — REQ-[0-9]+$"}}}}
  ]
}
```

The `author` of every version an automation run writes is the fixed bot name `Requirements Analysis Agent (bot)`; a report-page version body begins with a three-line banner — `> Generated automatically from <ticket key> on <timestamp>.`, `> Source requirement: version <n>.`, `> Verification status: **<status>** after <k> grading pass(es).` — followed by a blank line and the report (R17).

### 3.4 Harness change proposal, batch summary, comparison

```json
{
  "$id": "HarnessChange",
  "type": "object",
  "required": ["target", "issue", "recurrence", "evidence", "section", "change", "rejected"],
  "properties": {
    "target": {"enum": ["prompt", "tool", "grader", "configuration"]},
    "issue": {"type": "string", "minLength": 1, "description": "What goes wrong, as a property of the agent, not of one document."},
    "recurrence": {"type": "string", "minLength": 1, "description": "How many of the runs show it, and which."},
    "evidence": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}, "description": "Verbatim quotations from the runs' recorded gaps; never paraphrase."},
    "section": {"type": "string", "description": "The exact heading in the instructions file the text goes under; empty unless target is prompt."},
    "change": {"type": "string", "minLength": 1, "description": "The literal text to insert, ready to apply with no editing."},
    "rejected": {"type": "array", "items": {"type": "string"}, "description": "Noticed but not acted on, with why; one occurrence across a batch is not a pattern."}
  },
  "if": {"properties": {"target": {"const": "prompt"}}}, "then": {"properties": {"section": {"pattern": "^#{1,6} .+"}}}
}
```

A stored **Proposal** wraps a `HarnessChange`: `{ "id", "instructions_version", "status": "pending" | "approved" | "rejected" | "applied", "source": "analyst" | "human", "change": HarnessChange, "proposal_markdown": string, "created_at", "decided_at": string|null, "applied_version": string|null }`.

```json
{
  "$id": "BatchSummary",
  "type": "object",
  "required": ["instructions_version", "runs", "graded", "grader_errors", "first_attempt", "revisions_needed", "run_ids"],
  "properties": {
    "instructions_version": {"type": "string", "pattern": "^v[0-9]+$"},
    "runs": {"type": "integer", "minimum": 0},
    "graded": {"type": "integer", "minimum": 0, "description": "Runs whose first grading pass carries criteria; the denominator of every rate."},
    "grader_errors": {"type": "integer", "minimum": 0, "description": "runs - graded; excluded from the rates, never averaged away."},
    "first_attempt": {
      "type": "object",
      "required": ["completeness", "clarity", "depth"],
      "additionalProperties": {"type": "object", "required": ["passed", "total", "pass_rate"],
        "properties": {"passed": {"type": "integer"}, "total": {"type": "integer"}, "pass_rate": {"type": ["number", "null"]}}}
    },
    "revisions_needed": {"type": "integer", "minimum": 0, "description": "Graded runs whose first attempt failed at least one criterion."},
    "run_ids": {"type": "array", "items": {"type": "string"}}
  }
}
```

```json
{
  "$id": "Comparison",
  "type": "object",
  "required": ["before", "after", "verdict", "criteria", "runs", "revisions_needed", "attempts", "improved", "regressed"],
  "properties": {
    "before": {"type": "string"}, "after": {"type": "string"},
    "verdict": {"enum": ["regression", "success", "partial", "no effect"]},
    "criteria": {"type": "object", "additionalProperties": {"type": "array", "items": {"type": "integer"}, "minItems": 2, "maxItems": 2},
                 "description": "criterion → [first-attempt passes before, after]."},
    "runs": {"type": "array", "items": {"type": "integer"}, "minItems": 2, "maxItems": 2},
    "revisions_needed": {"type": "array", "items": {"type": "integer"}, "minItems": 2, "maxItems": 2},
    "attempts": {"type": "array", "items": {"type": "integer"}, "minItems": 2, "maxItems": 2, "description": "Total grading passes across the batch, before and after."},
    "improved": {"type": "array", "items": {"type": "string"}},
    "regressed": {"type": "array", "items": {"type": "string"}}
  }
}
```

### 3.5 API surface (relative paths; JSON unless noted)

| method + path | request | response |
|---|---|---|
| `GET api/health` | — | `{ "ok": true, "model_mode": "scripted"\|"live", "instructions_version": "v<n>", "data_dir": string }` |
| `GET api/tickets` · `POST api/tickets` | POST: `{ title, description?, linked_page_id, assignee? }` | list of Ticket · the created Ticket (after its automation run completes, R16) |
| `GET api/tickets/{key}` | — | `{ ticket, page, report_page, runs: [RunRecord], latest_run, changes }` — `changes` is null with fewer than two runs, else R19's table object `{ previous_run_id, latest_run_id, requirement_version: [prev, latest], status: [prev, latest], counts: {section: [prev, latest]}, compare: { page_id, a, b } }` |
| `POST api/tickets/{key}/rerun` · `POST api/tickets/{key}/close` | — | the Ticket; `409` when the ticket is Done (rerun) |
| `GET api/runs/{id}` | — | RunRecord |
| `GET api/pages` · `POST api/pages` | POST: `{ title, body, author? }` | list of Page · the created Page (kind requirement, version 1) |
| `GET api/pages/{id}?v=<n>` | — | `{ page, body (at v, default latest), linked_ticket }` |
| `POST api/pages/{id}/versions` | `{ body, author? }` | `{ page, retriggered: [ticket keys] }` — `400` for an analysis_report page (R17) |
| `GET api/pages/{id}/compare?a=<n>&b=<n>` | — | `{ a, b, diff: [unified diff lines], run_a: RunRecord\|null, run_b: RunRecord\|null }` |
| `POST api/batch` | — | `{ instructions_version, run_ids }` — one run per Open/Analysis Ready ticket, under the current instructions version |
| `GET api/harness/versions` · `GET api/harness/versions/{v}` | — | `[ { version, created_at, from_proposal } ]` · `{ version, text }` |
| `GET api/harness/summary/{v}` | — | BatchSummary |
| `POST api/harness/propose/{v}` | — | `{ proposal: Proposal }` or `{ proposal: null, reason: "no criterion fails first attempt in a majority of graded runs" }` |
| `POST api/harness/proposals` | `{ change: HarnessChange, instructions_version }` | the Proposal (source human, status pending) |
| `POST api/harness/proposals/{id}/approve` · `…/reject` · `…/apply` | — | the Proposal; apply returns `409` unless status is approved, `422` when the named section is missing or the target is not prompt |
| `GET api/harness/compare?before=<v>&after=<v>` | — | Comparison |
| `GET /` | — | the HTML page (board, ticket view, pages, compare, harness view) |

## 4. Business Rules

Each rule: the behavior, the failure it prevents (CTX-B anchor where the course demonstrated it), its provenance label, and the criteria that cite it. Provenance labels: *course-demonstrated* (CTX anchor), *project hardening*, `[environment]`, or the one sanctioned co-label.

**Agent loop**

1. **R1 — Fetch by key, never by hand-off.** A run begins with a single message naming only the ticket key; the agent must call the `fetch_requirement` tool to obtain the text, and the tool resolves the key to the *current version body* of the ticket's linked requirement page. The agent is never handed the document directly (CTX-A, the course's fetch tool docstrings). This keeps the agent identical whether the source is simulated or real. *Course-demonstrated.* → AC3
2. **R2 — Transient fetch failures are retried, not fatal.** When a tool result is an error (its text begins with `Error`, or the tool message carries an error status) the agent calls the same tool again with the same arguments. The fetch stand-in simulates **2** transient failures per run — a `503`-style and a timeout-style message — before returning the document (CTX-B1). *Course-demonstrated; the count is a post-build lever.* Contradiction note: the course's narration ("we are simulating two times of failure", Lesson 4), its notebook table and its pre-recorded trace say 2; its helper's shipped default and its batch runner say 0 ("only adds turns and noise"). Litmus: the sides differ only in a value → lever, not a row. Lever-value branch 1 (the narration in the lesson that introduces the concept) selects 2. Ask before changing (§6). → AC4
3. **R3 — The report is built in staged tool calls.** One `write_file` creates `/analysis.md` with the five-heading skeleton and the Confirmed Facts bullets; four `edit_file` calls fill Ambiguities, Clarification Questions, Assumptions and Summary, in that order, one section per call. The harness *requests* this order through the instructions file and does not enforce it; the run record reports `stage_order` as what actually happened, counting a section only when the same successful call supplied text under it (CTX-A). *Course-demonstrated.* → AC5
4. **R4 — Report shape.** The finished file validates against `AnalysisReport` (§3.1): the five headings in order; one bullet per confirmed fact, recording only what the document states; each ambiguity bullet quotes the exact clause in bold and carries an indented `Reason:` line; one bullet per clarification question and per assumption; a Summary of two or three sentences (an output-shape constraint the course's instructions impose). *Course-demonstrated.* → AC6
5. **R5 — Model-turn cap, and an honest stop status.** A run is capped at **40** model turns when the grader is present (several verification passes cost more turns than one review), **12** when it is absent (six stages plus headroom for retries and the closing message — the value for Ledger D2 option (b)). The cap is not the normal stop: the loop normally ends when the agent writes the Summary and replies with one sentence. When the cap ends a run whose file is incomplete, the run's status is `turn_limit_reached`, never "finished", and the grader does not run on the incomplete file — the run carries no grading passes (*project hardening*: the course's harness leaves this case to the library; the spec pins it) (CTX-B6; Lesson 4: "max_turns matters when that path fails"). *Course-demonstrated; both values are body values cited to Lesson 4 cell 6 / Lesson 5 cell 7.* → AC7
6. **R6 — Instructions are a file, loaded every run, and their absence is loud.** Every run workspace is seeded with the current instructions version at `/memories/AGENTS.md`; that file is loaded into the agent's context at the start of the run and the system prompt only points at it. If the file is missing the run **refuses to start** with an error naming the path — a silent fallback to the system prompt alone "would run with no review guidance and produce a plausible bad review" (CTX-B4). *Course-demonstrated.* Ledger D1 owns where the guidance lives. → AC8, AC13
7. **R7 — The agent never edits its own instructions.** Writes under `/memories/` are denied by the harness's filesystem permissions, not merely by the instructions' wording; a denied write returns an error result and the run continues (CTX-B5). *Course-demonstrated.* → AC9
8. **R8 — One fresh workspace per run.** Each run gets a new, empty workspace seeded only with the instructions file; it is removed when the run ends. A leftover `/analysis.md` from a previous run must never be visible to the agent, which otherwise "may read it and skip stages" (CTX-B3). Two tickets analysed back to back never see each other's files. *Course-demonstrated.* → AC10
9. **R9 — `edit_file` rejects an ambiguous edit.** When the `old_string` of an edit matches more than once (or not at all) the tool returns an error and changes nothing; the agent recovers by reading the file and retrying with an exact match. A failed edit contributes nothing to `stage_order` (CTX-B7). *Course-demonstrated.* → AC11
10. **R10 — The requirement is the source of truth, and the agent's filesystem is confined.** The agent's filesystem root is its run workspace; paths above it are unreachable; the only files ever present are `/memories/AGENTS.md` and `/analysis.md`. The requirement page's stored versions change only through a human save (R20); no run ever adds, edits or removes a requirement version. *Course-demonstrated* (Lesson 6 README: "the agent only ever reads it, never edits it"); the confinement also carries the environment dimension's filesystem invariant. → AC12

**Verification loop**

11. **R11 — The grader judges the file, per criterion, with a gap.** After the agent declares completion, a grader distinct from the agent reads `/analysis.md` itself — not the conversation transcript — and returns one pass/fail per rubric criterion with a short actionable `gap` on every failure; the verdict is `satisfied` only when every criterion passes. The grader must find and quote the text in the file that satisfies a criterion before passing it; a criterion it cannot quote fails (CTX-B8: a grader given only the transcript "passes criteria the file does not satisfy"). *Course-demonstrated.* → AC14, AC35
12. **R12 — Feedback, retry, budget.** A `needs_revision` verdict injects the grader's explanation and gaps into the conversation and the agent revises the file; the grader re-reads and re-scores. The grader may send the work back at most **3** times (so a run has at most 4 grading passes); when the budget is spent without `satisfied`, the run's status is `max_iterations_reached` — distinct from `satisfied` and never reported as finished (CTX-B2, CTX-B9). *Course-demonstrated; the budget is a post-build lever.* Contradiction note: Lesson 5's narration and notebook and the batch runner set 3; the course's shipped event-driven app set 2. Litmus: a value, not a component (0 — which removes the grader — is Ledger D2) → lever; lever-value branch 1 (narration) selects 3. Ask before changing (§6). → AC15, AC16, AC35
13. **R13 — The rubric is three literal criteria.** `completeness`: every clause of the requirement is addressed somewhere in the analysis; `clarity`: every bullet in the Ambiguities section has an indented `Resolved by:` line naming the specific fact or decision that would settle it; `depth`: every bullet in the Ambiguities section has an indented `Edge case:` line naming a concrete production failure the ambiguity could cause. Criteria are applied literally — only the exact label satisfies a labelled-line criterion, and coverage means every item, not a sample (CTX-C3). The criterion names are the strings before the colon, in this order. *Course-demonstrated.* → AC14
14. **R14 — A grader failure is recorded, not hidden.** If the grader errors or returns an unusable verdict, the pass is recorded with `result: grader_error` and no criteria, the run's status is `grader_error`, and the run counts as *ungraded*: excluded from every rate's denominator and reported as a `grader_errors` count (CTX-B10). *Course-demonstrated.* → AC17
15. **R15 — Every grading pass is kept with the file it saw.** Each pass records iteration, result, explanation, per-criterion results and the analysis file exactly as it stood when the grader read it, so a rejected first draft remains inspectable beside the final one (CTX-A). *Course-demonstrated.* → AC14

**Event-driven loop**

16. **R16 — Events trigger the whole loop.** Creating a ticket runs the review (with verification) on its linked page immediately; saving a new version of a requirement page re-runs every ticket linked to it whose status is not `Done`; a ticket page offers a manual "re-run analysis now" trigger. All three call the same automation function: fetch the linked page's current version, run the loop in a fresh workspace, write the report, record the run, update the ticket. The app mints ticket keys as `REQ-<n>` with n one above the highest existing key, and page ids as `page-<slug of the title>` (suffix `-2`, `-3`… on collision) (CTX-A, CTX-C5). *Course-demonstrated.* → AC18, AC19, AC38
17. **R17 — The report goes to a separate, agent-owned page.** Each ticket has at most one report page, titled `Analysis Report — <key>`, kind `analysis_report`, created on first use; every run appends a new version authored by the bot name, whose body begins with the §3.3 banner (ticket key, requirement version analysed, verification status, number of grading passes). The requirement page itself is never written by a run, and the API refuses human edits to report pages (CTX-C5: the page's own history then "shows every past analysis, who (or what) wrote it, and a diff between any two versions"). *Course-demonstrated.* → AC18, AC21
18. **R18 — Status moves forward by automation, closes only by a human.** A new ticket is `Open`; a completed run sets `Analysis Ready` (whatever the verdict), records `last_analyzed_version` and `last_run_id`, and adds a bot comment naming the verdict, the requirement version and the report page. Only the human close action sets `Done`; the agent never closes its own work, and a `Done` ticket is neither re-run by a page edit nor re-runnable by hand (CTX-C7). *Course-demonstrated.* → AC18, AC19, AC20
19. **R19 — "What changed" shows counts AND the full diff.** Once a ticket has two or more runs, its view carries a table of the previous and latest run — requirement version analysed, verification status, bullet count per list section — together with a reference to the report page's version compare. Both are required: bullet counts often look alike while the content changed completely (CTX-B11). *Course-demonstrated.* → AC22
20. **R20 — Pages are versioned, never rewritten, and any two versions compare.** A page's versions are numbered from 1 and only ever appended; the compare view returns a unified diff between any two versions, and for a report page also the two runs behind those versions with their status and counts (CTX-A). *Course-demonstrated.* → AC23, AC38
21. **R21 — Every run is a durable, untruncated record.** A `RunRecord` (§3.2) is written for every run before the trigger returns: every message of the conversation in full with complete tool-call arguments and tool results, every grading pass with its file snapshot, the final file, the instructions snapshot and version, status, model mode, timestamps. Records, pages and tickets survive a process restart (CTX-A: "for agents, the story is in the traces"). *Course-demonstrated*; the restart guarantee also carries the environment dimension's persistence invariant. → AC24, AC25

**Learning loop**

22. **R22 — The batch summary is the systemic-failure signal.** For an instructions version, the summary counts first-attempt passes per criterion over the *graded* runs produced under that version, the number of graded runs whose first attempt failed any criterion (`revisions_needed`), and the grader errors excluded. Criteria are matched by position in rubric order, not by the grader's paraphrase (CTX-C8). *Course-demonstrated.* → AC17, AC26, AC31
23. **R23 — The analyst reads evidence it cannot alter and proposes one change.** The analyst is an agent rooted above the run records with read-only access to the runs, the summary and the instructions of a version; its only permitted write is its own `proposal.md`. It starts from the summary, investigates the failing criteria in the runs, quotes gap text verbatim as evidence, and returns one `HarnessChange` (§3.4) whose `change` is literal text ready to insert. The recurrence bar: a criterion failing first attempt in **more than half** of the graded runs is a property of the agent and may be acted on; anything rarer goes under `rejected` (the course's words are "most runs" and "one run out of five is not a pattern" — the majority threshold is the generator's reading of them, a post-build lever). When no criterion clears the bar the analyst proposes nothing and says so (CTX-B12). *Course-demonstrated; the no-proposal path is project hardening.* → AC27, AC28, AC33
24. **R24 — Nothing is applied without recorded human approval.** A proposal is stored `pending`; a human approves or rejects it through the app; `apply` is refused unless the proposal is `approved`, and a rejected proposal is kept for the record and never applied (CTX-C9: Lesson 2's fourth oversight point, Lesson 7's "assume human-in-the-loop reviewed this proposal and approved"). *Course-demonstrated.* → AC29
25. **R25 — Applying is plain code, prompt-only, and makes a new version.** Only `target: prompt` is applied automatically; the change text is inserted at the end of the exact section heading the proposal names (before the next heading of equal or shallower depth); a missing section or a non-prompt target is refused with an error and nothing changes. The result is a new instructions version (`v<n+1>`) stored beside the untouched earlier versions and becomes the version new runs are seeded with (CTX-C9: "the agent decided what should change; deciding where it lands should not also be a model call"). *Course-demonstrated.* → AC29, AC30
26. **R26 — A change is measured, and the verdict is named.** Comparing two versions reports first-attempt passes per criterion before and after, runs, `revisions_needed`, total grading attempts, and a verdict: `regression` if any criterion's first-attempt passes fell; else `success` if the after-batch needed no revisions; else `partial` if any criterion improved; else `no effect` (CTX-B13: "making sure there are no regressions"). *Course-demonstrated.* → AC31, AC32, AC39, AC40

**Lab constraints**

27. **R27 — The app's instructions files never sit at the workspace root.** `[environment]` The IDE rewrites the workspace-root `AGENTS.md` at every boot, so the agent-harness file of that name lives only inside app-owned folders: the versioned store under the app's data directory and each run's own workspace. The build never creates, edits or relies on a root-level `AGENTS.md`. → AC36
28. **R28 — Live models come from the platform, through the environment, never from the learner.** `[environment]` In `live` mode the app reads exactly `OPENAI_API_KEY` and `OPENAI_BASE_URL` (the course's provider's pair) and the three model-role variables of §2; it never prompts for a key, never hardcodes one, never reads `ANTHROPIC_*`, and a missing variable fails the first live run with an error naming it. The model must support native tool calling and schema-typed responses (grader verdict, analyst proposal). **Model tiering lever:** the course argued matching model capability to task difficulty — a cheaper model for the agent and grader, a stronger one for the analyst, "the one job the cheaper model does unreliably" (Lessons 2, 5, 7) — and the three role variables carry that choice; the lab constrains the provider, not the tiering, so it stays a post-build lever with an Ask-First entry. *Environment-imposed; the tiering lever is course-demonstrated (CTX-C1).* → AC34, AC35
29. **R29 — The scripted stand-in is labelled as one.** The scripted model (§5) is registered with a name and description that say it is a fake standing in for a live model, `api/health` reports the mode, and every run record carries `model_mode`. *Project hardening (Ledger RR1).* → AC37
30. **R30 — One server, port 4000, relative URLs, HTTP only.** `[environment]` The app is one process bound to `0.0.0.0:4000` serving the page and `api/`; every URL the page or its assets reference is relative (`api/tickets`, never `/api/tickets`), because the preview is reverse-proxied under a path prefix; no WebSocket is used (streaming HTTP responses are allowed). → AC2
31. **R31 — The store exists as declared on a fresh start.** On first start against an empty data directory the app creates the JSON store (pages, tickets, runs, proposals) seeded with the §5 scenario and `instructions/v1.md` equal to the §5 instructions fixture. `[environment]` for the location; the seed scenario shape is *course-demonstrated* (Lesson 6: "seeded once, on first import, so a fresh clone starts from a known scenario"). → AC1, AC24

## 5. Acceptance Criteria ★ (the oracle)

### 5.1 Fixture corpus (declared first; the build agent MUST NOT modify fixtures to pass a test)

All fixtures live under `fixtures/` in the app folder. Every fact below is authored for this spec; nothing is copied from the course.

**Requirement documents** (`fixtures/requirements/*.md`; each body is the line `REQUIREMENT: <title>` followed by one clause per non-empty line). The *clauses* of a document are its non-empty lines after the title. A clause is **vague** when it contains, as a whole word, one of the terms in `VAGUE_TERMS = {reasonable, easily, appropriately, appropriate, quickly, common, securely, large, promptly, efficiently, special, timely, sensibly, aggressively}` (case-insensitive).

| file | title | clauses (vague term in brackets) | facts / ambiguities |
|---|---|---|---|
| `01_session_timeout.md` | Session Timeout Policy | Sessions shall expire after a reasonable period of inactivity. [reasonable] · Users must be warned before their session ends. · Administrators should be able to configure the timeout easily. [easily] · Expired sessions must be handled appropriately. [appropriately] | 4 / 3 |
| `02_invoice_export.md` | Invoice Export | Users shall export invoices as PDF files. · Exports should complete quickly. [quickly] · The export must include all common invoice fields. [common] · Exported files must be stored securely for later download. [securely] · Large exports should not block the interface. [large] | 5 / 4 |
| `03_password_reset.md` | Password Reset Flow | Users shall be able to reset a forgotten password by email. · Reset links must expire promptly. [promptly] · The system shall record every reset attempt. · Suspicious reset activity should be handled appropriately. [appropriately] | 4 / 2 |
| `04_audit_log_retention.md` | Audit Log Retention | The system shall record who changed what and when. · Audit records must be retained for an appropriate period. [appropriate] · Old records should be archived efficiently. [efficiently] · Auditors must be able to search records easily. [easily] · Sensitive fields require special handling. [special] | 5 / 4 |
| `05_feature_flag_rollout.md` | Feature Flag Rollout | New features shall be released behind feature flags. · Flags should be rolled out gradually to a reasonable share of users. [reasonable] · Flag changes must take effect quickly. [quickly] · Every flag change shall be logged. | 4 / 2 |

**Seed scenario** (`fixtures/seed_pages.json`, `fixtures/seed_tickets.json`, loaded on first start, R31): five requirement pages, ids `page-session-timeout-policy`, `page-invoice-export`, `page-password-reset-flow`, `page-audit-log-retention`, `page-feature-flag-rollout`, each titled `<title> — Requirements`, version 1 authored by `Dana (Product Manager)` with the matching document as body; five Open tickets `REQ-201`…`REQ-205`, in that order, each titled `Review requirements: <title>`, assignee `Jordan (Eng Lead)`, linked to the matching page, no runs. The fixed cast for assignee/author pickers: `Dana (Product Manager)`, `Jordan (Eng Lead)`, `Priya (QA Lead)`, `Sam (Backend Engineer)`, `Morgan (Frontend Engineer)`.

**Probe documents** (created by the tests through `api/pages` + `api/tickets`, never seeded; the scripted model keys special behavior on the title):

| title | body clauses | scripted behavior |
|---|---|---|
| Loop Forever Probe | The system shall keep looping. | the agent calls `fetch_requirement` on every turn and never writes a file |
| Self Edit Probe | Sessions shall expire after a reasonable period. [reasonable] | the agent's second turn is `edit_file` on `/memories/AGENTS.md`; after the denial it proceeds normally |
| Grader Outage Probe | Exports should complete quickly. [quickly] | the scripted grader raises an exception on every pass |
| Stubborn Draft Probe | Reset links must expire promptly. [promptly] | the agent never writes `Resolved by:` / `Edge case:` lines, on the first attempt or any revision, whatever the instructions say |

**Edited requirement** (`fixtures/requirements/01_session_timeout_v2.md`, posted by AC22 as version 2 of `page-session-timeout-policy`): `REQUIREMENT: Session Timeout Policy` · Sessions shall expire after 30 minutes of inactivity. · Users must be warned two minutes before their session ends. · Administrators should be able to configure the timeout easily. [easily] · Expired sessions must be handled appropriately. [appropriately] — 4 facts, 2 ambiguities.

**Probe proposals** (`fixtures/probe_proposals.json`, posted by AC29/AC30 through `api/harness/proposals`): `copy` — a byte-copy of the analyst's v1 proposal; `missing_section` — the same with `section: "### Nonexistent"`; `tool_target` — the same with `target: "tool"` and an empty `section`.

**Instructions fixture** (`fixtures/instructions_v1.md`, becomes `instructions/v1.md`): the build agent writes it to this structure. Title `# Requirements Review Agent`; `## Procedure` with six numbered stages — (1) call `fetch_requirement` to get the document; (2) `write_file` `/analysis.md` with the exact five-heading skeleton, filling only Confirmed Facts, one bullet per fact; (3) `edit_file` Ambiguities, one bullet per under-specified clause in the shape `- **"the exact clause"**` plus an indented `Reason:` line; (4) `edit_file` Clarification Questions, one bullet each; (5) `edit_file` Assumptions, one bullet each; (6) `edit_file` Summary, two or three sentences — then: retry a tool call that returns an error with the same arguments; never modify the requirement document; never edit this file; once the Summary is written reply with one short sentence and call no further tools. `## Review guidance` with `### Confirmed facts` (record only what the document states directly; do not infer), `### Ambiguities` (quote the exact clause, then the reason it is under-specified), `### Clarification questions` (what a reviewer needs answered before work starts), `### Assumptions` (what a developer would assume if nobody answered). v1 MUST NOT contain the strings `Resolved by:` or `Edge case:`.

**Rubric fixture** (`fixtures/rubric.md`): three lines, `- completeness: …`, `- clarity: …`, `- depth: …`, stating R13's criteria in those exact names and with the exact labels `Resolved by:` and `Edge case:`.

**Scripted model** (`fixtures/scripted_model.py`, module `scripted_model`; the RR1 stand-in): a fake chat model the harness accepts in place of a live one, named `scripted-stand-in` with the description "a scripted fake standing in for a live model; replays fixed responses per role". It records every input it receives (system text, messages) on the run for assertions. Per-role script:

- *Agent role.* Turn 1: call `fetch_requirement(ticket_key)`; while the latest tool result begins with `Error`, call it again with identical arguments. Then `ls('/')` once (its result is recorded like any tool result). Then `write_file` `/analysis.md` with the skeleton and Confirmed Facts = one bullet quoting each clause verbatim. Then `edit_file` Ambiguities: one bullet per vague clause, `- **"<clause>"**` / `  Reason: "<term>" is not defined.`; when the instructions text contains `Resolved by:`, also `  Resolved by: a written definition of "<term>" agreed with the product owner.` and `  Edge case: a build reads "<term>" differently from the author and fails in production.`. Then `edit_file` Clarification Questions: `- What exactly does "<term>" mean in "<clause>"?` per ambiguity; `edit_file` Assumptions: `- Assume the narrowest reading of "<term>" until confirmed.` per ambiguity; `edit_file` Summary: `The document states <facts> facts and leaves <ambiguities> clauses under-specified. The questions above must be answered before work starts.`; final reply `Review complete.` with no tool call. On grader feedback: one `edit_file` replacing the whole Ambiguities section with the labelled form, then `Revision complete.`. Special cases: for **Audit Log Retention** the first Ambiguities edit uses `old_string` `## ` (matches every heading) → after the error it calls `read_file('/analysis.md')` and retries with the exact heading; the four probes behave as tabled above.
- *Grader role.* Reads `/analysis.md` through the file tool it is given; `completeness` passes when every clause of the requirement appears verbatim in some bullet; `clarity` passes when every Ambiguities bullet has an indented `Resolved by:` line; `depth` likewise for `Edge case:`; gap texts are exactly `each ambiguity bullet is missing the required indented 'Resolved by:' line` and `each ambiguity bullet is missing the required indented 'Edge case:' line`; result `satisfied` iff all pass, else `needs_revision` with explanation `Clarity and depth are not satisfied by the file.` (or naming the failing names). Grader Outage Probe: raise.
- *Analyst role.* Reads the version's summary; collects criteria whose first-attempt `passed / total < 0.5`… strictly, whose failures exceed half of `graded`; if none → no proposal. Else returns `HarnessChange` with `target: prompt`, `section: ### Ambiguities`, `change` = `For every ambiguity bullet, add two indented labelled lines after the Reason line:\n  Resolved by: the specific fact or decision that would settle the ambiguity\n  Edge case: a concrete production failure that could happen if it stays unresolved`, `issue` naming the omitted labels, `recurrence` `"<k>/<graded> runs: <run ids>"`, `evidence` = the recorded gap strings of those runs quoted verbatim (one per run), `rejected` = one entry per run whose trace holds a tool error that is not a rubric failure (the Audit Log Retention edit error), and writes `proposal.md` with headings Summary signal / Current instruction gap / Evidence across runs / Proposed insertion / Rejected observations.

**Replay (done by the generator):** under v1, every seeded run's first pass is completeness pass, clarity fail, depth fail → `needs_revision`; the revision adds both labelled lines → pass 2 `satisfied`. Summary v1: completeness 5/5, clarity 0/5, depth 0/5, revisions_needed 5, graded 5. The analyst's proposal inserts the two labels under `### Ambiguities`; v2 therefore contains `Resolved by:`, so every v2 run passes all three on pass 1. Summary v2: 5/5, 5/5, 5/5, revisions 0. Compare(v1, v2): improved [clarity, depth], regressed [], verdict `success`, attempts (10, 5). Compare(v2, v1): regressed [clarity, depth] → `regression`. Counts for `REQ-201`: Confirmed Facts 4, Ambiguities 3, Clarification Questions 3, Assumptions 3; summary 2 sentences, > 0 words. Stubborn Draft Probe: passes 1–4 all `needs_revision` → `max_iterations_reached`.

### 5.2 Criteria

Each criterion group runs against a fresh `REVIEW_DATA_DIR` in `scripted` mode unless tagged `live`.

| # | Given | When | Then | cites |
|---|---|---|---|---|
| AC1 | an empty data directory | the server starts | `api/health` returns `ok: true`, `model_mode: scripted`, `instructions_version: v1`; the directory holds `pages.json` (5 requirement pages, 0 report pages), `tickets.json` (5 Open tickets `REQ-201`…`REQ-205`, none with runs), `runs.json` (`[]`), `proposals.json` (`[]`), `instructions/v1.md` byte-equal to the instructions fixture | (R31) |
| AC2 | the server is running | the test inspects the listening socket and fetches `/` and every asset the page references | the process listens on `0.0.0.0:4000` only; `/` returns HTML; no `href`, `src`, `action` or fetch URL in the page or its scripts starts with `/` or an absolute origin; no asset contains `WebSocket(` or `ws://`/`wss://` | (R30) |
| AC3 | seed state | `POST api/tickets/REQ-201/rerun` | the run's first `ai` message carries exactly one tool call, `fetch_requirement` with `ticket_key` `REQ-201`; the successful tool result and `requirement_doc` both equal the body of `page-session-timeout-policy` version 1; no message before it contains that body | (R1) |
| AC4 | the AC3 run | its messages are read | the first two `fetch_requirement` results begin with `Error` (one mentioning `503`, one a timeout), the third returns the document; all three calls have identical `args` | (R2) |
| AC5 | the AC3 run | its trace is read | exactly one `write_file` call; `stage_order` equals `[Confirmed Facts, Ambiguities, Clarification Questions, Assumptions, Summary]` with no repeats on the first attempt; every `edit_file` on the first attempt wrote exactly one section | (R3) |
| AC6 | the AC3 run | `analysis_markdown` is parsed | it validates against `AnalysisReport`; `counts` = `{Confirmed Facts: 4, Ambiguities: 3, Clarification Questions: 3, Assumptions: 3}`; every ambiguity bullet is `- **"<clause>"**` with an indented `Reason:` line; `summary_words > 0` | (R4) |
| AC7 | a page `Loop Forever Probe` and a ticket linked to it are created | the ticket's creation run completes | `turns == 40`, `status == turn_limit_reached`, `grading == []`, `analysis_markdown == ""`, and the ticket is `Analysis Ready` with a bot comment naming `turn_limit_reached` | (R5) |
| AC8 | seed state with `instructions/v1.md` deleted from the data directory | `POST api/tickets/REQ-202/rerun` | the response is an error (status ≥ 400) whose message names `/memories/AGENTS.md` or the missing version file; `runs.json` is unchanged; the ticket stays `Open` | (R6) |
| AC9 | a page `Self Edit Probe` + linked ticket | the creation run completes | the trace contains an `edit_file` on `/memories/AGENTS.md` whose result begins with `Error`; `instructions` equals `instructions/v1.md`; the file in the store is byte-unchanged; `status == satisfied` | (R7) |
| AC10 | the AC3 run has completed | `POST api/tickets/REQ-201/rerun` again | the second run's messages show no `read_file` before its `write_file`; its workspace path (recorded on the run as `workspace_path`) differs from the first run's and neither directory exists after the runs | (R8) |
| AC11 | seed state | `POST api/tickets/REQ-204/rerun` | the trace holds, in order, an `edit_file` whose result begins with `Error` and mentions `old_string`, a `read_file` of `/analysis.md`, and a successful `edit_file: Ambiguities`; `stage_order` is complete and in order; `grading[0]` matches AC14's pattern | (R9) |
| AC12 | the AC3 run | the store and the run's messages are inspected | `page-session-timeout-policy` still has exactly 1 version with an identical body; the recorded `ls('/')` result lists only `/memories/AGENTS.md` (the report is not yet written at that point) and nothing above the root; no run ever changes `pages.json` except by appending an `analysis_report` version | (R10) |
| AC13 | the AC3 run | the scripted model's recorded system text is inspected | it contains the full text of `instructions/v1.md`, and `run.instructions_version == v1` | (R6) |
| AC14 | the AC3 run | `grading[0]` is read | `result == needs_revision`; criteria in order `completeness` (passed), `clarity` (failed, gap mentions `Resolved by:`), `depth` (failed, gap mentions `Edge case:`); `grading[0].analysis_markdown` contains no `Resolved by:`; the scripted grader's recorded input includes that same file text obtained through the file tool | (R11, R13, R15) |
| AC15 | the AC3 run | `grading` and the final file are read | `len(grading) == 2`; `grading[1].result == satisfied` with all three passed; a `human`-typed message carrying the clarity and depth gaps precedes the revision edit; the final file has `Resolved by:` and `Edge case:` lines under all 3 ambiguity bullets; `status == satisfied` | (R12) |
| AC16 | a page `Stubborn Draft Probe` + linked ticket | the creation run completes | `len(grading) == 4`, every pass `needs_revision`, `status == max_iterations_reached`, the ticket is `Analysis Ready` and its comment names `max_iterations_reached` | (R12) |
| AC17 | a page `Grader Outage Probe` + linked ticket | the creation run completes, then `GET api/harness/summary/v1` | `grading == [{iteration 1, result grader_error, criteria []…}]`, `status == grader_error`; the summary counts this run in `runs`, not in `graded`, `grader_errors == 1`, and every `first_attempt.total` equals `graded` | (R14, R22) |
| AC18 | seed state | `POST api/tickets` `{title: "Review requirements: Invoice Export (copy)", linked_page_id: "page-invoice-export"}` | the response ticket has key `REQ-206`, `status == Analysis Ready`, `last_run_id` set, one bot comment; a page `page-analysis-req-206` of kind `analysis_report`, title `Analysis Report — REQ-206`, `linked_ticket REQ-206`, exactly 1 version authored `Requirements Analysis Agent (bot)` | (R16, R17, R18) |
| AC19 | seed state; `REQ-203` closed via `POST api/tickets/REQ-203/close` | `POST api/pages/page-password-reset-flow/versions` with a changed body, then `POST api/pages/page-session-timeout-policy/versions` with a changed body | the first save returns `retriggered == []` and creates no run (its only linked ticket is Done); the second returns `retriggered == ["REQ-201"]` and creates exactly one new run with `requirement_version == 2`, and `REQ-201` is `Analysis Ready` | (R16, R18) |
| AC20 | seed state | `POST …/REQ-205/rerun`, then `POST …/REQ-205/close`, then `POST …/REQ-205/rerun` | first: a run exists and status is `Analysis Ready`; second: `Done`; third: `409`, no new run; across the whole suite no ticket ever becomes `Done` except through the close endpoint | (R18) |
| AC21 | the AC18 run | the report page body is read; then `POST api/pages/page-analysis-req-206/versions` | the body's first three lines are the §3.3 banner naming `REQ-206`, `version 1`, `satisfied`, `2 grading pass(es)`, then a blank line, then `# Requirements Analysis`; the human-edit request returns `400` and the page still has 1 version; `page-invoice-export` still has 1 version | (R17) |
| AC22 | `REQ-201` re-run once, then its page saved with the edited-requirement fixture as its body, which re-runs it | `GET api/tickets/REQ-201` | `changes.requirement_version == [1, 2]`, `changes.status == [satisfied, satisfied]`, `changes.counts` has the four list sections with Confirmed Facts `[4, 4]`, Ambiguities `[3, 2]`, Clarification Questions `[3, 2]`, Assumptions `[3, 2]`, and `changes.compare` names `page-analysis-req-201` with `a = 1, b = 2` | (R19) |
| AC23 | the AC22 state | `GET api/pages/page-analysis-req-201/compare?a=1&b=2` | `diff` begins with lines `--- version 1` and `+++ version 2` and contains at least one `+` and one `-` content line; `run_a` and `run_b` are the two runs, each with `status` and `counts` | (R20) |
| AC24 | the AC22 state | the server process is stopped and started again on the same data directory | `api/tickets/REQ-201` returns the same two runs, the same `changes`, the same page versions; `api/harness/versions` still lists `v1` | (R21, R31) |
| AC25 | any completed run | `GET api/runs/{id}` | validates against `RunRecord`; `messages` contains the full requirement body and every full tool result (a result longer than 220 characters appears in full in `messages` and cut to 220 + `…` in `trace[].detail`); `model_mode == scripted`, `model == scripted` | (R21) |
| AC26 | seed state | `POST api/batch`, then `GET api/harness/summary/v1` | 5 runs under `v1`; summary: `graded 5`, `grader_errors 0`, `completeness {5, 5, 1.0}`, `clarity {0, 5, 0.0}`, `depth {0, 5, 0.0}`, `revisions_needed 5` | (R22) |
| AC27 | the AC26 state | `POST api/harness/propose/v1` | a `pending` proposal from source `analyst`; `change.target == prompt`, `change.section == "### Ambiguities"`, `change.change` contains `Resolved by:` and `Edge case:`, `recurrence` starts with `5/5`, `evidence` has 5 entries each byte-equal to a gap recorded in a v1 run, `rejected` has ≥ 1 entry mentioning the edit error; `proposal_markdown` has the five headings; `instructions/v1.md` unchanged; `api/health` still reports `v1` | (R23) |
| AC28 | the AC26 state, with a hash of `runs.json` and the summary taken | the AC27 call | the hashes are unchanged; the analyst's recorded writes are exactly one file, `/proposal.md` | (R23) |
| AC29 | the AC27 proposal | `…/apply` (pending) → `…/reject` on a second human-submitted copy → `…/approve` then `…/apply` on the original | first apply: `409`; the rejected copy stays `rejected` and `api/health` still `v1`; after approve + apply: proposal `applied` with `applied_version v2`; `instructions/v2.md` equals v1 with the change text inserted after the last line of the `### Ambiguities` section and before `### Clarification questions`; `v1.md` unchanged; `api/health` reports `v2` | (R24, R25) |
| AC30 | two human-submitted, approved proposals: one with `section: "### Nonexistent"`, one with `target: "tool"` | each is applied | both return `422` with a message naming the section or the target; `api/harness/versions` lists no new version | (R25) |
| AC31 | the AC29 state | `POST api/batch`, then `GET api/harness/summary/v2` and `GET api/harness/compare?before=v1&after=v2` | 5 runs under `v2`, each with `len(grading) == 1` and `satisfied`; summary v2 all `{5, 5, 1.0}`, `revisions_needed 0`; comparison `verdict success`, `improved [clarity, depth]`, `regressed []`, `revisions_needed [5, 0]`, `attempts [10, 5]`, `runs [5, 5]` | (R22, R26) |
| AC32 | the AC31 state, before AC39 runs | `GET api/harness/compare?before=v2&after=v1` | `verdict regression`, `regressed [clarity, depth]`, `improved []` | (R26) |
| AC33 | the AC31 state | `POST api/harness/propose/v2` | `proposal: null` with `reason` `no criterion fails first attempt in a majority of graded runs`; no proposal stored | (R23) |
| AC34 | `REVIEW_MODEL_MODE=live` with `OPENAI_API_KEY` unset (and the role variables set to any string) | the server starts and `POST api/tickets/REQ-201/rerun` is called; the source is grepped | the run fails with an error naming `OPENAI_API_KEY` and the app never prompts; the source references `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `REVIEW_AGENT_MODEL`, `REVIEW_GRADER_MODEL`, `REVIEW_ANALYST_MODEL` and contains no `ANTHROPIC` string and no literal key | (R28) |
| AC35 `live` | `REVIEW_MODEL_MODE=live`, the lab's `OPENAI_*` pair exported, the three role variables set to the checklist's platform ids | `POST api/tickets/REQ-201/rerun` | the run ends with `status` in `{satisfied, max_iterations_reached}` within 40 turns, `len(grading) ≥ 1`, each pass has 3 criteria, every failing criterion carries a gap, `model` equals `REVIEW_AGENT_MODEL`, and a report-page version was written | (R28, R11, R12) |
| AC36 | the workspace-root `AGENTS.md` (if any) hashed before the suite | the whole offline suite has run | the hash is unchanged (or the file is still absent); every file named `AGENTS.md` the app wrote lies under the app's data directory or a run workspace | (R27) |
| AC37 | the server is running in `scripted` mode | `api/health` and the scripted model's registration are read | `model_mode == scripted`; the model's name is `scripted-stand-in` and its description contains the words `stand-in` and `fake` | (R29) |
| AC38 | seed state | `POST api/pages` `{title: "Invoice Export — Requirements", body: "REQUIREMENT: Invoice Export\n\nUsers shall export invoices quickly."}` twice, then `POST api/tickets` linked to the first | the first page id is `page-invoice-export-requirements` (the title's slug; the seed used `page-invoice-export`) with version 1; the second gets `page-invoice-export-requirements-2`; the ticket key is `REQ-206` | (R16, R20) |
| AC39 | the AC31 state (compare already taken) | a page `Stubborn Draft Probe` + linked ticket are created (one run under `v2`), then `GET api/harness/compare?before=v1&after=v2` | summary v2 now has `runs 6`, `graded 6`, clarity `{5, 6}`, `revisions_needed 1`; the comparison's `verdict` is `partial`, `improved [completeness, clarity, depth]` (passes are counted, not rated: 5→6, 0→5, 0→5), `regressed []` | (R26) |
| AC40 | the AC26 state | `GET api/harness/compare?before=v1&after=v1` | `verdict` is `no effect`, `improved []`, `regressed []`, `revisions_needed [5, 5]` | (R26) |

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the offline suite (§7) in `scripted` mode and report every criterion with cited evidence before calling anything done.
- Keep every run record, page version and proposal append-only; write results to files under the app folder — in this lab the workspace is the record and a new chat starts with no memory of this one (`[environment]`).
- Write `resolved-decisions.md` before the first line of code (§0) and keep it in the app folder; it is why the grader can later see what this build was built from (`[environment]`).
- Batch the pinned installs early, announce their wall-clock cost, and record `python3 --version` (§2, `[environment]`).
- Label the scripted model as a stand-in wherever it is named (R29).

**Ask First** (derived from the course's spoken trade-offs, CTX-C table; each names its lever or row)
- Changing which model serves which role, or collapsing the three roles onto one model — the **model tiering lever** (R28; CTX-C1). Changes cost and grading behavior without failing any offline criterion.
- Changing the **revision budget** from 3 (R12; CTX-C4) — changes the retry guarantee; AC16 pins the value.
- Changing the **simulated fetch-failure count** from 2 (R2; CTX-C10) — AC4 pins it.
- Changing either **model-turn cap** (40 / 12, R5; CTX-C11) — a runaway loop stops later or sooner, silently.
- Changing the **recurrence threshold** the analyst acts on (majority of graded runs, R23; CTX-C12) — the generator's reading of "most runs".
- Moving guidance out of the single instructions file into skills — **Ledger D1**: every batch summary before the move stops being comparable with those after it (rework), and R25's apply target changes.
- Removing the grader (**Ledger D2**) — retires AC14–AC17 and AC26–AC33.
- Making any human-approval point automatic: applying a proposal without the approve step (R24; CTX-C9) or letting a run mark a ticket Done (R18; CTX-C7) — a guarantee change no test would catch.
- Dropping either half of the "what changed" view — counts table or full diff (R19; CTX-C13).
- Editing the rubric text (R13): the scripted grader and every recorded summary assume these three criteria; a change forces re-running every batch (*project hardening*).

**Never**
- Invent evidence: an analyst proposal's `evidence` must be verbatim recorded gaps; a grader must not pass a criterion it cannot quote from the file (R11, R23).
- Answer when the system should abstain: report a run as finished when the turn cap stopped it (R5), or as satisfied when the budget was exhausted (R12), or propose a change when no criterion clears the recurrence bar (R23).
- Mutate fixtures (§5.1) to pass a test; never adjust the scripted model's replies to fit an assertion.
- Commit or print secrets; never hardcode or prompt for an API key; never read `ANTHROPIC_*` (R28, `[environment]`).
- Write into a requirement page from a run, or let the agent write under `/memories/` (R10, R7, R17).
- Apply a proposal the store has not recorded as `approved` (R24).
- Author, edit or depend on the workspace-root `AGENTS.md` (R27, `[environment]`).
- Use a root-absolute URL in the page, bind to a port other than 4000, or open a WebSocket (R30, `[environment]`).

## 7. Test Plan & Self-Verification

Real commands, run from the app folder with the venv active:

```bash
python3 --version                                    # record in resolved-decisions.md (§2)
python3 -m venv --system-site-packages .venv && . .venv/bin/activate
pip install deepagents==0.7.11 langchain==1.3.18 langchain-core==1.6.1 langchain-openai==1.6.0 \
            langgraph==1.2.11 openai==3.6.0 pydantic==2.13.5 python-dotenv==1.2.3 pytest httpx
REVIEW_MODEL_MODE=scripted REVIEW_DATA_DIR=$(mktemp -d) python -m pytest tests/ -k "not live" -q   # AC1–AC34, AC36–AC40
REVIEW_MODEL_MODE=scripted python -m uvicorn app.main:app --host 0.0.0.0 --port 4000 &              # the served app (R30); run in the background
REVIEW_MODEL_MODE=live REVIEW_AGENT_MODEL=... REVIEW_GRADER_MODEL=... REVIEW_ANALYST_MODEL=... \
  python -m pytest tests/ -k "live" -q                                                               # AC35 only; needs the lab's OPENAI_* pair
```

The test module names are importable identifiers (`tests/test_agent_loop.py`, `tests/test_verification.py`, `tests/test_events.py`, `tests/test_learning.py`, `tests/test_lab.py`, `tests/test_live.py`); each criterion group starts its own server on a fresh `REVIEW_DATA_DIR` (AC24 restarts one).

**Reporting duty.** The building agent MUST report results per acceptance criterion — AC1 through AC40 — with cited evidence: the pytest output line for the test, and the file paths of the artifacts the criterion inspects (a run record, `instructions/v2.md`, the proposal). "Should pass", "looks correct", or a criterion with no cited output is treated as a failure — it means the test was not run. The report is written to `acceptance-report.md` in the app folder (the workspace is the record).

## Runtime (lab) `[environment]`

Everything in this section is environment-imposed; none of it is course provenance, and none of it appears in CTX-A or CTX-B.

**Container.** Debian, non-root user, Node 22, Python 3 with venv, `sqlite3`, git, build tooling. Preinstalled Python: `fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`; Node: `express`, `cors`, `better-sqlite3`, `vite`, `nodemon`. Nothing else — no vector stores, no embedding models, no ML frameworks. Outbound network works, so the §2 installs succeed, but each costs wall-clock time inside the session: batch them early and announce the cost. Create the venv with `--system-site-packages`; where a course pin and a preinstalled copy differ, the course pin wins inside the venv (§2: `openai`, `python-dotenv`). The Python minor version tracks the image and is not stated: run `python3 --version`, record it, and stop with a report if a course pin refuses the interpreter. Memory is finite and shared with the coding agent's own process; this pipeline holds no model resident (all models are called over the network), so no release-before-load rule is needed.

**Preview.** One server, port 4000, bound to `0.0.0.0`, serving both the page and `api/`; nothing else is previewable. Every URL inside the page is relative — the preview is reverse-proxied under a path prefix, so a root-absolute path resolves against the IDE. HTTP only: WebSocket upgrades are not proxied; streaming responses work. Long-running servers run in the background.

**Workspace.** The workspace is the record: a new chat starts with no memory of an earlier one and the grader sees only what is on disk, so decisions (`resolved-decisions.md`), resolved values and results (`acceptance-report.md`) are written to files, never left in chat. The workspace-root `AGENTS.md` is rewritten by the IDE at every boot and is never authored (Never tier); this app's agent-harness files of that name live in app-owned folders only (R27). Every tool call is visible to the learner.

**Model/provider.** The container exports `OPENAI_API_KEY` + `OPENAI_BASE_URL` and `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL`, each base URL pointing at the platform proxy; the app reads the first pair only (R28). The platform's model set is not enumerated here because it changes; the build agent names a platform model per role in `resolved-decisions.md` (§2), and the course's own model ids are provenance only (CTX-D).

**Environment failure modes** (written as a CTX-B entry would be, but these are the lab's, not the course's):

- **EF1 — Root-absolute URL under the proxied preview.** *Symptom:* the page loads but every button and API call 404s or hits the IDE. *Cause:* a URL beginning with `/` resolves against the proxy root, not the app's prefix. *Fix:* relative URLs everywhere. Enforced by R30, AC2.
- **EF2 — Guidance vanishes from the workspace-root `AGENTS.md`.** *Symptom:* instructions written there are gone after a reboot and the agent's behavior silently reverts. *Cause:* the IDE rewrites that file at boot. *Fix:* the harness's instructions file lives under the app's data directory and run workspaces. Enforced by R27, AC36.
- **EF3 — Server not reachable from the preview.** *Symptom:* a working app on `127.0.0.1` or another port shows nothing. *Cause:* only `0.0.0.0:4000` is proxied. *Fix:* R30. Enforced by AC2.
- **EF4 — A WebSocket that never connects.** *Symptom:* live updates hang. *Cause:* upgrades are not proxied. *Fix:* poll or stream over HTTP. Enforced by R30, AC2.
- **EF5 — A course pin refuses the container's Python.** *Symptom:* `pip install` of a course pin fails to build. *Cause:* the image's minor version may be below the course's `>= 3.12` floor. *Fix:* check first and stop with a report rather than loosening a pin silently (§2).
- **EF6 — A live run asks for a key.** *Symptom:* the app prompts for or logs a key. *Cause:* code that does not read the lab's exported names. *Fix:* R28, AC34.

## Course Context Pack (embedded — agent-readable)

Concepts only; no code from the course appears here. Anchors are position-independent.

### CTX-A. The pattern

Four loops nested around one agent, each existing for one reason:

`event trigger → fetch requirement by key → agent loop (staged file writes) → grader scores the file, retries with feedback → run recorded → [across runs] analyst proposes → human approves → apply as new instructions version → re-run batch → compare`

- **Agent loop** (Lessons 2, 4): the model receives the task, calls tools, observes results, repeats until it declares completion; here the tools are one fetch tool and the file tools, and the deliverable is a file the harness can open rather than text to parse out of a message. Exists because one model call is rarely enough for multi-step work.
- **Verification loop** (Lessons 2, 5): a grader reads the finished file against explicit criteria and sends it back with feedback; exists because "finished" does not mean "good enough", and explicit criteria make cheaper models viable on harder tasks.
- **Event-driven loop** (Lessons 2, 6): the loop runs where the work already happens — a ticket created, a requirement edited — instead of someone opening a tool and pasting; exists because an agent that is not easy to use is not used.
- **Learning (hill-climbing) loop** (Lessons 2, 7): an analyst reads traces from many runs, finds what the agent is corrected on every time, proposes one harness change, a human approves, the change is applied and its effect measured; exists because agents are non-deterministic — the truth is in the traces, not the code — and a loop that fixes one run at a time starts from the same place tomorrow.
- **Why the records are rich:** every message, every tool argument and result, every grading pass with the file as it stood, and the instructions the run was given — so a later diagnosis can see what the agent was told, what it produced, what it had to be told afterwards, and what it then fixed.

Course-term name map (provenance, not binding): the course calls the instructions file `AGENTS.md` (one slide: `Agent.md`); the fourth loop "hill-climbing", "learning" or "self-improvement" loop (one slide: "application loop" for the third); the fetch tool `fetch_requirement` (two snapshot files: `fetch_requirement_from_jira`); the harness "Deep Agents" / "DeepAgents"; the analyst "Engine" in LangChain's own docs agent (Lesson 2) and "hill climbing agent" in code; report sections Confirmed Facts / Ambiguities / Clarification Questions / Assumptions / Summary; grader verdict strings `satisfied` / `needs_revision` (plus the library's `failed` for a malformed rubric, folded into `grader_error` here — *project hardening*, since this build's rubric is fixed text); ticket statuses Open / Analysis Ready / Done. Presentation-only constants dropped by declaration: the course's trace run names and tags, tracer project names, the demo's blue/green theme colours.

### CTX-B. Failure-mode catalog

- **CTX-B1 — Transient fetch failure.** *Symptom:* the external lookup returns an error (unreachable, timed out) and a naive agent gives up or hallucinates the document. *Cause:* external systems fail transiently. *Fix:* retry the same call with the same arguments; the instructions and the tool's own description both say so. Enforced by R2, AC4.
- **CTX-B2 — First draft rejected.** *Symptom:* the agent finds the ambiguity and explains why it is unclear but never says what would resolve it or what could go wrong. *Cause:* nothing checks "done" against "good enough". *Fix:* a grader with explicit criteria sends the draft back with the exact gap; the second attempt adds the missing lines. Enforced by R11, R12, AC14, AC15.
- **CTX-B3 — Leftover file from a previous run.** *Symptom:* the agent reads a completed analysis left on disk and skips stages. *Cause:* a shared workspace across runs. *Fix:* a fresh workspace per run, removed afterwards. Enforced by R8, AC10.
- **CTX-B4 — Missing instructions, silent fallback.** *Symptom:* a plausible but bad review. *Cause:* the harness ignores a missing memory file and runs on the system prompt alone. *Fix:* fail loudly before the run starts. Enforced by R6, AC8.
- **CTX-B5 — The agent rewrites its own instructions.** *Symptom:* the instructions drift mid-run. *Cause:* the instructions file sits in the same writable filesystem as the report and the agent has an edit tool. *Fix:* deny writes to the memory path by permission, not by asking nicely. Enforced by R7, AC9.
- **CTX-B6 — Runaway retrying.** *Symptom:* the model keeps retrying past the point where retrying makes sense. *Cause:* the normal stop (writing the Summary) never arrives. *Fix:* a model-turn cap, with a distinct "turn limit reached" status so an exhausted budget never reads as a finished review. Enforced by R5, AC7.
- **CTX-B7 — Ambiguous edit.** *Symptom:* an `edit_file` call names an `old_string` that matches more than once; some drafts end up with duplicated headings. *Cause:* exact-string editing on a file with repeated fragments. *Fix:* the tool rejects the edit; the agent reads the file and retries with an exact match; a failed edit counts for no stage. Enforced by R9, AC11.
- **CTX-B8 — Grading the conversation instead of the file.** *Symptom:* the grader passes criteria the file does not satisfy, judging by resemblance. *Cause:* the grader is handed the transcript and the transcript reads as if the work were done. *Fix:* give the grader a file-reading tool, make it read the deliverable, and require a verbatim quote with a line number before any pass; apply labelled-line criteria literally. Enforced by R11, R13, AC14.
- **CTX-B9 — Revision budget exhausted.** *Symptom:* the last grading pass still says needs-revision. *Cause:* the agent cannot or will not satisfy a criterion. *Fix:* stop at the budget and report `max_iterations_reached`, never "satisfied". Enforced by R12, AC16.
- **CTX-B10 — Grader failure counted as a pass.** *Symptom:* batch rates look better than the evidence. *Cause:* a run whose grader errored carries no verdict either way. *Fix:* record it as `grader_error`, exclude it from every denominator, report the count. Enforced by R14, R22, AC17.
- **CTX-B11 — Counts alike, content changed.** *Symptom:* after a requirement edit the bullet counts look the same, so the re-run seems pointless. *Cause:* the agent finds roughly as many ambiguities either way while the text changed completely. *Fix:* show the counts table and the full text diff together. Enforced by R19, AC22, AC23.
- **CTX-B12 — Acting on noise.** *Symptom:* a harness change chasing a one-off. *Cause:* one run's quirk mistaken for a pattern. *Fix:* the analyst starts from first-attempt pass rates across the batch, acts only on a criterion failing in most runs, and lists everything else as rejected with the reason. Enforced by R23, AC27, AC33.
- **CTX-B13 — An unmeasured harness change.** *Symptom:* no confidence that the merged change helped, or a silent regression. *Cause:* no eval run after the change. *Fix:* re-run the same batch under the new version and compare first-attempt passes per criterion; name the verdict. Enforced by R26, AC31, AC32, AC39, AC40.

### CTX-C. Decision background

**How to read the provenance notes.** A *litmus branch* is how an argued subject was resolved: a **row** (both sides shown working; the sides differ in a component, identity or role — it is in the Ledger), a **bake-in** (the course showed or warned against the other side as a failure — it is a business rule, the other side only narrative), or a **lever** (the sides differ only in a value — it is a body default with an Ask-First entry). A *post-build lever* is a value you may change after the build without re-opening a Ledger question. A *contradiction* is a value the course set two ways; it passes the *stakes test* only if choosing the other side up front would change structure, semantics or a guarantee — otherwise its value is chosen by the *lever-value rule*: (1) the value the narration states in the lesson that introduces the concept; (2) else the end-to-end application's config; (3) else the most frequent value, earliest-taught on ties. A *substitution row* is a Ledger row whose Default departs from the course's realization because the course's needs setup the learner may not have — the *heavy bar*: a credential, a paid account, admin- or container-level setup, or special hardware (plain network access is not heavy). "Lightest" is decided by *realization tier*: (1) ships with the language's standard distribution, (2) an embedded library, (3) a locally served process. Environment terms: a dimension is **ANSWERED** (the lab fixes it), **CONSTRAINED** (narrowed, not fixed) or **KEPT** (unchanged); an option is **untakeable** here when it needs a credential the lab does not supply or would make the offline suite wait on a person. The *Never tier* is the third list in §6 Standing Permissions: actions forbidden for the whole build.

- **CTX-C1 — Model tiering per role** (→ R28 lever; Ask First). Lesson 2: loop engineering at the agent-loop level "means that you're selecting the right model — match the model intelligence to the complexity of the incoming task in order to optimize cost"; the verification loop is "particularly powerful when you want to use a cheaper model on challenging tasks". Lesson 5: the same model serves agent and grader, "but having a different model for grader is a common production choice". Lesson 7: the analyst runs on the stronger model because reading five full traces and finding what recurs "is the one job the cheaper model does unreliably". In this lab the provider is constrained, not the tiering, so the argument lives in the three role variables as a lever.
- **CTX-C2 — Instruction placement** (→ Ledger D1). Lesson 3 names three ways to instruct a deep agent: the system prompt (set at creation, used every call), an always-loaded memory file (loaded each run, editable over time — "use it for what is always true … it costs context on every call, so it should stay short"), and skills (a directory per procedure behind a frontmatter description; only the description is loaded until the agent reads the body — "twenty skills cost twenty lines of context, not twenty documents"). The primer's poet used memory plus four skills and its trace showed each skill read only when that form was written; the review agent used the memory file alone with a system prompt that only points at it ("instructions placed there carry the same weight"). Both working → row.
- **CTX-C3 — The verification loop and its rubric** (→ Ledger D2; R11–R13). Lesson 5: completeness, clarity, depth, each pass/fail, all three must pass. The course's grader notes say "what does done mean lives in this text rather than in a numeric threshold". Lesson 5 also names the removal setting: budget 0 "will have the same basic agent loop you built in the last lesson"; Lesson 2: loops compose and "you don't need the verification loop per se". The bare loop worked in Lesson 4 → row, with the grader present as the argued default. **Grader type** — one deck line says graders "can either be deterministic or agentic (LLM as a judge)"; nothing narrates or builds a deterministic grader and the completeness criterion as taught needs judgment, so this stays narrative, not a row.
- **CTX-C4 — Revision budget** (→ R12 lever; contradiction). 3 in Lesson 5's narration and notebook and in the batch runner; 2 in the course's shipped event-driven app. Stakes: a value, so a lever; narration selects 3.
- **CTX-C5 — Event surfaces: real versus simulated** (→ pinned in §2; §1 item 1). Lesson 6 demonstrates the review agent in a real Slack direct message and team channel, and triggered by real Jira and Confluence automations, then lists what running it yourself needs: Python 3.12+, an OpenAI key, a Slack workspace where you can install an app (two tokens), an Atlassian Cloud site with API tokens and automation rules, and a tunnelling service to expose the local agent. The course's shipped code is a simulated Jira+Confluence "so this lesson runs with no Atlassian account and no API tokens", with one automation function as "the seam for a real integration: swap the store's page/ticket lookups for the REST APIs and call it from an actual webhook endpoint. Nothing about the agent or the loop changes." Keyed → realization row in a standalone build, with the simulated surfaces as default because they carry the taught behavior keylessly; here every real alternative is untakeable, so the row is pinned.
- **CTX-C6 — Hosted tracing** (→ pinned in §2; §1 item 2). Lesson 3 shows a hosted trace of the poet run and says later lessons also keep "a local trace that won't require a login"; the course's notebooks link public traces that need no account. Keyed, optional, not the only carrier of the traces → pinned to the local record here.
- **CTX-C7 — A human closes the ticket** (→ R18 bake-in). Lesson 6 README: "A human, not the agent, decides when a ticket is actually Done … the agent never closes its own work"; Lesson 2's third oversight point (approve outputs before delivery). Warned side: automation closing its own work → bake-in.
- **CTX-C8 — Criteria matched by position** (→ R22). The course's batch code matches criteria by index in rubric order because "the grader paraphrases the criterion text differently from run to run, sometimes dropping the leading label, sometimes swapping quote characters".
- **CTX-C9 — Human approval; the agent proposes, code applies** (→ R24, R25 bake-ins; Ask First). Lesson 2: harness and code changes "must flow through systematic human review before final system deployment", and confidence in a merge comes from running the eval suite. Lesson 7: the proposal file exists "to be reviewed by a human in the loop to approve or reject", and the change is applied only after "assume human-in-the-loop reviewed this proposal and approved". Course code notes: the analyst "proposes and does not apply … that keeps the edit reviewable, deterministic, and means a proposal about tools or configuration can be read and rejected rather than half-applied"; the analysis is scoped to the prompt while the schema still names tool, grader and configuration. Warned side (auto-merge, model-performed edits) → bake-in.
- **CTX-C10 — Simulated fetch failures** (→ R2 lever; contradiction). Lesson 4 narration and notebook table: two failures before success, and the pre-recorded trace shows a 503 and a timeout; the helper's shipped default and the batch runner: 0 ("only adds turns and noise"). A value → lever; narration selects 2.
- **CTX-C11 — Turn caps** (→ R5 levers). 12 for the single review ("six stages, plus headroom for the simulated retries and the closing message"), 40 whenever the grader is present ("several verification passes cost more turns than one review"); the primer used 30. Lesson 4: the cap "is not the normal stopping mechanism … max_turns matters when that path fails".
- **CTX-C12 — Recurrence threshold** (→ R23 lever). Lesson 7 and the analyst's instructions: "a criterion failing in most runs is a property of the agent. A problem appearing in one run out of five is not a pattern." The spec's "more than half of graded runs" is the generator's reading of those words.
- **CTX-C13 — Counts and diff together** (→ R19 bake-in). Lesson 6 README walkthrough: bullet counts "often look similar before and after … the content changed completely even though the shape didn't. That's the point of showing both the counts table and the full text diff together, not just one or the other."
- **Other bake-ins from course code:** write-deny on the memory path "rather than relying on the instructions telling it not to" (R7); fresh workspace per run so "two tickets analyzed back to back never see each other's leftover analysis" (R8); the grader given a file tool "or it grades the conversation rather than the file the agent actually wrote" (R11).
- **Narrative only (framing, not builder choices):** the four-level taxonomy and the "Russian doll" nesting (Lesson 2); prompt/context/harness/loop engineering as disciplines; the two improvement categories — procedural (prompts, tool descriptions, skills) versus memory (user preferences, memory consolidation), of which only prompt edits were built (§1 item 5); the four human-oversight points, two built (R18, R24), two not (§1 item 4); the deep-agent pillars the review agent does not use (§1 item 9).

**Mined trade-off table** (every spoken trade-off, its lesson, its disposition and the tie-breaker that decided it):

| subject | lesson | disposition |
|---|---|---|
| model capability per role (cheaper agent/grader, stronger analyst; separate grader model) | 2, 5, 7 | lever R28 — environment: the model/provider dimension is CONSTRAINED to platform models, so the tiering argument stays a body lever + Ask First (CTX-C1) |
| instruction placement: always-loaded file vs skills | 3 | row D1 — both sides shown working; component choice |
| verification loop present vs budget 0 | 2, 5 | row D2 — a limit value that removes a component; the bare loop shown working in Lesson 4 |
| revision budget 3 vs 2 | 5 (+ shipped app) | lever R12 — tie-breaker 2 (value only); contradiction, narration wins |
| real Slack/Jira/Confluence vs simulated surfaces | 6 | row (realization) → every real alternative untakeable here → pinned §2, table row (CTX-C5) |
| hosted tracing vs local record | 3 | row (realization) → untakeable here → pinned §2, table row (CTX-C6) |
| human approval of harness changes vs automatic merge | 2, 7 | bake-in R24 — tie-breaker 1 reading: the course warns against the unreviewed side |
| analyst proposes / code applies vs model-performed edit | 7 (code) | bake-in R25 — warned side |
| grader reads the file vs judges the transcript | 5 (code) | bake-in R11 — tie-breaker 1: the transcript side shown failing |
| simulated fetch failures 0 vs 2 | 4 | lever R2 — tie-breaker 2; contradiction, narration wins |
| counts table vs full diff | 6 | bake-in R19 — the course argues both; one-only is the warned side |
| recurrence threshold ("most runs") | 7 | lever R23 — spoken heuristic quantified, generator's reading |
| turn cap values | 4, 5 | lever R5 — value only |
| deny writes to instructions vs trust the prompt | 4 (code) | bake-in R7 — warned side |
| shared vs fresh workspace per run | 4, 6 (code) | bake-in R8 — tie-breaker 1: leftover file shown causing skipped stages |
| human closes the ticket vs agent closes | 6 | bake-in R18 — warned side |
| grader deterministic vs LLM judge | 2 (deck line only) | narrative — presented, never argued or built (CTX-C3) |
| loop composability / nesting | 2 | narrative framing, except where it lands on D2 and the event-surfaces row |
| procedural vs memory improvements | 2 | narrative — taxonomy; memory never built (§1) |
| four human-oversight points | 2 | narrative framing; built points are R18/R24, unbuilt are §1 |

### CTX-D. Perishable assumptions

The concepts in CTX-A…CTX-C are durable. The names below are era-specific — **treat them as search keywords against current docs, not guaranteed imports**:

- Harness: `deepagents` 0.7.11 — `create_deep_agent(model, tools, system_prompt, memory=[...], skills=[...], backend=, permissions=, middleware=, checkpointer=, response_format=)`; `FilesystemBackend(root_dir, virtual_mode=True)`; `FilesystemPermission(operations, paths, mode)`; `FilesystemMiddleware(backend, tools=[...])`; `RubricMiddleware(model, max_iterations, tools, system_prompt, on_evaluation)` — flagged beta in this era, invoked by passing a `rubric` key on invocation state, keeping its terminal status in a private `_rubric_status` state key; its default grader system prompt is *replaced*, not extended, when a custom one is passed; its `GraderResponse` result values `satisfied` / `needs_revision` / `failed`.
- LangChain stack: `langchain` 1.3.18 `ModelCallLimitMiddleware(run_limit, exit_behavior="end")`, `langchain.tools.tool`; `langchain-core` 1.6.1 message types (`ai`, `tool`, `human`, content as a list of blocks on current models and a plain string on older ones); `langgraph` 1.2.11 `InMemorySaver`; `langchain-openai` 1.6.0 and the `openai:<model>` provider prefix.
- The course's own model ids: `openai:gpt-5.4-mini` (agent, grader, batches) and `openai:gpt-5.5` (analyst) — provenance only; never assume the lab proxy serves them. Per-million-token prices the course printed (`gpt-5.5` 5.00/30.00, `gpt-5.4-mini` 0.75/4.50) and the `tiktoken` `o200k_base` estimate — dropped (§1 item 11).
- **Request-parameter compatibility:** the course never sets sampling parameters (temperature, top-p) on any call; do not add them — model families of this era reject some of them, and an unstated one surfaces as a live API error in the first keyed run.
- Tracer: `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` (older aliases `LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`) — the seam for §1 item 2.
- Web: the course's demo used Flask on port 5050 with Jinja templates; this build uses the preinstalled FastAPI/uvicorn on port 4000.
- Install era: Python ≥ 3.12 required by the course's lock (numpy 2.5 / pandas 3.0 do not build below it); `flask` floored but absent from the lock.

### CTX-E. Provenance map

Nothing in this spec requires platform, notebook or repository access. Lesson numbering is the transcripts' (an Introduction counted as Lesson 1; the course's notebook folders are numbered one lower, and its README uses a third scheme).

| Lesson (transcript numbering) | Contributed |
|---|---|
| 1 — Introduction | the four loops previewed; the requirement-review example (CTX-A) |
| 2 — Overview of Loop Engineering | CTX-A loop rationale; CTX-C1 tiering; CTX-C3 composability; CTX-C9 human review and eval before merge; narrative items (taxonomy, oversight points, improvement categories); Slides 2.1–2.13 read (2.2–2.13 narrated — ranked with the transcript; 2.1 deck-only; the "Type:" grader-kind line on Slide 2.6 and the "APPLICATION LOOP" label on 2.12 are deck text not narrated) |
| 3 — Deep Agent Primer | CTX-C2 instruction placement (D1); CTX-C6 tracing; CTX-C11 primer cap 30; harness API names (CTX-D); Slides 3.1–3.5 read (3.2–3.5 narrated; 3.1 deck-only) |
| 4 — Agent Loop | CTX-A agent loop; CTX-B1, B3, B4, B5, B6, B7; CTX-C10, C11; R1–R10; the report shape (§3.1); Slides 4.1–4.5 read (4.2–4.5 narrated; 4.1 deck-only) |
| 5 — Verification Loop | CTX-A verification; CTX-B2, B8, B9, B10; CTX-C3, C4; R11–R15; Slides 5.1–5.4 read (5.2–5.4 narrated; 5.1 deck-only) |
| 6 — Event-Driven Loop | CTX-A event loop; CTX-B11; CTX-C5, C7, C13; R16–R21; the seed-scenario shape and the store (§2); Slides 6.1–6.6 read (6.2–6.4, 6.6 narrated; 6.1, 6.5 deck-only); the Slack/Jira/Confluence demos and setup steps are screen recordings narrated in the transcript, not slides |
| 7 — Learning loop | CTX-A learning loop; CTX-B12, B13; CTX-C8, C9, C12; R22–R26; the proposal and comparison schemas (§3.4); Slides 7.1–7.2 read (7.2 narrated; 7.1 deck-only) |
| 8 — Conclusion | recap only |
| **Environment (coding-agent-lab)** — not a lesson | every `[environment]` fact: the deliverable's shape (§1), the container, venv and pin-precedence rules (§2), the key and model-role variables (R28), port 4000 / relative URLs / HTTP only (R30), the workspace-root `AGENTS.md` rule (R27), the `## Runtime (lab)` section and its failure modes EF1–EF6, the `[environment]` paragraphs in §0, and the Environment Resolutions table |

Slide-sourced facts carry no conflict with code or narration except the ones already recorded above (deck lesson numbering absent; the third loop once labelled "application loop"; `Agent.md` vs `AGENTS.md`; the requirement's wording differing between slides and narration — all presentation-only and resolved in favour of transcripts and code).

---

**Status:** v1 · Course: Loop Engineering with LangChain DeepAgents · Environment: coding-agent-lab · Learner project: [the requirements-review loop app — fixed by the lab; see §1 "Adapting this beyond the lab"] · Living document: when the building agent produces something unexpected, add the missing constraint to the relevant rule or criterion here and re-run.
