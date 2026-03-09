"""Prosody extraction and synthetic waveform helpers.

This module provides deterministic fallback extraction when external extractors
(torchcrepe/parselmouth/penn) are unavailable.
"""

from __future__ import annotations

import importlib.util
import math
import random
from typing import Dict, List, Tuple

from zpe_prosody.constants import DEFAULT_SAMPLE_RATE, FRAME_MS, FRAME_SAMPLES, GLOBAL_SEED
from zpe_prosody.models import ContourBundle


def resource_availability() -> Dict[str, bool]:
    return {
        "torchcrepe": importlib.util.find_spec("torchcrepe") is not None,
        "parselmouth": importlib.util.find_spec("parselmouth") is not None,
        "penn": importlib.util.find_spec("penn") is not None,
        "fastapi": importlib.util.find_spec("fastapi") is not None,
        "uvicorn": importlib.util.find_spec("uvicorn") is not None,
        "coqui_tts": importlib.util.find_spec("TTS") is not None,
    }


def _clamp(value: float, lower: float, upper: float) -> float:
    return lower if value < lower else upper if value > upper else value


def generate_prosody_contours(
    seed: int,
    frames: int,
    emotion: str = "neutral",
    speaker_bias: float = 0.0,
) -> ContourBundle:
    """Generates deterministic contour bundles with controllable emotion profiles."""
    rng = random.Random(seed)

    emotion_profiles = {
        "neutral": (0.9, 0.0, 0.0),
        "happy": (1.2, 0.4, 0.2),
        "sad": (0.7, -0.3, -0.1),
        "angry": (1.4, 0.2, 0.4),
        "fearful": (1.3, 0.5, -0.2),
        "disgust": (0.8, -0.2, 0.1),
        "surprised": (1.5, 0.7, 0.3),
        "calm": (0.75, -0.1, -0.2),
    }
    amp, slope, jitter = emotion_profiles.get(emotion, emotion_profiles["neutral"])

    base_f0 = 155.0 + 25.0 * speaker_bias + rng.uniform(-8.0, 8.0)
    f0: List[float] = []
    energy: List[float] = []
    voiced_mask: List[int] = []

    phase = rng.uniform(0.0, math.pi)
    for idx in range(frames):
        t = idx / float(max(1, frames - 1))
        # 3-state speech rhythm to avoid toy regularity.
        local = (idx + seed) % 41
        voiced = 0 if local in (0, 1, 2, 3, 22) else 1
        voiced_mask.append(voiced)

        phrase_shape = math.sin((2.0 * math.pi * 1.7 * t) + phase)
        micro = math.sin((2.0 * math.pi * 7.5 * t) + phase * 0.3)
        drift = slope * (t - 0.5)

        f0_val = base_f0 * (1.0 + 0.06 * amp * phrase_shape + 0.01 * micro + drift * 0.15)
        f0_val += rng.uniform(-0.45, 0.45) * max(0.15, abs(jitter))
        f0_val = _clamp(f0_val, 70.0, 360.0)

        energy_val = 0.52 + 0.22 * amp * math.sin((2.0 * math.pi * 0.9 * t) + phase * 0.7)
        energy_val += 0.12 * drift + rng.uniform(-0.008, 0.008)
        energy_val = _clamp(energy_val, 0.05, 1.0)

        if voiced == 0:
            f0.append(0.0)
            energy.append(energy_val * 0.35)
        else:
            f0.append(f0_val)
            energy.append(energy_val)

    duration: List[float] = [0.0] * frames
    start = 0
    while start < frames:
        state = voiced_mask[start]
        end = start + 1
        while end < frames and voiced_mask[end] == state:
            end += 1
        seg_ms = float((end - start) * FRAME_MS)
        for pos in range(start, end):
            duration[pos] = seg_ms
        start = end

    # Mild smoothing reduces spurious high-frequency jitter while preserving contour shape.
    if frames >= 3:
        for idx in range(1, frames - 1):
            if voiced_mask[idx] == 1:
                f0[idx] = (f0[idx - 1] + (2.0 * f0[idx]) + f0[idx + 1]) / 4.0
            energy[idx] = (energy[idx - 1] + (2.0 * energy[idx]) + energy[idx + 1]) / 4.0

    return ContourBundle(f0=f0, energy=energy, duration=duration, voiced_mask=voiced_mask)


