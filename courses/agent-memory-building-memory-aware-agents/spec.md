# Spec: Memory-Aware Research Agent — Standalone Takeaway

> **This file is self-contained.** The embedded **Course Context Pack** (bottom of this file) replaces all external course references — nothing here requires access to the course platform, notebooks, or transcripts. `(CTX-X)` anchors mark course-derived knowledge. The **Decision Ledger** below holds every point where this build could diverge, each pinned to one course-derived default, so the spec builds as-is with zero intake.
>
> **Provenance:** generated from the *Agent Memory: Building Memory-Aware Agents* course notebooks (notebook dump incl. `helper.py` and `requirements.txt`) + lesson transcripts, on 2026-09-07. Generation guide version: repo commit `a7de8ef`.

---

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
2. **First question — build as-is, or customize?** Ask exactly one question with two options:
   build the course-default takeaway **as-is** (every Ledger row resolves to its Default), or
   **customize** the decisions row by row. If the user chooses as-is, skip step 3 — go straight
   to the step-5 checklist and build. If the user chooses customize, continue with step 3.
3. **Present the Ledger ONE ROW AT A TIME — one question per row.** For each row ask a single
   question: the **Decision** as the prompt, its **Options** as the choices. Append
   "(course default)" to the option the course actually used — on a substitution row that is
   the course-faithful Options entry, not the Ledger Default. You may also mark an option
   "(Recommended)" per your own judgment or your question tool's convention; when your
   recommended option IS the course's actual choice, merge the labels into
   "(Recommended - course default)". A recommendation never removes or moves the
   "(course default)" label. Use the answers already given (project, data, goal, …) to frame
   later questions and describe options in the person's own terms — but never skip a row, drop
   or alter an Option, or move the "(course default)" label because of an earlier answer. Put
   any realizations beyond the tool's option slots (or the free-form case) under the tool's
   "Other"/free-text. Ask about **every** row. A per-call item limit is NEVER a reason to drop,
   skip, merge, or silently default a row — make as many separate calls as there are rows.
4. **Presenting any of these questions ENDS YOUR TURN — stop here; write no code, create or edit
   no file, take no other build action.** Keep asking, one row at a time, until **every** row has
   an answer (a chosen option, an explicit "use the course default", or the step-2 as-is answer,
   which resolves every row at once). Answers to *some* rows do NOT release the build; "no reply
   yet" is not an answer — wait for the user.
