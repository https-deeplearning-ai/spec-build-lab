# CLAUDE.md — spec-build-eval-lab

Project memory for the coding agent working in this repo. The human-facing
overview is in `README.md`; this file holds the procedural detail.

## What this repo is
A loop run once per course: course materials → build-ready `spec.md` → a recorded
build → two evals → iterate. The goal is to test whether course materials yield
specs that produce apps which (a) follow the spec and (b) stay faithful to the
course.

## Where to work (one session, moving cwd)
Launch the session once at the repo root and stay there. Within this one session
your working directory moves:

- repo root → `/new-course`.
- `courses/<name>/` → `/generate-spec`, `/prepare-build`,
  `/extract-build-log`, `/eval-spec-vs-build`, `/eval-materials-vs-build`. `cd`
  here before running them; they act on the current course. Relative paths below
  are from this folder.
- `courses/<name>/builds/run-NN/` → the actual app development (install deps, run
  services, optional app-level `git init`). `cd` here to build.

Completing a build in the **same session that started it** keeps the breadcrumb
at `evals/run-NN/.session` accurate; `/extract-build-log` reads that breadcrumb
to find the right transcript. Cross-session continuation is possible but not yet
supported automatically — see "Building" below.

## Skills (invoke with `/name`)
- `/new-course <name>` — run from the repo root. Copies `templates/course/` to
  `courses/<name>/`. Does NOT generate the spec.
- `/generate-spec` — reads `materials/notebooks/` and `materials/transcripts/`,
  follows `.claude/skills/generate-spec/references/spec-generation-guide.md`, and
  writes `spec.md`.
- `/prepare-build` — the expected, explicit way to start a build run; allocates
  the run and drops a session breadcrumb at `evals/run-NN/.session` (see below).
  It will also fire on its own if the user just starts building against `spec.md`,
  but treat the explicit call as the norm.
- `/extract-build-log <run-NN>` — slices the build conversation out of Claude
  Code's session transcript and writes `evals/run-NN/session-log.md`. Run when
  the build is in a state worth capturing. Re-runnable with different bookends
  via `--until="<phrase>"`.
- `/eval-spec-vs-build <run-NN>` — compares the per-run spec snapshot
  `evals/run-NN/spec.md` against `builds/run-NN/`; writes
  `evals/run-NN/spec-vs-build.md`. **Spec fidelity only.** Requires a `run-NN`.
- `/eval-materials-vs-build <run-NN>` — compares `materials/` against
  `builds/run-NN/`; writes `evals/run-NN/materials-vs-build.md`. **Course alignment
  only.** Requires a `run-NN`.

If the user runs either eval without naming a run, do NOT guess and do NOT pick the
latest — list the runs in `builds/` and ask which one.

Do not swap the two evals: spec-vs-build asks "did it follow `spec.md`",
materials-vs-build asks "is it faithful to the course". Different reference,
different question.

Recording is **post-hoc**: Claude Code already writes every turn into
`~/.claude/projects/<slug>/<session>.jsonl`, and `/extract-build-log` slices that
transcript on demand. There is no `Stop` hook, no `.active-run` pointer, no
`build-complete` marker. Skipping `/extract-build-log` means the conversation is
still preserved in Claude Code's transcript directory; the eval skills judge the
**built artifact**, not the conversation, so they don't depend on the log.

## Materials are off-limits during a build (load-bearing)
While `cwd` is inside `courses/<name>/builds/run-NN/`, the build agent must read
**only** `spec.md` (the working copy in the build folder, or its snapshot at
`evals/run-NN/spec.md`) and the build folder's own contents. **Do not** read
`../materials/`, `../../courses/<name>/materials/`, or any course materials.

The two-eval design depends on this. `/eval-spec-vs-build` asks "did the build
follow `spec.md`?", `/eval-materials-vs-build` asks "is the build faithful to
the course?". If the agent saw the materials during the build, the second eval
measures the agent's recall, not the spec's fidelity — the experiment collapses
silently.

