# Spec: Memory-Aware Research Assistant — Standalone Takeaway

> **This file is self-contained.** The embedded **Course Context Pack** at the end replaces
> all external course references — nothing in this spec requires access to the course
> platform, notebooks, or transcripts. `(CTX-X)` anchors mark course-derived knowledge.
> The **Decision Ledger** below holds every point where the build could legitimately
> diverge; every row is pinned to one course-derived default, so this spec is buildable
> and evaluatable **as-is with zero intake**. `[bracketed]` values mark where a learner
> *may* substitute their own choice — they are never gaps.
>
> *Provenance: generated from the "Agent Memory: Building Memory-Aware Agents" course
> notebooks (L2–L5 dump + helper.py + requirements.txt) and lesson transcripts
> (Lessons 1–7) on 2026-07-15.*

## 0. Before you build — REQUIRED (do this first)

You are the build agent. Before writing ANY code, you MUST surface the design decisions
in the Decision Ledger (next section) to the person you are building for. Do **not** skip
this because the defaults look complete — the defaults exist so the build is *reproducible*,
not because they are the right choice for this person's project.

1. **Use a structured question tool if you have one.** If your environment offers an
   interactive structured-question tool (e.g. Claude Code's `AskUserQuestion`, or the equivalent
   in yours), you MUST use it to present the decisions — do not paraphrase them into a prose
   paragraph. Only if no such tool exists, list the rows in your reply and ask the user to
   respond to each.
2. **Present the Ledger ONE ROW AT A TIME — one question per row.** For each row ask a single
   question: the **Decision** as the prompt, its **Options** as the choices with the **course
   default** marked — append "(course default)" to that option's label, NEVER "(Recommended)";
   if your question tool's own guidance suggests a "Recommended" labeling convention, do not
   use it here (the default is factual course provenance, not advice for this person's
   project). Put any realizations beyond the tool's option slots (or the free-form case)
   under the tool's "Other"/free-text. Ask about **every** row (there are 18). A per-call item
   limit is NEVER a reason to drop, skip, merge, or silently default a row — make as many
   separate calls as there are rows.
3. **Presenting the decisions ENDS YOUR TURN — stop here; write no code, create or edit no file,
   take no other build action.** Keep asking, one row at a time, until **every** row has an
   answer (a chosen option, or an explicit "use the course default"). Answers to *some* rows do
   NOT release the build; "no reply yet" is not an answer — wait for the user.
