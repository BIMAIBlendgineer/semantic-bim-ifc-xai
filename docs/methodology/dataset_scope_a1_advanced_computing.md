# Dataset scope for A1-style advanced computing work

## Public sample

The public `sample20` dataset is a minimal reproducibility sample.

It demonstrates:

- record structure;
- schema validation;
- replay;
- public evidence boundary;
- safe publication format.

It is not a complete corpus.

## Proposed larger dataset

The larger dataset is an objective of the advanced computing work.

The intended dataset is synthetic/controlled and curated. It should support:

- dataset generation;
- normalization;
- deduplication;
- split definition;
- validation;
- benchmark execution;
- error analysis;
- lightweight adaptation experiments.

## Experimental order

The work should proceed in this order:

1. define the semantic BIM/IFC contract;
2. generate and curate the synthetic/controlled dataset;
3. validate schema, leakage, deduplication and coverage;
4. execute baseline model benchmarks;
5. analyze errors;
6. test lightweight LoRA/QLoRA adaptation only after dataset and benchmark validation;
7. compare before/after results.

## Boundary

The dataset work does not claim that a complete training corpus already exists. The public sample and preliminary internal experiments are starting evidence for a controlled research workflow.
