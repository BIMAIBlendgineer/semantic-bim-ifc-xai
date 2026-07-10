# sample20 Validation Summary

Status: `RESEARCH_PASS`

## Public Executable Checks

| Check | Public executable? | Command/path | Status | Notes |
| --- | --- | --- | --- | --- |
| JSON parse | yes | `python harness/schema_validator.py sample20/sample20_public_records.jsonl` | PASS | 20 records successfully parsed |
| Minimal public contract validation | yes | `python harness/schema_validator.py sample20/sample20_public_records.jsonl` | PASS | Verified types, values, and required schema keys |
| Replay | yes | `python harness/replay.py --sample sample20/` | PASS | Deterministic public replay completed successfully |
| Evidence trace presence | yes | `python harness/schema_validator.py sample20/sample20_public_records.jsonl` | PASS | Verified presence and non-emptiness of evidence_trace |
| Forbidden pattern scan | yes | `python scripts/public_forbidden_scan.py` | PASS | Scans tracked files for forbidden patterns and credentials |
| Leakage/dedupe | no | `not exposed as public executable check` | METHODOLOGICAL | Handled as a methodology-only process |
| NER sanitization | no | `not exposed as public executable check` | METHODOLOGICAL | Handled as a methodology-only process |

## Notes

- `sample20` is the public sanitized sample dataset.
- `smoke20` is the replay/validation run over `sample20`.
- This summary reports public evidence only.
