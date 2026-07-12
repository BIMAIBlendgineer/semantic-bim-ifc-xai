# Dataset scope and compute scaling

## Public sample

The public `sample20` dataset is a minimal reproducibility sample.

It demonstrates:

- record structure;
- schema validation;
- replay;
- public evidence boundary;
- safe publication format.

It is not a complete corpus.

## Private controlled pilot dataset

A private controlled synthetic pilot dataset of 1,000 records was used in a
preliminary QLoRA feasibility experiment.

The dataset is **not publicly released**. Only aggregate metrics, hashes, and
compute measurements derived from it are published in
[`benchmark/qlora/`](../../benchmark/qlora/).

The pilot dataset was used to:

- validate the dataset preparation and split construction pipeline;
- calibrate GPU resource consumption;
- measure controlled held-out target agreement;
- confirm the training workflow is executable end-to-end.

## Preliminary QLoRA experiment

A preliminary QLoRA fine-tuning experiment was executed on Kaggle
GPU infrastructure using the private pilot dataset.

Public notebook: <https://www.kaggle.com/code/xaibim/semantic-bim-ifc-xai>

The experiment measured:

- training runtime and end-to-end runtime;
- peak VRAM consumption;
- effective and allocated GPU-hours;
- controlled held-out target agreement before and after fine-tuning.

The result is **preliminary and bounded**:

- single run, single seed, one epoch;
- seven held-out semantic families;
- four IFC classes in the test split;
- no broad AECO generalization established;
- no production readiness claimed.

## Compute scaling

The pilot used 1,000 records and one epoch on a single Tesla T4.

Effective GPU-hours measured: ≈ 2.11 h (1 effective GPU).
Allocated GPU-hours measured: ≈ 4.22 h (2 allocated GPUs).

These figures are calibration data points for future resource planning.
They are not universal efficiency guarantees.

## Experimental order

The work proceeds in this order:

1. define the semantic BIM/IFC contract;
2. generate and curate the synthetic/controlled dataset;
3. validate schema, leakage, deduplication and coverage;
4. execute baseline model evaluations;
5. analyse errors;
6. test lightweight LoRA/QLoRA adaptation after dataset and evaluation validation;
7. compare before/after results.

## Boundary

A systematic benchmark at larger scale and a broader public dataset remain
future work. The public sample and preliminary internal experiments are
starting evidence for a controlled research workflow, not a replacement for
broader scientific validation.
