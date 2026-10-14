# Spec: Memory-Aware Research Assistant — Standalone Takeaway

> **What you're building:** a terminal research assistant that remembers — you tell it who your advisor is, ask it to summarize the conversation with its own tool, then ask "What was my first question?" and watch it open the stored summary and answer word for word, in a new session as well as the old one. Answer the gate's first question with the recommended baseline build and the agent builds it end to end; the build is COMPLETE when the offline acceptance suite passes — an OpenAI API key unlocks only the `live` tests and live use of the finished assistant.
>
> This file is self-contained: the Course Context Pack at the end replaces every external course reference, and nothing here requires platform access.
>
> `(CTX-X)` anchors mark course-derived knowledge. The Decision Ledger below holds every point where this build could diverge, each pinned to one course-derived default, so the spec builds as-is with no intake.
>
> Generated from the "Agent Memory: Building Memory-Aware Agents" notebooks + transcripts on 2026-10-14, guide @ b03ddc9.

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
   the course-faithful Options entry, not the Ledger Default. You may also mark an option
   "(Recommended)" — your judgment for THIS person's context, made now, at gate time; with no
   contextual reason to depart, recommend the row's Default. When your recommended option IS
   the course's actual choice, merge the labels into "(Recommended - course default)". A
   recommendation never removes or moves the "(course default)" label, and no option is ever
   labeled with a bare "(default)" — these two labels and their merged form are the only
   option labels. Use the answers already given (project, data, goal, …) to frame
   later questions and describe options in the person's own terms — but never skip a row, drop
   or alter an Option, or move the "(course default)" label because of an earlier answer. Put
   any realizations beyond the tool's option slots (or the free-form case) under the tool's
   "Other"/free-text. Ask about **every** row. A per-call item limit is NEVER a reason to drop,
   skip, merge, or silently default a row — make as many separate calls as there are rows.
4. **Presenting any of these questions ENDS YOUR TURN — stop here; write no code, create or edit
   no file, take no other build action.** Keep asking, one row at a time, until **every** row has
   an answer (a chosen option, an explicit "use the course default", or the step-2 baseline answer,
   which resolves every row at once). Answers to *some* rows do NOT release the build; "no reply
   yet" is not an answer — wait for the user.
