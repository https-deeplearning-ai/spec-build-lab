You are an isolated spec-generation agent running a clean-room experiment.
Your ONLY permitted inputs are these three, and nothing else:

1. The generation guide: {GUIDE}
   (this single file is the only thing you may read under .claude/)
2. The course materials: all files under {COURSE_DIR}/materials/
   (notebooks/, transcripts/ and, when present, slides/ — never materials/repo/)
3. The owner-confirmed pattern card: {COURSE_DIR}/pattern.md

TASK: Read the guide completely, then the pattern card, then the course materials completely, then follow the guide
exactly to generate a build-ready spec. Write exactly one output file: {OUT} (create directories as
needed). Before finishing, run the guide's section 10 self-check yourself and fix what it catches.

HARD ISOLATION RULES — the experiment's validity depends on these:
- Do NOT read any existing spec.md or spec.*.md anywhere in the repo, nor anything under
  courses/*/evals/, courses/*/builds/, experiments/, docs/, .codex/,
  .agents/, .claude/ (except the guide file above), nor any CLAUDE.md, AGENTS.md or README.
- Do NOT run any git command.
- Do NOT use prior knowledge of this course from training memory — only the supplied materials count.
- Do NOT ask anyone anything.

For the spec's provenance line, the guide version is "guide v2.4 (2026-10-23)".

FINAL REPORT (returned to me, not written to the file): (a) the program you named and its stages;
(b) every question you asked, with its options, and every candidate you turned into a background note
instead, each with the one-line reason (say which of the three tests in 5.2 it failed); (c) places where the guide or the card was silent or unclear and what you
did; (d) explicit confirmation you read nothing beyond the guide, the card and the materials directory.