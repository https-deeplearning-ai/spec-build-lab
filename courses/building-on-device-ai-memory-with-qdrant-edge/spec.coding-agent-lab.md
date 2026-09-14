# Spec: On-Device Memory Assistant — Standalone Takeaway

> **What you're building.** A small app you open in the preview pane, type *"what is the tool cage combination?"* into, and watch answer with the note you actually wrote — alongside the photo it matched from the same question — then show it two pictures of a part it has never seen, give the part a name, show it a third picture, and watch it name the part correctly. No language model is involved at any point: the whole thing is vectors, a local store, and a threshold.
>
> **Fastest path.** Answer the gate's first question with **recommended baseline build** and every decision below resolves to its default; that builds the app end-to-end. The build is **complete when the offline acceptance suite passes**. There is no key to unlock anything here — this pipeline calls no paid service and reads no credential (R15).
>
> **This file is self-contained.** The Course Context Pack at the end replaces every reference to the course: you need no notebooks, no videos, no platform access. Anchors like (CTX-A) point into it.
>
> **The Decision Ledger below holds every point where this build could diverge**, each pinned to exactly one course-derived default, so the spec builds and evaluates as-is with no intake. The **Environment Resolutions** table under it records the six learner-context dimensions and what the lab resolved each one to.
>
> **Provenance.** Generated from the *Building On-Device AI Memory with Qdrant Edge* notebook dump, lesson transcripts and slide descriptions on 2026-09-14. Spec-generation guide `8e44ecb`; `coding-agent-lab` overlay `58ecfb9`.

---

## 0. Before you build — REQUIRED (do this first)

You are the build agent. Before writing ANY code, you MUST surface the design decisions
in the Decision Ledger (next section) to the person you are building for. Do **not** skip
this because the defaults look complete — the defaults exist so the build is *reproducible*,
not because they are the right choice for this person's project.

1. **Use a structured question tool if you have one.** This environment has one: a fenced block
   whose info-string is the word `choices`. Put your explanation in prose **above** the fence, make
   the fence the **last** thing in the message, put **one option per line**, and end your turn
   there. Precede the fence with a line of the form `**Question N of M — <decision>**` so both you
   and the person can see that nothing was skipped. A click sends the option line verbatim, and a
   typed answer naming an option counts **identically** — accept either. Only the buttons in your
   **latest** message stay live, so never ask anyone to scroll back and change an earlier answer:
   re-ask it as a new question instead. (If you are somewhere without such a tool, list the rows in
   your reply and ask the person to respond to each.)
2. **First question — recommended baseline build, or customize?** Ask exactly one question with
   two options: the **recommended baseline build** — every Ledger row resolves to its Default:
   mostly the course's own choices, with a lighter stand-in wherever the course's choice needs
   setup you may not have (a paid API key, an admin-provisioned service); the step-5 checklist
   marks exactly where the baseline differs from the course — or **customize** the decisions row
   by row. If the person chooses the baseline, skip step 3 — go straight to the step-5 checklist
   and build. If the person chooses customize, continue with step 3.
3. **Present the Ledger ONE ROW AT A TIME — one question per row.** For each row ask a single
   question: the **Decision** as the prompt, its **Options** as the choices. Append
   "(course default)" to the option the course actually used — on a substitution row that is
   the course-faithful Options entry, not the Ledger Default. You may also mark an option
   "(Recommended)" — your judgment for THIS person's context, made now, at gate time; with no
   contextual reason to depart, recommend the row's Default. When your recommended option IS
   the course's actual choice, merge the labels into "(Recommended - course default)". A
   recommendation never removes or moves the "(course default)" label, and no option is ever
   labeled with a bare "(default)" — these two labels and their merged form are the only
   option labels. Use the answers already given to frame later questions and describe options in
   the person's own terms — but never skip a row, drop or alter an Option, or move the
   "(course default)" label because of an earlier answer. Put any realization beyond the tool's
   option slots (or the free-form case) under a free-text option. Ask about **every** row. A
   per-call item limit is NEVER a reason to drop, skip, merge, or silently default a row — make as
   many separate calls as there are rows.
4. **Presenting any of these questions ENDS YOUR TURN — stop here; write no code, create or edit
   no file, take no other build action.** Keep asking, one row at a time, until **every** row has
   an answer (a chosen option, an explicit "use the course default", or the step-2 baseline answer,
   which resolves every row at once). Answers to *some* rows do NOT release the build; "no reply
   yet" is not an answer — wait for the person.