5. **Before the first line of code, print a resolved-decision checklist and write it to
   `resolved-decisions.md`** — every Ledger row with its final value (the user's choice, or its
   Ledger default), each line carrying a deviation mark: `= course choice`, or
   `≠ course choice (course used: <option>)`. The file records what this build was built from;
   nothing reads it back — a later build re-runs this gate. If the baseline path was chosen,
   walk the person through every `≠` row — the course's actual choice, and why this build's
   default substitutes it (the row's Trade-off/branch note says why) — before building. Begin
   implementation ONLY after this checklist is shown and written; if any row is unresolved you
   are not done — return to step 3. Build on the checklist's values.

The Ledger has **14 rows** (L1–L6, D1–D4, RR1–RR3, C1); a complete customize pass asks 14 questions after the first one.

## Decision Ledger (§0 above requires the build agent to present these before building)

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L1 | learner | **Project** — what the memory-aware agent is for. The default is the course's *example realization* (a research assistant over academic papers, with paper-search tools); expect to swap it when your project differs — the memory pattern, not the research domain, is what must survive. | | `[project]`: a terminal research assistant that remembers across turns and sessions — the course's example, an assistant that helps a user investigate a topic over multiple sessions (CTX-A). Precedence branch: the course's example scenario shape, re-expressed on the synthetic fixture corpus (§5). | Terminal research assistant over papers (course default); your own domain assistant (support desk, personal notes, codebase helper) keeping the same memory stores and loop; free-text | Swapping the domain swaps the example tools (RR3, the paper tools in §2) and the seed data (L2); the stores, the context window layout and the loop stay. | learner |
| L2 | learner | **Data / inputs** — what the knowledge base is seeded with and what the agent operates on. | | `[data]`: the synthetic fixture corpus of §5 (`fixtures/papers.json` plus the scripted conversations) — no course data copied. | Synthetic fixture corpus; the course's seed — the first 100 records streamed from the public `nick007x/arxiv-papers` dataset, title + subjects + abstract per record (course default — needs network and the `datasets` package; no key); your own documents ingested through the same knowledge-base write; free-text | Real seed data does not change any acceptance criterion (all run on fixtures); a different embedding-friendly text layout per record changes what the knowledge segment retrieves. | learner |
| L3 | learner | **Goal** — what "working" means for this build. | | `[goal]`: within one thread the assistant resolves references to earlier turns; across a process restart it still recalls the thread; after its conversation is summarized it can recover the exact original turns on demand. | Default goal; your own goal (e.g. recall user preferences across weeks), stated as an observable behavior; free-text | A goal that needs memory types the pattern does not have (e.g. scheduled forgetting) is listed in §1 Not Included. | learner |
| L4 | learner | **Model / provider** for live use. | The model must support native tool (function) calling with JSON-schema parameters, a system role, and multi-turn tool-result messages (CTX-A, CTX-C3). | `[model]`: OpenAI via its Chat Completions API with tool calling, `tool_choice` automatic — the course's provider; the specific model is chosen at gate time. | OpenAI Chat Completions (course default — needs an OpenAI API key, paid; the course ran `gpt-5-mini` for the agent loop and summaries in the Lesson 5 notebook and `gpt-5` for tool augmentation, entity extraction and the end-to-end helper's summaries); any other provider with native tool calling; free-text | Switching provider changes request parameters (CTX-D) and possibly tool-call message shapes; the offline suite is unaffected (it runs on the scripted model, RR2). | course+learner |
| L5 | learner | **Environment** — where it runs. | Memory must survive process restarts: a new process pointed at the same store sees every earlier thread, summary, workflow, entity and tool (Lesson 6: the agent "persists across sessions"). | `[environment]`: one local machine, one Python process at a time, store location configurable (default: a file in the working directory). | Local single process; a long-running service process shared by several terminals (adds concurrent-writer concerns the course never covers); free-text | A shared service needs a store realization that tolerates concurrent writers (RR1 options). | course+learner |
| L6 | learner | **Scope boundary** — present the full §1 "Not Included" list (all 14 items, with their tags) inside this question; the gate shows nothing else that renders it. Ask whether to keep every exclusion or bring one back. | | Keep as-is: every §1 exclusion stands and the full acceptance set (AC1–AC34) is built. | Keep every exclusion; bring an item back — answered by its tag: *restorable* → added, with no acceptance criteria supplied (say so); *named, never built* → buildable, but this spec supplies no parameters and no acceptance criteria; *owned by another row* → answer it at the named row instead; *unavailable* → declined; free-text for an extra exclusion, which must name the acceptance criteria it retires | Restoring an item grows the build beyond what the acceptance suite checks. | learner |
| D1 | design-structural | **Memory-store topology** — how memory types map to stores. | Two kinds of storage must both exist: exact-key, time-ordered storage for conversation turns and tool logs (read by thread id, never by similarity), and similarity-searchable storage for knowledge base, workflow, toolbox, entity and summary memories with metadata filtering; every memory type stays separately readable. | One store per memory type, seven stores, named `CONVERSATIONAL_MEMORY` and `TOOL_LOG_MEMORY` (exact-key) and `SEMANTIC_MEMORY`, `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY` (similarity) — the course's layout (CTX-C1). | Seven per-type stores (course default); one similarity store holding all five similarity memory types with a memory-type field that every read filters on, plus the two exact-key stores; free-text | The single-store option saves tables but turns every read into a filtered read — a forgotten filter mixes memory types into the wrong context segment. Changing topology after data exists forces a migration (§6 Ask First). | course+learner |
| D2 | design-argued | **Tool-description augmentation** at toolbox registration. | Every registered tool is stored with a retrieval text that names the tool and describes what it does, and the description the model is offered comes from the same stored record. | Augmented for every tool: at registration the model rewrites the tool's description from its original description and source (one-line summary, step-by-step behavior, when to call it, caveats) and writes 5 synthetic user queries; name + augmented description + signature + queries become the retrieval text, and the augmented description is what the model is offered (R7). Course flags were per tool: the end-to-end helper augments the paper-fetch and both summary tools and registers paper search and the clock raw — the baseline departs only there. | Augmented registration (course default — the argued position, Lesson 4); raw registration — name + original description + signature, no model call (the course's baseline, used for its paper-search tool); free-text | Lesson 4 argues augmentation gives "higher and better separability between the tools … higher recall": plain semantic tool retrieval is "a great idea, but it might not be enough". Litmus branch: **row** — the course shows raw registration working (it built it first and still registers some tools raw) and moves beyond it; neither side is shown failing, and the sides differ in a component (a model call at registration), not a value. Cost: one or two model calls per tool registered. The course's code embeds the raw text into the vector row and keeps the augmented embedding only as metadata, contradicting the narration; this spec follows the narration (CTX-C4). | course+learner |
| D3 | design-argued | **Memory-operation trigger assignment** — which memory operations the harness runs every turn (deterministic) and which the model decides to run (agent-triggered, exposed as tools). | The baseline context load and the persistence writes that continuity depends on (conversation turns) must run deterministically every turn; at least one way to recover summarized detail must be agent-callable. | The course's end-to-end assignment (Lesson 6): deterministic — read conversation, knowledge base, workflow, entity and summary-context segments; check usage and offload above the threshold; select tools by similarity; write the user turn, extract entities from it, write workflow, extract entities from the answer, write the assistant turn. Agent-triggered — `summarize_and_store`, `expand_summary`, and the domain tools. | End-to-end assignment as above (course default); also expose toolbox search as an agent-callable tool so the model can look for more tools mid-loop (the Lesson 3 notebook's toolbox search is marked both deterministic and agent-triggered); the Lesson 3 classification table's assignment — entity writes and summary-context reads agent-triggered instead of every turn; free-text | Lesson 3 argues both sides: deterministic gives predictable behavior, "you don't want the agent to forget to save", and "the agent can't choose to look up what it doesn't know exists"; agent-triggered gives relevance, cost and latency control and higher-signal memory. Lesson 6 calls summarization "both a deterministic and an agent-triggered memory operation". Litmus branch: **row** — both sides shown working, the sides differ in ownership (harness vs model). Lower-precedence evidence: the course contradicts itself here — the Lesson 3 table marks entity writes and summary-context reads agent-triggered and toolbox search both, while the Lesson 6 loop runs all three deterministically and never exposes toolbox search as a tool; the default follows Lesson 6, the end-to-end application (CTX-C2). | course |
| D4 | design-argued | **Context-reduction mode** — what happens to conversation turns once they are summarized. | Summarizing must shrink the conversation segment and leave a summary reference the model can see in the summary segment. | Recoverable compaction: the summary is stored with its id, label and the full original transcript; the original turns stay in the conversation store marked with that summary id and drop out of the conversation segment; `expand_summary` returns the summary and the original turns (R11, R12, R15). | Recoverable compaction (course default); lossy summarization — the summary replaces the turns, the originals are deleted and no expand tool exists; free-text | Lesson 5 presents both: summarization keeps the highest-signal content but "will always be a lossy technique"; compaction offloads to the database with an id and a description so "if it needs more information, it can just go into the database". Litmus branch: **row** — the course presents lossy summarization as a technique with a cost, not a failure, and the sides differ in a component (the retained originals and the expand tool). Choosing lossy retires AC21's full-content assertion and AC25. | course |
| RR1 | realization | **Persistent store realization** — the engine behind the seven stores. | Durable storage (survives process restart) that offers exact-key tables queried by thread id in timestamp order, similarity search over stored embeddings using the configured metric, and metadata filters with equality (summary id, thread id) and numeric greater-than (workflow step count); writes committed before a turn returns. | SQLite from Python's standard library: one database file, each similarity row stores its embedding, similarity computed exactly (brute force) in-process at read time. Branch 1 substitution: the course's database needs a container plus an admin-created user and tablespace (heavy), and the course teaches the memory-core pattern, not the database product — the lessons' subject is memory types, the manager and the agent loop. Lightest tier that meets the Invariant at the declared scale (the §5 fixtures: tens of rows per store): **tier 1, ships with the language** — exact in-process similarity over fixture-sized data needs no vector index. | Oracle AI Database 26ai through LangChain's Oracle vector store, IVF vector index at target accuracy 95 (course default — heavy setup: a running database container, an admin connection to create the `VECTOR` user and an ASSM tablespace; tens of seconds to start); an embedded vector library beside SQLite (tier 2 — a package install, no separate process); a locally served vector database (tier 3 — its own process, no credentials); free-text | Moving stores after data exists means migrating every row and re-embedding if the embedding layout changes (§6 Ask First). An approximate index only pays off well above fixture scale. The course's index was IVF because HNSW raised errors on the free database edition; its notebook text still says HNSW (CTX-C5). | course+learner |
| RR2 | realization | **Model the acceptance suite runs against.** | Every offline acceptance criterion drives the real pipeline end to end — context build, tool selection, the loop, tool execution, tool logging, summarization, entity extraction, augmentation — with only the model's replies replaced. | The scripted model of §5 (`scripted_model.py`): an honestly labeled fake whose replies per role are authored in this spec; it never claims to be a real model. Branch: the model is the keyed dependency and is the only carrier of the agent-loop, summarization, entity-extraction and augmentation stages, so the stand-in is the default and omission is not offered. | Scripted stand-in model, declared in §5; OpenAI Chat Completions with the course's models (`gpt-5-mini`, `gpt-5`) (course default — needs an OpenAI API key, paid; runs only the `live` criteria); free-text | The scripted model proves the wiring, not the model's judgment; `live` criteria AC32–AC34 check real behavior. | course+learner |
| RR3 | realization | **Web search tool** (the course's keyed search-and-store tool). | External content a tool brings in is written to the knowledge base, with its source in metadata, so later turns retrieve it without calling the tool again. | Omit the keyed web-search tool; the keyless paper fetch-and-save tool (`fetch_and_save_paper_to_kb_db`) carries the search-and-store behavior (R20). Branch: keyed tool, not the only carrier of a taught behavior — omitted by default. The course's end-to-end Lesson 6 agent does not register it either. | `search_tavily` via the Tavily API, up to 5 results per query, each persisted to the knowledge base with title, URL, score, `source_type` "tavily_search", query and timestamp (course default — needs a Tavily API key); `search_tavily_standin` — an honestly labeled local stand-in that returns canned results from a fixture file, says it is a stand-in in its registered description, and persists them the same way; omit — the paper fetch-and-save tool does the job; free-text | With omission the assistant cannot search the open web, only the paper service. Restoring Tavily adds a key and a network dependency but no new memory behavior. | course+learner |
| C1 | contradicted | **Summary scoping** — whether summaries belong to a thread. | Whatever scope summaries are written with is the scope the summary segment reads with — a summary written must be visible to the thread that wrote it. | Thread-scoped: every summary records its thread id; the summary segment lists only the active thread's summaries; summaries made from free text inside a turn take that turn's thread. Taken from the end-to-end helper used by Lesson 6 and its system prompt ("prefer summaries for the active thread_id"). | Thread-scoped summaries (course default — Lesson 6 helper); global summaries visible to every thread — the Lesson 5 notebook writes summaries with no thread id (course default — Lesson 5 notebook); free-text | Stakes test passed: the two sides return different summary lists to the same read, a semantics change at first build. In the course the Lesson 5 notebook's unscoped summaries would never appear in Lesson 6's thread-scoped read — the failure CTX-B8 records. Choosing global changes AC20. | course |

## 1. Objective

A terminal research assistant that keeps memory outside the model — conversation turns, knowledge, past workflows, tools, entities, summaries and tool logs in separate persistent stores — assembles a labeled, partitioned context window from them on every turn, chooses its tools by similarity search, keeps its context under budget by compacting old turns into expandable summaries, and still recalls a thread after a restart (CTX-A).

The deliverable is a Python package with: the memory manager over the seven stores, the toolbox, the agent entry point (course name `call_agent`), and a terminal chat command that sends each line you type to the agent on one thread id (default `"1"`) and prints the answer. The terminal command is project hardening — the course drives the agent from notebook cells.

### Not Included            ★

1. **Hybrid (keyword + vector) knowledge-base search.** *Named, never built* — the course defines a hybrid-search setup it never calls; no parameters, no acceptance criteria.
2. **A re-ranking stage after retrieval.** *Named, never built* — described in Lesson 2's retrieval overview only.
3. **Graph-traversal retrieval.** *Named, never built* — listed among retrieval strategies in Lesson 3.
4. **A semantic cache of previous model responses.** *Named, never built* — a short-term memory form in Lesson 2's taxonomy.
5. **Deleting, forgetting, decaying or merging memories.** *Named, never built* — Lesson 3 names forget/update/delete operations and the notebook lists "strengthen, update, merge, or decay"; none is built.
6. **An agent-callable reader for logged tool output.** *Named, never built* — the course logs full tool output "for audit and later retrieval" but registers no tool that reads it back.
7. **Fine-tuning embedding or language models.** *Named, never built* — part of Lesson 3's memory-engineering overview.
8. **Web search via Tavily.** *Owned by another row* — row RR3.
9. **The course's database product and an approximate vector index.** *Owned by another row* — row RR1.
10. **The course's public paper dataset as seed data.** *Owned by another row* — row L2.
11. **Toolbox search exposed as an agent-callable tool.** *Owned by another row* — row D3.
12. **A web or graphical user interface.** *Restorable* — no acceptance criteria supplied.
13. **Multiple user accounts, authentication or access control.** *Restorable* — no acceptance criteria supplied.
14. **Integrating this pattern into an existing codebase.** *Unavailable* — this spec builds a standalone project only.

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python 3.10 or newer | The course code uses `X \| None` type syntax, which needs 3.10+ (generator's reading; the course states no Python version). |
| Install situation | Course installs were **unpinned**: its requirements list package names only (LangChain Oracle integration, LangChain Hugging Face, sentence-transformers, LangChain community, LangChain OpenAI, datasets, LangChain, tavily-python, pydantic, oracledb, openai, dotenv, arxiv, pymupdf), no versions. | Every dependency below is therefore taken at its latest stable release at build time; write the versions you resolved into the lock file you produce. Era-specific class and model names are perishable — see CTX-D. |
| Persistent store | Ledger RR1 Default | Change it at row RR1, not here. |
| Store topology | Ledger D1 Default | Change it at row D1. |
| Embedding model | `sentence-transformers/paraphrase-mpnet-base-v2`, 768-dimensional vectors, run locally through the `sentence-transformers` package | The course's model in every lesson. Keyless; needs a one-time download into the local model cache (§7), after which it runs offline. The same model embeds every write and every query (R18). |
| Similarity metric | Cosine, for all five similarity stores, at write and read | Post-build lever, contradicted in the course: cosine in the Lesson 3 and 4 notebooks and narrated aloud in Lesson 3; Euclidean in the Lesson 5 and 6 notebooks and in the Lesson 3 notebook's prose. Chosen by the lever-value rule's first branch — the narration of the lesson that introduces the stores says cosine (CTX-C6). |
| Model client | Ledger L4 (live use) and RR2 (acceptance suite) | The model is injected behind one interface; every call carries a role (§3). Secrets: the OpenAI key (and, if RR3 restores it, the Tavily key) are read from environment variables, loaded from a local `.env` file that is git-ignored; never hardcoded or logged. |
| Agent harness | A hand-written loop over the model's native tool-calling API — no agent framework | The course writes its own loop on the OpenAI SDK. |
| Paper tools | `arxiv_search_candidates` and `fetch_and_save_paper_to_kb_db` over the public arXiv API (keyless); PDF text extraction for full papers | The course's example tools (L1 example realization). Course realization: LangChain's arXiv retriever and loader with PyMuPDF; any library reaching the same API is fine. Criteria that touch the network are `live`. |
| Text splitting | Recursive character splitting, chunk 1,500 characters, overlap 200 | The course's values for full-paper ingestion (R20). |
| Tests | `pytest`, with a `live` marker for criteria that need a key or the network | §7. |

## 3. Input/Output Contracts            ★

**Entry point.** `call_agent(query: string, thread_id: string = "1") → TurnResult`. One call is one user turn. The model client and the store location are injectable (the acceptance suite injects the scripted model and a fresh store file).

**Model interface.** Every model call carries a `role` from `agent | augment | queries | summary | label | entities`. `agent` calls send messages plus a tool list and may return tool calls; the others send one prompt and return text.

**Tool names (binding):** `expand_summary(summary_id, thread_id?)`, `summarize_and_store(text?, thread_id?)`, `get_current_time(detailed?)`, `arxiv_search_candidates(query, k=5)`, `fetch_and_save_paper_to_kb_db(arxiv_id, chunk_size=1500, chunk_overlap=200)`; `search_tavily(query, max_results=5)` only if row RR3 restores it.

**Context segment headings (binding, in this order):** `# Question`, `## Conversation Memory`, `## Knowledge Base Memory`, `## Workflow Memory`, `## Entity Memory`, `## Summary Memory`.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$defs": {
    "ConversationMessage": {
      "type": "object",
      "required": ["id", "thread_id", "role", "content", "timestamp", "metadata", "created_at", "summary_id"],
      "properties": {
        "id": { "type": "string", "minLength": 1 },
        "thread_id": { "type": "string", "minLength": 1 },
        "role": { "enum": ["user", "assistant"] },
        "content": { "type": "string" },
        "timestamp": { "type": "string", "format": "date-time" },
        "metadata": { "type": "string" },
        "created_at": { "type": "string", "format": "date-time" },
        "summary_id": { "oneOf": [ { "type": "null" }, { "type": "string", "pattern": "^[0-9a-f]{8}$" } ] }
      }
    },
    "ToolLogEntry": {
      "type": "object",
      "required": ["id", "thread_id", "tool_call_id", "tool_name", "tool_args", "result", "result_preview", "status", "error_message", "metadata", "timestamp", "created_at"],
      "properties": {
        "id": { "type": "string", "minLength": 1 },
        "thread_id": { "type": "string", "minLength": 1 },
        "tool_call_id": { "type": ["string", "null"] },
        "tool_name": { "type": "string", "minLength": 1 },
        "tool_args": { "type": "string", "description": "JSON text of the arguments the model supplied" },
        "result": { "type": "string", "description": "full, untruncated tool output" },
        "result_preview": { "type": "string", "maxLength": 2000, "description": "first 2,000 UTF-8 bytes of result" },
        "status": { "enum": ["success", "failed"] },
        "error_message": { "type": ["string", "null"] },
        "metadata": { "type": "string", "description": "JSON text; carries the loop iteration number" },
        "timestamp": { "type": "string", "format": "date-time" },
        "created_at": { "type": "string", "format": "date-time" }
      },
      "if": { "properties": { "status": { "const": "failed" } } },
      "then": { "properties": { "error_message": { "type": "string", "minLength": 1 } } },
      "else": { "properties": { "error_message": { "type": "null" } } }
    },
    "SummaryRecord": {
      "type": "object",
      "required": ["id", "thread_id", "summary", "full_content", "description"],
      "properties": {
        "id": { "type": "string", "pattern": "^[0-9a-f]{8}$" },
        "thread_id": { "type": "string", "minLength": 1, "description": "required under row C1's default" },
        "summary": {
          "type": "string",
          "allOf": [
            { "pattern": "### Technical Information" },
            { "pattern": "### Emotional Context" },
            { "pattern": "### Entities & References" },
            { "pattern": "### Action Items & Decisions" }
          ]
        },
        "full_content": { "type": "string", "minLength": 1 },
        "description": {
          "type": "string",
          "minLength": 1,
          "not": { "enum": ["conversation summary", "summary", "chat summary", "thread summary", "Conversation summary", "Summary", "Chat summary", "Thread summary"] }
        }
      }
    },
    "SummarizeOutcome": {
      "oneOf": [
        { "type": "object", "required": ["status"], "properties": { "status": { "const": "nothing_to_summarize" } }, "additionalProperties": false },
        { "type": "object", "required": ["id", "description", "summary", "num_messages_summarized"],
          "properties": {
            "id": { "type": "string", "pattern": "^[0-9a-f]{8}$" },
            "description": { "type": "string" },
            "summary": { "type": "string" },
            "num_messages_summarized": { "type": "integer", "minimum": 1 }
          } }
      ]
    },
    "WorkflowRecord": {
      "type": "object",
      "required": ["text", "query", "success", "num_steps", "timestamp"],
      "properties": {
        "text": { "type": "string", "pattern": "^Query: [\\s\\S]*\\nSteps:\\n[\\s\\S]*\\nAnswer: " },
        "query": { "type": "string" },
        "success": { "type": "boolean" },
        "num_steps": { "type": "integer", "minimum": 1 },
        "timestamp": { "type": "string", "format": "date-time" }
      }
    },
    "EntityRecord": {
      "type": "object",
      "required": ["name", "type", "description"],
      "properties": {
        "name": { "type": "string", "minLength": 1 },
        "type": { "enum": ["PERSON", "PLACE", "SYSTEM"] },
        "description": { "type": "string" }
      }
    },
    "ToolDefinition": {
      "type": "object",
      "required": ["type", "function"],
      "properties": {
        "type": { "const": "function" },
        "function": {
          "type": "object",
          "required": ["name", "description", "parameters"],
          "properties": {
            "name": { "type": "string", "minLength": 1 },
            "description": { "type": "string" },
            "parameters": {
              "type": "object",
              "required": ["type", "properties", "required"],
              "properties": {
                "type": { "const": "object" },
                "properties": { "type": "object", "additionalProperties": { "type": "object", "required": ["type"], "properties": { "type": { "enum": ["string", "integer", "number", "boolean"] } } } },
                "required": { "type": "array", "items": { "type": "string" }, "uniqueItems": true }
              }
            }
          }
        }
      }
    },
    "ContextUsage": {
      "type": "object",
      "required": ["tokens", "max", "percent", "status"],
      "properties": {
        "tokens": { "type": "integer", "minimum": 0 },
        "max": { "type": "integer", "const": 256000 },
        "percent": { "type": "number", "minimum": 0 },
        "status": { "enum": ["ok", "warning", "critical"] }
      },
      "allOf": [
        { "if": { "properties": { "percent": { "exclusiveMaximum": 50 } } }, "then": { "properties": { "status": { "const": "ok" } } } },
        { "if": { "properties": { "percent": { "minimum": 50, "exclusiveMaximum": 80 } } }, "then": { "properties": { "status": { "const": "warning" } } } },
        { "if": { "properties": { "percent": { "minimum": 80 } } }, "then": { "properties": { "status": { "const": "critical" } } } }
      ]
    },
    "TurnResult": {
      "type": "object",
      "required": ["thread_id", "query", "final_answer", "exhausted", "iterations", "tool_calls", "summaries_created", "context_usage"],
      "properties": {
        "thread_id": { "type": "string", "minLength": 1 },
        "query": { "type": "string" },
        "final_answer": { "type": "string" },
        "exhausted": { "type": "boolean" },
        "iterations": { "type": "integer", "minimum": 1, "maximum": 10 },
        "tool_calls": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "arguments", "status", "log_id"],
            "properties": {
              "name": { "type": "string" },
              "arguments": { "type": "object" },
              "status": { "enum": ["success", "failed"] },
              "log_id": { "type": "string" }
            }
          }
        },
        "summaries_created": { "type": "array", "items": { "type": "object", "required": ["id", "description"], "properties": { "id": { "type": "string", "pattern": "^[0-9a-f]{8}$" }, "description": { "type": "string" } } } },
        "context_usage": { "$ref": "#/$defs/ContextUsage" }
      },
      "if": { "properties": { "exhausted": { "const": true } } },
      "then": { "properties": { "final_answer": { "const": "I was unable to complete the request within the allowed iterations." }, "iterations": { "const": 10 } } }
    }
  }
}
```

**Stores (declared structure).** `CONVERSATIONAL_MEMORY` holds `ConversationMessage` rows; `TOOL_LOG_MEMORY` holds `ToolLogEntry` rows; `SEMANTIC_MEMORY`, `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY` each hold rows of (text, metadata, 768-dimensional embedding). Workflow metadata is a `WorkflowRecord` without `text`; entity metadata is an `EntityRecord`; summary metadata is a `SummaryRecord`; toolbox metadata carries the tool's name, description offered to the model, signature, parameters, return type, `augmented` flag and synthetic queries.

## 4. Business Rules

Labels: *course-demonstrated* (traceable to the materials) or *project hardening* (added by this spec).

- **R1 — Durable, idempotent stores.** Initialization creates any missing store of the seven (row D1) and never drops or empties an existing one; a new process pointed at the same store location sees all earlier memory (CTX-B1). *Project hardening* for the never-drop half — every course notebook drops all seven tables at start for a clean lesson; *course-demonstrated* for persistence across sessions (Lesson 6). → AC1, AC2
- **R2 — Every turn is written.** The user query is written to the conversation store (role `user`, the turn's thread id) after the context is assembled and before the loop; the final answer is written (role `assistant`) after the loop — always, including on iteration exhaustion. Persistence of turns is deterministic, never left to the model (CTX-B1). *Course-demonstrated.* → AC2, AC3, AC4
- **R3 — Partitioned context, assembled deterministically.** Every turn builds, without any model call, a context window: `# Question` with the query, then the five memory segments in the binding order. Each segment opens with its heading, then `### What this memory is` and `### How you should leverage it` guidance for the model, then its retrieved content or an explicit empty-state line: `(No unsummarized messages found for this thread.)`, `(No relevant knowledge base passages found.)`, `(No relevant workflows found.)`, `(No entities found.)`, `(No summaries available for thread <id>.)`. The question is never summarized or offloaded (CTX-A). *Course-demonstrated.* → AC5, AC6
- **R4 — Conversation segment.** Shows only the active thread's messages that carry no summary id, each as `[HH:MM:SS] [role] content`, oldest first, at most the 10 most recent such messages. Messages of other threads never appear. *Course-demonstrated*, except "most recent": the course's query keeps the 10 oldest unsummarized messages — selecting the most recent is *project hardening* (CTX-C7). The limit 10 is a post-build lever, contradicted (the Lesson 5 notebook reads 100 for its monitor test): chosen by the lever-value rule's second branch, the end-to-end application's config. → AC4, AC6, AC7, AC25
- **R5 — Retrieval depths.** Knowledge base: top 3 passages by similarity to the query. Workflow: top 3 stored workflows by similarity, joined by `---` lines (the course also filters to workflows with at least one step). Entity: top 5, each shown as `• <name>: <description>`. Summary: up to 10 summaries of the active thread (row C1), each shown only as `• [ID: <id>] <label>` under a `Scope: thread_id = <id>` line and the instruction to call `expand_summary(id)` — never the summary body. Each depth is a single-valued course setting, a post-build lever. *Course-demonstrated.* → AC8, AC9, AC20, AC26
- **R6 — Tools are retrieved, never dumped.** For each turn the harness offers the model exactly the top 5 tools whose retrieval text is most similar to the query (fewer only when fewer are registered), with duplicate names removed, each as a `ToolDefinition`: parameter types map to JSON types (string, integer, number, boolean; anything else string), and a parameter is required exactly when it has no default. The full registry is never sent (CTX-B2). Bake-in: decided by the litmus — the course narrates "all tools in the prompt" as context bloat and tool-selection degradation, and that side is the limit value at which the retrieval stage ceases to exist, so it is a component choice the course shows failing, not a knob. The number 5 is a post-build lever, contradicted (toolbox-search signature 3, its own description "default: 5", the Lesson 4 demo 1, the Lesson 6 loop 5): the Lesson 4 narration states no value for the agent's toolset, so the lever-value rule's second branch takes the end-to-end application's 5. → AC10, AC11
- **R7 — Tool registration.** A tool is registered with its name, description, signature, parameter info and return type, augmented per row D2: under the default the model (role `augment`) rewrites the description and (role `queries`) writes 5 synthetic queries, and the retrieval text is name + augmented description + signature + the queries. Registering a name already stored writes no second row and makes no model call; the callable is still bound for execution. *Course-demonstrated.* → AC12, AC13
- **R8 — Loop control.** The loop calls the model (role `agent`) with the system prompt, the context and the turn's tools, at most 10 times. A reply without tool calls is the final answer. Each tool call is executed by name against every registered tool: an unknown name yields the result `Error: Tool '<name>' not found`; an exception yields the result `Error: <message>` with status `failed`; an empty result yields `Done`. After 10 iterations without a final answer, the answer is exactly `I was unable to complete the request within the allowed iterations.` (CTX-B7). The cap 10 is a single-valued course setting. *Course-demonstrated.* → AC14, AC15, AC16
- **R9 — Tool output offload.** Every tool call is logged to `TOOL_LOG_MEMORY` in full (thread, call id, name, arguments, untruncated result, 2,000-byte preview, status, error, iteration). The model receives the result unchanged if at most 3,000 characters, otherwise the first 3,000 characters followed by a blank line and `[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <log id>]` (CTX-B6). Values 3,000 and 2,000 are single-valued course settings. *Course-demonstrated.* → AC15, AC17
- **R10 — Context budget.** Usage is estimated as tokens = characters ÷ 4 (integer division) against a 256,000-token window, percent rounded to one decimal; status `ok` below 50, `warning` from 50 to below 80, `critical` from 80. Before the loop, if the assembled memory context's percent is **strictly greater than 80**, the harness offloads it (R11) without asking the model (CTX-B3). Post-build levers: the ratio 4 (spoken lever — Lesson 5 says some models divide by two, some by four, "we're going to use … four"; lever-value rule first branch); the threshold 80 (contradicted — Lesson 6 narration says both "exceeded or is equal to 80%" and "greater than 80%"; the narration conflicts, so the second branch takes the application's strict `> 80`). *Course-demonstrated.* → AC18, AC19
- **R11 — Compaction replaces only the conversation segment.** Offloading summarizes the thread's unsummarized turns (R12), replaces the whole `## Conversation Memory` segment with the stub "Older conversation content was summarized to reduce context size." / "Use Summary Memory references + expand_summary(id) for full detail.", keeps every other segment, and appends `[Summary ID: <id>] <label>` after the summary segment. *Course-demonstrated.* → AC19
- **R12 — Summarization.** Summarizing a thread reads its turns with no summary id in timestamp order, renders each as `[YYYY-MM-DD HH:MM:SS] [ROLE] content` (role upper-cased), sends the first 6,000 characters to the model (role `summary`) asking for exactly four headings — Technical Information, Emotional Context, Entities & References, Action Items & Decisions — keeping concrete details, separating facts from open questions and inventing nothing; then asks (role `label`) for a specific 8–12-word label. A label that is empty or one of "conversation summary", "summary", "chat summary", "thread summary" (any case) is replaced by the first summary line, skipping headings and lines under 4 words, cut to its first 12 words with trailing `,.;:` and spaces removed (else `Recent thread context, decisions, and open actions`). The id is the first 8 characters of a random UUID — 8 lowercase hex digits. The summary store keeps id, thread id (row C1), summary, the full rendered transcript and the label; exactly the rows read are then marked with the id. *Course-demonstrated* (label fallback from the end-to-end helper; the Lesson 5 notebook instead fell back to the generic "Conversation summary" — CTX-C8). → AC19, AC20, AC21, AC22, AC24
- **R13 — Never re-summarize.** Rows carrying a summary id are never read for summarization again; summarizing a thread with none left returns `{"status": "nothing_to_summarize"}` and writes nothing (CTX-B4). *Course-demonstrated.* → AC23
- **R14 — Summaries never come back empty.** If the summary reply is empty the harness retries once with a simpler prompt (four headings, at most 180 words); if still empty it stores a fallback whose Technical Information body is the first 500 characters of the transcript with newlines turned into spaces, and whose other three bodies read `Not available from model output.` (CTX-B9). *Course-demonstrated.* → AC24
- **R15 — Expansion recovers the originals.** `expand_summary(summary_id)` returns `## Summary Context`, the stored summary text, then `## Expanded Conversations for Summary ID: <id>`, `Total messages: <n>`, and every original turn marked with that id, oldest first, each as a `[YYYY-MM-DD HH:MM:SS] [ROLE]` line followed by the content line. An unknown id returns `Summary <id> not found.` and `No conversations found for summary_id: <id>` (CTX-B5). *Course-demonstrated.* → AC25
- **R16 — The summarize tool stays in its thread.** When the model calls `summarize_and_store` without a thread id, the harness supplies the active thread id before executing it; given a thread id the tool summarizes that thread's unsummarized turns (R12) and returns `Stored as [Summary ID: <id>] <label>`, or `No unsummarized messages found for thread <id>.` *Course-demonstrated.* → AC21, AC23
- **R17 — Persistence after the loop.** If the turn made at least one tool call, one workflow is written: text `Query: <query>`, `Steps:`, one `Step <n>: <tool>(<model-supplied arguments>) → success|failed` line per call, `Answer: <first 200 characters of the answer>`, with metadata query, success true, step count and timestamp; a turn without tool calls writes no workflow. Entities (role `entities`; types PERSON, PLACE, SYSTEM; from the first 500 characters) are extracted from the user query before the loop and from the final answer after it; an extraction failure stores nothing and never fails the turn. *Course-demonstrated.* → AC14, AC15, AC26, AC27
- **R18 — One embedding space.** All five similarity stores use the same embedding model (768 dimensions) and the same metric — cosine (§2) — for writes and reads; a changed model or metric is never mixed into an existing store. *Course-demonstrated* (shared model across stores); the metric choice is a post-build lever (§2, CTX-C6). → AC28
- **R19 — Knowledge ingestion.** Each seed record becomes one knowledge-base row whose text is title, subjects and abstract joined by newlines (empty parts dropped) and whose metadata holds id, title, subjects, abstract and submission date; a record with empty title, subjects and abstract is skipped. *Course-demonstrated.* → AC8
- **R20 — Search-and-store, deep ingestion.** A tool that brings in a full document splits it (1,500-character chunks, 200 overlap), writes every chunk to the knowledge base with metadata source, paper id, title, entry id, published date, authors, chunk index, chunk count and ingestion timestamp (UTC), and returns only `Saved <id> to SEMANTIC_MEMORY: <n> chunks (title: <title>).` — never the content (row RR3). Later turns retrieve those chunks from the knowledge segment without the tool. *Course-demonstrated.* → AC29, AC30, AC33
- **R21 — Memory-aware system prompt.** The system prompt names the assistant's role, lists the five segments and what each is for, tells the model to call `expand_summary` before relying on a detail found only in a summary, ranks conflicting sources — the current question, then the latest conversation memory, then knowledge-base evidence, then older summaries and workflows — tells it to start from the segments, use only the tools offered this turn with the fewest calls, say what is missing when memory is insufficient, and compact with `summarize_and_store` using the thread id. *Course-demonstrated* (behavior, not wording). → AC31
- **R22 — Paper candidate search.** `arxiv_search_candidates(query, k=5)` returns a JSON list of at most `k` candidates, each with paper id (the part of the entry URL after `/abs/`), entry id, title, authors, published date and the first 2,500 characters of the abstract; it writes nothing. Retriever settings: up to 8 documents, 4,000 characters each. *Course-demonstrated.* → AC32, AC33
- **R23 — The real model drives the same loop.** With the live provider (row L4) the loop, tool calls, logging and persistence behave exactly as with the scripted model; nothing in the pipeline branches on which model is attached. *Course-demonstrated* (Lesson 6 demo). → AC34

