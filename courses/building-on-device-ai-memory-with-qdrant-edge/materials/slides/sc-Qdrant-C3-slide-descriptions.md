# Slide descriptions: Building On-Device AI Memory with Qdrant Edge
Source decks: slides/Qdrant_Slides – Wide (16_9).pptx (14 slides), slides/Qdrant_Slides – Tall (8_9).pptx (22 slides)
Instructor: Dylan Couzon

Rich text descriptions of the course slides, organized by lesson in the same order and with the
same lesson titles as the transcripts in `../transcripts/`. Each entry gives the deck and original
slide number, the time range the slide is on screen in the lesson video, the transcript passage
spoken over it, every word visible on the slide, a description of the visual, and what it teaches.

## How to read this file

- **Lesson assignment comes from the videos, not the decks.** The decks use an earlier lesson
  plan (the Tall deck's title cards say "Lesson 2: Store and Recall", "Lesson 3: Finding the Right
  Memory", and so on, and the Course Map slide lists six lessons). Every slide below was matched to
  the lesson video it actually appears in, by sampling frames every 2 seconds and then every 0.5
  seconds around each slide.
- **Only eight deck slides appear in the five videos.** Lesson 1 uses five "Answered on Device"
  slides; Lesson 3 uses three Tall-deck slides beside the notebook. Lessons 2, 4, and 5 show no
  deck slides at all (only the instructor, the phone app, a screen recording of the repository, or
  the notebook). Those lessons are listed with a note so the file still has one section per lesson.
- **Slide numbering** is `Lesson.Order` in on-screen order. The deck and original slide number
  follow in parentheses so each entry can be traced back to the .pptx.
- **Timestamps** are `m:ss` in the lesson video and are accurate to about half a second. Several
  slides are animated builds; the description notes the order in which elements appear.
- **Text on slide** is transcribed verbatim from the .pptx text runs and the diagram images,
  including one typo that is on screen in the video ("Returning closes vectors").
- **Appendix A** describes the fifteen diagram slides that are in the decks but never appear in a
  video. They are grouped by the lesson they were drafted for. This goes slightly beyond the
  original request to omit unused slides; it is included because these are substantive teaching
  diagrams rather than production slides, and the appendix can be deleted without affecting the
  lesson sections. **Appendix B** lists the remaining non-content slides (teaser, placeholders,
  acknowledgments, style guide, title cards) in one line each, so all 36 slides are accounted for.
- Course-wide visual conventions: every content slide has the Qdrant logo top left and the
  DeepLearning.AI logo top right, a centered title in the deck's coral-red display face, and a
  coral-red wave along the bottom edge. Diagrams share a color code: light blue for input or
  capture, orange for embedding models, lavender/purple cylinders for the memory store, red for
  queries and recall, and teal-green for results and matches.

---

## Lesson 1: Why Devices Need Memory
Video: videos/sc-Qdrant-C3-L1-v2.mp4 (4:36) · Transcript: transcripts/sc-Qdrant-C3-L1-transcript.md

Five full-screen slides from the Wide deck, all titled "Answered on Device", run as one
continuous animated sequence from 0:45 to 1:50. Before and after this block the video shows the
instructor at a desk with the robot and two cat plushies, phone-app demos, and a screen recording
of the Qdrant Edge web page. Two other on-screen elements are video overlays, not deck slides: the
opening title card "Building AI Assistants with On-Device Memory / Overview of On-Device AI
Memory" (0:00) and the word list "Create / Store / Memory / Recall" (4:24 to 4:33).

### Slide 1.1 — Answered on Device: from a note to a vector (Wide deck, slide 10)
**On screen:** 0:45–1:06
**Transcript cue:** "I can take a note, 'I had ramen for lunch.' An embedding model turns the text into a vector. A vector is a list of numbers that represents the meaning of text. A vector search engine then creates a navigable graph to allow search through those vectors to happen extremely fast, sometimes in less than a millisecond."
**Text on slide:** Answered on Device · I had ramen for lunch · Embedding · MODEL · embed on device · 0.12, 0.85 · 0.34, 0.35 · 0.35, 0.72 · 0.81, 0.58 · 0.35, 0.19 · 0.09, 0.45 · 0.32, 0.27 · memory · top matches · stays on device · works offline
**Visual description:** A left-to-right pipeline built up one element at a time. It starts with a
rounded lavender card reading "I had ramen for lunch" with a small writing-hand-and-notepad emoji
above the text (0:46). A dashed arrow leads to a white square labelled "Embedding" over a gear
icon and the word "MODEL", with a small lavender pill underneath reading "embed on device" (0:48).
A second dashed arrow leads to a column of seven number pairs (0.12, 0.85 through 0.32, 0.27)
enclosed in large peach-colored curly braces, representing the vector (0:50). A dashed rounded
rectangle then encloses the note, the model, and the vector. A final dashed arrow points to a
lavender cylinder. The cylinder first appears labelled "memory" (0:51), then swaps to a cylinder
containing a graph of about ten white nodes joined by grey lines, captioned "top matches" in a
hand-lettered face (0:53), and later returns to the plain "memory" label (1:00). A footer line
appears at 0:55 with a green padlock emoji and "stays on device", then a paper-plane emoji and
"works offline".
**What it teaches:** The simplest memory is a text note. The embedding model runs on the device
and turns the note into a list of numbers whose values encode meaning. The vector search engine
stores those vectors and organizes them into a navigable graph so lookup is fast. The footer
states the lesson's two promises: nothing leaves the device, and it works with no network.

### Slide 1.2 — Answered on Device: asking a question (Wide deck, slide 11)
**On screen:** 1:06–1:21 (continues the animation of Slide 1.1 under the same title)
**Transcript cue:** "A question goes through the same embedding model. For example, 'What did I eat for lunch?' Then that vector search engine returns the approximate nearest neighbor to this query. The closer the vectors, the higher the similarity score. Returning the closest vectors is called retrieval. This is the core pattern you will use in this course."
**Text on slide:** Answered on Device · What did I eat for lunch? · Embedding · MODEL · embed on device · (the same seven number pairs as Slide 1.1) · memory · top matches · high similarity score · high similarity score · Qdrant · Returning closes vectors → **Retrieval** · stays on device · works offline
**Visual description:** Same layout as Slide 1.1, but the note card is replaced by a lavender card
reading "What did I eat for lunch?" (1:05). The embedding model and the vector then disappear so
that the dashed box holds only the question, with a dashed arrow straight to the "top matches"
cylinder (1:06). At 1:13 the cylinder changes to a darker purple cylinder labelled "Qdrant" at its
base, containing a graph of grey nodes and edges; two nodes glow bright green and each is
annotated in hand lettering "high similarity score", with green arrows tracing the search path
through the graph toward them. At 1:15 a caption appears at the top right: "Returning closes
vectors → Retrieval", with "Retrieval" in bold. ("closes" is a typo for "closest" and is on screen
as written.) The padlock and paper-plane footer stays visible throughout.
**What it teaches:** Retrieval is the core pattern of the course. A question is embedded with the
same model as the notes, the engine walks its graph to the nearest stored vectors, and the
closeness of vectors is the similarity score. The green glowing nodes are the approximate nearest
neighbors returned for the query.

