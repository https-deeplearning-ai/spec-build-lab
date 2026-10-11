# Regeneration and scorer prompt templates

## Clean-room regeneration prompt

Spawn a **fresh general-purpose subagent** (never a fork — a fork inherits the
session and contaminates the clean room) on an Opus-class model (skill model
policy). Fill exactly three slots: `{COURSE}` (course directory name), `{OUT}`
(output path under `experiments/{COURSE}/<passname>/regen-<X>/spec.md`),
`{HASH}` (the committed guide hash). Change nothing else — prompt drift between
regens invalidates comparisons.

**Lab-mode variant** (`--env=<slug>`): add the overlay rules file and its
`.runtime.md` companion as permitted inputs 3 and 4, say that the overlay's own
ordering rule governs when the companion is opened, fill `{OVERLAY_HASH}`, and
change `{OUT}` to `…/regen-<X>/spec.<slug>.md`. Nothing else changes.

```
You are an isolated spec-generation agent running a clean-room experiment.
Your ONLY permitted inputs are these two, and nothing else:

1. The generation guide: <repo>/.claude/skills/generate-spec/references/spec-generation-guide.md
2. The course materials: all files under <repo>/courses/{COURSE}/materials/
   (notebooks/, transcripts/ and, when present, slides/ subfolders — never
   materials/repo/)

TASK: Read the guide completely, then read the course materials completely,
then follow the guide exactly to generate a build-ready spec. Write exactly
one output file: {OUT} (create directories as needed). Before finishing, run
  python3 <repo>/.claude/skills/generate-spec/scripts/check_spec.py {OUT}
(run it; do not read it) and fix the spec until it reports 0 findings.

HARD ISOLATION RULES — the experiment's validity depends on these:
- Do NOT read any existing spec.md anywhere in the repo (there are several;
  all are off-limits), nor anything under any courses/*/evals/,
  courses/*/builds/, experiments/, docs/, .codex/, or .agents/ directory, nor
  any CLAUDE.md, README, or skill file other than the guide named above.
- Do NOT run any git command (no log, diff, show, blame).
- Do NOT use prior knowledge of this course from training memory — the
  guide's ground-truth rule applies: only the supplied materials count as
  course evidence.
- Do NOT ask the user anything. Learner intake is a build-time input, not a
  generation input; the guide explains this.

For the spec's provenance header, the guide version is repo commit `{HASH}`
(you cannot verify this via git; use it as given).

Before writing the final file, run the guide's §14 pre-handoff checklist
yourself and fix what it catches.

FINAL REPORT (returned to me, not written to the file): (a) one paragraph on
what you generated (Ledger row count and subjects, rule/AC counts, §6 tier
contents in brief, how each course contradiction and each keyed tool was
routed, and the persistent-store realization with its tier reasoning);
(b) which §14 self-check items you fixed; (c) explicit confirmation you read
nothing beyond the guide and the materials directory.
```

## Scorer prompt

One fresh subagent per regeneration. The scorer institutionalizes the
verified-vs-reported lesson: a verdict without quoted evidence is worthless.

```
You are scoring a generated spec against a property matrix. Read ONLY:
1. The matrix: {MATRIX_PATH} (the property tables and their IDs)
2. The spec under test: {REGEN_PATH}

For EVERY property in the matrix, return one line:
  <property-id>: PRESENT | ABSENT | PARTIAL — <verbatim quote of the spec
  line(s) that prove it, with an approximate line number; for ABSENT, name
  what you searched for and where you looked>

Rules: never mark PRESENT without a quote; never infer from the spec's
self-descriptions (e.g. its own checklists) — find the actual content; note
formatting variants you had to accommodate (units, spelled-out numbers,
unicode operators like ÷). Do not read any other file.
```

Orchestrator duties after scoring: spot-audit ≥20% of verdicts against the
file yourself (grep with LOOSE patterns — the founding pass's false ABSENTs
came from tight patterns missing `chars÷4`, "max_iterations 10", "a new
process opened against the same store"); label every matrix cell
[verified] (you checked) or [reported] (scorer/regen claim only).
