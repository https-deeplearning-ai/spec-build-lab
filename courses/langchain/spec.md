# Spec: Ask-your-documents question answering

**What you're building:** a small command-line program that loads a collection of documents (by default an outdoor-clothing product catalog that ships with this spec as sample data), indexes every document by meaning, and answers your plain-language questions from the few documents most similar to each question. When those documents do not hold the answer, it says it doesn't know. It also checks its own answer quality on a set of example questions and grades them with a language model.

**Fastest path:** when the build agent asks, answer **"recommended build"**. The build is done when the offline tests pass. They need no key and no network. An `OPENAI_API_KEY` only unlocks the `live` tests and real use of the finished program.

This file is self-contained: the build agent needs nothing else.

*Provenance: course "LangChain for LLM Application Development"; materials used: lesson transcripts (8 lessons), notebook code for 6 notebooks, 14 slide images, owner-confirmed pattern card (reconfirmed 2026-10-26); generated 2026-10-26 with guide v2.5 (2026-10-26).*

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
   checklist in step 5 marks each place it differs from the course), or **choose** question by
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

### C1. What documents will the program read?
- **C1a. A table file (CSV), where each row is one document (Recommended - course default).** Pick this when your material is already a list of records such as products, contacts or FAQ entries. Setup cost: none.
- **C1b. A folder of plain-text or Markdown files, where each file is one document.** Pick this when your material is notes or articles you write as files, for example "ask my English notes". Setup cost: none.
  *What to check:* every `.txt`/`.md` file in the folder becomes exactly one document whose text is the whole file and whose source names the file.
- **C1c. PDF files, where each page is one document.** Pick this when your material comes as PDFs, such as manuals, papers or reports. Setup cost: one PDF-reading package. Scanned PDFs without a text layer give no text.
  *What to check:* a 3-page sample PDF becomes 3 documents, each holding that page's text and naming the file and page number as its source.

### C2. Which provider runs the language model (it answers, writes example questions and grades)?
- **C2a. OpenAI's hosted chat models (Recommended - course default).** Pick this when you have, or can get, an OpenAI API key and are fine with retrieved document pieces being sent to OpenAI. Setup cost: an OpenAI API key; you pay per token.
- **C2b. Another hosted provider you already have a key for.** Pick this when your organisation already pays for a different model provider, or you cannot send data to OpenAI. Setup cost: that provider's API key and its LangChain integration package.
  *What to check:* with that provider's key set, the live answer test (L1) passes and the trace names that provider's model.
- **C2c. A local model served on your own machine.** Pick this when your documents must not leave your machine, or you have no API key. Setup cost: a local model server and a model download of several GB. It needs a reasonably strong computer. Answers and grades are slower and may be less reliable than a hosted model's.
  *What to check:* with the network disconnected, `ask` returns an answer from the local model and the live answer test (L1) passes against it.

### C3. Which model turns text into meaning vectors (the embedder)?
- **C3a. OpenAI's hosted embedding model (Recommended - course default).** Pick this when you use an OpenAI key anyway and your collection is small enough that embedding it costs little. Setup cost: the same OpenAI API key; every document is sent to OpenAI once per index build.
- **C3b. A local embedding model.** Pick this when you don't want your whole collection sent to a provider, or embedding a large collection would cost too much. Setup cost: one package and a model download of roughly 100 MB to 1 GB. No key needed.
  *What to check:* building the index makes no network call, and the question that finds the side-pockets document in the sample (Q2) still ranks that document first.

### C4. How will people ask their questions?
- **C4a. A command-line program (Recommended).** Pick this when you will ask questions yourself from a terminal. Setup cost: none.
- **C4b. A small web page served on your own machine.** Pick this when people who don't use a terminal will ask questions. Setup cost: one small web-framework package.
  *What to check:* submitting the side-pockets question (Q2) in the page shows the same answer the command line gives, and the trace option shows the same steps.

### C5. Should long documents be split into smaller pieces before indexing?
- **C5a. No: each document is indexed whole (Recommended - course default).** Pick this when each document is short, like a product row or an FAQ entry, so that 4 whole documents fit easily in one prompt. Setup cost: none.
- **C5b. Yes: split each document into overlapping pieces of about 1,000 characters with 200 characters of overlap.** These sizes are an addition: the course gave no size. Pick this when your documents are long notes, chapters or PDFs, where a whole document would crowd out the others or not fit in the model's context, and the answer usually sits in one passage. Setup cost: none.
  *What to check:* each piece remembers which document it came from, and the pieces of one document together hold the whole document.

