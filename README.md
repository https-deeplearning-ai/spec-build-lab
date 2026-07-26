# spec-build-lab

An exploration harness for one idea: **can a course's materials be turned into a
build-ready spec that a learner builds a real app from — and how well does the
result hold up?**

The loop:

```
course materials  →  spec.md  →  build  →  extract  →  eval  →  iterate
   notebooks +        /generate-   /prepare-   /extract-     /eval-spec-vs-build
   transcripts        spec         build       build-log     /eval-materials-vs-build
                                               (slice the
                                               session
                                               transcript)
```

This repo exists to run that loop many times, capture what happens, and judge it
from two angles — so the skills, the spec guide, and the eval criteria are all
expected to change as we learn.

## Structure

```
spec-build-lab/
├── .claude/
│   └── skills/
│       ├── new-course/                # scaffold courses/<name>/ from the template
│       ├── ingest-course-repo/        # optional extra: course repo → materials/notebooks/from-repo/
│       │   └── scripts/ingest_repo.py
│       ├── generate-spec/             # materials → spec.md (uses the guide below)
│       │   └── references/
│       │       └── spec-generation-guide.md
│       ├── prepare-build/             # allocate builds/run-NN/ + drop .session breadcrumb (auto-fires on build intent)
│       ├── extract-build-log/         # slice the conversation from the session transcript
│       │   └── scripts/extract.py
│       ├── eval-spec-vs-build/        # did the build follow spec.md?
│       └── eval-materials-vs-build/   # how does the build align with / diverge from the course?
├── templates/
│   └── course/                        # skeleton new-course copies
│       ├── materials/{notebooks,transcripts}/
│       ├── spec.md
│       ├── builds/
│       └── evals/
└── courses/
    └── <course-name>/                 # one per course (created by new-course)
        ├── materials/{notebooks,transcripts}/
        ├── spec.md
        ├── builds/
        │   └── run-NN/                # the built app, ONLY — gitignored here; may have its own git
        └── evals/
            └── run-NN/                # .session · spec.md · session-log.md · spec-vs-build.md · materials-vs-build.md
```

## Where you work (layers & movement)

Launch Claude Code **once, at the repo root**, and stay in that single session
for the whole loop. The root is where the skills and `CLAUDE.md` live. Your
*working directory* moves during the loop, but the *session* stays rooted at
the repo root.

| You're working in… | What happens there | What you run |
|---|---|---|
| repo root | manage courses | `/new-course` |
| `courses/<name>/` | spec + extract + evaluation | `/ingest-course-repo` (optional), `/generate-spec`, `/prepare-build`, `/extract-build-log`, `/eval-spec-vs-build`, `/eval-materials-vs-build` |
| `courses/<name>/builds/run-NN/` | actual app development | the build itself — install deps, run the dev server, optional app-level `git init` |

So `cd courses/<name>/` to work on a course; once a build starts, you and the
agent move down into `builds/run-NN/` to develop; come back up to the course
folder to extract the conversation and evaluate. Stay in one session per build —
the breadcrumb at `evals/run-NN/.session` points at that session's transcript,
which is what `/extract-build-log` slices.

## Lifecycle

```mermaid
flowchart TD
    NC["<b>/new-course</b><br/>scaffold courses/NAME/"]
    MAT(["add materials:<br/>notebooks + transcripts"])
    ICR["<b>/ingest-course-repo</b><br/>optional extra: course repo →<br/>materials/notebooks/from-repo/"]
    GS["<b>/generate-spec</b><br/>materials → spec.md"]
    PB["<b>/prepare-build</b><br/>allocate builds/run-NN/,<br/>snapshot spec → evals/run-NN/spec.md,<br/>drop .session breadcrumb"]
    OP(["you + coding agent<br/>build the app in builds/run-NN/"])
    EBL["<b>/extract-build-log</b><br/>slice transcript →<br/>evals/run-NN/session-log.md"]
    ESB["<b>/eval-spec-vs-build</b><br/>did it follow spec.md?"]
    EMB["<b>/eval-materials-vs-build</b><br/>aligned with the course?"]
    IT(["iterate"])

    NC --> MAT --> GS --> PB --> OP --> EBL
    MAT -. optional .-> ICR
    ICR -. adds to materials .-> GS
    OP --> ESB & EMB
    ESB --> IT
    EMB --> IT
    IT -. tune guide, regenerate .-> GS
    IT -. or start another build .-> PB
```

A walkthrough — building a RAG app from a `langchain-rag` course, empty repo to
evaluated run:

