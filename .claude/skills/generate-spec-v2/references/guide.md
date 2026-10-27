# Spec Generation Guide — v2 (draft)

*Guide v2.8, 2026-10-27. Every rule names the purpose clause (P1–P8) it serves. Owner decisions O1–O3 (settings never asked; the alternatives list is a working note; the test-suite model is not asked) were accepted on 2026-10-23.*

---

## 1. Purpose

### Who the spec is for
A learner has finished a course and wants to build something with what it taught. They hand the spec to a coding agent, the **build agent**, which asks them a few questions and then builds. The spec is the only thing the build agent reads; it cannot see the course.

A learner comes with one of two goals:
- **Build something like the course.** They want a working version of what the course built, running on their own machine.
- **Build their own version.** They want the same kind of program shaped for their own project. Example: after a course that answers questions about a product catalog, "ask my English notes".

The spec serves both. The first is the recommended build. The second is reached by answering the spec's questions differently.

### What the spec must do
**P1. One kind of program.** Every course teaches one design pattern. The spec describes the one kind of program that pattern builds. Material from other lessons appears only where it changes that program; otherwise it is a background note. The course's own example (its data, its topic) is one instance of the program, not the program itself.

**P2. A recommended build.** The spec defines one recommended version that follows the course's own choices. Where a course choice needs something the learner may not have (a paid API key, a hosted account, a huge download), it uses a lighter stand-in that does the same job, labelled honestly as a stand-in. The spec says where it departs from the course, and why.

**P3. Only real choices are asked.** A choice is asked only if the learner's project could change the answer: the spec must be able to say when a learner would pick something other than the recommended option. If it cannot, the subject is a background note. No question is asked just because every spec has it, including questions about the learner's project, data, model or machine. The course's choices set the recommended build; its arguments become the costs in "pick this when"; only what it shows failing is excluded.

**P4. Each choice explains itself.** Every question shows the question in plain words; the options, each with "pick this when …"; which option is recommended and which one the course used; and what each option costs to set up.

**P5. One list of what must stay true: the pattern card.** A short list states the essence of the course's pattern: what makes any build still this pattern, whatever the learner picks. It is the course's **pattern card**, confirmed by the owner. Every option must keep every item. Features of the full program are rules of the recommended build, which options may change.

**P6. The learner can finish and check the build.** The recommended build has exact tests that run offline on sample data the spec defines. Each other option has one plain sentence saying what to check, which the build agent turns into a test. The build is finished when the recommended tests, adjusted for the learner's choices, pass and each chosen option's check passes.

**P7. One question at a time.** Before building, the build agent asks its questions one at a time and writes the answers down before any code.

**P8. Faithful to the course.** What the spec says the course did matches the actual course. Anything the spec adds is labelled as an addition. The course's reasons and failure cases are kept as background notes.

