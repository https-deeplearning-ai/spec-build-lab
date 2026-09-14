# Spec: On-Device Memory Assistant — Standalone Takeaway

> **What you're building.** You type — or speak — a question like *"where did I leave the spare charger?"* and the app answers by handing back the note, the voice memo, or the photo from your own captures that actually holds the answer, ranked by meaning, with the most recent memory winning when two of them disagree. It runs as one process on your own machine, with no model API, no server, and no network once the local models are on disk. **Fastest path:** answer the first question of the pre-build gate below with *"recommended baseline build"* and the whole thing gets built end to end from this file alone. **The build is COMPLETE when the offline acceptance suite passes.** A credential unlocks only the `live`-tagged tests (the optional server-sync realization on Ledger row D7) and live use of the finished app against your own data — never any part of completion.
>
> **This file is self-contained.** The embedded **Course Context Pack** replaces every reference to the course: you do not need the notebooks, the videos, or the platform to build this.
>
> **(CTX-X) anchors** mark knowledge derived from the course materials. The **Decision Ledger** below holds every point where this build could legitimately diverge, each pinned to exactly one course-derived default, so the spec builds and evaluates as-is with zero intake from you.
>
> **Provenance.** Generated from the *Building On-Device AI Memory with Qdrant Edge* notebook dump (`sc-Qdrant-C3-notebook-context.md`), transcripts (`sc-Qdrant-C3-transcripts.md`, five lessons) and slide descriptions (`sc-Qdrant-C3-slide-descriptions.md`) on 2026-09-14, by spec-generation-guide.md at repo commit `8e44ecba383841fd78b6fc157a331f94d0ab5f68`.

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
2. **First question — recommended baseline build, or customize?** Ask exactly one question with
   two options: the **recommended baseline build** — every Ledger row resolves to its Default:
   mostly the course's own choices, with a lighter stand-in wherever the course's choice needs
   setup you may not have (a paid API key, an admin-provisioned service); the step-5 checklist
   marks exactly where the baseline differs from the course — or **customize** the decisions row
   by row. If the user chooses the baseline, skip step 3 — go straight to the step-5 checklist
   and build. If the user chooses customize, continue with step 3.
3. **Present the Ledger ONE ROW AT A TIME — one question per row.** This Ledger has **11 rows
   (D1–D11)**, so that is **11 separate questions**. For each row ask a single question: the
   **Decision** as the prompt, its **Options** as the choices. Append
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

---

## Decision Ledger (§0 above requires the build agent to present these before building)

These are the points where this build could diverge. Every row has a course-derived default, so the spec is buildable and evaluatable as-is; change a row only when applying to a real project or when you have reason to prefer another option.

