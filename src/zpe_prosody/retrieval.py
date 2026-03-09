"""Similarity retrieval utilities for compressed prosody representations."""

from __future__ import annotations

import math
from typing import Dict, Iterable, List, Tuple

from zpe_prosody.models import ContourBundle
from zpe_prosody.utils import mean, stddev


def _slope(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    return (values[-1] - values[0]) / float(len(values) - 1)


def _norm(values: Iterable[float]) -> float:
    return math.sqrt(sum(v * v for v in values))


def cosine_similarity(left: List[float], right: List[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Cosine similarity length mismatch")
    denom = _norm(left) * _norm(right)
    if denom == 0.0:
        return 0.0
    return sum(a * b for a, b in zip(left, right)) / denom


def build_embedding(bundle: ContourBundle) -> List[float]:
    voiced_f0 = [v for v, m in zip(bundle.f0, bundle.voiced_mask) if m == 1 and v > 0.0]
    if not voiced_f0:
        voiced_f0 = [0.0]

    voiced_ratio = sum(bundle.voiced_mask) / float(max(1, len(bundle.voiced_mask)))
    emb = [
        mean(voiced_f0),
        stddev(voiced_f0),
        max(voiced_f0) - min(voiced_f0),
        _slope(voiced_f0),
        mean(bundle.energy),
        stddev(bundle.energy),
        max(bundle.energy) - min(bundle.energy),
        _slope(bundle.energy),
        mean(bundle.duration),
        stddev(bundle.duration),
        voiced_ratio,
        _slope(bundle.duration),
    ]
    return emb


def rank_neighbors(
    query_id: str,
    embeddings: Dict[str, List[float]],
    top_k: int = 5,
) -> List[Tuple[str, float]]:
    query = embeddings[query_id]
    scored = []
    for item_id, item_emb in embeddings.items():
        if item_id == query_id:
            continue
        score = cosine_similarity(query, item_emb)
        scored.append((item_id, score))
    scored.sort(key=lambda row: row[1], reverse=True)
    return scored[:top_k]


def precision_at_k(
    query_id: str,
    labels: Dict[str, str],
    embeddings: Dict[str, List[float]],
    top_k: int = 5,
) -> float:
    ranked = rank_neighbors(query_id=query_id, embeddings=embeddings, top_k=top_k)
    if not ranked:
        return 0.0
    target = labels[query_id]
    hits = sum(1 for item_id, _ in ranked if labels.get(item_id) == target)
    return hits / float(top_k)


def mean_precision_at_k(
    labels: Dict[str, str],
    embeddings: Dict[str, List[float]],
    top_k: int = 5,
) -> float:
    if not labels:
        return 0.0
    scores = [
        precision_at_k(query_id=item_id, labels=labels, embeddings=embeddings, top_k=top_k)
        for item_id in labels
    ]
    return sum(scores) / float(len(scores))
