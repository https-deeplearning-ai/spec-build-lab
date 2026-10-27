# Spec: Ask your documents (question answering over a document collection)

**What you're building:** a program that answers your plain-language questions about your own collection of documents. It first indexes every document by meaning, then for each question it finds the few pieces most similar in meaning and has a language model write the answer from those pieces only. By default it answers questions about a small outdoor-clothing product catalog: you ask "Please suggest a shirt with sunblocking" and it names the catalog's sun hoodie and sun shirt. When the catalog does not hold the answer, it says "I don't know." It also checks itself: it builds a small set of test questions with known answers, runs them through the program, and has a model grade each answer CORRECT or INCORRECT.

**Fastest path:** at the first question, answer "recommended build". The build is finished when the offline tests pass. They need no key, because labelled stand-ins replace the real model and the real embedding service. Tests marked `live` are skipped when no key is set; that is expected, not a failure.

**To run for real**, the recommended build needs an OpenAI API key in the environment variable `OPENAI_API_KEY`, and network access to OpenAI for the chat model and the embedding service. Nothing else is downloaded beyond the Python packages.

This file is self-contained: everything the build needs is here.

*Provenance: course "LangChain for LLM Application Development" · materials used: lesson transcripts (8 lessons), the course notebooks (6), 13 slide images, the owner-confirmed pattern card · written 2026-10-27 · guide v2.7 (2026-10-27).*

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
   an OpenAI API key in `OPENAI_API_KEY` and network access to OpenAI), or **choose** question by
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

### C1. Which documents should the program answer questions about?
- **C1a. The sample outdoor-clothing catalog defined in this spec** (Recommended - course default). Pick this when you want to see the program work first, or to compare against the course. Setup cost: none.
- **C1b. Your own table file (CSV), one item per row.** Pick this when your information already lives in a spreadsheet-like list, such as products, contacts or inventory, where each row is short. Setup cost: none; you give the file path.
- **C1c. Your own plain-text or Markdown files in a folder.** Pick this when your documents are notes, pages or write-ups, such as "ask my English notes". Setup cost: none; you give the folder path.
- **C1d. Your own PDF files in a folder.** Pick this when your documents are reports, manuals or papers saved as PDFs. Setup cost: one extra package that reads text out of PDFs; scanned PDFs without a text layer will not work.

### C2. Which programming language should the program be written in?
- **C2a. Python** (Recommended - course default). Pick this when you have no reason to prefer another language, or you want to compare with the course. Setup cost: Python 3 and its package installer.
- **C2b. JavaScript / TypeScript (Node.js).** Pick this when the program must live inside a Node.js project you already have. The same framework ships a JavaScript package. Setup cost: Node.js and its package manager.

### C3. Which language-model provider should write the answers?
- **C3a. OpenAI** (Recommended - course default). Pick this when you have, or can get, an OpenAI key. Setup cost: an OpenAI account and API key (paid per use).
- **C3b. Another hosted provider (for example Anthropic, Google or Mistral).** Pick this when you already pay for another provider, or your organisation only allows that one. Setup cost: that provider's account and API key. Note: some providers offer no embedding service, so C6 may still need OpenAI or a local embedder.
- **C3c. A local model running on your machine.** Pick this when your documents must not leave your machine or you have no key. Setup cost: a local model server and a model download of several GB, and answers are slower and usually weaker.

### C4. How will you ask your questions?
- **C4a. From the command line: one command asks one question and prints the answer** (Recommended). Pick this when you are the only user and you work in a terminal. Setup cost: none.
- **C4b. A small web page served on your own machine.** Pick this when people who don't use a terminal will ask questions in a browser. Setup cost: one small web-framework package.

### C5. Should each document be split into smaller pieces before indexing?
- **C5a. No: each document is one piece** (Recommended - course default). Pick this when every document is short, such as one catalog row or one short note. Setup cost: none.
- **C5b. Yes: split each document into overlapping pieces of about 1000 characters, with 150 characters of overlap.** Pick this when your documents are long (pages, chapters, long notes): a long document may not fit what the model can read at once, and a small piece matches a question more sharply than a whole document. Cost: more pieces to embed, so indexing costs more; a fact split across two pieces can be missed. Setup cost: none.

### C6. Which embedding service turns text into its meaning representation?
- **C6a. OpenAI's hosted embedding service** (Recommended - course default). Pick this when you chose C3a, or have an OpenAI key anyway. Setup cost: the OpenAI key (the same one as C3a); every indexing run sends your documents to OpenAI.
- **C6b. A local embedding model running inside the program.** Pick this when your documents must not leave your machine, or you have no OpenAI key (for example with C3b or C3c). Setup cost: an embedding package and a model download of a few hundred MB; indexing a large collection is slower on a laptop.
- **C6c. Another hosted provider's embedding service.** Pick this when your organisation already uses that provider's embeddings. Setup cost: that provider's account and key.

### C7. Where is the index kept?
- **C7a. In memory, rebuilt every time the program starts** (Recommended - course default). Pick this when your collection is small and changes often; nothing to set up or clean up. Cost: every start re-embeds every document, which costs time and, with a hosted embedder, money.
- **C7b. In a file on your disk, reused at the next start and rebuilt when the documents change.** Pick this when your collection is large enough that re-embedding at every start is slow or costly. Setup cost: none beyond disk space.
- **C7c. In a separate vector database service.** Pick this when many people or programs share one large collection. Setup cost: running a database server (often in a container) or a hosted account.

