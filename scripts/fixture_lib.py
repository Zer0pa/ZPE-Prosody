"""Fixture loading helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List


def load_fixture_manifest(path: Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iter_records(manifest: Dict[str, object], dataset: str | None = None) -> Iterable[dict]:
    for record in manifest.get("records", []):
        if dataset is None or record.get("dataset") == dataset:
            yield record


def by_id(manifest: Dict[str, object]) -> Dict[str, dict]:
    return {record["id"]: record for record in manifest.get("records", [])}


def labels(manifest: Dict[str, object], dataset: str | None = None) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for record in iter_records(manifest, dataset=dataset):
        out[record["id"]] = record.get("label", "unknown")
    return out
