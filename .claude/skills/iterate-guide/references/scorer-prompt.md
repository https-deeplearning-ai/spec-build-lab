You are scoring one generated spec against fixed properties. Read only the file spec.md in the current folder. Do not read anything else, run no git, ask no one.

The spec contains a list of questions for the learner (usually headed "Questions", items C1, C2, ...), each with options; one option per question is marked "Recommended". The "recommended build" is the build you get by taking every Recommended option.

{MUSTS}

Score each property PASS or FAIL, with a one-line reason quoting the spec (question id and option text).

Output ONLY a JSON object on the last line, nothing after it, with one key per property id above and the value "PASS" or "FAIL", e.g. {"M1":"PASS","M2":"FAIL"}.
Before the JSON, give the one-line reasons.
