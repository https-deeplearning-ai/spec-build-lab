# Spec: Memory-Aware Research Assistant — Standalone Takeaway

> **This file is self-contained.** The embedded Course Context Pack (CTX-A…CTX-E, at the end)
> replaces all external course references — nothing in this spec requires access to the course
> platform, its notebooks, or its transcripts. `(CTX-X)` anchors mark course-derived knowledge.
> The **Decision Ledger** below holds every point where the build could diverge, each pinned to
> one course-derived default, so the spec is buildable and evaluatable **as-is with zero intake**;
> `[bracketed]` values mark where a learner *may* substitute their own choice.
> *Provenance: generated from the "Agent Memory: Building Memory-Aware Agents" course notebooks +
> transcripts on 2026-07-20.*
>
> **Variant note:** this file is a variant of the canonical `spec.md` in this course folder.
> Oracle AI Database 26ai has been removed as a selectable Options entry in Ledger rows **D14**
> (persistent store) and **D5** (environment) — it is no longer offered as something to build.
> The course's actual use of Oracle remains recorded as provenance in D14's Default note, §1,
> §2, and CTX-D; only the build-time *choice* was removed, not the historical fact.

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

## Decision Ledger (§0 above requires the build agent to present these before building)

These are the points where this build could diverge. Every row has a course-derived default, so
the spec is buildable and evaluatable as-is; change a row only when applying to a real project or
when you have reason to prefer another option.

