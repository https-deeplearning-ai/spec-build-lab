---
name: prepare-build
description: >
  Prepares a new build run for a course in the spec-build-lab —
  allocates the run folders, snapshots the spec into a frozen eval copy
  and a working copy, drops a session breadcrumb, and moves into the
  build folder. Does NOT do the building itself; that's the user +
  agent's subsequent work in builds/run-NN/. Use this skill ANY time
  the user signals intent to begin building an app from spec.md —
  including phrasings like "prepare a build", "set up a build",
  "start a new build", "begin the build", "kick off the build", "kick
  off run-02", "let's build the app", "let's build it", "build the X
  app from the spec", "implement the spec", "I'm ready, let's build",
  "let's do another build", "/prepare-build", or simply launching into
  coding work inside a course folder that has a spec.md. INVOKE
  PROACTIVELY — treat any clear build intent as the trigger. Do NOT
  use this skill to run an existing build, build a docker image, or
  build features in unrelated projects.
  Pass --env=<slug> to prepare a build from that environment's spec
  variant (spec.<slug>.md) instead of the canonical spec.md.
argument-hint: "[--env=<slug>]"
allowed-tools: [Bash, Read]
---

# prepare-build

Allocate the next `run-NN`, snapshot the spec, drop a session breadcrumb
that `/extract-build-log` will use later, and move into the build folder.
Does NOT start the build — building is the agent's subsequent work.

## Steps

0. **Parse `--env=<slug>`, if given.** Pass it only if the user supplied
   one — never synthesize a slug. It selects the *source* spec for this
   run: with a slug the source is `spec.<slug>.md`, without one it is
   `spec.md`. Call that file SOURCE_SPEC below. The slug changes nothing
   else: the snapshot and working copy are always named `spec.md`, so
   the build agent and both eval skills are unaffected.

1. **Verify cwd is a course folder.** Confirm all exist relative to cwd:
   SOURCE_SPEC (i.e. `spec.md`, or `spec.<slug>.md` with a flag),
   `builds/`, `evals/`, `materials/`. If any are missing, refuse with:
   "Run /prepare-build from inside a course folder — `cd courses/<name>`
   first." Stop. If SOURCE_SPEC is the only thing missing and a sibling
   `spec.*.md` exists, say which variants are present and name the
   `--env=<slug>` that selects one, instead of just reporting absence.
2. **Allocate the next run number.**
   ```bash
   highest=$(ls -1 builds/ 2>/dev/null | grep -E '^run-[0-9]+$' \
     | sed 's/run-//' | sort -n | tail -1)
   next=$(printf "run-%02d" $(( ${highest:-0} + 1 )))
   ```
3. **Create the run dirs and snapshot the spec.**
   ```bash
   mkdir -p "builds/$next" "evals/$next"
   cp "$SOURCE_SPEC" "evals/$next/spec.md"   # frozen snapshot, read by /eval-spec-vs-build
   cp "$SOURCE_SPEC" "builds/$next/spec.md"  # working copy, read by the build agent
   ```
   `SOURCE_SPEC` is `spec.md`, or `spec.<slug>.md` when `--env=<slug>`
   was given (step 0). **Both destinations are always named `spec.md`** —
   the filename is normalised here, which is why nothing downstream
   (the build agent, `/eval-spec-vs-build`, `/eval-materials-vs-build`)
   needs to know an environment variant was involved.
   The eval snapshot at `evals/$next/spec.md` is judged against later by
   `/eval-spec-vs-build`, so the run is judged against the spec it was
   actually built from even if `spec.md` is regenerated. The working
   copy at `builds/$next/spec.md` makes the build folder self-sufficient
   — the agent reads `./spec.md` from inside the build folder and has no
   reason to navigate back up to the course folder, where `materials/`
   sits and is forbidden.
4. **Drop the session breadcrumb.** Write the absolute path of the
   current Claude Code transcript JSONL to `evals/$next/.session`. The
   path is built from `$CLAUDE_PROJECT_DIR` and
   `$CLAUDE_CODE_SESSION_ID`:
   ```bash
   slug=$(echo "$CLAUDE_PROJECT_DIR" | sed 's:/:-:g')
   transcript="$HOME/.claude/projects/$slug/$CLAUDE_CODE_SESSION_ID.jsonl"
   echo "$transcript" > "evals/$next/.session"
   ```
   If `$CLAUDE_CODE_SESSION_ID` is unset for any reason, fall back to
   the most recently modified `*.jsonl` in
   `$HOME/.claude/projects/$slug/` and write that path. The file is
   per-run, write-once at allocation, never updated.
5. **Announce.** Say verbatim, replacing NN: "Run NN — building in
   builds/run-NN/. Read `spec.md` (in this folder) and nothing else
   from the parent course folder. When the build is in a state worth
   capturing, run `/extract-build-log run-NN` to slice the conversation
   into evals/run-NN/session-log.md."
6. **Move into the build folder.** `cd builds/$next`. From here on the
   agent develops the app inside this folder.

## Notes

- The breadcrumb at `evals/run-NN/.session` is a label on the run-NN
  folder, not coordination state. It's never updated and never read by
  any other tool — only `/extract-build-log` consumes it, and only when
  the user explicitly asks for an extract. Nothing recorder-like is
  running in the background.
- The whole conversation is already being persisted by Claude Code into
  `~/.claude/projects/<slug>/<session>.jsonl`; the breadcrumb just
  remembers which transcript to slice.

## Don't

- Don't generate or modify `spec.md` here — that's `/generate-spec`.
- Don't rename the snapshot or working copy after an `--env` run. Both
  stay `spec.md`; say in the announcement which source they came from,
  so the run's provenance is in the transcript.
- Don't ask the user for a run number — allocation is automatic.
- Don't reuse an existing run-NN folder. Every new build is a new run,
  even with the same `spec.md`, so runs and their evals can be compared.
- Don't read `../materials/`, `../../materials/`, or any course materials
  during the build. The build is a function of `spec.md` only — that's
  what the eval pipeline assumes. A `PreToolUse` hook blocks materials
  access from inside a build folder; if the hook is bypassed for any
  reason, `/extract-build-log` surfaces a contamination warning.
