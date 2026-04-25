# Implementation Runbook

## Purpose

Implement only the bounded CPU-first retrieval feasibility work needed to decide whether `PRO-C006` deserves rescue.

## Owner / Agent Type

Implementation agent.

## Input Artifacts

- `src/zpe_prosody/retrieval.py`
- `src/zpe_prosody/models.py`
- `src/zpe_prosody/codec.py`
- existing retrieval proof artifacts;
- validation runbook output.

## Procedure

1. Keep the existing 12-D cosine embedding available as baseline.
2. Add alternative retrieval implementations behind small, explicit functions or strategy objects:
   - normalized contour statistics;
   - voiced-mask-aware statistics;
   - temporal-shape/DTW distance;
   - binary or product-quantized contour codebook;
   - Hamming-distance retrieval.
3. Keep code decoupled:
   - no deep nesting;
   - no duplicated metric code;
   - dependency injection for retrieval scorer selection where useful.
4. Add focused tests:
   - baseline still works;
   - scorer handles empty/short contours;
   - binary/Hamming scorer is deterministic;
   - evaluation writes stable result schema.
5. Do not update README or commercial posture from implementation alone.

## Output Artifacts

- Code patch.
- Unit tests.
- Benchmark harness.
- Result JSON schema.

## Acceptance Gate

- `make test` passes.
- Baseline retrieval result remains reproducible.
- Alternative scorers produce deterministic outputs.
- Benchmark harness writes comparable p@5 metrics.

## Failure Mode

If implementation changes retrieval code without preserving the current failed baseline, the wave loses authority continuity and must be rejected.

## Resource Requirement

Mac CPU. No RunPod/GPU required.
