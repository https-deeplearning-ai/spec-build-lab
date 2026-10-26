# Spec: Ask Your Documents — a question-answering program over a document collection

**What you're building:** a small program that reads a collection of documents (by default an 8-item outdoor-clothing catalog that the spec supplies), indexes each one by meaning, and answers your plain-language questions from the few most relevant items. When the items do not contain the answer, it says "I don't know." It also includes an evaluation command that grades its own answers.

**Fastest path:** when the build agent asks its first question, answer "recommended build". The build is done when the offline tests pass. They run on scripted stand-ins, so you need no key. An OpenAI key only unlocks the `live` tests and real answers.

This file is self-contained: the build agent needs nothing else.

*Provenance: course "LangChain for LLM Application Development" (8 lessons); materials used: transcripts, course notebooks (rendered from the course repo), 13 lesson slides, owner-confirmed pattern card; written 2026-10-27; guide v2.6 (2026-10-27).*

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

Context questions come first, then the program's stages in order.

### C1. Whose documents should the finished program answer questions about?
- **C1a — The sample catalog this spec defines (8 clothing and camping products).** Pick this when you want a working copy of what the course built, to learn from or extend later. Setup cost: none. **(Recommended - course default)**
- **C1b — Your own folder of documents.** Pick this when you already have a collection you want to question, such as your notes, manuals or product sheets. The sample catalog still ships for the tests. Setup cost: none beyond pointing the program at your folder; you write a few question-and-answer examples of your own for the evaluation command.
  *What to check:* run with `--docs <your folder>`, ask a question whose answer appears in exactly one of your documents, and check that this document's source appears in the trace and the answer uses it.

### C2. What kind of files are your documents?
*Ask only when `C1` is `C1b`.*
- **C2a — A CSV table, one row per document.** Pick this when your collection is a table of records such as products, tickets or contacts. Setup cost: none. **(Recommended - course default)**
- **C2b — Plain text or Markdown files, one file per document.** Pick this when your collection is notes or articles kept as text files. Setup cost: none.
  *What to check:* each file becomes one document that remembers its file path, and a question about a phrase in one file retrieves that file.
- **C2c — PDF files, one document per page.** Pick this when your collection is PDFs such as manuals or reports. Setup cost: one PDF-reading package (small download, no key).
  *What to check:* each PDF page becomes one document that remembers its file name and page number, and a question about a phrase on one page retrieves that page.

