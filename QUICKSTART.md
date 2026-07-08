# Quickstart

Minimal replay steps for the public sample.

1. Create a virtual environment:

```powershell
python -m venv .venv
```

2. Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the public replay:

```powershell
python harness/replay.py --sample sample20/
```

Expected output:

- `records=20`
- `json_parse=PASS`
- `schema=PASS`
- `replay=PASS`
- `status=REPLAY_OK`