5. **Before the first line of code, print a resolved-decision checklist and write it to
   `resolved-decisions.md`** — every Ledger row with its final value (the person's choice, or its
   Ledger default), each line carrying a deviation mark: `= course choice`, or
   `≠ course choice (course used: <option>)`. If the baseline path was chosen, walk the person
   through every `≠` row — the course's actual choice, and why this build's default substitutes it
   (the row's Trade-off/branch note says why) — before building. Begin implementation ONLY after
   this checklist is shown and written; if any row is unresolved you are not done — return to
   step 3. Build on the checklist's values.

   **Why the file, not just the print, is load-bearing here** `[environment]`: in this workspace a
   new chat begins with no memory of this one, and a reviewer sees only what is on disk. Values
   left in chat are gone. `resolved-decisions.md` is a record, not an input — a later build re-runs
   this gate rather than reading the file back.

---

## Decision Ledger (§0 above requires the build agent to present these before building)

These are the points where this build could diverge. Every row has a course-derived default, so
the spec is buildable and evaluatable as-is; change a row only when applying to a real project or
when you have reason to prefer another option.

| # | Category | Decision | Invariant (must hold) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| D1 | learner | **Encoder set** — which text encoder, which image encoder, which speech-to-text model the pipeline runs on | The image encoder MUST share one vector space with a text encoder, so a text query can be searched against image vectors. Every encoder MUST run locally with no account, key or paid service. Each named vector space's declared width MUST equal its encoder's output width. A speech-to-text model MUST be available for the voice lane. | Nomic `nomic-embed-text-v1.5` (768-d) for notes and text questions; CLIP ViT-B/32 vision + text towers (512-d) for photos and photo-searching text; `whisper-base` for voice notes — all served locally through the course's own runtimes, no key. | (a) the course's three local models **(course default)**; (b) any other pair of local encoders where the image side is a shared-space dual-tower model, plus any local ASR; (c) a larger or GPU-class encoder — *impractical in this environment: CPU-only, and container memory is shared with the coding agent's process (R18)* `[environment]`; (d) a hosted embedding API — *impractical here: it breaks the offline invariant of D3 and needs a credential this build must not read (R15)* `[environment]`. | Changing either encoder means **re-embedding every stored memory** and **re-calibrating the recognition threshold** (D4): the widths change, the score scale changes, and the old vectors are unreadable in the new space. Changing the ASR model changes what a voice note's stored text says. | course+learner |
| D2 | learner | **Scope boundary** — the build's exclusion list. **Present the §1 "Not Included" list inside this question**, item by item, so the person is amending a list they have actually seen. | *(empty — the pattern imposes no capability requirement on this dimension)* | Keep as-is: every §1 exclusion stands and the full acceptance set (AC1–AC18) is built. | (a) keep the exclusion list as-is; (b) bring one or more excluded items back — say which, and you will be told how each is handled; free text also accepted for an *additional* exclusion, which must name the acceptance criteria it retires. Handling rules: *additive and owned by no other row* (e.g. a per-memory edit action) → restorable here; *named by the course but never built* (cloud sync beyond D3; live camera-frame recognition on a loop) → buildable, but this spec supplies no parameters and no acceptance criteria for it; *owned by another row* (cloud sync itself → D3; a different encoder → D1; where taught objects live → D5) → decided there, not here; *outside this build mode* (grafting the pattern into an existing codebase) → unavailable. | Restoring an item adds build time and unspecified behavior; adding an exclusion retires the acceptance criteria that covered it, so the oracle gets weaker. | learner |
| D3 | design-argued | **Memory locality** — does memory live only on the device, or also sync to a central server | Every read the app performs at query time MUST be served from the local on-disk store, with no network call in the retrieval path. | On-device only: one embedded, in-process store written to a directory on disk; no server, no sync. | (a) on-device only **(course default)**; (b) on-device plus optional one-way sync of selected memories to a central Qdrant cluster — *heavy setup: a provisioned cluster plus a URL and an API key supplied as environment variables; the course ships client helpers for this but this copy of the materials contains no working demonstration of it*; (c) cloud-only storage — *contradicts this row's invariant; listed for completeness, not selectable*. | Lesson 1 argues both sides aloud: on-device "can work without an internet connection… recall can be a lot faster and a lot more reliable… your private memories stay private without any cloud storage or API required", while "cloud storage can still be useful when some memories need to be shared" and local devices "have some limitations like less compute and less storage" — the instructor's conclusion is "for today, we will only be working locally… you can always use cloud and local retrieval combined together if your use case requires it" (Lesson 1; the architecture slide for Lesson 2 labels the server link "optional sync"). Switching on sync moves private memories off the device and puts a credential in the loop; switching it off later does not un-send them. | course+learner |
| D4 | design-argued | **Recognition threshold** — the similarity score a photo must reach before the app names what it is seeing | A recognition answer MUST be a decision against a threshold, not the bare nearest hit: below the threshold the app answers UNKNOWN. The threshold's value MUST come from the calibration procedure (R10), not from a guess. | `0.80`, sitting between the calibrated fixture corpus's highest non-match and lowest held-out match, exactly as the course sets it (`THRESHOLD = 0.80`, Lesson 5 §3). | (a) the calibrated midpoint, `0.80` **(course default)**; (b) a higher threshold — fewer false positives, more UNKNOWN answers; (c) a lower threshold — fewer UNKNOWN answers, more confident wrong names; (d) recalibrate against your own photos and take the new midpoint. | Lesson 5 argues this aloud as a genuine choice rather than a fixed number: the calibration run put "the lowest scoring match at 0.86, and the highest non-match at 0.74. So 0.8 is the right middle for the threshold **in my use case**. Depending on the significance of false positives and false negatives, for your use case, you can select a threshold that fits your use case the best." Moving it re-trades false positives against false negatives and changes the abstention guarantee — and no acceptance criterion fails when you get it wrong, which is why it is also an Ask-First entry (§6). | course+learner |
| D5 | design-structural | **Where taught objects live** — a dedicated object store, or the one assistant store alongside the day's memories | A taught subject MUST be retrievable by an image query, and a taught view MUST be distinguishable from a captured day photo by payload alone. | One combined store: the taught object is written into the same store as the day's memories, as a **single point carrying both an image vector and a text vector**, so it can be reached by sight or by words. This is what the course's end-to-end assistant does (Lesson 5 §4 and §6). | (a) one combined store **(course default)**; (b) a dedicated image-only object store beside the memory store, queried separately — also what the course does, for the teach-and-calibrate stage (Lesson 5 §1–§3). | Redrawing the diagram changes a box: two stores or one. A dedicated object store keeps taught views out of ordinary photo recall and lets the calibration sweep run in isolation; one combined store means a photo question can return a taught view — which is exactly what the course's closing table leans on when it marks a question answered by the same memory from both lanes. Moving taught objects between stores after they exist means re-embedding and re-writing them. | course+learner |
| D6 | contradicted | **Photo payload shape** — what a photo memory carries besides its vector | A photo memory MUST be reachable by the same payload filters and the same ranking formula as a text memory, or it silently drops out of both. | The full memory record: id, source type, category, location, timestamp, and the optional price/place fields — the shape Lessons 4 and 5 store photos with, in the end-to-end application. | (a) the full memory record **(course default, Lessons 4 and 5)**; (b) filename plus source type only — the shape Lesson 3 uses when it bulk-loads its image bank. | The course sets this both ways: Lesson 3's bulk photo write stores `{file, source_type}` and nothing else, while Lessons 4 and 5 store the photo's whole record. The two return **different result sets to the same read**: a filtered query cannot match a payload that has no category or price, and the freshness formula treats a memory with no timestamp as current, so filename-only photos float to the top of a recency-ranked result forever. Choosing the thin shape up front and wanting filters later means re-ingesting every photo. | course |

---

## Environment Resolutions

This spec was generated for the **`coding-agent-lab`** environment. All six learner-context
dimensions were derived from the course materials first, exactly as the agnostic guide requires,
and then resolved against what this lab actually fixes — derived and resolved, never skipped.

| Dimension | Resolution | Where the Invariant lives now |
|---|---|---|
| project | **ANSWERED** — the lab fixes the assignment | §1 Objective. The derived Invariant was empty (the pattern imposes no capability requirement on which project is built), so there is nothing to exercise; no AC is owed. |
| data/inputs | **ANSWERED** — inputs are seeded into the workspace as the fixture corpus | §5 fixture corpus + the §3 schema. Invariant: *every memory carries a text body or an image, an integer timestamp, and at least one filterable payload field* — exercised by AC5 (filter), AC6 (photo filter), AC9 (freshness reads the timestamp). |
| goal | **ANSWERED** — the lab fixes what "working" means | §1 Objective + AC1–AC18. Invariant: *success must be expressible as "the correct stored memory is returned and its score clears its lane's cutoff"; the pipeline generates no new text* — exercised by AC7 (per-lane cutoffs), AC11 (abstain below threshold), AC16 (no generated field, no provider call). |
| model/provider | **KEPT** — this pipeline needs no LLM, so the dimension is about the course's *own* encoders, which this lab does not fix | Ledger row **D1**, with its course-derived default and a real switching cost. The lab's ambient provider keys are covered separately by business rule **R15**. |
| environment | **ANSWERED** — the container | §2 Tech Stack + the *Runtime* subsection of §2. The derived capability invariants moved to the rows and rules that need them: *memory survives process restart* and *no server, no network in the retrieval path* → **D3** Invariant and **R12** (AC14); *CPU-only, memory shared with the agent's process* → **R18** (AC8) and §2. |
| scope-boundary | **KEPT** — the lab has no opinion about how much of the build the person wants | Ledger row **D2**. Its derived Invariant was empty and stays empty. |

---

## 1. Objective

A single-process, offline personal-memory assistant: it stores a day's captures — typed notes,
transcribed voice notes, and photos — as points in one local vector store, answers a typed question
by retrieving the nearest memories in a text lane and a photo lane at once, prefers recent memories
over stale ones, and learns to recognize a new physical subject from two example photos without any
training, retraining or language model (pattern: CTX-A).

### Not Included ★

1. Any large language model, chat completion, summarization, or generated prose. The app returns
   stored memories and scores; it never writes a sentence of its own.
2. Any fine-tuning, retraining, or gradient step. "Teaching" means writing example vectors.
3. Live camera capture, video, or frame-by-frame recognition on a loop.
4. Real hardware — cameras, single-board computers, enclosures, or a phone client.
5. Cloud storage, cross-device sync, or snapshot transfer (owned by Ledger **D3**; off by default).
6. Multi-user accounts, authentication, or per-user memory separation.
7. Editing or re-labelling a stored memory in place; the app can add and delete, not amend.
8. Audio playback or audio storage — a voice note is stored as its transcript only (R3).
9. Performance work: benchmarking, index tuning, quantization, or a store large enough to need it.
10. Grafting this pattern into an existing codebase. This spec builds a standalone app.

### Adapting this beyond the lab

Four of the six learner-context dimensions were answered by this environment rather than by you.
If you take this spec somewhere else, these are the places to change:

- **The project** is fixed by §1 above. Replace §1 and the fixture corpus together; the Ledger and
  the rules survive unchanged.
- **The data** is fixed by the §5 fixture corpus and the §3 schema. Point the loader at your own
  records; keep the schema's requirement of a timestamp and a filterable field, or R5 and R8 stop
  being testable.
- **The goal** is fixed by §1 plus AC1–AC18. If your definition of "working" needs generated text,
  you have left this pattern — R14 is the boundary.
- **The runtime** is fixed by §2's *Runtime* subsection and by R15–R17, all marked `[environment]`.
  Off this platform, R16 (relative URLs) and R17 (one server on port 4000) become ordinary
  deployment choices, and R15's prohibition on reading ambient provider keys becomes moot.

The two dimensions that stayed yours are the **encoder set** (D1) and the **scope boundary** (D2).

---

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language / runtime | Python 3.12 or newer | The container ships Python 3 with `venv`. Create the venv with `--system-site-packages` so the preinstalled packages stay reusable. `[environment]` |
| Memory store | `qdrant-edge-py` 0.7.2 | The embedded, in-process engine the course is built on — a library, not a server; its data is a directory on disk. Chosen by Ledger **D3**; change it there, not here. **The course's `requirements.txt` pins every version exactly, and says so on purpose — "every version below is pinned to the one the notebooks were run with, so the scores printed in the saved outputs reproduce exactly"; those saved outputs are not present in the supplied materials, so no score in this spec is quoted from them.** Era-specific class and model names are in **CTX-D** — treat them as search keywords against current docs, not guaranteed imports. |
| Text encoder | `fastembed` 0.8.0 → `nomic-ai/nomic-embed-text-v1.5`, 768-d | Ledger **D1**. Document and query embeddings use different task prefixes — use the library's query-embedding path for questions so scores line up (CTX-C1). |
| Image encoder | `fastembed` → `Qdrant/clip-ViT-B-32-vision` and `Qdrant/clip-ViT-B-32-text`, 512-d | Ledger **D1**. Two towers, one space: that is what makes a typed question searchable against photos. |
| Speech-to-text | `onnx-asr` 0.12.0 → `whisper-base`, CPU execution provider | Ledger **D1**. Used once per voice fixture at ingest; released before the encoders load (R18). |
| Model runtimes | `onnxruntime` 1.27.0, `tokenizers` 0.23.1 | The course pins these alongside the models because they decide the embedding numbers. |
| Imaging | `Pillow` 12.3.0 | Fixture image generation and page thumbnails. |
| Numerics | `numpy` 2.5.1 | |
| Web layer | `fastapi` + `uvicorn` | Already in the container. One process serves both the page and the API. `[environment]` |
| Tests | `pytest` | Not preinstalled; part of the install batch. |

**Secrets.** This build needs none. No key, no token, no `.env` entry is required, read, or written.
The container exports provider API keys and base URLs for other kinds of app; this one must not
read them (R15). Nothing is ever hardcoded.

### Runtime `[environment]`

- Debian container, non-root user, CPU only. Node 22 and sqlite3 are present but unused here.
- **Preinstalled and reusable:** `fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`.
  **Nothing in the memory or ML stack is preinstalled** — no vector store, no embedding models, no
  ML framework. Everything in the table above beyond FastAPI/uvicorn is an install.
- Outbound network works, so the installs and the one-time model downloads succeed, but each costs
  wall-clock time inside the session. **Batch them: one `pip install` and one warm-up run that
  fetches all three models, both announced with their cost before you start.** After that warm-up
  the app and its whole test suite run with no network at all.
- Container memory is shared with the coding agent's own process. R18 exists because of this.
- Serving and preview: R16 and R17 are not notes, they are business rules with acceptance criteria.

---

## 3. Input/Output Contracts ★

The memory record — the unit the loader reads, the store's payload, and the API's output row:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "memory-record",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "source_type", "category", "timestamp"],
  "properties": {
    "id": { "type": "integer", "minimum": 0 },
    "source_type": { "enum": ["text", "voice", "photo"] },
    "category": { "type": "string", "minLength": 1 },
    "location": { "type": "string" },
    "timestamp": { "type": "integer", "minimum": 0,
      "description": "epoch seconds; required so freshness ranking and date filters can read it" },
    "note": { "type": "string", "minLength": 1 },
    "transcript": { "type": "string", "minLength": 1 },
    "audio_file": { "type": "string" },
    "file": { "type": "string" },
    "label": { "type": "string", "description": "present only on a taught subject" },
    "price": { "type": "number", "minimum": 0 }
  },
  "allOf": [
    { "if":   { "properties": { "source_type": { "const": "text" } } },
      "then": { "required": ["note"],
                "not": { "anyOf": [ { "required": ["transcript"] }, { "required": ["file"] } ] } } },
    { "if":   { "properties": { "source_type": { "const": "voice" } } },
      "then": { "required": ["transcript", "audio_file"],
                "not": { "required": ["note"] } } },
    { "if":   { "properties": { "source_type": { "const": "photo" } } },
      "then": { "required": ["file"],
                "not": { "required": ["transcript"] } } }
  ]
}
```

The store's declared shape — one store, two named vector spaces, both cosine:

```json
{
  "$id": "store-config",
  "type": "object",
  "additionalProperties": false,
  "required": ["vectors", "payload_indexes"],
  "properties": {
    "vectors": {
      "type": "object",
      "additionalProperties": false,
      "required": ["text", "image"],
      "properties": {
        "text":  { "const": { "size": 768, "distance": "cosine" } },
        "image": { "const": { "size": 512, "distance": "cosine" } }
      }
    },
    "payload_indexes": {
      "type": "array",
      "minItems": 2,
      "items": { "enum": [
        { "field": "category", "kind": "keyword" },
        { "field": "price", "kind": "float" } ] }
    }
  }
}
```

The recall response — two lanes, never blended, and no generated text anywhere in it:

```json
{
  "$id": "recall-response",
  "type": "object",
  "additionalProperties": false,
  "required": ["question", "lanes"],
  "properties": {
    "question": { "type": "string", "minLength": 1 },
    "lanes": {
      "type": "object",
      "additionalProperties": false,
      "required": ["words", "picture"],
      "properties": {
        "words":   { "$ref": "#/$defs/lane" },
        "picture": { "$ref": "#/$defs/lane" }
      }
    }
  },
  "$defs": {
    "lane": {
      "type": "object",
      "additionalProperties": false,
      "required": ["cutoff", "hits"],
      "properties": {
        "cutoff": { "type": "number" },
        "hits": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["id", "score", "above_cutoff", "memory"],
            "properties": {
              "id": { "type": "integer" },
              "score": { "type": "number" },
              "above_cutoff": { "type": "boolean",
                "description": "MUST equal (score >= the enclosing lane's cutoff); never computed against the other lane's cutoff" },
              "memory": { "$ref": "memory-record" }
            }
          }
        }
      }
    }
  }
}
```

The recognition response — a decision, not a nearest hit:

```json
{
  "$id": "recognition-response",
  "type": "object",
  "additionalProperties": false,
  "required": ["verdict", "threshold", "score", "nearest_id"],
  "properties": {
    "verdict": { "type": "string",
      "description": "the taught subject's label when score >= threshold, otherwise exactly UNKNOWN" },
    "threshold": { "type": "number", "exclusiveMinimum": 0, "maximum": 1 },
    "score": { "type": "number" },
    "nearest_id": { "type": "integer" },
    "nearest_label": { "type": "string" }
  }
}
```

There is deliberately **no** `answer`, `summary`, or `response_text` field in any contract. The
absence is the guarantee (R14).

---

## 4. Business Rules

Each rule states the behavior and the failure it prevents, with its Context-Pack anchor and its
acceptance criteria. Provenance labels: *course-demonstrated*, *project hardening*, `[environment]`.

**R1. One store, two named vector spaces.** The app creates exactly one memory store holding a
`text` space of 768 dimensions and an `image` space of 512 dimensions, both compared by cosine
distance. A stored memory is one point: an id, one or both named vectors, and a payload holding the
whole memory record. A memory that exists in only one space is still one point, not two.
*Prevents: two parallel stores that drift, and scores from different models landing in one ranking*
(CTX-A). — *course-demonstrated* → **AC1**

**R2. Payload indexes exist before any filtered read.** A keyword index on `category` and a float
index on `price` are created at initialization. A filtered query issued before its field is indexed
is a defect, not a slow path. *Prevents: filters that silently match nothing* (CTX-B3).
— *course-demonstrated* → **AC2**, **AC5**

**R3. A voice memory stores its transcript, never its audio.** Speech-to-text runs once, at ingest;
the text it produces is what is embedded and what is stored. The audio filename is kept as a
provenance pointer only, and the app never plays or serves audio. *Prevents: an unsearchable blob
standing where a searchable memory should be* (CTX-A). — *course-demonstrated* → **AC3**

**R4. The id is the upsert key and is unique across every source type in one store.** Writing a
point with an existing id replaces that memory outright. The fixture loader and every write path
allocate from disjoint id ranges. *Prevents: a photo write silently overwriting a note.*
— *project hardening* (the lessons each use their own id scheme and never collide, but the
materials state no rule; this is added) → **AC4**

**R5. A filter is part of the query, not a pass over the results.** Conditions on payload fields are
evaluated inside the retrieval request, so the similarity search runs only over points that pass
them and the returned set is already both relevant and compliant. Retrieving first and discarding
afterwards is forbidden — it silently returns fewer results than asked for. *Prevents: a "top 3
under $15" that is really "whatever survived of the top 3"* (CTX-B3). — *course-demonstrated*
→ **AC5**, **AC6**

**R6. A photo memory carries the full memory record as its payload.** Every photo point stores id,
source type, category, timestamp and the optional fields, exactly as a text memory does. *Prevents:
photos dropping out of every filtered read and floating permanently to the top of every
recency-ranked read* (CTX-B6, Ledger **D6**). — *course-demonstrated* → **AC6**, **AC10**

**R7. The two lanes are never blended, and each carries its own cutoff.** A question is embedded
twice — once for the text space, once for the image space — and the results are returned as two
separate lanes, each with its own cutoff, each hit flagged against *its own* lane's cutoff. A hit
below its cutoff is returned and marked weak, never silently dropped. Text scores and photo scores
are never sorted into one list and never compared to each other. *Prevents: a photo score of 0.3
being read as "worse" than a text score of 0.6 when the two scales have nothing to do with each
other* (CTX-B2). — *course-demonstrated* → **AC7**

**R8. Text recall ranks by meaning and then by freshness.** The text lane fetches a wider candidate
set by similarity and re-scores it with `similarity + weight × decay(timestamp)`, where decay is
exponential with a seven-day half-life and the weight is bounded so meaning still leads and recency
breaks ties. A memory with no timestamp is treated as current rather than dropped. *Prevents: an
outdated fact winning on wording alone when a current one exists* (CTX-B4). — *course-demonstrated*
→ **AC9**, **AC10**

**R9. Retrieval always returns something; a recognition answer is a decision.** Nearest-neighbour
search has no concept of "no match" — it returns the closest point however far away it is. So the
recognition path compares the top score against the threshold and answers with the subject's label
only when the score clears it; otherwise it answers exactly `UNKNOWN`. *Prevents: the app naming a
thing it has never been shown* (CTX-B1). — *course-demonstrated* → **AC11**, **AC12**

**R10. The threshold is calibrated, not guessed, and must separate.** Calibration scores each
subject's held-out view against its own taught views (the matches) and against every other subject's
taught views and every scene photo (the non-matches), and the chosen threshold must lie strictly
between the highest non-match and the lowest match. If no such value exists, the fixture corpus is
wrong and must be regenerated — the threshold must not be fudged to make a test pass.
*Prevents: a threshold that works on one photo and nothing else* (CTX-C4, Ledger **D4**).
— *course-demonstrated* → **AC13**

**R11. Teaching is writing example vectors.** A subject is taught from **two or more** views; each
view is stored as its own point carrying that subject's label, and recognition takes the best score
across a subject's views. No weights change anywhere in the system. *Prevents: the assumption that
learning a new object requires training* (CTX-A). — *course-demonstrated* → **AC12**, **AC13**

**R12. Memory survives the process.** After every write batch the app compacts the store and flushes
it to disk. A new process opening the same directory sees the same points and answers the same
questions identically. *Prevents: a taught memory lost to a power cut or a restart* (CTX-B7).
— *course-demonstrated* → **AC14**

**R13. Forgetting is real deletion.** Deleting a memory removes its point. It never appears in any
later result, the next-best result promotes into its place, and every other result's score is
unchanged. *Prevents: a "forgotten" memory that is merely hidden* (CTX-B5). — *course-demonstrated*
→ **AC15**

**R14. No language model, anywhere.** The pipeline contains no chat completion, no generation, no
summarization and no fine-tuning. Every string the app shows a user is either the user's own
question or the text of a stored memory. *Prevents: the central claim of this pattern — recall
without an LLM — being quietly falsified* (CTX-A). — *course-demonstrated* → **AC16**

**R15. `[environment]` The ambient provider credentials are not for this app.** The container
exports provider API keys and base URLs. This app must not read them, must not import or call any
LLM provider client, and must never ask anyone for a key. → **AC16**

**R16. `[environment]` Every URL the page requests is relative.** `api/recall`, never `/api/recall`;
`assets/x.png`, never `/assets/x.png`. The preview is reverse-proxied under a path prefix, so a
root-absolute path resolves against the IDE instead of the app. *Prevents: the single most common
way a working app appears broken here.* → **AC17**

**R17. `[environment]` One server, port 4000, bound to `0.0.0.0`, serving both the page and the
API.** HTTP only — WebSocket upgrades are not proxied; streaming responses are fine. Nothing served
any other way is previewable. → **AC18**

**R18. One model family resident at a time.** The speech-to-text model is loaded, used for the whole
voice batch, and explicitly released before either embedding model is loaded. The app never holds
ASR and both encoders in memory simultaneously. *Prevents: exhausting a memory budget shared with
the coding agent's own process — the course releases its speech model for the same reason inside its
own sandbox.* — *course-demonstrated*, reinforced `[environment]` → **AC8**

---

## 5. Acceptance Criteria ★ (the oracle)

### Fixture corpus

Generated by `fixtures/make_fixtures.py` with a fixed seed (`20260914`), written under
`fixtures/`. Every fact below is invented for this spec; none is course data. The generator is
deterministic: re-running it reproduces byte-identical files. **The building agent MUST NOT modify
any fixture to make a test pass** — a failing test means the code is wrong, or (only for AC13) that
the generator is.

`fixtures/day_memories.json` — ten of today's captures, timestamps within a single day:

| id | source_type | category | price | content |
|---|---|---|---|---|
| 1 | text | parts | 9.50 | "Bought two chain links at the counter, nine fifty" |
| 2 | text | parts | 62.00 | "New wheel truing stand quoted at sixty-two" |
| 3 | text | admin | — | "The combination for the tool cage is 8812" |
| 4 | text | repairs | — | "Blue tandem needs its bottom bracket replaced before Saturday" |
| 5 | voice | parts | 4.25 | transcript "Note to self, brake cable housing is four twenty five a metre at the counter" · audio_file `housing.wav` |
| 6 | voice | admin | — | transcript "Remind the volunteers that the cage key moved to the blue hook" · audio_file `cage_key.wav` |
| 7 | text | parts | 21.00 | "Handlebar tape in the back room, twenty one a roll" |
| 8 | photo | repairs | — | file `workbench.png` |
| 9 | photo | parts | 18.00 | file `chainring.png` |
| 10 | photo | admin | — | file `noticeboard.png` |

`fixtures/earlier_days.json` — three memories from twenty-one days earlier:

| id | source_type | category | content |
|---|---|---|---|
| 1001 | text | admin | "The combination for the tool cage is 3940" |
| 1002 | text | repairs | "Red cargo bike collected by its owner" |
| 1003 | voice | parts | transcript "We are down to the last two inner tubes in the small size" · audio_file `tubes.wav` |

Ids 1001 and 3 are the planted freshness case: **near-identical wording, different numbers,
twenty-one days apart.** Their similarity scores to the same question are within noise of each
other, so meaning alone gives no guarantee about which combination comes back — that is the failure
(CTX-B4). Ids 2 and 7 are the planted filter case: both are `parts`, both priced above a $15
ceiling, and both are strong matches for a query about buying parts, so an unfiltered search
surfaces them (CTX-B3). Id 9 is the planted thin-payload case: a `parts` photo with a price, which
only a full-record payload can filter or rank (CTX-B6).

`fixtures/audio/` — four short WAV files (`housing.wav`, `cage_key.wav`, `tubes.wav`, and
`question.wav`, a spoken question), each synthesized by the generator so the speech step is a real
speech step. Each voice record's `transcript` field in the JSON is the *expected* transcript; the
app must produce its own at ingest and store that.

`fixtures/images/` — three scene photos (`workbench.png`, `chainring.png`, `noticeboard.png`),
procedurally drawn: one distinct high-contrast subject shape per file on its own background.

`fixtures/objects/` — four subjects, drawn the same way, each view being the subject's shape with a
small deterministic jitter in position, scale and rotation:

- `hex_nut_1.png`, `hex_nut_2.png` (teach), `hex_nut_3.png` (held out)
- `spoke_wheel_1.png`, `spoke_wheel_2.png` (teach), `spoke_wheel_3.png` (held out)
- `oil_can_1.png`, `oil_can_2.png` (teach), `oil_can_3.png` (held out)
- `tire_lever_1.png` — **never taught**, the abstention probe

### Criteria

| # | Given | When | Then |
|---|---|---|---|
| AC1 | a directory with no store in it | the app initializes | a store exists at that directory declaring exactly two named vector spaces, `text` at 768 dimensions and `image` at 512, both cosine; it reports **0** points. (R1) |
| AC2 | the freshly initialized store of AC1 | initialization completes | the store reports a keyword payload index on `category` and a float payload index on `price`; a filtered query issued before indexing is a build defect. (R2) |
| AC3 | `fixtures/day_memories.json` and `fixtures/audio/` | the app ingests the three voice records | each voice point's stored payload contains a non-empty `transcript` produced by the local speech model at ingest, its `audio_file` name, and **no** audio bytes; the transcript, not the filename, is what the text vector was built from — searching for "inner tubes" returns id 1003. (R3) |
| AC4 | a store already holding all thirteen fixture memories | a point is written with id 3 and different content | the store still reports thirteen points and id 3 now returns the new content — the write replaced, it did not duplicate; and no fixture id appears twice across the two JSON files. (R4) |
| AC5 | all thirteen memories ingested and indexed | the text lane is queried for "buying parts at the counter" with a filter of `category = "parts"` **and** `price < 15`, limit 3 | every returned hit has `category == "parts"` and `price < 15`; ids 2 and 7 (both `parts`, both over $15) are absent; the returned count is not reduced by any post-filtering step, and each hit still carries its similarity score. (R2, R5) |
| AC6 | the same store | the same filter is applied to a photo-lane query for "a bike part" | photo id 9 (`parts`, $18) is excluded by the price condition and photo id 10 (`admin`) by the category condition — which is only possible because the photo payloads carry those fields at all. (R5, R6) |
| AC7 | the same store | the app is asked "what is on the workbench?" through the recall API | the response has exactly two lanes, `words` and `picture`, each with its own `cutoff` value and the two cutoffs differing; every hit's `above_cutoff` equals `score >= its own lane's cutoff`; at least one hit falls below its cutoff and is still present in the payload, marked, not dropped; no field anywhere merges or sorts hits from both lanes together. (R7) |
| AC8 | a cold process | the full ingest runs (voice first, then text and photos) | an instrumented check of loaded models shows the speech model released before either embedding model is loaded, and at no point in the run are all three resident. (R18) |
| AC9 | all thirteen memories ingested | the text lane is asked "what is the combination for the tool cage?" both without and with freshness ranking | without ranking, ids 3 and 1001 both appear in the candidate set and their scores are within 0.05 of each other — which is the point: meaning cannot separate them; with ranking, id 3 is ranked **strictly above** id 1001, the gap accounted for by the decay term over twenty-one days. (R8) |
| AC10 | the same store, freshly ingested | every stored photo point's payload is inspected, then the freshness-ranked text query of AC9 is re-run | every photo point carries an integer `timestamp` and its `category`; a payload-shape assertion fails if any photo is missing either, because a photo with no timestamp is scored as current by design and would sit permanently above dated memories. (R6, R8) |
| AC11 | an object store taught with `hex_nut`, `spoke_wheel` and `oil_can` at the calibrated threshold | `tire_lever_1.png` — a subject that was never taught — is shown to it | the response's `verdict` is exactly `"UNKNOWN"`; `score` and `nearest_id` are still populated, because retrieval did return something; no taught label appears as the verdict. (R9) |
| AC12 | the same taught store | `hex_nut_3.png`, the held-out view, is shown to it | the verdict is `hex_nut`; the nearest point is one of the two taught `hex_nut` views, not the held-out file itself; and the subject is stored as two points, not one averaged vector. (R9, R11) |
| AC13 | the twelve object fixture images | calibration runs: each held-out view against its own taught views (matches) and against every other subject's taught views plus the three scene photos (non-matches) | the highest non-match score is strictly less than the lowest match score, and the threshold in use lies strictly between them. A failure here means the generated fixtures are not separable and `fixtures/make_fixtures.py` must be regenerated — **never** the threshold adjusted to fit. (R10, R11) |
| AC14 | a store written, compacted and flushed, then the process exited | a **new** process opens the same directory with the network disabled | the point count matches, and AC9's freshness-ranked question returns the identical ordering and identical top id as it did before the restart. (R12) |
| AC15 | the store holding all thirteen memories, and the top text hit for "what is the combination for the tool cage?" recorded | that top hit's point is deleted, then the same question is asked again | the deleted id never appears again; what was the second result is now first; every remaining result's score is unchanged from the pre-delete run. (R13) |
| AC16 | the finished build | the source tree and a full end-to-end run are inspected | no import of, reference to, or network call toward any LLM provider client; no read of any provider API key or base-URL environment variable; the recall and recognition responses validate against the §3 schemas, which admit no generated-text field; every string shown is a question or a stored memory. (R14, R15) |
| AC17 | the served page and its assets | the page's HTML and JS are scanned, and the page is loaded through the preview | no `src`, `href`, or fetch target begins with `/`; every request the page issues resolves under the proxy prefix and returns 200. (R16) |
| AC18 | the built app started with its documented command | the preview is opened | a single process is listening on port 4000 bound to `0.0.0.0`; it serves both the page and the API; no WebSocket upgrade is attempted anywhere in the client. (R17) |

