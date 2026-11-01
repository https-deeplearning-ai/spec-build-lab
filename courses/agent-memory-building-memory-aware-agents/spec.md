# Spec: a tool-using agent with memory outside the model

**What you're building:** a tool-using assistant whose memory lives outside the model, in a database on disk, so it carries on across turns and sessions. The default is a research assistant: you ask it for a paper, it finds and saves the paper, and a day later, in a new session, you can say "the paper" and it knows which one you mean. Along the way it records which tool steps worked, notes the people it meets, and when a conversation gets long it summarizes it, keeping the original messages one call away.

**What the recommended build needs to run:** an OpenAI API key (`OPENAI_API_KEY`), network access (paper search and download, and the first load of the embedding model), and a one-time download of the course's local embedding model.

**Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once `OPENAI_API_KEY` is set and are skipped until then; that is not a failure.

This file is self-contained: everything the build needs is in it. Nothing here requires access to the course.

*Provenance: generated from the course "Agent Memory: Building Memory-Aware Agents" (transcripts of Lessons 1–7, the four lesson notebooks with their helper module and requirements file, and the slide images), 2026-11-01, guide v2.9 (2026-10-31).*

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
   an OpenAI API key, network access, and a one-time download of the local embedding model), or **choose** question by
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
C1–C3 are context questions (your project, your model provider, where memory is stored); C4–C9 are the program's stages, in order.

### C1. What should the assistant work on?
- **C1a (Recommended - course default): Research assistant for papers.** The agent searches a public paper index, saves full papers into its knowledge base, and answers from them; the knowledge base starts from a file of paper records. *Pick this when* you want a working assistant over public papers, or want to see every memory kind working before changing anything. *Setup:* none beyond the build's model key; paper search needs network access.
- **C1b: Your own domain.** You name the agent's role, supply its tools and the documents that seed its knowledge base; all the memory machinery stays the same. *Pick this when* your agent works over different data, such as your notes, tickets or product docs, and the paper tools would be useless to you. *Setup:* whatever keys your own tools need.
  - *What to check:* the agent's role text and registered tools match your domain, and a question about one of your seeded documents is answered from the knowledge base.
- **C1c: Web research assistant.** The agent gets a web search tool that writes every result into the knowledge base, so a later question on the same topic is answered from memory without searching again. *Pick this when* your questions are about current events or general topics rather than papers; each search costs a call to a paid search service. *Setup:* a web search API key (for example Tavily, `TAVILY_API_KEY`).
  - *What to check:* each web search result is stored in the knowledge base with its title, URL and the query that found it, and a repeated question on the same topic is answered from the knowledge base without a new search.

### C2. Which model provider runs the agent?
- **C2a (Recommended - course default): OpenAI.** The agent loop and the helper roles (summarizer, labeler, entity extractor, tool describer) call OpenAI chat models with tool calling. *Pick this when* you have or can get an OpenAI key; the prompts in this spec were written for its models. *Setup:* `OPENAI_API_KEY`.
- **C2b: Another hosted provider.** The same roles call another provider whose models support tool calling. *Pick this when* you already pay for another provider; the prompts in this spec were written for OpenAI models, so summaries and tool choices need a look after switching. *Setup:* that provider's API key.
  - *What to check:* one real turn makes a tool call through the chosen provider and the tool's result reaches the model before the final answer.
- **C2c: A model served on your own machine.** The same roles call a locally served model that supports tool calling. *Pick this when* memory content must not leave your machine, or you have no API key; you need hardware that can run a tool-calling model. *Setup:* a model download and a local model server; no key.
  - *What to check:* one real turn makes a tool call through the local server with no request leaving the machine, and the tool's result reaches the model before the final answer.

### C3. Where is memory stored?
- **C3a (Recommended): One SQLite database file.** Every memory store is a table in one local file; vectors are stored beside each row and compared by the program. This is a stand-in for the course's Oracle AI Database. *Pick this when* the assistant runs on your own machine at personal scale; it needs no container or admin setup, but every similarity search reads every row of that store, which the course notes an index exists to avoid as data grows. *Setup:* none.
- **C3b (course default): Oracle AI Database 26ai.** The course's database: SQL tables for the conversation and tool logs, vector tables with vector indexes for the other stores. *Pick this when* you expect large stores that need vector indexes, or want several processes or users to share one memory; the course calls the database the agent's "memory core", the part that carries most of the agent's data traffic. *Setup:* a running database container (the course's took 30–60 seconds to start), an admin account to create the agent's database user, and a connection string.
  - *What to check:* after the app restarts, rows written before the restart are read back from the database, and each of the five vector stores has a vector index.

### C4. Which kinds of memory does the agent keep?
- **C4a (Recommended - course default): All memory kinds.** A per-thread conversation log, a knowledge base, workflow memory (which tool steps answered which request), entity memory (people, places, systems), summary memory, plus a tool log. *Pick this when* the agent does multi-step work over days and should reuse facts, steps and names across threads; each turn costs extra model calls for entity extraction. *Setup:* none.
- **C4b: Conversation log only.** Each thread's messages are stored and the thread's messages are loaded before every model call; the knowledge base, workflow, entity and summary stores are left out. *Pick this when* you want an assistant that simply picks up a conversation where it left off, even in a new session; the course warns that conversation windows are finite, valuable information often spans several conversations, and agents need structured, queryable knowledge, not just chat logs. *Setup:* none.
  - *What to check:* a new process given the same thread id answers a question about an earlier turn using the stored log, and no other memory store is created.

### C5. How does the agent get its tools each turn?
- **C5a (Recommended - course default): The five most relevant tools, retrieved per turn.** Tools live in a toolbox store; each turn the program searches it with the user's request and hands the model only the top five. *Pick this when* you have, or expect, many tools; the course argues this keeps tokens, latency and cost down and keeps tool choice reliable, and notes that providers recommend roughly 10–20 tools at most. *Setup:* none.
- **C5b: Every registered tool, every turn.** The model always sees the full tool list; no tool search. *Pick this when* you have fewer than about ten tools and want no retrieval step; the course warns that as tools grow, their definitions bloat the context, tool choice degrades, and latency and token cost rise. *Setup:* none.
  - *What to check:* every model call receives every registered tool, and a newly registered tool appears in the next call.
- **C5c: The five retrieved tools plus a toolbox-search tool.** As C5a, and the agent can also call a tool that searches the toolbox mid-turn; tools it finds are added to the tools offered on its next model call. *Pick this when* tasks often need a tool the first search misses; it lets the agent find capabilities beyond those first provided, at the cost of extra model iterations and tokens. *Setup:* none.
  - *What to check:* when a request needs a tool outside the first five, the agent calls the toolbox search and then calls the found tool in the same turn.

### C6. Which embedding model turns memory into vectors?
*Ask only when C4 is C4a or C5 is C5a or C5c.*
- **C6a (Recommended - course default): A local sentence-embedding model.** The course's model, `sentence-transformers/paraphrase-mpnet-base-v2` (768-dimensional vectors), runs on your machine. *Pick this when* you can install a local machine-learning library and download the model once; no key, and memory text stays on your machine. *Setup:* a one-time model download.
- **C6b: Your provider's embedding API.** Vectors come from a hosted embedding endpoint. *Pick this when* you cannot install the local libraries or download the model; every memory write and search then sends text to the provider and costs a call, and changing embedding models later means re-embedding every store. *Setup:* the provider's API key (often the same key as C2).
  - *What to check:* every store and every query uses the same embedding model, and the app refuses to search a store whose vectors came from a different model until it is re-embedded.

