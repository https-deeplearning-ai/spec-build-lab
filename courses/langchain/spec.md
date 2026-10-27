# Spec: Ask Your Documents — answer questions from the few most relevant pieces of a document collection

**What you're building:** a program that answers your plain-language questions about your own collection of documents by finding the few pieces most similar in meaning to your question and having a language model write the answer from them. By default it uses a small outdoor-clothing product catalog: you ask "Please suggest a shirt with sunblocking" and it names the sun-protection shirt and hoodie, says "I don't know" when the catalog lacks the answer, and can grade itself against a set of example questions.

**What the recommended build needs to run:** an OpenAI API key (used for the chat model and for the embeddings) and network access to OpenAI; no other account and no large download.

**Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once `OPENAI_API_KEY` is set and are skipped until then; that is not a failure.

This file is self-contained: everything the build needs is here.

*Provenance: course "LangChain for LLM Application Development"; materials used: lesson transcripts (8 lessons), the course notebooks (6), 14 course slide images, and the owner-confirmed pattern card; generated 2026-10-27 with guide v2.8 (2026-10-27).*

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

Context questions first (C1–C3), then the program's stages in order (C4–C9).

### C1. What kind of documents will you ask questions about?
- **C1a — A table (CSV file); each row is one document.** (Recommended - course default)
  Pick this when your knowledge already sits in rows: a product list, an FAQ sheet, an inventory. Setup cost: none.
- **C1b — A folder of plain-text or Markdown files; each file is one document.**
  Pick this when your knowledge is notes or articles you wrote (e.g. "ask my English notes"). Setup cost: none.
  *What to check:* every file in the folder becomes a document that remembers its file name, and a question about a fact found in only one file retrieves a piece of that file.
- **C1c — A folder of PDF files; each page is one document.**
  Pick this when your documents are reports, manuals or papers kept as PDFs. Setup cost: one PDF-reading package to install.
  *What to check:* each PDF page becomes a document that remembers its file name and page number, and a question about a fact on one page retrieves that page.

### C2. Which provider runs the language model?
- **C2a — OpenAI's chat models.** (Recommended - course default)
  Pick this when you have or can get an OpenAI API key. Setup cost: an OpenAI API key (usage is paid).
- **C2b — Another hosted provider's chat model.**
  Pick this when you already pay for, or your organisation requires, a different provider. Setup cost: that provider's API key.
  *What to check:* the answer, example-generator and grader roles all call the chosen provider, and the offline tests still pass on the stand-ins.
- **C2c — A local model running on your own machine.**
  Pick this when your documents must not leave your machine or you have no API key. Setup cost: no key; a model download of several GB and a machine with enough memory to run it.
  *What to check:* after setup, with the network off, asking the sample sun question still returns an answer written from the retrieved pieces.

### C3. How will people ask their questions?
- **C3a — A command-line program (`ask` and `eval` commands).** (Recommended)
  Pick this when you are the one asking, from a terminal. Setup cost: none.
- **C3b — A small web page served on your machine: a question box, the answer, and the pieces it used.**
  Pick this when people who do not use a terminal will ask questions. Setup cost: one web-framework package.
  *What to check:* submitting the sample sun question in the page shows the same answer and the same four retrieved pieces as the command line does.

### C4. Should documents be split into smaller pieces before indexing?
- **C4a — No splitting: each document is one piece.** (Recommended - course default)
  Pick this when each document is short (a table row, a short note). Setup cost: none.
- **C4b — Split each document into overlapping pieces of a fixed size.**
  Pick this when your documents are long (notes, manuals, PDFs) and a whole document would crowd out other relevant pieces in the prompt. Setup cost: none; adds two settings (piece size, overlap), which you choose and record because the course gives no values.
  *What to check:* each piece remembers which document it came from, and the pieces of one document together hold the whole document.

### C5. What turns text into meaning vectors (the embedder)?
- **C5a — OpenAI's embedding model.** (Recommended - course default)
  Pick this when you chose C2a or otherwise have an OpenAI key and don't mind your document text being sent to OpenAI. Setup cost: the OpenAI API key (paid per use); needs that key even if C2 is not OpenAI.
- **C5b — A local embedding model.**
  Pick this when your documents are private, you chose C2c, or your model provider offers no embeddings. Setup cost: no key; a one-time model download.
  *What to check:* two sentences about the same subject score as more similar than either does with an unrelated sentence, and the sample sun question still retrieves the two sun-protection products first.

### C6. Where are the pieces and their vectors kept?
- **C6a — In memory, rebuilt every time the program starts.** (Recommended - course default)
  Pick this when your collection is small enough to re-embed quickly. Setup cost: none, no database. It re-embeds every document on each start, which costs time and, with paid embeddings, money.
- **C6b — A vector store saved on disk.**
  Pick this when your collection is large or you restart the program often. Setup cost: one embedded database package; you must re-index when documents change.
  *What to check:* after a restart, questions are answered without re-embedding any document, and a document added and re-indexed becomes retrievable.

