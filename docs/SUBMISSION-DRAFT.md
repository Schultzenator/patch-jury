# Patch Jury — Evidence before merge

**Draft — not submitted.** Live inference, registration and final video are pending. Do not turn implementation plans into claims of completed integration.

**Tagline:** Compare competing fixes with boundary tests and executable evidence.

**Track:** Coding and Agentic Engineering.

## Inspiration

A patch can pass the regression's obvious test and still break an empty input, rounding tie, or touching interval. Maintainers need a concrete counterexample they can inspect, not another confident score from a language model.

## What it does

Patch Jury compares a buggy base with two alternative fixes for three original miniature regressions. It separates smoke cases, challenge cases, and held-out cases. Each result includes the exact input, specification-derived expectation, observed output, source hash, and execution time. A maintainer can export the evidence as JSON.

Offline examples work without an API key and are explicitly identified as hand-authored. The live path is designed to request boundary inputs from NVIDIA Nemotron through Nebius Token Factory. Live authentication and inference have not yet been verified.

## How we built it

Python handles validation, trusted oracles, cost accounting, and Docker execution. TypeScript supplies a small local comparison interface. Model output is data, never executable code. Each fixture variant runs in a network-disabled, read-only container with resource limits, without the model key. Held-out cases and competing patches are excluded from the model prompt.

The selected model is NVIDIA Nemotron 3.5 Lightning. A durable budget ledger reserves one cent per call and caps project reservations at ten dollars. Before requesting inference, the application checks current official catalog prices and requires explicit confirmation of free credits.

## Results demonstrated so far

Across three authored suites, both competing patches pass the smoke case, while the additional cases distinguish the symptom fix from the reference fix. Reference fixes pass 27/27 combined cases. This is a small synthetic demonstration, not a blind evaluation of model-generated tests or a correctness proof.

## Challenges

The useful boundary between model and execution is narrow: ask the model to suggest inputs, validate them, and let a deterministic oracle and constrained runner produce evidence. Docker behavior, timeout cleanup, budget concurrency, and same-origin request handling are tested. Account access and a real Nebius call remain release gates.

## What's next

After live validation, measure the incremental discriminatory value of generated cases separately from authored holdouts. Expand fixture coverage, support richer trusted oracles, and investigate stronger isolation before considering arbitrary repositories.

## Nebius / NVIDIA feedback — draft

The public catalog's machine-readable model IDs, context limits, regional information and prices made bounded integration straightforward. We selected a compact NVIDIA model for inexpensive input generation. We cannot yet provide feedback on authenticated inference quality, latency, free-credit activation, or operational reliability: those observations require a real call and must be added after testing. No AI Cloud deployment or fine-tuning has been performed.

## Submission fields still required

- Public repository URL: https://github.com/Schultzenator/patch-jury
- Working demo/test build URL: https://github.com/Schultzenator/patch-jury/releases/tag/v0.1.0-preview (installable local test build; not a hosted service).
- Public YouTube video URL: pending; preview MP4 is not a substitute.
- Live evidence: request ID, returned model, usage and authentic live demo.
- Eligibility, terms, tools feedback and final confirmation: review actual Devpost fields.
- IRL city: do not select a city unless actual attendance is confirmed.
