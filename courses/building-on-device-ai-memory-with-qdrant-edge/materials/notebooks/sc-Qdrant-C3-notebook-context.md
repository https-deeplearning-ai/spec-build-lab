# Notebook context: Building On-Device AI Memory with Qdrant Edge
Source: SC-Qdrant-C3-main/ (L3/Lesson3.ipynb, L4/Lesson4.ipynb, L5/Lesson5.ipynb, helper.py, requirements.txt, ro_shared_data/)
Instructor: Dylan Couzon

The course code, organized by lesson in the same order and with the same lesson titles as the
transcripts in `../transcripts/` and the slide descriptions in `../slides/`. Each notebook lesson
gives a short overview, the lesson's dependencies (packages, helper functions, data read, files
written), and then every notebook cell in order. The shared helper module and the data files the
notebooks read follow once, after the lessons, so the whole course runs from this one file.

## How to read this file

- **Lesson titles come from the videos and transcripts**, not from the notebook headings. The
  notebooks are numbered L3 to L5 to match the course; Lessons 1 and 2 are video only and have no
  notebook, so they appear below with a note, one section per lesson.
- **Cells are numbered by position in the .ipynb**, starting at 0, and reproduced verbatim.
  Markdown cells sit inside a ```markdown fence so the notebook's own `#` and `##` headings do
  not disturb this file's outline; code cells sit inside a ```python fence.
- **No cell outputs are shown**, because none are saved: all three notebooks are stored with
  empty `outputs` lists. (The course README says every package version is pinned "so the scores
  in the saved outputs reproduce", but the outputs are not in this copy of the repo. Where the
  transcript quotes a printed number, the lesson overview mentions it.)
- **helper.py appears once**, in the shared section, as the Lesson 5 copy. The root, L3 and L4
  copies are byte-identical to each other; the L5 copy is that same file plus six functions
  Lesson 5 uses. The shared section lists exactly what differs.
- **Data files appear once**, in the shared section: the two JSON memory files in full, the three
  small READMEs and notes in full, and a filename listing for the photo and audio folders.
  The `CREDITS.json` attribution files are named but not embedded.
- `from helper import *` is the first line of every notebook; the names it hands over are the
  `__all__` list at the top of helper.py. Each lesson's dependency list names the ones it uses.

---

## Course-wide environment

**Python.** 3.12 or newer. The notebooks' kernel metadata records Python 3.12.11; the README says
the course was built and validated on 3.14.6.

**Install.** One install at the repository root covers every lesson:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt jupyterlab
jupyter lab
```

**Models downloaded on first run** (no account or API key; offline after that):

| Model | Package | Used for | Vector size |
| --- | --- | --- | --- |
| `nomic-ai/nomic-embed-text-v1.5` | fastembed | text notes and text questions (`embed_text`, `embed_query`) | 768 |
| `Qdrant/clip-ViT-B-32-vision` | fastembed | photos (`embed_image`) | 512 |
| `Qdrant/clip-ViT-B-32-text` | fastembed | text descriptions searched against photos (`embed_query_clip`) | 512 |
| `whisper-base` | onnx-asr | voice notes and the spoken question in Lesson 4 (`transcribe`) | n/a |

**Memory layer.** `qdrant-edge-py` 0.7.2 (`import qdrant_edge`), an embedded engine with no server.
Each lesson creates one or more *shards*: directories on disk (`./mem_shard`, `./day_shard`,
`./object_shard`, `./assistant_shard`) that `fresh_start` / `new_shard` wipe and recreate at the
top of the lesson. The `.gitignore` excludes `**/*_shard/` and `**/my_photos/`.

**requirements.txt** (verbatim):

```
# python package requirements file

# Note to our Learners: Our courses are created at a specific point in time. The models and libraries used will naturally change over time.
# If you download and run the notebooks locally, you should create a Python virtual environment
# with the Python version matching the one used in the course and use this requirements.txt file to install the required Python packages.
# Due to the wide diversity of platforms and environments, DeepLearning does not explicitly support running locally. However, if you encounter
# issues, the course support channel is a good place to ask questions.

# Python 3.12 or newer. The course was built and validated on 3.14.6.
# Every version below is pinned to the one the notebooks were run with, so the
# scores printed in the saved outputs reproduce exactly.

# Memory layer
qdrant-edge-py==0.7.2

# Local text and image embeddings: Nomic and CLIP through FastEmbed. No
# account needed, and no network after the first model download.
fastembed==0.8.0

# On-device speech to text for the voice notes (ONNX Whisper)
onnx-asr==0.12.0

# FastEmbed and onnx-asr both run their models on these two. They decide the
# embedding numbers, so they are pinned alongside the models.
onnxruntime==1.27.0
tokenizers==0.23.1

# The upload button in Lesson 5. Ships its own JupyterLab extension, so it
# works in a container with no outbound network.
ipywidgets==8.1.8

# Visualization and data
matplotlib==3.11.0
numpy==2.5.1
Pillow==12.3.0

# Server client, for the optional cloud sync in the appendix
qdrant-client==1.18.0
```

---

## Lesson 1: Why Devices Need Memory

Video only (4:36). No notebook, code, or data files belong to this lesson. Transcript:
`../transcripts/sc-Qdrant-C3-L1-transcript.md`; slides: Lesson 1 section of
`../slides/sc-Qdrant-C3-slide-descriptions.md`.

---

## Lesson 2: Building the Device

Video only (2:32). No notebook, code, or data files belong to this lesson. Transcript:
`../transcripts/sc-Qdrant-C3-L2-transcript.md`.

---

## Lesson 3: Store, Find, and Forget Memories

Notebook: `SC-Qdrant-C3-main/L3/Lesson3.ipynb` (19 cells: 6 markdown, 13 code). Video 6:38.

### Overview

The first memory store, built from scratch. Section 1 creates an empty shard with two named
vector spaces (`text`, 768 dimensions, and `image`, 512 dimensions, both cosine) and queries it
to show that nothing comes back. Section 2 loads the 20 text notes from `memories.json`, embeds
them with Nomic, wraps each in a `Point` whose payload is the note's metadata (id, source_type,
category, location, timestamp, note, price), and upserts them; the same question now returns
the coffee place on 5th at a score of about 0.58. Section 3 creates keyword and float field
indexes on `category` and `price` and runs the question again with a `Filter` (category is
"food", price below 15). Section 4 stores the 165 bank photos through CLIP and retrieves "a red
bicycle" from a text description, for 185 memories in all. Section 5 deletes the top hit and
shows the before/after tables, then draws the latency curve; the curve replays numbers measured
on the instructor's machine (`LOOKUP_LATENCY` in helper.py, Apple M5 Pro, 1,000 to 250,000
vectors) rather than timing anything live.

Every Qdrant Edge call this lesson teaches (create, query, upsert, index, filter, delete) is
written out in the notebook; only embedding, loading and the display tables come from helper.py.

### Dependencies

**Imported in the notebook**

- `helper` (everything in `__all__`)
- `qdrant_edge`: `Distance`, `EdgeConfig`, `EdgeShard`, `EdgeVectorParams`, `Query`,
  `QueryRequest`, `Point`, `UpdateOperation`, `PayloadSchemaType`, `FieldCondition`, `Filter`,
  `MatchValue`, `RangeFloat`
- `display` (the IPython builtin, used bare in cell 17)

**helper.py names used** (13): `embed_query`, `embed_query_clip`, `embed_text`, `fresh_start`,
`latency_curve`, `load_memories`, `memories_table`, `point_card`, `results_table`,
`show_photo_results`, `store_photos`, `text_search`, `vector_preview`

**Packages pulled in through those helpers**: fastembed (Nomic text model; CLIP vision and text
models), matplotlib (`latency_curve`), Pillow (thumbnails in `show_photo_results` and
`show_images`), IPython.display (HTML tables).

**Data read**

- `./ro_shared_data/memories.json`, filtered to `source_type == "text"` (20 of 42 records)
- `./ro_shared_data/bank/` (165 JPEGs, stored one point each with the filename as payload)

**Files written**: `./mem_shard/` (deleted and recreated by `fresh_start` at the top of the lesson).

### Notebook cells

#### Cell 0 (markdown)

```markdown
# L3. Store, Find, and Forget Memories

Store personal notes as vectors in **Qdrant Edge**, an embedded engine with no server and no network required
```

#### Cell 1 (markdown)

```markdown
## 1. Ask an empty shard

fresh_start just creates the directory where your your memory store created, we call that a shard
Then we configure Qdrant Edge and tell it which type of vectors we want to store and which distance metric we want to use to compare those vectors
then we simply create the shard
```

#### Cell 2 (code)

```python
from helper import *
from qdrant_edge import (Distance, EdgeConfig, EdgeShard,
                         EdgeVectorParams, Query, QueryRequest)

SHARD_DIR = fresh_start("./mem_shard")

config = EdgeConfig(
    vectors={
        "text": EdgeVectorParams(size=768, distance=Distance.Cosine),
        "image": EdgeVectorParams(size=512, distance=Distance.Cosine),
    }
)
shard = EdgeShard.create(SHARD_DIR, config)
print("Empty shard created at", SHARD_DIR)
```

#### Cell 3 (code)

```python
question = "a good place to eat or drink nearby"

question_vector = embed_query(question)

hits = shard.query(
    QueryRequest(
        query=Query.Nearest(question_vector, using="text"),
        limit=3,
        with_payload=True,
    )
)
results_table(hits, "Closest memories", query=question)
```

#### Cell 4 (markdown)

```markdown
## 2. Load, embed, and store the notes

The vector carries the meaning, the note itself rides along as payload.
```

#### Cell 5 (code)

```python
notes = load_memories(
    "./ro_shared_data/memories.json",
    source_type="text",
)
memories_table(notes[:6], f"First 6 of {len(notes)} text notes")
```

#### Cell 6 (code)

```python
vectors = embed_text([m["note"] for m in notes])

vector_preview(notes[0]["note"], vectors[0])
```

#### Cell 7 (code)

```python
from qdrant_edge import Point, UpdateOperation

points = [
    Point(id=m["id"], vector={"text": vector}, payload=m)
    for m, vector in zip(notes, vectors)
]
shard.update(UpdateOperation.upsert_points(points))
shard.optimize()

print("Stored", shard.info().points_count, "memories")
point_card(points[0], shown=0)
```

#### Cell 8 (code)

```python
question = "a good place to eat or drink nearby"

question_vector = embed_query(question)

hits = shard.query(
    QueryRequest(
        query=Query.Nearest(question_vector, using="text"),
        limit=3,
        with_payload=True,
    )
)
results_table(hits, "Closest memories", query=question)
```

#### Cell 9 (markdown)

```markdown
## 3. Recall with category and price filters

The same question, narrowed to what the payload says.
```

#### Cell 10 (code)

```python
from qdrant_edge import PayloadSchemaType

shard.update(UpdateOperation.create_field_index(
    "category", PayloadSchemaType.Keyword))
shard.update(UpdateOperation.create_field_index(
    "price", PayloadSchemaType.Float))

shard.optimize()
print("Indexed category and price")
```

#### Cell 11 (code)

```python
from qdrant_edge import (FieldCondition, Filter, MatchValue,
                         RangeFloat)

cheap_food = Filter(
    must=[
        FieldCondition(key="category", match=MatchValue(value="food")),
        FieldCondition(key="price", range=RangeFloat(lt=15)),
    ]
)
hits_filtered = text_search(shard, question, cheap_food)

results_table(hits_filtered, "Food under $15", query=question)
```

#### Cell 12 (markdown)

```markdown
## 4. Adding images

Cross-modal search always returns its closest photo, so treat the result as the nearest thing in the bank.
```

#### Cell 13 (code)

```python
store_photos(shard, "./ro_shared_data/bank")
```

#### Cell 14 (code)

```python
my_description = "a red bicycle"

description_vector = embed_query_clip(my_description)

photo_hits = shard.query(
    QueryRequest(
        query=Query.Nearest(description_vector, using="image"),
        limit=1,
        with_payload=True,
    )
)
show_photo_results(photo_hits, "./ro_shared_data/bank",
                  my_description)
```

#### Cell 15 (markdown)

```markdown
## 5. Forgetting as memory grows
```

#### Cell 16 (code)

```python
forgotten = hits[0]

shard.update(UpdateOperation.delete_points([forgotten.id]))
shard.optimize()

print(f"Forgot id {forgotten.id}: {forgotten.payload['note']}")
```

#### Cell 17 (code)

```python
hits_after = text_search(shard, question, limit=3)

display(results_table(hits, "Before", query=question))
results_table(hits_after, "After",
              caption="the other scores are unchanged")
```

#### Cell 18 (code)

```python
latency_curve()
```

---

## Lesson 4: Your On-Device Assistant

Notebook: `SC-Qdrant-C3-main/L4/Lesson4.ipynb` (19 cells: 7 markdown, 12 code). Video 4:58.

### Overview

One day of captures (17 photos, 20 text notes, 5 voice notes: 42 memories) goes into a single
shard and the notebook builds the recall over it. Section 1 loads `memories.json` and prints the
count by source type; section 2 shows the photos as a time-stamped strip, lists the notes, and
transcribes the five voice memos plus a spoken question (`question.wav`) on-device with Whisper,
so what gets stored for a voice note is its transcript, not the audio. Section 3 creates
`./day_shard` with `new_shard` and stores the text and voice notes through Nomic and the photos
through CLIP. Section 4 defines `recall` in the notebook: one question, searched in the text
lane (top 10, then split into voice and text) and the photo lane (top 1), displayed by
`memory_inbox` with separate cutoffs per lane (0.6 for text, 0.23 for photos) because the two
lanes use different embedding models; results under the cutoff are shown greyed out. Section 5
feeds the Whisper transcript of the spoken question through the same `recall`. Section 6 upserts
a new text memory (id 900, "Left the spare key with the neighbor in apartment 4B") and recalls
it immediately.

Note that the notebook's `recall` shadows the `recall` exported by helper.py; the notebook
version is the one that runs from cell 12 on.

### Dependencies

**Imported in the notebook**

- `helper` (everything in `__all__`)
- `IPython.display.Audio`
- `qdrant_edge`: `Point`, `UpdateOperation`
- `display` (the IPython builtin, used bare in cell 15)

**helper.py names used** (13): `day_notes`, `day_photos`, `day_summary`, `embed_text`,
`load_memories`, `memory_inbox`, `new_shard`, `photo_search`, `store_notes`,
`store_photo_memories`, `text_search`, `transcribe`, `transcribe_notes`

**Packages pulled in through those helpers**: fastembed (Nomic, CLIP), onnx-asr (`whisper-base`
via `transcribe`; `transcribe_notes` frees the model afterwards), Pillow (thumbnails),
IPython.display (HTML tables and the audio player).

**Data read**

- `./ro_shared_data/memories.json`, all 42 records (20 text, 17 photo, 5 voice)
- `./ro_shared_data/audio/`: the five memos named by each voice record's `audio_file`
  (`bike.wav`, `birthday.wav`, `coffee.wav`, `ramen.wav`, `standup.wav`) and `question.wav`
- `./ro_shared_data/images/`: the 17 scene photos named by each photo record's `file`

**Files written**: `./day_shard/` (recreated by `new_shard`).

### Notebook cells

#### Cell 0 (markdown)

```markdown
# L4. Your On-Device Assistant