### C7. How are the retrieved pieces combined into one answer?
- **C7a — All retrieved pieces go into one prompt; one model call ("stuff").** (Recommended - course default)
  Pick this when the retrieved pieces fit in one prompt together. Setup cost: none. Simplest and cheapest, and the model sees all pieces at once; it stops working when the pieces together are larger than the model's context length.
- **C7b — Ask each piece separately, then combine the answers in one more call ("map_reduce").**
  Pick this when you retrieve many pieces that together do not fit in one prompt. Setup cost: none; one model call per piece plus one, and it treats pieces as independent.
  *What to check:* the model is called once per retrieved piece and once more to combine, and the final answer to the sample vest question still says it has side pockets.
- **C7c — Go piece by piece, improving the answer each time ("refine").**
  Pick this when answers must combine facts spread across several pieces and longer answers are fine. Setup cost: none; as many calls as map_reduce, made one after another, so it is slower.
  *What to check:* each call after the first includes the previous call's answer, the calls run in retrieval order, and the final answer to the sample vest question still says it has side pockets.
- **C7d — Ask each piece separately for an answer and a score; keep the highest-scored answer ("map_rerank").**
  Pick this when the answer is likely to sit in a single piece and you want the best single answer. Setup cost: none; one call per piece, and it depends on the model scoring relevance well.
  *What to check:* every per-piece call returns an answer and a numeric score, and the app returns the answer with the highest score.

### C8. Should the program evaluate itself on example questions?
- **C8a — Yes: hand-written examples plus examples generated by the model from the documents, all graded by a model.** (Recommended - course default)
  Pick this when you want to know whether a change (another model, another store, another setting) makes answers better or worse. Setup cost: none; about three model calls per example.
- **C8b — Yes, but hand-written examples only, graded by a model.**
  Pick this when every example must be checked by a person first, e.g. specialised documents where generated questions could be off. Setup cost: none; writing examples by hand takes time and does not scale.
  *What to check:* `eval` runs exactly the examples in the examples file and makes no generator calls.
- **C8c — No evaluation stage.**
  Pick this when you only want to ask questions and will judge the answers yourself. Setup cost: none.
  *What to check:* the program has no `eval` command and all remaining recommended tests pass.

### C9. How can you see what happened inside a run?
- **C9a — A debug switch that prints each step: the retrieved pieces, the full prompt, and token usage.** (Recommended - course default)
  Pick this when you debug on your own machine. Setup cost: none.
- **C9b — The debug switch, plus sending every run to a hosted tracing and evaluation platform.**
  Pick this when you want runs kept over time and want to grow your example set from real questions. Setup cost: an account and API key for that platform; your questions and document pieces are sent to it.
  *What to check:* with the platform key set, each `ask` and `eval` run appears on the platform with its retrieved pieces and prompt; without the key the program runs unchanged.

---

## 2. Departures from the course

| # | Where the recommended build differs | Reason |
|---|---|---|
| D1 | It is a command-line program, not notebook cells. (addition) | A notebook is how the course was taught, not part of the program. |
| D2 | Current library releases instead of the course's pinned `langchain==0.0.179` and `openai==0.27.7`. | Course-era versions often no longer install or work with current models. |
| D3 | The build agent picks a current chat model instead of the course's `gpt-3.5-turbo` (and `gpt-3.5-turbo-0301` before 2024-06-12). | Model names go stale. |
| D4 | Sample catalog written for this spec (8 products) instead of the course's outdoor-clothing CSV. | No course data is copied; the facts are known so tests can assert them. |
| D5 | Offline tests use a scripted stand-in model and a keyword stand-in embedder. (addition) | The course's model and embeddings need a key; tests must run offline. |
| D6 | The course's one-line index shortcut is not built; the program uses the step-by-step path (load → embed → store → retriever → answer) with the chat model. | Both give the same result per the course; the shortcut in the course notebook answered with a separate completion model (`text-davinci-003`, later replaced by `gpt-3.5-turbo-instruct`). The course's final end-to-end version (Evaluation lesson) uses the step-by-step retriever with the chat model. |
| D7 | Pieces in the prompt are separated by `<<<<>>>>>`. | Picked value: the course's final end-to-end version (Evaluation lesson) set it; the Q&A lesson used the library default. |
| D8 | A third hand-written evaluation example whose answer is not in the documents. (addition) | Makes the grader's INCORRECT verdict reachable and tests "I don't know". The course had 2 hand-written + 5 generated = 7 examples; this build has 8. |
| D9 | Evaluation results are also written to `eval_results.json`. (addition) | The course only printed them; a file gives the test evidence. |
| D10 | The hosted evaluation platform shown in the course is not in the recommended build (it is option C9b). | It needs a separate account. |

---

## 3. Objective

Given a collection of documents, index each piece by meaning once, then for every question retrieve the 4 pieces most similar in meaning and have a language model answer from only those pieces, saying it does not know when they lack the answer, and grade itself on example questions.

