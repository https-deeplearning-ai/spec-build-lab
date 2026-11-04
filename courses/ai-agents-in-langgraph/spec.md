# Spec — Plan, research, draft and critique writer with saved, rewindable steps

**What you're building:** a program that writes a short piece on a topic you give (by default a five-paragraph essay; the course's example topic is a pizza shop) by passing it through separate model roles, a planner, a researcher, a writer and a critic, in a fixed loop: plan, research, draft, then critique, research again and redraft until a revision limit. You type a topic into a browser page and watch each step's result appear. You can stop after any step, read or edit the plan, draft or critique, rewind to an earlier step, and keep several pieces on separate threads.

**What the recommended build needs to run:** an OpenAI API key (`OPENAI_API_KEY`) for the four model roles, network access to reach the model, and a one-time install of Python packages. No search key or account: research reads a local folder of documents.

**Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once `OPENAI_API_KEY` is set and are skipped until then; that is not a failure.

This file is self-contained: everything the build needs is in it.

*Provenance: course "AI Agents in LangGraph"; materials used: lesson transcripts (Lessons 1–9), the course notebooks and the final app's helper module (rendered as text), slide descriptions; pattern card confirmed by the owner 2026-11-03; written 2026-11-03 with guide v2.9 (2026-10-31).*

---

## 0. Before you build — REQUIRED (do this first)

You are the build agent. Before writing ANY code, you MUST ask the person you are building for
the questions in the next section. Do not skip this because the recommended answers look
complete: they exist so the build is reproducible, not because they fit this person's project.