### C3. Which programming language should the program use?
- **C3a — Python.** Pick this when you have no strong preference, or your other tools are in Python. Setup cost: Python 3 and pip. **(Recommended - course default)**
- **C3b — JavaScript/TypeScript (the library's JavaScript package).** Pick this when the program will live inside a Node.js project. Setup cost: Node.js and npm.
  *What to check:* every offline test in section 7 is ported to the JavaScript test runner with the same inputs and expected outputs, and they all pass.

### C4. Which language-model provider should write the answers?
- **C4a — OpenAI's hosted chat model.** Pick this when you have, or can get, an OpenAI API key. Setup cost: an OpenAI API key (paid account). The same key also covers the course's embeddings (C7a). **(Recommended - course default)**
- **C4b — Another hosted provider's chat model.** Pick this when you already pay for a different provider or your organisation requires one. Setup cost: that provider's API key and account.
  *What to check:* with that provider's key set, one live question about the sample catalog returns an answer that uses the retrieved items, and the unanswerable question in T8 returns a reply saying it does not know.
- **C4c — A local model served on your machine.** Pick this when your documents must not leave your computer, or you have no paid account. Setup cost: a local model server plus a model download of several GB; answers are slower and usually weaker on a laptop.
  *What to check:* with the network cable unplugged (or network disabled), one question about the sample catalog is answered from the retrieved items and the unanswerable question in T8 gets a "don't know" reply.

### C5. How do you want to ask questions?
- **C5a — From the command line: one question as an argument, or an interactive prompt that answers one line at a time.** Pick this when you are the only user and work in a terminal. Setup cost: none. **(Recommended)**
- **C5b — A small web page on your own machine with a question box and the answer below it.** Pick this when people who don't use a terminal will ask the questions. Setup cost: one small web-server package; no account.
  *What to check:* submitting the question from T6 in the page shows the same answer the command line gives, and the page shows "I don't know." for the question in T8.

### C6. Should long documents be split into smaller pieces before indexing?
- **C6a — No: each document is one piece.** Pick this when every document is short, like a product row or a short note. Setup cost: none. **(Recommended - course default)**
- **C6b — Yes: split each document into overlapping pieces of about 1,000 characters, overlapping by 200 (addition: the course gave no sizes).** Pick this when your documents are long (articles, manuals, long notes). Only a few pieces can go into the model at once, and a whole long document will not fit. Setup cost: none.
  *What to check:* each piece remembers which document it came from, and the pieces of one document together hold the whole document.

### C7. What turns each piece of text into numbers that capture its meaning (the embedding model)?
- **C7a — OpenAI's hosted embedding model.** Pick this when you chose C4a or already have an OpenAI key. Setup cost: the OpenAI API key (same as C4a); each piece is sent to OpenAI. **(Recommended - course default)**
- **C7b — A small embedding model that runs on your machine.** Pick this when you have no OpenAI key, or your documents must not leave your computer. Setup cost: one package plus a model download of roughly 100 MB; no key.
  *What to check:* with no API key set, indexing the sample catalog and asking "Please suggest a shirt with sunblocking" retrieves the Coastline Sun Hoodie and the Sunridge Trail Tee among the top four.
- **C7c — The hosted embedding service of another provider.** Pick this when you chose C4b and want a single provider and bill. Setup cost: that provider's API key.
  *What to check:* with that provider's key set, the same sunblocking question retrieves the Coastline Sun Hoodie and the Sunridge Trail Tee among the top four.

### C8. Where are the indexed pieces kept?
- **C8a — In memory, rebuilt every time the program starts.** Pick this when your collection is small (up to a few hundred short documents), so re-indexing at start-up takes seconds and costs little. Setup cost: none. **(Recommended - course default)**
- **C8b — In a store saved on disk and reused across runs; only new or changed documents are re-indexed.** Pick this when your collection is large, or re-indexing it at every start would cost noticeable time or embedding fees. Setup cost: one embedded vector-store package; no server, no account.
  *What to check:* after a restart, asking a question makes no embedding calls for unchanged documents, and editing one document re-indexes only that document.

### C9. How are the retrieved pieces combined into one answer?
- **C9a — "Stuff": put all retrieved pieces into one prompt and make one model call.** Pick this when the few retrieved pieces fit comfortably in one prompt, which is the usual case. It is the simplest and cheapest method. Setup cost: none. **(Recommended - course default)**
- **C9b — "Map-reduce": ask the question of each piece separately, then make one more call that combines the partial answers.** Pick this when you retrieve many pieces (you raised the retrieved-piece count) and they would not fit in one prompt. It costs one call per piece plus one, and treats pieces as independent of each other. Setup cost: none beyond the extra calls.
  *What to check:* a question asked with 4 retrieved pieces makes 4 per-piece calls plus 1 combining call, and the unanswerable question in T8 still ends in a "don't know" answer.
- **C9c — "Refine": go through the pieces one at a time, improving the answer with each.** Pick this when the answer has to combine facts scattered across several pieces. It is slower than the others because each call waits for the one before, and answers tend to be longer. Setup cost: none beyond the extra calls.
  *What to check:* a question asked with 4 retrieved pieces makes 4 calls in sequence, each call after the first includes the previous answer, and the question in T8 still ends in a "don't know" answer.
- **C9d — "Map-rerank": answer from each piece separately with a score, and keep the highest-scoring answer.** Pick this when the answer usually sits in one single piece and you want the best one picked. The scoring depends on the model and needs careful prompt instructions. Setup cost: none beyond the extra calls.
  *What to check:* a question asked with 4 retrieved pieces makes 4 scored calls, the returned answer is the one with the highest score, and the question in T8 still ends in a "don't know" answer.

### C10. Should the program include an evaluation command that grades its own answers?
- **C10a — Yes, with examples you write plus examples the model generates from your documents; a model grades each answer.** Pick this when you will change the program (another model, store or setting) and want to know whether answers got better or worse. Setup cost: extra model calls for generating and grading. **(Recommended - course default)**
- **C10b — Yes, but only with examples you write by hand; a model grades each answer.** Pick this when you want grading but don't want to pay for generated examples, or your documents are too sensitive to send for example generation. Setup cost: grading calls only.
  *What to check:* the eval command runs only the hand-written examples and makes no example-generation calls.
- **C10c — No evaluation command.** Pick this when you will only ask questions and judge the answers yourself by reading them. Setup cost: none.
  *What to check:* the program has no eval command and makes no grading or generation calls.

### C11. How do you see what each step did?
- **C11a — A step-by-step trace printed in the terminal when you ask for it (`--trace`).** Pick this when you are debugging on your own machine. Setup cost: none. **(Recommended - course default)**
- **C11b — The terminal trace, plus every run sent to a hosted tracing platform where you can browse runs and save them as evaluation examples.** Pick this when a team wants to keep a history of runs and build up an evaluation set over time. Setup cost: an account and API key for that platform. Every question, retrieved piece and answer is sent to it.
  *What to check:* after asking the question from T6, the platform shows that run with its retrieved pieces, the full prompt and the answer.

---

## 2. Departures from the course

| # | Where | Course did | This spec does | Why |
|---|---|---|---|---|
| D1 | How it is used | Ran the steps as notebook cells | A command-line program (`ask`, interactive prompt, `eval`) | A build is a program, not a notebook (addition). |
| D2 | Sample data | A 1,000-row outdoor-clothing catalog CSV | An 8-row catalog with invented facts (section 7) | No course data is copied; 8 rows let every test outcome be worked out by hand. |
| D3 | Trace default | Left verbose output on in the chain; turned the full debug trace on for one question, then off before batch runs | Trace off by default; `--trace` turns it on for a run | A command-line answer should print only the answer; the course itself turned the trace off for batch runs. |
| D4 | Example-generation format | Used the library's built-in example-generation prompt; its reply format is not shown | The generator is asked to reply `QUESTION: …` / `ANSWER: …`, which the program parses | Makes parsing testable (addition). |
| D5 | Grade format | Printed the grader's text (shown grading "correct") | Grades are exactly `CORRECT` or `INCORRECT` | Makes the summary countable (addition). |
| D6 | Evaluation report | Printed to the notebook | Printed and also written to `eval_report.json` | Gives the build agent file evidence (addition). |
| D7 | Library versions | Notebook note says it used `langchain==0.0.179` and `openai==0.27.7`; install lines were unpinned (`pip install --upgrade langchain`) | Current releases, unpinned | The course pinned nothing in its install lines (guide rule: never invent a pin). |
| D8 | Running without a key | Always called OpenAI | With no key, runs on labelled scripted stand-ins (model and embedder) | Offline tests and a first run need no account (addition). |
| D9 | Ties in retrieval | Not addressed | Equal similarity → lower row/file order first | Makes results reproducible (addition). |

---

## 3. Objective

Answer a person's plain-language questions about their own document collection by indexing every document by meaning, retrieving the few pieces most similar in meaning to each question, and having a language model write the answer from the question plus those pieces, saying it does not know when the pieces lack the answer.

---

## 4. Tech stack, versions and secrets

- **Language:** Python 3 (current release) — C3a. Package name `docqa` (run as `python -m docqa`).
- **Library:** LangChain (current release; the course left it unpinned). Use it for the chat model, embeddings, vector store and question-answering chain where it offers them. The scripted stand-ins plug in through the same interfaces. The course is about this library, so it is kept.
- **Chat model:** OpenAI chat model through the library's OpenAI integration (C4a).
- **Embeddings:** OpenAI embeddings through the same integration (C7a).
- **Vector store:** the library's in-memory vector store (C8a).
- **Tests:** pytest. `live` is a registered marker.
- **Secrets:** `OPENAI_API_KEY` is read from the environment. A `.env` file in the working directory is also read if present (the course loaded its key from a local `.env` file). The key is never printed, logged or written to any file. `.env` is listed in `.gitignore`.

---

## 5. Contracts

### 5.1 Commands

| Command | Behaviour |
|---|---|
| `python -m docqa ask "<question>" [--trace] [--docs <path>]` | Indexes the documents, answers one question, prints the answer alone on stdout, exits 0. |
| `python -m docqa [--trace] [--docs <path>]` | Interactive: indexes once, then reads one question per line from stdin and prints each answer. An empty line or `exit` ends the session. |
| `python -m docqa eval [--docs <path>]` | Runs the evaluation (section 6, R9–R11), prints one block per example and a summary line, and writes `eval_report.json`. |

`--docs` defaults to `sample_data/catalog.csv`. The stand-in notice (R12) and the trace (R8) go to stderr; answers go to stdout.

### 5.2 Document (after loading)

```json
{
  "type": "object",
  "required": ["text", "source"],
  "properties": {
    "text":   {"type": "string", "minLength": 1},
    "source": {"type": "object", "required": ["file", "row"],
               "properties": {"file": {"type": "string"}, "row": {"type": "integer", "minimum": 0}}}
  }
}
```
For a CSV, `text` is one line per column in column order, `<column>: <value>`, joined by `\n` (addition: the course's loader made one document per row; its exact text layout is not shown).

### 5.3 Store entry (one per piece)

```json
{
  "type": "object",
  "required": ["text", "vector", "source"],
  "properties": {
    "text":   {"type": "string", "minLength": 1},
    "vector": {"type": "array", "items": {"type": "number"}, "minItems": 1},
    "source": {"$ref": "#/document/source"}
  }
}
```

### 5.4 Evaluation example and report

Example (hand-written file `sample_data/eval_examples.json` is an array of these; key names follow the course):
```json
{"type": "object", "required": ["query", "answer"],
 "properties": {"query": {"type": "string", "minLength": 1}, "answer": {"type": "string", "minLength": 1}}}
```
Report `eval_report.json`:
```json
{
  "type": "object",
  "required": ["total", "correct", "skipped_generated", "examples"],
  "properties": {
    "total":   {"type": "integer", "minimum": 0},
    "correct": {"type": "integer", "minimum": 0},
    "skipped_generated": {"type": "integer", "minimum": 0},
    "examples": {"type": "array", "items": {
      "type": "object",
      "required": ["origin", "query", "answer", "result", "grade", "retrieved_rows"],
      "properties": {
        "origin": {"enum": ["hand", "generated"]},
        "query":  {"type": "string"},
        "answer": {"type": "string", "description": "reference answer"},
        "result": {"type": "string", "description": "the program's answer"},
        "grade":  {"enum": ["CORRECT", "INCORRECT"]},
        "retrieved_rows": {"type": "array", "items": {"type": "integer"}}
      }}}
  }
}
```
Printed block per example: `Example <i>:` / `Question: <query>` / `Real Answer: <answer>` / `Predicted Answer: <result>` / `Predicted Grade: <grade>`, then a blank line. Last line: `Correct: <correct>/<total>`.

### 5.5 Settings file `docqa_settings.json`

```json
{
  "type": "object",
  "properties": {
    "k":                       {"type": "integer", "minimum": 1, "default": 4},
    "document_separator":      {"type": "string", "default": "<<<<>>>>>"},
    "answer_temperature":      {"type": "number", "minimum": 0, "default": 0.0},
    "grader_temperature":      {"type": "number", "minimum": 0, "default": 0.0},
    "generated_example_docs":  {"type": "integer", "minimum": 0, "default": 5},
    "examples_path":           {"type": "string", "default": "sample_data/eval_examples.json"}
  },
  "additionalProperties": false
}
```
A missing file means all defaults.

### 5.6 Model roles

| Role | Does | Course model | Course settings |
|---|---|---|---|
| answerer | Writes the answer from the question plus retrieved pieces | `gpt-3.5-turbo` (`gpt-3.5-turbo-0301` before 2024-06-12) | temperature 0.0 |
| example generator | Writes one question-and-answer pair per document (C10a) | same | temperature not set (provider default) |
| grader | Judges whether the program's answer means the same as the reference answer (C10a/b) | same | temperature 0.0 |
| embedder | Turns text into a meaning vector | the library's default OpenAI embedding model (name not shown; vectors had "over a thousand" numbers) | — |

### 5.7 Settings

| Setting | Value | Source | Change this when … |
|---|---|---|---|
| `k` (pieces retrieved per question) | 4 | L5: the similarity search "returns four documents"; the course never set it (library default) | answers need facts spread over more pieces (raise), or pieces are long and the prompt gets too big (lower). |
| `document_separator` | `<<<<>>>>>` | L6 final question-answering chain (notebook cell 8); L5 used the library's default | your documents themselves contain this string. |
| `answer_temperature` | 0.0 | L5 and L6 notebooks; L2 instructor: set temperature to zero "to make this output a little bit less random" | you want more varied wording (the course never raised it for this program). |
| `grader_temperature` | 0.0 | L6 notebook (grading chain) | — |
| `generated_example_docs` | 5 (the first five documents) | L6 notebook (examples generated from the first five documents) | you want a larger evaluation set. |
| hand-written examples | 2 | L6 (two hand-written examples; seven examples in total) | you have more questions with known answers. |
| trace | off unless `--trace` | D3 | — |

---

## 6. Business rules

**What must stay true (the course's pattern card — every option keeps all three):**
1. **The documents are indexed by meaning before any question.** Each piece of text gets a numeric representation of its meaning, stored next to its original text, so pieces with similar meaning can be found later.
2. **For each question, only the few stored pieces most similar in meaning are retrieved, not the whole collection.**
3. **A language model writes the answer from the question plus the retrieved pieces, so the answer rests on the person's documents.**

**Rules of the recommended build:**

- **R1 — Load.** Each CSV row becomes one document (5.2) whose source is the file name and the 0-based row number. No splitting (C6a): each document is one piece. → T1
- **R2 — Index by meaning (card 1).** On every start the store is empty. Each piece is embedded once, and the store keeps its text, vector and source together. Indexing finishes before the first question is answered. → T2, L1
- **R3 — Retrieve (card 2).** A question is embedded with the same embedder as the pieces. It is compared with every stored vector by cosine similarity, and the `k` most similar pieces are returned, most similar first, with ties broken by lower row (D9). → T3, T5, L1
- **R4 — Answer (card 3; C9a).** The program makes exactly one answerer call per question with two messages. The system message holds the instruction text in R5, then a line `----------------`, then the retrieved pieces' texts in rank order joined by `document_separator`. The human message is the question exactly as asked. The program prints the answerer's reply unchanged. → T4, T6, T7, L1
- **R5 — Say "I don't know" (rule from the course's answer prompt).** The system message begins with exactly: `Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer.` The program never adds facts of its own and never answers without calling the answerer with the retrieved pieces. → T8, L2
- **R6 — Each question stands alone.** No earlier question or answer goes into a later prompt. Conversation memory is not part of this program. In an interactive session the documents are indexed once. → T9
- **R7 — Temperatures.** Answerer calls use `answer_temperature`, grader calls use `grader_temperature`, and generator calls set no temperature. → T10
- **R8 — Trace (C11a).** With `--trace`, the program writes to stderr, before the answer, the question; each retrieved piece as `#<rank> row <row> score <cosine to 4 decimals>` followed by its text; and the full system and human messages. Without `--trace`, it writes no trace. In both cases stdout holds only the answer. → T11, T12
- **R9 — Evaluation examples (C10a).** The examples are the hand-written ones from `examples_path` in file order, followed by one generated example for each of the first `generated_example_docs` documents in row order. The generator receives one document's text and is asked to reply in the form `QUESTION: <q>` newline `ANSWER: <a>`. A reply that does not parse into both parts is skipped, counted in `skipped_generated`, and reported on stderr as `skipped <n> generated example(s)`. → T13, T18, L3
- **R10 — Grade by meaning, never by matching strings.** Each example's answer from the program (`result`) is produced by the same path as `ask` (R3–R5). The grader model receives the query, the reference answer and the result, and its reply is read as `INCORRECT` if it contains the word INCORRECT, else `CORRECT` if it contains the word CORRECT, else `INCORRECT`. The program never compares strings itself to grade. → T14, T15, L3
- **R11 — Show the retrieval behind each graded answer.** Each report entry records the rows retrieved for its query, so a wrong answer can be traced to a retrieval miss or a model mistake. → T15, T17
- **R12 — Real provider or labelled stand-ins.** If `OPENAI_API_KEY` is set, the program uses the real answerer, generator, grader and embedder. If it is not set, the program uses the scripted stand-ins in 7.2. It writes this notice as the first stderr line: `Running on scripted stand-ins (no OPENAI_API_KEY): answers are canned test replies.` → T16
- **R13 — Evaluation report.** `eval` writes `eval_report.json` matching 5.4 and prints the per-example blocks and the summary line. → T17, L3

---

## 7. Tests

### 7.1 Sample data

**`sample_data/catalog.csv`** — columns `name,description`, 8 rows (row numbers are 0-based). All facts were written for this spec and are not course data.

| row | name | description |
|---|---|---|
| 0 | Sunridge Trail Tee | Lightweight long-sleeve hiking shirt rated UPF 50+ that blocks 98% of the sun's UV rays. Made of 100% nylon. Two chest pockets. Machine wash cold. |
| 1 | Coastline Sun Hoodie | Breathable hoodie made of UPF 40 fabric with a built-in face cover. 90% polyester, 10% spandex. |
| 2 | Harbor Rain Shell | Waterproof rain jacket with sealed seams and an adjustable hood. Packs into its own chest pocket. Weighs 310 grams. |
| 3 | Glacier Peak Down Parka | Warm insulated parka filled with 700-fill down, from the Summit Loft collection. Two zippered hand pockets. |
| 4 | Meadow Fleece Pullover | Soft fleece pullover with a kangaroo pocket. A warm layer for cool evenings. Made in Portugal. |
| 5 | Ridgeline Hiking Boots | Leather hiking boots with a waterproof membrane and lugged rubber soles. Weight 1.1 kg per pair. |
| 6 | Tidewater Swim Trunks | Quick-dry swim trunks with a mesh lining and a back pocket. UPF 50 fabric for sun protection at the beach. |
| 7 | Camp Mug Set | Set of two enamel camp mugs, 350 ml each. Dishwasher safe. |

Descriptions containing commas are quoted in the CSV file. Row 0's document text is therefore exactly:
`name: Sunridge Trail Tee` + `\n` + `description: Lightweight long-sleeve hiking shirt rated UPF 50+ that blocks 98% of the sun's UV rays. Made of 100% nylon. Two chest pockets. Machine wash cold.`

**`sample_data/eval_examples.json`** — two hand-written examples:
1. query `Does the Meadow Fleece Pullover have a pocket?`, answer `Yes`
2. query `What collection is the Glacier Peak Down Parka from?`, answer `The Summit Loft collection`

**Planted failures:**
- *Hand example 1* is the course's grading trap. The reference is `Yes`, while the program's answer is a full sentence. Exact string matching would call it wrong, but grading by meaning calls it right (R10).
- *The generated example for row 0* is a retrieval miss. The scripted embedder finds no meaning words in it, so row 0 is not retrieved, the answerer says "I don't know.", and the grade is INCORRECT. The report shows the retrieved rows `[7, 1, 2, 4]`, so the miss is visibly a retrieval problem, not a model problem (R11).

### 7.2 Scripted stand-ins (labelled stand-ins; used by offline tests and when no key is set)

**Stand-in embedder** (stands in for the hosted embedding model). Lower-case the text and split it on every character that is not `a`–`z` or `0`–`9`, dropping empty tokens. The vector has 9 numbers: for each concept group below, the count of tokens in that group, followed by a constant `1`.

| dim | group | tokens |
|---|---|---|
| 0 | sun | sun, sunblocking, upf, uv |
| 1 | rain | rain, waterproof, wet |
| 2 | warm | warm, insulated, down, fleece, parka |
| 3 | pocket | pocket, pockets |
| 4 | footwear | boots, boot, shoes, soles |
| 5 | swim | swim, beach, trunks |
| 6 | kitchen | mug, mugs, cup, coffee |
| 7 | shirt | shirt, shirts, hoodie, top |
| 8 | constant | (always 1) |

Resulting vectors for rows 0–7: `[3,0,0,1,0,0,0,1,1]`, `[2,0,0,0,0,0,0,2,1]`, `[0,3,0,1,0,0,0,0,1]`, `[0,0,6,1,0,0,0,0,1]`, `[0,0,3,1,0,0,0,0,1]`, `[0,1,0,0,3,0,0,0,1]`, `[2,0,0,1,0,5,0,0,1]`, `[0,0,0,0,0,0,2,0,1]`.

**Stand-in answerer** (stands in for the chat model). It looks up the human message (trimmed) in this table. It returns the reply only if the system message contains the required text; in every other case it returns exactly `I don't know.` It records each call's messages and temperature.

| question | required text in system message | reply |
|---|---|---|
| Please suggest a shirt with sunblocking | UPF 50+ | The Sunridge Trail Tee blocks 98% of UV rays (UPF 50+); the Coastline Sun Hoodie (UPF 40) is another option. |
| Does the Meadow Fleece Pullover have a pocket? | kangaroo pocket | Yes, the Meadow Fleece Pullover has a kangaroo pocket. |
| What collection is the Glacier Peak Down Parka from? | Summit Loft | It is from the Summit Loft collection. |
| What is the Sunridge Trail Tee made of? | 100% nylon | The Sunridge Trail Tee is made of 100% nylon. |
| What UPF rating does the Coastline Sun Hoodie fabric have? | UPF 40 | Its fabric is rated UPF 40. |
| How much does the Harbor Rain Shell weigh? | 310 grams | The Harbor Rain Shell weighs 310 grams. |
| How many hand pockets does the Glacier Peak Down Parka have? | Two zippered hand pockets | It has two zippered hand pockets. |
| Where is the Meadow Fleece Pullover made? | Made in Portugal | It is made in Portugal. |

**Stand-in generator** (stands in for the example-generation model). It replies according to which product name appears in the document text it receives. A document with none of these names gets the reply `Sorry.`, which does not parse.

| product name in document | reply |
|---|---|
| Sunridge Trail Tee | `QUESTION: What is the Sunridge Trail Tee made of?` / `ANSWER: 100% nylon` |
| Coastline Sun Hoodie | `QUESTION: What UPF rating does the Coastline Sun Hoodie fabric have?` / `ANSWER: UPF 40` |
| Harbor Rain Shell | `QUESTION: How much does the Harbor Rain Shell weigh?` / `ANSWER: 310 grams` |
| Glacier Peak Down Parka | `QUESTION: How many hand pockets does the Glacier Peak Down Parka have?` / `ANSWER: Two` |
| Meadow Fleece Pullover | `QUESTION: Where is the Meadow Fleece Pullover made?` / `ANSWER: Portugal` |

(The `/` marks the newline between the two lines.)

**Stand-in grader** (stands in for the grading model). It looks up the query in this table and replies `CORRECT` if the result contains the key phrase (case-insensitive), otherwise `INCORRECT`. It records each call's temperature.

| query | key phrase |
|---|---|
| Does the Meadow Fleece Pullover have a pocket? | pocket |
| What collection is the Glacier Peak Down Parka from? | summit loft |
| What is the Sunridge Trail Tee made of? | nylon |
| What UPF rating does the Coastline Sun Hoodie fabric have? | upf 40 |
| How much does the Harbor Rain Shell weigh? | 310 grams |
| How many hand pockets does the Glacier Peak Down Parka have? | two |
| Where is the Meadow Fleece Pullover made? | portugal |

### 7.3 Test table

All offline tests run with no `OPENAI_API_KEY` set (the test setup removes it), all settings at their defaults unless a test says otherwise, and the stand-ins above. Similarities are cosine values rounded to 4 decimals.

| id | Given | When | Then | Rules |
|---|---|---|---|---|
| T1 | `catalog.csv` | loaded | 8 documents; document 0's text is exactly the row-0 text in 7.1; its source is `{file: "catalog.csv", row: 0}`; document 7's source row is 7 | R1 |
| T2 | a fresh start | the store is inspected before indexing, then again after indexing | before: 0 entries. After: 8 entries, each with non-empty text, a 9-number vector and a source; row 3's vector is `[0,0,6,1,0,0,0,0,1]`; the embedder was called for exactly 8 pieces | R2 |
| T3 | indexed sample | retrieve for `Please suggest a shirt with sunblocking` | rows `[1, 0, 6, 7]` with scores `0.9623, 0.8333, 0.3111, 0.2582`; exactly 4 of the 8 entries returned | R3 |
| T4 | indexed sample | `ask "Please suggest a shirt with sunblocking"` | the one answerer call's system message contains the texts of rows 1, 0, 6, 7 and none of the names `Harbor Rain Shell`, `Glacier Peak Down Parka`, `Meadow Fleece Pullover`, `Ridgeline Hiking Boots`; stdout is exactly the stand-in answerer's reply for this question (7.2) | R4 |
| T5 | `docqa_settings.json` with `k: 2` | retrieve for `Please suggest a shirt with sunblocking` | rows `[1, 0]` only | R3 |
| T6 | indexed sample | `ask "Does the Meadow Fleece Pullover have a pocket?"` | stdout is exactly `Yes, the Meadow Fleece Pullover has a kangaroo pocket.`; exactly 1 answerer call; retrieved rows `[4, 3, 2, 0]` | R4 |
| T7 | indexed sample | `ask "Please suggest a shirt with sunblocking"` | the system message contains `<<<<>>>>>` exactly 3 times; row 1's text appears before row 0's, row 0's before row 6's, and row 6's before row 7's; the human message is exactly the question | R4 |
| T8 | indexed sample | `ask "What is the return policy for the boots?"` | retrieved rows `[5, 7, 1, 2]` (rows 2 and 4 tie at 0.2132; row 2 wins by lower row); the system message begins with the R5 instruction text verbatim; stdout is exactly `I don't know.` | R5 |
| T9 | interactive session | stdin lines: the T6 question, then the T8 question, then an empty line | two answers, as in T6 and T8; the second answerer call has exactly 2 messages, its human message is exactly the T8 question, and neither message contains `kangaroo`; the embedder embedded the 8 pieces once (8 piece calls plus 2 question calls in total) | R6 |
| T10 | `eval` on the sample | stand-in calls are inspected | every answerer call has temperature 0.0; every grader call has temperature 0.0; no generator call sets a temperature | R7 |
| T11 | indexed sample | `ask --trace "Please suggest a shirt with sunblocking"` | stderr contains the question; the lines `#1 row 1 score 0.9623`, `#2 row 0 score 0.8333`, `#3 row 6 score 0.3111`, `#4 row 7 score 0.2582`; and the full system and human messages. stdout is only the answer | R8 |
| T12 | indexed sample | `ask "Please suggest a shirt with sunblocking"` (no flag) | stderr is exactly the one R12 notice line; no `#1 row` line appears anywhere | R8 |
| T13 | sample + `eval_examples.json` | `eval` | 7 examples in this order: the 2 hand-written, then generated for rows 0, 1, 2, 3, 4 with the queries and answers from the generator table; the generator was called 5 times; `skipped_generated` is 0 | R9 |
| T14 | sample | `eval` | example 1: answer `Yes`, result `Yes, the Meadow Fleece Pullover has a kangaroo pocket.`, grade `CORRECT`, even though the two strings differ | R10 |
| T15 | sample | `eval` | `total` 7, `correct` 6. The generated example for row 0 has result `I don't know.`, grade `INCORRECT` and retrieved_rows `[7, 1, 2, 4]`. Every other example is `CORRECT`. The last printed line is `Correct: 6/7` | R10, R11 |
| T16 | no `OPENAI_API_KEY` | `ask "Does the Meadow Fleece Pullover have a pocket?"` | the first stderr line is exactly the R12 notice; stdout is the stand-in reply from T6; no network connection is opened | R12 |
| T17 | sample | `eval` | `eval_report.json` exists and validates against 5.4; each entry has `retrieved_rows` of length 4; `origin` is `hand` for entries 1–2 and `generated` for entries 3–7 | R11, R13 |
| T18 | `docqa_settings.json` with `generated_example_docs: 6` | `eval` | the generator is called 6 times; row 5's reply `Sorry.` is skipped; `skipped_generated` is 1; stderr contains `skipped 1 generated example(s)`; `total` 7 | R9 |
| L1 `live` | `OPENAI_API_KEY` set, real models | `ask "Does the Meadow Fleece Pullover have a pocket?"` | no stand-in notice; the answer mentions a pocket; the retrieved rows include row 4 | R2, R3, R4 |
| L2 `live` | key set | `ask "What is the return policy for the boots?"` | the real grader, given reference `I don't know` and this answer, grades it `CORRECT` (the answer says it does not know and states no return policy) | R5 |
| L3 `live` | key set | `eval` | the report has `total` + `skipped_generated` = 7, and every grade is `CORRECT` or `INCORRECT` | R9, R10, R13 |

Card coverage: item 1 → T2; item 2 → T3, T4; item 3 → T6 (plus T8: with no supporting text, there is no answer).

---

## 8. Standing permissions

- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in in its name and in the R12 notice; read secrets from the environment.
- **Ask first:** changing an answered question or a setting once the build has data; anything that sends data to a third party not already chosen at the gate.
- **Never:** invent provenance (claim the course did something it did not); return an answer when the program should say it does not know; change sample data or scripted replies to make a test pass; commit secrets.

---

## 9. Test plan

1. Install: `python -m pip install -U langchain langchain-openai pytest python-dotenv` (current releases; the integration package names may have changed, so check current docs) plus whatever the chosen options need.
2. Offline: `python -m pytest -q -m "not live"`. All of T1–T18 must pass.
3. Live (only when a key is present): `python -m pytest -q -m live`. These are skipped automatically when `OPENAI_API_KEY` is unset.
4. Manual smoke check: `python -m docqa ask --trace "Please suggest a shirt with sunblocking"`.
5. For each chosen non-recommended option, turn its "what to check" sentence (from `resolved-decisions.md`) into a test, run it, and report it.
6. Report one result per test with evidence (test output lines, file paths such as `eval_report.json`). "Should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes. When options change behaviour, adjust the matching tests: for example, C9b–d change the call count in T6, C6b changes piece counts in T2, and C10b removes generated examples from T13–T15.
7. Finish with a diagram of the built app, introduced by the sentence "This is the infra/structure diagram of this app".

---

## 10. Background notes (for the build agent)

### The program
A program that answers a person's plain-language questions about their own collection of documents, using the few pieces of the collection most similar in meaning to the question. Stages:
`load → (split) → embed → store → retrieve → answer → evaluate`
- **load:** turns the person's files into documents that remember where they came from.
- **split:** language models "can only inspect a few thousand words at a time", so long documents are broken into pieces. The course skipped this because its catalog rows were already small.
- **embed:** gives each piece a numeric representation of its meaning, so similar pieces can be found.
- **store:** keeps each vector next to its original text.
- **retrieve:** embeds the question and picks the n most similar pieces, so only what fits and matters reaches the model.
- **answer:** the model writes the answer from the question plus those pieces. This "combine[s] these language models with data that they weren't originally trained on".
- **evaluate:** checks whether changes (another model, store or retrieval strategy) make answers better or worse. The course built this onto the same question-answering program in the evaluation lesson.

Tracing (the debug printout, the hosted platform) only shows what ran, so it is not a stage; it is question C11.

### Failures
- **Exact-match grading cannot judge free-text answers (warned, L6).** *What you see:* reference `Yes` against a full-sentence answer; string matching, exact matching or regexes would mark it wrong. *Why:* answers are open-ended text, and "as long as they have the same semantic meaning, they should be graded as being similar". *Prevention:* R10 grades with a model. *Enforced by:* T14, T15, and the planted hand example 1.
- **A wrong answer often comes from retrieval, not the model (warned, L6).** *What you see:* the model answers wrongly or says it doesn't know although the document exists. *Why:* the right piece was not among those retrieved. *Prevention:* R8 trace and R11 retrieved rows in the report. *Enforced by:* T11, T15, and the planted row-0 generated example.
- **Stuffing too much into one prompt (stated limit, L5 slide "Stuff method").** "For large documents or many documents this will not work as it will result in a prompt larger than the context length." This is a cost, not a demonstrated failure, so it is carried in C9's "pick this when …" text and in the `k` setting.
- **A deprecated default model broke the one-line helper (course notebook note, L5).** The one-line index helper's default base model had been deprecated, so the course swapped in a replacement model for that call. This spec avoids depending on any library default model; the gate names the models.

### Why the questions and settings are what they are
- **C1/C2:** the course's example is one instance (a product catalog). L5 names the general case: text "extracted from a PDF file or from a webpage or from some company's intranet internal document collection".
- **C3:** L1 says the library has "a Python one and a JavaScript one". The course used Python.
- **C4/C7:** the course used OpenAI for both. Local and other-provider options are paths for learners without an OpenAI account or with privacy needs.
- **C5:** the course ran notebooks; a command line is the lightest program interface.
- **C6:** L5 explains chunking and then skips it: "Because these documents are already so small, we actually don't need to do any chunking here."
- **C8:** L5 chose the in-memory store because "it doesn't require connecting to an external database of any kind", and said "we can also swap out the vector store here for a different type of vector store."
- **C9:** L5 transcript and slides. Stuff is "pretty simple … quite cheap and it works pretty well", and the instructor called it the most common, with map_reduce second. Map_reduce "can operate over any number of documents", runs in parallel, "takes a lot more calls", and "does treat all the documents as independent". Refine is "really good for combining information", gives "longer answers" and is "not as fast". Map_rerank is "a bit more experimental", "relies on the language model to know what the score should be", and is "a bit more expensive".
- **C10:** L6 builds hand-written examples ("doesn't really scale that well"), model-generated examples, and model grading.
- **C11:** L6 debug mode, plus the hosted evaluation platform shown at the end of L6, which persists runs and lets you add them to datasets.

**Subjects that are not questions:**
- **Keyword or other non-meaning retrieval:** would break card item 2 (similar in meaning). The course mentions "plenty of different methods" without naming one.
- **Sending the whole collection to the model without retrieval:** breaks card item 2.
- **Dropping the "don't know" instruction:** answers would no longer rest only on the documents (card item 3); it is a rule of the recommended build.
- **Conversation memory (L3):** the owner's card lists it as a background note, not an option.
- **Agents and tools (L7), sequential and router chains (L4), prompt templates and output parsers (L2):** other lessons' parts that do not change this program's stages.
- **One-line index helper versus step-by-step building (L5):** "these two things equate to the same result", so it is not a choice.
- **Exact-match grading:** never offered (the failure above).
- **Which model the tests use:** not asked; tests always run offline on stand-ins.
- **Temperature, `k`, separator and example counts:** settings (5.7).

**Where picked values came from:**
- *Separator:* L5 used the library default and L6's final chain set `<<<<>>>>>`. The instructor never stated one, so the final end-to-end app decides (L6).
- *Model:* the notebooks pick `gpt-3.5-turbo` after 2024-06-12 and `gpt-3.5-turbo-0301` before; the transcript says "GPT 3.5 Turbo". The final app uses the date switch, so it is recorded as `gpt-3.5-turbo`. The one-line helper's query in L5 used `gpt-3.5-turbo-instruct` at temperature 0 as a replacement for the deprecated `text-davinci-003`; it is not used here.
- *Verbose:* the L5/L6 chains had verbose output on, while L6 turned full debug on for one question and off before batch predictions. See D3.
- *k = 4:* the library's default, as observed in L5.

### Names that go stale (search keywords, not guaranteed imports)
`ChatOpenAI`, `OpenAI` (completion-model wrapper), `OpenAIEmbeddings`, `embed_query`, `CSVLoader`, `DocArrayInMemorySearch` (needed the `docarray` package), `VectorstoreIndexCreator`, `from_loaders`, `from_documents`, `similarity_search`, `as_retriever`, `RetrievalQA.from_chain_type`, `chain_type="stuff" | "map_reduce" | "refine" | "map_rerank"`, `chain_type_kwargs={"document_separator": …}`, `call_as_llm`, `QAGenerateChain`, `apply_and_parse`, `QAEvalChain`, `langchain.debug`, `openai.ChatCompletion.create`, `load_dotenv`/`find_dotenv`. Course-era versions: `langchain==0.0.179`, `openai==0.27.7`. Course-era models: `gpt-3.5-turbo`, `gpt-3.5-turbo-0301`, `gpt-3.5-turbo-instruct`, `text-davinci-003` (deprecated since 1 January 2024 per the course note).

Request-parameter limits: the course's models all accepted `temperature`. If the current model you pick rejects a temperature parameter, omit it, note that in `resolved-decisions.md`, and skip the temperature assertions in T10 for that role with a stated reason.

### Course names → spec terms
| Course | Spec |
|---|---|
| index / vector store / vector database | store (5.3) |
| retriever | retrieve stage (R3) |
| chain type "stuff" | C9a / R4 |
| QA generation chain | example generator role |
| QA eval chain | grader role |
| example keys `query`, `answer`; prediction key `result` | same keys in 5.4 (binding) |
| `document_separator` | `document_separator` setting (binding) |
| `OutdoorClothingCatalog_1000.csv` | `sample_data/catalog.csv` (new facts) |

### Lesson map (transcript numbering)
| Lesson | Title | Used for |
|---|---|---|
| L1 | Introduction | C3 (Python and JavaScript packages) |
| L2 | Models, Prompts and parsers | temperature-0 reasoning; background only |
| L3 | Memory | background only (conversation memory not offered); slides memory_1, memory_2 read, counted like transcript |
| L4 | Chains | background only; slides chains_1–4 read, counted like transcript |
| L5 | Question and Answer | stages load→answer, store, `k`, C6, C8, C9, stuff-limit note; slides question_and_answer_1–7 read, counted like transcript (6 and 7 show the same slide) |
| L6 | Evaluation | evaluate stage, separator, grading failure, retrieval-miss failure, C10, C11 |
| L7 | Agents | background only |
| L8 | Conclusion | background only |

Notebook files count differently (the Q&A notebook is labelled lesson 4, the evaluation notebook lesson 5); the transcript numbering above decides. Nothing in this spec requires access to the course.

---

*Spec v2-draft · course: LangChain for LLM Application Development · project: Ask Your Documents (`docqa`) · when the build agent does something unexpected, add the missing constraint here and re-run.*
