# sample20

`sample20` is the public sanitized sample dataset. `smoke20` is the public smoke/replay validation run executed against `sample20`; it is not a separate dataset.

## What It Is

- A small public dataset for academic review.
- A sanitized set of replayable public sample records.
- The canonical public input for `harness/replay.py`.

## What It Is Not

- It is not a private pilot dataset.
- It is not a training corpus for private adapters.
- It is not a certification dataset.
- It is not a separate `smoke20` dataset.

## How To Validate

1. Read `sample20/MANIFEST.md`.
2. Run `python harness/replay.py --sample sample20/`.
3. Review `PUBLIC_EVIDENCE.md` and `benchmark/results_sample20.md`.

## Limits

- The sample is intentionally small.
- It does not claim full XAI.
- It does not include private data or private weights.
- It is a public evidence surface, not a production BIM service.

See [../QUICKSTART.md](../QUICKSTART.md) for the minimal local run.