| # | Category | Decision | Invariant (must hold) | Default (course-derived) | Options | Trade-off | Owner |
|---|---|---|---|---|---|---|---|
| D1 | learner | **Project** — what you are building | *(none — the pattern imposes no requirement on the subject of the project)* | A personal day-memory assistant: a library plus a command-line entry point that ingests a day of text notes, voice memos and photos from local files and answers typed questions about them. **This is the course's example realization re-expressed on this spec's own synthetic fixture corpus (§5) — expect to swap it** when your project differs; the pattern (CTX-A), not this scenario, is what must survive. | (a) the day-memory assistant on the fixture corpus (course example shape); (b) a field/inspection device that remembers what it was shown; (c) a personal archive over your own documents; (d) any other subject, free-text | Swapping the project changes the fixture corpus, the queries in §5, and the categories in the payload — nothing in the pipeline (CTX-A) or in any other row. | learner |
| D2 | learner | **Data / inputs** — what it remembers, and where that lives | Every input must reduce to **either a text string or a still image**, and must carry a **capture time** — the recency stage (R6) has nothing to rank on without one. Audio is admitted only via a transcription step (R12). *(Exercised by AC2 and AC10.)* | The synthetic fixture corpus defined in §5: one JSON file of 14 authored records plus images and audio **generated by `make_fixtures.py`** at build time. No course data and no binary assets travel in this spec. | (a) the fixture corpus; (b) your own folder of notes/photos/voice memos on local disk; (c) an export from a notes or photos app, converted to the §3 record shape; (d) other, free-text | Real data replaces the fixture facts the §5 acceptance criteria assert, so the ACs must be re-pinned to facts you can assert. Everything upstream and downstream is unchanged. | learner |
| D3 | learner | **Goal** — what "working" means | The goal must be reachable by **retrieval alone**: the answer is one or more stored memories, returned verbatim with their metadata and scores. Anything requiring a memory to be *composed*, summarized, or reasoned over is outside the pattern (R15, §1). | A question returns the nearest memories per modality lane, each lane gated by its own confidence floor, recency-weighted in the text lane; when nothing clears its floor the app says so instead of answering. | (a) recall (question in, memories out) — the course's goal; (b) recognition (photo in, label or UNKNOWN out); (c) both lanes of the same store; (d) other, free-text | Dropping recognition removes R13/AC12/AC17 and the calibration procedure (R17); dropping recall removes most of §5. The store and its schema are unchanged either way. | learner |
| D4 | learner | **Model / provider** — the encoders | **Three separately-addressable local encoders, none requiring a credential:** a text encoder with distinct *document* and *query* forms (R8); an image encoder whose text tower embeds into the **same** space as its vision tower (cross-modal recall); and a speech-to-text model. Text and image scores are **never** comparable (R4), so each space keeps its own width and its own floor. | The course's trio, all run locally on CPU through their course-pinned runtimes: `nomic-ai/nomic-embed-text-v1.5` for text (**768** dimensions), `Qdrant/clip-ViT-B-32-vision` / `Qdrant/clip-ViT-B-32-text` for images and cross-modal queries (**512** dimensions), and `whisper-base` for voice. No account, no key; one first-run download, offline after that. | (a) the course's trio (course default); (b) any other local sentence-embedding + CLIP-family pair at their own widths; (c) a hosted embedding API (heavy setup: a paid account and an API key, and it takes memories off the device — conflicts with D7's local-only default and R15); (d) other, free-text | Changing either encoder changes its vector width, **invalidates every stored vector, and forces a full re-embed and re-ingest** — the single most expensive change in this build (§6 Ask First). The calibrated floors (R17) must be re-derived too: they are properties of the encoder, not of the data. | course+learner |
| D5 | learner | **Environment** — where it runs | Memory **must survive process exit and power loss** (R10) and **must answer with no network** after the one-time model download (R15). No specific hardware: whatever runs the chosen encoders on CPU is enough. | One local process on the learner's own computer (Python 3.12+), with the memory store as a plain directory on local disk beside the code. | (a) your own computer (course default — the course states plainly that no specific hardware is needed and that the final lesson runs the same code on a personal machine); (b) a single-board computer such as a Raspberry Pi-class device; (c) an embedded compute module on a robot or camera rig (heavy setup: hardware the learner must buy and provision); (d) other, free-text | Smaller devices trade recall latency and model-load time for portability; the code, the store layout and every acceptance criterion are identical. The course's own latency figures are machine-specific and are *not* a target (CTX-C6). | course+learner |
| D6 | learner | **Scope boundary** — what this build leaves out. **Gate: read the full §1 "Not Included" list aloud inside this question, item by item, before offering the options** — §1 is not a Ledger row, so this question is the only place the learner ever sees it. | *(none)* | **Keep as-is:** every §1 exclusion stands and the full acceptance set in §5 is built. | (a) keep the boundary as written; (b) bring something back — say which §1 item, in free-text. Handling is determinate: *live camera/microphone capture, a graphical interface, frame-by-frame video, encryption at rest* are additive and owned by no other row → restorable here; *the robot hardware build* is named by the course but never built → buildable, but this spec supplies no parameters and no acceptance criteria for it, and you will be told so; *server sync* → owned by D7, *encoder choice* → D4, *store technology* → D10, decided there and never twice; *integration into an existing codebase* → outside this build mode, unavailable. A genuine additional exclusion also goes in free-text and must name the acceptance criteria it retires. | Restoring an item adds work with no acceptance criteria behind it unless you write them; excluding more retires the ACs you name. | learner |
| D7 | design-argued | **Where memory lives** — on the device only, or synced to a server | The device **must still answer with no network at all**. Any sync is additive and one-way-optional; it may never become the read path. | **Local only.** Nothing leaves the machine; there is no server component and no credential anywhere in the build. | (a) local only (course default); (b) local, plus optional one-way sync of a shard snapshot to a Qdrant server — *heavy setup: a hosted or self-run Qdrant cluster plus `QDRANT_URL` and `QDRANT_API_KEY`; the supplied materials contain the four helper functions and the pinned client for this, but the appendix notebook that used them is absent from the supplied repo copy, so the spec carries no worked parameters for it*; (c) server-only storage — outside the pattern, listed for completeness and excluded by the invariant | Lesson 1 argues both sides aloud: on-device wins because it works with no connection, avoids the network round trip, and keeps private memories private with no cloud storage or API; a server is genuinely useful *"when some memories need to be shared"* and when the device runs short of compute or storage, and the instructor states you can combine local and cloud retrieval if your use case requires it — but *"for today, we will only be working locally."* (Lesson 1: Why Devices Need Memory.) Cost of switching: a credential to manage, secrets to keep out of the repo, and the privacy guarantee becomes conditional. | course+learner |
| D8 | design-structural | **Memory-store topology** — one store for everything, or one per purpose | A single memory **must be reachable both by sight and by words**: one point may carry more than one named vector, and the spaces must stay separately addressable so a query names which space it searches and no score crosses spaces (R4). *(Exercised by AC22.)* | **One store, two named vector spaces** (`text` and `image`, widths pinned in row D4), with a taught subject stored as a *single* point carrying both its image vector and the text vector of its note. This is what the course's final end-to-end assistant does. | (a) one store, two named spaces, dual-vector points (course default); (b) a dedicated object store for taught subjects plus a separate store for day memories — also exercised by the course while teaching, and the right shape when the two have different lifecycles; (c) one store per modality | Redraw the diagram and a box disappears or appears. One store keeps a taught subject findable from a photo *and* from a typed question, and keeps one flush/restore path; separate stores let you wipe or re-teach object memory without touching the day's captures, at the cost of querying two handles and merging nothing (you cannot merge — R4). | course+learner |
| D9 | design-structural | **Sub-threshold results in recall** — mark them, or suppress them | A result below its lane's floor **must never be presented as a confident answer** (R3, R5). What happens to it beyond that is this row's choice. | **Mark and keep.** Below-floor hits are still returned and still rendered, visibly dimmed/flagged as weaker, so the person can see *why* the app was unsure. This is what the course's memory inbox does. | (a) mark and keep (course default); (b) suppress — below-floor hits are dropped from the result entirely and the lane reports "no confident answer" | The guarantee changes, not a number. Marking teaches the user where the boundary is and makes a near-miss recoverable by eye — the course leans on this when a note about a park surfaces as a weak match for a question about a parked bike (Lesson 4). Suppressing is the right call for a device with no screen, a spoken answer, or any surface where a dimmed result reads as an answer anyway. | course+learner |
| D10 | realization | **The vector memory store** | An **embedded, credential-free** store that persists to a local directory and offers, in one query surface: multiple independently-named vector spaces per point with an arbitrary payload; nearest-neighbour search naming the space to search; a payload **filter applied inside the query**, not after it; point deletion; and a **formula re-rank over a payload field** fed by a wider prefetch (R6). Retrieval must work with no network. | **Qdrant Edge (`qdrant-edge-py`, the course's pinned 0.7.2), used as an embedded library — no server process.** §3 dependency precedence **branch 2 applies: the specific technology IS the taught subject** (the course is *Building On-Device AI Memory with Qdrant Edge*), so it is reproduced as the default rather than substituted. No substitution is needed in any case: on the §3 tier ladder this is **tier 2 — an embedded library installed by the package manager, with no separate process and no credential** — so it is not a heavy dependency at all, and the whole setup cost is one `pip install`. | (a) Qdrant Edge as an embedded library (course default); (b) a server-based vector database, Qdrant or otherwise — *heavy setup: a separate process to run or a hosted cluster to provision, plus credentials*; (c) a stdlib-only brute-force store (tier 1): it can satisfy exact nearest-neighbour over a fixture-sized corpus, but it does **not** satisfy this row's Invariant — in-query payload filtering, indexed fields, and the decay-formula re-rank are the taught query surface and would have to be hand-built, which is the pattern itself, not a realization of it | Leaving the embedded library means either running and supervising a process (b) or reimplementing the query surface (c). Both keep the pattern; only (a) keeps it at one `pip install` and zero operational surface. The API is pre-1.0 — see §2 and CTX-D. | course+learner |
| D11 | contradicted | **Memory id scheme** | Every point id is **unique within its store** and **stable for a given source item**, so re-ingesting the same item updates exactly one point and can never overwrite a different memory (R16). | **A single allocator that namespaces ids by source**, so every source's range is disjoint within a store and stable across runs: `id = source_base + index_within_source`, with `source_base` declared once per source in one place, and an overlap between any two declared ranges raising at registration. | (a) integer id ranges chosen per source by hand, each source's base written where that source is loaded (course default); (b) integer ranges issued and checked by **one** allocator that owns every range in the store; (c) content-derived stable ids (a hash of the source item's identity); (d) opaque UUIDs recorded in a side index | The course sets this **inconsistently**: it allocates by disjoint hand-picked ranges — day memories at 0–41, a bulk photo import starting at 1000, taught views at 100+, a new note at 900, a taught assistant memory at 5000 — while its own history file independently occupies 1000–1101. Those two 1000-based ranges never collide only because the materials happen to put them in different stores; put them in one store, as row D8's default does, and **one source silently overwrites the other with no error**. Picking the scheme up front is cheap; changing it after data exists means a full re-ingest (§6 Ask First). (b) and (c) remove the hazard by construction but cost a lookup or a side index at write time. | course |

---

## 1. Objective

A standalone, fully-local memory assistant: it ingests text notes, voice memos and photos as vectors into one on-device store, and answers a typed or spoken question by returning the actual memories that match — ranked by meaning, gated by a calibrated per-modality confidence floor, and tie-broken by recency — with no LLM, no remote model and no network in the answer path. (pattern: CTX-A)

### Not Included ★

Each item below is out of scope for this build. Ledger row **D6** presents this list at the gate; a learner may ask for an item back there.

1. **Any LLM, chat model, or generated natural-language answer.** The app returns the retrieved memories themselves, with their scores and metadata — it never writes prose about them.
2. **Live camera or microphone capture.** The build ingests images and audio files that are already on disk.
3. **Syncing memories to a server or to another device.** (Owned by Ledger row D7 — decided there.)
4. **Any graphical interface** — no phone app, no web UI, no notebook front-end. The deliverable is a library plus a command-line entry point.
5. **Specific hardware.** No robot, no single-board-computer image, no enclosure, no wiring.
6. **Training, fine-tuning, distilling or quantizing any model.** Subjects are learned by writing example vectors, never by changing weights.
7. **Frame-by-frame ingestion of live video.**
8. **Multi-user accounts, authentication, or per-user memory isolation.**
9. **Encryption of the store at rest, and any data-retention or compliance policy.**
10. **Approximate-index tuning for very large stores** — index parameters, quantization, or more than one shard. The build targets a corpus that fits comfortably in one store on one device.
11. **Integration of this pattern into an existing codebase.** This spec's build mode is a standalone takeaway.
12. **Packaging or distribution** — no installer, container image, service definition, or release pipeline.

---

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
|---|---|---|
| Language / runtime | Python 3.12 or newer | The course's notebook kernels record 3.12.11 and its README states the course was built and validated on 3.14.6. Pick one and record it. |
| Vector memory store | `qdrant-edge-py==0.7.2` | **The Decision Ledger row D10 owns this choice — change it there, not here.** *Version policy, stated honestly:* unlike the usual case, the course's `requirements.txt` **pins every single dependency to an exact version** and says why — so the scores in the saved outputs reproduce. This library is **pre-1.0**, so its API surface is genuinely unstable; reproduce the course's pin rather than floating it, and treat every type name in CTX-D as a search keyword against the version you actually install, not as a guaranteed import. |
| Text embeddings | `fastembed==0.8.0`, model `nomic-ai/nomic-embed-text-v1.5`, 768-d | Ledger row D4. Downloaded once on first run; no account, no key. Disclose the download size to the user before the first run. |
| Image + cross-modal embeddings | `fastembed==0.8.0`, models `Qdrant/clip-ViT-B-32-vision` and `Qdrant/clip-ViT-B-32-text`, 512-d | Ledger row D4. The two towers share one space — that is what makes searching photos with words work. |
| Speech to text | `onnx-asr==0.12.0`, model `whisper-base`, CPU execution provider | Ledger row D4. Must be reachable behind an injectable interface (R12, AC16). |
| Model runtime | `onnxruntime==1.27.0`, `tokenizers==0.23.1` | The course pins these alongside the models because they decide the embedding numbers. |
| Image handling | `Pillow==12.3.0` | Also used by `make_fixtures.py` to generate the fixture images (§5). |
| Numerics | `numpy==2.5.1` | |
| Test runner | `pytest` (any recent version) | **Project hardening** — the course ships notebooks, not a test suite. Markers: `live` (needs a credential; excluded from the completion run). |
| Server client | `qdrant-client==1.18.0` | **Installed only if Ledger row D7 is changed from its default.** Reads `QDRANT_URL` and `QDRANT_API_KEY` from the environment. |

**Secrets.** No credential is required by the default build. If D7 is changed, `QDRANT_URL` and `QDRANT_API_KEY` are read from the process environment only — never written to a file in the repo, never printed, never committed. The store directory and any generated fixture assets are git-ignored.

---

## 3. Input/Output Contracts ★

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.invalid/on-device-memory/schemas.json",
  "$defs": {

    "MemoryRecord": {
      "title": "One captured memory, before it is embedded",
      "type": "object",
      "required": ["id", "source_type", "captured_at"],
      "additionalProperties": false,
      "properties": {
        "id":          { "type": "integer", "minimum": 0,
                         "description": "Unique within a store and stable for this source item (R16, Ledger D11)." },
        "source_type": { "enum": ["text", "voice", "photo"] },
        "captured_at": { "type": "integer",
                         "description": "Capture time, epoch seconds. Required: the recency stage ranks on it (R6)." },
        "category":    { "type": "string" },
        "location":    { "type": "string" },
        "text":        { "type": "string", "minLength": 1,
                         "description": "The searchable words of this memory. For a voice memory this is the transcript (R12)." },
        "price":       { "type": ["number", "null"] },
        "image_ref":   { "type": "string", "minLength": 1,
                         "description": "Path or name of the image file. The image itself is NEVER stored in the record." },
        "audio_ref":   { "type": "string", "minLength": 1,
                         "description": "Path or name of the audio file. Audio bytes are NEVER stored in the record (R12)." },
        "label":       { "type": "string",
                         "description": "Present only on a taught-subject memory (R13)." }
      },
      "allOf": [
        { "if":   { "properties": { "source_type": { "const": "text" } }, "required": ["source_type"] },
          "then": { "required": ["text"],
                    "not": { "anyOf": [ { "required": ["audio_ref"] }, { "required": ["image_ref"] } ] } } },
        { "if":   { "properties": { "source_type": { "const": "voice" } }, "required": ["source_type"] },
          "then": { "required": ["text", "audio_ref"] } },
        { "if":   { "properties": { "source_type": { "const": "photo" } }, "required": ["source_type"] },
          "then": { "required": ["image_ref"] } }
      ]
    },

    "StoredPoint": {
      "title": "One memory as it lives in the store",
      "type": "object",
      "required": ["id", "vectors", "payload"],
      "additionalProperties": false,
      "properties": {
        "id": { "type": "integer", "minimum": 0 },
        "vectors": {
          "type": "object",
          "minProperties": 1,
          "additionalProperties": false,
          "description": "Named vector spaces. A point may carry one or both; a taught subject carries both (Ledger D8).",
          "properties": {
            "text":  { "type": "array", "items": { "type": "number" }, "minItems": 1 },
            "image": { "type": "array", "items": { "type": "number" }, "minItems": 1 }
          }
        },
        "payload": { "$ref": "#/$defs/MemoryRecord" }
      },
      "allOf": [
        { "description": "A photo memory must carry an image vector; a text or voice memory must carry a text vector.",
          "if":   { "properties": { "payload": { "properties": { "source_type": { "const": "photo" } } } } },
          "then": { "properties": { "vectors": { "required": ["image"] } } } },
        { "if":   { "properties": { "payload": { "properties": { "source_type": { "enum": ["text", "voice"] } } } } },
          "then": { "properties": { "vectors": { "required": ["text"] } } } }
      ]
    },

    "Hit": {
      "title": "One retrieved memory",
      "type": "object",
      "required": ["id", "space", "score", "confident", "payload"],
      "additionalProperties": false,
      "properties": {
        "id":    { "type": "integer" },
        "space": { "enum": ["text", "image"],
                   "description": "Which named vector space produced this score. A score is meaningless without it (R4)." },
        "score": { "type": "number",
                   "description": "Similarity in `space` only. NEVER compare or merge scores across spaces." },
        "ranking_score": { "type": ["number", "null"],
                   "description": "Score after recency re-ranking, where applied (R6). Null where it was not." },
        "confident": { "type": "boolean",
                   "description": "score >= the floor calibrated for `space` (R3, R5)." },
        "payload": { "$ref": "#/$defs/MemoryRecord" }
      }
    },

    "RecallResult": {
      "title": "One question's answer: separate lanes, never one blended list",
      "type": "object",
      "required": ["question", "lanes", "has_confident_answer"],
      "additionalProperties": false,
      "properties": {
        "question": { "type": "string", "minLength": 1 },
        "lanes": {
          "type": "object",
          "additionalProperties": false,
          "required": ["text_notes", "voice_notes", "photos"],
          "description": "Each lane is ranked within itself. There is no cross-lane ranking and no combined list (R4).",
          "properties": {
            "text_notes":  { "type": "array", "items": { "$ref": "#/$defs/Hit" } },
            "voice_notes": { "type": "array", "items": { "$ref": "#/$defs/Hit" } },
            "photos":      { "type": "array", "items": { "$ref": "#/$defs/Hit" } }
          }
        },
        "has_confident_answer": { "type": "boolean" }
      },
      "allOf": [
        { "description": "Ungrounded ⇒ nothing confident: if no hit in any lane is confident, has_confident_answer is false.",
          "if": { "properties": { "has_confident_answer": { "const": true } } },
          "then": { "properties": { "lanes": { "anyOf": [
              { "properties": { "text_notes":  { "contains": { "properties": { "confident": { "const": true } }, "required": ["confident"] } } } },
              { "properties": { "voice_notes": { "contains": { "properties": { "confident": { "const": true } }, "required": ["confident"] } } } },
              { "properties": { "photos":      { "contains": { "properties": { "confident": { "const": true } }, "required": ["confident"] } } } }
          ] } } } }
      ]
    },

    "RecognitionResult": {
      "title": "A photo shown to the store: a label, or UNKNOWN",
      "type": "object",
      "required": ["verdict", "nearest_id", "nearest_label", "score", "threshold"],
      "additionalProperties": false,
      "properties": {
        "verdict":       { "enum": ["known", "unknown"] },
        "nearest_id":    { "type": "integer" },
        "nearest_label": { "type": ["string", "null"] },
        "score":         { "type": "number" },
        "threshold":     { "type": "number",
                           "description": "The calibrated recognition threshold this verdict was decided against (R17)." }
      },
      "allOf": [
        { "description": "A 'known' verdict REQUIRES a label. Nearest-neighbour always returns something; the threshold is what makes it an answer (R3).",
          "if":   { "properties": { "verdict": { "const": "known" } } },
          "then": { "properties": { "nearest_label": { "type": "string", "minLength": 1 } },
                    "required": ["nearest_label"] } }
      ]
    },

    "StoreDescriptor": {
      "title": "The store as created, asserted on fresh initialization (AC0)",
      "type": "object",
      "required": ["directory", "spaces", "indexed_fields"],
      "additionalProperties": false,
      "properties": {
        "directory": { "type": "string", "minLength": 1 },
        "spaces": {
          "type": "object", "minProperties": 1, "additionalProperties": false,
          "properties": {
            "text":  { "type": "object", "required": ["size", "distance"], "additionalProperties": false,
                       "properties": { "size": { "const": 768 }, "distance": { "const": "cosine" } } },
            "image": { "type": "object", "required": ["size", "distance"], "additionalProperties": false,
                       "properties": { "size": { "const": 512 }, "distance": { "const": "cosine" } } }
          }
        },
        "indexed_fields": {
          "type": "array", "minItems": 2, "uniqueItems": true,
          "items": { "type": "object", "required": ["field", "kind"], "additionalProperties": false,
                     "properties": { "field": { "enum": ["category", "price"] },
                                     "kind":  { "enum": ["keyword", "float"] } } }
        }
      }
    }
  }
}
```

> The `768` / `512` / `cosine` constants above are the widths and distance strategy of the encoders pinned in **Ledger row D4**. If D4 is changed, these three constants move with it — they are not independent choices.

---

## 4. Business Rules

Each rule states the behavior and the failure it prevents, carries a provenance label, and reaches at least one acceptance criterion.

**R1 — One point per memory.** *(course-demonstrated, CTX-A)* Every memory is stored as a single point: a stable id, one or more **named** vectors, and a payload carrying the memory's own words (or its file reference) plus its metadata. The vector carries the meaning; the payload rides along and is returned with every hit. Ranking is by vector similarity and, where R6 applies, by the recency formula — nothing else reorders results. → **AC2, AC3**

**R2 — An empty or unmatched store answers with nothing, never with something.** *(course-demonstrated, CTX-B1)* Querying a store before anything is written returns zero results and no error. → **AC1**

**R3 — Nearest is not the same as right; a floor decides.** *(course-demonstrated, CTX-B2)* Nearest-neighbour retrieval **always** returns its closest point no matter how far away it is. Every lane therefore applies a confidence floor calibrated for its own vector space, and when nothing clears it the app reports *no confident answer* (recall) or *UNKNOWN* (recognition). A below-floor hit is never presented as the answer. → **AC7, AC12**

**R4 — Scores from different encoders never meet.** *(course-demonstrated, CTX-B3)* Text scores and image scores come from different models on different scales. They are never compared, never merged into one ranked list, never shown in a shared bar/percentage scale, and never gated by a shared floor. Each named space has its own lane, its own floor, and its own result list. → **AC8, AC9**

**R5 — Weak results are marked, not promoted.** *(course-demonstrated, CTX-B4)* A hit below its lane's floor is returned with `confident: false` and rendered visibly weaker (Ledger D9 default: mark and keep; if D9 is set to *suppress*, it is dropped instead). Either way it can never become the confident answer. → **AC9**

**R6 — Meaning leads; recency breaks ties.** *(course-demonstrated, CTX-B5)* Two memories can carry the same fact with different values at different times, and similarity alone will happily return the stale one. Text-lane ranking therefore combines the similarity score with an **exponential decay on capture time** — value 1 at the newest memory in the store (the decay target is the maximum `captured_at` present, not wall-clock now), halved one **half-life** earlier, fading from there — added as a **bounded** bonus: `ranking_score = similarity + weight × freshness`, where `weight` is the *most* recency can ever add. The course's values, carried as this build's starting point: **half-life = 7 days (604800 seconds)** and **weight = 0.2**, both cited to Lesson 5 and both **post-build levers** (§6 Ask First #5). Candidates are re-scored from a **wider prefetch** than the number of results returned, so a fresher memory outside the top *k* can still surface. A memory with no capture time is treated as current rather than dropped. → **AC10, AC11**

**R7 — Forgetting is real.** *(course-demonstrated, CTX-B6)* Deleting a memory removes its point from the store; it must not appear in any later result, and the store's reported count must fall. Every other result's score is unchanged by the deletion. → **AC6**

**R8 — Questions and documents are embedded differently.** *(course-demonstrated, CTX-B7)* The text encoder distinguishes a *document* from a *query*; stored text goes through the document path and a question goes through the query path, so the scores line up. Using one path for both silently degrades every score in the build. → **AC13**

**R9 — Recall cost grows with the store; forgetting is how you control it.** *(course-demonstrated, CTX-B8)* Embedding the question costs the same whatever the store holds; the lookup grows with the number of vectors, sub-linearly but steadily. The app must expose the store's memory count and a first-class delete operation so the corpus can be pruned deliberately rather than growing without bound. → **AC6**

**R10 — A write is durable.** *(course-demonstrated, CTX-B9)* After a write, the store is compacted and flushed to disk before the operation reports success, so a taught memory survives the device losing power. Reopening the store directory in a **new process** returns the same memories and the same answers. → **AC14**

**R11 — Never remove a store directory while a handle is open.** *(course-demonstrated, CTX-B10)* An open store handle holds its files and flushes when it is dropped; deleting the files underneath it makes that flush fail inside a destructor and surfaces as a native crash rather than a catchable error. Any reset path closes every open handle first, then removes the directory. → **AC15**

**R12 — A voice memory is stored as its transcript.** *(course-demonstrated, CTX-A)* Audio is transcribed on-device at ingest; what is embedded and stored is the transcript text. The record keeps the audio file's *name* (`audio_ref`) and never its bytes. After ingest the answer path never touches the audio file — a spoken question is transcribed by the same step and then travels the ordinary text path. → **AC16**

**R13 — Subjects are learned by writing vectors, never by training.** *(course-demonstrated, CTX-A)* Teaching a subject means embedding two or more views of it and storing them as points sharing one label. No weights change. An unseen view of a taught subject must score higher against the taught views than any untaught photo in the store does. → **AC12, AC17**

**R14 — A filter is part of the query, not a post-filter.** *(course-demonstrated, CTX-A)* Payload conditions are passed into the search so similarity is computed only over points that pass them; results still carry their similarity scores. Every field used in a filter carries an index of the right kind (`category` keyword, `price` float). → **AC5**

**R15 — No LLM, no remote model, no network in the answer path.** *(course-demonstrated, CTX-A)* Answering is pure retrieval. After the one-time model download, the ingest and answer paths make zero outbound network calls, and no generative model exists anywhere in the build. → **AC18**

**R16 — Ids are unique within a store and stable across re-ingest.** *(project hardening — the course allocates hand-picked id ranges per source and relies on separate stores to keep them apart; see Ledger D11.)* One allocator issues ids; ingesting the same source item twice updates exactly one point; two different sources can never be issued the same id in the same store, and an attempt to do so raises rather than silently overwriting. → **AC4, AC19**

**R17 — Floors are calibrated on this build's own corpus, and recorded.** *(project hardening — the calibration **procedure** is course-demonstrated (CTX-C4); treating the course's numbers as portable constants is not.)* Before the floors are used, the build runs the held-out calibration: score each taught subject's held-out view against its own taught views (matches) and against every other subject's views and every scene photo (non-matches), then place the threshold between the highest non-match and the lowest match. The resulting value is written to a named file alongside the corpus it was derived from. The course's own numbers — text floor **0.6**, photo floor **0.23**, recognition threshold **0.80** — are recorded as the starting point and their provenance, not as constants to trust with different data or a different encoder. → **AC20**

---

## 5. Acceptance Criteria ★ (the oracle)

### 5.1 The fixture corpus

Nothing here is copied from the course; every fact is authored for this spec. **No binary assets travel in this file** — the images and audio are generated deterministically by `make_fixtures.py` at build time, from the descriptions below. The build agent **MUST NOT modify a fixture to make a test pass.**

All timestamps are offsets from a single declared constant so the recency criteria are deterministic regardless of wall-clock time:

```
CORPUS_NOW = 1750000000   # epoch seconds; the corpus anchor. Every captured_at below is
                          # CORPUS_NOW minus a fixed offset, so the corpus never depends on
                          # wall-clock time. The newest record (id 2) sits at CORPUS_NOW - 7200,
                          # and that — not CORPUS_NOW — is R6's decay target.
```

**`fixtures/day_memories.json`** — 14 records, ids 1–14, exactly these facts:

| id | source_type | captured_at | category | location | content |
|---|---|---|---|---|---|
| 1 | text | `CORPUS_NOW - 9*86400` | home | Flat | text: "Bike lock combination is 3812" |
| 2 | text | `CORPUS_NOW - 7200` | home | Flat | text: "Changed the bike lock combination to 7590" |
| 3 | text | `CORPUS_NOW - 18000` | food | Harbour Road | text: "Pastel de nata at the bakery on Harbour Road, 2.40"; price 2.40 |
| 4 | text | `CORPUS_NOW - 108000` | food | Harbour Road | text: "Soup and bread at the canteen, 11.00"; price 11.00 |
| 5 | text | `CORPUS_NOW - 100800` | food | Old Town | text: "Set lunch at the fish grill in the Old Town, 21.00"; price 21.00 |
| 6 | text | `CORPUS_NOW - 21600` | errands | Flat | text: "Umbrella stand by the front door is broken" |
| 7 | text | `CORPUS_NOW - 25200` | work | Studio | text: "Moved the Thursday review to the following Monday" |
| 8 | voice | `CORPUS_NOW - 14400` | errands | Tram stop | text (transcript): "Left the spare charger in the grey bag at the tram stop"; audio_ref "note_one.wav" |
| 9 | voice | `CORPUS_NOW - 93600` | home | Flat | text (transcript): "The window latch in the back room sticks and needs oil"; audio_ref "note_two.wav" |
| 10 | photo | `CORPUS_NOW - 18000` | food | Harbour Road | image_ref "red_circle.png" |
| 11 | photo | `CORPUS_NOW - 14400` | errands | Tram stop | image_ref "blue_square.png" |
| 12 | photo | `CORPUS_NOW - 25200` | work | Studio | image_ref "green_triangle.png" |
| 13 | text | `CORPUS_NOW - 259200` | home | Flat | text: "Recycling is collected on Tuesday mornings" |
| 14 | text | `CORPUS_NOW - 180000` | travel | Ferry terminal | text: "The ferry to the island leaves at 07:15 on Saturdays" |

Deliberate instances planted in this corpus, one per demonstrated failure mode: **ids 1 + 2** are the contradicting-fact pair (CTX-B5); **id 6** is the lexical near-miss for a question about a lost umbrella (CTX-B4); **id 8** is the memory deleted by AC6 (CTX-B6); **id 13** is a memory no plausible test question is about; and **no record at all** is about vehicle maintenance, which is what makes AC7's unanswerable question unanswerable (CTX-B2).

**`fixtures/make_fixtures.py`** — a module (importable identifier; no hyphens anywhere in a fixture module name) that writes, deterministically and with no network:

- Three scene photos, 512×512, white background, one flat-coloured shape each, centred: **`red_circle.png`**, **`blue_square.png`**, **`green_triangle.png`**.
- Three views of one subject to teach, 512×512 on white, a flat **yellow five-pointed star**, differing only in size, position and rotation: **`taught_view_one.png`**, **`taught_view_two.png`** (taught), **`taught_view_held_out.png`** (never taught; used to test).
- The taught subject's own note, used by AC22 when the subject is written into the day store as a single dual-vector memory (id 15): **"The yellow star came from the market stall"**.
- Two 16 kHz mono PCM WAV files, ~1.5 s, a fixed tone: **`note_one.wav`**, **`note_two.wav`**. Their *content* is irrelevant: they exist so the audio→transcript→store path is exercised on a real file. The transcript text comes from the transcriber (R12, AC16).

**Transcriber seam (project hardening).** Transcription is reached through an injectable interface. The default suite injects a deterministic fake that returns the record's own transcript for the matching `audio_ref`; a `live`-marked criterion may run the real model against a recording the learner supplies. The course calls its speech model directly; this seam is added so the voice contract is testable without a synthesized human voice.

### 5.2 Given / When / Then

| # | Given | When | Then | Rule |
|---|---|---|---|---|
| **AC0** | a directory that does not yet exist | the store is initialized fresh, before anything else runs | it matches `StoreDescriptor`: the directory exists on disk; it declares space `text` size 768 cosine **and** space `image` size 512 cosine; and it declares payload indexes `category` (keyword) and `price` (float) | R1, R14 |
| **AC1** | the freshly-initialized, empty store | any question is asked in any lane | every lane returns zero hits, `has_confident_answer` is false, and no exception is raised | R2 |
| **AC2** | the empty store | all 14 fixture records are ingested | the store reports exactly **14** memories; reading back id 3 returns payload `category` "food", `price` 2.40, `location` "Harbour Road" and its exact text; ids 10–12 carry an `image` vector of length 512 and ids 1–9, 13, 14 carry a `text` vector of length 768 | R1 |
| **AC3** | the ingested store | asking *"where did I leave the spare charger"* | the top hit of the **voice_notes** lane is **id 8**, and its `confident` is true | R1 |
| **AC4** | the ingested store (14 memories) | the same 14 fixture records are ingested a second time | the store still reports exactly **14** memories, and each id still resolves to the same source record — the second ingest updated points, it did not duplicate them | R16 |
| **AC5** | the ingested store | asking *"somewhere to eat"* with the filter `category == "food"` AND `price < 15` | the text_notes lane returns exactly **{id 3, id 4}** in some order — id 5 is excluded by price, id 10 is excluded because it is a photo with no price, and every returned hit still carries a similarity score | R14 |
| **AC6** | the ingested store, and AC3's result | id 8 is deleted, then AC3's question is asked again | the store reports exactly **13** memories; **id 8 appears in no lane**; the voice_notes lane's new top hit is **id 9**; and every remaining hit's score is identical to its score before the deletion | R7, R9 |
| **AC7** | the ingested store | asking *"how do I change a tyre on a motorbike"* | `has_confident_answer` is **false**, and no hit in any lane has `confident: true` — the app returns no answer rather than the nearest one | R3 |
| **AC8** | the ingested store | any question is asked | the result matches `RecallResult`: three separate lanes, every hit naming its `space`, and **no** combined or cross-lane ordering exists anywhere in the returned object or in the CLI rendering; the `text` floor and the `image` floor are two distinct configured values | R4 |
| **AC9** | the ingested store, with the **text** floor set for this run to `(top text score for the question) + 0.01` | asking *"where did I leave the umbrella"* | id 6 is returned in the text_notes lane with `confident: false`; `has_confident_answer` is false; and under Ledger D9's default the hit is still present and flagged weaker (under D9 *suppress*, it is absent from the lane instead) | R3, R5 |
| **AC10** | the ingested store, recency ranking enabled with half-life 604800 s and weight 0.2 | asking *"what is the bike lock combination"* | the top text_notes hit is **id 2** (the newer combination), and its `ranking_score` exceeds id 1's | R6 |
| **AC11** | the same store and ranking | asking *"when does the ferry leave"* | the top text_notes hit is **id 14** — the **third-oldest** memory in the corpus, older than nine others — proving the recency bonus is bounded and cannot pull a fresher but less relevant memory above a clearly better meaning match | R6 |
| **AC12** | an object store holding only the three scene photos as labelled views ("a red circle", "a blue square", "a green triangle") | `taught_view_held_out.png` is shown to it | a nearest match is returned with a **wrong** label (one of the three shapes), and the verdict is **`unknown`** because its score is below the calibrated recognition threshold — nearest-neighbour always answers, the threshold is what makes it an answer | R3, R13 |
| **AC13** | the text encoder | the identical string is embedded once through the document path and once through the query path | the two vectors differ, and the build uses the query path for questions and the document path for stored text throughout (if the encoder chosen in D4 has no separate query form, the build records that fact and uses one path consistently for both) | R8 |
| **AC14** | the ingested store, written and flushed, with its handle closed and **the process exited** | a **new process** loads the store from the same directory and asks AC3's question | the store reports the same memory count and the top voice_notes hit is **id 8** with the same score, to within floating-point equality | R10 |
| **AC15** | an open store handle on a populated directory | the build's reset path is asked to remove that directory | it refuses (or closes the handle first) and no native crash occurs; after an explicit close, the same call removes the directory and a fresh initialization succeeds | R11 |
| **AC16** | `note_one.wav` on disk and the fake transcriber injected | id 8 is ingested | the stored searchable text equals the transcriber's returned string exactly; the stored record carries `audio_ref` "note_one.wav" and **no audio bytes**; and asking AC3's question afterwards reads the audio file **zero** times | R12 |
| **AC17** | the AC12 object store, after `taught_view_one.png` and `taught_view_two.png` are taught under the label "yellow star" | `taught_view_held_out.png` is shown again | the nearest match is one of the two taught views, `nearest_label` is "yellow star", the verdict is **`known`**, and the score is **strictly greater** than the score recorded in AC12 | R13 |
| **AC18** | the completed build, after the one-time model download | the full suite runs with outbound network blocked, excluding `live`-marked criteria | every criterion passes; the ingest and answer paths make **zero** outbound network calls; and no generative or remote model is referenced anywhere in the source | R15 |
| **AC19** | the ingested store | a second source is registered whose id range overlaps the first, and ingest is attempted | the allocator **raises**; no existing memory's payload has changed; the store's count is unchanged | R16 |
| **AC20** | the six fixture images (three scene photos, three views of the taught subject) | the held-out calibration procedure of R17 is run | it reports the highest non-match score and the lowest match score, the chosen threshold lies strictly between them, and the value plus the corpus it came from is written to a named file that the build reads its recognition threshold from | R17 |
| **AC21** *(`live` — inactive under the baseline; applies only if Ledger D7 is changed)* | a reachable Qdrant server and valid `QDRANT_URL`/`QDRANT_API_KEY` in the environment | the local store is synced | every local point is present on the server with the same id, vectors and payload, **and** AC3 and AC7 still pass with the network then blocked — the sync never became the read path | R15, D7 |
| **AC22** | the ingested store, into which the taught subject of AC17 is written as one memory carrying **both** an image vector (a taught view) and a text vector (the note "The yellow star came from the market stall") | that one memory is reached twice — once by showing `taught_view_held_out.png`, once by asking *"where did the yellow star come from"* | **both** routes return the **same single id**; that point carries both a 512-length `image` vector and a 768-length `text` vector; the two hits report different `space` values and their scores are never compared | R1, R4, R13 |

Every demonstrated failure mode appears in all four places: **CTX-B1**→R2/AC1, **B2**→R3/AC7+AC12, **B3**→R4/AC8, **B4**→R5/AC9 (fixture id 6), **B5**→R6/AC10+AC11 (fixture ids 1+2), **B6**→R7/AC6 (fixture id 8), **B7**→R8/AC13, **B8**→R9/AC6, **B9**→R10/AC14, **B10**→R11/AC15.

---

## 6. Standing Permissions (in force for the entire build)

**Always**
- Read this spec, `resolved-decisions.md`, and anything inside the build folder.
- Create, run and re-run the fixture generator, the store, the CLI, and the test suite.
- Install the pinned dependencies of §2, and download the local models on first run.
- Write the calibration record (R17) and the resolved-decision checklist.
- Report every acceptance criterion with cited evidence.

**Ask First** — each of these is a trade-off the course argued aloud, or a change that forces rework; none of them is the agent's call.
1. **Changing either embedding model, or any vector width.** Forces a full re-embed and re-ingest of every memory, and invalidates every calibrated floor. (Ledger D4; argued in Lessons 1, 3 and 4.)
2. **Enabling any sync, upload, or off-device transfer of memories.** Silently converts a privacy guarantee into a conditional one and no acceptance criterion catches it. (Ledger D7; argued in Lesson 1.)
3. **Deleting, wiping or re-creating a populated store.** Irreversible, and the course's own reset helper does exactly this — which is why it needs a human. (Lesson 3 argues that forgetting is valuable *and* that vector stores comfortably hold far more than this corpus.)
4. **Changing any confidence floor or the recognition threshold away from its calibrated value.** Directly moves the false-positive / false-negative balance the course spends a whole section calibrating. (Lesson 5; R17.)
5. **Changing the recency half-life or weight, or applying recency ranking to a lane that did not have it.** The clearest instance of a silent guarantee change: raise the weight and recency starts overruling meaning, with every acceptance criterion still green. (Lesson 5; R6.)
6. **Making any optional operation automatic** — e.g. re-ranking every query by default, auto-teaching a subject from a low-scoring match, or auto-pruning the store. No test catches this class of change.
7. **Changing the memory id scheme after any data exists.** Forces re-ingest. (Ledger D11.)
8. **Introducing an LLM, a remote model, or any network call into the ingest or answer path.** Excluded by §1 and R15; if a learner wants it, it is a scope change, not an implementation detail.

**Never**
- Never invent provenance: no citation to a lesson, parameter or behavior that is not in this file.
- Never return a below-floor hit as a confident answer, or a recognition verdict of `known` without a label — abstain instead.
- Never modify, delete or regenerate-with-different-facts a fixture in order to make a test pass.
- Never commit, print, or write to a repo file any credential — `QDRANT_API_KEY` included.
- Never store raw audio bytes or image bytes inside a memory record.
- Never compare, merge, or jointly scale a text score and an image score.

---

## 7. Test Plan & Self-Verification

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m fixtures.make_fixtures   # writes the images and audio of §5.1; deterministic, offline

python -m app.cli warmup           # one-time model download; the ONLY step that needs the network
python -m app.cli ingest --corpus fixtures/day_memories.json
python -m app.cli calibrate        # R17; writes the calibration record
python -m app.cli ask "where did I leave the spare charger"

pytest -q -m "not live"            # the completion run — this is what "done" means
pytest -q                          # includes AC21; requires a credential, and is NOT part of completion
```

The building agent **MUST** report results **per acceptance criterion (AC0–AC22)** with cited evidence: the pytest node id, the relevant lines of its output, and the file path of anything it wrote. A criterion reported as *"should pass"*, *"looks correct"*, or *"implemented"* without cited output is treated as **failed** — those phrasings mean it was not run. AC18's network assertion must cite how outbound traffic was actually blocked, not merely that no call was expected. AC21, when it is not run, is reported as `skipped (live, no credential)` — never as passed.

---

## Course Context Pack (embedded — agent-readable)

*Concepts, not code. Everything in CTX-A…CTX-C is durable; only CTX-D is perishable.*

### CTX-A. The pattern

**`capture → transcribe (audio only) → embed → store → retrieve → threshold → rank → answer`**, with a second entrance for recognition: `show a photo → embed → retrieve nearest → threshold → label or UNKNOWN`.

- **capture** — a memory arrives as text, as a still image, or as audio. It is a fact worth recalling, with a time attached.
- **transcribe** — audio has no meaning a text encoder can read, so speech becomes text on the device at ingest; what is remembered is the transcript, never the recording. After this step a voice memory is indistinguishable from a typed one, which is why a *spoken* question works with no new machinery.
- **embed** — an encoder turns the memory into a vector: a list of numbers whose position encodes meaning. Text and images use different encoders, so a memory can live in more than one space at once; an image encoder whose text and vision towers share a space is what lets words find pictures.
- **store** — vectors are written as points into an embedded store that organizes them into a navigable graph, so a lookup over a large corpus stays fast. The payload — the original words and the metadata — rides along on the point, so a hit is already an answer and needs no second lookup.
- **retrieve** — a question goes through the *same* encoder as the memories and the store returns the approximate nearest neighbours. Payload conditions are pushed **into** the query so similarity is only computed where they hold. Closeness of vectors **is** the similarity score.
- **threshold** — retrieval always returns its nearest point. The floor is what turns "nearest" into "an answer", and it is a property of the encoder, so each space needs its own.
- **rank** — similarity decides the order, with an exponential decay on capture time added as a bounded bonus so the newer of two contradicting memories wins without recency ever outranking meaning.
- **answer** — the memories themselves come back, per lane, with their scores and their metadata. No model composes anything; the whole loop runs with the model weights frozen, and what changes over time is only the memory.

**Why the pattern is worth taking away:** it gives an application a memory that grows without any training, runs where the data already is, answers with no connection, and keeps private data private — and it is the same loop whether the device is a computer, a wearable, a camera rig, or a robot. The device is incidental; the memory loop is the asset.

### CTX-B. Failure-mode catalog

**CTX-B1 — The store answers nothing before it holds anything.** *Symptom:* a well-formed question returns an empty result. *Cause:* retrieval can only rank what was written; an empty store has no neighbours. *Fix:* treat empty as a legitimate, non-error answer and make the empty state visible in the UI rather than an exception. *Enforced by R2, AC1.*

**CTX-B2 — Nearest-neighbour always answers, even when it should not.** *Symptom:* an unfamiliar photo is confidently labelled as the closest thing the store happens to hold; an off-topic question returns a top hit. *Cause:* similarity search is a ranking, not a classifier — it has no notion of "none of these". *Fix:* a decision threshold on the score, below which the verdict is UNKNOWN / no confident answer. The right value is found by scoring held-out matches against non-matches and placing the line in the gap between them. *Enforced by R3, AC7, AC12.*

**CTX-B3 — Scores from two encoders are not on the same scale.** *Symptom:* a photo hit at 0.30 and a note hit at 0.65 get ranked against each other, and the photo lane effectively disappears — or a shared cutoff silently drops one whole modality. *Cause:* each model's similarity distribution is its own; the numbers are not commensurable even though both are called "cosine similarity". *Fix:* one lane and one floor per named vector space; never a blended list, never a shared bar scale. *Enforced by R4, AC8.*

**CTX-B4 — Lexical near-misses ride to the top of a lane.** *Symptom:* a note about a park surfaces for a question about a parked bike; a note about an umbrella *stand* surfaces for a question about a lost umbrella. *Cause:* the embedding is dominated by a shared token or a nearby concept; within a small corpus that is enough to be the nearest. *Fix:* the floor again — the near-miss is allowed to appear, but marked as below-confidence and never presented as the answer. Seeing the near-misses is itself diagnostic: it tells you where the boundary of the corpus is. *Enforced by R5, AC9.*

**CTX-B5 — Meaning alone returns the stale fact.** *Symptom:* two memories carry the same kind of fact — a code, an address, a schedule — recorded weeks apart, and the older one wins because it happens to be phrased slightly closer to the question. *Cause:* similarity has no notion of time. *Fix:* a recency bonus with an exponential decay and a **bounded** weight, computed over a wider prefetch than the result count so a fresher candidate outside the top *k* can still surface. Bounded is the load-bearing word: unbounded recency turns the assistant into a reverse-chronological log. *Enforced by R6, AC10, AC11.*

**CTX-B6 — A deleted memory that still answers.** *Symptom:* a memory removed from the corpus keeps coming back. *Cause:* the point was removed from a source file but not from the store, or the store's index was not compacted after the delete. *Fix:* delete by point id in the store itself and compact; verify by re-running the query that used to return it, and watch the next-best result take its place while every other score stays put. *Enforced by R7, AC6.*

**CTX-B7 — The question was embedded as if it were a document.** *Symptom:* every score is mediocre and retrieval feels blunt, with no single thing obviously broken. *Cause:* the text encoder applies different task prefixes to documents and to queries; using the document path for a question puts it in a slightly different region of the space. *Fix:* use the encoder's query path for questions and its document path for stored text, always and everywhere. This is the quietest failure in the catalog — it never throws. *Enforced by R8, AC13.*

**CTX-B8 — Recall slows as memory grows.** *Symptom:* lookups that were sub-millisecond creep upward as the corpus grows by orders of magnitude. *Cause:* graph traversal grows with the number of vectors, while the fixed cost of embedding the question does not — so their ratio inverts as the store fills. *Fix:* expect sub-linear growth (the course's own measurements grow the lookup roughly 50× while the corpus grows 250×), keep the question-embedding cost in view as the other half of the answer's latency, and treat forgetting as ordinary maintenance rather than an exception. *Enforced by R9, AC6.*

**CTX-B9 — A memory that did not survive the power going out.** *Symptom:* memories written just before a crash or an unclean exit are gone on restart. *Cause:* the write reached the store's in-memory state but was never compacted and flushed to disk. *Fix:* compact and flush as part of the write operation, not as an afterthought, and prove it by closing the handle and reloading from the directory in a **new process** — the only test that actually exercises the disk path. *Enforced by R10, AC14.*

**CTX-B10 — Deleting the store directory under an open handle crashes natively.** *Symptom:* a reset that used to work produces a native-level crash rather than a Python exception, usually only on a re-run inside a live session. *Cause:* the open handle flushes when it is dropped; if its files are already gone, that flush fails inside a destructor where no exception can be raised cleanly. *Fix:* close every open handle first, then remove the directory — and make the reset path do this itself, so a re-run is as safe as a clean start. *Enforced by R11, AC15.*

**CTX-B11 — Id ranges that collide once two sources share a store.** *(Project hardening — this one is latent in the course's code, not demonstrated by it.)* *Symptom:* memories vanish silently after ingesting a second source; the count is lower than the sum of the parts. *Cause:* ids were hand-allocated per source as disjoint ranges, and two sources' ranges overlap; an upsert with an existing id overwrites rather than erroring. *Fix:* one allocator that owns every range in a store, and an ingest that raises on an overlap instead of writing. *Enforced by R16, AC19.*

### CTX-C. Decision background

*Reference only. Every live decision is a Decision Ledger row; this section is the durable background behind those rows.*

**CTX-C1 — On-device versus a server. → Ledger D7.** The argument the course makes for keeping memory on the device has four distinct legs, and they are not equally strong for every project: it works with no connection at all; it avoids a network round trip, which makes recall both faster and more *reliable*; private memories stay private with no cloud storage and no API in the path; and a frozen model plus a growing local memory needs no retraining to learn something new. Against that, the course is explicit that a device has less compute and less storage than a server, and that a server earns its place when memories must be **shared between devices** — which is why the embedded engine offers sync at all, and why local and cloud retrieval can be combined. The decision is not ideological; it turns on whether anything other than this device needs to read these memories.

**CTX-C2 — One store with named spaces, versus a store per purpose. → Ledger D8.** A point may carry several independently-named vectors, which is what makes one memory reachable two ways: show the device a photo and the image vector answers; type a question and the text vector answers; both return the same point. That is the argument for one store. The argument for more than one is lifecycle: taught subjects and captured days are written, re-taught and forgotten on completely different schedules, and separating them lets you wipe one without touching the other. Note what you cannot do either way — you cannot merge results across the two spaces (CTX-B3), so "one store" buys a shared handle and a shared flush, not a shared ranking.

**CTX-C3 — Marking a weak result versus hiding it. → Ledger D9.** Both behaviors exist in the course, in different operations: recall renders sub-threshold hits dimmed and still visible, while recognition rejects them outright as UNKNOWN. That is not an inconsistency — it reflects the surface. A dimmed row on a screen is honest; the same row read aloud by a device with no screen is an answer. Choose by what the output surface can express.

**CTX-C4 — How the threshold was found, and why its value does not travel.** The course calibrates on real data rather than guessing: it scores a held-out view of each known subject against that subject's taught views (the matches) and against every other subject and every unrelated scene photo (the non-matches), then reads the gap. In the course's own run — a set with 220 non-matches and 6 matches — the lowest match landed at **0.86** and the highest non-match at **0.74**, so the line went in the middle at **0.80**, and the instructor immediately adds that the right value depends on how much a false positive costs you relative to a false negative. The same reasoning produced the recall floors: **0.6** for the text lane and **0.23** for the photo lane, two very different numbers for the same idea, precisely because they come from two different models (CTX-B3). Carry the **procedure**; re-derive the numbers. → Ledger D4, and R17.

**CTX-C5 — Retrieval breadth, and why it is a lever rather than a Ledger row.** The materials set the result count several ways: the lesson that introduces querying narrates a **limit of 3** out loud; the shared search helper defaults to 4; the assistant fetches 10 text candidates before splitting them into per-modality lanes of 3; the photo lane is fetched at 1 in one place and at 3-then-sliced-to-1 in another; the recency re-rank prefetches 20 candidates and returns 3, and the final demo returns 1. None of those choices changes a box, an arrow, an owner or a guarantee — only how many rows appear — so they are body defaults, not decisions to put to a learner. This spec resolves the **per-lane result count to 3**, selecting it by the first branch of the lever rule: *the value the transcript narration states aloud in the lesson that introduces the concept*. The two widths that are genuinely separate parameters keep their own single-valued settings: **10** candidates fetched before the text lane is split by source type, and a **20**-candidate prefetch before recency re-scoring (the prefetch must exceed the result count or R6's fix cannot work). All three are **post-build levers** — tune them after the build; nothing needs re-ingesting.

**CTX-C6 — Latency, and why this spec sets no performance target.** The course's latency curve is replayed from numbers measured once on the instructor's own laptop across corpora from 1,000 to 250,000 vectors, against a fixed question-embedding cost; the lesson states plainly that different machines produce different numbers and only the *trend* should be expected to hold. Any absolute millisecond target in this spec would therefore be invented rather than course-derived, which is why §1 excludes performance tuning and there is no performance-targets section. What does transfer is the shape: sub-linear growth in lookup, a constant embedding cost, and the conclusion that forgetting is ordinary maintenance. → R9.

**CTX-C7 — Where the materials contradict themselves, and how each was resolved.**
- *Result counts:* resolved as a body default by the lever rule — see CTX-C5.
- *Two definitions of the recall function:* a shared helper exports one signature while the lesson that teaches it defines a second, differently-shaped one in the notebook that then shadows the import for the rest of the lesson. The lesson's own version is the one that runs. Neither is contract-participating; this spec defines recall by its output contract (§3 `RecallResult`) instead of by either signature.
- *Blended results versus lanes:* one unused draft slide describes results from all modalities "merged into one inbox ranked by score", while the shipped display code states it renders "side-by-side lanes, never one blended list" and deliberately suppresses the proportional score bar wherever a column would mix scales, because comparing a score from one model with a score from another "means nothing". The shipped code and its stated reasoning win; blending is carried as the warned-against anti-pattern (CTX-B3) rather than as an option, which is why there is no Ledger row offering it.
- *An undefined threshold constant:* the calibration cell defines one name for the recognition threshold and then refers to a second, differently-spelled name that nothing in the materials defines — so that cell raises a `NameError` as written; the intent is unambiguously the value defined on the line above. Carried here as the reason the threshold lives in exactly one named place, written by the calibration step (R17).
- *A field's type:* the price field is a float on every record but one, where it is an integer, while the store's index for it is declared as a float index. The §3 schema therefore types it as a number, not an integer.
- *Lesson titles and numbering:* the slide decks are built on an earlier six-lesson plan whose title cards and course map are off by one from the final videos, and one notebook's own title cell disagrees with the title its video, transcript and README use. Transcript numbering and titles are authoritative throughout — see CTX-E.

**CTX-C8 — The id scheme. → Ledger D11.** The materials allocate point ids as hand-picked disjoint ranges, one per source: a day's captures low, a bulk photo import at one base, taught views at another, an ad-hoc new memory at a third, a taught assistant memory at a fourth. It reads clearly and it survives the lessons only because the two sources whose ranges actually overlap are never loaded into the same store. Once they are — which is exactly what a single-store topology does — an upsert with a colliding id overwrites silently. The pattern to carry is "ids are owned by one allocator per store"; the hand-picked ranges are the part to leave behind.

**CTX-C9 — Two ways a subject gets taught.** Teaching writes example vectors with a shared label — two or more views, so an unseen view has more than one neighbour to be close to, and the score for a new view rises as views accumulate. Where those points *live* is Ledger D8's business; what they *are* is not a decision: a taught subject is example vectors plus a label, never a trained classifier, and the final assistant stores a taught subject as one point carrying both its image vector and the text vector of its own note, so it answers to a photo and to a question alike.

**CTX-C10 — Name map: this spec's terms ↔ the course's own terms.** *Provenance only — none of the right-hand names is binding on this build. It exists so a learner who watched the lessons can map what they saw on screen onto what is specified here; the names in bold on the left are the ones this spec uses.*

| This spec | The course's word for it | Note |
|---|---|---|
| **memory store** | *shard* — and the instructor also calls it a *collection* | In the materials it is literally a directory on disk; the lessons create one per purpose with names like `mem_shard`, `day_shard`, `object_shard`, `assistant_shard`. This spec names one store per Ledger row D8 and does not inherit those directory names. |
| **point** | *point* | Binding, in effect: id + named vectors + payload is the storage unit (R1, §3 `StoredPoint`). |
| **payload** | *payload* | The metadata and original words carried on the point. Binding (§3). |
| **named vector space** | *named vector* | The two the course declares — `text` and `image` — **are binding here** (§3, AC0): the schema, the lanes and the floors are all keyed on those two names. |
| **source_type** values `text` / `voice` / `photo` | same three values | Binding — the lane split and the schema's conditionals depend on them (§3). |
| **capture time** (`captured_at`) | *timestamp*, an epoch integer | Renamed here only to say what it means; the type and role are the course's. |
| **confidence floor** | *minimum score* / *threshold* / *cutoff* — used interchangeably | One idea, three words in the materials. |
| **teaching a subject** | *teach* / *taught views* / *label* | R13. |
| **forgetting** | *forget*, implemented as deleting points | R7. |
| **compact + flush** | *optimize* then *flush* | R10. Two operations, in that order. |

### CTX-D. Perishable assumptions

**The concepts in CTX-A, CTX-B and CTX-C are durable. Everything in this subsection is not — treat every name below as a search keyword against current documentation, never as a guaranteed import.** The materials' store library is **pre-1.0** (pinned at 0.7.2), which is precisely the era where type names, constructor shapes and module paths move between minor versions.

- **Store library surface, era-specific:** the package installs under a hyphenated distribution name and imports under an underscored module name; its types cover a store handle with create/load/close/query/update/optimize/flush operations, a config object holding one vector-parameter object per named space, a distance enum, a point type carrying id + named vectors + payload, a request object for queries, a nearest-query constructor that names which space to search, update operations for upserting points, creating a payload field index, and deleting points, a payload-schema-type enum, filter/condition/match/range types, a prefetch type, and a formula/expression/decay family for score re-ranking.
- **Embedding library surface:** separate text-embedding and image-embedding classes, each taking a model identifier; the text class exposes a *document* embed and a separate *query* embed (see CTX-B7).
- **Model identifiers:** the course's text model, the two CLIP towers, and the speech model are named in §2. They are provenance — what the course actually used — and they stay true; they are **not** a claim about what is current. Choosing a currently-recommended model is a gate-time judgment, not something this spec bakes in.
- **Pinned versions:** every version in §2 is the course's own pin. Reproduce them for a first build; float them deliberately and re-run the full suite, not casually.
- **Request-parameter compatibility:** these are *local embedding and ASR* models, not chat completions — there is no sampling-parameter surface (`temperature` and friends do not exist here), and the only runtime knobs are the execution provider and thread counts. If Ledger row D4 is changed to a hosted API, that changes: hosted embedding endpoints differ in whether they accept a dimensionality parameter, an input-type/task parameter (the document-versus-query distinction of CTX-B7 is often expressed as exactly such a parameter), and batch size limits — check those before assuming R8 is satisfied.
- **Model download:** the models are fetched once, keyless, on first use, then cached. Size and cache location are library- and version-specific.

### CTX-E. Provenance map

Lesson numbering and titles below are **the transcripts'** — the authoritative source. The slide decks carry an earlier six-lesson plan whose numbering is off by one, and one notebook's own title cell disagrees with its lesson's title; neither was used here. **Nothing in this spec requires access to the course platform, the videos, the notebooks, or the repository.**

| Lesson (transcript numbering) | What came from it |
|---|---|
| **Lesson 1 — Why Devices Need Memory** | CTX-A (the whole loop: note → vector → navigable graph → nearest neighbour → similarity score; the same idea extended to images by a two-tower encoder); CTX-A's threshold step; **CTX-C1** and **Ledger D7** (the on-device argument and the case for a server); the "frozen model, growing memory" framing behind R13; **R15**. |
| **Lesson 2 — Building the Device** | **Ledger D5** (no specific hardware is needed; the same code runs on a small board or a personal computer); the store-is-a-directory-in-one-process fact behind **R10**, **R11** and Ledger D10's invariant; **Ledger D1**'s framing that the goal is the memory, not any one device. |
| **Lesson 3 — Store, Find, and Forget Memories** | The store's shape: named vector spaces at their two widths with cosine distance, and the point = id + named vectors + payload (**R1**, §3, AC0); **R14** and AC5 (indexed fields, filter inside the query); cross-modal recall by embedding a text query into the image space; **CTX-B1/R2**, **CTX-B2** (the "always returns its closest photo" warning), **CTX-B6/R7** (forgetting, before-and-after), **CTX-B8/R9** and **CTX-C6** (the latency curve and what it does and does not transfer); **CTX-C5** (the narrated result limit that resolves the lever). |
| **Lesson 4 — Your On-Device Assistant** | **R12/AC16** (a voice note is stored as its transcript, not as audio; a spoken question travels the same text path); **CTX-B3/R4** and the two very different per-lane floors; **CTX-B4/R5** (the weak match that is shown but greyed out) and **CTX-C3**; the per-modality lane structure of §3's `RecallResult`; the add-a-memory-and-recall-it-immediately behavior behind **R1** and **AC3**. |
| **Lesson 5 — Teaching Your Assistant to See** | **R13/AC12/AC17** (teach from a few views, test on a held-out one, no retraining); **CTX-B2** in its sharpest form (the wrong confident label before teaching) and **CTX-C4/R17** (the calibration experiment and its numbers); **CTX-B5/R6/AC10/AC11** (two contradicting memories, exponential decay, half-life, bounded weight, wider prefetch); **CTX-B9/R10/AC14** (close, reload from disk, still answers); **Ledger D8** and **CTX-C9** (one point carrying both vectors, reachable by sight and by words); the closing claim that the whole thing answers with no LLM involved (**R15**). |
| *(referenced, not supplied)* | Lessons 2 and 5 both refer forward to a further lesson that runs the assistant on a personal machine, and the repository README names a cloud-sync appendix; **neither is present in the supplied materials.** Nothing in this spec depends on either — the sync option on Ledger D7 is marked as carrying no worked parameters for exactly this reason. |

---

## 8. Finish with a diagram

When the build is complete and §7's per-criterion evidence has been reported, close by drawing the **infra/structure diagram of this app**: the processes and files that exist on disk, the store directory and its named vector spaces, where each model is loaded and cached, the ingest path from a source file to a stored point, and the answer path from a question to a lane of hits — marking clearly which boxes ever touch the network (under the baseline: only the one-time model download) and which Ledger row owns each box. Present it, then end with the sentence:

**"This is the infra/structure diagram of this app"**

---

*Status: v1 · Course: Building On-Device AI Memory with Qdrant Edge (5 lessons, transcript numbering) · Learner project: `[project]` — defaults to Ledger row D1's day-memory assistant on the §5 fixture corpus until you substitute your own · Generated 2026-09-14 from the supplied notebook dump, transcripts and slide descriptions by spec-generation-guide.md @ `8e44ecba383841fd78b6fc157a331f94d0ab5f68`.*

***This is a living document.*** *When the building agent produces something you did not expect, the missing constraint belongs here — add it as a business rule with an acceptance criterion, or as a Decision Ledger row if it is a genuine choice, and re-run the build. Do not patch the code and leave the spec behind.*
