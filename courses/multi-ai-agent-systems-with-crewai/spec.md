# Spec: a team of AI agents that tailors a résumé to a job posting

**What you're building:** a command-line program that takes three named inputs (a job posting address, a code-profile address and a short write-up about the candidate), runs a team of four specialised AI agents (job researcher, profiler, résumé strategist, interview preparer) through four tasks, and writes two files: a résumé tailored to that job and a set of interview questions with talking points.

**Fastest path:** at the first question, answer "recommended build". The build is finished when the offline tests pass. They need no API key and no network: a scripted stand-in model and stand-in page reader drive every stage. An OpenAI key is needed only for the `live` tests and for real runs.

**This file is self-contained.** Everything the build needs is in it. Nothing here requires access to the course.

*Provenance:* written from the course "Multi AI Agent Systems with crewAI", using its notebooks (6, rendered from the course repo, with their helper module), transcripts (18 lessons), slide descriptions (2 decks) and the owner-confirmed pattern card · 2026-10-27 · guide v2.6 (2026-10-27).

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
   checklist in step 5 marks each place it differs from the course), or **choose** question by
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

### C1. What job should the team of agents do?
- **C1a. Tailor a résumé and prepare interview notes for one job posting (Recommended - course default).** Four agents: a job researcher reads the posting, a profiler studies the candidate, a résumé strategist rewrites the résumé, an interview preparer writes questions and talking points. Pick this when you want the program exactly as described in this spec, or you are job hunting. Setup cost: none beyond the model key (C3).
- **C1b. Your own job, with your own named inputs, agents, tasks and result files.** You describe: the inputs each run takes; each agent's role, goal and backstory; each task's description, expected output, agent, the tasks it waits for, and the result file it writes (if any). The build agent writes these into the team definition file (section 4) in place of the résumé team. Pick this when you want the same kind of program for your own work, for example a team that researches a sales lead and drafts outreach emails, or one that plans and writes a blog post on a topic. Setup cost: your time to describe the team; sample data and scripted replies must be rewritten for your team.
  - *What to check:* with your team definition, every named input appears in at least one agent or task text and is filled in on a run, every task starts only after the tasks it waits for have finished, and every named result file is written.

### C2. Where does the team get its source material?
- **C2a. Web pages at addresses given in the inputs, plus local files the team definition names (Recommended - course default).** A page reader fetches each address an agent asks for; a file reader reads the résumé file. Pick this when your sources are public web pages and a document on disk. Setup cost: network access during real runs.
- **C2b. Local files only, no network.** The posting, profile and résumé are files in a folder the team may read; inputs name the files. Pick this when your sources are private documents, the page needs a login the reader cannot pass, or you must work offline. Setup cost: you save the pages as files yourself.
  - *What to check:* the team reads every source from the named local folder and a run makes no network request other than to the model provider.
- **C2c. Nothing beyond the inputs: agents use only the inputs and the model's own knowledge.** No tools. Pick this when the inputs themselves carry everything the job needs, for example writing an article on a given topic. Setup cost: none.
  - *What to check:* no agent has any tool, and a run produces every result file from the inputs alone.

### C3. Which model provider powers the agents?
- **C3a. OpenAI (Recommended - course default).** Pick this when you have, or can get, an OpenAI key; it is what the course used, and its embeddings also serve the résumé search (C5). Setup cost: an OpenAI API key (paid account).
- **C3b. Another hosted provider (for example Mistral, Cohere or Hugging Face).** Pick this when you already pay for another provider or your organisation requires one. Setup cost: that provider's key; the résumé search (C5) and memory (C9) need an embedding model, from that provider if it offers one, otherwise a local embedder (an addition).
  - *What to check:* a live run on the sample inputs completes with every agent's model calls going to the chosen provider and both result files written.
- **C3c. A local model served on your machine (for example through Ollama).** Pick this when you have no paid key or data must not leave your machine. The course warns that smaller and open-source models handle tools less well: they may pick the wrong tool or call the same tool over and over, so expect weaker results. Setup cost: a model download of several GB and a machine able to run it; a local embedder for C5 and C9.
  - *What to check:* a live run on the sample inputs completes with no request leaving the machine, and each agent ends its task with an answer within the step limit.

### C4. Should agents be able to search the web?
*Ask only when `C2` is `C2a`.*
- **C4a. No web search; agents read only the addresses and files they are given (Recommended).** Pick this when every page the agents need is named in the inputs. Setup cost: none.
- **C4b. Google search through the Serper service, for every agent (course default).** Pick this when the agents must find pages you cannot list in advance, for example the company's recent news or the candidate's other work. Setup cost: a Serper account and key (free credits at sign-up); searches count against its rate limit.
  - *What to check:* each agent has a web-search tool that returns results for a query, and a failed search (no key, rate limit) comes back to the agent as an error message instead of stopping the run.

### C5. Should agents be able to search inside the résumé by meaning, as well as read it whole?
*Ask only when `C2` is `C2a` or `C2b`.*
- **C5a. Both: a whole-document reader and a search-by-meaning tool over the same document (Recommended - course default).** Pick this when the main document is long enough that an agent benefits from pulling out just the matching passages. Setup cost: an embedding step and a small local vector store; embedding calls use your model key.
- **C5b. Whole-document reader only.** Pick this when the main document is short (one or two pages), so reading it whole is enough, or you want no embedding step. Setup cost: none.
  - *What to check:* the profiler, résumé strategist and interview preparer each have the whole-document reader and no search tool, and the tailored résumé is still written.

### C6. May agents hand work to, or ask questions of, their teammates?
- **C6a. Yes: every agent may delegate work to a teammate or ask a teammate a question (Recommended - course default).** The model decides at run time whether to do so. Pick this when you want the agents to cooperate and correct each other, which the course says improves results. Setup cost: none; some runs make extra model calls.
- **C6b. No: each agent only does its own task.** Pick this when you need a predictable number of model calls per run (a tight budget or rate limit): the course notes that whether an agent delegates is up to the model and not under your control. Setup cost: none.
  - *What to check:* no agent is offered a tool for delegating to, or questioning, a teammate, and a run still writes every result file.

