#!/usr/bin/env bash
# Bilibili audio -> 16 kHz mono mp3 (STT input).
#
# Usage: bili_audio.sh <URL|BV id> [workdir]      (audio lands in <workdir>/audio/)
#   stdout: path to <workdir>/audio/<ID>.16k.mp3  (exit 0)
#   stderr: progress + errors                     (exit 1)
# Steps: format probe (fails fast on 412/region/parse errors) -> resumable download
#        -> 16 k mono mp3 -> duration check vs metadata. Re-running with the output
#        already complete is a no-op. Public audio needs no login; for premium-only
#        videos: BILI_COOKIES=~/web-auth/bilibili-cookies.txt. Multi-part: BILI_PART=N.
set -euo pipefail

url="${1:?usage: bili_audio.sh <URL|BV id> [workdir]}"
work="${2:-.}"

[[ "$url" =~ ^BV[0-9A-Za-z]+$ ]] && url="https://www.bilibili.com/video/$url"

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
hdrs=(--add-header "Referer:https://www.bilibili.com"
      --add-header "Origin:https://www.bilibili.com"
      --add-header "User-Agent:$UA")
ck=(); [ -n "${BILI_COOKIES:-}" ] && ck=(--cookies "$BILI_COOKIES")
sel=(--no-playlist); [ -n "${BILI_PART:-}" ] && sel=(--playlist-items "$BILI_PART")

mkdir -p "$work/audio"

probe="$(yt-dlp --no-warnings --simulate -f "30216/30232/30280/ba" \
  --print "%(id)s|%(duration)s|%(format_id)s" "${ck[@]}" "${hdrs[@]}" "${sel[@]}" "$url")" || {
  echo "ERROR: preflight failed - headers/region/format, or yt-dlp outdated (update it first)" >&2
  exit 1
}
IFS='|' read -r id dur fid <<<"$probe"
echo "preflight ok: id=$id duration=$dur format=$fid" >&2

out="$work/audio/$id.16k.mp3"
src=""

dur_ok() {  # $1: file - within 1%+2s of the metadata duration
  local a
  a="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$1" 2>/dev/null || true)"
  [ -n "$a" ] || return 1
  case "$dur" in ''|NA|None) return 0;; esac
  awk -v e="$dur" -v a="$a" 'BEGIN{ d=a-e; if (d<0) d=-d; exit !(d <= e*0.01+2) }'
}

pick_src() {
  src=""
  for e in m4a webm mp4 opus mp3; do
    [ -f "$work/audio/$id.$e" ] || continue
    src="$work/audio/$id.$e"; break
  done
}

download() {
  yt-dlp --no-warnings --newline --no-playlist -c \
    -f "30216/30232/30280/ba" --socket-timeout 20 --retries 10 \
    "${ck[@]}" "${hdrs[@]}" "${sel[@]}" \
    -o "$work/audio/%(id)s.%(ext)s" "$url" >&2
  pick_src
  [ -n "$src" ] || { echo "ERROR: download produced no audio file" >&2; exit 1; }
}

convert() {
  ffmpeg -y -loglevel error -i "$src" -vn -ac 1 -ar 16000 -b:a 48k "$out"
  dur_ok "$out"
}

if [ -s "$out" ] && dur_ok "$out"; then
  echo "already complete" >&2
  echo "$out"; exit 0
fi

pick_src
[ -n "$src" ] || download

if ! convert; then
  echo "stale or truncated local file - refetching" >&2
  rm -f "$work/audio/$id".*
  download
  convert || { echo "ERROR: duration mismatch vs ${dur}s after refetch - check the source video" >&2; exit 1; }
fi

echo "$out"
