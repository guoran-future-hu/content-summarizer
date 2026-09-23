---
name: content-summarizer
description: Use when turning long-form source material into durable four-layer notes.
---

# Long-Form Source -> Notes

Use two roots:

- Skill root: this skill directory, for shipped files such as `./source-acquisition.md`, `./scripts/`, `./references/`, and optional `./LOCAL_ENVIRONMENT.md`.
- Summary root: the user's output folder, from `./LOCAL_ENVIRONMENT.md` or the user.

## Maintenance

This is a skill shared by many agents and machines. Track general rules only. Put local paths, host setup, private access, regional/network notes, etc. in git-ignored `./LOCAL_ENVIRONMENT.md`.

Read `dev/ENGINEERING.md` before editing the skill; `dev/` stays out of the repo and never enters a run.

## Steps

1. Load `./LOCAL_ENVIRONMENT.md` if present.
2. Identify source type and metadata.
3. Name the raw source `<base>.md` and the notes `<base>-summary.md`. Clean Markdown pulled from a web page keeps the bare name; a source rebuilt from captions, STT, or OCR becomes `<base>-transcript.md`. Take `<base>` from the target folder's existing files.
4. If usable Markdown/source text is not provided, read `./source-acquisition.md`; for Bilibili sources also `./references/bilibili-recipes.md`.
5. Save or copy raw/source material in `<summary-root>/<source-folder>/`; a source from outside the summary root gets copied in first.
6. Clean mechanical artifacts only.
7. Build the source index map into a temporary staging file, then write the notes (Layers 1, 3 and 4) beside the raw/source file with `-summary`.
8. Run the coverage audit (raw vs Layer 3).
9. Write Layer 2 from the finished notes.
10. Run the compression check; tighten if needed.
11. Delete the temporary files: the source index map and the coverage audit.

## Language

Summary should match the source language. Use UTF-8 for Markdown body content. Keep filenames and other meta in ASCII.

## Output Principles

The reader has not gone through the source and will not read the raw; these notes replace it.

Aim for **less reading time AND less mental effort** than the source. Fewer words alone won't get there — a dense paper is compact and still costs huge effort.

- Produce four layers. 
- Word choice is yours, not the source's. **Prefer short sentences and simple wording**.
- Carry only the source's thinking. Add brief notes for ambiguity and conflicts instead of resolving it yourself.
- Work from the raw source, as existing summaries might be outdated and produced in defected ways.


### Source Index Map

A temporary staging file, `<base>-index-map.md` in the source folder — separate from the notes file, deleted in the final cleanup. It indexes the source span by span as drafting material for Layer 3.

**Build it from the source, not memory.** Start with every explicit source heading, timestamp block, section break, or obvious topic shift, then scan between those anchors for unheaded topic shifts. Each entry is one heading plus one compact sentence of short phrases that **index** the distinct information worth preserving from that span—anything that materially changes what was claimed, how it works, what supports or limits it, or what branch of the source it belongs to. It **indexes**, not explains.


### L1. High-Level Abstract

Write 3-4 sentences, about 80-120 words. Name the topic, central question or thesis, and broad structure.


### L2. Structured Outline

A readable outline of the material — what a human skims before reading the notes. Write it from the finished notes.

Add timestamps only when directly available.


### L3. Educational Reading Notes

This is the main layer: a cleaner, clearer study version of the source, compressed for first-time absorption rather than review. Rewrite the source with fewer words and easier-to-follow presentation, so it costs **less reading time AND less mental effort** and still carries the source's effective information.

Cover every distinct topic, significant content move, and the logical connections between them. A topic may merge into a broader heading, but must not vanish.

**The keep test**: would removing it leave the reader with less than the source gave? What passes stays — a move in the argument, a branch the source went down, supporting examples, etc. What fails goes — padding, filler, chatter, decorative modifiers, etc.

Compression follows information density — the more a passage carries, the more room it gets. Chatty digressions, repeated framing, self-interruptions carry little, so they get cut hard.

Distinguish facts and author/speaker's opinions in the prose. Preserve the source's confidence level and hedges ("probably," "might") when needed.

Use structures like bullets and tables when they help clarify the content.


### L4. Key Takeaways

Distill what a reader should carry away once the details fade. Each takeaway keeps the shape it had in the source, and stays specific enough that it could not have been written from any other source on the topic.


## Wrong Source Warning

If the provided source already has this four-layer structure, stop and warn the user — it looks like a summary, not a raw source.


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
One readable line on what this part covers.

## 2. Topic Title [timestamp if available]
One readable line on what this part covers.

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

Audit the raw source against Layer 3 directly.

1. Read the source and Layer 3 side by side, span by span. For everything in the source that passes the keep test, check Layer 3 expands it with its effective detail — not merely names it.
2. Mark each source topic or content move: `expanded`, `merged into <Layer 3 heading>` (distinct content preserved), or `intentionally dropped: <low-info reason>`. Record the marks in `<base>-coverage-audit.md`, temporary, deleted with the staging files.
3. Expand the under-developed Layer 3 sections from the source.

Completion criterion: everything that passes the keep test is expanded in Layer 3.


## Compression Check

Check Layer 3 against the raw source:

```bash
python ./scripts/check_compression.py <summary-root>/<source-folder>/<summary-file>.md <summary-root>/<source-folder>/<raw-source-file>.md
```

Target: Layer 3 roughly 20-60% of raw, depending on source density. Ratios outside this range are warnings, not failures.

When the ratio is off, re-read the notes against the source and reconsider: cut what carries no information, add what is missing, keep the nuance.


## Ask When in Doubt

Ask whenever a choice would cost the user something they cannot see in the finished notes — an expensive run, the wrong source, a different compression level, nuance dropped for source quality, a file in the wrong place.
