# Spec: a crew of AI agents that works one job through defined tasks

**What you're building:** a program that takes a few named inputs for one job, runs a team of specialised AI agents through a set of defined tasks, hands each task's result to the tasks that depend on it, and writes out the finished results. By default it is a job-application crew: you give it a job posting link, your GitHub page link and a short write-up about yourself, and it reads your résumé. You then see four agents work: two research in parallel, a third rewrites your résumé for the posting, and a fourth writes interview questions and talking points. You get two Markdown files.

**What the recommended build needs to run:** an OpenAI API key (for the agents' model and for the embeddings behind the résumé search), and network access to fetch the job posting and GitHub pages. No search-API key, other account or large download.

**Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once `OPENAI_API_KEY` is set and are skipped until then; that is not a failure.

This file is self-contained: everything the build needs is in it.

*Provenance: course "Multi AI Agent Systems with crewAI" (18 lessons); materials used: lesson transcripts, the six course notebooks with their notebook map, the slide descriptions, and the owner-confirmed pattern card (confirmed 2026-10-27); generated 2026-10-27 with guide v2.8 (2026-10-27).*

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
   an OpenAI API key and network access), or **choose** question by
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

### C1. Which job should your crew do?
- **C1a. Tailor a résumé to a job posting and prepare for the interview** (Recommended - course default). Pick this when you want the crew described in this spec, working on your own résumé and a real posting. Setup: none beyond the recommended build.
- **C1b. A different job you describe.** Pick this when you have another multi-step job for a team of agents, for example researching and writing an article, answering a customer's question and checking the answer, profiling a sales lead and drafting outreach, planning an event, or analysing a stock. You name the inputs, the agents (role, goal, backstory, tools), the tasks (description, expected output, agent, which tasks it depends on) and the result files; the build replaces the sample team definition with yours and writes sample data and tests for it in the same shape as section 8. Setup: whatever your agents' tools need (e.g. a key for a service they call).
  *What to check:* every agent in your team has a role, goal and backstory, every task has a description, an expected output and an agent, a task that depends on others receives their outputs and starts only after them, and every input you name appears filled in wherever your agents and tasks use it.

### C2. What format is your résumé in?
*Ask only when `C1` is `C1a`.*
- **C2a. Markdown or plain text** (Recommended - course default). Pick this when your résumé is already a `.md` or `.txt` file, or you can paste it into one. Setup: none.
- **C2b. PDF.** Pick this when your résumé exists only as a PDF and you do not want to convert it by hand. Setup: a PDF text-extraction library (small download).
  *What to check:* the text the crew reads from the PDF résumé contains every section heading and every employer name in the original.
- **C2c. Word (.docx).** Pick this when your résumé is a Word document. Setup: a .docx reading library (small download).
  *What to check:* the text the crew reads from the Word résumé contains every section heading and every employer name in the original.

### C3. Which model provider will the agents use?
- **C3a. OpenAI** (Recommended - course default). Pick this when you have, or can get, an OpenAI API key. Setup: `OPENAI_API_KEY`, paid usage.
- **C3b. Another hosted provider** (for example Mistral, Cohere or a model served through Hugging Face). Pick this when you already pay for another provider or your organisation requires one. Setup: that provider's API key; the résumé search also needs an embedding model, from the same provider or another one.
  *What to check:* every agent's model requests go to the chosen provider, and a full run on the sample inputs writes both result files.
- **C3c. A local model served on your machine** (for example through Ollama). Pick this when you cannot send your résumé to a hosted service, or have no API key. Cost: a model download of several GB and a capable machine; smaller models get confused when an agent has many tools and may repeat tool calls, so runs are slower and less reliable. Setup: install the local model server and pull a chat model and an embedding model.
  *What to check:* with the network to hosted model providers blocked, a full run on the sample inputs still writes both result files.

### C4. How will you start a run?
- **C4a. A command in the terminal** (Recommended). Pick this when you run the crew yourself, one job at a time. Setup: none.
- **C4b. A small local web service** that accepts the inputs as a JSON request and returns the results. Pick this when another program of yours needs to start runs and read the results. Setup: a web framework package; a free local port.
  *What to check:* a request carrying the sample inputs returns both results, and a request missing an input is refused with that input's name before any model call.

### C5. Should the agents be able to search the web?
- **C5a. No web search; agents read only the pages you link and your résumé** (Recommended). Pick this when the posting and your GitHub page carry what the crew needs. Setup: none.
- **C5b. Add a web-search tool** (course default). Pick this when you want agents to look up the hiring company, the technologies named in the posting, or your public work beyond the links you give. Cost: a search-API account and key (the course used Serper, which offers free credits), and more model calls per run.
  *What to check:* an agent given the search tool can call it during a run and its results appear in that agent's next request to the model.

