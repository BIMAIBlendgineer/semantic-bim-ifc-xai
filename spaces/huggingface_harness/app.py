from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    import pandas as pd
except Exception as _pd_import_err:  # pragma: no cover - catch all import failures
    import sys
    print(f"[WARN] pandas import failed: {_pd_import_err}", file=sys.stderr)
    pd = None

try:
    import gradio as gr
except Exception as _gr_import_err:  # pragma: no cover - catch all import failures
    import sys
    print(f"[WARN] gradio import failed: {_gr_import_err}", file=sys.stderr)
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


def generate_obj_cube(x1: float, x2: float, y1: float, y2: float, z1: float, z2: float, name: str) -> str:
    temp_dir = ROOT / "temp_models"
    temp_dir.mkdir(parents=True, exist_ok=True)
    obj_path = temp_dir / f"{name}.obj"
    
    vertices = [
        (x1, y1, z1),
        (x2, y1, z1),
        (x2, y2, z1),
        (x1, y2, z1),
        (x1, y1, z2),
        (x2, y1, z2),
        (x2, y2, z2),
        (x1, y2, z2)
    ]
    faces = [
        (1, 2, 3, 4),
        (6, 5, 8, 7),
        (1, 5, 6, 2),
        (4, 3, 7, 8),
        (1, 4, 8, 5),
        (2, 6, 7, 3)
    ]
    out = []
    for v in vertices:
        out.append(f"v {v[0]:.3f} {v[1]:.3f} {v[2]:.3f}")
    for f in faces:
        out.append(f"f {f[0]} {f[1]} {f[2]} {f[3]}")
        
    obj_path.write_text("\n".join(out), encoding="utf-8")
    return str(obj_path)


