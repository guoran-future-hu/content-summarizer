# Content Summarizer

An agent skill for summarizing long-form content into clear, useful notes.

## Overview

`content-summarizer` helps agents turn articles, documents, transcripts, and other source material into concise summaries. It is intended for workflows where the important points, decisions, evidence, and follow-up actions need to be extracted quickly without losing the structure of the original content.

## Use Cases

- Summarize articles, blog posts, and documentation.
- Extract key points from reports or meeting notes.
- Produce concise briefings from long source material.
- Identify decisions, action items, risks, and open questions.
- Convert dense content into readable notes.

## Usage

Install or enable this skill in an agent workspace, then invoke it when you need content summarized. Provide the source content directly, or provide enough context for the agent to read the relevant files or pages.

Example requests:

```text
Summarize this article into key points and action items.
```

```text
Read this document and give me an executive summary with open questions.
```

```text
Condense these notes into a structured briefing.
```

## Output Style

Summaries should be:

- Accurate to the source material.
- Concise without dropping important caveats.
- Structured for quick scanning.
- Explicit about uncertainty, missing context, or assumptions.
- Focused on the user's requested format when one is provided.

## Development

This repository contains the skill source. Keep changes scoped, test examples against realistic content, and avoid adding broad behavior that belongs in a more specialized skill.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
