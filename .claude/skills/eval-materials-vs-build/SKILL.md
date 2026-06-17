---
name: eval-materials-vs-build
description: >
  Scores how faithfully a recorded build run aligned with the course
  materials, in the spec-build-eval-lab. Use this skill ANY time the user
  asks to evaluate, score, check, judge, or compare a specific build run
  AGAINST THE COURSE — including phrasings like "evaluate run-02 against
  the materials", "score run-02 against the course", "is run-02 faithful
  to the course", "did the build match the course", "course alignment
  check on run-NN", "how does run-02 compare to the notebooks and
  transcripts", "is the build aligned with what the course taught",
  "run a materials-vs-build eval", or "/eval-materials-vs-build run-NN".
  Reads materials/notebooks/, materials/transcripts/, and builds/<run>/,
  then writes evals/<run>/materials-vs-build.md. Requires an explicit
  run-NN; if none is given, list the runs in builds/ and ASK which one —
  never default. Do NOT use this skill to evaluate against spec.md —
  that's /eval-spec-vs-build, a different reference and different
  question.
argument-hint: <run-NN>
allowed-tools: [Read, Write, Glob, Grep, Bash]
---

# eval-materials-vs-build

Compare a recorded run's app against the original course materials.
**Course alignment only.** Spec fidelity is `/eval-spec-vs-build`.

## Steps

1. **Verify cwd is a course folder.** Confirm `spec.md`, `materials/`,
   `builds/`, `evals/` exist. Refuse otherwise.
2. **Require a run.** If `$ARGUMENTS` is empty:
   ```bash
   ls -1 builds/ 2>/dev/null | grep -E '^run-[0-9]+$' | sort
   ```
   List those runs and ask which one. Never default.
3. **Validate the run.** Confirm `builds/$ARGUMENTS/` is a non-empty
   directory. Refuse otherwise. The report reflects whatever the build
   folder contains — evaluating an in-progress run is fine; just re-run
   after the build finishes for a clean score.
4. **Read the inputs.**
   - Materials: every non-empty file under `materials/notebooks/` and
     `materials/transcripts/`.
   - Build: walk `builds/$ARGUMENTS/` (skip node_modules, .venv, dist,
     build, .git, and anything matching its own .gitignore).
5. **Produce the report at `evals/$ARGUMENTS/materials-vs-build.md`** with
   sections:
   - **Summary** — one-paragraph verdict on course faithfulness.
   - **Concept coverage** — concepts/techniques the materials taught →
     present / partial / missing in the build, with file references.
   - **Divergences from the course** — what the build did that the
     materials never covered (this can be fine, but call it out).
   - **Course concepts skipped** — what the course emphasized that the
     build ignored.
   - **Score** — judgment on a 0–10 scale, with reasoning.
6. **Report the path written.**

## Don't

- Don't read `evals/$ARGUMENTS/spec.md` or the top-level `spec.md` — that
  collapses this eval into `/eval-spec-vs-build`. Different reference,
  different question.
- Don't default a run. List the runs in `builds/` and ask the user
  which one.
- Don't penalize the build for not implementing something the materials
  didn't actually cover — that belongs in the spec eval.