---

## 6. Standing Permissions (in force for the entire build)

**Always**

- Read this spec and anything inside the build folder.
- Create, wipe and recreate store directories and fixture output **under the build folder**.
- Run `fixtures/make_fixtures.py`, the test suite, and the port-4000 server.
- Write `resolved-decisions.md` before the first line of code, and keep results on disk rather than
  in chat — in this workspace the files are the record. `[environment]`

**Ask First** — every entry below is a trade-off the course argued aloud whose wrong side either
forces rework or silently changes a guarantee no test catches.

- **Turning on any form of cloud sync or off-device storage** (Ledger **D3**). It moves private
  memories off the device and puts a credential in the retrieval path; switching it back off does
  not recall what was sent. No acceptance criterion fails when this goes wrong.
- **Changing either encoder, or either vector width** (Ledger **D1**). Forces re-embedding every
  stored memory and re-calibrating the threshold; old vectors are unreadable in the new space.
- **Moving the recognition threshold away from its calibrated value** (Ledger **D4**). Re-trades
  false positives against false negatives — the course's own framing, "depending on the significance
  of false positives and false negatives… select a threshold that fits your use case" — and no AC
  fails at either extreme.
- **Changing either lane's cutoff.** The two differ because the two models score on different
  scales (Lesson 4); moving one silently changes what a person is shown.