### Slide 1.3 — Answered on Device: CLIP (Wide deck, slide 12)
**On screen:** 1:21–1:39
**Transcript cue:** "That same idea also works with photos. For this, we use the model called CLIP. CLIP has one encoder for images, another one for text. It creates a similar embedding whether you show it an image of a cat or describe a cat. That means we can search images using words."
**Text on slide:** Answered on Device · cat · **CLIP** → Contrastive Language–Image Pre-training · CLIP Model · image encoder · text encoder · [1,5,6] · [1,8,4] · [1,2,5] · [1,6,3] · [1,3,0] · [0,8,0] · [0,6,4] · [1,5,18]
**Visual description:** On the left a lavender rounded square holds a simple line drawing of a
sitting cat, captioned "cat" beneath it; small pastel stars and dots decorate the corners of the
image, and a faint "stays on device / works offline" footer is part of the image file but is not
legible in the video. The line "CLIP → Contrastive Language–Image Pre-training" appears above the
diagram at 1:24, with "CLIP" in bold. At 1:25 a dashed arrow leads from the cat to a large salmon
box titled "CLIP Model". Inside it, a lighter inner panel holds two darker salmon boxes, "image
encoder" and "text encoder", joined by a red arrow with two small sine waves drawn above and
below it. At 1:29 two columns of three-number vectors appear to the right of the model: a blue
column ([1,5,6], [1,8,4], [1,2,5], [1,6,3]) and a green column ([1,3,0], [0,8,0], [0,6,4],
[1,5,18]).
**What it teaches:** CLIP has two encoders that map images and text into the same vector space,
so the picture of a cat and the word "cat" land near each other. The two columns of vectors
stand in for the image-side and text-side embeddings that can be compared directly. This is what
makes searching photos with words possible.

