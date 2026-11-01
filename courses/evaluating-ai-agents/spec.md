# Spec: an evaluation program for a tool-using agent

**What you're building:** a program that tests a tool-using agent (a router that picks among skills): it runs the agent over a fixed set of test questions, records every step of each run, scores the router's tool choices, each skill's output and the path the agent took with separate evaluators, and shows the scores per agent version side by side. By default the agent under test is a sales-data assistant (look up data with SQL, analyze it, write chart code) over a small sample store-sales table, and you see two versions of that agent scored in one table, so you can tell whether a prompt change helped or broke something.

**What the recommended build needs to run:** an OpenAI API key (agent model and judge model), network access to the OpenAI API, and the Phoenix Python package, which runs a local trace-and-experiment server on your own machine (no account, no container).

**Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once `OPENAI_API_KEY` is set and are skipped until then; that is not a failure.

This file is self-contained: everything the build needs is written here.

*Provenance: course "Evaluating AI Agents" (DeepLearning.AI with Arize AI); materials used: transcripts of all 15 lessons, the five lab notebooks and helper module (as one rendered context file), descriptions of all 116 slides, and the owner-confirmed pattern card (2026-11-01); generated 2026-11-01 with guide v2.9 (2026-10-31).*

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
   an OpenAI API key), or **choose** question by
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
C1–C3 are context (which agent, which data, which model provider); C4–C7 follow the program's stages in order (record runs, score the router, score the lookup skill, add human labels).

### C1. Which agent do you want to evaluate?
- **C1a (Recommended - course default): The sales-data assistant from this spec.** A router that picks among three skills (look up sales data with SQL, analyze data, write chart code) over a store-sales table, built as part of this program. *Pick this when* you want to learn the evaluation setup on a working agent first, or you have no agent of your own yet. *Setup:* none.
- **C1b: Your own router-and-skills agent.** You plug in your agent as one function that takes a conversation and returns its full message list, plus its tool definitions; the router judge and the path measure work unchanged, and each of your skills gets one evaluator: an exact comparison with an expected output where you can write one, otherwise an LLM judge that returns one of two labels. *Pick this when* you already have an agent whose router calls tools and you want to know which part of it fails; you must write your own test questions and your own set of similar questions, and expected outputs where you can (they unlock exact code checks; judges are never 100% accurate). *Setup:* whatever your own agent already needs.
  - *What to check:* one run of your agent produces a record with its tool calls, tool responses, final answer and step count, and each of your skills has its own score column in the comparison table.

### C2. Which sales table does the sales-data assistant query?
*Ask only when C1 is C1a.*
- **C2a (Recommended): The sample store-sales table defined in this spec.** Ten transactions across three stores, written for this spec as a small stand-in for the course's store-transactions file; every expected answer in the tests is known. *Pick this when* you want the tests to pass exactly as written. *Setup:* none.
- **C2b: Your own transactions table (CSV or parquet file).** The lookup skill queries your file instead of the sample. *Pick this when* you have your own store or sales data and want the agent judged on it; you must rewrite the test questions and produce their expected SQL and results from your file, because the exact lookup check needs ground truth. *Setup:* your data file.
  - *What to check:* the lookup skill answers a test question from your file, and the expected results stored in the test set were produced by running the reference SQL on your file.

### C3. Which model provider runs the agent and the judges?
- **C3a (Recommended - course default): OpenAI.** The agent and all LLM judges call OpenAI models. *Pick this when* you have an OpenAI key; the course used a small model for the agent and a stronger one for the judges. *Setup:* OpenAI API key.
- **C3b: Another hosted provider with tool calling (for example Anthropic).** Same program, different client for the agent and the judges. *Pick this when* your key or your company's account is with another provider; the course says only the best models agree closely with human judgment, so use that provider's strongest model for the judges. *Setup:* that provider's API key.
  - *What to check:* a run on that provider produces tool calls in the same record shape, and every judge reply is read as one of the judge's two labels.
- **C3c: A model served on your own machine.** The agent and the judges call a local model server. *Pick this when* your data must not leave your machine or you have no paid key; the course warns a judge needs a high-end model to agree with people, so expect more disagreement and a less reliable router. *Setup:* install a local model server and download a model that supports tool calling (often several GB).
  - *What to check:* one test question runs end to end against the local server, and every judge reply is read as one of the judge's two labels.

