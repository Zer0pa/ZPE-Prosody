"""Dataclasses for prosody contours and evaluation records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ContourBundle:
    f0: List[float]
    energy: List[float]
    duration: List[float]
    voiced_mask: List[int]

    def frame_count(self) -> int:
        return len(self.f0)

    def as_dict(self) -> Dict[str, List[float]]:
        return {
            "f0": list(self.f0),
            "energy": list(self.energy),
            "duration": list(self.duration),
            "voiced_mask": list(self.voiced_mask),
        }


@dataclass
class DecodeResult:
    bundle: ContourBundle
    metadata: Dict[str, object]
