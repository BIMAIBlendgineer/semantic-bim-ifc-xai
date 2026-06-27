from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    import pandas as pd
except ModuleNotFoundError:  # pragma: no cover - local self-test fallback
    pd = None

try:
    import gradio as gr
except ModuleNotFoundError:  # pragma: no cover - local self-test fallback
    gr = None


ROOT = Path(__file__).resolve().parent
SAMPLE_PATH = ROOT / "sample20_public_predictions.jsonl"
REQUIRED_CONTRACT_KEYS = ("status", "canonical_output", "validation", "metadata")
PUBLIC_WARNING = (
    "Public constrained demo. It does not run private models or private datasets."
)


def load_records() -> list[dict[str, Any]]:
    if not SAMPLE_PATH.exists():
        raise RuntimeError(f"Missing sample file: {SAMPLE_PATH}")

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
            if not isinstance(value, dict):
                raise RuntimeError(f"Expected object at line {line_number}")
            records.append(value)

    return records


RECORDS = load_records()


def to_json(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True)


def ui_update(**kwargs: Any) -> Any:
    if gr is None:
        return kwargs
    return gr.update(**kwargs)


def safe_get(record: dict[str, Any], *path: str) -> Any:
    current: Any = record
    for part in path:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def get_ifc_classes(record: dict[str, Any]) -> list[str]:
    classes: list[str] = []

    for path in (
        ("canonical_output", "ifc_class"),
        ("parsed_output", "ifc_class"),
        ("expected_output", "ifc_class"),
    ):
        value = safe_get(record, *path)
        if isinstance(value, str) and value:
            classes.append(value)

    allowed = record.get("allowed_ifc_classes")
    if isinstance(allowed, list):
        for value in allowed:
            if isinstance(value, str) and value:
                classes.append(value)

    deduped: list[str] = []
    for value in classes:
        if value not in deduped:
            deduped.append(value)
    return deduped


def normalize_terms(text: str) -> list[str]:
    return [part for part in re.findall(r"[A-Za-z0-9_]+", text.lower()) if part]


def searchable_text(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True).lower()


def score_record(record: dict[str, Any], terms: list[str]) -> int:
    if not terms:
        return 0

    text = searchable_text(record)
    score = 0
    if record.get("sample_id"):
        sample_id = str(record["sample_id"]).lower()
    else:
        sample_id = ""
    ifc_classes = [value.lower() for value in get_ifc_classes(record)]

    for term in terms:
        if term in text:
            score += max(1, text.count(term))
        if sample_id and term in sample_id:
            score += 2
        if any(term == value or term in value for value in ifc_classes):
            score += 2

    return score


def record_label(item: dict[str, Any]) -> str:
    index = item["index"]
    sample_id = item["record"].get("sample_id", f"sample-{index}")
    ifc_class = item.get("ifc_class") or "n/a"
    score = item.get("score", 0)
    return f"{index}: {sample_id} | {ifc_class} | score={score}"


def build_table_items(query: str, ifc_filter: str) -> list[dict[str, Any]]:
    terms = normalize_terms(query)
    filtered: list[dict[str, Any]] = []

    for index, record in enumerate(RECORDS):
        if ifc_filter != "All":
            if ifc_filter not in get_ifc_classes(record):
                continue

        score = score_record(record, terms)
        if terms and score == 0:
            continue

        parsed_output = safe_get(record, "parsed_output") or {}
        canonical_output = safe_get(record, "canonical_output") or {}
        metadata = safe_get(record, "metadata") or {}

        filtered.append(
            {
                "index": index,
                "record": record,
                "score": score,
                "sample_id": record.get("sample_id", f"sample-{index}"),
                "ifc_class": safe_get(record, "canonical_output", "ifc_class")
                or safe_get(record, "parsed_output", "ifc_class")
                or safe_get(record, "expected_output", "ifc_class")
                or (get_ifc_classes(record)[0] if get_ifc_classes(record) else ""),
                "semantic_type": safe_get(record, "parsed_output", "semantic_type")
                or safe_get(record, "canonical_output", "semantic_type")
                or "",
                "intent_class": safe_get(record, "parsed_output", "intent_class")
                or safe_get(record, "canonical_output", "intent_class")
                or "",
                "value_mode": safe_get(record, "parsed_output", "value_mode")
                or safe_get(record, "canonical_output", "value_mode")
                or "",
                "split": metadata.get("source_split") or record.get("contract_mode") or "",
                "risk_level": metadata.get("risk_level") or "",
                "latency_ms": record.get("latency_ms", ""),
                "preview": str(
                    safe_get(record, "prompt_payload", "instruction") or ""
                )[:120],
                "validated": bool(
                    safe_get(record, "validation", "ok")
                    or safe_get(record, "canonical_validation", "ok")
                ),
                "status": "PASS" if bool(record.get("ok")) else "FAIL",
                "canonical_state": "PASS"
                if bool(safe_get(record, "canonical_validation", "ok"))
                else "FAIL",
                "base_model": record.get("base_model", ""),
                "created_at_utc": record.get("created_at_utc", ""),
            }
        )

    if terms:
        filtered.sort(key=lambda item: (-item["score"], item["index"]))
    else:
        filtered.sort(key=lambda item: item["index"])

    return filtered