### C6. May agents hand work to each other or ask each other questions during a run?
- **C6a. Yes** (Recommended - course default). Pick this when you prefer better answers to predictable runs: an agent may pass part of its work to a teammate better suited to it, or ask it a question. Cost: more model calls, and runs differ more from one another.
- **C6b. No; each agent does only its own tasks.** Pick this when you want each run to follow the same path and cost about the same.
  *What to check:* in a full run, no agent hands work to or asks a question of another agent.

### C7. Should a reviewer check the final results before they are written?
- **C7a. No reviewer** (Recommended - course default). Pick this when you read the results yourself before using them. Setup: none.
- **C7b. Add a quality-assurance reviewer agent** with its own review task that runs last, checks the results against the inputs for accuracy and completeness, and produces the final version. If `C6` is `C6a`, it may also send work back to the agent that produced it. Pick this when the output goes straight to someone else (an employer, a customer) and should be fact-checked first. Cost: one more agent and task, more model calls.
  *What to check:* the reviewer's task receives the outputs it reviews, runs after them, and the files written are the reviewer's final versions.

### C8. Should the crew pause for your feedback before a task's result is final?
- **C8a. No; the run goes start to finish unattended** (Recommended - course default). Pick this when you want to start a run and come back to the results.
- **C8b. Yes, on the tasks you name.** Pick this when you want to steer an intermediate result (e.g. approve the job-requirements list) before later tasks build on it. Cost: the run waits at the terminal for you.
  *What to check:* the run stops at each named task, shows its result, and the task's final result reflects the feedback typed in.

### C9. How should the tasks be coordinated?
- **C9a. A fixed plan: tasks that don't depend on each other run in parallel; a task that depends on others waits for them** (Recommended - course default). Pick this when you know the steps of the job in advance. Setup: none.
- **C9b. Strictly one task after another, in list order, each getting the previous task's output.** Pick this when every step builds on the one before and you want the simplest run to follow. Cost: slower, and over a long chain the original inputs fade from later tasks' attention.
  *What to check:* no task starts before the task listed before it has finished, and each task's request includes the previous task's output.
- **C9c. A manager agent coordinates:** the framework adds a manager that keeps the overall goal, hands each task to its assigned agent, passes on what earlier agents found, and reviews results. Pick this when you would rather have a manager decide the flow and ask for improvements than fix it yourself. Cost: a model for the manager and many more model calls; the order of work varies between runs.
  *What to check:* every task is done by its assigned agent at the manager's request, and each agent's request includes what earlier agents found.

### C10. Should the crew remember across steps and across runs?
- **C10a. No memory beyond passing task results** (Recommended - course default). Pick this when each run is a separate job and you want runs independent of each other.
- **C10b. Turn on the crew's memory:** short-term memory shared by the agents during a run, long-term memory stored in a local database so agents learn from earlier runs, and memory of the people, organisations and places discussed. Pick this when you run the crew many times on similar jobs and want it to improve with use. Cost: local storage that grows over runs.
  *What to check:* after a first run, the memory store exists on disk, and a second run's agent requests include material recalled from the first run.

### C11. In what form should the results be written?
- **C11a. Markdown files** (Recommended - course default). Pick this when people read the results.
- **C11b. Markdown files plus a JSON file per result, matching a schema you define.** Pick this when another program reads the results (e.g. stores them in a database). Cost: you define the fields; the model's answer is converted to that structure.
  *What to check:* each JSON file validates against its schema and holds the same content as its Markdown result.

### Departures from the course (recommended build)
| # | Where | Course did | Recommended build does | Why |
|---|---|---|---|---|
| D1 | Web search tool | Gave the agents a Google-search tool (Serper) needing its own key | Leaves web search out (C5b adds it back) | It needs a second key and account; reading the linked pages and the résumé already exercises tool use. |
| D2 | Versions | Pinned `crewai==0.28.8`, `crewai_tools==0.1.6`, `langchain_community==0.0.29` | Current releases | Course-era versions often no longer install or work with current models. |
| D3 | Model | Videos used `gpt-4-turbo`; notebooks ran `gpt-3.5-turbo` | A current model from the chosen provider, named in the gate checklist | Model names go stale. |
| D4 | How it runs | Notebook cells | A terminal command (C4) | A notebook is how the course is taught, not the program. |
| D5 | Sample data | A made-up résumé, a real job-board posting and a real GitHub profile | Sample résumé, posting and GitHub page written for this spec, served from local files in tests | No course data is copied; tests must run offline. |
| D6 | Delegation | Left unset on the final crew's agents; the course states the default was "allowed" | Sets "allowed" explicitly | Current defaults may differ; the course's behaviour is kept. |
| D7 | Résumé search embeddings | Not named by the course | The chosen provider's embedding model (addition) | The search needs one; the gate's model line names it. |
| D8 | Additions | — | Input check before any model call; team definition validated on load; run log; output folder; run returns only after result files are written; clear message when the key is missing | Labelled additions that make the build checkable (sections 7–8). |