- **Changing the freshness weight or half-life.** Re-tunes every text ranking at once, invisibly.
- **Moving taught objects between the combined store and a dedicated object store** (Ledger **D5**).
  Means re-embedding and re-writing them, and changes whether ordinary photo recall can return a
  taught view.
- **Deleting memories outside of AC15's exercise.** Deletion is real and irreversible (R13); the
  course notes that cleanup is genuinely valuable, which is exactly why it is not automatic.
- **Adding any dependency not listed in §2.** Every install costs the person wall-clock time inside
  their session. `[environment]`

**Never**

- Invent provenance or citations — no claim about "what the course does" that is not already in
  this file.
- Emit generated prose in place of a stored memory, or answer when the system should abstain
  (R9, R14).
- Modify a fixture, or adjust the threshold, to make a test pass (R10, §5).
- Read or use the container's provider API keys or base URLs, or ask anyone for a key (R15).
  `[environment]`
- Author `AGENTS.md` in the workspace — the IDE rewrites it at every boot and any guidance placed
  there is silently lost. `[environment]`
- Commit secrets, or write anything outside the build folder.
- Report "should pass" or "looks correct" in place of a run.

---

## 7. Test Plan & Self-Verification

```bash
python3 -m venv .venv --system-site-packages
. .venv/bin/activate
pip install -r requirements.txt          # batch install; announce its cost first
python -m app.warmup                     # one-time model download: Nomic, CLIP x2, Whisper
python -m fixtures.make_fixtures         # deterministic, seed 20260914
python -m pytest -q -m "not preview"     # AC1-AC16; no network needed after warmup
uvicorn app.main:app --host 0.0.0.0 --port 4000 &
python -m pytest -q -m preview           # AC17, AC18, against the running server
```

