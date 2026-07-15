# Spec: Chat-with-Your-Documents — Standalone Takeaway

> **This file is self-contained.** The Course Context Pack at the bottom carries the
> course's transferable knowledge as concepts and decisions; you do not need access
> to the original notebooks, transcripts, or any deeplearning.ai platform to build
> from this spec. Course-derived knowledge is anchored as `(CTX-X)`; learner-supplied
> values are written `[in brackets]`. Generated from the *LangChain: Chat with Your
> Data* (DeepLearning.AI × LangChain) notebooks + transcripts on 2026-06-17.

## Complete before handoff

These are learner-intake slots. Defaults are provided so the spec is buildable and
evaluatable as-is; replace each slot when applying to a real project.

- `[learner_corpus]` — the real document set. **Default for build-from-spec runs:
  the synthetic fixture corpus defined in §5.** Do not substitute the fixtures
  with arbitrary other data when running the acceptance criteria; the failure
  modes the course demonstrates are encoded in *those specific* fixture files.
- `[deployment_surface]` — CLI? notebook? Panel UI? Web service? **Default: a
  Python CLI plus a minimal Panel UI**, mirroring the course's end-to-end chatbot
  shape (Lesson 7) without prescribing it as the only surface.
- `[llm_provider]` — model + provider. **Default: OpenAI `gpt-4o-mini` (chat) and
  OpenAI `text-embedding-3-small` (embeddings).** The course used `gpt-3.5-turbo`
  + `text-embedding-ada-002`; those names are perishable (CTX-D) and have been
  superseded.
- `[secrets_store]` — where API keys live. **Default: `.env` loaded via
  `python-dotenv`**, exactly as the course did. Never commit; never hardcode.

---

## 1. Objective

Build a chatbot that answers questions about a corpus of user-supplied documents
by retrieving relevant chunks and grounding the LLM's answer in them, while
preserving conversational history across turns. The pipeline is the course's
six-stage shape: **load → split → embed+store → retrieve → generate → converse**
(CTX-A).

The system MUST: (i) ingest documents from at least two source types; (ii) chunk
them with overlap; (iii) embed and persist them in a vector store; (iv) retrieve
context for a query using a method that handles diversity and metadata
specificity (CTX-B1, CTX-B2); (v) generate a grounded answer that abstains when
unsure (CTX-B5); (vi) maintain multi-turn chat history so follow-ups resolve
correctly (CTX-B4).

### Not Included ★

- **No fine-tuning.** Retrieval-augmented only. The course explicitly contrasts
  RAG with fine-tuning and stays on RAG.
- **No multi-tenant access control / row-level security** over the vector store.
- **No agentic tool use, function calling, web search, or code execution** during
  question answering. The system answers from retrieved chunks or abstains.
- **No long-running orchestration** (queues, schedulers, cron-driven re-ingest).
  Re-ingest is an explicit, on-demand operation invoked by the operator.
- **No automatic citation invention.** If the system does not find evidence in
  retrieved chunks, it MUST abstain (see §6 Never).
- **No image/audio modality at query time.** The course uses Whisper to load
  YouTube audio *during ingestion*; querying remains text-only.
- **No production hardening** (rate limits, observability dashboards, auth, PII
  scrubbing). These are out of scope for the takeaway.