### C8. How are the retrieved pieces combined into one answer?
- **C8a. All retrieved pieces go into one prompt, and the model answers in one call ("stuff")** (Recommended - course default). Pick this when the retrieved pieces are small and together fit what the model can read at once. It is the simplest, cheapest and most common method. Cost: with many or long pieces the prompt grows past what the model can read.
- **C8b. The model answers from each piece separately, then one more call combines those answers ("map-reduce").** Pick this when the retrieved pieces together are too long for one prompt. Cost: many more model calls; each piece is treated as independent of the others. The separate calls can run in parallel.
- **C8c. The model reads the pieces one after another, improving its answer with each ("refine").** Pick this when the answer must gather information spread across several pieces. Cost: as many calls as map-reduce, slower because each call waits for the previous one, and longer answers.
- **C8d. The model answers from each piece separately with a relevance score, and the best-scored answer wins ("map-rerank").** Pick this when the answer usually sits in one single piece and you want the best-supported one. Cost: one call per piece; it relies on the model scoring well, so the scoring instructions need care. The course calls it more experimental.

### C9. Should the program include a self-check (an evaluation command)?
- **C9a. Yes: an evaluation command runs a set of test questions with known answers through the program and has a model grade each answer** (Recommended - course default). Pick this when you will change the setup later (model, splitting, store, number of pieces) and want to know whether a change made answers better or worse. Setup cost: extra model calls each time you run it.
- **C9b. No evaluation command.** Pick this when it is a one-off personal tool that you check by reading its answers, and you won't tune it. Setup cost: none.

### C10. Where do the evaluation's test questions come from?
*Ask only when `C9` is `C9a`.*
- **C10a. A few questions you write by hand, plus one question-and-answer pair the model writes from each of the first few documents** (Recommended - course default). Pick this when you want a mix: a few questions you know matter, plus more without writing them all. Setup cost: one model call per generated pair.
- **C10b. Only questions you write by hand.** Pick this when you already have a list of real questions with known answers, or you don't want the model inventing questions. Cost: writing them takes time and doesn't scale.
- **C10c. Only questions the model writes from your documents.** Pick this when your collection is large and you have no time to write questions. Cost: the questions may not match what people really ask.

### C11. How can you see what happened inside one run?
- **C11a. A trace switch on the command: for that question it also prints the retrieved pieces, the full prompt sent to the model, and the token counts** (Recommended - course default). Pick this when you want to find out whether a wrong answer came from retrieval or from the model. Setup cost: none.
- **C11b. A hosted run dashboard that saves every run and lets you browse each step and add runs to an evaluation set.** Pick this when you want a lasting history of runs and want to grow your test-question set from real use over time. Setup cost: an account and API key with the dashboard service; every question, retrieved piece and answer is sent to that service.

### Departures from the course
| # | Where | The course | This spec | Why |
|---|---|---|---|---|
| D1 | Sample data | A product catalog file of outdoor clothing shipped with the course | A small 8-row catalog whose facts this spec writes (section 6.1) | No course data is copied; the tests need known facts. |
| D2 | Library versions | Pinned `langchain==0.0.179`, `openai==0.27.7` | Current releases | Course-era versions often no longer install or work with current models. |
| D3 | Model | `gpt-3.5-turbo` (with `gpt-3.5-turbo-0301` before 2024-06-12) | A current model of the chosen provider, picked by the build agent at the checklist | Model names go stale. |
| D4 | Offline tests | All runs called OpenAI | Offline tests use a scripted stand-in chat model and a stand-in embedder (labelled) | So the build can be finished and checked without a key. |
| D5 | How it is used | Notebook cells run one by one | A command-line program (`ask`, `evaluate`) with an `--offline` switch | The build is a program, not a notebook. `--offline` is an addition so you can see it work without a key. |
| D6 | Answering model | The one-line index query in the Q&A lesson used a completion-style model (the notebook replaced a retired one with `gpt-3.5-turbo-instruct`) | The chat model at temperature 0, as in the step-by-step chain and the evaluation lesson | The instructor introduced the chat model for answering; the final end-to-end app uses it (4.2 rule 1). |
| D7 | Piece separator | The Q&A lesson used the library's default separator | `<<<<>>>>>` between pieces | Taken from the course's final end-to-end app (evaluation lesson). |
| D8 | Grades | The grader's reply was printed as returned | Grades are exactly `CORRECT` or `INCORRECT`, plus a summary line | Addition, so tests can check grades. |
| D9 | Trace | A global debug switch toggled in the notebook | A `--trace` switch on one command | The same information, shown per command. Addition. |
| D10 | Example-generation prompt and grader prompt | The library's built-in prompts | Prompts with a fixed reply format defined in this spec (6.4) | Addition: the library's prompts are not in the materials, and the tests need a fixed format. |

---

## 2. Objective
Answer a person's plain-language questions about their own document collection from the few stored pieces most similar in meaning to each question, say "I don't know" when those pieces lack the answer, and grade the program's own answers against a set of test questions.

