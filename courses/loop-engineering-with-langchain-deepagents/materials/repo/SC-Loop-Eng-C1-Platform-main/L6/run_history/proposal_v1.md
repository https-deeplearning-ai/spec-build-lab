# Proposal

## Summary signal

`/v1/summary.json` shows first-attempt failures for the same two criteria in every run:

- clarity: 0/5 passed
- depth: 0/5 passed
- completeness: 5/5 passed

This points to a systematic instruction gap in how the agent formats ambiguity bullets, not a problem with coverage of requirement clauses.

## Current instruction gap

`/v1/AGENTS.md` tells the agent to write ambiguity bullets with only the quoted clause and a `Reason:` line:

```md
- **"the exact clause"**
  Reason: why it is under-specified
```

The rubric expected each ambiguity bullet to also include indented `Resolved by:` and `Edge case:` lines. Because the prompt never asked for those labels, every first attempt omitted them and every run required the same correction.

## Evidence across runs

- Run 1: "The analysis covers the requirement document and includes ambiguity bullets, but each ambiguity bullet is missing the required indented 'Resolved by:' line and 'Edge case:' line."
- Run 2: "The analysis covers the requirement document, but the Ambiguities section lacks the required indented \"Resolved by:\" and \"Edge case:\" lines for each ambiguity bullet."
- Run 3: "the Ambiguities section is missing the required indented 'Resolved by:' lines and 'Edge case:' lines for each ambiguity bullet."
- Run 4: "Each ambiguity needs an indented \"Resolved by:\" line and an indented \"Edge case:\" line; instead, the file uses \"Reason:\" lines and lacks edge-case failure descriptions."
- Run 5: "the Ambiguities section does not contain the required indented 'Resolved by:' and 'Edge case:' lines for each bullet."

## Proposed insertion

Add the following under `### Ambiguities` in `/v1/AGENTS.md`:

```md
For every ambiguity bullet, include two additional indented labelled lines after `Reason:`:

```
  Resolved by: the specific fact or decision that would settle the ambiguity
  Edge case: a concrete production failure that could happen if the ambiguity remains unresolved
```
```

## Rejected observations

- Some runs produced duplicate `## Assumptions` headings or edit-file ambiguity errors, but these were not the failing rubric criteria and were not the same required grader correction in all five runs.