---

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language runtime | Python 3.11 | The course's notebooks ran in CPython; no async/threading required. |
| Orchestration | `langchain` ≥ 0.3, `langchain-community`, `langchain-openai`, `langchain-chroma`, `langchain-text-splitters` | The course used the pre-1.0 namespace (e.g. `langchain.document_loaders`, `langchain.embeddings.openai`); installs in the notebooks were **unpinned** (`pip install langchain` with no version). Treat the course's import paths as **search keywords**, not guaranteed imports — see CTX-D. |
| LLM | OpenAI `gpt-4o-mini`, `temperature=0` `[llm_provider]` | The course used `gpt-3.5-turbo` (or date-conditional `gpt-3.5-turbo-0301`) with `temperature=0`; the *temperature=0* choice is the durable rationale (factual, low-variance) and stays. |
| LLM for retriever-side reasoning (self-query, compression extractor) | OpenAI `gpt-4o-mini`, `temperature=0` | The course originally used `text-davinci-003`; that model was deprecated 2024-01-04 and the notebook itself states the replacement was `gpt-3.5-turbo-instruct`. Either is now superseded by chat models. |
| Embeddings | OpenAI `text-embedding-3-small` | The course used the implicit default of `OpenAIEmbeddings()` (era: `text-embedding-ada-002`). Use `3-small` unless the learner intake specifies otherwise. |
| Vector store | Chroma, persisted to disk at `./.vector_store/` | Matches the course's `persist_directory='docs/chroma/'`. The course ran `!rm -rf ./docs/chroma` before re-creating; do **not** copy that — see Project Hardening in §4 R7. |
| Document loaders | PDF (`PyPDFLoader`), Markdown / plain text, URL (`WebBaseLoader`) | The course demos five loaders (PDF, YouTube via Whisper, URL, Notion, generic). Required minimum: PDF + Markdown/text. URL/Notion/YouTube are optional capabilities; if added they MUST follow the same Document(content, metadata) shape (CTX-A). |
| Splitter | `RecursiveCharacterTextSplitter` with `chunk_size=1500`, `chunk_overlap=150` | Provenance: this is the **end-to-end app config from Lesson 4 (notebook `03_vectorstores_and_embeddings.ipynb`, cell with `chunk_size=1500, chunk_overlap=150`)**. The course's chatbot in Lesson 7 (`load_db`) used `1000/150` instead; that is an alternative, NOT a contradiction (CTX-C2). Earlier lessons demonstrated `26/4`, `450/0`, `150/0` — those are pedagogical, not application configs. Never call any value "the course default" — there are several. |
| Conversation chain | `ConversationalRetrievalChain` (or LCEL equivalent) + `ConversationBufferMemory(memory_key="chat_history", return_messages=True)` | The shape — *condense follow-up + history into a stand-alone question, then retrieve, then answer* — is the durable concept (CTX-A, CTX-B4). The class name is perishable (CTX-D). |
| UI (default) | Python CLI (`python -m chat_with_your_data`) + optional Panel notebook | The course built a Panel/param GUI in Lesson 7. CLI is sufficient for ACs; Panel is optional. |
| Secrets | `.env` + `python-dotenv` `[secrets_store]` | API keys MUST come from environment. Never hardcoded. Never committed. |

---

## 3. Input/Output Contracts ★

The chatbot MUST expose a single core call. Encode invariants in the schema; do
not rely on prose elsewhere to enforce them.

```yaml
# JSON Schema (draft-2020-12) — the core query contract
$schema: https://json-schema.org/draft/2020-12/schema
title: ChatTurnRequest
type: object
required: [question]
additionalProperties: false
properties:
  question:
    type: string
    minLength: 1
  chat_history:
    type: array
    description: Prior turns, oldest-first. May be empty for a fresh conversation.
    items:
      type: object
      required: [role, content]
      additionalProperties: false
      properties:
        role: { enum: [user, assistant] }
        content: { type: string }
  retrieval:
    type: object
    additionalProperties: false
    properties:
      k: { type: integer, minimum: 1, maximum: 10, default: 4 }
      strategy:
        enum: [similarity, mmr, self_query, compression]
        default: mmr
      metadata_filter:
        description: Optional pre-filter applied to vector store metadata.
        type: object
```

```yaml
title: ChatTurnResponse
type: object
required: [answer, citations, retrieval_strategy]
additionalProperties: false
properties:
  answer:
    type: string
  citations:
    type: array
    description: Source spans actually used to ground the answer. MUST be empty when grounded=false.
    items:
      type: object
      required: [source]
      additionalProperties: false
      properties:
        source: { type: string, description: "e.g. 'expenses.md', 'lecture-03.md#p2'" }
        chunk_excerpt: { type: string }
  grounded:
    type: boolean
    description: |
      true iff retrieved chunks supplied the facts in `answer`. When false, `answer`
      MUST express abstention (e.g. "I don't know based on the documents provided")
      and `citations` MUST be empty (R5, AC5).
  retrieval_strategy:
    enum: [similarity, mmr, self_query, compression]
  retrieved_chunks:
    type: array
    description: Debug surface — raw chunks the retriever returned.
    items:
      type: object
      required: [source, content]
      properties:
        source: { type: string }
        content: { type: string }
        score: { type: number }
        metadata: { type: object }
allOf:
  - if:
      properties: { grounded: { const: false } }
    then:
      properties:
        citations: { maxItems: 0 }
```