## 5. Acceptance Criteria                ★  (the oracle)

### Fixture corpus (declare first; never modify a fixture to make a test pass)

All facts below are authored for this spec; none is course data.

- **`fixtures/papers.json`** — six records (`arxiv_id`, `title`, `subjects`, `abstract`, `submission_date`):
  1. `fx-0001` · "Tidal Lattice Caching for Lunar Habitat Thermal Control" · "Space Systems" · "A phase-change lattice buffers habitat heat through the fourteen-day lunar night." · 2026-01-10
  2. `fx-0002` · "Sparse Ledger Attention for Long Documents" · "Machine Learning" · "Ledger tokens index long documents so attention cost grows linearly." · 2026-02-03
  3. `fx-0003` · "Mangrove Root Carbon Accounting" · "Ecology" · "Sediment cores estimate the carbon stored in mangrove roots." · 2026-02-17
  4. `fx-0004` · "Queue-Aware Bread Baking Schedules" · "Operations Research" · "Oven schedules for small bakeries that minimise customer queue time." · 2026-03-01
  5. `fx-0005` · "Orbital Debris Nets with Shape-Memory Hinges" · "Space Systems" · "Deployable nets capture orbital debris using shape-memory alloy hinges." · 2026-03-22
  6. `fx-0006` · "" · "" · "" · "" — a planted empty record.
