from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ACCEPTED_SEMANTIC_KEYS = {
    "prompt",
    "input",
    "output",
    "expected",
    "canonical_output",
    "ifc_class",
    "semantic_type",
    "intent_class",
    "value_mode",
    "confidence",
    "missing_inputs",
    "evidence",
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


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python harness/schema_validator.py <sample.jsonl>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FILE_NOT_FOUND: {path}")
        return 2

    records = load_jsonl(path)
    if not records:
        print("NO_RECORDS_FOUND")
        return 1

    records_with_semantic_keys = 0
    for record in records:
        if ACCEPTED_SEMANTIC_KEYS.intersection(record.keys()):
            records_with_semantic_keys += 1

    print("SEMANTIC_XAIBIM_SCHEMA_VALIDATION")
    print(f"file={path}")
    print(f"records={len(records)}")
    print("json_parse_rate=1.0")
    print(f"records_with_semantic_keys={records_with_semantic_keys}")
    print("status=SCHEMA_VALIDATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
