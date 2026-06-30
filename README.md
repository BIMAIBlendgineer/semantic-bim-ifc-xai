# Semantic BIM/IFC XAI Research Harness

A public academic research artifact for studying how natural-language civil
engineering requests can be mapped to structured BIM/IFC semantic records,
validation gates, evidence traces, and future explainable AI evaluation
workflows.

> [!IMPORTANT]
> **Research Disclaimer**: This repository is a public academic artifact. It
> is intentionally separated from any commercial ecosystem components. It is
> not a product, certification system, university service, or institutional
> endorsement. Claims about XAI completeness are methodological and
> forward-looking, not certified deliverables.

---

## 1. Purpose

This repository supports open research into the automated semantic
interpretation of Building Information Modeling (BIM) data using the Industry
Foundation Classes (IFC) schema. The central research question is:

> **How can AI models interpret civil engineering requests expressed in natural
> language, map them to IFC-compliant structured records, and justify those
> mappings with auditable, traceable evidence?**

The repository provides a sanitized dataset sample, a replay validation
harness, an interactive public harness, and the academic methodology
documents that govern the research boundary.

---

## 2. Research Scope

This research operates at the intersection of:

- **BIM/IFC Semantic Interpretation**: Mapping unstructured natural language
  engineering requests to standardized IFC entity classes, property sets, and
  information requirements.
- **Structured Output Contracts**: Producing JSON/JSONL records that enforce
  schema compliance, provenance, and evidence tracing.
- **Validation Gates**: Multi-stage automated checks to ensure each record is
  schema-valid, evidence-supported, and free of unsupported claims.
- **Explainable AI (XAI) as a Research Constraint**: Treating explanation as an
  upstream dataset requirement rather than a post-hoc visualization layer.
- **LoRA/QLoRA Adaptation Roadmap**: Planning lightweight model fine-tuning
  after dataset validity and baseline benchmarks are established.

---

## 3. What This Repository Provides

| Artifact | Description |
|---|---|
| `sample20/` | 20 sanitized, synthetic BIM/IFC semantic records for reproducible evaluation |
| `harness/` | Python replay harness for deterministic validation of sample records |
| `spaces/huggingface_harness/` | Interactive Hugging Face Space harness code |
| `benchmark/` | Benchmark protocol definitions (intent accuracy, slot F1, IFC class, JSON validity) |
| `docs/methodology/` | Academic methodology documents (dataset construction, validation gates, XAI position) |
| `docs/literature/` | IEEE bibliography of relevant state-of-the-art publications |
| `docs/public_boundary.md` | Explicit public/private research boundary definition |

---

## 4. What This Repository Does Not Claim

- It does **not** generate certified IFC geometry or produce professional BIM
  authoring deliverables.
- It does **not** host active large language models. All current matching is
  deterministic against the sanitized sample dataset.
- It does **not** provide a formally complete XAI system. XAI is treated as a
  methodological requirement and evaluation criterion; full attribution (e.g.,
  SHAP/LIME over live model outputs) is a future research phase.
- It does **not** contain private training data, proprietary model weights, or
  adapter checkpoints.
- It does **not** represent an institutional endorsement from any university,
  research centre, or funding body.

---

## 5. Semantic BIM/IFC Record Concept

In this research, a **semantic record** is a structured, schema-validated
document that encodes:

- **Engineering Intent**: The precise technical objective expressed in the
  natural language request (e.g., `classify_bim_element`, `extract_properties`).
- **IFC Class Candidate**: The target entity within the buildingSMART IFC schema
  hierarchy (e.g., `IfcColumn`, `IfcWall`, `IfcSlab`).
- **Level of Information (LOI)**: The alphanumeric metadata fields required for
  the element (material, fire rating, load-bearing status, etc.).
- **Level of Development (LOD)**: Conceptual geometric metadata for
  illustration only; no certified geometry is generated.
