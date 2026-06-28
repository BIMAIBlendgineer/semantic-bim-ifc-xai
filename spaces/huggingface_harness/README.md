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

> [!WARNING]
> **Important Disclaimers**:
> - **This is not a full BIM authoring tool.**
> - **This is not a certified IFC generator.**
> - **This is a public research demo for semantic BIM/IFC interpretation.**
> - **This public demo does not generate full IFC geometry or certified BIM deliverables. It demonstrates semantic interpretation, structured output, validation and replay over a reduced sanitized sample.**

This Space is a public research validation harness loaded with 20 sanitized, hand-annotated records. It is intentionally separated from commercial XAIBIM ecosystem components. It is not an official product, certification system, university service or institutional endorsement.

---

## Tab Guide

### 1. Start here — Natural language to BIM/IFC semantic preview
- **What this does**: Translates your plain text construction requests into structured BIM/IFC metadata and generates an illustrative 3D shape.
- **What to try**: Type a request like *'I need a reinforced concrete column'* or click one of the examples below.
- **What result means**: The JSON represents the auditable metadata contract (LOI), and the 3D canvas displays a conceptual geometry preview (LOD).

### 2. Search public cases
- **What this does**: Permite inspeccionar los 20 registros públicos sanitizados.
- **What to try**: Search keywords like 'column' or 'wall', select a filter in the dropdown, and select a record from the list to view.
- **What result means**: The table shows the parsed properties of matches, and selecting one loads its original full JSON record.

### 3. Try semantic input
- **What this does**: Permite escribir una petición técnica. La demo pública no genera IFC nuevo; devuelve una interpretación semántica ilustrativa basada en matching y estructura JSON.
- **What to try**: Enter a query or select an example to see what metadata would be mapped in this harness.
- **What result means**: Shows the closest matching record in JSON format for review.

### 4. Validate JSON
- **What this does**: Permite comprobar si una salida cumple el contrato mínimo.
- **What to try**: Edit the pre-populated JSON payload and click 'Validate' to check for compliance.
- **What result means**: Returns PASS if all required keys (`status`, `canonical_output`, `validation`, `metadata`) are present, otherwise lists errors.

### 5. Run public harness
- **What this does**: Ejecuta una validación reproducible sobre los 20 registros.
- **What to try**: Click the 'Run validation' button to verify all records.
- **What result means**: Outputs `SCHEMA_VALIDATION_OK` and `REPLAY_OK` for exactly 20 records if the dataset is intact.

---

## Usage Examples

To test the **Start here** and **Try semantic input** tabs, you can use any of the following predefined prompts:

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

---

The long-term goal is not to replace engineers, but to study how AI systems can make BIM/IFC interpretation more explicit, auditable and explainable.
