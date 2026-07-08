# Evidence-Trace Position

## Statement of Position

Explainability in this research is not an afterthought, a post-hoc visualization tool, or a secondary analysis layer applied to a finished model. It is treated as an evidence-trace requirement across dataset design, validation, and evaluation.

---

## 1. Evidence Trace as an Upstream Requirement

At the dataset construction stage, every record must contain an explicit `evidence_trace` field. This field must reference the specific properties, entity relationships, or contextual cues that justified the classification or property assignment.

A model cannot be rewarded for producing a correct IFC class assignment without demonstrating why that class was selected. This means:

- The dataset enforces explainability before the model ever sees the training data.
- Models trained on this dataset are exposed, from the earliest learning signal, to the requirement that outputs must be grounded in traceable evidence.
- Records lacking a valid evidence trace fail Gate 5 of the validation matrix and are blocked from ingestion.

This is in contrast to approaches that apply attribution retrospectively. Post-hoc attribution can describe a model's behavior, but cannot correct a model that was never trained to explain itself.

---

## 2. Evidence Trace as a Parallel Validation Requirement

The validation gate matrix (see [validation_gates.md](validation_gates.md)) evaluates explanation quality alongside structural accuracy at every record.

This means:

- The evidence trace must correspond to the actual input context.
- The selected IFC class and property set must be supported by the trace.
- Unsupported or hallucinated rationale fails validation.

---

## 3. Evidence Trace as a Downstream Benchmark Criterion

The benchmark protocol measures whether the output is not only structurally valid, but also supported by a trace that a reviewer can inspect.

The benchmark is intentionally limited. It is a public sample validation protocol, not a final production benchmark.

---

## 4. What This Does Not Mean

- **Evidence trace is not a completed formal attribution system**: The current public harness demonstrates structured replay and validation, but it does not implement mathematical attribution methods such as SHAP or LIME in the public sample.
- **Evidence trace is not the mechanism of certification**: The explanation quality depends on the evidence trace, the record schema, and the validation gates.
- **Evidence trace is not a certification claim**: The research does not claim to certify any BIM/IFC deliverable, tool, or dataset.

---

## 5. LoRA/QLoRA and Evidence Trace

Any future adaptation work must preserve the evidence-trace contract.

This sequencing ensures that evidence-trace requirements are embedded in the training pipeline rather than added after the fact.

---

## 6. QAT / Post-Training Quantization and Evidence Trace

Quantization is a deployment-efficiency topic, not the explanation mechanism. If compressed models are studied later, they must still preserve the public evidence-trace contract.

---

## 7. Future Research Directions

| Topic | Direction |
| --- | --- |
| SHAP/LIME attribution | Future post-hoc attribution research over live fine-tuned model outputs |
| Counterfactual explanation | Future prompt perturbation studies |
| Human evaluation | Future review by domain experts |
