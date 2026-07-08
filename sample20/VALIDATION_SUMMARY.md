# sample20 Validation Summary

Status: `RESEARCH_PASS`

## Public Executable Checks

| Check | Public executable? | Command/path | Status | Notes |
| --- | --- | --- | --- | --- |
| JSON parse | yes | `python harness/replay.py --sample sample20/` | PASS | 20 records parsed |
| Schema validation | yes | `python harness/replay.py --sample sample20/` | PASS | Minimal public contract satisfied |
| Replay | yes | `python harness/replay.py --sample sample20/` | PASS | Deterministic public replay |
| Evidence trace presence | yes | `sample20/sample20_public_records.jsonl` | PASS | Records contain evidence traces |
| Forbidden pattern scan | yes | repository scan | PASS | No prohibited public terms found in the public surface |
| Leakage/dedupe | no | methodology only | METHODOLOGICAL | Not exposed as an executable public check |
| NER sanitization | no | methodology only | METHODOLOGICAL | Not exposed as an executable public check |

## Notes

- `sample20` is the public sanitized sample dataset.
- `smoke20` is the replay/validation run over `sample20`.
- This summary reports public evidence only.