def table_frame(items: list[dict[str, Any]]) -> pd.DataFrame:
    columns = [
        "rank",
        "index",
        "sample_id",
        "ifc_class",
        "semantic_type",
        "intent_class",
        "value_mode",
        "score",
        "split",
        "risk_level",
        "status",
        "canonical_state",
        "preview",
    ]
    rows = []
    for rank, item in enumerate(items, start=1):
        rows.append(
            {
                "rank": rank,
                "index": item["index"],
                "sample_id": item["sample_id"],
                "ifc_class": item["ifc_class"],
                "semantic_type": item["semantic_type"],
                "intent_class": item["intent_class"],
                "value_mode": item["value_mode"],
                "score": item["score"],
                "split": item["split"],
                "risk_level": item["risk_level"],
                "status": item["status"],
                "canonical_state": item["canonical_state"],
                "preview": item["preview"],
            }
        )
    if pd is None:
        return rows
    return pd.DataFrame(rows, columns=columns)


def initial_search_state() -> list[dict[str, Any]]:
    return build_table_items("", "All")


def search_public_cases(query: str, ifc_filter: str) -> tuple[Any, Any, list[dict[str, Any]], str, str]:
    items = build_table_items(query or "", ifc_filter or "All")
    frame = table_frame(items)
    labels = [record_label(item) for item in items]
    first = labels[0] if labels else None
    summary = f"Loaded records: {len(RECORDS)} | Search results: {len(items)}"
    selected_json = to_json(items[0]["record"]) if items else "{}"
    return (
        frame,
        ui_update(choices=labels, value=first),
        items,
        summary,
        selected_json,
    )


def show_selected_record(items: list[dict[str, Any]], choice: str | None) -> str:
    if not items:
        return "{}"

    if not choice:
        return to_json(items[0]["record"])

    prefix = choice.split(":", 1)[0].strip()
    try:
        index = int(prefix)
    except ValueError:
        return to_json(items[0]["record"])

    for item in items:
        if item["index"] == index:
            return to_json(item["record"])

    return to_json(items[0]["record"])


def find_closest_case(text: str) -> tuple[str, str, str]:
    query = (text or "").strip()
    if not query:
        item = build_table_items("", "All")[0]
        summary = f"Closest public case: {item['sample_id']} (score={item['score']})"
        return summary, to_json(item["record"]), PUBLIC_WARNING

    terms = normalize_terms(query)
    ranked = []
    for index, record in enumerate(RECORDS):
        score = score_record(record, terms)
        ranked.append(
            (
                score,
                index,
                {
                    "index": index,
                    "record": record,
                    "score": score,
                    "sample_id": record.get("sample_id", f"sample-{index}"),
                },
            )
        )

    ranked.sort(key=lambda item: (-item[0], item[1]))
    chosen = ranked[0][2]
    summary = (
        f"Closest public case: {chosen['sample_id']} "
        f"(score={chosen['score']}, index={chosen['index']})"
    )
    return summary, to_json(chosen["record"]), PUBLIC_WARNING


def validate_json_input(text: str) -> tuple[str, str, str]:
    raw = (text or "").strip()
    if not raw:
        return "FAIL", "Input is empty.", "{}"

    errors: list[str] = []
    parsed: Any
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        return "FAIL", f"JSON parse error: {exc}", "{}"

    if not isinstance(parsed, dict):
        errors.append("Root value must be a JSON object.")
    else:
        for key in REQUIRED_CONTRACT_KEYS:
            if key not in parsed:
                errors.append(f"Missing required key: {key}")

    verdict = "PASS" if not errors else "FAIL"
    error_text = "OK" if not errors else "\n".join(errors)
    normalized = to_json(parsed) if isinstance(parsed, dict) else to_json(parsed)
    return verdict, error_text, normalized


def run_public_harness() -> tuple[str, str]:
    errors: list[str] = []
    if len(RECORDS) != 20:
        errors.append(f"records = {len(RECORDS)}")

    for index, record in enumerate(RECORDS):
        if not isinstance(record, dict):
            errors.append(f"record {index}: not an object")
            continue
        for key in ("canonical_output", "validation", "canonical_validation", "parsed_output", "expected_output", "sample_id"):
            if key not in record:
                errors.append(f"record {index}: missing {key}")
        if not isinstance(record.get("validation"), dict):
            errors.append(f"record {index}: validation not an object")
        if not isinstance(record.get("canonical_validation"), dict):
            errors.append(f"record {index}: canonical_validation not an object")

    if errors:
        return "FAIL", "\n".join(errors)

    return "SCHEMA_VALIDATION_OK\nREPLAY_OK\nrecords = 20", "No issues detected."


