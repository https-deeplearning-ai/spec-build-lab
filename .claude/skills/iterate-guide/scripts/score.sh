#!/usr/bin/env bash
# score.sh <musts-file> <spec.md> <result.json> : blind-score one spec against a course's musts.
# The scorer is `claude -p` on Opus in an empty temporary folder holding only the spec, so it sees no
# repo, run name or setup. Its reasons go to <result.json>.txt; the last line (the JSON) to <result.json>.
set -euo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
musts=$(sed -n '/<!-- MUSTS -->/,/<!-- \/MUSTS -->/p' "$1" | sed '1d;$d')
[ -n "$musts" ] || { echo "no <!-- MUSTS --> block in $1" >&2; exit 1; }
room=$(mktemp -d "${TMPDIR:-/tmp}/score.XXXXXX"); cp "$2" "$room/spec.md"
prompt=$(MUSTS="$musts" python3 -c 'import os,sys; print(open(sys.argv[1]).read().replace("{MUSTS}", os.environ["MUSTS"]))' "$here/references/scorer-prompt.md")
(cd "$room" && claude -p "$prompt" --model opus --allowedTools "Read" > "$3.txt" 2>&1)
tail -1 "$3.txt" > "$3"
rm -rf "$room"
