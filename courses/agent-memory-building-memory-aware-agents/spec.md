# Spec: a memory-aware tool-using agent

**What you're building:** a tool-using assistant that keeps its memory in a database outside the model, so it carries on across turns and sessions. By default it is a research assistant that finds papers, saves them and discusses them. You ask it something on a conversation thread. It loads what it remembers about that thread and your request, picks the few tools that fit, answers, and saves what happened. When the conversation grows, it shrinks old turns into a summary it can open again later. Quit, start it again, and it carries on where you left off.

**What the recommended build needs to run:** an OpenAI API key (paid account), network access (model calls and the arXiv paper service), and a one-time download of the course's embedding model with PyTorch, a few hundred MB. No database server is needed.

**Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once `OPENAI_API_KEY` is set and are skipped until then; that is not a failure.

This file is self-contained: everything the build needs is in it.

*Provenance: course "Agent Memory: Building Memory-Aware Agents". Materials used: the notebooks file (four lesson notebooks), `helper.py`, `requirements.txt`, the transcripts for Lessons 1–7, and 60 slide images. Pattern card confirmed by the owner. Generated 2026-10-27 with guide v2.8 (2026-10-27).*

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
   an OpenAI API key, network access, and a one-time download of the embedding model with PyTorch), or **choose** question by
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

Context questions come first, then the program's stages in order (store → register tools → assemble context → shrink → select tools → run the loop → persist).

### C1. What should the agent help with, and what does it start out knowing?
- **C1a (Recommended - course default)** — A research assistant for papers. It starts with a small knowledge base of paper records and has tools to search arXiv and save a paper's full text into memory. *Pick this when* you want the course's assistant working first, or you read research papers. *Setup:* network access to arXiv; no key.
- **C1b** — Your own topic. You give a folder of your own text or Markdown files to load into the knowledge base. You also name the tools the agent needs; it may need none beyond the memory tools. The paper tools are left out unless you ask for them. *Pick this when* you want an assistant that remembers your own project, e.g. "my cooking notes and the meal plans we discussed". *Setup:* your documents; any tool you name may need its own key.
  - *What to check:* after your documents are loaded, a new session answers a question from one of their passages. On the same thread it still remembers what the earlier session said.

### C2. Which model provider runs the agent?
- **C2a (Recommended - course default)** — OpenAI. *Pick this when* you have, or can get, an OpenAI key. *Setup:* `OPENAI_API_KEY`, paid account.
- **C2b** — Another hosted provider whose models can call tools, e.g. Anthropic. *Pick this when* you already pay for that provider, or your organisation only allows it. *Setup:* that provider's API key.
  - *What to check:* one agent turn that calls a tool works through this provider's tool-calling format, and the final answer is saved to conversation memory.
- **C2c** — A local model served by Ollama. *Pick this when* your conversations must not leave your machine, or you have no paid key. *Setup:* install Ollama and download a model, typically several GB, on a machine with enough memory. Small local models call tools less reliably; C11b suits them.
  - *What to check:* one agent turn that calls a tool runs with no network access to any model provider, and the final answer is saved to conversation memory.

### C3. How will you use it?
- **C3a (Recommended)** — A command-line chat on your machine. You choose a thread id, type messages, and see the answers plus a one-line context-usage status. *Pick this when* only you use it, on your own machine. *Setup:* none.
- **C3b** — A small web chat page served on your machine. *Pick this when* you prefer a browser, or want to show it to others on your network. *Setup:* one web framework package.
  - *What to check:* two messages sent from the page on the same thread id get a second answer that uses the first one. After the server restarts, the thread is still there.

### C4. Where is memory stored?
- **C4a (Recommended)** — One SQLite database file on your disk. The program does the similarity search itself over the stored vectors. *This is a stand-in for the course's Oracle AI Database:* it keeps the same seven stores and the same behaviour without running a database server. *Pick this when* you are one user with up to tens of thousands of stored memories. *Setup:* none (Python's standard library).
- **C4b (course default)** — Oracle AI Database (the course used 26ai) with vector tables and vector indexes. *Pick this when* you already run Oracle, or your stores grow so large that scanning every row on each turn is slow. *Setup:* a running Oracle Database container or service, an admin login to create the application user, and its connection settings.
  - *What to check:* all seven stores exist as tables, the five vector stores have vector indexes, and memory written by one process is read by another.

### C5. Which embedding model turns text into vectors?
- **C5a (Recommended - course default)** — The course's local sentence-transformers model `paraphrase-mpnet-base-v2`, which makes 768-number vectors. *Pick this when* you can download a few hundred MB once and install PyTorch. *Setup:* a one-time model download plus PyTorch.
- **C5b** — The built-in word-hash embedder, the same one the offline tests use. *It is a stand-in for the course's embedding model:* it matches shared words, not meaning, so "car" will not find "automobile". *Pick this when* the machine cannot download models or install PyTorch. *Setup:* none.
  - *What to check:* a stored passage is found by a query that shares its key words, and the program never downloads a model.

### C6. Which kinds of memory does the agent keep?
- **C6a (Recommended - course default)** — The full set: conversation, knowledge base, workflow (past step sequences), entity (named people, places, systems) and summary memory. *Pick this when* the agent does repeated multi-step tasks, tracks names, or holds long conversations. *Setup:* none.
- **C6b** — Conversation, knowledge base and summary memory, without workflow or entity memory. *Pick this when* the agent answers one-off questions about documents and rarely repeats a multi-step task or needs to track people and things. *Setup:* none. *Cost:* past step sequences are not reused, and names are not tracked between turns. The course keeps workflow memory so that repeated multi-step tasks are faster and use less context.
  - *What to check:* the workflow and entity stores are never created and the context has no Workflow or Entity section. Conversation, knowledge base and summary memory pass the recommended tests.
- **C6c** — Conversation memory only. This is the simplest memory agent the course shows, the one that "remembers" by storing the chat log. *Pick this when* you want a chat companion that only needs to remember what was said, across sessions, on short threads. *Setup:* none. *Cost:* the course's own point is that chat logs alone are not enough. Nothing outside the chat is remembered as structured knowledge, and turns beyond the conversation window never come back. Tools that save into the knowledge base are left out.
  - *What to check:* a new session on the same thread sees the earlier messages in its context, and no knowledge-base, workflow, entity or summary store is created.

### C7. How does the agent get its tools each turn?
- **C7a (Recommended - course default)** — Toolbox memory. Each tool's description is stored as a vector. On each turn, the 5 tools whose descriptions best match the question are offered to the model. *Pick this when* you expect many tools; the course designs for tens to hundreds. *Setup:* none.
- **C7b** — Every tool is offered on every turn. *Pick this when* you will have fewer than about 10 tools and want a simpler program. *Setup:* none. *Cost:* the course warns that many tool definitions bloat the context, confuse tool choice, and raise cost and latency. Model providers recommend roughly 10–20 tools at most.
  - *What to check:* every registered tool appears in every model call's tool list, and no toolbox store is created.
- **C7c** — Toolbox memory, plus a tool the agent can call mid-turn to search the toolbox. The tools it finds are added to the tools offered in the next model call of the same turn. *Pick this when* you have hundreds of tools and the first 5 often miss the one needed. *Setup:* none. *Cost:* extra model calls, and the agent must recognise that it lacks a tool.
  - *What to check:* when the offered tools lack one the agent needs, it calls the toolbox search, and then calls the tool it found in the same turn.

### C8. Should the model rewrite tool descriptions before they are stored? — *Ask only when C7 is C7a or C7c.*
- **C8a (Recommended - course default)** — Rewrite them for each tool flagged to be rewritten, as the course does. The model writes a richer description and 5 example requests, and that text is what gets embedded. Tools not flagged use their own description. *Pick this when* your tool descriptions are short or similar to each other. *Setup:* one model call per rewritten tool, once, at registration.
- **C8b** — Never rewrite: embed each tool's own description. *Pick this when* your descriptions are already detailed, or you want tools registered without model calls. *Setup:* none. *Cost:* the course says rewritten descriptions keep tools further apart in the search and find the right one more often.
  - *What to check:* registering tools makes no model calls, and each tool's stored search text is its name, its own description and its parameter names.

