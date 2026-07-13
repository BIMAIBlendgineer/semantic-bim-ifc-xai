from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from public_sample20_v2 import validate_records

# Add parent or harness directory to path just in case
sys.path.insert(0, str(Path(__file__).resolve().parent))


def resolve_sample_file(path: Path) -> Path:
    if path.is_dir():
        for candidate_name in ("sample20_public_records.jsonl", "sample20_public_predictions.jsonl"):
            candidate = path / candidate_name
            if candidate.exists():
                return candidate
        raise SystemExit(f"SAMPLE_FILE_NOT_FOUND: {path}")
    return path


def resolve_schema_file(sample_path: Path) -> Path | None:
    if sample_path.is_dir():
        candidate = sample_path / "schema_public_sample20_v2.json"
        if candidate.exists():
            return candidate
    else:
        candidate = sample_path.with_name("schema_public_sample20_v2.json")
        if candidate.exists():
            return candidate
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Replay the public sample20 v2 dataset.")
    parser.add_argument("--sample", required=True, help="Path to sample20/ or the JSONL file.")
    args = parser.parse_args(argv)

    sample_input = Path(args.sample)
    sample_file = resolve_sample_file(sample_input)
    schema_file = resolve_schema_file(sample_input if sample_input.is_dir() else sample_file)

    if not schema_file or not schema_file.exists():
        print(f"ERROR: schema file not found", file=sys.stderr)
        return 1

    try:
        with schema_file.open("r", encoding="utf-8") as sf:
            schema = json.load(sf)
    except Exception as exc:
        print(f"ERROR reading schema: {exc}", file=sys.stderr)
        return 1

    # Load records using the common loader
    # load_records in public_sample20_v2 expects path: Path. But wait, in public_sample20_v2 we wrote load_records() without params that uses SAMPLE_PATH.
    # Let's write a local helper or adjust it.
    records: list[dict[str, Any]] = []
    with sample_file.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                records.append(json.loads(text))
            except json.JSONDecodeError as exc:
                print(f"JSON_PARSE_ERROR line={line_number}: {exc}", file=sys.stderr)
                return 1

    ok, errors, metrics = validate_records(records, schema)

    # Replay outputs expected:
    # SEMANTIC_XAIBIM_PUBLIC_REPLAY_V2
    # records=20
    # valid_cases=18
    # expected_rejections=2
    # expectation_met_rate=1.0
    # schema=PASS
    # integrity=PASS
    # status=PUBLIC_SAMPLE20_V2_VALID
    
    print("SEMANTIC_XAIBIM_PUBLIC_REPLAY_V2")
    print(f"records={len(records)}")
    print(f"valid_cases={metrics.get('valid_case_count', 0)}")
    print(f"expected_rejections={metrics.get('expected_canonical_rejection_count', 0)}")
    print(f"expectation_met_rate={metrics.get('expectation_met_rate', 0.0):.1f}")
    print(f"schema={'PASS' if ok else 'FAIL'}")
    print(f"integrity={'PASS' if ok else 'FAIL'}")
    print(f"status={'PUBLIC_SAMPLE20_V2_VALID' if ok else 'PUBLIC_SAMPLE20_V2_INVALID'}")

    if not ok:
        print("\nValidation errors found:", file=sys.stderr)
        for err in errors[:20]:
            print(f"  {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
