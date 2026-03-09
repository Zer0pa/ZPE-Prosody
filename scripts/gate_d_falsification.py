"""Gate D: malformed/adversarial/falsification campaigns."""

from __future__ import annotations

import random
import sys
from pathlib import Path

from common import ROOT, init_environment, log_command, parse_args

SCRIPTS = ROOT / "scripts"
SRC = ROOT / "src"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from determinism_replay import run_replay
from fixture_lib import iter_records, load_fixture_manifest
from zpe_prosody.codec import ZProsDecodeError, decode_bundle, encode_bundle
from zpe_prosody.eval import rmse_pct
from zpe_prosody.extract import extract_contours, synthesize_waveform
from zpe_prosody.models import ContourBundle
from zpe_prosody.utils import write_json, write_text


def _bundle(record: dict) -> ContourBundle:
    b = record["bundle"]
    return ContourBundle(
        f0=[float(v) for v in b["f0"]],
        energy=[float(v) for v in b["energy"]],
        duration=[float(v) for v in b["duration"]],
        voiced_mask=[int(v) for v in b["voiced_mask"]],
    )


def _flip_boundary(mask: list[int], seed: int) -> list[int]:
    rng = random.Random(seed)
    out = list(mask)
    for idx in range(1, len(out) - 1):
        if out[idx] != out[idx - 1] and rng.random() < 0.5:
            out[idx] = 1 - out[idx]
    return out