A day of photos, voice notes, and text notes land in one `EdgeShard`: the kind of day a phone or a pair of smart glasses captures. You build the recall yourself, then ask it your own questions and add your own memories, all offline.
```

#### Cell 1 (markdown)

```markdown
## 1. Transcribe voice notes
```

#### Cell 2 (code)

```python
from helper import *
from IPython.display import Audio
memories = load_memories("./ro_shared_data/memories.json")
day_summary(memories)
```

#### Cell 3 (markdown)

```markdown
## 2. See the day at a glance
```

#### Cell 4 (code)

```python
day_photos(memories, "./ro_shared_data/images")
```

#### Cell 5 (code)

```python
day_notes(memories)
```

#### Cell 6 (code)

```python
spoken = transcribe("./ro_shared_data/audio/question.wav")
voice = transcribe_notes(memories, "./ro_shared_data/audio")

first = voice[0]
print("Transcript:", first["transcript"])
print(len(voice), "voice notes transcribed on-device")

Audio(f"./ro_shared_data/audio/{first['audio_file']}")
```

#### Cell 7 (markdown)

```markdown
## 3. Store the day
```

#### Cell 8 (code)

```python
shard = new_shard("./day_shard", text=768, image=512)
```

#### Cell 9 (code)

```python
texts = [m for m in memories if m["source_type"] in ("text", "voice")]
store_notes(shard, texts)
```

#### Cell 10 (code)

```python
photos = [m for m in memories if m["source_type"] == "photo"]
store_photo_memories(shard, photos, "./ro_shared_data/images")
```

#### Cell 11 (markdown)

```markdown
## 4. Recall your day
```

#### Cell 12 (code)

```python
def recall(question):
    text_hits = text_search(shard, question, limit=10)
    photo_hits = photo_search(shard, question, limit=1)
    return {
        "Photos": photo_hits,
        "Voice Notes": [h for h in text_hits
                        if h.payload["source_type"] == "voice"][:3],
        "Text Notes": [h for h in text_hits
                       if h.payload["source_type"] == "text"][:3],
    }
```

#### Cell 13 (code)

```python
my_question = "what was the ramen place downtown"

hits = recall(my_question)
memory_inbox(hits, "./ro_shared_data/images",
             min_text_score=0.6, min_photo_score=0.23)
```

#### Cell 14 (markdown)

```markdown
## 5. Ask by voice

The model that read the day's notes also read a question. `recall` takes that text the same way it takes anything you type, so a spoken question reaches the same three lanes. Text and photos use separate cutoffs because they come from different embedding models.
```

#### Cell 15 (code)

```python
display(Audio("./ro_shared_data/audio/question.wav"))
print("Heard:", spoken)

hits = recall(spoken)
memory_inbox(hits, "./ro_shared_data/images",
             min_text_score=0.6, min_photo_score=0.23)
```

#### Cell 16 (markdown)

```markdown
## 6. Add a memory and recall it
```

#### Cell 17 (code)

```python
from qdrant_edge import Point, UpdateOperation

my_note = "Left the spare key with the neighbor in apartment 4B"

note_vector = embed_text([my_note])[0]

my_memory = Point(
    id=900,
    vector={"text": note_vector},
    payload={"source_type": "text", "category": "home",
             "location": "Home", "note": my_note},
)
shard.update(UpdateOperation.upsert_points([my_memory]))
```

#### Cell 18 (code)

```python
my_question = "where did I leave the spare key"

hits = recall(my_question)
memory_inbox(hits, "./ro_shared_data/images",
             min_text_score=0.6, min_photo_score=0.23)
```

---

## Lesson 5: Teaching Your Assistant to See

Notebook: `SC-Qdrant-C3-main/L5/Lesson5.ipynb` (23 cells: 7 markdown, 16 code). Video 5:36.
The notebook's own title cell reads "L5: Learning Through Memory"; the video, the course README
and the transcript call the lesson "Teaching Your Assistant to See".

### Overview

Recognition by writing example vectors to memory, with no training, then the whole assistant in
one shard. Section 1 creates `./object_shard` (image vector only), defines `add_memory` and
`teach` in the notebook, and seeds three known objects from the bank (a bicycle, chess pieces, a
camera) at ids 0 to 2. Section 2 shows the bundled example (three rubber duck views), offers two
upload cards (teach photos, one held-out test photo) that fall back to the duck when nothing is
uploaded, recognizes the test photo before teaching (closest match is the bicycle), teaches the
two views under the label "rubber duck" at ids 100+, and recognizes again (the duck, at about
0.88). Section 3 calibrates a threshold: `threshold_calibration` scores every bundled object's
held-out view against its own taught views (positives) and against other objects and the 17
scene photos (negatives), and the lesson settles on 0.80. Section 4 creates `./assistant_shard`
with both vector spaces, loads today's 42 memories plus the 102 earlier-day notes from
`recent_days.json`, stores the 127 text/voice notes and 17 photos with `store_day`, adds the
taught duck as one point with both an image vector and a text vector (id 5000, note "Rubber duck
for the bath, from the toy shop on Elm Street"), flushes, and prints a receipt: 145 memories.
Section 5 asks "what is my gym locker code?" by meaning alone (the older code wins), then builds
a `freshness_ranking` (exponential decay on `timestamp`, seven-day half-life, weight 0.2 on top
of the similarity score) and re-asks through `recent_text_search`, a prefetch of 20 candidates
re-scored by the formula, so the current code wins. Section 6 closes and reloads the shard from
disk and answers four questions from both lanes at once (words and picture) with no LLM.

**Known issue in the notebook.** Cell 12 uses the name `RECOGNIZE_THRESHOLD` twice, but the cell
defines `THRESHOLD = 0.80` and no file in the repo defines `RECOGNIZE_THRESHOLD` (helper.py
does not export it). Run as written, that cell raises `NameError` unless the name is defined
first; the intent is clearly the `THRESHOLD` value on the line above.

### Dependencies

**Imported in the notebook**

- `helper` (everything in `__all__`, L5 copy)
- `qdrant_edge`: `EdgeShard`, `Point`, `UpdateOperation`

**Defined in the notebook**: `add_memory` (one point with the given vectors and payload) and
`teach` (embed several views, store them under one label, optimize and flush).

**helper.py names used** (22; * marks the six that exist only in the L5 copy):
`answers_table`, `embed_image`, `embed_text`, `freshness_ranking`*, `load_day_and_history`,
`memory_receipt`*, `new_shard`, `object_photos`, `photo_search`, `photo_uploader`,
`recent_text_search`*, `recognition_result`, `recognize`, `results_table`, `save_shard`*,
`seed_objects`, `show`, `show_example_object`*, `show_taught_photos`, `store_day`*,
`text_search`, `threshold_calibration`

**Packages pulled in through those helpers**: fastembed (Nomic, CLIP), matplotlib
(calibration chart), Pillow (thumbnails), IPython.display (HTML tables and the upload cards;
`photo_uploader` renders HTML/JS that PUTs files to the Jupyter server, which is why
requirements.txt pins ipywidgets and JupyterLab is the expected front end).
`qdrant_edge` names used inside the L5-only helpers: `DecayKind`, `Expression`, `Formula`,
`Prefetch`.

**Data read**

- `./ro_shared_data/bank/`: `bicycle.jpg`, `chess_set.jpg`, `camera.jpg` (the three seeds)
- `./ro_shared_data/objects/`: `rubberduck_1.jpg`, `rubberduck_2.jpg` to teach and
  `rubberduck_3.jpg` to test, by default; all 16 object photos in `threshold_calibration`
- `./ro_shared_data/images/`: the 17 scene photos, as today's photo memories and as negatives
  in `threshold_calibration`
- `./ro_shared_data/memories.json` (42 records) and `./ro_shared_data/recent_days.json`
  (102 records: 81 text, 21 voice) through `load_day_and_history`
- `./my_photos/teach/` and `./my_photos/test/`: the student's uploads, if any; emptied once per
  fresh kernel by `_reset_uploads_once`

**Files written**: `./object_shard/`, `./assistant_shard/` (recreated by `new_shard`; the
assistant shard is closed and reloaded from disk in cell 22), `./my_photos/` (upload folders).

### Notebook cells

#### Cell 0 (markdown)

```markdown
# L5: Learning Through Memory

The device learns something new by writing example vectors to memory: no retraining, no fine-tuning. Pick a subject, give it a name, and teach it yourself. Then everything you built lands in one assistant that answers questions about your day and recognizes what you taught it, offline.
```

#### Cell 1 (markdown)

```markdown
## 1. Set up object memory
```

#### Cell 2 (code)

```python
from helper import *
from qdrant_edge import EdgeShard, Point, UpdateOperation

object_shard = new_shard("./object_shard", image=512)
```

#### Cell 3 (code)

```python
def add_memory(shard, memory_id, vectors, payload):
    memory = Point(
        id=memory_id,
        vector=vectors,
        payload=payload,
    )
    shard.update(UpdateOperation.upsert_points([memory]))

def teach(shard, subject, view_paths, start_id):
    image_vectors = embed_image(view_paths)
    for i, (path, vector) in enumerate(zip(view_paths, image_vectors)):
        add_memory(
            shard,
            memory_id=start_id + i,
            vectors={"image": vector},
            payload={"label": subject, "file": path},
        )
    shard.optimize()
    shard.flush()
```

#### Cell 4 (code)

```python
seed_objects(object_shard)
```

#### Cell 5 (markdown)

```markdown
## 2. Test, teach, test again
```

#### Cell 6 (code)

```python
show_example_object()
```

#### Cell 7 (code)

```python
photo_uploader("teach")
photo_uploader("test")
```

#### Cell 8 (code)

```python
test_photo = object_photos("test")
top_match = recognize(object_shard, test_photo)
recognition_result(test_photo, top_match)
```

#### Cell 9 (code)

```python
SUBJECT = "rubber duck"
teach_photos = object_photos("teach")
teach(object_shard, SUBJECT, teach_photos, start_id=100)
show_taught_photos(teach_photos, SUBJECT)
```

#### Cell 10 (code)

```python
top_match = recognize(object_shard, test_photo)
recognition_result(test_photo, top_match)
```

#### Cell 11 (markdown)

```markdown
## 3. Calibrate recognition
```

#### Cell 12 (code)

```python
THRESHOLD = 0.80
threshold_calibration("./ro_shared_data/objects","./ro_shared_data/images",
    selected=RECOGNIZE_THRESHOLD, current=(SUBJECT, top_match.score))

top_match = recognize(object_shard, test_photo)
is_known = top_match.score >= RECOGNIZE_THRESHOLD
recognition_result(test_photo,top_match,is_known,threshold=THRESHOLD)
```

#### Cell 13 (markdown)

```markdown
## 4. Build the assistant's memory
```

#### Cell 14 (code)

```python
ASSISTANT_DIR = "./assistant_shard"
assistant_shard = new_shard(ASSISTANT_DIR, text=768, image=512)
```

#### Cell 15 (code)

```python
day, notes, photos = load_day_and_history()
store_day(assistant_shard, notes, photos)
```

#### Cell 16 (code)

```python
MY_NOTE = "Rubber duck for the bath, from the toy shop on Elm Street"

photo_vector = embed_image([teach_photos[0]])[0]
note_vector = embed_text([MY_NOTE])[0]

add_memory(
    assistant_shard, memory_id=5000,
    vectors={"image": photo_vector, "text": note_vector},
    payload={"label": SUBJECT,"file": teach_photos[0],"note": MY_NOTE,},
)
save_shard(assistant_shard)

memory_receipt(assistant_shard, SUBJECT)
```

#### Cell 17 (markdown)

```markdown
## 5. Prefer recent memories

Two memories contain a gym locker code. Meaning alone retrieves the older one first. Add freshness so the assistant prefers the current code.
```

#### Cell 18 (code)

```python
question = "what is my gym locker code?"

by_meaning = text_search(assistant_shard, question, limit=3)

results_table(
    by_meaning, "Meaning only",
    query=question, when=True, price=False,
)
```

#### Cell 19 (code)

```python
LATEST_TIME = max(m["timestamp"] for m in day)
HALF_LIFE = 7 * 24 * 60 * 60  # A memory is half as fresh a week later
FRESHNESS_WEIGHT = 0.2  # Maximum boost to the similarity score

ranking = freshness_ranking(LATEST_TIME, HALF_LIFE, FRESHNESS_WEIGHT)
```

#### Cell 20 (code)

```python
by_freshness = recent_text_search(assistant_shard, question, ranking)

results_table(
    by_freshness, "Meaning + freshness",
    query=question, when=True, price=False,
)
```

#### Cell 21 (markdown)

```markdown
## 6. Ask your assistant
```

#### Cell 22 (code)

```python
assistant_shard.close()
assistant_shard = EdgeShard.load(ASSISTANT_DIR)

questions = ["what did I get at the toy shop?",
             "show me the bakery",
             "where did I have brunch",
             "what did the bike chain cost"]
answers = []
for question in questions:
    words = recent_text_search(assistant_shard, question, ranking, limit=1)[0]
    picture = photo_search(assistant_shard, question, limit=1)[0]
    answers.append((question, words, picture))
answers_table(answers, "./ro_shared_data/images")
```

---

## Shared: helper.py

Four copies exist in the repo: `helper.py` at the root, `L3/helper.py`, `L4/helper.py` and
`L5/helper.py`. The root, L3 and L4 copies are byte-identical (MD5 `c97ab0e4e48c7a7a70a178965f93b625`,
1,323 lines). The L5 copy (MD5 `095c404e0f02969acbfbc94b37d32b75`, 1,414 lines) is that same file
with additions and nothing removed, so it is the one reproduced here. What the L3 and L4 copies
lack, relative to the text below:

- six functions: `show_example_object`, `store_day`, `save_shard`, `memory_receipt`,
  `freshness_ranking`, `recent_text_search`
- the `qdrant_edge` imports those functions need: `DecayKind`, `Expression`, `Formula`, `Prefetch`
- the six names in `__all__`

Lessons 3 and 4 do not call any of the six, so either copy runs those notebooks. The module's
own docstring states the split the course follows: each Qdrant call is written out in the
notebook of the lesson that teaches it, and the repeat lives in helper.py. The four functions
`cloud_client`, `cloud_points`, `push_note` and `fetch_snapshot` belong to the cloud-sync
appendix notebook, which is not in this copy of the repo (see the appendix at the end of this
file); they need `qdrant-client` and the `QDRANT_URL` / `QDRANT_API_KEY` environment variables.

`SC-Qdrant-C3-main/L5/helper.py` (verbatim):

```python
"""Helper functions for the course notebooks.

Plumbing for the lessons: the on-device embedding models, speech-to-text for
the voice notes, the result tables and charts the lessons print, and the stores
and searches the lessons repeat. Each Qdrant call is written out in the
notebook of the lesson that teaches it; after that, the repeat lives here.
"""
import gc
import json
import math
import os
import shutil
import socket
from collections import Counter
from functools import lru_cache
from pathlib import Path

import matplotlib.pyplot as plt
from qdrant_edge import DecayKind, Distance, EdgeConfig, EdgeShard
from qdrant_edge import EdgeVectorParams, Expression, Formula
from qdrant_edge import Point, Prefetch, Query, QueryRequest, ScrollRequest
from qdrant_edge import UpdateOperation


