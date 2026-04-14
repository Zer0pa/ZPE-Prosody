"""Deterministic .zpros encoder/decoder with robust malformed handling."""

from __future__ import annotations

import json
import struct
import zlib
from typing import Dict, Iterable, List, Tuple

from zpe_prosody.constants import (
    CHANNEL_IDS,
    CHANNEL_ORDER,
    CHANNEL_STEPS,
    CHANNEL_STRIDES,
    PACKET_MAGIC,
    PACKET_VERSION,
)
from zpe_prosody.models import ContourBundle, DecodeResult


class ZProsDecodeError(Exception):
    """Raised when packet parsing fails in a structured, catchable way."""


def _zigzag_encode(value: int) -> int:
    return value * 2 if value >= 0 else (-value * 2) - 1


def _zigzag_decode(value: int) -> int:
    return value // 2 if value % 2 == 0 else -((value + 1) // 2)


def _encode_varint(value: int) -> bytes:
    if value < 0:
        raise ValueError("Varint cannot encode negative values")
    out = bytearray()
    while True:
        chunk = value & 0x7F
        value >>= 7
        if value:
            out.append(chunk | 0x80)
        else:
            out.append(chunk)
            break
    return bytes(out)


def _decode_varint(blob: bytes, offset: int) -> Tuple[int, int]:
    value = 0
    shift = 0
    idx = offset
    while idx < len(blob):
        byte = blob[idx]
        value |= (byte & 0x7F) << shift
        idx += 1
        if (byte & 0x80) == 0:
            return value, idx
        shift += 7
        if shift > 63:
            raise ZProsDecodeError("Varint overflow")
    raise ZProsDecodeError("Unexpected EOF while reading varint")


def _rle_encode(values: Iterable[int]) -> List[Tuple[int, int]]:
    values = list(values)
    if not values:
        return []
    runs: List[Tuple[int, int]] = []
    current = values[0]
    count = 1
    for value in values[1:]:
        if value == current and count < 1_000_000:
            count += 1
            continue
        runs.append((current, count))
        current = value
        count = 1
    runs.append((current, count))
    return runs


def _rle_decode(runs: Iterable[Tuple[int, int]], expected_len: int) -> List[int]:
    out: List[int] = []
    for value, count in runs:
        if count <= 0:
            raise ZProsDecodeError("Invalid run length")
        out.extend([value] * count)
        if len(out) > expected_len:
            raise ZProsDecodeError("Run exceeds expected length")
    if len(out) != expected_len:
        raise ZProsDecodeError("Decoded run length mismatch")
    return out


def _pack_channel(values: List[float], step: float, stride: int) -> bytes:
    if stride > 1:
        return _pack_channel_keyframes(values, step, stride)
    return _pack_channel_delta(values, step)


def _pack_channel_delta(values: List[float], step: float) -> bytes:
    quant = [int(round(v / step)) for v in values]
    prev = 0
    deltas: List[int] = []
    for qv in quant:
        deltas.append(qv - prev)
        prev = qv
    runs = _rle_encode(deltas)

    raw = bytearray()
    raw.append(0)  # delta-rle mode
    raw.extend(struct.pack("<I", len(values)))
    raw.extend(struct.pack("<f", float(step)))
    raw.extend(_encode_varint(len(runs)))
    for delta, count in runs:
        raw.extend(_encode_varint(_zigzag_encode(delta)))
        raw.extend(_encode_varint(count))
    return zlib.compress(bytes(raw), level=9)


def _pack_channel_keyframes(values: List[float], step: float, stride: int) -> bytes:
    quant = [int(round(v / step)) for v in values]
    if not quant:
        raw = bytearray()
        raw.append(1)
        raw.extend(struct.pack("<I", 0))
        raw.extend(struct.pack("<f", float(step)))
        raw.extend(struct.pack("<H", max(1, stride)))
        raw.extend(_encode_varint(0))
        return zlib.compress(bytes(raw), level=9)

    positions = list(range(0, len(quant), stride))
    if positions[-1] != len(quant) - 1:
        positions.append(len(quant) - 1)
    keys = [quant[pos] for pos in positions]

    raw = bytearray()
    raw.append(1)  # keyframe-interpolation mode
    raw.extend(struct.pack("<I", len(values)))
    raw.extend(struct.pack("<f", float(step)))
    raw.extend(struct.pack("<H", max(1, stride)))
    raw.extend(_encode_varint(len(keys)))

    prev = 0
    for value in keys:
        raw.extend(_encode_varint(_zigzag_encode(value - prev)))
        prev = value
    return zlib.compress(bytes(raw), level=9)


