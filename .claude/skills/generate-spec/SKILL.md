---
name: generate-spec
description: >
  Produces spec.md for a course in the spec-build-lab by reading the
  course's materials and writing a build-ready specification. Use this skill
  ANY time the user asks to generate, write, produce, build, regenerate,
  create, or run the spec for a course — including phrasings like
  "generate the spec", "write spec.md", "produce spec.md", "make a spec
  from this course", "turn the materials into a spec", "build the spec
  out of materials/", "regenerate spec.md", "run the spec generation",
  "I've added the notebooks, please create the spec", or "/generate-spec".
  Reads every file under materials/notebooks/ and materials/transcripts/
  and follows references/spec-generation-guide.md. Writes spec.md in the
  current working directory. Must run from inside a course folder
  (courses/<name>/). Do NOT use this skill for editing an existing
  spec.md or for writing product specs unrelated to a course.
  Pass --env=<slug> to generate for a known build environment instead of
  the agnostic learner takeaway (e.g. "/generate-spec --env=coding-agent-lab",
  "generate the lab version of the spec").
argument-hint: "[--env=<slug>]"
allowed-tools: [Read, Write, Glob, Grep, Bash]
---

# generate-spec

Turn `materials/notebooks/` + `materials/transcripts/` into a `spec.md` that
another engineer (or coding agent) can implement end-to-end.

## Steps

0. **Parse `--env=<slug>`, if given.** Pass it only if the user supplied one —
   never synthesize a slug. With a slug, resolve
   `.claude/skills/generate-spec/references/spec-generation-guide.<slug>.md`
   relative to `$CLAUDE_PROJECT_DIR`. If that file does not exist, refuse with
   "No environment overlay named `<slug>`." plus the list of
   `spec-generation-guide.*.md` overlays that do exist. Stop. Without a flag,
   every step below runs exactly as written and the output is `spec.md`.

1. **Verify cwd is a course folder.** Confirm all of these exist relative to
   cwd: `materials/notebooks/`, `materials/transcripts/`, `builds/`,
   `evals/`. If any are missing, refuse with: "Run /generate-spec from
   inside a course folder — `cd courses/<name>` first." Stop.
2. **Read the guide.** Read
   `.claude/skills/generate-spec/references/spec-generation-guide.md`
   relative to `$CLAUDE_PROJECT_DIR` (anchor on the repo root, not cwd).

   Follow it fully — it is the prescriptive contract for the spec's
   content, structure, and quality. Do not restate or summarize its rules
   here; defer to the guide so the two files can't drift.

   **With `--env=<slug>`:** after reading the base guide in full, also read the
   overlay resolved in step 0, and follow its precedence rules. The base guide
   is never edited for an environment; the overlay declares what it overrides.
3. **Read every material.** Glob `materials/notebooks/**/*` and
   `materials/transcripts/**/*`, then read each non-empty file. If both
   directories are empty (only `.gitkeep`), refuse with: "No materials
   found. Add notebooks to materials/notebooks/ and transcripts to
   materials/transcripts/, then re-run — or optionally run
   /ingest-course-repo <course-folder-URL> to add the course repo's
   notebooks and helper.py on top." Stop.
4. **Write spec.md.** Produce a self-contained build-ready spec at
   `./spec.md` in cwd (overwrite if it exists — this is regeneration, not
   editing). **With `--env=<slug>`, write `./spec.<slug>.md` instead**, leaving
   any existing `spec.md` alone — the two are siblings, and their diff is what
   shows the environment's effect. What the spec must contain and how it
   handles learner input are governed entirely by the guide — don't duplicate
   those rules here.
   The spec should end with a section telling the builder to
   conclude with an infra/structure diagram and the phrase
   "This is the infra/structure diagram of this app" — `/extract-build-log`
   uses that phrase as its default closing bookend when slicing the
   conversation. It's a UX hint, not a system requirement (the slice can
   also be controlled with `--until="<phrase>"`, and falls back to
   end-of-transcript if no closing match is found).
5. **Report.** Tell the user the path written and that they can review,
   then run /prepare-build when ready.

   **With `--env=<slug>`:** also print the overlay's Environment Resolutions —
   every one of the six learner-context dimensions with its resolution — so the
   removals are visible rather than implied, and remind the user that
   /prepare-build needs the same `--env=<slug>`.

   **Without a flag:** if the course already contains a `spec.<slug>.md`, say so
   and name the flag that regenerates it. Otherwise a course with an environment
   variant silently gets only its agnostic spec refreshed.

## Don't

- Don't write to `builds/`, `evals/`, or `materials/`.
- Don't pull in external knowledge to fill gaps in the materials —
  faithfulness to the course IS what /eval-materials-vs-build measures
  later.
- Don't stop short of the infra-diagram section — it's the default
  closing bookend `/extract-build-log` looks for; omitting it forces the
  log slice to extend to end-of-transcript.
