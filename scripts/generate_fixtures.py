"""Generates deterministic fixture corpora for Wave-1 execution."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zpe_prosody.constants import GLOBAL_SEED
from zpe_prosody.extract import generate_prosody_contours
from zpe_prosody.utils import ensure_dir


def _sample_record(sample_id: str, bundle, label: str, dataset: str) -> dict:
    return {
        "id": sample_id,
        "dataset": dataset,
        "label": label,
        "bundle": bundle.as_dict(),
    }


def build_fixture_manifest(seed: int) -> dict:
    rng = random.Random(seed)
    records = []

    # LibriSpeech-like corpus for compression/latency robustness.
    for idx in range(140):
        frames = rng.randint(260, 560)
        speaker_bias = rng.uniform(-1.0, 1.0)
        bundle = generate_prosody_contours(seed + idx, frames, emotion="neutral", speaker_bias=speaker_bias)
        records.append(_sample_record(f"libri_{idx:04d}", bundle, "neutral", "librispeech_like"))

    # CMU ARCTIC-like corpus for fidelity checks.
    for idx in range(80):
        frames = rng.randint(220, 420)
        speaker_bias = rng.uniform(-0.8, 0.8)
        emotion = "calm" if idx % 3 else "neutral"
        bundle = generate_prosody_contours(seed + 1000 + idx, frames, emotion=emotion, speaker_bias=speaker_bias)
        records.append(_sample_record(f"arctic_{idx:04d}", bundle, emotion, "cmu_arctic_like"))

    # RAVDESS-like emotional corpus for retrieval and confusion testing.
    emotions = ["neutral", "happy", "sad", "angry", "fearful", "disgust", "surprised", "calm"]
    for emo_idx, emo in enumerate(emotions):
        for idx in range(18):
            frames = rng.randint(200, 360)
            speaker_bias = rng.uniform(-0.05, 0.05) + ((emo_idx - 3.5) * 0.40)
            bundle = generate_prosody_contours(seed + 3000 + (emo_idx * 100) + idx, frames, emotion=emo, speaker_bias=speaker_bias)
            records.append(_sample_record(f"ravdess_{emo}_{idx:03d}", bundle, emo, "ravdess_like"))

    return {
        "seed": seed,
        "record_count": len(records),
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic prosody fixtures")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=GLOBAL_SEED)
    args = parser.parse_args()

    ensure_dir(args.out)
    manifest = build_fixture_manifest(seed=args.seed)
    with (args.out / "manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)

    print(f"Generated fixtures: {manifest['record_count']} -> {args.out / 'manifest.json'}")


if __name__ == "__main__":
    main()