```text
# 1 · from the repo root: create the course
/new-course langchain-rag                 # -> courses/langchain-rag/

# 2 · add source material by hand
#     Get notebooks + transcripts at https://course-context-lab.vercel.app
#     (manual download — the agent does NOT fetch from the URL).
#     Tip: drag the downloaded files from Finder into the terminal window;
#     that pastes their absolute paths so the agent can `cp` them straight
#     into the course folder. Saves tokens vs. having the agent traverse
#     your filesystem.
#     notebooks   -> courses/langchain-rag/materials/notebooks/
#     transcripts -> courses/langchain-rag/materials/transcripts/

# 3 · move into the course and generate the spec
cd courses/langchain-rag

#     optional extra — adds the course's real code + helper.py on top of
#     the site download (see "Ingesting a course repo" below):
/ingest-course-repo https://github.com/deeplearningai-eng/courses/tree/main/course_10

/generate-spec                            # -> courses/langchain-rag/spec.md

# 4 · start a build (call it explicitly)
/prepare-build                        # -> builds/run-01/  (the app lives here)
                                          #    snapshots spec.md -> evals/run-01/spec.md
                                          #    drops evals/run-01/.session, moves you into builds/run-01/

# 5 · build the app with your agent — you are now in builds/run-01/
#     "build the RAG app from the spec"  -> install deps, write code, run it...
#     no recorder is running; Claude Code persists the transcript on its own.

# 6 · extract the build conversation when you have something worth capturing
cd ../..                                  # back up to courses/langchain-rag
/extract-build-log run-01                 # -> evals/run-01/session-log.md
                                          #    slices the transcript between
                                          #    the /prepare-build announcement
                                          #    and a fuzzy diagram/structure phrase
                                          #    (or pass --until="<phrase>" to override)

# 7 · evaluate — name the run (no default; you are asked if you omit it)
/eval-spec-vs-build run-01                # -> evals/run-01/spec-vs-build.md
/eval-materials-vs-build run-01           # -> evals/run-01/materials-vs-build.md

# 8 · iterate: tune the guide, then start another build
/prepare-build                        # -> builds/run-02/, evals/run-02/spec.md, ...
```

## Ingesting a course repo

`/ingest-course-repo` is an **optional extra**, not a shortcut. Materials still
come from https://course-context-lab.vercel.app — both the notebooks `.md` and
the transcripts. What this adds on top is the course's real, runnable code and
its `helper.py` definitions, which the site dump doesn't carry.

```text
cd courses/<name>
/ingest-course-repo https://github.com/deeplearningai-eng/courses/tree/main/course_10
```

For DeepLearning.AI courses, browse https://github.com/deeplearningai-eng/courses
to find yours and paste the URL of its **folder**. That repo is a ~3.4 GB
monorepo holding every course, so a course-scoped URL is required — passing the
bare repo root is refused.

What it does, exactly (`ingest-course-repo/scripts/ingest_repo.py`, stdlib-only):

1. **Clones the repo** using your own git credentials — so a private repo works
   as long as *you* can reach it. Accepted forms:
   - **GitHub tree URL** — `…/tree/<ref>/<path>`, parsed into repo + `--ref` +
     `--subdir`. This is the form to use for the monorepo.
   - **SSH** — `git@github.com:org/repo.git` or `ssh://…` (uses your SSH key)
   - **HTTPS** — `https://github.com/org/repo.git`
   - **Local path** — an existing directory or `file://` URL is copied, not
     cloned (handy for testing or repos you already have on disk)

   With a `--subdir` the clone is **sparse and blobless**, so only that one
   course's files are fetched — pulling `course_10` out of the 3.4 GB monorepo
   transfers about 9 MB and takes a few seconds. LFS payloads are skipped;
   ingestion reads notebooks and helper modules, never datasets.
2. **Renders every `.ipynb`** in scope cell-by-cell into a single markdown file
   at `materials/notebooks/from-repo/<course>-context.md` — the same shape as a
   hand-downloaded course context dump.
3. **Appends a de-duplicated "Helper Module Context" section** from the repo's
   `helper.py` module(s): each unique top-level def/class appears once,
   identical copies (including symlinks) collapse, and a same-name-but-
   different-body collision keeps both variants flagged inline — nothing is
   silently dropped.

The `from-repo/` subfolder matters: a hand-downloaded context dump is named
`<course>-context.md` too, so a flat write would silently overwrite it. Both
files coexist and `/generate-spec` reads both — the site dump stays
authoritative for lesson numbering and titles, the ingested file carries the
code.

Scope guarantees: the script writes **only** into
`materials/notebooks/from-repo/`; `materials/transcripts/` is never touched and
remains a manual download from the course site. Lesson numbering in the output
is inferred from sorted notebook order — a convenience label, not authentic
platform numbering. The ingest is idempotent: re-running overwrites its own
output file cleanly and leaves everything else alone.

`/prepare-build` is the expected, explicit step — it will also fire on its own
if you simply start building, but the documented flow is to call it. The spec eval
reads the per-run snapshot `evals/run-NN/spec.md`, so an older run is always judged
against the spec it was actually built from, not a spec you regenerated later.

## Notes / TODO
- The structure here — skill names, folder layout, and read/write paths — matches
  this doc. The remaining stub is the spec-generation guide content
  (`generate-spec/references/spec-generation-guide.md`); it carries inline TODOs
  and is meant to be tuned against eval feedback.
- Recording is **post-hoc**, not real-time. Claude Code already persists every
  turn into `~/.claude/projects/<slug>/<session>.jsonl`; `/extract-build-log`
  slices that JSONL between bookends and writes `evals/run-NN/session-log.md`
  on demand. There is no `Stop` hook, no `.active-run` pointer, no
  `build-complete` marker — `evals/run-NN/.session` is a write-once breadcrumb
  recording which transcript to slice.
- Per course, only `spec.md`, `materials/`, and an optional
  `spec.coding-agent-lab.md` (a tracked variant of the canonical spec, for
  exploring a Decision Ledger change without touching `spec.md`) are
  version-controlled. Everything else under `courses/<name>/` — `builds/`
  (built apps are artifacts) and `evals/` — is gitignored and stays local.
