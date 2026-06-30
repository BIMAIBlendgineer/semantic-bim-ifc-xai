# Public/Private Research Boundary

This document defines the explicit boundary between what is publicly available in
this repository and what remains within the private research infrastructure.

---

## Purpose

The public/private boundary exists to ensure:

1. **Scientific Reproducibility**: External reviewers can access enough material
   to verify the methodology and replay the validation harness.
2. **Data Privacy**: No real-world project data, proprietary model weights,
   client identifiers, or infrastructure details are exposed.
3. **Academic Integrity**: The public surface accurately represents what has
   been built and validated, without overstating production readiness or
   institutional endorsements.

---

## What Is Publicly Available

| Category | Artifact | Location |
|---|---|---|
| Sanitized dataset | `sample20` (20 synthetic records) | `sample20/` |
| Replay harness | Deterministic validation code | `harness/` |
| Interactive harness | Hugging Face Space code | `spaces/huggingface_harness/` |
| Benchmark protocol | Evaluation metric definitions | `benchmark/` |
| Methodology docs | Dataset construction, validation gates, XAI position | `docs/methodology/` |
| Bibliography | IEEE references [1]–[24] | `docs/literature/` |
| Public boundary | This document | `docs/public_boundary.md` |
| Hugging Face Replay Space | Interactive record browser | https://huggingface.co/spaces/bimaiblend/semantic-xaibim-replay |
| Hugging Face Harness Space | Interactive validation harness | https://huggingface.co/spaces/bimaiblend/semantic-xaibim-harness |

---

## What Is Not Published

| Category | Reason |
|---|---|
| private pilot dataset | Private development pilot; contains curated cases not yet sanitized for public release |
| private high-fidelity internal dataset | Private high-fidelity seed dataset used for closed-loop testing |
| Fine-tuned adapter weights | No private model checkpoints are in this repository |
| Production inference infrastructure | Private cloud configuration and API routing |
| private commercial or project data | Proprietary client project data, corporate identifiers |
| Raw user feedback events | Unprocessed events; must pass sanitization gates before becoming dataset candidates |
| Internal database schemas | SQL migrations for private admin cluster |
| Local workspace paths | No internal filesystem paths are published |

---

## Enforcement

The public boundary is enforced by:

1. **Gate 11 (Public/Private Boundary Verification)** of the validation gate
   matrix, applied to every dataset record.
2. **Forbidden patterns scan (Gate 10)**, which rejects files containing real
   credentials, absolute local paths, or private model filenames.
3. **`.gitignore` rules** in this repository excluding private data directories
   and model weight file extensions.

---

## Repository Rename Notice

This repository was previously named `BIMAIBlendgineer/semantic`. It has been
renamed to `BIMAIBlendgineer/semantic-bim-ifc-xai` to more accurately reflect
its academic scope and research focus.

The Hugging Face Space names (`semantic-xaibim-replay`,
`semantic-xaibim-harness`) remain unchanged pending a separate decision on
Space naming.

---

## Institutional Disclaimer

This repository does not represent an endorsement from any university,
research centre, funding agency, or institutional partner. It is an
independent academic research artifact maintained by the BIMAIBlendgineer
research group.
