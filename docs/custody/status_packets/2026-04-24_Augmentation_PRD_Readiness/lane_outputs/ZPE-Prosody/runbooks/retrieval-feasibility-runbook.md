# Retrieval Feasibility Runbook

## Purpose

Adjudicate whether Prosody retrieval should be rescued, continued, or explicitly descoped.

## Owner / Agent Type

Experiment and verification agent pair.

## Input Artifacts

- Current `PRO-C006` failure analysis.
- Current retrieval implementation and baseline.
- New retrieval implementations from the implementation runbook.
- Corpus/license notes.
- HF custody manifest.

## Procedure

1. Freeze the protocol before running variants.
2. Run current baseline and record:
   - in-domain p@5;
   - OOD p@5;
   - sample count;
   - threshold;
   - command.
3. Run CPU variants:
   - normalized statistics;
   - temporal contour shape distance;
   - voiced-mask weighted scoring;
   - binary/product-quantized codebook plus Hamming retrieval.
4. Rank variants by in-domain p@5, OOD p@5, determinism, and implementation complexity.
5. Apply decision gates:
   - continue if in-domain p@5 >= 0.55 and OOD p@5 >= 0.35;
   - stop and descope if below those values;
   - pass only if in-domain p@5 >= 0.80 and OOD p@5 >= 0.65.
6. If continuing, propose a second wave:
   - CPU ANN such as RaBitQ/SOAR;
   - external embeddings only with explicit model/corpus custody.

## Output Artifacts

- Retrieval feasibility table.
- Variant result JSONs.
- Go/descope verdict.
- Updated failure analysis if no pass.

## Acceptance Gate

The pass gate is the accepted authority gate: in-domain `p@5 >= 0.80` and OOD `p@5 >= 0.65`. Intermediate lift only authorizes continued research; it does not authorize a public pass.

## Failure Mode

The main failure mode is converting intermediate lift into a pass narrative. Do not do that.

## Resource Requirement

Mac CPU first. CPU pod optional for repeated sweeps. GPU only after CPU feasibility justifies learned retrieval.
