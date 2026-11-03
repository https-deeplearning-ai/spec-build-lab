# Spec: a crew of specialised AI agents for one job

**What you're building:** a program that takes a few named inputs for one job, runs a team of specialised AI agents through a set of defined tasks, passes each task's result on to the tasks that depend on it, and returns the finished results. By default it is the course's job-application crew: you give it a link to a job posting, a link to your public code profile, a short write-up about yourself and your resume file. Four agents then go to work, two of them at the same time. You get back a tailored resume and a set of interview questions and talking points, written as two markdown files.

**What the recommended build needs to run:** an OpenAI API key (used by the agents and by the resume's search-by-meaning), network access to read the job posting and profile pages, and installing the Python packages.

**Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once `OPENAI_API_KEY` is set and are skipped until then; that is not a failure.

This file is self-contained: everything the build needs is here.

*Provenance: course "Multi AI Agent Systems with crewAI" · materials used: transcripts of all 18 lessons, the six course notebooks and their helper module, slide descriptions for both decks, and the owner-confirmed pattern card · generated 2026-10-31 · guide v2.9 (2026-10-31).*

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
C1–C4 are context (your job, how much of the crew, your model provider, how you start a run); C5–C12 follow the program's stages in order: the team (C5–C7), running the tasks (C8–C10), passing results on (C11) and returning the results (C12).

### C1. What job should the crew do?
- **C1a (Recommended - course default): Tailor a job application.** Four agents read a job posting, the applicant's public code profile, their write-up and their resume, then write a tailored resume and interview preparation notes. *Pick this when* you want the course's own crew running on your machine, or you are applying for jobs yourself. *Setup:* none beyond your model provider (C3).
- **C1b: Your own job.** You name the goal and the steps, the people you would hire for them (each with a role, goal and backstory), the tasks each one does with the output you expect, and the named inputs a run takes; every rule in this spec then applies to your team in place of the four. *Pick this when* your job is something else, for example writing an article on a topic, answering a customer's support question, drafting outreach to a sales lead, planning an event or analysing a stock; more agents and tasks mean longer runs and more model calls, so keep each agent on one thing and give it only the tools it needs, because agents offered too many tools pick badly, especially on smaller models. *Setup:* you write the team and the tasks; tools your job needs may need their own keys.
  - *What to check:* every agent has a role, goal and backstory, every task has a description, an expected output and one agent, and two runs with different input values each produce results that mention their own values.

### C2. How much of the job-application crew do you want?
*Ask only when C1 is C1a.*
- **C2a (Recommended - course default): All four agents.** Job researcher, profiler, resume strategist and interview preparer; results are the tailored resume and the interview materials. *Pick this when* you want both the resume and help preparing for the interview. *Setup:* none.
- **C2b: Without interview preparation.** The first three agents only; the run returns the tailored resume. *Pick this when* you only want the resume and would rather save the extra model calls. *Setup:* none.
  - *What to check:* the run writes only the tailored-resume file, and the tailored resume still comes from both the job research and the profile.
- **C2c: Without the profile step.** Job researcher, resume strategist and interview preparer; the run takes only the job posting link, and the strategist works from the job requirements and the resume alone. *Pick this when* you have no public code profile or write-up to add; the strategist then has less to draw on than the resume itself. *Setup:* none.
  - *What to check:* the only named input is the job posting link, and the strategist receives the job research result and reads the resume before writing.

### C3. Which model provider runs the agents?
- **C3a (Recommended - course default): OpenAI.** Every agent, and the resume's search-by-meaning, uses OpenAI models. *Pick this when* you have or can get an OpenAI key; the course ran every crew on OpenAI and moved to a larger model for crews that read a lot of web text, for its bigger context window. *Setup:* a paid OpenAI API key in `OPENAI_API_KEY`.
- **C3b: Another hosted provider.** The agents use another hosted provider's models, such as Mistral, Cohere or models hosted by Hugging Face. *Pick this when* you already pay for or prefer another provider. *Setup:* that provider's key; search-by-meaning (C6a) and memory (C11b) also need an embedding model, from that provider or run locally.
  - *What to check:* a live run with only that provider's key set completes and writes every result file.
- **C3c: A local model on your machine.** The agents use a model served on your own computer, such as Llama 3 through Ollama. *Pick this when* your data must not leave your machine or you want no per-call cost; smaller models get confused more easily, especially when offered many tools, so expect weaker tool use and less polished results. *Setup:* install a local model server and download a model (several GB); a local embedding model for C6a and C11b.
  - *What to check:* with no hosted-provider key set, a live run completes using only the local model and writes every result file.

### C4. How do you start a run?
- **C4a (Recommended): A command on your machine.** You run one command with a JSON file of the named inputs; it writes the result files and prints their paths. *Pick this when* you start the crew yourself. *Setup:* none.
- **C4b: A small local web service.** A local HTTP endpoint takes the named inputs as JSON and returns the results in its reply. *Pick this when* another program or a teammate needs to start runs; crews are often started through an API, and crewAI's own hosted platform turns crews into APIs, but it is a hand-picked beta needing a hosted account, so this option stays on your machine. *Setup:* none beyond a free local port.
  - *What to check:* posting the sample inputs to the endpoint returns every result, and a request missing an input is refused with that input's name.

### C5. Can the agents search the web?
- **C5a (Recommended): No search; agents read the pages they are given.** Agents read the job posting and code-profile links with the web-page reader. *Pick this when* your inputs already link the pages the agents need. *Setup:* none (network access only).
- **C5b (course default): Add web search.** Every agent also gets a web search tool backed by a Google search API service (the course used Serper, which gives free credits on sign-up). *Pick this when* the agents must find pages themselves, for example your inputs are names rather than links, or you want background on the company beyond the posting. *Setup:* a key for the search service in `SERPER_API_KEY`.
  - *What to check:* with the key set, a live run's job researcher makes at least one search, and two identical searches in one run reach the search service once.

### C6. How do agents read the document they work from (in the job-application crew, the resume)?
- **C6a (Recommended - course default): Read it whole and search it by meaning.** Agents can read the whole file, and can also ask for just the passages related to a question. *Pick this when* the document is long enough that agents should pull out only the relevant parts. *Setup:* an embedding model from your provider (with C3a, the same OpenAI key).
- **C6b: Read it whole only.** Agents read the whole file and nothing else. *Pick this when* the document is short, such as a one-page resume, or your provider has no embedding model. *Setup:* none.
  - *What to check:* no agent has a search-by-meaning tool, and the tailored resume still lists the job requirements found in the resume.

### C7. Should a reviewer check the result before it goes out?
- **C7a (Recommended - course default): No reviewer.** The resume strategist's tailored resume is the final one. *Pick this when* you read the results yourself before you use them. *Setup:* none.
- **C7b: Add a quality-assurance reviewer.** A fifth agent reviews the tailored resume against the job requirements and the profile, may send work back to the strategist to fix, and its revised version becomes the tailored resume. *Pick this when* the output reaches someone else, such as an employer or a customer, and should be fact-checked first; a final reviewer tends to improve results, at the cost of extra model calls and time, and it will not send work back on every run. *Setup:* none.
  - *What to check:* the reviewer's task runs after the strategist's, receives its draft, has no tools, and its output is what is written to the tailored-resume file and passed on to later tasks.

### C8. How are the tasks run?
- **C8a (Recommended - course default): In dependency order, independent tasks in parallel.** Tasks that need nothing from each other run at the same time; a task that depends on others waits for all of them. *Pick this when* you know ahead of time which task needs which results; running independent tasks together saves time. *Setup:* none.
- **C8b: One at a time, in list order.** Each task starts only after the one before it in the list has finished. *Pick this when* your tasks form a single chain, or your provider or local model cannot handle two requests at once; runs take longer, and along a long chain the original context fades as it passes from agent to agent. *Setup:* none.
  - *What to check:* every task starts only after the task before it in the list has finished, and each task still receives the results of every task it depends on.
- **C8c: A manager runs the team.** A manager agent, created for you, decides which agent does each task, passes on what earlier agents learned, and reviews results, asking for improvements when needed. *Pick this when* you want one coordinator to keep the original goal in view across many steps; runs make more model calls and take much longer. *Setup:* a model for the manager (the course used the same provider, at temperature 0.7).
  - *What to check:* the manager makes the run's first model call, every task's result is produced by one of the team's agents, and each task still receives the results of the tasks it depends on.

### C9. May agents hand work to teammates or ask them questions?
- **C9a (Recommended - course default): Yes.** During a task an agent may delegate part of the work to a teammate or ask one a question; the model decides at run time, so it will not happen on every run. *Pick this when* a task may benefit from another agent's knowledge or tools. *Setup:* none.
- **C9b: No delegation.** Each agent works alone on its own task and never hands off work or asks a teammate. *Pick this when* you want predictable runs with fewer model calls, with every agent just doing what it is told. *Setup:* none.
  - *What to check:* no agent is offered a way to hand off work or ask a teammate, and a run makes no delegation.

### C10. Should the run pause for your feedback?
*Ask only when C4 is C4a.*
- **C10a (Recommended - course default): No pauses.** The run goes from start to finish without stopping. *Pick this when* you are happy to read the results at the end. *Setup:* none.
- **C10b: Pause before chosen tasks finish.** Before a chosen task (for example the tailored resume) finishes, the run shows you its result and asks whether you like it; your answer is taken into account before the task's result is final. *Pick this when* you want to steer a step before later tasks build on it; the run waits for you each time. *Setup:* none.
  - *What to check:* the run stops at each chosen task and waits for typed feedback, and that task's final result is produced after the feedback is given.

### C11. Should the agents remember?
- **C11a (Recommended - course default): No memory.** Each run starts fresh, and results move only along task dependencies. *Pick this when* each run is a separate piece of work. *Setup:* none.
- **C11b: Turn memory on.** Agents share what they learn during a run (short-term), keep lessons from earlier runs in a local store (long-term), and track the people, companies and places discussed (entity). *Pick this when* you run the crew again and again on similar jobs and want it to improve with use; memory can make a large difference, but a single run does not need it. *Setup:* an embedding model and a local folder for the memory store.
  - *What to check:* after a first run a memory store exists on disk, and a second run's agents receive entries saved during the first run.

### C12. What form do the results take?
- **C12a (Recommended - course default): Markdown documents in files.** Each result is written as a markdown file. *Pick this when* people will read the results. *Setup:* none.
- **C12b: Structured data in JSON files.** Each result is checked against a declared set of fields and written as a JSON file. *Pick this when* another program will read the results, for example to save them in a database. *Setup:* none.
  - *What to check:* each result file parses as JSON and has every declared field with the declared type.

## 2. Departures from the course

The recommended build differs from the course in these places:

- **D1. Current library releases.** The course pinned crewai 0.28.8, crewai_tools 0.1.6 and langchain_community 0.0.29. The build uses current releases, because course-era versions often no longer install or work with current models.
- **D2. A current model.** The course's final crew ran on gpt-4-turbo in the video and on gpt-3.5-turbo in its notebook (the notebook's note says the platform could not run gpt-4-turbo). The build agent picks a current model at the gate, because model names go stale.
- **D3. Web search left out (C5a).** The course gave every agent of the final crew a web search tool. That tool needs a second paid key (Serper) on top of the model key. The recommended build's inputs are links, which the web-page reader already reads, so the search tool is left out. C5b restores it.
- **D4. A command-line program, not notebook cells.** The course ran the crew cell by cell in a notebook and wrote its result files to the working folder. The build is a program run by one command, and it writes its results to an `output/` folder. *(The folder is an addition.)*
- **D5. Inputs are checked before any model call.** *(Addition.)* The course passed its inputs straight to the crew. The build reads them from a JSON file and refuses missing, unknown or malformed inputs before any agent runs.
- **D6. Invented sample data.** The course used a made-up resume, a real job-posting link and a real public code profile. The build uses its own invented applicant, job pages and resume (section 7.1). The resume file is a setting (`samples/resume.md`), where the course hard-wired `fake_resume.md`.
- **D7. Offline test stand-ins.** *(Additions.)* The offline tests use a scripted stand-in model, saved web pages, and a keyword-overlap stand-in for search-by-meaning. The finished app uses the real model, the real web and the real embedding search.
- **D8. Delegation set explicitly.** In the final crew the course left delegation at its framework version's default, which the course states was on. The build turns it on explicitly (C9a), because current releases may default differently. The behaviour is the same.
- **D9. Agent and task wording rewritten.** Every role, goal, backstory, description and expected output keeps its purpose, but is written in this spec's own words. The strategy task also names the job-posting link, and the profile task puts the write-up on its own line, so the inputs reach those tasks visibly.

