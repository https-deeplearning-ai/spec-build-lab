# Spec: a team of specialised AI agents that works one job through to finished results

**What you're building:** a program that takes a few named inputs for one job, runs a team of specialised AI agents through a set of defined tasks, hands each task's result to the tasks that depend on it, and returns the finished results. By default the job is tailoring a job application: you give it a link to a job posting, a link to your GitHub profile, a short write-up about yourself and your resume file. You see four agents at work. One analyses the posting while another profiles you, both at the same time. A third rewrites your resume for that job, and a fourth writes interview questions and talking points. You get two Markdown files: `tailored_resume.md` and `interview_materials.md`.

**What the recommended build needs to run:** an OpenAI API key (`OPENAI_API_KEY`) for the agents' model and for the search over your resume; network access to fetch the job posting and GitHub pages you give it; no other account and no download beyond the Python packages.

**Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once `OPENAI_API_KEY` is set and are skipped until then; that is not a failure.

This file is self-contained: everything the build needs is here, and nothing in it requires access to the course.

*Provenance: course "Multi AI Agent Systems with crewAI" (crewAI with DeepLearning.AI); materials used: the six course notebooks and their helper module, the eighteen lesson transcripts, the slide descriptions of both slide decks, and the owner-confirmed pattern card (confirmed 2026-10-27, reconfirmed 2026-10-31); written 2026-10-31 with guide v2.9 (2026-10-31).*

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
   an OpenAI API key (`OPENAI_API_KEY`) and network access to the job posting and GitHub pages it reads), or **choose** question by
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
C1–C5 are about your project and setup (context); C6–C12 follow the program's stages in order.

### C1. What job should the agent team do?
- **C1a (Recommended - course default): Tailor a job application.** Four agents analyse a job posting, profile you from your GitHub page and write-up, rewrite your resume for that job, and write interview questions and talking points. *Pick this when* you want the course's full program working on your own machine, or you are applying for a job and want a resume aimed at one posting. *Setup:* an OpenAI API key.
- **C1b: Plan, write and edit an article.** The simplest team: a planner, a writer and an editor work in a straight line on a topic you name, with no tools, and you get one edited article in Markdown. *Pick this when* you want to see the pattern work with nothing to fetch or read, only a topic and a model. It is the smallest version of the pattern: no agent looks anything up, so the article rests on what the model already knows. *Setup:* an OpenAI API key.
  - *What to check:* with a topic as the only input, the planner's plan reaches the writer, the writer's draft reaches the editor, and `article.md` holds the editor's Markdown article.
- **C1c: Your own job.** You name the inputs, the specialists you would hire, their tasks and which task results to save; the program runs your team the same way. Examples: answering a customer's support question with a support agent and a reviewer, researching a sales lead and drafting outreach emails, planning an event, analysing a stock. *Pick this when* your job is not a job application and you can say who you would hire and what each person should hand in. *Setup:* an OpenAI API key, plus any account a tool you add needs.
  - *What to check:* your team file passes the program's validation, a run fills every placeholder with your inputs, and every task that names an output file writes it.

### C2. How does the team get the job posting?
*Ask only when C1 is C1a.*
- **C2a (Recommended - course default): A web link.** You give the posting's URL and the researcher agent fetches the page itself. *Pick this when* the posting is on a public page that opens without logging in. *Setup:* none.
- **C2b: A text file you paste the posting into.** You save the posting's text in a file and give its path; the researcher reads that file instead of fetching a page. *Pick this when* the posting sits behind a login, the site blocks automated fetching, or you only have the posting as an email or a PDF. *Setup:* none.
  - *What to check:* with the posting given as a file, the research task's result is built from that file's text and no web request is made for the posting.

### C3. What format is your resume in?
*Ask only when C1 is C1a.*
- **C3a (Recommended - course default): Markdown or plain text.** The agents read the resume file as it is. *Pick this when* your resume is already a `.md` or `.txt` file, or you are happy to paste it into one. *Setup:* none.
- **C3b: PDF or Word.** The program first takes the text out of your PDF or Word file, then the agents work from that text. *Pick this when* your resume only exists as a PDF or Word document. The text taken from a PDF can lose its layout (columns, tables), so check it once. *Setup:* a text-extraction package for PDF and Word files.
  - *What to check:* a sentence from the PDF or Word resume appears in the profiler's and the resume strategist's inputs, and the tailored resume is still written as Markdown.

### C4. Which model provider should the agents use?
- **C4a (Recommended - course default): OpenAI.** All agents, and the search over your resume, use OpenAI models. *Pick this when* you have, or can get, an OpenAI API key. *Setup:* an OpenAI API key.
- **C4b: Another hosted provider.** The agents use a different hosted provider, for example Mistral, Cohere, a Hugging Face endpoint or Anthropic; each agent can even run on a different model. *Pick this when* you already pay for another provider or your organisation requires one. The search over your resume still needs an embedding model, which some providers do not offer. *Setup:* that provider's API key, and an embedding model for the resume search.
  - *What to check:* every agent's calls go to the chosen provider, the resume search uses an embedding model the person has access to, and the offline tests still pass.
- **C4c: A local model on your own machine (for example through Ollama).** Nothing leaves your machine. *Pick this when* your resume must not be sent to a hosted service, or you have no API key. Smaller models struggle when an agent has many tools: they pick the wrong tool or skip one they need. Open-source models used to get stuck calling the same tool over and over. *Setup:* a local model server, a model download of several gigabytes, a machine that can run it, and a local embedding model for the resume search.
  - *What to check:* a full run on the sample inputs completes with no network call to a hosted model provider, and both result files are written.

### C5. How do you start a run?
- **C5a (Recommended): From the command line.** You run one command with an inputs file; the result files land in an output folder. *Pick this when* you are comfortable in a terminal or want to run it from scripts. *Setup:* none.
- **C5b: From a page in your browser on your own machine.** A small local web page has one field per named input and a start button, and shows links to the result files when the run ends. *Pick this when* you would rather fill in a form, or someone less used to terminals will use it on your machine. *Setup:* a small web-server package.
  - *What to check:* submitting the form with the sample inputs starts one run and the page shows links to both result files when it ends, and a missing field is refused before any model call.

### C6. Should the agents be able to search the web?
- **C6a (Recommended): No web search; agents read only the pages and files they are given.** The researcher fetches the posting link, the profiler fetches the GitHub link, and the resume comes from your file. *Pick this when* your inputs already point at everything the agents need. *Setup:* none.
- **C6b (course default): Agents can also search the web.** Every agent gets a web-search tool next to its other tools. *Pick this when* you want the agents to find things you did not link, for example more about the company or your public work. Each search is a paid request to a search service, and every extra tool gives an agent one more thing to choose between. *Setup:* a key for a web-search service, for example Serper, which gives free credits on sign-up.
  - *What to check:* the agents given search can call it and receive results, and with no search key set the program names the missing key before any model call.

