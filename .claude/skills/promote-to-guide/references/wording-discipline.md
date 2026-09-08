# Wording discipline for guide rules

Every rule leak in the founding pass (guide-pins-v2, 3 convergence rounds)
traced to violating one of these three rules. Read this before writing or
fixing any guide rule.

## 1. State WHEN a criterion is evaluated

A test without a timing anchor gets evaluated at whatever moment makes it
easiest to satisfy — or hardest, unpredictably.

**Observed leak:** Rule A's stakes test asked "would choosing the other side
force rework?" Both regen agents evaluated it at *change-after-data* time,
where nearly everything forces rework — so nothing ever demoted, and the
distance lever became a Ledger row in both. **Fix that worked:** "evaluated at
initial choice time — before any build artifact exists; the cost of changing
the value later is §6's business and never grounds for a row."

Checklist: does every conditional in your rule say *when* its condition is
judged, and from *whose* position?

## 2. Anchor to existing guide concepts, not to facts of one course

A rule keyed to what happens to be true of the current course (its stack, its
scale, its store names) breaks on the next course — and same-course regens
will never catch it.

**Observed leak:** the substitute-tier ladder assumed "stdlib can satisfy the
contracts" (true for agent-memory's SQLite case, not in general). **Fix that
worked:** anchor the fidelity guard to the row's **Invariant** — "when the
taught pattern genuinely requires a capability a lower tier lacks, that
capability belongs in the Invariant, which then excludes the tier" — so each
course's own invariant does the guarding, not the rule's assumptions.

Checklist: could a course with a different stack, scale, or domain read this
rule and reach a wrong-but-literal conclusion? Name the existing guide concept
(Invariant, contract, mined trade-off list, declared default scale) that
carries the judgment instead.

## 3. Audits reference rules; they never restate mechanics

A §14 checklist line that re-lists a rule's taxonomy or criteria creates a
second copy that drifts from the first — the same copies-drift failure the
guide's own "no cross-row restating" rule exists to prevent.

**Observed leak (caught in review):** a checklist line re-enumerating the tier
taxonomy "(standard distribution / embedded / locally served)". **Fix:**
"a branch-1 substitution's default note shows how 'lightest' was determined
(§3)" — the audit checks that the rule was followed, by reference.

Checklist: does the audit line contain any criterion, list, or label that also
appears in the rule? Move it out; cite the section instead.

## Two more habits that prevented leaks

- **Close every route.** When a rule forbids something, ask: can the same
  outcome re-enter through a sibling rule's door? (The tool-exposure row
  re-entered through three different §5.5 routes across three rounds; the
  durable fix was a precondition above all routes — "no route admits a
  non-decision".) Prefer one principle above the forks over patching forks
  one at a time — but expect to discover the need for it by iteration.
- **A degenerate case is not a second option.** If an "alternative" is just
  the taught mechanism's behavior on a trivial workload, it is not a choice
  and must not count as one.