**Document object (internal).** Every loader and splitter operates on the
LangChain-shaped `Document(page_content: string, metadata: object)`. Metadata
MUST carry at minimum a `source` field naming the originating file/URL; loaders
that produce paginated content MUST also carry a `page` (PDF) or equivalent
positional field so metadata-filtered retrieval (R2/AC2) is possible.

---

## 4. Business Rules

Each rule names the behavior, the failure it prevents (CTX-B), and the AC it's
verified by. Rules tagged *course-demonstrated* trace to a notebook cell or
transcript span; *project hardening* rules are constraints added beyond what the
course showed.

1. **R1 — Diversity-aware retrieval is the default.** Retrieval MUST NOT return
   two chunks whose text is byte-identical (or differs only in whitespace) for
   any single query. The default `strategy` is `mmr` for this reason
   (CTX-B1, CTX-C3). → AC1. *course-demonstrated.*
2. **R2 — Metadata-scoped queries respect the scope.** When the user's question
   refers to a structurally-distinguishable subset (e.g. "in lecture 3", "in the
   2024 policy") the system MUST filter retrieval to that subset, either via an
   explicit `metadata_filter` argument or by deriving one with self-query
   (CTX-B2, CTX-C4). → AC2. *course-demonstrated.*
3. **R3 — Chunks preserve semantic units.** Splitting MUST use a recursive,
   separator-aware strategy (paragraph → line → sentence → word → character) so
   that chunks do not slice mid-sentence whenever a higher-level boundary is
   available within `chunk_size` (CTX-B3, CTX-C1). → AC3. *course-demonstrated.*
4. **R4 — Conversation state is carried turn-to-turn.** A follow-up question
   MUST be resolved against prior turns: anaphora ("those", "they", "it") MUST
   be resolved before retrieval, by condensing the new question + history into a
   stand-alone question (CTX-B4, CTX-A stage 6). → AC4. *course-demonstrated.*
5. **R5 — The system abstains when ungrounded.** The generation prompt MUST
   instruct the LLM that *if the retrieved context does not contain the answer,
   it must say so and not invent one*. The response MUST set `grounded=false`
   and emit zero citations in that case (CTX-B5). → AC5. *course-demonstrated.*
6. **R6 — Source metadata survives splitting.** Any `Document` produced by a
   splitter MUST carry forward the `source` (and `page` where applicable) of its
   parent document (CTX-A stage 2). → AC6. *course-demonstrated.*
7. **R7 — Re-ingest is idempotent.** Re-running ingestion over the same corpus
   MUST NOT duplicate chunks in the vector store. The course's notebooks
   demonstrated `!rm -rf` of the persist directory; that is destructive and not
   acceptable when an operator has incremental data. Implement this by content
   hashing chunks (or by tracking ingested file hashes) so re-ingest of an
   unchanged file is a no-op and re-ingest of a modified file replaces only the
   affected chunks. → AC7. *project hardening — the course did the opposite.*
8. **R8 — Secrets come from the environment.** No API key, endpoint, or token
   appears in source, in fixtures, or in committed config. Loaded from
   `[secrets_store]`. → AC8. *project hardening; the notebooks loaded `.env`
   but did not enforce non-commit.*

---

## 5. Acceptance Criteria ★ — the oracle

### Fixture corpus (build-time author it; do not modify to make a test pass)

Create the following files under `./fixtures/`. The exact text matters — these
facts are what the ACs assert against.

- **`policies/expenses.md`**
  ```
  # Travel & Expense Policy

  ## Per-diem
  Employees travelling on company business may claim a per-diem of $75 per day
  for meals. Receipts are not required below $75/day; above that, itemised
  receipts MUST be submitted within 14 days of return.

  ## Air travel
  Economy class is the default for all flights under 6 hours. Premium economy
  is permitted for flights over 6 hours; business class requires VP approval.

  ## Mileage
  Personal-vehicle mileage is reimbursed at $0.67 per mile.
  ```
- **`policies/expenses-copy.md`** — byte-identical copy of `expenses.md`. This
  exercises R1 (CTX-B1: planted-duplicate failure). The duplicate is intentional;
  the system must not return both copies in a single retrieval result.
- **`lectures/lecture-01.md`**, **`lectures/lecture-02.md`**, **`lectures/lecture-03.md`**
  — each ~10–20 sentences. Lecture 1 covers *introductions and prerequisites*;
  Lecture 2 covers *linear regression*; Lecture 3 covers *logistic regression
  and classification*. **Critically, the word "regression" appears in all three
  files**, but only Lecture 3 contains the sentence: *"In this third lecture we
  derive the logistic-regression decision boundary."* This exercises R2
  (CTX-B2: lectures share vocabulary, only metadata distinguishes them).
- **`long/long-doc.md`** — ≥ 4000 characters of mostly-irrelevant filler about
  office snacks, with **exactly one sentence buried in the middle**: *"The
  WiFi password rotation interval is 90 days."* Exercises CTX-B6 (compression).
- **`out_of_scope/`** — empty directory. The corpus deliberately contains no
  information about "Q4 revenue" or "Aurelia Vance's tenure" — these are the
  abstention probes.

### Acceptance test table

| AC | Given | When | Then |
|---|---|---|---|
| **AC1** (R1) | The fixture corpus is ingested. | Asking *"What is the per-diem for meals?"* with `strategy=mmr`, `k=4`. | The four returned `retrieved_chunks` are pairwise non-identical (no two have byte-equal `content` after whitespace collapse). The `answer` MUST contain "$75". |
| **AC2** (R2) | Same corpus. | Asking *"What did the third lecture say about regression?"* with `strategy=self_query` (or `metadata_filter={source: 'lectures/lecture-03.md'}` if self-query is unavailable). | Every entry in `retrieved_chunks` has `metadata.source == 'lectures/lecture-03.md'`. The `answer` references the logistic-regression decision boundary. |
| **AC3** (R3) | A document containing the paragraph: *"Paragraphs are often delimited with a carriage return or two carriage returns. Sentences have a period at the end, but also have a space."* | Splitting with `chunk_size=150, chunk_overlap=0` and recursive separators including `"\n\n"`, `"\n"`, sentence boundary, `" "`, `""`. | No produced chunk ends mid-sentence when a sentence boundary was available within the chunk. Asserted by checking each chunk ends with `.`, `\n`, end-of-document, or — only if no sentence boundary fits — at a word boundary (` `). |
| **AC4** (R4) | Two-turn conversation: turn 1 *"Is probability a class topic?"*, the assistant answers (truthfully, "yes, as a prerequisite"). | Turn 2 *"Why are those prerequisites needed?"* | The retriever's stand-alone query (visible in `retrieved_chunks` debug or the chain's intermediate step) MUST contain the word *"probability"* or *"statistics"* — i.e., the anaphora "those" was resolved. The `answer` discusses probability/statistics, not generic CS prerequisites. |
| **AC5** (R5) | Same corpus. | Asking *"What were Aurelia Vance's Q4 revenue figures?"* | `grounded == false`, `citations == []`, `answer` expresses inability to answer from the provided documents (matches `/(don'?t know|not (in|found) (the|these) (documents|context))/i`). The answer MUST NOT contain a fabricated number. |
| **AC6** (R6) | Ingest `policies/expenses.md`. | Inspect any chunk in the vector store derived from it. | `metadata.source == 'policies/expenses.md'`. For PDF inputs, `metadata.page` is also present and is an integer. |
| **AC7** (R7) | Ingest the corpus once → record vector-store chunk count `N`. | Ingest the **same** corpus a second time without clearing the persist directory. | The vector store still contains exactly `N` chunks. Then modify one fixture (append one paragraph) and re-ingest: only chunks belonging to that file are replaced; total count changes by ≤ the chunk delta of that one file. |
| **AC8** (R8) | The repo. | `git grep -E '(sk-[A-Za-z0-9]{20}|OPENAI_API_KEY=)' -- ':!*.example'` and a search for hardcoded keys in fixtures. | Zero matches. `.env` is gitignored; only `.env.example` is committed. |

