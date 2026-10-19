# Spec: Memory-Aware Research Assistant Agent — Standalone Takeaway

> **What you're building:** a command-line research assistant agent that remembers its conversations across sessions. You ask it a question in a thread, ask a follow-up that only makes sense with the earlier turn, quit and start it again, ask it to summarize the conversation with its tool, then ask what your first question was — and you watch it expand the stored summary to answer. Answering the gate's first question with the recommended baseline build builds it end to end; the build is COMPLETE when the offline acceptance suite passes — API keys unlock only the `live` tests and live use of the finished agent.
>
> This file is self-contained: the embedded Course Context Pack replaces every external course reference, and nothing here requires course-platform access. (CTX-X) anchors mark course-derived knowledge. The Decision Ledger below holds every point where the build could diverge, each pinned to one course-derived default, so the spec builds as-is with no intake.
>
> Generated from the "Agent Memory: Building Memory-Aware Agents" notebooks + transcripts on 2026-10-20, guide @ 5caba53.

## 0. Before you build — REQUIRED (do this first)

You are the build agent. Before writing ANY code, you MUST surface the design decisions
in the Decision Ledger (next section) to the person you are building for. Do **not** skip
this because the defaults look complete — the defaults exist so the build is *reproducible*,
not because they are the right choice for this person's project.

1. **Use a structured question tool if you have one.** If your environment offers an
   interactive structured-question tool (e.g. Claude Code's `AskUserQuestion`, or the equivalent
   in yours), you MUST use it for the questions below — do not paraphrase them into a prose
   paragraph. Only if no such tool exists, list the rows in your reply and ask the user to
   respond to each.
2. **First question — recommended baseline build, or customize?** Ask exactly one question with
   two options: the **recommended baseline build** — every Ledger row resolves to its Default:
   mostly the course's own choices, with a lighter stand-in wherever the course's choice needs
   setup you may not have (a paid API key, an admin-provisioned service); the step-5 checklist
   marks exactly where the baseline differs from the course — or **customize** the decisions row
   by row. If the user chooses the baseline, skip step 3 — go straight to the step-5 checklist
   and build. If the user chooses customize, continue with step 3.
