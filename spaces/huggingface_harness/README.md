---
title: Semantic AI for BIM/IFC Public Harness
emoji: 🧪
colorFrom: blue
colorTo: gray
sdk: gradio
sdk_version: 5.33.0
app_file: app.py
pinned: false
license: mit
---

# Semantic AI for BIM/IFC: Public Research Harness

A public research artifact for studying how natural-language engineering requests can be mapped into structured BIM/IFC semantic outputs, validated records, evidence traces and future explainable AI workflows.

> **This public demo does not generate full IFC geometry or certified BIM deliverables. It demonstrates semantic interpretation, structured output, validation and replay over a reduced sanitized sample.**

This Space is a public research validation harness loaded with 20 sanitized, hand-annotated records. It is intentionally separated from commercial XAIBIM ecosystem components. It is not an official product, certification system, university service or institutional endorsement.

---

## Tab Guide

### 1. Search public cases
**Permite inspeccionar los 20 registros públicos sanitizados.**

Query the 20 public research records stored in the harness database. You can search by keywords (e.g. **column**, **wall**, **beam**, **pump**, **slab**) or look up specific sample IDs. Filter by target IFC class using the dropdown selector. If no results are returned, suggestions are displayed automatically.

### 2. Try semantic input
**Permite escribir una petición técnica. La demo pública no genera IFC nuevo; devuelve una interpretación semántica ilustrativa basada en matching y estructura JSON.**

Type or select a natural-language engineering prompt. The system returns an illustrative JSON output containing:
- `semantic_intent`: the classification task inferred
- `suggested_ifc_class`: the candidate IFC entity class
- `loi_note`: what Level of Information (LOI) this request implies
- `lod_note`: why LOD (geometry) is not generated in this demo
- `evidence_trace`: key semantic signals identified in the prompt
- `limitations`: explicit scope limitations
- `status`: always `PREVIEW` in this public demo

**This tab does not call any live model server. All interpretation is rule-based against the public sample.**

### 3. Validate JSON
**Permite comprobar si una salida cumple el contrato mínimo.**

Paste any JSON object to validate whether it conforms to the core research contract schema. The contract requires at minimum the following keys: `status`, `canonical_output`, `validation`, and `metadata`. A pre-populated minimal valid example is shown on load.

### 4. Run public harness
**Ejecuta una validación reproducible sobre los 20 registros.**

Runs the reproducibility and schema integrity suite over all 20 sanitized records in `sample20_public_predictions.jsonl`. This confirms that every record is fully compliant with the core contract, schema keys are present, and the file parses correctly.

---

## Usage Examples

To test the **Try semantic input** tab, you can use any of the following predefined prompts:

1. *"I need a reinforced concrete column with IFC classification and LOI information."*
2. *"Classify a partition wall and suggest IFC semantic information."*
3. *"Validate whether a window request can map to Pset_WindowCommon."*
4. *"Explain what information is missing to classify this BIM element."*
5. *"What is the difference between LOD and LOI for a BIM object?"*

---

## Scope Limitations

- **No 3D IFC geometry generation**: the public harness does not output 3D coordinate files.
- **No live model inference**: matching is deterministic and resolved against the static 20-record database.
- **No certified BIM decisions**: all outputs are labelled `PREVIEW` and must be audited by qualified engineers before any model insertion.
- **No private data**: no credentials, API keys, internal logs or proprietary BIM data are exposed.

---

The long-term goal is not to replace engineers, but to study how AI systems can make BIM/IFC interpretation more explicit, auditable and explainable.