### C9. Should the agent also search the web? — *Ask only when C6 is C6a or C6b.*
- **C9a (Recommended - course default)** — No web search. *Pick this when* your papers or documents, and the tools of C1, cover what the agent needs. *Setup:* none.
- **C9b** — Add a web-search tool (the course used Tavily) that saves every result into the knowledge base, so later questions find it without searching again. *Pick this when* your questions need current information beyond your papers or documents. *Setup:* a Tavily API key (account).
  - *What to check:* a web-search call writes each result to the knowledge base with its title, URL, score, query and time, and a later question retrieves it without a new search.

### C10. How should the knowledge base be searched? — *Ask only when C6 is C6a or C6b.*
- **C10a (Recommended - course default)** — By meaning: vector similarity, top 3 passages. *Pick this when* questions are asked in everyday words rather than exact codes. *Setup:* none.
- **C10b** — Hybrid: meaning plus exact keyword match, with the two result lists merged. *Pick this when* your documents are full of exact identifiers (part numbers, error codes, paper ids) that a meaning search blurs. *Setup:* none with C4a (a keyword index in the same file); a text index with C4b. *Cost:* a keyword index to keep up to date, and a rule for merging two kinds of score.
  - *What to check:* a query containing an exact identifier that appears in only one stored passage returns that passage first, and queries by meaning still work.

### C11. Who decides when memory work happens? — *Ask only when C6 is C6a or C6b.*
- **C11a (Recommended - course default)** — The work is split as the course splits it. Before each answer, the program always loads every memory section. After each answer, it always saves the conversation, the workflow and the entities. It also summarizes automatically once the context passes 80%. The agent decides on its own when to summarize early and when to open a summary. *Pick this when* your model calls tools reliably and you want every answer to start from all of its memory. *Setup:* none.
- **C11b** — The program does all memory work and the agent gets no memory tools. Summaries happen only at the 80% threshold, and the summary text itself goes into the context, not just its id. *Pick this when* your model's tool calling is unreliable, e.g. a small local model. *Setup:* none. *Cost:* the agent cannot open a summary to recover details, and the summary text costs tokens on every turn.
  - *What to check:* the model's tool list never contains a memory tool, and after a threshold summary the Summary section shows the summary text.
- **C11c** — The agent fetches long-term memory itself. The program loads only the conversation section and the list of summaries. The agent gets search tools for the knowledge base, workflow memory and entity memory, and decides when to call them. *Pick this when* your stores are large, most questions need none of them, and your model calls tools well. *Setup:* none. *Cost:* the course warns that the agent cannot look up what it does not know exists, and every lookup is an extra model call.
  - *What to check:* for a question whose answer is only in the knowledge base, the agent calls the knowledge-base search before its final answer, and the passage reaches the model.

### C12. How should old conversation be shrunk? — *Ask only when C6 is C6a or C6b and C11 is C11a.*
- **C12a (Recommended - course default)** — Summarize, keep the originals, and open them on demand. The summary and a short label are stored, the old messages are marked as summarized, and the context shows only the summary's id and label. The agent can open the summary to get the original messages back. *Pick this when* later questions may need exact earlier wording, as in the course's "what was my first question?" demo. *Setup:* none.
- **C12b** — Summarize and show the summary text. The Summary section shows the summary text itself. The originals stay in the database, but the agent has no tool to open them. *Pick this when* the gist is enough and you would rather not spend a tool call on each lookup. *Setup:* none. *Cost:* summarizing is lossy; in the course's words, "we will always lose a little bit of information". Exact earlier wording is out of the agent's reach.
  - *What to check:* after a summary is made, the next context's Summary section contains the summary text, and no tool for opening summaries is offered.

### C13. Keep a log of every tool call?
- **C13a (Recommended - course default)** — Yes. The full arguments, result, status and any error of each call are stored in the tool log. A long result is cut short for the model, with a pointer to its log row. *Pick this when* you want to review what tools did, or keep long outputs without filling the context. *Setup:* none.
- **C13b** — No log. A long result is still cut to 3000 characters for the model, and the rest is dropped. *Pick this when* nothing will ever review past runs and tool outputs are large, such as full documents, so a log would double the storage. *Setup:* none. *Cost:* cut-off output cannot be recovered, and failed calls cannot be reviewed afterwards.
  - *What to check:* no tool log table exists, and a tool result over 3000 characters reaches the model cut to 3000 characters, followed by a note that the rest was dropped.

## 2. Departures from the course