| # | Category | Decision | Invariant (must hold) | Default (course-derived) | Options | Trade-off | Owner |
|---|----------|----------|-----------------------|--------------------------|---------|-----------|-------|
| D1 | learner | `[project]` — what the agent is for. Default is the **course's example realization** (its running demo scenario), expected to be swapped when your project differs — the invariants, not the example, are what must survive. | — | A **memory-aware agentic research assistant**: a CLI/REPL chat agent that finds, saves, and discusses research papers across sessions, remembering prior findings and preferences (§3 project precedence, branch 1: the course's example scenario shape re-expressed on the synthetic fixture corpus of §5). | Course example shape: research assistant (course default); any domain assistant needing persistence (support bot, coding copilot, ops runbook agent) | Swapping the project keeps every memory mechanism; only the toolset (D15) and seed data (D2) change with it. | learner |
| D2 | learner | `[data/inputs]` — what the agent operates on. Default is a fixture stand-in for the **course's example data**; swap when D1 changes. | — | The **synthetic fixture corpus of §5** (two authored paper-notes files + one authored 12-message seed conversation), ingested at setup. | Fixture corpus (default); the learner's own documents/threads; the course streamed 100 records of a public arXiv dataset and live arXiv PDFs (course default) | Real corpora need the same ingest path (embed + metadata); large corpora may need an ANN index (see §2). | learner |
| D3 | learner | `[goal]` — what "working" means. | — | **Cross-session continuity**: the agent answers follow-ups without re-doing discovery, keeps context under budget via recoverable summarization, and can still recover the thread's first question after summarizing (the §5 oracle). | Continuity guarantee (default); latency/cost targets; retrieval-precision targets | Stricter retrieval goals push toward reranking/hybrid search — out of course scope (§1 Not Included). | learner |
| D4 | learner | `[model/provider]` — the LLM behind reasoning, summarization, augmentation, extraction. | Must support **native (OpenAI-style) tool calling** and a system role; its context-window size must be known to the budget monitor (R6). | **OpenAI**, per the materials: `gpt-5-mini` for the agent loop, `gpt-5` for docstring augmentation and entity extraction. Requires `OPENAI_API_KEY` (§2); LLM-dependent ACs are tagged `scripted` or `live` so the offline oracle still runs (§5). *Note (course-contradicted, carried here):* the L4 notebook's token-limit map lists only `gpt-5-mini: 256000` while `helper.py`'s lists only `gpt-5: 256000`, and helper function defaults say `gpt-5` where the L5 loop calls `gpt-5-mini` — the materials never reconcile the two; this spec pins the loop to `gpt-5-mini` with a 256,000-token budget (the L5 loop's actual call path). | OpenAI gpt-5-mini + gpt-5 (course default); any tool-calling model (Anthropic, local via an OpenAI-compatible server) | Changing provider means re-checking the tool-call message shapes and the token budget in R6; prompts (summarization, extraction) may need re-tuning. | learner |
| D5 | learner | `[environment]` — where it runs. | **All seven memory stores must survive process restarts** (memory is external to the model and persistent). | Local machine, Python 3.11+, single on-disk database file (realization: D14). First run needs network to download the embedding model; no Docker, no admin setup. | Local single file (default); any server environment | A shared/server environment adds connection management the course's local pattern doesn't cover. | learner |
| D6 | learner | `[out-of-scope]` — anything explicitly unwanted. | — | Nothing beyond §1 "Not Included". | Add exclusions freely | Exclusions only shrink scope; they never relax the D5/D7 invariants. | learner |
| D7 | design-argued | **Memory-core topology** — which memory types exist and their storage class. | Seven memory types, each with a dedicated store: **conversational + tool-log memory retrievable by exact key (thread) in chronological order; knowledge-base, workflow, toolbox, entity, and summary memory retrievable by semantic similarity.** | The course's seven stores: `CONVERSATIONAL_MEMORY` and `TOOL_LOG_MEMORY` as SQL-style tables; `SEMANTIC_MEMORY` (knowledge base), `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY` as vector stores — all fronted by one memory-manager abstraction (CTX-A, CTX-C1). | Seven-store split (course default); fewer stores (e.g. fold entity into KB); more (add semantic cache) | Lesson 3 argues the split: conversation needs *exact* retrieval by thread id, "not similarity search", while knowledge/workflow/toolbox/entity/summary need meaning-based lookup; collapsing stores loses the retrieval strategy matched to each type. | course |
| D8 | design-structural | **Deterministic vs agent-triggered operation split** — which memory operations the harness runs every turn vs which the model may invoke. | Context-building reads (conversation, KB, workflow, entity, summary-index) and post-turn writes (conversation, workflow) run **deterministically every turn**; judgment operations (expand a summary, summarize-and-store, external search, entity writes) are **also exposed as model-invocable tools**. | The course's classification (CTX-C2): deterministic = the five preload reads + conversation/workflow writes + the >80% budget check; agent-triggered = `expand_summary`, `summarize_and_store`, external search, deep paper ingest; `read_toolbox` is both. *Note (course-contradicted, carried here):* the Lesson 3/L2-notebook classification table marks entity **writes** and `read_summary_context` agent-triggered, yet the Lesson 6 loop runs both deterministically (entity extraction after query and answer; summary-index read in every preload) — this spec follows the Lesson 6 working loop. | Course split (course default); fully agent-managed memory; fully hardcoded memory | Moving reads/writes to model discretion risks "forgot to save" gaps and the chicken-and-egg problem (CTX-B7); hardcoding judgment ops (e.g. always summarize) wastes tokens and clutters memory (CTX-C2). | course |
| D9 | design-argued | **Partitioned context window + memory-aware system prompt** — how assembled memory is presented to the model. | The model input carries the question first, then **one labeled segment per memory type**, and the model instructions name each segment, its usage guidance, and a conflict-priority order (R16). | Markdown-heading partition in fixed order: `# Question`, then `## Conversation Memory`, `## Knowledge Base Memory`, `## Workflow Memory`, `## Entity Memory`, `## Summary Memory`, each segment self-describing ("what this memory is / how you should leverage it"). | Partitioned + self-describing (course default); one mixed context block; structured JSON context | Lesson 6 argues markdown headings let the model exploit its latent grasp of hierarchical structure, giving "structured, role-specific context instead of one mixed block"; a mixed block loses per-store semantics. | course |
| D10 | design-argued | **Context-window reduction strategy** — what happens when the context outgrows its budget. | Reduction must be **recoverable**: whatever is compressed out of the live context stays retrievable in full from the store via an id-addressable link. | The course's combined pipeline: threshold-triggered (deterministic, >80% of budget) and tool-triggered (agent-invoked) **summarization with write-back links** — summarize unsummarized thread messages, store the summary, mark the exact source rows with the `summary_id`, keep only a summary reference in context, and expand on demand (JIT) via the expand tool (CTX-C3). | Recoverable summarize-and-link (course default); pure lossy summarization; pure compaction (offload raw content by id, no summary) | Lesson 5 argues the trade-off aloud: summarization "will always be a lossy technique", while compaction keeps everything but preloads nothing useful — the shipped design pairs a lossy summary for the live window with a lossless database path back to the originals. | course |
| D11 | design-argued | **Tool-description augmentation** — what text gets embedded for each tool. | The text embedded for retrieval must be **rich enough to separate tools semantically** (retrieval is keyed on descriptions, not names). | Augmented registration as the course does for most tools: an LLM rewrites the docstring using the function's source, plus ~5 synthetic example queries; name + augmented description + signature + queries form the embedding text. Registration is idempotent per tool name (R5). | LLM-augmented descriptions (course default); raw docstrings only (the course registered its arXiv candidate-search tool unaugmented) | Lesson 4 argues augmentation buys higher separability and recall in the embedding space at the cost of one LLM call per registration; weak one-line docstrings retrieve poorly. | course+learner |
| D12 | design-argued | **Tool-result flow: full log + bounded excerpt** — what the model sees of a tool's output. | Every tool execution is **fully persisted** (args, complete result, status, errors) outside the context window; the model receives only a **bounded excerpt with an id pointer** back to the full record. | Persist every call to the tool-log store; pass at most 3,000 characters of the result to the model, appending a truncation notice naming the log id when cut (R10). | Log + bounded excerpt (course default); pass full outputs into context; discard raw outputs | Lesson 6 calls this context offloading — "move large payload handling out of the model context and into memory infrastructure"; skipping the log loses the audit trail and the JIT retrieval path, while full outputs blow up the window (CTX-B6). | course |
| D13 | design-argued | **Search-and-store acquisition** — what acquisition tools do with what they find. | Any tool that acquires external content **persists its results to knowledge-base memory with source metadata in the same call**, before/independent of what the model does with them. | Course pattern: search/fetch tools write each result (or chunk) into the knowledge base with source metadata (title, source id, timestamps, chunk indices), so information discovered once is retrievable in later turns without re-searching. | Search-and-store (course default); return-only tools (results live and die in one turn) | Lesson 4 argues this is how the agent "learns from its searches" — repeat questions stop costing API calls; the cost is knowledge-base growth and possible staleness of stored search results. | course |
| D14 | realization | **Persistent store (the Agent Memory Core)** — the database behind all seven stores. | **One persistent database is the memory core**: it serves both the exact-key/chronological stores and the semantic-similarity stores (topology: D7), and survives restarts (D5). | **SQLite** (single on-disk file, Python stdlib driver): SQL tables for conversational + tool-log memory; the five vector stores as tables holding text, JSON metadata, and the embedding, searched by exact similarity at fixture scale (indexing & distance strategy: §2). The lightest self-contained realization — zero setup, no admin bootstrap, no container (course provenance: the course itself ran Oracle AI Database 26ai in Docker with admin/tablespace setup and a dedicated DB user; not offered as a build option in this variant — see CTX-D for the historical record). | SQLite single-file (default); Postgres + pgvector; any DB offering both exact and vector retrieval | Switching stores means migrating schemas and re-embedding nothing (embeddings are store-agnostic) but re-implementing the store adapters. | course+learner |
| D15 | realization | **External acquisition toolset** — which live tools the default agent registers. | At least one **agent-triggered external acquisition tool** exists and follows search-and-store (D13). | The course's **keyless arXiv tools only**: a candidate-search tool returning structured JSON (id, title, authors, published, abstract) and a deep-ingest tool (fetch PDF → text → chunk → store to KB), plus a local current-time utility and the summary tools (expand, summarize-and-store) and self-lookup (`read_toolbox`). *§3 dependency precedence, branch 1* — the course's Tavily web search needs an API key (heavy); arXiv access is keyless and setup-free, so it stays (its ACs are tagged `live`), while Tavily becomes an option. These are the **course's example tools** — swap them when `[project]` (D1) differs. | Course toolset incl. Tavily web search with `TAVILY_API_KEY` (course default); keyless arXiv-only toolset (default); the learner's own domain tools | Dropping Tavily loses general web search (the agent only acquires from arXiv); adding it back is one keyed client + one registered tool following D13. | course+learner |

## 1. Objective

Build a persistent, memory-aware research assistant: a chat agent that, for a working engineer,
**remembers across sessions** — conversations, acquired knowledge, past workflows, entities, and
summaries — by treating an external database as its memory core, so that follow-up requests
resolve without repeating discovery and long threads never overflow the model's context window
(pattern: CTX-A).

### Not Included ★

- **Multi-user support, auth, or any UI beyond a CLI/REPL chat loop.**
- **Short-term-memory subsystems the course names but never builds**: semantic caching of LLM
  responses and session scratchpads beyond the live context window.
- **Hybrid (lexical+vector) search** — the course's store manager exposes a hybrid-search hook
  but never exercises it; excluded here.
- **Reranking models, graph-traversal retrieval, memory decay/forgetting policies, and
  embedding-model fine-tuning** — mentioned as concepts in the lessons, never implemented.
- **Oracle-specific operations** (tablespace admin, DB user provisioning, vector-memory pools) —
  they belong to the course's store realization, not the pattern (D14).
- **Integration into an existing codebase** — this spec targets the standalone takeaway only;
  the Ledger's Invariant column is written to serve as the future integration contract.
- `[out-of-scope]` — learner exclusions (D6; default: none).

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python 3.11+ | Course-era Python version is not stated in the materials. |
| Persistent store | SQLite (stdlib `sqlite3`), one on-disk file | Decision Ledger **D14** — learners change it there, not here. |
| Vector search | Exact (brute-force) similarity at fixture scale — add an ANN index only when corpora grow | One distance strategy — **cosine** — used consistently across all stores, write & read (R15). Both are tunable levers, not decisions: the course used both cosine and euclidean across lessons (tables wiped between them; near-equivalent for normalized embeddings) and built its ANN index (IVF/HNSW) only for the cloud store. |
| Embeddings | `sentence-transformers/paraphrase-mpnet-base-v2` (768-dim, local CPU) | The course's single embedding model for all stores and both write/read paths (CTX-C5). First run downloads it (keyless network). |
| LLM | OpenAI SDK (current stable) | Ledger **D4**. `OPENAI_API_KEY` required for scripted-interface parity and live ACs. |
| arXiv access | `arxiv` + `pymupdf` (current stable) | Ledger **D15**. The course reached arXiv through LangChain community wrappers — those names are perishable, see CTX-D. |
| Dependency pins | Pin exact versions **at build time** to current stable in a lockfile you generate | **Honest era note: the course's `requirements.txt` installs everything unpinned** (no versions at all, LangChain-family + `oracledb` + `openai` + `tavily-python` era); do not invent course pins. Era-specific import names → CTX-D. |
| Secrets | `.env` file loaded at startup; `OPENAI_API_KEY` (required), `TAVILY_API_KEY` (only if D15 is switched) | Never hardcoded and never committed. (The course notebooks hardcode local DB credentials — do not reproduce that.) |

Default store names (single-valued course constants; body defaults, not Ledger rows):
`CONVERSATIONAL_MEMORY`, `SEMANTIC_MEMORY` (knowledge base), `WORKFLOW_MEMORY`,
`TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY`, `TOOL_LOG_MEMORY` — identical in every
course notebook that declares them.

## 3. Input/Output Contracts ★

Core memory records and the agent turn result. These are the shapes tests assert against;
implementations may add fields but MUST NOT violate these.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$defs": {
    "ConversationRecord": {
      "type": "object",
      "required": ["id", "thread_id", "role", "content", "timestamp"],
      "properties": {
        "id": { "type": "string", "minLength": 1 },
        "thread_id": { "type": "string", "minLength": 1 },
        "role": { "type": "string", "enum": ["user", "assistant"] },
        "content": { "type": "string" },
        "timestamp": { "type": "string", "format": "date-time" },
        "metadata": { "type": "object" },
        "summary_id": {
          "type": ["string", "null"],
          "pattern": "^[0-9a-f]{8}$",
          "description": "null until consolidated; set once, to the id of the summary that absorbed this row"
        }
      }
    },
    "ToolLogRecord": {
      "type": "object",
      "required": ["id", "thread_id", "tool_name", "tool_args", "result", "result_preview", "status", "timestamp"],
      "properties": {
        "id": { "type": "string" },
        "thread_id": { "type": "string" },
        "tool_call_id": { "type": ["string", "null"] },
        "tool_name": { "type": "string" },
        "tool_args": { "type": "string", "description": "JSON-serialized arguments" },
        "result": { "type": "string", "description": "FULL untruncated output" },
        "result_preview": { "type": "string", "description": "≤ 2000 bytes UTF-8-safe truncation of result" },
        "status": { "type": "string", "enum": ["success", "failed"] },
        "error_message": { "type": ["string", "null"] },
        "metadata": { "type": "object" },
        "timestamp": { "type": "string", "format": "date-time" }
      },
      "if": { "properties": { "status": { "const": "failed" } } },
      "then": { "required": ["error_message"] }
    },
    "SummaryRecord": {
      "type": "object",
      "required": ["id", "summary", "description", "full_content"],
      "properties": {
        "id": { "type": "string", "pattern": "^[0-9a-f]{8}$" },
        "summary": { "type": "string", "description": "structured text containing the four R8 headings" },
        "description": { "type": "string", "minLength": 8, "description": "specific 8–12-word label; never a generic 'Conversation summary'" },
        "full_content": { "type": "string", "description": "the exact source transcript that was summarized" },
        "thread_id": { "type": ["string", "null"] }
      }
    },
    "WorkflowRecord": {
      "type": "object",
      "required": ["query", "steps", "answer_excerpt", "num_steps", "success", "timestamp"],
      "properties": {
        "query": { "type": "string" },
        "steps": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
        "answer_excerpt": { "type": "string", "maxLength": 200 },
        "num_steps": { "type": "integer", "minimum": 1 },
        "success": { "type": "boolean" },
        "timestamp": { "type": "string", "format": "date-time" }
      }
    },
    "EntityRecord": {
      "type": "object",
      "required": ["name", "type", "description"],
      "properties": {
        "name": { "type": "string", "minLength": 1 },
        "type": { "type": "string", "enum": ["PERSON", "PLACE", "SYSTEM", "UNKNOWN"] },
        "description": { "type": "string" }
      }
    },
    "RetrievedToolSchema": {
      "type": "object",
      "required": ["type", "function"],
      "properties": {
        "type": { "const": "function" },
        "function": {
          "type": "object",
          "required": ["name", "description", "parameters"],
          "properties": {
            "name": { "type": "string" },
            "description": { "type": "string", "minLength": 1 },
            "parameters": {
              "type": "object",
              "required": ["type", "properties", "required"],
              "properties": { "type": { "const": "object" } }
            }
          }
        }
      }
    },
    "AgentTurnResult": {
      "type": "object",
      "required": ["thread_id", "final_answer", "steps", "completed"],
      "properties": {
        "thread_id": { "type": "string" },
        "final_answer": { "type": "string", "minLength": 1 },
        "steps": { "type": "array", "items": { "type": "string" } },
        "completed": { "type": "boolean", "description": "false only when the iteration cap (R13) was hit" }
      }
    }
  }
}
```

Toolbox retrieval returns an array of `RetrievedToolSchema` with **unique** `function.name`
values (dedup rule R4). Retrieved tool count per turn: a single config value, **k=5** (R4).

## 4. Business Rules

Provenance labels: **[C]** course-demonstrated (traceable, with CTX anchor) · **[H]** project
hardening (added by this spec; the course did not demonstrate it — said so explicitly).

1. **R1 — Deterministic conversation persistence.** [C] Every user query and every final
   assistant answer is written to conversational memory with role, thread id, and timestamp, by
   the harness — never at model discretion (prevents CTX-B1). → AC1, AC12, AC20
2. **R2 — Deterministic context preload.** [C] Every turn, before the model is called, the
   harness reads all five context segments (conversation by thread; knowledge base, workflow,
   entity by query similarity; summary index by query+thread) and assembles them (prevents
   CTX-B7). Per-segment read defaults, each from its single course config: conversation limit 10
   messages, knowledge base k=3, workflow k=3, entity k=5, summary index k=10. → AC3, AC13
3. **R3 — Conversation reads are thread-scoped, chronological, and exclude consolidated rows.**
   [C] Reads filter to the thread, order by timestamp ascending, and skip rows whose
   `summary_id` is set; when nothing remains, the segment states that explicitly (prevents
   CTX-B5). → AC2, AC8
4. **R4 — Focused tool retrieval.** [C] Each turn passes the model only the toolbox's semantic
   top matches for the query (top-k, **k=5** — a single config value), deduplicated by tool name,
   as OpenAI function-format schemas (§3) (prevents CTX-B2). Semantic retrieval is the baked-in
   approach the course teaches for scaling tool use; for a tiny static toolset it simply returns
   all tools, so it is safe regardless of tool count. → AC4, AC17
5. **R5 — Idempotent, enriched tool registration.** [C] Registering a tool stores its
   description + embedding in the toolbox store; with augmentation enabled (D11) the stored
   description is LLM-enriched from docstring + source and ~5 synthetic queries join the
   embedding text; re-registering an existing tool name never writes a duplicate row. → AC5, AC18
6. **R6 — Context budget monitoring.** [C] Token usage is estimated as `len(chars) // 4`
   against the model's budget (256,000 for the default D4 model; 128,000 fallback for unknown
   models); status is `ok` below 50%, `warning` 50–79%, `critical` at ≥80% (prevents CTX-B3).
   [H] The budget is injectable so tests can shrink it. → AC6
