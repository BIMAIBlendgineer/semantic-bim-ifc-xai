# Dataset Construction and Training-Readiness Methodology

## 1. Scientific Motivation

The semantic interpretation of Building Information Modeling (BIM) data in the context of the Industry Foundation Classes (IFC) schema is not a generic prompt-response task. Standard natural language processing systems often treat text inputs and structured outputs in isolation, disregarding the deep domain constraints inherent in civil engineering. A valid semantic BIM record must capture and formalize:

- **Engineering Intent**: The precise technical objective requested by the practitioner (e.g., classification, property enrichment, spatial query, compliance check).
- **BIM/IFC Context**: The structural topology, spatial relationships, and metadata of the element under consideration.
- **IFC Class Candidate**: The target entity within the IFC schema hierarchy (e.g., `IfcWall`, `IfcColumn`, `IfcSlab`).
- **Information Requirements**: The Level of Information Need (LOIN) specifying mandatory properties, quantities, and classifications.
- **Evidence Trace**: The explicit grounds (GlobalIds, property sets, rules, or geometric parameters) that justify a classification or property assignment.
- **Validation State and Traceability**: Audit metadata detailing origin, sanitization status, and schema validation results.

Without these components, models are prone to hallucinating invalid IFC classes, incorrect property set mappings, and groundless technical claims — compromising safety and quality in governed AECO workflows.

---

## 2. Rejection of Plain Instruction-Output Training

Conventional LLM fine-tuning on plain `instruction/context/output` text pairs was rejected for several critical reasons:

1. **Lack of Schema Enforcement**: Standard token-generation models do not inherently respect the strict syntax and schema requirements of formats like IFC, ifcJSON, or structured engineering contracts.
2. **Hallucination of Catalogues**: In civil engineering, elements must map to canonical classification catalogues and standard property sets. Plain text outputs fail to maintain alignments with these Single Sources of Truth (SSOT).
3. **Absence of Grounding and Rationale**: A plain text response cannot easily be audited. Engineering decisions require a clear evidence trace back to the source model.
4. **Mutational Safety**: Plain instructions do not distinguish between safe queries (read-only preview) and destructive mutations (model alterations), presenting risks to the integrity of Common Data Environments (CDE).

Dataset design therefore centers on structured, schema-validated runtime payloads mapped to canonical catalogues.

---

## 3. Runtime and Payload Architecture

The dataset and pipeline infrastructure is governed by several key concepts:

- **Runtime Payload and SSOT**: A structured payload encapsulates the input prompt, the active database schema, and the target catalogues, ensuring any generated output is evaluated against a Single Source of Truth.
- **Capabilities Catalog**: A registry of supported operations, classes, and properties, preventing the AI from generating arbitrary properties or violating schema rules.
- **Internal Milestones (S18 / S19 / S20)**: Successive pipeline iterations improving validation rigor, catalogue mapping, and blocked-by-prerequisite gate enforcement.
  - **S18**: Introduced database schemas for dataset candidate tracking; suspended due to inadequate validation gates.
  - **S19**: Introduced runtime catalogue mapping and strict output validation.
  - **S20**: Established the fail-closed "blocked-by-prerequisite" gate.
- **pilot1000**: A private development pilot of 1,000 curated cases for early LoRA/QLoRA adaptation experiments (not published).
- **sample20**: A public, fully sanitized subset of 20 representative cases for scientific evidence and reproducible evaluation.
- **Replay and Guided Harness**: Codebases that ingest prompt records and run deterministic replay validation to verify schema compliance, class mapping, and evidence-tracing contracts.

---

## 4. Chronology of Technical Development Phases

