# Spec: On-Device Memory Assistant — Standalone Takeaway

> **What you're building.** A page you can open and ask *"where did I leave the bike?"* — and a note
> from this morning, a voice memo, and a photo come back side by side, each with its similarity
> score, the weak ones dimmed rather than dressed up as answers. Show it two photos of an object and
> hold a third back, and it names the third. Delete a memory and watch the next-best answer move up.
> No LLM, no cloud, no API key: every answer comes out of vectors on local disk.
>
> **Fastest path.** Answer the §0 gate's first question with the **recommended baseline build** and
> this gets built end-to-end with no further decisions. The build is **complete when the offline test
> suite passes** — nothing here needs a key, an account, or a network call at query time; the only
> network use is the one-time model download.
>
> **This file is self-contained.** The embedded **Course Context Pack** (`CTX-A`…`CTX-E`, at the end)
> replaces every external course reference — nothing in this spec requires the course platform, its
> notebooks, or its transcripts. `(CTX-X)` anchors mark course-derived knowledge. The **Decision
> Ledger** below holds every point where this build could legitimately diverge, each pinned to one
> course-derived default, so the spec is buildable and evaluatable **as-is**.
>
> **Provenance.** Generated from the *Building On-Device AI Memory with Qdrant Edge* notebook dump
> (`L3`/`L4`/`L5` notebooks, `helper.py`, `requirements.txt`, `ro_shared_data/`), the five lesson
> transcripts, and the slide descriptions, on **2026-09-11**, by spec-generation-guide commit
> **`8e44ecb`**. Lesson numbers follow the **transcripts** (authoritative) — the slide decks carry a
> *third*, earlier numbering that is off by one and must not be used (CTX-E). Slides are cited with
> their status: **shown** (one of the 8 that appear in a lesson video) or **drafted** (one of the 15
> that exist only in the decks) — a drafted slide never outranks shipped code or narration. Facts
> labelled **[environment]** come from `environment.md` — the AI Coding Lab runtime this build
> targets — **not** from the course; the course is never credited with them.

---

## 0. Before you build — REQUIRED (do this first)

You are the build agent. Before writing ANY code, you MUST surface the design decisions in the
Decision Ledger (next section) to the person you are building for. Do **not** skip this because the
defaults look complete — the defaults exist so the build is *reproducible*, not because they are the
right choice for this person.

1. **Use a structured question tool if you have one.** In the AI Coding Lab your structured-question
   mechanism is the fenced `choices` block: put the explanation in prose *above* it, put the fence
   **last** in the message, one option per line, and stop. Label the question
   `**Question N of M — <decision>**` on its own line before the fence so it renders as a question
   box. A click sends the option line verbatim; a typed answer that names an option counts exactly
   the same. Only the latest message's buttons stay live, so never ask anyone to go back and change
   an earlier answer — re-ask it as a new question instead. If you are running somewhere else, use
   that environment's structured-question tool (e.g. Claude Code's `AskUserQuestion`); only if none
   exists, list the rows in your reply and ask for an answer to each.
2. **First question — recommended baseline build, or customize?** Ask exactly one question with two
   options: the **recommended baseline build** — every Ledger row resolves to its Default: mostly the
   course's own choices, with a lighter stand-in wherever the course's choice needs setup you may not
   have (here: a Qdrant cluster URL and API key, on D2); the step-5 checklist marks exactly where the
   baseline differs from the course — or **customize** the decisions row by row. *(In this spec every
   row's Default happens to be the course's own choice, so a baseline build should print no `≠`
   lines in step 5; if you find one, say so rather than assuming it is fine.)* If the baseline is
   chosen, skip step 3: go straight to the step-5 checklist and build. If customize is chosen,
   continue with step 3.
3. **Present the Ledger ONE ROW AT A TIME — one question per row.** For each row ask a single
   question: the **Decision** as the prompt, its **Options** as the choices. Append "(course
   default)" to the option the course actually used. You may also mark an option "(Recommended)" —
   your judgment for THIS person, made now, at gate time; with no contextual reason to depart,
   recommend the row's Default. When your recommended option IS the course's actual choice, merge the
   labels into "(Recommended - course default)". A recommendation never removes or moves the "(course
   default)" label, and no option is ever labelled with a bare "(default)" — these two labels and
   their merged form are the only option labels. Put any realization beyond the offered options under
   a free-text answer. Ask about **every** row. A per-call item limit is NEVER a reason to drop,
   skip, merge, or silently default a row — make as many separate messages as there are rows.
4. **Presenting any of these questions ENDS YOUR TURN — stop here; write no code, create or edit no
   file, take no other build action.** Keep asking, one row at a time, until **every** row has an
   answer (a chosen option, an explicit "use the default", or the step-2 baseline answer, which
   resolves every row at once). Answers to *some* rows do NOT release the build; "no reply yet" is
   not an answer — wait.
5. **Before the first line of code, print a resolved-decision checklist and write it to
   `resolved-decisions.md`** in the workspace root — every Ledger row with its final value, each line
   carrying a deviation mark: `= course choice`, or `≠ course choice (course used: <option>)`. If the
   baseline path was chosen, walk the person through every `≠` row — the course's actual choice and
   why this build's default substitutes it — before building. Begin implementation ONLY after the
   checklist is shown and written; if any row is unresolved you are not done — return to step 3.
   Build on the checklist's values. **[environment]** Writing the file is not optional here: a new
   chat starts with no memory of this one, and the grader sees only what is on disk — a decision that
   lives only in chat is invisible to both.

---

## Decision Ledger

These are the points where this build could diverge. Every row has a course-derived default, so the
spec is buildable and evaluatable as-is; change a row only when you have reason to prefer another
option. §0 above requires you to present all four rows before building.

**Four rows, not ten.** The learner-context dimensions a standalone takeaway normally asks about —
*project*, *data/inputs*, *goal*, *model/provider*, *environment* — are **fixed by the lab** and are
not asked here: the project and goal are this spec's §1, the data is the §5 fixture corpus, the
runtime is the AI Coding Lab container (see *Runtime environment*), and the course uses **no LLM at
all**, so there is no model/provider to choose. See *Adapting this beyond the lab* in §1 for what to
change if you take this spec elsewhere.

