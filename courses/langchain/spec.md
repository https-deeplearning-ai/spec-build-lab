# Spec: Ask Your Documents (question answering over a document collection)

**What you're building:** a program that answers your plain-language questions about a collection of documents by finding the few pieces of the collection closest in meaning to your question and having a language model write the answer from them; by default the collection is a small outdoor-clothing catalog, and you will see it answer questions like "Do the Cedar Trail Pants have side pockets?", say "I don't know" when the catalog has no answer, and grade itself against a set of example questions.

**What the recommended build needs to run:** an OpenAI API key (answers, embeddings, evaluation) and network access to OpenAI; no account or large download beyond the Python packages.

**Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once `OPENAI_API_KEY` is set and are skipped until then; that is not a failure.

This file is self-contained: everything the build needs is here.

*Provenance: course "LangChain for LLM Application Development"; materials used: lesson transcripts (8 lessons), the course notebooks (6), 13 slide images; pattern card confirmed by the owner; written 2026-11-01 with guide v2.9 (2026-10-31).*

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
C1–C4 are context questions (your documents, your model provider, how people use the program); C5–C10 follow the program's stages in order (split, embed, store, combine, evaluate) and end with how you watch it work.

### C1. Which documents should the program answer questions about?
- **C1a (Recommended - course default): The sample outdoor-clothing catalog.** The program indexes the 8-item catalog defined in section 7 and answers questions about it. *Pick this when* you want to build what the course built and see every test pass before pointing it at your own documents. *Setup:* none.
- **C1b: Your own collection.** The program indexes documents you supply (your notes, manuals, policies, product list); the offline tests still run on the sample catalog. *Pick this when* you already have a collection you want to ask about, e.g. "ask my English notes". *Setup:* put the files in one folder the program reads.
  - *What to check:* after indexing your folder, a question whose answer is written in one of your documents gets an answer that states that fact, and the trace (C10) shows the retrieved pieces came from your files.

### C2. What form are your documents in?
*Ask only when C1 is C1b.*
- **C2a (Recommended - course default): A table file (CSV), one row per item.** Each row becomes one document. *Pick this when* your collection is a list of records, such as products, contacts or entries, kept as a spreadsheet. *Setup:* none.
- **C2b: A folder of plain-text or Markdown files.** Each file becomes one document. *Pick this when* your collection is notes or write-ups kept as separate text files. *Setup:* none.
  - *What to check:* every text or Markdown file in the folder becomes exactly one document that records its file name, and no other file types are read.
- **C2c: PDF files.** The text of each PDF becomes one document. *Pick this when* your collection is reports, papers or manuals kept as PDFs. *Setup:* a PDF text-extraction package (no key).
  - *What to check:* each PDF in the folder becomes one document that records its file name and holds that PDF's extracted text, and a PDF that yields no text is reported by name instead of being indexed empty.

### C3. Which provider's language model writes the answers (and runs the evaluation)?
- **C3a (Recommended - course default): An OpenAI chat model.** Answers, generated examples and grades all come from an OpenAI chat model. *Pick this when* you have an OpenAI key or are willing to get one; each question costs one paid call. *Setup:* OpenAI API key.
- **C3b: Another hosted provider's chat model.** The same program calls a different provider. *Pick this when* you already pay for another provider or your organisation requires one; you will likely also need C6b or that provider's own embeddings. *Setup:* that provider's API key.
  - *What to check:* with that provider's key set and no OpenAI key, a `live` question about the sample catalog is answered from the retrieved pieces, and the trace shows the call went to the chosen provider.
- **C3c: A model running on your own machine.** A locally served model writes the answers. *Pick this when* your documents must not leave your machine or you have no paid key; costs: a model download of several GB, slower answers, and answers that may be weaker. *Setup:* a local model server and a model download.
  - *What to check:* with the network to hosted providers blocked, a question about the sample catalog is still answered from the retrieved pieces by the local model.

### C4. How will people ask their questions?
- **C4a (Recommended): From the command line.** `ask "<question>"` prints the answer; `evaluate` prints the evaluation report. *Pick this when* you, or people comfortable with a terminal, will use it. *Setup:* none.
- **C4b: A small web page served on your machine.** A page with a question box shows the answer below it. *Pick this when* people who do not use a terminal will ask the questions. *Setup:* none beyond a web package.
  - *What to check:* typing a sample question into the page shows the same answer the command line gives for it, and an empty question is refused with a message instead of being sent to the model.

### C5. Should long documents be split into smaller pieces before indexing?
*Ask only when C1 is C1b.*
- **C5a (Recommended - course default): No splitting; each document is one piece.** *Pick this when* each document is already short (a row, a short note); the course skipped splitting because its documents were already small. *Setup:* none.
- **C5b: Split each document into smaller pieces.** Each piece is indexed separately. *Pick this when* your documents are long (notes, reports, PDFs): a whole long document may not fit into what the model can read, and smaller pieces let only the relevant parts be sent. *Setup:* none.
  - *What to check:* each piece remembers which document it came from, and the pieces of one document together hold the whole document.