- **`fixtures/long_paper.txt`** — 60 lines; line *n* (01–60) is `Line <nn>: the tidal lattice stores heat by day and releases it by night.` followed by a newline (72 characters per line, 4,320 total).
- **`fixture_data.py`** (importable module) — builds:
  - `OVERFLOW_THREAD`: 10 messages alternating `user`/`assistant`, message *i* (01–10) = `overflow-<ii> ` followed by the letter `a` until the message is exactly 90,000 characters.
  - `LONG_THREAD`: 14 messages alternating `user`/`assistant`, contents `m01` … `m14`.
  - `RESUM_THREAD`: 4 messages: user "Plan the Lisbon trip.", assistant "Booked for May.", user "Add a poster session.", assistant "Added."
  - `MONITOR_STRINGS`: the letter `m` repeated 400,000; 600,000; 819,200; and 820,000 times.
  - `SEVEN_ENTITIES`: seven entity records written directly to the entity store — `Ada Mensah` (PERSON, "lab manager"), `Kofi Boateng` (PERSON, "co-author"), `Accra` (PLACE, "lab city"), `Porto` (PLACE, "workshop city"), `Ledger Index` (SYSTEM, "baseline system"), `Thermal Bench` (SYSTEM, "test rig"), `Lena Ortiz` (PERSON, "reviewer").
