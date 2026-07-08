from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_KEYS = {
    "ok",
    "canonical_output",
    "validation",
    "sample_id",
    "parsed_output",
    "expected_output",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                value = json.loads(text)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"JSON_PARSE_ERROR line={line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise SystemExit(f"JSON_OBJECT_REQUIRED line={line_number}")
            records.append(value)
    return records


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
        candidate = sample_path / "schema_minimal.json"
        if candidate.exists():
            return candidate
    else:
        candidate = sample_path.with_name("schema_minimal.json")
        if candidate.exists():
            return candidate
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Replay the public sample20 dataset.")
    parser.add_argument("--sample", required=True, help="Path to sample20/ or the JSONL file.")
    args = parser.parse_args(argv)

    sample_input = Path(args.sample)
    sample_file = resolve_sample_file(sample_input)
    schema_file = resolve_schema_file(sample_input if sample_input.is_dir() else sample_file)

    records = load_jsonl(sample_file)
    schema = None
    if schema_file is not None:
        with schema_file.open("r", encoding="utf-8") as handle:
            schema = json.load(handle)

    required_keys = set(REQUIRED_KEYS)
    if isinstance(schema, dict):
        required_keys.update(key for key in schema.get("required", []) if isinstance(key, str))

    schema_ok = True
    for record in records:
        if not required_keys.issubset(record.keys()):
            schema_ok = False
            break
        validation = record.get("validation")
        if not isinstance(validation, dict) or validation.get("ok") is not True:
            schema_ok = False
            break

    replay_ok = bool(records) and all(record.get("ok") is True for record in records)

    print("SEMANTIC_XAIBIM_PUBLIC_REPLAY")
    print(f"sample={sample_file}")
    print(f"records={len(records)}")
    print(f"json_parse={'PASS' if len(records) > 0 else 'FAIL'}")
    print(f"schema={'PASS' if schema_ok else 'FAIL'}")
    print(f"replay={'PASS' if replay_ok and schema_ok else 'FAIL'}")
    print(f"status={'REPLAY_OK' if replay_ok and schema_ok else 'REPLAY_FAIL'}")
    return 0 if replay_ok and schema_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
