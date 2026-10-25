# LangChain (`courses/langchain`): owner-confirmed musts

Confirmed by the owner on 2026-10-24; M6b added on 2026-10-25. They describe the v2.4 benchmark spec, the quality the owner wants. Each generation is scored on them by the blind scorer (`../scorer-prompt.md`). The block between the markers is pasted into the scorer verbatim.

<!-- MUSTS -->
The spec describes an app built from a course on LangChain (question answering over documents).

M1. The recommended build includes the quality check (evaluating the app's answers, e.g. example questions graded by a model). FAIL if evaluation is only available when the learner picks a non-recommended option, or is not offered.
M2. The quality check (evaluation) is a question of its own (not one option inside a "bring something back"/add-ons question), and that question has an option for no evaluation at all.
M3. Remembering earlier questions (conversation memory) is a question of its own whose options are the course's kinds of memory (e.g. whole conversation, last k exchanges, token limit, summary). FAIL if memory appears only as one option of an add-ons/"bring something back" question, or only as yes/no. PASS if a separate question dedicated to the kind of memory exists, even if it is asked only after the learner opts into memory elsewhere.
M4. Splitting long documents into smaller pieces is a question of its own (FAIL if splitting only appears as part of the options of another question, e.g. folded into the document-type question).
M5. Some option lets the learner use a folder of their own notes/text/Markdown files.
M6a. The recommended way to use the app is a command-line program (not a notebook). Also PASS if the interface is not asked and the spec builds a command-line program.
M6b. No option anywhere offers a notebook (Jupyter or "notebook you run cell by cell") as the way to use the app, recommended or not.
M7. No question lets the learner pick several options at once ("pick one or more", "any of ... together", multi-select). Every question is single-choice. (A question asked only conditionally is fine.)
<!-- /MUSTS -->

## Not musts (owner, 2026-10-24)
- Which embedder the recommended build uses: **deferred**. Under 4.6 the recommended build needs an API key for real answers, while P2 lists "a paid API key" as needing a stand-in.
- Free: the embedder as its own question; the exact document types (if M5 holds); a vector-database-server option; offering the hosted tracing platform; the number of questions.

## Baseline on guide v2.4 (Opus 5.5, blind-scored, 2026-10-25)
Misses are counted over M1–M7, using M6a. M6b is counted separately.

| Runs | Misses per run | M6b fails (notebook offered) |
|---|---|---|
| 8 exact copies of the main-session input | 0, 2, 0, 0, 1, 0, 2, 1 | 8 of 8 |
| 8 exact copies of the separate-session input | 0, 1, 0, 2, 1, 1, 0, 1 | 6 of 8 |
| 4 runs from the owner's fresh session | 1, 0, 0, 0 | 4 of 4 |

Where the 16 copies missed: M4 ×4, M6a ×3, M1 ×2, M2, M3, M7 ×1 each. Two earlier runs (10-24) missed 5 and 4; exact re-runs of their input did not repeat it.