**On markers.** There is no `live` tier in this suite, and that is not an omission: nothing in this
pipeline needs a credential or a keyed service, so no acceptance criterion is excluded from the
offline run. The one network dependency is the *one-time* model download in `app.warmup`, which is
setup rather than a per-criterion call — after it, every criterion runs with the network off, and
AC14 asserts exactly that. The `preview` marker separates only the two criteria that need the server
process up.

**Reporting.** When the build is done, report **per acceptance criterion** — AC1 through AC18, each
named — with cited evidence: the pytest node id, its output, and the file paths involved. Quote the
calibration numbers AC13 actually produced. "Should pass", "looks correct", and "implemented" are
treated as failures: they mean it was not run.

---

## Course Context Pack (embedded — agent-readable)

### CTX-A. The pattern

**capture → embed → store → recall → decide.** The course's own course-map slide names the first
four as the spine of the whole curriculum; the fifth is what turns a retrieval into an answer.

1. **Capture** — a memory arrives as typed text, as speech, or as a photo. It exists as a small
   record with a body, a time, and a few labelled fields. *Why it's a stage:* the modality differs
   but the record does not, which is what lets one store hold all three.
2. **Embed** — a local encoder turns the body into a vector, a list of numbers positioned so that
   closeness means similar meaning. Text uses a text encoder; photos use the image tower of a
   dual-tower model whose *text* tower embeds a typed question into the same space. *Why it's a
   stage:* it is the only place meaning becomes geometry, and it is the reason a typed question can
   find a picture.
