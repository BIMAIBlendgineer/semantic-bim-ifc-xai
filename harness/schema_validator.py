from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from public_sample20_v2 import validate_records

# Add parent or harness directory to path just in case
sys.path.insert(0, str(Path(__file__).resolve().parent))


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python harness/schema_validator.py <sample.jsonl> [--schema <schema.json>]")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FILE_NOT_FOUND: {path}")
        return 2

    # Parse args for optional custom schema path
    schema_path = None
    if "--schema" in sys.argv:
        try:
            s_idx = sys.argv.index("--schema")
            if s_idx + 1 < len(sys.argv):
                schema_path = Path(sys.argv[s_idx + 1])
        except ValueError:
            pass

    if schema_path is None:
        # Fallback to schema_public_sample20_v2.json in same dir or sample20
        for candidate in (path.parent / "schema_public_sample20_v2.json", path.parent / "schema_public_sample20_v2.json"):
            if candidate.exists():
                schema_path = candidate
                break

    if schema_path is None or not schema_path.exists():
        # Look in sample20 directory as fallback
        schema_path = Path(__file__).resolve().parents[1] / "sample20" / "schema_public_sample20_v2.json"

    if not schema_path.exists():
        print(f"SCHEMA_FILE_NOT_FOUND: {schema_path}")
        return 2

    try:
        with schema_path.open("r", encoding="utf-8") as sf:
            schema = json.load(sf)
    except Exception as exc:
        print(f"ERROR: failed to read schema: {exc}")
        return 1

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
                    records.append(record)
                except json.JSONDecodeError as exc:
                    errors.append(f"Line {line_num}: JSON_PARSE_ERROR - {exc}")
                    continue

                if not isinstance(record, dict):
                    errors.append(f"Line {line_num}: JSON_OBJECT_REQUIRED - parsed record is not an object")
                    continue
    except Exception as exc:
        print(f"ERROR: failed to read input file: {exc}")
        return 1

    if total_lines == 0:
        print("SEMANTIC_XAIBIM_SCHEMA_VALIDATION")
        print(f"file={path}")
        print("records=0")
        print("json_parse_rate=0.0")
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
        print("status=SCHEMA_VALIDATION_FAIL")
        for err in errors:
            print(err)
        return 1

    ok, validation_errors, metrics = validate_records(records, schema)

    print("SEMANTIC_XAIBIM_SCHEMA_VALIDATION")
    print(f"file={path}")
    print(f"records={len(records)}")
    print(f"json_parse_rate={json_parse_rate:.1f}")
    print(f"records_with_required_keys={metrics.get('record_count', 0)}")
    print(f"records_with_evidence_trace={metrics.get('record_count', 0) if ok else 0}")

    if not ok or validation_errors:
        print("status=SCHEMA_VALIDATION_FAIL")
        for err in validation_errors:
            print(err)
        return 1
    else:
        print("status=SCHEMA_VALIDATION_OK")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