### C7. How are the tasks scheduled?
- **C7a. Tasks that do not depend on each other run at the same time; a task that depends on others waits for all of them (Recommended - course default).** The job research and the candidate profile run in parallel; the résumé rewrite waits for both; the interview notes wait for all three. Pick this when some tasks are independent and you want the run to finish sooner. Setup cost: none.
- **C7b. One task at a time, in list order.** Each task still receives the outputs of every task it depends on. Pick this when your provider's rate limit rejects two agents calling at once, or you want the run log in a strict order. Setup cost: none; runs take longer.
  - *What to check:* no two tasks overlap in time, and each task still receives the outputs of every task it depends on.
- **C7c. A manager agent decides who does what and reviews the results.** The framework creates the manager from a model you choose; it hands each task to an agent, receives the result, and may ask for improvements. Pick this when the order of the work is not fixed in advance or you want one agent that keeps the overall goal in view across a long chain of tasks. Setup cost: an extra model role (the manager); runs make many more model calls and take noticeably longer.
  - *What to check:* the manager acts first, each task's result goes back to the manager before the next task is handed out, and every result file is written.

### C8. Should a reviewer agent check the results before they are final?
- **C8a. No reviewer (Recommended - course default).** Pick this when the results are for your own use. Setup cost: none.
- **C8b. Add a quality-assurance reviewer agent and a final review task.** The reviewer reads the tailored résumé against the job requirements, the profile and the original résumé, and may send work back to the agent who wrote it (when `C6` is `C6b`, it corrects the text itself). Its reviewed version becomes the tailored résumé file. Pick this when your output reaches someone else, such as an employer or a customer, and should be fact-checked before it goes out. The course recommends a final QA agent for most teams. Setup cost: one more agent's model calls; longer runs.
  - *What to check:* the tailored résumé file holds the reviewer's version, and the reviewer's task received the job requirements, the profile and the original résumé.

### C9. Should the agents remember earlier steps and past runs?
- **C9a. No memory (Recommended - course default).** Each run starts fresh; agents share results only through task outputs. Pick this when runs are independent, for example a different job posting each time. Setup cost: none.
- **C9b. Memory on: short-term (shared across agents during a run), long-term (stored on disk after a run, so later runs learn from earlier ones) and entity memory (the people, companies and places a run discusses).** Pick this when you run the team again and again on similar jobs and want it to improve with use. Setup cost: embedding calls on your model key; a local memory database on disk.
  - *What to check:* after one run a local memory store exists on disk, and a second run's agents receive material stored by the first.

---

## 2. Departures from the course

| # | Where the recommended build differs | Why |
|---|---|---|
| D1 | No web search (C4a); the course gave every agent Serper search. | Serper needs its own account and key, which the build does not otherwise need. The page reader and résumé tools already carry the taught behaviour of agents gathering information with tools. Offered as C4b. |
| D2 | Offline tests use a scripted stand-in model, a stand-in page reader and a stand-in résumé search (additions). | The course's model and résumé search need an OpenAI key, and its page reader needs the network. The finished app uses the real ones when a key is present. |
| D3 | Sample data (job posting, code profile, résumé, write-up) is written for this spec. | No course data is copied; the facts are invented and fixed so tests can assert them. |
| D4 | The team (agents, tasks, which task waits for which, result files) is stored in a data file, `team.json` (addition). | The course defined the team in notebook code. A data file makes "one team definition serves any instance" testable and makes C1b a file edit. |
| D5 | Each agent is limited to 10 reasoning steps per task (addition). | The course relies on the framework's built-in guardrail against endless loops but states no number; tests need a known limit. |
| D6 | A run with a missing input stops before any model call and names the missing input (addition). | The course never shows a missing input; this stops a run from sending an unfilled `{placeholder}` to the model. |
| D7 | A command-line program writing to `output/`, not a notebook (addition). | The build is never a notebook. |
| D8 | The model is chosen at the checklist; the course used `gpt-3.5-turbo` in its code and `gpt-4-turbo` in the lesson video. | Model names go stale. |
| D9 | Agent and task texts fix the course's typos (for example "increditble", "reflrect", "candiadte"). | Readability; the meaning is unchanged. |

---

## 3. Objective

Given the three named inputs, run four specialised agents through four defined tasks, passing each task's result to the tasks that depend on it, and write a tailored résumé and interview materials to two files.

---

## 4. Tech stack and versions

