# Spec: a memory-aware research agent

**What you're building:** a command-line research assistant that keeps its memory in a local database file and reads the relevant part before every answer, so you see it find a paper, save it when you later say "save the content of the paper", and still tell you your first question after the chat has been summarized, even in a new session.

**Fastest path:** at the first question, answer "recommended build". The build is done when the offline tests pass; they need no key and no network. An OpenAI key (or the provider you choose) only unlocks the `live` tests and real answers.

This file is self-contained: everything the build needs is here. Nothing in it requires access to the course.

*Provenance: course "Agent Memory: Building Memory-Aware Agents"; materials used: notebooks with their helper module and requirements file, lesson transcripts, two slide decks (images); generated 2026-10-26 with guide v2.5 (2026-10-26).*

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

## Questions

Context questions first, then the program's stages in order (open the memory stores → register tools → assemble context → shrink context → run the loop).

### C1. What should the agent help with?
- **C1a. A research assistant for papers (Recommended - course default).** It finds papers, saves their full text into its knowledge base and answers from what it saved. Pick this when you want the course's assistant working on your machine. Setup cost: none beyond the build.
- **C1b. Your own subject.** You name the subject (e.g. "remember my reading notes and the decisions in my project"), its tools and its starting documents; the paper tools and sample papers are replaced by yours. Pick this when you want the same memory-aware agent for your own work. Setup cost: you describe or write your own tools. *What to check:* your own tools are registered in the toolbox and found by tool search, and a fact you give in one session is used in an answer in a new session of the same thread.

### C2. What does the knowledge base hold at first start?
- **C2a. The sample facts in this spec (Recommended).** Six short paper records (section "Sample data", S1). Pick this when you want a quick, reproducible start. Setup cost: none.
- **C2b. A public stream of arXiv paper records (course default).** At first start, read the first 100 records of a public arXiv-paper dataset, skip records with no title, abstract and subjects, and store title + subjects + abstract as one record with arXiv id, title, subjects, abstract and submission date as metadata. Pick this when you want a realistically sized library to test retrieval. Setup cost: network access and a dataset library. *What to check:* after first start the knowledge base holds one record per non-empty paper record (at most 100), each with its arXiv id, and a second start does not load them again.
- **C2c. Your own documents.** Every text file in a folder you name becomes one or more knowledge-base records. Pick this when the agent must know your own material. Setup cost: you prepare the folder. *What to check:* every file is stored as one or more records that keep the file name, and a question about a sentence in one file gets that sentence in its Knowledge Base Memory section.