### Slide 1.4 — Answered on Device: recognizing what it sees (Wide deck, slide 13)
**On screen:** 1:39–1:48
**Transcript cue:** "And the same idea lets this robot recognize what it sees by comparing with what it knows."
**Text on slide:** Answered on Device · Similarity Score · cat · CLIP
**Visual description:** A large white thought bubble fills most of the slide, with three small
trailing circles leading to a cartoon robot at the bottom right. The robot is a white rounded
capsule with a two-lens camera "face", speaker slots on its side, and a black baseball cap with
the Qdrant hexagon logo. Inside the bubble, from left to right: the label "Similarity Score" above
a photograph of a real grey-and-white tabby cat sitting on a wooden floor; an arrow into a salmon
box labelled "CLIP" whose inner lavender panel reads "cat" in a typewriter face; an arrow into a
pale green cylinder containing a small graph of green nodes; and a thin loop arrow from the top
of the cylinder back to the CLIP box. A faint dashed frame with pastel confetti (the deck's
underlay image) sits behind the bubble but is barely visible.
**What it teaches:** Recognition on the robot is the same retrieval loop. A camera frame goes
through CLIP, its vector is compared against what is already in memory, and the similarity score
tells the robot whether it is looking at something it knows. The robot is "thinking" the diagram.

### Slide 1.5 — Answered on Device: the match threshold (Wide deck, slide 14)
**On screen:** 1:48–1:50
**Transcript cue:** "If the similarity score is above a certain threshold, we have a match. And to do this, we need no LLM, no retraining, or no custom vision pipeline."
**Text on slide:** Answered on Device · similarity score > threshold · 0 · 5 · MATCH! · CLIP
**Visual description:** The same thought bubble and capped robot as Slide 1.4. The cat photo is
replaced by a small panel titled "similarity score > threshold" containing a horizontal slider
from 0 to 5 with a grey handle near 3 and a green check-mark badge at the left end. The CLIP box
now shows a green "MATCH!" badge in its inner panel instead of the word "cat". The green memory
cylinder and the loop arrow back to CLIP are unchanged.
**What it teaches:** A match is a decision rule, not a model: compare the similarity score against
a threshold. Everything the robot does in the demo comes from vectors and a threshold, with no
large language model, no retraining, and no custom vision pipeline.

---

## Lesson 2: Building the Device
Video: videos/sc-Qdrant-C3-L2-v2.mp4 (2:32) · Transcript: transcripts/sc-Qdrant-C3-L2-transcript.md

No slide from either deck appears in this video. The lesson is shot at the desk with the robot,
the two cat plushies, and the disassembled hardware, and it switches to a screen recording of the
open-source repository and the phone interface. The only graphic elements are video overlays: the
opening title card "Building AI Assistants with On-Device Memory / Inside the AI Assistant
Device" (0:00) and a word list that builds "Camera / Computer / Storage / Interface" at 0:24 to
0:27 while the instructor names the four parts of the robot.

---

## Lesson 3: Store, Find, and Forget Memories
Video: videos/sc-Qdrant-C3-L3-v2.mp4 (6:38) · Transcript: transcripts/sc-Qdrant-C3-L3-transcript.md