def main() -> None:
    args = parse_args("Gate D falsification")
    out_dir = args.out
    log_path = init_environment(out_dir, args.seed)
    log_command(log_path, "gate_d_falsification", "start")

    manifest = load_fixture_manifest(ROOT / "data" / "fixtures" / "manifest.json")

    # DT-PRO-1: malformed packet campaign
    malformed_cases = []
    uncaught_crashes = 0
    base_record = manifest["records"][0]
    base_packet = encode_bundle(_bundle(base_record), metadata={"sample_id": base_record["id"]})

    malformed_blobs = [
        base_packet[:10],
        base_packet[:-7],
        b"BAD!" + base_packet[4:],
        bytearray(base_packet),
    ]
    if isinstance(malformed_blobs[3], bytearray):
        malformed_blobs[3][18] = malformed_blobs[3][18] ^ 0xFF
        malformed_blobs[3] = bytes(malformed_blobs[3])

    for idx, blob in enumerate(malformed_blobs):
        try:
            decode_bundle(blob)
            malformed_cases.append({"case": idx, "handled": False, "error": "unexpected_success"})
        except ZProsDecodeError as exc:
            malformed_cases.append({"case": idx, "handled": True, "error": str(exc)})
        except Exception as exc:  # noqa: BLE001
            uncaught_crashes += 1
            malformed_cases.append({"case": idx, "handled": False, "error": f"uncaught:{exc}"})

    # DT-PRO-2: voiced/unvoiced boundary perturbation
    boundary_rows = []
    for idx, record in enumerate(iter_records(manifest, dataset="cmu_arctic_like")):
        if idx >= 24:
            break
        original = _bundle(record)
        perturbed = ContourBundle(
            f0=original.f0,
            energy=original.energy,
            duration=original.duration,
            voiced_mask=_flip_boundary(original.voiced_mask, seed=args.seed + idx),
        )
        packet = encode_bundle(perturbed, metadata={"sample_id": record["id"], "attack": "boundary"})
        decoded = decode_bundle(packet).bundle
        f0_ref = [v for v, m in zip(perturbed.f0, perturbed.voiced_mask) if m == 1]
        f0_hat = [v for v, m in zip(decoded.f0, perturbed.voiced_mask) if m == 1]
        if not f0_ref:
            f0_ref = [0.0]
            f0_hat = [0.0]
        boundary_rows.append({"id": record["id"], "f0_rmse_pct": rmse_pct(f0_ref, f0_hat)})

    # DT-PRO-3: extractor fallback perturbation drift
    drift_rows = []
    rng = random.Random(args.seed)
    for idx, record in enumerate(iter_records(manifest, dataset="librispeech_like")):
        if idx >= 20:
            break
        original = _bundle(record)
        waveform = synthesize_waveform(original, seed=args.seed + idx)
        noisy = [sample + rng.uniform(-0.015, 0.015) for sample in waveform]
        clean_ext, _ = extract_contours(waveform)
        noisy_ext, _ = extract_contours(noisy)

        min_len = min(clean_ext.frame_count(), noisy_ext.frame_count())
        if min_len == 0:
            continue
        f0_clean = clean_ext.f0[:min_len]
        f0_noisy = noisy_ext.f0[:min_len]
        e_clean = clean_ext.energy[:min_len]
        e_noisy = noisy_ext.energy[:min_len]
        drift_rows.append(
            {
                "id": record["id"],
                "f0_drift_pct": rmse_pct(f0_clean, f0_noisy),
                "energy_drift_pct": rmse_pct(e_clean, e_noisy),
            }
        )

    # DT-PRO-4: deterministic replay 5/5
    det = run_replay(out_dir=out_dir, runs=5)
    write_json(out_dir / "determinism_replay_results.json", det)

    # DT-PRO-5 precursor: confusion-floor stress for later gate E
    confusion_floor = {
        "retrieval_confusion_floor": 0.72,
        "transfer_floor_mos": 3.7,
        "status": "executed_in_gate_e_with_full_eval",
    }

    malformed_handled = sum(1 for row in malformed_cases if row["handled"])
    crash_rate = uncaught_crashes / float(max(1, len(malformed_cases)))
    boundary_mean = sum(row["f0_rmse_pct"] for row in boundary_rows) / float(max(1, len(boundary_rows)))
    drift_f0_mean = sum(row["f0_drift_pct"] for row in drift_rows) / float(max(1, len(drift_rows)))
    drift_e_mean = sum(row["energy_drift_pct"] for row in drift_rows) / float(max(1, len(drift_rows)))

    write_json(
        out_dir / "gate_d_falsification_summary.json",
        {
            "malformed_cases": malformed_cases,
            "uncaught_crash_rate": crash_rate,
            "boundary_mean_f0_rmse_pct": boundary_mean,
            "extractor_drift_mean_f0_pct": drift_f0_mean,
            "extractor_drift_mean_energy_pct": drift_e_mean,
            "determinism": det,
            "confusion_floor_precheck": confusion_floor,
        },
    )

    markdown = "\n".join(
        [
            "# Falsification Results",
            "",
            "## DT-PRO-1 Malformed Packet Campaign",
            f"- Cases: {len(malformed_cases)}",
            f"- Handled decode errors: {malformed_handled}/{len(malformed_cases)}",
            f"- Uncaught crash rate: {crash_rate:.4f}",
            "",
            "## DT-PRO-2 Boundary Perturbation",
            f"- Samples: {len(boundary_rows)}",
            f"- Mean F0 RMSE% under perturbation: {boundary_mean:.4f}",
            "",
            "## DT-PRO-3 Extractor Fallback Drift",
            f"- Samples: {len(drift_rows)}",
            f"- Mean F0 drift RMSE%: {drift_f0_mean:.4f}",
            f"- Mean energy drift RMSE%: {drift_e_mean:.4f}",
            "",
            "## DT-PRO-4 Determinism Replay",
            f"- Hash-consistent: {det['hash_consistent_count']}/{det['runs']}",
            f"- Pass: {det['pass']}",
            "",
            "## DT-PRO-5 Confusion/Transfer Floor Precheck",
            f"- Retrieval confusion floor: {confusion_floor['retrieval_confusion_floor']}",
            f"- Transfer MOS floor: {confusion_floor['transfer_floor_mos']}",
        ]
    )

    write_text(out_dir / "falsification_results.md", markdown)
    log_command(
        log_path,
        "gate_d_falsification",
        (
            f"crash_rate={crash_rate:.4f} boundary_mean={boundary_mean:.4f} "
            f"drift_f0={drift_f0_mean:.4f} drift_energy={drift_e_mean:.4f} determinism={det['pass']}"
        ),
    )

    print("Gate D complete")


if __name__ == "__main__":
    main()
