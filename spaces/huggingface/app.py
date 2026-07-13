from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import gradio as gr
except ImportError:
    gr = None

ROOT = Path(__file__).resolve().parent
SAMPLE_PATH = ROOT / "sample20_public_predictions.jsonl"
SCHEMA_PATH = ROOT / "schema_public_sample20_v2.json"


def load_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not SAMPLE_PATH.exists():
        return records
    with SAMPLE_PATH.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                value = json.loads(text)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"Invalid JSONL at line {line_number}: {exc}") from exc
            if isinstance(value, dict):
                records.append(value)
    return records


RECORDS = load_records()


def pretty(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, indent=2, ensure_ascii=False)


def record_choices() -> list[str]:
    choices: list[str] = []
    for idx, record in enumerate(RECORDS):
        sample_id = record.get("sample_id", f"sample-{idx}")
        choices.append(f"{idx}: {sample_id}")
    return choices


def summarize() -> str:
    keys: dict[str, int] = {}
    for record in RECORDS:
        for key in record:
            keys[key] = keys.get(key, 0) + 1

    lines = [
        "# Semantic XAIBIM Public Replay (v2)",
        "",
        f"Records loaded: {len(RECORDS)}",
        "",
        "Status: PUBLIC_SAMPLE_VALID_WITH_EXPECTED_NEGATIVES",
        "",
        "This demo replays a reduced public sample. It does not run inference.",
        "The two canonical rejections are expected negative cases.",
        "This is not a BIM product and does not provide certification.",
        "",
        "## Top-level keys",
    ]

    for key in sorted(keys):
        lines.append(f"- {key}: {keys[key]}")

    return "\n".join(lines)


def show_record(choice: str) -> tuple[str, str, str, str, str, str, str, str]:
    if not choice:
        index = 0
    else:
        try:
            index = int(choice.split(":", 1)[0])
        except (ValueError, IndexError):
            index = 0

    if not RECORDS:
        return ("", "", "", "", "", "", "", "")

    record = RECORDS[index]

    return (
        pretty(record.get("sample_id")),
        pretty(record.get("case_expectation")),
        pretty(record.get("record_status")),
        pretty(record.get("input_summary")),
        pretty(record.get("model_output")),
        pretty(record.get("reference_output")),
        pretty(record.get("canonical_check")),
        pretty(record.get("agreement")),
    )


def self_test() -> None:
    print("Starting self-test for Hugging Face Replay Space...")
    assert SAMPLE_PATH.exists(), f"sample file missing at {SAMPLE_PATH}"
    assert len(RECORDS) == 20, f"expected 20 records, found {len(RECORDS)}"

    # Validate schema v2 using jsonschema if available
    try:
        import jsonschema
        if SCHEMA_PATH.exists():
            with SCHEMA_PATH.open("r", encoding="utf-8") as sf:
                schema = json.load(sf)
            validator = jsonschema.Draft202012Validator(schema)
            for idx, r in enumerate(RECORDS):
                validator.validate(r)
            print("Schema validation: PASS")
        else:
            print("Schema file missing for self-test, skipping jsonschema validation")
    except ImportError:
        print("jsonschema not installed, skipping strict schema validation in self-test")

    # Check case expectations & statuses
    valids = [r for r in RECORDS if r.get("case_expectation") == "VALID"]
    rejections = [r for r in RECORDS if r.get("case_expectation") == "EXPECTED_CANONICAL_REJECTION"]
    
    assert len(valids) == 18, f"expected 18 VALID cases, found {len(valids)}"
    assert len(rejections) == 2, f"expected 2 EXPECTED_CANONICAL_REJECTION cases, found {len(rejections)}"

    for r in valids:
        assert r.get("record_status") == "PASS", f"VALID record {r.get('sample_id')} should have record_status PASS"
        assert r.get("expectation_met") is True
    for r in rejections:
        assert r.get("record_status") == "EXPECTED_REJECTION_PASS", f"REJECTION record {r.get('sample_id')} should have record_status EXPECTED_REJECTION_PASS"
        assert r.get("expectation_met") is True

    # Check absence of legacy keys or forbidden keys
    forbidden_keys = {
        "prompt_payload", "instruction", "metadata", "safety_constraints", "raw_output",
        "json_fragment", "parsed_output", "expected_output", "canonical_output",
        "runtime_context_v1", "source_notes", "source_refs", "source_split",
        "split_profile", "dataset_id", "source_dataset_id", "aiMode", "agent", "cognitive",
        "created_at_utc", "latency_ms", "comparison", "commit_allowed",
        "confidence", "material", "ifc_candidates", "primary_anchor", "scenario_focus",
        "location_context", "recovery_hint", "base_model", "adapter_dir"
    }

    import re
    legacy_pattern = re.compile(r"h[a]rd_bl[o]ck|s[a]fe_bl[o]ck")

    for r in RECORDS:
        # Check recursively
        def check_forbidden(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    assert k not in forbidden_keys, f"Forbidden key '{k}' found"
                    assert not legacy_pattern.search(k.lower()), f"Legacy key '{k}' found"
                    if isinstance(v, str):
                        assert not legacy_pattern.search(v.lower()), f"Legacy token in value of '{k}' found: {v}"
                    check_forbidden(v)
            elif isinstance(obj, list):
                for item in obj:
                    check_forbidden(item)

        check_forbidden(r)

    print("SELF_TEST_OK")


def build_demo() -> gr.Blocks:
    if gr is None:
        raise RuntimeError("gradio is required to build the Blocks interface")
        
    with gr.Blocks(title="Semantic XAIBIM Replay") as demo:
        gr.Markdown(summarize())

        selector = gr.Dropdown(
            choices=record_choices(),
            value=record_choices()[0] if RECORDS else None,
            label="Public sample record",
        )

        with gr.Row():
            sample_id_box = gr.Textbox(label="Sample ID")
            case_exp_box = gr.Textbox(label="Case Expectation")
            status_box = gr.Textbox(label="Record Status")

        with gr.Row():
            input_summary_box = gr.Code(label="Input Summary", language="json")
            agreement_box = gr.Code(label="Agreement Metrics", language="json")

        with gr.Row():
            model_output_box = gr.Code(label="Model Output", language="json")
            ref_output_box = gr.Code(label="Reference Output", language="json")

        canonical_check_box = gr.Code(label="Canonical Check", language="json")

        selector.change(
            fn=show_record,
            inputs=selector,
            outputs=[
                sample_id_box,
                case_exp_box,
                status_box,
                input_summary_box,
                model_output_box,
                ref_output_box,
                canonical_check_box,
                agreement_box,
            ],
        )

        demo.load(
            fn=show_record,
            inputs=selector,
            outputs=[
                sample_id_box,
                case_exp_box,
                status_box,
                input_summary_box,
                model_output_box,
                ref_output_box,
                canonical_check_box,
                agreement_box,
            ],
        )

    return demo


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    if gr is None:
        raise RuntimeError("gradio is required to launch the interface")
    demo = build_demo()
    demo.launch()


if gr is not None:
    demo = build_demo()
else:
    demo = None

if __name__ == "__main__":
    main()
