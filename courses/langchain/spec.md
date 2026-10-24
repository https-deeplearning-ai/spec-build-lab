# Spec: Ask Your Documents — answers drawn from the few most similar pieces

**What you're building:** a notebook on your own machine where you type a plain-language question about a small outdoor-gear catalog and get an answer written only from the four catalog entries closest in meaning to your question, or "I don't know" when those entries do not hold the answer.

**Fastest path:** when the build agent asks its first question, answer "recommended build". The build is finished when the offline tests pass; they need no key, no account and no network. An OpenAI API key only unlocks the `live` tests and real (non-scripted) answers.

This file is self-contained: everything the build needs is here. Nothing in it requires access to the course.

*Provenance: course "LangChain for LLM Application Development" (DeepLearning.AI); materials used: lesson transcripts (8 lessons), the course notebooks rendered from the course repo (6 notebooks), 13 slide images; owner-confirmed pattern card of 2026-10-23 (reconfirmed 2026-10-24); generated 2026-10-24 with guide v2.4 (2026-10-23).*

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

### C1. What kind of documents will you ask about?
- **C1a — Rows of a table (a CSV file); each row is one piece, no splitting. (Recommended - course default)**
  Pick this when each record is short, like product entries, contacts or FAQ rows, so one row fits easily in a prompt next to a few others.
  Setup cost: none.