### C6. How is each piece turned into a numeric representation of its meaning (an embedding)?
- **C6a (Recommended - course default): OpenAI embeddings.** *Pick this when* you already use an OpenAI key; costs: every document and every question is sent to OpenAI and paid per use. *Setup:* OpenAI API key (the same one as C3a).
- **C6b: A local embedding model on your machine.** *Pick this when* your documents must not leave your machine for indexing, or you do not use OpenAI; costs: a download of a few hundred MB, and its matching quality may differ from the course's. *Setup:* the embedding model download.
  - *What to check:* indexing and question embedding make no network call, and a question worded differently from a document (e.g. "sunblocking" for "sun protection") still retrieves that document among its pieces.

### C7. Where are the stored meaning vectors kept?
- **C7a (Recommended - course default): In memory, rebuilt each time the program starts.** *Pick this when* your collection is small; the course chose an in-memory store because it needs no external database and is easy to start with; cost: every start re-embeds every document (time and paid calls). *Setup:* none.
- **C7b: A store saved on disk.** *Pick this when* your collection is large or you restart often, so documents are embedded once and reused. *Setup:* an embedded vector-store package (no server).
  - *What to check:* after a restart, a question is answered without embedding any document again, and a newly added document becomes retrievable after it is indexed.

### C8. How are the retrieved pieces combined into one answer?
- **C8a (Recommended - course default): Stuff — all retrieved pieces in one prompt, one model call.** *Pick this when* the retrieved pieces fit in one prompt; it is the simplest, cheapest and most common method, but for large or many pieces the prompt can grow past what the model can read. *Setup:* none.
- **C8b: Map-reduce — ask each piece separately, then combine.** One call per piece, then one more call that combines the separate answers. *Pick this when* you retrieve many or large pieces; it works over any number of pieces and its per-piece calls can run in parallel; costs: many more calls, and it treats each piece as independent of the others. *Setup:* none.
  - *What to check:* for one question with 4 retrieved pieces the model is called once per piece plus once to combine, and the final answer is built only from those per-piece answers.
- **C8c: Refine — build the answer piece by piece.** The first piece gives a first answer; each next call improves it with the next piece. *Pick this when* an answer must combine information spread across several pieces; costs: generally longer answers, slower because each call waits for the previous one, and about as many calls as map-reduce. *Setup:* none.
  - *What to check:* for one question with 4 retrieved pieces the model is called 4 times in order, and each call after the first receives the previous answer together with the next piece.
- **C8d: Map-rerank — one scored answer per piece, keep the best.** Each call answers from one piece and gives a score; the highest-scoring answer is returned. *Pick this when* the answer to a question usually sits in a single piece; costs: the course calls it experimental, it relies on the model scoring well (the scoring instructions need care), and it makes one call per piece. *Setup:* none.
  - *What to check:* for one question with 4 retrieved pieces the model is called once per piece, each reply carries an answer and a score, and the answer returned is the one with the highest score.

### C9. How is the program checked against example questions?
- **C9a (Recommended - course default): Hand-written plus model-generated examples, graded by a model.** You write a few question–answer pairs; the model writes one more pair per document from the first few documents; the program answers them all and a model grades each answer. *Pick this when* you want a repeatable check to see whether a change (another model, store or retrieval setting) makes answers better or worse; costs: extra model calls, and the generated reference answers are themselves model output. *Setup:* none beyond the C3 key.
- **C9b: Hand-written examples only, graded by a model.** *Pick this when* you want every reference answer written by a person, or your documents do not suit automatic question writing; cost: writing examples by hand does not scale well. *Setup:* none beyond the C3 key.
  - *What to check:* the evaluation report lists exactly the hand-written examples, each with question, reference answer, predicted answer and a grade from the grading model, and no generation call is made.
- **C9c: No evaluation step; you judge answers by reading them.** *Pick this when* it is a small personal tool and you will notice bad answers yourself; costs: checking by eye is tedious and leaves no record of whether a change helped. *Setup:* none.
  - *What to check:* the program has no evaluate command and makes no generation or grading calls, while every question-answering test still passes.

### C10. How can you see what happened inside one question?
- **C10a (Recommended - course default): A step-by-step trace printed on your machine, off by default.** Turned on, it prints the question, the retrieved pieces, the full prompt and the model's reply. *Pick this when* you want to find out why an answer is wrong (often the retrieval step, not the model) without sending runs anywhere. *Setup:* none.
- **C10b: A hosted run dashboard.** Every run is saved and browsable step by step in a web interface, and runs can be added to an example set for evaluation. *Pick this when* you want a history of runs across sessions and to grow your evaluation examples over time; cost: questions and documents are sent to the hosted service. *Setup:* an account and key for the hosted tracing service.
  - *What to check:* after one question with tracing on, the run appears in the dashboard showing the retrieved pieces, the prompt and the reply.

