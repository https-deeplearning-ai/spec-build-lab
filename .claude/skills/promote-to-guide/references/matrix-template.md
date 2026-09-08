# Matrix template

Create `docs/research/<passname>-matrix.md` from this skeleton. The matrix is
the pass's single source of truth: properties, decisions, rounds, evidence.

```markdown
# <passname> — promotion-pass matrix

**Course:** <course> · **Guide under test:** `<hash>` (updated per round)
**Pass bar:** every property present in every confirmation regen; evidence
labels required on all claims.

## Decision log (Phase 1)

| Candidate | Verdict (promote / keep-local / already-covered / guide-only / routed-out) | Owner decisions attached |
|---|---|---|

## Core properties (carried forward — the guide's standing guarantees)

Copy from the previous pass's matrix; prune only with an owner decision.
| # | Property |
|---|---|

## Pass properties (one per promoted / guide-only item)

| # | Property (checkable, quotable) | Type (content-presence / template-conformance) | Candidate | Known flakiness (drives confirm-N) |
|---|---|---|---|---|

Template-conformance properties (rules changing guide text emitted verbatim
into specs, e.g. the §6.0 gate): score by near-exact comparison of the spec's
emitted section against the template. A pass touching a verbatim template must
UPDATE (never copy forward) the core properties describing that section — log
the update in the decision log.

## Rounds

### Round N (guide `<hash>`; regen(s): <paths>)
| Prop | regen-A | regen-B | Evidence label | Note |
|---|---|---|---|---|
- Failure→fix trace: <property> failed because <rule sentence>; fixed by <edit>.

## Confirmation & adoption

- Confirmation set: N=<n> (raised for known-flaky properties), results: …
- Adoption decision: <adopted regen-X / not adopted> — precondition check: …
- Probes run: <probe → outcome>
```

Conventions:
- **Property wording**: each property must be checkable by quoting spec lines
  ("Ask First contains a deterministic/agent-triggered entry cross-referencing
  the op-split row"), never impressionistic ("gate is clearer").
- **Evidence labels**: [verified] = the orchestrator checked the file;
  [reported] = a subagent's claim only. A confirmation pass may not rest on
  [reported] cells.
- **Keep-local edits are not properties** — regens are expected to lack them.
