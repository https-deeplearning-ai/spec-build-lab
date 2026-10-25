#!/bin/bash
# .claude/hooks/guide-change-ask.sh — PreToolUse hook
#
# PURE FUNCTION: f(tool_input) → no opinion | ask.
# An edit to the guide-v2 process files must be the owner's decision
# (iterate-guide). Protected:
#   .claude/skills/generate-spec-v2/            (guide, prompts, SKILL.md)
#   .claude/skills/iterate-guide/SKILL.md
#   .claude/skills/iterate-guide/references/    (register, musts, scorer prompt)
# Edit/Write/MultiEdit/NotebookEdit: ask when the target path is protected.
# Bash: ask when output is redirected into a protected path, or the command
# names one AND runs a writer (sed -i, tee, mv, cp, rm, truncate,
# git checkout/restore/apply, perl -i).
# Reads pass. String-based: catches honest mistakes, not obfuscation.

input=$(cat)
HOOK_INPUT="$input" python3 - <<'PY'
import json, os, re, sys
try:
    d = json.loads(os.environ.get("HOOK_INPUT", "") or "{}")
except Exception:
    sys.exit(0)
tool = d.get("tool_name", "") or ""
ti = d.get("tool_input") or {}
prot = re.compile(r"\.claude/skills/(generate-spec-v2/|iterate-guide/(SKILL\.md|references/))")
hit = False
if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
    hit = bool(prot.search(str(ti.get("file_path") or ti.get("notebook_path") or "")))
elif tool == "Bash":
    cmd = str(ti.get("command") or "")
    redirect = re.compile(r">>?\s*['\"]?\S*\.claude/skills/(generate-spec-v2/|iterate-guide/(SKILL\.md|references/))")
    write = re.compile(r"(\bsed\s+-i|\btee\b|\bmv\b|\bcp\b|\brm\b|\btruncate\b|\bgit\s+(checkout|restore|apply)\b|\bperl\s+-p?i)")
    hit = bool(redirect.search(cmd)) or (bool(prot.search(cmd)) and bool(write.search(cmd)))
if hit:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": "This edits the guide-v2 process (generate-spec-v2, or iterate-guide's SKILL.md, register or musts). "
            "Guide changes follow the iterate-guide skill: the owner decides each change. Approve only if the owner has said go for this edit."}}))
sys.exit(0)
PY
