# Spec: Requirements Review Loops — Coding-Agent-Lab Build

> **What you're building.** A one-page web app, served on the lab's preview port, whose agent
> grades its own reports and improves from a batch of them. You create a ticket that links to a
> vague requirement and watch the agent fetch that requirement and fill in a five-section analysis
> (confirmed facts, ambiguities, clarification questions, assumptions, summary). A grader reads the
> finished file, fails two of its three criteria, sends the gaps back, and passes the revised file on
> the second attempt. You edit the requirement and see the analysis re-run on its own; a
> human — never the agent — marks the ticket done. Then you run the same agent over a batch
> of requirements, see the same two criteria fail first-attempt on most of them, read an analyst
> agent's one-paragraph proposal to the agent's instructions, approve it, re-run the batch, and
> watch first-attempt pass rates climb with no criterion regressing.
> **Fastest path:** answer the gate's first question with the recommended baseline build and this
> builds end-to-end; the build is COMPLETE when the offline suite in §7 passes (the container's
> ambient model credentials unlock only the `live` tests and live use of the finished app).
>
> This file is self-contained: the Course Context Pack at the end replaces every external course
> reference. `(CTX-X)` anchors mark course-derived knowledge. The Decision Ledger below holds every
> point where the build could diverge, each pinned to one course-derived default, so the spec builds
> as-is with no intake.
>
> Generated from the *Loop Engineering with LangChain DeepAgents* notebooks + transcripts + slide
> descriptions on 2026-10-11, with the `coding-agent-lab` environment overlay. Base spec-generation
> guide commit `f1ab452`; overlay commit `a63e0e5`. Hand-evolved since 2026-10-11.

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
   *In this lab the tool is the fenced `choices` block* `[environment]`: write the explanation in
   prose above the fence, put the fence **last** in the message with one option per line, precede it
   with a line reading `**Question N of M — <decision>**` so it renders as a question box and both
   of you can see nothing was skipped, and end your turn there. A click sends the option line
   verbatim; a typed answer that names an option counts identically. Only the latest message's
   buttons stay live, so never ask the person to go back and change an earlier answer — re-ask it
   as a new question.
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
   Customize means one question per Ledger row, in table order, after the first question.
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
   *Why the file matters here* `[environment]`: in this lab the workspace is the record — a new
   chat starts with no memory of an earlier one and the grader sees only what is on disk, so a
   decision left in chat is a decision lost.

## Decision Ledger (§0 above requires the build agent to present these before building)

These are the points where this build could diverge. Every row has a course-derived default, so the
spec is buildable and evaluatable as-is; change a row only when applying to a real project or when
you have reason to prefer another option. Rows are grouped learner → design → realization →
contradicted (pipeline order within each group). This build's realization and contradicted groups
are empty: no course dependency met the heavy bar once the lab supplies model credentials, and every
course contradiction resolved as a body lever (CTX-C). Owner is a label only. When D-A1 selects an
option that drops a loop, rows D-A2 and D-S1 are still presented and answered — no row is ever
skipped — and the resolved-decisions checklist records each such answer with the note "not exercised
under D-A1 = (x)"; the acceptance criteria an option retires are exactly the ones its D-A1 Options
entry lists.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| D-L1 | learner | **Scope boundary.** Gate: present the §1 "Not Included" list *inside this question*, item by item with its handling tag, and ask whether every exclusion stands. | (empty) | Keep as-is: every §1 exclusion stands; the full acceptance set in §5 is built. | (1) Keep every exclusion; (2) Bring an item back — name it in free text (only items tagged *restorable* or *buildable, no AC* can come back; *defer* items are decided on their own row; *unavailable* items cannot). A genuine *additional* exclusion also goes in free text and must name the ACs it retires. | Bringing back a *buildable, no AC* item adds work the spec gives no parameters or acceptance criteria for; you are on your own for its correctness. | learner |
| D-A1 | design-argued | **Loop composition** — which of the four loops this build wires around the review agent. | The agent loop exists (model calls tools until it declares the file finished — CTX-A stage 3), and every added loop wraps the loops inside it: verification, when present, wraps the agent loop and sits between the trigger and the agent loop; the event trigger wraps whatever is inside it; the learning loop reads the records that everything inside produced. A loop is never added "beside" rather than around. | All four loops (agent + verification + event-driven + learning), as the course built them across Lessons 4–6 and the shipped event app. | (a) all four loops **(course default)**; (b) agent loop only — retires AC9–AC30, AC32, AC34–AC36 and every `live` AC past L1; (c) agent + verification — retires AC13–AC18, AC34 and AC-L3 (event), AC19's batch-run clauses, and AC9's analyst clauses, AC20–AC30, AC35–AC36 (learning; AC9's grader clause stays); (d) agent + verification + event-driven — retires AC19's batch-run clauses and AC9's analyst clauses, AC20–AC30, AC35–AC36 (AC9's grader clause stays); (e) agent + verification + learning, no event trigger — retires AC13–AC18, AC34 and AC-L3 (runs are started from the batch panel only); (f) agent + event-driven, no verification — retires AC9–AC12 and AC32 (grader), AC16's grading-pass clause, AC19 in full (its Given names the AC10 run and a batch run, both retired), and AC20–AC30, AC35–AC36 (learning). | Lesson 2: "I'm doing the Russian doll thing of nesting every loop inside of another. You don't necessarily have to do that for all four loops. For example, you could just nest a core agent loop in with an event-driven loop. You don't need the verification loop per se, but this just shows that they're all composable." Each dropped loop drops what it buys (Lesson 2 recap: verification → quality, event-driven → the agent actually gets used, learning → the agent improves over time). **Litmus branch: row** — the course endorses subsets as legitimate reduced-scope choices (Lesson 2) and shows the agent loop alone working to completion in Lesson 4; Lesson 5's first-attempt rubric failure is framed as "finished isn't good enough" — the reason to add a loop — not as the agent loop breaking. | course+learner |
| D-A2 | design-argued | **Trigger kind** — what starts a review run in the event-driven loop. | Something other than a person pressing "run" can invoke whatever loop composition row D-A1 selects, and every invocation — triggered or manual — produces one persisted run record (R15). | Event-driven: creating a ticket linked to a requirement page runs the loop; saving a new version of a requirement page re-runs it for every open ticket linked to that page; a manual "re-run now" also exists (the course's shipped event app). | (a) event-driven: ticket created / linked requirement edited **(course default)**; (b) scheduled: a periodic sweep re-reviews any open ticket whose linked requirement version is newer than its last analyzed version — AC effect: the "a run starts / is retriggered" clauses of AC14, AC15 and AC17 become "the run exists after the next sweep" (the sweep interval is a body default the build states and the suite shortens in test mode); AC13's manual re-run is unchanged; (c) both — every AC as written, plus the sweep clause of (b). | Lesson 2: triggers "can be scheduled, or they can be ad hoc and event-driven" — a calendar-summary agent runs every morning; an email assistant runs when an email arrives. Scheduled trades immediacy for simplicity (no write path has to call the loop); event-driven trades a trigger hook in every write path for runs that land while the change is fresh. **Litmus branch: row** — both kinds are shown as working, acceptable setups in Lesson 2; neither is warned against. | course+learner |
| D-S1 | design-structural | **Grader realization** — who judges the finished analysis against the rubric. | A grader that is not the review agent's own turn reads the *produced file* (never the conversation), returns pass/fail per criterion with a `gap` on every failure; the run reaches `satisfied` only when every criterion passes in the same grading pass, and exhausting the send-back budget ends it as `max_iterations_reached` (R8, R9, R10). | LLM judge: a model call given a `read_file` tool over the run workspace, instructed to quote verbatim evidence with a line number before passing any criterion and to match labelled lines literally (the course's built grader, Lesson 5). | (a) LLM judge with `read_file` **(course default)**; (b) deterministic checker in code — completeness still needs judgement, so (b) covers clarity and depth exactly (label presence under every Ambiguities bullet) and must state how completeness is decided — AC effect: AC9's `read_file`-only grader clause and AC32 apply to a model grader only and are replaced by "the checker calls no model and records the matched line as `evidence`"; the `GRADER_*` scripts are unused and AC10/AC12 hold as written because the checker fails clarity and depth on the baseline file deterministically; (c) hybrid — deterministic label checks, LLM for completeness — AC effect: AC9's grader clause and AC32 apply to the completeness model call; label criteria as under (b); (d) a person grades: reads the produced file against the rubric on the page and returns per-criterion pass/fail with a gap on each failure (the course names this placement on slide 2.12) — AC effect: AC9's grader clause and AC32 are retired; the page gains a grading form whose endpoint the build declares, and the offline suite drives AC10/AC12 by posting the scripted verdicts through it; no `evidence` is recorded. | Lesson 2 (slide 2.6): "Graders can either be deterministic or agentic (LLM as a judge is a classic example)"; the docs-writer example's grader is deterministic ("links resolve, CI passes"). Switching moves the judgement between harness code and the model: a deterministic checker is cheap and exact but only for mechanically checkable criteria; the LLM judge handles coverage criteria but must be forced to check the file rather than judge by resemblance (CTX-B3). **Litmus branch: row** — the deterministic grader is shown working in the course's own docs-agent example, not as a failure case; this row's category is structural (ownership moves between harness and model), with the Lesson 2 presentation of the alternative cited here rather than as an argued trade-off. | course+learner |
| D-A3 | design-argued | **Human oversight points** — where a person is inserted beyond the two the course bakes in. | Two gates are rules, not options (R14, R18): only a human marks a ticket Done, and a harness change is applied only after a human approves it. This row decides only the *additional* gates. | No additional gate: the review agent's tools (fetch, write, edit on a confined filesystem) are not sensitive, so no per-tool approval; the grader is whatever row D-S1 selects. | (a) no additional gate **(course default)**; (b) human approval before a named sensitive tool call (the course names "send email" as the kind of tool that warrants it); (c) a human acts as grader — a grader realization; decide it on row D-S1 (its option (d)), not here. | Lesson 2 / slide 2.12: "you can still add human approval at important or sensitive tool calls"; "you can add a human to the grader or verifier cycle"; "human approval on agent artifacts or results"; "approving harness and code changes to your core agent". Every added gate buys safety on a sensitive action and costs latency and attention on every run. **Litmus branch: row** for the additional gates (both configurations are shown as acceptable in Lesson 2); **bake-in** for the two gates the course never shows bypassed — R14 ("the agent never closes its own work") and R18 (harness changes "must flow through systematic human review before final system deployment"). | course+learner |

## Environment Resolutions (`coding-agent-lab`)

This spec is generated for the `coding-agent-lab` environment: the six learner-context dimensions
were derived first, exactly as for a standalone takeaway, and then *resolved* against the lab —
removed from the Ledger only where the lab answers or narrows them, never skipped.

| Dimension | Resolution | Where the Invariant lives now |
|---|---|---|
| project | **ANSWERED** — the lab fixes the assignment | spec §1 Objective (derived Invariant empty — no AC owed) |
| data/inputs | **ANSWERED** — inputs are seeded into the workspace | spec §5 fixture corpus; Invariant (a) "the agent is never handed the requirement text, only a ticket id to fetch" → R1, AC5; Invariant (b) "the learning loop needs a batch of ≥ 2 distinct documents" → R16, AC20 (the fixture batch has 5), AC36 (a 1-document batch is refused) |
| goal | **ANSWERED** — the lab fixes what "working" means | spec §1 + the acceptance criteria; Invariant "done = every rubric criterion passes in the same grading pass" → R8, AC10; Invariant "learning-loop success = first-attempt pass rate rises with no criterion regressing" → R19, AC27–AC28 |
| model/provider | **CONSTRAINED** — the built app needs an LLM (agent, grader and analyst roles are all model calls), so: platform models only, keys and base URLs read from the container environment, never ask the learner for a key | spec §2 + R20 + CTX-D; Invariant "native tool calling; structured output for the analyst; the grader role can call a `read_file` tool" → R20; the offline suite proves the wiring (AC1, AC9), the live set proves the capability on the platform's real models (AC10 L2 — grader calls `read_file`; AC24 L4 — analyst structured output; AC30; AC-L1 — agent tool calling) |
| environment | **ANSWERED** — the container | spec §2 + the Runtime (lab) section; capability invariants moved to the rows that need them: "file tools confined to a virtual root" → R5, AC4; "one isolated workspace per run" → R6, AC6; "run records persist so a later process can read a batch" → R15, AC19, AC35 (a new server process reads the batch); "instructions readable by the agent, writable only from outside" → R5, AC4 |
| scope-boundary | **KEPT** | stays a Ledger row (D-L1) |

## 1. Objective

A single-server web app in which a requirements-review agent turns a vague requirement into a
five-section analysis file, a rubric grader sends the file back until all three criteria pass, ticket
and requirement-page events trigger that loop automatically (a human alone closes a ticket), and a
learning loop runs the agent over a batch, finds the correction it needs on *most* documents, proposes
one edit to the agent's instructions for a human to approve, applies it, re-runs the batch and reports
whether first-attempt pass rates improved without regression. (pattern: CTX-A)

