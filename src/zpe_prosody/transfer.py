"""Prosody transfer helpers and deterministic MOS proxy scoring."""

from __future__ import annotations

from typing import List

from zpe_prosody.eval import rmse_pct
from zpe_prosody.models import ContourBundle


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def resample_series(values: List[float], target_len: int) -> List[float]:
    if target_len <= 0:
        return []
    if not values:
        return [0.0] * target_len
    if len(values) == 1:
        return [values[0]] * target_len

    out: List[float] = []
    scale = (len(values) - 1) / float(max(1, target_len - 1))
    for idx in range(target_len):
        pos = idx * scale
        left = int(pos)
        right = min(left + 1, len(values) - 1)
        frac = pos - left
        out.append(_lerp(values[left], values[right], frac))
    return out


def apply_transfer(source: ContourBundle, target_frames: int) -> ContourBundle:
    f0 = resample_series(source.f0, target_frames)
    energy = resample_series(source.energy, target_frames)
    duration = resample_series(source.duration, target_frames)
    voiced_float = resample_series([float(v) for v in source.voiced_mask], target_frames)
    voiced_mask = [1 if v >= 0.5 else 0 for v in voiced_float]
    return ContourBundle(f0=f0, energy=energy, duration=duration, voiced_mask=voiced_mask)


def mos_proxy(reference: ContourBundle, candidate: ContourBundle) -> float:
    """Maps objective contour error to a deterministic MOS-like 1..5 score."""
    target_len = reference.frame_count()
    if candidate.frame_count() != target_len:
        candidate = apply_transfer(candidate, target_len)

    f0_ref = [v for v, m in zip(reference.f0, reference.voiced_mask) if m == 1]
    f0_hat = [v for v, m in zip(candidate.f0, reference.voiced_mask) if m == 1]
    if not f0_ref:
        f0_ref = [0.0]
        f0_hat = [0.0]

    f0_pct = rmse_pct(f0_ref, f0_hat)
    e_pct = rmse_pct(reference.energy, candidate.energy)
    mask_diff = sum(1 for a, b in zip(reference.voiced_mask, candidate.voiced_mask) if a != b)
    mask_penalty = 0.4 * (mask_diff / float(max(1, target_len)))

    score = 5.0 - (0.08 * f0_pct) - (0.10 * e_pct) - mask_penalty
    if score < 1.0:
        return 1.0
    if score > 5.0:
        return 5.0
    return score