### C6. Where is the index kept?
- **C6a. In memory, rebuilt every time the program starts (Recommended - course default).** Pick this when your collection is small enough that re-embedding it at every start takes seconds and costs little. Setup cost: none; no database to run.
- **C6b. Saved to a file on disk and rebuilt only when the documents change.** Pick this when your collection is large enough that re-embedding at every start is slow or costs noticeable money. Setup cost: one embedded vector-store package; no server.
  *What to check:* a second start with unchanged documents makes no embedding calls for documents, and changing one document re-embeds only what changed or rebuilds the index.
- **C6c. A separate vector database server.** Pick this when several programs or people must query one shared index, or the collection is too big for one machine's memory. Setup cost: running a database server (container or hosted account) and its connection settings.
  *What to check:* after indexing, the server holds one entry per document (or piece) with its text and source, and the side-pockets question (Q2) retrieves the same top document as in memory.

### C7. How are the retrieved pieces combined into one answer?
- **C7a. Stuff: put all retrieved pieces into one prompt and make one model call (Recommended - course default).** Pick this when the retrieved pieces are few and short. It is the simplest and cheapest method and easy to follow. Its limit: with large or many pieces the prompt grows past the model's context length and the call fails. Setup cost: none.
- **C7b. Map-reduce: ask the question of each piece separately, then make one more call that combines the separate answers.** Pick this when you retrieve many pieces, or long ones, that together would not fit in one prompt. The per-piece calls can run in parallel. Costs: many more model calls, and each piece is treated as independent of the others. Setup cost: none beyond the extra token cost.
  *What to check:* with 4 retrieved pieces the model is called 5 times (4 per-piece calls, then 1 combining call), and the final answer is the combining call's reply.
- **C7c. Refine: go through the pieces one at a time, improving the answer with each.** Pick this when an answer must combine details spread across many pieces and you accept slower answers. Costs: about as many calls as map-reduce, but they run one after another, so it is slower, and answers tend to be longer. Setup cost: none beyond the extra token cost.
  *What to check:* with 4 retrieved pieces the model is called 4 times in retrieval order, each call after the first receives the previous call's answer, and the last reply is returned.
- **C7d. Map-rerank: ask each piece separately for an answer plus a relevance score, and keep the highest-scoring answer.** Pick this when each answer is normally found in a single piece and you want the answer from the best-matching one. Costs: one call per piece, which can run in parallel, and it depends on the model scoring sensibly, so the scoring instructions need care. Setup cost: none beyond the extra token cost.
  *What to check:* with 4 retrieved pieces the model is called 4 times, each reply carries a score, and the returned answer is the one with the highest score.

### C8. How can you see what happened inside one run?
- **C8a. A local trace switch, off by default, that prints each step of a run (Recommended - course default).** Pick this when you debug wrong answers on your own machine. Most often the retrieval step, not the model, is what went wrong. Setup cost: none.
- **C8b. The local trace switch, plus sending every run to a hosted tracing and evaluation dashboard.** Pick this when you want a history of runs across sessions, want to share runs with a team, or want to grow your example set by adding real runs to a dataset as you go. Setup cost: an account and API key for the dashboard service; your questions, document pieces and answers are sent to that service.
  *What to check:* with the dashboard key set, one `ask` run appears in the dashboard with the retrieval step and the model call as separate nested steps.

### C9. How is answer quality checked?
- **C9a. Hand-written example questions plus questions a model writes from the documents, all graded by a model (Recommended - course default).** Pick this when you want a quick, growing test set without writing every question yourself. Setup cost: extra model calls for generating and grading.
- **C9b. Only hand-written example questions, graded by a model.** Pick this when you want every expected answer checked by a person, or want fewer model calls. Costs: writing examples by hand is slow and doesn't scale. Setup cost: you write the examples file.
  *What to check:* `eval` grades exactly the examples in the hand-written file, in file order, and the generator role is never called.
- **C9c. No evaluation stage.** Pick this when you only want a personal tool and will judge each answer yourself as you read it. Setup cost: none; it saves the extra model calls.
  *What to check:* the program has no `eval` command, and asking a question still works and passes T1–T8.

