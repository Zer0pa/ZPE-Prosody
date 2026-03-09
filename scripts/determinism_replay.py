"""Determinism replay utility."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from common import ROOT, init_environment, log_command, write_json_artifact

SCRIPTS = ROOT / "scripts"
SRC = ROOT / "src"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fixture_lib import load_fixture_manifest
from zpe_prosody.codec import encode_bundle
from zpe_prosody.models import ContourBundle


def _bundle(record: dict) -> ContourBundle:
    b = record["bundle"]
    return ContourBundle(
        f0=[float(v) for v in b["f0"]],
        energy=[float(v) for v in b["energy"]],
        duration=[float(v) for v in b["duration"]],
        voiced_mask=[int(v) for v in b["voiced_mask"]],
    )


def run_replay(out_dir: Path, runs: int = 5) -> dict:
    manifest = load_fixture_manifest(ROOT / "data" / "fixtures" / "manifest.json")
    records = manifest["records"][:48]

    run_hashes = []
    for run_idx in range(runs):
        digest = hashlib.sha256()
        for record in records:
            bundle = _bundle(record)
            packet = encode_bundle(bundle, metadata={"sample_id": record["id"]})
            digest.update(packet)
        run_hashes.append(digest.hexdigest())

    baseline = run_hashes[0] if run_hashes else ""
    matches = [h == baseline for h in run_hashes]
    return {
        "runs": runs,
        "hashes": run_hashes,
        "hash_consistent_count": sum(1 for m in matches if m),
        "hash_consistent_required": runs,
        "pass": all(matches),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Determinism replay")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260220)
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()
    out_dir = args.out
    log_path = init_environment(out_dir, args.seed)

    result = run_replay(out_dir=out_dir, runs=args.runs)
    write_json_artifact(out_dir, "determinism_replay_results.json", result)
    log_command(log_path, "determinism_replay", f"pass={result['pass']} hashes={result['hashes']}")
    print(f"Determinism replay complete pass={result['pass']}")


if __name__ == "__main__":
    main()