### C7. How is the knowledge base searched?
*Ask only when C4 is C4a.*
- **C7a (Recommended - course default): Meaning-based similarity.** The request is embedded and the three closest passages are loaded. *Pick this when* your documents are ordinary prose; it is the simplest search. *Setup:* none.
- **C7b: Hybrid keyword and meaning search.** Passages are scored by both keyword match and meaning, and the three best combined are loaded. *Pick this when* your documents hold exact codes, ids or names that meaning-based search misses; the course names hybrid retrieval, two or more strategies combined, as a common way to retrieve memory; the cost is a second index to keep. *Setup:* none extra on SQLite (its built-in full-text index); a vectorizer preference on Oracle.
  - *What to check:* a request naming an exact identifier loads the passage containing it among the three, even when meaning-based scoring alone would not rank it there.
- **C7c: Similarity plus a reranking model.** More candidates are fetched by similarity, a reranking model reorders them, and its top three are loaded. *Pick this when* your knowledge base is large and the three closest passages often miss the best one; the cost is an extra model to download or call, and more latency per turn. *Setup:* a reranking model download or API key.
  - *What to check:* the search fetches more than three candidates and the three loaded are the reranker's top three, in its order.

### C8. Which memory actions run automatically, and which does the agent decide?
*Ask only when C4 is C4a.*
- **C8a (Recommended - course default): The program reads and writes; the agent may summarize and expand.** Before every turn the program loads every memory store; after it, the program saves the conversation, the steps taken and any entities. Summarizing runs automatically when the context is nearly full and is also a tool the agent can call; expanding a summary back into its messages is a tool only the agent calls. *Pick this when* you want memory always loaded and always saved, with the model deciding only when compression or detail is worth its cost; the course argues automatic reading avoids the "you need memory to know which memory you need" problem and automatic saving means nothing is forgotten. *Setup:* none.
- **C8b: The program does everything.** No memory tools for the agent: summarizing runs only at the threshold, and the summary memory section carries each summary's full text instead of an id to expand. *Pick this when* your model calls tools unreliably, or you want every run to be predictable and easy to debug; the course argues agent-triggered actions keep memory relevant and save tokens, and here the agent cannot bring back details a summary dropped. *Setup:* none.
  - *What to check:* the agent is offered no memory tool, and a fact present only in a summary reaches the model as summary text in the context.
- **C8c: The agent decides what to read.** The program still saves everything automatically and still loads the conversation and the list of summaries before every model call; the knowledge base, workflow and entity stores are read through tools the agent calls. *Pick this when* your stores are large and most turns need none of them, so you want to save context tokens; the course warns the agent cannot choose to look up what it does not know exists, so it may answer as if it had no memory. *Setup:* none.
  - *What to check:* when a stored fact answers the request, the agent calls the matching read tool before answering and the fact appears in the answer.

### C9. What happens to old messages when the conversation is summarized?
*Ask only when C4 is C4a.*
- **C9a (Recommended - course default): Summarize, keep the originals, expand on demand.** The summarized messages stay stored, tagged with the summary's id, and drop out of the conversation section; the summary can be expanded back into them. *Pick this when* you may later need exact wording or order of earlier messages; storage grows with every message. *Setup:* none.
- **C9b: Summarize and delete the originals.** Only the summary survives. *Pick this when* rules forbid keeping raw messages beyond a summary; the course warns summarizing "will always lose a little bit of information", and here it cannot be recovered. *Setup:* none.
  - *What to check:* after a summary is made, the thread's original messages no longer exist in storage and the summary is still loaded on the thread's later turns.

## 2. Departures from the course

1. **Storage stand-in (C3a).** The course stores memory in Oracle AI Database 26ai, run in a container with admin setup. The recommended build uses one SQLite file, labelled a stand-in, with similarity computed by the program over stored vectors instead of the database's vector indexes. Reason: container and admin setup; at personal scale the file keeps every must-stay-true item.
2. **Stores are never dropped on start.** Every course notebook drops all memory tables at its start ("clean slate") so each lesson runs alone. The app creates missing stores and keeps existing ones. Reason: dropping on start would erase memory between sessions, which breaks the first must-stay-true item.
3. **Toolbox search text.** The course's code computes an embedding from the LLM-improved tool description and example queries, but the store then embeds only the tool's name, original docstring and signature. The instructor states the improved description is what gets embedded, so the build embeds name, improved description and example queries (4.1: follow the instructor). The signature string is left out of the search text.
4. **Summarize threshold is "at or above 80%".** The course's code summarizes only above 80%; the instructor says "reaches 80%" and "exceeded or is equal to 80%". The build follows the instructor.
5. **Distance is cosine.** The instructor introduces the stores with cosine distance (Lesson 3, and the Lesson 3–4 notebooks); the Lesson 5–6 notebooks switch to Euclidean. The build uses cosine (4.2 rule 1).
6. **Web search tool left out (offered as C1c).** Lesson 4 built a web search tool that needs a paid key; the course's final agent does not register it, and the keyless paper tools already show search results being saved to memory.
7. **Toolbox-search tool left out (offered as C5c).** Lesson 4 exposed toolbox search as an agent tool; the course's final agent does not register it.
8. **Seed data.** The course streams the first 100 records of a public paper dataset into the knowledge base. The build seeds from a small paper-records file whose records are written for this spec (Section 7, S1), and accepts any file of the same shape.
9. **Workflow step text.** The course writes each step's arguments in its language's dictionary notation; the build writes them as a JSON object.
10. **Model ids.** The course's model ids (Section 5.6) are facts about the course; the build agent names a current model per role in the checklist, because course-era ids go stale.
11. **Additions** (not taught by the course): the offline test suite and its scripted stand-ins (model, embedder, paper source); a command-line entry point; the `MEMORY_DB_PATH` setting; microsecond timestamps with insertion-order tie-breaking (the course slept 50 ms between writes instead).

## 3. Objective
Build an agent that answers each request with tools and with memory loaded from persistent stores, saves what each turn produced, and keeps working across turns, threads and process restarts.