- **`fixture_tools.py`** (importable module) — local tools, each with the docstring quoted:
  `get_current_time(detailed: bool = False)` "Returns the current time." (the course's clock tool; detailed adds microseconds) · `count_words(text: str)` "Count the words in a piece of text." · `celsius_to_fahrenheit(celsius: float)` "Convert a temperature from Celsius to Fahrenheit." · `compound_interest(principal: float, rate: float, years: int)` "Compute compound interest on a savings balance." · `reverse_text(text: str)` "Reverse the characters of a string." · `roll_dice(sides: int = 6)` "Roll a die with the given number of sides." · `list_bakery_hours(day: str)` "Look up a bakery's opening hours." (returns "08:00-18:00") · `emit_large_output()` "Fixture: return a 5,000-character block of the letter x." (returns exactly 5,000 `x`) · `always_fails()` "Fixture: always raise an error." (raises a runtime error with message `fixture failure`).
- **Standard registry** — the 9 fixture tools plus `expand_summary`, `summarize_and_store`, `arxiv_search_candidates`, `fetch_and_save_paper_to_kb_db`: 13 tools, registered with the scripted model under row D2's default. No `search_tavily`.
- **`scripted_model.py`** (importable module) — the **scripted stand-in model** (row RR2). Its own description says: "Scripted stand-in for the live model; replies are fixed by the spec; it does not reason." It records every call (role, messages, tools). Replies by role:
  - `augment` → `Augmented: <first non-empty line of the original description> Call this when the task needs <tool name with underscores as spaces>.`
  - `queries` → the JSON array `["<name with spaces> request 1", … , "<name with spaces> request 5"]`.
  - `summary` → normal mode: `### Technical Information` / `Advisor is Dr. Imani Okafor; thesis presents the Tidal Lattice Cache in Lisbon.` / `### Emotional Context` / `Calm and focused.` / `### Entities & References` / `Dr. Imani Okafor (PERSON); Lisbon (PLACE); Tidal Lattice Cache (SYSTEM).` / `### Action Items & Decisions` / `None recorded.` (one per line). Empty mode: `""` on every call.
  - `label` → normal mode: `Advisor Dr. Imani Okafor and Tidal Lattice Cache Lisbon talk`. Generic mode: `Conversation summary`.
  - `entities` → a JSON list with one entry per keyword present in the text: "Okafor" → `{"name": "Dr. Imani Okafor", "type": "PERSON", "description": "the user's thesis advisor"}`; "Lisbon" → `{"name": "Lisbon", "type": "PLACE", "description": "presentation city"}`; "Tidal Lattice" → `{"name": "Tidal Lattice Cache", "type": "SYSTEM", "description": "the user's thesis system"}`; none → `[]`. Raise mode: raises an error.
  - `agent` → by the exact text after `# Question` in the latest user-role message:
    - `Remember that my advisor is Dr. Imani Okafor and I am presenting the Tidal Lattice Cache in Lisbon.` → final `Noted: your advisor is Dr. Imani Okafor.`
    - `Who is my advisor?` → final `Your advisor is Dr. Imani Okafor.`
    - `Summarize the conversation so far using your tool` → iteration 1: call `summarize_and_store` with `{}`; iteration 2: final `Stored the summary.`
    - `What was my first question?` → iteration 1: call `expand_summary` with `{"summary_id": <the first 8 characters after the first "[ID: " in the context>}`; iteration 2: final `Your first question was: ` + the line that follows the first line ending in `[USER]` in the latest tool result.
    - `What time is it?` → iteration 1: call `get_current_time` with `{}`; iteration 2: final `It is <latest tool result>.`
    - `Show me the big output` → iteration 1: call `emit_large_output` with `{}`; iteration 2: final `Done.`
    - `Trigger the failing tool` → iteration 1: call `always_fails` with `{}`; iteration 2: final `The tool failed.`
    - `Call a missing tool` → iteration 1: call `no_such_tool` with `{}`; iteration 2: final `That tool does not exist.`
    - `Loop forever` → every iteration: call `get_current_time` with `{}`.
    - anything else → final `SCRIPTED: no script for this query.`
- **The demo thread `t-demo`** — four turns in order: T1 `Remember that my advisor is Dr. Imani Okafor and I am presenting the Tidal Lattice Cache in Lisbon.`; T2 `Who is my advisor?`; T3 `Summarize the conversation so far using your tool`; T4 `What was my first question?`.
- **Defaults in force** unless a Given says otherwise: a fresh store file per criterion, the standard registry, scripted model in normal modes, every Ledger Default.

| AC | Given | When | Then | Rules |
|---|---|---|---|---|
| AC1 | An empty store location | The memory manager initializes, then initializes again | The seven stores exist with the exact names of row D1; the conversation store has the `ConversationMessage` fields and the tool-log store the `ToolLogEntry` fields; each similarity store accepts text, metadata and an embedding; the second initialization raises nothing and every store is still empty | (R1) |
| AC2 | Process A runs T1 on thread `t-restart` and exits | A new operating-system process opens the same store file and runs `Who is my advisor?` on `t-restart` | The context of process B's first `agent` call contains, in its Conversation Memory segment, `Remember that my advisor is Dr. Imani Okafor`; `t-restart` holds 4 conversation rows | (R1, R2) |
| AC3 | Fresh store | T1 runs on `t-demo` | `t-demo` holds exactly 2 rows: role `user` with the T1 text, then role `assistant` with `Noted: your advisor is Dr. Imani Okafor.`; both have no summary id; timestamps ascend | (R2) |
| AC4 | T1 has run on `t-demo` | T2 runs | The Conversation Memory segment of T2's first `agent` call lists the T1 user message then the T1 assistant message, each as `[HH:MM:SS] [role] content`, and does not contain `Who is my advisor?` | (R2, R4) |
| AC5 | T1 has run on `t-demo` | T2 runs | T2's first `agent` call has the system prompt as its system message, and its user message starts with `# Question` then `Who is my advisor?`, followed by the five segment headings in the binding order, each followed by `### What this memory is` and `### How you should leverage it` | (R3) |
| AC6 | Fresh store, nothing seeded | `What time is it?` runs on `t-empty` | The context shows the five exact empty-state lines of R3 (summary line naming `t-empty`); no summary is created in the turn; the scripted model's first recorded call of the turn has role `entities` or `agent`, never `summary` | (R3, R4) |
| AC7 | `LONG_THREAD` written to `t-long` in order | `Who is my advisor?` runs on `t-long` | The Conversation Memory segment contains `m05` through `m14` in ascending order and none of `m01`–`m04` | (R4) |
| AC8 | `fixtures/papers.json` ingested | `Which paper stores habitat heat through the lunar night?` runs on `t-kb` | `SEMANTIC_MEMORY` holds 5 rows (`fx-0006` skipped); the `fx-0001` row's text is its title, subjects and abstract on three lines and its metadata holds id, title, subjects, abstract, submission date; the Knowledge Base Memory segment contains "Tidal Lattice Caching for Lunar Habitat Thermal Control" and at most 3 passages | (R5, R19) |
| AC9 | T3 has run on four fresh threads `t-w1`…`t-w4` (four workflows); `SEVEN_ENTITIES` written | `What time is it?` runs on `t-w5` | The Workflow Memory segment shows exactly 3 workflows separated by `---` lines; the Entity Memory segment shows exactly 5 lines starting with `• ` | (R5) |
| AC10 | Standard registry (13 tools) | `What is the current date and time?` runs on `t-tools` | The turn's first `agent` call carries exactly 5 tool definitions with unique names, including `get_current_time`, whose parameters are `{"detailed": {"type": "boolean"}}` with `required` empty; a direct toolbox search for `count the words in a text` with depth 1 returns `count_words` with `{"text": {"type": "string"}}` and `required` `["text"]` | (R6) |
| AC11 | Standard registry | `Find papers on arXiv about agent memory` runs on `t-tools` | The first `agent` call's 5 tool definitions include `arxiv_search_candidates`; it never carries all 13 | (R6) |
| AC12 | Standard registry | The toolbox record for `get_current_time` is read | Its offered description is `Augmented: Returns the current time. Call this when the task needs get current time.`; its synthetic queries are `get current time request 1` … `request 5`; its retrieval text contains the name, that description, the signature and all 5 queries; `augmented` is true | (R7) |
| AC13 | Standard registry | `get_current_time` is registered again | `TOOLBOX_MEMORY` still holds exactly 1 row named `get_current_time`; the scripted model records no `augment` or `queries` call for the second registration; `What time is it?` still executes the tool | (R7) |
| AC14 | Standard registry | `Loop forever` runs on `t-loop` | Exactly 10 `agent` calls are recorded; `TOOL_LOG_MEMORY` holds 10 rows for `t-loop`; the `TurnResult` has `exhausted` true, `iterations` 10 and the fixed exhaustion answer, which is also the stored assistant message; one workflow is written with step count 10 | (R8, R17) |
| AC15 | Standard registry | `Trigger the failing tool` runs on `t-fail` | The tool log row has status `failed` and error message `fixture failure`; the tool message sent on iteration 2 is `Error: fixture failure`; the workflow text contains `Step 1: always_fails({}) → failed`; the answer is `The tool failed.` | (R8, R9, R17) |
| AC16 | Standard registry | `Call a missing tool` runs on `t-missing` | The tool message sent on iteration 2 is `Error: Tool 'no_such_tool' not found`; the answer is `That tool does not exist.` | (R8) |
| AC17 | Standard registry | `Show me the big output` runs on `t-big` | The tool log row's result is 5,000 characters and its preview 2,000; the tool message sent on iteration 2 is the first 3,000 `x` characters, a blank line, then `[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: <that row's id>]` | (R9) |
| AC18 | `MONITOR_STRINGS` | Usage is measured for each, and the automatic-offload decision is evaluated for the last two | Results: 100,000 tokens / 39.1 / `ok`; 150,000 / 58.6 / `warning`; 204,800 / 80.0 / `critical`; 205,000 / 80.1 / `critical`; max 256,000 each; offload decision false for 819,200 characters and true for 820,000 | (R10) |
| AC19 | `OVERFLOW_THREAD` written to `t-overflow` | `What time is it?` runs on `t-overflow` | Before the first `agent` call one summary is created with thread `t-overflow` and all 10 seeded rows carry its id; the first `agent` call's context contains the two stub lines, no `overflow-01`, all of the Knowledge Base, Workflow, Entity and Summary Memory headings, and ends with `[Summary ID: <id>] Advisor Dr. Imani Okafor and Tidal Lattice Cache Lisbon talk`; usage of that context is under 1 percent; `summaries_created` lists the id | (R10, R11, R12) |
| AC20 | T1–T3 have run on `t-demo` | `Who is my advisor?` runs on `t-other`, then T4 runs on `t-demo` | `t-other`'s Summary Memory segment shows `(No summaries available for thread t-other.)` and not the `t-demo` id; T4's Summary Memory segment shows `Scope: thread_id = t-demo` and `• [ID: <id>] Advisor Dr. Imani Okafor and Tidal Lattice Cache Lisbon talk`; the `t-other` Conversation Memory segment shows the no-messages line | (R5, R12) |
| AC21 | T1–T2 have run on `t-demo` | T3 runs | `summarize_and_store` executes with thread `t-demo` although the model passed `{}`; exactly 5 rows (T1 user, T1 assistant, T2 user, T2 assistant, T3 user) are marked with one id matching `^[0-9a-f]{8}$`; the tool message is `Stored as [Summary ID: <id>] Advisor Dr. Imani Okafor and Tidal Lattice Cache Lisbon talk`; the summary record holds thread `t-demo`, the scripted normal summary, and full content whose first line matches `^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] \[USER\] Remember that my advisor` | (R12, R16) |
| AC22 | `RESUM_THREAD` written to `t-label`; label mode generic | The thread is summarized | The stored label is `Advisor is Dr. Imani Okafor; thesis presents the Tidal Lattice Cache in` (12 words), not `Conversation summary` | (R12) |
| AC23 | `RESUM_THREAD` written to `t-resum` | The thread is summarized twice, then `summarize_and_store` is called with thread `t-resum` | The first summarization marks 4 rows; the second returns `{"status": "nothing_to_summarize"}`; the tool returns `No unsummarized messages found for thread t-resum.`; `SUMMARY_MEMORY` holds exactly 1 row | (R13, R16) |
| AC24 | `RESUM_THREAD` written to `t-empty-sum`; summary mode empty | The thread is summarized | Exactly 2 `summary` calls are recorded; the stored summary has the four headings, contains `Not available from model output.` exactly 3 times, and its Technical Information body equals the first 500 characters of the rendered transcript with newlines replaced by spaces | (R12, R14) |
| AC25 | T1–T3 have run on `t-demo` | T4 runs; then `expand_summary` is called with `ffffffff` | T4's Conversation Memory segment contains `Stored the summary.` and not the T1 text; `expand_summary` runs with the T3 summary id; its result contains `Total messages: 5` and the five turns oldest first; the answer is `Your first question was: Remember that my advisor is Dr. Imani Okafor and I am presenting the Tidal Lattice Cache in Lisbon.`; the unknown-id call returns `Summary ffffffff not found.` and `No conversations found for summary_id: ffffffff` | (R4, R15) |
| AC26 | Fresh store | T1, T2, T3 run on `t-demo`, then T4 | After T2 `WORKFLOW_MEMORY` is empty; after T3 it holds 1 workflow whose text contains `Query: Summarize the conversation so far using your tool`, `Step 1: summarize_and_store({}) → success` and `Answer: Stored the summary.`, with step count 1 and success true; T4's Workflow Memory segment contains `summarize_and_store` | (R5, R17) |
| AC27 | Fresh store | T1 then T2 run on `t-demo`; separately, with entities mode raise, T1 runs on `t-ent` | `ENTITY_MEMORY` holds entries typed PERSON (`Dr. Imani Okafor`), PLACE (`Lisbon`) and SYSTEM (`Tidal Lattice Cache`); T2's Entity Memory segment contains `• Dr. Imani Okafor: the user's thesis advisor`; in raise mode T1 still answers `Noted: your advisor is Dr. Imani Okafor.`, `t-ent` holds 2 rows and no entity is stored | (R17) |
| AC28 | `fixtures/papers.json` ingested; T3 has run on `t-demo` | The five similarity stores are inspected | All five report the same embedding model name and the cosine metric; every stored embedding has 768 numbers | (R18) |
| AC29 | Fresh store | The fetch-and-save tool's store step runs on `fixtures/long_paper.txt` with id `fx-long` and title `Tidal Lattice Long Form`; then `How does the tidal lattice store heat by day?` runs on `t-ingest` | It writes *n* ≥ 3 rows, each at most 1,500 characters, chunk indexes 0…*n*−1, chunk count *n* on every row; the first line of each chunk after the first also appears in the chunk before it; it returns `Saved fx-long to SEMANTIC_MEMORY: <n> chunks (title: Tidal Lattice Long Form).`; the turn's Knowledge Base Memory segment contains `the tidal lattice stores heat by day` | (R20) |
| AC30 | Standard registry under every Ledger Default | The registry is listed | It holds exactly the 13 standard tools and no `search_tavily` | (R20) |
| AC31 | — | The system prompt is read | It names the five segments, instructs `expand_summary` before relying on a detail found only in a summary, ranks the current question over the latest conversation memory over knowledge-base evidence over older summaries and workflows, and instructs `summarize_and_store` with the thread id | (R21) |
| AC32 `live` | Network access | `arxiv_search_candidates("MemGPT", 5)` | It returns a JSON list of 1–5 objects; every paper id matches `^\d{4}\.\d{4,5}(v\d+)?$`; every abstract is at most 2,500 characters; `SEMANTIC_MEMORY` row count is unchanged | (R22) |
| AC33 `live` | Network access | `fetch_and_save_paper_to_kb_db("2310.08560")` | It returns a string starting `Saved 2310.08560 to SEMANTIC_MEMORY:`; at least 1 knowledge row carries paper id `2310.08560` and source `arxiv` | (R20, R22) |
| AC34 `live` | OpenAI key set; row L4's provider attached; standard registry | `Can you get me the paper MemGPT`, then `Can you save the content of the paper`, then `What are the main key takeaways from the paper` run on `live-1` | Turn 1's tool log includes `arxiv_search_candidates`; turn 2's includes `fetch_and_save_paper_to_kb_db` with a paper id matching the pattern of AC32; turn 3 returns a non-empty answer; `live-1` holds 6 conversation rows | (R23) |

