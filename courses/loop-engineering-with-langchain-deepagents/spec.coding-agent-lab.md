# Spec: Requirements Review Agent with Four Loops — Coding-Agent-Lab Build

> **What you're building:** a web app that reviews requirement tickets and learns from its own runs. You open the board, create a ticket against a vague requirement page, and watch the agent fetch the page, write a five-section analysis file, get graded against a three-line rubric, and revise until the grader is satisfied; you edit the page and the analysis re-runs on its own; you open the Learning page, run the agent over five seeded documents, read the analyst's proposal for the agent's instructions, approve it, re-run the batch and see every document pass on the first attempt. The fastest path: answer the gate's first question with the recommended baseline build and it builds end-to-end; the build is COMPLETE when the offline suite passes — the platform's model keys unlock only the `live` tests and live use of the finished app.
>
> This file is self-contained: the Course Context Pack at the end replaces every external course reference, so nothing here requires course or platform access.
>
> `(CTX-X)` anchors mark course-derived knowledge; `[environment]` marks facts contributed by the lab, never by the course. The Decision Ledger below holds every point where the build could diverge, each pinned to one course-derived default, so the spec builds as-is with no intake.
>
> Generated from the *Loop Engineering with LangChain DeepAgents* notebooks + transcripts + slides on 2026-10-13, guide @ `4e1b71e`, overlay `coding-agent-lab` @ `bb420fa`.

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

   *`[environment]` In this lab the structured question tool is a fenced `choices` block: put the explanation in prose above it, make the fence the last thing in your message with one option per line, and precede it with a line reading "Question N of M — <decision>" so both of you can see nothing was skipped. M is defined once for the whole gate: the Ledger's row count plus one — this first question plus one question per row — so here M is 5 and this question is "Question 1 of 5"; on the baseline path the gate ends after Question 1. A click sends the option line verbatim, and a typed reply naming an option counts identically. Only the latest message's buttons stay live, so a changed answer is re-asked as a new question — never ask the person to go back to an earlier message.*

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

   *`[environment]` Each row is one message ending in its own `choices` fence, numbered "Question N of M — <decision>" with the M the step-2 paragraph defines (the row count plus one, so the rows are Questions 2 … M, here 2 … 5). A click and a typed answer naming an option are equivalent. Only the latest message's buttons stay live: if an earlier answer must change, re-ask that row as a new question rather than pointing at the old one.*

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

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option. Rows are grouped learner → design → realization (no contradicted row survived the stakes test — see CTX-C). The six learner-context dimensions were all derived; five of them are resolved by the lab in the Environment Resolutions table that follows, and only the scope-boundary row remains here.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L1 | learner | **Scope boundary.** Present the §1 "Not Included" list *inside this question*, item by item with each item's handling tag, and ask whether every exclusion stands. | — | Keep as is: every §1 exclusion stands and the full acceptance set (AC1–AC42) is built. | (a) keep every exclusion; (b) bring something back — name the item in free text; only items tagged `restorable` can come back at this gate, an `owned-by-row` item is decided on its own row, a `named-never-built` item can be built but this spec supplies no parameters and no acceptance criteria for it, and an `unavailable` item cannot be restored in this lab. A new exclusion is also free text and must name the acceptance criteria it retires. | Restoring an item adds work the acceptance criteria do not cover; retiring criteria removes the oracle for that behaviour. | learner |
| D1 | design-argued | **Instruction placement** — where the review agent's standing instructions live. | The instructions are loaded from a file at the start of every run; the file sits inside the agent's confined filesystem and outside its write reach; the harness refuses to run without it; and it is the file the learning loop's proposals target. Exercised by AC8–AC10, AC28. | One always-on instructions file (`/memories/AGENTS.md` inside the run workspace) loaded on every run, with a one-sentence system prompt that only points at it; no skills directory. This is the course's choice for the review agent (Lessons 4–7). | (a) one always-on instructions file, no skills (course default); (b) the always-on file plus a `skills/` directory whose per-procedure files are disclosed progressively — only each skill's name and description are loaded up front and its body is read on demand — the primer's layout, built and shown working on the poet agent (Lesson 3). Under (b) R7 seeds each run workspace with the `skills/` directory beside the instructions file; no acceptance criterion retires and none changes (AC8–AC11 assert the instructions file, the refusal without it and the fresh workspace, not the absence of other files); this spec authors no skill content — a build choosing (b) writes its own skills, and the spec supplies no fixture and no criterion for their disclosure. | Lesson 3 narration: the always-on file costs context on every call, so it must stay short; a skill costs one description line until the agent reads it, so a large library stays cheap. The review agent runs one fixed procedure every time, so the course kept it in the one file; with skills, the learning loop must also decide which file a proposed change targets (this spec's analyst targets only the always-on file). Litmus: **row** — both placements were built and shown working and the sides differ in a component, not a value. | course+learner |
| D2 | design-structural | **Grader kind** — what verifies the report. | An evaluator independent of the agent's own completion claim judges the written report *file* against the three named criteria, returns a per-criterion pass/fail with gap text for every failure, and the loop re-runs the agent with that feedback up to a budget. Exercised by AC12–AC15. | An LLM grader: a second model call that receives the rubric, holds a read-only file tool, and returns a structured verdict — the course's grader (Lesson 5). In the offline suite it is driven by the scripted grader stand-in (row RR1). | (a) LLM grader over a text rubric (course default); (b) deterministic grader — code evaluates each criterion directly (Lesson 2 names this kind, with "links resolve, CI passes" as its docs-agent example; the lab's clarity and depth criteria are label checks, and its completeness criterion becomes the literal check "every clause present verbatim"). Criteria that exercise only the Default and do not apply under (b): AC12's `read_file` tool-call assertion and AC13's line-number assertion (R8's read-and-quote discipline belongs to a model grader), and AC16 entirely (its grader error is the scripted model grader raising on the `(GRADER-ERROR)` title; a code grader never errors, so under (b) R10's path is reached only through the `batch_with_error` fixture, AC17); every other grading assertion stands, because the fixtures' verdicts are literal checks a code grader reproduces. | An LLM grader can judge a semantic criterion (completeness) but passes by resemblance unless forced to read and quote the file (R8); a deterministic grader is exact on label criteria and checks coverage only literally — a clause present verbatim — never semantically (a paraphrased clause counts as unaddressed). A human grader is Lesson 2's third kind but is not offered here: it would make the offline suite wait on a person (§1, `unavailable`). Switching moves ownership of the verdict between model and harness — the structural litmus. Litmus: **row via design-structural** — Lesson 2 presented the kinds without arguing a trade-off, so design-argued does not apply, and neither kind was shown failing. | course+learner |
| RR1 | realization | **Acceptance-suite model** — which model the offline acceptance suite runs the pipeline against. | The suite drives the real harness end to end — the fetch tool, the file tools, the grader, the triggers, the analyst, and the apply step — with model responses the suite controls; whatever is injected must support native tool calling and the structured outputs the grader and analyst return. Exercised by AC2, AC12, AC26, AC28, AC34. | The scripted stand-in models declared in §5 (`scripted_models.py`): honestly labelled fakes whose per-role responses follow a deterministic policy. Branch: the model is the keyed dependency, so the stand-in is the lightest realization that keeps every stage exercisable with no key — in-process code inside the app, adding no dependency beyond the §2 pins (lighter than tier 1 of the realization tiers, which rank substitute dependencies; this adds none). | (a) scripted stand-ins (§5); (b) the live platform model through the course's provider, in this lab reached through the ambient `OPENAI_API_KEY`/`OPENAI_BASE_URL` so choosing it costs no setup here (course default — the course ran the review agent and grader on `openai:gpt-5.4-mini` and the analyst on `openai:gpt-5.5`; those ids are provenance, the role models are set at the gate's checklist, R20). Criteria that exercise only the Default and do not apply under (b) — every exact-value assertion the scripted policies of §5 produce: AC2's step-1 position of the fetch call; AC3's three identical fetch calls; AC4's `turns` 12 and all-fetch turns; AC5's `turns` 7; AC6's counts, two-sentence Summary and one-write-four-edits tally; AC7's exact `stage_order`; AC9 (the tamper attempt is the scripted review model's); AC12–AC14's pass-by-pass verdicts, snapshot contents and `turns` 9; AC15 (the stubborn agent is scripted); AC16 (the grader error is the scripted grader's); AC18's `2 grading pass(es)` banner; AC20's Confirmed Facts count of 4; AC22's entry and row tallies; AC24, AC26, AC27, AC29 and AC30's exact summaries, proposal fields, pass counts and verdict; AC41 (the planted near-miss is scripted); AC42's equal counts. What stands under (b) is each of those criteria's structural assertion — a terminal status from the contract's enum, three criteria in rubric order with a gap on every failure, the report's five sections, the pages, versions, comments, refusals and records — which AC38 states for a live run, and the criteria that never touch a model's choices: AC1, AC8, AC10, AC11, AC17, AC19, AC21, AC23, AC25, AC28, AC31–AC33, AC35–AC37, AC39, AC40. | Live models make every criterion non-deterministic and slow and tie the completion gate to the proxy; the stand-ins make the suite exact but cannot judge prose quality — the `live`-tagged criteria (AC38) cover that. | course+learner |

## Environment Resolutions

This spec is generated for the **coding-agent-lab** environment. All six learner-context dimensions were derived from the course first and then resolved against the lab — resolved, not skipped. Two course-owned rows also leave the Ledger through this table because every alternative they offered is untakeable here.

| Dimension | Resolution | Where the Invariant lives now |
|---|---|---|
| project | **ANSWERED** — the lab fixes the assignment: the course's example shape (the requirements review agent wrapped in all four loops, on a simulated tracker and wiki) served as the lab's one-server app | spec §1 Objective. Invariant empty. |
| data/inputs | **ANSWERED** — inputs are seeded into the workspace: the authored requirement documents and instruction versions of §5 | spec §5 fixture corpus. Invariant empty. |
| goal | **ANSWERED** — the lab fixes what "working" means: a complete five-section report that satisfies all three rubric criteria, and a learning pass that lifts first-attempt pass rates to all-pass with no revisions | spec §1 + AC12–AC15, AC24, AC29. Invariant empty. |
| model/provider | **CONSTRAINED** — the built app needs an LLM, so: platform models only, keys and base URLs read from the environment, never asked for | Business rule R20 (+ §2, CTX-D), exercised by AC34 (offline) and AC38 (`live`). The derived invariant — native tool calling plus structured outputs — lives in R20 and in row RR1's Invariant, exercised through the scripted stand-in by AC2, AC12, AC26 and live by AC38. The course's three argued model-tiering trade-offs (grader on a different model; analyst on a stronger model; review model matched to task complexity) become body levers under R9, R17 and R20 (the §4 body-levers list) with Ask-First entries. |
| environment | **ANSWERED** — the container | spec §2 + the Runtime (lab) section. Capability invariants moved to rules: a confined per-run writable filesystem (R6, R7: AC8–AC11), run history that survives a process restart (R22: AC37), the course's Python floor (§2 interpreter row; R25, exercised by AC40). |
| scope-boundary | **KEPT** | Ledger row L1. |
| event-source integration surface (course-owned `realization` row) | **ANSWERED — every alternative unavailable here.** The course's shipped realization is the in-app simulated tracker and wiki; its two demonstrated alternatives — a real Slack bot and real Jira/Confluence automations — need tokens, an Atlassian site and a public tunnel the lab does not supply. | Pinned in §2 (event-source row) with the course's provenance; the trigger invariant lives in R12 (AC3, AC19, AC20); the alternatives are §1 `unavailable` items naming the seam. |
| run tracing (course-owned `realization` row) | **ANSWERED — every alternative unavailable here.** The course's default is its own local trace table; its optional hosted alternative (LangSmith) needs an account and key the lab does not supply. | Pinned in R14 (AC22); the hosted alternative is a §1 `unavailable` item naming the seam. |

## 1. Objective

One web app, served by one process on port 4000, that embodies the course's four loops around a requirements review agent: a simulated issue tracker and wiki hold requirement pages and tickets; creating a ticket or editing a page an open ticket links to triggers the agent, which fetches the page, writes a five-section analysis file, is graded against a three-criterion rubric and revised until satisfied, and publishes its report as a new version of an agent-authored page; a Learning page runs the same agent over five seeded documents, has an analyst propose one change to the agent's instructions from the recurring grader corrections, applies it only after a human approves, and shows the before/after verdict. (pattern: CTX-A) The guarantee: every run leaves a complete record (trace, grading passes, file snapshots, instructions version), a human — never the agent — closes a ticket or merges an instruction change, and the offline suite passes with no model key present.

**Deliverable shape** `[environment]`: one server on port 4000 serving both the page and its API — the lab's preview pane is the only view of the running app, so the course's notebooks and script are not the deliverable; this served app is.

**Adapting this beyond the lab.** Project: the assignment is fixed here; elsewhere it is the learner's own tracker and documents (§1). Data/inputs: §5's fixture corpus is seeded here; elsewhere real pages and tickets replace it. Goal: "working" is fixed here as the rubric plus the learning-pass outcome (§1, AC12–AC15, AC24, AC29); elsewhere the rubric is the learner's. Model/provider: R20 reads the lab's `OPENAI_API_KEY`/`OPENAI_BASE_URL` and the three role variables; elsewhere this returns to a Ledger row with the course's provider and model ids as its default. Environment: §2 and the Runtime (lab) section describe the container; elsewhere the port, the venv rule and the preview rules are the learner's. Event source and tracing: pinned here (§2, R14); elsewhere both return as Ledger rows offering the real integrations and hosted tracing.

### Not Included

Each item carries its handling tag for the scope-boundary gate (row L1).

1. **Real Slack bot integration** — `unavailable`: needs a Slack app, an app-level token and a bot token the lab does not supply. Seam: the trigger function R12 names, called from an inbound-message handler instead of the in-app forms.
2. **Real Jira and Confluence (Atlassian) automations** — `unavailable`: needs an Atlassian site, an API token and a public tunnel for webhooks. Seam (the course names it): swap the in-app store's page and ticket lookups for the Atlassian REST APIs and call the same trigger function from a webhook endpoint; nothing about the agent or the loops changes.
3. **Hosted trace viewing (LangSmith)** — `unavailable`: needs an account and API key. Seam: the harness turns it on from three environment variables (`LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`) with no code change; the local trace rows (R14) stay either way.
4. **A human acting as the grader** — `unavailable`: the offline suite is the completion gate and cannot wait on a person. Seam: row D2's invariant admits it; a grader that pauses for a human verdict would replace the LLM grader behind the same interface.
5. **Scheduled (time-based) triggers** — `named-never-built`: Lesson 2 names scheduled runs beside event triggers; the course built only event triggers. Buildable, but this spec supplies no parameters and no acceptance criteria for it.
6. **Memory consolidation as a learning-loop target** (user preferences persisted across runs) — `named-never-built`: Lesson 2 names it as the second category of harness improvement; the course built only instruction changes. Buildable, but this spec supplies no parameters and no acceptance criteria for it.
7. **Applying harness changes that target tools, the grader or configuration** — `named-never-built`: a proposal may name those targets (§3 `HarnessChange.target`), and R18 refuses to auto-apply them; building an applier for them is unspecified here.
8. **Delegation to subagents, a code interpreter or sandbox, summarization and context offloading** — `named-never-built`: pillars of the harness the course names (Lesson 3) and never exercises. Buildable, but this spec supplies no parameters and no acceptance criteria for them.
9. **Human approval before individual sensitive tool calls inside the agent loop** — `named-never-built`: Lesson 2 names it as the first oversight placement; the course's built approvals are the ticket close (R13) and the instruction change (R18). Buildable, but this spec supplies no parameters and no acceptance criteria for it.
10. **A skills directory for the review agent** — `owned-by-row D1`.
11. **A deterministic (code) grader** — `owned-by-row D2`.
12. **Running the acceptance suite against the live model** — `owned-by-row RR1` (the `live` criteria exist either way).
13. **The poet agent of the primer** (Lesson 3's own project) — `unavailable` in row L1's sense (cannot be restored in this lab): a different project the course built as its Lesson 3 example, not a deliverable here; the lab fixes the assignment (Environment Resolutions, project), so no gate answer can bring it back. Its skills layout is what row D1's option (b) offers for the review agent.
14. **Grafting the loops onto an existing codebase** — `unavailable`: outside the delivered build mode.
15. **A per-model price table beyond the course's two entries** — `restorable`: the compare view reports token estimates and a cost that is 0 for any model id outside the course's table (R19); extending the table is additive and owned by no row.
16. **Free-text assignees and authors** — `restorable`: the fixed cast of five names (§5) stands in for an account directory, as in the course; free text is additive.
17. **WebSocket-based live progress** — `unavailable` `[environment]`: the preview proxies HTTP only; streaming HTTP responses are allowed.
18. **Any UI polish beyond the pages and facts §3 and §5 name** — `restorable`: the pages must show the listed facts; styling is the build's choice.

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Interpreter | Python 3, course floor **≥ 3.12** (`requires-python = ">=3.12"`; the course says 3.11 fails while building its numeric packages) | `[environment]` The container's minor version is not stated: the build agent runs `python3 --version` first, records the output in `README.md`, and stops with a report if any course-pinned package below refuses the interpreter — never assume the floor is met. |
| Virtual environment | `python3 -m venv --system-site-packages .venv` | `[environment]` Reuses the preinstalled stack for unpinned packages. Where a course pin and a preinstalled copy differ (`openai`, `python-dotenv`), **the course pin wins inside the venv**. Batch the whole install into one early `pip install` and announce its wall-clock cost before running it. |
| Agent harness | `deepagents==0.7.11` | **Course-pinned** (its lock file resolves exactly this version; the project file's floor is `>=0.7.11`). The course's install situation: floors in `pyproject.toml`/`requirements.txt`, exact resolutions in `uv.lock`; this spec pins the lock's resolutions (the companion and token-estimate rows follow the same rule). Era-specific names: CTX-D. Provides the deep-agent constructor, the confined filesystem backend and its file tools, filesystem permissions, the rubric (grader) middleware and structured responses. |
| Harness companions | `langchain==1.3.18`, `langchain-core==1.6.1`, `langchain-openai==1.6.0`, `langgraph==1.2.11`, `pydantic==2.13.5`, `openai==3.6.0`, `python-dotenv==1.2.3` | **Course-pinned** — each is the version the course's lock file resolved (floors in its project file: `langchain>=1.3.14`, `langchain-core>=1.5.0`, `langchain-openai>=1.4.0`, `langgraph>=1.2.9`, `pydantic>=2.13.4`, `openai>=2.47.0`, `python-dotenv>=1.2.2`), pinned by the harness row's rule. |
| Token estimate | `tiktoken==0.14.0` (optional) | Course-pinned (lock); the course's own estimate falls back to length÷4 when the package is absent, and this build may take the fallback to save install time (R19). |
| Web server | FastAPI + uvicorn, the preinstalled copies, versions unpinned by this spec | `[environment]` Zero-install choice. The course served its app with Flask (floor `>=3.1.3`, no lock entry — unpinned by the course); the server framework is not the taught pattern, so the preinstalled server is pinned on zero-setup grounds and Flask is recorded as the course's choice. |
| Persistent store | JSON files under an app-owned `data/` directory, one list per collection (`pages`, `tickets`, `runs`) plus instruction versions as files and one directory per batch (`data/batches/<label>/`, R16) | Course default (its app keeps three plain JSON lists "a learner can open directly"). Realization tier: **tier 1 — ships with the language's standard distribution** (`json`); tier 1 satisfies the invariant — durable across restarts (R22), versioned pages, complete run records — at the declared scale (a handful of pages, tens of runs), so no higher tier is warranted; `sqlite3` is also tier 1 and would qualify, and the course's own choice wins among equals. Not a Ledger row: keyless, never argued, structurally identical across alternatives. |
| Event source | The in-app simulated tracker and wiki: forms and API calls on this server fire the trigger (R12) | Pinned by the Environment Resolutions table (course default — the course's shipped code; its real Slack/Atlassian alternatives are §1 items 1–2). |
| Run tracing | Local trace rows inside each run record (R14) | Pinned by the Environment Resolutions table; hosted tracing is §1 item 3. |
| Deliverable port | **4000**, bound to `0.0.0.0` | `[environment]` The course ran its app on port 5050; the lab previews only 4000 (R21). |
| Model mode switch | `MODEL_MODE` = `scripted` or `live`; unset means `scripted` | `scripted` injects the §5 stand-ins (row RR1); `live` builds the course's provider client. |
| Secrets and model roles | Environment variables only, never hardcoded, never asked for: the app reads **`OPENAI_API_KEY` and `OPENAI_BASE_URL`** (the course's provider is OpenAI through `langchain-openai`); **`ANTHROPIC_API_KEY` and `ANTHROPIC_BASE_URL`** are present in the container and **unread**; **`REVIEW_MODEL`, `GRADER_MODEL`, `ANALYST_MODEL`** name the platform model per role and are set by the build agent when it writes `resolved-decisions.md` (R20) | `[environment]` The platform's model set is not enumerated; the course's own ids (`openai:gpt-5.4-mini`, `openai:gpt-5.5`) are provenance only and are never assumed to be served. |
| Declared drop | `pandas`, `matplotlib`, `seaborn`, `numpy`, `jupyter`, `ipykernel`, `mistune`, `langsmith` | Notebook rendering and hosted-tracing dependencies of the course; nothing in the served app needs them. |

## 3. Input/Output Contracts

All API paths are relative to the served page (`api/...`, never `/api/...` — R21). The objects below are the app's storage and API shapes; the schemas carry the invariants.

| Endpoint (relative) | Method | Effect |
|---|---|---|
| `api/health` | GET | `{model_mode, python_version, model_roles{review,grader,analyst}, instructions_version}` |
| `api/pages` | GET / POST | list pages / create a requirement page `{title, body, author}` (author from the fixed cast) |
| `api/pages/{id}` | GET | page with all versions (`?v=n` selects one body) |
| `api/pages/{id}/versions` | POST | save a new version `{body, author}` of a requirement page; re-runs every open linked ticket (R12); report pages are not editable here (400) |
| `api/pages/{id}/compare?a=&b=` | GET | `CompareVersions` |
| `api/tickets` | GET / POST | list / create `{title, description, linked_page_id, assignee}` — creation runs the agent (R12) |
| `api/tickets/{key}` | GET | ticket with its runs and linked report page |
| `api/tickets/{key}/rerun` | POST | manual run; optional `{fetch_failures, rubric_iterations}` (R2, R9) |
| `api/tickets/{key}/close` | POST | human marks Done (R13) |
| `api/runs/{run_id}` | GET | `AnalysisRun` |
| `api/instructions` | GET | all instruction versions; `api/instructions/{n}` one |
| `api/batches` | POST `{label}` | run every batch document under the current instructions (R16); GET `api/batches/{label}` returns `BatchSummary` + runs |
| `api/batches/{label}/propose` | POST | run the analyst; returns `{change: HarnessChange, proposal_markdown, trace: TraceStep[]}` — `trace` is the analyst's own run (model turns and tool results, as R14 records them for a review run) (R17) |
| `api/batches/{label}/apply` | POST `{approved: true}` | human approval; applies the stored change (`proposal_<label>.json`, R17), creates the next instructions version (R18) |
| `api/compare?before=&after=` | GET | `CompareResult` (R19) |

Pages the server must render (any client-side framework or server templates; outcome-level): a **Board** (tickets: key, title, assignee, status; create-ticket form), a **Ticket** page (status, linked page and its current version, Re-run and Mark Done buttons hidden once Done, activity comments, latest run with its grading passes and trace rows, the "What changed since the previous run" table, run history), a **Pages** list (requirement pages, analysis reports, create-page form), a **Page** view (chosen version, source-of-truth vs agent-authored banner, edit form on requirement pages only, version history with compare links), a **Compare** view, and a **Learning** page (run batch, batch overview, first-attempt grid, recurring gaps grouped by criterion, propose, proposal and structured change, Approve & apply, compare verdict, instruction versions).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$defs": {
    "Person": { "type": "string", "enum": ["Avery (Product Manager)", "Blake (Eng Lead)", "Casey (QA Lead)", "Devon (Backend Engineer)", "Emery (Frontend Engineer)", "Unassigned"] },
    "PageVersion": {
      "type": "object", "required": ["n", "author", "timestamp", "body"],
      "properties": { "n": {"type": "integer", "minimum": 1}, "author": {"type": "string"}, "timestamp": {"type": "string"}, "body": {"type": "string", "minLength": 1} }
    },
    "RequirementPage": {
      "type": "object", "required": ["id", "kind", "title", "linked_ticket", "versions"],
      "properties": {
        "id": {"type": "string", "pattern": "^page-[a-z0-9-]+$"},
        "kind": {"type": "string", "enum": ["requirement", "analysis_report"]},
        "title": {"type": "string"},
        "linked_ticket": {"type": ["string", "null"]},
        "versions": {"type": "array", "items": {"$ref": "#/$defs/PageVersion"}}
      },
      "allOf": [
        { "if": {"properties": {"kind": {"const": "requirement"}}}, "then": {"properties": {"linked_ticket": {"type": "null"}, "versions": {"minItems": 1}}} },
        { "if": {"properties": {"kind": {"const": "analysis_report"}}}, "then": {"properties": {"linked_ticket": {"type": "string"}, "id": {"pattern": "^page-analysis-[a-z]+-[0-9]+$"}, "versions": {"items": {"properties": {"author": {"const": "Requirements Review Agent (bot)"}}}}}} }
      ]
    },
    "Ticket": {
      "type": "object", "required": ["key", "title", "description", "linked_page_id", "assignee", "status", "comments", "created_at", "last_analyzed_version", "last_run_id"],
      "properties": {
        "key": {"type": "string", "pattern": "^REQ-[0-9]+$"},
        "title": {"type": "string"}, "description": {"type": "string"},
        "linked_page_id": {"type": "string"},
        "assignee": {"$ref": "#/$defs/Person"},
        "status": {"type": "string", "enum": ["Open", "Analysis Ready", "Done"]},
        "comments": {"type": "array", "items": {"type": "object", "required": ["author", "text", "timestamp"]}},
        "created_at": {"type": "string"},
        "last_analyzed_version": {"type": ["integer", "null"]},
        "last_run_id": {"type": ["string", "null"]}
      }
    },
    "TraceStep": {
      "type": "object", "required": ["step", "actor", "action", "detail"],
      "properties": { "step": {"type": "integer", "minimum": 1}, "actor": {"type": "string", "enum": ["Model reasoning", "Tool"]}, "action": {"type": "string"}, "detail": {"type": "string"} }
    },
    "Criterion": {
      "type": "object", "required": ["name", "passed"],
      "properties": { "name": {"type": "string", "enum": ["completeness", "clarity", "depth"]}, "passed": {"type": "boolean"}, "gap": {"type": "string"} },
      "if": {"properties": {"passed": {"const": false}}}, "then": {"required": ["gap"], "properties": {"gap": {"minLength": 1}}}
    },
    "GradingPass": {
      "type": "object", "required": ["iteration", "result", "explanation", "criteria", "analysis_markdown", "tool_calls"],
      "properties": {
        "iteration": {"type": "integer", "minimum": 1},
        "result": {"type": "string", "enum": ["satisfied", "needs_revision", "grader_error"]},
        "explanation": {"type": "string"},
        "criteria": {"type": "array", "items": {"$ref": "#/$defs/Criterion"}},
        "analysis_markdown": {"type": "string"},
        "tool_calls": {"type": "array", "items": {"type": "object", "required": ["name", "args"]}}
      },
      "allOf": [
        { "if": {"properties": {"result": {"const": "grader_error"}}}, "then": {"properties": {"criteria": {"maxItems": 0}}}, "else": {"properties": {"criteria": {"minItems": 3, "maxItems": 3}}} },
        { "if": {"properties": {"result": {"const": "satisfied"}}}, "then": {"properties": {"criteria": {"items": {"properties": {"passed": {"const": true}}}}}} },
        { "if": {"properties": {"result": {"const": "needs_revision"}}}, "then": {"properties": {"criteria": {"contains": {"properties": {"passed": {"const": false}}}}}} }
      ]
    },
    "Message": {
      "type": "object", "required": ["type", "content", "tool_calls", "tool_call_id", "status"],
      "properties": { "type": {"type": "string"}, "content": {"type": "string"}, "tool_calls": {"type": "array", "items": {"type": "object", "required": ["name", "args"]}}, "tool_call_id": {"type": ["string", "null"]}, "status": {"type": ["string", "null"]} }
    },
    "AnalysisRun": {
      "type": "object",
      "required": ["id", "ticket_key", "requirement_page_id", "requirement_version", "report_page_id", "report_version", "instructions_version", "instructions", "model_mode", "model", "rubric", "rubric_iterations", "fetch_failures", "turn_cap", "status", "turns", "counts", "summary_words", "stage_order", "in_order", "missing", "trace", "messages", "grading", "analysis_markdown", "timestamp"],
      "properties": {
        "id": {"type": "string", "pattern": "^[0-9a-f]{8}$"},
        "ticket_key": {"type": "string"}, "requirement_page_id": {"type": "string"},
        "requirement_version": {"type": "integer"}, "report_page_id": {"type": ["string", "null"]}, "report_version": {"type": ["integer", "null"]},
        "instructions_version": {"type": "integer", "minimum": 1}, "instructions": {"type": "string", "minLength": 1},
        "model_mode": {"type": "string", "enum": ["scripted", "live"]}, "model": {"type": "string"},
        "rubric": {"type": "string"}, "rubric_iterations": {"type": "integer", "minimum": 0}, "fetch_failures": {"type": "integer", "minimum": 0},
        "turn_cap": {"type": "integer", "enum": [12, 40]},
        "status": {"type": "string", "enum": ["satisfied", "max_iterations_reached", "grader_error", "finished", "turn_limit_reached"]},
        "turns": {"type": "integer", "minimum": 1},
        "counts": {"type": "object", "required": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions"], "additionalProperties": false, "properties": {"Confirmed Facts": {"type": "integer"}, "Ambiguities": {"type": "integer"}, "Clarification Questions": {"type": "integer"}, "Assumptions": {"type": "integer"}}},
        "summary_words": {"type": "integer", "minimum": 0},
        "stage_order": {"type": "array", "items": {"type": "string", "enum": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"]}},
        "in_order": {"type": "boolean"}, "missing": {"type": "array", "items": {"type": "string"}},
        "trace": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/TraceStep"}},
        "messages": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/Message"}},
        "grading": {"type": "array", "items": {"$ref": "#/$defs/GradingPass"}},
        "analysis_markdown": {"type": "string"}, "timestamp": {"type": "string"}
      },
      "allOf": [
        { "if": {"properties": {"rubric_iterations": {"const": 0}}}, "then": {"properties": {"grading": {"maxItems": 0}, "status": {"enum": ["finished", "turn_limit_reached"]}}}, "else": {"properties": {"status": {"enum": ["satisfied", "max_iterations_reached", "grader_error", "turn_limit_reached"]}, "turn_cap": {"const": 40}}} },
        { "if": {"properties": {"rubric_iterations": {"const": 0}}}, "then": {"properties": {"turn_cap": {"const": 12}}} },
        { "if": {"properties": {"status": {"const": "turn_limit_reached"}}}, "then": {"properties": {"missing": {"minItems": 1}, "grading": {"maxItems": 0}}} }
      ]
    },
    "BatchSummary": {
      "type": "object", "required": ["label", "model", "instructions_version", "runs", "graded", "grader_errors", "first_attempt", "revisions_needed", "documents"],
      "properties": {
        "label": {"type": "string"}, "model": {"type": "string"}, "instructions_version": {"type": "integer"},
        "runs": {"type": "integer"}, "graded": {"type": "integer"}, "grader_errors": {"type": "integer"},
        "first_attempt": {"type": "object", "required": ["completeness", "clarity", "depth"], "additionalProperties": {"type": "object", "required": ["passed", "total", "pass_rate"], "properties": {"passed": {"type": "integer"}, "total": {"type": "integer"}, "pass_rate": {"type": ["number", "null"]}}}},
        "revisions_needed": {"type": "integer"},
        "documents": {"type": "array", "items": {"type": "string"}}
      }
    },
    "HarnessChange": {
      "type": "object", "required": ["target", "issue", "recurrence", "evidence", "section", "change", "rejected"],
      "properties": {
        "target": {"type": "string", "enum": ["prompt", "tool", "grader", "configuration"]},
        "issue": {"type": "string", "minLength": 1}, "recurrence": {"type": "string", "minLength": 1},
        "evidence": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        "section": {"type": "string"}, "change": {"type": "string"},
        "rejected": {"type": "array", "items": {"type": "string"}}
      },
      "if": {"properties": {"target": {"const": "prompt"}}}, "then": {"properties": {"section": {"pattern": "^#{1,6} .+"}, "change": {"minLength": 1}}}
    },
    "CompareResult": {
      "type": "object", "required": ["verdict", "criteria", "runs", "revisions_needed", "attempts", "input_tokens", "output_tokens", "cost_usd", "improved", "regressed"],
      "properties": {
        "verdict": {"type": "string", "enum": ["regression", "success", "partial", "no effect"]},
        "criteria": {"type": "object", "additionalProperties": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "integer"}}},
        "runs": {"type": "integer"},
        "revisions_needed": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "integer"}},
        "attempts": {"type": "array", "items": {"type": "integer"}}, "input_tokens": {"type": "array", "items": {"type": "integer"}}, "output_tokens": {"type": "array", "items": {"type": "integer"}}, "cost_usd": {"type": "array", "items": {"type": "number"}},
        "improved": {"type": "array", "items": {"type": "string"}}, "regressed": {"type": "array", "items": {"type": "string"}}
      },
      "allOf": [
        { "if": {"properties": {"regressed": {"minItems": 1}}}, "then": {"properties": {"verdict": {"const": "regression"}}} },
        { "if": {"properties": {"verdict": {"const": "success"}}}, "then": {"properties": {"regressed": {"maxItems": 0}, "revisions_needed": {"items": false, "prefixItems": [{"type": "integer"}, {"const": 0}]}}} }
      ]
    },
    "CompareVersions": {
      "type": "object", "required": ["page_id", "a", "b", "diff", "run_a", "run_b"],
      "properties": { "page_id": {"type": "string"}, "a": {"type": "integer"}, "b": {"type": "integer"}, "diff": {"type": "array", "items": {"type": "string"}}, "run_a": {"type": ["object", "null"]}, "run_b": {"type": ["object", "null"]} }
    }
  }
}
```

**The report file** (`/analysis.md` in the run workspace; `AnalysisRun.analysis_markdown`) is Markdown with this fixed structure, in this order: a first line `# Requirements Analysis`, then exactly five level-2 headings `## Confirmed Facts`, `## Ambiguities`, `## Clarification Questions`, `## Assumptions`, `## Summary`. The four list sections hold one bullet per entry; every Ambiguities bullet starts with the quoted clause in bold (`- **"<exact clause>"**`) followed by an indented line beginning `Reason:`; after the instruction change of §5 (version 2) each Ambiguities bullet also carries indented lines beginning `Resolved by:` and `Edge case:`. The Summary is prose of two or three sentences. `counts` covers the four list sections only; the Summary is reported as `summary_words`.

**The rubric** (`AnalysisRun.rubric`, fixed in this build) is three lines, one per criterion, each `- <name>: <threshold>`, in the order completeness, clarity, depth: completeness — every clause of the requirement document is addressed somewhere in the analysis; clarity — every bullet in the Ambiguities section has an indented `Resolved by:` line naming the specific fact or decision that would settle it; depth — every bullet in the Ambiguities section has an indented `Edge case:` line naming a concrete production failure the ambiguity could cause. The criterion names are parsed from these lines (the text before the first colon) and are the only names a grading pass may carry.

## 4. Business Rules

Labels: *course-demonstrated* (traceable to the materials, with a CTX anchor), *project hardening* (this spec's addition), `[environment]` (lab-imposed). A rule carrying one label may hold a sentence tagged with another; the tag covers that sentence only.

1. **R1 — The agent is never handed the document; it fetches by ticket.** *course-demonstrated* (CTX-A, CTX-C). A run's opening message names only the ticket key; the agent obtains the text by calling the `fetch_requirement` tool, which resolves the ticket's linked page at its current version; the run record stores the provenance of that text as `requirement_page_id` + `requirement_version` (the text itself survives as the fetch tool's result among `messages`, R14). Prevents an agent that only works when the document is pasted into the prompt. → AC2
2. **R2 — Transient tool failures are retried with identical arguments.** *course-demonstrated* (CTX-B1). The fetch tool can return an error string instead of the document; the agent's instructions tell it to call the exact same tool again with the same arguments, and every attempt appears as its own trace step. The simulated failure count is a per-run knob `fetch_failures`: a manual re-run defaults to **2** — the value the Lesson 4 narration states for the lesson that introduces the retry ("two times of failure before the requirement is fetched successfully"), chosen by the lever-value rule's first branch because the course's helper default (0, "a clean fetch") contradicts it (CTX-C); event-triggered and batch runs pass **0**, the course's own configuration for those paths ("here it only adds turns and noise"). Post-build lever; no gate question. → AC3
3. **R3 — The model-call cap is a safety net, and the stop reason is named.** *course-demonstrated* (CTX-B2). The run ends normally when the model finishes with a plain message after the Summary stage; the cap exists for the path where that never happens (an agent retrying past the point where retrying makes sense). Cap = **12** model calls when `rubric_iterations` is 0 (the course's agent-loop setting) and **40** when verification is on (the course's setting wherever a grader can send work back) — two configs, each cited, never one "default". When the cap ends the run with the report incomplete — under either cap — the run ends at that point with no grading pass, the last trace row's action reads `Stops: turn limit of <cap> reached`, the status is `turn_limit_reached`, and `missing` lists the unfilled sections. When the model ends with a plain message, the model row for that message carries the action `Finishes the review`; a finished agent-only run has status `finished`. → AC4, AC5
4. **R4 — The deliverable is a file with a fixed shape.** *course-demonstrated* (CTX-A, CTX-B4). The agent builds `/analysis.md` through the file tools — one write for the skeleton with Confirmed Facts filled, then one edit per remaining section — exactly as §3's report structure states; the Summary is two or three sentences; `counts` is bullets per list section and excludes the Summary (`summary_words` carries it). Output lives in the file, never only in the conversation. → AC6
5. **R5 — Stage order is requested, recorded, never enforced.** *course-demonstrated* (CTX-C). The instructions ask for the five stages in order, one tool call per turn; the harness records which sections each successful write or edit of the *first attempt* actually filled (`stage_order` — the stages before any grader feedback; a revision edit is not stage work; a section counts only when the same call supplies text under its heading, so writing the empty skeleton claims nothing), reports `in_order` (the recorded order is a subsequence of the canonical order) and `missing` (list sections with no bullet, plus Summary when empty). Filling two sections in one edit is not a violation; filling one out of order, or leaving one empty, is — reported, never enforced: no contract constraint ties `in_order` or `missing` to a grading status, so a run graded `satisfied` out of order is recorded as exactly that, and AC7 asserts the values the scripted run of AC5 produces. → AC7
6. **R6 — The instructions are a file the agent reads every run and can never write.** *course-demonstrated* (CTX-A, CTX-B5, CTX-B6); its last sentence is a separate `[environment]` constraint. Each run's confined workspace holds `memories/AGENTS.md`, seeded from the app's current instructions version and loaded into the agent's context at the start of the run; writes under `/memories/**` are denied by harness permission, not by instruction alone; a workspace without the file makes the run refuse before any model call, with an error naming the missing path, because a harness that silently ignores a missing memory file produces a plausible bad review. `[environment]` The baseline instructions and every run workspace live under app-owned subfolders; the build never authors or edits an `AGENTS.md` at the workspace root (the IDE rewrites that file at boot and the guidance is lost). → AC8, AC9, AC10
7. **R7 — One fresh, confined workspace per run.** *course-demonstrated* (CTX-B7). Every run gets a new directory the agent sees as `/` with paths above it unreachable, seeded with the instructions file alone under row D1's default and with the `skills/` directory beside it under D1 option (b), so two runs never see each other's leftover report; the directory is deleted when the run finishes, and the report survives only as a report-page version and inside the run record. → AC11
8. **R8 — The grader judges the file, literally.** *course-demonstrated* (CTX-B4). The grader holds a read-only file tool and must read `/analysis.md` before judging; it judges only what the file contains, never how the conversation reads; it passes a criterion only when it can quote the satisfying text; where a criterion names a labelled line, only that exact label counts; a coverage criterion is checked item by item. Each pass returns a result and one entry per criterion in rubric order with a gap on every failure, and records the grader's own tool calls in order (`GradingPass.tool_calls`, so the read is evidenced, not assumed). A verdict outside the contract's enum is recorded as `grader_error` (*project hardening*). → AC12, AC13, AC41
9. **R9 — Verification loop: retry with feedback up to a budget, and name the exit.** *course-demonstrated* (CTX-A, CTX-B3). After the agent stops, the grader runs; on `needs_revision` its feedback is injected into the same conversation and the agent revises; the loop ends on `satisfied` or when the budget is spent. Budget `rubric_iterations` = how many times the grader may send work back; default **3** — the Lesson 5 narration's stated value and the course's batch setting — chosen by the lever-value rule's first branch over the course's event-driven app, which used **2** (CTX-C); 0 turns the run into the plain agent loop (the course says so; the degenerate case). Status: `satisfied` when a pass satisfies; `max_iterations_reached` when the budget is spent without one — computed by the app from the budget and the pass list, because the final grading pass still says `needs_revision` and only the exit reason distinguishes "satisfied" from "ran out of tries". Model tiering is a body lever here: the course ran agent and grader on the same model and called a separate grader model "a common production choice" (Lesson 5); `GRADER_MODEL` may differ from `REVIEW_MODEL` (Ask First). → AC5, AC13, AC14, AC15, AC38
10. **R10 — A grader failure is evidence of nothing.** *course-demonstrated* (CTX-B11). When the grader errors, the pass is recorded with result `grader_error` and no criteria, the run status is `grader_error`, and batch statistics count that run under `grader_errors` and exclude it from every denominator — a batch with errors reports a weaker result rather than averaging them away. → AC16, AC17
11. **R11 — The agent reads the requirement and writes somewhere else.** *course-demonstrated* (CTX-B14). The requirement page is the source of truth: no run adds a version to it. The report is written as a new version of a separate page of kind `analysis_report` titled `Analysis Report — <ticket key>`, authored by the bot author, whose body begins with a banner stating the ticket, the requirement version analysed, the verification status and the number of grading passes, followed by the report file verbatim. → AC18
12. **R12 — Triggers.** *course-demonstrated* (CTX-A, CTX-B15, CTX-B16). The agent runs when (a) a ticket is created, (b) a requirement page is saved while one or more tickets that link to it are not Done — every such ticket re-runs, and the save response names them — and (c) a human presses Re-run. A save with no open linked ticket re-runs nothing and says so. Triggered runs use `fetch_failures` 0 and `rubric_iterations` 3; the manual re-run accepts both as overrides. → AC3, AC19, AC20
13. **R13 — A human, never the agent, decides Done.** *course-demonstrated* (CTX-B13, CTX-B15). A completed run sets the ticket to `Analysis Ready`, records `last_analyzed_version` and `last_run_id`, and adds a bot comment naming the status, the requirement version and the report page; only the close action moves a ticket to `Done`, after which Re-run and Mark Done are not offered and page saves do not re-run it. → AC20, AC21
14. **R14 — Every run is fully recorded, locally.** *course-demonstrated* (CTX-A, CTX-C). The run record keeps every message of the conversation untruncated with full tool-call arguments and tool results (the gap between what the agent was told, what it produced, what it was told afterwards and what it fixed is the evidence the learning loop reads), every grading pass with the file exactly as that pass saw it, the instructions snapshot and version, the trace rows (one `Model reasoning` row per model turn; a turn that calls a tool has its row immediately followed by one `Tool` row holding the result, and a plain reply has no tool row after it, so two `Tool` rows are never adjacent; a tool row's detail is the result text truncated to 220 characters), counts, summary words and status. The trace is recorded locally by the app; no hosted tracing service is contacted. → AC22
15. **R15 — "What changed" shows counts and text together.** *course-demonstrated* (CTX-B12, CTX-C). With two or more runs on a ticket, the ticket page shows the previous and latest run side by side — requirement version, verification status, bullet count per list section — and links to the report page's compare view, which shows the unified diff of the two versions plus the two runs' status and counts, because counts often look alike while the content changed completely. → AC23, AC42
16. **R16 — A batch is every batch document under one instructions version.** *course-demonstrated* (CTX-A, CTX-B8). A batch runs the five batch documents in filename order, each in its own fresh workspace seeded from one instructions version, with `rubric_iterations` 3 and `fetch_failures` 0; it writes, into the batch's own directory `data/batches/<label>/` (the batch store of §2), one run record per document and a `BatchSummary` whose `first_attempt` counts, per criterion by position in rubric order, the graded runs whose first grading pass passed it; `revisions_needed` is the number of graded runs whose first pass failed anything; the instructions text is snapshotted beside the batch. → AC17, AC24, AC25, AC29
17. **R17 — The analyst proposes from evidence and cannot touch it.** *course-demonstrated* (CTX-B8, CTX-B9). The analyst is an agent rooted at a fresh confined workspace whose `/<label>/` directory holds a copy of the batch's files (the run records, `summary.json`, `AGENTS.md`), with read tools and write permission on `/proposal.md` only; it starts from the batch summary to pick the criteria to investigate, quotes evidence from the runs verbatim, reads the instructions so its addition does not repeat them, and returns a `HarnessChange` whose `change` is the literal text to insert. A criterion failing in most runs is a property of the agent; a problem seen in one run is not a pattern and goes under `rejected`. The analyst never applies anything. When it finishes, the app copies `/proposal.md` into the batch directory (`data/batches/<label>/`, R16 — for a registered fixture batch, the app's copy, never the fixture directory) as `proposal.md`, writes `proposal_<label>.md` (the response's `proposal_markdown`: `proposal.md` under a header line naming the label, the instructions version and the timestamp) and `proposal_<label>.json` (the `HarnessChange` — the stored change R18 applies), changes no other file there, and deletes the workspace. Model tiering is a body lever: the course ran the analyst on a stronger model than the agent because reading several full traces and finding what recurs is the job the cheaper model does unreliably (Lesson 7, README); `ANALYST_MODEL` is set per role (Ask First). → AC26, AC27
18. **R18 — Apply only after a human approves, and only by code.** *course-demonstrated* (CTX-B10). A proposed change is applied only through the explicit approval action, which reads the stored change `proposal_<label>.json` (R17); the app inserts `change` at the end of the section `section` names (before the next heading of the same or shallower depth), refuses a `section` that is not found, refuses any `target` other than `prompt` with a message telling the human to read the proposal and decide, and stores the result as the next instructions version, leaving every earlier version intact. New runs use the newest version. → AC28, AC29
19. **R19 — Measure before you believe it.** *course-demonstrated* (CTX-B10). `CompareResult` for two batches: per criterion the pair of first-attempt pass counts; `improved` lists criteria whose count rose, `regressed` those whose count fell; `verdict` is `regression` if anything regressed, else `success` if the after-batch needed no revisions, else `partial` if anything improved, else `no effect`; `runs` is the graded-run count of each batch (both run the same documents) and `attempts` is, per batch, the total number of grading passes over its graded runs — the first attempt plus every revision. Token counts are estimated from the stored conversations (each model call sends the running history, so input is the running total plus the instructions length plus a fixed 120; a tokenizer if installed, else length÷4); cost uses a price table per million tokens holding the course's two entries (`openai:gpt-5.5`: 5.00 in / 30.00 out; `openai:gpt-5.4-mini`: 0.75 / 4.50) and 0 for any other id. → AC30, AC31, AC32, AC33
20. **R20 — Models come from the platform, through the environment.** `[environment]`. The app reads exactly `OPENAI_API_KEY` and `OPENAI_BASE_URL` and sends every live request to that base URL; it never asks the person for a key, never hardcodes one, never guesses other variable names, and never reads `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL` (present, unread). Model ids come from `REVIEW_MODEL`, `GRADER_MODEL` and `ANALYST_MODEL`, which the build agent sets when it writes `resolved-decisions.md` — that checklist carries one "model roles" line with the agent's "(Recommended)" platform model per role, and the person's confirmation of the checklist confirms them. Any injected model must support native tool calling and structured output (the grader verdict, the analyst's change) — the pattern's capability requirement. The app never probes a model-listing endpoint and never asserts a course model id is served. → AC34, AC38, AC39
21. **R21 — One server, port 4000, relative URLs only.** `[environment]`. The app is one process bound to `0.0.0.0:4000` serving the page and `api/*`; every URL the page emits or fetches is relative (`api/tickets`, `pages/x`), never root-absolute (`/api/...`), because the preview is reverse-proxied under a path prefix and a root-absolute path resolves against the IDE; no WebSocket. → AC35, AC36
22. **R22 — The record survives the process.** *project hardening* (the course's app kept flat JSON files on disk; this rule makes the guarantee explicit). Pages, tickets, runs, instruction versions and batches are written to disk on every change and are intact after the server is stopped and started again. → AC37
23. **R23 — Fresh initialization seeds a known scenario.** *course-demonstrated* (CTX-C). On first start with an empty `data/` directory the app creates the three collections, one requirement page (`page-workspace-logo-upload`, version 1 by Avery), one open ticket `REQ-101` linked to it (assignee Blake), no runs, and instructions version 1 — §5 states each text. Later starts never reseed. → AC1
24. **R24 — Scripted mode is fully offline.** *project hardening*. With `MODEL_MODE=scripted` the app constructs no provider client and makes no network request; `api/health` reports the mode; the whole offline suite runs with `OPENAI_API_KEY` unset. → AC34
25. **R25 — The recorded interpreter meets the course floor.** `[environment]` (the floor itself is the course's: §2 interpreter row, CTX-D; the check at build start and its record are the lab's: EF4). The build records the output of `python3 --version` in `README.md` before installing anything; `api/health.python_version` reports the running interpreter's version; both must be ≥ 3.12, and a lower version is a stop-and-report, never a silent continue. → AC40

**Body levers (post-build; no gate question):** `fetch_failures` 2/0 (R2); `rubric_iterations` 3 (R9); grader on a different model (R9); analyst on a stronger model (R17); review model matched to task complexity (Lesson 2's "match the model intelligence to the complexity of the task to optimize cost" — a tiering lever attached to the resolved model dimension, exercised through `REVIEW_MODEL`); the batch size of five documents (a fixture count).

## 5. Acceptance Criteria

### Fixture corpus (declared before use; the build agent never modifies a fixture to pass a test)

All fixtures live under an app-owned `fixtures/` directory. Every fact below is authored for this spec; none is copied from the course.

**Fixed cast** (`Person` enum): Avery (Product Manager), Blake (Eng Lead), Casey (QA Lead), Devon (Backend Engineer), Emery (Frontend Engineer); plus `Unassigned` for tickets created without one. Bot author string: `Requirements Review Agent (bot)`.

**Seed requirement page** `fixtures/seed_page.md` — page id `page-workspace-logo-upload`, title "Workspace Logo Upload — Requirements", version 1 by Avery, body (three clauses after the title line; a clause is a non-empty line after the `REQUIREMENT:` line):

```
REQUIREMENT: Workspace Logo Upload

Admins shall be able to upload a logo for their workspace.

The logo should be stored securely.

The feature should accept common image formats.
```

**Seed ticket** `REQ-101` — title "Review requirements: Workspace Logo Upload", description "Please review the linked requirement for ambiguity before implementation starts.", linked to the seed page, assignee Blake, status Open. Ticket keys are `REQ-<n>`; the next key is one above the highest existing number.

**Batch documents** `fixtures/requirement_docs/` (filename order is batch order; each has the `REQUIREMENT:` title line, then one clause per non-empty line; the bracketed count is how many clauses contain a word from `VAGUE_WORDS` below):

- `01_session_timeout.md` — "REQUIREMENT: Session Timeout Policy" / "Sessions shall expire after a reasonable period of inactivity." / "Users must be warned shortly before expiry." / "Admin sessions should be handled more strictly." / "Expired sessions shall be logged." [3 vague of 4]
- `02_export_scheduler.md` — "REQUIREMENT: Scheduled Report Export" / "Reports shall be exported on a schedule." / "Exports must be delivered through appropriate channels." / "Large exports should be handled efficiently." / "Failed exports must be retried sensibly." / "Export status shall be visible to the requester." [3 of 5]
- `03_invoice_dunning.md` — "REQUIREMENT: Invoice Dunning" / "Overdue invoices shall trigger reminders." / "Reminders must be spaced out appropriately." / "The system should stop reminding after a reasonable number of attempts." / "Disputed invoices should not be reminded." / "Each reminder shall be recorded." [2 of 5]
- `04_team_permissions.md` — "REQUIREMENT: Team Folder Permissions" / "Members shall only see folders they are entitled to." / "Owners must be able to share folders easily." / "Permission changes should apply promptly." / "The system shall record who opened which folder." [2 of 4]
- `05_incident_paging.md` — "REQUIREMENT: Incident Paging Rules" / "Incidents shall page the responsible on-call engineer." / "Unacknowledged pages must escalate quickly." / "Severity should determine how aggressively paging escalates." / "Duplicate incidents should be grouped." / "Paging shall pause during planned maintenance." [3 of 5 — `quickly`, `aggressively`, `planned`]

**Special documents** `fixtures/special_docs/` — requirement texts the tests create as pages (each with a ticket) through the API; the parenthesised marker in the title line is a fixture fact the scripted models key on:

- `stubborn.md` — "REQUIREMENT: Audit Log Retention (STUBBORN)" / "Audit logs shall be kept for a reasonable period." / "Deleting logs early must be handled appropriately." [2 of 2]
- `tamper.md` — "REQUIREMENT: Password Reset (TAMPER)" / "Reset links shall expire quickly." / "Reset emails must be sent securely." [2 of 2]
- `grader_error.md` — "REQUIREMENT: Bulk Import (GRADER-ERROR)" / "Imports shall handle large files efficiently." / "Malformed rows must be reported appropriately." [2 of 2]
- `nearmiss.md` — "REQUIREMENT: Data Export Consent (NEAR-MISS)" / "Users shall consent before large exports." / "Consent records must be stored securely." [2 of 2] — the planted grading-by-resemblance case (CTX-B4): the scripted review model's first attempt writes near-miss labels (`Resolution:`, `Edge-case risk:`) under every Ambiguities bullet, lines that look like the rubric's but are not the exact labels.
- `unlinked.md` — "REQUIREMENT: Holiday Calendar (UNLINKED)" / "Public holidays shall be shown promptly." [1 of 1] — created as a page that no ticket links to; its marker keys nothing, because no run is ever triggered on it (AC20's no-op save).

**`VAGUE_WORDS`** (fixture constant in `scripted_models.py`): reasonable, shortly, strictly, appropriate, appropriately, efficiently, sensibly, easily, promptly, quickly, aggressively, securely, common, large, planned. The "vague word" of a clause is the `VAGUE_WORDS` entry that occurs earliest in the clause's own text, reading left to right (so "Large exports should be handled efficiently." has `large`, not `efficiently`); list order plays no part.

**Instructions version 1** `fixtures/instructions_v1.md` — the agent's initial `AGENTS.md`, authored by the build in its own words to state exactly: the agent turns one requirement document into one report file `/analysis.md`; the procedure in order, one tool call per turn — fetch with `fetch_requirement`, write the skeleton of §3's report structure with only Confirmed Facts filled, then edit in Ambiguities (bold-quoted clause + indented `Reason:` line), Clarification Questions, Assumptions, Summary (two or three sentences); an error result from a tool means calling the same tool again with the same arguments until it succeeds; the requirement document and this file are never modified; after the Summary, reply with one short sentence and call no further tools; review guidance: facts are only what the document states, ambiguities quote the exact clause and say why it is under-specified, questions are what a reviewer needs answered before work starts, assumptions are what a developer would assume if nobody answered. **It deliberately says nothing about `Resolved by:` or `Edge case:` lines** — that gap is the planted recurring failure. Version 1 must not contain the string `Resolved by:`.

**Instruction change text** (the scripted analyst's `change`, authored here): "For every ambiguity bullet, add two more indented labelled lines after the `Reason:` line: `Resolved by:` — the specific fact or decision that would settle the ambiguity; `Edge case:` — one concrete production failure that could happen while it stays unresolved." with `section` = `### Ambiguities` (version 1 must contain that exact heading). Version 2 is version 1 with this text inserted at the end of that section.

**Scripted models** `scripted_models.py` (row RR1's default; honestly a fake — each registers a description beginning "Scripted stand-in for …"). Each implements the harness's chat-model interface and chooses its reply by a deterministic policy over the conversation it is given. **Recorded model string:** in scripted mode every run record and batch summary carries `model` = `scripted` — that one string, whatever the role variables hold (they still show in `api/health.model_roles`); in live mode `model` is the value of `REVIEW_MODEL`. The price table of R19 holds no entry `scripted`, so a scripted-mode batch always costs 0.

- *Scripted review model.* Reads the requirement title and clauses from the latest successful fetch result; an "ambiguous clause" is one containing a `VAGUE_WORDS` entry (whole-word, case-insensitive); the "vague word" of a clause is the entry occurring earliest in the clause's text (as defined beside `VAGUE_WORDS`). Turn policy: (1) if no fetch has succeeded, call `fetch_requirement` with the ticket key named in the opening message; (2) if the last tool result begins with `Error`, repeat the last call with identical arguments — **except** the one tamper attempt below, which is never retried; (3) on a `(TAMPER)` title, the first turn after the successful fetch calls `edit_file` on `/memories/AGENTS.md` once, then the policy continues as if that turn had not happened; (4) after the fetch, `write_file` `/analysis.md` with §3's skeleton and one Confirmed Facts bullet per clause, each the clause verbatim; (5) `edit_file` Ambiguities: one bullet per ambiguous clause — `- **"<clause>"**` then `  Reason: the term "<vague word>" is not defined` — and, **only if the instructions text in context contains `Resolved by:`, or a grader feedback message is present in the conversation**, also `  Resolved by: a stated definition of "<vague word>" for this feature` and `  Edge case: a build that reads "<vague word>" differently from the author fails in production`; on a `(STUBBORN)` title the two lines are never added; on a `(NEAR-MISS)` title, while neither condition holds, the same two lines are written with the labels `Resolution:` and `Edge-case risk:` instead (the exact labels once a condition holds); (6) `edit_file` Clarification Questions: `- What exactly does "<vague word>" mean in "<clause>"?` per ambiguous clause; (7) `edit_file` Assumptions: `- Assume "<vague word>" takes its narrowest reading until confirmed.` per ambiguous clause; (8) `edit_file` Summary: exactly two sentences — `The document states <N> clauses. <M> of them are ambiguous and need clarification before the build starts.`; (9) reply `Review complete: /analysis.md is written.` with no tool call. After grader feedback, the model re-enters at step (5) replacing the whole Ambiguities section (its previous block is unique in the file), then (9).
- *Scripted grader.* On every grading call for a `(GRADER-ERROR)` title it raises an error; otherwise it calls `read_file` on `/analysis.md` and judges that text only: completeness passes iff every clause appears verbatim in the file; clarity iff the Ambiguities section has at least one bullet and, among the indented lines under every bullet, one begins exactly `Resolved by:` (a near-miss label such as `Resolution:` does not count); depth likewise for `Edge case:`; a failing criterion's gap names the missing label (e.g. `missing indented "Resolved by:" line under every Ambiguities bullet`); result `satisfied` iff all pass, else `needs_revision`; the explanation quotes, with its line number, one satisfying line per passing criterion.
- *Scripted analyst.* First attempts `write_file` on `/<label>/summary.json` (denied by permission; it continues), then reads `/<label>/summary.json`, each `/<label>/run_*.json` and `/<label>/AGENTS.md`; a criterion whose first-attempt `pass_rate` is 0.5 or lower is "recurring"; one failing in some but fewer than half of the graded runs is a one-off; it writes `/proposal.md` with the headings `## Summary signal`, `## Evidence`, `## Current instruction`, `## Proposed insertion`, `## Rejected observations`, and returns a `HarnessChange` with `target` `prompt`, `recurrence` `"<k>/<n> runs: <run file names>"` (k = runs whose first pass failed a recurring criterion, n = graded runs), `evidence` = one entry per such run — its run file name, a colon, then that run's first-pass gap text for every recurring criterion it failed, joined by `; ` (so a run failing clarity and depth contributes one entry mentioning both labels), `section` `### Ambiguities`, `change` = the instruction change text above, and `rejected` = one sentence per one-off criterion naming the run(s) and saying a single occurrence is not a pattern.

**Compare fixtures** `fixtures/summaries/<name>/` — eight batch directories forming four pairs, each directory holding a `summary.json` (`BatchSummary` with `model` `scripted`, `instructions_version` 1, 5 runs, 5 graded, 0 errors; `first_attempt` passed counts listed below as completeness/clarity/depth; `revisions_needed` after the dash) and five fixture run files `run_01.json` … `run_05.json` (the shape defined below; each first pass matches the summary): `success_before` 5/0/0 — 5, `success_after` 5/5/5 — 0; `regression_before` 5/5/5 — 0, `regression_after` 5/3/5 — 2; `partial_before` 5/0/0 — 5, `partial_after` 5/5/2 — 3; `no_effect_before` 5/0/0 — 5, `no_effect_after` 5/0/0 — 5. No `AGENTS.md`: `propose` is never called on them.

**Fixture run file** — every `run_*.json` under `fixtures/` is a complete `AnalysisRun` record, valid against §3's schema: `model_mode` `scripted`, `model` `scripted`, `instructions_version` 1 with `instructions` = the version 1 text, `rubric` = §3's rubric, `rubric_iterations` 3, `fetch_failures` 0, `turn_cap` 40, `report_page_id` and `report_version` null, `messages` holding one human entry, `trace` holding one `Model reasoning` row, `grading` holding the first pass the fixture describes and — when that pass is `needs_revision` — one further pass `satisfied`, so `status` follows R9 (`satisfied`, or `grader_error` when the only pass is an error pass); the remaining required fields (`id`, `ticket_key`, `requirement_page_id`, `requirement_version`, `turns`, `counts`, `summary_words`, `stage_order`, `in_order`, `missing`, `analysis_markdown`, `timestamp`) carry schema-valid placeholder values. Registration (the `FIXTURE_BATCHES` hook) validates every run file against the schema and refuses the label, naming the file, when one fails. Token estimates (R19) compute from the single human message; first-attempt statistics read only each run's first pass.

**Grader-error batch fixture** `fixtures/batch_with_error/` — a batch directory with five fixture run files `run_01.json` … `run_05.json` and no `summary.json`: four whose first pass has three criteria (completeness passed; clarity and depth failed) and one whose first pass is `grader_error` with no criteria.

**One-off batch fixture** `fixtures/batch_one_off/` — a batch directory registered under the label `oneoff`: `AGENTS.md` = instructions version 1; `summary.json` with completeness 4/5, clarity 0/5, depth 0/5, revisions_needed 5; five fixture run files `run_01_a.json` … `run_05_e.json` whose first passes fail clarity and depth with gap text naming the missing labels, and `run_03_c.json` additionally fails completeness with gap `clause "Each reminder shall be recorded." is not addressed`.

**Planted changes** `fixtures/changes/` — four complete `HarnessChange` files the suite copies over a batch's stored change (`proposal_<label>.json`) to exercise R18's refusals: `fixtures/changes/target_tool.json`, `fixtures/changes/target_grader.json`, `fixtures/changes/target_configuration.json` (each with its named `target`, `section` `### Ambiguities`, `change` = the instruction change text, authored one-line `issue`/`recurrence`, one `evidence` entry, empty `rejected`) and `fixtures/changes/section_missing.json` (`target` `prompt`, `section` `### Missing`, otherwise the same).

**Edited seed body (version 2)** — the seed body with a fourth clause appended: "Logos must be smaller than 2 MB." (four clauses, two vague); used by AC20.

**Same-count seed body** — the seed body with its second clause reworded to "The logo must be encrypted securely at rest." (still three clauses, still two vague — `securely`, `common` — so every list-section count equals the original run's while the text differs); the planted counts-hide-a-change case (CTX-B12), used by AC42.

**Runaway knob**: a manual re-run with `fetch_failures` 99 — the fetch stand-in errors on every call for that run (the simulated error texts alternate between a `503 Service Unavailable` message and a `request timed out` message, each beginning `Error`).

**Denied file operations in the trace**: the app's trace writer (R14) records the result of a file-tool call whose path the app's own permission rules deny — any write under `/memories/**` by the review agent (R6), any write other than `/proposal.md` by the analyst (R17) — as a `Tool` row with action `Denied by permission: <path>`; the row's detail is the harness's denial text truncated as usual, and the criteria assert the action, never that text, because the denial message belongs to the harness.

**Test hooks** (declared once here; the suite is their only caller, and the pages never use them):

- `FIXTURE_BATCHES` — an environment variable read at startup: comma-separated `label=directory` pairs. Each directory is registered as a batch under that label: at registration the app copies the directory's files into the batch store at `data/batches/<label>/` (replacing any earlier copy under that label) and serves the copy — by `GET api/batches/{label}`, `POST api/batches/{label}/propose` and `api/compare` — without running anything; the fixture directory is never written to, so everything a later call stores (R17's proposal files, R16's computed summary) lands in the copy. A registered batch lacking `summary.json` gets one computed from its run files by R16's summariser at registration, written into the copy; one that has it is read as is. Every run file is validated as the fixture-run-file paragraph states. The suite sets, for example, `with_error=fixtures/batch_with_error,oneoff=fixtures/batch_one_off,regression_before=fixtures/summaries/regression_before,…`.
- `run_review(ticket_key, *, workspace_dir=None, fetch_failures=None, rubric_iterations=None)` in the app module `review_runner.py` — the one function every trigger calls. When `workspace_dir` is given, the run uses that directory as its workspace instead of creating a fresh one (R7's fresh workspace is the default path); the suite passes a directory it prepared, which is how AC10 starts a run on a workspace with no `memories/AGENTS.md`. Unset knobs take R12's trigger values.
- The stored change of a batch is the file `proposal_<label>.json` in its directory (R17). The suite plants a change by copying one of `fixtures/changes/*.json` over that file before calling `apply`.

### Given / When / Then

Unless stated, every criterion runs with `MODEL_MODE=scripted` and `OPENAI_API_KEY` unset. Criteria tagged `live` run only with `MODEL_MODE=live` and the platform variables present.

| # | Given | When | Then |
|---|---|---|---|
| AC1 (R23) | an empty `data/` directory | the server starts | `data/pages.json` holds exactly one page: id `page-workspace-logo-upload`, kind `requirement`, one version (n 1, author Avery, body = seed text); `data/tickets.json` holds exactly `REQ-101` (status Open, assignee Blake, linked to that page, `last_run_id` null); `data/runs.json` is `[]`; `api/instructions` lists exactly version 1 whose text contains `### Ambiguities` and not `Resolved by:`; `api/health` reports `instructions_version` 1 |
| AC2 (R1) | the seeded store | `POST api/tickets/REQ-101/rerun` with `{fetch_failures: 0}` | the run's first `messages` entry of type human names `REQ-101` and does not contain the seed body; trace step 1 is a model call to `fetch_requirement` with argument `REQ-101`; `requirement_page_id` is the seed page and `requirement_version` is 1 |
| AC3 (R2, R12) | the seeded store | `POST api/tickets/REQ-101/rerun` with an empty body | the trace shows three `fetch_requirement` calls with identical arguments, the first two followed by tool rows whose detail begins `Error`, the third by the document; `fetch_failures` is 2 in the record; status `satisfied` |
| AC4 (R3) | the seeded store | rerun with `{fetch_failures: 99, rubric_iterations: 0}` | `turns` is 12, `turn_cap` 12, every model turn is a `fetch_requirement` call, the last trace row's action is `Stops: turn limit of 12 reached`, status `turn_limit_reached`, `grading` is empty, every `counts` value is 0, `missing` lists all five sections |
| AC5 (R3, R9) | the seeded store | rerun with `{fetch_failures: 0, rubric_iterations: 0}` | status `finished`, `grading` empty, `turn_cap` 12, `turns` is 7, the last trace row's action is `Finishes the review`, `missing` is empty |
| AC6 (R4) | AC5's run | its `analysis_markdown` is read | first line `# Requirements Analysis`; exactly five `## ` headings in §3's order; `counts` = Confirmed Facts 3, Ambiguities 2, Clarification Questions 2, Assumptions 2; each Ambiguities bullet begins `- **"` and is followed by an indented `Reason:` line; the Summary has exactly two sentences and `summary_words` > 0; `counts` has no Summary key; the trace shows one `write_file` and four `edit_file` calls |
| AC7 (R5) | AC5's run | the record is read | `stage_order` is exactly `[Confirmed Facts, Ambiguities, Clarification Questions, Assumptions, Summary]`, `in_order` true, `missing` empty |
| AC8 (R6) | AC5's run | the record and the repository are inspected | `instructions` equals instructions version 1 text and `instructions_version` is 1; the run's first system-context message contains that text; the build tree contains no `AGENTS.md` at the workspace root, and the baseline instructions file and every run workspace sit under app-owned subfolders |
| AC9 (R6) | a page created from `tamper.md` and a ticket linked to it | the ticket is created (triggering the run) | the trace contains an `edit_file` call whose path is `/memories/AGENTS.md` followed by a `Tool` row whose action is `Denied by permission: /memories/AGENTS.md` (the §5 denied-operation row); instructions version 1 text is unchanged; the run still ends `satisfied` |
| AC10 (R6) | a directory prepared by the suite with no `memories/AGENTS.md` in it | `run_review("REQ-101", workspace_dir=<that directory>, fetch_failures=0)` is called (the §5 test hook) | it refuses before any model call with an error naming the missing path; no run record is added |
| AC11 (R7) | the seeded store | two consecutive reruns of `REQ-101` with `{fetch_failures: 0}` | the two runs have different ids; neither run's workspace directory exists after completion; the report page `page-analysis-req-101` has exactly two versions, each equal to its run's banner + `analysis_markdown` |
| AC12 (R8) | the seeded store at instructions version 1 | rerun with `{fetch_failures: 0}` | grading pass 1: its `tool_calls` include `read_file` with path `/analysis.md`; `criteria` names are exactly `completeness`, `clarity`, `depth` in that order; completeness passed; clarity failed with a gap containing `Resolved by:`; depth failed with a gap containing `Edge case:`; result `needs_revision`; its `analysis_markdown` snapshot contains no `Resolved by:` line |
| AC13 (R8, R9) | AC12's run | grading pass 2 is read | result `satisfied`, all three passed, the explanation contains a line number, and the snapshot has an indented `Resolved by:` and `Edge case:` line under each of the 2 Ambiguities bullets |
| AC14 (R9) | AC12's run | the record is read | status `satisfied`; `grading` has length 2; `messages` contains a grader feedback message positioned before the model's second Ambiguities edit; `turns` is 9; `turn_cap` 40; `rubric_iterations` 3 |
| AC15 (R9) | a page created from `stubborn.md` with a linked ticket | the run triggered by ticket creation completes | `grading` has exactly 4 passes (the first attempt plus the budget's 3 send-backs), every pass `needs_revision` with clarity and depth failed, status `max_iterations_reached`; the ticket is `Analysis Ready` and its report banner states `max_iterations_reached` |
| AC16 (R10) | a page created from `grader_error.md` with a linked ticket | the run completes | every grading pass has result `grader_error` and empty `criteria`; status `grader_error`; the ticket is `Analysis Ready` and the bot comment names `grader_error` |
| AC17 (R10, R16) | `fixtures/batch_with_error/` registered as batch `with_error` through `FIXTURE_BATCHES` (it ships no `summary.json`, so R16's summariser computes one at registration into the app's copy `data/batches/with_error/`; the fixture directory still has none afterwards) | `GET api/batches/with_error` | `runs` 5, `graded` 4, `grader_errors` 1, every criterion's `total` is 4, completeness passed 4, clarity 0, depth 0, `revisions_needed` 4 |
| AC18 (R11) | AC12's run | pages are read | the seed page still has exactly one version; `page-analysis-req-101` exists with kind `analysis_report`, `linked_ticket` `REQ-101`, title `Analysis Report — REQ-101`, every version authored by `Requirements Review Agent (bot)`; its latest body starts with a banner naming `REQ-101`, requirement version 1, status `satisfied` and `2 grading pass(es)`, followed by the run's `analysis_markdown` |
| AC19 (R12) | the seeded store | `POST api/tickets` with title "Review: logo upload again", linked to the seed page, assignee Casey; then `POST api/tickets` with title "Review: logo upload, unassigned", linked to the seed page, no `assignee` | the first response's ticket key is `REQ-102`; one run exists for it with `fetch_failures` 0 and `rubric_iterations` 3; the ticket is `Analysis Ready`; the second is `REQ-103` with assignee `Unassigned` and one run of its own |
| AC20 (R12, R13) | a fresh seeded store after one `POST api/tickets/REQ-101/rerun` with `{fetch_failures: 0}` (`REQ-101` Analysis Ready with one run), then AC19's two creations, then `REQ-102` and `REQ-103` closed via `api/tickets/{key}/close`; a page created from `unlinked.md` with no ticket | `POST api/pages/page-workspace-logo-upload/versions` with the edited seed body (version 2) | the response names `REQ-101` as re-run and neither `REQ-102` nor `REQ-103`; `REQ-101` gains a second run with `requirement_version` 2 whose Confirmed Facts count is 4; `REQ-102` and `REQ-103` gain no run and stay `Done`; a second save, of a new version to the `unlinked.md` page (which no ticket links to), returns a message that nothing was re-triggered and adds no run |
| AC21 (R13) | a fresh seeded store | the ticket is re-run, then `POST api/tickets/REQ-101/close` | after the run the status is `Analysis Ready`, `last_analyzed_version` 1 and `last_run_id` set, one bot comment present; the run itself never set `Done`; after close the status is `Done`, and the ticket page no longer offers Re-run or Mark Done |
| AC22 (R14) | AC12's run | `GET api/runs/{id}` | `messages` has ≥ 18 entries (1 human, 9 model, 7 tool results, 1 injected feedback, plus whatever the harness adds) including every tool call with its full `args` (the `write_file` content is present untruncated) and every tool result; each grading pass carries its own `analysis_markdown`; `trace` has exactly 16 rows — rows 1–12 alternate `Model reasoning`/`Tool` for the fetch, the `write_file` and the four `edit_file` calls, row 13 is turn 7's model row with action `Finishes the review` and no tool row after it, rows 14–15 are the revision `edit_file` and its result, row 16 is turn 9's model row with action `Finishes the review` — so no two `Tool` rows are adjacent, and a tool row's detail is at most 220 characters; `instructions` is non-empty; the process made no outbound network request during the run |
| AC23 (R15) | AC20's state (`REQ-101` with two runs) | the ticket page and `api/pages/page-analysis-req-101/compare?a=1&b=2` are fetched | the ticket page shows a table with previous and latest requirement version (1, 2), both statuses, and the four list-section counts side by side; the compare response's `diff` is a non-empty unified diff and `run_a`/`run_b` carry the two runs' status and counts |
| AC24 (R16) | the seeded store at instructions version 1 | `POST api/batches` `{label: "v1"}` | five run records in filename order, each `instructions_version` 1, `fetch_failures` 0, `rubric_iterations` 3, status `satisfied` with exactly 2 grading passes; the summary: `runs` 5, `graded` 5, `grader_errors` 0, completeness passed 5, clarity 0, depth 0 (pass_rate 1.0, 0.0, 0.0), `revisions_needed` 5, `documents` = the five stems in order |
| AC25 (R16) | AC24's batch | its directory is inspected | it contains `AGENTS.md` equal to instructions version 1, one `run_NN_<stem>.json` per document and `summary.json`; `GET api/batches/v1` returns the same summary |
| AC26 (R17) | AC24's batch | `POST api/batches/v1/propose` | `change.target` `prompt`, `section` `### Ambiguities`, `change` = the instruction change text, `recurrence` begins `5/5 runs`, `evidence` has 5 entries (one per run) each mentioning both `Resolved by:` and `Edge case:`, `rejected` empty; `proposal_markdown` contains the five headings; the batch directory gains `proposal.md`, `proposal_v1.md` and `proposal_v1.json` and no other file changed (hashes equal before and after) |
| AC27 (R17) | `fixtures/batch_one_off/` registered as batch `oneoff` through `FIXTURE_BATCHES` | `POST api/batches/oneoff/propose` | `rejected` has one entry naming `run_03_c.json` and completeness; `change` targets only `### Ambiguities`; the response's `trace` contains a model row calling `write_file` on `/oneoff/summary.json` followed by a `Tool` row whose action is `Denied by permission: /oneoff/summary.json` (the §5 denied-operation row); `summary.json` in the app's copy `data/batches/oneoff/` is byte-identical afterwards, and `fixtures/batch_one_off/` gained no file |
| AC28 (R18) | AC26's proposal | `POST api/batches/v1/apply` `{approved: true}`; then the same call after copying each of `fixtures/changes/target_tool.json`, `target_grader.json` and `target_configuration.json` in turn over the batch's `proposal_v1.json`; then once more after copying `section_missing.json` over it | the first call creates instructions version 2 = version 1 with the change text inserted at the end of the `### Ambiguities` section, version 1 unchanged, `api/health` reports 2; each of the four later calls is refused (4xx) with a message telling the human to read the proposal and decide (targets) or that the section was not found, and no version 3 exists; `POST api/batches/v1/apply` without `approved: true` is refused |
| AC29 (R16, R18) | instructions version 2 | `POST api/batches` `{label: "v2"}` | five runs each `instructions_version` 2 with exactly 1 grading pass `satisfied`; summary completeness 5, clarity 5, depth 5, `revisions_needed` 0 |
| AC30 (R19) | AC24's and AC29's batches | `GET api/compare?before=v1&after=v2` | `verdict` `success`, `improved` = `[clarity, depth]`, `regressed` empty, `revisions_needed` `[5, 0]`, `attempts` `[10, 5]`, `input_tokens` and `output_tokens` positive integers, `cost_usd` `[0.0, 0.0]` because both batches record `model` `scripted` (the string §5 declares for scripted-mode runs), which is not in R19's price table |
| AC31 (R19) | `fixtures/summaries/regression_before` and `regression_after` registered as batches of those labels through `FIXTURE_BATCHES` | `GET api/compare?before=regression_before&after=regression_after` | `verdict` `regression`, `regressed` `[clarity]`, `improved` empty |
| AC32 (R19) | `partial_before` and `partial_after` registered likewise | `GET api/compare?before=partial_before&after=partial_after` | `verdict` `partial`, `improved` `[clarity, depth]`, `revisions_needed` `[5, 3]` |
| AC33 (R19) | `no_effect_before` and `no_effect_after` registered likewise | `GET api/compare?before=no_effect_before&after=no_effect_after` | `verdict` `no effect`, `improved` and `regressed` empty |
| AC34 (R20, R24) | the source tree and a server started with `OPENAI_API_KEY` unset and `MODEL_MODE` unset | `api/health` is read, `REQ-101` is re-run with `{fetch_failures: 0}`, and the source is searched | `api/health` reports `model_mode` `scripted` and the three `model_roles`; the rerun ends `satisfied` and the process made no outbound network request; the configuration code reads the names `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `REVIEW_MODEL`, `GRADER_MODEL`, `ANALYST_MODEL` and the source contains no other `*_API_KEY`/`*_BASE_URL` name, no string `ANTHROPIC`, no literal key value, and no prompt asking the person for a key; in live mode the provider client is constructed with `base_url` taken from `OPENAI_BASE_URL` |
| AC35 (R21) | the server started by `run_server.sh` | a request to `http://0.0.0.0:4000/api/health` and to the page root | both return 200; no other port is listened on; the response to the root is the app's page |
| AC36 (R21) | the served page and every script or stylesheet it references | their text is searched | no `href`, `src`, `action`, `fetch(`, `open(` or `url(` value starts with `/`; every API call in the page's code is a relative path; no WebSocket is opened |
| AC37 (R22) | AC20's state | the server process is stopped and started again | `api/tickets/REQ-101` returns both runs, the seed page has 2 versions, the `unlinked.md` page has 2 versions, `api/instructions` lists the same versions, and no reseeding occurred |
| AC38 (R9, R20) `live` | `MODEL_MODE=live`, the platform variables set, `REVIEW_MODEL`/`GRADER_MODEL`/`ANALYST_MODEL` set from `resolved-decisions.md` | rerun `REQ-101` with `{fetch_failures: 0}` | the run reaches a terminal status in the contract's enum, `grading` has ≥ 1 pass with three criteria in order, `analysis_markdown` has all five sections with every list section non-empty, and `model_mode` is `live` |
| AC39 (R20) | the build folder after the gate | `resolved-decisions.md` is read | it exists, lists every Ledger row (L1, D1, D2, RR1) with a deviation mark, and carries one "model roles" line naming the values of `REVIEW_MODEL`, `GRADER_MODEL` and `ANALYST_MODEL` |
| AC40 (R25) | the build folder after the install step and a running server | `README.md` and `api/health` are read | `README.md` contains the recorded `python3 --version` output; `api/health.python_version` names the same version; its major.minor is ≥ 3.12 (the §2 course floor) |
| AC41 (R8) | a page created from `nearmiss.md` with a linked ticket | the run triggered by ticket creation completes | grading pass 1: completeness passed, clarity and depth failed with gaps naming the missing labels, although its `analysis_markdown` snapshot holds an indented `Resolution:` and `Edge-case risk:` line under every Ambiguities bullet; pass 2 `satisfied` with the exact labels present; `grading` has length 2; status `satisfied` |
| AC42 (R15) | a fresh seeded store after one `POST api/tickets/REQ-101/rerun` with `{fetch_failures: 0}` | `POST api/pages/page-workspace-logo-upload/versions` with the same-count seed body, then `GET api/pages/page-analysis-req-101/compare?a=1&b=2` | `REQ-101` has two runs whose `counts` are identical (Confirmed Facts 3, Ambiguities 2, Clarification Questions 2, Assumptions 2) and whose `requirement_version` are 1 and 2; `run_a` and `run_b` carry those equal counts; `diff` is non-empty and contains the reworded clause; the ticket page's "What changed" table shows the equal counts beside the compare link |

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the §0 gate first and write `resolved-decisions.md` (with the model-roles line) before any code; `[environment]` the workspace is the record — a new chat starts with no memory of this one and the grader sees only what is on disk, so every resolved value and result goes into a file.
- Run `python3 --version` first and record it in `README.md`; batch the install into one early step and announce its cost.
- Keep the agent's instructions file and every run workspace inside app-owned subfolders (R6).
- Emit relative URLs only; bind one server to `0.0.0.0:4000` (R21).
- Run the offline suite with `OPENAI_API_KEY` unset before claiming completion; report every criterion with cited evidence (§7).
- Label every fixture stand-in as a stand-in in its own description (row RR1).

**Ask First** (derived from the mined trade-off table in CTX-C; each either forces rework or silently changes a guarantee)
- Switching instruction placement (row D1): moving procedure text into skills changes what the learning loop targets and re-runs are needed to re-baseline.
- Switching the grader kind (row D2): a deterministic grader changes who owns the verdict; re-grade every stored batch before comparing across the switch.
- Changing `rubric_iterations` (R9) — raising it hides a stubborn agent behind more retries; 0 removes verification without failing an offline criterion that does not ask for it.
- Changing the rubric text (§3): it is the definition of done; every stored batch becomes incomparable with new ones (rework: re-run batches).
- Setting `GRADER_MODEL` to a different model than `REVIEW_MODEL` (R9 lever; Lesson 5's "common production choice"): changes cost and verdict strictness; no criterion fails.
- Changing `ANALYST_MODEL` to a cheaper tier (R17 lever): the course states the cheaper model finds recurrence unreliably; no offline criterion fails.
- Changing `REVIEW_MODEL` by task complexity (Lesson 2's tiering lever, R20): cost/quality trade with no failing criterion.
- Setting `fetch_failures` for triggered runs above 0, or the manual default to 0 (R2): changes the retry demonstration without changing any guarantee the suite needs beyond AC3.
- Making instruction changes apply without the approval action, or without a compare (R18, R19): removes a human guarantee no test watches.
- Re-running Done tickets on page saves (R12, R13): changes the human-ownership guarantee silently.
- Adding any scheduled trigger, memory target or non-prompt applier (§1 items 5–7): unspecified here.
- Any dependency beyond §2's table.

**Never**
- Author or edit an `AGENTS.md` at the workspace root `[environment]` — the IDE rewrites it at boot; the agent's instruction file lives in app-owned subfolders only.
- Ask the person for an API key, hardcode one, read `ANTHROPIC_*`, or guess variable names (R20).
- Bake a "current best" model id into code or docs; model ids come from the role variables.
- Invent provenance or citations (a `(CTX-X)` anchor only where the materials support it).
- Let the grader pass a criterion it cannot quote, or judge from the conversation instead of the file (R8) — the system must abstain from a pass it cannot show.
- Mutate a fixture, a seed text or an expected outcome to make a test pass.
- Let the agent close a ticket, edit a requirement page, or edit its own instructions (R6, R11, R13).
- Commit secrets or a `.env` with real values.
- Open a WebSocket or bind another port `[environment]`.

## 7. Test Plan & Self-Verification

The build provides two scripts at the app root; the commands are real and are what the evidence cites.

```
python3 --version                                  # record in README.md first
python3 -m venv --system-site-packages .venv && . .venv/bin/activate
pip install -r requirements.txt                    # the §2 pins; one batched install, cost announced
./run_tests.sh                                     # MODEL_MODE=scripted, OPENAI_API_KEY unset; runs AC1–AC37 and AC39–AC42
./run_server.sh                                    # MODEL_MODE=scripted uvicorn on 0.0.0.0:4000, in the background
curl -s http://0.0.0.0:4000/api/health             # AC35 evidence
MODEL_MODE=live ./run_tests.sh --live              # AC38 only; needs the platform variables and the role variables
```

`run_tests.sh` runs a `pytest` suite whose test ids carry the AC numbers (`test_ac12_...`). The building agent MUST report results per acceptance criterion — AC1 through AC42 — each with cited evidence: the test id and its pass line from the run output, or the file path and the exact excerpt the criterion asserts. "Should pass" / "looks correct" are treated as failures — they mean it was not run. A criterion that cannot be run is reported as failed with the reason. If a course-pinned package refuses the interpreter, stop and report (§2).

## Runtime (lab)

Everything in this section is `[environment]` — contributed by the lab, never by the course.

**Container.** Debian, non-root user, Node 22, Python 3 with venv, sqlite3, git and build tooling. Preinstalled Python: `fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`; Node: `express`, `cors`, `better-sqlite3`, `vite`, `nodemon`. Nothing else. Outbound network works, so §2's installs succeed, but each costs the learner wall-clock time inside the session: batch them early and announce the cost. Create the venv with `--system-site-packages`; the course's pins win over preinstalled copies inside it (§2). The Python minor version tracks the image: run `python3 --version`, record it, and stop with a report if a pinned package refuses it. Memory is finite and shared with the agent's own process; this pipeline holds no local model resident (every model is reached over HTTP), so no load-and-release rule is needed.

**Preview.** One server on port 4000 bound to `0.0.0.0` serving page and API (R21); every URL relative; HTTP only (streaming responses allowed; no WebSocket). Long-running servers run in the background and every tool call is visible to the learner.

**Workspace.** The workspace is the record: a new chat has no memory of an earlier one and the grader sees only what is on disk, so `resolved-decisions.md`, `README.md` (with the interpreter version and the test commands) and the test output are files, not chat. The workspace-root `AGENTS.md` is never authored (the IDE rewrites it at every boot); the review agent's own `AGENTS.md` lives inside its run folder under the app, which is unaffected.

**Models.** The lab fixes the model the coding agent runs on and exports `OPENAI_API_KEY`/`OPENAI_BASE_URL` and `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL` pointing at the platform proxy; R20 says which pair the app reads. The platform's model set changes, so the role variables are set at the gate's checklist.

**Environment failure modes** (never in CTX-A/CTX-B, which are the course's):
- **EF1 — Root-absolute URL under the proxied preview.** Symptom: the page loads but every link and API call 404s or hits the IDE. Cause: `/api/...` resolves against the proxy root. Fix: relative paths everywhere. Enforced by R21, AC36.
- **EF2 — Server on the wrong port or interface.** Symptom: nothing previewable. Cause: `localhost`/`127.0.0.1` binding or another port (the course ran on 5050). Fix: `0.0.0.0:4000`. Enforced by R21, AC35.
- **EF3 — Guidance written to the workspace-root `AGENTS.md`.** Symptom: instructions vanish after a restart. Cause: the IDE rewrites that file at boot. Fix: §6's Never list forbids it; app-owned subfolders. Enforced by R6, AC8.
- **EF4 — Unannounced install cost or an interpreter below the course floor.** Symptom: a stalled session or a compiler error during install. Fix: `python3 --version` first, one batched announced install (§2, §7). Enforced by R25, AC40 (the floor); the batched, announced install is a §6 Always entry that no criterion checks.
- **EF5 — A key asked for or guessed.** Symptom: a build that waits on the learner for a secret the container already holds. Fix: R20; AC34.

## Course Context Pack (embedded — agent-readable)

Concepts only; no code from the course appears here. Anchors are position-independent.

### CTX-A. The pattern

Four nested loops around one agent: `trigger → fetch requirement → agent loop (model calls tools until the report file is done) → grade against a rubric → retry with feedback up to a budget → publish report + record run → (across many runs) analyse the run history → propose one harness change → human approves → apply → re-run the batch → compare`.

- **Trigger** (Lesson 6): the agent is looped into where the work already happens — a ticket created, a linked page edited — so using it is no extra step; the system update it produces (a report page, a status change) is what makes the loop a loop.
- **Fetch** (Lesson 4): the agent is told a ticket, not a document; it must go and get the text as it would from a real tracker, and it must survive a transient failure by retrying.
- **Agent loop** (Lessons 3–4): the model calls tools, observes results and continues until it decides it is done; its deliverable is a file in a confined filesystem, built stage by stage; a model-call cap exists only for the path where the model never decides to stop.
- **Instructions as files** (Lesson 3): an always-on file is loaded on every run (what is always true: role, procedure, rules); skills are disclosed progressively; the file lives where the agent can read it and never where it can write it.
- **Verification loop** (Lesson 5): "finished" is not "good enough" — a grader reads the file, scores each rubric criterion pass/fail, and sends specific gaps back; all criteria must pass in the same pass; this is what lets a cheaper model handle harder work.
- **Learning loop** (Lesson 7): the verification loop fixes one run; the same correction recurring across different documents is a property of the agent, found in the traces, and the fix goes into the harness (here, the instructions file) — proposed by an analyst, approved by a human, applied by code, measured by a before/after batch.
- **Human oversight** (Lesson 2): humans approve artifacts (the ticket close) and harness changes (the apply); the automation never closes its own work.

### CTX-B. Failure-mode catalog

- **B1 Transient fetch failure.** Symptom: the external lookup returns an error message instead of the document. Cause: a busy or unreachable external system (a 503, a timeout). Fix: call the same tool again with the same arguments; record each attempt. Enforced by R2, AC3.
- **B2 Endless retry.** Symptom: the agent keeps retrying past the point where retrying makes sense and never finishes. Cause: the normal stop (the model deciding it is done) never happens. Fix: a model-call cap that ends the run and a trace that names the cap as the reason, distinct from a finished review. Enforced by R3, AC4, AC5.
- **B3 Shallow ambiguities on the first attempt.** Symptom: an ambiguity is found and explained, but nothing says what would resolve it or what goes wrong if it stays open; clarity and depth fail while completeness passes. Cause: the instructions never asked for those lines. Fix (one run): the grader's gap feedback and a revision pass. Fix (all runs): B8. Enforced by R9, AC12–AC14.
- **B4 Grading by resemblance.** Symptom: the grader passes criteria the file does not satisfy. Cause: it judges from how the conversation reads, or from what the file looks like, rather than from the file's text; a similar label is taken for the required one. Fix: give the grader a file-reading tool, require it to read the file and quote a line number before passing, apply labels literally, check coverage item by item. Enforced by R4, R8, AC12, AC13, AC41 (the planted near-miss labels of `nearmiss.md`).
- **B5 Missing instructions file.** Symptom: a plausible but bad review. Cause: the memory file was absent and the harness ignored that silently, so the agent ran on the system prompt alone. Fix: refuse to run without it. Enforced by R6, AC10.
- **B6 Agent edits its own instructions.** Symptom: drifting behaviour between runs. Cause: the instructions sit in the same writable filesystem as the report. Fix: deny writes under the memory path by permission, not by instruction alone. Enforced by R6, AC9.
- **B7 Stale report from a previous run.** Symptom: the agent reads a finished report left on disk and skips stages. Cause: re-running in the same workspace. Fix: one fresh workspace per run, removed afterwards. Enforced by R7, AC11.
- **B8 The same correction every run.** Symptom: every first attempt fails the same criteria for the same reason across unrelated documents. Cause: a systematic instruction gap. Fix: a batch over several documents, first-attempt pass rates per criterion, an analyst that reads the recurring gaps and proposes the literal instruction text that would make the correction unnecessary. Enforced by R16, R17, AC24, AC26.
- **B9 Acting on a one-off.** Symptom: an instruction change motivated by a single run. Cause: a problem in one document mistaken for a property of the agent. Fix: a single occurrence across the batch is not a pattern; it is recorded as rejected and not acted on. Enforced by R17, AC27.
- **B10 Merging a harness change without evidence or approval.** Symptom: no confidence that the change helped, or a regression merged silently. Cause: the analyst applies its own change, or no eval runs afterwards. Fix: the analyst only proposes; a human approves; code applies; a before/after batch comparison yields a verdict (regression / success / partial / no effect). Enforced by R18, R19, AC28–AC33.
- **B11 Grader error counted as a pass.** Symptom: a batch looks better than it is. Cause: a failed grader call recorded as if it were a verdict. Fix: record it as a grader error with no criteria, exclude it from every denominator, report the error count. Enforced by R10, AC16, AC17.
- **B12 Counts that hide a changed report.** Symptom: before/after bullet counts look alike although the content changed completely. Cause: the shape stayed while the text moved. Fix: show the counts table and the full text diff together. Enforced by R15, AC23, AC42 (the planted same-count seed body).
- **B13 Automation that closes its own work.** Symptom: a ticket marked done by the pipeline. Fix: only a human closes; the run sets "analysis ready". Enforced by R13, AC21.
- **B14 Agent writes into the source of truth.** Symptom: the requirement page gains agent-authored versions. Fix: the report goes to a separate agent-authored page; the requirement is read-only to the agent. Enforced by R11, AC18.
- **B15 Re-running work nobody asked for.** Symptom: a closed ticket re-analysed on every page edit. Fix: page saves re-run only open linked tickets. Enforced by R12, R13, AC20.
- **B16 Untriggered agent.** Symptom: a useful review that nobody runs because it lives in a separate tool. Cause: friction — copy, paste, ask. Fix: trigger it from the events where the work happens. Enforced by R12, AC19.

### CTX-C. Decision background

**How to read the provenance notes.** A *litmus branch* is how an argued subject was disposed of: a **row** (both sides shown working, differing in a component, identity or role — it becomes a Decision Ledger row), a **bake-in** (the course showed the other side failing or warned against it as a failure — it becomes a business rule), or a **lever** (the sides differ only in a value — a body default with the argument beside it). Two *tie-breakers* make the branch mechanical: *tie-breaker 1* — a demonstrated failure wins: if the course showed one side failing, that side is the anti-pattern and the subject is a bake-in, however many earlier lessons showed it working; *tie-breaker 2* — a trade-off about a value is a lever: when the sides differ only in a number, a tier or a budget, not in a component, an identity or a role, the subject is a lever. A *degenerate case* is the behaviour the taught mechanism itself produces at a trivial setting (a budget of 0 is just the agent loop); it is never a second side. A *lever* is a value the spec fixes but a learner may tune after the build; its *value-selection branches* — the *lever-value rule* — are, in order: (1) the value the narration states in the lesson that introduces the concept, (2) the end-to-end application's configuration, (3) the value used most often, earliest-taught on ties. A *post-build lever* is such a value, asked about after the build, never at the gate. `narrative` marks a subject in the trade-off table that the course used as framing — a taxonomy, a maturity story, a list of placements — and never argued as a choice the builder makes; it is not a disposition, because such a subject never enters the litmus, and the table carries it so the omission is visible rather than silent. A Ledger row's *Category* names the route that admitted it: *design-argued* (the course argued a two-sided trade-off), *design-structural* (choosing differently changes the system's structure, who owns a verdict, or a guarantee), *realization* (a keyed or heavy dependency with a lighter stand-in, surfaced by the substitution rules below), *learner* (a learner-context dimension). The *keyed-tool rule*: when the course's own tool needs a credential and a keyless simulation carries every taught behaviour, the keyless side is the default and the keyed tool is the course-faithful Options entry. *Stakes* is the test a course-contradicted value must pass to become a Ledger row: would picking the other side up front change the system's structure, semantics or a guarantee, or force rework? A *substitution row* is a Ledger row whose default stands in for the course's own technology because that technology needs a credential, account, admin setup or special hardware — the *heavy bar*; mere network access is not heavy. *Realization tiers* order substitutes from lightest: (1) ships with the language's standard distribution, (2) an embedded library, (3) a locally served process. In this lab mode a learner-context dimension is *ANSWERED* (the lab fixes it), *CONSTRAINED* (the lab narrows it) or *KEPT* (the lab has no opinion); an option is *untakeable* when it needs a credential the lab does not supply or makes the offline suite wait on a person.

**Mined spoken trade-off table** (transcripts and narrated slides; every argued subject has exactly one disposition):

| Subject | Lesson | Disposition |
|---|---|---|
| Match model intelligence to task complexity to optimise cost | 2 | **lever** (tie-breaker 2: sides differ in a tier/value; attached to the CONSTRAINED model dimension) — `REVIEW_MODEL`, Ask First |
| Verification lets a cheaper model handle harder tasks; budget 0 is just the agent loop | 2, 5 | **lever** (tie-breaker 2: the no-verification side is the degenerate case of the budget) — `rubric_iterations`, R9, Ask First |
| Grader deterministic or agentic (LLM-as-judge) | 2 (narrated slide) | **row D2** via design-structural — presented, not argued, so not design-argued; neither side shown failing |
| Instruction placement: system prompt / always-on file / skills with progressive disclosure | 3 | **row D1** — both file placements built and shown working; sides differ in a component |
| The always-on file costs context every call, so keep it short; skills cost one line until read | 3 | folded into **row D1**'s Trade-off |
| The cap is not the normal stop; it matters when retrying never ends | 4 | **bake-in R3** (tie-breaker 1: the uncapped side is shown as the failure case) |
| Same model for agent and grader vs a separate grader model ("common production choice") | 5 | **lever** (tie-breaker 2: the sides differ in which model tier grades, a value, not in a component or role; attached to the CONSTRAINED model dimension) — `GRADER_MODEL`, R9, Ask First |
| Analyst on a stronger model because the cheaper one finds recurrence unreliably | 7 (+ README) | **lever** (tie-breaker 2: a stronger vs cheaper tier is a value; attached to the CONSTRAINED model dimension) — `ANALYST_MODEL`, R17, Ask First |
| Output as a file you can open vs text parsed out of a message | 3 | **bake-in R4** (tie-breaker 1: judging from the conversation is the demonstrated failure, B4) |
| Analyst proposes, code applies; an agent that edits its evidence is not analysing | 7 (module narration) | **bake-in R17/R18** (tie-breaker 1: the other side is warned against as a failure — half-applied, unreviewable) |
| Human approval of harness changes and an eval suite before merging | 2, 7 | **bake-in R18/R19** (tie-breaker 1: merging without evals is warned against as the failure) |
| Simulated tracker/wiki vs real Slack / Jira / Confluence | 6 | **realization row** (keyed-tool rule: the keyless simulation carries every taught behaviour, so the real tools are not the default) — resolved by the Environment Resolutions table: every real alternative untakeable here |
| Local trace table vs hosted tracing | 3 | **realization row** (hosted tracing is keyed and optional; the local trace is the course's default) — resolved by the table: untakeable here |
| Loops are composable; you need not nest all four | 2 | `narrative` — framing of the taxonomy, not a builder's choice the course argued; the assignment nests all four |
| Scheduled vs event triggers | 2 | `narrative` — presented without a trade-off; scheduled triggers are §1 item 5 |
| Human oversight at four levels | 2 | `narrative` — framing; the two built placements are R13 and R18 |
| Two categories of harness improvement: procedural vs memory | 2 | `narrative` — framing; memory is §1 item 6 |

**Contradictions mined, with both sides and their routing:**
- *Grader send-back budget*: 3 in the Lesson 5 notebook and narration and in the batch runner; 2 in the course's event-driven app. Stakes: a numeric budget, no structural change → body default via lever branch (1) = 3; post-build lever (R9).
- *Simulated fetch failures*: 2 in the Lesson 4 narration, the notebook's tool table and the pre-baked trace; 0 in the helper's default and in the batch runner ("here it only adds turns and noise"). Stakes: a count → body default via lever branch (1) = 2 for the manual review; the batch and triggered runs keep the course's explicit 0 (R2).
- *Fetch tool name*: `fetch_requirement` in the shipped instructions and tool definition and in the Lesson 4 narration; `fetch_requirement_from_jira` in the learning-loop batch snapshots and a slide. Contract-participating (the instructions must name the registered tool) → binding `fetch_requirement`, lever branch (1).
- *Model-call caps*: 12 for the agent loop alone, 40 wherever a grader can send work back — two configurations the course explains, not a contradiction; both carried (R3).
- *Memory file name*: `Agent.md` on one slide and once in the Lesson 3 narration; `AGENTS.md` everywhere in code and in the rest of the narration → `AGENTS.md`, lever branch (2): the narration conflicts with itself, so the application's configuration decides; contract-participating (R6 loads the file by this exact name), so the value is binding.
- *Number of batch documents*: "four" then "five" in the Lesson 7 narration; a slide shows two placeholders; the code runs five → five fixture documents, lever branch (2): the introducing narration states both values, so the application's configuration decides.
- *Requirement wording on slides vs narration* and *lesson numbering* (transcripts 1–8; repo folders one lower; the README's own numbering): presentation only; transcript numbering is used throughout.
- *README's claim that a missing key falls back to pre-baked traces*: no such code exists in the materials; this spec's offline mode is the scripted stand-in (RR1), not a replay.
- *Third-loop name* ("Application loop" on one slide) and *fourth-loop names* (hill-climbing / learning / self-improvement): name map only.
- *Tracing project names*, run names and tags, notebook card styles and the app's stylesheet colours: presentation constants, declared dropped.

**Row and rule background.**
- → Ledger D1: the course's three instruction channels — a system prompt string used every call; an always-on file loaded every run and editable over time; skills disclosed by frontmatter description, body read on demand. The review agent used the file only; its system prompt points at the file and says the two carry equal weight. The learning loop edits the file, which is why the file is the target and why the agent cannot write it.
- → Ledger D2: the grader receives the agent's whole conversation by default, which is why the course gave it a file tool and the literal-judging additions (B4); the verdict vocabulary is satisfied / needs revision / error; a cap exhausted still reads "needs revision" on the last pass, so the exit reason is tracked separately (R9).
- → Ledger RR1: the course ran every live path on one provider; the offline paths in the notebooks were replays of saved traces, not stand-in models; this spec's stand-ins drive the real harness instead — the rule being that a pipeline which needs a model declares, in §5, scripted stand-ins that drive the real harness end to end, so that the offline suite exercises every stage with no key and a replay of saved outputs is never mistaken for a test.
- → R5: stage order is requested in the instructions, not enforced by the harness; the course's checker reports what happened (in order, complete, missing) and is meant to keep a bad reference run from being saved.
- → R14: the batch keeps every message untruncated because the gap between what the agent was told, produced, was told afterwards and fixed is the diagnosis evidence; the course's condensed trace rows are for display.
- → R15/R23: the course's event-driven app seeded one vague page and one open ticket, kept three JSON lists, and showed counts beside the diff because counts alone hide content changes.
- → R19: the compare verdict order (regression first, then success on zero revisions, then partial, then no effect) and the price table are the course's; token estimation sums the running history per model call.
- → §2 store: tier reasoning in the row; the course's app stores pages with a version list, tickets with status/comments/last-analysed fields, runs with trace and grading; this spec unifies the notebook's batch records and the app's run records into one `AnalysisRun` shape (project hardening).
- → Environment resolutions: the course's real integrations needed an app-level and a bot token (Slack), an API token, site URL and email plus a tunnel (Atlassian); the course's own README says the simulation exists "so this lesson runs with no Atlassian account and no API tokens", and names the trigger function as the seam.
- *Name map to the course's own terms*: course ticket ids `AUTH-142`, `NOTIF-205`, `AUTH-101`, `PAY-310`, `ACCESS-118`, `ALERT-227` and the app's `REQ-104` → this spec's `REQ-101`/`REQ-102` (format kept, values authored); page id `page-req-upload` → `page-workspace-logo-upload`; course cast (Dana, Jordan, Priya, Sam, Morgan) → this spec's cast; labels `v1`/`v2` and files `run_NN_<doc>.json`, `summary.json`, `proposal_<label>.md/.json` kept; `run_history/` → the app's batch directory; `workspace/memories/AGENTS.md` → the app's instructions versions; `/analysis.md`, `/proposal.md`, `/memories/AGENTS.md` kept as the agent-visible paths; primer skills (haiku, limerick, sonnet, acrostic) are the poet example only.

### CTX-D. Perishable assumptions

Treat these as search keywords against current documentation, not guaranteed imports. The concepts in CTX-A…CTX-C are durable; only these names are perishable.

- Harness: `deepagents` 0.7.11 — `create_deep_agent(model, tools, system_prompt, memory=[...], skills=[...], backend, permissions, middleware, checkpointer, response_format)`; `FilesystemBackend(root_dir, virtual_mode=True)`; `FilesystemPermission(operations, paths, mode)` (first match wins; unmatched allowed); `FilesystemMiddleware(backend, tools=[...])` as the way to hand a grader a `read_file` tool; `RubricMiddleware(model, max_iterations, tools, system_prompt, on_evaluation)` — flagged beta, warns on construction, activates only when a `rubric` key is on the invocation state, passing `system_prompt` replaces its default grader prompt (so the verdict definitions and the untrusted-transcript rule must be restated); the private `_rubric_status` state value; `result["structured_response"]` for a structured reply.
- LangChain: `ModelCallLimitMiddleware(run_limit, exit_behavior="end")`; `langchain.tools.tool`; model strings prefixed `openai:`; `langgraph.checkpoint.memory.InMemorySaver`; `agent.stream(..., stream_mode="updates")`; `agent.get_state(config).values`.
- Provider: `langchain-openai` 1.6.0 over `openai` 3.6.0; the ambient `OPENAI_BASE_URL` must reach the client; course model ids `openai:gpt-5.4-mini` (agent, grader) and `openai:gpt-5.5` (analyst) — provenance only.
- **Request/response compatibility:** message content arrives as a list of content blocks on current model families and as a plain string on older ones (the course's trace reader handles both); the platform proxy may serve families that reject some standard request parameters — treat parameter support as perishable and surface a rejected parameter as a reported error, not a retry.
- Tracing: `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` (picked up by the framework with no code change; unavailable here).
- Tokenizer: `tiktoken` encoding `o200k_base`.
- Python ≥ 3.12 (course floor); `uv.lock` format version 1.

### CTX-E. Provenance map

Nothing in this spec requires platform or course access. Lesson numbering follows the transcripts.

| Lesson (transcript numbering) | What this spec took from it |
|---|---|
| 1 Introduction | the four-loop framing and the requirement review agent as the running project (CTX-A) |
| 2 Overview of Loop Engineering | loop taxonomy, model-tiering lever, grader kinds (D2), human-oversight placements (R13, R18), evals before merging (R19), triggers and improvement categories (§1 items 5–6), trade-off table rows (CTX-C) |
| 3 Deep Agent Primer | instruction channels and progressive disclosure (D1), confined filesystem (R6, R7), local vs hosted trace (R14, §1 item 3), harness pillars (§1 item 8), perishables (CTX-D) |
| 4 Agent Loop | fetch-by-ticket (R1), transient-failure retry with two simulated failures (R2, B1), the cap as a safety net and the 12-call setting (R3, B2), report sections and tool sequence (R4), stage-order recording (R5), missing-file and write-deny behaviour (R6, B5, B6) |
| 5 Verification Loop | rubric criteria and label semantics (§3, R8, B3, B4), budget 3 and the 40-call cap (R9), same-vs-different grader model lever, grader-error handling (R10) |
| 6 Event-Driven Loop | triggers and re-run on edit (R12, B15, B16), human closes (R13, B13), agent-authored report page and banner (R11, B14), counts beside diff (R15, B12), seed scenario and store shape (R23, §2), send-back budget 2 (CTX-C contradiction), the real integrations and their seam (§1 items 1–2, Environment Resolutions) |
| 7 Learning loop | batch runs and first-attempt signal (R16, B8), analyst discipline and rejected one-offs (R17, B9), approve-then-apply-by-code (R18, B10), compare verdicts and cost estimate (R19), analyst model lever |
| 8 Conclusion | nothing beyond the recap |

**Slides read** (35, from the slide-descriptions file; "narrated" is that file's proxy for video-shown and ranks with the lesson's transcript; "deck-only" ranks below code and narration): Lesson 2 — Wide deck slides 1 (deck-only title card) and 2–13 (narrated); Lesson 3 — Tall deck 1 (deck-only), 2–5 (narrated); Lesson 4 — Tall 6 (deck-only), 7–10 (narrated); Lesson 5 — Tall 11 (deck-only), 12–14 (narrated); Lesson 6 — third deck 1 (deck-only), 2–4 (narrated), Tall 15 (deck-only), 16 (narrated); Lesson 7 — Tall 17 (deck-only), 18 (narrated). No slide contributed a value the code or narration lacked; slide/narration differences are listed under CTX-C contradictions.

**Environment row** `[environment]`: the deliverable shape (§1), the container, venv and interpreter rules (§2), port 4000 / relative URLs / HTTP only (R21), the model-provider variables and role variables (R20), the workspace-is-the-record and root-`AGENTS.md` rules (§6, Runtime (lab)), the `choices`-fence paragraphs in §0, and every environment failure mode come from the coding-agent-lab environment, not from any lesson.

---

*Spec version 1 · Course: Loop Engineering with LangChain DeepAgents · Learner project: the lab assignment (fixed) · Living document: when the building agent produces something unexpected, add the missing constraint here and re-run.*
