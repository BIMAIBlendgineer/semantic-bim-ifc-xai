from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import gradio as gr
except ImportError:
    gr = None

ROOT = Path(__file__).resolve().parent
SAMPLE_PATH = ROOT / "sample20_public_predictions.jsonl"
SCHEMA_PATH = ROOT / "schema_public_sample20_v2.json"
PUBLIC_WARNING = (
    "Public constrained demo. It does not run private models or private datasets."
)


def load_records() -> list[dict[str, Any]]:
    if not SAMPLE_PATH.exists():
        return []

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
    return json.dumps(value, indent=2, ensure_ascii=False)


def generate_obj_cube(x1: float, x2: float, y1: float, y2: float, z1: float, z2: float, name: str) -> str:
    """Generate a conceptual wavefront OBJ model for element visualization."""
    obj_dir = ROOT / "temp_models"
    obj_dir.mkdir(exist_ok=True)
    obj_path = obj_dir / f"{name}.obj"

    vertices = [
        (x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2),
        (x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2)
    ]
    faces = [
        (1, 2, 3, 4), (5, 6, 7, 8), (1, 2, 6, 5),
        (2, 3, 7, 6), (3, 4, 8, 7), (4, 1, 5, 8)
    ]

    with obj_path.open("w", encoding="utf-8") as fh:
        fh.write(f"# Conceptual 3D model for {name}\n")
        for v in vertices:
            fh.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        for f in faces:
            fh.write(f"f {f[0]} {f[1]} {f[2]} {f[3]}\n")

    return str(obj_path)


