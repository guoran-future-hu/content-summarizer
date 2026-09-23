# content-summarizer

Turn one long source — a podcast, lecture, video, blog post, or paper — into notes you absorb in a single pass, instead of going through the whole thing.

Written for one reader: someone who has not been through the material and will not read the raw. The notes replace it.

## What you get

One Markdown file per source, beside the preserved raw:

- **L1 — High-Level Abstract**: the topic, central question, and broad structure at a glance.
- **L2 — Structured Outline**: a readable map of the material, to skim before reading the notes.
- **L3 — Educational Reading Notes**: the layer you actually read — the source rewritten shorter and easier to follow.
- **L4 — Key Takeaways**: what to carry away once the details fade.

The notes are audited back against the raw source so nothing that matters is dropped, and held to a compression target so they stay short.

## Using it

Point an agent at a source and ask for notes, or invoke the skill by name (`content-summarizer`). Audio and video sources go through caption or speech-to-text acquisition; the notes come out in the source's language.

## Repository layout

- `SKILL.md` — the operating spec an agent runs.
- `source-acquisition.md`, `references/`, `scripts/` — acquisition recipes and tooling.
- `LOCAL_ENVIRONMENT.md` — machine-local paths and notes, git-ignored, not shipped.

## License

MIT — see `LICENSE`.
