#!/usr/bin/env python3
"""
Extract English-only content from bilingual (EN+ZH) transcripts.
Designed for 毕英杰's Machiavelli lecture transcripts from Bilibili Clippings.

Pattern: English paragraph(s) → Chinese translation paragraph(s), alternating.
Handles bilingual headings and inline EN/ZH mixing when no blank line separator exists.
"""

import re
import sys
from pathlib import Path


SPEAKER_NAMES = r'Johnathan Bi|Guest\s*\d+|毕英杰|观众\d+|Maurizio Viroli|Harvey Mansfield|毛里齐奥·维罗利|哈维·曼斯菲尔德'
# Match both formats: **Name**： (Princeton) and **Name：** (Harvard)
SPEAKER_MARKER_RE = re.compile(rf'(\*\*(?:{SPEAKER_NAMES})(?:\*\*\s*[：:]|\s*[：:]\*\*))')
ZH_SPEAKER_RE = re.compile(r'毕英杰|观众|毛里齐奥|哈维·曼斯菲尔德')


def cjk_ratio(text: str) -> float:
    """Return the fraction of CJK characters in text."""
    if not text:
        return 0.0
    cjk = sum(1 for c in text if '\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf')
    return cjk / len(text)


def strip_inline_chinese(text: str) -> str:
    """
    Strip Chinese text that appears inline on the same line as English.
    Splits at the boundary where CJK text begins after English content.
    Example: 'English sentence. 中文翻译。' → 'English sentence.'
    """
    # If no CJK, return as-is
    if cjk_ratio(text) == 0:
        return text
    
    # Split into lines and process each line
    result_lines = []
    for line in text.split('\n'):
        stripped = line.strip()
        if not stripped:
            result_lines.append(line)
            continue
        
        # Find the first CJK character
        cjk_pos = None
        for i, c in enumerate(stripped):
            if '\u4e00' <= c <= '\u9fff':
                cjk_pos = i
                break
        
        if cjk_pos is None:
            result_lines.append(line)
            continue
        
        # Walk back to find a natural boundary: sentence-ending punctuation or space
        j = cjk_pos
        while j > 0 and stripped[j-1] in '  \u3000':
            j -= 1
        
        if j == 0:
            # Chinese starts at beginning — this line is all Chinese
            continue
        
        # Check if there's English content before the CJK
        prefix = stripped[:j].rstrip()
        if prefix and cjk_ratio(prefix) < 0.10:  # mostly English before the split
            result_lines.append(prefix)
        # If prefix has mixed content too, skip the line
    
    return '\n'.join(result_lines)


def strip_chinese_suffix(text: str) -> str:
    """
    Strip the Chinese suffix from a bilingual string.
    Finds the first CJK character, walks back to a natural split point.
    Handles quoted Chinese like '"邪恶" 的摩西' — cuts before the opening quote.
    
    Examples:
      '1.1 "Evil" Moses: Massacre "邪恶" 的摩西：大屠杀' → '1.1 "Evil" Moses: Massacre'
      '2.1 Qualification: Evil for Good 限定条件：为善而恶' → '2.1 Qualification: Evil for Good'
      '1. Why Write The Prince? 他为什么写《君主论》？' → '1. Why Write The Prince?'
      '4. Did Machiavelli Have a Shadow?马基雅维利有阴暗面吗？' → '4. Did Machiavelli Have a Shadow?'
      '## 1. "Evil" Moses "邪恶" 的摩西：' → '## 1. "Evil" Moses'
    """
    for i, c in enumerate(text):
        if '\u4e00' <= c <= '\u9fff':
            # Found first CJK character. Walk back to find the natural split.
            j = i
            # Walk past Chinese punctuation and spaces
            while j > 0 and text[j-1] in ' ｜|：:、，。 \u3000':
                j -= 1
            # If we landed on a quote that opens Chinese text (next non-space is CJK), cut before it
            if j > 0 and text[j-1] in '\"\u201c\u2018\u300c':
                # Check if this quote is opening Chinese text
                after_quote = text[j:].lstrip()
                if after_quote and ('\u4e00' <= after_quote[0] <= '\u9fff'):
                    j -= 1  # include the opening quote in the cut
            # Walk past more spaces/punctuation
            while j > 0 and text[j-1] in ' ｜|：:、，。 \u3000':
                j -= 1
            result = text[:j].rstrip()
            return result if result else text
    return text


def is_chinese_dominant(text: str, threshold: float = 0.40) -> bool:
    """Determine if text is predominantly Chinese."""
    clean = re.sub(r'\*\*[^*]+\*\*', '', text)
    clean = re.sub(r'[*_~`#>]', '', clean)
    # Don't strip # for headings — handled separately
    return cjk_ratio(clean) > threshold


def split_mixed_block(block: str) -> list[tuple[str, bool]]:
    """
    Split a block that contains both EN and ZH content inline (no blank line separator).
    Returns list of (text, is_english) tuples.
    Supports both **Name**： (Princeton) and **Name：** (Harvard) marker formats.
    """
    # Split by speaker markers while preserving them
    tokens = []
    last_end = 0
    
    # Find all speaker boundaries
    all_markers = list(SPEAKER_MARKER_RE.finditer(block))
    
    if not all_markers:
        # No speaker markers — decide by CJK ratio
        return [(block, not is_chinese_dominant(block))]
    
    for match in all_markers:
        start = match.start()
        if start > last_end:
            # Text before this marker
            pre_text = block[last_end:start].strip()
            if pre_text:
                tokens.append((pre_text, not is_chinese_dominant(pre_text)))
        
        marker = match.group(1)
        # Determine if this marker is Chinese or English
        is_zh_marker = bool(ZH_SPEAKER_RE.search(marker))
        
        # Find the end of this speaker's text (next marker or end)
        next_start = None
        remaining = block[match.end():]
        m2 = SPEAKER_MARKER_RE.search(remaining)
        if m2:
            next_start = match.end() + m2.start()
        
        if next_start is not None:
            text_after = block[match.end():next_start].strip()
        else:
            text_after = block[match.end():].strip()
        
        # The marker + text
        full = marker + text_after
        tokens.append((full, not is_zh_marker))
        last_end = next_start if next_start is not None else len(block)
    
    return tokens