- **C1b — Longer documents (plain-text, Markdown or PDF files), split into overlapping pieces before indexing.**
  Pick this when your documents run longer than a few paragraphs, e.g. your own lecture notes or reports, so a whole document would crowd the prompt and you want only the relevant part of it sent.
  Setup cost: no key; a PDF text-extraction package if you use PDFs. Pieces are about 1,000 characters with about 100 characters of overlap (this spec's addition: the course gives no piece size).
  What to check: each piece remembers which file it came from, and the pieces of one file, with overlaps removed, together hold the whole file's text.

### C2. Which models turn text into meaning-numbers and write the answers?
- **C2a — OpenAI's hosted chat model and embedding model. (Recommended - course default)**
  Pick this when you have, or can get, an OpenAI API key and your documents may be sent to OpenAI.
  Setup cost: an OpenAI API key; paid per token. Without a key the build still runs, on labelled scripted stand-ins (see R9).
- **C2b — Models running on your own machine (a local chat model and a local embedding model).**
  Pick this when you have no paid key, or your documents must not leave your machine.
  Setup cost: no key; a download of several gigabytes and a local model server kept running; answers are slower and may be weaker.
  What to check: with no access to any hosted provider, the program indexes the sample collection and answers a sample question with the local models, and questions are embedded with the same local embedding model as the pieces.
- **C2c — Another hosted provider you already have a key for.**
  Pick this when you already pay for a different provider and do not want a second account.
  Setup cost: that provider's API key; paid per token.
  What to check: pieces and questions are embedded with the same provider's embedding model, and switching to it rebuilds the index rather than mixing vectors from two embedders.

### C3. Where will you ask your questions?
- **C3a — In a notebook that calls the program's functions. (Recommended - course default)**
  Pick this when you want to run the stages one at a time and look at what each produced, as the course did.
  Setup cost: a notebook runtime (Jupyter) installed locally; no account.
- **C3b — From the command line.**
  Pick this when you want to ask from a terminal or call the program from scripts.
  Setup cost: none.
  What to check: running the command with a question prints the answer, and with a debug flag also prints the retrieved pieces and the prompt; it works on stand-ins when no key is set.
- **C3c — In a small web page served on your machine.**
  Pick this when someone who does not use a terminal or notebook will ask the questions.
  Setup cost: a web framework package; no account.
  What to check: submitting a question in the page shows the answer and the names of the retrieved pieces, and the page works on stand-ins when no key is set.

### C4. Where are the indexed pieces kept?
- **C4a — In memory; the index is rebuilt every time the program starts. (Recommended - course default)**
  Pick this when the collection is small enough to embed at every start (the course's catalog had about a thousand short rows).
  Setup cost: none; with a paid embedder, every start pays to embed the collection again.
- **C4b — Saved to disk and reused until the documents change.**
  Pick this when the collection is large, or re-embedding at every start costs you noticeable time or money.
  Setup cost: an embedded on-disk vector store package; no server, no account.
  What to check: after a restart with unchanged documents no piece is embedded again, and changing one document's text re-embeds that document before the next question.
- **C4c — A vector database server.**
  Pick this when several programs, people or machines must share one index.
  Setup cost: running a database server (container or install) or a hosted account.
  What to check: an index built by one process is queried by a second process, which returns the same ranked pieces for the same question.

### C5. How are the retrieved pieces combined into one answer?
- **C5a — "Stuff": all retrieved pieces go into one prompt; one model call. (Recommended - course default)**
  Pick this when the retrieved pieces together fit comfortably in one prompt, as with short records.
  Setup cost: none; one model call per question; it stops working once the pieces exceed the model's context length.
- **C5b — "Map-reduce": one call per piece, then one call that combines the partial answers.**
  Pick this when many or long pieces must be consulted and they do not fit in one prompt together.
  Setup cost: none; k+1 calls per question (the per-piece calls can run in parallel); each piece is treated independently of the others.
  What to check: each retrieved piece gets its own model call with the question, and one final call combines those partial answers into the answer (k+1 calls for k pieces).
- **C5c — "Refine": pieces are read one after another, improving the answer each time.**
  Pick this when the answer has to be built up by combining information spread across many pieces and longer answers are welcome.
  Setup cost: none; k calls per question, one after another, so it is slower than map-reduce.
  What to check: the pieces are processed in rank order, each call receiving the answer so far plus the next piece, and the final answer is the last call's output (k calls for k pieces).
- **C5d — "Map-rerank": one call per piece returns an answer and a score; the best-scored answer wins.**
  Pick this when the answer is expected to sit in a single piece and you want the answer from the best-supported piece.
  Setup cost: none; k calls per question (independent, can run in parallel); relies on the model to score well, so the scoring instructions must say what earns a high score.
  What to check: each retrieved piece gets its own call returning an answer and a numeric score, and the answer with the highest score is returned (k calls for k pieces).

### C6. Bring something back that this build leaves out?
- **C6a — Nothing; build only the question-answering program. (Recommended)**
  Pick this when you want the smallest program that answers questions from your documents.
  Setup cost: none.
- **C6b — Add an evaluation run.**
  Pick this when you plan to change models, settings or the store and need to know whether answers got better or worse.
  Setup cost: none beyond C2; each evaluation run spends model calls on generating examples and grading.
  What to check: a set of question–answer examples (some written by hand, some generated by the model from single pieces) is run through the program and each prediction is graded CORRECT or INCORRECT by the model comparing meaning, so a short true answer ("Yes") and a long correct prediction that never contains the word "yes" are graded correct.
- **C6c — Remember the conversation so follow-up questions work.**
  Pick this when people will ask follow-ups that point back to earlier turns ("does it come with pockets?" right after asking about one jacket).
  Setup cost: none; each question sends the recent conversation too, so it costs more tokens.
  What to check: a follow-up that refers to the previous turn retrieves pieces about the item named in that turn, every question still retrieves its own pieces, and the conversation sent with each question is capped at the most recent few exchanges.
- **C6d — Both: an evaluation run and conversation memory.**
  Pick this when both situations above apply.
  Setup cost: as C6b plus C6c.
  What to check: both the C6b and the C6c sentences hold.

### Departures from the course
| # | Where | What this build does | What the course did | Why |
|---|---|---|---|---|
| D1 | Models in tests and keyless runs | Scripted stand-in embedder and scripted stand-in chat model (declared in the sample data) | OpenAI embeddings and OpenAI chat model, key required | Tests must run offline with no key (P6); the real provider is used whenever a key is present |
| D2 | Library versions | Current releases | Install lines unpinned (`--upgrade`); a notebook note records `langchain==0.0.179` and `openai==0.27.7` as what that notebook used | No pin in an install line; the course-era versions no longer match current APIs |
| D3 | Sample data | An 8-row catalog written for this spec | A provided ~1,000-row outdoor-clothing catalog | No course data is copied; 8 rows keep every expected outcome checkable by hand |
| D4 | Chat model | A current model picked at the checklist | `gpt-3.5-turbo` (`gpt-3.5-turbo-0301` before 2024-06-12) | Model names go stale |
| D5 | Piece separator | `<<<<>>>>>` between pieces in the prompt | The Q&A lesson used the chain's own default, and its hand-built prompt joined pieces with nothing between them; the Evaluation lesson's rebuilt app used `<<<<>>>>>` | Picked by the "final end-to-end app" rule (see Background) |
| D6 | Code layout | The stages live in an importable package; the notebook calls it | All code inline in notebook cells | Tests must be able to run the stages (addition) |
| D7 | Ranking details | Cosine similarity, rounded to 6 decimals, ties broken by row order | The course says "pick the n most similar" without naming the measure or a tie rule | Two builds must rank identically (addition) |
| D8 | Evaluation | Not built unless C6b/C6d | The Evaluation lesson evaluated the same app | Evaluation does not change any stage of the program; it is offered at C6 |

---

## 2. Objective and Not Included

**Objective:** a program that answers a person's plain-language questions about their own collection of documents, using the few pieces of the collection most similar in meaning to the question.

**Not Included**
| Item | Tag |
|---|---|
| Splitting long documents into pieces | *decided by question C1* |
| Saving the index between runs; a shared vector database | *decided by question C4* |
| Map-reduce, refine and map-rerank combining | *decided by question C5* |
| Evaluation run (example generation and model grading) | *decided by question C6* |
| Conversation memory for follow-ups | *decided by question C6* |
| Hosted run-tracing and dataset platform | *can be added on request* |
| Agents that pick tools (web search, encyclopedia lookup, calculator, code runner, custom tools) | *can be added on request* |
| Routing a question between specialist prompts; multi-step sequential chains | *can be added on request* |
| Parsing answers into structured fields (JSON) | *can be added on request* |
| Grafting this program onto an existing codebase | *not available in this build* |

---

## 3. Tech stack, versions and secrets

- **Language:** Python 3, current release (the course did not pin Python).
- **Framework:** LangChain, current release (course install lines: `pip install --upgrade langchain`, unpinned). Use it for loading, the vector store, the retriever and the answer chain where current releases provide them; course-era class names are listed under "Names that go stale".
- **Provider SDK (C2a):** current `openai` and LangChain's OpenAI integration (course: unpinned `pip install openai`).
- **Vector store (C4a):** an in-memory vector store from the LangChain ecosystem (the course used an in-memory DocArray store, installed with an unpinned `pip install docarray`). It is not heavy: no server, no account.
- **Secrets:** `python-dotenv` (course: unpinned). `OPENAI_API_KEY` is read from the environment or from a local `.env` file. `.env` is listed in `.gitignore`.
- **Tests (addition):** `pytest`, with a `live` marker; `nbclient` (or `nbconvert`) to execute the notebook headless.
- **Notebook (C3a):** Jupyter, current release.

Files:
- `docqa/` — the importable package (the stages and the stand-ins).
- `sample_data/catalog.csv`, `sample_data/standin_embedder.json`, `sample_data/standin_replies.json` — section 7.
- `ask_your_documents.ipynb` — the notebook (C3a).
- `tests/` — the tests in section 7.
- `resolved-decisions.md` — the gate checklist.

---

## 4. Contracts

### 4.1 Piece (one indexed unit)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Piece",
  "type": "object",
  "required": ["id", "row", "source", "text"],
  "additionalProperties": false,
  "properties": {
    "id":     {"type": "integer", "minimum": 1, "description": "Equals row under C1a"},
    "row":    {"type": "integer", "minimum": 1, "description": "1-based data-row number in the CSV (header excluded)"},
    "source": {"type": "string", "description": "File name the piece came from, e.g. catalog.csv"},
    "text":   {"type": "string", "minLength": 1, "description": "One line per CSV column in header order, each 'column: value', joined by a newline"}
  }
}
```

### 4.2 Index entry (what the store holds)
```json
{
  "title": "IndexEntry",
  "type": "object",
  "required": ["piece", "vector"],
  "properties": {
    "piece":  {"$ref": "Piece"},
    "vector": {"type": "array", "items": {"type": "number"}, "minItems": 1,
               "description": "Embedding of piece.text; all vectors in one index have the same length"}
  }
}
```

### 4.3 Answer result (returned by the program's answer function)
```json
{
  "title": "AnswerResult",
  "type": "object",
  "required": ["question", "answer", "pieces", "models", "model_calls"],
  "additionalProperties": false,
  "properties": {
    "question":    {"type": "string", "minLength": 1},
    "answer":      {"type": "string", "description": "The answer model's reply, unchanged"},
    "pieces": {
      "type": "array", "maxItems": 4,
      "description": "The retrieved pieces in rank order; length = top_k when the index holds at least top_k pieces",
      "items": {
        "type": "object",
        "required": ["id", "source", "text", "score"],
        "properties": {
          "id":     {"type": "integer"},
          "source": {"type": "string"},
          "text":   {"type": "string"},
          "score":  {"type": "number", "minimum": -1, "maximum": 1, "description": "Cosine similarity rounded to 6 decimals"}
        }
      }
    },
    "models":      {"enum": ["stand-in", "provider"]},
    "model_calls": {"type": "integer", "minimum": 1, "description": "Answer-model calls made for this question; 1 under C5a"}
  }
}
```
`maxItems` follows `top_k`; change it with the setting.

### 4.4 Model roles
| Role | Course model | Used for | Offline stand-in |
|---|---|---|---|
| `embedder` | OpenAI embeddings through LangChain's OpenAI embeddings class, default model (the course does not name it; its vectors have "over a thousand" numbers) | Embedding every piece and every question | Scripted concept embedder (`standin_embedder.json`) |
| `answerer` | `gpt-3.5-turbo` at temperature 0 | Writing the answer from the question and the retrieved pieces | Scripted replies (`standin_replies.json`) |

Under C6b/C6d add two roles, both from the chosen provider: `example_writer` (writes a question and answer from one piece) and `grader` (temperature 0; grades a prediction against an answer).

### 4.5 Settings
| Setting | Value | Source | Change this when … |
|---|---|---|---|
| `top_k` | 4 | Q&A lesson: the similarity search "returns four documents"; the course never sets n itself | you need more or fewer pieces in each prompt (this spec's guidance; the course gives none) |
| `answer_temperature` | 0.0 | Models lesson: "When I'm building applications ... set the temperature ... to be equal to zero" (the default is 0.7); Q&A and Evaluation notebooks set 0.0 | — keep it at 0 for factual answers; the course raises temperature only for creative naming in the Chains lesson |
| `piece_separator` | `<<<<>>>>>` | Evaluation-lesson notebook, the rebuilt question-answering chain | your pieces themselves contain that string |
| `debug` | `false` | Evaluation lesson: debug output is turned on to inspect one run, then off "to just not print everything out" | an answer is wrong: turn it on and look at the retrieved pieces first ("it's actually the retrieval step that's messing up") |
| `similarity` | cosine, rounded to 6 decimals, ties by lower row | Addition (D7) | never; it keeps rankings reproducible |
| `data_path` | `sample_data/catalog.csv` | Addition | you point the program at your own collection |
| `answer_instruction` | "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer." | Evaluation lesson: the prompt the course's question-answering chain sends, shown in debug output | never; it carries rule R6 |

---

## 5. Business rules

**What must stay true (the pattern card — every option keeps every item):**
1. **The documents are indexed by meaning before any question.** Each piece of text gets a numeric representation of its meaning, stored next to its original text, so pieces with similar meaning can be found later. → T2, T4
2. **For each question, only the few stored pieces most similar in meaning are retrieved, not the whole collection.** → T5, T6
3. **A language model writes the answer from the question plus the retrieved pieces, so the answer rests on the person's documents.** → T6, T7

**Rules of the recommended build:**
- **R1 Load.** Each data row of the CSV becomes exactly one piece. Its text is one line per column in header order, `column: value`, joined by newlines; it records the file name and its 1-based row number. No splitting (C1a). → T1
- **R2 Index before questions, once per start.** At start, before the first question, every piece is embedded and stored with its original text. Asking further questions in the same session never re-embeds pieces (C4a: the index lives in memory and is rebuilt at the next start). → T2, T3
- **R3 Retrieve by meaning.** The question is embedded with the same embedder as the pieces. Pieces are ranked by cosine similarity, rounded to 6 decimals, highest first; equal scores keep lower row first; a zero vector has similarity 0 to everything. The first `top_k` are retrieved. → T4, T5, T13
- **R4 Only the retrieved pieces reach the model.** The answer prompt holds the `top_k` retrieved pieces and nothing else from the collection. *(Guards a failure the course warned about: a model can only inspect a few thousand words at a time, and stuffing too much makes the prompt larger than the context length.)* → T6
- **R5 Stuff and answer.** One answer-model call per question with two messages: a system message made of `answer_instruction`, a blank line, then the retrieved pieces' texts in rank order joined by `piece_separator`; and a user message that is exactly the question. The model's reply is returned unchanged as `answer`. → T6, T7, T13
- **R6 Say "I don't know".** The system message always carries the `answer_instruction`, which tells the model to say it does not know rather than make up an answer; the program passes such a reply through unchanged. *(Guards a failure the course's prompt warns about: making up an answer.)* → T8, T14
- **R7 Temperature.** The answer call uses `answer_temperature` = 0.0. If the current model picked at the gate rejects a temperature parameter, omit it and record that in `resolved-decisions.md` (addition). → T9
- **R8 Debug.** With `debug` on, the answer function prints, before returning, each retrieved piece's id, score and text, then both prompt messages. With `debug` off it prints nothing. *(Guards a failure the course warned about: wrong answers usually come from retrieval, and the final answer alone does not show it.)* → T10
- **R9 Models.** With `OPENAI_API_KEY` set (environment or `.env`), the real provider is used for both roles and `models` = `"provider"`. Without it, both roles use the scripted stand-ins, `models` = `"stand-in"`, and a one-line notice containing the word `stand-in` goes to standard error once per session. Offline tests always use the stand-ins, even when a key is present. → T11, T13
- **R10 Notebook.** The notebook loads the sample catalog through the package, builds the index and answers questions by calling the package's answer function; it runs top to bottom on a fresh kernel. → T12

---

## 6. Tests

### 6.1 Sample data

**`sample_data/catalog.csv`** (header `id,name,description`; written for this spec, no course data):
| id | name | description |
|---|---|---|
| 1 | TrailLite Sun Hoodie | Lightweight hoodie with UPF 50 sun protection fabric. Thumbholes keep sleeves in place. |
| 2 | Harbor Linen Shirt | Breathable linen button-down shirt for hot days. Offers UPF 30 sun protection. |
| 3 | Stormline Rain Shell | Waterproof rain jacket with sealed seams and an adjustable hood. |
| 4 | Ridge Fleece Pullover | Warm fleece pullover with two zip side pockets. |
| 5 | Summit Hiking Boots | Waterproof leather hiking boots with a cushioned sole. |
| 6 | Meadow Kids Sun Hat | Wide-brim kids hat with UPF 50 sun protection and a chin strap. |
| 7 | Glacier Down Parka | Insulated down parka rated for winter cold, from the Northfield collection. |
| 8 | Canyon Cargo Shorts | Quick-dry cargo shorts with six pockets. |

Under R1, piece 4's text is exactly:
`id: 4` / `name: Ridge Fleece Pullover` / `description: Warm fleece pullover with two zip side pockets.` (three lines joined by `\n`).

**`sample_data/standin_embedder.json` — scripted stand-in embedder (stands in for the course's OpenAI embeddings).** It turns text into an 8-number vector, one number per concept, in this order: `sun, water, warm, pocket, feet, kids, shirt, hat`. Text is lowercased and split on every character that is not a letter or digit; each token found in a concept's list adds 1 to that concept. Tokens in no list are ignored.
| Concept | Tokens |
|---|---|
| sun | sun, sunny, sunblocking, upf |
| water | waterproof, rain, rainy, wet |
| warm | warm, fleece, insulated, winter, cold, parka |
| pocket | pocket, pockets |
| feet | boot, boots, hiking |
| kids | kids, child, children |
| shirt | shirt, shirts, hoodie |
| hat | hat, cap |

Vectors this gives for the pieces (the `id: N` line adds nothing):
| id | sun | water | warm | pocket | feet | kids | shirt | hat |
|---|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| 2 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| 3 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| 4 | 0 | 0 | 3 | 1 | 0 | 0 | 0 | 0 |
| 5 | 0 | 1 | 0 | 0 | 4 | 0 | 0 | 0 |
| 6 | 3 | 0 | 0 | 0 | 0 | 2 | 0 | 2 |
| 7 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| 8 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

The stand-in knows "sunblocking" means sun protection only because its table says so; it is a stand-in for a real meaning model, not one.

**Sample questions:**
| Id | Question | Stand-in vector |
|---|---|---|
| Q1 | `Please suggest a shirt with sunblocking` | sun 1, shirt 1 |
| Q2 | `Does the Ridge Fleece Pullover have side pockets?` | warm 1, pocket 1 |
| Q3 | `Do you sell bicycle helmets?` | all zero (planted: the collection does not hold the answer) |
| Q4 | `What collection is the Glacier Down Parka from?` | warm 1 |

**`sample_data/standin_replies.json` — scripted stand-in answer model (stands in for the course's chat model).** It looks only at the user message (the question) and replies:
| Question | Reply |
|---|---|
| Q1 | `The Harbor Linen Shirt and the TrailLite Sun Hoodie both offer sun protection.` |
| Q2 | `Yes, the Ridge Fleece Pullover has two zip side pockets.` |
| Q4 | `The Glacier Down Parka is from the Northfield collection.` |
| anything else (including Q3) | `I don't know.` |
It records every call: the messages and the parameters (including temperature).

### 6.2 Test table
Unless stated, tests run offline on the stand-ins with the default settings and the sample catalog.

| Test | Given | When | Then | Rules |
|---|---|---|---|---|
| T1 | `catalog.csv` | it is loaded | 8 pieces; piece 4 has `row` 4, `source` `catalog.csv` and the exact three-line text above; no piece holds two rows | R1 |
| T2 | a fresh start, no question asked yet | the index is built | the store exists and holds 8 entries; each entry's text equals its piece's text and its vector equals the stand-in vector in the table (length 8); the embedder has embedded the 8 pieces before any question | R2, card 1 |
| T3 | the index from T2 | Q2 and then Q4 are asked in the same session | the embedder embedded pieces 8 times in total (no re-embedding) plus one embedding per question (2) | R2 |
| T4 | the index | Q1 is asked | retrieved ids `[2, 1, 6, 3]` with scores `[1.0, 0.980581, 0.514496, 0.0]`; no piece contains the word "sunblocking" yet both sun-protection shirts rank first | R3, card 1 |
| T5 | the index | Q2 is asked; then Q4 | Q2 → ids `[4, 7, 8, 1]`, scores `[0.894427, 0.707107, 0.707107, 0.0]` (7 before 8: equal score, lower row); Q4 → ids `[7, 4, 1, 2]`, scores `[1.0, 0.948683, 0.0, 0.0]`; every result has exactly 4 pieces out of 8 | R3, card 2 |
| T6 | the index | Q2 is asked | the answer model received exactly 2 messages; the system message starts with `answer_instruction`, then holds the texts of pieces 4, 7, 8, 1 in that order with exactly 3 occurrences of `<<<<>>>>>`, and holds none of the texts of pieces 2, 3, 5, 6; the user message is exactly Q2 | R4, R5, card 2, card 3 |
| T7 | the index | Q2 is asked | `answer` = `Yes, the Ridge Fleece Pullover has two zip side pockets.`; `pieces` ids `[4, 7, 8, 1]`; `model_calls` = 1; the result validates against the AnswerResult schema | R5, card 3 |
| T8 | the index | Q3 is asked | retrieved ids `[1, 2, 3, 4]`, all scores 0.0; the system message contains `answer_instruction`; `answer` = `I don't know.` | R6 |
| T9 | the index | Q2 is asked | the recorded answer call has temperature 0.0 | R7 |
| T10 | the index | Q2 is asked with `debug` on, then again with `debug` off | with debug: standard output lists ids 4, 7, 8, 1 with scores 0.894427, 0.707107, 0.707107, 0.0 and their texts, then the system message and the user message; without debug: standard output is empty | R8 |
| T11 | `OPENAI_API_KEY` unset and no `.env` | a session asks Q2 then Q4 | both results have `models` = `"stand-in"`; standard error holds exactly one line containing `stand-in`; Q2's answer is the scripted Q2 reply | R9 |
| T12 | `OPENAI_API_KEY` unset | the notebook is executed headless on a fresh kernel | it finishes without error and its last cell's output contains `Yes, the Ridge Fleece Pullover has two zip side pockets.` | R10 |
| T13 `live` | `OPENAI_API_KEY` set; real provider | `Which jacket keeps me dry in heavy rain?` is asked | `models` = `"provider"`; retrieved pieces include id 3; the answer names `Stormline Rain Shell` | R3, R5, R9 |
| T14 `live` | `OPENAI_API_KEY` set; real provider | Q3 is asked | the answer says it does not know (contains "don't know" or "do not know", any case) and does not offer any catalog item as a helmet | R6 |

Rules ↔ tests: R1 T1 · R2 T2 T3 · R3 T4 T5 T13 · R4 T6 · R5 T6 T7 T13 · R6 T8 T14 · R7 T9 · R8 T10 · R9 T11 T13 · R10 T12.

---

## 7. Standing permissions

- **Always:** run the offline tests after every change; keep every stand-in labelled as a stand-in in code, output and docs; read secrets from the environment or `.env`.
- **Ask first:** changing an answered question or a setting once the build holds data; anything that sends data to a third party beyond the provider chosen at C2.
- **Never:** invent provenance (claim the course did something it did not); answer when the program should say it does not know; change sample data or scripted replies to make a test pass; commit secrets or `.env`.

---

## 8. Test plan

1. `python -m pytest -m "not live"` — T1–T12. Must pass with no key and no network.
2. `python -m pytest -m live` — T13–T14. Runs automatically when `OPENAI_API_KEY` is set; skipped (and reported as skipped) otherwise.
3. T12 executes `ask_your_documents.ipynb` headless from inside the test suite.
4. Adjust for the chosen options: a test that checks something only the recommended option does (e.g. T1's one-row-one-piece under C1b, T7's `model_calls` = 1 under C5b–C5d) is rewritten for the chosen option, and the change is noted in `resolved-decisions.md`.
5. For each chosen non-recommended option, turn its "what to check" sentence (copied into the checklist) into a test, run it, and report it.

Report a result per test with evidence (test output, file paths). "Should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes.

Finish with a diagram of the built app introduced by the sentence "This is the infra/structure diagram of this app".

---

## 9. Background notes (for the build agent)

### The program
A program that answers a person's plain-language questions about their own collection of documents, using the few pieces most similar in meaning to the question. Stages:
- **load** — turn the collection into pieces a model can read; the course's CSV rows were already small, so "we actually don't need to do any chunking here".
- **(split)** — only for long documents (C1b); the course explains it ("we may not be able to pass the whole document to the language model") but its own data did not need it.
- **embed** — give each piece a numeric representation of its meaning, so similar text has similar vectors.
- **store** — keep each vector next to its original text; "that's what happens when we create the index".
- **retrieve** — embed the question, compare it with all stored vectors, pick the n most similar; needed because "language models can only inspect a few thousand words at a time".
- **answer** — pass the retrieved pieces and the question to a language model, which writes the answer; this "combine[s] these language models with data that they weren't originally trained on".

### Failures
The course demonstrated no failure of the question-answering program itself; it warned about three, each kept as a rule, a test and this note:
- **Too much text for the model.** What you see: the prompt exceeds the context length and the call fails. Why: models read only a few thousand words at once; the stuff method's slide adds "for large documents or many documents this will not work". Prevented by sending only `top_k` pieces (R4, T6); C5b–C5d exist for larger needs.
- **A made-up answer.** What you see: a confident answer to something the documents never say. Why: the model fills gaps from its training. Prevented by the course's own instruction "If you don't know the answer, just say that you don't know, don't try to make up an answer" (R6, T8, T14).
- **A wrong answer whose cause is hidden.** What you see: a wrong answer with no clue why. Why: "it's not necessarily the language model itself that's messing up. It's actually the retrieval step". Prevented by the debug setting showing the retrieved pieces and the prompt (R8, T10).

Failures demonstrated in other lessons (not part of this program):
- Models lesson: the model's JSON-looking output is a string, so reading a key from it raises an error; an output parser fixes it.
- Memory lesson: a window memory keeping only 1 exchange forgets the user's name two turns later; the instructor says real use sets a larger window. Relevant to C6c: never offer a window of 1.
- Evaluation lesson: exact string matching cannot grade "Yes" against "The … does have side pockets" — the strings share no words; grading by meaning with a model is the fix. Relevant to C6b's check.
- Agents lesson: the agent first concluded the 2022 World Cup had not happened despite search results saying otherwise; "agents are still pretty exploratory". The notebook also warns the agent "will sometimes come to the wrong conclusion".
- Notebook note: the one-line index query originally used `text-davinci-003`, deprecated since 1 January 2024; the notebook substituted `gpt-3.5-turbo-instruct` and warns output may differ from the video.

### Why the questions and settings are what they are
- **C1** — the course loaded a CSV where each row is a document and skipped splitting because rows are small; it explains splitting for big documents and names PDFs, web pages and intranet documents as typical sources.
- **C2** — the course used OpenAI for both the chat model and the embeddings. Local and other hosted providers are this spec's additions for learners without that key; the course never discusses them.
- **C3** — the course ran everything in notebooks. The command line and the web page are additions.
- **C4** — the course chose the in-memory store because "it doesn't require connecting to an external database of any kind so it makes it really easy to get started", and said the store can be swapped "for a different type of vector store". Disk and server options are this spec's concrete forms of that swap.
- **C5** — from the Q&A lesson and its slides: stuff is "the simplest method", "quite cheap and it works pretty well", one call, but fails when the prompt exceeds the context length; map-reduce "can operate over any number of documents", runs calls in parallel, "does take a lot more calls" and treats documents as independent; refine "builds upon the answer from the previous document", gives longer answers, is slower and "takes just as many calls as Map_reduce"; map-rerank is "a bit more experimental", does one call per document returning a score and keeps the highest, and "relies on the language model to know what the score should be". The course says stuff is the most common and map-reduce second.
- **C6** — the Evaluation lesson rebuilt the same app and evaluated it: two hand-written examples, more generated by a model from individual documents (five in the notebook), predictions for all, then a model grader; it also showed the debug view and a hosted platform that stores runs and example sets. The Memory lesson taught conversation memory with a plain chatbot, never with document question answering. Neither changes a stage of the program, so both sit outside the recommended build. No option on C6 carries "(course default)": the course's question-answering lesson built the program without either, and evaluation came in its own lesson.

Subjects that are not questions:
- **The learner's project** — no option would differ by project beyond C1–C2; asking would be a question for its own sake.
- **The one-line index builder vs the step-by-step chain** — the course says "these two things equate to the same result"; it is code organisation, not behaviour.
- **The hand-assembled prompt** (pieces joined and sent with the question, no instruction) — an earlier step the course showed on the way to the chain; it does the same job as C5a with less, so no learner situation picks it.
- **Similarity search without an answer** — returns pieces but no answer; breaks card item 3.
- **Other retriever methods** ("some less advanced, some more advanced") — the course names none; any that does not compare meaning breaks card item 1.
- **Agents with tools** — the answer may come from web search or an encyclopedia rather than the documents; breaks card item 3.
- **Router chain** — its default route is "a generic call to the language model", answering from the model's own knowledge; breaks card item 3.
- **Sequential chains, prompt templates, output parsers** — they change no stage; the course's own query asks for a markdown table in the question itself, which needs no parser. Listed as *can be added on request*.
- **Hosted run-tracing platform** — needs a hosted account; the debug setting and C6b cover inspecting runs and building example sets locally. *Can be added on request.*
- **Temperature, top_k, separator, debug** — settings (4.3 of the guide): they tune a part that is there.

Where each picked value came from:
- `top_k` = 4: Q&A lesson transcript ("it returns four documents"; later "we only got four documents back"). The notebook never sets it; 4 is what the course's store returned by default.
- `answer_temperature` = 0.0: Models lesson transcript and every question-answering cell (Q&A notebook cell 28; Evaluation notebook cell 8). The Chains lesson uses 0.9 for creative naming only.
- `piece_separator` = `<<<<>>>>>`: the course gives two behaviours. The Q&A notebook's hand-built prompt joins piece texts with nothing between them (cell 29), and its chain uses the chain's own default; the Evaluation notebook's rebuilt chain sets `<<<<>>>>>` (cell 8). The instructor never states a separator, so rule (1) does not apply; rule (2), the course's final end-to-end app, picks `<<<<>>>>>`. Note for the build agent: the hand-built join with no separator runs pieces together; it looks like a shortcut, and the final app does not use it.
- `answer_instruction`: quoted from the Evaluation lesson transcript, where the debug output shows the prompt the course's chain sends.
- Chat model `gpt-3.5-turbo`: every notebook switches to it after 2024-06-12 (earlier: `gpt-3.5-turbo-0301`).
- Similarity measure, rounding, tie order, piece text layout, C1b piece size: this spec's additions.

Other course behaviours, kept as facts:
- The Q&A notebook first builds the index in one line from the CSV loader and queries it with `gpt-3.5-turbo-instruct` (the replacement model), then rebuilds step by step: load, embed with OpenAI embeddings, store in the in-memory store, retrieve, answer with the chat model at temperature 0 using the stuff method with verbose output on.
- It then shows the index builder can take an explicit embedding object; that rebuilt index is never queried in the notebook.
- The Evaluation notebook builds its retriever from the one-line index and its chain with the stuff method, verbose output and the `<<<<>>>>>` separator.

### Names that go stale
Treat these as search keywords against current documentation, not guaranteed imports:
- LangChain (course era ~0.0.179): `langchain.chat_models.ChatOpenAI`, `langchain.llms.OpenAI`, `langchain.embeddings.OpenAIEmbeddings`, `langchain.document_loaders.CSVLoader`, `langchain.vectorstores.DocArrayInMemorySearch`, `langchain.indexes.VectorstoreIndexCreator` (`from_loaders`, `index.query`, `index.vectorstore`), `RetrievalQA.from_chain_type` (`chain_type="stuff"`, `chain_type_kwargs={"document_separator": …}`, `verbose`), `similarity_search`, `as_retriever`, `embed_query`, `from_documents`, `call_as_llm`, `chain.run`, `langchain.debug`.
- C6b: `langchain.evaluation.qa.QAGenerateChain` (`apply_and_parse`), `QAEvalChain` (`evaluate`), `chain.apply`.
- C6c: `ConversationBufferMemory`, `ConversationBufferWindowMemory`, `ConversationTokenBufferMemory`, `ConversationSummaryBufferMemory`, `ConversationChain`.
- OpenAI SDK (course era 0.27.7): `openai.ChatCompletion.create`, `openai.api_key`.
- Models: `gpt-3.5-turbo`, `gpt-3.5-turbo-0301`, `gpt-3.5-turbo-instruct`, `text-davinci-003` (deprecated since 1 January 2024 per the course notebook).
- Request parameters: the course's models all accepted `temperature`; if the current model chosen at the gate rejects it, follow R7.

### Course names
| Course name | Spec term | Binding? |
|---|---|---|
| `OutdoorClothingCatalog_1000.csv` | the collection; here `sample_data/catalog.csv` | no |
| document (one CSV row) | piece | no |
| index / vector store / vector database | the store / the index | no |
| retriever | retrieve stage | no |
| `RetrievalQA` with `stuff` | answer stage, C5a | no |
| `map_reduce`, `refine`, `map_rerank` | C5b, C5c, C5d | no |
| `document_separator` | `piece_separator` | value `<<<<>>>>>` is binding |
| `langchain.debug` | `debug` setting | no |
| `llm_model` | `answerer` role | no |

### Lesson map
Transcript numbering (the notebooks count one lower from lesson 2 on):
| Transcript lesson | Notebook | Notes taken from it |
|---|---|---|
| 1 Introduction | — | course scope only |
| 2 Models, Prompts and Parsers | L1 | temperature 0 for applications; output-parser failure (background) |
| 3 Memory | L2 | C6c; window-of-1 forgetting (background) |
| 4 Chains | L3 | sequential and router chains → Not Included; temperature 0.9 for naming |
| 5 Question and Answer | L4-QnA | the program, its stages, C1, C2, C4, C5, `top_k`, failures 1 and 3's grounding |
| 6 Evaluation | L5-Evaluation | `answer_instruction`, `piece_separator`, debug setting, C6b, exact-match failure (background) |
| 7 Agents | L6-Agents | agents → Not Included; agent failure (background) |
| 8 Conclusion | — | nothing |

Slides read: question_and_answer 1–7 (Q&A lesson: documents and the model, embeddings, the vector database's create and index steps, process with the model, stuff method, three additional methods; slides 6 and 7 are the same slide, one cropped), chains 1–4 (Chains lesson), memory 1–2 (Memory lesson). Each is talked through in its lesson's transcript, so each counted like that transcript. The stuff-method slide's "cons" line (prompt larger than the context length) is the one slide-only wording used; it agrees with the transcript.

Nothing in this spec requires access to the course.

---

*Spec v2-draft · course: LangChain for LLM Application Development · project: Ask Your Documents · when the build agent does something unexpected, add the missing constraint here and re-run.*