---

## 6. Boundaries

**Always**
- Always keep `temperature=0` for both the answer-generation LLM and any
  retriever-side LLM (self-query, compression). The course's spoken rationale —
  *factual, low-variance, reproducible* — is durable.
- Always carry `metadata.source` (and `page` where applicable) end-to-end from
  loader through splitter through retriever to citation.
- Always condense follow-up + history into a stand-alone question before
  retrieval (R4).
- Always abstain when retrieval did not surface the answer (R5).

**Ask First**
- **Switching the embedding model after data has been ingested.** Embeddings
  are not interchangeable across models; mixing `text-embedding-3-small` chunks
  with `text-embedding-ada-002` chunks in one collection silently breaks
  similarity scoring. A switch forces full re-embedding — the course's
  vector-store lesson treats this as expensive enough to plan around. Ask
  before doing it.
- **Switching the splitter or chunk size/overlap.** Re-chunking changes every
  vector and every metadata mapping; a downstream evaluation will not be
  comparable to one taken before. Ask before changing.
- **Adding `chain_type='map_reduce'` or `'refine'` to RetrievalQA.** The course
  showed these are not free wins — *map_reduce was both slower AND produced a
  worse answer than `stuff` on the example*; refine helped sometimes. Don't
  silently swap chain types to "scale to longer docs"; ask whether longer-doc
  scaling is a real requirement first.
