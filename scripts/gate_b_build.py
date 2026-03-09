"""Gate B: core contour encode/decode and packet robustness smoke checks."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from common import ROOT, init_environment, log_command, parse_args, write_json_artifact

SCRIPTS = ROOT / "scripts"
SRC = ROOT / "src"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fixture_lib import load_fixture_manifest
from zpe_prosody.codec import decode_bundle, encode_bundle
from zpe_prosody.eval import contour_metrics
from zpe_prosody.extract import extract_contours, synthesize_waveform
from zpe_prosody.models import ContourBundle


def _bundle_from_record(record: dict) -> ContourBundle:
    bundle = record["bundle"]
    return ContourBundle(
        f0=[float(v) for v in bundle["f0"]],
        energy=[float(v) for v in bundle["energy"]],
        duration=[float(v) for v in bundle["duration"]],
        voiced_mask=[int(v) for v in bundle["voiced_mask"]],
    )


def main() -> None:
    args = parse_args("Gate B build")
    out_dir = args.out
    log_path = init_environment(out_dir, args.seed)
    log_command(log_path, "gate_b_build", "start")

    manifest = load_fixture_manifest(ROOT / "data" / "fixtures" / "manifest.json")
    records = manifest["records"][:60]

    max_f0_pct = 0.0
    max_energy_pct = 0.0
    deterministic_ok = True
    extract_lengths_ok = True
    packet_hashes = []

    for record in records:
        bundle = _bundle_from_record(record)
        packet_1 = encode_bundle(bundle, metadata={"sample_id": record["id"]})
        packet_2 = encode_bundle(bundle, metadata={"sample_id": record["id"]})
        if packet_1 != packet_2:
            deterministic_ok = False
        packet_hashes.append(hashlib.sha256(packet_1).hexdigest())

        decoded = decode_bundle(packet_1).bundle
        metrics = contour_metrics(bundle, decoded)
        max_f0_pct = max(max_f0_pct, metrics["f0_rmse_pct"])
        max_energy_pct = max(max_energy_pct, metrics["energy_rmse_pct"])

        waveform = synthesize_waveform(bundle, seed=args.seed)
        extracted, _meta = extract_contours(waveform)
        if extracted.frame_count() == 0:
            extract_lengths_ok = False

    result = {
        "checked_samples": len(records),
        "max_f0_rmse_pct": max_f0_pct,
        "max_energy_rmse_pct": max_energy_pct,
        "deterministic_packet_bytes": deterministic_ok,
        "extract_nonempty": extract_lengths_ok,
        "packet_hash_examples": packet_hashes[:10],
        "status": "PASS" if deterministic_ok and extract_lengths_ok else "FAIL",
    }

    write_json_artifact(out_dir, "gate_b_roundtrip.json", result)
    log_command(log_path, "gate_b_build", f"result={result['status']}")
    print(f"Gate B complete -> {out_dir / 'gate_b_roundtrip.json'}")


if __name__ == "__main__":
    main()