---

## 2. Objective
Given a job-posting link, a GitHub-profile link, a short personal write-up and a résumé file, a crew of four role-playing agents writes a résumé tailored to the posting and a set of interview questions and talking points, each to its own Markdown file.

## 3. Tech stack and secrets
- Python (current release), crewAI and its tools package (current releases; see section 11 "Names that go stale"), pytest for tests. Package name: `crew_app`.
- Secrets come only from the environment (`OPENAI_API_KEY`, and under C5b the search key); a `.env` file may be loaded; it is never committed.
- Network access is needed at run time only by the page-reading tool.

## 4. Contracts

### 4.1 Run inputs (`inputs.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["job_posting_url", "github_url", "personal_writeup"],
  "additionalProperties": false,
  "properties": {
    "job_posting_url": {"type": "string", "format": "uri", "pattern": "^https?://"},
    "github_url":      {"type": "string", "format": "uri", "pattern": "^https?://"},
    "personal_writeup": {"type": "string", "minLength": 1}
  }
}
```
Command: `python -m crew_app run --inputs <file>`; exit code 0 on success, non-zero with a one-line message otherwise.

### 4.2 Team definition (one file, `crew_app/team.yaml` or `.json`; addition)
The team is data, kept apart from the run logic, so one team definition serves any instance of the job.
```json
{
  "type": "object",
  "required": ["inputs", "agents", "tasks"],
  "properties": {
    "inputs": {"type": "array", "items": {"type": "string", "pattern": "^[a-z_][a-z0-9_]*$"}, "minItems": 1},
    "agents": {
      "type": "object", "minProperties": 2,
      "additionalProperties": {
        "type": "object",
        "required": ["role", "goal", "backstory", "tools", "allow_delegation"],
        "properties": {
          "role": {"type": "string", "minLength": 1},
          "goal": {"type": "string", "minLength": 1},
          "backstory": {"type": "string", "minLength": 1},
          "tools": {"type": "array", "items": {"enum": ["read_page", "read_resume", "search_resume", "web_search"]}},
          "allow_delegation": {"type": "boolean"}
        }
      }
    },
    "tasks": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "description", "expected_output", "agent"],
        "properties": {
          "id": {"type": "string", "pattern": "^[a-z_][a-z0-9_]*$"},
          "description": {"type": "string", "minLength": 1},
          "expected_output": {"type": "string", "minLength": 1},
          "agent": {"type": "string"},
          "context": {"type": "array", "items": {"type": "string"}},
          "async_execution": {"type": "boolean", "default": false},
          "output_file": {"type": "string", "pattern": "^[A-Za-z0-9_.-]+\\.md$"}
        }
      }
    }
  }
}
```
Rules the schema cannot hold are in R1–R3 (agent exists, every agent has a task, placeholders declared, context names earlier tasks).

### 4.3 The sample team (C1a)
Placeholders are written `{name}`. Wording below is the required content; exact phrasing is free unless quoted.

| Agent id | Role (exact) | Goal | Backstory | Tools | Delegation |
|---|---|---|---|---|---|
| `researcher` | Tech Job Researcher | Do excellent analysis of job postings to help job applicants. | Unmatched at navigating job postings and extracting the qualifications and skills employers seek; this forms the foundation for tailoring an application. | read_page | allowed |
| `profiler` | Personal Profiler for Engineers | Do excellent research on job applicants to help them stand out in the job market. | Dissects and synthesises information from diverse sources into comprehensive personal and professional profiles, the groundwork for résumé improvements. | read_page, read_resume, search_resume | allowed |
| `resume_strategist` | Resume Strategist for Engineers | Find the best ways to make a résumé stand out in the job market. | Refines résumés to highlight the most relevant skills and experience so they match the job's requirements. | read_page, read_resume, search_resume | allowed |
| `interview_preparer` | Engineering Interview Preparer | Create interview questions and talking points based on the résumé and job requirements. | Anticipates interview dynamics and prepares candidates to address every aspect of the job confidently. | read_page, read_resume, search_resume | allowed |

| Task id | Agent | Description must say | Expected output | Context | Parallel | Output file |
|---|---|---|---|---|---|---|
| `research_task` | researcher | Analyse the posting at `{job_posting_url}`; extract the key skills, experience and qualifications required; use the tools to gather the content and categorise the requirements. | A structured list of job requirements: skills, qualifications, experience. | — | yes | — |
| `profile_task` | profiler | Compile a detailed personal and professional profile from the GitHub page `{github_url}` and the write-up `{personal_writeup}`, using the tools to extract and synthesise. | A profile covering skills, project experience, contributions, interests and communication style. | — | yes | — |
| `resume_strategy_task` | resume_strategist | Using the profile and job requirements from the earlier tasks, tailor the résumé to highlight the most relevant areas; update every section — the opening summary, work experience, skills and education; "don't make up any information". | An updated résumé that highlights the candidate's qualifications and experience relevant to the job. | research_task, profile_task | no | `tailored_resume.md` |
| `interview_preparation_task` | interview_preparer | Create potential interview questions and talking points from the tailored résumé and the job requirements, helping the candidate highlight the résumé's main points and how it matches the posting. | A document of key questions and talking points to prepare for the first interview. | research_task, profile_task, resume_strategy_task | no | `interview_materials.md` |

### 4.4 Tools
- `read_page(url)`: fetches a web page and returns its text. In tests it is backed by the page stand-in (section 8.1).
- `read_resume()`: returns the whole text of the résumé file at the `RESUME_PATH` setting; it can read no other file.
- `search_resume(query)`: semantic search over the résumé, split into sections at `## ` headings; returns the best-matching section(s). It may be the framework's résumé/Markdown search tool or a custom tool built on the framework's custom-tool base class.
- `web_search(query)`: only under C5b.