1. **Use a structured question tool if you have one** (e.g. Claude Code's `AskUserQuestion`);
   otherwise list the question in your reply and ask.
2. **First question — recommended build, or choose?** Two options: the **recommended build**
   (every question takes its "(Recommended)" option — mostly the course's own choices, with a
   lighter stand-in wherever the course's choice needs setup the person may not have; the
   checklist in step 5 marks each place it differs from the course; to run for real it needs
   an OpenAI API key (`OPENAI_API_KEY`)), or **choose** question by
   question. Recommended → go to step 5. Choose → step 3.
3. **Ask ONE question at a time.** Show the question, its options with their "pick this when …"
   and setup cost, and the labels "(course default)" / "(Recommended)" /
   "(Recommended - course default)" exactly as written — no other labels. Say once, before the
   first question, that "(Recommended)" was fixed when this spec was written and does not
   reflect this person's setup. Use earlier answers to explain later options in the person's
   own terms, but never drop or change an option because of them. Skip a question only when its
   own "Ask only when …" condition is false, and say so in one line. A per-call limit of your
   question tool is never a reason to skip, merge or default a question.
4. **Asking ends your turn.** Write no code and touch no file until the person answers. Keep
   asking until every question is answered or skipped by its condition. Answers to some
   questions do not release the build; no reply is not an answer.
5. **Before the first line of code, print a checklist and write it to `resolved-decisions.md`:**
   every question with the chosen option's id and text, each marked `= course choice`,
   `≠ course choice (course used: <option>)`, `no course choice`, or `not asked (<condition>)`.
   Add one line per model role naming the current model you will use from the chosen provider;
   if you cannot tell, ask, and otherwise use the course's own model id and say it may need
   changing. For every chosen option that is not recommended, copy its "what to check" sentence
   into the checklist. On the recommended path, walk the person through every `≠` line and its
   reason. Start building only after the checklist is shown, written and confirmed. Leave out
   every part of the spec that exists only for an option not chosen.

---

## 1. Questions
C1–C2 are context (what you write, which model provider); C3–C9 follow the program's stages in order: research (C3–C5), drafting (C6), saving steps (C7), controlling and watching a run (C8–C9).

### C1. What kind of piece should the program write?
- **C1a (Recommended - course default): A short essay.** Every run produces a five-paragraph essay on the topic you type, planned as an outline with notes per section and graded by a critic acting as a teacher. *Pick this when* an essay is what you need, or you have no other form in mind. *Setup:* none.
- **C1b: Another kind of piece you name.** The planner, writer and critic instructions are reworded for your form (for example a study summary of your notes, a product brief, a blog post); the flow is unchanged. *Pick this when* your project needs a written piece other than an essay; the wording of each role's instructions for your form is yours to get right, and a weak wording gives weak plans and critiques. *Setup:* none; you name the form and its length.
  - *What to check:* the planner, writer and critic instructions name your kind of piece instead of an essay, and a run on a sample topic ends with a draft in that form.

### C2. Which model provider runs the four roles?
- **C2a (Recommended - course default): OpenAI.** The planner, researcher, writer and critic all call an OpenAI chat model. *Pick this when* you have, or can get, an OpenAI key. *Setup:* an OpenAI API key in `OPENAI_API_KEY`.
- **C2b: Another hosted provider.** The same four roles call a different hosted chat model; only the model connection changes. *Pick this when* you already pay for another provider or your organisation requires one; the researcher needs a model that can return a structured list of search queries, which the course relies on function calling for. *Setup:* that provider's API key and its integration package.
  - *What to check:* all four roles run on the chosen provider and the researcher still returns a list of search query strings.
- **C2c: A model served on your own machine.** The four roles call a locally served open model; no key, and no text leaves your machine. *Pick this when* your topics or documents must stay private or you cannot get a key; smaller local models follow the "list of queries" format less reliably and write weaker drafts. *Setup:* a local model server and a model download of several GB.
  - *What to check:* with the local model server running and no key set, a full run on the sample topic ends after two drafts with research added to the record.

### C3. Where does research come from?
- **C3a (Recommended): A local folder of documents (stand-in for web search).** Each search query is matched against the text files in a `library/` folder by shared words, and the best two passages are added to the research; it is a stand-in for a web search service built for agents (C3b), which needs its own key. *Pick this when* you want to run without a search account, or your topics are covered by documents you have (your own notes, reports); it cannot find anything newer than the files you put in. *Setup:* none; the build ships sample documents and you can add your own `.txt` or `.md` files.
- **C3b (course default): A web search service built for agents (Tavily).** Each query goes to a web search service built for agents, which returns up to two results as ready-to-use text rather than links. *Pick this when* your topics need current information from the web; the course's reason for searching at all is that a model's fixed knowledge cannot answer about recent events. *Setup:* a Tavily account and API key in `TAVILY_API_KEY`; searches use your account's quota.
  - *What to check:* with `TAVILY_API_KEY` set, each query adds up to two web result texts to the research, and without the key the program says the key is missing instead of running a step.
- **C3c: An ordinary keyless web search.** Each query goes to a general web search (DuckDuckGo) that returns links; the program fetches the top pages and keeps their heading and paragraph text. *Pick this when* you want live web results but cannot get a search key; the course showed this returns links rather than answers, and page text that is long and not concise, and its notebook notes the search can refuse requests under heavy use. *Setup:* network access and the search and HTML-parsing packages; no key.
  - *What to check:* each query adds up to two pieces of page text (headings and paragraphs, whitespace collapsed) to the research, and a refused search is reported to the person and adds nothing.

### C4. How does the research step choose its searches?
- **C4a (Recommended - course default): A short list of queries written in one go.** The researcher writes a list of search queries (at most three after the plan, at most two after a critique), every query is run, and all results are added. *Pick this when* your topics can be researched from queries planned up front. *Setup:* none.
- **C4b: A research agent that decides its own searches.** The research step becomes a model that calls search one or more times, reads each result, and decides whether to search again, until it stops or reaches a turn limit. *Pick this when* your topics need follow-up searches that depend on what earlier searches found; each extra turn is another model call and another search. *Setup:* none beyond the chosen research source.
  - *What to check:* the research step's model chooses its own searches, stops when it replies without asking for a search or after 5 turns, and every search result it receives is added to the research gathered so far.

### C5. Should a person approve the searches before they run?
- **C5a (Recommended - course default): No, searches run as soon as they are written.** Writing the queries and running them happen in one step. *Pick this when* searches are free or cheap and you trust the generated queries. *Setup:* none.
- **C5b: Yes, stop between writing the queries and running them.** The run pauses with the proposed queries shown; the person can keep, edit or drop each one, and only the approved queries are searched. *Pick this when* your searches cost money or quota, or your topics need the queries vetted before anything is sent out; every research step then waits for a person. *Setup:* none.
  - *What to check:* the run stops after the queries are written and before any search runs, and only the queries the person kept or edited are searched and added.

### C6. What does the writer see when it redrafts?
- **C6a (Recommended - course default): The topic, the plan and all research.** Every draft, first or later, is written from the topic, the plan and all research gathered so far; the critique reaches the writer only through the new research it led to. *Pick this when* you want redrafts driven by the research the critique led to, with shorter model inputs. *Setup:* none.
- **C6b: Also the latest critique and the previous draft.** Redrafts additionally receive the critic's latest critique and the draft it criticised, so the writer can answer each point directly. *Pick this when* you want each redraft to fix what the critic asked for, not only to use new research; inputs get longer, so each redraft costs more. *Setup:* none.
  - *What to check:* each redraft's model input contains the latest critique and the previous draft, and the first draft's input contains neither.

### C7. Where are the saved steps kept?
- **C7a (Recommended - course default): In memory while the program runs.** Every step is saved and can be viewed, edited and rewound, but everything is gone when the program stops. *Pick this when* you write a piece in one sitting; the course notes this store disappears on restart. *Setup:* none.
- **C7b: In a database file on disk.** The same saved steps go into a local database file, so threads survive a restart. *Pick this when* you want to come back to a piece another day. *Setup:* none; a file is created on first run.
  - *What to check:* after stopping and restarting the program, a thread started before the restart is listed, its record can be viewed, and it continues from its last saved step.
- **C7c: In a database server.** Saved steps go to a database server (for example Postgres or Redis), shared by several copies of the program. *Pick this when* several people or processes use the writer at once. *Setup:* a running database server and its connection string.
  - *What to check:* a thread started by one running copy of the program can be listed, viewed and continued by a second copy connected to the same server.

### C8. How does a person drive the program?
- **C8a (Recommended - course default): A browser page.** A local web page with a topic box, Generate and Continue buttons, step checkboxes for where to stop, thread and step pickers, and tabs to read and edit the plan, draft and critique and to read the research and saved steps. *Pick this when* you want to see and edit each part comfortably. *Setup:* none; it opens on your machine.
- **C8b: Terminal commands.** The same actions as commands in a terminal, with records printed as text. *Pick this when* you run it over a remote shell or from scripts, or do not want a web page. *Setup:* none.
  - *What to check:* every action of the browser page (start, continue, choose stop steps, view the record, view history, edit plan, draft or critique, rewind, switch thread) is available as a command and gives the same results in the offline tests.

### C9. How is progress shown while a run works?
- **C9a (Recommended - course default): Each step's result as the step finishes.** After every step, its output is added to a live output area. *Pick this when* step-by-step updates are enough. *Setup:* none.
- **C9b: Also the model's words as they are written.** Drafts, plans and critiques appear word by word while the model writes them, as well as each finished step. *Pick this when* drafts are long and you want to watch them form rather than wait; it needs the program to run the model calls in streaming mode. *Setup:* none.
  - *What to check:* while a draft is being written its words appear as they are produced, and the saved record afterwards holds the same complete draft.

## 2. Departures from the course

Each item names where the recommended build differs from the course and why.

1. **Research from a local folder instead of the course's web search service (stand-in).** The course searched the web with Tavily, which needs a key and account separate from the model's. The recommended build searches a local `library/` folder instead (section 6, R17); Tavily is option C3b.
2. **The researcher sees the plan, not only the topic, when writing the first queries.** The instructor says queries are generated "given a plan"; the course's code passes only the topic. The build follows the instructor (guide rule: an instructor's explicit statement beats code that looks like a slip). See notes, "Where values came from".
3. **The revision count starts at 1, so a limit of 2 gives two drafts.** The instructor starts it at 1 ("it is starting on the first revision") and says the run makes two drafts; the course's browser app starts it at 0, which gives three drafts.
4. **Five-paragraph essays, at most three queries after the plan and at most two after a critique.** The course disagrees with itself: its lesson notebook and slide ask for five paragraphs and three queries in both research steps; its browser app asks for three paragraphs and two queries after a critique. Picks and reasons are in the notes.
5. **Empty starting fields.** The course's browser app seeds plan, draft, critique and research with placeholder words ("no content" etc.), and the placeholder research line reaches the writer. The instructor describes this state as "we don't have any"; the build starts the fields empty and shows placeholders only on screen.
6. **Current library releases and a current model.** The course pinned course-era releases and used `gpt-3.5-turbo`; the build uses current releases and a current model chosen at the checklist (section 0, step 5).
7. **Addition: offline tests with scripted stand-ins.** The course ran no tests. The build adds offline tests driven by a scripted stand-in model and the local search (section 7).
8. **Addition: a missing model key is reported.** Starting a run without the model key says so and runs no step (R18); the course assumed the key was present.

