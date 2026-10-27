# 80-second submission demo

New artifact: [submission/submission-offline.mp4](submission/submission-offline.mp4), 1280×720 H.264/AAC, English TTS, no face. It is an edited sequence of **actual local application screen captures**, not continuous interaction footage. All application results are real Docker runs with hand-authored inputs. The full-width label discloses offline mode on every frame. The ENV card is a placeholder, not evidence of inference. The old `preview.mp4` is a separate 116-second terminal replay.

## Shot list and voice-over (80 seconds)

| Time | Capture / action | Message |
| --- | --- | --- |
| 00–08 | Landing page | Two fixes can pass the smoke test but differ on root cause. |
| 08–16 | Fixture and offline selector | Explicit offline disclosure; compare bundled patches. |
| 16–28 | Result and verdict | Validate inputs, use trusted expectations, execute all variants. |
| 28–40 | Source cards and group counts | B passes the suite; A has counterexamples despite green smoke. |
| 40–54 | Distinguishing cases | Inspect exact input, expected value and actual outputs. |
| 54–64 | Money regression | Repeat the same workflow on decimal rounding. |
| 64–74 | ENV placeholder card | Where NVIDIA Nemotron and Nebius enter; key remains owner supplied. |
| 74–80 | Application / close | Export evidence; human retains merge decision. |

Full English narration: [submission-narration.txt](submission-narration.txt). Eight captured PNGs and FFmpeg concat timeline: [submission/](submission/).

## Reproduce the offline render

Requires running Docker with the pinned image already pulled, Python, Pillow, Playwright, Chrome, espeak and FFmpeg. These are optional video build tools, not application runtime dependencies. Port 8000 must be free.

```bash
python3 -m pip install pillow playwright
# Set CHROME to a Chrome/Chromium executable if not on PATH.
TMPDIR=/tmp FFMPEG=/path/to/ffmpeg python3 scripts/render_submission_demo.py
```

The script starts and stops its own localhost server, captures real offline results and a sanitized placeholder card, writes `evidence/submission-pages.json`, and renders an 80-second MP4. No account session is opened. Generated narration WAV is ignored by Git. Local Factory FFmpeg used for this render: `/tmp/flight-video-tools/node_modules/ffmpeg-static/ffmpeg`.

## Owner's live capture (60–90 seconds)

After the owner verifies credits and injects ENV, restart the server. Record only the application window at 1280×720 or higher. Use the same 80-second structure, replacing the placeholder/offline section with a real selection of **Nemotron · live Nebius API**, the request, real results and exported live provenance. Keep the waiting interval honest or mark the edit. Show the returned NVIDIA model, request ID and token usage; do not expose the key or console. Export evidence during the capture. If generated inputs do not distinguish patches, report that and separate the authored holdout contribution.

Replace the offline narration with observed facts, remove the offline banner only from authenticated footage, retain finite-suite limitations, and review playback before publishing. Public YouTube upload and submission are PW steps. The offline MP4 is a production rehearsal and cannot establish the mandatory Nebius runtime call.