def self_test() -> None:
    assert SAMPLE_PATH.exists(), "sample file missing"
    assert len(RECORDS) == 20, f"expected 20 records, found {len(RECORDS)}"

    items = build_table_items("column", "All")
    assert items, "search should return at least one item"

    verdict, errors, normalized = validate_json_input(
        json.dumps(
            {
                "status": "PASS",
                "canonical_output": {"ok": True},
                "validation": {"ok": True},
                "metadata": {"source_split": "test"},
            }
        )
    )
    assert verdict == "PASS", errors
    assert "canonical_output" in normalized

    verdict, errors, _ = validate_json_input("{")
    assert verdict == "FAIL"
    assert "JSON parse error" in errors

    harness_result, harness_detail = run_public_harness()
    assert "SCHEMA_VALIDATION_OK" in harness_result, harness_detail
    assert "REPLAY_OK" in harness_result, harness_detail
    assert "records = 20" in harness_result, harness_detail

    print("SELF_TEST_OK")


def build_demo() -> gr.Blocks:
    if gr is None:
        raise RuntimeError("gradio is required to launch the public harness demo")

    ifc_options = ["All"]
    for record in RECORDS:
        for value in get_ifc_classes(record):
            if value not in ifc_options:
                ifc_options.append(value)
    ifc_options = ["All"] + sorted(value for value in ifc_options if value != "All")

    with gr.Blocks(title="Semantic XAIBIM Public Harness") as demo:
        gr.Markdown(
            "# Semantic XAIBIM Public Harness\n\n"
            f"Loaded public records: **{len(RECORDS)}**\n\n"
            f"{PUBLIC_WARNING}"
        )

        search_state = gr.State(initial_search_state())

        with gr.Tab("Search public cases"):
            query = gr.Textbox(
                label="Search text",
                placeholder="Search public cases by semantic words, sample id, or evidence labels",
            )
            ifc_filter = gr.Dropdown(
                choices=ifc_options,
                value="All",
                label="IFC class filter",
            )
            search_button = gr.Button("Search")
            search_summary = gr.Textbox(label="Search summary", interactive=False)
            result_table = gr.Dataframe(
                label="Search results",
                interactive=False,
                wrap=True,
            )
            result_choice = gr.Dropdown(label="Selected result", choices=[], value=None)
            selected_json = gr.Code(label="Selected record JSON", language="json")

            search_button.click(
                fn=search_public_cases,
                inputs=[query, ifc_filter],
                outputs=[result_table, result_choice, search_state, search_summary, selected_json],
            )
            result_choice.change(
                fn=show_selected_record,
                inputs=[search_state, result_choice],
                outputs=selected_json,
            )
            query.submit(
                fn=search_public_cases,
                inputs=[query, ifc_filter],
                outputs=[result_table, result_choice, search_state, search_summary, selected_json],
            )
            ifc_filter.change(
                fn=search_public_cases,
                inputs=[query, ifc_filter],
                outputs=[result_table, result_choice, search_state, search_summary, selected_json],
            )

        with gr.Tab("Try semantic input"):
            semantic_input = gr.Textbox(
                label="Semantic input",
                lines=6,
                placeholder="Write a public semantic request and match it against the reduced sample.",
            )
            semantic_button = gr.Button("Match public case")
            semantic_summary = gr.Textbox(label="Match summary", interactive=False)
            semantic_json = gr.Code(label="Matched record JSON", language="json")
            semantic_warning = gr.Textbox(label="Public demo warning", interactive=False)

            semantic_button.click(
                fn=find_closest_case,
                inputs=semantic_input,
                outputs=[semantic_summary, semantic_json, semantic_warning],
            )
            semantic_input.submit(
                fn=find_closest_case,
                inputs=semantic_input,
                outputs=[semantic_summary, semantic_json, semantic_warning],
            )

        with gr.Tab("Validate JSON"):
            json_input = gr.Textbox(
                label="JSON input",
                lines=10,
                placeholder="Paste a JSON object with status, canonical_output, validation and metadata.",
            )
            json_button = gr.Button("Validate")
            json_verdict = gr.Textbox(label="Verdict", interactive=False)
            json_errors = gr.Textbox(label="Errors", interactive=False)
            json_normalized = gr.Code(label="Normalized JSON", language="json")

            json_button.click(
                fn=validate_json_input,
                inputs=json_input,
                outputs=[json_verdict, json_errors, json_normalized],
            )
            json_input.submit(
                fn=validate_json_input,
                inputs=json_input,
                outputs=[json_verdict, json_errors, json_normalized],
            )

        with gr.Tab("Run public harness"):
            harness_button = gr.Button("Run validation")
            harness_result = gr.Textbox(label="Harness result", interactive=False)
            harness_notes = gr.Textbox(label="Notes", interactive=False)

            harness_button.click(
                fn=run_public_harness,
                inputs=[],
                outputs=[harness_result, harness_notes],
            )

    return demo


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    demo = build_demo()
    demo.launch()


if __name__ == "__main__":
    main()
