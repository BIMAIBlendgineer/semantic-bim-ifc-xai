# XAI Roadmap for Semantic AI in BIM/IFC

This roadmap outlines the evolution of the Semantic AI research harness toward a formal Explainable AI (XAI) framework for digital construction and engineering schemas.

---

## What exists today

The current version of the public harness provides structured traceability and syntactic verification:
- **Canonical Output**: Structured representation of mapped parameters.
- **Validation Blocks**: Checks mapping outputs against baseline schemas.
- **Metadata Trace**: Logs execution parameters (e.g. latency, source split, risk level).
- **Replay Mechanism**: Deterministic retrieval of records to inspect classification logs.
- **Evidence-like fields**: Basic parameters indicating recovery types and ambiguity contexts.

> [!WARNING]
> **Not Full XAI**: These capabilities represent metadata logging and rule-based validation. They do **not** constitute a complete Explainable AI framework.

---

## Why it is not full XAI yet

To achieve complete explainability, the system must bridge the gap between model weights and engineering intent. The following elements are not yet implemented in the repository:
- **No Local interpreters (e.g. SHAP, LIME)**: No mathematical attribution highlighting which words in the prompt led to specific parameter choices.
- **No Counterfactual explanation**: No mechanism to compute what change in the prompt would change the output classification.
- **No Causal explanation**: The system cannot mathematically trace the causal chain of decisions.
- **No Formal explanation benchmarks**: No metric evaluates how understandable, faithful, or accurate the explanations are.
- **No Systematic human evaluation**: There is no built-in feedback loop for professional engineers to audit and correct explanations.

---

## What XAI will mean in this research

Within this research, **Explainable AI (XAI)** is defined as the capability to explain, with technical and auditable evidence, *why* a natural-language engineering request was parsed and transformed into a specific BIM/IFC entity or property set. 

An explanation must satisfy both computer science rigor (faithfulness) and civil engineering utility (correctness).

---

## Future Research Modules

The roadmap targets seven development modules to achieve formal XAI:

### 1. Explanation Trace
- **Objective**: Capture step-by-step reasoning behind classifications.
- **Implementation**: Train models to output textual, step-by-step arguments (Chain-of-Thought) before declaring the final JSON mapping.

### 2. Evidence Mapping
- **Objective**: Map specific output parameters back to input prompt segments.
- **Implementation**: Create token alignment matrices mapping parameter suggestions (e.g. `reinforced concrete`) directly to the source prompt tokens.

### 3. Uncertainty and Alternatives
- **Objective**: Expose alternative classifications and confidence.
- **Implementation**: Output probability tables showing candidate classifications (e.g. `IfcWall: 70%`, `IfcColumn: 20%`) and flag missing details.

### 4. Counterfactual BIM Prompts
- **Objective**: Allow interactive "what-if" testing.
- **Implementation**: Build interactive tools showing what changes would alter the classification.
  - *Example*: *"What would change if this element were a beam instead of a column?"* (Modifying the prompt keywords to see where the decision boundary shifts).

### 5. Human Engineering Review
- **Objective**: Integrate a professional review loop.
- **Implementation**: Build interfaces for licensed engineers to review, correct, or reject suggestions and explanations, feeding corrections back into training.

### 6. Explanation Quality Metrics
- **Objective**: Quantify explanation effectiveness.
- **Implementation**: Develop scoring formulas measuring:
  - **Utility**: Relevance to the engineer.
  - **Fidelity**: How well the explanation matches the actual model logic.
  - **Completeness**: Whether all decisions are justified.
  - **Clarity**: Readability of the explanation.
  - **Technical correctness**: Adherence to IFC specifications.
  - **Knowledge boundaries**: Expressing what the AI *does not* know.

### 7. Optional Model Attribution Layer
- **Objective**: Mathematical feature attribution.
- **Implementation**: Integrate attribution libraries (such as SHAP or LIME) to calculate token importance scores once a live model server is deployed.
