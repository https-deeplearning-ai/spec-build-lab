# Spec: Requirements-Review Loop App — Coding-Agent-Lab Build

> **What you're building:** a requirements-review web app whose agent checks its own work and learns across runs. You create a ticket linked to a vague requirement page and watch the agent write a report of facts, ambiguities, questions and assumptions; a grader sends the first draft back once, and the second draft passes. Then you run a five-document batch, read the analyst's one proposed instruction change, approve it, re-run the batch, and see every first attempt pass. Answering the gate's first question with the recommended baseline builds all of it end to end, and the build is COMPLETE when the offline acceptance suite passes; the platform's model key only powers the live criteria (a non-gating pass) and live use of the finished app.
>
> This file is self-contained: the Course Context Pack at the end replaces every external course reference, and nothing here requires access to the course platform.
>
> `(CTX-X)` anchors mark course-derived knowledge. The Decision Ledger below holds every point where this build could still diverge, each pinned to one course-derived default, so the spec builds as-is with no intake; the Environment Resolutions table under it shows which decisions this lab has already answered.
>
> Generated from the *Loop Engineering with LangChain DeepAgents* notebooks + transcripts + slides on 2026-10-20, guide @ `5caba53`, coding-agent-lab overlay @ `efeb69f`.

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
   *[environment] In this lab the structured question tool is a `choices` fence: the explanation goes in prose above it, the fence is the last thing in the message with one option per line, and the turn ends there. Put a line `**Question N of M — <decision>**` before each fence; M counts every question this gate could ask, and a row skipped by its own condition keeps its number in its one-line skip note. A clicked option sends its line verbatim; a typed answer naming an option counts exactly the same.*