### Departures from the course (the recommended build)
| # | Where the build differs | Why |
|---|---|---|
| D1 | Offline tests use scripted **stand-ins** for every model role and the embedder (section 6, "Scripted stand-ins"). The finished program uses the real provider when `OPENAI_API_KEY` is set. | The course called OpenAI live for everything; tests must run without a key. |
| D2 | A command-line program (`ask`, `eval`) instead of notebook cells; answers print as text. | The course ran in notebooks; a notebook is never the build. Addition. |
| D3 | Model names: the build agent picks current models. The course used `gpt-3.5-turbo` (or `gpt-3.5-turbo-0301` before 2024-06-12) for chat, an unnamed default OpenAI embedding model, and `gpt-3.5-turbo-instruct` for the one-line index query. | Course model names go stale. |
| D4 | Libraries are current releases. The course's install lines were unpinned. A notebook note says it ran `langchain==0.0.179` and `openai==0.27.7`. | Guide rule: pin only what the install lines pinned. |
| D5 | The in-memory store is today's LangChain in-memory vector store. The course used the `DocArrayInMemorySearch` class. | Class names go stale; the behaviour is the same (in memory, no external database). |
| D6 | Retrieved pieces are joined with the separator `<<<<>>>>>`. | The course's final version (the evaluation lesson) set this. The earlier Q&A lesson used the library's default separator. |
| D7 | The similarity measure is cosine, and ties go to the document that comes first in the file. | The course said only "the n most similar". Addition, for reproducibility. |
| D8 | Each answer result also carries the ids and scores of the retrieved documents (shown in the trace). | Addition, so tests and the trace can see retrieval. |
| D9 | The generator returns a JSON object `{"query", "answer"}`. Grades are normalised to `CORRECT`/`INCORRECT`, and the evaluation report is also written to `eval_report.json` with a summary count. | Addition. The course printed the model's raw grade text in the notebook. |
| D10 | Hand-written examples live in a file (`sample_data/hand_examples.json`), not in code. | Addition, so learners can edit them. |
| D11 | Without a key and without injected stand-ins, the program exits with a message naming `OPENAI_API_KEY`. | Addition. |
| D12 | The sample catalog and examples were written for this spec. No course data is copied. | Guide rule (own sample data). |
| D13 | One way to build the index. The course showed a one-line index creator and a step-by-step version and said both give the same result. | Same behaviour, so only one path is needed. |

---

## 2. Objective
Answer a person's plain-language questions about their own collection of documents, using only the few documents most similar in meaning to each question, and measure how often the answers are right.

## 3. Tech stack and versions
- **Python** 3.11 or newer (addition: the course ran Python notebooks and stated no version).
- **LangChain**, current release, with its OpenAI integration and its in-memory vector store. The course's install lines were unpinned (`pip install --upgrade langchain`); see D4.
- **python-dotenv**, current release: reads a local `.env` file, as the course did.
- **pytest**, current release (addition): the test runner.
- Package name `docqa`; command entry `python -m docqa`.

**Secrets:** `OPENAI_API_KEY` comes from the environment or a local `.env` file. It is never written to code, logs, the trace or `resolved-decisions.md`. `.env` is listed in `.gitignore`.

## 4. Contracts

**Document** (one per CSV row under C1a):
```json
{"type":"object","required":["doc_id","text","source"],"additionalProperties":false,
 "properties":{
  "doc_id":{"type":"integer","minimum":1,"description":"1-based row number in file order"},
  "text":{"type":"string","minLength":1,"description":"each column as '<column>: <value>' lines, in column order, joined by newlines (addition)"},
  "source":{"type":"object","required":["file","row"],"properties":{"file":{"type":"string"},"row":{"type":"integer","minimum":1}}}}}
```

**Index entry** (held in memory; one per document; built before any question is accepted):
```json
{"type":"object","required":["doc_id","text","vector","source"],
 "properties":{"doc_id":{"type":"integer"},"text":{"type":"string","description":"identical to Document.text"},
  "vector":{"type":"array","items":{"type":"number"},"minItems":1},"source":{"type":"object"}}}
```

**Answer result** (what `ask` produces):
```json
{"type":"object","required":["question","answer","retrieved"],
 "properties":{"question":{"type":"string","minLength":1},"answer":{"type":"string","minLength":1},
  "retrieved":{"type":"array","maxItems":4,"description":"length = retrieval_k, best first",
   "items":{"type":"object","required":["doc_id","score"],"properties":{"doc_id":{"type":"integer"},"score":{"type":"number"}}}}}}
```

**Example** (evaluation input):
```json
{"type":"object","required":["query","answer","origin"],
 "properties":{"query":{"type":"string","minLength":1},"answer":{"type":"string","minLength":1},
  "origin":{"enum":["hand","generated"]}}}
```

**Graded record** (evaluation output; `eval_report.json` holds `{"records":[...], "summary":{"correct":int,"total":int}}`):
```json
{"type":"object","required":["query","answer","result","grade"],
 "properties":{"query":{"type":"string"},"answer":{"type":"string","description":"the real (expected) answer"},
  "result":{"type":"string","description":"the program's predicted answer"},"grade":{"enum":["CORRECT","INCORRECT"]}}}
```

