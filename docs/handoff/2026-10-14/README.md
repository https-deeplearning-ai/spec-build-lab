# Handoff — loop-engineering lab spec, guide iteration, and the agent-memory comparison (2026-10-13 → 14)

Written for the owner and for a fresh agent session. **Start here.** Everything here is verifiable in the repo or in the
files listed in §9; every artifact this document cites that is not part of the repo proper sits beside it in this folder. Dates are absolute. "Owner" = Carr.

## 0. State of the repo right now

| Thing | State |
|---|---|
| `main` | has guide rules #43, #44, #45 and the **unaudited** loop-engineering lab spec E (merge `09da2a8`, PR #46) |
| PR #47 (open) | `course/loop-engineering-audit` → main: spec E after two audit/repair rounds. **Merge it before any build.** Merge as a merge commit, never squash (specs pin guide commits by hash) |
| Shipped lab spec after #47 | `courses/loop-engineering-with-langchain-deepagents/spec.coding-agent-lab.md`, 694 lines, 29 rules, 51 ACs, 5 rows, guide `b03ddc9`, overlay `184a0ed` |
| Agnostic loop-engineering spec | `spec.md` on main is still the `fb75bb6` generation (guide `11b3673`); **not regenerated** on the updated transcript (new Lesson 6) |
| Agent-memory regen (comparison only) | `docs/handoff/2026-10-14/agent-memory/{spec.md,diff-analysis.md}`; shipped agent-memory spec untouched |
| Builds/evals on loop-engineering | **none have ever run** |
| Open issues | #38 (RR1 live option; overlay one-answer rows), #35 (composition variance; overlay silences), #31, #26, #19 |

Model assignment (owner rule): clean-room generation and repairs on **Fable 5.1** (`model: fable`), independent
audits on **Opus 5.5** (`model: opus`). The agent-memory comparison regen was run on Opus by explicit owner request.

## 1. Owner's working rules (in force)

1. One guide/overlay rule per PR, only what the owner asked for and can explain back. Audit findings that need a
   decision go to an issue, never into a repair.
2. Surface decisions before executing; stop and report instead of starting the next round.
3. After a generation, run the **checkpoint** (§3) and stop; audits only on the owner's call. No third audit round.
4. Repairs never change a Ledger row, Option, Default, "(course default)" label or trade-off disposition.
5. Before blaming a guide sentence for a generator's reading, grep the whole guide and overlay for the concept
   and read the generator's own stated reasoning (a mis-aimed rule cost one regeneration on 2026-10-13).
6. Findings: precise, short, plain English, verifiable by a reader with no context.

## 2. What was changed in the guide, overlay, runtime — and why

Runtime file `spec-generation-guide.coding-agent-lab.runtime.md`: **untouched**. Checker `check_spec.py`: **untouched**.
All paths under `.claude/skills/generate-spec/references/`.

