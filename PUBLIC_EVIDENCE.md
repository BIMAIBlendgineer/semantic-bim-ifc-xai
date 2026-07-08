# Public Evidence

This repository contains a public, reduced, and sanitized evidence layer for the sample20 public artifact.

## Current public status

`RESEARCH_PASS`

## Public Executable Checks

| Check | Public executable? | Command/path | Status | Notes |
| --- | --- | --- | --- | --- |
| JSON parse | yes | `python harness/replay.py --sample sample20/` | PASS | 20 records parsed |
| Schema validation | yes | `python harness/replay.py --sample sample20/` | PASS | Minimal public contract satisfied |
| Replay | yes | `python harness/replay.py --sample sample20/` | PASS | Deterministic replay completed |
| Evidence trace presence | yes | `sample20/sample20_public_records.jsonl` | PASS | Each record includes evidence-linked output fields |
| Forbidden pattern scan | yes | repository scan | PASS | Public surface contains no prohibited private markers |
| Leakage/dedupe | no | methodology only | METHODOLOGICAL | Not exposed as a public executable check |
| NER sanitization | no | methodology only | METHODOLOGICAL | Not exposed as a public executable check |

## Evidence Included

- Public sample20 records.
- Public smoke/replay execution over sample20.
- Public sample validation summary.
- Replay harness.
- Schema validator helper.

## Evidence Interpretation

The current evidence shows that a public sanitized sample can be replayed and validated with auditable outputs under a controlled research setting.

The evidence does not claim:

- Product readiness.
- Normative certification.
- Full BIM compliance.
- Deployment approval.
- Exhaustive benchmark coverage.
