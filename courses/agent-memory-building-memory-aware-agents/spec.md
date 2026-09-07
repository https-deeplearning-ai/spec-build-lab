# Spec: Memory-Aware Research Assistant — Standalone Takeaway

> **This file is self-contained.** The embedded Course Context Pack (CTX-A…CTX-E, at the end)
> replaces all external course references — nothing in this spec requires access to the course
> platform, notebooks, or transcripts. `(CTX-X)` anchors mark course-derived knowledge. The
> **Decision Ledger** below holds every point where the build could diverge, each pinned to one
> course-derived default, so the spec builds as-is with zero intake.
>
> **Provenance:** generated from the *Agent Memory: Building Memory-Aware Agents* course
> (DeepLearning.AI × Oracle) notebook dump + lesson transcripts on 2026-09-06.
> Spec-generation guide version: repo commit `73c37ef`.
>
> Citation convention: notebooks are cited by file + cell (e.g. "L2.ipynb cell 16"); lessons are
> cited by **transcript numbering** (Lessons 1–7), which is authoritative — the notebook filenames
> and the dump's own lesson-map header are shifted relative to it (see CTX-E).

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
when you have reason to prefer another option. Unfilled rows do NOT block handoff — the defaults
ARE the build target. Owner is metadata only; it never changes how a row is surfaced.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|----------|----------|----------------------------------------------------------------------------------|--------------------------|---------|-----------|-------|
| 1 | learner | `[project]` — what you're building | — | A memory-aware research-assistant CLI, re-expressing the shape of the course's own example (the "ArxivScout" agentic research assistant that investigates topics over multiple sessions — L2.ipynb cells 2 & 28), instantiated on the §5 synthetic fixture corpus. **This is the course's example realization**, expected to be swapped when your project differs — the invariants, not the example, must survive. Resolution: §3 project precedence branch 1 (the materials afford a clear concrete example; its shape is kept, all facts re-authored). | Course example shape (default); any project needing multi-session, long-horizon agent memory | A new domain means re-authoring seed data, fixture tools, and goal; the pattern (typed stores + memory-aware loop, CTX-A) transfers unchanged | learner |
| 2 | learner | `[data / inputs]` — what it operates on | — | The §5 synthetic fixture corpus (authored paper records + scripted conversation threads). **The course's example data realization** — streaming the first 100 records of the `nick007x/arxiv-papers` HuggingFace dataset (L2.ipynb cells 29–31) — is expected to be swapped for your corpus. | Fixture corpus (default); live arXiv ingestion via the fetch tool (row 12 invariant applies); your own documents | Real data means re-running ingestion; chunking and embedding body defaults may need re-tuning (Ask First AF3) | learner |
| 3 | learner | `[goal]` — what "working" means | — | Passing the §5 acceptance criteria: multi-session continuity, retrieval that finds ingested facts semantically, recoverable consolidation, bounded tool context | §5 ACs as-is (default); learner-defined success criteria | A different goal means rewriting the §5 ACs *before* building, preserving the §10-style four-way encoding of each failure mode | learner |
| 4 | learner | `[model / provider]` | MUST support native tool calling: structured tool-call outputs and tool-result turns (the agent loop protocol in L5.ipynb cell 20 depends on it) | OpenAI `gpt-5-mini` for every LLM role (agent loop, summarization, docstring augmentation, entity extraction). Course-contradicted note (fails the §5.5 stakes test → stays here as the row's value note): the notebooks' agent-facing calls use `gpt-5-mini` (L4.ipynb cells 24/26, L5.ipynb cell 18) while `helper.py` utilities use `gpt-5` (Toolbox default, entity extraction, helper token map); this spec pins one model everywhere, taking the end-to-end app's value. Model names are perishable (CTX-D). | `gpt-5-mini` (course default — app config); `gpt-5` (course default — helper config); any chat model with native tool calling | Swapping provider means porting the tool-call message protocol and re-checking the token-limit config; the memory layer is unaffected | course+learner |
| 5 | learner | `[environment]` — where it runs | ALL memory contents MUST survive process restarts — cross-session continuity is the pattern's founding requirement (Lessons 2 and 6) | Local single-machine Python CLI; the persistent store is one local file (row 11); secrets loaded from `.env` (the course's `load_env` pattern); `OPENAI_API_KEY` is required only for ACs marked `live` | Local file (default); containerized client-server DB (the course ran Oracle in Docker); cloud deployment | A server DB adds setup/credential cost and buys concurrent access; a local file is single-writer but zero-setup | course+learner |
| 6 | learner | `[out of scope]` — explicitly unwanted | — | Nothing beyond the §1 Not Included list | Add your own exclusions at build time | Every unlisted exclusion is a feature the build agent may plausibly invent | learner |
| 7 | design-structural | Memory-store topology | Memory MUST be partitioned by type, each type's store using a retrieval mode matched to its access pattern: exact, thread-scoped, time-ordered access for conversational history and tool logs; semantic-similarity retrieval with metadata filtering for the other types (L2.ipynb cell 9 table; Lesson 3) | All seven course stores: **Conversational** and **Tool Log** (exact/relational) plus **Knowledge Base**, **Workflow**, **Toolbox**, **Entity**, **Summary** (vector) — L2.ipynb cells 10–17 | Seven stores (course default); a reduced set that drops Entity and/or Workflow (invariant still holds) | Fewer stores means less write-back learning — no reusable trajectories, no entity continuity (Lesson 6 demo shows both paying off). A single merged store violates the invariant and is not an option | course |
| 8 | design-argued | Deterministic vs agent-triggered operation split | Every memory operation MUST be explicitly classified as deterministic (harness-executed) or agent-triggered (a tool the model may call); context-assembly reads and conversation/tool-log persistence MUST be deterministic; summarization and summary expansion MUST also be agent-callable | The end-to-end app's split (L5.ipynb cell 20): **deterministic** — the five context reads at loop start, write conversational memory (user query + final answer), write workflow, write entity (on query and final answer), write tool log per call, and the >80% offload trigger; **agent-triggered tools** — `read_toolbox`, `expand_summary`, `summarize_and_store`, external search/fetch tools, `get_current_time`. Course-contradicted note (both sides cited, CTX-C3): the L2.ipynb cell 20 classification table marks `write_entity` and `read_summary_context` agent-triggered-only, while the L5.ipynb app executes both deterministically — the app config is this default's source. | Course split (default); shift more operations to agent discretion; fully deterministic (no memory tools) | Argued aloud in Lessons 3 and 6: deterministic buys predictability, completeness, and debuggability ("you need memory to know which memory you need" — L2.ipynb cell 21); agent-triggered buys relevance, cost control, and signal-to-noise. Reclassifying an operation silently changes a behavior guarantee → Ask First AF4 | course |
| 9 | design-argued | Tool-description augmentation | The toolbox retrieval key MUST be an embedded textual description of each tool — docstring-as-retrieval-key (L3.ipynb cell 2) | Selective per-tool augmentation matching the course's flags: LLM-augmented descriptions (`augment=True`) for the web/fetch/summary tools; plain docstring (`augment=False`) for `arxiv_search_candidates`. When augmenting, the embedded text combines name + augmented description + signature + 5 synthetic example queries (helper `register_tool`). Course-contradicted note: `get_current_time` is registered `augment=True` in L3.ipynb cell 33 but `augment=False` in helper `register_common_tools` (the config the L5 app runs) — default False, per the app config. | Selective (course default); augment every tool; augment none | Argued aloud in Lesson 4: augmentation buys embedding-space separability and retrieval recall, at the cost of LLM calls at registration time (and requires a live model then). Changing which tools are augmented silently changes retrieval quality → Ask First AF6 | course |
| 10 | design-argued | Context-reduction strategy | Context reduction MUST be recoverable: after any consolidation, the original units remain retrievable on demand — "compaction and recoverability stay paired" (L4.ipynb cell 31) | The course's combined pipeline: LLM summarization into the four-heading structured summary **plus** `summary_id` marking of exactly the consumed conversation rows **plus** just-in-time recovery via `expand_summary` (L4.ipynb Part 2; helper) | Combined (course default); pure compaction — offload with ID + description only, no LLM summary (shown working in Lesson 5) | Argued aloud in Lesson 5: "summarization is always a lossy technique"; compaction offloads context to the database and lets the model pull detail back when needed. Pure summarization *without* a back-link is the warned lossy side — it violates this row's invariant and is not an option (CTX-B7). The combined default costs LLM tokens per consolidation | course |
| 11 | realization | Persistent store (the "memory core") | One persistent store layer MUST provide **(a)** exact relational access — thread-scoped filtering, timestamp ordering, and in-place update of a `summary_id` marker — for conversational + tool-log memory, and **(b)** vector-similarity retrieval with metadata filtering for the five vector memory types; all contents survive process restarts (rows 5, 7) | **SQLite via Python's stdlib `sqlite3`, one local database file**, with each vector memory's embeddings stored per row and similarity computed exactly in-process over the stored vectors. Resolution: §3 dependency precedence **branch 1** (substitution) — the course's realization, Oracle AI Database 26ai in Docker with admin credentials (L2.ipynb cell 6; Lesson 3), is heavy (container-level setup + credentials), and the course teaches the memory-engineering *pattern*, which the product realizes. "Lightest" by tier: **tier 1** — `sqlite3` ships with the standard Python distribution, and exact brute-force similarity meets the retrieval contract at this spec's declared default scale (the fixture corpus, tens of rows); no ANN index is required at that scale, so no step up to tier 2 (embedded vector library) or tier 3 (served component). Scaling realizations live in Options. | Oracle AI Database 26ai + LangChain OracleVS with IVF vector indexes **(course default)**; SQLite + an embedded vector-search extension (tier 2 — when a corpus outgrows brute force); PostgreSQL + pgvector (tier 3) | The course store buys ANN indexing (the course built IVF indexes; HNSW is also named — see the §4 index note), hybrid search, and one engine at production scale — at setup + credential cost. Any store swap after data exists forces re-ingestion and re-embedding → Ask First AF7 | course+learner |
| 12 | realization | Web-search tool (Tavily) | Any tool that fetches external content MUST follow the search-and-store pattern: persist its results to the knowledge base with source metadata (title, url-or-id, originating query, timestamp) so later turns retrieve instead of re-fetching (L3.ipynb cell 28) | **Omitted by default.** Resolution: §3 keyed-tool rule — Tavily requires an API key (heavy), and its taught behavior (external results persisted to the knowledge base) is fully carried by the keyless course tools `fetch_and_save_paper_to_kb_db` and `arxiv_search_candidates`, so the deterministic default is omission; no local stand-in is needed | Tavily `search_tavily` with search-and-store, `max_results=5`, result metadata per L3.ipynb cell 29 **(course default)**; an honestly-labeled fake web-search stand-in returning canned fixture results (a fake standing in for the real service — it must say so in its own registered description); omit (default) | Enabling Tavily buys open-web reach beyond arXiv, at key + per-call cost; enabling it is an Ask-First change (AF8) | course+learner |