## 3. Objective

Given a job-posting link, a code-profile link and a personal write-up, a team of four specialised agents produces a tailored resume and interview materials, with each task working from the results of the tasks it depends on.

## 4. Tech stack and secrets

- **Language:** Python (current stable release). Package name `job_crew`; runnable as `python -m job_crew`.
- **Framework:** current releases of crewAI and its tools package (course pins in D1). Where the course leaves a behaviour to the framework (how an agent's loop ends, retries after a tool error, caching identical tool calls, passing earlier task results as context, running independent tasks in parallel), use the current release's behaviour. In `resolved-decisions.md`, note which feature of the release provides each one.
- **Tools (spec terms; course names in section 10.5):**
  - **web-page reader:** fetches a URL and returns its text. It may read any URL the agent chooses (setting S6). Its fetching is replaceable so the offline tests can serve saved pages.
  - **resume reader:** reads the resume file named by setting S3.
  - **resume search:** returns the passages of the resume file most related to a query, using an embedding model (C6a).
  - **web search:** C5b only.
- **Tests:** pytest, with a `live` marker for the tests that need a real model.
- **Secrets:** `OPENAI_API_KEY` (and `SERPER_API_KEY` for C5b) are read from the environment or from a local `.env` file. The course loaded its keys from `.env`. `.env` is listed in `.gitignore`. Keys are never printed or written to result files.

## 5. Contracts

### 5.1 Run inputs (JSON file passed with `--inputs`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["job_posting_url", "github_url", "personal_writeup"],
  "additionalProperties": false,
  "properties": {
    "job_posting_url": { "type": "string", "pattern": "^https?://\\S+$" },
    "github_url":      { "type": "string", "pattern": "^https?://\\S+$" },
    "personal_writeup": { "type": "string", "minLength": 1 }
  }
}
```

The input names are binding: they are the placeholders used in the agent and task texts. With C2c only `job_posting_url` is required and allowed. A refused input file stops the run before any model call. The command exits with code 2 and prints the name of each offending field.

### 5.2 Run result

```json
{
  "type": "object",
  "required": ["tailored_resume", "interview_materials"],
  "additionalProperties": false,
  "properties": {
    "tailored_resume":     { "type": "object", "required": ["path", "text"],
                             "properties": { "path": { "type": "string", "pattern": "tailored_resume\\.md$" },
                                             "text": { "type": "string", "minLength": 1 } } },
    "interview_materials": { "type": "object", "required": ["path", "text"],
                             "properties": { "path": { "type": "string", "pattern": "interview_materials\\.md$" },
                                             "text": { "type": "string", "minLength": 1 } } }
  }
}
```

The run function returns this object. The command prints the two paths, one per line, and exits 0. Any other failure exits non-zero (not 2) and names the task that failed. With C2b, `interview_materials` is absent.

### 5.3 The team (binding texts)

| Agent | Role | Goal | Backstory |
|---|---|---|---|
| A1 | Tech Job Researcher | Extract the skills, experience and qualifications a job posting asks for, so the application can be tailored to them. | You read job postings for a living and can tell which requirements matter to the employer. Your findings are what the rest of the team tailors the application to. |
| A2 | Personal Profiler for Engineers | Build a clear profile of the applicant from their public code profile, their own write-up and their resume. | You research engineers and turn scattered sources into one profile of skills, projects and interests that the resume strategist can rely on. |
| A3 | Resume Strategist for Engineers | Rewrite the applicant's resume so the skills and experience the job asks for stand out, without adding anything untrue. | You refine engineers' resumes so the most relevant experience is the first thing an employer sees, and you never claim a skill the applicant does not have. |
| A4 | Engineering Interview Preparer | Prepare interview questions and talking points that help the applicant show how they match the job. | You anticipate what interviewers will ask and help candidates answer with concrete examples from their own history. |

Tools per agent: A1 has the web-page reader. A2, A3 and A4 each have the web-page reader, the resume reader and the resume search. With C5b, every agent also has web search. With C6b, nobody has the resume search. Delegation is allowed for every agent (C9a).

### 5.4 The tasks (binding texts; `{…}` are the named inputs)

| Task | Agent | Description | Expected output | Depends on | Parallel | Result file |
|---|---|---|---|---|---|---|
| K1 research | A1 | Read the job posting at {job_posting_url}. Extract and group the skills, experience and qualifications it requires. | A structured list of the job's title, company and requirements. | — | yes | — |
| K2 profile | A2 | Compile a profile of the applicant from their code profile at {github_url}, their resume and their own write-up.<br>Personal write-up: {personal_writeup} | A profile listing the applicant's skills, projects, experience, interests and communication style. | — | yes | — |
| K3 strategy | A3 | Using the job requirements and the applicant profile from the earlier tasks, rewrite the resume so the most relevant skills and experience stand out. The job posting is at {job_posting_url}. Update every section, including the summary, work experience, skills and education. Do not make up any information. | An updated resume, in markdown, that highlights the applicant's qualifications and experience relevant to the job. | K1, K2 | no | `tailored_resume.md` |
| K4 interview | A4 | Using the job requirements, the applicant profile and the tailored resume, write interview questions and talking points that help the applicant show how the resume matches the job. | A markdown document of the key questions and talking points the applicant should prepare for a first interview. | K1, K2, K3 | no | `interview_materials.md` |

In K2, "Personal write-up: {personal_writeup}" sits on its own line.

### 5.5 Model roles

One model role per agent: `tech_job_researcher`, `personal_profiler`, `resume_strategist`, `interview_preparer`. The gate's model lines name one model for each role. They may all be the same model; the course used one model for every agent and said agents can run on different models. Extra roles exist only when their option is chosen: `manager` (C8c), `qa_reviewer` (C7b), and `embedder` (C6a's resume search, C11b's memory). Offline tests replace every role with the scripted stand-in (section 7.2).

### 5.6 Settings

| # | Setting | Value | Source | Change this when … |
|---|---|---|---|---|
| S1 | Model per role | chosen at the gate. Course: gpt-4-turbo (video) / gpt-3.5-turbo (notebook) | L9, L16 transcripts; L16 notebook | the instructor moved to the larger model "because we're going to be handling with more data", for its context window. Keep a model whose context window holds a scraped web page plus the earlier results. |
| S2 | Manager temperature (C8c only) | 0.7 | L15 notebook | your manager model rejects a temperature setting (see 10.4). |
| S3 | Resume file | `samples/resume.md` | course: `fake_resume.md` (L16 notebook) | you tailor an application for a different person. |
| S4 | Output folder | `output/` | addition (D4) | you want the results somewhere else. |
| S5 | Result file names | `tailored_resume.md`, `interview_materials.md` | L16 notebook | never for the recommended build; tests depend on them. |
| S6 | Web-page reader target | any URL the agent chooses | L16 notebook (reader without a fixed page) | you want an agent to read only one fixed page (the course did this in L6 to keep a support agent on one documentation page). |
| S7 | Verbose step log | on | L16 notebook (`True`); L4 used level 2 | you want a quiet run. |
| S8 | Cache identical tool calls within a run | on | framework behaviour the course describes (L8, L9) | not for this program (see 10.3). |
| S9 | Stand-in reply delay (tests only) | 0.5 s for A1 and A2 replies | addition | never; T7 depends on it. |

## 6. Business rules

### 6.1 What must stay true (the course's pattern card)

- **M1.** The work is split across several specialised agents, and each agent has its own role, goal and backstory. No single agent does the whole job. → T1
- **M2.** Every piece of work is a task with a clear description and a stated expected output, and each task is assigned to an agent. → T2
- **M3.** Results move between agents: a task works from the outputs of the tasks it depends on and does not start until they are done. The run finishes when every task is done. → T6, T7, T9
- **M4.** One team definition serves any instance of the job: each run takes its named inputs and puts them in place wherever the agents and tasks use them. → T3, T4

Every option in section 1 keeps M1–M4.

### 6.2 Rules

- **R1. The team.** The crew has exactly the four agents of 5.3, each with its own role, goal and backstory exactly as written, and each task goes to a different agent. → T1
- **R2. The tasks.** The crew has the four tasks of 5.4. Each has its description, its expected output and its agent exactly as written, and the agent working on a task receives both texts. → T2
- **R3. Inputs fill every placeholder.** Each run's named inputs replace every `{name}` in the agent and task texts before any agent works. No request to a model ever contains an unfilled placeholder. The same team definition serves any set of inputs. → T3, T4
- **R4. Inputs are checked first** *(addition)*. An input file that breaks the schema of 5.1 is refused before any model call. The refusal names every offending field, the command exits with code 2, and no result file is written. → T5
- **R5. Dependency order.** K1 and K2 depend on nothing and run at the same time. K3 starts only after both K1 and K2 have finished, and it receives both results. K4 starts only after K1, K2 and K3 have finished, and it receives all three results. → T6, T7
- **R6. Results.** K3's result is written to `tailored_resume.md` and K4's to `interview_materials.md` in the output folder (S4), which is created if missing. The run returns only after every task has finished and both files hold their full content. The returned object (5.2) carries each file's path and text, and the text equals the file's content. → T8, T9, T18
- **R7. Tools per agent.** Each agent has exactly the tools listed in 5.3. → T10
- **R8. A tool error does not stop the run.** When a tool call fails, for example the resume reader is asked to read a web address, the agent gets another turn to choose differently, and the run carries on. *(The course says its framework provides this; the build relies on the framework, and the rule sets no message or format.)* → T11
- **R9. Identical tool calls run once.** Within one run, a tool called again with the same arguments, even by a different agent, does not repeat the external request. → T12
- **R10. A stuck agent does not run forever.** An agent that keeps repeating the same tool call does not keep the run going. The run ends on its own, with or without that task's result. *(The course says its framework provides this; the rule sets no limit or message.)* → T13
- **R11. Delegation is allowed** for every agent (C9a). → T14
- **R12. Model.** Offline tests use the scripted stand-in model and need no key. The finished app uses the chosen provider when its key is set. Tests that need a real model are marked `live` and are skipped when the key is missing. → T15, T16
- **R13. Step log.** With S7 on, the run prints a step log that names each agent as it works. → T17

## 7. Tests

### 7.1 Sample data (invented for this spec; no course data)

**`samples/resume.md`** (exact content):

```
# Mara Quinn