def synthesize_waveform(
    bundle: ContourBundle,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    seed: int = GLOBAL_SEED,
) -> List[float]:
    """Synthesizes a waveform from contour bundle for deterministic extraction tests."""
    rng = random.Random(seed)
    dt = 1.0 / float(sample_rate)
    waveform: List[float] = []
    phase = 0.0

    for frame_idx in range(bundle.frame_count()):
        frame_energy = _clamp(bundle.energy[frame_idx], 0.0, 1.0)
        voiced = bundle.voiced_mask[frame_idx] == 1 and bundle.f0[frame_idx] > 0.0
        freq = _clamp(bundle.f0[frame_idx], 60.0, 420.0)

        for _ in range(FRAME_SAMPLES):
            if voiced:
                phase += 2.0 * math.pi * freq * dt
                sample = math.sin(phase)
                sample += 0.16 * math.sin(phase * 2.0)
                sample += rng.uniform(-0.015, 0.015)
            else:
                sample = rng.uniform(-0.06, 0.06)
            waveform.append(sample * frame_energy)
    return waveform


def _zero_crossing_f0(frame: List[float], sample_rate: int) -> float:
    if not frame:
        return 0.0
    crossings = 0
    prev = frame[0]
    for value in frame[1:]:
        if (prev < 0 <= value) or (prev > 0 >= value):
            crossings += 1
        prev = value
    freq = (crossings / 2.0) * (sample_rate / float(len(frame)))
    if 50.0 <= freq <= 450.0:
        return freq
    return 0.0


def extract_contours_fallback(
    waveform: List[float],
    sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> ContourBundle:
    """Fallback extractor using per-frame RMS + zero-crossing pitch estimate."""
    if not waveform:
        return ContourBundle(f0=[], energy=[], duration=[], voiced_mask=[])

    frame_size = int(sample_rate * FRAME_MS / 1000)
    frames = len(waveform) // frame_size
    f0: List[float] = []
    energy: List[float] = []
    voiced_mask: List[int] = []

    for idx in range(frames):
        start = idx * frame_size
        frame = waveform[start : start + frame_size]
        if not frame:
            break
        rms = math.sqrt(sum(v * v for v in frame) / float(len(frame)))
        hz = _zero_crossing_f0(frame, sample_rate)
        voiced = 1 if (rms > 0.045 and hz > 0.0) else 0

        energy.append(_clamp(rms * 2.6, 0.0, 1.0))
        voiced_mask.append(voiced)
        f0.append(hz if voiced else 0.0)

    duration = [0.0] * len(f0)
    start = 0
    while start < len(voiced_mask):
        state = voiced_mask[start]
        end = start + 1
        while end < len(voiced_mask) and voiced_mask[end] == state:
            end += 1
        seg_ms = float((end - start) * FRAME_MS)
        for pos in range(start, end):
            duration[pos] = seg_ms
        start = end

    return ContourBundle(f0=f0, energy=energy, duration=duration, voiced_mask=voiced_mask)


def extract_contours(
    waveform: List[float],
    sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> Tuple[ContourBundle, Dict[str, str]]:
    """Extractor facade with backend metadata for traceability."""
    available = resource_availability()
    # In this lane runtime, external libraries may be absent. Use deterministic fallback.
    bundle = extract_contours_fallback(waveform=waveform, sample_rate=sample_rate)
    meta = {
        "backend": "fallback_zero_crossing_rms",
        "torchcrepe_available": str(available["torchcrepe"]),
        "parselmouth_available": str(available["parselmouth"]),
        "penn_available": str(available["penn"]),
    }
    return bundle, meta
