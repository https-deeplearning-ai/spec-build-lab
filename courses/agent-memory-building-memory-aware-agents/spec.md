# Spec: an assistant whose memory lives outside the model

**What you're building:** a tool-using assistant whose memory lives in a database outside the model, so it carries on across turns and sessions. By default it is the course's research assistant: you ask it to find a paper, save it and discuss it. It remembers the conversation, the papers it saved, the steps it took and the names it came across. It shrinks old conversation into summaries it can expand again. When you close it and come back later, it still knows what you talked about.

**Fastest path:** answer "recommended build" at the first question below. The build is finished when the offline tests pass. They need no key, because scripted stand-ins replace the model, the embedder and the paper search. `live` tests that are skipped because no key is set are expected, not failures.

**To run for real**, the recommended build needs an OpenAI API key (`OPENAI_API_KEY`), network access to arXiv for paper search and download, and a one-time download of the course's embedding model.

This file is self-contained. Everything the build needs is in it.

*Provenance: course "Agent Memory: Building Memory-Aware Agents" · materials used: transcripts of Lessons 1–7, the code notebooks for Lessons 3–6 with their shared helper module and requirements list, 60 slide images (Lesson 2 deck and Lessons 3–6 deck) · generated 2026-10-27 · guide v2.7 (2026-10-27).*

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
   an OpenAI API key, network access to arXiv, and a one-time download of the embedding model), or **choose** question by
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

## Questions

Context questions come first (C1–C3), then the program's stages in order (C4–C12).

### C1. Where does the assistant get knowledge from outside the conversation?
- **C1a — Research papers (Recommended - course default).** The assistant searches arXiv for candidate papers, downloads a chosen paper's full text, and saves it in chunks to its knowledge base. A clock tool tells it the date and time. Its knowledge base starts with a small set of paper records. *Pick this when* you work with research papers or want the course's own example. *Setup:* no key; needs network access to arXiv.
- **C1b — Your own folder of documents.** The assistant gets two tools instead of the arXiv ones. One lists the documents in a folder you name that match a request, giving path, title (first line) and a 300-character preview. The other saves one document to the knowledge base, using the same chunk sizes and recording the file path in each chunk's metadata. The clock tool stays. *Pick this when* your material is your own notes or files, e.g. "ask my English notes", not public papers. *Setup:* none; no network needed for knowledge. *What to check:* saving a file from the folder stores its chunks in the knowledge base, each with the file path in its metadata, and a question in a later session on the same thread finds a passage from that file in Knowledge Base Memory.
- **C1c — The web, search-and-store.** The assistant gets a web-search tool that returns up to 5 results. It also writes each result to the knowledge base as "Title / Content / URL" text, with metadata title, url, score, source_type `web_search`, query and timestamp, so later questions can use it without searching again. The clock tool stays. *Pick this when* your questions are about current or general web content rather than papers. *Setup:* a web-search API key (paid or quota-limited, depending on the service). *What to check:* after one search, every returned result is a knowledge-base row with its URL and the query, and a later question on the same topic shows that row in Knowledge Base Memory.

### C2. Which model provider runs the assistant?
- **C2a — OpenAI (Recommended - course default).** Chat completions with tool calling. *Pick this when* you have, or can get, an OpenAI key. *Setup:* `OPENAI_API_KEY`; paid per use.
- **C2b — Another hosted provider with tool calling.** *Pick this when* you already pay for a different provider and want one bill. *Setup:* that provider's key; paid per use. *What to check:* a turn that needs a tool produces a tool call through that provider's tool-calling interface, the loop sends the result back, and the final answer arrives in the same turn.
- **C2c — A model served on your own machine, with tool calling.** *Pick this when* no conversation text may leave your machine. *Setup:* a model download and a machine that can run it; smaller local models call tools less reliably. *What to check:* the same tool-call round trip as C2b works with no network connection to any hosted model provider.

### C3. How do you talk to it?
- **C3a — Terminal chat (Recommended).** A command-line program. You give it a thread id, each line you type is one turn, and it prints context usage, the tools it was offered, its tool calls and its answer. *Pick this when* you are the only user and work in a terminal. *Setup:* none.
- **C3b — A local web chat page.** A page served on your own machine with a thread-id field, a message box and the answer. *Pick this when* you would rather use a browser, or want to show it to someone at your desk. *Setup:* one web-framework dependency. *What to check:* the page sends each message with its thread id, shows the answer, and reopening the page with the same thread id after the server restarts continues the conversation from the database.

### C4. Where is memory stored?
- **C4a — One SQLite file on your machine, searched in-process (Recommended).** *Stand-in for the course's Oracle AI Database:* the same seven stores, each a table in one file (default `memory.db`). Vector search is an exact similarity scan in the program. *Pick this when* you want it to run with no setup. *Setup:* none (Python's standard library). Searches slow down as stores reach many thousands of rows, because there is no vector index.
- **C4b — Oracle AI Database 26ai in a local container, with its vector search (course default).** *Pick this when* you want the course's actual database, or expect stores large enough that a vector index matters. *Setup:* a container runtime, a database image download, and admin setup: a database user with grants and a tablespace that supports JSON columns. *What to check:* all seven stores are tables in the database, each vector store has a vector index, and a message written before restarting the app is read back after it.

### C5. Which kinds of memory does the assistant keep?
- **C5a — All seven (Recommended - course default):** conversation, knowledge base, workflow, toolbox, entity, summary and tool log. *Pick this when* the assistant should learn from documents, past task steps and names, not just the chat. *Setup:* none beyond C4 and C6.
- **C5b — Conversation memory only, with its summaries.** It keeps the conversation log, the summaries made from it, and the tool log. It has no knowledge base, workflow, entity or toolbox store, and needs no embedder. Every tool is offered on every turn. Tools whose only job is saving to the knowledge base are left out, and search tools return their results straight to the model. Summary Memory lists the thread's summaries newest first, up to 10. Memory reads and writes work as in C11a. *Pick this when* the assistant only has to remember what was said, e.g. a study companion that should recall last week's discussion, and there is no document library to build up. *Costs (course):* "conversation windows are finite; user relationships aren't"; agents "need structured, queryable knowledge — not just chat logs"; nothing is kept from task steps or from names mentioned. *Setup:* none; no embedding download. *What to check:* a fact the user states in one session appears in Conversation Memory, or in a summary of it, at the first turn of a new session on the same thread, and no knowledge base, workflow, entity or toolbox store is created.

### C6. Which embedding model turns text into searchable vectors?
*Ask only when C5 is C5a.*
- **C6a — The course's local sentence-transformers model, `sentence-transformers/paraphrase-mpnet-base-v2`, 768 dimensions (Recommended - course default).** *Pick this when* you can do a one-time download and want meaning-based search that never leaves your machine. *Setup:* a one-time download of the model and its machine-learning runtime; no key.
- **C6b — The model provider's hosted embedding service.** *Pick this when* you cannot download models, and sending your memory text to the provider is acceptable. *Setup:* the same key as C2 and a cost per call; every stored text is sent to the provider. *What to check:* every stored vector has the provider model's dimension, and the same query returns the same top passage before and after a restart.
- **C6c — The word-overlap stand-in (the one the offline tests use).** *Stand-in for an embedding model.* Each text becomes counts of its words, and similarity is the cosine of those counts. *Pick this when* your data is tiny and nothing may be downloaded or sent anywhere. *Cost:* it only matches shared words and misses paraphrases. *Setup:* none. *What to check:* a query that shares a distinctive word with exactly one stored passage ranks that passage first.

### C7. How does the model get its tools?
*Ask only when C5 is C5a.*
- **C7a — Toolbox search: tools are stored with searchable descriptions, and the 5 most relevant to the request are offered (Recommended - course default).** *Pick this when* you expect the tool list to grow. *Setup:* none.
- **C7b — Every registered tool on every turn.** *Pick this when* you have only a handful of tools (under about ten) and want no retrieval step. *Costs (course):* every tool definition uses context tokens; as tools grow, tool selection degrades and latency and cost rise; providers recommend limiting the number of tools. *Setup:* none. *What to check:* every registered tool is offered on every model call, whatever the request.
- **C7c — Toolbox search plus a tool to search for more.** The 5 most relevant tools are offered, and one more tool lets the agent search the toolbox mid-turn. Tools it finds are offered on the next model call of the same turn. *Pick this when* you have many tools and multi-step tasks often need one that the first five missed. *Cost:* extra model calls when the agent searches. *Setup:* none. *What to check:* when the model calls the toolbox-search tool, the tools it returns are among those offered on the next model call of that turn.

### C8. Should the model improve tool descriptions when tools are registered?
*Ask only when C5 is C5a and C7 is C7a or C7c.*
- **C8a — As the course did (Recommended - course default).** The knowledge-saving tool, the web-search tool (if C1c), and the expand and summarize tools are improved. The search-candidates tool, the document-listing tool (if C1b) and the clock tool keep their own descriptions. For an improved tool, the model rewrites its description from the code and invents 5 example requests, and both become part of its searchable text. *Pick this when* your tools have short descriptions. *Setup:* two model calls per improved tool, at its first registration only.
- **C8b — No improvement: every tool is stored with the description written in code.** *Pick this when* you write detailed tool descriptions yourself, or start-up must make no model calls. *Cost (course):* plain descriptions sit closer together in search, so the right tool is found less reliably. *Setup:* none. *What to check:* registering tools makes no model calls, and each tool's stored description equals the one written in code.

