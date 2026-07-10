from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# Obfuscated patterns to avoid matching this script during self-scan
PATTERNS = {
    "C:\\0 Work": "C:\\" + "0 Work",
    "PRODUCT_POLICY_FAIL": "PRODUCT_POLICY_" + "FAIL",
    "adapter_model.safetensors": "adapter_model." + "safetensors",
    ".safetensors": "." + "safetensors",
    ".docx": "." + "docx",
    ".zip": "." + "zip",
    "internal_family_dataset_5k": "internal_family_" + "dataset_5k",
}

# Regex for long hf_... and sk-... tokens
HF_TOKEN_RE = re.compile("hf_" + "[a-zA-Z0-9]{15,}")
SK_TOKEN_RE = re.compile("sk-" + "[a-zA-Z0-9]{15,}")


def main() -> int:
    # Get versioned files via git ls-files
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True
        )
        files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except Exception as exc:
        print(f"Error running git ls-files: {exc}", file=sys.stderr)
        return 1

    matches_found = 0
    scanned_count = 0

    print("SEMANTIC_XAIBIM_PUBLIC_FORBIDDEN_SCAN")

    for file_path_str in files:
        file_path = Path(file_path_str)
        if not file_path.exists() or not file_path.is_file():
            continue

        # Skip this script to avoid false positives on pattern definitions
        if file_path.name == "public_forbidden_scan.py":
            continue

        scanned_count += 1
        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
                for line_idx, line in enumerate(handle, start=1):
                    # Check exact string patterns
                    for name, value in PATTERNS.items():
                        if value in line:
                            # Avoid false positive matching of "construction" or similar substrings
                            # (not needed for C:\0 Work or specific filenames, but good practice)
                            print(f"MATCH: file={file_path_str} line={line_idx} pattern='{name}'", file=sys.stderr)
                            matches_found += 1

                    # Check long tokens
                    if HF_TOKEN_RE.search(line):
                        print(f"MATCH: file={file_path_str} line={line_idx} pattern='hf_token'", file=sys.stderr)
                        matches_found += 1
                    if SK_TOKEN_RE.search(line):
                        print(f"MATCH: file={file_path_str} line={line_idx} pattern='sk_token'", file=sys.stderr)
                        matches_found += 1
        except Exception as exc:
            print(f"WARNING: Could not read {file_path_str}: {exc}", file=sys.stderr)

    print(f"files_scanned={scanned_count}")
    print(f"matches={matches_found}")

    if matches_found > 0:
        print("status=FORBIDDEN_SCAN_FAIL")
        return 1
    else:
        print("status=FORBIDDEN_SCAN_OK")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