| PR / commit | File · section | Change (one rule each) | Why |
|---|---|---|---|
| #41 `adeff70` (merged 10-13) | overlay · OVERRIDE 2 | An Option the learner **cannot take in the lab** (needs a credential the lab does not supply, or makes the offline suite wait on a person) is not presented. Some alternatives takeable → the untakeable one leaves the cell, goes to §1 Not Included as `unavailable` with its seam. None takeable → the row leaves the Ledger via the Environment Resolutions table ("ANSWERED — every alternative unavailable here"), default pinned in §2. Audit check (q). | The old rule "mark the impractical option in its cell, never delete it" produced a gate question whose only second answer needed an Atlassian token (#38 §1). |
| #43 `4e1b71e` (+ count fix `a6064cb`) | guide · §5.5 new paragraph after "No route admits a non-decision"; §4 Pass-B disposition vocabulary; §5.5 scope-boundary handling rule (one clause); §14 line; audit check (r) | **An argued subject has three dispositions and no fourth**: row / bake-in / lever. `narrative` only for framing/taxonomy the course never argued as a builder's choice. A §1 tag, a §2 pin or a CTX paragraph is *where a side is recorded*, never a way out of the Ledger; a side built on a primer/toy still counts as built; its §1 item is `owned-by-row`. Non-row entries name their tie-breaker. | Instruction placement (always-on file vs skills) was a Ledger row in 11 generations and a `restorable` exclusion or `narrative` in 5, on one guide. Every earlier convergence fix sharpened the row/bake-in/lever test; the open splits were subjects that passed it and then left the Ledger through a separately defined home. |
| #44 `57d4414` | guide · §5.5 right after tie-breaker 2; §14 clause; audit (r) clause | **A limit value that removes a component is a component choice, not a knob** (budget 0 removes the grader; depth 0 removes retrieval): tie-breaker 2 and the degenerate-case clause do not apply; the litmus decides — row if the course showed the system working without the component, bake-in if it showed it failing. The number stays a lever on the side where the component exists. | "What a triggered run runs" (verified loop vs bare agent loop) was a row in 4 lab generations and a lever in 3; the lever reading cited tie-breaker 2 (which lists "a budget") with the degenerate-case reason — two rules that contradict each other (audit finding). |
| #45 `b03ddc9` (rewritten) | guide · §3 keyed-tool rule after its yes/no test; §14 clause; audit (r) clause | **Omission means leaving out the keyed tool, never the taught behavior it carried.** On the yes-branch (the tool is the only carrier of a taught stage: trigger surface, grader, model) the Options cell holds two realizations, real tool + stand-in; "omit" is not listed. On the no-branch "omit" means the keyless course tool does the job. | Generation C offered "omit the event-driven layer — tickets and pages removed" as a row option the course never presented. **First version of #45 patched the §5.5 reduced-scope sentence instead** (mis-diagnosis; generator report on the next run named line 83 as its real basis) — withdrawn and rewritten. |
| overlay re-pins | overlay line 6 "Written against base guide" | hash only, in each PR; four OVERRIDE quotes verified unchanged with `grep -cF` | the overlay's staleness check |