### How this guide may change
A new rule may be added only if it serves one of P1–P8 or fixes a problem seen in a real build or with a real learner, and it must name which. Two generated specs disagreeing is not, on its own, a reason for a new rule. A change counts as an improvement only when specs made with it are shown better by builds (the recommended build and at least one learner's own version) and by the owner reading their questions.

---

## 2. Inputs and working rules

| Input | Required? | Good for |
|---|---|---|
| **Notebooks** (the course's code, cell by cell, including any README or docstrings shipped with it) | yes | What the course ran: parameters, model names, prompts, configuration. |
| **Transcripts** | yes | Lesson numbers and titles, the reasons behind choices, alternatives the instructor discussed, failures shown or warned about. |
| **Pattern card** (`courses/<name>/pattern.md`) | yes | The owner-confirmed essence of the course's pattern (P5): a few items, each quoting where the course states it. |
| **Slides** | optional | A slide the instructor talks through counts like that lesson's transcript. A slide that exists only in the deck counts less than code and transcripts: when they disagree, the slide loses and the disagreement is recorded. |

If notebooks or transcripts are missing, stop: no spec. If the pattern card is missing, write a proposed card instead (a few items, each with the course quote that supports it) and stop for the owner's confirmation: no spec. (P5, P8)

- **W1. Use only the supplied materials and the pattern card.** Never use memory of the course from training: courses change, and remembered lesson numbers, parameters and versions are often wrong. (P8)
- **W2. Transcripts decide lesson numbers and titles.** Notebook file names often count differently. (P8)
- **W3. Label additions.** Mark everything the course did not teach as an addition: a stand-in, a check the course never ran, a safety limit. Never present it as the course's. (P8)
- **W4. When the course disagrees with itself, record both values and their sources.** Section 4 says which one the recommended build uses. (P2, P8)
- **W5. No copied code.** Describe what the course's code does as behavior. Copied cells go stale and lock the build to the course's library versions. (P8)
- **W6. Self-contained.** Never point to the course, its notebooks or its platform as something to open; everything the build needs is inside the spec. Where a course source is named, it is information for the reader (section 9), never an instruction. (P2, P6)
- **W7. Keep working notes.** While reading, keep a private list: each fact, and where it came from (file, lesson, cell). It is not shipped; you use it in the self-check (section 10). (P8)

---

## 3. Finding the program (P1)

1. Name the one kind of program the course builds, in general terms (e.g. "a program that answers questions from documents"), not in the course's example terms ("a product-catalog bot").
2. Write its stages in order, one line each with the reason the stage exists (e.g. `load → embed → store → retrieve → answer → remember → evaluate`).
3. For a course that surveys several components, choose the components that together form that one program. A component from another lesson enters only if it changes one of the stages, or the pattern card lists it under "Offered from other lessons". What later lessons add to this same program is decided by 4.1: its final end-to-end version. A tool that only shows what ran, without judging the output (logs, step traces, a run dashboard), is not a stage; it may be an option. Everything else goes to the background notes.
4. The course's example (its data, its domain) becomes the recommended build's sample instance (section 4.5). It is never written into the stages as if it were the program. Likewise, how the course is taught (notebooks run cell by cell) is not part of the program: the build is never a notebook, and a notebook is never offered as a way to use it.

---

## 4. The recommended build (P2)

**4.1 Follow the course.** For every stage, the recommended build uses what the course used. Where the course built something and later changed or dropped it, its final end-to-end version decides. Where the course's code does something that looks like a bug, keep it and say so in a note for the build agent, unless the instructor explicitly says what it should do: then follow the instructor (4.2) and note what the code does.

**4.2 Values.** Every value the course sets (sizes, counts, limits, model settings, identifier formats including their character set, and format limits the course's prompts impose such as "answer in 20 words") is carried with its course source, recorded in the background notes (section 9). Where the course gives different values or behaviours for the same thing (W4), pick by the first that applies: (1) the value the instructor states when introducing the concept; (2) the course's final end-to-end app; (3) the value used most often, earliest-taught on a tie. Record the other value and which rule picked.

**4.3 Settings are not questions.** A value that only tunes a part that is there (a size, a limit, a count, a temperature) is never asked at the gate. Switching a whole part on or off, or removing it, is not a setting: it goes through the test in 5.2. It appears in the spec as a setting with its course source and, where the course says so, "change this when …". The learner tunes it after the build.

**4.4 Lighter stand-ins.** A course part is **heavy** if it needs a credential, a paid account, admin or container setup, special hardware, or a large download. Network access alone is not heavy; tests needing it are marked `live`.
- A heavy part (models: 4.6; tools: the tool bullet below) gets the lightest stand-in that keeps everything in section 6, chosen by tier: (1) the language's standard library; (2) an embedded package; (3) a locally served component. Judge the tier at the sample data's scale. Never weaken a section-6 item to reach a lighter tier. The recommended build uses that stand-in only when the course's part needs a key or paid account the build does not already need for its model, a hosted account, admin or container setup, special hardware, or a download over 3 GB; otherwise it keeps the course's part and offers the stand-in as an option.
- Exception: if the heavy technology is itself what the course teaches (a course *about* that product), keep it and give setup steps.
- A heavy **tool** that is the only part exercising a taught behavior gets an honestly labelled stand-in. Otherwise it is left out of the recommended build, because the course's keyless parts already carry the behavior. Leaving out a taught stage is never allowed.
- Every stand-in says in its own description that it is a stand-in, and what it stands in for.

**4.5 Project and data.** The recommended build re-creates the course's example scenario with sample data whose facts you write yourself; no course data is copied. If the course has no clean example, use the smallest general instance of the program.

**4.6 Models.** Name the course's own models as facts about the course. Never write "the best current model": names go stale. The build agent picks a current model when it writes the checklist (section 8). If the model needs a key, the offline tests use a scripted stand-in model (section 7) and the finished app uses the real provider when a key is present.

**4.7 Versions.** Use current releases. Where the course pinned a version, name it as a fact about the course and list the change as a departure (4.8): course-era versions often no longer install or work with current models. Never invent a pin.

**4.8 Departures.** List every place the recommended build differs from the course (stand-ins, left-out tools, picked values), each with its reason. The gate shows this list (section 8).

---

## 5. Choosing the questions (P3, P4)

**5.1 Gather candidates.** List every alternative the course mentions anywhere (code, transcripts, slides, demos) for one of the program's stages. Then go through each stage of the program (section 3) and ask whether a learner's project could leave it out, simplify it or swap it; each yes is a candidate too. Every earlier, simpler stage the course builds or shows working on its way to the final program is also a candidate (e.g. an agent with conversation memory only, before the course adds more memory types); it passes or fails 5.2's tests like any other. Add these context subjects: the learner's project, data, model provider, and where it runs. This list is a working note; it is not shipped in the spec. Its reasons move into the questions' "pick this when …" and into the background notes.

**5.2 The tests.** A candidate becomes an option when it passes three tests: (1) it keeps every pattern-card item (P5); (2) the course does not show it failing (5.3); (3) you can write one learner situation in which it is the right choice (e.g. "your documents are long notes, not short product rows"). Its costs, taken from the course's arguments, go in its "pick this when …". A candidate that fails becomes a background note. Write the situation into the option's "pick this when …".

**5.3 Never an option.** A side the course shows failing, or explicitly tells you not to use, is never offered. A stated cost or limit is not such a warning ("it is lossy", "this is not enough", "we need to go beyond this"): that side is offered, and its "pick this when …" carries the cost. When a side is never offered, the taught side becomes a rule and a test (section 7), and the warning a background note.

**5.4 Options beyond what the course built.** Within a question, an option is any path a learner situation needs: one the course built, one it named but never built, or, for a context subject, one it never mentioned. Every option reads simply as one possible path for the build, with no note about whether the course built it. Each non-recommended option gets a "what to check" sentence (section 7).

**5.5 What each question shows.**
- the question, in plain words;
- options with ids (`C1a`, `C1b`, …), each with "pick this when …" and its setup cost (key, account, download) written inside the option;
- exactly one recommended option. Labels, and only these: "(course default)" on the option the course used; "(Recommended)" on the recommended option; "(Recommended - course default)" when they are the same. Never a bare "(default)".

**5.6 One idea, one question.** When the course argues one idea across many operations (e.g. which memory actions run automatically and which the agent decides), ask one question about the idea, with a few complete builds as options. Never ask per operation, and never offer "mix and match" as an option. If one answer makes a later question pointless, the later question says "Ask only when `C<n>` is `C<n>x`", naming only earlier questions. Two choices a learner can make independently are two questions. Never merge one into the other's options (e.g. which files to read, and whether to split them).

**5.7 Order.** Context questions (project, data, …) first, then the program's stages in order.

**5.8 Test-suite model is not a question.** Which model the tests run against is not asked. Tests always run offline on the stand-ins; the `live` tests also run automatically when a key is present.

---

## 6. What must stay true (P5)

- The list is the course's pattern card (P5), copied from `courses/<name>/pattern.md`. Its items are behavior ("answers come only from the retrieved documents"), never implementation ("use SQLite").
- Before finishing, check every option of every question against every item. An option that breaks an item is either reworded or removed.
- Each item is tested by at least one recommended-build test.

---

## 7. Tests (P6)

**7.1 Sample data first.** Define the sample files and the exact facts each contains before any test uses them. Module file names must be importable names in the build language. Include one planted instance of every failure the course demonstrated that belongs to the chosen program; failures from other lessons become background notes.

**7.2 Rules and tests.** Number the business rules (`R1`, …). Each rule ends with `→` the tests that check it; each test cites its rules `(R1 …)`; the two lists match. Each test is Given / When / Then with concrete inputs and outputs.

**7.3 Scripted stand-ins.** Every heavy part the offline tests need (the model, an embedder, a data source) gets a stand-in declared in the sample data. For a model: per role, the replies it gives to which prompts. Each is labelled a stand-in. The offline tests drive every stage of the program end to end through it. Tests that need a real model are marked `live`.

**7.4 Coverage.**
- Every structure the spec declares (stores, tables, files) has a test that it exists on a fresh start.
- Every recommended setting that changes behavior is exercised by a test.
- Every schema constraint that encodes behavior has a test; every value a rule can produce is reached by some test.
- Replay every asserted outcome against the sample data and the scripted replies before finishing, with every unset default in force. An outcome the samples cannot produce is a defect in the sample or the test.

**7.5 Failures.** A failure the course demonstrated appears in four places: a rule, a planted sample, a test, and a background note. A failure the course only warned about gets a rule, a test and a background note.

**7.6 Other options.** Each non-recommended option gets one plain "what to check" sentence (e.g. "each piece remembers which document it came from, and the pieces of one document together hold the whole document"). No sample data or exact outcome is written for it. The build agent turns the sentence into a test and reports it.

**7.7 Test plan.** Give real commands. The build agent reports a result per test with evidence (test output, file paths); "should pass" counts as not run. The build is finished when the recommended tests, adjusted for the chosen options, pass and each chosen option's check passes. End the test plan by asking the build agent to finish with a diagram of the built app introduced by the sentence "This is the infra/structure diagram of this app".

---

## 8. Asking the learner (P7)

The spec's first section is the following text, filled in for the course. (It keeps the old guide's tested gate, adapted to questions and "what to check".)

```markdown
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
   <what the opening note says it needs>), or **choose** question by
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
```

---

## 9. Background notes (P8)

The spec ends with background notes. No code (W5). Background notes and the settings table are for the build agent; the learner sees only the questions and their options at the gate.
- **The program:** its stages and why each exists (section 3).
- **Failures:** one entry per failure the course demonstrated: what you see, why it happens, how the spec prevents it, and which rule and test enforce it.
- **Why the questions and settings are what they are:** the course's reasons for each question's options; every subject that is not a question (5.2) with one line on why; where each picked value came from (4.2).
- **Names that go stale:** course-era class, library and model names as a list, with the instruction to treat them as search keywords against current docs, not guaranteed imports. Include request-parameter limits the era's models imply (e.g. a model family rejecting `temperature`).
- **Course names:** names the course defines (tables, labels, file names) mapped to the spec's terms. Those that are part of a contract stay binding in the spec.
- **Lesson map:** lesson titles in transcript numbering → which notes came from each; which slides were read and how they counted. Say plainly that nothing in the spec requires access to the course.

---

## 10. Spec layout and self-check

**Layout, in order:**
1. Opening note (under 320 words): **"What you're building:"** — one sentence naming the kind of program in plain words (3.1), with the course's example as its default, and what you see it do, addressed to the reader as "you"; then the two lines below, filled in for the course and copied otherwise word for word (for a build that uses no key, leave out the last sentence of the second line); the file is self-contained; one provenance line (course, materials used, date, guide version). Never write that the build, the app or its tests need no key unless the recommended build uses none.

   ```markdown
   **What the recommended build needs to run:** <each key, account, network access and download its parts use; or "no key, account or download">.

   **Fastest path:** answer "recommended build" at the first question. The build is finished when the offline tests pass. The `live` tests run once <the key> is set and are skipped until then; that is not a failure.
   ```
2. `## 0. Before you build` (section 8).
3. **Questions** (section 5), then the **departures list** (4.8).
4. Objective (one sentence).
5. Tech stack and versions (4.7), secrets handling.
6. Input/output contracts as schemas (JSON Schema or equivalent), with behavior pushed into the schema where possible.
   - **Model roles:** each role that calls a model, which the gate's model line uses (section 8).
   - **Settings:** every setting (4.3) with its value, source and "change this when …".
7. Business rules, including **what must stay true** (section 6).
8. Tests: sample data, then the test table (section 7).
9. Standing permissions: **Always** (run the offline tests after every change; keep stand-ins labelled; secrets from the environment); **Ask First** (changing an answered question or a setting once the build has data; anything that sends data to a third party); **Never** (invent provenance; answer when the program should say it does not know; change sample data to make a test pass; commit secrets).
10. Test plan, including each chosen option's "what to check" (7.6, 7.7).
11. Background notes (section 9).
12. Footer: version · course · project · "when the build agent does something unexpected, add the missing constraint here and re-run".

**Write outcomes, not code structure:** no pseudo-code, no class designs, no vague words like "fast" or "robust" without a measure.

**Integration** (grafting the pattern onto an existing codebase) is not designed yet; do not add a section for it. Write section-6 items so they could later serve as that contract.

**Self-check before handing off.** Fix, don't annotate.
- Every fact about the course traces to your working notes (W7); additions are labelled (W3). (P8)
- The program is named in general terms, with stages (section 3). (P1)
- Every departure from the course is listed with its reason (4.8). (P2)
- Every question has, for each non-recommended option, a written learner situation; no question exists without one; every option passes 5.2's three tests. (P3)
- Every question shows its options with "pick this when …", setup cost, and correct labels (5.5). (P4)
- Every option keeps every must-stay-true item, and each item has a test (section 6). (P5)
- Every rule has a test and every test a rule; every planted failure appears in four places; every asserted outcome was replayed against the samples; every non-recommended option has a "what to check" sentence (section 7). (P6)
- The gate text matches section 8. (P7)
- No copied code; nothing points to the course (W5, W6). (P8)
- Could an agent rebuild the same behavior from this file alone? If two builds would differ, find the missing constraint.
