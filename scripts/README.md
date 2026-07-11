# scripts

## Purpose

This folder contains small public utility scripts used by the reproducibility checks.

## Contents

- `public_forbidden_scan.py`: scans tracked repository files for forbidden local paths, credentials, private artifacts, and public-boundary violations.

## What this folder does not contain

- private automation;
- internal dataset generation scripts;
- model training scripts;
- credentials;
- local workspace paths.

## Related files

- `.github/workflows/public-sample20.yml`
- `PUBLIC_EVIDENCE.md`
- `sample20/VALIDATION_SUMMARY.md`
