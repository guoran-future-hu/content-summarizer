#!/usr/bin/env python3
"""Compose the final raw transcript file: metadata header + normalization table + body.

Usage: finalize_raw.py <workdir> --out FILE [--title T] [--speakers S] [--type T]
                       [--quality Q] [--note N]... [--table FILE]

Reads <workdir>/meta.json (bili_meta.sh) and <workdir>/transcript.md
(make_transcript.py). --table takes apply_replacements.py's markdown table file;
--note lines are placed under the table (one bullet each). Fields without a value
fall back to meta.json or '-'; edit the output afterwards for quality prose.
"""
import json
import sys


def get(argv, flag, default=None):
    return argv[argv.index(flag) + 1] if flag in argv else default


def main():
    argv = sys.argv[1:]
    if not argv or argv[0].startswith("--"):
        sys.exit(__doc__)
    work = argv[0]
    out = get(argv, "--out")
    if not out:
        sys.exit("ERROR: --out FILE is required")
    try:
        meta = json.load(open(f"{work}/meta.json", encoding="utf-8"))
    except Exception:
        meta = {}
    notes = [argv[i + 1] for i, a in enumerate(argv) if a == "--note"]
    title = get(argv, "--title", meta.get("title") or "—")
    speakers = get(argv, "--speakers", "—")
    typ = get(argv, "--type", "视频 · 语音转写（STT）")
    quality = get(argv, "--quality", "—")
    table = ""
    tpath = get(argv, "--table")
    if tpath:
        table = open(tpath, encoding="utf-8").read().strip()
    body = open(f"{work}/transcript.md", encoding="utf-8").read().strip()

    parts = [f"# {title}", "", "## Metadata", "",
             f"- Source: {meta.get('webpage_url') or '—'} （{meta.get('uploader') or '—'}）",
             f"- Speakers: {speakers}",
             f"- Date: {meta.get('upload_date') or '—'}（发布）",
             f"- Duration: {meta.get('duration_hms') or '—'}",
             f"- Type: {typ}",
             f"- Transcript Quality: {quality}", ""]
    if table:
        parts += ["### 归一化（STT 原样 → 修正 → 本稿次数）", "", table, ""]
    for n in notes:
        parts.append(n if n.startswith("-") else f"- {n}")
    parts += ["", "---", "", body, ""]
    open(out, "w", encoding="utf-8").write("\n".join(parts))
    print(f"-> {out}")


if __name__ == "__main__":
    main()
