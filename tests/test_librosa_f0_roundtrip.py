from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

HAS_LIBROSA = importlib.util.find_spec("librosa") is not None
if HAS_LIBROSA:
    import librosa
    import numpy as np

from zpe_prosody.codec import decode_bundle, encode_bundle
from zpe_prosody.constants import DEFAULT_SAMPLE_RATE, FRAME_MS, FRAME_SAMPLES
from zpe_prosody.eval import rmse_pct, voiced_only
from zpe_prosody.extract import generate_prosody_contours, synthesize_waveform
from zpe_prosody.models import ContourBundle


def run_length_durations(mask: list[int]) -> list[float]:
    durations = [0.0] * len(mask)
    start = 0
    while start < len(mask):
        state = mask[start]
        end = start + 1
        while end < len(mask) and mask[end] == state:
            end += 1
        seg_ms = float(end - start) * FRAME_MS
        for idx in range(start, end):
            durations[idx] = seg_ms
        start = end
    return durations


@unittest.skipUnless(HAS_LIBROSA, "librosa test extra not installed")
class LibrosaRoundTripTests(unittest.TestCase):
    def test_librosa_f0_roundtrip(self) -> None:
        source = generate_prosody_contours(seed=701, frames=180, emotion="surprised")
        waveform = np.asarray(synthesize_waveform(source, sample_rate=DEFAULT_SAMPLE_RATE), dtype=np.float32)

        yin_f0 = librosa.yin(
            y=waveform,
            fmin=65.0,
            fmax=420.0,
            sr=DEFAULT_SAMPLE_RATE,
            frame_length=1024,
            hop_length=FRAME_SAMPLES,
        )
        rms = librosa.feature.rms(
            y=waveform,
            frame_length=1024,
            hop_length=FRAME_SAMPLES,
        )[0]

        frame_count = min(len(yin_f0), len(rms))
        peak_rms = max(float(rms[:frame_count].max()), 1e-9)
        energy = [float(value) / peak_rms for value in rms[:frame_count]]
        voiced_mask = []
        extracted_f0 = []
        for pitch_hz, energy_value in zip(yin_f0[:frame_count], energy):
            voiced = 1 if (energy_value > 0.05 and math.isfinite(float(pitch_hz))) else 0
            voiced_mask.append(voiced)
            extracted_f0.append(float(pitch_hz) if voiced else 0.0)

        bundle = ContourBundle(
            f0=extracted_f0,
            energy=energy,
            duration=run_length_durations(voiced_mask),
            voiced_mask=voiced_mask,
        )
        packet = encode_bundle(bundle, metadata={"backend": "librosa_yin"})
        decoded = decode_bundle(packet).bundle

        self.assertEqual(bundle.frame_count(), decoded.frame_count())
        self.assertLessEqual(
            rmse_pct(voiced_only(bundle.f0, bundle.voiced_mask), voiced_only(decoded.f0, bundle.voiced_mask)),
            5.0,
        )
        self.assertLessEqual(rmse_pct(bundle.energy, decoded.energy), 3.0)


if __name__ == "__main__":
    unittest.main()