| Phase | Title | Description |
|---|---|---|
| 0 | Scientific Problem Definition | Established limits of NL interfaces in BIM; identified semantic interpretation gap. |
| 1 | Literature and Domain Framing | Analysed state of the art; defined lack of auditable evidence as the primary research gap. |
| 2 | Semantic Record Definition | Formalized the record structure: NL request, IFC class, LOI, conceptual LOD, evidence trace. |
| 3 | Runtime/Payload Discovery | Initial payload design; discovered structured prompting templates required for correct JSON output. |
| 4 | SSOT and Catalogue Correction | Integrated canonical catalogues; corrected schemas to prevent out-of-spec property generation. |
| 5 | S18 Training-Readiness Suspension | Pipeline suspended — inadequate sanitization and deduplication checks. |
| 6 | S19 Runtime/Catalog Validation | Strict runtime validation schemas; automated output compliance before dataset commit. |
| 7 | S20 Blocked-by-Prerequisite Gate | Fail-closed gate: candidates lacking provenance, anonymization, or review are blocked. |
| 8 | Feedback/Raw Events Excluded | Governance decision: raw user feedback excluded from training lake until sanitized. |
| 9 | Semantic Record Contract Design | Finalized the structured data contract fields (intent, class, LOI, LOD, evidence, limitations). |
| 10 | JSON/JSONL Validation Strategy | Automated test suites for syntax and full schema compliance. |
| 11 | Dataset Candidate Governance | SQL migrations tracking `FrameworkDatasetCandidate` and `FrameworkDatasetGateDecision`. |
| 12 | Train/Val/Test/Eval/Rejected Split | Formulated strict criteria for dataset split assignment. |
| 13 | pilot1000 Private Experiment Boundary | QLoRA fine-tuning on private cluster; private model boundary defined. |
| 14 | sample20 Public Sanitized Subset | 20 representative cases extracted; proprietary data replaced with synthetic alternatives. |
| 15 | Replay Harness | Lightweight Python harness for deterministic schema and intent checking. |
| 16 | Guided Public Harness | Hugging Face interactive harness for external reviewer access. |
| 17 | Benchmark Methodology | Formal benchmark protocol: intent accuracy, slot F1, IFC class mapping, JSON validity, explanation supportedness. |
| 18 | LoRA/QLoRA Adaptation Roadmap | Next experimental phase planned: fine-tuning open LLMs after baseline benchmarks are confirmed. |
| 19 | XAI as Upstream Requirement | XAI established as active engineering constraint, not post-hoc analysis. |
| 20 | Quantization/QAT as Efficiency Study | Post-training quantization and QAT planned as future resource-efficiency research. |
| 21 | Public Academic Dissemination Boundary | Delineation of public vs. private research surface. |

---

## 5. Dataset Record Structure

A single valid semantic dataset record contains:

| Field | Description |
|---|---|
| `natural_language_request` | The input user prompt |
| `semantic_intent` | The identified engineering goal (e.g., `classify_bim_element`) |
| `bim_element` | Generic description of the physical component |
| `suggested_ifc_class` | buildingSMART IFC class (e.g., `IfcColumn`) |
| `expected_json_output` | The structured JSON payload with parsed details |
| `loi_table` | Level of Information Need properties required |
| `lod_conceptual_preview` | Simplified geometric description for illustration only |
| `evidence_trace` | Logical proof linking classification to input context |
| `validation_metadata` | Hashes, timestamps, quality grades, reviewer decisions |
| `limitations` | Explicit warnings on what cannot be verified |
| `quality_grade` | Grade A, B, or C |
| `split_assignment` | Target subset: train, validation, test, or eval_only |

---

## 6. Public Artifact Boundary

The public artifacts in this repository represent a strictly sanitized and demonstrative research surface:

- **Sanitized Dataset**: `sample20` uses generic, synthetic cases. No real building models, proprietary databases, or private corporate structures are exposed.
- **No Private Models**: The public harnesses run on lightweight, open-source base models or deterministic replay files. No private weights or custom adapters are published.
- **Research Orientation**: This repository demonstrates feasibility of the semantic contract and benchmark protocol. It does not provide certified commercial deliverables or professional engineering signatures.