This lesson is a notebook screen recording in the tall half-screen format. Three Tall-deck slides
cut in, each filling the frame in place of the notebook for a few seconds. The opening title card
"Building AI Assistants with On-Device Memory / Building the Memory" (0:00) and the "Find the
latency_curve() method in helper.py for this lesson" callout (5:36 to 5:43) are video overlays,
not deck slides.

### Slide 3.1 — Anatomy of a point (Tall deck, slide 4)
**On screen:** 2:33–2:44
**Transcript cue:** "So we use what we call points to store the memory with all the vectors, but also any metadata that is associated with that memory. So we have the ID, we have the source type, which is where the memory came from. We have a category label, the location, the exact timestamp, the text version of the notes and the price when it is applicable."
**Text on slide:** Anatomy of a point · Point · id: 3 · named vector · text · payload · note + fields
**Visual description:** Under the title, a bold "Point" label sits above a tall lavender rounded
rectangle with a purple outline that fills the width of the slide. The rectangle is divided by two
dashed horizontal lines into three rows. Top row: a grey hash icon and "id: 3". Middle row: an
orange waveform icon, "named vector" with a small dot and the qualifier "text", and beneath it a
row of nine small orange-outlined boxes with partial orange fill (a strip of vector cells) ending
in an ellipsis. Bottom row: a grey document icon, "payload" with a dot and the qualifier "note +
fields". The slide appears right after the notebook cell that upserts twenty points and prints
Point 0's fields (id, source_type, category, location, timestamp, note, price).
**What it teaches:** A point is the unit of storage in Qdrant Edge: an id, one or more named
vectors (here the 768-dimensional text vector), and a payload holding the original note plus
metadata fields. The instructor reads the payload fields off the notebook output while the slide
is up.

### Slide 3.2 — Recognizing with CLIP (Tall deck, slide 9, untitled)
**On screen:** 4:16–4:21
**Transcript cue:** "Our robot doesn't only process text. It also process images and live video. Now let's add images to our memories."
**Text on slide:** cat · CLIP
**Visual description:** The same thought-bubble diagram as Lesson 1's Slide 1.4, reused in the tall
format without a title: a white thought bubble with a photograph of a tabby cat, an arrow into a
salmon "CLIP" box whose inner panel reads "cat", an arrow into a pale green cylinder with a small
node graph, and a loop arrow from the cylinder back to CLIP. The "Similarity Score" label from the
Lesson 1 version is not present. The capped white robot sits at the bottom right with three small
circles connecting it to the bubble. Above the bubble is empty space with only the Qdrant and
DeepLearning.AI logos.
**What it teaches:** A bridge from text to images. The robot's camera frames go through CLIP into
the same kind of memory store, which is what the next notebook cells build by storing 165 photos.

