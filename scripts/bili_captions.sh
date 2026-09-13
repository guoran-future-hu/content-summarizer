#!/usr/bin/env bash
# Bilibili captions: check for captions, download them when present.
#
# Usage: bili_captions.sh <URL|BV id> [outdir] [lang]
#   stdout: path to the downloaded .srt        (exit 0)
#           NO_CAPTIONS                        (exit 3 -> go to audio/STT)
#           error message                      (exit 1)
# Needs the cookie jar (AI captions are login-gated): ~/web-auth/bilibili-cookies.txt
# Override lang explicitly as 3rd arg; default picks ai-zh, else the first listed.
set -euo pipefail

url="${1:?usage: bili_captions.sh <URL|BV id> [outdir] [lang]}"
out="${2:-.}"
want_lang="${3:-}"

[[ "$url" =~ ^BV[0-9A-Za-z]+$ ]] && url="https://www.bilibili.com/video/$url"

CK="${BILI_COOKIES:-$HOME/web-auth/bilibili-cookies.txt}"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
hdrs=(--add-header "Referer:https://www.bilibili.com"
      --add-header "Origin:https://www.bilibili.com"
      --add-header "User-Agent:$UA")

mkdir -p "$out"

listing="$(yt-dlp --cookies "$CK" --list-subs --skip-download --no-playlist "${hdrs[@]}" "$url" 2>&1)" || {
  echo "ERROR: caption listing failed - check cookie jar (nav isLogin), headers, yt-dlp version" >&2
  exit 1
}

# Bilibili hides the whole subtitle list from logged-out sessions: an empty
# listing then means "not logged in", NOT "no captions" - never fall through to STT on it.
if printf '%s\n' "$listing" | grep -q 'only available when logged in'; then
  echo "ERROR: not logged in - captions are hidden. Check nav isLogin; re-scan the QR if false (recipes §0)" >&2
  exit 1
fi

langs="$(printf '%s\n' "$listing" \
  | awk '/Available subtitles for /{f=1;next} f&&NF>=2&&$1!="Language"{print $1}' \
  | grep -v '^danmaku$' || true)"

if [ -z "$langs" ]; then
  echo "NO_CAPTIONS"
  exit 3
fi

lang="${want_lang:-$(printf '%s\n' "$langs" | grep -x 'ai-zh' | head -1 || true)}"
[ -n "$lang" ] || lang="$(printf '%s\n' "$langs" | head -1)"
echo "available: $(printf '%s' "$langs" | tr '\n' ' ') | picking: $lang" >&2

yt-dlp --cookies "$CK" --write-subs --sub-lang "$lang" --skip-download --no-playlist \
  "${hdrs[@]}" -o "$out/%(id)s.%(ext)s" "$url" >&2

f="$(find "$out" -maxdepth 1 -name "*.$lang.srt" -type f | head -1)"
[ -n "$f" ] || { echo "ERROR: subtitle file not written (lang '$lang' unavailable?)" >&2; exit 1; }
echo "$f"
