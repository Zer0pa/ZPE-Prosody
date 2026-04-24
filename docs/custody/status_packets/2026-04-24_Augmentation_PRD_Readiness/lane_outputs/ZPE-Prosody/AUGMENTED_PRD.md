# ZPE-Prosody Augmented PRD

Date: 2026-04-24
Lane: ZPE-Prosody
Local repo: `/Users/Zer0pa/ZPE/ZPE Prosody/ZPE-Prosody`

## Lane Objective

Prepare ZPE-Prosody for a bounded augmentation wave that answers one governing question:

Can the failed retrieval surface be materially rescued with a CPU-first method, or should the lane explicitly narrow to deterministic prosodic feature encoding infrastructure?

The objective is not to polish the existing codec story. Compression, F0 fidelity, determinism, and tests are already real. The commercial blocker is retrieval. The augmentation wave must either improve retrieval against the accepted gate or produce a proof-backed descope decision.

## Current Authority Surface

Current accepted evidence:

| Surface | Current value | Authority |
|---|---:|---|
| Compression | 16.5952x | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/before_after_metrics.json` |
| F0 RMSE | 0.8925% | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/before_after_metrics.json` |
| Energy RMSE | 2.0780% | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/before_after_metrics.json` |
| Quality score | 47/50 | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/quality_gate_scorecard.json` |
| Retrieval p@5 | 0.3067 vs 0.80 gate | `proofs/artifacts/c006_retrieval_failure_analysis.md` |
| OOD retrieval p@5 | 0.1707 vs 0.65 gate | `proofs/artifacts/c006_retrieval_failure_analysis.md` |
| LibriSpeech real-speech compression | 13.012x on 100 utterances | `proofs/artifacts/librispeech_benchmark/README.md` |
| LibriSpeech F0 RMSE | 0.6367% mean | `proofs/artifacts/librispeech_benchmark/f0_fidelity.json` |

Current public verdict remains `FAIL`. The current retrieval code is a 12-D contour-statistics embedding with cosine similarity in `src/zpe_prosody/retrieval.py`.

## Sovereign Acceptance Gate

The sovereign commercial gate is retrieval if retrieval remains in the wedge:

- In-domain emotional-speech retrieval must reach `p@5 >= 0.80`.
- OOD retrieval stress must reach `p@5 >= 0.65`.
- Codec metrics, green unit tests, and clean packaging do not substitute for this gate.

If the augmentation wave descopes generic retrieval, the PRD must create a new, narrower authority surface before any public posture change:

- deterministic packet/replay mechanics remain promoted;
- generic retrieval remains explicitly failed;
- new narrowed metrics must be measured before they are claimed.

## Blockers And Kill Conditions

Blockers:

- `PRO-C006` retrieval is a real performance failure, not a missing environment issue.
- Current branch state has local Git stashes that require a later GitHub decision.
- No active `.gpd/ROADMAP.md` or `.gpd/STATE.md` exists in the repo, so execution must use a GPD-ready manual phase plan unless GPD structure is installed later.
- PR #27 remains a conflicting doc-reorientation PR and should not be blindly rebased into execution.

Kill conditions:

- If a CPU binary-codebook or contour-temporal rescue cannot move in-domain `p@5` above `0.55` and OOD `p@5` above `0.35` on the same authority protocol, stop generic retrieval rescue and narrow the lane.
- If CPU rescue reaches intermediate lift but cannot pass `p@5 >= 0.80` in-domain and `p@5 >= 0.65` OOD after the second comparator wave, stop claiming retrieval as a commercial blocker to be actively rescued.
- If any proposed learned/GPU method requires new corpora or model weights without HF custody and a reproducible proof harness, do not start it.
- If public docs would need to hide the failed retrieval metric to look coherent, the doc change is rejected.

## Augmentation Research Synthesis

The shared research offers three competing Prosody directions:

1. Narrow to streaming prosody-aware codec infrastructure.
   - Claude argues the generic p@5 retrieval gate is stale relative to speech tokenization systems such as Mimi, FACodec, WavTokenizer, and speech-text token models.
   - Strong narrowed direction: streaming prosody codec plus emotion/SER retrieval as a service metric, not the sovereign commercial gate.

2. Try a CPU-first discrete retrieval rescue.
   - Perplexity argues FocalCodec-style binary/discrete codebooks may repair continuous embedding fragmentation.
   - This maps cleanly to Mac CPU work: product quantization or binary codebooks over F0/energy/duration/voiced-mask streams, Hamming retrieval, and exact p@5 comparison.