| # | Category | Decision | Invariant (must hold) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| **D1** | learner | **Scope check.** Present the §1 *Not Included* list **inside this question**, item by item, then ask whether to build exactly that scope or bring something back. | *(none — the pattern imposes no scope requirement)* | **Keep as-is**: every §1 exclusion stands and the full acceptance set is built. | 1) Build the scope exactly as §1 defines it. 2) Bring back one or more excluded items — say which. Free text may also add a *new* exclusion. | Each restored item adds build time and, unless §1 says otherwise, arrives with no acceptance criteria of its own. A new exclusion must name the ACs it retires. | learner |
| **D2** | design-argued | **Where memories live** — on the device only, or on the device with sync to a Qdrant server. | Recall and recognition must work with **no network and no credentials** once the models are on disk. | **On-device only** — an embedded store in a directory, no server, no cluster, no credentials. *§3 dependency precedence: no substitution is needed — the course's own demonstrated choice is already the lightest self-contained realization (tier 2, an embedded library: package-manager install, no separate process, no credential), so it stands as the Default unchanged.* The heavy alternative is the one the course names but never runs in the supplied materials, and it stays in Options. | 1) On-device only **(course default)** — tier 2, an embedded library, no separate process. 2) On device **plus** sync to a Qdrant server *(heavy setup: a reachable cluster URL and an API key you must hold; Lesson 1 names this path and the course ships helper functions for it, but no notebook in the supplied materials runs it).* | Lesson 1 argues both sides aloud: local works with no connection, recall is faster and more reliable, and private memories stay private; cloud buys sharing between devices and more compute and storage than a small device has. The instructor's own framing — "for today, we will only be working locally… you can always use cloud and local retrieval combined together if your use case requires it." Switching later means re-uploading every point and taking on a credential. | course+learner |
| **D3** | design-structural | **Memory topology** — one store holding both vector spaces, or a separate store per purpose. | Text and image embeddings must live in **separate named vector spaces**, each with its own dimensionality and its own score scale; one question must be able to reach both lanes; and every stored memory must survive the process exiting and the store being reopened from disk. | **One store** declaring both named spaces (`text` 768, `image` 512, cosine on both) — what the course's end-to-end assistant does (Lesson 5, §4). | 1) One store, both named vector spaces **(course default for the finished assistant)**. 2) A separate store per purpose — e.g. an object-recognition store beside the day store, which is what the course itself does in Lesson 5 §1 before folding the taught object into the assistant's store. | Separate stores isolate recognition from recall and let either be wiped alone, but a question then has to be fanned out and merged by hand, and a memory that is *both* a photo and a note (the course's taught object carries both vectors on one point) has to be written twice and kept in step. | course+learner |
| **D4** | design-structural | **Ranking** — similarity alone, or similarity with a freshness boost. | When two memories carry the same kind of fact, ranking must be able to prefer the more recent one **without letting recency outrank meaning**; a memory with no timestamp must be treated as current, never dropped. | **Similarity + exponential freshness decay**: prefetch 20 candidates by meaning, then re-score them with an exponential decay over `timestamp` (target = the newest memory's timestamp, half-life 7 days = 604,800 s, midpoint 0.5) added at a weight of **0.2** on top of the similarity score (Lesson 5, cell 19). | 1) Similarity + freshness decay **(course default for the finished assistant, Lesson 5 §5)**. 2) Similarity only — what Lessons 3 and 4 run on, and enough when no two memories restate the same fact. | Lesson 5 narrates the failure it fixes: two memories hold a code, meaning alone puts the outdated one first, and "ideally we would want the most recent memory with the most recent code to score the highest". The 0.2 weight is a ceiling, so meaning still leads and recency only breaks ties. Choosing similarity-only retires AC16 and AC17. | course+learner |

---

## 1. Objective

A single-page web app, served on port 4000, that stores a day's text notes, voice notes and photos as
vectors in an on-device store and answers typed questions from them by similarity alone — returning
text, voice and photo results as three separate ranked lanes with their scores — while also
recognising an object it was taught from two example photos, and forgetting a memory on request.
No LLM anywhere in the pipeline. (pattern: CTX-A)

### Not Included ★

The build stops at this line. Each item carries a **handling rule** so the D1 gate question has a
determinate answer.

| # | Excluded | Handling rule at the D1 gate |
|---|---|---|
| N1 | **Any LLM** — no generated prose answers, no summarising or re-writing of results, no chat. Answers are retrieved memories and their scores. | *Owned by the course as a taught guarantee* — this is R1, not a scope choice. Unavailable. |
| N2 | **Cloud sync** — no Qdrant server, no cluster URL or API key, no cross-device sharing. | *Owned by another row* — decided at **D2**, never here. |
| N3 | **Live camera or video-frame loop** (the robot in Lessons 1–2 runs this same loop frame by frame). | *Named by the course but never built in the supplied materials* — buildable, but this spec supplies no parameters and no acceptance criteria for it. |
| N4 | **Recording audio in the browser.** Voice memories arrive as audio files already in the workspace, or as pre-transcribed records. | Additive, owned by no other row — restorable at the gate. |
| N5 | **Uploading your own photos from the browser** to teach with. Teaching uses photo files already in the workspace. | Additive, owned by no other row — restorable at the gate. |
| N6 | **Any latency benchmark or performance chart.** | Additive, owned by no other row — restorable at the gate, but only as numbers this build measures itself, labelled as measured here on this machine. Replaying the course's figures is never restorable: R14 forbids it outright. |
| N7 | **Authentication, accounts, multi-user separation, memory sharing between people.** | Additive, owned by no other row — restorable at the gate, but it changes the §3 contract. |
| N8 | **Swapping embedding models at runtime**, or a UI for it. Models and vector widths are pinned in config (§2). | Additive; changing a model means re-embedding every point (§6 Ask First). |
| N9 | **Grafting this onto an existing codebase.** The deliverable is a standalone app in the workspace. | *Outside the delivered build mode* — unavailable. |
| N10 | **A notebook deliverable.** The deliverable is the served app plus its test suite. | *Outside the delivered build mode* — unavailable. **[environment]** there is no notebook surface in this runtime. |

### Adapting this beyond the lab

Four dimensions a standalone takeaway would normally put to you are fixed here, and each has one
place to change it: **project and goal** → this §1; **data/inputs** → the §5 fixture corpus (replace
the fixture records and photos with your own captures; the ACs that quote fixture facts move with
them); **runtime** → *Runtime environment* below; **model/provider** → §2, remembering that the
course's pipeline has no LLM in it at all and nothing here needs an inference provider.

---

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language | Python ≥ 3.12 | **[environment]** use the container's `python3`; create the venv with `--system-site-packages` so the preinstalled web stack is reusable. Verify the version before installing and report it as build evidence; a version below 3.12 is a blocker to raise, not to work around. |
| Memory store | `qdrant-edge-py==0.7.2` | The embedded on-device engine — no server, no network, memories in a directory. **This is the course's subject, kept as the default (§3 precedence branch 2).** *The course pins every dependency exactly and was validated on Python 3.14.6; those pins are carried forward here unchanged. If a pin no longer resolves, treat the names in **CTX-D** as search keywords against current docs, not as guaranteed imports.* Locality is **D2**; topology is **D3** — change them there, not here. |
| Text embeddings | `fastembed==0.8.0`, model `nomic-ai/nomic-embed-text-v1.5`, **768 dims** | Runs locally on CPU. Documents and queries use **different task prefixes** — use the library's query-embedding call for questions and its document call for stored text (R9). |
| Image embeddings | `fastembed==0.8.0`, models `Qdrant/clip-ViT-B-32-vision` and `Qdrant/clip-ViT-B-32-text`, **512 dims** | One shared image/text space, so a typed description can retrieve a photo. Its scores are on a different scale from the text model's — never compared or merged with them (R5). |
| Speech to text | `onnx-asr==0.12.0`, model `whisper-base`, CPU provider | Voice notes only. Released from memory before the embedding models load (R11). |
| Runtime deps | `onnxruntime==1.27.0`, `tokenizers==0.23.1`, `numpy==2.5.1`, `Pillow==12.3.0` | Pinned alongside the models because they decide the embedding numbers. |
| Web layer | FastAPI + uvicorn | **[environment]** preinstalled in the container. **One** server, bound to `0.0.0.0:4000`, serving both the page and the API (R14). |
| Tests | `pytest` | §7. |
| Secrets | **none** | Nothing in this build reads an API key. **[environment]** the container exports `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`; this build must not read or use them (R2). Never hardcode or commit a credential. |

**Install cost, stated plainly. [environment]** None of the memory stack is preinstalled: the store,
both embedding packages, the ASR package and the runtime deps all install on first use, and the four
models download once (keyless, no account). Do this as **one batched install early**, tell the person
it is running and roughly what it costs in wall-clock, and do not start it in the middle of an
interactive question. After the first download everything runs offline.

---

## 3. Input/Output Contracts ★

**The memory record** — one record is one point in the store: an integer id, one or two named
vectors, and this payload.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "memory-record",
  "type": "object",
  "required": ["id", "source_type"],
  "properties": {
    "id": { "type": "integer", "minimum": 0 },
    "source_type": { "enum": ["text", "voice", "photo", "object"] },
    "category": { "type": "string" },
    "location": { "type": "string" },
    "timestamp": {
      "type": "integer",
      "description": "Epoch seconds. Optional: a record without it is treated as current by the D4 ranking, never dropped."
    },
    "note": { "type": "string", "minLength": 1 },
    "transcript": { "type": "string", "minLength": 1 },
    "file": { "type": "string", "minLength": 1 },
    "label": { "type": "string", "minLength": 1 },
    "price": { "type": "number", "minimum": 0 },
    "audio_file": { "type": "string" }
  },
  "allOf": [
    { "if": { "properties": { "source_type": { "const": "text" } }, "required": ["source_type"] },
      "then": { "required": ["note"], "not": { "required": ["file"] } } },
    { "if": { "properties": { "source_type": { "const": "voice" } }, "required": ["source_type"] },
      "then": { "required": ["transcript"], "not": { "required": ["file"] } } },
    { "if": { "properties": { "source_type": { "const": "photo" } }, "required": ["source_type"] },
      "then": { "required": ["file"], "not": { "anyOf": [{ "required": ["note"] }, { "required": ["transcript"] }] } } },
    { "if": { "properties": { "source_type": { "const": "object" } }, "required": ["source_type"] },
      "then": { "required": ["label", "file"] } }
  ],
  "unevaluatedProperties": false,
  "$comment": "Audio is never stored: a voice record carries its transcript and at most the source filename. No property may hold audio or image bytes."
}
```

**Vector assignment is part of the contract.** `text` and `voice` records carry a `text` vector
(768) and no `image` vector. `photo` and `object` records carry an `image` vector (512). A record may
carry **both** only when it is genuinely both — the taught object that also has a written note.

**The recall response** — three lanes, never one blended list (R5).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "recall-response",
  "type": "object",
  "required": ["question", "cutoffs", "lanes"],
  "properties": {
    "question": { "type": "string", "minLength": 1 },
    "cutoffs": {
      "type": "object",
      "required": ["text", "photo"],
      "properties": {
        "text": { "type": "number" },
        "photo": { "type": "number" }
      },
      "$comment": "Two cutoffs because the two lanes come from different models on different scales."
    },
    "lanes": {
      "type": "object",
      "required": ["text_notes", "voice_notes", "photos"],
      "additionalProperties": false,
      "properties": {
        "text_notes": { "$ref": "#/$defs/lane" },
        "voice_notes": { "$ref": "#/$defs/lane" },
        "photos": { "$ref": "#/$defs/lane" }
      }
    }
  },
  "$defs": {
    "lane": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "score", "weak", "payload"],
        "properties": {
          "id": { "type": "integer" },
          "score": { "type": "number" },
          "weak": { "type": "boolean", "description": "true when score < this lane's cutoff" },
          "payload": { "$ref": "memory-record" }
        }
      }
    }
  }
}
```

**The recognition response.**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "recognition-response",
  "type": "object",
  "required": ["verdict", "score", "threshold", "nearest_id"],
  "properties": {
    "verdict": { "type": "string", "description": "the matched label, or the literal UNKNOWN" },
    "label": { "type": ["string", "null"], "description": "the nearest point's label, always reported, even when the verdict is UNKNOWN" },
    "score": { "type": "number" },
    "threshold": { "type": "number" },
    "nearest_id": { "type": "integer" }
  },
  "$comment": "Nearest search always returns something, so a verdict is a separate decision against the threshold — never the bare nearest hit."
}
```

---

## 4. Business Rules

Numbered. Each rule states the behaviour and the failure it prevents, and reaches at least one
acceptance criterion.

1. **No LLM in the pipeline.** Answers are retrieved memories and their scores — never generated,
   summarised or re-worded text. Recognition is a vector comparison against stored examples: no
   training, no fine-tuning, no vision pipeline (CTX-B1). → AC19 · *course-demonstrated*
2. **No credentials, no query-time network.** Once the models are on disk, storing and recalling
   work with no network and no API key; the container's provider keys are not read (CTX-B1). → AC19,
   AC20 · *course-demonstrated + [environment]*
3. **Two named vector spaces, fixed widths.** The store declares `text` at 768 and `image` at 512,
   both cosine, before any point is written; a point's vector goes into the space that matches its
   model. Prevents dimension mismatches and the silent mixing of two score scales (CTX-B7). → AC1,
   AC4 · *course-demonstrated*
4. **A question reaches both lanes by being embedded twice** — once with the text model, once with
   the image-space text encoder — and each embedding queries only its own space (CTX-B7). → AC6, AC8
   · *course-demonstrated*
5. **Results are presented as separate lanes, never one blended list**, and each lane is judged
   against its own cutoff: **0.6** for text and voice, **0.23** for photos. Scores from two different
   models are never compared, merged or sorted together (CTX-B2). → AC9 · *course-demonstrated*
   *(Both cutoffs are single-valued in the materials — Lesson 4, cells 13/15/18 and its narration —
   and both are post-build levers: see §6 Ask First.)*
   **The course considered the other design and dropped it.** A slide describing a single merged
   inbox — all modalities "merged into one inbox ranked by score" — was drafted for Lesson 4 and
   appears in **no** video; the shipped display renders three columns and its own source calls the
   merged form out by name as the thing not to do. If you have seen that slide, it is not the
   course's position (CTX-C8).
   **Lane sizes.** One recall fetches the text space wide — top 10 — and splits that set into at most
   3 voice and 3 text results, and fetches the image space at top 1. *The materials set the photo
   fetch two ways: the shared helper pulls 3 photo candidates and shows the first, while the
   lesson's own recall — defined in the notebook, and the one that actually runs from that cell
   onward — pulls 1. Near-equivalent (both surface a single photo), so this is resolved as a body
   default, not a Ledger row: by the lever rule's second branch, the end-to-end application's own
   configuration wins → top 1. A **post-build lever**: widen it if a lane feels thin.*
6. **A result below its lane's cutoff is returned but marked weak**, and never presented as the
   answer. Nothing below a cutoff is silently promoted or silently dropped (CTX-B3). → AC10 ·
   *course-demonstrated*
7. **Payload filtering requires a field index, and the filter runs inside the search.** Fields used
   in filters — `category` (keyword) and `price` (float) — are indexed at initialisation; a filtered
   recall returns only points satisfying every condition, and a point missing a filtered field cannot
   satisfy a range condition on it. **The filter is part of the query, not a trim applied to its
   results:** the similarity search runs *over the points that pass the conditions*, so a filtered
   search returns the nearest matches **within** the filtered set — never "the top k, minus the ones
   that failed" (CTX-B4, CTX-C8). → AC3, AC7, AC7b · *course-demonstrated*
8. **Forgetting really forgets.** Deleting a memory removes its point; the next-best result moves up
   and the other results' scores are unchanged; the stored count drops by one (CTX-B5). → AC11 ·
   *course-demonstrated*
9. **Queries and documents are embedded by their own call.** The text model uses different task
   prefixes for the two, so a question embedded as a document (or the reverse) mis-scores everything
   (CTX-B6). → AC6 · *course-demonstrated*
10. **Voice becomes text at the boundary.** A voice memory is stored as its transcript and is
    searched exactly like a text memory; the audio itself is never stored in the payload — at most
    its source filename (CTX-B8). → AC5, AC21 · *course-demonstrated*
11. **Release the speech model before the embedding models load.** Transcription finishes first, its
    session is freed, and only then are the embedding models loaded. Prevents holding two model sets
    resident at once (CTX-B9). **[environment]** the container's memory budget makes this
    load-bearing, not cosmetic. → AC21 · *course-demonstrated*
12. **Writes are durable before they are announced.** After a write the store is optimised and
    flushed, so a memory survives the process exiting; reopening the same directory in a new process
    returns the same memories and the same answers (CTX-B10, CTX-C9). → AC12 · *course-demonstrated*
13. **Recognition is a threshold decision, not a nearest hit.** A match "is a decision rule, not a
    model" — Lesson 1's closing slide (shown) puts the similarity score against a threshold and calls
    that the whole mechanism: no LLM, no retraining, no custom vision pipeline. Nearest search always
    returns something, so a verdict is produced by comparing the top score with **one named threshold
    constant, 0.80**, used everywhere the decision is made; below it the verdict is `UNKNOWN` and the
    nearest label is still reported (CTX-B11). → AC15, AC13, AC14 · *course-demonstrated; the
    single-constant requirement is **project hardening** — the course's own Lesson 5 cell defines the
    threshold under one name and reads it under another, which fails on the spot (CTX-D)*
14. **No fabricated measurements.** The course's latency figures were measured on the instructor's
    machine and are background only (CTX-C5): never printed, plotted or quoted as this build's own.
    Any number this build shows must have been measured by this build, here, and labelled as such.
    → AC22 · *project hardening*
15. **One server, port 4000, relative URLs. [environment]** The app binds `0.0.0.0:4000` and serves
    the page and the API from the same process; every URL inside the page is relative
    (`api/recall`, not `/api/recall`), because the preview is reverse-proxied under a path prefix and
    a root-absolute path escapes the app. → AC18 · *[environment]*
16. **Teaching is writing, not training.** Teaching an object stores one point per example view under
    a shared label, then flushes; recognising compares a new photo against those stored views. Adding
    a subject never retrains or reloads a model (CTX-B12). → AC14 · *course-demonstrated*

---

## 5. Acceptance Criteria ★ (the oracle)

### Fixture corpus (define FIRST; every fact authored for this spec — no course data is copied)

All fixture facts are invented here. `NOW` is the fixed constant **1767225600** (2026-01-01T00:00:00Z);
every timestamp below is `NOW` minus the stated offset, so the corpus is deterministic.

**`fixtures/memories.json`** — 13 note records (10 `text`, 3 `voice`), ids 1–13:

| id | source_type | category | location | timestamp | note / transcript | price |
|---|---|---|---|---|---|---|
| 1 | text | transit | Station | NOW−3,600 | "Left the blue bike in rack 3 at the east entrance of the station" | — |
| 2 | text | home | Home | NOW−1,036,800 (12 d) | "Side gate code is 1145" | — |
| 3 | text | home | Home | NOW−7,200 | "Replaced the lock on the side gate this morning, so the code to get in is 8890 now" | — |
| 4 | text | food | Alder St | NOW−9,000 | "Soup and bread at the corner canteen, quick and cheap" | 11.5 |
| 5 | text | food | Harbour | NOW−345,600 (4 d) | "Tasting menu at the harbour place, worth it once" | 68.0 |
| 6 | voice | food | Alder St | NOW−8,600 | "Note to self, the canteen on Alder does a lentil soup that is better than it looks" | 9.0 |
| 7 | text | work | Office | NOW−18,000 | "Sprint review moved to Thursday, bring the migration numbers" | — |
| 8 | text | errand | Market | NOW−172,800 (2 d) | "Parking permit for the market runs out at the end of the month" | 45.0 |
| 9 | voice | transit | Station | NOW−3,500 | "Quick memo, the east entrance rack was nearly full this morning" | — |
| 10 | text | garden | Home | NOW−2,592,000 (30 d) | "The fig cutting needs water twice a week until it roots" | — |
| 11 | text | work | Office | NOW−432,000 (5 d) | "Handed the spare office key to the facilities desk" | — |
| 12 | text | food | Alder St | NOW−518,400 (6 d) | "Canteen closes at 2pm on Saturdays" | — |
| 13 | text | home | Home | *(none — deliberately absent)* | "Spare fuse box key lives in the tin on the shelf" | — |

Planted failure instances: **ids 2 and 3** are the same fact twelve days apart (the stale-value case,
R‑D4); **id 8** is the lexical near-miss for a bike question ("parking" without a bike); **ids 4, 5, 6,
12** exercise the category/price filter, with id 12 carrying no `price` at all; **id 13** carries no
timestamp; **ids 6 and 9** are voice records stored by transcript.

**`fixtures/gen_images.py`** — a deterministic generator (no randomness, no network) writing PNGs
under `fixtures/images/`. Every image is 512×512, a flat background with one centred filled glyph:

| file | ids | background | glyph | glyph colour | scale | rotation |
|---|---|---|---|---|---|---|
| `circle_red_on_white.png` | 100 | #FFFFFF | circle | #D7263D | 60% | — |
| `circle_blue_on_white.png` | 101 | #FFFFFF | circle | #1B4FA0 | 60% | — |
| `square_red_on_white.png` | 102 | #FFFFFF | square | #D7263D | 60% | 0° |
| `square_blue_on_white.png` | 103 | #FFFFFF | square | #1B4FA0 | 60% | 0° |
| `triangle_green_on_black.png` | 104 | #101010 | triangle | #2E9E4F | 60% | 0° |
| `triangle_yellow_on_black.png` | 105 | #101010 | triangle | #E8C020 | 60% | 0° |
| `cross_black_on_white.png` | 106 | #FFFFFF | cross | #101010 | 60% | 0° |
| `ring_purple_on_grey.png` | 107 | #9A9A9A | ring | #6B2FA0 | 60% | — |
| `widget_a_1.png` / `_2.png` / `_3.png` | 200, 201, *(held out)* | #FFFFFF / #F2F2F2 / #EAEAEA | filled pentagon | #D7263D | 60 / 56 / 64% | 0 / 18 / 36° |
| `widget_b_1.png` / `_2.png` / `_3.png` | 210, 211, *(held out)* | #FFFFFF / #F2F2F2 / #EAEAEA | filled five-point star | #1B4FA0 | 60 / 56 / 64% | 0 / 18 / 36° |

Photo records (ids 100–107) carry `source_type: "photo"`, `category: "fixture"`, their `file`, and
`timestamp` = NOW − (id − 99) × 600. Object records carry `source_type: "object"` and `label`
`"widget-a"` / `"widget-b"`. `widget_a_3.png` and `widget_b_3.png` are **held out** — never stored
until a test teaches with them.

**Two standing rules about fixtures.** (a) Fixture *records* are never edited to make an assertion
pass — that is a defect in the build, not in the corpus. (b) The generator's *parameters* are part of
the fixture definition: if the two subjects turn out not to separate under the pinned image model,
report it as a fixture-design defect and regenerate with more visually distinct subjects, documenting
the change in the test evidence — but never weaken the assertion.

**Absolute course scores are never asserted on fixture data.** 0.80, 0.6 and 0.23 are the course's
calibrated values on the course's own photos and notes; on synthetic fixtures they mean nothing. The
criteria below assert *mechanisms and relative order*; the constants are asserted only as
configuration and as threshold **semantics**.

### Given / When / Then

Tiers: **core** criteria must pass for the build to be complete; **voice** criteria additionally need
the speech package and its model. Both tiers are keyless and offline after the one-time download.

| # | Tier | Given | When | Then |
|---|---|---|---|---|
| AC1 | core | a clean store directory | the store is initialised | it reports 0 points, and its config declares exactly two named vector spaces: `text` size 768 cosine and `image` size 512 cosine |
| AC2 | core | the freshly initialised, empty store | the text lane is queried with "a place to eat nearby", limit 3 | zero results are returned and no exception is raised |
| AC3 | core | the freshly initialised store | its indexes are inspected | a keyword index exists on `category` and a float index on `price` |
| AC4 | core | the 13 note records and 8 photo records | they are ingested | the store reports 21 points; every text/voice point has a 768-length `text` vector and no `image` vector; every photo point has a 512-length `image` vector and no `text` vector |
| AC5 | core | voice record id 6 | it is ingested and then read back | its payload carries the transcript, carries no audio bytes under any key, and is retrievable by a text query like any note |
| AC6 | core | the ingested corpus | the text lane is queried with "where did I leave the bike" | id 1 is the top text result, and it outranks id 8 ("parking permit…") |
| AC7 | core | the ingested corpus | the same question is run with a filter of `category == "food"` **and** `price < 15` | exactly ids 4 and 6 come back — id 5 fails the price bound and id 12, which has no `price`, cannot satisfy the range condition |
| AC7b | core | the ingested corpus, in which id 10 (the fig cutting) is the only `garden` point and is semantically unrelated to food | "somewhere to eat" is searched with a filter of `category == "garden"`, limit 3 | id 10 comes back. *This is the test that separates a filter applied **inside** the search from one applied to its results: id 10 would never enter an unfiltered top 3 for this question, so a post-filtered implementation returns nothing here and fails.* |
| AC8 | core | the ingested photos | the image lane is queried with the stored vector of `circle_red_on_white.png` | that same point is the top hit with a score ≥ 0.99 |
| AC9 | core | the ingested corpus | a recall for "soup" is requested | the response validates against *recall-response*: exactly the three lanes, no id in more than one lane, every item carrying its own `weak` verdict, and both cutoffs reported |
| AC10 | core | the ingested corpus | a recall runs with the text cutoff set above every returned score | every text item comes back with `weak: true`, none is presented as the answer, and none is dropped from the response |
| AC11 | core | the ingested corpus and the top hit for "where did I leave the bike" | that memory is deleted and the question re-run | the previously second result is now first with its score unchanged to within 1e-6, the deleted id is absent, and the point count has dropped by exactly one |
| AC12 | core | a store holding the corpus, optimised and flushed | the store is closed and reopened from the same directory **in a new process** | the point count is unchanged and the same question returns the same top id with the same score |
| AC13 | core | the 8 fixture photos stored, nothing taught yet | `widget_a_3.png` is recognised | the nearest point is one of the 8 photos, not a widget view, and its score is lower than the score the same photo reaches in AC14 |
| AC14 | core | views `widget_a_1/2` taught under label "widget-a" and `widget_b_1/2` under "widget-b" | `widget_a_3.png` is recognised | the nearest point is a taught **widget-a** view and the reported label is "widget-a" |
| AC15 | core | the taught object store | recognition of `widget_a_3.png` runs with the threshold set to 1.01, then to 0.0 | the first returns verdict `UNKNOWN` while still reporting the nearest label and score; the second returns verdict "widget-a" — and the shipped configuration carries exactly one threshold constant, 0.80 |
| AC16 | core | ids 2 and 3 (same fact, 12 days apart; id 2 is the closer paraphrase of the question, id 3 the newer and wordier note) | "side gate code" is asked by similarity only, then with the D4 freshness ranking | similarity alone ranks id 2 above id 3; with freshness applied id 3 ranks first. *If similarity alone already ranks id 3 first, the fixture has failed to reproduce the stale-value case — a fixture-design defect: report it and regenerate so the older note is the closer paraphrase. The assertion does not move.* |
| AC17 | core | id 13, which has no timestamp | the D4 freshness ranking is applied | id 13 is scored as current and is still returned — not dropped and not scored as infinitely old |
| AC18 | core | the built app | the server is started and the page fetched | it listens on 0.0.0.0:4000, serves the page at `/`, its API returns JSON, and no URL in the served HTML or JS begins with `/` |
| AC19 | core | the built source tree | it is searched | no import of an LLM SDK and no outbound HTTP call exists on the query path |
| AC20 | core | `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` unset (or set to invalid values) and the models already downloaded | the full core suite is run | every core criterion still passes |
| AC21 | voice | a voice record whose `audio_file` is present in the workspace | it is ingested | the stored payload holds the transcript the speech model produced and no audio bytes, and the speech session is released before any embedding model is loaded |
| AC22 | core | the built app and its output | every number it displays is traced | each is either computed from this build's own store or measured by this build at run time; none of the course's latency figures appears as this build's measurement |

Every business rule reaches at least one criterion above, and every criterion traces back to a rule.

---

## 6. Standing Permissions (in force for the entire build)

**Always**
- Install the whole dependency set in one early batch, and say what it costs before starting it.
- Keep every URL in the served page relative, and every long-running process in the background.
- Run the core suite after each milestone and paste the real output.
- Write decisions, thresholds and cutoffs into files (`resolved-decisions.md`, a config module), not
  only into chat.
- Report a blocked or failing criterion as failed, with its output.

**Ask First** *(each entry is a trade-off the course argued aloud, whose wrong side either forces
rework or changes a guarantee no test would catch)*
- **Changing the recognition threshold from 0.80** — the instructor calibrated it against 6 matches
  and 220 non-matches and says plainly that the right value depends on how much a false positive
  costs you versus a false negative (Lesson 5). Changing it silently re-draws the known/unknown line.
- **Changing either lane cutoff (0.6 text, 0.23 photo)** — Lesson 4 sets them per model; a change
  moves results between "answer" and "weak" without failing any criterion.
- **Changing the freshness weight or half-life, or turning ranking off** — cross-referenced to **D4**.
  Weight 0.2 is what keeps meaning ahead of recency; raising it lets recent-but-irrelevant win.
- **Switching to, or adding, a cloud store** — cross-referenced to **D2**. It introduces a credential
  and re-uploads every point.
- **Changing an embedding model or a vector width** — every stored point must be re-embedded, and
  stored scores stop being comparable with anything recorded before. *(project hardening)*
- **Deleting any memory the person did not ask to forget**, including wiping the store to "start
  clean" — deletion is irreversible and the course teaches it as a deliberate act.

**Never**
- Add an LLM, or route any answer through a generative model.
- Read or use the container's provider API keys; commit any secret.
- Present the course's measured latency numbers — or any number not measured by this build — as this
  build's own.
- Edit a fixture record to make a criterion pass.
- Create or edit `AGENTS.md` in the workspace. **[environment]** the IDE rewrites it at every boot,
  so guidance written there is silently lost.
- Serve on a port other than 4000, run a second server, or use root-absolute URLs in the page.
- Claim a criterion passes without its output.

---

## 7. Test Plan & Self-Verification

```bash
python3 --version                      # must be >= 3.12; report the actual value
python3 -m venv --system-site-packages .venv && . .venv/bin/activate
pip install -r requirements.txt        # the pins in §2, one batch

