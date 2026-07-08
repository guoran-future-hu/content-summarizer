---
name: content-summarizer
description: Use when converting podcasts, videos, audio, transcripts, articles, papers, PDFs, Markdown files, pasted text, or other long-form source material into durable educational notes. Covers source acquisition, raw-source preservation, local `content-summary` filing, and four-layer notes that preserve reasoning, evidence, confidence, scope, and useful detail while compressing away low-value transcript or prose clutter.
---

# Long-Form Source -> Educational Notes Skill

## Operating Posture

Act as a source-faithful learning-note editor. Reduce reading effort while preserving the author's structure of thought: claims, evidence, mechanisms, assumptions, uncertainty, scope, and practical implications. The notes should feel like a cleaner, compressed study version of the source, not a review, critique, translation, or new essay.

## Workflow

1. Identify the source type and original publication metadata.
2. Check `workflow-registry.md` for source-specific acquisition, cleanup, and naming guidance.
3. Acquire the best available transcript or source text.
4. Save the raw/source material under `./content-summary/<source-folder>/`.
5. Clean only mechanical artifacts: VTT markup, duplicated captions, newsletter boilerplate, PDF conversion artifacts, or HTML clutter.
6. Write the four-layer notes beside the raw/source file with a `-summary` suffix.
7. Run the compression check and tighten the notes before finishing if they are too close to the source length.
8. Delete temporary staging files, including any temporary Layer 3 file used for byte checks.
9. Update `workflow-registry.md` only when a reusable acquisition method, fallback, or source-specific failure case was discovered.

## Source Acquisition

Prefer sources in this order:

1. Official human transcript or source text
2. Official captions/subtitles
3. Platform-native transcript
4. Community captions
5. Auto-generated captions
6. Speech-to-text transcription (local downloader for Bilibili sources; Groq Whisper for general audio)

Prefer free, local, official, or platform-native methods. Ask before using paid APIs or paid external services. When transcript quality is poor, clean obvious mechanical errors and mark reliability concerns in metadata rather than filling gaps.

For PDFs, use the `pdf-to-markdown` skill first, then summarize the resulting Markdown. For arXiv papers, prefer the arXiv HTML page when available because it usually produces cleaner Markdown than PDF conversion.

### Bilibili Audio Acquisition

For Bilibili videos, see `workflow-registry.md` → Bilibili for the full download → chunk → transcribe pipeline. Quick start:

```powershell
& "C:\Users\i2754\.qclaw\.venv\Scripts\python.exe" `
  scripts/bili_download.py `
  --url "BV id or full URL" --whisper
```

File the merged transcript under `content-summary/<source-folder>/` before writing the four-layer notes.

## Filing and Naming

Save final outputs under `./content-summary/`, organized by source. Use existing source folders when possible, including:

- `./content-summary/lyn-alden-investment-report/`
- `./content-summary/latent-space/`
- `./content-summary/ones-and-tooze-economics/`

Create new source folders in descriptive kebab-case. Preserve the raw/source file because it is the ground truth for future re-summarization.

### Default Names

Use publication date, not processing date, for date-prefixed material:

- Raw/source: `YYYY-MM-DD-<title>.md`
- Summary: `YYYY-MM-DD-<title>-summary.md`

Derive `<title>` from the source title, convert spaces to hyphens, and keep filenames ASCII-only. If the user provides an `.md` file or transcript already inside the correct `content-summary` folder, use it in place and save the summary beside it. If it is outside `content-summary`, copy it into the right source folder before summarizing.

### Source-Specific Names

Use these exceptions when they match existing library conventions:

- Lyn Alden Investment Report: replace the date in the title with the filename prefix, e.g. `2026-06-05-the-wild-west.md`.
- Ones and Tooze: `YYYY-MM-DD-<descriptive-slug>-(Plus-<secondary-topic>)-Ep<NNN>.md`; keep `(Plus: ...)` but replace `: ` with `-`.
- Academic papers: `<title-slug>-<year>.md` and `<title-slug>-<year>-summary.md`; use the metadata year at the end so papers sort by topic, then year.
- Wang Xiao monthly review (Bilibili, titles like "一条视频看X月"): `YYYY-MM-DD-monthly-review.md` and `YYYY-MM-DD-monthly-review-summary.md`. Derive the date from the video publish date, not processing date.

## Language and Encoding

The summary language should match the source's primary language:

Use UTF-8 for Markdown body content. Keep filenames and other infrastructure identifiers ASCII-only.

## Output Contract

Always produce four layers. Use formatting only when it improves scanability.

### 1. High-Level Abstract

Write 3-4 sentences, about 80-120 words. Name the topic, central question or thesis, and broad structure. Keep this layer index-card sized.

### 2. Structured Outline

Create a table of contents for scanning. Each entry is one heading plus one short sentence, max about 20 words. Collapse low-value or similar sections into broader headings. Use timestamps only when directly available.

### 3. Educational Reading Notes

This is the main layer. Rewrite the source into clear, navigable notes while preserving the user's interpretive work.

Preserve:

- Definitions, frameworks, mental models, and technical details
- Reasoning chains, causal mechanisms, assumptions, and evidence
- Caveats, disagreements, limitations, exceptions, null results, and trade-offs
- Claim posture: observation, experiment, theory, speculation, forecast, interpretation, or prescription
- Useful examples when they clarify the argument

Compress according to information density. Dense scripted explainers and papers can keep more structure and detail; rambling conversations should be cut aggressively. Remove filler, repeated statements, casual chatter, jokes, verbal padding, and low-information anecdotes.

### 4. Key Takeaways

Distill the source's core conclusions, strongest arguments, practical implications, and ideas worth remembering. Keep findings, mechanisms, implications, recommendations, and boundaries distinct instead of flattening them into generic advice.

## Fidelity, Attribution, and Confidence

Default to clean source-grounded prose. Attribute only when speaker identity or author framing changes interpretation, such as disagreement, expertise, disputed claims, forecasts, or clearly personal analysis.

Preserve the source's confidence level. Keep hedges such as "probably," "might," "very likely," "I estimate," "in my view," etc. Mark unclear transcript passages or weak source quality instead of upgrading uncertain claims.

For controversial or interpretive claims, signal the frame once at the section or paragraph level rather than repeating attribution sentence by sentence. Use direct quotes sparingly, only for precise or memorable wording.

## Output Template

```md
# <Content Title>

## Metadata
- Source:
- Author / Speakers:
- Date:
- Duration / Type:
- Transcript Quality:

---

# High-Level Abstract

...

---

# Structured Outline

## 1. Topic Title [timestamp if available]
One short sentence.

## 2. Topic Title [timestamp if available]
One short sentence.

---

# Educational Reading Notes

## Concept / Section Title
...

## Concept / Section Title
...

---

# Key Takeaways

- ...
- ...
- ...
```

## Compression Check

After writing, compare byte size against the source. Use a temporary Layer 3 file when practical, then delete it.

```bash
# Windows
(Get-Item summary.md).Length; (Get-Item transcript.md).Length
(Get-Item layer3.md).Length; (Get-Item transcript.md).Length

# Unix
wc -c summary.md transcript.md
wc -c layer3.md transcript.md
```

Targets:

- Full summary should be clearly shorter than the source; rewrite if it is >=80% of source size.
- Layer 3 should usually be less than 50% of source size.
- Dense sources justify gentler compression; low-density conversations require stronger cuts.

If too long, cut Layer 2 to bare navigation, merge repeated points in Layer 3, remove low-information examples, and sharpen Layer 4.

## Ambiguity

Ask before choosing a costly workflow, guessing the intended source or episode, changing the desired compression level, dropping nuance because of source quality, or filing outputs into an uncertain source folder.