Impact checked read-only before each rule on the other two courses: agent-memory and Qdrant rows do not move on
paper. **But see §6: a fresh Opus generation of agent-memory on this guide moved one subject (#43's "maturity
story" clause).**

## 3. The workflow as run, and its philosophy

```
guide change (one rule, PR, overlay re-pin)
   ▼
course branch: merge guide, delete old spec (clean room: Write cannot overwrite an unread file)
   ▼
GENERATE  fresh Fable agent · inputs: guide, overlay, runtime (opened only after Phase 1), materials
          forbidden: every spec, experiments/, docs/, evals/, builds/, materials/repo/, git
          output: spec + checker=0 + report (a) rows (b) self-check fixes (c) overlay gaps (d) isolation (e) tokens
   ▼
CHECKPOINT  orchestrator, read-only, ~0 tokens — added after generation B
          checker · provenance pins · row set vs the record · trade-off table (dispositions + tie-breakers)
          · Not Included tags (owned-by-row targets exist; no restorable item is an argued side)
          · target row read as the learner sees it · overlay gaps reported
          fails → fix wording once, regenerate once; second failure → document and stop
          holds → STOP and report; audits only on owner's go
   ▼
AUDIT 1   fresh Opus agent, prompt = audit-prompt.md (18 checks, whole file, defects only, HARD/SOFT)
   ▼
orchestrator: spot-check ≥3 HARD by eye; write findings file; mark decisions [ORCHESTRATOR: SKIP]
   ▼
REPAIR 1  fresh Fable agent; constraint: never change a decision; checker=0; citations reciprocal; fix log
   ▼
AUDIT 2 → spot-check → REPAIR 2 → commit → PR        (round 3 only on owner's call)
```

**Philosophy (skill step 4a/4b + audit-prompt orchestrator duties).** Two defect classes, two fixes:
- *Decision defects* (a row missing, an option invented, a disposition wrong) belong to the guide. Only a rule plus a
  regeneration fixes them, because a hand-edited row says nothing about the next generation. → the five regenerations.
- *Consistency defects* (a turn count not following its rule, fixture arithmetic, an undeclared hook, a wrong anchor)
  are generator slips against rules the guide already states. Repair in place; decisions untouched. → the audit rounds.

**Honest critique (owner's question "isn't repair just hand editing?").** Yes, by design, bounded to class two. Three caveats:
1. The boundary got stretched: repairs added rules (R25/R29) and criteria (AC36–38 on B; AC48–51 on E), and one new
   behaviour (a Revert control, see §5). The audit prompt says criterion coverage is the generator's.
2. Volume is systematic: first-round HARD counts 23 → 18 → 14 across the day, nearly all inside the scripted-stand-in
   oracle (exact turn counts, fixtures, hooks). The guide demands that precision (§3 scripted-model rule; "replay every
   verdict"); the fix that would cut the count is an altitude rule (stand-in specified by outcomes, not a 9-step
   policy) — proposed, deferred.
3. The merged spec is co-authored: Ledger = generator; oracle = generator + two repair passes.

Cost per cycle (approx.): generation 300–330k tokens; each audit 150–170k; each repair 140–185k → ~950k with audits.

## 4. The loop-engineering lab saga — what we struggled with

### 4.1 Generation record (all on Fable 5.1; A is the pre-session spec)

| Gen | Guide | Rows | Instruction placement | Grader present vs bare loop | Grader kind | Event source | Audited? |
|---|---|---|---|---|---|---|---|
| A `ac0ec65` (merged #42) | `11b3673` | 4 | **missing** | row ("what a trigger runs") | row | table | yes |
| B `8ab9489` | `4e1b71e` #43 | 4 | row | **lever** | row | table | yes (18/14 → 8/13) |
| C raw | `57d4414` #44 | 6 | row | row | row | **row with invented "omit" option** | no |
| D raw | `57d8df0` old #45 | 4 | row | row | **missing** | table | no |
| E `35da066`/#47 | `b03ddc9` #45 | 5 | row | row | row | table | yes (14/15 → 11/11) |

E is the target set: L6 scope, D1 instruction placement, D2 verification stage present, D3 grader kind, RR1 suite model.
(Scope row id is `L6` not `L1` — cosmetic, generator counted the sixth learner dimension.)

### 4.2 Each split, the sentence behind it, the fix

| Split | Generator's stated reading | Guide sentence | Fix |
|---|---|---|---|
| Instruction placement → Not Included `restorable` | "skills are additive, shown on a toy agent" | §5.5 scope-boundary "additive and owned by no other row → restorable" had no precedence vs the argued-row route | #43 |
| Trigger composition → lever | "budget 0 is the degenerate case of the budget" | tie-breaker 2 lists "a budget"; degenerate-case clause | #44 |
| "omit the event layer" option | keyed-tool rule's third realization "omission" (+ reduced-scope sentence as secondary) | §3 line 83 "present all three realizations … and omission" | #45 rewritten |
| Grader kind → `narrative` (gen D only) | "presented, never argued or built" | §5.5 "may still enter through design-structural on its own merits" — the word *may* | **no rule**; returned on its own in E; parked |

### 4.3 Things that cost time (so the next session avoids them)

- **Mis-diagnosis** of the "omit" option (blamed one §5.5 sentence; the generator's basis was §3 line 83). One wasted
  regeneration (D). Rule 5 in §1 exists because of this.
- **Checkpoint missing** on B: ~630k of audits spent before noticing the trigger row was gone.
- **Convergence worry**: every regeneration moved a different row. What converged: each subject with a rule stayed put
  afterwards (instruction row 4/4, grader-present 3/3, no invented omit 1/1). What did not: a new reading appeared each
  time. Owner's standing concern: the guide must not grow a rule per surprise. Measure convergence as "the set of
  splitting subjects shrinks"; stop at a threshold (e.g. two consecutive regenerations with the same row set).
- **PR #42 was merged mid-session** (2026-10-13 05:48Z, at spec A) without the orchestrator noticing; later commits sat
  on a closed PR. Check `gh pr view` state before updating a PR body.
- **Shell pitfalls**: `git checkout` refused while an untracked raw spec sat in the tree (copy it to scratch, remove);
  a chained command hung on `sed -i` with an unset path — keep chains short, no stdin-dependent tools.
- **Stacked PRs**: after merging the base PR, retarget the next (`gh pr edit N --base main`) before merging; GitHub
  reported #46 CONFLICTING after retarget while a local `git merge origin/main` was clean — merge locally, push, retry.

## 5. The shipped lab spec (E after #47) — what the owner should know

Rows, plain words:

| Row | Question | Default | Alternative |
|---|---|---|---|
| L6 | Should any exclusion come back? | keep | bring an item back (tags: restorable / buildable-unparameterized / owned-by-row / unavailable) |
| D1 | Where do the agent's instructions live? | one always-loaded file | file + skills directory (progressive disclosure; path `/skills/<section>/SKILL.md`, writes denied) |
| D2 | Is there a grader around the agent loop? | present, budget 3 | absent, budget 0 — retires the grader ACs and leaves the learning loop without signal |
| D3 | What kind of grader? | model, reads the file, quotes lines | deterministic code grader |
| RR1 | Which model does the suite run against? | scripted stand-in | course's live models via the lab key |

Resolved by the lab, not asked: event surfaces (real Slack / Jira+Confluence → `unavailable`, seam = the single trigger
function a webhook would call), hosted tracing (`unavailable`). Lesson 6's value in the lab is therefore a documented
seam, not a question. A possible future option: a **simulated chat surface** (fake Slack page, formatted + raw Markdown
reply) as a takeable second realization — owner decision, not started.

Skipped in both audit rounds (decisions): RR1's live option contradicting the offline completion gate (#38 item 2);
the hosted-tracing collapse. Added by repair pass 1, **owner to accept or strike**: a human-triggered **Revert** control
on the Learning page (R21 clause, AC50) to define "a regression means the change is not kept".

Owner-reported assessment of the spec against the repo's purpose (build on the pattern / customize / swap project):
build-on-pattern strong (CTX-A, 16-entry failure catalog); customization thinner than the course invites (loop
composition asked only piecewise; no learning-loop row); project swap not supported where it matters — the 51-criterion
oracle is keyed to the review-agent fixtures and would not survive a swap (an agnostic-mode problem). The scripted
stand-in is specified at implementation altitude (9-step policy, exact turn counts), where the guide's §2 forbids it.

## 6. Agent-memory comparison (Opus 5.5 clean room on guide `b03ddc9`, 2026-10-14)

Files: `docs/handoff/2026-10-14/agent-memory/spec.md` (550 lines, 23 rules, 34 ACs, 14 rows) and
`diff-analysis.md` (six sections, line-numbered quotes). Shipped spec untouched.

Agreement on the core: seven stores, SQLite substituted for Oracle (tier 1), recoverable compaction, thread-scoped
summaries, Tavily omitted, cosine, five tools per turn.

| Difference | New | Shipped | Note |
|---|---|---|---|
| Conversation-only memory | `narrative` ("maturity story") | option on D7 (Lesson 2 argues it aloud) | **caused by #43's wording**; the exact case the reduced-scope sentence was written for (2026-09-07); the pre-PR impact check said it would not move |
| Model the suite runs against | new row RR2 (scripted stand-in) | none; stubs as hardening, demo tested live only | gain |
| Toolbox search | harness-only (Lesson 6 app) | also an agent tool | different reading of the course |
| Context reduction options | 2 | 3 (adds pure compaction) | |
| Category labels | topology structural / triggers argued | topology argued / triggers structural | the known label variance (#33 F2) |

Generator's reported tensions: is Oracle the taught subject (substituted); the embedding model is keyless but a large
download ("offline after first fetch" has no class); conversation-only memory — the guide's "maturity story" and
"moves beyond … legitimate reduced-scope choice" point opposite ways.

## 7. Unresolved findings (decide from this list, not from the next surprise)

| # | Finding | Where | Decision needed |
|---|---|---|---|
| U1 | #43's "`narrative` … framing, taxonomy, a maturity story" put agent-memory's argued conversation-only baseline at narrative | guide §5.5 three-dispositions paragraph | narrow "maturity story" to "a story the course did not argue as a choice"? or accept |
| U2 | "may still enter through design-structural" dropped the grader-kind row once (gen D) | guide §5.5 design-argued paragraph | leave (returned on its own) or make the structural test mandatory for presented alternatives |
| U3 | RR1 offers the live-model option that contradicts the offline completion gate | guide §3 scripted-model rule; spec RR1 | #38 item 2 — adopt a rule, hand-edit, or leave |
| U4 | Overlay collapse case says "no alternative remains takeable"; intended "no alternative to the Default" | overlay OVERRIDE 2 | one word |
| U5 | Web framework flips Flask/FastAPI every generation (course unpinned vs lab preinstalled) | overlay (silent) | one sentence either way (#35 §2) |
| U6 | Runtime file never states what the lab does **not** supply (generator inferred Slack/Atlassian/LangSmith are unsupplied) | runtime file | state the negative |
| U7 | "(course default)" label when the course used both a real and a simulated realization | overlay/guide | one sentence |
| U8 | Hosted tracing collapsed through the table in 4 generations; audits say stand-in + omission are takeable | spec + overlay | owner's call |
| U9 | Revert control added by repair (R21, AC50) | spec E / #47 | accept or strike |
| U10 | Repairs add rules/ACs although the audit prompt reserves AC coverage for the generator | audit-prompt orchestrator duties | tighten the wording, or sanction additions explicitly |
| U11 | Scripted stand-in at implementation altitude; ~all audit HARDs live there | guide §3 scripted-model rule + §2 altitude | altitude rule: specify stand-ins by outcomes |
| U12 | Agnostic oracle does not survive a project swap | guide §5/§8 | tag ACs pattern-level vs example-level |
| U13 | Lab asks loop composition piecewise (D2) and never about the learning loop | overlay / project answer | ask all loops the same way, or none |
| U14 | Simulated chat surface as a takeable Lesson 6 option | overlay/guide keyed-tool stand-in | owner decision |
| U15 | Scope row numbered L6 instead of L1 | spec E | cosmetic; audit may flag |
| U16 | Checkpoint is practice, not in the skill | `generate-spec/SKILL.md` step 4a-bis | one PR if it keeps paying |
| U17 | No build or eval has run on loop-engineering | — | `/prepare-build --env=coding-agent-lab` after #47; Sonnet recommended, Haiku if cost rules |
| U18 | Agnostic loop-engineering spec not regenerated on the new transcript (real-Jira option lives there) | `courses/…/spec.md` | clean-room regen, same flow |

## 8. Next-action options (owner picks)

1. Merge #47 (merge commit). Then build spec E with a subagent, baseline answer at the gate, run both evals — the
   first evidence on this course; do this before any further guide rule.
2. File one issue carrying U1–U16 verbatim.
3. Decide U1 before the next agent-memory regeneration; it is the first sign of a new rule moving another course.
4. Baseline (agnostic) loop-engineering regeneration on the updated transcript (U18), same flow, checkpoint, stop.

## 9. File index

- Guide/overlay/audit prompt: `.claude/skills/generate-spec/references/{spec-generation-guide.md, spec-generation-guide.coding-agent-lab.md, spec-generation-guide.coding-agent-lab.runtime.md, audit-prompt.md}`; skill: `.claude/skills/generate-spec/SKILL.md` (steps 4a/4b).
- Session artifacts (this folder): `docs/handoff/2026-10-14/loop-engineering/` — `spec-A…E-*.md` (every generation, raw and audited), `audit-{B,E}-round{1,2}.md` (findings with orchestrator notes), `fixlog-{B,E}-audit{1,2}.md`, `spec-E-before-audit{1,2}.md`.
- Earlier regens (local, untracked — may be absent on another machine): `experiments/loop-engineering/guide-loop-engineering-residuals/regen-*/`; matrices (tracked): `docs/research/guide-loop-engineering-residuals-matrix.md`, `docs/research/guide-sources-and-tiebreaks-property-matrix.md` (X2 instruction placement, X3 change target).
- Agent-memory comparison: `docs/handoff/2026-10-14/agent-memory/{spec.md, diff-analysis.md}`.
- PRs: #41, #43, #44, #45, #46 merged; #47 open. Issues: #38, #35, #26, #31, #19.
- Agent memory notes for the orchestrator: `~/.claude/projects/-Users-carr-Developments-spec-build-lab/memory/` — `guide-changes-only-what-user-asked.md`, `regen-fable-audit-opus.md`, `diagnose-guide-readings-by-grep.md`, `summary-style-precise-plain-short.md`.