## 3. Objective

Build a program that, for a topic the person gives, plans once, researches, drafts, and then critiques, researches again and redrafts until a revision limit, saving every step per thread so the person can stop, inspect, edit and rewind the run.

## 4. Tech stack and secrets

- **Language:** Python, current release.
- **Flow and saved steps:** LangGraph, current release (the course built the flow as a LangGraph state graph with a checkpointer). Its checkpointer gives "saved after every step", per-thread history, editing a saved record "as if written by" a step, and resuming from an earlier record. Where the course leaves a behaviour to the framework (stopping after a step, how the next step is computed after an edit, snapshot ids), keep the current release's behaviour and note in the checklist how the release provides it.
- **Model access:** the current LangChain integration for the chosen provider (course: `langchain-openai`).
- **Saved-step store (C7a):** an in-memory store (the course used SQLite's in-memory database through LangGraph's SQLite checkpointer).
- **Browser page (C8a):** Gradio, current release (the course's page was built with Gradio).
- **Tests:** pytest; tests needing a real model carry the marker `live`.
- **Secrets:** read `OPENAI_API_KEY` (and `TAVILY_API_KEY` only for C3b) from the environment; a git-ignored `.env` file may set them. Never write a key to a file the build creates or to logs.

## 5. Contracts

### 5.1 The run record (one per saved step)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "RunRecord",
  "type": "object",
  "required": ["task", "plan", "draft", "critique", "content", "queries",
               "revision_number", "max_revisions", "last_step", "count"],
  "additionalProperties": false,
  "properties": {
    "task":            {"type": "string", "minLength": 1, "description": "The topic the person typed. Never changed by a step."},
    "plan":            {"type": "string", "description": "Planner output; \"\" until the planner runs."},
    "draft":           {"type": "string", "description": "Latest draft; \"\" until the first draft."},
    "critique":        {"type": "string", "description": "Latest critique; \"\" until the first critique."},
    "content":         {"type": "array", "items": {"type": "string"}, "description": "All research texts gathered so far, oldest first. Only ever extended by research steps; duplicates kept."},
    "queries":         {"type": "array", "items": {"type": "string"}, "description": "Queries written by the research step after the plan (see R9)."},
    "revision_number": {"type": "integer", "minimum": 0, "description": "Starts at 1; each draft adds 1."},
    "max_revisions":   {"type": "integer", "minimum": 1, "description": "The run ends after a draft when revision_number > max_revisions."},
    "last_step":       {"type": "string", "enum": ["", "planner", "research_plan", "generate", "reflect", "research_critique"]},
    "count":           {"type": "integer", "minimum": 0, "description": "Step counter. Every write ADDS to it (see R10)."}
  }
}
```

### 5.2 Steps and flow

Step names are binding: `planner`, `research_plan`, `generate`, `reflect`, `research_critique`. Entry: `planner`. Fixed edges: `planner → research_plan → generate`; `reflect → research_critique → generate`. After `generate` the decision returns `end` or `reflect`.

### 5.3 Operations (shared by the browser page and the tests)

| Operation | Input | Effect / output |
|---|---|---|
| start | topic (string), stop_after (set of step names) | Creates the next thread id (`"0"`, `"1"`, …, decimal strings counting from 0), sets the starting record (R2), runs steps (R12). Returns the live output text. |
| continue | thread id, stop_after | Runs steps from the thread's latest record (R12). |
| current | thread id | The latest record plus next step (none when the run has ended). |
| history | thread id | Entries latest first, one per saved record after the first step: `thread:count:last_step:next_step:revision_number:snapshot_id`. Records saved before the first step are not listed. |
| snapshots | thread id | All saved records as text, with `plan`, `draft`, `critique` cut to their first 80 characters plus `...` and each research text cut to its first 20 characters plus `...`. |
| modify | thread id, field ∈ {plan, draft, critique}, new text | R14. Does not run any step. |
| rewind | thread id, snapshot id | R15. Does not run any step. |
| threads | — | List of thread ids, in creation order. |

### 5.4 Search contract

A search takes one query string and returns at most 2 result texts (strings), best first. The research step appends them to `content` in query order, then rank order.

### 5.5 Model roles

| Role | Used by step | Instructions (course content, in words) | Input | Output |
|---|---|---|---|---|
| planner | `planner` | An expert writer writing a high-level outline of an essay for the user's topic, with relevant notes or instructions for each section. | task | plain text → `plan` |
| researcher | `research_plan`, `research_critique` | After the plan: a researcher providing information for writing the essay; generate a list of search queries that will gather any relevant information; only generate 3 queries max. After a critique: the same, for making the requested revisions (the critique); only generate 2 queries max. | after the plan: task and plan; after a critique: critique only | a structured list of query strings |
| writer | `generate` | An essay assistant writing excellent 5-paragraph essays; generate the best essay possible for the user's request and the initial outline; if the user provides critique, respond with a revised version of previous attempts; use all the information below as needed, followed by a separator line and all research texts joined by one blank line. | user part: `task`, a blank line, `Here is my plan:`, a blank line, `plan` | plain text → `draft` |
| critic | `reflect` | A teacher grading an essay submission; generate critique and recommendations, detailed, including requests for length, depth, style. | draft | plain text → `critique` |

With C1b, replace "essay" and "5-paragraph" in these instructions with the chosen form and length.

### 5.6 Settings

| Setting | Value | Source | Change this when … |
|---|---|---|---|
| Essay length in the writer's instructions | 5 paragraphs | Lesson 7 notebook writer prompt and slide 7.3; the browser app used 3 | you want shorter or longer pieces |
| Queries after the plan (instruction limit) | at most 3 | Lesson 7 notebook and browser app, slide 7.3 | your topics need wider research |
| Queries after a critique (instruction limit) | at most 2 | Lesson 7 browser app; the notebook used 3 | critiques ask for many separate points |
| Results per query | 2 | Lesson 7 notebook and browser app | research is too thin (raise) or the writer's input is too long (lower) |
| `max_revisions` default | 2 | Lesson 7 notebook, transcript and browser app | you want more or fewer redrafts |
| `revision_number` at start | 1 | Lesson 7 notebook and transcript; the browser app used 0 | — (with 1, the number of drafts equals `max_revisions`) |
| Model temperature | 0 | Lesson 7 notebook and browser app | you want more varied drafts; omit it for a model family that rejects the parameter |
| Stop-after default | all five steps checked | browser app | you want runs to go further between stops |
| Steps per thread through the interface | 10 | browser app | you rewind or redraft often (see note on R16) |
| Default topic on the page | `Pizza Shop` | browser app | — |
| Snapshot summary cuts | 80 characters (plan, draft, critique), 20 (each research text) | browser app | — |
| Live output area | 5 lines | browser app | — |

## 6. Business rules

### What must stay true (the pattern card, copied; every option keeps every item)

- **M1. Fixed flow with one decision point, through separate roles that share one record.** Every run follows the same order: plan → research → draft → decide. If the run continues, the order is critique → research → draft → decide again. The only branch is the decision after each draft: finish, or go round again. Each step is its own LLM role with its own instructions (planner, researcher, writer, critic). The roles pass work to each other only through one shared record of the run: task, plan, research, draft, critique and revision count. → T3, T4
- **M2. A plan is made once, before any research or drafting, and every draft follows it.** → T3, T5
- **M3. Research grounds the writing, and the research only grows.** Before the first draft, and again after every critique, the program writes a few search queries, runs them, and adds the results to the research gathered so far. Earlier research is never dropped. Every draft is written with all the research gathered so far. → T5, T6, T16
- **M4. Critique drives each revision.** After a draft, if the run continues, a critic role writes a critique of that draft. The next draft is written only after that critique has been turned into new research. → T4, T6
- **M5. The loop is bounded by a revision count kept in the record.** Each draft adds one to the revision count. After each draft, the program compares that count with the maximum given for the run, then ends or goes round again. Every run ends. → T4, T9
- **M6. Every step is saved, per thread.** The record is saved after every step under a thread id. Continuing a thread resumes it with its full history. A different thread is a separate piece of work with no shared history. → T10, T11
- **M7. A person can stop, inspect, edit and rewind the run.** The run can stop after any step the person chooses. The person can then view the current record, change a field (for example the plan), and continue from the changed record. They can also pick an earlier step's saved record and continue from there. An edit or a rewind adds a new latest record and never erases the history. → T12, T13, T14, T15

### Rules

- **R1. Flow.** Steps run in the order of 5.2. After each `generate`, the decision is `end` when `revision_number > max_revisions`, otherwise `reflect`. No other branch exists. → T3, T4, L1
- **R2. Starting record.** `start` saves a record with `task` = topic, `max_revisions` = 2 (unless given), `revision_number` = 1, `plan` = `draft` = `critique` = `""`, `content` = `[]`, `queries` = `[]`, `last_step` = `""`, `count` = 0. Steps read and write only this record. → T2
- **R3. Plan once.** `planner` runs exactly once per run, first, and writes `plan`. → T3
- **R4. Writer input.** `generate` sends the writer its instructions followed by all of `content` joined by one blank line, and a user part of `task` + blank line + `Here is my plan:` + blank line + `plan`. It does not send `critique` or the previous `draft` (course behaviour; C6b changes this). It writes `draft` and adds 1 to `revision_number`. → T5, T19
- **R5. Research after the plan.** `research_plan` asks the researcher, with the after-plan instructions, for a list of queries, giving it the task and the plan. Every returned query is searched; the "3 max" limit lives in the instructions only and the program does not cut the list (course behaviour). → T6, T19, L2
- **R6. Research only grows.** Each research step appends every result text of every query to `content`, in query order then rank order, at most 2 per query, keeping duplicates and never removing or reordering earlier items. → T6, T8, T16
- **R7. Bounded loop.** Each draft adds exactly 1 to `revision_number`; with the start value 1, a run makes `max_revisions` drafts and then ends. → T4, T9, L1
- **R8. Critique and research after it.** `reflect` sends the critic its instructions and the latest `draft`, and writes `critique`. `research_critique` asks the researcher, with the after-critique instructions, for queries, giving it `critique` only; results are appended as in R6; the flow then returns to `generate`. → T4, T6, T19
- **R9. Queries field.** `research_plan` writes its queries to `queries`; `research_critique` does not change `queries` (course behaviour). → T6
- **R10. Every step saved.** After every step the record is saved under the thread with `last_step` = that step's name and `count` increased by 1. `count` is an adding field: any write adds the written value to it, including the writes of R14 and R15 (course behaviour). → T10
- **R11. Threads.** Every `start` creates a new thread with the next id (`"0"`, `"1"`, …). A thread's records, research and history never include anything from another thread. → T2, T11
- **R12. Stopping after chosen steps.** `start` and `continue` run one step at a time and stop after a step whose name is in `stop_after`, when the run has ended, or when R16's limit is reached. The default `stop_after` is all five steps, so each press runs one step. → T12, T18
- **R13. Viewing.** `current`, `history` and `snapshots` return what 5.3 says, latest first, and change nothing. → T13, T18, T20
- **R14. Editing.** `modify` writes the latest record back with one field changed, as a new latest record written as if by the step that produces that field (`plan` by `planner`, `draft` by `generate`, `critique` by `reflect`); the next step is the one that follows that step in the flow. Earlier records are unchanged. → T14
- **R15. Rewinding.** `rewind` takes the saved record with the given snapshot id and writes its values as a new latest record, as if by that record's `last_step`; the next `continue` runs from it. Earlier records, including those after the chosen one, are unchanged. → T15
- **R16. Steps per thread through the interface.** Across all `start`/`continue` calls on one thread, at most 10 steps run; after that, `continue` runs nothing and leaves the record unchanged (course behaviour, see notes). → T16
- **R17. Local search (stand-in for the course's web search service; C3a).** The `library/` folder holds `.txt` and `.md` files. Each file is split into passages at blank lines. Words are lowercase runs of letters and digits of length 3 or more, minus the stopwords `the and for are was were with from that this how what why its into than has had but not`. A passage's score for a query is the number of distinct query words found among its words. A search returns the text of up to 2 passages with score ≥ 1, highest score first, ties broken by file name (ascending) then passage order. → T1, T7, T8
- **R18. Missing model key.** With the real provider and no key in the environment, `start` reports that `OPENAI_API_KEY` (or the chosen provider's key) is not set and runs no step and creates no thread. → T17
- **R19. Fresh start.** On a fresh start the saved-step store exists and holds no threads, and `threads` returns an empty list. → T1
- **R20. Model settings.** The real model is configured with temperature 0 (where the chosen model accepts it). → T19

## 7. Tests

### 7.1 Sample data

**`library/` (ships with the build; used by offline tests).** Each line below is one passage; each file's passages are separated by one blank line. The `[Fn]` tags are part of the text.

- `delivery.txt`
  - `[F5] Delivery in Velmora began in 1921 with bicycles carrying insulated boxes.`
  - `[F6] Records show drivers in vans replaced the bicycles by 1960.`
- `gardening.txt`
  - `[F7] Tomato plants need six hours of sun each day.`
- `history.txt`
  - `[F3] The first pizza shop in Velmora opened in 1897 and sold slices.`
  - `[F4] Early owners baked bread in the morning and pizza at night.`
- `ipa.txt`
  - `[F8] A New England IPA is hazy because of late hops.`
- `ovens.txt`
  - `[F1] A wood-fired oven reaches a temperature of 450 degrees Celsius and bakes a pizza in ninety seconds.`
  - `[F2] Electric deck ovens run cooler, near 300 degrees.`

All facts are invented for this spec. `gardening.txt` is a planted unrelated document that no test query may return.

**Scripted stand-in model (stand-in for the real provider; `tests/stand_ins.py`).** It decides its reply by the role making the call (how the role is passed is the build's choice) and records every input it receives.

| Role | Reply |
|---|---|
| planner | `Plan for <task>: I. Origins II. Ovens III. Delivery` (with the task text inserted) |
| researcher, after the plan | if its input contains `IPA`: `["hops haze"]`; otherwise `["oven temperature", "first shop opened", "delivery began"]` |
| researcher, after a critique | `["drivers vans", "bread morning"]` |
| writer | `Essay draft citing ` followed by every tag `F<n>` found in its instructions, each once, in order of first appearance, separated by single spaces |
| critic | `Critique: say more about how delivery changed and how early shops worked.` |

**Expected search results (replayed against R17).**

| Query | Results |
|---|---|
| `oven temperature` | F1 |
| `first shop opened` | F3 |
| `delivery began` | F5 |
| `drivers vans` | F6 |
| `bread morning` | F4 |
| `hops haze` | F8 |
| `pizza` | F3, F4 (F1 also scores 1 but `ovens.txt` sorts after `history.txt`) |
| `quantum` | none |

**Planted failure (from Lesson 5): a second thread sees nothing of the first.** Thread `"0"` runs topic `Pizza Shop`; thread `"1"` runs topic `New England IPA`.

**Planted edit (from the Lesson 7 walkthrough):** the plan replacement text `Discuss the importance of jelly donuts in pizza making`.

### 7.2 Test table

All offline tests use the stand-in model and the local search on `library/`. "Full run" = `start("Pizza Shop", stop_after = {})` with the default `max_revisions` 2.

| ID | Rules | Given | When | Then |
|---|---|---|---|---|
| T1 | R17, R19 | fresh start | the program starts | the saved-step store exists and holds no threads; `threads` = `[]`; `library/` holds the 5 sample files |
| T2 | R2, R11 | fresh start | `start("Pizza Shop", stop_after = {planner})` | thread `"0"` exists; record: `task` `Pizza Shop`, `max_revisions` 2, `revision_number` 1, `plan` `Plan for Pizza Shop: I. Origins II. Ovens III. Delivery`, `draft` `""`, `critique` `""`, `content` `[]`, `queries` `[]`, `last_step` `planner`, `count` 1 |
| T3 | R1, R3 | fresh start | full run | the `last_step` values of the saved records, oldest first, are `planner, research_plan, generate, reflect, research_critique, generate`; `planner` appears once; next step is none |
| T4 | R1, R7, R8 | fresh start | full run | final `revision_number` 3; writer called 2 times, critic 1 time; `critique` = the critic reply; final `draft` = `Essay draft citing F1 F3 F5 F6 F4`; `count` 6 |
| T5 | R4 | fresh start | full run | first writer input: instructions contain `5-paragraph` and end with the F1, F3, F5 passages joined by one blank line; user part = `Pizza Shop`, blank line, `Here is my plan:`, blank line, the plan; second writer input contains F1, F3, F5, F6, F4 passages; neither input contains the critique text nor `Essay draft citing` |
| T6 | R5, R6, R8, R9 | fresh start | full run | `content` after `research_plan` = [F1, F3, F5] passages; final `content` = [F1, F3, F5, F6, F4]; after-plan researcher input contains both `Pizza Shop` and the plan; after-critique researcher input equals the critique text; final `queries` = `["oven temperature", "first shop opened", "delivery began"]` |
| T7 | R17 | `library/` as given | search each query in the expected-results table | results exactly as listed; F7 never returned |
| T8 | R6, R17 | `library/` as given | search `pizza` | exactly 2 results: F3 then F4 |
| T9 | R7 | fresh start | `start("Pizza Shop", stop_after = {})` with `max_revisions` 1 | 3 steps run (`planner, research_plan, generate`); `revision_number` 2; critic never called; next step none |
| T10 | R10 | full run done | `history("0")` | 6 entries, latest first, with `count` 6, 5, 4, 3, 2, 1 and `last_step` `generate, research_critique, reflect, generate, research_plan, planner`; all snapshot ids distinct; the entry with `count` 3 has `draft` `Essay draft citing F1 F3 F5` |
| T11 | R11 | full run done on thread `"0"` | `start("New England IPA", stop_after = {})` with `max_revisions` 1 | new thread `"1"`; its `content` = [F8 passage]; `plan` `Plan for New England IPA: I. Origins II. Ovens III. Delivery`; `draft` `Essay draft citing F8`; no F1–F7 text anywhere in its record; its history has 3 entries; thread `"0"`'s latest record is unchanged; `threads` = `["0", "1"]` |
| T12 | R12 | fresh start | `start("Pizza Shop")` with default `stop_after`, then `continue("0")`; separately, on a fresh start, `start("Pizza Shop", stop_after = {generate})` | first call stops with `last_step` `planner`, `count` 1, next `research_plan`; `continue` stops with `last_step` `research_plan`, `count` 2; the second run stops with `last_step` `generate`, `count` 3 |
| T13 | R13 | `start("Pizza Shop")` stopped after `planner` | `current`, `history`, `snapshots` | `current` shows the plan and next step `research_plan`; `history` has 1 entry `0:1:planner:research_plan:1:<id>`; `snapshots` shows the plan as its first 80 characters plus `...`; calling them twice changes nothing |
| T14 | R14 | `start("Pizza Shop")` stopped after `planner` | `modify("0", plan, "Discuss the importance of jelly donuts in pizza making")`, then `continue` twice | after modify: latest record has the jelly plan, `last_step` `planner`, `count` 2, next `research_plan`; the `count` 1 entry still has the original plan; after the two continues: the writer's user part contains the jelly plan; `count` 4; `revision_number` 2 |
| T15 | R15 | the end state of T14 | `rewind("0", <snapshot id of the count-1 entry>)`, then `continue` twice | after rewind: latest record has the original plan, `content` `[]`, `draft` `""`, `revision_number` 1, `last_step` `planner`, `count` 5, next `research_plan`; history has 5 entries and the 4 earlier ones are unchanged; after the continues: the latest writer user part contains the original plan and not `jelly`; `draft` `Essay draft citing F1 F3 F5`; `count` 7 |
| T16 | R6, R16 | fresh start | `start("Pizza Shop", stop_after = {})` with `max_revisions` 10, then `continue("0", stop_after = {})` | the start runs exactly 10 steps and stops with `last_step` `reflect`, `count` 10, next `research_critique`; `content` = [F1, F3, F5, F6, F4, F6, F4]; the continue runs no step and the record is unchanged |
| T17 | R18 | real provider configured, `OPENAI_API_KEY` unset | `start("Pizza Shop")` | the message names `OPENAI_API_KEY` as not set; no step runs; `threads` = `[]` |
| T18 | R12, R13 | fresh start | build the browser page without launching it | it has tabs `Agent`, `Plan`, `Research Content`, `Draft`, `Critique`, `StateSnapShots`; the topic box holds `Pizza Shop`; all five steps are checked under "Interrupt After State"; Plan, Draft and Critique tabs have Refresh and Modify; Research Content has Refresh only; the live output area shows 5 lines |
| T19 | R4, R5, R8, R20 | the program's configuration | read the role instructions and the real model settings | writer instructions contain `5-paragraph`; after-plan researcher instructions contain `3 queries max`; after-critique researcher instructions contain `2 queries max`; the real model is set to temperature 0 |
| T20 | R13 | full run done | `snapshots("0")` | the text contains `[F1] A wood-fired ov...` (first 20 characters of the F1 passage plus `...`) and the final draft cut to its first 80 characters plus `...` |
| L1 `live` | R1, R7 | `OPENAI_API_KEY` set; `library/` as given | full run on `Pizza Shop` with the real model and local search | the run ends with `revision_number` 3, two drafts written, a non-empty final `draft`, and non-empty `content` |
| L2 `live` | R5 | `OPENAI_API_KEY` set | the after-plan researcher is asked for queries on `Pizza Shop` | it returns a list of 1 to 3 non-empty strings |

## 8. Standing permissions

- **Always:** run the offline tests after every change; keep stand-ins labelled as stand-ins in code comments and the interface; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has saved data; anything that sends data to a third party beyond the chosen model provider and research source.
- **Never:** invent provenance; answer when the program should say it does not know (for example, report a missing key or an empty research result instead of hiding it); change sample data to make a test pass; commit secrets.

## 9. Test plan

1. Install: create a virtual environment and install the packages for the chosen options.
2. Offline: `python -m pytest -m "not live"` — every T test must pass.
3. Live: `OPENAI_API_KEY=… python -m pytest -m live` — L1 and L2; skipped without the key, which is not a failure.
4. For every chosen non-recommended option, turn its "what to check" sentence from section 1 into a test, run it, and report it.
5. Run the app (`python app.py` for the browser page, or the terminal command for C8b) and do one full run on `Pizza Shop` with the stop-after checks cleared.
6. Report one result per test with evidence (test output, file paths). "Should pass" counts as not run.

The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.

Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

## 10. Background notes

### The program
A program that writes a piece on a topic by planning, researching, drafting and critiquing in a bounded loop, saving every step per thread so a person can control it. Stages:
- **plan** — fixes the structure once, so every draft follows one outline.
- **research (after the plan)** — writes a few queries and gathers texts, because a model's fixed knowledge cannot be trusted on current or specific facts.
- **draft** — writes the piece from the topic, the plan and all research.
- **decide** — ends when the revision count passes the limit, so every run ends.
- **critique** — a separate role judges the draft and asks for changes.
- **research (after the critique)** — turns the critique into new queries and more research, which drives the next draft.
- **save every step per thread** — makes the run resumable, separable by topic, and controllable.
- **human control** — stop after chosen steps, view, edit, rewind.

### Failures
- **A separate thread has no history (Lesson 5, demonstrated).** What you see: asking "which one is warmer?" on a new thread id left the model confused, because that thread had none of the earlier conversation. Why: saved state is kept per thread. How the spec prevents it from causing harm: a new topic always gets a new thread, and a thread only ever sees its own record (R11); the planted second topic checks it (T11).
- **Answering from fixed model knowledge (Lesson 4, warned).** The instructor warns a model's weights cannot answer about recent events and that sources reduce hallucination. The spec makes every draft use all research gathered (R4, R6; T5, T6).
- **Failures from other lessons, kept as notes only.** The Lesson 3 notebook added a guard because a model can call a tool name that does not exist, answering "bad tool name, retry" (relevant to C4b). The Lesson 4 notebook falls back to fixed links when the keyless web search refuses requests under heavy traffic (relevant to C3c).

### Notes for the build agent on course behaviour kept as is
- The writer's instructions say "if the user provides critique, respond with a revised version", but the course never passes the critique or the previous draft to the writer; it gets only the topic, plan and research. Kept (R4); C6b offers the other behaviour.
- `research_critique` does not record its queries; `queries` keeps the after-plan list. Kept (R9).
- `count` adds on every write, so editing doubles it and rewinding adds the old record's count (the Lesson 6 notebook points out that a write to an adding field adds rather than replaces). Kept (R10).
- The browser app's 10-step limit counts every step a thread has ever run through the page, not per press, so a thread that has rewound a few times stops responding. Kept (R16); raise the setting if it gets in the way.
- The query limits live only in the instructions; the program runs every query returned. Kept (R5).
- Research texts are appended without removing duplicates. Kept (R6).

### Why the questions and settings are what they are
- **C1:** the course only wrote essays, but every role instruction names the form; a learner's own version changes only the wording.
- **C2:** the course used OpenAI and says the model wrapper can be swapped for another supported provider without changing other code; the course credits function calling for reliable structured output, which the researcher needs.
- **C3:** the course used Tavily because agents want answers to cite, in a predictable format, rather than links; it contrasted a keyless regular search that returned links and long page text. The local folder is the recommended stand-in because Tavily needs its own key.
- **C4:** the agentic research loop is the Lessons 2–3 agent (a model calling search until done, with a turn limit of 5 in Lesson 2's loop); the pattern card offers it.
- **C5:** Lesson 6 interrupts before tools run "to make sure that tools are executed correctly"; the pattern card offers it for the research step.
- **C6:** see the first note above.
- **C7:** Lesson 5 uses an in-memory store and says it "will disappear" on refresh, and that other checkpointers use Redis and Postgres and other persistent databases.
- **C8:** the course's final app is a browser page; a notebook is never offered, as the build is a program.
- **C9:** Lesson 5 streams step messages and then tokens; Lesson 7 streams steps "because this is going to take a while"; the pattern card offers streaming.

**Subjects that are not questions (each failed a test in the guide's 5.2):**
- *Skip the plan* — fails test 1 (breaks M2).
- *Plan-and-execute with replanning (Lesson 9)* — fails test 1 (M2: the plan is made once).
- *Skip the critique, or redraft straight from the critique without research* — fails test 1 (M4).
- *A critic that can end the run early* — fails test 1 (M5: the decision compares the count with the limit).
- *No saved steps, or no human control (the Lesson 7 notebook version before the browser app)* — fails test 1 (M6, M7).
- *Supervisor, multi-agent router, flow engineering, tree search (Lesson 9)* — fail test 1 (M1: fixed flow and one shared record).
- *The Lessons 2–6 single-agent research assistant as the whole program* — fails test 1 (it has no plan, critique or revision loop); its loop survives as C4b.
- *Different models per role* — not a question: a model per role is a setting, chosen at the checklist (guide 4.3).
- *Editing the research directly* — fails test 3: the course's page shows research read-only, and vetting research input is already covered by C5b; no learner situation needs a third way.
- *Supplying a search result by hand (Lesson 6, "as if" the tool ran)* — fails test 3 for the same reason as above.
- *Where it runs (on your machine or as a web service)* — fails test 3: every option runs on the learner's machine; the course only names a deployment tool as a further resource, and serving it to others is covered by C7c's shared store.
- *A custom message-merging rule (Lesson 6)* — not part of this program: the record has no message list.
- *Which model the tests use* — never asked (guide 5.8).

### Where values came from
- **Five paragraphs:** the instructor does not say a number aloud; slide 7.3, which the instructor talks through when introducing the essay writer, shows the writer prompt "writing excellent 5-paragraph essays" (Lesson 7 notebook, cell 6). The browser app's prompts say 3 paragraphs and ask the planner for three main headers. Picked by rule (1), the value shown when introducing the concept; the other value is recorded here.
- **Queries after a critique:** notebook cell 9 says 3 max; the browser app says 2 max. The instructor states neither; picked by rule (2), the course's final end-to-end app.
- **Queries after the plan:** 3 max in notebook cell 8, the browser app and slide 7.3.
- **Results per query:** 2 in notebook cells 13 and 16 and the browser app. (Earlier lessons used 4 and 2 for a different tool.)
- **Revision start:** the instructor passes 1 ("it is starting on the first revision") and says the run makes two drafts (notebook cell 25); the browser app passes 0. Picked by rule (1).
- **Max revisions:** 2 everywhere.
- **Temperature 0 and the model `gpt-3.5-turbo`:** notebook cell 4 and the browser app. (The transcript says "I don't think GPT-3.5 knows about any of these" when choosing the example topic.)
- **Researcher input after the plan:** the instructor says "given a plan, we're going to generate a bunch of queries" and "based on that plan we're going to do some research"; when walking through the code, he says the queries are generated "based on the task", and the code passes only the task. The spec follows the introductory statement and passes task and plan.
- **Starting fields:** the browser app seeds `content` with `["no content"]` and other fields with placeholder words (and a misnamed `planner` key instead of `plan`); the notebook starts without them; in the walkthrough the instructor reads the empty research as "we don't have any". The spec starts them empty.
- **Thread ids:** the browser app counts threads from 0 as decimal strings; the instructor refers to "thread zero" and "one".
- **Stop-after default, 10-step limit, default topic `Pizza Shop`, snapshot cuts 80/20, 5-line live output:** the browser app.
- **History entry format:** the browser app's step picker shows `thread:count:last_node:next_node:rev:thread_ts`.

### Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports: `StateGraph`, `END`, `set_entry_point`, `add_conditional_edges`, `compile(checkpointer=…, interrupt_after=…, interrupt_before=…)`, `get_state`, `get_state_history`, `update_state(…, as_node=…)`, `SqliteSaver.from_conn_string(":memory:")`, `langgraph.checkpoint.sqlite`, `langgraph.checkpoint.aiosqlite.AsyncSqliteSaver`, `thread_ts` (snapshot id; newer releases call it a checkpoint id), `astream_events(version="v1")`, `on_chat_model_stream`, `ChatOpenAI`, `with_structured_output`, `langchain_core.pydantic_v1.BaseModel`, `TavilyClient`, `TavilySearchResults` (`langchain_community.tools.tavily_search`), `duckduckgo_search.DDGS`, BeautifulSoup, Gradio `Blocks`, `draw_png`; models `gpt-3.5-turbo`, `gpt-4o`. Some current model families reject the `temperature` parameter; then leave it out and say so in the checklist.

### Course names
| Course name | Spec term |
|---|---|
| `AgentState` | the run record |
| `task`, `plan`, `draft`, `critique`, `content`, `queries`, `revision_number`, `max_revisions`, `count` | same names (binding) |
| `lnode` | `last_step` |
| nodes `planner`, `research_plan`, `generate`, `reflect`, `research_critique` | same step names (binding) |
| `should_continue` | the decision after `generate` |
| `ewriter` | the program |
| `writer_gui` | the browser page |
| "Generate Essay", "Continue Essay", "Interrupt After State", tab names | same labels on the page |
| thread id, `thread_ts` | thread id, snapshot id |

### Lesson map (transcript numbering)
- **1 Introduction** — the agentic writing workflow (plan, research, draft, critique) and design patterns; motivation for the program.
- **2 Build an Agent from Scratch** — the hand-built tool-calling loop and its turn limit (C4b).
- **3 LangGraph Components** — steps, edges, conditional edges, the shared record and adding fields; provider swap (C2); the tool-name guard (failure notes).
- **4 Agentic Search Tools** — why agents search, agent-ready search versus links (C3), dynamic data (failure notes).
- **5 Persistence and Streaming** — saved steps, threads, the in-memory store and other stores (C7), step and token streaming (C9), the separate-thread failure.
- **6 Human in the loop** — stopping before a step (C5), viewing, editing, history, rewinding, writing as a step, adding fields adding on write (R10, R14, R15).
- **7 Essay Writer** — the program itself: record, roles, prompts, flow, values, the browser app and its walkthrough (edit the plan, rewind, second thread).
- **8 LangChain Resources** — package landscape; nothing changes the program.
- **9 Conclusion** — other architectures (not questions, see above).

Slides: all slide descriptions were read. Slide 7.3 (narrated) counted like the Lesson 7 transcript and decided the paragraph count; slides 3.9 and 6.3–6.17 (narrated) confirmed the record and saved-step behaviour; deck-only slides (6.17, 9.11, backup slides) were not used for any decision.

Nothing in this spec requires access to the course.

---

*Spec v2 draft · course: AI Agents in LangGraph · project: plan, research, draft and critique writer · When the build agent does something unexpected, add the missing constraint here and re-run.*