## 4. Tech stack, versions, secrets

- Python 3, current release. Current releases of LangChain (core, community integrations, OpenAI integration), the in-memory vector store the course used (`DocArrayInMemorySearch`, needs the `docarray` package), `python-dotenv`, and `pytest`. No pins are invented; the course's own pins are listed in the background notes.
- Command-line interface with the standard library's argument parser (C3a).
- Secrets: `OPENAI_API_KEY` is read from the environment, or from a local `.env` file (as the course did). Never written to code, logs, `resolved-decisions.md` or `eval_results.json`.
- Stand-in mode: when the environment variable `QA_STAND_INS=1` is set, every model role and the embedder use the scripted stand-ins of section 8.2. The tests set it. Without it, the program uses the real provider. (addition)

## 5. Contracts

### 5.1 Files

| File | Contents |
|---|---|
| `sample_data/products.csv` | The sample catalog (section 8.1). Columns `name`, `description`; header row; UTF-8. |
| `sample_data/hand_examples.json` | The hand-written evaluation examples (section 8.1). |
| `eval_results.json` | Written by `eval` (R7). |
| `resolved-decisions.md` | Written at the gate (section 0). |

The Python package is named `qa_app` (importable). The CLI runs as `python -m qa_app <command>`.

### 5.2 Commands

- `python -m qa_app ask "<question>" [--debug] [--data <csv path>]` — prints the answer on one line (debug lines before it when `--debug`). `--data` defaults to `sample_data/products.csv`. Exit code 0 on success.
- `python -m qa_app eval [--data <csv path>] [--examples <json path>]` — runs evaluation (R5–R7). `--examples` defaults to `sample_data/hand_examples.json`.
- Without `OPENAI_API_KEY` and without `QA_STAND_INS=1`: exits with code 2 and a message naming `OPENAI_API_KEY` (R9).

### 5.3 Schemas (JSON Schema, abbreviated)

**Document / stored piece**
```json
{"type":"object","required":["text","source","row","vector"],
 "properties":{
  "text":{"type":"string","minLength":1,
          "description":"For a CSV row: one line per column, 'name: <name>' then 'description: <description>', joined by a newline."},
  "source":{"type":"string","description":"Path of the file the piece came from."},
  "row":{"type":"integer","minimum":0,"description":"0-based data row number in the CSV."},
  "vector":{"type":"array","items":{"type":"number"},"minItems":1}}}
```

**Answer result** (what `ask` produces; `--debug` prints `pieces` and `prompt`)
```json
{"type":"object","required":["question","answer","pieces"],
 "properties":{
  "question":{"type":"string","minLength":1},
  "answer":{"type":"string","description":"The model's reply, unchanged."},
  "pieces":{"type":"array","minItems":1,"maxItems":4,
            "items":{"type":"object","required":["text","source","row"],
                     "description":"A stored piece without its vector."},
            "description":"Most similar first."}}}
```

**Example**
```json
{"type":"object","required":["query","answer","origin"],
 "properties":{"query":{"type":"string","minLength":1},
               "answer":{"type":"string","minLength":1},
               "origin":{"enum":["hand-written","generated"]}}}
```

**`eval_results.json`**
```json
{"type":"object","required":["results","total","correct","incorrect"],
 "properties":{
  "results":{"type":"array","items":{"type":"object",
     "required":["query","real_answer","predicted_answer","grade"],
     "properties":{"query":{"type":"string"},"real_answer":{"type":"string"},
                   "predicted_answer":{"type":"string"},
                   "grade":{"enum":["CORRECT","INCORRECT"]}}}},
  "total":{"type":"integer"},"correct":{"type":"integer"},"incorrect":{"type":"integer"}}}
```
`correct + incorrect = total = len(results)`.

### 5.4 Model roles

| Role | What it does | Course model (fact about the course) |
|---|---|---|
| `answerer` | Writes the answer from the question plus the retrieved pieces. | `gpt-3.5-turbo` |
| `example_generator` | Writes one question–answer pair from one document. | `gpt-3.5-turbo` |
| `grader` | Judges whether a predicted answer means the same as the real answer. | `gpt-3.5-turbo` |
| `embedder` | Turns a piece or a question into a vector. | OpenAI's default embedding model (the course showed a vector of "over a thousand" numbers) |

### 5.5 Settings

