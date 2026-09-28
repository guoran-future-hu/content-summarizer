# content-summarizer

Turn one long source — a podcast, lecture, video, blog post — into notes you absorb in a single pass, instead of going through the whole thing.

Written for one reader: someone who has not been through the material and will not read the raw. The notes replace it.

## What you get

One Markdown file per source, beside the preserved raw:

- **L1 — High-Level Abstract**: the topic, central question, and broad structure at a glance.
- **L2 — Structured Outline**: a readable map of the material, to skim before reading the notes.
- **L3 — Educational Reading Notes**: the layer you actually read — the source rewritten shorter and easier to follow.
- **L4 — Key Takeaways**: what to carry away once the details fade.

The notes are audited against the raw source so nothing that matters is dropped, and held to a compression target so they stay short.

## Using it

Point an agent at a source and ask for notes, or invoke the skill by name (`content-summarizer`). Audio and video sources go through caption or speech-to-text acquisition; the notes come out in the source's language.

## Repository layout

- `SKILL.md` — the operating spec an agent runs.
- `source-acquisition.md`, `references/`, `scripts/` — acquisition recipes and tooling.
- `LOCAL_ENVIRONMENT.md` — machine-local paths and private access, git-ignored and not shipped, so the skill stays portable across machines and agents.
- `dev/ENGINEERING.md` — design and maintenance notes for whoever works on the skill; `dev/` also holds past failure cases and retired flows, which stay local.

## What went into it

**Product**

- Two axes are optimised together: reading time and mental effort. Shorter alone is not the goal; a dense paper is compact and still costs enormous effort to absorb.

**Engineering**

- Follows current prompt-engineering practice — single source of truth, fewest possible words, explicit routing — plus Matt Pocock's [writing-for-agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents).

- Research shows that building an outline before the main body makes a summary less likely to drop content, so the pipeline writes a source index map before drafting and audits the finished notes against the raw afterwards. This is what keeps coverage high on very long (4 hrs+) podcasts.

- The coverage audit warns when Layer 3 falls outside 20–60% of the raw's file size — the range a healthy compressed body should land in.

- `dev/ENGINEERING.md` records what I want from this skill. A large part of the skill is "capability patches" that compensate for weaknesses in current-generation backend LLMs; it exists so newer models can see the intent and improve the skill.


## License

MIT — see `LICENSE`.