**Command line:**
- `python -m docqa ask "<question>" [--data PATH] [--k N] [--trace]` prints the answer line. With `--trace` it also prints the trace (R9).
- `python -m docqa eval [--data PATH] [--examples PATH] [--report PATH] [--trace]` prints, for each example, `Question:`, `Real Answer:`, `Predicted Answer:` and `Predicted Grade:` lines, then `Summary: <correct>/<total> CORRECT`, and writes the report file.

### Model roles
| Role | What it does | Course model (fact about the course) | Temperature |
|---|---|---|---|
| answerer | writes the answer from the question and the retrieved pieces | `gpt-3.5-turbo` via the chat-model wrapper | 0.0 |
| example generator | writes one question-and-answer pair from one document | `gpt-3.5-turbo` | left unset (course) |
| grader | grades a predicted answer against the real answer by meaning | `gpt-3.5-turbo` | 0 |
| embedder | turns document text and questions into vectors | OpenAI's default embedding model (unnamed in the course; "over a thousand" numbers per vector) | — |

### Settings
| Setting | Value | Source | Change this when … |
|---|---|---|---|
| `retrieval_k` | 4 | Q&A lesson: the default similarity search "returns four documents" | answers need more context than 4 pieces hold (with stuff, keep the prompt under the context length) |
| `document_separator` | `<<<<>>>>>` | Evaluation lesson, final Q&A chain | your documents themselves contain that string |
| `answer_temperature` | 0.0 | Q&A and evaluation lessons; the instructor sets 0 "to make this output a little bit less random" | you want more varied wording |
| `grader_temperature` | 0 | Evaluation lesson | — |
| `generator_temperature` | unset (provider default) | Evaluation lesson: the generator model was created without a temperature; L2 transcript: the default "is 0.7" | you want more or less varied generated questions |
| `generated_from_first_n_docs` | 5 | Evaluation lesson: one generated pair from each of the first 5 documents | you want a bigger generated set |
| `trace` | off | Evaluation lesson: debug turned on to inspect, then off for batch runs | you are debugging a wrong answer |
| `data_path` | `sample_data/catalog.csv` | addition | you point it at your own file |
| `examples_path` | `sample_data/hand_examples.json` | addition | you write your own examples |
| `report_path` | `eval_report.json` | addition | — |

## 5. Business rules