- **Language:** Python. The course states no Python version; use one that the pinned packages below install on (addition). If the pins cannot be installed on the person's machine, stop and ask.
- **Agent framework (course, pinned):** `crewai==0.28.8`, `crewai_tools==0.1.6`, `langchain_community==0.0.29`.
- **Unpinned (course left them unpinned; use a release compatible with the pins):** `pydantic`, `python-dotenv`, `langchain_openai` (only for C7c's manager model).
- **Tests (addition, unpinned):** `pytest`.
- **Secrets:** read from the environment, or from a `.env` file in the project folder (the course loaded keys this way). `OPENAI_API_KEY` (C3a); `OPENAI_MODEL_NAME` names the model (the course set the model through this variable); `SERPER_API_KEY` only for C4b. Never write a key into a file the build creates, and keep `.env` out of version control.

### Files the build creates

| Path | What it is |
|---|---|
| `team.json` | The team definition (schema 5.2). |
| `samples/` | Sample data (section 7.1). |
| `crew_app/` | The program package; run as `python -m crew_app run --inputs <file>`. |
| `tests/` | Offline and `live` tests. |
| `output/` | Result files; created on first run if missing. |
| `resolved-decisions.md` | The gate checklist (section 0). |

---

## 5. Contracts

### 5.1 Run inputs (`--inputs <file>`, JSON)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Run inputs (recommended team)",
  "type": "object",
  "required": ["job_posting_url", "github_url", "personal_writeup"],
  "properties": {
    "job_posting_url": {"type": "string", "format": "uri", "minLength": 1},
    "github_url":      {"type": "string", "format": "uri", "minLength": 1},
    "personal_writeup": {"type": "string", "minLength": 1}
  },
  "additionalProperties": true
}
```
Input names are the course's and are binding. Extra keys are allowed and ignored (the course passed unused keys in one lesson). The required list is not fixed in code: it is every `{name}` placeholder that appears in any agent or task text in `team.json` (R4, R5).

### 5.2 Team definition (`team.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Team definition",
  "type": "object",
  "required": ["agents", "tasks", "process"],
  "properties": {
    "process": {"enum": ["parallel_where_independent", "one_at_a_time", "manager"]},
    "memory": {"type": "boolean", "default": false},
    "agents": {
      "type": "array", "minItems": 2,
      "items": {
        "type": "object",
        "required": ["id", "role", "goal", "backstory", "tools"],
        "properties": {
          "id": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"},
          "role": {"type": "string", "minLength": 1},
          "goal": {"type": "string", "minLength": 1},
          "backstory": {"type": "string", "minLength": 1},
          "tools": {"type": "array", "items": {"enum": ["page_reader", "resume_reader", "resume_search", "web_search"]}, "uniqueItems": true},
          "may_delegate": {"type": "boolean", "default": true}
        }
      }
    },
    "tasks": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "description", "expected_output", "agent"],
        "properties": {
          "id": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"},
          "description": {"type": "string", "minLength": 1},
          "expected_output": {"type": "string", "minLength": 1},
          "agent": {"type": "string", "description": "an agents[].id"},
          "waits_for": {"type": "array", "items": {"type": "string"}, "description": "ids of earlier tasks whose outputs this task receives", "default": []},
          "runs_alongside_next": {"type": "boolean", "default": false, "description": "may run at the same time as the tasks after it"},
          "task_tools": {"type": "array", "items": {"type": "string"}, "description": "if present, the agent uses only these tools for this task"},
          "output_file": {"type": "string", "pattern": "^[A-Za-z0-9_.-]+\\.md$"}
        }
      }
    }
  }
}
```
Load-time checks beyond the schema (R2): every `agent` names an existing agent; every `waits_for` id names an earlier task; role texts are unique. Any failure stops the program before any model call and names the offending task or agent.

**The recommended `team.json`** (role names exact from the course; goals, backstories and task texts are the course's wording with typos fixed):

| Agent id | Role | Goal | Backstory | Tools |
|---|---|---|---|---|
| `researcher` | Tech Job Researcher | Make sure to do amazing analysis on job postings to help job applicants | As a Job Researcher, your prowess in navigating and extracting critical information from job postings is unmatched. Your skills help pinpoint the necessary qualifications and skills sought by employers, forming the foundation for effective application tailoring. | `page_reader` |
| `profiler` | Personal Profiler for Engineers | Do incredible research on job applicants to help them stand out in the job market | Equipped with analytical prowess, you dissect and synthesize information from diverse sources to craft comprehensive personal and professional profiles, laying the groundwork for personalized resume enhancements. | `page_reader`, `resume_reader`, `resume_search` |
| `resume_strategist` | Resume Strategist for Engineers | Find all the best ways to make a resume stand out in the job market. | With a strategic mind and an eye for detail, you excel at refining resumes to highlight the most relevant skills and experiences, ensuring they resonate perfectly with the job's requirements. | `page_reader`, `resume_reader`, `resume_search` |
| `interview_preparer` | Engineering Interview Preparer | Create interview questions and talking points based on the resume and job requirements | Your role is crucial in anticipating the dynamics of interviews. With your ability to formulate key questions and talking points, you prepare candidates for success, ensuring they can confidently address all aspects of the job they are applying for. | `page_reader`, `resume_reader`, `resume_search` |

All four agents have `may_delegate: true` (C6a). Under C4b add `web_search` to all four; under C5b remove `resume_search`.

| Task id | Agent | Description | Expected output | Waits for | Runs alongside next | Output file |
|---|---|---|---|---|---|---|
| `research` | researcher | Analyze the job posting URL provided ({job_posting_url}) to extract key skills, experiences, and qualifications required. Use the tools to gather content and identify and categorize the requirements. | A structured list of job requirements, including necessary skills, qualifications, and experiences. | — | yes | — |
| `profile` | profiler | Compile a detailed personal and professional profile using the GitHub ({github_url}) URLs, and personal write-up ({personal_writeup}). Utilize tools to extract and synthesize information from these sources. | A comprehensive profile document that includes skills, project experiences, contributions, interests, and communication style. | — | yes | — |
| `resume_strategy` | resume_strategist | Using the profile and job requirements obtained from previous tasks, tailor the resume to highlight the most relevant areas. Employ tools to adjust and enhance the resume content. Make sure this is the best resume ever but don't make up any information. Update every section, including the initial summary, work experience, skills, and education. All to better reflect the candidate's abilities and how it matches the job posting. | An updated resume that effectively highlights the candidate's qualifications and experiences relevant to the job. | research, profile | no | `tailored_resume.md` |
| `interview_preparation` | interview_preparer | Create a set of potential interview questions and talking points based on the tailored resume and job requirements. Utilize tools to generate relevant questions and discussion points. Make sure to use these questions and talking points to help the candidate highlight the main points of the resume and how it matches the job posting. | A document containing key questions and talking points that the candidate should prepare for the initial interview. | research, profile, resume_strategy | no | `interview_materials.md` |

`process`: `parallel_where_independent` (C7a; `one_at_a_time` for C7b, `manager` for C7c). `memory`: false (C9a).

### 5.3 Tools

| Tool id | Behaviour | Stand-in for offline tests |
|---|---|---|
| `page_reader` | Fetches the web page at an address the agent gives and returns its text (course: a website scraping tool, unbound, so any address). | **Stand-in page reader** (stand-in for the web scraper): maps each sample address to a file in `samples/pages/`; an unknown address raises the error `page not found: <address>`. |
| `resume_reader` | Returns the full text of the résumé file named by the `resume_file` setting, whatever argument it is given (course: a file reader bound to one file). | None needed (local file). |
| `resume_search` | Returns the résumé passages that best match a query, by meaning (course: a semantic search tool over the résumé file). Uses the provider's embeddings. | **Stand-in résumé search** (stand-in for search by meaning): splits the résumé into non-empty lines, scores each line by how many distinct query words (lower-cased, split on non-letters and non-digits) it contains as whole words, and returns up to 3 lines with a score above 0, highest first, ties in file order, joined by newlines; no match returns `no matching passage`. |
| `web_search` | C4b only. Searches Google through Serper and returns the results. | Not used offline. |

### 5.4 Model roles

| Role | Calls a model for | Course model |
|---|---|---|
| `researcher` | job research | `gpt-3.5-turbo` in code; `gpt-4-turbo` in the video |
| `profiler` | candidate profile | same |
| `resume_strategist` | tailored résumé | same |
| `interview_preparer` | interview materials | same |
| `embedder` | résumé search (C5a), memory (C9b) | not stated by the course |
| `manager` | C7c only: assigning and reviewing tasks | `gpt-3.5-turbo`, temperature 0.7 |
| `reviewer` | C8b only: QA review | same as the agents |

### 5.5 Settings

| Setting | Value | Source | Change this when … |
|---|---|---|---|
| `max_steps_per_task` | 10 | Addition (D5); the course relies on the framework's default limit. | your tasks need long tool chains and agents stop before finishing. |
| `resume_file` | `samples/resume.md` | Course bound the reader and search tools to one résumé file (`fake_resume.md`). | you use your own résumé. |
| `output_dir` | `output/` | Addition (D7). | you want results elsewhere. |
| result file names | `tailored_resume.md`, `interview_materials.md` | Course. | C1b: your team names its own files. |
| run log | every step of every agent is printed | Course set the highest log level when introducing it. | — (fixed; see R14) |
| `manager` temperature | 0.7 | Course (C7c only). | the chosen manager model rejects a temperature setting: drop it and say so in the checklist. |

---

## 6. Business rules

### What must stay true (the pattern card)

These hold for every option of every question.

1. **The work is split across several specialised agents, and each agent has its own role, goal and backstory.** No single agent does the whole job.
2. **Every piece of work is a task with a clear description and a stated expected output, and each task is assigned to an agent.**
3. **Results move between agents: a task works from the outputs of the tasks it depends on and does not start until they are done. The run finishes when every task is done.**
4. **One team definition serves any instance of the job: each run takes its named inputs and puts them in place wherever the agents and tasks use them.**

### Rules

- **R1** (card 1). The team has at least two agents, each with a non-empty role, goal and backstory, and no two agents share a role. The recommended team has exactly the four agents of 5.2, and each of its four tasks is done by a different agent. → T1, T2
- **R2** (card 2). Every task has a non-empty description, a non-empty expected output and an existing agent. A team definition that breaks this, or names a missing agent or a later or unknown task in `waits_for`, is rejected before any model call with an error naming the task. → T1, T3
- **R3** (card 3). A task receives the final outputs of every task in its `waits_for` in its prompt and does not start until all of them have finished. The run ends after every task has finished, and the run's returned result is the last task's output. → T5, T6, T7, L1
- **R4** (card 4). Every `{name}` placeholder in any agent or task text is replaced by the run's input of that name before the text reaches the model; no literal `{name}` reaches the model. The same `team.json` serves any set of inputs. → T8, T9
- **R5** (addition, D6). If a run's inputs lack a value for any placeholder used in `team.json`, the program exits with a non-zero status and an error naming each missing input, before any model call. → T10
- **R6** (course, C7a). Tasks marked "runs alongside next" run at the same time as the tasks that follow them, up to the next task that waits for them: `research` and `profile` overlap in time. → T11
- **R7** (course warning: initial context fades along a long chain). The interview task receives the research, profile and tailored-résumé outputs directly, not only the output of the task just before it. → T7
- **R8** (course demonstration: a tool fails mid-run). When a tool raises an error, the error message is returned to the agent as the tool's result and the run continues; it never stops the run. → T12
- **R9** (course: agents always attempt to get to an answer, guardrails stop endless loops). Every task ends with a non-empty result within `max_steps_per_task` steps, even if the agent keeps calling tools. → T13
- **R10** (course: give each agent only the tools its job needs). Each agent is offered exactly the tools listed for it in `team.json`, plus the framework's teammate tools when `may_delegate` is true; a task with `task_tools` restricts its agent to those tools for that task. → T14
- **R11** (course, C6a). An agent with `may_delegate: true` is offered tools to delegate work to, and ask a question of, each of its teammates. → T15
- **R12** (course). Each task with an `output_file` writes its final output, unchanged, to that file in `output_dir`; `output_dir` is created if missing. After the run the program prints the path of every result file. → T4, T16, L1
- **R13** (course: "don't make up any information"). The tailored résumé contains only facts found in the résumé, the code profile or the write-up. → L2
- **R14** (course). The run log shows every step of every agent, starting with the agent's role. → T17
- **R15** (course; 4.6). With a key present, real runs and `live` tests use the real provider; the offline tests need no key and make no network request. → T18, L1
- **R16** (course). The résumé reader returns the whole résumé; the résumé search returns the passages that best match a query; the page reader returns the text of the page at a given address. → T19, T20, L3, L4

---

## 7. Tests

### 7.1 Sample data

All facts below are invented for this spec (D3).

**`samples/inputs.json`**
```json
{
  "job_posting_url": "https://jobs.example.test/larkspur/backend-engineer",
  "github_url": "https://code.example.test/samrivera",
  "personal_writeup": "Sam has 12 years in software, the last 4 leading a payments team. Sam wants to move back to hands-on backend work in Go."
}
```

**`samples/inputs-b.json`**
```json
{
  "job_posting_url": "https://jobs.example.test/quillworks/data-engineer",
  "github_url": "https://code.example.test/alexchen",
  "personal_writeup": "Alex enjoys building data pipelines."
}
```

**`samples/inputs-missing.json`** — the same as `inputs.json` without `github_url`.

**`samples/team-bad.json`** — the recommended `team.json` with `expected_output` removed from task `profile`.

**`samples/pages/larkspur-backend-engineer.txt`** (served for `https://jobs.example.test/larkspur/backend-engineer`)
```
Larkspur Labs - Backend Engineer
We build logistics software.
Requirements:
- 5+ years building backend services
- Go
- PostgreSQL
- REST API design
- Docker
- Experience mentoring engineers
```