## 3. Tech stack and secrets
- **Language:** Python 3 (current release) unless C2b.
- **Framework:** the current LangChain packages (the course teaches LangChain, so the build uses it). Course-era names are search keywords only (section 9).
- **Index store (C7a):** an in-memory vector store that ships with the framework. The course used `DocArrayInMemorySearch`, which needs no external database.
- **Tests:** `pytest`, with a `live` marker for tests that need a real key.
- **Secrets:** read `OPENAI_API_KEY` (or the chosen provider's key) from the environment, or from a local `.env` file that is never committed. The course loaded it from a `.env` file. Never print a key.
- No version pins are invented. Pin what the build agent installs, in the build's own dependency file.

## 4. Contracts

### 4.1 Program surface (C4a)
- `python -m docqa ask [--offline] [--trace] "<question>"` prints the answer text to standard output and exits 0.
- `python -m docqa evaluate [--offline]` prints one block per example, then a summary line, and exits 0 (C9a).
- `--offline` uses the stand-in model and the stand-in embedder (section 6.2), and prints `[offline: stand-in model and stand-in embedder]` to standard error. *(addition)*
- Without `--offline` and without the key, the program prints `Missing OPENAI_API_KEY: set it, or use --offline` to standard error, makes no network call, and exits 2. *(addition)*
- The documents path is a setting (S1). For C1a it is `sample_data/catalog.csv`.

### 4.2 Schemas (JSON Schema, abbreviated)

**Document** (one per CSV row, under C1a/C1b and C5a):
```json
{"type":"object","required":["text","source","row"],"additionalProperties":false,
 "properties":{
  "text":{"type":"string","description":"each column as a 'column: value' line, in header order, joined by a newline"},
  "source":{"type":"string","description":"path of the file it came from"},
  "row":{"type":"integer","minimum":1,"description":"1-based data-row number in the file"}}}
```

**Index entry** (one per piece, built before any question):
```json
{"type":"object","required":["vector","text","source","row"],
 "properties":{"vector":{"type":"array","items":{"type":"number"},"minItems":1},
  "text":{"type":"string"},"source":{"type":"string"},"row":{"type":"integer","minimum":1}}}
```

**Answer result** (internal, also what `--trace` prints):
```json
{"type":"object","required":["question","answer","pieces"],
 "properties":{"question":{"type":"string"},"answer":{"type":"string"},
  "pieces":{"type":"array","minItems":0,"maxItems":4,"description":"maxItems = S2",
   "items":{"type":"object","required":["text","source","row","score"],
    "properties":{"text":{"type":"string"},"source":{"type":"string"},"row":{"type":"integer"},
     "score":{"type":"number","description":"cosine similarity, rounded to 3 places when printed"}}}}}}
```

**Evaluation example / prediction / grade** (field names follow the course):
```json
{"type":"object","required":["query","answer"],
 "properties":{"query":{"type":"string"},"answer":{"type":"string","description":"expected answer"},
  "result":{"type":"string","description":"the program's answer (prediction)"},
  "grade":{"enum":["CORRECT","INCORRECT"]},
  "origin":{"enum":["hand-written","generated"]}}}
```

### 4.3 Model roles
| Role | What it does | Course model | Temperature |
|---|---|---|---|
| Answerer | Writes the answer from the question and the retrieved pieces | `gpt-3.5-turbo` chat model | S3 = 0 |
| Question generator | Writes one question-and-answer pair from one document (C9a) | the same chat model | S6 = 0.7 |
| Grader | Grades a prediction against the expected answer (C9a) | the same chat model | S7 = 0 |
| Embedder | Turns each piece and each question into a vector | OpenAI's embedding service (model not named in the course; its vectors have "over a thousand" numbers) | — |

### 4.4 Messages sent to models
- **Answerer:** a system message, then a human message. The system message is the instruction (S4), a blank line, then the retrieved pieces' texts in rank order joined by the separator (S5) exactly, with no added characters. The human message is the question exactly as asked. One call per question (C8a).
- **Question generator** *(format is an addition)*: asks for one question and its answer from the given document text, replying in exactly two lines: `QUESTION: <question>` and `ANSWER: <answer>`. The program reads these into `query` and `answer`.
- **Grader** *(format is an addition)*: gives the question, the expected answer and the predicted answer, asks whether the predicted answer means the same as the expected one, and asks for a one-word reply, `CORRECT` or `INCORRECT`. A reply whose trimmed, upper-cased text starts with `CORRECT` is `CORRECT`; anything else is `INCORRECT`.

### 4.5 Settings
| Id | Setting | Value | Source | Change this when … |
|---|---|---|---|---|
| S1 | Documents path | `sample_data/catalog.csv` | addition (C1a) | you answered C1b–C1d. |
| S2 | Pieces retrieved per question | 4 | Q&A lesson: the similarity search "returns four documents" (library default; the course never set it) | answers miss facts spread over more pieces (raise), or prompts get too long (lower). |
| S3 | Answerer temperature | 0 | Q&A and evaluation notebooks; instructor in the prompts lesson: "set the temperature parameter to be equal to zero … to make this output a little bit less random" | you want more varied wording (not advised for answers from documents). |
| S4 | Answer instruction | "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer." | evaluation lesson, the prompt shown in debug mode | your documents are in another language (translate it, keep its meaning). |
| S5 | Piece separator | `<<<<>>>>>` | evaluation notebook, the final end-to-end app | a document itself contains that string. |
| S6 | Question-generator temperature | 0.7 | the course left it unset; the instructor states in the prompts lesson that "the default temperature is 0.7" | generated questions are too repetitive (raise) or odd (lower). |
| S7 | Grader temperature | 0 | evaluation notebook | never needed for grading. |
| S8 | Documents used for generated pairs | the first 5 documents | evaluation notebook | you want a bigger or smaller test set. |
| S9 | Hand-written examples | the 2 in section 6.1 | evaluation lesson wrote 2 by hand | you have real questions with known answers (C1b–C1d: replace them with your own). |

---

## 5. Business rules

**What must stay true** (the course's pattern card; every option keeps all three):
- **M1. The documents are indexed by meaning before any question.** Each piece of text gets a numeric representation of its meaning, stored next to its original text, so pieces with similar meaning can be found later. → T1, T2, L1
- **M2. For each question, only the few stored pieces most similar in meaning are retrieved, not the whole collection.** → T3, T4, T5, T6
- **M3. A language model writes the answer from the question plus the retrieved pieces, so the answer rests on the person's documents.** → T6, T7, T9, L2

**Rules of the recommended build:**
- **R1. Load.** Each data row of the CSV becomes one document whose text is its columns as `column: value` lines in header order, joined by newlines, and which remembers its file path and 1-based row number. *(The exact text layout is an addition.)* → T1
- **R2. Index first.** On start, before any question is answered, every document is one piece (C5a), every piece is embedded, and the index holds one entry per piece with its vector, original text, file and row. The index lives in memory and nothing is written to disk (C7a). → T2
- **R3. Retrieve.** Each question is embedded with the same embedder. It is compared with every entry by cosine similarity, and the S2 highest entries are returned, highest first. Equal scores keep the original document order. A zero vector has similarity 0 with everything. → T3, T4, T5, T9
- **R4. Answer in one call.** The answerer receives exactly the messages in 4.4, built from the retrieved pieces only, at temperature S3, in one call per question. → T6
- **R5. Answer only from the pieces.** The answer is the answerer's reply, unchanged. When the retrieved pieces lack the answer, the reply is "I don't know." The program never adds facts of its own. → T7, T8, T9, L2, L3
- **R6. Evaluation set (C9a, C10a).** The set is the S9 hand-written examples first, then one generated pair per document for the first S8 documents, in document order, each generated at temperature S6. → T10
- **R7. Predictions.** Each example's `query` runs through the full program (R3–R5), and the reply becomes `result`. → T11
- **R8. Grading by model, never by string matching.** Each prediction is graded by the grader (4.4) at temperature S7. The grade is `CORRECT` or `INCORRECT`. The program never decides a grade by comparing strings. → T11, T12
- **R9. Evaluation output.** For each example, `evaluate` prints `Example <i>:` (0-based), then `Question: `, `Real Answer: `, `Predicted Answer: ` and `Predicted Grade: ` lines, a blank line, and finally `<n correct>/<n total> CORRECT`. (The four labels follow the course; the summary line is an addition.) → T11
- **R10. Trace (C11a).** `ask --trace` additionally prints, after the answer: a `Pieces:` section with one line per retrieved piece (rank, score to 3 places, `source:row`, first line of its text); a `Prompt:` section with the full system and human messages; and a `Tokens:` line with `prompt_tokens`, `completion_tokens` and `total_tokens`. → T13
- **R11. Offline mode and keys.** `--offline` uses the stand-ins and says so on standard error. Without it and without the key, the program fails as in 4.1 and makes no network call. With the key, the real provider is used. → T14, T15

---

## 6. Tests

### 6.1 Sample data *(written for this spec; not course data)*

**File `sample_data/catalog.csv`.** Header `name,description`, then these 8 rows in this order. Quote fields as CSV requires.

| row | name | description |
|---|---|---|
| 1 | Trailblazer Sun Shirt | Lightweight nylon shirt with a UPF 50+ rating that blocks most of the sun's rays. Quick-dry fabric and two chest pockets. |
| 2 | Harbor Linen Shirt | Breathable linen shirt for hot days, with a button-down collar. |
| 3 | Ridge Sun Hoodie | Hooded shirt with UPF 40 sun protection and thumb loops. |
| 4 | Glacier Down Jacket | Part of the Summit Loft collection. Filled with 800-fill goose down and weighs 540 grams. |
| 5 | Meadow Fleece Pullover Set | Soft fleece top and joggers with two side pockets and elastic cuffs. |
| 6 | Canyon Hiking Pants | Water-resistant pants with zip-off legs. |
| 7 | Cedar Wool Socks | Merino wool socks sold as a pack of three. |
| 8 | Drift Rain Shell | Waterproof shell jacket that packs into its own pocket and weighs 310 grams. |

Document 4's text is therefore exactly `name: Glacier Down Jacket` + newline + `description: Part of the Summit Loft collection. Filled with 800-fill goose down and weighs 540 grams.`

**Hand-written examples (S9):**
- E1: query `Does the Meadow Fleece Pullover Set have side pockets?`, answer `Yes`
- E2: query `What collection is the Glacier Down Jacket from?`, answer `The Summit Loft collection`

**Planted cases:**
- P1 (the course's grading warning): E1's expected answer `Yes` and its scripted prediction share no wording, so string matching would fail them.
- P2 (the answer is not in the documents): the question `What is the return policy for worn items?`

### 6.2 Stand-ins *(labelled stand-ins, used by every offline test and by `--offline`)*

**Stand-in embedder** (stands in for the hosted embedding service). Lower-case the text and take as words the runs of letters, digits and hyphens (so `sun's` gives `sun` and `s`, and `water-resistant` stays one word). The vector has 10 numbers, one per group below. A number is 1 if any of its group's words appears, else 0. Then the vector is divided by its length; an all-zero vector stays zero.

| # | group words |
|---|---|
| 0 | sun, sunblocking, upf, uv |
| 1 | shirt, shirts, hoodie |
| 2 | jacket, shell, coat |
| 3 | pocket, pockets |
| 4 | down, fleece, wool, warm |
| 5 | rain, waterproof, water-resistant, wet |
| 6 | weigh, weighs, weight, grams |
| 7 | collection |
| 8 | pants, legs |
| 9 | socks, sock |

**Stand-in chat model** (stands in for the hosted chat model). It records every call: its messages and its temperature. It reports token usage as word counts: `prompt_tokens` = whitespace-separated words in all messages sent, `completion_tokens` = words in its reply, `total_tokens` = their sum. Its reply depends on the role.

*Answerer:* it looks up the human message (trimmed) in this table. If found, and every required phrase appears in the system message (case-sensitive), it replies with that row's reply. Otherwise it replies `I don't know.`

| id | question | required phrases | reply |
|---|---|---|---|
| A1 | Please suggest a shirt with sunblocking | `Ridge Sun Hoodie`, `Trailblazer Sun Shirt` | The Ridge Sun Hoodie (UPF 40) and the Trailblazer Sun Shirt (UPF 50+) both protect you from the sun. |
| A2 | Does the Meadow Fleece Pullover Set have side pockets? | `two side pockets` | Yes, the Meadow Fleece Pullover Set has two side pockets. |
| A3 | What collection is the Glacier Down Jacket from? | `Summit Loft collection` | The Glacier Down Jacket is part of the Summit Loft collection. |
| A4 | What UPF rating does the Trailblazer Sun Shirt have? | `UPF 50+ rating` | The Trailblazer Sun Shirt has a UPF 50+ rating. |
| A5 | What fabric is the Harbor Linen Shirt made of? | `Breathable linen shirt` | The Harbor Linen Shirt is made of breathable linen. |
| A6 | What UPF rating does the Ridge Sun Hoodie have? | `UPF 40` | The Ridge Sun Hoodie has UPF 40 sun protection. |
| A7 | How much does the Glacier Down Jacket weigh? | `540 grams` | The Glacier Down Jacket weighs 540 grams. |
| A8 | What kind of cuffs does the Meadow Fleece Pullover Set have? | `elastic cuffs` | The Meadow Fleece Pullover Set has elastic cuffs. |

*Question generator:* it finds the `name: ` line of the document in its prompt and replies with that row's two lines. An unknown name gets `QUESTION: What is this item?` / `ANSWER: Unknown`.

| name | reply |
|---|---|
| Trailblazer Sun Shirt | `QUESTION: What UPF rating does the Trailblazer Sun Shirt have?` / `ANSWER: UPF 50+` |
| Harbor Linen Shirt | `QUESTION: What fabric is the Harbor Linen Shirt made of?` / `ANSWER: Linen` |
| Ridge Sun Hoodie | `QUESTION: What UPF rating does the Ridge Sun Hoodie have?` / `ANSWER: UPF 40` |
| Glacier Down Jacket | `QUESTION: How much does the Glacier Down Jacket weigh?` / `ANSWER: 540 grams` |
| Meadow Fleece Pullover Set | `QUESTION: What kind of cuffs does the Meadow Fleece Pullover Set have?` / `ANSWER: Elastic cuffs` |

*Grader:* it replies `CORRECT` when the (question, predicted answer) pair is one of the 8 (question, reply) pairs in the answerer table above (A1–A8). Otherwise it replies `INCORRECT`. (It stands in for a model judging meaning. It is a lookup, not string matching between the expected and predicted answers.)

### 6.3 Test table
All offline tests use the sample data, the stand-ins and the settings at their values in 4.5, unless a test says otherwise. Scores are cosine similarities rounded to 3 places.

| Test | Rules | Given | When | Then |
|---|---|---|---|---|
| T1 | R1, M1 | `sample_data/catalog.csv` | the documents are loaded | there are 8 documents in row order; document 4 has the exact text given in 6.1, source `sample_data/catalog.csv` and row 4. |
| T2 | R2, M1 | a fresh start, offline | the index is built | it holds 8 entries before any question, each with a vector of 10 numbers, its document's exact text, source and row. Entry 1's vector is non-zero in groups 0, 1 and 3 only; entry 2's in group 1 only. No file is created or changed in the project folder. |
| T3 | R3, M2 | the index from T2 | retrieve `Please suggest a shirt with sunblocking` | exactly 4 pieces: Ridge Sun Hoodie 1.000, Trailblazer Sun Shirt 0.816, Harbor Linen Shirt 0.707, Glacier Down Jacket 0.000. |
| T4 | R3, M2 | the index from T2 | retrieve E1's query | Meadow Fleece Pullover Set 1.000, Cedar Wool Socks 0.500, Trailblazer Sun Shirt 0.408, Glacier Down Jacket 0.354. Glacier ranks above Drift Rain Shell (also 0.354) because it comes first. |
| T5 | R3, M2 | the index from T2 | retrieve E2's query | Glacier Down Jacket 0.866, Meadow Fleece Pullover Set 0.408, Cedar Wool Socks 0.408, Drift Rain Shell 0.289. |
| T6 | R4, M2, M3 | offline | `ask "Please suggest a shirt with sunblocking"` | exactly 1 answerer call, at temperature 0. Its system message starts with S4, then a blank line, then the texts of Ridge, Trailblazer, Harbor and Glacier in that order, joined by `<<<<>>>>>`, which appears exactly 3 times. The system message does not contain `Meadow`, `Canyon`, `Cedar` or `Drift`. The human message equals the question. |
| T7 | R5, M3 | as T6 | the answer is printed | the output is exactly A1's reply; exit code 0. |
| T8 | R5 | offline (P2) | `ask "What is the return policy for worn items?"` | 4 pieces are retrieved (rows 1–4, all score 0.000); the answer is `I don't know.` |
| T9 | R3, R5, M3 | offline, S2 set to 1 | `ask "Please suggest a shirt with sunblocking"` | only Ridge Sun Hoodie is retrieved; the system message lacks `Trailblazer Sun Shirt`; the answer is `I don't know.` |
| T10 | R6 | offline | the evaluation set is built | it has 7 examples: E1, E2 (origin hand-written), then the 5 generated pairs for rows 1–5 in row order, with query and answer exactly as in the generator table (origin generated). The generator was called 5 times, each at temperature 0.7. Rows 6–8 were not used. |
| T11 | R7, R8, R9 | offline | `evaluate --offline` | 7 answerer calls; each `result` equals the matching A-row reply (E1→A2, E2→A3, generated→A4–A8). 7 grader calls at temperature 0; all grades are `CORRECT`. The output has blocks `Example 0:` … `Example 6:` with the four labelled lines each, and ends with `7/7 CORRECT`. Exit code 0. |
| T12 | R8 | offline (P1) | E1 is graded with result `Yes, the Meadow Fleece Pullover Set has two side pockets.` and, separately, with result `I don't know.` | the first grade is `CORRECT` although the expected answer `Yes` is not equal to the result; the second is `INCORRECT`. Both grades came from grader calls. |
| T13 | R10 | offline | `ask --offline --trace "Does the Meadow Fleece Pullover Set have side pockets?"` | after A2's reply, the output shows `Pieces:` with 4 lines in T4's order and scores; `Prompt:` with the full system message (containing S4) and the human message; and a `Tokens:` line with `prompt_tokens`, `completion_tokens` and `total_tokens`, where `completion_tokens` is 10 and `total_tokens` equals the sum of the other two. |
| T14 | R11 | offline | `python -m docqa ask --offline "What collection is the Glacier Down Jacket from?"` | standard output is A3's reply; standard error contains `[offline: stand-in model and stand-in embedder]`; exit code 0. |
| T15 | R11 | `OPENAI_API_KEY` unset, no `--offline` | `python -m docqa ask "anything"` | standard error contains `Missing OPENAI_API_KEY`; exit code 2; no network connection attempted. |
| L1 `live` | M1 | a real key | embed `My puppy loves chasing balls in the park.`, `Our kitten naps on the windowsill all afternoon.` and `The pickup truck needs new brake pads.` | the puppy–kitten similarity is higher than the puppy–truck similarity. |
| L2 `live` | M3, R5 | a real key, sample catalog | `ask` E1's query, then grade it with the real grader against `Yes` | grade `CORRECT`. |
| L3 `live` | R5 | a real key, sample catalog | `ask "What is the return policy for worn items?"`, then grade it with the real grader against `I don't know` | grade `CORRECT`. |

Coverage: R1→T1 · R2→T2 · R3→T3, T4, T5, T9 · R4→T6 · R5→T7, T8, T9, L2, L3 · R6→T10 · R7→T11 · R8→T11, T12 · R9→T11 · R10→T13 · R11→T14, T15 · M1→T1, T2, L1 · M2→T3–T6 · M3→T6, T7, T9, L2.

---

## 7. Standing permissions
- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in, in code and in output; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has data; anything that sends data to a third party (a hosted embedder, model or dashboard other than those already chosen).
- **Never:** invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets.

## 8. Test plan
1. Install the dependencies, then run `python -m pytest -m "not live"`. Every T-test must pass.
2. Run `python -m pytest -m live`. With no key these are skipped, which is expected. With a key, all L-tests must pass.
3. Run by hand: `python -m docqa ask --offline "Please suggest a shirt with sunblocking"`, `python -m docqa ask --offline --trace "Does the Meadow Fleece Pullover Set have side pockets?"`, and `python -m docqa evaluate --offline`. Paste their output into the report.
4. **Adjust for the chosen options.** Tests always run on the sample data. Drop the tests for parts that were left out (C9b drops T10–T12 and the evaluate part of the test plan; C10b drops the generated part of T10–T11; C10c drops E1/E2 from T10–T11 but keeps T12 with a generated example). For an option that changes a stage, keep every test that still applies and replace stage-specific expectations with that option's check. For each chosen non-recommended option, write a test from its "what to check" sentence and report it:
   - C1b: each row of your file becomes one document that remembers its file and row, and a question about a fact in one row retrieves that row among the top pieces.
   - C1c: each file becomes one document that remembers its file path, and a question about a fact in one file retrieves that file's text among the top pieces.
   - C1d: each PDF page's text becomes one document that remembers its file and page number, and a question about a fact on one page retrieves that page among the top pieces.
   - C2b: the whole test table passes under the JavaScript test runner, with the same sample data and stand-ins.
   - C3b: with that provider's key set, the live tests pass, and with no key the program names the missing key and exits 2.
   - C3c: with the local model running and no key set, the live tests pass.
   - C4b: a question typed into the page shows the same answer as the command line, and a trace view shows the same pieces, prompt and token counts.
   - C5b: each piece remembers which document it came from, and the pieces of one document together hold the whole document.
   - C6b: the index is built with no network call, and the puppy–kitten sentences score more similar than the puppy–truck sentences.
   - C6c: with that provider's key set, the puppy–kitten sentences score more similar than the puppy–truck sentences.
   - C7b: after a restart with unchanged documents, the program answers without embedding any document again; after a document changes, the index is rebuilt.
   - C7c: the database holds one entry per piece with its vector, text and source, and the same question returns the same top pieces as the in-memory store.
   - C8b: one model call per retrieved piece plus one combining call, and the final answer still says "I don't know" when no piece holds the answer.
   - C8c: the model is called once per retrieved piece in rank order, each call gets the previous answer, and the final answer still says "I don't know" when no piece holds the answer.
   - C8d: one call per retrieved piece, each returning an answer and a score, and the answer with the highest score is the one returned.
   - C9b: the program has no evaluate command, and every remaining test passes.
   - C10b: the evaluation set holds exactly your hand-written examples, and no generator call is made.
   - C10c: the evaluation set holds one generated pair per document for the first S8 documents, and no hand-written example.
   - C11b: after one question, the dashboard shows that run with its retrieved pieces, full prompt and answer, and nothing is sent when the dashboard key is unset.
5. Report one result per test with evidence (test output, file paths). "Should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.
6. Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

---

## 9. Background notes (for the build agent)

### The program
`load → (split) → embed → store → retrieve → answer → evaluate`
- **load:** turn the person's files into documents that remember where they came from, so every answer can be traced to its source.
- **split** (C5b only): break long documents into pieces small enough for the model to read and to match a question sharply. The course skipped it: "Because these documents are already so small, we actually don't need to do any chunking here."
- **embed:** give each piece a numeric representation of its meaning, so pieces can be compared by meaning rather than by wording.
- **store:** keep each vector next to its original text, so a match returns readable text (the slide "Vector Database" shows the embedding vector beside the original chunk).
- **retrieve:** "Language models can only inspect a few thousand words at a time", so only the n most similar pieces go to the model.
- **answer:** the model answers from the question plus those pieces, which "combine[s] these language models with data that they weren't originally trained on".
- **evaluate:** "if you decide to change your implementation … how do you know if you're making it better or worse?" The course builds examples, runs the program on them, and grades with a model.
- The trace (C11) shows what ran without judging it, so it is not a stage.

### Failures and warnings
- **String matching cannot grade answers** (evaluation lesson, shown with an example, not run). What you see: the expected answer "Yes" and the predicted answer "The Cozy Comfort Pullover Set, Stripe does have side pockets." are "nothing alike". "If we were to try to do some string matching, or exact matching, or even some regexes here, it wouldn't know what to do." Why: open-ended answers have "many different variants". Prevention: R8 grades by model only. Planted P1; tested by T12 (and T11).
- **Answering beyond the documents** (warned, in the course's answer prompt: "If you don't know the answer, just say that you don't know, don't try to make up an answer."). Prevention: R5 and S4. Planted P2; tested by T8, T9, L3. The pattern card makes this a rule of the recommended build, not a must-stay-true item.
- **Wrong answers often come from retrieval, not the model** (warned, evaluation lesson: "it's not necessarily the language model itself that's messing up. It's actually the retrieval step"). Prevention: the `--trace` switch (R10, T13) shows the retrieved pieces and the full prompt.
- **Stuffing too much** (stated limit, Q&A lesson and slide "Stuff method": "for large documents or many documents this will not work as it will result in a prompt larger than the context length"). This is a cost, not a warning: it is carried in C8a's "pick this when", and C8b–C8d are offered.
- **Retired model** (Q&A notebook note): the one-line index query defaulted to `text-davinci-003`, "deprecated since 1 January 2024", and the notebook substituted `gpt-3.5-turbo-instruct`. This is why D3 has the build agent choose a current model.
- **Code that looks like a bug, not carried over:** in the Q&A lesson's by-hand demonstration, the retrieved pages are joined with an empty string, so neighbouring pieces run together. The recommended build follows the course's chain with a separator instead (S5), so this demonstration is not reproduced. Also, the evaluation notebook's hand-written query strings contain long runs of spaces left over from line continuations. The sample data here is written fresh, so this does not arise.

### Why the questions and settings are what they are
- **C1** context: the course's example is a product catalog loaded from a CSV; the Q&A lesson names PDFs, web pages and "some company's intranet internal document collection" as typical sources.
- **C2** context: "We have two different packages, a Python one and a JavaScript one." The course used Python.
- **C3** context: the course used OpenAI throughout. Local and other providers are options this spec adds for learners without that key.
- **C4** context: the course had no interface (notebook only), so there is no course choice; the command line is the lightest.
- **C5:** the course explained chunking and skipped it because each row was already small. The pattern card marks splitting as a learner choice. The 1000/150 sizes are additions (the course set none).
- **C6:** the course used OpenAI's embedding class and said the embedding can be swapped ("this will give us flexibility over how the embeddings themselves are created"). The OpenAI embedder uses the same key as the course's model, so per 4.4 it stays the recommended option and the local embedder is offered.
- **C7:** the course chose an in-memory store because "it doesn't require connecting to an external database of any kind", and said "we can also swap out the vector store here for a different type of vector store".
- **C8:** the costs are the instructor's. Stuff: "pretty simple … quite cheap and it works pretty well", "the most common". Map-reduce: "can operate over any number of documents", calls run "in parallel", "does take a lot more calls", "treat[s] all the documents as independent", "the second most common". Refine: "good for combining information and building up an answer over time", "longer answers", "not as fast". Map-rerank: "a bit more experimental", "relies on the language model to know what the score should be", "a bit more expensive".
- **C9/C10:** hand-written examples "[don't] really scale that well"; generated pairs save time ("We didn't have to write it all ourselves"). The course used 2 hand-written plus 5 generated ("I think we had seven examples total").
- **C11:** the course toggled a global debug mode for one question and turned it off for the batch ("just not print everything out onto the screen"). It also showed a hosted evaluation platform that persists runs, shows each step, and lets you add runs to a dataset ("have this flywheel of evaluation start turning").
- **Subjects that are not questions:**
  - Number of pieces, temperatures, separator, number of generated pairs: settings (S2–S8), tuned after the build.
  - One-line index creator versus step-by-step chain: the course says they "equate to the same result". No learner situation changes the outcome.
  - Retrievers not based on meaning (the course: a retriever is "a generic interface … plenty of different methods"): would break M1/M2.
  - Returning matching pieces without an answer (the course's plain similarity search, an earlier step): would break M3.
  - Sending the whole collection to the model: would break M2.
  - Letting the model fill gaps from its general knowledge: would break M3 and R5.
  - String-matching grades: the course shows it failing.
  - Conversation memory and other lessons' parts (prompt templates, output parsers, sequential and router chains, agents and tools): the pattern card lists them as background notes, not offered. They do not change a stage.
  - Markdown display in the notebook: how the course is taught, not the program.
  - The machine it runs on: covered by C3c and C6b; no other choice changes the build.
- **Picked values (4.2):**
  - Answering model: chat model at temperature 0. The instructor introduced ChatOpenAI for answering (rule 1), and the final app agrees. The other value was the completion model used by the one-line `index.query` (D6).
  - Separator `<<<<>>>>>`: the instructor never discussed it, so rule 2, the final end-to-end app (evaluation notebook), decides. The other value was the library default (Q&A notebook).
  - k = 4: the only value the course shows.
  - Generator temperature 0.7: the course left it unset, and the instructor states the default is 0.7.

### Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports: `langchain` (course pinned `0.0.179`), `openai` (pinned `0.27.7`; the course called `openai.ChatCompletion.create`), `ChatOpenAI`, `OpenAI` (completion wrapper), `OpenAIEmbeddings` and `embed_query`, `CSVLoader`, `DocArrayInMemorySearch` (package `docarray`), `VectorstoreIndexCreator` with `from_loaders` and `index.query`, `from_documents`, `similarity_search`, `as_retriever`, `RetrievalQA.from_chain_type` with `chain_type="stuff"` and `chain_type_kwargs={"document_separator": ...}`, `call_as_llm`, `QAGenerateChain` with `apply_and_parse`, `QAEvalChain` with `evaluate`, `langchain.debug`, `python-dotenv` (`load_dotenv`, `find_dotenv`), `tiktoken`. Models: `gpt-3.5-turbo`, `gpt-3.5-turbo-0301`, `text-davinci-003`, `gpt-3.5-turbo-instruct`. Course-era chat models accepted `temperature`. Some current model families reject it or fix it: if the chosen model rejects it, omit the parameter for that role, and say so in `resolved-decisions.md`.

### Course names
| Course name | Spec term |
|---|---|
| `OutdoorClothingCatalog_1000.csv` | `sample_data/catalog.csv` (new facts, 8 rows) |
| `index` / `db` (vector store) | the index |
| `retriever` | retrieve stage |
| `qa` / `qa_stuff` (RetrievalQA, stuff) | answer stage, C8a |
| `examples`, `new_examples` | evaluation set (hand-written, generated) |
| `predictions` with `query`, `answer`, `result` | prediction fields (binding names in 4.2) |
| `graded_outputs` | grades |
| printed labels "Question:", "Real Answer:", "Predicted Answer:", "Predicted Grade:" | R9 output labels (binding) |
| `document_separator` | S5 |
| debug mode | `--trace` (C11a) |
| session "deeplearningai" on the evaluation platform | C11b |

### Lesson map (transcript numbering)
- L1 Introduction: framework overview only.
- L2 Models, Prompts and parsers: temperature 0 habit and default 0.7 (S3, S6); prompt templates and output parsers (another lesson's parts, notes only).
- L3 Memory: conversation memory types (background only, per the pattern card).
- L4 Chains: sequential and router chains (background only); the router's "admit that you don't know" persona is not used.
- L5 Question and Answer: the program's stages, the in-memory store, embeddings, k = 4, stuff and the three other methods (C5–C8, M1–M3, D6). Notebook "L4-QnA".
- L6 Evaluation: the final end-to-end app with the separator (S5), the answer prompt (S4), hand-written and generated examples, model grading, debug mode, the hosted platform (C9–C11, R6–R10). Notebook "L5-Evaluation".
- L7 Agents: tools and agents (background only). The notebook loads a math tool and Wikipedia, while the transcript names DuckDuckGo search and Wikipedia; unused here.
- L8 Conclusion: no facts used.
- Notebook file names count lessons differently (L1–L6). The transcript numbering above decides.
- Slides read: "LLM's on Documents", "Embeddings", two "Vector Database" slides, "Stuff method", two copies of "3 additional methods" (Q&A lesson); "Sequential Chains", "Simple Sequential Chain", "Sequential Chain", "Router Chain" (Chains lesson); "Memory", "Additional Memory Types" (Memory lesson). Each matches the instructor's narration and counted as that lesson's transcript; none disagreed with code or transcripts.
- Nothing in this spec requires access to the course.

---

*Spec v2-draft · course: LangChain for LLM Application Development · project: question answering over your own documents · when the build agent does something unexpected, add the missing constraint here and re-run.*
