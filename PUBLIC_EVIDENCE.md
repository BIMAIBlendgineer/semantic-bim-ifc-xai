# Public Evidence

This repository contains a public, reduced, and sanitized evidence layer for the sample20 public artifact.

## Current public status

`RESEARCH_PASS`

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

## Evidence Included

- Public sample20 records.
- Public smoke/replay execution over sample20.
- Public sample validation summary.
- Replay harness.
- Schema validator helper.
- Public forbidden scan utility script.

## Evidence Interpretation

The current evidence shows that a public sanitized sample can be replayed and validated with auditable outputs under a controlled research setting.

The evidence does not claim:

- Product readiness.
- Normative certification.
- Full BIM compliance.
- Deployment approval.
- Exhaustive benchmark coverage.
