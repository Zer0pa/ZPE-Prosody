# LibriSpeech Benchmark

This artifact set benchmarks the live ZPE Prosody codec on 100 real LibriSpeech `test-clean` utterances.

## Method

- Dataset: OpenSLR LibriSpeech `test-clean`.
- Samples: 100
- Extractor: `praat-parselmouth` (`Sound.to_pitch`, `Sound.to_intensity`) at 10 ms frames.
- Codec path: `encode_bundle -> decode_bundle` from `src/zpe_prosody/codec.py`.
- Baseline size: float32 arrays for `f0`, `energy`, `duration`, and `voiced_mask`.

## Results

- Mean compression ratio: 13.012x
- Mean voiced-F0 RMSE: 1.437 Hz (0.637%)
- Mean timing RMSE: 0.000 ms
- Mean encode latency: 2.668 ms

Lane note: this evidence shows the codec works on real speech, but it does not change the commercial lane verdict. `PRO-C005` and `PRO-C006` remain blocked by separate authority gates.