**`samples/pages/samrivera-profile.txt`** (served for `https://code.example.test/samrivera`)
```
samrivera - code profile
Repositories:
- ledgerline: payments ledger in Go with PostgreSQL
- trailmap: hiking map viewer in React
Languages: Go, Python, TypeScript
```

No other address is served. In particular `https://jobs.example.test/larkspur/backend-engineer-old` is **not** served (planted failure, R8).

**`samples/resume.md`**
```
# Sam Rivera
## Profile
Engineering leader with 12 years in software and 4 years leading teams. Known for growing engineers and running hiring.
## Experience
### Finch Payments - Engineering Manager (2019-2024)
- Led a team of 6 engineers; ran hiring and quarterly planning.
- Built the first version of the payments ledger service in Go on PostgreSQL.
### Corvid Health - Software Engineer (2012-2019)
- Designed REST APIs in Python for patient scheduling.
- Built an internal dashboard in React.
## Education
BSc Computer Science, Lakeview University
```
The résumé buries the hands-on skills the posting asks for under leadership wording, and has no Docker experience.

**Scripted stand-in model** (a stand-in for the real provider, used by every offline test). It identifies the calling agent from the role text in the prompt and gives that role's replies in order, one per model call within the task; it is safe to call from two tasks at once. Tool calls are written in whatever reply format the framework's agent loop expects, using the build's names for the tools. It records every prompt it receives, with the role and a timestamp.