5. **Before the first line of code, print a resolved-decision checklist** — every Ledger row
   with its final value (the user's choice, or its Ledger default). Begin implementation ONLY
   after this complete checklist is shown; if any row is unresolved you are not done — return to
   step 3. Build on the checklist's values.

---

## Decision Ledger (§0 above requires the build agent to present these before building)

These are the points where this build could diverge. Every row has a course-derived default, so
the spec is buildable and evaluatable as-is; change a row only when applying to a real project or
when you have reason to prefer another option.

| # | Category | Decision | Invariant (must hold) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| D1 | learner | **Project** `[project]` — the Default is the course's *example realization* (a research-assistant scenario), expected to be swapped when the learner's own project differs; the invariants, not the example, must survive | — | A memory-aware **research-assistant chat agent** (terminal chat over per-thread sessions), re-expressing the course's example scenario shape ("an agentic research assistant that helps users investigate complex topics over multiple sessions", CTX-E L3) on the §5 synthetic fixture corpus. §3-precedence **branch 1**: the materials clearly afford a concrete example shape; all fixture facts are authored here — no course data is copied | Course-example shape (default); the learner's own project (free text at the gate) | Swapping the project means re-seeding the KB fixtures, retitling, and re-reading D2/D3; the pattern and every invariant are unchanged | learner |
| D2 | learner | **Data / inputs** `[data]` — Default is the course-shaped *example* seed, expected to be swapped for the learner's real corpus | — | The §5 **synthetic fixture corpus** (3 authored knowledge-base documents, 1 seeded 30-message conversation, fixture tools). Course provenance (what the course did, not advice): it streamed 100 records of public arXiv paper metadata plus on-demand fetched arXiv papers (CTX-C10, CTX-E L3/L4) | Fixture corpus (default); live arXiv ingestion (course demo path — keyless public API, network; ACs touching it are `live`); the learner's own documents | Real data adds network/latency and does not run the offline oracle; fixtures keep every AC runnable on day one. Changing embedded data after ingest → re-ingest (see Ask First AF2) | learner |
| D3 | learner | **Goal** `[goal]` — what "working" means | — | **Cross-session continuity**: after the §5 scripted demo sequence, the agent answers a question about earlier turns (including turns already summarized away) using only persisted memory — the course's own closing demo shape ("what was my first question?", CTX-E L6) | Default continuity goal; a learner-defined retrieval/continuity goal (free text) | A different goal re-weights which memory types matter; ACs 1–25 pin the default goal only | learner |
| D4 | learner | **Model / provider** `[model]` | The model MUST be reachable through an OpenAI-style chat-completions interface and MUST support **native tool/function calling** | **OpenAI hosted API**: `gpt-5-mini` for the agent loop + `gpt-5` for background memory operations (summarization, tool-docstring augmentation, entity extraction) — the end-to-end app's configuration (loop default in the L5 app notebook; helper defaults for memory ops). The materials are split on naming: the L4 notebook's local token-limit map keys `gpt-5-mini` while `helper.py`'s keys `gpt-5` (same 256 000 value both sides) — both sources cited in CTX-C6. Keyed API ⇒ ACs needing it are marked `live` | OpenAI gpt-5 family **(course default)**; any OpenAI-compatible endpoint (hosted or locally served) meeting the invariant | Weaker models degrade summary fidelity, entity extraction, and tool selection; a different model changes the token-limit body default (§4 R4) | learner |
| D5 | learner | **Environment** `[environment]` | **All memory must survive process restarts** — the course's core promise ("persists across sessions", CTX-E L6/L7) | Local single-machine run, Python ≥ 3.11 (this build's pin — *project hardening*: the materials state no Python version and install unpinned, see §2) | Local machine (default); container; always-on server | Environments without a durable filesystem break the invariant and force a hosted store (see D11 Options) | learner |
| D6 | learner | **Scope boundary** `[scope-boundary]` — *gate instruction:* when asking this row, present the §1 "Not Included" list **verbatim inside the question** (§1 is not a Ledger row; this row is the only way the learner ever sees the exclusion list before being asked to amend it) | — | **Keep as-is**: every §1 exclusion stands; the full acceptance set is built | (a) Keep the boundary as-is (default); (b) bring an excluded item back — free text names which; each §1 item carries a handling rule that determines the answer. A genuinely new exclusion also arrives via free text and MUST name the ACs it retires | Restoring a "named-but-never-built" item adds work the spec supplies no parameters or ACs for; restoring a row-owned item re-opens that row | learner |
| D7 | design-argued | **Memory-core topology** | An external persistent store exists and a **single manager abstraction** mediates every memory read/write (the agent code never touches storage directly) | The full **seven-type segmented topology**: conversational, knowledge-base, workflow, toolbox, entity, summary, tool-log — one store each, unified behind the memory manager (CTX-A) | Seven-type topology (default — the course's argued position); **conversational-memory-only** (the course's Lesson-2 baseline, demonstrated working for chat continuity and then deliberately built beyond — a legitimate reduced-scope choice); any subset in between | Lesson 2 argues the trade-off aloud: conversational-only gives continuity but "conversation windows are finite, user relationships are not", "not all valuable information is in a single conversation", and "agents need structured, queryable knowledge, not just chat logs" (CTX-E L2). Dropping a type removes its context segment, its persistence rules, and its ACs | course+learner |
| D8 | design-structural | **Deterministic vs agent-triggered operation split** — who triggers each memory operation: the harness (code) or the model (tool call) | Context-assembly reads and the persistence writes continuity depends on run **deterministically every turn**, never at model discretion; judgment-requiring operations are exposed to the model **as tools** | The end-to-end app's split (§4 R3/R11–R13, R14): deterministic each turn — read conversational/KB/workflow/entity/summary-context at loop start, write user + assistant conversational rows, write workflow after tool-using runs, write a tool log after every call, extract entities from query and answer (non-fatally), and offload at the >80 % threshold; agent-triggered tools — `read_toolbox`, `arxiv_search_candidates`, `fetch_and_save_paper_to_kb_db`, `get_current_time`, `expand_summary`, `summarize_and_store`. Contradiction note (lower-precedence evidence, both sides cited in CTX-C4): the Lesson-3 classification table marks `read_summary_context` and `write_entity` agent-triggered-only, while the Lesson-6 app runs both deterministically — the app's behavior is the default. Summarization is deliberately **both** deterministic (threshold) and agent-callable — narrated in Lesson 6 | The app split (default); moving individual operations between the two categories (e.g. agent-discretionary entity writes, per the Lesson-3 table) | Deterministic ops buy predictability, continuity, and "no forgotten saves" at token/latency cost; agent-triggered ops buy relevance and cost control but risk missed saves and the chicken-and-egg problem ("you need memory to know which memory you need") — argued in Lessons 3 and 6 (CTX-C4) | course+learner |
| D9 | design-argued | **Context-window reduction strategy** | Context usage is monitored every turn and reduced before overflow; the current question is **never** summarized away | **Recoverable compaction** (the course's built mechanism): summarize the thread's unsummarized rows, persist the summary (id + description + summary + full source text, thread-scoped), mark the exact source rows with the `summary_id`, replace only the conversation segment with a stub + `[Summary ID: …]` reference, and expose `expand_summary` for on-demand recovery (§4 R7) | Recoverable compaction (default); **pure lossy summarization** (summary replaces context, no back-link — presented by the course as a legitimate technique with an explicit warning that it "will always lose a little bit of information", Lesson 5); pure compaction (offload raw content under an ID + description, no summary) | Lesson 5 argues it aloud: summarization is inherently lossy; compaction preserves recoverability at the cost of storage and an extra retrieval hop (CTX-C3). Choosing lossy-only retires ACs 11–12's recovery assertions | course+learner |
| D10 | design-argued | **Tool-description augmentation at registration** | Tool retrieval is **semantic**: keyed on the stored description text embedded at registration, not on exact tool names | **LLM augmentation ON by default** at registration (original docstring + function source → enriched description + 5 synthetic trigger queries, all folded into the embedding text), overridable per tool. The course registered a mix (most tools augmented; `arxiv_search_candidates` deliberately raw). Contradiction note (CTX-C7): `get_current_time` is registered `augment=True` in the Lesson-4 notebook cell but `augment=False` in the helper's common-tools registration used by the Lesson-6 app | Augmented (default — the course's argued position); raw docstrings (course-demonstrated working: the unaugmented arXiv tool was still retrieved first in the Lesson-4 validation query) | Lesson 4 argues it aloud: augmentation buys higher separability and recall in the embedding space at the cost of LLM calls per registration (CTX-C5) | course+learner |
| D11 | realization | **Persistent memory store** — heavy-dependency substitution row | One durable store layer provides **both** (a) exact-key, time-ordered relational access (conversation rows by `thread_id`; tool logs) **and** (b) semantic-similarity retrieval with metadata filtering over embedded text for the five vector memory types. (Durability across restarts: owned by D5) | **SQLite via Python's stdlib `sqlite3`** — one database file, seven tables carrying the §4 canonical store names; embedding vectors stored per row; similarity computed **exactly, in process (brute-force cosine)** at the declared fixture scale. §3 dependency precedence **branch 1** (substitution): the course teaches a memory *pattern* that Oracle realizes; Oracle is not the taught subject — the course's own close is "take these patterns, adapt them to your own use case" (CTX-E L7). "Lightest" decided by tier: **tier 1** (ships with the standard distribution) satisfies the invariant at the declared default scale, because exact brute-force similarity meets the retrieval contract on fixture-sized data; no indexing tier is required at that scale — scaling realizations live in Options | Oracle AI Database 26ai + LangChain `OracleVS` + IVF vector index **(course default)**; SQLite stdlib (Default); an embedded vector library (tier 2) once the corpus outgrows brute force; a locally served / hosted vector DB (tier 3) | Switching stores forces re-ingestion and re-implementation of the metadata filters; Oracle adds container + admin setup (Docker, admin credentials) but brings IVF/HNSW indexing and hybrid search at scale — the course's Lesson-3 rationale for indexing (CTX-C1, CTX-C2) | course+learner |
| D12 | realization | **Web-search tool** (course realization: Tavily) — keyed-tool row | If a web-search tool is enabled it MUST be toolbox-registered and follow the **search-and-store** pattern: results persisted to knowledge-base memory with title/url/score/query/timestamp metadata, never returned only ephemerally (§4 R17) | **Omitted.** §3 keyed-tool rule: Tavily needs an API key (heavy), and it is *not* the only carrier of the taught search-and-store behavior — the keyless arXiv tool `fetch_and_save_paper_to_kb_db` also persists fetched external content to the knowledge base — so the deterministic default is omission, with the keyless course tools carrying the behavior | Tavily via `TAVILY_API_KEY` **(course default)**; an honestly-labeled local stand-in (a fake `search_web_local` tool serving canned fixture results, whose registered description MUST say it is a fake standing in for a real web-search service); omit (Default) | Omission removes open-web reach (the agent is limited to arXiv + its own memory); the stand-in keeps the pattern exercisable offline but only answers from fixtures; Tavily restores the course demo exactly at the cost of a key | course+learner |

**Contradicted group: empty.** Every mined course contradiction failed the §5.5 stakes test
(each is a near-equivalent lever whose up-front choice changes no structure, semantics, or
guarantee). Each is resolved as a **body default** carrying its in-place contradiction note,
its lever-value branch citation, and a *post-build lever* label — see §4 R4/R16 notes and the
"Post-build levers" list at the end of §4, with background in CTX-C6–C9.

---

## 1. Objective

Build a persistent, memory-aware research-assistant agent that reads from and writes to seven
typed memory stores on every turn, manages its own context-window budget by recoverable
summarization, selects tools by semantic retrieval instead of context-stuffing, and therefore
answers follow-up questions across sessions from memory rather than from scratch (pattern:
CTX-A).

### Not Included ★

Each item carries its §5.5 handling rule in brackets, so the D6 gate answer is determinate.

