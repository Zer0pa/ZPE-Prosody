# ZPE-Prosody Novelty Card

**Product:** ZPE-Prosody
**Domain:** Deterministic encoding of prosodic contour signals: F0, energy, duration, and voiced-mask structure.
**What we sell:** Auditable, reproducible prosody packets for speech-analysis and voice-infrastructure workflows where replay stability matters more than generic audio compression.

## Novel contributions

1. **`.zpros` packet format with deterministic replay semantics** — ZPE-Prosody packages contour channels into a versioned binary packet with `ZPRS` magic, explicit packet versioning, per-channel typed payloads, metadata framing, and CRC32 verification at decode time. The lane-specific value is not CRC32 by itself; it is the combination of deterministic contour packing plus a structured packet contract that makes replay auditable and malformed-input handling explicit. Code: `src/zpe_prosody/constants.py:8-23`, `src/zpe_prosody/codec.py:263-359`. What is genuinely new here: a prosody-specific packet contract for deterministic replay over F0, energy, duration, and voiced-mask channels.
2. **Quantized contour codec tuned for prosodic signals** — The codec quantizes prosodic channels with lane-specific steps, converts them into delta streams, zigzag-varint serializes signed changes, applies run-length encoding where repetition exists, and compresses each channel independently before packet assembly. Code: `src/zpe_prosody/constants.py:8-20`, `src/zpe_prosody/codec.py:25-148`, `src/zpe_prosody/codec.py:263-296`. What is genuinely new here: applying this deterministic contour-specific packing scheme to prosodic features with explicit channel steps for F0, energy, and duration rather than treating speech as a generic waveform codec problem.
3. **12-D hand-crafted retrieval embedding for contour similarity** — The retrieval surface builds a fixed-size embedding from contour statistics over voiced F0, energy, duration, and voiced ratio, then uses cosine similarity plus `precision_at_k`/`mean_precision_at_k` evaluation to rank neighbors. Code: `src/zpe_prosody/retrieval.py:31-95`. What is genuinely new here: a lightweight contour-structured embedding designed around prosodic channels rather than learned acoustic representations or generic speech embeddings.

## Standard techniques used (explicit, not novel)

- zlib compression
- Zigzag integer encoding
- Varint serialization
- Run-length encoding
- CRC32 integrity checking
- Cosine similarity

## Compass-8 / 8-primitive architecture

NO — this codec does not implement Compass-8 or any directional primitive encoder. It uses quantized contour deltas, zigzag-varint serialization, RLE, and zlib over prosody channels instead. Code: `src/zpe_prosody/codec.py:25-148`, `src/zpe_prosody/codec.py:263-296`.

## Open novelty questions for the license agent

- The 12-D retrieval embedding in `src/zpe_prosody/retrieval.py:31-95` is lane-specific and structured, but the retrieval claim is still blocked at `p@5 = 0.307` versus the `0.80` gate. Treat the embedding as a candidate novelty surface, not a proven product capability.
- The license schedule should list verified codec and packet-surface contributions, but it should not present retrieval closure as achieved capability while `PRO-C006` remains `FAIL`.
- Verified claims safe to schedule: compression (`16.60×`) and fidelity (`F0_RMSE 0.89%`, `ENERGY_RMSE 2.08%`) from `proofs/artifacts/2026-02-20_zpe_prosody_wave1/`. Retrieval should remain explicitly blocked.