3. **Present the Ledger ONE ROW AT A TIME — one question per row.** For each row ask a single
   question: the **Decision** as the prompt, its **Options** as the choices. Append
   "(course default)" to the option the course actually used — on a substitution row that is
   the course-faithful Options entry, not the Ledger Default. Append "(Recommended)" to the
   row's Default — the option the recommended baseline build takes, chosen when this spec was
   written as the most efficient way to build the course's pattern; say once, before presenting
   the first Ledger row, that it does not reflect this person's setup. When the Default IS the course's
   actual choice, merge the labels into "(Recommended - course default)". "(Recommended)" never
   removes or moves the "(course default)" label, and no option is ever
   labeled with a bare "(default)" — these two labels and their merged form are the only
   option labels. Use the answers already given (project, data, goal, …) to frame
   later questions and describe options in the person's own terms — but never drop or alter an
   Option or move the "(course default)" label because of an earlier answer, and never skip a row
   because an earlier answer seems to make it irrelevant. The only skip: a row whose Decision
   says "Applies only when `<row>` is `<id>`" is skipped when the answer on that row is none of
   those ids, or that row was itself skipped. Say so in one line (e.g. "<row> is skipped: it applies
   only when <row> is <id>; <row> = <answer>") and go on to the next row — a skip resolves that row
   only. If the person changes an earlier answer, re-check every condition that names it. Put
   any realizations beyond the tool's option slots (or the free-form case) under the tool's
   "Other"/free-text. Ask about every row that is not skipped this way. A per-call item limit is NEVER a reason to drop,
   skip, merge, or silently default a row — make as many separate calls as there are rows.
4. **Presenting any of these questions ENDS YOUR TURN — stop here; write no code, create or edit
   no file, take no other build action.** Keep asking, one row at a time, until **every** row is
   resolved — answered (a chosen option, an explicit "use the course default", or the step-2
   baseline answer, which answers every row at once) or skipped by its own condition (step 3). Answers to *some* rows do NOT release the build; "no reply
   yet" is not an answer — wait for the user.
5. **Before the first line of code, print a resolved-decision checklist and write it to
   `resolved-decisions.md`** — every Ledger row with its final value (the chosen option's id and
   text — the user's choice, or its Ledger default), each line carrying a deviation mark: `= course choice`, or
   `≠ course choice (course used: <option>)`, or `no course choice` on a row where the course
   made no choice (the scope boundary), or — on a row skipped by its condition, with no value —
   `not applicable (applies only when <row> is <id>; <row> = <answer>)`. If the build calls a language model, add one line per
   model role the chosen options use, naming the current model you will use from the Default
   provider — one you know that provider serves; if you cannot tell, say so and ask the person
   to name one, and if they do not, use the course's own model id from this spec for that role
   and say it may need changing. A missing model name never blocks confirming the checklist.
   For every chosen option that is not its row's Default, copy its line from §7's "Tests by
   option" table into the checklist, so the criteria and Ledger cells this build retires or
   changes are recorded before the first line of code. The file records what this build was built from;
   nothing reads it back — a later build re-runs this gate. If the baseline path was chosen,
   walk the person through every `≠` row — the course's actual choice, and why this build's
   default substitutes it (the row's Trade-off/branch note says why) — before building. Begin
   implementation ONLY after this checklist is shown, written, and confirmed by the person; if
   any row is unresolved you are not done — return to step 3. A `not applicable` line whose
   quoted condition is not false is unresolved. Build on the checklist's values. Leave out
   every part of this spec that exists only for a rule a chosen option retires — its commands,
   flags, settings, schema fields, fixtures and permission items. Where a chosen option changes
   a criterion and its §7 line does not fully state the new form, adapt the criterion to the
   chosen options and list it, with what you changed, under *Adapted* in the checklist and in
   your final report.

Model roles this build uses (for the step-5 model lines): **agent** (the tool-calling loop), **summarizer** (summary, retry and label requests), **entity extractor**, **tool augmenter** (description rewrite and example-query generation). The course ran the agent role on `gpt-5-mini` and the other roles on `gpt-5` in its end-to-end code (CTX-D).

## Decision Ledger (§0 above requires the build agent to present these before building)

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L1 | learner | **Project** — what you are building. The default is the course's example realization (its research-assistant use case), expected to be swapped when your project differs. | | L1a. Branch: the course's example scenario shape, re-expressed on facts authored in this spec. | L1a — a command-line research assistant agent that remembers its conversations across sessions and works with research papers (Recommended - course default); L1b — an assistant for your own domain on the same memory pattern: your tools, your seed data, the same memory core and agent loop | Swapping the project re-points the tools, the seed data and the role line of the system prompt; the memory pattern itself is unchanged. The course frames every lab as an "agentic research assistant" over arXiv papers (Lessons 3–6). | learner |
| L2 | learner | **Data / inputs** — what the agent's knowledge base starts with. | | L2a. Branch: the learner data row defaults to the synthetic corpus so the build runs offline on facts authored here; the course's dataset stays an option. | L2a — the synthetic fixture paper corpus in §5 (five invented paper records), ingested into the knowledge base by the `seed` command (Recommended); L2b — the first 100 records streamed from the public Hugging Face dataset `nick007x/arxiv-papers` (course default — needs a network download through the datasets library; no key); L2c — your own document records, one record per document | The course seeded its knowledge base with 100 streamed arXiv records (title, subjects, abstract, submission date; Lesson 3). Changing seed data after ingestion means re-seeding. | learner |
| L3 | learner | **Goal** — what "working" means. | | L3a | L3a — in one thread you can ask a follow-up that depends on an earlier turn, stop and restart the program, and still get answers that use the earlier turns, including details recovered from summarized conversation (Recommended - course default); L3b — a goal you state at the gate (what retrieval must find, what answers must guarantee); the build adds criteria for it and keeps the rest | L3a is the course's closing demo (Lesson 6: fetch a paper, save it, ask for takeaways, summarize, ask "what was my first question?"). | learner |
| L4 | learner | **Model / provider** for live use of the agent. | A chat model with native tool calling: it returns structured tool-call requests and accepts tool results in the next request. | L4a | L4a — OpenAI Chat Completions with tool calling (Recommended - course default — needs an OpenAI API key for live use); L4b — Anthropic Messages API with tool use (needs an Anthropic API key); L4c — a local open-weights model behind an OpenAI-compatible endpoint with tool calling (heavy setup: a local model server and hardware able to run it) | The course used OpenAI's client for every model role (Lessons 4–6). Another provider changes the tool-call message format, not the memory pattern. The offline suite never calls a live model (row RR3). | course+learner |
| L5 | learner | **Environment** — where it runs. | Memory survives process restarts: a new process opened on the same data location sees everything earlier processes wrote. | L5a | L5a — a local command-line program on your machine with a file-backed database (Recommended); L5b — Jupyter notebook cells that call the agent once per question, as the course ran it (course default) | The course ran in hosted notebooks and dropped its tables at the start of each lesson; persistence across sessions is the course's stated purpose (Lessons 1, 2, 6), so this spec keeps data between runs. | course+learner |
| L6 | learner | **Scope boundary** — present the full "Not Included" list from §1 inside this question, item by item with its handling tag, then ask whether to keep it as-is or bring something back. | | L6a | L6a — keep every §1 exclusion as written (Recommended); L6b — bring one or more §1 items back: name them in free text, and each is handled by its tag in §1 | The course made no choice here; each §1 item says whether it is restorable, buildable without criteria, owned by another row, or unavailable. | learner |
| D1 | design-argued | **Memory-core topology** — which memory stores the agent keeps in its database. | Memory lives in a database outside the model; conversation history is stored per thread with timestamps and read back in time order. | D1a | D1a — seven stores: conversational and tool-log tables, plus knowledge-base, workflow, toolbox, entity and summary vector stores (Recommended - course default); D1b — conversational memory only: the thread's interaction history in the database, and every registered tool offered on every turn (shown in the course; no code shipped) | Lesson 2 shows a memory-augmented agent with conversational memory alone completing a follow-up the stateless agent could not ("book the first one on the list"), then argues it is a naive form: conversation windows are finite, valuable information spans conversations, and agents need structured, queryable knowledge and workflow outcomes, not just chat logs. Litmus: shown working and weighed (the working branch), so a row. Lesson 3 builds the seven stores. | course+learner |
| D2 | design-argued | **Tool-description augmentation** — whether a tool's stored description is rewritten by the model at registration. Applies only when `D1` is `D1a`. | Each tool is found by similarity between the turn's question and the tool's stored retrieval text; registering a tool name twice stores it once. | D2a. The current-time tool is plain, following the end-to-end agent's registration (value branch 2); the Lesson 4 notebook augmented it. | D2a — per tool, as the course's end-to-end agent registers them: the summarize, summary-expansion and toolbox-search tools augmented; each of the course's tools, or of those row L1's answer brings, augmented or plain as the §5 toolbox criteria mark it (Recommended - course default); D2b — every tool augmented; D2c — no tool augmented: each tool's retrieval text is its name, its own docstring and its signature | Lesson 4: augmentation (the "memory unit augmentation") gives better separability between tools in embedding space, higher recall and "high-signal embedding text", at the cost of two model calls per tool at registration; plain registration is shown working (the arXiv candidate-search tool, registered plain, is retrieved and called in the Lesson 6 demo). Litmus: both sides shown working, so a row. Contradiction carried here: Lesson 4's narration and notebook say the enriched text is what gets embedded, while the course's registration code stores the vector of the name + original docstring + signature and keeps the enriched text only as the description; this spec follows the narration. Changing the choice after tools exist means clearing the toolbox store, because registration skips names already stored. | course+learner |
| D3 | design-argued | **Memory-operation trigger split** — which memory operations the harness runs on every turn and which the model calls as tools. Applies only when `D1` is `D1a`. | Bootstrap reads of memory and the writing of each turn's messages run on every turn without the model choosing them. | D3a | D3a — the course's split: on every turn the harness reads conversation, knowledge-base, workflow, entity and summary-list memory, selects tools, offloads at the context threshold, and writes the turn's messages, its workflow and the entities it extracts; the model calls summarization, summary expansion, toolbox search and the paper tools (Recommended - course default); D3b — as D3a, except entity writing becomes a tool the model calls instead of a per-turn extraction (the course's operation table classifies it this way; the course never built it, and this spec supplies no parameters and no acceptance criteria for it); D3c — as D3a, except summarization runs only when the model calls its tool: no automatic offload at the context threshold | Lesson 3 (narration and notebook) argues deterministic operations for predictability, reliability, completeness and less model bookkeeping, and agent-triggered ones for relevance, cost and latency control and judgment. Bake-ins (tie-breaker 1, a warned failure): bootstrap reads — without them "the agent behaves stateless", and it "can't choose to look up what it doesn't know exists" — and conversation and workflow writes — the agent may "forget to save". D3c: Lesson 6 shows the agent calling its summarize tool successfully, and calls summarization "both a deterministic and an agent-triggered memory operation" (working branch). D3b: argued, never built, and it moves an operation's owner (structural), so it is an option that says so. Contradiction carried here: the operation table marks entity writing agent-triggered and toolbox search both; the end-to-end agent extracts entities every turn and registers no toolbox-search tool, which the Lesson 4 notebook does register; D3a takes the code's entity extraction and Lesson 4's toolbox-search tool. | course+learner |
| D4 | design-structural | **Context-reduction guarantee** — whether reduced conversation stays recoverable. Applies only when `D1` is `D1a`. | Context reduction replaces only conversation content; the current question and the other memory segments pass through unchanged. | D4a | D4a — recoverable compaction: a summary with an ID and short label replaces the conversation in context, the original messages stay in the database linked to that ID, and the model can expand them on demand (Recommended - course default); D4b — lossy summarization: the summary text replaces the conversation and the originals are not kept retrievable (the course described this and never built it; this spec supplies no parameters and no acceptance criteria for it) | Lesson 5 argues context summarization "will always be a lossy technique", while context compaction moves content into the database under an ID with a description so the model can pull the detail back. The lossy side was never shown working; the subject changes a guarantee (reversibility), so it is a row with a never-built option (the never-shown branch on a structural subject). | course+learner |
| RR1 | realization | **Memory-core database** — which database realizes the stores. | One persistent database holds every store D1's answer keeps. Its relational stores support exact match on thread id and time ordering, and updating each row's summary link where the answers on rows D1 and D4 keep one. Each vector store D1's answer keeps holds text, JSON metadata and an embedding per record, and returns the top k records by similarity with metadata filters (equality and greater-than). Contents survive process restarts. | RR1a. Branch: substitution — the course teaches the memory-core pattern ("the agent memory core would be your database", Lesson 2) that its database realizes; the course is not about that product. Lightest tier that meets the invariant: tier 1 (ships with Python) — exact in-process similarity over fixture-scale data meets the contract, so no index is needed; indexed realizations stay in Options. | RR1a — an embedded SQLite database file through Python's standard-library `sqlite3`, each vector store D1's answer keeps holding its embeddings beside text and metadata, similarity computed exactly in-process (Recommended); RR1b — Oracle AI Database 26ai Free with LangChain's Oracle vector-store integration and an IVF vector index for each vector store D1's answer keeps (course default — heavy setup: a local database container, an admin account to create a database user with an ASSM default tablespace, and the `oracledb` driver); RR1c — PostgreSQL with the pgvector extension, run locally (heavy setup: a database server you install and administer) | The course ran Oracle AI Database 26ai in a local container, with SQL tables for conversation and tool logs and one Oracle vector table per vector store, plus IVF indexes (target accuracy 95) because its helper reports that HNSW indexes fail on some Oracle Free versions (ORA-00600, ORA-51928, ORA-51962). Moving stores after data exists is a migration. | course+learner |
| RR2 | realization | **Web-search tool** — whether the agent has a keyed web-search tool. Applies only when `D1` is `D1a`. | Any search tool writes each result it returns into the knowledge base with its source metadata, so later turns can retrieve it without searching again. | RR2a. Branch: the keyed-tool rule — the keyed tool is not the only carrier of a taught behavior (the keyless paper-fetch tool also writes what it finds into the knowledge base), so it is left out by default. | RR2a — no web-search tool; the keyless tools — the course's tools, or those row L1's answer brings — carry search-and-store (Recommended); RR2b — Tavily web search writing each result into the knowledge base (course default — heavy setup: a Tavily API key; registered in the Lesson 4 notebook, absent from the course's end-to-end agent); RR2c — a local stand-in, named and described as a fake web search, returning two fixed results and writing them into the knowledge base | Lesson 4 teaches search-and-store with Tavily: results are persisted so "future queries can retrieve this information without searching again". The course's end-to-end agent (Lesson 6) registers only the arXiv, time and summary tools. | course+learner |
| RR3 | realization | **Acceptance-suite model** — which model the offline acceptance suite runs against. | The suite drives the real pipeline end to end — every stage the chosen rows keep — and only the model's responses are scripted. | RR3a. Branch: the model is the keyed dependency, so the suite runs the real pipeline against a scripted stand-in; criteria that need a real model are tagged `live`. | RR3a — the scripted stand-in model declared in §5, named and described as a fake (Recommended); RR3b — the course's live OpenAI models (course default — heavy setup: an OpenAI API key and paid usage on every run) | A scripted model makes every asserted outcome replayable offline; a live model makes text outcomes vary run to run, so its criteria can assert shape only. | course+learner |
| C1 | contradicted | **Summary scoping** — whether a summary belongs to the thread it came from. Applies only when `D1` is `D1a`. | One scoping rule applies to both writing and listing summaries. | C1a. The course set this both ways; the stakes test passes because the two sides return different summary lists for the same read. | C1a — thread-scoped: a summary made from a thread's messages records that thread, and the summary list shown to the model holds only the active thread's summaries (Recommended - course default); C1b — unscoped: summaries record no thread, and every thread's summary list shows all of them (the Lesson 5 notebook's code) | Course-contradicted: the Lesson 5 notebook writes summaries without a thread; the end-to-end agent's helper code (Lesson 6) writes the thread and filters the list by it, and its system prompt says "prefer summaries for the active thread_id". | course |

## 1. Objective

A command-line research assistant agent that remembers its conversations across sessions and works with research papers: for each question in a thread it builds a partitioned context window from database-backed memory, selects tools by semantic search, runs a bounded tool-calling loop, and writes back what happened — guaranteeing that a thread's history survives restarts and that summarized conversation stays recoverable on demand. (pattern: CTX-A)

### Not Included            ★

Each item carries its handling tag for the scope-boundary row (L6):

1. **Hybrid (lexical + vector) search over the knowledge base** — *named by the course but never built* (the course created a hybrid-search preference it never used): buildable, but this spec supplies no parameters and no acceptance criteria for it.
2. **A reranking model between retrieval and the answer** — *named by the course but never built* (Lesson 2's retrieval pipeline): buildable, no parameters and no acceptance criteria supplied.
3. **A semantic cache that reuses earlier responses for similar queries** — *named by the course but never built* (Lesson 2): buildable, no parameters and no acceptance criteria supplied.
4. **Graph-traversal retrieval and relationship mapping between memories** — *named by the course but never built* (Lesson 3): buildable, no parameters and no acceptance criteria supplied.
5. **Strengthening, merging, decaying, or resolving contradictions between stored memories** — *named by the course but never built* (Lessons 1 and 3): buildable, no parameters and no acceptance criteria supplied.
6. **Fine-tuning the embedding model** — *named by the course but never built* (Lesson 3): buildable, no parameters and no acceptance criteria supplied.
7. **An agent-callable tool that reads a full tool-log entry back by its log id** — *restorable* (additive, owned by no other row); the build adds its own criteria if restored.
8. **A web or graphical interface** — *owned by row L5*; decided there (L5 decides where and how the program runs, and none of its options is a web or graphical interface).
9. **Multiple users and authentication** — *restorable* (additive, owned by no other row); the build adds its own criteria if restored.
10. **A keyed web-search tool** — *owned by row RR2*; decided there.
11. **Grafting this pattern onto an existing codebase** — *unavailable* (outside the delivered build mode: this spec builds a standalone project).

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python ≥ 3.11 | The course states no Python version; its `requirements.txt` lists every package **unpinned** (no versions anywhere), so each library below is a current release chosen at build time. Era-specific class, module and model names are perishable search keywords — see CTX-D. |
| Memory-core database | Row RR1's Default: standard-library `sqlite3`, one database file | Learners change this in Ledger row RR1, not here. |
| Embedding model | `sentence-transformers/paraphrase-mpnet-base-v2` (768-dimensional vectors) through `langchain-huggingface`'s HuggingFaceEmbeddings over `sentence-transformers` | The course's embedder in every lesson (CTX-D). Keyless; downloads the model on first use. The offline suite uses the fixture embedder from §5 instead. |
| Model provider | Row L4's Default: the `openai` SDK, Chat Completions with tool calling | Model names are chosen in the §0 checklist, never here. |
| Paper tools | `langchain-community` (ArxivRetriever, ArxivLoader) with `arxiv` and `pymupdf`; `langchain-text-splitters` (RecursiveCharacterTextSplitter) | Keyless public arXiv access; criteria that need it are `live`. |
| Seed data (row L2) | Row L2's Default: the fixture module in §5; `datasets` only under L2b | |
| Configuration | `python-dotenv` reads a `.env` file; environment variables override | Secrets come only from the environment: `OPENAI_API_KEY` (live model use), `TAVILY_API_KEY` (only under RR2b), database credentials (only under RR1b or RR1c). The course's notebooks hard-code database passwords; this spec never does. |
| Tests | `pytest`, marker `live` for criteria that need a key or network | |

## 3. Input/Output Contracts            ★

### 3.1 Command-line surface and configuration

| Command | Behavior |
|---|---|
| `python -m memory_agent init` | Opens or creates the memory core at the data location, then registers the course tools (idempotent). |
| `python -m memory_agent seed` | Ingests row L2's seed data into the knowledge base. |
| `python -m memory_agent ask --thread <id> "<question>"` | Runs one agent turn and prints the final answer on stdout. |
| `python -m memory_agent chat --thread <id>` | Reads one question per line and runs a turn for each; `/exit` quits. |

Every command performs the startup sequence first: open or create the memory core, verify the stored embedder settings (R4), register the course tools (R8).

| Variable | Values | Default |
|---|---|---|
| `AGENT_MEMORY_DB` | path of the database file | `./agent_memory.db` |
| `AGENT_MODEL_BACKEND` | `openai` (live) or `scripted` (the §5 stand-in) | `openai` |
| `AGENT_MODEL` | model name used for the agent role and for the context-limit lookup | the name in the §0 checklist (`scripted-model` under `scripted`) |
| `AGENT_EMBEDDER` | `course` (the §2 embedder), `fixture` (the §5 `FIXTURE_EMBEDDER`) or `fixture-alt` (the §5 `ALT_EMBEDDER`, used only by AC7) | `course` |
| `SCRIPTED_MODEL_SCRIPT` | `default`, `empty`, `generic-label`, `bad-entities` | `default` |
| `SCRIPTED_MODEL_LOG` | path of the stand-in's request log (JSON lines) | unset (no log) |

### 3.2 Persistent structures

Store names are binding (they are the course's own names, CTX-E): relational stores `CONVERSATIONAL_MEMORY` and `TOOL_LOG_MEMORY`; vector stores `SEMANTIC_MEMORY` (knowledge base), `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY`; plus one `store_settings` record per vector store.

```json
{
  "$id": "ConversationMessage",
  "type": "object",
  "required": ["id", "thread_id", "role", "content", "timestamp", "metadata", "created_at", "summary_id"],
  "properties": {
    "id": {"type": "string", "minLength": 1},
    "thread_id": {"type": "string", "minLength": 1},
    "role": {"enum": ["user", "assistant"]},
    "content": {"type": "string"},
    "timestamp": {"type": "string", "format": "date-time"},
    "metadata": {"type": "string", "description": "JSON text; '{}' when empty"},
    "created_at": {"type": "string", "format": "date-time"},
    "summary_id": {"type": ["string", "null"], "pattern": "^[0-9a-f]{8}$",
                   "description": "null until the row is summarized; then the summary's id"}
  }
}
```

```json
{
  "$id": "ToolLogEntry",
  "type": "object",
  "required": ["id", "thread_id", "tool_call_id", "tool_name", "tool_args", "result", "result_preview", "status", "error_message", "metadata", "timestamp", "created_at"],
  "properties": {
    "id": {"type": "string", "minLength": 1},
    "thread_id": {"type": "string"},
    "tool_call_id": {"type": ["string", "null"]},
    "tool_name": {"type": "string", "minLength": 1},
    "tool_args": {"type": "string", "description": "JSON text of the call's arguments"},
    "result": {"type": "string", "description": "full, untruncated tool output"},
    "result_preview": {"type": "string", "maxLength": 2000, "description": "first 2000 UTF-8 bytes of result"},
    "status": {"enum": ["success", "failed"]},
    "error_message": {"type": ["string", "null"]},
    "metadata": {"type": "string", "description": "JSON text, e.g. {\"iteration\": 1}"},
    "timestamp": {"type": "string", "format": "date-time"},
    "created_at": {"type": "string", "format": "date-time"}
  },
  "if": {"properties": {"status": {"const": "failed"}}},
  "then": {"properties": {"error_message": {"type": "string", "minLength": 1}}}
}
```

```json
{
  "$id": "VectorRecord",
  "type": "object",
  "required": ["id", "text", "metadata", "embedding"],
  "properties": {
    "id": {"type": "string"},
    "text": {"type": "string", "description": "the text that was embedded"},
    "metadata": {"type": "object"},
    "embedding": {"type": "array", "items": {"type": "number"}}
  }
}
```

```json
{
  "$id": "StoreSettings",
  "type": "object",
  "required": ["store", "embedder_id", "dimension", "distance"],
  "properties": {
    "store": {"enum": ["SEMANTIC_MEMORY", "WORKFLOW_MEMORY", "TOOLBOX_MEMORY", "ENTITY_MEMORY", "SUMMARY_MEMORY"]},
    "embedder_id": {"type": "string"},
    "dimension": {"type": "integer", "minimum": 1},
    "distance": {"const": "cosine"}
  }
}
```

Metadata shapes per vector store:

```json
{
  "KnowledgeSeedMeta": {"type": "object", "required": ["arxiv_id", "title", "subjects", "abstract", "submission_date"]},
  "PaperChunkMeta": {"type": "object",
    "required": ["source", "arxiv_id", "title", "entry_id", "published", "authors", "chunk_id", "num_chunks", "ingested_ts_utc"],
    "properties": {"source": {"const": "arxiv"}, "chunk_id": {"type": "integer", "minimum": 0}, "num_chunks": {"type": "integer", "minimum": 1}}},
  "WorkflowMeta": {"type": "object", "required": ["query", "success", "num_steps", "timestamp"],
    "properties": {"success": {"type": "boolean"}, "num_steps": {"type": "integer", "minimum": 1}}},
  "ToolboxMeta": {"type": "object", "required": ["name", "description", "signature", "parameters", "return_type", "augmented"],
    "properties": {"augmented": {"type": "boolean"},
      "queries": {"type": "array", "items": {"type": "string"}, "description": "present when augmented"}},
    "if": {"properties": {"augmented": {"const": true}}}, "then": {"required": ["queries"]}},
  "EntityMeta": {"type": "object", "required": ["name", "type", "description"],
    "properties": {"name": {"type": "string", "minLength": 1}, "type": {"enum": ["PERSON", "PLACE", "SYSTEM", "UNKNOWN"]}}},
  "SummaryMeta": {"type": "object", "required": ["id", "full_content", "summary", "description"],
    "properties": {
      "id": {"type": "string", "pattern": "^[0-9a-f]{8}$"},
      "description": {"type": "string", "minLength": 1,
        "not": {"enum": ["conversation summary", "summary", "chat summary", "thread summary", "Conversation summary", "Summary", "Chat summary", "Thread summary"]},
        "description": "lists common casings of the generic labels; R13 replaces any generic label (compared case-insensitively, surrounding quotes removed) before the record is written"},
      "thread_id": {"type": "string", "description": "present on thread summaries under C1a"}}}
}
```

### 3.3 Model-facing objects

```json
{
  "$id": "ToolSchema",
  "type": "object",
  "required": ["type", "function"],
  "properties": {
    "type": {"const": "function"},
    "function": {
      "type": "object",
      "required": ["name", "description", "parameters"],
      "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "parameters": {
          "type": "object",
          "required": ["type", "properties", "required"],
          "properties": {
            "type": {"const": "object"},
            "properties": {"type": "object", "additionalProperties": {
              "type": "object", "required": ["type"],
              "properties": {"type": {"enum": ["string", "integer", "number", "boolean"]}}}},
            "required": {"type": "array", "items": {"type": "string"},
                         "description": "exactly the parameters without a default value"}
          }
        }
      }
    }
  }
}
```

```json
{
  "$id": "ContextUsage",
  "type": "object",
  "required": ["tokens", "max", "percent", "status"],
  "properties": {
    "tokens": {"type": "integer", "minimum": 0, "description": "floor(characters / 4)"},
    "max": {"type": "integer", "minimum": 1},
    "percent": {"type": "number", "description": "tokens / max * 100, rounded to one decimal"},
    "status": {"enum": ["ok", "warning", "critical"]}
  },
  "allOf": [
    {"if": {"properties": {"percent": {"exclusiveMaximum": 50}}}, "then": {"properties": {"status": {"const": "ok"}}}},
    {"if": {"properties": {"percent": {"minimum": 50, "exclusiveMaximum": 80}}}, "then": {"properties": {"status": {"const": "warning"}}}},
    {"if": {"properties": {"percent": {"minimum": 80}}}, "then": {"properties": {"status": {"const": "critical"}}}}
  ]
}
```

```json
{
  "$id": "SummaryResult",
  "oneOf": [
    {"type": "object", "required": ["status"], "properties": {"status": {"const": "nothing_to_summarize"}}, "additionalProperties": false},
    {"type": "object", "required": ["id", "description", "summary"],
     "properties": {
       "id": {"type": "string", "pattern": "^[0-9a-f]{8}$"},
       "description": {"type": "string", "minLength": 1},
       "summary": {"type": "string", "allOf": [
         {"pattern": "### Technical Information"}, {"pattern": "### Emotional Context"},
         {"pattern": "### Entities & References"}, {"pattern": "### Action Items & Decisions"}]},
       "num_messages_summarized": {"type": "integer", "minimum": 1}}}
  ]
}
```

### 3.4 The context window sent to the model

Every agent request carries exactly: one system message (the memory-aware system prompt, R7) and one user message laid out as below, then the loop's assistant and tool messages. Placeholder lines appear when a segment retrieves nothing.

```text
# Question
<the question, verbatim>

## Conversation Memory
### What this memory is
### How you should leverage it
### Retrieved messages
[HH:MM:SS] [<role>] <content>            (placeholder: (No unsummarized messages found for this thread.))

## Knowledge Base Memory
### What this memory is
### How you should leverage it
### Retrieved passages                    (placeholder: (No relevant knowledge base passages found.))

## Workflow Memory
### What this memory is
### How you should leverage it
### Retrieved workflows                   (placeholder: (No relevant workflows found.))

## Entity Memory
### What this memory is
### How you should leverage it
### Retrieved entities
• <name>: <description>                   (placeholder: (No entities found.))

## Summary Memory
### What this memory is
### How you should leverage it
### Available summaries
  • [ID: <8 hex>] <label>                 (placeholder: (No summaries available for thread <thread id>.))
```

Each "What this memory is" / "How you should leverage it" subsection carries one or more sentences, written by the builder, stating the store's content and how the model should use it (CTX-A).

## 4. Business Rules

Labels: *course-demonstrated* (traceable to the course, with a CTX anchor) or *project hardening* (added by this spec; the course did not demonstrate it).

**R1 — Memory core with declared structure, created idempotently.** On first start the program creates every store and field declared in §3.2 for the stores D1's answer keeps, and one `store_settings` record per vector store. Starting again on the same data location keeps every existing row and creates nothing twice. *Course-demonstrated* store set and fields (CTX-A, CTX-E); *project hardening* for keeping data: the course's notebooks drop every table at the start of each lesson (CTX-C). → AC1, AC2

**R2 — Memory survives restarts.** A new process opened on the same data location reads everything earlier processes wrote. *Course-demonstrated* purpose ("persists across sessions", Lessons 1, 2, 6; CTX-B1). → AC3

**R3 — Conversational memory is exact, per thread, and time-ordered.** Before the loop — after the turn's memory segments are built (R6), so the turn's own question is not in its Conversation Memory segment — the harness writes the user's question as a `user` row; after the loop, it writes the final answer as an `assistant` row, both under the turn's thread id. The Conversation Memory segment holds only the active thread's rows whose `summary_id` is null, in time order, at most 10 rows (value: the end-to-end agent's read limit; the Lesson 5 test read 100). When more than 10 such rows exist, the segment holds the 10 most recent (*project hardening*: the course's query returns the earliest 10, CTX-C). Rows with equal timestamps keep insertion order (*project hardening*). Conversation is read by exact thread match, never by similarity (*course-demonstrated*, CTX-B1, CTX-C). → AC3, AC4, AC5, AC6

**R4 — One embedder and one distance strategy across all vector stores.** Every vector store embeds writes and queries with the same embedder and ranks by cosine similarity; each store's `store_settings` records the embedder id, dimension and distance, and startup fails with an error naming the store and both embedder ids when the configured embedder's id or dimension differs from what is recorded. Equal similarities are returned in insertion order. Cosine is a **post-build lever** — course-contradicted: cosine in the Lesson 3 and Lesson 4 code, Euclidean in the Lesson 5 and Lesson 6 code and in the Lesson 3 notebook's text; chosen by value branch 1 (Lesson 3's narration says "cosine"). The same-embedder rule is *course-demonstrated* (Lesson 2: the query embedder "would be the same we use during the ingestion"); the startup check and tie order are *project hardening*. → AC7

**R5 — Knowledge-base memory.** A write takes one text with one metadata object, or a list of texts with a list of metadata of equal length; unequal lengths raise an error naming the length mismatch and write nothing. A read returns the top 3 passages by similarity (value: the course's only setting) in the Knowledge Base Memory segment, or its placeholder. *Course-demonstrated* (CTX-A). → AC8, AC9, AC10

**R6 — Partitioned context window, built deterministically.** On every turn, before the model is called, the harness builds the user message of §3.4: the `# Question` section first, then the five segments in the order Conversation, Knowledge Base, Workflow, Entity, Summary, each with its subsections or placeholder, whether or not the model would have asked for them. The question is never summarized or offloaded. *Course-demonstrated* (Lessons 3 and 6; CTX-B13). → AC11, AC20

**R7 — Memory-aware system prompt.** The system message states: the role (a memory-aware research assistant with tools); that the user input is a partitioned context window with a `# Question` section and the five segments, naming each heading; each segment's purpose; the summary-expansion policy (when a critical detail is only in Summary Memory or is ambiguous, call `expand_summary` before relying on it); and these operating rules — start from the memory segments before using tools; resolve conflicts with exactly this priority line: "current `# Question` > latest Conversation Memory > Knowledge Base evidence > older summaries/workflows"; use only the tools provided this turn and the fewest calls needed; when memory is insufficient, say what is missing and then use a tool; for conversation compaction, call `summarize_and_store` with `thread_id`. *Course-demonstrated* (Lesson 6). → AC12

**R8 — Toolbox: tools as retrievable memory.** Registering a tool stores one toolbox record with name, description, signature, parameters (name, type, default when present), return type and the augmentation flag. Registration is idempotent by name: a name already stored is not written again and triggers no model call. A toolbox read returns tool schemas (§3.3) for the top-k records by similarity, one per distinct name; parameter types map str→string, int→integer, float→number, bool→boolean, anything else→string; `required` lists exactly the parameters without a default. At startup the harness registers the course tools: `arxiv_search_candidates`, `fetch_and_save_paper_to_kb_db`, `get_current_time`, `expand_summary`, `summarize_and_store`, `read_toolbox`. *Course-demonstrated* (Lesson 4; CTX-B10). → AC13, AC14, AC15, AC44

**R9 — Tool-description augmentation (row D2).** For an augmented tool, registration asks the tool augmenter for a richer description (a one-line summary, what the tool does step by step, when an agent should call it, caveats) from the original docstring and the tool's source, then asks for 5 diverse example user queries returned as a JSON array. The stored description is the augmented one; the stored retrieval text is the name, the augmented description, the signature and the queries joined by spaces. A plain tool's retrieval text is its name, docstring and signature. *Course-demonstrated* (Lesson 4; the retrieval text follows the narration, CTX-C). → AC16, AC44

**R10 — Per-turn semantic tool selection.** On every turn the harness retrieves the 5 tools most similar to the question and offers only those to the model. Executing a call resolves any registered tool by name. The `read_toolbox` tool lets the model search the toolbox itself (its own default k is 3). k = 5 is a **post-build lever** — course-contradicted: 5 in the end-to-end agent and in the toolbox-search tool's docstring, 3 in the tool's signature and the memory manager's default, 1 in the Lesson 4 demo; chosen by value branch 2 (the end-to-end agent's value). *Course-demonstrated* (Lesson 4; CTX-B2). → AC13, AC17

**R11 — Context-usage estimate.** Usage of a context string is: tokens = floor(characters / 4); max = the agent model's entry in the context-limit table, or 128,000 for an unlisted model; percent = tokens / max × 100 rounded to one decimal; status `ok` below 50, `warning` from 50 to below 80, `critical` from 80. The table holds the course's `gpt-5` and `gpt-5-mini` at 256,000 tokens, `scripted-model` at 256,000 and `scripted-model-tiny` at 1,000; the build adds an entry for the model named in the §0 checklist with its published context window. The divisor 4 is a **post-build lever** (Lesson 5 says some models' ratio is closer to 2 characters per token). *Course-demonstrated* (Lesson 5). → AC18, AC19

**R12 — Deterministic offload above the threshold (row D3 default).** After building the memory segments and before writing the question, the harness computes usage of the segments; when percent is greater than 80, it summarizes the thread's unsummarized conversation rows (R13, R14), replaces the whole Conversation Memory segment with a stub containing "Older conversation content was summarized to reduce context size." and "Use Summary Memory references + expand_summary(id) for full detail.", appends `[Summary ID: <id>] <label>` to the Summary Memory segment, and leaves every other segment unchanged. The threshold 80 is a **post-build lever** — course-contradicted: Lesson 6's narration says both "exceeded or is equal to 80%" and "greater than 80%"; chosen by value branch 2 (the end-to-end agent's code: greater than). *Course-demonstrated* (Lessons 5 and 6; CTX-B3). → AC20

**R13 — Summarization output.** A summarization takes at most the first 6,000 characters of its input and asks the summarizer for a summary under exactly these headings, in order: `### Technical Information`, `### Emotional Context`, `### Entities & References`, `### Action Items & Decisions` — keeping concrete details, separating confirmed facts from open questions, inventing nothing. If the reply is empty it retries once with a simpler request asking for at most 180 words under the same headings; if that is empty too, the summary is the four headings with the first 500 characters of the input (newlines as spaces) under Technical Information and "Not available from model output." under each other heading. It then asks for an 8–12 word label that is specific and not generic. A reply that is empty or equals "conversation summary", "summary", "chat summary" or "thread summary" (compared case-insensitively, surrounding quotes removed) is replaced by the first line of the summary — skipping heading lines and lines under 4 words, leading "-", "•", "*" removed — cut to its first 12 words with trailing spaces, commas, periods, semicolons and colons removed; if no line qualifies, the label is "Recent thread context, decisions, and open actions". The summary id is the first 8 characters of a random UUID — 8 lowercase hexadecimal characters. The summary record stores id, full input, summary and label, and its thread under C1a. *Course-demonstrated* (Lesson 5 and the end-to-end helper; CTX-B6, CTX-B7). → AC21, AC22, AC23

**R14 — Summarized rows are marked and never re-summarized.** Summarizing a thread reads all of its rows with null `summary_id` in time order, summarizes a transcript of lines `[YYYY-MM-DD HH:MM:SS] [ROLE] content`, then sets exactly those rows' `summary_id` to the new id. With no such rows it returns `nothing_to_summarize` and writes no summary. *Course-demonstrated* (Lesson 5; CTX-B5). → AC24

**R15 — Summaries expand on demand.** The `expand_summary` tool returns, in order: `## Summary Context`, the summary text, `## Expanded Conversations for Summary ID: <id>`, `Total messages: <n>`, then each linked message in time order as `[YYYY-MM-DD HH:MM:SS] [ROLE]` followed by its content. For an unknown id it returns "Summary <id> not found." and "No conversations found for summary_id: <id>". *Course-demonstrated* (Lessons 5 and 6, "just-in-time retrieval"; CTX-B4). → AC25, AC26, AC36

**R16 — The Summary Memory segment lists ids and labels only.** It shows up to 10 summaries as `  • [ID: <id>] <label>` and never their summary text; under C1a it holds only summaries recorded for the active thread. *Course-demonstrated* (Lesson 6). → AC27

**R17 — Bounded tool-calling loop.** The loop calls the agent model with the messages and the offered tools at most 10 times. A reply with tool calls appends the assistant message with its calls, runs each call, and appends one tool message per call; a reply without tool calls is the final answer. A call to an unregistered name produces the result "Error: Tool '<name>' not found" (no tool raised, so its tool-log row and workflow step carry `success`, R18, R19); a tool that raises produces the result "Error: <message>" with status `failed`; neither ends the turn. After 10 model calls without a final answer, the final answer is "I was unable to complete the request within the allowed iterations." *Course-demonstrated* (Lesson 6; CTX-B9). → AC28, AC31, AC32, AC33, AC43

**R18 — Tool outputs are offloaded to the tool log.** Every tool call writes a tool-log row with the thread id, the call id, the tool name, the arguments as JSON, the full result, the first 2,000 UTF-8 bytes as preview, the status, the error message and metadata `{"iteration": <n>}`. When a result is longer than 3,000 characters, the tool message holds its first 3,000 characters followed by "\n\n[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <id>]"; otherwise it holds the whole result. *Course-demonstrated* ("context offloading", Lesson 6; CTX-B8). → AC33, AC34

**R19 — Workflow memory.** After a turn with at least one tool call, the harness writes one workflow record with text "Query: <question>\nSteps:\nStep 1: <step>\n…\nAnswer: <first 200 characters of the final answer>" and metadata query, success (true), num_steps and timestamp; each step reads `<tool>(<arguments as a JSON object, string values over 50 characters cut to 50 followed by "...">) → success` or `→ failed`. A turn without tool calls writes no workflow. The Workflow Memory segment shows the top 3 workflows by similarity whose num_steps is greater than 0, separated by "\n---\n". *Course-demonstrated* (Lessons 5 and 6; CTX-B11). → AC28, AC29, AC30

**R20 — Entity memory (row D3 default).** On every turn the harness asks the entity extractor for a JSON array of entities (name, type PERSON, PLACE or SYSTEM, short description) from the first 500 characters of the question, and again from the final answer; a text shorter than 5 characters after trimming is skipped without a model call. Each entity with a name is stored as text "<name> (<type>): <description>" with metadata name, type (UNKNOWN when missing) and description. A reply that is not a JSON array yields no entities, and extraction failure never fails the turn. The Entity Memory segment shows the top 5 entities as `• <name>: <description>`. *Course-demonstrated* (Lesson 6 code; CTX-B14). → AC37, AC38, AC39

**R21 — The summarize tool marks the active thread.** `summarize_and_store` with a `thread_id` summarizes that thread (R14) and returns "Stored as [Summary ID: <id>] <label>", or "No unsummarized messages found for thread <id>." when nothing is left; with only non-empty `text` it summarizes that text (R13) and returns "Stored as [Summary ID: <id>] <label>"; with neither it returns a message asking for one of them. When the model calls it without `thread_id`, the harness adds the active thread's id before running it. *Course-demonstrated* (Lesson 6; CTX-B12). → AC21, AC35

**R22 — Paper tools store what they find.** `arxiv_search_candidates(query, k=5)` returns a JSON array of up to k candidates, each with `arxiv_id` (the part of the entry URL after `/abs/`), `entry_id`, `title`, `authors`, `published` and `abstract` (at most 2,500 characters), from a retriever set to load at most 8 documents of at most 4,000 characters without full text. `fetch_and_save_paper_to_kb_db(arxiv_id, chunk_size=1500, chunk_overlap=200)` loads the full paper text, splits it with a recursive character splitter at those sizes, writes the chunks into the knowledge base with `PaperChunkMeta`, and returns "Saved arXiv <id> to SEMANTIC_MEMORY: <n> chunks (title: <title>)."; with no document or empty text it returns a message saying so. The full paper text never passes through the model. *Course-demonstrated* (Lessons 4 and 6; chunk sizes are the tool's defaults). → AC40, AC41, AC43

**R23 — Current-time tool.** `get_current_time(detailed=False)` returns local time as `YYYY-MM-DD HH:MM:SS`, with microseconds appended after a period when `detailed` is true. *Course-demonstrated* (Lesson 4). → AC28

**R24 — Secrets from the environment only.** Keys and credentials are read from the environment or `.env`; none is written into code, fixtures or logs. With the live backend and no `OPENAI_API_KEY`, every command exits with a non-zero status and an error that names `OPENAI_API_KEY`. *Project hardening.* → AC42

**R25 — Seeding the knowledge base.** `seed` writes one knowledge-base record per seed paper with text "<title>\n<subjects>\n<abstract>" and `KnowledgeSeedMeta` metadata, skipping a record whose title, subjects and abstract are all empty. *Course-demonstrated* shape (Lesson 3). → AC45

**R26 — Every model call names its purpose.** Each model request carries one purpose: `agent`, `summarize`, `summarize_retry`, `label`, `extract_entities`, `augment_docstring` or `generate_queries`. Requests for these purposes set no temperature; every purpose except `agent` sets a completion-token cap (4,000 for summaries, 2,000 for the others), and `agent` requests set none. *Project hardening* for the purpose tag (it lets the stand-in answer by role); the caps and the absent temperature are *course-demonstrated* (CTX-D). → AC16, AC21

## 5. Acceptance Criteria                ★  (the oracle)

### 5.1 Fixture corpus (declared first; the build MUST NOT modify fixtures to make a test pass)

All fixture modules live in `tests/fixtures/` and are importable modules: `fixture_embedder.py`, `scripted_model.py`, `fixture_papers.py`, `fixture_tools.py`, `fixture_threads.py`, `fixture_texts.py`. Every fact below is authored by this spec.

**`fixture_embedder.py` — fixture embedders (test stand-ins for the embedding model, honestly labelled).**
- `FIXTURE_EMBEDDER`: id `fixture-embedder-v1`, dimension 8. Vocabulary, in order: `ferry`, `tide`, `weather`, `time`, `paper`, `invoice`, `garden`, `music`. A text is lower-cased and split into tokens at every character that is not a–z or 0–9; component i is the number of tokens equal to vocabulary word i. Similarity is cosine; when either vector is all zeros, similarity is 0.
- `ALT_EMBEDDER`: id `fixture-embedder-alt`, dimension 8, same behavior.

**`scripted_model.py` — scripted stand-in model (a fake standing in for the live model; its own description says so).** It accepts every request through the same model interface the app uses, appends `{"purpose", "messages", "tools"}` as one JSON line to `SCRIPTED_MODEL_LOG` when set, and answers by purpose (a script not named under a purpose answers it as `default` does):
- `augment_docstring`: the original docstring, trimmed, followed by " (augmented)".
- `generate_queries`: `["example query 1", "example query 2", "example query 3", "example query 4", "example query 5"]`.
- `summarize`: SUMMARY_TEXT = "### Technical Information\nFixture thread discussed the Lumen Bay ferry schedule.\n\n### Emotional Context\nCalm and practical.\n\n### Entities & References\nLumen Bay (PLACE).\n\n### Action Items & Decisions\nNo open actions." Script `empty`: the empty string.
- `summarize_retry`: SUMMARY_TEXT; script `empty`: the empty string.
- `label`: "Lumen Bay ferry timetable questions and the chosen departure time"; script `empty`: "Summary"; script `generic-label`: "Conversation summary".
- `extract_entities`: if the request contains "Orrin Vale": `[{"name": "Orrin Vale", "type": "PERSON", "description": "harbor master"}, {"name": "Tidewatch", "type": "SYSTEM", "description": "tide alert service"}, {"name": "Gull Pier", "description": "old pier"}]`; else if it contains "Lumen Bay": `[{"name": "Lumen Bay", "type": "PLACE", "description": "fictional harbor town"}]`; else `[]`. Script `bad-entities`: "not json at all" for every request.
- `agent`: reads the question from the line after `# Question` in the user message and counts the tool messages already present (n). Tool-call ids are `call_<n+1>`. Script by question:

| Question | Replies, in order |
|---|---|
| "What time does the Lumen Bay ferry leave on Sundays?" | final "The Sunday ferry leaves Lumen Bay at 09:00." |
| "Book a seat on that one." | final "Booking noted for the 09:00 Sunday ferry." |
| "What time is it?" | call `get_current_time` `{}`; final "Here is the time." |
| "Loop forever" | call `get_current_time` `{}` on every request |
| "Show the long report" | call `fixture_long_report` `{}`; final "Report received." |
| "Use a missing tool" | call `no_such_tool` `{}`; final "Done." |
| "Trigger a failing tool" | call `fixture_failing_tool` `{}`; final "Handled." |
| "Summarize our conversation" | call `summarize_and_store` `{"text": ""}`; final "Summary stored." |
| "What was my first question?" | call `expand_summary` `{"summary_id": <the 8 characters after the first "[ID: " in the user message, or "none">}`; final "Answered from the expanded summary." |
| any other question | final "OK." |

**`fixture_papers.py` — five invented paper records** (fields arxiv_id, title, subjects, abstract, submission_date):
- P1 `fixture-0001`, "Ferry Routing Under Tide Constraints", "Operations Research", "We schedule a ferry fleet around tide windows.", "2026-01-05"
- P2 `fixture-0002`, "Weather Signals in Garden Yields", "Agronomy", "Weather records predict garden harvests.", "2026-01-12"
- P3 `fixture-0003`, "Invoice Fraud Detection at Scale", "Machine Learning", "A paper on invoice anomaly scoring.", "2026-02-02"
- P4 `fixture-0004`, "Music Recommendation with Listening Time", "Information Retrieval", "Listening time shapes music suggestions.", "2026-02-20"
- P5 `fixture-0005`, "Tide Gauges and Weather Fronts", "Oceanography", "Tide readings track weather fronts.", "2026-03-01"

**`fixture_tools.py` — test-only tools** (registered plain unless an AC says otherwise; none has parameters unless listed; every one returns a string):
- `fixture_tool_1` "Returns the ferry timetable."; `fixture_tool_2` "Returns the tide table."; `fixture_tool_3` "Returns the weather report."; `fixture_tool_4` "Returns the local time."; `fixture_tool_5` "Returns a paper abstract."; `fixture_tool_6` "Returns an invoice total."; `fixture_tool_7` "Returns garden tips."; `fixture_tool_8` "Returns a music playlist."
- `fixture_tool_params(city: str, days: int = 3, exact: bool = False, ratio: float = 0.5)` "Returns a forecast for a city."
- `fixture_long_report` "Returns a long report." — returns "0123456789" repeated 450 times (4,500 characters).
- `fixture_failing_tool` "Always fails." — raises an error with message "fixture failure".

**`fixture_threads.py` — planted conversation and workflow state** (rows written in this order through the conversational write, so timestamps are non-decreasing):
- `FERRY_THREAD` (thread `ferry-thread`): user "When does the first ferry leave Lumen Bay?"; assistant "The first weekday ferry leaves Lumen Bay at 07:15."; user "And on Sundays?"; assistant "On Sundays the first ferry leaves at 09:00."
- `LONG_THREAD` (thread `long-thread`): 10 user rows; row k (k = 0…9) is the digit k repeated 400 times.
- `TWELVE_THREAD` (thread `twelve-thread`): 12 user rows "msg-01" … "msg-12".
- `ZERO_STEP_WORKFLOW`: a workflow record written directly into `WORKFLOW_MEMORY` by the test, bypassing `WorkflowMeta` validation (it plants a record the app never writes, R19), with text "Query: ferry time\nSteps:\nAnswer: none" and metadata num_steps 0, success true.

**`fixture_texts.py`:**
- `FERRY_NOTE` = "Ferry departs Lumen Bay at 07:15 on weekdays and 09:00 on Sundays."
- `LONG_TEXT` = "a" repeated 6,000 times, then "ZQXJ", then "b" repeated 996 times (7,000 characters).

Assertions on the stand-in's request log count only the requests made from the start of the AC's When step. Unless an AC says otherwise: `AGENT_MODEL_BACKEND=scripted`, `AGENT_MODEL=scripted-model`, `AGENT_EMBEDDER=fixture`, `SCRIPTED_MODEL_SCRIPT=default`, `SCRIPTED_MODEL_LOG` set to a fresh file (so every AC that asserts on requests, a segment's contents or "no model request" reads them from that log), a fresh data location per AC, and the startup sequence already run (course tools registered).

### 5.2 Criteria

| AC | Given | When | Then |
|---|---|---|---|
| AC1 (R1) | An empty data location | `init` runs | The database holds `CONVERSATIONAL_MEMORY` and `TOOL_LOG_MEMORY` with exactly the §3.2 fields, the five vector stores each accepting `VectorRecord` fields, and five `store_settings` records with `distance` = `cosine`, `embedder_id` = `fixture-embedder-v1`, `dimension` = 8; the conversation, tool-log, knowledge-base, workflow, entity and summary stores hold 0 records |
| AC2 (R1) | AC1's data location plus one conversation row written for thread `t-keep` | `init` runs again | `CONVERSATIONAL_MEMORY` still holds exactly that one row; each store_settings record still exists once |
| AC3 (R2, R3) | A fresh data location; `SCRIPTED_MODEL_LOG` set | Process 1 runs `ask --thread t-restart "What time does the Lumen Bay ferry leave on Sundays?"`, exits; process 2 runs `ask --thread t-restart "Book a seat on that one."` | Process 1 prints "The Sunday ferry leaves Lumen Bay at 09:00."; the user message of process 2's first `agent` request contains "[user] What time does the Lumen Bay ferry leave on Sundays?" followed later by "[assistant] The Sunday ferry leaves Lumen Bay at 09:00." |
| AC4 (R3) | AC3's state | A turn "Book a seat on that one." runs in thread `t-other` | Its Conversation Memory segment contains "(No unsummarized messages found for this thread.)" and not "Lumen Bay ferry leave" |
| AC5 (R3) | A fresh data location | One turn "What time does the Lumen Bay ferry leave on Sundays?" runs in thread `t-sunday` | `CONVERSATIONAL_MEMORY` holds, for `t-sunday`, exactly two rows in time order: (`user`, the question) and (`assistant`, "The Sunday ferry leaves Lumen Bay at 09:00."), both with null `summary_id` |
| AC6 (R3) | `TWELVE_THREAD` planted | A turn "Hello there" runs in thread `twelve-thread` | Its Conversation Memory segment lists "msg-03" through "msg-12" in that order and does not contain "msg-01" or "msg-02" |
| AC7 (R4) | AC1's data location (created with `FIXTURE_EMBEDDER`) | The memory core is opened with `AGENT_EMBEDDER=fixture-alt` (`ALT_EMBEDDER`) | Opening fails with an error naming `SEMANTIC_MEMORY` (or another vector store) and both embedder ids; no record is written |
| AC8 (R5) | `seed` ran with `fixture_papers` | A knowledge-base read for "ferry tide" | The segment's passages are, in order, P1's text, P5's text, P2's text (P1 similarity 1.0, P5 0.5, P2 0 and earliest among the ties) |
| AC9 (R5) | A fresh data location | A knowledge-base write of texts ["alpha", "beta"] with metadata [{"k": 1}] | An error mentioning the length mismatch is raised; `SEMANTIC_MEMORY` holds 0 records |
| AC10 (R5) | A fresh data location (nothing seeded) | A knowledge-base read for "ferry" | The segment contains "(No relevant knowledge base passages found.)" |
| AC11 (R6) | A fresh data location; `SCRIPTED_MODEL_LOG` set | A turn "Hello there" runs in thread `t-fresh` | The first `agent` request's user message starts with "# Question\nHello there\n\n## Conversation Memory"; the headings `## Conversation Memory`, `## Knowledge Base Memory`, `## Workflow Memory`, `## Entity Memory`, `## Summary Memory` appear in that order, each followed by "### What this memory is" and "### How you should leverage it"; it contains the placeholders "(No unsummarized messages found for this thread.)", "(No relevant knowledge base passages found.)", "(No relevant workflows found.)", "(No entities found.)", "(No summaries available for thread t-fresh.)" |
| AC12 (R7) | AC11's run | Inspect the first `agent` request's system message | It contains each of the five segment headings, "expand_summary", "summarize_and_store", "thread_id", and the line "current `# Question` > latest Conversation Memory > Knowledge Base evidence > older summaries/workflows" |
| AC13 (R8, R10) | A fresh memory core whose toolbox holds only `fixture_tool_1` … `fixture_tool_8`, registered in that order | A toolbox read for "ferry time" with k = 5 | Tool names returned, in order: `fixture_tool_1`, `fixture_tool_4`, `fixture_tool_2`, `fixture_tool_3`, `fixture_tool_5` |
| AC14 (R8) | AC13's toolbox | `fixture_tool_1` is registered again | `TOOLBOX_MEMORY` holds 8 records and exactly one named `fixture_tool_1`; no model request was made |
| AC15 (R8) | A fresh memory core whose toolbox holds only `fixture_tool_params` | A toolbox read for "forecast" with k = 1 | It returns exactly one schema: name `fixture_tool_params`, parameters `{"type": "object", "properties": {"city": {"type": "string"}, "days": {"type": "integer"}, "exact": {"type": "boolean"}, "ratio": {"type": "number"}}, "required": ["city"]}` |
| AC16 (R9, R26) | A fresh memory core with an empty toolbox; `SCRIPTED_MODEL_LOG` set | `fixture_tool_2` is registered with augmentation | The log shows exactly two requests, purposes `augment_docstring` then `generate_queries`; the record's metadata has description "Returns the tide table. (augmented)", `augmented` true and 5 queries; the record's text contains "(augmented)" and "example query 1" |
| AC17 (R10) | A fresh data location; `fixture_long_report` and `fixture_failing_tool` registered besides the course tools; `SCRIPTED_MODEL_LOG` set | A turn "What time is it?" runs in thread `t-tools` | The first `agent` request offers exactly 5 tool schemas with 5 distinct names |
| AC18 (R11) | `AGENT_MODEL=scripted-model-tiny` | Usage is computed for strings of 1,996, 2,000, 3,196 and 3,200 characters | Results: (499, 1000, 49.9, `ok`), (500, 1000, 50.0, `warning`), (799, 1000, 79.9, `warning`), (800, 1000, 80.0, `critical`) as (tokens, max, percent, status) |
| AC19 (R11) | `AGENT_MODEL=unlisted-model` | Usage is computed for a 512,000-character string | (128000, 128000, 100.0, `critical`) |
| AC20 (R6, R12) | `LONG_THREAD` planted; `AGENT_MODEL=scripted-model-tiny`; `SCRIPTED_MODEL_LOG` set | A turn "Continue please" runs in thread `long-thread` | The log shows a `summarize` request before the first `agent` request; that `agent` request's user message starts with "# Question\nContinue please", contains "Older conversation content was summarized to reduce context size." and "[Summary ID: <id>] Lumen Bay ferry timetable questions and the chosen departure time" with `<id>` matching `^[0-9a-f]{8}$`, and does not contain "7" repeated 400 times; still contains `## Knowledge Base Memory` with "(No relevant knowledge base passages found.)" and `## Entity Memory` with "(No entities found.)"; all 10 planted rows carry that same `summary_id`; the "Continue please" row's `summary_id` is null |
| AC21 (R13, R21, R26) | Script `empty`; `SCRIPTED_MODEL_LOG` set | `summarize_and_store` runs with text `FERRY_NOTE` and no thread | Request purposes in order: `summarize`, `summarize_retry`, `label`; the `summarize_retry` request contains "180 words"; the result is "Stored as [Summary ID: <id>] Ferry departs Lumen Bay at 07:15 on weekdays and 09:00 on Sundays" with `<id>` matching `^[0-9a-f]{8}$`; the stored summary contains the four headings in order, `FERRY_NOTE`, and "Not available from model output." three times |
| AC22 (R13) | Script `generic-label`; `FERRY_THREAD` planted | `summarize_and_store` runs with `thread_id` `ferry-thread` | The stored label is "Fixture thread discussed the Lumen Bay ferry schedule" |
| AC23 (R13) | `SCRIPTED_MODEL_LOG` set | `summarize_and_store` runs with text `LONG_TEXT` | The `summarize` request contains 6,000 consecutive "a" characters and does not contain "ZQXJ"; the stored full input is 7,000 characters and contains "ZQXJ" |
| AC24 (R14) | `FERRY_THREAD` planted | `summarize_and_store` runs with `thread_id` `ferry-thread`, then again the same way | First result "Stored as [Summary ID: <id>] Lumen Bay ferry timetable questions and the chosen departure time"; all 4 rows carry `<id>`; a Conversation Memory read for `ferry-thread` shows "(No unsummarized messages found for this thread.)"; the second result is "No unsummarized messages found for thread ferry-thread." and `SUMMARY_MEMORY` still holds 1 record |
| AC25 (R15) | AC24's state after the first call | `expand_summary` runs with `<id>` | The output contains, in this order: "## Summary Context", "Fixture thread discussed the Lumen Bay ferry schedule.", "## Expanded Conversations for Summary ID: <id>", "Total messages: 4", then the 4 `FERRY_THREAD` contents in their planted order, each preceded by a `[YYYY-MM-DD HH:MM:SS]` timestamp and "[USER]" or "[ASSISTANT]" matching its role |
| AC26 (R15) | A fresh data location | `expand_summary` runs with `deadbeef` | The output contains "Summary deadbeef not found." and "No conversations found for summary_id: deadbeef" |
| AC27 (R16) | AC24's state after the first call | Summary Memory segments are built for threads `ferry-thread` and `t-other` | The `ferry-thread` segment contains "[ID: <id>] Lumen Bay ferry timetable questions and the chosen departure time" and not "Calm and practical."; the `t-other` segment contains "(No summaries available for thread t-other.)" |
| AC28 (R17, R19, R23) | `SCRIPTED_MODEL_LOG` set | A turn "What time is it?" runs in thread `t-time` | Two `agent` requests; the second ends with a tool message whose call id is `call_1` and whose content matches `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$`; the answer is "Here is the time."; `WORKFLOW_MEMORY` holds one record with text "Query: What time is it?\nSteps:\nStep 1: get_current_time({}) → success\nAnswer: Here is the time." and num_steps 1 |
| AC29 (R19) | A fresh data location | A turn "What time does the Lumen Bay ferry leave on Sundays?" runs | `WORKFLOW_MEMORY` holds 0 records |
| AC30 (R19) | AC28's state plus `ZERO_STEP_WORKFLOW` | A turn "What time is it now?" runs in thread `t-time2` | Its Workflow Memory segment contains "Step 1: get_current_time" and does not contain "Answer: none" |
| AC31 (R17) | `SCRIPTED_MODEL_LOG` set | A turn "Loop forever" runs in thread `t-loop` | Exactly 10 `agent` requests; the answer is "I was unable to complete the request within the allowed iterations."; `TOOL_LOG_MEMORY` holds 10 rows for `t-loop` with call ids `call_1` … `call_10`; the last `t-loop` conversation row is that answer with role `assistant` |
| AC32 (R17) | `SCRIPTED_MODEL_LOG` set | A turn "Use a missing tool" runs | The second `agent` request's tool message is "Error: Tool 'no_such_tool' not found"; the answer is "Done." |
| AC33 (R17, R18) | `fixture_failing_tool` registered | A turn "Trigger a failing tool" runs in thread `t-fail` | The tool-log row has status `failed`, error_message "fixture failure" and result "Error: fixture failure"; the workflow record contains "Step 1: fixture_failing_tool({}) → failed"; the answer is "Handled." |
| AC34 (R18) | `fixture_long_report` registered; `SCRIPTED_MODEL_LOG` set | A turn "Show the long report" runs in thread `t-long` | The second `agent` request's tool message is the report's first 3,000 characters followed by "\n\n[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <id>]", where `<id>` is the tool-log row's id; that row has result length 4,500, result_preview length 2,000, call id `call_1`, status `success`, metadata `{"iteration": 1}`, thread `t-long` |
| AC35 (R21) | `FERRY_THREAD` planted; `SCRIPTED_MODEL_LOG` set | A turn "Summarize our conversation" runs in thread `ferry-thread` | The second `agent` request's tool message is "Stored as [Summary ID: <id>] Lumen Bay ferry timetable questions and the chosen departure time"; the 4 planted rows and the "Summarize our conversation" row carry `<id>`; the "Summary stored." row has null `summary_id` |
| AC36 (R15) | AC35's state | A turn "What was my first question?" runs in thread `ferry-thread` | The first `agent` request's Summary Memory segment contains "[ID: <id>]"; the second request's tool message contains "When does the first ferry leave Lumen Bay?" and "Total messages: 5"; the answer is "Answered from the expanded summary." |
| AC37 (R20) | A fresh data location | A turn "What time does the Lumen Bay ferry leave on Sundays?" runs in thread `t-ent`, then a turn "Book a seat on that one." in the same thread | After the first turn `ENTITY_MEMORY` holds 2 records named "Lumen Bay" with type PLACE; the second turn's Entity Memory segment contains "• Lumen Bay: fictional harbor town" |
| AC38 (R20) | `SCRIPTED_MODEL_LOG` set | A turn "Who is Orrin Vale at Gull Pier using Tidewatch?" runs | `ENTITY_MEMORY` holds (Orrin Vale, PERSON), (Tidewatch, SYSTEM), (Gull Pier, UNKNOWN); the turn made exactly one `extract_entities` request (the answer "OK." is skipped) |
| AC39 (R20) | Script `bad-entities` | A turn "What time does the Lumen Bay ferry leave on Sundays?" runs | The answer is "The Sunday ferry leaves Lumen Bay at 09:00."; `ENTITY_MEMORY` holds 0 records |
| AC40 (R22) `live` | Network access; `AGENT_EMBEDDER=course` | `fetch_and_save_paper_to_kb_db` runs with `2310.08560` | The result starts "Saved arXiv 2310.08560 to SEMANTIC_MEMORY:" and reports n ≥ 2 chunks; n new knowledge-base records exist, each with `PaperChunkMeta` keys, `chunk_id` 0 … n−1, `num_chunks` n, and text of at most 1,500 characters |
| AC41 (R22) `live` | Network access | `arxiv_search_candidates` runs with "memory augmented language agents", k = 3 | The result parses as a JSON array of at most 3 objects, each with keys arxiv_id, entry_id, title, authors, published, abstract; each arxiv_id equals the part of entry_id after "/abs/"; each abstract is at most 2,500 characters |
| AC42 (R24) | `AGENT_MODEL_BACKEND=openai`, `OPENAI_API_KEY` unset, no `.env` in the working directory | `ask --thread t-key "Hello there"` runs | Exit status is non-zero and the error output contains "OPENAI_API_KEY" |
| AC43 (R17, R22) `live` | `AGENT_MODEL_BACKEND=openai`, `OPENAI_API_KEY` set, `AGENT_EMBEDDER=course` | Turns "Can you find the MemGPT paper on arXiv?" then "Can you save the content of the paper?" run in thread `t-live` | The second turn's first request contains the first question in its Conversation Memory segment; `TOOL_LOG_MEMORY` holds a `success` row for `fetch_and_save_paper_to_kb_db` in `t-live`; `SEMANTIC_MEMORY` holds more records than before the turns |
| AC44 (R8, R9) | An empty data location; `SCRIPTED_MODEL_LOG` set | `init` runs twice | `TOOLBOX_MEMORY` holds exactly six records: `fetch_and_save_paper_to_kb_db`, `expand_summary`, `summarize_and_store`, `read_toolbox` with `augmented` true; `arxiv_search_candidates`, `get_current_time` with `augmented` false; no record named `search_tavily`; the second `init` made no model request |
| AC45 (R25) | An empty data location | `seed` runs | `SEMANTIC_MEMORY` holds 5 records; P3's record text is "Invoice Fraud Detection at Scale\nMachine Learning\nA paper on invoice anomaly scoring." and its metadata is arxiv_id `fixture-0003`, title "Invoice Fraud Detection at Scale", subjects "Machine Learning", abstract "A paper on invoice anomaly scoring.", submission_date "2026-02-02"; every other record's metadata likewise equals its paper's five fields |

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the offline suite with the scripted backend and the fixture embedder; run `live` criteria only when the person supplies keys.
- Keep `resolved-decisions.md` as the record of the gate's answers and build on its values.
- Read secrets from the environment or `.env`; keep `.env` out of version control.
- Report every criterion with cited evidence (§7).
- Treat CTX-D names as search keywords against current documentation.

**Ask First** (derived from the course's argued trade-offs in CTX-C; each wrong side forces rework or changes a guarantee without failing a criterion)
- Changing the embedding model or the distance strategy once any vector store holds data — every vector store must be re-embedded (R4; CTX-C T18).
- Changing the paper chunk size or overlap after papers are ingested — ingested papers must be re-fetched (R22; CTX-C T24).
- Moving any operation between harness-run and model-called, e.g. letting the model decide when to read memory or save turns (row D3; CTX-C T4).
- Changing tool-description augmentation after tools are registered — the toolbox store must be cleared and tools re-registered (row D2; CTX-C T6).
- Switching recoverable compaction to a lossy summary (row D4; CTX-C T8).
- Changing summary scoping after summaries exist (row C1; CTX-C T21).
- Changing the offload threshold of 80 or the 50/80 status bands (R11, R12; CTX-C T9).
- Changing the token-estimate divisor of 4 (R11; CTX-C T10).
- Changing the per-turn tool count of 5 (R10; CTX-C T20).
- Changing the 3,000-character tool-result cut or sending full tool outputs to the model (R18; CTX-C T12).
- Moving stores to another database after data exists (row RR1; CTX-C T22).

**Never**
- Invent provenance or citations, or describe a hardening rule as course-taught.
- Let the agent answer from memory it does not have: when memory is insufficient it states what is missing (R7).
- Modify fixtures, the scripted model's replies or the fixture embedder to make a test pass.
- Commit secrets or write keys into code, fixtures or logs.
- Drop or recreate memory stores at startup.
- Bake a "current best" model name into code defaults; models come from the §0 checklist.

## 7. Test Plan & Self-Verification

Commands, run from the project root:

```bash
python -m pip install -e ".[test]"
python -m pytest tests -m "not live" -q            # offline suite: scripted model + fixture embedder
OPENAI_API_KEY=... python -m pytest tests -m live -q  # live criteria AC40, AC41, AC43
python -m memory_agent init && python -m memory_agent seed
AGENT_MODEL_BACKEND=scripted AGENT_EMBEDDER=fixture python -m memory_agent ask --thread demo "What time is it?"
```

The build agent MUST report results per acceptance criterion (AC1 … AC45) with cited evidence — the test name and its output, and the file paths that implement the behavior. "Should pass" or "looks correct" counts as a failure: it means the criterion was not run. Live criteria not run for lack of keys are reported as "not run (no key)", never as passed.

**Tests by option** — one line per Options entry that is not its row's Default. A build that chose an option reports the criteria it retires as not applicable, not as failures, and builds the changed ones as changed.

| Option id | Rules and criteria that no longer apply | Rules, criteria and Ledger cells that change (and how) | Offline-suite criteria switched off |
|---|---|---|---|
| L1b | — | R7 (role line names your domain); R8, AC44 (the registered tools and their `augmented` flags are your domain's tools plus the memory tools); R22, AC40, AC41, AC43 (your domain's tools and their live checks); R25, AC45 (your seed data's fields) | — |
| L2b | — | R25 (seed streams the first 100 dataset records, text = title, subjects, abstract joined by newlines; metadata arxiv_id, title, subjects, abstract, submission_date); AC45 (asserts at most 100 records with those keys; becomes `live`) | AC45 |
| L2c | — | R25 (one record per document of yours, with your metadata); AC45 (asserts your record count and fields) | — |
| L3b | — | Your stated goal's criteria are added to §5; nothing else changes | — |
| L4b | — | R17 and R26 (tool calls and results use the provider's tool-use message format); AC42 (names the provider's key variable); AC43 (runs against this provider) | — |
| L4c | — | R17 and R26 (the local endpoint's tool-calling format); AC42 (checks the endpoint setting instead of a key); AC43 (runs against the local model) | — |
| L5b | — | AC3 (the two processes become two kernel sessions on the same data location); AC42 (the key check runs in the first cell that builds the model client); AC1, AC2, AC44, AC45 (`init` and `seed` run as notebook cells); §3.1 (notebook cells replace the commands); L1 Options cell L1a (it names a command-line agent) and L2 Options cell L2a (it names the `seed` command) | — |
| L6b | — | The restored §1 items are built; criteria are supplied only for restorable items, by the build | — |
| D1b | R4, R5, R8, R9, R10, R11, R12, R13, R14, R15, R16, R19, R20, R21, R25; AC7, AC8, AC9, AC10, AC13, AC14, AC15, AC16, AC17, AC18, AC19, AC20, AC21, AC22, AC23, AC24, AC25, AC26, AC27, AC29, AC30, AC35, AC36, AC37, AC38, AC39, AC40, AC43, AC44, AC45 | R1, AC1, AC2 (only `CONVERSATIONAL_MEMORY` exists); R6, AC11 (user message = `# Question` + Conversation Memory only); R7, AC12 (prompt names only the conversation segment, no summary tools); R17, R18, R22 (no tool log; every registered tool — `arxiv_search_candidates`, `get_current_time` — offered each turn; tool results over 3,000 characters cut with "[Truncated for context.]" and no log pointer); AC28, AC31, AC32, AC33, AC34 (assert on tool messages and answers only, no tool-log or workflow records); L2 Decision cell and Options cell L2a (they name the knowledge base); L3 Options cell L3a (it names summarized conversation); L1 Options cell L1b (it names your seed data, which has no store) | — |
| D2b | — | R9 (every tool augmented); AC44 (all six records `augmented` true) | — |
| D2c | R9; AC16 | R8 (retrieval text = name, own docstring, signature for every tool); AC44 (all six `augmented` false; the first `init` makes no model request) | — |
| D3b | AC37, AC38, AC39 | R20 (no per-turn extraction; an agent-callable entity-writing tool, never built by the course — no parameters or criteria supplied); R7 (prompt mentions the entity tool); AC44 (a seventh toolbox record) | — |
| D3c | R12; AC20 | R11 (usage is still computed and reported; nothing acts on it automatically) | — |
| D4b | R15; AC25, AC26, AC36 | R7, AC12 (no summary-expansion policy, no `expand_summary`; the system message does not contain "expand_summary"); R8 (`expand_summary` is not registered); R12, AC20 (the stub is replaced by the summary text itself; no `[Summary ID: …]`); R13, R14, AC24 (summaries keep no link to recoverable originals); R16, AC27 (Summary Memory carries summary text); R21, AC35 (result names no id); AC44 (no `expand_summary` record); L3 Options cell L3a (it names details recovered from summarized conversation); D2 Options cell D2a and D3 Options cell D3a (they name summary expansion) — the course never built this side, so adapt these criteria and list them under *Adapted* | — |
| RR1b | — | R1, AC1 (Oracle tables and five IVF vector indexes — neighbor partitions, target accuracy 95, distance matching the stores'); R2, AC3 (same database across processes); R4, AC7 (settings kept in a table in the same schema); AC8, AC13 (ties are unordered under an approximate index: assert P1 then P5; `fixture_tool_1` and `fixture_tool_4` first in either order); R24 (database user and password from the environment) | — (the suite needs the database container running) |
| RR1c | — | R1, AC1 (PostgreSQL tables with a vector column per vector store); R2, AC3; R4, AC7; AC8, AC13 (as RR1b when an approximate index is used); R24 (connection settings from the environment) | — (the suite needs the database server running) |
| RR2b | — | R22 (adds `search_tavily(query, max_results=5)`, augmented, writing each result as "Title: …\nContent: …\nURL: …" with metadata title, url, score, source_type "tavily_search", query, timestamp — checked live); R24 (`TAVILY_API_KEY`); AC44 (seven records, `search_tavily` augmented true) | — |
| RR2c | — | R22 (adds a tool described as a fake web search that returns two fixed results and writes them like RR2b); AC44 (seven records) | — |
| RR3b | — | AC3, AC5, AC16, AC20, AC21, AC22, AC23, AC24, AC25, AC27, AC28, AC29, AC31, AC32, AC33, AC34, AC35, AC36, AC37, AC38, AC39, AC44 (run against the live model; assert shape — headings, id formats, record counts and fields — not scripted text or request sequences); AC4, AC6, AC11, AC12, AC14, AC17, AC30 (the requests and "no model request" are read from a log of the live client's requests in the `SCRIPTED_MODEL_LOG` line format, not from the stand-in's log) | all offline criteria move to the live run |
| C1b | — | R13 (summaries record no thread); R16, AC27 (every thread's segment lists every summary; the `t-other` segment also shows the summary); AC11 (Summary Memory placeholder is "(No summaries available.)") | — |

Finally, conclude the build by drawing an infra/structure diagram of the app as built — the memory core and its stores, the harness steps around the agent loop, the tools, the model and the CLI — and state exactly: "This is the infra/structure diagram of this app".

## Course Context Pack (embedded — agent-readable)

### CTX-A. The pattern

The course's central buildable pattern — a memory-aware agent over a database memory core:

`memory core (stores) → register tools as memory → build partitioned context → check usage and offload → select tools semantically → bounded tool-calling loop (log tool outputs) → write back (conversation, workflow, entities)`

- **Memory core** — the database is where most of an agent's data traffic flows; memory is external to the model, persistent and structured (Lesson 2). Each memory type gets its own store: conversation and tool logs as relational tables (exact retrieval by thread, time order), knowledge base, workflow, toolbox, entity and summary as vector stores (similarity search) (Lesson 3).
- **Memory manager** — one abstraction offering read and write operations for every store, hiding queries and vector operations from the agent loop (Lesson 3).
- **Toolbox** — tools are procedural memory: stored with embeddings, retrieved per query, so the agent sees a focused toolset instead of every definition (Lesson 4).
- **Partitioned context window** — each store's retrieved content goes into its own Markdown-headed segment with "what this memory is" and "how to use it", making the model aware of its memory (Lessons 3 and 6). Markdown headings work because models learned hierarchical Markdown structure from training data (Lesson 6).
- **Context-window management** — usage is estimated each turn; above the threshold the conversation is compacted into a summary referenced by ID; the model expands summaries just in time (Lessons 5 and 6).
- **Agent loop and harness** — assemble context, invoke the model, act (respond, call tools), until a final answer or the iteration limit; memory operations outside the loop (reads at the start, writes at the end) and inside it (tool calls, tool-log offloading) form the harness (Lesson 6).
- **Write-back** — each turn persists its conversation, the steps it took as a workflow, and the entities it met, so later runs reuse them (Lesson 6).

### CTX-B. Failure-mode catalog

- **B1 Stateless forgetting** — symptom: the agent cannot resolve "book the first one on the list" because it has no record of the previous turn (Lesson 2). Cause: no memory beyond a single turn. Fix: store interaction history per thread outside the model and load it every turn. Enforced by R2, R3, AC3.
- **B2 Tool overload** — symptom: context bloat and confusion, degraded tool selection, higher latency and cost when every tool definition is placed in the prompt (Lesson 4). Cause: tool definitions crowd the context window. Fix: retrieve only the tools relevant to the query. Enforced by R10, AC13, AC17.
- **B3 Context overflow** — symptom: long conversations exhaust the token budget and the agent fails or loses history (Lesson 5). Cause: unbounded conversation in context. Fix: monitor usage and offload conversation into a summary above the threshold. Enforced by R11, R12, AC18, AC20.
- **B4 Summaries lose details** — symptom: an exact earlier detail is gone after summarization (Lesson 5: summarization is lossy; Lesson 6: "what was my first question?"). Cause: the summary replaces the original text. Fix: keep originals linked to the summary id and expand on demand. Enforced by R15, AC25, AC36.
- **B5 Re-summarizing processed messages** — symptom: the same messages are summarized again on each pass (Lesson 5 notebook). Cause: no marker on summarized rows. Fix: tag each summarized row with its summary id and summarize only untagged rows. Enforced by R14, AC24.
- **B6 Empty summary output** — symptom: the model returns no summary text, leaving nothing to store (Lesson 5 code). Cause: model output variability. Fix: one simpler retry, then a deterministic fallback summary. Enforced by R13, AC21.
- **B7 Generic summary labels** — symptom: labels like "Conversation summary" make summary lists useless to the model (end-to-end helper). Cause: weak labeling output. Fix: reject generic labels and derive one from the summary. Enforced by R13, AC22.
- **B8 Tool-output bloat** — symptom: a large tool result floods the next model request (Lesson 6). Cause: raw outputs passed straight back. Fix: keep the full output in the tool log and pass a bounded cut with a pointer. Enforced by R18, AC34.
- **B9 Runaway loop** — symptom: the agent keeps calling tools without answering (Lesson 6). Cause: no stop condition besides a final answer. Fix: an iteration limit with a fixed fallback answer. Enforced by R17, AC31.
- **B10 Duplicate tool records** — symptom: re-running registration stores the same tool again (end-to-end helper). Cause: registration without a name check. Fix: skip names already stored. Enforced by R8, AC14, AC44.
- **B11 Empty workflows** — symptom: workflow memory fills with trajectories that have no steps (end-to-end helper filter). Cause: writing a workflow for every turn. Fix: write only turns with tool calls; read only workflows with steps. Enforced by R19, AC29, AC30.
- **B12 Summaries that mark nothing** — symptom: the model calls the summarize tool without a thread, so source rows are never marked (Lesson 6 code). Cause: a missing argument. Fix: the harness adds the active thread id. Enforced by R21, AC35.
- **B13 The agent cannot look up what it does not know exists** — symptom: an agent left to decide whether to read memory starts from scratch (Lesson 3 notebook). Cause: retrieval left to the model's discretion. Fix: deterministic bootstrap reads every turn. Enforced by R6, AC11.
- **B14 Entity extraction breaks a turn** — symptom: a malformed extraction reply would raise an error mid-turn (end-to-end helper). Cause: unparseable model output. Fix: treat any non-array reply as no entities and never fail the turn on extraction. Enforced by R20, AC39.

### CTX-C. Decision background

**How to read the provenance notes.** Each argued subject was judged by a three-step litmus: *failure* (the course shows or warns that the alternative breaks → the taught side is a **bake-in**, a business rule, and the alternative is recorded as an anti-pattern — tie-breaker 1: a demonstrated or warned failure wins over earlier demos); *working* (the course shows the alternative producing a correct result → both sides are options of a Ledger **row**); otherwise the alternative is **never shown** — a Ledger option that says the course never built it when the subject changes the system's structure (a component, an owner or a guarantee), or **narrative** (background only, never asked and never built) when it does not, or when it is only a stage of the course's progression that the course does not argue stopping at. A subject whose sides differ only in a number is a **lever** (tie-breaker 2): a body value carrying the argument plus an Ask-First entry; a **post-build lever** is such a value that no gate question asks about. A contradicted value is chosen by **value branches**: (1) the value the narration states in the lesson that introduces it; (2) else the course's end-to-end agent's value; (3) else the most frequent value, earliest-taught on ties. **Stakes**: a contradiction becomes a row only if choosing the other side at the start would change structure, semantics or a guarantee. A Default's **Branch** note names the rule that chose it: *the course's example scenario shape* (the project row takes the course's own example, re-expressed on facts this spec authors); *the learner data row* (the data row defaults to a synthetic corpus so the build runs offline); *substitution* (a substitution row, below); *the keyed-tool rule* (a tool that needs a key is left out by default when a keyless tool also carries the behavior it teaches); *the model is the keyed dependency* (the offline suite runs against a scripted stand-in model, and criteria that need a real model are tagged `live`). A **substitution row** replaces a heavy course dependency with a lighter one that keeps the row's invariant; **heavy** means needing a key, a paid account, admin or container setup, or special hardware (network access alone is not heavy). **Realization tiers**, lightest first: (1) ships with the language; (2) an embedded library; (3) a locally served component. "(course default)" marks what the course used; "(Recommended)" marks the Default.

**Mined trade-off table** (every argued or spoken trade-off, its lesson, and its disposition):

| # | Subject | Lesson | Disposition |
|---|---|---|---|
| T1 | Stateless agent vs memory-augmented agent | 2 | bake-in R2, R3 — tie-breaker 1 (the stateless agent fails the follow-up turn) |
| T2 | Conversational memory only vs multiple memory stores | 2, 3 | row D1 (conversation-only shown working in the walkthrough) |
| T3 | Memory-augmented vs memory-aware agent | 3 | narrative — a stage of the progression ("we can take things further") the course never argues stopping at |
| T4 | Deterministic vs agent-triggered memory operations | 3 | row D3; bake-ins R6 (bootstrap reads) and R3, R19 (turn and workflow writes) — tie-breaker 1 (warned: stateless behavior, forgotten saves) |
| T5 | All tools in the prompt vs semantic tool retrieval | 4 | bake-in R10 — tie-breaker 1 (warned: context confusion, selection degradation) |
| T6 | Plain vs LLM-augmented tool descriptions | 4 | row D2 (both shown working) |
| T7 | Local tools vs third-party API tools | 4 | narrative — presented as two kinds of tool, no builder's choice argued |
| T8 | Lossy summarization vs recoverable compaction | 5 | row D4 (lossy never shown; reversibility is a guarantee) |
| T9 | When to summarize: the 80% threshold, ≥ vs >, or manually at any time | 5, 6 | lever R12 — tie-breaker 2 (a value); value branch 2 (> 80) |
| T10 | Token estimate: 4 vs 2 characters per token | 5 | lever R11 — tie-breaker 2 |
| T11 | Different summarization prompts ("try different prompts") | 5 | narrative — an invitation to experiment, no sides argued |
| T12 | Full tool outputs in context vs offloaded to the tool log | 6 | bake-in R18 — tie-breaker 1 (warned: tool-output bloat) |
| T13 | Search-and-store vs search only | 4 | narrative — only the taught side is presented; carried as R22 and the RR2 invariant |
| T14 | Hybrid search for the knowledge base | 3 | narrative — named and set up, never used, no trade-off argued (§1 item 1) |
| T15 | Retrieval strategies: lexical, vector, graph, hybrid | 3 | narrative — a taxonomy |
| T16 | Memory types: semantic cache, working, procedural, semantic, episodic | 2 | narrative — a taxonomy |
| T17 | Conversation in a relational table vs a vector store | 3 | bake-in R3 — tie-breaker 1 (the course states conversation needs exact thread retrieval that similarity search cannot give) |
| T18 | Cosine vs Euclidean distance | 3, 4, 5, 6 | lever R4 — contradicted, stakes fail (a value); value branch 1 (cosine, Lesson 3 narration) |
| T19 | HNSW vs IVF vector index (course database only) | 3 | bake-in for option RR1b — tie-breaker 1 (the helper's index function builds IVF and reports HNSW errors on Oracle Free; the Lesson 3 notebook's text still names HNSW, which loses to the shipped code); not used by RR1a |
| T20 | Tools per turn: 1, 3 or 5 | 4, 6 | lever R10 — contradicted, stakes fail; value branch 2 (5) |
| T21 | Summary thread scoping | 5, 6 | row C1 — contradicted, stakes pass |
| T22 | The course's database vs a lighter local store for the memory core | 2, 3 | row RR1 (realization: the course's database needs container and admin setup) |
| T23 | Candidate search before full-paper ingestion | 4 | narrative — two tools of the course's toolset, no alternative argued |
| T24 | Chunking full papers for embedding input limits (1,500 / 200) | 4 | lever R22 — single-valued, argued only as "chunking prevents failures"; changing after ingestion forces re-fetch |
| T25 | Moving large payloads out of the model context (fetch and store) | 4 | bake-in R22 — the course presents routing the full paper through the model as what the tool avoids |

**Background per row and contradiction.**
- **D1 (→ Ledger D1).** Lesson 2's progression: stateless agent → memory-augmented with conversational memory → beyond conversational memory. Lesson 3 adds explicit memory types, then memory awareness (store awareness in the system prompt, memory operations as tools, context partitions).
- **D2 (→ Ledger D2).** The course's registration computes an embedding from the enriched text but writes the record with the original text as the embedded text; Lesson 4 narration ("this enriched text is what gets embedded") is followed here. Lesson 4 code augments `get_current_time`; the end-to-end registration does not (D2a follows the end-to-end agent).
- **D3 (→ Ledger D3).** The course's operation table: conversation, knowledge-base, workflow and entity reads deterministic; summary-list read agent-triggered (the end-to-end agent nevertheless loads the list every turn); conversation and workflow writes deterministic; entity write agent-triggered; web search, summary expansion and summarization agent-triggered; toolbox read both.
- **D4 (→ Ledger D4).** Compaction stores content under an ID with a description; the model reads the description and fetches the full content only when needed ("just-in-time retrieval").
- **RR1 (→ Ledger RR1).** The course's database setup (admin connection, a dedicated user with an ASSM tablespace for JSON columns, a container that takes 30–60 seconds to start) is the setup weight the substitution avoids.
- **C1 (→ Ledger C1).** Lesson 5's summary writer stores no thread; the end-to-end helper stores it for thread summaries and filters the summary list by thread; text-only summaries record no thread in either.
- **Conversation window.** The course reads the first 10 unsummarized rows in time order (earliest first); this spec shows the 10 most recent, in time order (hardening, R3).
- **Clean-slate tables.** Every lesson notebook drops all seven tables before running; this spec never drops data (R1), because persistence across sessions is the course's purpose.
- **Label fallback.** The Lesson 5 notebook falls back to "Conversation summary"; the end-to-end helper rejects that label as generic (value branch 2, R13).
- **Summary model.** Lesson 5's notebook summarizes with `gpt-5-mini`; the end-to-end helper's summarizer, entity extractor and tool augmenter use `gpt-5`; the agent loop uses `gpt-5-mini`. Current models are chosen at the gate.
- **Unknown tools.** The course returns "Error: Tool '<name>' not found" as an ordinary result and records it as a success in the tool log; this spec keeps that status (R17) and asserts only the result text.
- **Workflow success flag.** The course records success true for every workflow, including turns that hit the iteration limit; this spec keeps that behavior (R19).

### CTX-D. Perishable assumptions

The concepts in CTX-A through CTX-C are durable; only the names below are perishable. Treat them as search keywords against current documentation, not guaranteed imports.

- Installs: the course's `requirements.txt` lists `langchain-oracledb`, `langchain-huggingface`, `sentence-transformers`, `langchain-community`, `langchain-openai`, `datasets`, `langchain`, `tavily-python`, `pydantic`, `oracledb`, `openai`, `dotenv`, `arxiv`, `pymupdf` — all unpinned.
- Vector store: `langchain_oracledb.vectorstores.OracleVS`; `langchain_oracledb.retrievers.hybrid_search.OracleVectorizerPreference`; `langchain_community.vectorstores.utils.DistanceStrategy` (`COSINE`, `EUCLIDEAN_DISTANCE`, `DOT_PRODUCT`); Oracle `CREATE VECTOR INDEX … ORGANIZATION NEIGHBOR PARTITIONS … WITH TARGET ACCURACY 95`.
- Database: Oracle AI Database 26ai Free, service `FREEPDB1`, driver `oracledb`.
- Embeddings: `HuggingFaceEmbeddings` imported from `langchain_huggingface` in Lessons 3 and 5 and from `langchain_community.embeddings` in Lessons 4 and 6; model `sentence-transformers/paraphrase-mpnet-base-v2`.
- Paper tools: `langchain_community.retrievers.ArxivRetriever` (`load_max_docs`, `get_full_documents`, `doc_content_chars_max`), `langchain_community.document_loaders.ArxivLoader`, `langchain_text_splitters.RecursiveCharacterTextSplitter`; arXiv metadata keys "Entry ID", "Title", "Authors", "Published".
- Seed dataset: `datasets.load_dataset("nick007x/arxiv-papers", split="train", streaming=True)`.
- Web search: `tavily.TavilyClient().search(query=…, max_results=…)`.
- Model API: OpenAI `client.chat.completions.create` with `tools` and `tool_choice="auto"`; tool results as `role="tool"` messages with `tool_call_id`; models `gpt-5` and `gpt-5-mini`.
- **Request-parameter compatibility:** the course's calls set `max_completion_tokens` (4,000 for summaries; 2,000 for labels, augmentation, query generation and entity extraction) and never set `temperature` or `max_tokens`. Parameter support differs between model families; check the chosen model's accepted parameters before the first keyed run.

### CTX-E. Provenance map

Lesson titles in transcript numbering. Nothing in this spec requires course-platform access.

| Lesson | Title | Contributes |
|---|---|---|
| 1 | Introduction | CTX-A (memory engineering framing); §1 item 5 |
| 2 | Why AI Agents Need Memory | CTX-A (memory core, agent memory definition); CTX-B1; CTX-C T1, T2, T16, T22; §1 items 2–3 |
| 3 | Constructing The Memory Manager | CTX-A (stores, memory manager, memory-aware steps); CTX-B13; CTX-C T2, T3, T4, T14, T15, T17, T18, T19, T22; §1 items 1, 4–6 |
| 4 | Scaling Agent Tool Use with Semantic Tool Memory | CTX-A (toolbox); CTX-B2, B10; CTX-C T5, T6, T7, T13, T18, T20, T23–T25 |
| 5 | Memory Operations: Extraction, Consolidation, and Self-Updating Memory | CTX-A (context management); CTX-B3–B7; CTX-C T8–T11, T18, T21 |
| 6 | Memory Aware Agent | CTX-A (agent loop, harness, write-back); CTX-B8, B9, B11, B12, B14; CTX-C T9, T12, T18, T20, T21 |
| 7 | Conclusion | CTX-A (patterns summary) |

- **Notebook-to-lesson mapping.** The notebook dump's own lesson map pairs L2 with Lesson 4, L3 with Lesson 5 and L4 with Lesson 6, but each notebook's title and content match the transcripts one lesson earlier: L2 "Constructing the Memory Manager" = Lesson 3, L3 "Scaling Agent Tool Use with Semantic Tool Memory" = Lesson 4, L4 "Memory Operations" = Lesson 5, L5 "Memory Aware Agent" = Lesson 6. The narration itself also drifts ("you've completed lesson 4" at the end of Lesson 5; "end of lesson 5" at the end of Lesson 6). Transcript headers win throughout this spec.
- **Code-side evidence** comes from the notebooks and the shared helper module (memory manager, store manager, toolbox, summarization, common tools), including its docstrings (the IVF-over-HNSW reason, chunking for embedding input limits).
- **Slides:** the course folder holds slide images only, with no slide-descriptions file; no slide was read or weighted.
- **Name map to the course's terms:** stores `CONVERSATIONAL_MEMORY`, `SEMANTIC_MEMORY`, `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY`, `TOOL_LOG_MEMORY` (binding here); the course's classes `MemoryManager`, `StoreManager`, `Toolbox`, `ToolMetadata`; its loop `call_agent` with `AGENT_SYSTEM_PROMPT`; its functions `calculate_context_usage`, `monitor_context_window`, `summarise_context_window`, `summarize_conversation`, `offload_to_summary`; its tools `read_toolbox`, `search_tavily`, `get_current_time`, `arxiv_search_candidates`, `fetch_and_save_paper_to_kb_db`, `expand_summary`, `summarize_and_store` (tool names binding here). The course's research assistant was called "ArxivScout" in Lesson 3.
- **Declared drops (presentation-only constants):** print-display cuts (70 and 200 characters), the 0.05-second delay between seeded messages (replaced by the insertion-order rule), connection program name, DSN and passwords, index names `*_vs_ivf`, the hybrid-search preference name, demo thread ids ("50000", "test_summary_<time>"), and the sample conversation's stated length (30 in code, 32 in narration).

---
v1 · Agent Memory: Building Memory-Aware Agents · learner project: [project] (default: memory-aware research assistant agent, row L1) · Living document: when the build agent produces something unexpected, add the missing constraint here and re-run.
