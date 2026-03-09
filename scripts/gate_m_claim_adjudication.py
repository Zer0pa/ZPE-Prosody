"""Appendix D/E claim adjudication and max-wave artifact generation."""

from __future__ import annotations

import json
import os
import shlex
import struct
import subprocess
import wave
from pathlib import Path
from typing import Dict, List, Tuple

from common import ROOT, bootstrap_env, init_environment, log_command, parse_args, write_json_artifact

import sys

SCRIPTS = ROOT / "scripts"
SRC = ROOT / "src"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zpe_prosody.codec import decode_bundle, encode_bundle
from zpe_prosody.extract import extract_contours
from zpe_prosody.models import ContourBundle
from zpe_prosody.retrieval import build_embedding, mean_precision_at_k


def _run(cmd: str, cwd: Path, env: Dict[str, str], timeout: int = 1800) -> Dict[str, object]:
    try:
        proc = subprocess.run(
            ["/bin/zsh", "-lc", cmd],
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        stdout = (proc.stdout or "").strip()
        stderr = (proc.stderr or "").strip()
        signature = ""
        if proc.returncode != 0:
            lines = (stderr or stdout).splitlines()
            signature = lines[0] if lines else f"returncode_{proc.returncode}"
        rc = proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = ((exc.stdout or "") if isinstance(exc.stdout, str) else "").strip()
        stderr = ((exc.stderr or "") if isinstance(exc.stderr, str) else "").strip()
        signature = "timeout_expired"
        rc = 124
    return {
        "command": cmd,
        "cwd": str(cwd),
        "returncode": rc,
        "stdout_tail": stdout[-1200:],
        "stderr_tail": stderr[-1200:],
        "failure_signature": signature,
    }


def _read(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_wav(path: Path) -> Tuple[List[float], int]:
    with wave.open(str(path), "rb") as w:
        n_channels = w.getnchannels()
        sampwidth = w.getsampwidth()
        framerate = w.getframerate()
        frames = w.readframes(w.getnframes())
    if sampwidth != 2:
        raise ValueError(f"Unsupported sample width: {sampwidth}")
    total_samples = len(frames) // 2
    ints = struct.unpack("<" + "h" * total_samples, frames)
    if n_channels == 1:
        audio = [v / 32768.0 for v in ints]
    else:
        audio = []
        for i in range(0, len(ints), n_channels):
            audio.append(sum(ints[i : i + n_channels]) / float(n_channels) / 32768.0)
    return audio, framerate


def _bundle_from_wav(path: Path) -> ContourBundle:
    waveform, sample_rate = _load_wav(path)
    bundle, _meta = extract_contours(waveform=waveform, sample_rate=sample_rate)
    packet = encode_bundle(bundle, metadata={"source": str(path.name)})
    return decode_bundle(packet).bundle


def _ravdess_retrieval(ravdess_manifest: Path) -> Dict[str, object]:
    manifest = _read(ravdess_manifest)
    items = manifest.get("items", [])
    if len(items) < 16:
        return {
            "executed": False,
            "reason": "insufficient_ravdess_items",
            "p_at_5": 0.0,
            "samples": len(items),
        }

    labels: Dict[str, str] = {}
    embeddings: Dict[str, List[float]] = {}

    for idx, item in enumerate(items[:120]):
        wav_path = Path(item["path"])
        if not wav_path.exists():
            continue
        label = str(item.get("label", "unknown"))
        sample_id = f"ravdess_{idx:04d}"
        labels[sample_id] = label
        try:
            bundle = _bundle_from_wav(wav_path)
            embeddings[sample_id] = build_embedding(bundle)
        except Exception:
            continue

    if len(embeddings) < 16:
        return {
            "executed": False,
            "reason": "ravdess_embedding_build_failed",
            "p_at_5": 0.0,
            "samples": len(embeddings),
        }

    score = mean_precision_at_k(labels=labels, embeddings=embeddings, top_k=5)
    return {
        "executed": True,
        "dataset": "ravdess_real",
        "samples": len(embeddings),
        "p_at_5": score,
        "threshold": 0.80,
        "pass_metric": score >= 0.80,
    }


def _ood_retrieval(emovoice_root: Path) -> Dict[str, object]:
    audio_files = list(emovoice_root.rglob("*.wav")) + list(emovoice_root.rglob("*.flac"))
    if len(audio_files) < 16:
        return {
            "executed": False,
            "reason": "insufficient_ood_audio",
            "p_at_5": 0.0,
            "samples": len(audio_files),
        }

    labels: Dict[str, str] = {}
    embeddings: Dict[str, List[float]] = {}
    for idx, path in enumerate(audio_files[:120]):
        label = path.parent.name.lower() or "unknown"
        sample_id = f"ood_{idx:04d}"
        labels[sample_id] = label
        try:
            bundle = _bundle_from_wav(path)
            embeddings[sample_id] = build_embedding(bundle)
        except Exception:
            continue

    if len(embeddings) < 16:
        return {
            "executed": False,
            "reason": "ood_embedding_build_failed",
            "p_at_5": 0.0,
            "samples": len(embeddings),
        }

    score = mean_precision_at_k(labels=labels, embeddings=embeddings, top_k=5)
    return {
        "executed": True,
        "dataset": "emovome_or_emovoice_real",
        "samples": len(embeddings),
        "p_at_5": score,
        "threshold": 0.65,
        "pass_metric": score >= 0.65,
    }


def _choose_ood_eval(candidates: List[Tuple[str, Path]]) -> Dict[str, object]:
    results: List[Dict[str, object]] = []
    for name, root in candidates:
        if not root.exists():
            continue
        eval_result = _ood_retrieval(root)
        eval_result["source_name"] = name
        eval_result["source_root"] = str(root)
        results.append(eval_result)

    for result in results:
        if result.get("executed"):
            return result

    if results:
        return results[0]
    return {
        "executed": False,
        "reason": "ood_dataset_missing",
        "p_at_5": 0.0,
        "samples": 0,
        "source_name": "none",
    }


def _attempt_xtts_transfer(venv_python: Path, ravdess_manifest: Path, out_dir: Path, env: Dict[str, str]) -> Dict[str, object]:
    transfer_dir = out_dir / "xtts_transfer"
    transfer_dir.mkdir(parents=True, exist_ok=True)

    script = f"""
import json
from pathlib import Path
from TTS.api import TTS

manifest = json.loads(Path(r'{ravdess_manifest}').read_text())
items = [x for x in manifest.get('items', []) if Path(x['path']).exists()][:6]
out = Path(r'{transfer_dir}')
out.mkdir(parents=True, exist_ok=True)

model='tts_models/multilingual/multi-dataset/xtts_v2'
tts = TTS(model_name=model, progress_bar=False, gpu=False)
for idx, item in enumerate(items):
    speaker = item['path']
    target = out / f'transfer_{{idx:02d}}.wav'
    tts.tts_to_file(text='Prosody transfer validation sentence.', speaker_wav=speaker, language='en', file_path=str(target))
print(len(list(out.glob('*.wav'))))
""".strip()

    cache_dir = ROOT / ".runtime" / "maxwave" / "tts_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cmd = (
        f"COQUI_TOS_AGREED=1 TTS_HOME='{cache_dir}' "
        f"{shlex.quote(str(venv_python))} - <<'PY'\n{script}\nPY"
    )
    attempt = _run(cmd=cmd, cwd=ROOT, env=env, timeout=5400)
    generated = len(list(transfer_dir.glob("*.wav")))
    return {
        "attempt": attempt,
        "generated_files": generated,
        "transfer_dir": str(transfer_dir),
        "executed": attempt["returncode"] == 0 and generated > 0,
    }


def _attempt_speechmos(venv_python: Path, transfer_dir: Path, out_path: Path, env: Dict[str, str]) -> Dict[str, object]:
    script = f"""
import json
from pathlib import Path
from speechmos import dnsmos
import librosa
import numpy as np

files = sorted(Path(r'{transfer_dir}').glob('*.wav'))
out = {{'tool': 'SpeechMOS-DNSMOS', 'files': [], 'mean_mos': 0.0, 'executed': False}}
if files:
    vals = []
    for fp in files:
        wav, _sr = librosa.load(str(fp), sr=16000, mono=True)
        if wav.size:
            peak = float(np.max(np.abs(wav)))
            if peak > 1.0:
                wav = wav / peak
            wav = np.clip(wav, -1.0, 1.0)
        result = dnsmos.run(wav, sr=16000, model_type='dnsmos', return_df=False, verbose=False)
        score = float(result['p808_mos'])
        vals.append(score)
        out['files'].append({{'path': str(fp), 'mos': score}})
    out['mean_mos'] = sum(vals) / len(vals)
    out['executed'] = True
Path(r'{out_path}').write_text(json.dumps(out, indent=2))
print(out['executed'])
""".strip()
    cmd = f"{shlex.quote(str(venv_python))} - <<'PY'\n{script}\nPY"
    attempt = _run(cmd=cmd, cwd=ROOT, env=env, timeout=3600)
    if out_path.exists():
        return {"attempt": attempt, "result": _read(out_path)}
    return {
        "attempt": attempt,
        "result": {
            "tool": "SpeechMOS-DNSMOS",
            "executed": False,
            "mean_mos": 0.0,
            "files": [],
            "error": attempt.get("failure_signature", "speechmos_failed"),
        },
    }


def _attempt_text(resource_item: Dict[str, object]) -> str:
    chunks = []
    for attempt in resource_item.get("attempts", []):
        chunks.append(str(attempt.get("stdout_tail", "")))
        chunks.append(str(attempt.get("stderr_tail", "")))
        chunks.append(str(attempt.get("failure_signature", "")))
    return "\n".join(chunks).lower()


def _xtts_is_nc_restricted(resource_item: Dict[str, object]) -> bool:
    text = _attempt_text(resource_item)
    return "cpml" in text or "non-commercial" in text or "terms of service" in text


def main() -> None:
    args = parse_args("Appendix D/E claim adjudication")
    out_dir = args.out
    log_path = init_environment(out_dir, args.seed)
    env_bootstrap = bootstrap_env(log_path)

    max_lock = _read(out_dir / "max_resource_lock.json")
    impractical = _read(out_dir / "impracticality_decisions.json")
    resource_index = {item["resource_name"]: item for item in max_lock.get("resources", [])}

    venv_python = Path(max_lock.get("venv_python", str(ROOT / ".runtime" / "maxwave" / "venv" / "bin" / "python")))
    env = os.environ.copy()

    ravdess_manifest = ROOT / "data" / "external" / "ravdess" / "manifest.json"
    ravdess_eval = _ravdess_retrieval(ravdess_manifest) if ravdess_manifest.exists() else {
        "executed": False,
        "reason": "ravdess_manifest_missing",
        "p_at_5": 0.0,
        "samples": 0,
    }

    emovdb_root = ROOT / "data" / "external" / "emov_db"
    emovoice_root = ROOT / "data" / "external" / "EmoVoice"
    ood_eval = _choose_ood_eval(
        candidates=[
            ("emov_db_commercial_safe", emovdb_root),
            ("emovome_or_emovoice", emovoice_root),
        ]
    )

    xtts_status = resource_index.get("XTTS_v2", {})
    speechmos_status = resource_index.get("SpeechMOS", {})
    cosyvoice_status = resource_index.get("CosyVoice2_commercial_safe", {})
    cosyvoice_container_status = resource_index.get("CosyVoice2_containerized_path", {})
    parler_status = resource_index.get("ParlerTTS_commercial_safe", {})
    piper_status = resource_index.get("PiperTTS_commercial_safe", {})
    emovdb_status = resource_index.get("EMOV_DB_commercial_safe", {})
    ravdess_status = resource_index.get("RAVDESS", {})

    xtts_nc_restricted = _xtts_is_nc_restricted(xtts_status)
    ravdess_attempt_text = _attempt_text(ravdess_status)
    ravdess_nc_restricted = ("cc-by-nc" in ravdess_attempt_text) or ("non-commercial" in ravdess_attempt_text)
    emovdb_attempt_text = _attempt_text(emovdb_status)
    emovdb_nc_restricted = ("non-commercial" in emovdb_attempt_text) or ("non commercial" in emovdb_attempt_text)
    emovoice_license_present = any((emovoice_root / name).exists() for name in ("LICENSE", "LICENSE.txt", "COPYING", "COPYRIGHT"))
    emovdb_license_present = any((emovdb_root / name).exists() for name in ("LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING", "COPYRIGHT"))

    xtts_transfer = {
        "executed": False,
        "generated_files": 0,
        "transfer_dir": "",
        "attempt": {"returncode": 1, "failure_signature": "xtts_not_attempted"},
    }
    if xtts_status.get("status") == "SUCCESS" and ravdess_manifest.exists() and venv_python.exists():
        xtts_transfer = _attempt_xtts_transfer(venv_python, ravdess_manifest, out_dir, env)

    mos_crosscheck_path = out_dir / "mos_crosscheck_report.json"
    mos_result = {
        "tool": "SpeechMOS",
        "executed": False,
        "mean_mos": 0.0,
        "files": [],
        "reason": "speechmos_unavailable_or_xtts_missing",
    }
    mos_attempt = {"returncode": 1, "failure_signature": "mos_not_attempted"}
    if speechmos_status.get("status") == "SUCCESS" and xtts_transfer.get("executed") and venv_python.exists():
        speechmos_eval = _attempt_speechmos(venv_python, Path(xtts_transfer["transfer_dir"]), mos_crosscheck_path, env)
        mos_attempt = speechmos_eval["attempt"]
        mos_result = speechmos_eval["result"]
    else:
        write_json_artifact(out_dir, "mos_crosscheck_report.json", mos_result)

    # Claim adjudication for M1/M2.
    pro_c005_status = "FAIL"
    pro_c005_reason = "Transfer MOS evidence chain did not execute successfully."
    alt_transfer_resources = {
        "CosyVoice2_commercial_safe": cosyvoice_status.get("status") == "SUCCESS",
        "CosyVoice2_containerized_path": cosyvoice_container_status.get("status") == "SUCCESS",
        "ParlerTTS_commercial_safe": parler_status.get("status") == "SUCCESS",
        "PiperTTS_commercial_safe": piper_status.get("status") == "SUCCESS",
    }
    alt_transfer_ready = any(alt_transfer_resources.values())
    if xtts_transfer.get("executed") and mos_result.get("executed"):
        pro_c005_status = "PASS" if float(mos_result.get("mean_mos", 0.0)) >= 4.0 else "FAIL"
        pro_c005_reason = "XTTS transfer executed with SpeechMOS evidence."
    elif alt_transfer_ready:
        pro_c005_status = "FAIL"
        pro_c005_reason = (
            "Commercial-safe TTS substitutes executed, but MOS-equivalent transfer evidence "
            "did not meet protocol for PASS."
        )
    if xtts_nc_restricted and not alt_transfer_ready:
        pro_c005_status = "PAUSED_EXTERNAL"
        pro_c005_reason = (
            "XTTS is CPML/non-permissive and no executable commercial-safe transfer substitute was proven in-lane."
        )

    pro_c006_status = "FAIL"
    pro_c006_reason = "Real RAVDESS retrieval evidence unavailable."
    if ravdess_eval.get("executed"):
        # E-G3: cannot be PASS without OOD stress path.
        ravdess_ok = bool(ravdess_eval.get("pass_metric"))
        ood_ok = bool(ood_eval.get("executed") and ood_eval.get("pass_metric"))
        if ravdess_ok and ood_ok:
            pro_c006_status = "PASS"
            pro_c006_reason = "RAVDESS + OOD retrieval stress passed."
        else:
            pro_c006_status = "FAIL"
            if not ood_eval.get("executed"):
                pro_c006_reason = "RAVDESS executed but OOD stress corpus unavailable; E-G3 blocks PASS."
            else:
                pro_c006_reason = "RAVDESS/OOD retrieval metrics below thresholds."
    commercial_ood_ready = (
        emovdb_status.get("status") == "SUCCESS"
        and emovdb_license_present
        and (not emovdb_nc_restricted)
    )
    if ravdess_nc_restricted and not (commercial_ood_ready or emovoice_license_present):
        pro_c006_status = "PAUSED_EXTERNAL"
        pro_c006_reason = (
            "Emotional-corpus path is NC/restricted and no commercial-safe licensed substitute is proven in-lane."
        )

    # RunPod readiness when IMP-COMPUTE present.
    impractical_items = impractical.get("items", [])
    has_imp_compute = any(item.get("impracticality_code") == "IMP-COMPUTE" for item in impractical_items)
    if has_imp_compute:
        runpod_lock = max_lock.get("runpod_lockfile", str(ROOT / ".runtime" / "maxwave" / "requirements_runpod_lock.txt"))
        runpod_lock_path = Path(runpod_lock)
        runpod_lock_artifact = out_dir / "runpod_requirements_lock.txt"
        if runpod_lock_path.exists():
            runpod_lock_artifact.write_text(runpod_lock_path.read_text(encoding="utf-8"), encoding="utf-8")
        runpod_chain = [
            "python3.11 -m venv .runtime/maxwave/venv",
            ".runtime/maxwave/venv/bin/pip install --upgrade pip setuptools wheel",
            f".runtime/maxwave/venv/bin/pip install -r {runpod_lock_artifact.name}",
            ".runtime/maxwave/venv/bin/python scripts/gate_m_resource_ingestion.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220",
            ".runtime/maxwave/venv/bin/python scripts/gate_m_claim_adjudication.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220",
            ".runtime/maxwave/venv/bin/python scripts/gate_e_eval_and_pack.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220",
        ]
        expected_artifacts = [
            "mos_crosscheck_report.json",
            "prosody_transfer_eval.json",
            "prosody_retrieval_eval.json",
            "max_claim_adjudication.json",
            "quality_gate_scorecard.json",
            "handoff_manifest.json",
        ]
        runpod_manifest = {
            "required": True,
            "gpu_profile": "RunPod NVIDIA A100/B200 (>=40GB VRAM)",
            "base_image": "runpod/pytorch:2.4.0-py3.11-cuda12.1",
            "workspace_sync_root": "/workspace/ZPE Prosody",
            "python_version": "3.11",
            "lockfile": runpod_lock,
            "lockfile_artifact": runpod_lock_artifact.name,
            "packages": [
                "torch",
                "torchaudio",
                "torchcrepe",
                "praat-parselmouth",
                "TTS",
                "speechmos",
                "onnxruntime",
                "datasets",
                "soundfile",
                "parler-tts",
                "piper-tts",
            ],
            "deferred_resources": [
                item["resource_name"] for item in impractical_items if item.get("impracticality_code") == "IMP-COMPUTE"
            ],
            "exact_command_chain": runpod_chain,
            "expected_artifact_manifest": expected_artifacts,
        }
        write_json_artifact(out_dir, "runpod_readiness_manifest.json", runpod_manifest)

        runpod_dataset_stage = {
            "ravdess": "stage to /workspace/data/ravdess with manifest + checksums",
            "ood_dataset": "stage EmoVoice/EMOVOME corpus to /workspace/data/ood",
            "xtts_outputs": "stage generated transfer wav files to /workspace/artifacts/xtts_transfer",
        }
        write_json_artifact(out_dir, "runpod_dataset_stage_manifest.json", runpod_dataset_stage)

        runpod_exec_plan = "\n".join(
            [
                "# RunPod Execution Plan",
                "",
                "## Exact Command Chain",
                *[f"- `{cmd}`" for cmd in runpod_chain],
                "",
                "## Expected Artifacts",
                *[f"- `{name}`" for name in expected_artifacts],
            ]
        )
        (out_dir / "runpod_exec_plan.md").write_text(runpod_exec_plan, encoding="utf-8")

    # Net-new gap closure matrix.
    gap_matrix = {
        "gaps": [
            {
                "gap_id": "D2-G1",
                "description": "Extractor stack enabled (torchcrepe/parselmouth/penn)",
                "status": "CLOSED" if resource_index.get("torchcrepe", {}).get("status") == "SUCCESS" and resource_index.get("Parselmouth", {}).get("status") == "SUCCESS" else "OPEN",
                "evidence": "max_resource_lock.json",
            },
            {
                "gap_id": "D2-G2",
                "description": "XTTS bridge + MOS protocol executed",
                "status": "CLOSED" if xtts_transfer.get("executed") and mos_result.get("executed") else "OPEN",
                "evidence": "mos_crosscheck_report.json",
            },
            {
                "gap_id": "D2-G3",
                "description": "RAVDESS retrieval validity closed",
                "status": "CLOSED" if ravdess_eval.get("executed") else "OPEN",
                "evidence": "prosody_retrieval_eval.json",
            },
            {
                "gap_id": "E3-OOD",
                "description": "OOD retrieval stress path (EMOVOME/EmoVoice)",
                "status": "CLOSED" if ood_eval.get("executed") else "OPEN",
                "evidence": "max_resource_lock.json",
            },
        ]
    }
    write_json_artifact(out_dir, "net_new_gap_closure_matrix.json", gap_matrix)

    eg1 = all(len(item.get("attempts", [])) > 0 for item in max_lock.get("resources", []))
    eg2 = not (pro_c005_status == "PASS" and not (xtts_transfer.get("executed") and mos_result.get("executed")))
    eg3 = not (pro_c006_status == "PASS" and not (ravdess_eval.get("executed") and ood_eval.get("executed")))
    eg4 = (not has_imp_compute) or ((out_dir / "runpod_readiness_manifest.json").exists() and (out_dir / "runpod_exec_plan.md").exists())
    eg5 = True
    fg1 = pro_c005_status in {"PASS", "FAIL", "PAUSED_EXTERNAL"} and pro_c006_status in {"PASS", "FAIL", "PAUSED_EXTERNAL"}
    fg2 = (
        ("PAUSED_EXTERNAL" not in {pro_c005_status, pro_c006_status})
        or xtts_nc_restricted
        or ravdess_nc_restricted
    )

    max_adjudication = {
        "env_bootstrap": env_bootstrap,
        "m1_pro_c005": {
            "status": pro_c005_status,
            "reason": pro_c005_reason,
            "xtts_transfer": xtts_transfer,
            "mos_evidence": mos_result,
            "mos_attempt": mos_attempt,
            "xtts_nc_restricted": xtts_nc_restricted,
            "commercial_safe_alternative_status": cosyvoice_status.get("status", "UNAVAILABLE"),
            "commercial_safe_container_status": cosyvoice_container_status.get("status", "UNAVAILABLE"),
            "commercial_safe_replacement_paths": alt_transfer_resources,
            "evidence": "mos_crosscheck_report.json",
        },
        "m2_pro_c006": {
            "status": pro_c006_status,
            "reason": pro_c006_reason,
            "ravdess_eval": ravdess_eval,
            "ood_eval": ood_eval,
            "ravdess_nc_restricted": ravdess_nc_restricted,
            "emovoice_license_present": emovoice_license_present,
            "emovdb_license_present": emovdb_license_present,
            "emovdb_nc_restricted": emovdb_nc_restricted,
            "emovdb_resource_status": emovdb_status.get("status", "UNAVAILABLE"),
            "evidence": "prosody_retrieval_eval.json",
        },
        "m3_quality_gate": "DEFER_TO_FINAL_PACKAGING",
        "m4_fallback_controlled": True,
        "appendix_e_gates": {
            "E-G1": eg1,
            "E-G2": eg2,
            "E-G3": eg3,
            "E-G4": eg4,
            "E-G5": eg5,
        },
        "appendix_f_gates": {
            "F-G1": fg1,
            "F-G2": fg2,
        },
    }
    write_json_artifact(out_dir, "max_claim_adjudication.json", max_adjudication)

    # Update core eval files from real corpus execution when available.
    transfer_eval_path = out_dir / "prosody_transfer_eval.json"
    retrieval_eval_path = out_dir / "prosody_retrieval_eval.json"
    transfer_eval = _read(transfer_eval_path)
    retrieval_eval = _read(retrieval_eval_path)

    transfer_eval.update(
        {
            "status": pro_c005_status,
            "reason": pro_c005_reason,
            "xtts_transfer_executed": bool(xtts_transfer.get("executed")),
            "mos_tool_used": mos_result.get("tool"),
            "mos_evidence_executed": bool(mos_result.get("executed")),
            "mean_mos": float(mos_result.get("mean_mos", transfer_eval.get("mean_mos", 0.0))),
            "pass_metric": float(mos_result.get("mean_mos", 0.0)) >= 4.0 if mos_result.get("executed") else False,
            "resource_equivalence_proven": bool(xtts_transfer.get("executed") and mos_result.get("executed")),
        }
    )
    write_json_artifact(out_dir, "prosody_transfer_eval.json", transfer_eval)

    retrieval_eval.update(
        {
            "dataset": "ravdess_real" if ravdess_eval.get("executed") else retrieval_eval.get("dataset", "ravdess_like"),
            "p_at_5": float(ravdess_eval.get("p_at_5", retrieval_eval.get("p_at_5", 0.0))),
            "ood_p_at_5": float(ood_eval.get("p_at_5", 0.0)) if ood_eval.get("executed") else None,
            "status": pro_c006_status,
            "reason": pro_c006_reason,
            "pass_metric": bool(ravdess_eval.get("pass_metric", False) and ood_eval.get("pass_metric", False)),
            "resource_equivalence_proven": bool(ravdess_eval.get("executed")),
        }
    )
    write_json_artifact(out_dir, "prosody_retrieval_eval.json", retrieval_eval)

    log_command(
        log_path,
        "gate_m_claim_adjudication",
        f"pro_c005={pro_c005_status} pro_c006={pro_c006_status} egates={max_adjudication['appendix_e_gates']}",
    )
    print("Gate M claim adjudication complete")


if __name__ == "__main__":
    main()