- **Replacing vector retrieval with TF-IDF or SVM retrievers.** The course
  showed these as alternatives but TF-IDF noticeably underperformed SVM on
  their example, and both lack the diversity controls (MMR) and metadata
  filters of the vector path. If asked for a "simpler retriever", confirm
  what is gained and lost.
- **Letting `k` exceed 5.** The course observed quality degradation at the
  tail of larger `k`s. Going above 5 is permissible but ask first; a wider
  retrieval window often surfaces less-relevant chunks that crowd the prompt.

**Never**
- Never invent citations. If `grounded=false`, `citations` MUST be empty.
- Never answer the user's question when the retrieved context does not
  support an answer — abstain instead (R5).
- Never modify a fixture file to make an acceptance criterion pass. The
  fixtures encode the failure modes the course planted; mutating them invalidates
  the test.
- Never commit secrets, `.env`, API keys, or any credential.
- Never destructively wipe the vector store (`rm -rf` of the persist
  directory) as part of normal re-ingest. Idempotent re-ingest is R7.

---

## 7. Test Plan & Self-Verification

The build agent MUST execute these and report each AC's outcome with cited
evidence (the actual command output, file paths, line numbers). "Should pass"
or "looks correct" without execution evidence is a failure of the test plan.

```bash
# 1. Install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Ingest the fixture corpus
python -m chat_with_your_data.ingest --corpus ./fixtures --persist ./.vector_store

# 3. Run the AC suite
pytest -q tests/acceptance/    # tests/acceptance/test_ac1_diversity.py … test_ac8_no_secrets.py

# 4. Re-ingest idempotency check (AC7)
python -m chat_with_your_data.ingest --corpus ./fixtures --persist ./.vector_store
pytest -q tests/acceptance/test_ac7_idempotent_reingest.py

# 5. Secret scan (AC8)
git grep -E 'sk-[A-Za-z0-9]{20}|OPENAI_API_KEY=' -- ':!*.example' || echo "AC8 PASS"
```

For each AC, the report MUST include: AC id, command run, observed output (or
the relevant excerpt), and PASS/FAIL with the file:line of the assertion.

---

## Course Context Pack (embedded — agent-readable)

> Concepts and decisions only — no code copied from the notebooks. Anchored by
> stable `CTX-*` tags so the cross-references in §3–§6 survive any reordering.

### CTX-A. The pattern

The course's central pipeline is six stages. Each stage exists for a reason
that is independent of any specific library:

1. **Load** — turn external sources (PDF, URL, Notion export, transcribed
   audio, plain text) into a uniform `Document(content, metadata)` shape, so
   every downstream stage operates on one type. Without this, every loader's
   quirks leak into splitters and retrievers.
