# Spec: a team of AI agents that works through one job (crew runner)

**What you're building:** A program that takes a few named inputs for one job, runs a team of specialised AI agents through a set of defined tasks, passes each task's result to the tasks that depend on it, and writes the finished results. By default it does the course's example job, tailoring a résumé to a job posting. You give it a job-posting link, a code-profile link and a short write-up about yourself. You then see two agents study the posting and your profile at the same time, a third rewrite your résumé for that job, and a fourth write interview questions and talking points. The two documents are saved as files.

**What the recommended build needs to run:** an OpenAI API key (`OPENAI_API_KEY`, paid account) for the agents and the résumé search; network access to fetch the pages you give it and to reach the model provider; no other account and no download beyond the Python packages.

**Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once `OPENAI_API_KEY` is set and are skipped until then; that is not a failure.

This file is self-contained: everything the build needs is here.

*Provenance: generated from the course "Multi AI Agent Systems with crewAI" (its notebooks, lesson transcripts, slide descriptions and the owner-confirmed pattern card), 2026-10-28, guide v2.8 (2026-10-27).*

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
   an OpenAI API key (`OPENAI_API_KEY`) and network access), or **choose** question by
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

Context questions first (C1–C5), then the program's stages in order (C6–C14). Model roles for the checklist's model lines are in section 5.1.

### C1. What job should the crew do?
- **C1a (Recommended - course default): Tailor a résumé to one job posting.** Four agents: a job researcher reads the posting, a profiler studies the person's code profile, write-up and résumé, a résumé strategist rewrites the résumé for the job, and an interview preparer writes questions and talking points. *Pick this when* you want the course's example working on your own résumé, or want to see the pattern run before adapting it. *Setup:* nothing beyond the recommended build.
- **C1b: Your own job.** You and the build agent write a team definition (section 5, contract A) for your job: its named inputs, at least two agents (role, goal, backstory, tools), its tasks (description, expected output, agent, which tasks it waits for, which run side by side) and which results are saved to files. Tools your job needs that this spec does not define (for example reading your customer records) are written to the tool contract (section 5, contract D). *Pick this when* your project is a different multi-step job, for example "research a sales lead, then draft a personalised outreach email" or "find a venue, then plan catering and promotion side by side". *Setup:* writing the definition and any custom tools; keys for any outside service a custom tool calls.
  - *What to check:* your definition passes validation, a run with your inputs puts every input in place in the prompts, each task starts only after the tasks it depends on are done, and each named result file is written with that task's result.

### C2. What format is the résumé in?
*Ask only when C1 is C1a.*
- **C2a (Recommended - course default): Markdown or plain text.** *Pick this when* your résumé is, or can be saved as, a text or Markdown file. *Setup:* none.
- **C2b: PDF or Word file, turned into text when loaded.** *Pick this when* your résumé exists only as a PDF or Word document and you do not want to keep a text copy by hand. *Setup:* one text-extraction package per format; some layout (columns, tables) may come out in a different order.
  - *What to check:* loading the PDF or Word résumé gives text containing every section heading and bullet of the original, and the résumé tools read and search that text.

### C3. Which model provider runs the agents?
- **C3a (Recommended - course default): OpenAI hosted models.** *Pick this when* you have, or can get, an OpenAI key. *Setup:* `OPENAI_API_KEY`, paid account.
- **C3b: Another hosted provider** (for example Mistral, Cohere or Hugging Face). *Pick this when* you already pay for one of these or your organisation requires it. *Setup:* that provider's key; if it has no embedding model, C7 must be C7b.
  - *What to check:* every model role in the checklist runs on that provider, a live run completes, and no request goes to OpenAI.
- **C3c: A model on your own machine, through a local model server** (for example Ollama). *Pick this when* your résumé and other data must not leave your machine, or you have no paid key. *Setup:* installing the server and downloading a model (often several GB — an estimate added by this spec), and a machine that can run it. Cost: smaller models cope worse with many tools and may repeat the same tool call; keep each agent's tool set small.
  - *What to check:* a full run completes with every model role pointing at the local server and no request sent to a hosted model provider.

### C4. What is the orchestration built on?
- **C4a (Recommended - course default): crewAI, current release.** *Pick this when* you want the framework this pattern was taught with; delegation, tool-result caching and returning tool errors to the agent come with it. *Setup:* Python packages only.
- **C4b: Your own small orchestrator in plain Python.** *Pick this when* you want to see and control every step, or cannot add an agent framework to your project. Cost: much more code — you write the agent loop, delegation, caching, error return and parallel runs yourself.
  - *What to check:* all offline tests in section 8 pass with no agent framework installed.
- **C4c: Another agent framework you already use.** *Pick this when* your codebase already depends on one and you do not want a second. Cost: you map each rule in section 7 to that framework's features or write the missing parts.
  - *What to check:* all offline tests in section 8 pass, and the build report names, for each item in section 7.1, the framework feature or code that keeps it.

### C5. How does a run get started?
- **C5a (Recommended): From the command line.** One command takes a team definition and an inputs file and prints where the results were written. *Pick this when* you start runs yourself. *Setup:* none.
- **C5b: A small local web service.** Another program sends the inputs as JSON and gets the results back. *Pick this when* another program (a job-tracker app, a form) must start runs. *Setup:* a web framework package. Cost: a run takes minutes, so the caller must wait or check back.
  - *What to check:* sending the sample inputs returns the same task results the command line writes, and a request missing an input gets an error naming that input.

### C6. Should agents be able to search the web?
- **C6a (Recommended): No web search.** Agents fetch the pages they are given and read the résumé. *Pick this when* your inputs already point at what matters (a posting link, a profile link). *Setup:* none.
- **C6b (course default): Add a web-search tool** (a search-API service; the course used Serper, which gives free credits on sign-up) to every agent that has the page-fetch tool. *Pick this when* agents need facts that are not in the pages you give them, for example the hiring company's recent news. *Setup:* a search-API account and key (`SERPER_API_KEY`).
  - *What to check:* a search request returns result titles and links as text, and the same search made twice in one run, by any agent, reaches the search service once.

### C7. How should agents search the résumé?
*Ask only when C1 is C1a.*
- **C7a (Recommended - course default): Search by meaning.** Résumé passages are ranked by meaning, using an embedding model from your provider. *Pick this when* the résumé and the posting use different words for the same thing. *Setup:* none beyond the provider key; each search makes a small embedding call.
- **C7b: Search by shared words** (a stand-in for search by meaning: standard library only, no model calls). *Pick this when* your provider has no embedding model, or you want no extra model calls. Cost: misses passages that say the same thing in other words.
  - *What to check:* a query returns at most 3 passages, each sharing at least one word with the query, those sharing the most words first.