3. **Store** — each memory becomes one point: an id, one or more *named* vectors, and a payload
   carrying the original record. Two encoders means two named spaces in one store, never one blended
   space — their scores are not comparable. *Why it's a stage:* the payload is what makes a memory
   filterable and rankable after the fact; the vector alone is just a position.
4. **Recall** — a question is embedded and the store returns its nearest points, optionally narrowed
   by conditions evaluated inside the same request, optionally re-scored by a formula that folds in
   recency. *Why it's a stage:* this is the whole product. Nothing generates; it retrieves.
5. **Decide** — for recognition, the nearest hit is compared against a calibrated threshold and
   either named or refused. *Why it's a stage:* nearest-neighbour search cannot say "I don't know";
   the threshold is the only thing that can.

Two properties hold across every stage and are the point of the pattern: **the model never changes —
only the memory grows**, and **no language model is involved at all**. Teaching the system a new
subject means writing a handful of example vectors under a label; recognition then means retrieval
plus a threshold. That is the whole learning mechanism.

### CTX-B. Failure-mode catalog

**CTX-B1 — the confident wrong name.** *Symptom:* shown something it has never been taught, the
system names it anyway, picking whichever stored subject happens to be least far away. *Cause:*
nearest-neighbour search has no null result — it returns the closest point regardless of distance.
*Fix:* make the answer a decision: compare the top score against a calibrated threshold and answer
UNKNOWN below it. *Enforced by R9, AC11.*

