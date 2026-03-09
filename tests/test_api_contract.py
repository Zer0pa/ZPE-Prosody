from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zpe_prosody.api_service import capability, decode_payload, encode_payload, transfer_payload
from zpe_prosody.extract import generate_prosody_contours


class APIContractTests(unittest.TestCase):
    def test_encode_decode_payload(self) -> None:
        bundle = generate_prosody_contours(seed=200, frames=160)
        payload = encode_payload(bundle.as_dict())
        decoded = decode_payload(payload["packet_b64"])
        self.assertIn("bundle", decoded)
        self.assertEqual(len(decoded["bundle"]["f0"]), 160)

    def test_transfer_payload(self) -> None:
        bundle = generate_prosody_contours(seed=201, frames=100)
        out = transfer_payload(bundle.as_dict(), target_frames=180)
        self.assertEqual(len(out["bundle"]["f0"]), 180)

    def test_capability(self) -> None:
        caps = capability()
        self.assertIn("/encode", caps.endpoints)


if __name__ == "__main__":
    unittest.main()
