# Semantic XAIBIM

Semantic XAIBIM is an open research toolkit for Semantic BIM/IFC, prompt-to-structure tasks, explainable AI outputs, and reproducible benchmark evidence.

The repository is intended for researchers, BIM engineers, information managers, and AECO professionals interested in semantic interpretation of BIM/IFC information using structured and auditable AI workflows.

## Scope

This repository focuses on:

- Semantic BIM/IFC research.
- Prompt BIM semantic tasks.
- Structured AI outputs.
- IFC grounding.
- Explainability and traceability.
- Public benchmark seeds.
- Replayable evidence.
- Lightweight validation harnesses.

## What this repository is not

This repository is not:

- A certified BIM compliance product.
- A normative certification tool.
- A deployment-ready commercial system.
- A full training workspace.
- A repository of private BIM models.
- A repository of raw model adapters or internal experiment logs.


## Live demo

A public replay demo is available on Hugging Face Spaces:

- Space: https://huggingface.co/spaces/bimaiblend/semantic-xaibim-replay
- Direct app: https://bimaiblend-semantic-xaibim-replay.hf.space

The demo loads the reduced public JSONL sample and displays prompt payloads, canonical outputs, parsed outputs and validation metadata. It does not run model inference.

## Public evidence

The initial public evidence package includes:

- A reduced public sample of 20 semantic BIM predictions.
- Aggregated smoke20 metrics.
- A public research summary.
- A normative text audit summary.
- A replay harness for validating public examples.
- A schema validator for structured outputs.

## Quick start

Validate the public example file:

    python harness/schema_validator.py examples/sample20_public_predictions.jsonl

Replay public examples:

    python harness/replay_harness.py examples/sample20_public_predictions.jsonl

## Repository map

- docs: conceptual documentation for Semantic BIM/IFC.
- research: preliminary public research evidence and publication policy.
- benchmark: metrics, schema and benchmark documentation.
- examples: public sample prompts and outputs.
- harness: replay and validation scripts.
- demo: plans for Hugging Face Space and Vercel landing page.

## Public status

Current public evidence status:

    RESEARCH_PASS

This means preliminary research evidence. It does not imply product readiness, certification, or deployment approval.

