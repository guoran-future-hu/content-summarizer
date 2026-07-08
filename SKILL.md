---
name: content-summarizer
description: Use when converting podcasts, videos, audio, transcripts, articles, papers, PDFs, Markdown files, pasted text, or other long-form source material into durable educational notes. Covers workflow-registry acquisition, raw-source preservation, `content-summary` filing, and four-layer notes that preserve reasoning, evidence, confidence, scope, and useful detail while compressing away low-value transcript or prose clutter.
---

# Long-Form Source -> Notes

## Posture

Act as a source-faithful learning-note editor. Reduce reading effort while preserving the author's structure of thought: claims, evidence, mechanisms, assumptions, uncertainty, scope, and practical implications. The notes should feel like a cleaner, compressed study version of the source, not a review, critique, translation, or new essay.

## Maintenance

This is a skill shared by many agents and machines. Track general rules only. Put local paths, host setup, private access, regional/network notes, one-offs, and tool quirks in git-ignored `LOCAL_ENVIRONMENT.md`.

## Steps

1. Load `LOCAL_ENVIRONMENT.md` if present.
2. Identify source type, metadata, and source folder.
3. Read `workflow-registry.md`; use the matching entry or default policy.
4. Acquire the highest-tier transcript/source text.
5. Save raw/source material under `./content-summary/<source-folder>/`.
6. Clean mechanical artifacts only.
7. Write four-layer notes beside the raw/source file with `-summary`.
8. Run the compression check; tighten if needed.
9. Delete temporary staging files.
10. Update `workflow-registry.md` only for reusable acquisition, cleanup, fallback, folder, or naming rules.

## Filing
Save final outputs under `./content-summary/`, organized by source. Preserve the raw/source file. Use existing source folders when possible.

Default names:

- Raw/source: `YYYY-MM-DD-<title>.md`
- Summary: `YYYY-MM-DD-<title>-summary.md`

Use publication date. Put source-specific names in `workflow-registry.md`. If a provided source is outside `content-summary`, copy it into the right source folder first.

## Language

Summary should match the source language. For mixed sources, use the dominant language and preserve source terms/quotes as written. Use UTF-8 for Markdown body content. Keep filenames, dirs, IDs, links, YAML values, and source folders ASCII.

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

```bash
python scripts/check_compression.py summary.md transcript.md
```

Targets: full summary <80% of raw; Layer 3 between 20–50%. Expand Layer 3 if too short; merge repeats and cut examples if too long.

## Ask When in Doubt

Ask before costly workflows, uncertain source choice, changed compression level, dropping nuance because of source quality, or uncertain filing.
