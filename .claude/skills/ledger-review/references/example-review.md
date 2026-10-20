<!-- Reference example for /ledger-review: the review comment posted on PR #63 (agent-memory spec, guide 5caba53), with two cells standardized (the D1b separator and the D4b label) and the closing line updated for per-decision threads. It restates only that spec's Ledger. -->
## Decision Ledger for review: agent-memory

A plain-language version of the spec's Decision Ledger, for review. Each heading links to its row in this PR's `spec.md`.

**How to read it.** Before building, the build agent asks the learner one question per decision below. Each table lists the answers they can pick.
- ✅ **Recommended**: what the default build uses (chosen when the spec was written, not tailored to the learner).
- 📘 **Course used**: what the course itself did.
- **If chosen**: what the build leaves out or changes. "—" means nothing.

Some questions are asked only after a certain earlier answer; they say so.

---

### [L1](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L87) · What the assistant is for
**The learner is asked:** what are you building? **Why it's a choice:** the default is the course's own example; a learner with a different project swaps it.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| L1a | A command-line research assistant that remembers conversations across sessions and works with research papers | None | ✅ 📘 | — |
| L1b | An assistant for your own field, on the same memory design, with your own tools and starting data | None | | The tools, starting data and the assistant's role line become yours; their tests are rewritten to match |

### [L2](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L88) · What the paper library starts with
**The learner is asked:** what data does the assistant start with? **Why it's a choice:** the course loaded 100 real arXiv records; the default uses invented records so the build runs offline.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| L2a | Five invented paper records, loaded by a `seed` command | None | ✅ | — |
| L2b | The first 100 records of the public arXiv dataset on Hugging Face | A network download, no key | 📘 | The loading test checks up to 100 real records and needs the network |
| L2c | Your own documents, one record each | Your files | | The loading test checks your records |

### [L3](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L89) · What "working" means
**The learner is asked:** what should the finished assistant be able to do? **Why it's a choice:** the default is the course's closing demo; a learner can state their own goal.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| L3a | Ask a follow-up that depends on an earlier turn, restart the program, and still get answers that use earlier turns, including details recovered from summarized conversation | None | ✅ 📘 | — |
| L3b | A goal you state (what search must find, what answers must guarantee) | None | | Tests for your goal are added; the rest stay |

### [L4](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L90) · Which AI model provider, for live use
**The learner is asked:** which model provider should the assistant use? **Why it's a choice:** the course used OpenAI; another provider changes the message format, not the memory design. The offline tests never call a live model.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| L4a | OpenAI, with tool calling | An OpenAI API key (live use only) | ✅ 📘 | — |
| L4b | Anthropic, with tool use | An Anthropic API key | | Tool messages use Anthropic's format; the key check names its key |
| L4c | A local open-weights model behind an OpenAI-compatible server | Heavy: a local model server and hardware able to run it | | Tool messages use the server's format; the key check becomes a server-address check |

### [L5](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L91) · Where it runs
**The learner is asked:** where should the assistant run? **Why it's a choice:** the course ran in notebooks and wiped its tables each lesson; memory surviving restarts is the course's point, so the default keeps data between runs.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| L5a | A local command-line program with a database file on your machine | None | ✅ | — |
| L5b | Jupyter notebook cells, one call per question | None stated | 📘 | Commands become notebook cells; the restart test uses two notebook sessions |

