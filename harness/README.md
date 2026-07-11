# harness

## Purpose
The public harness is a lightweight replay and validation layer for testing record serialization, minimal schemas, and consistency checks on the public reproducibility sample.

## Contents
- `replay.py`: The public replay execution script.
- `schema_validator.py`: A Python-only schema validation helper for public JSONL records.
- `replay_harness.py`: Additional harness utility function support.

## What this folder does not contain
- It does not contain private datasets or model checkpoints.
- It does not contain a full BIM validator, model server, or certified IFC checker.
- It does not represent a production/certification tool.

## Related files
- `sample20/sample20_public_records.jsonl`: The target public dataset for replay.
- `sample20/schema_minimal.json`: The minimal schema validated by the harness.
