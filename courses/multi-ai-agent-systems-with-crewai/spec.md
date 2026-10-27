# Spec: a team of AI agents that turns a few named inputs into finished results

**What you're building:** a program that takes a few named inputs for one job, runs a team of
specialised AI agents through defined tasks, hands each task's result to the tasks that depend
on it, and writes the finished results. By default the job is tailoring a job application: you
give it a job-posting address, a code-profile address and a short write-up about the candidate.
Four agents (a job researcher, a candidate profiler, a résumé strategist and an interview
preparer) then produce two files: a résumé rewritten for that posting, and interview questions
with talking points. You see the agents start, use their tools, ask each other questions, and
the two files appear.

**Fastest path:** answer "recommended build" at the first question. The build is finished when
the offline tests pass. They need no key, because stand-ins replace the model, the web pages and
the embedding model. `live` tests skipped for lack of a key are expected, not failures.

**To run for real**, the recommended build needs an OpenAI API key (its document search uses an
embedding model from the same provider) and network access to the pages you name.

This file is self-contained: everything the build needs is here.

*Provenance: course "Multi AI Agent Systems with crewAI" (18 lessons). Materials used: lesson
transcripts, the six course notebooks with their helper module, slide descriptions of two decks,
and the owner-confirmed pattern card. Written 2026-10-27 with guide v2.7 (2026-10-27).*

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
   an OpenAI API key and network access to the pages you name), or **choose** question by
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

### C1. What job does your agent team do?
- **C1a. Tailor a job application (Recommended - course default).** Inputs: a job-posting
  address, a code-profile address, a short write-up about the candidate, plus the candidate's
  résumé file. Results: a tailored résumé and interview preparation notes. Pick this when you
  want the program as the spec defines it, with its sample data and exact tests. Setup cost:
  none beyond the model key.
- **C1b. Your own job.** You name the inputs, the people you would hire for the job (each
  becomes an agent with a role, goal and backstory), the tasks each one does, which tasks wait
  for which, and which task results are the finished results. Pick this when you want the same
  kind of program for your own work, for example "research a sales lead and draft an outreach
  email" or "plan an event from a city, date and head-count". Setup cost: you write a team
  definition (section 4.1 schema) and your own sample inputs.
  *What to check:* every agent in your definition has a non-empty role, goal and backstory,
  every task has a description, an expected output and one assigned agent, every placeholder in
  the definition is a named input, and one run with your sample inputs writes each finished
  result.

### C2. What format are the documents the agents read (the résumé, by default)?
- **C2a. Markdown or plain text (Recommended - course default).** Pick this when your documents
  are already text, or you can export them as text. Setup cost: none.
- **C2b. PDF.** Pick this when your documents only exist as PDFs (a résumé exported from a
  design tool). Setup cost: a PDF text-extraction package; scanned PDFs with no text layer will
  not work without OCR.
  *What to check:* the document-reading tool returns the PDF's text, and searching inside it
  returns passages whose words appear in the PDF.
- **C2c. Word (.docx).** Pick this when your documents are Word files you keep editing. Setup
  cost: a .docx reading package.
  *What to check:* the document-reading tool returns the Word file's paragraph text in order,
  and searching inside it returns passages whose words appear in the file.

### C3. Which model provider powers the agents?
- **C3a. OpenAI (Recommended - course default).** Pick this when you have, or can get, an OpenAI
  API key. Setup cost: a paid OpenAI account and key in `OPENAI_API_KEY`.
- **C3b. Another hosted provider (for example Mistral, Cohere or Hugging Face).** Pick this when
  you already pay for another provider, or your organisation only approves one. Setup cost: that
  provider's account and key; document search needs an embedding model from it or from C3c.
  *What to check:* a `live` run with that provider's key completes every task and writes every
  finished result, and no request goes to OpenAI.
- **C3c. A local model served on your machine (for example through Ollama).** Pick this when you
  have no key, cannot send data to a third party, or want runs to cost nothing. Setup cost: a
  model download of several GB, enough memory to run it, and a local embedding model. Smaller
  models get more confused by tools and extra context, so agents may misuse tools more often.
  *What to check:* with the network to outside hosts blocked except for the pages being fetched,
  a run completes every task through the local model and writes every finished result.

### C4. Do all agents use the same model?
- **C4a. One model for every agent (Recommended - course default).** Pick this when you want the
  simplest setup and one bill. Setup cost: none.
- **C4b. A model per agent role.** Pick this when some roles need a stronger model (the one that
  writes the final text) and others can run on a cheaper or local one (the one that gathers
  facts). Setup cost: configuring, and possibly paying for, each model.
  *What to check:* each agent's model calls go to the model configured for its role, shown by
  the model name recorded with each call in the run log.

### C5. Which agent framework is the program built on?
- **C5a. crewAI (Recommended - course default).** Pick this when you want the framework's
  built-in agents, tasks, crews, tools, tool-error handling, caching, delegation and memory.
  Setup cost: installing the framework and its tools package.
- **C5b. No framework.** Pick this when you cannot add the dependency or want full control of
  every prompt. Setup cost: a lot more code; you write the agent loop, tool calling, tool-error
  handling, caching and delegation yourself.
  *What to check:* the offline tests in section 6 pass unchanged against your own agent loop.
- **C5c. Another agent framework you already use.** Pick this when your project already runs on
  a different agent framework and you do not want two. Setup cost: mapping each rule in
  section 5 onto that framework; some behaviours (tool-error handling, cross-agent caching) may
  need your own code.
  *What to check:* the offline tests in section 6 pass unchanged on that framework.

### C6. How is a run started?
- **C6a. A command-line program on your machine (Recommended).** Pick this when you start runs
  yourself. Setup cost: none.
- **C6b. A local web service.** It accepts the inputs as JSON over HTTP and responds with the
  finished results. Pick this when another program, or a teammate's tool, needs to start runs.
  Setup cost: a web server package; a run holds the request open for minutes.
  *What to check:* a POST of the sample inputs to the service returns every finished result and
  writes the same files the command line writes.
- **C6c. Deployed on the framework vendor's hosted platform as an API.** Pick this when your team
  needs an always-on API with managed scaling and you are allowed to use that platform. Setup
  cost: an account on the vendor's platform (it requires the framework of C5a), a code
  repository it can read, and your keys stored there.
  *What to check:* a kickoff request with the sample inputs to the deployed API returns every
  finished result.