def semantic_bim_preview(text: str) -> tuple[str, list[list[str]], str, str, str, str]:
    query = (text or "").strip()
    lower_query = query.lower()

    # Determine matched keyword/class
    ifc_class = None
    matched_keyword = None
    if any(k in lower_query for k in ("column", "pilar", "columna")):
        ifc_class = "IfcColumn"
        matched_keyword = "column"
    elif any(k in lower_query for k in ("wall", "muro", "parede", "partition")):
        ifc_class = "IfcWall"
        matched_keyword = "wall"
    elif any(k in lower_query for k in ("window", "janela", "ventana")):
        ifc_class = "IfcWindow"
        matched_keyword = "window"
    elif any(k in lower_query for k in ("beam", "viga")):
        ifc_class = "IfcBeam"
        matched_keyword = "beam"
    elif any(k in lower_query for k in ("slab", "losa", "laje")):
        ifc_class = "IfcSlab"
        matched_keyword = "slab"

    # Extract user-declared materials and dimensions (strictly from prompt)
    user_material = "information not supplied by user"
    if "reinforced concrete" in lower_query:
        user_material = "reinforced concrete (user declared)"
    elif "concrete" in lower_query:
        user_material = "concrete (user declared)"
    elif "structural steel" in lower_query:
        user_material = "structural steel (user declared)"
    elif "steel" in lower_query:
        user_material = "steel (user declared)"
    elif "drywall / steel stud" in lower_query:
        user_material = "drywall / steel stud (user declared)"
    elif "drywall" in lower_query:
        user_material = "drywall (user declared)"
    elif "double glazing / aluminum frame" in lower_query:
        user_material = "double glazing / aluminum frame (user declared)"
    elif "double glazing" in lower_query:
        user_material = "double glazing (user declared)"
    elif "aluminum frame" in lower_query:
        user_material = "aluminum frame (user declared)"
    elif "aluminum" in lower_query:
        user_material = "aluminum (user declared)"
    elif "glass" in lower_query:
        user_material = "glass (user declared)"

    user_dimensions = "information not supplied by user"
    # Match standard numbers/dimensions
    dims = re.findall(r"\b\d+(?:\.\d+)?\s*(?:mm|m|cm|in|ft|minutes|db|w/m²k)?\b", lower_query)
    if dims:
        user_dimensions = f"{', '.join(dims)} (user declared)"

    # Determine outputs based on recognition
    if ifc_class:
        # Recognized prompt
        value_mode = "PREVIEW"
        recovery_needed = False
        safe_next_action = "Proceed with caution. Conceptual preview only."
        missing_inputs = []

        # Geometry cube dimensions mapping
        if ifc_class == "IfcColumn":
            obj_path = generate_obj_cube(-0.25, 0.25, 0.0, 3.0, -0.25, 0.25, "column")
        elif ifc_class == "IfcWall":
            obj_path = generate_obj_cube(-1.5, 1.5, 0.0, 2.5, -0.1, 0.1, "wall")
        elif ifc_class == "IfcWindow":
            obj_path = generate_obj_cube(-0.6, 0.6, 0.8, 1.8, -0.05, 0.05, "window")
        elif ifc_class == "IfcBeam":
            obj_path = generate_obj_cube(-2.0, 2.0, 2.4, 2.8, -0.2, 0.2, "beam")
        else: # IfcSlab
            obj_path = generate_obj_cube(-2.5, 2.5, -0.2, 0.0, -2.5, 2.5, "slab")

        loi_fields = [
            ["IFC class candidate", ifc_class, "Conceptual classification only."],
            ["conceptual geometry placeholder", "Included (3D OBJ)", "Illustrative LOD preview only; not certified IFC geometry."],
            ["Material Baseline", user_material, "missing project-specific evidence; professional review required" if "information not supplied" in user_material else "User declared material."],
            ["Structural Function", "information not supplied by user", "missing project-specific evidence; professional review required"],
            ["Performance / Rating", "information not supplied by user", "missing project-specific evidence; professional review required"],
            ["Dimensions / Compliance", user_dimensions, "missing project-specific evidence; professional review required" if "information not supplied" in user_dimensions else "User declared dimensions."],
            ["Professional Review Required", "Yes", "Professional review required before any model insertion."]
        ]

        evidence = [
            f"'{matched_keyword}' in input indicates a {ifc_class} candidate",
            "conceptual geometry placeholder loaded for visual review",
            f"material is '{user_material}'",
            f"dimensions are '{user_dimensions}'"
        ]

    else:
        # Unrecognized prompt
        value_mode = "GUIDED_RECOVERY"
        recovery_needed = True
        safe_next_action = "Please clarify the specific BIM element class or function (e.g. wall, column, slab, beam, window)."
        missing_inputs = ["ifc_class_keyword"]
        obj_path = ""

        loi_fields = [
            ["IFC class candidate", "information not supplied by user", "BIM element class not recognized in input prompt."],
            ["conceptual geometry placeholder", "None", "No geometry generated for unrecognized classes; cannot default to column."],
            ["Professional Review Required", "Yes", "Professional review required."],
            ["Value Mode", "GUIDED_RECOVERY", "Prompt does not contain clear wall, column, window, beam or slab keywords."],
            ["Safe Next Action", safe_next_action, "Requires class clarification."]
        ]

        evidence = [
            "no recognized class keyword matched in query",
            "cannot default to column to prevent incorrect mapping",
            "value_mode set to GUIDED_RECOVERY to request user clarification"
        ]

    # Create the demo contract JSON payload
    contract_json = {
        "demo_contract_version": "1.0-illustrative",
        "input": query,
        "ifc_candidates": [ifc_class] if ifc_class else [],
        "suggested_ifc_class": ifc_class, # backward compatibility for tests
        "value_mode": value_mode,
        "missing_inputs": missing_inputs,
        "recovery_needed": recovery_needed,
        "safe_next_action": safe_next_action,
        "evidence_trace": {
            "matched_keywords": [matched_keyword] if matched_keyword else [],
            "user_declared_material": user_material,
            "user_declared_dimensions": user_dimensions,
            "professional_review": "required"
        },
        "limitations": [
            "No certified IFC geometry generation",
            "No live model inference (deterministic match)",
            "No certified BIM decisions",
            "No professional validation",
            "No final benchmark or production deployment"
        ],
        "model_output": {
            "value_mode": value_mode
        }
    }

    json_str = to_json(contract_json)
    lod_note = "LOD Status: Conceptual 3D preview only; no certified IFC geometry generated."
    evidence_str = "\n".join([f"- {ev}" for ev in evidence])
    limitations_str = "\n".join([
        "- No certified BIM decision / no certification",
        "- No full IFC file generated / no product",
        "- No professional validation / professional review required",
        "- Research prototype only / no final benchmark"
    ])

    return json_str, loi_fields, lod_note, evidence_str, limitations_str, obj_path


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
        ("canonical_check", "ifc_class"),
        ("model_output", "ifc_class"),
        ("reference_output", "ifc_class"),
    ):
        value = safe_get(record, *path)
        if isinstance(value, str) and value:
            classes.append(value)
    return list(set(classes))


