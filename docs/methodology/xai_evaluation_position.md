# XAI Evaluation Position

## Statement of Position

Explainable Artificial Intelligence (XAI) in this research is not an
afterthought, a post-hoc visualization tool, or a secondary analysis layer
applied to a finished model. It is treated as an **upstream, parallel, and
downstream research requirement** governing every stage of dataset design,
validation, and evaluation.

---

## 1. XAI as an Upstream Requirement

At the dataset construction stage, every record must contain an explicit
`evidence_trace` field. This field must reference the specific properties,
entity relationships, or contextual cues that justified the AI's
classification or property assignment.

A model cannot be rewarded for producing a correct IFC class assignment without
demonstrating *why* that class was selected. This means:

- The dataset enforces explainability before the model ever sees the training
  data.
- Models trained on this dataset are exposed, from the earliest learning signal,
  to the requirement that outputs must be grounded in traceable evidence.
- Records lacking a valid evidence trace fail Gate 5 of the validation matrix
  and are blocked from ingestion.

This is in contrast to approaches that apply XAI retrospectively (e.g., SHAP or
LIME applied to a model trained without any explanation-awareness). Post-hoc
attribution can describe a model's behavior, but cannot correct a model that
was never trained to explain itself.

---

## 2. XAI as a Parallel Validation Requirement

The validation gate matrix (see [validation_gates.md](validation_gates.md))
evaluates explanation quality alongside structural accuracy at every record
review:

- **Gate 5 (Evidence Trace Completeness)**: Confirms that the justification
  provided is anchored in the input context.
- **Gate 6 (Hallucination / Unsupported Claim Scan)**: Confirms that no claim is
  made without corresponding support in the input context or canonical
  catalogue.

These gates run in parallel with schema validation (Gate 2), IFC class
validation (Gate 3), and LOI consistency (Gate 4). A record that produces a
structructurally perfect JSON output but provides no evidence for its IFC
class is blocked — the structural accuracy does not compensate for the
explanation failure.

---

## 3. XAI as a Downstream Benchmark Criterion

The formal benchmark evaluation protocol scores model outputs on multiple
dimensions. Explanation quality is a first-class metric, not a secondary
observation:

| Metric | Description |
|---|---|
| Intent Accuracy | Does the model correctly identify the engineering intent? |
| Slot F1 | Does the model correctly extract all required property slots? |
| IFC Class Accuracy | Does the model assign the correct IFC class? |
| JSON Validity | Is the output schema-compliant? |
| Evidence Supportedness | Are all classification claims supported by explicit input context references? |
| Explanation Completeness | Does the model explain the selected class, the used evidence, any missing information, and plausible alternatives? |

A model that achieves high IFC Class Accuracy but low Evidence Supportedness
scores poorly overall. The evaluation treats unexplained correctness as
insufficient for engineering deployment contexts.

---

## 4. What XAI Does Not Mean in This Research

> [!IMPORTANT]
> The following clarifications are essential to avoid misrepresenting the
> research scope:

- **XAI is not a completed formal system**: The current public harness
  demonstrates the evidence-trace contract and validation logic. Full
  mathematical attribution (SHAP, LIME, integrated gradients over live model
  outputs) is a future research phase, planned after fine-tuned models are
  available for evaluation.
- **XAI is not the mechanism of explanation**: The explanation quality depends
  on the dataset design and the model's training signal. Quantization and QAT
  (Quantization-Aware Training) are downstream efficiency studies — they
  preserve explanation quality, but they do not generate it.
- **XAI is not a certification**: The research does not claim to certify any
  model as "explainable" in a legal or regulatory sense. It establishes a
  research methodology for measuring explanation quality in BIM/IFC semantic
  interpretation contexts.

---

## 5. LoRA/QLoRA and XAI Relationship

LoRA (Low-Rank Adaptation) and QLoRA (Quantization-Aware Low-Rank Adaptation)
are tools for efficient model fine-tuning. In our methodology:

- LoRA/QLoRA will be applied **after** dataset schema validity is confirmed and
  **after** benchmark baselines establish what a non-fine-tuned model achieves
  on the evaluation metrics.
- The adaptation experiments will test whether fine-tuning on the structured,
  evidence-traced dataset improves the model's adherence to schema formatting
  and explanation completeness — not whether it improves accuracy alone.
- This sequencing ensures that XAI requirements are embedded in the training
  signal before any optimization step is applied.

---

## 6. QAT / Post-Training Quantization and XAI

Quantization-Aware Training (QAT) and post-training quantization are planned
as future research phases focused on resource efficiency:

- The research question for QAT is: *Does quantization preserve the model's
  explanation quality and structural accuracy, or does compression degrade the
  evidence-tracing capability?*
- QAT is a downstream step, applied only after a model has been fine-tuned and
  evaluated with full precision.
- It is explicitly not the mechanism by which the model generates explanations.

---

## 7. Future XAI Research Directions

| Direction | Description |
|---|---|
| SHAP/LIME attribution | Post-hoc attribution over live fine-tuned model outputs |
| Counterfactual explanations | Generating alternative IFC class candidates with contrastive evidence |
| Attention-based grounding | Mapping input token attention to output IFC class decisions |
| Human evaluation protocol | Expert civil engineer review of explanation plausibility |
| Cross-dataset benchmark | Evaluation of explanation quality across multiple BIM domain datasets |
