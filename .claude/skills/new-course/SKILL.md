---
name: new-course
description: >
  Adds a new course to the spec-build-eval-lab. Use this skill ANY time the
  user wants to register, scaffold, set up, add, create, init, or start
  tracking a NAMED COURSE in this repo — including phrasings like
  "scaffold a new course called X", "set up a course folder for X",
  "make a new course called X", "add the X course", "init the X course",
  "let's start tracking the X course", "I want to add a new course",
  "/new-course X", or any user message naming a course they want to begin.
  This skill copies templates/course/ to courses/<name>/ and nothing else;
  it does NOT read materials, write spec.md, or run a build. If the user
  asks anything about an EXISTING course, do NOT use this skill. Always
  run from the repo root.
argument-hint: <course-name>
allowed-tools: [Bash, Read]
---

# new-course

Scaffold `courses/<name>/` from `templates/course/`. This skill ONLY copies
the template; it does not read materials and does not generate `spec.md`.

## Steps

1. **Verify cwd is the repo root.** Confirm both paths exist relative to cwd:
   - `templates/course/`
   - `.claude/skills/new-course/`
   If either is missing, refuse with: "Run /new-course from the repo root —
   the folder containing templates/ and .claude/." Stop.
2. **Require the course name.** If `$ARGUMENTS` is empty (or the user did not
   provide a name in their message), ask: "What should the course be called?
   It becomes the folder name under courses/." Stop until they answer.
3. **Refuse on collision.** If `courses/$ARGUMENTS/` exists, refuse with:
   "courses/$ARGUMENTS/ already exists. Pick a different name or remove the
   existing folder first." Stop.
4. **Copy the template:**
   ```bash
   cp -R templates/course/ "courses/$ARGUMENTS/"
   ```
5. **Report and hand off.** Tell the user, verbatim style:
   "Scaffolded courses/$ARGUMENTS/. Drop notebooks into
   courses/$ARGUMENTS/materials/notebooks/ and transcripts into
   courses/$ARGUMENTS/materials/transcripts/, then `cd courses/$ARGUMENTS`
   and run /generate-spec."

## Don't

- Don't read or write `materials/`, `spec.md`, `builds/`, or `evals/`.
- Don't `cd` for the user — they choose when to move into the course folder.
- Don't run from inside an existing course folder. The session is anchored
  at the repo root.