1. **Web search (Tavily or other)** — [owned by Ledger row D12 — defer to that row; never decide twice].
2. **Hybrid (lexical + vector) search** — named by the course (a knowledge-base vectorizer preference is defined but never invoked) and never built [buildable, but this spec supplies no parameters and no acceptance criteria for it].
3. **Reranking of retrieval results** — named in the course's RAG overview, never built [buildable; no parameters or ACs supplied].
4. **Semantic cache** (short-term memory form) — named in Lesson 2, never built [buildable; no parameters or ACs supplied].
5. **Memory decay / merge / strengthen / forget operations** — named as judgment questions ("should I strengthen, update, merge, or decay this memory?"), never built [buildable; no parameters or ACs supplied].
6. **Vector indexing at scale (IVF/HNSW) and Oracle-specific features** — [owned by Ledger row D11's Options — defer to that row].
7. **Bulk course-demo data ingestion** (streamed arXiv-metadata dataset) — [owned by Ledger row D2 — defer to that row].
8. **Fine-tuning embedding models / continual-learning pipelines** — named as memory-engineering disciplines, never built [buildable; no parameters or ACs supplied].
9. **Multi-user auth, concurrency, or a web/GUI frontend** — past course scope (*project hardening* exclusion) [additive and owned by no other row — restorable at the gate; note the spec supplies no ACs for it].
10. **Integration into an existing codebase** — [outside the delivered build mode (standalone takeaway) — unavailable].

The agent must not add features beyond this boundary on its own initiative.

---

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python ≥ 3.11 | This build's pin (*project hardening* — see honesty note below). Environment: Ledger D5 |
| Persistent store | SQLite (stdlib `sqlite3`) | Ledger row **D11** — learners change it there, not here |
| LLM | OpenAI API: `gpt-5-mini` (agent loop), `gpt-5` (memory ops) | Ledger row **D4**. Key via `OPENAI_API_KEY`; ACs needing it are `live` |
| Embeddings | `sentence-transformers` model `paraphrase-mpnet-base-v2` (768-dim) | Course-demonstrated in all lessons; keyless, runs locally (one-time model download). Post-build lever — changing it after ingest forces re-embedding (AF2) |
| arXiv access | Keyless public arXiv API (metadata + PDF text extraction) | Keyless public API stays the default per the mere-network rule; ACs touching it are `live` |
| Text chunking | Recursive character splitting, chunk_size 1500 / overlap 200 | Course-demonstrated values (deep-ingestion tool). Implementation library is the agent's choice |
| Testing | `pytest` | *Project hardening* — the course ran verification cells, not a test framework |
| Secrets | Environment variables (`.env` supported), never hardcoded, never committed | The course's lab DB credentials that appear in the materials are course-lab artifacts, not values to reuse (CTX-D) |

**Install/pin honesty (the one required note):** the course's `requirements.txt` installs
**everything unpinned** — no version pins exist anywhere in the materials, and the Python
version placeholder is unfilled. Do not invent pins "from the course". Pin current stable
versions as *this build's* choice at build time, and treat every era-specific name
(`langchain-oracledb`, `OracleVS`, `HuggingFaceEmbeddings` import path, `gpt-5` family) as a
perishable search keyword per **CTX-D**, not a guaranteed import.

---

## 3. Input/Output Contracts ★

The core objects, as JSON Schema. Storage may add columns; these fields and constraints are
binding. The seven store names, the entity `type` enum, the four summary headings, the
`[Summary ID: …]` reference format, and the context-segment headings are **course-declared,
contract-participating constants** and are binding (CTX-E maps them to lessons).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "memory-aware-agent/contracts",
  "$defs": {
    "StoreName": {
      "enum": ["CONVERSATIONAL_MEMORY", "SEMANTIC_MEMORY", "WORKFLOW_MEMORY",
               "TOOLBOX_MEMORY", "ENTITY_MEMORY", "SUMMARY_MEMORY", "TOOL_LOG_MEMORY"]
    },
    "ConversationRow": {
      "type": "object",
      "required": ["id", "thread_id", "role", "content", "timestamp"],
      "properties": {
        "id": {"type": "string", "minLength": 1},
        "thread_id": {"type": "string", "minLength": 1},
        "role": {"enum": ["user", "assistant"]},
        "content": {"type": "string", "minLength": 1},
        "timestamp": {"type": "string", "format": "date-time"},
        "metadata": {"type": "object"},
        "summary_id": {"type": ["string", "null"], "pattern": "^[0-9a-f]{8}$"}
      }
    },
    "ToolLogRow": {
      "type": "object",
      "required": ["id", "thread_id", "tool_name", "result", "status", "timestamp"],
      "properties": {
        "id": {"type": "string"},
        "thread_id": {"type": "string"},
        "tool_call_id": {"type": ["string", "null"]},
        "tool_name": {"type": "string"},
        "tool_args": {"type": "string", "description": "JSON-serialized arguments"},
        "result": {"type": "string", "description": "FULL, untruncated tool output"},
        "result_preview": {"type": "string", "description": "<= 2000 UTF-8 bytes of result"},
        "status": {"enum": ["success", "failed"]},
        "error_message": {"type": ["string", "null"]},
        "metadata": {"type": "object", "properties": {"iteration": {"type": "integer", "minimum": 1}}},
        "timestamp": {"type": "string", "format": "date-time"}
      },
      "if": {"properties": {"status": {"const": "failed"}}},
      "then": {"required": ["error_message"]}
    },
    "SummaryRecord": {
      "type": "object",
      "required": ["id", "description", "summary", "full_content"],
      "properties": {
        "id": {"type": "string", "pattern": "^[0-9a-f]{8}$"},
        "description": {"type": "string", "minLength": 8,
          "not": {"enum": ["conversation summary", "summary", "chat summary", "thread summary"]},
          "$comment": "case-insensitive rejection of these generic labels is enforced by R6"},
        "summary": {"type": "string",
          "pattern": "### Technical Information[\\s\\S]*### Emotional Context[\\s\\S]*### Entities & References[\\s\\S]*### Action Items & Decisions"},
        "full_content": {"type": "string", "minLength": 1},
        "thread_id": {"type": ["string", "null"]}
      }
    },
    "EntityRecord": {
      "type": "object",
      "required": ["name", "type", "description"],
      "properties": {
        "name": {"type": "string", "minLength": 1},
        "type": {"enum": ["PERSON", "PLACE", "SYSTEM", "UNKNOWN"]},
        "description": {"type": "string"}
      }
    },
    "WorkflowRecord": {
      "type": "object",
      "required": ["query", "steps", "answer_excerpt", "num_steps", "success"],
      "properties": {
        "query": {"type": "string"},
        "steps": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        "answer_excerpt": {"type": "string", "maxLength": 200},
        "num_steps": {"type": "integer", "minimum": 1},
        "success": {"type": "boolean"},
        "timestamp": {"type": "string", "format": "date-time"}
      }
    },
    "ToolboxRecord": {
      "type": "object",
      "required": ["name", "description", "signature", "parameters", "augmented"],
      "properties": {
        "name": {"type": "string"},
        "description": {"type": "string", "minLength": 1},
        "signature": {"type": "string"},
        "parameters": {"type": "object"},
        "return_type": {"type": "string"},
        "augmented": {"type": "boolean"},
        "queries": {"type": "array", "items": {"type": "string"}}
      }
    },
    "ToolSchemaForLLM": {
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
              "properties": {"type": {"const": "object"}}
            }
          }
        }
      }
    },
    "ContextWindow": {
      "type": "string",
      "description": "The assembled per-turn LLM input. MUST start with the '# Question' section (never summarized away), followed by these segments in this order, each under its exact markdown heading: '## Conversation Memory', '## Knowledge Base Memory', '## Workflow Memory', '## Entity Memory', '## Summary Memory'. Summary references render exactly as '[Summary ID: <id>] <description>'.",
      "pattern": "^# Question\\n"
    },
    "AgentTurnResult": {
      "type": "object",
      "required": ["thread_id", "answer", "iterations", "steps", "tools_offered"],
      "properties": {
        "thread_id": {"type": "string"},
        "answer": {"type": "string", "minLength": 1},
        "iterations": {"type": "integer", "minimum": 1, "maximum": 10},
        "steps": {"type": "array", "items": {"type": "string"},
          "description": "one entry per executed tool call: '<tool>(<args-preview>) → success|failed'"},
        "tools_offered": {"type": "array", "maxItems": 5,
          "items": {"$ref": "#/$defs/ToolSchemaForLLM"},
          "description": "the focused toolset passed to the LLM this turn — never the full registry"},
        "summaries_created": {"type": "array", "items": {"type": "string", "pattern": "^[0-9a-f]{8}$"}}
      }
    }
  }
}
```

---

## 4. Business Rules

Provenance labels: **[C]** course-demonstrated (with CTX anchor), **[H]** project hardening.
Parameter values cite their exact source; where the materials contain more than one config,
the contradiction is stated in place.

1. **R1 — Seven stores, canonical names, idempotent init.** [C] (CTX-A, CTX-B1) On startup the
   system creates, if missing, exactly the seven stores named in the §3 `StoreName` enum
   (conversational + tool-log relational; knowledge-base, workflow, toolbox, entity, summary
   semantic). Initialization is create-if-missing (the helper's existence-check pattern);
   **no implicit wipe** — the notebooks' drop-all-tables cells are lesson-scoped resets, and an
   explicit `reset` command may reproduce them, but startup never destroys memory (destroying it
   breaks D5's invariant). → AC1, AC2
2. **R2 — Deterministic conversational persistence and reads.** [C] (CTX-B1) Every user query
   and every final assistant answer is written to conversational memory (thread_id, role,
   content, timestamp; `summary_id` initially null) on every turn, without model discretion
   (D8). Reads are thread-scoped, chronological (ascending timestamp), **exclude rows whose
   `summary_id` is set**, default limit 10 messages (source: MemoryManager
   `read_conversational_memory` default), rendered as `[HH:MM:SS] [role] content`, with an
   explicit "(No unsummarized messages found for this thread.)" placeholder when empty. → AC3, AC4
3. **R3 — Partitioned deterministic context assembly.** [C] (CTX-A, CTX-B1) At the start of
   every turn the harness deterministically builds the context window from memory:
   conversational (thread), knowledge base (query, k=3), workflow (query, k=3), entity (query,
   k=5), summary-context (query, k=10, thread-scoped when a thread is active) — each rendered
   under its exact §3 segment heading with a "what this memory is / how to leverage it"
   preamble; the current query is prepended as `# Question` **after** any offload and is never
   summarized. k sources: MemoryManager read-method defaults (`k=3`/`k=3`/`k=5`/`k=10`). The
   system prompt declares the segments, their semantics, and the conflict-priority order:
   current Question > latest Conversation Memory > Knowledge Base evidence > older
   summaries/workflows. → AC5