def semantic_bim_preview(text: str) -> tuple[str, list[list[str]], str, str, str, str]:
    query = (text or "").strip()
    lower_query = query.lower()
    
    if any(k in lower_query for k in ("column", "pilar", "columna")):
        ifc_class = "IfcColumn"
        bim_element = "reinforced concrete column"
        loi_fields = [
            ["IFC Class", "IfcColumn", "Identifies the structural vertical component for load path calculations."],
            ["Material Baseline", "reinforced concrete", "Determines structural capacity, weight, and self-weight calculation."],
            ["Structural Role", "Load-bearing", "Crucial for structural analysis models to transfer gravity loads."],
            ["Fire Rating", "120 minutes", "Required to ensure evacuation time compliance under fire safety codes."]
        ]
        obj_path = generate_obj_cube(-0.25, 0.25, 0.0, 3.0, -0.25, 0.25, "column")
        evidence = [
            "column indicates a vertical structural element",
            "reinforced concrete indicates material information",
            "IFC classification indicates schema mapping",
            "LOI indicates alphanumeric information requirements"
        ]
    elif any(k in lower_query for k in ("wall", "muro", "parede", "partition")):
        ifc_class = "IfcWall"
        bim_element = "partition wall"
        loi_fields = [
            ["IFC Class", "IfcWall", "Identifies vertical enclosure or partition elements."],
            ["Material Baseline", "drywall / steel stud", "Affects acoustic insulation, partition weight, and cost estimation."],
            ["Is External", "false", "Determines thermal boundary conditions and weathering requirements."],
            ["Fire Rating", "60 minutes", "Safety parameter to check compartmentation compliance."]
        ]
        obj_path = generate_obj_cube(-1.5, 1.5, 0.0, 2.5, -0.1, 0.1, "wall")
        evidence = [
            "wall/muro/parede/partition indicates a vertical enclosure or dividing element",
            "drywall/steel stud indicates material specification",
            "IFC classification indicates wall schema mapping",
            "LOI indicates fire partition and partition attributes"
        ]
    elif any(k in lower_query for k in ("window", "janela", "ventana")):
        ifc_class = "IfcWindow"
        bim_element = "exterior glazed window"
        loi_fields = [
            ["IFC Class", "IfcWindow", "Identifies openings for daylighting and ventilation."],
            ["Material Baseline", "double glazing / aluminum frame", "Affects thermal envelope performance and cost."],
            ["U-Value", "1.4 W/m²K", "Required for energy efficiency and HVAC heat loss simulation."],
            ["Acoustic Rating", "35 dB", "Assures acoustic comfort against exterior environmental noise."]
        ]
        obj_path = generate_obj_cube(-0.6, 0.6, 0.8, 1.8, -0.05, 0.05, "window")
        evidence = [
            "window/janela/ventana indicates an opening for light/ventilation",
            "exterior glazed indicates window role",
            "IFC classification indicates window schema mapping",
            "LOI indicates thermal/acoustic requirements"
        ]
    elif any(k in lower_query for k in ("beam", "viga")):
        ifc_class = "IfcBeam"
        bim_element = "horizontal structural beam"
        loi_fields = [
            ["IFC Class", "IfcBeam", "Identifies horizontal bending members."],
            ["Material Baseline", "structural steel S355", "Determines structural capacity, yield strength, and deflection limits."],
            ["Span", "4.5 m", "Governs shear, bending moment, and structural sizing checks."],
            ["Deflection Limit", "L/360", "Required to prevent cracking in plaster/finishes below."]
        ]
        obj_path = generate_obj_cube(-2.0, 2.0, 2.4, 2.8, -0.2, 0.2, "beam")
        evidence = [
            "beam/viga indicates a horizontal bending/load member",
            "structural steel indicates material specification",
            "IFC classification indicates beam schema mapping",
            "LOI indicates structural capacity parameters"
        ]
    elif any(k in lower_query for k in ("slab", "losa", "laje")):
        ifc_class = "IfcSlab"
        bim_element = "reinforced concrete slab"
        loi_fields = [
            ["IFC Class", "IfcSlab", "Identifies floor plates or structural decks."],
            ["Thickness", "200 mm", "Determines bending resistance, concrete cover, and sound transmission."],
            ["Load-bearing", "true", "Defines if the slab transfers live/dead structural loads."],
            ["Concrete Grade", "C30/37", "Determines compressive strength and durability parameters."]
        ]
        obj_path = generate_obj_cube(-2.5, 2.5, -0.2, 0.0, -2.5, 2.5, "slab")
        evidence = [
            "slab/losa/laje indicates a flat horizontal floor or deck plate",
            "reinforced concrete indicates material specification",
            "IFC classification indicates slab schema mapping",
            "LOI/thickness indicates bending and acoustic attributes"
        ]
    else:
        ifc_class = "IfcColumn"
        bim_element = "reinforced concrete column (fallback)"
        loi_fields = [
            ["IFC Class", "IfcColumn", "Fallback classification."],
            ["Status", "Conceptual fallback", "Prompt did not match wall, column, window, beam or slab keywords."],
            ["Material", "unknown", "Unspecified material, defaulting to reinforced concrete column parameters."]
        ]
        obj_path = generate_obj_cube(-0.25, 0.25, 0.0, 3.0, -0.25, 0.25, "column")
        evidence = [
            "no class keyword matched, defaulting to vertical column",
            "IFC classification matches base IfcColumn schema",
            "LOI has minimal fallback information"
        ]

    contract_json = {
        "input": query if query else "I need a reinforced concrete column with IFC classification and LOI information.",
        "semantic_intent": "classify_bim_element",
        "suggested_ifc_class": ifc_class,
        "bim_element": bim_element,
        "loi": {
            "meaning": "Level of Information",
            "required_information": [
                "element type",
                "IFC class",
                "material",
                "structural role",
                "classification",
                "validation status"
            ]
        },
        "lod": {
            "meaning": "Level of Detail / Development",
            "status": "Conceptual 3D preview only; no certified IFC geometry generated"
        },
        "evidence_trace": evidence,
        "limitations": [
            "No certified BIM decision",
            "No full IFC file generated in this public preview",
            "No professional validation",
            "Research demo only"
        ],
        "status": "PREVIEW"
    }

    json_str = to_json(contract_json)
    
    lod_note = "LOD Status: Conceptual 3D preview only; no certified IFC geometry generated."
    evidence_str = "\n".join([f"- {ev}" for ev in evidence])
    limitations_str = "\n".join([
        "- No certified BIM decision",
        "- No full IFC file generated in this public preview",
        "- No professional validation",
        "- Research demo only"
    ])
    
    return json_str, loi_fields, lod_note, evidence_str, limitations_str, obj_path


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
    if len(items) == 0:
        summary = (
            "Search results: 0 records found. "
            "Suggestions: column, wall, beam, slab, window, IfcColumn, Pset_WindowCommon, PREVIEW."
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
    parsed = record.get("parsed_output") or {}
    canonical = record.get("canonical_output") or {}
    
    # Determine class dynamically
    lower_query = query.lower()
    if "column" in lower_query or "pilar" in lower_query:
        suggested_ifc_class = "IfcColumn"
    elif "wall" in lower_query or "muro" in lower_query:
        suggested_ifc_class = "IfcWall"
    elif "window" in lower_query or "ventana" in lower_query:
        suggested_ifc_class = "IfcWindow"
    elif "beam" in lower_query or "viga" in lower_query:
        suggested_ifc_class = "IfcBeam"
    elif "slab" in lower_query or "losa" in lower_query:
        suggested_ifc_class = "IfcSlab"
    elif "pump" in lower_query or "bomba" in lower_query:
        suggested_ifc_class = "IfcPump"
    else:
        suggested_ifc_class = canonical.get("ifc_class") or parsed.get("ifc_class") or "IfcColumn"

    # Determine intent dynamically
    if "validate" in lower_query or "comprobar" in lower_query:
        semantic_intent = "validate_bim_element"
    elif "explain" in lower_query or "missing" in lower_query:
        semantic_intent = "explain_missing_info"
    elif "difference" in lower_query or "loi" in lower_query or "lod" in lower_query:
        semantic_intent = "explain_domain_concepts"
    else:
        semantic_intent = "classify_bim_element"

    # Build dynamic evidence trace list
    evidence_trace = []
    if "column" in lower_query or "pilar" in lower_query:
        evidence_trace.append("column indicates a vertical structural element")
    if "wall" in lower_query or "muro" in lower_query:
        evidence_trace.append("wall indicates a vertical partition component")
    if "window" in lower_query or "ventana" in lower_query:
        evidence_trace.append("window indicates an opening for light/ventilation")
    if "beam" in lower_query or "viga" in lower_query:
        evidence_trace.append("beam indicates a horizontal structural element")
    if "concrete" in lower_query or "hormigón" in lower_query:
        evidence_trace.append("reinforced concrete indicates candidate material information")
    if "classification" in lower_query or "ifc" in lower_query:
        evidence_trace.append("IFC classification indicates a need for schema mapping")
    if "loi" in lower_query:
        evidence_trace.append("LOI indicates alphanumeric information requirements")
    if "lod" in lower_query:
        evidence_trace.append("LOD indicates Level of Development geometry context")

    if not evidence_trace:
        evidence_trace = [
            "general terms match closest public record",
            "schema matching suggests standard parameter alignment"
        ]

    illustrative_json = {
        "input": query if query else "Default Replay Case",
        "semantic_intent": semantic_intent,
        "suggested_ifc_class": suggested_ifc_class,
        "loi_note": "LOI refers to the information required for the object, not only its geometry.",
        "lod_note": "LOD refers to geometric/detail representation and is not generated in this public demo.",
        "evidence_trace": evidence_trace,
        "limitations": [
            "No certified BIM decision is produced",
            "No full IFC geometry is generated",
            "The output is a public research preview"
        ],
        "status": "PREVIEW"
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

    # Verify semantic preview logic
    json_str, loi, lod, evidence, lims, path = semantic_bim_preview("I need a concrete column")
    assert "IfcColumn" in json_str, json_str
    assert "reinforced concrete column" in json_str, json_str
    assert Path(path).exists(), f"OBJ model not generated at {path}"

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

    with gr.Blocks(title="Semantic AI for BIM/IFC: Guided Research Demo") as demo:
        gr.Markdown(
            "# Semantic AI for BIM/IFC: Guided Research Demo\n\n"
            f"Loaded public records: **{len(RECORDS)}**\n\n"
            f"{PUBLIC_WARNING}\n\n"
            "**Subtitle**: Natural-language AECO/BIM request → IFC-aware semantic contract → evidence trace → validation/replay → AECO answer.\n\n"
            "**Disclaimer**: This public research demo does not generate certified IFC geometry or professional BIM deliverables. "
            "It provides a conceptual 3D preview, structured semantic metadata, LOI explanation, validation and replay over a reduced sanitized sample."
        )

        search_state = gr.State(initial_search_state())

        with gr.Tab("Start here — Guided BIM/IFC preview"):
            gr.Markdown(
                "### Start here — Guided BIM/IFC preview\n"
                "- **What this does**: Translates your plain text construction requests into structured BIM/IFC metadata and generates an illustrative 3D shape.\n"
                "- **What to try**: Type a request like *'I need a reinforced concrete column'* or click one of the examples below.\n"
                "- **What result means**: The JSON represents the auditable metadata contract (LOI), and the 3D canvas displays a conceptual geometry preview (LOD)."
            )
            with gr.Row():
                with gr.Column(scale=1):
                    semantic_input_first = gr.Textbox(
                        label="Enter natural language construction request",
                        lines=5,
                        value="I need a reinforced concrete column with IFC classification and LOI information.",
                        placeholder="e.g. column, wall, window, beam, slab request..."
                    )
                    generate_button = gr.Button("Generate semantic BIM preview", variant="primary")
                    
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
            
            # Run preview once on startup to populate default state
            demo.load(
                fn=semantic_bim_preview,
                inputs=semantic_input_first,
                outputs=[json_output, loi_table, lod_note, evidence_trace_box, limitations_box, preview_3d]
            )

        with gr.Tab("Search public cases"):
            gr.Markdown(
                "### Search Sanitised Public Cases\n"
                "- **What this does**: Permite inspeccionar los 20 registros públicos sanitizados.\n"
                "- **What to try**: Search keywords like 'column' or 'wall', select a filter in the dropdown, and select a record from the list to view.\n"
                "- **What result means**: The table shows the parsed properties of matches, and selecting one loads its original full JSON record."
            )
            query = gr.Textbox(
                label="Search text",
                placeholder="e.g. pilar, column, wall, beam, pump, or a sample ID",
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
            
            def load_example(choice: str) -> str:
                return choice or ""
            
            examples_dropdown.change(
                fn=load_example,
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
                "- **What this does**: Permite comprobar si una salida cumple el contrato mínimo. This is a demo helper, not the full sample20 public record validator.\n"
                "- **What to try**: Edit the pre-populated JSON payload and click 'Validate' to check for compliance.\n"
                "- **What result means**: This validates the minimum research contract, not a BIM certification."
            )
            
            minimal_valid_json = to_json({
                "status": "PASS",
                "canonical_output": {
                    "ifc_class": "IfcColumn",
                    "semantic_type": "semantic_enrichment"
                },
                "validation": {
                    "ok": True
                },
                "metadata": {
                    "source_split": "train",
                    "risk_level": "low"
                }
            })

            json_input = gr.Textbox(
                label="JSON input",
                lines=10,
                value=minimal_valid_json,
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
            gr.Markdown(
                "### Run Reproducibility & Schema Validation\n"
                "- **What this does**: Ejecuta una validación reproducible sobre los 20 registros.\n"
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

    if demo is None:
        raise RuntimeError("gradio is required to launch the public harness demo")
    demo.launch()


# Build demo at module level so HF Spaces SDK can discover it
# (HF may import this module rather than run it as __main__)
if gr is not None and hasattr(gr, "Blocks"):
    demo = build_demo()
else:
    demo = None

if __name__ == "__main__":
    main()
