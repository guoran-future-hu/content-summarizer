# README — engineering guide for future agents

## Principle of this skill: not telling you what to do but help you understand what should be done

I learn from blogs and podcasts, however I don't have the time/energy.
That's why I create this skill. From the first principle, the esssential outcome I want is:

**Spend less time AND mental effort absorbing the same content**

A few implications:
- It usually means not going through the whole article/vid
- Simple wording and short sentences are prefered.
- There is no lossless compression, but we can still aim for minimum loss in the parts that matter
- Fewer words does not necessary mean less mental effort. Academic papers are compact but requires huge effort to understand.

This skill optimizes for BOTH.

Use case is usually, I want to read a blog but don't have time, so I want to read the output of this skill and don't read the raw at all. It is a first-read replacement when I have no prior knowledge about content, not a summary for review.

In detail, it does:

Turn long sources (video / podcast / article / paper) into notes the user absorbs in one pass.
- L1 indexes, L2 maps, L3 is the layer the user actually reads, L4 distills.
- Trust mechanisms are load-bearing — keep them intact: raw preserved beside the summary · coverage audit raw↔L3 · compression targets · no added thinking · hedges kept.
- Optimize the stable floor across agents and machines, not hero runs.
## How to work on it

- The skill steers rather than instructs: mostly what to do, why only when necessary; mechanics live in `scripts/` and `references/`, and the model judges inside the frame.
- Judge every line against current models: trim what a capable model does by default — over-specification confuses. See `~/.agents/prompts-guide/`.
- When a workflow stabilizes, script it — download, STT, transcript join, normalization, metadata, and assembly are already scripted.
- Retired flows live in `archive/` — reference only.

## Editing rules

Before adding anything here, ask: **would this help with a different source / paper / video / account?**
The test is per single item (one video / paper / episode) — tooling built for a whole corpus, author, or channel (e.g. one author's full works) is reusable: keep it in the skill.
If not, it belongs in the job's output folder.

**Keep:** rules, thresholds, rates, commands, paths, pitfalls, fallbacks.
**Drop:** specific URLs, BV ids, paper titles, channel names, per-job numbers and timings, account ids, one-off case notes.

Write steps and commands imperatively. No rationale prose, no worked example that fits only one case.

## Open items (feel free to share your thoughts)

- L2's outline-first design came from old research on outlining improving summary quality; the premise is doubtful for current models — kept provisionally.
- Outputs land in the vault (`Inbox/` for now); tighter KB integration is an open direction.
- Different media has different characteristics that I'm considering writing specific versions targetting them:
  - Podcasts and lectures are presented on the fly, they might be less organized and contain filler words more ofter
    - So skill should aim for better organization and cutting rambling words
    - But there are also lecture-style podcasts that has different traits
  - Blogs are better organized, but also contain filler or connecting words
    - So skill should aim for shorter version
  - Thesis are dense and compact, their issue mainly comes from the wording complexity and difficulty to absorb, instead of being too long. Also there are different content that I would pay attention to at different time. E.x. at first read I wouldn't bother with experimental and engineering detail.