### C7. Does a quality-assurance reviewer check the results before they are final?
- **C7a. No reviewer (Recommended - course default).** Pick this when you read the results
  yourself before using them. Setup cost: none.
- **C7b. Add a reviewer agent.** One more agent with its own role, goal and backstory (for
  example "Quality Assurance Specialist"). For each task that writes a finished result, a review
  task runs after it, takes its output, checks it for completeness, accuracy and tone, and its
  result is what gets written. The reviewer may send the draft back to the agent that wrote it
  and use the revision. Pick this when your output reaches someone else, such as a customer or
  an employer, and should be fact-checked before it goes out. Setup cost: one more model call
  chain per finished result; runs take longer.
  *What to check:* each finished-result file holds the reviewer's output, the review task
  started only after the task it reviews finished, and the review task's input contains that
  task's output.

### C8. In what order do the tasks run?
- **C8a. Each task names the tasks it waits for; tasks with nothing to wait for run at the same
  time (Recommended - course default).** A task starts only when every task it names has
  finished, and gets all of their results. Pick this when some steps do not depend on each other
  (researching the job and the candidate), so running them side by side saves time. Setup cost:
  none.
- **C8b. One at a time, in list order.** Each task starts when the one before it finishes and
  gets its result. Pick this when your job is one straight chain of steps and you want the
  simplest run to follow in the log. Cost: slower; in a long chain the first task's details fade
  as they are passed along, so a late task may lose facts an early one found.
  *What to check:* in the run log each task starts only after the previous one in the list
  finished, and each task's input contains the previous task's output.
- **C8c. A manager agent coordinates.** The program adds a manager agent that keeps the overall
  goal in view, hands each task to the agent it judges best, reviews each result and may ask for
  improvements; it still starts a task only after the tasks it depends on are done and passes
  their results on. Pick this when you want one coordinator that remembers the original goal
  across a long job and checks each step. Setup cost: a model for the manager; many more model
  calls; the order of work is decided during the run, so runs differ more from each other.
  *What to check:* the run log shows the manager handing out every task, no task starts before
  the tasks it depends on have finished, and each task's input contains their results.

### C9. Does a person review any task's result before it counts as done?
*Ask only when `C6` is `C6a`.*
- **C9a. No (Recommended - course default).** Pick this when runs should finish unattended.
  Setup cost: none.
- **C9b. Yes, for the tasks you name.** Before a named task finishes, the run shows its result
  in the terminal and waits for your feedback; the agent revises with it before later tasks use
  the result. Pick this when a step's result should be approved by a person before other steps
  build on it (picking a venue before planning catering around it). Setup cost: someone must be
  at the terminal during the run.
  *What to check:* with scripted feedback typed into the terminal, the named task's final result
  is produced after the feedback, and the next task's input contains the revised result.

### C10. May agents ask each other for help?
- **C10a. Yes; each agent may ask a teammate a question or hand it part of its work, and decides
  for itself when (Recommended - course default).** Pick this when you want agents to cooperate
  and correct each other. Cost: extra model calls; you do not control when it happens.
- **C10b. No; each agent does only its own task.** Pick this when you want predictable runs and
  fewer model calls, or you use a small model that gets confused by the extra choice. Setup
  cost: none.
  *What to check:* no agent is offered a way to ask or hand work to a teammate, and the run log
  holds no delegation events.

### C11. Can agents search the web, or only fetch the pages you name?
- **C11a. Only fetch pages whose addresses are in the inputs (Recommended).** Pick this when the
  inputs already name the pages that matter (the job posting and the code profile). Setup cost:
  network access only.
- **C11b. Also search the web (course default).** Agents get a web-search tool that returns
  search results, which they can then fetch. Pick this when the inputs do not include every
  address agents need, for example researching a company from its name alone. Setup cost: an
  account and key with a search-API service (the course used one that gives free starting
  credits).
  *What to check:* a `live` run where an agent searches for a name from the inputs records a
  search call and a fetch of one of the returned addresses.

### C12. How do agents use the long documents (the résumé, by default)?
- **C12a. Read the whole document, and also search inside it by meaning (Recommended - course default).** Pick this when documents are long enough that finding the right passage helps.
  Setup cost: an embedding model from your provider.
- **C12b. Read the whole document only.** Pick this when documents are short (a one-page résumé)
  and you would rather not set up an embedding model. Setup cost: none.
  *What to check:* no agent has a document-search tool, every agent that had one can read the
  whole document, and the run writes every finished result.

### C13. When a tool fails, what happens?
- **C13a. The error goes back to the agent as a message and the run continues (Recommended - course default).** The agent can retry with other input or another tool. Pick this when a lost
  run is costly and agents can usually work around a failed call. Setup cost: none.
- **C13b. The run stops and reports the error.** Pick this when a tool acts on the world
  (sends email, writes to a database) and continuing after a failed call could repeat or
  compound the damage. Cost: everything done so far in the run is lost.
  *What to check:* a planted tool error stops the run with a message naming the tool and the
  error, and no finished-result file is written.

### C14. Do agents remember earlier steps and past runs?
- **C14a. No memory; each run starts blank (Recommended - course default).** Pick this when you
  want each run to depend only on its inputs. Setup cost: none.
- **C14b. Memory on.** Short-term memory shared by all agents during a run; long-term memory
  stored in a local database after a run, where each agent critiques its own finished task and
  later runs reuse the lessons; and entity memory of the people, organisations and places a run
  discusses. Pick this when you want the agents to remember earlier steps and past runs, so the
  team improves with use. Setup cost: a local database file, extra model calls for the
  self-critique, and results that depend on earlier runs.
  *What to check:* after one run the local memory store holds entries from it, and a second run
  with the same inputs reads those entries.

### C15. What form do the finished results take?
- **C15a. Markdown files (Recommended - course default).** Pick this when a person reads the
  results. Setup cost: none.
- **C15b. JSON files that match a declared schema.** Each result is converted into a typed object
  and saved as JSON. Pick this when your results feed other code (a database, another program)
  rather than a reader. Setup cost: writing a schema per result.
  *What to check:* each finished-result file parses as JSON and validates against its declared
  schema.

### Departures from the course
- **D1. Models.** The course's code used `gpt-3.5-turbo`; its videos used GPT-4 and GPT-4 Turbo.
  The build uses a current model from the chosen provider, because model names go stale.
