# Ganesh Pancharatnam — 24/7 YouTube Loop Stream

A still Ganpati image + an AI-generated Ganesh Pancharatnam chant, assembled
into one video and streamed to YouTube Live on an infinite loop via GitHub
Actions — same pattern as [youtube-247-loop-stream](../youtube-247-loop-stream),
kept as a separate project/repo per your call.

## Pipeline

1. Drop your Ganpati image in `image/` (`.jpg`/`.png`).
2. Drop your AI-generated audio in `audio/` (`.mp3`/`.wav`/`.m4a`/`.aac`).
3. Run `scripts/make-video.ps1` — holds the image still for the exact
   length of the audio track, outputs `video/loop.mp4`.
4. Commit + push `video/loop.mp4`. The GitHub Actions workflow loops *that*
   file forever into YouTube RTMP (so the image+chant repeats back-to-back,
   seamlessly, for as long as the stream runs).

`image/` and `audio/` are gitignored (raw source files stay local, only the
assembled `video/loop.mp4` gets committed) — see `.gitignore`.

## Setup

### 1. Build the video

```powershell
.\scripts\make-video.ps1
```

Check `video/loop.mp4` afterward — if it's over ~50-80MB, re-run with the
image pre-shrunk (e.g. resize to 1280px wide) or re-encode the audio at a
lower bitrate first; GitHub hard-blocks files over 100MB.

### 2. YouTube Live (same account/channel setup as the first project)

YouTube Studio → Go Live → Stream → copy your **Stream key**. If this is a
*different* channel than the first stream, you'll need its own key — the
two streams can't share one YouTube live broadcast.

### 3. Create the GitHub repo (public, for free unlimited Actions minutes)

```bash
git init
git add .
git commit -m "Initial Ganesh Pancharatnam loop stream setup"
git branch -M main
```

Then create an empty **public** repo on [github.com/new](https://github.com/new)
(no README/gitignore added there), and:

```bash
git remote add origin https://github.com/<your-username>/ganesh-pancharatnam-loop.git
git push -u origin main
```

### 4. Add the stream key secret

Repo → Settings → Secrets and variables → Actions → New repository secret
→ name it exactly `YT_STREAM_KEY` → paste the value from step 2.

### 5. Start it

Actions tab → "Ganesh Pancharatnam 24/7 Stream" → **Run workflow**. The
cron schedule (every 6 hours) keeps it going after that with no further
action needed.

## Known limitations

Same as the first project: a short gap (~1-10 min, occasionally more) at
each ~6-hour restart boundary due to GitHub's job cap + cron scheduling
jitter. See [youtube-247-loop-stream/README.md](../youtube-247-loop-stream/README.md#known-limitations)
for the full writeup and the gap-free (non-GitHub) alternative if that
matters for a devotional stream.
