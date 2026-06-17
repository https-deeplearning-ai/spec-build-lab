#!/bin/bash
# .claude/hooks/no-materials-during-build.sh — PreToolUse hook
#
# PURE FUNCTION: f(cwd, tool_input) → allow|deny.
# No file reads, no file writes, no global coordination state.
#
# Logic:
#   1. If cwd is NOT inside courses/<name>/builds/run-NN/, allow (exit 0).
#      This is the only context where the prohibition applies.
#   2. If the tool target path mentions materials/, deny (exit 2 with
#      decision JSON on stderr). The build agent must not consume course
#      materials — see CLAUDE.md "Materials are off-limits during a build".
#   3. Otherwise, allow.
#
# Pattern matching is intentionally string-based: catches honest mistakes,
# not adversarial obfuscation. Acceptable for a research lab.

set -euo pipefail

input=$(cat)

# Extract cwd, tool_name, and the candidate "target" path from tool_input.
# tool_input keys vary by tool: file_path (Read/Write/Edit), pattern (Grep),
# path (Glob), command (Bash). Try each.
read -r cwd tool target < <(
  HOOK_INPUT="$input" python3 - <<'PY'
import json, os, sys
try:
    d = json.loads(os.environ.get("HOOK_INPUT", "") or "{}")
except Exception:
    d = {}
cwd = d.get("cwd", "") or ""
tool = d.get("tool_name", "") or ""
ti = d.get("tool_input") or {}
target = ""
if isinstance(ti, dict):
    target = (
        ti.get("file_path")
        or ti.get("path")
        or ti.get("pattern")
        or ti.get("command")
        or ""
    )
# Single-line, whitespace-collapsed for shell read
def s(v):
    return str(v).replace("\n", " ").replace("\t", " ").strip() or "-"
print(s(cwd), s(tool), s(target))
PY
)

# 1. Only fire when the agent is inside a build folder.
case "$cwd" in
  */courses/*/builds/run-*) ;;
  *) exit 0 ;;
esac

# 2. Deny anything that touches a materials/ path.
case "$target" in
  *courses/*/materials/*|*../materials/*|*/materials/*|materials/*)
    python3 - <<'PY' >&2
import json
print(json.dumps({
  "decision": "deny",
  "reason": (
    "Build agent may not read course materials from inside a build folder. "
    "The build must be a function of spec.md only — see CLAUDE.md "
    "\"Materials are off-limits during a build\"."
  ),
}))
PY
    exit 2
    ;;
esac

# 3. Allow.
exit 0
