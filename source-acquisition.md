# Source Acquisition

Shared by many agents and machines; local workarounds go in `./LOCAL_ENVIRONMENT.md`.

Run commands from the skill root (or use the absolute `scripts/` path). `<summary-root>` = user's output folder; `<source-folder>` = per-source subfolder.


## Source order

1. Official transcript
2. Platform Auto transcript
3. Speech-to-text — audio/video only

Ask before paid APIs/services. Mark poor source quality.


## Text sources

If text sources (articles, reports, papers) are available:

- Web pages: use the `defuddle` skill.
- PDFs: use the `pdf2md` skill. For arXiv, prefer HTML when available.

You can safely ignore the rest.


## Audio and video sources

Captions/transcripts first when they exist; speech-to-text is the fallback:

```bash
./scripts/stt.sh <summary-root>/<source-folder>   # 120 s parts, resume-safe, guards; keys from env/.env; read the script header before changing anything
```

- Single pass: OpenRouter `openai/gpt-4o-mini-transcribe` — lightly normalized output is the base text (`stt/part_NN.json`; ~$0.09–0.13/audio-hour). No segment timestamps; `transcript.md` anchors each part's start (~2 min grid).
- Join + validate: `./scripts/make_transcript.py <summary-root>/<source-folder>` — STT parts or a captions `.srt` (auto-detected; `--srt FILE` to force) → `transcript.md`.
- Normalize after joining (mangled names straddle segments); apply decided fixes with `./scripts/apply_replacements.py transcript.md pairs.txt --table normalization.md` (counts table). Summarize only after the transcript file exists; a very long transcript may need a fresh session.

---

## Ones and Tooze

**Source:** @Foreign-Policy YouTube playlist `PLYRt3SPnw6gzpIl6aE325N8QxJ6ejlJVU`

```bash
python -m yt_dlp --flat-playlist --dump-json "<playlist_url>"
python -m yt_dlp --write-auto-subs --sub-lang en --skip-download -o "<summary-root>/ones-and-tooze-economics/<slug>.%(ext)s" "https://www.youtube.com/watch?v=<id>"
```

**Transcript:** YouTube auto-subs; clean VTT; check Tooze/Cam speaker errors.
**Fallback:** `defuddle` skill on FP page for episode metadata.

---

## Lex Fridman

**Source:** `lexfridman.com`, @lexfridman YouTube playlist `PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4`
**Discovery:** RSS `lexfridman.com/feed/podcast/` or yt-dlp flat playlist.
**Episode page:** `defuddle` skill on `https://lexfridman.com/<guest-slug>`.

Acquisition:

1. `defuddle` skill on `https://lexfridman.com/<guest-slug>-transcript`
2. Fallback parser: `python ./scripts/lex_fridman_transcript_parse.py <guest-slug> -o <summary-root>/<source-folder>/transcript.md`
3. Manual YouTube subtitles: `python -m yt_dlp --write-subs --sub-lang en --skip-download -o "<summary-root>/<source-folder>/<guest-slug>.%(ext)s" "<youtube-url>"`
4. Auto YouTube subtitles:
   ```bash
   python -m yt_dlp --write-auto-subs --sub-lang en --skip-download -o "<summary-root>/<source-folder>/<guest-slug>.%(ext)s" "<youtube-url>"
   python ./scripts/clean_vtt_subtitles.py <summary-root>/<source-folder>/<guest-slug>.en.vtt <summary-root>/<source-folder>/transcript.md
   ```

---

## Latent Space

**Source:** Substack email transcript
**Acquisition:** convert `.eml` with `eml-to-md` in the active project/agent environment.
**Fallback:** package Python API when CLI path handling fails.
**Cleanup:** strip newsletter header/footer.

---

## Lyn Alden Investment Report

**Source:** report text supplied by user or workspace
**Acquisition:** preserve report body, headings, tables, chart captions, source links. Remove email/web chrome.

---

## Bilibili

**Source:** Bilibili URL / BV id
**Recipe:** `./references/bilibili-recipes.md` — login cookies §0, exit codes, 多P, premium.

```bash
./scripts/bili_captions.sh <url> <source-folder>   # exit 3 = NO_CAPTIONS -> run next line
./scripts/bili_audio.sh    <url> <source-folder>   # -> <source-folder>/audio/<ID>.16k.mp3
./scripts/stt.sh   <source-folder>                 # language=zh default
```