### C7. How should the agents read your resume?
*Ask only when C1 is C1a.*
- **C7a (Recommended - course default): Read the whole file, and also search it by meaning.** The profiler, the resume strategist and the interview preparer can read the whole resume and can ask for the passages that match a question (for example "backend databases"). *Pick this when* your resume is long, or you want agents to find matching experience buried deep in it. *Setup:* none beyond the model key (the search uses an embedding model).
- **C7b: Read the whole file only.** Those agents get only the whole-file reader. *Pick this when* your resume is a page or two, or you run a small or local model: the course warns that too many tools confuse agents, especially smaller models. *Setup:* none.
  - *What to check:* no agent is offered the resume search tool, and the profile and strategy tasks still receive the resume's full text.

### C8. In what order should the tasks run?
- **C8a (Recommended - course default): A fixed plan where independent tasks run at the same time.** Tasks that depend on nothing start together; a task that depends on others waits until all of them are done and then works from their results. *Pick this when* you know which task needs which results; it finishes sooner than one task at a time. *Setup:* none.
- **C8b: One task at a time, in list order.** Each task starts only when the one before it is done. *Pick this when* you want logs that are easy to follow, or your provider limits how many requests you may send at once. It is slower. In a long chain, the course warns, the details of the first task slowly fade as results pass from agent to agent. *Setup:* none.
  - *What to check:* no task starts before the previous one in the list has finished, and each task still receives the results of the tasks it depends on.
- **C8c: A manager agent hands out the work and reviews it.** The program creates a manager that keeps the original goal in view, gives each task to the agent it thinks best, checks each result and can ask for improvements. *Pick this when* the order of the work is not fixed in advance, or you want one agent that remembers the overall goal and reviews everything. The course called this a long-running crew: it makes many more model calls, and the order is decided during the run. *Setup:* a model for the manager (same provider).
  - *What to check:* the manager hands every task to an agent, each task's result reaches the tasks that use it, and the run ends only after every task has a result.

### C9. Should the agents remember earlier steps and earlier runs?
- **C9a (Recommended - course default): No memory.** Each task works from its own instructions and the results it is handed; nothing is kept between runs. *Pick this when* each run is a separate job, or you do not want anything about the run kept on disk. *Setup:* none.
- **C9b: Memory within a run only.** While a run lasts, agents share what they have learned and the people, companies and places mentioned, so later agents can use facts earlier agents found. *Pick this when* your tasks overlap and later agents keep needing details earlier agents dug up. *Setup:* none beyond the model key (memory uses an embedding model).
  - *What to check:* a fact found by an earlier agent is available to a later agent in the same run, and a new run starts with no memory of the previous one.
- **C9c: Memory within and across runs.** As C9b, and after each task the agent also notes what it should have done better, kept in a local database so later runs improve. The course said memory can make more difference than everything else combined. *Pick this when* you will run the team many times on similar jobs and want it to get better with use. Results can change from run to run as memories build up, and the memories stay on your disk until you delete them. *Setup:* none beyond the model key; the memory database lives in a local folder.
  - *What to check:* after one run the memory store on disk exists and is not empty, a second run reads from it, and deleting the store resets it.

### C10. Should a reviewer check the results before they are returned?
- **C10a (Recommended - course default): No reviewer.** The resume strategist's result is the final tailored resume. *Pick this when* you will read and correct the results yourself before using them. *Setup:* none.
- **C10b: A quality-assurance reviewer agent checks the main result.** One more agent reviews the tailored resume (or, for your own job, your main result) against the earlier tasks' results, can send work back to the agent that wrote it, and its reviewed version becomes the final file. *Pick this when* the result goes to someone else, such as a recruiter or a customer, and should be fact-checked before it goes out. It adds at least one more model call per run, and more each time it sends work back. *Setup:* none.
  - *What to check:* the reviewer has its own role, goal and backstory, its review task runs after the main result exists and receives it together with the results it was built from, and the final file is the reviewer's output.

### C11. Should the program stop for your comments before finishing the main result?
- **C11a (Recommended - course default): No; the run goes straight through.** Every task finishes and every file is written without waiting for you. *Pick this when* you want to start it and come back to finished files. *Setup:* none.
- **C11b: Yes; it pauses before the main result is final.** Before the tailored resume (or, for your own job, your main result) is written, the program shows the draft and waits for your comments, and the agent applies them. *Pick this when* you want a say before the result is final, for example to keep a skill off your resume. Someone must be at the keyboard while it runs. *Setup:* none.
  - *What to check:* the run stops before the main result file is written, shows the draft, the comment typed in reply reaches the agent's next input, and the file is written only after that.

### C12. What form should the results take?
- **C12a (Recommended - course default): Markdown files.** Each saved result is a Markdown file. *Pick this when* a person will read the results. *Setup:* none.
- **C12b: Markdown files plus one result as JSON with fixed fields.** The first task's result is also saved as a JSON file in a fixed shape; for the job application, `job_requirements.json` with the job title, the company, and lists of must-have and nice-to-have requirements. *Pick this when* another program, a spreadsheet or a tracker will read that result. The agent has to fit its answer into the fields, which can drop nuance the text version keeps. *Setup:* none.
  - *What to check:* the JSON file is valid against its fixed shape and lists the same requirements as the text result.

---

## 2. Departures from the course

Each place the recommended build differs from what the course did, with its reason:

1. **Current library releases instead of the course's pinned ones.** The course pinned crewAI 0.28.8, crewAI tools 0.1.6 and LangChain community 0.0.29. Versions from that era often no longer install or work with current models.
2. **No web-search tool in the recommended build (C6a).** The course gave every agent of its final team a web-search tool (Serper), which needs its own key. The recommended build already gets the posting and the GitHub page as links and reads them with the keyless page-fetching tool, so search is left out and offered as C6b.
3. **The model.** The course's video ran its final team on GPT-4 Turbo; its notebooks ran GPT-3.5 Turbo because of the course platform's limits. Both are older models. The build agent picks a current model per role at the gate (section 0, step 5).
4. **A command-line program instead of notebook cells.** The course ran each team cell by cell in a notebook and displayed the results inline. The build is a program with a `run` command, an inputs file and an output folder (addition).
5. **The team is described in a data file that the program checks before running** (addition). The course wrote its agents and tasks directly in code. The file lets one definition serve any instance and lets the program refuse a team that breaks the pattern (section 6).
6. **The resume path is a setting** (addition). The course hard-coded its sample resume file.
7. **A run record, a `describe` command and refusal before any model call** for missing inputs, unknown inputs or a missing key (additions).
8. **Delegation is left to the current framework release's default.** The course's final team did not set whether agents may hand work to each other, so it got the framework's default of that era (allowed). The build agent writes in the checklist what the current release does.
9. **Own sample data.** The course used a made-up resume, a real job-board posting and a real GitHub profile. The recommended build uses a made-up candidate, posting and GitHub page whose facts are written in this spec (section 7.1), served from a local folder for the live test.
10. **Stand-ins for the offline tests** (additions, each labelled): a scripted stand-in model per agent, a stand-in page fetcher that reads local sample files, and a stand-in word-overlap resume search (section 7.1).
11. **The agents' and tasks' texts are written in this spec's own words.** The course's texts carry the same meaning; its spelling slips are not carried over.