### C8. Who decides the order of work?
- **C8a (Recommended - course default): A fixed plan.** Tasks run in the listed order; each waits for the tasks it depends on. *Pick this when* the steps of your job are known in advance.
- **C8b: A manager agent.** An extra agent keeps the job's goal in view, hands each task to its assigned agent, passes on what earlier agents found, reviews each result and may ask for improvements. *Pick this when* your job is a long chain where the original request gets lost by the later steps, or you want one coordinator to review every step. Cost: extra model calls for the manager (an extra model role), slower runs, a less predictable log.
  - *What to check:* the run record shows the manager handing every task to its assigned agent, no task starting before the tasks it depends on are done, and the run ending only when every task is done.

### C9. Should independent tasks run at the same time?
- **C9a (Recommended - course default): Yes.** Tasks marked parallel start together (in the résumé crew, the posting research and the profile research). *Pick this when* your provider accepts several requests at once; runs finish sooner.
- **C9b: No, one task at a time in list order.** A task with no declared dependencies receives the previous task's result. *Pick this when* your model server handles one request at a time (common for a local server) or you want a log that reads in order. Cost: slower runs.
  - *What to check:* no two tasks overlap in time in the run record, and every task still receives the results it depends on.

### C10. May agents hand work to each other?
- **C10a (Recommended - course default): Yes.** Any agent may ask a coworker a question or hand it a piece of work; the agent decides when. *Pick this when* tasks gain from a second opinion from a better-suited agent.
- **C10b: No.** Each agent works only on its own tasks. *Pick this when* you want a fixed number of model calls per task and a log that matches the task plan exactly, since whether an agent delegates is decided by the model, not by you.
  - *What to check:* no delegation appears in the run record, and a delegation request is answered with a tool-error message.

