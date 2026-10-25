# Patch Jury

**Two patches. Let the tests speak.**

Patch Jury helps a maintainer see whether a fix addresses a regression or only its most obvious symptom. It asks NVIDIA Nemotron on Nebius Token Factory for boundary inputs, supplies expected answers from a trusted specification oracle, and executes the base and two competing fixes in separate network-disabled containers. The report exposes individual inputs, expected and actual values, source hashes, and model provenance.

**Current status:** working local MVP with three original bundled regressions. Offline examples and Docker execution have been tested. Live inference is implemented but has **not** been exercised against an authenticated Nebius account. Offline examples are hand-authored, not recorded model responses. This is not yet a complete hackathon submission.

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
# After injecting the two environment variables into your shell:
python3 -m patchjury --fixture pages --live --output live-report.json
# Or restart the server and choose Nemotron · live Nebius API.
```

Model: `nvidia/Nemotron-3_5-Lightning`, verified against the official [machine-readable catalog](https://tokenfactory.nebius.com/api/public/models_info) on 25 October 2026. Endpoint: `https://api.tokenfactory.nebius.com/v1/chat/completions`. The application rechecks prices before every live call, blocks price increases, accepts only validated JSON argument lists, and records returned model ID, request ID and token usage. Provider contract tests use a mock and do not establish live API compatibility or account availability.

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

## Architecture

`web/app.ts` → localhost JSON server → validated live inputs or explicitly labeled authored examples → specification oracle → three isolated fixture executions → JSON evidence and comparison UI.

`patchjury/provider.py` handles inference and budget. `fixtures.py` owns the three specifications and original source variants. `runner.py` owns isolation and report hashes. `server.py` exposes the local interface. No GitHub writes or automatic merge decision.

## Demo and submission

[Draft description](docs/SUBMISSION-DRAFT.md) · [Demo script and production status](demo/README.md) · [Release checklist](docs/SUBMISSION-CHECKLIST.md).

The preview video is an English TTS narration over a faithful rendering of actual terminal recordings, clearly labeled offline. It contains no face or invented API activity. It is not the final live Nebius demonstration or a public YouTube upload.

Created during the hackathon build window using AI coding assistance. MIT licensed original application and fixtures. Docker runtime image and NVIDIA model carry their own upstream licenses. No NVIDIA model weights are redistributed.
