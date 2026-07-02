# Workflow Registry

Each entry covers: how to discover new episodes, the preferred transcript acquisition method (tiered by quality), cleanup steps, file naming conventions, and fallback strategies.

---

## Ones and Tooze (`foreignpolicy.com` → YouTube)

**Source:** @Foreign-Policy YouTube channel
**Playlist:** `PLYRt3SPnw6gzpIl6aE325N8QxJ6ejlJVU`

```bash
# List latest episodes
python -m yt_dlp --flat-playlist --dump-json "<playlist_url>"

# Download auto-subs
python -m yt_dlp --write-auto-subs --sub-lang en --skip-download -o "<out>.%(ext)s" "https://www.youtube.com/watch?v=<id>"
```

**New episode check:** compare latest `id` vs `ones-and-tooze_last_episode_id.txt`
**Transcript:** auto-subs, ~400KB VTT → ~43KB clean. Name errors: "Adam Tus" → Tooze, "Kim" → Cam.
**Fallback:** `web_fetch` FP podcast page (titles only, no transcript)
**Folder:** `content-summary\ones-and-tooze-economics\`
**Naming:** `YYYY-MM-DD-<slug>-(Plus-<topic>)-Ep<NNN>.md`

---

## Lex Fridman (`lexfridman.com`)

**YouTube:** @lexfridman, playlist `PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4`. All episodes have YouTube videos.
**Discovery:** RSS `lexfridman.com/feed/podcast/` or yt-dlp `--flat-playlist --dump-json`.
**Episode page:** `web_fetch lexfridman.com/<guest-slug>` gives timestamps outline (~3KB).
**Folder:** `content-summary\lex-fridman-podcast\`
**Naming:** `YYYY-MM-DD-<guest-slug>-<descriptive>-transcript.md` and `...-summary.md`

### Transcript tiers (try in order)

**Tier 1 — Official transcript page** (episodes ~2023+):
```bash
python scripts/lex_fridman_transcript_parse.py <guest-slug> -o transcript.md
```
Downloads `lexfridman.com/<slug>-transcript` raw HTML, parses with Python `HTMLParser` → clean markdown with speaker labels, section headings, timestamps. ~135KB output.

**Tier 2 — Manual YouTube subtitles** (rare but clean):
```bash
python -m yt_dlp --write-subs --sub-lang en --skip-download -o "<out>.%(ext)s" "<youtube-url>"
```
~190KB VTT, cleaner than auto-subs (no inline timestamps in text). Some episodes have them, most don't.

**Tier 3 — YouTube auto-generated subtitles** (always available, lowest quality):
```bash
python -m yt_dlp --write-auto-subs --sub-lang en --skip-download -o "<out>" "<youtube-url>"
# Then clean:
python scripts/clean_vtt_subtitles.py <out>.en.vtt transcript.md
```
~1.5MB VTT → ~160KB plain text after cleaning. No speaker labels, typical auto-sub word errors. Use `clean_vtt_subtitles.py` (in this skill directory) — strips `<c>` tags, inline timestamps, deduplicates.

---

## Latent Space (Substack → Email `.eml`)

**Source:** email newsletter with verbatim transcript

```bash
pip install eml-to-md
eml2md message.eml --stdout > transcript.md
```

**Gotcha:** em dashes in filename break CLI on Windows. Use Python API instead:
```python
import eml_to_md, glob
files = glob.glob(r'path/*.eml')
md = eml_to_md.convert(files[0])
open('output.md', 'w', encoding='utf-8').write(md)
```

**Cleanup:** strip ~17% newsletter header/footer — find "Transcript" heading → extract to end (before Copyright / Unsubscribe).
**Quality:** verbatim, speaker-labeled, per-line timestamps. Zero token cost to extract.
**Folder:** `content-summary\latent-space\`

---

## Bilibili (`bilibili.com` — local downloader → Groq Whisper)

**Source:** Bilibili video URL or BV id.

### Acquisition
```powershell
& "C:\Users\i2754\.qclaw\.venv\Scripts\python.exe" `
  scripts/bili_download.py `
  --url "BV id or full URL" -f 30232 --whisper
```
- Downloads m4a audio + converts to 16 kHz mono wav (`*_16k_mono.wav`).
- No cookies needed — B站 412 is a missing Referer/Origin header issue, not login. Script handles it.
- Highest accessible bitrate for non-members: ~143 kbps AAC.

**Audio quality:** for speech/podcast content, prefer ~94 kbps (`-f 30232`). Use `--list` / `-F` to inspect before choosing; use highest bitrate for music.

### Transcription (Groq Whisper)
1. Split `*_16k_mono.wav` into ≤15 MB chunks (~8 min each) to stay under Groq's 25 MB limit:
   ```powershell
   ffmpeg -i input_16k_mono.wav -f segment -segment_time 500 -c copy chunk_%02d.wav
   ```
2. Transcribe each chunk with Windows native `curl.exe` (not PowerShell `curl` alias, not Python `requests`):
   ```powershell
   C:\Windows\System32\curl.exe -s -X POST https://api.groq.com/openai/v1/audio/transcriptions `
     -H "Authorization: Bearer $env:GROQ_API_KEY" `
     -F "file=@chunk_00.wav;type=audio/wav" `
     -F "model=whisper-large-v3-turbo" `
     -F "response_format=text"
   ```
3. Merge chunks in order into `transcript.txt`.

**Known issues:** whisper mishears rare English proper nouns (Anthropic → Enferpik, Claude → Cloud, Frontier Models → Fable 5). GPT post-processing fixes this. `verbose_json` gives timestamps but does not improve text quality.

**GFW note:** Groq + curl schannel works. OpenRouter and Python `requests` are blocked (TLS SNI RST).

**Folder:** choose or create a source-specific folder under `content-summary\`.

---

## Built-in Tools

| Tool | Location | Purpose |
|---|---|---|
| `bili_download.py` | `scripts/` | Bilibili audio download + 16 kHz mono WAV conversion |
| `lex_fridman_transcript_parse.py` | `scripts/` | LF official transcript download + HTML→MD parse |
| `clean_vtt_subtitles.py` | `scripts/` | YouTube auto-sub VTT→plain text (any source, not just LF) |
| `eml-to-md` (pip) | — | Substack `.eml` → markdown for Latent Space |
