"""Validates threshold files emitted by Gate C."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from common import init_environment, log_command, parse_args, write_json_artifact


def _read(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    args = parse_args("Validate gate C thresholds")
    out_dir = args.out
    log_path = init_environment(out_dir, args.seed)

    compression = _read(out_dir / "prosody_compression_benchmark.json")
    f0 = _read(out_dir / "prosody_f0_fidelity.json")
    energy = _read(out_dir / "prosody_energy_fidelity.json")
    latency = _read(out_dir / "prosody_latency_benchmark.json")

    checks = {
        "PRO-C001": bool(compression.get("pass")),
        "PRO-C002": bool(f0.get("pass")),
        "PRO-C003": bool(energy.get("pass")),
        "PRO-C004": bool(latency.get("pass")),
    }
    overall = all(checks.values())

    write_json_artifact(
        out_dir,
        "gate_c_threshold_validation.json",
        {
            "checks": checks,
            "overall_pass": overall,
        },
    )
    log_command(log_path, "validate_thresholds", f"overall_pass={overall}")
    if not overall:
        sys.exit(1)


if __name__ == "__main__":
    main()