3. Narrow toward articulatory/physics infrastructure.
   - Gemini argues for deterministic articulatory encoding: map stable F0/prosody features into interpretable vocal-tract or style-control parameters.
   - This has grant value but does not rescue the current commercial retrieval gate.

Synthesis decision:

Run one bounded CPU-first retrieval feasibility phase before narrowing. This does not reward the current failed result. It is the smallest honest test of whether retrieval deserves to stay in scope. If it fails the intermediate lift thresholds, the lane narrows explicitly to deterministic prosodic feature infrastructure, with optional later work on emotion/SER, identity fingerprinting, or articulatory physics under new gates.

## Chosen Wedge / Rejected Wedges

Chosen wedge for the next execution wave:

CPU-first retrieval feasibility for deterministic prosody packets, followed by an explicit wedge decision.

The execution wave must compare:

- current 12-D contour-statistics cosine baseline;
- normalized temporal contour statistics;
- voiced-mask-aware DTW or shape-distance baselines;
- binary/product-quantized codebook plus Hamming retrieval;
- optional CPU ANN path only after the above shows material lift.

Rejected for this wave:

- GPU-first learned retrieval.
- Publicly retiring the retrieval gate before a bounded CPU feasibility pass.
- Treating compression/F0 fidelity as retrieval success.
- Broad speech-codec or speech-intelligence claims.
- Compass-8 or unified-platform framing; Prosody does not implement Compass-8.

Candidate narrow wedge if rescue fails:

Deterministic prosodic feature packet infrastructure: auditable `.zpros` packets for F0, energy, duration, and voiced-mask traces with reproducible replay, real-speech codec evidence, and explicit retrieval failure evidence.

## Commercial / Grant / Research Upside

Commercial upside today is limited by failed retrieval. The strongest current commercial angle is infrastructure:

- reproducible prosodic feature packets for speech analytics;
- audit and replay for call-center, speech QA, and voice-infrastructure pipelines;
- compressed prosodic fingerprints only after a new identity/SER benchmark exists.

Grant upside is moderate:

- auditory science infrastructure;
- speech-prosody reproducibility;
- multilingual prosody data tooling;
- deterministic feature extraction and replay for speech research.

Research upside is credible if the wave produces one of:

- a CPU discrete-codebook retrieval lift against the accepted failed baseline;
- a proof-backed negative showing generic retrieval should be descoped;
- a narrowed mechanics artifact that explains exactly what the codec preserves and fails to preserve.

## Mechanics-Layer Implications

Prosody needs a mechanics layer before any front-door mechanics promotion. The promotable facts must come from source or proof artifacts, not new language.

Candidate mechanics fields:

- Object Basis: sampled prosodic contour bundle.
- Object Currency: F0, energy, duration, voiced-mask frames.
- Transform: quantize, delta encode, zigzag varint, RLE, zlib, packetize as `ZPRS/v1`.
- Preserved Surface: compression, F0 RMSE, energy RMSE, deterministic replay, LibriSpeech real-speech benchmark.
- Failure Surface: retrieval `PRO-C006` failed in-domain and OOD.
- Authority Anchors: `src/zpe_prosody/codec.py`, `src/zpe_prosody/retrieval.py`, Wave-1 proof artifacts, LibriSpeech benchmark, C006 failure analysis.
- State Label: partial, because encode/replay passes while retrieval fails.

The mechanics block must not be promoted until an artifact explicitly enumerates these fields and cites resolving paths.

## Repo-Front-Door Implications

The README already preserves the core failure truth, but repo alignment still has known drift:

- docs/ARCHITECTURE.md and docs/market_surface.json still contain private-stage or stale posture language on current checkout.
- PR #27 contains useful reorientation material but conflicts with later canonical README/SAL changes.
- Any README update must preserve the parser-sensitive ten-section spine and the `Commercial Readiness` enum.
- `Verdict` must remain `FAIL` until the authority gate changes.
- No front-door claim may imply release readiness, commercial transfer closure, or retrieval closure.

## GitHub Requirements

GitHub remains the authority for code, docs, scripts, tests, and small proof files.

Required later, when GitHub mutation is authorized:

- resolve local stashes:
  - README.md plus `WORKSTREAM_PLAN_2026-04-23.md`;
  - CITATION.cff plus CONTRIBUTING.md;
- decide whether to selectively restack PR #27 or close/recreate it;
- add the GPD-ready phase plan or formal `.gpd` structure if the project is being brought under GPD execution;
- commit any new proof manifests, benchmark scripts, small result JSONs, and docs after the CPU feasibility phase.