4. **R4 — Context budget monitoring and threshold offload.** [C] (CTX-B2) Token usage is
   estimated as `len(context) // 4` (≈4 chars/token) against a limit of **256 000** tokens for
   the configured loop model, falling back to 128 000 for unknown models. *Contradiction note:*
   the L4 notebook keys this limit under `gpt-5-mini` while `helper.py` keys it under `gpt-5`
   (both 256 000); resolved by lever-value **branch 2** (the end-to-end app's limit applies to
   whatever model the loop is configured with) — post-build lever (CTX-C6). Status bands:
   <50 % `ok`, <80 % `warning`, else `critical` (helper `monitor_context_window`). When usage
   exceeds **80 %** during context assembly, the harness deterministically offloads per D9
   before reasoning. Threshold and bands are post-build levers (AF5). → AC6, AC7
5. **R5 — Structured summarization output shape.** [C] (CTX-B6) Summaries are produced with
   **exactly four headings in this order**: `### Technical Information`, `### Emotional
   Context`, `### Entities & References`, `### Action Items & Decisions`; behavior constraints:
   keep concrete details (names, dates, APIs, errors, decisions), separate confirmed facts from
   open questions, never invent information, stay concise. Input to the summarizer is capped at
   6 000 characters; completion capped at 4 000 tokens (source: `summarise_context_window`).
   On empty model output, retry once with a simpler instruction (≤180 words, same headings);
   if still empty, emit the deterministic fallback that preserves all four headings with a
   ≤500-character source excerpt under Technical Information — the pipeline never breaks on a
   bad LLM response. → AC8 (offline, stubbed), AC9 (`live`)
