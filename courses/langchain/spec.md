# Spec: Ask your documents (question answering over a document collection)

**What you're building:** a program that answers your plain-language questions about your own collection of documents, using the few pieces of the collection most similar in meaning to each question. By default it answers questions about a small sample outdoor-clothing product catalog. You ask "Please suggest a shirt with sunblocking". It finds the four catalog entries closest in meaning, writes an answer from only those entries, and says it doesn't know when they lack the answer. It can also grade itself on a set of example questions, and it has a switch that shows you what happened inside one answer.

**What the recommended build needs to run:** an OpenAI API key (for the answering model and for the embeddings) and network access to OpenAI.

**Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once `OPENAI_API_KEY` is set and are skipped until then; that is not a failure.

This file is self-contained: everything the build needs is in it.

*Provenance: from the course "LangChain for LLM Application Development" (materials used: lesson transcripts 1–8, the course notebooks, 13 slide images, and the owner-confirmed pattern card). Generated 2026-11-03 with guide v2.9 (2026-10-31).*

---

## 0. Before you build — REQUIRED (do this first)

You are the build agent. Before writing ANY code, you MUST ask the person you are building for
the questions in the next section. Do not skip this because the recommended answers look
complete: they exist so the build is reproducible, not because they fit this person's project.

1. **Use a structured question tool if you have one** (e.g. Claude Code's `AskUserQuestion`);
   otherwise list the question in your reply and ask.
2. **First question — recommended build, or choose?** Two options: the **recommended build**
   (every question takes its "(Recommended)" option — mostly the course's own choices, with a
   lighter stand-in wherever the course's choice needs setup the person may not have; the
   checklist in step 5 marks each place it differs from the course; to run for real it needs
   an OpenAI API key and network access to OpenAI), or **choose** question by
   question. Recommended → go to step 5. Choose → step 3.
3. **Ask ONE question at a time.** Show the question, its options with their "pick this when …"
   and setup cost, and the labels "(course default)" / "(Recommended)" /
   "(Recommended - course default)" exactly as written — no other labels. Say once, before the
   first question, that "(Recommended)" was fixed when this spec was written and does not
   reflect this person's setup. Use earlier answers to explain later options in the person's
   own terms, but never drop or change an option because of them. Skip a question only when its
   own "Ask only when …" condition is false, and say so in one line. A per-call limit of your
   question tool is never a reason to skip, merge or default a question.
4. **Asking ends your turn.** Write no code and touch no file until the person answers. Keep
   asking until every question is answered or skipped by its condition. Answers to some
   questions do not release the build; no reply is not an answer.
5. **Before the first line of code, print a checklist and write it to `resolved-decisions.md`:**
   every question with the chosen option's id and text, each marked `= course choice`,
   `≠ course choice (course used: <option>)`, `no course choice`, or `not asked (<condition>)`.
   Add one line per model role naming the current model you will use from the chosen provider;
   if you cannot tell, ask, and otherwise use the course's own model id and say it may need
   changing. For every chosen option that is not recommended, copy its "what to check" sentence
   into the checklist. On the recommended path, walk the person through every `≠` line and its
   reason. Start building only after the checklist is shown, written and confirmed. Leave out
   every part of the spec that exists only for an option not chosen.

---

## 1. Questions
C1–C4 are context questions (your collection, its file format, your model provider, how you use the program); C5–C10 follow the program's stages in order (split, embed, store, combine and answer, evaluate, see inside).

### C1. Which collection of documents should the program answer questions about?
- **C1a (Recommended - course default): The sample product catalog.** A small outdoor-clothing catalog, written for this spec, with one entry per product; every test runs against it. *Pick this when* you want a working copy of the course's program first and can point it at your own documents later. *Setup:* none.
- **C1b: Your own collection.** The program indexes the documents you name (a folder or a file) instead of the sample catalog; the sample catalog stays for the tests. *Pick this when* you already have a set of documents you want answers from, such as your notes, a manual or a team's internal pages. *Setup:* none beyond having the files.
  - *What to check:* each of your documents shows up as at least one stored piece that names its source file, and a question about a fact found in only one document gets that document among the four retrieved pieces.

### C2. What form are your documents in?
*Ask only when C1 is C1b.*
- **C2a (Recommended - course default): A table file, one row per document.** Each row of a CSV file becomes one document whose text is every column written as "column: value". *Pick this when* your collection is a list of similar records, such as products, contacts or tickets. *Setup:* none.
- **C2b: Plain-text or Markdown files.** Each file in a folder becomes one document. *Pick this when* your collection is notes or pages you wrote yourself. *Setup:* none.
  - *What to check:* every .txt or .md file in the folder becomes a document whose text equals the file's text and whose source is the file name.
- **C2c: PDF files.** The text of each PDF in a folder is extracted and becomes one document. *Pick this when* your collection is reports, papers or manuals you received as PDFs. *Setup:* a PDF text-extraction package.
  - *What to check:* every PDF in the folder becomes a document whose text contains a sentence you copy from that PDF and whose source is the file name.

### C3. Which provider's language model writes the answers?
- **C3a (Recommended - course default): OpenAI chat model.** Answers, evaluation examples and grades come from an OpenAI chat model. *Pick this when* you have, or can get, an OpenAI API key; the same key also serves the recommended embeddings (C6a). *Setup:* an OpenAI API key, billed per token.
- **C3b: Another hosted provider.** The same three model roles use a chat model from a provider you already pay for. *Pick this when* your organisation already has a key for another provider and not for OpenAI. *Setup:* that provider's API key and its integration package.
  - *What to check:* with that provider's key set, the sunblocking sample question returns an answer that names the Breezeway Sun Shirt.
- **C3c: A local model on your machine.** The model runs on your own computer through a local model server. *Pick this when* your documents must not leave your machine or you have no paid key. *Setup:* a local model server and a model download of several gigabytes; answers are slower on a machine without a strong graphics card.
  - *What to check:* with no hosted-provider key set, the sunblocking sample question is answered by the local model and names the Breezeway Sun Shirt.

### C4. How do you want to ask questions?
- **C4a (Recommended): From the command line.** You type a question in a terminal command and the answer is printed. *Pick this when* you are the only user and are happy in a terminal. *Setup:* none.
- **C4b: In a small web page on your machine.** A local page with a question box shows the answer and the pieces it rests on. *Pick this when* someone who does not use a terminal will ask the questions. *Setup:* a small web-framework package; the page runs locally only.
  - *What to check:* asking the sunblocking sample question in the page shows the same answer and the same four retrieved pieces as the command line does.

### C5. Should long documents be cut into smaller pieces before they are indexed?
- **C5a (Recommended - course default): No cutting; each document is one piece.** Every document is embedded and stored whole. *Pick this when* each document is short, like a product entry or a short record; cutting would only split facts that belong together. *Setup:* none.
- **C5b: Cut long documents into overlapping pieces.** Each document longer than the piece size is cut into overlapping pieces, each embedded and stored on its own. *Pick this when* your documents are long (notes, manuals, reports): a whole long document may not fit in what the model can read at once, and small pieces let only the relevant parts reach the model. *Setup:* none.
  - *What to check:* each piece remembers which document it came from, and the pieces of one document together hold the whole document.

### C6. What turns each piece of text into its numeric meaning (its embedding)?
- **C6a (Recommended - course default): OpenAI embeddings.** Each piece and each question is embedded by OpenAI's embedding service. *Pick this when* you are using an OpenAI key anyway (C3a). *Setup:* the OpenAI API key; billed per token and documents are sent to OpenAI.
- **C6b: A local embedding model.** An embedding model runs inside the program on your machine. *Pick this when* you have no OpenAI key (for example with C3b or C3c) or your documents must not leave your machine. *Setup:* an embedding package and a model download of a few hundred megabytes.
  - *What to check:* with no OpenAI key set, indexing the sample catalog and asking the sunblocking question works, and the four retrieved pieces include both the Breezeway Sun Shirt and the Trailmark Hiking Shirt.

### C7. Where are the pieces and their embeddings kept?
- **C7a (Recommended - course default): In memory, rebuilt at each start.** The store lives inside the running program and is rebuilt from the documents every time it starts. *Pick this when* your collection is small enough to re-embed in seconds; it needs no database of any kind and is the easiest to start with. *Setup:* none.
- **C7b: Saved to a file on your disk.** The store is written to disk after indexing and loaded at the next start. *Pick this when* your collection is large enough that re-embedding at every start is slow or costs noticeable embedding fees. *Setup:* an embedded vector-store package.
  - *What to check:* after a restart, questions are answered without embedding the documents again (the embedder is called only for the question), and the loaded store holds the same pieces as before.
- **C7c: A vector database server or hosted service.** The store lives in a separate database that several programs can share. *Pick this when* several people or programs must query one large collection. *Setup:* a database container or a hosted account and its key.
  - *What to check:* after indexing, the database holds one entry per piece with its text, embedding and source, and a second program instance answers the sunblocking question without indexing again.

### C8. How are the retrieved pieces given to the model to write the answer?
- **C8a (Recommended - course default): All in one prompt ("stuff").** The retrieved pieces are put into a single prompt with the question and the model is called once. *Pick this when* the retrieved pieces are few and short; it is the simplest, cheapest and most common method and the model sees all pieces at once, but a prompt bigger than the model can read will not work. *Setup:* none.
- **C8b: Answer per piece, then combine ("map-reduce").** The model answers the question from each piece separately, then one more call combines those answers into the final one. *Pick this when* you retrieve many pieces or long ones; it works over any number of pieces and the per-piece calls can run in parallel, but it makes many more calls and treats the pieces as independent. *Setup:* none.
  - *What to check:* for the sunblocking question the model is called once per retrieved piece and once more to combine, and the answer is the combining call's reply.
- **C8c: Build the answer piece by piece ("refine").** The model reads the pieces one after another, improving the answer from the previous piece each time. *Pick this when* the answer must combine information spread across pieces; answers tend to be longer, and it is slower because each call waits for the one before, with as many calls as map-reduce. *Setup:* none.
  - *What to check:* the model is called once per retrieved piece in order, every call after the first receives the previous answer, and the last call's reply is the answer.
- **C8d: Answer per piece with a score, keep the best ("map-rerank").** The model answers from each piece separately and gives each answer a score; the highest-scoring answer is returned. *Pick this when* one piece is likely to hold the whole answer; it is experimental, depends on telling the model clearly how to score, and makes one call per piece. *Setup:* none.
  - *What to check:* the model is called once per retrieved piece, each reply carries a numeric score, and the answer is the reply with the highest score.

### C9. How does the program check the quality of its answers?
- **C9a (Recommended - course default): Hand-written plus model-written examples, graded by a model.** An evaluation command runs a few hand-written question–answer pairs plus pairs a model writes from documents through the program, and a grading model marks each answer correct or incorrect by meaning. *Pick this when* you will change the program (model, retrieval, settings) and want to know whether it got better or worse; writing examples by hand is slow, so a model writes most of them. *Setup:* none beyond the model key; each run costs model calls.
- **C9b: Hand-written examples only, graded by a model.** The same evaluation, but only with question–answer pairs you write yourself. *Pick this when* you want full control over every test question, or your documents are too few for generated questions to add anything. *Setup:* none beyond the model key.
  - *What to check:* the evaluation runs exactly the hand-written examples and makes no example-writing model calls.
- **C9c: No evaluation.** The program only answers questions. *Pick this when* you want a personal question tool and will judge answers yourself as you read them. *Setup:* none.
  - *What to check:* the program has no evaluation command and every remaining test passes.

### C10. How do you see what happened inside one answer?
- **C10a (Recommended - course default): A debug switch that prints every step.** When switched on, the program prints the question, the retrieved pieces, the full prompt sent to the model, the model's reply and the token counts. *Pick this when* you want to find out why an answer is wrong; often the retrieval step, not the model, is at fault. *Setup:* none.
- **C10b: A hosted run dashboard.** Every run is recorded to a hosted tracing service, where you click down through each step and can save questions and answers into an example set for evaluation. *Pick this when* a team wants runs kept and browsable over time and wants to grow an evaluation set from real questions. *Setup:* a hosted account and its API key; questions and documents are sent to that service.
  - *What to check:* after one question is asked, the run appears in the dashboard with the question, the retrieved pieces, the prompt and the reply.

## 2. Departures from the course

| # | Where | Course did | This spec does | Why |
|---|---|---|---|---|
| D1 | Library versions | Pinned `langchain==0.0.179` and `openai==0.27.7` | Current releases | Course-era versions often no longer install or work with current models. |
| D2 | Models | `gpt-3.5-turbo` (`gpt-3.5-turbo-0301` before 2024-06-12); `gpt-3.5-turbo-instruct` for the one-line index query | The build agent picks a current model per role at the checklist | Model names go stale; the course's own note says one of its models was deprecated. |
| D3 | Program form | Notebook cells, answers rendered as Markdown in the notebook | A command-line program with `ask` and `eval` commands (C4 can change this) | The build is a program, never a notebook. |
| D4 | Sample data | A 1000-row outdoor clothing catalog CSV | An 8-row outdoor clothing catalog with facts written for this spec | No course data is copied; a small catalog keeps every outcome checkable by hand. |
| D5 | Offline tests | None; every call went to OpenAI | Scripted stand-in model and a stand-in embedder, labelled as stand-ins (addition) | Tests must run offline with exact outcomes. |
| D6 | One-line index shortcut | Built the same index two ways: a one-line index creator and step by step | One indexing path | The course says both give the same result; one path is enough. |
| D7 | Hosted evaluation platform | Shown in the video for viewing runs and building example sets | Left out of the recommended build; offered as C10b | It needs a hosted account; the debug switch already shows each step. |
| D8 | Grade values | The grader's text was printed as returned | Grades are normalised to `CORRECT` or `INCORRECT` (addition) | A fixed value set makes the report and tests exact. |
| D9 | Missing-key message, stand-in switch | Not present | Added (R10) | Lets the offline tests run without a key and gives a clear error without one. |

---

## 3. Objective
Index a collection of documents by meaning, then answer each plain-language question from the four stored pieces most similar in meaning to it, saying "I don't know" when those pieces lack the answer, and grade the program on example questions.

## 4. Tech stack, versions and secrets
- Python 3.11 or newer; the current release of LangChain and its OpenAI integration (the framework the course teaches); pytest for tests. Use current releases throughout; pin nothing that the course pinned (D1).
- Where this spec leaves a behaviour to the framework (how the one-prompt answer chain formats its prompt, retries, how a parsed reply is produced), keep the current release's behaviour and note in `resolved-decisions.md` how the release provides it.
- Package name `docqa` (importable). Commands: `python -m docqa ask "<question>" [--debug]`, `python -m docqa eval`.
- Secrets: `OPENAI_API_KEY` read from the environment or a local `.env` file; never written to code, logs or the debug output. `.env` is listed in `.gitignore`.
- `DOCQA_STANDINS=1` makes the program use the stand-in model and stand-in embedder of section 8 instead of real providers (addition, for tests and demos).

## 5. Input/output contracts

**Catalog file (`sample_data/catalog.csv`)**: CSV with header `id,name,description`.

**Piece** (one per document under C5a):
```json
{
  "type": "object",
  "required": ["piece_id", "text", "vector", "source"],
  "properties": {
    "piece_id": {"type": "string", "pattern": "^[A-Za-z0-9_-]+$"},
    "text": {"type": "string", "minLength": 1, "description": "For a CSV row: each column as 'column: value', one per line, in header order"},
    "vector": {"type": "array", "items": {"type": "number"}, "minItems": 1},
    "source": {
      "type": "object",
      "required": ["file", "row"],
      "properties": {"file": {"type": "string"}, "row": {"type": ["integer", "null"], "minimum": 0}}
    }
  }
}
```

**Answer record** (what `ask` produces; printed as the answer text, full record available to tests):
```json
{
  "type": "object",
  "required": ["question", "answer", "retrieved"],
  "properties": {
    "question": {"type": "string", "minLength": 1},
    "answer": {"type": "string"},
    "retrieved": {
      "type": "array", "maxItems": 4,
      "items": {"type": "object", "required": ["piece_id", "score"],
                "properties": {"piece_id": {"type": "string"}, "score": {"type": "number"}}},
      "description": "Most similar first"
    }
  }
}
```

**Evaluation example**: `{"query": string (minLength 1), "answer": string, "origin": "hand" | "generated"}`.

**Evaluation result** (one per example, in `eval` output):
```json
{
  "type": "object",
  "required": ["query", "real_answer", "predicted_answer", "grade"],
  "properties": {
    "query": {"type": "string"},
    "real_answer": {"type": "string"},
    "predicted_answer": {"type": "string"},
    "grade": {"enum": ["CORRECT", "INCORRECT"]}
  }
}
```
The `eval` output ends with a totals line: `CORRECT: <n>  INCORRECT: <m>`.

**Model roles**
- **Answerer:** writes the answer from the question plus retrieved pieces.
- **Example writer:** writes one question–answer pair from one document (C9a only).
- **Grader:** decides whether a predicted answer means the same as the real answer.
- **Embedder:** turns each piece and each question into a vector (an embedding model, not a chat model).

**Settings**

| Setting | Value | Source | Change this when … |
|---|---|---|---|
| `top_k` (pieces retrieved per question) | 4 | Course: the similarity search "returns four documents" (L5); the course never set it, this is the framework's default it ran with | your pieces are tiny or answers need more pieces; keep it small enough that the prompt fits the model |
| `answer_temperature` | 0.0 | Course: answer model built with temperature 0.0 (L5 notebook); instructor: "When I'm building applications, one thing I will often do is set the temperature parameter to be equal to zero" (L2) | you want more varied wording; answers will vary run to run |
| `grader_temperature` | 0.0 | Course: grading model built with temperature 0 (L6 notebook) | rarely; grades should be repeatable |
| `example_writer_temperature` | framework default (not set) | Course: the example-writing model was built without a temperature (L6 notebook); the instructor said the default was 0.7 (L2) | you want more or less varied generated questions |
| `piece_separator` | `<<<<>>>>>` | Course: final question-answering chain in L6 set this separator; L5 left it at the framework default | your documents contain that string |
| `examples_from_first_n_docs` | 5 | Course: example pairs generated from the first five documents (L6 notebook) | your collection is larger and you want more examples |
| `debug` | off | Course: debug turned on for one run, then off (L6 notebook) | you are investigating one answer |
| `chunk_size`, `chunk_overlap` (C5b only) | 1000 characters, 100 characters (addition) | Not set by the course; the course did not cut its short documents | your documents are much shorter or longer than a page |

## 6. Business rules

**What must stay true** (the course's pattern card; every option keeps every item):
- **M1. The documents are indexed by meaning before any question.** Each piece of text gets a numeric representation of its meaning, stored next to its original text, so pieces with similar meaning can be found later. → T1, T2
- **M2. For each question, only the few stored pieces most similar in meaning are retrieved, not the whole collection.** → T3, T4, T12
- **M3. A language model writes the answer from the question plus the retrieved pieces, so the answer rests on the person's documents.** → T5, T12

**Rules of the recommended build**
- **R1. Indexing.** Before the first question, every document becomes exactly one piece (C5a) whose text is its columns written as `column: value` lines in header order, whose vector comes from the embedder, and whose source names the file and row (0-based). The store starts empty. → T1, T2
- **R2. Retrieval.** The question is embedded with the same embedder; it is compared with every stored vector by cosine similarity (a zero vector scores 0); the `top_k` most similar pieces are returned most similar first; equal scores keep catalog order. The rest of the collection is never sent to the model. → T3, T4, T6, T12
- **R3. Answering.** The answerer is called once per question (C8a) with a prompt that contains, in order: the instruction "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer.", the retrieved pieces' texts joined by `piece_separator`, and the question. The answer is the model's reply, unchanged. → T4, T5, T12
- **R4. Saying it does not know.** When the retrieved pieces do not hold the answer, the program returns the model's "don't know" reply as the answer and adds no answer of its own. → T6, T13
- **R5. Evaluation examples.** The example set is the hand-written examples followed by one generated example per document for the first `examples_from_first_n_docs` documents, in document order. Each generated reply is parsed into a `{query, answer}` record. → T7
- **R6. Evaluation run.** `eval` runs each example's query through the same ask path as R2–R3 and records the reply as the predicted answer. → T8
- **R7. Grading by meaning, never by string match.** Each prediction is graded by the grader model given the query, the real answer and the predicted answer. The grade is `CORRECT` when the reply's first word, uppercased, is `CORRECT`, otherwise `INCORRECT`. The program never compares the real and predicted answers as strings. → T8, T9
- **R8. Report.** `eval` prints, per example: question, real answer, predicted answer, grade; then the totals line. → T8
- **R9. Debug switch.** With `--debug`, `ask` additionally prints the question, each retrieved piece's id, score and text, the full prompt sent to the answerer, the reply, and the token counts when the provider reports them. Without it, `ask` prints only the answer. → T10
- **R10. Keys (addition).** With `DOCQA_STANDINS=1` no key is read and no network call is made. Without it and without `OPENAI_API_KEY`, `ask` and `eval` exit with a non-zero status and a message naming `OPENAI_API_KEY`. → T11

## 7. Tests

### 7.1 Sample data

**`sample_data/catalog.csv`** (facts written for this spec; quoted CSV, header `id,name,description`):

| id | name | description |
|---|---|---|
| P1 | Breezeway Sun Shirt | Lightweight long-sleeve shirt with UPF 50+ sun protection. Fabric: 100% recycled polyester. Has two chest pockets. |
| P2 | Trailmark Hiking Shirt | Short-sleeve top with UPF 30 sun protection. Fabric: nylon. Weight: 6 oz. |
| P3 | Harbor Fleece Pullover | Cozy fleece pullover with side pockets. Fabric: polyester fleece. Weight: 12 oz. |
| P4 | Summit Down Jacket | Insulated hooded jacket from the Alpine collection. Fill: 800-fill goose down. |
| P5 | Riverbend Rain Pants | Waterproof pants with taped seams. Fabric: nylon with waterproof coating. |
| P6 | Canyon Wool Socks | Merino wool hiking socks. Sold in packs of three. |
| P7 | Meadow Sun Hat | Wide-brim hat with UPF 50 sun protection and a chin strap. |
| P8 | Lakeside Cotton Tee | Basic cotton t-shirt for everyday wear. |

Piece ids are the `id` values. Piece text example for P1: `id: P1` / `name: Breezeway Sun Shirt` / `description: Lightweight long-sleeve …` on three lines.

**`sample_data/examples.json`** — the hand-written examples:
- E1: query "Does the Harbor Fleece Pullover have side pockets?", answer "Yes" (planted failure: a correct prediction that does not match this answer as a string).
- E2: query "What collection is the Summit Down Jacket from?", answer "The Alpine collection".

**Stand-in embedder (stand-in for the embedding service; standard library only).** Lowercase the text, split on every character that is not a letter or digit, map each token through this table, count each concept, and return the 14-number count vector in this order (tokens not in the table are ignored):

| # | Concept | Tokens |
|---|---|---|
| 1 | SUN | sun, sunblocking, sunblock, upf, uv |
| 2 | SHIRT | shirt, shirts, tee |
| 3 | POCKET | pocket, pockets |
| 4 | JACKET | jacket, jackets |
| 5 | DOWN | down |
| 6 | RAIN | rain, waterproof |
| 7 | PANTS | pants |
| 8 | WOOL | wool, merino |
| 9 | SOCKS | socks |
| 10 | HAT | hat |
| 11 | FLEECE | fleece, pullover |
| 12 | COLLECTION | collection |
| 13 | KAYAK | kayak, kayaks |
| 14 | HIKING | hiking |

Resulting non-zero counts: P1 SUN 3, SHIRT 2, POCKET 1 · P2 SUN 2, SHIRT 1, HIKING 1 · P3 FLEECE 5, POCKET 1 · P4 JACKET 2, DOWN 2, COLLECTION 1 · P5 RAIN 3, PANTS 2 · P6 WOOL 3, SOCKS 2, HIKING 1 · P7 SUN 3, HAT 2 · P8 SHIRT 2.

**Stand-in model (stand-in for the chat model; scripted).** Every reply is chosen by the first matching row; the answerer matches only against the question part of its prompt.

| Role | When the input contains | Reply |
|---|---|---|
| Answerer | "sunblocking" | "The Breezeway Sun Shirt has UPF 50+ sun protection and the Trailmark Hiking Shirt has UPF 30." |
| Answerer | "side pockets" | "The Harbor Fleece Pullover does have side pockets." |
| Answerer | "What collection" | "The Summit Down Jacket is from the Alpine collection." |
| Answerer | "fabric is the Breezeway" | "The Breezeway Sun Shirt is made of 100% recycled polyester." |
| Answerer | "UPF rating does the Trailmark" | "The Trailmark Hiking Shirt has UPF 30 sun protection." |
| Answerer | "weigh" | "The Harbor Fleece Pullover weighs 12 oz." |
| Answerer | "fill does the Summit" | "The Summit Down Jacket uses 800-fill goose down." |
| Answerer | "seams do the Riverbend" | "The Riverbend Rain Pants have welded seams." (planted wrong answer) |
| Answerer | anything else, including "kayaks" | "I don't know." |
| Example writer | "Breezeway Sun Shirt" | `{"query": "What fabric is the Breezeway Sun Shirt made of?", "answer": "100% recycled polyester"}` (G1) |
| Example writer | "Trailmark Hiking Shirt" | `{"query": "What UPF rating does the Trailmark Hiking Shirt have?", "answer": "UPF 30"}` (G2) |
| Example writer | "Harbor Fleece Pullover" | `{"query": "How much does the Harbor Fleece Pullover weigh?", "answer": "12 oz"}` (G3) |
| Example writer | "Summit Down Jacket" | `{"query": "What fill does the Summit Down Jacket use?", "answer": "800-fill goose down"}` (G4) |
| Example writer | "Riverbend Rain Pants" | `{"query": "What seams do the Riverbend Rain Pants have?", "answer": "Taped seams"}` (G5) |
| Grader | query contains "seams do the Riverbend" | "INCORRECT" |
| Grader | anything else | "CORRECT" |

The stand-in model records every call (role, prompt, settings) so tests can inspect them. It reports no token counts.

### 7.2 Test table

All tests run with `DOCQA_STANDINS=1` unless marked `live`. Scores are cosine similarities, checked to ±0.001.

| Test | Rules | Given | When | Then |
|---|---|---|---|---|
| T1 | R1, M1 | A fresh start | The store is created, then the sample catalog is indexed | Before indexing the store holds 0 pieces; after, 8 pieces with ids P1–P8 |
| T2 | R1, M1 | The indexed sample catalog | Piece P1 is read | Its text is the three lines `id: P1`, `name: Breezeway Sun Shirt`, `description: Lightweight long-sleeve shirt with UPF 50+ sun protection. Fabric: 100% recycled polyester. Has two chest pockets.`; its vector has 14 numbers with SUN 3, SHIRT 2, POCKET 1 and all others 0; its source is `catalog.csv`, row 0 |
| T3 | R2, M2 | The indexed sample catalog | `ask "Please suggest a shirt with sunblocking"` | `retrieved` is P1 (0.945), P2 (0.866), P8 (0.707), P7 (0.588), in that order; answer is "The Breezeway Sun Shirt has UPF 50+ sun protection and the Trailmark Hiking Shirt has UPF 30." |
| T4 | R2, R3, M2 | The same question | The answerer's prompt is inspected | It contains the texts of P1, P2, P8, P7 and none of "Harbor", "Summit", "Riverbend", "Canyon" |
| T5 | R3, M3 | The same question | The answerer's calls are inspected | Exactly one answerer call; the prompt contains the R3 instruction sentence, then the four piece texts separated by exactly three `<<<<>>>>>`, then the question last; temperature 0.0; the returned answer equals the stand-in reply |
| T6 | R2, R4 | The indexed sample catalog | `ask "Do you sell kayaks?"` | `retrieved` is P1, P2, P3, P4, each with score 0 (tie, catalog order); the prompt contains the "If you don't know the answer, just say that you don't know" sentence; the answer is "I don't know." |
| T7 | R5 | The sample catalog and `examples.json` | The evaluation example set is built | 7 examples in order E1, E2, G1, G2, G3, G4, G5; E1–E2 have origin `hand`, G1–G5 origin `generated` with the queries and answers of the stand-in table; the example writer was called 5 times, once each for P1–P5, with no temperature set in its request |
| T8 | R6, R7, R8 | The 7 examples | `python -m docqa eval` | Each example's predicted answer equals the answerer's scripted reply for its query; grades E1, E2, G1, G2, G3, G4 `CORRECT` and G5 `INCORRECT`; the output ends with `CORRECT: 6  INCORRECT: 1`; the grader was called 7 times at temperature 0.0 |
| T9 | R7 | E1 (planted) | E1 is graded during `eval` | The real answer "Yes" and the predicted answer "The Harbor Fleece Pullover does have side pockets." are not equal as strings, the grader's prompt contains both, and the grade is `CORRECT` |
| T10 | R9 | The indexed sample catalog | `ask "Please suggest a shirt with sunblocking"` without and then with `--debug` | Without: the output is only the answer. With: the output also holds the question, the ids P1, P2, P8, P7 with their scores, their texts, the full prompt including the R3 instruction, and the reply |
| T11 | R10 | No `OPENAI_API_KEY` and no `DOCQA_STANDINS` | `python -m docqa ask "Please suggest a shirt with sunblocking"` | Exit status is non-zero, the message names `OPENAI_API_KEY`, and no network call is made |
| T12 `live` | R2, R3, M2, M3 | `OPENAI_API_KEY` set; real embedder and model | `ask "Please suggest a shirt with sunblocking"` | The retrieved pieces include P1 and P2, and the answer names the Breezeway Sun Shirt |
| T13 `live` | R4 | `OPENAI_API_KEY` set | `ask "Do you sell kayaks?"` | The answer says it does not know or that no kayak is listed, and names no product as a kayak |

## 8. Standing permissions
- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in in its code and output; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has data; anything that sends data to a third party (including turning on C10b's hosted dashboard).
- **Never:** invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets.

## 9. Test plan
1. Install: `python -m pip install -e ".[test]"` (dependencies declared in `pyproject.toml`).
2. Offline tests: `python -m pytest -m "not live"` — T1–T11 must pass.
3. Live tests: `OPENAI_API_KEY=… python -m pytest -m live` — T12–T13; skipped without the key, which is not a failure.
4. Manual run: `python -m docqa ask "Please suggest a shirt with sunblocking" --debug` and `python -m docqa eval`.
5. Adjust for the chosen options: leave out tests whose rules exist only for options not chosen (for C9c, leave out T7–T9; for C8b–C8d, T5's "exactly one answerer call" is replaced by that option's check). For each chosen non-recommended option, turn its "what to check" sentence from `resolved-decisions.md` into a test and run it.
6. Report one result per test with evidence (test output, file paths). "Should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.
7. Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

## 10. Background notes

### The program
A program that answers a person's plain-language questions about their own collection of documents, using the few pieces of the collection most similar in meaning to the question. Stages:
`load → (split) → embed → store → retrieve → answer → evaluate`
- **load:** turn the collection into documents with their source, because everything later works on text pieces.
- **split:** cut long documents into pieces, because a model can read only a few thousand words at a time; the course's documents were short, so it skipped this.
- **embed:** give each piece a numeric meaning, because pieces with similar content get similar vectors and can then be compared.
- **store:** keep each vector next to its original text, so a match can return the text.
- **retrieve:** embed the question and pick the n most similar pieces, so only the relevant few reach the model.
- **answer:** the model writes the answer from the question plus those pieces, which combines the model with data it was not trained on.
- **evaluate:** run example questions and grade the answers, so a change (another model, another retrieval setting) can be judged better or worse.
The debug switch is not a stage; it only shows what ran.

### Failures
- **Exact string matching cannot grade answers (demonstrated, L6).** What you see: the real answer "Yes" and the predicted "The Cozy Comfort Pullover Set, Stripe does have side pockets" share no words, yet the answer is right. Why: open-ended answers have many correct wordings. Prevention: a model grades by meaning (R7); planted as E1; tested by T9 (and T8).
- **Made-up answers when the pieces lack the answer (warned, L6).** The course's chain prompt tells the model "If you don't know the answer, just say that you don't know, don't try to make up an answer." The framework's prompt carries this; the spec requires the outcome (R4) and checks it with an unanswerable question (T6, live T13).
- **Wrong answers caused by retrieval (warned, L6).** The instructor: when a wrong result is returned, "it's not necessarily the language model itself that's messing up. It's actually the retrieval step". Prevention: the debug switch shows the retrieved pieces and the full prompt (R9, T10).
- **Results vary between runs (warned, every notebook).** "LLM's do not always produce the same results." Temperature 0 for answering and grading; live tests check content loosely.
- **A deprecated default model (course-era).** The one-line index query defaulted to a completion model deprecated on 1 January 2024; the course swapped in a replacement. The spec does not use that shortcut (D6) and picks models at the checklist (D2).

### Why the questions and settings are what they are
- **C1/C2:** the course's example is one product catalog loaded from a CSV, one row per document; the instructor names other sources (a PDF, a webpage, a company's internal documents). Plain-text and PDF loading are options the learner's data needs.
- **C3/C6:** the course used OpenAI for both the chat model and embeddings; the same key covers both, so the recommended build keeps OpenAI embeddings and offers a local embedder for learners without that key.
- **C4:** the course ran in notebooks; a notebook is never the build, so the recommended interface is the command line, with no course default.
- **C5:** "Because these documents are already so small, we actually don't need to do any chunking here" (L5); chunking is described for big documents "because we may not be able to pass the whole document to the language model" (L5).
- **C7:** the in-memory store was chosen because "it doesn't require connecting to an external database of any kind so it makes it really easy to get started"; the instructor notes "there are many different types of vector stores" and that the store can be swapped.
- **C8:** costs are the instructor's: stuff is simplest, cheapest, works well and is the most common, but the slide says for large or many documents "this will not work as it will result in a prompt larger than the context length"; map-reduce is second most common, works over any number of documents and in parallel, but takes more calls and treats documents as independent; refine builds answers over time, gives longer answers and is slower; map-rerank is "a bit more experimental", relies on the model's scoring and is more expensive. The slide's "will not work" is a stated limit of stuff, not a failure shown, so stuff stays recommended.
- **C9:** hand-written examples "don't really scale that well", so the course generated more with a model; grading uses a model because string matching cannot judge meaning.
- **C10:** the course used the debug flag in the notebook and showed a hosted evaluation platform in the video; the platform needs a hosted account (D7).
- **Not questions:**
  - Exact-string grading — the course shows it failing (5.2 test 2); it is a rule instead (R7).
  - Sending the whole collection to the model, or retrieving by a method other than meaning (the instructor mentions retrievers "some less advanced, some more advanced") — breaks pattern-card items M1/M2 (5.2 test 1).
  - The one-line index creator versus building step by step — the instructor says "these two things equate to the same result"; no learner situation changes what the program does (5.2 test 3).
  - Conversation memory, prompt templates and output parsers, sequential and router chains, agents and tools — other lessons' parts that do not change a stage of this program (background only, per the pattern card).
  - Which model the tests run against — never asked; tests run on the stand-ins, `live` tests when a key is present.
  - `top_k`, temperatures, separator, example count, chunk size — settings (section 5), tuned after the build.
- **Where values came from (course disagreements):** the separator is `<<<<>>>>>` in the L6 final chain and the framework default in L5; picked by the final end-to-end app rule because the instructor never stated one. The course's model id was `gpt-3.5-turbo-0301` before 2024-06-12 and `gpt-3.5-turbo` after (notebook date switch). The example writer had no temperature set; the instructor said the default was 0.7 (L2). The course reports "four documents" retrieved and "seven examples total" (2 hand-written + 5 generated), which the sample data mirrors.

### Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports: `ChatOpenAI` (from `langchain.chat_models`), `OpenAI` (from `langchain.llms`), `OpenAIEmbeddings` (from `langchain.embeddings`), `CSVLoader` (from `langchain.document_loaders`), `DocArrayInMemorySearch` (from `langchain.vectorstores`, with the `docarray` package), `VectorstoreIndexCreator` (from `langchain.indexes`), `RetrievalQA` with `chain_type="stuff"` and `chain_type_kwargs={"document_separator": …}`, `similarity_search`, `as_retriever`, `call_as_llm`, `chain.run` / `chain.apply`, `QAGenerateChain` with `apply_and_parse`, `QAEvalChain` with `evaluate`, `langchain.debug`; models `gpt-3.5-turbo`, `gpt-3.5-turbo-0301`, `gpt-3.5-turbo-instruct`, `text-davinci-003`; versions `langchain==0.0.179`, `openai==0.27.7`. Some current model families reject a `temperature` parameter: if the chosen model does, keep the setting configured, leave it out of that model's request, and record this in `resolved-decisions.md`.

### Course names
| Course name | Spec term | Binding? |
|---|---|---|
| document / chunk | document / piece | no |
| vector store / vector database / index | store | no |
| `k` / "n most similar" | `top_k` | the value 4 is binding |
| "stuff", "map_reduce", "refine", "map_rerank" | C8a–C8d | no |
| `document_separator` | `piece_separator` | the value is binding |
| `query`, `answer` (example keys) | `query`, `answer` | yes (example contract) |
| `result` (predicted answer) | `predicted_answer` | no |
| `OutdoorClothingCatalog_1000.csv` | `sample_data/catalog.csv` | no |

### Lesson map
Transcript numbering (the notebooks count one lower from lesson 2 on):
- L1 Introduction — framework overview only.
- L2 Models, Prompts and parsers — temperature habit and default (settings); output parsing (background).
- L3 Memory — background only (pattern card).
- L4 Chains — background only.
- L5 Question and Answer — the program's stages, in-memory store, OpenAI embeddings, four retrieved pieces, no chunking for short rows, the four combining methods (C5–C8), the one-line index (D6).
- L6 Evaluation — final end-to-end version: separator, hand-written and generated examples, model grading, the string-matching failure, the "don't know" prompt, debug switch, hosted platform (C9, C10, R4–R9).
- L7 Agents — background only.
- L8 Conclusion — nothing used.
Slides read: question_and_answer 1–7 (L5; talked through by the instructor, counted like the transcript; 6 and 7 show the same slide), chains 1–4 (L4) and memory 1–2 (L3), background only. Nothing in this spec requires access to the course.

---
*Spec version 1 · course: LangChain for LLM Application Development · project: Ask your documents · when the build agent does something unexpected, add the missing constraint here and re-run.*
