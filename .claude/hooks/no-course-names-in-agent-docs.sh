#!/bin/bash
# .claude/hooks/no-course-names-in-agent-docs.sh — PreToolUse hook
#
# f(tool_input, list of courses/*/ folder names) → no opinion | ask.
# CLAUDE.md: every document a build agent can read stays course-agnostic.
# A build agent can read anything under .claude/, CLAUDE.md and AGENTS.md,
# so a write there that names a course must be the owner's call.
#   Edit/Write/MultiEdit/NotebookEdit: ask when the target is under .claude/
#     (or is CLAUDE.md/AGENTS.md) and the new text names a course folder.
#   Bash: ask when the command writes into such a target (redirect, sed -i,
#     tee, cp, mv) and the command text names a course folder.
# A course name is a folder under courses/, matched case-insensitively,
# with dashes or spaces. Catches names, not course content written without
# a name; iterate-guide's pre-commit step covers the rest.

input=$(cat)
HOOK_INPUT="$input" python3 - <<'PY'
import json, os, re, sys
try:
    d = json.loads(os.environ.get("HOOK_INPUT", "") or "{}")
except Exception:
    sys.exit(0)
tool = d.get("tool_name", "") or ""
ti = d.get("tool_input") or {}
root = os.environ.get("CLAUDE_PROJECT_DIR") or d.get("cwd") or ""
try:
    names = sorted(n for n in os.listdir(os.path.join(root, "courses"))
                   if not n.startswith(".") and os.path.isdir(os.path.join(root, "courses", n)))
except Exception:
    sys.exit(0)
if not names:
    sys.exit(0)
course = re.compile("|".join(re.escape(n).replace(r"\-", "[- ]") for n in names), re.I)
target = re.compile(r"(\.claude/|(^|/)(CLAUDE|AGENTS)\.md$)")

hit = None
if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
    path = str(ti.get("file_path") or ti.get("notebook_path") or "")
    if target.search(path):
        text = " ".join(str(x) for x in [ti.get("content"), ti.get("new_string"), ti.get("new_source")] if x)
        text += " ".join(str(e.get("new_string", "")) for e in (ti.get("edits") or []) if isinstance(e, dict))
        m = course.search(text)
        hit = m and m.group(0)
elif tool == "Bash":
    cmd = str(ti.get("command") or "")
    writes = re.search(r"(>>?\s*['\"]?\S*(\.claude/|(CLAUDE|AGENTS)\.md))|((\bsed\s+-i|\btee\b|\bcp\b|\bmv\b)[^|;&]*(\.claude/|(CLAUDE|AGENTS)\.md))", cmd)
    if writes:
        m = course.search(cmd)
        hit = m and m.group(0)
if hit:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": f"This writes the course name '{hit}' into a file a build agent can read (under .claude/, or CLAUDE.md/AGENTS.md). "
            "CLAUDE.md requires these documents to stay course-agnostic: course-specific data belongs outside them. Approve only if the owner said so."}}))
sys.exit(0)
PY
