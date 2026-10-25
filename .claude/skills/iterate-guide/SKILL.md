---
name: iterate-guide
description: >
  Changes the spec-generation guide used by generate-spec-v2
  (.claude/skills/generate-spec-v2/references/guide.md), its generation or
  card prompt, or the owner decision register, under the owner's
  guide-change principle: every change names its reason, is decided by the
  owner one item at a time, and is tested on several blind-scored clean-room
  generations before it lands on a PR. Use this skill ANY time the user asks
  to change, fix, iterate, extend or version the guide, or to turn a spec
  problem into a guide rule, including "change the guide", "fix this in the
  guide", "add a rule", "the guide should say…", "guide v2.5" or
  "/iterate-guide". Do NOT use it to generate a spec (generate-spec-v2), for
  an environment overlay (generate-spec --env), or to hand-edit a spec.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion]
---

# iterate-guide

Changes guide v2 (`.claude/skills/generate-spec-v2/references/guide.md`) the
way the owner agreed: a change has a reason, the owner decides it, and specs
made with it are shown better before it lands.

## Files

| File | Read by |
|---|---|
| `.claude/skills/generate-spec-v2/references/guide.md` | generators; this session when changing it |
| `references/owner-decisions.md` | this session only, never a generator. Every owner decision the guide carries. |
| `references/scorer-prompt.md`, `scripts/score.sh` | the blind scorer, which takes a round's musts file as input |

None of this goes into CLAUDE.md, AGENTS.md or any file a generator or build
agent reads.

Every file here, like everything under `.claude/`, stays course-agnostic. A
build agent can read any of them, and CLAUDE.md forbids course content in
documents a build agent can read. Course-specific test data (a course's
musts, its scores, examples from its specs) lives in the round's notes
outside the repo, never in this skill.

## The principle

1. **Every change names its reason:** a purpose clause (P1–P8), a problem
   seen in a real build or with a real learner, or the owner's reading. Two
   generated specs disagreeing is not a reason on its own. (Guide §1, "How
   this guide may change".)
2. **One rule per change,** in words the owner understands. Present the
   decision and wait for the owner's go. Change only what the owner asked.
3. **No stacking.** Before writing, grep the whole guide for every sentence
   on the subject. Fix the sentence that misleads in place; prefer editing
   or removing over adding a new rule on top.
4. **Check claims in the materials.** What a generator says the course
   shows, warns or fails is a claim until it is quoted from `materials/`.
5. **Keep the register.** Every change updates `references/owner-decisions.md`.
   No row is removed. A change that overrides a row needs the owner's
   explicit decision, recorded as a new row naming the row it overrides and
   why.
6. **"Better" is decided by builds and the owner's reading,** never by text
   checks alone. A change that affects what the recommended build includes
   or how it runs needs at least one build.
7. **Several runs per arm, scored blind.** Never compare 4 runs with 4: one
   input gave 4, 2 and 0 misses on the same day. Score against the course's
   musts with `scripts/score.sh`. Comparing setups means diffing the
   generators' logged inputs, not assuming them.
8. **Predict before running.** Write each arm's predicted outcome down
   before the runs, and compare afterwards.
9. **Report every generator note to the owner, unfiltered.** Where the
   guide was unclear is a finding about the guide.
10. **Nothing course-specific in agent-readable files.** No course name,
    course content, musts or scores in the guide, the prompts, this skill,
    the register, CLAUDE.md or AGENTS.md. The guide speaks in general terms;
    course examples stay in the round's notes.
11. **Only what was agreed.** Before committing, list every file the change
    adds or touches beyond what the owner agreed, and get the owner's go on
    each.

## Steps

1. **List the items.** One line each: what fails, in which runs (with a
   quote from the spec), and which must and purpose clause it concerns.
   Agree the order with the owner, and put first any item that pulls other
   misses after it.

2. **One item at a time:**
   a. Grep the guide for every sentence on the subject and quote them.
      Name the sentence(s) causing the failure, or the contradiction
      between two sentences.
   b. Propose the smallest fix as an exact before/after, with its reason
      (rule 1), the register rows it touches, and the word count change.
      Name any row it overrides (rule 5).
   c. The owner decides: **(a)** change the guide; **(b)** room, the
      builder handles it, recorded only; **(c)** not a guide problem.
      Wait for the answer before the next item.

3. **Test the accepted changes together, in one round.** Each change
   targets a different must, and the scorer scores each must separately.
   - Make the changes on a new branch, in a worktree from `origin/main`.
     Bump the version in guide line 3, in the provenance line of
     `generate-spec-v2/references/generation-prompt.md`, and in the
     version named in `generate-spec-v2/SKILL.md`.
   - Ask the owner which model runs the generators, and have the owner
     reconfirm each course's pattern card (register row 24).
   - **Agree the musts with the owner** for each test course: the
     properties its spec must have, each written so a reader can mark it
     PASS or FAIL, with an id (M1, M2, …). Start from the previous round's
     notes if there are any, and have the owner confirm them item by item,
     as with the card. Write them into the round's notes file, outside the
     repo, between the lines `<!-- MUSTS -->` and `<!-- /MUSTS -->`, after
     one sentence naming what the app is. Keep the baseline scores (the
     current guide's runs) in the same notes.
   - Write predictions (rule 8).
   - Generate with `generate-spec-v2/references/generation-prompt.md`, its
     slots filled: `{GUIDE}` = the changed guide in the worktree,
     `{COURSE_DIR}` = the course folder, `{OUT}` = a scratch file. Use a
     fresh general-purpose subagent (never a fork) for each run, and send
     the prompt unchanged. At least 8 runs on each course with agreed musts,
     and 2 on each other benchmark course for the owner's reading. Run the
     baseline arm (the current guide) the same way if the notes have no
     baseline yet.
   - Score each spec with
     `scripts/score.sh <round notes with musts> <spec> <out.json>`, and
     compare with the baseline.
   - Show the owner the scores, the specs' question lists and every
     generator note. Run builds where rule 6 asks for them.

4. **Land it.** If the owner accepts:
   - one PR, one commit per rule;
   - add register rows (or new status) for each change;
   - record the round's scores in the round's notes as the next baseline.

   **Before committing,** for every file the PR adds or changes:
   - table who **can** read it (generators, build agents, eval agents, any
     session), not only who is meant to;
   - check it against CLAUDE.md's constraints, above all "documents a
     build agent reads stay course-agnostic";
   - grep the diff for every course folder name
     (`git ls-tree -d --name-only origin/main courses/`); a hit under
     `.claude/`, CLAUDE.md or AGENTS.md blocks the commit;
   - list any file beyond what the owner agreed (rule 11).

   The PR body carries this checklist:
   - [ ] each changed sentence names its purpose clause or evidence;
   - [ ] word count before → after;
   - [ ] register updated; overridden rows named;
   - [ ] runs per course, scores against the baseline, predictions against
     results;
   - [ ] builds run, or why none were needed;
   - [ ] generator notes reported to the owner;
   - [ ] who-can-read table done; no course names or content in
     agent-readable files; no file beyond what the owner agreed.

   Specs already generated are not regenerated here. That is
   `generate-spec-v2`, run by the owner per course.

## Don't

- Don't change the guide, the prompts or the register without the owner's
  go on that item.
- Don't add a rule because two runs disagreed, or because an audit counted
  something.
- Don't let a generator read the register, the musts or the scores.
- Don't store a course's musts, scores or examples anywhere under `.claude/`.
- Don't edit a spec to make a must pass. A spec problem is fixed through
  the card or the guide, then a regeneration.
