#!/usr/bin/env python3
"""Build the draft transcript from STT part files or a caption .srt.

Usage:
  make_transcript.py <workdir> [--srt FILE] [--target SEC]

STT mode (default): joins <workdir>/stt/part_*.json. Text-only parts (gpt-4o-mini
transcribe output) become one paragraph each, anchored at the part's start
([HH:MM:SS], ~2 min grid); parts that carry segments are grouped into ~<target> s
paragraphs instead.

SRT mode (--srt FILE, or one <workdir>/*.srt when no STT parts exist): builds
<workdir>/transcript.md from a caption file; consecutive duplicate cues are dropped.

Output: <workdir>/transcript.md. Validates part contiguity, monotonic anchors,
per-part coverage; prints a report. Exit 1 on hard problems (missing/empty part,
non-monotonic, unknown duration); warnings printed inline.
"""
import glob
import json
import os
import re
import subprocess
import sys


def hms(t):
    t = int(t)
    return f"{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}"


def ffprobe_dur(p):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=nw=1:nk=1", p], capture_output=True, text=True)
        return float(r.stdout.strip())
    except Exception:
        return None


def load_json(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}


def group_paragraphs(entries, target):
    paras, cur, start = [], [], None
    for s, e, t in entries:
        if start is None:
            start = s
        cur.append(t)
        if e - start >= target or len(cur) >= 45:
            paras.append((start, "".join(cur)))
            cur, start = [], None
    if cur:
        paras.append((start, "".join(cur)))
    return paras


def parse_srt(text):
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l for l in block.splitlines() if l.strip()]
        hit = [i for i, l in enumerate(lines) if "-->" in l]
        if not hit:
            continue
        i = hit[0]
        m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", lines[i])
        if not m:
            continue
        g = m.groups()

        def sec(h, mn, s, ms):
            return int(h) * 3600 + int(mn) * 60 + int(s) + int(ms) / (10 ** len(ms))

        start, end = sec(*g[:4]), sec(*g[4:8])
        txt = " ".join(lines[i + 1:])
        txt = re.sub(r"<[^>]+>", "", txt)
        txt = re.sub(r"\{\\[^}]*\}", "", txt)
        txt = re.sub(r"\s+", " ", txt).strip()
        if not txt or (cues and txt == cues[-1][2].strip()):
            continue
        # Latin-script cues need an explicit separator; CJK cues must not get one.
        if re.search(r"[A-Za-z0-9\.,!?;:\)\]\"']$", txt):
            txt += " "
        cues.append((start, end, txt))
    return cues


def write_transcript(work, paras):
    out = f"{work}/transcript.md"
    chars = 0
    with open(out, "w", encoding="utf-8") as f:
        for s, t in paras:
            f.write(f"[{hms(s)}] {t}\n\n")
            chars += len(t)
    return out, chars


def stt_mode(work, target):
    parts = sorted(glob.glob(f"{work}/stt/part_*.json"))
    if not parts:
        sys.exit(f"ERROR: no stt/part_*.json in {work} — run stt.sh first")
    nums = [int(os.path.basename(p).split("part_")[1].split(".")[0]) for p in parts]
    hard, soft, paras = [], [], []
    if nums != list(range(len(nums))):
        hard.append(f"part numbering not contiguous: {nums}")
    offset = 0.0
    for i, p in enumerate(parts):
        n = nums[i]
        j = load_json(p)
        segs = j.get("segments") or []
        cand = glob.glob(f"{work}/segments/part_{n:02d}.*")
        pdur = (ffprobe_dur(cand[0]) if cand else None) or j.get("duration") or (segs[-1]["end"] if segs else None)
        if not pdur:
            hard.append(f"part_{n:02d}: duration unknown (no segments/ file and no duration field)")
            continue
        if segs:
            for a, b in zip(segs, segs[1:]):
                if b["start"] + 1e-6 < a["start"]:
                    hard.append(f"part_{n:02d}: timestamps not monotonic inside the part")
                    break
            if segs[-1]["end"] < pdur - 10:
                soft.append(f"part_{n:02d}: coverage {segs[-1]['end']:.0f}s of {pdur:.0f}s — check the tail")
            ents = [(s["start"] + offset, s["end"] + offset, s["text"]) for s in segs]
            paras.extend(group_paragraphs(ents, target))
        else:
            text = (j.get("text") or "").strip()
            if not text:
                hard.append(f"part_{n:02d}: no text")
                continue
            if len(text) < 20 * (pdur / 60):
                soft.append(f"part_{n:02d}: only {len(text)} chars for {pdur:.0f}s — verify coverage")
            paras.append((offset, text))
        offset += pdur
    starts = [s for s, _ in paras]
    if any(b < a for a, b in zip(starts, starts[1:])):
        hard.append("anchors not monotonic across parts")
    tpath, chars = write_transcript(work, paras)
    print(f"mode=stt parts={len(parts)} paras={len(paras)} duration={hms(offset)} chars={chars}")
    print(f"-> {tpath}")
    return hard, soft


def srt_mode(work, srt, target):
    cues = parse_srt(open(srt, encoding="utf-8-sig").read())
    hard, soft = [], []
    if not cues:
        hard.append("no cues parsed from the caption file")
    starts = [c[0] for c in cues]
    if any(b + 1e-6 < a for a, b in zip(starts, starts[1:])):
        hard.append("cues not monotonic")
    paras = group_paragraphs(cues, target)
    tpath, chars = write_transcript(work, paras)
    dur = cues[-1][1] if cues else 0
    print(f"mode=srt file={srt} cues={len(cues)} paras={len(paras)} duration={hms(dur)} chars={chars}")
    print(f"-> {tpath}")
    return hard, soft


def main():
    argv = sys.argv[1:]
    if not argv or argv[0].startswith("--"):
        sys.exit(__doc__)
    work = argv[0]
    target = float(argv[argv.index("--target") + 1]) if "--target" in argv else 90.0
    srt = None
    if "--srt" in argv:
        srt = argv[argv.index("--srt") + 1]
    elif not glob.glob(f"{work}/stt/part_*.json"):
        found = glob.glob(f"{work}/*.srt")
        if len(found) == 1:
            srt = found[0]
    hard, soft = srt_mode(work, srt, target) if srt else stt_mode(work, target)
    for w in soft:
        print("FLAG:", w)
    for h in hard:
        print("ERROR:", h)
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
