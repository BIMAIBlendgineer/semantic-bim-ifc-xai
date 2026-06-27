# Research Overview

## 1. Engineering Problem

BIM projects contain geometric, alphanumeric and documentary information. However, much engineering intent still appears as natural language: requirements, comments, design decisions, review notes, specifications and coordination instructions. The research question is how AI can interpret this natural language and map it to structured BIM/IFC concepts without losing traceability.

On active construction and engineering projects, communication is often unstructured. The translation from natural-language engineering intent (e.g. email threads or client requirements) to physical databases must be systematized to reduce structural errors, misalignment, and parameter corruption.

---

## 2. BIM as Information Management

Under the global standards such as **ISO 19650**, Building Information Modeling (BIM) is defined not merely as a 3D CAD modeling process, but as a collaborative, structured framework for managing information over the entire lifecycle of a built asset. 

ISO 19650 introduces concepts such as:
- **Exchange Information Requirements (EIR)**: Defining exactly what data needs to be delivered at different phases.
- **Common Data Environment (CDE)**: The single source of truth for all project information.
- **Level of Information Need**: Specifying the quantity, quality, and granularity of geometric and non-geometric information.

Semantic AI research aims to automate the translation of natural-language requirements directly into these regulated structures.

---

## 3. IFC as Semantic Infrastructure

To ensure software interoperability, the industry relies on the **Industry Foundation Classes (IFC)** schema (ISO 16739). IFC is an open, object-oriented data specification that provides a logical framework to represent building components, properties, and relationships.

Key components of the IFC semantic infrastructure include:
- **Spatial Hierarchies**: e.g., `IfcProject` &rarr; `IfcSite` &rarr; `IfcBuilding` &rarr; `IfcBuildingStorey`.
- **Physical Entities**: e.g., `IfcColumn`, `IfcWall`, `IfcWindow`, `IfcBeam`.
- **Property Sets (Psets)**: Alphanumeric attribute sheets attached to entities (e.g., `Pset_WallCommon`, `Pset_WindowCommon`).
- **Relational Grounding**: Establishing clear object relationships (e.g., connecting a wall and a column via `IfcRelConnectsElements`).

---

## 4. Semantic AI

In this research context, "semantic" goes beyond simple word association or conversational AI. It refers to the systematic alignment of human natural language with standard technical schemas. 

The complete translation pipeline operates as:
`natural language → engineering meaning → IFC candidate → information requirement → validation → evidence trace`.

Rather than acting as a creative text generator, a semantic parser behaves as a classifier and structurer, mapping unstructured prompts into explicit, typed entities governed by engineering schemas.

---

## 5. Why JSON Contracts

The research harness uses JSON (JavaScript Object Notation) and JSONL (JSON Lines) to structure predictions. This format is selected because it enables:
- **Machine-readable outputs**: Standardized payloads can be ingested by any BIM authoring plugin or CDE system.
- **Reproducible validation**: The structured format allows schema checkers to evaluate keys and data types programmatically.
- **Model comparisons**: Enables researchers to run different LLMs on identical inputs and contrast their schema compliance rates.
- **Auditing and Replay**: Simplifies tracing historical predictions, letting developers replay inputs and inspect output flags.
- **Downstream CDE Integration**: Facilitates writing parameters directly back to active databases with high structural security.

---

## 6. Current Public Harness

The public harness hosted in this repository is a reduced demonstration designed to review the core architecture of the research.
- **Sanitized Dataset**: Uses a limited database of 20 hand-annotated, sanitized records.
- **No Live Inference**: The web interface does not call live model servers or API keys.
- **No 3D Generation**: It is designed to validate text metadata classification, not coordinate geometries.
- **Focus**: Serves as a peer-review tool to audit matching mechanics, JSON contracts, and local verification runs.

---

## 7. Limitations

- **No geometric generation**: The system does not output 3D geometry or model files (no physical IFC files are generated).
- **No live public model**: There is no live neural network running inference in the public web app.
- **No SHAP/LIME feature attribution**: Mathematical explanation metrics are not implemented in this public release.
- **No technical certification**: The system does not certify BIM models for compliance or regulatory review.
- **No replacement for human review**: All AI predictions are preview-only and must be audited by qualified civil engineers before model insertion.
