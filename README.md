# Patch Jury

**Two patches. Let the tests speak.**

Patch Jury helps a maintainer see whether a fix addresses a regression or only its most obvious symptom. It asks NVIDIA Nemotron on Nebius Token Factory for boundary inputs, supplies expected answers from a trusted specification oracle, and executes the base and two competing fixes in separate network-disabled containers. The report exposes individual inputs, expected and actual values, source hashes, and model provenance.

**Current status:** working local MVP with three original bundled regressions. Offline examples and Docker execution have been tested. Live inference is implemented but has **not** been exercised against an authenticated Nebius account. Offline examples are hand-authored, not recorded model responses. The offline submission kit is ready; authenticated live evidence and publication remain owner steps.

Public repository: https://github.com/Schultzenator/patch-jury

Preview release: https://github.com/Schultzenator/patch-jury/releases/tag/v0.1.1-preview

## Run the test build

Requirements: Python 3.12+ and a running Docker daemon. No Python packages required. Docker execution was tested on Linux; Docker Desktop paths on other platforms are unverified.

```sh
docker pull "$(cat runner-image.txt)"
python3 -m patchjury --serve
# Open http://127.0.0.1:8000
```

The compiled browser code is included. To modify TypeScript, install Node 20+ and run `npm ci && npm run build`.

```sh
python3 -m patchjury --fixture pages --output report.json
python3 -m patchjury --fixture money --output report.json
python3 -m patchjury --fixture intervals --output report.json
PATCHJURY_INTEGRATION=1 python3 -m unittest discover -s tests -v
```

The HTTP app binds to localhost and is designed for a single operator. It is not a public multi-user service. Do not expose the Docker socket or this server to the internet. The downloadable repository is the test build; public deployment is not yet provided.

## Live NVIDIA inference on Nebius

Confirm that free credits are active in your own account, then inject the API key from a secret store into `NEBIUS_API_KEY` and set `NEBIUS_CREDITS_CONFIRMED=yes`. Do not put credentials in source, a URL, browser storage, or a report.

```sh
# Use a local shell; the key is hidden while typed and is never stored in Git.
read -rsp 'Nebius API key: ' NEBIUS_API_KEY; echo
export NEBIUS_API_KEY
export NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1
export MODEL=nvidia/Nemotron-3_5-Lightning
export NEBIUS_CREDITS_CONFIRMED=yes  # only after owner verifies credits
python3 -m patchjury --fixture pages --live --output live-report.json
# Or: python3 -m patchjury --serve, then choose Nemotron · live Nebius API.
# Restart an already running server after changing ENV.
```

`.env.example` documents all variables; `.env` is not loaded automatically. No code change is needed to switch to live. `NEBIUS_BASE_URL` is an HTTPS API base ending in `/v1` (not `/chat/completions`). `MODEL` must be an NVIDIA model in the official catalog within the price ceilings below. Defaults select `nvidia/Nemotron-3_5-Lightning` and `https://api.tokenfactory.nebius.com/v1`. Custom endpoints must be trusted by the operator because they receive the API key.

