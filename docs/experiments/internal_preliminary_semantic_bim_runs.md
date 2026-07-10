# Internal preliminary semantic BIM experiments

## Status

This document summarizes internal preliminary experiments used to test whether the semantic BIM/IFC compilation protocol is technically measurable.

These experiments are internal preliminary experiments and are not final A1 benchmark results, trained model claims or production readiness evidence. They are feasibility evidence for the proposed benchmark workflow.

## Research task

The experiments evaluate a structured task:

```text
natural-language BIM request
+ structured BIM/runtime context
+ safety and evidence constraints
        ↓
IFC-aware semantic JSON record
        ↓
schema validation
        ↓
field-level comparison
        ↓
evidence and replay checks
```

The target is not a generic BIM chatbot. The target is a prompt-to-IFC contract model that can produce structured records suitable for validation and benchmark comparison.

## Smoke20 diagnostic run

The smoke20 run is a diagnostic smoke test. It demonstrates that the evaluation pipeline can validate JSON, schema conformance, IFC class mapping and evidence trace completeness, while also exposing weaknesses in intent classification, missing-field handling and Pset recall.

| Metric | Preliminary value |
| --- | ---: |
| processed_count | 20 |
| json_parse_success | 1.0 |
| schema_valid_rate | 1.0 |
| ifc_class_accuracy | 1.0 |
| semantic_type_accuracy | 1.0 |
| evidence_trace_completeness | 1.0 |
| intent_class_accuracy | 0.55 |
| missing_fields_accuracy | 0.85 |
| required_psets_recall | 0.866667 |
| relationship_recall | 1.0 |
| latency_average_ms | 9265.93 |

Interpretation: this smoke test should not be read as a performance claim. Its value is methodological: it confirms that the harness can both detect valid structured outputs and expose measurable failure modes.

## V4 5k preliminary run

A larger internal preliminary run was used to test the same protocol at a higher scale.

| Metric | Preliminary value |
| --- | ---: |
| processed_count | 5000 |
| json_parse_success | 1.0 |
| schema_valid_rate | 1.0 |
| ifc_class_accuracy | 1.0 |
| intent_class_accuracy | 1.0 |
| semantic_type_accuracy | 1.0 |
| evidence_trace_completeness | 1.0 |
| required_psets_recall | 0.90655 |
| relationship_recall | 0.9878 |
| missing_fields_accuracy | 0.9914 |
| latency_average_ms | 9126.94 |
| latency_median_ms | 8992.93 |
| latency_p95_ms | 11144.58 |

Interpretation: this run indicates that the protocol can be executed at larger preliminary scale. It does not replace a controlled public benchmark and should not be reported as a final A1 result.

## What these experiments demonstrate

The preliminary runs show that the proposed protocol can measure:

* JSON parse validity;
* schema conformance;
* IFC class selection;
* semantic type assignment;
* intent classification;
* required Pset recall;
* IFC relationship recall;
* missing-field handling;
* evidence trace completeness;
* latency.

## What these experiments do not claim

These runs do not claim that:

* it does not claim that a complete corpus already exists;
* it does not claim that the final A1 dataset has already been produced;
* it does not claim that the model is trained;
* it does not claim that an adapter is ready;
* it does not claim that the benchmark is final;
* it does not claim that the system is production ready;
* it does not claim that the repository is a certified BIM or regulatory checker.

## Relation to the proposed A1 work

The public repository currently provides a minimal reproducibility sample and replayable validation protocol. The A1 work is expected to scale this into a curated synthetic/controlled dataset, systematic benchmark, error analysis and lightweight adaptation experiment under documented computational conditions.
