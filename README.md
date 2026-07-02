# Content Summarizer

An agent skill for summarizing long-form, information-dense content into clear notes.

## Overview

`content-summarizer` is built for sources where the useful signal is spread across many minutes or pages, such as YouTube transcripts, blog articles, podcasts, interviews, talks, documentation, and reports.

Use it to extract the main ideas, supporting evidence, caveats, decisions, action items, and open questions without losing the structure of the original material.

## Usage

Install or enable this skill in an agent workspace, then provide the source content directly or enough context for the agent to read it.

Example requests:

```text
Summarize this YouTube transcript into key ideas, examples, and action items.
```

```text
Read this long blog article and give me an executive summary with caveats and open questions.
```

```text
Condense these podcast notes into a structured briefing.
```

## Output Style

Summaries should be:

- Accurate to the source material.
- Concise without dropping important caveats.
- Structured for quick scanning.
- Explicit about uncertainty or missing context.
- Focused on the user's requested format when one is provided.

## Development

This repository contains the skill source. Keep changes scoped and test examples against realistic long-form content.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.