| Role | Call 1 | Call 2 | Call 3 |
|---|---|---|---|
| Tech Job Researcher | use `page_reader` on `https://jobs.example.test/larkspur/backend-engineer-old` | use `page_reader` on `https://jobs.example.test/larkspur/backend-engineer` | final answer **A-research** |
| Personal Profiler for Engineers | use `page_reader` on `https://code.example.test/samrivera` | final answer **A-profile** | — |
| Resume Strategist for Engineers | use `resume_reader` | use `resume_search` with query `Go PostgreSQL` | final answer **A-resume** |
| Engineering Interview Preparer | final answer **A-interview** | — | — |

**A-research**
```
JOB REQUIREMENTS - Backend Engineer, Larkspur Labs
- Skills: Go; PostgreSQL; REST API design; Docker
- Experience: 5+ years building backend services
- Qualifications: experience mentoring engineers
```
**A-profile**
```
PROFILE - Sam Rivera
- Skills: Go; PostgreSQL; React; Python
- Projects: ledgerline (Go payments ledger on PostgreSQL); trailmap (React)
- Experience: 12 years in software; 4 years leading teams
- Interests: hands-on backend work
- Communication style: concise
```
**A-resume**
```
# Sam Rivera - Backend Engineer
## Summary
Backend engineer with 12 years in software, building Go services on PostgreSQL.
## Skills
Go, PostgreSQL, REST API design, Python, React
## Experience
- Finch Payments, Engineering Manager (2019-2024): built the first version of the payments ledger service in Go on PostgreSQL; led a team of 6 engineers.
- Corvid Health, Software Engineer (2012-2019): designed REST APIs in Python.
## Education
BSc Computer Science, Lakeview University
```
**A-interview**
```
# Interview preparation - Sam Rivera, Backend Engineer at Larkspur Labs
1. Question: Walk us through the Go payments ledger you built at Finch Payments.
   Talking point: PostgreSQL design and transaction safety.
2. Question: How have you designed REST APIs?
   Talking point: the scheduling APIs at Corvid Health.
3. Question: Have you used Docker?
   Talking point: no production Docker experience yet; say how you would learn it.
```

**Looping script** (used only by T13): the Tech Job Researcher replies to every call with "use `page_reader` on `https://jobs.example.test/larkspur/backend-engineer`" and never gives a final answer. The other roles use the table above.

**Parallel check** (used only by T11): the stand-in page reader holds each fetch of a served page until a second fetch of a served page is in progress, or 5 seconds have passed, and records which happened. Errors for unserved addresses return at once.

Replay of the expected outcomes against these samples (with the recommended options and every default in force): the researcher's call 1 raises `page not found: https://jobs.example.test/larkspur/backend-engineer-old`, which comes back to it as the tool result; call 2 returns the Larkspur page; the strategist's `resume_search` for `Go PostgreSQL` returns exactly the line `- Built the first version of the payments ledger service in Go on PostgreSQL.` (the only line containing either word); the two result files hold A-resume and A-interview; the run's returned result is A-interview.

### 7.2 Test table

Offline unless marked `live`. Every offline test uses the scripted stand-in model, the stand-in page reader and the stand-in résumé search.