4. **Before the first line of code, print a resolved-decision checklist** — every Ledger row
   with its final value (the user's choice, or "course default"). Begin implementation ONLY
   after this complete checklist is shown; if any row is unresolved you are not done — return to
   step 2. Build on the checklist's values.

## Decision Ledger (§0 above requires the build agent to present these before building)

These are the points where this build could diverge. Every row has a course-derived
default, so the spec is buildable and evaluatable as-is; change a row only when applying
to a real project or when you have reason to prefer another option. "Default" is factual
provenance — what the course did, or the stated substitution branch — not a recommendation
for your specific project.

| # | Category | Decision | Invariant (must hold) | Default (course-derived) | Options | Trade-off | Owner |
|---|----------|----------|----------------------|--------------------------|---------|-----------|-------|
| 1 | design-argued | Memory-store topology | Seven distinct memory types exist as separate stores: Conversational and Tool Log in an exact-key, time-ordered relational store; Knowledge Base, Workflow, Toolbox, Entity, and Summary in semantic-similarity (vector) stores with metadata filtering. One manager class fronts all reads/writes. | The 7-store layout exactly as taught: 2 SQL tables (`CONVERSATIONAL_MEMORY`, `TOOL_LOG_MEMORY`) + 5 vector stores (`SEMANTIC_MEMORY`, `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY`), unified behind a `MemoryManager` (CTX-A, CTX-C1). | Merge some vector types into one collection with a type field; add graph store; fewer memory types. | Lesson 3 argues it aloud: conversational memory needs *exact retrieval by thread id, not similarity*, so it must not live in a vector store; each memory type has distinct data-model + retrieval needs. Merging types loses per-type retrieval strategies and the memory-aware prompt segmentation. | course |
| 2 | design-argued | Deterministic vs agent-triggered operation split | Context-bootstrapping reads and post-turn persistence run deterministically every turn (never at the model's discretion); judgment-heavy operations (deep retrieval, summary expansion, external search) are agent-triggered tools. Conversation summarization is reachable BOTH ways: deterministically at the context threshold and as an agent tool. | The Lesson 6 loop's split: deterministic = read conversational/KB/workflow/entity/summary-context at loop start, write user msg + final answer + workflow + entities + tool logs; agent-triggered = `expand_summary`, `summarize_and_store`, knowledge-acquisition tools; `read_toolbox` is both (CTX-C2). | Make more ops agent-triggered (leaner, riskier); make summarization deterministic-only. | Lesson 3 narrates the argument: "the agent can't choose to look up what it doesn't know exists — you need memory to know which memory you need"; deterministic ops buy predictability/continuity, agent-triggered ops buy signal-to-noise and cost control. NOTE the course self-contradicts in detail: the Lesson 3 classification table marks `read_summary_context` and `write_entity` agent-triggered, but the Lesson 6 loop executes both deterministically every turn. Default follows the Lesson 6 loop (the end-to-end app). | course |
| 3 | design-argued | Context-reduction strategy | Reducing context must be *recoverable*: any compression stores a link back to the original units, and an agent-callable expansion path exists. The current `# Question` is never summarized away. | Recoverable compaction as taught: LLM summarization into structured summaries stored with `summary_id`, source conversation rows marked with that id, `expand_summary(id)` retrieves summary + all original messages (CTX-B4, CTX-C3). | Pure lossy summarization (no write-back links); sliding-window truncation; no reduction. | Lesson 5 argues it explicitly: summarization "will always be a lossy technique"; compaction offloads to the database with an ID + description so the model can pull full detail back on demand. Dropping the link severs recoverability. | course |
| 4 | design-argued | Tool exposure to the LLM | The LLM never receives the full toolbox. Tools live in a searchable vector store keyed on their (optionally augmented) descriptions; per query, only the top-k semantically relevant tools are passed, deduplicated by name. | Toolbox vector store + semantic retrieval, `k=5` at the agent loop (CTX-C4). | Static hand-picked toolset per agent; all tools in every prompt (only viable for very few tools). | Lesson 4 argues the failure: too many tool definitions cause context confusion/bloat, tool-selection degradation, higher latency and cost; the notebook cites provider guidance of ~10–20 tools max for reliable selection, with 3–5 retrieved typically. | course |
| 5 | design-argued | Tool docstring augmentation | Each registered tool is retrievable by semantic search over a text that includes at least its name, description, and signature. | Augment heavy/ambiguous tools at registration: an LLM rewrites the docstring from docstring + source code, plus ~5 synthetic trigger queries, and that enriched text is embedded (`augment=True`). Final-lesson config: `fetch_and_save_paper_to_kb_db`, `expand_summary`, `summarize_and_store` augmented; `arxiv_search_candidates`, `get_current_time` registered raw (helper `register_common_tools`). | Raw docstrings only (cheaper registration, weaker separability); augment everything. | Lesson 4 argues augmentation gives better separability in embedding space, higher recall, higher-signal embedding text — at the cost of LLM calls per registration. Minor course drift: the Lesson 4 notebook registered `get_current_time` with `augment=True`; the final helper registers it raw. Default follows the final helper. | course |
| 6 | design-structural | Partitioned context window + memory-aware system prompt | The prompt context is assembled as a `# Question` section followed by one markdown `##` segment per memory type (Conversation, Knowledge Base, Workflow, Entity, Summary), each carrying what-this-memory-is and how-to-use-it guidance; the system prompt names the segments, their semantics, the summary-expansion policy, and a conflict-priority order (Question > latest Conversation > KB evidence > older summaries/workflows). | Exactly that structure, as taught in Lesson 6 (CTX-C5). | One undifferentiated context blob; JSON-structured context. | Lesson 6 explains the mechanism: markdown headings let the LLM exploit its latent grasp of hierarchical structure, making the agent *aware* of its memories instead of merely augmented by them. Restructuring the segments changes what every memory read returns (each read formats its own segment). | course |
| 7 | realization | Persistent store technology | One durable local system providing (a) exact-key relational tables with timestamp ordering for Conversational + Tool Log memory and (b) vector similarity search **with metadata filtering** (equality and numeric `$gt`) for the 5 vector stores. All memory survives process restarts. | **SQLite (two relational tables) + Chroma `PersistentClient` (five collections), both under `./data/`.** §3 dependency-precedence **branch 1**: the course realizes this on Oracle AI Database 26ai in Docker (admin bootstrap, `VECTOR` user, DSN `127.0.0.1:1521/FREEPDB1`), a heavy dependency that merely realizes the taught dual-store pattern — the pattern, not Oracle, is the subject, so the default substitutes the lightest self-contained equivalent. | Oracle AI Database 26ai + `langchain-oracledb` `OracleVS` (course-faithful; needs Docker + admin setup); Postgres + pgvector; any store meeting the invariant. | Switching store later means migrating rows and re-creating indexes; Oracle adds infra setup cost but restores 1:1 fidelity with course APIs (OracleVS, hybrid-search preference, IVF indexes). | course+learner |
| 8 | realization | Knowledge-acquisition toolset | At least one agent-triggered tool acquires external knowledge and **persists what it finds to the Knowledge Base** (the search-and-store pattern), so discovered information is reusable without re-fetching. | The final lesson's common toolset: `arxiv_search_candidates` (metadata-only discovery) + `fetch_and_save_paper_to_kb_db` (full PDF→text, chunked 1500/200, stored with metadata) + `get_current_time`, plus the summary tools. **Tavily web search is NOT in the default build** — §3 branch 1: it needs a paid API key and the final lesson's agent doesn't register it; the search-and-store pattern it demonstrated is preserved by the arXiv ingestion tool. | Add `search_tavily` (course showed it in Lesson 4; requires `TAVILY_API_KEY`); substitute your own domain's fetch/search tools. | Tavily gives open-web reach at key + cost; arXiv tools are keyless but network-dependent and domain-narrow. | course+learner |
| 9 | realization | Knowledge-base seed data | The KB starts non-empty so retrieval grounding is demonstrable on day one; each record carries searchable text (title+subjects+abstract concatenated) and metadata for filtering/attribution. | **The synthetic fixture corpus defined in §5** (6 self-authored paper records baked into this repo). §3 branch 1: the course streamed 100 records from the HuggingFace dataset `nick007x/arxiv-papers` — an external download that can't be baked into this file; the fixture corpus preserves the record shape (title, subjects, abstract, submission_date, arxiv_id). | The HF dataset (course-faithful); the learner's own documents. | Fixtures make acceptance tests deterministic/offline; the HF stream gives realistic scale but non-reproducible content and a network dependency. | course+learner |
| 10 | learner | Project — [project] | — (the pattern imposes nothing) | A **memory-aware research-assistant chat agent** (CLI), the course's own running example shape ("agentic research assistant … over multiple sessions", a.k.a. ArxivScout), instantiated on the §5 fixture corpus. §3 project precedence **branch 1** (course example shape on synthetic fixtures). | Any project the learner wants to graft the pattern onto. | Retitling to a real project means re-deriving fixtures and goals; the default is judged by §5 as-is. | learner |
| 11 | learner | Data / inputs — [data] | — | Synthetic fixture corpus (§5) + live arXiv metadata/PDFs fetched on demand by the row-8 tools. | Learner's own corpus/APIs. | Real data invalidates the fixture-based ACs until equivalents are authored. | learner |
| 12 | learner | Goal / definition of "working" — [goal] | — | Pass all §5 acceptance criteria: cross-session continuity, capped semantic tool retrieval, threshold-triggered recoverable compaction, summary expansion, audit-logged tool execution. | Learner-defined retrieval/answer guarantees. | — | learner |
| 13 | learner | Model / provider — [model] | Must support **native tool/function calling** (tools + tool-role result messages in a chat API) and a system role. | **OpenAI Chat Completions, model `gpt-5-mini`** — the model the Lesson 6 agent loop calls. NOTE the course self-contradicts on the name: the Lesson 5 notebook uses `gpt-5-mini` (token-limit table `{"gpt-5-mini": 256000}`), while helper.py uses `gpt-5` everywhere (token table, Toolbox default, entity extraction). Default follows the agent loop; treat both names as perishable (CTX-D). | Any tool-calling chat model/provider. | Swapping providers means re-mapping the tool-call message format; summary/augmentation prompt behavior may shift. | learner |
| 14 | learner | Environment — [environment] | Memory MUST survive process restarts (the whole point of the course); secrets come from the environment, never hardcoded. | Local machine, Python 3.11+ virtualenv, file-backed stores under `./data/`, `OPENAI_API_KEY` loaded from `.env`. | Containers, cloud, notebooks. | — | learner |
| 15 | learner | Out of scope — [out-of-scope] | — | Exactly the §1 "Not Included" list. | Learner may pull items in or push more out. | — | learner |
| 16 | contradicted | Vector distance strategy | All five vector stores use the **same** distance strategy as each other and as their indexes, chosen once before any data is embedded. | **EUCLIDEAN (L2)** — the final application's config: the Lesson 5 and Lesson 6 notebooks both construct the StoreManager with `DistanceStrategy.EUCLIDEAN_DISTANCE`. The course contradicts itself: the Lesson 3 and Lesson 4 notebooks (and the Lesson 3 narration, "which in this case is going to be cosine") use `COSINE`, and the Lesson 3 notebook's own intro table says EUCLIDEAN while its code says COSINE. Default follows the end-to-end app config per the multiple-configs rule. | COSINE (Lessons 3–4 config); DOT product. | Changing strategy after ingest invalidates similarity semantics and requires re-indexing; mixed strategies across lessons is exactly the stale-data hazard the notebooks' "drop all tables for a consistent distance strategy" warning exists for. | course |
| 17 | contradicted | Toolbox retrieval k | Tool retrieval returns a small bounded set (course guidance: providers recommend ~10–20 tools max exposed; typically 3–5 retrieved). | **k=5 at the agent loop** (Lesson 6 `read_toolbox(query, k=5)`). The course contradicts itself: `MemoryManager.read_toolbox` signature defaults `k=3`; the Lesson 4 registered `read_toolbox` tool's signature says `k: int = 3` while its own docstring says "default: 5". Keep the manager default 3 and pass 5 in the loop, matching the course's call site. | Any small k. | Larger k re-introduces the context-bloat/selection-degradation failure the toolbox pattern exists to prevent (Lesson 4). | course |
| 18 | contradicted | Vector index type | Every vector store has an ANN index created before serving queries; index distance matches row 16. | Follow the row-7 default store's native ANN index (Chroma manages its own). If Oracle is chosen: **IVF** (`ORGANIZATION NEIGHBOR PARTITIONS … WITH TARGET ACCURACY 95`) — what the course's `safe_create_index` actually creates. The course contradicts itself: Lesson 3's notebook markdown and lesson objectives narrate an **HNSW** index, but the helper deliberately uses IVF to dodge Oracle Free bugs (ORA-00600, ORA-51928, ORA-51962). | HNSW (as narrated); IVF (as coded). | HNSW was shown to be crash-prone on the course's own Oracle build; IVF trades some recall for stability there. | course |

## 1. Objective

Build a persistent, memory-aware research-assistant agent: a chat loop that, on every
turn, deterministically assembles a partitioned context from seven typed memory stores,
manages its own context-window budget by recoverable compaction, selects tools by
semantic search instead of prompt-stuffing, executes them with full audit logging, and
writes what it learned back to memory — so the agent resumes, remembers, and improves
across sessions instead of resetting (pattern: CTX-A).

### Not Included ★

- **Tavily / open-web search** — demonstrated in Lesson 4 but not registered in the final
  agent; excluded by default (Ledger row 8).
- **Hybrid (lexical+vector) search** — the course's StoreManager stubs a
  `setup_hybrid_search` vectorizer preference but never exercises it end-to-end; do not build it.
- **Semantic cache** — named in Lesson 2 as a short-term memory form, never implemented.
- **Reranking models / graph traversal retrieval** — mentioned in the RAG/lifecycle
  overviews only.
- **Memory decay, merging, strengthening** — named as agent-triggered judgment examples,
  never implemented.
- **Multi-user auth, web UI, deployment** — outside course scope entirely.
- **Fine-tuning embedding or language models** — mentioned as part of the memory-engineering
  discipline, not built.
- Anything in `[out-of-scope]` (Ledger row 15).

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python 3.11+ | Course-era Python; pick the current stable 3.x at build time. |
| LLM API | `openai` SDK, current 1.x; model `gpt-5-mini` | Ledger row 13. Course calls `chat.completions.create` with `tools`, `tool_choice="auto"`, `max_completion_tokens`. |
| Embeddings | `sentence-transformers`, model `sentence-transformers/paraphrase-mpnet-base-v2` | Course-consistent across all lessons; produces 768-dim vectors (Lesson 3 notebook). Course loads it via LangChain's `HuggingFaceEmbeddings` (two different import paths across lessons — CTX-D); loading it directly through `sentence-transformers` is equivalent for this build. |
| Relational store | SQLite (stdlib `sqlite3`) | Ledger row 7 default. Two tables mirroring the course schemas (§3). |
| Vector store | `chromadb` (PersistentClient), current release | Ledger row 7 default; five collections, l2 (euclidean) space per Ledger row 16. |
| Chunking | `langchain-text-splitters` `RecursiveCharacterTextSplitter` (or behavior-equivalent) | chunk_size=1500, chunk_overlap=200 — the course's `fetch_and_save_paper_to_kb_db` defaults. |
| arXiv access | `langchain-community` `ArxivRetriever`/`ArxivLoader` + `arxiv` + `pymupdf` | Ledger row 8. Retriever config: `load_max_docs=8`, `get_full_documents=False`, `doc_content_chars_max=4000`. |
| Env/secrets | `python-dotenv`; `OPENAI_API_KEY` in `.env` | **Never hardcode credentials.** (The course notebooks hardcode Oracle DB passwords; do not reproduce that.) |
| **Install/pin honesty** | — | **The course's `requirements.txt` is entirely unpinned** (it even says models/libraries "will naturally change over time"); no version claims below come from the course. Pin whatever current versions you install into this build's own lockfile, and treat every course-era API name as a search keyword, not a guaranteed import (CTX-D). |

## 3. Input/Output Contracts ★

Core turn contract. `call_agent`-equivalent entry point takes a query + thread id and
returns a structured result *(structured return object is project hardening — the course
returned a bare string; the fields below are all course-demonstrated data)*:

```json
{
  "$id": "AgentTurnResult",
  "type": "object",
  "required": ["thread_id", "query", "answer", "iterations_used", "steps", "context_usage"],
  "properties": {
    "thread_id": {"type": "string"},
    "query": {"type": "string"},
    "answer": {"type": "string", "minLength": 1},
    "iterations_used": {"type": "integer", "minimum": 1, "maximum": 10},
    "steps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["tool_name", "status"],
        "properties": {
          "tool_name": {"type": "string"},
          "status": {"enum": ["success", "failed"]},
          "tool_log_id": {"type": "string"}
        }
      }
    },
    "summaries_created": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "description"],
        "properties": {
          "id": {"type": "string", "minLength": 8, "maxLength": 8},
          "description": {"type": "string", "minLength": 1}
        }
      }
    },
    "context_usage": {
      "type": "object",
      "required": ["tokens", "max", "percent", "status"],
      "properties": {
        "tokens": {"type": "integer", "minimum": 0},
        "max": {"type": "integer"},
        "percent": {"type": "number"},
        "status": {"enum": ["ok", "warning", "critical"]}
      }
    }
  }
}
```

*(Loop-exhaustion behavior — the templated inability answer — is asserted behaviorally by
R9/AC13 rather than in-schema, because a genuine final answer may legitimately arrive on
the 10th iteration.)*

Memory-unit contracts (course-demonstrated; storage columns from the Lesson 3 schemas):

```json
{
  "$id": "ConversationalMemoryUnit",
  "type": "object",
  "required": ["id", "thread_id", "role", "content", "timestamp"],
  "properties": {
    "id": {"type": "string"},
    "thread_id": {"type": "string"},
    "role": {"type": "string"},
    "content": {"type": "string"},
    "timestamp": {"type": "string", "format": "date-time"},
    "metadata": {"type": "string"},
    "summary_id": {"type": ["string", "null"], "$comment": "null = not yet summarized; non-null links to SummaryRecord.id"}
  }
}
```

```json
{
  "$id": "ToolLogRecord",
  "type": "object",
  "required": ["id", "thread_id", "tool_name", "status", "timestamp"],
  "properties": {
    "id": {"type": "string"},
    "thread_id": {"type": "string"},
    "tool_call_id": {"type": ["string", "null"]},
    "tool_name": {"type": "string"},
    "tool_args": {"type": "string", "$comment": "JSON-serialized args"},
    "result": {"type": "string", "$comment": "FULL result, never truncated here"},
    "result_preview": {"type": "string", "maxLength": 2000},
    "status": {"enum": ["success", "failed"]},
    "error_message": {"type": ["string", "null"]},
    "metadata": {"type": "string"},
    "timestamp": {"type": "string", "format": "date-time"}
  },
  "if": {"properties": {"status": {"const": "failed"}}},
  "then": {"required": ["error_message"]}
}
```

```json
{
  "$id": "SummaryRecord",
  "type": "object",
  "required": ["id", "summary", "description", "full_content"],
  "properties": {
    "id": {"type": "string", "minLength": 8, "maxLength": 8},
    "full_content": {"type": "string"},
    "summary": {
      "type": "string",
      "$comment": "MUST contain the four headings: ### Technical Information, ### Emotional Context, ### Entities & References, ### Action Items & Decisions"
    },
    "description": {"type": "string", "minLength": 1},
    "thread_id": {"type": ["string", "null"]}
  }
}
```

Workflow record text: `Query: <q>\nSteps:\nStep 1: …\nAnswer: <first 200 chars>` with
metadata `{query, success, num_steps, timestamp}`. Entity record: `<name> (<TYPE>): <description>`
with metadata `{name, type, description}`, `type ∈ {PERSON, PLACE, SYSTEM}` (or UNKNOWN).
Toolbox record metadata carries `{name, description, signature, parameters, return_type, augmented, queries?}`
and retrieval converts it to an OpenAI function schema (`{type:"function", function:{name, description, parameters}}`),
mapping Python annotation strings to JSON-schema types and marking parameters without defaults as required.

## 4. Business Rules

Each rule: behavior + the failure it prevents + enforcement. Labels per §9 of the
generation guide: **[C]** course-demonstrated, **[H]** project hardening.

1. **[C] Deterministic conversational persistence & recall.** Every user query and every
   final assistant answer is written to conversational memory with role, thread_id, and
   timestamp — every turn, unconditionally. Context assembly reads the thread's
   *unsummarized* messages (default limit 10), timestamp-ascending. Prevents the stateless
   reset where the agent can't resolve "the first one on the list" (CTX-B1). → AC1, AC2
2. **[C] Partitioned context, question preserved.** The prompt context is
   `# Question` + `## Conversation Memory` + `## Knowledge Base Memory` + `## Workflow Memory`
   + `## Entity Memory` + `## Summary Memory`, each segment self-describing (what it is /
   how to use it / retrieved items). The question is prepended AFTER any offload and is never
   summarized. The system prompt encodes the segment semantics, the summary-expansion policy,
   the conflict priority (Question > latest Conversation > KB evidence > older
   summaries/workflows), minimal-tool-call guidance, and the instruction to pass `thread_id`
   to conversation compaction (CTX-C5). → AC3, AC17
3. **[C] Capped semantic tool retrieval.** Per query, the LLM receives only the top-k
   (k=5, Ledger row 17) tools from toolbox similarity search, deduplicated by tool name,
   as OpenAI-format function schemas. The full toolbox is never sent. Prevents context
   bloat / tool-selection degradation (CTX-B2). → AC4, AC5
4. **[C] Context budgeting.** Estimated tokens = `len(context) // 4`; max = 256,000 for the
   default model, 128,000 fallback for unknown models; status `ok` <50%, `warning` <80%,
   `critical` ≥80% *(source: Lesson 5 notebook `calculate_context_usage`/`monitor_context_window`;
   helper.py duplicates them keyed on `gpt-5`)*. When memory-context usage exceeds 80%
   before reasoning, offload runs deterministically: the thread's unsummarized messages are
   summarized, the `## Conversation Memory` section is replaced by a pointer stub, a
   `[Summary ID: <id>] <description>` reference is appended under `## Summary Memory`, and
   all other segments are preserved (CTX-B3). **[H]** The token limit MUST be overridable
   (env var or parameter) so acceptance tests can trip the threshold with small fixtures. → AC6
5. **[C] Recoverable, structured summarization.** Summaries are produced by an LLM prompt
   requiring exactly the four headings (Technical Information / Emotional Context /
   Entities & References / Action Items & Decisions), on input clipped to 6,000 chars,
   `max_completion_tokens=4000`; an 8–12-word description label is generated separately;
   `id` = first 8 chars of a UUID4. The summary stores the full original content and, when
   thread-scoped, the thread_id. Source conversation rows are marked with the `summary_id`.
   `expand_summary(id)` returns the summary text plus ALL original messages chronologically
   with timestamps (CTX-B4). → AC7, AC8
6. **[C] No re-summarization.** Rows with a non-null `summary_id` are excluded from
   conversational reads and from future summarization; summarizing a fully-summarized
   thread returns a "nothing to summarize" outcome, not an error (CTX-B5). → AC9
7. **[C] Summarizer never returns empty.** If the model's summary comes back empty, retry
   once with a simpler prompt; if still empty, emit the deterministic fallback (four
   headings, excerpt of the source under Technical Information). If the description label
   is empty or generic ("Conversation summary" etc.), derive a specific fallback label from
   the summary text (CTX-B6). → AC10
8. **[C] Full-fidelity tool audit log.** Every tool invocation — success or failure — writes
   a tool-log record with full args, FULL result, ≤2000-byte UTF-8-safe preview, status,
   error message, and iteration metadata. The LLM's next turn receives at most 3,000 chars
   of a tool result; longer results are truncated with a pointer naming the tool-log id
   where the full payload lives (CTX-B7). Tool logs are read just-in-time (newest-first,
   default limit 20), NOT preloaded into the context. → AC11, AC12
9. **[C] Bounded agent loop.** The reason/act loop runs at most 10 iterations; a tool
   exception is caught, logged as a `failed` step, and its error string returned to the
   model — never a crash; on exhaustion the answer is the templated inability message
   ("I was unable to complete the request within the allowed iterations.") (CTX-B8). → AC13
10. **[C] Post-turn learning writes.** After a turn that used ≥1 tool, write one workflow
    record (query, ordered steps with status, answer truncated to 200 chars,
    success, num_steps). Workflow reads filter to `num_steps > 0` (k=3). Entity extraction
    (LLM, types PERSON/PLACE/SYSTEM, input clipped to 500 chars) runs on the user query and
    on the final answer; extraction failures are swallowed silently (the turn never fails
    because entity extraction did). → AC14
11. **[C] Idempotent tool registration.** Registering a tool whose name already exists in
    the toolbox store skips the store write but still binds the callable; toolbox retrieval
    returns unique names. → AC15
12. **[C] Search-and-store ingestion.** Knowledge-acquisition tools persist what they fetch:
    full-document ingestion chunks at 1500/200 and writes every chunk with metadata
    (source, arxiv_id, title, entry_id, published, authors, chunk_id, num_chunks,
    ingested timestamp); batch writes require equal-length text/metadata lists and reject
    mismatches; discovery returns structured JSON candidates (arxiv_id, entry_id, title,
    authors, published, abstract ≤2500 chars) without ingesting. Empty extraction or no
    results return explanatory strings, not exceptions. → AC16
13. **[C] KB read grounding.** `read_knowledge_base` (k=3) returns the KB segment with
    retrieved passages, and its guidance text instructs the model to ground claims in the
    passages and state uncertainty when evidence is missing rather than assume. → AC3 (segment
    content), AC17 (prompt rule)

## 5. Acceptance Criteria ★ (the oracle)

### Fixture corpus (define FIRST; all facts authored here — none copied from the course)

All fixtures live in `fixtures/`. **The building agent MUST NOT modify fixtures to make a
test pass.**

- `fixtures/papers.jsonl` — 6 synthetic paper records, fields
  `{arxiv_id, title, subjects, abstract, submission_date}`; seeded into the KB at setup
  (text = title+subjects+abstract concatenated, remaining fields as metadata):
  1. `9901.00001` — "Orchid: A Memory Layer for Conversational Agents" — cs.AI —
     abstract states: *"Orchid introduces an episodic buffer that survives restarts and
     reduced repeat lookups by 41% in synthetic trials."* — 2024-01-15
  2. `9902.00002` — "Sparrowhawk: Tool Selection Under Context Pressure" — cs.CL —
     abstract states: *"Sparrowhawk shows selection accuracy collapsing once more than 24
     tool schemas share a prompt."* — 2024-02-20
  3. `9903.00003` — "Ledgerline: Auditable Tool Logs for Agent Pipelines" — cs.SE —
     abstract states: *"Ledgerline records full tool payloads out-of-band and passes only
     bounded excerpts to the model."* — 2024-03-05
  4. `9904.00004` — "Foldback: Recoverable Summarization for Long Dialogues" — cs.CL —
     abstract states: *"Foldback links every summary to its source utterances so detail is
     recoverable on demand."* — 2024-04-11
  5. `9905.00005` — "Cartographer: Entity Graphs from Chat Transcripts" — cs.IR —
     abstract states: *"Cartographer tags people, places, and systems from raw dialogue."*
     — 2024-05-30
  6. `9906.00006` — "Quillwork: Procedural Memory for Multi-Step Agent Workflows" — cs.AI —
     abstract states: *"Quillwork replays stored step sequences to cut planning tokens."*
     — 2024-06-18
- `fixtures/thread_long.json` — a synthetic 12-message user/assistant conversation
  (thread `t-long`) about planning a literature review codenamed **"Atlas Review"** for a
  user named **Priya**; message 1 (user) is exactly:
  *"Which paper introduced the Orchid memory layer?"*; later messages record the decision
  *"target venue: Journal of Synthetic Benchmarks"* and an action item
  *"draft the related-work section by Friday"*. Deliberate instance of CTX-B1/B3/B4/B5.
- `fixtures/long_payload.txt` — ≥5,000 characters of synthetic prose (authored filler
  paragraphs about the six fixture papers). Deliberate instance of CTX-B7.
- `fixtures/extra_tools.py` — four no-op fixture tools with distinct docstrings:
  `convert_temperature`, `roll_dice`, `count_words`, `reverse_string`; registered
  (unaugmented) in tests to exceed the retrieval cap. Deliberate instance of CTX-B2.
- `fixtures/stub_llms.py` — two fake chat clients: `EmptyLLM` (returns empty content on
  every call — CTX-B6) and `ToolLoopLLM` (returns a `get_current_time` tool call on every
  call, never a final answer — CTX-B8).

### Given / When / Then

| AC | Given | When | Then |
|----|-------|------|------|
| AC1 | Fresh stores; live agent | `call_agent("Hello, note that my project is Atlas Review", thread_id="t1")` completes | Conversational store has ≥2 rows for `t1`: the exact user query (role `user`) and a non-empty final answer (role `assistant`), timestamp-ordered, `summary_id` null. |
| AC2 | AC1 has run; **a new process is started** (restart) | `call_agent("What was my first question?", thread_id="t1")` | The assembled context's `## Conversation Memory` segment contains the AC1 messages, and the answer references the first question's content ("Atlas Review"/"Hello"). Survives restart per Ledger row 14 invariant. |
| AC3 | Seeded KB (papers.jsonl); any query mentioning "recoverable summarization" | Context is assembled for the turn | Context begins with `# Question` and contains all five `## <X> Memory` headings in rule-2 order; the KB segment contains text from the "Foldback" fixture record; each segment includes its what-it-is / how-to-use guidance lines. |
| AC4 | Default toolset registered + the 4 fixture tools (≥9 named tools in store) | Tools are retrieved for query "fetch the full text of a paper and store it" | The tools list passed to the LLM has ≤5 entries, all unique names, each a valid OpenAI function schema, and includes `fetch_and_save_paper_to_kb_db`. |
| AC5 | Same toolbox | Retrieve for "what time is it right now" | ≤5 tools returned; `get_current_time` is among them. |
| AC6 | Thread `t-long` seeded from fixture; token limit overridden to a value making the memory context exceed 80% | A turn runs on `t-long` | Offload triggers before reasoning: a SummaryRecord exists (8-char id, 4-heading summary); the post-offload context's `## Conversation Memory` is the pointer stub (no original fixture messages); `## Summary Memory` contains `[Summary ID: <id>]` + description; `# Question` still contains the verbatim query; recomputed usage < pre-offload usage. |
| AC7 | AC6's summary id | `expand_summary(<id>)` | Returns the summary text AND all 12 original fixture messages in chronological order with timestamps, including verbatim *"Which paper introduced the Orchid memory layer?"*. |
| AC8 | AC6 has run | Inspect conversational store for `t-long` | 0 rows with `summary_id` null; 12 rows carrying the AC6 summary id. |
| AC9 | AC8 state | `summarize_and_store(thread_id="t-long")` again | Returns the no-unsummarized-messages message; no new SummaryRecord is created; no row's `summary_id` changes. |
| AC10 | `EmptyLLM` stub as the LLM client | Summarize the fixture thread's transcript | Result summary is non-empty, contains all four `###` headings, with the source excerpt under Technical Information; description label is non-empty and not in {"Conversation summary","Summary","Chat summary","Thread summary"}. |
| AC11 | A registered fixture tool that reads `long_payload.txt` (returns ≥5,000 chars) | The agent loop executes that tool | Tool-log row stores the FULL result (≥5,000 chars) + preview ≤2,000 bytes; the tool-role message given to the LLM is ≤3,000 chars + a truncation notice naming the tool-log id. |
| AC12 | A registered tool that raises `ValueError("boom")` | The agent loop calls it | No crash; tool-log row has `status="failed"`, `error_message` containing "boom"; the step is recorded as failed; the loop continues to a final answer. |
| AC13 | `ToolLoopLLM` stub | `call_agent(...)` with max_iterations=10 | Loop stops after exactly 10 iterations; answer == "I was unable to complete the request within the allowed iterations."; 10 tool-log rows exist for the thread. |
| AC14 | A live turn that used ≥1 tool | Turn completes | Exactly one workflow record written: text contains the query, `Step 1:`-numbered steps, answer clipped ≤200 chars; metadata `num_steps` ≥1; `read_workflow` on a similar query returns it; a workflow record with 0 steps (written directly in the test) is NOT returned by `read_workflow`. |
| AC15 | `get_current_time` already registered | Register `get_current_time` again | Toolbox store row count for that name stays 1; the callable remains invocable; retrieval returns it once. |
| AC16 | Empty KB; network available *(marked `live`, excluded from the default test run)* | `arxiv_search_candidates("agent memory", k=5)` then `fetch_and_save_paper_to_kb_db(<first id>)` | Candidates parse as JSON with the six documented fields, ≤5 entries, abstracts ≤2,500 chars, and no KB writes; the fetch writes ≥1 chunk rows each with all 9 metadata fields, `num_chunks` consistent, and returns the saved-confirmation string. |
| AC17 | — | Inspect the system prompt string | It names all five memory segments with their semantics, the expand-before-relying summary policy, the conflict-priority order of rule 2, the minimum-necessary-tool-calls rule, and the summarize-with-thread_id instruction. |

Every business rule reaches ≥1 AC (R1→AC1/2, R2→AC3/17, R3→AC4/5, R4→AC6, R5→AC7/8,
R6→AC9, R7→AC10, R8→AC11/12, R9→AC13, R10→AC14, R11→AC15, R12→AC16, R13→AC3/17); every AC
traces to a rule.

## 6. Boundaries

**Always**
- Read the five deterministic memory segments before reasoning, and persist conversation,
  workflow, entities, and tool logs after — every turn, unconditionally (R1, R10).
- Mark source rows with `summary_id` in the same operation that stores their summary (R5).
- Log every tool call, including failures, at full fidelity (R8).
- Load secrets from the environment (`.env`); keep all stores under `./data/`.

**Ask First**
- Changing the embedding model or the distance strategy after any data is ingested — the
  course itself warns stale mixed-strategy data breaks lessons (its notebooks drop all
  tables to guarantee "consistent distance strategy"); either change forces re-embedding /
  re-indexing everything (Ledger rows 16, 18).
- Raising toolbox k or bypassing retrieval to pass more tools — re-opens the Lesson-4
  failure mode (context confusion, selection degradation, latency/cost); course-cited
  guidance is ~10–20 tools max exposed (Ledger row 17).
- Moving an operation across the deterministic/agent-triggered line (Ledger row 2) — the
  course argues each side's costs aloud (Lesson 3): determinism buys reliability, agent
  triggering buys signal-to-noise; swapping silently changes behavior guarantees.
- Replacing recoverable compaction with plain summarization — Lesson 5: summarization "will
  always be a lossy technique"; dropping the write-back link makes detail unrecoverable
  (Ledger row 3).
- Swapping the store realization (Ledger row 7) or adding keyed services (Tavily, row 8).
- Changing the summarization prompt's four-heading structure — the structure IS the
  consolidation contract (Lesson 5: prompt choice determines summary quality).

**Never**
- Never invent citations, paper metadata, or provenance; when KB evidence is missing, say
  what is missing (and optionally use a tool) instead of asserting (R13).
- Never summarize or discard the current `# Question` (R2, R4).
- Never pass the full toolbox to the LLM (R3).
- Never mutate fixtures to make a test pass (§5).
- Never hardcode or commit secrets — no API keys or DB passwords in source (§2).
- Never let entity-extraction or logging failures abort a turn (R10).

## 7. Test Plan & Self-Verification

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # this build's own pinned requirements
python scripts/seed_fixtures.py          # seeds fixtures/papers.jsonl into the KB
pytest tests/ -m "not live" -v           # AC1–AC15, AC17 — offline, deterministic (stub LLMs where specified)
pytest tests/ -m live -v                 # AC16 + any end-to-end live-LLM checks (needs OPENAI_API_KEY + network)
```

Tests for AC6/AC10/AC13 use the fixture stub clients and the overridable token limit —
they MUST NOT depend on live model output. AC2 MUST actually restart the process (separate
`subprocess` invocation or two test phases against the same `./data/`), not just re-call a
function.

**Reporting requirement:** the building agent MUST report results **per acceptance
criterion** (AC1–AC17) with cited evidence — the pytest output lines, and file paths /
store row counts where relevant. "Should pass" or "looks correct" is treated as a failure:
it means the check was not run.

## Final deliverable note (for the build session)

After the build is verified, conclude the session by presenting an infra/structure diagram
of the built app (components: agent loop, MemoryManager, the seven stores, toolbox
retrieval, LLM, tools) and end with the exact phrase:

**"This is the infra/structure diagram of this app"**

---

## Course Context Pack (embedded — agent-readable)

Concepts only — no course code. Durable knowledge for applying this course's pattern;
CTX-D lists the only perishable parts.

### CTX-A. The pattern

The course's central buildable pattern is the **memory-aware agent loop** over a
seven-type memory core:

```
perceive query
  → assemble partitioned context   (deterministic reads: conversational, knowledge base,
                                     workflow, entity, summary-context — each a self-
                                     describing markdown segment; question prepended last)
  → budget the context             (estimate tokens; ≥80% ⇒ recoverable compaction of the
                                     conversation segment into summary memory)
  → select tools semantically      (top-k similarity over the toolbox store — never all tools)
  → reason/act loop                (LLM proposes tool calls; harness executes, logs full
                                     payloads out-of-band, returns bounded excerpts; ≤10 turns)
  → persist learning               (deterministic writes: conversation turn, workflow steps,
                                     extracted entities)
  → repeat next turn / next session
```

Why each stage exists: deterministic preloads solve the chicken-and-egg problem ("you need
memory to know which memory you need" — Lesson 3); budgeting prevents context overflow
while compaction keeps detail recoverable (Lesson 5); semantic tool retrieval prevents
tool-overload degradation (Lesson 4); audit logging keeps big payloads out of the prompt
but available just-in-time (Lesson 6); persistence turns each interaction into reusable
experience — the difference between a memory-*augmented* and a memory-*aware* agent
(Lessons 2–3): the aware agent is *told* about its memories (system prompt + partitioned
segments) and *operates* on them via tools.

The surrounding vocabulary the course builds on: the **agent memory core** is the database
(where most data traffic flows); the **memory manager** is the abstraction exposing typed
read/write operations over it; a **memory unit** is the smallest atomic record (e.g. one
timestamped message; one workflow with steps+outcome); the **memory lifecycle** is
ingest → enrich (embed/augment) → store → organize (index) → retrieve (lexical / vector /
graph / hybrid) → LLM → write back; **context engineering** is curating high
signal-per-token context; **memory engineering** is the umbrella discipline (database +
agent + ML engineering + information retrieval).

Memory-type map (Lesson 3): Conversational = episodic (time-ordered, exact-key by thread);
Knowledge Base = semantic; Workflow + Toolbox = procedural; Entity = semantic/episodic
entity context; Summary = compressed episodic; Tool Log = execution audit trail.

### CTX-B. Failure-mode catalog

- **CTX-B1 — Stateless reset.** *Symptom:* agent asks "please specify" about something the
  user said two turns ago (Lesson 2's restaurant-booking demo). *Cause:* no persisted
  interaction history loaded into context. *Fix:* deterministic conversational
  write-every-turn + read-at-loop-start, thread-scoped, time-ordered. *Enforced by* R1 → AC1, AC2.
- **CTX-B2 — Tool overload.** *Symptom:* wrong or degraded tool selection, bloated prompts,
  higher latency/cost as the tool count grows. *Cause:* all tool schemas stuffed into every
  prompt. *Fix:* toolbox-as-memory — embed tool descriptions, retrieve top-k per query
  (3–5 typical; providers recommend ≤10–20 exposed). *Enforced by* R3 → AC4, AC5.
- **CTX-B3 — Context overflow.** *Symptom:* long threads exhaust the window; the agent
  loses history or fails on token limits. *Cause:* unbounded accumulation of conversation
  in context. *Fix:* monitor estimated usage; at ≥80% deterministically offload the
  conversation segment to summary memory, leaving a stub + reference; never touch the
  question. *Enforced by* R4 → AC6.
- **CTX-B4 — Irrecoverable summarization loss.** *Symptom:* after compression, exact
  quotes/chronology are gone for good. *Cause:* summarization is inherently lossy
  (Lesson 5, spoken). *Fix:* recoverable compaction — store the full content with the
  summary, mark source rows with the summary id, expose `expand_summary(id)` for
  just-in-time recovery. *Enforced by* R5 → AC7, AC8.
- **CTX-B5 — Re-summarization.** *Symptom:* the same messages get folded into summary
  after summary; duplicate compressed memories. *Cause:* no marker distinguishing
  processed rows. *Fix:* `summary_id` marking; reads and summarization consider only
  unmarked rows; fully-processed threads report nothing-to-summarize. *Enforced by* R6 → AC9.
- **CTX-B6 — Empty summarizer output.** *Symptom:* downstream flow breaks on an empty
  summary or a useless generic label. *Cause:* model returns empty/degenerate content.
  *Fix:* retry with a simpler prompt, then a deterministic excerpt-based fallback; derive a
  specific fallback label. *Enforced by* R7 → AC10.
- **CTX-B7 — Tool-output context bloat.** *Symptom:* one big tool payload (a full paper)
  swamps the window. *Cause:* raw tool results echoed into the prompt. *Fix:* persist the
  full payload to the tool log; hand the model a bounded excerpt plus a pointer id
  (context offloading). *Enforced by* R8 → AC11, AC12.
- **CTX-B8 — Runaway loop.** *Symptom:* the agent keeps calling tools and never answers.
  *Cause:* no stop condition beyond "model decides". *Fix:* max-iteration cap with a
  templated inability answer; tool exceptions become failed steps, not crashes.
  *Enforced by* R9 → AC13.

### CTX-C. Decision background

Reference only — decisions live in the Decision Ledger; this is the mechanism and
provenance behind its rows.

- **CTX-C1 (→ Ledger 1).** Storage-by-retrieval-need: conversational and tool-log memory
  are retrieved by exact key (thread id) and time order — similarity search is the wrong
  primitive, so they live in relational tables; the other five types are retrieved by
  meaning, so they live in vector stores. Lesson 3 presents the per-type table
  (memory type → human analogy → storage → retrieval strategy) as the design method.
- **CTX-C2 (→ Ledger 2).** The deterministic side buys: context bootstrapping
  (non-negotiable), no forgotten saves, predictability/debuggability, reduced model
  bookkeeping. The agent-triggered side buys: relevance filtering (not everything deserves
  storage), cost/latency control, judgment about *what* to store or expand. Tool calls are
  typically agent-triggered because only the agent can judge whether external information
  is needed. The Lesson 3 classification table vs the Lesson 6 loop disagree on
  `read_summary_context` and `write_entity` (table: agent-triggered; loop: deterministic) —
  the Ledger default follows the loop.
- **CTX-C3 (→ Ledger 3).** Two reduction techniques taught: **context summarization**
  (compress via LLM, re-seed a clean window — always lossy) and **context compaction**
  (move content to the database under an id + description, let the model pull it back —
  recoverable). The course's implementation composes them: summarize, store with links,
  expand on demand. The summary's four-heading structure (technical / emotional /
  entities / action items) is the consolidation contract — "structured extraction, not just
  compression" (Lesson 5 takeaway).
- **CTX-C4 (→ Ledger 4).** The toolbox pattern: embed `name + description + signature`
  (augmented text when available), store per-tool metadata, retrieve by query similarity,
  convert hits to provider function schemas at the call boundary. Exposing `read_toolbox`
  *itself* as a registered tool lets the agent discover capabilities mid-execution
  (programmatic and agent-callable at once).
- **CTX-C5 (→ Ledger 6).** Markdown-partitioned context: `#`/`##` headings exploit the
  model's latent understanding of hierarchical documents; each segment tells the model what
  the memory is and how to use it, which is what upgrades "augmented" to "aware". The
  conflict-priority rule (Question > latest Conversation > KB > older summaries/workflows)
  is part of the same design.
- **CTX-C6 (→ Ledger 16, 18).** Provenance of the contradictions: distance strategy —
  COSINE in the Lesson 3/4 notebooks and Lesson 3 narration, EUCLIDEAN in the Lesson 5/6
  notebooks (the running app); index — HNSW narrated in Lesson 3's objectives/markdown,
  IVF (`NEIGHBOR PARTITIONS`, target accuracy 95) in the helper code, with an explicit
  comment that HNSW hit ORA-00600/51928/51962 on Oracle Free. The notebooks' "drop all
  tables for a consistent distance strategy" banner is the course's own acknowledgment
  that mixing strategies across sessions corrupts comparability.
- **CTX-C7 (body defaults, exact sources).** Retrieval k's: knowledge base 3, workflow 3,
  entity 5, summary-context 10, toolbox 3 (manager default) / 5 (agent loop);
  conversational read limit 10 (agent loop) — the Lesson 5 notebook's verification cell
  used `limit=100`, an exploratory config, not the app default. Token estimate: chars//4
  (narration: some models are nearer chars//2 — it is an estimate, not tokenizer truth).
  Chunking 1500/200. Tool-result LLM bound 3,000 chars; preview 2,000 bytes. Entity
  extraction input clip 500 chars; summary input clip 6,000 chars. Max iterations 10.
  Workflow answer clip 200 chars. Summary id = uuid4[:8].
- **CTX-C8 (→ Ledger 8).** The search-and-store pattern (Lesson 4, spoken): a search tool
  that persists results means information discovered once becomes long-term memory —
  "the agent learns from its searches" — and large payload handling moves out of model
  context into memory infrastructure.

### CTX-D. Perishable assumptions

Treat every name below as a **search keyword against current docs, not a guaranteed
import**. The concepts in CTX-A…CTX-C are durable; only these names age. The course's own
installs were entirely unpinned.

- Models: `gpt-5`, `gpt-5-mini` (both appear; token table 256,000; 128,000 fallback),
  `sentence-transformers/paraphrase-mpnet-base-v2` (768-dim).
- OpenAI SDK: `OpenAI()` client, `chat.completions.create`, `tools`/`tool_choice="auto"`,
  `max_completion_tokens`, tool-role messages keyed by `tool_call_id`.
- LangChain-era names: `langchain_oracledb.vectorstores.OracleVS`,
  `langchain_oracledb.retrievers.hybrid_search.OracleVectorizerPreference`,
  `langchain_community.vectorstores.utils.DistanceStrategy`
  (COSINE / EUCLIDEAN_DISTANCE / DOT_PRODUCT), `HuggingFaceEmbeddings` imported from BOTH
  `langchain_huggingface` and `langchain_community.embeddings` in different lessons,
  `langchain_community.retrievers.ArxivRetriever`,
  `langchain_community.document_loaders.ArxivLoader`,
  `langchain_text_splitters.RecursiveCharacterTextSplitter`.
- Services/data: `tavily.TavilyClient`, HuggingFace `datasets.load_dataset`
  (`nick007x/arxiv-papers`, streaming).
- Oracle-era specifics: Oracle AI Database **26ai** (Docker "FREE" image), DSN
  `127.0.0.1:1521/FREEPDB1`, `VECTOR` user bootstrap, ASSM tablespace requirement for JSON
  columns (ORA-43853), `CREATE VECTOR INDEX … ORGANIZATION NEIGHBOR PARTITIONS … WITH
  TARGET ACCURACY 95` (IVF), HNSW, error lore: ORA-00600, ORA-51928, ORA-51962, ORA-00955,
  ORA-00942.

### CTX-E. Provenance map

Lesson numbering below is the **transcripts'** (authoritative). The notebook files are
shifted: `L2.ipynb` ↔ Lesson 3, `L3.ipynb` ↔ Lesson 4, `L4.ipynb` ↔ Lesson 5,
`L5.ipynb` ↔ Lesson 6 — and several notebook H1 titles carry the *previous* notebook's
name (e.g. `L3.ipynb`'s H1 says "Scaling Agent Tool Use" — correct — but `L2.ipynb`'s H1
"Constructing the Memory Manager" pairs with the dump section mislabeled "Lesson 4"). Even
the narration's sign-offs are off by one ("completed lesson 4" ends Lesson 5; "end of
lesson 5" ends Lesson 6). Nothing in this spec requires platform access.

- **Lesson 1 — Introduction:** course framing; memory engineering as first-class,
  persistent, structured infrastructure external to the model (CTX-A vocabulary).
- **Lesson 2 — Why AI Agents Need Memory:** stateless-agent failure demo (CTX-B1);
  conversational memory attributes (timestamp/role/content, time-ordered); why
  conversational history alone is insufficient; short-term vs long-term memory taxonomy
  (semantic cache, working memory / procedural, semantic, episodic); RAG→agent-memory
  bridge; agent memory core definition (CTX-A).
- **Lesson 3 — Constructing The Memory Manager (`L2.ipynb`):** agent stack / memory layer;
  memory manager, memory units, context engineering, memory lifecycle, memory-engineering
  disciplines; augmented→aware progression (CTX-A, CTX-C5); the 7-type storage/retrieval
  table and SQL-vs-vector argument (CTX-C1); deterministic vs agent-triggered
  classification + rationale (CTX-C2); table schemas + indexes; StoreManager with COSINE;
  IVF-vs-HNSW discrepancy (CTX-C6); HF dataset ingestion + `read_knowledge_base`
  demonstration (Ledger 9).
- **Lesson 4 — Scaling Agent Tool Use with Semantic Tool Memory (`L3.ipynb`):** tool-calling
  mechanics; tool-overload failure modes and 10–20 guidance (CTX-B2); toolbox pattern +
  memory-unit augmentation and its separability/recall argument (CTX-C4, Ledger 5);
  `read_toolbox` self-registration; Tavily search-and-store (CTX-C8); `get_current_time`;
  arXiv discovery + deep-ingestion (chunk 1500/200) tools; original-vs-augmented docstring
  comparison; retrieval validation (`k=1` demo).
- **Lesson 5 — Memory Operations: Extraction, Consolidation, and Self-Updating Memory
  (`L4.ipynb`):** context engineering; summarization-vs-compaction argument, "always lossy"
  (CTX-B4, CTX-C3); token estimation chars//4 and thresholds (CTX-C7); four-heading
  summarization prompt + retry/fallback (CTX-B6); `expand_summary`; thread summarization
  with `summary_id` marking + DB-level verification (CTX-B5); offload policy; ok/warning/
  critical monitor; EUCLIDEAN switch (CTX-C6).
- **Lesson 6 — Memory Aware Agent (`L5.ipynb`):** agent loop (start/stop conditions,
  pseudo-code); agent harness; in-loop vs out-of-loop memory operations (CTX-C2); the
  memory-aware system prompt with partitioned segments and conflict priority (CTX-C5);
  80% deterministic offload; toolbox k=5; tool-log persistence + 3,000-char bound
  (CTX-B7); max-iterations stop (CTX-B8); post-turn workflow/entity/conversation writes;
  the MemGPT walk-through demonstrating continuity, summarize-via-tool, and
  expand-to-answer "what was my first question?" (CTX-B1, basis of AC2/AC7).
- **Lesson 7 — Conclusion:** pattern recap — memory modeling, semantic retrieval,
  extraction, consolidation, write-back as the transferable building blocks.

---

*Status: v1 · Course: Agent Memory: Building Memory-Aware Agents (DeepLearning.AI ×
Oracle) · Learner project: [project] (default: memory-aware research-assistant CLI on the
fixture corpus) · Living document: when the building agent produces something unexpected,
add the missing constraint here and re-run the build.*