### 4.5 Model roles
One model per agent role: `researcher`, `profiler`, `resume_strategist`, `interview_preparer` (the course used one model for all four); `resume_search_embedder` (embeddings for `search_resume`). Under C9c add `manager`; under C7b add `qa_reviewer`.

### 4.6 Outputs
- `output/tailored_resume.md`, `output/interview_materials.md`: the raw final answers of their tasks.
- `output/run_log.jsonl` (addition): one JSON object per line, `{"event": "task_started"|"task_finished"|"tool_error"|"run_finished", "task": <id or null>, "t": <seconds since run start, float>, "detail": <string>}`. `task_started` is logged when the task's agent first asks the model.
- The command prints the final task's output and returns it from the run function.

### 4.7 Settings
| Setting | Value | Source | Change this when … |
|---|---|---|---|
| `RESUME_PATH` | `data/resume.md` | Course read a fixed local Markdown résumé (Lesson 16) | your résumé lives elsewhere. |
| `OUTPUT_DIR` | `output/` | Addition | you want results elsewhere. |
| Result file names | `tailored_resume.md`, `interview_materials.md` | Lesson 16 | — (contract). |
| Parallel tasks | `research_task`, `profile_task` | Lesson 16 | — |
| Tool-result caching | on, shared across agents | Lesson 8 (the framework's cross-agent caching) | a tool's answer changes between calls with the same input. |
| Maximum agent steps per task | the framework's current default (the course set none) | Lessons 5, 7: agents always reach an answer | agents stop too early on long tasks. |
| Delegation | allowed on all four agents | Lessons 6, 16 (see D6) | — (that is C6). |
| Memory | off | Lesson 16 crew sets none | — (that is C10). |
| Verbose logging | on (show each agent's reasoning and tool use) | Lesson 16 `verbose` true; Lesson 4 used the highest level | you want quiet runs. Changes only console output, not results. |
| Manager model temperature (C9c only) | 0.7 | Lesson 15 | the chosen manager model rejects a temperature: leave it unset. |

## 5. Business rules

### What must stay true (pattern card, every option keeps these)
1. **The work is split across several specialised agents, and each agent has its own role, goal and backstory.** No single agent does the whole job. → T1, T2, T3
2. **Every piece of work is a task with a clear description and a stated expected output, and each task is assigned to an agent.** → T1, T3
3. **Results move between agents: a task works from the outputs of the tasks it depends on and does not start until they are done. The run finishes when every task is done.** → T6, T7, T8
4. **One team definition serves any instance of the job: each run takes its named inputs and puts them in place wherever the agents and tasks use them.** → T4, T5

### Rules
- **R1.** The team has at least two agents; each has a non-empty role, goal and backstory; each agent is assigned at least one task. (card 1) → T1, T3
- **R2.** Every task has a non-empty description and expected output and names an agent that exists; a task's context names only tasks listed before it. (card 2) → T1, T3
- **R3.** Every `{name}` placeholder in agent or task text is a declared input; a definition breaking R1–R3 is refused on load with a message naming the problem. (card 4; addition) → T3
- **R4.** A run with a declared input missing or empty stops before any model request, with a message naming that input, and writes no result file. (card 4; addition) → T4
- **R5.** Each run puts every input's value into every place its placeholder appears; no placeholder text reaches the model. (card 4) → T5
- **R6.** A task's request to the model includes the outputs of the tasks in its context list (without a context list, the previous task's output), and the task does not start until those tasks have finished. (card 3) → T6, T7, L1
- **R7.** `research_task` and `profile_task` run in parallel; neither waits for the other. (Lesson 16) → T7
- **R8.** The run returns only after every task has finished and every result file is written; it returns the last task's output. (card 3; Lesson 12 notebook warning) → T8, L1
- **R9.** When a tool raises an error, the error text is sent back to the agent as the tool's result and the run continues. (Lessons 8, 9, demonstrated) → T9
- **R10.** An agent's work on one task is bounded by the maximum-steps setting and always ends with an answer, even if the model keeps asking for tools. (Lessons 5, 7, warned) → T10
- **R11.** Tool results are cached across agents: a second call of the same tool with the same input, by any agent, does not repeat the fetch. (Lesson 8) → T11
- **R12.** `read_resume` returns only the file at `RESUME_PATH`; `search_resume` returns the résumé section(s) most similar to the query. (Lesson 16) → T12
- **R13.** The résumé-strategy task's request tells the model not to make up information and to update the summary, work experience, skills and education sections. (Lesson 16) → T13
- **R14.** The sample team matches section 4.3: roles, tools per agent, delegation allowed, the two parallel tasks, the context lists and output file names; memory is off. (Lesson 16) → T2, T14
- **R15.** On a fresh start the run creates `OUTPUT_DIR` and writes both result files and `run_log.jsonl` there; a missing résumé file stops the run before any model request, naming the path. (addition) → T15
- **R16.** Without `OPENAI_API_KEY` the `run` command exits non-zero with a message naming that variable; the scripted stand-in model is used only by tests, never by the `run` command. (addition) → T16

## 6. Tests

### 6.1 Sample data (write these files; facts are fixed)
- `data/resume.md` — sections, in order:
  - `# Mara Lindqvist`
  - `## Summary`: "Engineering manager with 11 years in software. Led a team of 8 engineers across two time zones. Holds an MBA."
  - `## Work experience`: "Northwind Logistics — Engineering Manager, 2019–2024: led the platform team; built the shipment-tracking REST API in Go; migrated the orders database to PostgreSQL." and "Brightleaf Health — Senior Software Engineer, 2014–2019: wrote Python data pipelines; led the on-call rotation."
  - `## Skills`: "Go, Python, PostgreSQL, Kubernetes, team leadership."
  - `## Education`: "BSc Computer Science, Lakeside University, 2013. MBA, 2018."
- `data/sample_inputs.json`: `job_posting_url` = `https://jobs.example/backend-engineer-42`; `github_url` = `https://code.example/mara-lindqvist`; `personal_writeup` = "Mara has 11 years in software and wants to return to hands-on backend work."
- `tests/pages/` — the **page stand-in** (stand-in for live web pages; tests only). A URL→file map:
  - `https://jobs.example/backend-engineer-42` → `job_posting.md`: "Backend Engineer — Example Freight Co. Must have: 5+ years of Go; PostgreSQL; designing REST APIs; on-call experience. Nice to have: Kubernetes."
  - `https://code.example/mara-lindqvist` → `github_profile.md`: "Repositories: route-planner (Go), pg-migrate-kit (PostgreSQL migration helper)."
  - `https://code.example/mara-lindqvist/private` → **planted failure**: raises an error with message "403 Forbidden".
  - The stand-in counts fetches per URL and, when the test sets `PAGE_DELAY=0.5`, waits 0.5 s per fetch.
- **Scripted embedder** (stand-in for the embedding model; tests only): a text's vector is the counts of its lower-cased words (a word is a run of letters and digits); similarity is cosine.
- **Scripted model** (stand-in for the chat model; tests only). It records every request (role, task, full text, time). Per role, it answers by the first matching line below; a "tool call" reply is expressed in whatever form the framework expects for a tool request.

| Role | When the request … | Reply |
|---|---|---|
| researcher | has no tool result yet | call `read_page` with `https://jobs.example/backend-engineer-42` |
| researcher | contains "Backend Engineer" (case-sensitive) | final answer: `[R-OUT] Requirements: Go (5+ years); PostgreSQL; REST API design; on-call. Nice to have: Kubernetes.` |
| profiler | has no tool result yet | call `read_page` with `https://code.example/mara-lindqvist/private` |
| profiler | contains "403" but not "route-planner" | call `read_page` with `https://code.example/mara-lindqvist` |
| profiler | contains "route-planner" but not "Northwind" | call `read_resume` |
| profiler | contains "Northwind" | final answer: `[P-OUT] Profile: Go, Python, PostgreSQL; repos route-planner and pg-migrate-kit; wants hands-on backend work.` |
| resume_strategist | lacks `[R-OUT]` or `[P-OUT]` | final answer: `MISSING CONTEXT` |
| resume_strategist | has both, no tool result yet | call `search_resume` with `PostgreSQL REST API` |
| resume_strategist | has both and a tool result | final answer: `[S-OUT]` then `# Mara Lindqvist`, `## Summary` "Backend engineer with 11 years in software, building REST APIs in Go on PostgreSQL.", `## Work experience` (the same two jobs, each led by its Go/PostgreSQL/Python work), `## Skills` "Go, PostgreSQL, REST APIs, Python, Kubernetes.", `## Education` (unchanged) |
| interview_preparer | lacks any of `[R-OUT]`, `[P-OUT]`, `[S-OUT]` | final answer: `MISSING CONTEXT` |
| interview_preparer | has all three, no tool result yet | call `read_page` with `https://jobs.example/backend-engineer-42` |
| interview_preparer | has all three and a tool result | final answer: `[I-OUT]` then "Q1: How did you design the shipment-tracking REST API in Go? Talking point: ..." and Q2 (PostgreSQL migration), Q3 (on-call) in the same shape |

A **looping variant** (T10 only): the researcher always replies with a call to `read_page` on the job URL.

### 6.2 Test table
Offline tests use the scripted model, scripted embedder and page stand-in, with every default in §4.7 in force.

| Test | Given | When | Then | Rules |
|---|---|---|---|---|
| T1 | The sample team definition | it is loaded | 4 agents with the exact roles of §4.3, each with non-empty goal and backstory; 4 tasks, each with non-empty description and expected output and an existing agent; every agent has a task | R1, R2 |
| T2 | The sample team, built into a crew | its configuration is inspected | researcher's tools = {read_page}; the other three = {read_page, read_resume, search_resume}; all four allow delegation; `research_task` and `profile_task` parallel; `resume_strategy_task` context = [research_task, profile_task]; `interview_preparation_task` context = [research_task, profile_task, resume_strategy_task]; output files as §4.3 | R14 |
| T3 | Four broken copies of the definition: (a) one task's expected output empty; (b) only one agent; (c) a task description using `{company}` not in inputs; (d) `resume_strategy_task` context naming `interview_preparation_task` | each is loaded | each is refused; the message names respectively the task id, "at least two agents", `company`, and `interview_preparation_task` | R1, R2, R3 |
| T4 | `sample_inputs.json` without `github_url` | `run` | non-zero exit; message contains `github_url`; scripted model received 0 requests; no result file written | R4 |
| T5 | Sample inputs | a full run | the researcher's first request contains `https://jobs.example/backend-engineer-42`; the profiler's first request contains `https://code.example/mara-lindqvist` and "hands-on backend work"; no recorded request contains `{job_posting_url}`, `{github_url}` or `{personal_writeup}` | R5 |
| T6 | Sample inputs | a full run | `output/tailored_resume.md` starts with `[S-OUT]` and contains `## Summary`, `## Work experience`, `## Skills`, `## Education`; `output/interview_materials.md` starts with `[I-OUT]`; neither file contains `MISSING CONTEXT` | R6 |
| T7 | Sample inputs, `PAGE_DELAY=0.5` | a full run, reading `run_log.jsonl` | `research_task` started before `profile_task` finished and `profile_task` started before `research_task` finished; `resume_strategy_task` started after both finished; `interview_preparation_task` started after `resume_strategy_task` finished | R6, R7 |
| T8 | Sample inputs | the run function returns | at that moment both result files exist and are non-empty; the returned value starts with `[I-OUT]`; the last log line is `run_finished` | R8 |
| T9 | Sample inputs (the profiler's first page is the planted 403) | a full run | the run completes; `run_log.jsonl` has a `tool_error` for `profile_task` mentioning "403"; the profiler's second request contains "403"; T6's outcomes hold | R9 |
| T10 | Looping variant | a full run | `research_task` ends with some output and the run reaches `run_finished`; the scripted model received at most (maximum steps + 1) requests for `research_task` | R10 |
| T11 | Sample inputs | a full run | the page stand-in's fetch count for `https://jobs.example/backend-engineer-42` is 1, though both the researcher and the interview preparer called `read_page` on it | R11 |
| T12 | `data/resume.md`, scripted embedder | `read_resume` is called (with any argument, e.g. `/etc/hosts`); `search_resume("PostgreSQL database")` is called | `read_resume` returns text containing "Northwind Logistics" and nothing from any other file; the top `search_resume` result contains "PostgreSQL" | R12 |
| T13 | Sample inputs | a full run | the resume strategist's first request contains "make up" (case-insensitive) and the words "summary", "work experience", "skills", "education" | R13 |
| T14 | The sample crew | its configuration is inspected | memory is off | R14 |
| T15 | (a) No `output/` folder; (b) `RESUME_PATH` pointing to a missing file | `run` with sample inputs | (a) `output/` exists afterwards with `tailored_resume.md`, `interview_materials.md`, `run_log.jsonl`; (b) non-zero exit, message names the missing path, scripted model received 0 requests | R15 |
| T16 | `OPENAI_API_KEY` unset | `python -m crew_app run --inputs data/sample_inputs.json` | non-zero exit; message contains `OPENAI_API_KEY`; no scripted model is used | R16 |
| L1 (`live`) | `OPENAI_API_KEY` set; page stand-in for fetching; real model and embedder | a full run on sample inputs | both result files non-empty; the tailored résumé contains "Mara Lindqvist", "Go" and "PostgreSQL"; the interview materials contain at least 3 "?" | R6, R8 |

## 7. Standing permissions
- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has data; anything that sends data to a third party.
- **Never:** invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets.

## 8. Test plan
- Install: `python -m pip install -r requirements.txt` (current crewAI, its tools package, pytest, and any library a chosen option needs).
- Offline: `pytest -m "not live"` — must pass.
- Live: `OPENAI_API_KEY=... pytest -m live` — runs only when the key is set; skipped otherwise.
- Real run: `python -m crew_app run --inputs my_inputs.json`.
- Adjust the table for the chosen options: drop T2/T11/T12 parts for tools an option removes, replace sample data and T1–T16 outcomes for C1b, and add one test per chosen option from its "what to check" sentence, copied into `resolved-decisions.md`.
- Report a result per test with evidence (test output, file paths). "Should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.
- Finish with a diagram of the built app introduced by the sentence "This is the infra/structure diagram of this app".

## 9. Background notes (for the build agent)

### The program
1. **Take the inputs** — the named values for this instance of the job; checked before anything runs, so the same team works for any posting or person.
2. **Assemble the team** — agents with role, goal and backstory (agents do better when role-playing and focused on one job) and a small, chosen set of tools each.
3. **Define the tasks** — each with a description and an expected output (the expected output forces you to say what you want back), an assigned agent, the tasks it depends on, and where its result goes.
4. **Run in dependency order** — independent tasks in parallel to save time; a dependent task waits.
5. **Agent work** — each agent reasons on its own and uses its tools; tool errors go back to the agent; the work is bounded.
6. **Hand off results** — each task's output becomes context for the tasks that depend on it.
7. **Return the finished results** — each result written to its file; the run ends when every task is done.

Logs of what ran (verbose output, `run_log.jsonl`) show the run; they are not a stage.

### Failures
- **Tool error stops nothing (demonstrated, Lesson 9).** Seen: an agent used a file-reading tool on a web address; the tool failed. Why: the model passes fuzzy inputs to tools that expect exact ones. The course's framework sends the error back to the agent, which then tried another way; stopping the run would lose all work so far. Prevented by R9; planted as the 403 page; tested by T9.
- **Agents looping on tools (warned, Lessons 5 and 7).** Agents, especially on open-source models, could get stuck calling the same tool over and over or take too long. Prevented by R10 (bounded steps, always an answer) and R11 (repeat calls hit the cache); tested by T10, T11.
- **Result file not ready when the run seems done (warned, Lesson 12 notebook).** The course told learners to wait about 45 seconds after the run before a parallel task's file appeared. Prevented by R8; tested by T8.
- **Made-up facts in the tailored résumé (warned, Lessons 5 and 16).** Mixing in too much can lead to hallucination; the course's résumé task says not to make up information. R13, T13 (the live test L1 checks the real résumé keeps the candidate's own name and skills).
- **Context fading along a long chain (stated cost, Lesson 14).** In a strictly sequential run the initial context fades as tasks pass along; carried as C9b's cost, not a failure.

### Why the questions and settings are what they are
- **C1:** the course built six crews (article writing, customer support, sales outreach, event planning, financial analysis, job application) on the same pattern, and invited learners to bring their own topic, stocks and inputs. The final, most complete crew (Lesson 16) is the recommended build.
- **C2:** the course's résumé was Markdown; its tool list includes search tools for PDF and Word files, so other formats are named paths.
- **C3:** the course used OpenAI; its first notebook lists Hugging Face, Mistral and Cohere, and Lesson 3 names Ollama for local models; Lesson 5 warns smaller models handle many tools poorly.
- **C4:** the course ran notebooks; Lesson 17 shows turning crews into APIs, and Lesson 12 mentions starting crews from an API as one way to integrate them.
- **C5:** web search (Serper) appears in Lessons 6, 9, 12, 15, 16; it needs its own key.
- **C6:** Lesson 6 contrasts an agent not allowed to delegate with a QA agent that may; Lesson 14 says agents can delegate and ask each other whatever the process. The final crew left delegation at the then-default "allowed".
- **C7:** pattern card, "Offered from other lessons"; Lesson 6 recommends a final QA agent.
- **C8:** Lesson 12 used human input on two tasks; the final crew used none.
- **C9:** Lesson 4 ran sequentially (default), Lessons 12 and 16 ran independent tasks in parallel with dependent tasks waiting, Lesson 15 ran a manager (hierarchical). The final crew decides the recommended option.
- **C10:** pattern card, "Offered from other lessons"; Lessons 5, 6, 9 explain and enable the three memory types; the final crew does not.
- **C11:** Lesson 12 converted a task's answer into a typed structure and wrote it as JSON, for use by other code.
- **Not questions:** a different model per agent (Lesson 3) — set per role on the gate's model lines; caching off — the course argues only for caching; stopping the run on a tool error — the course tells you not to let exceptions stop the crew; per-task callbacks (Lesson 11 slide only) — the course never uses one and it changes no result; giving tools at task level instead of agent level (Lesson 6) — a wiring detail with no learner situation in this program; directory-reading, website-RAG and custom tools (Lessons 6, 9) — not part of this program's crew, available to a C1b team; LangChain tools (Lessons 8, 10) — a tool source, no situation; the hosted deployment platform (Lesson 17) — a hand-picked beta; C4b covers the need; running as a notebook — how the course is taught; which model the tests use — never asked (tests use stand-ins).
- **Picked values (4.2):** model — Lesson 16 video "GPT-4 turbo", notebook `gpt-3.5-turbo` (platform constraint, per the notebook's own note); rule 1 (instructor's statement) picks GPT-4 turbo as the course fact; the gate names a current model. Verbose — Lesson 4 used level 2, Lesson 16 used true; rule 2 (final app) picks true. Manager temperature 0.7 — Lesson 15 notebook only. Résumé file `./fake_resume.md`, result files `tailored_resume.md` and `interview_materials.md` — Lesson 16 notebook.
- **Course code that looks off:** the course's task prompts carry typos ("inlcuding", "reflrect", "candiadte"); the spec gives their meaning, not their spelling. The Lesson 16 notebook's heading says "your first multi-agent system" though it is the last crew; harmless.

### Names that go stale
Use these as search keywords against current docs, not as guaranteed imports: `crewai==0.28.8`, `crewai_tools==0.1.6`, `langchain_community==0.0.29`, `langchain_openai.ChatOpenAI`; classes `Agent`, `Task`, `Crew`, `Process` (`Process.hierarchical`), `BaseTool` (imported then from `crewai_tools`, with a `_run` method); tools `SerperDevTool`, `ScrapeWebsiteTool`, `FileReadTool`, `MDXSearchTool`, `DirectoryReadTool`, `WebsiteSearchTool`; attributes `role`, `goal`, `backstory`, `allow_delegation`, `verbose` (then an integer 1–2 or boolean), `tools`, `expected_output`, `context`, `async_execution`, `human_input`, `output_file`, `output_json`, `output_pydantic`, `memory`, `manager_llm`, `kickoff(inputs=...)`; env var `OPENAI_MODEL_NAME`; models `gpt-3.5-turbo`, `gpt-4-turbo`, Llama 3 70B, GPT-4. Some current model families reject a `temperature` parameter: leave it unset for them.

### Course names
| Course name | Spec term |
|---|---|
| crew | the team / the program run |
| `research_task`, `profile_task`, `resume_strategy_task`, `interview_preparation_task` | same ids (binding) |
| `researcher`, `profiler`, `resume_strategist`, `interview_preparer` | same agent ids (binding) |
| `job_posting_url`, `github_url`, `personal_writeup` | same input names (binding) |
| `fake_resume.md` | `data/resume.md` (`RESUME_PATH`) |
| `tailored_resume.md`, `interview_materials.md` | same (binding) |
| `scrape_tool`, `read_resume`, `semantic_search_resume`, `search_tool` | `read_page`, `read_resume`, `search_resume`, `web_search` |
| kickoff inputs / interpolation | inputs put into placeholders |

### Lesson map (transcript numbering)
1 Introduction — roles, building blocks. 2 Overview — the job-application crew's goal, agents and tools; fuzzy inputs and outputs. 3 AI Agents — agents, tools, one model per agent, Ollama. 4 Research and write an article — Agent/Task/Crew, role/goal/backstory, description/expected output, sequential order, inputs into placeholders. 5 Key elements of AI agents — role-play, focus, tools, cooperation, guardrails, memory types. 6 Customer support — delegation, QA agent, tools per task, memory on. 7 Mental framework — think like a manager hiring a team. 8 Key elements of agent tools — versatile, fault-tolerant, caching. 9 Customer outreach — custom tool, tool error handled. 10 Recap of tools. 11 Well-defined tasks — mandatory description and expected output; task options. 12 Event planning — structured JSON output, output files, human input, parallel tasks, late-file note. 13 Recap on tasks. 14 Multi agent collaboration — processes, context fade, manager. 15 Financial analysis — hierarchical run, manager model. 16 Job applications — the recommended build. 17 Next steps — docs, deployment platform. 18 Conclusion.
Notebooks were matched to lessons 4, 6, 9, 12, 15, 16 by the notebook map. Slide descriptions for all lessons were read; narrated slides counted as their lesson's transcript, deck-only slides (e.g. 2.18, 16.2) counted less. Nothing in this spec requires access to the course.

---
*spec-v2-draft · course: Multi AI Agent Systems with crewAI · project: multi-agent crew (job-application default) · when the build agent does something unexpected, add the missing constraint here and re-run.*
