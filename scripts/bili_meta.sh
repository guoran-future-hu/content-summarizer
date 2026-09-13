#!/usr/bin/env bash
# Bilibili video metadata -> <workdir>/meta.json (+ stdout). For the raw header.
#
# Usage: bili_meta.sh <URL|BV id> [workdir]      (BILI_PART=N as in bili_audio.sh)
# Fields: id, title, uploader, upload_date, duration, duration_hms, webpage_url.
set -euo pipefail

url="${1:?usage: bili_meta.sh <URL|BV id> [workdir]}"
work="${2:-.}"

[[ "$url" =~ ^BV[0-9A-Za-z]+$ ]] && url="https://www.bilibili.com/video/$url"

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
hdrs=(--add-header "Referer:https://www.bilibili.com"
      --add-header "Origin:https://www.bilibili.com"
      --add-header "User-Agent:$UA")
sel=(--no-playlist); [ -n "${BILI_PART:-}" ] && sel=(--playlist-items "$BILI_PART")

mkdir -p "$work"
yt-dlp --no-warnings --skip-download "${hdrs[@]}" "${sel[@]}" -J "$url" \
| python3 -c '
import json, sys
j = json.load(sys.stdin)
d = {k: j.get(k) for k in ("id", "title", "uploader", "upload_date", "duration", "webpage_url")}
ud = d.get("upload_date") or ""
d["upload_date"] = f"{ud[:4]}-{ud[4:6]}-{ud[6:8]}" if len(ud) == 8 else ud
t = int(d.get("duration") or 0)
d["duration_hms"] = f"{t//3600:d}:{t%3600//60:02d}:{t%60:02d}" if t else None
open(sys.argv[1], "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
print(json.dumps(d, ensure_ascii=False, indent=2))
' "$work/meta.json"
echo "-> $work/meta.json" >&2