## 4. Tech stack and versions
- **Language:** Python, current release. The package is named `memory_agent`.
- **Storage:** Python's standard `sqlite3` module (C3a stand-in). Course fact: Oracle AI Database 26ai Free, reached through the `oracledb` driver and LangChain's Oracle vector store integration.
- **Model client:** the current OpenAI Python SDK, chat completions with tool calling (C2a).
- **Embedding model:** the current `sentence-transformers` release loading `sentence-transformers/paraphrase-mpnet-base-v2` (C6a).
- **Paper source:** the public arXiv API and a PDF-to-text library, current releases (the course used LangChain's arXiv retriever and loader over the `arxiv` and `pymupdf` packages).
- **Text splitting:** a recursive character splitter (the course used LangChain's `RecursiveCharacterTextSplitter`), current release.
- **Tests:** `pytest` (addition), with a `live` marker.
- **Versions:** use current releases. The course's requirements file names packages without versions, so there are no course pins to carry.
- **Secrets:** read `OPENAI_API_KEY` (and `TAVILY_API_KEY` for C1c, provider keys for C2b/C6b/C7c) from the environment; a `.env` file in the working directory may supply them (the course loaded one). Never write a key to a file the app creates, a log or the database. Database credentials for C3b also come from the environment.

## 5. Contracts

### 5.1 Entry points (addition)
- `call_agent(query: str, thread_id: str = "1", max_iterations: int = 10) -> str` — one turn; returns the final answer.
- `python -m memory_agent chat --thread <id>` — reads one request per line and prints each answer.
- `python -m memory_agent seed <path.jsonl>` — loads paper records into the knowledge base (Rule R6).
- `MEMORY_DB_PATH` (default `memory.db`) names the store file.

### 5.2 Stores
Store names are the course's table names and are binding.

```json
{
  "CONVERSATIONAL_MEMORY": {
    "type": "object",
    "required": ["id", "thread_id", "role", "content", "timestamp", "metadata", "created_at"],
    "properties": {
      "id": {"type": "string", "pattern": "^[0-9a-f]{32}$", "description": "generated, unique"},
      "thread_id": {"type": "string", "minLength": 1, "maxLength": 100},
      "role": {"enum": ["user", "assistant"]},
      "content": {"type": "string"},
      "timestamp": {"type": "string", "format": "date-time", "description": "set at insert, microsecond precision"},
      "metadata": {"type": "string", "default": "{}"},
      "created_at": {"type": "string", "format": "date-time"},
      "summary_id": {"type": ["string", "null"], "pattern": "^[0-9a-f]{8}$", "default": null}
    }
  },
  "TOOL_LOG_MEMORY": {
    "type": "object",
    "required": ["id", "thread_id", "tool_name", "status", "timestamp"],
    "properties": {
      "id": {"type": "string", "pattern": "^[0-9a-f]{32}$"},
      "thread_id": {"type": "string", "maxLength": 100},
      "tool_call_id": {"type": ["string", "null"], "maxLength": 200},
      "tool_name": {"type": "string", "maxLength": 200},
      "tool_args": {"type": "string", "description": "JSON text"},
      "result": {"type": "string", "description": "full, never truncated"},
      "result_preview": {"type": "string", "description": "first 2000 bytes of result in UTF-8, cut at a character boundary"},
      "status": {"enum": ["success", "failed"], "default": "success"},
      "error_message": {"type": ["string", "null"]},
      "metadata": {"type": "string", "description": "JSON text {\"iteration\": n}, n starting at 1"},
      "timestamp": {"type": "string", "format": "date-time"},
      "created_at": {"type": "string", "format": "date-time"}
    }
  },
  "VECTOR_STORE_ROW (SEMANTIC_MEMORY, WORKFLOW_MEMORY, TOOLBOX_MEMORY, ENTITY_MEMORY, SUMMARY_MEMORY)": {
    "type": "object",
    "required": ["id", "text", "metadata", "embedding"],
    "properties": {
      "id": {"type": "string"},
      "text": {"type": "string", "description": "the text that was embedded"},
      "metadata": {"type": "object"},
      "embedding": {"type": "array", "items": {"type": "number"}}
    }
  }
}
```

Metadata per vector store:
- **SEMANTIC_MEMORY** (knowledge base). Seed record: `{arxiv_id, title, subjects, abstract, submission_date}`. Paper chunk: `{source: "arxiv", arxiv_id, title, entry_id, published, authors, chunk_id (0-based), num_chunks, ingested_ts_utc}`. Web result (C1c only): `{title, url, score, source_type: "tavily_search", query, timestamp}`.
- **WORKFLOW_MEMORY:** `{query, success: true, num_steps (integer ≥ 1), timestamp}`.
- **TOOLBOX_MEMORY:** `{name, description, parameters: {<param>: {name, type?, default?}}, return_type, augmented (boolean), queries (array of strings, only when augmented)}`.
- **ENTITY_MEMORY:** `{name, type ("PERSON" | "PLACE" | "SYSTEM", or "UNKNOWN" when the extractor gave none), description}`.
- **SUMMARY_MEMORY:** `{id (8 lowercase hex characters), full_content, summary, description, thread_id (null for a summary of free text)}`; the row's text is `"<id>: <description>"`.

Vector search returns the top k rows by cosine similarity whether or not their score is above zero; a query or row with an all-zero vector scores 0; ties go to the row stored first. A search may carry an equality filter on metadata fields.

### 5.3 Tool schema handed to the model
```json
{"type": "function",
 "function": {"name": "<tool name>", "description": "<stored description>",
   "parameters": {"type": "object",
     "properties": {"<param>": {"type": "string | integer | number | boolean"}},
     "required": ["<every parameter without a default>"]}}}
```
A parameter whose type is unknown is typed `string`. A tool name appears at most once per list.

### 5.4 Registered tools (C1a)
| Tool | Parameters (defaults) | Improved description? | Behaviour |
|---|---|---|---|
| `arxiv_search_candidates` | `query`, `k` (5) | no | Searches the paper source; returns a JSON array of up to `k` candidates, each `{arxiv_id, entry_id, title, authors, published, abstract}`; `arxiv_id` is the part of `entry_id`'s path after `/abs/`; `abstract` is cut to 2500 characters. |
| `fetch_and_save_paper_to_kb_db` | `arxiv_id`, `chunk_size` (1500), `chunk_overlap` (200) | yes | Fetches one paper's full text, splits it into chunks of at most `chunk_size` characters overlapping by `chunk_overlap`, stores each chunk in the knowledge base with chunk metadata, returns `Saved arXiv <id> to SEMANTIC_MEMORY: <n> chunks (title: <title>).` Unknown id → `No documents found for arXiv id: <id>`; empty text → `Loaded arXiv <id> but extracted empty text (PDF parsing issue).` |
| `get_current_time` | `detailed` (false) | no | Returns local time as `YYYY-MM-DD HH:MM:SS`, with `.ffffff` microseconds when `detailed`. |
| `expand_summary` | `summary_id`, `thread_id` (none) | yes | Rule R19. |
| `summarize_and_store` | `text` (""), `thread_id` (none) | yes | With `thread_id`: summarizes that thread (R17), returns `Stored as [Summary ID: <id>] <description>` or `No unsummarized messages found for thread <id>.` Without: summarizes `text` (not tied to a thread); empty text → ``Provide `thread_id` (preferred) or non-empty `text` to summarize.`` |

The original one-line descriptions: search — "Search arXiv and return a JSON list of candidate papers with IDs + metadata."; fetch — "Fetch full arXiv paper text and store it into the knowledge base as chunked records."; time — "Returns the current time."; expand — "Expand a summary reference to retrieve the original conversations. Use when you need more details from a [Summary ID: xxx] reference."; summarize — "Summarize content and store it in Summary Memory. Provide thread_id to summarize unsummarized conversation units and mark them."

### 5.5 Context window layout (binding)
The first user message of each turn is:

```
# Question
<query>

## Conversation Memory
...
## Knowledge Base Memory
...
## Workflow Memory
...
## Entity Memory
...
## Summary Memory
...
```

Each `## … Memory` section has, in order: `### What this memory is` (one sentence), `### How you should leverage it` (two or three bullets, written for the build, saying how the model should use that store), then the retrieved items under `### Retrieved messages` / `### Retrieved passages` / `### Retrieved workflows` / `### Retrieved entities` / `### Available summaries`. Empty results show exactly: `(No unsummarized messages found for this thread.)`, `(No relevant knowledge base passages found.)`, `(No relevant workflows found.)`, `(No entities found.)`, `(No summaries available for thread <thread_id>.)`.

Item formats: conversation `[HH:MM:SS] [<role>] <content>`; knowledge base, each passage's text on its own lines; workflows, each record's text separated by a line `---`; entities `• <name>: <description>`; summaries, a line `Use expand_summary(id) to retrieve the detailed underlying conversation.`, a line `Scope: thread_id = <thread_id>`, then one line per summary `  • [ID: <id>] <description>`.

### 5.6 Model roles
| Role | Calls | Course model (fact) |
|---|---|---|
| agent | the agent loop, with tools, tool choice left to the model | `gpt-5-mini` |
| summarizer | summary text (R17) | `gpt-5` in the final agent; `gpt-5-mini` in the Lesson 5 notebook |
| labeler | the 8–12 word summary label (R17) | same as summarizer |
| entity_extractor | entities from text (R8) | `gpt-5` |
| tool_describer | improved tool description (R9) | `gpt-5` |
| query_generator | example requests for a tool (R9) | `gpt-5` |

### 5.7 Settings
| Setting | Value | Course source | Change this when … |
|---|---|---|---|
| conversation messages loaded | 10 | final agent's conversation read | your threads are long and turns are short |
| knowledge base passages loaded | 3 | final agent's knowledge base read | answers need more passages |
| workflows loaded | 3, only those with ≥ 1 step | final agent's workflow read | — |
| entities loaded | 5 | final agent's entity read | — |
| summaries listed | 10, current thread only | final agent's summary read | — |
| tools per turn | 5 | final agent (`k=5`); course: "test with different values of K" | your requests need more tools at once |
| max agent iterations | 10 | final agent | tasks need longer tool chains |
| context token limit | 256000 | course's limit table for its model; unknown model → 128000 | your model's window differs |
| characters per token | 4 | Lesson 5: "some divide by two, some divide by four" | your model's tokenizer is denser |
| summarize threshold | ≥ 80% of the limit | Lessons 5–6 (instructor) | — |
| usage status bands | ok < 50%, warning < 80%, critical ≥ 80% | Lesson 5 monitor | — |
| tool result sent to model | first 3000 characters | final agent | your model's window is small |
| tool log preview | 2000 bytes | tool log store | — |
| summary input | first 6000 characters of the transcript | summarizer | "try different prompts" (Lesson 5) |
| summary output limit | 4000 completion tokens; label 2000 | summarizer | — |
| retry summary length | ≤ 180 words | summarizer retry | — |
| fallback excerpt | first 500 characters | summarizer fallback | — |
| summary label | 8–12 words | labeler | — |
| summary id | 8 lowercase hex characters (start of a random UUID) | summarizer | — |
| entity extraction input | first 500 characters; texts under 5 characters skipped | entity extractor | — |
| workflow answer excerpt | first 200 characters | workflow write | — |
| step argument display | string values cut to 50 characters + `...` | agent loop | — |
| chunk size / overlap | 1500 / 200 characters | paper fetch tool ("embeddings have input limits") | your embedder's input limit differs |
| paper search | up to 8 results fetched, 4000 characters each; `k` 5; abstract 2500 characters | paper search tool | — |
| example queries per improved tool | 5 | tool registration | — |
| similarity | cosine | Lesson 3 (instructor) | — |
| embedding model | `sentence-transformers/paraphrase-mpnet-base-v2`, 768 dimensions | Lessons 3–6 | C6 |

## 6. Business rules

### What must stay true (the course's pattern card)
Every build, whatever is chosen above, keeps both:
1. **Memory lives outside the model and survives the session.** What the agent learns in one turn or session is stored in persistent storage and is available to later turns and new sessions; nothing depends on the model or the process remembering it. (Rule R2; tests T02, T10.)
2. **Before the model answers, the memory relevant to the request reaches its context.** (Rule R5; tests T05, T10.)

### Rules
- **R1. Stores on start.** On start the app creates any missing store of the seven (`CONVERSATIONAL_MEMORY`, `TOOL_LOG_MEMORY`, `SEMANTIC_MEMORY`, `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY`) and never drops or clears an existing one. → T01, T02
- **R2. Persistence.** Everything written to a store is readable by a new process opened on the same store file. → T02, T10, L1
- **R3. Conversation write.** Each message is stored with its thread id, role, content, a microsecond timestamp and no summary id. Messages written in the same instant keep insertion order. → T03
- **R4. Conversation read.** The conversation section lists the thread's messages that have no summary id, oldest first, at most 10. Note for the build agent: this is the course's code, which takes the 10 *oldest* unsummarized messages, not the 10 newest; keep it. → T03, T04
- **R5. Context before the model.** Each turn, before the first model call, the program builds the context of 5.5: the request under `# Question`, then the five sections in order, each read with the request (the conversation and summary sections with the thread id). The request is stored in the conversation only after the context is built, so it never appears in its own conversation section. The system message is the agent prompt (R11). → T05, T10, L1
- **R6. Knowledge base.** A knowledge base write stores text with metadata; a read embeds the request and loads the 3 most similar passages. Seeding reads a JSON-lines file of `{arxiv_id, title, subjects, abstract, submission_date}`; each record's text is title, subjects and abstract joined by newlines, leaving out empty parts; a record whose title, subjects and abstract are all empty is skipped. → T06, L2
- **R7. Workflow memory.** After a turn with at least one tool call, the program stores one workflow whose text is `Query: <request>` / `Steps:` / one line `Step <i>: <tool>(<args as JSON>) → success|failed` per call / `Answer: <first 200 characters of the answer>`, with metadata `num_steps` and `success: true`. A turn without tool calls stores none. A read loads the 3 most similar workflows that have at least one step. → T07, T10
- **R8. Entity memory.** The program sends the request (before the loop) and the final answer (after it) to the entity extractor, which returns a JSON array of `{name, type, description}`; each entity is stored with text `<name> (<type>): <description>`, the type being `UNKNOWN` when the extractor gave none. Text under 5 characters is not sent. A reply that holds no JSON array, or any extractor error, stores nothing and the turn carries on. A read loads the 5 most similar entities. → T08, T10
- **R9. Toolbox registration.** Registering a tool stores its name, description, parameters (with types and defaults) and return type. When the tool is marked for improvement, the tool describer writes a richer description from the tool's original description and source (one-line summary, steps, when an agent should call it, caveats) and the query generator is asked for 5 example requests, of which every one returned is kept; the stored description is the improved one. The row's search text is `<name> <description> <example requests joined by spaces>`. A name already in the toolbox is not stored again, but the tool is still callable. → T09
- **R10. Tool selection.** Each turn the program searches the toolbox with the request and passes the model the top 5 tools as 5.3 schemas. → T09, T11
- **R11. Agent loop.** The system message tells the model: it is a memory-aware research assistant with tools; its input holds a `# Question` and five memory segments, named exactly as in 5.5, each with a stated purpose; when a needed detail is only in Summary Memory it calls `expand_summary` first; it uses memory before tools; on conflict it trusts the current question, then the latest conversation, then knowledge base evidence, then older summaries and workflows; it uses only the tools offered and as few calls as needed; when memory is not enough it says what is missing and then uses a tool; for compaction it calls `summarize_and_store` with the thread id. The program calls the model with the messages and tools; for every tool call it runs the tool and appends the result as a tool message; it stops when a reply has no tool calls (that reply is the answer). After 10 iterations without such a reply, the answer is `I was unable to complete the request within the allowed iterations.` → T10, T12, L1
- **R12. Tool execution.** A call to a tool name that is not registered returns `Error: Tool '<name>' not found` and is logged with status `success` (the course's code returns this text instead of raising; keep it). A tool that raises returns `Error: <message>`, is logged with status `failed` and that message, and its step ends `→ failed`. A `summarize_and_store` call without `thread_id` gets the current thread id. → T13, T14, T10
- **R13. Tool log and truncation.** Every tool call is stored in the tool log with its full result, preview, status, error and iteration. The model receives the result unchanged when it is at most 3000 characters; otherwise the first 3000 characters, then a blank line, then `[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <log id>]`. → T15
- **R14. After the loop.** The program stores the workflow (R7), the answer's entities (R8) and the answer as an `assistant` message. → T10
- **R15. Context usage.** Estimated tokens = number of characters in the memory sections (everything after the question) divided by 4, rounded down; percent = tokens ÷ limit × 100, rounded to one decimal; status ok below 50, warning below 80, critical at 80 or above. → T16
- **R16. Automatic summarizing.** When usage of the memory sections is at or above 80%, before the model is called the program summarizes the thread's unsummarized messages (R17), replaces the whole conversation section with exactly the three lines `## Conversation Memory` / `Older conversation content was summarized to reduce context size.` / `Use Summary Memory references + expand_summary(id) for full detail.`, and appends the line `[Summary ID: <id>] <description>` at the end of the summary section. The question is never summarized. When the thread has nothing to summarize the context is unchanged. → T17
- **R17. Summarizing a thread.** The transcript is the thread's unsummarized messages, oldest first, one line each `[YYYY-MM-DD HH:MM:SS] [<ROLE in capitals>] <content>`. The summarizer receives its first 6000 characters and must answer under exactly the headings `### Technical Information`, `### Emotional Context`, `### Entities & References`, `### Action Items & Decisions`, keeping concrete details, separating facts from open questions, inventing nothing. An empty reply is retried once with a shorter prompt asking for at most 180 words under the same headings; a second empty reply gives a fallback summary: the four headings, the first 500 characters of the transcript (newlines turned to spaces) under Technical Information, and `Not available from model output.` under each other heading. The labeler then writes an 8–12 word label; an empty label or one of `conversation summary`, `summary`, `chat summary`, `thread summary` (any case) is replaced by the first 12 words of the first summary line that is not a heading and has at least 4 words (with leading `-•* ` and trailing ` ,.;:` removed), or else `Recent thread context, decisions, and open actions`. The summary is stored with a new 8-hex id, the full transcript, the summary, the label and the thread id, and exactly the messages in the transcript get that id. A thread with no unsummarized messages produces no summary. → T17, T18, T19
- **R18. Summary list.** The summary section lists up to 10 of the thread's summaries as id and label only, never the summary text. → T10, T20
- **R19. Expanding a summary.** `expand_summary(id)` returns `## Summary Context`, the stored summary text, a blank line, then `## Expanded Conversations for Summary ID: <id>`, `Total messages: <n>`, a blank line, and for each message tagged with that id, oldest first, a line `[YYYY-MM-DD HH:MM:SS] [<ROLE>]`, its content and a blank line. An unknown id gives `Summary <id> not found.` (or `Summary <id> not found for thread <thread_id>.` when a thread id was given) and `No conversations found for summary_id: <id>`. When a thread id is given, the summary is looked up only among that thread's summaries. → T10, T20
- **R20. Built-in tools.** The paper and time tools behave as 5.4. → T21, T22, T24, L3
- **R21. Earlier turns resolve from memory.** A follow-up that refers to an earlier turn of the thread without naming it ("the paper") is resolved from stored memory, in the same or any later session. → T10, T23

## 7. Tests

### 7.1 Sample data (all facts invented for this spec)
**S1 `sample_data/papers_seed.jsonl`** — four records, one per line:
1. `{"arxiv_id": "2502.00011", "title": "Coral Reef Acoustics Under Warming Seas", "subjects": "Physics - Atmospheric and Oceanic Physics", "abstract": "We recorded reef soundscapes at six sites and found that snapping shrimp activity drops by 40 percent when water is above 30 degrees Celsius.", "submission_date": "2025-02-03"}`
2. `{"arxiv_id": "2502.00022", "title": "Lunar Regolith Bricks for Habitat Shielding", "subjects": "Astrophysics - Instrumentation and Methods", "abstract": "Sintered lunar regolith bricks 50 centimetres thick block 85 percent of the galactic cosmic ray dose, which supports long space exploration missions.", "submission_date": "2025-02-10"}`
3. `{"arxiv_id": "2502.00033", "title": "Sparse Retrieval for Long Legal Documents", "subjects": "Computer Science - Information Retrieval", "abstract": "A keyword index over contract clauses beats dense retrieval on exact clause numbers by 12 points of recall.", "submission_date": "2025-02-17"}`
4. `{"arxiv_id": "2502.00044", "title": "", "subjects": "", "abstract": "", "submission_date": "2025-02-20"}` (must be skipped)

**S2 `paper_source_stub.py`** — stand-in for the arXiv API (labelled a stand-in). `search(query)` returns, for every query, one candidate: entry id `http://arxiv.org/abs/2501.01234v1`, title `Tiered Recall: Paging Memory for Language Agents`, authors `Ada Moreno, Kenji Ito`, published `2025-01-15`, abstract `We give a language agent a main context and an archive tier, and let it page facts between them with function calls.` `fetch(arxiv_id)` returns, for `2501.01234v1` only, the same metadata and this full text: paragraph one `Tiered Recall: Paging Memory for Language Agents. Key takeaways of this paper: (1) facts are paged between a main context and an archive tier; (2) paging is done with function calls; (3) old messages stay searchable.`, a blank line, then paragraph two: the sentence `The archive tier stores every past message with a timestamp. ` repeated 30 times (1830 characters). For `2501.00000v1` it returns title `Empty Scan`, the same authors and published date, and empty text. Any other id returns nothing.

**S3 `term_embedder.py`** — stand-in embedder (labelled a stand-in). Lower-case the text, split on every character that is not `a–z` or `0–9`, drop tokens of one character and the stopwords `the a an of on to and or in for is it me my you your can what was are with by from this that be as at its`; the vector is the count of each remaining token. Similarity is cosine over these counts.

**S4 `scripted_model.py`** — stand-in model (labelled a stand-in). It receives the role name with each call, records every call's messages and tools, and replies:
- *agent* — matched on the text of the `# Question` line; "after a tool result" means the last message is a tool message:
  - A1 contains `get me the paper on tiered recall`: first call → tool call `arxiv_search_candidates {"query": "tiered recall paging memory"}`; after a tool result → `Found it: "Tiered Recall: Paging Memory for Language Agents" (arXiv 2501.01234v1) by Ada Moreno and Kenji Ito.`
  - A2 contains `save the content of the paper`: if the context contains `2501.01234v1` → first call: tool call `fetch_and_save_paper_to_kb_db {"arxiv_id": "2501.01234v1"}`; after a tool result → `Saved paper 2501.01234v1 to the knowledge base.` If not → `I have no record of which paper you mean. Please name it.` with no tool call.
  - A3 contains `key takeaways`: if the context contains `Key takeaways` → `The paper's key takeaways: facts are paged between a main context and an archive tier; paging is done with function calls; old messages stay searchable.`; else `I do not have the paper's text.` No tool call.
  - A4 contains `Summarize the conversation`: first call → tool call `summarize_and_store {}`; after → `I stored a summary of our conversation.`
  - A5 contains `What was my first question`: first call → if the context contains `[ID: ` followed by 8 hex characters and `]`, tool call `expand_summary {"summary_id": "<the first such id>"}`, else `I don't know.`; after a tool result → if it contains `Can you get me the paper on tiered recall?`, `Your first question was: "Can you get me the paper on tiered recall?"`, else `I don't know.`
  - A6 contains `Loop forever`: every call → tool call `get_current_time {}`.
  - A7 contains `Dump the log`: first call → tool call `dump_text {}`; after → `Dumped.`
  - A8 contains `Teleport me`: first call → tool call `teleport {}`; after → `I cannot teleport.`
  - A9 contains `Break something`: first call → tool call `always_fails {}`; after → `The tool failed.`
  - A10 contains `Search long`: first call → tool call `arxiv_search_candidates {"query": "<the letter q repeated 60 times>"}`; after → `Done.`
  - anything else → `OK.`
- *summarizer* → `### Technical Information\nThe user asked for the Tiered Recall paper (2501.01234v1) and saved it.\n### Emotional Context\nNeutral.\n### Entities & References\nAda Moreno, Kenji Ito.\n### Action Items & Decisions\nNone.` In *empty mode* (set by a test) → empty string. In *terse mode* → `### Technical Information\nok\n### Emotional Context\nok`.
- *labeler* → `Tiered Recall paper search, save and takeaways with Ada Moreno`. In empty mode and terse mode → `Conversation summary`.
- *entity_extractor* → if the text contains `Ada Moreno`: `[{"name": "Ada Moreno", "type": "PERSON", "description": "co-author of Tiered Recall"}, {"name": "Kenji Ito", "type": "PERSON", "description": "co-author of Tiered Recall"}]`; if it contains `Lena Park`: `[{"name": "Lena Park", "description": "editor"}]`; else `[]`. In *junk mode* → `no entities here`.
- *tool_describer* → the row below whose tool name appears in its prompt:
  - `fetch_and_save_paper_to_kb_db`: `Download the full text of a paper by its arXiv id, split it into chunks and save the chunks into the knowledge base. Call it when the user asks to save, store or ingest a paper.`
  - `expand_summary`: `Expand a summary ID back into the original conversation messages in time order. Call it when a detail is only in Summary Memory.`
  - `summarize_and_store`: `Summarize the unsummarized messages of the current thread, store the summary and mark those messages as summarized. Call it when asked to summarize or compact the conversation.`
- *query_generator* → for the same three tools, a JSON array: fetch `["save this paper to memory", "store the paper content"]`; expand `["what did I ask earlier", "show the original messages behind a summary"]`; summarize `["summarize our conversation", "compact the chat history"]`.

**S5 test tools** (`sample_data/test_tools.py`, no improved description): `convert_units` ("Convert a value between metric and imperial units."), `lookup_weather` ("Look up the weather forecast for a city."), `dump_text` ("Return a long block of text for testing."; returns `x` × 3500), `always_fails` ("A tool that always raises an error."; raises an error with message `boom`).

**S6 research scenario** — thread `t-research`, five requests in order: (1) `Can you get me the paper on tiered recall?` (2) `Can you save the content of the paper?` — the planted instance of the course's stateless-agent failure: it names no paper and can only be answered from memory. (3) `What are the main key takeaways from the paper?` (4) `Summarize the conversation so far using your tool` (5) `What was my first question?`

**S7 short thread** — thread `t-long`, four messages: user `My deadline for the survey is 14 March.`; assistant `Noted: the survey is due 14 March.`; user `Use the archive-tier paper as the main source.`; assistant `Understood: Tiered Recall is the main source.`

**Standard fixture:** a fresh store file; S1 seeded; the five tools of 5.4 registered in table order, then the four S5 tools; S2, S3, S4 wired in; default settings.

### 7.2 Test table
All tests run offline on the standard fixture unless stated.

| Test | Rules | Given / When / Then |
|---|---|---|
| T01 | R1 | Given a path with no store file, when the app starts, then all seven stores exist and the conversation, tool log, knowledge base, workflow, entity and summary stores are empty; a knowledge base read on the empty store gives `(No relevant knowledge base passages found.)`. |
| T02 | R1, R2 | Given process A writes message `hello` (user, thread `t-p`) and seeds S1, when A closes and process B starts on the same file, then B's conversation read for `t-p` contains `[user] hello`, the knowledge base holds 3 records, and starting B created or cleared nothing. |
| T03 | R3, R4 | Given messages `one`, `two`, `three` written to `t-a` in that order and `other` to `t-b`, when `t-a` is read, then it lists exactly `one`, `two`, `three` in that order, each as `[HH:MM:SS] [<role>] <content>`, without `other`; reading `t-z` gives `(No unsummarized messages found for this thread.)`. |
| T04 | R4 | Given messages `m01` … `m12` written to `t-c`, when `t-c` is read, then `m01` … `m10` appear and `m11`, `m12` do not. |
| T05 | R5 | When `call_agent("Tell me about space exploration", "t-ctx")` runs, then the first agent call's user message starts with `# Question\nTell me about space exploration\n\n## Conversation Memory`; the five section headings appear in the order of 5.5; the conversation, workflow, entity and summary sections show `(No unsummarized messages found for this thread.)`, `(No relevant workflows found.)`, `(No entities found.)` and `(No summaries available for thread t-ctx.)`; the knowledge base section contains `Lunar Regolith Bricks for Habitat Shielding`; the system message names all five segments and `expand_summary`; the answer is `OK.` |
| T06 | R6 | Then the knowledge base holds 3 records (record 4 skipped); a read for `space exploration` lists 3 passages, the first starting `Lunar Regolith Bricks for Habitat Shielding`, whose metadata has `arxiv_id` `2502.00022` and `submission_date` `2025-02-10`. |
| T07 | R7 | Given T10's turn 1, then the workflow store holds one record whose text is `Query: Can you get me the paper on tiered recall?` / `Steps:` / `Step 1: arxiv_search_candidates({"query": "tiered recall paging memory"}) → success` / `Answer: ` + the A1 answer, with `num_steps` 1 and `success` true; after turn 3 the count is unchanged. Given four more workflows written directly, a workflow read lists exactly 3. A workflow written directly with a 300-character answer stores only its first 200 characters after `Answer: `. `call_agent("Search long", "t-arg")` stores the step `Step 1: arxiv_search_candidates({"query": "<q × 50>..."}) → success`. |
| T08 | R8 | Given T10's turn 1, then the entity store holds exactly `Ada Moreno (PERSON): co-author of Tiered Recall` and `Kenji Ito (PERSON): co-author of Tiered Recall`. Writing entities from text `ok` makes no model call and stores nothing. Writing entities from `Lena Park joined the team.` stores `Lena Park (UNKNOWN): editor`. Writing entities from `"b" × 500 + "QQQQ" × 25` sends a prompt containing no `QQQQ`. With the extractor in junk mode, a turn completes and stores no entity. Given six entities stored directly, an entity read lists exactly 5 lines starting `• `. |
| T09 | R9, R10 | Then the toolbox holds 9 rows; registering `fetch_and_save_paper_to_kb_db` again leaves 9; the tool describer and query generator were each called exactly 3 times; the stored description of the fetch tool is S4's describer text; a toolbox search for `Get more details on a paper on AI` with k = 1 returns only `fetch_and_save_paper_to_kb_db`; the schema of `arxiv_search_candidates` has `query` typed `string`, `k` typed `integer`, and `required` equal to `["query"]`. |
| T10 | R2, R5, R7, R8, R11, R12, R14, R18, R19, R21 | Run S6 on thread `t-research`: request 1 in process A, requests 2–4 in process B, request 5 in process C, all on one store file. Then: (1) one call to `arxiv_search_candidates` with `{"query": "tiered recall paging memory"}`, answer = A1's. (2) the first agent call's conversation section contains `2501.01234v1`; `fetch_and_save_paper_to_kb_db` is called with `2501.01234v1`; answer `Saved paper 2501.01234v1 to the knowledge base.` (3) the knowledge base section contains `Key takeaways of this paper`; one agent call; answer = A3's first reply. (4) `summarize_and_store` runs with `thread_id` `t-research` supplied by the program; its result is `Stored as [Summary ID: <id>] Tiered Recall paper search, save and takeaways with Ada Moreno` with `<id>` matching `^[0-9a-f]{8}$`; 7 messages carry that id; answer `I stored a summary of our conversation.` (5) the first agent call's conversation section lists exactly one message, `[assistant] I stored a summary of our conversation.`; its summary section contains `[ID: <id>] Tiered Recall paper search, save and takeaways with Ada Moreno` and not `### Technical Information`; `expand_summary` is called with `<id>` and its result contains `Total messages: 7` and `Can you get me the paper on tiered recall?`; answer `Your first question was: "Can you get me the paper on tiered recall?"`. Finally: 10 conversation messages for the thread (7 with a summary id), 4 workflows, 4 tool log rows, 2 entities. |
| T11 | R10 | In T10's request 1, the first agent call receives exactly 5 tools: `arxiv_search_candidates`, `fetch_and_save_paper_to_kb_db`, `get_current_time`, `expand_summary`, `summarize_and_store` (none of the S5 tools). |
| T12 | R11 | When `call_agent("Loop forever", "t-loop")` runs, then the agent is called 10 times, the answer is `I was unable to complete the request within the allowed iterations.`, the tool log holds 10 rows for `t-loop` with iterations 1–10, one workflow with `num_steps` 10 is stored, and the thread holds the user and assistant messages. |
| T13 | R12 | When `call_agent("Teleport me", "t-tp")` runs, then the tool message sent to the model is `Error: Tool 'teleport' not found`, the tool log row has status `success`, and the answer is `I cannot teleport.` |
| T14 | R12 | When `call_agent("Break something", "t-bad")` runs, then the tool message is `Error: boom`, the tool log row has status `failed` and error `boom`, the workflow step is `Step 1: always_fails({}) → failed`, and the answer is `The tool failed.` |
| T15 | R13 | When `call_agent("Dump the log", "t-dump")` runs, then the tool message is 3000 `x` characters, a blank line, and `[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <id>]` where `<id>` is the tool log row's id; that row's result is 3500 characters and its preview 2000 bytes; the answer is `Dumped.` |
| T16 | R15 | With limit 500 tokens: memory text of 1600 characters → 400 tokens, 80.0%, `critical`; 1596 → 399, 79.8%, `warning`; 1000 → 250, 50.0%, `warning`; 996 → 249, 49.8%, `ok`. |
| T17 | R16, R17 | With the token limit set to 100: given S7 stored for `t-long`, when `call_agent("Where do we stand?", "t-long")` runs, then before the first agent call all 4 S7 messages carry one 8-hex id; that call's context starts `# Question\nWhere do we stand?`, its conversation section is exactly the three stub lines and contains no `14 March`, and the context ends with `[Summary ID: <id>] Tiered Recall paper search, save and takeaways with Ada Moreno`. With the same limit, `call_agent("Hi", "t-empty")` creates no summary and its conversation section shows `(No unsummarized messages found for this thread.)`. |
| T18 | R17 | Given S7 stored for `t-long`, when `summarize_and_store(thread_id="t-long")` is called, then it returns `Stored as [Summary ID: <id>] Tiered Recall paper search, save and takeaways with Ada Moreno`; the summary row has `thread_id` `t-long`, the S4 summary text, and `full_content` of 4 lines, the first matching `^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] \[USER\] My deadline for the survey is 14 March\.$`; the summarizer prompt contains all four headings; all 4 messages carry `<id>`. Calling it again returns `No unsummarized messages found for thread t-long.` and stores nothing. `summarize_and_store(text="a" * 6000 + "ZZZZ" * 250)` sends the summarizer a prompt that contains no `ZZZZ`. `summarize_and_store()` with neither argument returns ``Provide `thread_id` (preferred) or non-empty `text` to summarize.`` |
| T19 | R17 | With summarizer and labeler in empty mode, `summarize_and_store(thread_id="t-long")` on S7: the summarizer is called twice, the second prompt containing `180 words`; the stored summary starts `### Technical Information\n` followed by the first 500 characters of the transcript with newlines as spaces, and contains `Not available from model output.` three times; the label equals the first 12 space-separated words of that excerpt line, with trailing ` ,.;:` removed. With summarizer and labeler in terse mode, the label is `Recent thread context, decisions, and open actions`. |
| T20 | R18, R19 | `expand_summary("deadbeef")` contains `Summary deadbeef not found.` and `No conversations found for summary_id: deadbeef`; `expand_summary("deadbeef", "t-s")` contains `Summary deadbeef not found for thread t-s.` Given 11 summaries stored for thread `t-s`, the summary section for `t-s` lists exactly 10 `[ID: ` lines and no summary text. |
| T21 | R20 | `arxiv_search_candidates("anything", 5)` returns a JSON array of one object with `arxiv_id` `2501.01234v1`, `entry_id` `http://arxiv.org/abs/2501.01234v1`, `title` `Tiered Recall: Paging Memory for Language Agents`, `authors` `Ada Moreno, Kenji Ito`, `published` `2025-01-15`. |
| T22 | R20 | `fetch_and_save_paper_to_kb_db("2501.01234v1")` returns `Saved arXiv 2501.01234v1 to SEMANTIC_MEMORY: <n> chunks (title: Tiered Recall: Paging Memory for Language Agents).` with n ≥ 2; n new knowledge base rows, each ≤ 1500 characters, with `chunk_id` 0 … n−1, `num_chunks` n, `source` `arxiv`; every sentence of the full text appears in some chunk. `fetch_and_save_paper_to_kb_db("9999.99999")` returns `No documents found for arXiv id: 9999.99999` and adds no row; `fetch_and_save_paper_to_kb_db("2501.00000v1")` returns `Loaded arXiv 2501.00000v1 but extracted empty text (PDF parsing issue).` and adds no row. |
| T24 | R20 | `get_current_time()` matches `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$`; `get_current_time(detailed=True)` matches the same followed by `\.\d{6}$`. |
| T23 | R21 | Given a fresh store with nothing written for `t-research`, when S6 request 2 runs, then no tool is called and the answer is `I have no record of which paper you mean. Please name it.` (the planted failure, which T10 shows memory prevents). |
| L1 `live` | R5, R11, R2 | With `OPENAI_API_KEY` set and network access: run S6 requests 1 and 2 against the real model, embedder and arXiv in two processes; then request 2's first context contains the arXiv id found in request 1 and the knowledge base gains chunks for that id. |
| L2 `live` | R6 | With network access: the real embedder returns 768-number vectors, and after seeding S1 a read for `space exploration` lists the lunar regolith record first. |
| L3 `live` | R20 | With network access: a real `arxiv_search_candidates` call for `memory paging language agents` returns at least one candidate with a non-empty `arxiv_id`. |

## 8. Standing permissions
- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in in its own description; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has data; anything that sends data to a third party.
- **Never:** invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets.

## 9. Test plan
- Offline: `python -m pytest -m "not live"` — must pass in full.
- Live: `python -m pytest -m live` — runs when `OPENAI_API_KEY` is set (L2 and L3 need network only); skipped otherwise, which is not a failure.
- Adjust the recommended tests to the chosen options (for example C5b changes T11 to "all registered tools"; C4b leaves out the tests of stores it removes), and for every chosen non-recommended option write one test from its "what to check" sentence (copied into `resolved-decisions.md`) and report it.
- Report a result per test with evidence (test output, file paths). "Should pass" counts as not run.
- The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.
- Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

## 10. Background notes

### The program
A tool-using agent whose memory lives outside the model. Stages, in order:
- **create stores** → so memory outlives the process (course: memory as "first-class infrastructure, external to the model, persistent and structured", Lesson 1);
- **register tools in a toolbox** → tools become searchable memory instead of prompt text (Lesson 4);
- **read memory into a partitioned context** → the model sees relevant memory, labelled by kind, before it answers (Lessons 3, 6);
- **check context usage and summarize when nearly full** → the context stays within the model's window (Lessons 5–6);
- **select tools by similarity** → the model sees only the few relevant tools (Lesson 4);
- **write the request; run the agent loop** (assemble, invoke, act until a stop condition) **with tool results offloaded to the tool log** → the agent acts while large outputs stay out of the context (Lesson 6);
- **write back the workflow, entities and answer** → the next turn and the next session can use what this one produced (Lesson 6).
The course's example, a research assistant over papers, is the recommended build's sample instance (C1).

### Failures
- **Stateless agent forgets (demonstrated, Lesson 2).** What you see: in a later turn the user says "book the first one" and the agent answers that it has no recollection of the conversation. Why: nothing from earlier turns is stored outside the model. Prevention: every turn is stored and reloaded before the model answers. Enforced by R2, R5, R21; planted as S6 request 2; tested by T10 and T23.
- **Too many tools in the prompt (warned, Lesson 4).** Context bloat and confusion, worse tool choice, more latency and tokens. Enforced by R10; tested by T11.
- **Context overflow (warned, Lesson 5 notebook: "context overflow crashes the agent").** Enforced by R15, R16; tested by T16, T17.
- **Re-summarizing already summarized messages (warned, Lesson 5).** Enforced by R17 (exact rows tagged, tagged rows skipped); tested by T18.
- **Tool output bloat (warned, Lesson 6).** Enforced by R13; tested by T15.
- **Agent loop never reaching an answer (warned, Lesson 6 stop conditions: final answer, error or timeout).** Enforced by R11; tested by T12.
- **Empty summary from the model (handled in the course's code by retry and fallback).** Enforced by R17; tested by T19.
- **"Forgetting to save" (warned, Lesson 3 notebook).** The course makes saving automatic; enforced by R14; tested by T10.

### Why the questions and settings are what they are
- **C1.** The course's example is a research assistant; its tools are generic paper search and fetch. Lesson 4 also built a web search tool that saves results to the knowledge base (the "search-and-store pattern").
- **C2.** The course used OpenAI throughout; other providers are paths a learner's situation needs.
- **C3.** The course calls the database the "agent memory core", the component with the most data traffic; it says an index lets a database find items without scanning them all.
- **C4.** Lesson 2 builds a naive memory-augmented agent with conversation memory only, then argues for going beyond it: "conversation windows are finite, but user relationships are not", "not all valuable information is stored in a single conversation", "agents need structured, queryable knowledge, not just chat logs". These are costs, not demonstrated failures, so the simpler build is offered.
- **C5.** Lesson 4: tool definitions in the prompt cause context bloat, tool-selection degradation, latency and cost; providers suggest roughly 10–20 tools. The Lesson 4 notebook also exposes toolbox search as an agent tool "to autonomously query for tools mid-execution".
- **C7.** Lesson 3 names lexical, vector, graph traversal and hybrid retrieval and sets up (but never calls) a hybrid-search preference for the knowledge base; Lesson 2's retrieval pipeline includes a reranking model.
- **C8.** Lesson 3 classifies operations as deterministic (run by the program) or agent-triggered (tools). Arguments for deterministic: context bootstrapping, "the agent can't choose to look up what it doesn't know exists", predictability, nothing forgotten. Arguments for agent-triggered: relevance, cost and latency control, better judgement about what to store or compress. The course disagrees with itself on entity writes: the Lesson 3 notebook table marks them agent-triggered, but the Lesson 6 instructor lists them among the operations outside the loop and the final agent runs them automatically; the build follows the instructor (4.2 rule 1). The same table marks toolbox reads as both; the final agent only reads the toolbox automatically.
- **C9.** Lesson 5 contrasts summarization (lossy: "we will always lose a little bit of information") with compaction (move content to the database with an id and description, fetch it on demand). The course's code combines them: a stored summary plus tagged originals and an expand tool. Its Lesson 6 demo shows the agent expanding a summary to recall the first question.
- **Not questions:**
  - Tool description improvement is set per tool by whoever registers it (the course improves some tools and not others in the same build), so it stays a per-tool flag, not a build-wide choice.
  - A stateless agent with no stored memory breaks must-stay-true item 1 (fails test 1).
  - Semantic cache, working memory and a persona memory kind appear in the course's taxonomy (persona only on slides); none is an alternative to one of the program's stages, and none is built or described.
  - Graph-traversal retrieval is named once in a list; the stores hold text passages with no relationships to traverse, so no learner situation makes it the right way to search them (fails test 3).
  - Memory decay, merging and contradiction handling are named as examples of judgement calls but never built or described.
  - Fine-tuning embedders, model versioning and continual learning are listed as disciplines memory engineering draws on, not parts of this program.
  - Marking every unsummarized message of the thread (an older helper) versus marking exactly the summarized rows: the course's final code marks exact rows, and no situation favours marking messages the summary never saw (fails test 3).
  - Exposing the tool log to the agent: the course stores it "for audit and just-in-time retrieval" but never gives the agent a way to read it.
  - Which model the tests use is never asked: offline tests use the stand-ins.
- **Where picked values came from:** distance — cosine (Lesson 3 instructor, Lesson 3–4 notebooks) over Euclidean (Lesson 5–6 notebooks), rule 1. Threshold — "at or above 80%" (Lessons 5–6 instructor) over the code's "above 80%", rule 1. Toolbox search text — instructor's description over the code's behaviour, 4.1. Tools per turn — 5 (final agent) over the toolbox read default of 3 and a tool docstring saying 5. Token limit 256000 — the course's limit table (listed for `gpt-5` in the final helper and `gpt-5-mini` in the Lesson 5 notebook; same value). Summary model — `gpt-5` (final helper) over `gpt-5-mini` (Lesson 5 notebook), rule 2. Every other value in 5.7 has one course source.
- **Other course code behaviour kept:** the conversation read takes the 10 oldest unsummarized messages (R4); an unknown tool is logged as `success` (R12); entities are also extracted from the request before the loop (the instructor mentions only the answer); the workflow `success` flag is always true.

### Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports: `OracleVS`, `OracleVectorizerPreference`, `DistanceStrategy.COSINE` / `EUCLIDEAN_DISTANCE`, `langchain_oracledb`, `HuggingFaceEmbeddings` (imported from both `langchain_huggingface` and `langchain_community.embeddings` in different lessons), `ArxivRetriever`, `ArxivLoader`, `RecursiveCharacterTextSplitter`, `TavilyClient`, `oracledb`, `load_dataset`, Oracle AI Database 26ai Free, `gpt-5`, `gpt-5-mini`, `sentence-transformers/paraphrase-mpnet-base-v2`. The course's model calls set `max_completion_tokens` and never set `temperature`; keep any temperature at the provider's default unless the chosen model accepts another.

### Course names
| Course name | Spec term |
|---|---|
| `CONVERSATIONAL_MEMORY`, `SEMANTIC_MEMORY`, `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY`, `TOOL_LOG_MEMORY` | the seven stores (binding names) |
| Memory Manager | the component that reads and writes every store |
| StoreManager | store creation and lookup |
| Toolbox | tool registration and search (R9, R10) |
| memory unit | one stored row |
| `call_agent` | one turn (binding entry point) |
| `summarize_and_store`, `expand_summary`, `arxiv_search_candidates`, `fetch_and_save_paper_to_kb_db`, `get_current_time` | tool names (binding) |
| `[Summary ID: <id>]`, `[ID: <id>]` | summary references (binding formats) |
| agent harness | the program code around the agent loop |
| ArxivScout | the course's name for its seeded knowledge base |

### Lesson map (transcript numbering)
- **L1 Introduction** — memory as infrastructure outside the model; card item 1.
- **L2 Why AI Agents Need Memory** — stateless vs memory-augmented agents (demonstrated failure), conversation memory and its limits (C4), memory kinds, the agent memory core (C3), retrieval pipeline with reranking (C7); card items 1 and 2.
- **L3 Constructing the Memory Manager** (notebook titled "L2") — stores and their schemas, cosine distance, deterministic vs agent-triggered operations (C8), memory awareness via the system prompt and partitioned context, knowledge base seeding.
- **L4 Scaling Agent Tool Use with Semantic Tool Memory** (notebook titled "L3") — toolbox, improved descriptions, paper and web tools, toolbox search as a tool (C1, C5).
- **L5 Memory Operations: Extraction, Consolidation, and Self-Updating Memory** (notebook titled "L4") — context usage, summarization vs compaction (C9), summary expansion, exact-row tagging, workflow memory.
- **L6 Memory Aware Agent** (notebook titled "L5") — the agent loop, memory operations in and out of the loop, the final end-to-end agent and its five-turn demo; card item 2.
- **L7 Conclusion.**
The notebook file names, and the instructors' own spoken lesson counts, run one behind the transcript headings; the transcript headings decide. Slides: 41 tall and 19 wide images were read; all except one template slide match slides the instructors talk through in Lessons 2–6 and count like those transcripts; the template slide (base vs instruction-tuned models) was ignored. Nothing in this spec requires access to the course.

---
*Spec v2 draft · Agent Memory: Building Memory-Aware Agents · memory_agent · When the build agent does something unexpected, add the missing constraint here and re-run.*
