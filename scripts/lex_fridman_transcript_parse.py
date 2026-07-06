#!/usr/bin/env python3
"""
Parse Lex Fridman podcast transcript HTML from lexfridman.com/<guest>-transcript.

Usage:
    python lex_fridman_transcript_parse.py <slug> -o transcript.md

    # Example:
    python lex_fridman_transcript_parse.py jensen-huang -o transcript.md

    # Or with explicit input/output:
    python lex_fridman_transcript_parse.py raw.html -o transcript.md
"""

import sys
from html.parser import HTMLParser


class LFTranscriptParser(HTMLParser):
    """Parse Lex Fridman transcript HTML -> clean markdown.

    HTML structure:
      - Chapter headings:  <h2 id="chapterN_slug">Title</h2>
      - Speaker segments:  <div class="ts-segment">
                             <span class="ts-name">Speaker</span>
                             <span class="ts-timestamp"><a href="...?t=NN">(HH:MM:SS)</a></span>
                             <span class="ts-text">Spoken text...</span>
                           </div>
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.lines = []
        self.in_h2 = False
        self.in_segment = False
        self.in_name = False
        self.in_ts = False
        self.current_name = None
        self.current_ts = None

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'nav', 'header', 'footer'):
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == 'h2':
            self.in_h2 = True
        if tag == 'div':
            attr_dict = dict(attrs)
            if attr_dict.get('class') == 'ts-segment':
                self.in_segment = True
        if tag == 'span':
            attr_dict = dict(attrs)
            cls = attr_dict.get('class', '')
            if cls == 'ts-name':
                self.in_name = True
            elif cls == 'ts-timestamp':
                self.in_ts = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'nav', 'header', 'footer'):
            self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag == 'h2':
            self.in_h2 = False
            self.lines.append('')       # blank line between sections
        if tag == 'div' and self.in_segment:
            self.in_segment = False
            self._flush_segment()
        if tag == 'span':
            self.in_name = False
            self.in_ts = False

    def handle_data(self, data):
        if self.skip_depth:
            return
        d = data.strip()
        if not d:
            return
        if self.in_h2:
            self.lines.append(f'## {d}')
            return
        if self.in_name:
            self.current_name = f'**{d}**'
            return
        if self.in_ts:
            self.current_ts = f'*{d}*'
            return
        if self.in_segment:
            self.lines.append(d)

    def _flush_segment(self):
        if self.current_ts:
            if self.current_name:
                self.lines.append(f'{self.current_name} {self.current_ts}')
            else:
                self.lines.append(self.current_ts)
        self.current_name = None
        self.current_ts = None

    def get_text(self) -> str:
        return '\n\n'.join(self.lines)


import urllib.error
import urllib.request


def download_html(slug: str) -> str:
    """Download raw HTML from lexfridman.com/<slug>-transcript."""
    url = f'https://lexfridman.com/{slug}-transcript'
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f'Error: No transcript page at {url}', file=sys.stderr)
            print('This episode may not have an official transcript page.', file=sys.stderr)
            print('Fall back to YouTube subtitles:', file=sys.stderr)
            print('  python -m yt_dlp --write-auto-subs --sub-lang en --skip-download -o "<out>" "<youtube-url>"', file=sys.stderr)
            print('  python clean_vtt_subtitles.py <out>.en.vtt transcript.md', file=sys.stderr)
            sys.exit(1)
        raise


def parse_html(html: str) -> str:
    parser = LFTranscriptParser()
    parser.feed(html)
    text = parser.get_text()
    # Find transcript start at "## Introduction" heading
    start_idx = 0
    for i, line in enumerate(parser.lines):
        if line.strip() == '## Introduction':
            start_idx = i
            break
    return text


def main():
    import argparse
    ap = argparse.ArgumentParser(description='Parse Lex Fridman transcript HTML')
    ap.add_argument('input', nargs='?', help='HTML file path, or slug to download (e.g. "jensen-huang")')
    ap.add_argument('-o', '--output', help='Output file path (default: stdout)')
    args = ap.parse_args()

    if args.input:
        if args.input.startswith('http'):
            # Extract slug from URL like https://lexfridman.com/jensen-huang-transcript
            slug = args.input.rstrip('/').rsplit('/', 1)[-1].replace('-transcript', '')
            html = download_html(slug)
        elif args.input.endswith('.html') or args.input.endswith('.htm'):
            with open(args.input, 'r', encoding='utf-8') as f:
                html = f.read()
        else:
            # Try as file first, then as slug
            try:
                with open(args.input, 'r', encoding='utf-8') as f:
                    html = f.read()
            except (FileNotFoundError, OSError):
                # Not a readable file — assume it's a slug
                html = download_html(args.input)
    else:
        html = sys.stdin.read()

    text = parse_html(html)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'Wrote {len(text)} chars to {args.output}', file=sys.stderr)
    else:
        sys.stdout.write(text)


if __name__ == '__main__':
    main()