---

## 3. Objective

Given the named inputs for one job, run a validated team of specialised agents through their tasks in dependency order and write each finished result to a file.

---

## 4. Tech stack, versions and secrets

- **Language:** Python, current release (3.11 or newer).
- **Agent framework:** crewAI and its tools package, current releases. The course used crewAI throughout and taught its agents, tasks, crews, processes and tools.
- **Other packages:** a YAML reader for the team file, pytest for the tests.
- **Framework behaviour left to the current release (4.7):** how an agent's loop ends, retries after a tool error, caching of repeated tool calls, delegation between agents, and how a task's dependencies' results reach it. In the checklist, the build agent notes in one line each how the current release provides these.
- **Secrets:** keys come from the environment, or from a `.env` file in the project folder that is read into the environment at start (the course did this). Never hard-coded, never logged, never written to the run record. `.env` is listed in `.gitignore`.
- **Stand-in switch:** when the environment variable `CREW_APP_STANDIN` holds the path of a scripted-replies file (section 7.1), the program swaps in the stand-ins: each agent's model becomes the scripted stand-in model, `scrape_website` becomes the stand-in page fetcher, and `search_resume` becomes the stand-in word-overlap search. No key is needed and no network call is made. Every stand-in is labelled as one in its own description.

---

## 5. Input/output contracts

### 5.1 Commands

- `python -m crew_app run --inputs <inputs.json> [--team team.yaml] [--resume <path>] [--out <dir>] [--quiet]` runs one job. Defaults: `--team team.yaml`, `--resume sample_data/resume.md`, `--out output`. It prints the path of each result file. Exit code 0 means completed. Exit code 2 means refused before any model call (invalid team, invalid inputs, missing key). Exit code 1 means the run started and failed.
- `python -m crew_app describe [--team team.yaml]` validates the team file. If it is invalid, it exits with 2 and prints each problem to stderr. If it is valid, it prints a JSON description: each agent's id, role and tools (each tool with its name and argument names), each task's id, agent, dependencies, whether it may run in parallel and its output file, and the declared input names.

### 5.2 Team file (`team.yaml`), validated against this schema

```json
{
  "type": "object",
  "required": ["inputs", "agents", "tasks"],
  "additionalProperties": false,
  "properties": {
    "verbose": {"type": "boolean", "default": true},
    "inputs": {"type": "array", "minItems": 1, "uniqueItems": true,
               "items": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"}},
    "agents": {"type": "array", "minItems": 2, "items": {
      "type": "object", "required": ["id", "role", "goal", "backstory", "tools"],
      "additionalProperties": false,
      "properties": {
        "id": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"},
        "role": {"type": "string", "minLength": 1},
        "goal": {"type": "string", "minLength": 1},
        "backstory": {"type": "string", "minLength": 1},
        "tools": {"type": "array", "items": {"enum": ["scrape_website", "read_resume", "search_resume"]}}
      }}},
    "tasks": {"type": "array", "minItems": 1, "items": {
      "type": "object", "required": ["id", "description", "expected_output", "agent"],
      "additionalProperties": false,
      "properties": {
        "id": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"},
        "description": {"type": "string", "minLength": 1},
        "expected_output": {"type": "string", "minLength": 1},
        "agent": {"type": "string"},
        "context": {"type": "array", "items": {"type": "string"}, "default": []},
        "parallel": {"type": "boolean", "default": false},
        "output_file": {"type": "string", "pattern": "^[A-Za-z0-9_.-]+\\.(md|json)$"}
      }}}
  }
}
```

Checks beyond the schema, all run before any model call (rules R1, R2, R5): ids unique; every task's `agent` names an existing agent; every agent is the agent of at least one task; every `context` entry names a task listed earlier; every `{name}` placeholder in any role, goal, backstory, description or expected output is a declared input; every declared input appears in at least one of those texts. Options extend the tool list (C6b adds a web-search tool, C2b a posting-file reader).

### 5.3 The recommended team (contents of `team.yaml`)

`verbose: true`. `inputs: [job_posting_url, github_url, personal_writeup]`.

| Agent id | Role (course name, binding) | Goal | Backstory | Tools |
|---|---|---|---|---|
| `researcher` | Tech Job Researcher | Analyse job postings thoroughly so applicants know exactly what the employer wants. | You are unmatched at reading job postings and pulling out the qualifications and skills employers seek; your analysis is the foundation for tailoring an application. | `scrape_website` |
| `profiler` | Personal Profiler for Engineers | Research job applicants in depth so they stand out in the job market. | You analyse and combine information from many sources into complete personal and professional profiles that ground every resume improvement. | `scrape_website`, `read_resume`, `search_resume` |
| `resume_strategist` | Resume Strategist for Engineers | Find the best ways to make a resume stand out for the job it targets. | You refine resumes with an eye for detail so the most relevant skills and experience match the job's requirements. | `scrape_website`, `read_resume`, `search_resume` |
| `interview_preparer` | Engineering Interview Preparer | Create interview questions and talking points from the resume and the job requirements. | You anticipate how interviews go and prepare candidates to address every aspect of the job with confidence. | `scrape_website`, `read_resume`, `search_resume` |

| Task id | Agent | Description must say | Expected output | Depends on (`context`) | Parallel | Output file |
|---|---|---|---|---|---|---|
| `research_task` | researcher | Analyse the job posting at `{job_posting_url}`; use the tools to get its content; pick out and group the required skills, experience and qualifications. | A structured list of the job's requirements: skills, qualifications and experience. | none | yes | none |
| `profile_task` | profiler | Compile a detailed personal and professional profile from the GitHub page at `{github_url}` and the write-up `{personal_writeup}`; use the tools to extract and combine information. | A full profile: skills, project experience, contributions, interests and communication style. | none | yes | none |
| `resume_strategy_task` | resume_strategist | Using the profile and job requirements from the earlier tasks, tailor the resume to highlight the most relevant areas; use the tools to read and adjust the resume; do not make up any information; update every section: summary, work experience, skills and education. | An updated resume that highlights the candidate's qualifications and experience relevant to the job. | `research_task`, `profile_task` | no | `tailored_resume.md` |
| `interview_preparation_task` | interview_preparer | Create potential interview questions and talking points based on the tailored resume and the job requirements, so the candidate can bring out the resume's main points and how they match the posting. | A document of key questions and talking points the candidate should prepare for the first interview. | `research_task`, `profile_task`, `resume_strategy_task` | no | `interview_materials.md` |