2. **Split** — break documents into chunks small enough to fit retrieval +
   generation budgets, but large enough to preserve a coherent unit of
   meaning. Overlap exists to cushion sentence boundaries that fall near a
   chunk edge.
3. **Embed + store** — turn each chunk into a numeric vector via an embedding
   model, then index those vectors in a similarity-searchable store. The
   store persists; ingestion is amortised.
4. **Retrieve** — at query time, embed the question and find the top-k
   most-similar chunks, optionally with filters (metadata) or post-processing
   (MMR for diversity, compression for relevance distillation).
5. **Generate** — pass the question + retrieved chunks to an LLM with a
   prompt that grounds the answer in the chunks and instructs abstention when
   the chunks don't cover the question.
6. **Converse** — track multi-turn history; before each retrieval, condense
   `(history, new question)` into a stand-alone question so anaphora resolves
   to the right entities.

### CTX-B. Failure-mode catalog

Each entry is the symptom seen in the course → the cause → the fix → which
rule/AC enforces it. Prose only.

- **CTX-B1 — Duplicate-content retrieval.** *Symptom:* top-k similarity search
  returns two byte-identical chunks; the second adds zero information and
  crowds out a third distinct chunk. *Cause:* the corpus contained a duplicate
  source file, and pure cosine-similarity retrieval has no diversity term.
  *Fix:* use MMR (Maximum Marginal Relevance), which optimises for relevance
  *and* mutual-dissimilarity, parameterised by `k` (final) and `fetch_k`
  (initial pool). *Enforced by:* R1, AC1.
- **CTX-B2 — Metadata-blind retrieval over structurally distinguishable
  content.** *Symptom:* a question scoped to a specific lecture / year / source
  returns chunks from other sources because the structural marker was not
  embedded; semantic similarity alone cannot represent "the third lecture".
  *Cause:* embeddings encode topic, not provenance; provenance is metadata.
  *Fix:* either pass an explicit `metadata_filter` at query time, or use a
  **self-query retriever** that uses an LLM to extract `(query, metadata
  filter)` from the natural-language question. *Enforced by:* R2, AC2.
- **CTX-B3 — Naive splitting slices mid-sentence.** *Symptom:* a question
  whose answer spans a sentence is unanswerable because the sentence was cut
  across two chunks, and only one chunk is retrieved. *Cause:* fixed-width
  splitting on character count without respecting separator hierarchy.
  *Fix:* use a recursive splitter with a separator hierarchy
  (paragraph → line → sentence → word → character), so a chunk only descends
  to the next-finer separator if the coarser one would over-shoot the size.
  *Enforced by:* R3, AC3.
- **CTX-B4 — RetrievalQA forgets prior turns.** *Symptom:* the user asks
  "Is probability a class topic?" and gets a relevant answer; then asks "Why
  are those prerequisites needed?" and gets an answer about basic CS skills,
  not probability — because the second retrieval never saw "probability".
  *Cause:* RetrievalQA is stateless; the second question was embedded
  literally, with "those" unresolved. *Fix:* a conversational chain that, on
  every turn, condenses `(history, new question) → stand-alone question` and
  retrieves against the stand-alone query. *Enforced by:* R4, AC4.
- **CTX-B5 — Hallucinated answers when retrieval misses.** *Symptom:* the LLM
  fluently confabulates details when the retrieved chunks don't contain the
  answer. *Cause:* the default behaviour of a chat LLM is to produce a
  plausible answer; nothing in `RetrievalQA(...)` alone tells it to abstain.
  *Fix:* a grounding instruction in the prompt — *"If you don't know the
  answer based on the context, say you don't know; do not make one up"* — and
  an output contract that ties `grounded=false` to zero citations.
  *Enforced by:* R5, AC5.
- **CTX-B6 — Long irrelevant context dilutes answers and inflates cost.**
  *Symptom:* a retrieved chunk is mostly off-topic, with one relevant
  sentence buried inside; the LLM either misses it or answers around it, and
  the prompt is needlessly long. *Cause:* retrieval returns whole chunks;
  granularity is the chunk, not the sentence. *Fix:* contextual compression —
  pass each retrieved chunk through an LLM-based extractor that pulls only
  the spans relevant to the query, then send the compressed bundle to the
  answer-generation step. *Trade-off:* extra LLM calls; only worthwhile when
  chunks are large or noisy. (Not separately enforced by an AC; available as
  the `compression` strategy in the contract.)