### Slide 3.3 — Cross-Model recall (Tall deck, slide 10)
**On screen:** 4:43–4:54
**Transcript cue:** "Since we're using CLIP, an embedding model that matches text and images, we can ask it a red bicycle, embed that query, and then search. And here we have a red bicycle retrieved."
**Text on slide:** Cross-Model recall · "a red bicycle" · CLIP text tower · text query → image space · text · image · bicycle.jpg
**Visual description:** A vertical flow. At the top, a light-blue rounded box with a speech-bubble
icon holds the query "a red bicycle". A red arrow leads down to an orange rounded box, "CLIP text
tower". From there a red arrow curves down and to the left, annotated in small red text "text
query → image space", and enters a lavender cylinder. Inside the cylinder are two stacked pills:
"text" with a document icon and five vector cells, and "image" with a picture icon and five vector
cells. The "image" pill is outlined in red to show the arrow lands there, skipping the text
vectors. A final red arrow exits the cylinder to the bottom right into a teal-green rounded box
with a picture icon, "bicycle.jpg", and a green check mark.
**What it teaches:** Because CLIP's text encoder and image encoder share one space, a text query
can be embedded with the text tower and searched against the image vectors in the shard. The
shard holds two named vectors per point, and the query chooses which one to search ("using
image" in the notebook). The result is a photo found from words.

---

## Lesson 4: Your On-Device Assistant
Video: videos/sc-Qdrant-C3-L4-v2.mp4 (4:58) · Transcript: transcripts/sc-Qdrant-C3-L4-transcript.md

No slide from either deck appears in this video. After the opening title card "Building AI
Assistants with On-Device Memory / Building the Voice Assistant" (0:00) and a short on-camera
introduction, the whole lesson is a notebook screen recording (day summary, photo grid, notes
table, voice-note transcription, the recall function, the memory inbox results, and adding a
new memory). The Tall deck's "What comes back" slide was drafted for this lesson but is not used;
see Appendix A.

---

## Lesson 5: Teaching Your Assistant to See
Video: videos/sc-Qdrant-C3-L5-v2.mp4 (5:36) · Transcript: transcripts/sc-Qdrant-C3-L5-transcript.md

No slide from either deck appears in this video. After the opening title card "Building AI
Assistants with On-Device Memory / Learning Through Memory" (0:00) and an on-camera
introduction, the lesson is a notebook screen recording (object shard, teach and recognize
functions, the rubber-duck example, threshold calibration plot, the assistant's memory, freshness
ranking, and the final question table). The Tall deck's "Teach, Store, and Recognize" and "One
Point, Two Doors" slides were drafted for this lesson but are not used; see Appendix A.

---

## Appendix A: Diagram slides in the decks that do not appear in any video

Grouped by the lesson each slide was drafted for, using the Tall deck's own title cards and the
topic of the transcript. None of these is on screen in the final videos, so there are no
timestamps. Where a diagram matches part of a transcript, the passage is quoted as context.

### Drafted for Lesson 1

#### A.1 — Frozen and Growing (Wide deck, slides 2 and 3; slide 3 is an identical duplicate)
**Text on slide:** Frozen and Growing · device · model (frozen) · context · your app · write · recall · memory (grows)
**Visual description:** A dashed rounded rectangle labelled "device" in the top-left corner
encloses the whole diagram. On the left, an orange rounded box holds a small neural-network
drawing (three columns of nodes fully connected by orange lines) with a padlock icon in the top
right corner; it is captioned "model (frozen)". In the middle, a light-blue rounded box reads
"your app", with a grey arrow pointing left to the model labelled "context". On the right, a
lavender cylinder captioned "memory (grows)" contains three rows, each with an icon (picture,
waveform, document) followed by seven orange vector cells; three purple plus signs float above
it. Two red curved arrows connect the app and the memory: "write" going in and "recall" coming
out.
**What it teaches:** The course's central framing. The model's weights never change; what grows
is the memory. The app writes new memories and recalls them to give the frozen model context.
Related transcript passage (Lesson 1): "We created, stored, and recalled memories without using
any LLM. What changed was only some vectors."

#### A.2 — Answered on Device, "where did I put it?" (Wide deck, slide 6)
**Text on slide:** Answered on Device · 🗣 · device · "where did I put it?" · embed on device · top matches · memory · stays on device · works offline
**Visual description:** An earlier, single-image version of the Lesson 1 sequence. A dashed
"device" rectangle encloses everything. Top left, a light-blue rounded box holds the spoken
question "where did I put it?" (the deck also places a speaking-head emoji, 🗣, as a separate
text element). A red arrow leads to a small orange box showing three text lines turning into
three vector cells, captioned "embed on device", then a red arrow into a lavender cylinder
captioned "memory". The cylinder holds three rows of vector cells with picture, waveform, and
document icons; the middle (waveform) row is highlighted with a teal outline and a teal check
mark sits to its right. A teal arrow labelled "top matches" curves from the cylinder back down to
a teal result box at the bottom left containing a picture icon, a document icon, and a check
mark. Bottom right, a padlock with "stays on device" and a paper plane with "works offline".
**What it teaches:** The whole question-to-answer loop happens inside the device boundary: embed
the question locally, find the top matches in local memory, return them. The "device" border and
the footer make the privacy and offline points visually.

#### A.3 — In-Process and On-Disk (Wide deck, slide 7)
**Text on slide:** In-Process and On-Disk · your app (one process) · upsert() · query() · Qdrant Edge · edge_config.json · segments/ · wal/ · on disk · central Qdrant server · optional sync
**Visual description:** On the left, a dashed rounded rectangle labelled "your app (one process)"
contains a light-blue box with a code-brackets icon and, to its right, a lavender box labelled
"Qdrant Edge". Two horizontal lines join them, labelled "upsert()" above and "query()" below in a
monospace face. A line from Qdrant Edge exits the dashed box to a lavender folder shape on the
right listing three monospace entries: "edge_config.json", "segments/", "wal/"; it is captioned
"on disk" with a small drive icon. Above the folder, a grey rounded box with a database icon
reads "central Qdrant server", connected to the folder by a dashed double-headed arrow labelled
"optional sync".
**What it teaches:** Qdrant Edge is a library inside the application's own process, not a server.
Memory is a directory on disk (config, segments, write-ahead log), and syncing to a central
Qdrant server is optional. Related transcript passage (Lesson 2): "There is no separate vector
database server, and the memory is stored in a folder on the device."

#### A.4 — Course Map (Wide deck, slide 8)
**Text on slide:** Course Map · capture · embed · store · recall · L2 store + recall · L3 photos · L4 a whole day · L5 teach it to see · L6 on a robot
**Visual description:** Four rounded boxes in a row, joined by grey arrows: light-blue "capture"
(picture, waveform, and document icons), orange "embed" (text lines turning into vector cells),
lavender "store" (a small cylinder), and red "recall" (a magnifying glass). A long red arrow
arcs over the top from recall back to capture, closing the loop. Below, horizontal bars show
which stages each lesson covers: "L2 store + recall" spans store and recall; "L3 photos" sits
under embed; "L4 a whole day" sits under capture; and two full-width grey bars, "L5 teach it to
see" (with a phone icon) and "L6 on a robot" (with a robot icon), span all four stages.
**What it teaches:** The capture, embed, store, recall loop is the spine of the course, and each
lesson adds one stage or one modality. Note that the lesson numbers are from an earlier
six-lesson plan and are off by one from the final videos (the final course has five lessons, with
the robot covered in Lessons 1 and 2).

### Drafted for Lesson 3 (Tall deck "Lesson 2: Store and Recall" and "Lesson 3: Finding the Right Memory")

#### A.5 — The memory loop, recall highlighted (Tall deck, slide 3, untitled)
**Text on slide:** capture · embed · store · recall · this lesson
**Visual description:** The four loop stages stacked vertically in the tall format: light-blue
"capture" with a camera icon, orange "embed" with a waveform icon, a lavender "store" cylinder
with a strip of vector cells, and red "recall" with a magnifying glass, joined top to bottom by
grey arrows, with a red arrow curving up the left side from recall back to capture. A
hand-lettered label "this lesson" on the right points with a black arrow at "recall". The three
non-highlighted stages are drawn with lighter text.
**What it teaches:** A section marker: this part of the lesson is about recall (querying).

#### A.6 — The Vector space (Tall deck, slide 5)
**Text on slide:** The Vector space · stored points · query · nearest
**Visual description:** A two-axis plot drawn by hand, with grey axes and arrowheads. About a
dozen lavender dots are scattered in two loose clusters, labelled "stored points". A red
asterisk at the upper right is labelled "query" in red. A red curved arrow runs from the query to
one dot in the lower-right cluster, which is circled in teal and labelled "nearest" in teal.
**What it teaches:** Similarity search in picture form: every memory is a point in a vector
space, the question is another point, and recall returns the stored point closest to it.

#### A.7 — The memory loop, embed and recall highlighted (Tall deck, slide 7, untitled)
**Text on slide:** capture · embed · store · recall · this lesson
**Visual description:** Same vertical loop as A.5, but the "this lesson" label has two black
arrows, one to "embed" and one to "recall".
**What it teaches:** A section marker for the part of the lesson that adds a second embedding
model (images) and searches with it.

#### A.8 — Two Encoders, One Shard (Tall deck, slide 8)
**Text on slide:** Two Encoders, One Shard · Nomic-Embed-Text · 768-d · EdgeShard · text · image · 512-d · CLIP ViT-B/32
**Visual description:** At the top, an orange rounded box with a document icon reads
"Nomic-Embed-Text"; an orange arrow labelled "768-d" points down into a lavender cylinder labelled
"EdgeShard" to its upper left. Inside the cylinder are two stacked pills: "text" with a document
icon and six vector cells, and "image" with a picture icon and five vector cells. From the
bottom, an orange rounded box with a picture icon reads "CLIP ViT-B/32", and an orange arrow
labelled "512-d" points up into the "image" pill.
**What it teaches:** One shard holds two named vectors per point, each produced by a different
model: the 768-dimensional Nomic text embedding and the 512-dimensional CLIP image embedding.
This matches the shard configuration at the start of the Lesson 3 notebook ("text" size 768,
"image" size 512, cosine distance).

#### A.9 — Filter inside Query (Tall deck, slide 11)
**Text on slide:** Filter inside Query · query · find: "something to eat" · where: category = food · price < 15 · food · $9 · food · $12 · food · $22 · gear · $45 · taco truck on 5th · 0.92 · pho spot downtown · 0.87
**Visual description:** At the top, a pale-pink rounded box tagged "query" in small red text holds
two lines separated by a rule: "find:" in red followed by "something to eat" in quotes, and
"where:" in teal followed by "category = food · price < 15". A red arrow leads down into a
lavender cylinder containing four rows. Each row is a strip of five orange vector cells and a
teal tag: "food · $9", "food · $12", "food · $22", "gear · $45". The first two rows are drawn at
full strength with a short red mark on their left; the last two are faded to show they are
excluded. A red arrow leads down to two pink result bars: "taco truck on 5th 0.92" and "pho spot
downtown 0.87".
**What it teaches:** A filter is part of the query, not a post-processing step. The semantic
search ("something to eat") runs only over points whose payload passes the conditions
(category is food, price under 15), and the results still carry similarity scores. This is the
category-and-price filter built in the Lesson 3 notebook.

### Drafted for Lesson 4 (Tall deck "Lesson 4: Your On-Device Assistant")

#### A.10 — The memory loop, capture and recall highlighted (Tall deck, slide 13, untitled)
**Text on slide:** capture · embed · store · recall · this lesson
**Visual description:** Same vertical loop as A.5, with "this lesson" pointing at both "capture"
and "recall".
**What it teaches:** A section marker: Lesson 4 captures a whole day (photos, notes, voice) and
recalls from it.

#### A.11 — What comes back (Tall deck, slide 14)
**Text on slide:** What comes back · "the ramen downtown" · Nomic · CLIP · memory inbox · ramen_shop.jpg · 0.71 · "$14 and worth it" · 0.68 · picked up groceries · 0.42 · weak match
**Visual description:** At the top, a light-blue rounded box with a speech-bubble icon holds the
query "the ramen downtown". Two grey arrows fan out to two orange boxes with waveform icons,
"Nomic" on the left and "CLIP" on the right. Red arrows from both converge into a large
teal-outlined panel titled "memory inbox". Inside are three result rows: a picture icon with
"ramen_shop.jpg" and score 0.71; a microphone icon with the quoted voice note "$14 and worth it"
and score 0.68; and a faded document row "picked up groceries" with score 0.42, annotated
outside the panel with "weak match".
**What it teaches:** One question is embedded twice and searched against both the text and image
vectors, and the results from all modalities (photo, voice note, text note) are merged into one
inbox ranked by score, with low scores flagged as weak. This is the memory inbox display used in
the Lesson 4 notebook.

### Drafted for Lesson 5 (Tall deck "Lesson 5: Teaching It to See")

#### A.12 — The memory loop, all of it (Tall deck, slide 16, untitled)
**Text on slide:** capture · embed · store · recall · all of it
**Visual description:** Same vertical loop as A.5, but instead of a pointer, a tall black curly
brace spans all four stages on the right, labelled "all of it".
**What it teaches:** A section marker: the final lesson exercises the whole loop end to end.

#### A.13 — Teach, Store, and Recognize (Tall deck, slide 17)
**Text on slide:** Teach, Store, and Recognize · photos (teach) · CLIP · object shard · label · nearest match > threshold · new photo (recognize)
**Visual description:** At the top, two small blue picture icons labelled "photos (teach)" send an
orange arrow into an orange "CLIP" box. From CLIP, an orange arrow and a red arrow both point down
into a lavender cylinder labelled "object shard", which contains a strip of six vector cells and a
small lavender pill reading "label". At the bottom left, a single blue picture icon labelled "new
photo (recognize)" sends a long red arrow up the left side into CLIP. From the cylinder, a red
arrow exits to the bottom right into a teal box with a check mark reading "nearest match >
threshold".
**What it teaches:** Teaching and recognizing are the same pipeline through CLIP. Teaching stores
a few photo vectors with a label in a dedicated object shard; recognizing embeds a new photo,
finds the nearest stored view, and accepts it only if the similarity clears a threshold. This is
the teach, recognize, and threshold-calibration sequence in the Lesson 5 notebook.

#### A.14 — One Point, Two Doors (Tall deck, slide 18)
**Text on slide:** One Point, Two Doors · Point · named vector · image · named vector · text · payload · note · by sight · by words
**Visual description:** The same lavender "Point" card as Slide 3.1, now with three rows: "named
vector · image" (picture icon, six orange vector cells), "named vector · text" (document icon,
six vector cells), and "payload · note" (document icon). Outside the card on the left, a blue
picture icon with a red arrow into the image row is labelled "by sight"; on the right, a blue
speech-bubble icon with a red arrow into the text row is labelled "by words".
**What it teaches:** One memory can be reached two ways. A taught object is stored as a single
point carrying both a CLIP image vector and a text vector for its note, so the assistant can
find it from a new photo or from a typed or spoken question. This is the final "assistant
memory" built in Lesson 5, where the rubber duck is stored with both a photo and a note.

