"""Evaluation metrics for fidelity, latency, and ranking."""

from __future__ import annotations

from typing import Iterable, List

from zpe_prosody.models import ContourBundle
from zpe_prosody.utils import mean


def rmse(a: Iterable[float], b: Iterable[float]) -> float:
    left = list(a)
    right = list(b)
    if len(left) != len(right):
        raise ValueError("Length mismatch in RMSE")
    if not left:
        return 0.0
    mse = sum((x - y) ** 2 for x, y in zip(left, right)) / float(len(left))
    return mse ** 0.5


def rmse_pct(reference: Iterable[float], observed: Iterable[float]) -> float:
    ref = list(reference)
    obs = list(observed)
    if len(ref) != len(obs):
        raise ValueError("Length mismatch in RMSE%")
    if not ref:
        return 0.0
    baseline = max(abs(v) for v in ref)
    if baseline == 0:
        baseline = 1.0
    return (rmse(ref, obs) / baseline) * 100.0


def voiced_only(values: List[float], mask: List[int]) -> List[float]:
    return [v for v, m in zip(values, mask) if m == 1]


def contour_metrics(original: ContourBundle, reconstructed: ContourBundle) -> dict:
    f0_ref = voiced_only(original.f0, original.voiced_mask)
    f0_hat = voiced_only(reconstructed.f0, original.voiced_mask)
    e_ref = original.energy
    e_hat = reconstructed.energy
    return {
        "f0_rmse": rmse(f0_ref, f0_hat),
        "f0_rmse_pct": rmse_pct(f0_ref, f0_hat),
        "energy_rmse": rmse(e_ref, e_hat),
        "energy_rmse_pct": rmse_pct(e_ref, e_hat),
        "frames": original.frame_count(),
    }


def aggregate_metric(rows: List[dict], key: str) -> float:
    return mean(row.get(key, 0.0) for row in rows)


def compression_ratio(raw_bytes: int, encoded_bytes: int) -> float:
    if encoded_bytes <= 0:
        return 0.0
    return raw_bytes / float(encoded_bytes)


def percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = int(round((len(ordered) - 1) * pct))
    return ordered[max(0, min(len(ordered) - 1, idx))]