Tools (names are this spec's contract):
- `scrape_website(url)` fetches a web page and returns its visible text (the course's website-scraping tool).
- `read_resume()` returns the full text of the configured resume file. It takes no path: it can read only that one file, as the course confined its resume reader to one file.
- `search_resume(query)` returns the passages of the configured resume that match the query by meaning (the course's semantic search over the resume).

### 5.4 Inputs file (recommended team)

```json
{
  "type": "object",
  "required": ["job_posting_url", "github_url", "personal_writeup"],
  "additionalProperties": false,
  "properties": {
    "job_posting_url": {"type": "string", "pattern": "^https?://"},
    "github_url": {"type": "string", "pattern": "^https?://"},
    "personal_writeup": {"type": "string", "minLength": 1}
  }
}
```

In general, the inputs file is a JSON object whose keys are exactly the team file's declared `inputs`, each with a non-empty string value.

### 5.5 Outputs (in the `--out` folder, created if missing)

- One file per task that names an `output_file`, holding that task's final result as written by its agent.
- `run_record.json` (addition), written on completion and on failure:

```json
{
  "type": "object",
  "required": ["status", "inputs", "tasks", "error"],
  "properties": {
    "status": {"enum": ["completed", "failed"]},
    "inputs": {"type": "object"},
    "tasks": {"type": "array", "items": {
      "type": "object", "required": ["id", "agent_role", "output", "output_file"],
      "properties": {
        "id": {"type": "string"}, "agent_role": {"type": "string"},
        "output": {"type": ["string", "null"]}, "output_file": {"type": ["string", "null"]}}}},
    "error": {"type": ["string", "null"]}
  }
}
```

- With `CREW_APP_STANDIN` set, also `standin_log.jsonl` (test aid): one JSON object per stand-in model call, with `agent_role`, `call_index` (1-based, per agent), `received_at` and `replied_at` (seconds since the run started), `prompt_text` (all messages the stand-in received, joined) and `reply_kind` (`tool` or `final`).

### 5.6 Model roles

Each role calls a model; the gate's model line (section 0, step 5) names one current model per role:
- Tech Job Researcher
- Personal Profiler for Engineers
- Resume Strategist for Engineers
- Engineering Interview Preparer
- Resume search embedder (the embedding model behind `search_resume`)

The course ran every agent on one model (GPT-4 Turbo in the video, GPT-3.5 Turbo in the notebooks). Option roles appear only when chosen: the manager (C8c), the reviewer (C10b), the memory embedder (C9b, C9c).

### 5.7 Settings

| Setting | Value | Source | Change this when … |
|---|---|---|---|
| Model per role | picked at the gate | course: GPT-4 Turbo (video), GPT-3.5 Turbo (notebooks) | the chosen model is slow or costly for a role; the course noted different agents can run on different models |
| Model temperature | not set (provider default) | the course set none for its agents | the chosen model rejects or ignores it |
| `verbose` | `true` (`--quiet` turns it off for one run) | course final team: on | you only want the result files and no step-by-step log |
| `research_task.parallel`, `profile_task.parallel` | `true` | course final team ran both at the same time | your provider limits requests sent at once |
| Resume path (`--resume`) | `sample_data/resume.md` | addition (course hard-coded its sample resume) | always, to point at your own resume |
| Output folder (`--out`) | `output` | addition | you keep results for several jobs side by side |
| Result file names | `tailored_resume.md`, `interview_materials.md` | course | another program expects other names |
| Delegation between agents | current framework release's default | course left it to the framework (4.7) | you choose C10b, where the reviewer may send work back |

---

## 6. Business rules

### What must stay true (the course's pattern card; every option keeps every item)

1. **The work is split across several specialised agents, and each agent has its own role, goal and backstory.** No single agent does the whole job. → R1
2. **Every piece of work is a task with a clear description and a stated expected output, and each task is assigned to an agent.** → R2
3. **Results move between agents: a task works from the outputs of the tasks it depends on and does not start until they are done. The run finishes when every task is done.** → R3, R4
4. **One team definition serves any instance of the job: each run takes its named inputs and puts them in place wherever the agents and tasks use them.** → R5

### Rules

- **R1.** The team has at least two agents; each has a non-empty role, goal and backstory; each agent is the assigned agent of at least one task. A team file that breaks this is refused before any model call, with stderr naming the agent id and the problem. → T1, T2, T3, T4
- **R2.** Every task has a non-empty description, a non-empty expected output and one assigned agent that exists in the team. A team file that breaks this is refused before any model call, with stderr naming the task id and the problem. → T5
- **R3.** A task starts only after every task in its `context` has finished, and its input contains each of those tasks' results. Tasks marked `parallel` with no unfinished dependency run at the same time. → T10, T11
- **R4.** The run finishes only when every task is done. The program returns, and prints the result paths, only after every task has finished and every output file is written. `run_record.json` lists every task's result. → T8, T10
- **R5.** Every `{name}` placeholder in the agents' and tasks' texts is a declared input, and every declared input is used. At run time each placeholder is replaced, everywhere, by that run's value, so no placeholder reaches a model. A missing input or an input the team does not declare is refused before any model call, with stderr naming it. The same unchanged team file serves runs with different inputs. → T6, T7, T9, T19
- **R6.** The recommended team is the one in 5.3: four agents, four tasks, those dependencies, the research and profile tasks in parallel, two output files. → T1, T14, T21
- **R7.** Each task that names an output file writes its final result to that file in the output folder; the file's content is that task's final result. → T8, T21
- **R8.** *(Failure the course demonstrated.)* When a tool call fails, for example because the agent passed a malformed argument, the error goes back to the agent that called it as the tool's result. The run does not stop, and the task still finishes. → T12
- **R9.** *(Failure the course warned about; the course says its framework prevents it.)* A run always ends: an agent that keeps repeating the same step does not keep the program running forever. → T13
- **R10.** Each agent can use only the tools listed for it in the team file. → T14
- **R11.** The resume tools read only the configured resume file: `read_resume` takes no path, and `search_resume` searches only that file. → T14, T15, T16, T18
- **R12.** With no stand-in switch and no `OPENAI_API_KEY` (or the chosen provider's key), the program refuses to start, exits with 2 and names the missing key; no model call is made and no result file is written. → T20
- **R13.** The settings are honoured: `verbose` on prints each agent's steps, including its role, and `--quiet` prints only the result paths; `--resume` changes the file the resume tools read; `--out` changes where results are written. → T17, T18

---

## 7. Tests

### 7.1 Sample data (all facts invented for this spec)

**`sample_data/resume.md`**, exactly:

```markdown
# Dana Okafor

## Profile
Engineering leader with 12 years in software, the last five managing platform teams of 8 to 20 people across three time zones. Known for hiring, mentoring and running delivery for large programmes. Holds an MBA.

## Work History
### Harborlight Logistics — Engineering Manager (2019–2024)
- Led the platform group of 14 engineers through two reorganisations.
- Ran quarterly planning and budget for the group.
- Wrote the first shipment-tracking REST API in Python (FastAPI), backed by a PostgreSQL database.

### Quillstone Analytics — Senior Software Engineer (2014–2019)
- Built the event pipeline on Kafka with services written in Go.
- Packaged every service in Docker containers.

### Brightmoor Bank — Software Engineer (2012–2014)
- Maintained internal reporting tools in Python.

## Skills
Leadership, hiring, roadmap planning, stakeholder management.

## Education
- BSc Computer Science, University of Leeds, 2012
- MBA, Open University, 2018
```

Like the course's example, the profile sells leadership while the matching technical skills sit buried in the work history.

**`sample_data/resume_short.md`**, exactly:

```markdown
# Dana Okafor

## Work History
### Fernhill Labs — Engineer (2010–2012)
- Wrote Python scripts.
```

**`sample_data/pages/job_posting.html`**, a minimal HTML page whose visible text, line by line, is:
`Senior Backend Engineer — Lumen Freight` / `Remote (UK) · Full time` / `About the role: You will build the services that track freight across Europe.` / `Must have:` / `- 5+ years writing Python in production` / `- PostgreSQL` / `- Designing REST APIs` / `- Docker` / `Nice to have:` / `- Kafka` / `- Go`

**`sample_data/pages/github_profile.html`**, a minimal HTML page whose visible text is:
`dana-okafor` / `Pinned repositories:` / `freight-eta — Python, FastAPI service that predicts delivery times` / `kafka-replay — Go tool to replay Kafka topics after incidents`

**`sample_data/inputs.json`**:
- `job_posting_url`: `http://127.0.0.1:8765/job_posting.html`
- `github_url`: `http://127.0.0.1:8765/github_profile.html`
- `personal_writeup`: `Dana has 12 years in software and has led platform teams for the last five. Dana wants to return to hands-on backend engineering and is strongest in Python and PostgreSQL.`

**`sample_data/inputs_alt.json`**: as `inputs.json`, but `personal_writeup` is `Dana wants a data engineering role.`

**`sample_data/inputs_missing.json`**: as `inputs.json` without `github_url`.

**`sample_data/inputs_extra.json`**: as `inputs.json` plus `"salary": "90000"`.

**Invalid team files in `tests/fixtures/`**, each a copy of the recommended `team.yaml` with one change:
- `team_one_agent.yaml`: only the `researcher` agent and `research_task` remain.
- `team_no_backstory.yaml`: `profiler`'s backstory is the empty string.
- `team_idle_agent.yaml`: a fifth agent `editor` (role "Editor", any goal and backstory) is assigned no task.
- `team_no_expected_output.yaml`: `research_task` has no `expected_output`.
- `team_unknown_agent.yaml`: `research_task`'s agent is `recruiter`.
- `team_undeclared_placeholder.yaml`: `research_task`'s description also mentions `{salary}`.
- `team_unused_input.yaml`: `inputs` also lists `location`, used nowhere.

**Stand-in page fetcher** (stand-in for `scrape_website`, offline tests only). For an argument that does not start with `http://` or `https://` it raises an error with the message `not a valid URL: <argument>`. For `http://127.0.0.1:8765/<file>` where `sample_data/pages/<file>` exists, it returns that file's visible text: tags removed, each line trimmed, empty lines dropped, lines joined with newlines. For any other URL it raises `page not reachable: <url>`.

**Stand-in resume search** (stand-in for the meaning-based `search_resume`, offline tests only). It splits the configured resume into passages at blank lines. A word is a lowercase run of letters and digits. Each passage's score is the number of distinct query words it contains. It returns up to two passages with a score of at least 1, highest score first and earlier passage first on ties, as lines `Passage 1: <passage>`, `Passage 2: <passage>`. With no match it returns `No matching passage in the resume.` Replayed for the query `backend API database` on `resume.md`: only the passage starting `## Work History` scores (2: `api`, `database`), so the result is exactly one passage, `Passage 1: ## Work History` followed by the Harborlight section.

**Scripted stand-in model** (stand-in for every agent's model, offline tests only). `sample_data/scripted_replies.yaml` gives, per agent role, a `delay_seconds` (waited before each reply) and an ordered list of replies. Each reply is either a tool call (tool name and arguments, in whatever form the current framework release expects a model to request a tool) or a final answer (text). Each agent gets its own stand-in instance. Its n-th call gets the n-th reply, and once the list is used up the last reply repeats. Every call is logged to `standin_log.jsonl` (5.5).

| Role | Delay | Replies, in order |
|---|---|---|
| Tech Job Researcher | 0.5 s | 1. `scrape_website(url="jobs posting lumen backend")` *(planted: malformed argument)* · 2. `scrape_website(url="http://127.0.0.1:8765/job_posting.html")` · 3. final: `Job requirements — Senior Backend Engineer, Lumen Freight` / `Must have: Python (5+ years); PostgreSQL; REST API design; Docker.` / `Nice to have: Kafka; Go.` |
| Personal Profiler for Engineers | 1.0 s *(planted: slow parallel task)* | 1. `scrape_website(url="http://127.0.0.1:8765/github_profile.html")` · 2. `read_resume()` · 3. `search_resume(query="backend API database")` · 4. final: `Candidate profile — Dana Okafor` / `Hands-on: Python (FastAPI), PostgreSQL, REST APIs, Kafka, Go, Docker.` / `Leadership: managed platform teams of 8 to 20 for five years.` / `Goal: return to hands-on backend engineering.` |
| Resume Strategist for Engineers | 0 s | 1. `read_resume()` · 2. final: the tailored resume below |
| Engineering Interview Preparer | 0 s | 1. final: the interview materials below |

The strategist's final answer, exactly:

```markdown
# Dana Okafor
## Summary
Backend engineer with 12 years in software: Python (FastAPI), PostgreSQL, REST API design and Docker, plus five years leading platform teams.
## Work Experience
### Harborlight Logistics — Engineering Manager (2019–2024)
- Wrote the first shipment-tracking REST API in Python (FastAPI) on PostgreSQL.
### Quillstone Analytics — Senior Software Engineer (2014–2019)
- Built a Kafka event pipeline with Go services, packaged in Docker.
## Skills
Python, FastAPI, PostgreSQL, REST APIs, Docker, Kafka, Go; team leadership.
## Education
- BSc Computer Science, University of Leeds, 2012
- MBA, Open University, 2018
```

The interview preparer's final answer, exactly:

```markdown
# Interview questions and talking points — Lumen Freight
1. Question: Walk us through the shipment-tracking API you built with FastAPI and PostgreSQL.
   Talking point: schema design and query performance.
2. Question: How did you run Kafka in production at Quillstone?
   Talking point: replaying topics after incidents.
3. Question: Why move from management back to hands-on backend work?
   Talking point: five years leading teams makes you a stronger reviewer and mentor.
```

**`sample_data/scripted_replies_loop.yaml`**: as `scripted_replies.yaml`, except the Tech Job Researcher has delay 0 s and a single reply, `scrape_website(url="http://127.0.0.1:8765/job_posting.html")`, which therefore repeats on every call *(planted: an agent that never stops calling the same tool)*.

Planted failures: the malformed tool argument (R8, course-demonstrated); the slow parallel task, whose result a later task must wait for (R3, R4; the course demonstrated a parallel task's file that was not ready when read); the never-ending tool loop (R9, course-warned).

### 7.2 Test table

All offline tests run the CLI with `CREW_APP_STANDIN=sample_data/scripted_replies.yaml` (unless stated otherwise), `--inputs sample_data/inputs.json` and a fresh temporary `--out` folder that does not exist beforehand.

| Test | Given | When | Then |
|---|---|---|---|
| **T1** fresh start (R1, R6) | a fresh checkout | `python -m crew_app describe` | exit 0; `team.yaml`, every `sample_data` file of 7.1 and every `tests/fixtures` file exist; the JSON lists 4 agents with roles Tech Job Researcher, Personal Profiler for Engineers, Resume Strategist for Engineers, Engineering Interview Preparer, 4 tasks, inputs `job_posting_url`, `github_url`, `personal_writeup`; `research_task` and `profile_task` are parallel; `resume_strategy_task` depends on those two; `interview_preparation_task` on all three |
| **T2** one agent refused (R1) | `team_one_agent.yaml` | `describe --team` it, and `run --team` it | both exit 2; stderr says the team needs at least two agents; with `run`, `standin_log.jsonl` has no lines (or does not exist) |
| **T3** empty backstory refused (R1) | `team_no_backstory.yaml` | `describe --team` it | exit 2; stderr names `profiler` and `backstory` |
| **T4** idle agent refused (R1) | `team_idle_agent.yaml` | `describe --team` it | exit 2; stderr names `editor` as having no task |
| **T5** task fields enforced (R2) | `team_no_expected_output.yaml`, then `team_unknown_agent.yaml` | `describe --team` each | both exit 2; the first's stderr names `research_task` and `expected_output`; the second's names `research_task` and `recruiter` |
| **T6** placeholders match inputs (R5) | `team_undeclared_placeholder.yaml`, then `team_unused_input.yaml` | `describe --team` each | both exit 2; stderr names `salary`, then `location` |
| **T7** run inputs enforced (R5) | `inputs_missing.json`, then `inputs_extra.json` | `run` with each | both exit 2; stderr names `github_url`, then `salary`; no stand-in call is logged; no result file exists |
| **T8** end to end (R4, R7) | sample data | `run` | exit 0; the `--out` folder now exists; `tailored_resume.md` equals the strategist's scripted final answer and `interview_materials.md` equals the interview preparer's (ignoring trailing whitespace); `run_record.json` has status `completed`, error null, and 4 tasks, each with a non-null output; the researcher's output starts `Job requirements — Senior Backend Engineer, Lumen Freight`; stdout lists both result paths |
| **T9** inputs filled in everywhere (R5) | sample data | `run` | the researcher's call 1 `prompt_text` contains `http://127.0.0.1:8765/job_posting.html`; the profiler's call 1 contains `http://127.0.0.1:8765/github_profile.html` and `Dana wants to return to hands-on backend engineering`; no logged `prompt_text` contains `{job_posting_url}`, `{github_url}` or `{personal_writeup}` |
| **T10** later tasks wait and receive results (R3, R4) | sample data (profiler slowed to 1.0 s a reply) | `run` | the strategist's call 1 `received_at` is later than the `replied_at` of the profiler's call 4 and of the researcher's call 3; the strategist's call 1 contains `Job requirements — Senior Backend Engineer, Lumen Freight` and `Candidate profile — Dana Okafor`; the interview preparer's call 1 contains those two lines and `Backend engineer with 12 years in software` |
| **T11** independent tasks overlap (R3) | sample data | `run` | the profiler's call 1 `received_at` is earlier than the researcher's call 3 `replied_at` (the profiler started before the researcher finished; replayed: about 0 s versus about 1.5 s) |
| **T12** tool error goes back to the agent (R8) | sample data (researcher's first tool call is malformed) | `run` | the researcher's call 2 `prompt_text` contains `not a valid URL: jobs posting lumen backend`; the researcher has exactly 3 logged calls; the run exits 0 with status `completed` |
| **T13** a run always ends (R9) | `CREW_APP_STANDIN=sample_data/scripted_replies_loop.yaml` | `run` with a 120-second limit | the process exits within 120 seconds; `run_record.json` exists with status `completed` or `failed` |
| **T14** each agent has only its tools (R6, R10, R11) | the recommended team | `describe` | the researcher's tools are exactly `scrape_website(url)`; each of the other three agents' tools are exactly `scrape_website(url)`, `read_resume()` with no arguments, and `search_resume(query)` |
| **T15** the resume reader returns the configured file (R11) | sample data | `run` | the profiler's call 3 `prompt_text` contains `Harborlight Logistics` (the result of its `read_resume()` call) |
| **T16** resume search returns matching passages (R11) | sample data | `run` | the profiler's call 4 `prompt_text` contains `Passage 1: ## Work History` and does not contain `Passage 2:` |
| **T17** verbose setting (R13) | sample data | `run`, then `run --quiet` into a second fresh folder | the first stdout contains all four role names; the second stdout contains none of them and contains both result paths |
| **T18** resume path and output folder settings (R11, R13) | sample data | `run --resume sample_data/resume_short.md --out <fresh folder B>` | the profiler's call 3 `prompt_text` contains `Fernhill Labs` and not `Harborlight Logistics`; both result files are in folder B |
| **T19** one team, other inputs (R5) | `inputs_alt.json`, the same unchanged `team.yaml` | `run` | exit 0; the profiler's call 1 `prompt_text` contains `Dana wants a data engineering role.` and does not contain `return to hands-on backend engineering` |
| **T20** missing key refused (R12) | no `CREW_APP_STANDIN`, no `OPENAI_API_KEY` in the environment, no `.env` | `run` | exit 2; stderr contains `OPENAI_API_KEY`; no result file exists |
| **T21** `live` real run (R6, R7) | `OPENAI_API_KEY` set; no stand-in switch; the test serves `sample_data/pages` at `http://127.0.0.1:8765/` | `run` | exit 0; both result files exist and are non-empty; `tailored_resume.md` contains `Dana Okafor` and `PostgreSQL`; `run_record.json` has status `completed` |

Each item of section 6 is tested by at least one recommended-build test: item 1 by T1–T4, item 2 by T5, item 3 by T8, T10 and T11, item 4 by T6, T7, T9 and T19.

---

## 8. Standing permissions

- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in in its own description; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has data; anything that sends data to a third party beyond the chosen model provider and the pages named in the inputs (the person's resume is personal data).
- **Never:** invent provenance; let the program answer when it should say it does not know (an agent must not make up resume facts); change sample data to make a test pass; commit secrets.

---

## 9. Test plan

1. Install: `python -m pip install crewai crewai-tools pyyaml pytest` (current releases), plus any package a chosen option needs.
2. Offline tests: `python -m pytest -q`. T1–T20 must pass; T21 is marked `live` and is skipped without a key.
3. Live test: `OPENAI_API_KEY=<key> python -m pytest -q -m live`.
4. Manual run on the sample: in one terminal `python -m http.server 8765 --directory sample_data/pages`; in another `python -m crew_app run --inputs sample_data/inputs.json --out output`.
5. Adjust for the chosen options. Tests tied to the recommended team (T1, T8–T19, T21) are rewritten for C1b or C1c using that team's own sample. T10 and T11 change for C8b (no overlap) and are replaced by C8c's check. T15, T16 and the resume tools in T14 go with C7b. For each chosen non-recommended option, the build agent turns its "what to check" sentence (copied into `resolved-decisions.md`) into a test and reports it.
6. Report one result per test with evidence (test output, file paths). "Should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.
7. Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

---

## 10. Background notes (for the build agent)

### 10.1 The program
Kind of program: one job's named inputs → a team of specialised agents → tasks run in dependency order → finished results. Stages:
1. **Fill in the inputs.** One team definition serves any instance of the job (pattern card item 4).
2. **Assign the specialists.** Each agent has one role, goal and backstory, and each task one clear description and expected output, because the course found focused, role-playing agents with clear expectations do better than one agent doing everything (items 1 and 2).
3. **Gather.** Agents use their own small set of tools to read the pages and files they are pointed at, because tools are how an agent reaches the outside world. The course warned that too many tools confuse an agent.
4. **Run in dependency order.** Independent tasks run at the same time; a dependent task waits and works from its dependencies' results (item 3).
5. **Write the results.** Each task with an output file saves its final result, and the run ends when every task is done.

The course's job-application team is the recommended instance. Its other teams (article writing, customer support, sales-lead outreach, event planning, stock analysis) are other instances of the same program and are reachable through C1c. The step-by-step log (`verbose`) only shows what ran, so it is a setting, not a stage.

### 10.2 Failures
- **Tool given a wrong kind of argument** (demonstrated, Lesson 9). *What you see:* an agent tries to read a website with the file-reading tool, and the tool raises an exception. *Why:* the model chooses tools and arguments itself and sometimes picks wrong. *How the spec prevents a stopped run:* the error goes back to the agent, which tries another way, as the course's framework did by design. The course contrasted this with frameworks that stop the whole run and lose the work done so far. *Enforced by:* R8, planted malformed `scrape_website` argument, T12.
- **A parallel task's result not ready when read** (demonstrated, Lesson 12 notebook: the marketing report file of a task run in parallel was not written until some seconds after the run returned, and reading it early showed only its name). *How the spec prevents it:* a dependent task waits for all its dependencies, and the program returns only after every task is done and every file written. *Enforced by:* R3, R4, planted slow profiler, T10, T8.
- **Agents stuck repeating a tool or looping** (warned, Lessons 5 and 7: early versions of the course's framework had agents calling the same tool over and over, especially open-source models; the framework added guardrails so agents always try to reach an answer). The framework prevents this, so R9 states only the outcome. *Enforced by:* R9, planted endless tool loop, T13.
- **Context fading in a long chain** (a cost the course stated, Lesson 14, not a failure). It is carried in C8b's "pick this when". The recommended team names each task's dependencies explicitly, so the interview preparer receives the research and profile results directly.
- **Too many tools confusing agents, worse on smaller models** (a cost, Lesson 5). It is carried in C4c, C6b and C7b.

### 10.3 Why the questions and settings are what they are
- **C1:** the course's final team (Lesson 16) is its end-to-end program. The article team (Lesson 4) is the earliest, simplest version the course built. The course invited learners to change agents, tasks and inputs for their own uses (Lessons 4, 13, 15).
- **C2, C3:** context subjects for the learner's data. The course fetched its posting from a URL and read a Markdown resume.
- **C4:** the course used OpenAI and listed Hugging Face, Mistral, Cohere and local Ollama models as alternatives (Lesson 4 notebook, Lesson 3). It noted agents can run on different models (Lesson 3).
- **C5:** a context subject about where it runs. The course ran notebooks, which are never offered.
- **C6:** the course gave every final-team agent a web-search tool (Serper; Lessons 9, 12, 15, 16). It is left out of the recommended build because it needs its own key (departure 2).
- **C7:** the course's final team had both a whole-file reader and a semantic search over the resume. It also warned against overloading agents with tools (Lesson 5).
- **C8:** the course taught sequential (default; Lesson 4), parallel tasks with explicit dependencies (Lessons 12 and 16), and hierarchical with a framework-created manager whose model you choose (Lesson 15). The final team uses the second.
- **C9:** memory (short-term, long-term, entity) was switched on with one setting in Lessons 6 and 9 and described in Lesson 5. The final team did not use it. Offered per the pattern card.
- **C10:** the reviewer that can delegate back is Lesson 6's quality-assurance pattern, which the instructor recommended adding to any team. Offered per the pattern card.
- **C11:** asking a person before a task finishes is from Lesson 12.
- **C12:** typed JSON output and file output are from Lesson 12, described as useful for connecting agents to existing systems.

**Subjects that are not questions:**
- *Delegation between worker agents:* framework behaviour the course's final team left to the framework (4.7). It is noted in the checklist. The reviewer's send-back is part of C10b.
- *Caching of repeated tool calls* (Lesson 8): framework behaviour (4.7).
- *Retrying after a tool error:* framework behaviour (4.7). The outcome is fixed by R8.
- *A different model per agent:* handled by the gate's one-line-per-role model choice (a setting, 4.3).
- *Verbose logging, parallel flags, file names, paths:* settings (4.3).
- *Giving tools at the task level instead of the agent level* (Lesson 6): fails 5.2's test 3. No learner situation changes what the program does; the course's final team gives tools per agent.
- *Building a custom tool* (Lesson 9's always-positive sentiment tool) and *a directory reader* (Lesson 9): from other lessons and not a change to a stage (3.3). A learner adds tools through C1c.
- *Semantic search over a whole website* (imported in Lesson 6, never used): fails 5.2's test 3. A single job posting page is short enough to read whole.
- *Task callbacks* (listed on a Lesson 11 slide, never built or described): not a change to a stage (3.3).
- *Using LangChain's tools* (Lessons 8, 10) and *deploying crews as hosted APIs on crewAI's paid platform* (Lessons 3, 17): not stages (3.3). The platform needs a hosted account.
- *A custom manager agent* (Lesson 15 says future versions would allow it): only the framework-made manager was taught. It is part of C8c only as "a manager".

**Where picked values came from (4.2):**
- *Model:* the video says GPT-4 Turbo for the final team (Lesson 16; Lesson 9 says it moved to GPT-4 for its larger context window). The notebooks set GPT-3.5 Turbo because of platform limits. Rule (1), the instructor's stated value, makes GPT-4 Turbo the course's model; either way the gate picks a current model.
- *Verbose:* Lesson 4 used the highest level (2), the final team used on (true). Rule (2), the final app, applies.
- *Memory:* on in Lessons 6 and 9, absent in the final team. Rule (2) gives no memory.
- *Parallel research and profile tasks, the dependencies and the two output file names:* the final team (Lesson 16 notebook and narration).
- The course set no temperature for agents; Lesson 15's manager model used 0.7, relevant only to C8c.

**Other places the course disagrees with itself:**
- Lesson 16's narration says "among our three agents" while the team has four.
- The narration says the resume strategist has search, scrape, resume reading and resume search; the notebook gives the researcher only scrape and search. The spec follows the notebook, minus search (departure 2).
- Lesson 12's narration says "synchronous execution" where the notebook sets parallel (asynchronous) execution.
- A slide calls the final team "your first multi-agent system" though it is the last one built.
- Lesson 4's narration says agents default to GPT-4 while the notebook sets GPT-3.5 Turbo.

**Course code that looks like a slip:**
- The final team's profile task mentions only the GitHub page and the write-up, though its agent also has the resume tools. Kept as the course did.
- The final team's texts contain spelling slips. Not carried over (departure 11).

### 10.4 Names that go stale
Treat these course-era names as search keywords against current documentation, not as guaranteed imports:
- *crewAI:* `Agent`, `Task`, `Crew`, `Process.hierarchical`, `manager_llm`, `allow_delegation`, `verbose=2`, `memory=True`, `async_execution`, `context`, `output_file`, `output_json`, `human_input`, `kickoff(inputs=...)`.
- *crewAI tools:* `SerperDevTool`, `ScrapeWebsiteTool` (with `website_url`), `WebsiteSearchTool`, `FileReadTool` (with `file_path`), `DirectoryReadTool`, `MDXSearchTool` (with `mdx`), and `BaseTool` with a `_run` method, imported from the tools package in the course.
- *LangChain:* `langchain_openai.ChatOpenAI`, `langchain_community.llms.HuggingFaceHub`, `langchain_community.chat_models.ChatCohere`.
- *Setup:* the environment variables `OPENAI_MODEL_NAME`, `OPENAI_API_BASE`, `SERPER_API_KEY`, and `python-dotenv`'s `load_dotenv`.
- *Models:* `gpt-3.5-turbo`, `gpt-4-turbo`, GPT-4, Llama 3 70B, `mistral-small`, `HuggingFaceH4/zephyr-7b-beta`.
- *Versions:* crewAI 0.28.8, crewAI tools 0.1.6, LangChain community 0.0.29; the documentation shown was v0.22.4.
- *Request limits:* if a chosen current model rejects a `temperature` parameter, leave it unset; the course set none for its agents.

### 10.5 Course names
- Agent roles: Tech Job Researcher, Personal Profiler for Engineers, Resume Strategist for Engineers, Engineering Interview Preparer. Binding in 5.3.
- Course variables `researcher`, `profiler`, `resume_strategist`, `interview_preparer` → agent ids. Same names.
- Course tasks `research_task`, `profile_task`, `resume_strategy_task`, `interview_preparation_task` → task ids. Same names.
- Course inputs `job_posting_url`, `github_url`, `personal_writeup` → declared inputs. Binding.
- Course output files `tailored_resume.md`, `interview_materials.md`. Binding.
- Course tools: `scrape_tool` → `scrape_website`; `read_resume` (file reader confined to the resume) → `read_resume`; `semantic_search_resume` → `search_resume`; `search_tool` → C6b's web search.
- Course sample `fake_resume.md` → `sample_data/resume.md`, with this spec's own invented facts.
- "Crew" → the agent team; "kickoff" → `run`.

### 10.6 Lesson map (transcript numbering)
1. Introduction: the program in one line, its building blocks.
2. Overview: the job-application example (posting, resume, four agents, tools, rewritten resume, interview material); the C1a scenario.
3. AI Agents: agents and tools, different models per agent (C4), the framework.
4. Create agents to research and write an article: agents, tasks, crew, inputs filled in at kickoff, sequential by default (card items 1–4, C1b, C8b).
5. Key elements of AI agents: role playing, focus, tools, cooperation, guardrails (R9), memory (C9).
6. Multi agent customer support automation: delegation, the QA reviewer (C10), tool scoping, memory on.
7. Mental framework for agent creation: think like a manager, specific roles.
8. Key elements of agent tools: versatile, fault-tolerant, caching (R8, 4.7 notes).
9. Tools for a customer outreach campaign: tools, a custom tool, the demonstrated tool error (R8), inputs used in every text (R5).
10. Recap of tools.
11. Key elements of well defined tasks: description and expected output (R2), task options.
12. Automate event planning: parallel tasks, human input (C11), JSON and file output (C12), the file not ready (10.2).
13. Recap on tasks.
14. Multi agent collaboration: processes, context fading (C8).
15. Multi agent collaboration for financial analysis (transcript title spells it "Mutli"): hierarchical process (C8c).
16. Build a crew to tailor job applications: the recommended team (5.3, R3, R4, R6, R7).
17. Next steps with AI agent systems: resources and the hosted platform (not used).
18. Conclusion.

Slides: the descriptions of both decks were read. Narrated slides counted like their lesson's transcript; slides that exist only in the deck counted less and decided nothing. The notebooks' folder numbers (L2–L7) are not lesson numbers: L2 is Lesson 4, L3 Lesson 6, L4 Lesson 9, L5 Lesson 12, L6 Lesson 15, L7 Lesson 16. Nothing in this spec requires access to the course.

---

*Spec version 1 · course: Multi AI Agent Systems with crewAI · project: an agent team that tailors job applications (by default) · when the build agent does something unexpected, add the missing constraint here and re-run.*
