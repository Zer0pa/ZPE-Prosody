from __future__ import annotations

import unittest

from zpe_prosody.codec import ZProsDecodeError, decode_bundle, encode_bundle
from zpe_prosody.extract import generate_prosody_contours


class PacketFormatTests(unittest.TestCase):
    def test_encode_decode_shape(self) -> None:
        bundle = generate_prosody_contours(seed=111, frames=320)
        packet = encode_bundle(bundle, metadata={"sample_id": "unit"})
        decoded = decode_bundle(packet)
        self.assertEqual(bundle.frame_count(), decoded.bundle.frame_count())
        self.assertEqual(len(bundle.voiced_mask), len(decoded.bundle.voiced_mask))

    def test_bad_magic_raises(self) -> None:
        bundle = generate_prosody_contours(seed=112, frames=100)
        packet = encode_bundle(bundle)
        bad = b"BAD!" + packet[4:]
        with self.assertRaises(ZProsDecodeError):
            decode_bundle(bad)


if __name__ == "__main__":
    unittest.main()
