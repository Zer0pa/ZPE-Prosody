"""Shared helpers for gate scripts."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zpe_prosody.constants import GLOBAL_SEED  # noqa: E402
from zpe_prosody.utils import append_text, ensure_dir, set_global_seed, write_json  # noqa: E402


def parse_args(description: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--out", type=Path, required=True, help="Artifact output directory")
    parser.add_argument("--seed", type=int, default=GLOBAL_SEED)
    return parser.parse_args()


def init_environment(out_dir: Path, seed: int) -> Path:
    ensure_dir(out_dir)
    set_global_seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    return out_dir / "command_log.txt"


def log_command(log_path: Path, command_name: str, detail: str) -> None:
    timestamp = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    append_text(log_path, f"[{timestamp}] {command_name}: {detail}\n")


def write_json_artifact(out_dir: Path, filename: str, payload: Dict[str, Any]) -> None:
    write_json(out_dir / filename, payload)


def bootstrap_env(log_path: Path) -> Dict[str, Any]:
    """Bootstraps environment using startup contract with fallback parsing."""
    env_file = ROOT / ".env"
    result: Dict[str, Any] = {
        "env_file_exists": env_file.exists(),
        "source_attempted": True,
        "source_success": False,
        "source_error_signature": "",
        "fallback_parser_used": False,
        "loaded_keys": [],
    }

    if not env_file.exists():
        log_command(log_path, "env_bootstrap", "env file missing")
        return result

    source_cmd = "set -a; source .env; set +a; env"
    proc = subprocess.run(
        ["/bin/zsh", "-lc", source_cmd],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        result["source_success"] = True
        loaded = []
        for line in proc.stdout.splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key and key not in os.environ:
                os.environ[key] = value
            if key and key in {"HUGGINGFACE_HUB_TOKEN", "HF_TOKEN", "HF_HOME", "HF_HUB_ENABLE_HF_TRANSFER"}:
                loaded.append(key)
        result["loaded_keys"] = sorted(set(loaded))
        log_command(log_path, "env_bootstrap", f"source_success keys={result['loaded_keys']}")
        return result

    result["source_error_signature"] = (proc.stderr or proc.stdout).strip().splitlines()[0] if (proc.stderr or proc.stdout) else "unknown_source_failure"
    log_command(log_path, "env_bootstrap", f"source_failed signature={result['source_error_signature']}")

    # Fallback parser for .env files containing unquoted spaces.
    loaded_keys = []
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and ((value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")):
            value = value[1:-1]
        os.environ[key] = value
        loaded_keys.append(key)

    result["fallback_parser_used"] = True
    result["loaded_keys"] = sorted(loaded_keys)
    log_command(log_path, "env_bootstrap", f"fallback_parser_used keys={result['loaded_keys']}")
    return result
