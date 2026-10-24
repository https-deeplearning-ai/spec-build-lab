---
name: generate-spec-v2
description: >
  Produces the course-agnostic spec.md for a course in the spec-build-lab,
  using guide v2 in a clean room: an owner-confirmed pattern card first, then
  an isolated generator agent, then a new branch and pull request. Use this
  skill ANY time the user asks to generate, write, produce, regenerate or
  create the spec for a course WITHOUT an --env flag, including "generate
  the spec", "write spec.md", "regenerate spec.md", "make a spec from this
  course" or "/generate-spec-v2". Must run from inside a course folder
  (courses/<name>/). For an environment spec (--env=<slug>) use
  generate-spec instead. Do NOT use this skill to edit an existing spec.md
  or to change the guide.
allowed-tools: [Read, Write, Glob, Grep, Bash, AskUserQuestion]
---

# generate-spec-v2

Writes `courses/<name>/spec.md` from the course materials with guide v2.4
(`references/guide.md`). It is the same process the guide was validated with
(clean-room generation, then builds, on three courses, 2026-10-23/24):
1. the pattern card, confirmed by the owner;
2. one clean-room generator;
3. the spec it writes, unedited, on a new pull request.

Running it again on a course is how a spec is iterated: reconfirm or revise
the card, then regenerate.

## Files

| File | Read by |
|---|---|
| `references/guide.md` | the clean-room agents only, never the session running this skill |
| `references/card-prompt.md` | the card-proposal agent (step 3a) |
| `references/generation-prompt.md` | the generator agent (step 4) |
| `courses/<name>/pattern.md` | the generator agent, and the owner at step 3 |
| `scripts/run_clean.sh` | this session, to start both agents |

## The empty folder

Both agents run through `scripts/run_clean.sh`, never through the Agent tool.
An agent started inside the repo gets this session's CLAUDE.md, memory index,
git status and skill list attached automatically, and that context differs by
session. On LangChain (2026-10-24/25), four specs generated that way from a
separate session missed 12 of the owner's required properties in total; four
generated through this script from a separate session missed 3.

The script makes an empty temporary folder outside any repo, copies in the
guide, the materials (never `materials/repo/`) and, for generation, the card,
fills the prompt's slots with those copies, and runs `claude -p` there. It
copies the agent's output back and prints the agent's final report. The
prompt is sent exactly as it is; add nothing to it.

A run takes about 10 minutes, longer than the shell's foreground limit: run
the script in the background and wait for it to finish.

## Steps

1. **Check the folder.** Confirm that `materials/notebooks/` and
   `materials/transcripts/` exist in the current folder. If not, refuse:
   "Run /generate-spec-v2 from inside a course folder — `cd courses/<name>`
   first." If `--env` was passed, refuse: "Environment specs use
   /generate-spec --env=<slug>." Check with `ls` that materials exist; do not
   read them yet.

2. **Ask which model runs the clean-room agents.** Ask every time, with no
   default. Use the structured question tool if there is one. Options: opus,
   sonnet, fable, haiku. The answer is used for both step 3a and step 4. Say
   once that the guide was validated with opus only.

3. **The pattern card.** The owner confirms it before every generation. An
   unconfirmed card is never used, because a stale card passes its errors
   into the spec.

   a. **No `pattern.md` yet:** from the course folder, run
      `bash <skill>/scripts/run_clean.sh card . <model> pattern-proposed.md`.
      The agent writes a proposed card and stops.

   b. **Check every quote.** For each quote, in the proposal or in an existing
      `pattern.md`, grep `materials/` and confirm it is there and says what
      the item claims. A generator's reading of the course is a claim, not
      evidence. Report any quote that is missing or reads differently.

   c. **The owner decides each item, one at a time.** Show the item, its
      quotes, and whether the check in 3b passed.
      - You may suggest dropping or rewording an item, with the reason.
      - The card holds only the essence: what every build must keep, whatever
        the learner picks. A feature of the full program stays a rule of the
        recommended build, not a card item.
      - An item that would block an option the course does not show failing
        belongs off the card.
      - The owner's answer decides. With an existing `pattern.md`, the owner
        keeps, rewords or drops each item.

   d. **Write `pattern.md`.** The first lines, in italics, record:
      - the date it was confirmed;
      - how it was drafted (agent and model);
      - each change, each marked "suggested by Claude (the orchestrator) and
        accepted by the owner" or "the owner's own edit".

      On a reconfirmation, add that day's date and any changes. Keep the
      format of the card itself:
      - the line "**The one kind of program:** …";
      - "## What every build keeps";
      - numbered items, each with its quotes.

4. **Generate.** From the course folder, run
   `bash <skill>/scripts/run_clean.sh generate . <model> spec-v2-draft.md`.
   Git ignores that name, so a failed run leaves nothing tracked.
   - The agent reads only the guide, the card and the materials, writes the
     spec, and runs the guide's section 10 self-check itself.
   - Do not audit, check or edit the spec afterwards. The guide was validated
     on unedited generations.

5. **Open the pull request.** A rewrite of `spec.md` always goes on a new
   branch and a new pull request, never into an existing branch.

   ```bash
   git fetch origin main
   git worktree add -b spec/<name>-v2-<YYYYMMDD> <tmp-dir> origin/main
   cp spec-v2-draft.md <tmp-dir>/courses/<name>/spec.md
   cp pattern.md <tmp-dir>/courses/<name>/pattern.md
   ```

   - Commit both files and push.
   - Open the pull request with `gh pr create`. The body names the model, the
     card's confirmation date and the guide version.
   - Remove the worktree.
   - If `courses/<name>/materials/` is not on `main` yet, stop and ask the
     owner which base branch to use.

6. **Report.** Give the owner:
   - the pull request link and the model used;
   - the generator's final report in full, unfiltered: the program and its
     stages, every question with its options, every candidate turned into a
     background note and why, and every place the guide or the card was
     unclear.

   Places where the guide was unclear are findings about the guide. List
   them; never change the guide here.

## Don't

- Don't read `references/guide.md` into this session or summarize it to the
  agents. They read it themselves.
- Don't let the agents read anything beyond what their prompt allows: no
  other spec, no `builds/`, `evals/`, `experiments/` or `docs/`, no git.
- Don't edit the generated spec. A problem in it is a finding for the owner,
  fixed through the card or the guide and then a regeneration.
- Don't change `references/guide.md` or either prompt from this skill.