7. **R7 — Threshold offload.** [C] When assembled memory context exceeds 80% of budget, the
   harness (not the model) summarizes the thread's unconsolidated conversation, replaces the
   conversation segment with a short stub pointing at summary references, appends the
   `[Summary ID: …]` reference under the summary segment — and never summarizes the
   `# Question` text (prevents CTX-B3). → AC7
8. **R8 — Structured summarization.** [C] Summaries are produced with exactly four headings —
   Technical Information / Emotional Context / Entities & References / Action Items & Decisions —
   from at most the first 6,000 characters of input, with one simpler-prompt retry and then a
   deterministic non-empty fallback if the model returns nothing; each summary gets an 8-char
   hex id and a specific 8–12-word label (generic labels like "Conversation summary" are
   rejected and replaced). → AC8, AC14
9. **R9 — Recoverable consolidation.** [C] Summarizing a thread marks **exactly** the consumed
   rows with the new `summary_id`; expanding a summary returns the stored summary text plus all
   original messages, chronologically, with timestamps; already-marked rows are never
   re-summarized (prevents CTX-B4, CTX-B5). → AC8, AC9, AC20
10. **R10 — Complete tool logging with bounded excerpts.** [C] Every tool execution writes a
    tool-log record (args, full result, ≤2000-byte preview, status, error message on failure);
    the model receives at most 3,000 characters of the result — when truncated, the message ends
    with a notice naming the log id where the full output lives (prevents CTX-B6). → AC10
