"""Wave-CB Phase 1 — ZPE-Prosody comp-benchmark vs lossless float32 codecs.

Compares the ZPE-Prosody codec against gzip and zstd on the committed
CMU-Arctic-like prosody-contour fixture (80 samples) under the
`proofs/artifacts/2026-02-20_zpe_prosody_wave1/` proof bundle.

Per-sample raw representation: float32 concatenation of
    [F0 | energy | duration | voiced_mask]
matching the `raw_baseline_definition` recorded in
`prosody_compression_benchmark.json` ("float32 arrays for f0, energy,
duration, voiced_mask"). All four channels are concatenated into a
single buffer so each comparator sees identical input bytes.

Audio waveform codecs (Opus, FLAC, Vorbis, AAC) are intentionally NOT
in the comparator set — see the framing note in the proof JSON and the
README subsection "Why audio codecs (Opus/FLAC) don't apply".

Usage::

    python scripts/comp_benchmark/run_prosody_comparison.py \
        --fixture data/fixtures/manifest.json \
        --output proofs/artifacts/comp_benchmarks/prosody_codec_comparison.json
"""

from __future__ import annotations

import argparse
import gzip
import json
import statistics
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import zstandard

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from zpe_prosody.codec import decode_bundle, encode_bundle  # noqa: E402
from zpe_prosody.models import ContourBundle  # noqa: E402

DATASET_KEY = "cmu_arctic_like"


def _bundle_from_record(rec: dict) -> ContourBundle:
    b = rec["bundle"]
    return ContourBundle(
        f0=list(b["f0"]),
        energy=list(b["energy"]),
        duration=list(b["duration"]),
        voiced_mask=list(b["voiced_mask"]),
    )


def _raw_float32_buffer(bundle: ContourBundle) -> bytes:
    arr = np.concatenate(
        [
            np.asarray(bundle.f0, dtype=np.float32),
            np.asarray(bundle.energy, dtype=np.float32),
            np.asarray(bundle.duration, dtype=np.float32),
            np.asarray(bundle.voiced_mask, dtype=np.float32),
        ]
    )
    return arr.tobytes()


def _voiced_f0_rmse_hz(orig: ContourBundle, decoded: ContourBundle) -> float:
    f0_o = np.asarray(orig.f0, dtype=np.float64)
    f0_d = np.asarray(decoded.f0, dtype=np.float64)
    mask = np.asarray(orig.voiced_mask, dtype=np.int32) == 1
    if not mask.any():
        return 0.0
    diff = f0_o[mask] - f0_d[mask]
    return float(np.sqrt(np.mean(diff * diff)))


def benchmark_sample(rec: dict) -> Dict[str, float]:
    bundle = _bundle_from_record(rec)
    raw = _raw_float32_buffer(bundle)
    raw_bytes = len(raw)

    gzip_bytes = len(gzip.compress(raw, compresslevel=6))
    zstd_bytes = len(zstandard.ZstdCompressor(level=3).compress(raw))

    packet = encode_bundle(bundle, metadata={"id": rec["id"]})
    zpe_bytes = len(packet)

    decoded = decode_bundle(packet).bundle
    voiced_f0_rmse = _voiced_f0_rmse_hz(bundle, decoded)

    return {
        "id": rec["id"],
        "frames": len(bundle.f0),
        "raw_bytes": raw_bytes,
        "zpe_bytes": zpe_bytes,
        "gzip_bytes": gzip_bytes,
        "zstd_bytes": zstd_bytes,
        "zpe_cr": raw_bytes / zpe_bytes,
        "gzip_cr": raw_bytes / gzip_bytes,
        "zstd_cr": raw_bytes / zstd_bytes,
        "voiced_f0_rmse_hz_zpe": voiced_f0_rmse,
    }