**What must stay true** (the course's pattern card; every option keeps every item):
1. **The documents are indexed by meaning before any question.** Each piece of text gets a numeric representation of its meaning, stored next to its original text, so pieces with similar meaning can be found later. → T1, T2
2. **For each question, only the few stored pieces most similar in meaning are retrieved, not the whole collection.** → T3, T5
3. **A language model writes the answer from the question plus the retrieved pieces, so the answer rests on the person's documents.** → T6, T8

**Rules of the recommended build:**
- **R1. Index at start.** On start, the program loads every document from the data file (one per CSV row, in file order), embeds each document's text once, and stores an index entry holding the vector next to the unchanged text and its source. No question is accepted until indexing has finished. → T1, T2, L1
- **R2. Retrieve by meaning.** For a question, the program embeds the question with the same embedder used for the documents and scores every index entry by cosine similarity. If either vector is all zeros, the score is 0. It returns the `retrieval_k` highest-scoring entries, best first, with ties going to the lower `doc_id`. Documents are never re-embedded per question. Only the retrieved entries go on to the next step, never the whole collection (the course: language models "can only inspect a few thousand words at a time"). → T2, T3, T4, T5, L1
- **R3. Stuff prompt, one call.** The answerer gets one call with two messages. The **system message** starts with the instruction "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer." It is followed by a blank line and then the retrieved pieces' texts, best first, joined by `document_separator`. The **human message** is the question, unchanged. The answer is the model's reply, unchanged. → T5, T6, T14, L1
- **R4. Say "I don't know".** When the retrieved pieces don't hold the answer, the program's answer says it doesn't know rather than inventing one. It never answers from outside knowledge in place of the documents. → T4, T7, T8, L2
- **R5. Model settings.** The answerer is called with `answer_temperature`, the grader with `grader_temperature`, and the generator with no temperature set. → T6, T9, T10
- **R6. Build the example set.** `eval` loads the hand-written examples (origin `hand`) in file order. It then asks the generator for one pair from each of the first `generated_from_first_n_docs` documents, in file order (origin `generated`). The generator gets one document's text and replies with a JSON object `{"query": ..., "answer": ...}`. Hand-written examples come first. → T9, L3
- **R7. Grade by meaning, never by string match.** Every grade comes from the grader role, which gets the question, the real answer and the predicted answer and replies with a grade. The program maps a reply that starts with `CORRECT` to `CORRECT` and anything else to `INCORRECT`. The program never decides a grade by comparing strings itself: a correct answer can share no words with the real answer (planted failure F1). → T10, T11, L3
- **R8. Evaluation run.** `eval` gets a predicted answer for every example by running its query through the same ask pipeline (R2–R4). It grades each one (R7), prints the four lines per example and the summary, and writes `report_path`. → T12, L3
- **R9. Trace switch.** With trace off, `ask` prints only the answer line. With trace on, it also prints, in order: the question; each retrieved `doc_id` with its score; the full system and human messages sent to the answerer; the model's reply; and the token usage and model name when the provider reports them. → T13, T14
- **R10. Missing key.** If no `OPENAI_API_KEY` is set and no stand-ins are injected, `ask` and `eval` exit with code 2, print a message naming `OPENAI_API_KEY` to standard error, make no model call and write no file. → T15

## 6. Tests

### Sample data
**`sample_data/catalog.csv`**: header `name,description`, 8 rows (doc_id = row number):

| doc_id | name | description |
|---|---|---|
| 1 | Sunridge Linen Shirt | Long-sleeve linen shirt with UPF 50+ sun protection. Two chest pockets. Weighs 7 oz. |
| 2 | Trailbreeze Tech Tee | Short-sleeve tee made of sun-blocking fabric rated UPF 30. Dries quickly. |
| 3 | Harbor Rain Shell | Waterproof rain jacket from the StormGuard collection. Packs into its own pocket. |
| 4 | Fireside Fleece Pullover Set | Fleece pullover with matching pants. The set has side pockets. |
| 5 | Summit 800 Down Parka | Warm parka filled with 800-fill down, from the LoftCore collection. |
| 6 | Canyon Hiking Shorts | Quick-dry hiking shorts with five pockets. |
| 7 | Alpine Wool Socks | Merino wool socks sold as a 3-pack. |
| 8 | Riverbend Sandals | Water-friendly sandals with a grippy rubber sole. |

Each document's text is `name: <name>\ndescription: <description>`. Only doc 4 contains the words "side pockets", and only doc 5 contains "LoftCore".

**`sample_data/hand_examples.json`**: a list of two examples:
- H1 `{"query": "Does the Fireside Fleece Pullover Set have side pockets?", "answer": "Yes"}` is **planted failure F1**: the correct predicted answer shares almost no text with "Yes".
- H2 `{"query": "What collection is the Summit 800 Down Parka from?", "answer": "The LoftCore collection"}`

**Sample questions:** Q1 "Please suggest a shirt with sunblocking"; Q2 = H1's query; Q3 = H2's query; Q4 "Do you sell a tent?" (planted: the answer is in no document).

### Scripted stand-ins (tests only; each is labelled as a stand-in in its code and stands in for a real model)
- **Stand-in embedder** (stands in for the embedding model). It lowercases the text, splits it into tokens matching `[a-z0-9]+(-[a-z0-9]+)*`, and counts tokens per concept, giving an 8-number vector in this order:
  1. sun {sun, sun-blocking, sunblocking, upf, uv}
  2. shirt {shirt, shirts, tee}
  3. water {rain, waterproof, water, water-friendly}
  4. pocket {pocket, pockets}
  5. warm {warm, fleece, down, wool, parka}
  6. collection {collection}
  7. feet {socks, sandals}
  8. legs {shorts, pants}

  It counts its calls. Resulting document vectors:
  - 1 = [2,2,0,1,0,0,0,0]
  - 2 = [2,2,0,0,0,0,0,0]
  - 3 = [0,0,3,1,0,1,0,0]
  - 4 = [0,0,0,1,2,0,0,1]
  - 5 = [0,0,0,0,5,1,0,0]
  - 6 = [0,0,0,1,0,0,0,2]
  - 7 = [0,0,0,0,2,0,2,0]
  - 8 = [0,0,1,0,0,0,2,0]
- **Stand-in answerer** (stands in for the chat model). It records every call's messages and temperature. It looks only at the **system message**:
  - Q1 → if it contains both "Trailbreeze Tech Tee" and "Sunridge Linen Shirt", reply "The Trailbreeze Tech Tee and the Sunridge Linen Shirt both block the sun."
  - Q2 → if it contains "side pockets", reply "Yes, the Fireside Fleece Pullover Set has side pockets."
  - Q3 → if it contains "LoftCore", reply "The Summit 800 Down Parka is from the LoftCore collection."
  - "What does the <name> offer?" → if it contains "name: <name>", reply "The <name>: <first sentence of that document's description>" (no extra period)
  - In every other case it replies "I don't know."
- **Stand-in generator** (stands in for the chat model in the generator role). For a document with name N and description D, it replies `{"query": "What does the N offer?", "answer": "<first sentence of D>"}`. The first sentence is the description up to and including the first period that is followed by a space, or the whole description when there is none. It records the temperature it got.
- **Stand-in grader** (stands in for the chat model in the grader role). Its key phrase is "side pockets" for H1's query, "LoftCore" for H2's query, and the real answer for every other query. It replies `CORRECT` if the predicted answer contains the key phrase (ignoring case) and `INCORRECT` otherwise. It records the temperature it got. A test may override it with a fixed reply.

### Test table
All tests are offline with the stand-ins injected, unless marked `live`.

| Test | Given | When | Then | Rules |
|---|---|---|---|---|
| T1 | fresh start, catalog.csv | the index is built | it holds 8 entries; entry *i* has doc_id *i*, text exactly `name: …\ndescription: …` from row *i*, source `{file: "catalog.csv", row: i}`, and the 8-number vector listed above | R1, item 1 |
| T2 | fresh start | the index is built, then Q2 is asked | the embedder has been called 8 times before Q2 and exactly 9 times after it (only the question was embedded) | R1, R2, item 1 |
| T3 | index built | Q1, Q2, Q3 are asked | retrieved doc_ids are Q1 → [2,1,3,4] (scores 1.0, 0.943, 0, 0), Q2 → [4,5,7,6] (0.866, 0.693, 0.5, 0.316), Q3 → [5,4,7,3] (0.965, 0.730, 0.632, 0.135), scores to 3 decimals | R2, item 2 |
| T4 | index built, `--k 1` | Q1 is asked | retrieved = [2]; the answer is "I don't know." (doc 1 was not retrieved) | R2, R4 |
| T5 | index built | Q2 is asked | the system message contains the texts of docs 4, 5, 7, 6 in that order and none of docs 1, 2, 3, 8; `<<<<>>>>>` appears in it exactly 3 times | R2, R3, item 2 |
| T6 | index built | Q2 is asked | the answerer is called exactly once with temperature 0.0; the system message starts with the R3 instruction sentence; the human message equals Q2; the answer is "Yes, the Fireside Fleece Pullover Set has side pockets." | R3, R5, item 3 |
| T7 | index built | Q4 is asked | retrieved = [1,2,3,4] (all scores 0); the answer is "I don't know." | R4 |
| T8 | an index built from catalog.csv without row 4 (copied inside the test; the sample file is unchanged) | Q2 is asked | the answer is "I don't know." | R4, item 3 |
| T9 | fresh start | `eval` builds its examples | 7 examples: H1, H2 (origin `hand`), then generated queries "What does the Sunridge Linen Shirt offer?", "…Trailbreeze Tech Tee…", "…Harbor Rain Shell…", "…Fireside Fleece Pullover Set…", "…Summit 800 Down Parka…" with answers equal to each description's first sentence; the generator was called 5 times with no temperature | R5, R6 |
| T10 | stand-in grader | H1's query, real "Yes", predicted "I don't know." are graded | the grade is `INCORRECT`; the grader got temperature 0 | R5, R7 |
| T11 | planted F1 | H1 is run through `eval` | the predicted answer "Yes, the Fireside Fleece Pullover Set has side pockets." is not equal to "Yes", yet the grade is `CORRECT`. Then, with the grader overridden to always reply `INCORRECT`, grading H1's query with real "Yes" and predicted "Yes" gives `INCORRECT` (the grade comes only from the grader) | R7 |
| T12 | fresh start, no `eval_report.json` | `python -m docqa eval` runs | it prints 7 blocks of Question / Real Answer / Predicted Answer / Predicted Grade and then `Summary: 7/7 CORRECT`; `eval_report.json` now exists with 7 records, all `CORRECT`, and summary `{correct: 7, total: 7}` | R8 |
| T13 | trace off (default) | Q2 is asked from the command line | standard output is exactly the answer line | R9 |
| T14 | `--trace` | Q2 is asked | the output contains, in order: Q2; doc_ids 4, 5, 7, 6 with their T3 scores; the R3 instruction sentence; 3 occurrences of `<<<<>>>>>`; the answer | R9, R3 |
| T15 | `OPENAI_API_KEY` unset, no stand-ins injected | `ask` Q2 runs, then `eval` runs | each exits with code 2; standard error names `OPENAI_API_KEY`; no `eval_report.json` is written | R10 |
| L1 `live` | key set, real models, catalog.csv | Q2 is asked | retrieved[0] is doc 4 and the answer confirms side pockets (the real grader grades it `CORRECT` against "Yes") | R1, R2, R3 |
| L2 `live` | key set | Q4 is asked | the answer says it doesn't know or that the catalog has no tent; it names no tent product | R4 |
| L3 `live` | key set | `eval` runs | the report has 7 records; H1 and H2 are graded `CORRECT`; every grade is `CORRECT` or `INCORRECT` | R6, R7, R8 |

Every outcome above was replayed by hand against the sample data and the scripted replies, with all defaults in force.

## 7. Standing permissions
- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has data; anything that sends data to a third party.
- **Never:** invent provenance; answer when the program should say it doesn't know; change sample data to make a test pass; commit secrets.

## 8. Test plan
1. Install: `python -m venv .venv && . .venv/bin/activate && pip install -U langchain langchain-openai langchain-community python-dotenv pytest` (plus the packages your chosen options need).
2. Offline: `python -m pytest -q -m "not live"`. All of T1–T15 must pass.
3. Live (only when `OPENAI_API_KEY` is set): `python -m pytest -q -m live`. L1–L3 run automatically when the key is present and are skipped otherwise.
4. Manual: `python -m docqa ask "Please suggest a shirt with sunblocking" --trace` and `python -m docqa eval`.
5. For each chosen option that is not recommended, turn its "what to check" sentence (copied into `resolved-decisions.md`) into a test, run it and report it.
6. Adjust the recommended tests for the chosen options (for example, under C5b the index holds pieces rather than whole rows; under C9c T9–T12 and L3 are dropped) and say which you changed and why.
7. Report a result per test with evidence (test output, file paths). "Should pass" counts as not run. The build is finished when the adjusted recommended tests pass and each chosen option's check passes.

Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

---

## 9. Background notes (for the build agent)

### The program
A program that answers a person's plain-language questions about their own collection of documents, using the few pieces most similar in meaning to the question. Its stages:

`load → embed → store → retrieve → answer → evaluate`

- **load:** turns the person's files into documents with a source, so answers can rest on them.
- **embed:** gives each document a meaning vector, so documents similar in meaning can be found without matching exact words.
- **store:** keeps vector and text together, so a match returns readable text.
- **retrieve:** picks only the few most similar documents, because a model "can only inspect a few thousand words at a time".
- **answer:** has a model write the answer from the question plus those documents, so it uses data the model was never trained on.
- **evaluate:** checks answer quality on example questions, so changes (another model, another store, other settings) can be judged better or worse.

The trace is not a stage: it shows what ran and does not judge it.

### Failures
- **F1 (shown in the course): exact string matching can't grade answers.** *What you see:* real answer "Yes", predicted answer "The … Pullover Set … does have side pockets": "these two strings are actually nothing alike", and string matching, exact matching or regexes "wouldn't know what to do". *Why:* free-text answers have many correct wordings. *Prevention:* a model grades by meaning (R7). Planted as H1, tested by T11.
- **F2 (warned): the whole collection doesn't fit in the model.** Models "can only inspect a few thousand words at a time". *Prevention:* only `retrieval_k` documents go into the prompt (R2). Tested by T5.
- **Warned, a cost rather than a failure:** the stuff method fails for large or many documents because the prompt exceeds the context length (Q&A slides). It is carried as C7a's limit and as the reason for C5b, C7b and C7c.
- **Warned:** when a wrong answer comes back, "it's not necessarily the language model … it's actually the retrieval step". This is the reason for the trace (R9).
- From other lessons, background only: reading a model's JSON-looking reply as a dictionary fails until it is parsed (L2); a one-exchange memory window forgets the user's name (L3); an agent wrongly concluded the 2022 World Cup had not happened and the notebook warns that agents "will sometimes come to the wrong conclusion" (L7).

### Why the questions and settings are what they are
- **C1:** the course loaded a CSV, one row per product. The instructor named PDFs, web pages and internal document collections as typical sources.
- **C2/C3:** the course used OpenAI for chat and embeddings, and says embeddings can be swapped ("flexibility over how the embeddings themselves are created"). These are two questions because a learner can choose them independently.
- **C4:** the course has no interface beyond notebooks, so it made no choice here.
- **C5:** "Because these documents are already so small, we actually don't need to do any chunking here". The instructor's diagram splits big documents into chunks first. Splitting was moved off the pattern card as a learner choice.
- **C6:** the course chose an in-memory store because "it doesn't require connecting to an external database"; it notes "many different types of vector stores" and that the store "can be swapped out".
- **C7:** stuff is "the most common … simple … quite cheap and it works pretty well". Map-reduce is second most common, "can operate over any number of documents", runs in parallel, "does take a lot more calls" and treats documents as independent. Refine builds the answer up over time and is slower, with longer answers. Map-rerank is "a bit more experimental", relies on the model's scores and makes many calls.
- **C8:** the course's debug mode printed every nested step, prompt and token usage. The hosted "Evaluation Platform" kept runs and let you add them to a dataset.
- **C9:** hand-written examples "don't really scale"; model-generated examples save time; grading is done by a model.
- **Not questions:**
  - Retrieving without embeddings (keyword or other "less advanced" retrievers): breaks pattern item 1.
  - Sending the whole collection without retrieval: breaks item 2.
  - Returning the retrieved documents with no model answer (the course's similarity-search step): breaks item 3.
  - The hand-joined prompt with no "don't know" instruction (the course's by-hand step): drops R4, so the answer no longer rests on the documents (item 3).
  - Grading by string match: the course shows it failing (F1).
  - The one-line index creator versus the step-by-step build: same result.
  - Conversation memory, chains/routers, output parsers and agents: other lessons, background only.
  - The learner's project as its own question: what it changes is covered by C1.
  - Temperatures, `retrieval_k`, separator and example counts: settings.
  - The test-suite model: always the stand-ins.
- **Picked values:**
  - `document_separator`: the evaluation lesson's final chain sets `<<<<>>>>>`; the Q&A lesson used the library default. Picked by rule (2), the final end-to-end app.
  - `retrieval_k` = 4: the library default the course used and printed ("returns four documents").
  - Temperatures: answerer 0.0 (Q&A and evaluation lessons); grader 0 (evaluation lesson); generator unset (evaluation lesson).
  - Chat models in the chains lesson used 0.9 for creative names; that is another lesson.
  - Example counts: two hand-written examples plus five generated from `data[:5]`; "seven examples total".

### Notes on the course's code
- The Q&A lesson's one-line index query used a completion model (`gpt-3.5-turbo-instruct`) because the library's default model (`text-davinci-003`) was deprecated. The step-by-step chain used the chat model.
- The by-hand step joined retrieved documents with no separator at all. The final chain used a separator.
- The evaluation loop printed the real answer from the prediction records, which carried each example's question and answer through alongside the predicted result.

### Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports:
- `ChatOpenAI`, `OpenAIEmbeddings`, `OpenAI` (completion wrapper)
- `CSVLoader`, `DocArrayInMemorySearch` (needs `docarray`), `VectorstoreIndexCreator`
- `RetrievalQA` (chain type "stuff", document separator option), `as_retriever`, `similarity_search`
- `QAGenerateChain` (`apply_and_parse`), `QAEvalChain` (`evaluate`)
- `langchain.debug`, `verbose=True`, `load_dotenv`/`find_dotenv`
- models `gpt-3.5-turbo`, `gpt-3.5-turbo-0301`, `gpt-3.5-turbo-instruct`, `text-davinci-003`
- library versions `langchain==0.0.179`, `openai==0.27.7`

Some newer reasoning-model families reject a `temperature` parameter. If the chosen model does, record that in `resolved-decisions.md` and omit the parameter.

### Course names
| Course name | This spec |
|---|---|
| `OutdoorClothingCatalog_1000.csv` | `sample_data/catalog.csv` (own data) |
| `examples` / `new_examples` | hand / generated Examples |
| `query`, `answer`, `result` | Example and Graded record fields (binding) |
| the grader's raw text output | `grade` (normalised) |
| `qa_stuff` / `qa` | the ask pipeline |
| "Predicted Grade" | printed line label (binding) |
| `deeplearningai` session | (dashboard name in C8b; not needed) |

### Lesson map (transcript numbering)
| Lesson | What this spec took from it |
|---|---|
| L1 Introduction | components overview only |
| L2 Models, Prompts and parsers | temperature 0 habit, default 0.7; parsing failure (background) |
| L3 Memory | background only |
| L4 Chains | background only |
| L5 Question and Answer | the whole program, the stages, stuff and the other three methods, store, embeddings, k = 4, chunking remark |
| L6 Evaluation | final Q&A chain with separator, the "don't know" prompt, debug trace, generated and hand examples, model grading, F1, hosted platform |
| L7 Agents | background only |
| L8 Conclusion | none |

- The notebook files count lessons differently (their "L4-QnA" is transcript L5); transcript numbering is used here.
- All 14 slides were read. The seven Q&A slides are talked through in L5 and counted like its transcript. They agree with it, and the stuff-method slide adds its stated pro and con.
- The four chains slides and two memory slides belong to L4 and L3: background only.
- Nothing in this spec requires access to the course.

---

*Spec draft v2 · LangChain for LLM Application Development · project: ask-your-documents · When the build agent does something unexpected, add the missing constraint here and re-run.*
