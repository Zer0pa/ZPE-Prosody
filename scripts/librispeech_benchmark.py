"""Run a real-data LibriSpeech benchmark for the ZPE Prosody codec."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
from pathlib import Path

import parselmouth

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zpe_prosody.codec import (  # noqa: E402
    decode_bundle,
    encode_bundle,
    encoded_channel_sizes,
)
from zpe_prosody.models import ContourBundle  # noqa: E402

LIBRISPEECH_TEST_CLEAN_URL = "https://www.openslr.org/resources/12/test-clean.tar.gz"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--samples",
        type=int,
        default=100,
        help="Number of LibriSpeech utterances to benchmark.",
    )
    parser.add_argument(
        "--cache-root",
        type=Path,
        default=ROOT / ".runtime" / "datasets" / "librispeech_test_clean",
        help="Ignored cache directory for the dataset payload.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "proofs" / "artifacts" / "librispeech_benchmark",
        help="Artifact output directory.",
    )
    return parser.parse_args()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_log(path: Path, message: str) -> None:
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    entry = f"[{timestamp}] {message}\n"
    prior = path.read_text(encoding="utf-8") if path.exists() else ""
    path.write_text(
        prior + entry,
        encoding="utf-8",
    )


def download_dataset(cache_root: Path, log_path: Path) -> Path:
    ensure_dir(cache_root)
    tar_path = cache_root / "test-clean.tar.gz"
    extract_root = cache_root / "LibriSpeech"
    if not tar_path.exists():
        append_log(log_path, f"download start url={LIBRISPEECH_TEST_CLEAN_URL}")
        urllib.request.urlretrieve(LIBRISPEECH_TEST_CLEAN_URL, tar_path)
        append_log(log_path, f"download complete bytes={tar_path.stat().st_size}")
    if not extract_root.exists():
        append_log(log_path, f"extract start path={tar_path}")
        with tarfile.open(tar_path, "r:gz") as archive:
            archive.extractall(cache_root)
        append_log(log_path, f"extract complete root={extract_root}")
    return extract_root


def list_audio_files(dataset_root: Path, limit: int) -> list[Path]:
    files = sorted(dataset_root.rglob("*.flac"))
    if len(files) < limit:
        raise RuntimeError(f"Requested {limit} samples but only found {len(files)} .flac files")
    return files[:limit]


def normalize(values: list[float]) -> list[float]:
    if not values:
        return []
    lo = min(values)
    hi = max(values)
    if math.isclose(lo, hi):
        return [0.0 for _ in values]
    span = hi - lo
    return [(value - lo) / span for value in values]


def run_length_durations(mask: list[int], frame_ms: float = 10.0) -> list[float]:
    durations = [0.0] * len(mask)
    start = 0
    while start < len(mask):
        state = mask[start]
        end = start + 1
        while end < len(mask) and mask[end] == state:
            end += 1
        seg_ms = float(end - start) * frame_ms
        for idx in range(start, end):
            durations[idx] = seg_ms
        start = end
    return durations


def load_sound(audio_path: Path) -> parselmouth.Sound:
    try:
        return parselmouth.Sound(str(audio_path))
    except Exception:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-loglevel",
                    "error",
                    "-i",
                    str(audio_path),
                    str(tmp_path),
                ],
                check=True,
            )
            return parselmouth.Sound(str(tmp_path))
        finally:
            if tmp_path.exists():
                tmp_path.unlink()


def extract_bundle(audio_path: Path) -> ContourBundle:
    sound = load_sound(audio_path)
    pitch = sound.to_pitch(time_step=0.01, pitch_floor=75.0, pitch_ceiling=500.0)
    intensity = sound.to_intensity(time_step=0.01)

    f0_values = pitch.selected_array["frequency"].tolist()
    intensity_values = intensity.values[0].tolist()
    frame_count = min(len(f0_values), len(intensity_values))
    f0 = [float(value) if value and value > 0.0 else 0.0 for value in f0_values[:frame_count]]
    voiced_mask = [1 if value > 0.0 else 0 for value in f0]
    energy = normalize([float(value) for value in intensity_values[:frame_count]])
    duration = run_length_durations(voiced_mask)
    return ContourBundle(f0=f0, energy=energy, duration=duration, voiced_mask=voiced_mask)


def rmse(reference: list[float], observed: list[float]) -> float:
    if len(reference) != len(observed):
        raise ValueError("RMSE inputs must have equal length")
    if not reference:
        return 0.0
    mse = sum((left - right) ** 2 for left, right in zip(reference, observed))
    mse /= float(len(reference))
    return mse ** 0.5


def rmse_pct(reference: list[float], observed: list[float]) -> float:
    baseline = max((abs(value) for value in reference), default=1.0)
    if baseline == 0.0:
        baseline = 1.0
    return (rmse(reference, observed) / baseline) * 100.0


def voiced_only(values: list[float], mask: list[int]) -> list[float]:
    return [value for value, voiced in zip(values, mask) if voiced == 1]


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = int(round((len(ordered) - 1) * pct))
    return ordered[idx]


def summarize_mean(rows: list[dict], key: str) -> float:
    if not rows:
        return 0.0
    return sum(float(row[key]) for row in rows) / float(len(rows))


def build_readme(
    sample_count: int,
    compression_result: dict,
    f0_result: dict,
    timing_result: dict,
    latency_result: dict,
) -> str:
    return "\n".join(
        [
            "# LibriSpeech Benchmark",
            "",
            "This artifact set benchmarks the live ZPE Prosody codec on "
            + str(sample_count)
            + " real LibriSpeech `test-clean` utterances.",
            "",
            "## Method",
            "",
            "- Dataset: OpenSLR LibriSpeech `test-clean`.",
            "- Samples: "
            + str(sample_count),
            (
                "- Extractor: `praat-parselmouth` (`Sound.to_pitch`, "
                "`Sound.to_intensity`) at 10 ms frames."
            ),
            "- Codec path: `encode_bundle -> decode_bundle` from `src/zpe_prosody/codec.py`.",
            "- Baseline size: float32 arrays for `f0`, `energy`, `duration`, and `voiced_mask`.",
            "",
            "## Results",
            "",
            f"- Mean compression ratio: {compression_result['mean_compression_ratio']:.3f}x",
            (
                f"- Mean voiced-F0 RMSE: {f0_result['mean_f0_rmse_hz']:.3f} Hz "
                f"({f0_result['mean_f0_rmse_pct']:.3f}%)"
            ),
            f"- Mean timing RMSE: {timing_result['mean_timing_rmse_ms']:.3f} ms",
            f"- Mean encode latency: {latency_result['mean_encode_ms']:.3f} ms",
            "",
            (
                "Lane note: this evidence shows the codec works on real speech, "
                "but it does not change the commercial lane verdict. "
                "`PRO-C005` and `PRO-C006` remain blocked by separate authority gates."
            ),
            "",
        ]
    )


def main() -> None:
    args = parse_args()
    ensure_dir(args.out)
    log_path = args.out / "command_log.txt"
    dataset_root = download_dataset(args.cache_root, log_path)
    audio_files = list_audio_files(dataset_root, args.samples)

    compression_rows: list[dict] = []
    f0_rows: list[dict] = []
    timing_rows: list[dict] = []
    latency_rows: list[float] = []
    channel_rows: list[dict] = []
    manifest_rows: list[dict] = []

    append_log(log_path, f"benchmark start samples={len(audio_files)}")
    for audio_path in audio_files:
        bundle = extract_bundle(audio_path)
        if bundle.frame_count() == 0:
            append_log(log_path, f"skip empty_bundle path={audio_path}")
            continue

        t0 = time.perf_counter()
        packet = encode_bundle(
            bundle,
            metadata={"sample_path": str(audio_path.relative_to(dataset_root))},
        )
        latency_ms = (time.perf_counter() - t0) * 1000.0
        decoded = decode_bundle(packet).bundle

        sample_id = audio_path.stem
        raw_bytes = bundle.frame_count() * 4 * 4
        encoded_bytes = len(packet)
        voiced_f0 = voiced_only(bundle.f0, bundle.voiced_mask)
        voiced_hat = voiced_only(decoded.f0, bundle.voiced_mask)

        compression_rows.append(
            {
                "id": sample_id,
                "frames": bundle.frame_count(),
                "raw_bytes": raw_bytes,
                "encoded_bytes": encoded_bytes,
                "compression_ratio": raw_bytes / float(encoded_bytes),
            }
        )
        f0_rows.append(
            {
                "id": sample_id,
                "f0_rmse_hz": rmse(voiced_f0, voiced_hat),
                "f0_rmse_pct": rmse_pct(voiced_f0, voiced_hat),
            }
        )
        timing_rows.append(
            {
                "id": sample_id,
                "timing_rmse_ms": rmse(bundle.duration, decoded.duration),
            }
        )
        latency_rows.append(latency_ms)
        channel_rows.append({"id": sample_id, **encoded_channel_sizes(packet)})
        manifest_rows.append(
            {
                "id": sample_id,
                "path": str(audio_path.relative_to(dataset_root)),
                "frames": bundle.frame_count(),
            }
        )

    compression_result = {
        "dataset": "librispeech_test_clean",
        "samples": len(compression_rows),
        "raw_baseline_definition": "float32 arrays for f0, energy, duration, voiced_mask",
        "mean_compression_ratio": summarize_mean(compression_rows, "compression_ratio"),
        "p50_compression_ratio": percentile(
            [row["compression_ratio"] for row in compression_rows],
            0.50,
        ),
        "p95_compression_ratio": percentile(
            [row["compression_ratio"] for row in compression_rows],
            0.95,
        ),
        "sample_rows": compression_rows[:20],
        "channel_size_rows": channel_rows[:20],
    }
    f0_result = {
        "dataset": "librispeech_test_clean",
        "samples": len(f0_rows),
        "mean_f0_rmse_hz": summarize_mean(f0_rows, "f0_rmse_hz"),
        "mean_f0_rmse_pct": summarize_mean(f0_rows, "f0_rmse_pct"),
        "p95_f0_rmse_hz": percentile([row["f0_rmse_hz"] for row in f0_rows], 0.95),
        "p95_f0_rmse_pct": percentile([row["f0_rmse_pct"] for row in f0_rows], 0.95),
        "sample_rows": f0_rows[:20],
    }
    timing_result = {
        "dataset": "librispeech_test_clean",
        "samples": len(timing_rows),
        "mean_timing_rmse_ms": summarize_mean(timing_rows, "timing_rmse_ms"),
        "p95_timing_rmse_ms": percentile([row["timing_rmse_ms"] for row in timing_rows], 0.95),
        "sample_rows": timing_rows[:20],
    }
    latency_result = {
        "dataset": "librispeech_test_clean",
        "samples": len(latency_rows),
        "mean_encode_ms": sum(latency_rows) / float(max(1, len(latency_rows))),
        "p95_encode_ms": percentile(latency_rows, 0.95),
    }

    write_json(args.out / "compression_benchmark.json", compression_result)
    write_json(args.out / "f0_fidelity.json", f0_result)
    write_json(args.out / "timing_fidelity.json", timing_result)
    write_json(args.out / "latency_benchmark.json", latency_result)
    write_json(
        args.out / "sample_manifest.json",
        {"dataset": "librispeech_test_clean", "samples": manifest_rows},
    )
    (args.out / "README.md").write_text(
        build_readme(
            sample_count=len(compression_rows),
            compression_result=compression_result,
            f0_result=f0_result,
            timing_result=timing_result,
            latency_result=latency_result,
        ),
        encoding="utf-8",
    )
    append_log(log_path, f"benchmark complete samples={len(compression_rows)}")


if __name__ == "__main__":
    main()
