# Spec: a memory-aware research agent

**What you're building:** a command-line research assistant whose memory lives in a database file outside the model. You see it find a paper, save the paper into its knowledge base, answer follow-ups days later in a fresh session, compress its own older conversation into a summary, and expand that summary when you ask about something said earlier.

**Fastest path:** at the first question, answer "recommended build". The build is done when the offline tests pass. They need no key and no network, because a scripted stand-in model and a stand-in paper catalog replace the real ones. An OpenAI key only unlocks the `live` tests and real use.

This file is self-contained. Everything the build needs is here. It never asks you to open the course or its notebooks.

*Provenance: course "Agent Memory: Building Memory-Aware Agents" (7 lessons). Materials used: lesson transcripts, the course notebooks with their helper module and requirements file, and the lesson slide images. Written 2026-10-27 with guide v2.6 (2026-10-27).*

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

Asked in this order. Each option has an id, a "pick this when …", and its setup cost.

### C1. What will your assistant help with?
- **C1a. A research assistant that finds papers on arXiv, saves them into its knowledge base, and answers from them (Recommended - course default).** Pick this when you want the course's assistant, or you research papers. Setup cost: none beyond the model (arXiv needs network access but no key).
- **C1b. An assistant for your own subject.** You name its role in one line (e.g. "a support assistant that remembers each customer"), give a folder of your own documents for its knowledge base, and list the tools it should have. Pick this when your work is not paper research, e.g. you want an assistant over your own notes or tickets. Setup cost: you write or supply each tool; any tool that calls a paid service needs that service's key.
  - What to check: the system prompt names your assistant's role; your documents load through the knowledge-base loader, and a question about one of them returns a passage from it; each of your tools is found by a query that describes what it does.

### C2. Which model provider will run the agent?
- **C2a. OpenAI (Recommended - course default).** Pick this when you have an OpenAI key, or want the course's own setup. Setup cost: an OpenAI API key (paid account).
- **C2b. Another hosted provider whose API supports tool calling** (for example Anthropic or Google). Pick this when you already pay for a different provider, or your organisation allows only that one. Setup cost: that provider's API key (paid account).
  - What to check: with a real key, one turn that needs a tool calls it through the chosen provider and then answers, and the conversation log holds both the question and the answer.
- **C2c. A model served on your own machine that supports tool calling** (for example through Ollama). Pick this when you have no paid key, or your conversations must not leave your machine. Setup cost: a local model server and a model download of several GB. Small local models call tools less reliably.
  - What to check: with network access to cloud model APIs blocked, one turn that needs a tool calls it through the local server and then answers, and the conversation log holds both messages.

### C3. How will you talk to the assistant?
- **C3a. A command-line chat (Recommended).** You type questions in a terminal session tied to a thread id. Pick this when you use the assistant yourself. Setup cost: none.
- **C3b. A small local HTTP API.** A `POST /ask` endpoint that takes a thread id and a question and returns the answer as JSON. Pick this when another program of yours (a web page, a bot) will call the assistant. Setup cost: one web-framework package.
  - What to check: a `POST /ask` with a thread id and a question returns the answer as JSON; after restarting the server, a second `POST` on the same thread sees the first exchange in Conversation Memory.

### C4. Where is memory stored?
- **C4a. A single SQLite database file, using Python's standard library (Recommended).** This is a stand-in for the course's Oracle AI Database. Vectors are stored in the file and searched by direct comparison. Pick this when you run the assistant on one machine for one user. Setup cost: none.
- **C4b. Oracle AI Database 26ai (course default).** It runs as a local server in a container: tables for conversation and tool logs, and vector tables with vector indexes for the other stores. Pick this when you already run Oracle, need several processes or users sharing one memory, or have enough records to need a real vector index. Setup cost: a container runtime, the database image (a download of several GB), an admin password, and a one-time user and tablespace setup.
  - What to check: on the Oracle database, all seven stores exist after the first start; a turn written before restarting the app appears in Conversation Memory after the restart; vector searches return the closest records by cosine distance.

### C5. Which kinds of memory does the assistant keep?
- **C5a. The full set: conversation log, knowledge base, workflow memory, entity memory, summaries, the toolbox, and the tool log (Recommended - course default).** Pick this when the assistant must reuse knowledge, past procedures and names across sessions, not only past chat. Setup cost: none beyond C7's choice.
- **C5b. Conversation memory only.** It keeps the conversation log, the tool log and, unless C9 is C9c, summaries of older conversation. There is no knowledge base, workflow, entity or toolbox store. Every tool is passed to the model every turn, and tools that write to a knowledge base are left out. Pick this when the assistant only needs to carry on past conversations (e.g. a personal helper that should recall what you discussed last week) and has only a handful of tools. Setup cost: none, and no embedding model is needed. Cost, from the course: "Conversation windows are actually finite, but the user relationships are not"; "Agents need structured, queryable knowledge, not just chat logs."
  - What to check: only the conversation-log, tool-log and summary stores exist; each turn's context holds the thread's conversation and summary references and no Knowledge Base, Workflow or Entity section; every registered tool is passed on every model call.

### C6. How does the model get its tools?
*Ask only when `C5` is `C5a`.*
- **C6a. A toolbox: tools are stored with embeddings of their descriptions, and only the 5 most relevant to the request are passed (Recommended - course default).** Pick this when you have, or expect, more tools than a model handles well. Setup cost: none. Tool descriptions marked for augmentation cost one model call each, the first time they are registered.
- **C6b. Every registered tool on every model call.** Pick this when you have only a few tools (the course cites model-provider guidance of roughly 5–20 at most). Setup cost: none. Cost, from the course: as tools grow you get context bloat, worse tool selection, and more latency and tokens.
  - What to check: with seven tools registered, every model call receives all seven, and no toolbox store is created.

### C7. How is memory searched?
*Ask only when `C5` is `C5a`.*
- **C7a. By meaning: a local embedding model turns text into vectors, and the closest records by cosine similarity are returned (Recommended - course default).** Pick this when users phrase things differently from the stored text. Setup cost: an embedding model of about 0.4 GB plus PyTorch, downloaded once. No key.
- **C7b. By shared words (lexical search).** Records are ranked by the overlap between their words and the query's words. Pick this when you cannot install PyTorch or download the model (e.g. a restricted or offline machine), or your queries reuse the stored wording. Setup cost: none. Cost: a paraphrase that shares no words with the stored text is missed.
  - What to check: with no embedding model installed, a knowledge-base query that shares words with exactly one stored record returns that record first.
- **C7c. Hybrid: the meaning score and the word score combined.** Pick this when memories hold exact identifiers (paper ids, error codes, product codes) that meaning-based search ranks poorly, but users also paraphrase. Setup cost: the same as C7a.
  - What to check: a record that matches the query only through an exact identifier and a record that matches only in meaning both appear in the top results.

### C8. Which memory operations does the program run, and which does the agent decide?
*Ask only when `C5` is `C5a`.*
- **C8a. The program reads every memory kind before each answer and writes the conversation, workflow and entities after it. The agent decides only to summarize or to expand a summary; the program also summarizes on its own past the context threshold (Recommended - course default).** Pick this when you want the agent always to start from what it already knows. Setup cost: none.
- **C8b. The agent reads long-term memory itself.** The program still preloads the thread's conversation and a list of the memory stores and what each holds. Reading the knowledge base, workflow, entity and summary memory becomes tools the agent calls. Writes stay as in C8a. Pick this when the long-term stores are large and most requests need none of them (e.g. quick follow-up turns over a big research archive), so preloading wastes tokens. Setup cost: none. Cost, from the course: "the agent can't choose to look up what it doesn't know exists"; it may skip a lookup it needed, and each lookup is an extra model round trip.
  - What to check: for a question that needs a fact stored only in the knowledge base, the first model call's context has no Knowledge Base section, the agent calls the knowledge-base read tool, and the answer uses the passage it returned; Conversation Memory is still preloaded.
- **C8c. The program runs every memory operation; the agent gets no memory tools.** Older conversation is summarized only past the context threshold, and the summary text itself, not only its label, is placed in Summary Memory. Pick this when your model calls tools unreliably (e.g. a small local model), or you want memory behaviour that is fully predictable. Setup cost: none. Cost, from the course's case for agent-triggered operations: the agent cannot pull back exact older detail or choose to compress early, and summaries take more context.
  - What to check: no summarize or expand tool is offered to the model; past the threshold, the context shows the summary text under Summary Memory and the original messages stay marked as summarized.