# The lessons open with `from helper import *`; this is what that hands them.
__all__ = [
    "answers_table", "cloud_client", "cloud_points", "day_notes",
    "day_photos", "day_summary", "embed_image", "embed_query",
    "embed_query_clip", "embed_text", "fetch_snapshot", "file_size",
    "fresh_start", "freshness_ranking", "latency_curve",
    "load_day_and_history",
    "load_image", "load_memories", "memories_table", "memory_inbox",
    "memory_receipt",
    "new_shard", "object_photos", "photo_search", "photo_uploader",
    "point_card", "push_note", "recall", "receipt_table",
    "recent_text_search",
    "recognition_result", "recognize", "results_table", "save_shard",
    "seed_objects", "show", "show_example_object", "show_images",
    "show_photo_results", "show_taught_photos",
    "store_day", "store_notes", "store_photo_memories", "store_photos",
    "text_search", "threshold_calibration", "transcribe",
    "transcribe_notes", "vector_preview"
]


# Embedding models: Nomic for text, CLIP for images --------------------
NOMIC_MODEL = "nomic-ai/nomic-embed-text-v1.5"
NOMIC_DIM = 768


@lru_cache(maxsize=1)
def _text_model():
    from fastembed import TextEmbedding
    return TextEmbedding(NOMIC_MODEL)


def embed_text(texts):
    """Embed documents for storage. Returns list[list[float]] (one per input)."""
    return [v.tolist() for v in _text_model().embed(list(texts))]


def embed_query(text):
    """Embed a single query string.

    Nomic uses different task prefixes for documents and queries; FastEmbed's
    `query_embed` applies the query prefix so retrieval scores line up.
    """
    return next(_text_model().query_embed([text])).tolist()


# CLIP: one shared text/image space, for cross-modal recall in L3 and later.
# Nomic and CLIP scores sit on different scales, so photos live in their own
# named vector and a text query is embedded twice, once per space.
CLIP_VISION_MODEL = "Qdrant/clip-ViT-B-32-vision"
CLIP_TEXT_MODEL = "Qdrant/clip-ViT-B-32-text"
CLIP_DIM = 512


@lru_cache(maxsize=1)
def _clip_vision():
    from fastembed import ImageEmbedding
    return ImageEmbedding(CLIP_VISION_MODEL)


@lru_cache(maxsize=1)
def _clip_text():
    from fastembed import TextEmbedding
    return TextEmbedding(CLIP_TEXT_MODEL)


def embed_image(paths):
    """Embed image files with CLIP's vision encoder. Returns list[list[float]]."""
    return [v.tolist() for v in _clip_vision().embed(list(paths))]


def load_image(url_or_path):
    """Return a local image path, fetching http(s) URLs to a temp JPEG first.

    A path to a file already on disk passes straight through, so the upload
    button and a filename typed by hand both land here.
    """
    if not str(url_or_path).startswith(("http://", "https://")):
        return url_or_path
    import io
    import os
    import tempfile
    import urllib.parse
    import urllib.request
    from PIL import Image

    # A search-results link points at a viewer page and carries the real
    # image URL in its imgurl parameter.
    query = urllib.parse.parse_qs(urllib.parse.urlparse(url_or_path).query)
    url = query.get("imgurl", [url_or_path])[0]

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
        image = Image.open(io.BytesIO(data)).convert("RGB")
    except OSError:
        raise ValueError(
            f"No image came back from this link:\n  {url[:90]}\n"
            "Right-click the image itself and copy the image address (it "
            "ends in .jpg or .png), or use the upload button instead."
        ) from None
    fd, path = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)
    image.save(path, "JPEG")
    return path


def embed_query_clip(text):
    """Embed a text query into CLIP's space, to search the image vector."""
    return next(_clip_text().query_embed([text])).tolist()


EXAMPLE_OBJECT = "./ro_shared_data/objects/rubberduck_"
TEACH_DIR = "./my_photos/teach"
TEST_DIR = "./my_photos/test"
IMAGE_TYPES = (".jpg", ".jpeg", ".png", ".webp")
_UPLOADS_RESET = False


def _uploaded(folder):
    """Photos sitting in an upload folder, oldest first."""
    path = Path(folder)
    if not path.is_dir():
        return []
    files = [f for f in path.iterdir() if f.suffix.lower() in IMAGE_TYPES]
    return sorted(files, key=lambda f: f.stat().st_mtime)


def _server_root():
    """The Jupyter server's root directory (JUPYTER_SERVER_ROOT, or home)."""
    return Path(os.environ.get("JUPYTER_SERVER_ROOT", str(Path.home()))).resolve()


def _relative_to_server_root(folder):
    """Path to `folder`, relative to the server root, forward-slashed.

    The browser-side upload script talks to the Jupyter Contents API, whose
    paths are relative to the server root -- not to this kernel's cwd.
    """
    return Path(folder).resolve().relative_to(_server_root()).as_posix()


def _upload_box(folder, heading, hint, box_id):
    """One labelled upload card that PUTs files into `folder` via HTML/JS.

    Built on plain HTML output and the Jupyter Contents REST API rather than
    ipywidgets' `FileUpload`: some proxied JupyterLab setups fail to load the
    ipywidgets front-end JS, so the widget silently falls back to a text repr
    instead of rendering. Plain HTML/JS output always renders -- it needs no
    extension -- and the Contents API is core Jupyter server functionality,
    so this works wherever the notebook itself loads.
    """
    Path(folder).mkdir(parents=True, exist_ok=True)
    rel_path = _relative_to_server_root(folder)
    existing = [f.name for f in _uploaded(folder)]

    return f"""
<div style="display:inline-block;vertical-align:top;width:330px;
            font-family:inherit;border:1px solid #999;border-radius:6px;
            padding:10px;margin:4px 8px 4px 0;box-sizing:border-box;">
  <b>{heading}</b><br><small>{hint}</small><br><br>
  <input type="file" id="{box_id}" accept="image/*" multiple>
  <div id="{box_id}-status" style="margin-top:6px;">
    {_upload_status(folder)}
  </div>
</div>
<script>
(function() {{
  const input = document.getElementById("{box_id}");
  const status = document.getElementById("{box_id}-status");
  const relPath = {rel_path!r};
  const uploaded = {existing!r};

  function baseUrl() {{
    const cfgEl = document.getElementById('jupyter-config-data');
    if (cfgEl) {{
      try {{
        const b = JSON.parse(cfgEl.textContent).baseUrl;
        if (b) return b.endsWith('/') ? b : b + '/';
      }} catch (e) {{}}
    }}
    const m = location.pathname.match(/^(.*?)(?:\\/lab|\\/notebooks|\\/tree)\\//);
    return m ? m[1] + '/' : '/';
  }}
  function xsrfToken() {{
    const m = document.cookie.match(/(?:^|; )_xsrf=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : '';
  }}
  function readAsBase64(file) {{
    return new Promise((resolve, reject) => {{
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result.split(',')[1]);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    }});
  }}
  function render() {{
    status.innerHTML = uploaded.length
      ? '<small>' + uploaded.length + ' ready: ' + uploaded.join(', ') + '</small>'
      : '<small>Nothing uploaded yet.</small>';
  }}

  input.addEventListener('change', async () => {{
    const files = Array.from(input.files);
    status.innerHTML = '<small>Uploading\\u2026</small>';
    for (const file of files) {{
      const content = await readAsBase64(file);
      const path = relPath.split('/').map(encodeURIComponent).join('/')
                   + '/' + encodeURIComponent(file.name);
      try {{
        const resp = await fetch(baseUrl() + 'api/contents/' + path, {{
          method: 'PUT',
          headers: {{'Content-Type': 'application/json',
                     'X-XSRFToken': xsrfToken()}},
          body: JSON.stringify({{type: 'file', format: 'base64', content: content}}),
        }});
        if (resp.ok) {{
          uploaded.push(file.name);
        }} else {{
          console.error('upload failed:', file.name, resp.status, await resp.text());
        }}
      }} catch (e) {{
        console.error('upload error:', file.name, e);
      }}
    }}
    input.value = '';
    render();
  }});
}})();
</script>
"""


def _upload_status(folder):
    files = _uploaded(folder)
    if not files:
        return "<small>Nothing uploaded yet.</small>"
    return f"<small>{len(files)} ready: {', '.join(f.name for f in files)}</small>"


def _reset_uploads_once():
    """Start each fresh kernel with empty upload folders.

    The flag keeps a same-kernel re-run of the first cell from deleting photos
    the student just uploaded. Restarting the kernel reloads this module,
    resets the flag, and clears the previous session's files.
    """
    global _UPLOADS_RESET
    if _UPLOADS_RESET:
        return
    for folder in (TEACH_DIR, TEST_DIR):
        path = Path(folder)
        if path.is_dir():
            for uploaded in path.iterdir():
                if uploaded.is_file() or uploaded.is_symlink():
                    uploaded.unlink()
    _UPLOADS_RESET = True


def photo_uploader(kind):
    """Show the upload button for teaching photos or the held-out test photo."""
    from IPython.display import display, HTML

    _reset_uploads_once()
    if kind == "teach":
        box = _upload_box(
            TEACH_DIR, "Teach with these",
            "Two or more photos of one object, from different angles or "
            "in different places.", "upload-teach")
    elif kind == "test":
        box = _upload_box(
            TEST_DIR, "Test with this one",
            "One more photo of the same object. Keep it out of the teaching "
            "photos.", "upload-test")
    else:
        raise ValueError('kind must be "teach" or "test"')
    display(HTML(box))


def object_photos(kind):
    """Read teaching photos or the held-out photo, with a bundled fallback."""
    _reset_uploads_once()
    teach = [str(f) for f in _uploaded(TEACH_DIR)]
    test = [str(f) for f in _uploaded(TEST_DIR)]
    if kind == "teach":
        if not teach:
            print("Bundled example: 2 rubber duck photos")
            return [EXAMPLE_OBJECT + f"{i}.jpg" for i in (1, 2)]
        if len(teach) < 2:
            raise ValueError(
                f"Found {len(teach)} teaching photo(s). Upload two or more, "
                "or leave this empty for the bundled example."
            )
        print(f"{len(teach)} photos to teach with")
        return teach
    if kind == "test":
        if not test:
            print("Bundled example: 1 held-out rubber duck photo")
            return EXAMPLE_OBJECT + "3.jpg"
        if len(test) != 1:
            raise ValueError(
                f"Found {len(test)} test photos. Upload exactly one, or leave "
                "this empty for the bundled example."
            )
        print("1 photo held back to test")
        return test[0]
    raise ValueError('kind must be "teach" or "test"')


def show_example_object():
    """Show the bundled rubber duck: two photos to teach with, one held out.

    This runs before the uploaders so the shape of the job is on screen
    first: a few views of one object, plus one more photo of it kept aside
    to test with. Upload your own object or run straight through with the
    duck; `object_photos` falls back to these files either way.
    """
    return show_images(
        [EXAMPLE_OBJECT + f"{i}.jpg" for i in (1, 2, 3)],
        captions=["teach with this", "teach with this",
                  "held out, to test with"],
        title='Bundled example: "rubber duck"',
    )


# Shard setup, the offline guard, and benchmark filler -----------------
# How much of a write to show back. Small: the recording frame is tall,
# not endless, and the point is what landed, not all of it.
PREVIEW_ROWS = 4
PREVIEW_PHOTOS = 6


def load_memories(path, source_type=None):
    """Read a memories JSON file, optionally keeping one source type."""
    memories = json.load(open(path))
    if source_type:
        memories = [m for m in memories if m["source_type"] == source_type]
    return memories


MODEL_NAME = {"text": "Nomic", "image": "CLIP"}


def new_shard(directory, text=None, image=None):
    """Create an empty shard on a clean directory, one named vector space
    per width given: `new_shard("./day_shard", text=768, image=512)`.

    Lesson 3 writes this out in full, an `EdgeConfig` holding one
    `EdgeVectorParams` per named vector and then `EdgeShard.create`. After
    that first time the repeat lives here. The widths stay arguments, so a
    lesson still says on screen which spaces it has and how wide they are.
    """
    sizes = {name: size for name, size in
             (("text", text), ("image", image)) if size}
    config = EdgeConfig(vectors={
        name: EdgeVectorParams(size=size, distance=Distance.Cosine)
        for name, size in sizes.items()
    })
    shard = EdgeShard.create(fresh_start(directory), config)
    print("Memory bank ready:", ", ".join(
        f"{name} {size}-d ({MODEL_NAME[name]})"
        for name, size in sizes.items()))
    return shard


def store_notes(shard, notes, preview=True):
    """Embed text and voice notes with Nomic and store one point per note.

    The write this wraps is taught in Lesson 3: embed the note, build a
    Point with the note as payload, upsert. A voice note embeds its
    transcript.
    """
    vectors = embed_text([m.get("note") or m["transcript"] for m in notes])
    shard.update(UpdateOperation.upsert_points([
        Point(id=m["id"], vector={"text": v}, payload=m)
        for m, v in zip(notes, vectors)
    ]))
    if preview:
        show(memories_table(notes[:PREVIEW_ROWS],
                            f"Stored {len(notes)} notes"))
    else:
        print(f"Stored {len(notes)} notes")


def store_photos(shard, folder, start_id=1000, preview=True):
    """Embed a folder of photos with CLIP and store them in the image vector."""
    photos = sorted(Path(folder).glob("*.jpg"))
    vectors = embed_image([str(p) for p in photos])
    shard.update(UpdateOperation.upsert_points([
        Point(id=start_id + i, vector={"image": v},
              payload={"file": p.name, "source_type": "photo"})
        for i, (p, v) in enumerate(zip(photos, vectors))
    ]))
    shard.optimize()
    if preview:
        show(show_images([str(p) for p in photos[:PREVIEW_PHOTOS]],
                         captions=[p.name for p in photos[:PREVIEW_PHOTOS]],
                         per_row=6,
                         title=f"Stored {len(photos)} photos · "
                               f"{shard.info().points_count} memories"))
    else:
        print(f"Stored {len(photos)} photos · "
              f"{shard.info().points_count} memories")


def store_photo_memories(shard, photos, folder, preview=True):
    """Embed photo memories with CLIP and store one point per photo."""
    vectors = embed_image([f"{folder}/{m['file']}" for m in photos])
    shard.update(UpdateOperation.upsert_points([
        Point(id=m["id"], vector={"image": v}, payload=m)
        for m, v in zip(photos, vectors)
    ]))
    shard.optimize()
    if preview:
        show(day_photos(photos[:PREVIEW_PHOTOS], folder,
                        f"Stored {len(photos)} photos · "
                        f"{shard.info().points_count} memories"))
    else:
        print(f"Stored {len(photos)} photos · "
              f"{shard.info().points_count} memories")


def store_day(shard, notes, photos, folder="./ro_shared_data/images"):
    """Load a day's notes and photos into one shard, notes then photos.

    Both writes are taught in Lessons 3 and 4; this is the repeat, so the
    lesson that builds the assistant only shows the memory it adds itself.
    """
    store_notes(shard, notes, preview=False)
    store_photo_memories(shard, photos, folder, preview=False)


def save_shard(shard):
    """Compact the shard and write it to disk.

    `optimize` builds the index over what was just written, `flush` puts it
    on disk, so a taught memory survives the device losing power.
    """
    shard.optimize()
    shard.flush()


