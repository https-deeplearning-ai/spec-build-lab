---
name: eval-spec-vs-build
description: >
  Scores how faithfully a recorded build run followed its spec.md, in the
  spec-build-lab. Use this skill ANY time the user asks to evaluate,
  score, check, judge, assess, or compare a specific build run AGAINST
  THE SPEC — including phrasings like "evaluate run-02 against the spec",
  "score run-02 against the spec", "did the build follow the spec",
  "did run-02 implement the spec", "spec fidelity check on run-NN",
  "how closely did run-02 follow spec.md", "run a spec-vs-build eval",
  "evaluate the spec adherence of the latest run", or
  "/eval-spec-vs-build run-NN". Reads the per-run snapshot
  evals/<run>/spec.md (NOT the live spec.md) and the contents of
  builds/<run>/, then writes evals/<run>/spec-vs-build.md. Requires an
  explicit run-NN; if none is given, list the runs in builds/ and ASK
  which one — never default. Do NOT use this skill to evaluate against
  course materials — that's /eval-materials-vs-build, a different
  reference and different question.
argument-hint: <run-NN>
allowed-tools: [Read, Write, Glob, Grep, Bash]
---

# eval-spec-vs-build

Compare a recorded run's app against the spec snapshot it was built from.
**Spec fidelity only.** Course alignment is `/eval-materials-vs-build`.

## Steps

1. **Verify cwd is a course folder.** Confirm `spec.md`, `materials/`,
   `builds/`, `evals/` exist. Refuse otherwise: "Run /eval-spec-vs-build
   from inside a course folder."
2. **Require a run.** If `$ARGUMENTS` is empty:
   ```bash
   ls -1 builds/ 2>/dev/null | grep -E '^run-[0-9]+$' | sort
   ```
   List those runs and ask the user: "Which run should I evaluate?
   Pick one — I won't default to the latest." Stop until they answer.
3. **Validate the run.** Confirm `evals/$ARGUMENTS/spec.md` (the snapshot)
   exists and `builds/$ARGUMENTS/` is a non-empty directory. Refuse
   otherwise. The report reflects whatever the build folder contains —
   evaluating an in-progress run is fine; just re-run after the build
   finishes for a clean score.
4. **Read the inputs.**
   - Snapshot spec: `evals/$ARGUMENTS/spec.md` (NOT the top-level
     `spec.md` — that may have been regenerated since this run).
   - Build: walk `builds/$ARGUMENTS/` (skip node_modules, .venv, dist,
     build, .git, and anything matching its own .gitignore).
5. **Produce the report at `evals/$ARGUMENTS/spec-vs-build.md`** with
   sections:
   - **Summary** — one-paragraph verdict.
   - **Coverage matrix** — each spec section → present / partial / missing,
     with file references into `builds/$ARGUMENTS/`.
   - **Divergences** — things the build did that the spec did not specify.
   - **Missing** — things the spec specified that the build did not do.
   - **Score** — your judgment on a 0–10 scale, with reasoning.
6. **Report the path written, then hand off.** After echoing the report
   path, tell the user: "Spec-fidelity report written. The companion
   eval is /eval-materials-vs-build $ARGUMENTS — different reference,
   different question (course alignment, not spec fidelity). Say 'go
   ahead' to run it next, or skip if you've already done it."

## Don't

- Don't read `materials/` — that's the *other* eval. Mixing them defeats
  the point of having two.
- Don't read the top-level `spec.md` — always the per-run snapshot.
- Don't pick a default run. List the runs in `builds/` and ask the user
  which one.