11. **R11 — Workflow write-back.** [C] Any run that made ≥1 tool call persists one workflow
    record: the query, the ordered step descriptions with outcome markers, an answer excerpt of
    at most 200 characters, and `num_steps`; workflow reads exclude records with zero steps.
    → AC11
12. **R12 — Non-blocking entity extraction.** [C] After the user query and after the final
    answer, entities (PERSON/PLACE/SYSTEM, from at most the first 500 characters of text) are
    extracted via the LLM and written to entity memory; any extraction failure is swallowed —
    it must never fail the turn. → AC15
13. **R13 — Bounded agent loop.** [C] The loop runs at most 10 iterations; if no final answer
    is produced by then, the turn ends with a fixed inability message, which is still persisted
    per R1 (prevents CTX-B8). → AC12
14. **R14 — Search-and-store acquisition.** [C] Acquisition tools persist what they find to the
    knowledge base with source metadata (source, id, title, chunk index/count, timestamps) in
    the same call; deep ingestion chunks documents (default: recursive character splitting,
    chunk size 1,500, overlap 200 — the course's single ingest config) before storing. → AC16, AC19
15. **R15 — Configuration coherence.** [C] One distance strategy (cosine; §2) governs every vector
    store, write and read (the course wipes and rebuilds all tables between lessons specifically
    to guarantee this); [H] the distance strategy, toolbox k, and token budget are each defined
    in exactly one configuration point. → AC17
16. **R16 — Memory-aware model instructions.** [C] The system prompt names each context segment
    and its purpose, instructs the model to consult memory before tools, sets the conflict
    priority (current question > latest conversation > knowledge-base evidence > older
    summaries/workflows), requires expanding a summary before relying on detail that exists only
    there, and requires stating uncertainty instead of asserting unsupported claims. → AC13, AC20

## 5. Acceptance Criteria ★ (the oracle)

### Fixture corpus (define FIRST; authored for this spec — no course data copied)

| Fixture | Exact contents |
|---|---|
| `fixtures/kb/kestrel-notes.md` | Synthetic paper notes: *"Kestrel: Streaming Memory Consolidation for Long-Horizon Agents. Authors: R. Marlow, T. Iversen (2025). Id: KX-2025-011. Claim: tiered summary ledgers cut resumption errors by 41% on synthetic long-horizon tasks."* (+ ~2 paragraphs of filler you author). |
| `fixtures/kb/heron-notes.md` | Synthetic paper notes: *"Heron: Entity Graphs for Tool Routing. Author: F. Adeyemi (2024). Id: HX-2024-007. Claim: entity-conditioned routing halves tool-selection errors versus flat tool lists."* (+ filler). |
| `fixtures/conversation/seed-thread.json` | 12 authored messages (6 user / 6 assistant), thread `seed-01`, about researching Kestrel. First user message is exactly: `"Find the Kestrel paper about streaming memory consolidation."` Deliberately long enough to exercise consolidation (failure modes CTX-B1/B4/B5). |
| Fixture tool registry (9 tools) | 3 relevant: `paper_search` (returns fixture candidates JSON), `fetch_notes` (acquisition: reads a `fixtures/kb/*.md` file, chunks it, writes KB rows per R14, returns the full text — which exceeds 3,000 chars via the filler; failure modes CTX-B2/B6), `get_current_time`; 6 decoys with unrelated authored docstrings: `knit_pattern_helper`, `currency_convert`, `recipe_scaler`, `translate_phrase`, `calendar_lookup`, `sports_scores`. |
| `fixtures/tools/oversized-output.txt` | ≥4,000 characters of authored filler used by `fetch_notes` to guarantee the >3,000-char case (CTX-B6). |
| Scripted LLM client [H] | A deterministic stand-in honoring the D4 tool-calling interface, with canned per-test scripts (always-tool-call, canned summary, canned entities). Lets the oracle run without a key. Building agents MUST NOT modify fixtures to make a test pass (§6 Never). |

Modes: **Offline** (no network after the one-time embedding-model download), **Scripted**
(offline + scripted LLM client), **Live** (real network; `live-keyless` needs no key,
`live-keyed` needs `OPENAI_API_KEY`). Live ACs are excluded from the default offline run.

### Given / When / Then

| # | Mode | Given | When | Then |
|---|---|---|---|---|
| AC1 | Offline | Fixtures ingested and seed thread written by process 1 | A **new OS process** opens the same DB file and reads seed-thread conversation and queries the KB for "streaming memory consolidation" | All 12 seed messages return chronologically, and a `kestrel-notes` chunk is the top KB hit — memory survived restart (D5/D14 invariants; R1) |
| AC2 | Offline | Seed thread + 2 messages written to thread `other-01` | Reading conversational memory for `seed-01` with default limit | Only `seed-01` unconsolidated messages return, timestamp-ascending, each with role and timestamp; no `other-01` content (R3) |
| AC3 | Offline | Both fixture notes ingested | KB similarity query "entity graphs for routing tools", k=3 | A `heron-notes` chunk ranks first — the true nearest neighbor, exact at fixture scale — and carries its source-file metadata (R2; D7 invariant) |
| AC4 | Offline | All 9 fixture tools registered | Toolbox query "find research papers on agent memory" with k=5 | At most 5 schemas return, all valid `RetrievedToolSchema`, names unique, `paper_search` present (R4 invariant) |
| AC5 | Offline | `paper_search` already registered | It is registered again under the same name | The toolbox store holds exactly one row for `paper_search` (R5) |
| AC6 | Offline | A test budget of 1,000 tokens [H]; strings sized to 40% / 65% / 85% of it | Monitoring each | Statuses are `ok` / `warning` / `critical` respectively and each token estimate equals `len(chars)//4` (R6) |
| AC7 | Scripted | Assembled context >80% of the test budget containing a `## Conversation Memory` section and a `# Question` line | The pre-model budget check runs | Returned context has the conversation section replaced by the offload stub, a `[Summary ID: …]` reference under `## Summary Memory`, and the `# Question` text byte-identical (R7; D10 invariant) |
| AC8 | Scripted | Seed thread fully unconsolidated | Thread summarization runs, then immediately runs again | After run 1: every seed row carries the same new 8-char hex `summary_id`, unconsolidated count is 0, and the conversation read reports no unconsolidated messages; run 2 reports nothing to summarize (R3, R8, R9) |
| AC9 | Scripted | AC8's summary id | The expand operation runs on it | Output contains the stored summary text AND all 12 originals with timestamps, chronological, including the first user message `"Find the Kestrel paper about streaming memory consolidation."` verbatim (R9; D10 invariant) |
| AC10 | Scripted | `fetch_notes` returns >3,000 chars inside an agent turn | The loop executes the tool call | A tool-log record holds the FULL result, args, `status="success"`, preview ≤2,000 UTF-8 bytes; the tool message given to the model is ≤3,000 chars + a truncation notice naming the log id (R10; D12 invariant) |
| AC11 | Scripted | A scripted run making exactly 2 tool calls then answering; plus one zero-step workflow row written directly as a control | The turn completes; then workflow memory is queried for a similar task | One workflow record exists with the query, 2 ordered steps with outcome markers, answer excerpt ≤200 chars, `num_steps=2`; the query returns it and never returns the zero-step control (R11; D8 invariant) |
| AC12 | Scripted | A scripted model that always emits a tool call | `call_agent` runs a turn | The loop stops after exactly 10 iterations, `completed=false`, the final answer is the fixed inability message, and that answer is persisted to conversational memory (R13, R1) |
| AC13 | Scripted | Any query on a fresh thread | The turn's exact model input is captured | The user content begins `# Question` and contains all five segment headings in order (Conversation, Knowledge Base, Workflow, Entity, Summary); the system message names all five segments and states the R16 conflict-priority order (R2, R16; D9 invariant) |
| AC14 | Scripted | The seed transcript; scripted summary reply | Summarization runs | Output contains the four exact R8 headings; the id matches `^[0-9a-f]{8}$`; the label is 8–12 words and not in the generic-label reject set (R8) |
| AC15 | Scripted | Scripted extractor returns 2 entities for the fixture text; a second scripted run throws | Entity extraction runs after a turn | Run 1 writes 2 `EntityRecord`s and the entity read returns both as formatted bullets; run 2's exception leaves the turn's final answer unchanged (R12) |
| AC16 | Offline | `fetch_notes` acquisition tool | It executes on `kestrel-notes` | KB gains chunk rows with `source`, `chunk_id`, `num_chunks` metadata **within the tool call itself**, and chunk sizes respect the 1,500/200 chunking default (R14; D13 invariant) |
| AC17 | Offline | The running configuration | All five vector stores and the toolbox retriever are inspected | Every store reports the identical distance strategy (§2/R15) and the retrieval k resolves from a single config point (R4, R15) |
| AC18 | Scripted | A tool registered with augmentation on; scripted LLM returns enriched text + 5 queries | Registration completes | The stored description equals the enriched text (not the raw docstring) and the embedded text contains the 5 synthetic queries (R5; D11 invariant) |
| AC19 | Live-keyless | Network available | The arXiv candidate-search tool runs with query "agent memory" | A JSON array returns; every element has `arxiv_id`, `entry_id`, `title`, `authors`, `published`, `abstract` (abstract ≤2,500 chars) (R14; D15 invariant) |
| AC20 | Live-keyed | `OPENAI_API_KEY` set; fresh thread | Turns: "Find the MemGPT paper" → "Save the content of the paper" → "Summarize the conversation so far using your tool" → "What was my first question?" | Turn 2 resolves "the paper" from conversation memory without re-asking; turn 3 stores a summary and marks rows; turn 4's answer names the first question, having expanded the summary (R1, R2, R9, R16; D4 invariant — real native tool calling against the default provider) — the course's own end-to-end demonstration sequence (CTX-E, Lesson 6) |

Every business rule reaches ≥1 AC and every AC traces to a rule (mapping inline above). Every
demonstrated failure mode appears as rule + fixture + AC + CTX-B entry (§10 four-way encoding).

## 6. Boundaries

**Always**
- Persist every user query and final answer (R1) and write a tool-log record for every tool call (R10).
- Run the budget check before every model call (R6/R7); keep the `# Question` text intact through any offload.
- Use the same embedding model for every store and for both write and read paths (CTX-C5).
- Load secrets from the environment; keep the DB file out of version control.

**Ask First** (course-spoken trade-offs — anything here forces rework or was shown lateral-or-worse)
- **Changing the embedding model** — every vector store must be re-embedded; the course stresses the query-time model must match the ingest-time model (Lesson 2's RAG walkthrough).
- **Changing distance strategy or adding/altering a vector index after data exists** (see §2) — the course wipes and rebuilds all tables between lessons precisely to avoid inconsistent-strategy corruption.
- **Raising the toolbox retrieval count or passing all tools to the model** (R4) — Lesson 4 shows this degrades tool selection and bloats context; providers recommend ~10–20 tools max.
- **Rewriting the summarization prompt structure** (R8) — Lesson 5: summarization is lossy and "the prompting technique you use … will determine the quality of the output".
- **Switching the store realization** (D14) or **enabling Tavily web search** (D15) — migration/setup cost and a new secret respectively.

**Never**
- Invent citations, paper metadata, or provenance for content not present in memory.
- Assert factual claims unsupported by knowledge-base evidence without stating uncertainty (R16); answer when the system should abstain.
- Mutate fixtures (or the scripted LLM's scripts) to make a test pass.
- Commit secrets or hardcode credentials (the course notebooks hardcode local DB passwords — do not reproduce that).
- Re-summarize rows already marked with a `summary_id`, or bypass the tool log for any tool call.

## 7. Test Plan & Self-Verification

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # generate a lockfile; pins are this build's choice (§2)
cp .env.example .env                   # set OPENAI_API_KEY (required only for live-keyed)

pytest -q -m "not live"                # AC1–AC18: offline + scripted (first run downloads the embedding model)
pytest -q -m "live"                    # AC19 (keyless network), AC20 (needs OPENAI_API_KEY)
```

The building agent MUST report results **per acceptance criterion** (AC1…AC20) with cited
evidence: the test command run, the pass/fail output line, and file paths of artifacts examined
(e.g. the DB file inspected for AC1, the captured model input for AC13). "Should pass" /
"looks correct" are treated as failures — they mean it wasn't run. If a live AC cannot run
(no network / no key), report it as SKIPPED with the reason; never as passed.

## Course Context Pack (embedded — agent-readable)

Concepts only — no code from the course notebooks appears here or anywhere in this spec. The
concepts in CTX-A…CTX-C are durable; only the names in CTX-D are perishable.

### CTX-A. The pattern

**Memory-aware agent loop over an external memory core.** A stateless LLM becomes a persistent
agent by routing all durable state through a database (the *Agent Memory Core* — the component
that sees the most data traffic in the system) and by making the model *aware* of that memory:

`persist & preload memory → assemble partitioned context → guard the budget → retrieve focused tools → reason/act loop with logged tools → write back learning artifacts`

Stage by stage, each with the reason it exists:
1. **Typed memory stores behind one manager** — different memory types need different data
   models and retrieval strategies (exact-by-thread vs semantic similarity), so each gets its
   own store; a memory-manager abstraction unifies read/write so the agent code never touches
   storage details (D7).
2. **Deterministic preload** — the agent cannot choose to look up what it doesn't know exists
   (the chicken-and-egg problem), so context bootstrapping runs every turn by harness rule (D8).
3. **Partitioned context** — labeled, self-describing memory segments let the model use each
   store for its intended role instead of one undifferentiated blob (D9).
4. **Budget guard with recoverable reduction** — context windows are finite; consolidate
   conversation into summaries that keep an id-link back to the originals, expandable
   just-in-time (D10).
5. **Semantic tool retrieval** — tools are procedural memory: register many, retrieve few per
   query, so the system scales to hundreds of tools without degrading selection (R4, D11).
6. **Logged execution with bounded excerpts** — full tool outputs live in the database; the
   context window gets a pointer-bearing excerpt (D12).
7. **Write-back learning** — conversations, workflows (steps + outcome), entities, and search
   results persist after each turn, so the agent improves across sessions instead of restarting
   from scratch (D13).

### CTX-B. Failure-mode catalog

- **CTX-B1 — Stateless amnesia.** *Symptom:* mid-conversation, the agent asks the user to
  re-specify things already said ("book the first one" → "which list?"); nothing carries across
  sessions. *Cause:* no external persistence; each turn starts from a blank context. *Fix:*
  deterministic conversation persistence and preload every turn. *Enforced by R1, R2 / AC1, AC2,
  AC20.*
- **CTX-B2 — Tool overload.** *Symptom:* wrong or failed tool selection, ballooning latency and
  cost as the toolset grows. *Cause:* every tool definition stuffed into the context — confusion
  and bloat degrade selection. *Fix:* toolbox store + per-query semantic retrieval of a focused
  subset. *Enforced by R4, R5 / AC4, AC5, AC18.*
- **CTX-B3 — Context overflow.** *Symptom:* long threads crash into token limits or silently
  drop history. *Cause:* unbounded accumulation with no monitoring. *Fix:* estimate usage every
  turn; at ≥80% of budget, offload conversation to summary memory. *Enforced by R6, R7 / AC6,
  AC7.*
- **CTX-B4 — Unrecoverable (lossy) summarization.** *Symptom:* after compaction the agent can no
  longer answer detail questions ("what was my first question?"). *Cause:* summarization alone
  is lossy; originals were discarded. *Fix:* recoverable consolidation — mark source rows with
  the summary id and expand on demand. *Enforced by R9 / AC9, AC20.*
- **CTX-B5 — Re-summarizing processed messages.** *Symptom:* duplicate summaries, growing cost,
  drifting summaries of summaries. *Cause:* no marker distinguishing consolidated rows. *Fix:*
  set `summary_id` on exactly the consumed rows; reads and later summarizations exclude them.
  *Enforced by R3, R9 / AC8.*
- **CTX-B6 — Tool-output bloat.** *Symptom:* one verbose tool result crowds out the rest of the
  context. *Cause:* full payloads routed through the model. *Fix:* full output to the tool log;
  ≤3,000-char excerpt with a log-id pointer to the model. *Enforced by R10 / AC10.*
- **CTX-B7 — Blind memory (chicken-and-egg).** *Symptom:* the agent never consults memory it
  actually has. *Cause:* retrieval left to model discretion — you need memory to know which
  memory you need. *Fix:* deterministic preload of all segments every turn. *Enforced by R2 /
  AC13.*
- **CTX-B8 — Runaway loop.** *Symptom:* a turn never terminates or burns unlimited tool calls.
  *Cause:* no stop condition besides the model choosing to answer. *Fix:* hard iteration cap
  with a templated, persisted inability answer. *Enforced by R13 / AC12.*

### CTX-C. Decision background

Reference only — decisions are made in the Decision Ledger, not here.

- **CTX-C1 — Why typed stores (→ Ledger D7, D14).** The course's taxonomy: short-term memory
  (semantic cache, working memory/context window) vs long-term memory (procedural → workflow &
  toolbox; semantic → knowledge base, entity, summary; episodic → conversational, which is
  time-ordered and timestamp-addressable). Conversation and tool logs need exact, chronological,
  thread-keyed retrieval — a relational table, indexed on the thread key and on the timestamp so
  lookups and chronological ordering stay fast (the course creates both indexes explicitly); the
  other five need meaning-based retrieval — vector stores. The *memory manager* abstracts CRUD over all of them; the *memory unit* is the
  smallest atomic record (e.g. a conversational unit = timestamp + role + content). The
  database is called the memory core because it carries most of the system's data traffic.
- **CTX-C2 — Why the deterministic/agent-triggered split (→ Ledger D8).** Deterministic ops buy
  predictability, continuity, completeness, and lower model cognitive load ("don't let it forget
  to save"); agent-triggered ops buy relevance filtering, cost/latency control, and judgment
  ("should this be a durable preference? consolidate now?"). External tool calls are
  agent-triggered because only the model can judge whether extra information is worth the cost.
  The course's classification table and its final working loop disagree on two operations
  (entity writes, summary-index reads) — evidence carried in D8's default note.
- **CTX-C3 — Summarization vs compaction mechanics (→ Ledger D10).** Summarization compresses
  content through the LLM into a shorter representation preserving task-relevant facts,
  relationships, and removing redundancy — always lossy. Compaction moves content to the
  database under an id with a short description, letting the model pull it back when needed — 
  lossless but preloads nothing. The shipped pipeline pairs them: structured summary (four
  fixed headings: technical / emotional / entities / actions-decisions) in the window, full
  originals recoverable by id (JIT retrieval: fetch only what the current reasoning step needs,
  when it needs it). Working parameters, each from its single course config: input cap 6,000
  chars; summary generation capped at 4,000 completion tokens; label prompt capped at 2,000;
  one retry then deterministic fallback; 8-char summary ids; budget estimate `chars//4`;
  thresholds 50/80; budget 256,000 tokens (see D4's note for the model-name discrepancy).
- **CTX-C4 — Toolbox mechanics (→ Ledger D11; R4).** Tool retrieval is keyed on
  descriptions, not names: registration embeds name + description + signature (+ synthetic
  queries when augmented); a user query embeds to the same space; nearest tools win. Augmented
  registration has the LLM rewrite the docstring using the function source (summary, steps,
  when-to-call, caveats) and generate ~5 example queries — the course demonstrates the enriched
  text is far more separable than a one-line docstring. Model providers recommend exposing only
  ~10–20 tools; the course passes the top 3–5. The self-lookup tool (`read_toolbox` as a
  registered tool) lets the agent discover capabilities mid-execution when the initial toolset
  proves insufficient. Registration deduplicates by tool name against the store.
- **CTX-C5 — Embedding & consistency (→ §2, R15).** One local sentence-transformers
  model (768-dim) serves every store; the query-time model must match the ingest-time model or
  similarity is meaningless. The course re-creates all tables at each lesson start explicitly
  "to guarantee a clean starting state with consistent distance strategy" — the strongest
  in-course signal that mixed strategies corrupt retrieval. Distance config homes: cosine in the
  L2/L3 notebooks' store setup; Euclidean in the L4/L5 notebooks' store setup; the L2 notebook's
  markdown names Euclidean while its code passes cosine.
- **CTX-C6 — Index background (→ §2).** The course text teaches HNSW (graph-based
  nearest-neighbor traversal) and its lesson objectives name it, but the helper that actually
  creates indexes builds IVF (neighbor-partition organization, target accuracy 95) to dodge
  store-version bugs — a reminder that index choice is a store-realization detail, while the
  invariant is retrieval correctness. Indexes exist to avoid full scans; at fixture scale exact
  search is correct and simpler.
- **CTX-C7 — Acquisition & ingestion (→ Ledger D13, D15; R14).** The course's acquisition tools:
  a web search (default 5 results per call, each written with title/url/score/query/timestamp
  metadata), a candidate
  search returning structured JSON (id, title, authors, published, abstract capped at 2,500
  chars; retriever configured for up to 8 docs, 4,000 chars each), and deep ingest
  (PDF → text → chunks of 1,500 chars with 200 overlap → KB rows with chunk_id/num_chunks/
  timestamps). Chunking exists because embedding inputs are bounded — oversized inputs fail or
  truncate. Its bootstrap corpus streamed the first 100 records of a public arXiv dataset,
  concatenating title + subjects + abstract as the embedded text with the fields as metadata.
- **CTX-C8 — Loop & write-back parameters (→ Ledger D8, D12; R11–R13).** Max 10 iterations;
  tool results >3,000 chars truncated for the model with a log-id pointer; tool-log previews
  capped at 2,000 UTF-8 bytes; workflow records store the query, ordered outcome-marked steps,
  and an answer excerpt capped at 200 chars, and reads filter to `num_steps > 0`; entity
  extraction reads at most 500 chars of source text, classifies PERSON/PLACE/SYSTEM, is capped
  at 2,000 completion tokens, and is wrapped so failures never break the turn; conversation
  preload defaults to 10 messages — the agent loop uses that default, while one L4-notebook
  *verification* cell reads with limit 100 (a test read, not the loop's config); KB k=3,
  workflow k=3, entity k=5, summary index k=10 — each from its single course config (no
  competing configs exist for these). The course validated its consolidation pipeline on a
  seeded ~30-message thread; this spec's authored 12-message seed fixture plays that role.

### CTX-D. Perishable assumptions

Treat these as **search keywords against current documentation, not guaranteed imports**. The
concepts in CTX-A…CTX-C are durable; only these names are perishable. The course's installs
were entirely **unpinned** (no versions in its requirements file), so no course version pins
exist to reproduce.

- `langchain-oracledb` — `OracleVS`, `OracleVectorizerPreference` (hybrid search hook)
- `langchain_community.vectorstores.utils.DistanceStrategy` (`COSINE`, `EUCLIDEAN_DISTANCE`, `DOT_PRODUCT`)
- `langchain_huggingface` / `langchain_community.embeddings` — `HuggingFaceEmbeddings`
- `sentence-transformers/paraphrase-mpnet-base-v2` (embedding model name)
- `langchain_community.retrievers.ArxivRetriever`, `langchain_community.document_loaders.ArxivLoader`
- `langchain_text_splitters.RecursiveCharacterTextSplitter`
- `tavily` — `TavilyClient` (web search; keyed)
- `openai` — chat-completions API with `tools` / `tool_choice="auto"`; model names `gpt-5`, `gpt-5-mini`
- `oracledb`, Oracle AI Database `26ai`, DSN form `host:1521/FREEPDB1`, `datasets.load_dataset` streaming, dataset `nick007x/arxiv-papers`
- `pymupdf`, `arxiv` (PDF/metadata access)

### CTX-E. Provenance map

Lesson numbering below follows the **transcripts** (authoritative). The notebook files are named
L2–L5 and correspond to transcript Lessons 3–6 (off by one — the platform counts the
Introduction as Lesson 1); the notebook dump's own "Lesson Map" header mislabels this mapping —
where they disagree, the transcripts win. **Nothing in this spec requires platform access.**

- **Lesson 1 — Introduction:** course framing; memory engineering as first-class, external,
  persistent infrastructure → CTX-A preamble.
- **Lesson 2 — Why AI Agents Need Memory:** stateless-agent failure demo (CTX-B1); conversational
  memory and its limits; short/long-term memory taxonomy (CTX-C1); RAG-to-agent-memory bridge and
  same-embedding-model requirement (CTX-C5); the Agent Memory Core (CTX-C1, D14).
- **Lesson 3 — Constructing The Memory Manager** *(notebook file L2)*: agent stack and memory
  layer; memory manager and memory units (CTX-C1); deterministic vs agent-triggered
  classification (CTX-C2, D8); context engineering and the memory lifecycle; store creation, SQL
  vs vector argument (D7), index creation (CTX-C6); dataset bootstrap ingest (CTX-C7).
- **Lesson 4 — Scaling Agent Tool Use with Semantic Tool Memory** *(notebook file L3)*: the
  toolbox pattern and its failure argument (CTX-B2, R4); memory-unit augmentation (CTX-C4,
  D11); search-and-store with web search (D13, D15); arXiv candidate search and deep ingest
  incl. chunking config (CTX-C7).
- **Lesson 5 — Memory Operations: Extraction, Consolidation, and Self-Updating Memory**
  *(notebook file L4)*: summarization vs compaction trade-off (CTX-C3, D10); workflow memory
  rationale (R11); budget monitoring thresholds and the summarize/mark/expand pipeline
  (CTX-B3/B4/B5, R6–R9).
- **Lesson 6 — Memory Aware Agent** *(notebook file L5)*: the agent loop and harness; memory
  operations in/out of the loop (D8); partitioned context and memory-aware system prompt (D9,
  R16); tool-log context offloading (D12, CTX-B6); iteration cap (CTX-B8); the end-to-end
  MemGPT-paper demonstration sequence reused as AC20.
- **Lesson 7 — Conclusion:** recap of memory modeling, semantic retrieval, extraction,
  consolidation, write-back.

## Final deliverable note to the build agent

When the build is complete and the acceptance criteria have been reported per §7, conclude your
build conversation with an infra/structure diagram of the app you built (stores, harness, loop,
and tool flows), and end with the exact phrase:

**"This is the infra/structure diagram of this app"**

---

*Spec v1 · Course: Agent Memory: Building Memory-Aware Agents · Learner project: `[project]`
(default: memory-aware research assistant, D1) · Living document: when the building agent
produces something unexpected, add the missing constraint here (rule + AC + fixture as needed)
and re-run.*