Engineering manager with 12 years in software, leading teams of up to 9 engineers across two offices.

Skills: Python, PostgreSQL, REST APIs, Docker, Airflow, team leadership

## Experience

Harbor Analytics: Engineering Manager, 2019-2025. Led the data platform group. Built the first REST APIs for the billing service in Python.

Northwind Labs: Senior Engineer, 2014-2019. Ran PostgreSQL migrations and packaged services with Docker.
```

**Saved web pages** in `samples/pages/`, mapped by `samples/pages/index.json`:

| URL | File | Exact content (one fact per line) |
|---|---|---|
| `https://jobs.example.test/lumen-tide/backend-engineer` | `backend-engineer.txt` | `TITLE: Backend Engineer` / `COMPANY: Lumen Tide` / `REQUIRED: Python, PostgreSQL, REST APIs, Docker, Kubernetes` / `ABOUT: Lumen Tide builds route planning software for ferry operators.` |
| `https://jobs.example.test/ostrava-grain/data-platform-engineer` | `data-platform-engineer.txt` | `TITLE: Data Platform Engineer` / `COMPANY: Ostrava Grain` / `REQUIRED: Python, Airflow, PostgreSQL` |
| `https://code.example.test/maraquinn` | `maraquinn.txt` | `NAME: Mara Quinn` / `PINNED: tidewatch (Python service exposing REST APIs over PostgreSQL)` |