### C3. Which model provider answers?
- **C3a. OpenAI (Recommended - course default).** Pick this when you have or can get an OpenAI key. Setup cost: an OpenAI API key (paid account).
- **C3b. Another hosted provider whose models support tool calling.** Pick this when you already pay for or must use another provider. Setup cost: that provider's API key. *What to check:* one live question is answered through the chosen provider, with one tool call executed and logged in the tool log.
- **C3c. A local model served on your machine that supports tool calling.** Pick this when conversations must not leave your machine. Setup cost: a model download and hardware able to run it; smaller local models may call tools less reliably (this note is an addition, not the course's). *What to check:* the live question is answered through the local endpoint with a tool call executed, and no request goes to a hosted model API.

### C4. How do you talk to the agent?
- **C4a. Command-line chat with a thread id (Recommended).** Pick this when you use it yourself from a terminal. Setup cost: none.
- **C4b. A small local HTTP service.** One endpoint takes a thread id and a question and returns the answer. Pick this when another app or a web page will call the agent. Setup cost: one web-framework dependency. *What to check:* two requests on the same thread id — the second answer uses the first exchange — and the data is still there after the service restarts.

### C5. Where does memory live?
- **C5a. A single SQLite database file, with vector similarity computed by the program (Recommended).** Stand-in for the course's Oracle AI Database: same seven stores, same reads and writes, stored in a local file using the language's standard library. Pick this when you run on one machine with up to tens of thousands of memories. Setup cost: none.
- **C5b. Oracle AI Database with built-in vector search (course default).** Pick this when you need many users, much larger memory, built-in vector indexes and hybrid search, or you already run Oracle. Setup cost: a database container, an admin account to create the application user, and a vector memory allocation. *What to check:* the seven stores are created in Oracle on first start, are not dropped on restart, and every offline test passes against it.
- **C5c. Another database you already run that offers vector search.** Pick this when your team already operates one. Setup cost: access to that database. *What to check:* the seven stores are created there on first start, are not dropped on restart, and every offline test passes against it.

### C6. How is text turned into vectors for search?
- **C6a. A word-count embedder written in the program (Recommended).** Stand-in for the course's sentence-embedding model: each text becomes a hashed count of its words (exact rule in "Input/output contracts"). It finds memory that shares words with the query. Pick this when your questions use the same words as your stored memory, or you cannot download a model. Setup cost: none.
- **C6b. The sentence-embedding model `sentence-transformers/paraphrase-mpnet-base-v2`, run locally (course default).** Pick this when people phrase questions differently from how the memory is written. Setup cost: a model download and the libraries to run it. *What to check:* a stored passage is retrieved by a query that shares no words with it but means the same (e.g. stored "automobile repair costs", query "how much to fix a car").
- **C6c. A hosted embedding API.** Pick this when you want meaning-based search but cannot download a model. Setup cost: that provider's API key; your memory text is sent to it. *What to check:* the same no-shared-words retrieval passes, and stored vectors all have the provider's dimension.

### C7. Which outside-information tools does the agent get?
*Ask only when `C1` is `C1a`.*
- **C7a. Paper search, fetch-and-save paper, and current time (Recommended - course default).** Pick this when your questions are about research papers. Setup cost: network access for live use.
- **C7b. The same plus a web search tool that saves every result into the knowledge base.** Pick this when users ask about things papers do not cover (news, product docs). Setup cost: a web-search API key (the course used Tavily). *What to check:* each web result is written to the knowledge base with title, URL, score, query and timestamp, and a later question retrieves it from memory without searching again.
- **C7c. No outside tools; memory only.** Pick this when the agent must not reach the internet and should answer only from what is stored. Setup cost: none. *What to check:* no tool reaches the network, and a question about a stored fact is still answered.

### C8. How are tools chosen for each turn?
- **C8a. Search the toolbox with the question and offer the 5 best-matching tools (Recommended - course default).** Pick this when you have, or expect, many tools. Setup cost: none.
- **C8b. Offer every registered tool on every turn.** Pick this when you have about ten tools or fewer. Setup cost: none; the course's cost: every tool definition takes context space, and tool choice gets worse and slower as the count grows. *What to check:* every registered tool is offered to the model on every turn and the toolbox is not searched in the loop.
- **C8c. Search for the 5 best, and also let the agent search the toolbox mid-run.** The toolbox search is itself offered as a tool. Pick this when tasks often need a tool the question did not hint at. Setup cost: none. *What to check:* when the agent calls the toolbox-search tool, the tools it finds are offered on the next model call of the same turn.

### C9. How are tool descriptions prepared for search?
*Ask only when `C8` is `C8a` or `C8c`.*
- **C9a. A model rewrites the description of selected tools and adds 5 example requests (Recommended - course default).** Which tools get this is fixed per tool (R13). Pick this when tools have short descriptions that look alike. Setup cost: model calls at first registration (scripted offline).
- **C9b. Plain descriptions only.** Pick this when your tool descriptions are already detailed, or registration must make no model calls. Setup cost: none; the course's cost: tools are harder to tell apart in search. *What to check:* each tool's searchable text is its name, its plain description and its parameters, and registration makes no model call.

### C10. Which memory goes into the context before each answer?
- **C10a. Conversation, knowledge base, workflows, entities and summaries (Recommended - course default).** Pick this when the agent should reuse facts, past step sequences and named things across conversations. Setup cost: one extra model call per turn to extract entities.
- **C10b. Conversation, knowledge base and summaries only.** Pick this when you do not need past step sequences or named-entity tracking and want fewer model calls. Setup cost: none. *What to check:* the Workflow and Entity Memory sections and their stores do not exist, and a knowledge-base fact still reaches the context.
- **C10c. Conversation and summaries only.** The simplest memory-augmented agent: it only carries the chat across turns and sessions; tools that write to the knowledge base are left out. Pick this when the agent only needs to continue conversations (e.g. a support chat with no documents). Setup cost: none; the course's cost: facts outside the chat log are not kept. *What to check:* the context holds only Question, Conversation Memory and Summary Memory, and a fact from an earlier session of the same thread reaches the answer.

### C11. Which memory actions does the program run, and which does the agent decide?
- **C11a. The course's split (Recommended - course default).** The program always: reads memory before the loop, selects tools, writes every message, writes workflows, extracts entities, logs tool calls, and summarizes when the context passes 80%. The agent decides: expanding a summary, summarizing on request, and calling outside tools. Pick this when you want reliable memory with the agent judging only what needs judgment. Setup cost: none.
- **C11b. The program does everything.** No memory tool is offered to the model; Summary Memory shows each summary's full text instead of just its id; summarizing happens only by the 80% rule. Pick this when your model's tool calling is weak or every run must be predictable for audit. Setup cost: none; the course's cost: the agent cannot fetch detail a summary dropped, and full summary text uses more context. *What to check:* no memory tool is ever offered to the model, and after an automatic summary the next turn's context carries the summary text.
- **C11c. The agent reads most memory on demand.** The program loads Conversation and Summary Memory automatically; reads of the other stores kept by `C10` (knowledge base, and workflow and entity when kept) become tools the agent calls before answering; under `C10c` this option behaves like `C11a`. Pick this when your stores are large and most questions do not need them. Setup cost: none; the course's cost: the agent cannot choose to look up what it does not know exists. *What to check:* for a question needing a stored knowledge-base fact, the agent calls the knowledge-base read tool before its final answer and the fact is in the answer.

### C12. How is memory searched?
*Ask only when `C10` is `C10a` or `C10b`.*
- **C12a. Vector similarity (Recommended - course default).** Pick this when questions and memory are plain prose. Setup cost: none.
- **C12b. Hybrid: keyword search and vector similarity combined, for the knowledge base.** Pick this when your documents contain exact codes, ids or names that similarity search misses. Setup cost: a keyword index next to the vectors. *What to check:* a query made only of an exact identifier (e.g. "2401.00001v1") returns the record holding it first.
- **C12c. Vector similarity plus graph traversal over entity relationships.** Entities are stored with their relationships, and a read follows links from the entities the question names. Pick this when questions follow links between people, projects or systems ("who worked with the author of that paper?"). Setup cost: storing relationships and a traversal step. *What to check:* after "Ines Varga co-wrote Tidal Memory Networks with Tomas Reyes", the question "who wrote with Ines Varga?" gets Tomas Reyes in Entity Memory.

### C13. Re-rank retrieved memory?
*Ask only when `C10` is `C10a` or `C10b`.*
- **C13a. No re-ranking (Recommended - course default).** Pick this when the top results by similarity are usually right. Setup cost: none.
- **C13b. Fetch more candidates and re-order them with a re-ranking model, then keep the usual count.** Pick this when your memory has many near-duplicate passages. Setup cost: a re-ranking model download or API key. *What to check:* each read fetches more candidates than its count, re-orders them with the re-ranker, and keeps the configured count.

### C14. What happens when the conversation gets too long?
- **C14a. Summarize, keep the originals, expand on demand (Recommended - course default).** Old messages get a summary with an id; the originals stay stored and marked; the agent can expand a summary back into the original messages. Pick this when exact earlier details may matter later. Setup cost: model calls when summarizing.
- **C14b. Summarize and keep only the summary.** Pick this when you must not keep raw chat (retention rules) or storage is tight. Setup cost: model calls when summarizing; the course's cost: summarizing always loses some information, and nothing can bring it back. *What to check:* after summarizing, the source messages are deleted, the summary appears in Summary Memory in a new session, and no expand tool exists.
- **C14c. No shrinking.** Pick this when conversations stay short and your model's context window is large. Setup cost: none; the course's cost: long conversations fill the context window. *What to check:* no summary store or summary tools exist, and a 12-message thread still answers.

### C15. What happens to large tool outputs?
- **C15a. Save every full output in the tool log; give the model at most 3,000 characters (Recommended - course default).** Pick this when tools can return long text (papers, search results) or you want an audit trail. Setup cost: none.
- **C15b. Give the model the full output; keep no tool log.** Pick this when your tools return short outputs and you need no audit trail. Setup cost: none; the course's cost: large outputs crowd the context. *What to check:* tool results reach the model in full and no tool-log store exists.

---

## Departures from the course

| # | Where | Recommended build | Course | Why |
|---|---|---|---|---|
| D1 | Memory database (C5) | SQLite file, similarity computed by the program — **stand-in** | Oracle AI Database 26ai in a container, vector store integration | Course choice needs container and admin setup (4.4). |
| D2 | Embedder (C6) | Hashed word-count embedder — **stand-in** | `sentence-transformers/paraphrase-mpnet-base-v2` (768 dims) | Large model download (4.4). |
| D3 | Model in tests | Scripted model — **stand-in** — offline; real provider when a key is present | OpenAI models | Needs a key (4.6). |
| D4 | Startup | Stores are created if missing and **never dropped at startup**; an explicit `reset` command clears them | Every lesson drops all seven tables before starting | Pattern card item 1: memory must survive the session. The drop exists so each lesson starts clean. |
| D5 | Knowledge base content | Six sample records written for this spec | First 100 records streamed from a public arXiv-paper dataset | Sample data must be self-written and reproducible (4.5). |
| D6 | Paper tools in tests | Scripted paper source — **stand-in**; real arXiv in `live` tests | Live arXiv API | Offline tests (7.3). |
| D7 | Web search tool | Left out (offered as C7b) | Built in Lesson 4 with Tavily; not registered in the final agent | Needs a key, and the final agent did not use it (4.1, 4.4). |
| D8 | Vector distance | Cosine | Cosine when introduced (Lesson 3); Euclidean in the Lesson 5 and Lesson 6 notebooks | Value rule 4.2 (1): the instructor states cosine when introducing it. |
| D9 | Summary length limit | The stored summary is at most 6,000 characters; the summarizer receives the whole transcript | Code sends only the first 6,000 characters of the transcript to the summarizer | 4.1: the instructor says the limit is on the final summary. |
| D10 | Tool search text | Searchable text = name + model-written description + parameters + 5 example requests | Code computes that text but stores the original description as the searched text | 4.1: the instructor and notebook say the enriched text is what gets embedded. |
| D11 | Vector index | None; exact similarity over all rows | IVF vector index, target accuracy 95 (HNSW described, IVF used to avoid database errors) | Not needed at sample scale with SQLite. |
| D12 | Interface | Command-line program | Functions called from notebook cells | A notebook is never the build (guide 3.4). |
| D13 | Context budget | One setting, 256,000 tokens, for whichever agent model is chosen | A table keyed by model name (256,000 for its two models), 128,000 for any other name | The build agent picks a current model name the table would not know. |

---

## Objective

Build an agent that keeps every kind of memory in persistent storage outside the model, puts the memory relevant to each request into the model's context before it answers, and writes back what each turn produced, so it carries on across turns and sessions.

## Tech stack and versions

- **Language:** Python 3 (current release; the course did not pin a Python version).
- **Recommended build dependencies:** standard library only for storage (`sqlite3`), hashing, JSON and ids; the `openai` client for live model calls; the `arxiv` package and a PDF-to-text library (the course installed `arxiv` and `pymupdf`) for live paper tools; `pytest` for tests (addition). The course left every package unpinned; use current releases and do not invent pins.
- **Package layout:** an importable package named `memory_agent`, run as `python -m memory_agent`.
- **Secrets:** read `OPENAI_API_KEY` (or the chosen provider's key) from the environment or a `.env` file; never write keys to the database, logs or repository.
- **Environment switches (addition):** `MEMORY_AGENT_DB` (database file path; default `memory_agent.db`), `MEMORY_AGENT_MODEL=scripted` (use the scripted model and scripted paper source; tests set it).

## Input/output contracts

### Command line (C4a)
- `python -m memory_agent ask --thread <id> "<question>"` → prints the final answer on the last line of output; exit code 0.
- `python -m memory_agent chat --thread <id>` → reads questions line by line until `exit`; prints each answer.
- `python -m memory_agent reset` → asks for confirmation, then empties all seven stores (addition: the course had no reset command; see D4).
- Each `ask` is a new process: all memory comes from the database file.

### Stores (names are binding; they appear in model-visible text)
| Store | Kind | Contents |
|---|---|---|
| `CONVERSATIONAL_MEMORY` | table | one row per message |
| `TOOL_LOG_MEMORY` | table | one row per tool call |
| `SEMANTIC_MEMORY` | vector store | knowledge base records |
| `WORKFLOW_MEMORY` | vector store | completed task step sequences |
| `TOOLBOX_MEMORY` | vector store | tool definitions |
| `ENTITY_MEMORY` | vector store | named people, places, systems |
| `SUMMARY_MEMORY` | vector store | summaries with their originals |

A vector-store record is `{id, text, embedding, metadata}`; the embedding is computed from `text`. Vector reads always return up to `k` nearest records by cosine similarity, with no score threshold, ties broken by earlier insertion; an optional metadata filter is applied before ranking.

Conversation row:
```json
{"type":"object","required":["id","thread_id","role","content","timestamp","summary_id"],
 "properties":{"id":{"type":"string"},"thread_id":{"type":"string","maxLength":100},
 "role":{"enum":["user","assistant"]},"content":{"type":"string","minLength":0},
 "timestamp":{"type":"string","format":"date-time","description":"microsecond precision; ties ordered by insertion"},
 "metadata":{"type":"string","default":"{}"},"created_at":{"type":"string","format":"date-time"},
 "summary_id":{"type":["string","null"],"pattern":"^[0-9a-f]{8}$","default":null}}}
```

Tool-log row:
```json
{"type":"object","required":["id","thread_id","tool_name","status","timestamp"],
 "properties":{"id":{"type":"string"},"thread_id":{"type":"string"},"tool_call_id":{"type":["string","null"]},
 "tool_name":{"type":"string"},"tool_args":{"type":"string","description":"JSON text"},
 "result":{"type":"string","description":"full output"},
 "result_preview":{"type":"string","description":"result cut to at most 2000 UTF-8 bytes, never splitting a character"},
 "status":{"enum":["success","failed"]},"error_message":{"type":["string","null"]},
 "metadata":{"type":"string","description":"JSON text holding {\"iteration\": n}"},"timestamp":{"type":"string","format":"date-time"}}}
```

Vector-store metadata:
- Knowledge base: free metadata per source (sample: `arxiv_id`, `title`, `subjects`; saved paper chunk: `source`="arxiv", `arxiv_id`, `title`, `entry_id`, `published`, `authors`, `chunk_id` 0..N-1, `num_chunks` N, `ingested_ts_utc`).
- Workflow: text `Query: <query>\nSteps:\nStep 1: <step>\n…\nAnswer: <first 200 characters of the final answer>`; metadata `{query, success, num_steps, timestamp}`.
- Toolbox: text = the searchable text (R13); metadata `{name, description, signature, parameters, return_type, augmented, queries?}` where `parameters` maps each parameter name to `{name, type?, default?}`.
- Entity: text `<name> (<TYPE>): <description>`; metadata `{name, type, description}`; TYPE is one of PERSON, PLACE, SYSTEM (or UNKNOWN when the extractor gives none).
- Summary: text `<summary_id>: <description>`; metadata `{id, full_content, summary, description, thread_id?}`.

Tool schema offered to the model:
```json
{"type":"function","function":{"name":"<tool name>","description":"<stored description>",
 "parameters":{"type":"object","properties":{"<param>":{"type":"string|integer|number|boolean"}},"required":["<params without a default>"]}}}
```
Parameter type mapping: text → string, whole number → integer, decimal → number, true/false → boolean, anything else or missing → string.

### Embedder stand-in (C6a)
Lowercase the text; take runs of `[a-z0-9]`; keep tokens of 3+ characters that are not in this stop list: `the and for with that this are was you your from what which can use used how does into its has have about`. Each token adds 1 to dimension `int(first 8 hex digits of MD5(token), 16) mod 512`. Normalize to length 1 (an empty text gives the zero vector, similarity 0). This is a **stand-in** for the course's sentence-embedding model.

### Memory section text (binding headings; the offload step and the system prompt rely on them)
The context sent to the model is `# Question\n<question>\n\n` followed by these sections in this order, separated by blank lines. Each section has a heading, `### What this memory is`, `### How you should leverage it` (2–4 short guidance lines in the spirit given), and its retrieved content:
1. `## Conversation Memory` — chronological unsummarized messages of this thread; guidance: keep continuity, resolve references like "the paper above", prefer the latest user direction. Lines `[HH:MM:SS] [<role>] <content>`. Empty: `(No unsummarized messages found for this thread.)`
2. `## Knowledge Base Memory` — retrieved passages, one per line block; guidance: ground factual claims, state uncertainty when evidence is missing. Empty: `(No relevant knowledge base passages found.)`
3. `## Workflow Memory` — past step sequences joined by `\n---\n`; guidance: reuse and adapt, do not copy blindly. Empty: `(No relevant workflows found.)`
4. `## Entity Memory` — lines `• <name>: <description>`; guidance: disambiguate, keep naming consistent. Empty: `(No entities found.)`
5. `## Summary Memory` — when summaries exist: `Use expand_summary(id) to retrieve the detailed underlying conversation.`, `Scope: thread_id = <id>`, then lines `  • [ID: <summary_id>] <description>`; guidance: call expand_summary(id) before relying on exact details. Empty: `(No summaries available for thread <id>.)`

### Model roles
| Role | What it does | Course model |
|---|---|---|
| agent | reasons, calls tools, answers | `gpt-5-mini` |
| summarizer | writes a conversation summary | `gpt-5` (final agent); `gpt-5-mini` (Lesson 5 notebook) |
| labeller | writes an 8–12 word label for a summary | same as summarizer |
| entity_extractor | lists people, places, systems in a text | `gpt-5` |
| tool_describer | rewrites a tool description; writes 5 example requests | `gpt-5` |

### Settings
| Setting | Value | Source | Change this when … |
|---|---|---|---|
| Conversation messages read per turn | 10 (oldest unsummarized first) | final agent default; Lesson 5 test used 100 | you want a longer visible history |
| Knowledge base passages per read | 3 | memory manager default | answers need more passages |
| Workflows per read | 3, only those with ≥1 step | memory manager | — |
| Entities per read | 5 | memory manager | — |
| Summaries listed per read | 10, this thread only | memory manager | — |
| Tools offered per turn (C8a) | 5 | final agent loop | your tasks need more tools per turn |
| Context budget | 256,000 tokens | final agent and Lesson 5 (both models 256,000) | your model's window differs |
| Token estimate | characters ÷ 4, rounded down | Lesson 5 ("we're going to use this estimation as four characters per token") | your provider gives a token counter |
| Summarize when usage is | above 80% (strictly greater) | Lesson 5/6 transcripts and code | — |
| Max loop iterations | 10 | final agent | long multi-tool tasks |
| Tool result given to the model | first 3,000 characters + truncation note | final agent | — |
| Tool-log preview | 2,000 UTF-8 bytes | tool-log store | — |
| Summary length cap | 6,000 characters | Lesson 5 transcript (D9) | — |
| Retry prompt length | ≤ 180 words | summarizer | — |
| Fallback excerpt | first 500 characters | summarizer | — |
| Label length | 8–12 words; fallback first 12 words | summarizer | — |
| Summary id | first 8 characters of a random UUID: `^[0-9a-f]{8}$` | summarizer | — |
| Entity extraction input | first 500 characters; skip texts under 5 characters | memory manager | — |
| Workflow answer excerpt | 200 characters | memory manager | — |
| Step argument display | string values over 50 characters cut to 50 + `...` | final agent | — |
| Paper search | at most 8 fetched, 4,000 characters each (live source only), `k` default 5, abstract cut to 2,500 | Lesson 4 / common tools | — |
| Paper chunking | 1,500 characters, 200 overlap | Lesson 4 / common tools | your embedder's input limit differs |
| Example requests per augmented tool | 5 | toolbox | — |
| Vector distance | cosine | Lesson 3 transcript (D8) | — |
| Max output tokens per call (live only; the scripted model ignores it) | summarizer 4,000; retry 4,000; labeller 2,000; entity 2,000; tool_describer 2,000; agent unset | course code | your provider's limits differ |

---

## Business rules

### What must stay true (pattern card, owner-confirmed)
**The one kind of program:** a tool-using agent whose memory lives outside the model, so it carries on across turns and sessions.

1. **Memory lives outside the model and survives the session.** What the agent learns in one turn or session is stored in persistent storage and is available to later turns and new sessions; nothing depends on the model or the process remembering it. (L1: "treating long-term memory as first-class infrastructure, external to the model, persistent and structured." L2: "Turn 1 and 2 in a Memory-Augmented Agent would have been stored in an external memory source such as a database.") → R2, tests T02, T03, T36.
2. **Before the model answers, the memory relevant to the request reaches its context.** (L6: "At a start condition, when we are about to enter the Agent Loop, we typically would have memory operations that read from memory. This is because we're assembling context for our LLMs.") → R6, test T10.

Every option above keeps both items.

### Rules
- **R1. Stores on a fresh start.** Starting the program on a new database file creates all seven stores, empty. → T01
- **R2. Memory persists.** Startup creates missing stores and never drops or empties existing ones; only `reset` empties them. Everything written in one process is readable by the next. → T02, T03, T36
- **R3. Conversation memory.** Every user and assistant message is stored with thread id, role, content, timestamp and an empty summary id. A read returns this thread's messages whose summary id is empty, oldest first, and keeps the first 10 (course behavior — see the note below). → T04, T05
- **R4. Context assembly.** Before the loop, the program builds the five sections in order (Conversation, Knowledge Base, Workflow, Entity, Summary), using the question as the search query for the vector reads and this thread for the conversation and summary reads; the question is prepended under `# Question` and is never summarized. The user's message is stored only after the context is built, then entities are extracted from the question. → T06, T34
- **R5. Vector reads.** Knowledge base k=3, workflow k=3 limited to workflows with at least one step, entity k=5, summary list k=10 limited to this thread, cosine similarity over the embedder in "Input/output contracts". → T07, T08, T09, T29, T30
- **R6. Relevant memory reaches the model.** The model's first call in a turn receives the assembled context; an answer that depends on a stored fact can only come from that context or a tool result. → T10, L1
- **R7. Context budget.** Usage = (characters of the memory sections ÷ 4, rounded down) ÷ 256,000 × 100, rounded to one decimal. If usage is above 80, the program summarizes this thread's unsummarized messages (R8), replaces the whole Conversation Memory section with the stub `## Conversation Memory` / `Older conversation content was summarized to reduce context size.` / `Use Summary Memory references + expand_summary(id) for full detail.`, keeps the other sections, and appends `[Summary ID: <id>] <description>` at the end (adding a `## Summary Memory` section with `Use expand_summary(id) to retrieve full underlying content.` if none exists). → T11
- **R8. Summarizing a thread.** Read this thread's unsummarized messages oldest first, build a transcript of lines `[YYYY-MM-DD HH:MM:SS] [ROLE] <content>`, summarize it (R9) with the thread id, then set the summary id on exactly those messages and no others. With no unsummarized messages, the result is "nothing to summarize" and nothing is written. → T12, T13
- **R9. Summary generation.** The summarizer is asked for a summary under exactly the headings `### Technical Information`, `### Emotional Context`, `### Entities & References`, `### Action Items & Decisions`, keeping concrete details (names, dates, APIs, errors, decisions), separating confirmed facts from open questions, inventing nothing, concise. If its reply is empty, ask once more for at most 180 words under the same headings; if still empty, use a fixed summary: the first 500 characters of the transcript (newlines as spaces) under Technical Information and `Not available from model output.` under the other three. The stored summary is cut to 6,000 characters. The labeller is asked for a specific 8–12 word label, not a generic one; if it returns empty or one of "conversation summary", "summary", "chat summary", "thread summary" (any case), the label is the first 12 words of the first summary line that is not a heading and has at least 4 words (bullet marks and trailing `,.;:` removed), else `Recent thread context, decisions, and open actions`. The summary is stored with a new id, the full original text, the summary, the label and the thread id. → T14, T15, T16, T17
- **R10. Expanding a summary.** `expand_summary(summary_id, thread_id?)` returns `## Summary Context`, the stored summary text, then `## Expanded Conversations for Summary ID: <id>`, `Total messages: <n>`, and each original message as `[YYYY-MM-DD HH:MM:SS] [ROLE]` followed by its content, oldest first. Unknown id: `Summary <id> not found.` (or `… not found for thread <t>.` when a thread is given) and `No conversations found for summary_id: <id>`. → T18, T34
- **R11. Summarize tool.** `summarize_and_store(text="", thread_id=None)`: in the loop the program fills in the current thread id when the model omits it. With a thread id: summarize the thread (R8) and return `Stored as [Summary ID: <id>] <label>`, or `No unsummarized messages found for thread <id>.`. Without a thread id and with text: summarize the text (no thread id stored) and return the same `Stored as …` form. With neither: `Provide `thread_id` (preferred) or non-empty `text` to summarize.` → T19, T20, T34
- **R12. Toolbox registration.** Registering a tool stores its name, description, signature, parameters (with type and default when given) and return type. If a tool of that name is already stored, nothing new is written but the tool stays callable. Reading returns tool schemas (contract above), one per tool name; parameters without a default are required. → T21, T22
- **R13. Tool search text.** Augmented tools (`fetch_and_save_paper_to_kb_db`, `expand_summary`, `summarize_and_store`) get a description rewritten by the tool_describer (one-line summary, steps, when to call, caveats) and 5 example requests; their searchable text is `<name> <rewritten description> (<signature>) <the 5 requests joined by spaces>` and their stored description is the rewritten one. Plain tools (`arxiv_search_candidates`, `get_current_time`) have searchable text `<name> <description> (<signature>)`. Each turn, the program offers the model the 5 tools whose searchable text best matches the question. → T23, T24
- **R14. The loop.** Up to 10 model calls per turn. If the reply has tool calls, each is executed in order and its result is sent back as a tool message; then the model is called again. If the reply has no tool call, its text is the final answer. After 10 calls without a final answer, the answer is `I was unable to complete the request within the allowed iterations.` An unknown tool returns `Error: Tool '<name>' not found` (status success — course behavior, see note). A tool that raises gives `Error: <message>` with status failed. An empty tool result becomes `Done`. Each executed call adds a step `<tool>(<args>) → success|failed`, where `<args>` is the arguments as JSON with `, ` and `: ` separators, keys in the order given, string values over 50 characters cut to 50 characters plus `...`. → T25, T26, T27, L1
- **R15. Tool log and truncation.** Every executed tool call is logged with thread id, call id, tool name, arguments, full result, preview, status, error message and `{"iteration": n}`. If the result is over 3,000 characters, the model gets its first 3,000 characters followed by `\n\n[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <log id>]`; otherwise the full result. → T28
- **R16. Write-back after the loop.** If the turn had at least one step, store a workflow (format above) with success true and the number of steps; extract and store entities from the final answer; store the final answer as an assistant message. → T29, T30, T34
- **R17. Entity extraction.** Texts under 5 characters are skipped. The extractor sees the first 500 characters and must return a JSON list of `{name, type, description}`; the program takes the outermost `[...]` in the reply, keeps items with a name, and stores each. Any extraction error stores nothing and never stops the turn. → T31
- **R18. Paper tools.** `arxiv_search_candidates(query, k=5)` returns a JSON list of at most k candidates `{arxiv_id, entry_id, title, authors, published, abstract}` with the abstract cut to 2,500 characters and `arxiv_id` taken from the entry id after `/abs/`. `fetch_and_save_paper_to_kb_db(arxiv_id, chunk_size=1500, chunk_overlap=200)` loads the full text, splits it into chunks of at most 1,500 characters (split on paragraph breaks, then line breaks, then spaces; each chunk starts with up to 200 characters of the previous chunk's end), stores each chunk in the knowledge base with the chunk metadata above, and returns `Saved arXiv <id> to SEMANTIC_MEMORY: <n> chunks (title: <title>).`; no paper: `No documents found for arXiv id: <id>`; empty text: `Loaded arXiv <id> but extracted empty text (PDF parsing issue).` `get_current_time(detailed=False)` returns `YYYY-MM-DD HH:MM:SS` (with microseconds when detailed). → T32, T33, L2, L3
- **R19. Continuity across turns.** Within one thread, later turns use earlier ones: references like "the paper" resolve from Conversation Memory, past steps appear in Workflow Memory, and after a summary the agent expands it to answer about summarized turns. → T34
- **R20. System prompt.** The model's system message says: it is a memory-aware research assistant with tools; the user message is a partitioned context with a `# Question` and the five named sections, each a distinct memory store with the purposes above; if a needed detail is only in Summary Memory or is ambiguous, call `expand_summary(summary_id)` first; start from the memory sections before using tools; on conflict prefer `# Question` > latest Conversation Memory > Knowledge Base evidence > older summaries/workflows; use only the tools offered this turn, with the fewest calls; if memory is insufficient, say what is missing, then use a tool; for compaction use `summarize_and_store` with the thread id. → T35
- **R21. Command line.** The commands in "Input/output contracts" behave as stated; each `ask` is a fresh process. → T36

**Note for the build agent (course behavior kept, 4.1):** the course's conversation read sorts oldest first and keeps the first 10, so in a thread with more than 10 unsummarized messages the newest ones are not shown, even though its guidance text calls them "recent". The course's unknown-tool path returns an error text without raising, so it is logged as success. Workflows are always stored with success true. Keep all three; they are tested as written.

---

## Tests

### Sample data (define before any test)
All sample data lives in `tests/sample_data/`. It is written for this spec; none of it is course data.

- **S1 `knowledge_base.json`** — six records `{text, metadata}`, loaded at first start under C2a, in this order:
  - K1 `Title: Tidal Memory Networks\nSubjects: cs.LG\nAbstract: Tidal Memory Networks store agent episodes in a ring buffer of 512 slots and replay them during planning.` — `{arxiv_id: "2401.00001v1", title: "Tidal Memory Networks", subjects: "cs.LG"}`
  - K2 `Title: Lantern Retrieval for Long Documents\nSubjects: cs.IR\nAbstract: Lantern retrieval splits long documents into overlapping windows and ranks windows with a lexical prefilter.`
  - K3 `Title: Orchard Planning with Sparse Rewards\nSubjects: cs.AI\nAbstract: Orchard planners grow a search tree whose branches are pruned when rewards stay below a threshold of 0.2.`
  - K4 `Title: Glacier Embeddings for Slow-Changing Text\nSubjects: cs.CL\nAbstract: Glacier embeddings are refreshed monthly and reduce index rebuilds by 40 percent.`
  - K5 `Title: Kestrel Scheduling of Tool Calls\nSubjects: cs.DC\nAbstract: Kestrel batches tool calls from many agents and cuts median latency to 85 milliseconds.`
  - K6 `Title: Meadow Benchmarks for Dialogue Recall\nSubjects: cs.CL\nAbstract: Meadow measures whether a dialogue system recalls user facts after 20 turns.`
  (K2–K6 metadata: their title and subjects, arxiv_id `2401.0000Nv1` for N = 2..6 — note K2's id `2401.00002v1` is also the empty-text paper in S2.)
- **S2 `paper_source.json` — scripted paper source (stand-in for arXiv).** Search returns, in listed order, every paper whose title or abstract shares an embedder token with the query, at most k. Fetch returns the paper's full text by arxiv id.
  - P1 `2401.00001v1`, entry id `http://arxiv.org/abs/2401.00001v1`, title `Tidal Memory Networks`, authors `Ines Varga, Tomas Reyes`, published `2024-01-02`, abstract = K1's abstract sentence. Full text: 30 lines joined by `\n`, line i (01..30) = `Line {i:02d}: Tidal Memory Networks section {i:02d} discusses ring buffer replay and recall in long agent episodes.` (105 characters each; 3,179 in total).
  - S-1 `2402.00011v1` `A Survey of Agent Recall Stores`; S-2 `2402.00012v1` `A Survey of Context Compaction`; S-3 `2402.00013v1` `A Survey of Tool Retrieval`; authors `Mara Quist`, published `2024-02-01`. Abstract = `<title> abstract. ` followed by `This survey filler sentence repeats to pad the abstract. ` repeated, cut to 2,000 characters for S-1 and S-2 and 3,000 for S-3. Not fetchable.
  - `2401.00002v1` fetch returns empty full text. `0000.00000v0` fetch raises an error with message `network unavailable`. Any other id: no paper.
- **S3 `scripted_model.json` — scripted model (stand-in for every model role).** The program's model calls go to it when `MEMORY_AGENT_MODEL=scripted`. Per role:
  - **agent** — looks at the `# Question` text (case-insensitive) and the messages so far; "after a tool" means the last message is a tool result. First matching rule wins:
    1. contains `loop forever` → always call `get_current_time` with `{}`.
    2. contains `find the paper on tidal memory networks` → before a tool: call `arxiv_search_candidates` `{"query":"tidal memory networks"}`; after: answer `I found Tidal Memory Networks (arXiv 2401.00001v1) by Ines Varga and Tomas Reyes.`
    3. contains `save the content of the paper` → if Conversation Memory contains `arXiv <id>` (id like `2401.00001v1`): before a tool call `fetch_and_save_paper_to_kb_db` `{"arxiv_id":"<id>"}`, after answer `Saved arXiv <id> to the knowledge base.`; if no id: answer `Which paper do you mean?`
    4. contains `summarize the conversation` → before a tool: call `summarize_and_store` with `{}`; after: answer `Stored the summary.`
    5. contains `what was my first question` → if Summary Memory contains `[ID: <8 hex>]`: before a tool call `expand_summary` `{"summary_id":"<first id>"}`, after answer `Your first question was: <the line after the first line ending in [USER] in the tool result>`; else if Conversation Memory has a `[user]` line answer `Your first question was: <its content>`; else `I don't know based on my memory.`
    6. contains `list survey papers` → before: `arxiv_search_candidates` `{"query":"survey","k":5}`; after: answer `Found 3 survey papers: A Survey of Agent Recall Stores (2402.00011v1), A Survey of Context Compaction (2402.00012v1), and A Survey of Tool Retrieval (2402.00013v1). Each covers a different part of memory-aware agents and is worth reading in that order.` (252 characters).
    7. contains `search with a long query` → before: `arxiv_search_candidates` `{"query":"<q repeated 60 times>"}`; after: answer `No results.`
    8. contains `fetch the broken paper` → before: `fetch_and_save_paper_to_kb_db` `{"arxiv_id":"0000.00000v0"}`; after: `The fetch failed.`
    9. contains `call a missing tool` → before: call `teleport` `{}`; after: `Done.`
    10. contains `ring buffer` → if Knowledge Base Memory contains `ring buffer of <n> slots`: answer `Tidal Memory Networks use a ring buffer of <n> slots.`; else `I don't know based on my memory.`
    11. contains `what do i study` → if Conversation Memory contains `I study <x>.`: answer `You study <x>.`; else `I don't know based on my memory.`
    12. contains `my name is` → answer `Noted.`
    13. otherwise → `I don't know based on my memory.`
  - **summarizer** — mode `standard` (used unless a test sets another mode) replies:
    `### Technical Information\nDiscussed Tidal Memory Networks (arXiv 2401.00001v1) and saved it to the knowledge base.\n\n### Emotional Context\nNeutral, task-focused.\n\n### Entities & References\nTidal Memory Networks; Ines Varga; Tomas Reyes.\n\n### Action Items & Decisions\nRead the saved paper.`
    Mode `long`: 7,000 `a` characters. Mode `empty`: empty every time. Mode `empty-once`: empty, then the standard reply.
  - **labeller** — mode `standard`: `Tidal Memory Networks paper search and saving session` (8 words). Mode `generic`: `Conversation summary`.
  - **entity_extractor** — replies a JSON list containing `{"name":"Tidal Memory Networks","type":"SYSTEM","description":"memory architecture from a research paper"}` when the text contains `tidal memory networks` (any case) and `{"name":"Ines Varga","type":"PERSON","description":"paper author"}` when it contains `Ines Varga`; otherwise `[]`. Mode `garbage`: `not json`. It records the text it received.
  - **tool_describer** — description request: `AUGMENTED <original description> Use when: <tool name with underscores as spaces>.`; example-request request: a JSON list of 5 strings `please <tool name with spaces> (1)` … `(5)`.
- **S4 tool descriptions (binding plain descriptions and signatures).** `arxiv_search_candidates` "Search arXiv and return a JSON list of candidate papers with IDs and metadata." `(query: str, k: int = 5)`; `fetch_and_save_paper_to_kb_db` "Fetch full arXiv paper text and store it into the knowledge base as chunked records." `(arxiv_id: str, chunk_size: int = 1500, chunk_overlap: int = 200)`; `get_current_time` "Returns the current time." `(detailed: bool = False)`; `expand_summary` "Expand a summary reference to retrieve the original conversations." `(summary_id: str, thread_id: str = None)`; `summarize_and_store` "Summarize content and store it in Summary Memory." `(text: str = '', thread_id: str = None)`. Registered in that order.
- **S5 decoy tools** (registered only in T24, plain): `convert_celsius_to_fahrenheit` "Convert a temperature from Celsius to Fahrenheit." `(celsius: float)`; `count_words` "Count the words in a piece of text." `(text: str)`; `roll_dice` "Roll a six-sided die and return the result." `()`; `reverse_string` "Reverse the characters of a string." `(text: str)`; `add_numbers` "Add two numbers together." `(a: float, b: float)`; `random_color` "Pick a random color name." `()`.
- **S6 session script (planted failure: a stateless agent forgets between sessions).** Process A, thread `t-200`: `My name is Ines and I study glacier embeddings.` Process B (new process, same database file): `What do I study?`. A stateless agent answers `I don't know based on my memory.`; this build must answer `You study glacier embeddings.`
- **S7 overflow thread.** Thread `t-300` with 10 stored messages, roles alternating user/assistant, each the text `overflow filler ` repeated and cut to 90,000 characters.

Every test runs with `MEMORY_AGENT_MODEL=scripted`, a fresh temporary database file (unless the test says otherwise), the sample knowledge base S1 loaded, the S4 tools registered, and all settings at their defaults.

### Test table
| Test | Rules | Given / When / Then |
|---|---|---|
| T01 | R1 | Given a new database file. When the program starts. Then the seven stores named in the contract exist; all are empty except `SEMANTIC_MEMORY` (6 records from S1) and `TOOLBOX_MEMORY` (5 tools). |
| T02 | R2 | Given a database with one conversation message and one summary. When the program starts again (new process). Then both are still there and no store was emptied; after `reset` (confirmed) all seven stores are empty. |
| T03 | R2 | Given S6. When process A runs its question and process B runs its question. Then A answers `Noted.` and B answers `You study glacier embeddings.`; the same question on thread `t-201` answers `I don't know based on my memory.` |
| T04 | R3 | Given thread `t-1` with messages m01..m03 written in order. When conversation memory is read for `t-1`. Then the section lists m01, m02, m03 in order as `[HH:MM:SS] [user|assistant] <content>`; for thread `t-2` it shows `(No unsummarized messages found for this thread.)` |
| T05 | R3 | Given thread `t-3` with 12 messages m01..m12. When conversation memory is read. Then exactly m01..m10 appear (course behavior, see note). |
| T06 | R4 | Given an empty thread `t-4`. When `ask` "Hello" runs. Then the context sent to the model starts with `# Question\nHello`, then the five section headings in order, the Conversation section shows the empty text (the question is not in it), and after the turn the thread holds the user message then the assistant message. |
| T07 | R5 | Given the embedder stand-in. When it embeds the same text twice, and an empty text. Then the vectors are equal, of length 512 and unit length; the empty text gives similarity 0 with anything. |
| T08 | R5 | Given S1. When the knowledge base is read with `glacier embeddings refresh`. Then 3 passages are returned and the first is K4. |
| T09 | R5 | Given 12 summaries stored for thread `t-5` and 1 for `t-6`. When the summary list is read for `t-5`. Then exactly 10 `[ID: …]` lines appear, `Scope: thread_id = t-5` is shown, and the `t-6` summary is absent; for an unused thread it shows `(No summaries available for thread <id>.)` |
| T10 | R6 | Given S1. When `ask` thread `t-400` "What ring buffer size do tidal memory networks use?". Then the first model call's context has K1 first in Knowledge Base Memory and the answer is `Tidal Memory Networks use a ring buffer of 512 slots.` Given an empty knowledge base, the same question answers `I don't know based on my memory.` |
| T11 | R7 | Given S7. When `ask` thread `t-300` "Hello after the long chat". Then usage before shrinking is above 80 (about 88), all 10 stored messages get one summary id, the summarizer received a transcript of at least 900,000 characters, the context sent to the model contains `Older conversation content was summarized to reduce context size.` and `[Summary ID: <id>] Tidal Memory Networks paper search and saving session`, contains no `overflow filler`, usage after shrinking is below 5, and the answer is `I don't know based on my memory.` |
| T12 | R8 | Given thread `t-7` with 3 messages and thread `t-8` with 2. When thread `t-7` is summarized. Then the 3 `t-7` rows carry one id matching `^[0-9a-f]{8}$`, the `t-8` rows have none, and the summary store holds that id with thread `t-7`. |
| T13 | R8 | Given T12's end state. When `t-7` is summarized again. Then the result is "nothing to summarize", no summary is added, and conversation memory for `t-7` shows `(No unsummarized messages found for this thread.)` |
| T14 | R9 | Given T12. Then the summarizer's prompt names the four headings, the stored summary equals the standard reply, the stored full content equals the transcript, and the labeller's prompt asks for an 8-12 word label. |
| T15 | R9 | Given summarizer mode `long`. When a thread is summarized. Then the stored summary is exactly 6,000 characters. |
| T16 | R9 | Given summarizer mode `empty-once`, then mode `empty`. When a thread is summarized each time. Then the first makes 2 summarizer calls, the second prompt contains `180 words`, and the standard summary is stored; the second stores a summary starting `### Technical Information\n` followed by the transcript's first 500 characters (newlines as spaces) and containing `Not available from model output.` three times. |
| T17 | R9 | Given labeller mode `generic`. When a thread is summarized. Then the label is `Discussed Tidal Memory Networks (arXiv 2401.00001v1) and saved it to the knowledge`. |
| T18 | R10 | Given T12. When `expand_summary(<id>)` runs. Then the output starts `## Summary Context`, contains the standard summary, `## Expanded Conversations for Summary ID: <id>`, `Total messages: 3`, and the three messages oldest first each under `[YYYY-MM-DD HH:MM:SS] [USER]` or `[ASSISTANT]`. `expand_summary("abcd1234")` contains `Summary abcd1234 not found.` and `No conversations found for summary_id: abcd1234`. |
| T19 | R11 | Given thread `t-700` holding one stored user message `Earlier note.`. When `ask` thread `t-700` "Summarize the conversation so far using your tool". Then the model calls `summarize_and_store` with `{}`, the program runs it for `t-700`, exactly 2 messages (the earlier note and this question) get the new summary id, the summary is stored with thread `t-700`, and the answer is `Stored the summary.` |
| T20 | R11 | When `summarize_and_store()` is called with no arguments, then with `text="Some notes about glacier embeddings."`, then with `thread_id="t-999"` (empty thread). Then the results are `Provide `thread_id` (preferred) or non-empty `text` to summarize.`, `Stored as [Summary ID: <id>] Tidal Memory Networks paper search and saving session` with no thread id stored, and `No unsummarized messages found for thread t-999.` |
| T21 | R12 | Given S4 registered. When the toolbox is read with any query and k=5. Then 5 distinct schemas return; `fetch_and_save_paper_to_kb_db` has properties `arxiv_id` string, `chunk_size` integer, `chunk_overlap` integer and required `["arxiv_id"]`; `get_current_time` has `detailed` boolean and required `[]`; `expand_summary` requires `["summary_id"]`; `summarize_and_store` requires `[]`. |
| T22 | R12 | Given T21. When the program restarts and registers S4 again. Then `TOOLBOX_MEMORY` still holds 5 records and all 5 tools still execute. |
| T23 | R13 | Given S4 registered on a fresh database. Then the tool_describer was called for exactly the 3 augmented tools; their stored descriptions start `AUGMENTED ` and their metadata holds 5 example requests. Toolbox reads with k=1 return: `fetch and save the full paper text` → `fetch_and_save_paper_to_kb_db`; `expand a summary reference` → `expand_summary`; `what is the current time` → `get_current_time`; `search arxiv for candidate papers` → `arxiv_search_candidates`; `summarize the conversation and store it` → `summarize_and_store`. |
| T24 | R13 | Given S4 and S5 registered (11 tools). When `ask` "fetch and save the full paper text" runs. Then the model is offered exactly 5 tools, `fetch_and_save_paper_to_kb_db` first and `count_words` among them. |
| T25 | R14 | When `ask` thread `t-500` "loop forever". Then the model is called 10 times, `get_current_time` runs 10 times, the answer is `I was unable to complete the request within the allowed iterations.`, the tool log holds 10 rows for `t-500` with iterations 1..10, and one workflow with 10 steps is stored. |
| T26 | R14 | When `ask` "call a missing tool". Then the tool message is `Error: Tool 'teleport' not found`, the log row has status `success`, and the answer is `Done.` |
| T27 | R14 | When `ask` "fetch the broken paper". Then the tool message is `Error: network unavailable`, the log row has status `failed` and error message `network unavailable`, the workflow step ends `→ failed`, and the answer is `The fetch failed.` |
| T28 | R15 | When `ask` "list survey papers". Then the logged result is the full JSON (over 3,000 characters, three candidates, S-3's abstract 2,500 characters), its preview is at most 2,000 bytes, and the tool message is the first 3,000 characters plus `\n\n[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <that row's id>]`. |
| T29 | R16, R5 | Given T28. Then one workflow is stored: `Query: list survey papers\nSteps:\nStep 1: arxiv_search_candidates({"query": "survey", "k": 5}) → success\nAnswer: ` + the first 200 characters of the answer, metadata num_steps 1, success true. `ask` "Hello" stores no workflow. `ask` "search with a long query" stores a step whose query shows 50 `q` then `...`. A 0-step workflow written directly never appears in Workflow Memory. Given 4 workflows with steps stored, a workflow read returns exactly 3, separated by `---`. |
| T30 | R16, R5 | Given T34 turn 1. Then `ENTITY_MEMORY` holds 3 records (Tidal Memory Networks from the question; Tidal Memory Networks and Ines Varga from the answer). Given 7 entities stored, an entity read returns 5 lines. |
| T31 | R17 | When entities are extracted from an 800-character text, from `hi`, and with extractor mode `garbage`. Then the extractor received at most the first 500 characters; for `hi` it was not called; with `garbage` nothing is stored and no error surfaces. |
| T32 | R18 | When `arxiv_search_candidates("tidal memory networks")` and `("survey", k=2)` run. Then the first returns a JSON list of 1 item with arxiv_id `2401.00001v1`, entry_id, title, authors `Ines Varga, Tomas Reyes`, published `2024-01-02`, abstract; the second returns 2 items, S-1 and S-2. |
| T33 | R18 | When `fetch_and_save_paper_to_kb_db("2401.00001v1")` runs. Then N ≥ 3 chunks are stored, each at most 1,500 characters, every one of the 30 lines appears whole in some chunk, each chunk after the first begins with at most 200 characters repeated from the end of the previous chunk, chunk metadata has `source` "arxiv", chunk_id 0..N-1 and num_chunks N, and it returns `Saved arXiv 2401.00001v1 to SEMANTIC_MEMORY: <N> chunks (title: Tidal Memory Networks).` `9999.99999v9` returns `No documents found for arXiv id: 9999.99999v9`; `2401.00002v1` returns `Loaded arXiv 2401.00002v1 but extracted empty text (PDF parsing issue).` |
| T34 | R4, R10, R11, R16, R19 | Thread `t-100`, four `ask` runs, each a new process. Turn 1 "Can you find the paper on tidal memory networks?" → Knowledge Base Memory lists K1 first; answer `I found Tidal Memory Networks (arXiv 2401.00001v1) by Ines Varga and Tomas Reyes.` Turn 2 "Can you save the content of the paper?" → context Conversation Memory holds turn 1, Workflow Memory contains `Step 1: arxiv_search_candidates`, Entity Memory contains `• Ines Varga: paper author`; the paper is saved; answer `Saved arXiv 2401.00001v1 to the knowledge base.` Turn 3 "Summarize the conversation so far using your tool" → `summarize_and_store` runs for `t-100`, marks exactly 5 messages; answer `Stored the summary.` Turn 4 "What was my first question?" → Conversation Memory shows only `Stored the summary.`, Summary Memory lists one id with label `Tidal Memory Networks paper search and saving session`, Workflow Memory shows the 3 workflows of turns 1–3; the model calls `expand_summary`; answer `Your first question was: Can you find the paper on tidal memory networks?` |
| T35 | R20 | When any turn runs. Then the system message names all five section headings, the `expand_summary` policy, the priority order `# Question` > latest Conversation Memory > Knowledge Base evidence > older summaries/workflows, and `summarize_and_store` with the thread id. |
| T36 | R21, R2 | With `MEMORY_AGENT_DB` set to a temporary file: `python -m memory_agent ask --thread t-600 "My name is Ines and I study glacier embeddings."` prints `Noted.`; a second invocation with "What do I study?" prints `You study glacier embeddings.`; both exit 0. |
| L1 `live` | R14, R6 | With a provider key: `ask` "What ring buffer size do tidal memory networks use?" returns an answer containing `512`, and the conversation store holds both messages. |
| L2 `live` | R18 | With network: `arxiv_search_candidates("retrieval augmented generation", k=3)` returns 1–3 candidates with non-empty arxiv ids. |
| L3 `live` | R18 | With network: fetching the first L2 candidate stores ≥ 1 chunk, each at most 1,500 characters. |

---

## Standing permissions

- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in in code comments and docs; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has stored data; anything that sends data to a third party (including a hosted model or embedding API beyond the chosen provider).
- **Never:** invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets; drop stores at startup.

---

## Test plan

1. Offline: `MEMORY_AGENT_MODEL=scripted python -m pytest -m "not live"` — must pass with no key and no network.
2. Live (only when a key and network are present): `python -m pytest -m live`.
3. Report one result per test (T01–T36, L1–L3) with evidence: the test output line and any file paths it created. "Should pass" counts as not run.
4. Adjust the recommended tests for the chosen options: drop tests that exist only for an option not chosen (e.g. T28 under C15b, T11–T20 under C14c), and for each chosen non-recommended option turn its "what to check" sentence into a test and report it.
5. The build is finished when the adjusted recommended tests pass and each chosen option's check passes.
6. Finish with a diagram of the built app introduced by the sentence "This is the infra/structure diagram of this app".

---

## Background notes

### The program and its stages
A tool-using agent whose memory lives outside the model.
`open stores → register tools → assemble context → shrink context → select tools → store question → reason and act → write back`
- **Open stores** — memory must be outside the model and survive the process (card item 1).
- **Register tools** — tools are kept as searchable memory so only relevant ones reach the model (Lesson 4).
- **Assemble context** — the relevant memory must reach the model before it answers (card item 2); sections are labelled so the model knows each store's purpose (Lesson 3 "memory aware" steps, Lesson 6).
- **Shrink context** — keeps the window from filling while keeping a way back to detail (Lesson 5).
- **Select tools** — fewer, relevant tools per turn (Lesson 4).
- **Store question** — the user message becomes conversation memory; entities are pulled out of it.
- **Reason and act** — the agent loop: call the model, run tools, return results, stop on a final answer or the iteration cap (Lesson 6).
- **Write back** — conversation, workflow and entities are saved so later turns reuse them (Lesson 6).

### Failures
- **F1. The stateless agent forgets (demonstrated, Lesson 2 transcript and slides).** You see: in a later turn the agent says it has no recollection of the list it gave and asks you to specify. Why: nothing outside the model holds earlier turns. Prevention: every message is stored and read back each turn, and stores are never dropped at startup. Enforced by R2, R3; planted in S6; tested by T03, T36.
- **F2. Re-summarizing already summarized messages (warned, Lesson 5 notebook).** You see: the same messages summarized again and again. Why: messages are not marked after summarizing. Prevention: exactly the summarized rows get the summary id; reads and summaries skip marked rows. R8; T12, T13.
- **F3. Context overflow (warned, Lesson 5).** You see: the request fails or detail is crowded out as history grows. Prevention: usage check above 80% triggers summarizing. R7; T11.
- **F4. Too many tools in the prompt (warned, Lesson 4).** You see: context confusion and bloat, worse tool choice, more tokens and latency. Prevention: tools retrieved by search, 5 per turn. R13; T24.
- **F5. Large tool outputs in the prompt (warned, Lesson 6).** Prevention: full output to the tool log, 3,000 characters to the model. R15; T28.

### Why the questions and settings are what they are
- **C5 storage / C6 embedder:** the course's agent memory core is a database ("this is where you're going to see the most traffic of data", Lesson 2); any database that stores and searches the seven stores keeps the pattern. The stand-ins avoid container setup and a model download.
- **C8 tools:** the course argues stuffing all tools fails at scale; the notebook says providers recommend limiting tools (often 10–20), the slides say ~5–20 — recorded disagreement; neither is used as a value. Lesson 4 also exposed toolbox search as an agent tool ("allows the agent to autonomously query for tools mid-execution"); the final agent did not — hence C8c.
- **C9 augmentation:** "this is a great idea, but it might not be enough" — the course adds model-written descriptions for higher separability and recall (Lesson 4).
- **C10 memory kinds:** the course goes from a naive agent with conversation memory to the full set ("conversation windows are finite… agents need structured, queryable knowledge, not just chat logs", Lesson 2) — a cost, not a failure, so the simpler builds are offered.
- **C11 who triggers:** the course's table and arguments (Lesson 3 notebook): deterministic reads because "the agent can't choose to look up what it doesn't know exists"; deterministic writes for reliability and completeness; agent-triggered actions for relevance and cost. The table marks `write_entity` agent-triggered and `read_toolbox` both; the final agent runs entity writes automatically and does not offer toolbox search — the final version decides (4.1). The Lesson 6 slide also shows reads inside the loop as agent operations, supporting C11c.
- **C12 retrieval:** Lesson 3 lists "text or lexical, vector, Graph Traversal, or hybrid" strategies; the course set up a hybrid-search preference for the knowledge base but never used it.
- **C13 re-ranking:** the Lesson 2 RAG pipeline passes retrieved rows through a re-ranking model; the course's agent never re-ranks.
- **C14 shrinking:** summarization "will always be a lossy technique"; compaction offloads to the database with an id and description and expands on demand (Lesson 5). The course's code combines both; C14b is the lossy side alone.
- **C15 tool outputs:** "move some of the tool logs outside of the agent loop and into the database. This is context offloading" (Lesson 6).
- **Not questions:** the context-usage status labels (ok under 50%, warning under 80%, critical otherwise) are a display tool, not a stage. Semantic cache, working memory, persona memory and the procedural/semantic/episodic taxonomy are other memory forms the course names but this program does not build; persona memory appears only on one slide. Database admin setup, retry on connection failure and vector-memory cleanup helpers are course infrastructure. The test model is never asked (tests always run on the scripted model).
- **Values and how they were picked (4.2):** distance — cosine (Lesson 3 transcript, rule 1) over Euclidean (final notebooks). Summary model — `gpt-5` (final agent's helper, rule 2) over `gpt-5-mini` (Lesson 5 notebook). Summary 6,000 limit — on the summary (Lesson 5 transcript, rule 1) over input truncation (code). Toolbox k — 5 in the final loop; the toolbox read's own default is 3 and its tool description says 5. Conversation read — 10 (final loop) over 100 (Lesson 5 test). Token budget — 256,000 for both course models; 128,000 for unknown names (D13). The course drops all stores at each lesson start; the final helper's table creation reuses existing tables (D4).
- **Course's own run (for orientation, not tests):** its Lesson 6 demo summarized seven messages; its Lesson 5 test thread had 30 messages (the transcript says 32) and measured about 2,000 tokens, under 1%.

### Names that go stale
Treat these as search keywords against current docs, not guaranteed imports: `OracleVS`, `langchain_oracledb`, `OracleVectorizerPreference`, `DistanceStrategy`, `HuggingFaceEmbeddings` (imported from both `langchain_huggingface` and `langchain_community`), `sentence-transformers/paraphrase-mpnet-base-v2`, `ArxivRetriever`, `ArxivLoader`, `RecursiveCharacterTextSplitter`, `TavilyClient`, `datasets.load_dataset` (streaming), OpenAI Chat Completions with `tools` and `tool_choice="auto"`, models `gpt-5` and `gpt-5-mini`, Oracle AI Database 26ai / Oracle Free. Request limits implied by the era: the course passes `max_completion_tokens` (not `max_tokens`) and never sets `temperature`; assume these model families may reject a non-default temperature and check current docs (this caution is an addition).

### Course names
| Course name | Spec term |
|---|---|
| `CONVERSATIONAL_MEMORY`, `SEMANTIC_MEMORY`, `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY`, `TOOL_LOG_MEMORY` | the seven stores (binding) |
| MemoryManager / StoreManager | the program's memory read/write layer (no class design required) |
| Toolbox, `register_tool(augment=…)` | tool registration (R12, R13) |
| `call_agent(query, thread_id, max_iterations)` | one `ask` turn |
| `summarize_conversation`, `summarise_context_window`, `offload_to_summary`, `summarize_and_store`, `expand_summary` | R8, R9, R7, R11, R10 (tool names binding) |
| `arxiv_search_candidates`, `fetch_and_save_paper_to_kb_db`, `get_current_time` | paper and time tools (names binding) |
| `## Conversation Memory` … `## Summary Memory`, `# Question`, `[Summary ID: …]` | binding context text |
| ArxivScout, agentic research assistant | the sample instance |

### Lesson map
Transcript numbering decides (W2). The notebooks are named one number lower than their lesson.
- **L1 Introduction** — the problem (stateless agents), memory as external, persistent infrastructure; card item 1.
- **L2 Why AI Agents Need Memory** — stateless vs memory-augmented agents (F1), conversational memory and its limits (C10), memory forms, RAG pipeline with re-ranking (C13), agent memory core. Wide slide deck (talked through) read with this lesson; its last slide is a leftover template about base vs instruction-tuned models and was ignored.
- **L3 Constructing the Memory Manager** (notebook "L2") — stores and their schemas, cosine distance (D8), deterministic vs agent-triggered table (C11), memory-aware agent steps, retrieval strategies (C12), knowledge-base ingest from an arXiv dataset (C2b, D5). Tall-deck slides for this lesson read; the "Common Memory Operations" slide adds a Persona store found nowhere else — slide-only, it loses.
- **L4 Scaling Agent Tool Use with Semantic Tool Memory** (notebook "L3") — tool retrieval (C8), augmentation (C9, D10), Tavily search-and-store (C7b, D7), paper tools (R18). Tall-deck slides read; "~5–20 tools" disagrees with the notebook's "10–20" (recorded, unused).
- **L5 Memory Operations: Extraction, Consolidation, and Self-Updating Memory** (notebook "L4") — context usage, summarize/compact/expand (C14, R7–R11), workflow memory. Tall-deck slides read; a slide shows a workflow table with a JSON document column — the code stores workflows as vector-store text, and code wins. The transcript ends "lesson 4" (internal miscount).
- **L6 Memory Aware Agent** (notebook "L5") — the final end-to-end agent loop (R4, R14–R16, R20), in/out-of-loop operations, the four-turn demo that T34 mirrors with sample data. Tall-deck slides read. The transcript ends "lesson 5" (internal miscount).
- **L7 Conclusion** — recap only.

Nothing in this spec requires access to the course.

---

*Spec v2-draft · Agent Memory: Building Memory-Aware Agents · spec-build-lab · When the build agent does something unexpected, add the missing constraint here and re-run.*
