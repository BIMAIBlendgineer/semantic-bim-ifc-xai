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
    replay_ok = bool(records)
    errors: list[str] = []

    for idx, record in enumerate(records):
        record_errors = []
        # Check required keys
        missing_keys = required_keys - record.keys()
        if missing_keys:
            record_errors.append(f"Missing required keys: {list(missing_keys)}")
        else:
            # Validate types and values
            if record.get("ok") is not True:
                record_errors.append("ok is not True")

            canonical = record.get("canonical_output")
            if not isinstance(canonical, dict):
                record_errors.append("canonical_output is not a dict")
            else:
                if "evidence_trace" not in canonical:
                    record_errors.append("Missing evidence_trace in canonical_output")
                else:
                    ev_trace = canonical.get("evidence_trace")
                    if ev_trace is None:
                        record_errors.append("evidence_trace is null")
                    elif isinstance(ev_trace, (list, dict, str)) and len(ev_trace) == 0:
                        record_errors.append("evidence_trace is empty")
                    elif not isinstance(ev_trace, (list, dict, str)):
                        record_errors.append("evidence_trace is not a valid container/string")

            validation = record.get("validation")
            if not isinstance(validation, dict):
                record_errors.append("validation is not a dict")
            elif validation.get("ok") is not True:
                record_errors.append("validation.ok is not True")

            sample_id = record.get("sample_id")
            if not isinstance(sample_id, str):
                record_errors.append("sample_id is not a string")
            elif not sample_id.strip():
                record_errors.append("sample_id is empty")

            if not isinstance(record.get("parsed_output"), dict):
                record_errors.append("parsed_output is not a dict")

            if not isinstance(record.get("expected_output"), dict):
                record_errors.append("expected_output is not a dict")

        if record_errors:
            schema_ok = False
            errors.append(f"Record {idx}: " + " | ".join(record_errors))

        if record.get("ok") is not True:
            replay_ok = False

    replay_passed = replay_ok and schema_ok

    print("SEMANTIC_XAIBIM_PUBLIC_REPLAY")
    print(f"sample={sample_file}")
    print(f"records={len(records)}")
    print(f"json_parse={'PASS' if len(records) > 0 else 'FAIL'}")
    print(f"schema={'PASS' if schema_ok else 'FAIL'}")
    print(f"replay={'PASS' if replay_passed else 'FAIL'}")
    print(f"status={'REPLAY_OK' if replay_passed else 'REPLAY_FAIL'}")

    if not replay_passed and errors:
        print("\nReplay validation errors:", file=sys.stderr)
        for err in errors[:10]:
            print(f"  {err}", file=sys.stderr)
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors", file=sys.stderr)

    return 0 if replay_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