def memory_receipt(shard, subject):
    """Confirm what the assistant now holds: the new memory, and the total."""
    return receipt_table([
        ("taught", f"{subject}: photo + note"),
        ("total", f"{shard.info().points_count} memories"),
    ], title="Assistant memory ready")


def text_search(shard, query, query_filter=None, limit=4):
    """Embed a query with Nomic and return the nearest text memories.

    Lesson 3 teaches both halves in the open: the raw nearest query, then
    `query_filter` narrowing it.
    """
    return shard.query(QueryRequest(
        query=Query.Nearest(embed_query(query), using="text"),
        filter=query_filter,
        limit=limit,
        with_payload=True,
    ))


def photo_search(shard, description, limit=1):
    """Embed a description with CLIP and return the nearest photos.

    The raw cross-modal call is taught in Lesson 3.
    """
    return shard.query(QueryRequest(
        query=Query.Nearest(embed_query_clip(description), using="image"),
        limit=limit,
        with_payload=True,
    ))


def freshness_ranking(latest_time, half_life, weight):
    """Build a ranking formula: similarity plus a bonus for recent memories.

    `Expression.Decay` turns a memory's `timestamp` into a freshness score
    between 0 and 1: 1 at `latest_time`, half of that `half_life` seconds
    earlier, fading from there. `weight` is the most that freshness can add
    to the similarity score, so meaning still leads and recency breaks ties.
    Memories with no timestamp are treated as current rather than dropped.
    """
    freshness = Expression.Decay(
        DecayKind.Exp,
        Expression.Variable("timestamp"),
        target=Expression.Constant(latest_time),
        midpoint=0.5,
        scale=half_life,
    )
    return Formula(
        Expression.Sum([
            Expression.Variable("$score"),
            Expression.Mult([Expression.Constant(weight), freshness]),
        ]),
        defaults={"timestamp": latest_time},
    )


def recent_text_search(shard, question, ranking, limit=3):
    """Search text memories by meaning, then re-rank with `ranking`.

    Two steps in one request: the prefetch pulls a wider set of candidates
    by meaning, and the formula from `freshness_ranking` rescores just those
    and keeps the top `limit`.
    """
    return shard.query(QueryRequest(
        limit=limit,
        prefetches=[Prefetch(
            limit=20,
            query=Query.Nearest(embed_query(question), using="text"),
        )],
        query=ranking,
        with_payload=True,
    ))


def recall(shard, question):
    """One question, two lanes: text memories by Nomic, photos by CLIP.

    Lesson 4 builds this in the open; later lessons import it. Extra text
    hits are fetched so one lane cannot crowd out the other.
    """
    text_hits = text_search(shard, question, limit=10)
    photo_hits = photo_search(shard, question, limit=3)
    return {
        "Photos": [h for h in photo_hits
                   if h.payload.get("source_type") == "photo"][:1],
        "Voice Notes": [h for h in text_hits
                        if h.payload.get("source_type") == "voice"][:3],
        "Text Notes": [h for h in text_hits
                       if h.payload.get("source_type") == "text"][:3],
    }


def recognize(shard, photo):
    """Return the closest stored photo.

    Nearest search always returns a match. The notebook applies the decision
    threshold separately.
    """
    top_match = shard.query(QueryRequest(
        query=Query.Nearest(embed_image([photo])[0], using="image"),
        limit=1,
        with_payload=True,
    ))[0]
    return top_match


def seed_objects(shard, folder="./ro_shared_data/bank"):
    """Store three known objects and show them, one photo each at ids 0-2.

    Writes exactly what Lesson 5's `teach` writes: the photo's CLIP vector
    with the label as payload, flushed to disk so a taught memory survives
    a power cut.
    """
    seeds = {"a bicycle": "bicycle.jpg",
             "chess pieces": "chess_set.jpg",
             "a camera": "camera.jpg"}
    paths = [f"{folder}/{f}" for f in seeds.values()]
    vectors = embed_image(paths)
    shard.update(UpdateOperation.upsert_points([
        Point(id=i, vector={"image": v},
              payload={"label": label, "file": p})
        for i, (label, p, v) in enumerate(zip(seeds, paths, vectors))
    ]))
    shard.optimize()
    shard.flush()
    show(show_images(paths, captions=list(seeds)))


def load_day_and_history(folder="./ro_shared_data"):
    """The assistant's full memory: today's captures plus the earlier days.

    Returns today's memories, text and voice notes from all days, and today's
    photos.
    """
    day = load_memories(f"{folder}/memories.json")
    history = load_memories(f"{folder}/recent_days.json")
    notes = [m for m in day + history
             if m["source_type"] in ("text", "voice")]
    photos = [m for m in day if m["source_type"] == "photo"]
    return day, notes, photos


def cloud_client(collection, text=768, image=512):
    """Connect to the cluster in QDRANT_URL / QDRANT_API_KEY, collection ready.

    Pasting credentials is how a student opts in, so there is no second
    switch to forget: returns a ready qdrant_client.QdrantClient with the
    collection created, or None when either variable is empty. A collection
    that already exists is left alone and None comes back, because the
    course never deletes one. None means every memory stays on the device,
    and the calling cell says so.

    The server's vectors_config is the twin of the `EdgeConfig` Lesson 3
    writes out, so it lives here rather than repeating on screen.
    """
    import os
    if not (os.getenv("QDRANT_URL") and os.getenv("QDRANT_API_KEY")):
        return None
    from qdrant_client import QdrantClient, models
    client = QdrantClient(url=os.environ["QDRANT_URL"],
                          api_key=os.environ["QDRANT_API_KEY"])
    if client.collection_exists(collection):
        print(f"{collection} already exists on the cluster.",
              "Delete it there first, or rename the collection here.")
        return None
    client.create_collection(collection, vectors_config={
        "text": models.VectorParams(size=text,
                                    distance=models.Distance.COSINE),
        "image": models.VectorParams(size=image,
                                     distance=models.Distance.COSINE),
    })
    return client


def cloud_points(shard, limit=1000):
    """Every point in a shard, in the shape a Qdrant server takes.

    Same ids, same vectors, same payloads: the format does not change on
    the way up. Reading them back is the `ScrollRequest` the appendix
    shows in the open one cell earlier.
    """
    from qdrant_client import models
    records, _ = shard.scroll(ScrollRequest(limit=limit, with_payload=True,
                                            with_vector=True))
    return [models.PointStruct(id=r.id, vector=r.vector, payload=r.payload)
            for r in records]


def push_note(client, collection, point_id, note):
    """Store one text note straight onto the cluster, as another device would.

    Used where the write belongs to some other device in the fleet. A write
    the student makes themselves stays in the notebook.
    """
    from qdrant_client import models
    client.upsert(collection, points=[models.PointStruct(
        id=point_id,
        vector={"text": embed_text([note])[0]},
        payload={"source_type": "text", "note": note},
    )])


def fetch_snapshot(collection, dest, manifest=None):
    """Download a shard snapshot from the cluster in QDRANT_URL to a file.

    With a manifest (from `EdgeShard.snapshot_manifest`), asks the server
    for a partial snapshot holding only what this shard is missing.
    """
    import os
    import urllib.request
    base_url = os.environ["QDRANT_URL"]
    headers = {"api-key": os.getenv("QDRANT_API_KEY") or ""}
    if manifest is None:
        url = f"{base_url}/collections/{collection}/shards/0/snapshot"
        req = urllib.request.Request(url, headers=headers)
    else:
        url = (f"{base_url}/collections/{collection}"
               "/shards/0/snapshot/partial/create")
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(
            url, data=json.dumps(manifest).encode(),
            headers=headers, method="POST")
    with urllib.request.urlopen(req) as response, open(dest, "wb") as f:
        f.write(response.read())
    return dest


def file_size(path):
    """A downloaded snapshot's size, in whichever unit reads better."""
    import os
    kb = os.path.getsize(path) / 1024
    return f"{kb / 1024:.1f} MB" if kb >= 1024 else f"{kb:.0f} KB"


def fresh_start(directory):
    """Delete any previous run's shard directory and recreate it empty.

    A shard the notebook still has bound holds its files open, and Edge flushes
    when that object is dropped. Deleting the files first makes the flush fail
    inside a destructor, which surfaces as a Rust panic rather than a Python
    error. So close any shard the notebook still holds before removing
    anything: that makes re-running a setup cell in a live kernel safe,
    instead of only working on a clean top-to-bottom run.

    The notebook's own namespace is `__main__`, whatever the call depth, so
    this works whether a lesson calls it directly or `new_shard` does.

    Only a directory that already holds a shard can have one open on it, so
    the sweep is skipped for a directory that does not exist yet. Without
    that guard, opening a second shard closes the first, which is exactly
    what a lesson holding two shards at once needs not to happen.
    """
    import sys
    if any(Path(directory).glob("*")):
        notebook = vars(sys.modules.get("__main__", None)) or {}
        for value in list(notebook.values()):
            if isinstance(value, EdgeShard):
                try:
                    value.close()
                except Exception:
                    pass
    gc.collect()
    shutil.rmtree(directory, ignore_errors=True)
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory


# The views the lessons print ------------------------------------------
QDRANT_RED = "#DC244C"
INK = "#28324D"
MUTED = "#6B7280"
LINE = "#E5E7EB"
FONT = "font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
FIG_W = 8.0        # recording frame is 8 wide by 9 high

MODALITY_COLOR = {"photo": QDRANT_RED, "voice": "#8547FF", "text": INK}
MODALITY_EMOJI = {"photo": "📷", "voice": "🎙️", "text": "📝"}


def show(view):
    """Put a view on screen from inside a helper, mid-cell."""
    from IPython.display import display
    display(view)


def _html(markup):
    from IPython.display import HTML
    return HTML(markup)


def _esc(value):
    import html
    return html.escape(str(value))


def _score_cell(score, peak):
    """A score with a proportional bar behind it, still selectable as text.

    Pass `peak=None` where the column mixes score scales: a bar would invite
    a comparison between a CLIP score and a Nomic one, which means nothing.
    """
    pct = max(0.0, min(1.0, score / peak)) * 100 if peak else 0
    return (f'<td style="text-align:right;font-variant-numeric:tabular-nums;'
            f'font-weight:700;color:{QDRANT_RED};'
            f'background:linear-gradient(to left,rgba(220,36,76,.14) {pct:.0f}%,'
            f'transparent {pct:.0f}%)">{score:.3f}</td>')


def _table(headers, rows, title=None, caption=None, widths=None, above=""):
    """Render a table as HTML. `rows` holds ready-made <td> strings.

    `widths` is one CSS width per column. Without it the browser sizes every
    column by its content, which lets a three-character Price column sit on
    top of Category and squeezes the memory itself into what is left. The
    memory is what the reader came to read, so it gets most of the width.
    """
    cols = ("<colgroup>"
            + "".join(f'<col style="width:{w}">' for w in widths)
            + "</colgroup>") if widths else ""
    layout = "table-layout:fixed;" if widths else ""
    head = "".join(
        f'<th style="text-align:left;padding:6px 10px;font-size:12px;'
        f'letter-spacing:.04em;text-transform:uppercase;color:{MUTED};'
        f'border-bottom:2px solid {QDRANT_RED}">{_esc(h)}</th>'
        for h in headers)
    body = "".join(
        f'<tr style="background:{"#FFFFFF" if i % 2 else "#FAFAFB"}">{r}</tr>'
        for i, r in enumerate(rows))
    parts = [f'<div style="{FONT};max-width:760px">']
    if title:
        parts.append(f'<div style="font-weight:800;font-size:15px;color:{INK};'
                     f'margin-bottom:6px">{_esc(title)}</div>')
    parts.append(above)
    parts.append(f'<table style="border-collapse:collapse;width:100%;'
                 f'{layout}font-size:13.5px;color:{INK}">{cols}'
                 f'<thead><tr>{head}</tr></thead>'
                 f'<tbody>{body}</tbody></table>')
    if caption:
        parts.append(f'<div style="font-size:12px;color:{MUTED};'
                     f'margin-top:6px">{_esc(caption)}</div>')
    parts.append("</div>")
    return "".join(parts)


def _cell(value, align="left", color=INK, weight=400, size=13.5,
          nowrap=False):
    return (f'<td style="padding:6px 10px;text-align:{align};color:{color};'
            f'font-weight:{weight};font-size:{size}px;'
            f'{"white-space:nowrap;" if nowrap else ""}'
            f'border-bottom:1px solid {LINE}">{_esc(value)}</td>')


def _memory_text(payload):
    """The words of a memory: its note, its transcript, or its filename."""
    return payload.get("note") or payload.get("transcript") or payload.get("file", "")


def _price(payload):
    return f"${payload['price']:.0f}" if payload.get("price") is not None else "-"


def _has_price(payloads):
    """Whether the price column is worth a column at all."""
    return any(p.get("price") is not None for p in payloads)


def _result_row(hit, peak, price=True, when=False):
    """One table row for a search hit: score, category, price, the memory."""
    p = hit.payload
    return (_score_cell(hit.score, peak)
            + _cell(p.get("category", "-"), color=MUTED)
            + (_cell(_price(p), align="right", color=MUTED) if price else "")
            + (_cell(_hhmm(p["timestamp"], "%b %d") if p.get("timestamp")
                     else "-", color=MUTED, nowrap=True) if when else "")
            + _cell(_memory_text(p)))


def results_table(hits, title=None, caption=None, query=None,
                  when=False, price=None):
    """Show search hits as a table: score, category, price, and the memory.

    `query` puts the question above the answers, where a reader looks for it.
    An empty result renders as the same view with nothing in it, so asking
    before and after storing reads as one picture with a row count.
    `when` adds the memory's date, for the lessons that rank by it.
    `price` defaults to showing the column when a memory carries one.
    """
    asked = _query_block(query) if query else ""
    if not hits:
        return _html(
            f'<div style="{FONT};max-width:760px">'
            f'<div style="font-weight:800;font-size:15px;color:{INK};'
            f'margin-bottom:6px">{_esc(title or "No memories found")}</div>'
            + asked
            + f'<div style="border:1px dashed {LINE};border-radius:8px;'
            f'padding:18px;text-align:center;color:{MUTED};font-size:13.5px">'
            f'Nothing stored yet.</div>'
            + (f'<div style="font-size:12px;color:{MUTED};margin-top:6px">'
               f'{_esc(caption)}</div>' if caption else '') + '</div>')
    peak = max((h.score for h in hits), default=1.0)
    if price is None:
        price = _has_price([h.payload for h in hits])
    rows = [_result_row(h, peak, price=price, when=when) for h in hits]
    headers = (["Score", "Category"] + (["Price"] if price else [])
               + (["When"] if when else []) + ["Memory"])
    widths = {(True, True): ("10%", "12%", "9%", "10%", "59%"),
              (True, False): ("10%", "13%", "9%", "68%"),
              (False, True): ("10%", "13%", "11%", "66%"),
              (False, False): ("10%", "14%", "76%")}[(price, when)]
    return _html(_table(headers, rows, title, caption, widths, above=asked))