The juror input-generation step calls `POST {NEBIUS_BASE_URL}/chat/completions` with a Bearer key, the chosen model, temperature 0 and JSON output. NVIDIA Nemotron supplies candidate boundary arguments; the oracle, runner and verdict remain deterministic. The application checks catalog prices before inference, validates returned arguments, and records the endpoint, returned model, request ID and usage in the report and live UI. The selected model is listed in the official [catalog](https://tokenfactory.nebius.com/api/public/models_info) (rechecked 27 October 2026). Tests exercise mocked HTTP contracts, not authenticated service compatibility. Live results can vary even at temperature 0.

If live fails, check key/credits, `/v1` URL, model availability, catalog price ceilings and Docker availability. Errors never silently fall back to offline; select offline explicitly. Unknown or more expensive models fail before inference. The $0.01 reservation is retained after failed inference attempts.

The model sees the specification and buggy base implementation, **not** either patch or the held-out cases. It cannot submit Python, commands, expected answers, URLs or filesystem paths for execution. The trusted oracle computes the expected answer; model-generated cases that violate the fixture's domain are rejected. No automatic retries or fine-tuning jobs.

## Example evidence

| Original regression | Base | Symptom fix A | Root fix B |
| --- | --- | --- | --- |
| Page count ceiling / empty input | 6/9 | 3/9 | 9/9 |
| Decimal half-up cents | 1/9 | 4/9 | 9/9 |
| Half-open interval overlap | 5/9 | 6/9 | 9/9 |

Each fix passes the single smoke test. The combined suite has one smoke case, three authored challenge cases and five held-out cases. `evidence/*.json` contains the actual container results. The holdout is excluded from the model prompt but is public source, not an independent blind benchmark. These three synthetic regressions demonstrate the workflow; they do not establish general accuracy on real pull requests. Passing finite tests does not prove correctness. Patch B is intentionally the reference fix in these educational fixtures.

## Isolation and budget

Each variant runs as UID 65534 in a digest-pinned Python image, with no network, a read-only filesystem and input mount, no Linux capabilities, no privilege escalation, 128 MB RAM, 32 PIDs, 0.5 CPU, limited file descriptors, and a host-enforced timeout. Containers receive no API key or host environment. Container timeout cleanup, blocked egress, read-only root and absent host secrets are integration tested. Docker shares the host kernel; this MVP deliberately accepts only bundled original code and does not promise safe execution of arbitrary public PRs.

The durable SQLite ledger `.state/budget.sqlite3` reserves **$0.01 per inference attempt**, including failures. At the catalog ceilings of $0.06 input and $0.24 output per million tokens, a <=20,000-byte request and <=4,096 output tokens cost below that reservation. Reservations serialize across concurrent processes and stop at $10. The public catalog fetch does not perform inference. Preserve the ledger and use one shared workspace for all project calls; deleting it or using independent installations defeats the project-wide cap. The app does not activate billing or attach a payment card. Credit balance remains an account-level prerequisite.

## Juror verdict

Select a bundled regression (base + symptom fix A + root fix B), then click **Compare patches**. Both fixes pass the smoke test; boundary cases expose their difference. The UI shows a verdict, per-group results, source, counterexamples and JSON export. A unique patch passing every evaluated case is `supported`; ties or two failing patches are `inconclusive`. This is a finite-suite recommendation for human review. The UI counts and the report separately lists challenge-only distinguishing cases so authored holdouts cannot be mistaken for model contribution.

Offline inputs, oracle expectations and pass/fail results are repeatable. Container timings and report hashes containing timings vary between runs. Docker is required offline; no network or API key is needed after the pinned runner image has been pulled.

## Architecture

`web/app.ts` → localhost JSON server → validated live inputs or explicitly labeled authored examples → specification oracle → three isolated fixture executions → JSON evidence and comparison UI.

`patchjury/provider.py` handles inference and budget. `fixtures.py` owns the three specifications and original source variants. `runner.py` owns isolation and report hashes. `server.py` exposes the local interface. No GitHub writes or automatic merge decision.

## Demo and submission

[Submission kit](SUBMISSION-KIT.md) · [80-second demo script](demo/README.md) · [Release checklist](docs/SUBMISSION-CHECKLIST.md).

The new [80-second offline demo](demo/submission/submission-offline.mp4) uses actual application screen captures, edited timing and English TTS. The key card is a labeled placeholder. [Captured frames](demo/submission/) and the rendering script are included. The older `demo/preview.mp4` is a terminal replay. Neither is authenticated live evidence or a public YouTube upload.

Created during the hackathon build window using AI coding assistance. MIT licensed original application and fixtures. Docker runtime image and NVIDIA model carry their own upstream licenses. No NVIDIA model weights are redistributed.
