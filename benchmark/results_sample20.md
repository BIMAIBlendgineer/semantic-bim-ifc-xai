# Public Sample20 v2 Results

These are public sample validation results over the public `sample20` v2 reproducibility sample. They are not representative of general model performance or generalization.

## Executed Replay

- Command: `python harness/replay.py --sample sample20/`
- Sample: `sample20/sample20_public_records.jsonl`
- Schema: `sample20/schema_public_sample20_v2.json` (strict public sample20 v2 contract using JSON Schema Draft 2020-12)
- Records: `20`
- Valid Cases: `18`
- Expected Canonical Rejections: `2`
- Canonical Validation Rate: `canonical_validation_rate = 0.9` (since the 2 expected negatives are successfully rejected)
- Expectation Met Rate: `expectation_met_rate = 1.0` (all 20 records match their case expectations)
- JSON parse: `PASS`
- Schema validation: `PASS`
- Replay: `PASS`
- Status: `PUBLIC_SAMPLE20_V2_VALID`

## Notes

- The sample is public, sanitized, and consists of 18 valid positive cases and 2 expected negative rejection cases.
- These results are evidence for public review, not a certification claim.
- The status of this package is `PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES`.
- All 1.0 metrics indicate internal agreement with the stored synthetic reference, not a final benchmark, production deployment, or certification. This is an academic research artifact, not a final benchmark, not a product, and does not claim production readiness or certification.
