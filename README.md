# Content Summarizer

An agent skill for turning long-form sources into notes.

## Overview

`content-summarizer` handles transcripts, articles, podcasts, interviews,
talks, docs, reports, and papers.

Use it to preserve claims, evidence, reasoning, caveats, confidence, and
implications while cutting clutter.

## Usage

Install or enable this skill in an agent workspace, then provide the source content directly or enough context for the agent to read it.

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

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
