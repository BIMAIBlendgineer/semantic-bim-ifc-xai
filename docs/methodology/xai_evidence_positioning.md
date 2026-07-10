# XAI evidence positioning

## Scope

This repository uses XAI in an evidence-oriented sense.

It does not claim full mathematical interpretability, model-internal explanation or SHAP/LIME-style feature attribution.

## Operational meaning

An output is considered more explainable when it exposes:

- the selected IFC class or candidate classes;
- the Psets and relationships required;
- missing or ambiguous information;
- confidence and reason codes;
- evidence trace entries;
- validation and replay status.

## Evaluation direction

Future benchmark work should evaluate explanation quality through criteria such as:

- evidence completeness;
- evidence relevance;
- schema-grounded consistency;
- field-level faithfulness;
- missing-information detection;
- replay reproducibility.

This keeps the explainability claim bounded, auditable and compatible with BIM/IFC validation.
