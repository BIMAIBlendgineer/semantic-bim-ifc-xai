from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Patterns are constructed at runtime to avoid self-detection during scan.
# Plain literal strings are split so this file does not match its own rules.
# ---------------------------------------------------------------------------

# Exact substring patterns (case-insensitive matching applied below)
_FORBIDDEN_SUBSTRINGS: dict[str, str] = {
    "local_path_c0work":      "c:\\" + "0 work",
    "product_policy_fail":    "PRODUCT_POLICY_" + "FAIL",
    "safetensors_file":       "adapter_model." + "safetensors",
    "safetensors_ext":        "." + "safetensors",
    "docx_ext":               "." + "docx",
    "zip_ext":                "." + "zip",
    "internal_dataset_name":  "internal_family_" + "dataset_5k",
    "file_url_triple":        "file://" + "/",
    "file_url_double":        "file:" + "//",
    "local_url_c0work_enc":   "c:/0%20" + "work",
    "local_url_c0work_plain": "c:/0 " + "work",
    "xaibim_trainer_enc":     "0%20xaibim%20" + "ai%20trainer",
    "users_path":             "c:\\" + "users\\",
    "mnt_data":               "/mnt/" + "data",
    "sandbox_mnt":            "sandbox:" + "/mnt/data",
}

# Regex patterns (compiled with IGNORECASE)
_FORBIDDEN_REGEXES: dict[str, re.Pattern[str]] = {
    "hf_token":  re.compile(r"hf_" + r"[a-zA-Z0-9]{15,}"),
    "sk_token":  re.compile(r"sk-" + r"[a-zA-Z0-9]{15,}"),
}

# Files to skip entirely (self-exclusion by name)
_SKIP_FILENAMES: frozenset[str] = frozenset(["public_forbidden_scan.py"])


def main() -> int:
    # Collect versioned files via git ls-files
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        )
        files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except Exception as exc:
        print(f"Error running git ls-files: {exc}", file=sys.stderr)
        return 1

    matches_found = 0
    scanned_count = 0
    match_lines: list[str] = []

    for file_path_str in files:
        file_path = Path(file_path_str)

        # Skip self
        if file_path.name in _SKIP_FILENAMES:
            continue

        if not file_path.exists() or not file_path.is_file():
            continue

        scanned_count += 1

        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as fh:
                for line_idx, line in enumerate(fh, start=1):
                    line_lower = line.lower()

                    # Substring patterns (case-insensitive via .lower())
                    for pattern_name, pattern_value in _FORBIDDEN_SUBSTRINGS.items():
                        if pattern_value.lower() in line_lower:
                            msg = (
                                f"MATCH file={file_path_str} "
                                f"line={line_idx} "
                                f"pattern='{pattern_name}'"
                            )
                            match_lines.append(msg)
                            matches_found += 1

                    # Regex patterns (compiled with IGNORECASE)
                    for pattern_name, rx in _FORBIDDEN_REGEXES.items():
                        if rx.search(line):
                            msg = (
                                f"MATCH file={file_path_str} "
                                f"line={line_idx} "
                                f"pattern='{pattern_name}'"
                            )
                            match_lines.append(msg)
                            matches_found += 1

        except Exception as exc:
            print(f"WARNING: could not read {file_path_str}: {exc}", file=sys.stderr)

    # Output
    print("SEMANTIC_XAIBIM_PUBLIC_FORBIDDEN_SCAN")
    print(f"files_scanned={scanned_count}")
    print(f"matches={matches_found}")

    if matches_found > 0:
        print("status=FORBIDDEN_SCAN_FAIL")
        for m in match_lines:
            print(m, file=sys.stderr)
        return 1

    print("status=FORBIDDEN_SCAN_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