| Test | Given | When | Then | Rules |
|---|---|---|---|---|
| T1 | a fresh checkout | `team.json` is loaded | it validates against 5.2; it has exactly the four agents of 5.2 with those roles, each with non-empty goal and backstory; each of its four tasks has a non-empty description and expected output and names a different agent | R1, R2 |
| T2 | `samples/inputs.json` | the team runs | the stand-in model recorded final answers from all four roles (four distinct roles) | R1 |
| T3 | `samples/team-bad.json` | the program loads it | it exits non-zero with an error naming task `profile` and `expected_output`; the stand-in model recorded zero calls | R2 |
| T4 | a fresh checkout with no `output/` folder | the team runs on `samples/inputs.json` | `output/` exists and holds `tailored_resume.md` and `interview_materials.md` | R12 |
| T5 | `samples/inputs.json` | the team runs | the strategist's first prompt contains the line `- Skills: Go; PostgreSQL; REST API design; Docker` (A-research) and `- Projects: ledgerline (Go payments ledger on PostgreSQL); trailmap (React)` (A-profile); its first prompt's timestamp is later than the researcher's and the profiler's final-answer timestamps | R3 |
| T6 | `samples/inputs.json` | the team runs | the program returns only after the interview task has finished; the returned result equals A-interview; both result files exist at that moment | R3 |
| T7 | `samples/inputs.json` | the team runs | the interview preparer's first prompt contains A-research's Skills line, A-profile's Projects line and A-resume's line `Backend engineer with 12 years in software, building Go services on PostgreSQL.` | R3, R7 |
| T8 | `samples/inputs.json` | the team runs | no recorded prompt contains `{job_posting_url}`, `{github_url}` or `{personal_writeup}`; the researcher's first prompt contains `https://jobs.example.test/larkspur/backend-engineer`; the profiler's first prompt contains `https://code.example.test/samrivera` and `Sam wants to move back to hands-on backend work in Go.` | R4 |
| T9 | `samples/inputs-b.json` and the same `team.json` | the team runs | the researcher's first prompt contains `https://jobs.example.test/quillworks/data-engineer` and not `larkspur/backend-engineer`; the profiler's first prompt contains `https://code.example.test/alexchen` and `Alex enjoys building data pipelines.` and not `samrivera` | R4 |
| T10 | `samples/inputs-missing.json` | the program runs | it exits non-zero with an error naming `github_url`; the stand-in model recorded zero calls; `output/` holds no new files | R5 |
| T11 | the parallel check on | the team runs on `samples/inputs.json` | both held fetches (Larkspur page, Sam Rivera profile) were released by the other fetch, not by the 5-second timeout; the profile task's first model call is earlier than the research task's final answer | R6 |
| T12 | `samples/inputs.json` (planted unserved address) | the team runs | the researcher's second prompt contains `page not found: https://jobs.example.test/larkspur/backend-engineer-old`; the run completes; both result files are written | R8 |
| T13 | the looping script | the team runs on `samples/inputs.json` | the run completes; the research task's result is non-empty; the researcher made at most 12 model calls (the 10-step limit plus up to 2 closing calls the framework may make); both result files are written | R9 |
| T14 | the recommended `team.json` | the team is built | the researcher is offered `page_reader` and the framework's teammate tools, nothing else; the other three are offered `page_reader`, `resume_reader`, `resume_search` and the teammate tools, nothing else; no task has `task_tools` | R10 |
| T15 | the recommended `team.json` | the team is built | each agent is offered a tool to delegate work to a teammate and a tool to ask a teammate a question, and those tools name the other three roles | R11 |
| T16 | `samples/inputs.json` | the team runs | `output/tailored_resume.md` equals A-resume and `output/interview_materials.md` equals A-interview (ignoring trailing whitespace); standard output contains both file paths | R12 |
| T17 | `samples/inputs.json` | the team runs | the run log contains each of the four role names, each before that agent's first tool call or answer | R14 |
| T18 | `OPENAI_API_KEY` and `SERPER_API_KEY` unset (a dummy key only if the framework refuses to start without one) and network blocked | the offline suite runs | every offline test passes and no request leaves the machine | R15 |
| T19 | `samples/resume.md` | `resume_reader` is called, with and without an argument | it returns the whole résumé text both times | R16 |
| T20 | the stand-in résumé search over `samples/resume.md` | queried with `Go PostgreSQL`, then with `kubernetes` | the first returns exactly `- Built the first version of the payments ledger service in Go on PostgreSQL.`; the second returns `no matching passage` | R16 |
| L1 `live` | a real key, the real model, the stand-in page reader, the real résumé search | the team runs on `samples/inputs.json` | the run completes; both result files are non-empty; the tailored résumé contains `Go` and `PostgreSQL` | R3, R12, R15 |
| L2 `live` | the result of L1 | the tailored résumé is read | its skills section does not list Docker; the only employers it names are Finch Payments and Corvid Health | R13 |
| L3 `live` | the real résumé search over `samples/resume.md` | queried with `payments ledger database` | the result contains `ledger` | R16 |
| L4 `live` | the real page reader, network access | it reads `https://example.com` | the text contains `Example Domain` | R16 |

---

## 8. Standing permissions

- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in, in code and in the run log; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has produced results; anything that sends data to a third party beyond the chosen model provider (and Serper under C4b).
- **Never:** invent provenance; let the program answer when it should say it does not know (a missing page is reported as missing, not filled in); change sample data to make a test pass; commit secrets.

---

## 9. Test plan

1. Install: `python -m pip install crewai==0.28.8 crewai_tools==0.1.6 langchain_community==0.0.29 pydantic python-dotenv pytest` (add `langchain_openai` for C7c).
2. Offline suite (no key, no network): `python -m pytest tests -m "not live" -v`.
3. Live suite (needs `OPENAI_API_KEY`; runs automatically when the key is set): `python -m pytest tests -m live -v`.
4. Real run: `python -m crew_app run --inputs samples/inputs.json`, then open the two printed files.
5. For every chosen option that is not recommended, turn its "what to check" sentence from section 1 into a test, run it, and report it.
6. Report a result for every test with evidence (test output, file paths). "Should pass" counts as not run. Adjust the recommended tests to the chosen options (for example, under C5b, T14 and T20 drop `resume_search`; under C7b, T11 is replaced by C7b's check; under C1b, the sample data and scripted replies are rewritten for the person's team and every test is re-pointed at them).
7. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.
8. Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

---

## 10. Background notes

### The program
A program that takes a few named inputs for one job, runs a team of specialised AI agents through a set of defined tasks, passes each task's result on to the tasks that depend on it, and returns the finished results. Stages:

`take inputs → fill in the team → gather (in parallel) → combine → write results`

1. **Take inputs:** a run is one instance of the job; its named inputs are all that changes between runs.
2. **Fill in the team:** the inputs are put in place in every agent's and task's text, so one team definition serves any instance.
3. **Gather, in parallel:** independent agents (job researcher, profiler) collect facts with tools at the same time, because neither needs the other's result.
4. **Combine:** a dependent task (the résumé rewrite) waits for every task it depends on and works from their outputs.
5. **Write results:** later tasks (the interview notes) work from all earlier outputs; tasks that own a result file write it, and the run ends when every task is done.

The course's example (one candidate, one job posting) is the sample instance; the job-application team is the recommended build of the program.

### Failures
- **A tool fails mid-run (demonstrated, Lesson 9).** *What you see:* an agent uses a tool the wrong way (in the course, the file reader on a web address) and the tool raises an error. *Why:* the model chooses tool arguments loosely. *How the spec prevents it:* the error goes back to the agent as the tool's result and the run continues, so the agent can correct itself. *Enforced by* R8, planted unserved address in 7.1, T12.
- **Initial context fades along a long chain (warned, Lesson 14).** *What you see:* later tasks lose sight of the original goal and inputs. *Why:* in a sequence, each task mostly sees the task before it. *How the spec prevents it:* the interview task receives all three earlier outputs directly. *Enforced by* R7, T7.
- **Agents loop or never answer (warned, Lessons 5 and 7).** *What you see:* an agent keeps calling the same tool. *Why:* weaker models in particular get stuck; the course says early framework versions had this problem. *How the spec prevents it:* a step limit, after which the agent must answer. *Enforced by* R9, T13.
- **Too many tools confuse an agent (warned, Lesson 5).** *What you see:* the agent picks the wrong tool or none. *How the spec prevents it:* each agent gets exactly its listed tools. *Enforced by* R10, T14.
- **Made-up résumé content (warned in the task text: "don't make up any information").** *Enforced by* R13, L2 (needs a real model).

### Why the questions are what they are
- **C1:** the course built six teams on the same pattern (article writing, customer support, sales outreach, event planning, financial analysis, job applications) and invited learners to bring their own topic and inputs, so a learner's own job is a real path.
- **C2:** the final team reads web pages and a résumé file; another lesson's team read a local folder of instruction files; the first team used no tools at all. These are the three source situations.
- **C3:** the course ran OpenAI models and showed how to plug in Hugging Face, Mistral, Cohere and local models through Ollama; it warned that smaller and open-source models struggle with tools.
- **C4:** every agent in the final team had Serper search, which needs its own key; the course says many other search tools would also do.
- **C5:** the final team had both a whole-file reader and a search-by-meaning tool over the same résumé.
- **C6:** the final team's agents were left at the framework default, which allows delegation. The course argues cooperation improves results and also says whether an agent delegates is the model's call, not yours.
- **C7:** the course taught three processes: one after another (its first team), parallel where independent (event planning and the final team), and a manager-led hierarchy (financial analysis), where the manager keeps the goal in view, delegates and reviews. The financial run "will take some time".
- **C8:** the reviewer comes from the customer-support team (Lesson 6); the instructor recommends adding a QA agent "into whatever multi-agent systems that you do". The final team has none, so the recommended build follows it (4.1).
- **C9:** memory comes from the customer-support and outreach teams; the course says it makes agents more reliable and self-improving across runs. The final team does not turn it on.

