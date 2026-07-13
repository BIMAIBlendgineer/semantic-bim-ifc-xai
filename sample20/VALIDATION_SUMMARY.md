# sample20 Validation Summary

Status: `PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`

## Public Executable Checks

| Check | Public executable? | Command/path | Status | Notes |
| --- | --- | --- | --- | --- |
| JSON parse | yes | `python harness/schema_validator.py sample20/sample20_public_records.jsonl` | PASS | 20 records successfully parsed |
| Strict public sample20 v2 contract validation (JSON Schema Draft 2020-12) | yes | `python harness/schema_validator.py sample20/sample20_public_records.jsonl --schema sample20/schema_public_sample20_v2.json` | PASS | Validated against strict public sample20 v2 contract |
| Replay | yes | `python harness/replay.py --sample sample20/` | PASS | Deterministic public replay completed successfully |
| Evidence trace presence | yes | `python harness/schema_validator.py sample20/sample20_public_records.jsonl` | PASS | Verified presence and non-emptiness of evidence_trace |
| Forbidden pattern scan | yes | `python scripts/public_forbidden_scan.py` | PASS | Scans tracked files for forbidden patterns and credentials |
| Leakage/dedupe | no | `not exposed as public executable check` | METHODOLOGICAL | Handled as a methodology-only process |
| NER sanitization | no | `not exposed as public executable check` | METHODOLOGICAL | Handled as a methodology-only process |

## Notes

- `sample20` is the public sanitized sample dataset.
- `smoke20` is the replay/validation run executed on `sample20`.
- The public sample contains 20 records: 18 valid positive cases and 2 expected canonical rejections.
- Expected metrics are: `canonical_validation_rate = 0.9` and `expectation_met_rate = 1.0`.
- This summary reports public evidence only.
