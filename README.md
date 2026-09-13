# README — engineering guide for future agents

## Why this exists

Turn long sources (video / podcast / article / paper) into notes the user absorbs in one pass.
- L1 indexes, L2 maps, L3 is the layer the user actually reads, L4 distills.
- Trust mechanisms are load-bearing — keep them intact: raw preserved beside the summary · coverage audit raw↔L3 · compression targets · no added thinking · hedges kept.
- Optimize the stable floor across agents and machines, not hero runs.

## How to work on it

- The skill steers rather than instructs: mostly what to do, why only when necessary; mechanics live in `scripts/` and `references/`, and the model judges inside the frame.
- Judge every line against current models: trim what a capable model does by default — over-specification confuses. See `~/.agents/prompts-guide/`.
- When a workflow stabilizes, script it — download, STT, transcript join, normalization, metadata, and assembly are already scripted.
- Retired flows live in `archive/` — reference only, never active policy.

## Editing rules

Before adding anything here, ask: **would this help with a different source / paper / video / account?**
The test is per single item (one video / paper / episode) — tooling built for a whole corpus, author, or channel (e.g. one author's full works) is reusable: keep it in the skill.
If not, it belongs in the job's output folder.

**Keep:** rules, thresholds, rates, commands, paths, pitfalls, fallbacks.
**Drop:** specific URLs, BV ids, paper titles, channel names, per-job numbers and timings, account ids, one-off case notes.

Write steps and commands imperatively. No rationale prose, no worked example that fits only one case.

## Open items

- L2's outline-first design came from old research on outlining improving summary quality; the premise is doubtful for current models — kept provisionally.
- Outputs land in the vault (`Inbox/` for now); tighter KB integration is an open direction.