### C9. How is the knowledge base searched?
*Ask only when C5 is C5a.*
- **C9a — By meaning only: the 3 passages most similar to the request (Recommended - course default).** *Pick this when* your material is ordinary prose. *Setup:* none.
- **C9b — Hybrid: meaning plus exact keywords, merged.** *Pick this when* your material is full of exact terms that meaning search can miss, such as IDs, part codes or names. *Setup:* a keyword index (SQLite full-text search with C4a; the database's hybrid index with C4b). *What to check:* a query made of one rare code that appears in exactly one passage returns that passage among the 3, even when its meaning similarity is low.

### C10. Should retrieved knowledge be re-ranked before it reaches the model?
*Ask only when C5 is C5a.*
- **C10a — No re-ranking (Recommended - course default).** *Pick this when* the knowledge base is small, as in the sample. *Setup:* none.
- **C10b — Re-rank with a reranking model.** More candidates are fetched (10), and the reranker keeps the best 3. *Pick this when* the knowledge base holds thousands of passages and the top 3 by similarity are often off-topic. *Cost (course):* deep retrieval and reranking cost tokens and time. *Setup:* a reranking model download, or a reranking API key. *What to check:* the reranker receives 10 candidates, and the 3 passages shown are its 3 highest-scored.

### C11. Which memory actions run automatically, and which does the agent decide?
*Ask only when C5 is C5a.*
- **C11a — The program reads all memory before each answer and writes it back after; the agent decides only to expand a summary, to summarize when asked, and to use its outside tools (Recommended - course default).** *Pick this when* you want memory always loaded and always saved. *Setup:* none.
- **C11b — The program does all memory work.** No memory tool is offered, the conversation is shrunk only by the automatic size check, and Summary Memory shows each summary's full text, since the agent cannot expand it. *Pick this when* your model calls tools unreliably, or every turn must behave the same for testing and debugging (course: predictable behaviour, easier debugging). *Costs (course):* the agent cannot judge what is worth compressing or expanding; old detail beyond a summary cannot be recovered; full summaries use more context. *Setup:* none. *What to check:* no memory tool is ever offered to the model, and each of the thread's summaries appears as full text in Summary Memory.
- **C11c — The agent decides what to read.** Only Conversation Memory is read automatically, and the system prompt lists the other stores. The agent gets read tools for the knowledge base, workflows, entities and summaries, and decides when to save an entity. Conversation and workflow writes stay automatic. *Pick this when* most requests need no stored knowledge and you want to save tokens (course: cost and latency control, less clutter). *Costs (course):* "the agent can't choose to look up what it doesn't know exists"; without automatic retrieval it can behave as if stateless; behaviour is less predictable. *Setup:* none. *What to check:* Conversation Memory is in every first model call, the knowledge base is read only when the model calls its read tool, and a stored fact asked about directly is found through that tool before the answer.

### C12. When the conversation is shrunk, what is kept?
- **C12a — A summary plus the original messages, which the agent can expand by the summary's id (Recommended - course default).** *Pick this when* you want short context but exact recall on demand. *Setup:* none.
- **C12b — The summary only.** After the summary is stored, the summarized messages are deleted. Summary Memory shows each summary's full text, and the expand tool is not offered. *Pick this when* a retention rule says raw chat text must not be kept, e.g. personal data. *Cost (course):* summarizing is lossy — "we will always lose a little bit of information"; exact earlier wording is gone. *Setup:* none. *What to check:* after shrinking, the summarized messages are gone from every store, the summary row exists, and its full text appears in Summary Memory.
- **C12c — A label plus the original messages, with no summary text.** The agent sees only a short label per shrunk block and expands it to read the originals. With C11b, where nothing can be expanded, the program shows the originals under the label instead. *Pick this when* exact wording matters and a paraphrase could mislead, e.g. notes where a reworded instruction would be wrong. *Cost:* the agent has to expand before it knows anything about older turns, which means more tool calls. *Setup:* none. *What to check:* after shrinking, Summary Memory shows a label per block and no summary text, and expanding returns the original messages word for word.

---

## Departures from the course (the gate shows these)

| # | The recommended build does | The course did | Why |
|---|---|---|---|
| D1 | Stores memory in one SQLite file, using an exact similarity scan (stand-in, C4a) | Oracle AI Database 26ai in a container, through LangChain's Oracle vector store, with IVF vector indexes | The course database needs container and admin setup (4.4). Everything in section 6 still holds: the file persists. |
| D2 | Uses cosine similarity for every vector store | Cosine in the Lesson 3 and 4 code; Euclidean distance in the Lesson 5 and 6 code | The instructor states cosine when introducing the distance (Lesson 3). Rule 4.2(1). |
| D3 | Seeds the knowledge base from the spec's sample paper file (4 records) | Streamed 100 paper records from a public dataset | No course data is copied (4.5); no download is needed. |
| D4 | Makes an improved tool's searchable text its name, improved description, signature and 5 example requests | The code built that text but searched on the tool's original description and signature; the improved text was only kept as metadata | The instructor says the improved text "is what gets embedded and stored" (Lesson 4). 4.1 says to follow the instructor. |
| D5 | Caps the stored summary at 6,000 characters and sends the whole transcript to the summarizer | The code cut the summarizer's input at 6,000 characters | The instructor describes 6,000 characters as the limit on the final response (Lesson 5). Rule 4.2(1). |
| D6 | Never drops or clears a store on start | Each lesson notebook dropped every table at the start, for a clean slate | Dropping would break "memory survives the session" (section 6). The clean slate was a teaching convenience. |
| D7 | Runs as a terminal program (C3a) | Ran as notebook cells | A notebook is how the course was taught, not part of the program. |
| D8 | Uses current library releases and a current model for each role, picked at the gate | Unpinned packages of its era; models `gpt-5-mini` (agent) and `gpt-5` (other roles) | Course-era names go stale (4.6, 4.7). |
| D9 | Breaks ties between messages with the same timestamp by insertion order | Waited 50 ms between test writes so timestamps differed | Addition: makes the order deterministic. |
| D10 | Has offline tests driven by scripted stand-ins, a missing-key check, and a test-only `--scripted` flag | Checks were printouts in the notebooks | Additions so the build can be finished and checked (P6). |
| D11 | Reads passwords for C4b from the environment | Hard-coded the database passwords | Addition: secrets from the environment. |

---

## Objective

Build a terminal program in which an agent answers each request after loading the relevant memory from persistent stores, calls tools when it needs to, and writes the turn back, so that it continues correctly across turns, restarts and long conversations.

## Tech stack and versions

- **Language:** Python, current release. Package `memory_agent`, run as `python -m memory_agent`. Tests use `pytest` under `tests/`.
- **Libraries (current releases, no pins):** `openai` (C2a); `sentence-transformers` (C6a), optionally through `langchain-huggingface` as the course did; `langchain-community` arXiv retriever and loader, which need the `arxiv` and `pymupdf` packages (C1a), or the `arxiv` package directly if those loaders no longer install; `langchain-text-splitters` recursive character splitter (any splitter with the same behaviour, R22, is acceptable); `python-dotenv`. SQLite comes from the standard library (C4a).
- **Course facts, for information:** the course's requirements list named `langchain-oracledb`, `langchain-huggingface`, `sentence-transformers`, `langchain-community`, `langchain-openai`, `datasets`, `langchain`, `tavily-python`, `pydantic`, `oracledb`, `openai`, `dotenv`, `arxiv` and `pymupdf`, none of them pinned. It used Oracle AI Database 26ai. No Python version was stated.
- **Secrets:** `OPENAI_API_KEY`, plus any key that C1c, C2b, C6b or C10b needs, are read from the environment or a `.env` file. They are never written to any store, log or printout.

## Contracts

### Command line (C3a)
| Command | Behaviour |
|---|---|
| `python -m memory_agent seed --papers PATH [--db PATH]` | Loads paper records (S1 format) into the knowledge base (R23). Prints `Seeded N records`. Needs no model key. |
| `python -m memory_agent chat --thread ID [--db PATH]` | Interactive. Each input line is one turn (R17); `exit` quits. |
| `python -m memory_agent ask --thread ID [--db PATH] "QUESTION"` | Runs one turn, prints its output, exits 0. |
| `--scripted` (test only) | Swaps in the scripted stand-ins S5, S6 and S4. Documented as test-only. |

The default database path is `memory.db` in the working directory. On every start the program opens or creates the stores (R3) and registers its tools (R14).

Each turn prints, in this order: a usage line `Context: <percent>% (<tokens>/<max> tokens)` (plus a second line after an offload, R9), the names of the offered tools, one line per tool call with its name and displayed arguments (R20), and the final answer.

### Stores (C4a table names are binding; C4b uses the same names)
| Store | Kind | Holds |
|---|---|---|
| `CONVERSATIONAL_MEMORY` | table | one row per message |
| `TOOL_LOG_MEMORY` | table | one row per tool call |
| `SEMANTIC_MEMORY` | vector store | knowledge base passages |
| `WORKFLOW_MEMORY` | vector store | past task step sequences |
| `TOOLBOX_MEMORY` | vector store | tool definitions |
| `ENTITY_MEMORY` | vector store | people, places, systems |
| `SUMMARY_MEMORY` | vector store | summaries of shrunk conversation |

```json
{
  "$id": "conversation_row",
  "type": "object",
  "required": ["id", "thread_id", "role", "content", "timestamp"],
  "properties": {
    "id": {"type": "string", "pattern": "^[0-9A-F]{32}$", "description": "generated on insert"},
    "thread_id": {"type": "string", "minLength": 1, "maxLength": 100},
    "role": {"enum": ["user", "assistant"]},
    "content": {"type": "string", "minLength": 0},
    "timestamp": {"type": "string", "format": "date-time", "description": "set on insert, microsecond precision; ties ordered by insertion"},
    "metadata": {"type": "string", "default": "{}"},
    "created_at": {"type": "string", "format": "date-time"},
    "summary_id": {"type": ["string", "null"], "pattern": "^[0-9a-f]{8}$", "default": null, "description": "null = unsummarized"}
  }
}
```

```json
{
  "$id": "tool_log_row",
  "type": "object",
  "required": ["id", "thread_id", "tool_name", "status", "timestamp"],
  "properties": {
    "id": {"type": "string", "pattern": "^[0-9A-F]{32}$"},
    "thread_id": {"type": "string", "maxLength": 100},
    "tool_call_id": {"type": ["string", "null"], "maxLength": 200},
    "tool_name": {"type": "string", "maxLength": 200},
    "tool_args": {"type": "string", "description": "JSON text of the arguments"},
    "result": {"type": "string", "description": "full result, never truncated"},
    "result_preview": {"type": "string", "description": "first 2000 bytes of result in UTF-8, cut at a character boundary"},
    "status": {"enum": ["success", "failed"]},
    "error_message": {"type": ["string", "null"]},
    "metadata": {"type": "string", "description": "JSON text, contains {\"iteration\": n}"},
    "timestamp": {"type": "string", "format": "date-time"},
    "created_at": {"type": "string", "format": "date-time"}
  }
}
```

```json
{
  "$id": "vector_row",
  "type": "object",
  "required": ["id", "text", "metadata", "embedding"],
  "properties": {
    "id": {"type": "string"},
    "text": {"type": "string", "description": "the text that was embedded"},
    "metadata": {"type": "object"},
    "embedding": {"type": "array", "items": {"type": "number"}, "description": "C6a: 768 numbers"}
  },
  "metadata_by_store": {
    "SEMANTIC_MEMORY (seed)": ["arxiv_id", "title", "subjects", "abstract", "submission_date"],
    "SEMANTIC_MEMORY (paper chunk)": ["source=arxiv", "arxiv_id", "title", "entry_id", "published", "authors", "chunk_id", "num_chunks", "ingested_ts_utc"],
    "WORKFLOW_MEMORY": ["query", "success (boolean)", "num_steps (integer)", "timestamp"],
    "TOOLBOX_MEMORY": ["_id", "name", "description", "signature", "parameters", "return_type", "augmented (boolean)", "queries (list, augmented only)"],
    "ENTITY_MEMORY": ["name", "type (PERSON|PLACE|SYSTEM|UNKNOWN)", "description"],
    "SUMMARY_MEMORY": ["id (^[0-9a-f]{8}$)", "full_content", "summary", "description (the label)", "thread_id (when made from a thread)"]
  }
}
```

The text of each vector row: a seed paper is `title`, `subjects` and `abstract` joined by newlines, leaving out empty parts. A paper chunk is the chunk text. A workflow is `Query: <q>\nSteps:\nStep 1: <s1>\n…\nAnswer: <first 200 chars of answer>`. A tool is its searchable text (R14, R15). An entity is `<name> (<TYPE>): <description>`. A summary is `<id>: <label>`.

**Tool definition offered to the model** (one per selected tool), in the provider's function-calling format: `{"type":"function","function":{"name":…,"description":<stored description>,"parameters":{"type":"object","properties":{<param>:{"type":<json type>}},"required":[<params without default>]}}}`.

**arXiv candidate list** (output of `arxiv_search_candidates`, JSON text): an array of up to k objects `{"arxiv_id", "entry_id", "title", "authors", "published", "abstract"}`. `arxiv_id` is the part of `entry_id`'s path after `/abs/`, with slashes stripped (e.g. `http://arxiv.org/abs/2502.01234v1` → `2502.01234v1`). `abstract` is at most 2,500 characters.

**Entity extractor reply:** text containing a JSON array of `{"name", "type", "description"}`. Everything from the first `[` to the last `]` is parsed.

### Context window passed to the model (binding format)
The first model call of a turn carries two messages: a system message containing the agent system prompt (R6), and a user message laid out as:

```
# Question
<the request>

## Conversation Memory
…
## Knowledge Base Memory
…
## Workflow Memory
…
## Entity Memory
…
## Summary Memory
…
```

Each memory section has three sub-headings: `### What this memory is`, `### How you should leverage it`, and one for the retrieved items (`### Retrieved messages`, `### Retrieved passages`, `### Retrieved workflows`, `### Retrieved entities`, `### Available summaries`). The "what" and "how" texts say:
- **Conversation:** chronological, unsummarized messages from the current thread, capturing intent, constraints and commitments. Use them to keep continuity, resolve references like "the paper above", and prefer the latest user direction.
- **Knowledge base:** retrieved background passages. Ground factual claims in them, and state uncertainty when evidence is missing.
- **Workflow:** past task trajectories (query, ordered steps, outcome). Use them as patterns to adapt, not to copy blindly.
- **Entity:** named people, organisations and systems. Use them to disambiguate and keep naming consistent.
- **Summary:** compressed snapshots of older conversation. Call `expand_summary(id)` before relying on exact quotes, fine detail or chronology.

The empty states are, exactly: `(No unsummarized messages found for this thread.)`, `(No relevant knowledge base passages found.)`, `(No relevant workflows found.)`, `(No entities found.)` and `(No summaries available for thread <thread_id>.)`. The item formats are in R5 and R8.

### Model roles
| Role | Does | Course model | Request settings (course) |
|---|---|---|---|
| agent | reasons and calls tools in the loop | `gpt-5-mini` | tools passed with tool choice "auto" when any are offered |
| summarizer | writes the four-heading summary | `gpt-5` | max completion tokens 4000 |
| labeler | writes the 8–12-word summary label | `gpt-5` | max completion tokens 2000 |
| entity extractor | extracts entities as JSON | `gpt-5` | max completion tokens 2000 |
| tool describer | improves a tool description (C8a) | `gpt-5` | max completion tokens 2000 |
| query generator | writes example requests for a tool (C8a) | `gpt-5` | max completion tokens 2000 |

### Settings
| Setting | Value | Source | Change this when … |
|---|---|---|---|
| `conversation_read_limit` | 10 messages | Lesson 6 code (shared helper default) | — |
| `kb_top_k` | 3 | Lesson 6 code | — |
| `workflow_top_k` | 3, only workflows with at least 1 step | Lesson 6 code | — |
| `entity_top_k` | 5 | Lesson 6 code | — |
| `summary_list_k` | 10, scoped to the thread | Lesson 6 code | — |
| `tool_top_k` | 5 | Lesson 6 code | the course invites trying different values of k |
| `max_iterations` | 10 | Lesson 6 code | — |
| `offload_threshold_percent` | 80 (offload when strictly greater) | Lessons 5 and 6 transcripts and code | — |
| `context_limit_tokens` | 256000; 128000 for a model the program does not know | Lessons 5 and 6 code | your model's context window differs (the course keys it by model) |
| `chars_per_token` | 4 | Lesson 5 transcript and code | your model's tokens average a different size (the course: "some of them divide by two") |
| `tool_result_char_limit` | 3000 | Lesson 6 code | — |
| `tool_log_preview_bytes` | 2000 | Lesson 6 code | — |
| `summary_output_char_limit` | 6000 | Lesson 5 transcript (see D5) | — |
| `summary_retry_word_limit` | 180 | Lesson 5 code | — |
| `summary_label_words` | 8–12 | Lesson 5 code | — |
| `summary_fallback_excerpt_chars` | 500 | Lesson 5 code | — |
| `entity_input_chars` | 500; texts under 5 characters skipped | Lesson 6 code | — |
| `workflow_answer_chars` | 200 | Lesson 6 code | — |
| `step_arg_display_chars` | 50 | Lesson 6 code | — |
| `chunk_size` / `chunk_overlap` | 1500 / 200 characters | Lesson 4 code | — |
| `arxiv_candidates_k` | 5 (retriever fetches up to 8; content up to 4000 characters; abstract cut at 2500) | Lesson 4 code | — |
| `web_search_max_results` (C1c) | 5 | Lesson 4 code | — |
| `example_requests_per_tool` (C8a) | 5 | Lesson 4 code | — |
| `distance` | cosine | Lesson 3 transcript (see D2) | — |
| `db_path` | `memory.db` | addition | you want memory in a different file |
| summarizer prompt wording | four headings and rules (R10) | Lesson 5 | the course invites trying different summarization prompts |

---

## Business rules

### What must stay true (the course's pattern card — every option keeps these)
1. **Memory lives outside the model and survives the session.** What the agent learns in one turn or session is stored in persistent storage and is available to later turns and new sessions; nothing depends on the model or the process remembering it.
2. **Before the model answers, the memory relevant to the request reaches its context.**

### Rules of the recommended build
- **R1 (card item 1).** Every memory store is persistent. Anything written in one process is readable by a later process opened on the same database, and no part of the program relies on in-process state to remember a turn. → T1, T2, T3
- **R2 (card item 2).** Every turn assembles the context from the stores before the first model call. That first call carries the request under `# Question`, followed by the five memory sections, in the order shown under Contracts. → T4, T38, L4
- **R3.** On a fresh start the seven stores exist, with the names in the Stores table, and are empty. On later starts they are opened as they are, and nothing is dropped or cleared (D6). → T1, T2
- **R4 (the course's demonstrated failure: a stateless agent forgets).** A follow-up that refers to an earlier turn ("save the content of the paper") resolves the reference through stored conversation, even when the earlier turn happened in another process. The same follow-up in a thread with no history gets the "no record" reply. → T3
- **R5.** Conversation writes and reads:
  - Each turn writes the user's request (role `user`) after the context is assembled and before the first model call. It writes the final answer (role `assistant`) after the loop. Both rows carry the thread id and a timestamp.
  - A read returns the thread's unsummarized messages ordered by timestamp (ties by insertion), oldest first, and at most `conversation_read_limit` of them. These are therefore the **oldest** 10 unsummarized messages, which is the course's behaviour (see Notes for the build agent).
  - Each message is shown as `[HH:MM:SS] [<role>] <content>`.
  → T6, T7
- **R6.** The system prompt makes the agent memory-aware. It states:
  - the role: a memory-aware research assistant with tools;
  - that the user message is a partitioned context with a `# Question` section and the five named memory sections;
  - what each section is for (as under Contracts);
  - the expansion policy: when critical detail is only in Summary Memory, or is ambiguous there, call `expand_summary(summary_id)` before relying on it;
  - five operating rules: (1) start with the memory sections before using tools; (2) on conflict, prefer the current question, then the latest Conversation Memory, then Knowledge Base evidence, then older summaries and workflows; (3) use only the tools offered this turn, and as few calls as needed; (4) if memory is insufficient, say what is missing and use a tool; (5) for conversation compaction, use `summarize_and_store` with the thread id.

  → T4, T5
- **R7.** A knowledge base read returns the `kb_top_k` passages with the highest cosine similarity to the request (ties by insertion order), joined by newlines under `### Retrieved passages`. → T8, L3
- **R8.** Other reads:
  - A workflow read returns up to `workflow_top_k` of the most similar workflows that have `num_steps` > 0, separated by lines of `---`.
  - An entity read returns up to `entity_top_k` entities, each as `• <name>: <description>`.
  - A summary read returns up to `summary_list_k` of the thread's summaries. It starts with the line `Use expand_summary(id) to retrieve the detailed underlying conversation.` and a line `Scope: thread_id = <id>`, then one line per summary: `  • [ID: <id>] <label>`.

  → T9, T37
- **R9.** Context budget:
  - Estimated tokens = (number of characters in the five memory sections) ÷ `chars_per_token`, rounded down. Percent = tokens ÷ `context_limit_tokens` × 100, rounded to 1 decimal.
  - If percent > `offload_threshold_percent`, the program summarizes the thread's unsummarized messages (R10). It then replaces the Conversation Memory section with exactly: `## Conversation Memory`, `Older conversation content was summarized to reduce context size.`, `Use Summary Memory references + expand_summary(id) for full detail.` It keeps the other sections and appends the line `[Summary ID: <id>] <label>` at the end of the context.
  - The usage line is printed before the check, and again after an offload.

  → T10, T11
- **R10.** Summarizing a thread:
  - Read the thread's unsummarized messages oldest first. If there are none, report "nothing to summarize".
  - Build a transcript of lines `[YYYY-MM-DD HH:MM:SS] [<ROLE>] <content>`, with the role in upper case, and send the whole transcript to the summarizer.
  - The summarizer is asked for exactly the headings `### Technical Information`, `### Emotional Context`, `### Entities & References` and `### Action Items & Decisions`. Its rules: keep concrete details (names, dates, APIs, errors, decisions); separate confirmed facts from open questions; do not invent; be concise and useful for continuation. The stored summary is cut to `summary_output_char_limit` characters.
  - If the reply is empty, ask once more with a simpler prompt: the same headings in at most `summary_retry_word_limit` words. If that is also empty, the summary becomes `### Technical Information`, then the first 500 characters of the transcript with newlines replaced by spaces, then the other three headings, each followed by `Not available from model output.`
  - The labeler is asked for an 8–12-word label, "Return ONLY the label", specific, with a concrete signal, never generic. Quotes around the reply are stripped. If the label is empty or one of `conversation summary`, `summary`, `chat summary` or `thread summary` (ignoring case), the label becomes the first 12 words of the first summary line that does not start with `###` and has at least 4 words, after stripping surrounding `-•* ` characters; the 12 words are then stripped of surrounding ` ,.;:`. If there is no such line, it becomes `Recent thread context, decisions, and open actions`.
  - The summary id is 8 lowercase hexadecimal characters, from a random UUID. The program stores the summary row (id, full transcript, summary, label, thread id), then sets `summary_id` on exactly the rows it read.

  → T12, T13, T14, T15
- **R11 (course warning: re-summarizing already processed messages).** A message that already has a `summary_id` is never read for summarizing again and never appears in Conversation Memory again. → T12, T16
- **R12 (course warning: losing the original conversation).** `expand_summary(summary_id, thread_id=None)` returns:
  - `## Summary Context`, then the summary text (or `Summary <id> not found.`), then a blank line;
  - `## Expanded Conversations for Summary ID: <id>`, then `Total messages: <n>`, then a blank line;
  - each original message as `[YYYY-MM-DD HH:MM:SS] [<ROLE>]` with its content on the next line and a blank line after, in chronological order. When there are none, `No conversations found for summary_id: <id>`.

  → T17, T38, L4
- **R13.** `summarize_and_store(text="", thread_id=None)`:
  - With a thread id, it summarizes that thread (R10) and returns `Stored as [Summary ID: <id>] <label>`, or `No unsummarized messages found for thread <id>.`
  - Without one but with non-empty text, it summarizes the text without marking any rows and returns the same `Stored as …` form.
  - With neither, it returns ``Provide `thread_id` (preferred) or non-empty `text` to summarize.``
  - When the agent calls it without a thread id, the loop fills in the current thread id.

  → T18, T38
- **R14.** Tool registration:
  - The program registers `arxiv_search_candidates`, `fetch_and_save_paper_to_kb_db`, `get_current_time`, `expand_summary` and `summarize_and_store`.
  - A tool whose name already exists in the toolbox store is not written again, and no model call is made for it, but it can still be executed.
  - A stored tool records its name, description, signature, parameters (each with its type and default, when present), return type, whether it was improved, and (if improved) its example requests.
  - A plain tool's searchable text is `<name> <description> <signature>`.

  → T19, T21
- **R15.** An improved tool (C8a list):
  - The tool describer receives the original description and the function's source. It is asked for a one-line summary, step-by-step behaviour, when an agent should call it, and caveats, returning only the description.
  - The query generator is asked for 5 varied example requests as a JSON array of strings. If the reply is not a JSON array, the whole reply becomes a single example.
  - The stored description is the describer's reply. The searchable text is `<name> <improved description> <signature> <examples joined by spaces>` (D4).

  → T20
- **R16.** Tool selection returns the `tool_top_k` tools most similar to the request, with duplicate names dropped, as function definitions. Parameter types map from the Python annotation: `str`→`string`, `int`→`integer`, `float`→`number`, `bool`→`boolean`, and anything else or unannotated→`string`. A parameter is required exactly when it has no default. → T21, T22
- **R17.** The agent loop runs for at most `max_iterations` model calls:
  - If the reply has tool calls, the program appends the reply, runs each call in order, appends each result as a tool message, and calls the model again.
  - A reply without tool calls is the final answer.
  - If the limit is reached without one, the answer is `I was unable to complete the request within the allowed iterations.`

  → T23, T24, T38, L1
- **R18.** Tool execution:
  - A tool name not in the registry returns `Error: Tool '<name>' not found` as the tool result. It is logged with status `success` and recorded as a successful step, which is the course's behaviour.
  - A tool that raises returns `Error: <message>` as the result. It is logged with status `failed` and the error message, and recorded as a failed step.
  - A tool that returns nothing returns `Done`.

  → T25, T26
- **R19 (course warning: tool output bloats the context).** Every tool call writes a tool-log row with the full result, the preview, its status, the error, `{"iteration": n}` and the provider's tool-call id. The model receives the result unchanged when it is at most `tool_result_char_limit` characters. Otherwise it receives the first 3000 characters followed by `\n\n[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <id>]`. → T27
- **R20.** Write-back:
  - Each tool call adds a step `<name>(<args>) → success|failed`. `<args>` is the arguments rendered as a Python dict, e.g. `{'query': 'MemoryLane'}`, with each string value over 50 characters cut to 50 and followed by `...`.
  - After the loop, if there was at least one step, a workflow row is written: text as under Contracts, `success` true, `num_steps`, and a timestamp. `success` is true even when the iteration limit was hit, which is the course's behaviour.

  → T28
- **R21.** Entities:
  - The program extracts entities from the request (before the loop) and from the final answer (after it).
  - A text of fewer than 5 characters, after trimming, yields none. Only its first 500 characters are sent, with the request to return a JSON array of `{"name","type":"PERSON|PLACE|SYSTEM","description"}`, or `[]` when there are none.
  - Items without a name are dropped, and a missing type becomes `UNKNOWN`. Each entity is stored as its own row.
  - Any extraction error is ignored and stores nothing.

  → T29
- **R22.** Knowledge tools (C1a):
  - `arxiv_search_candidates(query, k=5)` returns the candidate list (Contracts).
  - `fetch_and_save_paper_to_kb_db(arxiv_id, chunk_size=1500, chunk_overlap=200)` loads the full text of one paper. It splits the text at paragraph breaks, then line breaks, then spaces, then characters, merging pieces up to `chunk_size` and carrying over up to `chunk_overlap` characters of trailing pieces. It stores every chunk with the paper-chunk metadata and returns `Saved arXiv <id> to SEMANTIC_MEMORY: <n> chunks (title: <title>).`
  - If no document is found, it returns `No documents found for arXiv id: <id>`. If the text is empty, it returns `Loaded arXiv <id> but extracted empty text (PDF parsing issue).`

  → T30, T31, T32, L2
- **R23.** Seeding writes one knowledge-base row per paper record that has at least one of title, abstract and subjects (after trimming), with the seed metadata. Other records are skipped. → T33
- **R24.** `get_current_time(detailed=False)` returns the local time as `YYYY-MM-DD HH:MM:SS`, or with `.ffffff` microseconds appended when `detailed` is true. → T34
- **R25.** Without `--scripted`, `chat` and `ask` check for the model key before registering tools. If it is missing, they print `OPENAI_API_KEY is not set` and exit with code 2. → T35
- **R26.** Model requests follow the Model roles table: the completion caps per role, and tools with tool choice "auto" on agent calls that offer tools. No temperature is set. → T36

---

## Tests

### Sample data (in `tests/sample_data/`; all facts written for this spec)

**S1 `papers.jsonl`** — five paper records, one JSON object per line, with fields `arxiv_id`, `title`, `subjects`, `abstract` and `submission_date`:
1. `2501.10001` · "Tide Gauges Read by Drones" · `physics.ao-ph` · "Small drones photograph harbor tide gauges at dawn and a vision model reads the water level to within two centimeters." · 2025-01-14
2. `2501.10002` · "Sintering Lunar Regolith with Microwave Arrays" · `astro-ph.IM` · "Microwave arrays heat lunar regolith simulant into bricks strong enough for landing pads, using forty percent less energy than lasers." · 2025-01-15
3. `2501.10003` · "Sparse Attention for Genome Reads" · `q-bio.GN` · "A sparse attention kernel aligns long genome reads on a laptop GPU in under an hour." · 2025-01-16
4. `2501.10004` · "Listening to Coral Reefs at Night" · `q-bio.PE` · "Hydrophones logged reef sounds for ninety nights; snapping shrimp activity tracked coral health better than water temperature." · 2025-01-17
5. `2501.10005` · title "" · subjects "" · abstract "" · 2025-01-18 (must be skipped)

**S2 `research_chat.json`** — a 12-message conversation, a list of `[role, content]` pairs in this order:
1. user: "I'm starting a thesis on reef acoustics and need a reading plan."
2. assistant: "Start with hydrophone basics, then night-time reef soundscapes, then health indicators."
3. user: "My advisor is Dr. Lena Ortiz at Coastal University."
4. assistant: "Noted: your advisor is Dr. Lena Ortiz at Coastal University."
5. user: "I prefer short summaries with bullet points."
6. assistant: "Understood - I will keep summaries short and use bullet points."
7. user: "Which recorder should I use for ninety nights?"
8. assistant: "A low-power recorder with a 96 kHz sample rate and a 1 TB card covers ninety nights."
9. user: "I'm worried the batteries will die halfway."
10. assistant: "Plan a battery swap on night 45 and log the swap time."
11. user: "Great, that makes me feel better."
12. assistant: "Next steps: email Dr. Lena Ortiz, then draft the methods chapter by Friday."

**S3 `sample_tools.json`** — eight tool definitions (name; description; parameters as name:type[=default]), registered **plain** in the tests that use them:
1. `convert_temperature`; "Convert a temperature between celsius and fahrenheit."; value:float, to_unit:str
2. `get_weather_forecast`; "Return tomorrow's forecast for a city."; city:str, days:int=1
3. `search_flights`; "Find flights between two airports on a date."; origin:str, destination:str, date:str
4. `translate_text`; "Translate text into another language."; text:str, target_language:str
5. `send_email`; "Send an email message to a recipient."; to:str, subject:str, body:str
6. `calculate_mortgage`; "Compute a monthly mortgage payment."; principal:float, rate:float, years:int
7. `lookup_dictionary`; "Look up the definition of an English word."; word:str
8. `book_restaurant`; "Reserve a table at a restaurant."; name:str, time:str, party_size:int=2

Plus three test-only tools, registered plain by the tests that need them: `always_fails()` raises an error with message `boom`; `big_report(title: str)` returns 5,000 `x` characters; `accent_report()` returns 1,500 `é` characters.

**S4 `paper_source.json` — scripted paper source (stand-in for arXiv, offline tests only):**
- Search: a query containing `memorylane` (ignoring case) returns two results:
  - `entry_id` `http://arxiv.org/abs/2502.01234v1`, title "MemoryLane: Paging Context for Agents", authors "Ada Okafor, Ben Liu", published `2025-02-03`, content "MemoryLane pages old context out of the prompt into a store and pages it back on demand."
  - `entry_id` `http://arxiv.org/abs/2502.04321v2`, title "Lanes of Memory in Sparse Transformers", authors "Chen Wu", published `2025-02-10`, content "Sparse transformers route tokens through memory lanes."
- Search: a query containing `survey` returns seven results, `entry_id` `http://arxiv.org/abs/2503.0000Nv1` for N = 1…7, title "Agent Survey Part N", authors "Survey Team", published `2025-03-0N`, content 3,000 `s` characters.
- Search: any other query returns no results.
- Full text: `2502.01234v1` has title "MemoryLane: Paging Context for Agents", entry_id as above, published `2025-02-03` and authors "Ada Okafor, Ben Liu". Its text is three paragraphs joined by a blank line (`\n\n`). Each paragraph is its opening sentence followed by the sentence " Pages move between prompt and store." repeated, cut to exactly 1,000 characters. The openings are:
  - P1: "Key takeaways of the MemoryLane paper: paging old context to a store keeps prompts short, and a page table records where each piece went."
  - P2: "Method: the agent writes each evicted turn to a lane with a timestamp."
  - P3: "Results: on long chats, answers stayed correct while prompts shrank by half."
- Full text: `2502.09999v1` is found but has empty text.
- Full text: any other id finds no document.

**S5 — scripted model (stand-in for every model role, offline tests only).** The program tells it which role is calling. It records every request it receives (messages, tools, settings). "Question" means the text under `# Question` in the user message. "After a tool" means the last message is a tool result. Agent rules, first match wins:

| # | Question | Reply |
|---|---|---|
| A1 | "Can you get me the paper MemoryLane" | not after a tool: call `arxiv_search_candidates` with `{"query": "MemoryLane"}`; after a tool: final "I found 'MemoryLane: Paging Context for Agents' (arXiv 2502.01234v1) by Ada Okafor and Ben Liu." |
| A2 | "Can you save the content of the paper" | if the Conversation Memory section contains `2502.01234v1`: not after a tool, call `fetch_and_save_paper_to_kb_db` with `{"arxiv_id": "2502.01234v1"}`; after a tool, final "Saved the MemoryLane paper to your knowledge base." Otherwise: final "Which paper do you mean? I have no record of an earlier paper in this conversation." |
| A3 | "What are the main key takeaways from the paper" | if the Knowledge Base Memory section contains "Key takeaways of the MemoryLane paper": final "Takeaways: MemoryLane keeps prompts short by paging old context to a store, and a page table records where each piece went." Otherwise: final "I don't have that paper's content yet." |
| A4 | "Summarize the conversation so far using your tool" | not after a tool: call `summarize_and_store` with `{}`; after a tool: final "Done - the conversation so far is stored as a summary." |
| A5 | "What was my first question?" | not after a tool and the context contains `[ID: `: call `expand_summary` with `{"summary_id": <the 8 characters after the first "[ID: ">}`; after a tool whose result contains "Can you get me the paper MemoryLane": final "Your first question was: Can you get me the paper MemoryLane". Otherwise: final "I can't find your first question." |
| A6 | "loop forever" | always call `get_current_time` with `{}` |
| A7 | "use a missing tool" | not after a tool: call `no_such_tool` with `{}`; after: final "Tool missing." |
| A8 | "trigger a failing tool" | not after a tool: call `always_fails` with `{}`; after: final "It failed." |
| A9 | "big output please" | not after a tool: call `big_report` with `{"title": <60 "T" characters>}`; after: final of 300 `R` characters |
| A10 | "accent output please" | not after a tool: call `accent_report` with `{}`; after: final "Accents done." |
| A0 | anything else | final "OK." |

Other roles:
- **Summarizer.** Mode `normal` (the default) returns:

  ```
  ### Technical Information
  The user asked for the MemoryLane paper (arXiv 2502.01234v1); it was found, saved to the knowledge base, and its takeaways were discussed.
  ### Emotional Context
  Neutral and focused.
  ### Entities & References
  MemoryLane; Ada Okafor; Ben Liu.
  ### Action Items & Decisions
  None open.
  ```

  Mode `long` returns 7,000 `L` characters. Mode `empty` returns "" to both attempts.
- **Labeler.** Mode `normal` returns `MemoryLane paper found, saved, and its takeaways discussed`. Mode `generic` returns `"Conversation summary"`, quotes included.
- **Entity extractor.** If the text contains "Ada Okafor", it returns `[{"name": "Ada Okafor", "type": "PERSON", "description": "co-author of MemoryLane"}]`. Else, if the text contains "MemoryLane", it returns `[{"name": "MemoryLane", "type": "SYSTEM", "description": "context paging method"}]`. Otherwise it returns `[]`.
- **Tool describer.** For `get_weather_forecast` it returns "Returns a weather outlook for a city. Call this when the user asks about rain, sun or wind." For any other tool it returns "AUGMENTED: " followed by the original description.
- **Query generator.** For `get_weather_forecast` it returns `["will it rain tomorrow in Oslo", "is it sunny this weekend", "wind speed in Lisbon tomorrow", "do I need an umbrella", "forecast for Paris"]`. In mode `garbled` it returns `not json`. For any other tool it returns a JSON array of the 5 strings `<tool name> example 1` … `example 5`.

**S6 — word-overlap embedder (stand-in for the embedding model; offline tests and option C6c).**
- A text becomes the counts of its tokens. Tokens are the maximal runs of `[a-z0-9]` in the lower-cased text, minus these stopwords: a, an, and, are, as, at, be, by, can, do, for, from, get, how, i, in, is, it, me, my, of, on, or, so, that, the, this, to, was, what, with, you, your.
- Similarity is the cosine of two count vectors, and 0 if either is empty.
- Any fixed-length encoding is acceptable only if no asserted outcome changes.

**S7 `demo_turns.json`** — thread `t-demo`, five requests in order: (1) "Can you get me the paper MemoryLane" (2) "Can you save the content of the paper" (3) "What are the main key takeaways from the paper" (4) "Summarize the conversation so far using your tool" (5) "What was my first question?" It also has the planted stateless case: thread `t-fresh` with request (2) alone.

Unless a test says otherwise, every test uses a fresh database file, S5 in normal modes, S6, S4, and the five recommended tools with C8a improvement.

### Test table
| ID | Rules | Given | When | Then |
|---|---|---|---|---|
| T1 | R1, R3 | no database file | the program starts | the seven stores exist with the names in the Stores table, and each has 0 rows except `TOOLBOX_MEMORY`, which has 5 |
| T2 | R1, R3 | instance A writes S2 message 1 to thread `t-chat`, then closes | instance B opens the same file and reads `t-chat` | B's Conversation Memory contains "I'm starting a thesis on reef acoustics and need a reading plan."; `TOOLBOX_MEMORY` still has exactly 5 rows |
| T3 | R1, R4 | — | three separate processes run `ask --scripted`: (a) `--thread t-demo "Can you get me the paper MemoryLane"`, (b) `--thread t-demo "Can you save the content of the paper"`, (c) `--thread t-fresh "Can you save the content of the paper"` | `memory.db` is created in the (temporary) working directory and shared by all three; (b) prints a call to `fetch_and_save_paper_to_kb_db` and the answer "Saved the MemoryLane paper to your knowledge base."; (c) prints "Which paper do you mean? I have no record of an earlier paper in this conversation." and no tool call |
| T4 | R2, R6 | S1 seeded | `call_agent("how do you heat lunar regolith", thread "t-new")` | the first agent request has 2 messages: system (the R6 prompt) and user, whose content starts `# Question\nhow do you heat lunar regolith\n\n## Conversation Memory`; the headings appear in the order Conversation, Knowledge Base, Workflow, Entity, Summary; Conversation shows `(No unsummarized messages found for this thread.)`; Summary shows `(No summaries available for thread t-new.)`; answer "OK." |
| T5 | R6 | — | the system prompt is read | it contains `## Conversation Memory`, `## Knowledge Base Memory`, `## Workflow Memory`, `## Entity Memory`, `## Summary Memory`, `expand_summary` and `summarize_and_store` |
| T6 | R5 | T4 has run | conversation rows for `t-new` are listed | exactly 2 rows in order: (user, "how do you heat lunar regolith"), (assistant, "OK."); the turn's own first agent request did not contain the request inside Conversation Memory |
| T7 | R5 | S2 written in order to `t-chat` | Conversation Memory is read for `t-chat` | exactly 10 lines, the first `[hh:mm:ss] [user] I'm starting a thesis on reef acoustics and need a reading plan.` and the last ending `Plan a battery swap on night 45 and log the swap time.`; messages 11 and 12 absent |
| T8 | R7 | S1 seeded | Knowledge Base Memory is read for "how do you heat lunar regolith" | exactly 3 passages, in the order S1-2, S1-1, S1-3 (S1-2 is the only one sharing words; the rest tie at 0 and come in insertion order); S1-4 absent |
| T9 | R8 | workflows written directly: one with 0 steps (query "zero"), one with 2 steps (query "two"); six entities E1…E6 written directly | workflow and entity reads for "x" | the Workflow section contains `Query: two` and not `Query: zero`; the Entity section has exactly 5 lines, `• E1: …` through `• E5: …` |
| T10 | R9 | S2 in `t-chat`; `context_limit_tokens` set to 100 | `call_agent("Status?", "t-chat")` | 12 rows get the same new summary id; the first agent request contains `Older conversation content was summarized to reduce context size.`, does not contain "reading plan", and ends with `[Summary ID: <id>] MemoryLane paper found, saved, and its takeaways discussed`; two usage lines are printed, both showing `/100 tokens`; after the turn, `t-chat`'s only unsummarized rows are "Status?" (user) and "OK." (assistant) |
| T11 | R9 | S2 in `t-chat`; default settings | `call_agent("Status?", "t-chat")`; separately, the usage check on a 400-character and a 404-character memory text with the limit set to 125 | no summary is created, the request contains "reading plan", and the usage line shows `/256000 tokens`; 400 chars → 100 tokens, 80.0%, no offload; 404 chars → 101 tokens, 80.8%, offload |
| T12 | R10, R11 | S2 in `t-chat` | the thread is summarized, then summarized again | the first run returns an id matching `^[0-9a-f]{8}$` and 12 summarized messages; all 12 rows carry that id; the summary row has `thread_id` `t-chat`, `full_content` equal to the 12-line transcript, and the normal summary text; Conversation Memory then shows `(No unsummarized messages found for this thread.)`; the second run returns "nothing to summarize" |
| T13 | R10 | S2 in `t-chat` plus a 7,000-character user message of `q`, then the user message "final marker message"; summarizer mode `long` | the thread is summarized | the summarizer request contains "final marker message" (the whole transcript was sent); the stored summary is exactly 6,000 characters |
| T14 | R10 | S2 in `t-chat`; summarizer mode `empty` | the thread is summarized | the summarizer receives 2 requests, the second containing `<= 180 words`; the stored summary starts `### Technical Information\n[`, contains `[USER] I'm starting a thesis on reef acoustics`, has an excerpt line of at most 500 characters with no newline inside it, and ends with `### Action Items & Decisions\nNot available from model output.` |
| T15 | R10 | S2 in `t-chat`; labeler mode `generic` | the thread is summarized | the labeler request contains `8-12 word`; the stored label is `The user asked for the MemoryLane paper (arXiv 2502.01234v1); it was found` |
| T16 | R11 | T12's first summary done; then messages "One more thing." (user) and "Sure." (assistant) are written | the thread is summarized | exactly 2 rows are marked, with a new id different from the first; the 12 earlier rows keep the first id |
| T17 | R12 | T12's first summary done (id X) | `expand_summary(X)`; `expand_summary("zzzzzzzz")` | the first result contains `## Summary Context`, the normal summary, `## Expanded Conversations for Summary ID: X`, `Total messages: 12`, and the 12 messages in S2 order, each under a `[YYYY-MM-DD HH:MM:SS] [USER]` or `[ASSISTANT]` line; the second contains `Summary zzzzzzzz not found.` and `No conversations found for summary_id: zzzzzzzz` |
| T18 | R13 | S2 in `t-chat` | `summarize_and_store(text="Notes about reef sounds.")`; `summarize_and_store()`; `summarize_and_store(thread_id="t-empty")` | the first returns `Stored as [Summary ID: <8 hex>] MemoryLane paper found, saved, and its takeaways discussed` and marks no row of `t-chat`; the second returns ``Provide `thread_id` (preferred) or non-empty `text` to summarize.``; the third returns `No unsummarized messages found for thread t-empty.` |
| T19 | R14 | `convert_temperature` already registered (plain) | it is registered again, once plain and once with improvement | `TOOLBOX_MEMORY` holds 1 row named `convert_temperature`; the scripted model received no request during the second registration; the tool can still be executed |
| T20 | R15 | an empty toolbox | `convert_temperature` is registered plain, then `get_weather_forecast` with improvement; tool selection runs for "will it rain" with k = 1; separately, with query generator mode `garbled`, `translate_text` is registered with improvement | the selection returns `get_weather_forecast`; its stored description is "Returns a weather outlook for a city. Call this when the user asks about rain, sun or wind."; its stored examples are the 5 S5 strings; the describer and query generator were each called once for it, and the query generator request asks for 5; `translate_text`'s examples are `["not json"]` |
| T21 | R14, R16 | the eight S3 tools registered plain, in order | tool selection for "convert 30 celsius to fahrenheit" with k = 1 | exactly one definition, `convert_temperature`, whose parameters are `value` `number` and `to_unit` `string`, both required; and selection with k = 8 shows `get_weather_forecast` with `days` `integer`, not required |
| T22 | R16 | the 5 program tools plus the 8 S3 tools | `call_agent("Status?", "t-x")` | the agent request carries exactly 5 tool definitions with distinct names |
| T23 | R17 | the 5 program tools | `call_agent("Can you get me the paper MemoryLane", "t-demo")` | the agent receives 2 requests; the second ends with a tool message containing `"arxiv_id": "2502.01234v1"`; answer equals A1's final text |
| T24 | R17 | — | `call_agent("loop forever", "t-loop")` | exactly 10 agent requests; answer `I was unable to complete the request within the allowed iterations.`; 10 tool-log rows; one workflow row with `num_steps` 10 and `success` true |
| T25 | R18 | — | `call_agent("use a missing tool", "t-m")` | the tool message is `Error: Tool 'no_such_tool' not found`; the tool-log row has status `success`; the workflow step is `no_such_tool({}) → success` |
| T26 | R18 | `always_fails` registered | `call_agent("trigger a failing tool", "t-f")` | the tool message is `Error: boom`; the tool-log row has status `failed` and error_message `boom`; the step ends `→ failed`; answer "It failed." |
| T27 | R19 | `big_report` and `accent_report` registered | `call_agent("big output please", "t-b")`; `call_agent("accent output please", "t-a")` | the `big_report` tool message is 3,000 `x` followed by `\n\n[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <id>]`, where `<id>` is that log row's id; its log row has a 5,000-character result and a 2,000-character preview; the `accent_report` log row has a preview of 1,000 `é` characters (2,000 bytes), and its tool message is the full 1,500 characters |
| T28 | R20 | T27's first call has run | the `t-b` workflow row is read | its text is `Query: big output please\nSteps:\nStep 1: big_report({'title': '<50 T>...'}) → success\nAnswer: <200 R>`; metadata `num_steps` 1, `success` true |
| T29 | R21 | — | T23's call has run; separately, entity extraction runs on "Hi" and on a 600-character text that starts with "MemoryLane" | `ENTITY_MEMORY` holds 2 rows from T23, `MemoryLane (SYSTEM): context paging method` and `Ada Okafor (PERSON): co-author of MemoryLane`; "Hi" sends no extractor request; the 600-character text's request contains only its first 500 characters |
| T30 | R22 | S4 | `arxiv_search_candidates("agent survey")`; `arxiv_search_candidates("nothing here")` | the first returns a JSON array of 5 items, the first with `arxiv_id` `2503.00001v1` and a 2,500-character abstract; the second returns `[]` |
| T31 | R22 | S4 | `fetch_and_save_paper_to_kb_db("2502.01234v1")` | it returns `Saved arXiv 2502.01234v1 to SEMANTIC_MEMORY: 3 chunks (title: MemoryLane: Paging Context for Agents).`; 3 new knowledge rows, each equal to one paragraph (ignoring surrounding whitespace), with `chunk_id` 0, 1, 2, `num_chunks` 3, `source` `arxiv` and `authors` "Ada Okafor, Ben Liu" |
| T32 | R22 | S4 | fetch `2502.09999v1`; fetch `9999.00000v1` | `Loaded arXiv 2502.09999v1 but extracted empty text (PDF parsing issue).`; `No documents found for arXiv id: 9999.00000v1`; no rows added |
| T33 | R23 | S1 | `seed --papers tests/sample_data/papers.jsonl` | it prints `Seeded 4 records`; S1-2's row text is "Sintering Lunar Regolith with Microwave Arrays\nastro-ph.IM\nMicrowave arrays heat lunar regolith simulant into bricks strong enough for landing pads, using forty percent less energy than lasers."; no row has `arxiv_id` `2501.10005` |
| T34 | R24 | — | `get_current_time()`; `get_current_time(detailed=True)` | they match `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$` and `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}$` |
| T35 | R25 | `OPENAI_API_KEY` unset | `ask --thread t "hi"` without `--scripted` | it prints `OPENAI_API_KEY is not set` and exits with code 2; no tool is written to `TOOLBOX_MEMORY` |
| T36 | R26 | S2 in `t-chat` | the thread is summarized; T23's call runs | the summarizer request has max completion tokens 4000 and the labeler request 2000; the entity, describer and query-generator requests each have 2000; every agent request with tools has tool choice "auto"; no request sets a temperature |
| T37 | R8 | 11 summaries written directly for thread `t-s` and 1 for thread `t-other` | Summary Memory is read for `t-s` | it contains `Scope: thread_id = t-s` and exactly 10 `  • [ID: ` lines, none of them the `t-other` summary |
| T38 | R2, R12, R13, R17 | S1 seeded | the five S7 turns run in thread `t-demo` | turn 1: 5 tools offered, one `arxiv_search_candidates` call, A1's answer. Turn 2: one fetch call; `SEMANTIC_MEMORY` has 7 rows. Turn 3: 1 agent request, no tool call, A3's "Takeaways: …" answer. Turn 4: `summarize_and_store` runs with `thread_id` `t-demo` filled in by the loop; 7 rows are marked. Turn 5: the first agent request's Conversation Memory holds exactly 1 message ("Done - the conversation so far is stored as a summary."), and Summary Memory has one `[ID: <id>] MemoryLane paper found, saved, and its takeaways discussed` line; the agent calls `expand_summary` with that id, whose result contains `Total messages: 7`; the answer is "Your first question was: Can you get me the paper MemoryLane". `WORKFLOW_MEMORY` has 4 rows. |
| L1 `live` | R17 | a real model key | `ask --thread live1 "Say hello in five words"` | a non-empty answer within 10 iterations; 2 conversation rows |
| L2 `live` | R22 | network access | `arxiv_search_candidates("attention transformer")` | 1–5 candidates, each `arxiv_id` matching `^\d{4}\.\d{4,5}v\d+$` |
| L3 `live` | R7 | the course's embedding model (download on first run) | embed "heating lunar soil into bricks", S1-2's text and S1-4's text | each vector has 768 numbers; the query's cosine with S1-2 is higher than with S1-4 |
| L4 `live` | R2, R12 | a real model key and network access | five turns in thread `live4`: "Can you get me the paper Attention Is All You Need", "Can you save the content of the paper", "What are the main key takeaways from the paper", "Summarize the conversation so far using your tool", "What was my first question?" | turn 1 calls `arxiv_search_candidates`; turn 4 calls `summarize_and_store`; turn 5's first request has a summary line; turn 5 calls `expand_summary` and its answer contains "Attention" |

**Replay notes** (checked against S1–S7 with every default in force):
- **T8:** the query tokens are heat, lunar and regolith. Only S1-2 contains any of them.
- **T21:** convert, celsius and fahrenheit appear only in `convert_temperature`.
- **T20:** with improvement, "rain" and "will" appear only in the weather tool's text. Without it, both tools score 0, and insertion order would pick `convert_temperature`.
- **T38 turn 3:** the query tokens are main, key, takeaways and paper. Only chunk P1 shares any of them (key, takeaways, paper), so P1 is in the top 3.
- **T38 turn 4:** the 6 rows from turns 1–3 plus turn 4's request make 7.
- **T38 turn 5:** only turn 4's answer is unsummarized when the context is built.
- **T10:** the boilerplate of the five sections alone exceeds 320 characters, i.e. more than 80 tokens.

---

## Standing permissions
- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in, both in code and in printouts; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has data in its stores; anything that sends data to a third party beyond the chosen model provider and knowledge source.
- **Never:** invent provenance (never call a stand-in or an addition the course's); answer when the program should say it does not know; change sample data to make a test pass; commit secrets or a `.env` file.

## Test plan
1. `python -m pytest tests -m "not live"` runs T1–T38 offline with the stand-ins.
2. `python -m pytest tests -m live` runs L1–L4. Each live test skips with a clear reason when its key, network or model download is unavailable.
3. Report one result per test with evidence: the test output line, plus file paths for anything written. "Should pass" counts as not run.
4. For every chosen option that is not recommended, write a test from its "what to check" sentence, run it, and report it with the others. Drop or adjust the recommended tests for parts the chosen options remove (e.g. C5b removes the knowledge-base, workflow, entity and toolbox tests), and say which.
5. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.
6. Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

---

## Background notes (for the build agent)

### The program
A tool-using agent whose memory lives outside the model, so it carries on across turns and sessions. Its stages:
`store → embed → register tools → assemble context → check budget → select tools → reason and act → write back`
- **store:** seven stores in a database, because memory must outlive the model call and the process (card item 1).
- **embed:** text becomes vectors, so memory can be found by meaning.
- **register tools:** tools are stored as searchable memory, so only the relevant ones reach the prompt.
- **assemble context:** relevant memory is read into labelled sections before the model is called (card item 2). The labels make the model aware of what each memory is for.
- **check budget:** the context is measured, and old conversation is shrunk into an expandable summary before it overflows.
- **select tools:** the top 5 tools for this request.
- **reason and act:** the model answers or calls tools in a bounded loop. Raw tool output goes to the tool log, and only a bounded copy goes back to the model.
- **write back:** the request, answer, steps taken and names mentioned are saved for later turns.

### Notes for the build agent on course behaviour kept as-is
- **Oldest 10, not newest 10.** The conversation read takes the first 10 unsummarized messages by time, so in a thread with more than 10 unsummarized messages the newest ones are not shown. This looks like a bug, but the course does it, and the instructor only says conversation memory is "time-ordered". Kept, and tested in T7. Summaries (manual or automatic) are what clears the backlog.
- **Usage counts only the memory sections.** The context measure ignores the system prompt, the question and the tool definitions.
- **Workflow `success` is always true**, even when the loop hit its iteration limit.
- **Missing tools are logged as successes.** A call to an unknown tool is logged and stepped as `success`, with an error text as its result.
- **Entities are never merged.** Repeated mentions add new rows.
- **Agent-triggered summarizing marks the current request too.** It runs after the current request was written, so that request is included (7 messages in the demo).

### Failures
- **Demonstrated: the stateless agent forgets (Lesson 2, slides and transcript).**
  - *What you see:* after recommending restaurants, the agent answers "book the first one" with "I have no recollection … please provide a list".
  - *Why it happens:* nothing from earlier turns is stored or loaded.
  - *How the spec prevents it:* every turn is stored and the thread's conversation is loaded before the model is called (R4, R5, R2). The planted sample is S7's `t-fresh` case, and T3 checks it.
- **Warned: context overflow.** The Lesson 5 code notes say "Context overflow crashes the agent", and "agents lose important historical context or fail due to token limits". R9 enforces the budget check, tested by T10 and T11.
- **Warned: re-summarizing processed messages** (Lesson 5 code notes). R11, tested by T12 and T16.
- **Warned: summaries lose important details; the original conversation cannot be reached** (Lesson 5 code notes). The four headings and expandable originals answer this. R10 and R12, tested by T12–T17.
- **Warned: empty model output during summarizing** (Lesson 5 transcript: "a fallback mechanism … so that if the first output is empty, we will never completely lose all the context"). R10, tested by T14.
- **Warned: too many tools in the prompt** cause context bloat, confusion, worse tool selection, and more latency and cost (Lesson 4 transcript and slides). R16, tested by T22.
- **Warned: large tool outputs bloat the context** (Lesson 6 code notes). R19, tested by T27.
- **Warned: the agent "forgets to save"** (Lesson 3 code notes on deterministic storage). R5 and R20, tested by T6 and T28.
- **Shown in code:** an empty PDF text or a missing paper returns a message instead of failing (R22, T32). A loop that never finishes ends with a fixed message (R17, T24).

### Why the questions and settings are what they are
- **C1:** the course's example is a research assistant over arXiv papers (Lessons 3–6). The course built web search with store-to-knowledge-base in Lesson 4 ("the agent learns from its searches") but did not register it in the final Lesson 6 agent, so it is an option. A learner's own documents are the "own version" path.
- **C2, C3:** context subjects. The course used OpenAI and ran in notebook cells, and a notebook is never offered.
- **C4:** the course's Oracle database needs container and admin setup, so the recommended build uses a stand-in (4.4). The course calls the database the "agent memory core".
- **C5:** Lesson 2 shows a "naive memory-augmented agent" with conversation memory only working ("reliability in continuation of interaction"), then argues for going beyond it. That argument is a cost, not a failure.
- **C6:** the course's embedder is a local download with no key; this spec judges it under the 3 GB line (an addition: the course states no size), so it stays recommended (4.4). The hosted option and the stand-in are lighter paths.
- **C7:** the course argues the toolbox at scale. Lesson 4 also registered toolbox search as an agent tool ("both a programmatic operation and an agent-callable skill"), which the final agent dropped, so it is C7c.
- **C8:** "this is a great idea, but it might not be enough", so the course added augmentation for "higher recall" and "better separability". The per-tool split is the course's.
- **C9:** Lesson 3 names lexical, vector, graph and hybrid retrieval. Its code defined a hybrid-search setup for the knowledge base but never used it.
- **C10:** reranking appears in the Lesson 2 RAG pipeline, and the Lesson 3 code notes say "Deep retrieval, reranking … cost tokens/time".
- **C11:** the Lesson 3 code notes give the deterministic case (context bootstrapping, the "can't look up what it doesn't know exists" problem, predictability, reliability, completeness) and the agent-triggered case (relevance, cost and latency, higher-quality memory). The final loop is C11a.
- **C12:** Lesson 5 contrasts summarization ("always a lossy technique") with compaction (an ID plus a description in the database, expanded on demand). The final code keeps both the summary and the originals.

**Subjects that are not questions:**
- **Store kept in memory only, or a stateless agent.** Fails test 1, because it breaks card item 1. The stateless agent also fails test 2: the course shows it failing.
- **No context-size check or shrinking.** Fails test 2: the course warns that context overflow crashes the agent. It also fails test 3: in short threads the check never fires, so removing it is never the better choice.
- **No tool log.** Fails test 3: no situation found where losing the full tool output is the better choice; the truncation only applies above 3,000 characters.
- **Unlabelled context, or no memory description in the system prompt.** Fails test 3: no situation found where an unlabelled context serves the learner better. It stays a rule (R6).
- **Persona memory.** Not a 5.2 candidate. It appears only in two slide tables (with `write_persona`/`read_persona`), with no behaviour described; it is not in the final program, and the pattern card offers nothing from other lessons (section 3.3).
- **Semantic cache.** Not a 5.2 candidate. It is named in the Lesson 2 memory taxonomy, never built, and not part of the final program (section 3.3).
- **Graph-traversal retrieval.** Fails test 3: no store in this program holds relationships, so no situation fits.
- **Lexical-only retrieval.** Fails test 3: every situation is already served by C9b or C6c.
- **Fine-tuning embedding models.** Not a 5.2 candidate. It is named only as part of the "memory engineering" disciplines, not as an alternative for any stage.
- **Settings, not questions (4.3):** distance metric, index type, every k, iteration limit, threshold, chunk sizes, prompt wording.

**Where the picked values came from (4.2):**
- **Distance:** cosine. The Lesson 3 transcript says "in this case is going to be cosine", and the Lesson 3 and 4 code agree. The Lesson 5 and 6 code use Euclidean distance, and the Lesson 3 code notes list Euclidean in passing. Rule 1 picked cosine.
- **Tool k:** 5. The final Lesson 6 loop uses 5. The shared helper's default is 3, the Lesson 4 check used 1, and the Lesson 4 tool docstring says "default: 5". Rule 2 picked 5.
- **Summarizer model:** the Lesson 5 notebook used `gpt-5-mini`; the shared helper used by the final agent uses `gpt-5`. Rule 2 picked `gpt-5` as the course fact.
- **Summary 6,000-character limit:** the instructor describes it as the limit on the summary output; the code applied it to the input. Rule 1 picked the output (D5).
- **Tool searchable text:** the instructor and the code notes say the improved text is embedded; the code embedded the original. 4.1 says to follow the instructor (D4).
- **Which operations are automatic:** the Lesson 3 table marks reading summaries and writing entities as agent-triggered, and toolbox reading as both. The final loop does all three automatically and gives no toolbox-search tool. Rule 2 picked the final loop.
- **Vector index:** the Lesson 3 code notes say HNSW; the code creates IVF ("neighbor partitions", target accuracy 95), with a comment that it avoids errors on the free database edition. The final Lesson 6 notebook creates no index. This applies only to C4b, which uses IVF, the only index the course's code actually creates.
- **Knowledge base contents in Lesson 6:** the transcript says papers were "ingested earlier on", but the Lesson 6 notebook drops all tables first and does not seed them. The recommended build seeds (D3).
- **Recommended tool limit:** the slides say "~5–20 in practice" and the Lesson 4 code notes say "often 10-20 max". Slides that disagree count less, and no value is used for this.
- **The course's sample conversation:** the code comment says 30 messages, while the list and the Lesson 5 transcript say 32. It is not copied; S2 is this spec's own.

**Option C4b details (course facts; use only when C4b is chosen):**
- The course ran Oracle AI Database 26ai (Free) in a local container, reached at `127.0.0.1:1521/FREEPDB1`.
- A one-time admin step created a dedicated user with connect, resource, session, table, sequence and view grants and unlimited tablespace. It also set that user's default tablespace to one with automatic segment space management (needed for JSON columns; error ORA-43853 otherwise).
- Connections retried 3 times, 5 seconds apart. The course notes "Admin connection failed" right after start-up means the database is still starting: wait and retry.
- Vector stores used LangChain's Oracle vector store, with one IVF ("neighbor partitions") vector index per vector store, matching the store's distance, at target accuracy 95. An index that already exists (ORA-00955) is skipped.
- A helper existed to drop vector indexes when vector memory ran out (ORA-51962).
- Passwords come from the environment (D11).

### Names that go stale (search keywords for current docs, not guaranteed imports)
- `OracleVS` (`langchain_oracledb.vectorstores`), `OracleVectorizerPreference` (`langchain_oracledb.retrievers.hybrid_search`), `DistanceStrategy` (`langchain_community.vectorstores.utils`), `oracledb`.
- `HuggingFaceEmbeddings`, imported from `langchain_huggingface` in some lessons and from `langchain_community.embeddings` in others.
- `ArxivRetriever` and `ArxivLoader` (`langchain_community`), `RecursiveCharacterTextSplitter` (`langchain_text_splitters`), `TavilyClient` (`tavily`), `load_dataset` streaming (`datasets`).
- The OpenAI client's chat completions call with `max_completion_tokens`, tools and `tool_choice="auto"`.
- Models `gpt-5-mini` (agent) and `gpt-5` (summarizer, labeler, entity extractor, tool describer, query generator); embedding model `sentence-transformers/paraphrase-mpnet-base-v2`.
- **Request-parameter limits implied by the course's calls:** they use `max_completion_tokens` rather than `max_tokens`, and never set `temperature`. This suggests the course-era models may reject `max_tokens` or a non-default temperature; check the current models' docs before adding either.

### Course names (→ spec terms)
- **Store names:** `CONVERSATIONAL_MEMORY`, `SEMANTIC_MEMORY` (knowledge base), `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY`, `TOOL_LOG_MEMORY`. These are binding.
- **Classes:** `MemoryManager` → the memory read and write operations; `StoreManager` → store setup; `Toolbox` and `register_tool` → tool registration (R14, R15).
- **Functions:** `call_agent` → one turn (R17); `summarize_conversation`, `summarise_context_window`, `offload_to_summary` → R9 and R10. `expand_summary`, `summarize_and_store`, `arxiv_search_candidates`, `fetch_and_save_paper_to_kb_db`, `get_current_time` are binding tool names. `calculate_context_usage` → R9. `monitor_context_window` (statuses ok under 50%, warning under 80%, critical otherwise) was a Lesson 5 utility the final loop imported but never used, so it is not required.
- **Terms:** "memory unit" → a row; "agent memory core" → the database; "thread" → `thread_id`; `[Summary ID: x]` → summary reference.
- **Example names:** "ArxivScout" was the Lesson 3 example assistant's name. `SAMPLE_RESEARCH_CONVERSATION` is replaced by S2.

### Lesson map (transcript numbering decides)
- **L1 Introduction:** framing — memory as infrastructure outside the model (card item 1).
- **L2 Why AI Agents Need Memory:** stateless vs memory-augmented agents (failure F1, C5b), conversational memory, the memory taxonomy (semantic cache, persona: background), RAG and reranking (C10), the agent memory core.
- **L3 Constructing the Memory Manager:** stores and names, distance (D2), indexes, the deterministic vs agent-triggered table (C11), seeding (R23, D3), the memory-aware agent steps (R6).
- **L4 Scaling Agent Tool Use with Semantic Tool Memory:** the toolbox (C7, R14, R16), augmentation (C8, R15, D4), web search with store (C1c), the arXiv tools (R22), toolbox search as a tool (C7c).
- **L5 Memory Operations — Extraction, Consolidation, and Self-Updating Memory:** context engineering, summarization vs compaction (C12), budget (R9), the summary pipeline (R10–R13, D5), workflow memory.
- **L6 Memory Aware Agent:** the agent loop and harness, memory operations in and out of the loop, the final end-to-end agent (R2, R5, R17–R21), and the five-turn demo (T38).
- **L7 Conclusion:** recap.

The code materials label their notebooks L2–L5, and their section headers map them to Lessons 4, 5 and 6. Their content belongs to transcript Lessons 3–6 in order: "Constructing the Memory Manager", "Scaling Agent Tool Use", "Memory Operations", "Memory Aware Agent". Content and transcripts decide. The instructor's spoken "lesson 4/5" at the end of Lessons 5 and 6 also counts differently.

**Slides:** all 60 slide images were read. The Lesson 2 deck has 19 wide slides; the Lessons 3–6 deck has 41 tall slides. They are talked through in the transcripts and counted like them. Slide-only items, which count less:
- persona memory in two tables;
- a workflow table sketch with run id, thread id, a JSON workflow document and an embedding, plus a richer step-by-step workflow JSON (the code stores text plus metadata, and the spec follows the code);
- "~5–20 tools in practice".

One deck slide is a template leftover (base vs instruction-tuned LLM) and was ignored.

Nothing in this spec requires access to the course.

---

*Spec v2 draft · course: Agent Memory: Building Memory-Aware Agents · project: memory_agent · when the build agent does something unexpected, add the missing constraint here and re-run.*