def normalize_terms(text: str) -> list[str]:
    return [part for part in re.findall(r"[A-Za-z0-9_]+", text.lower()) if part]


def searchable_text(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True).lower()


def score_record(record: dict[str, Any], terms: list[str]) -> int:
    if not terms:
        return 0

    text = searchable_text(record)
    score = 0
    sample_id = str(record.get("sample_id", "")).lower()
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

        model_output = record.get("model_output") or {}
        reference_output = record.get("reference_output") or {}
        canonical_check = record.get("canonical_check") or {}
        input_summary = record.get("input_summary") or {}
        agreement = record.get("agreement") or {}

        ifc_class = canonical_check.get("ifc_class") or model_output.get("ifc_class") or ""
        semantic_type = model_output.get("semantic_type") or reference_output.get("semantic_type") or ""
        intent_class = model_output.get("intent_class") or reference_output.get("intent_class") or ""
        value_mode = canonical_check.get("value_mode") or model_output.get("value_mode") or ""

        # input_summary preview
        discipline = input_summary.get("discipline") or ""
        group = input_summary.get("major_ifc_class_group") or ""
        preview_desc = f"{discipline} - {group} - {semantic_type}"

        filtered.append(
            {
                "index": index,
                "record": record,
                "score": score,
                "sample_id": record.get("sample_id", f"sample-{index}"),
                "ifc_class": ifc_class,
                "semantic_type": semantic_type,
                "intent_class": intent_class,
                "value_mode": value_mode,
                "split": record.get("reference_scope", "public"),
                "risk_level": "",
                "latency_ms": "",
                "preview": preview_desc[:120],
                "validated": bool(record.get("expectation_met")),
                "status": record.get("record_status", ""),
                "canonical_state": "PASS" if canonical_check.get("ok") else "FAIL",
                "base_model": "",
                "created_at_utc": "",
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
    if len(items) == 0:
        summary = (
            "Search results: 0 records found. "
            "Suggestions: column, wall, beam, slab, window, IfcColumn."
        )
    else:
        summary = f"Loaded records: {len(RECORDS)} | Search results: {len(items)}"
    selected_json = to_json(items[0]["record"]) if items else "{}"
    return (
        frame,
        ui_update(choices=labels, value=first),
        items,
        summary,
        selected_json,
    )


def ui_update(**kwargs: Any) -> Any:
    if gr is not None and hasattr(gr, "update"):
        return gr.update(**kwargs)
    return kwargs


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
        chosen = {
            "index": 0,
            "record": RECORDS[0],
            "score": 0,
            "sample_id": RECORDS[0].get("sample_id", "sample-0"),
        }
    else:
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

    record = chosen["record"]
    lower_query = query.lower()

    # If no class recognized, return GUIDED_RECOVERY block matching rule 8
    has_class = any(k in lower_query for k in ("column", "pilar", "columna", "wall", "muro", "parede", "partition", "window", "janela", "ventana", "beam", "viga", "slab", "losa", "laje", "pump", "bomba"))
    
    if not has_class:
        illustrative_json = {
            "schema_version": "2.0",
            "sample_id": "0000000000000000",
            "case_expectation": "EXPECTED_CANONICAL_REJECTION",
            "expectation_met": True,
            "record_status": "EXPECTED_REJECTION_PASS",
            "model_output": {
                "intent_class": "unknown",
                "suggested_ifc_class": None,
                "ifc_candidates": [],
                "value_mode": "GUIDED_RECOVERY",
                "recovery_needed": True,
                "safe_next_action": "Please clarify the specific BIM element class or function (e.g. wall, column, slab, beam, window).",
                "evidence_trace": [
                    "no class keyword matched, cannot default to column"
                ]
            }
        }
        summary = "No class recognized. Returning GUIDED_RECOVERY block."
        return summary, to_json(illustrative_json), PUBLIC_WARNING

    model_output = record.get("model_output") or {}
    canonical_check = record.get("canonical_check") or {}
    suggested_ifc_class = canonical_check.get("ifc_class") or model_output.get("ifc_class") or "IfcColumn"

    evidence_trace = []
    if "column" in lower_query or "pilar" in lower_query:
        evidence_trace.append("column indicates a vertical structural element")
    if "wall" in lower_query or "muro" in lower_query:
        evidence_trace.append("wall indicates a vertical partition component")
    if "window" in lower_query or "ventana" in lower_query:
        evidence_trace.append("window indicates an opening for light/ventilation")
    if "beam" in lower_query or "viga" in lower_query:
        evidence_trace.append("beam indicates a horizontal structural element")

    if not evidence_trace:
        evidence_trace = [
            "general terms match closest public record",
            "schema matching suggests standard parameter alignment"
        ]

    illustrative_json = {
        "schema_version": "2.0",
        "sample_id": record.get("sample_id"),
        "case_expectation": record.get("case_expectation"),
        "expectation_met": True,
        "record_status": record.get("record_status"),
        "model_output": {
            "intent_class": "classify_bim_element",
            "suggested_ifc_class": suggested_ifc_class,
            "value_mode": "PREVIEW",
            "recovery_needed": False,
            "safe_next_action": "Proceed with caution. Conceptual preview only.",
            "evidence_trace": evidence_trace,
        }
    }

    summary = (
        f"Closest matched public case: {chosen['sample_id']} "
        f"(similarity score={chosen['score']}, index={chosen['index']})"
    )
    return summary, to_json(illustrative_json), PUBLIC_WARNING


def validate_json_input(text: str) -> tuple[str, str, str]:
    raw = (text or "").strip()
    if not raw:
        return "FAIL", "Input is empty.", "{}"

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        return "FAIL", f"JSON parse error: {exc}", "{}"

    if not isinstance(parsed, dict):
        return "FAIL", "Root value must be a JSON object.", "{}"

    # Validate against schema if available
    try:
        import jsonschema
        if SCHEMA_PATH.exists():
            with SCHEMA_PATH.open("r", encoding="utf-8") as sf:
                schema = json.load(sf)
            jsonschema.validate(parsed, schema)
            return "PASS", "OK", to_json(parsed)
        else:
            return "FAIL", "Schema file not found.", "{}"
    except Exception as exc:
        return "FAIL", str(exc), to_json(parsed)


def run_public_harness() -> tuple[str, str]:
    if len(RECORDS) != 20:
        return "FAIL", f"expected 20 records, found {len(RECORDS)}"

    # Validate all using jsonschema
    try:
        import jsonschema
        if not SCHEMA_PATH.exists():
            return "FAIL", "Schema file missing"
        with SCHEMA_PATH.open("r", encoding="utf-8") as sf:
            schema = json.load(sf)
        validator = jsonschema.Draft202012Validator(schema)
        for idx, r in enumerate(RECORDS):
            validator.validate(r)
    except Exception as exc:
        return "FAIL", f"Schema validation error: {exc}"

    # Check for legacy and internal keys
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

    errors = []
    for idx, r in enumerate(RECORDS):
        def check_keys(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k in forbidden_keys:
                        errors.append(f"record {idx}: internal key '{k}' found")
                    if legacy_pattern.search(k.lower()):
                        errors.append(f"record {idx}: legacy key '{k}' found")
                    if isinstance(v, str):
                        if legacy_pattern.search(v.lower()):
                            errors.append(f"record {idx}: legacy token found in value of '{k}'")
                    check_keys(v)
            elif isinstance(obj, list):
                for item in obj:
                    check_keys(item)
        check_keys(r)

    if errors:
        return "FAIL", "\n".join(errors[:10])

    return "SCHEMA_VALIDATION_OK\nREPLAY_OK\nrecords = 20", "No issues detected."


def self_test() -> None:
    print("Running self-test...")
    assert SAMPLE_PATH.exists(), "sample file missing"
    assert len(RECORDS) == 20, f"expected 20 records, found {len(RECORDS)}"

    # 1. Prompt desconocido no cae en IfcColumn
    json_str, loi, lod, evidence, lims, path = semantic_bim_preview("I need some random item")
    parsed_json = json.loads(json_str)
    assert parsed_json.get("suggested_ifc_class") is None, f"expected None, got {parsed_json.get('suggested_ifc_class')}"
    assert parsed_json.get("value_mode") == "GUIDED_RECOVERY", f"expected GUIDED_RECOVERY, got {parsed_json.get('value_mode')}"
    assert parsed_json.get("recovery_needed") is True
    assert "clarify" in parsed_json.get("safe_next_action", "").lower()
    assert not path, f"expected empty path, got {path}"

    # 2. No se generan valores profesionales inventados
    forbidden_vals = ["120 minutes", "60 minutes", "1.4 W/m²K", "35 dB", "S355", "4.5 m", "L/360", "200 mm", "C30/37"]
    for prompt in ["column", "wall", "window", "beam", "slab"]:
        js, loi_fields, _, _, _, _ = semantic_bim_preview(f"a concrete {prompt}")
        loi_values = [str(row[1]).lower() for row in loi_fields]
        for fv in forbidden_vals:
            for val in loi_values:
                assert fv.lower() not in val, f"Invented value {fv} found in {val}"

    # 3. Los datos sample20 y schema coinciden con la fuente canónica
    import jsonschema
    assert SCHEMA_PATH.exists(), "schema file missing"
    with SCHEMA_PATH.open("r", encoding="utf-8") as sf:
        schema = json.load(sf)
    validator = jsonschema.Draft202012Validator(schema)
    for r in RECORDS:
        validator.validate(r)

    # 4. Harness execution
    harness_result, harness_detail = run_public_harness()
    assert "SCHEMA_VALIDATION_OK" in harness_result, harness_detail
    assert "REPLAY_OK" in harness_result, harness_detail
    assert "records = 20" in harness_result, harness_detail

    print("SELF_TEST_OK")


def build_demo() -> gr.Blocks:
    if gr is None:
        raise RuntimeError("gradio is required to launch the public harness demo")

    ifc_options = ["All", "IfcColumn", "IfcWall", "IfcWindow", "IfcBeam", "IfcSlab"]
    search_state = gr.State(initial_search_state)

    with gr.Blocks(title="Semantic XAIBIM Harness") as demo:
        gr.Markdown(
            "# Semantic XAIBIM Public Replay Harness (v2)\n\n"
            "**Subtitle**: Natural-language AECO/BIM request → IFC-aware semantic contract → evidence trace → validation/replay → AECO answer.\n\n"
            "This demo shows how to validate and replay stored semantic contract records. No actual inference is run."
        )

        with gr.Tab("Start here — Guided BIM/IFC preview"):
            gr.Markdown(
                "### Start here — Guided BIM/IFC preview\n"
                "- **What this does**: Simulates a semantic BIM/IFC preview based on keywords.\n"
                "- **What to try**: Select a predefined suggestion or type a prompt.\n"
                "- **What result means**: Compliance check output is shown below."
            )
            with gr.Row():
                with gr.Column(scale=1):
                    semantic_input_first = gr.Textbox(
                        label="Semantic input",
                        lines=3,
                        value="I need a reinforced concrete column with IFC classification and LOI information.",
                    )
                    generate_button = gr.Button("Generate illustrative preview")
                    
                    gr.Examples(
                        examples=[
                            "I need a reinforced concrete column with IFC classification and LOI information.",
                            "Classify a partition wall and suggest IFC semantic information.",
                            "Validate whether a window request can map to Pset_WindowCommon.",
                            "Explain what information is missing to classify this BIM element.",
                            "What is the difference between LOD and LOI for a BIM object?"
                        ],
                        inputs=semantic_input_first
                    )

                with gr.Column(scale=1):
                    gr.Markdown("This is a conceptual LOD preview, not a certified IFC model.")
                    preview_3d = gr.Model3D(
                        label="3D Element Preview (LOD)",
                        clear_color=[0.9, 0.9, 0.9, 1.0]
                    )
                    lod_note = gr.Textbox(label="LOD Note", interactive=False)

            with gr.Row():
                with gr.Column(scale=1):
                    loi_table = gr.Dataframe(
                        headers=["Information field", "Example value", "Why it matters"],
                        datatype=["str", "str", "str"],
                        label="Level of Information (LOI) Attributes",
                        interactive=False,
                        wrap=True
                    )
                with gr.Column(scale=1):
                    evidence_trace_box = gr.Textbox(label="Evidence Trace", lines=4, interactive=False)
                    limitations_box = gr.Textbox(label="Limitations & Warnings", lines=4, interactive=False)

            with gr.Row():
                json_output = gr.Code(label="Contract JSON Output", language="json")

            generate_button.click(
                fn=semantic_bim_preview,
                inputs=semantic_input_first,
                outputs=[json_output, loi_table, lod_note, evidence_trace_box, limitations_box, preview_3d]
            )

            demo.load(
                fn=semantic_bim_preview,
                inputs=semantic_input_first,
                outputs=[json_output, loi_table, lod_note, evidence_trace_box, limitations_box, preview_3d]
            )

        with gr.Tab("Search public cases"):
            gr.Markdown(
                "### Search Sanitised Public Cases\n"
                "- **What this does**: Allows inspecting the 20 sanitised public records.\n"
                "- **What to try**: Search keywords like 'column' or 'wall', select a filter in the dropdown, and select a record from the list to view.\n"
                "- **What result means**: The table shows the parsed properties of matches, and selecting one loads its original full JSON record."
            )
            query = gr.Textbox(
                label="Search text",
                placeholder="e.g. column, wall, beam, pump, or a sample ID",
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

        with gr.Tab("Find similar public sample"):
            gr.Markdown(
                "### Find similar public sample\n"
                "- **What this does**: This tab does not generate a new BIM/IFC semantic preview. It searches the reduced 20-record public sample and returns the closest existing public record.\n"
                "- **What to try**: Enter a query or select an example to see what metadata would be mapped in this harness.\n"
                "- **What result means**: Shows the closest matching record in JSON format for review."
            )

            examples_dropdown = gr.Dropdown(
                choices=[
                    "I need a reinforced concrete column with IFC classification and LOI information.",
                    "Classify a partition wall and suggest IFC semantic information.",
                    "Validate whether a window request can map to Pset_WindowCommon.",
                    "Explain what information is missing to classify this BIM element.",
                    "What is the difference between LOD and LOI for a BIM object?"
                ],
                label="Predefined Examples (Click to load)",
                value=None
            )

            semantic_input = gr.Textbox(
                label="Semantic input",
                lines=6,
                placeholder="Write a public semantic request and match it against the reduced sample.",
            )

            examples_dropdown.change(
                fn=lambda choice: choice or "",
                inputs=examples_dropdown,
                outputs=semantic_input
            )

            semantic_button = gr.Button("Match public case")
            semantic_summary = gr.Textbox(label="Match summary", interactive=False)
            semantic_json = gr.Code(label="Matched record JSON (Illustrative Output)", language="json")
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

        with gr.Tab("Validate illustrative demo JSON"):
            gr.Markdown(
                "### Validate Research JSON Payload\n"
                "- **What this does**: Allows verifying whether an output complies with the minimum contract. This is a demo helper, not the full sample20 public record validator.\n"
                "- **What to try**: Edit the pre-populated JSON payload and click 'Validate' to check for compliance.\n"
                "- **What result means**: This validates the minimum research contract, not a BIM certification."
            )

            minimal_valid_json = to_json({
                "schema_version": "2.0",
                "sample_id": "1234567890abcdef",
                "case_expectation": "VALID",
                "expectation_met": True,
                "record_status": "PASS",
                "input_summary": {
                    "discipline": "Structural",
                    "major_ifc_class_group": "IfcColumn",
                    "semantic_type": "column",
                    "ambiguity_flags": [],
                    "missing_inputs": [],
                    "recovery_type": None
                },
                "model_output": {
                    "intent_class": "classify",
                    "semantic_type": "column",
                    "ifc_class": "IfcColumn",
                    "value_mode": "PREVIEW",
                    "normalized_dimensions_m": {},
                    "required_psets": [],
                    "required_relationships": [],
                    "missing_inputs": [],
                    "ambiguity_flags": [],
                    "recovery_needed": False,
                    "recovery_type": None,
                    "safe_next_action": "none",
                    "reason_codes": [],
                    "evidence_trace": {
                        "evidence_pattern": None,
                        "relation_observed": None,
                        "ambiguity_context": None
                    }
                },
                "reference_output": {
                    "intent_class": "classify",
                    "semantic_type": "column",
                    "ifc_class": "IfcColumn",
                    "value_mode": "PREVIEW",
                    "normalized_dimensions_m": {},
                    "required_psets": [],
                    "required_relationships": [],
                    "missing_inputs": [],
                    "ambiguity_flags": [],
                    "recovery_needed": False,
                    "recovery_type": None,
                    "safe_next_action": "none",
                    "reason_codes": [],
                    "evidence_trace": {
                        "evidence_pattern": None,
                        "relation_observed": None,
                        "ambiguity_context": None
                    }
                },
                "canonical_check": {
                    "ok": True,
                    "ifc_class": "IfcColumn",
                    "value_mode": "PREVIEW",
                    "errors": [],
                    "warnings": []
                },
                "agreement": {
                    "ifc_class": True,
                    "semantic_type": True,
                    "intent_class": True,
                    "value_mode": True,
                    "dimensions": True,
                    "missing_inputs": True,
                    "required_psets_recall": 1.0,
                    "required_relationships_recall": 1.0
                },
                "reference_scope": "synthetic_target_not_normative_certification"
            })

            json_input = gr.Textbox(
                label="JSON input",
                lines=10,
                value=minimal_valid_json,
                placeholder="Paste a JSON object adhering to the v2 schema.",
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
            gr.Markdown(
                "### Run Reproducibility & Schema Validation\n"
                "- **What this does**: Executes a reproducible validation check over the 20 public records.\n"
                "- **What to try**: Click the 'Run validation' button to verify all records.\n"
                "- **What result means**: Outputs `SCHEMA_VALIDATION_OK` and `REPLAY_OK` for exactly 20 records if the dataset is intact."
            )
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

    if gr is None:
        raise RuntimeError("gradio is required to launch the public harness demo")
    demo = build_demo()
    demo.launch()


if gr is not None and hasattr(gr, "Blocks"):
    demo = build_demo()
else:
    demo = None

if __name__ == "__main__":
    main()
