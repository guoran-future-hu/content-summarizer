---
name: content-summarizer
description: Use when converting podcasts, videos, audio, transcripts, articles, papers, PDFs, Markdown files, pasted text, or other long-form source material into durable educational notes. Covers workflow-registry acquisition, raw-source preservation, `content-summary` filing, and four-layer notes that preserve reasoning, evidence, confidence, scope, and useful detail while compressing away low-value transcript or prose clutter.
---

# Long-Form Source -> Notes

## Posture

Act as a source-faithful learning-note editor. Compress for first-time absorption, not review. Reduce reading time and mental load while preserving the source's effective information. The notes should feel like a cleaner, clearer study version of the source.

## Maintenance

This is a skill shared by many agents and machines. Track general rules only. Put local paths, host setup, private access, regional/network notes, one-offs, and tool quirks in git-ignored `LOCAL_ENVIRONMENT.md`.

## Steps

1. Load `LOCAL_ENVIRONMENT.md` if present.
2. Identify source type, metadata, and source folder.
3. Read `workflow-registry.md`; use the matching entry or default policy.
4. Acquire the highest-tier transcript/source text.
5. Save raw/source material under `./content-summary/<source-folder>/`.
6. Clean mechanical artifacts only.
7. Draft Layer 2 as the source map, then write the four-layer notes beside the raw/source file with `-summary`.
8. Run the coverage audit.
9. Run the compression check; tighten if needed.
10. Delete temporary staging files.
11. Update `workflow-registry.md` only for reusable acquisition, cleanup, fallback, folder, or naming rules.

## Filing
Save final outputs under `./content-summary/`, organized by source. Preserve the raw/source file. Use existing source folders when possible.

Default names:

- Raw/source: `YYYY-MM-DD-<title>.md`
- Summary: `YYYY-MM-DD-<title>-summary.md`

Use publication date. Put source-specific names in `workflow-registry.md`. If a provided source is outside `content-summary`, copy it into the right source folder first.

## Language

Summary should match the source language. For mixed sources, use the dominant language and preserve source terms/quotes as written. Use UTF-8 for Markdown body content. Keep filenames and other meta in ASCII.

## Output Contract

Always produce four layers. Same information -> fewer words -> easier absorption. 

Prefer short sentences and simple wording. Use longer sentences or complex wording only when needed for accuracy.

Do not drop information because it is complex. Make complex points easier to absorb by applying the following rules.

Do not add new thinking. If the source is unclear or a rule seems to conflict with source fidelity, preserve the source point and add a brief note instead of resolving it yourself.

### 1. High-Level Abstract

Write 3-4 sentences, about 80-120 words. Name the topic, central question or thesis, and broad structure. Keep this layer index-card sized.

### 2. Structured Outline

Create the source map, not just a polished table of contents. Layer 2 is the coverage artifact that makes Layer 3's content salient.

**Build it from the source, not memory**. Start with every explicit source heading, timestamp block, section break, or obvious topic shift, then scan between those anchors for unheaded topic shifts. Each entry is one heading plus one compact sentence made from connecting short phrases that index distinct claims, mechanisms, examples, caveats, historical facts, source-bias points, practical implications, institutional or economic structures, and side branches worth preserving.

Compactness and complete coverage do not conflict here: the sentence indexes and connects content; it does not explain it.

Low-value or similar sections may be merged, but the merged heading or sentence must name the covered material.

Use timestamps only when directly available.

### 3. Educational Reading Notes

This is the main layer. Rewrite the source with fewer words, simpler presentation, same effective information.

Cover every distinct topic and significant content move in the source. A topic may be merged into a broader heading, but it must not vanish. Preserve side branches when they carry a distinct claim, example, mechanism, historical fact, source caveat, or practical implication.

Preserve (minimal list):

- Technical terms
- Key points, arguments, and reasoning chains
- Definitions, frameworks, mental models, and technical details
- Causal mechanisms, assumptions, evidence, and necessary examples
- Caveats, disagreements, limitations, exceptions, null results, and trade-offs
- Claim posture: observation, experiment, theory, speculation, forecast, interpretation, or prescription

Remove (minimal list):

- Overused adjectives and adverbs that do not add information
- Academic and verbal padding, filler
- Jokes, casual chatter and low-info examples

Compress according to information density. Dense scripted explainers and papers can keep more structure and detail; rambling conversations should be cut aggressively.

Use structures like bullets and tables when they substantially help clarify the content.

### 4. Key Takeaways

Distill the source's core conclusions, strongest arguments, practical implications, and ideas worth remembering. Keep findings, mechanisms, implications, recommendations, and boundaries distinct instead of flattening them into generic advice.

## Wrong Source Warning

If you are provided a source that has simialr 4 layer structure, stop and warn the user for potentially provided summary as source.

## Fidelity, Attribution, and Confidence

Default to clean source-grounded prose. Attribute only when speaker identity or author framing changes interpretation, such as disagreement, expertise, disputed claims, forecasts, or clearly personal analysis.

Preserve the source's confidence level. Keep hedges such as "probably," "might," "very likely," "in my view," etc.

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

## Coverage Audit

Before moving to Layer 3, compare the source against Layer 2 for omissions. Scripts may extract headings or timestamps, but semantic coverage is judged by reading the source map.

1. Re-check the source against Layer 2. Every explicit source heading must appear, unless marked `intentionally dropped: <low-info reason>`.
2. For each source topic or significant content move, mark one of: `indexed`, `merged into <Layer 2 heading>`, or `intentionally dropped: <low-info reason>`.
3. Add missing effective information to Layer 2 before changing Layer 3.
4. Refresh the affected Layer 3 notes from the corrected Layer 2 source map.

Completion criterion: every source heading, topic, and significant content move has a visible destination in Layer 2, or a concrete low-information drop reason.

## Compression Check

Check summary size against raw source:

```bash
python scripts/check_compression.py summary.md transcript.md
```

Targets:

- full summary < 80% of raw, if more than 80% then it's not really a summary
- Layer 3 should be roughly between 20–50% depends on the density of source. < 20% is a warning sign of potentially skipping content.
- Do not rerun only to satisfy a ratio. If Layer 3 is below target, run the coverage audit first; expand only with missing effective information.

## Ask When in Doubt

Ask before costly workflows, uncertain source choice, changed compression level, dropping nuance because of source quality, or uncertain filing.
