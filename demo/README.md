# Demo production

`preview.mp4` is a <3 minute **offline terminal recording replay with English TTS**, not a final live Nebius demonstration. No face, personal mail, credentials or fabricated API activity. `terminal-recording.json` contains the actual CLI outputs; `scripts/make_demo.py` captures them and renders the terminal replay. Frame timing is edited for readability. The CLI reports are real executions; no pass/fail text is invented.

Run `python3 scripts/make_demo.py` with Pillow, `espeak`, and FFmpeg installed. Set `FFMPEG` if it is not on PATH. The resulting video and first frame are local artifacts. Narration is in `narration.txt`.

Final video plan (<180 seconds):
1. 0:00–0:15: maintainer problem and two green smoke tests.
2. 0:15–0:45: choose a fixture; request real Nemotron inputs with visible live provenance.
3. 0:45–1:20: inspect distinguishing cases, show all three variant results and held-out group.
4. 1:20–1:50: export the real report; show returned NVIDIA model, usage and source hashes.
5. 1:50–2:20: repeat a boundary case on another fixture; explain finite-test limits and isolation.
6. 2:20–2:40: show repository and test-build setup, tools feedback based on actual use.

Capture only the application window and sanitized report. Do not show account settings, a secret-bearing terminal, owner face, or private inbox. Publish final video as public YouTube and verify playback signed out. Publication is pending account/browser access.