**Deliverable shape** `[environment]`: **one server on port 4000 serving both the page and its API** —
the lab's preview pane is the learner's only view of the running app, and the course's own artifacts
(four notebooks and a two-UI Flask demo on port 5050) are never the deliverable. The pattern has a
user-facing surface (the course's own event app is one), so the library-plus-tests escape is not
taken.

### Not Included            ★

Each item carries its handling tag for the D-L1 gate question: *restorable* (additive, owned by no
other row — can come back at the gate), *buildable, no AC* (named by the course but never built —
you may build it, but this spec supplies no parameters and no acceptance criteria), *defer* (owned
by a Ledger row — decided there), *unavailable* (outside the delivered build mode).

1. Real Jira / Confluence / Slack / GitHub integration — REST calls or incoming webhooks. The course
   simulates the tracker and the wiki inside the app and names the real integration as "the next
   step, not built here". — *buildable, no AC*
2. Hosted tracing (the course's optional LangSmith setup, keyed). The build records its own local
   trace per run (R15); nothing here needs a hosted tracer. — *restorable* (restoring adds a key and
   live criteria this spec does not supply)
3. Skills with progressive disclosure, subagent delegation, context summarization/offloading, and a
   code interpreter or sandbox — deep-agent capabilities the course's primer names; the review agent
   uses none of them. — *buildable, no AC*
4. Memory consolidation of user preferences across runs (the course's email-assistant illustration).
   — *buildable, no AC*
5. Scheduled triggers — *defer* (row D-A2)
6. Human approval before tool calls; a human acting as grader — *defer* (rows D-A3, D-S1)
7. A deterministic or hybrid grader — *defer* (row D-S1)
8. Token and USD cost estimates for a batch (the course computes an estimate from a hard-coded price
   table for its own models; those prices and model names are era-specific, CTX-D). — *restorable*
9. Accounts, login, or per-user permissions on the page — the course uses a fixed cast of names.
   — *restorable*
10. Notebook-style renderings (matplotlib plots, HTML report cards) — the served page replaces them.
    — *unavailable* `[environment]` (the notebook is never the deliverable)
11. The poet/skills primer agent — the course's teaching toy for the deep-agent primer, unrelated to
    the review loop. — *restorable* (no parameters or criteria supplied)
12. WebSocket or server-push updates — the preview proxies HTTP only; the page polls (R23). —
    *unavailable* `[environment]`
13. Integration into an existing codebase — outside the delivered build mode. — *unavailable*

(Automatic application of harness changes whose target is a tool, the grader, or configuration is not
a scope exclusion but the negation of R18 — carried there, in row D-A3's Trade-off and in CTX-B14.)

### Adapting this beyond the lab

Taking this spec out of the lab, re-open what the environment resolved: **project** and **goal** are
fixed in this §1 and in §5 — retitle and re-scope there; **data** is the §5 fixture corpus — swap the
ticket store and requirement documents for your own, keeping R1 (fetch by id); **model/provider** is
§2 + R20 — outside the lab there are no ambient credentials, so supply your own provider keys via
`.env` (the course's way) and pick models for the three roles; **environment** is §2 + the Runtime
(lab) section — port 4000, relative URLs and the no-WebSocket rule (R21–R23) are lab facts you may
relax; **scope boundary** was never resolved and stays row D-L1.

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language / runtime | Python 3 (the container's), inside a venv created with `--system-site-packages` | `[environment]` Python 3 with venv is preinstalled; the flag keeps the preinstalled packages usable. Course: `requires-python >= 3.12` (pyproject), notebooks ran 3.12.10; the course's floor was justified by numpy/pandas builds, which this app does not use. The build agent checks `python3 --version`; if below 3.12 and the pinned harness refuses to install, report it — do not invent a workaround. |
| Agent harness | `deepagents==0.7.11` | **Course's actual pin situation:** `pyproject.toml` sets floors (`>=`), and `uv.lock` resolves exact versions; §2 pins the `uv.lock` versions for every package the course locked. `[environment]` **Not preinstalled** — the container ships no agent framework. Batch every install below into one early command and announce its wall-clock cost before running it. Era-specific class and argument names → CTX-D. |
| LLM orchestration | `langchain==1.3.18`, `langchain-core==1.6.1`, `langgraph==1.2.11` | Course-locked (`uv.lock`). Not preinstalled `[environment]`. |
| Provider adapter | `langchain-openai==1.6.0` for an OpenAI-compatible platform endpoint (the course's provider); if the container exports only another provider, the matching LangChain adapter for it at a current version — the course never pinned one | Course-locked for OpenAI. The adapter is driven by the ambient base URL and key (R20). |
| Provider SDK | `openai==3.6.0` | Course-locked. `[environment]` `openai` and `anthropic` are preinstalled at unstated versions; the course pin wins inside the venv (§2's rule throughout: pin what the course pinned). |
| Structured output | `pydantic==2.13.5` | Course-locked; carries the `HarnessChange` schema (§3.4). |
| Env loading | `python-dotenv==1.2.3` | Course-locked; also preinstalled `[environment]`. In the lab the keys are already in the process environment; `.env` is for use outside the lab. |
| Web server + API | FastAPI + uvicorn, at the preinstalled versions | `[environment]` preinstalled; one process on port 4000 bound to `0.0.0.0` (R21). The course's event app used Flask (floor `>=3.1.3`, absent from its lock — unpinned) on port 5050 → CTX-D. |
| Page | One HTML page with inline or static JS served by the same process; every URL relative (R22) | `[environment]`. The course server-rendered two separately styled UIs (tracker vs wiki); keep the two surfaces visually distinct, but one page and one process. |
| Persistent records | JSON files (stdlib `json`) in two sibling directories at the project root: `data/` — `tickets.json`, `pages.json`, `runs.json` — and `run_history/` — one `<label>/` folder per batch (`AGENTS.md`, `run_0N_<doc>.json`, `summary.json`, and `proposal.md` once the analyst has run) plus the app's stored proposal records `proposal_<label>.json` / `.md` (§3.4). `run_history/` is NOT under `data/`; every path in this spec writes it as `run_history/...` from the project root | Course default (flat JSON lists; "a learner can open any of these files directly"); tier 1 (standard distribution). sqlite3 is preinstalled `[environment]` but the course never argued for a database — no Ledger row. |
| Models (three roles) | `AGENT_MODEL`, `GRADER_MODEL`, `ANALYST_MODEL` environment variables, each a platform model id | `[environment]` resolution CONSTRAINED: platform models only. Course's own values (provenance, never "current best"): agent and grader `openai:gpt-5.4-mini`, analyst `openai:gpt-5.5` — see R20 for the tiering lever. The build agent fills `.env.example` with the platform models it finds exported at build time; model currency is its gate-time job. |
| Test runner | `pytest`, current release (unpinned) | **Project hardening** — the course ran no test suite and pinned no runner; this spec's §7 offline suite needs one. Installed in the same §2 batch; not an "install beyond §2". |
| HTTP test client | `httpx`, current release (unpinned) | **Project hardening** — the in-process client the §7 suite uses against the FastAPI app (the test-mode server ACs listed in §7); the course never pinned it. Installed in the same §2 batch. |
| Token counting | none required | The course used `tiktoken==0.14.0` with a length/4 fallback only for the cost estimate, which is Not Included #8. |
| Secrets | Provider keys and base URLs read from the container environment; never hardcoded, never committed, never requested from the learner | `[environment]` + course (`.env` gitignored). The build agent discovers the exported variable names by inspecting the environment (`env`, filtered for `KEY` / `BASE_URL`) and wires them through; it does not guess names into the code. |

## 3. Input/Output Contracts            ★

All API paths below are **relative** (`api/...`), never root-absolute (R22). All timestamps are UTC
strings. The schemas are JSON Schema (draft 2020-12).

### 3.1 The analysis file (`/analysis.md` in the run workspace) — Markdown grammar + parsed form

Exact heading sequence, each a level-2 heading, in this order and no other:
`# Requirements Analysis` · `## Confirmed Facts` · `## Ambiguities` · `## Clarification Questions` ·
`## Assumptions` · `## Summary`. List sections hold `- ` bullets; Summary is prose. An Ambiguities
bullet is `- **"<exact clause quoted from the requirement>"**` followed by an indented
`Reason: <why under-specified>` line; under the *improved* instructions each bullet also carries
indented `Resolved by: <fact or decision that settles it>` and `Edge case: <concrete production
failure if unresolved>` lines (these two labels are what the rubric's clarity and depth criteria look
for, literally — R4, R8).

```json
{
  "$id": "AnalysisReport",
  "type": "object",
  "required": ["confirmed_facts", "ambiguities", "clarification_questions", "assumptions", "summary", "counts", "summary_words"],
  "properties": {
    "confirmed_facts": {"type": "array", "items": {"type": "string"}},
    "ambiguities": {"type": "array", "items": {
      "type": "object", "required": ["clause", "reason"],
      "properties": {
        "clause": {"type": "string", "minLength": 1},
        "reason": {"type": "string", "minLength": 1},
        "resolved_by": {"type": "string"},
        "edge_case": {"type": "string"}
      }}},
    "clarification_questions": {"type": "array", "items": {"type": "string"}},
    "assumptions": {"type": "array", "items": {"type": "string"}},
    "summary": {"type": "string"},
    "counts": {"type": "object",
      "required": ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions"],
      "additionalProperties": {"type": "integer", "minimum": 0}},
    "summary_words": {"type": "integer", "minimum": 0}
  }
}
```

`counts` is bullets per list section (Summary is excluded — it is prose, measured by
`summary_words`). A file is *complete* when every list section has ≥ 1 bullet and `summary_words > 0`.

### 3.2 A run record (one review, with every grading pass)

```json
{
  "$id": "RunRecord",
  "type": "object",
  "required": ["id", "ticket_key", "requirement_version", "label", "status", "stop_reason", "turns",
               "trace", "stages", "stage_order", "in_order", "grading", "analysis_markdown", "instructions",
               "counts", "started_at", "finished_at"],
  "properties": {
    "id": {"type": "string", "pattern": "^[0-9a-f]{8}$"},
    "ticket_key": {"type": "string", "pattern": "^[A-Z]+-[0-9]+$"},
    "requirement_version": {"type": "integer", "minimum": 1},
    "label": {"type": "string", "description": "batch label, or \"ticket\" for event/manual runs"},
    "status": {"enum": ["satisfied", "max_iterations_reached", "needs_revision", "failed", "grader_error", "ungraded"]},
    "stop_reason": {"enum": ["finished", "turn_limit"]},
    "turns": {"type": "integer", "minimum": 0},
    "trace": {"type": "array", "items": {
      "type": "object", "required": ["step", "actor", "action", "detail"],
      "properties": {
        "step": {"type": "integer", "minimum": 1},
        "actor": {"enum": ["Model reasoning", "Tool"]},
        "action": {"type": "string"},
        "detail": {"type": "string", "maxLength": 221}
      }}},
    "stages": {"type": "array", "description": "every write_file / edit_file call on /analysis.md, in trace order, successful or not (R3)",
      "items": {
        "type": "object", "required": ["step", "section", "ok"],
        "properties": {
          "step": {"type": "integer", "minimum": 1, "description": "the trace step of the tool call"},
          "section": {"type": "string", "description": "derived, never trusted from the model: for write_file, the first §3.1 list section that is non-empty in the written content (Confirmed Facts for a correct skeleton); for edit_file, the §3.1 section whose heading line starts at or before the first occurrence of old_string in the file as it stood before the call; \"unknown\" when there is no such section or no occurrence"},
          "ok": {"type": "boolean"},
          "error": {"type": "string", "description": "the tool's error text when ok is false"}
        },
        "if": {"properties": {"ok": {"const": false}}}, "then": {"required": ["error"]}
      }},
    "stage_order": {"type": "array", "items": {"type": "string"},
      "description": "the sections of successful stages only, in the order they were written; a failed stage adds nothing"},
    "in_order": {"type": "boolean",
      "description": "true when stage_order equals the §3.1 sequence (Confirmed Facts, Ambiguities, Clarification Questions, Assumptions, Summary) and no section ended empty"},
    "grading": {"type": "array", "items": {"$ref": "#/$defs/GradingPass"}},
    "analysis_markdown": {"type": "string"},
    "instructions": {"type": "string", "description": "the instructions file this run was given, verbatim"},
    "counts": {"type": "object", "additionalProperties": {"type": "integer"}},
    "messages": {"type": "array", "description": "batch runs only: every message untruncated, with full tool-call args",
      "items": {"type": "object", "required": ["type", "content", "tool_calls"]}},
    "started_at": {"type": "string"},
    "finished_at": {"type": "string"}
  },
  "$defs": {
    "GradingPass": {
      "type": "object",
      "required": ["iteration", "result", "explanation", "criteria", "analysis_markdown"],
      "properties": {
        "iteration": {"type": "integer", "minimum": 1},
        "result": {"enum": ["satisfied", "needs_revision", "failed", "grader_error"]},
        "explanation": {"type": "string"},
        "criteria": {"type": "array", "minItems": 0, "items": {
          "type": "object", "required": ["name", "passed"],
          "properties": {"name": {"type": "string"}, "passed": {"type": "boolean"}, "gap": {"type": "string"},
            "evidence": {"type": "object", "required": ["quote", "line"],
              "description": "the satisfying text quoted verbatim from /analysis.md and its 1-based line number; required on every passed criterion under a model or deterministic grader (R9), absent only when a person grades (row D-S1 option (d))",
              "properties": {"quote": {"type": "string", "minLength": 1}, "line": {"type": "integer", "minimum": 1}}}},
          "if": {"properties": {"passed": {"const": false}}}, "then": {"required": ["gap"]}
        }},
        "analysis_markdown": {"type": "string", "description": "the file exactly as this pass saw it"}
      },
      "allOf": [
        {"if": {"properties": {"result": {"const": "satisfied"}}},
         "then": {"properties": {"criteria": {"items": {"properties": {"passed": {"const": true}}}}}}},
        {"if": {"properties": {"result": {"const": "grader_error"}}},
         "then": {"properties": {"criteria": {"maxItems": 0}}}}
      ]
    }
  },
  "allOf": [
    {"if": {"properties": {"status": {"const": "satisfied"}}},
     "then": {"properties": {"grading": {"minItems": 1}}}},
    {"if": {"properties": {"stop_reason": {"const": "turn_limit"}}},
     "then": {"properties": {"trace": {"contains": {"properties": {"action": {"pattern": "^Stops: turn limit of [0-9]+ reached$"}}}}}}}
  ]
}
```

Status semantics: `satisfied` — every criterion passed in one pass; `max_iterations_reached` — the
send-back budget was spent and the last pass still read `needs_revision` (R10); `ungraded` — the run
had no grader (agent-loop-only runs); the rest are the grader's own terminal verdicts. A trace
`detail` is the tool result collapsed to one line and cut at 220 characters plus an ellipsis. `stages`
is the stage-by-stage record R3 requires: a failed `edit_file` (non-unique `old_string`) appears there
with `ok: false` and its error, is absent from `stage_order`, and does not stop the run. A grading
pass whose grader (model or deterministic) never read `/analysis.md`, or passed a criterion without
`evidence`, is not accepted as a verdict: the harness records it as `result: "grader_error"` with
`criteria: []` and an `explanation` starting `grader verdict rejected:`, and the run's status is
`grader_error` (R9).

### 3.3 Batch summary and comparison

```json
{
  "$id": "BatchSummary",
  "type": "object",
  "required": ["label", "model", "runs", "graded", "grader_errors", "first_attempt", "revisions_needed", "documents"],
  "properties": {
    "label": {"type": "string"},
    "model": {"type": "string", "description": "the agent model id recorded at batch start: the AGENT_MODEL variable's value, or the scripted stand-in's label \"scripted_model (fake)\" in test mode"},
    "runs": {"type": "integer", "minimum": 0},
    "graded": {"type": "integer", "minimum": 0},
    "grader_errors": {"type": "integer", "minimum": 0},
    "first_attempt": {"type": "object",
      "propertyNames": {"enum": ["completeness", "clarity", "depth"]},
      "additionalProperties": {"type": "object", "required": ["passed", "total", "pass_rate"],
        "properties": {"passed": {"type": "integer"}, "total": {"type": "integer"},
                       "pass_rate": {"type": ["number", "null"]}}}},
    "revisions_needed": {"type": "integer", "minimum": 0},
    "documents": {"type": "array", "items": {"type": "string"}}
  }
}
```
Invariants: `graded + grader_errors == runs`; every `first_attempt.*.total == graded`;
`pass_rate == round(passed / total, 3)` or `null` when `graded == 0`; `revisions_needed` counts
graded runs whose first pass failed ≥ 1 criterion (R16). The summary is computed once, at batch end,
from the batch's run records and stored as `run_history/<label>/summary.json`; `GET api/batches/{label}`
returns that stored file (for a batch loaded from a fixture, the fixture's file with `label` set to the
loaded label).

```json
{
  "$id": "Comparison",
  "type": "object",
  "required": ["before", "after", "verdict", "criteria", "runs", "revisions_needed", "improved", "regressed"],
  "properties": {
    "before": {"type": "string"}, "after": {"type": "string"},
    "verdict": {"enum": ["success", "partial", "regression", "no effect"]},
    "criteria": {"type": "object", "additionalProperties": {
      "type": "array", "prefixItems": [{"type": "integer"}, {"type": "integer"}], "minItems": 2, "maxItems": 2}},
    "runs": {"type": "integer"},
    "revisions_needed": {"type": "array", "prefixItems": [{"type": "integer"}, {"type": "integer"}]},
    "improved": {"type": "array", "items": {"type": "string"}},
    "regressed": {"type": "array", "items": {"type": "string"}}
  },
  "allOf": [
    {"if": {"properties": {"regressed": {"minItems": 1}}}, "then": {"properties": {"verdict": {"const": "regression"}}}}
  ]
}
```
Verdict order (R19): any criterion whose first-attempt `passed` fell → `regression`; else
`revisions_needed[1] == 0` → `success`; else any criterion rose → `partial`; else `no effect`.

### 3.4 The analyst's proposal

```json
{
  "$id": "HarnessChange",
  "type": "object",
  "required": ["target", "issue", "recurrence", "evidence", "section", "change", "rejected"],
  "properties": {
    "target": {"enum": ["prompt", "tool", "grader", "configuration"]},
    "issue": {"type": "string", "minLength": 1},
    "recurrence": {"type": "string", "minLength": 1},
    "evidence": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}},
    "section": {"type": "string"},
    "change": {"type": "string", "minLength": 1},
    "rejected": {"type": "array", "items": {"type": "string"}}
  },
  "allOf": [
    {"if": {"properties": {"target": {"const": "prompt"}}},
     "then": {"properties": {"section": {"pattern": "^#{1,6} .+"}}},
     "else": {"properties": {"section": {"const": ""}}}}
  ]
}
```
The analyst writes its reasoning to `/proposal.md` in its own root, the batch directory — on disk
`run_history/<label>/proposal.md` (R17). The app then derives its stored record from that file and the
analyst's structured response: `run_history/proposal_<label>.json` (this schema) beside
`run_history/proposal_<label>.md` (a copy of the batch-dir file), both at the project-root
`run_history/` (§2), plus an `applied` flag and `applied_at` once a human approves (R18).

### 3.5 Tracker and wiki records

```json
{
  "$id": "Ticket",
  "type": "object",
  "required": ["key", "title", "description", "linked_page_id", "assignee", "status", "comments", "created_at", "last_analyzed_version", "last_run_id"],
  "properties": {
    "key": {"type": "string", "pattern": "^[A-Z]+-[0-9]+$"},
    "title": {"type": "string", "minLength": 1},
    "description": {"type": "string"},
    "linked_page_id": {"type": "string"},
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
    "title": {"type": "string"},
    "linked_ticket": {"type": ["string", "null"]},
    "versions": {"type": "array", "items": {
      "type": "object", "required": ["n", "author", "timestamp", "body"],
      "properties": {"n": {"type": "integer", "minimum": 1}, "author": {"type": "string"},
                     "timestamp": {"type": "string"}, "body": {"type": "string"},
                     "run_id": {"type": "string", "pattern": "^[0-9a-f]{8}$",
                                "description": "set on every version a run writes to a report page (the RunRecord id); absent on human-authored versions; compare reads it to return run_a / run_b"}}}}
  },
  "allOf": [
    {"if": {"properties": {"kind": {"const": "analysis_report"}}},
     "then": {"properties": {"linked_ticket": {"type": "string"}, "id": {"pattern": "^page-analysis-[a-z]+-[0-9]+$"}}}},
    {"if": {"properties": {"kind": {"const": "requirement"}}},
     "then": {"properties": {"linked_ticket": {"const": null}}}}
  ]
}
```
Version numbers are dense from 1. Generated ticket keys are `REQ-<n>` with `n` starting at 100 and
incrementing past the highest existing number. A report page is titled `Analysis Report — <key>`,
authored `Requirements Analysis Agent (bot)`, carries the writing run's id in `run_id` (human-authored
requirement versions have none), and each version's body opens with a three-line
quoted banner: generated from which ticket and when; source requirement version; verification status
and number of grading passes — followed by the analysis file verbatim.

### 3.6 API surface (relative paths; JSON in and out)

| Method | Path | Request | Response |
|---|---|---|---|
| GET | `api/health` | — | `{"ok": true, "port": 4000}` |
| GET | `api/tickets` | — | `Ticket[]` |
| POST | `api/tickets` | `{title, description, linked_page_id, assignee}` | `{ticket: Ticket, run_id}` — creating a ticket starts a run (R12) |
| GET | `api/tickets/{key}` | — | `{ticket, page, report_page, runs: RunRecord[] (oldest first), latest_run, previous_run, what_changed}` — `latest_run` / `previous_run` are the two most recent records (`null` when absent); `what_changed` is the **"what changed" table** the ticket view renders when both exist: one row per §3.1 list section (`Confirmed Facts`, `Ambiguities`, `Clarification Questions`, `Assumptions`), each row holding that section's bullet count under `previous_run` and under `latest_run` (from each record's `counts`), plus one row for the requirement version analysed and one for the final status — `[{row, previous, latest}]`; `null` when fewer than two runs exist |
| POST | `api/tickets/{key}/rerun` | — | `{run_id}` — 409 if status is `Done` |
| POST | `api/tickets/{key}/close` | — | `{ticket}` with status `Done` (human action only, R14) |
| GET | `api/runs/{id}` | — | `RunRecord` plus `"state": "running" | "done"` |
| GET | `api/pages` | — | `Page[]` |
| POST | `api/pages` | `{title, body, author}` | `Page` (kind `requirement`, version 1) |
| GET | `api/pages/{id}?v=N` | — | `{page, version: N, body, linked_ticket}` |
| POST | `api/pages/{id}/versions` | `{body, author}` | `{version, retriggered: [key...]}` — 400 unless kind is `requirement` (R13) |
| GET | `api/pages/{id}/compare?a=N&b=M` | — | `{a, b, diff: [unified-diff lines], run_a, run_b}` (`run_*` only for report pages: the `RunRecord` each version's `run_id` names, §3.5) |
| POST | `api/batches` | `{label, instructions_source: "baseline" | "run_history/<label>/AGENTS.md", documents?: [stem...]}` | `{label, state: "running"}` — reviews every fixture document once under that instructions file (R15, R16); the optional `documents` filter (corpus stems) narrows the batch and exists for tests — fewer than 2 documents → 400 with a message naming the minimum of 2 (R16) |
| GET | `api/batches/{label}` | — | `{summary: BatchSummary, runs: RunRecord[], instructions, recurring_gaps: {criterion: [{document, gap}]}, state}` |
| POST | `api/batches/{label}/propose` | — | `{proposal: HarnessChange, proposal_md}` (R17) |
| GET | `api/proposals/{label}` | — | `{proposal, proposal_md, applied, applied_at}` |
| POST | `api/proposals/{label}/apply` | `{approved: true, new_label}` | `{diff: [...], instructions_path: "run_history/<new_label>/AGENTS.md"}` — 400 if `target != "prompt"` or `approved != true`; 422 if the section is missing (R18) |
| GET | `api/compare?before=L1&after=L2` | — | `Comparison` (R19) |
| POST | `api/test/load-batch` | `{label, fixture_dir}` | **test mode only** (404 unless `REVIEW_TEST_MODE=1`, R24): copies every file of `fixture_dir` (a path under `fixtures/`, e.g. `fixtures/batch_v1`) into `run_history/<label>/`, creating it, and returns `{label, runs}`, rewriting `label` in the copied `summary.json` to the given label; this is what "`fixtures/batch_v1` loaded as `v1`" means in §5 |
| POST | `api/test/load-proposal` | `{label, fixture_file}` | **test mode only** (404 otherwise): reads `fixture_file` (a `HarnessChange` under `fixtures/proposals/`) and writes `run_history/proposal_<label>.json` (the change, `applied: false`, `applied_at: null`) and `run_history/proposal_<label>.md` (its `change` text as the reasoning); returns `{label}`; this is what "`prompt_change.json` as proposal `p1`" means in §5 |

Run-starting endpoints (`POST api/tickets`, `.../rerun`, `.../versions`, `api/batches`) return within
2 seconds with the run or batch id and let the work continue in the background; the page polls
`api/runs/{id}` / `api/batches/{label}` until `state == "done"` (R23).

## 4. Business Rules

Labels: **course-demonstrated** `(CTX-…)`, **project hardening**, `[environment]`, and the one
sanctioned co-label **course-demonstrated, reinforced `[environment]`**.

1. **R1 — Fetch by id, never by hand.** The review agent is built with no document; its opening
   message names only a ticket key ("The requirement document is tracked as ticket X. Fetch it to
   begin.") and the text reaches it only through its `fetch_requirement` tool. *Tool name — contradicted
   in the materials:* the helper and the Lesson 4 narration say `fetch_requirement`; the two
   batch-snapshot instruction files and slide 3.5 say `fetch_requirement_from_jira`. The narrated name
   wins (CTX-C "Fetch tool name"); `fetch_requirement` is used everywhere in this spec. (course-demonstrated;
   Lesson 4 + helper docstring, CTX-A stage 2) → AC5
2. **R2 — Retry a transient tool failure with the same call.** The fetch tool can return an error
   string instead of a document; the agent's instructions and the tool's description both tell it to
   call the same tool again with the same arguments until it succeeds. The fixture ticket `OUT-900`
   fails twice (a 503, then a 10-second timeout) before returning its document. Value provenance: the
   Lesson 4 narration states two simulated failures and the shipped pre-recorded trace contains them,
   while the helper's shipped constant is 0 ("a clean fetch") and the batch runner also uses 0 —
   contradicted; stakes test fails (a number), so this is a **post-build lever** resolved by lever
   rule branch (1), the narrated value, 2. (course-demonstrated, CTX-B1) → AC5
3. **R3 — The analysis is a file, built stage by stage.** The deliverable is `/analysis.md` in the
   run workspace with the §3.1 heading sequence; the instructions direct the agent to write the
   skeleton once with only Confirmed Facts filled, then fill one section per `edit_file` call, in
   order, one tool call per turn, and to end with one short confirming sentence and no further tool
   calls. Order is *requested*, not enforced: the harness records the order sections were actually
   written and whether any ended empty; filling two sections in one successful edit is not a
   violation, filling one out of order or leaving one empty is; a failed edit (non-unique
   `old_string`) counts no section — it is recorded in `stages` with its error (§3.2) and the run
   continues. (course-demonstrated; helper docstring, CTX-A stage 3, CTX-B16) → AC8, AC31, AC-L1
4. **R4 — Output shape constraints.** Ambiguities bullets quote the exact clause in bold and carry an
   indented `Reason:` line; the Summary is two or three sentences; Confirmed Facts record only what
   the document states ("do not infer"); questions ask what a reviewer needs answered before work can
   start; assumptions state what a developer would end up assuming if nobody answered. The
   **baseline** instructions deliberately do NOT ask for `Resolved by:` / `Edge case:` lines — that
   omission is the systematic gap the learning loop must find (CTX-B8). (course-demonstrated) →
   AC8, AC11
5. **R5 — Instructions are a file the agent reads and cannot write.** The agent's instructions live at
   `/memories/AGENTS.md` *inside its own run workspace* (never at the lab workspace root — see Never
   tier; *filename — contradicted in the materials:* the course's code and Lesson 4 say `AGENTS.md`,
   slide 3.4 and parts of Lesson 3 say "Agent.md"; the application's own config wins, CTX-C
   "Instructions file name"), are loaded into context at the start of every run, and writes under `/memories/**` are
   denied by the harness's filesystem permissions rather than by the prompt. The agent's file tools
   see the run workspace as `/` and cannot reach above it. Building an agent whose workspace lacks the
   instructions file fails loudly — a silently ignored missing file produces a plausible bad review.
   (course-demonstrated; helper comments, CTX-B5, CTX-B6) → AC4, AC34
6. **R6 — One fresh workspace per run.** Every run gets its own workspace seeded from the instructions
   under test; no `/analysis.md` pre-exists (a stale one lets the agent read it and skip stages); runs
   never see each other's files; the workspace may be deleted once the run record is written. The
   run function also accepts an explicit workspace directory (a test hook); whatever that directory
   already holds, the harness removes any `/analysis.md` from it before the agent's first tool call.
   (course-demonstrated; CTX-B4) → AC6, AC33
7. **R7 — A turn cap that is not the normal stop.** Model calls per run are capped and the run ends
   when the cap is hit: 12 for an agent-only run (Lesson 4 notebook, helper default), 40 when a grader
   can send work back (Lesson 5 notebook, event app, batch runner), 40 for the analyst. When the cap
   stops a run whose file is incomplete, the record's `stop_reason` is `turn_limit` and the trace's
   last action reads `Stops: turn limit of <N> reached` — never "Finishes the review". These are body
   defaults, not contradictions: each value belongs to a different loop depth. (course-demonstrated;
   CTX-B7) → AC7, AC-L1
8. **R8 — The rubric defines done.** Three criteria, in this order and with these names: `completeness`
   (every clause of the requirement is addressed somewhere in the analysis), `clarity` (every
   Ambiguities bullet has an indented `Resolved by:` line naming the fact or decision that settles
   it), `depth` (every Ambiguities bullet has an indented `Edge case:` line naming a concrete
   production failure the ambiguity could cause). Each is pass/fail with a `gap` on fail; the run is
   `satisfied` only when all three pass in the *same* pass; otherwise the gaps go back to the agent as
   feedback and it revises the same file. The grader may send work back at most **3** times (lever:
   the Lesson 5 narration and notebook and the batch runner say 3; the shipped event app uses 2 —
   contradicted, stakes test fails, lever rule branch (1) → 3, **post-build lever**); with the budget
   at 0 the build is the plain agent loop. (course-demonstrated; Lesson 5, CTX-B2) → AC10, AC11, AC12,
   AC16
9. **R9 — The grader judges the file, not the conversation.** Whatever realizes the grader (row D-S1)
   judges `/analysis.md` as produced, never the agent's conversation. When the grader is a model call
   (the D-S1 default): it has exactly one tool, `read_file` over the run workspace, and must read
   `/analysis.md` before judging; it passes a criterion only after quoting the satisfying text
   verbatim with its line number (`evidence` on the criterion, §3.2); a labelled-line criterion is
   satisfied only by that exact label; a coverage criterion is checked item by item, not sampled;
   anything it cannot positively confirm fails with a gap saying what evidence would be needed. A
   deterministic check (D-S1 (b), (c)) records the matched line as its `evidence` instead; a person
   (D-S1 (d)) returns the verdicts and gaps on the page with no `evidence` required. The harness does
   not accept a model or deterministic verdict that skipped the file or passed a criterion without
   `evidence` — it is recorded as `grader_error` (§3.2). Results are `satisfied` / `needs_revision` /
   `failed` (malformed rubric), and a grader exception is recorded as `grader_error` with no criteria.
   (course-demonstrated; the course's grader prompt exists because a transcript-judging grader "passes
   criteria the file does not satisfy", CTX-B3) → AC9, AC10 (live L2), AC11, AC12, AC32
10. **R10 — Status distinguishes satisfied from out-of-tries.** When the send-back budget is spent,
    the last grading pass still reads `needs_revision`; the run's `status` is `max_iterations_reached`,
    never `satisfied`. (course-demonstrated; CTX-B12) → AC12
11. **R11 — Every grading pass keeps the file as it saw it.** Each pass records `analysis_markdown`
    at grading time, so a run shows the draft the grader rejected next to the revision it accepted.
    (course-demonstrated; Lesson 5 notebook) → AC11
12. **R12 — Events start runs; closed tickets never re-run.** Creating a ticket linked to a
    requirement page starts a run; saving a new version of a requirement page starts one run per
    ticket linked to it whose status is not `Done`; "re-run now" starts one for an open ticket; a
    `Done` ticket is never re-run (409). Each run records the requirement version it analyzed and the
    ticket records `last_analyzed_version` and `last_run_id`. (course-demonstrated; event app,
    CTX-A stage 1; row D-A2 default) → AC14, AC15, AC17, AC-L3
13. **R13 — The requirement is the source of truth; the report is a separate, versioned page.** The
    agent never writes to a requirement page; only humans add requirement versions (400 on any other
    kind). Each run writes its result as a *new version* of the agent-authored report page for that
    ticket (title, author and banner per §3.5), so the page's version history shows every past
    analysis and any two versions diff. After a run the ticket is `Analysis Ready` and carries a bot
    comment naming the status, the requirement version and the report page. (course-demonstrated;
    event app README) → AC14, AC16, AC34, AC-L3
14. **R14 — Only a human marks Done.** The agent never closes its own work; `Done` is reachable only
    through the close action, and a run never changes a `Done` ticket's status. (course-demonstrated;
    Lesson 2 oversight + event app; row D-A3 bake-in, litmus: the course never shows an agent closing
    its ticket as acceptable) → AC17, AC18, AC34
15. **R15 — Every run is written to disk as a record.** Each run persists a `RunRecord` (§3.2): the
    trace, every grading pass with its file snapshot, the final file, the instructions it was given,
    status, turns, counts; batch runs additionally persist every message untruncated with full tool
    arguments ("the story is in the traces"); each batch persists its instructions snapshot and
    `summary.json`; proposals and comparisons are files too. **Course-demonstrated, reinforced
    `[environment]`**: the course writes the analysis, every run and the proposal to files ("the
    analysis is a file"; run history "with everything kept"), and the lab independently requires it
    because the workspace is the record — a new chat has no memory and the grader sees only disk.
    The record structures §2 declares (`data/*.json`, `run_history/`) exist from the first start,
    before any run; records outlive the process that wrote them — a freshly started server reads an
    earlier process's batches and runs from disk. (CTX-A stage 5) → AC3, AC19, AC29, AC30, AC35
16. **R16 — The batch signal is first-attempt pass rate per criterion, by position.** A batch reviews
    every fixture document once under one instructions file (≥ 2 documents — a batch request naming
    fewer is refused with 400 and a message naming the minimum; the fixture corpus has 5). The
    summary counts, per criterion, how many graded runs passed it on the *first* grading pass;
    criteria are identified by rubric position, never by the grader's wording (it paraphrases names
    run to run); runs whose first pass is a `grader_error` are excluded from every denominator and
    reported as `grader_errors`, never averaged away; `revisions_needed` is the number of graded runs
    whose first pass failed anything. Recurring gaps are grouped by criterion position with the
    document named under each. (course-demonstrated; batch runner, CTX-B10, CTX-B11) → AC20, AC21,
    AC22, AC23, AC29, AC30, AC36
17. **R17 — The analyst reads evidence it cannot change and proposes one change.** The analyst role
    (`ANALYST_MODEL`) is a file-tool agent rooted at the batch directory `run_history/<label>/` (least
    privilege: it can read only the batch under analysis) with read tools over everything under that
    root and write permission for exactly one file, `/proposal.md` — on disk
    `run_history/<label>/proposal.md` (any other write is denied); the app derives its stored
    proposal record from that file (§3.4).
    It starts from the summary, then reads individual runs for evidence, then the instructions the
    batch ran with; it proposes exactly one change (§3.4) whose `evidence` entries are quoted verbatim
    from the runs (not paraphrased), whose `change` is literal insertable text with exact labels when
    a labelled line is required, and which does not restate instructions already present. A criterion
    failing in **most** graded runs (more than half — the course's "most runs"; "a problem appearing in
    one run out of five is not a pattern") is a property of the agent; anything seen in fewer goes in
    `rejected` with the reason. (course-demonstrated; analyst prompt + module docstring, CTX-B8, CTX-B9)
    → AC9, AC24 (live L4), AC29, AC30
18. **R18 — Propose, never apply; a human approves; only prompt targets apply.** The analyst never
    edits the instructions. Applying requires an explicit approval action on the page. Application is
    deterministic text work — the `change` is inserted at the end of the named section (the section
    ends at the next heading of the same or shallower depth), nothing else in the file changes, and
    the result ends with a newline. A proposal whose `target` is not `prompt` is shown for a human to
    read and is never applied automatically (400); a `prompt` proposal naming a section the file does
    not contain applies nothing (422). The applied instructions are saved as a new labelled snapshot;
    the baseline file is never edited in place. (course-demonstrated; Lesson 6 "human-in-the-loop
    reviewed this proposal and approved"; module docstring; row D-A3 bake-in, litmus: auto-apply is
    only ever named as the thing to avoid, CTX-B14) → AC25, AC26, AC29, AC30
19. **R19 — Measure the change under the same rubric.** After applying, the batch re-runs under the
    new snapshot as a new label; the comparison reports per-criterion first-attempt counts before and
    after, `revisions_needed` before and after, and the §3.3 verdict. A regression on any criterion
    is reported as `regression` regardless of other gains. (course-demonstrated; Lesson 2 "how do you
    feel confident with that merge? By running your eval suite and making sure there are no
    regressions", Lesson 6) → AC27, AC28, AC29, AC30
20. **R20 — Platform models through three roles; keys from the environment.** `[environment]`
    (resolution CONSTRAINED): the app reads provider keys and base URLs from the container's exported
    environment, uses platform models for the `agent`, `grader` and `analyst` roles via the three
    model-id variables in §2, never hardcodes a key, and never asks the learner for one — a missing
    key is reported as a configuration error naming the variable, not a prompt for input — the one
    exception is test mode, `REVIEW_TEST_MODE=1` (R24), in which no model is called and the key check
    is waived. Each role's
    model must support native tool calling; the analyst's must return structured output; the grader's
    must be able to call `read_file`. *Tiering lever* (course-demonstrated, not a Ledger row — the
    sides differ only in a model id): the course ran agent and grader on the same cheaper model
    ("having a different model for grader is a common production choice") and the analyst on its more
    capable one ("reading five full run traces and finding what recurs is the one job the cheaper
    model does unreliably"); keep that tiering when the platform offers more than one tier. → AC1, AC30
21. **R21 — One server on port 4000.** `[environment]` One process serves the page and `api/*` on
    `0.0.0.0:4000`; nothing else is previewable. → AC2
22. **R22 — Every URL in the page is relative.** `[environment]` The preview is reverse-proxied under
    a path prefix, so `api/thing` works and `/api/thing` resolves against the IDE and breaks; the page
    and any script or stylesheet it loads contain no root-absolute (`/...`) or absolute-origin URLs.
    → AC2
23. **R23 — HTTP only, progress by polling.** `[environment]` No WebSocket is opened; run-starting
    endpoints answer within 2 seconds with an id and the page polls the status endpoint until
    `state == "done"`; the page shows a run as in progress meanwhile. → AC13
24. **R24 — The offline suite drives the loops with an honestly labelled scripted stand-in.** The
    agent, grader **and analyst** roles each accept an injected model so the §7 offline suite can run
    the loops with `fixtures/scripted_model.py` — a fake that replays canned tool calls, canned grading
    verdicts and a canned proposal, named as a fake in its own description — with no network and no
    key; test mode — the environment variable `REVIEW_TEST_MODE=1`, read by the server at startup —
    injects the same scripts into the running server and waives R20's key check, since no model is
    called. In test mode the server selects its scripts from three environment variables read at
    startup: `REVIEW_SCRIPT` (default `REVIEW_OK`; after grader feedback every review script except
    `REVIEW_RUNAWAY` continues with `REVIEW_REVISE`), `GRADER_SCRIPT` (default
    `GRADER_FAIL_THEN_PASS`) and `ANALYST_SCRIPT` (default `ANALYST_WRITES_EVIDENCE`, the only
    analyst script); test mode also enables `api/test/load-batch` (§3.6). Real-model behaviour is
    exercised only by the `live` criteria. (project hardening: the course replayed *recorded* results
    offline; driving the live loop with a scripted model is this spec's addition) → AC1, AC4–AC7,
    AC9, AC10, AC12, AC13, AC20, AC31–AC36

## 5. Acceptance Criteria                ★  (the oracle)

### Fixture corpus (authored for this spec; no course data copied)

All fixtures live under `fixtures/`. Module filenames are importable identifiers.

- `fixtures/tickets.json` — the stand-in ticket store (an honestly labelled fake of a tracker; the
  file's top-level `"_note"` says so). Six tickets, key → document:
  - `SESS-301` "Session Timeout Policy" — body: `REQUIREMENT: Session Timeout Policy` / "Sessions
    should expire after a reasonable period of inactivity." / "Users must be warned before they are
    logged out." / "Administrators should be able to adjust the policy."
  - `EXPO-412` "Report Export" — "Users shall be able to export reports." / "Exports should complete
    quickly." / "Large exports must not degrade the system for other users." / "Supported formats
    should cover common needs."
  - `RATE-118` "API Rate Limiting" — "Clients shall be rate limited fairly." / "Limits must be
    communicated clearly." / "Bursts should be tolerated within reason." / "Abusive clients must be
    blocked."
  - `BACK-207` "Nightly Backups" — "The system shall back up data nightly." / "Backups must be
    restorable." / "Retention should be sensible." / "Failures must be reported to someone."
  - `SRCH-509` "Product Search" — "Users shall be able to search products." / "Results should be
    relevant." / "Search must be fast." / "Typos should be tolerated."
  - `OUT-900` "Outage Notifications" — "Customers shall be told about outages." / "Notices should go
    out quickly." / "The tone should be appropriate." — **planted failure (CTX-B1):** the stand-in
    serves this ticket with two errors first — `Error fetching ticket: 503 Service Unavailable. The
    tracker is temporarily unreachable, please retry.` then `Error fetching ticket: request timed out
    after 10s. Please retry.` — and the document on the third call; the attempt counter is per built
    agent.
- `fixtures/requirements/` — the batch corpus: `01_session_timeout.md`, `02_report_export.md`,
  `03_api_rate_limiting.md`, `04_nightly_backups.md`, `05_product_search.md`, each byte-identical to
  the matching ticket body above (the batch seeds each into the stand-in under the batch ticket key
  `BATCH-1`).
- `fixtures/instructions_baseline.md` — the review agent's baseline instructions (the file copied to
  `/memories/AGENTS.md` in every run workspace): procedure per R3 (fetch first; skeleton with
  Confirmed Facts; one section per edit in order; retry a failed tool call with the same arguments;
  never modify the requirement; never edit this file; finish with one sentence) and review guidance
  per R4. **Planted gap (CTX-B8):** its Ambiguities guidance asks only for the quoted clause and a
  `Reason:` line — nothing about `Resolved by:` or `Edge case:`. **Heading structure (R18 relies on
  it):** one level-1 title `# Review Agent Instructions`; two level-2 sections `## Procedure` and
  `## Review guidance`; under `## Review guidance`, exactly five level-3 sections in this order —
  `### Confirmed Facts`, `### Ambiguities`, `### Clarification Questions`, `### Assumptions`,
  `### Summary` — and no other level-3 heading anywhere (in particular no `### Tone`, which
  `missing_section.json` names). The `### Ambiguities` section therefore ends at
  `### Clarification Questions`, the next heading of the same depth.
- `fixtures/workspace_no_instructions/` — **planted failure (CTX-B5):** a run-workspace template whose
  `memories/` directory exists but is empty (held in git by `memories/.gitkeep`) — no `AGENTS.md`.
  AC4 builds the review agent on a copy of it.
- `fixtures/stale_analysis.md` — **planted failure (CTX-B4):** a complete five-section analysis of
  `SESS-301` with three Ambiguities bullets (each with `Reason:`, `Resolved by:` and `Edge case:`
  lines) and the Summary "This analysis is stale and must not survive a fresh run." AC33 copies it
  to `analysis.md` in a run's workspace before the run starts.
- `fixtures/seed_pages.json` — one requirement page `page-req-session-timeout`, title "Session
  Timeout Policy — Requirements", version 1 body = the `SESS-301` text, author "Dana (Product
  Manager)"; `fixtures/seed_tickets.json` — one open ticket `REQ-104` "Review requirements: Session
  Timeout Policy" linked to that page, assignee "Jordan (Eng Lead)", no runs. (Fixed cast of names:
  Dana, Jordan, Priya, Sam, Morgan — the course used a fixed cast; names here are this spec's.)
- `fixtures/batch_v1/` — a canned batch of five `RunRecord`s (`run_01_01_session_timeout.json` …
  `run_05_05_product_search.json`), `AGENTS.md` (= baseline) and `summary.json`, under the baseline
  instructions. Facts: every run has two grading passes, first `needs_revision`, second `satisfied`;
  on the first pass `completeness` passes in runs 1, 2, 4, 5 and fails in run 3 with gap "the clause
  'Abusive clients must be blocked' is not addressed anywhere"; `clarity` and `depth`
  fail in all five with gaps that each contain the exact phrases `"Resolved by:"` and `"Edge case:"`
  (worded differently per run — e.g. run 1 "each ambiguity bullet lacks an indented 'Resolved by:'
  line", run 2 "no 'Resolved by:' line follows any Reason: line"); the grader's criterion names vary
  in wording across runs (`Completeness`, `completeness — coverage`, `1. completeness`) to exercise
  position-based grouping. `summary.json` therefore reads: label `v1`, model `scripted_model (fake)`,
  runs 5, graded 5, grader_errors 0, first_attempt completeness 4/5 (0.8), clarity 0/5 (0.0), depth
  0/5 (0.0), revisions_needed 5, documents = the five corpus stems in order. (Every canned batch's
  `summary.json` carries its directory suffix as `label` — `v1`, `v1_err`, `v2`, `v2_regress` — and
  the same `model` and `documents`; `api/test/load-batch` rewrites `label` on load.)
- `fixtures/batch_v1_err/` — the same five runs except run 4's only grading pass is
  `{"iteration": 1, "result": "grader_error", "explanation": "grader raised: RuntimeError: simulated
  grader failure", "criteria": [], "analysis_markdown": <the file exactly as it stood at that pass>}`
  (validating against §3.2) with status `grader_error`; its `summary.json` reads
  runs 5, graded 4, grader_errors 1, completeness 3/4 (0.75), clarity 0/4, depth 0/4,
  revisions_needed 4.
- `fixtures/batch_v2/` — five runs under `fixtures/instructions_v2.md` (baseline plus the applied
  `prompt_change` below), each with one `satisfied` pass; `summary.json`: 5/5 on all three,
  revisions_needed 0. `fixtures/batch_v2_regress/` — like v2 but runs 2 and 3 each fail
  `completeness` on their first pass (every later pass fails it too; status `max_iterations_reached`
  after exhausting the budget) while clarity and depth pass; summary completeness 3/5 (0.6), clarity
  5/5, depth 5/5, revisions_needed 2 — so v1 → v2_regress is a *fall* on completeness (4 → 3), which
  is what R19 calls a regression.
- `fixtures/proposals/prompt_change.json` — `HarnessChange` with `target: "prompt"`, `section:
  "### Ambiguities"`, `change`: "After the `Reason:` line, add two indented labelled lines to every
  ambiguity bullet:\n\n```\n  Resolved by: the fact or decision that would settle this ambiguity\n
  Edge case: one concrete production failure if it stays unresolved\n```", `evidence` = the five
  clarity gaps from `batch_v1` verbatim, `rejected` = ["run 3 missed one clause (completeness); a
  single run is not a pattern"]. `fixtures/proposals/tool_change.json` — same shape with `target:
  "tool"`, `section: ""`. `fixtures/proposals/missing_section.json` — `target: "prompt"`, `section:
  "### Tone"` (not present in the baseline).
- `fixtures/instructions_v2.md` — exactly what applying `prompt_change.json` to the baseline must
  produce (the change inserted after the last non-blank line of the `### Ambiguities` section, one
  blank line before and after, nothing else touched, trailing newline).
- `fixtures/scripted_model.py` — the honestly labelled fake model (R24). Scripts:
  `REVIEW_OK` — fetch, (on error) fetch again, (on error) fetch again, `write_file` skeleton with two
  Confirmed Facts, `edit_file` Ambiguities (two bullets with `Reason:` only), `edit_file` Clarification
  Questions (two), `edit_file` Assumptions (one), `edit_file` Summary (two sentences), final message
  "Review complete."; `REVIEW_REVISE` — after grader feedback, one `edit_file` adding `Resolved by:`
  and `Edge case:` lines under both ambiguities, then "Revised."; `REVIEW_RUNAWAY` — calls fetch
  forever; `GRADER_FAIL_THEN_PASS` — every pass begins with `read_file /analysis.md`; pass 1:
  completeness pass (with `evidence` quoting the first Confirmed Facts bullet and its line), clarity
  fail (gap "no 'Resolved by:' line under either ambiguity"), depth fail (gap "no 'Edge case:' line
  under either ambiguity"); pass 2: all pass, each with `evidence` quoting a line of the file;
  `GRADER_ALWAYS_FAIL` — always the pass-1 verdict (read first, evidence on the pass); `GRADER_RAISES`
  — throws; `GRADER_NO_READ` — **planted failure (CTX-B3):** never calls `read_file` and returns all
  three criteria passed with no `evidence` (the resemblance verdict: the conversation "looks like" a
  satisfying run);
  `REVIEW_WRITES_INSTRUCTIONS` — fetch, then `write_file` to `/memories/AGENTS.md` (body "hijacked"),
  then `edit_file` on `/memories/notes.md`, then `read_file` of `/../spec.md`, then the `REVIEW_OK`
  sequence from the skeleton onward (the three denied calls are each followed by the next call
  regardless of the result); `REVIEW_BAD_EDIT` — the `REVIEW_OK` sequence except that its first
  Ambiguities `edit_file` uses `old_string: "## A"` (which matches both `## Ambiguities` and
  `## Assumptions` in the skeleton, so the edit is rejected as non-unique; its first occurrence is the
  `## Ambiguities` heading line, so the derived `section` is `Ambiguities`, §3.2), then
  `read_file /analysis.md`, then the Ambiguities `edit_file` again with the unique anchor
  `## Ambiguities\n`, then continues as `REVIEW_OK` (so on a clean fetch it ends with `turns == 9`,
  two more than `REVIEW_OK`'s 7); `REVIEW_OVERREACH` — **planted failure (CTX-B13):** fetch, then a
  tool call named `close_ticket` with `{key}`, then a tool call named `save_requirement_version` with
  `{page_id, body: "rewritten by the agent"}` (neither tool exists for the review agent), then
  `write_file` to `/../data/pages.json` (escapes the virtual root), then the `REVIEW_OK` sequence from
  the skeleton onward — each of the three rejected calls is followed by the next regardless of its
  result; `ANALYST_WRITES_EVIDENCE` — for the analyst role (rooted at the batch directory, R17):
  `read_file /summary.json`, then `write_file` to `/summary.json` (body "tampered"), then `write_file`
  to `/proposal.md` with the text of `fixtures/proposals/prompt_change.json`'s `change`, then returns
  `prompt_change.json` as its structured proposal. Every canned batch (`batch_v1`, `batch_v1_err`,
  `batch_v2`, `batch_v2_regress`) carries `evidence` on every passed criterion of every pass.
- `fixtures/page_urls.txt` — not a fixture of data but of the check: the list of regexes that must not
  match the served page or its assets: `(href|src|fetch\(|url\()\s*=?\s*["'`]/` and `https?://`.

### Given / When / Then

`live` = requires the container's ambient model credentials; excluded from the offline run.

| AC | Given | When | Then |
|---|---|---|---|
| AC1 | a fresh checkout, provider key and base URL exported, three role variables set | the server starts | `GET api/health` returns `{"ok": true, "port": 4000}`; the process logs the three role model ids and the provider base URL host, never a key; with the key variable unset and `REVIEW_TEST_MODE` unset the process exits with a message naming that variable and never prompts; with the key variable unset and `REVIEW_TEST_MODE=1` it starts and `api/health` answers (R20, R24) |
| AC2 | the server running | `GET /` and every asset it references are fetched | HTTP 200; the server is bound to `0.0.0.0:4000` (socket check); no line of the page or any served script/stylesheet matches `fixtures/page_urls.txt` (R21, R22) |
| AC3 | a fresh `data/` directory | the server starts | `data/tickets.json`, `data/pages.json`, `data/runs.json` exist as JSON lists; `tickets.json` holds exactly `REQ-104` (status `Open`, `last_run_id` null); `pages.json` holds exactly `page-req-session-timeout` with one version; `run_history/` (project root, beside `data/`) exists and is empty — the existence check for every persistent structure §2 declares, run before any other behaviour (R15) |
| AC4 | a run workspace copied from `fixtures/workspace_no_instructions/` (its `memories/AGENTS.md` is missing) | the review agent is built | it raises an error naming the missing path; and given a built agent on `SESS-301` with scripted `REVIEW_WRITES_INSTRUCTIONS`, when the loop runs, the `write_file` to `/memories/AGENTS.md` and the `edit_file` to `/memories/notes.md` both return denials (their trace `detail` is an error, not a success) and `/memories/AGENTS.md` is byte-identical to the baseline afterwards with no `/memories/notes.md` created; the `read_file` of `/../spec.md` fails; the run still finishes with a complete file (R5, R24) |
| AC5 | ticket `OUT-900`, scripted `REVIEW_OK`, agent-only (budget 0, cap 12) | the loop runs | the opening message contains `OUT-900` and not the document text; the trace holds three `fetch_requirement` Tool rows — the first two with `detail` starting `Error fetching ticket` — then `write_file: Confirmed Facts`, then four `edit_file` rows named Ambiguities / Clarification Questions / Assumptions / Summary, then `Finishes the review`; `turns == 9`, `len(trace) == 17`; `stop_reason == "finished"`; `status == "ungraded"` (R1, R2, R24) |
| AC6 | two consecutive runs on `SESS-301` with scripted `REVIEW_OK` | both complete | each run used a different workspace path; neither workspace contained `/analysis.md` before its first tool call; each record's `instructions` equals `fixtures/instructions_baseline.md` byte for byte (R6, R24) |
| AC7 | ticket `SESS-301`, scripted `REVIEW_RUNAWAY`, cap 4 | the loop runs | `stop_reason == "turn_limit"`, the last trace action is `Stops: turn limit of 4 reached`, `turns == 4`, and the file is not complete (R7, R24) |
| AC8 | the AC5 run's record | parsed per §3.1 | `counts == {"Confirmed Facts": 2, "Ambiguities": 2, "Clarification Questions": 2, "Assumptions": 1}`, `summary_words > 0`, headings in the §3.1 order, each ambiguity has `clause` and `reason` and no `resolved_by`; the record's `stages` has five entries all `ok: true`, `stage_order == ["Confirmed Facts", "Ambiguities", "Clarification Questions", "Assumptions", "Summary"]` and `in_order == true` (§3.2) (R3, R4) |
| AC9 | the grader role wired; test mode, `fixtures/batch_v1` loaded as `v1` via `api/test/load-batch`, the analyst role on scripted `ANALYST_WRITES_EVIDENCE` | the grader's tool list is inspected; `POST api/batches/v1/propose` | the grader has exactly one tool, named `read_file`, scoped to the run workspace; the analyst's `write_file` to `/summary.json` is denied and `run_history/v1/summary.json` is byte-identical to the loaded fixture, its `write_file` to `/proposal.md` succeeds and lands at `run_history/v1/proposal.md`, and after the load nothing under `run_history/` was created or changed except that file and the app's own `run_history/proposal_v1.json` / `proposal_v1.md`; the stored proposal's `rejected` holds exactly one entry, and it names run 3 and `completeness` — the planted one-off miss is rejected as not a pattern, with its reason (R9, R17, R24) |
| AC10 | `SESS-301`, scripted `REVIEW_OK` + `REVIEW_REVISE`, grader `GRADER_FAIL_THEN_PASS`, budget 3, cap 40 | the verification loop runs | `status == "satisfied"`; `len(grading) == 2`; pass 1 `result == "needs_revision"` with criteria `[completeness pass, clarity fail (gap present), depth fail (gap present)]` in that order; pass 2 all pass; **live L2** with real models on `SESS-301`: a terminal status in `{satisfied, max_iterations_reached}` and every pass has three criteria in rubric order — or `status == "grader_error"` with the last pass's `explanation` starting `grader verdict rejected:` (the real grader omitted evidence or skipped the file), in which case the test reports the rejection and is **inconclusive**, not failed (R8, R9, R24) |
| AC11 | the AC10 record | its passes are compared | pass 1's `analysis_markdown` contains no `Resolved by:`; pass 2's and the final file contain `Resolved by:` and `Edge case:` under both ambiguities; the final file is the same path that pass 1 graded (R4, R8, R9, R11) |
| AC12 | `SESS-301`, scripted `REVIEW_OK` + `REVIEW_REVISE`, grader `GRADER_ALWAYS_FAIL`, budget 2 | the loop runs | `status == "max_iterations_reached"`, `len(grading) >= 2`, every pass `needs_revision`; with grader `GRADER_RAISES` instead: `len(grading) == 1`, `grading[0].result == "grader_error"`, `criteria == []`, `status == "grader_error"` (R8, R9, R10, R24) |
| AC13 | the server in test mode with the default scripts (`REVIEW_OK`/`REVIEW_REVISE`, `GRADER_FAIL_THEN_PASS`) | `POST api/tickets/REQ-104/rerun`, then `GET api/runs/{id}` polled every 250 ms | the response arrives in < 2 s with a `run_id`; polling reaches `state == "done"` within 30 s and the terminal record has `status == "satisfied"` (observing `state == "running"` on the way is expected but not asserted — a scripted run is short); server-side, the app's route table contains no WebSocket route and the poll endpoint is a plain HTTP `GET`. *live (manual)*: the ticket view shows an in-progress indicator while the poll runs and the latest run afterwards — observed by the learner in the preview, not asserted by the suite (R23, R24) |
| AC14 | the seed data, test mode with the default scripts | `POST api/tickets` `{title: "Review: Report Export", description: "", linked_page_id: "page-req-session-timeout", assignee: "Priya (QA Lead)"}` | a ticket `REQ-105` is created with status `Open` and a `run_id`; when done, `GET api/tickets/REQ-105` shows status `Analysis Ready`, `last_analyzed_version == 1`, `last_run_id == run_id`, one bot comment whose text contains `Analysis Report — REQ-105` (R12, R13) |
| AC15 | `REQ-104` analysed once (version 1) | `POST api/pages/page-req-session-timeout/versions` `{body: "<v1 text> Sessions expire after 30 minutes.", author: "Dana (Product Manager)"}` | response `retriggered == ["REQ-104"]` (and `REQ-105` if AC14 ran); a new run per retriggered ticket records `requirement_version == 2`; `GET api/tickets/REQ-104` returns `previous_run` and `latest_run` with versions 1 and 2 and a non-null `what_changed`; the page renders the "what changed" table defined in §3.6 — one row per §3.1 list section with that section's bullet count under each of the two runs (R12) |
| AC16 | AC15 complete (test mode, default scripts — so each run ends `satisfied` after two passes) | `GET api/pages/page-analysis-req-104` | kind `analysis_report`, `linked_ticket == "REQ-104"`, author of every version `Requirements Analysis Agent (bot)`, two versions, version 2's body starts with a `>` banner line containing `REQ-104`, then a line containing `version 2`, then a line containing the status and `N grading pass` with `N >= 1` — the event-started run behind version 2 has `len(grading) >= 1` and a terminal status in `{satisfied, max_iterations_reached}` (the trigger wrapped verification, not the bare agent loop); `GET api/pages/page-analysis-req-104/compare?a=1&b=2` returns a non-empty unified diff and both `run_a` and `run_b`; `POST api/pages/page-analysis-req-104/versions` returns 400 and adds no version (R8, R13) |
| AC17 | `REQ-104` at `Analysis Ready` | `POST api/tickets/REQ-104/close`, then a new requirement version is saved | status `Done`; `retriggered == []` for that ticket; `POST api/tickets/REQ-104/rerun` returns 409; no new run for `REQ-104` exists (R12, R14) |
| AC18 | any run finishing on any ticket | the run completes | the ticket's status is `Analysis Ready` (never `Done`) and no code path other than the close action writes `Done` (grep + behavioural check: a run on a `Done` ticket cannot start) (R14) |
| AC19 | the AC10 run and a batch run | records are inspected on disk | `data/runs.json` holds a `RunRecord` validating against §3.2 with non-empty `trace`, `grading`, `analysis_markdown`, `instructions`; the batch run file additionally has `messages` where at least one entry has a non-empty `tool_calls[0].args`; `run_history/<label>/AGENTS.md` equals the instructions used (R15) |
| AC20 | test mode with the default scripts (`REVIEW_OK`/`REVIEW_REVISE`, `GRADER_FAIL_THEN_PASS`) | `POST api/batches` `{label: "t1", instructions_source: "baseline"}` | when done, `run_history/t1/` holds `AGENTS.md`, five `run_0N_<doc>.json` in corpus order and `summary.json` with `runs == 5`, `graded == 5`, `documents` equal to the five corpus stems in order; `first_attempt` reads completeness 5/5, clarity 0/5, depth 0/5, `revisions_needed == 5` (R16, R24) |
| AC21 | test mode, `fixtures/batch_v1` loaded as label `v1` via `api/test/load-batch` | `GET api/batches/v1` | `summary` equals the fixture's `summary.json` field by field — `label == "v1"`, `model == "scripted_model (fake)"`, `runs`, `graded`, `grader_errors`, every `first_attempt` entry, `revisions_needed`, and `documents` equal to the five corpus stems in order; `recurring_gaps` has 5 entries under `clarity`, 5 under `depth`, 1 under `completeness` (document `03_api_rate_limiting`), grouped despite the varied criterion wording (R16) |
| AC22 | test mode, `fixtures/batch_v1_err` loaded as `v1e` via `api/test/load-batch` | `GET api/batches/v1e` (the stored summary — computed at batch end from the runs; for a loaded fixture, the fixture's file) | `label == "v1e"`, `graded == 4`, `grader_errors == 1`, every `total == 4`, completeness `passed == 3` and `pass_rate == 0.75`, `revisions_needed == 4` (R16) |
| AC23 | a batch of zero graded runs | summary computed | every `pass_rate` is `null`, no division error (R16) |
| AC24 | `v1` loaded | `POST api/batches/v1/propose` **live L4** | the response validates against §3.4; `target == "prompt"`; every `evidence` string occurs verbatim in some grading `gap` of the v1 runs; `change` contains both `Resolved by:` and `Edge case:`; `run_history/v1/proposal.md` (the analyst's own file), `run_history/proposal_v1.md` and `proposal_v1.json` exist; the analyst wrote no file other than `run_history/v1/proposal.md` (R17) |
| AC25 | test mode; baseline instructions; `fixtures/proposals/prompt_change.json` registered as proposal `p1` via `api/test/load-proposal` | `POST api/proposals/p1/apply` `{approved: true, new_label: "v2"}` | `run_history/v2/AGENTS.md` is byte-identical to `fixtures/instructions_v2.md`; `fixtures/instructions_baseline.md` is unchanged; the response `diff` shows only added lines; `GET api/proposals/p1` shows `applied: true` (R18) |
| AC26 | test mode; `tool_change.json` as `p2`, `missing_section.json` as `p3`, `prompt_change.json` as `p4`, each registered via `api/test/load-proposal` | apply each: `p2` with `approved: true`; `p3` with `approved: true`; `p4` with `approved: false` | `p2` → 400 and no snapshot written; `p3` → 422 and no snapshot written; `p4` → 400 and `applied` stays false (R18) |
| AC27 | test mode, `fixtures/batch_v1` and `fixtures/batch_v2` loaded as `v1`, `v2` via `api/test/load-batch` | `GET api/compare?before=v1&after=v2` | `verdict == "success"`, `criteria == {completeness: [4,5], clarity: [0,5], depth: [0,5]}`, `revisions_needed == [5,0]`, `improved == ["completeness","clarity","depth"]`, `regressed == []` (R19) |
| AC28 | test mode, `fixtures/batch_v1` and `fixtures/batch_v2_regress` loaded as `v1`, `v2r` via `api/test/load-batch` | `GET api/compare?before=v1&after=v2r` | `verdict == "regression"`, `criteria.completeness == [4, 3]` (the first-attempt count fell), `regressed == ["completeness"]`, `improved == ["clarity", "depth"]`, `revisions_needed == [5, 2]` — the fall outranks the two gains; and comparing `v1` with itself → `verdict == "no effect"`, `improved == []`, `regressed == []` (R19) |
| AC29 | the page open on the learning panel | the learner walks: run batch → view grid → propose → approve → re-run → compare | each step's result is visible on the page without a reload loop: the first-attempt grid (documents × criteria, pass/fail), the recurring-gaps table grouped by criterion, the proposal text with its evidence quotes and rejected list, an explicit Approve control, the v1→v2 diff, and the comparison table with the verdict (R15–R19) |
| AC30 | **live L5** — the full learning loop with real models | batch `live1` under the baseline, propose, approve, apply to `live2`, batch `live2`, compare | every artifact of AC20/AC24/AC25/AC27 exists for the live labels; the comparison validates against §3.3 and its verdict is reported with evidence; the first-attempt grid for `live1` shows clarity and depth failing on a majority of documents (the planted gap) — if it does not, the test reports the observed grid rather than asserting success; runs whose real grader's verdict was rejected (`grader_error`, explanation `grader verdict rejected:`) are counted in `grader_errors` and listed in the report — if they are a majority of either batch the test is **inconclusive**, not failed; all three roles ran on the platform models named by the §2 variables (R15–R20) |
| AC31 | ticket `SESS-301`, scripted `REVIEW_BAD_EDIT`, agent-only (budget 0, cap 12) | the loop runs | the run is not stopped by the rejected edit: `stop_reason == "finished"`, `turns == 9`; the record's `stages` has six entries — the second entry has `section == "Ambiguities"` (derived per §3.2: the first occurrence of `"## A"` is the `## Ambiguities` heading), `ok: false` and a non-empty `error` naming the non-unique `old_string`; the other five are `ok: true`; `stage_order` lists the five sections once each in the §3.1 order and `in_order == true`; the trace holds a `read_file` Tool row between the failed and the successful Ambiguities edit; the final file is complete per §3.1 (R3, R24) |
| AC32 | `SESS-301`, scripted `REVIEW_OK`, grader `GRADER_NO_READ`, budget 3 | the verification loop runs | the grader's resemblance verdict is not accepted: `len(grading) == 1`, `grading[0].result == "grader_error"`, `grading[0].criteria == []`, `grading[0].explanation` starts with `grader verdict rejected:`, `status == "grader_error"`; no criterion anywhere in the record is recorded as passed (R9, R24) |
| AC33 | a run started with an explicit workspace directory into which `fixtures/stale_analysis.md` was copied as `analysis.md`; `SESS-301`, scripted `REVIEW_OK`, agent-only | the loop runs | the workspace did not contain `/analysis.md` at the agent's first tool call (the harness removed it); the first write is `write_file: Confirmed Facts`; the final file has `counts["Ambiguities"] == 2` and a Summary that does not contain `stale`; `stages` has five `ok: true` entries and `in_order == true` (R6, R24) |
| AC34 | the seed data, test mode with `REVIEW_SCRIPT=REVIEW_OVERREACH` and the default grader | `POST api/tickets/REQ-104/rerun`, then done | the trace holds Tool rows for `close_ticket` and `save_requirement_version` whose `detail` is an error (no such tool) and a `write_file` row for `/../data/pages.json` whose `detail` is a denial; the run still finishes (`stop_reason == "finished"`) with a complete file; afterwards `page-req-session-timeout` still has exactly one version, the ticket's status is `Analysis Ready` (not `Done`), and the only page that gained a version is `page-analysis-req-104` (R5, R13, R14, R24) |
| AC35 | AC20 complete (`run_history/t1/` written by one server process) | that server process is stopped and a new one is started in test mode against the same `data/` and `run_history/` | `GET api/batches/t1` from the new process returns `state == "done"` and a `summary` equal to `run_history/t1/summary.json`, five runs, and `instructions` equal to `run_history/t1/AGENTS.md`; `GET api/runs/{id}` for a run id from the first process returns its `RunRecord` (R15, R24) |
| AC36 | test mode, default scripts | `POST api/batches` `{label: "one", instructions_source: "baseline", documents: ["01_session_timeout"]}` | HTTP 400 whose message names the minimum of 2 documents; `run_history/one/` does not exist; the same request with `documents: ["01_session_timeout", "02_report_export"]` is accepted and, when done, `summary.runs == 2` (R16, R24) |
| AC-L1 | **live** — `SESS-301` with real models, agent-only | the loop runs | the file is complete per §3.1, `stop_reason == "finished"`, `in_order == true` (R3, R7) |
| AC-L3 | **live** — seed data | `POST api/tickets/REQ-104/rerun` | the ticket reaches `Analysis Ready` and the report page gains a version whose banner names the status; if that status is `grader_error` with the last pass's `explanation` starting `grader verdict rejected:`, the test reports the rejection and is **inconclusive**, not failed (R12, R13) |

Every Ledger row with a non-empty Invariant is exercised: D-A1 by AC5 (agent loop), AC10 (verification wraps it), AC16 (the event-started run was graded: event wraps verification), AC20 (learning reads the records); D-A2 by AC14, AC15, AC17; D-S1 by AC9–AC12 and AC32; D-A3 by AC18 and AC25–AC26.

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the §0 gate, then write `resolved-decisions.md` before any code; keep it, every run record, every
  batch summary, proposal and comparison on disk — in this lab the workspace is the record and chat is
  forgotten `[environment]` (R15).
- Batch the §2 installs into one early command and announce their wall-clock cost before running it
  `[environment]`.
- Start the server in the background and keep it running while you test `[environment]`; bind
  `0.0.0.0:4000` (R21).
- Read keys, base URLs and model ids from the environment (R20); keep every page URL relative (R22).
- Run the offline suite after every change that touches a rule in §4; report per-AC evidence (§7).
- Keep the three model roles separately configurable, and a model grader's tools limited to `read_file`.

**Ask First** (derived from the course's spoken trade-offs)
- Adding or removing a loop (row D-A1) or changing the trigger kind (row D-A2) — changes what the
  system guarantees and retires ACs.
- Replacing the LLM grader with a deterministic or hybrid one, or adding a human gate (rows D-S1, D-A3).
- Changing the rubric's criteria, their order, or the `Resolved by:` / `Edge case:` labels after any
  batch exists — every stored summary and proposal was computed against the old rubric (rework) (R8).
- Changing the send-back budget (3) — at 0 the verification loop silently disappears, a guarantee
  change no offline AC catches once the AC10/AC12 fixtures are adjusted (R8, lever).
- Changing the model for any role, including giving the grader a different model from the agent
  ("a common production choice") or collapsing the analyst onto the cheaper tier (R20 lever).
- Changing the recurrence threshold ("most runs") — moves what counts as a pattern without failing any
  AC (R17).
- Changing the turn caps (12 / 40 / 40) or the simulated failure count (2) — post-build levers (R2, R7).
- Editing the baseline instructions by hand instead of through a proposal — the learning loop's
  evidence would no longer describe the instructions in use (R18).
- Installing anything beyond §2 `[environment]`.

**Never**
- Author `AGENTS.md` at the lab workspace root — the IDE rewrites it at every boot and anything placed
  there is silently lost `[environment]`. (The review agent's own `/memories/AGENTS.md` lives inside
  its run workspace and is a different file.)
- Ask the learner for an API key, hardcode one, print one, or commit one (R20).
- Modify fixtures to make a test pass; or edit `fixtures/instructions_baseline.md` in place (R18).
- Invent evidence: an analyst `evidence` string that is not a verbatim quote from a run is a defect;
  a model-grader pass without a quoted line, or a deterministic check without its matched line, is a
  defect (R9, R17).
- Let the agent write to a requirement page, to `/memories/**`, or mark a ticket `Done` (R5, R13, R14).
- Apply a harness change without the approval action, or apply a non-prompt target automatically (R18).
- Open a WebSocket or use root-absolute URLs in the page `[environment]` (R22, R23).
- Report "should pass" / "looks correct" — unrun is failed (§7).

## 7. Test Plan & Self-Verification

```bash
python3 -m venv .venv --system-site-packages && . .venv/bin/activate
pip install deepagents==0.7.11 langchain==1.3.18 langchain-core==1.6.1 langgraph==1.2.11 \
  langchain-openai==1.6.0 openai==3.6.0 pydantic==2.13.5 python-dotenv==1.2.3 pytest httpx
# announce the cost of the line above before running it [environment]

# offline suite — must pass with no network and no key; completion gate
env -u OPENAI_API_KEY -u ANTHROPIC_API_KEY python -m pytest tests/ -m "not live" -q

# server, in the background [environment]
nohup uvicorn app:app --host 0.0.0.0 --port 4000 > server.log 2>&1 &
curl -s localhost:4000/api/health
curl -s localhost:4000/ | grep -nE '(href|src)=["'"'"']/' && echo "ROOT-ABSOLUTE URL FOUND" || echo "urls ok"

# live suite — only with the container's ambient credentials
python -m pytest tests/ -m live -q
```

Adjust the module path and the key variable names to what the environment actually exports (R20); do
not invent them. Test mode (scripted stand-in injected) is selected by `REVIEW_TEST_MODE=1`, which the
server reads at startup and which waives the key check (R20, R24). The ACs that hit the server in test
mode, without a model, are exactly: AC1 (its `REVIEW_TEST_MODE=1` branch), AC2, AC3, AC9, AC13, AC14,
AC15, AC16, AC17, AC18, AC19, AC20, AC21, AC22, AC23, AC25, AC26, AC27, AC28, AC29, AC34, AC35, AC36;
AC24 and AC30 hit it with real models (`live`);
the suite sets `REVIEW_TEST_MODE=1` for every server it starts except AC1's key-unset exit check,
which starts one without it.

**Report format (required).** For every AC in §5, one line: `AC<n> — PASS|FAIL|SKIPPED(live) —
<evidence>`, where evidence is the pytest node id and the assertion's observed values, or the file
path and the lines that show the artifact (`run_history/v2/AGENTS.md:38-41`, `data/tickets.json`
entry). A line without evidence, or reading "should pass" / "looks correct", is a failure — it means
the test was not run. Finish with the resolved-decisions checklist path and the server's listening
line from `server.log`.

Conclude the build with an infra/structure diagram of the app (processes, files, the four loops and
what each reads and writes) and the phrase **"This is the infra/structure diagram of this app"**.

## Runtime (lab) `[environment]`

Facts contributed by the `coding-agent-lab` environment, not by the course. Container: Debian,
non-root user, Node 22, Python 3 with venv, sqlite3, git, build tooling. Preinstalled Python:
`fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`; Node: `express`, `cors`,
`better-sqlite3`, `vite`, `nodemon`. Nothing else — no agent frameworks. Outbound network works, so
the §2 installs succeed but cost session time. Memory is finite and shared with the coding agent's own
process (this app holds no local models, so the release-before-load rule does not apply). The preview
pane shows one server on port 4000 bound to `0.0.0.0`, reverse-proxied under a path prefix (hence
R22), HTTP only (hence R23; streaming responses work). The container exports provider API keys and
base URLs; the coding agent's own model is chosen per conversation by the learner and this spec
assumes nothing about it. Every tool call is visible to the learner; long-running servers run in the
background. The workspace is the record; `AGENTS.md` at its root is rewritten at every boot.

**Environment pitfall — root-absolute URL under a proxied preview** `[environment]` (moved here from
the course's failure catalog, where it was B15; it is the lab's failure mode, not the course's).
Symptom: a working app renders with dead links or failed fetches. Cause: `/api/...` resolves against
the IDE, not the app. Fix: relative URLs only. Enforced by R22, AC2.

## Course Context Pack (embedded — agent-readable)

### CTX-A. The pattern

Loop engineering: build the agent, then build loops around it, each wrapping the last.

1. **Trigger** — an event (a ticket created, a requirement edited) or a person starts a run; the agent
   is "looped into" the system where the work happens, so it gets used (Lesson 2; event app).
2. **Fetch** — the agent is told a ticket id, never the text, and fetches it with a tool; tool calls can
   fail transiently and are retried with the same arguments (Lesson 4).
3. **Agent loop** — the model calls tools, observes results and repeats until it says it is done:
   write the skeleton, then edit one section per turn into a single file; a turn cap stops a loop that
   never finishes (Lessons 3–4). Instructions live in a file loaded every run; the harness, not the
   prompt, keeps the agent from editing them.
4. **Verification loop** — "finished" is not "good enough": a grader reads the produced file against a
   rubric, passes or fails each criterion with a gap, sends the gaps back, and the agent revises; the
   loop ends when every criterion passes in one pass or the send-back budget runs out (Lesson 5).
5. **Record** — every run is a trace plus every grading pass with the file as it stood; batches of
   runs under one instructions file summarize to first-attempt pass rate per criterion (Lesson 6).
6. **Learning (hill-climbing) loop** — an analyst agent reads the batch (read-only), finds what the
   agent is corrected on in *most* runs, proposes one literal change to the instructions with quoted
   evidence; a human approves; code applies it; the batch re-runs; before/after is compared with
   regressions called out (Lesson 6).
7. **Human oversight** — a human marks work done and approves harness changes; more gates can be added
   at sensitive tool calls or at the grader (Lesson 2).

Loops compose: the course nests all four, and says you need not (row D-A1).

### CTX-B. Failure-mode catalog

- **B1 Transient tool failure.** Symptom: the fetch returns "503" or "timed out". Cause: an external
  system is busy. Fix: the agent calls the same tool with the same arguments again until it succeeds;
  the fixture plants two failures. Enforced by R2, AC5.
- **B2 Finished but not good enough.** Symptom: the agent declares the review done, but each ambiguity
  says only why the clause is unclear — not what fact would resolve it or what goes wrong if it stays
  unresolved. Cause: nothing in the agent loop checks quality. Fix: a grader with a rubric sends the
  specific gaps back; the second attempt passes. Enforced by R8, R11, AC10–AC11.
- **B3 Grader judges by resemblance.** Symptom: criteria the file does not satisfy are marked passed.
  Cause: the grader reads the conversation, which "looks like" a satisfying run. Fix: give the grader
  `read_file`, require a verbatim quote with a line number per passed criterion, literal label
  matching, item-by-item coverage, conservative verdicts — and the harness refuses a verdict that
  skipped the file or carries no evidence. Planted by the `GRADER_NO_READ` script. Enforced by R9,
  AC9–AC10, AC32.
- **B4 Stale analysis file.** Symptom: the agent skips stages. Cause: a finished `/analysis.md` from an
  earlier run is still in the workspace and the agent reads it. Fix: fresh workspace per run; delete
  the file before a run. Planted by `fixtures/stale_analysis.md`. Enforced by R6, AC6, AC33.
- **B5 Missing instructions, silently.** Symptom: a plausible but bad review. Cause: the memory loader
  ignores a missing file without warning, so the agent runs on the system prompt alone. Fix: fail
  loudly when the instructions file is absent. Planted by `fixtures/workspace_no_instructions/`.
  Enforced by R5, AC4.
- **B6 Agent edits its own instructions.** Symptom: instructions drift during a run. Cause: the
  instructions sit in the same writable filesystem as the output and the agent has `edit_file`. Fix:
  deny writes under `/memories/**` at the permission layer, not in the prompt. Enforced by R5, AC4.
- **B7 Runaway loop.** Symptom: the model keeps retrying past the point where retrying makes sense.
  Cause: the normal stop (the model finishing) never arrives. Fix: a model-call cap that ends the run,
  reported as a turn-limit stop, never as a finished review. Enforced by R7, AC7.
- **B8 The same correction every run.** Symptom: clarity and depth fail first-attempt on most documents,
  with near-identical grader gaps. Cause: a systematic gap in the instructions (nothing asks for
  `Resolved by:` / `Edge case:`). Fix: analyze the batch, propose one literal insertion, approve,
  apply, re-run. Enforced by R4 (planted), R17–R19, AC20–AC28.
- **B9 One-off noise mistaken for a pattern.** Symptom: a proposal built on one run's quirk. Cause: no
  recurrence threshold. Fix: only a criterion failing in most graded runs is a property of the agent;
  everything else is listed under `rejected`. Planted by `batch_v1`'s single completeness miss (run 3).
  Enforced by R17, AC9 (the scripted analyst rejects it), AC24.
- **B10 Criterion names drift.** Symptom: one recurring failure appears as several. Cause: grouping by
  the grader's paraphrased criterion name. Fix: identify criteria by rubric position. Enforced by R16,
  AC21.
- **B11 Grader error counted as a pass.** Symptom: pass rates look better than they are. Cause: a run
  with no verdict averaged into the denominator. Fix: exclude `grader_error` runs and report them.
  Enforced by R16, AC22.
- **B12 Out-of-tries reads as a verdict.** Symptom: a run that exhausted its budget looks like any
  rejected pass. Cause: the last grading pass still says `needs_revision`. Fix: a run-level status
  `max_iterations_reached` distinct from `satisfied`. Enforced by R10, AC12.
- **B13 The agent closes or overwrites.** Symptom: the requirement page changes, or a ticket is Done
  with nobody having looked. Cause: the agent is allowed to write where it should only read, or to
  decide completion. Fix: separate agent-authored versioned report page; only humans add requirement
  versions or mark Done; the review agent has no tool that reaches a page or a ticket's status, and its
  file tools cannot leave the run workspace. Planted by the `REVIEW_OVERREACH` script. Enforced by
  R5, R13–R14, AC16–AC18, AC34.
- **B14 Harness change applied blind.** Symptom: an unreviewed prompt edit, or a tool/config proposal
  silently reshaped into a prompt edit. Cause: the analyst applies, or the applier accepts any target.
  Fix: propose/apply split, explicit approval, prompt-only automatic application, other targets shown
  for reading. Enforced by R18, AC25–AC26.
- **B15** — moved to the Runtime (lab) section; not a course failure mode. (Number kept so no
  reference dangles.)
- **B16 Failed edit counted as a stage.** Symptom: stage order looks complete when a section was never
  written. Cause: `edit_file` rejects a non-unique `old_string`; the call still names the section.
  Fix: count only successful writes toward stage order; the model recovers by reading and retrying.
  Planted by the `REVIEW_BAD_EDIT` script. Enforced by R3, AC8, AC31.

### CTX-C. Decision background

**How to read the provenance notes.** Four phrases recur in this spec's Ledger cells, rules and the
entries below; they mean exactly this. A **litmus branch** records how a course-argued alternative was
classified: **row** — the course showed the alternative working as an acceptable choice, so it is a
Ledger option; **bake-in** — the course showed it only as a failure or warned against it, so the taught
side is a business rule and the alternative appears only as the cited anti-pattern; **lever** — the
sides differ only in a value (a number, a model id), so the subject is a body default with the
argument attached, not a row. A **lever** is such a value; when the materials set it inconsistently its
value is chosen by the **lever rule** in order of **branch (1)** the value the narration states aloud in
the lesson that introduces it, **branch (2)** the end-to-end application's own configuration, **branch
(3)** the value used most often across the materials, earliest-taught on ties — a **post-build lever**
may be changed after the build (Ask First, §6) and is never asked about at the gate. The **stakes test**
asks whether picking the other side of a contradiction *up front* would change the system's structure,
semantics or a guarantee (a box, arrow, owner or guarantee in the architecture diagram), or force
rework; a contradiction that fails it becomes a lever, one that passes it becomes a Ledger row.
**Realization tiers** rank a dependency's weight — **tier 1** the language's standard distribution,
**tier 2** a library installed by the package manager, **tier 3** an external service or provisioned
resource (a key, an admin install, a large download); where the course's own choice needs setup the
learner may lack, the lightest tier that satisfies the invariant is the default and the course's choice
stays in Options marked "(course default)". The **heavy bar** is the test a course dependency must meet
to earn a *realization* Ledger row: it is tier 3, or it needs setup the learner may not have (a paid
key, an admin-provisioned service, a large download) — a dependency below the bar is simply pinned in
§2. The **Never tier** is the "Never" list of §6 Standing Permissions (as "Always" and "Ask First" are
its other two tiers).

- **Loop composition → Ledger D-A1.** Lesson 2's four-level taxonomy (agent / verification /
  event-driven / hill-climbing) is the course's teaching frame; the *decision* it argues is that the
  nesting is optional and composable. Lesson 4 shows the agent loop alone completing a review; Lesson 5
  wraps it; the shipped event app wraps that; Lesson 6 reads the records. Litmus branch recorded in the
  row: row (subsets endorsed, not warned against).
- **Trigger kind → Ledger D-A2.** Lesson 2: scheduled (a morning calendar summary) versus event-driven
  (an email arrives; a Slack message in a channel). The course's shipped code is event-driven: ticket
  created, or a linked requirement edited while a ticket is open; the ticket page also has a manual
  re-run. The transcripts have no event-driven lesson of their own — Lesson 5 announces one as next
  and Lesson 6 is the learning loop; the Tall deck has a title card and a diagram for it (deck-only);
  the Flask app is the only shipped code for it. Litmus branch: row.
- **Grader realization → Ledger D-S1.** The docs-writer example (Lesson 2, slides 2.6–2.7) grades
  mechanically — links resolve, CI passes; the course's own review grader is a model with `read_file`.
  Slide 2.6's "deterministic or agentic" line is video-shown (narrated slide) and so ranks with the
  transcript. The hybrid is this spec's naming of the obvious split (labels are mechanical, coverage is
  not). Litmus branch: row (the deterministic grader is shown working).
- **Human oversight → Ledger D-A3.** Lesson 2 / slide 2.12 list four insertion points. The course's
  shipped system uses two (human marks Done; human approves the proposal) and names the other two as
  options. Litmus: bake-in for the two, row for the rest.
- **Model tiering → R20 lever.** Lesson 2: match model to task complexity to optimize cost;
  verification "can make cheaper models viable for harder tasks"; Lesson 5: same model for agent and
  grader here, "a different model for grader is a common production choice"; Lesson 6 and the README:
  the analyst runs on the more capable model because reading five traces and finding what recurs is
  what the cheaper one does unreliably. Sides differ only in a model id → lever, not a row (an argued
  trade-off whose sides differ only in a value never becomes a Ledger row). The course's ids — `openai:gpt-5.4-mini`, `openai:gpt-5.5` — are provenance, not a
  recommendation; the lab fixes the provider set (Environment Resolutions).
- **Send-back budget 3 vs 2 → R8 lever.** Lesson 5 narration and notebook: 3; batch runner: 3; event
  app: 2. Stakes test: a number — picking 2 up front changes no box or guarantee. Lever rule branch (1)
  (narration) → 3. Post-build lever.
- **Simulated fetch failures 2 vs 0 → R2 lever.** Lesson 4 narration: "simulating two times of
  failure"; notebook table: "simulates two transient failures"; shipped pre-recorded trace: two error
  results; helper constant: 0 ("set it higher to turn the retry demonstration on"); batch runner: 0
  ("only adds turns and noise"). Lever rule branch (1) → 2, as a fixture property of one ticket so the
  batch is clean. Post-build lever.
- **Turn caps → R7 body defaults.** 12 (agent-only, Lesson 4 + helper), 40 (with a grader: Lesson 5
  notebook, event app "several verification passes cost more turns than one review", batch runner),
  40 (analyst), 30 (the poet primer). Different depths, not a contradiction. The course's own live run
  took 9 turns / 17 steps with two fetch failures — the AC5 numbers reproduce that shape on this
  spec's fixture.
- **Fetch tool name.** The root instructions and the helper define `fetch_requirement`; the two
  batch-snapshot instruction files and slide 3.5 say `fetch_requirement_from_jira`. Lever rule branch
  (1): the Lesson 4 narration says `fetch_requirement`. Used here.
- **Instructions file name.** Code and Lesson 4: `AGENTS.md`; slide 3.4 and parts of Lesson 3: "Agent.md".
  Branch (2), the application config → `AGENTS.md`. Path `/memories/AGENTS.md` inside the agent's
  virtual root (the lab's root-level `AGENTS.md` ban concerns a different file — Never tier).
- **Lesson 6 narration vs committed batch.** The narration reports completeness failing on one document
  and clarity/depth passing on the last; the committed batch has completeness 5/5 and clarity/depth
  0/5; the notebook's saved output is a third run. Different live runs of a nondeterministic agent —
  recorded as provenance, not a parameter; the fixture batch (4/5, 0/5, 0/5) deliberately includes a
  one-off completeness miss so the recurrence rule has something to reject.
- **Run count four vs five.** Lesson 6 narration first says four documents, then five; the notebook
  runs five; slide 6.2 draws two placeholders. Fixture: five.
- **Requirement wording.** Slides quote the course's example requirement slightly differently from the
  Lesson 4 narration; immaterial here — this spec authors its own documents.
- **Flat JSON records → §2.** The event app's data store is three JSON lists, chosen so a learner can
  open the files and see exactly what the app sees; the batch runner writes one JSON per run. No
  database was argued. Tier 1 (stdlib).
- **Checkpointer.** The course attaches an in-memory checkpointer when a grader is present and says it
  is "not required for the rubric loop … measured"; it exists only so the shape matches the library
  docs. Not an invariant.
- **Event app port and framework.** Course: Flask on 5050, two visually distinct UIs; this build: the
  lab's one server on 4000 (`[environment]` — the lab's preview pane shows exactly one server, so the
  page and its API share a process; §1 Deliverable shape). The "two tools" look is kept as a styling
  note, not a rule.
- **Cost estimate.** `compare` in the course adds token and USD estimates from a hard-coded price table
  for its two models; perishable, Not Included #8.
- **Slides.** Weighting applied: a slide shown in the video ranks with the transcript; a deck-only slide
  loses any conflict to code and narration, and the conflict is recorded in this section. Read: Wide
  deck 1–13 (all Lesson 2, narrated except the title card);
  Tall deck 1–5 (Lesson 3), 6–10 (Lesson 4), 11–14 (Lesson 5), 17–18 (Lesson 6), 15–16 deck-only
  (event-driven, no transcript lesson). No slide-only fact contradicts code or narration in a way that
  reached a rule; the deck-only event-driven diagram agrees with Lesson 2's narrated one.

### CTX-D. Perishable assumptions

Concepts in CTX-A…CTX-C are durable. Treat the names below as search keywords against current
documentation, not guaranteed imports.

- Harness: `deepagents` 0.7.11 — `create_deep_agent(model, tools, system_prompt, memory=[...],
  skills=[...], backend, permissions, middleware, checkpointer, response_format)`;
  `deepagents.backends.FilesystemBackend(root_dir, virtual_mode=True)`; `FilesystemMiddleware(backend,
  tools=[...])` (its `.tools` is how the grader gets `read_file`); `FilesystemPermission(operations,
  paths, mode)` — first match wins, unmatched allowed; `RubricMiddleware(model, max_iterations, tools,
  system_prompt, on_evaluation)` — flagged beta; passing `system_prompt` *replaces* the library's
  default grader prompt (the course restated the 0.7.11 default then appended its additions); the
  rubric text is supplied per invocation under a `rubric` state key; the terminal status lives in a
  private `_rubric_status` state value; structured output returned under `structured_response`.
- LangChain 1.3.x: `langchain.agents.middleware.ModelCallLimitMiddleware(run_limit, exit_behavior="end")`;
  `langchain.tools.tool`; `langgraph.checkpoint.memory.InMemorySaver`; message `content` may be a list
  of blocks or a plain string; a fake/scripted chat model for tests exists in `langchain_core`'s
  language-model test utilities (search "fake chat model" / "GenericFakeChatModel").
- Provider: model ids as `openai:<name>` via `langchain-openai`; the course's models `gpt-5.4-mini`
  and `gpt-5.5`; the course set no sampling parameters (no `temperature`) on any role — do not add
  any, since parameter support varies by model family and an unsupported one surfaces as a live API
  error. Request-parameter compatibility for the platform's models is unknown to this spec: use
  defaults.
- Course era extras not used here: Flask 3.1 on port 5050; LangSmith env vars `LANGSMITH_TRACING`,
  `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` (three different project names appear across the
  materials); `tiktoken` `o200k_base`; the course's price table.
- Python ≥ 3.12 was the course's floor for numpy/pandas; `uv.lock` revision 3 holds the pins in §2.

### CTX-E. Provenance map

Lesson numbering follows the transcripts (the repo folders are one lower for each notebook; the
README uses a third numbering). Nothing in this spec requires platform access.

| Lesson (transcript) | Title | Contributed |
|---|---|---|
| 1 | Introduction | CTX-A overview; the promise of an event-driven run "when a new requirement is received" |
| 2 | Overview of Loop Engineering | CTX-A stages 1, 4, 6, 7; D-A1, D-A2, D-S1, D-A3 arguments; R20 tiering; the eval/regression rule behind R19; slides 2.1–2.13 (Wide deck; all narrated except the title card) |
| 3 | Deep Agent Primer | CTX-A stage 3 (filesystem, instructions as files, progressive disclosure → Not Included #3); turn cap 30 for the primer; slides 3.1–3.5 (Tall deck; 3.1 deck-only) |
| 4 | Agent Loop | R1–R7, CTX-B1, B4–B7, B16; turn cap 12; two simulated failures; slides 4.1–4.5 (4.1 deck-only) |
| 5 | Verification Loop | R8–R11, CTX-B2, B3, B12; budget 3; turn cap 40; same model for agent and grader; slides 5.1–5.4 (5.1 deck-only) |
| (no lesson) | Event-driven app (shipped code; Tall deck 15–16 deck-only) | R12–R14, CTX-B13; budget 2 (contradiction, CTX-C); port 5050 |
| 6 | Learning loop | R15–R19, CTX-B8–B11, B14; analyst on the capable model; slides 6.1–6.2 (6.1 deck-only) |
| 7 | Conclusion | nothing beyond the recap |
| — | Shipped helper modules, batch runner, lock file | parameter values, status semantics, §2 pins, HarnessChange schema |
| — | **Environment (`coding-agent-lab` overlay, not the course)** | §1 deliverable shape; §2 container, preinstalled set, venv flag; R20–R23; the `choices` question mechanism in §0; the Runtime (lab) section and its environment pitfall (formerly CTX-B15); Never-tier `AGENTS.md` rule |

---

*Status:* version 1 (lab) · course: Loop Engineering with LangChain DeepAgents · learner project:
[the lab's assignment — this §1 Objective] · This is a living document: when the building agent
produces something unexpected, add the missing constraint here and re-run.
