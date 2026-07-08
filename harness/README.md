# Harness

The public harness is a lightweight replay and validation layer.

It does not run a model.

## replay.py

- Entry point: `python harness/replay.py --sample sample20/`
- Input: `sample20/` or a direct JSONL path.
- Output: record count, JSON parse status, schema status, replay status, and a final `REPLAY_OK` or `REPLAY_FAIL`.

## What It Does

- Reads the public JSONL sample.
- Resolves `sample20/` to the canonical public file.
- Validates the minimal public contract.
- Reports a deterministic public replay summary.

## Limits

- It is not a model server.
- It is not a production BIM validator.
- It only checks the public sample surface.