python -m fixtures.gen_images          # writes fixtures/images/, deterministic
pytest -q tests                        # the core tier
pytest -q tests -m voice               # the voice tier (needs the speech model)

uvicorn app.main:app --host 0.0.0.0 --port 4000   # then open the preview
```

After the suite runs, report **per acceptance criterion**: its id, pass or fail, and the evidence —
the test name and the assertion output, or the file path and line where the behaviour lives. Numbers
that appear in the app (point counts, scores, any timing) must be traceable to this build's own run.

"Should pass", "looks correct" and "works as expected" are treated as failures: they mean it was not
run. A criterion that cannot run in this environment is reported as blocked, with the reason —
never quietly skipped.

---

## Runtime environment — the AI Coding Lab (binding) [environment]

Everything in this section comes from `environment.md`, not from the course.

- **One container per learner, no terminal, no notebook.** The person you are building for works
  entirely through chat; they see your tool calls and the files you touch, and the app appears in a
  preview pane beside the conversation.
- **Port 4000, one server, relative URLs** — restated as R15 because it is the single most common way
  a working app appears broken: the preview is reverse-proxied under a path prefix, so a
  root-absolute URL resolves against the IDE, not the app. WebSocket upgrades are not proxied;
  ordinary HTTP and streaming responses are.
- **The workspace is the record.** Only what is on disk survives into a new chat or reaches the
  grader. Decisions, thresholds and results belong in files.
- **Preinstalled:** Python 3 with venv, Node 22, sqlite3, git, build tooling; FastAPI, uvicorn,
  python-dotenv. **Not** preinstalled: everything in §2's memory stack. Outbound network works, so
  installs and the one-time model downloads succeed — they just cost wall-clock inside the session.
- **Memory is finite.** Loading a speech model and both embedding models at once is the realistic way
  to get the process killed; R11 exists for that reason as much as for the course's.
- **`AGENTS.md` is rewritten at every boot** — never author one (§6 Never).
- **Questions are asked one per message**, with the options in a fenced `choices` block placed last;
  the turn ends there. This is the same discipline §0 already requires.

---

## Course Context Pack (embedded — agent-readable)

### CTX-A. The pattern

`capture → embed per modality → store as points (vector + payload) → retrieve (nearest, filtered,
re-ranked) → decide and present` — with two operations hanging off the store: **teach** (write
example vectors under a label) and **forget** (delete points). The course draws this as a closed
four-stage loop — *capture → embed → store → recall*, with recall feeding back into capture — and
every lesson adds one stage or one modality to it.

**The framing underneath it all: the model is frozen, the memory grows.** Nothing is trained,
fine-tuned or adapted; what changes between "it doesn't know this" and "it does" is a set of vectors
written to disk. That is why teaching costs a few photos instead of a training run, and why the
capability of the finished thing is a property of its memory rather than of its weights.

- **Capture** — a memory arrives as typed text, as a photo, or as speech. Speech is turned into text
  at the boundary and never stored as audio, so everything downstream has only two modalities to
  handle.
- **Embed** — a text model turns notes and questions into vectors; a joint image/text model turns
  photos into vectors and lets a typed description reach them. The two models produce different
  widths on different score scales, which is why their vectors live in separate named spaces and
  their results are never merged.
- **Store** — one point per memory: an id, its named vector(s), and the whole memory as payload. The
  payload is what lets a result be shown and filtered; the vector is what lets it be found. Fields
  you intend to filter on must be indexed before the filter runs.
- **Retrieve** — *approximate* nearest-neighbour search inside one named space: the engine organises
  stored vectors into a navigable graph and walks it, which is what makes lookup fast enough to feel
  instant and why the index has to be built before it can be searched well. Optionally narrowed by
  payload conditions *evaluated inside the search* (R7), and optionally re-scored by a formula over
  payload values — which is where recency enters.
- **Decide and present** — nearest search always returns its closest point, however poor. Turning a
  neighbour into an answer is a separate act: compare against a cutoff, show what cleared it, dim
  what did not.
- **Teach** — recognition without training: store a handful of example views under one label. More
  views of the same subject make it easier to recognise; nothing is retrained.
- **Forget** — delete the point. The next-best answer moves up; nothing else changes. Stores handle
  very large numbers of memories, but lookup cost still grows with size, so forgetting has value
  beyond privacy.

This whole loop runs on the device, with no inference provider anywhere in it.

### CTX-B. Failure-mode catalog

1. **An answer that sounds authored.** *Symptom:* the assistant explains rather than recalls.
   *Cause:* a generative model in the answer path. *Fix:* the pipeline has none — what comes back is
   the memory itself and its score. *Enforced by R1, R2 / AC19, AC20.*
2. **One blended result list.** *Symptom:* photo results and note results interleave, and the
   ordering looks arbitrary. *Cause:* two models' scores compared as if they shared a scale.
   *Fix:* separate lanes, separate cutoffs, no cross-model sorting. *Enforced by R5 / AC9.*
3. **A weak match presented as the answer.** *Symptom:* a question about a bike returns a note about
   parking. *Cause:* nearest search always returns something; without a cutoff the closest thing
   becomes "the answer". *Fix:* score against the lane's cutoff and mark what falls below it.
   *Enforced by R6 / AC10.*
4. **A filter that quietly does nothing.** *Symptom:* narrowing by category or price changes no
   results. *Cause:* filtering a payload field that was never indexed. *Fix:* create the field
   indexes at initialisation; a point missing the field cannot satisfy a range condition on it.
   *Enforced by R7 / AC3, AC7.*
5. **A forgotten memory that keeps answering.** *Symptom:* a deleted note still tops the results.
   *Cause:* deletion that never reached the store, or an index left stale. *Fix:* delete the point,
   then confirm the next-best has moved up and the remaining scores are untouched. *Enforced by
   R8 / AC11.*
6. **Every score slightly wrong.** *Symptom:* retrieval is plausible but consistently mediocre.
   *Cause:* the text model applies different task prefixes to documents and to queries, and one call
   was used for both. *Fix:* embed questions with the query call, stored text with the document call.
   *Enforced by R9 / AC6.*
7. **Dimension and space mistakes.** *Symptom:* writes rejected, or a photo query scored against
   notes. *Cause:* one shared vector space, or a width that does not match its model. *Fix:* declare
   both named spaces with their widths up front and embed the question once per space. *Enforced by
   R3, R4 / AC1, AC4, AC8.*
8. **Audio kept as audio.** *Symptom:* voice memories cannot be searched. *Cause:* storing the
   recording instead of its transcript. *Fix:* transcribe at ingest and store the text; a voice
   memory is a text memory that remembers where it came from. *Enforced by R10 / AC5, AC21.*
9. **The process killed mid-build.** *Symptom:* the run dies during ingestion of a mixed corpus.
   *Cause:* a speech model and both embedding models resident at once. *Fix:* transcribe first,
   release that session, then load the embedding models. *Enforced by R11 / AC21.*
10. **Memories that do not survive a restart.** *Symptom:* a taught object is gone after a reopen.
    *Cause:* writes never optimised and flushed to disk. *Fix:* flush before announcing success, and
    prove it by reopening in a new process. *Enforced by R12 / AC12.*
11. **A confident wrong name.** *Symptom:* an object never taught is named as something else.
    *Cause:* treating the nearest hit as the verdict. *Fix:* a threshold decision, with `UNKNOWN`
    below it and the nearest label still reported. *Enforced by R13 / AC13, AC14, AC15.*
12. **Recognition treated as training.** *Symptom:* adding a subject is expected to need a training
    run. *Cause:* the mental model of fine-tuning. *Fix:* teaching writes example vectors; a few
    views of one subject are enough, and more views improve it. *Enforced by R16 / AC14.*

### CTX-C. Decision background *(reference only — decisions live in the Decision Ledger)*

1. **On-device versus cloud → D2.** Lesson 1 makes the case for keeping memory local: it works with
   no connection, recall is faster and more reliable than a network round trip, and private memories
   stay private with no cloud storage or API involved. The same lesson concedes what cloud buys —
   sharing memories between devices, and compute and storage a small device does not have — and
   states that the two can be combined. The course works locally throughout; the sync path is named
   and shipped as helper functions, but no lesson in the supplied materials exercises it, and it
   needs a cluster URL and an API key.
2. **One store or several → D3.** The course does both: the finished assistant keeps text and image
   spaces in one store, while object recognition is built in a store of its own before the taught
   object is folded into the assistant's store as a single point carrying both a photo vector and a
   note vector. The pattern is indifferent; the operational consequences are not. Two drafted slides
   make the one-store arrangement explicit: *Two Encoders, One Shard* (one store, two named vectors,
   768-d text from one model and 512-d image from another) and *One Point, Two Doors* (a single point
   carrying an image vector, a text vector and a note, reachable "by sight" or "by words"). Neither
   appears in a video, but both match what the Lesson 5 notebook builds.
3. **Meaning versus recency → D4.** Lesson 5 builds the failure deliberately: two memories hold a
   code, the older one wins on meaning alone, and the newer one is the one you want. The fix adds an
   exponential decay over the timestamp to the similarity score, capped by a weight so that meaning
   still leads. The mechanism is a two-step query — pull a wider candidate set by meaning, then
   re-score just those. A memory with no timestamp is treated as current rather than discarded.
4. **Where the thresholds came from.** The recognition threshold was calibrated, not guessed: the
   instructor scored a held-out view of each known subject against its own taught views (6 matches)
   and against unrelated subjects and scene photos (220 non-matches), found the lowest match at 0.86
   and the highest non-match at 0.74, and settled on 0.80 as the middle. He says explicitly that the
   right value depends on the relative cost of false positives and false negatives in your
   application. The two recall cutoffs (0.6 text, 0.23 photo) differ because the two models score on
   different scales — not because photos matter less.
5. **The latency figures are background, not a target.** The course's curve was measured on the
   instructor's own machine (a desktop-class CPU, medians over 300 queries per size) and replayed in
   the lesson rather than timed live, because a store of a quarter-million vectors does not fit in a
   course container and a number timed on a shared sandbox moves every run. The shape is the lesson:
   growing the store 250× raised lookup time roughly 50×, while the cost of embedding the question
   stays flat regardless of store size. Treat it as intuition about where time goes, never as a
   benchmark to reproduce (R14).
6. **Course identifiers, for reading the lessons.** The course calls a store directory a *shard*
   (also "collection"), names them per lesson, and allocates ids by purpose — seed objects at 0–2,
   taught views from 100, bulk photos from 1000, an ad-hoc note at 900, the assistant's taught
   memory at 5000. None of these names or ranges is binding here; they exist so the lessons are
   recognisable when you go back to them. This spec picks its own ranges in §5. The lessons' own
   result sets are small throughout — searches fetch between 3 and 10 candidates depending on the
   call site, and after a bulk write the lessons preview only the first 4 notes or 6 photos. Those
   are presentation conventions for a recorded lesson, not constraints on the pattern; R5 fixes what
   this build fetches.
7. **Scale of the course's own corpus, for context.** The lessons work with a day of 42 captures (20
   text, 17 photo, 5 voice), a 165-photo image bank, about a hundred notes of earlier history, and
   six object subjects with two or three views each. The fixture corpus in §5 is deliberately smaller
   and wholly invented; nothing about the pattern depends on corpus size.
8. **The merged inbox the course drafted and dropped → backs R5.** A slide titled *What comes back*
   was drafted for Lesson 4: one question fanned out to both models, and the photo, voice and text
   results "merged into one inbox ranked by score", with low scores flagged as weak. It appears in no
   video, and the display the course actually shipped does the opposite — three side-by-side lanes,
   with its own source stating that a blended list is never the right rendering. The mechanical
   reason is the one Lesson 4 narrates aloud: the two lanes come from different models, so their
   scores do not share a scale and a single ranked list would be ordering incomparable numbers. Two
   supplied materials genuinely disagree here; the shipped code and the narration win over a slide
   that was cut, so this resolves as a business rule (R5) and **not** as a decision anyone is asked
   to make — offering "merged or lanes?" as a menu would invite picking the side the course removed.
9. **What a store is on disk → backs D2, D3 and R12.** A drafted slide, *In-Process and On-Disk*,
   draws the engine as a library living inside the application's own process — not a server — with
   the memory itself a directory holding a config file, segment files and a write-ahead log, and a
   dashed, explicitly *optional* link out to a central server. Lesson 2 says the same in words:
   "there is no separate vector database server, and the memory is stored in a folder on the device."
   That shape is why durability is an explicit act (R12): a write reaches the log and the segments
   only when the store is optimised and flushed, and why "back up your memories" means copying a
   directory.
10. **A third lesson numbering exists — do not use it.** Both decks were built against an earlier
    six-lesson plan: their title cards read "Lesson 2: Store and Recall", "Lesson 3: Finding the
    Right Memory", "Lesson 5: Teaching It to See", and a *Course Map* slide lists six lessons
    ending with one on the robot. The final course has five, and every deck number is off by one.
    Transcript numbering is authoritative throughout this spec (CTX-E).

### CTX-D. Perishable assumptions

Concepts in CTX-A, CTX-B and CTX-C are durable. The following names are **era-specific — treat them
as search keywords against current documentation, not as guaranteed imports**:

- Store package and symbols: `qdrant-edge-py` / `qdrant_edge`; `EdgeShard`, `EdgeConfig`,
  `EdgeVectorParams`, `Distance.Cosine`, `Point`, `UpdateOperation` (upsert / delete / create field
  index), `QueryRequest`, `Query.Nearest(using=…)`, `PayloadSchemaType.Keyword` / `.Float`,
  `Filter`, `FieldCondition`, `MatchValue`, `RangeFloat`, `Prefetch`, `Formula`, `Expression.Decay`,
  `DecayKind.Exp`, `ScrollRequest`, `info().points_count`, `optimize()`, `flush()`, `close()`,
  `load()`. On-disk artefacts of a store directory, as the deck draws them: `edge_config.json`,
  `segments/`, `wal/` — implementation detail that may be renamed at any version; never depend on
  these paths, only on the directory being the unit you copy or delete.
- Embedding packages and models: `fastembed` (`TextEmbedding`, `ImageEmbedding`, its document-embed
  versus query-embed calls); `nomic-ai/nomic-embed-text-v1.5` (768), `Qdrant/clip-ViT-B-32-vision`
  and `Qdrant/clip-ViT-B-32-text` (512).
- Speech: `onnx-asr`, model `whisper-base`, CPU execution provider.
- Version pins as the course froze them: store 0.7.2, fastembed 0.8.0, onnx-asr 0.12.0, onnxruntime
  1.27.0, tokenizers 0.23.1, numpy 2.5.1, Pillow 12.3.0; Python 3.12+ (validated on 3.14.6).
- **Known defect in the course material, worth knowing before you copy a pattern from it:** the
  recognition lesson defines its threshold constant under one name and reads it under another in the
  same cell, so that cell raises a `NameError` as written. The value is the one on the line above.
  R13's single-named-constant requirement exists because of exactly this.
- **No "current best model" names are pinned anywhere in this spec.** The models above are the
  course's own, recorded as provenance. If a newer local embedding or speech model is worth using at
  build time, that is the gate-time "(Recommended)" judgment (§0), not a fact this file should carry.
- **Parameter compatibility.** Nothing here calls a hosted inference API, so no request-parameter
  compatibility question arises. If cloud sync is ever enabled (D2), the server-side collection must
  declare the same named spaces and widths as the local store, or points will not load.

### CTX-E. Provenance map

Lesson numbering follows the transcripts, which are authoritative. **Three numberings exist in the
materials** — the transcripts' (used here), the notebook filenames' (`L3`–`L5`, which happen to
agree), and the slide decks', which follow an abandoned six-lesson plan and is off by one; never
cite the deck's. Lessons 1 and 2 are video only and have no notebook. Slides are cited as **shown**
(8 of them appear in a lesson video) or **drafted** (15 exist only in the decks); a drafted slide is
weaker evidence than shipped code or spoken narration, and where the two conflict the drafted slide
loses — see CTX-C8. **Nothing in this spec requires course-platform access.**

| Lesson (transcript numbering) | What came from it |
|---|---|
| **1. Why Devices Need Memory** | CTX-A (the retrieval loop, text and image in one space via a joint model); CTX-B1; CTX-C1 (the on-device versus cloud argument) → **D2**; the "no LLM, no retraining" guarantee → R1 |
| **2. Building the Device** | CTX-A framing — everything including the models and the search runs inside the application, with no separate database server and memory in a folder on the device; the point that the memory loop is the transferable part, not the specific hardware |
| **3. Store, Find, and Forget Memories** | The store/query/index/filter/delete surface → R3, R7, R8; the empty-store demonstration → AC2; the two named spaces and their widths → R3; cross-modal retrieval from a typed description → R4; CTX-B4, B5, B7; CTX-C5 (the latency curve) |
| **4. Your On-Device Assistant** | Three lanes with per-model cutoffs 0.6 / 0.23 → R5, R6; voice transcribed on-device and stored as text → R10; releasing the speech model before embedding → R11; the near-miss ("park" versus "parking the bike") → CTX-B3; adding a memory and recalling it immediately |
| **5. Teaching Your Assistant to See** | Teaching as writing example vectors → R16; the threshold decision and its calibration → R13, CTX-C4; the stale-code failure and the freshness formula → **D4**, CTX-C3; closing and reloading the store from disk → R12; the finished assistant answering from both lanes with no LLM |
| *Slide descriptions (across lessons)* | **Shown:** Lesson 1's five "Answered on Device" slides → CTX-A's note→vector→memory→top-matches loop, the two-encoder shared space, and "a match is a decision rule, not a model" → R13; Lesson 3's *Anatomy of a point* → the §3 record contract, and *Cross-Model recall* → R4. **Drafted (in no video):** *Frozen and Growing* → CTX-A's framing; *In-Process and On-Disk* → CTX-C9, R12; *Filter inside Query* → **R7's pre-filtering clause and AC7b**; *Two Encoders, One Shard* and *One Point, Two Doors* → CTX-C2, D3; *What comes back* → CTX-C8, the design R5 rejects; *Course Map* → CTX-C10's numbering warning |
| *`environment.md` (not course material)* | Everything labelled **[environment]**: R2's key rule, R11's operational weight, R15, §2's install-cost note, the *Runtime environment* section, and §0's `choices`-fence mechanism |

---

## Final deliverable note to the build agent

When the build is complete and the criteria have been reported with their evidence, close by drawing
the app's infra/structure diagram — the processes, the store and its two named vector spaces, the
ingest path for each modality, the query path with its two lanes and cutoffs, and where the teaching
and forgetting operations write — and introduce it with exactly this sentence:

**"This is the infra/structure diagram of this app."**

---

*Spec version 1.0 · Course: Building On-Device AI Memory with Qdrant Edge (5 lessons, transcript
numbering) · Target: the AI Coding Lab standalone takeaway · Generated 2026-09-11 by
spec-generation-guide `8e44ecb`.*

*Living document: if the build produces something this spec did not intend, add the missing
constraint here and re-run — do not patch it only in the code.*
