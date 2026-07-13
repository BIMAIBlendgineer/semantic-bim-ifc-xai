# Examples

This folder contains reduced public examples for Semantic XAIBIM.

## Public Sample Dataset

The canonical public sample dataset is located at:

    ../sample20/sample20_public_records.jsonl

Do **not** maintain a separate copy in this folder. The canonical copy is
validated by `scripts/verify_public_sample20_integrity.py`, which checks that
exactly three identical copies exist:

- `sample20/sample20_public_records.jsonl`
- `spaces/huggingface/sample20_public_predictions.jsonl`
- `spaces/huggingface_harness/sample20_public_predictions.jsonl`

All three copies are verified to be byte-for-byte identical (SHA-256 match).
Any additional copy outside this set breaks the integrity check.

## Sample Prompts

See `sample_prompts.md` for illustrative prompts that cover the semantic
BIM/IFC task categories represented in the sample dataset.

## Schema

The public schema is:

    sample20/schema_public_sample20_v2.json

It uses JSON Schema Draft 2020-12 and enforces the strict public sample20 v2
contract. See `sample20/README.md` for details.
