#!/usr/bin/env python3
"""Check content-summarizer compression ratios against raw transcript.

Usage:
    python ./scripts/check_compression.py <summary-root>/<source-folder>/<summary-file>.md <summary-root>/<source-folder>/<raw-source-file>.md

Prints byte sizes, ratios, and PASS/FAIL for:
    - Full summary < 80% of raw
    - Layer 3 (Educational Reading Notes) between 20% and 50% of raw
"""

import re
import sys


def extract_layer3(summary: str) -> str:
    """Extract the Educational Reading Notes section."""
    lines = summary.split('\n')
    start = end = None
    for i, line in enumerate(lines):
        if 'Educational Reading Notes' in line and line.strip().startswith('#'):
            start = i + 1
        if start is not None and 'Key Takeaways' in line and line.strip().startswith('#'):
            end = i
            break
    if start is None or end is None:
        print("ERROR: Could not find Layer 3 boundaries", file=sys.stderr)
        sys.exit(1)
    layer3 = '\n'.join(lines[start:end]).strip()
    layer3 = re.sub(r'^---\s*\n', '', layer3)
    layer3 = re.sub(r'\n---\s*$', '', layer3)
    return layer3


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} summary.md transcript.md", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        summary = f.read()
    raw_bytes = len(open(sys.argv[2], 'rb').read())
    summary_bytes = len(summary.encode('utf-8'))

    layer3 = extract_layer3(summary)
    layer3_bytes = len(layer3.encode('utf-8'))

    full_pct = summary_bytes / raw_bytes * 100
    l3_pct = layer3_bytes / raw_bytes * 100

    print(f"Full summary: {summary_bytes:>6d} / {raw_bytes:>6d} = {full_pct:5.1f}%  {'PASS' if full_pct < 80 else 'FAIL'}")
    print(f"Layer 3 only: {layer3_bytes:>6d} / {raw_bytes:>6d} = {l3_pct:5.1f}%  {'PASS' if 20 < l3_pct < 50 else 'FAIL'}")
    if full_pct >= 80 or not (20 < l3_pct < 50):
        sys.exit(1)


if __name__ == '__main__':
    main()
