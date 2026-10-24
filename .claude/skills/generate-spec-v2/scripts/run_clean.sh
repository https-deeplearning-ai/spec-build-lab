#!/usr/bin/env bash
# Runs one clean-room agent in an empty folder outside any repo, so Claude Code
# attaches no CLAUDE.md, memory, git status or repo skills to it.
#
#   run_clean.sh <card|generate> <course-dir> <model> <out-file>
#
# The folder holds copies of the guide, the materials (never materials/repo/)
# and, for "generate", pattern.md. The agent's output is copied to <out-file>;
# its final report is printed and saved next to it as <out-file>.report.txt.
set -euo pipefail
TMPDIR=${TMPDIR:-/tmp}

kind=$1 course=$(cd "$2" && pwd) model=$3 out=$4
c=courses/$(basename "$course")
skill=$(cd "$(dirname "$0")/.." && pwd)
case $kind in
  card)     prompt=$skill/references/card-prompt.md;       name=pattern-proposed.md ;;
  generate) prompt=$skill/references/generation-prompt.md; name=spec.md ;;
  *) echo "kind must be card or generate" >&2; exit 2 ;;
esac

room=$(mktemp -d "${TMPDIR%/}/clean-room.XXXXXX")
if git -C "$room" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "refusing: $room is inside a git repo" >&2; exit 1
fi

guide=$room/.claude/skills/generate-spec-v2/references/guide.md
mkdir -p "$(dirname "$guide")" "$room/$c/materials" "$room/out"
cp "$skill/references/guide.md" "$guide"
for d in notebooks transcripts slides; do
  if [ -d "$course/materials/$d" ]; then cp -R "$course/materials/$d" "$room/$c/materials/"; fi
done
if [ "$kind" = generate ]; then
  [ -f "$course/pattern.md" ] || { echo "no pattern.md in $course" >&2; exit 1; }
  cp "$course/pattern.md" "$room/$c/"
fi

sed -e "s#{GUIDE}#$guide#" -e "s#{COURSE_DIR}#$room/$c#" -e "s#{OUT}#$room/out/$name#" \
  "$prompt" > "$room/prompt.md"

(cd "$room" && claude -p "$(cat prompt.md)" --model "$model" \
  --allowedTools "Read,Write,Edit,Glob,Grep,Bash") > "$out.report.txt" 2>&1

[ -f "$room/out/$name" ] || { echo "agent wrote no $name; report: $out.report.txt" >&2; exit 1; }
cp "$room/out/$name" "$out"
cat "$out.report.txt"
echo
echo "clean room: $room"
