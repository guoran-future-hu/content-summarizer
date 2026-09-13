# Bilibili → Chinese Transcript (STT)

Copy-paste recipe: Bilibili URL / BV id → Chinese transcript. STT mechanics and policy: `../source-acquisition.md`.

## When to use

- A Bilibili URL / BV id must become a Chinese transcript (跑/处理/转录), or be summarized from one — transcribe first.
- The video has no usable captions.

## 0. Login cookies

Path: `~/web-auth/bilibili-cookies.txt` (Netscape, 600). Check: `nav` → `data.isLogin: true`.

```bash
yt-dlp --cookies ~/web-auth/bilibili-cookies.txt --list-subs --skip-download <URL>
curl -s -b ~/web-auth/bilibili-cookies.txt https://api.bilibili.com/x/web-interface/nav
```

`isLogin: false` → re-scan the QR:

1. Open `https://passport.bilibili.com/login` in the browser session.
2. Read `qrcode_key` from the QR wrapper div's `title` attribute (`…scan-web?…&qrcode_key=<KEY>&from=main_web`).
3. Save the QR `<img src>` (base64 PNG, 140×140) to a file, upscale ×4 (`ffmpeg -vf scale=560:560:flags=neighbor`), send to the user (`MEDIA:<abs-path>`). Valid ~180 s.
4. Poll the key yourself every 3 s — the page is recycled between browser calls, so its own polling dies:
   `fetch('https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key=<KEY>', {credentials:'include'})`
   `data.code`: `0` = ok · `86090` = scanned, keep polling · `86038` = expired → issue a new QR.
5. `cdp('Network.getCookies', urls=['https://api.bilibili.com/','https://www.bilibili.com/','https://passport.bilibili.com/'])` → write the 7-column Netscape file → `~/web-auth/bilibili-cookies.txt`, `chmod 600`.
6. Confirm `nav` → `isLogin: true`.

SESSDATA is HttpOnly: it never shows in `document.cookie` — judge login only by `nav`.

## 1. Captions first (before any STT)

```bash
./scripts/bili_captions.sh "https://www.bilibili.com/video/<BV_ID>" <summary-root>/bilibili-<BVid>
```

- exit 0 → captions saved (`.srt` path on stdout) — skip STT entirely.
- exit 3 (`NO_CAPTIONS`) → go to §2.
- exit 1 → error: fix it first (login/headers/yt-dlp). Never read it as "no captions".
- Captions need the cookie jar (§0): logged-out sessions get the whole list hidden, so the script refuses to report NO_CAPTIONS then.
- `ai-zh` = AI captions; pass another code as the 3rd arg to override.
- Captions exist only if the UP has enabled them.

## 2. Audio (no captions)

```bash
./scripts/bili_audio.sh "https://www.bilibili.com/video/<BV_ID>" <summary-root>/bilibili-<BVid>
```

Output: `<summary-root>/bilibili-<BVid>/audio/<BV_ID>.16k.mp3` (path on stdout). The script does it all: format probe → resumable download (30216 → 30280 fallback) → 16 k mono mp3 → duration check vs metadata. Re-running with the output complete is a no-op.

- Public audio needs no login, so this step survives SESSDATA expiry. Premium-only videos: prefix `BILI_COOKIES=~/web-auth/bilibili-cookies.txt`.
- 多P: `BILI_PART=N` selects part N (default P1).
- Headers are baked into the script; the raw `HTTP Error 412` you see without them is a missing-header response, not an IP ban.
- 2 h+ sources: run it in the background with a completion notification — minutes of silence look like a hang.
- Unexplained parse failures (extractor error, empty format list, `Unable to download JSON metadata`) → update yt-dlp first: `uv pip install -U yt-dlp --python ~/.hermes/hermes-agent/venv/bin/python`.

## 3. Transcribe

Run `./scripts/stt.sh <summary-root>/bilibili-<BVid>` (defaults: `language=zh`, audio from `audio/*.16k.mp3`).

## 4. Post-process

- Draft: `./scripts/make_transcript.py <summary-root>/bilibili-<BVid>` (STT parts or the captions `.srt`) → `transcript.md`; then normalize per `../source-acquisition.md` (§ Audio and video sources).
- Apply fixes: `./scripts/apply_replacements.py transcript.md pairs.txt --table normalization.md`; header data: `./scripts/bili_meta.sh <url> <workdir>`; assemble: `./scripts/finalize_raw.py <workdir> --out <name>.md --table normalization.md ...`.
- Save the transcript in `<summary-root>/bilibili-<BVid>/`; no raw audio in skill repos — keep it in the output folder.
