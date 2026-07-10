# Semantic BIM compilation task

## Definition

The semantic BIM compilation task converts a natural-language AECO/BIM request into a structured IFC-aware semantic record.

The objective is not to generate a pleasant free-text answer first. The objective is to produce a machine-checkable contract that can be validated, replayed and compared.

In practical terms, this is a prompt-to-IFC contract.

## Input

Typical input includes:

- a human BIM request;
- structured BIM or runtime context;
- IFC-related constraints;
- safety constraints;
- evidence requirements.

## Output

The output is a structured semantic record containing fields such as:

- intent class;
- semantic type;
- IFC class;
- IFC candidates;
- normalized dimensions;
- material;
- required Psets;
- required relationships;
- missing information;
- ambiguity flags;
- recovery needs;
- confidence;
- reason codes;
- evidence trace.

## User-facing answer

The chat-style answer is a presentation layer. It should be derived from the structured contract, not replace it.

A practical user-facing response can be organized into:

1. Modeling IFC / 3D intent;
2. Information, Pset, class and property mapping;
3. Building AECO answer.

This keeps the interface understandable for users while preserving a benchmarkable machine contract.
