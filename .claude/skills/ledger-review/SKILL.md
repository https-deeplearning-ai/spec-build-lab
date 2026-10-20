---
name: ledger-review
description: Posts a plain-language review on a spec pull request, one thread per Decision Ledger decision on its row, listing every option so a curriculum product manager can review them. Run only when the user types /ledger-review <PR number>.
disable-model-invocation: true
argument-hint: <PR number>
allowed-tools: [Read, Write, Edit, Bash]
---

# ledger-review

Writes a review for each spec file a pull request changes: every Decision Ledger row as a short
section, every option as a table row, in plain language a non-engineer can review and comment on.
Each section is posted as a review comment on its row of the Ledger table, so each decision gets its
own thread; a header comment on the table's header lines carries the legend and the open points.
When part of the Ledger is not in the PR's diff, GitHub cannot take a comment there, and the whole
review goes up as one comment on the file instead.

The comment has two kinds of content, and they are produced differently:
- **Fixed and factual parts** — the header, legend, headings and their links, the table columns,
  every option id, the Labels column, "Asked only if…", the test counts and skipped questions, the
  footer. `scripts/ledger_review.py skeleton` renders these from the spec. **Never type or edit them.**
- **Slots** (`⟦…⟧`) — the plain-language wording. You write these, following the writing rules below
  and the worked example in `references/example-review.md`.
`scripts/ledger_review.py check` then compares your draft with the skeleton line by line.

## Steps

`$S` below is `"$CLAUDE_PROJECT_DIR/.claude/skills/ledger-review/scripts/ledger_review.py"`. Work in a
fresh scratch folder (`W=$(mktemp -d)`); write nothing into the repo.

1. **Find the specs.** `gh pr view <N> --json headRefOid,title,body,url`,
   `gh pr diff <N> --name-only` and `gh pr diff <N> > "$W/pr.diff"`. Keep the changed files matching
   `courses/<course>/spec.md` or `courses/<course>/spec.<variant>.md`. If there are none, say so and
   stop. Do steps 2–7 once per file, then step 8 once.
2. **Get the spec at the PR's head commit.** `git fetch origin pull/<N>/head` then
   `git show <headRefOid>:<path> > "$W/<path's file name>"` (keep the file name: the header shows it).
