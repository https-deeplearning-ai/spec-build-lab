# Spec: Outdoor-Gear Catalog Q&A Assistant — Standalone Takeaway

> **What you're building:** a terminal catalog Q&A assistant that answers only from your catalog and grades itself. You ask "Please suggest a shirt with sun protection" and see it recommend the matching product from the retrieved catalog entries; you ask "Do you sell kayaks?" and see it say "I don't know." instead of inventing an answer; you ask "What is my name?" and see that the earlier turn reached the model; then you run the evaluation and see every test question graded CORRECT or INCORRECT. Answering the gate's first question with the recommended baseline build builds all of this end to end, and the build is COMPLETE when the offline suite passes — API keys unlock only the `live` tests and live use of the finished app.
>
> This file is self-contained: the Course Context Pack at the end replaces every external course reference, and nothing here needs course or platform access.
>
> `(CTX-X)` anchors mark course-derived knowledge. The Decision Ledger below holds every point where the build could diverge, each pinned to one course-derived default, so the spec builds as-is with no intake.
>
> Generated from the "LangChain for LLM Application Development" notebooks + transcripts + slides on 2026-10-21, guide @ 5caba53. Hand-evolved since 2026-10-22.

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

Model roles this build uses (for the step-5 checklist): **answerer** (always), **example generator** (when D5 is D5a), **grader** (always), **summarizer** (only when D3 is D3d). The course's own model id for every role is `gpt-3.5-turbo` (CTX-D).

## Decision Ledger (§0 above requires the build agent to present these before building)

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option.