def memories_table(memories, title=None):
    """Show stored memories, which carry no score: category, price, words."""
    price = _has_price(memories)
    rows = [_cell(m.get("category", "-"), color=MUTED)
            + (_cell(_price(m), align="right", color=MUTED) if price else "")
            + _cell(_memory_text(m)) for m in memories]
    headers = ["Category"] + (["Price"] if price else []) + ["Memory"]
    widths = ("14%", "9%", "77%") if price else ("15%", "85%")
    return _html(_table(headers, rows, title, widths=widths))


def receipt_table(rows, title="Restart receipt"):
    """Render a list of (label, value) pairs as a two-column table."""
    cells = [_cell(label, color=MUTED)
             + _cell(value, weight=700) for label, value in rows]
    return _html(_table(["", ""], cells, title))


def _thumb_data_uri(path, size=120):
    """Return a base64 data URI for a small thumbnail of an image file."""
    import base64
    import io
    from PIL import Image
    img = Image.open(path).convert("RGB")
    img.thumbnail((size, size))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def show_photo_results(hits, image_dir, query):
    """Show the photo a description retrieved, large, with its score.

    Only the closest match is shown: the search always returns something, and
    a big single answer says that more clearly than a row of runners-up.
    """
    hero = hits[0]
    uri = _thumb_data_uri(Path(image_dir) / hero.payload["file"], size=420)
    return _html(
        f'<div style="{FONT};max-width:460px">'
        f'<div style="font-size:12px;color:{MUTED};text-transform:uppercase;'
        f'letter-spacing:.04em">closest photo</div>'
        f'<div style="font-size:17px;font-weight:700;color:{INK};'
        f'margin:2px 0 8px">"{_esc(query)}"</div>'
        f'<img src="{uri}" style="width:100%;border-radius:10px;display:block">'
        f'<div style="margin-top:8px;font-size:13.5px;color:{INK}">'
        f'{_esc(hero.payload["file"])} · similarity '
        f'<span style="color:{QDRANT_RED};font-weight:700">'
        f'{hero.score:.3f}</span></div></div>')


def _query_block(text):
    """The question, shown above its answers rather than captioned under them."""
    return (f'<div style="font-size:13.5px;color:{INK};background:#FAFAFB;'
            f'border-left:3px solid {QDRANT_RED};padding:8px 10px;'
            f'margin-bottom:10px">{_esc(text)}</div>')


def _cosine(a, b):
    """Cosine similarity between two embeddings, the score a search returns."""
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a))
                  * math.sqrt(sum(y * y for y in b)))


def _payload_value(key, value):
    """A payload value as stored, glossed where the raw number is unreadable.

    A timestamp is an epoch integer on disk and stays one here, with the time
    it stands for beside it: the point of the card is what was really stored.
    """
    if key == "timestamp" and isinstance(value, (int, float)):
        return f"{value}  ({_hhmm(value, '%b %d, %H:%M')})"
    return value


def vector_preview(text, vector, shown=8):
    """One memory beside the start of the vector it became.

    The caption names the vector and counts its dimensions, because those are two
    different things and the lesson leans on the difference: one note becomes
    one vector, and that vector is a list of coordinates.
    """
    numbers = ", ".join(f"{x:+.3f}" for x in vector[:shown])
    return _html(
        f'<div style="{FONT};max-width:760px">'
        f'<div style="font-size:13.5px;color:{INK};margin-bottom:6px">'
        f'"{_esc(text)}"</div>'
        f'<div style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;'
        f'font-size:12.5px;color:{QDRANT_RED};background:#FAFAFB;'
        f'border:1px solid {LINE};border-radius:8px;padding:10px">'
        f'[{numbers}, ...]</div>'
        f'<div style="font-size:12px;color:{MUTED};margin-top:6px">'
        f'{len(vector)} dimensions'
        f'</div></div>')


def point_card(record, vector_name="text", shown=6):
    """One point in full: its id, its vector, and its payload.

    Takes anything carrying `.id`, `.vector`, and `.payload`, so it renders a
    `Point` the lesson just built as readily as a record read back off disk.
    """
    vector = record.vector[vector_name]
    # shown=0 where the cell above already printed the vector in full:
    # the card is then about the point's shape, not its values twice.
    values = ", ".join(f"{x:+.3f}" for x in vector[:shown])
    rows = [_cell(k, color=MUTED, nowrap=True) + _cell(_payload_value(k, v))
            for k, v in record.payload.items()]
    return _html(
        f'<div style="{FONT};max-width:760px">'
        f'<div style="font-weight:800;font-size:15px;color:{INK}">'
        f'Point {_esc(record.id)}</div>'
        f'<div style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;'
        f'font-size:12.5px;color:{QDRANT_RED};background:#FAFAFB;'
        f'border:1px solid {LINE};border-radius:8px;padding:10px;'
        f'margin:8px 0">{_esc(vector_name)}: '
        f'{f"[{values}, ...] " if shown else ""}'
        f'<span style="color:{MUTED}">{len(vector)} dimensions</span></div>'
        + _table(["Field", "Value"], rows,
                  widths=("20%", "80%")) + '</div>')


def _hhmm(ts, fmt="%H:%M"):
    from datetime import datetime, timezone
    return datetime.fromtimestamp(ts, timezone.utc).strftime(fmt)


def day_summary(memories):
    """One line: how many captures the day holds, by source type."""
    counts = Counter(m["source_type"] for m in memories)
    print(len(memories), "captures:",
          ", ".join(f"{v} {k}" for k, v in sorted(counts.items())))


def day_photos(memories, image_dir, title=None):
    """A wrapping strip of the day's photos, each stamped with its time."""
    photos = sorted((m for m in memories if m.get("file")),
                    key=lambda m: m["timestamp"])
    cards = "".join(
        f'<figure style="margin:0;width:104px">'
        f'<img src="{_thumb_data_uri(Path(image_dir) / m["file"], 200)}" '
        f'style="width:104px;height:104px;object-fit:cover;'
        f'border-radius:8px;display:block">'
        f'<figcaption style="font-size:11px;color:{MUTED};margin-top:3px">'
        f'{_hhmm(m["timestamp"])} · {_esc(m.get("store") or m.get("location", ""))}'
        f'</figcaption></figure>' for m in photos)
    return _html(
        f'<div style="{FONT};max-width:760px">'
        f'<div style="font-weight:800;font-size:15px;color:{INK};'
        f'margin-bottom:8px">📷 {_esc(title) if title else f"{len(photos)} photos, in time order"}</div>'
        f'<div style="display:flex;flex-wrap:wrap;gap:10px">{cards}</div></div>')


def day_notes(memories, limit=10):
    """The day's voice and text notes as a table: time, kind, and words.

    Shows the earliest `limit` notes, because a whole day of them runs off
    the bottom of the recording frame. Pass a bigger number for more, or
    `limit=None` for the lot. The title says how many there are either way.
    """
    notes = sorted((m for m in memories if not m.get("file")),
                   key=lambda m: m["timestamp"])
    total = len(notes)
    if limit is not None:
        notes = notes[:limit]
    # A couple of notes are stamped the evening before, so the date is shown
    # whenever the set spans more than one day.
    spans_days = len({_hhmm(m["timestamp"], "%j") for m in notes}) > 1
    fmt = "%b %d · %H:%M" if spans_days else "%H:%M"
    rows = []
    for m in notes:
        kind = m["source_type"]
        rows.append(_cell(_hhmm(m["timestamp"], fmt), color=MUTED,
                          nowrap=True)
                    + _cell(f'{MODALITY_EMOJI.get(kind, "")} {kind}',
                            color=MODALITY_COLOR.get(kind, INK), weight=600,
                            nowrap=True)
                    + _cell(_memory_text(m)))
    title = (f"{total} voice and text notes" if len(notes) == total
             else f"First {len(notes)} of {total} voice and text notes")
    return _html(_table(["Time", "Kind", "Note"], rows, title,
                        widths=("15%", "12%", "73%")))


def answers_table(answers, image_dir=None, title="Ask your assistant"):
    """Questions answered from both lanes at once: the words and the picture.

    `answers` is a list of (question, text_hit, photo_hit). The two scores sit
    in their own columns and carry no bars because they come from different
    retrieval lanes and do not compare. When both lanes land on the same
    point, the row says so: one memory, reached two ways.
    """
    rows = []
    for question, words, photo in answers:
        p = words.payload
        when = ("you taught this" if p.get("label")
                else _hhmm(p["timestamp"], "%b %d") if p.get("timestamp")
                else "-")
        same = photo is not None and photo.id == words.id
        file = photo.payload.get("file", "") if photo is not None else ""
        if file and "/" not in file and image_dir:
            file = str(Path(image_dir) / file)
        thumb = (f'<img src="{_thumb_data_uri(file, 180)}" style="width:88px;'
                 f'height:66px;object-fit:cover;border-radius:6px;display:block">'
                 if file else "")
        tag = ('<div style="font-size:11px;color:#009688;font-weight:700;'
               'white-space:nowrap">✅ same memory</div>' if same else "")
        photo_cell = (f'<td style="padding:6px 10px;border-bottom:1px solid '
                      f'{LINE}">{thumb}<div style="font-size:11px;'
                      f'color:{QDRANT_RED};font-weight:700;margin-top:3px">'
                      f'{photo.score:.3f}</div>{tag}</td>'
                      if photo is not None else _cell("-"))
        rows.append(_cell(question, weight=600)
                    + _cell(_memory_text(p))
                    + _score_cell(words.score, None)
                    + _cell(when, color=MUTED, nowrap=True)
                    + photo_cell)
    return _html(_table(["You asked", "It remembered", "Words", "When",
                         "Photo"], rows, title))


def memory_inbox(sections, image_dir, min_text_score=None,
                 min_photo_score=None):
    """One question's answers as side-by-side lanes, never one blended list.

    `sections` maps a lane title to a list of ScoredPoint, and each lane is a
    column ranked best first. Columns rather than a wrapping row because the
    lanes are the point: a reader compares down one lane and across three,
    and a wrap would put two lanes' cards on the same line. Every lane is
    drawn even when empty. Scores below their model's cutoff are dimmed.
    """
    def card(h):
        p = h.payload
        cutoff = min_photo_score if p.get("file") else min_text_score
        weak = cutoff is not None and h.score < cutoff
        ctx = " · ".join(x for x in [_hhmm(p["timestamp"]) if p.get("timestamp") else "",
                                     p.get("store"), p.get("location"),
                                     _price(p) if p.get("price") is not None else ""]
                         if x)
        if p.get("file"):
            uri = _thumb_data_uri(Path(image_dir) / p["file"], 260)
            body = (f'<img src="{uri}" style="width:100%;height:130px;'
                    f'object-fit:cover;border-radius:8px;display:block;'
                    f'margin-top:6px">')
        else:
            body = (f'<div style="font-size:13px;margin-top:6px;'
                    f'color:{INK}">{_esc(_memory_text(p))}</div>')
        tag = ('<span style="font-size:11px;color:#B0088A"> · weaker</span>'
               if weak else '')
        head = (f'<div style="font-size:11px;color:{MUTED}">{_esc(ctx)}</div>'
                if ctx else '')
        return (f'<div style="border:1px solid {LINE};border-radius:10px;'
                f'padding:9px;margin-bottom:8px;background:#fff;'
                f'{"opacity:.5" if weak else ""}">'
                f'{head}'
                f'{body}<div style="font-size:12.5px;margin-top:6px">'
                f'<span style="color:{QDRANT_RED};font-weight:700">'
                f'{h.score:.3f}</span>{tag}</div></div>')

    lanes = []
    for title, hits in sections.items():
        ranked = sorted(hits, key=lambda h: h.score, reverse=True)
        inner = ("".join(card(h) for h in ranked) if ranked else
                 f'<div style="font-size:13px;color:{MUTED};font-style:italic">'
                 f'No matches</div>')
        lanes.append(
            f'<div style="flex:1 1 0;min-width:0">'
            f'<div style="font-weight:700;font-size:13px;color:{INK};'
            f'border-bottom:2px solid {QDRANT_RED};margin-bottom:8px;'
            f'padding-bottom:3px">{_esc(title)}</div>{inner}</div>')
    return _html(
        f'<div style="{FONT};background:#F7F7F8;border-radius:12px;'
        f'padding:14px 16px;max-width:760px">'
        f'<div style="display:flex;gap:12px;align-items:flex-start">'
        f'{"".join(lanes)}</div></div>')


def threshold_calibration(object_dir, scene_dir, selected, current=None):
    """Calibrate image recognition on held-out and unrelated photos.

    Each bundled object keeps its last view out of the teaching set. Positive
    scores compare that held-out view with its own taught views. Negative
    scores compare held-out and scene photos with taught views of a different
    object. `current` may be `(label, score)` for the student's held-out photo.
    """
    groups = {}
    for path in sorted(Path(object_dir).glob("*.jpg")):
        groups.setdefault(path.stem.rsplit("_", 1)[0], []).append(path)

    taught = {label: views[:-1] for label, views in groups.items()}
    held_out = {label: views[-1] for label, views in groups.items()}
    scenes = sorted(Path(scene_dir).glob("*.jpg"))
    paths = [p for views in groups.values() for p in views] + scenes
    vectors = dict(zip(paths, embed_image([str(p) for p in paths])))

    same = []
    different = []
    for label, query in held_out.items():
        same.append(max(_cosine(vectors[query], vectors[p])
                        for p in taught[label]))
        different.extend(
            _cosine(vectors[query], vectors[p])
            for other, views in taught.items() if other != label
            for p in views)
    different.extend(
        _cosine(vectors[scene], vectors[p])
        for scene in scenes for views in taught.values() for p in views)

    same_min = min(same)
    different_max = max(different)
    fig, ax = plt.subplots(figsize=(FIG_W, 3.2))

    # Hundreds of negative dots hide the boundary that matters. Show their
    # tested range and hardest example instead, then keep each positive test.
    different_min = max(0.4, min(different))
    ax.hlines(0, different_min, different_max, color="#C8CEDD",
              linewidth=12, alpha=0.65)
    ax.scatter([different_max], [0], s=70, color="#8F98B2",
               edgecolors="white", linewidths=0.8, zorder=3)
    same_y = [0.96 + 0.04 * (i % 3) for i in range(len(same))]
    ax.scatter(same, same_y, s=58, color="#009688",
               edgecolors="white", linewidths=0.8, zorder=3)
    if different_max < same_min:
        ax.axvspan(different_max, same_min, color="#009688", alpha=0.09)
    ax.axvline(selected, color=QDRANT_RED, lw=2, ls="--")
    ax.annotate(f"highest {different_max:.3f}",
                xy=(different_max, 0), xytext=(-5, 14),
                textcoords="offset points", ha="right", color=MUTED,
                fontsize=9)
    ax.annotate(f"lowest {same_min:.3f}",
                xy=(same_min, 1), xytext=(5, -18),
                textcoords="offset points", ha="left", color="#00796B",
                fontsize=9)
    if current:
        ax.scatter([current[1]], [1.25], marker="*", s=170,
                   color=QDRANT_RED, edgecolors="white", linewidths=0.8,
                   zorder=4)
        ax.annotate(f"your view {current[1]:.3f}",
                    xy=(current[1], 1.25), xytext=(7, 0),
                    textcoords="offset points", va="center",
                    color=QDRANT_RED, fontsize=9, fontweight="bold")
    ax.set_xlim(0.4, 1.0)
    ax.set_ylim(-0.35, 1.50)
    ax.set_yticks([0, 1])
    ax.set_yticklabels([f"{len(different)} non-matches",
                        f"{len(same)} held-out matches"])
    ax.set_xlabel("similarity to nearest taught view")
    ax.set_title("Where should the threshold go?", loc="left")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    plt.show()