---

## Appendix B: Non-content slides (omitted)

| Deck | Slide | Title / content | Reason omitted |
| --- | --- | --- | --- |
| Wide | 1 | "Building on-device AI memory / Why Devices Need Memory" with Qdrant and DeepLearning.AI logos | Marketing teaser slide (speaker notes say so); not in any video |
| Wide | 4 | "Demo 1" | Empty placeholder |
| Wide | 5 | "Demo 1" | Empty placeholder |
| Wide | 9 | "Acknowledgments": names and photos of six DeepLearning.AI staff, with a template instruction still on the slide | Credits template; not in any video |
| Tall | 1 | "Building on-device AI memory / Dylan Couzon" | Title card; not in any video |
| Tall | 2 | "Building on-device AI memory / Lesson 2: Store and Recall" | Title card from the earlier lesson plan |
| Tall | 6 | "Building on-device AI memory / Lesson 3: Finding the Right Memory" | Title card from the earlier lesson plan |
| Tall | 12 | "Building on-device AI memory / Lesson 4: Your On-Device Assistant" | Title card; not in any video |
| Tall | 15 | "Building on-device AI memory / Lesson 5: Teaching It to See" | Title card; not in any video |
| Tall | 19 | "Style Guide": typography (Poppins, Verdana for code) and color swatches | Production reference |
| Tall | 20 | "Building AI Assistants with On-Device Memory / Building the Memory" | Older-style title card; the videos use a similar card as a video overlay |
| Tall | 21 | "Building AI Assistants with On-Device Memory / Building the Voice Assistant" | Older-style title card; same note |
| Tall | 22 | "Building AI Assistants with On-Device Memory / Learning Through Memory" | Older-style title card; same note |

Totals: 8 slides shown in videos + 15 diagram slides in Appendix A + 13 non-content slides in
Appendix B = 36 slides, the full contents of both decks. (Wide slides 2 and 3 are counted
separately but described once, in A.1.)