def _unpack_channel(blob: bytes) -> List[float]:
    try:
        raw = zlib.decompress(blob)
    except zlib.error as exc:
        raise ZProsDecodeError(f"Channel decompression failed: {exc}") from exc

    if len(raw) < 9:
        raise ZProsDecodeError("Channel payload too short")

    mode = raw[0]
    expected_len = struct.unpack("<I", raw[1:5])[0]
    step = struct.unpack("<f", raw[5:9])[0]
    if expected_len == 0:
        return []

    if mode == 0:
        offset = 9
        run_count, offset = _decode_varint(raw, offset)
        runs: List[Tuple[int, int]] = []
        for _ in range(run_count):
            zzd, offset = _decode_varint(raw, offset)
            count, offset = _decode_varint(raw, offset)
            runs.append((_zigzag_decode(zzd), count))

        deltas = _rle_decode(runs, expected_len)
        quant: List[int] = []
        prev = 0
        for delta in deltas:
            value = prev + delta
            quant.append(value)
            prev = value
    elif mode == 1:
        if len(raw) < 11:
            raise ZProsDecodeError("Keyframe payload too short")
        stride = struct.unpack("<H", raw[9:11])[0]
        stride = max(1, stride)
        offset = 11
        key_count, offset = _decode_varint(raw, offset)
        keys: List[int] = []
        prev = 0
        for _ in range(key_count):
            zzd, offset = _decode_varint(raw, offset)
            prev = prev + _zigzag_decode(zzd)
            keys.append(prev)
        if not keys:
            return [0.0] * expected_len

        positions = list(range(0, expected_len, stride))
        if positions[-1] != expected_len - 1:
            positions.append(expected_len - 1)
        if len(positions) != len(keys):
            raise ZProsDecodeError("Keyframe count/position mismatch")

        quant = [0] * expected_len
        for idx in range(len(positions) - 1):
            start = positions[idx]
            end = positions[idx + 1]
            v0 = keys[idx]
            v1 = keys[idx + 1]
            span = end - start
            if span <= 0:
                quant[start] = v0
                continue
            for pos in range(start, end + 1):
                t = (pos - start) / float(span)
                quant[pos] = int(round(v0 + (v1 - v0) * t))
    else:
        raise ZProsDecodeError(f"Unknown channel coding mode {mode}")

    return [qv * step for qv in quant]


def _pack_voiced_mask(mask: List[int]) -> bytes:
    if not mask:
        return zlib.compress(struct.pack("<I", 0), level=9)
    runs = _rle_encode(mask)
    raw = bytearray()
    raw.extend(struct.pack("<I", len(mask)))
    raw.append(1 if mask[0] else 0)
    raw.extend(_encode_varint(len(runs)))
    for value, count in runs:
        raw.append(1 if value else 0)
        raw.extend(_encode_varint(count))
    return zlib.compress(bytes(raw), level=9)


def _unpack_voiced_mask(blob: bytes) -> List[int]:
    try:
        raw = zlib.decompress(blob)
    except zlib.error as exc:
        raise ZProsDecodeError(f"Mask decompression failed: {exc}") from exc

    if len(raw) < 4:
        raise ZProsDecodeError("Mask payload too short")
    expected_len = struct.unpack("<I", raw[0:4])[0]
    if expected_len == 0:
        return []
    if len(raw) < 6:
        raise ZProsDecodeError("Mask payload too short")
    offset = 5
    run_count, offset = _decode_varint(raw, offset)
    runs: List[Tuple[int, int]] = []
    for _ in range(run_count):
        if offset >= len(raw):
            raise ZProsDecodeError("Mask payload truncated")
        value = 1 if raw[offset] else 0
        offset += 1
        count, offset = _decode_varint(raw, offset)
        runs.append((value, count))
    return _rle_decode(runs, expected_len)