def aggregate(rows: List[Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    def agg(key: str) -> Dict[str, float]:
        vals = [r[key] for r in rows]
        return {
            "mean": float(statistics.fmean(vals)),
            "median": float(statistics.median(vals)),
            "min": float(min(vals)),
            "max": float(max(vals)),
        }

    return {
        "zpe_prosody": {
            **agg("zpe_cr"),
            "voiced_f0_rmse_hz_mean": float(
                statistics.fmean(r["voiced_f0_rmse_hz_zpe"] for r in rows)
            ),
        },
        "gzip_level6": agg("gzip_cr"),
        "zstd_level3": agg("zstd_cr"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fixture", default=str(REPO_ROOT / "data/fixtures/manifest.json"))
    ap.add_argument(
        "--output",
        default=str(
            REPO_ROOT / "proofs/artifacts/comp_benchmarks/prosody_codec_comparison.json"
        ),
    )
    args = ap.parse_args()

    fixture_path = Path(args.fixture)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with fixture_path.open() as fh:
        manifest = json.load(fh)

    samples = [r for r in manifest["records"] if r.get("dataset") == DATASET_KEY]
    if len(samples) != 80:
        raise SystemExit(
            f"Expected 80 {DATASET_KEY} samples in fixture, found {len(samples)}"
        )

    per_sample = [benchmark_sample(rec) for rec in samples]
    summary = aggregate(per_sample)

    payload = {
        "schema_version": "1.0.0",
        "lane": "ZPE-Prosody",
        "wave": "Wave-CB Phase 1",
        "dataset": {
            "name": DATASET_KEY,
            "fixture_path": str(fixture_path.relative_to(REPO_ROOT)),
            "sample_count": len(samples),
            "source_proof": "proofs/artifacts/2026-02-20_zpe_prosody_wave1/",
        },
        "raw_baseline_definition": (
            "float32 concatenation of [F0 | energy | duration | voiced_mask] "
            "(matches raw_baseline_definition in prosody_compression_benchmark.json)"
        ),
        "comparators": {
            "zpe_prosody": {
                "kind": "ZPE-Prosody .zpros packet",
                "level": "default (CHANNEL_STEPS / CHANNEL_STRIDES from constants.py)",
                "loss_profile": "bounded-lossy (quantized contours, lossless voiced mask)",
            },
            "gzip_level6": {
                "kind": "stdlib gzip on raw float32 bytes",
                "level": 6,
                "loss_profile": "lossless",
            },
            "zstd_level3": {
                "kind": "zstandard.ZstdCompressor on raw float32 bytes",
                "level": 3,
                "loss_profile": "lossless",
            },
        },
        "framing_note": (
            "Audio waveform codecs (Opus, FLAC, Vorbis, AAC) are intentionally "
            "excluded from the comparator set. ZPE-Prosody encodes prosody "
            "contour metadata sequences (F0, energy, duration, voiced_mask), "
            "not time-domain audio waveform samples. Audio codecs operate on a "
            "different abstraction level (PCM at 16-48 kHz) and would compare "
            "apples to oranges. Lossless general-purpose byte codecs (gzip, "
            "zstd) are the apples-to-apples baseline because the published "
            "claim is compression ratio against the float32 contour baseline."
        ),
        "metric_notes": {
            "compression_ratio": "raw_bytes / encoded_bytes; higher is better.",
            "voiced_f0_rmse_hz": (
                "RMSE in Hz between original and ZPE-decoded F0, restricted "
                "to frames where voiced_mask == 1. gzip and zstd are lossless "
                "by construction so their RMSE is 0 Hz and is not stored."
            ),
        },
        "summary": summary,
        "per_sample": per_sample,
    }

    with output_path.open("w") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")

    print(f"Wrote {output_path}")
    print(
        "ZPE mean CR: {:.3f}x | gzip mean CR: {:.3f}x | zstd mean CR: {:.3f}x".format(
            summary["zpe_prosody"]["mean"],
            summary["gzip_level6"]["mean"],
            summary["zstd_level3"]["mean"],
        )
    )
    print(
        "ZPE voiced-F0 RMSE mean: {:.4f} Hz".format(
            summary["zpe_prosody"]["voiced_f0_rmse_hz_mean"]
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