- **Evidence Trace**: The explicit justification linking the classification to
  properties or entities in the input context.
- **Validation State**: Audit metadata including schema compliance, sanitization
  status, and split assignment.

### Semantic Flow Diagram

```mermaid
flowchart LR
    A[Natural-language engineering request] --> B[Semantic parsing]
    B --> C[Engineering intent]
    C --> D[IFC candidate class]
    D --> E[LOI / LOD interpretation]
    E --> F[Structured JSON record]
    F --> G[Validation gates]
    G --> H[Evidence trace]
    H --> I[Future XAI evaluation]

    style A fill:#1e293b,stroke:#334155,color:#fff
    style B fill:#3b82f6,stroke:#1d4ed8,color:#fff
    style F fill:#0f766e,stroke:#115e59,color:#fff
    style G fill:#d97706,stroke:#b45309,color:#fff
    style I fill:#16a34a,stroke:#15803d,color:#fff
```

### Example Record (Simplified)

- **Natural language request**: *"I need a reinforced concrete column with IFC
  classification and LOI information."*
- **Engineering intent**: `classify_bim_element`
- **IFC class candidate**: `IfcColumn`
- **Material candidate**: Reinforced concrete
- **LOI fields**: `LoadBearing`, `Material`, `FireRating`, `CrossSectionArea`
- **LOD**: Conceptual bounding box preview only
- **Structured output**: JSON contract with all above fields and evidence
- **Validation**: Automated schema check against required minimum fields
- **Evidence**: Textual trace identifying which input terms triggered the
  classification

---

## 6. Dataset Construction Methodology

The dataset was constructed through a multi-phase pipeline rejecting plain
instruction-output pairs in favour of structured, schema-validated contracts.
Key methodological decisions include:

- **Rejection of plain text training**: Standard LLM fine-tuning on raw
  instruction-output pairs was rejected due to lack of schema enforcement,
  hallucination of catalogue entries, and absence of auditable grounding.
- **Runtime payload design**: Each record is built around a structured payload
  encapsulating the input prompt, the active schema, and the target catalogues.
- **Internal milestones (S18 / S19 / S20)**: Successive pipeline iterations
  improving validation rigor, catalogue mapping, and blocked-by-prerequisite
  gate enforcement.
- **Fail-closed gate**: Any dataset candidate lacking clear provenance,
  anonymization, or manual review decision is blocked from ingestion.

For the full academic history of dataset construction phases, see
[docs/methodology/dataset_construction_and_training_readiness.md](docs/methodology/dataset_construction_and_training_readiness.md).

---

## 7. Public Sanitized Sample

The `sample20` dataset contains 20 representative, fully sanitized records:

- No real-world building models, proprietary databases, or private corporate
  identifiers.
- All project-specific GlobalIds replaced with synthetic alternatives.
- All records pass the full validation gate matrix before publication.
- Intended for reproducibility, peer review, and benchmark protocol
  demonstration.

Private datasets (private pilot dataset, private high-fidelity internal dataset)
remain within the private research environment and are not published here.

---

## 8. Replay and Guided Harness

### Replay Harness

The replay harness (`harness/`) provides deterministic validation:

```bash
python harness/replay.py --sample sample20/
```

This checks that each record in `sample20` produces a consistent, schema-valid
output when the canonical pipeline is replayed.

### Interactive Hugging Face Spaces