| # | Where the recommended build differs | Why |
|---|---|---|
| D1 | Memory lives in one SQLite file, and similarity search is a full scan computing cosine similarity in the program. The course used Oracle AI Database 26ai through LangChain's Oracle vector store, with IVF vector indexes. | The course's database needs container and admin setup. The stand-in keeps every store and behaviour at sample scale (guide rule 4.4). Oracle stays available as C4b. |
| D2 | On start, the program creates missing stores and never drops existing ones. | The course's notebooks drop and recreate every memory table at the start of each lesson to get a clean slate. An app that did that would forget everything between sessions, which breaks what-must-stay-true item 1. |
| D3 | Rewritten tool descriptions (and their example requests) are what gets embedded for tool search. | The instructor says the enriched text "is what gets embedded and stored". The course's code computes that vector but searches over the original docstring text instead (see note B-4). |
| D4 | The summarizer receives the whole unsummarized transcript, and the stored summary is cut to its first 6000 characters. | The instructor says the summary keeps "a maximum of 6000 characters in our final response". The code instead cuts the *input* at 6000 characters, so later messages get marked as summarized without being summarized (note B-4). |
| D5 | Similarity is cosine. | The instructor names cosine when introducing the stores (Lesson 3). The Lesson 5–6 notebooks use Euclidean distance (guide rule 4.2, first test: the instructor's stated value). |
| D6 | A tool's search text uses its parameter names, not a Python signature string, and the workflow step text shows arguments as JSON, not Python dict text. | Keeps the build independent of one language's printing. |
| D7 | The sample data is your own fictional paper records and a stand-in arXiv catalog for the offline tests. The course downloaded 100 records from a Hugging Face dataset. | No course data is copied (guide rule 4.5), and the tests must run offline (section 7). |
| D8 | A command-line program (C3a) replaces notebook cells that call the agent function. | The build is never a notebook (guide rule 3.4). The command line is an addition. |
| D9 | The embedding model is loaded directly with sentence-transformers. The course loaded the same model through LangChain's Hugging Face wrapper. | Same model, same vectors, fewer packages. |
| D10 | Web search (Tavily) and the agent-callable toolbox search are not in the recommended build. | The course built both in Lesson 4, but its final app (Lesson 6) registers neither (guide rule 4.1: the final version decides). Both are offered as C9b and C7c. |
| D11 | Entity extraction runs automatically on every question and every final answer. | The final app's code and the Lesson 6 transcript do this. A Lesson 3 notebook table lists entity writing as agent-triggered (guide rule 4.2, second test: the final app). |
| D12 | Current models and current library releases. | The course used `gpt-5-mini` and `gpt-5` and listed its packages without versions. The build agent picks current models at the checklist (guide rules 4.6, 4.7). |
| D13 | The offline tests use a scripted stand-in model, the word-hash embedder and a stand-in arXiv catalog. | They let the tests run with no key and no network (guide rule 7.3). Each one is labelled as a stand-in. |

---

## 3. Objective

On every turn, load the memory relevant to the user's request from a persistent store into the model's context. Let a tool-using model answer. Save the new conversation, steps and facts back to the store, so that the next turn or session carries on.

## 4. Tech stack, versions, secrets

- **Language:** Python (the course's language), current release. Use current releases of every package; the course listed its packages without versions.
- **Recommended packages:** `openai` (model calls), `sentence-transformers` (C5a embedder), `arxiv` plus a PDF-to-text library (the course's loaders used `arxiv` and `pymupdf`), `langchain-text-splitters` (the course's chunker), `python-dotenv` (loads `.env`), `pytest` (tests). The standard library's `sqlite3` is the store (C4a).
- **Package name:** `memory_agent`. Runs as `python -m memory_agent …`.
- **Secrets:** `OPENAI_API_KEY` comes from the environment or a `.env` file that is never committed. If no key is set, the command-line chat stops with the message "Set OPENAI_API_KEY to chat (offline tests do not need it)." and makes no model call (addition).
- **Paths:** the database file is `data/memory.db` by default, overridable with `MEMORY_AGENT_DB`.

## 5. Contracts

### 5.1 Commands (C3a)
- `python -m memory_agent seed <file.json>` loads paper records into the knowledge base (format in 7.1, `papers.json`). For each record with any non-empty title, subjects or abstract, it stores the text `title\nsubjects\nabstract` (empty parts skipped) with metadata `{arxiv_id, title, subjects, abstract, submission_date}`. Records whose title, subjects and abstract are all empty are skipped. Only the first 100 records of the file are read per run (setting); skipped records count toward the 100, as in the course.
- `python -m memory_agent chat --thread <id>` is an interactive loop: each line is one turn. Before each answer it prints `Context: <percent>% (<tokens>/<max> tokens) <status>`.
- `python -m memory_agent ask --thread <id> "<question>"` runs one turn, prints the answer and exits.
- The default thread id is `"1"` (course default). Thread ids are stored as text.

### 5.2 Stores (course table names are binding)

The SQL-style stores are:

```json
{
  "CONVERSATIONAL_MEMORY": {
    "id": "string, generated, primary key",
    "thread_id": "string, required",
    "role": "string, required, 'user' | 'assistant'",
    "content": "string, required",
    "timestamp": "datetime with microseconds, set on insert",
    "metadata": "JSON text, default '{}'",
    "created_at": "datetime, set on insert",
    "summary_id": "string or null; null = unsummarized"
  },
  "TOOL_LOG_MEMORY": {
    "id": "string, generated, primary key",
    "thread_id": "string, required",
    "tool_call_id": "string or null",
    "tool_name": "string, required",
    "tool_args": "JSON text",
    "result": "full result text",
    "result_preview": "first 2000 bytes of result (UTF-8, cut cleanly)",
    "status": "'success' | 'failed', default 'success'",
    "error_message": "string or null",
    "metadata": "JSON text, e.g. {\"iteration\": 1}",
    "timestamp": "datetime with microseconds",
    "created_at": "datetime"
  }
}
```

Lookups are indexed by `thread_id` and `timestamp`, and the tool log is also indexed by `tool_name`. Rows with equal timestamps keep insertion order.

The vector stores are `SEMANTIC_MEMORY` (knowledge base), `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY` and `SUMMARY_MEMORY`. Every row is `{id, text, metadata (JSON object), embedding (list of numbers)}`. The `text` is what gets embedded, except in the toolbox, where the embedding comes from the search text in R12. A search returns the top k rows by cosine similarity between the query's embedding and each row's embedding, highest first. Ties go to the earlier-inserted row. An optional metadata filter supports equality and `{"$gt": n}`.

| Store | `text` | `metadata` |
|---|---|---|
| SEMANTIC_MEMORY (seed) | `title\nsubjects\nabstract` | `{arxiv_id, title, subjects, abstract, submission_date}` |
| SEMANTIC_MEMORY (saved paper chunk) | chunk text | `{source:"arxiv", arxiv_id, title, entry_id, published, authors, chunk_id, num_chunks, ingested_ts_utc}` |
| WORKFLOW_MEMORY | `Query: <q>\nSteps:\nStep 1: <step>\n…\nAnswer: <first 200 chars of answer>` | `{query, success: true, num_steps, timestamp}` |
| TOOLBOX_MEMORY | `<name> <own description> <parameter names>` | `{name, description (shown to the model), parameters: {pname: {type, default?}}, return_type, augmented: bool, queries?: [...]}` |
| ENTITY_MEMORY | `<name> (<TYPE>): <description>` | `{name, type, description}` |
| SUMMARY_MEMORY | `<summary_id>: <label>` | `{id, full_content, summary, description (= label), thread_id}` |

### 5.3 Tool schema offered to the model

```json
{"type": "function",
 "function": {"name": "<tool name>", "description": "<metadata.description>",
   "parameters": {"type": "object",
     "properties": {"<param>": {"type": "string|integer|number|boolean"}},
     "required": ["<every param with no default>"]}}}
```

Parameter types map str→string, int→integer, float→number, bool→boolean, and anything else→string. A tool name appears at most once per list.

### 5.4 Tools in the recommended build (names are binding; the model sees them)

| Tool | Parameters | Own description (embedded) | Rewritten? (C8a) | Behaviour |
|---|---|---|---|---|
| `arxiv_search_candidates` | `query` (string), `k` (int, default 5) | "Search arXiv for papers matching a query and return a JSON list of candidate papers with ids, titles, authors, dates and abstracts." | no | It fetches up to 8 matches, each with up to 4000 characters of content, and returns a JSON list of the first `k` as `{arxiv_id, entry_id, title, authors, published, abstract (first 2500 chars)}`. `arxiv_id` is the part of `entry_id` after `/abs/`, e.g. `http://arxiv.org/abs/2501.00011v2` → `2501.00011v2`. |
| `fetch_and_save_paper_to_kb_db` | `arxiv_id` (string), `chunk_size` (int, 1500), `chunk_overlap` (int, 200) | "Fetch the full text of an arXiv paper and store it in the knowledge base as chunks." | yes | It loads the paper's full text. If no paper is found it returns `No documents found for arXiv id: <id>`. If the text is empty it returns `Loaded arXiv <id> but extracted empty text (PDF parsing issue).` Otherwise it splits the text into chunks of at most `chunk_size` characters with up to `chunk_overlap` overlap, preferring paragraph, then line, then word boundaries. It stores all chunks in SEMANTIC_MEMORY with chunk metadata and returns `Saved arXiv <id> to SEMANTIC_MEMORY: <n> chunks (title: <title>).` |
| `get_current_time` | `detailed` (bool, false) | "Return the current date and time as text." | no | Returns the local time as `YYYY-MM-DD HH:MM:SS`, or with microseconds (`.ffffff`) when detailed. |
| `expand_summary` | `summary_id` (string), `thread_id` (string, default null) | "Expand a summary reference to retrieve the original conversation messages." | yes | See R11. |
| `summarize_and_store` | `text` (string, default ""), `thread_id` (string, default null) | "Summarize content and store it in summary memory." | yes | With a `thread_id`, it summarizes that thread (R9) and returns `Stored as [Summary ID: <id>] <label>`, or `No unsummarized messages found for thread <id>.` With only `text`, it summarizes that text into the same store. With neither, it returns ``Provide `thread_id` (preferred) or non-empty `text` to summarize.`` |

### 5.5 Model roles

| Role | Used for | Course model |
|---|---|---|
| `agent` | The tool-calling loop (tool choice "auto") | `gpt-5-mini` |
| `summarizer` | Summary, retry summary, and the 8–12 word label | `gpt-5` |
| `entity_extractor` | Entity JSON from text | `gpt-5` |
| `tool_describer` | Rewritten tool descriptions and 5 example requests (C8a) | `gpt-5` |

The program reaches the model through one replaceable connection, so tests can substitute the scripted stand-in (7.1). The course's calls set `max_completion_tokens` (4000 for summaries, 2000 for labels, entities and rewritten descriptions) and never set a temperature.

### 5.6 Settings

| Setting | Value | Source | Change this when … |
|---|---|---|---|
| Conversation window | 10 unsummarized messages | course helper `read_conversational_memory` | your threads run long before a summary is made |
| Which 10 | the **oldest** 10 unsummarized, shown oldest first | course helper (query takes the first rows by ascending time; see note B-4) | you want the newest 10: change to "newest 10, shown oldest first" |
| Knowledge-base results | 3 | course helper | answers need more passages |
| Workflow results | 3, only workflows with ≥1 step | course helper | — |
| Entity results | 5 | course helper | — |
| Summary list size | 10, scoped to the thread | course helper | — |
| Tools offered per turn | 5 | Lesson 6 notebook (`k=5`; the method's default is 3) | you have many similar tools |
| Context budget | 256000 tokens; 128000 for an unknown model | Lesson 5 notebook / helper | your chosen model's real window differs |
| Token estimate | characters ÷ 4, rounded down; percent rounded to 1 decimal | Lesson 5 transcript and notebook | — |
| Auto-summary threshold | usage **> 80%** | Lessons 5 and 6 transcripts and notebooks | you want earlier summaries |
| Status words | `ok` < 50%, `warning` < 80%, else `critical` | Lesson 5 notebook | — |
| Loop limit | 10 model calls per turn | Lesson 6 notebook | tasks need more steps |
| Tool result shown to model | first 3000 characters | Lesson 6 notebook | your model's window is small |
| Tool-log preview | 2000 bytes | course helper | — |
| Summary length cap | 6000 characters | Lesson 5 transcript (D4) | — |
| Retry summary limit | ≤ 180 words | course helper | — |
| Label length | 8–12 words | course helper | — |
| Summary id | 8 lowercase hex characters (first 8 of a random UUID) | course helper | — |
| Entity input | first 500 characters of the text; types PERSON, PLACE, SYSTEM; texts under 5 characters skipped | course helper | your domain has other entity kinds |
| Workflow answer excerpt | 200 characters | course helper | — |
| Step argument display | string values over 50 characters cut to 50 + `...` | Lesson 6 notebook | — |
| Example requests per rewritten tool | 5 | course helper | — |
| Paper search | fetch 8, return `k`=5, abstract 2500 characters, content 4000 characters | Lesson 4 notebook, helper | — |
| Paper chunks | 1500 characters, 200 overlap | Lesson 4 notebook, helper | your embedder's input limit differs |
| Seed limit | 100 records per run | Lesson 3 notebook | — |
| Embedder | `sentence-transformers/paraphrase-mpnet-base-v2`, 768 dimensions | Lessons 3–6 | changing it needs a fresh database, because vectors from different embedders cannot be compared |
| Similarity | cosine | Lesson 3 transcript (D5) | — |

## 6. Business rules

### What must stay true (the course's pattern card; every option keeps both)
- **M1. Memory lives outside the model and survives the session.** What the agent learns in one turn or session is stored in persistent storage and is available to later turns and new sessions. Nothing depends on the model or the process remembering it. → T1, T2
- **M2. Before the model answers, the memory relevant to the request reaches its context.** → T4, T23

### Rules of the recommended build
- **R1. Conversation persists by thread.** Each user question is written to CONVERSATIONAL_MEMORY (role `user`) after the context is built and before the first model call. Each final answer is written (role `assistant`) at the end of the turn. A new process opened on the same database file sees them. Messages of other threads never appear. → T1, T2
- **R2. Fresh start.** On first use the program creates all seven stores under the course names. On later starts it keeps every existing row. → T3
- **R3. Context layout.** The model receives two messages: the system prompt (R16), then one user message. The user message is `# Question\n<question>\n\n` followed by, in this order, the Conversation, Knowledge Base, Workflow, Entity and Summary sections. Each section starts with `## <Name> Memory` and has a `### What this memory is` line, a `### How you should leverage it` list and a results part. The question is never summarized or cut. → T4
- **R4. Conversation section.** It holds the oldest 10 unsummarized messages of the thread in time order, each as `[HH:MM:SS] [<role>] <content>`, under `### Retrieved messages`. Summarized messages are excluded. If there are none, it shows `(No unsummarized messages found for this thread.)`. → T5, T13
- **R5. Knowledge Base section.** It holds the top 3 passages for the question, one per line, under `### Retrieved passages`. If there are none, it shows `(No relevant knowledge base passages found.)`. → T6
- **R6. Workflow memory.** After a turn with at least one tool call, one workflow row is written (5.2). Each step reads `<tool name>(<args as JSON, long strings cut>) → success` or `→ failed`. A turn with no tool call writes no workflow. The section shows the top 3 workflows with `num_steps > 0`, separated by `\n---\n`. If there are none, it shows `(No relevant workflows found.)`. → T7
- **R7. Entity memory.** Entities are extracted from the question (after it is written) and from the final answer. The entity extractor sees only the first 500 characters. Each entity it returns is stored, with no de-duplication. The section lists the top 5 as `• <name>: <description>`. If there are none, it shows `(No entities found.)`. Extraction errors are ignored. → T8
- **R8. Context budget.** Usage is computed on the memory sections only (question and system prompt excluded): tokens = characters ÷ 4 against the 256000 budget. If usage is over 80%, the program summarizes the thread (R9). It then replaces the whole Conversation section with `## Conversation Memory\nOlder conversation content was summarized to reduce context size.\nUse Summary Memory references + expand_summary(id) for full detail.` and appends `[Summary ID: <id>] <label>` at the end of the Summary section. Other sections are untouched. Usage is then recomputed, and the status line shows both values. → T9, T10b
- **R9. Summarizing a thread.** The program reads all unsummarized messages of the thread in time order and builds the transcript `[YYYY-MM-DD HH:MM:SS] [ROLE] <content>`, one line per message, with the role in capitals. The summarizer is asked for exactly four headings: `### Technical Information`, `### Emotional Context`, `### Entities & References`, `### Action Items & Decisions`. It keeps concrete details, separates facts from open questions, invents nothing, and stays concise. If the reply is empty, the program retries once with a shorter prompt (≤180 words, same headings). If the retry is also empty, it uses a fixed fallback: the four headings, with the first 500 characters of the transcript (newlines → spaces) under Technical Information and "Not available from model output." under the other three. The stored summary is cut to 6000 characters. Next the summarizer is asked for an 8–12 word label. If the label is empty or one of "conversation summary", "summary", "chat summary" or "thread summary" (any case), the label becomes the first line of the summary that, after removing leading `-`, `•`, `*` and spaces, is not empty, does not start with `###`, and has at least 4 words, cut to 12 words and trimmed of ` ,.;:`. If no such line exists, the label is "Recent thread context, decisions, and open actions". The summary is stored with a new 8-hex id, the full transcript, the label and the thread id. Exactly the messages that were read are marked with that id. If there are no unsummarized messages, nothing is stored and the result is "nothing to summarize". → T10, T11, T12
- **R10. No re-summarizing.** A message already marked with a summary id is never read for, or marked by, another summary. → T13
- **R11. Summary list and opening a summary.** The Summary section lists this thread's summaries (top 10 by similarity to the question) as `  • [ID: <id>] <label>`, under `Use expand_summary(id) to retrieve the detailed underlying conversation.` and `Scope: thread_id = <thread>`. If there are none, it shows `(No summaries available for thread <thread>.)`. `expand_summary(id)` returns `## Summary Context\n<summary text>\n\n## Expanded Conversations for Summary ID: <id>\nTotal messages: <n>\n`, then for each message, in time order, `[YYYY-MM-DD HH:MM:SS] [ROLE]`, its content, and a blank line. An unknown id returns `Summary <id> not found.` and `No conversations found for summary_id: <id>`. → T14
- **R12. Toolbox.** Registering a tool stores one row (5.2). For a tool that is not rewritten, the search text is `<name> <own description> <parameter names>`. For a rewritten tool (C8a), the tool describer is asked for a richer description (a one-line summary, what it does step by step, when an agent should call it, caveats) and for 5 example requests as a JSON list. The search text is then `<name> <rewritten description> <parameter names> <example requests joined by spaces>`, and the rewritten description is what the model sees. If the example-request reply is not a JSON list, the whole reply is used as one example. Registering a name that is already stored writes nothing and calls no model, but the tool can still be run. On each turn, the 5 best-matching tools for the question are offered (5.3). Only these are offered, never every tool. → T15, T16
- **R13. The loop.** The program makes up to 10 model calls per turn. If a reply has tool calls, each one runs by name. An unknown name returns `Error: Tool '<name>' not found` with status success, as in the course. A call that raises returns `Error: <message>` with status `failed`. A `summarize_and_store` call without a `thread_id` gets the current thread id. Each result goes back to the model as a tool message. A reply without tool calls is the final answer. If 10 calls pass without a final answer, the answer is `I was unable to complete the request within the allowed iterations.` → T17, T18, T19
- **R14. Tool log and cut results.** Every tool call is logged in full (5.2), with `{"iteration": n}` as metadata. A result over 3000 characters reaches the model as its first 3000 characters followed by `\n\n[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <id>]`. → T20
- **R15. Tools** behave as in 5.4. → T21, T22, T24, T26
- **R16. System prompt.** It tells the model the following:
  - It is a memory-aware research assistant with tools.
  - The user message is a partitioned context: a `# Question` followed by the five named sections, each a distinct memory store. The prompt states each section's purpose: conversation for continuity and preferences, knowledge base for grounding facts, workflow for planning tools without copying blindly, entity for consistent names, summary for older context, preferring this thread's summaries.
  - When a needed detail exists only in a summary, call `expand_summary` first.
  - Start from the memory sections before using tools.
  - On conflicts, prefer the current question, then the latest conversation, then knowledge-base evidence, then older summaries and workflows.
  - Use only the tools offered this turn, and as few calls as needed.
  - If memory is insufficient, say what is missing, then use a tool.
  - To compact the conversation, use `summarize_and_store` with the thread id.

  → T4
- **R17. End of turn order.** First the workflow is written (if there were steps), then entities from the final answer, then the final answer as an assistant message. → T23
- **R18. Seeding the knowledge base** follows 5.1: text `title\nsubjects\nabstract`, empty parts left out, all-empty records skipped, only the first 100 records of the file read per run. → T6, T25

## 7. Tests

### 7.1 Sample data (all facts invented for this spec)

**`sample_data/papers.json`** is a list of 5 records with fields `{arxiv_id, title, subjects, abstract, submission_date}`:
1. `2501.00011`, "Tidepool: Paged Context for Long-Running Agents", "Artificial Intelligence (cs.AI)", "Tidepool keeps an agent's older conversation pages in an external store and pages them back into the prompt only when a task needs them.", `2025-01-03`
2. `2501.00022`, "Lantern: Finding the Right Tool Among Hundreds", "Computation and Language (cs.CL)", "Lantern embeds tool descriptions and retrieves the few tools that match each request instead of listing every tool.", `2025-01-09`
3. `2501.00033`, "Coral Reef Soundscapes at Night", "Populations and Evolution (q-bio.PE)", "Hydrophone recordings show reef fish choruses peak two hours after sunset.", `2025-01-15`
4. `2501.00044`, "Basalt: Replaying Workflows for Web Agents", "Artificial Intelligence (cs.AI)", "Basalt records the ordered steps a web agent took and replays them for similar requests.", `2025-01-21`
5. `2501.00055`, "", "", "", `2025-01-30` (empty record; must be skipped)

**`sample_data/arxiv_catalog.json`** is the *stand-in for the arXiv service* in offline tests. It is a list of `{entry_id, title, authors, published, abstract, full_text}`, in this order:
1. `http://arxiv.org/abs/2501.00011v2`, Tidepool title as above, "Ana Ruiz, Ben Osei", `2025-01-03`, Tidepool abstract as above. Its full_text is four paragraphs joined by a blank line (`\n\n`). Paragraph k (k = 1..4) is `Tidepool paragraph k.` followed by a space and then the sentence `Pages move between the prompt and the store.` 20 times, separated by single spaces. Each paragraph is 921 characters; the full text is 3690.
2. `http://arxiv.org/abs/2501.00022v1`, Lantern title, "Chen Wu", `2025-01-09`, Lantern abstract; full_text "Lantern embeds each tool description once and searches them per request."
3. `http://arxiv.org/abs/2501.00044v3`, Basalt title, "Dara Kim", `2025-01-21`, Basalt abstract; full_text "" (empty: the planted empty-text case).
4. `http://arxiv.org/abs/2502.00101v1`, "Longform Survey of Agent Memory I", "Eli Stone", `2025-02-02`, abstract = the word `memory` 400 times separated by single spaces (2799 characters); full_text = the abstract.
5. `http://arxiv.org/abs/2502.00102v1`, "Longform Survey of Agent Memory II", "Eli Stone", `2025-02-03`, abstract and full_text as in 4.
6. `http://arxiv.org/abs/2502.00201v1`, "Quartz: Scheduling Tool Calls for Agents", "Fay Lund", `2025-02-10`, "Quartz orders tool calls so agents finish multi-step tasks sooner."; full_text = abstract.
7. `http://arxiv.org/abs/2502.00202v1`, "Mica: Token Budgets for Agents", "Gus Hale", `2025-02-11`, "Mica splits a token budget between instructions, retrieved passages and tool results."; full_text = abstract.
8. `http://arxiv.org/abs/2502.00203v1`, "Shale: Testing Agents Offline", "Hana Ito", `2025-02-12`, "Shale replays recorded model replies so agent tests run without a network."; full_text = abstract.
9. `http://arxiv.org/abs/2502.00204v1`, "Flint: Safer Shell Use for Agents", "Ivo Berg", `2025-02-13`, "Flint limits which shell commands agents may run."; full_text = abstract.

The stand-in's search splits the query and each entry's title + abstract into lowercase `[a-z0-9]+` words. An entry matches if it shares at least one word with the query. It returns up to 8 matching entries in catalog order. Its fetch matches an id against `entry_id` after `/abs/`, ignoring any trailing `v<digits>` on both sides.

**`sample_data/previous_session.json`** is the planted "stateless agent" failure: the messages of an earlier session on thread `"50000"`, to be written by one process and read by another:
`[{"role":"user","content":"Can you find the paper on Tidepool?"}, {"role":"assistant","content":"Found Tidepool: Paged Context for Long-Running Agents (arXiv 2501.00011v2)."}]`

**Word-hash embedder.** It is a *stand-in for the embedding model*, used by every offline test and by C5b. The text is lowercased and split into `[a-z0-9]+` words. Each word adds 1 at position `int(sha256(word), 16) mod 512` of a 512-number vector, which is then scaled to length 1. An empty text gives an all-zero vector, whose similarity to anything is 0.

**Scripted model.** It is a *stand-in for every model role* and is chosen by the tests. For the agent role, the question is the text between `# Question\n` and the first blank line of the user message. "Tool result present" means the conversation for this turn already holds a tool message.

| Agent question | No tool result yet | Tool result present |
|---|---|---|
| `Can you find the paper on Tidepool?` | call `arxiv_search_candidates` `{"query":"Tidepool"}` | final `Found Tidepool: Paged Context for Long-Running Agents (arXiv 2501.00011v2).` |
| `Please save the content of that paper.` | call `fetch_and_save_paper_to_kb_db` `{"arxiv_id":"2501.00011v2"}` | final `Saved Tidepool to the knowledge base.` |
| `What are the key takeaways from the paper?` | final `Tidepool keeps older context in an external store and pages it back in only when needed.` | — |
| `Summarize the conversation so far using your tool.` | call `summarize_and_store` `{}` | final `I stored a summary of our conversation.` |
| `What was my first question?` | if the user message contains `[ID: ` + 8 hex + `]`, call `expand_summary` `{"summary_id": <those 8 hex>}`; otherwise final `I don't know.` | final `Your first question was: ` + the content line right after the first `[USER]` header in the tool result |
| `Find surveys about memory.` | call `arxiv_search_candidates` `{"query":"memory survey"}` | final `Found two surveys.` |
| `Keep checking the time.` | call `get_current_time` `{}` | call `get_current_time` `{}` (never ends) |
| `Try a broken call.` | call `arxiv_search_candidates` `{"q":"x"}` | final `That call failed.` |
| `Call a missing tool.` | call `no_such_tool` `{}` | final `That tool does not exist.` |
| anything else | final `OK.` | final `OK.` |

The other roles reply as follows:
- **Summarizer, summary prompt:** an empty reply if the transcript contains `EMPTY-SUMMARY-PROBE`. If the transcript contains `LONG-SUMMARY-PROBE`, the reply is `### Technical Information\n` followed by 7000 letters `A`. Otherwise the reply is `### Technical Information\nThe user searched for the Tidepool paper and saved it.\n\n### Emotional Context\nNeutral.\n\n### Entities & References\nTidepool (arXiv 2501.00011v2).\n\n### Action Items & Decisions\nNone.`
- **Summarizer, label prompt:** `Summary` if the summary contains `Not available from model output`. Otherwise `Tidepool paper search, save, and takeaways for paged agent context`.
- **Entity extractor:** `[{"name":"Tidepool","type":"SYSTEM","description":"paged context method for agents"}]` if the text it receives contains `Tidepool`, otherwise `[]`.
- **Tool describer:** the rewritten descriptions, chosen by the tool name in the prompt:
  - fetch_and_save_paper_to_kb_db → "Download the full text of one paper by its arXiv id, split it into overlapping chunks and save every chunk into the knowledge base so later questions about that paper can be answered from memory."
  - expand_summary → "Turn a summary id from Summary Memory back into the original conversation messages, in time order with timestamps, when exact earlier wording or details are needed."
  - summarize_and_store → "Summarize the unsummarized messages of the current thread with the model, store the summary in summary memory and mark those messages as summarized to shrink the context."
- **Tool describer, example-request prompt:** a JSON list, chosen by how the description starts:
  - "Download…" → `["save this paper","store the full paper text","download the paper by its id","add the paper to my knowledge base","keep this paper for later"]`
  - "Turn a summary…" → `["what did I ask earlier","show the original messages","expand that summary","what exactly did we say before","recover the earlier conversation"]`
  - "Summarize the…" → `["summarize our conversation","compress the chat so far","store a summary of this thread","shrink the context","save a summary of what we discussed"]`

**Standard setup ("the five tools")** is a fresh database file, the word-hash embedder, the scripted model, the stand-in catalog, `papers.json` seeded, and the five tools of 5.4 registered with their rewrite flags.

### 7.2 Test table

| Test | Given | When | Then |
|---|---|---|---|
| **T1** (R1, M1) | The five tools | You ask `Can you find the paper on Tidepool?` on thread `50000` | CONVERSATIONAL_MEMORY has 2 rows for `50000`: user with that question, then assistant with `Found Tidepool: Paged Context for Long-Running Agents (arXiv 2501.00011v2).`. Both have `summary_id` null. Thread `60000` has 0 rows. |
| **T2** (R1, M1; planted failure F1) | Process A writes `previous_session.json` to thread `50000` in a database file and exits | Process B opens the same file and runs `Please save the content of that paper.` on `50000`; separately, `OK test` on thread `60000` | B's first agent call has a Conversation section containing `[user] Can you find the paper on Tidepool?` and `[assistant] Found Tidepool: Paged Context for Long-Running Agents (arXiv 2501.00011v2).`. Thread `60000`'s Conversation section shows `(No unsummarized messages found for this thread.)`. |
| **T3** (R2) | No database file | The program starts; you write one message; the program starts again | All seven stores exist under the course names after the first start. The message is still there after the second start. |
| **T4** (R3, R16, M2) | T1 done | You ask `Please save the content of that paper.` on `50000` | The first model call has 2 messages. The system message contains `# Question`, the five section names and `expand_summary`. The user message starts with `# Question\nPlease save the content of that paper.\n\n## Conversation Memory`. The headings `## Knowledge Base Memory`, `## Workflow Memory`, `## Entity Memory`, `## Summary Memory` follow in that order. The Conversation section has the T1 question and answer but not the current question. |
| **T5** (R4) | Thread `80000` has 12 user messages `m01` … `m12`, written in order | Build its Conversation section | It contains `m01` … `m10` in that order and not `m11` or `m12` (course behaviour: oldest 10). |
| **T6** (R5, R18) | The five tools (seed done) | Build the Knowledge Base section for `paged context for long running agents` | Exactly 3 passages. The first starts with `Tidepool: Paged Context for Long-Running Agents`, the next two are Basalt then Lantern, and no Coral passage appears. SEMANTIC_MEMORY has 4 rows: the empty record was skipped. |
| **T7** (R6) | Fresh database | Write 4 workflows with 1 step each and 1 workflow with 0 steps; build the Workflow section for `Find the paper`. Separately, run T1's question with the five tools on a fresh database, and write one workflow whose single step is a call with a 60-character string argument. | The section shows exactly 3 workflows, none with `num_steps` 0. After T1's question, WORKFLOW_MEMORY has 1 row with text `Query: Can you find the paper on Tidepool?\nSteps:\nStep 1: arxiv_search_candidates({"query": "Tidepool"}) → success\nAnswer: Found Tidepool: …` and metadata `num_steps` 1, `success` true. A step whose argument is a 60-character string shows its first 50 characters plus `...`. The text after `Answer: ` is at most 200 characters. |
| **T8** (R7) | The five tools | (a) Run T1's question. (b) Ask a 600-character question whose only `Tidepool` is at characters 551–558. (c) Write 6 entities directly and build the Entity section for `Tidepool`. | (a) ENTITY_MEMORY has exactly 2 rows `Tidepool (SYSTEM): paged context method for agents`, one from the question and one from the answer. (b) No entity is added from the question. (c) The section lists exactly 5 lines starting `• `. |
| **T9** (R8; warned failure F3) | Thread `70000` has 10 messages, each the letter `x` 90000 times, alternating user/assistant | You ask `Continue.` on `70000` | The first usage printed is over 80%. Before the model is called, all 10 rows are marked with one 8-hex summary id. The user message sent to the model contains `Older conversation content was summarized to reduce context size.` and `[Summary ID: <id>] Tidepool paper search, save, and takeaways for paged agent context`, and no run of 100 `x`s. The recomputed usage is under 1%. A thread with 2 short messages and the same question creates no summary. |
| **T10** (R9) | The five tools; T1 and T4 done on `50000` | Call `summarize_and_store` with `{"thread_id":"50000"}` | It returns `Stored as [Summary ID: <id>] Tidepool paper search, save, and takeaways for paged agent context`, with `<id>` matching `^[0-9a-f]{8}$`. SUMMARY_MEMORY has 1 row with that id, the scripted summary, thread `50000`, and a `full_content` whose lines start with `[YYYY-MM-DD HH:MM:SS] [USER]` or `[ASSISTANT]`. All 4 messages carry the id. |
| **T10b** (R8, status words) | — | Compute status for contexts of 400000, 512000 and 819200 characters; then for 512000 characters with a model name not in the budget table | `ok` (39.1%), `warning` (50.0%), `critical` (80.0%); then max 128000 and `critical` (100.0%). |
| **T11** (R9, cap) | Thread `91000` has one message `LONG-SUMMARY-PROBE` | Summarize the thread | The stored summary is exactly 6000 characters and starts with `### Technical Information\nA`. |
| **T12** (R9; warned failure F6) | Thread `90000` has one user message `EMPTY-SUMMARY-PROBE alpha beta gamma delta` | Summarize the thread | The summarizer was called twice for the summary. The stored summary has the four headings, with the transcript line under Technical Information and `Not available from model output.` under the other three. The label ends with `[USER] EMPTY-SUMMARY-PROBE alpha beta gamma delta`. |
| **T13** (R10, R4; warned failure F4) | T10 done | Summarize `50000` again; then build its Conversation section | It returns `No unsummarized messages found for thread 50000.`, and SUMMARY_MEMORY still has 1 row. The section shows `(No unsummarized messages found for this thread.)`. |
| **T14** (R11) | T10 done | Call `expand_summary` with `{"summary_id":"<id>"}`; call it with `"ffffffff"`; build the Summary section for thread `50000`, then for `60000`; write 11 summaries to thread `95000` and build its section | The first call returns text starting `## Summary Context\n` with the scripted summary, then `## Expanded Conversations for Summary ID: <id>`, `Total messages: 4`, and the 4 messages oldest first. The unknown id returns `Summary ffffffff not found.` and `No conversations found for summary_id: ffffffff`. The `50000` section has `  • [ID: <id>] Tidepool paper search, save, and takeaways for paged agent context`. The `60000` section shows `(No summaries available for thread 60000.)`. The `95000` section lists exactly 10 `[ID:` lines. |
| **T15** (R12; warned failure F2) | The five tools | Search the toolbox with k=1 for `what time is it now`, for `download the paper and keep it in my knowledge base`, and for `what did I ask earlier in this conversation`; register a sixth, test-only tool `echo_text(text)` described as "Echo the given text back." and run any turn | The searches return `get_current_time`, `fetch_and_save_paper_to_kb_db` and `expand_summary`. The turn's model call is offered exactly 5 tools. The schema for `fetch_and_save_paper_to_kb_db` has `arxiv_id` string, `chunk_size` integer, `chunk_overlap` integer and `required` `["arxiv_id"]`. |
| **T16** (R12) | The five tools | Register the same five tools again in a new process | TOOLBOX_MEMORY still has 5 rows, and the tool describer was not called. The three rewritten tools have `augmented` true and 5 `queries`; the other two have `augmented` false. |
| **T17** (R13) | The five tools | Ask `Try a broken call.`; then `Call a missing tool.` | The first logs status `failed` with a non-empty `error_message`, the model receives a tool message starting `Error: `, and the workflow step ends `→ failed`. The second sends the model `Error: Tool 'no_such_tool' not found`, and its log status is `success`. |
| **T18** (R13; warned failure F8) | The five tools | Ask `Keep checking the time.` | Exactly 10 model calls are made, and the stored assistant answer is `I was unable to complete the request within the allowed iterations.` |
| **T19** (R13) | T1 done | Ask `Summarize the conversation so far using your tool.` on `50000` | `summarize_and_store` ran with thread id `50000` injected, and 3 messages were marked: T1's 2 plus this question. |
| **T20** (R14; warned failure F7) | The five tools | Ask `Find surveys about memory.` | TOOL_LOG_MEMORY has 1 row whose `result` is a JSON list of 2 candidates (Longform I and II), each abstract 2500 characters, total over 3000 characters. Its `result_preview` is at most 2000 bytes and its metadata is `{"iteration": 1}`. The tool message to the model is the first 3000 characters of `result` plus `\n\n[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <that row's id>]`. |
| **T21** (R15) | Stand-in catalog | Call `arxiv_search_candidates` with `{"query":"agents"}` and with `{"query":"Tidepool"}` | The first returns exactly 5 candidates, Tidepool, Basalt, Quartz, Mica and Shale, without Flint. The second returns 1 candidate with `arxiv_id` `2501.00011v2`, authors "Ana Ruiz, Ben Osei", published `2025-01-03`. |
| **T22** (R15; failure F9) | The five tools | Call `fetch_and_save_paper_to_kb_db` with `2501.00011v2`, then `2501.00044v3`, then `9999.99999` | First: at least 3 chunks, each at most 1500 characters. Each of `Tidepool paragraph 1.` … `Tidepool paragraph 4.` appears in some chunk, chunk metadata has `chunk_id` 0..n−1, `num_chunks` n, `source` `arxiv`, and it returns `Saved arXiv 2501.00011v2 to SEMANTIC_MEMORY: <n> chunks (title: Tidepool: Paged Context for Long-Running Agents).` Second returns `Loaded arXiv 2501.00044v3 but extracted empty text (PDF parsing issue).` Third returns `No documents found for arXiv id: 9999.99999`. Neither the second nor the third adds a row. |
| **T23** (R17, M2, end to end) | The five tools, fresh thread `50000` | Ask in order: `Can you find the paper on Tidepool?`, `Please save the content of that paper.`, `What are the key takeaways from the paper?`, `Summarize the conversation so far using your tool.`, `What was my first question?` | Turn 2's context has Turn 1 in its Conversation section and `arxiv_search_candidates` in its Workflow section. Turn 3 makes 1 model call and adds no workflow (WORKFLOW_MEMORY has 2 rows after turn 3). Turn 4 marks 7 messages. In Turn 5's first context, the Conversation section holds only `I stored a summary of our conversation.`, and the Summary section holds the `[ID: …]` line. Turn 5 calls `expand_summary`, and the final answer is `Your first question was: Can you find the paper on Tidepool?`. In every turn, the assistant message is the last row written. |
| **T24** (R15) | — | Call `get_current_time` with no arguments and with `{"detailed": true}` | The results match `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$` and `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}$`. |
| **T25** (R18) | Fresh database; a file of 105 records, each with title `Paper <n>` and the other fields empty | Seed it | SEMANTIC_MEMORY has exactly 100 rows, `Paper 1` … `Paper 100`, each with text `Paper <n>`. |
| **T26** (R15) | The five tools | Call `summarize_and_store` directly with `{"text":"Tidepool notes"}`; then with `{}` | The first returns `Stored as [Summary ID: <8 hex>] Tidepool paper search, save, and takeaways for paged agent context`, and its SUMMARY_MEMORY row has no `thread_id`. The second returns ``Provide `thread_id` (preferred) or non-empty `text` to summarize.`` and stores nothing. |
| **L1** `live` (M1, M2) | Real model, C5a embedder, fresh database | Ask `Can you find the paper on MemGPT?`, then, in a new process, `What did I just ask you?` on the same thread | The first turn calls `arxiv_search_candidates`. The second answer mentions MemGPT. |
| **L2** `live` (R15) | Network | Real `arxiv_search_candidates` for `memory agents` | It returns 1–5 candidates, each with a non-empty `arxiv_id` and title. |
| **L3** `live` (5.6) | The C5a model downloaded | Embed two texts | Vectors have 768 numbers, and the Tidepool query from T6 still ranks the Tidepool passage first. |

Rules → tests: R1→T1,T2 · R2→T3 · R3→T4 · R4→T5,T13 · R5→T6 · R6→T7 · R7→T8 · R8→T9,T10b · R9→T10,T11,T12 · R10→T13 · R11→T14 · R12→T15,T16 · R13→T17,T18,T19 · R14→T20 · R15→T21,T22,T24,T26 · R16→T4 · R17→T23 · R18→T6,T25 · M1→T1,T2 · M2→T4,T23.

---

## 8. Standing permissions

- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in in code comments and output; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has data; anything that sends data to a third party beyond the chosen model provider and arXiv.
- **Never:** invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets.

## 9. Test plan

1. Install: `python -m pip install -e .[dev]` (or the equivalent for your packaging).
2. Offline: `python -m pytest -m "not live"`. This must pass with no key and no network.
3. Live: `OPENAI_API_KEY=… python -m pytest -m live`. These are skipped automatically when the key is missing.
4. For each chosen option that is not recommended, turn its "what to check" sentence into a test, run it, and report it.
5. Report one result per test, with evidence: test output and file paths. "Should pass" counts as not run.
6. The build is finished when the recommended tests, adjusted for the chosen options, pass, and each chosen option's check passes.
7. Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

---

## 10. Background notes (for the build agent)

### B-1. The program
A tool-using agent whose memory lives outside the model, so it carries on across turns and sessions. Stages, in order:

`store → register tools → assemble context → shrink if over budget → select tools → run the loop → persist`

- **store:** seven stores in one database (conversation, tool log, knowledge base, workflow, toolbox, entity, summary). Memory must outlive the process (M1).
- **register tools:** tool descriptions become searchable memory, so that only the relevant tools are offered.
- **assemble context:** load conversation, knowledge, workflows, entities and summary references into labelled sections before the model answers (M2).
- **shrink:** keep the context under budget by summarizing older conversation while keeping a way back to it.
- **select tools:** offer the 5 best-matching tools.
- **run the loop:** reason, call tools, observe results, up to 10 calls, with raw outputs offloaded to the tool log.
- **persist:** save the conversation, the steps taken and the entities, so the next turn and session can use them.

The course's own instance is a research assistant over arXiv papers (C1a); the stages do not depend on it.

### B-2. Failures
- **F1. The stateless agent forgets** (demonstrated in Lesson 2's turn-by-turn example). The user asks for restaurant recommendations, then asks to book "the first one", and an agent without memory replies that it has no recollection. It happens because nothing outside the model keeps earlier turns. The spec prevents it with R1, the planted `previous_session.json`, and test T2.
- **F2. Too many tools in the prompt** (warned, Lesson 4). It causes context confusion, context bloat, degraded tool selection, more tokens and latency. Prevented by R12 (top 5 per turn); T15. C7b keeps the risk, as its stated cost.
- **F3. Context overflow** (warned, Lesson 5: "Context overflow crashes the agent"). Prevented by R8 (summarize above 80%); T9.
- **F4. Re-summarizing already summarized messages** (warned, Lesson 5). Prevented by R10 (mark exact rows); T13.
- **F5. Summaries lose detail** (a stated cost, not a failure: "we will always lose a little bit of information"). The course keeps originals and opens them on demand (R11, T14, T23). C12b carries the cost.
- **F6. The model returns an empty summary** (handled in course code "so downstream flow never breaks"). Handled by R9 (retry, then fallback); T12.
- **F7. Tool output floods the context** (warned, Lesson 6 "control tool-output bloat"). Prevented by R14; T20.
- **F8. The loop never reaches an answer** (Lesson 6 stop condition). Prevented by R13 (10 calls, fixed message); T18.
- **F9. The paper's PDF yields no text** (course code's message). Handled by R15; T22.
- **Oracle starting up** (course notebooks): "Admin connection failed" right after the database starts means it is not ready yet. Wait and retry. This applies only to C4b.

### B-3. Why the questions and settings are what they are
- **C4/C5 stand-ins:** Oracle needs container and admin setup, so it gets a stand-in (guide rule 4.4). The embedding model is a modest download, so the course's model stays recommended and the stand-in is offered (guide rule 4.4).
- **C6:** the course builds a conversation-only agent first, then says "we need to go beyond this" and "agents need structured, queryable knowledge, not just chat logs". Those are stated limits, not a failure shown, so C6c is offered with that cost (guide rule 5.3).
- **C7:** the course's Lesson 4 is entirely about toolbox retrieval; its warnings are about scale, so C7b is offered for small tool sets with that cost.
- **C8:** the course's Lesson 4 transcript: rewritten tool definitions give "higher and better separability" and "higher recall".
- **C11:** the course's Lesson 3 notebook argues both sides. Deterministic loading: "context bootstrapping is non-negotiable", "the agent can't choose to look up what it doesn't know exists", predictability. Agent-triggered: relevance, cost and latency, judgment. The course mixes them per operation; this is one idea, so it is one question with complete builds (guide rule 5.6).
- **C12:** context summarization (lossy) and context compaction (offload with an id and description, pull the whole back when needed) are both taught in Lesson 5. The course's code combines them, and that combination is C12a.

**Subjects that are not questions:**
- **The stateless agent:** fails tests 1 and 2 (it breaks M1, and the course shows it failing).
- **Semantic cache** (Lesson 2's list of short-term memory): a component no stage uses (guide rule 3.3), never built.
- **Persona memory:** appears only on a Lesson 3 slide table with `write_persona`/`read_persona` and is never in code or transcript. A slide-only fact loses to code and transcripts; not built.
- **Graph-traversal retrieval** (Lesson 3 lists it): needs relationships between memories, which no stage of this program stores (guide rule 3.3).
- **Lexical-only retrieval:** test 3. Any situation for it is already served by C5b and C10b.
- **Reranking** (Lesson 2's recap of a document-QA pipeline): shown only as background on that pipeline, never tied to this program's stages (guide rule 3.3).
- **Distance metric, vector index type and every number in 5.6:** settings (guide rule 4.3).
- **The context-usage monitor:** it only shows what ran (guide rule 3.3). It is kept as the status line, not as a question.
- **The learner's machine:** no situation changes the build beyond C2c, C4 and C5.

**Where picked values came from (guide rules 4.2 and W4):**
- **Distance:** cosine (Lesson 3 transcript; Lesson 3–4 notebooks) vs Euclidean (Lesson 5–6 notebooks; the Lesson 3 notebook's own key-components table). Rule (1) picks cosine.
- **Vector index:** the Lesson 3 notebook text says HNSW; the course code builds IVF (neighbor partitions, target accuracy 95) to avoid HNSW errors on some Oracle versions. This matters only for C4b; use the code's.
- **Summarizer model:** `gpt-5-mini` (Lesson 5 notebook) vs `gpt-5` (helper used by the final app). Rule (2) picks `gpt-5`. The token-limit table is keyed `gpt-5-mini` in one and `gpt-5` in the other; both are 256000.
- **Entity writing:** agent-triggered (Lesson 3 notebook table) vs automatic each turn (final app code and the Lesson 6 transcript). Rule (2) picks automatic (D11).
- **Entity types:** "people, places and organization" (Lesson 6 transcript) and "place, people, and relationships to people" (Lesson 2) vs PERSON, PLACE, SYSTEM in code. No single stated list, so rule (2) picks the code's.
- **Sample conversation length in the course's test:** "30 messages" in notebook comments vs 32 entries in the helper and "32 messages" in the transcript. It is not used here.
- **`read_toolbox` k:** its docstring says 5 while its default is 3; the agent loop uses 5.
- **`get_current_time` rewriting:** rewritten in Lesson 4, not rewritten in the final app. The final app decides.
- **Summary thread scoping:** the Lesson 5 notebook stores summaries without a thread; the final helper scopes them to the thread. The final app decides.
- **`read_toolbox` as an agent tool:** Lesson 4 only; dropped in the final app (D10).
- **Tavily web search:** Lesson 4 only (D10, C9).

### B-4. Course code that looks like a bug
- **Conversation window** (kept, R4/T5). The course reads "the first 10 rows ordered by ascending time", which is the oldest 10 unsummarized messages, although the section's own text speaks of "recent turns". The instructor never says which ten, so the build keeps the course's behaviour as a setting. On a thread with more than 10 unsummarized messages and no summary yet, the newest turns are not loaded. Change the setting to "newest 10" if that bites.
- **Tool search text** (changed, D3). The course's registration computes a vector from the rewritten text but stores the row with the original docstring as its searched text. The instructor says the rewritten text is what gets embedded, so the build follows the instructor.
- **Summary input cut** (changed, D4). The course passes only the first 6000 characters of the transcript to the summarizer yet marks every message as summarized. The instructor describes 6000 as a limit on the response, so the build follows the instructor.
- **Unknown tool name.** The course returns an error string with status "success". This is kept (T17).
- **Workflow success.** The course always stores `success: true`, even when a step failed. This is kept.
- **Entity duplicates.** The course never de-duplicates entities. This is kept (T8).

### B-5. Names that go stale
Treat every name below as a search keyword against current documentation, not as a guaranteed import:
- **Database and vector store:** `OracleVS` (`langchain_oracledb.vectorstores`), `OracleVectorizerPreference` (`langchain_oracledb.retrievers.hybrid_search`), `DistanceStrategy` (`langchain_community.vectorstores.utils`), `oracledb`, Oracle AI Database 26ai, service `FREEPDB1`.
- **Embeddings:** `HuggingFaceEmbeddings` (`langchain_huggingface`, or `langchain_community.embeddings` in two notebooks), `sentence-transformers/paraphrase-mpnet-base-v2`.
- **Papers and chunking:** `ArxivRetriever`, `ArxivLoader` (`langchain_community`), `RecursiveCharacterTextSplitter` (`langchain_text_splitters`), `arxiv`, `pymupdf`.
- **Other services:** `TavilyClient` (`tavily-python`), `datasets.load_dataset` with the `nick007x/arxiv-papers` dataset.
- **Models:** OpenAI Chat Completions with `tools`, `tool_choice="auto"` and `max_completion_tokens`; models `gpt-5` and `gpt-5-mini`. The course never sets a temperature; check the current documentation for the chosen model before adding one.

### B-6. Course names
| Course name | This spec |
|---|---|
| `CONVERSATIONAL_MEMORY`, `SEMANTIC_MEMORY`, `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY`, `TOOL_LOG_MEMORY` | the seven stores (binding) |
| `MemoryManager`, `StoreManager` | the read/write operations of R1–R14 (not binding as names) |
| `Toolbox`, `register_tool(augment=…)` | R12 and the rewrite flag |
| `call_agent(query, thread_id, max_iterations)` | one turn (R3–R17) |
| `summarise_context_window`, `summarize_conversation`, `offload_to_summary` | R9, R8 |
| `[Summary ID: …]`, `## Conversation Memory` and the other section headings | binding text formats |
| the five tool names in 5.4 | binding: the model sees them |

### B-7. Lesson map (transcript numbering)
- **Lesson 1, Introduction:** the purpose, "memory engineering … external to the model, persistent and structured".
- **Lesson 2, Why AI Agents Need Memory:** F1; conversational memory; going beyond it (C6); the memory types; agent memory as embedding model + database + LLM; the agent memory core.
- **Lesson 3, Constructing the Memory Manager:** the stores and schemas (5.2), the memory manager, deterministic vs agent-triggered operations (C11), knowledge-base seeding (5.1), cosine (D5). Notebook file `L2.ipynb`.
- **Lesson 4, Scaling Agent Tool Use with Semantic Tool Memory:** toolbox (R12, C7, C8), Tavily (C9), the paper tools (5.4). Notebook `L3.ipynb`.
- **Lesson 5, Memory Operations: Extraction, Consolidation, and Self-Updating Memory:** context budget, summarization, expansion, marking (R8–R11, C12). Notebook `L4.ipynb`.
- **Lesson 6, Memory Aware Agent:** the agent loop and the final app (R3, R13, R14, R16, R17; T23 mirrors its five-call demo). Notebook `L5.ipynb`.
- **Lesson 7, Conclusion:** no new facts.

Notebook file numbers run one behind the transcripts. The notebooks file's own header map (L2→Lesson 4, L3→Lesson 5, L4→Lesson 6) does not match the notebooks' contents, so the lessons were matched by content; the transcripts decide lesson numbers. The transcripts also call Lesson 5 "lesson 4" and Lesson 6 "lesson 5" in passing.

**Slides read:** 19 wide images, Lesson 2. One of them is a leftover template slide about base vs instruction-tuned models and was ignored. 41 tall images cover Lessons 3–6. Slides the instructor talks through counted like that lesson's transcript. Two slide-only items lost: persona memory, and a workflow table schema (`run_id`, `thread_id`, `created_at`, `workflow_doc` JSON, `embedding`) that differs from the course code's vector store.

Nothing in this spec requires access to the course.

---

*Spec v2-draft · course: Agent Memory: Building Memory-Aware Agents · project: memory-aware tool-using agent · when the build agent does something unexpected, add the missing constraint here and re-run.*