### CTX-C. Decision guides

Numbered trade-offs, each grounded in what the course actually showed.

1. **Splitter choice — Recursive vs. Character vs. Token.**
   - `RecursiveCharacterTextSplitter` is the **default for prose**; it
     descends a separator hierarchy and only goes finer when needed. The
     course's lessons 3 and 4 application configs both use it.
   - `CharacterTextSplitter` (single separator, default `"\n"`) only fits
     when the document has a single reliable separator. The course showed it
     producing weird mid-sentence splits when the separator didn't appear.
   - `TokenTextSplitter` is appropriate when the **downstream LLM context
     budget is the binding constraint**, since LLM context windows are
     measured in tokens, not characters. The course noted "tokens are often
     ~4 characters" as a rough conversion.
   - `MarkdownHeaderTextSplitter` is the right tool when the document has
     **explicit semantic structure (headings)** and you want those headings
     to ride along as metadata into each chunk — natural for Notion exports.
2. **Chunk size + overlap — there is no single "default".** The course used
   different values in different settings; record the source when you cite a
   value. The two **application** configs were `1500/150` (Lesson 4 vector
   store + Lessons 5–6 retrieval/QA) and `1000/150` (Lesson 7 chatbot
   `load_db`). Smaller chunks → more precise but more retrieval calls and
   more risk of cutting context; larger chunks → fewer cuts but lower
   density. Start at `1500/150` for prose; revisit if precision is poor.
3. **Diversity — when MMR pays off.** Use MMR (or another diversity-aware
   method) whenever the corpus may contain duplicates or near-duplicates, or
   when several documents legitimately cover the same topic from different
   angles. The course planted a duplicate PDF and showed MMR cleanly recovers
   distinct chunks. Trade-off: MMR usually requires a `fetch_k > k` pool;
   slightly more work per query.
4. **Self-query vs. explicit `metadata_filter`.**
   - Use **self-query** when the user types natural-language questions with
     embedded structural constraints ("in lecture 3", "from 2024 onwards") —
     an LLM extracts the filter automatically.
   - Use **explicit `metadata_filter`** when the calling code already knows
     the scope (e.g. tabbed UIs, account-scoped chat). It's cheaper (no LLM
     call to parse the filter) and more reliable.
5. **Chain type for QA — `stuff` is the default.** The course showed:
   `stuff` (one prompt, all chunks) is fastest and gave the best result on
   their example; `map_reduce` was both slower and worse on that example;
   `refine` was better than `map_reduce` because it sequentially carries
   information forward. Reach for `map_reduce` / `refine` only when the
   retrieved set genuinely cannot fit in the model's context window.
6. **Vector retrieval vs. TF-IDF / SVM retrievers.** The course presents
   TF-IDF and SVM retrievers as alternatives. SVM retrieved comparable
   results on their MATLAB query; TF-IDF was noticeably worse. Neither
   composes with MMR or metadata filtering as cleanly as the vector path.
   Default to vector + Chroma; consider lexical retrievers as a *complement*
   for keyword-heavy queries, not a replacement.

### CTX-D. Perishable assumptions

The course's notebooks installed everything **unpinned** and used the
**pre-1.0 LangChain namespace**. Treat the names below as **search
keywords against current docs**, not guaranteed imports.

- `langchain.document_loaders` (PyPDFLoader, NotionDirectoryLoader,
  WebBaseLoader, GenericLoader, FileSystemBlobLoader, OpenAIWhisperParser,
  YoutubeAudioLoader, TextLoader) — modern split: `langchain_community.document_loaders.*`.
- `langchain.text_splitter` (RecursiveCharacterTextSplitter,
  CharacterTextSplitter, TokenTextSplitter, MarkdownHeaderTextSplitter) —
  modern: `langchain_text_splitters`.
- `langchain.embeddings.openai.OpenAIEmbeddings` — modern: `langchain_openai.OpenAIEmbeddings`.
- `langchain.vectorstores.Chroma` — modern: `langchain_chroma.Chroma`.
- `langchain.vectorstores.DocArrayInMemorySearch` — modern: `langchain_community.vectorstores.docarray`.
- `langchain.llms.OpenAI` (default model `text-davinci-003`, replaced by
  `gpt-3.5-turbo-instruct`, both now superseded by chat models).
