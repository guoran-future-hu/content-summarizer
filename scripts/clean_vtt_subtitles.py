"""Clean YouTube auto-generated VTT to plain text.
Removes: <c> tags, inline timestamps (<00:00:00.000>), duplicate consecutive lines.
"""
import re, sys

def clean_vtt(text: str) -> str:
    lines = text.split('\n')
    result = []
    prev = ''
    
    for line in lines:
        # Skip VTT header
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        # Skip timestamp lines
        if re.match(r'^\d\d:\d\d:\d\d\.\d\d\d --> ', line):
            continue
        # Skip alignment/position lines
        if line.startswith('align:') or line.startswith('position:'):
            continue
        # Skip empty lines
        stripped = line.strip()
        if not stripped:
            continue
        # Remove <c> tags
        cleaned = re.sub(r'</?c>', '', stripped)
        # Remove inline timestamps
        cleaned = re.sub(r'<\d\d:\d\d:\d\d\.\d{3}>', '', cleaned)
        # Skip lines that are still just timestamps or numbers
        if re.match(r'^[\d\s\.:]+$', cleaned):
            continue
        # Collapse multiple spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        if not cleaned:
            continue
        # Deduplicate consecutive lines
        if cleaned != prev:
            result.append(cleaned)
            prev = cleaned
    
    return '\n'.join(result)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
        out = clean_vtt(text)
        outpath = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].replace('.vtt', '-transcript.md')
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(out)
        print(f'{len(out)} chars -> {outpath}')
    else:
        text = sys.stdin.read()
        print(clean_vtt(text))
