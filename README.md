# Content Summarizer

An agent skill for turning long-form sources into notes.

## Overview

`content-summarizer` handles transcripts, articles, podcasts, interviews,
talks, docs, reports, and papers.

Use it to preserve claims, evidence, reasoning, caveats, confidence, and
implications while cutting clutter.

## Feature

- Support a variety of tools that help you get the source from web article / blog / youtube video / Bilibili video etc.

- Reached decent major topic coverage on super-long podcast, up to 4.5 hrs, tested with DeepSeek V4 pro reasoning max

## Design philosophy

### Comporession Goal

What makes a good summary? Depends on how you use it. My primary use is:
1. Read as first-time expose, to absorb the same **effective information** while saving time and mental energy
2. As compressed version for LLM knowledge base to save token and attention budget


Two use cases require similar compression goal:
- Prefer short sentences over long
- Prefer simple wording over complicated (but preserve techinical terms)
- Use intuitive language
- Use structures like bulletpoints and table when help clafity
- Remove overused adj/adv that don't add information, padding words, rambling conversation words, etc.
- Preserve all effective information, cover all major topics and side branches
- No introducing of new ideas, synthesis, integration (that's my job or knowledge base's work)


### Topic Coverage in Long Corpus
Relevant research reveals that LLM generally summarize well when using layered approach, i.e. generate section outline, then the actual content.

[TODO add source paper later]


The mechanism is close to that, the outline serves as an index or anchor for the later work to fill in information.

So the coverage completeness of outline directly affects the completeness of whole summary.

Lots of context engineering effort goes into design the outline layer as coverage map, this substantially improved model ability when working on super-long courpus (hours of podcast transcript)

### Save Context to Save Attention Resources

LLM context windows are growing rapidly.

But being able to fit the context doesn't means the preserve of attention performance.

One of my core belief is that, the essense of intelligence is to recognise what is "relevant" in the context. In LLM this is done by the attention mechaism.

But there is limited attention resource, which will be dilluted if context is large. When context is more than a hidden threshold, model's ability to pick up "relevant" bits can drop dramatically, despite there are lots of room in context window.

So conclution is simple, when designing context, this skill tried to cut assresively on the context that feed to a model, and only feed the model text it actually need. This helps preserve the model's attention resources and thus, its intelligence.


## Usage

Install or enable this skill in an agent workspace, then provide the source content directly or enough context for the agent to read it.

The skill files live in the skill root. Generated transcripts, source copies,
and summaries should live in a user-owned summary root. This skill repository
ignores `LOCAL_ENVIRONMENT.md` and its own `content-summary/` path so private
notes and source material are not published with the skill.

Example requests:

```text
Summarize this YouTube transcript into four-layer notes.
```

```text
Read this long article and preserve the main argument, evidence, and caveats.
```

```text
Condense these podcast notes without losing the speaker's reasoning chain.
```

## Output Style

Notes should be:

- Accurate to the source material.
- Concise without dropping caveats.
- Structured for quick scanning.
- Explicit about uncertainty or missing context.
- Focused on the user's requested format when one is provided.

## Development

This repository contains the skill source. Keep changes scoped and test examples against realistic long-form content.

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.