- **D2. Versions.** The course pinned crewAI 0.28.8, crewAI tools 0.1.6 and LangChain Community
  0.0.29. The build uses current releases, because course-era versions often no longer install
  or work with current models.
- **D3. Web search left out (C11a).** The course's final team also had a web-search tool that
  needs a separate search-API account and key. The inputs already name the pages to fetch, and
  fetching them carries the taught tool use, so the recommended build leaves search out. It is
  option C11b.
- **D4. Sample data written for this spec.** The course used its own candidate résumé, a real
  job posting and a real code profile. The recommended build uses a fictional candidate and
  fictional pages (section 6.1), served by a stand-in fetcher in the offline tests.
- **D5. A command-line program, not notebook cells (C6a).** The course ran the team cell by
  cell and displayed the files in the notebook. The build is a program that writes the files and
  prints their paths.
- **D6. Team definition as a data file.** The course defined agents and tasks in code. The build
  keeps them in one definition file (section 4.1) so it can be validated, tested and swapped.
- **D7. Additions for safety and checking.** A step limit per agent (setting `max_agent_steps`),
  a passage count for document search (`search_passages`), an output folder, a run log, refusal of a run with a missing input, a `--stand-in` flag, and
  the offline tests with their stand-ins. None of these is in the course.
- **D8. The run returns only after every result file is written.** In one course notebook a
  result file appeared up to 45 seconds after the run returned; the build waits (rule R7).
- **D9. Typos fixed in the course's prompt text.** The agents' and tasks' text in section 4.1 is
  the course's wording with spelling and spacing fixed.

---

## 2. Objective

Given the named inputs of one job, the program runs a defined team of specialised agents through
defined tasks in dependency order and writes the finished results, using the same team definition
for every run.

## 3. Tech stack, versions and secrets

- **Language:** Python, current release. **Framework:** crewAI and its tools package, current
  releases (C5a). **Tests:** pytest, current release.
- **Tools (recommended build):** the framework's website-scraping tool (fetch one address and
  return its text), its file-reading tool bound to the résumé file, and its document semantic
  search tool bound to the same file (C12a). The semantic search uses an embedding model from the
  chosen provider (addition: the course does not say which embedder its search used).
- **Package:** importable name `crew_app`; entry point `python -m crew_app run --inputs <file>`.
- **Secrets:** read from the environment; a local `.env` file may be loaded into the environment
  (the course loaded its keys this way). Recommended build: `OPENAI_API_KEY`. C11b adds the
  search service's key. Never written to logs, results or the repository.
- **Real or stand-in:** with the provider key present, the program uses the real model. With
  `--stand-in`, it uses the stand-ins of section 6.1 and needs no key or network (addition).
  Without the key and without `--stand-in`, it exits before any agent runs (rule R16).

## 4. Contracts

### 4.1 Team definition

File: `crew_app/team.json`. Validated on load against this schema; a definition that fails is
refused with the failing task or agent id and field (rules R1, R2).

```json
{
  "type": "object",
  "required": ["name", "agents", "tasks"],
  "additionalProperties": false,
  "properties": {
    "name": {"type": "string", "minLength": 1},
    "agents": {
      "type": "array", "minItems": 2,
      "items": {
        "type": "object",
        "required": ["id", "role", "goal", "backstory", "tools", "allow_delegation"],
        "additionalProperties": false,
        "properties": {
          "id": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"},
          "role": {"type": "string", "minLength": 1},
          "goal": {"type": "string", "minLength": 1},
          "backstory": {"type": "string", "minLength": 1},
          "tools": {"type": "array", "uniqueItems": true,
                    "items": {"enum": ["scrape_website", "read_resume", "search_resume", "search_web"]}},
          "allow_delegation": {"type": "boolean"},
          "model_role": {"type": "string", "minLength": 1}
        }
      }
    },
    "tasks": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "description", "expected_output", "agent"],
        "additionalProperties": false,
        "properties": {
          "id": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"},
          "description": {"type": "string", "minLength": 1},
          "expected_output": {"type": "string", "minLength": 1},
          "agent": {"type": "string"},
          "depends_on": {"type": "array", "uniqueItems": true, "items": {"type": "string"}, "default": []},
          "parallel": {"type": "boolean", "default": false},
          "tools": {"type": "array", "uniqueItems": true,
                    "items": {"enum": ["scrape_website", "read_resume", "search_resume", "search_web"]}},
          "output_file": {"type": "string", "pattern": "^[A-Za-z0-9_.-]+\\.(md|json)$"}
        }
      }
    }
  }
}
```

Checks the schema cannot express (rule R2): every task's `agent` names an agent `id`; every
`depends_on` entry names an earlier task's `id`; ids are unique. A task's `tools`, when present,
replace its agent's tools for that task (the course: task tools override agent tools). With C1b
the tool list may name the learner's own tools.

