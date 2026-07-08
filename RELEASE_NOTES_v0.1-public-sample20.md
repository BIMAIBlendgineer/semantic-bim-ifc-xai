# Release Notes: v0.1-public-sample20

## Summary

This release candidate packages the public sanitized sample20 workflow for academic review.

## Public Artifacts

- `sample20/README.md`
- `sample20/MANIFEST.md`
- `sample20/VALIDATION_SUMMARY.md`
- `sample20/sample20_public_records.jsonl`
- `sample20/schema_minimal.json`
- `QUICKSTART.md`
- `PUBLIC_EVIDENCE.md`
- `benchmark/results_sample20.md`
- `harness/replay.py`
- `harness/schema_validator.py`

## Validation Commands

```bash
python harness/replay.py --sample sample20/
python harness/schema_validator.py sample20/sample20_public_records.jsonl
```

## Expected Outputs

- `JSON parse PASS`
- `schema PASS`
- `replay PASS`
- `status REPLAY_OK`

## Limitations

- The sample is intentionally small and public.
- The repository does not claim full mathematical XAI.
- The repository does not claim certification, production readiness, or benchmark finality.

## Not Included

- Private datasets
- Private checkpoints
- Private adapters
- Internal logs
- Non-public artifacts

## Suggested Tag After Human Review

`v0.1-public-sample20`
