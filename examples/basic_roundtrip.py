from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zpe_prosody.codec import decode_bundle, encode_bundle
from zpe_prosody.eval import compression_ratio, contour_metrics
from zpe_prosody.extract import generate_prosody_contours


def main() -> None:
    bundle = generate_prosody_contours(seed=314, frames=240, emotion="happy")
    packet = encode_bundle(bundle, metadata={"sample_id": "basic_roundtrip"})
    decoded = decode_bundle(packet).bundle
    metrics = contour_metrics(bundle, decoded)
    raw_bytes = bundle.frame_count() * 4 * 4
    result = {
        "compression_ratio": round(compression_ratio(raw_bytes, len(packet)), 3),
        "encoded_bytes": len(packet),
        "f0_rmse_pct": round(metrics["f0_rmse_pct"], 4),
        "frames": bundle.frame_count(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