## 2. Departures from the course

| # | Where the recommended build differs | Reason |
|---|---|---|
| D1 | Current releases of the libraries instead of the course's pinned `langchain==0.0.179` and `openai==0.27.7`. | Course-era versions often no longer install or work with current models (4.7). |
| D2 | A command-line program (`ask`, `evaluate`) instead of notebook cells. | The build is a program, not a notebook. *Addition.* |
| D3 | An 8-item catalog and example questions written for this spec instead of the course's 1000-row outdoor-clothing catalog and its examples. | No course data is copied; small samples make outcomes exact. *Addition.* |
| D4 | Offline tests use a scripted stand-in model and a scripted stand-in embedder. | Tests must run without a key. *Addition, labelled stand-ins.* |
| D5 | The build agent picks a current OpenAI chat model; the course used `gpt-3.5-turbo` (and `gpt-3.5-turbo-instruct` for its one-line index query). | Model names go stale (4.6). |
| D6 | The index is built one way only (load → embed → store) instead of both the course's one-line index creator and its step-by-step version. | The course says both give the same result; one behavior is specified. |
| D7 | The course's in-memory vector store class is used if the current release still provides it; otherwise the current release's in-memory vector store. | Same behavior; the class may no longer exist (4.7). |
| D8 | The hosted evaluation platform the course demonstrated is not part of the recommended build (offered as C10b). | It needs a hosted account (4.4). |
| D9 | Document separator `<<<<>>>>>` between pieces in the answer prompt, from the course's final (evaluation-lesson) app; the question-answering lesson left the framework default. | Picked by 4.2 rule (2), final end-to-end app. |
| D10 | Grades are exactly `CORRECT` or `INCORRECT`; ties in retrieval order are not asserted. | Makes test outcomes exact. *Addition.* |
| D11 | Without a key and without stand-ins, `ask` and `evaluate` stop with a message naming `OPENAI_API_KEY`. | A clear failure instead of a crash. *Addition.* |

---

## 3. Objective
Answer a person's plain-language questions about their own document collection from the few stored pieces most similar in meaning to each question, say "I don't know" when those pieces lack the answer, and measure answer quality against example questions.