### Subjects that are not questions
- **A single agent doing the whole job:** breaks card item 1 (5.2 test 1).
- **A task with no expected output:** breaks card item 2 (5.2 test 1).
- **Strict sequence where each task sees only the previous task's output:** breaks card item 3 when a task depends on an earlier, non-adjacent task (5.2 test 1). C7b keeps every dependency.
- **A different model per agent** (course: a researcher on one model, a writer on another): already covered by the gate's one-model-line-per-role checklist, so no question is needed.
- **Human feedback before a task finishes** (Lessons 11–12): a component from another lesson that is not on the pattern card's "offered" list and does not change a stage (section 3.3).
- **Structured output as a typed object or JSON file** (Lesson 12): the course used it to hand agent output to other code. The final results are documents for a person, and grafting onto other code is not designed in this guide.
- **Task callbacks** (Lesson 11): named only, never built; not on the card.
- **Tool result caching across agents** (Lesson 8): framework behaviour that is always on. No learner situation calls for turning it off (5.2 test 3).
- **Task-level versus agent-level tools** (Lesson 6): supported by `task_tools` in `team.json` for C1b teams; the final team uses agent-level tools only.
- **Custom tools** (Lesson 9: a tool class with a name, a description and a run function): the stand-ins are built this way, and C1b teams add their own data sources this way.
- **Log detail level:** fixed at "every step". No learner project changes it (5.2 test 3).
- **Deploying the team as a hosted API** (Lesson 17, the vendor's beta platform): outside the program, needs an account you apply for, and integration is not designed in this guide.
- **The model used by the tests:** never asked; the tests run offline on the stand-ins, and the `live` tests run when a key is present.

### Where picked values came from
- **Model:** `gpt-3.5-turbo` (all six notebooks; Lesson 4 transcript: "let's make sure that they're running from GPT-3.5 turbo") versus `gpt-4-turbo` (Lessons 15 and 16 video; Lesson 9 video says "GPT-4"; notebooks note "The video uses gpt-4-turbo"). Rule 4.2(1), the value stated when the concept is introduced (Lesson 4), picks `gpt-3.5-turbo` as the fallback id. Lesson 4 also says the framework's default was GPT-4.
- **Log level:** `verbose=2` (Lessons 4, 6, 9 notebooks; Lesson 4: "we are going to set the highest number possible") versus `verbose=True` (Lessons 12, 15, 16 notebooks). Rule 4.2(1) picks the highest level.
- **Delegation:** off for every agent in Lesson 4; off for the support agent and default (on) for the QA agent in Lesson 6, where the concept is introduced; default (on) in the final team. Rule 4.2(1) and the final team agree: on.
- **Memory:** on in Lessons 6 and 9; off in Lessons 4, 12, 15 and the final team. It is a whole part, so it is a question (C9); the final team (4.1) sets its recommended option.
- **Parallel tasks and dependencies:** the research and profile tasks run alongside the next; the résumé task waits for both; the interview task waits for all three (Lesson 16 notebook and transcript).
- **Result files:** `tailored_resume.md`, `interview_materials.md` (Lesson 16 notebook).
- **Résumé tools bound to one file:** Lesson 16 notebook (`fake_resume.md`).
- **Manager temperature 0.7:** Lesson 15 notebook.
- **Pinned versions:** `crewai==0.28.8 crewai_tools==0.1.6 langchain_community==0.0.29` (install line in every notebook). A slide shows documentation for crewAI v0.22.4 (slide-only; the install line wins).
- **Step limit 10, output folder, missing-input check, `team.json`:** additions (D4–D7).
- **Other disagreements recorded:** the Lesson 16 transcript says the profiler compares the résumé with the posting; the notebook's profile task uses the code profile and write-up (the notebook is followed). The transcript says "among our three agents, all of them have access" to the four tools; in the notebook the researcher has only search and scraping (the notebook is followed). A slide calls the final team "your first multi-agent system"; the transcript calls it the most complex (slide-only, so it loses).

### Behaviour of the course code to keep in mind
- In the event-planning lesson, a parallel task's output file appeared up to 45 seconds after the run returned. It does not affect this build (both result files come from tasks that do not run alongside others), but under C1b a result file from a task that runs alongside others may need the same wait.
- Leaving delegation unset means delegation is allowed (course notebook note, Lesson 6).

### Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports:
`crewai` `Agent`, `Task`, `Crew`, `Process`, `Process.hierarchical`, `manager_llm`, `kickoff(inputs=...)`, agent fields `role`, `goal`, `backstory`, `tools`, `allow_delegation`, `verbose`, `llm`; task fields `description`, `expected_output`, `agent`, `tools`, `context`, `async_execution`, `output_file`, `output_json`, `output_pydantic`, `human_input`; crew fields `memory`, `verbose` (integer 1–2 or boolean in the course's version); `crewai_tools` `ScrapeWebsiteTool` (with `website_url`), `SerperDevTool`, `WebsiteSearchTool`, `FileReadTool` (with `file_path`), `DirectoryReadTool` (with `directory`), `MDXSearchTool` (with `mdx`), `BaseTool` (custom tools: `name`, `description`, `_run`); `langchain_openai.ChatOpenAI`; `langchain_community` `HuggingFaceHub`, `ChatCohere`; environment variables `OPENAI_API_KEY`, `OPENAI_MODEL_NAME`, `OPENAI_API_BASE`, `SERPER_API_KEY`, `COHERE_API_KEY`. Models: `gpt-3.5-turbo`, `gpt-4-turbo`, `gpt-4`, `mistral-small`, `HuggingFaceH4/zephyr-7b-beta`, Llama 3 70B. If a current model rejects a request parameter the course set (for example `temperature` on the manager), drop it and note it in the checklist.

### Course names
| Course name | Spec term | Binding? |
|---|---|---|
| `job_posting_url`, `github_url`, `personal_writeup` | run inputs | yes |
| `researcher`, `profiler`, `resume_strategist`, `interview_preparer` | agent ids | yes |
| `research_task`, `profile_task`, `resume_strategy_task`, `interview_preparation_task` | task ids `research`, `profile`, `resume_strategy`, `interview_preparation` | ids as in this spec |
| `scrape_tool`, `read_resume`, `semantic_search_resume`, `search_tool` | `page_reader`, `resume_reader`, `resume_search`, `web_search` | ids as in this spec |
| `fake_resume.md` | `samples/resume.md` (`resume_file`) | no |
| `tailored_resume.md`, `interview_materials.md` | result files | yes |
| `async_execution=True`, `context=[...]` | "runs alongside next", `waits_for` | behaviour binding |
| crew, kickoff | team, run | no |

### Lesson map (transcript numbering)
1 Introduction — the course's building blocks and processes. 2 Overview — the job-application example (posting, résumé, four agents and their tools, before/after); agentic versus rule-based automation. 3 AI Agents — agents, tools, multi-agent systems, per-agent models. 4 Create agents to research and write an article — agents, tasks, crew, sequential order, input placeholders, the model setting and its alternatives (C3, C7b, C2c). 5 Key elements of AI agents — role playing, focus, tools, cooperation, guardrails, memory (failures, C9). 6 Multi agent customer support automation — delegation, the QA reviewer pattern, task-level tools, memory flag (C6, C8, C9). 7 Mental framework for agent creation — think like a manager hiring people; specific role names. 8 Key elements of agent tools — versatile, fault-tolerant, cached tools; LangChain tools. 9 Tools for a customer outreach campaign — directory and file readers, custom tool, the failing-tool demonstration (R8), caching, search key. 10 Recap of tools. 11 Key elements of well defined tasks — description and expected output required; optional task features. 12 Automate event planning — parallel tasks, human input, typed output, output files. 13 Recap on tasks. 14 Multi agent collaboration — processes, context fading (R7), hierarchical manager. 15 Multi agent collaboration for financial analysis — the hierarchical run (C7c), manager model and temperature. 16 Build a crew to tailor job applications — the final end-to-end program: the recommended build. 17 Next steps — vendor resources and hosted platform (not used). 18 Conclusion.

Slides: both decks' descriptions were read. A slide the instructor narrates counted like that lesson's transcript; slide-only content counted less and lost where it disagreed (the "first multi-agent system" subtitle; the documentation version shown on a slide).

Nothing in this spec requires access to the course.

---

*Spec v2-draft · Multi AI Agent Systems with crewAI · résumé-tailoring agent team · when the build agent does something unexpected, add the missing constraint here and re-run.*