| Space | Purpose |
|---|---|
| [semantic-xaibim-replay](https://huggingface.co/spaces/bimaiblend/semantic-xaibim-replay) | Browse and replay the 20 sanitized records |
| [semantic-xaibim-harness](https://huggingface.co/spaces/bimaiblend/semantic-xaibim-harness) | Interactive semantic matching, JSON validation, and evidence preview |

---

## 9. Validation Gates

Records are accepted into the dataset only after passing an 11-stage validation
matrix:

1. JSON syntax parse
2. Schema validation (Pydantic contract)
3. IFC class candidate validation (buildingSMART registry)
4. LOI/LOD consistency check
5. Evidence trace completeness
6. Hallucination / unsupported claim scan
7. Replay validation (deterministic re-execution)
8. Leakage and deduplication check
9. Sanitization scan (NER and regex)
10. Forbidden patterns scan (credentials, paths, private model tags)
11. Public/private boundary verification

See [docs/methodology/validation_gates.md](docs/methodology/validation_gates.md)
for full specification.

---

## 10. XAI Position

Explainable AI (XAI) is treated as an **upstream dataset and evaluation
requirement**, not a post-hoc visualization layer:

- **Upstream**: Dataset records must contain explicit evidence traces. A model
  cannot be rewarded for generating a correct IFC class without justifying
  *why* that class was selected.
- **Parallel**: Validation gates inspect explanation quality and truthfulness
  alongside structural accuracy of JSON output.
- **Downstream (benchmark)**: The evaluation protocol penalizes models that
  produce correct classifications without valid, context-supported rationales.

> [!NOTE]
> Full mathematical XAI attribution (e.g., SHAP, LIME over live model outputs)
> is a future research phase. The current public harness demonstrates the
> evidence-trace contract and validation logic, not a completed formal XAI
> system.

See [docs/methodology/xai_evaluation_position.md](docs/methodology/xai_evaluation_position.md)
for the full methodological statement.

---

## 11. LoRA/QLoRA and Quantization Roadmap

Model adaptation and compression are explicitly separated from dataset design:

- **LoRA/QLoRA**: Lightweight fine-tuning will be studied after dataset schema
  validity is confirmed and benchmark baselines establish what a non-fine-tuned
  model achieves on the evaluation metrics. No adapter checkpoints are
  published in this repository.
- **QAT / Post-Training Quantization**: A future research phase to study
  whether compressed models preserve semantic accuracy and explanation quality.
  Quantization is a resource-efficiency study, not the source of the
  explanation mechanism.

---

## 12. Public/Private Boundary

This repository represents a strictly sanitized public surface:

| Publicly available | Privately maintained |
|---|---|
| `sample20` (20 synthetic records) | private pilot dataset |
| Replay and harness code | Production inference infrastructure |
| Benchmark protocol definition | Fine-tuned adapter weights |
| IEEE bibliography | private high-fidelity internal dataset |
| Methodology documents | private commercial or project data |

See [docs/public_boundary.md](docs/public_boundary.md) for the full boundary
definition.

---

## 13. Repository Structure

```
semantic-bim-ifc-xai/
├── README.md                          # This document
├── CITATION.cff                       # Academic citation metadata
├── CONTRIBUTING.md                    # Contribution guidelines
├── LICENSE                            # Repository license
├── PUBLIC_EVIDENCE.md                 # Public evidence summary
├── sample20/                          # 20 sanitized semantic records (JSONL)
├── harness/                           # Replay validation harness
├── benchmark/                         # Benchmark protocol definitions
├── spaces/
│   └── huggingface_harness/           # Hugging Face Space application code
├── demo/                              # Standalone demo utilities
├── examples/                          # Usage examples
├── research/                          # Supporting research materials
└── docs/
    ├── methodology/
    │   ├── dataset_construction_and_training_readiness.md
    │   ├── validation_gates.md
    │   └── xai_evaluation_position.md
    ├── literature/
    │   └── semantic_bim_ifc_bibliography_ieee.md
    └── public_boundary.md
```

---

## 14. Citation

If you use this repository in academic work, please cite it using the metadata
in [CITATION.cff](CITATION.cff).

---

## 15. License

See [LICENSE](LICENSE) for terms. This repository contains no proprietary data,
no production model weights, and no private client information.

---

The long-term research goal is not to replace engineers, but to study how AI
systems can make BIM/IFC interpretation more explicit, auditable, and
explainable.