**Recommended team (course wording, typos fixed).** All agents: `allow_delegation: true` (C10a;
the course's final team left it unset, which the course says means allowed).

| id | role | goal | backstory | tools |
|---|---|---|---|---|
| `researcher` | Tech Job Researcher | Make sure to do amazing analysis on job posting to help job applicants | As a Job Researcher, your prowess in navigating and extracting critical information from job postings is unmatched. Your skills help pinpoint the necessary qualifications and skills sought by employers, forming the foundation for effective application tailoring. | `scrape_website` |
| `profiler` | Personal Profiler for Engineers | Do incredible research on job applicants to help them stand out in the job market | Equipped with analytical prowess, you dissect and synthesize information from diverse sources to craft comprehensive personal and professional profiles, laying the groundwork for personalized resume enhancements. | `scrape_website`, `read_resume`, `search_resume` |
| `resume_strategist` | Resume Strategist for Engineers | Find all the best ways to make a resume stand out in the job market. | With a strategic mind and an eye for detail, you excel at refining resumes to highlight the most relevant skills and experiences, ensuring they resonate perfectly with the job's requirements. | `scrape_website`, `read_resume`, `search_resume` |
| `interview_preparer` | Engineering Interview Preparer | Create interview questions and talking points based on the resume and job requirements | Your role is crucial in anticipating the dynamics of interviews. With your ability to formulate key questions and talking points, you prepare candidates for success, ensuring they can confidently address all aspects of the job they are applying for. | `scrape_website`, `read_resume`, `search_resume` |

(With C11b every agent also gets `search_web`, as in the course. With C12b, drop `search_resume`.)

| id | description | expected_output | agent | depends_on | parallel | output_file |
|---|---|---|---|---|---|---|
| `research_task` | Analyze the job posting URL provided ({job_posting_url}) to extract key skills, experiences, and qualifications required. Use the tools to gather content and identify and categorize the requirements. | A structured list of job requirements, including necessary skills, qualifications, and experiences. | `researcher` | — | true | — |
| `profile_task` | Compile a detailed personal and professional profile using the GitHub ({github_url}) URLs, and personal write-up ({personal_writeup}). Utilize tools to extract and synthesize information from these sources. | A comprehensive profile document that includes skills, project experiences, contributions, interests, and communication style. | `profiler` | — | true | — |
| `resume_strategy_task` | Using the profile and job requirements obtained from previous tasks, tailor the resume to highlight the most relevant areas. Employ tools to adjust and enhance the resume content. Make sure this is the best resume ever but don't make up any information. Update every section, including the initial summary, work experience, skills, and education. All to better reflect the candidate's abilities and how it matches the job posting. | An updated resume that effectively highlights the candidate's qualifications and experiences relevant to the job. | `resume_strategist` | `research_task`, `profile_task` | false | `tailored_resume.md` |
| `interview_preparation_task` | Create a set of potential interview questions and talking points based on the tailored resume and job requirements. Utilize tools to generate relevant questions and discussion points. Make sure to use these question and talking points to help the candidate highlight the main points of the resume and how it matches the job posting. | A document containing key questions and talking points that the candidate should prepare for the initial interview. | `interview_preparer` | `research_task`, `profile_task`, `resume_strategy_task` | false | `interview_materials.md` |

### 4.2 Run inputs

Recommended inputs file (JSON). Extra keys are ignored; a missing key that a placeholder uses is
refused (rule R3).

```json
{
  "type": "object",
  "required": ["job_posting_url", "github_url", "personal_writeup"],
  "properties": {
    "job_posting_url": {"type": "string", "pattern": "^https?://\\S+$"},
    "github_url": {"type": "string", "pattern": "^https?://\\S+$"},
    "personal_writeup": {"type": "string", "minLength": 1}
  }
}
```

A placeholder is `{name}` where `name` matches `^[a-z_][a-z0-9_]*$`; it may appear in any agent's
role, goal or backstory and in any task's description or expected output.

### 4.3 Run result

The command prints, and returns to a caller, the path of every finished-result file and the
text of each. Files are written to `output_dir`; a new run overwrites them. Exit code 0 when
every task finished, non-zero otherwise.

### 4.4 Run log (addition)

File: `output_dir/run_log.jsonl`, rewritten each run, one JSON object per line:

```json
{
  "type": "object",
  "required": ["time", "event"],
  "properties": {
    "time": {"type": "number", "description": "seconds since run start"},
    "event": {"enum": ["run_started", "task_started", "task_finished", "tool_called",
                       "tool_error", "cache_hit", "delegated", "model_call", "run_finished"]},
    "task": {"type": "string"},
    "agent": {"type": "string"},
    "tool": {"type": "string"},
    "model": {"type": "string"},
    "detail": {"type": "string"}
  }
}
```

### 4.5 Model roles

One role per agent: `researcher`, `profiler`, `resume_strategist`, `interview_preparer` (all on
one model with C4a). Optional roles: `manager` (C8c), `reviewer` (C7b). Embedding model for
document search (C12a), not a chat role.

### 4.6 Settings

| Setting | Value | Source | Change this when … |
|---|---|---|---|
| Log detail (`verbose`) | most detailed: print each agent's steps, tool calls and answers | Lesson 4 sets the highest level (2); Lesson 16 sets `True`; rule 4.2(1) picked Lesson 4 | you run unattended and want quieter output |
| `max_agent_steps` | 15 model calls per agent per task, then it must give a final answer | addition (the course relies on the framework's built-in guardrails and sets no value) | a task legitimately needs more tool calls |
| `output_dir` | `output/` | addition (the course wrote into the notebook's folder) | you want results elsewhere |
| `resume_path` | `samples/resume.md` | Lesson 16 bound both résumé tools to one Markdown file | you use your own résumé |
| Result file names | `tailored_resume.md`, `interview_materials.md` | Lesson 16 | never for C1a (they are part of the contract) |
| Tool cache | on: identical calls within a run reach the source once | Lessons 8 and 9 (built into the framework) | — |
| `search_passages` | 3 passages returned per document search | addition | documents are long and agents need more context |
| Manager temperature (C8c only) | 0.7 | Lesson 15 | the current manager model rejects a temperature: drop it |

---

## 5. Business rules

### What must stay true (pattern card)
1. **The work is split across several specialised agents, and each agent has its own role, goal
   and backstory.** No single agent does the whole job.
2. **Every piece of work is a task with a clear description and a stated expected output, and
   each task is assigned to an agent.**
3. **Results move between agents: a task works from the outputs of the tasks it depends on and
   does not start until they are done. The run finishes when every task is done.**
4. **One team definition serves any instance of the job: each run takes its named inputs and puts
   them in place wherever the agents and tasks use them.**

Every option of every question keeps all four (with C8b a task depends on the one before it;
with C8c the manager still respects dependencies; with C13b a failed run ends as failed, without
results).

### Rules
- **R1.** A team has at least two agents; each has a non-empty role, goal and backstory; roles
  are distinct; when there are two or more tasks, no agent is assigned all of them. (Card 1) → T1, T2
- **R2.** Every task has a non-empty description, a non-empty expected output and exactly one
  assigned agent from the team; `depends_on` names only earlier tasks. A definition breaking
  this or R1 is refused on load, naming the agent or task id and the field. (Card 1, 2) → T2, T3
- **R3.** Every placeholder in the definition must have a value in the run's inputs; otherwise
  the run is refused before any model call, naming each missing input. (Card 4; addition) → T4
- **R4.** Each run puts its own input values in place of every placeholder, in every agent field
  and task text; no placeholder text remains in any prompt. The same definition serves runs with
  different inputs. (Card 4) → T5
- **R5.** A task starts only after every task in its `depends_on` has finished, and its input
  contains the output of each of them, not only the one before it. (Card 3; prevents the fading
  context the course warned about) → T6, T7
- **R6.** Tasks marked `parallel` whose dependencies are done run at the same time; a task that
  depends on them waits for all of them even when one finishes early. (Lesson 16) → T6
- **R7.** The run finishes when every task is done. It returns only after every finished-result
  file is fully written, and it returns every result's path and text. (Card 3; course warning,
  addition fix) → T8
- **R8.** Each agent can use only the tools listed for it (or for its current task); the
  delegation actions of R11 are not tools. (Course warning about overloaded agents) → T9
- **R9.** A tool error is returned to the calling agent as a message containing the error text;
  the run continues. (Course failure, Lesson 9) → T10
- **R10.** Within one run, a tool call with the same tool and the same arguments as an earlier
  call, by any agent, is answered from the cache and does not reach the source again. (Lessons
  8, 9) → T11, T13
- **R11.** With delegation allowed, an agent may ask a named teammate a question or hand it part
  of its work; the teammate's answer is returned to the asking agent, which continues its own
  task. (Lessons 6, 14) → T12
- **R12.** An agent that has made `max_agent_steps` model calls in a task without a final answer
  is told to answer now; its next reply is taken as its final answer, and the run continues.
  (Course warning about agents stuck in loops; limit is an addition) → T13
- **R13.** The résumé-reading tool returns exactly the content of the file at `resume_path` and
  reads no other file; the résumé-search tool searches only that file. (Lesson 16) → T14
- **R14.** The résumé-search tool returns at most `search_passages` passages of the résumé,
  best match first. (Lesson 16; count is an addition) → T15
- **R15.** The tailored résumé states only facts found in the résumé, the fetched pages or the
  write-up. (Lesson 16's task text: "don't make up any information") → T16 (`live`)
- **R16.** With the provider key present the program uses the real model; with `--stand-in` it
  uses the stand-ins; with neither, it exits before any agent runs, naming the missing
  environment variable. Keys never appear in logs or results. (Addition) → T17
- **R17.** On a fresh start, a run creates `output_dir` and the run log; the team definition
  loads and validates. (Addition) → T18
- **R18.** With the most detailed log level, the console shows each agent's role when it starts
  a task and each tool call it makes. (Lessons 4, 16) → T19
- **R19.** Fetching a real public page returns its text. (Course tool, checked live) → T20 (`live`)

---

## 6. Tests

### 6.1 Sample data and stand-ins

All facts below are written for this spec; none comes from the course.

**`samples/resume.md`** (one section per heading of any level):
```
# Alex Moreno
## Profile
Engineering manager with eight years in software, the last four leading a team of 12 engineers. Focused on hiring, roadmaps and delivery.
## Experience
### Northwind Logistics — Engineering Manager (2020–2024)
- Led a team of 12 engineers across two time zones.
- Rewrote the billing service in Go with PostgreSQL, cutting invoice errors by 30%.
### Brightlane — Software Engineer (2016–2020)
- Built REST APIs in Python for the shipment-tracking product.
- Packaged services with Docker for the move to the cloud.
## Skills
Leadership, hiring, roadmap planning, stakeholder communication.
## Education
BSc Computer Science, University of Leeds (2016).
```

**`samples/pages/job_backend.md`** — "Lumen Freight — Backend Engineer, Payments. Must have: Go;
PostgreSQL; REST API design; Docker; 3+ years of backend experience. Nice to have: Kafka."

**`samples/pages/job_data.md`** — "Okapi Health — Data Engineer. Must have: Python; SQL; Airflow."

**`samples/pages/profile_alex.md`** — "alex-moreno. Repositories: ledger-go — a double-entry ledger
in Go backed by PostgreSQL; dockyard — Docker Compose templates for local development."

**`samples/inputs_a.json`**: `job_posting_url` = `https://jobs.example.com/backend-engineer-42`,
`github_url` = `https://code.example.com/alex-moreno`, `personal_writeup` = "Alex has eight years
in software, the last four leading a team, and wants to return to hands-on backend work."

**`samples/inputs_b.json`**: as A, but `job_posting_url` =
`https://jobs.example.com/data-engineer-7`.

**`samples/inputs_missing.json`**: as A without `personal_writeup`.

**`samples/team_bad_task.json`**: the recommended team with `expected_output` removed from
`profile_task`. **`samples/team_bad_agent.json`**: the recommended team with `backstory` removed
from `profiler`.

**Stand-in fetcher (stand-in for the website-scraping tool's network access).** Maps addresses to
sample files and counts fetches per address:

| Address | File | Delay |
|---|---|---|
| `https://jobs.example.com/backend-engineer-42` | `job_backend.md` | 1.0 s (planted: makes the researcher finish after the profiler) |
| `https://jobs.example.com/data-engineer-7` | `job_data.md` | 0 s |
| `https://code.example.com/alex-moreno` | `profile_alex.md` | 0 s |

Any other text raises the tool error `could not fetch '<text>': not a web address` when it does
not start with `http://` or `https://`, and `page not found: <address>` otherwise.

**Stand-in embedder (stand-in for the embedding model).** Scores each résumé section by the number
of distinct lower-cased words (split on non-letters and non-digits) it shares with the query,
heading included; ties go to the earlier section; returns the top `search_passages` sections with
a score above 0.

**Stand-in model (stand-in for the chat model), file `samples/stand_in_model.json`.** Each call is
attributed to a role by the agent making it. A call belongs to a task when its prompt contains
that task's marker phrase; any other call to a role is a teammate question. Within a task, the
role's N-th call gets turn N. When a prompt contains the framework's instruction to give a final
answer now (the build agent finds that text in the current framework), or the turns run out, the
role's fallback reply is returned. "URL in task" means the first `http(s)://` address in that
task's description. Every reply is given in the reply format the framework's agent loop expects.
Every prompt received is recorded for the tests.

| Role | Task marker | Turns | Teammate answer | Fallback |
|---|---|---|---|---|
| researcher | "extract key skills, experiences, and qualifications" | 1: `scrape_website(url = URL in task)`; 2: final "JOB REQUIREMENTS: Go; PostgreSQL; REST API design; Docker; 3+ years backend experience. Nice to have: Kafka." | "The two most important requirements are Go and PostgreSQL." | "FORCED: no final answer reached." |
| profiler | "Compile a detailed personal and professional profile" | 1: `scrape_website(url = "ledger-go")` (planted tool misuse); 2: `scrape_website(url = URL in task)`; 3: final "CANDIDATE PROFILE: hands-on Go and PostgreSQL (billing rewrite, ledger-go); REST APIs in Python; Docker; four years leading 12 engineers; wants hands-on backend work." | "No further details." | "FORCED: no final answer reached." |
| resume_strategist | "tailor the resume to highlight the most relevant areas" | 1: `read_resume()`; 2: `scrape_website(url = "https://jobs.example.com/backend-engineer-42")`; 3: `search_resume(query = "Go PostgreSQL billing")`; 4: final = the tailored résumé text below | "No further details." | "FORCED: no final answer reached." |
| interview_preparer | "Create a set of potential interview questions and talking points" | 1: ask teammate "Tech Job Researcher": "Which two requirements matter most?" (with C10b, skip to turn 2); 2: final = the interview text below | "No further details." | "FORCED: no final answer reached." |

Tailored résumé text (strategist's final):
```
# Alex Moreno — Backend Engineer
## Profile
Backend engineer with eight years in software, hands-on in Go, PostgreSQL, REST APIs and Docker.
## Experience
- Northwind Logistics: rewrote the billing service in Go with PostgreSQL, cutting invoice errors by 30%.
- Brightlane: built REST APIs in Python; packaged services with Docker.
## Skills
Go, PostgreSQL, REST API design, Docker, Python, team leadership.
## Education
BSc Computer Science, University of Leeds (2016).
```

Interview text (preparer's final):
```
# Interview preparation
1. Question: How did you rewrite the billing service in Go with PostgreSQL? Talking point: the 30% drop in invoice errors.
2. Question: How have you designed REST APIs? Talking point: the Brightlane shipment-tracking APIs.
Focus areas from the researcher: Go and PostgreSQL.
```

**`samples/stand_in_loop.json`**: as `stand_in_model.json`, except the researcher's turns are 100
copies of `scrape_website(url = URL in task)`.

### 6.2 Test table

Offline unless marked `live`. "Run A" = a run with `inputs_a.json`, the recommended team and the
stand-ins, starting from an empty `output_dir`. Text comparisons ignore leading and trailing
whitespace.

| Test | Given | When | Then | Rules |
|---|---|---|---|---|
| T1 | the recommended `team.json` | it is loaded | 4 agents with distinct, non-empty roles, goals and backstories; 4 tasks assigned to 4 different agents | R1 |
| T2 | `team_bad_task.json`; `team_bad_agent.json` | each is loaded | each is refused; the messages name `profile_task` / `expected_output` and `profiler` / `backstory`; no model call is made | R1, R2 |
| T3 | the recommended `team.json` | it is loaded | every task has a non-empty description and expected output and an agent id present in the team; every `depends_on` id names an earlier task | R2 |
| T4 | `inputs_missing.json` | a run is started | refused before any model call; the message names `personal_writeup`; the stand-in model recorded 0 prompts | R3 |
| T5 | run A, then a run with `inputs_b.json`, same definition | both finish | in run B the researcher's first prompt contains `https://jobs.example.com/data-engineer-7` and not `backend-engineer-42`; in both runs no recorded prompt contains `{job_posting_url}`, `{github_url}` or `{personal_writeup}`; run B's fetch count for the data-engineer address is 1; the profiler's prompt in run A contains "wants to return to hands-on backend work" | R4 |
| T6 | run A | it finishes | run log: `profile_task` starts before `research_task` finishes; `profile_task` finishes before `research_task` finishes (planted delay); `resume_strategy_task` starts after both finished; `interview_preparation_task` starts after `resume_strategy_task` finished | R5, R6 |
| T7 | run A | it finishes | the strategist's first prompt contains "JOB REQUIREMENTS: Go" and "CANDIDATE PROFILE: hands-on Go"; the preparer's first prompt contains both of those and "# Alex Moreno — Backend Engineer" | R5 |
| T8 | run A | the run call returns | immediately on return, `output/tailored_resume.md` equals the tailored résumé text and `output/interview_materials.md` equals the interview text; the result lists both paths and texts; the run log has 4 `task_finished` events before `run_finished`; exit code 0 | R7 |
| T9 | run A | tools offered to each agent are inspected | researcher: {scrape_website}; profiler, resume_strategist, interview_preparer: {scrape_website, read_resume, search_resume} (delegation actions excluded) | R8 |
| T10 | run A | it finishes | run log has one `tool_error` for the profiler's `scrape_website` with detail containing "not a web address"; the profiler's second prompt contains "not a web address"; `profile_task` finished; exit code 0 | R9 |
| T11 | run A | it finishes | fetch count for `https://jobs.example.com/backend-engineer-42` is 1; run log has a `cache_hit` for the strategist's `scrape_website` | R10 |
| T12 | run A | it finishes | run log has a `delegated` event from `interview_preparer` to `researcher`; the researcher received a teammate prompt containing "Which two requirements matter most?"; the preparer's second prompt contains "The two most important requirements are Go and PostgreSQL." | R11 |
| T13 | a run with `inputs_a.json` and `stand_in_loop.json` | it finishes | `research_task`'s output is "FORCED: no final answer reached."; the researcher made at most 16 model calls in `research_task`; all 4 tasks finished; fetch count for the backend address is 1 | R12, R10 |
| T14 | `resume_path` = `samples/resume.md` | `read_resume` is called with no argument, and again with argument `samples/pages/job_data.md` | both calls return exactly the content of `samples/resume.md` | R13 |
| T15 | the stand-in embedder, `search_passages` = 3 | `search_resume("Go PostgreSQL billing")`; then `search_resume("Go PostgreSQL Docker Python REST engineers hiring Leeds")` | the first returns exactly 1 passage, the "Northwind Logistics" section (only it scores above 0); the second returns exactly 3 passages in this order: "Northwind Logistics" (score 3), "Brightlane" (score 3, later section), "Profile" (score 2), although 5 sections score above 0 | R14 |
| T16 `live` | provider key set; real model; stand-in fetcher; `inputs_a.json` | a run finishes | both files exist and are non-empty; `tailored_resume.md` contains "Go" and "PostgreSQL" and does not contain "Kafka" | R15 |
| T17 | no provider key in the environment | `python -m crew_app run --inputs samples/inputs_a.json`; then the same with `--stand-in` | the first exits non-zero before any agent runs with a message naming `OPENAI_API_KEY`, no network request made; the second exits 0 and writes both files; with a dummy key set, neither the log nor the results contain the key | R16 |
| T18 | a fresh checkout with no `output/` | run A | `crew_app/team.json` loads and validates; `output/` and `output/run_log.jsonl` exist; every line of the log validates against 4.4 | R17 |
| T19 | run A with console output captured | it finishes | the console shows "Tech Job Researcher", "Personal Profiler for Engineers", "Resume Strategist for Engineers" and "Engineering Interview Preparer", and a line for each `scrape_website` call | R18 |
| T20 `live` | network access; the real website-scraping tool | it fetches `https://example.com` | the text returned contains "Example Domain" | R19 |

Card items: 1 → T1, T2; 2 → T2, T3; 3 → T6, T7, T8; 4 → T4, T5.

---

## 7. Standing permissions

- **Always:** run the offline tests after every change; keep every stand-in labelled as a
  stand-in in its own description; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has produced results;
  anything that sends data to a third party beyond the chosen model provider and the pages named
  in the inputs.
- **Never:** invent provenance; let the program make up an answer when it should say it does not
  know; change sample data to make a test pass; commit secrets.

## 8. Test plan

- Offline: `pytest` (the `live` marker is excluded by default in the test configuration).
- Live: `pytest -m live` with the provider key set and network access.
- Real run: `python -m crew_app run --inputs samples/inputs_a.json`; offline demo: add
  `--stand-in`.
- Adjust the tests for the chosen options (for example, with C8b replace T6's parallel checks by
  C8b's check; with C10b drop T12 and skip the preparer's turn 1; with C12b drop T15 and the
  strategist's turn 3). Then turn every chosen option's "what to check" sentence (copied into
  `resolved-decisions.md`) into a test and run it.
- Report a result per test with evidence (test output, file paths). "Should pass" counts as not
  run. The build is finished when the recommended tests, adjusted for the chosen options, pass
  and each chosen option's check passes.
- Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure
  diagram of this app".

---

## 9. Background notes

### The program
- **Define the team:** the course's advice is to think like a manager: name the goal and the
  process, then the people you would hire; each becomes an agent whose role, goal and backstory
  steer it, because agents perform better when role-playing (Lessons 4, 5, 7).
- **Define the tasks:** each task has a description and an expected output, which acts as a
  forcing function for what you want back (Lessons 4, 11, 13).
- **Fill in the inputs:** placeholders in agents and tasks are replaced by the run's inputs, so
  one team serves any instance (Lessons 4, 9, 15).
- **Run in dependency order:** sequential by default; independent tasks can run in parallel and
  a task given others as context waits for them (Lessons 4, 12, 16).
- **Agents work:** each agent thinks in a loop, uses its tools and may ask teammates (Lessons 3,
  6, 8).
- **Pass results on:** a task's output becomes part of the next task's input (Lesson 4).
- **Write the results:** results go to files (Lessons 12, 16).

### Failures
- **Tool used on the wrong kind of input (shown, Lesson 9).** You see an agent try to read a web
  address with a file-reading tool and get an error. It happens because the model picks tools by
  their descriptions and sometimes picks wrong. Prevented by returning the error to the agent so
  it can try again instead of stopping the run. The spec plants it as the profiler passing a
  non-address to the scraper (the spec's file reader is bound to one file, so it cannot be misused
  the same way). Rule R9, test T10.
- **Context fades along a long chain (warned, Lesson 14).** In a sequential run the first task's
  details weaken as results are passed from agent to agent. Prevented by giving each task the
  outputs of every task it depends on. Rule R5, test T7.
- **Agents stuck repeating a tool or looping (warned, Lesson 5).** Early framework versions let
  agents call the same tool over and over, especially on open-source models; the framework added
  guardrails so agents always attempt an answer. Prevented by the step limit. Rule R12, test T13.
- **A result file not there yet when the run returns (warned, Lesson 12 notebook).** With
  parallel tasks writing files, the course told learners to wait about 45 seconds after the run
  before opening one. Prevented by returning only after files are written. Rule R7, test T8.
- **Too many tools confuse an agent (warned, Lesson 5),** worse on smaller models. Prevented by
  giving each agent only its listed tools. Rule R8, test T9.
- **Made-up facts in the tailored résumé (warned by the course's task text, Lesson 16; guardrails
  against hallucination, Lesson 5).** Rule R15, test T16 (`live`; a scripted model cannot show
  it).

### Why the questions and settings are what they are
- **C1:** the course's final team tailors job applications; every earlier lesson built the same
  kind of program for another job (article writing, customer support, sales outreach, event
  planning, financial analysis), which is why "your own job" is an option.
- **C2:** the course read a Markdown résumé; its tool list includes search tools for PDF, Word
  and other formats.
- **C3:** the course used OpenAI and showed Hugging Face, Mistral, Cohere and local models through
  Ollama as alternatives; it warned that smaller models get messier with many tools.
- **C4:** the course named running different agents on different models (one on Llama 3, another
  on GPT-4) as a benefit of several agents.
- **C5:** the course taught crewAI but said its concepts apply to all major frameworks, and that
  you can build agents without one at the cost of a lot more code, including your own exception
  handling.
- **C6:** the course ran notebooks (never offered: the build is a program) and pointed to its
  vendor's hosted platform for turning a team into an API; the local web service is an option the
  course did not mention.
- **C7:** the course recommended adding a quality-assurance agent to most teams, because a final
  reviewer that can send work back improves quality (Lesson 6); its final team has none.
- **C8:** sequential is the framework default (Lesson 4); parallel tasks with context are the
  final team's choice (Lesson 16); a manager that keeps the goal, delegates and reviews is the
  hierarchical process (Lessons 14, 15), changed with one line, and the instructor invited
  learners to try sequential instead. The course's financial run was "a long running crew".
- **C9:** human input before a task finishes was taught in Lesson 12 for venue selection; the
  course's final team does not use it.
- **C10:** the course's final team leaves delegation at the framework's default, which the course
  states is "allowed"; earlier teams switched it off, for example for an agent that is "just supposed to do what it's
  told" (Lessons 4, 9). The instructor said an agent allowed to delegate will not always do it,
  and you do not fully control when.
- **C11:** the course's final team had a web-search tool that needs a search-API key (free
  credits); the instructor noted many other search tools would do.
- **C12:** the course's final team had both a whole-file reader and a semantic search over the
  résumé.
- **C13:** the course contrasted frameworks that stop on a tool exception (you then handle
  restart yourself; work so far is lost) with crewAI, which continues and tells the agent.
- **C14:** the course said memory "can make more difference than all the other things combined"
  and is one flag; it used it in Lessons 6 and 9 but not in its final team. Short-term memory is
  shared during a run, long-term memory is stored locally and improves later runs via
  self-critique, entity memory holds the subjects discussed (Lesson 5).
- **C15:** the course showed turning a task's output into a typed object and a JSON file to bridge
  agent output and regular code (Lesson 12); its final team writes Markdown.
- **Subjects that are not questions:**
  - A single agent doing the whole job — breaks card item 1.
  - Tasks without an expected output — breaks card item 2.
  - Turning the tool cache off — no learner situation found where identical calls within one run
    should reach the source twice (test 3).
  - Task callbacks (Lesson 11, named once in a list) — they only report on a task and do not
    change any result; no situation found that changes the built program (test 3).
  - A custom manager agent (Lesson 15 said it would come in future versions) — part of C8c; the
    build agent may let the learner define it.
  - Tools given at task level instead of agent level (Lesson 6) — supported by the definition
    schema (task tools override agent tools), so not a separate choice.
  - Other built-in tools (directory reading, website search, many search-by-format tools) and
    custom tools (Lesson 9) — part of defining your own team (C1b).
  - LangChain tools usable inside crewAI (Lessons 8, 10) — a source of tools, not a stage choice.
  - Log detail — a setting (4.6), tuned after the build.
  - Which model the tests use — never asked: tests run offline on stand-ins; `live` tests run
    when a key is present.
- **Where picked values came from:** log detail — Lesson 4 introduced it at the highest level (2),
  Lesson 16 used `True`; rule 4.2(1) chose Lesson 4. Delegation — Lesson 16's agents leave it unset,
  which the Lesson 6 notebook says means allowed; Lessons 4 and 9 set it off for their agents; the
  final app (rule 4.2(2) / 4.1) decides. Models — the code sets `gpt-3.5-turbo`; the videos use
  GPT-4 Turbo (Lessons 9, 12, 15, 16 notebooks say so; Lesson 9's narration says GPT-4, Lesson 4's
  narration says the framework's default was GPT-4); the build picks a current model (4.6).
  Manager temperature 0.7 — Lesson 15. File names and inputs — Lesson 16.

### Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports:
`crewai==0.28.8`, `crewai_tools==0.1.6`, `langchain_community==0.0.29`, `Agent`, `Task`, `Crew`,
`Process.hierarchical`, `manager_llm`, `ChatOpenAI` (from `langchain_openai`), `kickoff(inputs=…)`,
`allow_delegation`, `verbose=2`, `memory=True`, `async_execution`, `context`, `output_file`,
`output_json`, `human_input`, `SerperDevTool`, `ScrapeWebsiteTool`, `FileReadTool`,
`MDXSearchTool`, `DirectoryReadTool`, `WebsiteSearchTool`, `BaseTool` with a `_run` method,
environment variables `OPENAI_MODEL_NAME`, `OPENAI_API_KEY`, `SERPER_API_KEY`, `OPENAI_API_BASE`;
`HuggingFaceHub`, `ChatCohere`; models `gpt-3.5-turbo`, `gpt-4-turbo`, GPT-4, Llama 3 70B,
`HuggingFaceH4/zephyr-7b-beta`, `mistral-small`. The course set a temperature only on the manager
model; some current models reject a temperature parameter, so drop it when they do. Current
releases may expect `verbose` as true/false rather than a level.

### Course names
| Course name | Spec term |
|---|---|
| `job_application_crew` | the recommended team (`crew_app/team.json`, name "job_application") |
| `researcher`, `profiler`, `resume_strategist`, `interview_preparer` | agent ids (binding) |
| `research_task`, `profile_task`, `resume_strategy_task`, `interview_preparation_task` | task ids (binding) |
| `job_posting_url`, `github_url`, `personal_writeup` | run inputs (binding) |
| `fake_resume.md` | `samples/resume.md` (`resume_path`) |
| `tailored_resume.md`, `interview_materials.md` | finished-result files (binding) |
| `search_tool`, `scrape_tool`, `read_resume`, `semantic_search_resume` | `search_web`, `scrape_website`, `read_resume`, `search_resume` |
| `context=[…]` | `depends_on` |
| `async_execution=True` | `parallel: true` |

### Lesson map (transcript numbering)
- 1 Introduction; 2 Overview — the final team's goal, agents, tools and before/after résumé;
  agentic versus traditional automation.
- 3 AI Agents — agents, tools, multi-agent systems, different models per agent (C4).
- 4 Create agents to research and write an article — agents, tasks, crew, placeholders, kickoff
  inputs, sequential default, log levels (card 1–4, C8, settings).
- 5 Key elements of AI agents — role playing, focus, tools, cooperation, guardrails, memory
  (C14, failures).
- 6 Multi agent customer support automation — delegation, the QA reviewer, task-level tools,
  memory flag (C7, C10).
- 7 Mental framework for agent creation — think like a manager (card 1).
- 8 Key elements of agent tools — versatile, fault-tolerant, caching (R9, R10).
- 9 Tools for a customer outreach campaign — custom tool, directory tool, the tool-misuse failure
  (C13, failure).
- 10 Recap of tools; 11 Key elements of well defined tasks (card 2, C9, C15).
- 12 Automate event planning — typed JSON output, output files, human input, parallel tasks, the
  late-file warning (C9, C15, R7).
- 13 Recap on tasks; 14 Multi agent collaboration — processes, fading context (C8, R5).
- 15 Multi agent collaboration for financial analysis — hierarchical manager (C8c).
- 16 Build a crew to tailor job applications — the recommended build.
- 17 Next steps — the vendor's hosted platform (C6c); 18 Conclusion.
- Notebooks: six, one each for Lessons 4, 6, 9, 12, 15, 16 (their own folder numbers L2–L7 count
  differently). Slides: descriptions of both decks were read; narrated slides counted like their
  lesson's transcript, deck-only slides counted less. One deck-only slide calls the final team
  "your first multi-agent system", against the transcripts, which call it the most complex and
  last; the transcripts win.
- Nothing in this spec requires access to the course.

---

*Spec v2 draft · Multi AI Agent Systems with crewAI · project: a team of agents that tailors a job
application · when the build agent does something unexpected, add the missing constraint here and
re-run.*
