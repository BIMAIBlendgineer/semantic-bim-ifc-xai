# Changelog

## v0.1.1-public-validation - public validation cleanup

- Strengthened the public `sample20` schema validator.
- Strengthened replay checks for required fields, types and evidence traces.
- Added public forbidden-pattern scan for local paths, credentials, private artifacts and boundary violations.
- Added README coverage for public folders.
- Added schema contract mapping for public record envelope, semantic output contract and demo validation.
- Updated public benchmark terminology from hard-block wording to human-review / non-executable preview wording.
- Updated Hugging Face harness wording to align with IFC-aware semantic contract, evidence trace and validation/replay.
- Added `.gitignore` coverage for generated harness preview models.
- Confirmed that no private datasets, checkpoints, adapters or secrets are included.
- This release does not introduce a complete corpus, trained model, production system, certification tool or final A1 benchmark.

## v0.1-public-sample20 - public sample snapshot

- Added the public sample20 entrypoint and quickstart.
- Added replay and schema validation for the public sample20 artifact.
- Added benchmark sample20 public results and evidence-grounded wording.
- Clarified the public/private boundary for public review.
- Confirmed that no private datasets, checkpoints, or adapters are included.