6. **R6 — Specific summary labels.** [C] (CTX-B10) Each summary gets an 8–12-word label that
   names a concrete signal (entity, task, or issue). Labels in the reject set {"conversation
   summary", "summary", "chat summary", "thread summary"} (case-insensitive) or empty are
   replaced by the deterministic fallback label builder (first content line of ≥4 words,
   trimmed to 12 words; final fallback "Recent thread context, decisions, and open actions").
   Source: helper `summarise_context_window` + `_fallback_description`. → AC10 (offline, stubbed)
7. **R7 — Recoverable compaction (per D9's default).** [C] (CTX-B3) Summarizing a thread reads
   only rows with `summary_id IS NULL` (chronological), generates the R5 summary, persists a
   `SummaryRecord` (8-hex-char id, description, summary, **full source content**, thread_id),
   marks **exactly the source rows** with the new `summary_id`, and reports the count.
   The conversation segment is replaced by a stub telling the model to use
   `expand_summary(id)`, and the reference is rendered exactly as
   `[Summary ID: <id>] <description>` in the Summary Memory segment. `expand_summary(id)`
   returns the summary text plus **all** original messages in chronological order with
   timestamps. No source row is ever deleted by compaction. → AC11, AC12
8. **R8 — No re-summarization.** [C] (CTX-B9) Already-summarized rows are never re-processed:
   summarization selects only `summary_id IS NULL` rows; when none exist it returns a
   "nothing to summarize" result and writes nothing. → AC13
9. **R9 — Semantic tool retrieval; focused toolset; deduplicated registry.** [C] (CTX-B4,
   CTX-B8) Tools are registered into toolbox memory with metadata (name, description,
   signature, parameters, return type, augmented flag) and an embedding of their description
   text (per D10). Registration is **name-deduplicated**: a tool whose name already exists in
   the store is registered in-memory for execution but writes no duplicate row; retrieval also
   deduplicates by name. Per turn, the harness retrieves the top **k=5** semantically relevant
   tools for the query and passes **only those** to the LLM as OpenAI-style function schemas
   (§3 `ToolSchemaForLLM`) — never the full registry. *Contradiction note:* the registered
   `read_toolbox` tool's signature defaults `k=3` while its own docstring says "default: 5"
   and the end-to-end agent loop calls `k=5`; resolved by lever-value **branch 2** (app config:
   the loop's `k=5`) — post-build lever (CTX-C8). → AC14, AC15
10. **R10 — Toolbox retrieval is itself agent-callable.** [C] (CTX-A) `read_toolbox(query, k)`
    is registered as a tool so the agent can discover additional capabilities mid-execution
    (when current tools error or seem insufficient) beyond the initial per-turn toolset. → AC16
11. **R11 — Full tool-execution audit + bounded tool results in context.** [C] (CTX-B5) Every
    tool call is logged to the tool-log store as a §3 `ToolLogRow`: full untruncated result, a
    preview truncated to **2 000 UTF-8 bytes** (byte-safe), status `success`/`failed`,
    error message on failure, and the loop iteration in metadata. The result fed back to the
    LLM is capped at **3 000 characters**; when truncated it carries the exact notice
    `[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <id>]`.
    Tool logs are **not** preloaded into context (JIT-only by default). Sources: helper
    `write_tool_log`, L5 app loop. → AC17
12. **R12 — Workflow capture and quality-filtered reads.** [C] (CTX-A) After any turn that
    executed ≥1 tool call, the harness writes a workflow record: the query, the ordered step
    strings (`<tool>(<args-preview>) → success|failed`), an answer excerpt capped at 200 chars,
    and metadata (num_steps, success, timestamp). Workflow reads filter to `num_steps > 0`
    and instruct the model to *adapt* patterns, not copy them blindly. Turns with zero tool
    calls write no workflow. → AC18
13. **R13 — Entity extraction (non-fatal).** [C] (CTX-A) Entities are extracted by LLM from
    the user query and from the final answer (input capped at 500 chars per extraction), as a
    JSON array of `{name, type, description}` with `type ∈ {PERSON, PLACE, SYSTEM}` (`UNKNOWN`
    fallback); "none" is the empty array. Records are stored as text
    `"<name> (<TYPE>): <description>"` plus metadata. Extraction failures are swallowed —
    they must never fail the turn. → AC19 (`live`)
14. **R14 — Bounded agent loop with honest exhaustion.** [C] (CTX-B7) The loop runs at most
    **max_iterations = 10** (source: `call_agent` default). Each iteration either executes the
    model's tool calls (feeding results back as `tool`-role messages) or accepts a final
    answer and stops. On exhaustion without a final answer, the answer is exactly:
    "I was unable to complete the request within the allowed iterations." — never a fabricated
    result. → AC20, AC21 (`live`)
15. **R15 — Grounding and abstention.** [C] (CTX-A) Factual/technical claims are grounded in
    the Knowledge Base segment; when evidence is missing or ambiguous the agent states what is
    missing (uncertainty) before/instead of asserting, and only then uses a tool; it makes the
    minimum necessary tool calls. (Behavior encoded by the course's system prompt and KB
    segment instructions — expressed here as behavior, not prompt text.) → AC22 (`live`)
16. **R16 — One embedding model + one distance strategy, consistent across writes and reads.**
    [C] All five vector stores use the same embedding model (768-dim
    `paraphrase-mpnet-base-v2` by default, §2) and one distance strategy for both ingestion
    and retrieval. Distance strategy default: **cosine**. *Contradiction note:* the materials
    set cosine in the Lesson-3/Lesson-4 store code and the Lesson-3 narration states cosine
    aloud, while the Lesson-5/Lesson-6 notebooks configure Euclidean and one Lesson-3 markdown
    cell names `EUCLIDEAN_DISTANCE`; fails the §5.5 stakes test (near-equivalent at initial
    choice) and resolves by lever-value **branch 1** — the transcript narration of the lesson
    that introduces vector stores (Lesson 3) says cosine — post-build lever (CTX-C9). The
    course's own clean-slate warning ("consistent distance strategy, no stale data") is the
    consistency guard this rule encodes; mixing strategies or models across stores or across
    write/read is a defect. → AC23
17. **R17 — Search-and-store for external content.** [C] (CTX-A, CTX-C10) Any tool that fetches
    external content persists it to knowledge-base memory with source metadata so later
    queries answer from memory without re-fetching. The deep-ingestion tool
    (`fetch_and_save_paper_to_kb_db`) chunks full paper text at chunk_size **1500** / overlap
    **200** (source: the tool's defaults) and stores per-chunk metadata (source, arxiv_id,
    title, entry_id, published, authors, chunk_id, num_chunks, ingested timestamp), returning a
    saved-count confirmation naming the store; empty extraction and no-results cases return
    explicit non-exceptional messages. The discovery tool (`arxiv_search_candidates`) returns a
    JSON list of at most k candidates (default **5**; source: the tool's signature) with
    `arxiv_id`, `entry_id`, `title`, `authors`, `published`, and abstract capped at 2 500 chars
    (discovery reads metadata only — cheap before expensive ingestion; retriever caps: 8 docs,
    4 000 chars). → AC24 (`live`), AC25 (offline via fixture tool)
18. **R18 — Thread-scoped summary retrieval.** [C] Summary-context reads prefer/filter
    summaries for the active thread when a thread_id is known; `expand_summary` accepts an
    optional thread scope and reports "not found" per scope explicitly. (Source: helper
    summary methods — the app path; the Lesson-5 notebook's local variant predates thread
    scoping, CTX-C11.) → AC12 covers scope; AC11 asserts thread_id persisted.

**Post-build levers (body defaults, not Ledger rows — each carries its §5.5 lever-value
branch):** distance strategy = cosine (branch 1, R16); loop toolbox k = 5 (branch 2, R9);
token-limit map key (branch 2, R4); retrieval k's 3/3/5/10 (single-valued, R3); 80 % threshold
and 50/80 bands (single-valued, R4); chunking 1500/200 (single-valued, R17); caps 6000/4000/
2000-bytes/3000-chars/500-chars/200-chars/10-iterations (single-valued, R5/R11/R13/R12/R14);
augmentation synthetic-query count = 5 (single-valued, D10). Change any of these only through
§6 Ask First where flagged.

---

## 5. Acceptance Criteria ★ (the oracle)

### Fixture corpus (define FIRST; all facts authored for this spec — no course data copied)

The building agent MUST create these fixtures exactly as described and MUST NOT modify them to
make a test pass.

| Fixture | Contents (exact facts) |
|---|---|
| `fixtures/kb/coral-atlas.md` | "The Coral Atlas Project mapped 214 reef sites in the Meridian Sea between 2021 and 2023. Lead scientist: Dr. Imara Voss. Funding: the Bluewater Trust. Key finding: staghorn coverage declined 9 percent per year at unshaded sites." |
| `fixtures/kb/glacier-sensors.md` | "The Halvard Glacier array uses 36 LoRa sensor nodes reporting every 90 minutes. Battery life per node: 14 months. Maintainer: the Nordfell Institute. Known issue: node 22 drifts +0.4 °C after firmware 2.1." |
| `fixtures/kb/desert-battery.md` | "The Solara Flats storage pilot pairs 12 MWh of sodium-ion batteries with a 9 MW solar field near the town of Arrey. Operator: Meridian Grid Co. Round-trip efficiency measured in 2024: 87 percent." |
| `fixtures/conversation-seed.json` | A 30-message alternating user/assistant conversation (authored) in which a masters student plans a field study of low-power sensor networks. It deliberately contains one of each summary-heading category: technical facts (the Halvard array's 90-minute cadence; a CRC error on node 22), emotional context (the student says they are "nervous about the fieldwork window"), entities (Dr. Imara Voss; the Nordfell Institute; the LoRaWAN gateway "Kestrel-3"), and action items (email Dr. Voss by Friday; order 4 spare nodes). Long enough that its rendered form exceeds a test-scaled context threshold. **Failure-mode seed for F2/F3.** |
| `fixtures/turns-reference.json` | Two scripted user turns on one thread: (1) "List the three projects in the knowledge base with their operators or maintainers." (2) "Book time to review the second one." Turn 2 is resolvable only via conversational memory. **Seed for F1.** |
| `fixtures/tools.py` (fixture tools, registered at test start) | `lookup_reef_site(site_id)` → returns the coral-atlas facts for a site; `big_report()` → returns a deterministic 5 000-character report (**seed for F5**); `get_current_time(detailed)` → course utility tool; plus five distinct no-op tools with unrelated single-purpose descriptions (`convert_units`, `spell_check`, `roll_dice`, `hash_text`, `count_words`) so the registry (≥8 tools) exceeds k=5 (**seed for F4**); a duplicate re-registration of `lookup_reef_site` is attempted once (**seed for F8**). |
| `fixtures/llm-stubs.py` | [H] A scripted stand-in LLM client for offline ACs (the course used the live API; stubs are project hardening): `stub_empty_summarizer` (returns empty content twice, **seed for F6**), `stub_generic_labeler` (returns "Conversation summary", **seed for F10**), `stub_always_tool_caller` (always emits a `get_current_time` tool call, never a final answer, **seed for F7**), `stub_echo_answerer` (returns a fixed final answer with no tool calls). |

Offline ACs run with stubs and no network (after the one-time embedding-model download).
ACs tagged **`live`** need `OPENAI_API_KEY` (and network for AC24) and are excluded from the
offline run.

### Given / When / Then

| AC | Rule | Given | When | Then | Mode |
|---|---|---|---|---|---|
| AC1 | R1 | A fresh environment (no DB file) | The app initializes | All seven stores from the §3 `StoreName` enum exist with their declared fields (conversation: id, thread_id, role, content, timestamp, metadata, summary_id; tool log: the §3 `ToolLogRow` fields; vector stores: text + embedding + metadata), before any other behavior runs | offline |
| AC2 | R1, D5/D11 invariants | A process wrote 3 conversational rows, 1 KB doc, 1 summary, and 1 tool log, then exited | A **new process** starts against the same store and reads each memory type | All written records are returned unchanged; startup performed no wipe | offline |
| AC3 | R2 | Thread `t1` with 4 written messages, 2 of them marked with a summary_id | `read_conversational_memory("t1")` | Exactly the 2 unmarked messages return, ascending by timestamp, rendered `[HH:MM:SS] [role] content`; an empty thread returns the explicit no-messages placeholder | offline |
| AC4 | R2, R3 (F1) | The `turns-reference.json` script, KB seeded with the 3 fixture docs | Both turns run through the agent | Turn 2's answer identifies the Halvard Glacier array / Nordfell Institute (the second-listed project) without the user restating it — resolved from conversational memory | live |
| AC5 | R3, D7/D8 invariants | Thread with prior messages; KB/workflow/entity/summary stores populated; `stub_echo_answerer` as LLM | One agent turn runs | The assembled context starts with `# Question` and contains all five segment headings in §3 order; the user query and the stub's answer are both persisted to conversational memory even though the model made no tool call (deterministic ops ran without model discretion) | offline |
| AC6 | R4 | A 1 024 000-character string; loop model configured | `calculate_context_usage` / `monitor_context_window` | tokens = 256 000; percent = 100.0 against max 256 000; status `critical`; a 100 000-char string → status `ok`; an unknown model name → max 128 000 | offline |
| AC7 | R4, R7 (F2) | The 30-message `conversation-seed` loaded into thread `t2`; threshold scaled for test (or context padded) so usage > 80 %; `stub_empty_summarizer` replaced by a scripted summarizer stub returning a valid 4-heading summary | Context assembly runs for `t2` | Offload triggers before reasoning: a SummaryRecord exists, the conversation segment is the compaction stub, and the Summary Memory segment carries `[Summary ID: <id>] <description>` | offline |
| AC8 | R5 (F6) | `stub_empty_summarizer` (empty content on first and retry calls); the seed conversation text | Summarization runs | The retry was attempted; the deterministic fallback summary is stored containing all four headings in order, with a ≤500-char excerpt under Technical Information; no exception propagates | offline |
| AC9 | R5 | Live LLM; the seed conversation | Summarization runs | Output contains exactly the four §3 headings in order and mentions at least one authored technical fact, one entity, and one action item from the seed | live |
| AC10 | R6 (F10) | `stub_generic_labeler` returning "Conversation summary" as the label | A summary is stored | The stored description is NOT in the reject set; it equals the fallback builder's output (first ≥4-word content line, ≤12 words) | offline |
| AC11 | R7 | Thread `t2` with 30 unsummarized rows; scripted summarizer stub | `summarize_conversation("t2")` | A SummaryRecord with an 8-hex-char id, non-generic description, 4-heading summary, full source text, and `thread_id="t2"` exists; exactly those 30 rows now carry that summary_id; the result reports 30 messages summarized; no row was deleted | offline |
| AC12 | R7, R18, D9 invariant (F3) | The AC11 state | `expand_summary(<id>)` | Returns the summary text AND all 30 original messages, chronological, each with a timestamp; an unknown id (or wrong thread scope) returns an explicit not-found message | offline |
| AC13 | R8 (F9) | The AC11 state (all rows marked) | `summarize_conversation("t2")` again | Returns the nothing-to-summarize result; no new SummaryRecord; no row's summary_id changed | offline |
| AC14 | R9 (F8) | `lookup_reef_site` already registered | It is registered a second time | The toolbox store contains exactly one row named `lookup_reef_site`; the callable remains executable; a retrieval for reef lookups returns no duplicate names | offline |
| AC15 | R9 (F4) | All ≥8 fixture tools registered | Toolset retrieval for "what time is it right now" | Exactly 5 tool schemas are returned (never the full registry), each valid per §3 `ToolSchemaForLLM`; `get_current_time` is among them | offline |
| AC16 | R10 | The registered toolset | The toolbox store is inspected | `read_toolbox` itself exists as a registered, retrievable tool with a callable behind it | offline |
| AC17 | R11 (F5) | `stub_always_tool_caller` scripted to call `big_report()` once then answer | One agent turn runs | A ToolLogRow exists with the full 5 000-char result, a ≤2 000-byte preview, status `success`, and iteration metadata; the tool message fed to the LLM is ≤3 000 chars + the exact truncation notice naming the log id; a forced tool exception yields a `failed` row with `error_message` set and the turn continues | offline |
| AC18 | R12 | A turn that executed 2 tool calls (stub-scripted); a turn with 0 tool calls | Both turns complete | The first writes one WorkflowRecord (query, 2 ordered `→ success` steps, ≤200-char answer excerpt, num_steps=2); the second writes none; workflow retrieval returns only records with num_steps > 0 | offline |
| AC19 | R13 | Live LLM; the text "Dr. Imara Voss of the Nordfell Institute reviewed the Kestrel-3 gateway." | Entity extraction runs on it | ≥2 EntityRecords are stored with types from the §3 enum (e.g. a PERSON for Dr. Voss); extraction on gibberish/empty text stores nothing and raises nothing | live |
| AC20 | R14 (F7) | `stub_always_tool_caller`, max_iterations=3 for the test | One agent turn runs | Exactly 3 iterations execute, then the answer is exactly "I was unable to complete the request within the allowed iterations."; all 3 tool calls are logged | offline |
| AC21 | R14, D4 invariant | Live LLM + network; empty thread `50000`; KB pre-seeded with fixtures | The scripted demo sequence runs: (1) find a paper on an authored fixture topic via discovery, (2) save its content, (3) ask for key takeaways, (4) "summarize the conversation so far using your tool", (5) "What was my first question?" | Each turn ends within 10 iterations; (2) grows the KB; (4) creates a summary and marks rows; (5)'s answer states turn 1's question — recoverable only via summary expansion — proving native tool calling and end-to-end continuity | live |
| AC22 | R15 | Live LLM; KB seeded with fixtures only | Query: "What is the round-trip efficiency of the Solara Flats pilot, and who audited it?" | The efficiency answer is grounded in the fixture (87 percent); for the auditor — absent from all memory — the agent states the information is missing (or seeks it via a tool) rather than fabricating a name | live |
| AC23 | R16 | The five vector stores initialized; config inspected | Startup + one write/read round-trip per store | One embedding model instance and one distance strategy (cosine) are configured for all five stores, identical at write and read; a doc written to KB is retrieved by a paraphrase of its content (not its exact words) | offline |
| AC24 | R17 | Live network; empty KB | `arxiv_search_candidates("agent memory")` then `fetch_and_save_paper_to_kb_db(<first id>)` | Candidates parse as JSON with the §4 R17 keys and ≤2 500-char abstracts; the fetch stores >1 chunk with the full R17 metadata set incl. sequential chunk_id and correct num_chunks, and returns a confirmation naming the store and chunk count | live |
| AC25 | R17, D12 invariant | Offline; `lookup_reef_site` wrapped as a search-and-store fixture tool | The tool runs via the agent harness (stub-scripted) | Its fetched content lands in the KB with source metadata (source name, query, timestamp); a follow-up KB read answers from memory without re-invoking the tool | offline |

Coverage: every rule R1–R18 has ≥1 AC; every AC maps to a rule; every demonstrated failure
mode F1–F10 (CTX-B) appears as a rule, a fixture seed, an AC, and a CTX-B entry. D-row
invariants: D4→AC21, D5→AC2, D7→AC5, D8→AC5, D9→AC12, D10→AC15/AC16 (retrieval keyed on stored
descriptions), D11→AC1/AC2/AC23, D12→AC25. D1–D3/D6 invariants are empty (nothing to test).

---

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the offline AC suite after any change to memory, summarization, or toolbox code, and before declaring any AC met.
- Create stores idempotently on startup (R1); read/write memory only through the manager abstraction (D7 invariant).
- Persist every tool execution to the tool log (R11) and every turn's user/assistant messages to conversational memory (R2).
- Load secrets from the environment.

**Ask First** (derived from the course's spoken trade-offs; each cross-referenced)
- AF1 — Switching the context-reduction strategy to lossy-only or altering compaction so summaries stop linking back to source rows (→ D9): silently changes the recoverability guarantee; Lesson 5 warns summarization "will always lose a little bit of information".
- AF2 — Changing the embedding model or the distance strategy after any data is ingested (→ R16, D11): forces a wipe/re-embed/re-ingest — the course's clean-slate cells exist precisely to keep the distance strategy consistent.
- AF3 — Moving an operation between deterministic and agent-triggered (→ D8): changes a behavior guarantee (e.g. saves become discretionary, or an optional operation starts running automatically) without failing any AC; Lessons 3/6 argue the predictability-vs-cost trade-off.
- AF4 — Raising the per-turn toolset k or passing more than the retrieved toolset to the LLM (→ R9): re-invites the context-bloat / tool-selection degradation the course demonstrated (Lesson 4).
- AF5 — Changing the 80 % offload threshold, the status bands, or the token-estimate rule (→ R4): shifts when memory is compacted — a silent behavior change no test catches.
- AF6 — Turning docstring augmentation off (or on) globally (→ D10): changes retrieval separability/recall at registration-cost trade-off argued in Lesson 4.
- AF7 — Changing the 3 000-char tool-result cap or disabling full-result tool logging (→ R11): alters the audit and context-offloading guarantee ("move large payloads out of model context") argued in Lesson 6.
- AF8 — Running any store wipe/reset outside a test sandbox (→ R1): destroys the D5 persistence invariant.
- AF9 — [H] Changing summarization caps (6 000-char input, label rules) or max_iterations: post-build levers; not narrated as trade-offs by the course, flagged here as hardening.

**Never**
- Invent provenance, citations, sources, or entity facts; answer when the system should state that evidence is missing (R15).
- Mutate fixtures (§5) to make a test pass.
- Commit secrets, or reuse the course-lab credentials that appear in the materials as real credentials.
- Delete conversational source rows during compaction (R7), or wipe stores implicitly at startup (R1).
- Present the toolbox's full registry to the LLM in a normal turn (R9).

---

## 7. Test Plan & Self-Verification

Runnable commands (adjust only the project root):

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt          # pins chosen at build time (§2 honesty note)
python -m pytest tests/offline -q        # AC1–AC3, AC5–AC8, AC10–AC18, AC20, AC23, AC25 — no key, no network
RUN_LIVE=1 python -m pytest tests/live -q   # AC4, AC9, AC19, AC21, AC22, AC24 — needs OPENAI_API_KEY (+ network for AC24)
python app.py --thread 50000             # interactive demo; scripted sequence per AC21
```

The building agent MUST report results **per acceptance criterion**, each with cited evidence:
the test command run, the pass/fail output line, and relevant file paths (e.g. the SQLite file,
a dumped ToolLogRow, the printed resolved-decision checklist from §0). "Should pass",
"looks correct", or an unrun `live` AC reported as passing are treated as **failures** — they
mean it wasn't run. `live` ACs skipped for lack of a key must be reported as *skipped (live)*,
never as passed.

---

## Course Context Pack (embedded — agent-readable)

Concepts only — no code copied from the course. CTX anchors are position-independent.
Everything in CTX-A…C is durable; only CTX-D's names are perishable. Nothing in this spec
requires access to the course platform.

### CTX-A. The pattern

The course's central buildable pattern is the **memory-aware agent loop** over a **seven-type
memory core**:

`init stores → assemble partitioned context → check budget (offload >80%) → retrieve focused toolset → reason/act loop (log every tool call) → persist artifacts → answer`

Stage reasons:
1. **Init seven typed stores** — different memory types need different data models and retrieval strategies (exact/time-ordered vs semantic), coordinated by one memory-manager abstraction so the agent never touches storage directly.
2. **Assemble partitioned context** (conversation / knowledge base / workflow / entity / summary segments under markdown headings) — segment labels + usage instructions make the model *memory-aware*: it knows what each memory is for and how to prioritize on conflict.
3. **Budget check + offload** — context windows are finite; deterministic monitoring prevents overflow, and compaction keeps a recovery path (summary IDs + expansion) instead of silent loss.
4. **Semantic tool retrieval (Toolbox)** — tools are memory too: embed descriptions, retrieve only the few relevant per query; scales to hundreds of tools without context bloat or selection degradation.
5. **Reason/act loop with tool logging** — bounded iterations; full tool outputs go to the database (context offloading), only bounded results go back into context.
6. **Persist artifacts** (conversation, workflow trajectories, entities, summaries) — the agent *learns*: discovered information and executed patterns become reusable memory, enabling long-horizon tasks and cross-session continuity.

Also taught as framing (teaching structure, not decisions): the short-term/long-term memory
taxonomy (semantic cache, working memory vs procedural/semantic/episodic), the "agent memory
core = the database" concept, the agent-stack/memory-layer picture, the memory lifecycle
(ingest → enrich → store → organize → retrieve → LLM → write back), and the naive→augmented→
aware progression. The running example is a research assistant the notebooks nickname
**ArxivScout**.

### CTX-B. Failure-mode catalog

1. **Stateless cross-turn amnesia** — symptom: the agent cannot resolve "book the first one" and asks the user to re-specify; cause: no persisted interaction history, context lost between turns/sessions; fix: deterministic conversational persistence + deterministic context preload every turn; enforced by R1–R3, AC2–AC5.
2. **Context overflow** — symptom: long conversations crash the turn or evict important history; cause: finite context window, unbounded accumulation; fix: estimate usage every turn, offload at >80 %; enforced by R4, AC6–AC7.
3. **Unrecoverable summarization loss** — symptom: after compaction the agent can't answer "what was my first question?"; cause: lossy summaries with no path back to originals; fix: store full source + mark rows with summary_id + expand-on-demand; enforced by R7/R18, AC11–AC12 (and live AC21 step 5).
4. **Tool-context bloat / selection degradation** — symptom: with many tools the model picks wrong tools, latency and cost rise; cause: all tool definitions stuffed into context; fix: toolbox memory + top-k semantic retrieval per query; enforced by R9, AC15.
5. **Tool-output flooding** — symptom: one large tool result devours the window; cause: raw payloads routed through the model; fix: persist full output to the tool log, feed the model a bounded result + log-id notice; enforced by R11, AC17.
6. **Empty/failed summarizer output breaking the pipeline** — symptom: a blank LLM response aborts compaction; cause: model returns no content; fix: retry with a simpler instruction, then a deterministic 4-heading fallback; enforced by R5, AC8.
7. **Runaway agent loop** — symptom: endless tool-calling; cause: no stop condition; fix: max-iterations bound + honest templated exhaustion answer; enforced by R14, AC20.
8. **Duplicate tool registration** — symptom: retrieval returns the same tool twice, crowding the toolset; cause: re-running registration; fix: name-dedup at write and at read; enforced by R9, AC14.
9. **Re-summarizing processed messages** — symptom: duplicate summaries, drifting content; cause: no marker on already-summarized rows; fix: select only unmarked rows; second pass is a no-op; enforced by R8, AC13.
10. **Generic summary labels** — symptom: "Conversation summary" labels make summary references useless for JIT selection; cause: weak model labeling; fix: reject-list + deterministic specific-label fallback; enforced by R6, AC10.

### CTX-C. Decision background (reference only — decisions live in the Ledger)

1. **Store realization** (→ Ledger D11): the course ran Oracle AI Database 26ai in Docker with an admin-provisioned VECTOR user, LangChain's OracleVS per vector table, and IVF vector indexes created by a helper (the notebooks' markdown *says* HNSW, but the helper deliberately creates IVF — "NEIGHBOR PARTITIONS", target accuracy 95 — to dodge specific Oracle-Free errors it names). At fixture scale no index is needed at all; the index story matters only when you scale, which is why it lives in D11's Options, not the Default.
2. **Why relational for conversation/tool-log but vector for the rest** (→ D11 invariant): chat history needs exact retrieval by thread id in time order — similarity is the wrong tool; the other five types are retrieved by meaning. This dual-mode requirement is the store row's invariant.
3. **Reduction techniques** (→ D9): the course teaches Context Summarization (lossy compression, clean-window restart) vs Context Compaction (offload to DB under an ID + description; the model pulls detail back when needed), then *builds the pairing*: summarize, store with full source, mark rows, expand on demand. Mechanism behind the trade-off: summarization spends tokens once and loses detail; compaction spends storage and a retrieval hop but is reversible.
4. **Deterministic vs agent-triggered** (→ D8): deterministic ops give context bootstrapping ("the agent can't choose to look up what it doesn't know exists"), reliability ("don't want the agent to forget to save"), and debuggability; agent-triggered ops give relevance filtering and cost control (deep retrieval, consolidation, external tools only when judged worthwhile). The Lesson-3 classification table and the Lesson-6 app disagree on `read_summary_context` and `write_entity` (table: agent-triggered; app: deterministic each turn) — D8's default follows the app.
5. **Docstring augmentation** (→ D10): registration can send docstring + source to an LLM for an enriched description plus synthetic trigger queries; the enriched text is what gets embedded — mechanism: richer, more separable embedding text raises recall and separability in the tool-embedding space.
6. **Model naming and token limits** (→ D4, R4): the loop's chat default is `gpt-5-mini` (app notebook) while the helper's memory-op defaults are `gpt-5`; the 256 000 token-limit map is keyed `gpt-5-mini` in the Lesson-5 notebook but `gpt-5` in the helper — same value, different key; unknown models fall back to 128 000. Resolved as a body default by lever branch 2 (app config).
7. **`get_current_time` augment flag** (→ D10): registered augmented in the Lesson-4 notebook cell, unaugmented in the helper's common-tools path the Lesson-6 app uses.
8. **Toolbox k** (→ R9): manager default 3; registered tool signature default 3 with a docstring claiming 5; app loop retrieves 5; lesson prose says "typically 3–5". Body default 5 by lever branch 2.
9. **Distance strategy** (→ R16): cosine in Lesson-3/4 store configs and Lesson-3 narration; Euclidean in Lesson-5/6 notebook configs and one Lesson-3 markdown key-components list. Body default cosine by lever branch 1 (narration of the introducing lesson). The clean-slate drop cells exist to guarantee strategy consistency across a lesson run — the consistency rule R16 keeps that guard without the wipe.
10. **Search-and-store** (→ D12, R17): the web-search tool doesn't just return results — it writes each result into the knowledge base with title/url/score/query/timestamp so the agent "learns from its searches"; the arXiv deep-ingest tool applies the same pattern to full papers (chunk 1500/200), keeping large payloads out of model context.
11. **Summary thread-scoping** (→ R18): the Lesson-5 notebook's local summary writer has no thread scope; the helper version used by the Lesson-6 app adds thread_id scoping and thread-filtered summary-context reads. The app path is the default.
12. **Instructor heuristics**: providers recommend exposing roughly 10–20 tools max for reliable selection; ~4 chars/token is a serviceable estimate (some models nearer 2); prompt wording determines summarization quality — vary it per problem; validate tool registration on a low-risk utility tool first; record workflows so the model doesn't "figure it out on the fly" each time.

### CTX-D. Perishable assumptions

Treat these as **search keywords against current docs, not guaranteed imports**. The concepts
in CTX-A…C are durable; only these names are perishable. The course's installs were **unpinned**
(no version numbers exist in the materials).

- Packages/APIs: `langchain-oracledb` (`OracleVS`, `OracleVectorizerPreference`), `langchain_huggingface.HuggingFaceEmbeddings` (some lessons import the older `langchain_community.embeddings` path), `langchain_community` (`DistanceStrategy`, `ArxivRetriever`, `ArxivLoader`), `langchain_text_splitters.RecursiveCharacterTextSplitter`, `sentence-transformers`, `oracledb`, `openai` chat-completions with `tools`/`tool_choice="auto"` and `max_completion_tokens`, `tavily-python`, `datasets` (streaming), `pymupdf`, `dotenv`, `pydantic`.
- Models: `gpt-5`, `gpt-5-mini`; embedding `sentence-transformers/paraphrase-mpnet-base-v2` (768-dim).
- Oracle-era artifacts (provenance only; not used by the default build): Oracle AI Database 26ai in Docker; admin user `system`; a `VECTOR` user with a lab password; DSN `127.0.0.1:1521/FREEPDB1`; connection `program` tag `devrel.deeplearning.course_1`; index names `*_vs_ivf`; hybrid preference `KB_VECTORIZER_PREF`; lab quirk: "Admin connection failed" on first run resolves by waiting and re-running. Never reuse lab credentials.
- Demo-data names: HuggingFace dataset `nick007x/arxiv-papers` (100 streamed records); demo query paper "MemGPT"; assistant nickname "ArxivScout"; demo thread id `50000`; sample 30-message PhD-research conversation shipped in the helper (re-expressed here as an authored fixture, not copied).

### CTX-E. Provenance map (transcript numbering — authoritative)

Platform numbering per the transcripts. The notebook dump's own lesson-map headers drift from
both the notebook titles and the transcripts (e.g. it labels the Memory-Manager notebook
"Lesson 4"); transcripts win. Notebook files are numbered L2–L5 and sit one-to-three lessons
off the platform numbers.

| Transcript lesson | Title | Notebook file | Contributed |
|---|---|---|---|
| Lesson 1 | Introduction | — | Course goal: memory engineering as first-class infrastructure (CTX-A framing) |
| Lesson 2 | Why AI Agents Need Memory | — | Stateless-agent failure demo (CTX-B1); conversational memory + its limits (D7's argued trade-off); memory taxonomy; RAG→memory bridge; Agent Memory Core (CTX-A) |
| Lesson 3 | Constructing The Memory Manager | L2.ipynb | Seven stores + manager (CTX-A stages 1–2, CTX-C1–C2); deterministic/agent-triggered classification (D8, CTX-C4); cosine narration (CTX-C9); index rationale; KB ingest/read demo (CTX-C10 seed) |
| Lesson 4 | Scaling Agent Tool Use with Semantic Tool Memory | L3.ipynb | Toolbox pattern (CTX-B4, CTX-B8); augmentation argument (D10, CTX-C5); Tavily search-and-store (D12, CTX-C10); arXiv discovery + deep ingestion (R17) |
| Lesson 5 | Memory Operations: Extraction, Consolidation, and Self-Updating Memory | L4.ipynb | Summarization vs compaction argument (D9, CTX-C3); token monitoring (CTX-B2); summary pipeline with marking + expansion (CTX-B3, B6, B9, B10); workflow-memory rationale |
| Lesson 6 | Memory Aware Agent | L5.ipynb | Agent loop + harness (CTX-A stages 2–6); system-prompt memory awareness and priority order (R3, R15); tool-log offloading (CTX-B5); the 5-query continuity demo (AC21 shape); "summarize is both deterministic and agent-triggered" (D8) |
| Lesson 7 | Conclusion | — | "Take these patterns, adapt them" — the pattern-over-product close that licenses D11's substitution |

Nothing in this spec requires platform access.

---

*Version 1.0 · Course: Agent Memory — Building Memory-Aware Agents · Learner project: `[project]` (default: memory-aware research-assistant agent) · Living document: when the building agent produces something unexpected, add the missing constraint here and re-run.*
