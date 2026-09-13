#!/usr/bin/env bash
# Speech-to-text (single pass) for content-summarizer.
#   OpenRouter `openai/gpt-4o-mini-transcribe` — lightly normalized output is THE base text.
#
# Usage: stt.sh <workdir> [audio-file] [language]
#   audio    default: <workdir>/audio/*.16k.mp3 ; language default: zh
# Output : <workdir>/segments/part_NN.<ext>   (120 s each)
#          <workdir>/stt/part_NN.json         ({text, usage}; no segment timestamps)
# Exit   : 0 = all parts complete, guards clear; 1 = failures/flags (listed).
#
# Do-not-change-casually (hard-won):
#   120 s parts — mini caps output at 2048 tokens (≈10 min of dense Chinese). At 900 s
#                 the tail is dropped SILENTLY (HTTP stays 200; measured cut at 619 s
#                 of 900). 120 s gives ~5x margin and keeps part-start anchors ~2 min.
#   mp3 input   — OpenAI-family providers reject ogg/flac; mp3 works.
#   json only   — mini does not support verbose_json (no segment timestamps).
#   resume-safe — a valid existing part file is skipped, so a rerun resumes.
set -euo pipefail

work="${1:?usage: stt.sh <workdir> [audio-file] [language]}"
audio="${2:-}"
lang="${3:-zh}"

# key: environment first, else ~/.hermes/.env
if [ -z "${OPENROUTER_API_KEY:-}" ] && [ -f "$HOME/.hermes/.env" ]; then
  export $(grep -E '^OPENROUTER_API_KEY=' "$HOME/.hermes/.env" | xargs)
fi
: "${OPENROUTER_API_KEY:?OPENROUTER_API_KEY not found (env or ~/.hermes/.env)}"

if [ -z "$audio" ]; then
  audio="$(find "$work/audio" -maxdepth 1 -name '*.16k.mp3' 2>/dev/null | head -1 || true)"
fi
[ -n "$audio" ] && [ -f "$audio" ] || { echo "ERROR: audio not found — expected <workdir>/audio/*.16k.mp3 or pass arg 2" >&2; exit 1; }
ext="${audio##*.}"

mkdir -p "$work/segments" "$work/stt"

if ! ls "$work/segments"/part_*."$ext" >/dev/null 2>&1; then
  ffmpeg -y -loglevel error -i "$audio" -f segment -segment_time 120 -c copy "$work/segments/part_%02d.$ext"
fi
nparts=$(ls "$work/segments"/part_*."$ext" 2>/dev/null | wc -l || true)
[ "$nparts" -gt 0 ] || { echo "ERROR: segmentation produced no parts" >&2; exit 1; }

valid() {  # $1 file — needs non-empty 'text'
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if (d.get('text') or '').strip() else 1)" "$1" 2>/dev/null
}

for f in "$work/segments"/part_*."$ext"; do
  b=$(basename "$f" ".$ext")
  if ! valid "$work/stt/$b.json"; then
    rm -f "$work/stt/$b.json"
    curl -sf --retry 3 --retry-delay 2 --max-time 600 -o "$work/stt/$b.json" \
      https://openrouter.ai/api/v1/audio/transcriptions \
      -H "Authorization: Bearer $OPENROUTER_API_KEY" \
      -F model=openai/gpt-4o-mini-transcribe -F language="$lang" \
      -F response_format=json -F file=@"$f" || true
    valid "$work/stt/$b.json" || { rm -f "$work/stt/$b.json"; echo "FAIL: $b"; continue; }
  fi
  echo "done $b"
done

# summary + guards (2048-token tripwire, low-text check, cost)
python3 - "$work" "$ext" <<'PY'
import glob, json, os, subprocess, sys

work, ext = sys.argv[1], sys.argv[2]

def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return {}

parts = sorted(glob.glob(f"{work}/segments/part_*.{ext}"))
flags, ok, cost, tok_max = [], 0, 0.0, 0
for p in parts:
    b = os.path.splitext(os.path.basename(p))[0]
    try:
        dur = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", p],
            capture_output=True, text=True).stdout or 0)
    except Exception:
        dur = 0.0
    j = load(f"{work}/stt/{b}.json")
    txt = (j.get("text") or "")
    u = j.get("usage") or {}
    ot = u.get("output_tokens") or 0
    cost += u.get("cost") or 0
    tok_max = max(tok_max, ot)
    if not txt.strip():
        flags.append(f"{b}: no text — rerun this part")
    else:
        ok += 1
        if ot == 2048:
            flags.append(f"{b}: hit the 2048-token output cap — split this window and rerun")
        elif dur and len(txt) < 20 * (dur / 60):
            flags.append(f"{b}: only {len(txt)} chars for {dur:.0f}s — verify coverage")

print(f"parts={len(parts)} | ok={ok} | cost=${cost:.4f} | max output_tokens={tok_max}")
for f in flags:
    print("FLAG:", f)
sys.exit(1 if flags else 0)
PY