- `langchain.chat_models.ChatOpenAI` — modern: `langchain_openai.ChatOpenAI`.
- `langchain.retrievers.{ContextualCompressionRetriever, SVMRetriever, TFIDFRetriever}` — modern under `langchain_community.retrievers` or `langchain.retrievers`.
- `langchain.retrievers.self_query.base.SelfQueryRetriever` — still under
  `langchain.retrievers.self_query` but its lark dependency moves around.
- `langchain.retrievers.document_compressors.LLMChainExtractor`.
- `langchain.chains.RetrievalQA`, `langchain.chains.ConversationalRetrievalChain` —
  these are now generally implemented as **LCEL** (LangChain Expression Language)
  pipelines; the named-class forms still exist but the idiom is to compose
  retriever | prompt | llm explicitly.
- `langchain.memory.ConversationBufferMemory` — still available, but LCEL
  patterns increasingly manage history outside a "memory" object.
- `OpenAI` model names: `text-davinci-003` → `gpt-3.5-turbo-instruct` →
  `gpt-3.5-turbo`/`gpt-4o-mini`. Embeddings: `text-embedding-ada-002` →
  `text-embedding-3-small` / `text-embedding-3-large`.

The concepts in CTX-A, CTX-B, CTX-C are durable. **Only the names above are
perishable.** When an import fails, search current LangChain docs for the new
location of that concept; don't pin notebook-era names.

### CTX-E. Provenance map

Lesson titles and numbering follow the **transcripts**, not notebook
filenames. (Notebook files are numbered 01–06; the platform counts the
Introduction as Lesson 1, so notebook `0N` corresponds to transcript
Lesson `N+1`.) Nothing in this spec requires platform access.

| Transcript lesson | Notebook file | Contributes to |
|---|---|---|
| **Lesson 1 — Introduction** | (no notebook) | CTX-A (overview) |
| **Lesson 2 — Document Loading** | `01_document_loading.ipynb` | CTX-A stage 1; §2 loader rows |
| **Lesson 3 — Document Splitting** | `02_document_splitting.ipynb` | CTX-A stage 2; CTX-B3; CTX-C1; CTX-C2; R3/AC3 |
| **Lesson 4 — Vectorstores and Embedding** | `03_vectorstores_and_embeddings.ipynb` | CTX-A stages 3–4; CTX-B1; CTX-B2; §2 splitter `1500/150` config; the duplicate-PDF planted failure |
| **Lesson 5 — Retrieval** | `04_retrieval.ipynb` | CTX-C3 (MMR), CTX-C4 (self-query), CTX-B6 (compression), CTX-C6 (TF-IDF/SVM); R1/AC1, R2/AC2; "Ask First" trade-offs (chain type, k, retriever swap) |
| **Lesson 6 — Question Answering** | `05_question_answering.ipynb` | CTX-A stage 5; CTX-B5 (grounding/abstention); CTX-C5 (`stuff` vs `map_reduce` vs `refine`); R5/AC5 |
| **Lesson 7 — Chat** | `06_chat.ipynb` | CTX-A stage 6; CTX-B4 (history-condensed retrieval); §2 chatbot `1000/150` alt config; R4/AC4 |
| **Lesson 8 — Conclusion** | (no notebook) | (recap only) |

---

## Build closer

After the build is in a working state and the test plan in §7 has been run with
cited evidence, conclude the build by emitting **an infra/structure diagram of
the app** (an ASCII or Mermaid sketch is fine — components and the data flow
between them: loaders → splitter → embedding model → vector store → retriever
→ chat chain → UI, plus the secrets boundary and the `.vector_store/` persist
location). Close with the exact phrase, on its own line:

> This is the infra/structure diagram of this app

---

*Spec v1 · Course: LangChain Chat with Your Data (DeepLearning.AI × LangChain) ·
Project: `[learner_corpus]` chatbot (default: synthetic fixture corpus) ·
**Living document**: when the building agent produces something unexpected, add
the missing constraint here and re-run.*
