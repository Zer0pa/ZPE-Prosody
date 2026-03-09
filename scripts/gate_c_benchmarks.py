"""Gate C: compression, fidelity, and latency benchmarking."""

from __future__ import annotations

import sys
import time
from pathlib import Path

from common import ROOT, init_environment, log_command, parse_args, write_json_artifact

SCRIPTS = ROOT / "scripts"
SRC = ROOT / "src"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fixture_lib import iter_records, load_fixture_manifest
from zpe_prosody.codec import decode_bundle, encode_bundle, encoded_channel_sizes
from zpe_prosody.constants import CLAIM_THRESHOLDS
from zpe_prosody.eval import aggregate_metric, compression_ratio, contour_metrics, percentile
from zpe_prosody.models import ContourBundle


def _bundle(record: dict) -> ContourBundle:
    b = record["bundle"]
    return ContourBundle(
        f0=[float(v) for v in b["f0"]],
        energy=[float(v) for v in b["energy"]],
        duration=[float(v) for v in b["duration"]],
        voiced_mask=[int(v) for v in b["voiced_mask"]],
    )


def main() -> None:
    args = parse_args("Gate C benchmarks")
    out_dir = args.out
    log_path = init_environment(out_dir, args.seed)
    log_command(log_path, "gate_c_benchmarks", "start")

    manifest = load_fixture_manifest(ROOT / "data" / "fixtures" / "manifest.json")

    compression_rows = []
    latency_ms = []
    channel_size_rows = []

    for record in iter_records(manifest, dataset="librispeech_like"):
        bundle = _bundle(record)

        t0 = time.perf_counter()
        packet = encode_bundle(bundle)
        t1 = time.perf_counter()
        latency = (t1 - t0) * 1000.0
        latency_ms.append(latency)

        # Raw baseline uses float32 arrays for f0, energy, duration, and voiced mask.
        raw_size = bundle.frame_count() * 4 * 4
        encoded_size = len(packet)
        compression_rows.append(
            {
                "id": record["id"],
                "frames": bundle.frame_count(),
                "raw_bytes": raw_size,
                "encoded_bytes": encoded_size,
                "compression_ratio": compression_ratio(raw_size, encoded_size),
            }
        )
        channel_size_rows.append({"id": record["id"], **encoded_channel_sizes(packet)})

    arctic_rows = []
    for record in iter_records(manifest, dataset="cmu_arctic_like"):
        bundle = _bundle(record)
        packet = encode_bundle(bundle)
        decoded = decode_bundle(packet).bundle
        arctic_rows.append(contour_metrics(bundle, decoded))

    compression_result = {
        "dataset": "librispeech_like",
        "raw_baseline_definition": "float32 arrays for f0, energy, duration, voiced_mask",
        "samples": len(compression_rows),
        "mean_compression_ratio": aggregate_metric(compression_rows, "compression_ratio"),
        "p50_compression_ratio": percentile([row["compression_ratio"] for row in compression_rows], 0.50),
        "p95_compression_ratio": percentile([row["compression_ratio"] for row in compression_rows], 0.95),
        "threshold": CLAIM_THRESHOLDS["compression_ratio"],
        "pass": aggregate_metric(compression_rows, "compression_ratio") >= CLAIM_THRESHOLDS["compression_ratio"],
        "sample_rows": compression_rows[:20],
        "channel_size_rows": channel_size_rows[:20],
    }

    f0_result = {
        "dataset": "cmu_arctic_like",
        "samples": len(arctic_rows),
        "mean_f0_rmse_pct": aggregate_metric(arctic_rows, "f0_rmse_pct"),
        "p95_f0_rmse_pct": percentile([row["f0_rmse_pct"] for row in arctic_rows], 0.95),
        "threshold": CLAIM_THRESHOLDS["f0_rmse_pct"],
        "pass": aggregate_metric(arctic_rows, "f0_rmse_pct") <= CLAIM_THRESHOLDS["f0_rmse_pct"],
    }

    energy_result = {
        "dataset": "cmu_arctic_like",
        "samples": len(arctic_rows),
        "mean_energy_rmse_pct": aggregate_metric(arctic_rows, "energy_rmse_pct"),
        "p95_energy_rmse_pct": percentile([row["energy_rmse_pct"] for row in arctic_rows], 0.95),
        "threshold": CLAIM_THRESHOLDS["energy_rmse_pct"],
        "pass": aggregate_metric(arctic_rows, "energy_rmse_pct") <= CLAIM_THRESHOLDS["energy_rmse_pct"],
    }

    latency_result = {
        "dataset": "librispeech_like",
        "samples": len(latency_ms),
        "mean_encode_ms": sum(latency_ms) / float(max(1, len(latency_ms))),
        "p95_encode_ms": percentile(latency_ms, 0.95),
        "threshold": CLAIM_THRESHOLDS["encode_ms"],
        "pass": (sum(latency_ms) / float(max(1, len(latency_ms)))) <= CLAIM_THRESHOLDS["encode_ms"],
    }

    write_json_artifact(out_dir, "prosody_compression_benchmark.json", compression_result)
    write_json_artifact(out_dir, "prosody_f0_fidelity.json", f0_result)
    write_json_artifact(out_dir, "prosody_energy_fidelity.json", energy_result)
    write_json_artifact(out_dir, "prosody_latency_benchmark.json", latency_result)

    log_command(
        log_path,
        "gate_c_benchmarks",
        (
            f"compression={compression_result['mean_compression_ratio']:.3f} "
            f"f0={f0_result['mean_f0_rmse_pct']:.3f} "
            f"energy={energy_result['mean_energy_rmse_pct']:.3f} "
            f"latency_ms={latency_result['mean_encode_ms']:.3f}"
        ),
    )
    print("Gate C complete")


if __name__ == "__main__":
    main()