3. **Present the Ledger ONE ROW AT A TIME — one question per row.** For each row ask a single
   question: the **Decision** as the prompt, its **Options** as the choices. Append
   "(course default)" to the option the course actually used — on a substitution row that is
   the course-faithful Options entry, not the Ledger Default. Append "(Recommended)" to the
   row's Default — the option the recommended baseline build takes, chosen when this spec was
   written as the most efficient way to build the course's pattern; say once, before presenting
   the first Ledger row, that it does not reflect this person's setup. When the Default IS the course's
   actual choice, merge the labels into "(Recommended - course default)". "(Recommended)" never
   removes or moves the "(course default)" label, and no option is ever
   labeled with a bare "(default)" — these two labels and their merged form are the only
   option labels. Use the answers already given (project, data, goal, …) to frame
   later questions and describe options in the person's own terms — but never drop or alter an
   Option or move the "(course default)" label because of an earlier answer, and never skip a row
   because an earlier answer seems to make it irrelevant. The only skip: a row whose Decision
   says "Applies only when `<row>` is `<id>`" is skipped when the answer on that row is none of
   those ids, or that row was itself skipped. Say so in one line (e.g. "<row> is skipped: it applies
   only when <row> is <id>; <row> = <answer>") and go on to the next row — a skip resolves that row
   only. If the person changes an earlier answer, re-check every condition that names it. Put
   any realizations beyond the tool's option slots (or the free-form case) under the tool's
   "Other"/free-text. Ask about every row that is not skipped this way. A per-call item limit is NEVER a reason to drop,
   skip, merge, or silently default a row — make as many separate calls as there are rows.
   *[environment] Only the latest message's buttons stay live. If the person wants to change an earlier answer, ask that row again as a new question; never ask them to go back to an earlier message.*
4. **Presenting any of these questions ENDS YOUR TURN — stop here; write no code, create or edit
   no file, take no other build action.** Keep asking, one row at a time, until **every** row is
   resolved — answered (a chosen option, an explicit "use the course default", or the step-2
   baseline answer, which answers every row at once) or skipped by its own condition (step 3). Answers to *some* rows do NOT release the build; "no reply
   yet" is not an answer — wait for the user.
5. **Before the first line of code, print a resolved-decision checklist and write it to
   `resolved-decisions.md`** — every Ledger row with its final value (the chosen option's id and
   text — the user's choice, or its Ledger default), each line carrying a deviation mark: `= course choice`, or
   `≠ course choice (course used: <option>)`, or `no course choice` on a row where the course
   made no choice (the scope boundary), or — on a row skipped by its condition, with no value —
   `not applicable (applies only when <row> is <id>; <row> = <answer>)`. If the build calls a language model, add one line per
   model role the chosen options use, naming the current model you will use from the Default
   provider — one you know that provider serves; if you cannot tell, say so and ask the person
   to name one, and if they do not, use the course's own model id from this spec for that role
   and say it may need changing. A missing model name never blocks confirming the checklist.
   For every chosen option that is not its row's Default, copy its line from §7's "Tests by
   option" table into the checklist, so the criteria and Ledger cells this build retires or
   changes are recorded before the first line of code. The file records what this build was built from;
   nothing reads it back — a later build re-runs this gate. If the baseline path was chosen,
   walk the person through every `≠` row — the course's actual choice, and why this build's
   default substitutes it (the row's Trade-off/branch note says why) — before building. Begin
   implementation ONLY after this checklist is shown, written, and confirmed by the person; if
   any row is unresolved you are not done — return to step 3. A `not applicable` line whose
   quoted condition is not false is unresolved. Build on the checklist's values. Leave out
   every part of this spec that exists only for a rule a chosen option retires — its commands,
   flags, settings, schema fields, fixtures and permission items. Where a chosen option changes
   a criterion and its §7 line does not fully state the new form, adapt the criterion to the
   chosen options and list it, with what you changed, under *Adapted* in the checklist and in
   your final report.

## Decision Ledger (§0 above requires the build agent to present these before building)

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L1 | learner | **Scope boundary.** Present the §1 "Not Included" list inside this question — every item with its handling tag — and ask whether to keep every exclusion or bring one back. | | **L1a** — keep every exclusion; the full acceptance set is built. | L1a — Keep every exclusion and build the full acceptance set (Recommended) · L1b — Bring one excluded item back (name it; it is handled by its tag: `restorable` items are built, `buildable, no criteria` items are built with no parameters or criteria from this spec, `unavailable` items cannot be brought back in this lab) | Restoring an item adds scope that the acceptance suite does not cover. The course made no choice on this row. | learner |
| D1 | design-argued | **Trigger surface** — what starts a review run. | A run starts without anyone copying the requirement into the agent: the agent is told only the document's id and fetches the text itself, and a run started by a change analyzes the requirement's latest version. | **D1a** — the course's example realization of the trigger surface (a simulated tracker standing in for a real one); outside the lab, expect to swap it for your real tracker through the §1 seam. Branch: the course's own shipped realization, already keyless — kept as is. | D1a — A simulated ticket tracker inside the app: creating a ticket linked to a requirement page, or saving a new version of a page that an open ticket links to, starts a run; an open ticket also has a "re-run now" control (Recommended - course default) · D1b — Manual runs only: a page control starts a review of a chosen document, and nothing starts a run on its own (shown working in the course's Agent Loop, Verification Loop and Learning loop notebooks) | Lesson 6 argues for events: "If you have to open a separate agent, copy the requirement, paste it, and ask for a review, that's several extra steps. Even if the review is useful, you might not do it every time." Manual runs are shown producing correct reports (Lessons 4, 5, 7) and the course attributes no failure to them, only friction. Litmus: working (the alternative is shown working) → row. The course also showed the agent in real Slack, Jira and Confluence (screen recordings, no code shipped); those need service credentials this lab does not supply, so they are not offered here — see §1 Not Included. | course+learner |
| D2 | design-argued | **Instruction placement** — where the review agent's procedure and review guidance live, and when they load. | The instructions reach the agent's context at the start of every run, every version is kept outside the agent, and the agent cannot change them during a run. | **D2a**. Branch: the course's own realization, keyless. | D2a — One instruction file in the agent's own filesystem, loaded whole into its context at the start of every run (Recommended - course default) · D2b — The procedure stays in the instruction file; each section's review guidance becomes a skill whose one-line description loads up front and whose body the agent reads only when it reaches that section (shown working in the course's Deep Agent Primer on a poet agent; never built for the review agent) · D2c — The instructions are written into the system prompt fixed when the agent is created, with no instruction file in the agent's filesystem (shown in the course's base-agent example) | Lesson 3 argues the three placements: the system prompt "you specify when the agent is created, and you use that every time"; the always-loaded file "is loaded each time the agent's called, and you can modify it over time", and "costs context on every call, so it should stay short"; skills "work with progressive disclosure", so "twenty skills cost twenty lines of context, not twenty documents". Litmus: working — all three are shown working in Lesson 3 → row. The choice moves what an approved learning-loop change edits. | course+learner |
| D3 | design-argued | **Verification stage** — whether and how a finished report is graded before the run ends. | When a grader is present it judges the written report file (never the conversation) against the run's rubric, each criterion pass or fail; the run is done only when every criterion passes in one grading pass; a failing pass sends specific feedback back for another attempt within a bounded budget. | **D3a**. Branch: the course's own realization. | D3a — A model grader reads the report file, grades each rubric criterion pass or fail with quoted evidence, and sends the failing criteria back with their gaps, up to the revision budget (Recommended - course default) · D3b — A deterministic grader: code checks each criterion against the report file (shown in the course only as a narrated example on a different agent — links resolve, CI passes; never built for this agent, and the spec supplies no parameters and no acceptance criteria for it) · D3c — No grader: the run ends when the agent says it is done (the course's Agent Loop lesson, shown working) | Lesson 5: "just because the agent says it is done, is the analysis actually good enough? In the agent loop, nothing is checking for this", and "If you set this to 0, you will have the same basic agent loop you built in the last lesson." Lesson 2: "You don't need the verification loop per se", and verification "can make cheaper models viable for harder tasks". Litmus: a budget of 0 removes the grader — a component choice, not a knob — and the course shows the system working without it (Lesson 4) → row; the budget number itself stays a lever. Grader kind (model or code) is merged here as one subject: it moves the verdict's owner. The course also named a human acting as the grader (Lesson 2); here the offline suite would wait on a person, so it is not offered — see §1. | course+learner |
| D4 | design-argued | **Learning loop** — whether runs over many documents improve the agent's instructions. Applies only when `D3` is `D3a` or `D3b` | An improvement is drawn only from a failure that recurs across most runs of one batch, is proposed by an analyst that cannot alter the evidence it reads, is applied in plain code only after a human approves it, and is judged by re-running the same batch and comparing. | **D4a**. Branch: the course's own realization. | D4a — A batch learning loop: review a batch of documents under one instruction version, let an analyst propose one instruction change from the recurring first-attempt failures, apply it on human approval, re-run the batch and compare the two (Recommended - course default) · D4b — No learning loop: each run is corrected only by its own grading passes (shown working in the course's Event-Driven Loop lesson, whose app has no learning loop) | Lesson 7: "if we give that same agent a brand new document tomorrow, the agent will start from the same place, and if it makes the same mistake, it will correct it all over again." Lesson 2: "You don't necessarily have to do that for all four loops." Litmus: working — the event-driven app is shown working without it, and the course names a repeated correction cost, not a failure → row. | course+learner |

## Environment Resolutions (coding-agent-lab)

This spec targets the coding-agent-lab environment; the six learner-context dimensions below were derived from the course first and then resolved against the lab's facts — none was skipped. Two course-owned decisions also left the Ledger because every alternative to their default is unavailable here; they are listed last.

| Dimension | Resolution | Where the Invariant lives now |
|---|---|---|
| project | **ANSWERED** — the lab fixes the assignment: the course's requirements-review app. Invariant empty. | §1 Objective |
| data/inputs | **ANSWERED** — inputs are seeded into the workspace as the §5 fixture corpus. Invariant: documents are plain text fetched by id at run time (the agent is never handed the text), and a learning batch holds several distinct documents (course: five). | §5 fixture corpus; R1 (AC2), R20 (AC23) |
| goal | **ANSWERED** — the lab fixes what "working" means: the course's three-criterion rubric. Invariant: every criterion is pass/fail and decidable from the report file alone; done means all pass in one grading pass. | §1 + R10, R11 (AC12, AC14) |
| model/provider | **CONSTRAINED** — the built app needs an LLM: platform models only, through the ambient OpenAI-compatible key and base URL; never asked of the learner. Invariant: each model role supports native tool calling and structured output. The course's model-tiering argument stays as a body lever with an Ask-First entry. | §2 + R27 (AC35, AC36, AC44) + CTX-D |
| environment | **ANSWERED** — the lab container. Invariant (capability): tickets, pages, runs, instruction versions and batches survive a process restart. | §2 + `## Runtime (lab)`; R32 (AC41) |
| scope-boundary | **KEPT** | Ledger row L1 |
| acceptance-suite model (which model the offline suite runs against) | **ANSWERED — every alternative unavailable here.** The live model as the suite's model would make completion depend on a live model's output. Pinned: a scripted stand-in model drives the real pipeline end to end. Because the lab supplies the key, the `live` criteria still run after the offline suite, as a pass that never gates completion. Invariant: the offline suite exercises every stage the pattern wires around the model. | §2 pin + §5 scripted model + §7; R28 (AC37) |
| hosted trace viewer | **ANSWERED — every alternative unavailable here.** The course's optional hosted tracing needs its own account and key, which this lab does not supply. Pinned: local trace records only (the course's own default). Invariant: every run leaves a local record of every model turn and tool result. | §2 pin; R34 (AC43) |

## 1. Objective

Build a requirements-review web app — one server on port 4000 serving one page and its JSON API — in which creating or updating a requirement ticket starts a review agent that fetches the requirement and writes a structured analysis file, a grader sends the analysis back with specific feedback until a three-criterion rubric passes, and a learning loop turns failures that recur across a batch of documents into one human-approved instruction change, guaranteeing that every report, verdict and instruction change is stored with the evidence that produced it. (pattern: CTX-A)

The deliverable's shape is `[environment]`: the lab's preview pane shows only one server on port 4000, so the course's own artifacts — notebooks, and a separate tracker app on another port — are never the deliverable; this app embodies their pattern.

**Adapting this beyond the lab.** Each lab-resolved dimension now lives in a named place: the project in this Objective; the data in the §5 fixture corpus (swap in your own documents behind the same fetch-by-id contract); the goal in R10's rubric; the model/provider in §2 and R27 (outside the lab, read your own provider's key and base URL — the scripted model and offline suite stay); the environment in §2 and `## Runtime (lab)` (port 4000, relative URLs and the venv rule are lab facts, not course facts). The two pinned decisions reopen outside the lab: the live model as an acceptance-suite option, and hosted tracing as a keyed option.

### Not Included ★

Each item carries its handling tag for the L1 question.

1. **Real Jira and Confluence integration** (webhooks into the app, REST lookups of tickets and pages) — `unavailable` `[environment]`: needs an Atlassian Cloud site, an API token and automation rules, which this lab does not supply. Seam: the single "run review for ticket" function — swap the store's ticket and page lookups for the services' APIs and call it from a webhook; nothing about the agent or the loops changes.
2. **A Slack bot that runs a review from a message** — `unavailable` `[environment]`: needs a Slack workspace app and its two tokens. Seam: the same "run review" function, called from a chat event handler that replies with the formatted report and its raw Markdown.
3. **A human acting as the grader** — `unavailable` `[environment]`: the offline suite would wait on a person. Seam: the grader slot of the verification loop — anything returning the same per-criterion verdict shape can fill it.
4. **The live model as the acceptance suite's model** — `unavailable` `[environment]`: completion would depend on a live model's output. Seam: the `LLM_BACKEND` switch; the `live` criteria already run as a non-gating pass.
5. **Hosted trace viewer (sending traces to a tracing service)** — `unavailable` `[environment]`: needs an account and key this lab does not supply. Seam: the tracing service's environment variables; local trace records are unaffected.
6. **Scheduled triggers** (a review that runs on a timer) — `buildable, no criteria`: named by the course (Lesson 2), never built; the spec supplies no parameters and no acceptance criteria.
7. **Memory consolidation in the learning loop** (persisting per-user preferences across runs) — `buildable, no criteria`: named by the course (Lesson 2), never built; the spec supplies no parameters and no acceptance criteria.
8. **Subagents, a code-execution sandbox, and other harness features the framework offers but this agent does not use** — `buildable, no criteria`: named in Lesson 3, never used by the review agent; the spec supplies no parameters and no acceptance criteria.
9. **Automatic application of a proposed change that targets tools, the grader or configuration** — `buildable, no criteria`: the course's change format names these targets but applies only instruction changes in code; others are read and decided by a person.
10. **Dollar-cost estimates in the batch comparison** — `restorable`: the course priced its two models; prices are perishable (CTX-D).
11. **A before/after chart of pass rates** — `restorable`: the course drew one; this spec shows the same numbers as a table.
12. **User accounts and sign-in** — `restorable`: past the course's scope; authors and assignees come from a fixed cast.
13. **Grafting this pattern into an existing codebase** — `unavailable`: outside the delivered build mode.

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python 3 in a venv created with `--system-site-packages` | `[environment]` The container's Python minor version is not fixed. Run `python3 --version` first, record it in `resolved-decisions.md`, and stop with a report if a course-pinned package below refuses the interpreter. The course itself required Python ≥3.12 (its README: older versions fail building its numerical packages). |
| Agent harness | `deepagents==0.7.11` | **Install/pin situation, stated honestly:** the course's `pyproject.toml` sets floors (`>=`) and its `uv.lock` pins exact resolved versions; every pin in this table is the lock's version. Where a preinstalled copy differs (`openai`, `python-dotenv`), **the course pin wins inside the venv** `[environment]`. Era-specific class and argument names are perishable — see CTX-D. |
| Framework packages | `langchain==1.3.18`, `langchain-core==1.6.1`, `langchain-openai==1.6.0`, `langgraph==1.2.11`, `pydantic==2.13.5` | Course lock pins. |
| Model SDK / env loader | `openai==3.6.0`, `python-dotenv==1.2.3` | Course lock pins; override the preinstalled copies inside the venv. |
| Web server | Flask, current 3.x | The course's own web layer; its floor `flask>=3.1.3` is unpinned and absent from its lock, so take the current release. Not preinstalled — install it with the rest. |
| Storage | Flat JSON files under the app's data directory (`APP_DATA_DIR`, default `data/`) | The course's choice (three JSON lists for pages, tickets, runs); standard library only. Runs, batches and proposals sit beside them. Instruction versions are the one exception: each is a file `v<n>.md` in the app folder's `harness/instructions/` (R33), the single place the app reads and writes them. |
| Test runner | `pytest`, current | Project hardening (the course shipped no test suite). Mark live criteria with a `live` marker. |
| Model provider | The platform's OpenAI-compatible proxy | `[environment]` CONSTRAINED (Environment Resolutions). The app reads exactly `OPENAI_API_KEY` and `OPENAI_BASE_URL` (the course's provider is OpenAI). `ANTHROPIC_API_KEY` and `ANTHROPIC_BASE_URL` are also present in the container and are never read. Never hardcode a key, never ask the learner for one. |
| Model roles | `REVIEW_AGENT_MODEL`, `GRADER_MODEL` (defaults to `REVIEW_AGENT_MODEL` when unset), `ANALYST_MODEL` | `[environment]` One variable per role, provider-prefixed ids (`openai:<model>`). The build agent sets them when it writes the step-5 checklist, one current platform model per role that supports native tool calling and structured output (R27). The course's own ids are provenance only (CTX-D); no claim is made that the proxy serves them. Course tiering, kept as a lever: review agent and grader on a cheaper tier, analyst on a stronger one (§6 Ask First). |
| Model backend switch | `LLM_BACKEND` = `live` (default when serving) or `scripted` | `scripted` selects the §5 scripted stand-in model for every role; the offline suite always runs with `scripted`. |
| Acceptance-suite model | Scripted stand-in (§5) — pinned | `[environment]` Environment Resolutions: every alternative unavailable here. |
| Tracing | Local trace records in each run record — pinned | `[environment]` Environment Resolutions: hosted tracing unavailable here. The course's default was also off (`LANGSMITH_TRACING=false` in its example env file). |
| Fetch-failure injection | `FETCH_SIMULATED_FAILURES`, default `0` | Test knob for R2 (a contradicted lever, see R2). |
| Not installed | `pandas`, `matplotlib`, `seaborn`, `numpy`, `jupyter`, `ipykernel`, `mistune`, `tiktoken`, `langsmith` | Declared drop: the course used them only to render notebooks, draw charts and price tokens. Token estimates use the course's own fallback (characters ÷ 4). |

**Install cost** `[environment]`: everything above beyond the preinstalled set (`deepagents`, the LangChain packages, Flask, pytest, and the pinned `openai`/`python-dotenv`) installs from the network. Batch it into one install command early in the build and tell the learner it will take a few minutes.

**Secrets**: read from the environment only; never written to a file, a log, a run record or the page.

## 3. Input/Output Contracts ★

All endpoints are relative to the app root (R30). Bodies are JSON unless noted. A run started by an endpoint is asynchronous: the endpoint returns at once, and the run record moves from `running` to `complete` or `error`.

| Method and path | Body | Returns |
|---|---|---|
| `GET ./` | — | the page (HTML) |
| `GET api/config` | — | `{llm_backend, roles: {review_agent, grader, analyst}, base_url}` (never a key) |
| `GET api/tickets` · `GET api/tickets/<key>` | — | `Ticket[]` · `Ticket` plus its `RunRecord[]` |
| `POST api/tickets` | `{title, description, linked_page_id, assignee}` | `201 Ticket` with `last_run_id` of the started run; `400` if the page does not exist or is not a requirement page |
| `POST api/tickets/<key>/rerun` | — | `202 {run_id}`; `409` if the ticket is `Done` |
| `POST api/tickets/<key>/done` | — | `200 Ticket` with `status: "Done"` |
| `GET api/pages` · `GET api/pages/<id>?v=<n>` | — | `Page[]` · one `Page` (all versions; `v` selects the body shown) |
| `POST api/pages` | `{title, body, author}` | `201 Page` (kind `requirement`, version 1) |
| `POST api/pages/<id>/versions` | `{body, author}` | `201 {version, retriggered: [ticket keys]}`; `400` for an `analysis_report` page |
| `GET api/pages/<id>/compare?a=<n>&b=<n>` | — | `{diff: [unified-diff lines], run_a: RunRecord or null, run_b: RunRecord or null}` |
| `GET api/runs/<run_id>` | — | `RunRecord` |
| `GET api/instructions` · `GET api/instructions/<n>` | — | versions list · `{version, text, created_at, source}` |
| `GET api/batches` · `GET api/batches/documents` | — | batch labels · the batch document names |
| `GET api/proposals` | — | `Proposal[]` |
| `POST api/batches` | — | `202 {label}`; runs every batch document under the current instruction version; label is `v<version>` |
| `GET api/batches/<label>` | — | `{summary: BatchSummary, runs: BatchRunRecord[]}` |
| `POST api/batches/<label>/analyze` | — | `201 Proposal` (status `pending`) |
| `POST api/proposals/<id>/approve` · `.../reject` | — | `{proposal: Proposal, instruction_version}` |
| `GET api/compare?before=<label>&after=<label>` | — | `Comparison` |

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$defs": {
    "Ticket": {
      "type": "object",
      "required": ["key", "title", "description", "linked_page_id", "assignee", "status", "comments", "created_at", "last_analyzed_version", "last_run_id"],
      "properties": {
        "key": {"type": "string", "pattern": "^REQ-[0-9]+$"},
        "status": {"enum": ["Open", "Analysis Ready", "Done"]},
        "linked_page_id": {"type": "string", "pattern": "^page-[a-z0-9-]+$"},
        "assignee": {"type": "string"},
        "comments": {"type": "array", "items": {"type": "object", "required": ["author", "text", "timestamp"]}},
        "last_analyzed_version": {"type": ["integer", "null"], "minimum": 1},
        "last_run_id": {"type": ["string", "null"], "pattern": "^[0-9a-f]{8}$"}
      }
    },
    "Page": {
      "type": "object",
      "required": ["id", "kind", "title", "linked_ticket", "versions"],
      "properties": {
        "id": {"type": "string", "pattern": "^page-[a-z0-9-]+$"},
        "kind": {"enum": ["requirement", "analysis_report"]},
        "linked_ticket": {"type": ["string", "null"]},
        "versions": {"type": "array", "items": {"type": "object", "required": ["n", "author", "timestamp", "body"],
          "properties": {"n": {"type": "integer", "minimum": 1}}}}
      },
      "if": {"properties": {"kind": {"const": "analysis_report"}}},
      "then": {"properties": {"id": {"pattern": "^page-analysis-req-[0-9]+$"}, "linked_ticket": {"type": "string", "pattern": "^REQ-[0-9]+$"}}}
    },
    "TraceStep": {
      "type": "object", "required": ["step", "actor", "action", "detail"],
      "properties": {"actor": {"enum": ["Model reasoning", "Tool", "Harness"]}, "detail": {"type": "string", "maxLength": 221}}
    },
    "Criterion": {
      "type": "object", "required": ["name", "passed"],
      "properties": {"name": {"type": "string"}, "passed": {"type": "boolean"}, "gap": {"type": "string", "minLength": 1}},
      "if": {"properties": {"passed": {"const": false}}}, "then": {"required": ["gap"]}
    },
    "GradingPass": {
      "type": "object", "required": ["iteration", "result", "explanation", "criteria", "analysis_markdown"],
      "properties": {
        "result": {"enum": ["satisfied", "needs_revision", "failed", "grader_error"]},
        "criteria": {"type": "array", "items": {"$ref": "#/$defs/Criterion"}},
        "analysis_markdown": {"type": "string", "description": "the report file exactly as this pass saw it"}
      },
      "allOf": [
        {"if": {"properties": {"result": {"enum": ["satisfied", "needs_revision"]}}}, "then": {"properties": {"criteria": {"minItems": 3, "maxItems": 3}}}},
        {"if": {"properties": {"result": {"const": "satisfied"}}}, "then": {"properties": {"criteria": {"items": {"properties": {"passed": {"const": true}}}}}}},
        {"if": {"properties": {"result": {"const": "grader_error"}}}, "then": {"properties": {"criteria": {"maxItems": 0}}}}
      ]
    },
    "SectionCounts": {
      "type": "object", "additionalProperties": false,
      "required": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions"],
      "properties": {"Confirmed Facts": {"type": "integer"}, "Ambiguities": {"type": "integer"}, "Clarification Questions": {"type": "integer"}, "Assumptions": {"type": "integer"}}
    },
    "RunRecord": {
      "type": "object",
      "required": ["id", "state", "ticket_key", "requirement_page_id", "requirement_version", "report_page_id", "report_version", "workspace_id", "instruction_version", "verification_status", "stop_reason", "turns", "counts", "summary_words", "stage_order", "in_order", "trace", "grading", "analysis_markdown", "timestamp"],
      "properties": {
        "id": {"type": "string", "pattern": "^[0-9a-f]{8}$"},
        "workspace_id": {"type": "string", "pattern": "^[0-9a-f]{8}$"},
        "state": {"enum": ["running", "complete", "error"]},
        "error": {"type": "string"},
        "verification_status": {"enum": ["satisfied", "max_iterations_reached", "failed", "grader_error", null]},
        "stop_reason": {"enum": ["finished", "turn_limit", null]},
        "counts": {"$ref": "#/$defs/SectionCounts"},
        "stage_order": {"type": "array", "items": {"enum": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"]}},
        "trace": {"type": "array", "items": {"$ref": "#/$defs/TraceStep"}},
        "grading": {"type": "array", "maxItems": 4, "items": {"$ref": "#/$defs/GradingPass"}}
      },
      "allOf": [
        {"if": {"properties": {"state": {"const": "error"}}}, "then": {"required": ["error"]}},
        {"if": {"properties": {"verification_status": {"const": "max_iterations_reached"}}}, "then": {"properties": {"grading": {"minItems": 4}}}}
      ]
    },
    "BatchRunRecord": {
      "type": "object",
      "required": ["run_id", "doc_name", "label", "model", "requirement_doc", "instructions", "messages", "grading", "analysis_markdown", "status", "started_at", "stage_order"],
      "properties": {
        "run_id": {"type": "integer", "minimum": 1},
        "messages": {"type": "array", "items": {"type": "object", "required": ["type", "content", "tool_calls", "tool_call_id", "status"]}},
        "grading": {"type": "array", "items": {"$ref": "#/$defs/GradingPass"}},
        "status": {"enum": ["satisfied", "max_iterations_reached", "failed", "grader_error"], "description": "the run's verification status, derived from its passes as R13 derives verification_status"}
      }
    },
    "CriterionRate": {
      "type": "object", "required": ["passed", "total", "pass_rate"],
      "properties": {"passed": {"type": "integer"}, "total": {"type": "integer"}, "pass_rate": {"type": ["number", "null"]}}
    },
    "BatchSummary": {
      "type": "object",
      "required": ["label", "model", "runs", "graded", "grader_errors", "first_attempt", "revisions_needed", "documents"],
      "properties": {
        "first_attempt": {"type": "object", "additionalProperties": false, "required": ["completeness", "clarity", "depth"],
          "properties": {"completeness": {"$ref": "#/$defs/CriterionRate"}, "clarity": {"$ref": "#/$defs/CriterionRate"}, "depth": {"$ref": "#/$defs/CriterionRate"}}},
        "revisions_needed": {"type": "integer", "minimum": 0}
      }
    },
    "HarnessChange": {
      "type": "object", "required": ["target", "issue", "recurrence", "evidence", "section", "change", "rejected"],
      "properties": {
        "target": {"enum": ["prompt", "tool", "grader", "configuration"]},
        "evidence": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "section": {"type": "string"},
        "change": {"type": "string", "minLength": 1, "description": "literal text to insert, not a description of it"},
        "rejected": {"type": "array", "items": {"type": "string"}}
      },
      "if": {"properties": {"target": {"const": "prompt"}}}, "then": {"properties": {"section": {"pattern": "^#+ \\S"}}}
    },
    "Proposal": {
      "type": "object", "required": ["id", "label", "status", "change", "proposal_markdown"],
      "properties": {
        "id": {"type": "string", "pattern": "^[0-9a-f]{8}$"},
        "status": {"enum": ["pending", "approved", "rejected"]},
        "change": {"$ref": "#/$defs/HarnessChange"}
      }
    },
    "Comparison": {
      "type": "object",
      "required": ["verdict", "criteria", "runs", "revisions_needed", "attempts", "input_tokens", "output_tokens", "improved", "regressed"],
      "properties": {
        "verdict": {"enum": ["regression", "success", "partial", "no effect"]},
        "criteria": {"type": "object", "additionalProperties": {"type": "array", "items": {"type": "integer"}, "minItems": 2, "maxItems": 2}},
        "revisions_needed": {"type": "array", "minItems": 2, "maxItems": 2},
        "attempts": {"type": "array", "minItems": 2, "maxItems": 2},
        "improved": {"type": "array", "items": {"type": "string"}},
        "regressed": {"type": "array", "items": {"type": "string"}}
      },
      "if": {"properties": {"regressed": {"minItems": 1}}}, "then": {"properties": {"verdict": {"const": "regression"}}}
    }
  }
}
```

**The report file contract** (the agent's deliverable, `/analysis.md` in its workspace): exactly these headings in this order — `# Requirements Analysis`, `## Confirmed Facts`, `## Ambiguities`, `## Clarification Questions`, `## Assumptions`, `## Summary`. List sections hold `- ` bullets; each Ambiguities bullet is `- **"<the exact clause>"**` followed by an indented `Reason:` line (and, once the instructions ask for them, indented `Resolved by:` and `Edge case:` lines). Section counts count `- `/`* ` bullet lines per list section; the Summary is counted in words.

## 4. Business Rules

Labels: *course-demonstrated* `(CTX-…)`; *project hardening*; `[environment]` (from the lab, never the course). Rubric budget, caps and failure counts cite their exact source.

**Agent loop**

- **R1** — The review agent is never handed the requirement text. Its opening message names only the document's id ("The requirement document is tracked as ticket `<id>`. Fetch it to begin."), and it must call `fetch_requirement(ticket_id)` to get the text, which resolves to the line `REQUIREMENT: <page title>` followed by the linked page's latest version body (event runs), or to the batch document file of that id (batch runs). An unknown id returns an error text, not an exception. *Course-demonstrated* (CTX-A). → AC2
- **R2** — `fetch_requirement` can fail transiently; when a tool returns an error text the agent calls the same tool again with the same arguments, and the run still completes. Failure injection is a counter per run (`FETCH_SIMULATED_FAILURES`), returning these texts in turn: `Error fetching requirement: 503 Service Unavailable. Please retry.` then `Error fetching requirement: request timed out after 10s. Please retry.` Default `0`. Contradicted lever: the course's helper default is 0 ("a clean fetch"), its Lesson 4 notebook table and narration say two failures, and its batch module uses 0; value chosen by narration for the demonstration (2, set by the fixture in AC3) and by the end-to-end config for normal runs (0) — post-build lever. *Course-demonstrated* (CTX-B1). → AC3
- **R3** — The analysis is one file, `/analysis.md`, built in stages, one tool call per turn: one `write_file` laying down the exact skeleton (§3) with Confirmed Facts filled, then one `edit_file` each for Ambiguities, Clarification Questions, Assumptions, Summary; then a one-sentence completion reply with no tool call. Stage order is requested by the instructions, not enforced by the harness: each run records `stage_order` (sections filled by successful write/edit calls during the first attempt) and `in_order`; a failed edit does not count. *Course-demonstrated* (CTX-A, CTX-C). → AC4, AC5
- **R4** — Section content: Confirmed Facts record only what the document states; each Ambiguities bullet quotes the exact clause and gives a `Reason:`; one bullet per clarification question and per assumption; the Summary is two or three sentences. Counts and summary words are computed from the file (§3). *Course-demonstrated* (CTX-A). → AC5, AC6
- **R5** — The agent never modifies the requirement; the requirement page is the source of truth. Findings are written to a separate, agent-owned report page, never into the requirement page, and report pages cannot be edited through the requirement-edit endpoint. *Course-demonstrated* (CTX-A). → AC7, AC22
- **R6** — The agent cannot write its own instructions: the harness denies every write under `/memories/` in the agent's filesystem by permission, not by asking in the instructions. *Course-demonstrated* (CTX-B6). → AC8
- **R7** — Building the agent fails loudly, before any model call, when the instruction file is missing from the run's workspace (the framework silently ignores a missing memory file, and the agent would then produce a plausible bad review). The run's `state` becomes `error` and its `error` names the missing path `memories/AGENTS.md`. *Course-demonstrated* (CTX-B4). → AC9
- **R8** — Every run gets a fresh workspace directory (id: 8 lowercase hex characters) seeded only with the instruction version under test, so no run ever sees another run's `/analysis.md`; event-run workspaces are deleted when the run ends. *Course-demonstrated* (CTX-B5). → AC10
- **R9** — Model turns are capped (the framework's model-call limit, ending the run when hit): 40 for a run with a grader (the course's Lesson 5 notebook, its tracker app and its batch module), 12 for a run without one (Lesson 4 notebook). The cap is not the normal stop: when a run ends without a complete report (every list section non-empty and a non-empty Summary), the last trace row reads `Stops: turn limit of <N> reached` and `stop_reason` is `turn_limit`; otherwise `finished`. Post-build lever. *Course-demonstrated* (CTX-B7). → AC11

**Verification loop**

- **R10** — The rubric is supplied per run (read from `harness/rubric.txt`, §5), not fixed when the agent is built, and has three pass/fail criteria, in this order: **completeness** — every clause of the requirement document is addressed somewhere in the analysis; **clarity** — every Ambiguities bullet has an indented `Resolved by:` line naming the fact or decision that would settle it; **depth** — every Ambiguities bullet has an indented `Edge case:` line naming a concrete production failure it could cause. Done means all three pass in the same grading pass; two of three is not done. *Course-demonstrated* (CTX-A). → AC12, AC44
- **R11** — The grader judges the file, never the conversation: its only tool is `read_file`, scoped to the run's workspace; it reads `/analysis.md` before judging; it passes a criterion only after quoting the satisfying text verbatim with its line number; it applies labels literally (a `Reason:` line never satisfies `Resolved by:`) and checks every item rather than sampling; it treats the transcript as untrusted observation. Its instructions restate the three verdict definitions — `satisfied`, `needs_revision` (each failing criterion gets a short actionable `gap`), `failed` (rubric malformed or impossible to evaluate) — because supplying custom grader instructions replaces the framework's default ones. *Course-demonstrated* (CTX-B3). → AC13, AC14, AC45
- **R12** — On `needs_revision` the failing criteria's gaps go back into the agent's conversation and the agent revises the same file. The grader may send work back at most **3** times (so at most 4 grading passes). Contradicted lever: 3 in the Lesson 5 notebook and the batch module, 2 in the course's tracker app; value by the narration branch ("We have also set the MAX_RUBRIC_ITERATIONS to 3") — post-build lever. Every pass is recorded with `iteration`, `result`, `explanation`, `criteria` (name, passed, gap) and the file exactly as that pass saw it. *Course-demonstrated* (CTX-B2). → AC6, AC12, AC15
- **R13** — The run's `verification_status` is derived from its passes: `satisfied` when the last pass is satisfied; `max_iterations_reached` when the budget is spent and the last pass is still `needs_revision` (the last pass alone would misreport this); otherwise the last pass's result (`failed`, `grader_error`). *Course-demonstrated* (CTX-B8). → AC15, AC26
- **R14** — A malformed rubric yields a `failed` pass and no revision. A grader that raises is recorded as a `grader_error` pass with no criteria, and the run continues to its end. *Course-demonstrated* (CTX-B11). → AC16, AC26

**Event-driven loop** (applies under D1a)

- **R15** — Triggers: creating a ticket linked to a requirement page starts a run; saving a new version of a requirement page starts a run for every ticket linked to it whose status is not `Done`; "re-run now" on a ticket that is not `Done` starts a run. A `Done` ticket is never re-triggered. Every run analyzes the page's latest version. *Course-demonstrated* (CTX-A). → AC17, AC18, AC19
- **R16** — Write-back: each run adds a new version, authored `Requirements Analysis Agent (bot)`, to the ticket's report page (created on its first run: id `page-analysis-<ticket key lowercased>`, title `Analysis Report — <key>`), whose body is a banner — `> Generated automatically from <key> on <timestamp>.`, `> Source requirement: version <n>.`, `> Verification status: **<status>** after <k> grading pass(es).` — followed by the report file. The ticket then gets `status: "Analysis Ready"`, `last_analyzed_version`, `last_run_id`, and a bot comment `Analysis complete (<status>), requirement version <n>. See Analysis Report — <key>.` Timestamps use `YYYY-MM-DD HH:MM UTC`. *Course-demonstrated* (CTX-A). → AC17, AC18
- **R17** — Only a person marks a ticket `Done` (the done endpoint); no run ever sets `Done`, and the agent never closes its own work. *Course-demonstrated* (CTX-C). → AC19, AC20
- **R18** — Every run is stored. A ticket's view shows the latest run (status, turns, each grading pass's criterion/result/gap table, the trace) and, once it has two runs, a "what changed since the previous run" table — requirement version analyzed, verification status, and bullet counts for the four list sections — together with a link to the full unified diff of the two report versions. Both are shown because counts can stay identical while the content changes completely. *Course-demonstrated* (CTX-B13). → AC21
- **R19** — Pages are versioned; any two versions of a page can be compared as a unified diff, and for report pages the comparison also returns the two runs behind those versions. New requirement page ids are `page-` plus the title lowercased with every non-alphanumeric run turned into one `-`, trimmed, and suffixed `-2`, `-3`, … on collision. New ticket keys are `REQ-` plus one more than the highest existing number (100 when none). Authors and assignees are chosen from a fixed cast: `Avery (Product Manager)`, `Blake (Eng Lead)`, `Casey (QA Lead)`, `Drew (Backend Engineer)`, `Emery (Frontend Engineer)`. *Course-demonstrated* (CTX-A); names are the generator's own. → AC17, AC21, AC22

