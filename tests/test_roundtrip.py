from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zpe_prosody.codec import decode_bundle, encode_bundle
from zpe_prosody.eval import contour_metrics
from zpe_prosody.extract import generate_prosody_contours


class RoundTripTests(unittest.TestCase):
    def test_roundtrip_fidelity(self) -> None:
        bundle = generate_prosody_contours(seed=113, frames=400, emotion="happy")
        packet = encode_bundle(bundle)
        decoded = decode_bundle(packet).bundle
        metrics = contour_metrics(bundle, decoded)
        self.assertLessEqual(metrics["f0_rmse_pct"], 5.0)
        self.assertLessEqual(metrics["energy_rmse_pct"], 3.0)

    def test_deterministic_bytes(self) -> None:
        bundle = generate_prosody_contours(seed=114, frames=220, emotion="sad")
        packet_a = encode_bundle(bundle, metadata={"a": 1})
        packet_b = encode_bundle(bundle, metadata={"a": 1})
        self.assertEqual(packet_a, packet_b)


if __name__ == "__main__":
    unittest.main()
