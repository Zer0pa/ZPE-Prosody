"""Integration-ready API layer.

Uses FastAPI when available, otherwise provides an equivalent in-process service
contract used by gate validation.
"""

from __future__ import annotations

import base64
import importlib.util
from dataclasses import dataclass
from typing import Dict, List

from zpe_prosody.codec import decode_bundle, encode_bundle
from zpe_prosody.models import ContourBundle
from zpe_prosody.retrieval import build_embedding, cosine_similarity
from zpe_prosody.transfer import apply_transfer


@dataclass
class APICapability:
    framework: str
    endpoints: List[str]
    openapi_available: bool


def capability() -> APICapability:
    has_fastapi = importlib.util.find_spec("fastapi") is not None
    if has_fastapi:
        return APICapability(
            framework="fastapi",
            endpoints=["/encode", "/decode", "/search", "/transfer"],
            openapi_available=True,
        )
    return APICapability(
        framework="equivalent_inprocess_service",
        endpoints=["/encode", "/decode", "/search", "/transfer"],
        openapi_available=False,
    )


def encode_payload(bundle_dict: Dict[str, List[float]]) -> Dict[str, str]:
    bundle = ContourBundle(
        f0=list(bundle_dict["f0"]),
        energy=list(bundle_dict["energy"]),
        duration=list(bundle_dict["duration"]),
        voiced_mask=[int(v) for v in bundle_dict["voiced_mask"]],
    )
    packet = encode_bundle(bundle=bundle, metadata={"api": True})
    return {"packet_b64": base64.b64encode(packet).decode("ascii")}


def decode_payload(packet_b64: str) -> Dict[str, object]:
    packet = base64.b64decode(packet_b64.encode("ascii"))
    decoded = decode_bundle(packet)
    return {
        "bundle": decoded.bundle.as_dict(),
        "metadata": decoded.metadata,
    }


def search_payload(query: Dict[str, List[float]], candidates: Dict[str, Dict[str, List[float]]]) -> Dict[str, object]:
    query_bundle = ContourBundle(
        f0=query["f0"],
        energy=query["energy"],
        duration=query["duration"],
        voiced_mask=[int(v) for v in query["voiced_mask"]],
    )
    query_emb = build_embedding(query_bundle)
    scored = []
    for item_id, item_bundle in candidates.items():
        candidate = ContourBundle(
            f0=item_bundle["f0"],
            energy=item_bundle["energy"],
            duration=item_bundle["duration"],
            voiced_mask=[int(v) for v in item_bundle["voiced_mask"]],
        )
        score = cosine_similarity(query_emb, build_embedding(candidate))
        scored.append({"id": item_id, "score": score})
    scored.sort(key=lambda row: row["score"], reverse=True)
    return {"results": scored}


def transfer_payload(source: Dict[str, List[float]], target_frames: int) -> Dict[str, object]:
    source_bundle = ContourBundle(
        f0=source["f0"],
        energy=source["energy"],
        duration=source["duration"],
        voiced_mask=[int(v) for v in source["voiced_mask"]],
    )
    transferred = apply_transfer(source_bundle, target_frames=target_frames)
    return {"bundle": transferred.as_dict()}


def build_fastapi_app():
    """Optional FastAPI app, created only when dependency exists."""
    if importlib.util.find_spec("fastapi") is None:
        return None
    from fastapi import FastAPI

    app = FastAPI(title="zpe-prosody", version="0.1.0")

    @app.post("/encode")
    def encode_route(payload: Dict[str, Dict[str, List[float]]]):
        return encode_payload(payload["bundle"])

    @app.post("/decode")
    def decode_route(payload: Dict[str, str]):
        return decode_payload(payload["packet_b64"])

    @app.post("/search")
    def search_route(payload: Dict[str, object]):
        return search_payload(payload["query"], payload["candidates"])

    @app.post("/transfer")
    def transfer_route(payload: Dict[str, object]):
        return transfer_payload(payload["source"], int(payload["target_frames"]))

    return app