## 4. Tech stack, versions and secrets
- **Language:** Python 3 (current release). The course's framework is LangChain; the course is about it, so the build uses the current LangChain release (with its OpenAI integration) rather than a stand-in.
- **Versions:** current releases; no pins invented. The course pinned `langchain==0.0.179` and `openai==0.27.7` (fact about the course; see D1).
- **Framework behaviour:** where the course leaves behaviour to the framework (how the stuff/map-reduce/refine/map-rerank methods call the model, the answer prompt's wording, retries), keep the current release's behaviour; note in `resolved-decisions.md` how the release provides it.
- **Package layout:** an importable package `qa_app`; command line `python -m qa_app ask "<question>" [--trace] [--data <path>]` and `python -m qa_app evaluate [--trace] [--data <path>]`. Default data path `data/catalog.csv`.
- **Secrets:** `OPENAI_API_KEY` read from the environment (a local `.env` file may set it, as the course did); never written to any file the program creates, never printed, never committed.

## 5. Input/output contracts

```json
{
  "$id": "catalog.csv",
  "description": "UTF-8 CSV with a header row; each data row is one document.",
  "columns": ["name", "description"],
  "rowSchema": {"type": "object", "required": ["name", "description"],
    "properties": {"name": {"type": "string", "minLength": 1}, "description": {"type": "string", "minLength": 1}}}
}
```

```json
{
  "$id": "Document",
  "type": "object", "required": ["text", "source"],
  "properties": {
    "text": {"type": "string", "description": "For a CSV row: 'name: <name>' newline 'description: <description>'."},
    "source": {"type": "string", "description": "File path plus row number (1-based, header excluded)."}
  }
}
```

```json
{
  "$id": "StoredEntry",
  "type": "object", "required": ["vector", "text", "source"],
  "properties": {
    "vector": {"type": "array", "items": {"type": "number"}, "minItems": 1},
    "text": {"type": "string", "description": "The original text of the piece, unchanged."},
    "source": {"type": "string"}
  }
}
```

```json
{
  "$id": "Example",
  "type": "object", "required": ["query", "answer"],
  "properties": {"query": {"type": "string", "minLength": 1}, "answer": {"type": "string", "minLength": 1}}
}
```

```json
{
  "$id": "GradedExample",
  "type": "object", "required": ["query", "answer", "result", "grade"],
  "properties": {
    "query": {"type": "string"}, "answer": {"type": "string", "description": "Reference answer."},
    "result": {"type": "string", "description": "The program's predicted answer."},
    "grade": {"enum": ["CORRECT", "INCORRECT"]}
  }
}
```

- **`ask` output:** the answer text on one line of standard output (with `--trace`, the trace lines come first, the answer last). Exit code 0.
- **`evaluate` output:** for each example i (1-based) five lines: `Example i:`, `Question: <query>`, `Real Answer: <answer>`, `Predicted Answer: <result>`, `Predicted Grade: <grade>`, then a blank line (the course printed these five labels).

### Model roles
| Role | What it does | Course model (fact) |
|---|---|---|
| answer | Writes the answer from the question and retrieved pieces. | `gpt-3.5-turbo`, temperature 0 |
| example-generator | Writes one question–answer pair from one document. | `gpt-3.5-turbo`, temperature not set |
| grader | Grades a predicted answer against the reference answer. | `gpt-3.5-turbo`, temperature 0 |
| embedder | Turns each piece and each question into a meaning vector. | OpenAI embeddings (model not named; vectors of "over a thousand" numbers) |

### Settings
| Setting | Value | Source | Change this when |
|---|---|---|---|
| Answer temperature | 0.0 | L5 notebook (file L4-QnA) cell 28; L6 notebook (file L5-Evaluation) cell 8; L2 transcript: "set the temperature parameter to be equal to zero … less random". | You want more varied wording; the course raised it (0.9) only for creative naming in the chains lesson. |
| Pieces retrieved per question (n) | 4 | L5 transcript: similarity search "returns four documents" (the framework default; the course never sets it). | Answers need more pieces, or the prompt grows too long. |
| Document separator in the answer prompt | `<<<<>>>>>` | L6 notebook cell 8. | Never needed for the sample; any distinctive string works. |
| Documents used to generate examples | the first 5 | L6 notebook cell 18. | You want generated examples to cover more of the collection. |
| Grader temperature | 0 | L6 notebook cell 31. | — |
| Example-generator temperature | not set by the course; keep the framework default | L6 notebook cell 16. | — |
| Trace | off | L6 notebook cells 25–27 turn it on for one run, then off. | Turn on with `--trace` to see why an answer is wrong. |

## 6. Business rules

### What must stay true (the pattern card)
Every build, whatever options are chosen, keeps all three:
- **MST1. The documents are indexed by meaning before any question.** Each piece of text gets a numeric representation of its meaning, stored next to its original text, so pieces with similar meaning can be found later. → T1, T2
- **MST2. For each question, only the few stored pieces most similar in meaning are retrieved, not the whole collection.** → T3, T4
- **MST3. A language model writes the answer from the question plus the retrieved pieces, so the answer rests on the person's documents.** → T5, T6

### Rules of the recommended build
- **R1.** On start, the program loads every document (one per CSV row), embeds each with the embedder, and stores each vector with its original text and source, before accepting any question. → T1, T2
- **R2.** Each question is embedded with the same embedder and compared with every stored vector; the n = 4 most similar pieces are retrieved, most similar first. → T3, T4, T12
- **R3.** The answer model receives one prompt holding the question and exactly the retrieved pieces, separated by `<<<<>>>>>`, and no other document text; one answer-model call per question (stuff). → T4, T5, T12
- **R4.** The answer prompt tells the model to answer from the given pieces and, if it does not know the answer, to say that it does not know rather than make one up; the program returns the model's reply unchanged. (Course source: the evaluation lesson shows this instruction inside the question-answering prompt.) → T6, T13
- **R5.** The answer model is called with temperature 0. → T5
- **R6.** `evaluate` builds its examples as the hand-written examples followed by one generated example per document for the first 5 documents, in catalog order; each generated example is parsed into the Example structure (`query`, `answer`). → T7
- **R7.** `evaluate` answers every example's `query` through the same path as `ask` (R2–R5). → T8
- **R8.** Each predicted answer is graded by the grader model, which judges whether it means the same as the reference answer; the program never grades by exact or pattern string comparison. Each grade is `CORRECT` or `INCORRECT`, and the report follows the `evaluate` output contract. → T8, T9
- **R9.** The trace is off by default; with `--trace` the program prints, before the answer, the question, each retrieved piece's text, the full prompt sent to the answer model, and the model's reply. Without `--trace` it prints only the answer. → T10
- **R10.** When `OPENAI_API_KEY` is absent and the stand-ins are not in use, `ask` and `evaluate` exit with a non-zero code and a message containing `OPENAI_API_KEY`, and make no network call. *Addition.* → T11

## 7. Tests

### 7.1 Sample data
**`data/catalog.csv`** — written for this spec (*addition*; no course data copied). Header `name,description`, then these 8 rows in this order (P1–P8 are the row numbers 1–8):

| Row | name | description |
|---|---|---|
| P1 | Trailbreeze Sun Shirt | Lightweight long-sleeve shirt rated UPF 50+ for sun protection. One zip chest pocket. Fabric: recycled polyester. |
| P2 | Harbor Linen Tee | Short-sleeve linen tee for hot days. Relaxed fit. Fabric: linen. |
| P3 | Summit Shade Hoodie | Hoodie with UPF 40 sun protection and thumb loops. Fabric: nylon blend. |
| P4 | Glacier Down Parka | Insulated parka from the NorthLoft collection, filled with 700-fill goose down. |
| P5 | Cedar Trail Pants | Hiking pants with two zippered side pockets. Fabric: stretch nylon. |
| P6 | Riverstone Rain Jacket | Waterproof, packable rain jacket with a hood. |
| P7 | Meadow Fleece Pullover | Half-zip fleece pullover. It has no side pockets. |
| P8 | Coastline Swim Trunks | Quick-dry swim trunks with a mesh liner. |

(Descriptions containing commas are quoted in the CSV.) Each row's Document text is `name: <name>` newline `description: <description>`.

**Sample questions:**
- **Q-A** `Please suggest a shirt with sunblocking`
- **H1** `Do the Cedar Trail Pants have side pockets?` (also used as a plain question)
- **H2** `What collection is the Glacier Down Parka from?` (also used as a plain question)
- **Q-D** `Do you sell kayaks?` (planted: the catalog has no answer)

**Hand-written examples** (`data/examples.json`, a list of Example): H1 → answer `Yes`; H2 → answer `The NorthLoft collection`.

**Stand-in embedder** (*stand-in for the OpenAI embeddings*, tier 1, standard library only). Lower-case the text and split it into words on every character that is not a letter or digit. The vector has 9 numbers: one per concept below, 1 if any of the concept's words appears and 0 otherwise, then a final number that is always 1.

| # | Concept | Words |
|---|---|---|
| 1 | sun | sun, upf, sunblocking, uv |
| 2 | top | shirt, shirts, tee, tees, hoodie, hoodies |
| 3 | pocket | pocket, pockets |
| 4 | warm | down, parka, fleece, insulated |
| 5 | rain | rain, waterproof |
| 6 | pants | pants, trousers |
| 7 | collection | collection |
| 8 | swim | swim, trunks |

Similarity is cosine similarity. Resulting document concepts: P1 {sun, top, pocket}; P2 {top}; P3 {sun, top}; P4 {warm, collection}; P5 {pocket, pants}; P6 {rain}; P7 {warm, pocket}; P8 {swim}.

**Scripted stand-in model** (*stand-in for the OpenAI chat model*). It records every call (role, full prompt, temperature).
- *answer role:* find which question below appears in the prompt; if every listed fact also appears in the prompt, reply with the listed text; otherwise, or for any other prompt, reply `I don't know.`

| Question in prompt | Facts that must be in the prompt | Reply |
|---|---|---|
| Q-A | `UPF 40` and `UPF 50+` | The Summit Shade Hoodie (UPF 40) and the Trailbreeze Sun Shirt (UPF 50+) offer sun protection. |
| H1 | `two zippered side pockets` | Yes, the Cedar Trail Pants have two zippered side pockets. |
| H2 | `NorthLoft collection` | The Glacier Down Parka is from the NorthLoft collection. |
| G1 | `UPF 50+` | The Trailbreeze Sun Shirt is rated UPF 50+. |
| G2 | `Fabric: linen` | The Harbor Linen Tee is made of linen. |
| G3 | `thumb loops` | Yes, the Summit Shade Hoodie has thumb loops. |
| G4 | `700-fill` | The Glacier Down Parka uses 700-fill goose down. |
| G5 | `two zippered side pockets` | The Cedar Trail Pants have two side pockets. |

- *example-generator role:* given one document, returns one question–answer pair (in whatever structure the program's generation step requests) chosen by the product name in the document:

| Document | Generated query | Generated answer |
|---|---|---|
| P1 | G1 `What UPF rating does the Trailbreeze Sun Shirt have?` | `UPF 50+` |
| P2 | G2 `What fabric is the Harbor Linen Tee made of?` | `Linen` |
| P3 | G3 `Does the Summit Shade Hoodie have thumb loops?` | `Yes` |
| P4 | G4 `What fill power is the Glacier Down Parka?` | `700-fill` |
| P5 | G5 `How many side pockets do the Cedar Trail Pants have?` | `Two` |

- *grader role:* given a question, reference answer and predicted answer, replies `CORRECT` if the predicted answer contains the question's key term (ignoring case), otherwise `INCORRECT`. Key terms: H1 `yes`; H2 `NorthLoft`; G1 `50+`; G2 `linen`; G3 `yes`; G4 `700`; G5 `two`.

**Expected retrieval with the stand-in embedder** (replayed; similarity rounded). Pieces tied in similarity may come back in any order; tests never assert the order or identity of tied pieces.
- Q-A {sun, top}: P3 1.000, P1 0.866, P2 0.816, then P6/P8 0.408 (tied).
- H1 and G5 {pocket, pants}: P5 1.000, P7 0.667, P1 0.577, then P2/P6/P8 0.408 (tied).
- H2 {warm, collection}: P4 1.000, P7 0.667, then P2/P6/P8 0.408 (tied).
- Q-D {}: P2/P6/P8 0.707 (tied), then one of P3/P4/P5/P7 0.577 (tied).
- G1 {sun, top}: as Q-A (P1 retrieved). G2 and G3 {top}: P2 1.000, P3 0.816, P1 0.707, then P6/P8 0.500 (tied). G4 {warm}: P4/P7 0.816 (tied), then two of P2/P6/P8 0.500.

### 7.2 Test table
All tests run offline with the stand-ins unless marked `live`.

| Test | Given / When / Then |
|---|---|
| **T1** (R1, MST1) | *Given* the sample catalog and a fresh start. *When* the program starts. *Then* the store holds exactly 8 entries, each with a 9-number vector, its original Document text and its source, and the stand-in embedder has embedded 8 documents and no question. |
| **T2** (R1, MST1) | *Given* T1's started program. *When* H1 is asked. *Then* the embedder has embedded 8 documents and exactly 1 question, the question after all 8 documents. |
| **T3** (R2, MST2) | *Given* the started program. *When* Q-A is asked. *Then* exactly 4 pieces are retrieved and the first three, in order, are P3, P1, P2. |
| **T4** (R2, R3, MST2) | *Given* the started program. *When* H1 is asked. *Then* the single answer-model prompt contains H1, the text of P5, P7 and P1, exactly 4 pieces, and exactly 3 occurrences of `<<<<>>>>>`; at least 4 of the 8 product names are absent from it. |
| **T5** (R3, R5, MST3) | *Given* the sample catalog. *When* `python -m qa_app ask "What collection is the Glacier Down Parka from?"` runs. *Then* exactly one answer-model call is made, at temperature 0, its prompt contains the question and `NorthLoft collection`, and standard output is `The Glacier Down Parka is from the NorthLoft collection.` |
| **T6** (R4, MST3) | *Given* the started program. *When* Q-D is asked. *Then* the answer prompt contains the retrieved pieces and an instruction to say it does not know when the pieces lack the answer, and the program returns exactly `I don't know.` |
| **T7** (R6) | *Given* the sample catalog and `data/examples.json`. *When* `evaluate` builds its examples. *Then* there are 7 examples in this order: H1, H2, G1, G2, G3, G4, G5, each with the `query` and `answer` listed in 7.1, and the example-generator was called 5 times, once each for P1–P5. |
| **T8** (R7, R8) | *Given* T7's examples. *When* `python -m qa_app evaluate` runs. *Then* 7 answer-model calls and 7 grader calls are made, every grader call is at temperature 0, every grade is `CORRECT`, and the output has the five labelled lines for each of examples 1–7 with H1's `Predicted Answer: Yes, the Cedar Trail Pants have two zippered side pockets.` |
| **T9** (R8) | *Given* example H1 (reference answer `Yes`). *When* the predicted answer `Yes, the Cedar Trail Pants have two zippered side pockets.` is graded, and then `No, they have no pockets.` *Then* the first is `CORRECT` although it does not equal `Yes`, the second is `INCORRECT`, and both grades came from grader-model calls. |
| **T10** (R9) | *Given* the sample catalog. *When* H2 is asked with `--trace`, then again without it. *Then* the traced output contains H2, the text of P4, `<<<<>>>>>` and the reply, with the reply on the last line; the untraced output is only the reply line. |
| **T11** (R10) | *Given* no `OPENAI_API_KEY` and the stand-ins not in use. *When* `python -m qa_app ask "Do you sell kayaks?"` runs. *Then* it exits non-zero, its message contains `OPENAI_API_KEY`, and no network call is made. |
| **T12** `live` (R2, R3) | *Given* `OPENAI_API_KEY` and the sample catalog with the real embedder and model. *When* H2 is asked. *Then* the answer contains `NorthLoft`. |
| **T13** `live` (R4) | *Given* `OPENAI_API_KEY` and the sample catalog. *When* Q-D is asked. *Then* the answer says it does not know (contains "don't know" or "do not know", ignoring case) and names no kayak product. |

## 8. Standing permissions
- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in in its code and output; read secrets from the environment.
- **Ask First:** changing an answered question or a setting once the build has data; anything that sends data to a third party (for example C10b, or a provider not chosen at the gate).
- **Never:** invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets.

## 9. Test plan
- Offline: `python -m pytest -q` (tests in `tests/`, module names importable, e.g. `tests/test_retrieval.py`). The `live` tests are marked `live` and skipped when `OPENAI_API_KEY` is unset.
- Live: `OPENAI_API_KEY=… python -m pytest -q -m live`.
- Adjust the recommended tests for chosen options: tests that assert a behaviour the chosen option replaces (e.g. one answer-model call under C8b–C8d; the evaluate tests under C9b/C9c; R10's key name under C3b/C3c) are rewritten to that option's "what to check" sentence, and the rewrite is reported.
- For every chosen non-recommended option, turn its "what to check" sentence (copied into `resolved-decisions.md`) into a test and report it.
- Report one result per test with evidence (test output, file paths). "Should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.
- Finish with a diagram of the built app introduced by the sentence "This is the infra/structure diagram of this app".

---

## 10. Background notes
*For the build agent. No code.*

### The program
A program that answers a person's plain-language questions about their own collection of documents, using the few pieces of the collection most similar in meaning to the question. Stages:
`load → (split) → embed → store → retrieve → answer → evaluate`
- **load** — turns the collection into documents (one per catalog row); the model can only use text it is given.
- **split** — only for long documents (C5); the course's catalog rows were small enough to skip it.
- **embed** — gives each piece a numeric representation of its meaning, so similar texts get similar vectors (L5).
- **store** — keeps each vector beside its original text so pieces can be found and returned later (L5 slides "Vector Database: create").
- **retrieve** — embeds the question, compares it with every stored vector and picks the n most similar, because the model "can only inspect a few thousand words at a time" (L5).
- **answer** — passes the question and the retrieved pieces to the model in one prompt (stuff) to get the final answer (L5).
- **evaluate** — the course's final lesson on this program (L6) adds example questions, runs the program on them and grades the answers with a model, to tell whether a change makes the program better or worse.
The step trace (L6 "debug") only shows what ran; it is not a stage (C10).

### Failures
The course ran no failure of this program live; these were warned about or argued:
- **Whole collection does not fit in the model** (warned, L5: "Language models can only inspect a few thousand words at a time"). You would see a failed or truncated call on a large collection. Prevented by retrieving only n pieces. Rule R3 (with R2); test T4.
- **Grading by string matching fails** (argued with a concrete pair, L6: the reference "Yes" and the predicted "The Cozy Comfort Pullover Set, Stripe does have side pockets" are "nothing alike … if we were to try to do some string matching, or exact matching, or even some regexes here, it wouldn't know what to do"). You would see correct answers graded wrong. Prevented by model grading on meaning. Rule R8; test T9. Never offered as an option (5.3).
- **Wrong answers usually come from retrieval, not the model** (warned, L6: "oftentimes when a wrong result is returned, it's not necessarily the language model itself that's messing up. It's actually the retrieval step"). The trace (R9, T10) shows the retrieved pieces and prompt.
- **Stuff overflows on large or many pieces** (stated cost, L5 transcript and the "Stuff method" slide: "for large documents or many documents this will not work as it will result in a prompt larger than the context length"). A cost, not a ban: it is carried in C8a's "pick this when", and the other methods are offered.
- **Deprecated model** (L5 notebook note): the one-line index query defaulted to `text-davinci-003`, deprecated since 1 January 2024, replaced in the notebook by `gpt-3.5-turbo-instruct`. Covered by picking a current model (D5).
- Failures from other lessons, kept as notes only: a raw model reply that looks like JSON is still a string and cannot be read as a dictionary (L2, shown failing); a window memory of one exchange forgets the user's name (L3, shown); an agent first wrongly concluding that the 2022 World Cup had not happened (L7, shown).

### Why the questions and settings are what they are
- **C1/C2/C5:** the course's data was a CSV with one product per row (L5); the instructor names other sources ("extracted from a PDF file or from a webpage or from some company's intranet internal document collection", L5). Splitting: "When we get a big incoming document, we're first going to break it up into smaller chunks … because we may not be able to pass the whole document to the language model", and "Because these documents are already so small, we actually don't need to do any chunking here" (L5). Which files to read and whether to split are independent, so they are two questions.
- **C3/C6:** the course used OpenAI for the model and embeddings throughout. The provider and the embedder are independent choices.
- **C4:** the course ran notebook cells, so it has no interface choice; the command line is the lightest one (*addition*).
- **C7:** "it's an in-memory vector store and it doesn't require connecting to an external database of any kind so it makes it really easy to get started", "There are many different types of vector stores", and "we can also swap out the vector store here for a different type of vector store" (L5).
- **C8:** all four methods with their costs come from L5's transcript and slides: stuff "is the simplest method … quite cheap and it works pretty well. But that doesn't always work okay"; map_reduce "can operate over any number of documents … you can do the individual questions in parallel. But it does take a lot more calls. And it does treat all the documents as independent"; refine "is really good for combining information … will generally lead to longer answers … not as fast … takes just as many calls as Map_reduce"; map_rerank "is a pretty interesting and a bit more experimental one … relies on the language model to know what the score should be … you're making a bunch of language model calls". "The most common … is the stuff method … The second most common is the Map_reduce method."
- **C9:** hand-written examples "[don't] really scale that well" and model-generated ones save time (L6); manual grading "starts to get a little bit tedious" (L6). The course combined both kinds of examples (L6 notebook cell 22).
- **C10:** the debug flag prints each step's inputs, the prompt and token usage (L6); the hosted evaluation platform "is a way to do everything that we just did in the notebook, but persisted and show it in a UI", and lets you add runs to a dataset (L6).
- **Not questions (each fails a 5.2 test or is not a stage):**
  - Number of pieces retrieved, temperatures, separator: settings (4.3).
  - The one-line index creator versus the step-by-step build: the course says "these two things equate to the same result"; no learner situation tells them apart (test 3).
  - Other retrieval methods ("plenty of different methods, some less advanced, some more advanced", L5): none is named; a method that does not compare meaning would break MST1/MST2 (test 1).
  - Exact-match or regex grading: shown not to work (test 2; 5.3).
  - The answer prompt's "don't know" instruction: a rule of the recommended build (pattern card), not a choice.
  - Conversation memory, entity memory and storing conversations in a database (L3): from another lesson and they change no stage; the pattern card lists them as background notes, not offered.
  - Prompt templates and output parsers (L2), sequential and router chains (L4), agents and tools (L7): other lessons; they change no stage of this program.
  - Which model the tests run against: never asked (5.8).
- **Where picked values came from (4.2):**
  - Answer model: the final end-to-end app (L6 notebook cell 8) uses a chat model at temperature 0 with the stuff method; the L5 one-line `index.query` used a completion model (`gpt-3.5-turbo-instruct`) instead. Picked by rule (2), final end-to-end app.
  - Separator: L6 sets `<<<<>>>>>`; L5 left the framework default. Rule (2).
  - Course model id: notebooks pick `gpt-3.5-turbo` after 2024-06-12, else `gpt-3.5-turbo-0301`; the build agent picks a current model anyway (D5).
  - n = 4: the only value the course shows (L5, framework default).
- **Course code that looks odd:** in L5's step-by-step demonstration the retrieved documents were joined with no separator at all before being sent to the model (notebook cell 29). It is a by-hand demonstration replaced by the chain; the final app uses the separator above.

### Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports: `langchain.chat_models.ChatOpenAI`, `ChatPromptTemplate`, `RetrievalQA` (`from_chain_type`, `chain_type="stuff"`, `chain_type_kwargs`, `document_separator`), `langchain.document_loaders.CSVLoader`, `langchain.vectorstores.DocArrayInMemorySearch` (needs the `docarray` package), `langchain.indexes.VectorstoreIndexCreator`, `langchain.embeddings.OpenAIEmbeddings` (`embed_query`), `similarity_search`, `as_retriever`, `langchain.evaluation.qa.QAGenerateChain` (`apply_and_parse`), `QAEvalChain` (`evaluate`), `langchain.debug`, `langchain.llms.OpenAI`, the LangChain Evaluation Platform; models `gpt-3.5-turbo`, `gpt-3.5-turbo-0301`, `gpt-3.5-turbo-instruct`, `text-davinci-003` (deprecated); pins `langchain==0.0.179`, `openai==0.27.7`. Some newer model families reject a `temperature` parameter or accept only its default; if the chosen model does, record that in `resolved-decisions.md` and drop the setting for that role.

### Course names
| Course name | Spec term | Binding? |
|---|---|---|
| `OutdoorClothingCatalog_1000.csv` | `data/catalog.csv` (sample catalog) | file name binding in this spec |
| `query`, `answer` (example keys) | Example `query`, `answer` | yes (Example schema) |
| `result` (prediction key) | GradedExample `result` (predicted answer) | yes |
| graded output `text` | GradedExample `grade` | yes |
| `stuff`, `map_reduce`, `refine`, `map_rerank` | C8a–C8d | no |
| "Question:", "Real Answer:", "Predicted Answer:", "Predicted Grade:" | `evaluate` report labels | yes |
| index / vector store / retriever | store and retrieve stages | no |

### Lesson map
Transcript numbering (notebook file names count differently):
- L1 Introduction — framing only.
- L2 Models, Prompts and parsers (notebook file L1-Model_prompt_parser) — temperature 0 habit; string-not-dictionary failure (other lesson).
- L3 Memory (file L2-Memory) — conversation and other memory types: background only.
- L4 Chains (file L3-Chains) — LLM, sequential and router chains: background only; temperature 0.9 for creative naming.
- L5 Question and Answer (file L4-QnA) — the program: CSV loader, embeddings, in-memory vector store, retrieval of 4, stuff method, the other three methods, chunking, the one-line index; pattern card items 1–3.
- L6 Evaluation (file L5-Evaluation) — final end-to-end app (separator), hand and generated examples, debug trace, model grading, the "don't know" prompt, hosted platform.
- L7 Agents (file L6-Agents) — background only.
- L8 Conclusion — framing only.
Slides read: question_and_answer 1–7 (counted with L5's transcript, which talks through them; the "Stuff method" slide's pros/cons are used for C8a's cost), chains 1–4 (L4, background), memory 1–2 (L3, background). No slide disagreed with code or transcripts.
Nothing in this spec requires access to the course.

---
*Spec v2 draft · LangChain for LLM Application Development · Ask Your Documents · when the build agent does something unexpected, add the missing constraint here and re-run.*