**CTX-B2 — comparing scores that don't compare.** *Symptom:* a photo result scoring 0.3 looks worse
than a note scoring 0.6, and the "better" one is shown first. *Cause:* the two came from different
encoders; the score is a similarity within each model's own space and the two scales have nothing to
do with each other. *Fix:* keep the lanes separate, give each its own cutoff, and never merge them
into one ranking. *Enforced by R7, AC7.*

**CTX-B3 — the filter that was applied too late.** *Symptom:* a request for three cheap options
returns one, or returns expensive ones. *Cause:* the similarity search ran over everything and the
conditions were applied to its output, so most of the top-k was thrown away. *Fix:* index the
payload fields and put the conditions inside the retrieval request, so the search runs only over
compliant points and the returned count is real. *Enforced by R2, R5, AC5, AC6.*

**CTX-B4 — meaning alone returns the stale fact.** *Symptom:* two memories hold the same kind of
fact — a code, a price, an address — recorded weeks apart in near-identical words, and the one that
comes back is the old one. *Cause:* similarity is about wording, not time; near-identical wording
gives near-identical scores, so which one wins is effectively arbitrary. *Fix:* re-score the
candidate set with an exponential decay on the timestamp, weighted so meaning still leads and
recency breaks ties. *Enforced by R8, AC9.*

**CTX-B5 — the memory that was only hidden.** *Symptom:* a "forgotten" memory reappears in a later
result, or the results list is one item short after a deletion. *Cause:* the deletion filtered the
display rather than removing the point. *Fix:* delete the point; the next-best result then promotes
naturally and every other score is untouched — which is itself the check that nothing else moved.
*Enforced by R13, AC15.*

**CTX-B6 — the photo with nothing to filter on.** *Symptom:* photos never appear in any filtered
result, and they sit permanently at the top of every recency-ranked result. *Cause:* they were
written with a thin payload — filename and type only. A condition on a field that isn't there
matches nothing, and a recency formula with no timestamp to read treats the memory as brand new.
*Fix:* write photos with the same full record as any other memory. *Enforced by R6, AC6, AC10; the
underlying inconsistency is Ledger **D6**.*

**CTX-B7 — the memory that didn't survive the restart.** *Symptom:* a subject taught minutes ago is
unknown after a restart, or the point count drops. *Cause:* writes were still in memory; compaction
builds the index over what was just written, and the flush is what puts it on disk. *Fix:* compact
and flush after every write batch, and prove it by reopening the directory from a fresh process.
*Enforced by R12, AC14.*

### CTX-C. Decision background

*Reference for the Ledger rows above — background, not where a decision is made.*

**CTX-C1 — asymmetric query embedding.** The course's text encoder uses different task prefixes for
stored documents and for questions, and the library exposes a separate query-embedding call that
applies the query prefix. Embedding a question through the document path shifts every score and
quietly invalidates any cutoff tuned the other way. Background for **D1**: swapping encoders means
checking whether the new one has the same asymmetry.

**CTX-C2 — why the store is a library, not a server.** The engine runs inside the application's own
process; "the memory" is a directory on disk holding a config file, segment files and a write-ahead
log. There is no port, no daemon, and nothing to provision. Lesson 2 states it plainly: "There is no
separate vector database server, and the memory is stored in a folder on the device." This is the
mechanism behind **D3**'s invariant, and the reason the default costs nothing to run.

**CTX-C3 — what the cloud side would actually be.** The course's helper module ships client
functions for the sync story — connect to a cluster addressed by a URL and an API key, read every
point out of the local store in the shape the server takes, push a single note as another device
would, and download a full or *partial* snapshot for only what the local store is missing. The
partial-snapshot idea is the interesting half: sync is differential, not a re-upload. The supplied
materials contain the helpers and the transcript's framing but **no working demonstration** — the
appendix notebook the course README lists is absent from the supplied repository. Treat this as a
design sketch when weighing **D3**'s option (b), not as something shown to work.

**CTX-C4 — how the threshold was actually found.** The instructor ran a sweep over a large set —
described in Lesson 5 as 220 non-matches and 6 matches — and reported the boundary: the lowest
scoring true match landed at 0.86 and the highest non-match at 0.74, leaving a clear gap, and 0.80
was chosen as the middle of it. Two things transfer and one does not. What transfers: the *method*
(hold a view out, score it against its own taught views and against everything else, put the
threshold in the gap) and the framing (where in the gap you sit is a false-positive/false-negative
trade). What does not transfer: the numbers, which belong to that photo set and that encoder. This
is the background for **D4**, and the reason AC13 asserts *separation* rather than a value.

**CTX-C5 — retrieval limits, and how this spec picked them.** The materials set retrieval limits
several different ways: the lesson that introduces querying narrates "a limit of 3" on screen; a
shared search helper carries a signature default of 4; the end-to-end assistant's own recall fetches
10 text candidates and 1 photo, then keeps the top 3 per source type; and the freshness-ranked
search prefetches 20 candidates and returns 3. These are near-equivalent tunables, not design
decisions — changing one alters how many rows a person sees, not the system's structure or any
guarantee — so they are **post-build levers**, set as body defaults rather than Ledger rows:

- **Plain text query: 3.** Selected by the value the narration states aloud in the lesson that
  introduces the concept.
- **Recall text lane: 10 candidates, top 3 per source type; photo lane: 1.** The narration names no
  number here, so this falls to the next branch: the end-to-end application's own configuration.
- **Freshness-ranked text search: prefetch 20, return 3.** Same branch, same source.

One genuine inconsistency sits underneath: a `recall` function exists both in the shared helper
module and, redefined, in the assistant lesson's own notebook, and they differ — the helper fetches
3 photos and slices to 1 while also filtering photo hits by source type, and the notebook fetches 1.
The notebook's definition is the one that actually runs from that cell onward. This spec follows the
notebook (the end-to-end application), and R6 makes the helper's source-type filter unnecessary by
requiring photos to carry their type in the payload anyway.

