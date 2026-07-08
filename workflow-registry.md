# Workflow Registry

This is acquisition rules shared by many agents and machiens. Keep local specific workarounds in `./LOCAL_ENVIRONMENT.md`.

Run helper commands from the skill root, or replace `./scripts/` with the absolute path to this skill's `scripts` directory. Replace `<summary-root>` with the user's output folder, usually `./content-summary` in the active workspace, and replace `<source-folder>` before running a command.

## Default

Source order:

1. Official transcript/source text
2. Official captions
3. Platform transcript
4. Community captions
5. Auto captions
6. Speech-to-text

Prefer free, local, official, platform-native methods. Ask before paid APIs/services. Mark poor source quality.

Web pages: use the `defuddle` skill, including official transcript pages.

PDFs: use the `pdf2md` skill. For arXiv, prefer HTML when available.

Local files: if already in the right `<summary-root>` folder, summarize in place; otherwise copy first.

Video speech-to-text: when transcripts are unavailable and the workflow reaches STT, run two independent API transcripts:

1. Groq `whisper-large-v3-turbo`.
2. OpenRouter `openai/gpt-4o-mini-transcribe`.

Prefer local models if availalbe, otherwise use web API.

Compare both outputs before summarizing. Merge them into one unified transcript, preferring agreement and resolving uncertain passages. Save the two raw transcripts plus the merged transcript in the source folder. Move to summarization only after the merged transcript exists. If the merged transcript is too long, start a fresh LLM session for the summarization step.

---

## Ones and Tooze

**Source:** @Foreign-Policy YouTube playlist `PLYRt3SPnw6gzpIl6aE325N8QxJ6ejlJVU`

```bash
python -m yt_dlp --flat-playlist --dump-json "<playlist_url>"
python -m yt_dlp --write-auto-subs --sub-lang en --skip-download -o "<summary-root>/ones-and-tooze-economics/<slug>.%(ext)s" "https://www.youtube.com/watch?v=<id>"
```

**Transcript:** YouTube auto-subs; clean VTT; check Tooze/Cam speaker errors.
**Fallback:** `defuddle` skill on FP page for episode metadata.
**Folder:** `<summary-root>/ones-and-tooze-economics/`
**Naming:** `YYYY-MM-DD-<slug>-(Plus-<topic>)-Ep<NNN>.md`

---

## Lex Fridman

**Source:** `lexfridman.com`, @lexfridman YouTube playlist `PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4`
**Discovery:** RSS `lexfridman.com/feed/podcast/` or yt-dlp flat playlist.
**Episode page:** `defuddle` skill on `https://lexfridman.com/<guest-slug>`.
**Folder:** `<summary-root>/lex-fridman/`
**Naming:** `YYYY-MM-DD-<guest-slug>-<descriptive>-transcript.md`

Acquisition:

1. `defuddle` skill on `https://lexfridman.com/<guest-slug>-transcript`
2. Fallback parser: `python ./scripts/lex_fridman_transcript_parse.py <guest-slug> -o <summary-root>/<source-folder>/transcript.md`
3. Manual YouTube subtitles:
   ```bash
   python -m yt_dlp --write-subs --sub-lang en --skip-download -o "<summary-root>/<source-folder>/<guest-slug>.%(ext)s" "<youtube-url>"
   ```
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
**Folder:** `<summary-root>/latent-space/`

---

## Lyn Alden Investment Report

**Source:** report text supplied by user or workspace
**Acquisition:** preserve report body, headings, tables, chart captions, source links. Remove email/web chrome.
**Folder:** `<summary-root>/lyn-alden-investment-report/`
**Naming:** replace the title date with filename prefix, e.g. `2026-06-05-the-wild-west.md`.

---

## Academic Papers

**Acquisition:** official/arXiv HTML first; `pdf2md` for PDF-only.
**Cleanup:** preserve sections, equations, tables, figures/captions, appendix refs, citation context. Remove conversion artifacts.
**Folder:** existing paper/source collection or new kebab-case folder.
**Naming:** `<title-slug>-<year>.md`

---

## Bilibili

**Source:** Bilibili URL or BV id
**Acquisition:** subtitles first. Otherwise:

```bash
python ./scripts/bili_download.py --url "BV id or full URL" --output <summary-root>/<source-folder>/audio --mp3
```

Transcribe using the default dual-STT policy. Use `response_format=text`; start with `language=zh` for Chinese. Flag proper-noun errors in transcript quality.

**Folder:** `<summary-root>/bilibili-<BVid>/` or source-specific folder.

---

## Wang Xiao Monthly Review

**Source:** Bilibili titles like `一条视频看X月`
**Acquisition:** Bilibili entry.
**Folder:** existing Wang Xiao folder or new kebab-case folder.
**Naming:** `YYYY-MM-DD-monthly-review.md`; date from video publish date.
