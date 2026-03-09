"""Gate A: resource lock + deterministic fixture preparation."""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

from common import ROOT, bootstrap_env, init_environment, log_command, parse_args, write_json_artifact

if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from generate_fixtures import build_fixture_manifest  # noqa: E402


def _has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def _resource_item(
    name: str,
    source_reference: str,
    planned_usage: str,
    available: bool,
    substitution: str,
    comparability_impact: str,
) -> dict:
    return {
        "resource_name": name,
        "source_reference": source_reference,
        "planned_usage": planned_usage,
        "access_time_utc": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "availability": "AVAILABLE" if available else "UNAVAILABLE",
        "substitution": substitution,
        "comparability_impact": comparability_impact,
    }


def main() -> None:
    args = parse_args("Gate A resource lock")
    out_dir = args.out
    log_path = init_environment(out_dir, args.seed)
    log_command(log_path, "gate_a_lock", f"start seed={args.seed}")
    env_bootstrap = bootstrap_env(log_path)

    fixtures_dir = ROOT / "data" / "fixtures"
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    fixture_manifest = build_fixture_manifest(seed=args.seed)
    fixture_path = fixtures_dir / "manifest.json"
    with fixture_path.open("w", encoding="utf-8") as handle:
        json.dump(fixture_manifest, handle, indent=2, sort_keys=True)
    log_command(log_path, "gate_a_lock", f"fixtures generated path={fixture_path} count={fixture_manifest['record_count']}")

    libri_local = (ROOT / "data" / "external" / "librispeech").exists()
    ravdess_local = (ROOT / "data" / "external" / "ravdess").exists()
    arctic_local = (ROOT / "data" / "external" / "cmu_arctic").exists()

    resources = [
        _resource_item(
            name="torchcrepe_primary_f0",
            source_reference="https://github.com/maxrmorrison/torchcrepe",
            planned_usage="Primary F0 extractor baseline",
            available=_has_module("torchcrepe"),
            substitution="fallback_zero_crossing_rms_extractor",
            comparability_impact="Medium: fallback is deterministic but not deep-learning equivalent; affects external validity.",
        ),
        _resource_item(
            name="parselmouth_energy_duration",
            source_reference="https://github.com/YannickJadoul/Parselmouth",
            planned_usage="Energy and duration extraction baseline",
            available=_has_module("parselmouth"),
            substitution="fallback_rms_segment_duration_extractor",
            comparability_impact="Medium: algorithmic approximation may miss Praat-specific behaviors.",
        ),
        _resource_item(
            name="penn_comparator",
            source_reference="https://github.com/interactiveaudiolab/penn",
            planned_usage="Modern comparator for pitch extraction",
            available=_has_module("penn"),
            substitution="none (comparator retained as open item)",
            comparability_impact="High: no comparator run means upgrade claim remains inconclusive.",
        ),
        _resource_item(
            name="librispeech_dataset",
            source_reference="https://www.openslr.org/12",
            planned_usage="Compression/latency fidelity evaluation",
            available=libri_local,
            substitution="deterministic_librispeech_like_fixture_set",
            comparability_impact="Medium: contour distribution calibrated but provenance not identical.",
        ),
        _resource_item(
            name="ravdess_dataset",
            source_reference="https://zenodo.org/record/1188976",
            planned_usage="Emotion retrieval evaluation",
            available=ravdess_local,
            substitution="deterministic_ravdess_like_fixture_set",
            comparability_impact="Medium: emotional archetypes are synthetic proxies.",
        ),
        _resource_item(
            name="cmu_arctic_dataset",
            source_reference="http://www.festvox.org/cmu_arctic",
            planned_usage="F0 and energy fidelity evaluation",
            available=arctic_local,
            substitution="deterministic_cmu_arctic_like_fixture_set",
            comparability_impact="Medium: phonetic coverage approximated statistically.",
        ),
        _resource_item(
            name="coqui_xtts_bridge",
            source_reference="https://github.com/coqui-ai/TTS",
            planned_usage="Prosody transfer synthesis checks",
            available=_has_module("TTS"),
            substitution="objective_transfer_proxy_with_contour_mos",
            comparability_impact="High: no real TTS listening panel; MOS equivalence unproven.",
        ),
        _resource_item(
            name="fastapi_uvicorn_serving",
            source_reference="https://fastapi.tiangolo.com",
            planned_usage="Integration API serving path",
            available=_has_module("fastapi") and _has_module("uvicorn"),
            substitution="equivalent_inprocess_service_contract",
            comparability_impact="Low: endpoint semantics validated without runtime web server.",
        ),
    ]

    write_json_artifact(
        out_dir,
        "resource_lock.json",
        {
            "seed": args.seed,
            "env_bootstrap": env_bootstrap,
            "fixture_manifest": str(fixture_path),
            "resource_items": resources,
        },
    )
    log_command(log_path, "gate_a_lock", "resource_lock.json written")
    print(f"Gate A complete -> {out_dir / 'resource_lock.json'}")


if __name__ == "__main__":
    main()
