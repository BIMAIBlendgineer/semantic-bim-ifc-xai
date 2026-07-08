# Evidence-Trace Roadmap for Semantic AI in BIM/IFC

This roadmap outlines the evolution of the Semantic AI research harness toward stronger evidence traceability for digital construction and engineering schemas.

---

## What exists today

The current version of the public harness provides structured traceability and syntactic verification:

- **Canonical Output**: Structured representation of mapped parameters.
- **Validation Blocks**: Checks mapping outputs against baseline schemas.
- **Metadata Trace**: Logs execution parameters such as latency, source split, and risk level.
- **Replay Mechanism**: Deterministic retrieval of records to inspect classification logs.
- **Evidence-like fields**: Basic parameters indicating recovery types and ambiguity contexts.

> [!WARNING]
> **Not Full Attribution**: These capabilities represent metadata logging and rule-based validation. They do **not** constitute a complete mathematical attribution framework.

---

## Why it is not full attribution yet

To achieve complete explainability, the system must bridge the gap between model weights and engineering intent. The following elements are not yet implemented in the repository:

- **No local interpreters**: No mathematical attribution highlighting which words in the prompt led to specific parameter choices.
- **No counterfactual explanation**: No mechanism to compute what change in the prompt would change the output classification.
- **No causal explanation**: The system cannot mathematically trace the causal chain of decisions.
- **No formal explanation benchmarks**: No metric evaluates how understandable, faithful, or accurate the explanations are.
- **No systematic human evaluation**: There is no built-in feedback loop for professional engineers to audit and correct explanations.

---

## What explainability means in this research

Within this research, explainability is defined as the capability to explain, with technical and auditable evidence, why a natural-language engineering request was parsed and transformed into a specific BIM/IFC entity or property set.

An explanation must satisfy both computer science rigor and civil engineering utility.

---

## Future Research Modules