**Learning loop** (applies under D4a)

- **R20** — A batch reviews every batch document once under one instruction version, each run in its own fresh workspace seeded from that version, with the verification loop on and fetch-failure injection off; the batch folder keeps a snapshot of the instructions it ran with. Each run record keeps the whole conversation untruncated (every message, full tool-call arguments, the grader feedback injected after a failed pass), every grading pass, the final file, the instructions snapshot, the status and the stage order. The batch summary gives, per criterion, first-attempt passes, total and pass rate (3 decimals), plus `revisions_needed` (graded runs whose first pass failed anything). Criteria are identified by their **position** in the rubric, never by the name the grader echoes back (the grader paraphrases names run to run). *Course-demonstrated* (CTX-B9, CTX-B10). → AC23, AC24, AC25
- **R21** — A run whose first pass carries no criteria (a `grader_error`) is excluded from every rate and counted in `grader_errors`; denominators are graded runs. *Course-demonstrated* (CTX-B11). → AC26
- **R22** — The analyst is a separate agent rooted at the batch history: it may read anything there and write only `/proposal.md`; every other write is denied, so it cannot alter the evidence it reasons from. It starts from the batch summary, reads the runs and the instructions snapshot, and acts only on a criterion that failed the first attempt in **more than half** of the graded runs (the generator's reading of the course's "most runs" and "a problem appearing in one run out of five is not a pattern" — a post-build lever); anything seen in at least one but not more than half of the graded runs goes under `rejected` with the reason. It quotes evidence verbatim, never restates instructions the file already has, returns one structured `HarnessChange` whose `change` is the literal text to insert, and writes `proposal.md` with the sections `Summary signal`, `Current instruction gap`, `Evidence across runs`, `Proposed insertion`, `Rejected observations`. Turn cap 40. *Course-demonstrated* (CTX-B12). → AC27, AC28, AC46
- **R23** — Nothing is applied until a person approves the proposal; rejecting it leaves the instructions unchanged. *Course-demonstrated* (CTX-C). → AC29
- **R24** — Applying is plain code, never a model call: only `target: "prompt"` is applied, by inserting the `change` text at the end of the named section (the section ends at the next heading of the same or shallower depth; trailing blank lines are trimmed; one blank line before and after the insertion). Any other target is refused with a message containing `not applied automatically`; a section that does not exist is an error naming it. Each applied change creates a new instruction version; earlier versions are kept. *Course-demonstrated* (CTX-C). → AC30, AC31
- **R25** — After a change, the same batch is re-run under the new version and the two summaries are compared: per criterion (before, after) first-attempt passes, revisions needed, attempts (grading passes in total), token estimates; `improved` and `regressed` criteria; verdict `regression` if any criterion's passes fell, else `success` if no revisions were needed after, else `partial` if any criterion improved, else `no effect`. *Course-demonstrated* (CTX-C). → AC32, AC33
- **R26** — The baseline instruction file (version 1) has a fixed Procedure half and a Review guidance half (the half that gets revised), names the registered fetch tool exactly as `fetch_requirement` (the course's copies disagree — see CTX-C — and the code-registered name wins), and does **not** ask for `Resolved by:` or `Edge case:` lines: the rubric expects lines the instructions never ask for, which is the recurring gap the learning loop exists to find. *Course-demonstrated* (CTX-B9). → AC23, AC34

**Model, runtime and records**

- **R27** — `[environment]` The app reads exactly `OPENAI_API_KEY` and `OPENAI_BASE_URL` for every live model call, sends every request to `OPENAI_BASE_URL`, and reads the model for each role from `REVIEW_AGENT_MODEL`, `GRADER_MODEL` (falling back to the review agent's model, as the course ran both on one model) and `ANALYST_MODEL`. It never reads the `ANTHROPIC_*` pair, never contains a key literal, and never asks anyone for a key. Each role's model is a platform model that supports native tool calling and structured output (the model/provider Invariant, Environment Resolutions). `api/config` reports the backend, each role's model and the base URL — never a key. → AC35, AC36, AC44
- **R28** — `LLM_BACKEND=scripted` swaps every role's model for the §5 scripted stand-in and changes nothing else: the same harness, tools, permissions, grader wiring, stores and endpoints run. The offline suite passes with no key and no reachable network. *Project hardening* (the course's offline path replayed saved traces instead). → AC37
- **R29** — `[environment]` One server, bound to `0.0.0.0` on port 4000, serves both the page and the API. → AC38
- **R30** — `[environment]` Every URL inside the page is relative (`api/tickets`, never `/api/tickets`). → AC39
- **R31** — `[environment]` HTTP only: no WebSocket; the page learns about a running run by polling its run record. → AC40
- **R32** — Tickets, pages, runs, instruction versions, batches and proposals persist across a process restart. Environment-dimension invariant; *course-demonstrated* (the course's tracker and batch history kept them in flat JSON files, CTX-A). → AC41
- **R33** — `[environment]` The instruction files live inside the app's own folder (default `harness/instructions/`; each run's workspace gets a copy at `/memories/AGENTS.md`); the build never writes the workspace-root `AGENTS.md`. → AC42
- **R34** — Every run keeps a local trace: one row per model turn (`Model reasoning`, action `Calls <tool>[: <sections filled>]`, or `Finishes the review`) and one per tool result (`Tool`, the call's label, the result's text with whitespace collapsed and cut to 220 characters plus `…`); a run the turn cap ends (R9) closes with one `Harness` row whose action is `Stops: turn limit of <N> reached`. The grader's turns are recorded in the same trace, in order, with the same row kinds: its `read_file` call as a `Model reasoning` row `Calls read_file` followed by that call's `Tool` row, and its verdict as a `Model reasoning` row `Returns verdict: <result>`, a finishing row with no tool row after it. *Course-demonstrated* (CTX-A); replaces the hosted viewer (Environment Resolutions). → AC43
- **R35** — On first start with an empty data directory the app seeds: one requirement page `page-req-export` (kind `requirement`, title `Customer Data Export — Requirements`, version 1 authored `Avery (Product Manager)`, body = the `seed_data_export.md` clauses, one per line), one ticket `REQ-104` (`Review requirements: Customer Data Export`, linked to that page, assignee `Blake (Eng Lead)`, status `Open`), an empty run list, instruction version 1 = the baseline file, and the five batch documents. *Course-demonstrated* shape (CTX-A); content is the generator's own. → AC1

## 5. Acceptance Criteria ★ (the oracle)

### Fixture corpus

All files below live under `fixtures/` in the app folder, except the two shipped app files `harness/instructions/v1.md` and `harness/rubric.txt`, declared here because criteria read them; the building agent MUST NOT modify fixtures to make a test pass. A planted state that removes or overwrites a shipped app file restores it when the test ends. A **clause** is each non-empty line after a document's `REQUIREMENT:` title line. **Vague terms** (whole word, case-insensitive): `quickly`, `securely`, `standard`, `reasonable`, `appropriate`, `easily`, `promptly`, `relevant`, `sensible`, `large`. A clause containing one is **ambiguous**.

| File | Title line | Clauses (ambiguous ones marked with their term) |
|---|---|---|
| `requirement_docs/seed_data_export.md` | `REQUIREMENT: Customer Data Export` | `Customers shall be able to export their account data.` · `Exports should be delivered quickly.` (quickly) · `The system should support standard file formats.` (standard) |
| `requirement_docs/doc_01_session_timeout.md` | `REQUIREMENT: Session Timeout` | `Idle sessions shall be closed after a reasonable time.` (reasonable) · `Users must be warned before their session closes.` · `Closed sessions should be resumable easily.` (easily) |
| `requirement_docs/doc_02_product_search.md` | `REQUIREMENT: Product Search` | `Search results shall appear promptly.` (promptly) · `Results must be ordered by relevant criteria.` (relevant) · `The system shall record every search query.` |
| `requirement_docs/doc_03_audit_log.md` | `REQUIREMENT: Audit Log` | `Every administrator action shall be logged.` · `Logs must be stored securely.` (securely) · `Old entries should be archived after an appropriate period.` (appropriate) · `The log shall be searchable by date.` |
| `requirement_docs/doc_04_rate_limits.md` | `REQUIREMENT: Rate Limits` | `Clients shall be limited to a sensible number of requests.` (sensible) · `Limit breaches must be reported to the client.` · `Large customers may request higher limits.` (large) |
| `requirement_docs/doc_05_scheduled_reports.md` | `REQUIREMENT: Scheduled Reports` | `Users shall be able to schedule recurring reports.` · `Reports must arrive quickly after the scheduled time.` (quickly) · `Failed deliveries should be retried an appropriate number of times.` (appropriate) |
| `special/fx_stubborn.md` | `REQUIREMENT: Stubborn Fixture` | `Dashboards should load quickly.` (quickly) |
| `special/fx_loop.md` | `REQUIREMENT: Loop Fixture` | `Uploads should finish promptly.` (promptly) |
| `special/fx_rogue.md` | `REQUIREMENT: Rogue Fixture` | `Passwords must be stored securely.` (securely) |
| `special/fx_decoy.md` | `REQUIREMENT: Decoy Fixture` | `Emails should be sent promptly.` (promptly) |
| `special/fx_grader_error.md` | `REQUIREMENT: Grader Error Fixture` | `Invoices should be issued promptly.` (promptly) |

- The **batch documents** are the five `doc_0N_*` files; their ids are their file stems. `seed_data_export.md` is the seed page's version-1 body (R35).
- `seed_edit_v2.txt` — the seed page body with its second clause replaced by `Exports should be delivered in a reasonable time.` (still ambiguous: reasonable), the other two clauses unchanged.
- `harness/instructions/v1.md` (shipped as the baseline, R26/R33) — contains: a title; a `## Procedure` section listing the six stages of R3 in order, naming `fetch_requirement`, `write_file`, `edit_file`, giving the exact skeleton headings and the ambiguity bullet shape (bold-quoted clause, indented `Reason:` line), telling the agent to retry a tool that returns an error with the same arguments, never to modify the requirement or this file, and to finish with one short sentence and no tool call; a `## Review guidance` section with exactly four subsections in this order: `### Confirmed facts`, `### Ambiguities`, `### Clarification questions`, `### Assumptions`. It contains neither `Resolved by:` nor `Edge case:`.
- `verdict_pairs.json` — three before/after summary pairs (first-attempt passes out of 5; `revisions_needed`):

| Pair | Before (completeness, clarity, depth; revisions) | After | Expected verdict |
|---|---|---|---|
| `regression` | 5, 3, 3; 2 | 5, 2, 4; 3 | `regression` (clarity fell) |
| `partial` | 5, 0, 0; 5 | 5, 3, 0; 5 | `partial` (clarity improved, revisions remain) |
| `no_effect` | 5, 0, 0; 5 | 5, 0, 0; 5 | `no effect` |

- `harness/rubric.txt` (shipped with the app, R10; read at the start of every run) — exactly three lines, in R10's order: `- completeness: every clause of the requirement document is addressed somewhere in the analysis.`, `- clarity: every Ambiguities bullet has an indented "Resolved by:" line naming the fact or decision that would settle it.`, `- depth: every Ambiguities bullet has an indented "Edge case:" line naming a concrete production failure it could cause.`
- `bad_rubric.txt` — the single line `No criteria here.` (no `- ` criterion lines).
- **Planted states** (set up by the tests, declared here): `FETCH_SIMULATED_FAILURES=2` (two transient fetch failures, then success); the current instruction version's file removed from `harness/instructions/` (a missing instruction file); `harness/rubric.txt` overwritten with the text of `bad_rubric.txt` (a malformed rubric); a directory named with a finished run's `workspace_id`, recreated holding an `analysis.md` that contains `STALE-MARKER` (stale output from an earlier run); the two-document batch `fx_grader_error` + `doc_01_session_timeout` run directly through the batch runner, whose `fetch_requirement` resolves `fx_grader_error` to `special/fx_grader_error.md` (a planted batch may name a `special/` fixture by its file stem) and `doc_01_session_timeout` to its batch document file.
- `refused_changes.json` — three `HarnessChange` objects identical except `target`: `tool`, `grader`, `configuration`; plus one with `target: "prompt"` and `section: "### Nonexistent"`.

### The scripted model (honestly labelled stand-in)

`scripted_model.py` defines a chat model registered with the description **"Scripted stand-in for the live model — not a real LLM; responses follow the declared fixture script."** It implements the framework's chat-model interface, including tool binding and structured output, so the real harness runs unchanged (R28). It keeps a call counter, and exposes a test hook that holds its next response until the test releases it. Per role:

**Review agent role.** It reads the document title from the fetched text's `REQUIREMENT:` line to pick its mode (`normal` unless the title names a special fixture). A quirk below keyed by a document id (`doc_02_product_search`, `doc_03_audit_log`, `doc_04_rate_limits`) applies to any fetched text whose title is that document's (`Product Search`, `Audit Log`, `Rate Limits`), in event runs as in batch runs; the grader role keys its quirks the same way. The **label condition** holds when the agent's loaded instructions contain `Resolved by:` or its conversation contains grader feedback.
1. Calls `fetch_requirement` with the id from the opening message; on each error result, calls it again with the same id, until a call returns the document.
2. `write_file` `/analysis.md`: the skeleton with one Confirmed Facts bullet per clause (the clause text verbatim). Exception: on `doc_03_audit_log` while the instructions lack `Resolved by:` and no grader feedback has arrived, the clause `The log shall be searchable by date.` is omitted.
3. `edit_file` Ambiguities: one bullet per ambiguous clause, `- **"<clause>"**` then `  Reason: "<term>" is not defined.`; when the label condition holds, also `  Resolved by: a stated, measurable value for "<term>".` and `  Edge case: an implementation that guesses "<term>" fails in production.` On `doc_02_product_search`, the first Ambiguities edit uses an old string that occurs more than once in the file (a blank line); after the tool's error, it repeats the edit with the unique heading line.
4. `edit_file` Clarification Questions: one bullet per ambiguous clause, `- What exactly does "<term>" mean in "<clause>"?`
5. `edit_file` Assumptions: one bullet per ambiguous clause, `- A developer would choose their own meaning for "<term>".`
6. `edit_file` Summary: `The requirement has <c> clauses, <a> of which need clarification. Answer the clarification questions before implementation starts.`
7. Replies `Review complete.` with no tool call.
8. After grader feedback: one `write_file` rewriting the whole file — the six §3 headings, one Confirmed Facts bullet per clause, the Ambiguities bullets with their labelled lines, and the Clarification Questions, Assumptions and Summary sections exactly as steps 4–6 wrote them — then `Review complete.`

Modes: **stubborn** (`Stubborn Fixture`) — every revision rewrites the file without the two labelled lines; **loop** (`Loop Fixture`) — calls `fetch_requirement` again on every turn and never writes; **rogue** (`Rogue Fixture`) — before step 2, calls `edit_file` on `/memories/AGENTS.md`, then continues normally; **decoy** (`Decoy Fixture`) — step 7 replies `Added Resolved by: and Edge case: lines to every ambiguity.` although the file lacks them.

**Grader role.** First calls `read_file` on `/analysis.md`, then returns a verdict computed from the file it read and the rubric: if the rubric has no `- ` criterion lines → `failed`, no criteria. Otherwise, in rubric order: completeness passes when every clause of the fetched document appears verbatim in the file, else gap `Clause not addressed: "<first missing clause>".`; clarity passes when every Ambiguities bullet has an indented line starting `Resolved by:`, else gap `Each ambiguity bullet needs an indented "Resolved by:" line.`; depth likewise with `Edge case:`, gap `Each ambiguity bullet needs an indented "Edge case:" line.` Result `satisfied` when all pass, else `needs_revision`; explanation `<k> of 3 criteria pass.` Criterion names are echoed as `completeness`, `clarity`, `depth` — except on `doc_04_rate_limits`, where it echoes `Completeness check`, `Clarity (Resolved by)`, `Depth (Edge case)`. On `Grader Error Fixture` it raises an error on every pass.

**Analyst role.** First calls `write_file` on `/<label>/summary.json` (expected to be denied); then reads `/<label>/summary.json`, `/<label>/AGENTS.md` and every `/<label>/run_*.json`; writes `/proposal.md` with the five R22 sections; returns a `HarnessChange`: `target` `prompt`; `section` `### Ambiguities`; `issue` — one string naming every criterion failing the first attempt in more than half of graded runs (clarity first, joined with ` and `); `evidence` holding that criterion's first-pass gap quoted verbatim from each failing run (one string per run, clarity first); `recurrence` `<n>/<graded> runs: <run file stems, comma-separated>`; `change` = `For every ambiguity bullet, add two indented lines after Reason:` + a blank line + `  Resolved by: the fact or decision that would settle this ambiguity` + `  Edge case: a concrete production failure if this stays unresolved` (one line for each recurring criterion among clarity and depth); `rejected` = one entry per criterion failing the first attempt in at least one but not more than half of graded runs (`<criterion> failed the first attempt in <n> of <graded> runs (<doc ids>); not a pattern.`), and one entry per tool name that returned an error in at least one but not more than half of graded runs (`<tool> returned an error in <n> of <graded> runs (<doc ids>); not a pattern.`).

### Criteria

Each Given starts from a fresh data directory with `LLM_BACKEND=scripted`, budget 3 and `FETCH_SIMULATED_FAILURES=0` unless it says otherwise, and with `harness/instructions/` holding only the shipped `v1.md`, so the current instruction version is 1: a test that creates later versions removes their files when it ends, like any planted state. "A run on `<fixture>`" means: create a requirement page titled with the fixture's title-line text after `REQUIREMENT: ` (e.g. `Stubborn Fixture`) whose body is that fixture's clauses, one per line, and a ticket linked to it, then wait for the run to reach `complete` or `error`. `live` criteria use `LLM_BACKEND=live` and run after the offline suite; they never gate completion.

| AC | Given | When | Then | Rules |
|---|---|---|---|---|
| AC1 | A fresh start | `GET api/tickets`, `api/pages`, `api/instructions`, `api/batches/documents`; list the data directory | One ticket `REQ-104`, `Open`, linked to `page-req-export`, assignee `Blake (Eng Lead)`; one page `page-req-export`, kind `requirement`, one version whose body is the three seed clauses; instruction version 1 whose text equals `harness/instructions/v1.md`; documents `doc_01_session_timeout` … `doc_05_scheduled_reports`; the files for tickets, pages and runs exist; the runs list, the batch list (`GET api/batches`) and the proposal list are empty | (R35) |
| AC2 | Fresh start | `POST api/tickets/REQ-104/rerun`; read the run | The agent's opening message contains `REQ-104` and none of the seed clauses; the first trace row is `Calls fetch_requirement`; that call's argument is `REQ-104`; the fetched text is `REQUIREMENT: Customer Data Export — Requirements` followed by the page's latest version body | (R1) |
| AC3 | `FETCH_SIMULATED_FAILURES=2` | Re-run `REQ-104` | Trace has three `fetch_requirement` tool rows: the first detail starts `Error fetching requirement: 503`, the second `Error fetching requirement: request timed out`, the third contains `Customers shall be able to export their account data.`; the run reaches `complete` with `verification_status` `satisfied` | (R2) |
| AC4 | A run on `doc_02_product_search` | Read the run and its trace | The final file's headings are exactly the six §3 headings in order; `stage_order` is `Confirmed Facts, Ambiguities, Clarification Questions, Assumptions, Summary`; `in_order` is true; exactly one `edit_file` tool row has a detail starting `Error` | (R3) |
| AC5 | Re-run `REQ-104` completed | Read the run | `counts` = Confirmed Facts 3, Ambiguities 2, Clarification Questions 2, Assumptions 2; `summary_words` = 17; the Summary has two sentences | (R3, R4) |
| AC6 | Same run | Read the final Ambiguities section | Two bullets, `- **"Exports should be delivered quickly."**` and `- **"The system should support standard file formats."**`, each followed by indented `Reason:`, `Resolved by:` and `Edge case:` lines; `grading[0].analysis_markdown` has the `Reason:` lines and no `Resolved by:` line | (R4, R12) |
| AC7 | Same run | Read `page-req-export` and `page-analysis-req-104` | The requirement page still has exactly one version with the original body; the report page has kind `analysis_report` and `linked_ticket` `REQ-104` | (R5) |
| AC8 | A run on `fx_rogue` | Read the trace and the run's instruction version | The `edit_file` call on `/memories/AGENTS.md` returned an error; instruction version 1's text is byte-identical to before; the run reaches `complete` with `satisfied` | (R6) |
| AC9 | The current instruction version's file removed from `harness/instructions/` | Re-run `REQ-104` | The run's `state` is `error`, its `error` contains `memories/AGENTS.md`, and the scripted model's call counter did not move | (R7) |
| AC10 | Re-run `REQ-104` twice; after the first run, a directory with the first run's `workspace_id` recreated holding an `analysis.md` that contains `STALE-MARKER` | Read both runs | The two `workspace_id`s differ; the second run's final file does not contain `STALE-MARKER`; no workspace directory with the second run's id remains after it completes | (R8) |
| AC11 | A run on `fx_loop` | Read the run | `stop_reason` is `turn_limit`; the last trace row reads `Stops: turn limit of 40 reached`; the report is not complete | (R9) |
| AC12 | Re-run `REQ-104` | Read `grading` | Two passes: pass 1 `needs_revision` with completeness passed, clarity and depth failed with their gaps; pass 2 `satisfied` with all three passed; `verification_status` `satisfied`; `stop_reason` `finished` | (R10, R12) |
| AC13 | The built app | Inspect the configured grader instructions and the grader's tools | The instructions contain `satisfied`, `needs_revision`, `failed`, `/analysis.md` and `line number`; the grader's only tool is `read_file`, and during a run it returns that run's own `/analysis.md` | (R11) |
| AC14 | A run on `fx_decoy` | Read the run | The agent's final message of attempt 1 claims the labelled lines were added; pass 1 is `needs_revision` with clarity and depth failed; the grader's first action was `read_file` on `/analysis.md`; pass 2 is `satisfied` | (R11) |
| AC15 | A run on `fx_stubborn` | Read the run and its report page | Four grading passes, all `needs_revision`; `verification_status` `max_iterations_reached`; the report banner reads `Verification status: **max_iterations_reached** after 4 grading pass(es).` | (R12, R13) |
| AC16 | `harness/rubric.txt` overwritten with the text of `bad_rubric.txt` | Re-run `REQ-104` | One grading pass, result `failed`, no criteria; no revision write follows; `verification_status` `failed` | (R14) |
| AC17 | Fresh start | `POST api/tickets` linked to `page-req-export`, assignee `Casey (QA Lead)` | Response `201` with key `REQ-105` and a `last_run_id`; while the scripted model is held, that run's `state` is `running` and the ticket is still `Open`; once released and complete, page `page-analysis-req-105` exists, titled `Analysis Report — REQ-105`, version 1 authored `Requirements Analysis Agent (bot)` | (R15, R16, R19) |
| AC18 | Re-run `REQ-104` completed | Read `REQ-104` and its report page | Ticket `status` `Analysis Ready`, `last_analyzed_version` 1, `last_run_id` = the run's id, last comment `Analysis complete (satisfied), requirement version 1. See Analysis Report — REQ-104.`; report version 1 opens with the three banner lines, the third `Verification status: **satisfied** after 2 grading pass(es).` | (R15, R16) |
| AC19 | `REQ-105` created as in AC17; then `REQ-104` marked done | `POST api/pages/page-req-export/versions` with `seed_edit_v2.txt` | `retriggered` is `["REQ-105"]`; `REQ-104` has no new run and stays `Done`; `REQ-105`'s new run has `requirement_version` 2 | (R15, R17) |
| AC20 | Fresh start; `REQ-104` re-run completed | Inspect every status change; then `POST api/tickets/REQ-104/done`; then `POST api/tickets/REQ-104/rerun` | No run set `Done`; after the done call the status is `Done`; the rerun returns `409` and starts no run | (R17) |
| AC21 | Re-run `REQ-104` completed; then a page version saved with `seed_edit_v2.txt` (which re-runs `REQ-104`) | `GET api/tickets/REQ-104`; `GET api/pages/page-analysis-req-104/compare?a=1&b=2` | Two runs; the what-changed table shows requirement versions 1 → 2, status satisfied → satisfied, and identical counts (3, 2, 2, 2 both times); the diff is non-empty and contains `+` and `-` lines naming the changed clause; `run_a` and `run_b` are the two runs | (R18, R19) |
| AC22 | Fresh start | `POST api/pages` titled `Order History — Requirements` twice; `POST api/pages/page-analysis-req-104/versions` after a run | Page ids `page-order-history-requirements` and `page-order-history-requirements-2`; the report-page edit returns `400` | (R5, R19) |
| AC23 | Fresh start | `POST api/batches` (label `v1`); read its summary | `runs` 5, `graded` 5, `grader_errors` 0; completeness 4/5 (0.8), clarity 0/5 (0.0), depth 0/5 (0.0); `revisions_needed` 5; every run `satisfied` after exactly 2 passes; `v1/AGENTS.md` equals instruction version 1 | (R20, R26) |
| AC24 | The `v1` batch | Read run 4 (`doc_04_rate_limits`) and the summary | Run 4's first-pass criterion names are the paraphrased ones, yet the summary counts clarity and depth over all 5 graded runs (totals 5, passes 0) | (R20) |
| AC25 | The `v1` batch | Read run 3 (`doc_03_audit_log`) | First pass: completeness failed with gap `Clause not addressed: "The log shall be searchable by date."`; `messages` include a message containing that gap text; at least one `write_file` call's arguments are longer than 220 characters (untruncated); the final file contains the clause | (R20) |
| AC26 | A batch run directly over `fx_grader_error` and `doc_01_session_timeout` | Read the summary and the runs | `runs` 2, `graded` 1, `grader_errors` 1; rates are over 1 run (completeness 1/1, clarity 0/1, depth 0/1); the `fx_grader_error` run's passes are all `grader_error` with no criteria and its `status` is `grader_error` | (R13, R14, R21) |
| AC27 | The `v1` batch | `POST api/batches/v1/analyze` | Proposal `pending`; change `target` `prompt`, `section` `### Ambiguities`, `recurrence` starts `5/5 runs:`; `evidence` has 10 quotes, each a verbatim substring of a first-pass gap; `change` contains `Resolved by:` and `Edge case:`; `rejected` has exactly two entries, one naming completeness and `doc_03_audit_log`, one naming `edit_file` and `doc_02_product_search`; `proposal_markdown` has the five R22 section headings | (R22) |
| AC28 | Same analysis | Read the analyst's trace and `v1/summary.json` | The analyst's write to `/v1/summary.json` returned an error; the summary file is byte-identical to before; the only file the analyst created is `proposal.md` | (R22) |
| AC29 | A pending proposal from AC27 | `GET api/instructions`; reject it; analyze again; approve the new one | While pending and after rejecting, the current version is 1 and the rejected proposal's status is `rejected`; after approving, version 2 exists, version 1 is unchanged, and the proposal is `approved` | (R23) |
| AC30 | Approved as in AC29 | Compare instruction versions 1 and 2 | Version 2 = version 1 with the change's lines inserted after the last non-blank line of `### Ambiguities` and before `### Clarification questions`, one blank line on each side; every other line identical | (R24) |
| AC31 | `refused_changes.json` | Apply each change | The `tool`, `grader` and `configuration` changes are refused with `not applied automatically`; the `### Nonexistent` change errors naming `### Nonexistent`; the current instruction version is unchanged | (R24) |
| AC32 | Version 2 current (AC29) | `POST api/batches` (label `v2`); `GET api/compare?before=v1&after=v2` | v2: all three criteria 5/5 (1.0), `revisions_needed` 0, each run 1 pass; comparison: completeness (4, 5), clarity (0, 5), depth (0, 5); revisions (5, 0); attempts (10, 5); `improved` all three; `regressed` empty; verdict `success` | (R25) |
| AC33 | `verdict_pairs.json` | Compare each pair | Verdicts `regression`, `partial`, `no effect` respectively | (R25) |
| AC34 | `harness/instructions/v1.md` | Read it | Contains `fetch_requirement`, `## Procedure`, `## Review guidance` and the four `###` subsections in order; contains neither `Resolved by:` nor `Edge case:` | (R26) |
| AC35 | The source tree; then `GRADER_MODEL` unset, `REVIEW_AGENT_MODEL=openai:test-a`, `ANALYST_MODEL=openai:test-b` | Search every environment-variable read; `GET api/config` | Variables read are only `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `REVIEW_AGENT_MODEL`, `GRADER_MODEL`, `ANALYST_MODEL`, `LLM_BACKEND`, `FETCH_SIMULATED_FAILURES`, `APP_DATA_DIR`; no `ANTHROPIC_` read; no string starting `sk-`; config shows grader `openai:test-a`, analyst `openai:test-b`, and no key | (R27) |
| AC36 | `LLM_BACKEND=live`, `OPENAI_API_KEY=dummy`, `OPENAI_BASE_URL=http://127.0.0.1:9/v1` | `GET api/config`; re-run `REQ-104` | Config `base_url` is `http://127.0.0.1:9/v1`; the run reaches `state` `error` (connection refused) without any request leaving the container | (R27) |
| AC37 | `OPENAI_API_KEY` unset, `OPENAI_BASE_URL=http://127.0.0.1:9/v1`, `LLM_BACKEND=scripted` | Run the offline suite | Every non-`live` criterion other than AC37 itself passes | (R28) |
| AC38 | Server started | `curl` `http://localhost:4000/` and `http://localhost:4000/api/tickets`; inspect the listening socket | `200` HTML and `200` JSON from the same process; it listens on `0.0.0.0:4000` | (R29) |
| AC39 | The served page and every script it loads | Search for URLs | No `href`, `src`, `action` or request URL begins with `/` | (R30) |
| AC40 | Same | Search | No `WebSocket` and no `ws://`; run progress comes from polling `api/runs/<id>` | (R31) |
| AC41 | AC17's ticket and run completed; a `v1` batch done | Stop the server, start it again, read everything | `REQ-104`, `REQ-105`, `REQ-105`'s run and its report page, the instruction versions and the `v1` batch are all still returned | (R32) |
| AC42 | The built app | Read the instruction-file path the app uses | It is inside the app folder (`harness/instructions/`); the workspace-root `AGENTS.md` was not written by the build | (R33) |
| AC43 | Re-run `REQ-104` completed | Read the trace | Rows alternate `Model reasoning` and `Tool` (a finishing row — `Finishes the review` or the grader's `Returns verdict: <result>` — has no tool row after it); a row reads `Calls write_file: Confirmed Facts`; every `detail` has no newline and at most 221 characters | (R34) |
| AC44 `live` | `LLM_BACKEND=live`, platform models set per §2 | Re-run `REQ-104` | The run completes; the file has the six headings; `verification_status` is `satisfied` or `max_iterations_reached`; every request went to `OPENAI_BASE_URL` | (R10, R27) |
| AC45 `live` | Same | Read that run's passes | Every pass has 3 criteria in rubric order, each failing one with a non-empty gap; the grader's first tool call was `read_file` on `/analysis.md` | (R11) |
| AC46 `live` | Same; a live `v1` batch | Analyze it | A `HarnessChange` validates against §3; `proposal.md` exists; no file under `/v1/` changed | (R22) |

## 6. Standing Permissions (in force for the entire build)

**Always**
- Report every acceptance criterion with cited evidence (test output, file path, response body).
- Keep the scripted model's description honest (§5) and keep it out of the `live` path.
- Write decisions, resolved values and results to files: `resolved-decisions.md` is load-bearing here because the workspace is the record — a new chat starts with no memory of this one, and only what is on disk survives `[environment]`.
- Run long-lived servers in the background `[environment]`.

**Ask First** (derived from the course's argued trade-offs; CTX-C table)
- Changing a model role's tier — the review agent and grader on a cheaper model, the analyst on a stronger one (Lessons 2, 7) — or giving the grader its own model (Lesson 5): changes reliability without failing any offline criterion. This is the lever attached to the CONSTRAINED model/provider dimension.
- Changing the revision budget (3) or the turn caps (40 / 12): changes when a run gives up, without failing an offline criterion (Lessons 4, 5).
- Changing the "more than half of graded runs" recurrence threshold for the analyst (Lesson 7).
- Making more events start runs (for example `Done` tickets, or every page view) — changes what runs automatically without failing a criterion (Lesson 6; Ledger D1).
- Changing the instruction placement after the learning loop has produced versions — reworks where approved changes land (Lesson 3; Ledger D2).
- Removing the grader or the learning loop after build (Lessons 2, 5, 7; Ledger D3, D4).

**Never**
- Invent provenance or citations, or label an `[environment]` fact as course-taught.
- Let the agent or the analyst write its own instructions or the evidence it reads; apply a change without a recorded human approval.
- Mark a run `satisfied` (or a ticket `Done`) when the evidence says otherwise — the system must report `max_iterations_reached`, `failed` or `grader_error` honestly rather than pass.
- Modify fixtures to make a test pass.
- Commit, log or display secrets; ask the learner for a key; read any key variable other than `OPENAI_API_KEY`.
- Author the workspace-root `AGENTS.md` `[environment]` — the IDE rewrites it at every boot; the app's instruction files stay in its own folder.

## 7. Test Plan & Self-Verification

```bash
python3 --version                                   # record in resolved-decisions.md
python3 -m venv --system-site-packages .venv
.venv/bin/pip install deepagents==0.7.11 langchain==1.3.18 langchain-core==1.6.1 \
  langchain-openai==1.6.0 langgraph==1.2.11 openai==3.6.0 pydantic==2.13.5 \
  python-dotenv==1.2.3 flask pytest
# offline suite — the completion gate
env -u OPENAI_API_KEY LLM_BACKEND=scripted OPENAI_BASE_URL=http://127.0.0.1:9/v1 \
  .venv/bin/python -m pytest -m "not live" -q
# serve (background), then the HTTP checks
.venv/bin/python app.py &
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:4000/
curl -s http://localhost:4000/api/tickets
# live pass — runs after the offline suite, never gates completion
LLM_BACKEND=live .venv/bin/python -m pytest -m live -q
```

The building agent MUST report results per acceptance criterion (AC1–AC46) with cited evidence — test output lines, file paths, response bodies. "Should pass" or "looks correct" counts as a failure: it means the criterion was not run. Report each `live` criterion's result separately; a `live` failure is reported, not hidden, and does not block completion.

**Tests by option**

| Option id | Rules and criteria that no longer apply | Rules, criteria and Ledger cells that change (and how) | Offline-suite criteria switched off |
|---|---|---|---|
| L1b | — | The restored item is built per its handling tag; it adds no criteria | — |
| D1b | R15, R16, R17, R18, R19; AC17, AC18, AC19, AC20, AC21, AC22 | R1/AC2: the opening message names the chosen document's id. R5/AC7: the report is shown on the run's page; no report page exists. R35/AC1: no tickets or requirement pages are seeded; the seed document is listed as a runnable document. R32/AC41: runs, instruction versions and batches persist. AC3, AC4, AC5, AC6, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15, AC16, AC36, AC43, AC44: "re-run `REQ-104`" and "a run on `<fixture>`" become a manual run on that document. AC15: its report-banner clause is dropped (no report page exists); the four passes and `max_iterations_reached` stay. Ledger L1 Decision (the §1 list it presents): item 1's seam swaps only the page lookup, since no tickets exist | AC17, AC18, AC19, AC20, AC21, AC22 |
| D2b | — | R6/AC8: writes are denied under `/memories/` and `/skills/`. R7/AC9: a missing instruction file or skill file fails the build of the agent. R26/AC34: version 1 is the procedure file plus one skill per review-guidance subsection; the Ambiguities skill lacks the two labels. R24/AC30: an approved change is appended to the end of the Ambiguities skill's body. R33/AC42: skills sit beside the instruction file. AC43: the scripted review agent, before the write or edit that fills each of the four list sections, calls `read_file` on that section's skill (`/skills/confirmed-facts/SKILL.md`, `/skills/ambiguities/SKILL.md`, `/skills/clarification-questions/SKILL.md`, `/skills/assumptions/SKILL.md`), and its label condition reads "loaded instructions" as the instruction file plus the skill bodies it has read; before the step-2 `write_file` it reads `/skills/ambiguities/SKILL.md` as well as `/skills/confirmed-facts/SKILL.md`, so the `doc_03_audit_log` exception sees an approved change and AC32 holds unchanged; the trace adds those `read_file` rows | — |
| D2c | R6; AC8 | R7/AC9: missing stored instruction text fails the build. R26/AC34: version 1 is stored text passed as the system prompt. R24/AC30: an approved change edits the stored text, taking effect for agents built afterwards. R20: the batch snapshot is that text. R33/AC42: the text is stored in the app folder | AC8 |
| D3b | AC13, AC45 | R10, R11, R12, R13, R14: verdicts come from code checks on the report file; the spec supplies no parameters for them (in particular none for completeness). AC12, AC14, AC15, AC16, AC23, AC24, AC25, AC26, AC27, AC32: run against the deterministic grader; assertions hold only where its checks agree with the scripted grader's declared rule — list each one as *Adapted*. `GRADER_MODEL` is not read | AC13 |
| D3c | R10, R11, R12, R13, R14, R20, R21, R22, R23, R24, R25; AC12, AC13, AC14, AC15, AC16, AC23, AC24, AC25, AC26, AC27, AC28, AC29, AC30, AC31, AC32, AC33, AC44, AC45, AC46 (D4 is skipped by its condition) | R9/AC11: cap 12. R16/AC18: banner `Verification status: **not graded** after 0 grading pass(es).`; `verification_status` is null. AC3, AC8: end `complete` with no grading. AC5, AC6: the first draft is final — Ambiguities bullets carry only `Reason:` lines. R16/AC18: the comment reads `Analysis complete (not graded), requirement version 1. See Analysis Report — REQ-104.` R18/AC21: the what-changed table shows status not graded → not graded. R35/AC1: no batch documents are listed. R32/AC41: no batches to persist — the Given drops "a `v1` batch done" and the Then drops "the `v1` batch". Ledger D2 Invariant ("every version is kept outside the agent"): only version 1 exists, since no learning loop creates versions. R27/AC35: only `REVIEW_AGENT_MODEL` is read for roles. Ledger L1 Decision (the §1 list it presents): items 3, 7 and 9 are left out, since the grader slot and the learning loop they attach to do not exist | AC12, AC13, AC14, AC15, AC16, AC23, AC24, AC25, AC26, AC27, AC28, AC29, AC30, AC31, AC32, AC33 |
| D4b | R20, R21, R22, R23, R24, R25; AC23, AC24, AC25, AC26, AC27, AC28, AC29, AC30, AC31, AC32, AC33, AC46 | R35/AC1: no batch documents are listed. R32/AC41: no batches to persist — the Given drops "a `v1` batch done" and the Then drops "the `v1` batch". Ledger D2 Invariant ("every version is kept outside the agent"): only version 1 exists, since no learning loop creates versions. R27/AC35: `ANALYST_MODEL` is not read. Ledger L1 Decision (the §1 list it presents): items 7 and 9 are left out, since the learning loop they attach to does not exist | AC23, AC24, AC25, AC26, AC27, AC28, AC29, AC30, AC31, AC32, AC33 |

When the build is complete and every result above is reported, conclude your final report with an infra/structure diagram of the built app — the server, its page and API, the agent with its tools and per-run workspace, the grader, the stores, the batch history and the analyst — followed by the exact sentence: "This is the infra/structure diagram of this app".

## Runtime (lab)

Everything in this section is `[environment]`: contributed by the lab, never by the course.

**Container.** Debian, non-root user, Node 22, Python 3 with venv, sqlite3, git, build tooling. Preinstalled Python packages: `fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic` — nothing else (no vector stores, embedding models or ML frameworks). Outbound network works, but every install costs the learner session time: batch installs early and announce them (§2). Create the venv with `--system-site-packages`; where a course pin differs from a preinstalled copy, the course pin wins inside the venv. Memory is shared with the coding agent's own process; this app holds no local model, so no model-release rule is needed.

**Model access.** The container exports `OPENAI_API_KEY`/`OPENAI_BASE_URL` and `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`, each base URL pointing at the platform proxy. This app reads only the OpenAI pair (R27). No other service key or account exists here, which is why several course options are `unavailable` (§1). The model the coding agent runs on is the learner's per-conversation choice and says nothing about the app's models.

**Preview.** One server on port 4000 bound to `0.0.0.0` (R29); the preview is reverse-proxied under a path prefix, so every in-page URL is relative (R30); HTTP only, WebSocket upgrades are not proxied, streaming responses work (R31).

**Workspace.** The workspace is the record: decisions and results go to files. Every tool call is visible to the learner. The workspace-root `AGENTS.md` is rewritten by the IDE at every boot and is never authored (§6 Never); the app's own instruction files, which this course's pattern versions and edits, live in the app folder (R33).

**Question mechanism.** Questions are asked with a `choices` fence as described in §0's `[environment]` paragraphs.

**Environment failure modes.**
- **Root-absolute URL under the proxied preview.** *Symptom:* the app works on `localhost` but the preview shows a blank or broken page and failing API calls. *Cause:* `/api/...` resolves against the IDE's origin, not the proxied app prefix. *Fix:* relative URLs everywhere in the page. Enforced by R30, AC39.
- **Live updates over WebSocket.** *Symptom:* run progress never arrives in the preview. *Cause:* the proxy does not upgrade WebSockets. *Fix:* poll the run record. Enforced by R31, AC40.
- **Guidance written to the workspace-root `AGENTS.md`.** *Symptom:* instructions vanish after a restart. *Cause:* the IDE rewrites that file at boot. *Fix:* keep the app's instruction files in its own folder. Enforced by R33, AC42.
- **A key asked of the learner or read under a guessed name.** *Symptom:* a stalled build or auth errors against the proxy. *Cause:* the ambient variables were not used. *Fix:* read exactly `OPENAI_API_KEY` and `OPENAI_BASE_URL`. Enforced by R27, AC35, AC36.

## Course Context Pack (embedded — agent-readable)

Concepts only; no course code is reproduced. Anchors are stable names, not numbers.

### CTX-A. The pattern

Four nested loops around one agent, each answering a different question:

1. **Agent loop — do the work.** The model repeatedly calls tools, observes results and decides the next step until it says it is done. Here: fetch the requirement by id, lay down a report skeleton, fill one section per turn. Engineering levers at this level are the model, the tools and how tools are described.
2. **Verification loop — is "done" actually good enough?** A grader checks the finished output against a rubric of explicit pass/fail criteria; if any fails, specific feedback goes back for another attempt within a bounded budget. It adds reliability and can make a cheaper model viable for harder work.
3. **Event-driven loop — when should the agent run?** An event in the system where the work already happens (a ticket created, a requirement edited) triggers the verification-wrapped agent, and its result is written back into that system (an agent-owned report page, a ticket status, a comment), producing new events. A person still decides when the work is done.
4. **Learning (hill-climbing) loop — improve the agent itself.** Runs over many documents are recorded in full; first-attempt pass rates per criterion show what the agent is systematically corrected on; an analyst agent reads the evidence (read-only) and proposes one change to the agent's instructions; a person approves; plain code applies it; the same batch is re-run and compared to confirm the improvement without regression. Traces — the record of every step, tool call and grader feedback — are where an agent's behavior is visible, because the agent is not deterministic.

Supporting harness ideas: instructions live in files loaded every run (versionable and improvable from outside the agent); the agent's filesystem is confined to one workspace; permissions, not instructions, keep the agent off its own instructions.

### CTX-B. Failure-mode catalog

- **B1 Transient tool failure.** Symptom: the fetch returns an error (503, timeout). Cause: an unreachable external system. Fix: retry the same call with the same arguments; the run completes. Enforced by R2, AC3.
- **B2 "Done" that is not good enough.** Symptom: the first draft names an ambiguity but not what would resolve it or what could go wrong. Cause: nothing in the agent loop checks the output. Fix: a grader with explicit criteria sends it back with the gap. Enforced by R10, R12, AC6, AC12.
- **B3 Grading by resemblance.** Symptom: the grader passes criteria the file does not satisfy. Cause: it judged the conversation, or how the file looked, not its content. Fix: give it a file-reading tool, require a verbatim quote with a line number, apply labels literally. Enforced by R11, AC13, AC14.
- **B4 Silently missing instructions.** Symptom: a plausible but bad review. Cause: the framework ignores a missing memory file. Fix: fail loudly before the run. Enforced by R7, AC9.
- **B5 Stale output from an earlier run.** Symptom: the agent reads a finished report left on disk and skips stages. Cause: a reused workspace. Fix: a fresh workspace per run. Enforced by R8, AC10.
- **B6 The agent editing its own instructions.** Symptom: instructions drift during a run. Cause: the agent has `edit_file` and the instructions sit in its filesystem. Fix: deny writes there by permission. Enforced by R6, AC8.
- **B7 Turn cap mistaken for completion.** Symptom: an exhausted run reads like a finished one. Cause: both end the stream the same way. Fix: name the stop reason. Enforced by R9, AC11.
- **B8 Budget exhaustion reported as an ordinary verdict.** Symptom: a run that ran out of revisions shows `needs_revision` like any other pass. Cause: the last pass's result does not say the budget is spent. Fix: derive `max_iterations_reached`. Enforced by R13, AC15.
- **B9 The same correction every time.** Symptom: clarity and depth fail the first attempt on every document. Cause: the rubric expects labelled lines the instructions never ask for. Fix: the learning loop finds the recurrence and adds the missing instruction. Enforced by R20, R25, R26, AC23, AC32.
- **B10 Criterion names that drift.** Symptom: one recurring criterion splits into several in the counts. Cause: the grader paraphrases criterion names. Fix: identify criteria by rubric position. Enforced by R20, AC24.
- **B11 Grader errors counted as passes.** Symptom: inflated pass rates. Cause: a failed grader leaves a pass with no criteria. Fix: exclude ungraded runs and count them separately. Enforced by R14, R21, AC26.
- **B12 Acting on a one-off.** Symptom: a change made for one document's quirk. Cause: a single occurrence mistaken for a pattern. Fix: act only on what recurs across most runs; record the rest as rejected. Enforced by R22, AC27.
- **B13 Counts that hide change.** Symptom: before/after bullet counts look the same, so nothing seems to have changed. Cause: the content changed completely while the shape did not. Fix: show counts and the full text diff together. Enforced by R18, AC21.

### CTX-C. Decision background

**How to read the provenance notes.** A *litmus branch* says why an argued subject became what it is: *row* (both sides were shown working, so the reader chooses), *bake-in* (the course showed or warned that the other side fails, so the taught side is a rule), or *lever* (the sides differ only in a number, so it is a default value you may tune later). A Trade-off note `Litmus: working` means the alternative is shown working, which takes the *row* branch. *Narrative* marks a subject the course raised but did not argue as a builder's choice, or an alternative it argued but never showed working on a subject that changes no component, owner or guarantee — background only, never asked and never built. A *realization branch* is the `Branch:` note in a Ledger Default cell, saying how the default relates to what the course ran: *the course's own realization* (the default is what the course built, kept as is; *keyless* adds that it needs no credential) or a lighter stand-in on a substitution row. A *post-build lever* is a value set by default and tunable after the build; a *contradicted lever* is one the course set inconsistently, resolved by fixed branches in order — the value the narration states, else the end-to-end application's config, else the most frequent value. *Stakes* asks whether picking the other side up front would change structure, semantics or a guarantee; only then does a contradiction become a row. The *heavy bar*: an option is heavy when it needs a credential, a paid account, admin or container setup, or special hardware; network access alone is not heavy. A *substitution row* is one whose default is a lighter stand-in for what the course ran; *realization tiers* rank stand-ins (ships with the language, embedded library, local service). *Untakeable* means this lab cannot provide what an option needs (a credential it does not supply, or a completion gate that would wait on a person or a live model); such options are tagged `unavailable` in §1. `[environment]` marks facts from the lab, never the course. *Tie-breaker 1* (a demonstrated failure wins): when the course shows or warns that the other side fails, the taught side is baked in as a rule. *Tie-breaker 2* (a trade-off about a value is a lever): when the sides differ only in a number, the subject is a body default plus a §6 Ask-First entry, never a row. *The generator's reading* marks a number the spec chose to quantify a spoken heuristic of the course (e.g. "most runs"); it is a post-build lever. A *declared drop* names course packages or constants left out because they only served presentation. Rule labels: *course-demonstrated* traces to the course materials through a `(CTX-…)` anchor; *project hardening* is a constraint this spec added that the course did not demonstrate. §1 handling tags: `restorable` — additive and owned by no row, built if brought back at L1; `buildable, no criteria` — named by the course but never built, so it may be built but the spec supplies no parameters and no acceptance criteria for it; `unavailable` — cannot be taken in this lab (untakeable, or outside the delivered build mode).

**Mined trade-offs** (every argued or spoken trade-off, its lesson, and where it went):

| Trade-off | Lesson | Disposition |
|---|---|---|
| Match model capability to task: cheaper, faster model for simple work, a capable one for complex work | 2 | lever — attached to the CONSTRAINED model/provider dimension; tie-breaker: sides differ in which model fills a role, which this lab resolves per role at checklist time (§2, Ask First) |
| Same model for agent and grader, or a different grader model ("a common production choice") | 5 | lever — same attachment as above (§2, Ask First) |
| Analyst on a stronger model, because finding what recurs across five traces is "the one job the cheaper model does unreliably" (course README) | 7 | lever — same attachment (§2, Ask First) |
| Verification loop or the agent loop alone ("set this to 0 … the same basic agent loop") | 2, 5 | row D3 |
| Grader kind: deterministic or a model as judge | 2 (slides 2.6, 2.7) | row D3 (merged as one subject) |
| A human acting as the grader | 2 (slide 2.12) | row D3 option; unavailable in this lab (§1) |
| Verification makes cheaper models viable for harder tasks | 2 | narrative — rationale for D3's default, not a separate choice |
| Event-triggered or manual runs (friction of copy-paste) | 6 (slide 6.3) | row D1 |
| Real Slack/Jira/Confluence or the simulated tracker | 6 | row D1; real services unavailable in this lab (§1) |
| Scheduled versus event triggers | 2 | narrative — a taxonomy of trigger kinds, never argued for this agent; §1 item 6 |
| Nest all loops or compose a subset | 2 | rows D1, D3, D4 |
| Learning loop or per-run correction only | 7 | row D4 |
| Instruction placement: system prompt, always-loaded file, skills | 3 | row D2 |
| Procedural improvements versus memory improvements | 2 | narrative — a taxonomy of what a learning loop can change; §1 item 7 |
| Merging harness changes only with evals that show no regression | 2 | bake-in R25 — tie-breaker 1: the course warns confidence is not possible without them |
| Human approval at each loop level | 2 (slide 2.12) | narrative — a taxonomy of oversight points; the two the course built are bake-ins R17, R23 |
| Turn cap is a safety stop, not the normal stop | 4 | lever R9 — tie-breaker 2 (a number) |
| Revision budget 3 (notebook, batch) versus 2 (tracker app) | 5 | lever R12 — tie-breaker 2; contradicted, value by the narration branch |
| Grader judging the file versus the conversation (code comments) | 5 | bake-in R11 — tie-breaker 1: the course states the grader otherwise passes unsatisfied criteria |
| Analyst proposes, plain code applies (module docstring) | 7 | bake-in R22, R24 — tie-breaker 1: the course warns an agent editing its evidence "is not analyzing anything" and a non-prompt change could be half-applied |
| A single occurrence is not a pattern | 7 | lever R22 — tie-breaker 2 (a threshold); "more than half" is the generator's reading |
| Counts versus full diff when comparing runs (tracker README) | 6 | bake-in R18 — tie-breaker 1: the course warns counts alone mislead |
| Write-deny on instructions versus relying on instructions | 4, 5 (code) | bake-in R6 — tie-breaker 1 |
| Saved-trace replay versus live runs (`USE_LIVE_LLM`) | 4, 5, 7 | narrative — notebook convenience; its role is taken here by the scripted model (Environment Resolutions) |

**Contradictions recorded** (both sides, and how each was settled):
- *Revision budget*: 3 (Lesson 5 notebook, batch module) vs 2 (tracker app) → 3, narration branch; lever (R12).
- *Simulated fetch failures*: 0 (helper default, batch module) vs 2 (Lesson 4 notebook table, narration, saved trace) → 2 for the demonstration fixture (narration), 0 for normal runs (end-to-end config); lever (R2).
- *Fetch tool name in the instructions*: `fetch_requirement` (working copy, the registered tool) vs `fetch_requirement_from_jira` (the two batch snapshots and a slide) → the registered name, narration branch ("fetch_requirement tool", Lesson 4); stakes fail (no structural change) (R26).
- *Memory file name*: `Agent.md` (slides) vs `AGENTS.md` (code, Lesson 4 narration) → `AGENTS.md`, narration branch (Lesson 4 narration).
- *Lesson 5 first-attempt results*: narration says completeness failed only for the third document and the fifth passed everything; the committed batch summary has completeness 5/5 and clarity/depth 0/5 (different runs). The fixtures reproduce the narration's completeness one-off and the committed clarity/depth signal.
- *Requirement wording* (slides "shall … common file types" vs narration "should … all common files"): irrelevant here — fixtures are the generator's own.
- *Course model in slide code* (`gpt-5.5` on the base-agent slide vs `gpt-5.4-mini` in notebooks): provenance only (CTX-D).

**Backing for Ledger rows.** → Ledger D1: the course's tracker app exposed ticket creation, page edits and a manual re-run as triggers and wrote results to a separate agent-owned page so version history shows every past analysis and who wrote it. → Ledger D2: the review agent's file separates a fixed Procedure from Review guidance, "the half that gets revised"; the system prompt only points at it. → Ledger D3: the grader in the course is the framework's rubric middleware with custom instructions and a file-reading tool; a checkpointer was attached only to match the framework's docs. → Ledger D4: the analyst's change format names four targets (prompt, tool, grader, configuration) but the course scoped analysis to the prompt "because that is what the current evidence implicates".

**Course name-map (provenance, not binding).** Review agent builder `build_review_agent`; runners `run_review_loop_live` / `run_verification_loop_live`; tracker trigger `run_automation`; batch runner `generate_run_history`; analyst `propose_harness_change`; applier `apply_change`; comparer `compare`; course ticket ids `AUTH-142` (file upload), `NOTIF-205`, `AUTH-101`, `PAY-310`, `ACCESS-118`, `ALERT-227`; tracker seed `REQ-104` / `page-req-upload`; tracker port 5050; the primer's poet agent (turn cap 30, four poem-form skills) is teaching material, not built. Declared drop of presentation-only constants: run names and tags, tracing project names, the tracker's colors and styles, the course's cast of names (replaced by the generator's own).

### CTX-D. Perishable assumptions

Treat these as search keywords against current documentation, not guaranteed imports. The concepts in CTX-A to CTX-C are durable; only these names are perishable.

- `deepagents` 0.7.11: `create_deep_agent(model, tools, system_prompt, memory=[...], backend, permissions, middleware, checkpointer, response_format)`; `FilesystemBackend(root_dir, virtual_mode=True)` (the agent sees its root as `/`); `FilesystemPermission(operations, paths, mode)` (first match wins; unmatched is allowed); `FilesystemMiddleware(backend, tools=[...])`; `RubricMiddleware(model, max_iterations, tools, system_prompt, on_evaluation)` — flagged beta, warns on construction, activates only when a `rubric` is present on the invocation state; passing `system_prompt` replaces its default grader prompt, so restate the verdict definitions and re-check that default before upgrading. Private state key `_rubric_status`.
- `langchain`: `ModelCallLimitMiddleware(run_limit, exit_behavior="end")`; `create_agent`; `tool` decorator; skills via `skills=["/skills/"]` with YAML frontmatter `name`/`description`. `langgraph`: `InMemorySaver`.
- Course model ids (provenance only, never assumed served by the proxy): `openai:gpt-5.4-mini` (agent, grader, batch runs), `openai:gpt-5.5` (analyst). Course prices per million tokens: gpt-5.5 5.00/30.00, gpt-5.4-mini 0.75/4.50.
- **Request-parameter compatibility:** reasoning-era model families may reject standard parameters such as `temperature` or a maximum-token argument; parameter support is as perishable as a model name. Send none the course did not set (it set none).
- Token counting: `tiktoken` encoding `o200k_base`, falling back to characters ÷ 4.
- Hosted tracing variables (unavailable here): `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`.

### CTX-E. Provenance map

Lesson numbering follows the transcripts. Nothing in this spec requires platform access.

| Lesson (transcripts) | Course files | Feeds |
|---|---|---|
| 1 Introduction | — (video) | CTX-A overview |
| 2 Overview of Loop Engineering | Wide deck, 13 slides (all narrated except the title card) | CTX-A 1–4; CTX-C trade-offs on models, grader kind, human oversight, composability, triggers, learning categories |
| 3 Deep Agent Primer | primer notebook; Tall deck slides 1–5 (title card deck-only, others narrated) | CTX-A harness ideas; Ledger D2; CTX-D |
| 4 Agent Loop | agent-loop notebook; helper module; instruction file; Tall deck slides 6–10 | CTX-A 1; B1, B4, B5, B6, B7; R1–R9, R34 |
| 5 Verification Loop | verification notebook; rubric and grader instructions in the helper module; Tall deck slides 11–14 | CTX-A 2; B2, B3, B8, B11; Ledger D3; R10–R14 |
| 6 Event-Driven Loop | tracker app (no notebook) and its README; third deck (4 slides) and Tall deck slides 15–16; screen-recorded Slack/Jira/Confluence demos | CTX-A 3; B13; Ledger D1; R15–R19 |
| 7 Learning loop | learning notebook; batch and analysis modules; two instruction snapshots, proposal, summaries; Tall deck slides 17–18 | CTX-A 4; B9, B10, B12; Ledger D4; R20–R26 |
| 8 Conclusion | — (video) | — |
| `[environment]` coding-agent-lab overlay (not a lesson) | the lab's rules and runtime facts | Environment Resolutions; §2 environment rows; R27, R29–R31, R33; `## Runtime (lab)`; §0 `[environment]` paragraphs |

Slides read: all 35 — Wide deck (13), Tall deck (18), third deck (4). Title cards are deck-only; every other slide is narrated (ranks with its lesson's transcript). Deck-only contributions: none beyond lesson titles; the slide-only `Agent.md` spelling lost to the code (CTX-C).

---
*Spec v1 · course: Loop Engineering with LangChain DeepAgents · project: requirements-review loop app (lab-fixed) · Living document: when the build agent produces something unexpected, add the missing constraint here and re-run.*