---

## 1. Objective

Build a persistent, memory-aware research-assistant agent that remembers conversations, learned
facts, entities, tool trajectories, and summaries across sessions in typed memory stores, and
assembles a partitioned, budget-monitored context window plus a semantically-retrieved toolset for
every turn — so the agent completes multi-session, long-horizon tasks instead of resetting to
stateless behavior. (pattern: CTX-A) Project target: `[project]` (Ledger row 1 default).

### Not Included ★

Learner exclusions: `[out of scope]` (Ledger row 6 — default: none). Beyond course scope, do NOT build:

- **Web search via Tavily** — omitted by default (Ledger row 12).
- **Hybrid / lexical / graph-traversal retrieval** — the course names these strategies (Lesson 3)
  and provisions a hybrid-search hook (`setup_hybrid_search`, L2.ipynb cell 15) but never exercises
  hybrid retrieval in the running system. Vector similarity + metadata filtering only.
- **Reranking models** — mentioned only inside the Lesson 2 RAG overview, never built.
- **Semantic cache and working-memory scratchpads** — named as short-term memory forms (Lesson 2)
  but not implemented; the context window itself is the only working memory here.
- **Memory decay, strengthening, merging, or forgetting policies** — posed as judgment questions
  (L2.ipynb cell 22), not implemented by the course.
- **Bulk dataset seeding** — the course's 100-record HuggingFace `arxiv-papers` ingestion is demo
  seeding; the fixture corpus replaces it (Ledger row 2).