**Input files:**
- `samples/inputs.json` (instance S1): `job_posting_url` = `https://jobs.example.test/lumen-tide/backend-engineer`, `github_url` = `https://code.example.test/maraquinn`, `personal_writeup` = `Mara is an engineering manager who still writes Python every week and wants to return to hands-on backend work.`
- `samples/inputs_2.json` (instance S2): the same, except `job_posting_url` = `https://jobs.example.test/ostrava-grain/data-platform-engineer`.

**Planted failure (from the course's tool-error demonstration):** the profiler's scripted first move asks the resume reader to read `https://code.example.test/maraquinn`, a web address that is not a file.

### 7.2 Stand-ins (all labelled stand-ins in code and output)

- **Saved-page fetcher** *(stand-in for the web)*. In offline tests the web-page reader fetches through this. It returns the saved file's text for a URL listed in `index.json` and fails with an error for any other URL. It counts how many times each URL was fetched.
- **Keyword resume search** *(stand-in for search-by-meaning)*. It splits the resume file into paragraphs at blank lines and returns the paragraph that shares the most lowercase words with the query; on a tie, the earliest one. For the query `skills` it returns `Skills: Python, PostgreSQL, REST APIs, Docker, Airflow, team leadership`.
- **Scripted model** *(stand-in for every model role)*. It recognises the agent by the role name in the request. In each task's conversation it counts the tool results it has received so far (n). It asks for tools in whatever form the framework's agent loop accepts, and it records every call: role, task, full request text, start and end time. Its replies:

| Agent | n | Reply |
|---|---|---|
| A1 | 0 | call the web-page reader with the first `http(s)://` URL in the request |
| A1 | ≥1 | final answer: `Job: <TITLE> at <COMPANY>` newline `Requirements: <REQUIRED>`, taken from the latest tool result's lines |
| A2 | 0 | call the resume reader with the first URL in the request as the file path (planted failure) |
| A2 | 1 | call the web-page reader with that same URL |
| A2 | 2 | call the resume search with the query `skills` |
| A2 | ≥3 | final answer: `Candidate GitHub: <PINNED from the page>` newline `Resume says: <the search result>` newline `Write-up: <rest of the request line that starts with "Personal write-up: ">` |
| A3 | 0 | call the web-page reader with the first URL in the request |
| A3 | 1 | call the resume reader with no file path |
| A3 | ≥2 | final answer, built as below |
| A4 | 0 | final answer, built as below (no tool call) |

A3's final answer:
- *name* is the resume's first line without `# `;
- *job* is the text after the first `Job: ` in the request;
- *requirements* is the text after the first `Requirements: ` in the request, split at `, `;
- a requirement *matches* when it appears, ignoring case, in the resume text from the latest tool result.

It writes `# Tailored resume: <name>`, a blank line, `## Matches for <job>`, one `- <requirement>` line for each match in order, a blank line, `## Not claimed`, and one `- <requirement>` line for each non-match, or `- none` when there is none.

A4's final answer:
- *job* is the text after `## Matches for ` in the request;
- the *matches* are the `- ` lines under that heading;
- the *gaps* are the `- ` lines under `## Not claimed`, except `- none`;
- the *talking point* is the text after `Candidate GitHub: `.

It writes `# Interview preparation: <job>`, a blank line, one `- Q: Walk us through a project where you used <m>.` line for each match, one `- Q: How would you get up to speed on <g>?` line for each gap, and `- Talking point: <talking point>`.

**Looping variant** (T13 only): A1 always replies with the n = 0 move; the other agents are unchanged.

### 7.3 Expected outcomes (replayed against the samples and the scripted replies)

Instance S1:
- K1 result: `Job: Backend Engineer at Lumen Tide` / `Requirements: Python, PostgreSQL, REST APIs, Docker, Kubernetes`
- K2 result: `Candidate GitHub: tidewatch (Python service exposing REST APIs over PostgreSQL)` / `Resume says: Skills: Python, PostgreSQL, REST APIs, Docker, Airflow, team leadership` / `Write-up: Mara is an engineering manager who still writes Python every week and wants to return to hands-on backend work.`
- `tailored_resume.md`:
```
# Tailored resume: Mara Quinn

## Matches for Backend Engineer at Lumen Tide
- Python
- PostgreSQL
- REST APIs
- Docker

## Not claimed
- Kubernetes
```
- `interview_materials.md`:
```
# Interview preparation: Backend Engineer at Lumen Tide

- Q: Walk us through a project where you used Python.
- Q: Walk us through a project where you used PostgreSQL.
- Q: Walk us through a project where you used REST APIs.
- Q: Walk us through a project where you used Docker.
- Q: How would you get up to speed on Kubernetes?
- Talking point: tidewatch (Python service exposing REST APIs over PostgreSQL)
```

Instance S2:
- K1 result: `Job: Data Platform Engineer at Ostrava Grain` / `Requirements: Python, Airflow, PostgreSQL`
- `tailored_resume.md`: `# Tailored resume: Mara Quinn`, blank line, `## Matches for Data Platform Engineer at Ostrava Grain`, `- Python`, `- Airflow`, `- PostgreSQL`, blank line, `## Not claimed`, `- none`.
- `interview_materials.md`: `# Interview preparation: Data Platform Engineer at Ostrava Grain`, blank line, the three `- Q: Walk us through a project where you used …` lines for Python, Airflow and PostgreSQL in that order, then `- Talking point: tidewatch (Python service exposing REST APIs over PostgreSQL)`.

File comparisons ignore trailing whitespace.

### 7.4 Test table

Unless a test says otherwise, every test runs offline with the stand-ins of 7.2, no `OPENAI_API_KEY`, and a fresh temporary output folder.

| ID | Rules | Given | When | Then |
|---|---|---|---|---|
| T1 | R1, M1 | the built crew | it is inspected, then run on S1 | it has exactly four distinct agents whose role, goal and backstory equal 5.3. Each agent's first request contains its own role, goal and backstory verbatim. K1–K4 are assigned to A1–A4, one each. |
| T2 | R2, M2 | the built crew | it is inspected, then run on S1 | each task has the description, expected output and agent of 5.4. Each task's first request contains its description, with the inputs filled in, and its expected output. |
| T3 | R3, M4 | `samples/inputs.json` | the run on S1 completes | A1's request contains `https://jobs.example.test/lumen-tide/backend-engineer`. A2's request contains `https://code.example.test/maraquinn` and the line `Personal write-up: Mara is an engineering manager who still writes Python every week and wants to return to hands-on backend work.` A3's request contains the job URL. No recorded request contains `{job_posting_url}`, `{github_url}` or `{personal_writeup}`. |
| T4 | R3, M4 | one built crew definition | it runs on S1, then on S2 | the first run's two files equal the S1 expectations and the second run's equal the S2 expectations. The second tailored resume ends with `- none`. |
| T5 | R4 | an input file with one fault: (a) no `github_url`; (b) an extra field `budget`; (c) `job_posting_url` = `jobs.example.test/x`; (d) `personal_writeup` = `""` | `python -m job_crew --inputs <file>` runs | the exit code is 2. The output names the field (`github_url`, `budget`, `job_posting_url`, `personal_writeup` respectively). The scripted model was called 0 times. No result file exists. |
| T6 | R5, M3 | S1 | the run completes | A3's first call starts after the last calls of both A1 and A2 have ended. A3's request contains the full K1 and K2 results of 7.3. A4's first call starts after A3's last call has ended, and its request contains the K1 and K2 results and the full tailored resume. |
| T7 | R5 | S1, with S9's 0.5 s delay | the run completes | A2's first call starts before A1's last call ends. |
| T8 | R6 | no `output/` folder | the run on S1 completes | `output/` exists and holds exactly `tailored_resume.md` and `interview_materials.md`, equal to the S1 expectations. |
| T9 | R6, M3 | S1 | the run function returns | the returned object matches 5.2. Read at once on return, with no waiting, both files exist with their full expected content, and each `text` equals its file's content. |
| T10 | R7 | the built crew | it is inspected | A1's tools are exactly {web-page reader}. A2's, A3's and A4's tools are each exactly {web-page reader, resume reader, resume search}. |
| T11 | R8 (planted) | S1, with the planted failure (A2's first move reads the URL as a file) | the run completes | the run did not stop. The K2 result equals 7.3, including the `PINNED` text that only the later page read supplies. The scripted model was called at least 4 times in K2. |
| T12 | R9 | S1 | the run completes | the saved-page fetcher fetched `https://jobs.example.test/lumen-tide/backend-engineer` exactly once, although A1 and A3 each asked for it with identical arguments. |
| T13 | R10 | S1, with the looping variant | the run is started | within 120 s the run ends on its own, either returning or raising an error that names K1. A1 was called fewer than 100 times. The fetcher fetched the job URL at most once. |
| T14 | R11 | the built crew | it is inspected | all four agents have delegation allowed. |
| T15 | R12 | `OPENAI_API_KEY` unset | the offline suite runs | every offline test passes, and the `live` tests are reported as skipped. |
| T16 | R12 (`live`) | `OPENAI_API_KEY` set; a local HTTP server on 127.0.0.1 serving the saved pages; inputs pointing at it, with S1's write-up | a real run completes | both files exist and are non-empty. The tailored resume contains `Python` and `PostgreSQL`. The interview materials contain at least one of the job's `REQUIRED` items. |
| T17 | R13 | S1, with S7 on | the run completes | the console output names each of the four roles at least once. |
| T18 | R6 | `JOB_CREW_OFFLINE=1` set *(addition: switches the program to the stand-ins of 7.2)* | `python -m job_crew --inputs samples/inputs.json` runs | the exit code is 0, the output lists two lines ending in `tailored_resume.md` and `interview_materials.md`, and those files equal the S1 expectations. |

## 8. Standing permissions

- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in, in code and in output; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has data; anything that sends data to a third party beyond the chosen model provider and the pages the inputs link to.
- **Never:** invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets.

## 9. Test plan

1. Install: `python -m pip install -U crewai crewai-tools pytest`, plus whatever the chosen options need.
2. Offline suite: `pytest -m "not live" -v`. Every test T1–T15, T17 and T18 must pass.
3. Live suite: `OPENAI_API_KEY=… pytest -m live -v`, which runs T16. Without the key it reports skipped, which is not a failure.
4. Demo without a key: `JOB_CREW_OFFLINE=1 python -m job_crew --inputs samples/inputs.json`.
5. Adjust the tests for the chosen options. Example: with C5b, T10 adds web search to every agent; with C8b, T7 is replaced by C8b's check. For each chosen non-recommended option, turn its "what to check" sentence from `resolved-decisions.md` into a test and run it.
6. Report one result per test with evidence: the test output and the paths of the files written. "Should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass, and each chosen option's check passes.
7. Finish with a diagram of the built app introduced by the sentence "This is the infra/structure diagram of this app".

## 10. Background notes (for the build agent)

### 10.1 The program
Stages, in order, each with the reason it exists:
`take inputs → build the team → define the tasks → fill in the inputs → run the tasks in dependency order → pass each result on → return the results`
1. **Take the named inputs.** One team must serve any instance of the job (M4).
2. **Build the team.** Each agent gets a role, goal and backstory, because agents perform better when role-playing, and focused agents do better than one agent doing everything (M1). Each agent also gets only the tools its job needs.
3. **Define the tasks.** Each task gets a description and an expected output, because the expected output forces you to say what you want back (M2).
4. **Fill in the inputs** wherever the agent and task texts use them (M4).
5. **Run the tasks in dependency order.** A task needs the results it builds on; independent tasks can run together to save time (M3).
6. **Pass each result on** to the tasks that depend on it, so later agents build on earlier work (M3).
7. **Return the results** as files and a returned object, so a person or program can use them.

The course's step log (verbose output) shows what ran; it is a setting, not a stage.

### 10.2 Failures
- **F1. An agent uses the wrong tool (demonstrated, L9).** *What you see:* an agent tries to read a website with the file-reading tool, and the tool raises an error. *Why:* agents choose tools from fuzzy inputs and sometimes pick the wrong one. *How the spec prevents harm:* the framework returns the error to the agent instead of stopping the run; the agent then tries another tool. The course stresses that a framework which lets the exception stop the run loses all the work done so far. *Enforced by* R8, the planted A2 move, and T11.
- **F2. An agent stuck repeating itself (warned, L5 and L7).** *What you see:* an agent uses the same tool over and over, or never reaches an answer; the course says this happened more with open-source models in early framework versions. *How prevented:* framework guardrails steer the agent toward an answer and stop endless loops. *Enforced by* R10 and T13.
- **F3. Results read before they are written (warned, L12 notebook).** *What you see:* the course told learners to wait about 45 seconds after a run before opening a file written by a parallel task, or they would see only the file's name. *How prevented:* the run returns only after every task has finished and every file is complete. *Enforced by* R6 and T9.
- **Not a failure, a cost (L14):** along a long one-at-a-time chain, the original context fades as it passes from agent to agent. This is carried in C8b's and C8c's "pick this when".
- **Note on variability (all notebooks):** models give different outputs for the same input. That is why exact outcomes are asserted only against the scripted stand-in.

### 10.3 Why the questions and settings are what they are
- **C1.** The course built six crews, with the job-application crew as its final, end-to-end one (L16). Its manager mental model (L7, L11) is how a learner designs their own job: start from the goal and the process, ask who you would hire, then what tasks you expect of each. The costs come from L5 (focus; too many tools confuse agents, worse with smaller models).
- **C2.** The course frames interview preparation as "a bonus" (L16). Leaving out the profile is the simpler path for an applicant with no public profile.
- **C3.** OpenAI was the course's provider throughout. The L4 notebook lists Hugging Face, Mistral and Cohere as alternatives and points to Ollama for local models; L3 says agents can run on different models, such as Llama 3 or GPT-4. The cost for small models comes from L5.
- **C4.** The course ran in notebooks, which the build never is. L12 mentions starting a crew through an API, and L17 shows crewAI's hosted platform turning crews into APIs (hand-picked beta).
- **C5.** The course used Serper search in every tool-using lesson after L6 and noted that other search tools would do. It is left out of the recommended build under the heavy-part rule (D3).
- **C6.** In L16 the course gave agents both a file reader and a search-by-meaning tool over the resume. The course does not say which embedding model that tool used, so the spec names none.
- **C7.** The pattern card offers it. In L6 the instructor recommends a final QA agent and lets it delegate back.
- **C8.** C8a is the L16 crew (two parallel tasks, then tasks that wait for them through declared dependencies). C8b is the default process from L4. C8c is L15's hierarchical process, where the framework creates the manager; the course said a future version would let you define the manager agent yourself, which is the same behaviour and not a separate option.
- **C9.** The L6 notebook states that delegation is on unless switched off. L15 turned it on for every agent; L4, L6 (support agent) and L9 switched it off for agents that should only do their own work.
- **C10.** L12 used human input on two tasks. It is conditional on C4a because a web service has no terminal to type into.
- **C11.** The pattern card offers it. Memory was on in L6 and L9 (one flag for short-term, long-term and entity memory); L9 adds "You don't necessarily need to if you don't need".
- **C12.** In L12 the course wrote a task's output as JSON checked against a declared model of fields, to bridge agent output into regular code.

**Subjects that are not questions:**
- *One agent doing the whole job:* fails test 1 (breaks M1).
- *Tasks without an expected output:* fails test 1 (breaks M2).
- *Running every task in parallel, dependencies included:* fails test 1 (breaks M3).
- *Custom tools (L9's sentiment tool, which always answers "positive"):* part of designing your own job (C1b); as a separate question it fails test 3, because no learner situation for the job-application crew needs one.
- *Reading a folder of instruction files (L9):* the same as custom tools; it fails test 3 outside C1b.
- *Giving tools to the agent or to the task (task tools override agent tools, L6):* fails test 3; it changes nothing the learner gets.
- *Stopping the run on a tool error (the alternative L9 describes):* fails test 3; no situation for this program makes losing the completed work the right choice, because reading pages and files is safe to retry.
- *Turning off caching:* fails test 3; no situation found where repeating an identical request in one run helps.
- *crewAI's hosted platform:* fails test 3 as a separate option, because a hand-picked beta is not a path a learner can count on; C4b covers starting runs through an API.
- *Task callbacks (listed once on an L11 slide):* not a candidate; the course names them without showing a use, and they change none of the program's stages.
- *LangChain tools:* a source of tools, not a choice.
- *The learner's data:* follows from C1; on its own it fails test 3.
- *A different model per agent:* a setting (S1, model roles).
- *A scraper confined to one page:* a setting (S6).
- *Verbose logs:* a setting (S7), not a stage.

**Where picked values came from:**
- *Model:* L16's transcript says gpt-4-turbo and its notebook uses gpt-3.5-turbo. Rule (1), the value the instructor states when introducing it, picks gpt-4-turbo: L9 introduces the move "to four" for its larger context window. The other value is recorded in D2.
- *Verbose:* L4 used level 2 and L16 used `True`; rule (2), the final app, picks `True`.
- *Manager temperature 0.7:* from L15, the only value given.

**Heavy parts (those needing a key, account or large download):**
- The OpenAI model needs a key: scripted stand-in in tests, real model in the app.
- Serper search needs a second key: left out (C5).
- The web-page reader needs network only: kept, with saved pages in offline tests and `live` for real pages.
- The resume reader is local: kept.
- Resume search needs an embedding model through the key the build already needs: kept, with a keyword stand-in in tests.

**Places where the course disagrees with itself:**
- L4's narration says crewAI agents run on GPT-4 by default, while the course set gpt-3.5-turbo.
- L3 says a multi-agent system gives "one single final answer", while the final crew returns two results; the pattern card settles this as "returns the finished results".
- A deck-only slide in L16 calls the job-application crew "your first multi-agent system", while the narration calls it the course's most complex crew. The narration wins.

### 10.4 Names that go stale
Treat these as search keywords against current documentation, not as guaranteed imports or ids:
- *Libraries:* crewai 0.28.8, crewai_tools 0.1.6, langchain_community 0.0.29.
- *Classes and settings:* `Agent`, `Task`, `Crew`, `Process`, `Process.hierarchical`, `manager_llm`, `allow_delegation`, `async_execution`, `context`, `output_file`, `output_json`, `human_input`, `memory=True`, `verbose=2`.
- *Tools:* `SerperDevTool`, `ScrapeWebsiteTool`, `FileReadTool`, `MDXSearchTool`, `DirectoryReadTool`, `WebsiteSearchTool`, and `BaseTool` imported from the tools package.
- *Model wiring:* `ChatOpenAI` from `langchain_openai`, the `OPENAI_MODEL_NAME` environment variable, `OPENAI_API_BASE`.
- *Models:* gpt-3.5-turbo, gpt-4-turbo, mistral-small, HuggingFaceH4/zephyr-7b-beta, `ChatCohere`.

The course set a temperature for its manager model (S2); some current model families reject a temperature parameter. If the chosen manager model does, leave S2 unset and record that in `resolved-decisions.md`.

### 10.5 Course names
| Course name | Spec term | Binding? |
|---|---|---|
| `job_posting_url`, `github_url`, `personal_writeup` | named inputs | yes |
| `tailored_resume.md`, `interview_materials.md` | result files | yes |
| `researcher`, `profiler`, `resume_strategist`, `interview_preparer` | A1–A4 (role names kept) | role names yes |
| `research_task`, `profile_task`, `resume_strategy_task`, `interview_preparation_task` | K1–K4 | no |
| `fake_resume.md` | resume file, S3 | no |
| `scrape_tool`, `read_resume`, `semantic_search_resume`, `search_tool` | web-page reader, resume reader, resume search, web search | no |
| `job_application_crew` | the crew | no |

### 10.6 Lesson map (transcript numbering)
1. Introduction: the multi-agent idea, roles, sequential, parallel and hierarchical work (10.1).
2. Overview: the job-application crew's goal and before/after resume, and the crew as a team with roles (C1).
3. AI Agents: what agents and multi-agent systems are; different models per agent (C3, S1); "one single final answer" (10.3, disagreements).
4. Create agents to research and write an article: agents, tasks, crews, placeholders filled at kickoff (M2, M4, R3); sequential by default (C8b); verbose level 2.
5. Key elements of AI agents: role-playing, focus, tools, cooperation, guardrails, memory (M1, F2, C11).
6. Multi agent customer support automation: the QA reviewer and delegation (C7, C9); tool scope (10.3); memory flag (C11); a page-restricted scraper (S6).
7. Mental framework for agent creation: think like a manager (C1b); guardrails and focus recap (F2).
8. Key elements of agent tools: versatile, fault-tolerant and cached tools (R8, R9); LangChain tools.
9. Tools for a customer outreach campaign: Serper (C5); custom and folder-reading tools (10.3); the tool-error demonstration (F1, R8, T11); caching (R9); the move to a larger model (S1).
10. Recap of tools.
11. Key elements of well defined tasks: description and expected output are mandatory (M2); task options (C10, C12, callbacks).
12. Automate event planning: JSON output (C12), human input (C10), parallel tasks (C8a), the result-file wait (F3).
13. Recap on tasks (M2).
14. Multi agent collaboration: processes, context fading in long chains (C8b), the hierarchical manager (C8c), collaboration under any process (C9).
15. Multi agent collaboration for financial analysis: the hierarchical crew, manager temperature (S2), different inputs give different behaviour (M4).
16. Build a crew to tailor job applications: the final end-to-end program and the recommended build (5.3, 5.4, R5, R6).
17. Next steps with AI agent systems: crewAI's hosted platform for API deployment (C4).
18. Conclusion: nothing used.

**Slides:** both decks were read through the slide descriptions. Narrated slides counted like their lesson's transcript; deck-only slides counted less and lost every disagreement (one recorded in 10.3). The notebooks' own numbering (L2–L7) is not the lesson numbering; the transcripts decide.

Nothing in this spec requires access to the course.

---

*Spec version 1 · course: Multi AI Agent Systems with crewAI · project: job_crew · when the build agent does something unexpected, add the missing constraint here and re-run.*