## Hugging Face Requirements

HF auth was verified during custody with:

`user=Architect-Prime orgs=Zer0pa`

Live dataset repo:

- `Zer0pa/ZPE-Prosody-artifacts`

Already in HF custody:

- `data/fixtures/manifest.json`
- `proofs/artifacts/`

Requirements for execution:

- Upload any new validation corpora, benchmark packs, large result bundles, model weights, checkpoints, or RunPod salvage to HF before relying on them.
- Keep small proof JSONs in GitHub when appropriate, but mirror large bundles in HF.
- If a future learned retrieval or RVQ experiment creates model weights, use `Zer0pa/ZPE-Prosody-models`.
- If a future RunPod experiment creates scratch/intermediate outputs, use `Zer0pa/ZPE-Prosody-scratch`.

## RunPod Requirements

RunPod is not required for the first execution phase.

Use local Mac CPU for:

- branch/GitHub hygiene;
- current baseline reproduction;
- binary-codebook retrieval sweep on current fixture/proof scale;
- DTW/shape-distance comparator;
- small CREMA-D/EMO-DB protocol planning if corpora are obtained.

RunPod CPU is useful only if repeated sweeps become slow or need isolated reproducibility.

RunPod GPU is not justified unless:

- CPU feasibility shows material lift;
- the owner explicitly chooses learned embeddings or SSL/audio representation bake-off;
- all large corpora and model weights are in HF custody.

## Execution Phases

### Phase 0: Repo Truth And Execution Setup

Objective: establish a clean execution baseline without changing public claims.

Tasks:

- verify branch, stashes, PR #27 status, and open PR state;
- verify all README proof anchors resolve;
- run `make test`;
- confirm HF target and file count;
- create a small authority map for all metrics and gates.

Gate:

- working tree clean or intentionally branched;
- tests pass;
- HF custody confirmed;
- retrieval fail remains documented.

### Phase 1: CPU Retrieval Feasibility

Objective: test whether retrieval deserves rescue.

Tasks:

- reproduce current 12-D baseline;
- implement evaluation harness that writes exact p@5 and OOD p@5;
- run normalized statistics, temporal-shape, voiced-mask, DTW, and binary-codebook/Hamming variants;
- compare each against current `0.3067` in-domain and `0.1707` OOD.

Gate:

- continue only if in-domain p@5 >= 0.55 and OOD p@5 >= 0.35 without regressing codec metrics or determinism.

### Phase 2A: Retrieval Rescue Continuation

Objective: continue only if Phase 1 shows credible lift.

Tasks:

- add CPU ANN/index comparator such as RaBitQ/SOAR or equivalent;
- optionally test external embeddings only with explicit model/corpus custody;
- freeze protocol and compare against 0.80/0.65 gates.

Gate:

- pass requires in-domain p@5 >= 0.80 and OOD p@5 >= 0.65.

### Phase 2B: Narrowed Lane Decision

Objective: if Phase 1 or Phase 2A fails, narrow with proof instead of narrative.

Tasks:

- preserve retrieval failure artifacts;
- write a descope proof note;
- define new narrow metrics for deterministic prosodic infrastructure;
- optionally plan emotion/SER, identity fingerprint, or articulatory physics as new gated research, not as inherited retrieval closure.

Gate:

- public docs keep `PRO-C006` failed;
- new wedge has its own measured acceptance gates.

### Phase 3: Mechanics And Front-Door Alignment

Objective: promote only proof-backed mechanics.

Tasks:

- create mechanics artifact under proofs or docs;
- update README/docs only after artifact grounding;
- keep parser-safe section spine;
- keep Commercial Readiness `FAIL` unless authority changes.

Gate:

- every promoted value resolves to source/proof path;
- no invented mechanics noun;
- no broad speech-intelligence claim.

## Verification Gates

- `make test` must pass.
- README proof anchors must resolve.
- `docs/market_surface.json` must parse.
- HF live dataset must contain expected artifacts before new proof bundles are referenced.
- Retrieval benchmarks must compare against the current accepted baseline and write failure as well as success.
- Any new corpus must have license status recorded.
- Any RunPod run must have command log, manifest, and HF custody.

## End-To-End Readiness Verdict

Ready for end-to-end execution of the planned augmentation wave: yes, with constraints.

This is not a product-pass verdict. It means the next execution wave is sufficiently specified to run from repo truth through CPU retrieval feasibility, proof production, and either retrieval continuation or explicit narrowing. Commercial readiness remains `FAIL` until the sovereign retrieval gate passes or the lane is formally narrowed with new authority artifacts.
