from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python harness/schema_validator.py <sample.jsonl>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FILE_NOT_FOUND: {path}")
        return 2

    # Search for schema_minimal.json in the same directory
    schema_required = [
        "ok",
        "canonical_output",
        "validation",
        "sample_id",
        "parsed_output",
        "expected_output"
    ]
    schema_file = path.parent / "schema_minimal.json"
    if schema_file.exists():
        try:
            with schema_file.open("r", encoding="utf-8") as sf:
                schema_data = json.load(sf)
                if isinstance(schema_data, dict) and "required" in schema_data:
                    schema_required = list(schema_data["required"])
        except Exception as exc:
            print(f"WARNING: failed to read schema file: {exc}")

    # Read and validate JSONL lines
    errors: list[str] = []
    records: list[dict[str, Any]] = []
    total_lines = 0
    parsed_lines = 0

    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_num, line in enumerate(handle, start=1):
                text = line.strip()
                if not text:
                    continue
                total_lines += 1
                try:
                    record = json.loads(text)
                    parsed_lines += 1
                except json.JSONDecodeError as exc:
                    errors.append(f"Line {line_num}: JSON_PARSE_ERROR - {exc}")
                    continue

                if not isinstance(record, dict):
                    errors.append(f"Line {line_num}: JSON_OBJECT_REQUIRED - parsed record is not an object")
                    continue

                records.append((line_num, record))
    except Exception as exc:
        print(f"ERROR: failed to read input file: {exc}")
        return 1

    if total_lines == 0:
        print("SEMANTIC_XAIBIM_SCHEMA_VALIDATION")
        print(f"file={path}")
        print("records=0")
        print("json_parse_rate=0.0")
        print("records_with_required_keys=0")
        print("records_with_evidence_trace=0")
        print("status=SCHEMA_VALIDATION_FAIL")
        print("Error: JSONL is empty")
        return 1

    json_parse_rate = parsed_lines / total_lines

    # If any JSON parse errors, we report schema failure
    if errors:
        print("SEMANTIC_XAIBIM_SCHEMA_VALIDATION")
        print(f"file={path}")
        print(f"records={len(records)}")
        print(f"json_parse_rate={json_parse_rate:.2f}")
        print("records_with_required_keys=0")
        print("records_with_evidence_trace=0")
        print("status=SCHEMA_VALIDATION_FAIL")
        for err in errors:
            print(err)
        return 1

    records_with_required_keys = 0
    records_with_evidence_trace = 0

    for line_num, record in records:
        record_errors: list[str] = []
        # Check required keys
        missing_keys = [k for k in schema_required if k not in record]
        if missing_keys:
            record_errors.append(f"Missing required keys: {missing_keys}")
        else:
            records_with_required_keys += 1

            # Validate types and values only if keys exist
            if record.get("ok") is not True:
                record_errors.append(f"Key 'ok' must be boolean True, got {record.get('ok')}")

            canonical = record.get("canonical_output")
            if not isinstance(canonical, dict):
                record_errors.append(f"Key 'canonical_output' must be an object, got {type(canonical).__name__}")
            else:
                # Check evidence trace inside canonical_output
                if "evidence_trace" not in canonical:
                    record_errors.append("Missing 'evidence_trace' in 'canonical_output'")
                else:
                    ev_trace = canonical.get("evidence_trace")
                    # Check not empty
                    if ev_trace is None:
                        record_errors.append("Key 'evidence_trace' is null")
                    elif isinstance(ev_trace, (list, dict, str)) and len(ev_trace) == 0:
                        record_errors.append("Key 'evidence_trace' is empty")
                    elif not isinstance(ev_trace, (list, dict, str)):
                        record_errors.append(f"Key 'evidence_trace' must be container or string, got {type(ev_trace).__name__}")
                    else:
                        records_with_evidence_trace += 1

            validation = record.get("validation")
            if not isinstance(validation, dict):
                record_errors.append(f"Key 'validation' must be an object, got {type(validation).__name__}")
            elif validation.get("ok") is not True:
                record_errors.append(f"Key 'validation.ok' must be boolean True, got {validation.get('ok')}")

            sample_id = record.get("sample_id")
            if not isinstance(sample_id, str):
                record_errors.append(f"Key 'sample_id' must be a string, got {type(sample_id).__name__}")
            elif not sample_id.strip():
                record_errors.append("Key 'sample_id' cannot be empty or blank")

            if not isinstance(record.get("parsed_output"), dict):
                record_errors.append(f"Key 'parsed_output' must be an object, got {type(record.get('parsed_output')).__name__}")

            if not isinstance(record.get("expected_output"), dict):
                record_errors.append(f"Key 'expected_output' must be an object, got {type(record.get('expected_output')).__name__}")

        if record_errors:
            errors.append(f"Record index {line_num - 1} (Line {line_num}): " + " | ".join(record_errors))

    print("SEMANTIC_XAIBIM_SCHEMA_VALIDATION")
    print(f"file={path}")
    print(f"records={len(records)}")
    print(f"json_parse_rate={json_parse_rate:.1f}")
    print(f"records_with_required_keys={records_with_required_keys}")
    print(f"records_with_evidence_trace={records_with_evidence_trace}")

    if errors:
        print("status=SCHEMA_VALIDATION_FAIL")
        for err in errors:
            print(err)
        return 1
    else:
        print("status=SCHEMA_VALIDATION_OK")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
