# Independent audit prompt (step 4b of /generate-spec)

Spawn a **fresh general-purpose subagent** (never a fork) on an Opus-class model. Fill
`{SPEC}` (absolute path of the spec under audit) and, for an `--env` generation, `{OVERLAY}`
(absolute path of the overlay rules file); otherwise delete the overlay sentences. Change
nothing else.

```
Read-only audit. Repo: {REPO}. Do not modify any file.

Target: {SPEC}. Audit it fresh against §14 of
{REPO}/.claude/skills/generate-spec/references/spec-generation-guide.md (read §3, §5.5, §6,
§6.0, §8 and §10 too, since §14 refers to them). With an overlay: also audit against the ADD
checklist in {OVERLAY} and its OVERRIDE rules.

Run every check on the whole file, not a sample:
(a) rule↔AC citations: every rule cited by ≥1 AC, every AC cites ≥1 rule, every rule-side
    "→ AC…" list reciprocated and every AC citation present in that rule's list — write a
    small script and paste its counts;
(b) every non-empty Ledger-row Invariant is exercised by an AC or the row says why not;
(c) no bare "(default)" label anywhere;
(d) the §0 gate matches the guide's §6.0 template; no "proceed if no response" escape; one
    question per row; no numeric cap; not keyed on row counts or ids;
(e) no "current best" model name baked into a default or Options cell;
(f) every fixture, script, planted file, test hook and number an AC relies on is declared in §5
    (or wherever the spec declares test hooks) and is arithmetically consistent with the rule
    that defines the asserted verdict — replay every verdict-asserting AC against its fixture;
(g) every cross-reference resolves to the thing it describes (check the target's heading, not
    just that the number exists); no pointer to the guide's or overlay's own sections; every
    provenance term is defined in CTX-C's "How to read the provenance notes" paragraph;
(h) every Ledger row names exactly one buildable default;
(i) the scope-boundary row's four requirements; every Not Included tag is one of the classes
    the row defines AND matches the guide's definition of that class;
(j) the four-way encoding for every CTX-B entry (rule, AC, fixture, CTX);
(k) every Options entry satisfies its own row's Invariant, and no option on one row makes
    another row's Invariant false;
(l) no Options entry is a side the row's own Trade-off says the course warned against;
(m) contract fields vs what ACs assert;
(n) pairwise AC consistency: each AC's Given is true after the AC it builds on;
(o) the provenance header pins the guide commit (and the overlay commit, with an overlay).
(r) the CTX-C trade-off table: every entry the course argues as a builder's choice is dispositioned
    row / bake-in / lever, never `narrative`; every bake-in or lever entry names its tie-breaker; no
    §1 item tagged `restorable` is a side of an entry in this table (§5.5 three dispositions).
    No `lever` entry has a side that is the value at which a component ceases to exist (§5.5 limit-value rule).
With an overlay also: (p) nothing labelled [environment] inside CTX-A or CTX-B; the
Environment Resolutions table accounts for all six dimensions and each row points at a rule
and AC that exercise its invariant, or says "Invariant empty"; the "Adapting this beyond the
lab" note is present; the co-label appears only where both sources require the constraint;
(q) read every Ledger row as the learner who will answer the gate: every Options entry can
    actually be taken in this build mode (no credential the spec forbids asking for; the
    offline suite never waits on a person); no row has only one takeable entry; a course-owned
    row the overlay resolved appears in the Environment Resolutions table with its §2 pin and
    its Not Included entry; no Not Included item tagged owned-by-row points at a row that no
    longer offers it.

Report ONLY defects, each as: check id or checklist line → verbatim quote with line number →
why it fails. Do not suggest rewrites. Classify each HARD (a MUST violated, a mechanical check
failed, a test that cannot pass, or a builder forced to guess) or SOFT (wording or convention).
End with one line: N defects, M hard, K soft.
```

Orchestrator duties: spot-check at least three HARD findings against the file before
repairing (auditors are right far more often than not, but a repair made on a misread costs a
round); never let the repair agent change a decision — Ledger rows, defaults, rule meanings and
AC coverage are the generator's, and a repair that needs one is a guide finding to file, not an
edit to make silently.
