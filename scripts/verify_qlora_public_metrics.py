"""
verify_qlora_public_metrics.py
==============================
Deterministic verifier for the public QLoRA preliminary results JSON.

Uses Python standard library only — no external dependencies.

Exit 0  → all checks pass, prints QLORA_PUBLIC_METRICS_VALID
Exit 1  → at least one check failed
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Locate the JSON relative to this script
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
JSON_PATH = REPO_ROOT / "benchmark" / "qlora" / "xaibim_qwen25_7b_qlora_preliminary_public_results.json"

EXPECTED_KAGGLE_URL = "https://www.kaggle.com/code/xaibim/semantic-bim-ifc-xai"

# Tolerances for float comparisons
ABS_TOL = 1e-9
REL_TOL = 1e-9


def close(a: float, b: float, label: str) -> bool:
    ok = math.isclose(a, b, rel_tol=REL_TOL, abs_tol=ABS_TOL)
    if not ok:
        print(f"FAIL [{label}]: expected {b!r}, got {a!r}")
    return ok


def equal(a, b, label: str) -> bool:
    ok = a == b
    if not ok:
        print(f"FAIL [{label}]: expected {b!r}, got {a!r}")
    return ok


def main() -> int:
    # -----------------------------------------------------------------------
    # Load JSON
    # -----------------------------------------------------------------------
    if not JSON_PATH.exists():
        print(f"FAIL: JSON not found at {JSON_PATH}")
        return 1

    with open(JSON_PATH, encoding="utf-8") as fh:
        data = json.load(fh)

    failures: list[str] = []

    def check(label: str, result: bool) -> None:
        if not result:
            failures.append(label)

    # -----------------------------------------------------------------------
    # 1. Kaggle URL
    # -----------------------------------------------------------------------
    check(
        "kaggle_notebook_url",
        equal(data.get("kaggle_notebook_url"), EXPECTED_KAGGLE_URL, "kaggle_notebook_url"),
    )

    # -----------------------------------------------------------------------
    # 2. adapter_publicly_released must be false
    # -----------------------------------------------------------------------
    check(
        "adapter_publicly_released",
        equal(
            data.get("model_and_training", {}).get("adapter_publicly_released"),
            False,
            "adapter_publicly_released",
        ),
    )

    # -----------------------------------------------------------------------
    # 3. record_count in corrected results = 100
    # -----------------------------------------------------------------------
    for layer in ("baseline", "adapter"):
        rc = data.get("corrected_held_out_results", {}).get(layer, {}).get("record_count")
        check(
            f"corrected_held_out_results.{layer}.record_count",
            equal(rc, 100, f"record_count ({layer})"),
        )

    # -----------------------------------------------------------------------
    # 4. Derived calculations
    # -----------------------------------------------------------------------
    compute = data.get("compute", {})
    derived = data.get("derived_calculations", {})
    model_training = data.get("model_and_training", {})
    data_section = data.get("data", {})

    training_s: float = compute.get("training_runtime_seconds", 0)
    e2e_s: float = compute.get("measured_end_to_end_runtime_seconds", 0)
    effective_gpus: int = compute.get("effective_gpu_count", 1)
    allocated_gpus: int = compute.get("allocated_gpu_count", 2)
    adapter_bytes: int = model_training.get("adapter_size_bytes", 0)
    train_records: int = data_section.get("train_records", 0)
    effective_batch: int = model_training.get("effective_batch_size", 0)
    epochs: int = model_training.get("epochs", 0)

    # 4a. Training runtime hours
    expected_train_h = training_s / 3600.0
    check(
        "derived.training_runtime_hours",
        close(derived.get("training_runtime_hours", float("nan")), expected_train_h, "training_runtime_hours"),
    )

    # 4b. End-to-end runtime hours
    expected_e2e_h = e2e_s / 3600.0
    check(
        "derived.end_to_end_runtime_hours",
        close(derived.get("end_to_end_runtime_hours", float("nan")), expected_e2e_h, "end_to_end_runtime_hours"),
    )

    # 4c. Non-training overhead seconds
    expected_overhead_s = e2e_s - training_s
    check(
        "derived.non_training_overhead_seconds",
        close(derived.get("non_training_overhead_seconds", float("nan")), expected_overhead_s, "non_training_overhead_seconds"),
    )

    # 4d. Non-training overhead hours
    expected_overhead_h = expected_overhead_s / 3600.0
    check(
        "derived.non_training_overhead_hours",
        close(derived.get("non_training_overhead_hours", float("nan")), expected_overhead_h, "non_training_overhead_hours"),
    )

    # 4e. Effective GPU-hours
    expected_eff_gpu_h = expected_e2e_h * effective_gpus
    check(
        "derived.effective_gpu_hours_recomputed",
        close(derived.get("effective_gpu_hours_recomputed", float("nan")), expected_eff_gpu_h, "effective_gpu_hours_recomputed"),
    )

    # 4f. Allocated GPU-hours
    expected_alloc_gpu_h = expected_e2e_h * allocated_gpus
    check(
        "derived.allocated_gpu_hours_recomputed",
        close(derived.get("allocated_gpu_hours_recomputed", float("nan")), expected_alloc_gpu_h, "allocated_gpu_hours_recomputed"),
    )

    # 4g. Expected optimizer steps
    if effective_batch > 0 and epochs > 0:
        expected_steps = (train_records // effective_batch) * epochs
        check(
            "derived.expected_optimizer_steps",
            equal(derived.get("expected_optimizer_steps"), expected_steps, "expected_optimizer_steps"),
        )

    # 4h. Adapter size MiB
    expected_mib = adapter_bytes / 1_048_576
    check(
        "derived.adapter_size_mib",
        close(derived.get("adapter_size_mib", float("nan")), expected_mib, "adapter_size_mib"),
    )

    # 4i. Training runtime share
    if e2e_s > 0:
        expected_train_share = training_s / e2e_s * 100.0
        check(
            "derived.training_runtime_share_percent",
            close(derived.get("training_runtime_share_percent", float("nan")), expected_train_share, "training_runtime_share_percent"),
        )

        # 4j. Non-training runtime share
        expected_nontrain_share = expected_overhead_s / e2e_s * 100.0
        check(
            "derived.non_training_runtime_share_percent",
            close(derived.get("non_training_runtime_share_percent", float("nan")), expected_nontrain_share, "non_training_runtime_share_percent"),
        )

        # Both shares must sum to 100
        share_sum = (
            derived.get("training_runtime_share_percent", 0.0) +
            derived.get("non_training_runtime_share_percent", 0.0)
        )
        check(
            "derived.shares_sum_to_100",
            close(share_sum, 100.0, "shares_sum_to_100"),
        )

    # -----------------------------------------------------------------------
    # 5. Test distribution sums
    # -----------------------------------------------------------------------
    test_dist = data.get("corrected_held_out_results", {}).get("test_distribution", {})

    for dim_name, expected_total in [
        ("intent_class", 100),
        ("semantic_type", 100),
        ("ifc_class", 100),
        ("value_mode", 100),
    ]:
        dist = test_dist.get(dim_name, {})
        total = sum(dist.values())
        label = f"test_distribution.{dim_name}.sum"
        ok = total == expected_total
        if not ok:
            print(f"FAIL [{label}]: expected sum {expected_total}, got {total}")
        check(label, ok)

    # -----------------------------------------------------------------------
    # 6. No forbidden local paths in any string value (recursive)
    # -----------------------------------------------------------------------
    def find_local_paths(obj, path: str = "") -> list[str]:
        hits = []
        if isinstance(obj, str):
            lowered = obj.lower()
            # detect Windows drive-letter paths or Kaggle working/input dirs
            drive_path = obj[:3].lower() if len(obj) >= 3 else ""
            has_drive = drive_path[1:3] == ":\\" or drive_path[1:3] == ":/"
            has_kaggle_ws = ("kaggle" in lowered and
                             ("working" in lowered or "input" in lowered) and
                             obj.startswith("/"))
            if has_drive or has_kaggle_ws:
                hits.append(f"{path}: {obj[:80]}")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                hits.extend(find_local_paths(v, f"{path}.{k}"))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                hits.extend(find_local_paths(v, f"{path}[{i}]"))
        return hits

    local_path_hits = find_local_paths(data)
    if local_path_hits:
        for h in local_path_hits:
            print(f"FAIL [local_path_found]: {h}")
        failures.append("local_paths")

    # -----------------------------------------------------------------------
    # 7. Verify /notebook suffix NOT present in kaggle URL
    # -----------------------------------------------------------------------
    url = data.get("kaggle_notebook_url", "")
    if "/notebook" in url:
        print(f"FAIL [kaggle_url_suffix]: URL must not end with /notebook, got {url!r}")
        failures.append("kaggle_url_suffix")

    # -----------------------------------------------------------------------
    # Final verdict
    # -----------------------------------------------------------------------
    if failures:
        print(f"\nFAILED checks: {failures}")
        return 1

    print("QLORA_PUBLIC_METRICS_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
