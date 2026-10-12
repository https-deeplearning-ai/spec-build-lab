# Spec: Requirements Review Loop Service — Coding-Agent-Lab Build

> **What you're building:** a single-server web app that reviews software requirements through four engineered loops. You create a ticket on the app's Jira-like board and watch the review agent fetch the requirement by id, draft a five-section analysis file, get sent back by a rubric grader, and pass on its second try; you edit the requirement page and watch the review re-run on its own; then you open the Learning page, run a batch of five reviews, read the analyst's proposed instruction change, approve it, re-run the batch and watch five first-attempt failures become five first-attempt passes. Answering the gate's first question with the recommended baseline builds all of this end to end, and the build is COMPLETE when the offline acceptance suite passes — the lab's ambient model credentials unlock only the `live` criteria and live use of the finished app.
>
> This file is self-contained: the embedded Course Context Pack replaces every external course reference, and nothing here requires platform access. `(CTX-X)` anchors mark course-derived knowledge. The Decision Ledger below holds every point where the build could diverge, each pinned to one course-derived default, so the spec builds as-is with no intake; the Environment Resolutions table under it shows which learner dimensions the lab fixed.
>
> Generated from the *Loop Engineering with LangChain DeepAgents* notebooks + transcripts + slides on 2026-10-12, guide @ `11b3673`, overlay `coding-agent-lab` @ `f9cc86d`. Hand-evolved since 2026-10-12.

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

   *[environment] In this lab the structured question tool is a fenced `choices` block: explain in prose above the fence, put the fence last in the message with one option per line, and end the turn there. A click sends the option line verbatim, and a typed answer naming an option counts identically. Only the latest message's buttons stay live, so never ask the person to go back and change an earlier answer — re-ask it as a new question.*

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

   *[environment] Each per-row question is its own `choices` fence, preceded by a line of the form `**Question N of M — <decision>**` so the person and you can both see that nothing was skipped. A click and a typed answer naming an option are equivalent. Because only the latest message's buttons stay live, a changed answer to an earlier row is collected by asking that row again as a new question, never by pointing back at an old message.*

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

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option. Rows are grouped learner → design, in pipeline order within each group. The row id prefixes are `L` (learner) and `D` (design); business rules are `R<n>` and are a different namespace. An alternative a learner cannot take in this build mode is not offered as an option; it is listed in §1 Not Included as `unavailable` with the seam it would use. Each non-default option states which acceptance criteria it retires or alters; the §7 report lists a retired criterion as retired, not failed.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L1 | learner | **Scope boundary.** Present the §1 "Not Included" list *inside this question*, item by item with each item's handling tag, and ask whether the person wants any item brought back or any further exclusion added. | (empty — the pattern demands nothing of this dimension) | **Keep as-is**: every §1 exclusion stands and the full acceptance set in §5 is built. | (1) Keep the list as-is; (2) Bring an item back — name it in free text; the item's §1 tag says what happens: `restorable` items are added to the build as an additive extra that changes no existing criterion — this spec supplies no parameters or criteria for them, so the §7 report lists each as built but unverified; `named-not-built` items are buildable, but before building them the agent tells the person that the course never built them and this spec supplies no parameters and no acceptance criteria, so their design is the build agent's own invention — the §7 report lists each as invented and unverified; `owned-by-row` items are decided on the row named, never here; `unavailable` items cannot be restored in this build mode. A further exclusion is also free text and must name the acceptance criteria it retires. | Bringing an item back adds unspecified work with no oracle; dropping one retires criteria the §7 report must then list as retired, not failed. | learner |
| D2 | design-argued | **Where the agent's revisable instructions live** (the artefact the learning loop edits). | The instructions the learning loop revises are **available to the review agent on every run** — the always-on part in its context at start, any on-demand part discoverable by description and readable with its own file tool; the review agent **cannot write them**; a human-approved apply step edits them **outside the agent**; and the analyst can read the exact version each batch ran under. | **One always-loaded instructions file** (`memories/AGENTS.md` inside each run's workspace, seeded from the app's current instructions). | (a) One always-loaded instructions file (course default); (b) skill files with progressive disclosure — a name and one-line description always in context, the body read on demand (the course's primer shows this working). Under (b) the app keeps `data/instructions/AGENTS.md` as the store the apply step edits, but each run's workspace receives it as the body of one skill, `/skills/requirements-review/SKILL.md`, behind the frontmatter `name: requirements-review` / `description: How to write the requirements review report: stages, section shapes, labelled lines.`, instead of as `memories/AGENTS.md`, and writes under `/skills/` are denied instead of under `/memories/`. The scripted review's label condition (§5 review script, step 5) keys on the always-loaded text, which under (b) holds only the frontmatter, so under (b) the review script makes one extra turn — `read_file(file_path="/skills/requirements-review/SKILL.md")`, right before its `write_file` stage — and tests the `Resolved by:` / `Edge case:` condition against that read result instead of the system prompt. AC34 then asserts exactly what it asserts under (a) (every v2 run passes on its first grading pass with both labelled lines), and AC35–AC37 hold unchanged. Altered under (b): AC4 (the per-run copy is `data/workspaces/<run>/skills/requirements-review/SKILL.md`, not under `memories/`) and AC11 (the write probe targets `/skills/requirements-review/SKILL.md` and must be denied). No criterion retires. (c) a fixed system-prompt string in code, snapshotted into each batch's run history as `data/run_history/<label>/AGENTS.md` so the analyst can read it; the apply step then becomes a code change a person makes. Retired under (c): AC31, AC32, AC33 (there is no apply endpoint), AC34–AC37 (each needs the suite to apply a change, which a code edit cannot be) and AC10 (there is no instructions file to go missing). Altered under (c): AC1 (no `data/instructions/AGENTS.md` is created), AC4 (the only app path holding `AGENTS.md` is the batch snapshot) and AC11 (the write probe no longer targets the instructions, so its denial assertion drops; the read-probe and unchanged-`tickets.json` assertions stand, and `instructions` equals the in-code prompt). | (CTX-C2) Lesson 3 argues the trade-off aloud: the always-loaded file "costs context on every call, so it should stay short" and is "for what is always true"; skills cost "twenty lines of context, not twenty documents" and pull detail in only when it applies; the system prompt is fixed when the agent is created. Litmus: design-argued, two-sided — the course demonstrated both the file (review agent) and skills (poet primer) working; neither is shown failing. | course+learner |
| D3 | design-structural | **Grader type** — what scores the finished analysis against the rubric. | A grader **distinct from the review agent** scores the **file the agent wrote** (never the conversation) against every criterion, returns pass/fail per criterion with a `gap` text on each failure, and its verdict alone decides retry-with-feedback or stop. | **LLM judge inside the harness** (the agent framework's rubric middleware, given a `read_file` tool and the grader instructions in R8). | (a) LLM judge inside the harness (course default); (b) a deterministic checker in code — exact for the two labelled-line criteria (clarity: every Ambiguities bullet has an indented line beginning `Resolved by:`; depth: every Ambiguities bullet has an indented line beginning `Edge case:`), and for completeness the declared proxy rule **each of the four list sections has ≥ 1 bullet and Summary has ≥ 1 word** (R3's completeness test; a proxy, because code cannot tell whether every clause of the requirement is addressed); it emits the canonical criterion names on every pass and the same `gap` texts as the §5 grader script. Retired under (b): AC13 (the `[[never-satisfied]]` rule is a scripted-grader behaviour; the checker passes depth once the lines exist), AC14 and AC27 (code does not raise, so `grader_error` is never produced, and AC27's counts rest on one) and AC15 (the fixture rubric is never unevaluable to code, so `failed` is never produced). Altered under (b): AC9 (pass 1 carries the canonical names, not the paraphrased forms; every other assertion stands) and AC28 (its paraphrased-name assertion drops; the summary-key and count assertions stand). | (CTX-C3) The course's overview slide states graders "can either be deterministic or agentic (LLM as a judge is a classic example)", and the human-oversight slide names "a human acts as the grader" — the course names a human grader; it is unavailable in this build mode, because the offline suite is the completion gate and cannot wait on a person, so it is not offered here (Not Included #7). The course built only the LLM judge and had to force it to read the file and quote line numbers because it otherwise "passes criteria the file does not satisfy". Switching cost: a deterministic checker cannot judge completeness, only its proxy. Litmus: design-structural — the grader box changes owner (model → code → person); the course names the types without arguing a trade-off, so not design-argued. | course+learner |

## Environment Resolutions

This spec was generated for the `coding-agent-lab` environment: the six learner-context dimensions were each derived from the course first and then resolved against the lab, not skipped.

| Dimension | Resolution | Where the Invariant lives now |
|---|---|---|
| project | **ANSWERED** — the lab fixes the assignment | §1 Objective. Invariant empty. |
| data/inputs | **ANSWERED** — inputs are seeded into the workspace | §5 fixture corpus. Invariant empty. |
| goal | **ANSWERED** — the lab fixes what "working" means | §1 + the acceptance criteria. Invariant empty. |
| model/provider | **CONSTRAINED** — the built app needs an LLM, so platform models only, keys and base URL read from the environment, never asked for | §2 (role variables, key variables) + CTX-D. Derived invariant (the model must support native tool calling and structured output) → R21, exercised by AC40 and AC41 (`live`); the key-handling constraint → R20, exercised by AC38 and AC39. |
| environment | **ANSWERED** — the container | §2 + the Runtime (lab) section. Derived capability invariants moved to rules: virtual-root workspace and fresh workspace per run → R7 (AC11 probes above the root, AC12 checks removal); instructions file must exist before a run → R6 (AC10); run records persist as files across restarts → R10 and R16 (AC18, AC26). |
| scope-boundary | **KEPT** | Ledger row L1. Invariant empty. |

## 1. Objective

A single-server web app (one process, port 4000, page and API together) that runs a **requirements-review agent inside four nested loops** — an agent loop that fetches a requirement by id and writes a structured analysis file; a verification loop whose grader scores that file against a three-criterion rubric and sends it back with feedback until it passes or the budget runs out; an event-driven loop that triggers a review when a ticket is created or its linked requirement page is edited and writes the report to a separate agent-owned page; and a learning loop that runs a batch of reviews, finds the correction the grader makes every time, proposes one instruction change for human approval, applies it, and proves by re-running the batch that first-attempt pass rates improved without regression (pattern: CTX-A). For a software team's engineer, with the guarantee that every recorded run is reproducible from its record and that the agent never edits the requirement, its own instructions, or the ticket's Done state.

**Deliverable shape** `[environment]`: one server on port 4000 serving both the pages and the API — the lab's preview pane is the only view of the running app. The course's own artefacts (notebooks and a demo web app on another port) are not the deliverable; this served app embodies the course's pattern, with the learning loop moved from a notebook into a page of the same app.

**Adapting this beyond the lab.** The dimensions the lab fixed live here: *project* and *goal* in this section; *data/inputs* in the §5 fixture corpus (swap the requirement documents for your own); *model/provider* in §2's role and key variables and R20 (point them at your provider; R21 states what any model must support); *environment* in §2 and the Runtime (lab) section (port, URL form, venv rule — change these first when leaving the lab). The scope boundary stays a Ledger row.

### Not Included            ★

Each item carries one handling tag that the L1 gate question uses: `restorable` (additive, owned by no Ledger row — can be brought back at the gate as an extra that changes no existing criterion; this spec supplies no parameters or criteria for it), `named-not-built` (the course names it but never builds it — buildable, but the agent must first say that this spec supplies no parameters and no acceptance criteria, so the design is its own invention), `owned-by-row` (decided on the named Ledger row, never here), `unavailable` (outside this build mode).

1. Real Jira / Confluence integration (REST calls, inbound webhooks, Atlassian credentials) — `unavailable` — outside this build mode: needs credentials the lab does not supply (an Atlassian site, account and API token) and this spec never asks for. The swap seam is pinned in §2 (System of record) so the standalone takeaway can restore it.
2. Hosted trace viewing (the course's optional LangSmith tracing, used in its primer; the app renders its own local trace table instead) — `unavailable` — outside this build mode: needs a LangSmith API key the lab does not supply and this spec never asks for (restorable in a standalone takeaway, through the tracing variables recorded in CTX-D).
3. Skills with progressive disclosure for the review agent (the course's primer uses them for a poet agent; the review agent has none) — `owned-by-row D2`.
4. Memory consolidation across runs (user preferences, the course's "second category" of harness improvement) — `named-not-built`.
5. Subagents / delegation, context summarization and a code sandbox (named as harness pillars, never used by the course's review agent) — `named-not-built`.
6. Human approval on individual tool calls — `named-not-built`.
7. A human acting as the grader — `unavailable` — outside this build mode: the lab's completion gate is an offline suite that cannot wait on a person (row D3's Trade-off names the seam: the grader box, whose verdict alone decides retry or stop).
8. Scheduled (cron) triggers; the course names them as a trigger kind and builds only event and manual triggers — `named-not-built`.
9. Token and cost estimates on the batch comparison (the course computes them with era-specific prices; the prices are perishable and recorded in CTX-D) — `restorable`.
10. The poet primer agent and its skill files — `restorable` (not part of the pattern).
11. Notebook-style plots (matplotlib charts); the Learning page shows tables instead — `restorable`.
12. User accounts and authentication — `restorable`.
13. Integration of the pattern into an existing codebase — `unavailable`.

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python 3 — the course requires ≥ 3.12 (its project file and README; its kernels ran 3.12.10) | `[environment]` The container's Python minor version is not stated. **First build step:** run `python3 --version`, record the output in `resolved-decisions.md`, and if any course-pinned package below refuses that interpreter, stop and report instead of substituting versions. |
| Virtual env | `python3 -m venv --system-site-packages .venv` | `[environment]` Reuses the preinstalled stack for unpinned packages. **Where a course pin below differs from a preinstalled copy, the course pin wins inside the venv** (`openai`, `python-dotenv` are preinstalled and may differ). Batch the whole install into one early command and announce its wall-clock cost before running it. |
| Agent harness | `deepagents==0.7.11` | **Honest pin situation:** the course's project file sets floors (`>=`), and its lock file resolves exact versions; this spec pins the lock's resolved versions. The course's own grader prompt restates the harness's default grader rules "as of deepagents 0.7.11", so this pin is load-bearing for R8. Era-specific class and argument names are search keywords in CTX-D, not guaranteed imports. |
| LangChain core + models | `langchain==1.3.18`, `langchain-core==1.6.1`, `langchain-openai==1.6.0`, `langgraph==1.2.11` | From the course lock file. The `openai:` model-string prefix resolves through `langchain-openai`. |
| OpenAI client | `openai==3.6.0` | Course lock pin; overrides the preinstalled copy inside the venv. |
| Pydantic | `pydantic==2.13.5` | Course lock pin; the analyst's structured response (`HarnessChange`, §3) is a Pydantic model. |
| dotenv | `python-dotenv==1.2.3` | Course lock pin; loads a local `.env` for live use **only if present** — the lab exports the variables directly (R20). |
| Web framework | `flask>=3.1.3` (latest release at build time) | The course listed Flask with a floor only and its lock file holds no Flask entry, so this is a modern-version choice, not a course pin. Bound to `0.0.0.0:4000` `[environment]` (R23). |
| Test runner | `pytest` (latest) | Project hardening: the course had no test suite; the §5 criteria need a runner. |
| Stores | JSON files under `data/` (standard library `json`) | Course default; tier (1), no server. |
| System of record | **In-app simulated Jira + Confluence** — the course's own stand-in: two page families and a ticket board in the app's own JSON files, keyless; the realization every event criterion in §5 runs against | Not a Ledger row in this build mode: its only alternative, real Atlassian Jira + Confluence through their REST APIs and a webhook, needs an Atlassian site, an account and an API token the lab does not supply, and this spec never asks for keys — so it is Not Included #1 (`unavailable`), not a choice. What must hold regardless of realization (the swap seam the course points at, CTX-C1): the requirement document lives in a system of record the review agent reads **by id through a fetch tool** and never edits (R1, R12); the review's output goes to a **separate, agent-owned, versioned** place (R12); a **human**, never the agent, closes the ticket (R13); the trigger seam (`run the loop for ticket K`) is one function a webhook could call (R11). |
| Acceptance-suite model | **The scripted stand-in** (`fixtures/scripted_model.py`, `MODEL_BACKEND=scripted`) — always | Not a Ledger row in this build mode: the completion gate is the offline suite, so it always runs on the stand-in (R22), which keeps every verdict in §5 deterministic and free and needs no key (CTX-C4). The course's live models (`gpt-5.4-mini` for review agent and grader, `gpt-5.5` for the analyst; course default) are how the finished app runs live (R21) and what the `live`-tagged criteria use. |
| Model backend switch | env `MODEL_BACKEND` ∈ {`scripted`, `live`}; default `scripted` | Acceptance-suite model row above. `scripted` loads `fixtures/scripted_model.py`; `live` builds platform models from the role variables below. |
| Model role variables | `REVIEW_MODEL`, `GRADER_MODEL`, `ANALYST_MODEL` — each a platform model id | `[environment]` One variable per model role the course's pipeline has (review agent, grader, analyst — course provenance: `gpt-5.4-mini`, `gpt-5.4-mini`, `gpt-5.5`). **The build agent sets these when it writes `resolved-decisions.md`** (gate step 5): the checklist carries one "model roles" line naming the "(Recommended)" platform model per role, and the person's confirmation of the checklist confirms them. No current model name is baked into this spec; the course's ids are provenance only and are not asserted to be served by the platform proxy. |
| Key variables | `OPENAI_API_KEY` + `OPENAI_BASE_URL` (read by the app — the course's provider is OpenAI); `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL` (present in the container, **never read**) | `[environment]` Read exactly these names; never hardcode a key, never ask the person for one, never probe a model-listing endpoint, never guess other variable names (R20). Secrets are never written to any file the app owns. |

## 3. Input/Output Contracts            ★

All API responses are JSON. Every page in the UI renders the same objects. Every URL in a served page is relative (`api/tickets`, `jira/REQ-100` — never `/api/...`) `[environment]`.

### 3.1 Ticket

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Ticket",
  "type": "object",
  "required": ["key", "title", "description", "linked_page_id", "assignee", "status", "comments", "created_at", "last_analyzed_version", "last_run_id"],
  "properties": {
    "key": {"type": "string", "pattern": "^REQ-[0-9]+$"},
    "title": {"type": "string", "minLength": 1},
    "description": {"type": "string"},
    "linked_page_id": {"type": "string", "pattern": "^page-[a-z0-9-]+$"},
    "assignee": {"type": "string", "enum": ["Avery (Product Manager)", "Blake (Eng Lead)", "Casey (QA Lead)", "Devin (Backend Engineer)", "Emery (Frontend Engineer)", "Unassigned"]},
    "status": {"type": "string", "enum": ["Open", "Analysis Ready", "Done"]},
    "comments": {"type": "array", "items": {"type": "object", "required": ["author", "text", "timestamp"], "properties": {"author": {"type": "string"}, "text": {"type": "string"}, "timestamp": {"type": "string"}}}},
    "created_at": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2} UTC$"},
    "last_analyzed_version": {"type": ["integer", "null"], "minimum": 1},
    "last_run_id": {"type": ["string", "null"]}
  },
  "if": {"properties": {"status": {"const": "Analysis Ready"}}},
  "then": {"properties": {"last_run_id": {"type": "string"}, "last_analyzed_version": {"type": "integer"}}}
}
```

### 3.2 Page (requirement page or analysis report)

```json
{
  "title": "Page",
  "type": "object",
  "required": ["id", "kind", "title", "linked_ticket", "versions"],
  "properties": {
    "id": {"type": "string", "pattern": "^page-[a-z0-9-]+$"},
    "kind": {"type": "string", "enum": ["requirement", "analysis_report"]},
    "title": {"type": "string", "minLength": 1},
    "linked_ticket": {"type": ["string", "null"]},
    "versions": {
      "type": "array",
      "items": {"type": "object", "required": ["n", "author", "timestamp", "body"], "properties": {"n": {"type": "integer", "minimum": 1}, "author": {"type": "string"}, "timestamp": {"type": "string"}, "body": {"type": "string"}}}
    }
  },
  "allOf": [
    {"if": {"properties": {"kind": {"const": "requirement"}}}, "then": {"properties": {"linked_ticket": {"type": "null"}, "versions": {"minItems": 1}}}},
    {"if": {"properties": {"kind": {"const": "analysis_report"}}}, "then": {"properties": {"linked_ticket": {"type": "string", "pattern": "^REQ-[0-9]+$"}, "id": {"pattern": "^page-analysis-req-[0-9]+$"}, "title": {"pattern": "^Analysis Report — REQ-[0-9]+$"}}}}
  ]
}
```

Version `n` is 1 for the first version and increments by exactly 1 per save. Every version of an `analysis_report` page has author `Requirements Review Agent (bot)` and a body that begins with the three banner lines of R12 followed by a blank line and the analysis file (or R12's no-file line). A requirement page's versions are only ever written by a person from the `assignee` cast (R15); a run never adds one (R12).

### 3.3 Run (one automation run)

```json
{
  "title": "Run",
  "type": "object",
  "required": ["id", "ticket_key", "requirement_page_id", "requirement_version", "report_page_id", "report_version", "status", "turns", "counts", "stage_order", "complete", "trace", "grading", "instructions", "rubric_iterations", "max_turns", "simulated_failures", "timestamp"],
  "properties": {
    "id": {"type": "string", "pattern": "^[0-9a-f]{8}$"},
    "ticket_key": {"type": "string"},
    "requirement_page_id": {"type": "string"},
    "requirement_version": {"type": "integer", "minimum": 1},
    "report_page_id": {"type": "string"},
    "report_version": {"type": "integer", "minimum": 1},
    "status": {"type": "string", "enum": ["satisfied", "max_iterations_reached", "failed", "grader_error", "ungraded"]},
    "turns": {"type": "integer", "minimum": 1},
    "counts": {"type": "object", "required": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions"], "additionalProperties": false,
               "properties": {"Confirmed Facts": {"type": "integer", "minimum": 0}, "Ambiguities": {"type": "integer", "minimum": 0}, "Clarification Questions": {"type": "integer", "minimum": 0}, "Assumptions": {"type": "integer", "minimum": 0}}},
    "stage_order": {"type": "array", "items": {"type": "string", "enum": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"]}},
    "complete": {"type": "boolean"},
    "trace": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/TraceStep"}},
    "grading": {"type": "array", "items": {"$ref": "#/$defs/GradingPass"}},
    "instructions": {"type": "string", "minLength": 1},
    "rubric_iterations": {"type": "integer", "minimum": 0},
    "max_turns": {"type": "integer", "minimum": 1},
    "simulated_failures": {"type": "integer", "minimum": 0},
    "timestamp": {"type": "string"}
  },
  "allOf": [
    {"if": {"properties": {"grading": {"maxItems": 0}}}, "then": {"properties": {"status": {"const": "ungraded"}}}},
    {"if": {"properties": {"grading": {"minItems": 1}}}, "then": {"properties": {"status": {"enum": ["satisfied", "max_iterations_reached", "failed", "grader_error"]}}}}
  ],
  "$defs": {
    "TraceStep": {
      "type": "object", "required": ["step", "actor", "action", "detail"],
      "properties": {
        "step": {"type": "integer", "minimum": 1},
        "actor": {"type": "string", "enum": ["Model reasoning", "Tool"]},
        "action": {"type": "string", "minLength": 1},
        "detail": {"type": "string", "maxLength": 221}
      }
    },
    "GradingPass": {
      "type": "object", "required": ["iteration", "result", "explanation", "criteria", "analysis_markdown"],
      "properties": {
        "iteration": {"type": "integer", "minimum": 1},
        "result": {"type": "string", "enum": ["satisfied", "needs_revision", "failed", "grader_error"]},
        "explanation": {"type": "string"},
        "criteria": {"type": "array", "items": {"type": "object", "required": ["name", "passed"], "properties": {"name": {"type": "string"}, "passed": {"type": "boolean"}, "gap": {"type": "string"}}}},
        "analysis_markdown": {"type": "string"}
      },
      "allOf": [
        {"if": {"properties": {"result": {"const": "satisfied"}}}, "then": {"properties": {"criteria": {"minItems": 3, "maxItems": 3, "items": {"properties": {"passed": {"const": true}}}}}}},
        {"if": {"properties": {"result": {"const": "needs_revision"}}}, "then": {"properties": {"criteria": {"minItems": 3, "maxItems": 3, "contains": {"properties": {"passed": {"const": false}}, "required": ["gap"]}}}}},
        {"if": {"properties": {"result": {"enum": ["failed", "grader_error"]}}}, "then": {"properties": {"criteria": {"maxItems": 0}}}}
      ]
    }
  }
}
```

`stage_order` lists the sections in the order the agent's successful write/edit calls first filled them, before any grader feedback; `complete` is R3's completeness test on the final file; `turns` counts model turns (tool-calling turns and closing messages; the cap row of R5 is not a turn). Run status derivation (R9): `ungraded` when no grading pass was recorded (no grader attached, or the cap ended the run before the grader ran); `satisfied` when the last grading pass is `satisfied`; `max_iterations_reached` when the last pass is `needs_revision` and the revision budget is exhausted; otherwise the last pass's result (`failed` or `grader_error`).

### 3.4 Analysis file (`/analysis.md` in the agent's workspace)

Markdown with this exact grammar — heading line `# Requirements Analysis`, then the five `##` sections **in this order**: `Confirmed Facts`, `Ambiguities`, `Clarification Questions`, `Assumptions`, `Summary`. The four list sections hold `- ` bullets; `Summary` holds prose. Each Ambiguities bullet matches, line by line:

```
- **"<exact clause quoted from the requirement>"**
  Reason: <why it is under-specified>
  Resolved by: <the specific fact or decision that would settle it>      ← required by the rubric's clarity criterion
  Edge case: <a concrete production failure if it stays unresolved>      ← required by the rubric's depth criterion
```

Regex per line, in order: `^- \*\*".+"\*\*$`, `^  Reason: .+$`, `^  Resolved by: .+$`, `^  Edge case: .+$`. The two labelled lines are what the baseline instructions never ask for and the learning loop adds (R4). A file is **complete** when each list section has ≥ 1 bullet and Summary has ≥ 1 word (R3).

### 3.5 BatchSummary (`data/run_history/<label>/summary.json`)

```json
{
  "title": "BatchSummary",
  "type": "object",
  "required": ["label", "model", "runs", "graded", "grader_errors", "first_attempt", "revisions_needed", "attempts", "documents"],
  "properties": {
    "label": {"type": "string", "pattern": "^[A-Za-z0-9_-]+$"},
    "model": {"type": "string"},
    "runs": {"type": "integer", "minimum": 1},
    "graded": {"type": "integer", "minimum": 0},
    "grader_errors": {"type": "integer", "minimum": 0},
    "first_attempt": {"type": "object", "required": ["completeness", "clarity", "depth"], "additionalProperties": false,
      "properties": {
        "completeness": {"$ref": "#/$defs/Rate"}, "clarity": {"$ref": "#/$defs/Rate"}, "depth": {"$ref": "#/$defs/Rate"}}},
    "revisions_needed": {"type": "integer", "minimum": 0},
    "attempts": {"type": "integer", "minimum": 0},
    "documents": {"type": "array", "items": {"type": "string"}}
  },
  "$defs": {"Rate": {"type": "object", "required": ["passed", "total", "pass_rate"], "properties": {"passed": {"type": "integer", "minimum": 0}, "total": {"type": "integer", "minimum": 0}, "pass_rate": {"type": ["number", "null"], "minimum": 0, "maximum": 1}}}}
}
```

Invariants (R16): `runs = graded + grader_errors`; every `total = graded`; `revisions_needed ≤ graded`; `attempts` = total grading passes across all runs; `pass_rate = passed / total` rounded to 3 decimals, `null` when `total = 0`.

### 3.6 HarnessChange (the analyst's structured response; also the `change` member of the apply endpoint's body)

```json
{
  "title": "HarnessChange",
  "type": "object",
  "required": ["target", "issue", "recurrence", "evidence", "section", "change", "rejected"],
  "properties": {
    "target": {"type": "string", "enum": ["prompt", "tool", "grader", "configuration"]},
    "issue": {"type": "string", "minLength": 1},
    "recurrence": {"type": "string", "minLength": 1},
    "evidence": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}},
    "section": {"type": "string"},
    "change": {"type": "string", "minLength": 1},
    "rejected": {"type": "array", "items": {"type": "string"}}
  },
  "if": {"properties": {"target": {"const": "prompt"}}},
  "then": {"properties": {"section": {"pattern": "^#{1,6} .+$"}}}
}
```

### 3.7 Comparison (`GET api/compare?before=<label>&after=<label>`)

```json
{
  "title": "Comparison",
  "type": "object",
  "required": ["verdict", "criteria", "runs", "revisions_needed", "attempts", "improved", "regressed"],
  "properties": {
    "verdict": {"type": "string", "enum": ["success", "partial", "no effect", "regression"]},
    "criteria": {"type": "object", "required": ["completeness", "clarity", "depth"],
      "additionalProperties": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "integer", "minimum": 0}}},
    "runs": {"type": "integer", "minimum": 1},
    "revisions_needed": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "integer", "minimum": 0}},
    "attempts": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "integer", "minimum": 0}},
    "improved": {"type": "array", "items": {"type": "string", "enum": ["completeness", "clarity", "depth"]}},
    "regressed": {"type": "array", "items": {"type": "string", "enum": ["completeness", "clarity", "depth"]}}
  },
  "allOf": [
    {"if": {"properties": {"regressed": {"minItems": 1}}}, "then": {"properties": {"verdict": {"const": "regression"}}}},
    {"if": {"properties": {"regressed": {"maxItems": 0}, "revisions_needed": {"items": false, "prefixItems": [{}, {"const": 0}]}}}, "then": {"properties": {"verdict": {"const": "success"}}}}
  ]
}
```

`attempts` is each summary's `attempts` value (before, after); `runs` is the before summary's `runs`, and the endpoint returns 400 when the two summaries' `runs` differ.

### 3.8 Endpoints

| Method and path | Body / query | Returns |
|---|---|---|
| `GET api/health` | — | `{"model_backend": "scripted"\|"live", "roles": {"review": str, "grader": str, "analyst": str}, "port": 4000}` — each role is the platform model id in live mode and the literal `ScriptedModel` in scripted mode |
| `GET api/tickets`, `GET api/tickets/<key>` | — | Ticket[] / `{"ticket": Ticket, "runs": Run[] (oldest first), "report_page_id": str\|null}` |
| `POST api/tickets` | `{"title", "description", "linked_page_id", "assignee"}` | 201, `{"ticket": Ticket, "run_id": str}` after the triggered run completes (R11) |
| `POST api/tickets/<key>/rerun` | optional `{"rubric_iterations": int, "max_turns": int, "simulated_failures": int}` — defaults: `rubric_iterations` 3; `max_turns` 40 when `rubric_iterations` > 0, 12 when it is 0; `simulated_failures` 0 (R9, R5, R2) | `{"run_id": str}` after the run completes |
| `POST api/tickets/<key>/close` | — | Ticket with status `Done` (R13) |
| `GET api/runs/<id>` | — | Run |
| `GET api/pages`, `GET api/pages/<id>` | optional `?v=<n>` | Page[] / Page (+ `"body"` of the requested or latest version) |
| `POST api/pages` | `{"title", "body", "author"}` | 201, Page (kind `requirement`) |
| `POST api/pages/<id>/versions` | `{"body", "author"}` | `{"page": Page, "retriggered": [ticket keys]}` after any re-runs complete (R11) |
| `GET api/pages/<id>/compare?a=<n>&b=<n>` | — | `{"diff": [unified-diff lines], "run_a": Run\|null, "run_b": Run\|null}` (R14) |
| `GET api/instructions` | — | `{"text": str}` — the app's current instructions |
| `POST api/instructions/apply` | `{"change": HarnessChange, "approved": true}` | `{"text": str}` after insertion; 400 unless `approved` is `true`, unless `target` is `prompt`, or unless `section` exists (R18) |
| `POST api/instructions/reset` | — | `{"text": str}` — restores the fixture baseline (test hook, project hardening) |
| `POST api/batches` | `{"label": str, "docs": [paths] (optional; default every `fixtures/requirement_docs/*.md`)}` | 201, BatchSummary after every run completes (R16) |
| `GET api/batches/<label>` | — | `{"summary": BatchSummary, "runs": [batch run records]}` |
| `POST api/proposals` | `{"label": str}` | 201, `{"label", "change": HarnessChange, "proposal_markdown": str, "trace": TraceStep[]}` — `trace` is the analyst's own run, one row per model turn and tool result in §3.3's TraceStep form (R17) |
| `GET api/proposals/<label>` | — | `{"label", "change", "proposal_markdown"}`, read from `data/run_history/proposal_<label>.json` and `.md` |
| `POST api/reset` | — | Test hook (project hardening): deletes everything under `data/` and re-seeds per R25; this is what "Fresh init" in §5 means |
| `GET api/compare?before=&after=` | — | Comparison (R19) |
| Pages | `GET /`, `jira`, `jira/<key>`, `jira/<key>/runs/<run_id>`, `confluence`, `confluence/<page_id>`, `confluence/<page_id>/compare?a=&b=`, `learning` | HTML renderings of the objects above |

Every error response is JSON `{"error": <message>}` with status 400 (bad input, refused apply, mismatched batches), 404 (unknown key, page, run, label) or 500 (a run that could not start or a missing environment variable). A batch run record is a Run without the ticket/page fields, plus `run_id` (1-based position), `doc_name` (file stem), `label`, `model`, `requirement_doc`, `messages` (every message of the conversation, untruncated, with full tool-call arguments) and `started_at`; it is written to `data/run_history/<label>/run_<NN>_<doc_name>.json`.

## 4. Business Rules

Each rule states the behaviour, the failure it prevents, its provenance label, and the criteria that cite it.

**R1. Fetch by id, never by hand.** The review agent is never handed the requirement text. Its opening message names only an id (`The requirement document is tracked as ticket <id>. Fetch it to begin.`) — the ticket key for a triggered run, `BATCH-<NN>` (the run's two-digit position) for a batch run — and before each run the app registers the document's **current** text under that id in the fetch store; the agent's `fetch_requirement(ticket_id)` tool resolves it there. An unknown key returns an error result, not an exception. Prevents the agent reasoning from a stale or pasted copy, and a run dying on the first fetch error (CTX-A, CTX-B1). *Course-demonstrated.* → AC5, AC6

**R2. Transient tool failure → retry the same call.** A tool result that begins with the word `Error` is an error result; the agent retries the exact same tool with the same arguments. The fetch tool supports deterministic fault injection: `simulated_failures = n` makes its first `n` calls in a run return, in rotation, `Error: requirement service returned 503 Service Unavailable, please retry.` and `Error: requirement service timed out after 10s, please retry.`; this is a fault-injection switch, not a tunable of the pattern: the acceptance fixture injects 2, the value the Lesson 4 narration states for its retry demonstration, and the app's default is 0, the value every course end-to-end path ran with (CTX-C6 records the contradiction). Prevents a run dying on an unreachable external system (CTX-B1). *Course-demonstrated.* → AC6

**R3. One report file, five sections, staged.** The review's deliverable is `/analysis.md` in the agent's workspace, with the §3.4 grammar. The instructions ask the agent to work in stages, one tool call per turn: one `write_file` laying down the skeleton with only Confirmed Facts filled, then one `edit_file` per remaining section in order. Stage order is **requested, not enforced**: the run record reports the order actually followed and whether the file is complete (every list section ≥ 1 bullet, Summary ≥ 1 word). Prevents an unparseable or half-written review (CTX-B2). *Course-demonstrated.* → AC5, AC7, AC43

**R4. Ambiguity bullets carry a quoted clause, a reason, and — once instructed — the two labelled lines.** The baseline instructions ask only for the quoted clause and an indented `Reason:` line; the rubric additionally requires indented `Resolved by:` and `Edge case:` lines on **every** Ambiguities bullet, and the learning loop's whole demonstration is that the baseline never asks for them. Labels are literal: a different label is a different line. Prevents reviews that name a vagueness without saying what would settle it or what it breaks (CTX-B3). *Course-demonstrated.* → AC7, AC9, AC34

**R5. A model-call cap ends a run that stops making progress.** Each run is capped at `max_turns` model calls: **12** for a plain review (`rubric_iterations` 0 — the course's single-review cap: six stages plus headroom for retries and the closing message) and **40** for a review with a grader (several grading passes cost more turns). When the cap ends a run whose file is incomplete, the trace's last row is a `Model reasoning` row whose action is `Stops: turn limit of <n> reached` (the app appends it if the harness produced no closing message) rather than `Finishes the review`. The cap is not the normal stop — the normal stop is the agent's own closing message — it exists for the case where the agent keeps retrying past the point where retrying makes sense. Prevents an unbounded, unbilled loop (CTX-B4). *Course-demonstrated.* → AC8

**R6. The instructions file is loaded every run, must exist, and is read-only to the agent.** The app keeps its current instructions at `data/instructions/AGENTS.md`; before each run they are copied to `memories/AGENTS.md` inside that run's workspace and loaded into the agent's context at start. If the baseline file is missing, or the copy is missing from a workspace, the run fails loudly with an error naming the missing path — a silently missing file would make the agent "run on the system prompt alone and produce a plausible bad review". Writes under `/memories/` are **denied by the harness's permission layer**, not merely discouraged: the agent has `edit_file` and the file sits in its filesystem. The agent never modifies the requirement document (it is not in the agent's filesystem at all). Prevents a review produced without guidance, and self-edited instructions (CTX-B5). *Course-demonstrated.* → AC10, AC11

**R7. One fresh, confined workspace per run.** Each run gets its own directory under `data/workspaces/`, seeded with `memories/AGENTS.md`, exposed to the agent as `/` with paths above it unreachable; no `/analysis.md` exists at start, and the directory is removed when the run is recorded. Prevents a leftover analysis from an earlier run letting the agent skip stages, and two tickets analysed back to back seeing each other's files (CTX-B6). *Course-demonstrated.* → AC11, AC12

**R8. The grader judges the file, literally, and quotes it.** The grader is a second model call with its own instructions and a `read_file` tool; it must read `/analysis.md` before judging and judge only what that file contains — never the conversation, which "can make a criterion look satisfied just from how the conversation reads". It passes a criterion only if it can quote the satisfying text with its line number; it applies each criterion literally (a line with a different label is a different line; coverage criteria check every item, not a sample); it is conservative (anything it cannot confirm fails, with a `gap` describing the missing evidence); its allowed results are `satisfied`, `needs_revision` (every failing criterion carries an actionable `gap`) and `failed` (the rubric is malformed or impossible to evaluate). Prevents a grader that passes "by resemblance" (CTX-B7). *Course-demonstrated.* → AC9, AC13, AC44

**R9. The verification loop: three criteria, all in one pass, bounded retries.** The rubric has exactly three pass/fail criteria, in this order: **completeness** (every clause of the requirement is addressed somewhere in the analysis), **clarity** (every Ambiguities bullet has an indented `Resolved by:` line), **depth** (every Ambiguities bullet has an indented `Edge case:` line). The run stops when all three pass **in the same pass**; otherwise the grader's feedback is injected into the conversation and the agent revises, up to `rubric_iterations` send-backs — **default 3** (post-build lever: the Lesson 5 narration states 3, as do the notebook and the batch runner; the course's event-driven app ran 2 — a near-equivalent contradiction resolved by lever-value branch (1), the narrated value; CTX-C6). The rubric reaches the grader only (it is passed in invocation state), never the review agent's instructions or context. Setting it to 0 yields the plain agent loop with no grader. A `grader_error` (the grader call raised) or `failed` pass carries no criteria and ends grading; run status follows §3.3's derivation. Prevents "finished" being mistaken for "good enough", and endless revision (CTX-B3, CTX-B4). *Course-demonstrated; the `failed`/`grader_error` run-status derivation is project hardening.* → AC8, AC9, AC13, AC14, AC15, AC16, AC43

**R10. Every run that starts is recorded, in full, as a file.** (A run refused before its workspace is seeded — R6's missing-file case — is not a run and leaves no record.) The run record (§3.3) holds the trace — one row per model turn and one per tool result, so every tool-result row directly follows the model row that called it. A model row has actor `Model reasoning` and action `Calls <tool>` (`Calls <tool>: <sections>` when a `write_file`/`edit_file` call fills sections), with detail = the call's `file_path` argument (empty when none); the closing message's row has action `Finishes the review` and detail = the message text; the cap row is R5's. A tool-result row has actor `Tool`, action = the tool's name (plus `: <sections>` for a section-filling write/edit) and detail = the result text. Every detail is truncated to 220 characters plus `…`. The trace holds the review agent's turns only: the grader's turns (its `read_file` call and its verdict) are not trace rows — each grading pass is recorded in `grading` instead. The record also holds every grading pass with the file exactly as the grader saw it, the instructions snapshot, the section counts and the status. Records are appended to `data/analysis_runs.json` and survive a process restart. Prevents the "story in the traces" being lost: for agents, the truth is in the trace, not the code (CTX-C9). *Course-demonstrated.* → AC5, AC9, AC14, AC17, AC18

**R11. Events trigger the loop; the request waits for it.** Three triggers run the review+grader loop for a ticket: the ticket is **created**; a requirement page is **saved** while one or more **open** (not `Done`) tickets link to it — one run per such ticket; a person presses **re-run**. Saving a page with no open linked ticket runs nothing. All three triggers call one function — `run the loop for ticket K` — the trigger seam a real webhook would call; no trigger runs the loop by another path. Runs are synchronous: the HTTP request returns once the run is recorded. Prevents the agent waiting for someone to start it (CTX-A). *Course-demonstrated.* → AC19, AC20, AC21

**R12. The report goes to a separate agent-owned page; the ticket is updated, never closed.** Each run writes its analysis as a **new version** of the page `Analysis Report — <key>` (id `page-analysis-<key lowercased>`, kind `analysis_report`, created on first use, author `Requirements Review Agent (bot)`), whose body starts with three banner lines — `> Generated automatically from <key> on <timestamp>.`, `> Source requirement: version <n>.`, `> Verification status: **<status>** after <k> grading pass(es).` — then a blank line and the analysis file — or, when the run ended with no `/analysis.md` written (a capped run, R5), the single line `_No analysis file was written._` in its place. The requirement page is never written by a run. The ticket's status becomes `Analysis Ready` unless it is `Done` (a person may still re-run a Done ticket; its status stays `Done`), `last_analyzed_version` and `last_run_id` are set, and a bot comment `Analysis complete (<status>), requirement version <n>. See Analysis Report — <key> in Confluence.` is added. Prevents the agent editing the source of truth and hiding the history of past analyses (CTX-B8). *Course-demonstrated; the no-file line is project hardening.* → AC8, AC19, AC20, AC22

**R13. A human marks Done.** Only the close endpoint moves a ticket to `Done`; no run ever sets `Done`; a `Done` ticket is never re-triggered by a page save. Prevents the agent closing its own work (CTX-B8). *Course-demonstrated.* → AC21, AC23

**R14. Show what changed as counts *and* as a diff.** When a ticket has two or more runs, its page shows a "What changed since the previous run" table — requirement version analysed, verification status, and the bullet count of each of the four list sections, previous vs latest — with a link to the report page's version compare. The compare view for any page returns the unified diff between two versions (`--- version <a>` / `+++ version <b>` headers), and for a report page also the two runs behind those versions. Prevents the false impression that similar bullet counts mean nothing changed: "the content changed completely even though the shape didn't" (CTX-C7). *Course-demonstrated.* → AC20, AC24

**R15. People are picked from a fixed cast.** Ticket assignees and page authors are chosen from the five-name cast in §3.1 (plus `Unassigned` for tickets); any other value is rejected with 400. Prevents free-text identities; the course notes real trackers pull names from a directory (CTX-C1). *Course-demonstrated.* → AC25

**R16. A batch is every document once, under one instructions version, summarised by first-attempt verdict.** `POST api/batches` reviews each document in the given list (default: every file in `fixtures/requirement_docs/`, sorted) with the review+grader loop (`rubric_iterations` 3, `max_turns` 40, no fault injection), each in its own workspace, all under a **snapshot** of the current instructions copied to `data/run_history/<label>/AGENTS.md`; each run is written as `run_<NN>_<doc_name>.json` with every message untruncated. `summary.json` reports, per criterion, how many **graded** runs passed it on the **first** grading pass; a run is graded only if its first pass carries criteria (a `grader_error` or `failed` first pass carries none and is excluded from every denominator, counted in `grader_errors`); criteria are matched **by position in the rubric**, never by the name the grader echoes back; `revisions_needed` counts graded runs whose first pass failed anything; `attempts` totals grading passes. Prevents the two things that hide a systemic failure: averaging ungraded runs in, and splitting one recurring criterion across the grader's paraphrases (CTX-B9). *Course-demonstrated.* → AC26, AC27, AC28, AC34

**R17. The analyst reads everything and writes only its proposal.** `POST api/proposals` runs an analyst agent rooted at `data/run_history/` with `ls`, `read_file`, `glob`, `grep` and `write_file`, where every write except `/proposal.md` is denied by the permission layer. Its instructions: start with `/<label>/summary.json`, then read the runs for evidence, then `/<label>/AGENTS.md` so the addition fits and repeats nothing; a criterion failing in most runs is a property of the agent, a problem in one run of five is **not a pattern** and goes under `rejected`; quote evidence, never paraphrase; `change` is the literal text to insert, with exact labels if a labelled line is required. The structured response is a HarnessChange (§3.6); the proposal markdown and the change are persisted as `data/run_history/proposal_<label>.md` and `proposal_<label>.json`. Prevents an analyst that edits the evidence it reasons from, and one-off noise becoming instruction churn (CTX-B10). *Course-demonstrated.* → AC29, AC30, AC41

**R18. A change is applied by a person's approval and by plain code — prompt changes only.** The apply endpoint refuses without `"approved": true` (the human-in-the-loop step), refuses any `target` other than `prompt` ("read the proposal and decide" — never half-applied), and errors when `section` is not a heading line in the current instructions. On success it inserts `change` at the **end of the named section** (before the next heading of equal or shallower depth, after trailing blank lines are trimmed, separated by one blank line) and the new text becomes the app's current instructions. Deciding where the text lands is never a model call. Prevents unreviewed harness mutation and non-deterministic edits (CTX-B11). *Course-demonstrated.* → AC31, AC32, AC33

**R19. A change is judged by re-running the batch and comparing first-attempt verdicts.** `GET api/compare` reads two summaries and returns per-criterion first-attempt passes (before, after), lists criteria that `improved` (after > before) and `regressed` (after < before), rejects (400) two batches of different size, and gives a verdict: `regression` if anything regressed; else `success` if the after batch needed 0 revisions; else `partial` if anything improved; else `no effect`. Prevents merging a harness change on faith: "it's pretty hard to have confidence merging changes to your core harness if you don't have good evals" (CTX-B11). *Course-demonstrated; the size check is project hardening.* → AC27, AC35, AC36, AC37

**R20. Keys and models come from the environment, never from the person.** `[environment]` With `MODEL_BACKEND=live` the app reads exactly `OPENAI_API_KEY` and `OPENAI_BASE_URL` (the course's provider) and the three role variables of §2; a missing variable produces a clear error naming it; the app never prompts for a key, never writes one to a file, never reads `ANTHROPIC_API_KEY` or `ANTHROPIC_BASE_URL` (present in the container, unread), and never probes a model-listing endpoint. With `MODEL_BACKEND=scripted` (the default) no key is read at all. Prevents a key request the lab has already answered, and a leaked secret. *Environment-imposed.* → AC38, AC39, AC42

**R21. Every model in a role must support native tool calling and structured output.** The agent loop is a tool-call loop (fetch and file tools), the grader needs `read_file`, and the analyst returns a typed `HarnessChange`; a model that cannot do both cannot fill any role. Prevents a model that narrates tool use instead of calling tools (CTX-A). *Course-demonstrated; `live` only.* → AC40, AC41

**R22. The acceptance suite runs the real pipeline on a scripted stand-in.** With `MODEL_BACKEND=scripted` the app builds the same agents, middleware, tools, permissions, stores and pages as in live mode and substitutes only the chat-model object with `fixtures/scripted_model.py` — a fake honestly named `ScriptedModel` whose per-role scripts §5 declares; nothing else is mocked. Prevents a test suite that tests the mocks (CTX-C4). *Project hardening (the stand-in); the roles it scripts are the course's.* → AC42, AC5

**R23. One server, relative URLs, HTTP only.** `[environment]` The app is one process bound to `0.0.0.0:4000` serving pages and API; every `href`, `src` and form `action` in served HTML is relative (no leading `/`, no scheme or host) because the preview is reverse-proxied under a path prefix and a root-absolute path resolves against the IDE; no WebSocket is used (streaming HTTP responses are fine). Prevents a working app that looks broken in the preview (Runtime (lab), E1). *Environment-imposed.* → AC2, AC3

**R24. The agent's instructions file lives inside app-owned folders, never at the workspace root.** The baseline is `data/instructions/AGENTS.md` and each run's copy is `<run workspace>/memories/AGENTS.md`; the app never creates, reads or edits a file named `AGENTS.md` at the build-folder root. Both sources require the file to sit inside an app-owned folder rather than at the project root: the course seeds each run's own workspace with it and keeps its one tracked copy under a workspace directory (never beside the code), and the environment forbids the workspace-root location because the IDE rewrites the workspace-root `AGENTS.md` at every boot, so anything placed there is silently lost (CTX-B5; Runtime (lab), E2). *Course-demonstrated, reinforced `[environment]`.* → AC4

**R25. Fresh initialization creates the declared structures and the seed scenario.** On first start with an empty `data/`, the app creates `data/pages.json` holding one requirement page (`page-session-timeout-requirements`, title `Session Timeout — Requirements`, one version by `Avery (Product Manager)` whose body is fixture `fixtures/seed/req_06_session_timeout.md`), `data/tickets.json` holding one ticket `REQ-100` (`Review requirements: Session Timeout`, assignee `Blake (Eng Lead)`, status `Open`, linked to that page, no comments, no runs), `data/analysis_runs.json` as `[]`, `data/instructions/AGENTS.md` byte-identical to `fixtures/instructions/AGENTS.md`, and the empty directories `data/run_history/` and `data/workspaces/`. New ticket keys are `REQ-<n>` with `n` = highest existing + 1. `POST api/reset` (§3.8) reproduces this state on demand for the suite. Prevents downstream failures that only surface as confusing retrieval errors. *Project hardening (existence check); the seed shape — one vague page, one open ticket — is the course's.* → AC1

## 5. Acceptance Criteria                ★  (the oracle)

### 5.1 Fixture corpus (all synthetic; authored for this spec; none copied from the course)

All fixtures live under `fixtures/` in the build folder. The building agent MUST NOT modify a fixture to make a criterion pass.

**Requirement documents** — `fixtures/requirement_docs/` (the batch corpus; stems are the `doc_name`s). Each is `REQUIREMENT: <title>` then one sentence per paragraph. Sentences containing a word from `VAGUE_WORDS` (below) are the ones the scripted review flags.

- `req_01_password_reset.md` — title `Password Reset`; sentences: `Users shall be able to reset a forgotten password from the login page.` / `Reset links should expire after a short time.` / `The reset process must be secure.` / `Users should be notified promptly when their password changes.` → 4 facts, 3 ambiguities (short, secure, promptly).
- `req_02_data_export.md` — `Account Data Export`; `Users shall be able to request an export of their account data.` / `Exports should be delivered in a reasonable time.` / `The export must include all relevant records.` / `Large exports should be handled efficiently.` → 4 facts, 3 ambiguities (reasonable, relevant, efficiently).
- `req_03_search_results.md` — `Catalog Search`; `The system shall return search results for a text query.` / `Results must appear quickly.` / `Misspelled queries should be handled gracefully.` / `The most relevant items should appear first.` → 4 facts, 3 ambiguities (quickly, gracefully, relevant).
- `req_04_audit_retention.md` — `Audit Log Retention`; `The system shall record every administrative action.` / `Records must be kept for an appropriate period.` / `Old records should be archived securely.` / `Auditors must be able to search the log easily.` → 4 facts, 3 ambiguities (appropriate, securely, easily).
- `req_05_rate_limiting.md` — `API Rate Limiting`; `The API shall limit how many requests a client may make.` / `Limits should be generous for normal use.` / `Clients exceeding the limit must receive a clear error.` / `Limits should reset after a short window.` → 4 facts, 3 ambiguities (generous, clear, short).
**Seed document** — `fixtures/seed/req_06_session_timeout.md` (the seed page's body; deliberately outside `requirement_docs/` so the default batch has exactly five documents):

- `req_06_session_timeout.md` — first line `REQUIREMENT: Session Timeout`, then one sentence per paragraph: `Users shall be logged out after a period of inactivity.` / `The timeout should be reasonable.` / `Users must be warned before being logged out.` / `Active work should not be lost.` → 4 facts, 1 ambiguity (reasonable).

**Marker documents** — `fixtures/marker_docs/` (each used by one criterion; created as requirement pages through the API, never in the batch default):

- `loop_forever.md` — `REQUIREMENT: Marker loop-forever` / `The system shall respond quickly. [[loop-forever]]`
- `never_satisfied.md` — `REQUIREMENT: Marker never-satisfied` / `The system shall respond quickly. [[never-satisfied]]`
- `grader_error.md` — `REQUIREMENT: Marker grader-error` / `The system shall respond quickly. [[grader-error]]`
- `rubric_unevaluable.md` — `REQUIREMENT: Marker rubric-unevaluable` / `The system shall respond quickly. [[rubric-unevaluable]]`
- `probe_permissions.md` — `REQUIREMENT: Marker probe-permissions` / `The system shall respond quickly. [[probe-permissions]]`
- `skip_stage.md` — `REQUIREMENT: Marker skip-stage` / `The system shall respond quickly. [[skip-stage]]`
- `claim_success.md` — `REQUIREMENT: Marker claim-success` / `The system shall respond quickly. [[claim-success]]`

**Constants** (declared in `fixtures/constants.py`): `VAGUE_WORDS = ["short", "secure", "securely", "promptly", "reasonable", "relevant", "efficiently", "quickly", "gracefully", "appropriate", "easily", "generous", "clear"]`; `PEOPLE` = the five cast names in §3.1.

**Fault injection (test hook)** — the `simulated_failures` field of `POST api/tickets/<key>/rerun` (§3.8), implemented by the fetch tool per R2; AC6 sets it to 2 and nothing else in the suite sets it.

**Rubric** — `fixtures/rubric.md`, exactly three `- <name>: <criterion>` lines in the order completeness, clarity, depth, with the criterion texts of R9.

**Baseline instructions** — `fixtures/instructions/AGENTS.md` (copied to `data/instructions/AGENTS.md` on fresh init). Exact content:

```
# Requirements Review Agent

You turn a raw requirement document into a structured review report held in one
file, `/analysis.md`.

## Procedure

Work through these stages in order, one tool call per turn. Do not skip a stage
and do not combine two stages into one call.

1. Call `fetch_requirement` with the ticket id you were given.
2. Call `write_file` to create `/analysis.md` with this skeleton, filling in only
   the Confirmed Facts section: a `# Requirements Analysis` heading, then the
   sections `## Confirmed Facts`, `## Ambiguities`, `## Clarification Questions`,
   `## Assumptions`, `## Summary`, in that order, each list section as `- ` bullets.
3. Call `edit_file` to fill in Ambiguities. One bullet per vague clause, shaped as
   a bold quoted clause on the first line and an indented `Reason:` line under it.
4. Call `edit_file` to fill in Clarification Questions. One bullet each.
5. Call `edit_file` to fill in Assumptions. One bullet each.
6. Call `edit_file` to fill in Summary with two or three sentences.

If a tool call returns an error message instead of a result, call the exact same
tool again with the same arguments; transient failures are expected.

You never modify the requirement document, and you never edit this file.

Once the Summary is written, reply with one short sentence and call no more tools.

## Review guidance

### Confirmed facts

Record only what the document states directly. Do not infer.

### Ambiguities

Quote the exact clause, then give the reason it is under-specified.

### Clarification questions

Ask what a reviewer would need answered before work could start.

### Assumptions

State what a developer would assume if nobody answered the questions.
```

Note what it does **not** say: nothing about `Resolved by:` or `Edge case:`. That omission is the planted failure the learning loop finds.

**Changes** — `fixtures/changes/`:

- `change_v1.json` — the HarnessChange the scripted analyst returns: `target` `prompt`; `issue` `The agent writes Ambiguities bullets with only a Reason line, so every first attempt lacks the Resolved by and Edge case lines the rubric requires.`; `recurrence` `5/5 runs failed clarity and depth on the first attempt.`; `evidence` = five strings, one per batch run, each the grader's own first-pass clarity gap quoted verbatim: `3 of 3 Ambiguities bullets lack an indented 'Resolved by:' line` (identical for all five runs, since every batch document has three ambiguities); `section` `### Ambiguities`; `change` = the two lines `For every ambiguity bullet, add two indented labelled lines after the Reason line:` and `  Resolved by: the specific fact or decision that would settle it, and Edge case: a concrete production failure if it stays unresolved.`; `rejected` = one string `run_03 wrote a three-sentence Summary where the others wrote two; one occurrence in five is not a pattern.`
- `change_partial.json` — identical to `change_v1.json` except `change` = `For every ambiguity bullet, add an indented labelled line after the Reason line: Resolved by: the specific fact or decision that would settle it.` (mentions `Resolved by:` only).
- `change_tool_target.json` — identical to `change_v1.json` except `target` `tool` and `section` `""`.
- `change_grader_target.json` — identical to `change_v1.json` except `target` `grader` and `section` `""`.
- `change_configuration_target.json` — identical to `change_v1.json` except `target` `configuration` and `section` `""`.
- `change_missing_section.json` — identical to `change_v1.json` except `section` `### Nonexistent`.

**Scripted stand-in model** — `fixtures/scripted_model.py`, class `ScriptedModel`, a fake chat model accepted wherever the harness takes a model (including the grader's structured `GraderResponse` and the analyst's structured `HarnessChange`). It chooses a script by the role it is constructed for (the app constructs one per role). Scripts, exactly:

*Review script* (one tool call per turn, reading only the conversation it is given):
1. If the conversation holds no `fetch_requirement` result yet, call `fetch_requirement(ticket_id=<the key named in the opening message>)`.
2. If the latest tool result is a `fetch_requirement` result that begins with `Error`, repeat that call with identical arguments. (Error results from the probe calls of step 4 are ignored, never retried.)
3. If the fetched document contains `[[loop-forever]]`, call `fetch_requirement` again, every turn, forever.
4. If the fetched document contains `[[probe-permissions]]` and the probes have not been made yet, make two probe calls on consecutive turns — `write_file(file_path="/memories/AGENTS.md", content="probe")` (expected to be denied) and `read_file(file_path="/../../tickets.json")` (expected to fail: paths above the root are unreachable) — then continue.
5. Otherwise proceed one stage per turn `write_file` of the skeleton with Confirmed Facts = one `- <sentence>` bullet per non-title sentence of the document; `edit_file` filling Ambiguities with one bullet per sentence containing a `VAGUE_WORDS` entry — whole-word, case-insensitive match; `w` is the first such word in sentence order (so `archived securely` matches `securely`, not `secure`) — lines: `- **"<sentence>"**`, `  Reason: "<w>" has no measurable definition.`, plus `  Resolved by: a stated value or definition for "<w>".` **only if the system prompt it received contains the text `Resolved by:`**, plus `  Edge case: two teams implement "<w>" differently and the feature fails acceptance.` **only if the system prompt contains `Edge case:`**; `edit_file` filling Clarification Questions with one `- What value or definition is intended by "<w>" in "<sentence>"?` per ambiguity; `edit_file` filling Assumptions with one `- Until answered, a developer will pick their own meaning of "<w>".` per ambiguity; `edit_file` filling Summary with `The document states <facts> facts. <ambiguities> clauses are ambiguous and need clarification before work starts.` — plus a third sentence `Search quality is hard to specify.` when the document title is `Catalog Search` (a planted one-off, so the batch holds exactly one run that differs); then a final message with no tool call: `Review complete.` — or, if the document contains `[[claim-success]]`, `Review complete. Every ambiguity bullet already carries its Resolved by and Edge case lines, so all three criteria are satisfied.` (a false claim; the file is unchanged). If the document contains `[[skip-stage]]`, the Assumptions stage is skipped on this first pass (the section stays empty).
6. After a grader-feedback message arrives (any non-tool message following its `Review complete.` or `Revision complete.`), the next turn is one `edit_file` replacing the whole Ambiguities section with the same bullets carrying **all three** labelled lines; if Assumptions is still empty, one further `edit_file` fills it as in step 5; then a final message `Revision complete.`

*Grader script* (two turns per grading pass): turn 1 calls `read_file(file_path="/analysis.md")`; turn 2 returns the structured `GraderResponse`. If the file content contains `[[grader-error]]`, it raises `RuntimeError("scripted grader failure")` instead. If it contains `[[rubric-unevaluable]]`, it returns result `failed` with an empty criteria list and explanation `Rubric cannot be evaluated.` Otherwise three criteria in rubric order: completeness passes iff the file exists, each of the four list sections has ≥ 1 bullet and Summary ≥ 1 word; clarity passes iff every Ambiguities bullet has an indented line beginning `Resolved by:`; depth passes iff every Ambiguities bullet has an indented line beginning `Edge case:` **and** the file does not contain `[[never-satisfied]]`. Each failing criterion's `gap` is `<k> of <n> Ambiguities bullets lack an indented '<Label>' line` where `<Label>` is `Resolved by:` or `Edge case:` including the colon, except: completeness's gap is `a section is empty`, and whenever the file contains `[[never-satisfied]]` depth's gap is `depth cannot be confirmed` (this marker rule takes precedence over the count form). Criterion names are **paraphrased on purpose** to exercise positional matching: on odd-numbered passes (every first attempt included) `Completeness check`, `Clarity (Resolved by lines)`, `Depth (Edge case lines)`; on even-numbered passes `completeness`, `clarity`, `depth`. `result` is `satisfied` iff all three pass, else `needs_revision`; `explanation` is one sentence.

*Analyst script* (five turns): `write_file(file_path="/<label>/summary.json", content="probe")` (expected to be denied); `read_file("/<label>/summary.json")`; `read_file("/<label>/AGENTS.md")`; `write_file("/proposal.md", <text>)` where `<text>` is `# Proposal\n\nFirst-attempt failures recur on clarity and depth across the batch.\n\nProposed insertion under ### Ambiguities: the two labelled lines.\n`; then the structured response equal to `fixtures/changes/change_v1.json`.

**Replay of the verdict-bearing numbers** (every value asserted below follows from these scripts): under the baseline instructions the review omits both labelled lines, so pass 1 of every batch run is completeness pass / clarity fail / depth fail, the revision adds both lines, pass 2 is all-pass → v1 summary completeness 5/5, clarity 0/5, depth 0/5, revisions 5, attempts 10. After `change_v1.json` is applied the instructions contain both labels, so pass 1 is all-pass → v2: 5/5/5, revisions 0, attempts 5. After `change_partial.json` (applied to the baseline) only `Resolved by:` is present → batch `v1b`: completeness 5/5, clarity 5/5, depth 0/5, revisions 5, attempts 10. Hence compare(v1, v2) = success with improved [clarity, depth]; compare(v2, v1) = regression; compare(v1, v1) = no effect; compare(v1, v1b) = partial with improved [clarity].

### 5.2 Criteria

All criteria run with `MODEL_BACKEND=scripted` unless tagged `live`. **"Fresh init"** in a Given means the test first calls `POST api/reset` (§3.8), which wipes `data/` and re-seeds it per R25, so every criterion starts from the AC1 state unless its Given says it builds on another criterion (§7 says how such chains are replayed). A Given that says "a marker page with a linked ticket" means: Fresh init, then `POST api/pages` with the named marker document as `body`, title `Marker <name>`, author `Avery (Product Manager)`, then `POST api/tickets` with title `Review marker`, description `Marker run.`, `linked_page_id` = that page, assignee `Blake (Eng Lead)`; the run under inspection is the one that ticket creation triggered. `live` criteria run with `MODEL_BACKEND=live` and the lab's ambient variables, are excluded from the offline run, and are non-deterministic in wording — they assert shape, not text.

| AC | Given | When | Then | Rules |
|---|---|---|---|---|
| AC1 | An empty `data/` directory | The app starts | The structures of R25 exist exactly as declared: one page `page-session-timeout-requirements` with one version whose body equals `fixtures/seed/req_06_session_timeout.md`; one ticket `REQ-100`, status `Open`, `last_run_id` null; `analysis_runs.json` is `[]`; `data/instructions/AGENTS.md` is byte-identical to `fixtures/instructions/AGENTS.md`; `data/run_history/` and `data/workspaces/` exist and are empty | (R25) |
| AC2 | The app is started with no arguments | A client requests `http://0.0.0.0:4000/` and `http://0.0.0.0:4000/api/health` | Both return 200; the first is HTML; the second's JSON has `model_backend` `scripted` and `port` 4000; no other port is listened on | (R23) |
| AC3 | The app is running after AC20 (so every page has content and the report page has two versions; the compare page is fetched with `a=1&b=2`) | Each page path in §3.8 is fetched and every `href`, `src` and `action` attribute value is extracted | No value starts with `/`, `http:`, `https:` or `//`; no page references a WebSocket | (R23) |
| AC4 | A completed run (AC5) | The build folder root is listed and the app's source is searched for the string `AGENTS.md` | No file `AGENTS.md` exists at the build-folder root that the app created; every path the app uses for the file is `fixtures/instructions/AGENTS.md` (read only, for seeding and reset) or under `data/instructions/`, `data/workspaces/<run>/memories/` or `data/run_history/<label>/` | (R24) |
| AC5 | Fresh init (AC1) | `POST api/tickets/REQ-100/rerun` with an empty body | The returned run has `status` `satisfied`; its trace's first row is `Model reasoning` / `Calls fetch_requirement`, exactly one `Tool` row has action `fetch_requirement` and its detail does not begin with `Error`; exactly one `Tool` row whose action begins `write_file`, and exactly four `edit_file` rows before the first grading pass (that is, before the first `Finishes the review` row — grader turns are not trace rows, R10), filling, in order, Ambiguities, Clarification Questions, Assumptions, Summary; `stage_order` is the five sections in §3.4 order and `complete` is true; `counts` = `{Confirmed Facts: 4, Ambiguities: 1, Clarification Questions: 1, Assumptions: 1}`; `simulated_failures` 0, `rubric_iterations` 3, `max_turns` 40; the run is present in `data/analysis_runs.json` | (R1, R3, R10, R22) |
| AC6 | Fresh init | `POST api/tickets/REQ-100/rerun` with `{"simulated_failures": 2}` | The trace holds exactly three `Tool` rows with action `fetch_requirement`: the first's detail begins `Error: requirement service returned 503`, the second's begins `Error: requirement service timed out`, the third's begins `REQUIREMENT: Session Timeout`; each error row is immediately followed by a `Model reasoning` row calling `fetch_requirement` again; the run ends `satisfied` | (R1, R2) |
| AC7 | The run of AC5 | `grading[0].analysis_markdown` is parsed | It starts with `# Requirements Analysis`, has the five `##` headings in the §3.4 order and no others; its single Ambiguities bullet matches the first two line regexes of §3.4 and has **no** `Resolved by:` or `Edge case:` line; Summary has exactly two sentences; the final `analysis_markdown` (from `grading[1]`) matches all four line regexes | (R3, R4) |
| AC8 | Fresh init; `POST api/tickets/REQ-100/close`; then the seed page is saved (`POST api/pages/page-session-timeout-requirements/versions`) with body = `loop_forever.md` and author `Avery (Product Manager)` — `retriggered` is `[]` because the ticket is Done | `POST api/tickets/REQ-100/rerun` with `{"rubric_iterations": 0, "max_turns": 12}` | The run's `grading` is `[]`, `status` is `ungraded`, `turns` is 12, `complete` is false, `stage_order` is `[]`; the last trace row is `Model reasoning` / `Stops: turn limit of 12 reached` and every other `Model reasoning` row calls `fetch_requirement` (12 of them, each followed by its `Tool` row); `counts` are all 0; the ticket's status is still `Done`; `page-analysis-req-100` exists with one version whose body is the R12 banner (`REQ-100`, `Source requirement: version 2.`, `**ungraded**` after `0 grading pass(es)`), a blank line and `_No analysis file was written._` | (R5, R9, R12) |
| AC9 | The run of AC5 | Its `grading` list is inspected | Exactly two passes. Pass 1: `result` `needs_revision`, criteria by position (first = completeness, second = clarity, third = depth; pass 1's names are the paraphrased forms) `passed` true, false with `gap` containing `'Resolved by:'`, false with `gap` containing `'Edge case:'`. Pass 2: `result` `satisfied`, three criteria (canonical names) all `passed` true. Pass 1's `analysis_markdown` lacks both labels; pass 2's contains both on its Ambiguities bullet; after pass 1 the trace shows one `Tool` row whose action begins `edit_file` (filling Ambiguities) and a final `Finishes the review` | (R4, R8, R9, R10) |
| AC10 | Fresh init, then `data/instructions/AGENTS.md` is deleted | `POST api/tickets/REQ-100/rerun` | HTTP 500 whose JSON `error` names `data/instructions/AGENTS.md`; `data/analysis_runs.json` is unchanged; the ticket is still `Open` | (R6) |
| AC11 | A marker page from `probe_permissions.md` with a linked ticket | The triggered run is inspected | The trace contains a `Tool` row with action `write_file` whose detail begins `Error` (its model row's detail is `/memories/AGENTS.md`) and, on the next tool row, a `Tool` row with action `read_file` whose detail begins `Error`; the run's `instructions` equals the current `data/instructions/AGENTS.md` byte for byte; `data/tickets.json` is unchanged by the run except for the ticket's own fields; `status` is `satisfied` | (R6, R7) |
| AC12 | Fresh init | Two `rerun` calls on `REQ-100` back to back | Both runs are `satisfied`, both traces begin with the fetch and contain exactly one `Tool` row whose action begins `write_file`; after each call `data/workspaces/` contains no directories | (R7) |
| AC13 | A marker page from `never_satisfied.md` with a linked ticket | The triggered run is inspected | `status` is `max_iterations_reached`; `grading` has at least two passes, every pass is `needs_revision`, every pass's depth criterion (third position) has `passed` false with `gap` `depth cannot be confirmed`; the report banner's status line reads `**max_iterations_reached**` | (R8, R9) |
| AC14 | A marker page from `grader_error.md` with a linked ticket | The triggered run is inspected | `grading[0].result` is `grader_error` with empty `criteria`; `status` is `grader_error`; the run is recorded in `data/analysis_runs.json` and the ticket is `Analysis Ready` with `last_run_id` = that run | (R9, R10) |
| AC15 | A marker page from `rubric_unevaluable.md` with a linked ticket | The triggered run is inspected | `grading[0].result` is `failed` with empty `criteria`; `status` is `failed` | (R9) |
| AC16 | Fresh init | `rerun` with an empty body, then with `{"rubric_iterations": 1}` | The first run records `rubric_iterations` 3; the second records 1 and still ends `satisfied` with two grading passes | (R9) |
| AC17 | The run of AC5 | Its trace rows are checked pairwise | Every `Tool` row is immediately preceded by a `Model reasoning` row; every `detail` is ≤ 221 characters and any 221-character detail ends with `…`; `step` values are 1..N consecutive | (R10) |
| AC18 | The run of AC5 | The app process is stopped and started again, then `GET api/runs/<id>` | The identical run record is returned | (R10) |
| AC19 | Fresh init, then `POST api/tickets/REQ-100/close` (so the seed ticket is `Done` and cannot be re-triggered) | `POST api/tickets` with title `Review: Session Timeout`, description `Please review before implementation.`, `linked_page_id` `page-session-timeout-requirements`, assignee `Casey (QA Lead)` | 201 with key `REQ-101`; the response's `run_id` names a run with `status` `satisfied`; the ticket is `Analysis Ready` with `last_analyzed_version` 1 and `last_run_id` = that run; page `page-analysis-req-101` exists, kind `analysis_report`, title `Analysis Report — REQ-101`, one version by `Requirements Review Agent (bot)` whose body's first three lines are the R12 banner with `REQ-101`, `version 1`, `**satisfied**` and `2 grading pass(es)`, followed by a blank line and a body equal to the run's final `analysis_markdown`; the ticket has one comment by the bot reading `Analysis complete (satisfied), requirement version 1. See Analysis Report — REQ-101 in Confluence.` | (R11, R12) |
| AC20 | After AC19 | `POST api/pages/page-session-timeout-requirements/versions` with body = `fixtures/seed/req_06_session_timeout.md` with the sentence `Sessions shall time out after 30 minutes.` appended as a new paragraph (a blank line, then the sentence) and author `Avery (Product Manager)` | `retriggered` is `["REQ-101"]`; the ticket now has two runs, the latest with `requirement_version` 2; `page-analysis-req-101` has version 2; `GET jira/REQ-101` HTML contains the heading `What changed since the previous run` and the four section names with previous/latest counts (`Confirmed Facts` 4 → 5); `last_analyzed_version` is 2 | (R11, R12, R14) |
| AC21 | After AC20, `POST api/tickets/REQ-101/close` | The same page is saved again (same author, body unchanged) | `retriggered` is `[]`; the ticket still has exactly two runs; a save of a newly created page with no linked ticket at all also returns `retriggered` `[]` | (R11, R13) |
| AC22 | After AC21 | `GET api/pages/page-session-timeout-requirements` | Its versions are exactly the three written by people (the seed, AC20's save, AC21's save — authors from the cast), none by the bot; the report page's every version has author `Requirements Review Agent (bot)` | (R12) |
| AC23 | After AC21 | `POST api/tickets/REQ-101/rerun`, then the page is saved again | The rerun records a third run and the ticket's status is still `Done` (never moved out of `Done`, never set to `Done` by a run); the save returns `retriggered` `[]`; across chain B's runs (§7) no run set a ticket to `Done` — REQ-101 became `Done` only through AC21's close call | (R13) |
| AC24 | After AC20 | `GET api/pages/page-analysis-req-101/compare?a=1&b=2` | `diff` begins with `--- version 1` and `+++ version 2`, contains at least one `+` line holding `30 minutes`; `run_a` and `run_b` are the two runs with `requirement_version` 1 and 2 | (R14) |
| AC25 | Fresh init | `POST api/tickets` with assignee `Nobody`; `POST api/pages` with author `Nobody` | Both return 400 and nothing is created | (R15) |
| AC26 | Fresh init | `POST api/batches` with `{"label": "v1"}` | `data/run_history/v1/` holds `AGENTS.md` (byte-identical to the current instructions), `run_01_req_01_password_reset.json` … `run_05_req_05_rate_limiting.json` and `summary.json`; the summary is `runs` 5, `graded` 5, `grader_errors` 0, completeness `{5,5,1.0}`, clarity `{0,5,0.0}`, depth `{0,5,0.0}`, `revisions_needed` 5, `documents` = the five stems in order; every run file has two grading passes and `status` `satisfied`; the app process is restarted and `GET api/batches/v1` returns the same summary | (R16) |
| AC27 | Fresh init | `POST api/batches` with `{"label": "mixed", "docs": ["fixtures/requirement_docs/req_01_password_reset.md", "fixtures/marker_docs/grader_error.md"]}`, then with `{"label": "errors", "docs": ["fixtures/marker_docs/grader_error.md"]}` | `mixed`: `runs` 2, `graded` 1, `grader_errors` 1, every `total` is 1, completeness `passed` 1, clarity 0, depth 0, `revisions_needed` 1, `attempts` 3. `errors`: `runs` 1, `graded` 0, `grader_errors` 1, every `total` 0 and every `pass_rate` `null`, `revisions_needed` 0; `GET api/compare?before=mixed&after=errors` returns 400 (different `runs`) | (R16, R19) |
| AC28 | The `v1` batch of AC26 | Each run file's grading passes and the summary are read | Pass 1 of every run carries the paraphrased names (`Completeness check`, …) — so name-based matching would find no `completeness` at all — while the summary's `first_attempt` keys are exactly `completeness`, `clarity`, `depth` and its counts are those of AC26 | (R16) |
| AC29 | The `v1` batch of AC26; a SHA-256 of every file under `data/run_history/v1/` is taken | `POST api/proposals` with `{"label": "v1"}` | 201 with `change` deep-equal to `change_v1.json` and `proposal_markdown` equal to the analyst script's text; every hashed file is unchanged (the probe write was denied); the response's `trace` contains a `Model reasoning` row `Calls write_file` with detail `/v1/summary.json` whose `Tool` row's detail begins `Error`, later two `Tool` rows with action `read_file`, and a `Calls write_file` row with detail `/proposal.md` whose `Tool` row's detail does not begin `Error`; `change.rejected` has one entry naming `run_03`, and `data/run_history/v1/run_03_req_03_search_results.json`'s final `analysis_markdown` has a three-sentence Summary while the other four have two | (R17) |
| AC30 | After AC29 | `GET api/proposals/v1` | Returns `label`, `change` and `proposal_markdown` equal to AC29's; `data/run_history/proposal_v1.json` holds the change and `proposal_v1.md` the markdown | (R17) |
| AC31 | Fresh init | `POST api/instructions/apply` with `change_v1.json` and `approved` true | 200; the returned text equals the baseline with the two `change` lines inserted after `Quote the exact clause, then give the reason it is under-specified.` and one blank line, before `### Clarification questions`, with one blank line between; `GET api/instructions` returns the same text; `data/instructions/AGENTS.md` matches | (R18) |
| AC32 | Fresh init | `POST api/instructions/apply` with `change_v1.json` and no `approved` field, then with `approved` false | Both return 400; the instructions are byte-identical to the baseline | (R18) |
| AC33 | Fresh init | Apply `change_tool_target.json`, `change_grader_target.json`, `change_configuration_target.json` and `change_missing_section.json`, each approved | All four return 400 with an `error` naming, respectively, the target `tool`, the target `grader`, the target `configuration` and the section `### Nonexistent`; the instructions are unchanged | (R18) |
| AC34 | After AC26; then `POST api/instructions/apply` with `change_v1.json` and `approved` true (the AC31 call, without AC31's reset) | `POST api/batches` with `{"label": "v2"}` | Summary: completeness, clarity and depth each `{5,5,1.0}`, `revisions_needed` 0; every run file has exactly one grading pass, `satisfied`, and its Ambiguities bullets all carry both labelled lines; `data/run_history/v2/AGENTS.md` contains the inserted lines | (R4, R16) |
| AC35 | After AC34 | `GET api/compare?before=v1&after=v2` | `verdict` `success`; `criteria` completeness `[5,5]`, clarity `[0,5]`, depth `[0,5]`; `revisions_needed` `[5,0]`; `attempts` `[10,5]`; `improved` `["clarity","depth"]`; `regressed` `[]` | (R19) |
| AC36 | After AC34 | `GET api/compare?before=v2&after=v1` | `verdict` `regression`; `regressed` `["clarity","depth"]`; `improved` `[]` | (R19) |
| AC37 | After AC34; then `POST api/instructions/reset`, apply `change_partial.json` (approved), `POST api/batches` `{"label": "v1b"}` | `GET api/compare?before=v1&after=v1` and `GET api/compare?before=v1&after=v1b` | The first is `no effect` with empty `improved` and `regressed`; the second is `partial` with `improved` `["clarity"]`, `regressed` `[]`, `revisions_needed` `[5,5]`, and `v1b`'s summary is completeness 5/5, clarity 5/5, depth 0/5 | (R19) |
| AC38 | `MODEL_BACKEND=live` with `OPENAI_API_KEY` unset and `OPENAI_BASE_URL`, `REVIEW_MODEL`, `GRADER_MODEL`, `ANALYST_MODEL` all set | The app starts, `GET api/health`, then `POST api/tickets/REQ-100/rerun` | Health reports `model_backend` `live`; the rerun response is an error (HTTP 500) whose `error` names `OPENAI_API_KEY`; the app never blocked waiting for input; no file under `data/` contains the string `OPENAI_API_KEY=` | (R20) |
| AC39 | `ANTHROPIC_API_KEY` and `ANTHROPIC_BASE_URL` removed from the environment | The app's source tree is searched for `ANTHROPIC` (the §7 offline command already runs every offline criterion with both `ANTHROPIC_*` variables unset) | The search finds no match in app code (this spec and tests excluded); the app started and answered `GET api/health` without them | (R20) |
| AC40 `live` | `MODEL_BACKEND=live`, the four lab variables and three role variables set | `POST api/tickets/REQ-100/rerun` | The run's `status` is `satisfied` or `max_iterations_reached`; the trace contains ≥ 1 `fetch_requirement` tool result and ≥ 1 `write_file` row; the final `analysis_markdown` is complete (every list section ≥ 1 bullet, Summary ≥ 1 word) | (R21) |
| AC41 `live` | `MODEL_BACKEND=live`; a batch `live1` of the five documents has been run | `POST api/proposals` with `{"label": "live1"}` | The response validates against §3.6; `target` is one of the four values; every `evidence` string is non-empty; `data/run_history/live1/` files are unchanged | (R17, R21) |
| AC42 | No `MODEL_BACKEND` set | `GET api/health` | `model_backend` is `scripted` and `roles` reports `ScriptedModel` for all three roles; the app started and answered without `OPENAI_API_KEY` set (the §7 offline command unsets it) | (R20, R22) |
| AC43 | A marker page from `skip_stage.md` with a linked ticket | The triggered run is inspected | `grading[0]` is `needs_revision` with completeness `passed` false and `gap` `a section is empty`, and its `analysis_markdown` has an empty Assumptions section; `grading[1]` is `satisfied`; the final file is complete (`complete` true, `counts` Assumptions ≥ 1); `stage_order` lacks `Assumptions` (it was filled only after feedback) | (R3, R9) |
| AC44 | A marker page from `claim_success.md` with a linked ticket | The triggered run is inspected | The first `Finishes the review` row's detail contains `all three criteria are satisfied`, yet `grading[0]` is `needs_revision` with clarity and depth `passed` false; `grading[0].analysis_markdown` has no `Resolved by:` line | (R8) |

Every rule R1–R25 is cited by at least one criterion above (AC1–AC44); every criterion cites at least one rule; the lists are reciprocal.

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the offline suite (`MODEL_BACKEND=scripted`) before reporting any criterion as passing, and quote its output.
- Record every resolved value, model-role assignment and test result in files in the workspace (`resolved-decisions.md`, the §7 report) — `[environment]` a new chat starts with no memory of this one and the grader sees only what is on disk.
- Keep the agent's instructions file under `data/` and inside each run's workspace (R24).
- Keep every served URL relative (R23).

**Ask First** (derived from the course's spoken trade-offs, CTX-C's table; each either forces rework or changes a guarantee no criterion catches)
- Changing the model behind any role, or splitting the grader onto a different model than the review agent (the course argues a separate grader model is "a common production choice" and that cheaper models suit simpler tasks — a tiering lever on the lab-constrained model dimension; no offline criterion notices the swap).
- Changing `rubric_iterations` from 3 (including to 0, which removes the grader) — alters the retry guarantee; AC16 reads the recorded value, so no criterion fails (lever, CTX-C6).
- Applying a proposal whose compare verdict is anything but `success`, or applying one whose `target` is not `prompt` by hand — the course gates harness merges on eval results and human review (CTX-C8).
- Switching the instruction store (Ledger D2) or the grader type (Ledger D3) — structural; re-run the whole suite.
- Running the acceptance suite against a live model instead of the scripted stand-in (§2 Acceptance-suite model) — the completion gate would then depend on the ambient key and on model behaviour; no criterion notices the swap.

**Never**
- Author, read or edit the workspace-root `AGENTS.md` `[environment]` — the IDE rewrites it at every boot.
- Modify a fixture under `fixtures/` to make a criterion pass.
- Invent provenance: never label a constraint course-derived unless a `(CTX-…)` anchor backs it.
- Write a run's analysis into the requirement page, or let a run set a ticket to `Done` (R12, R13).
- Apply an instruction change without `approved: true`, or let a model decide where inserted text lands (R18).
- Hardcode, prompt for, log or write to disk any API key; read `ANTHROPIC_*` (R20).
- Answer when the system should abstain: a grader that cannot confirm a criterion fails it with a gap (R8).
- Report "should pass" or "looks correct" — only cited test output counts (§7).

## 7. Test Plan & Self-Verification

```bash
# 0. Record the interpreter (first build step; stop and report if a pin refuses it)
python3 --version

# 1. Environment (one early batched install; announce its wall-clock cost first)
python3 -m venv --system-site-packages .venv && . .venv/bin/activate
pip install "deepagents==0.7.11" "langchain==1.3.18" "langchain-core==1.6.1" \
  "langchain-openai==1.6.0" "langgraph==1.2.11" "openai==3.6.0" "pydantic==2.13.5" \
  "python-dotenv==1.2.3" "flask>=3.1.3" pytest

# 2. Offline acceptance suite — the build is complete when this is green
rm -rf data && env -u OPENAI_API_KEY -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL MODEL_BACKEND=scripted python -m pytest -q tests -m "not live"

# 3. Serve for the preview (background; the lab proxies port 4000)
MODEL_BACKEND=scripted python -m app     # binds 0.0.0.0:4000
curl -s http://0.0.0.0:4000/api/health

# 4. Live criteria (optional; needs the lab's OPENAI_* variables and the three role variables)
MODEL_BACKEND=live python -m pytest -q tests -m live
```

The test package `tests/` holds one test per criterion, named `test_ac<NN>`, marked `live` where the table says so; a Given that names another criterion ("The run of AC5", "After AC20", "The `v1` batch of AC26") means the test first replays that criterion's whole chain from Fresh init inside itself — every chain is deterministic, so a session-scoped pytest fixture may compute a chain once and hand its result to each dependent test — and no test ever relies on the file order of other tests or on state another test left behind. The chains are: A = AC5 → {AC4, AC7, AC9, AC17, AC18}; B = AC19 → AC20 → {AC3, AC24, AC21 → {AC22, AC23}}; C = AC26 → {AC28, AC29 → AC30, AC34 → {AC35, AC36, AC37}}. Each test drives the running app through its HTTP API (the suite may start the app in-process on port 4000) and checks files under `data/` directly where the criterion names them.

**Reporting.** When done, report **per acceptance criterion** AC1–AC44: pass / fail / retired (with the gate answer that retired it), each with cited evidence — the pytest line, and for file assertions the path checked. "Should pass" and "looks correct" are failures: they mean it was not run. Also report the `python3 --version` output, the install command's wall-clock time, and the model-roles line from `resolved-decisions.md`.

**Closing instruction.** Conclude your final report with an infra/structure diagram of the built app — the server, the stores under `data/`, the per-run workspace, the review agent and its tools, the grader, the fetch store, the batch runner and analyst, and the fixtures — and end with the exact phrase: **"This is the infra/structure diagram of this app"**.

## Runtime (lab)

Everything in this section is `[environment]` provenance — facts about the lab the build must obey, none of them from the course.

**Container.** Debian, non-root user, Node 22, Python 3 with venv (minor version not stated — record it, §2), sqlite3, git, build tooling. Preinstalled Python: `fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`; Node: `express`, `cors`, `better-sqlite3`, `vite`, `nodemon`. Nothing else. Outbound network works; every install costs wall-clock time inside the session, so §2's install is one early batched command with its cost announced. Venvs are created with `--system-site-packages`; where a course pin differs from a preinstalled copy, the course pin wins inside the venv. Memory is finite and shared with the agent's own process; this pipeline loads no local models (all models are remote or the in-process scripted stand-in), so no release-before-load rule is needed.

**Preview.** One server, port 4000, bound to `0.0.0.0`, serving both the pages and the API; nothing else is previewable. Every URL inside a page is relative. HTTP only — WebSocket upgrades are not proxied; streaming responses work.

**Workspace.** The workspace is the record: a new chat has no memory of an earlier one and the grader sees only what is on disk — which is why `resolved-decisions.md` and the §7 report are written as files, not left in chat. The workspace-root `AGENTS.md` is rewritten by the IDE at every boot and is never authored (the §6 Never list); the course's instructions file of the same name lives inside app-owned folders (R24). Every tool call is visible to the learner; long-running servers run in the background.

**Models.** The lab fixes the model the coding agent itself runs on, exports `OPENAI_API_KEY`/`OPENAI_BASE_URL` and `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL` pointing at the platform proxy, and does not enumerate its model set. The app reads the OpenAI pair only (R20); the role variables are set at checklist time (§2).

**Environment failure modes** (pitfalls the lab creates; enforced by rules and criteria here, never listed in CTX-B):

- **E1 — root-absolute URL under the proxied preview.** Symptom: pages load but every link, form and `api/` call 404s or lands on the IDE. Cause: an `href="/api/..."` resolves against the proxy root. Fix: relative URLs everywhere. Enforced by R23, AC3.
- **E2 — guidance lost in the workspace-root `AGENTS.md`.** Symptom: instructions written there vanish at the next boot; or the app's instructions collide with the IDE's file. Cause: the IDE rewrites that one file. Fix: the app's instructions live under `data/`; the root file is never touched. Enforced by R24, AC4.
- **E3 — asking for a key the lab already supplied.** Symptom: the build stalls on a prompt for an API key. Cause: not reading the exported variables. Fix: read the exported names only. Enforced by R20, AC38, AC42.

Three further lab pitfalls are build-process facts rather than app behaviour and are handled by §2 and §6 rather than by a rule and criterion: a course pin may refuse the container's Python (record `python3 --version` first, stop and report rather than substitute — §2, evidence in the §7 report); a preinstalled package may shadow a course pin (install the pin inside the venv so it wins — §2); and anything left only in chat is lost to the grader (the §6 Always list).

## Course Context Pack (embedded — agent-readable)

Concepts only; no code from the course appears here. Anchors are position-independent.

### CTX-A. The pattern

The course's central buildable pattern is one agent wrapped in four nested loops, each a ring around the previous:

1. **Agent loop** — `request (ticket id) → model → tool call → observation → … → result`. The model receives context, calls tools, observes, and repeats until it decides it is done. The model must call tools natively — the harness executes real tool calls, not narrated intentions — and the analyst's result is a typed object. Here the tools are one custom fetch tool and the harness's file tools; the agent is never handed the document — it is told an id and must fetch it, as it would against a real tracker — and the result is a file, not a message: the deliverable is `/analysis.md`, which anyone can open rather than parse out of a reply. The instructions live in a file loaded into context on every run (what is always true: role, procedure, rules), kept short because it costs context every call. The harness confines the agent to a virtual filesystem root and denies writes to its own instructions. A model-call cap exists for the case where the normal stop (the agent's closing message) never comes.
2. **Verification loop** — `agent loop → grader (rubric) → pass: done | fail: retry with feedback`. "Finished" is not "good enough": a second model, with its own instructions and a read tool, scores the finished file against explicit criteria, and either accepts it or injects specific feedback for another attempt, bounded by a revision budget. All criteria must pass in the same pass. Explicit criteria raise reliability and make cheaper models viable on harder tasks.
3. **Event-driven loop** — `event trigger → verification loop → system update → new events`. The agent is looped into the systems where the work already happens: a ticket created or a linked requirement page edited triggers the review; the result is written back as a new version of a separate, agent-owned page so the system of record keeps every past analysis and who wrote it; a human, not the agent, decides when the ticket is done. The trigger seam is one function a real webhook would call.
4. **Hill-climbing (learning) loop** — `many runs → traces → analyst → proposed harness change → human approval + evals → improved agent`. Agents are non-deterministic, so the story is in the traces. A batch of runs under one instructions version is summarised by what failed on the **first** attempt; an analyst agent reads the summary, the runs and the instructions and proposes the one change that would remove the correction the grader makes every time; a person approves; plain code applies it; the batch is re-run and compared, criterion by criterion, before anything is kept. Two kinds of improvement exist — procedural (prompts, tool descriptions, skills) and memory (preferences persisted across runs); this build does the first.

Human oversight has a place at every ring: approving sensitive tool calls (agent loop), acting as grader (verification), approving outputs before delivery (event loop — here, marking Done), and reviewing harness changes before deployment (learning loop — here, the approval on apply).

### CTX-B. Failure-mode catalog

- **CTX-B1 — The external fetch fails transiently.** Symptom: the fetch tool returns an error (service unavailable, timeout) instead of the document. Cause: external systems are flaky; a run that gives up on the first error never starts. Fix: the agent treats an error result as a signal to call the same tool with the same arguments again; the tool's own description says so. The fixture injects two failures. Enforced by R1, R2, AC6.
- **CTX-B2 — A half-written or unparseable review.** Symptom: a section missing or empty; sections out of order; two stages collapsed into one call. Cause: the agent has every tool on every turn and the order is only requested. Fix: a fixed five-section skeleton written once, then one edit per section; the record reports completeness and the order actually followed. Planted instance: the `skip_stage.md` marker makes the first pass leave Assumptions empty. Enforced by R3, AC5, AC7, AC43.
- **CTX-B3 — The first draft names a vagueness without saying what would settle it or what it breaks.** Symptom: the grader fails clarity and depth on the first attempt — in the course's batch, on every one of five documents. Cause: the baseline instructions never ask for the `Resolved by:` and `Edge case:` lines the rubric requires. Fix: short term, the grader's feedback drives a revision that adds them; long term, the learning loop inserts the missing guidance so first attempts pass. Enforced by R4, R9, AC9, AC34.
- **CTX-B4 — The agent keeps retrying past the point where retrying makes sense.** Symptom: a run that never emits its closing message. Cause: a tool that never succeeds, or a model that loops. Fix: a model-call cap per run (12 for a plain review, 40 with a grader), with the trace stating the cap stopped it. Enforced by R5, R9, AC8.
- **CTX-B5 — A review produced without its guidance, or an agent that rewrites its own rules.** Symptom: a plausible but bad review; or instructions drifting mid-run. Cause: the harness silently ignores a missing memory file; the agent has an edit tool and its instructions sit in the same filesystem. Fix: fail loudly when the file is missing; deny writes under the instructions directory at the permission layer; keep the file inside app-owned folders — the course seeds each run's own workspace with it and keeps its one tracked copy under a workspace directory, never beside the code. Enforced by R6, R24, AC4, AC10, AC11.
- **CTX-B6 — Leftover state from an earlier run.** Symptom: the agent reads a finished analysis from a previous run and skips stages; two tickets analysed back to back see each other's files. Cause: a shared workspace. Fix: one fresh confined workspace per run, removed afterwards. Planted instance: the `probe_permissions.md` marker has the agent try to read above its root (the confinement half). No leftover `/analysis.md` fixture can be planted for the fresh-workspace half: the app creates each workspace itself, so a planted file would have to bypass the very rule under test, and the scripted review reads only its conversation, so a leftover file could not change what it does. The fresh-workspace half is checked structurally instead: AC12 runs two reviews back to back, the first leaving an `/analysis.md` behind if workspaces were shared, and asserts the workspace is removed after each. Enforced by R7, AC11, AC12.
- **CTX-B7 — The grader passes by resemblance.** Symptom: criteria pass that the file does not satisfy. Cause: the grader is handed the whole conversation, which reads like success, and judges from it. Fix: the grader must read the file, quote the satisfying text with its line number, apply labels literally, check every item, and fail anything it cannot confirm. Planted instance: the `claim_success.md` marker makes the agent's closing message claim the criteria are met while the file lacks the lines. Enforced by R8, AC9, AC13, AC44.
- **CTX-B8 — The agent edits the source of truth or closes its own work.** Symptom: the requirement page changes under a run; a ticket flips to Done with nobody having looked. Cause: writing the report into the requirement; letting automation set terminal state. Fix: the report goes to a separate agent-owned versioned page; only a person marks Done; Done tickets are never re-triggered. Planted instance: the `probe_permissions.md` marker's second probe reaches for `tickets.json` above the workspace root, and AC11 asserts the ticket store is unchanged by the run except for the ticket's own fields; the requirement page is not in the agent's filesystem at all, so no fixture can make a run write it — AC22 checks that no version of it is by the bot. Enforced by R7, R12, R13, AC11, AC19, AC22, AC23.
- **CTX-B9 — A systemic failure hidden by the summary.** Symptom: pass rates look fine or look random. Cause: ungraded runs averaged in; the grader paraphrases criterion names differently each run so one recurring failure splits into several. Fix: denominators count graded runs only and say how many errored; criteria are matched by rubric position. Enforced by R16, AC27, AC28.
- **CTX-B10 — Instruction churn from one-off noise, or an analyst that edits its evidence.** Symptom: a change proposed from a single run; traces altered while being analysed. Cause: no discipline about what counts as a pattern; a writable evidence directory. Fix: the analyst may write only its proposal; a problem in one run of five goes under `rejected`. Enforced by R17, AC29.
- **CTX-B11 — A harness change merged on faith.** Symptom: the "improved" agent is worse on a criterion nobody re-checked; or a model-applied edit lands in the wrong place. Cause: no eval after the change; letting a model perform the edit. Fix: human approval, plain-code insertion at the named section, re-run the batch, compare first-attempt verdicts, and treat any regression as a regression. Enforced by R18, R19, AC31, AC35, AC36.

### CTX-C. Decision background

**How to read the provenance notes.** A *litmus branch* is the outcome of asking whether a course subject is a decision: it becomes a **row** (two legitimate options, listed in the Ledger), a **bake-in** (the course warned against the alternative, so the taught side is a business rule and the warned side is narrative), or a **lever** (the sides differ only in a value, so the value is a body default and the choice is a post-build knob). A *lever* is such a numeric or small-valued setting; a *post-build lever* is one you tune after the build, never asked at the gate. The *lever-value branches* pick a contradicted lever's value deterministically: (1) the value the lesson narration states aloud; (2) failing that, the end-to-end application's config; (3) failing that, the value used most often, earliest-taught on ties. *Stakes* is the test a course-contradicted value must pass to earn a row: would picking the other side up front change structure, semantics or a guarantee. A *substitution row* is one whose Default is a lighter stand-in for what the course actually ran; the course's own choice then sits in Options tagged "(course default)". The *dependency-precedence branch* is the choice made for a heavy course dependency: substitute the lightest invariant-preserving realization, or keep the course's technology because it is the taught subject; a row whose course realization is not heavy records that no substitution was needed. The *heavy bar*: a realization is heavy only if it needs a credential, a paid account, admin or container-level setup, or special hardware — mere network access is not heavy. *Realization tiers* order the lightest candidate: (1) ships with the language's standard distribution; (2) an embedded library; (3) a locally served component. The *keyed-tool rule*: when a course tool needs a key, an honestly-labelled local stand-in is the default if that tool is the only carrier of a taught behaviour. A *scripted stand-in* is a fake model whose responses this spec authors. An *example realization* is the course's own domain-specific instantiation of a pattern stage (its demo tools, its demo data) as opposed to the pattern itself. In CTX-E, *narrated* means a slide whose content a transcript passage describes (it ranks with that lesson's narration) and *deck-only* means a slide no transcript passage matches (it ranks below both narration and code). The Ledger's Category names the route that admitted a row: *design-argued* (the course presented an alternative and argued a trade-off aloud), *design-structural* (choosing differently changes a box, arrow, owner or guarantee of the architecture, even if the course never argued it), *realization* (a heavy-dependency decision), *learner* (a learner-context dimension). A *two-sided* argument is one where the course shows both sides working, not one side as a failure. A *near-equivalent* contradiction is one whose sides differ only in a value and fail the stakes test. Provenance labels on rules: *Course-demonstrated* (traceable to the materials, with a `(CTX-…)` anchor), *Project hardening* (added by this spec; the course did not demonstrate it), *Environment-imposed* `[environment]` (contributed by the lab, never the course), and the one co-label *Course-demonstrated, reinforced `[environment]`* (both sources independently require it).

- **CTX-C1 — System of record (→ §2 System of record; no Ledger row in this build mode, see Not Included #1).** The course's event-driven code simulates Jira and Confluence in one app so the lesson needs no Atlassian account or tokens; its README names the real REST APIs and a webhook endpoint as the next step and says nothing about the agent or loop changes when they are swapped in. The README also claims the course's example environment file carries Atlassian placeholders; the file in the materials carries none — recorded as a materials inconsistency, no effect on this build. The stand-in is the course's own realization, so no substitution was needed and no "(course default)" tag moves. Its ticket creation and page edits pick a person from a small fixed cast rather than free text, because real trackers pull names from an account directory (R15).
- **CTX-C2 — Instruction store (→ Ledger D2).** Lesson 3 teaches three ways to instruct the agent and when each loads: the system prompt (fixed at creation, used every call), the memory file (loaded at the start of every run; for what is always true; costs context every call, so keep it short), and skills (frontmatter name and description always loaded, the body read only when the agent decides the skill applies — "twenty skills cost twenty lines of context, not twenty documents"). The review agent uses the memory file; the primer's poet uses four skills. The course notes instructions in the memory file "carry the same weight" as the system prompt. A code comment also notes the agent's checkpointer is not required for the revision loop and only matches the documented shape — a perishable detail, CTX-D.
- **CTX-C3 — Grader type (→ Ledger D3).** The overview slide states graders can be deterministic or agentic, with LLM-as-judge the classic example; the human-oversight slide names a human grader for sensitive workflows. The course built the LLM judge and discovered it passed criteria the file did not satisfy — grading the conversation by resemblance — so it restated the harness's default grader rules and added three requirements (read the file first, quote with line numbers, apply labels literally). The grader's result vocabulary is `satisfied` / `needs_revision` / `failed`, plus `grader_error` recorded by the harness when the grader call itself fails.
- **CTX-C4 — Acceptance-suite model (→ §2 Acceptance-suite model; no Ledger row in this build mode).** The course's notebooks run live against OpenAI `gpt-5.4-mini` (review agent and grader) and `gpt-5.5` (analyst) and ship pre-captured traces so lessons replay offline; the notebooks warn that live results differ from the video. The scripted stand-in generalises that replay idea: deterministic responses per role, with the real harness around them.
- **CTX-C5 — Model roles and tiering (lever on the lab-constrained model dimension; → Ask First).** Lesson 2: match model intelligence to task complexity to optimise cost — cheaper, faster models for simple tasks; the verification loop "can help keep those core agent loop cycles on track" so cheaper models become viable on harder tasks. Lesson 5: the grader may run on a different model than the agent; the course used the same model for both but calls a separate grader model "a common production choice". Lesson 6 and the course README: the analyst runs on the stronger model because reading five full traces and finding what recurs is the one job the cheaper model does unreliably. Litmus: levers, not rows — the sides differ in which model id fills a role on a dimension the lab resolved.
- **CTX-C6 — Contradicted values resolved as levers.** (a) Revision budget: Lesson 5 narration and notebook set 3, the batch runner sets 3, the event-driven app sets 2 → stakes fail (a knob) → body default 3 by branch (1); post-build lever (R9). (b) Fault injection: Lesson 4 narration says the fetch fails twice before succeeding, the notebook's table and the pre-captured trace agree, but the helper's default is 0 and the notebook never overrides it, so a live run fetched cleanly → a fault-injection switch, not a pattern lever: the acceptance fixture injects 2 (the narrated demonstration) and the app's default is 0 (the value every end-to-end path — the batch runner and the event app — actually ran with) (R2). (c) Tool name: the course's instructions file and helper call the fetch tool `fetch_requirement`; two instruction snapshots in the batch history say `fetch_requirement_from_jira` → binding name `fetch_requirement` (code and narration). (d) The instructions file is `AGENTS.md` in code and narration; one slide says `Agent.md`. (e) Turn caps: 12 for the single-review lesson, 40 wherever a grader is attached, 30 for the poet primer, 40 for the analyst — not contradictions, per-mode values (R5). (f) The learning lesson's narration first says four documents, then five; the notebook runs five → five.
- **CTX-C7 — Counts and diff together.** The course's event app shows bullet counts side by side *and* a full text diff because counts often look similar before and after while the content changed completely (R14).
- **CTX-C8 — Evals and humans gate harness changes.** Lesson 2: a helper agent that can update prompts, tools, skills and memory is only safe to merge with evals that show no regression; human review of harness changes is the fourth oversight point. Lesson 6 assumes a person reviews the proposal before it is applied. Code: the analyst "proposes and does not apply"; plain code performs the edit so it stays reviewable and deterministic; a non-prompt target is read and rejected rather than half-applied (R17–R19).
- **CTX-C9 — Why the trace is the record.** Lesson 2: traditional software's truth is in the code; an agent's is in its traces — what the model did, which tools it called, what the grader said. The batch keeps every message untruncated because the gap between what the agent was told, what it produced, and what it had to be told afterwards is the evidence a diagnosis works from (R10, R16).
- **CTX-C10 — Composability and triggers (narrative).** Lesson 2: the loops nest like Russian dolls but need not all be present — an agent loop alone can sit inside an event loop. Triggers can be scheduled or event-driven; the course builds event and manual triggers only. The event loop is "a bit of a stretch to call a loop": its loop is looping the agent into existing workflows.

**Mined trade-offs and their disposition** (every subject the course argued aloud or named as an alternative; Ask-First entries and the Ledger's design rows trace to this table):

| Subject | Lesson | Disposition |
|---|---|---|
| Model intelligence vs task complexity (cost) | 2 | lever R20 (role variables); Ask First (CTX-C5) |
| Verification loop makes cheaper models viable | 2 | narrative + lever (CTX-C5) |
| Grader deterministic vs agentic vs human (named, not argued) | 2 (slides) | row D3 |
| Loops composable; verification optional inside the event loop | 2 | narrative (CTX-C10); the revision-budget lever's 0 value is the plain loop |
| Scheduled vs event-driven triggers | 2 | narrative (CTX-C10); scheduled is Not Included |
| Human oversight at each loop level | 2 | bake-in R13 (Done) and R18 (approval); tool-call approval and human grader Not Included / D3 |
| Evals must gate harness merges | 2 | bake-in R19; Ask First (CTX-C8) |
| Procedural vs memory improvements | 2 | narrative; memory Not Included |
| System prompt vs memory file vs skills (when each loads, context cost) | 3 | row D2 |
| Max turns is not the normal stop | 4 | bake-in R5 |
| Retry the same tool on transient error | 4 | bake-in R2 |
| Separate grader model is a common production choice | 5 | lever R20; Ask First (CTX-C5) |
| Revision budget; 0 = plain agent loop | 5 | lever R9; Ask First (CTX-C6) |
| Analyst on the stronger model | 6 + README | lever R20; Ask First (CTX-C5) |
| One run in five is not a pattern | 6 + code | bake-in R17 |
| Proposal reviewed by a human before apply | 6 | bake-in R18 |
| Report on a separate page, never the requirement | README (event app) | bake-in R12 |
| Counts and diff shown together | README (event app) | bake-in R14 |
| Simulated Jira/Confluence vs real REST + webhook (named, not argued) | README (event app) | narrative — pinned in §2 (System of record); the alternative is unavailable in this build mode (Not Included #1), so no row |
| Live notebook runs vs pre-captured traces replayed offline (named, not argued) | 4–6 (notebooks) | narrative — pinned in §2 (Acceptance-suite model): the suite always runs on the scripted stand-in, the live models are the app's live mode (R21) (CTX-C4) |
| Fresh workspace per run | code docstrings | bake-in R7 |
| Grader must read the file, not the transcript | code comments | bake-in R8 |
| Apply by plain code, not by a model call | code docstring | bake-in R18 |

**Course-declared identifiers kept as provenance only** (not binding here): course ticket ids `AUTH-142` (the default), `AUTH-101`, `NOTIF-205`, `PAY-310`, `ACCESS-118`, `ALERT-227`; the event app's seed ticket `REQ-104` and page id `page-req-upload`; its five-name cast; its port 5050; the batch labels `v1`/`v2` (kept); run-name and tag strings for hosted tracing; the per-million-token prices used for cost estimates. Declared drop: CSS, badge class names and notebook rendering helpers (presentation only).

### CTX-D. Perishable assumptions

The concepts in CTX-A to CTX-C are durable. Only the names below are perishable: **treat them as search keywords against current documentation, not guaranteed imports.**

- Harness: `deepagents` 0.7.11 — `create_deep_agent(model, tools, system_prompt, memory=[...], skills=[...], backend, permissions, middleware, checkpointer, response_format)`; `deepagents.backends.FilesystemBackend(root_dir, virtual_mode=True)` (the agent sees `root_dir` as `/`); `FilesystemMiddleware(backend, tools=[...], _permissions=...)`; `FilesystemPermission(operations, paths, mode)` (first match wins; unmatched is allowed); `RubricMiddleware(model, max_iterations, tools, system_prompt, on_evaluation)` (flagged beta; activates only when a `rubric` key is passed in invocation state; passing `system_prompt` *replaces* the library's default grader prompt; terminal state in a private `_rubric_status` value; the grader response type `GraderResponse`); file tools `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`, `delete`; `memory=` ignores a missing file without warning.
- LangChain 1.x: `langchain.agents.middleware.ModelCallLimitMiddleware(run_limit, exit_behavior="end")`; `langchain.tools.tool`; `langgraph.checkpoint.memory.InMemorySaver` (the course attaches one when a rubric is present; its comment says the revision loop works without it); `agent.stream(..., stream_mode="updates")`; message `type` values `ai` / `tool`; message content as a list of blocks on current models, a string on older ones.
- Models: the `openai:` prefix resolves through `langchain-openai`; course ids `gpt-5.4-mini`, `gpt-5.5`; course-era prices (per million tokens, input/output) `gpt-5.5` 5.00/30.00, `gpt-5.4-mini` 0.75/4.50; token estimates via `tiktoken` `o200k_base` with a length/4 fallback.
- **Request-parameter compatibility** `[environment]`: the course passes no sampling parameters (no temperature, no max tokens) to any model; keep it that way — the platform proxy's models are not enumerated here and some families reject non-default parameters, which would surface as a live API error in the first keyed run.
- Hosted tracing: `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` (optional; Not Included).

### CTX-E. Provenance map

Lesson numbering follows the transcripts (the repo's folders are numbered one lower for each notebook, and its README uses a third scheme). Nothing in this spec requires platform access.

| Lesson (transcript) | Title | Contributed |
|---|---|---|
| 1 | Introduction | CTX-A (the four loops, the requirement-review example) |
| 2 | Overview of Loop Engineering | CTX-A, CTX-C3, CTX-C5, CTX-C8, CTX-C9, CTX-C10; slides 2.2–2.13 (all narrated; the deck's "Loop/Level" numbering and the "APPLICATION LOOP" label on the oversight slide are deck wording, not used here) |
| 3 | Deep Agent Primer | CTX-A (filesystem, instructions as files), CTX-C2, CTX-D; slides 3.2–3.5 (narrated); the poet notebook (primer, Not Included) |
| 4 | Agent Loop | CTX-B1, CTX-B2, CTX-B4, CTX-B5, CTX-B6, CTX-C6 (b)(c)(d); slides 4.2–4.5 (narrated); the review notebook and helper module |
| 5 | Verification Loop | CTX-B3, CTX-B7, CTX-C4, CTX-C5, CTX-C6 (a); slides 5.2–5.4 (narrated); the verification notebook and helper module |
| (no transcript lesson) | Event-driven loop — repo code only (a demo web app; Lesson 2 describes the loop; two deck-only Tall-deck slides A.1–A.2 carry a title card and a diagram identical to Lesson 2's) | CTX-B8, CTX-C1, CTX-C7, R11–R15 |
| 6 | Learning loop | CTX-B9, CTX-B10, CTX-B11, CTX-C6 (f), CTX-C8, CTX-C9; slides 6.2 (narrated); the hill-climbing notebook, batch runner and analyst modules |
| 7 | Conclusion | nothing beyond CTX-A's recap |
| Environment (`coding-agent-lab` overlay, not a lesson) | — | Every `[environment]` item: the deliverable shape (§1), §2's container, venv, role and key variables, R20, R23, R24's environment half, §3's relative-URL note, §6's `[environment]` entries, the Runtime (lab) section, the `[environment]` paragraphs in §0, CTX-D's request-parameter entry |

Slides read: Wide deck (13 slides, all placed in Lesson 2; title card deck-only, the rest narrated) and Tall deck (18 slides: five title cards deck-only; 3.2–3.5, 4.2–4.5, 5.2–5.4, 6.2 narrated; A.1–A.2 deck-only, unassigned). No slide-only fact was needed where code or narration spoke; the grader-type line on slide 2.6 and the human-grader line on slide 2.12 are narrated-slide evidence for D3.

---

*Version 1 · Course: Loop Engineering with LangChain DeepAgents · Learner project: the lab's fixed assignment (§1) · Living document: when the building agent produces something unexpected, add the missing constraint here and re-run.*
