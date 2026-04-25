# Comp-Benchmark — ZPE-Prosody (Wave-CB Phase 1)

Source data: `proofs/artifacts/2026-02-20_zpe_prosody_wave1/` — committed
CMU-Arctic-like prosody fixture, 80 samples, four contour channels per
sample (F0, energy, duration, voiced_mask).

Raw baseline: `float32` concatenation of all four channels per sample.
Identical input bytes are fed to every comparator.

## Comparator set

| Codec         | Loss profile   | Notes                                              |
|---------------|----------------|----------------------------------------------------|
| ZPE-Prosody   | bounded-lossy  | `.zpros` packet, default `CHANNEL_STEPS`/strides   |
| gzip level 6  | lossless       | stdlib `gzip.compress`                             |
| zstd level 3  | lossless       | `zstandard.ZstdCompressor(level=3)`                |

## Results (80 samples, CMU-Arctic-like)

| Codec        | Mean CR | Median CR | Min CR | Max CR | Voiced-F0 RMSE (Hz) |
|--------------|--------:|----------:|-------:|-------:|--------------------:|
| ZPE-Prosody  | 13.65x  | 13.85x    | 10.16x | 17.07x | 1.44                |
| gzip (L6)    |  2.21x  |  2.22x    |  2.14x |  2.26x | 0 (lossless)        |
| zstd (L3)    |  2.22x  |  2.22x    |  2.15x |  2.26x | 0 (lossless)        |

## Honest framing

ZPE-Prosody is bounded-lossy (quantized contours), so a strict
apples-to-apples comparison with lossless gzip/zstd needs to account
for the residual error budget. The voiced-F0 RMSE of ~1.4 Hz is well
inside the lane's published 5% RMSE threshold (see
`prosody_f0_fidelity.json`, mean 0.89%), so the additional ~6x
compression over lossless byte codecs comes at a fidelity cost the
lane has already classified as PASS by its own gate.

This is a portfolio result for the prosody-contour codec only. It is
not a claim about audio quality, perceptual prosody, or speech codec
performance.

## Why audio codecs (Opus/FLAC) don't apply

ZPE-Prosody encodes prosody contour metadata (per-frame F0, energy,
duration, voiced-mask sequences). Audio codecs (Opus, FLAC, Vorbis,
AAC) encode time-domain PCM waveform samples (typically 16-48 kHz).
The two operate at different abstraction levels — comparing them would
be apples to oranges.

The correct apples-to-apples baseline for the published "compression
ratio vs float32 contour buffer" claim is general-purpose lossless byte
compression (gzip, zstd), which is exactly the comparator set used
here.

## Reproduce

```bash
python -m venv .venv && source .venv/bin/activate
pip install zstandard numpy
python scripts/comp_benchmark/run_prosody_comparison.py \
    --fixture data/fixtures/manifest.json \
    --output proofs/artifacts/comp_benchmarks/prosody_codec_comparison.json
```