Ledger coverage: L4 → AC21, AC34; L5 → AC2; D1 → AC1; D2 → AC12; D3 → AC6, AC19, AC21; D4 → AC25; RR1 → AC1, AC2, AC28; RR2 → every offline criterion (e.g. AC21); RR3 → AC29, AC30; C1 → AC20. L1–L3 and L6 have empty invariants; L6's default is exercised by building the whole set.

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the offline suite after every change that touches a rule, and report per criterion.
- Keep fixtures, the scripted model's script and the binding names exactly as §5 and §3 declare them.
- Label any behavior you add beyond this spec as project hardening in the README.
- Read keys from the environment only.

**Ask First** (derived from the course's argued trade-offs, CTX-C3 table)
- Changing the memory-operation trigger assignment after the build (row D3) — it moves ownership between harness and model without necessarily failing a criterion.
- Switching to lossy summarization (row D4) — discards originals irreversibly.
- Turning tool augmentation off, or changing its prompt, after tools are registered (row D2) — every toolbox row must be re-registered and re-embedded.
- Changing the toolset size 5 (R6) — changes what the model can choose from without failing a criterion when kept small.
- Changing the characters-per-token ratio or the 80 percent offload threshold (R10) — moves when automatic compaction fires.
- Changing the embedding model or the metric once any similarity store holds data (R18, §2) — forces re-embedding and re-indexing every store.
- Changing summary scoping once summaries exist (row C1) — existing summaries become invisible or leak across threads.
- Changing the store realization or topology once data exists (rows RR1, D1) — forces a migration.
- Changing chunk size or overlap after papers are ingested (R20) — forces re-ingestion.

**Never**
- Invent provenance or citations, in code comments, docs or answers.
- Answer from a summary's label when the detail needed is only in the originals — expand first (R21); when memory lacks the answer, say what is missing instead of guessing.
- Modify a fixture or the scripted model's script to make a test pass.
- Commit secrets, `.env` files or the store file.
- Drop or empty stores at startup (R1).
- Send the whole tool registry to the model (R6).
- Mark conversation rows summarized without storing the summary they point to (R12).

## 7. Test Plan & Self-Verification

Commands, from the project root:

1. Install: `python -m pip install -e ".[test]"` (dependencies per §2).
2. One-time embedding-model download (needs network once; later runs are offline): `python -c "from sentence_transformers import SentenceTransformer as S; S('sentence-transformers/paraphrase-mpnet-base-v2')"`.
3. Offline suite (the completion bar): `python -m pytest -m "not live" -q`.
4. Live suite (only with keys): `OPENAI_API_KEY=… python -m pytest -m live -q`.
5. Manual smoke: start the terminal chat on thread `demo`, run T1–T4 of §5 with the live model, quit, restart, and ask `What was my first question?` again.

The building agent MUST report results **per acceptance criterion** — AC id, pass/fail, and cited evidence (the test name and its output line, or the file path and value inspected). "Should pass" or "looks correct" counts as a failure: it means the criterion was not run. Live criteria not run for lack of a key are reported as "not run (no key)", never as passed.

## Course Context Pack (embedded — agent-readable)

### CTX-A. The pattern

`memory core (persistent stores per memory type) → memory manager (read/write per type) → toolbox (tools as searchable procedural memory) → assemble partitioned context (deterministic reads) → check budget (compact if over) → select tools by similarity → record the user turn → agent loop (model + tool calls, tool output offloaded) → persist (workflow, entities, answer) → expand summaries on demand`

- **Memory core** — memory lives outside the model in a database, the component that sees the most data traffic; this is what turns a stateless agent into one that persists across sessions (Lessons 2–3).
- **Memory manager** — one abstraction over every store, so the loop calls read/write per memory type instead of touching storage (Lesson 3).
- **Memory types** — conversational (episodic, exact by thread, time-ordered), knowledge base (semantic), workflow (procedural: past step sequences and outcomes), toolbox (procedural: tool definitions), entity (people, places, systems), summary (compressed older context), tool log (raw tool audit trail) (Lessons 2–3, 5).
- **Toolbox** — tools are stored with embeddings and retrieved per query so the model sees a focused toolset, which lets the registry grow to hundreds of tools (Lesson 4).
- **Partitioned context** — markdown headings label each memory segment and tell the model what it is and how to use it; models read this hierarchy well because such structure is common in their training data (Lesson 6). This plus memory operations as tools makes the agent *memory-aware* (Lesson 3).
- **Agent loop** — assemble context, invoke the model, act (respond or call tools), repeat until a final answer or the iteration cap (Lesson 6). Memory operations outside the loop are the harness; inside it, the model triggers them.
- **Context reduction** — monitor usage; above the threshold, compact: summarize, keep originals in the database under the summary id, leave a reference and an expand tool (Lesson 5).

### CTX-B. Failure-mode catalog

- **B1 Stateless forgetting** (Lesson 2) — symptom: on a follow-up ("book the first one") the agent has no recollection of the earlier turn. Cause: no interaction history persisted or loaded. Fix: persist every turn and load the thread's history deterministically every turn — the agent cannot choose to look up what it does not know exists. Enforced by R1, R2, R4 / AC2, AC3, AC4.
- **B2 Tool overload** (Lesson 4) — symptom: context bloat, the model picks the wrong tool, latency and token cost rise. Cause: every tool definition in the prompt. Fix: retrieve the top tools by similarity. Enforced by R6 / AC10, AC11.
- **B3 Context overflow** (Lesson 5 notebook) — symptom: the agent fails once the context exceeds the window. Cause: unbounded history. Fix: estimate usage every turn and compact above 80 percent. Enforced by R10, R11 / AC18, AC19.
- **B4 Re-summarization** (Lesson 5 notebook) — symptom: the same turns are summarized again on every pass. Cause: summarized rows not marked. Fix: mark exactly the rows read with the summary id; read only unmarked rows. Enforced by R13 / AC23.
- **B5 Lost detail** (Lesson 5) — symptom: a summary drops a needed exact detail and the original is gone. Cause: lossy summarization. Fix: keep originals, reference them by id, expand on demand. Enforced by R12, R15 / AC21, AC25.
- **B6 Tool-output bloat** (Lesson 6) — symptom: one large tool result floods the next model call. Cause: raw output routed back into context. Fix: log the full result, pass a bounded excerpt with a pointer. Enforced by R9 / AC17.
- **B7 Runaway loop** (Lesson 6) — symptom: the loop never reaches a final answer. Cause: no stop condition besides the answer. Fix: cap iterations and return a fixed message. Enforced by R8 / AC14.
- **B8 Invisible summaries** (course contradiction) — symptom: a summary exists but never appears in the summary segment. Cause: the Lesson 5 notebook writes summaries with no thread id while the Lesson 6 loop reads summaries filtered by thread. Fix: write and read with the same scope (row C1). Enforced by R5, R12 / AC20.
- **B9 Empty or generic summaries** (end-to-end helper) — symptom: an empty summary or a label like "Conversation summary" that cannot tell summaries apart. Cause: the model returns nothing or a generic label. Fix: retry, deterministic fallback, reject generic labels. Enforced by R12, R14 / AC22, AC24.

### CTX-C. Decision background

**How to read the provenance notes.** A *litmus branch* records how an argued subject was disposed of: **row** (the course showed both sides working and they differ in a component, an identity or a role — so the learner chooses), **bake-in** (the course showed or warned the other side failing — the taught side became a business rule), or **lever** (the sides differ only in a value — the value is a body default). The deciding test is named beside each. A *limit value that removes a component* (a toolset of "everything" removes tool retrieval) is treated as a component choice, not a value. A *post-build lever* is a value set once and tunable after the build, never asked at the gate. When the course set a lever inconsistently, the *lever-value rule* picks it: first, the value the narration states aloud in the lesson that introduces the concept; second, if the narration names none or conflicts, the end-to-end application's config; third, the value used most often, earliest-taught on ties. The *stakes test* asks whether picking the other side of a contradiction at first build would change structure, semantics or a guarantee — if yes it is a Ledger row, if no a lever. A *substitution row* has a Default that departs from the course's technology because that technology is *heavy* — it needs a credential, a paid account, admin- or container-level setup, or special hardware; mere network access is not heavy. "Lightest" is decided by *realization tier*: (1) ships with the language, (2) an embedded library installed by the package manager, (3) a locally served component in its own process — the lowest tier that meets the row's Invariant at the spec's declared scale. *(course default)* marks the option the course actually used; *project hardening* marks behavior this spec adds; `[bracketed]` values are learner intake with defaults; *live* criteria need a key or network and sit outside the offline suite; the *scripted model* is a declared fake model.

**C1 Store layout (→ Ledger D1).** The course keeps conversation and tool logs in plain tables because they need exact retrieval by thread id and time order, "not similarity search" (Lesson 3 notebook); every other memory type gets its own vector table, all sharing one embedding model. Course store names (binding here): `CONVERSATIONAL_MEMORY`, `SEMANTIC_MEMORY` (knowledge base), `WORKFLOW_MEMORY`, `TOOLBOX_MEMORY`, `ENTITY_MEMORY`, `SUMMARY_MEMORY`, `TOOL_LOG_MEMORY`. The conversation table indexes thread id and timestamp; the tool-log table indexes thread id, tool name and timestamp.

**C2 Trigger assignment (→ Ledger D3).** The Lesson 3 notebook's classification table marks reads of conversation, knowledge base, workflow and entity deterministic; summary-context read agent-triggered; conversation and workflow writes deterministic; entity write agent-triggered; web search, summary expansion and summarize-and-store agent-triggered; toolbox search both. The Lesson 6 loop instead reads the summary context and writes entities every turn and offers toolbox search only to the harness. Lesson 6 also runs summarization both ways: automatically above 80 percent and as a tool. The default follows Lesson 6.

**C3 Mined trade-off table.** Every spoken or notebook-argued trade-off, with its disposition.

| # | Subject | Lesson | Disposition |
|---|---|---|---|
| T1 | Stateless → memory-augmented → memory-aware agent | 2, 3 | narrative — a maturity story the course uses as framing, not a choice the builder makes |
| T2 | Conversation history alone vs. multiple memory types | 2 | narrative — the same maturity story ("naive" memory-augmented agent → fully memory-augmented) |
| T3 | Short-term (semantic cache, working memory) vs. long-term (procedural, semantic, episodic) memory | 2 | narrative — a taxonomy |
| T4 | Retrieval strategies: lexical, vector, graph traversal, hybrid | 3 | narrative — a taxonomy; hybrid and graph are §1 items |
| T5 | Conversation in an exact-key table vs. a similarity store | 3 (notebook), 5 | bake-in into row D1's Invariant — litmus: a similarity-searched conversation store is never shown working |
| T6 | Deterministic vs. agent-triggered memory operations | 3, 6 | row D3 |
| T7 | All tools in the prompt vs. similarity-retrieved toolset | 4 | bake-in R6 — tie-breaker 1 (warned failure: tool-selection degradation, bloat); "all tools" is the limit value that removes retrieval, so the litmus decides it, not the value rule |
| T8 | How many tools to retrieve ("typically 3-5"; providers advise 10–20 at most; "test with different values of K") | 4 | lever R6 — tie-breaker 2 (the sides differ only in a number) |
| T9 | Augmented vs. raw tool descriptions | 4 | row D2 |
| T10 | Local vs. third-party tool implementations | 4 | narrative — presented without an argued trade-off; the keyed consequence is handled by row RR3 |
| T11 | Lossy summarization vs. recoverable compaction | 5 | row D4 |
| T12 | Characters per token: divide by two or by four | 5 | lever R10 — tie-breaker 2 |
| T13 | Summary prompt wording ("try different prompts") | 5 | narrative — an invitation to experiment, not an argued choice; the four-heading output is baked into R12 |
| T14 | Full tool output in context vs. logged output with a bounded excerpt | 6 | bake-in R9 — litmus: full output in context appears only as the bloat being prevented |
| T15 | Routing a full fetched paper through the model vs. storing it directly | 4 (notebook) | bake-in R20 — litmus: routing through the model is never shown working |
| T16 | Approximate index type HNSW vs. IVF | 3 (notebook, helper docstring) | bake-in inside RR1's course option — tie-breaker 1 (the helper records HNSW raising errors on the free database edition) |
| T17 | Workflow memory: reuse recorded steps vs. work them out each time | 5 | narrative — a benefit statement with no alternative argued; workflow persistence is R17 |
| T18 | Summary scope: thread vs. global | 5, 6 (contradiction) | row C1 |
| T19 | Cosine vs. Euclidean distance | 3–6 (contradiction) | lever R18 — stakes test failed (no box, owner or guarantee changes); first branch of the lever-value rule |
| T20 | Chunking with "a little bit of overlap" vs. none | 4 | lever R20 — tie-breaker 2 (chunk size 1,500 and overlap 200 are values) |
| T21 | The same embedding model at ingestion and query vs. different models | 2 | bake-in R18 — litmus: mismatched models are never shown working |

Ask First (§6) walks T6 (row D3), T8 (R6), T9 (row D2), T11 (row D4), T12 (R10), T18 (row C1), T19 and T21 (metric and embedding model, R18), T5 and T16 (store topology and realization, rows D1 and RR1), and T20 (chunk sizes, R20).

**C4 Augmentation in code vs. narration (→ Ledger D2).** Lesson 4 narrates encoding the enhanced name and description into the embedding. The course's registration computes that embedding but stores the vector row from the raw "name, description, signature" text and keeps the augmented embedding only in metadata, so its retrieval runs on raw text while the model is offered the augmented description. This spec follows the narration (R7). Per-tool flags also differ: the clock tool is augmented in the Lesson 4 notebook and raw in the end-to-end helper.

**C5 Store realization (→ Ledger RR1).** The course runs Oracle AI Database 26ai in a local container, connects as a `VECTOR` user created by an admin connection with an ASSM tablespace, and builds each vector store with LangChain's Oracle integration. Its notebook prose promises HNSW indexing; its index helper builds IVF ("neighbor partitions", target accuracy 95) because HNSW hit internal errors and vector-memory limits on the free edition. The course's demo database password is a local credential and is deliberately not carried here.

**C6 Distance metric (→ §2, R18).** Cosine: Lesson 3 and 4 notebook store setup; Lesson 3 narration ("which in this case is going to be cosine"). Euclidean: Lesson 5 and 6 notebook store setup and the Lesson 3 notebook's component list. The Lesson 5 and 6 notebooks drop every table first "to guarantee … consistent distance strategy" — the course itself treats mixing metrics in one store as wrong, which R18 keeps.

**C7 Conversation window (→ R4).** The course reads unsummarized thread messages oldest first and keeps the first 10, so in a long unsummarized thread the newest turns fall out of view; its prompt calls the segment "recent" dialogue. This spec keeps the 10 most recent (project hardening). The Lesson 5 notebook passes 100 for its monitor test; the agent loop uses the default 10.

**C8 Summarization sources (→ R12, R14).** The Lesson 5 notebook's summarizer and the end-to-end helper share the four-heading prompt, 6,000-character input cap, retry and fallback; they differ in the label: the notebook falls back to "Conversation summary", the helper forbids generic labels and derives one from the summary. The end-to-end application (Lesson 6) loads the helper's version.

**C9 Other values carried.** Entity extraction prompt reads the first 500 characters and skips text under 5 characters. Summary model calls allow up to 4,000 completion tokens (label: 2,000). The paper fetch tool returns a not-found or empty-text message instead of raising. Course thread ids in demos: `"50000"`; default `"1"`. The course's sample research conversation is 32 messages (the notebook comment says 30; the narration says 32) — replaced here by authored fixtures. The course's knowledge seed streamed 100 records (row L2). Read-by-id summary lookups search with depth 5 under an id filter. Declared drops (presentation or course-environment only, carried nowhere else): the connection program label, the connection retry count and delay, the hybrid-search preference name, the per-store vector-index names, the 0.05-second pause between seeded messages, the tool-log reader's default of 20 (it has no caller), and the course's demo database password.

### CTX-D. Perishable assumptions

Treat every name below as a search keyword against current documentation, not a guaranteed import. The concepts in CTX-A to CTX-C are durable; only these names are perishable.

- Model names: `gpt-5-mini` (agent loop and Lesson 5 summarizer), `gpt-5` (toolbox augmentation, entity extraction, end-to-end helper summarizer); window table entries `gpt-5-mini: 256000`, `gpt-5: 256000`, fallback 128,000.
- **Request-parameter compatibility:** the course's calls pass `max_completion_tokens` (not `max_tokens`) and never set `temperature`; tool calls use `tools` with `tool_choice: "auto"` and `role: "tool"` result messages. Parameter support differs by model family and changes over time — check it before the first live run.
- LangChain: `OracleVS` (`langchain_oracledb.vectorstores`), `OracleVectorizerPreference` (`langchain_oracledb.retrievers.hybrid_search`), `DistanceStrategy` (`langchain_community.vectorstores.utils`), `HuggingFaceEmbeddings` (imported from both `langchain_huggingface` and `langchain_community.embeddings` across lessons), `ArxivRetriever`, `ArxivLoader` (`langchain_community`), `RecursiveCharacterTextSplitter` (`langchain_text_splitters`).
- Other packages: `oracledb`, `sentence-transformers`, `datasets` (`load_dataset(..., streaming=True)`), `tavily` (`TavilyClient`), `openai` (`OpenAI().chat.completions.create`), `python-dotenv`, `arxiv`, `pymupdf`, `pydantic`.
- Database: Oracle AI Database 26ai, Oracle Free container at `127.0.0.1:1521/FREEPDB1`; error codes the course handles — ORA-00942 (table missing), ORA-00955 (index exists), ORA-43853 (JSON column needs ASSM tablespace), ORA-51962 (vector memory full), ORA-00600 and ORA-51928 (HNSW issues).
- Dataset: `nick007x/arxiv-papers` on Hugging Face.

### CTX-E. Provenance map

Lesson numbers follow the transcripts. The notebook files are numbered one lower (`L2.ipynb` is Lesson 3, … `L5.ipynb` is Lesson 6), and the dump's own lesson map pairs each file with the lesson after its content — content and transcripts decide here. Slides: the course's decks were supplied only as images with no descriptions file, so no slide was read. Nothing in this spec requires platform access.

| Lesson (transcript) | Notebook | Feeds |
|---|---|---|
| 1 Introduction | — | CTX-A framing |
| 2 Why AI Agents Need Memory | — | CTX-A memory core and types; CTX-B1; C3 T1–T3 |
| 3 Constructing The Memory Manager | `L2.ipynb` | CTX-A manager; C1, C2, C5, C6; C3 T4–T6, T16; R1, R3, R19 |
| 4 Scaling Agent Tool Use with Semantic Tool Memory | `L3.ipynb` | CTX-A toolbox; CTX-B2; C4; C3 T7–T10, T15; R6, R7, R20, R22 |
| 5 Memory Operations: Extraction, Consolidation, and Self-Updating Memory | `L4.ipynb` | CTX-A reduction; CTX-B3–B5, B9; C7, C8; C3 T11–T13, T17–T18; R10–R16 |
| 6 Memory Aware Agent | `L5.ipynb`, helper module | CTX-A loop; CTX-B6–B8; C2; C3 T14, T18; R2–R5, R8, R9, R17, R21, R23 |
| 7 Conclusion | — | CTX-A ("persists across sessions") |

---

v1 · Agent Memory: Building Memory-Aware Agents · learner project: `[project]` (default: terminal research assistant) · Living document: when the build agent produces something unexpected, add the missing constraint here and re-run.