### C4. Where are runs recorded and scores shown?
- **C4a (Recommended - course default): A local Phoenix server.** Every run is traced as nested steps, the test sets and experiments are stored in Phoenix, and its web page shows each trace and a table of evaluator scores per experiment. *Pick this when* you want to click through each run's steps and see the scores in a browser. *Setup:* none beyond installing the Python package; it runs on your machine.
- **C4b: Hosted Phoenix (the vendor's web app).** Same as C4a but the server is hosted. *Pick this when* several people must see the same traces and scores; your agent's questions and answers are sent to that service. *Setup:* an account and its API key.
  - *What to check:* after one evaluate run, the hosted project shows that run's trace and both experiments with their evaluator scores.
- **C4c: Plain local files.** Each run's step record is written as JSON lines and each version's scores as a JSON file; the comparison is printed as a table. *Pick this when* you cannot run an extra server, or want records you can keep in version control; you lose the clickable trace view. *Setup:* none.
  - *What to check:* after one evaluate run, a file holds each run's ordered steps (router decisions, tool calls with arguments and results, final answer, step count) and the comparison table reads its scores from the version's results file.

### C5. How is the router scored?
- **C5a (Recommended - course default): An LLM judge on every tool call.** For each tool call in a run, a judge sees the question, the call and all tool definitions and answers correct or incorrect; the run's router score is the average. *Pick this when* your test questions have no written "expected tool"; the judge also checks the parameters, but it is never 100% accurate. *Setup:* none.
- **C5b: The LLM judge plus an exact comparison with an expected tool.** Each test case also states the tool the router should call first, and a code check scores 1 when it did; both router scores appear side by side. *Pick this when* you can write the expected tool for every test question and want an exactly right check beside the judge; it costs you that ground truth for each case. *Setup:* none.
  - *What to check:* a test case whose first tool call matches its expected tool scores 1 on the exact check, one that does not scores 0, and the comparison shows both router columns.

### C6. How is the lookup skill's output scored?
*Ask only when C1 is C1a.*
- **C6a (Recommended - course default): Compare the numbers in the result with an expected result.** The numbers in the lookup result must equal the numbers in the test case's expected result. *Pick this when* you can write expected results for your test questions; it is the more accurate check, and comparing numbers only tolerates different column names. *Setup:* none.
- **C6b: An LLM judge of the generated SQL.** A judge sees the question and the generated SQL and answers correct or incorrect. *Pick this when* you have many questions and no expected results; a judge is never 100% accurate. *Setup:* none.
  - *What to check:* each run that called the lookup skill gets a correct or incorrect label from the judge, given the question and the SQL that run generated.

### C7. Should people also label recorded runs?
- **C7a (Recommended - course default): Evaluators only.** All scores come from the code checks and the LLM judges. *Pick this when* the automatic evaluators settle your cases; human labelling is slow and hard to do at scale. *Setup:* none.
- **C7b: Add a human label queue.** A command shows a version's recorded runs one at a time (question, tool calls, final answer, evaluator scores) and saves the person's label (correct or incorrect) and an optional note beside the evaluators' scores. *Pick this when* your evaluators cannot settle some cases alone, or you need labels you can fully trust; it costs a person's time per run, and feedback from end users is biased toward those who choose to give it. *Setup:* none.
  - *What to check:* a label entered for one recorded run is saved with that run and appears beside the evaluators' scores in the comparison for its version.

## 2. Departures from the course

- **D1. Sample data.** The course queried its own store-transactions file; this spec uses ten transactions written for it (section 7.1), so every expected answer is known. No course data is copied; the prompts and tool descriptions name the sample dataset instead of the course's.
- **D2. Test questions.** The two test sets keep the course's kinds of question but are reworded for the sample table; the similar-question set has 6 questions instead of the course's 17, to keep the offline replay small.
- **D3. Expected results are produced, not pasted.** The course pasted expected SQL results from an earlier run; here setup runs each case's reference SQL on the sample table through the lookup skill's own execution path, so the stored text has the same formatting the agent's results will have.
- **D4. Ordered reference SQL.** The course's reference SQL for "sales by store" had no ordering; the number comparison is order-sensitive, so the sample's reference SQL orders its rows.
- **D5. Generated code runs in a separate process with a time limit.** The course ran generated chart code inside the evaluator's own process; the course also advises running generated code in an enclosed environment, so the build does that (addition).
- **D6. Step limit.** The course's agent loop had no limit; the build stops a run after `max_router_calls` router calls and counts it as failed (addition, safety limit).
- **D7. One command per version, one comparison table.** The course ran the path experiment and the overall experiment in separate notebooks and compared versions in the Phoenix page; the build runs both for a version with one command and also prints a comparison table (addition).
- **D8. One run-record shape.** The course's path experiment returned only a step count and a readable message list; the build uses the overall experiment's record shape for both.
- **D9. Version names in every experiment name.** The course named its first overall experiment without a version and the second "v2"; the build appends the version name to every experiment name.
- **D10. A program, not notebooks.** The course ran everything cell by cell in notebooks with Phoenix pre-launched; the build is a command-line program that starts or connects to a local Phoenix.
- **D11. Current models and libraries.** The course's model ids and library names are listed as facts (section 10, N5); the build uses current releases.
- **D12. Plotting library installed (addition).** The course ran chart code in a notebook that already had a plotting library; the build installs one with a non-interactive backend so real chart code can run in the check.

---

## 3. Objective
Given an agent and two fixed test sets, run every test case through a named version of the agent, record each run's steps, score the router, each skill and the path with separate evaluators, and show every version's scores side by side.

## 4. Tech stack and versions
- Python (current release). Libraries, current releases: an OpenAI client; pandas and a parquet engine; DuckDB (in-memory SQL over the table); pydantic (structured chart config); python-dotenv (reads `.env`); Arize Phoenix with its evals, OpenTelemetry registration and the OpenInference OpenAI instrumentation; a plotting library for generated chart code (addition, D12); pytest (addition).
- The course's requirements file is not in the materials; no version pins are known, and none are invented.
- Where the course leaves a behaviour to a library (how experiments run cases, how traces are exported, how a judge reply is parsed into a label), keep the current release's behaviour and note in the checklist how the release provides it.
- **Secrets:** `OPENAI_API_KEY` and `PHOENIX_COLLECTOR_ENDPOINT` come from the environment or a `.env` file, never from code or committed files. When `PHOENIX_COLLECTOR_ENDPOINT` is unset, the program uses a local Phoenix at its default address and starts it if none is running.

## 5. Contracts

**Commands** (package `agent_evals`):
- `python -m agent_evals setup` — creates the sample table file, the two test-set files and the two version files if missing, then uploads both test sets to the recording backend.
- `python -m agent_evals ask "<question>" [--version v1]` — runs the agent once, traced, prints the final answer.
- `python -m agent_evals evaluate --version <name>` — runs the overall experiment and the path experiment for that version, writes `results/<name>.json`.
- `python -m agent_evals compare` — prints the comparison table for every version in `results/`, in the order they were evaluated.

**Sample table** `data/sample_sales.parquet`, loaded as SQL table `sales`. Columns and types: `Store_Number` integer, `SKU_Coded` integer, `Sold_Date` date, `Qty_Sold` integer, `Total_Sale_Value` double, `On_Promo` integer 0 or 1.

**Test case** (`datasets/overall_questions.json`, a list):
```json
{"type":"object","required":["question","sql_generated","sql_result"],"additionalProperties":false,
 "properties":{"question":{"type":"string","minLength":1},
   "sql_generated":{"type":"string","description":"reference SQL"},
   "sql_result":{"type":"string","description":"result text of the reference SQL, produced at setup (D3)"}}}
```
Only `question` is an input; `sql_generated` and `sql_result` are expected outputs.

**Similar-question case** (`datasets/convergence_questions.json`, a list): `{"question": string}`, input only.

**Version** (`versions/<name>.json`):
```json
{"type":"object","required":["name"],"additionalProperties":false,
 "properties":{"name":{"type":"string","pattern":"^[A-Za-z0-9_-]+$"},
   "overrides":{"type":"object","additionalProperties":false,
     "properties":{"sql_generation_prompt":{"type":"string"},"system_prompt":{"type":"string"},
       "tool_descriptions":{"type":"object","additionalProperties":{"type":"string"}},
       "agent_model":{"type":"string"}}}}}
```
Anything not overridden takes the setting in the settings table. The version-name pattern is an addition.

**Run record** (what the task returns for one completed run; evaluators read only this):
```json
{"type":"object","required":["question","tool_calls","tool_responses","final_output","unchanged_messages","path_length"],
 "properties":{"question":{"type":"string"},
   "tool_calls":{"type":"array","items":{"type":"object","required":["name","arguments"],
      "properties":{"name":{"enum":["lookup_sales_data","analyze_sales_data","generate_visualization"]},
                    "arguments":{"type":"object"}}}},
   "tool_responses":{"type":"array","items":{"type":"object","required":["tool_name","tool_response"],
      "properties":{"tool_name":{"type":"string"},"tool_response":{"type":"string"}}}},
   "final_output":{"type":"string"},
   "unchanged_messages":{"type":"array","items":{"type":"object","required":["role"],
      "properties":{"role":{"enum":["system","user","assistant","tool"]}}}},
   "path_length":{"type":"integer","minimum":2,"description":"equals the number of unchanged_messages"}}}
```
`tool_calls` and `tool_responses` are in call order. A failed run (error or step limit) has no record.

**Results file** `results/<name>.json`: `version`, `evaluated_at` (ISO time), `overall` {`experiment_name`, `cases`: list of {`question`, `scores`: {evaluator → number}, `failed`: boolean}, `means`: {evaluator → number}}, `path` {`experiment_name`, `optimal_path_length`: integer, `cases`: list of {`question`, `path_length`: integer or null, `failed`: boolean, `score`: number}, `mean`: number}. Every score is between 0 and 1.

### Model roles
- **agent** — the router and every model step inside the skills (SQL generation, analysis, chart config, chart code); the course used one model for all of them.
- **judge** — every LLM judge (router tool calls, analysis clarity, entity correctness).

### Settings
| Setting | Value | Source | Change this when |
|---|---|---|---|
| agent model | course: `gpt-4o-mini` | Lesson 4 (Lab 1) code; same in Labs 2–5 | — |
| judge model | course: `gpt-4o` | Lessons 8 and 12 (Labs 3 and 5) code; Lesson 7 asks for "a GPT-4o or Claude3.5 Sonnet or similarly high-end model" | judges disagree with people too often |
| table name | `sales` | Lesson 4 code | — |
| system prompt | "You are a helpful assistant that can answer questions about the store sales dataset." | Lesson 4 code (course names its own dataset; the sample's name is used here) | you want to test a different router prompt (make it a version override) |
| SQL generation prompt | "Generate an SQL query based on a prompt. Do not reply with anything besides the SQL query." followed by the user's prompt, the available columns and the table name | Lesson 4 code | you test a different prompt (version override; sample v2 adds "Think before you respond.", Lesson 12) |
| analysis prompt | asks the model to analyze the given data and answer the given question | Lesson 4 code | — |
| chart config | one structured reply with `chart_type`, `x_axis`, `y_axis`, `title`; on an unreadable reply the fallback is `line`, `date`, `value`, title = the visualization goal | Lesson 4 code | — |
| chart code prompt | asks for Python code that draws a chart from the config, "Only return the code, no other text." | Lesson 4 code | — |
| tool descriptions | lookup: "Look up data from the store sales dataset", parameter `prompt` = "The unchanged prompt that the user provided."; analyze: "Analyze sales data to extract insights", parameters `data` = "The lookup_sales_data tool's output." and `prompt` as above; visualization: "Generate Python code to create data visualizations", parameters `data` as above and `visualization_goal` = "The goal of the visualization." | Lesson 4 code; Lesson 4 says descriptions are what you "end up changing a lot" | you test new descriptions (version override, Lesson 11) |
| judge explanation | on: each judge writes a reason with its label | Lessons 8 and 12 code | — |
| project name | `evaluating-agent` | Lesson 8 code (Lesson 6 used `tracing-agent`; the final labs' name is used) | — |
| test-set names | `overall_experiment_inputs-<YYYY-MM-DD HH:MM:SS>` and `convergence_questions-<YYYY-MM-DD HH:MM:SS>` (local time at upload) | Lessons 10 and 12 code | — |
| experiment names | `Overall Experiment <version>` and `Convergence Eval <version>` | Lessons 10 and 12 code, plus D9 | — |
| repetitions per version | 1 | Lessons 10 and 12 ran each experiment once; Lesson 12: "it's always good to do multiple runs of each experiment" | scores move between versions on a small test set; then run more and average |
| `max_router_calls` | 10 (addition) | none; safety limit (D6) | your agent legitimately needs more steps |
| `code_run_timeout_seconds` | 30 (addition) | none; safety limit (D5) | real chart code takes longer to run |
| displayed decimals | 2 | Lesson 11 slide of the experiment table shows two decimals | — |

## 6. Business rules

**The agent under test (C1a)**
- **R1. Agent loop.** The agent sends the conversation and the three tool definitions to the router model. When the reply contains tool calls, each is run in the order given and its result is appended as a tool message; then the router is called again. When a reply contains no tool calls, its text is the final answer and the run ends. One reply may contain several tool calls. → T3, T4, L1
- **R2. System message position.** If the conversation has no system message, one with the system prompt is appended after the user's message (the course's code appends it, so it sits second; keep this). → T3
- **R3. Every tool call gets its reply.** Before the next router call, every tool call has exactly one tool message carrying that call's id. → T5
- **R4. Lookup skill.** Loads the sample table into table `sales` if it is not already there; asks the agent model for SQL with the user's prompt, the column names and the table name; removes surrounding whitespace and any ```` ```sql ```` / ```` ``` ```` fences; runs the SQL; returns the result table as text. On any error it returns text starting `Error accessing data:` and the run continues. → T6, T7, L1
- **R5. Analysis skill.** One agent-model call with the data and the question; an empty reply becomes `No analysis could be generated`. → T8
- **R6. Visualization skill.** Two agent-model calls: first the structured chart config (fallback in the settings table when the reply cannot be read), then the chart code from that config; removes any ```` ```python ```` / ```` ``` ```` fences and returns the code as text. The agent never runs the code. → T9
- **R7. Step limit (addition).** A run that reaches `max_router_calls` router calls without a final answer stops and is a failed run. → T10

**Recording and evaluating**
- **R8. Every run is recorded.** A completed run returns the run record (section 5) with `path_length` = number of messages, counting the system and user messages. Every run is also traced to the recording backend as nested steps: one agent-run step; one router-call step per router call; one step for handling the tool calls; one tool step per tool run; inside the lookup tool a step for executing the SQL whose input is the cleaned SQL; inside the visualization tool one step each for the config and the code; and every model call. → T3, T11
- **R9. Judge calls are not part of the agent's record.** No judge's model call appears in an agent trace or in a run record. → T12
- **R10. Judges return a label, never a number.** Each LLM judge's prompt asks for a single word from its two labels and an explanation; the reply is matched to a label ignoring case and surrounding punctuation; a reply that matches neither label scores 0. Labels map to scores 1 (correct, clear) and 0 (incorrect, unclear). No judge is ever asked for a score on a scale. → T13, L2
- **R11. Router evaluator (`function_calling_eval`).** For each tool call in the record, the judge sees the question, the call (name and arguments) and all tool definitions, and answers `correct` or `incorrect`; "incorrect" means the tool would not answer the question, uses information not in the question, or has parameter values that do not fit the tool definitions. The run's score is the mean over its calls; a record with no tool calls scores 0. → T14
- **R12. Lookup evaluator (`evaluate_sql_result`).** Takes the first `lookup_sales_data` tool response; keeps only its digits and only the digits of the case's `sql_result`; scores 1 when they are equal, else 0. A record with no tool responses, or no lookup response, scores 1 (the course's code does this; keep it and see note N3). → T15
- **R13. Clarity evaluator (`evaluate_clarity`).** The judge sees the question and the final answer and answers `clear` (precise, coherent, directly answers) or `unclear` (ambiguous, poorly organized or not effectively communicated). → T16
- **R14. Entity evaluator (`evaluate_entity_correctness`).** The judge sees the question and the final answer and answers `correct` when every entity (store, product, date, name) in the answer is correctly named and fits the question's context, else `incorrect`. → T16
- **R15. Chart-code evaluator (`code_is_runnable`).** Takes the first `generate_visualization` tool response, removes fences, and runs it in a separate process, in a temporary working directory, with `code_run_timeout_seconds`; scores 1 when it exits without error, 0 on error or timeout. A record with no visualization response scores 1 (the course's code does this; see N3). The evaluator's own process is never affected by the code. → T17, T18
- **R16. Path evaluator (`Convergence Eval`).** Over one version's runs of the similar-question set: the optimal path length is the smallest `path_length` among completed runs; each completed run scores optimal ÷ its `path_length`; the version's path score is the mean over all runs. → T19
- **R17. Fixed test sets.** `setup` writes the two test sets once (section 7.1) and uploads them; every version is evaluated on exactly these cases; `setup` never overwrites existing test-set files. → T1, T2, T20
- **R18. Versions.** `evaluate --version <name>` builds the agent from `versions/<name>.json` and runs the overall set with the five evaluators of R11–R15 and the similar-question set with R16, `repetitions per version` times, under the experiment names in the settings table. → T20
- **R19. Comparison.** `compare` prints one row per evaluated version, in evaluation order, with columns: version, `function_calling_eval`, `evaluate_sql_result`, `evaluate_clarity`, `evaluate_entity_correctness`, `code_is_runnable`, `convergence`, optimal path length, failed runs; scores to 2 decimals. → T21
- **R20. Failed runs.** A failed run (an error, or R7) has no record; every overall evaluator scores it 0, the path evaluator scores it 0 and leaves it out of the optimal path length, and the comparison counts it under failed runs. → T10, T17, T19, T21
- **R21. Fresh start.** On an empty folder, `setup` creates the sample table file, the two test-set files, `versions/v1.json` and `versions/v2.json`, and `results/`, and the recording backend has project `evaluating-agent` and both test sets. → T1, T2

### What must stay true (the course's pattern card)
Every option of every question keeps all four.
- **MST1. The agent is judged part by part, not only by its final answer.** The router's choice of tool, the arguments it passes to that tool, and each skill's output each get their own evaluator, so a failure points to the part that caused it. → T14, T15, T16, T17, T21
- **MST2. Every run leaves a record of its steps, and the evaluators score that record.** For each run the record holds the question, each router decision, each tool call with its arguments and result, the final answer and the number of steps; evaluators read the parts they judge from it. → T3, T11
- **MST3. The path the agent takes is measured, not only what it outputs.** Similar questions are run through the agent, the steps of each run are counted, and each run is compared with the shortest path seen for that kind of question. → T19
- **MST4. One fixed set of test cases is run through every version of the agent, and the scores are compared side by side.** A change to the agent (a prompt, a tool description, the model, the logic) is judged by re-running the same test set through all the evaluators and comparing the new version's scores with the old one's. → T20, T21

## 7. Tests

### 7.1 Sample data

**Sample table** (`data/sample_sales.parquet`, written by `setup`; facts written for this spec):

| # | Sold_Date | Store_Number | SKU_Coded | Qty_Sold | Total_Sale_Value | On_Promo |
|---|---|---|---|---|---|---|
| 1 | 2021-11-01 | 1320 | 6200700 | 2 | 10.00 | 1 |
| 2 | 2021-11-01 | 1320 | 6200800 | 1 | 4.50 | 0 |
| 3 | 2021-11-02 | 2970 | 6200700 | 3 | 15.00 | 1 |
| 4 | 2021-11-02 | 2970 | 6201000 | 1 | 20.00 | 0 |
| 5 | 2021-11-15 | 880 | 6200800 | 2 | 9.00 | 0 |
| 6 | 2021-11-20 | 2970 | 6200700 | 4 | 20.00 | 0 |
| 7 | 2021-12-01 | 1320 | 6201000 | 1 | 20.00 | 1 |
| 8 | 2021-12-05 | 880 | 6200700 | 1 | 5.00 | 0 |
| 9 | 2021-12-10 | 2970 | 6200800 | 2 | 9.00 | 0 |
| 10 | 2021-12-20 | 1320 | 6200700 | 2 | 10.00 | 0 |

Derived facts: units per SKU 6200700 = 12, 6200800 = 5, 6201000 = 2; total sales value 122.50; value per store 1320 = 44.50, 2970 = 64.00, 880 = 14.00; units per store 1320 = 6, 2970 = 10, 880 = 3; 3 of 10 transactions on promotion (30.0%); average transaction value 12.25; average units per transaction 1.9; 2021 value by month: November 78.50, December 44.00.

**Overall test set** (`datasets/overall_questions.json`; `sql_result` is produced by `setup` from the reference SQL, D3):

| id | question | reference SQL (behaviour) | result holds |
|---|---|---|---|
| O1 | Which product SKU sold the most units? | SKU with the largest summed `Qty_Sold`, top 1 | 6200700, 12 |
| O2 | What was the total sales value across all stores? | sum of `Total_Sale_Value` | 122.5 |
| O3 | Which store had the highest total sales value? | store with the largest summed `Total_Sale_Value`, top 1 | 2970, 64 |
| O4 | Make a bar chart of total sales value by store | summed `Total_Sale_Value` per store, ordered by `Store_Number` | 880 14, 1320 44.5, 2970 64 |
| O5 | What share of transactions had a promotion? | 100 × sum of `On_Promo` ÷ row count | 30 |
| O6 | What was the average value of a transaction? | mean of `Total_Sale_Value` | 12.25 |
| O7 | Draw a line chart of monthly sales value in 2021 | summed `Total_Sale_Value` per month of 2021, ordered by month | 11 78.5, 12 44 |

**Similar-question set** (`datasets/convergence_questions.json`): K1 "What was the mean number of units per transaction?" · K2 "On average, how many units are in one transaction?" · K3 "How many items does one sale contain on average?" · K4 "Work out the usual quantity in a transaction" · K5 "How many units does a customer buy per transaction on average?" · K6 "What's the average basket size in units?"

**Versions:** `v1` has no overrides. `v2` overrides `sql_generation_prompt` with the default prompt plus a final line "Think before you respond." (the course's own change in Lesson 12).

**Test-only questions** (used by single tests, not in any test set): P "Show data and analysis together", E "Analyze nothing", LOOP "Keep looking up sales", HELLO "Hello".

**Scripted stand-in model (a stand-in for the real provider; used by every offline test).** It answers per role, keyed as below; a request it has no reply for fails the test loudly.

*Agent role, router* (keyed by the user question and how many router calls this run has already made; "data = last tool reply" means the text of the latest tool message):

| question | step 1 | step 2 | step 3 |
|---|---|---|---|
| O1, O2, O3, O6 | call `lookup_sales_data`(prompt = the question) | call `analyze_sales_data`(prompt = the question, data = last tool reply) | final answer (below) |
| O4, O7 | call `lookup_sales_data`(prompt = the question) | call `generate_visualization`(data = last tool reply, visualization_goal = the question) | final answer = text below + the code text |
| O5 | call `analyze_sales_data`(prompt = the question, data = "") — planted wrong tool | call `lookup_sales_data`(prompt = the question) | final answer |
| K1–K4 | call `lookup_sales_data`(prompt = the question) | final answer "The average is 1.9 units per transaction." | — |
| K5 | call `lookup_sales_data`(prompt = the question) | call `lookup_sales_data` again, same prompt — planted repeated step | final answer as K1 |
| K6 | raises a provider error — planted failed run | — | — |
| P | one reply with two calls: `lookup_sales_data`(prompt = P) and `analyze_sales_data`(prompt = P, data = "") | final answer "Done." | — |
| E | call `analyze_sales_data`(prompt = E, data = "x") | final answer "Nothing to report." | — |
| LOOP | call `lookup_sales_data`(prompt = LOOP), at every step | — | — |
| HELLO | final answer "Hi! Ask me about store sales." | — | — |

Before every router reply, the stand-in raises "tool reply missing" if any earlier tool call lacks a tool message with its id (used by T5).

Final answers: O1 "SKU 6200700 sold the most units, 12 in total." · O2 "Total sales value across all stores was 122.50.", or, when its lookup reply starts with `Error accessing data:` (as under v2), "I could not retrieve the total sales value because the query failed." · O3 "Store 2970 had the highest total sales value." · O4 "Here is the code for a bar chart of total sales value by store:" · O5 "30% of transactions had a promotion." · O6 "The average transaction value was 12.25, at store 6200700." (planted entity mix-up: a SKU called a store) · O7 "Sales went up and down, see chart." (planted unclear answer).

*Agent role, SQL generation* (keyed by the question inside the prompt and whether the prompt contains "Think before you respond."): every O and K question returns its reference SQL, under both versions, except: O1 returns its reference SQL wrapped in ```` ```sql ```` fences (planted fence); O3 returns SQL that sums `Qty_Sold` instead of `Total_Sale_Value` (planted wrong SQL: result 2970, 10); O2 under v2 returns "Let me think step by step. " followed by the reference SQL (planted regression: the SQL fails). K questions' reference SQL is the mean of `Qty_Sold`. P and LOOP return O2's reference SQL.

*Agent role, analysis*: returns "Analysis: " plus the first 40 characters of the data; for question E returns an empty reply; for data "" returns "No data was provided to analyze."

*Agent role, chart config* (keyed by the visualization goal): O4 {bar, Store_Number, Total_Sales, "Total sales value by store"}; O7 {line, Month, Total_Sales, "Monthly sales value in 2021"}; goal "odd chart" returns an unreadable reply.

*Agent role, chart code* (keyed by the config's title): O4's config returns, inside ```` ```python ```` fences, one line that prints an undefined name `totals_by_store` (planted code that does not run); O7's config returns three lines that build the lists `[11, 12]` and `[78.5, 44.0]` and print them zipped, standard library only; any other config returns `print("chart")`.

*Judge role*: tool-call judge answers "incorrect" for the call `analyze_sales_data` with data "", "Correct" (capital C) for both calls of O2, "correct" otherwise. Clarity judge answers "unclear" for O7's final answer, "clear" otherwise. Entity judge answers "incorrect" for O6's final answer, "correct" otherwise. Every judge reply includes an explanation "Scripted reason." For the single test of R10's no-match case, a judge reply "maybe".

### 7.2 Test table
Every test runs offline against the stand-in and a local Phoenix started by the test setup in a temporary working directory (under C4c: the local files), except tests marked `live`.

| Test | Rules | Given | When | Then |
|---|---|---|---|---|
| T1 | R17, R21 | an empty folder | `setup` | `data/sample_sales.parquet` has 10 rows and exactly the six columns of section 5; `datasets/overall_questions.json` has 7 cases, `datasets/convergence_questions.json` has 6; `versions/v1.json` and `versions/v2.json` exist; `results/` exists; running `setup` again leaves both test-set files byte-identical |
| T2 | R17, R21 | after T1 | read the backend | project `evaluating-agent` exists; two test sets whose names match `overall_experiment_inputs-` / `convergence_questions-` + `YYYY-MM-DD HH:MM:SS`; the overall set has input key `question` and output keys `sql_result`, `sql_generated`; O1's `sql_result` contains `6200700` and `12`; O3's contains `2970` and `64` |
| T3 | R1, R2, R8, MST2 | v1 | run O1 | record: `tool_calls` = [`lookup_sales_data` {prompt: O1}, `analyze_sales_data` {prompt: O1, data: the lookup result text}]; first `tool_responses` entry has `tool_name` `lookup_sales_data` and contains `6200700`; `final_output` = O1's final answer; message roles = user, system, assistant, tool, assistant, tool, assistant; `path_length` = 7 |
| T4 | R1 | v1 | run P | both calls of the single reply run in order; two tool messages follow that reply; `final_output` "Done."; `path_length` = 6 |
| T5 | R3 | v1 | run O1 | the stand-in never raised "tool reply missing"; every assistant tool-call id appears in exactly one tool message |
| T6 | R4 | v1 | run O1 | the SQL executed is O1's reference SQL without fences; the lookup result does not start with `Error accessing data:` |
| T7 | R4 | v2 | run O2 | the lookup result starts with `Error accessing data:`; the run still ends with O2's error-case final answer; `path_length` = 7 |
| T8 | R5 | v1 | run E | the analyze tool response is `No analysis could be generated` |
| T9 | R6 | v1 | run O4; then call the visualization tool with data "d" and goal "odd chart" | O4's `generate_visualization` response is the one `print(totals_by_store)` line without fences, and the run completes (the code was not run); for "odd chart" the config sent to the chart code step is `line`, `date`, `value`, title "odd chart" |
| T10 | R7, R20 | v1, `max_router_calls` 10 | run LOOP | the router was called exactly 10 times; no record is returned; the run is reported as failed |
| T11 | R8, MST2 | v1, local Phoenix | `ask` O1 | project `evaluating-agent` has one new trace with one agent-run step, three router-call steps, one `lookup_sales_data` tool step containing one SQL-execution step whose input is O1's reference SQL without fences, one `analyze_sales_data` tool step, and at least 5 model-call steps (3 router, 1 SQL, 1 analysis) |
| T12 | R9 | after `evaluate --version v1` | search every recorded agent trace and run record | no model-call step or message contains the clarity judge's prompt or the tool-call judge's prompt; O1's `path_length` is still 7 |
| T13 | R10 | after `evaluate --version v1`; separately, the "maybe" reply | read O2's router scores; score the "maybe" reply | O2's two calls are labelled `correct` (from "Correct") and score 1; every stored label is one of its judge's two labels and has the explanation "Scripted reason."; "maybe" scores 0; each judge prompt names its two labels and asks for one word |
| T14 | R11, MST1 | after `evaluate --version v1`; separately, a record of HELLO | read `function_calling_eval` | O5 = 0.5; O1 = 1; HELLO record = 0; overall mean 0.93 (6.5 ÷ 7) |
| T15 | R12, MST1 | after `evaluate --version v1`; separately, a record with no tool responses | read `evaluate_sql_result` | O1 = 1, O4 = 1, O5 = 1, O3 = 0; the no-response record = 1; overall mean 0.86 (6 ÷ 7) |
| T16 | R13, R14, MST1 | after `evaluate --version v1` | read clarity and entity scores | clarity: O7 = 0, others 1, mean 0.86; entity: O6 = 0, others 1, mean 0.86 |
| T17 | R15, R20, MST1 | after `evaluate --version v1`; separately, a missing record | read `code_is_runnable` | O4 = 0; O7 = 1; O1 = 1 (no visualization call); the missing record = 0; overall mean 0.86 (6 ÷ 7) |
| T18 | R15 | `code_run_timeout_seconds` 2 | score code that loops forever; then score code that writes `escape.txt` to its working directory; then score O7's code | the loop scores 0 and the check returns within 10 seconds; `escape.txt` does not exist in the project folder; O7's code still scores 1 afterwards |
| T19 | R16, R20, MST3 | after `evaluate --version v1` | read the path experiment | path lengths K1–K4 = 5, K5 = 7, K6 failed; optimal path length 5; scores 1, 1, 1, 1, 0.71 (5 ÷ 7), 0; mean 0.79 (4.714 ÷ 6) |
| T20 | R17, R18, MST4 | after `evaluate --version v1` then `--version v2` | read both results files | both ran the same 7 and 6 questions, once each; experiments are named `Overall Experiment v1`, `Overall Experiment v2`, `Convergence Eval v1`, `Convergence Eval v2`; v2's SQL prompts contain "Think before you respond."; v2's `evaluate_sql_result` mean is 0.71 (O2 and O3 score 0) |
| T21 | R19, R20, MST1, MST4 | after T20 | `compare` | two rows in order v1, v2: `function_calling_eval` 0.93 / 0.93; `evaluate_sql_result` 0.86 / 0.71; `evaluate_clarity` 0.86 / 0.86; `evaluate_entity_correctness` 0.86 / 0.86; `code_is_runnable` 0.86 / 0.86; `convergence` 0.79 / 0.79; optimal path length 5 / 5; failed runs 1 / 1 |
| L1 `live` | R1, R4 | real agent model, sample table | `ask` O3 | the record has at least one `lookup_sales_data` call and the final answer contains `2970` (2970 leads by value and by units, so either SQL reading passes) |
| L2 `live` | R10 | real judge model | score O1's v1 record with the three judges | every label is one of its judge's two labels and has a non-empty explanation |

## 8. Standing permissions
- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has data; anything that sends data to a third party (including a hosted trace service).
- **Never:** invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets.

## 9. Test plan
1. `pip install` the stack in section 4, then `python -m agent_evals setup`.
2. Offline: `pytest -m "not live"`. Report each of T1–T21 with its pytest result line and, where it reads files, the file paths.
3. Live, once `OPENAI_API_KEY` is set: `pytest -m live` (L1, L2). Skipped without a key; that is not a failure.
4. End to end: `python -m agent_evals evaluate --version v1`, `python -m agent_evals evaluate --version v2`, `python -m agent_evals compare`; paste the table.
5. For each chosen option that is not recommended, turn its "what to check" sentence into a test, run it and report it.
6. Report a result per test with evidence (test output, file paths); "should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.

Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

## 10. Background notes

### N1. The program
Stages, in order, and why each exists:
1. **Agent under test** — a router that picks among skills; the thing being improved (Lessons 3–4).
2. **Record** — every run is traced step by step; "these traces will become the bedrock that is used to run evaluation" (Lesson 5).
3. **Fixed test sets** — one set of representative questions with expected outputs where possible, and one set of similar questions for the path (Lessons 10–11).
4. **Run a version** — every test case goes through one named version of the agent; this is an experiment (Lessons 10–12).
5. **Evaluate part by part** — the router's tool calls by an LLM judge; the lookup skill by number comparison; the analysis by clarity and entity judges; the chart code by a run check; the path by convergence (Lessons 7–10, 12).
6. **Compare versions** — the same scores side by side per version, so a change's effect on every part is visible (Lessons 11–12).

The sales-data assistant (C1a) is the course's sample instance, not the program; its tools, prompts and table are rules of the recommended build.

### N2. Failures
- **Wrong tool or wrong parameters (demonstrated).** Lesson 7 shows a router that picks the right function but passes an order number as a shipping tracking id; Lessons 8 and 12 show the router judge finding incorrect calls. Why: the router is an LLM reading tool descriptions. Prevented by the per-call router judge (R11); planted in O5; tested by T14.
- **Wrong SQL (demonstrated).** Lesson 12's overall experiment shows "some issues with SQL generation". Why: the model writes SQL from a short prompt and column names. Caught by R12; planted in O3; tested by T15.
- **SQL wrapped in markdown (demonstrated).** Lesson 4: the model "doesn't just respond with code. Sometimes it includes that extra SQL bit". Prevented by fence removal (R4); planted in O1; tested by T6.
- **Chart code that does not run (demonstrated).** Lesson 8: "it looks like the generated code wasn't runnable. So in this case it's good eval caught that". Caught by R15; planted in O4; tested by T17.
- **A small prompt change breaks a case (demonstrated).** Lesson 2's slide shows an added "Remember to respond politely" fixing two cases and breaking one; Lesson 12's v2 prompt did not fix SQL and some answers came back less clear. Caught by re-running the fixed sets per version and comparing (R17–R19); planted as v2's O2 reply; tested by T20, T21. The specific v2 failure (reasoning text breaking the SQL) is invented for the sample.
- **Missing tool reply (warned).** Lesson 4: if a tool message with the call id is not sent back, the provider will "actually error". R3, T5.
- **Judge calls polluting the traces (warned).** Lesson 8: without turning tracing off, "you would actually see some spans tracked to your project for all of the evaluation calls". R9, T12. (The course's Lab 5 evaluators did not turn it off; the instructor's rule is followed.)
- **Incomplete runs skewing convergence (warned).** Lesson 9: a run that errors after three steps "will skew your convergence evaluation data". R16, R20, planted K6, T19. The course's code scores such a run 0 and leaves it out of the minimum; kept.
- **Numeric judge scores (warned, never offered).** Lesson 7: "never a measure like score this response on a scale from 1 to 100", because LLMs cannot tell 83 from 79. R10, T13.
- **Errors cascading through the agent (warned).** Lesson 4: a response that breaks halfway should not "cascade and break everything else". R4, R5, T7, T8.
- **Running generated code unsafely (warned).** Lesson 4: code from an LLM "could do things that you don't expect"; run it "within an enclosed environment". The agent never runs code (R6); the evaluator runs it in a separate process with a time limit (R15, T18).
- **Mixing up entities (warned).** Lesson 12: the entity judge makes sure the agent "doesn't start referring to SKU or skew columns as store IDs". R14; planted in O6; T16.
- **Getting stuck in a loop (warned).** Lesson 1: evaluate the path "to ensure it doesn't get stuck in a loop or repeat steps unnecessarily". Measured by R16 (planted K5); a run is also cut off by R7 (addition), T10.
- **Limits that remain:** convergence does not catch an unnecessary step taken on every run, because that step is inside the minimum (Lesson 9); a chart can run yet "look slightly off" (Lesson 4), which the run check does not see; judges are never 100% accurate (Lesson 7).

### N3. Notes for the build agent on course code kept as is
- The system message is appended after the user's message, so it is second in the list (R2); path lengths count it.
- `evaluate_sql_result` and `code_is_runnable` score 1 when the run never called their tool. This makes their means look better on questions that do not use the tool; it is the course's behaviour and is kept.
- The number comparison drops decimal points and keeps the result table's row numbers, so it also depends on row order (hence D4).
- In Lesson 8 the router judge was fed the tool definitions offered to the model (the `llm.tools` attribute) as the "tool call"; Lesson 12's final version feeds the actual calls from the record, and that is what R11 uses.

### N4. Why the questions and settings are what they are
- **C1** — the pattern card's scope decision: the program is the evaluation setup; a learner may bring a different router-and-skills agent. Lesson 11: expected outputs "unlock different types of evaluations"; Lesson 7: judges are never 100% accurate.
- **C2** — the sample replaces the course's file (D1); own data needs its own ground truth because the lookup check compares with expected results (Lesson 12).
- **C3** — Lesson 7: "only really the best models actually align closely with human judgment… GPT-4o or Claude3.5 Sonnet or similarly high-end model".
- **C4** — Lesson 6: Phoenix can be launched in a notebook, "run it on your own local machine, or you can access it through a web app"; the local server needs no account, so it stays recommended; plain files are the lighter option.
- **C5** — Lessons 11 and 13 list both a code comparison with the expected tool and the function-calling judge for the router; Lesson 12 had no expected tool and used the judge only. An exact comparison alone was not offered: it does not check the arguments, which MST1 requires.
- **C6** — Lesson 7 and Lesson 8 judged SQL with an LLM; Lesson 12 compared with ground truth and called it "generally going to be a more accurate kind of evaluation", but it "relies on you having those expected values".
- **C7** — the pattern card offers human labels from Lessons 7 and 14; Lesson 7: human labels are "flexible and deterministic" but "hard to get… at scale", and end-user feedback has "selection bias".
- **Subjects that are not questions:**
  - Router form (LLM, classifier, rules), routing spread across the agent, one or several tool calls per router step, loop or recursion — these belong to the agent under test; a learner with a different agent picks C1b.
  - Letting the agent run its own code — belongs to the agent under test (C1b); the course left it out "to keep things safe".
  - Judges giving numeric scores — the course forbids it (R10).
  - Evaluating traces of ad-hoc runs without a fixed test set (Lesson 8, an earlier stage) — breaks MST4.
  - Tracing only, or an agent without evaluators (Lessons 4–6, earlier stages) — break MST1–MST4.
  - Leaving out the path measure, the router judge, or the comparison — break MST3, MST1, MST4.
  - Testing the judges against labelled answers (Lesson 13), production monitoring, CI gates, self-improving agents and feeding production runs into the test sets (Lesson 14) — not part of this program: the pattern card offers only human labels from other lessons.
  - Semantic similarity for free-text expected outputs (Lessons 7, 13) — no recommended check compares free text; a C1b learner may use it as an evaluator after the build.
  - Different or extra evaluators for the analysis and chart skills — Lesson 7 calls choosing evals "more of an art than a science"; the recommended set is the course's, and changes are made after the build.
  - The prompt playground (Lesson 12) — a viewing tool inside Phoenix, not a stage.
  - Test-set size — the Lesson 11 slide says "25+ examples", the narration asks for "1 or 2 examples from each of the different types of inputs"; the narration wins (slide only), and the sample keeps the course's 7.
  - Model temperature and similar request settings — the course set none.
  - Tracing style (automatic instrumentation of model calls plus hand-marked steps, decorators or blocks) — how the trace is produced may differ; R8 fixes what it must contain.
- **Picked values:** clarity judge wording — Lesson 8 and Lesson 12 define "unclear" differently ("some part of the response could be better structured or worded" vs "ambiguous, poorly organized, or not effectively communicated"); Lesson 12's wording is used (rule 2, final app). Project name — `tracing-agent` (Lesson 6) vs `evaluating-agent` (Lessons 8 onward); the later is used (rule 2). Router model label — most slides say GPT-4o-mini, a few say GPT-4o; the code uses `gpt-4o-mini` for the agent (code wins over slides). SQL evaluator — LLM judge (Lesson 8) vs number comparison (Lesson 12, and the Lesson 7 slide that keeps only the code-based check); the final app's comparison is used (rule 2).

### N5. Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports: OpenAI `chat.completions.create`, `beta.chat.completions.parse` with a pydantic `response_format`; `duckdb.sql(...).df()`; pandas `read_parquet`; Phoenix `px.Client`, `launch_app`, `phoenix.otel.register`, `SpanQuery`, `query_spans`, `log_evaluations`, `SpanEvaluations`, `upload_dataset`, `run_experiment`, `evaluate_experiment`, `create_evaluator`, `Example`; Phoenix evals `llm_classify` (its data argument was `dataframe=` in Lab 3 and `data=` in Lab 5), `OpenAIModel`, `TOOL_CALLING_PROMPT_TEMPLATE`; OpenInference `OpenAIInstrumentor`, `suppress_tracing`, `TracerProvider`, `SpanAttributes`; OpenTelemetry `StatusCode`; `nest_asyncio` (needed only inside notebooks); `python-dotenv`. Models: `gpt-4o-mini` (agent), `gpt-4o` (judge), "Claude3.5 Sonnet" (named as an alternative judge). The course set no temperature, so request-parameter limits of newer models do not conflict with it.

### N6. Course names
- Tools `lookup_sales_data`, `analyze_sales_data`, `generate_visualization` — binding: evaluators find responses by these names.
- Evaluators `function_calling_eval`, `evaluate_sql_result`, `evaluate_clarity`, `evaluate_entity_correctness`, `code_is_runnable`, "Convergence Eval" — binding as comparison column names (convergence shown as `convergence`).
- Record keys `tool_calls`, `tool_responses`, `final_output`, `unchanged_messages`, `path_length`; test-set keys `question`, `sql_result`, `sql_generated` — binding.
- Trace steps `AgentRun`, `router_call`, `handle_tool_calls`, `execute_sql_query`, `extract_chart_config`, `create_chart` — the course's step names; R8 fixes what is traced, the names are recommended.
- Table `sales`; column names follow the course's (`Store_Number`, `SKU_Coded`, `Sold_Date`, `Qty_Sold`, `Total_Sale_Value`, `On_Promo`); the course's helper names `run_agent`, `start_main_span`, `process_messages`, `run_agent_task`, `run_agent_and_track_path`, `update_sql_gen_prompt` map to `ask`, the run record and versions here.

### N7. Lesson map (transcript numbering)
1 Introduction — program scope, path and loop warning (N2). 2 Evaluation in the time of LLMs — regressions from small changes, consistent test sets (MST4, N2). 3 Decomposing agents — router, skills, memory; the sample agent and its tool steps (R1–R6). 4 Lab 1: Building your agent — prompts, tools, router loop, fences, tool-reply ids, error handling, code safety (settings, R1–R6, N2, N3). 5 Tracing agents — traces and spans as the basis of evaluation (R8, MST2). 6 Lab 2: Tracing your agent — step kinds and names, Phoenix launch modes (R8, C4, N6). 7 Adding router and skill evaluations — three techniques, label-only judges, router checks, skill evals (R10–R15, C5–C7). 8 Lab 3 — router, SQL, clarity and code evals on traces, suppressing judge traces (R9, N3, C6). 9 Adding trajectory evaluations — convergence, its formula and limits (R16, N2). 10 Lab 4 — path experiment, similar questions, path length counting (R16, D8). 11 Adding structure to your evaluations — evaluation-driven development, experiments, test-set curation (R17–R19, C5). 12 Lab 5 — overall experiment, five evaluators, v2 prompt change, comparison (R11–R15, R17–R19, N2). 13 Improving your LLM-as-a-judge — judge testing (not part of this program, N4). 14 Monitoring agents — human labels on the card (C7); monitoring and CI out of scope (N4). 15 Conclusion.
Slides: descriptions of all 116 slides were read; a slide the instructor talks through counted like its lesson's transcript; slide-only content counted less and lost where it disagreed (test-set size, router model label). Nothing in this spec requires access to the course.

---
*v2-draft · Evaluating AI Agents · spec-build-lab · when the build agent does something unexpected, add the missing constraint here and re-run*