### C9. How is older conversation shrunk when the context fills up?
- **C9a. Summarize and keep the originals (Recommended - course default).** Unsummarized messages of the thread are summarized. The summary is stored with the full transcript, and the original messages are marked with the summary's id. The context then shows only the summary's id and short label, and the full detail can be recovered (by the agent's expand tool, unless C8 is C8c). Pick this when old detail may matter later. Setup cost: none.
- **C9b. Summarize and replace (lossy).** The summary is stored, the original messages are deleted, and the context shows the summary text. Nothing can be expanded. Pick this when old messages must not be kept (privacy or retention rules), or storage must stay small. Setup cost: none. Cost, from the course: summarization "will always be a lossy technique … We will always lose a little bit of information".
  - What to check: after a summary is made, the summarized messages are gone from the conversation log, the context shows the summary text, and no expand tool exists.
- **C9c. Never shrink.** There is no context check, no summary store and no summary tools. Pick this when every session is short (a few turns), so a thread never nears the model's context window. Setup cost: none. Cost, from the course: context bloat, and once a thread outgrows the window the model call fails.
  - What to check: no summary store and no summary tools exist, and a thread past the threshold is sent whole, without a stub.

---

## 2. Departures from the course (recommended build)

| # | Where | The course | The recommended build | Why |
|---|---|---|---|---|
| D1 | Storage (C4) | Oracle AI Database 26ai in a container, accessed through LangChain's Oracle vector store | **Stand-in:** one SQLite file (Python standard library); vectors kept in the file and compared directly | Oracle needs container and admin setup. At sample scale, direct comparison returns the same ranking. Oracle stays offered as C4b. |
| D2 | Start-up | Every lesson notebook drops all memory tables at start, "to start fresh" | Stores are created if missing and **never dropped** on start | Dropping existed so each lesson could run alone. It would erase memory between sessions, which pattern-card item 1 forbids. |
| D3 | Interface | Functions called from notebook cells | A command-line chat (C3a) and a one-shot `ask` command | A build is never a notebook. *Addition.* |
| D4 | Knowledge-base seed | Streams 100 paper records from a public dataset over the network | Loads paper records from a local JSON-lines file through the same loader; the sample file is written for this spec | No course data is copied, and the seed works offline. |
| D5 | Web-search tool | One lesson registers a web-search tool that needs a paid search key and saves its results into the knowledge base | Left out | It is absent from the course's final agent, and "search, then store into the knowledge base" is already exercised by the paper-saving tool. |
| D6 | Tool descriptions | The code embeds the original docstring for search and uses the LLM-augmented description only as the description shown to the model | The text searched is the name, the **augmented** description, the signature and the generated example queries | The instructor states that the enhanced name and description are what get encoded and loaded (4.1: follow the instructor; see note N3). |
| D7 | Distance | Cosine in two lessons; Euclidean in the last two lessons' code | Cosine | The instructor states cosine when introducing it (4.2 rule 1). |
| D8 | Entity writes | One lesson's table marks entity writes as agent-triggered | Entities are extracted automatically from each question and each final answer | The final agent's code does this, and the instructor describes it as a write outside the loop (4.2 rules 1–2). |
| D9 | Timestamps | Database current time; the course's test adds a 0.05 s pause between writes | Timestamps with microseconds; ties are ordered by insertion | Without this, messages in the same second come back in an undefined order. *Addition.* |
| D10 | Vector index | One lesson creates an IVF vector index (target accuracy 95) | No index in SQLite (direct comparison); C4b creates it | No index exists to build in the stand-in. |
| D11 | Models | gpt-5-mini runs the agent; gpt-5 runs summaries, labels, entity extraction and tool augmentation | The build agent picks current models per role (§5.1) | Model names go stale. |
| D12 | Tests | The course checked by printing | Offline tests on a scripted stand-in model, a stand-in embedder and a stand-in paper catalog; `live` tests when a key is present | So the build can be checked offline. *Addition.* |

---

## 3. Objective

Build a tool-using agent whose memory lives in persistent storage outside the model. Before every answer it assembles the memory relevant to the request, and after every answer it records what happened, so it carries on across turns and sessions.

---

## 4. Tech stack and versions

- **Language:** Python 3.10 or newer. The course did not state a version; its code uses the `X | None` type syntax, which needs 3.10.
- **Packages:** the course installed every package unpinned, so use current releases. None is pinned here. Course packages the recommended build uses: `openai` (model client), `sentence-transformers` and `langchain-huggingface` (embedder), `langchain-community` with `arxiv` and `pymupdf` (paper search and PDF text), `langchain-text-splitters` (chunking), and `python-dotenv` (reads `.env`). You may call `arxiv`/`pymupdf` directly instead of the LangChain wrappers if the behaviour in §6 is kept.
- **Standard library:** `sqlite3` for storage (D1).
- **Tests:** `pytest`, with a `live` marker. *Addition.*
- **Package name:** `memagent`, run as `python -m memagent`.
- **Secrets:** `OPENAI_API_KEY` is read from the environment or a `.env` file (as the course did) and never written anywhere. Under C4b, the Oracle admin and user passwords are also read from the environment (`MEMAGENT_ORACLE_ADMIN_PASSWORD`, `MEMAGENT_ORACLE_PASSWORD`). The course hard-coded them; never do that.
- **Configuration:** `MEMAGENT_DB` gives the database file path (default `memory.db`). `MEMAGENT_OFFLINE=1` makes the app use the scripted stand-ins of §7.1 instead of the real model, embedder and arXiv. *Addition, labelled stand-in mode.* Without a key and without offline mode, the app prints `OPENAI_API_KEY is not set (or set MEMAGENT_OFFLINE=1 for stand-in mode).` and exits with status 2.

---

## 5. Contracts

### 5.0 The stores
The store names are binding. They appear in text the model and the tool log see.

| Store (course name) | Kind | Record schema |
|---|---|---|
| `CONVERSATIONAL_MEMORY` | table | Conversation row (below) |
| `TOOL_LOG_MEMORY` | table | Tool-log row (below) |
| `SEMANTIC_MEMORY` | vector store | Knowledge-base record |
| `WORKFLOW_MEMORY` | vector store | Workflow record |
| `TOOLBOX_MEMORY` | vector store | Toolbox record |
| `ENTITY_MEMORY` | vector store | Entity record |
| `SUMMARY_MEMORY` | vector store | Summary record |

Every vector-store record holds three things: `text` (the text that is embedded and searched), `metadata` (a JSON object) and `embedding`. Search returns records in descending similarity; ties keep insertion order, oldest first. A metadata filter applies before ranking.

```json
{
  "ConversationRow": {
    "type": "object",
    "required": ["id", "thread_id", "role", "content", "timestamp", "metadata", "created_at"],
    "properties": {
      "id": {"type": "string", "description": "unique, generated"},
      "thread_id": {"type": "string", "maxLength": 100},
      "role": {"enum": ["user", "assistant"]},
      "content": {"type": "string", "minLength": 1},
      "timestamp": {"type": "string", "format": "date-time", "description": "microsecond precision"},
      "metadata": {"type": "string", "const": "{}"},
      "created_at": {"type": "string", "format": "date-time"},
      "summary_id": {"type": ["string", "null"], "pattern": "^[0-9a-f]{8}$", "default": null}
    }
  },
  "ToolLogRow": {
    "type": "object",
    "required": ["id", "thread_id", "tool_name", "status", "timestamp"],
    "properties": {
      "id": {"type": "string"},
      "thread_id": {"type": "string"},
      "tool_call_id": {"type": ["string", "null"]},
      "tool_name": {"type": "string"},
      "tool_args": {"type": "string", "description": "JSON text of the arguments"},
      "result": {"type": "string", "description": "full, untruncated result"},
      "result_preview": {"type": "string", "description": "first 2000 bytes of result as UTF-8, cut at a whole character"},
      "status": {"enum": ["success", "failed"]},
      "error_message": {"type": ["string", "null"]},
      "metadata": {"type": "string", "description": "JSON text, e.g. {\"iteration\": 1}"},
      "timestamp": {"type": "string", "format": "date-time"},
      "created_at": {"type": "string", "format": "date-time"}
    }
  },
  "KnowledgeRecord.metadata": {
    "oneOf": [
      {"description": "seeded paper", "required": ["arxiv_id", "title", "subjects", "abstract", "submission_date"]},
      {"description": "saved paper chunk", "required": ["source", "arxiv_id", "title", "entry_id", "published", "authors", "chunk_id", "num_chunks", "ingested_ts_utc"],
       "properties": {"source": {"const": "arxiv"}, "chunk_id": {"type": "integer", "minimum": 0}, "num_chunks": {"type": "integer", "minimum": 1}}}
    ]
  },
  "WorkflowRecord": {
    "text": "Query: <query>\\nSteps:\\nStep 1: <step>\\n…\\nStep n: <step>\\nAnswer: <first 200 characters of the final answer>",
    "metadata": {"required": ["query", "success", "num_steps", "timestamp"],
                 "properties": {"success": {"type": "boolean"}, "num_steps": {"type": "integer", "minimum": 0}}}
  },
  "ToolboxRecord": {
    "text": "<name> <description> <signature> <generated queries joined by spaces>  (description = augmented description when augmented; queries only when augmented)",
    "metadata": {"required": ["name", "description", "signature", "parameters", "return_type", "augmented"],
                 "properties": {"parameters": {"type": "object", "description": "per parameter: name, type (if annotated), default (if any)"},
                                "queries": {"type": "array", "items": {"type": "string"}}}}
  },
  "EntityRecord": {
    "text": "<name> (<type>): <description>",
    "metadata": {"required": ["name", "type", "description"],
                 "properties": {"type": {"enum": ["PERSON", "PLACE", "SYSTEM", "UNKNOWN"]}}}
  },
  "SummaryRecord": {
    "text": "<id>: <label>",
    "metadata": {"required": ["id", "full_content", "summary", "description"],
                 "properties": {"id": {"pattern": "^[0-9a-f]{8}$"}, "thread_id": {"type": "string", "description": "present for thread summaries"}}}
  },
  "ToolSchemaPassedToModel": {
    "type": "function",
    "function": {"name": "<name>", "description": "<stored description>",
                 "parameters": {"type": "object", "properties": {"<param>": {"type": "string|integer|number|boolean"}}, "required": ["<params with no default>"]}}
  }
}
```

Parameter types map `str`→`string`, `int`→`integer`, `float`→`number` and `bool`→`boolean`; anything else becomes `string`.

### 5.0.1 Agent call
- **Input:** `query` (text), `thread_id` (text, default `"1"`), `max_iterations` (default 10).
- **Output:** the final answer text.
- **Side effects:** the rows and records named in R3, R10 and R11.

### 5.0.2 The context window (what the model receives)
- **System message:** the agent system prompt (R9a).
- **User message:** `# Question\n<query>\n\n` followed by the memory sections, in this order. Each section ends with a blank line.
  1. `## Conversation Memory` then `### What this memory is` (chronological, unsummarized messages from the current thread: user intent, constraints and commitments from recent turns), `### How you should leverage it` (keep continuity with earlier decisions, terminology and preferences; resolve references such as "that" or "the paper above" from earlier turns; let newer user instructions win over older context), `### Retrieved messages`, a blank line, then one line per message `[HH:MM:SS] [<role>] <content>`, or `(No unsummarized messages found for this thread.)`.
  2. `## Knowledge Base Memory` then `### What this memory is` (retrieved background documents and ingested reference material relevant to the query), `### How you should leverage it` (ground factual and technical claims in these passages; prefer them over assumptions; if evidence is missing, say so and ask or retrieve more), `### Retrieved passages`, a blank line, then the passages' text joined by newlines, or `(No relevant knowledge base passages found.)`.
  3. `## Workflow Memory` then `### What this memory is` (past task trajectories: query, ordered steps, outcomes), `### How you should leverage it` (reuse them as execution patterns; adapt rather than copy; reuse successful patterns first), `### Retrieved workflows`, then the workflow texts separated by lines of `---`, or `(No relevant workflows found.)`.
  4. `## Entity Memory` then `### What this memory is` (people, organisations, systems and other named items seen before), `### How you should leverage it` (disambiguate references; keep names consistent; keep attributes across turns), `### Retrieved entities`, then lines `• <name>: <description>`, or `(No entities found.)`.
  5. `## Summary Memory` then `### What this memory is` (compressed snapshots of older conversation), `### How you should leverage it` (use summaries for continuity; call expand_summary(id) before relying on exact quotes, fine detail or chronology), `### Available summaries`. When summaries exist, the next lines are `Use expand_summary(id) to retrieve the detailed underlying conversation.`, `Scope: thread_id = <thread_id>` and one line per summary `  • [ID: <id>] <label>`. When none exist, the line is `(No summaries available for thread <thread_id>.)`.

### 5.1 Model roles

The gate's model lines (§0 step 5) name one model for each role.

| Role | What it does | Course model |
|---|---|---|
| agent | Runs the agent loop with tool calling (`tool_choice` automatic) | gpt-5-mini |
| summarizer | Writes the four-heading summary | gpt-5 (final agent); gpt-5-mini in the summarization lesson |
| labeler | Writes the 8–12-word summary label | as summarizer |
| entity-extractor | Returns a JSON list of entities | gpt-5 |
| tool-augmenter | Rewrites a tool's description from its docstring and source | gpt-5 |
| query-generator | Writes 5 example user queries per tool | gpt-5 |

The stand-in routes requests by these exact prompt openings, which are binding:
- **summarizer:** `You are creating durable memory for an AI research assistant.` (main prompt); `Summarize this conversation in <= 180 words using these headings:` (retry).
- **labeler:** `Create a short 8-12 word label for this summary.`
- **entity-extractor:** `Extract entities from:`
- **tool-augmenter:** `You are a technical writer.`
- **query-generator:** `Based on the following tool description,`
- **agent:** a request whose system message is the agent system prompt.

### 5.2 Settings
These are not questions. The person tunes them after the build.

| Setting | Value | Course source | Change this when … |
|---|---|---|---|
| conversation read limit | 10 messages, oldest unsummarized first (note N1) | conversation read default; final agent | threads routinely hold more than 10 unsummarized messages |
| knowledge-base results | 3 | knowledge-base read default | answers need more passages |
| workflow results | 3, only workflows with at least 1 step | workflow read | — |
| entity results | 5 | entity read default | — |
| summary references listed | 10, current thread only | summary-context read | — |
| tools passed per request | 5 | final agent loop (the toolbox read default is 3) | you have many near-duplicate tools |
| max loop iterations | 10 | final agent loop | tasks need longer tool chains |
| tool result sent to model | first 3000 characters | final agent loop | tools return long but essential output |
| tool-log preview | first 2000 bytes | tool-log write | — |
| summarize threshold | context usage percent **greater than** 80 (note N2) | final agent loop; Lesson 5–6 transcripts | you want earlier or later compression |
| characters per token | 4 | usage estimator ("~4 chars per token") | your model's tokenizer differs a lot |
| context window | 256,000 tokens (course code falls back to 128,000 for unlisted models) | token-limit table | your model's window differs |
| summarizer input cap | first 6000 characters of the transcript | summary prompt | — |
| summary reply budget | 4000 completion tokens; retry prompt ≤ 180 words | summary function | — |
| label length | 8–12 words; label budget 2000 completion tokens | label prompt | — |
| fallback summary excerpt | first 500 characters, newlines replaced by spaces | summary function | — |
| entity text cap | first 500 characters of the text | entity prompt | — |
| entity / augment / query reply budget | 2000 completion tokens each | helper | — |
| generated example queries per tool | 5 | toolbox | — |
| tool augmentation per tool | `arxiv_search_candidates` off, `fetch_and_save_paper_to_kb_db` on, `get_current_time` off, `expand_summary` on, `summarize_and_store` on | final agent's tool registration | retrieval confuses similar tools (turn on) or registration cost matters (turn off) |
| summary id | 8 lowercase hex characters | summary function | — |
| arXiv search | at most 8 papers fetched, 4000 characters each; at most 5 candidates returned; abstract cut to 2500 characters | arXiv retriever and search tool | — |
| paper chunking | chunk size 1500 characters, overlap 200 | paper-saving tool | your embedder takes longer inputs |
| workflow answer excerpt | first 200 characters | workflow write | — |
| step argument display | string values longer than 50 characters shown as their first 50 characters + `...` | agent loop | — |
| similarity | cosine (D7) | memory-manager lesson | — |
| embedder (C7a) | `sentence-transformers/paraphrase-mpnet-base-v2`, 768 dimensions | all lessons | — |
| default thread id | `"1"` | agent loop | — |

---

## 6. Business rules

### 6.1 What must stay true (pattern card)
These items come from the owner-confirmed pattern card. Every option keeps them.
1. **Memory lives outside the model and survives the session.** What the agent learns in one turn or session is stored in persistent storage and is available to later turns and new sessions. Nothing depends on the model or the process remembering it. → T2, T12, L1
2. **Before the model answers, the memory relevant to the request reaches its context.** → T4, T2

### 6.2 Rules

- **R1. Stores.** On start, the seven stores of §5.0 are created if missing. Existing stores and their data are never dropped (D2). → T1, T2
- **R2. Persistence across sessions.** Anything written by one process is read by a new process that opens the same database file, for the same thread id. Different thread ids never see each other's conversation. → T2
- **R3. Conversation writes.** Each agent call writes the user message (after context assembly, before the loop) and the final answer (after the loop) as conversation rows. Each row carries role `user` or `assistant`, the thread id, a microsecond timestamp, metadata `{}` and no summary id. → T10, T3
- **R4. Conversation read.** For a thread, return only rows with no summary id, in ascending time (ties by insertion), the **first** 10, formatted as in §5.0.2; an empty thread gets the placeholder. → T3, T13
- **R5. Context assembly (card item 2).** Before the first model call of each agent call, the program builds the context of §5.0.2 from the conversation read (R4), the knowledge base (top 3 for the query), workflows (top 3 for the query, `num_steps > 0`), entities (top 5 for the query) and the summary references of the thread (top 10 for the query; ids and labels only). The query is never summarized away. → T4, T5
- **R6. Context budget.** Usage tokens = characters of the assembled memory sections ÷ 4, rounded down; percent = tokens ÷ 256,000 × 100, rounded to one decimal. If percent > 80, the program offloads before continuing (R6a) and recomputes usage. → T6, T7
  - **R6a. Offload.** Summarize the thread's conversation (R14). If there was nothing to summarize, the context is unchanged. Otherwise the whole `## Conversation Memory` section (up to the next `## ` heading) is replaced by three lines: `## Conversation Memory`, `Older conversation content was summarized to reduce context size.`, `Use Summary Memory references + expand_summary(id) for full detail.` Then `[Summary ID: <id>] <label>` is appended on a new line at the end of the context. → T6
- **R7. Tool registration.** A tool is stored at most once per name, and registering a name that already exists in the toolbox (including from an earlier process) writes nothing new. The callable is still available for execution. Metadata: name, description (the augmented description when augmentation is on, else the docstring), signature, parameters, return type, `augmented`, and `queries` (when augmented). When augmentation is on, the tool-augmenter receives the docstring and the function's source, and the query-generator receives the augmented description and returns a JSON array of 5 queries. If its reply is not a JSON array, the queries are a one-item list holding the raw reply. Search text as in §5.0 (D6). → T8, T9
- **R8. Tool selection.** Per agent call, the top 5 toolbox records by similarity to the query are passed as tool schemas (§5.0), with duplicate names dropped. Parameters with no default are required. → T8
- **R9. Agent loop.** Messages start as [system prompt, context]. At each iteration (at most 10) the model either returns tool calls or a final answer.
  - Each tool call is executed by name from the registered tools, whether or not it was passed this turn.
  - An unknown name yields the result `Error: Tool '<name>' not found` with status `success` (note N4). A tool that raises yields `Error: <message>` with status `failed` and the error message recorded. A tool returning an empty result yields `Done`.
  - When `summarize_and_store` is called without `thread_id`, the current thread id is added.
  - The assistant message carrying the tool calls, then one tool message per call, are appended. Each step is recorded as `<tool>(<args>) → success|failed` (args displayed as in §5.2).
  - A reply with no tool calls is the final answer. If 10 iterations pass without one, the final answer is `I was unable to complete the request within the allowed iterations.`
  → T10, T12, T14, T16, L1
  - **R9a. System prompt.** It must contain, in substance:
    - the role: "a memory-aware agentic research assistant with access to tools" (under C1b, the person's role line);
    - that the user input is a partitioned context with a `# Question` section and the five memory sections, named by their headings;
    - one line per store on what it is for (Conversation: continuity, preferences and unresolved requests; Knowledge Base: grounding claims; Workflow: planning tool use, adapting rather than copying; Entity: disambiguating names; Summary: compressed older context, preferring summaries of the active thread);
    - the expansion policy: call `expand_summary(summary_id)` before relying on detail found only in a summary;
    - the operating rules: (1) start from the memory sections before using tools; (2) on conflict, prefer the current question, then the latest conversation, then knowledge-base evidence, then older summaries and workflows; (3) use only the tools given this turn, with the fewest calls needed; (4) if memory is insufficient, say what is missing, then use a tool; (5) for conversation compaction, use `summarize_and_store` with `thread_id`.
    → T4
- **R10. Tool log and result size.** Every tool call writes one tool-log row with the full result, the preview, the status, the error message, and metadata `{"iteration": n}` (n counted from 1). The tool message sent to the model is the result, or, when the result is longer than 3000 characters, its first 3000 characters followed by `\n\n[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <log id>]`. → T15, T10
- **R11. After the loop.** If at least one tool call was made, a workflow record is written (§5.0): `success` true, `num_steps` = the number of steps (note N5). Entities are extracted from the final answer (R12). The final answer is written as the assistant message. → T10, T11, T14, T26
- **R12. Entities.** Entities are extracted from the user message (before the loop) and from the final answer (after the loop).
  - The extractor receives the first 500 characters of the text, and texts shorter than 5 non-space characters are skipped. It is asked for a JSON list of `{name, type: PERSON|PLACE|SYSTEM, description}`.
  - The reply is parsed from its first `[` to its last `]`. Entries without a name are dropped, and a missing type becomes `UNKNOWN`.
  - Any failure means no entities and never stops the agent call.
  - Each entity is stored as an entity record.
  → T11
- **R13. Summary making.** Given text:
  - Strip it; empty text gives "nothing to summarize".
  - The summarizer receives the first 6000 characters under the main prompt, which asks for exactly the headings `### Technical Information`, `### Emotional Context`, `### Entities & References` and `### Action Items & Decisions`, to keep concrete details (names, dates, APIs, errors, decisions), to separate confirmed facts from open questions, not to invent, and to stay concise.
  - An empty reply triggers one retry with the ≤ 180-word prompt.
  - If the reply is still empty, the summary is the deterministic fallback: `### Technical Information\n<excerpt>\n\n### Emotional Context\nNot available from model output.\n\n### Entities & References\nNot available from model output.\n\n### Action Items & Decisions\nNot available from model output.`, where the excerpt is the first 500 characters with newlines replaced by spaces.
  - The labeler then asks for a specific 8–12-word label, never a generic one. A reply that is empty, or (ignoring case, after stripping quotes) is `conversation summary`, `summary`, `chat summary` or `thread summary`, is replaced by the fallback label: the first line of the summary (or of the text, if the summary is empty) that, after trimming spaces and leading `-•* `, is not empty, does not start with `###`, and has at least 4 words; its first 12 words, trimmed of ` ,.;:`. If no line qualifies, the label is `Recent thread context, decisions, and open actions`.
  - The id is 8 lowercase hex characters. A summary record is stored with the full text, summary, label and (for thread summaries) the thread id.
  → T17, T18, T19
- **R14. Summarizing a thread.** Read all of the thread's rows without a summary id, in time order. None means "nothing to summarize". Otherwise build the transcript, one line per row `[YYYY-MM-DD HH:MM:SS] [<ROLE in capitals>] <content>`, summarize it (R13, thread-scoped), and set the summary id on exactly those rows. Report the id, label, summary and number of messages summarized. Rows that already carry a summary id are never summarized again. → T6, T12, T17, T20
- **R15. Tool `summarize_and_store(text="", thread_id=None)`.**
  - With a thread id: summarize the thread (R14) and reply `Stored as [Summary ID: <id>] <label>`, or `No unsummarized messages found for thread <thread_id>.`
  - Without one: stripped empty text replies ``Provide `thread_id` (preferred) or non-empty `text` to summarize.``; otherwise summarize the text (R13, no thread) and reply `Stored as [Summary ID: <id>] <label>`.
  → T12, T19, T20
- **R16. Tool `expand_summary(summary_id, thread_id=None)`.**
  - Replies `## Summary Context`, the stored summary text (or `Summary <id> not found.`, or `Summary <id> not found for thread <thread_id>.` when a thread is given and does not match), a blank line, then the originals.
  - The originals section is `## Expanded Conversations for Summary ID: <id>`, `Total messages: <n>`, a blank line, then per message a line `[YYYY-MM-DD HH:MM:SS] [<ROLE in capitals>]`, a line with the content, and a blank line, in time order. With no originals it is `No conversations found for summary_id: <id>`.
  → T12, T21
- **R17. Recommended tools (C1a).** Their descriptions begin with these first lines, which are binding because the toolbox searches them: `arxiv_search_candidates` "Search arXiv and return a JSON list of candidate papers with IDs + metadata."; `fetch_and_save_paper_to_kb_db` "Fetch full arXiv paper text and store it in the knowledge base as chunked records."; `get_current_time` "Returns the current time."; `expand_summary` "Expand a summary reference to retrieve the original conversations."; `summarize_and_store` "Summarize content and store it in Summary Memory."
  - `arxiv_search_candidates(query, k=5)` returns a JSON list (indented by 2) of at most `k` candidates in source order. Each candidate has `arxiv_id` (the part of the entry id's path after `/abs/`, without slashes), `entry_id`, `title`, `authors`, `published`, and `abstract` (first 2500 characters).
  - `fetch_and_save_paper_to_kb_db(arxiv_id, chunk_size=1500, chunk_overlap=200)` loads the paper's full text and splits it recursively (paragraphs, then lines, then words, then characters) into chunks of at most `chunk_size` characters, with up to `chunk_overlap` characters carried between merged pieces. It writes each chunk to the knowledge base with the chunk metadata of §5.0 (title falls back to `arXiv <id>`), and replies `Saved arXiv <id> to SEMANTIC_MEMORY: <n> chunks (title: <title>).`
  - With no document it replies `No documents found for arXiv id: <id>`; with empty text it replies `Loaded arXiv <id> but extracted empty text (PDF parsing issue).`
  - `get_current_time(detailed=False)` returns local time `YYYY-MM-DD HH:MM:SS`, or with microseconds when `detailed`.
  → T22, T23, L1, L2
- **R18. Knowledge seed loader.** `python -m memagent seed <file.jsonl>` reads records with `arxiv_id`, `title`, `subjects`, `abstract` and `submission_date`. Records whose title, subjects and abstract are all empty after trimming are skipped. Each record's text is the non-empty ones among title, subjects and abstract, joined by newlines, with all five fields as metadata. → T24
- **R19. Command line (C3a).** `python -m memagent chat --thread <id>` reads one question per line and prints each answer. `--thread` defaults to `1`. `python -m memagent ask --thread <id> "<question>"` answers once, prints the answer and exits 0. `--verbose` also prints the context usage line `Context: <percent>% (<tokens>/<max> tokens)`, the tools passed, and each tool call, as the course's agent printed them. *Addition.* → T25
- **R20. The stateless failure (course-demonstrated).** An agent without stored memory cannot resolve "the first one" or "that paper" from an earlier turn. The program must answer a follow-up in a new process from stored conversation, not from process state. → T2

---

## 7. Tests

### 7.1 Sample data and stand-ins
All of these live under `tests/sample_data/`. All facts were written for this spec. Each stand-in is labelled a stand-in in its module docstring.

**`papers.jsonl`** (knowledge-base seed, 5 lines):

| id | title | subjects | abstract | submission_date |
|---|---|---|---|---|
| 2401.00001v1 | Tidal Memory Networks | cs.LG | An agent stores every conversation turn in an external tidal store and recalls it in later sessions. | 2024-01-01 |
| 2401.00002v1 | Coral Reef Acoustics | physics.ao-ph | Underwater microphones record reef sounds to estimate fish populations. | 2024-01-02 |
| 2401.00003v1 | Glacier Speed Estimation | physics.geo-ph | Satellite images measure how fast glaciers move each season. | 2024-01-03 |
| 2401.00004v1 | Sparse Kitchen Robots | cs.RO | A robot arm learns to load a dishwasher from three demonstrations. | 2024-01-04 |
| 2401.00005v1 | *(empty)* | *(empty)* | *(empty)* | 2024-01-05 |

**`standin_embedder`** (stand-in for the embedding model; it is also C7b's word matcher; it lives in the app package as `memagent/standin_embedder.py`):
- Lower-case the text, split it on every character that is not `a–z` or `0–9`, and drop tokens shorter than 2 characters and the stop words `the and or of to in on for is it this that with as by be are from at an you your me my we our can`.
- The vector is the token counts. Similarity is the cosine of two count vectors, and 0 if either is empty.

**`fake_arxiv.py`** (stand-in for the arXiv network source). A catalog of 8 entries. The entry id is `http://arxiv.org/abs/<arxiv_id>`.

| arxiv_id | title | authors | published | abstract | full text |
|---|---|---|---|---|---|
| 2401.00001v1 | Tidal Memory Networks | Ada Brightwater | 2024-01-02 | Agents that keep every conversation turn in an external tidal store can recall it in later sessions. | 3 paragraphs joined by `\n\n`; paragraph k (k = 1, 2, 3) is `Tidal memory paragraph k. ` repeated and cut to exactly 1000 characters |
| 2402.00002v1 | Glacier Study 2 | Bo Icefield | 2024-02-02 | `Glacier ` followed by `g` × 2992 (3000 characters) | `Glacier text 2.` |
| 2402.0000Nv1, N = 3–7 | Glacier Study N | Bo Icefield | 2024-02-0N | `Glacier flow measurements, part N.` | `Glacier text N.` |
| 2402.00099v1 | Empty Scan | Cy Scanner | 2024-02-09 | A scanned document. | *(empty)* |

- **Search:** entries whose title or abstract contains, case-insensitively, any query word of 3 or more letters, in catalog order, at most 8.
- **Load by id:** the entry with that exact id, or nothing.

**`scripted_model.py`** (stand-in model). It records every request it receives. Tool-call ids are `call_1`, `call_2`, … per instance. It replies by role (§5.1):
- **summarizer:**
  - If the prompt contains `EMPTY-SUMMARY-PLEASE`, it replies `""` (main and retry).
  - Else if it contains `tiny-case`: `### Technical Information\nshort note here\n### Emotional Context\nnone`
  - Else if it contains `river sensor`: `### Technical Information\nBudget review for the river sensor project.\n### Emotional Context\nCalm.\n### Entities & References\nNone.\n### Action Items & Decisions\nNone.`
  - Else if it contains `tidal` (any case): `### Technical Information\nSearched for and saved Tidal Memory Networks (2401.00001v1).\n### Emotional Context\nNeutral.\n### Entities & References\nAda Brightwater; Tidal Memory Networks\n### Action Items & Decisions\nNone.`
  - Otherwise: `### Technical Information\nLong filler content.\n### Emotional Context\nNone.\n### Entities & References\nNone.\n### Action Items & Decisions\nNone.`
- **labeler:**
  - If the prompt contains `river sensor` or `short note here`: `Summary`.
  - Else if it contains `Tidal`: `Search, save and takeaways of the Tidal Memory Networks paper`.
  - Otherwise: `Long filler thread condensed to free context window space`.
- **entity-extractor:**
  - If the prompt contains `BROKEN-JSON`: `no entities here`.
  - Otherwise a JSON list with one item per name found in the prompt, in this order:
    - `Ada Brightwater` → `{"name":"Ada Brightwater","type":"PERSON","description":"author of Tidal Memory Networks"}`
    - `Tidal Memory Networks` → `{"name":"Tidal Memory Networks","type":"SYSTEM","description":"memory architecture paper"}`
    - `Harbor Lab` → `{"name":"Harbor Lab","description":"research group"}` (no type)
  - With no names found, the reply is `[]`.
- **tool-augmenter:** `Augmented: ` + the first non-empty line of the docstring it received.
- **query-generator:**
  - If the prompt contains `Odd helper`: `not json`.
  - Otherwise the JSON array `["use <name>", "<name> please", "run <name>", "call <name>", "need <name>"]`, where `<name>` is the first word of the description after `Augmented: `, lower-cased.
- **agent:** the question is the text between `# Question\n` and the next blank line of the first user message. "After a tool result" means the last message is a tool message.

| Question | Before any tool result | After a tool result |
|---|---|---|
| `Find the paper on tidal memory` | call `arxiv_search_candidates` `{"query": "tidal memory"}` | `Found Tidal Memory Networks (arXiv 2401.00001v1) by Ada Brightwater.` |
| `Save the content of that paper` | if the Conversation Memory section contains `2401.00001v1`: call `fetch_and_save_paper_to_kb_db` `{"arxiv_id": "2401.00001v1"}`; else final `I have no record of which paper you mean.` | `Saved the paper to the knowledge base.` |
| `What are the main takeaways from the paper` | final `Takeaway: agents that store each turn outside the model can recall it in later sessions.` | — |
| `Summarize the conversation so far using your tool` | call `summarize_and_store` `{}` | `Summary stored.` |
| `What was my first question?` | if the context contains `[ID: ` followed by 8 hex characters and `]`: call `expand_summary` `{"summary_id": <those 8>}`; else final `I don't know.` | `Your first question was: ` + the line right after the first line ending in `[USER]` in the tool result |
| `Keep checking the time` | call `get_current_time` `{}` | call `get_current_time` `{}` (always) |
| `Run the long report` | call `long_report` `{"text": "r" × 60}` | `Done reading.` |
| `Use the missing tool` | call `no_such_tool` `{}` | `Could not.` |
| `Use the broken tool` | call `broken_tool` `{}` | `Could not.` |
| `Use the quiet tool` | call `quiet_tool` `{}` | `Quiet done.` |
| anything else | final `OK.` | `OK.` |

**`test_tools.py`** (test-only tools, *addition*, registered with augmentation off; signature `(text: str = "")` unless stated):
- `long_report` returns `L` × 5000.
- `broken_tool` raises an error with message `boom`.
- `quiet_tool` returns `""`.
- The seven-tool set for T8 has signature `(text: str)` and the one-line docstrings below, registered in this order:
  1. `search_papers`: "Search arxiv for research papers."
  2. `save_paper`: "Download a paper and save its text."
  3. `current_time`: "Return the current time."
  4. `convert_currency`: "Convert money between currencies."
  5. `weather_report`: "Report the weather forecast."
  6. `play_music`: "Play a music track."
  7. `count_words`: "Count words in text."

**Planted failure (stateless agent, R20):** the scripted agent's reply `I have no record of which paper you mean.` is what a stateless agent says. T2 must not get it on the remembered thread, and must get it on a thread with no history.

**`big_thread`** (in `tests/sample_data/threads.py`): thread `t-big` with 10 messages, alternating `user`/`assistant` starting with `user`, each `z` × 90,000.

Unless a test says otherwise, every test runs with `MEMAGENT_OFFLINE=1` semantics (scripted model, stand-in embedder, fake arXiv), a fresh temporary database file, the recommended tools registered with the settings of §5.2, and all other settings at their defaults.

### 7.2 Test table

| Test | Rules | Given | When | Then |
|---|---|---|---|---|
| T1 | R1 | a fresh database file | the app starts | the seven stores of §5.0 exist and are empty except the toolbox, which holds exactly 5 records (`arxiv_search_candidates`, `fetch_and_save_paper_to_kb_db`, `get_current_time`, `expand_summary`, `summarize_and_store`); `augmented` is false for `arxiv_search_candidates` and `get_current_time` and true for the other three |
| T2 | R1, R2, R20, card 1, card 2 | the papers seeded; process A answers `Find the paper on tidal memory` on thread `t-50` and closes | process B opens the same file (nothing shared in memory) and asks `Save the content of that paper` on `t-50`; then asks the same on thread `t-other` | `t-50`: the first model call's Conversation Memory contains `2401.00001v1`, `fetch_and_save_paper_to_kb_db` is called, and the answer is `Saved the paper to the knowledge base.`; `t-other`: no tool call, and the answer is `I have no record of which paper you mean.`; process B registering tools wrote no new toolbox records (still 5) |
| T3 | R3, R4 | thread `t-3` with user `hi` then assistant `hello` | the conversation is read | the retrieved lines are `[HH:MM:SS] [user] hi` then `[HH:MM:SS] [assistant] hello` (each time matches its row); reading thread `t-none` shows `(No unsummarized messages found for this thread.)` |
| T4 | R5, R9a, card 2 | papers seeded | `Find the paper on tidal memory` on `t-50` | the first model request's system message contains all five section headings and `expand_summary`; its user message starts with `# Question\nFind the paper on tidal memory\n\n## Conversation Memory`, has the five headings in the order of §5.0.2, and its Knowledge Base section's first passage starts `Tidal Memory Networks`; Workflow shows `(No relevant workflows found.)`, Entity shows `(No entities found.)`, Summary shows `(No summaries available for thread t-50.)` |
| T5 | R5 | directly written: 4 workflows (1 step each), 6 entities, 11 thread summaries for `t-k` and 1 for `t-j` | the context for `t-k` is assembled with query `anything` | the workflow section holds 3 workflows (2 `---` separators); the entity section holds 5 `•` lines; the summary section shows `Scope: thread_id = t-k` and 10 `[ID: ` lines, none of them `t-j`'s |
| T6 | R6, R6a, R14 | `big_thread` planted in `t-big` | `Hello` on `t-big` | usage before the offload is above 80; the 10 planted rows all carry one summary id; the model's user message contains `Older conversation content was summarized to reduce context size.` and `[Summary ID: <that id>] Long filler thread condensed to free context window space`, and contains no `zzzzzzzzzz`; the answer is `OK.`; the `Hello` row has no summary id. Separately, offloading the context `## Conversation Memory\nx` for thread `t-none` (no rows) returns it unchanged and creates no summary |
| T7 | R6 | — | the usage check runs on strings of `a` × 1,000,000, `a` × 819,200 and `a` × 819,816 | tokens 250,000 / percent 97.7 / offload; 204,800 / 80.0 / no offload; 204,954 / 80.1 / offload |
| T8 | R7, R8 | a fresh store with only the seven-tool set registered | the tools for query `find research papers on arxiv` are selected | exactly, in order, `search_papers`, `save_paper`, `current_time`, `convert_currency`, `weather_report`; `search_papers`' schema has property `text` of type `string`, required `["text"]`; registering `search_papers` again leaves 7 records |
| T9 | R7 | a fresh store | `fetch_and_save_paper_to_kb_db` (augmentation on) and a tool `odd_tool` (docstring "Odd helper.", augmentation on) are registered | the fetch record's description starts `Augmented: Fetch`; its `augmented` is true; its `queries` are 5 strings starting `use fetch`; the augmenter's request contained the function's source; its search text contains the description and all 5 queries; augmenter and query-generator requests each carried a completion budget of 2000; `odd_tool`'s queries are `["not json"]` |
| T10 | R3, R9, R10, R11 | papers seeded | `Find the paper on tidal memory` on `t-50` | the answer is `Found Tidal Memory Networks (arXiv 2401.00001v1) by Ada Brightwater.`; conversation rows for `t-50`: the user then the assistant message; 1 tool-log row (`arxiv_search_candidates`, status `success`, metadata iteration 1, result is JSON with one candidate whose `arxiv_id` is `2401.00001v1`); 1 workflow whose text starts `Query: Find the paper on tidal memory\nSteps:\nStep 1: arxiv_search_candidates(` and whose step ends `→ success`, with `num_steps` 1 and `success` true |
| T11 | R11, R12 | T10's run | entities are inspected; then extraction runs directly on `Ada Brightwater works at Harbor Lab.`, on `BROKEN-JSON Ada Brightwater`, on `x` × 495 + `Ada Brightwater`, and on `Ada` | after T10: entity records `Ada Brightwater` (PERSON) and `Tidal Memory Networks` (SYSTEM); direct calls: `Ada Brightwater`/PERSON and `Harbor Lab`/UNKNOWN (extractor request budget 2000); no entities; no entities, because the extractor's prompt held only the first 500 characters (it contains `Ada B` but not `Brightwater`); no entities, and the extractor was not called (shorter than 5 characters) |
| T12 | R9, R14, R15, R16, card 1 | papers seeded | on `t-50` in order: `Find the paper on tidal memory`, `Save the content of that paper`, `What are the main takeaways from the paper`, `Summarize the conversation so far using your tool`, `What was my first question?` | turn 4: the tool result is `Stored as [Summary ID: <id>] Search, save and takeaways of the Tidal Memory Networks paper` with `<id>` matching `^[0-9a-f]{8}$`; exactly 7 rows carry `<id>`; the `summarize_and_store` call had no `thread_id` in the model's arguments, but the summary record's thread id is `t-50`. Turn 5: the Conversation Memory section holds exactly one line, `[..] [assistant] Summary stored.`; the agent calls `expand_summary` with `<id>`; the tool result has `Total messages: 7`; the answer is `Your first question was: Find the paper on tidal memory` |
| T13 | R4 | thread `t-13` with 12 user messages `m01` … `m12` | the conversation is read | `m01` … `m10` in order; no `m11`, no `m12` (course behaviour, note N1) |
| T14 | R9, R11 | — | `Keep checking the time` on `t-14` | the answer is `I was unable to complete the request within the allowed iterations.`; 10 tool-log rows with iterations 1–10; 1 workflow with `num_steps` 10 and `success` true |
| T15 | R10 | `long_report` registered | `Run the long report` on `t-15` | the tool-log row's result is `L` × 5000 and its preview `L` × 2000; the tool message sent to the model is `L` × 3000 + `\n\n[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <that row's id>]`; the workflow step shows `r` × 50 followed by `...` and never 51 `r`s, while the tool-log arguments hold all 60; the answer is `Done reading.` |
| T16 | R9 | `broken_tool` and `quiet_tool` registered | `Use the missing tool`, `Use the broken tool`, `Use the quiet tool` on `t-16` | missing: result `Error: Tool 'no_such_tool' not found`, status `success`; broken: result `Error: boom`, status `failed`, error message `boom`, the step ends `→ failed`; quiet: result `Done`; answers `Could not.`, `Could not.`, `Quiet done.` |
| T17 | R13, R14 | `big_thread` planted | the thread is summarized | the summarizer's main prompt contains the transcript's first 6000 characters but not its first 6001; the stored summary record's full content is the whole transcript; the transcript's first line starts `[` + a date `YYYY-MM-DD HH:MM:SS` + `] [USER] zzz`; the summary request carried a completion budget of 4000 and the label request 2000 |
| T18 | R13 | thread `t-18`: user `EMPTY-SUMMARY-PLEASE please summarize nothing`, assistant `o` × 600 | the thread is summarized | the summarizer was called twice (main, retry); the summary starts `### Technical Information\n[`, contains `[USER] EMPTY-SUMMARY-PLEASE please summarize nothing [` (the newline became a space), and contains `Not available from model output.` three times; the line after `### Technical Information` is exactly 500 characters and ends with `o` |
| T19 | R13, R15 | — | `summarize_and_store(text="river sensor notes")`; then `summarize_and_store(text="tiny-case")` | the first reply is `Stored as [Summary ID: <id>] Budget review for the river sensor project`, and the record has no thread id; the second is `Stored as [Summary ID: <id>] Recent thread context, decisions, and open actions` |
| T20 | R14, R15 | T12's first three turns on `t-50` | `summarize_and_store(thread_id="t-50")` twice; then `summarize_and_store(thread_id="t-none")` and `summarize_and_store()` | first call: 6 messages summarized; second: `No unsummarized messages found for thread t-50.`; then `No unsummarized messages found for thread t-none.` and ``Provide `thread_id` (preferred) or non-empty `text` to summarize.`` |
| T21 | R16 | — | `expand_summary("zzzzzzzz")`; then `expand_summary("zzzzzzzz", thread_id="t-x")` | the first reply contains `## Summary Context`, `Summary zzzzzzzz not found.` and `No conversations found for summary_id: zzzzzzzz`; the second contains `Summary zzzzzzzz not found for thread t-x.` |
| T22 | R17 | fake arXiv | `arxiv_search_candidates("glacier")`; `get_current_time()`; `get_current_time(detailed=True)` | 5 candidates with ids `2402.00002v1` … `2402.00006v1` in order, each with the six fields; `2402.00002v1`'s abstract is 2500 characters; the times match `^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d$` and `^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d{6}$` |
| T23 | R17 | fake arXiv | `fetch_and_save_paper_to_kb_db("2401.00001v1")`, then `"9999.99999v9"`, then `"2402.00099v1"` | `Saved arXiv 2401.00001v1 to SEMANTIC_MEMORY: 3 chunks (title: Tidal Memory Networks).`; the knowledge base gained 3 records, each 1000 characters, with `chunk_id` 0, 1, 2, `num_chunks` 3, `source` `arxiv`, `authors` `Ada Brightwater`; then `No documents found for arXiv id: 9999.99999v9`; then `Loaded arXiv 2402.00099v1 but extracted empty text (PDF parsing issue).` |
| T24 | R18 | `papers.jsonl` | `python -m memagent seed tests/sample_data/papers.jsonl`; then a knowledge-base read for `tidal memory for agents` | 4 records stored (the empty one skipped); the first record's text is `Tidal Memory Networks\ncs.LG\nAn agent stores every conversation turn in an external tidal store and recalls it in later sessions.` with all five metadata fields; the read returns 3 records, the first being that record |
| T25 | R19 | `MEMAGENT_OFFLINE=1`, temporary `MEMAGENT_DB` | `python -m memagent ask --thread t-cli "Hello"`; then `python -m memagent ask "Hi"` | prints `OK.` and exits 0; the second call's rows are on thread `1` (the default); without a key and without offline mode, it prints the missing-key message and exits 2 |
| T26 | R11 | — | a workflow is written directly with query `q`, steps `a → success` and `b → success`, and a 250-character answer of `w`; another with steps `[]`; then workflows are read for `q` | the first's text is `Query: q\nSteps:\nStep 1: a → success\nStep 2: b → success\nAnswer: ` + `w` × 200, with `num_steps` 2; the read returns only the first (the zero-step one is filtered out) |
| L1 `live` | R9, R17, card 1 | a real key, network | T12's five turns on a fresh thread with the real model, the course embedder and real arXiv | after turn 1 an arXiv tool was called; turn 2 saves at least 1 chunk; turn 5's answer mentions the first question's wording |
| L2 `live` | R17 | network | `arxiv_search_candidates("memory augmented language model agents")` | 1–5 candidates, each with a non-empty `arxiv_id` |

**Replay notes (asserted outcomes checked against the samples):**
- **T4 / T24 (knowledge-base ranking):** T24's query tokens are `tidal`, `memory`, `agents`; T4's are `find`, `paper`, `tidal`, `memory`. In both, only the Tidal record shares tokens (`tidal` ×2, `memory`), so it ranks first.
- **T8 (tool ranking):** the query tokens are `find`, `research`, `papers`, `arxiv`. Only `search_papers` overlaps (dot product 4, cosine ≈ 0.58). The other six score 0 and keep registration order.
- **T2 / T12 / T20 (counts):** each turn writes two rows.
  - Turns 1–3 give 6 rows; turn 4's user row makes 7 at summarizing time.
  - Turn 4's assistant row is the only unsummarized row at turn 5.
  - In T20, `summarize_and_store` is called directly after three turns, so it summarizes 6 rows.
- **T23 (chunking):** two 1000-character paragraphs plus the separator make 2002 > 1500, so no merge happens. The overlap cannot carry a 1000-character piece (more than 200), so the result is 3 chunks.
- **T6 (budget):** the conversation section is about 900,600 characters, so the total is over 819,200 characters (more than 80%). After the stub the context is about 2,000 characters.
- **T7 (rounding):** 204,800 / 256,000 is exactly 80.0. 204,954 / 256,000 = 80.060…, which rounds to 80.1 (80.05 itself was avoided, because binary rounding of it is unreliable).
- **T19 (fallback label):** the first qualifying line is "Budget review for the river sensor project." It has 7 words, and the trailing `.` is trimmed.

---

## 8. Standing permissions
- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in in its own description; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build holds real data; anything that sends data to a third party beyond the chosen model provider and arXiv.
- **Never:** invent provenance (claim the course did something it did not); answer when the program should say it does not know; change sample data to make a test pass; commit secrets or a `.env` file.

---

## 9. Test plan

1. `python -m pytest -m "not live"`. Every test must run offline, with no key.
2. If `OPENAI_API_KEY` is set (or the chosen provider's key), also run `python -m pytest -m live`.
3. Report a result per test (T1–T26, L1–L2) with evidence: the test output line and the paths of the files written. "Should pass" counts as not run.
4. **Adjust for the chosen options.** Drop or adapt the tests that exist only for the recommended option, then add one test per chosen option from its "what to check" sentence (copied into `resolved-decisions.md`):
   - **C1b:** drop T22, T23, L2. Adapt T2, T4, T10–T12 and L1 to the person's own sample questions.
   - **C3b:** replace T25 with the HTTP check.
   - **C4b:** run T1–T26 against Oracle where they touch storage.
   - **C5b:** drop T5, T8, T9, T24, the knowledge-base parts of T4, T10 and T11, and T23.
   - **C6b:** replace T8.
   - **C7b/C7c:** recompute T4 and T24's ranking with the chosen scorer.
   - **C8b/C8c:** adapt T4 and T12.
   - **C9b:** adapt T12 and T21.
   - **C9c:** drop T6, T12 (turns 4–5), T17–T21.
5. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.
6. Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

---

## 10. Background notes (for the build agent)

### 10.1 The program
A tool-using agent whose memory lives outside the model, so it carries on across turns and sessions. Its stages:

```
stores → register tools → assemble context → check budget → select tools → agent loop → persist
```

- **stores:** persistent tables and vector stores, one per memory kind, so nothing depends on the process remembering.
- **register tools:** tools become searchable records (procedural memory), so the model is not handed every tool.
- **assemble context:** the program reads each memory kind and lays it out in labelled sections, because "the agent can't choose to look up what it doesn't know exists" (Lesson 3 notebook).
- **check budget:** context windows are finite, so older conversation is compressed before overflow.
- **select tools:** only the tools relevant to this request are passed.
- **agent loop:** assemble → invoke the model → act, until a final answer or the iteration limit (Lesson 6).
- **persist:** the conversation, the procedure followed (workflow) and the names seen (entities) are written back, so later turns and sessions reuse them.

The course's research-paper scenario is the recommended build's sample instance (C1a), not the program.

### 10.2 Failures
- **Stateless agent forgets earlier turns (demonstrated, Lesson 2 slides and transcript).**
  - What you see: asked to "book the first recommendation on the list", the agent replies it has no recollection of any list.
  - Why: nothing from earlier turns is stored outside the model.
  - Prevention: every turn is written to the conversation store and read back in the next turn, in any process.
  - Enforced by R2, R20; planted as the scripted reply `I have no record of which paper you mean.`; tested by T2.
- **Too many tools in the prompt (warned, Lesson 4).** The course lists context confusion, context bloat, tool-selection degradation, more latency and tokens, and performance degradation. Prevented by passing only the top 5 tools (R8, T8).
- **Context overflow (warned, Lesson 5 notebook: "Context overflow crashes the agent").** Prevented by the threshold offload (R6, T6, T7).
- **Re-summarizing processed messages (warned, Lesson 5 notebook).** Prevented by marking rows with the summary id (R14, T20).
- **Summaries lose details, and the originals cannot be reached (warned, Lesson 5 notebook and transcript).** Prevented by the four required headings (R13, T17) and expansion back to the originals (R16, T12).
- **Summarizer returns nothing (warned, Lesson 5 transcript: a fallback "so that … we will never completely lose all the context").** Prevented by the retry, then the deterministic fallback (R13, T18).
- **The loop never finishes (Lesson 6: the stop condition includes "max iteration has been reached").** Prevented by the fixed fallback answer (R9, T14).
- **Tool output bloats the context (Lesson 6 notebook).** Prevented by truncation, with the full output kept in the tool log (R10, T15).

### 10.3 Why the questions and settings are what they are
- **C1:** the course's own instance is a research assistant ("an agentic research assistant that helps users investigate complex topics over multiple sessions", Lesson 3 notebook). Lesson 7: "Take these patterns, adapt them to your own use case."
- **C2:** the course used OpenAI throughout. Provider and machine are context subjects with real situations.
- **C3:** the course had no interface beyond notebook calls. Notebooks are never offered.
- **C4:** the course used Oracle AI Database 26ai ("the database … the Agent Memory Core", Lesson 2). It needs a container, so the SQLite stand-in is recommended (4.4).
- **C5:** Lesson 2 builds the "naive memory augmented agent" with conversation memory and argues "we actually need to go beyond this". That is a stated limit, not a failure shown, so it is offered with its cost. The pattern card's owner note keeps a chat-memory-only build open.
- **C6:** Lesson 4's toolbox. Passing all tools is argued against "at scale" but never shown failing. The provider guidance appears as "~5–20" on a slide and "10-20 max" in the notebook; both are recorded.
- **C7:** Lesson 3 names lexical, vector, graph-traversal and hybrid retrieval. The transcript says hybrid search is set up for the knowledge base, but the code only defines the hybrid preference and never calls it. Vector is what ran.
- **C8:** the Lesson 3 notebook's deterministic-versus-agent-triggered table and its reasons: bootstrapping, the chicken-and-egg problem and predictability for deterministic operations; relevance, cost and judgment for agent-triggered ones. The Lesson 6 slide "Memory Ops In/Out of The Loop" shows memory reads also available inside the loop as agent calls, which grounds C8b. The pattern card's notes keep both agent-driven reading and "program does everything" open.
- **C9:** Lesson 5 contrasts context summarization ("a lossy technique") with context compaction (keep in the database with an id and a description, expand on demand). The final agent combines them (C9a).

**Subjects considered and not asked:**
- **Embedding-model choice beyond C7:** the course used one model. A model swap is a setting-like tuning with no course argument.
- **Separate on/off for workflow memory or entity memory:** that would be mix-and-match (5.6); C5's complete builds cover it.
- **Reranking retrieved memory:** it appears only in Lesson 2's general retrieval explainer and the Lesson 3 list of disciplines. No reranking part, model or argument is given for this program.
- **Graph-traversal retrieval:** named in Lesson 3, but no store here holds relationships. It needs a different program.
- **Semantic cache and persona memory:** named as memory kinds (persona only on slides). Neither is built, and neither replaces a stage.
- **The stateless agent:** it fails pattern-card item 1.
- **Unlabelled context:** no learner situation was found in which dropping the section labels is right. The course's memory-aware step is "context window segmentation".
- **The context monitor's ok/warning/critical labels** (below 50 / below 80 / otherwise; Lesson 5): they only display, and folding them into `--verbose` changes no behaviour.
- **The agent-callable toolbox search** (Lesson 4 registers it; the final agent does not): left out by 4.1.
- **The web-search tool:** see D5.

**Where picked values came from (4.2):**
- **Distance:** cosine (Lessons 3–4 code; the instructor in Lesson 3: "in this case is going to be cosine") over Euclidean (Lessons 5–6 code; the Lesson 3 notebook's key-components table). Rule 1.
- **Threshold:** the Lesson 6 transcript says both "exceeded or is equal to 80%" and "greater than 80%"; the final agent's code uses strictly greater. Rule 2.
- **Tools per request:** 5 (final agent) over 3 (toolbox read default). Rule 2.
- **Summarizer model:** gpt-5 (helper used by the final agent) over gpt-5-mini (Lesson 5 notebook). Rule 2.
- **Label fallback:** the helper's specific-line fallback (final) over the Lesson 5 notebook's `Conversation summary`. Rule 2.
- **`summarize_and_store` and `expand_summary` signatures:** the helper's (thread-aware, `text` optional), which the final agent uses. Rule 2.
- **Entity writes:** automatic (D8).
- **Toolbox embedding text:** D6.

**Notes on course code kept as-is (4.1):**
- **N1.** The conversation read returns the **oldest** 10 unsummarized messages. In a thread with more than 10, the newest turns are left out of the context until a summary clears older rows. The course's prompt text calls this memory "recent turns", but no instructor statement says which 10, so the code's behaviour is kept and T13 pins it.
- **N2.** The comparison is made on the percent after rounding to one decimal.
- **N3.** The course's code stores the augmented embedding only inside metadata, and searches on the plain docstring. The instructor explicitly says the enhanced description is what gets encoded, so this build follows the instructor (D6).
- **N4.** An unknown tool name is logged with status `success`, because the course's executor returns an error string instead of raising.
- **N5.** Workflows are always written with `success` true, even when the loop hit its limit.

### 10.4 Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports:
- `OracleVS` and `OracleVectorizerPreference` (`langchain_oracledb`)
- `DistanceStrategy` (`langchain_community.vectorstores.utils`)
- `HuggingFaceEmbeddings` (imported from both `langchain_huggingface` and `langchain_community.embeddings` in different lessons)
- `ArxivRetriever` and `ArxivLoader` (`langchain_community`)
- `RecursiveCharacterTextSplitter` (`langchain_text_splitters`)
- `OpenAI().chat.completions.create` with `tools` and `tool_choice="auto"`
- `oracledb`, `TavilyClient`, `datasets.load_dataset(..., streaming=True)`
- models `gpt-5` and `gpt-5-mini`

The course sent `max_completion_tokens`, never `max_tokens`, and never set `temperature`. The gpt-5 family rejects non-default `temperature` values, so do not send one to those models. Oracle notes for C4b: the course created vector indexes with `ORGANIZATION NEIGHBOR PARTITIONS … WITH TARGET ACCURACY 95` (IVF), chosen over HNSW to avoid several Oracle Free errors, and its user setup needed an ASSM tablespace for JSON columns.

### 10.5 Course names
| Course name | Spec term | Binding? |
|---|---|---|
| `CONVERSATIONAL_MEMORY`, `TOOL_LOG_MEMORY`, `SEMANTIC_MEMORY`, `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY` | the seven stores | yes (they appear in model-visible text) |
| `read_*` / `write_*` methods of the memory manager | store reads and writes | no |
| `call_agent` | the agent call | no |
| `arxiv_search_candidates`, `fetch_and_save_paper_to_kb_db`, `get_current_time`, `expand_summary`, `summarize_and_store` | tool names | yes (the model calls them by name) |
| `summary_id` | a conversation row's summary id | yes |
| `## Conversation Memory` … `## Summary Memory`, `# Question` | context sections | yes |
| "memory unit" | one stored record | no |

### 10.6 Lesson map
Transcript numbering decides. The notebook files' own titles are one lower than the transcript numbering, and the notebook bundle's lesson map is also misaligned.
- **Lesson 1, Introduction:** the motivation (pattern card item 1's quote).
- **Lesson 2, Why AI Agents Need Memory:** the stateless failure (§10.2), conversation memory, memory kinds, the "agent memory core" (C4, C5).
- **Lesson 3, Constructing the Memory Manager** (notebook titled "L2"): stores, schemas, cosine, the deterministic/agent-triggered table (C8), the knowledge-base loader (R18), retrieval strategies (C7).
- **Lesson 4, Scaling Agent Tool Use with Semantic Tool Memory** (notebook "L3"): toolbox, augmentation (R7, R8, D6), arXiv tools (R17), web search (D5).
- **Lesson 5, Memory Operations: Extraction, Consolidation, and Self-Updating Memory** (notebook "L4"): usage, summarization, expansion, offload (R6, R13–R16, C9). Its transcript closes "completed lesson 4".
- **Lesson 6, Memory Aware Agent** (notebook "L5"): the final end-to-end agent, which decides every stage (R5–R12). Its transcript closes "end of lesson 5".
- **Lesson 7, Conclusion.**

**Slides read:** the wide deck (Lesson 2) and the tall deck (Lessons 3–6), all talked through in the transcripts, so they count like those lessons. One wide slide (base versus instruction-tuned language models) is a leftover from a slide template and was ignored. Slide-only items count less, and where they disagree with the code they lose:
- the persona memory kind with `write_persona`/`read_persona`, not built;
- a relational workflow table with a JSON workflow document, where the code uses vector-store text plus metadata.

Nothing in this spec requires access to the course.

---

*Spec v2-draft · course: Agent Memory: Building Memory-Aware Agents · project: a memory-aware research agent (`memagent`) · when the build agent does something unexpected, add the missing constraint here and re-run.*
