"""Shared constants for ZPE prosody lane."""

GLOBAL_SEED = 20260220
DEFAULT_SAMPLE_RATE = 16_000
FRAME_MS = 10
FRAME_SAMPLES = DEFAULT_SAMPLE_RATE * FRAME_MS // 1000

CHANNEL_ORDER = ("f0", "energy", "duration")
CHANNEL_IDS = {"f0": 1, "energy": 2, "duration": 3, "voiced_mask": 4}
CHANNEL_STEPS = {
    "f0": 5.0,
    "energy": 0.05,
    "duration": 10.0,
}

CHANNEL_STRIDES = {
    "f0": 1,
    "energy": 1,
    "duration": 1,
}

PACKET_MAGIC = b"ZPRS"
PACKET_VERSION = 1

CLAIM_THRESHOLDS = {
    "compression_ratio": 15.0,
    "f0_rmse_pct": 5.0,
    "energy_rmse_pct": 3.0,
    "encode_ms": 50.0,
    "transfer_mos": 4.0,
    "retrieval_p_at_5": 0.80,
}
