"""Utility helpers for deterministic execution and filesystem IO."""

from __future__ import annotations

import hashlib
import json
import os
import random
from pathlib import Path
from typing import Any, Dict, Iterable

from zpe_prosody.constants import GLOBAL_SEED


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as handle:
        handle.write(content)


def append_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(content)


def sha256_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(1 << 16)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def set_global_seed(seed: int = GLOBAL_SEED) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)


def mean(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / float(len(values))


def variance(values: Iterable[float]) -> float:
    values = list(values)
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return sum((v - m) * (v - m) for v in values) / float(len(values))


def stddev(values: Iterable[float]) -> float:
    return variance(values) ** 0.5
