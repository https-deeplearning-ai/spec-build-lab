---
name: extract-build-log
description: >
  Extracts the build conversation for a recorded run in the
  spec-build-eval-lab and writes it to evals/<run>/session-log.md. Use
  this skill ANY time the user wants to capture, save, snapshot,
  extract, export, or render the conversation for a specific build run —
  including phrasings like "extract the build log", "save the
  conversation for run-02", "snapshot run-02", "export the build log",
  "render the session log", "log this build", "produce the session log
  for run-NN", or "/extract-build-log run-NN". Reads the transcript
  recorded by Claude Code (located via the .session breadcrumb at
  evals/<run>/.session) and slices it between an opening bookend (the
  /prepare-build announcement) and a closing bookend (a fuzzy
  diagram/structure phrase by default, or a user-supplied --until
  pattern). Idempotent — re-runnable with different bookends. Requires
  an explicit run-NN; if none is given, list the runs in builds/ and
  ASK which one — never default. Do NOT use this skill to evaluate the
  run — that's /eval-spec-vs-build or /eval-materials-vs-build.
argument-hint: <run-NN> [--until="phrase"]
allowed-tools: [Read, Write, Bash, Grep]
---

# extract-build-log

Slice the build conversation out of Claude Code's session transcript and
render it as a markdown log at `evals/<run>/session-log.md`.

## Steps

1. **Verify cwd is a course folder.** Confirm `spec.md`, `materials/`,
   `builds/`, `evals/` exist. Refuse otherwise: "Run /extract-build-log
   from inside a course folder — `cd courses/<name>` first." Stop.
2. **Require a run.** If `$ARGUMENTS` (or its first whitespace-separated
   token) is empty:
   ```bash
   ls -1 builds/ 2>/dev/null | grep -E '^run-[0-9]+$' | sort
   ```
   List those runs and ask: "Which run should I extract? Pick one — I
   won't default to the latest." Stop until they answer.
3. **Validate the run.** Confirm `evals/$ARGUMENTS/.session` exists.
   Refuse otherwise: "evals/$ARGUMENTS/.session is missing — this run
   wasn't allocated by /prepare-build, so I can't locate its
   transcript." Stop.
4. **Run the extractor.** From the project root:
   ```bash
   python3 "$CLAUDE_PROJECT_DIR/.claude/skills/extract-build-log/scripts/extract.py" \
     "evals/$ARGUMENTS" \
     [--until="<user-supplied phrase>"]
   ```
   Pass `--until` only if the user gave one. The script:
   - Reads `evals/$ARGUMENTS/.session` to find the transcript
   - Slices between the opening bookend (the `/prepare-build`
     announcement matching this run number) and the closing bookend
     (`--until` regex if given, else a fuzzy default, else end of
     transcript)
   - Writes `evals/$ARGUMENTS/session-log.md` (overwrites if present —
     re-run freely with different bookends)
5. **Report.** Echo the script's stdout — it prints the path written
   plus a one-line summary of how many turns were extracted and which
   bookends were used.

## Don't

- Don't generate or judge content — this skill is a transcript slicer,
  not an analyst.
- Don't read or write to `builds/<run>/` — that's the build artifact,
  out of scope.
- Don't pick a default run. List the runs in `builds/` and ask.
- Don't fabricate a `.session` file if it's missing — that means the
  run wasn't allocated normally; refuse and ask the user to investigate.
