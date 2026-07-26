---
name: ingest-course-repo
description: >
  Adds a course repo's notebooks and helper modules to a course's
  materials/ in the spec-build-lab, rendered into
  materials/notebooks/from-repo/<course>-context.md. Use this skill ANY
  time the user wants to pull course code out of a git repo — including
  phrasings like "ingest the course repo", "pull the notebooks from this
  repo", "here's the course repo", "add the course code to materials",
  "get the notebooks from git", or "/ingest-course-repo <url>". Takes a
  course-scoped repo URL: a GitHub tree URL pointing at one course
  folder, a plain SSH/HTTPS repo URL, or a local path. It is an OPTIONAL
  supplement to the manual material download, never a replacement — it
  adds the course's real code and helper.py on top, and NEVER produces
  transcripts. Must run from inside a course folder (courses/<name>/).
  Do NOT use this skill to write spec.md — that's /generate-spec.
argument-hint: <course-repo-url>
allowed-tools: [Bash, Read, Glob]
---

# ingest-course-repo

Render a course repo's `.ipynb` files and helper module(s) into
`materials/notebooks/from-repo/<course>-context.md`.

This is an **extra**, not a shortcut. The main way materials arrive is still a
manual download from https://course-context-lab.vercel.app — both the notebooks
`.md` and the transcripts. What this skill adds on top is the course's real,
runnable code and its `helper.py` definitions, which the site dump doesn't
carry. Transcripts are never produced here.

## Steps

1. **Verify cwd is a course folder.** Confirm all of these exist relative to
   cwd: `materials/notebooks/`, `materials/transcripts/`, `builds/`, `evals/`.
   If any are missing, refuse with: "Run /ingest-course-repo from inside a
   course folder — `cd courses/<name>` first." Stop.
2. **Require the repo URL.** If `$ARGUMENTS` is empty, say: "Which course repo?
   If it's a DeepLearning.AI course, find it at
   https://github.com/deeplearningai-eng/courses and paste the URL of the
   course's folder — e.g. `.../courses/tree/main/course_10`." Stop until they
   answer.
3. **Parse the URL.** Strip any `?query` or `#fragment` first, then:

   | Input | Becomes |
   |---|---|
   | `https://github.com/<org>/<repo>/tree/<ref>/<path…>` | repo `https://github.com/<org>/<repo>`, `--ref <ref>`, `--subdir <path…>` |
   | `https://github.com/<org>/<repo>` | repo as given, no `--subdir` |
   | `git@…:…`, `ssh://…`, local path, `file://…` | repo as given, no `--subdir` |

   Strip only the `/tree/<ref>/<path…>` tail; don't add or remove a `.git`
   suffix. The repo string lands in the generated file's provenance line, so it
   should read back as what the user actually pasted.

   A `/blob/` URL points at a file — ask for the folder URL instead. Splitting
   `tree/<ref>/<path>` assumes the ref is a single segment; if the branch name
   contains a `/`, that guess is wrong, so let the user correct it and pass
   `--ref` / `--subdir` explicitly.
4. **Refuse the courses index.** If the input resolves to
   `deeplearningai-eng/courses` with no subdirectory, refuse with: "That's the
   courses index — 262 courses, 3.4 GB. Browse to your course and paste its
   folder URL, e.g. `.../courses/tree/main/course_10`." Stop. Any other repo
   root is fine and proceeds without `--subdir`.
5. **Run the ingest script** from the course folder:
   ```bash
   python3 "$CLAUDE_PROJECT_DIR/.claude/skills/ingest-course-repo/scripts/ingest_repo.py" \
     <repo> --out "materials/notebooks/from-repo/<course>-context.md" \
     [--ref <ref>] [--subdir <path>]
   ```
   Use the course-folder name (cwd basename) for `<course>`. With `--subdir`
   the clone is sparse and blobless, so only that course's files are fetched.
   Other flags, rarely needed: `--title` (document H1), `--helper-name`
   (default `helper.py`), `--keep-clone` (debugging). If the script exits
   non-zero — clone/auth failure, a subdir that doesn't exist, nothing to
   ingest, or a bad `--out` — surface its error verbatim and Stop.
6. **Report.** Echo the script's one-line summary (notebooks, cells, helper
   files, unique defs, conflicts). Then `Glob materials/notebooks/*.md`: if a
   hand-downloaded `*-context.md` sits at the top level, add a note that both
   are now read by `/generate-spec` — the site dump is authoritative for lesson
   numbering and titles, this file carries the real code and `helper.py`. State
   it and move on; don't ask the user to choose.
7. **Hand off.** Remind them the site download is still the main source: if
   `materials/transcripts/` is empty, transcripts must come from
   https://course-context-lab.vercel.app. Once materials are in place, run
   `/generate-spec`.

## Don't

- Don't write `spec.md` — that's `/generate-spec`.
- Don't write anywhere under `materials/` except
  `materials/notebooks/from-repo/`, and never into `materials/transcripts/`.
  The script enforces this too, but don't rely on it.
- Don't overwrite or edit a hand-downloaded `*-context.md`. The `from-repo/`
  subfolder exists precisely because the two share a filename.
- Don't WebFetch course content, or the courses index — the user browses it and
  pastes a URL. The agent only clones the repo it was handed.
- Don't clone a monorepo root hoping to filter afterwards. Scope it with
  `--subdir` so the fetch stays small.
- Don't run from the repo root or from inside a build folder. Materials are
  off-limits during a build, and a `PreToolUse` hook enforces that.