### C11. Add a reviewer agent at the end?
- **C11a (Recommended - course default): No reviewer.**
- **C11b: A quality-assurance reviewer.** One more agent and task run last. The reviewer checks the final result (the tailored résumé, or your job's last result) against the inputs and earlier results, may send work back to the agent that produced it, and writes the reviewed version; the unreviewed version is kept as a draft file. *Pick this when* the result goes to someone else, such as an employer or a customer, and must be fact-checked before it goes out. Cost: one more agent and task, more model calls.
  - *What to check:* the review task starts only after the tasks it reviews are done, it may delegate back, and every fact in the reviewed version appears in the inputs, the résumé or an earlier task's result.

### C12. Should the agents remember things?
- **C12a (Recommended - course default): No memory** beyond the task results passed along.
- **C12b: Memory within one run only.** Agents share what they learn during the run (short-term memory) and keep notes on the people, organisations and places it mentions (entity memory); nothing is kept after the run. *Pick this when* agents need facts other agents found that are not in their direct inputs, and nothing may be stored afterwards (a résumé is personal data).
  - *What to check:* an agent can recall a fact found by another agent earlier in the same run, and no memory file remains after the run.
- **C12c: Memory within and across runs** (short-term, entity and long-term memory together). After each task the agent critiques its own work and stores what to do better, in a local database read by later runs. *Pick this when* you run the crew again and again on similar jobs and want it to improve with use. Cost: a database on disk that holds personal data between runs, and extra model calls for the self-critique.
  - *What to check:* a second run receives a lesson stored by the first run, and the memory store is a file on disk.

### C13. Should a run pause for your feedback?
- **C13a (Recommended - course default): No pauses.**
- **C13b: Pause after the tasks you name** (résumé crew: after the résumé rewrite). The run shows the draft result and asks you to approve or give feedback; feedback goes back to the agent before the task finishes. *Pick this when* you want to steer the rewritten résumé before the interview materials are built on it. Cost: the run waits for you and cannot run unattended.
  - *What to check:* the run stops at that task and shows the draft, and the task's final result is produced after, and responds to, the feedback typed.

### C14. Do you need machine-readable results?
- **C14a (Recommended - course default): Text results**, saved as Markdown files.
- **C14b: Also a JSON file** for the job-requirements task (or the tasks you name), with fixed fields checked against a schema (résumé crew: `skills`, `qualifications`, `experience`, each a list of strings). *Pick this when* another program, such as a job tracker, reads the results.
  - *What to check:* the JSON file validates against its schema and lists the same requirements as the task's text result.

## 2. Departures from the course

| # | The course | This build | Why |
|---|---|---|---|
| D1 | Every agent with page tools also had a web-search tool (a search-API service needing its own key). | Left out of the recommended build; offered as C6b. | It needs a key the model does not; the page-fetch tool already exercises "agents gather information with tools". |
| D2 | Pinned `crewai==0.28.8`, `crewai_tools==0.1.6`, `langchain_community==0.0.29`. | Current releases. | Course-era versions often no longer install or work with current models. |
| D3 | Model `gpt-3.5-turbo` in the notebooks; GPT-4 / GPT-4 turbo in the videos. | The build agent picks a current model from the chosen provider at the checklist. | Model names go stale. |
| D4 | Ran as notebook cells. | A command-line program (C5). | The build is a program, never a notebook. |
| D5 | Agents and tasks written as code in the notebook. | The team is a JSON definition file checked against a schema (addition). | Lets one program serve the course's job and the learner's own job (C1b), and makes validation testable. |
| D6 | The course's own résumé, posting and profile. | Sample data written for this spec (section 8.1). | No course data is copied. |
| D7 | Agent and task wording as course prompt strings. | Same meaning, paraphrased; spelling slips not carried. | No copied code. |
| D8 | Results written to the working folder. | Written to an output folder, plus a run record file (additions). | Tests need a known place and an inspectable record. |
| D9 | No stated limit on agent steps or on résumé-search results; the framework's own guardrails. | Step limit 15 per task; résumé search returns 3 passages (additions). | Needed so behaviour is testable and the same across frameworks. |
| D10 | The résumé-search tool's embedding model is not stated. | Uses the chosen provider's embedding model (addition, an assumption). | The course does not say. |
| D11 | Not stated. | Offline tests use a scripted stand-in model, a stand-in page fetcher and the shared-words résumé search. | Tests must run offline. |

## 3. Objective

Given a team definition and a set of named inputs, run the team's agents through the defined tasks in dependency order, passing each task's result to the tasks that depend on it, and save the finished results.

## 4. Tech stack, versions, secrets

- **Language:** Python, current release. Package name `crew_runner` (importable).
- **Orchestration:** per C4 (recommended: crewAI, current release). The course pinned crewAI 0.28.8; that pin is not used (D2).
- **Tests:** `pytest`; offline tests are the default, `live` tests carry a `live` marker.
- **Schema checks:** a JSON Schema validator package, or equivalent hand-written checks that give the same refusals.
- **Secrets:** read only from environment variables: `OPENAI_API_KEY` (C3a), the chosen provider's key (C3b), `SERPER_API_KEY` (C6b). Never written to files, logs, prompts or the run record. A `.env` file may be loaded if present and must be git-ignored.
- **Model selection:** `--model scripted` selects the scripted stand-in model (tests and demos only; labelled a stand-in in every output it produces). Otherwise the real provider is used, and a missing key stops the run (R14). There is never a silent fallback to the stand-in.
- **Page source:** `--pages live` (default) fetches over the network; `--pages sample` uses the stand-in page fetcher serving the sample pages (section 8.1).

## 5. Contracts

### Contract A — Team definition (JSON file)

```json
{
  "type": "object",
  "required": ["name", "agents", "tasks"],
  "properties": {
    "name": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"},
    "agents": {
      "type": "array", "minItems": 2,
      "items": {
        "type": "object",
        "required": ["role", "goal", "backstory", "tools"],
        "properties": {
          "role": {"type": "string", "minLength": 1},
          "goal": {"type": "string", "minLength": 1},
          "backstory": {"type": "string", "minLength": 1},
          "tools": {"type": "array", "items": {"enum": ["fetch_page", "read_resume", "search_resume", "web_search"]}, "uniqueItems": true},
          "allow_delegation": {"type": "boolean", "default": true}
        }
      }
    },
    "tasks": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "description", "expected_output", "agent"],
        "properties": {
          "name": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"},
          "description": {"type": "string", "minLength": 1},
          "expected_output": {"type": "string", "minLength": 1},
          "agent": {"type": "string", "description": "must equal the role of an agent in this definition"},
          "context": {"type": "array", "items": {"type": "string"}, "description": "names of EARLIER tasks whose results this task needs"},
          "parallel": {"type": "boolean", "default": false},
          "tools": {"type": "array", "items": {"enum": ["fetch_page", "read_resume", "search_resume", "web_search"]}, "description": "if present, replaces the agent's tools for this task"},
          "output_file": {"type": "string", "pattern": "^[A-Za-z0-9_][A-Za-z0-9_.-]*\\.(md|txt|json)$"}
        }
      }
    }
  }
}
```

Checks beyond the schema (each refused, R1): agent roles unique; task names unique; every `agent` names a defined role; every `context` entry names an earlier task; every tool name is known; at least two different agents are assigned tasks; `web_search` only when C6b. Placeholders are `{name}` with `name` matching `^[a-z][a-z0-9_]*$`, allowed in role, goal, backstory, description and expected output. The run's required inputs are exactly the placeholder names used anywhere in the definition.

C1b adds tool names for custom tools to the enum; C11b adds the reviewer agent and task.

### Contract B — Inputs (JSON file)

An object whose keys match `^[a-z][a-z0-9_]*$` and whose values are strings, numbers or booleans. Each value is placed into placeholders as its text form. Keys not used by any placeholder are accepted and ignored.

### Contract C — Run result and run record

The run returns, and the command line prints, an object:
`{"status": "completed", "results": {<task name>: <result text>}, "files": {<task name>: <path>}, "record": <path>}`.

The run record, `<output dir>/run_record.json`:

```json
{
  "type": "object",
  "required": ["crew", "inputs", "model", "tasks", "status"],
  "properties": {
    "crew": {"type": "string"},
    "inputs": {"type": "object"},
    "model": {"type": "string", "description": "model name, or 'scripted (stand-in)'"},
    "status": {"enum": ["completed", "refused"]},
    "tasks": {"type": "array", "items": {
      "type": "object",
      "required": ["name", "agent", "started_at", "ended_at", "available_tools", "may_delegate", "tool_calls", "delegations", "result"],
      "properties": {
        "name": {"type": "string"}, "agent": {"type": "string"},
        "started_at": {"type": "number", "description": "seconds, monotonic clock"},
        "ended_at": {"type": "number"},
        "available_tools": {"type": "array", "items": {"type": "string"}},
        "may_delegate": {"type": "boolean"},
        "tool_calls": {"type": "array", "items": {"type": "object",
          "required": ["tool", "argument", "cached", "error"],
          "properties": {"tool": {"type": "string"}, "argument": {"type": "string"},
                         "cached": {"type": "boolean"}, "error": {"type": "boolean"},
                         "message": {"type": "string"}}}},
        "delegations": {"type": "array", "items": {"type": "object",
          "required": ["kind", "to", "request", "answer"],
          "properties": {"kind": {"enum": ["ask_question", "delegate_work"]}, "to": {"type": "string"},
                         "request": {"type": "string"}, "answer": {"type": "string"}}}},
        "result": {"type": "string"}
      }}}
  }
}
```

Delegation requests appear under `delegations`, not `tool_calls`, but count toward the step limit (R10). Delegation actions are never listed in `available_tools`; `may_delegate` shows them. Names a framework uses internally may differ; the record uses these names.

### Contract D — Tools

Every tool has a name, a one-line description shown to the agent, and one text argument (may be empty); it returns text. Any failure returns text starting `Tool error:` to the agent (R7).

| Tool | Argument | Returns |
|---|---|---|
| `fetch_page` | a URL | the page's readable text (markup removed). Stand-in: the text of the sample file mapped to that URL, or `Tool error: page not found: <url>`. |
| `read_resume` | empty, or a path | the whole résumé file. A path other than the configured résumé file returns `Tool error: read_resume only reads <configured path>; it cannot read <path>`. |
| `search_resume` | a query | up to 3 passages, one per line, numbered `1.`, `2.`, `3.`, best first (R16). |
| `web_search` (C6b only) | a query | result titles and links as text. |
| `ask_question` / `delegate_work` (when the agent may delegate) | coworker role and request | the coworker's answer. Unknown role, or the agent's own role: `Tool error: no coworker with role <role>`. |

Résumé passages: every non-empty line of the résumé file that does not start with `#`, with a leading `- ` removed.

### 5.1 Model roles

| Role | Used by | Course model (fact) |
|---|---|---|
| Agent model | every agent in the team (one model for all unless setting S1 is changed) | `gpt-3.5-turbo` (notebooks); GPT-4 turbo (videos) |
| Embedder | `search_resume` under C7a (live only) | not stated |
| Manager model | C8b only | `gpt-3.5-turbo`, temperature 0.7 |

### 5.2 Settings

| Id | Setting | Value | Source | Change this when … |
|---|---|---|---|---|
| S1 | Model per agent | one agent model for all agents | course ran all agents on one model; it also said agents can run on different models | a role needs a larger context window (the course moved to a larger model when agents handled "more data"), or a simpler role can use a cheaper model |
| S2 | Temperature | not set (provider default) | course set none for agents; 0.7 for the manager (C8b) | answers vary more than you want |
| S3 | Console progress log | on | final course crew logged every step; earlier crews used the most detailed level | runs are unattended |
| S4 | Step limit per task | 15 tool and delegation requests | addition | a task legitimately needs more tool calls |
| S5 | Résumé file | `sample_data/resume.md` | course read one Markdown résumé file through a tool fixed to that file | always: point it at your own résumé |
| S6 | Résumé search results | 3 passages | addition | your résumé is long and answers need more passages |
| S7 | Output folder | `output/` | addition (course wrote to the working folder) | you keep runs apart, e.g. one folder per posting |
| S8 | Tool-result cache | on, one cache per run, shared by all agents; errors not cached | course (shared cache across agents) | never needed for this program (see 9.3) |
| S9 | Hosts `fetch_page` may fetch | any | final course crew's page tool was unrestricted; the course also showed fixing a page tool to one address | you want agents to fetch only the links you gave them |
| S10 | Stand-in reply delay per role | 0 seconds | test-only addition | tests need tasks of different lengths |

## 6. The recommended team (contract A instance: `crews/job_application.json`)

Agents (all `allow_delegation: true`):

| Role (binding) | Goal | Backstory | Tools |
|---|---|---|---|
| Tech Job Researcher | Analyse job postings thoroughly so applicants know what the employer needs. | You are unmatched at pulling the critical information out of job postings: you pinpoint the qualifications and skills employers want, which forms the foundation for tailoring an application. | `fetch_page` |
| Personal Profiler for Engineers | Research job applicants in depth to help them stand out in the job market. | You dissect and combine information from many sources into complete personal and professional profiles that ground résumé improvements. | `fetch_page`, `read_resume`, `search_resume` |
| Resume Strategist for Engineers | Find the best ways to make a résumé stand out for a job. | You refine résumés to bring forward the most relevant skills and experience so they match the job's requirements. | `fetch_page`, `read_resume`, `search_resume` |
| Engineering Interview Preparer | Create interview questions and talking points from the résumé and the job requirements. | You anticipate how interviews go and prepare candidates with key questions and talking points so they can confidently address every aspect of the job. | `fetch_page`, `read_resume`, `search_resume` |

Tasks:

| Name | Agent | Description | Expected output | Context | Parallel | Output file |
|---|---|---|---|---|---|---|
| `research` | Tech Job Researcher | Analyse the job posting at {job_posting_url} to extract the key skills, experience and qualifications it requires. Use your tools to gather the content, then identify and categorise the requirements. | A structured list of job requirements: skills, qualifications and experience. | — | yes | — |
| `profile` | Personal Profiler for Engineers | Compile a detailed personal and professional profile from the code profile at {github_url} and this personal write-up: {personal_writeup}. Use your tools to extract and combine information from these sources. | A profile covering skills, project experience, contributions, interests and communication style. | — | yes | — |
| `resume_strategy` | Resume Strategist for Engineers | Using the profile and the job requirements from earlier tasks, tailor the résumé to bring forward the most relevant areas. Use your tools to adjust and improve the résumé content. Make it the best résumé possible. Do not make up any information. Update every section: the summary, work experience, skills and education, so they better show the candidate's abilities and how they match the job posting. | An updated résumé that highlights the candidate's qualifications and experience relevant to the job. | `research`, `profile` | no | `tailored_resume.md` |
| `interview_preparation` | Engineering Interview Preparer | Create a set of likely interview questions and talking points based on the tailored résumé and the job requirements. Use your tools to produce relevant questions and discussion points that help the candidate bring out the résumé's main points and how they match the job posting. | A document of key questions and talking points the candidate should prepare for the first interview. | `research`, `profile`, `resume_strategy` | no | `interview_materials.md` |

Required inputs (from the placeholders): `job_posting_url`, `github_url`, `personal_writeup`.

## 7. Business rules

### 7.1 What must stay true (the course's pattern card)

Every option of every question keeps all four items.

1. **The work is split across several specialised agents, and each agent has its own role, goal and backstory.** No single agent does the whole job. → T1, T3
2. **Every piece of work is a task with a clear description and a stated expected output, and each task is assigned to an agent.** → T1, T2
3. **Results move between agents: a task works from the outputs of the tasks it depends on and does not start until they are done. The run finishes when every task is done.** → T8, T9, T10
4. **One team definition serves any instance of the job: each run takes its named inputs and puts them in place wherever the agents and tasks use them.** → T4, T5, T6

### 7.2 Rules

- **R1 Valid team only.** A definition that breaks contract A or its extra checks is refused before any model call, with a message naming the agent or task and the field at fault; nothing is written except the refusal. → T1, T2, T3
- **R2 Inputs in place.** Every `{name}` in roles, goals, backstories, descriptions and expected outputs is replaced by the input's text before any prompt is sent; no prompt contains an unreplaced placeholder. A run missing any required input is refused before any model call with `missing input: <name>` for each. Unused inputs are accepted and ignored. → T4, T5, T6, T7
- **R3 Results passed on.** A task's prompt contains its agent's role, goal and backstory, the task's description and expected output, and the results of the tasks it receives, each labelled with the task name. A task with `context` receives exactly those tasks' results. A task without `context` receives the result of the task listed just before it, unless both are parallel tasks started together (then it receives none) or it is first. → T9, T15
- **R4 Order.** A task starts only when every task in its `context` is done. Consecutive parallel tasks start together once the tasks before them are done. A non-parallel task starts only after every earlier task is done. → T8, L1
- **R5 Run ends when every task is done.** The run returns, and the command exits, only after every task, including parallel ones, has finished and every output file and the run record are written. → T10, T19, L1
- **R6 Result files.** A task with `output_file` writes exactly its result text (surrounding whitespace trimmed, one trailing newline) to `<output dir>/<output_file>`. → T10
- **R7 Tool errors go back to the agent.** A failing tool or delegation request never stops the run: its `Tool error: …` text is returned to the agent as the result of that request, recorded with `error: true`, and the agent continues. → T11, T15
- **R8 Résumé tool fixed to one file.** `read_resume` reads only the configured résumé file (S5). → T11
- **R9 Shared cache.** Within one run, a tool request with the same tool and argument as an earlier successful request, by any agent, is answered from the cache without reaching the source, and recorded `cached: true`. → T12, T13
- **R10 Step limit.** An agent may make at most S4 (15) tool and delegation requests in one task. The 15th request's result is returned together with the line `Step limit reached: give your final answer now.`; the agent's next reply is the task's result, whatever it contains. → T13
- **R11 Delegation.** An agent with `allow_delegation: true` may ask a coworker a question or hand it a piece of work by role; the coworker answers in its own role with its own prompt, and the answer returns to the asker as the request's result. Asking an unknown role or itself is a tool error (R7). An agent with `allow_delegation: false` is offered no delegation. → T14, T15
- **R12 No invented résumé facts.** The résumé-rewrite task's prompt tells the agent not to make up any information and to update the summary, work experience, skills and education. → T16
- **R13 Focused tools.** Each agent is offered only its listed tools; a task's `tools` list replaces its agent's tools for that task. → T17
- **R14 Secrets and model choice.** Without the chosen provider's key and without `--model scripted`, the program exits with a non-zero code and a message naming the missing variable, before any task starts and without writing result files. → T18
- **R15 Run record and progress log.** Every run writes the run record (contract C), creating the output folder if absent. With S3 on, each task prints `[<task>] started — <role>` when it starts and `[<task>] finished` when it ends; with S3 off these lines are not printed. → T19, T21
- **R16 Résumé search.** `search_resume` returns at most S6 (3) passages, best first. C7a ranks by embedding similarity. The shared-words search (offline stand-in, and C7b) lowercases and splits text into words at every character that is not a letter or digit, scores each passage by how many distinct query words it contains, drops passages scoring 0, and orders by score, then by position in the file. → T20, L3
- **R17 Page text.** `fetch_page` returns the fetched page's readable text with markup removed; the stand-in returns the mapped sample file's text exactly. → T11, L2

## 8. Tests

### 8.1 Sample data (all facts written for this spec)

**`sample_data/resume.md`** (exact content):

```
# Mara Lindqvist
## Summary
Engineering manager with 12 years in software, leading teams of up to 20 engineers across three countries.
## Work experience
### Northwind Freight — Head of Engineering, 2019–2024
- Led the platform reorganisation and grew the engineering team from 6 to 20 people.
- Wrote the first version of the shipment-tracking API in Python (Flask) backed by PostgreSQL.
### Quillon Health — Senior Software Engineer, 2014–2019
- Mentored four junior engineers on the billing team.
- Moved the billing service into Docker containers.
## Skills
Leadership, hiring, roadmapping, Python, SQL
## Education
BSc Computer Science, University of Tartu, 2012
```

Its passages, in order: P1 "Engineering manager with 12 years … three countries.", P2 "Led the platform reorganisation … 6 to 20 people.", P3 "Wrote the first version … backed by PostgreSQL.", P4 "Mentored four junior engineers on the billing team.", P5 "Moved the billing service into Docker containers.", P6 "Leadership, hiring, roadmapping, Python, SQL", P7 "BSc Computer Science, University of Tartu, 2012".

**Sample pages** (`sample_data/pages/`, served by the stand-in page fetcher through `sample_data/pages/map.json`):

| URL | File | Exact text |
|---|---|---|
| `https://jobs.example.test/fernhill/backend-engineer` | `fernhill_backend_engineer.txt` | `Backend Engineer — Fernhill Analytics` / `We build forecasting tools for regional grocers.` / `Requirements: Python; PostgreSQL; REST API design; Docker; 5+ years building backend services.` / `Nice to have: Kubernetes.` (four lines) |
| `https://jobs.example.test/oakline/data-engineer` | `oakline_data_engineer.txt` | `Data Engineer — Oakline Energy` / `Requirements: Python; Airflow; SQL.` (two lines) |
| `https://code.example.test/maralind` | `maralind_profile.txt` | `maralind — code profile` / `Repositories:` / `- freight-tracker-api (Python, PostgreSQL), 120 stars` / `- dockerized-billing (Docker)` / `- rest-patterns (REST API examples)` (five lines) |

Any other URL: `Tool error: page not found: <url>`. The stand-in fetcher counts how often each URL reaches it (the "source count").

**`sample_data/inputs.json`:** `job_posting_url` = `https://jobs.example.test/fernhill/backend-engineer`; `github_url` = `https://code.example.test/maralind`; `personal_writeup` = `Mara has led engineering teams for five years and still writes backend code every week. She wants to return to a hands-on backend role.`

**`sample_data/crews/loop_test.json`** (test-only team, a contract A instance):
- Agents: `Looping Agent` (goal "Fetch pages.", backstory "You fetch pages.", tools `fetch_page`, `allow_delegation: false`); `Helper Agent` (goal "Help out.", backstory "You help.", tools `fetch_page`, `allow_delegation: true`).
- Tasks: `t_loop` (agent Looping Agent, description "Fetch {job_posting_url} until satisfied.", expected output "One line starting with FINAL."); `t_help` (agent Helper Agent, description "Help with {job_posting_url}.", expected output "One line.", `tools: ["read_resume"]`). Neither is parallel; no context.

**Planted failure:** the Profiler's first scripted request asks `read_resume` to read a web address (the course demonstrated an agent using a file-reading tool on a website).

**Scripted stand-in model** (`sample_data/scripted_replies.json`; a stand-in for the real model, labelled as such). For each reply, the rows for the replying role are checked in order; the first matching row wins. "n" is how many request results (tool results, errors, delegation answers) the agent has received so far in the current task or delegated conversation. A reply is either a request (tool or delegation, with its argument) or a final answer.

| Role | When | Reply |
|---|---|---|
| Tech Job Researcher | prompt contains `Which requirement matters most?` | final: `PostgreSQL experience at scale.` |
| Tech Job Researcher | n = 0 | `fetch_page` with the first `https://` URL in its task description |
| Tech Job Researcher | n = 1 | final: `JOB REQUIREMENTS: Python; PostgreSQL; REST API design; Docker; 5+ years backend services.` |
| Personal Profiler for Engineers | n = 0 | `read_resume` with the first `https://` URL in its task description (planted failure) |
| Personal Profiler for Engineers | n = 1 | `fetch_page` with that same URL |
| Personal Profiler for Engineers | n = 2 | `read_resume` with an empty argument |
| Personal Profiler for Engineers | n = 3 | final: `CANDIDATE PROFILE: Python (Flask) API on PostgreSQL at Northwind Freight; Docker at Quillon Health; REST API examples in rest-patterns; led teams of up to 20.` |
| Resume Strategist for Engineers | n = 0 | `fetch_page` `https://jobs.example.test/fernhill/backend-engineer` |
| Resume Strategist for Engineers | n = 1 | `search_resume` `PostgreSQL` |
| Resume Strategist for Engineers | n = 2 | final: the tailored résumé text below |
| Engineering Interview Preparer | n = 0 | `ask_question` to `Tech Job Researcher`: `Which requirement matters most?` |
| Engineering Interview Preparer | n = 1 | final: the interview text below |
| Looping Agent | prompt contains `Step limit reached` | final: `FINAL: stopped` |
| Looping Agent | otherwise | `fetch_page` `https://jobs.example.test/fernhill/backend-engineer` |
| Helper Agent | n = 0 | `ask_question` to `Recruiter`: `Any advice?` |
| Helper Agent | n = 1 | final: `HELPER DONE` |

Tailored résumé text (Strategist's final answer):

```
# Mara Lindqvist
## Summary
Backend engineer with 12 years in software who builds Python APIs on PostgreSQL and ships them in Docker.
## Work experience
- Northwind Freight: wrote the first shipment-tracking API in Python (Flask) backed by PostgreSQL.
- Quillon Health: moved the billing service into Docker containers.
## Skills
Python, SQL, PostgreSQL, Docker, REST API design
## Education
BSc Computer Science, University of Tartu, 2012
```

Interview text (Interview Preparer's final answer):

```
INTERVIEW MATERIALS
1. Q: How did you design the shipment-tracking API on PostgreSQL? Talking point: the first version was written in Python (Flask).
2. Q: How did you move the billing service into Docker? Talking point: containers at Quillon Health.
```

Every test runs with `--model scripted --pages sample`, a fresh output folder, and all settings at their defaults, unless it says otherwise.

### 8.2 Test table

| Test | Rules | Given | When | Then |
|---|---|---|---|---|
| T1 | R1; card 1, 2 | `crews/job_application.json` | it is validated, then run with `sample_data/inputs.json` | valid; 4 agents with distinct roles, each with non-empty role, goal, backstory; 4 tasks, each with non-empty description and expected output and an agent among the 4; each task's first prompt contains its own agent's role and backstory and no other agent's backstory |
| T2 | R1; card 2 | copies of `job_application.json` with one fault each: (a) `interview_preparation` without `expected_output`; (b) `research` with empty `description`; (c) `profile` with agent `Recruiter`; (d) `resume_strategy` with context `interview_preparation`; (e) Researcher with tool `send_email`; (f) two tasks named `research`; (g) `output_file` `../x.md`; (h) Profiler without `backstory` | each is run | each refused; message names the task or agent and the field; stand-in model received 0 prompts; no result files |
| T3 | R1; card 1 | copy of `loop_test.json` with `t_help` assigned to `Looping Agent` | it is run | refused with a message saying at least two different agents must be assigned tasks; 0 prompts |
| T4 | R2; card 4 | sample inputs without `github_url` | run | refused with `missing input: github_url`; 0 prompts; no result files |
| T5 | R2; card 4 | sample inputs | run | the Profiler's first prompt contains `https://code.example.test/maralind` and the full `personal_writeup` text; no prompt in the run contains `{job_posting_url}`, `{github_url}` or `{personal_writeup}` |
| T6 | R2; card 4 | sample inputs with `job_posting_url` = `https://jobs.example.test/oakline/data-engineer` | run; then compare the definition file's bytes before and after | the Researcher's first prompt contains the Oakline URL and not the Fernhill URL; its first `fetch_page` argument is the Oakline URL; the definition file is unchanged |
| T7 | R2 | sample inputs plus `"budget": "none"` | run | status `completed` |
| T8 | R4; card 3 | sample inputs; S10 = 0.3 s for Tech Job Researcher, 0.05 s for Personal Profiler for Engineers | run | in the record: `research.started_at` < `profile.ended_at` and `profile.started_at` < `research.ended_at` (they overlap); `profile.ended_at` < `research.ended_at`; `resume_strategy.started_at` ≥ `research.ended_at`; `interview_preparation.started_at` ≥ `resume_strategy.ended_at` |
| T9 | R3; card 3 | sample inputs | run | the Strategist's first prompt contains `JOB REQUIREMENTS:` and `CANDIDATE PROFILE:`; the Interview Preparer's first prompt contains both and `# Mara Lindqvist`; the Researcher's and Profiler's first prompts contain neither `JOB REQUIREMENTS:` nor `CANDIDATE PROFILE:` |
| T10 | R5, R6; card 3 | sample inputs | the run returns | `results` has exactly `research`, `profile`, `resume_strategy`, `interview_preparation`; `output/tailored_resume.md` equals the tailored résumé text and `output/interview_materials.md` equals the interview text (trimmed, one trailing newline); both exist at the moment the run returns; the record lists 4 tasks |
| T11 | R7, R8, R17 (planted failure) | sample inputs | run | `profile.tool_calls[0]` is `read_resume` with argument `https://code.example.test/maralind`, `error: true`, message contains `only reads` and `resume.md`; `tool_calls[1]` is `fetch_page` of the same URL, `error: false`, and the Profiler's third prompt contains `freight-tracker-api (Python, PostgreSQL), 120 stars`; `tool_calls[2]` is `read_resume` with an empty argument, `error: false`, and the Profiler's fourth prompt contains `Mentored four junior engineers`; `profile.result` starts `CANDIDATE PROFILE:`; status `completed` |
| T12 | R9 | sample inputs | run | `resume_strategy.tool_calls[0]` is `fetch_page` of the Fernhill URL with `cached: true`; source count for the Fernhill URL is 1 and for the profile URL is 1 |
| T13 | R9, R10 | `loop_test.json`, inputs `{"job_posting_url": "https://jobs.example.test/fernhill/backend-engineer"}` | run | `t_loop.tool_calls` has 15 entries: first `cached: false`, the other 14 `cached: true`; source count for the Fernhill URL is 1; the Looping Agent's 16th prompt contains `Step limit reached: give your final answer now.`; `t_loop.result` = `FINAL: stopped` |
| T14 | R11 | sample inputs | run | `interview_preparation.delegations` has one entry: kind `ask_question`, to `Tech Job Researcher`, request `Which requirement matters most?`, answer `PostgreSQL experience at scale.`; the Interview Preparer's second prompt contains that answer |
| T15 | R3, R7, R11 | as T13 | run | the Helper Agent's first prompt contains `FINAL: stopped`; `t_help.delegations[0]` is to `Recruiter` with answer starting `Tool error: no coworker with role Recruiter`; `t_help.result` = `HELPER DONE`; status `completed`; `t_loop.may_delegate` is false |
| T16 | R12 | sample inputs | run | the Strategist's first prompt contains `Do not make up any information.` and the words `summary`, `work experience`, `skills`, `education` |
| T17 | R13 | sample inputs; then as T13 | run each | `research.available_tools` = [`fetch_page`]; `profile`, `resume_strategy`, `interview_preparation` each = [`fetch_page`, `read_resume`, `search_resume`] (any order); `t_help.available_tools` = [`read_resume`] |
| T18 | R14 | `OPENAI_API_KEY` unset; no `--model scripted` | `python -m crew_runner run --crew crews/job_application.json --inputs sample_data/inputs.json` | exit code ≠ 0; stderr contains `OPENAI_API_KEY`; no result files |
| T19 | R5, R15 | no `output/` folder | run with sample inputs | `output/` exists and holds `run_record.json` (valid against contract C, status `completed`, model `scripted (stand-in)`), `tailored_resume.md`, `interview_materials.md` |
| T20 | R16 | `sample_data/resume.md`, shared-words search | `search_resume("engineering team billing")`; `search_resume("PostgreSQL")` | first returns exactly P2, P4, P1 in that order (scores 2, 2, 1; P5 also scores 1 but is dropped by the limit of 3); second returns exactly P3 |
| T21 | R15 | sample inputs; S3 on, then S3 off | run each | with S3 on, stdout contains `[research] started — Tech Job Researcher` and `[research] finished`; with S3 off, no stdout line starts with `[research]` |
| L1 `live` | R4, R5 | `OPENAI_API_KEY` set; `--pages sample`; real agent model | run with sample inputs | status `completed`; both result files exist and are non-empty; `tailored_resume.md` contains `Mara Lindqvist`; ordering as in T8 (without the overlap condition) |
| L2 `live` | R17 | `OPENAI_API_KEY` set; network | live `fetch_page("https://example.com")` | text contains `Example Domain` |
| L3 `live` | R16 | `OPENAI_API_KEY` set; C7a embedder | `search_resume("database work")` | 3 passages; P3 is among them |

Every test's rules match section 7.2's arrows.

## 9. Standing permissions

- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in in code, output and run record; read secrets from the environment only.
- **Ask first:** changing an answered question or a setting once the build has data; anything that sends data to a third party beyond the chosen model provider and the pages the inputs name (a résumé is personal data).
- **Never:** invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets.

## 10. Test plan

- Install: `pip install -e ".[test]"` (or the project's equivalent).
- Offline: `pytest -m "not live" -q` — T1–T21.
- Live: `OPENAI_API_KEY=… pytest -m live -q` — L1–L3; skipped, not failed, when the key is unset.
- Demo run (stand-ins): `python -m crew_runner run --crew crews/job_application.json --inputs sample_data/inputs.json --model scripted --pages sample`.
- Real run: `python -m crew_runner run --crew crews/job_application.json --inputs my_inputs.json`.
- Adjust for choices: where a chosen option changes a rule (for example C9b removes T8's overlap condition and makes `profile` receive `research`'s result; C10b changes T14 and T15 to expect a refused delegation; C3b/C3c change T18's variable name; C1b adds the same tests for the learner's definition), change the affected test and say so in the report.
- For every chosen non-recommended option, turn its "what to check" sentence (section 1) into a test and report it.
- Report a result per test with evidence (test output, file paths). "Should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.
- Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

## 11. Background notes (for the build agent)

### 11.1 The program
`take named inputs (one team serves any instance) → put them into the team's roles and tasks (the same definition, different jobs) → start the tasks that need nothing, side by side (save time) → each agent works its task with its own focused tools, may ask coworkers (specialists do better than one generalist) → pass each result to the tasks that depend on it (later work builds on earlier work) → wait until every task is done, save the results (the job is finished only when every part is)`.
The progress log and run record show what ran; they are not a stage.

### 11.2 Failures
- **Wrong tool for the input (demonstrated).** In the outreach lesson, an agent tried to read a website with the file-reading tool and got an error. The framework returned the error to the agent instead of stopping, and the agent switched to another tool. Prevention: R7, R8; planted in the Profiler's scripted replies; tested by T11.
- **An error that stops the run (warned).** The course says an unhandled tool error stops the crew and loses the work done so far, and that "you don't want to do that". Never offered; R7, T11, T15.
- **Agents stuck repeating a tool (warned).** Early versions of the framework had agents use the same tool over and over, especially on open-source models; the framework added guardrails so agents always reach an answer. R9, R10; T13.
- **Too many tools (warned).** Overloaded agents struggle to choose a tool, and smaller models do worse. R13; T17. C3c warns of the same.
- **Context fades along a long chain (warned).** In a sequential process the original context weakens with each handoff. Explicit `context` lists give later tasks the original results directly (R3, T9); C8b is the course's other remedy.
- **Result file read too early (warned, event-planning lesson).** A notebook note said to wait for a parallel task's file after the run returned. R5 makes the run return only after every file is written; T10.
- **Made-up content (warned).** The course says guardrails help prevent hallucinations, and its résumé task said not to make up any information. R12, T16; C11b adds a fact-checking reviewer.
- **Different outputs for the same input (noted throughout).** That is why offline tests use the scripted stand-in and live tests check loosely.

### 11.3 Why the questions and settings are what they are
- C1: the course built six crews for different jobs on the same parts and invited learners to try their own topics and inputs. C1b's examples are the course's earlier crews.
- C2: the course's résumé was Markdown; its tool list included PDF and Word search tools. C2b is an option this spec adds for learners whose résumé is not text.
- C3: the course used OpenAI and named Hugging Face, Mistral, Cohere and local models through Ollama as alternatives; it warned that smaller models handle many tools worse.
- C4: the course said its concepts apply to all major frameworks and that agents can be built without a framework, at the cost of "a lot of more coding".
- C5: the course ran in notebooks and mentioned a hosted service that turns crews into APIs; both options here are additions.
- C6: the course used a Google-search API service with its own key (free credits); see D1.
- C7: the course did semantic search (RAG) over the résumé. Keeping it (the key is already needed) follows the stand-in rule, and the shared-words search is offered as the lighter stand-in.
- C8: the course showed a hierarchical process in the financial-analysis lesson. Its stated benefits: a manager that remembers the initial goal, delegates and reviews. The course's final crew used the default sequential process.
- C9: parallel tasks were taught in the event-planning lesson and used in the final crew for the two research tasks.
- C10: delegation was taught in the support lesson. The course said leaving the delegation flag unset means delegation is allowed. The final crew leaves it unset, so delegation is on.
- C11, C12: offered from other lessons by the pattern card. The QA reviewer and memory come from the support lesson; memory types were explained in the key-elements lesson and used again in the outreach crew. The final crew used neither.
- C13, C14: human input before a task finishes, and JSON output from a typed model, were taught in the event-planning lesson.
- **Subjects that are not questions:**
  - Turning the tool cache off fails test 3: this spec could not write a learner situation for this program that needs the same fetch twice in one run to give a fresh result.
  - Stopping the run on a tool error fails test 2: the course says not to.
  - A single agent doing the whole job fails test 1 (card item 1).
  - A model per agent is setting S1 (4.3). The progress log level is S3, temperature S2, the résumé path S5.
  - Fixing a page tool to one address is setting S9.
  - Task callbacks and the directory-reading tool fail test 3: no learner situation for this program that C1b's custom tools and the run record do not already cover.
  - The course's hosted deployment service fails test 3: access was by application to an early beta, so the spec cannot give a situation where it is a buildable path that C5b does not already serve.
  - Custom tools are part of C1b, not a separate question.
  - The website semantic-search tool (imported in the support lesson, never used) is not a question: it does not change a stage.
- **Where values came from (4.2):**
  - Agent model: the notebooks set `gpt-3.5-turbo` in every lesson. The videos of the outreach, event-planning, financial and job-application lessons used GPT-4 / GPT-4 turbo; the notebooks say the platform could not run it. The narration of lesson 4 also says the framework's default model was GPT-4. Rule (1) picks `gpt-3.5-turbo`, the model the instructor chose when introducing model choice. The build agent picks a current model anyway (D3).
  - Progress log: on in the final crew; the most detailed level ("2") in the first, support and outreach crews. Rule (2): the final app.
  - Delegation on: the course-stated default, left unset in the final crew.
  - Parallel `research` and `profile`, the `context` lists, the output file names and the three input names all come from the job-application lesson.
  - Memory off: unset in the final crew.
  - Manager temperature 0.7: financial lesson.
  - Step limit 15, 3 passages, output folder, run record: additions.
- **Course disagreements recorded (W4):**
  - In the job-application lesson, the narration first describes the profiler as crossing the résumé with the job posting. Its code runs the profiler side by side with the posting research, without the posting's result, and the narration later says the two run in parallel. This spec follows the code and the later narration.
  - A deck-only slide calls the job-application crew "your first multi-agent system", but it is the course's last crew; the transcripts win.
  - The job-application lesson's "back into lesson one" refers to the overview lesson (transcript lesson 2).
- **Course quirk kept:** the course passed inputs that no placeholder used (the event budget, the trading capital); R2 accepts and ignores them.

### 11.4 Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports:
- Library names: `crewai` 0.28.8, `crewai_tools` 0.1.6, `langchain_community` 0.0.29, `langchain_openai.ChatOpenAI`.
- Classes and parameters: `Agent`, `Task`, `Crew`, `Process.hierarchical`, `manager_llm`, `kickoff(inputs=…)`, `allow_delegation`, `verbose=2`, `memory=True`, `async_execution`, `context`, `output_file`, `output_json`, `human_input`, `tools=` on agent and task.
- Tools: `BaseTool` with a `_run` method, `SerperDevTool`, `ScrapeWebsiteTool(website_url=…)`, `FileReadTool(file_path=…)`, `MDXSearchTool(mdx=…)`, `DirectoryReadTool(directory=…)`, `WebsiteSearchTool`.
- The `OPENAI_MODEL_NAME` environment variable.
- Models: `gpt-3.5-turbo`, `gpt-4-turbo`, GPT-4, Llama 3 70B, `HuggingFaceH4/zephyr-7b-beta`, `mistral-small`, Cohere chat. Documentation shown: v0.22.4.

The course states no request-parameter limits for these models.

### 11.5 Course names
- The course's résumé file `fake_resume.md` becomes the `sample_data/resume.md` setting (S5).
- The output files `tailored_resume.md` and `interview_materials.md` (binding).
- The input names `job_posting_url`, `github_url`, `personal_writeup` (binding).
- The four agent roles (binding).
- The task variable names `research_task`, `profile_task`, `resume_strategy_task`, `interview_preparation_task` become `research`, `profile`, `resume_strategy`, `interview_preparation`.
- The course's "crew" is this spec's "team".

### 11.6 Lesson map (transcript numbering)
1 Introduction, 2 Overview (job-application crew preview: posting, résumé, four agents, tools; agentic vs rule-based automation), 3 AI Agents (multi-agent systems; different models per agent), 4 Create agents to research and write an article (agents, tasks, crews; placeholders; sequential pass-on; inputs at kickoff), 5 Key elements of AI agents (six elements; focus and tool warnings; guardrails; memory types), 6 Multi agent customer support automation (delegation, QA reviewer, agent vs task tools, memory), 7 Mental framework for agent creation (roles from "who would I hire"), 8 Key elements of agent tools (versatile, fault-tolerant, caching), 9 Tools for a customer outreach campaign (custom tool; demonstrated wrong-tool error; caching), 10 Recap of tools, 11 Key elements of well defined tasks (description and expected output mandatory; task options), 12 Automate event planning (parallel tasks, human input, JSON output, output files), 13 Recap on tasks, 14 Multi agent collaboration (processes; context fading; manager), 15 Multi agent collaboration for financial analysis (hierarchical run; unused inputs), 16 Build a crew to tailor job applications (the recommended build), 17 Next steps (hosted service; building without a framework), 18 Conclusion.

Notebooks belong to lessons 4, 6, 9, 12, 15 and 16. All slide descriptions were read: narrated slides counted as their lesson's transcript; deck-only slides counted less, and the one disagreement found is recorded above.

Nothing in this spec requires access to the course.

---

*Spec v1 · course: Multi AI Agent Systems with crewAI · project: crew runner (default job: résumé tailoring) · When the build agent does something unexpected, add the missing constraint here and re-run.*