### [L6](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L92) · What this build leaves out
**The learner is asked:** here is everything this build does not include; keep it, or bring something back? (The question shows the full list.) **Why it's a choice:** the course made no choice here.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| L6a | Keep everything left out as listed | None | ✅ | — |
| L6b | Bring one or more items back, named in free text | Per item (each item's note in the list says) | | The items are built; tests are added only for items marked as restorable |

### [D1](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L93) · Which memories the assistant keeps
**The learner is asked:** should the assistant keep a full set of memory types, or only the chat history? **Why it's a choice:** Lesson 2 shows a chat-history-only agent working, then argues it isn't enough; Lesson 3 builds the full set.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| D1a | Seven kinds of memory: chat history, a tool log, a paper library, past workflows, a tool catalogue, people and things mentioned, and summaries | None | ✅ 📘 | — |
| D1b | Chat history only; every tool is offered on every turn | None | shown in the course, no code shipped | Saving papers, past workflows, tool search, people/things memory and summaries; 30 tests no longer apply. **Skips 5 later questions** (D2, D3, D4, RR2, C1) |

### [D2](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L94) · Rewriting tool descriptions to make tools easier to find
*Asked only if D1 = D1a.* **The learner is asked:** should the model rewrite each tool's description when the tool is added? **Why it's a choice:** Lesson 4 shows rewritten descriptions find the right tool more reliably, at the cost of two model calls per tool; plain descriptions also work.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| D2a | As the course's final agent: some tools rewritten, others plain | None | ✅ 📘 | — |
| D2b | Every tool rewritten | None | | One test checks that all tools are marked rewritten |
| D2c | No tool rewritten: each tool is found by its name, its own description and its parameters | None | | Leaves out the rewrite step; 1 test no longer applies |

### [D3](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L95) · What runs automatically, and what the model decides to do
*Asked only if D1 = D1a.* **The learner is asked:** which memory steps run automatically every turn, and which does the model choose to call? **Why it's a choice:** Lesson 3 argues automatic steps are predictable and complete, while model-called steps save cost and use judgment.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| D3a | The course's split. Automatic: reading memory, choosing tools, shrinking the conversation when it gets too long, saving each turn. Model-called: summarize, expand a summary, search tools, paper tools | None | ✅ 📘 | — |
| D3b | As D3a, but saving people and things mentioned becomes a tool the model calls | None | never built by the course; the spec gives no tests for it | Leaves out automatic saving of people and things; 3 tests no longer apply |
| D3c | As D3a, but summaries happen only when the model asks; nothing shrinks the conversation automatically at the limit | None | | Leaves out automatic shrinking; 1 test no longer applies |

### [D4](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L96) · Can a shrunk conversation be recovered?
*Asked only if D1 = D1a.* **The learner is asked:** when the conversation is summarized, should the original messages stay retrievable? **Why it's a choice:** Lesson 5 argues a plain summary always loses detail, while compaction keeps the originals so the model can pull them back.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| D4a | Recoverable: a short summary with an ID replaces the conversation; the originals stay in the database, and the model can expand them | None | ✅ 📘 | — |
| D4b | Lossy: the summary replaces the conversation and the originals are not kept | None | never built by the course; the spec gives no tests for it | Leaves out expanding a summary; 3 tests no longer apply |

### [RR1](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L97) · Which database stores the memories
**The learner is asked:** which database should hold the assistant's memories? **Why it's a choice:** the course used Oracle, which needs an admin-installed database; the lesson is about the memory design, not the product.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| RR1a | A single SQLite file, built into Python | None | ✅ | — |
| RR1b | Oracle AI Database 26ai Free, as in the course | Heavy: a local database container, an admin account, the Oracle driver | 📘 | The tests need the database running; two ranking tests allow ties |
| RR1c | PostgreSQL with the pgvector extension | Heavy: a database server you install and run | | The same as RR1b |

### [RR2](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L98) · A web-search tool
*Asked only if D1 = D1a.* **The learner is asked:** should the assistant have a web-search tool that needs a key? **Why it's a choice:** Lesson 4 teaches "search and save" with Tavily, but the course's final agent doesn't use it; the paper tools already save what they find.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| RR2a | No web search; the paper tools save what they find | None | ✅ | — |
| RR2b | Tavily web search, saving each result | A Tavily API key | 📘 | Adds the tool; its check runs live |
| RR2c | A local fake web search, clearly labelled as fake, returning two fixed results | None | | Adds the tool |

### [RR3](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L99) · Which model the tests run against
**The learner is asked:** should the offline tests use a scripted fake model or the live one? **Why it's a choice:** a scripted model makes every test repeatable offline; a live model's answers vary from run to run.

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| RR3a | A scripted fake model, defined in the spec and labelled as fake | None | ✅ | — |
| RR3b | The course's live OpenAI models | Heavy: an OpenAI API key, paid usage on every run | 📘 | About 30 tests check only the shape of answers, not exact text |

### [C1](https://github.com/https-deeplearning-ai/spec-build-lab/blob/a701e19a2c22856076ec0a0b26bec5a6a242cd11/courses/agent-memory-building-memory-aware-agents/spec.md#L100) · Do summaries belong to one conversation thread?
*Asked only if D1 = D1a.* **The learner is asked:** should a summary be visible only in the thread it came from? **Why it's a choice:** the course did it both ways (Lesson 5 without threads, Lesson 6 with them).

| Ref | Option | Setup | Labels | If chosen |
|---|---|---|---|---|
| C1a | Each thread sees only its own summaries | None | ✅ 📘 | — |
| C1b | Every thread sees all summaries (the Lesson 5 notebook's way) | None | | Summaries record no thread; 2 tests change |

---

### Known open points (already flagged; tracked on #48)
1. **D4b (lossy)** is offered as a choice, but the spec's own list of failures names "summaries lose details" as a failure. It's open whether it should be a choice at all.
2. **RR2's rule** says every search tool saves its results, but the paper *search* tool only lists candidates and saves nothing (the *fetch* tool does).
3. **D2a** doesn't list which tools get rewritten; it points to the spec's test section for that.

*Reviewers: reply in the thread on each decision's row (for example under D1b); use this thread for the review as a whole.*