- **Oracle-specific operations** — tablespace/user administration, IVF/HNSW index tuning,
  vector-memory-pool management (all specific to the course's store realization; CTX-D).
- **Multi-user auth, concurrent writers, any UI beyond a CLI, deployment/hosting.**
- **Embedding-model fine-tuning and model versioning pipelines** — named as adjacent disciplines
  of memory engineering (Lesson 3), not built.

---

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python 3.12 | **This build's pin.** Honest era note: the course's `requirements.txt` pins nothing — every install is unversioned and even its "note which revision of python" placeholder is unfilled. Do not invent course pins; treat all course-era package and class names as search keywords → CTX-D. |
| Persistent store | SQLite (stdlib `sqlite3`), one DB file | Decided in Ledger row 11 — learners change it there, not here. |
| Embedding model | `sentence-transformers/paraphrase-mpnet-base-v2` (768-dim, local, keyless) | Course value, used identically in every lesson (L2.ipynb cell 8). First run downloads the model (keyless network); after that, fully offline. Changing it after ingestion → Ask First AF2. |
| Similarity metric | Cosine, all vector memories | Body default — see the §4 pinned-parameters table for the contradiction note and lever citation. |
| LLM | OpenAI `gpt-5-mini` | Decided in Ledger row 4. |
| LLM SDK | `openai` (chat-completions tool-calling protocol) | Era-specific API surface → CTX-D. |
| arXiv access (live tools) | `arxiv` + `pymupdf` | The course reached arXiv through LangChain community wrappers (`ArxivRetriever`, `ArxivLoader`, `RecursiveCharacterTextSplitter`) — perishable names, CTX-D; the behavior contract is R16. |
| Config & secrets | `python-dotenv`, `.env` | Secrets live in `.env` / environment only — never in source, never committed. The course notebooks inline a database password (L2.ipynb cell 6); that is a lesson-sandbox artifact — do **not** reproduce it. |
| Tests | `pytest` | Offline suite runs with no key; `live`-marked tests need `OPENAI_API_KEY` (+ network for arXiv). |

---

## 3. Input/Output Contracts ★

Schemas, not prose. These are the persistent record shapes and the per-turn result. Every
structure declared here must exist on fresh initialization (AC1).

```json
{
  "$id": "spec:conversational-unit",
  "type": "object",
  "required": ["id", "thread_id", "role", "content", "timestamp"],
  "properties": {
    "id": {"type": "string", "minLength": 1},
    "thread_id": {"type": "string", "minLength": 1},
    "role": {"enum": ["user", "assistant"]},
    "content": {"type": "string", "minLength": 1},
    "timestamp": {"type": "string", "format": "date-time"},
    "metadata": {"type": "object"},
    "created_at": {"type": "string", "format": "date-time"},
    "summary_id": {"type": ["string", "null"], "default": null}
  }
}
```

```json
{
  "$id": "spec:tool-log-record",
  "type": "object",
  "required": ["id", "thread_id", "tool_name", "result", "status", "timestamp"],
  "properties": {
    "id": {"type": "string", "minLength": 1},
    "thread_id": {"type": "string", "minLength": 1},
    "tool_call_id": {"type": ["string", "null"]},
    "tool_name": {"type": "string", "minLength": 1},
    "tool_args": {"type": "string", "description": "JSON-serialized arguments"},
    "result": {"type": "string", "description": "FULL result, never truncated here"},
    "result_preview": {"type": "string", "maxLength": 2000},
    "status": {"enum": ["success", "failed"]},
    "error_message": {"type": ["string", "null"]},
    "metadata": {"type": "object"},
    "timestamp": {"type": "string", "format": "date-time"}
  },
  "if": {"properties": {"status": {"const": "failed"}}},
  "then": {"properties": {"error_message": {"type": "string", "minLength": 1}}}
}
```

```json
{
  "$id": "spec:summary-record",
  "type": "object",
  "required": ["id", "description", "summary", "full_content"],
  "properties": {
    "id": {"type": "string", "pattern": "^[0-9a-f]{8}$"},
    "description": {
      "type": "string", "minLength": 1,
      "not": {"enum": ["Conversation summary", "Summary", "Chat summary", "Thread summary"]}
    },
    "summary": {
      "type": "string",
      "allOf": [
        {"pattern": "### Technical Information"},
        {"pattern": "### Emotional Context"},
        {"pattern": "### Entities & References"},
        {"pattern": "### Action Items & Decisions"}
      ]
    },
    "full_content": {"type": "string", "minLength": 1},
    "thread_id": {"type": "string"}
  }
}
```

```json
{
  "$id": "spec:retrieved-tool",
  "type": "object",
  "required": ["type", "function"],
  "properties": {
    "type": {"const": "function"},
    "function": {
      "type": "object",
      "required": ["name", "description", "parameters"],
      "properties": {
        "name": {"type": "string", "minLength": 1},
        "description": {"type": "string"},
        "parameters": {
          "type": "object",
          "required": ["type", "properties", "required"],
          "properties": {
            "type": {"const": "object"},
            "properties": {"type": "object"},
            "required": {"type": "array", "items": {"type": "string"},
                         "description": "exactly the parameters with no default value"}
          }
        }
      }
    }
  }
}
```

```json
{
  "$id": "spec:context-usage-report",
  "type": "object",
  "required": ["tokens", "max", "percent", "status"],
  "properties": {
    "tokens": {"type": "integer", "minimum": 0},
    "max": {"type": "integer", "minimum": 1},
    "percent": {"type": "number", "minimum": 0},
    "status": {"enum": ["ok", "warning", "critical"]}
  },
  "allOf": [
    {"if": {"properties": {"percent": {"exclusiveMaximum": 50}}},
     "then": {"properties": {"status": {"const": "ok"}}}},
    {"if": {"properties": {"percent": {"minimum": 50, "exclusiveMaximum": 80}}},
     "then": {"properties": {"status": {"const": "warning"}}}},
    {"if": {"properties": {"percent": {"minimum": 80}}},
     "then": {"properties": {"status": {"const": "critical"}}}}
  ]
}
```

```json
{
  "$id": "spec:agent-turn-result",
  "type": "object",
  "required": ["thread_id", "final_answer", "steps", "workflow_written"],
  "properties": {
    "thread_id": {"type": "string", "minLength": 1},
    "final_answer": {"type": "string", "minLength": 1},
    "steps": {"type": "array", "items": {"type": "string"}},
    "workflow_written": {"type": "boolean"},
    "summaries_created": {"type": "array",
      "items": {"type": "object", "required": ["id", "description"]}},
    "context_usage": {"$ref": "spec:context-usage-report"}
  },
  "allOf": [
    {"if": {"properties": {"steps": {"minItems": 1}}},
     "then": {"properties": {"workflow_written": {"const": true}}}},
    {"if": {"properties": {"steps": {"maxItems": 0}}},
     "then": {"properties": {"workflow_written": {"const": false}}}}
  ]
}
```

Assembled-context shape (structural contract, verified by AC3/AC4): the string handed to the LLM
is `# Question\n<query>` followed by exactly these markdown segments in this order —
`## Conversation Memory`, `## Knowledge Base Memory`, `## Workflow Memory`, `## Entity Memory`,
`## Summary Memory` — each carrying a "What this memory is" and a "How you should leverage it"
instruction block before its retrieved content (L5.ipynb cells 18–20; Lesson 6).

---

## 4. Business Rules

Each rule: behavior + the failure it prevents (CTX-B anchor) + tested-by. Label:
**[C]** course-demonstrated, **[H]** project hardening.

1. **[C] Cross-session persistence.** Everything written to any memory store in one process run
   is readable, unchanged and correctly ordered, from a new process opened against the same store
   file (CTX-B1 — stateless reset). → AC2, AC21
2. **[C] Deterministic context assembly.** Every agent turn begins with harness-executed reads —
   never left to model discretion: conversational memory (thread-scoped, unsummarized only,
   timestamp-ascending, limit 10), knowledge base (semantic, k=3), workflow (k=3, only workflows
   with ≥1 step), entity (k=5), and summary context (thread-scoped IDs + descriptions, k=10)
   (CTX-B2 — the chicken-and-egg retrieval problem). Read k/limit values: §4 parameter table. → AC3, AC22
3. **[C] Partitioned, memory-aware context.** The assembled context follows the §3 structural
   contract, and the system prompt names each segment, its purpose, and the conflict priority:
   current question > latest conversation memory > knowledge-base evidence > older
   summaries/workflows (L5.ipynb cell 18). → AC4
4. **[C] Deterministic persistence.** The user query and the final assistant answer are always
   written to conversational memory with thread_id and timestamp; every tool execution is always
   written to the tool log with args, FULL result, status, and error message on failure —
   selective saving is forbidden (CTX-B3 — selective-save gaps). → AC5, AC6
5. **[C] Semantic tool retrieval.** Tools live in the toolbox store with embedded descriptions;
   each turn the LLM receives only the top-k (k=5, agent-loop config) semantically relevant tool
   schemas, deduplicated by name, in the §3 retrieved-tool format — never the full registry
   (CTX-B4 — context bloat and tool-selection degradation). → AC7
6. **[C] Idempotent tool registration.** Registering a tool whose name already exists in the
   toolbox store must not write a duplicate row; the callable is still (re)bound and invocable
   (CTX-B5 — duplicate tool rows). → AC8
7. **[C] Context monitoring with automatic offload.** Before each LLM call the harness computes
   estimated usage (length ÷ 4 chars/token against the configured model limit); usage above 80%
   deterministically triggers recoverable consolidation of the conversational segment before
   reasoning; the current `# Question` text is never summarized away (CTX-B6 — context overflow).
   The model token limit is injectable configuration (course shape: a model→limit map). → AC9
8. **[C] Recoverable consolidation.** Summarizing a thread must (a) produce a structured summary
   under exactly the four headings *Technical Information / Emotional Context / Entities &
   References / Action Items & Decisions*, (b) store it as a §3 summary record with a short unique
   id, a specific (non-generic) description, and the thread_id, and (c) mark exactly the source
   conversation rows it consumed with that summary_id (CTX-B7 — lossy summarization). → AC10
9. **[C] No re-summarization.** Conversational reads and subsequent summarizations operate only on
   rows with no summary_id; summarizing a fully-summarized thread is a no-op that reports
   nothing-to-summarize and writes nothing (CTX-B8 — re-processing churn). → AC11
10. **[C] Just-in-time expansion.** Given a summary_id, the system returns the stored summary text
    plus ALL original messages marked with that id, chronological with timestamps — consolidation
    is always reversible (CTX-B7). → AC12
11. **[C] Tool-output bounding.** A tool result longer than 3,000 characters reaches the LLM
    truncated at 3,000 characters with an explicit pointer naming the tool-log record id holding
    the full output; the tool-log copy is never truncated (CTX-B9 — tool-output bloat). → AC13
12. **[C] Loop termination.** The agent loop runs at most max_iterations (default 10); exhausting
    them ends the turn with the templated "unable to complete the request within the allowed
    iterations" answer — never a hang, crash, or fabricated success (CTX-B10 — runaway loop). → AC14
13. **[C] Summarization robustness.** An empty LLM summary triggers exactly one retry with a
    simpler prompt; a second empty result falls back to a deterministic template that still
    carries all four headings — the pipeline never crashes or stores an empty summary
    (CTX-B11 — empty-output failure). → AC15
14. **[C] Learning write-back.** After any turn that executed tools, the query, the ordered step
    list, and the outcome are written to workflow memory (answer excerpt capped at 200 chars,
    metadata: query, success, num_steps, timestamp); workflow retrieval excludes zero-step
    records. Entities are extracted (LLM, from the first 500 chars) from the user query and the
    final answer and stored as name/type/description records; an entity-extraction failure must
    never fail the turn. → AC16, AC17
15. **[C] Store consistency.** All five vector memories use the same embedding model and the same
    similarity metric, for writes and reads alike — the course drops and rebuilds all stores per
    lesson precisely to guarantee "consistent distance strategy" (L3.ipynb cell 15 note). → AC18
16. **[C] Search-and-store.** External-content tools persist what they fetch to the knowledge
    base — the arXiv fetch tool chunks full paper text (size 1500, overlap 200) and stores each
    chunk with metadata (source, arxiv_id, title, entry_id, published, authors, chunk_id,
    num_chunks, ingestion timestamp) so subsequent queries retrieve without re-fetching
    (CTX-B12 — repeated discovery work). → AC19
17. **[C] Grounded honesty.** When a memory segment has no relevant content, its read returns an
    explicit no-content marker (e.g. "(No relevant knowledge base passages found.)"), never
    invented content; segment instructions direct the model to state what is missing rather than
    guess, and to ground factual claims in the knowledge-base segment. → AC20

### Pinned working parameters (body defaults — not Ledger rows; each is single-home here)

Every value cites its exact source config; contradicted values carry both sides and their
§5.5 lever-branch resolution. Items marked **post-build lever** are changed only via Ask First.

| Parameter | Default | Source & notes |
|---|---|---|
| Similarity metric | cosine (all stores) | **Course-contradicted, fails the stakes test → body default.** COSINE in L2.ipynb cell 16 and L3.ipynb cell 20; EUCLIDEAN_DISTANCE in L4.ipynb cell 19 and L5.ipynb cell 12; L2.ipynb markdown cell 3 names EUCLIDEAN while its own code runs COSINE. Resolved by lever-value **branch 1**: the Lesson 3 transcript narration states the value aloud ("the distance_strategy, which in this case is going to be cosine") in the lesson that introduces the stores. **Post-build lever** (consistency invariant is R15; late change = AF2/AF7 territory). CTX-C4. |
| Vector index | none at default scale (exact in-process search) | Ledger row 11 tier reasoning. Course context: L2.ipynb markdown (cells 2–3) names **HNSW**, while the code the course actually ran creates **IVF** ("ORGANIZATION NEIGHBOR PARTITIONS … TARGET ACCURACY 95", helper `safe_create_index`, which documents IVF as the workaround for Oracle Free errors). Contradiction fails the stakes test at the default scale → recorded here + CTX-C5; relevant only if you choose an ANN-indexed store in row 11. |
| Agent-loop tool retrieval k | 5 | L5.ipynb cell 20 app config (lever **branch 2** — narration names no value). Contradicted near-equivalent: the `read_toolbox` tool's docstring says "default: 5" while its signature defaults to 3 (L3.ipynb cell 25; helper `read_toolbox` k=3). **Post-build lever.** |
| Context reads | conversational limit 10; KB k=3; workflow k=3 (filter num_steps>0); entity k=5; summary context k=10 | Helper `MemoryManager` defaults, as invoked by L5.ipynb cell 20. (L4.ipynb's test cell 46 reads with limit=100 — exploratory config, not the app default.) |
| Token estimate | chars ÷ 4 | Lesson 5 narration states it aloud ("four characters per token") — branch 1; L4.ipynb cell 26. |
| Model token limit | 256,000 for the default model; 128,000 fallback for unknown models | Value 256000 stated aloud in Lesson 5 narration (branch 1). Map-key contradiction: `{"gpt-5-mini": 256000}` in L4.ipynb cell 24 vs `{"gpt-5": 256000}` in helper — moot under the row-4 single-model pin. Injectable config (R7). |
| Usage thresholds | <50% ok, 50–79% warning, ≥80% critical; offload trigger >80% | L4.ipynb cell 40; L5.ipynb cell 20. |
| Summarization | input capped at 6,000 chars; completion cap 4,000 tokens; description label 8–12 words with generic-label rejection + deterministic fallback label; summary id = 8 hex chars | helper `summarise_context_window`. |
| Tool-output bounds | 3,000-char LLM truncation; 2,000-unit tool-log preview (course truncated by UTF-8 bytes) | L5.ipynb cell 20; helper `write_tool_log`. |
| Agent loop | max_iterations 10 | L5.ipynb cell 20. |
| Entity extraction | input capped at 500 chars; completion cap 2,000 tokens; types PERSON/PLACE/SYSTEM; silent-empty on failure | helper `extract_entities`. |
| Chunking (fetch tool) | chunk_size 1500, chunk_overlap 200 | L3.ipynb cell 39 defaults (= helper). **Post-build lever** (AF3). |
| Docstring augmentation | 5 synthetic queries per augmented tool; augmentation + description completions capped at 2,000 tokens | helper `Toolbox`. |
| arXiv candidates | retriever load_max_docs 8, doc chars 4,000, full documents off; candidates k=5, abstract capped 2,500 chars | L3.ipynb cells 35–37 (= helper). |
| Embedding dimension | 768 | L2.ipynb markdown cell 3 (property of the pinned model). |

---

## 5. Acceptance Criteria ★ (the oracle)

### Fixture corpus (defined first — all facts authored for this spec; no course or real-world data copied)

The build ships these files under `fixtures/`. The building agent MUST NOT modify fixtures to make
a test pass. Facts below are the exact assertable content:

- `fixtures/papers/paper-001.json` — title *"Cadence Windows: Sliding Attention for Tidal
  Forecasting"*, authors *"R. Onda, M. Veles"*, subjects `cs.LG`, abstract stating: *"Cadence
  Windows reaches 87.5% accuracy on the TIDEBENCH-9 benchmark."*
- `fixtures/papers/paper-002.json` — title *"Ledger Distillation for Long-Horizon Planning
  Agents"*, author *"K. Aurelio"*, abstract stating: *"introduces the PLANMARK evaluation suite
  of 40 multi-day planning tasks."*
- `fixtures/papers/paper-003.json` — title *"Glass Harbor: Memory Consolidation in Dialogue
  Systems"*, author *"Dr. Ilsa Brandt"*, abstract stating: *"consolidation reduced context tokens
  by 62% with no loss on the recall probes."*
- `fixtures/papers/paper-004.json` — title *"Toolbox Embeddings at Scale"*, author *"P. Nwosu"*,
  abstract stating: *"evaluates tool-selection accuracy for registries of 10 to 200 tools."*
- `fixtures/papers/paper-005.json` — title *"Quiet Harbors: Entity Tracking Across Sessions"*,
  author *"Dr. Ilsa Brandt"* (recurring entity), abstract stating: *"tracks 312 named entities
  over 14 simulated sessions."*
- `fixtures/papers/paper-006.json` — title *"The Lantern Protocol for Session Persistence"*,
  author *"S. Farrow"*, abstract stating: *"agents resumed 94% of long-horizon tasks after a full
  process restart."*
- `fixtures/conversations/thread-research.json` — a scripted 12-message user/assistant thread
  planning a literature review. Planted content (one instance per consolidation-related failure
  mode): technical facts (names *Glass Harbor* and its 62% figure), an entity (*Dr. Ilsa Brandt,
  ibrandt@harborlab.example*), emotional context (user says they are *"nervous about contacting
  senior researchers"*), action items (*"draft the outline by Friday"*), and message 1 is the
  user question *"Which paper introduced the Lantern Protocol?"* (the "first question" probe).
- `fixtures/conversations/thread-short.json` — 4 messages: user asks for paper suggestions,
  assistant lists paper-001 then paper-006 by title, user says *"save the second one from that
  list"* — a pronoun/coreference follow-up (the stateless-agent failure instance, CTX-B1).
- `fixtures/workflows/workflow-empty.json` — a workflow record with `num_steps: 0` (the planted
  zero-step instance for the R14 filter).
- **Fixture tools** (registered by the test suite; defined by behavior, not code):
  `lookup_fixture_paper(paper_id)` returns the matching fixture paper record;
  `bulk_fixture_dump()` returns a >3,500-character concatenation of fixture abstracts (the
  planted oversized-output instance, CTX-B9); plus the course utility `get_current_time(detailed)`.
  Registering `lookup_fixture_paper` twice is the planted duplicate-registration instance (CTX-B5).
- `fixtures/llm-scripts/` — **honestly-labeled scripted LLM test doubles** (fakes standing in for
  the keyed model, used only in offline harness-mechanics ACs, never presented as the real
  service): `script-answer.json` (answers immediately, no tool calls), `script-one-tool.json`
  (calls a named tool once, then answers), `script-always-tool.json` (emits a tool call every
  iteration — the planted runaway-loop instance, CTX-B10), `script-empty.json` (returns empty
  content on every call — the planted empty-summary instance, CTX-B11),
  `script-canned-summary.json` (returns a fixed four-heading summary and a fixed label).

**Modes.** `offline` = no key, no network (embedding model assumed cached after first install);
`offline·double` = offline using a scripted LLM double; `live` = requires `OPENAI_API_KEY`
(AC19/AC21 additionally need arXiv network). Live ACs are excluded from the day-one offline run.

### Given / When / Then

| AC | Mode | Given | When | Then | Rule |
|----|------|-------|------|------|------|
| AC1 | offline | An empty directory | The store layer initializes fresh | The single store file exists and contains, empty: the conversational structure with exactly the §3 fields (incl. `summary_id`), the tool-log structure with the §3 fields, and five distinct vector memory collections (knowledge base, workflow, toolbox, entity, summary), each supporting metadata per record | contracts, R15; Ledger 7/11 invariants |
| AC2 | offline | thread-short written via the manager and papers 001+006 ingested into the KB | The process exits and a NEW process opens the same store file | Conversational read returns the 4 messages in timestamp order; KB retrieval for "session persistence after restart" returns paper-006 content | R1; Ledger 5/11 invariants |
| AC3 | offline·double | Seeded stores; `script-answer` double | One agent turn runs on thread-short | The context handed to the double contains `# Question` and all five `## … Memory` headings in the §3 order, and all five deterministic reads executed before the LLM call | R2, R3; Ledger 7/8 invariants |
| AC4 | offline·double | Same turn as AC3 | Inspecting the context and system prompt | Each segment carries "What this memory is" and "How you should leverage it" blocks; the system prompt names the five segments and the R3 conflict priority | R3 |
| AC5 | offline·double | Same turn as AC3 | The turn completes | Conversational memory holds the user query row and the final-answer row (roles `user`/`assistant`), timestamps ascending | R4 |
| AC6 | offline·double | `script-one-tool` double scripted to call `bulk_fixture_dump` | The turn completes | Exactly one tool-log record exists: correct tool_name, JSON args, FULL (>3,500-char) result, `status=success`, `error_message` null | R4 |
| AC7 | offline | ≥6 tools registered incl. `lookup_fixture_paper` | Retrieving tools for "look up a stored fixture paper" | At most 5 schemas return, deduplicated by name, each valid against the §3 retrieved-tool schema with `required` = exactly the no-default parameters; `lookup_fixture_paper` is among them | R5; Ledger 9 invariant |
| AC8 | offline | `lookup_fixture_paper` already registered | It is registered again under the same name | The toolbox store holds exactly one record for that name; the callable remains invocable; the second registration reports a skip | R6 |
| AC9 | offline·double | Model token limit configured to 1,000 for the test; thread-research seeded (assembled context >3,200 chars ⇒ >80%); `script-canned-summary` double | An agent turn assembles context | Offload runs BEFORE the reasoning call: a summary record is stored, the conversational segment is replaced by a compaction stub that names `expand_summary`, a `[Summary ID: …]` reference appears under `## Summary Memory`, and the `# Question` text survives verbatim | R7; Ledger 10 invariant |
| AC10 | live | thread-research seeded, unsummarized | `summarize_and_store(thread_id)` runs with the real LLM | A summary record valid against the §3 schema exists (four exact headings, 8-hex id, non-generic description, thread_id) and ALL 12 source rows now carry that summary_id | R8 |
| AC11 | live (follows AC10) | The AC10 thread | Summarization runs again on the same thread | It reports nothing-to-summarize, writes no new summary record, and the conversational read returns the explicit no-unsummarized-messages marker | R9 |
| AC12 | live (follows AC10) | The AC10 summary id | `expand_summary(id)` is called | The return contains the stored summary text AND all 12 original messages, chronological with timestamps | R10; Ledger 10 invariant |
| AC13 | offline·double | The AC6 turn (`bulk_fixture_dump` >3,500 chars) | The tool result is passed back to the LLM | The tool message given to the double is ≤3,000 chars + a pointer naming the tool-log id; the tool-log row still holds the full output | R11 |
| AC14 | offline·double | `script-always-tool` double; max_iterations configured to 3 | An agent turn runs | The loop stops after exactly 3 iterations and returns the templated inability answer; no exception; all 3 tool calls are in the tool log | R12; Ledger 4 invariant (tool-call protocol round-trips) |
| AC15 | offline·double | `script-empty` double | Summarization runs on thread-short's text | Exactly one retry occurs, then the deterministic fallback summary is stored — valid against the §3 schema (all four headings present) — and an id is returned | R13 |
| AC16 | offline·double | The AC6 turn completed; `fixtures/workflows/workflow-empty.json` also seeded | Workflow memory is read for the AC6 query | A workflow record from the turn exists (num_steps=1, query text, answer excerpt ≤200 chars); retrieval returns NO zero-step workflow | R14 |
| AC17 | offline·double | An entity extractor stubbed to raise | An agent turn runs | The turn completes and returns its final answer; the failure is contained (no exception escapes) | R14 |
| AC18 | offline | The initialized store layer | Introspecting configuration and running one semantic probe | All five vector memories report the same embedding model id and the same similarity metric; the paraphrase query "papers about remembering across sessions" (no shared keywords required) retrieves paper-006 from the KB | R15; Ledger 11 invariant |
| AC19 | live | Network + a real arXiv id chosen by the tester | `fetch_and_save_paper_to_kb_db(arxiv_id)` runs | ≥1 chunk lands in the KB with the full R16 metadata set (chunk_size/overlap = 1500/200 defaults); an immediate KB query for the paper's topic retrieves stored content with no second fetch | R16; Ledger 12 invariant |
| AC20 | offline | ALL stores empty | Each of the five context reads runs | Each returns its explicit no-content marker text inside its segment; no segment contains invented content | R17 |
| AC21 | live | A fresh store; fixture tools registered | Turn 1: "Find the fixture paper about session persistence" → turn 2 (same thread): "Who wrote it?" → process restart → summarize the thread → turn 3: "What was my first question?" | Turn 1's answer names *The Lantern Protocol*; turn 2 answers *S. Farrow* from memory (coreference, no re-lookup required); after restart + consolidation, turn 3's run expands the summary and the answer contains turn 1's question | R1, R2, R8, R10 end-to-end |
| AC22 | offline·double | thread-short seeded; `script-answer` double | A turn runs with the query "save the second one from that list" | The assembled context's conversation segment contains the prior assistant list naming paper-006, so the referent of "the second one" is present in context | R2, R3 (CTX-B1) |

Every business rule reaches ≥1 AC (mapping in §4); every AC traces to a rule; every CTX-B failure
mode appears as a rule, a planted fixture instance, an AC, and a CTX-B entry (§10 four-way encoding).

---

## 6. Standing Permissions (in force for the entire build)

**Always**
- Create and initialize the local store file; read/write memory only through the manager layer.
- Run the offline AC suite at any time; add tests that strengthen (never weaken) the §5 oracle.
- Register the fixture tools and the labeled LLM doubles in tests.
- Read this spec, including the Context Pack, at any point.

**Ask First** — derived by walking the course's spoken trade-offs (Pass-B list); each entry
forces rework (a) or silently changes a behavior guarantee (b):

- **AF1** Changing the summarization threshold (80%), the chars÷4 estimate, or the token-limit
  defaults — (b): silently changes *when* consolidation fires without failing an AC (Lesson 5
  thresholds; §4 table).
- **AF2** Changing the embedding model or the similarity metric after ANY data is ingested —
  (a): forces re-embedding/re-tuning of every vector store (Lesson 3's consistency warning;
  §4 metric lever).
- **AF3** Changing chunk_size/chunk_overlap after knowledge-base content exists — (a): forces
  re-ingestion (Lesson 4's chunking rationale; §4 table).
- **AF4** Reclassifying ANY operation between deterministic and agent-triggered — e.g. making
  an agent-triggered summarization run automatically beyond the >80% trigger, or leaving
  persistence to model discretion — (b): the canonical silent guarantee change (Lessons 3 & 6;
  → Ledger row 8).
- **AF5** Making a currently-optional operation run automatically every turn (deep retrieval,
  auto-consolidation, auto-entity sweeps) — (b): changes cost/behavior with no failing test
  (Lesson 3's agent-triggered rationale; → Ledger row 8).
- **AF6** Turning docstring augmentation on/off for a tool, or changing which tools are
  augmented — (b): silently shifts tool-retrieval quality (Lesson 4; → Ledger row 9).
- **AF7** Swapping the persistent store, or any destructive reset (drop/recreate) of persisted
  memory — (a): re-ingestion/re-embedding; the course's per-lesson clean-slate drops are a
  teaching-sandbox pattern, not a takeaway behavior (→ Ledger row 11).
- **AF8** Enabling the Tavily web-search tool (or any keyed external tool) — (a)+(b): introduces
  a credentialed dependency and changes what enters the knowledge base (→ Ledger row 12).

**Never**
- Fabricate paper metadata, citations, memory contents, or summary text — summaries must derive
  from stored units (R8, R17).
- Answer as though evidence exists when the segments returned their empty markers — state what is
  missing (R17).
- Mutate fixtures or the scripted LLM doubles to make an acceptance criterion pass.
- Hardcode or commit secrets or credentials (including reproducing the course's inline DB
  password pattern — §2).
- **[H]** Delete or rewrite persisted memory rows outside the defined operations —
  `summary_id` marking is the only in-place update the pattern defines (project hardening; the
  course does not demonstrate row deletion in the running system).

---

## 7. Test Plan & Self-Verification

Real commands (adjust only the venv path to your platform):

```
python3.12 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt        # pytest, sentence-transformers, openai, python-dotenv, arxiv, pymupdf
pytest tests -m "not live" -q          # offline suite: AC1–AC9, AC13–AC18, AC20, AC22 — no key, no network
OPENAI_API_KEY=... pytest tests -m live -q   # live suite: AC10–AC12, AC19, AC21 (AC19/AC21 need arXiv network)
```

The building agent MUST report results **per acceptance criterion** with cited evidence: the test
command run, the pass/fail output for that AC's test id, and the file paths of artifacts examined
(e.g. the store file inspected for AC1, the logged context for AC3). "Should pass" / "looks
correct" are treated as failures — they mean it wasn't run. Fixture files and LLM-double scripts
are read-only inputs to the suite; a change to either invalidates the run.

---

## Course Context Pack (embedded — agent-readable)

Concepts only — no course code. CTX anchors are position-independent. Everything in CTX-A…CTX-C is
durable; only the names in CTX-D are perishable.

### CTX-A. The pattern

The course's central buildable pattern is the **memory-aware agent loop over typed persistent
stores**:

`register/ingest → [per turn] assemble partitioned context → monitor budget (offload >80%) →
retrieve top-k tools semantically → reason + act loop (log every tool call) → persist learning
(conversation, workflow, entities) → [next session] reuse`

- **Register/ingest** — tools enter a searchable toolbox store (descriptions embedded); knowledge
  enters the KB: capabilities and facts must exist in memory before any turn can retrieve them.
- **Assemble partitioned context** — deterministic reads fill typed markdown segments, each with
  usage instructions: the agent cannot choose to look up what it doesn't know exists, so the
  harness bootstraps context every turn, and markdown headings give the model a hierarchy it
  already knows how to read (Lessons 3 & 6).
- **Monitor budget** — context windows are finite; a cheap length estimate plus a threshold turns
  overflow from a crash into a scheduled consolidation (Lesson 5).
- **Retrieve tools semantically** — passing every tool bloats context and degrades selection;
  embedding descriptions and retrieving top-k scales the registry to hundreds of tools (Lesson 4).
- **Reason + act** — an iterative loop with a stop condition (final answer, or max iterations);
  tool results are bounded in context and complete in the audit log (Lesson 6).
- **Persist learning** — conversation, trajectories (workflow), and entities are written back
  deterministically so each run makes future runs cheaper and more consistent (Lessons 3, 5, 6).
- **Reuse across sessions** — the store, not the process, is the agent's memory core: everything
  above survives restart (Lesson 2's stateless-agent failure is the motivating counterexample).

### CTX-B. Failure-mode catalog

Each entry: symptom → cause → fix → enforcement.

- **CTX-B1 Stateless reset.** Symptom: agent cannot resolve "book the first one" / loses all
  context between sessions (Lesson 2's restaurant demonstration). Cause: no external memory —
  knowledge dies with the context window. Fix: persist conversation (and all memory types) in an
  external store read back every turn. Enforced by R1/R2 — AC2, AC21, AC22.
- **CTX-B2 Chicken-and-egg retrieval.** Symptom: agent never consults memory it actually has.
  Cause: retrieval left to model discretion — "you need memory to know which memory you need"
  (Lesson 3). Fix: deterministic context-assembly reads at loop start. Enforced by R2 — AC3.
- **CTX-B3 Selective-save gaps.** Symptom: later turns miss context that "should" exist. Cause:
  the model decides what to save and forgets; gaps break long-horizon tasks (Lesson 3). Fix:
  deterministic persistence of every turn and every tool call. Enforced by R4 — AC5, AC6.
- **CTX-B4 Tool-context bloat & selection degradation.** Symptom: worse answers, higher latency
  and cost as tools grow; providers recommend ~10–20 tools max (Lesson 4). Cause: all tool
  definitions stuffed into context. Fix: toolbox-as-memory with semantic top-k retrieval.
  Enforced by R5 — AC7.
- **CTX-B5 Duplicate tool rows.** Symptom: repeated registrations pollute retrieval. Cause:
  re-running registration writes again. Fix: name-keyed dedup that skips the store write.
  Enforced by R6 — AC8.
- **CTX-B6 Context overflow.** Symptom: token-limit failures or silently dropped history in long
  conversations (Lesson 5). Cause: unbounded accumulation. Fix: usage monitoring with a
  deterministic >80% consolidation trigger that never touches the current question. Enforced by
  R7 — AC9.
- **CTX-B7 Lossy summarization.** Symptom: details (exact quotes, chronology) unrecoverable after
  compression — "summarization is always a lossy technique" (Lesson 5). Cause: destructive
  summarization with no link back. Fix: structured four-heading extraction + summary_id links +
  expand-on-demand. Enforced by R8/R10 — AC10, AC12.
- **CTX-B8 Re-summarization churn.** Symptom: the same messages summarized repeatedly; summaries
  of summaries. Cause: no marking of consumed units. Fix: summary_id marking; reads and
  summarizers see only unmarked rows. Enforced by R9 — AC11.
- **CTX-B9 Tool-output bloat.** Symptom: one large tool result crowds the window. Cause: raw
  payloads routed through the model. Fix: bounded in-context result + full copy in the tool log
  with a pointer (context offloading, Lesson 6). Enforced by R11 — AC13.
- **CTX-B10 Runaway loop.** Symptom: the agent iterates forever or dies without an answer.
  Cause: no stop condition. Fix: max-iterations bound with a templated inability answer
  (Lesson 6). Enforced by R12 — AC14.
- **CTX-B11 Empty-summary failure.** Symptom: consolidation stores nothing / crashes when the
  model returns empty output. Cause: single unguarded LLM call. Fix: one simpler-prompt retry,
  then a deterministic four-heading fallback (Lesson 5's "safety mechanism"). Enforced by
  R13 — AC15.
- **CTX-B12 Repeated discovery work.** Symptom: the agent re-fetches what it already found.
  Cause: tool results returned but never persisted. Fix: search-and-store — external results are
  written to the KB with source metadata at fetch time (Lesson 4). Enforced by R16 — AC19.

### CTX-C. Decision background (reference only — decisions live in the Decision Ledger)

- **CTX-C1 Store topology → Ledger 7.** The course maps human memory taxonomy to stores:
  conversational = episodic (time-addressable), knowledge base + entity + summary = semantic,
  workflow + toolbox = procedural (Lessons 2–3). The short-term forms (semantic cache, working
  memory) are taught as taxonomy, not built. "Memory Unit" = the smallest atomic record per store
  (Lesson 3). The "Agent Memory Core" framing: the database sees the most data traffic of any
  component, hence one persistent core rather than scattered state (Lesson 2).
- **CTX-C2 Memory-aware vs memory-augmented → Ledger 7/8 and R3.** Lesson 3 defines the upgrade
  path: explicit memory-type allocation → system-prompt awareness of the stores → memory
  operations as tools → partitioned context window. R3's segment instructions and the R2/R4
  deterministic frame implement it.
- **CTX-C3 Deterministic vs agent-triggered → Ledger 8.** Mechanism: deterministic ops buy
  predictability, completeness, and debuggability; agent-triggered ops buy relevance and cost
  control; external tools are agent-triggered because only the model can judge intent (L2.ipynb
  cells 20–23). Contradiction record: the L2.ipynb classification table lists `write_entity` and
  `read_summary_context` as agent-triggered-only, but the L5.ipynb app runs both deterministically
  (entity extraction on query/answer; summary context at loop start); `read_toolbox` is dual
  (deterministic top-k each turn AND a registered tool); summarize is dual by design — Lesson 6:
  "both a deterministic and an agent-triggered memory operation."
- **CTX-C4 Similarity metric lever → §4 table.** Why it matters mechanically: the metric defines
  neighborhood shape in embedding space; mixing metrics between write-time indexing and read-time
  search silently degrades retrieval, which is why the course rebuilds all stores per lesson "with
  consistent distance strategy" (L3.ipynb cell 15). Both sides' sources are in the §4 row.
- **CTX-C5 Index realization → §4 table, Ledger 11.** The course markdown teaches HNSW
  (graph-based traversal); the course's executed helper builds IVF partitioned indexes instead,
  documenting Oracle-Free-edition errors as the reason. Durable lesson: index choice is an
  operational fit decision inside the chosen store, invisible at the pattern level; exact search
  is the correct realization at small scale.
- **CTX-C6 Toolbox augmentation → Ledger 9.** Mechanism: richer embedded text (LLM-expanded
  description + synthetic queries) increases inter-tool separability in embedding space, raising
  retrieval recall (Lesson 4's live original-vs-augmented comparison). Cost: LLM calls at
  registration. The `get_current_time` flag discrepancy is recorded in the row.
- **CTX-C7 Context reduction → Ledger 10.** Summarization compresses into a clean window (lossy);
  compaction moves content to the DB under an id + description and lets the model pull it back
  (recoverable); the course's app combines them and adds structured extraction under four headings
  because "consolidation isn't just compression — it's structured extraction" (L4.ipynb summary).
  JIT retrieval is the read-side twin: fetch detail only at the moment of need (L5.ipynb cell 15).
- **CTX-C8 Provenance of the running example.** The course's demo assistant is named "ArxivScout"
  (L2.ipynb cell 28); its seed corpus streams 100 records from a public arXiv dataset; its test
  thread is a scripted PhD-research conversation (helper's sample; the helper comment says 30
  messages, the Lesson 5 narration says 32 — no build impact; this spec's fixtures are authored
  fresh). Hybrid search is provisioned on the KB store but never exercised (→ §1 Not Included).
- **CTX-C9 Model/token config → Ledger 4, §4 table.** The course splits model use (mini model in
  the loop, larger in helpers) without arguing it; the token map is keyed inconsistently across
  files. Durable point: token limits are per-model configuration the harness must own.

### CTX-D. Perishable assumptions

Treat every name below as a **search keyword against current documentation, not a guaranteed
import**. The course's installs are entirely unpinned (its requirements file lists bare package
names); the concepts in CTX-A…CTX-C are durable — only these names age:

- Store/course infra: Oracle AI Database **26ai**, `FREEPDB1` DSN, `VECTOR` schema user, Docker
  bootstrap, `langchain-oracledb` (`OracleVS`, `OracleVectorizerPreference`), `DistanceStrategy`
  (`COSINE` / `EUCLIDEAN_DISTANCE`), IVF DDL "ORGANIZATION NEIGHBOR PARTITIONS … TARGET ACCURACY
  95", HNSW.
- Embeddings: `HuggingFaceEmbeddings` — imported from `langchain_huggingface` in some lessons and
  `langchain_community.embeddings` in others (same era, drifting namespace);
  `sentence-transformers/paraphrase-mpnet-base-v2`.
- LLM: OpenAI Python SDK `chat.completions` with `tools` / `tool_choice="auto"` /
  `max_completion_tokens`; model names `gpt-5`, `gpt-5-mini`.
- Tools/data: `tavily-python` `TavilyClient`, `langchain_community` `ArxivRetriever` /
  `ArxivLoader`, `langchain_text_splitters` `RecursiveCharacterTextSplitter`, `datasets`
  `load_dataset("nick007x/arxiv-papers", streaming=True)`, `pymupdf`, `pydantic`, `python-dotenv`.

### CTX-E. Provenance map (transcript numbering — authoritative)

Nothing in this spec requires platform access. **Numbering note:** notebook FILES L2–L5 correspond
to transcript Lessons 3–6 (each notebook's own title cell matches the transcript one step behind
its filename's slot), and the notebook dump's lesson-map header is itself shifted (it labels
L2.ipynb "Lesson 4" over Memory-Manager content that the transcripts place in Lesson 3).
Transcripts win; notebook citations in this spec use file+cell for that reason.

- **Lesson 1 — Introduction:** course framing, Oracle partnership, memory engineering as
  first-class infrastructure → CTX-A framing.
- **Lesson 2 — Why AI Agents Need Memory:** stateless-agent failure demo, conversational memory
  and its limits, short/long-term taxonomy, RAG→agent-memory bridge, Agent Memory Core →
  CTX-B1, CTX-C1, Ledger rows 5/11 invariants.
- **Lesson 3 — Constructing The Memory Manager (L2.ipynb):** agent stack & memory layer,
  deterministic/agent-triggered classification, memory units, context engineering, memory
  lifecycle, StoreManager/MemoryManager, cosine narration, index creation, ArxivScout ingestion →
  CTX-C1–C4, Ledger rows 7/8/11, R2/R4/R15, §4 metric lever.
- **Lesson 4 — Scaling Agent Tool Use with Semantic Tool Memory (L3.ipynb):** toolbox pattern,
  docstring augmentation, Tavily search-and-store, arXiv candidate + deep-ingestion tools,
  chunking rationale → CTX-B4/B5/B12, CTX-C6, Ledger rows 9/12, R5/R6/R16.
- **Lesson 5 — Memory Operations: Extraction, Consolidation, Self-Updating (L4.ipynb):**
  summarization vs compaction, workflow memory, token estimation and thresholds, four-heading
  extraction, summary_id marking, expansion, verification pipeline → CTX-B6–B8/B11, CTX-C7,
  Ledger row 10, R7–R13.
- **Lesson 6 — Memory Aware Agent (L5.ipynb):** agent loop and harness, in/out-of-loop memory
  ops, partitioned system prompt, JIT retrieval, tool-log offloading, max-iterations stop, the
  MemGPT-paper walkthrough of continuity/summarize/expand → CTX-B9/B10, CTX-C2/C3, R2/R3/R11/R12/
  R14, Ledger row 8.
- **Lesson 7 — Conclusion:** pattern recap (modeling, semantic retrieval, extraction,
  consolidation, write-back) → CTX-A.

---

*Spec v1.0 · Course: Agent Memory: Building Memory-Aware Agents (DeepLearning.AI × Oracle) ·
Learner project: `[project]` (Ledger row 1 default until substituted) · Living document: when the
building agent produces something unexpected, add the missing constraint here (rule + AC + CTX
anchor) and re-run — divergence is a diagnostic, not a footnote.*
