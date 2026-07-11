# Quickstart

Minimal local validation steps for the public sample and public validation layer.

## 1. Create a virtual environment

```powershell
python -m venv .venv
```

## 2. Activate it on Windows

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install root dependencies

```powershell
pip install -r requirements.txt
```

The root public replay and validation harnesses use Python standard library only. The optional Hugging Face harness has its own dependency file.

## 4. Run the public replay

```powershell
python harness/replay.py --sample sample20/
```

Expected output includes:

* `records=20`
* `json_parse=PASS`
* `schema=PASS`
* `replay=PASS`
* `status=REPLAY_OK`

## 5. Run the public schema validator

```powershell
python harness/schema_validator.py sample20/sample20_public_records.jsonl
```

Expected output includes:

* `records=20`
* `json_parse_rate=1.0`
* `records_with_required_keys=20`
* `records_with_evidence_trace=20`
* `status=SCHEMA_VALIDATION_OK`

## 6. Run the public forbidden-pattern scan

```powershell
python scripts/public_forbidden_scan.py
```

Expected output includes:

* `matches=0`
* `status=FORBIDDEN_SCAN_OK`

## 7. Optional: run the Hugging Face harness self-test

Install optional demo dependencies:

```powershell
pip install -r spaces/huggingface_harness/requirements.txt
```

Run:

```powershell
python spaces/huggingface_harness/app.py --self-test
```

Expected output:

* `SELF_TEST_OK`

If `pandas` or `gradio` are not installed locally, the script may print warnings. These warnings do not block the public self-test if the command ends with `SELF_TEST_OK`.

## Scope

These commands validate the public sample and public reproducibility layer. They do not run private models, private datasets, adapters, checkpoints, production BIM services or certification workflows.
