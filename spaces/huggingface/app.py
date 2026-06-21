from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import gradio as gr


ROOT = Path(__file__).resolve().parent
SAMPLE_PATH = ROOT / "sample20_public_predictions.jsonl"


def load_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
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
        "# Semantic XAIBIM Public Replay",
        "",
        f"Records loaded: {len(RECORDS)}",
        "",
        "Status: RESEARCH_PASS",
        "",
        "This demo replays a reduced public sample. It does not run inference.",
        "",
        "## Top-level keys",
    ]

    for key in sorted(keys):
        lines.append(f"- {key}: {keys[key]}")

    return "\n".join(lines)


def show_record(choice: str) -> tuple[str, str, str, str, str]:
    if not choice:
        index = 0
    else:
        index = int(choice.split(":", 1)[0])

    record = RECORDS[index]

    prompt_payload = record.get("prompt_payload")
    canonical_output = record.get("canonical_output")
    expected_output = record.get("expected_output")
    parsed_output = record.get("parsed_output")
    validation = {
        "validation": record.get("validation"),
        "canonical_validation": record.get("canonical_validation"),
        "comparison": record.get("comparison"),
        "ok": record.get("ok"),
        "parse_error": record.get("parse_error"),
        "latency_ms": record.get("latency_ms"),
        "contract_mode": record.get("contract_mode"),
        "base_model": record.get("base_model"),
    }

    return (
        pretty(prompt_payload),
        pretty(canonical_output),
        pretty(expected_output),
        pretty(parsed_output),
        pretty(validation),
    )


with gr.Blocks(title="Semantic XAIBIM Replay") as demo:
    gr.Markdown(summarize())

    selector = gr.Dropdown(
        choices=record_choices(),
        value=record_choices()[0] if RECORDS else None,
        label="Public sample record",
    )

    with gr.Row():
        prompt_box = gr.Code(label="Prompt payload", language="json")
        validation_box = gr.Code(label="Validation", language="json")

    with gr.Row():
        canonical_box = gr.Code(label="Canonical output", language="json")
        expected_box = gr.Code(label="Expected output", language="json")

    parsed_box = gr.Code(label="Parsed output", language="json")

    selector.change(
        fn=show_record,
        inputs=selector,
        outputs=[
            prompt_box,
            canonical_box,
            expected_box,
            parsed_box,
            validation_box,
        ],
    )

    demo.load(
        fn=show_record,
        inputs=selector,
        outputs=[
            prompt_box,
            canonical_box,
            expected_box,
            parsed_box,
            validation_box,
        ],
    )


if __name__ == "__main__":
    demo.launch()