**CTX-C6 — the id schemes, and why R4 is hardening.** Different lessons allocate point ids
differently: the day's memories keep their source ids, a bulk photo load starts at 1000, taught
object views start at 0 or at 100 depending on the lesson, a single added note uses 900, and the
assistant's taught subject uses 5000. None collides in the materials, but no rule is ever stated. R4
states one, and is labelled *project hardening* for that reason — do not read it as course-taught.

**CTX-C7 — latency, as the course frames it.** The lesson on storing and forgetting plots retrieval
latency against store size from numbers pre-measured on the instructor's own machine rather than
timing anything live, and the shape is the teaching point: memory count grew 250×, lookup time grew
about 50×, on a logarithmic axis — sublinear. The spoken conclusion is that vector stores handle
hundreds of thousands of memories comfortably *and* that forgetting and cleanup remain worth doing.
Two consequences for this build: performance work is explicitly out of scope (§1), and deletion is a
first-class operation (R13), not an afterthought.

### CTX-D. Perishable assumptions

The concepts in CTX-A, CTX-B and CTX-C are durable. **The names below are not.** Treat every one as
a *search keyword against current documentation*, never as a guaranteed import, class, or model id.

- **Store library and its surface.** The engine's Python package and its era's type names — a config
  object holding one vector-params object per named vector, a shard-creation call, a query-request
  object wrapping a "nearest" query that names which vector space to use, an update-operation façade
  for upserts / field-index creation / point deletion, a scroll request for reading points back, and
  a payload-schema enum for index kinds. Also its ranking primitives: a formula object, an
  expression algebra with a decay function, a decay-kind enum, and a prefetch object for two-stage
  retrieval. Names and packaging for a pre-1.0 library move fast.
- **Model ids.** The text encoder, the two towers of the image encoder, and the speech model are
  named in §2 exactly as the supplied materials name them. Model repositories rename, re-version and
  deprecate; confirm each id resolves before assuming a download failure is a network problem.
- **Version pinning.** The course's requirements file pins every version exactly and states the
  reason — reproducible scores. Those pins are that course's era, not a guarantee about today. This
  spec carries them forward as a starting point; if any fails to resolve, move it forward and expect
  the absolute score *values* (never the orderings the ACs assert) to shift.
- **A defect to expect in the era's code.** The calibration cell in the supplied materials defines a
  threshold constant under one name and then uses a *different*, never-defined name three times in
  the same cell; run verbatim it raises a name error. Noted here so that reproducing the course's
  calibration step does not send you hunting for a missing dependency.
- **Request-parameter compatibility.** Not applicable in the usual sense: this pipeline calls no
  chat-completion API, so no model family's parameter support (temperature and friends) can affect
  it. The equivalent perishable here is **vector width** — a model's output dimension is part of its
  identity, and a re-versioned encoder that changes width invalidates an existing store rather than
  degrading it. AC1 pins the declared widths for exactly this reason.

### CTX-E. Provenance map

Lesson numbering follows the transcripts, which are authoritative. The supplied materials contain
five lesson transcripts, three lesson notebooks (Lessons 3–5; Lessons 1 and 2 are video only), one
shared helper module, the data files, and a slide-description document. **Nothing in this spec
requires platform access, the course repository, or the videos.**

| Source | What came from it |
|---|---|
| **Lesson 1 — Why Devices Need Memory** | CTX-A stages 1, 2 and 4 (note → vector → nearest neighbour → similarity score); the dual-tower image/text idea; CTX-B1 (threshold as the match rule); Ledger **D3**'s whole argument, both sides, in the instructor's own words; the "no LLM, no retraining, no custom vision pipeline" claim behind R14. |
| **Lesson 2 — Building the Device** | CTX-C2 (library not server; memory is a folder on disk); Ledger **D3**'s "optional sync" framing; the framing that the memory loop is the transferable part and the specific hardware is not — which is why §1's exclusions 3 and 4 exist. |
| **Lesson 3 — Store, Find, and Forget Memories** | CTX-A stage 3 and the point anatomy behind R1 and the §3 contracts; the declared vector widths and cosine distance (AC1); CTX-B3 with R2 and R5 (field indexes, filter inside the query); Ledger **D6**'s thin-payload side; CTX-B5 and R13 (deletion, runner-up promotion, unchanged scores); CTX-C5's narrated "limit of 3"; CTX-C7 (latency curve and the case for forgetting). |
| **Lesson 4 — Your On-Device Assistant** | CTX-B2 and R7 (two lanes, two cutoffs, different models); R3 (store the transcript, not the audio); R18's release-before-load behavior; Ledger **D6**'s full-record side; CTX-C5's end-to-end recall configuration. |
| **Lesson 5 — Teaching Your Assistant to See** | R11 (teaching is writing example vectors; several views per subject); CTX-B1 and R9 (the pre-teaching wrong match, then the threshold decision); CTX-C4 and Ledger **D4** (the calibration sweep and its numbers); CTX-B4 and R8 (the stale-fact failure, decay, half-life, bounded weight); Ledger **D5** (a dedicated object store *and* a combined assistant store, both used); R12 and CTX-B7 (compact, flush, close, reopen from disk); the single point carrying both vectors. |
| **Shared helper module + data files** | CTX-C1 (asymmetric query embedding); CTX-C3 (the cloud client, point export, single-note push, and partial snapshot); CTX-C5's helper-vs-notebook `recall` discrepancy; CTX-C6 (the id schemes); CTX-C7's pre-measured latency table; the observation that the cloud-sync appendix the README lists is absent from the supplied repository. |
| **Slide descriptions** | The capture → embed → store → recall spine named as the course map (CTX-A); the point anatomy diagram (R1); the two-encoders-one-store diagram and its stated widths; the "filter is part of the query, not post-processing" diagram (CTX-B3); the library-in-process, folder-on-disk, optional-sync diagram (CTX-C2); the one-point-two-doors diagram behind Ledger **D5**'s default; the frozen-model/growing-memory framing in CTX-A. Note: the decks use an earlier six-lesson plan whose numbering is off by one from the final videos — the transcripts' numbering is what this table uses. |
| **`coding-agent-lab` environment** `[environment]` | Everything labelled `[environment]`: §2's *Runtime* subsection, R15, R16, R17, R18's reinforcement, the §0 question mechanism and the reason `resolved-decisions.md` is load-bearing, the `[environment]` Always / Ask-First / Never entries, and the impracticality notes inside Ledger **D1** and **D3** options. **None of this comes from the course, and none of it is course-demonstrated.** |

---

## Closing: the infra/structure diagram

When the build is finished and you have reported every acceptance criterion with cited evidence,
close by drawing the infra/structure diagram of what you built — the processes, the store directory,
the two named vector spaces, the two retrieval lanes, the model load order, and the single
port-4000 server — and introduce it with exactly this sentence:

**"This is the infra/structure diagram of this app."**

---

*Version 1.0 · Course: Building On-Device AI Memory with Qdrant Edge (5 lessons, transcript
numbering) · Environment: `coding-agent-lab` · Target project: the on-device memory assistant of §1,
fixed by the lab · Generated 2026-09-14 from the supplied notebook dump, transcripts and slide
descriptions; spec-generation guide `8e44ecb`, overlay `58ecfb9`.*

*Living document: when the building agent produces something you did not expect, do not correct it
in chat — add the missing constraint here as a numbered rule with an acceptance criterion, and
re-run the build.*
