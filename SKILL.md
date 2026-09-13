---
name: content-summarizer
description: Use when turning long-form source material into durable four-layer notes.
---

# Long-Form Source -> Notes

Use two roots:

- Skill root: this skill directory, for shipped files such as `./source-acquisition.md`, `./scripts/`, `./references/`, and optional `./LOCAL_ENVIRONMENT.md`.
- Summary root: the user's output folder, chosen by the user or local environment. Do not store user source material in the skill repo by default.

## Posture

Act as a source-faithful learning-note editor. Compress for first-time absorption, not review. Reduce reading time and mental load while preserving the source's effective information. The notes should feel like a cleaner, clearer study version of the source.

## Maintenance

This is a skill shared by many agents and machines. Track general rules only. Put local paths, host setup, private access, regional/network notes, etc. in git-ignored `./LOCAL_ENVIRONMENT.md`.

Read `README.md` before editing the skill.

## Steps

1. Load `./LOCAL_ENVIRONMENT.md` if present.
2. Identify source type and metadata.
3. For naming convention, check existing files in the target folder; follow their pattern.
4. If usable Markdown/source text is not already provided, read `./source-acquisition.md`; for Bilibili sources also `./references/bilibili-recipes.md`.
5. Save or copy raw/source material in `<summary-root>/<source-folder>/`; a source from outside the summary root gets copied in first.
6. Clean mechanical artifacts only.
7. Draft Layer 2 as the source map, then write the four-layer notes beside the raw/source file with `-summary`.
8. Run the coverage audit (raw vs Layer 3).
9. Run the compression check; tighten if needed.
10. Delete temporary staging files.
11. If necessary, update `./source-acquisition.md` for acquisition or fallback rules.

## Language

Summary should match the source language. Use UTF-8 for Markdown body content. Keep filenames and other meta in ASCII.

## Output Contract

Always produce four layers. 

Prefer short sentences and simple wording. Use longer sentences or complex wording only when needed for accuracy.

Do not drop information because it is complex. Make complex points easier to absorb by applying the following rules.

Do not add new thinking. If the source is unclear or a rule seems to conflict with source fidelity, preserve the source point and add a brief note instead of resolving it yourself.

### 1. High-Level Abstract

Write 3-4 sentences, about 80-120 words. Name the topic, central question or thesis, and broad structure. Keep this layer index-card sized.

### 2. Structured Outline

Create the source map, not just a polished table of contents. Layer 2 makes Layer 3's content salient.

**Build it from the source, not memory.** Start with every explicit source heading, timestamp block, section break, or obvious topic shift, then scan between those anchors for unheaded topic shifts. Each entry is one heading plus one compact sentence connecting short phrases that index distinct claims, mechanisms, examples, caveats, historical facts, source-bias points, practical implications, institutional or economic structures, and side branches worth preserving. It indexes; it does not explain.

Use timestamps only when directly available.

### 3. Educational Reading Notes

This is the main layer. Rewrite the source with fewer words, simpler presentation, same effective information.

Cover every distinct topic and significant content move. A topic may merge into a broader heading, but must not vanish. Preserve anything carrying distinct substance: claims, examples, mechanisms, historical facts, caveats, disagreements, confidence signals, practical implications — side branches included.

Remove (minimal list):

- Overused adjectives and adverbs that do not add information
- Academic and verbal padding, filler
- Jokes, casual chatter and low-info examples

Compress by information density, not medium; casual conversation can be dropped aggressively.

Use structures like bullets and tables when they substantially help clarify the content.

### 4. Key Takeaways

Distill the source's core conclusions, strongest arguments, practical implications, and ideas worth remembering. Keep findings, mechanisms, implications, recommendations, and boundaries distinct instead of flattening them into generic advice.

## Wrong Source Warning

If the provided source already has this four-layer structure, stop and warn the user — it looks like a summary, not a raw source.

## Fidelity, Attribution, and Confidence

Default to clean source-grounded prose. Attribute only when speaker identity or framing changes interpretation (disagreement, expertise, disputed claims, forecasts, personal analysis); then signal the frame once per section, not sentence by sentence. Preserve the source's confidence level — keep its hedges ("probably," "might," "in my view"); quote sparingly, only for precise or memorable wording.

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

Audit the raw source against Layer 3 directly — only this surfaces details lost in the source→Layer-2 squeeze; neither Layer-2 comparison shows them.

1. Read the source and Layer 3 side by side. For every topic, mechanism, example, caveat, and claim in the source, check Layer 3 expands it with its effective detail — not merely names it.
2. Mark each source topic or significant content move: `expanded`, `merged into <Layer 3 heading>` (distinct content preserved), or `intentionally dropped: <low-info reason>`.
3. Expand the under-developed Layer 3 sections from the source. Afterward, re-check Layer 2 for index drift.

Completion criterion: every source topic, mechanism, and significant detail is fully expanded in Layer 3, or has a concrete low-information drop reason. A topic present only as a Layer 2 heading does not count as covered.

## Compression Check

Check summary size against raw source:

```bash
python ./scripts/check_compression.py <summary-root>/<source-folder>/<summary-file>.md <summary-root>/<source-folder>/<raw-source-file>.md
```

Targets:

- Full summary must be < 80% of raw; tighten if >= 80%.
- Layer 3 should be roughly 20-50% of raw, depending on source density. Ratios outside this range are warnings, not failures.
- Do not add filler, drop nuance, or make byte-count edits only to satisfy a ratio.

## Ask When in Doubt

Ask before costly workflows, uncertain source choice, changed compression level, dropping nuance because of source quality, or uncertain filing.
