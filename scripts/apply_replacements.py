#!/usr/bin/env python3
"""Apply normalization pairs to a transcript; report hit counts.

Usage: apply_replacements.py <file.md> <pairs.txt> [--dry-run] [--table OUT.md]

pairs.txt: one pair per line, "original=>fixed" or "original→fixed"; # comments and
blank lines allowed. Pairs are applied in order (counts are pre-replacement).
Prints a markdown table for the transcript header's normalization section and warns
on zero-hit pairs. Writes the file back unless --dry-run.

The pairs themselves are decided by hand (two-pass policy, source-acquisition.md);
this script only applies and counts them.
"""
import sys


def main():
    argv = sys.argv[1:]
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 2:
        sys.exit(__doc__)
    fpath, ppath = args[0], args[1]
    dry = "--dry-run" in argv
    table_out = argv[argv.index("--table") + 1] if "--table" in argv else None

    text = open(fpath, encoding="utf-8").read()
    pairs = []
    for ln in open(ppath, encoding="utf-8"):
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        sep = "=>" if "=>" in ln else ("→" if "→" in ln else None)
        if not sep:
            print("SKIP (no separator):", ln)
            continue
        a, b = (x.strip() for x in ln.split(sep, 1))
        if a:
            pairs.append((a, b))

    rows, zero = [], []
    for a, b in pairs:
        c = text.count(a)
        rows.append((a, b, c))
        if c == 0:
            zero.append(a)
        if not dry:
            text = text.replace(a, b)
    if not dry:
        open(fpath, "w", encoding="utf-8").write(text)

    table = ("| STT 原样 | 修正为 | 次数 |\n|---|---|---|\n"
             + "\n".join(f"| {a} | {b} | {c} |" for a, b, c in rows))
    print(table)
    if table_out:
        open(table_out, "w", encoding="utf-8").write(table + "\n")
    if zero:
        print("\nZERO-HIT (verify spelling):", " , ".join(zero))
    print(f"\n{len(rows)} pairs, {sum(c for _, _, c in rows)} replacements"
          f"{' (dry run)' if dry else ''}")


if __name__ == "__main__":
    main()