def extract_english(input_path: Path) -> tuple[str, str | None]:
    """Extract English-only content from a bilingual transcript file."""
    content = input_path.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    output_lines = []
    in_frontmatter = False
    frontmatter_done = False
    in_toc = False
    toc_done = False
    
    i = 0
    publish_date = None  # extracted from Bilibili UI line like "2025年12月09日"
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # YAML frontmatter
        if i == 0 and stripped == '---':
            in_frontmatter = True
            output_lines.append(line)
            i += 1
            continue
        
        if in_frontmatter:
            output_lines.append(line)
            if stripped == '---':
                in_frontmatter = False
                frontmatter_done = True
            i += 1
            continue
        
        # Skip Bilibili UI noise: everything between frontmatter close and **目录**/first heading
        if frontmatter_done and not toc_done:
            # Capture publish date from Bilibili UI (e.g. "2025年12月09日 11:23")
            date_match = re.match(r'(\d{4})年(\d{1,2})月(\d{1,2})日', stripped)
            if date_match:
                y, m, d = date_match.groups()
                publish_date = f'{y}-{int(m):02d}-{int(d):02d}'
            if stripped == '**目录**' or stripped == '目录：' or stripped == '目录' or line.startswith('#'):
                pass  # let normal processing handle it
            elif not line.startswith('#'):
                i += 1
                continue
        
        # TOC section (between frontmatter end and first ## heading)
        if frontmatter_done and not toc_done and not line.startswith('#'):
            if stripped in ('目录：', '**目录**', '目录'):
                in_toc = True
                i += 1
                continue
            if in_toc and stripped:
                # Skip Chinese-only TOC entries and section markers
                if stripped in ('---', '（上篇）', '（下篇）', '（剩余文稿请看下篇）'):
                    i += 1
                    continue
                if cjk_ratio(stripped) > 0.5:
                    i += 1
                    continue
                en_line = strip_chinese_suffix(stripped)
                if en_line:
                    output_lines.append(en_line)
                i += 1
                continue
            if in_toc and not stripped:
                output_lines.append('')
                i += 1
                continue
            if not stripped:
                output_lines.append('')
                i += 1
                continue
        
        # Section heading (bilingual) — strip Chinese part
        if line.startswith('#'):
            cleaned = strip_chinese_suffix(stripped)
            output_lines.append(cleaned)
            if not toc_done:
                toc_done = True
                in_toc = False
            i += 1
            continue
        
        # Body content: collect paragraphs (separated by blank lines)
        if stripped:
            # Skip Chinese blockquote lines
            if stripped.startswith('>') and is_chinese_dominant(stripped):
                i += 1
                continue
            
            block_lines = []
            while i < len(lines) and lines[i].strip():
                block_lines.append(lines[i])
                i += 1
            
            block_text = '\n'.join(block_lines).strip()
            
            # Check if this block is mixed (has both EN and ZH inline)
            if is_chinese_dominant(block_text):
                # Could be purely Chinese, but check for inline English
                sub_blocks = split_mixed_block(block_text)
                for sub_text, is_en in sub_blocks:
                    if is_en:
                        output_lines.append(sub_text)
            else:
                # English dominant — but check for inline Chinese
                if cjk_ratio(block_text) > 0.08:
                    # Has some Chinese — try speaker-marker split first,
                    # then fall back to inline stripping
                    sub_blocks = split_mixed_block(block_text)
                    if len(sub_blocks) == 1 and sub_blocks[0][1]:
                        # No speaker markers found, block is mixed — strip inline Chinese
                        cleaned = strip_inline_chinese(block_text)
                        if cleaned.strip():
                            output_lines.append(cleaned)
                    else:
                        for sub_text, is_en in sub_blocks:
                            if is_en:
                                output_lines.append(sub_text)
                else:
                    output_lines.append(block_text)
        else:
            output_lines.append('')
            i += 1
    
    # Post-process: remove excessive blank lines (more than 2 consecutive)
    result = '\n'.join(output_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = result.strip() + '\n'
    
    return result, publish_date


def main():
    if len(sys.argv) < 2:
        print("Usage: python strip_chinese_bilingual.py <input.md> [output.md]")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path.with_stem(input_path.stem + '-en')
    
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)
    
    result, publish_date = extract_english(input_path)
    
    # Use publish date for filename if available, otherwise keep input stem
    if publish_date and output_path is None:
        slug = re.sub(r'[^\w\-]', '-', input_path.stem)[:60]
        output_path = input_path.with_stem(f'{publish_date}-{slug}')
    elif output_path is None:
        output_path = input_path.with_stem(input_path.stem + '-en')
    
    output_path.write_text(result, encoding='utf-8')
    
    # Stats
    orig_size = input_path.stat().st_size
    new_size = output_path.stat().st_size
    print(f"Input:  {input_path.name} ({orig_size:,} bytes)")
    print(f"Output: {output_path.name} ({new_size:,} bytes)")
    print(f"Ratio:  {new_size/orig_size*100:.1f}%")


if __name__ == '__main__':
    main()