| Setting | Value | Source | Change this when … |
|---|---|---|---|
| S1 Retrieval count (n) | 4 | Q&A lesson: the similarity search "returns four documents" (library default). | Answers need facts spread over more pieces, or pieces are long and crowd the prompt. |
| S2 Answerer temperature | 0.0 | Q&A and Evaluation notebooks; Models lesson: temperature 0 "to make this output a little bit less random". | You want more varied wording. If the chosen model rejects a temperature, leave it unset and record that in the checklist. |
| S3 Piece separator in the prompt | `<<<<>>>>>` | Evaluation notebook (the course's final end-to-end version). | Your documents contain that string. |
| S4 Documents used to generate examples | the first 5 documents, in file order | Evaluation notebook (first five rows). | You want more or fewer generated examples. |
| S5 Example-generator temperature | not set (library default) | Evaluation notebook sets none; the Models lesson says the default is 0.7. | Generated questions are too repetitive or too odd. |
| S6 Grader temperature | 0 | Evaluation notebook. | Rarely; keep grading repeatable. |
| S7 Debug switch | off unless `--debug` | Evaluation lesson: turned on to inspect one run, then off "to just not print everything". | You are inspecting a wrong answer. |

## 6. Business rules

### 6.1 What must stay true (the course's pattern card — every option keeps these)
1. **The documents are indexed by meaning before any question.** Each piece of text gets a numeric representation of its meaning, stored next to its original text, so pieces with similar meaning can be found later. → R1
2. **For each question, only the few stored pieces most similar in meaning are retrieved, not the whole collection.** → R2
3. **A language model writes the answer from the question plus the retrieved pieces, so the answer rests on the person's documents.** → R3

### 6.2 Rules
- **R1 Index first.** On start, every document in the data file is loaded (C1a: one document per CSV row), each becomes one piece (C4a), each piece is embedded, and the piece's vector is stored together with its original text, source and row. No question is answered before indexing finishes. → T1, T2
- **R2 Retrieve the few most similar.** A question is embedded with the same embedder as the pieces, compared with every stored vector by cosine similarity, and the S1 = 4 most similar pieces are returned, most similar first. Only those pieces reach the model. → T3, T4, T5, T15
- **R3 One answer call from question plus pieces.** The answerer receives one prompt (C7a) made of: the instruction "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer." (the course's prompt, as a system message); the retrieved pieces' texts in retrieval order joined by the S3 separator; and the question (as the user message). Temperature S2. Exactly one answerer call per question. → T6, T7, T15
- **R4 Say "I don't know"; never add to the answer.** The program shows the answerer's reply unchanged; it adds no facts of its own. When the pieces lack the answer, the reply the model gives (e.g. "I don't know.") is what the person sees. → T8, T16
- **R5 Examples.** `eval` builds its example list as: the hand-written examples from the examples file, in file order; then one generated example per document for the first S4 = 5 documents, in file order, each parsed from the example generator's reply into `{query, answer}` with `origin: "generated"`. → T9, T17
- **R6 Grade by meaning, never by string matching.** Each example's query goes through the same path as `ask` (R2–R4) to get the predicted answer. The grader receives the query, the real answer and the predicted answer and judges whether they mean the same; its reply is normalised to `INCORRECT` if it contains "INCORRECT", else `CORRECT` if it contains "CORRECT", else `INCORRECT` (normalisation is an addition). The program never decides a grade by comparing strings, exact or by pattern. One grader call per example; grader temperature S6. → T10, T11, T17
- **R7 Report.** `eval` prints, per example, the question, real answer, predicted answer and grade, then writes `eval_results.json` (schema 5.3) with the totals. → T10, T12, T17
- **R8 Debug switch.** With `--debug`, `ask` prints, before the answer: each retrieved piece's text (most similar first), the full prompt sent to the answerer, and token usage when the provider reports it. Without `--debug` it prints only the answer line. → T13
- **R9 Real provider or labelled stand-ins.** With `QA_STAND_INS=1`, all model roles and the embedder are the section-8.2 stand-ins, each of which describes itself as a stand-in (its name or description contains "stand-in"). Without it and without `OPENAI_API_KEY`, the program exits with code 2 and a message naming `OPENAI_API_KEY`. → T14
- **R10 Structures on a fresh start.** After a fresh start on the sample data, the store holds exactly 8 pieces; after `eval`, `eval_results.json` exists. → T1, T12

## 8. Tests

### 8.1 Sample data (facts written for this spec)

**`sample_data/products.csv`** — header `name,description`, then these 8 rows (row numbers 0–7). Quote the description field where it contains a comma.

| row | name | description |
|---|---|---|
| 0 | Trailline Sun Shirt | Lightweight long-sleeve shirt with UPF 50+ sun protection. Made of recycled polyester. Has two chest pockets. |
| 1 | Coastline Sun Hoodie | Pullover hoodie rated UPF 40 for sun protection, with thumb loops. Machine washable. |
| 2 | Ridgeback Rain Jacket | Waterproof jacket with taped seams and a packable hood. Part of the StormGuard collection. |
| 3 | Summit Down Vest | Insulated vest filled with 700-fill down from the AlpineLoft collection. Has two zippered side pockets. |
| 4 | Harbor Fleece Pullover | Soft fleece pullover with a half zip and a kangaroo front pocket. No side pockets. |
| 5 | Trek Hiking Socks | Merino wool hiking socks, sold in packs of three. |
| 6 | Canyon Cargo Shorts | Quick-dry shorts with six pockets, including two cargo pockets. |
| 7 | Glacier Wool Beanie | Knit beanie of merino wool. One size fits most. |

Each row's piece text is `name: <name>` newline `description: <description>`.

**`sample_data/hand_examples.json`** — a JSON array, in this order:

| # | query | answer | note |
|---|---|---|---|
| H1 | Does the Summit Down Vest have side pockets? | Yes | Planted failure F1: a one-word real answer that an exact string match would mark wrong. |
| H2 | What collection is the Ridgeback Rain Jacket from? | The StormGuard collection | |
| H3 | What is the warranty on the Trek Hiking Socks? | Lifetime warranty | Addition (D8): the catalog has no warranty facts; planted unanswerable question. |

### 8.2 Scripted stand-ins (each is a stand-in for the real provider; label it so)

**Stand-in embedder** (stands in for the provider's embedding model). Lower-case the text, split it into words on every character that is not `a–z` or `0–9`, and build a 9-number vector: numbers 1–8 count how many words fall in each keyword group below; number 9 is always `0.5`.

| # | group | words |
|---|---|---|
| 1 | sun | sun, upf, sunblocking, uv |
| 2 | rain | rain, waterproof, storm, stormguard |
| 3 | warm | down, insulated, fleece, wool, merino, warm |
| 4 | pocket | pocket, pockets |
| 5 | feet | socks, sock |
| 6 | head | beanie, hat |
| 7 | legs | shorts, pants |
| 8 | collection | collection |

Resulting piece vectors: row 0 `[3,0,0,1,0,0,0,0,0.5]`; row 1 `[3,0,0,0,0,0,0,0,0.5]`; row 2 `[0,3,0,0,0,0,0,1,0.5]`; row 3 `[0,0,3,1,0,0,0,1,0.5]`; row 4 `[0,0,2,2,0,0,0,0,0.5]`; row 5 `[0,0,2,0,2,0,0,0,0.5]`; row 6 `[0,0,0,2,0,0,2,0,0.5]`; row 7 `[0,0,3,0,0,2,0,0,0.5]`.

Replayed retrieval (cosine similarity, top 4; "tie" means equal scores):

| question | top 4 rows, most similar first |
|---|---|
| Q-sun "Please suggest a shirt with sunblocking" | 1, 0, then two of the tied rows {4, 5, 6} |
| H1 "Does the Summit Down Vest have side pockets?" | 4, 3, 7, then one of the tied rows {5, 6} |
| H2 "What collection is the Ridgeback Rain Jacket from?" | 2, 3, then two of the tied rows {4, 5, 6} |
| H3 "What is the warranty on the Trek Hiking Socks?" | 5, then 4 and 6 (tied), then 1 — exactly {5, 4, 6, 1} |
| G1–G5 (below) | G1: 1, 0, then two of {4, 5, 6}; G2: 1, 0, then two of {4, 5, 6}; G3: 2, then exactly {4, 5, 6}; G4: 3, 7, then 4 and 5 (tied) — exactly {3, 7, 4, 5}; G5: 4, 3, 7, then one of {5, 6} |

Tests assert only the untied positions.

**Stand-in answerer** (stands in for the chat model). It reads the question and the context from the prompt. If the question is in this table **and** the context contains the marker, it replies with the reply; otherwise it replies exactly `I don't know.` It records every call's prompt and temperature.

| question | marker in context | reply |
|---|---|---|
| Please suggest a shirt with sunblocking | UPF | The Coastline Sun Hoodie (UPF 40) and the Trailline Sun Shirt (UPF 50+) both offer sun protection. |
| Does the Summit Down Vest have side pockets? | zippered side pockets | Yes. The Summit Down Vest has two zippered side pockets. |
| What collection is the Ridgeback Rain Jacket from? | StormGuard | The Ridgeback Rain Jacket is part of the StormGuard collection. |
| What sun protection rating does the Trailline Sun Shirt have? | UPF 50+ | The Trailline Sun Shirt has UPF 50+ sun protection. |
| Can the Coastline Sun Hoodie be machine washed? | Machine washable | Yes, the Coastline Sun Hoodie is machine washable. |
| Does the Ridgeback Rain Jacket have taped seams? | taped seams | Yes, the Ridgeback Rain Jacket has taped seams. |
| What fill power is the down in the Summit Down Vest? | 700-fill | The Summit Down Vest uses 700-fill down. |
| Does the Harbor Fleece Pullover have side pockets? | No side pockets | No. The Harbor Fleece Pullover has a kangaroo front pocket and no side pockets. |

**Stand-in example generator** (stands in for the chat model). Given one document, it returns the pair for the product named in it, in whatever reply format the build's generator parser expects; after parsing, `{query, answer}` must equal:

| row | query (G#) | answer |
|---|---|---|
| 0 | G1 What sun protection rating does the Trailline Sun Shirt have? | UPF 50+ |
| 1 | G2 Can the Coastline Sun Hoodie be machine washed? | Yes |
| 2 | G3 Does the Ridgeback Rain Jacket have taped seams? | Yes |
| 3 | G4 What fill power is the down in the Summit Down Vest? | 700-fill |
| 4 | G5 Does the Harbor Fleece Pullover have side pockets? | No |

It records every call and its temperature (none set, S5).

**Stand-in grader** (stands in for the chat model's judgement). For the query, it replies `CORRECT` if the predicted answer contains the key fact below (ignoring case), else `INCORRECT`. It records each call's prompt and temperature.

| query | key fact |
|---|---|
| H1 | yes |
| H2 | stormguard |
| H3 | lifetime |
| G1 | upf 50+ |
| G2 | yes |
| G3 | yes |
| G4 | 700-fill |
| G5 | no side pockets |

### 8.3 Test table

All tests run with `QA_STAND_INS=1` on the sample data unless marked `live`. `live` tests use the real provider, run when `OPENAI_API_KEY` is set and are skipped otherwise.

| Test | Given | When | Then | Rules |
|---|---|---|---|---|
| T1 | A fresh start, sample data | The program indexes | The store holds exactly 8 pieces; each has row 0–7, `source` ending in `products.csv`, the piece text of section 8.1 and the 9-number vector of section 8.2. | R1, R10 |
| T2 | A fresh start | `ask "Please suggest a shirt with sunblocking"` | The embedder's call log shows 8 piece embeddings before the first question embedding. | R1 |
| T3 | Indexed sample | `ask` Q-sun | Exactly 4 pieces are retrieved; the first is row 1, the second row 0. | R2 |
| T4 | Indexed sample | `ask` G4 | The 4 pieces are rows {3, 7, 4, 5} with row 3 first and row 7 second; the answerer's prompt contains none of "Trailline", "Coastline", "Ridgeback", "Canyon". Reply: `The Summit Down Vest uses 700-fill down.` | R2 |
| T5 | Indexed sample | `ask` H2 | The first piece is row 2; reply `The Ridgeback Rain Jacket is part of the StormGuard collection.` | R2 |
| T6 | Indexed sample | `ask "Does the Summit Down Vest have side pockets?"` | Output is exactly `Yes. The Summit Down Vest has two zippered side pockets.`; the answerer was called exactly once; its prompt contains the question and the text of row 3. | R3 |
| T7 | Indexed sample | `ask` Q-sun | The answerer's prompt contains the R3 instruction sentence exactly, contains `<<<<>>>>>` exactly 3 times, lists row 1's text before row 0's; the call's temperature is 0.0. Output is exactly the Q-sun reply. | R3 |
| T8 | Indexed sample | `ask "What is the warranty on the Trek Hiking Socks?"` | Output is exactly `I don't know.`; the prompt contains the R3 instruction sentence. | R4 |
| T9 | Indexed sample, `hand_examples.json` | `eval` | The example list has 8 entries: H1, H2, H3 (origin hand-written), then G1–G5 (origin generated) with the queries and answers of section 8.2; the generator was called exactly 5 times, on rows 0–4 in order, with no temperature set. | R5 |
| T10 | Indexed sample | `eval` | Grades: H1 CORRECT, H2 CORRECT, H3 INCORRECT, G1–G5 CORRECT; totals 8 / 7 / 1; the printed report shows, for each example, question, real answer, predicted answer and grade. | R6, R7 |
| T11 | Planted F1 (H1) | `eval` | For H1, the real answer `Yes` and the predicted answer `Yes. The Summit Down Vest has two zippered side pockets.` are not equal strings, yet the grade is CORRECT; the grader was called 8 times (once per example), each prompt containing that example's query, real answer and predicted answer, each with temperature 0. | R6 |
| T12 | A fresh directory with no `eval_results.json` | `eval` | `eval_results.json` exists, validates against schema 5.3, has 8 results, `total` 8, `correct` 7, `incorrect` 1. | R7, R10 |
| T13 | Indexed sample | `ask` Q-sun with `--debug`, then without | With `--debug` the output contains the full text of rows 1 and 0 and the R3 instruction sentence, before the answer line. Without it, the output is the answer line only. | R8 |
| T14 | `QA_STAND_INS` unset and `OPENAI_API_KEY` unset | `ask` Q-sun | Exit code 2; the message contains `OPENAI_API_KEY`. Separately, each stand-in's name or description contains "stand-in". | R9 |
| T15 `live` | Real provider, sample data | `ask` Q-sun | The answer names "Coastline Sun Hoodie" or "Trailline Sun Shirt"; rows 0 and 1 are among the 4 retrieved pieces. | R2, R3 |
| T16 `live` | Real provider, sample data | `ask` H3 | The answer says it does not know (contains "don't know" or "do not know", ignoring case) and names no warranty term. | R4 |
| T17 `live` | Real provider, sample data | `eval` | 8 results, each grade CORRECT or INCORRECT; `eval_results.json` written; H3 graded INCORRECT. | R5, R6, R7 |

## 9. Standing permissions

- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in; read secrets from the environment (or `.env`).
- **Ask First:** changing an answered question or a setting once the build has data; anything that sends data to a third party (including C9b's platform).
- **Never:** invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets.

## 10. Test plan

1. `python -m pip install -U langchain langchain-core langchain-community langchain-openai docarray python-dotenv pytest`
2. Offline: `QA_STAND_INS=1 python -m pytest -q` — T1–T14 must pass; T15–T17 report as skipped without a key.
3. Live (when `OPENAI_API_KEY` is set): `python -m pytest -q -m live` — T15–T17.
4. Manual: `QA_STAND_INS=1 python -m qa_app ask "Please suggest a shirt with sunblocking" --debug` and `QA_STAND_INS=1 python -m qa_app eval`.
5. Adjust for chosen options: drop tests that exist only for an option not chosen (e.g. T9–T12 and T17 under C8c; T9's generator assertions under C8b), and for every chosen non-recommended option turn its "what to check" sentence (copied into `resolved-decisions.md`) into a test and run it.
6. Report one result per test with evidence (test output, file paths). "Should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.
7. Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

---

## 11. Background notes (for the build agent)

### The program
A program that answers a person's plain-language questions about their own documents using the few pieces most similar in meaning to the question. Stages:
- **load** — read the person's documents; each becomes a document with its source.
- **split** (optional, C4) — break long documents into pieces small enough that only the relevant ones go to the model; the course skipped it because its rows were already small.
- **embed** — give each piece a numeric meaning vector so similar text can be found ("Pieces of text with similar content will have similar vectors").
- **store** — keep each vector next to its original text (the course's "vector database").
- **retrieve** — embed the question, compare it with all stored vectors, pick the n most similar, because "Language models can only inspect a few thousand words at a time".
- **answer** — the model writes the answer from the question plus the retrieved pieces, which lets it use data it was not trained on.
- **evaluate** (C8) — check answers on example questions, graded by a model, so changes can be judged better or worse.
Debug tracing (C9) shows what ran without judging it; it is not a stage.

### Failures
- **F1 — exact string matching cannot grade answers (Evaluation lesson).** You see: the real answer "Yes" and the predicted answer "The Cozy Comfort Pullover Set, Stripe does have side pockets" are "nothing alike" as strings, so "string matching, or exact matching, or even some regexes" "wouldn't know what to do", though the answer is correct. Why: open-ended answers have many wordings with the same meaning. Prevention: grading is done by a model judging meaning (R6). Planted sample: H1 (real "Yes" vs a long predicted answer). Test: T11.
- **Warned: making up an answer.** The course's answer prompt tells the model "If you don't know the answer, just say that you don't know, don't try to make up an answer." Prevention: R3 includes the instruction, R4 shows the reply unchanged. Planted sample: H3. Tests: T8, T16.
- **Warned: wrong answers often come from retrieval, not the model (Evaluation lesson):** "oftentimes when a wrong result is returned, it's not necessarily the language model itself that's messing up. It's actually the retrieval step." Prevention: the debug switch shows the retrieved pieces and full prompt (R8). Test: T13.
- **Stated limit, not a failure: "stuff" with large or many documents.** The course slide says that for large or many documents stuffing "will not work as it will result in a prompt larger than the context length"; the transcript says "that doesn't always work okay" and introduces the other methods. It is carried as C7a's cost, and C7b–d are offered.
- Failures from other lessons (background only): a window memory of one exchange forgot the user's name (Memory lesson); an agent first concluded a past event "has not happened yet" and needed more searches (Agents lesson; the notebook notes agents "will sometimes come to the wrong conclusion"); a model reply that looks like JSON is still a string until parsed (Models, Prompts and Parsers lesson).

### Why the questions and settings are what they are
- **C1 documents:** the course loads a CSV of products, one document per row; the Q&A lesson names other sources ("extracted from a PDF file or from a webpage or from some company's intranet"). The "ask my English notes" case is C1b.
- **C2 provider:** the course used OpenAI chat models throughout. Other providers and local models keep every pattern-card item.
- **C3 interface:** the course ran in notebooks, which is not part of the program; no course choice.
- **C4 splitting:** course: "Because these documents are already so small, we actually don't need to do any chunking here"; for big documents "we're first going to break it up into smaller chunks". The pattern card makes splitting a learner choice. The course gives no piece size or overlap.
- **C5 embeddings / C6 store:** the course: "we can specify an embedding here as well ... we can also swap out the vector store here for a different type of vector store". Its store was chosen because "it's an in-memory vector store and it doesn't require connecting to an external database of any kind".
- **C7 combining:** stuff ("the simplest method", "quite cheap and it works pretty well", most common), map_reduce ("can operate over any number of documents", parallel, "a lot more calls", treats documents as independent; second most common), refine ("really good for combining information and building up an answer over time", longer answers, slower, "just as many calls as Map_reduce"), map_rerank ("a bit more experimental", relies on the model to score, independent calls, more expensive). The course also says these methods work for other chains, e.g. map_reduce for summarisation.
- **C8 evaluation:** hand-written examples "don't really scale that well"; generating them with a model "saves us a bunch of time"; grading by a model because exact matching fails (F1).
- **C9 tracing:** the course turned on a global debug mode showing every nested step, the full prompt and token usage ("corresponds very closely to the total cost"), then showed a hosted evaluation platform that keeps runs and lets you add examples to a dataset.
- **Subjects that are not questions:**
  - The learner's project as a separate question — it changes nothing beyond what C1 already asks (fails 5.2 test 3).
  - A retrieval method other than meaning similarity (the course: a retriever can be "any method that takes in a query and returns documents") — would break pattern-card item 2 (fails test 1).
  - Sending the whole collection to the model without retrieval — breaks item 2 (fails test 1).
  - Grading by exact or pattern matching — shown failing (F1; fails test 2); it is a rule (R6).
  - The one-line index shortcut versus the step-by-step build — the course says "these two things equate to the same result"; no learner situation changes the behavior (fails test 3).
  - The course's earlier "by hand" answer (joining retrieved texts and calling the model directly) — the same stages without the don't-know instruction; no situation needs it over R3 (fails test 3).
  - Conversation memory, chains (simple/sequential/router), output parsers and agents — other lessons; they change no stage of this program, and the pattern card lists them as background, not offered.
  - Retrieval count, temperatures, separator, generated-example count, debug default — settings (section 5.5), never asked.
  - Which model the tests run against — never asked; tests run on stand-ins, `live` tests on the real provider when a key is present.
- **Where each picked value came from:** S1 transcript (four documents returned); S2 notebooks (temperature 0.0); S3 Evaluation notebook vs Q&A notebook default, picked by "the course's final end-to-end app"; S4 Evaluation notebook (first five rows), matching the transcript's "seven examples total" (2 hand-written + 5 generated); S5 notebook sets none, Models lesson says default 0.7; S6 Evaluation notebook; S7 Evaluation lesson.

### Names that go stale (search keywords against current docs, not guaranteed imports)
- Course pins: `langchain==0.0.179`, `openai==0.27.7`.
- Models: `gpt-3.5-turbo`, `gpt-3.5-turbo-0301`, `text-davinci-003` (deprecated 1 January 2024 per the course notebook), `gpt-3.5-turbo-instruct`; default OpenAI embeddings.
- Classes and functions: `ChatOpenAI`, `OpenAI`, `OpenAIEmbeddings`, `CSVLoader`, `DocArrayInMemorySearch` (needs `docarray`), `VectorstoreIndexCreator`, `RetrievalQA` (chain type "stuff", option `document_separator`), `as_retriever`, `similarity_search`, `embed_query`, `QAGenerateChain` (`apply_and_parse`), `QAEvalChain` (`evaluate`), `langchain.debug`, `load_dotenv`.
- Request-parameter limits: course-era chat models accepted `temperature`; some current model families reject it or accept only the default. If so, leave it unset and record it (S2, S6).

### Course names
| Course name | Spec term |
|---|---|
| vector store / vector database / index | store |
| chunk / document | piece / document |
| embeddings | embedder |
| retriever, similarity search | retrieve stage |
| `chain_type="stuff"` / map_reduce / refine / map_rerank | C7a / C7b / C7c / C7d |
| QA generation chain | example generator role |
| QA eval chain | grader role |
| query / answer (example keys) | `query` / `answer` in the Example schema (binding) |
| `result` (predicted answer) | `predicted_answer` |
| debug mode | debug switch (R8) |

### Lesson map (transcript numbering)
- **L1 Introduction** — framing only.
- **L2 Models, Prompts and Parsers** — default temperature 0.7 vs 0 (S2, S5); parser failure (background).
- **L3 Memory** — background only (pattern card: not offered).
- **L4 Chains** — background only.
- **L5 Question and Answer** — the program, stages, the pattern-card quotes, S1, C1, C4–C7, the one-line shortcut (D6).
- **L6 Evaluation** — the final end-to-end version: separator S3, examples S4, grading, F1, R3's instruction text, debug, hosted platform (C8, C9, D7–D10).
- **L7 Agents** — background only.
- **L8 Conclusion** — no notes.

The notebook files number lessons differently (their Q&A notebook is labelled lesson 4); the transcript numbering above is used. Slides read: 7 Q&A slides (talked through in L5: documents and context length, embeddings, vector database create/index, stuff method pros and cons, the three additional methods — two copies of the same slide), 4 Chains slides (L4), 2 Memory slides (L3); all were talked through and counted as their lesson's transcript; none disagreed with code or transcripts. Course disagreements recorded: the separator (S3); the Agents lesson's tools (transcript: web search and Wikipedia; notebook: a calculator tool and Wikipedia — background only). Nothing in this spec requires access to the course.

---

*Spec v2-draft · course: LangChain for LLM Application Development · project: Ask Your Documents · when the build agent does something unexpected, add the missing constraint here and re-run.*