Three layers reinforce this beyond the rule itself:
- `/prepare-build` copies `spec.md` into `builds/run-NN/`, so the build
  folder is self-sufficient and the agent has no reason to navigate up.
- A stateless `PreToolUse` hook (`.claude/hooks/no-materials-during-build.sh`)
  blocks any tool call from inside a `builds/run-*/` cwd whose target path
  matches `materials/`. The agent literally cannot read materials there.
- `/extract-build-log` scans the recorded transcript afterwards and surfaces a
  "WARNING: N reads touched materials/" header in `session-log.md` if the hook
  was somehow bypassed. Contamination is recorded, not silent.

**Writing constraint**: any document the build agent reads (this CLAUDE.md, every
SKILL.md) must stay course-agnostic. Mentioning the path pattern `materials/` for
the prohibition is safe — that's meta-knowledge about the experiment, not course
content. Describing what specific courses contain or teach is NOT safe — that
would leak course content into the docs themselves.

## Building — `/prepare-build` and `/extract-build-log`
- The user normally calls `/prepare-build` to begin. If they instead just start
  building against `spec.md`, treat that as the trigger too.
- **The human never creates run folders. `/prepare-build` does, as its first
  action:**
  1. Allocate the next run: scan `builds/` for the highest `run-NN`, add one
     (`run-01` if empty), zero-padded.
  2. Create `builds/run-NN/` — this folder holds the **app only**.
  3. Snapshot the spec: copy the course's `spec.md` to `evals/run-NN/spec.md`. The
     spec eval reads this frozen copy, so the run is judged against the spec it was
     actually built from even if `spec.md` is regenerated later.
  4. Drop the session breadcrumb at `evals/run-NN/.session` containing the
     absolute path to the current Claude Code transcript JSONL. Write-once,
     never updated, never read by anything except `/extract-build-log`.
  5. Announce, e.g. "Run 03 — building in `builds/run-03/`. When the build is in
     a state worth capturing, run `/extract-build-log run-03`," and `cd` into
     `builds/run-NN/` to develop the app there.
- After the build is in a satisfactory state — or any time you want a snapshot —
  run `/extract-build-log run-NN`. It reads the breadcrumb, opens the transcript
  JSONL, slices between an opening bookend (the `/prepare-build` announcement
  for this run) and a closing bookend (default: a fuzzy diagram/structure phrase;
  override with `--until="<phrase>"`; falls back to end-of-transcript if no
  closing bookend is found), and writes `evals/run-NN/session-log.md`. Idempotent
  — re-run with different bookends to re-slice.
- **Cross-session caveat:** the breadcrumb points at the transcript that existed
  at allocation time. If a build is started in session A but continued in
  session B, only session A's portion is captured. Stay in one session per build
  for now.

## Per-run layout
- `builds/run-NN/` — the built app, only. Clean; may have its own git. This repo
  gitignores `builds/`.
- `evals/run-NN/` — everything recorded or judged about the run: `.session` (the
  breadcrumb dropped at allocation, hidden), `spec.md` (the snapshot taken at
  allocation), `session-log.md` (produced by `/extract-build-log`),
  `spec-vs-build.md`, `materials-vs-build.md`.
- `evals/run-NN/` is generated to match the build. The run number is the join key
  between a build and its evaluation — keep them aligned. Evals require an explicit
  `run-NN`; if none is given, list the runs in `builds/` and ask — never default.

## Run numbering
`run-NN` is per course (`run-01`, `run-02`, …). Every new build is a new run —
even with the same `spec.md` — so runs and their evals can be compared.

## Still stubs — tune before relying on them
- `spec-generation-guide.md` — the core lever; defines what a build-ready spec
  must contain. Authored iteratively against eval feedback.
- `extract-build-log/scripts/extract.py` rendering — v1 keeps assistant tool-call
  metadata as one-line previews and suppresses tool-result outputs. Revisit if
  rendered logs feel thin once we have a real build to look at.
