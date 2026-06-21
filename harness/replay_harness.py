from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


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
        print("Usage: python harness/replay_harness.py <sample.jsonl>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FILE_NOT_FOUND: {path}")
        return 2

    records = load_jsonl(path)
    print("SEMANTIC_XAIBIM_PUBLIC_REPLAY")
    print(f"file={path}")
    print(f"records={len(records)}")

    key_counts: dict[str, int] = {}
    for record in records:
        for key in record.keys():
            key_counts[key] = key_counts.get(key, 0) + 1

    print("top_level_keys:")
    for key in sorted(key_counts):
        print(f"- {key}: {key_counts[key]}")

    print("status=REPLAY_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