# Measured by .build/measure_latency.py on Apple M5 Pro, CPU only,
# Python 3.14.6, 300 queries per size, median reported. The lesson draws
# this curve rather than timing anything live: a 250,000-vector store does
# not fit in the course container, and a number timed on a shared sandbox
# moves on every re-run. Re-measure and paste if the model or Edge changes.
LOOKUP_LATENCY = [
    (1_000, 0.054),
    (5_000, 0.179),
    (25_000, 0.526),
    (100_000, 1.439),
    (250_000, 2.646),
]
QUERY_EMBED_MS = 5.50
MEASURED_ON = "Apple M5 Pro, CPU only, median of 300 queries per size"


def latency_curve(points=LOOKUP_LATENCY, embed_ms=QUERY_EMBED_MS):
    """Vector lookup time as the store grows, against the cost of embedding.

    Two local costs make up one answer. Embedding the question is a fixed
    price the encoder charges whatever the store holds, so it draws as a
    flat line. The lookup grows with the number of vectors, so it draws as
    a curve. Both stay on the device, which keeps this a breakdown of where
    the time goes and never a comparison against a server.
    """
    sizes = [n for n, _ in points]
    times = [ms for _, ms in points]
    fig, ax = plt.subplots(figsize=(FIG_W, 3.5))

    ax.axhline(embed_ms, color="#8F98B2", lw=2, ls="--")
    ax.annotate(f"query embedding · {embed_ms:.1f} ms",
                xy=(sizes[0], embed_ms), xytext=(0, 7),
                textcoords="offset points", color="#5C6480", fontsize=9.5)
    ax.plot(sizes, times, color=QDRANT_RED, lw=2.2, marker="o",
            markersize=6, markerfacecolor="white",
            markeredgecolor=QDRANT_RED, markeredgewidth=2, zorder=3)
    for n, ms in points:
        ax.annotate(f"{ms:.2f} ms", xy=(n, ms), xytext=(0, 11),
                    textcoords="offset points", ha="center", va="bottom",
                    color=QDRANT_RED, fontsize=9.5, fontweight="bold")

    ax.set_xscale("log")
    ax.set_xticks(sizes)
    ax.set_xticklabels([f"{n:,}" for n in sizes])
    ax.minorticks_off()
    ax.set_xlabel("memories (log scale)")
    ax.set_ylabel("milliseconds")
    ax.set_ylim(0, max(embed_ms, max(times)) * 1.35)
    ax.set_title("Vector lookup as memory grows", loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    # One provenance line, kept shorter than the figure: a wider line makes
    # matplotlib grow the whole figure past the recording frame.
    fig.subplots_adjust(bottom=0.24)
    fig.text(0.012, 0.03, MEASURED_ON, fontsize=9.5, color="#4E5366")
    plt.show()


def show_images(paths, captions=None, per_row=None, title=None, height=170):
    """A row of photos with a caption under each, sized to the video frame.

    Every photo gets the same box, whatever its shape, so a row reads as a row
    rather than a ragged stack. `contain` keeps the whole subject visible,
    which matters when the photo is the evidence.
    """
    paths = list(paths)
    # Fill the row with what there is, rather than leaving a hole for photos
    # that were never uploaded.
    per_row = per_row or min(len(paths), 4) or 1
    gap = 14
    cards = []
    for i, path in enumerate(paths):
        caption = captions[i] if captions and i < len(captions) else ""
        cards.append(
            f'<figure style="margin:0;flex:0 0 auto;'
            f'width:calc((100% - {gap * (per_row - 1)}px) / {per_row})">'
            f'<img src="{_thumb_data_uri(path, 460)}" style="width:100%;'
            f'height:{height}px;object-fit:contain;background:#FAFAFB;'
            f'border-radius:10px;display:block">'
            f'<figcaption style="font-size:12.5px;font-weight:600;color:{INK};'
            f'margin-top:6px;overflow:hidden;text-overflow:ellipsis;'
            f'white-space:nowrap">{_esc(caption)}</figcaption></figure>')
    head = (f'<div style="font-weight:800;font-size:15px;color:{INK};'
            f'margin-bottom:8px">📷 {_esc(title)}</div>' if title else '')
    return _html(f'<div style="{FONT};max-width:760px">{head}'
                 f'<div style="display:flex;flex-wrap:wrap;gap:{gap}px">'
                 f'{"".join(cards)}</div></div>')


def show_taught_photos(paths, subject):
    """Show the photos used to teach one subject."""
    return show_images(
        paths,
        title=f'Taught "{subject}" from {len(paths)} photos',
    )


def recognition_result(query_photo, top_match, is_known=None, image_dir=None,
                       threshold=None):
    """The photo you showed beside the closest memory, with the verdict.

    `is_known=None` shows the nearest memory without making a decision.
    Otherwise it says whether the score cleared the threshold. Both photos
    get the same box so the pair reads as a comparison.
    """
    stored = top_match.payload["file"]
    if image_dir:
        stored = str(Path(image_dir) / stored)
    label = top_match.payload.get("label", "UNKNOWN")
    if is_known is None:
        verdict, color, mark = f"Closest memory: {label}", INK, ""
    elif is_known:
        verdict, color, mark = label, "#009688", "✅"
    else:
        verdict, color, mark = "UNKNOWN", MUTED, "❓"

    def pane(path, caption):
        return (f'<figure style="margin:0;width:290px">'
                f'<img src="{_thumb_data_uri(path, 460)}" style="width:100%;'
                f'height:210px;object-fit:contain;background:#FAFAFB;'
                f'border-radius:10px;display:block">'
                f'<figcaption style="font-size:13px;color:{MUTED};'
                f'margin-top:6px">{_esc(caption)}</figcaption></figure>')

    detail = ""
    if is_known is not None and threshold is not None:
        if is_known:
            detail = (f'{top_match.score:.3f} clears the '
                      f'{threshold:.3f} threshold.')
        else:
            detail = (f'{top_match.score:.3f} is below the '
                      f'{threshold:.3f} threshold.')
        detail = (f'<div style="font-size:13px;color:{color};font-weight:650;'
                  f'margin:0 0 10px">{_esc(detail)}</div>')

    heading = f"{mark} " if mark else ""
    score_detail = (f" · closest: {_esc(label)} · similarity "
                    f"{top_match.score:.3f}" if is_known is False else
                    f" · similarity {top_match.score:.3f}")
    return _html(
        f'<div style="{FONT};max-width:620px">'
        f'<div style="font-size:19px;font-weight:800;color:{color};'
        f'margin-bottom:10px">{heading}{_esc(verdict)}'
        f'<span style="font-size:14px;font-weight:600;color:{MUTED}">'
        f'{score_detail}</span></div>{detail}'
        f'<div style="display:flex;gap:16px">'
        + pane(query_photo, "the photo you showed it")
        + pane(stored, f"closest memory: {label}")
        + '</div></div>')


# Speech to text for the voice notes -----------------------------------
WHISPER_MODEL = "whisper-base"


@lru_cache(maxsize=1)
def _asr_model():
    import onnx_asr
    return onnx_asr.load_model(WHISPER_MODEL, providers=["CPUExecutionProvider"])


def transcribe(audio_path):
    """Transcribe one audio file to text with a local Whisper model."""
    return _asr_model().recognize(audio_path).strip()


def transcribe_notes(memories, audio_dir):
    """Transcribe every voice note in place, then free the speech model.

    Releasing Whisper before the embedding models load keeps the notebook
    inside the 4 GB sandbox budget.
    """
    voice = [m for m in memories if m["source_type"] == "voice"]
    for m in voice:
        m["transcript"] = transcribe(f"{audio_dir}/{m['audio_file']}")
    _asr_model.cache_clear()
    return voice
```

---

## Shared: data (`ro_shared_data/`)

The notebooks read this folder as `./ro_shared_data/` relative to the lesson directory. On the
course platform the folder is copied into each lesson; in this repo it sits once at the root.

### `notes_on_shared_data.txt` (verbatim)

```
This directory can contain read only data shared by all the lessons.
This is a good location for shared images or datasets used by multiple lessons.

When the repo is deployed to the platform, the shared directory will be copied to a subdirectory in each lesson.
So, when referring to the shared data in your code, you should use
./ro_shared_data/shared_file
and not
../shared_data/shared_file.

Because each lesson is potentially in its own docker container, data written to files in the shared directory is not visible to other lessons.
If you wish, for example to write to a database in lesson1 and have it visible in lesson2, you will need to copy the data from the L1 location to a location under the L2 directory that is not shared.
This is helpful in that students may not run the labs in order, or at all, and will still expect later labs to run in the same way as they see in the video.

```

### `memories.json`

42 records, one day of captures: 20 `text`, 17 `photo`, 5 `voice`; ids 0 to 41; timestamps
1694624400 to 1694728800 (13 to 14 September 2023, UTC). Fields: `id`, `source_type`, `category`,
`location`, `timestamp`, then `note` and optional `price` for text, `file` for photos,
`transcript` and `audio_file` for voice, and `store` on some records. Read by Lesson 3 (text
records only), Lesson 4 (all), and Lesson 5 (all, through `load_day_and_history`).

```json
[
  {
    "id": 0,
    "source_type": "text",
    "category": "food",
    "location": "5th St",
    "timestamp": 1694679480,
    "note": "Great little coffee place on 5th with outdoor seating and fast wifi",
    "price": 6.0
  },
  {
    "id": 1,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1694685600,
    "note": "Standup with Sarah moved to Thursday to review the Q3 roadmap"
  },
  {
    "id": 2,
    "source_type": "text",
    "category": "errands",
    "location": "Home",
    "timestamp": 1694682000,
    "note": "Pick up dry cleaning before Friday, ticket is on the fridge"
  },
  {
    "id": 3,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1694691000,
    "note": "Idea: batch the weekly report so it drafts itself every Monday"
  },
  {
    "id": 4,
    "source_type": "text",
    "category": "social",
    "location": "Home",
    "timestamp": 1694718000,
    "note": "Mum's new address is 14 Elm Court, buzzer 3"
  },
  {
    "id": 5,
    "source_type": "text",
    "category": "shopping",
    "location": "Mall",
    "timestamp": 1694704680,
    "note": "Liked the black and white running shoes at the mall, about $45",
    "price": 45.0
  },
  {
    "id": 6,
    "source_type": "text",
    "category": "social",
    "location": "Home",
    "timestamp": 1694725200,
    "note": "Book club is reading the new sci-fi novel, we meet next Tuesday"
  },
  {
    "id": 7,
    "source_type": "text",
    "category": "health",
    "location": "Home",
    "timestamp": 1694692800,
    "note": "Dentist appointment confirmed for next Wednesday at 2pm"
  },
  {
    "id": 8,
    "source_type": "text",
    "category": "food",
    "location": "Downtown",
    "timestamp": 1694694600,
    "note": "Try the new ramen place downtown, everyone raves about the tonkotsu",
    "price": 18.0
  },
  {
    "id": 9,
    "source_type": "text",
    "category": "home",
    "location": "Home",
    "timestamp": 1694712600,
    "note": "Water the plants twice a week while the amaryllis is blooming"
  },
  {
    "id": 10,
    "source_type": "text",
    "category": "health",
    "location": "Gym",
    "timestamp": 1694676600,
    "note": "Renewed the gym membership, locker code is 4471",
    "price": 40.0
  },
  {
    "id": 11,
    "source_type": "text",
    "category": "work",
    "location": "Park",
    "price": 14,
    "timestamp": 1694707200,
    "note": "Found a quiet cafe with good wifi to work from near the park"
  },
  {
    "id": 12,
    "source_type": "text",
    "category": "errands",
    "location": "Home",
    "timestamp": 1694721600,
    "note": "Remember to call the landlord about the leaking tap"
  },
  {
    "id": 13,
    "source_type": "text",
    "category": "food",
    "location": "5th St",
    "timestamp": 1694678400,
    "note": "New bakery on the corner does an amazing morning cronut",
    "price": 4.0
  },
  {
    "id": 14,
    "source_type": "text",
    "category": "errands",
    "location": "Home",
    "timestamp": 1694728800,
    "note": "Parking permit renewal is due at the end of the month"
  },
  {
    "id": 15,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1694700000,
    "note": "Meeting notes: ship the edge demo before the conference"
  },
  {
    "id": 16,
    "source_type": "text",
    "category": "home",
    "location": "Home",
    "timestamp": 1694714400,
    "note": "Bought a new houseplant for the kitchen windowsill",
    "price": 12.0
  },
  {
    "id": 17,
    "source_type": "text",
    "category": "travel",
    "location": "Station",
    "timestamp": 1694727000,
    "note": "Weekend trip: check train times to the coast on Saturday"
  },
  {
    "id": 18,
    "source_type": "text",
    "category": "food",
    "location": "Office",
    "timestamp": 1694624400,
    "note": "Coffee run to the espresso bar near the office",
    "price": 3.0
  },
  {
    "id": 19,
    "source_type": "text",
    "category": "work",
    "location": "Home",
    "timestamp": 1694635200,
    "note": "Late night fixing the deploy pipeline, finally green"
  },
  {
    "id": 20,
    "source_type": "voice",
    "category": "food",
    "location": "Downtown",
    "timestamp": 1694697840,
    "transcript": "Note to self, the ramen downtown was incredible, fourteen dollars and worth it, sat right by the window",
    "audio_file": "ramen.wav",
    "price": 14.0,
    "store": "Ramen-ya"
  },
  {
    "id": 21,
    "source_type": "voice",
    "category": "shopping",
    "location": "Mall",
    "timestamp": 1694705400,
    "transcript": "Reminder, buy a birthday present for Alex this week, maybe those headphones he mentioned",
    "audio_file": "birthday.wav"
  },
  {
    "id": 22,
    "source_type": "voice",
    "category": "work",
    "location": "Office",
    "timestamp": 1694685960,
    "transcript": "Quick memo, the standup is moved to Thursday, tell the rest of the team",
    "audio_file": "standup.wav"
  },
  {
    "id": 23,
    "source_type": "voice",
    "category": "travel",
    "location": "Station",
    "timestamp": 1694682720,
    "transcript": "Parked the bike near the station, second rack from the entrance",
    "audio_file": "bike.wav"
  },
  {
    "id": 24,
    "source_type": "voice",
    "category": "errands",
    "location": "Home",
    "timestamp": 1694719800,
    "transcript": "Just remembered, we are low on coffee at home, grab a bag on the way back",
    "audio_file": "coffee.wav"
  },
  {
    "id": 25,
    "source_type": "photo",
    "category": "food",
    "location": "5th St",
    "timestamp": 1694679119,
    "file": "coffee.jpg",
    "store": "Blue Cup"
  },
  {
    "id": 26,
    "source_type": "photo",
    "category": "food",
    "location": "5th St",
    "timestamp": 1694678760,
    "file": "bakery.jpg",
    "price": 4.0
  },
  {
    "id": 27,
    "source_type": "photo",
    "category": "food",
    "location": "Downtown",
    "timestamp": 1694696400,
    "file": "restaurant.jpg",
    "store": "Elizabeth's"
  },
  {
    "id": 28,
    "source_type": "photo",
    "category": "food",
    "location": "Downtown",
    "timestamp": 1694697120,
    "file": "ramen.jpg",
    "price": 14.0,
    "store": "Ramen-ya"
  },
  {
    "id": 29,
    "source_type": "photo",
    "category": "food",
    "location": "Home",
    "timestamp": 1694721600,
    "file": "pizza.jpg",
    "price": 18.0
  },
  {
    "id": 30,
    "source_type": "photo",
    "category": "shopping",
    "location": "Mall",
    "timestamp": 1694704680,
    "file": "sneakers.jpg",
    "price": 45.0,
    "store": "SportsWorld"
  },
  {
    "id": 31,
    "source_type": "photo",
    "category": "travel",
    "location": "5th St",
    "timestamp": 1694682360,
    "file": "bicycle.jpg"
  },
  {
    "id": 32,
    "source_type": "photo",
    "category": "travel",
    "location": "Station",
    "timestamp": 1694727360,
    "file": "train.jpg"
  },
  {
    "id": 33,
    "source_type": "photo",
    "category": "travel",
    "location": "Downtown",
    "timestamp": 1694707920,
    "file": "street.jpg"
  },
  {
    "id": 34,
    "source_type": "photo",
    "category": "travel",
    "location": "Park",
    "timestamp": 1694709000,
    "file": "park.jpg"
  },
  {
    "id": 35,
    "source_type": "photo",
    "category": "home",
    "location": "Home",
    "timestamp": 1694712960,
    "file": "plant.jpg",
    "price": 12.0
  },
  {
    "id": 36,
    "source_type": "photo",
    "category": "home",
    "location": "Home",
    "timestamp": 1694715120,
    "file": "kitchen.jpg"
  },
  {
    "id": 37,
    "source_type": "photo",
    "category": "social",
    "location": "Park",
    "timestamp": 1694710800,
    "file": "dog.jpg"
  },
  {
    "id": 38,
    "source_type": "photo",
    "category": "shopping",
    "location": "Mall",
    "timestamp": 1694706480,
    "file": "book.jpg",
    "price": 15.0
  },
  {
    "id": 39,
    "source_type": "photo",
    "category": "work",
    "location": "Park",
    "timestamp": 1694707560,
    "file": "laptop.jpg"
  },
  {
    "id": 40,
    "source_type": "photo",
    "category": "work",
    "location": "Office",
    "timestamp": 1694685600,
    "file": "meeting.jpg"
  },
  {
    "id": 41,
    "source_type": "photo",
    "category": "health",
    "location": "Gym",
    "timestamp": 1694676240,
    "file": "gym.jpg"
  }
]
```

### `recent_days.json`

102 records from the earlier days: 81 `text`, 21 `voice`, no photos; ids 1000 to 1101; timestamps
1692862200 to 1694635200 (24 August to 13 September 2023, UTC). Same fields as `memories.json`.
Read by Lesson 5 only, through `load_day_and_history`, as the assistant's history. Its note
id 1033 (30 August, "locker code at the gym is 2280") and `memories.json` id 10 (14 September,
"locker code is 4471") are the two gym locker memories the freshness section is about.

```json
[
  {
    "id": 1000,
    "source_type": "text",
    "category": "food",
    "location": "5th St",
    "timestamp": 1692862200,
    "note": "Coffee at Blue Cup, espresso, $5",
    "price": 5.0,
    "store": "Blue Cup"
  },
  {
    "id": 1001,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1692867600,
    "note": "Standup at 9:30, review dashboard update"
  },
  {
    "id": 1002,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1692885600,
    "note": "Sarah says the kitchen refactor PR is live"
  },
  {
    "id": 1003,
    "source_type": "voice",
    "category": "errands",
    "location": "Station",
    "timestamp": 1692901800,
    "transcript": "Note to self, buy milk and bread on the way home"
  },
  {
    "id": 1004,
    "source_type": "text",
    "category": "health",
    "location": "Gym",
    "timestamp": 1692945000,
    "note": "Gym early, shoulders and back day"
  },
  {
    "id": 1005,
    "source_type": "text",
    "category": "social",
    "location": "Office",
    "timestamp": 1692957600,
    "note": "Meeting with Alex about the coast trip weekend"
  },
  {
    "id": 1006,
    "source_type": "text",
    "category": "food",
    "location": "Downtown",
    "timestamp": 1692964800,
    "note": "Lunch at Ramen-ya, tonkotsu broth, $14",
    "price": 14.0,
    "store": "Ramen-ya"
  },
  {
    "id": 1007,
    "source_type": "text",
    "category": "social",
    "location": "Home",
    "timestamp": 1692975600,
    "note": "Book club Friday, new sci-fi novel starts"
  },
  {
    "id": 1008,
    "source_type": "voice",
    "category": "social",
    "location": null,
    "timestamp": 1692990000,
    "transcript": "Reminder, Mum's birthday, she wants a scarf"
  },
  {
    "id": 1009,
    "source_type": "text",
    "category": "home",
    "location": "Home",
    "timestamp": 1693000800,
    "note": "Fixed the dripping kitchen tap finally"
  },
  {
    "id": 1010,
    "source_type": "text",
    "category": "travel",
    "location": null,
    "timestamp": 1693033200,
    "note": "Commute took 35 min, bike path was blocked"
  },
  {
    "id": 1011,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1693042200,
    "note": "Debug production issue in user auth service"
  },
  {
    "id": 1012,
    "source_type": "text",
    "category": "food",
    "location": "Office",
    "timestamp": 1693054800,
    "note": "Sandwich from deli, turkey Swiss, $8.50",
    "price": 8.5
  },
  {
    "id": 1013,
    "source_type": "voice",
    "category": "errands",
    "location": "Home",
    "timestamp": 1693065600,
    "transcript": "Quick memo, need to buy new lightbulbs for the living room"
  },
  {
    "id": 1014,
    "source_type": "text",
    "category": "social",
    "location": "Park",
    "timestamp": 1693123200,
    "note": "Coffee with Alex at Park, meeting was good"
  },
  {
    "id": 1015,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1693134000,
    "note": "Stakeholder meeting about Q3 roadmap"
  },
  {
    "id": 1016,
    "source_type": "text",
    "category": "errands",
    "location": "Downtown",
    "timestamp": 1693146600,
    "note": "Groceries, $52, including meat for Sunday roast",
    "price": 52.0
  },
  {
    "id": 1017,
    "source_type": "voice",
    "category": "home",
    "location": "Home",
    "timestamp": 1693159200,
    "transcript": "Note to self, landlord says rent stays same next year"
  },
  {
    "id": 1018,
    "source_type": "text",
    "category": "home",
    "location": "Home",
    "timestamp": 1693170000,
    "note": "Planted basil in kitchen window, hoping it survives"
  },
  {
    "id": 1019,
    "source_type": "text",
    "category": "social",
    "location": "Home",
    "timestamp": 1693213200,
    "note": "Finished sci-fi book, really gripping"
  },
  {
    "id": 1020,
    "source_type": "text",
    "category": "food",
    "location": "Downtown",
    "timestamp": 1693224000,
    "note": "Lunch special at Ramen-ya, $11.50 with tea",
    "price": 11.5,
    "store": "Ramen-ya"
  },
  {
    "id": 1021,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1693234800,
    "note": "Sarah's PR review needs one more iteration"
  },
  {
    "id": 1022,
    "source_type": "voice",
    "category": "travel",
    "location": "Home",
    "timestamp": 1693243800,
    "transcript": "Reminder, bike needs new chain soon, check pressure"
  },
  {
    "id": 1023,
    "source_type": "text",
    "category": "health",
    "location": null,
    "timestamp": 1693252800,
    "note": "Flu shot appointment next Tuesday at 3pm"
  },
  {
    "id": 1024,
    "source_type": "text",
    "category": "health",
    "location": "Gym",
    "timestamp": 1693290600,
    "note": "Gym session, legs, feeling strong today"
  },
  {
    "id": 1025,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1693303200,
    "note": "Code review for new API endpoints done"
  },
  {
    "id": 1026,
    "source_type": "text",
    "category": "travel",
    "location": "Home",
    "timestamp": 1693323000,
    "note": "Planning items for weekend coast trip"
  },
  {
    "id": 1027,
    "source_type": "voice",
    "category": "errands",
    "location": "Home",
    "timestamp": 1693335600,
    "transcript": "Note to self, return library books tomorrow morning"
  },
  {
    "id": 1028,
    "source_type": "text",
    "category": "social",
    "location": "Home",
    "timestamp": 1693342800,
    "note": "Mum called, she likes the scarf idea"
  },
  {
    "id": 1029,
    "source_type": "text",
    "category": "food",
    "location": "5th St",
    "timestamp": 1693382400,
    "note": "Morning coffee, oat milk cappuccino, $6",
    "price": 6.0,
    "store": "Blue Cup"
  },
  {
    "id": 1030,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1693391400,
    "note": "Team standup, release planned for Friday"
  },
  {
    "id": 1031,
    "source_type": "text",
    "category": "social",
    "location": "Downtown",
    "timestamp": 1693400400,
    "note": "Lunch meeting with Alex at downtown spot"
  },
  {
    "id": 1032,
    "source_type": "text",
    "category": "shopping",
    "location": "Mall",
    "timestamp": 1693411200,
    "note": "Bought scarf for Mum, blue wool, $45",
    "price": 45.0
  },
  {
    "id": 1033,
    "source_type": "voice",
    "category": "health",
    "location": "Gym",
    "timestamp": 1693420200,
    "transcript": "Quick memo, locker code at the gym is 2280"
  },
  {
    "id": 1034,
    "source_type": "text",
    "category": "travel",
    "location": "Home",
    "timestamp": 1693432800,
    "note": "Packed for coast trip, leaving tomorrow"
  },
  {
    "id": 1035,
    "source_type": "text",
    "category": "travel",
    "location": "Station",
    "timestamp": 1693465200,
    "note": "Coast trip day, early morning departure"
  },
  {
    "id": 1036,
    "source_type": "text",
    "category": "food",
    "location": null,
    "timestamp": 1693483200,
    "note": "Lunch at beach cafe, fish and chips, $16",
    "price": 16.0
  },
  {
    "id": 1037,
    "source_type": "voice",
    "category": "travel",
    "location": null,
    "timestamp": 1693494000,
    "transcript": "Note to self, Alex found great hiking trail near coast"
  },
  {
    "id": 1038,
    "source_type": "text",
    "category": "food",
    "location": null,
    "timestamp": 1693508400,
    "note": "Hotel dinner, local seafood place, $38",
    "price": 38.0
  },
  {
    "id": 1039,
    "source_type": "text",
    "category": "social",
    "location": null,
    "timestamp": 1693515600,
    "note": "Sunset walk along the beach with Alex"
  },
  {
    "id": 1040,
    "source_type": "text",
    "category": "food",
    "location": null,
    "timestamp": 1693555200,
    "note": "Breakfast at cafe, avocado toast, $12",
    "price": 12.0
  },
  {
    "id": 1041,
    "source_type": "text",
    "category": "travel",
    "location": null,
    "timestamp": 1693566000,
    "note": "Hiking trail with Alex, saw three deer"
  },
  {
    "id": 1042,
    "source_type": "text",
    "category": "shopping",
    "location": null,
    "timestamp": 1693584000,
    "note": "Bought local pottery, $28, hand wash only",
    "price": 28.0
  },
  {
    "id": 1043,
    "source_type": "voice",
    "category": "home",
    "location": "Home",
    "timestamp": 1693596600,
    "transcript": "Reminder, the pottery can't go in the dishwasher"
  },
  {
    "id": 1044,
    "source_type": "text",
    "category": "social",
    "location": null,
    "timestamp": 1693602000,
    "note": "Evening at hotel, wine and board games"
  },
  {
    "id": 1045,
    "source_type": "text",
    "category": "food",
    "location": null,
    "timestamp": 1693641600,
    "note": "Last morning at coast, relaxed breakfast"
  },
  {
    "id": 1046,
    "source_type": "text",
    "category": "errands",
    "location": null,
    "timestamp": 1693659600,
    "note": "Drove back, stopped at roadside market"
  },
  {
    "id": 1047,
    "source_type": "text",
    "category": "home",
    "location": "Home",
    "timestamp": 1693677600,
    "note": "Back home, unpacking from the trip"
  },
  {
    "id": 1048,
    "source_type": "voice",
    "category": "errands",
    "location": "Home",
    "timestamp": 1693684800,
    "transcript": "Note to self, do laundry tomorrow morning"
  },
  {
    "id": 1049,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1693731600,
    "note": "Back at work, caught up on emails"
  },
  {
    "id": 1050,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1693738800,
    "note": "Sarah wants to pair program on auth service"
  },
  {
    "id": 1051,
    "source_type": "text",
    "category": "home",
    "location": "Home",
    "timestamp": 1693753200,
    "note": "Finished laundry, put pottery on shelf"
  },
  {
    "id": 1052,
    "source_type": "voice",
    "category": "social",
    "location": "Home",
    "timestamp": 1693765800,
    "transcript": "Quick reminder, book club Friday night, bring wine"
  },
  {
    "id": 1053,
    "source_type": "text",
    "category": "health",
    "location": "Gym",
    "timestamp": 1693771200,
    "note": "Gym session, arms and core work"
  },
  {
    "id": 1054,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1693821600,
    "note": "Pair programming with Sarah, fixed bug"
  },
  {
    "id": 1055,
    "source_type": "text",
    "category": "shopping",
    "location": "Mall",
    "timestamp": 1693843200,
    "note": "Shopping for book club wine, red blend, $18",
    "price": 18.0
  },
  {
    "id": 1056,
    "source_type": "voice",
    "category": "home",
    "location": "Home",
    "timestamp": 1693854000,
    "transcript": "Reminder, basil on windowsill needs water today"
  },
  {
    "id": 1057,
    "source_type": "text",
    "category": "travel",
    "location": null,
    "timestamp": 1693900800,
    "note": "Commute smooth, bike path working again"
  },
  {
    "id": 1058,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1693909800,
    "note": "Release prep meeting, everything good"
  },
  {
    "id": 1059,
    "source_type": "text",
    "category": "food",
    "location": "Downtown",
    "timestamp": 1693917000,
    "note": "Team lunch at sandwich place, $9.50",
    "price": 9.5
  },
  {
    "id": 1060,
    "source_type": "text",
    "category": "health",
    "location": null,
    "timestamp": 1693926000,
    "note": "Doctor appointment confirmed, Tuesday 2pm"
  },
  {
    "id": 1061,
    "source_type": "voice",
    "category": "social",
    "location": "Home",
    "timestamp": 1693936800,
    "transcript": "Note to self, Mum got the scarf, she loves it"
  },
  {
    "id": 1062,
    "source_type": "text",
    "category": "health",
    "location": "Park",
    "timestamp": 1693944000,
    "note": "Evening jog around the park, 3 miles"
  },
  {
    "id": 1063,
    "source_type": "text",
    "category": "health",
    "location": "Gym",
    "timestamp": 1693981800,
    "note": "Gym early, chest and triceps day"
  },
  {
    "id": 1064,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1693990800,
    "note": "Final release tests passing, shipping Friday"
  },
  {
    "id": 1065,
    "source_type": "text",
    "category": "social",
    "location": "Office",
    "timestamp": 1694008800,
    "note": "Alex texted, wants to hike again next month"
  },
  {
    "id": 1066,
    "source_type": "voice",
    "category": "social",
    "location": "Home",
    "timestamp": 1694019600,
    "transcript": "Reminder, need to prep something nice for book club"
  },
  {
    "id": 1067,
    "source_type": "text",
    "category": "food",
    "location": "5th St",
    "timestamp": 1694073600,
    "note": "Friday coffee, celebrating the release",
    "price": 6.0,
    "store": "Blue Cup"
  },
  {
    "id": 1068,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1694080800,
    "note": "Release deployed successfully, no issues"
  },
  {
    "id": 1069,
    "source_type": "text",
    "category": "food",
    "location": "Downtown",
    "timestamp": 1694088000,
    "note": "Celebration lunch with Sarah and team",
    "price": 15.0
  },
  {
    "id": 1070,
    "source_type": "text",
    "category": "social",
    "location": "Home",
    "timestamp": 1694098800,
    "note": "Left work early, heading to book club"
  },
  {
    "id": 1071,
    "source_type": "voice",
    "category": "social",
    "location": "Home",
    "timestamp": 1694113200,
    "transcript": "Book club night, great discussion, wine perfect"
  },
  {
    "id": 1072,
    "source_type": "text",
    "category": "social",
    "location": "Home",
    "timestamp": 1694167200,
    "note": "Book club moves to Alex place next time, 22 Birch Lane"
  },
  {
    "id": 1073,
    "source_type": "text",
    "category": "food",
    "location": "Downtown",
    "timestamp": 1694174400,
    "note": "Brunch at the cafe, pancakes and coffee, $14",
    "price": 14.0
  },
  {
    "id": 1074,
    "source_type": "text",
    "category": "errands",
    "location": "Downtown",
    "timestamp": 1694185200,
    "note": "Grocery shopping, ingredients for new recipe",
    "price": 38.0
  },
  {
    "id": 1075,
    "source_type": "voice",
    "category": "food",
    "location": "Home",
    "timestamp": 1694196000,
    "transcript": "Note to self, try the Thai curry recipe this week"
  },
  {
    "id": 1076,
    "source_type": "text",
    "category": "health",
    "location": "Gym",
    "timestamp": 1694203200,
    "note": "Gym session, cardio and weights"
  },
  {
    "id": 1077,
    "source_type": "text",
    "category": "travel",
    "location": "Park",
    "timestamp": 1694242800,
    "note": "Morning bike ride, clearing my head"
  },
  {
    "id": 1078,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1694253600,
    "note": "Monday standup, planning next sprint"
  },
  {
    "id": 1079,
    "source_type": "text",
    "category": "food",
    "location": "Office",
    "timestamp": 1694264400,
    "note": "Lunch, tried Thai curry, really good, $11",
    "price": 11.0
  },
  {
    "id": 1080,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1694273400,
    "note": "Sarah wants to discuss refactoring payment module"
  },
  {
    "id": 1081,
    "source_type": "voice",
    "category": "health",
    "location": "Home",
    "timestamp": 1694286000,
    "transcript": "Reminder, doctor appointment tomorrow, bring insurance card"
  },
  {
    "id": 1082,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1694343600,
    "note": "Code review for payment refactoring PR"
  },
  {
    "id": 1083,
    "source_type": "text",
    "category": "food",
    "location": "Office",
    "timestamp": 1694352600,
    "note": "Quick lunch, sandwich from deli, $9",
    "price": 9.0
  },
  {
    "id": 1084,
    "source_type": "voice",
    "category": "health",
    "location": "Office",
    "timestamp": 1694354400,
    "transcript": "Quick memo, doctor appointment in an hour"
  },
  {
    "id": 1085,
    "source_type": "text",
    "category": "health",
    "location": null,
    "timestamp": 1694361600,
    "note": "Doctor visit went well, all clear"
  },
  {
    "id": 1086,
    "source_type": "text",
    "category": "food",
    "location": "Home",
    "timestamp": 1694370600,
    "note": "Made Thai curry at home, turned out great"
  },
  {
    "id": 1087,
    "source_type": "text",
    "category": "health",
    "location": "Gym",
    "timestamp": 1694417400,
    "note": "Gym session, back to routine"
  },
  {
    "id": 1088,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1694426400,
    "note": "Payment refactoring PR approved, merging today"
  },
  {
    "id": 1089,
    "source_type": "text",
    "category": "social",
    "location": "Downtown",
    "timestamp": 1694433600,
    "note": "Lunch with Alex, planning next coast trip"
  },
  {
    "id": 1090,
    "source_type": "text",
    "category": "travel",
    "location": "Home",
    "timestamp": 1694444400,
    "note": "Bike chain needs replacing, will do this weekend"
  },
  {
    "id": 1091,
    "source_type": "voice",
    "category": "shopping",
    "location": "Station",
    "timestamp": 1694455200,
    "transcript": "Note to self, buy new bike chain at the station shop"
  },
  {
    "id": 1092,
    "source_type": "text",
    "category": "social",
    "location": "Home",
    "timestamp": 1694462400,
    "note": "Evening walk with Alex around neighborhood"
  },
  {
    "id": 1093,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1694516400,
    "note": "Sprint planning session for next cycle"
  },
  {
    "id": 1094,
    "source_type": "text",
    "category": "shopping",
    "location": "Station",
    "timestamp": 1694534400,
    "note": "Bought new bike chain, $32 at station shop",
    "price": 32.0
  },
  {
    "id": 1095,
    "source_type": "voice",
    "category": "travel",
    "location": "Home",
    "timestamp": 1694547000,
    "transcript": "Reminder, replace the bike chain tomorrow afternoon"
  },
  {
    "id": 1096,
    "source_type": "text",
    "category": "social",
    "location": "Home",
    "timestamp": 1694552400,
    "note": "Watched sci-fi movie, good one"
  },
  {
    "id": 1097,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1694588400,
    "note": "Office wifi password is on the whiteboard by the kitchen"
  },
  {
    "id": 1098,
    "source_type": "text",
    "category": "work",
    "location": "Office",
    "timestamp": 1694599200,
    "note": "Final checks on deployed feature, no issues"
  },
  {
    "id": 1099,
    "source_type": "text",
    "category": "travel",
    "location": "Home",
    "timestamp": 1694617200,
    "note": "Replaced bike chain finally, runs smooth"
  },
  {
    "id": 1100,
    "source_type": "voice",
    "category": "social",
    "location": "Home",
    "timestamp": 1694628000,
    "transcript": "Note to self, Alex wants to hike again next weekend"
  },
  {
    "id": 1101,
    "source_type": "text",
    "category": "health",
    "location": "Gym",
    "timestamp": 1694635200,
    "note": "Evening gym session, finished strong"
  }
]
```

### `audio/` (6 files)

`audio/README.md` (verbatim):

```markdown
# Voice-note audio

Five short voice memos, one per voice capture in `ro_shared_data/memories.json`, plus `question.wav`, a spoken question Lesson 4 asks the assistant in section 5. Lesson 4 transcribes them on-device with a small Whisper model, so the "voice" modality runs a real speech-to-text step. Each memo maps to its note through the `audio_file` field in `ro_shared_data/memories.json`. `question.wav` stands on its own and belongs to no memory.
```
Files: `bike.wav`, `birthday.wav`, `coffee.wav`, `question.wav`, `ramen.wav`, `standup.wav`


### `images/` (17 files)

Scene photos for one day, referenced by the `file` field of the photo records in `memories.json`
(Lesson 4 and Lesson 5). Attribution in `images/CREDITS.json` (not embedded).

Files: `bakery.jpg`, `bicycle.jpg`, `book.jpg`, `coffee.jpg`, `dog.jpg`, `gym.jpg`, `kitchen.jpg`, `laptop.jpg`, `meeting.jpg`, `park.jpg`, `pizza.jpg`, `plant.jpg`, `ramen.jpg`, `restaurant.jpg`, `sneakers.jpg`, `street.jpg`, `train.jpg`


### `objects/` (16 files)

`objects/README.md` (verbatim):

```markdown
# Object photos

Six subjects, two or three photos of each: backpack, gaillardia, hardhat, lithops, rubberduck, vase. Each set is several views of the same physical object, which is what Lesson 5 needs to teach recognition from a handful of examples and then test on a view it never saw.

Lesson 5 falls back to the rubber duck when you upload nothing. To teach one of the other five instead, use the two upload buttons in the lesson's first cell and pick the files from this folder: two or more views on the left to teach with, and one more view of the same object on the right, held back for the test. The vase set, for example, teaches from `vase_1.jpg` and `vase_2.jpg` and tests on `vase_3.jpg`.

Photo credits, with author and license for each file, are in `CREDITS.json`.
```
Files: `backpack_1.jpg`, `backpack_2.jpg`, `gaillardia_1.jpg`, `gaillardia_2.jpg`, `gaillardia_3.jpg`, `hardhat_1.jpg`, `hardhat_2.jpg`, `hardhat_3.jpg`, `lithops_1.jpg`, `lithops_2.jpg`, `rubberduck_1.jpg`, `rubberduck_2.jpg`, `rubberduck_3.jpg`, `vase_1.jpg`, `vase_2.jpg`, `vase_3.jpg`

Attribution in `objects/CREDITS.json` (not embedded).


### `bank/` (165 files)

The image-search bank for Lesson 3 (all 165 stored as photo memories) and the source of
Lesson 5's three seed objects (`bicycle.jpg`, `chess_set.jpg`, `camera.jpg`). One object or
scene per photo, named for its subject. Attribution in `bank/CREDITS.json` (not embedded).

Files: `airport_terminal.jpg`, `ambulance.jpg`, `autumn_leaves.jpg`, `avocado.jpg`, `backpacking_gear.jpg`, `bagel.jpg`, `banana.jpg`, `baseball_glove.jpg`, `basketball.jpg`, `beach_sunset.jpg`, `bed.jpg`, `beer_glass.jpg`, `bell_pepper.jpg`, `bicycle.jpg`, `bouquet_flowers.jpg`, `bridge_over_river.jpg`, `bus_stop.jpg`, `butterfly.jpg`, `cactus_plant.jpg`, `calculator.jpg`, `camera.jpg`, `cappuccino.jpg`, `carrot.jpg`, `cat.jpg`, `chess_set.jpg`, `chocolate_cake.jpg`, `city_bus.jpg`, `coffee_mug.jpg`, `coins_money.jpg`, `cooking_pot.jpg`, `corn_cob.jpg`, `cow.jpg`, `croissant.jpg`, `cupcake.jpg`, `curry_rice.jpg`, `delivery_van.jpg`, `denim_jacket.jpg`, `desert_dunes.jpg`, `desk_fan.jpg`, `dice.jpg`, `dog_puppy.jpg`, `dolphin.jpg`, `drum_kit.jpg`, `duck_pond.jpg`, `dumbbell_weights.jpg`, `elephant.jpg`, `espresso.jpg`, `fire_extinguisher.jpg`, `fishing_rod.jpg`, `forest_trail.jpg`, `french_fries.jpg`, `fried_chicken.jpg`, `frog.jpg`, `fruit_bowl.jpg`, `full_moon.jpg`, `game_controller.jpg`, `garden_shovel.jpg`, `gas_station.jpg`, `giraffe.jpg`, `goldfish.jpg`, `grocery_store_aisle.jpg`, `gym_interior.jpg`, `hair_dryer.jpg`, `hamburger.jpg`, `hamster.jpg`, `headphones.jpg`, `helicopter.jpg`, `high_heels.jpg`, `hiking_boots.jpg`, `honeybee.jpg`, `horse.jpg`, `ice_cream_cone.jpg`, `jack_o_lantern.jpg`, `keyboard.jpg`, `kitchen_knife.jpg`, `ladder.jpg`, `ladybug.jpg`, `lake.jpg`, `leather_boots.jpg`, `lemon.jpg`, `library_shelves.jpg`, `light_bulb.jpg`, `lightning_storm.jpg`, `lion.jpg`, `map.jpg`, `microphone.jpg`, `microwave_oven.jpg`, `morning_fog.jpg`, `mushroom.jpg`, `necklace.jpg`, `necktie.jpg`, `newspaper.jpg`, `notebook_journal.jpg`, `ocean_waves.jpg`, `office_desk.jpg`, `onion.jpg`, `palm_tree.jpg`, `park_bench.jpg`, `park_fountain.jpg`, `parrot_bird.jpg`, `pencil.jpg`, `penguin.jpg`, `piano.jpg`, `picture_frame.jpg`, `piggy_bank.jpg`, `pizza_slice.jpg`, `rabbit.jpg`, `rainbow_sky.jpg`, `rainy_window.jpg`, `red_wine_glass.jpg`, `refrigerator.jpg`, `river_stream.jpg`, `roller_skates.jpg`, `rose_flower.jpg`, `sailboat.jpg`, `sandwich.jpg`, `scissors.jpg`, `scooter.jpg`, `shopping_cart.jpg`, `skateboard.jpg`, `skyline_at_night.jpg`, `smoothie.jpg`, `snowflakes.jpg`, `snowy_street.jpg`, `soccer_ball.jpg`, `sofa_couch.jpg`, `spider_web.jpg`, `squirrel.jpg`, `stapler.jpg`, `starry_night_sky.jpg`, `statue.jpg`, `steak_dinner.jpg`, `strawberries.jpg`, `subway_platform.jpg`, `sunflower.jpg`, `sunglasses.jpg`, `sushi_platter.jpg`, `swimming_pool.jpg`, `tacos.jpg`, `tea_cup.jpg`, `telescope.jpg`, `tennis_racket.jpg`, `tent_camping.jpg`, `thermometer.jpg`, `tomato.jpg`, `toothbrush.jpg`, `tulip.jpg`, `turtle.jpg`, `vineyard.jpg`, `vinyl_record.jpg`, `waffles.jpg`, `wall_clock.jpg`, `wallet.jpg`, `washing_machine.jpg`, `water_bottle.jpg`, `water_glass.jpg`, `waterfall.jpg`, `watering_can.jpg`, `watermelon.jpg`, `wheat_field.jpg`, `wine_bottle.jpg`, `wool_scarf.jpg`, `wristband.jpg`, `wristwatch.jpg`, `yellow_taxi.jpg`


---

## Appendix: items the course README lists that are not in this copy of the repo

- **`Appendix/` (Cloud Sync: One Memory, Many Devices).** The README's lesson table, "Run the
  notebooks locally" section and repository layout all name an appendix notebook that syncs one
  device's memory to a Qdrant cluster and to a second device. There is no `Appendix/` directory in
  `SC-Qdrant-C3-main/`. Its helper functions are present in every copy of helper.py
  (`cloud_client`, `cloud_points`, `push_note`, `fetch_snapshot`, `file_size`), and
  `requirements.txt` pins `qdrant-client` for it.
- **Saved notebook outputs.** The README and requirements.txt refer to scores "in the saved
  outputs"; all three notebooks here have empty outputs.
- **The recognition threshold name.** As noted under Lesson 5, `RECOGNIZE_THRESHOLD` is used in
  cell 12 but defined nowhere in the repo.