def encode_bundle(bundle: ContourBundle, metadata: Dict[str, object] | None = None) -> bytes:
    frame_count = bundle.frame_count()
    if not (len(bundle.energy) == len(bundle.duration) == len(bundle.voiced_mask) == frame_count):
        raise ValueError("Contour channel length mismatch")

    channel_payloads: Dict[str, bytes] = {}
    for channel in CHANNEL_ORDER:
        step = CHANNEL_STEPS[channel]
        stride = CHANNEL_STRIDES.get(channel, 1)
        values = getattr(bundle, channel)
        channel_payloads[channel] = _pack_channel(values, step, stride)
    channel_payloads["voiced_mask"] = _pack_voiced_mask(bundle.voiced_mask)

    meta = dict(metadata) if metadata else {}
    meta_bytes = json.dumps(meta, sort_keys=True, separators=(",", ":")).encode("utf-8")

    payload = bytearray()
    for name in list(CHANNEL_ORDER) + ["voiced_mask"]:
        channel_blob = channel_payloads[name]
        payload.append(CHANNEL_IDS[name])
        payload.extend(struct.pack("<I", len(channel_blob)))
        payload.extend(channel_blob)
    payload_bytes = bytes(payload)

    crc = zlib.crc32(payload_bytes)
    packet = bytearray()
    packet.extend(PACKET_MAGIC)
    packet.append(PACKET_VERSION)
    packet.extend(struct.pack("<I", len(meta_bytes)))
    packet.extend(struct.pack("<I", len(payload_bytes)))
    packet.extend(struct.pack("<I", crc))
    packet.extend(meta_bytes)
    packet.extend(payload_bytes)
    return bytes(packet)


def decode_bundle(packet: bytes) -> DecodeResult:
    if len(packet) < 17:
        raise ZProsDecodeError("Packet too short")
    if packet[0:4] != PACKET_MAGIC:
        raise ZProsDecodeError("Bad magic")
    version = packet[4]
    if version != PACKET_VERSION:
        raise ZProsDecodeError(f"Unsupported version {version}")

    meta_len = struct.unpack("<I", packet[5:9])[0]
    payload_len = struct.unpack("<I", packet[9:13])[0]
    crc_expected = struct.unpack("<I", packet[13:17])[0]

    if len(packet) < 17 + meta_len + payload_len:
        raise ZProsDecodeError("Packet truncated")
    meta_start = 17
    meta_end = meta_start + meta_len
    payload_end = meta_end + payload_len

    try:
        metadata = json.loads(packet[meta_start:meta_end].decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ZProsDecodeError(f"Metadata decode failed: {exc}") from exc

    payload = packet[meta_end:payload_end]
    crc_observed = zlib.crc32(payload)
    if crc_expected != crc_observed:
        raise ZProsDecodeError("Payload CRC mismatch")

    channels_by_id = {value: key for key, value in CHANNEL_IDS.items()}
    channel_data: Dict[str, bytes] = {}
    offset = 0
    while offset < len(payload):
        if offset + 5 > len(payload):
            raise ZProsDecodeError("Payload channel header truncated")
        channel_id = payload[offset]
        channel_len = struct.unpack("<I", payload[offset + 1 : offset + 5])[0]
        offset += 5
        if offset + channel_len > len(payload):
            raise ZProsDecodeError("Payload channel body truncated")
        name = channels_by_id.get(channel_id)
        if not name:
            raise ZProsDecodeError(f"Unknown channel id {channel_id}")
        channel_data[name] = payload[offset : offset + channel_len]
        offset += channel_len

    required = list(CHANNEL_ORDER) + ["voiced_mask"]
    for item in required:
        if item not in channel_data:
            raise ZProsDecodeError(f"Missing channel: {item}")

    f0 = _unpack_channel(channel_data["f0"])
    energy = _unpack_channel(channel_data["energy"])
    duration = _unpack_channel(channel_data["duration"])
    voiced_mask = _unpack_voiced_mask(channel_data["voiced_mask"])

    if not (len(f0) == len(energy) == len(duration) == len(voiced_mask)):
        raise ZProsDecodeError("Decoded channel length mismatch")

    bundle = ContourBundle(f0=f0, energy=energy, duration=duration, voiced_mask=voiced_mask)
    return DecodeResult(bundle=bundle, metadata=metadata)


def encoded_channel_sizes(packet: bytes) -> Dict[str, int]:
    """Returns compressed per-channel byte sizes from a packet."""
    if len(packet) < 17 or packet[0:4] != PACKET_MAGIC:
        return {}
    meta_len = struct.unpack("<I", packet[5:9])[0]
    payload_len = struct.unpack("<I", packet[9:13])[0]
    payload = packet[17 + meta_len : 17 + meta_len + payload_len]
    offset = 0
    channels_by_id = {value: key for key, value in CHANNEL_IDS.items()}
    sizes: Dict[str, int] = {}
    while offset + 5 <= len(payload):
        channel_id = payload[offset]
        channel_len = struct.unpack("<I", payload[offset + 1 : offset + 5])[0]
        offset += 5
        sizes[channels_by_id.get(channel_id, f"unknown_{channel_id}")] = channel_len
        offset += channel_len
    return sizes