3. **Previous review.** `python3 $S previous <path> --exclude-pr <N> > "$W/prev.md"` (it finds either
   kind: a review's comments or a single PR comment). If the file is non-empty, sections whose spec
   text is unchanged are copied from it word for word.
4. **Skeleton.**
   `python3 $S skeleton "$W/<file>" --out "$W/out" --path <path> --name "<name>" --link-base "https://github.com/<owner>/<repo>/blob/<headRefOid>/<path>"`
   plus `--previous "$W/prev.md"` when step 3 found one. `<name>` is the PR title's text before its
   first ":" (e.g. `support-bot` for "support-bot: adopt …"); without a ":", the course folder name. Read `out/skeleton.md` and
   `out/sources.md`.
5. **Fill the slots.** Copy `skeleton.md` to `draft.md` and replace every `⟦…⟧` using `sources.md`
   (each slot's source spec text is listed under its row) and the writing rules. Change nothing
   outside the slots, and keep the `<!-- ledger-review … -->` lines.
6. **Check.** `python3 $S check "$W/out/skeleton.md" "$W/draft.md"` until it prints PASS. Then reread
   every slot against its source: each claim must be in the spec; nothing is added.
7. **Split.** `python3 $S split "$W/draft.md" "$W/<file>" --path <path> --commit <headRefOid> --diff "$W/pr.diff" --out "$W/post"`.
   It prints `threads` (the comments go into `post/review.json`; a second spec file appends to it,
   because GitHub allows one pending review per person per PR) or `file comment` (the whole draft
   goes into `post/file-comment-<file>.json`, because part of the Ledger is not in the diff).
8. **Show, then post.**
   - **Threads:** create the review as pending, which only the user can see:
     `gh api -X POST repos/{owner}/{repo}/pulls/<N>/reviews --input "$W/post/review.json" --jq .id`.
     Then `python3 $S verify <N> <review id> "$W/post/review.json"` must print PASS; if it fails,
     delete the pending review (`gh api -X DELETE repos/{owner}/{repo}/pulls/<N>/reviews/<review id>`)
     and stop to report. Tell the user where to look: the PR's Files changed tab, "Load diff" on a
     large spec, the Ledger table's lines; the review button shows the comment count. Submit only
     after they say so: `gh api -X POST repos/{owner}/{repo}/pulls/<N>/reviews/<review id>/events -f event=COMMENT`.
     If they don't want it, delete the pending review. Report the review's URL.
   - **File comment:** GitHub cannot hold one as pending; it is public the moment it is posted.
     Show the user the draft in the terminal and post only after they say so:
     `gh api -X POST repos/{owner}/{repo}/pulls/<N>/comments --input "$W/post/file-comment-<file>.json"`.
     Report the comment's URL.

## Writing rules for the slots

These are the rules the reference comment (`references/example-review.md`) was written with. **Read
the example before writing**, and match its style and its brevity.

1. **Plain English for a non-engineer.** No internal terms (Invariant, litmus, realization, stand-in,
   acceptance criteria, tie-breaker, disposition, narrative, bake-in, Ledger, §) and no rule or test
   ids (`R12`, `AC7`); the checker rejects them. Course terms (a lesson, a tool's name) stay, explained
   once where they first matter. Say "fake" for a scripted stand-in and "tests" for acceptance criteria.
2. **Every claim comes from the spec**: the row's Decision, Default and Trade-off cells, the option's
   own cell, and its §7 line — all quoted in `sources.md`. Never add a fact. Translating a spec term
   into the reader's words is not adding one, when the meaning is the same (a "knowledge base" the
   spec says holds documents is "a document library").
3. **Brief.** Say only what a reviewer needs to judge the choice; leave out mechanism (how something is
   logged, file and variable names, exact counts the skeleton already shows). In the reference, a
   title runs about 5 words, a question about 11, a "why" about 18, an option about 10, an "If chosen"
   about 9 and a setup 1–3. These are its typical lengths, not limits: a cell that must name several
   parts can run longer.
4. **Name things as the reader sees them,** not with the spec's category words: name the concrete
   parts ("a ticket inbox, a reply history and a team directory"), not "three stores".

Per slot:
- **S1 title** — the subject as the reader thinks of it, as a short phrase ("Where replies are
  stored", "Who approves a reply"), never the spec's term ("Persistence realization").
- **S2 question** — the question the gate asks, in the reader's words, as one question ("should the
  assistant send replies itself, or wait for a person to approve each one?").
- **S3 why** — one sentence giving the gist of why this is a choice, from the Trade-off cell (or the
  Default cell, when it says why): at most one clause per side, citing the lesson when the cell names
  one ("Lesson 3 shows auto-sending working; Lesson 4 adds approval for risky replies"). Not the
  cell's full argument. When neither cell gives a reason, say in one clause what the question is
  for, or that the course made no choice here when a cell says so.
- **S4 option** — what the reader gets, starting with that thing ("A local database file, built into
  the language", "Every reply waits for a person"), from the option's own cell. Leave out where the
  course showed it: the Why line and the Labels column already carry that.
- **S6 setup** — taken from the option's own cell only. "None" when the option uses nothing outside
  the build; the key or account it needs ("An email-service API key"); "Heavy: …" when the option's
  cell calls its setup heavy, with that note in plain words; "Per item" when the option's setup
  depends on what the learner names; only setup text counts (an effect such as "results vary" is not
  setup); "None stated" only when the option plausibly needs something (a
  different runtime, an outside service) and the spec does not say.
- **S5 what it leaves out or changes** — from the option's §7 line, in plain words, **the main effect
  in one clause**: what the build leaves out ("Leaves out automatic sending") or what changes ("The
  tests need the service running"). When the line is mostly adjustments to individual tests, say what
  a reviewer would notice ("Most tests check only the shape of answers") instead of listing them.
  The skeleton appends the count and skip sentence after it; do not restate that count (other numbers
  from the §7 line are fine when the reviewer needs them). When an option changes what another option
  of the same row changes, a pointer is fine ("The same as the option above").
- **OPEN-NOTE / OPEN** — the PR body's "Known open points" (or similarly named) section, rewritten in
  plain words as a numbered list, one point per line, each starting with the Ref or subject in bold.
  The note in parentheses is "already flagged", plus "; tracked on #N" when the PR body names a
  tracking issue. If the PR lists none, write `1. None listed in this PR.` and the note
  "none listed".

## Don't

- Don't type, reorder or reword any part outside a slot — a mismatch fails the check.
- Don't read course materials; the spec is the only source.
- Don't submit the review or post a file comment before the user says so. Creating the pending
  review is fine: only the user sees it, and it is how they see the review before it is public.
