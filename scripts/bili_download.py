#!/usr/bin/env python3
"""
Bilibili audio downloader for content-summarizer.

Downloads the best available audio stream and can convert it to a
16 kHz mono PCM WAV suitable for Whisper or other ASR systems.
"""

import argparse
import glob
import json
import os
import subprocess
import sys


def run(cmd, **kwargs):
    """Run a subprocess with stable UTF-8 decoding on Windows."""
    return subprocess.run(
        cmd,
        encoding="utf-8",
        errors="replace",
        **kwargs,
    )


def find_executable(name):
    """Find a tool on PATH or in QClaw's common local tool directories."""
    search_paths = [
        os.path.join(os.path.expanduser("~"), ".qclaw", "tools"),
        os.path.join(os.path.expanduser("~"), ".qclaw", ".venv", "Scripts"),
    ]
    try:
        run([name, "--version"], capture_output=True, check=True)
        return name
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    for path in search_paths:
        exe = os.path.join(path, name + ".exe")
        if os.path.exists(exe):
            return exe
        plain = os.path.join(path, name)
        if os.path.exists(plain):
            return plain
    return None


FFMPEG = None
YTDLP = None

# Referer and Origin are required for many Bilibili requests; this handles
# public videos without cookie handling.
BILI_HEADERS = [
    "--add-header",
    "Referer:https://www.bilibili.com",
    "--add-header",
    "Origin:https://www.bilibili.com",
    "--add-header",
    "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]


def ensure_deps():
    global FFMPEG, YTDLP
    YTDLP = find_executable("yt-dlp")
    FFMPEG = find_executable("ffmpeg")
    if not YTDLP:
        print("[FAIL] yt-dlp was not found")
        sys.exit(1)
    if not FFMPEG:
        print("[FAIL] ffmpeg was not found")
        sys.exit(1)
    print(f"[OK] yt-dlp: {YTDLP}")
    print(f"[OK] ffmpeg: {FFMPEG}")


def list_formats(url):
    """List available media formats for the URL."""
    run([YTDLP] + BILI_HEADERS + ["-F", url], check=True)


def pick_best_audio(url):
    """Select the highest-bitrate audio-only stream."""
    result = run([YTDLP] + BILI_HEADERS + ["-J", url], capture_output=True, check=True)
    info = json.loads(result.stdout)
    formats = info.get("formats", [])
    audio_only = [fmt for fmt in formats if fmt.get("resolution") == "audio only"]
    if not audio_only:
        print("[FAIL] No audio-only stream was found")
        sys.exit(1)

    best = max(audio_only, key=lambda fmt: fmt.get("tbr", 0) or fmt.get("abr", 0) or 0)
    format_id = best["format_id"]
    bitrate = best.get("abr") or best.get("tbr", "?")
    size_mb = (best.get("filesize") or best.get("filesize_approx", 0)) / (1024 * 1024)
    print(f"[INFO] Selected audio: id={format_id}, bitrate={bitrate} kbps, approx {size_mb:.1f} MB")
    return format_id


def download_audio(url, output_dir, format_id="bestaudio"):
    """Download one audio stream and return the newest downloaded file."""
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    cmd = [YTDLP] + BILI_HEADERS + ["-f", format_id, "-o", output_template, url]
    print(f"[DL] URL: {url}")
    print(f"[DIR] Output: {output_dir}")
    run(cmd, check=True)

    audio_files = glob.glob(os.path.join(output_dir, "*.m4a")) + glob.glob(os.path.join(output_dir, "*.mp4"))
    audio_files.sort(key=os.path.getmtime, reverse=True)
    if not audio_files:
        print("[FAIL] Download finished but no audio file was found")
        sys.exit(1)
    return audio_files[0]


def audio_info(filepath):
    """Print duration and audio stream details from ffmpeg stderr."""
    result = run([FFMPEG, "-i", filepath], capture_output=True)
    for line in (result.stderr or "").splitlines():
        if "Duration" in line or "Audio:" in line:
            print(f"  {line.strip()}")


def convert_to_whisper(input_path, output_path=None):
    """Convert audio to 16 kHz mono PCM WAV."""
    if output_path is None:
        base = os.path.splitext(input_path)[0]
        output_path = base + "_16k_mono.wav"
    cmd = [FFMPEG, "-i", input_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", output_path, "-y"]
    print(f"[CONVERT] {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
    run(cmd, capture_output=True, check=True)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  [OK] {size_mb:.1f} MB")
    return output_path


def convert_to_mp3(input_path, output_path=None):
    """Convert audio to MP3."""
    if output_path is None:
        base = os.path.splitext(input_path)[0]
        output_path = base + ".mp3"
    cmd = [FFMPEG, "-i", input_path, "-vn", "-acodec", "libmp3lame", "-q:a", "2", output_path, "-y"]
    print(f"[CONVERT] {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
    run(cmd, capture_output=True, check=True)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  [OK] {size_mb:.1f} MB")
    return output_path


def list_and_pick(url):
    """List formats, then prompt for a format id."""
    print("\n--- Available formats ---")
    list_formats(url)
    format_id = input("\nEnter format id, or leave blank for best audio: ").strip()
    return format_id if format_id else pick_best_audio(url)


def main():
    parser = argparse.ArgumentParser(description="Download Bilibili audio and create Whisper-ready files.")
    parser.add_argument("--url", required=True, help="Bilibili video URL or BV id")
    parser.add_argument(
        "--output",
        "-o",
        default=os.path.join(os.path.expanduser("~"), "Desktop", "bilibili_downloads"),
        help="Output directory (default: Desktop/bilibili_downloads)",
    )
    parser.add_argument("--whisper", action="store_true", help="Also write a 16 kHz mono WAV")
    parser.add_argument("--mp3", action="store_true", help="Also write an MP3 file")
    parser.add_argument("--list", "-F", action="store_true", help="Only list available formats")
    parser.add_argument("--format", "-f", default="auto", help="Format id (default: auto selects best audio)")
    parser.add_argument("--pick", action="store_true", help="List formats and choose interactively")

    args = parser.parse_args()
    ensure_deps()

    if args.pick:
        format_id = list_and_pick(args.url)
    elif args.list:
        list_formats(args.url)
        return
    elif args.format != "auto":
        format_id = args.format
    else:
        format_id = pick_best_audio(args.url)

    audio_file = download_audio(args.url, args.output, format_id=format_id)
    print(f"[DONE] Downloaded: {os.path.basename(audio_file)}")
    audio_info(audio_file)

    outputs = [audio_file]
    if args.mp3:
        outputs.append(convert_to_mp3(audio_file))
    if args.whisper:
        outputs.append(convert_to_whisper(audio_file))

    print("\n--- Output files ---")
    for path in outputs:
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"  {os.path.basename(path)} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