| # | Category | Decision | Invariant (must hold; blank unless the pattern imposes a capability requirement) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| L1 | learner | **Project** — what the assistant is for. | | L1a. The course's example realization (a product-catalog Q&A assistant), re-expressed on this spec's synthetic catalog; expected to be swapped when your project differs — the pipeline and rules, not the outdoor-gear example, are what must survive. Branch: the course's example scenario shape. | L1a — Outdoor-gear catalog Q&A assistant with conversation memory and a self-grading evaluation run, on the synthetic fixture catalog (Recommended - course default; the course's example, expected to be swapped when your project differs). L1b — A Q&A assistant over your own document collection, with the same pipeline and evaluation run. | Switching changes only names and data; every rule and criterion still runs on the fixture catalog. | learner |
| L2 | learner | **Data / inputs** — the records the assistant answers from, and where they live. | | L2a. The course ran on its own 1,000-product outdoor clothing CSV, which this spec does not copy; the fixture catalog re-expresses its shape (one row per product: id, name, description) with facts this spec authors. | L2a — The synthetic 10-product fixture catalog declared in §5 (Recommended). L2b — The course's own outdoor clothing catalog CSV of 1,000 products (course default; not shipped in this spec — you must supply the file yourself). L2c — Your own records (CSV rows or text files), one record per document. | Real data needs its own evaluation examples; the fixture suite keeps running on the fixture catalog either way. Long records make document splitting matter (row D1). | learner |
| L3 | learner | **Goal** — what "working" means for an answer. | | L3a. | L3a — Answer product questions only from the retrieved catalog entries, reply "I don't know." when they lack the answer, and pass the evaluation run (Recommended - course default). L3b — The same, and also answer listing questions with a markdown table of matching products with a one-line summary each (the course's demo query format). | L3b adds a response format that the course's demo asked for in its query text; it needs its own criterion. | learner |
| L4 | learner | **Model / provider** for live use of the finished app (chat and embeddings). | | L4a. The course used OpenAI for both chat and embeddings. | L4a — OpenAI chat and embedding models (Recommended - course default; live use needs a paid OpenAI API key). L4b — A locally served open-weights chat and embedding model (no credential; heavy setup: install a local model server and download model weights). | Changing provider after an index exists means re-embedding the catalog, and answers and grades must be re-evaluated (Lesson 6: "if you decide to … swap in a different LLM … how do you know if you're making it better or worse?"). | learner |
| L5 | learner | **Environment** — where the app runs. | | L5a. The course ran everything as notebook cells; a terminal app is the lightest runnable form of the same pipeline. | L5a — A local terminal (command-line) app run with Python (Recommended). L5b — Jupyter notebook cells (course default). | The pipeline and criteria are identical; only how you invoke it changes. | learner |
| L6 | learner | **Scope boundary** — present the full §1 "Not Included" list *inside this question*, item by item with its tag, then ask whether to keep it or bring something back. Each item carries one of four tags: *Restorable* (additive, owned by no other row: built on request, with no acceptance criteria from this spec); *Owned by row* `<id>` (decided on that row, never here); *Named by the course but never built* (buildable, but this spec supplies no parameters and no acceptance criteria); *Unavailable* (outside the standalone build mode). | | L6a. The course made no choice here. | L6a — Keep every §1 exclusion; build the full acceptance set (Recommended). L6b — Bring back one or more §1 items: name them, and each is handled by its tag in §1. | A restored *restorable* item is built without acceptance criteria from this spec; an item tagged *owned by row …* is decided on that row instead; an *unavailable* item cannot be restored. A new exclusion is free text and must name the criteria it retires. | learner |
| D1 | design-argued | **Document splitting** before embedding. | Each retrievable unit is small enough that several retrieved units fit together in one model prompt. | D1a. | D1a — One catalog record = one document, no splitting (Recommended - course default). D1b — Split each document into smaller chunks before embedding (the course describes this but never built it; this spec supplies no chunk size, no overlap and no acceptance criteria for it). | Lesson 5 argues it: big documents are split into chunks "because we may not be able to pass the whole document to the language model … so we can only pass the most relevant ones", but "because these documents are already so small, we actually don't need to do any chunking here." Litmus: the split side is argued and never shown working, and it adds a pipeline stage, so the subject is a row with D1b marked never-built. Switching later forces re-embedding. | course+learner |
| D2 | design-argued | **Combining retrieved documents into an answer.** | The final answer is produced by the language model from the documents retrieved for the question. | D2a. | D2a — Stuff: all retrieved documents in one prompt, one model call (Recommended - course default). D2b — Map-reduce: one call per document with the question, then one call combining the answers (described in the course with a slide; never built; this spec supplies no parameters and no acceptance criteria for it). D2c — Refine: walk the documents one at a time, each call improving the previous answer (described with a slide; never built; no parameters and no acceptance criteria supplied). D2d — Map-rerank: one call per document returning an answer and a relevance score, keep the highest-scoring answer (described with a slide; never built; no parameters and no acceptance criteria supplied). | Lesson 5 and its video-shown slides argue it: stuff is "pretty simple … quite cheap and it works pretty well" and makes a single call, but "for large documents or many documents this will not work" (context length); map-reduce "can operate over any number of documents" and runs in parallel "but it does take a lot more calls" and treats documents as independent; refine combines information over time, gives longer answers, and is slower because calls depend on each other; map-rerank is "more experimental", relies on the model to score, and costs a call per document. Stuff is the most common, map-reduce second. Litmus: the alternatives are argued but never shown working, and each changes the number and order of model calls, so the subject is a row with D2b–D2d marked never-built. | course+learner |
| D3 | design-argued | **Conversation memory** — what prior conversation is carried into each prompt. | The model is stateless: prior conversation reaches it only through memory rendered into each turn's prompt, and when memory is bounded the oldest exchanges are dropped or condensed first. | D3a. All four of D3a–D3d run in the course's code; the full buffer is the one the course's chatbot example is built on first. | D3a — Full buffer: every exchange so far (Recommended - course default). D3b — Window: only the last k exchanges, with k = 2 (also run in the course's code, with k = 1). D3c — Token buffer: the most recent exchanges up to a token limit of 50, counted with the model's tokenizer (also run in the course's code). D3d — Summary buffer: recent exchanges verbatim up to a token limit of 100, older ones condensed into a model-written summary — adds a summarizer model call (also run in the course's code). D3e — Vector-data memory: store exchanges as embeddings and retrieve the most relevant ones each turn (named in the course; never built; this spec supplies no parameters and no acceptance criteria for it). D3f — Entity memory: model-extracted facts about specific people and things (named in the course; never built; no parameters and no acceptance criteria supplied). | Lesson 3 argues it and shows D3a–D3d working: the full buffer grows "longer and longer" and sending many tokens "will also become more expensive"; the window "prevents the memory from growing without limit" but forgets — with k = 1 the assistant lost the user's name; the token buffer "maps more directly to the cost of the LLM calls"; the summary buffer keeps recent turns verbatim and has an LLM summarize the rest. Vector-data and entity memory are named on a video-shown slide as further kinds (and "you can also use multiple memories at one time" — a mix goes to free text). Litmus: alternatives shown working and differing in which component holds memory, so the subject is a row. The numeric limits are levers (CTX-C). | course+learner |
| D4 | design-structural | **Durable conversation log** beyond the running process. | | D4a. | D4a — No durable log: the conversation exists only in the running process's memory (Recommended - course default). D4b — Also append every exchange to a local SQLite database via Python's standard library, for auditing and later improvement (the course suggested storing the whole conversation in a key-value or SQL database but never built it; this spec supplies no schema and no acceptance criteria for it). | Lesson 3 and its video-shown slide name it: "it's also not uncommon for developers to store the entire conversation in the conventional database … so you could refer back to the whole conversation for auditing or for improving the system further." Presented, not argued, so it enters as structural: D4b adds a store box. If chosen, the lightest realization that needs no setup is the standard library's embedded SQLite. | course+learner |
| D5 | design-argued | **Where evaluation examples come from.** | Every evaluation example pairs a question with a reference answer written from a source catalog record. | D5a. The course combined its two hand-written examples with five generated from its first five records. | D5a — Hand-written examples plus model-generated examples, one per source record for the first 5 catalog records (Recommended - course default). D5b — Hand-written examples only. | Lesson 6 argues it: hand-written examples are "the most simple" but "this doesn't really scale that well. It takes a bit of time", so the course automates with a model that writes a question-answer pair per document, then combines both sets. Litmus: hand-written-only is shown working and only outgrown (a limit, not a failure), so it is an option and the subject is a row. | course+learner |
| D6 | design-argued | **Run inspection** — how you see what happened inside one question's run. | Turning inspection on or off never changes any answer or grade. | D6a. The keyed hosted platform is not the only carrier of the taught behavior (seeing each step's inputs and outputs) — the keyless in-process trace carries it — so the platform is left out by default. | D6a — An in-process step trace, switched on per run, printing each step's inputs and outputs to the console (Recommended - course default). D6b — The framework vendor's hosted evaluation platform, which stores runs and shows them in a web UI and can collect examples into datasets (shown in the course; no code shipped; heavy setup: a hosted account and API key, and run data leaves your machine). D6c — Local stand-in for that platform: the same trace events appended to a local JSON-lines file as a run history — a stand-in, not the hosted service (the course never built it). D6d — Final answer only, no step trace (shown in the course as the first step it then goes beyond). | Lesson 6 argues it: running an example and reading the answer is the first thing to do, but "it's oftentimes not enough to just look at the final answer to understand what is or could be going wrong"; the debug trace shows the retrieved context and the full prompt, and "oftentimes when a wrong result is returned, it's not necessarily the language model … It's actually the retrieval step." The hosted platform does "everything that we just did in the notebook, but persisted and show it in a UI." Litmus: final-answer-only is shown working and only outgrown, and the platform is shown in a video demo, so the subject is a row. | course+learner |
| RR1 | realization | **Embedding function** the offline acceptance suite (and the app's offline mode) runs against. | Documents and queries are embedded by the same function; text that shares content with a query scores higher than unrelated text; the same text always maps to the same vector. | RR1a. Substitution: the course's embedding model needs a paid key (heavy), and embedding is the only carrier of the embed stage, so an honest stand-in is the Default and omission is not offered. Lightest tier: the Python standard library is enough — exact cosine over a 10-record catalog meets the Invariant at the spec's declared scale, so no embedded library or local service is needed. | RR1a — Stand-in: a standard-library term-count vector with cosine similarity — a lexical stand-in for a semantic embedding model, labeled as a stand-in in code and in trace output (Recommended). RR1b — The OpenAI embedding model in the suite too (course default; heavy setup: a paid OpenAI API key; the retrieval criteria become `live`). | Lesson 5: embeddings capture meaning so "pieces of text with similar content will have similar vectors". The stand-in matches shared words, not meaning: a paraphrase with no shared word scores 0. It exists so the pipeline runs on day one; live use goes through the provider chosen on L4. | course+learner |
| RR2 | realization | **Model the offline acceptance suite runs against.** | The suite drives the real pipeline end to end — retrieval, prompt building, memory, output parsing, grading — with only the model swapped. | RR2a. Substitution: the course's model needs a paid key (heavy) and is the only carrier of the answering and grading stages, so the scripted stand-in is the Default and omission is not offered. | RR2a — Scripted stand-in model: a fake whose per-role responses are declared in §5, labeled as a stand-in in its own description (Recommended). RR2b — The course's live OpenAI chat model (course default; heavy setup: a paid OpenAI API key; criteria that assert scripted text become `live` and are re-asserted by behavior). | A live model makes answers vary run to run (the course notebooks warn "LLM's do not always produce the same results"), so exact-text criteria cannot run against it. | course+learner |

## 1. Objective

A terminal app that answers questions about a product catalog by retrieving the most similar catalog records and having a language model answer from them alone — replying "I don't know." when they lack the answer — carries conversation memory across turns, and grades itself on a set of question-answer examples with a language-model grader (CTX-A).

### Not Included

Each item is tagged with how the gate's scope-boundary row (L6) handles it.

1. **Agents with tools** — a model that decides which tool to call (a calculator, an encyclopedia lookup, web search, a custom "today's date" tool, a Python-code agent). *Restorable* — the course built this; this spec supplies no acceptance criteria for it (background in CTX-C).
2. **Router chain** — sending each question to a subject-specialized prompt, with a fallback prompt when no subject fits. *Restorable* — no acceptance criteria supplied.
3. **Multi-step sequential chains** — e.g. translate a review, summarize it, detect its language, write a reply in that language. *Restorable* — no acceptance criteria supplied.
4. **Review field extraction** — turning a free-text customer review into fixed fields (was it a gift, delivery days, price/value remarks). *Restorable* — no acceptance criteria supplied.
5. **Document splitting into chunks.** *Owned by row D1*.
6. **Map-reduce, refine and map-rerank answer combining.** *Owned by row D2*.
7. **Vector-data memory and entity memory.** *Owned by row D3*.
8. **A durable conversation log for auditing.** *Owned by row D4*.
9. **The hosted evaluation platform.** *Owned by row D6*.
10. **A different or persistent vector store** (the index is rebuilt in memory at each start). *Named by the course but never built* — buildable, but this spec supplies no parameters and no acceptance criteria for it.
11. **A web or chat UI, multiple users, or authentication.** *Restorable* — past the course's scope; no acceptance criteria supplied.
12. **Grafting this pattern into an existing codebase.** *Unavailable* — this spec builds a standalone app only.

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python 3.11 or newer | The course is Python notebooks. |
| LLM framework | LangChain, current release (core package plus the provider integration package) | **Honest install situation:** the course's install lines are unpinned (`pip install --upgrade langchain`, and `openai`, `python-dotenv`, `tiktoken`, `docarray`, `wikipedia` with no versions). A markdown note in the course's Q&A notebook records that it ran on langchain 0.0.179 and openai 0.27.7 — a record of the run, not an install pin — so this spec uses a current release. Every era-specific class and model name is in CTX-D as a search keyword, not a guaranteed import. |
| Chat + embedding provider | Row L4's Default (OpenAI) | Change it on row L4, not here. |
| Offline embedding function | Row RR1's Default (standard-library stand-in) | Change it on row RR1. |
| Offline model | Row RR2's Default (scripted stand-in) | Change it on row RR2. |
| Vector store | The framework's in-process in-memory vector store, rebuilt from the catalog at each start | The course used an in-memory vector store "because it … doesn't require connecting to an external database of any kind" (CTX-C). Keyless and embedded, so it stays as the course had it; not a Ledger row. |
| Token counting | The provider's tokenizer (only when row D3 is D3c or D3d) | The course installed `tiktoken` for this, unpinned. |
| Secrets | Read from the environment, optionally loaded from a local `.env` file (`python-dotenv`, unpinned in the course) | `OPENAI_API_KEY` is needed only for live use and `live` tests; never hardcoded or committed. |
| Tests | pytest, with a `live` marker | Project hardening. |

## 3. Input/Output Contracts

All four objects below are emitted as JSON by the app (stdout for `ask` and `eval`, one object per line for trace events).

**AnswerResult** — one answered question.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AnswerResult",
  "type": "object",
  "required": ["question", "answer", "abstained", "retrieved_ids"],
  "additionalProperties": false,
  "properties": {
    "question": {"type": "string", "minLength": 1},
    "answer": {"type": "string", "minLength": 1},
    "abstained": {"type": "boolean", "description": "true exactly when answer, trimmed, starts with \"I don't know\""},
    "retrieved_ids": {
      "type": "array",
      "items": {"type": "string", "pattern": "^P[0-9]{2}$"},
      "minItems": 1,
      "maxItems": 4,
      "uniqueItems": true,
      "description": "product_id of each retrieved document, most similar first"
    }
  },
  "if": {"properties": {"abstained": {"const": true}}},
  "then": {"properties": {"answer": {"pattern": "^\\s*I don't know"}}},
  "else": {"properties": {"answer": {"not": {"pattern": "^\\s*I don't know"}}}}
}
```

The `retrieved_ids` pattern fits the fixture catalog's ids; with rows L2b/L2c it widens to the data's own id format.

**GeneratedExample** — one parsed output of the example generator (key names are the course's own).

```json
{
  "title": "GeneratedExample",
  "type": "object",
  "required": ["query", "answer", "source_id"],
  "additionalProperties": false,
  "properties": {
    "query": {"type": "string", "minLength": 1},
    "answer": {"type": "string", "minLength": 1},
    "source_id": {"type": "string"}
  }
}
```

**EvalReport** — written to `eval_report.json` by the evaluation run.

```json
{
  "title": "EvalReport",
  "type": "object",
  "required": ["examples", "parse_errors", "totals"],
  "additionalProperties": false,
  "properties": {
    "examples": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["query", "answer", "origin", "prediction", "grade"],
        "additionalProperties": false,
        "properties": {
          "query": {"type": "string"},
          "answer": {"type": "string", "description": "reference answer"},
          "origin": {"enum": ["hand_written", "generated"]},
          "source_id": {"type": "string"},
          "prediction": {"type": "string"},
          "grade": {"enum": ["CORRECT", "INCORRECT"]}
        }
      }
    },
    "parse_errors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source_id", "raw"],
        "properties": {"source_id": {"type": "string"}, "raw": {"type": "string"}}
      }
    },
    "totals": {
      "type": "object",
      "required": ["graded", "correct", "incorrect", "parse_errors"],
      "properties": {
        "graded": {"type": "integer", "minimum": 0},
        "correct": {"type": "integer", "minimum": 0},
        "incorrect": {"type": "integer", "minimum": 0},
        "parse_errors": {"type": "integer", "minimum": 0}
      },
      "description": "graded = correct + incorrect = length of examples; parse_errors = length of parse_errors"
    }
  }
}
```

**TraceEvent** — one step of one run, emitted only when inspection is on (row D6).

```json
{
  "title": "TraceEvent",
  "type": "object",
  "required": ["run_id", "step", "inputs", "outputs"],
  "properties": {
    "run_id": {"type": "string"},
    "step": {"enum": ["retrieve", "prompt", "model", "answer"]},
    "inputs": {"type": "object"},
    "outputs": {"type": "object"},
    "token_usage": {"type": ["object", "null"], "description": "provider-reported prompt/completion/total tokens when available; null for the scripted model"},
    "stand_in": {"type": "array", "items": {"type": "string"}, "description": "names of stand-ins in use for this run (e.g. scripted model, lexical embeddings)"}
  }
}
```

Per question, events come in the order `retrieve` (inputs: question; outputs: retrieved ids and texts), `prompt` (outputs: the full rendered prompt), `model` (outputs: the raw model response), `answer` (outputs: the AnswerResult).

## 4. Business Rules

**R1. Grounded answers, honest abstention.** The answer prompt instructs the model to answer the question using only the retrieved catalog context and, when that context does not contain the answer, to reply exactly "I don't know." without making up an answer. The app passes the model's reply through unchanged and sets `abstained` per the §3 contract. Prevents invented answers (CTX-B5). *Course-demonstrated* (the course's question-answering prompt carries this instruction, seen in Lesson 6's trace); the exact fixed phrase and the `abstained` flag are *project hardening*. → AC5, AC6, AC7, AC20

**R2. Similarity retrieval.** Each question is embedded with the same function used for the catalog documents and the 4 most similar documents are retrieved, most similar first; ties break by `product_id` ascending (tie order is *project hardening*). k = 4 is a body default: Lesson 5 narrates that similarity search "returns four documents"; the course never sets or argues it. *Course-demonstrated* (CTX-A). → AC2, AC3

**R3. Stuff the context, one call.** All retrieved documents go into one answer prompt, joined by the separator `<<<<>>>>>`, and each question costs exactly one answerer call. *Course-demonstrated* (stuff method, row D2). The separator is a contradicted near-equivalent value: the course's Lesson 5 chain used the framework's default separator and its Lesson 6 evaluated chain set `<<<<>>>>>`; selected by the end-to-end application's config (the chain Lesson 6 evaluates end to end), since no narration states a value — a **post-build lever** (CTX-C). → AC4

**R4. Model output used as data is parsed, never trusted as a string.** Wherever the app consumes model output as structured data (generated examples, grader verdicts), the prompt carries format instructions for the expected shape, and the reply is parsed into that shape (`GeneratedExample`; grade enum). A reply that does not parse is recorded as a parse error with its raw text, and the run continues. Prevents the course's planted failure of reading a field from a reply that only looks like JSON (CTX-B1). *Course-demonstrated*; continuing past a parse error is *project hardening*. → AC11, AC12

**R5. Prompt variables must line up.** Every prompt template declares its input variables (the answer prompt: `question`, `context`, `history`); building a prompt with a missing or misnamed variable fails before any model call with an error naming the variable. Prevents the key-mismatch errors the course warns about when outputs feed later steps (CTX-B3). *Course-demonstrated* warning; failing before the model call is *project hardening*. → AC10

**R6. Memory reaches the model through the prompt.** In a conversation, each turn's answer prompt carries the conversation memory (as kept by row D3) in a "conversation so far" section, as alternating human and assistant lines in order; retrieval uses the current question only. Prevents the stateless model forgetting earlier turns (CTX-B2). *Course-demonstrated* (memory); combining memory with retrieval in one prompt and retrieving on the current question only are *project hardening* — the course taught memory and document Q&A in separate lessons. → AC8

**R7. Temperature per role.** Answerer and grader calls use temperature 0 (the course's Q&A and grading configs; Lesson 2: "set the temperature … to zero … to make this output a little bit less random"); the example generator uses the provider's default temperature (the course's generator config sets none; Lesson 2 narrates the default as 0.7); the summarizer (row D3 is D3d) uses 0 (the course's memory config). Temperature is a **post-build lever**: the course argues a value trade-off (0 for repeatable answers, 0.9 in Lesson 4 "so that we can get some fun descriptions"), decided as a lever because the sides differ only in a number. *Course-demonstrated.* → AC15

**R8. Evaluate with examples, predictions and a model grader — never exact string matching.** The evaluation run builds its examples per row D5, predicts an answer for each with the full question-answering pipeline, and asks the grader model to grade each prediction against the reference answer as CORRECT or INCORRECT by meaning, one grader call per example. It writes `eval_report.json` (§3). It never grades by exact string comparison, substring match or regex: the course shows a reference "Yes" and a correct long prediction that share no characters (CTX-B4). Generated examples come from the first 5 catalog records (the course's config), one per record. *Course-demonstrated*; the two-value grade enum is *project hardening* over the course's free-text grade. → AC13, AC14, AC21

**R9. Inspection on demand.** A per-run switch (`--trace`) turns on step inspection per row D6: one TraceEvent per step (§3), showing the retrieved documents, the full prompt and the raw model response, so a wrong answer can be located in retrieval or in the model (CTX-B6). Off by default. Inspection never changes an answer or grade. *Course-demonstrated* (Lesson 6 debug mode); off-by-default and the event shape are *project hardening*. → AC16, AC17

**R10. Fresh in-memory index, one document per record.** At start the app loads the catalog, turns each record into one document whose text lists every field as "field: value" lines and whose metadata carries its `product_id`, embeds all documents and holds them in the in-memory vector store. Nothing is persisted between runs. *Course-demonstrated* (rows D1, and the course rebuilt its in-memory index each run). → AC1

**R11. Keyless offline suite, secrets from the environment.** The offline suite (rows RR1, RR2) runs with no API key and no network. Live mode reads `OPENAI_API_KEY` from the environment or `.env`; no key appears in source or committed files. *Course-demonstrated* (the course loads its key from a local `.env`); the keyless suite is *project hardening*. → AC18

**R12. Conversation lives in the process.** Conversation memory exists only in the running process; ending the process ends the conversation, and no store of exchanges is written (row D4). *Course-demonstrated* (the course's memory lived in the notebook process). → AC9

**R13. Live mode uses the chosen provider.** Without `--offline`, the app answers, generates examples and grades with row L4's provider for chat and embeddings. *Course-demonstrated.* → AC19

## 5. Acceptance Criteria

### Fixture corpus (declared first; the build agent MUST NOT modify any of it to make a test pass)

**`fixtures/catalog.csv`** — columns `product_id,name,description`; exactly these 10 rows:

| product_id | name | description |
|---|---|---|
| P01 | Trailhead Fleece Pullover | Midweight pullover made of recycled polyester fleece. Two zippered side pockets. Weight 14 oz. |
| P02 | Summit Down Parka | Hooded winter parka from the AlpineLoft collection. Insulated with 700-fill down. |
| P03 | Coastal Sun Shirt | Long-sleeve shirt rated UPF 50+ for sun protection. Quick-dry nylon. |
| P04 | Ridge Runner Tee | Everyday cotton tee with a relaxed fit. |
| P05 | Canyon Hiking Shorts | Stretch hiking shorts with a 7 inch inseam. |
| P06 | Harbor Rain Shell | Waterproof breathable rain jacket with sealed seams. |
| P07 | Meadow Wool Socks | Merino wool crew socks for cool weather. |
| P08 | Glacier Beanie | Ribbed knit beanie lined with fleece. |
| P09 | Breeze Sun Hoodie | Lightweight hoodie with UPF 30 sun protection and a thumb-loop cuff. |
| P10 | Trail Daypack | 20 liter daypack with a padded laptop sleeve. |

**Stand-in embedding (row RR1a) — declared behavior.** Text is lowercased and split on every run of characters that are not `a–z` or `0–9`; empty tokens and these stopwords are dropped: a, an, the, and, or, of, for, to, in, on, with, is, are, do, does, did, what, which, how, please, you, your, my, it, its, this, that, from, has, have, me, i, any. The vector is the count of each remaining token; similarity is cosine (0 when either vector is empty). Replayed over the fixture: the query "Please suggest a shirt with sun protection" scores P03 ≈ 0.521, P09 ≈ 0.327, every other record 0, so the top 4 are P03, P09, P01, P02; "Do you sell kayaks?" scores every record 0, so the top 4 are P01, P02, P03, P04.

**`fixtures/conversation_script.json`** — four human turns, in order: T1 "Hi, my name is Priya." · T2 "Please suggest a shirt with sun protection" · T3 "Do you sell kayaks?" · T4 "What is my name?"

**`fixtures/handwritten_examples.json`** — two examples (the course also wrote two by hand):
- E1 — query "Does the Trailhead Fleece Pullover have side pockets?", answer "Yes"
- E2 — query "What collection is the Summit Down Parka from?", answer "The AlpineLoft collection"

**`fixtures/scripted_model.py`** (module `scripted_model`) — the **scripted stand-in model** (row RR2a). Its own description says it is a fake standing in for a language model. It is created per role, receives each rendered prompt plus the prompt's variable values, records every call (role, full prompt text, request parameters such as temperature) for tests to inspect, and replies by role:

- *answerer* — exact match on the current `question` value:
  - "Hi, my name is Priya." → "Hello Priya! How can I help you with our catalog today?"
  - "Please suggest a shirt with sun protection" → "I recommend the Coastal Sun Shirt, rated UPF 50+."
  - "What is my name?" → "Your name is Priya."
  - "Does the Trailhead Fleece Pullover have side pockets?" → "The Trailhead Fleece Pullover does have two zippered side pockets."
  - "What collection is the Summit Down Parka from?" → "It is part of the AlpineLoft collection."
  - "What is the Trailhead Fleece Pullover made of?" → "It is made of recycled polyester fleece."
  - "What fill power is the Summit Down Parka insulated with?" → "I don't know." (a deliberate model miss: retrieval finds P02, the model fails — CTX-B6)
  - "What UPF rating does the Coastal Sun Shirt have?" → "The Coastal Sun Shirt is rated UPF 50+."
  - "How long is the inseam of the Canyon Hiking Shorts?" → "The inseam is 7 inches."
  - any other question (including "Do you sell kayaks?") → "I don't know."
- *example generator* — keyed by the `product_id` in the document it receives; replies are a JSON object inside a fenced json block, except P04:
  - P01 → query "What is the Trailhead Fleece Pullover made of?", answer "Recycled polyester fleece"
  - P02 → query "What fill power is the Summit Down Parka insulated with?", answer "700-fill down"
  - P03 → query "What UPF rating does the Coastal Sun Shirt have?", answer "UPF 50+"
  - P04 → the plain text `QUESTION: What is the Ridge Runner Tee made of? ANSWER: cotton` (deliberately not in the instructed format — CTX-B1)
  - P05 → query "How long is the inseam of the Canyon Hiking Shorts?", answer "7 inches"
- *grader* — keyed by the example's query: "What fill power is the Summit Down Parka insulated with?" → "INCORRECT"; every other query → "CORRECT".
- *summarizer* (used only when row D3 is D3d) — always → "Priya introduced herself and asked for a sun-protective shirt; the assistant recommended the Coastal Sun Shirt."

**Planted states.**
- *keyless environment* — `OPENAI_API_KEY` unset and outbound network blocked (e.g. a test fixture that fails any socket connect).
- *misaligned variables* — an attempt to build the answer prompt with the variables `query`, `context`, `history` (no `question`).

Replayed outcomes the criteria assert (defaults in force: D3a, D5a, D6a, RR1a, RR2a): generated examples parse for P01, P02, P03, P05 and fail for P04 → 1 parse error; graded examples = E1, E2 + 4 generated = 6; grades CORRECT for 5, INCORRECT for 1 (the fill-power question).

### Criteria

| AC | Given | When | Then | Mode |
|---|---|---|---|---|
| AC1 | the fixture catalog, a fresh start (R10) | the index is built | the vector store holds exactly 10 documents, one per row, each with metadata `product_id` P01…P10 and text containing that row's full `name` and `description` unchanged | offline |
| AC2 | AC1's index (R2) | `ask --offline "Please suggest a shirt with sun protection"` | `retrieved_ids` is exactly ["P03", "P09", "P01", "P02"] | offline |
| AC3 | the stand-in embedding function (R2) | the query "Please suggest a shirt with sun protection" is compared with P03's and P07's document texts, and P03's text is embedded twice; then `ask --offline --trace "Please suggest a shirt with sun protection"` runs | similarity to P03 > similarity to P07; the two embeddings of P03 are identical; the trace's `stand_in` list names the lexical embeddings | offline |
| AC4 | AC1's index, scripted model (R3) | `ask --offline "Please suggest a shirt with sun protection"` | exactly 1 answerer call is recorded; its prompt contains the texts of P03, P09, P01, P02 and exactly 3 occurrences of `<<<<>>>>>` | offline |
| AC5 | as AC4 (R1) | the recorded answerer prompt is inspected | it instructs answering only from the given context and replying exactly "I don't know." when the context lacks the answer | offline |
| AC6 | AC1's index, scripted model (R1) | `ask --offline "Do you sell kayaks?"` | the AnswerResult validates against §3 with `answer` "I don't know.", `abstained` true, `retrieved_ids` ["P01", "P02", "P03", "P04"] | offline |
| AC7 | as AC4 (R1) | the AnswerResult is read | it validates against §3 with `answer` "I recommend the Coastal Sun Shirt, rated UPF 50+." and `abstained` false | offline |
| AC8 | `fixtures/conversation_script.json`, scripted model (R6) | the four turns run in one `chat --offline` session | T1's answerer prompt has an empty conversation section; T4's prompt contains, in order, "Hi, my name is Priya.", "Hello Priya! How can I help you with our catalog today?", the T2 exchange and the T3 exchange; T4's answer is "Your name is Priya." | offline |
| AC9 | AC8's session ended (R12) | a new `chat --offline` process sends T1 again | its answerer prompt has an empty conversation section, and no file or database holding the earlier exchanges exists in the build folder | offline |
| AC10 | the *misaligned variables* planted state (R5) | the answer prompt is built | an error is raised whose message names `question`, and the scripted model records 0 calls | offline |
| AC11 | the scripted generator (R4) | `eval --offline` runs | the generator is called 5 times (P01–P05); `parse_errors` has exactly one entry, `source_id` "P04", whose `raw` is the P04 reply text; the run exits with status 0 | offline |
| AC12 | as AC11 (R4) | the generated examples are read | 4 validate as GeneratedExample; the one with `source_id` "P01" has `query` "What is the Trailhead Fleece Pullover made of?" and `answer` "Recycled polyester fleece" | offline |
| AC13 | as AC11 (R8) | `eval_report.json` is read | it validates against §3; `examples` has 6 entries — 2 with `origin` "hand_written", 4 "generated"; `totals` = graded 6, correct 5, incorrect 1, parse_errors 1; the INCORRECT entry's query is "What fill power is the Summit Down Parka insulated with?" | offline |
| AC14 | as AC11 (R8) | E1's report entry and the grader calls are inspected | E1 has `answer` "Yes", `prediction` "The Trailhead Fleece Pullover does have two zippered side pockets.", `grade` "CORRECT"; the grader is called exactly 6 times, once per graded example, each prompt holding that example's query, reference answer and prediction | offline |
| AC15 | AC11's recorded calls (R7) | request parameters are inspected | every answerer and grader call carries temperature 0; no generator call sets a temperature | offline |
| AC16 | AC1's index, scripted model (R9) | `ask --offline --trace "What fill power is the Summit Down Parka insulated with?"` | 4 TraceEvents validate against §3 in the order retrieve, prompt, model, answer; the retrieve event's ids start with "P02"; the prompt event holds the full prompt including P02's text; the model event holds "I don't know." | offline |
| AC17 | AC1's index, scripted model (R9) | AC16's question is asked with `ask --offline --trace` and with `ask --offline` | without `--trace` no TraceEvent is emitted; the two AnswerResults are identical | offline |
| AC18 | the *keyless environment* planted state (R11) | the offline suite runs | every offline criterion passes; no source or committed file contains an API key (a search for an `sk-` prefix followed by letters or digits finds none) | offline |
| AC19 | a valid `OPENAI_API_KEY`, live mode (R13) | `ask "Please suggest a shirt with sun protection"` | `retrieved_ids` starts with "P03" and `answer` names the Coastal Sun Shirt | live |
| AC20 | as AC19 (R1) | `ask "Do you sell kayaks?"` | `abstained` is true | live |
| AC21 | as AC19 (R8) | `eval` runs | `eval_report.json` validates against §3 and every example carries a grade from the live grader | live |

## 6. Standing Permissions (in force for the entire build)

**Always**
- Run the offline suite and report per criterion before claiming any part done.
- Keep every stand-in labeled as a stand-in — in its own description, in trace output, and in the checklist.
- Read secrets from the environment or `.env`; keep `.env` out of version control.
- Keep inspection off unless `--trace` is given.
- Build on the values in `resolved-decisions.md`.

**Ask First** — derived from the course's spoken trade-offs (CTX-C table); each entry either forces rework or changes a behavior guarantee no criterion catches.
- Changing the embedding function or provider once an index exists — forces re-embedding the catalog (rows RR1, L4).
- Turning on document splitting, or changing how records become documents — forces re-embedding (row D1).
- Switching the answer-combining method — changes the number of model calls and what each sees, with no criterion catching the cost change (row D2).
- Changing the memory kind or its limits (window k, token limits) — changes what the model sees and what each turn costs (row D3; window k = 2 is the generator's reading of the course's "set to a larger number" than 1, a post-build lever).
- Raising the answerer's or grader's temperature — makes answers and grades vary run to run without failing an offline criterion (R7 lever).
- Swapping the chat model, or the retrieval strategy, and calling the result better — re-run the evaluation first (Lesson 6).
- Sending run data to the hosted evaluation platform — data leaves the machine (row D6).
- Writing conversations to any durable store — changes what is retained about users, with no criterion catching it (row D4).
- Making inspection, example generation or summarization run automatically on every question — changes cost silently (rows D5, D6, D3).
- Changing the document separator or retrieval k — post-build levers; changing k changes how much context each answer sees.

**Never**
- Invent provenance, citations or course claims.
- Answer when the retrieved context lacks the answer, or rewrite the model's "I don't know." into an answer.
- Modify fixtures (or the scripted model's declared replies) to make a test pass.
- Commit secrets.
- Grade by exact string match, substring or regex.
- Present a stand-in as the real service or model.

## 7. Test Plan & Self-Verification

Commands (run from the app's root):

- `python -m pytest -m "not live"` — the offline suite (AC1–AC18).
- `OPENAI_API_KEY=… python -m pytest -m live` — the live criteria (AC19–AC21).
- `python -m catalog_qa ask --offline "Please suggest a shirt with sun protection"` — prints an AnswerResult.
- `python -m catalog_qa ask --offline --trace "What fill power is the Summit Down Parka insulated with?"` — prints TraceEvents then the AnswerResult.
- `python -m catalog_qa chat --offline` — interactive conversation.
- `python -m catalog_qa eval --offline` — writes `eval_report.json` and prints its totals.
- Drop `--offline` for live use with row L4's provider.

The building agent MUST report results per acceptance criterion with cited evidence — the test name and its output, and file paths. "Should pass" or "looks correct" counts as a failure: it means the test was not run.

**Tests by option** — one line per non-Default option. A build that chose an option reports the criteria it retires as not applicable, not as failures, and builds the changed ones as changed.

| Option id | Rules and criteria that no longer apply | Rules, criteria and Ledger cells that change (and how) | Offline-suite criteria switched off |
|---|---|---|---|
| L1b | — | Title, blockquote and §1 wording name your project; every criterion still runs on the fixture catalog. | — |
| L2b | — | The app's live catalog path points at the course CSV you supply; AC1 still checks the fixture catalog. | — |
| L2c | — | The app's live catalog path points at your records; AC1 still checks the fixture catalog; the §3 `retrieved_ids` pattern widens to your ids. | — |
| L3b | — | R1 adds: listing questions get a markdown table with one row per matching product (name, one-line summary). AC7 adapted: add a declared scripted answerer entry for a listing question and assert a table with ≥ 1 row; existing entries unchanged. | — |
| L4b | — | R11: live mode needs no key. R13, AC19, AC20, AC21 run against the local server. | — |
| L5b | — | §7's CLI commands become notebook cells calling the same functions; the pytest commands are unchanged. | — |
| L6b | — (unless a restored item retires one; name it) | Each restored §1 item is built per its tag; restorable items carry no criteria from this spec — list them under *Adapted*. | — |
| D1b | — | R10: a record may yield several documents. AC1 adapted: each stored chunk keeps its record's `product_id`, and a record's chunks together hold its full text; no chunk size is supplied. AC2, AC4 adapted to chunk ids. §3's id `pattern` ("^P[0-9]{2}$") and `uniqueItems` on retrieved ids no longer hold for chunk ids, which AC6 and AC7 validate against; this spec does not restate the schema for D1b. | AC1, AC2, AC4 (as written) |
| D2b | R3, AC4, AC16 | R1 applies to every per-document call and to the combining call; AC5 adapted to check every answerer prompt; AC16's four-event order no longer holds with several model calls; no parameters supplied. | AC4, AC16 |
| D2c | R3, AC4, AC16 | As D2b, for the refine calls. | AC4, AC16 |
| D2d | R3, AC4, AC16 | As D2b; each per-document call also returns a score. | AC4, AC16 |
| D3b | — | R6: memory keeps the last 2 exchanges. AC8 new form: T4's prompt contains the T2 and T3 exchanges and does not contain "Priya". | AC8 (as written) |
| D3c | — | R6: memory keeps the most recent exchanges whose token count totals ≤ 50, oldest dropped first; offline, tokens are counted as whitespace-separated words of the human and assistant utterances (a stand-in for the provider tokenizer). AC8 new form: at limit 50 T4's prompt holds all three earlier exchanges (39 words); with the limit set to 20, only the T3 exchange. | AC8 (as written) |
| D3d | — | R6: summary buffer with limit 100, adding the summarizer role (R7: temperature 0). AC8 new form: at limit 100 T4's prompt holds all three exchanges verbatim and the summarizer is not called; with the limit set to 20, T4's prompt holds the scripted summary followed by the T3 exchange verbatim, and the summarizer was called. | AC8 (as written) |
| D3e | R6, AC8 | No parameters or criteria supplied; list the memory behavior built under *Adapted*. | AC8 |
| D3f | R6, AC8 | No parameters or criteria supplied; list the memory behavior built under *Adapted*. | AC8 |
| D4b | R12, AC9 | A local SQLite store of exchanges exists; no schema or criterion supplied — list what was built under *Adapted*. | AC9 |
| D5b | AC11, AC12 | R8: no generator role; R4 then covers only grader verdicts, and no criterion exercises it (AC11 and AC12 are retired). AC13 new form: 2 examples, both `hand_written`, totals graded 2, correct 2, incorrect 0, parse_errors 0. AC14: grader called exactly 2 times. AC15: no generator calls to check. | AC11, AC12, AC13 (as written) |
| D6b | — | R9: trace events go to the hosted platform (account and key needed). AC16 and AC17 become `live`, checked in the platform's run view. | AC16, AC17 |
| D6c | — | R9: trace events are appended to `trace.jsonl` instead of the console; AC16 and AC17 read that file. | — |
| D6d | R9, AC16, AC17 | `--trace` is not built. AC3 drops its trace (`stand_in` list) clause; row RR1a's "labeled as a stand-in … in trace output" applies to code only. | AC16, AC17 |
| RR1b | — | R2 uses the OpenAI embedding model in the suite. AC2 and AC3 become `live` (AC2 asserts only that P03 ranks first; AC3 drops the `stand_in` check). AC6's `retrieved_ids` assertion is dropped. AC3's "two embeddings of P03 are identical" may not hold for hosted embeddings, and this spec does not restate it. Every criterion that builds the index (AC1, AC4–AC17) then needs the provider key, so R11's "runs with no API key" and AC18's keyless pass no longer hold for those criteria. | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15, AC16, AC17, AC18 |
| RR2b | — | AC4–AC8, AC11–AC17 become `live` and are re-asserted by behavior: AC6 abstains; AC7 names the Coastal Sun Shirt; AC8's T4 answer contains "Priya"; AC11 counts whatever parse errors occur; AC13 checks report shape and totals arithmetic; AC14 checks one grader call per example; AC16 checks event order and that P02 is retrieved. AC9 becomes `live` with AC8 (its Given is AC8's session) and still checks the empty conversation section; AC10's "the scripted model records 0 calls" has no scripted model to read under RR2b, and this spec does not restate it. | AC4, AC5, AC6, AC7, AC8, AC9, AC11, AC12, AC13, AC14, AC15, AC16, AC17 |

## Course Context Pack (embedded — agent-readable)

### CTX-A. The pattern

`load → (split) → embed + store → retrieve → stuff + generate → converse → evaluate`, with inspection available at every step.

- **Load** — each catalog record becomes a document. The model has to be given data it was never trained on.
- **Split** — needed only when documents are too large to pass whole. "Language models can only inspect a few thousand words at a time." The course's records were small enough to skip it (row D1).
- **Embed + store** — each document becomes a vector that captures its meaning, and the vectors are held in a vector store. Similar text gives similar vectors, so relevance becomes a distance.
- **Retrieve** — the question is embedded the same way, compared with every stored vector, and the n most similar documents are picked. "The returned values can now fit in the LLM context."
- **Stuff + generate** — the retrieved documents are put into one prompt with the question and a grounding instruction, and the model answers in one call (row D2).
- **Converse** — the model is stateless, so memory supplies earlier turns as context, within a cost bound (row D3).
- **Evaluate** — examples are written by hand and by a model, the pipeline predicts each answer, and a model grades the predictions by meaning. String matching cannot judge open-ended text.
- **Inspect** — a step trace shows what went in and out of each step. A wrong answer often comes from retrieval, not from the model.

The course frames the components as models, prompts (reusable templates), output parsers (model text → structured data), memory, chains (a model plus a prompt, composable), indexes, and agents (the model as a reasoning engine that picks tools). This build uses all of them except agents (§1).

### CTX-B. Failure-mode catalog

- **B1. Text that looks like data.** *Symptom:* reading a field from the model's reply raises an error. *Cause:* the reply looks like JSON but is a string. *Fix:* put format instructions in the prompt and parse the reply into the declared shape; record replies that do not parse. *Enforced by R4 / AC11, AC12.* (Lesson 2, where it is planted.)
- **B2. The stateless model forgets.** *Symptom:* the assistant cannot recall the user's name. *Cause:* each model call is independent. *Fix:* render memory into every prompt. A window that is too small forgets too: at k = 1 the course's assistant answered that it did not have access to that information. *Enforced by R6 / AC8.* (Lesson 3.)
- **B3. Misaligned variable names.** *Symptom:* key errors when one step's output feeds another. *Cause:* output and input names do not line up exactly. *Fix:* templates declare their variables, and building with a missing one fails loudly before any call. *Enforced by R5 / AC10.* (Lesson 4: "if you get any key errors, you should definitely check that they are lined up.")
- **B4. Exact-match grading.** *Symptom:* correct answers are graded wrong. *Cause:* a reference "Yes" and a correct long sentence share no characters; "there's no single one truth string." *Fix:* grade by meaning with a model grader. *Enforced by R8 / AC13, AC14.* (Lesson 6.)
- **B5. Invented answers.** *Symptom:* a confident answer to something the catalog does not contain. *Cause:* nothing tells the model to abstain. *Fix:* the grounding instruction — use only the given context; say you don't know rather than make up an answer. *Enforced by R1 / AC5, AC6.* (Lesson 6's trace of the course's Q&A prompt.)
- **B6. Blaming the wrong step.** *Symptom:* a wrong answer. *Cause:* often retrieval, sometimes the model; the final answer alone cannot tell which. *Fix:* inspect the retrieved context and the full prompt. The fixture plants a model miss on a question whose record is retrieved correctly. *Enforced by R9 / AC16.* (Lesson 6.)

### CTX-C. Decision background

**How to read the provenance notes.** Each subject the course argued was sorted by a three-step *litmus*:
1. **Failure** — the course shows or warns that one side breaks. That side is the *anti-pattern*, and the other side is *baked in* as a business rule (a *bake-in*; tie-breaker 1: a demonstrated failure wins over earlier demos of the same side).
2. **Working** — the course shows the other side working. Both sides are real options, so the subject is a Ledger *row*.
3. **Never shown working** — the other side is argued but never built. It becomes a row option marked never-built when choosing it would change a box, an owner or a guarantee in the architecture. Otherwise it is *narrative*.

Other terms used in these notes:
- **Lever** — a subject whose sides differ only in a number (tie-breaker 2). It is a body default plus an Ask-First entry, not a row. A *post-build lever* is such a value, tuned after the build without a build-start question.
- **Lever-value selection** — when the course itself sets a value inconsistently, it is chosen by: (1) the value the narration states where the concept is introduced; (2) else the end-to-end application's config; (3) else the most frequent, earliest-taught value.
- **Stakes test** — a contradiction becomes a row only if picking the other side at the start would change structure or a guarantee.
- **Degenerate case** — an "alternative" that is just the taught mechanism on a trivial workload. It is not a second side.
- **Narrative** — a subject the course raised but did not argue as a builder's choice, or an alternative it argued but never showed working on a subject that changes no box, owner or guarantee, or a stage of its progression it does not argue stopping at. It is background only, never asked and never built. In this spec, narrative also covers subjects that live only in the parts §1 leaves out.
- **Heavy bar** — a realization is heavy only if it needs a credential, a paid account, admin or container setup, or special hardware. Network access alone is not heavy.
- **Substitution row** — a row whose Default replaces a heavy course realization with the lightest one that keeps the row's Invariant.
- **Realization tiers** — lightest first: (1) the language's standard distribution; (2) an embedded library; (3) a locally served component.
- **Provenance labels** — *Course-demonstrated* marks content traceable to the course materials; *project hardening* marks a constraint this spec adds that the course did not teach. *The generator's reading* marks a number this spec chose to quantify the course's words. A *body default* is a value set in the spec body (§2–§5) rather than as a Ledger row.
- **Categories** — *design-argued* (the course argued the trade-off), *design-structural* (changes the architecture), *realization* (a heavy-dependency substitution), *contradicted* (the course set it both ways), *learner* (the learner's own context).

**Mined spoken trade-offs** (every one, with its disposition):

| # | Trade-off as the course argued it | Lesson | Disposition |
|---|---|---|---|
| T1 | Temperature 0 for less random output vs the 0.7 default | 2 | lever R7 (tie-breaker 2: sides differ only in a value) |
| T2 | High temperature (0.9) "so that we can get some fun descriptions" | 4 | lever R7 (tie-breaker 2) |
| T3 | Prompt templates vs plain f-strings: templates make long prompts reusable; direct API calls vs the framework | 2 | narrative — not a choice this build offers: either way the system is identical (same boxes, owners, guarantees), and the framework itself is a §2 pin |
| T4 | Reading the raw reply as data vs parsing with an output parser | 2 | bake-in R4 (tie-breaker 1: the raw-string side is shown failing) |
| T5 | Full buffer vs window vs token buffer vs summary buffer memory | 3 | row D3 |
| T6 | Window k = 1 in the demo vs "set to a larger number" in practice | 3 | lever (k = 2 under D3b; tie-breaker 2; the number is the generator's reading of "a larger number") |
| T7 | Token limits: token buffer 50 vs 100 narrated; summary buffer 400 narrated vs 100 | 3 | lever (tie-breaker 2); values in "Contradictions" below |
| T8 | Vector-data memory, entity memory, several memories combined | 3 (slide) | row D3 (options D3e, D3f; litmus step 3: never shown, structural) |
| T9 | Storing the whole conversation in a key-value or SQL database for auditing | 3 (slide) | row D4 (presented, not argued; enters as structural) |
| T10 | SimpleSequentialChain (single input/output) vs SequentialChain (multiple) | 4 (slides) | no row: the simple form is the degenerate single-variable case of the general one; outside the build (§1 item 3) |
| T11 | Router chain with a default chain for inputs that fit no subject | 4 (slide) | narrative — outside the build (§1 item 2) |
| T12 | One-line index creation vs the step-by-step build: "these two things equate to the same result" | 5 | narrative — not a choice this build offers: the same system either way |
| T13 | Chunking large documents vs not chunking small ones | 5 | row D1 (litmus step 3, structural) |
| T14 | In-memory vector store: "doesn't require connecting to an external database"; other stores can be swapped in | 5 | narrative — presented, not argued; §2 pin; §1 item 10 |
| T15 | Stuff vs map-reduce vs refine vs map-rerank | 5 (slides) | row D2 (litmus step 3, structural) |
| T16 | Hand-written vs model-generated evaluation examples | 6 | row D5 |
| T17 | Grading by hand: "starts to get a little bit tedious" | 6 | narrative — never shown, and described only as a step on the way to model grading |
| T18 | Exact string / regex matching vs model grading | 6 | bake-in R8 (tie-breaker 1: the course warns string matching "wouldn't know what to do") |
| T19 | Final answer only vs step trace | 6 | row D6 |
| T20 | Hosted evaluation platform vs in-notebook trace | 6 | row D6 (option D6b) |
| T21 | The model as knowledge store vs reasoning engine | 7 | narrative — framing for agents, outside the build (§1 item 1) |
| T22 | Agents are exploratory: one needed extra lookups after a wrong first conclusion | 7 | narrative — outside the build (§1 item 1) |
| T23 | A tool's detailed description decides when and how the agent calls it | 7 | narrative — outside the build (§1 item 1) |
| T24 | Built-in prompts get an app working fast vs engineering your own | 2 | narrative — presented, not argued as a choice in this build |

**Contradictions in the materials** (each with both sources; none passes the stakes test, so none is a row):
- *Document separator* — the Lesson 5 Q&A chain uses the framework default; the Lesson 6 evaluated chain sets `<<<<>>>>>`. This is a near-equivalent value. The narration states none, so it is chosen by the end-to-end application's config: `<<<<>>>>>` (R3), a post-build lever.
- *Token-buffer limit (D3c)* — the code uses 50. The narration says 50, then "if I increase the token limit to 100, it now has the whole conversation." The narration conflicts with itself, so the end-to-end config value of 50 is used. This is a lever.
- *Summary-buffer limit (D3d)* — the code uses 100. The narration says "a max token limit of 400 in this case", then reduces it to 100. The narration conflicts with itself, so the code value of 100 is used. This is a lever.
- *Agent tools* — the narration loads "DuckDuckGo search and Wikipedia" and asks about the 2022 World Cup. The code loads a math tool and Wikipedia and asks "What is the 25% of 300?". This is outside the build and recorded only.
- *Lesson numbering* — notebook files are numbered 1–6, while the transcripts count an Introduction as Lesson 1, so the notebooks are Lessons 2–7. The transcripts win (CTX-E).

**Agents background (for a restored §1 item 1).** The course initialized a chat-tuned ReAct-style agent with a math tool and an encyclopedia tool, with parsing-error handling on ("handle_parsing_errors=True"). It added a custom date tool whose description says its input "should always be an empty string". It ran a Python-code agent that sorted a list of customer names. The notebook warns: "The agent will sometimes come to the wrong conclusion … try running it again."

**Course name-map** (provenance, not binding unless noted):
- The course's catalog file was a 1,000-row outdoor clothing CSV, and its chain-lesson data was a product/review CSV.
- Generated-example keys `query`/`answer` are **binding** in GeneratedExample; the course's prediction key was `result`.
- The review-extraction fields were `gift` (true/false; false when unknown), `delivery_days` (−1 when not found) and `price_value` (a list of sentences).
- The sequential-chain output keys were `English_Review`, `summary`, `language` and `followup_message`.
- The router destinations were physics, math, History and computer science, with `DEFAULT` as the fallback. Its output fields were `destination` and `next_inputs`.
- The custom tool was named `time`. The platform session was named "deeplearningai".
- Presentation-only values from the out-of-build lessons are dropped deliberately: a 20-word company description, a one-sentence review summary, and the demo customer list.

### CTX-D. Perishable assumptions

Treat these as search keywords against current docs, not guaranteed imports. The concepts in CTX-A to CTX-C are durable; only these names are perishable.

- **Versions:** the course notebook ran on langchain 0.0.179 and openai 0.27.7 (pre-1.0 SDK, `openai.ChatCompletion.create`), and its installs were unpinned.
- **Models:** `gpt-3.5-turbo`, chosen by a date check that used `gpt-3.5-turbo-0301` before 2024-06-12. `text-davinci-003` was retired on 2024-01-01 and replaced by `gpt-3.5-turbo-instruct` for the one-line index query. The embedding vectors have "over a thousand" elements.
- **Class and function names:** `ChatOpenAI`, `ChatPromptTemplate`, `ResponseSchema`, `StructuredOutputParser`, `ConversationChain`, `ConversationBufferMemory`, `ConversationBufferWindowMemory`, `ConversationTokenBufferMemory`, `ConversationSummaryBufferMemory`, `LLMChain`, `SimpleSequentialChain`, `SequentialChain`, `MultiPromptChain`, `LLMRouterChain`, `RouterOutputParser`, `RetrievalQA` (chain type "stuff"), `CSVLoader`, `DocArrayInMemorySearch`, `VectorstoreIndexCreator`, `OpenAIEmbeddings`, `QAGenerateChain` (with `apply_and_parse`), `QAEvalChain`, `langchain.debug`, `load_tools`, `initialize_agent`, `AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION`, `create_python_agent`, `PythonREPLTool` and the `@tool` decorator.
- **Call styles:** `.run`, `.predict`, `chat(messages)`, `call_as_llm`, `index.query`.
- **Request-parameter compatibility:** some newer model families reject a non-default `temperature`. If the model chosen at the gate does, record that in the checklist, drop the parameter for that role, and list R7 and AC15 under *Adapted*.

### CTX-E. Provenance map

Lesson numbers and titles follow the transcripts. Nothing in this spec requires platform access.

| Lesson (transcripts) | Notebook | Feeds |
|---|---|---|
| 1. Introduction | — | CTX-A component framing |
| 2. Models, Prompts and parsers | L1 | CTX-B1; R4, R7; T1, T3, T4, T24; name-map review fields |
| 3. Memory | L2 | CTX-B2; R6, R12; rows D3, D4; T5–T9 |
| 4. Chains | L3 | CTX-B3; R5; T2, T10, T11; name-map chain keys and router |
| 5. Question and Answer | L4 | CTX-A; R1 (instruction seen in 6), R2, R3, R10; rows D1, D2, RR1; T12–T15 |
| 6. Evaluation | L5 | CTX-B4, B5, B6; R1, R3 separator, R8, R9; rows D5, D6; T16–T20 |
| 7. Agents | L6 | Agents background; T21–T23; §1 item 1 |
| 8. Conclusion | — | §1 framing (the course's three application kinds) |

**Slides read** — all video-shown, so each ranks with its lesson's transcript:
- `memory_1` (stateless model, full conversation as context — Lesson 3) and `memory_2` (additional memory types and conversation database — Lesson 3).
- `chains_1`–`chains_3` (sequential chains — Lesson 4, narrated "we can look at the slide") and `chains_4` (router chain — Lesson 4).
- `question_and_answer_1`–`4` (LLMs on documents, embeddings, vector database create/index/process — Lesson 5), `question_and_answer_5` (stuff method pros and cons — Lesson 5) and `question_and_answer_6`, `7` (map-reduce, refine, map-rerank — Lesson 5; slide 6 is a cropped duplicate of 7).

No deck-only slide was supplied, so no slide conflicts with code or narration.

---
*v1 · LangChain for LLM Application Development · learner project: [outdoor-gear catalog Q&A assistant] · Living document: when the building agent produces something unexpected, add the missing constraint here and re-run.*
