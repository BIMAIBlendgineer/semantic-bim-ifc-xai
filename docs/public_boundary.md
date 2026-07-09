# Public/Private Boundary

This document defines the public surface of the repository and the material that remains private.

## Purpose

The boundary exists to keep the repository reproducible, sanitized, and narrow enough for academic review.

## Publicly Available

| Category | Artifact | Location |
| --- | --- | --- |
| Sanitized dataset | `sample20` | `sample20/` |
| Replay harness | Public validation entrypoint | `harness/` |
| Benchmark sample results | Executed sample20 replay results | `benchmark/results_sample20.md` |
| Public evidence | Validation status and checks | `PUBLIC_EVIDENCE.md` |
| Methodology docs | Public validation and boundary notes | `docs/methodology/` |
| Hugging Face links | Public demo references | `README.md` |

## Not Published

| Category | Reason |
| --- | --- |
| Private pilot datasets | Not part of the public artifact |
| Private high-fidelity datasets | Not part of the public artifact |
| Fine-tuned adapter weights | Not included in the public repo |
| Production inference infrastructure | Not included in the public repo |
| Private commercial or project data | Not included in the public repo |
| Raw user feedback events | Not included in the public repo |
| Internal database schemas | Not included in the public repo |
| Local workspace paths | Not included in the public repo |

## Enforcement

The public boundary is enforced by:

1. Validation gates documented in `docs/methodology/validation_gates.md`.
2. Public pattern scans for forbidden private markers.
3. Repository hygiene rules that exclude private artifacts.

## Public Sample Note

`sample20` is the public sanitized sample dataset. `smoke20` is the replay/validation run executed against `sample20`; it is not a separate dataset.

## Disclaimer

This is an academic research artifact.
It is not a certification tool, production BIM service, or institutional endorsement.
It contains only public synthetic or sanitized examples.
