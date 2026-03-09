"""Appendix D/E Gate M resource ingestion and attempt-all evidence capture."""

from __future__ import annotations

import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

from common import ROOT, bootstrap_env, init_environment, log_command, parse_args, write_json_artifact


def _run(
    log_path: Path,
    cmd: str,
    cwd: Path,
    env: Dict[str, str],
    timeout: int = 1200,
) -> Dict[str, object]:
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
    log_command(log_path, "gate_m_cmd", f"rc={rc} cmd={cmd}")
    return {
        "command": cmd,
        "cwd": str(cwd),
        "returncode": rc,
        "stdout_tail": stdout[-1200:],
        "stderr_tail": stderr[-1200:],
        "failure_signature": signature,
    }


def _classify_imp(resource_name: str, attempts: List[Dict[str, object]]) -> str:
    text = "\n".join(
        str(item.get("failure_signature") or "") + "\n" + str(item.get("stderr_tail") or "")
        for item in attempts
        if int(item.get("returncode", 0)) != 0
    ).lower()

    if not text:
        return ""
    if "license" in text or "non-commercial" in text or "forbidden by license" in text:
        return "IMP-LICENSE"
    if (
        "module not found" in text
        or "failed building wheel" in text
        or "error: subprocess-exited-with-error" in text
        or "array_api not found" in text
        or "typeerror" in text
        or "runtimeerror" in text
        or "timeout_expired" in text
        or "compiled using numpy 1.x cannot be run in" in text
        or "killed" in text
        or "exit code: 137" in text
    ):
        return "IMP-COMPUTE"
    if "403" in text or "401" in text or "permission denied" in text or "could not resolve" in text:
        return "IMP-ACCESS"
    if "no space" in text or "disk" in text or "quota" in text:
        return "IMP-STORAGE"
    if "requires" in text or "build" in text or "killed" in text or "cuda" in text or "not found" in text:
        return "IMP-COMPUTE"
    if resource_name in {"emovome_or_emovoice"}:
        return "IMP-NOCODE"
    return "IMP-COMPUTE"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(1 << 16)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    args = parse_args("Appendix D/E resource ingestion")
    out_dir = args.out
    log_path = init_environment(out_dir, args.seed)
    env_bootstrap = bootstrap_env(log_path)

    runtime = ROOT / ".runtime" / "maxwave"
    runtime.mkdir(parents=True, exist_ok=True)
    external_dir = ROOT / "data" / "external"
    external_dir.mkdir(parents=True, exist_ok=True)

    py311 = shutil.which("python3.11")
    py_exec = py311 if py311 else sys.executable
    venv_dir = runtime / "venv"
    env = os.environ.copy()

    setup_attempts = []
    setup_attempts.append(_run(log_path, f"{shlex.quote(str(py_exec))} -m venv '{venv_dir}'", ROOT, env, timeout=300))
    pip = venv_dir / "bin" / "pip"
    python = venv_dir / "bin" / "python"
    pip_cmd = shlex.quote(str(pip))
    py_cmd = shlex.quote(str(python))
    setup_attempts.append(_run(log_path, f"{pip_cmd} install --upgrade pip setuptools wheel", ROOT, env, timeout=600))
    setup_attempts.append(_run(log_path, f"{pip_cmd} install 'numpy<2' 'numba==0.59.1' 'llvmlite==0.42.0' librosa==0.10.2.post1", ROOT, env, timeout=1200))
    setup_attempts.append(_run(log_path, f"{pip_cmd} install 'transformers<5' 'onnxruntime>=1.17,<1.23' soundfile", ROOT, env, timeout=1200))

    resources: List[Dict[str, object]] = []

    def record_resource(
        name: str,
        claim_link: List[str],
        attempts: List[Dict[str, object]],
        fallback: str,
        comparability_impact: str,
        success_override: bool | None = None,
    ) -> None:
        success = (
            bool(success_override)
            if success_override is not None
            else (all(int(a.get("returncode", 0)) == 0 for a in attempts) and len(attempts) > 0)
        )
        imp_code = "" if success else _classify_imp(name, attempts)
        resources.append(
            {
                "resource_name": name,
                "claims": claim_link,
                "attempts": attempts,
                "status": "SUCCESS" if success else "FAILED",
                "impracticality_code": imp_code,
                "fallback": fallback,
                "comparability_impact": comparability_impact,
            }
        )

    # UTMOSv2
    utmos_repo = external_dir / "UTMOSv2"
    utmos_attempts = [
        _run(log_path, f"rm -rf '{utmos_repo}' && git clone --depth 1 https://github.com/sarulab-speech/UTMOSv2 '{utmos_repo}'", ROOT, env, timeout=600),
        _run(
            log_path,
            (
                f"if [ -f '{utmos_repo / 'requirements.txt'}' ]; then "
                f"{pip_cmd} install -r '{utmos_repo / 'requirements.txt'}'; "
                f"else {pip_cmd} install -e '{utmos_repo}'; fi"
            ),
            ROOT,
            env,
            timeout=1200,
        ),
        _run(log_path, f"{py_cmd} -c \"import utmosv2; print('utmosv2_ok')\"", ROOT, env, timeout=300),
    ]
    record_resource(
        "UTMOSv2",
        ["PRO-C005"],
        utmos_attempts,
        fallback="speechmos_if_available_else_proxy_mos",
        comparability_impact="High if unavailable: transfer MOS claim remains unclosed.",
    )

    # SpeechMOS
    speechmos_attempts = [
        _run(log_path, f"{pip_cmd} install speechmos onnxruntime", ROOT, env, timeout=1200),
        _run(log_path, f"{py_cmd} -c \"from speechmos import dnsmos; print('speechmos_dnsmos_ok')\"", ROOT, env, timeout=300),
    ]
    record_resource(
        "SpeechMOS",
        ["PRO-C005"],
        speechmos_attempts,
        fallback="utmosv2_if_available_else_proxy_mos",
        comparability_impact="High if unavailable: no independent MOS cross-check.",
    )

    # RAVDESS via HuggingFace datasets.
    ravdess_dir = external_dir / "ravdess"
    ravdess_dir.mkdir(parents=True, exist_ok=True)
    ravdess_py = (
        "import json, wave, struct, pathlib; "
        "from datasets import load_dataset; "
        f"out=pathlib.Path('{ravdess_dir}'); out.mkdir(parents=True, exist_ok=True); "
        "ds=load_dataset('narad/ravdess', split='train[:120]'); "
        "meta=[]; "
        "\nfor i,row in enumerate(ds):\n"
        "  audio=row['audio']; arr=audio['array']; sr=int(audio['sampling_rate']);\n"
        "  label=str(row.get('emotion', row.get('label', 'unknown')));\n"
        "  path=out / f'ravdess_{i:04d}_{label}.wav';\n"
        "  with wave.open(str(path),'wb') as w:\n"
        "    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr);\n"
        "    pcm=bytearray();\n"
        "    for v in arr:\n"
        "      iv=max(-32768,min(32767,int(v*32767)));\n"
        "      pcm.extend(struct.pack('<h',iv));\n"
        "    w.writeframes(bytes(pcm));\n"
        "  meta.append({'path':str(path),'label':label,'sr':sr});\n"
        "(out / 'manifest.json').write_text(json.dumps({'items':meta}, indent=2)); print(len(meta))"
    )
    ravdess_fallback_py = (
        "import json, pathlib, re; "
        f"root=pathlib.Path(r'{ravdess_dir}'); "
        "pattern=re.compile(r'(\\d{2})-(\\d{2})-(\\d{2})-(\\d{2})-(\\d{2})-(\\d{2})-(\\d{2})\\.wav$'); "
        "items=sorted([{'path':str(p),'label':(pattern.search(p.name).group(3) if pattern.search(p.name) else 'unknown'),'sr':48000} "
        "for p in root.rglob('*.wav')], key=lambda x: x['path'])[:240]; "
        "root.joinpath('manifest.json').write_text(json.dumps({'items':items}, indent=2)); "
        "print(len(items))"
    )
    ravdess_attempts = []
    ravdess_attempts.append(_run(log_path, f"{pip_cmd} install datasets soundfile", ROOT, env, timeout=1200))
    ravdess_attempts.append(_run(log_path, f"{py_cmd} -c \"{ravdess_py}\"", ROOT, env, timeout=1800))
    if not (ravdess_dir / "manifest.json").exists():
        ravdess_attempts.append(
            _run(
                log_path,
                f"mkdir -p '{ravdess_dir}' && curl -L -o '{ravdess_dir / 'Audio_Speech_Actors_01-24.zip'}' https://zenodo.org/records/1188976/files/Audio_Speech_Actors_01-24.zip",
                ROOT,
                env,
                timeout=2400,
            )
        )
        ravdess_attempts.append(
            _run(
                log_path,
                f"unzip -o -q '{ravdess_dir / 'Audio_Speech_Actors_01-24.zip'}' -d '{ravdess_dir}'",
                ROOT,
                env,
                timeout=1800,
            )
        )
        ravdess_attempts.append(_run(log_path, f"{py_cmd} -c \"{ravdess_fallback_py}\"", ROOT, env, timeout=900))
    ravdess_attempts.append(
        _run(
            log_path,
            f"curl -s https://zenodo.org/api/records/1188976 | rg -n \"license|rights|access_right\"",
            ROOT,
            env,
            timeout=300,
        )
    )
    ravdess_attempts.append(_run(log_path, f"test -f '{ravdess_dir / 'manifest.json'}'", ROOT, env, timeout=120))
    record_resource(
        "RAVDESS",
        ["PRO-C006"],
        ravdess_attempts,
        fallback="deterministic_ravdess_like_fixture",
        comparability_impact="High if unavailable: retrieval cannot be proven on real emotional corpus.",
        success_override=int(ravdess_attempts[-1].get("returncode", 1)) == 0,
    )

    # torchcrepe + torch
    torchcrepe_attempts = [
        _run(log_path, f"{pip_cmd} install --index-url https://download.pytorch.org/whl/cpu torch torchaudio", ROOT, env, timeout=1200),
        _run(log_path, f"{pip_cmd} install torchcrepe", ROOT, env, timeout=900),
        _run(log_path, f"{py_cmd} -c \"import torch, torchcrepe; print(torch.__version__)\"", ROOT, env, timeout=300),
    ]
    record_resource(
        "torchcrepe",
        ["PRO-C001", "PRO-C002"],
        torchcrepe_attempts,
        fallback="fallback_zero_crossing_f0",
        comparability_impact="Medium-to-high: extractor fidelity comparability drops if missing.",
    )

    # Parselmouth
    parselmouth_attempts = [
        _run(log_path, f"{pip_cmd} install praat-parselmouth", ROOT, env, timeout=600),
        _run(log_path, f"{py_cmd} -c \"import parselmouth; print(parselmouth.__version__)\"", ROOT, env, timeout=120),
    ]
    record_resource(
        "Parselmouth",
        ["PRO-C003"],
        parselmouth_attempts,
        fallback="fallback_rms_energy_duration",
        comparability_impact="Medium: missing Praat-standard extraction weakens equivalence.",
    )

    # XTTS v2
    xtts_out = out_dir / "xtts_probe.wav"
    xtts_cache = runtime / "tts_cache"
    xtts_probe_py = (
        "import json, pathlib; "
        "from TTS.api import TTS; "
        f"manifest=pathlib.Path(r'{ravdess_dir / 'manifest.json'}'); "
        "items=json.loads(manifest.read_text()).get('items', []); "
        "speaker=next(pathlib.Path(i['path']) for i in items if pathlib.Path(i['path']).exists()); "
        "tts=TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2', progress_bar=False, gpu=False); "
        f"tts.tts_to_file(text='Prosody transfer validation sentence.', speaker_wav=str(speaker), language='en', file_path=r'{xtts_out}'); "
        "print('xtts_ok')"
    )
    xtts_attempts = [
        _run(log_path, f"{pip_cmd} install TTS", ROOT, env, timeout=900),
        _run(log_path, f"{pip_cmd} install 'transformers==4.41.2'", ROOT, env, timeout=900),
        _run(
            log_path,
            "curl -L -s https://huggingface.co/coqui/XTTS-v2/raw/main/README.md | rg -n \"license|coqui-public-model-license|cpml|non-commercial\" -i",
            ROOT,
            env,
            timeout=120,
        ),
        _run(
            log_path,
            (
                f"COQUI_TOS_AGREED=1 TTS_HOME='{xtts_cache}' {py_cmd} -c \"{xtts_probe_py}\""
            ),
            ROOT,
            env,
            timeout=900,
        ),
    ]
    record_resource(
        "XTTS_v2",
        ["PRO-C005"],
        xtts_attempts,
        fallback="objective_transfer_proxy_without_tts",
        comparability_impact="High: no true transfer synthesis means PRO-C005 cannot be fully closed.",
    )

    # Commercial-safe alternative (Appendix F): CosyVoice2 Apache path.
    cosyvoice_repo = external_dir / "CosyVoice"
    cosyvoice_attempts = [
        _run(log_path, f"rm -rf '{cosyvoice_repo}' && git clone --depth 1 https://github.com/FunAudioLLM/CosyVoice '{cosyvoice_repo}'", ROOT, env, timeout=900),
        _run(log_path, f"git -C '{cosyvoice_repo}' submodule update --init --recursive", ROOT, env, timeout=1200),
        _run(log_path, f"test -f '{cosyvoice_repo / 'LICENSE'}' && rg -n \"Apache\" '{cosyvoice_repo / 'LICENSE'}'", ROOT, env, timeout=120),
        _run(log_path, f"{pip_cmd} install -r '{cosyvoice_repo / 'requirements.txt'}'", ROOT, env, timeout=1200),
        _run(log_path, f"PYTHONPATH='{cosyvoice_repo}:$PYTHONPATH' {py_cmd} -c \"from cosyvoice.cli.cosyvoice import CosyVoice; print('cosyvoice_ok')\"", ROOT, env, timeout=300),
    ]
    record_resource(
        "CosyVoice2_commercial_safe",
        ["PRO-C005"],
        cosyvoice_attempts,
        fallback="runpod_gpu_transfer_with_permissive_tts",
        comparability_impact="High: commercial-safe transfer closure blocked if CosyVoice2 path is unavailable.",
    )

    # Containerized path (Appendix F step b).
    cosyvoice_container_attempts = [
        _run(log_path, "docker --version", ROOT, env, timeout=120),
        _run(
            log_path,
            f"docker build -t cosyvoice_runtime_probe '{cosyvoice_repo / 'runtime' / 'python'}'",
            ROOT,
            env,
            timeout=300,
        ),
    ]
    record_resource(
        "CosyVoice2_containerized_path",
        ["PRO-C005"],
        cosyvoice_container_attempts,
        fallback="runpod_gpu_transfer_with_permissive_tts",
        comparability_impact="Medium-to-high: containerized fallback unavailable in-lane if docker build/runtime fails.",
    )

    # Commercial-safe alternative path 3: Parler-TTS (Apache-2.0).
    parler_out = out_dir / "parler_probe.wav"
    parler_script = f"""
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

model_name = "parler-tts/parler-tts-mini-v1"
model = ParlerTTSForConditionalGeneration.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
description = "A calm speaker with clear articulation and neutral delivery."
prompt = "Prosody transfer validation sentence."
input_ids = tokenizer(description, return_tensors="pt").input_ids
prompt_ids = tokenizer(prompt, return_tensors="pt").input_ids
audio = model.generate(input_ids=input_ids, prompt_input_ids=prompt_ids)
arr = audio.cpu().numpy().squeeze()
sf.write(r"{parler_out}", arr, int(model.config.sampling_rate))
print("parler_ok")
""".strip()
    parler_attempts = [
        _run(
            log_path,
            "curl -L -s https://raw.githubusercontent.com/huggingface/parler-tts/main/LICENSE | rg -n \"apache\" -i",
            ROOT,
            env,
            timeout=120,
        ),
        _run(log_path, f"{pip_cmd} install parler-tts accelerate", ROOT, env, timeout=1200),
        _run(log_path, f"{py_cmd} - <<'PY'\n{parler_script}\nPY", ROOT, env, timeout=3600),
        _run(log_path, f"test -f '{parler_out}'", ROOT, env, timeout=120),
    ]
    record_resource(
        "ParlerTTS_commercial_safe",
        ["PRO-C005"],
        parler_attempts,
        fallback="runpod_gpu_transfer_with_parler_tts",
        comparability_impact="Medium-to-high: no direct speaker-clone transfer; usable only as commercialization-safe synthesis substitute.",
        success_override=int(parler_attempts[-1].get("returncode", 1)) == 0,
    )

    # Commercial-safe alternative path 4: Piper TTS (MIT).
    piper_model_dir = runtime / "piper_models"
    piper_model_dir.mkdir(parents=True, exist_ok=True)
    piper_model = piper_model_dir / "en_US-lessac-medium.onnx"
    piper_cfg = piper_model_dir / "en_US-lessac-medium.onnx.json"
    piper_out = out_dir / "piper_probe.wav"
    piper_attempts = [
        _run(
            log_path,
            "curl -L -s https://raw.githubusercontent.com/rhasspy/piper/master/LICENSE.md | rg -n \"mit\" -i",
            ROOT,
            env,
            timeout=120,
        ),
        _run(log_path, f"{pip_cmd} install piper-tts", ROOT, env, timeout=900),
        _run(
            log_path,
            (
                f"curl -L -o '{piper_model}' "
                "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
            ),
            ROOT,
            env,
            timeout=1200,
        ),
        _run(
            log_path,
            (
                f"curl -L -o '{piper_cfg}' "
                "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
            ),
            ROOT,
            env,
            timeout=1200,
        ),
        _run(
            log_path,
            (
                f"printf 'Prosody transfer validation sentence.' | "
                f"'{venv_dir / 'bin' / 'piper'}' --model '{piper_model}' --config '{piper_cfg}' --output_file '{piper_out}'"
            ),
            ROOT,
            env,
            timeout=900,
        ),
        _run(log_path, f"test -f '{piper_out}'", ROOT, env, timeout=120),
    ]
    record_resource(
        "PiperTTS_commercial_safe",
        ["PRO-C005"],
        piper_attempts,
        fallback="runpod_gpu_transfer_with_piper_or_other_permissive_tts",
        comparability_impact="Medium-to-high: lacks direct XTTS-style voice transfer conditioning.",
        success_override=int(piper_attempts[-1].get("returncode", 1)) == 0,
    )

    # Commercial-safe emotional corpus substitute: EmoV-DB (OpenSLR-115).
    emovdb_dir = external_dir / "emov_db"
    emovdb_manifest = emovdb_dir / "manifest.json"
    emovdb_zip = emovdb_dir / "emovdb.zip"
    emovdb_manifest_py = (
        "import json, pathlib; "
        f"root=pathlib.Path(r'{emovdb_dir}'); root.mkdir(parents=True, exist_ok=True); "
        "files=sorted(list(root.rglob('*.wav')) + list(root.rglob('*.flac'))); "
        "items=[{'path':str(p),'label':p.parent.name.lower(),'sr':0} for p in files[:240]]; "
        f"pathlib.Path(r'{emovdb_manifest}').write_text(json.dumps({{'items':items}}, indent=2)); "
        "print(len(items))"
    )
    emovdb_attempts = [
        _run(log_path, f"rm -rf '{emovdb_dir}' && git clone --depth 1 https://github.com/numediart/EmoV-DB '{emovdb_dir}'", ROOT, env, timeout=900),
        _run(log_path, f"curl -L -s https://www.openslr.org/115/ | rg -n \"License|license|CC|commercial\" -i", ROOT, env, timeout=120),
        _run(log_path, "curl -L -s https://raw.githubusercontent.com/numediart/EmoV-DB/master/LICENSE.md | head -n 30", ROOT, env, timeout=120),
        _run(log_path, f"find '{emovdb_dir}' -type f \\( -name '*.wav' -o -name '*.flac' \\) | head -n 5", ROOT, env, timeout=120),
        _run(
            log_path,
            (
                f"if [ \"$(find '{emovdb_dir}' -type f -name '*.wav' | wc -l | tr -d ' ')\" -lt 16 ]; then "
                f"mkdir -p '{emovdb_dir}' && curl -L -o '{emovdb_zip}' https://www.openslr.org/resources/115/emovdb.zip; "
                "else echo 'skip_download_has_audio'; fi"
            ),
            ROOT,
            env,
            timeout=1800,
        ),
        _run(
            log_path,
            (
                f"if [ -f '{emovdb_zip}' ]; then unzip -o -q '{emovdb_zip}' -d '{emovdb_dir}'; "
                "else echo 'skip_unzip_no_zip'; fi"
            ),
            ROOT,
            env,
            timeout=1800,
        ),
        _run(log_path, f"{py_cmd} -c \"{emovdb_manifest_py}\"", ROOT, env, timeout=300),
        _run(
            log_path,
            (
                f"{py_cmd} -c \"import json, pathlib, sys; p=pathlib.Path(r'{emovdb_manifest}'); "
                "items=json.loads(p.read_text()).get('items', []) if p.exists() else []; "
                "print(len(items)); sys.exit(0 if len(items) >= 16 else 3)\""
            ),
            ROOT,
            env,
            timeout=120,
        ),
    ]
    emovdb_text = "\n".join(
        str(attempt.get("stdout_tail", "")) + "\n" + str(attempt.get("stderr_tail", ""))
        for attempt in emovdb_attempts
    ).lower()
    emovdb_noncommercial = ("non-commercial" in emovdb_text) or ("non commercial" in emovdb_text)
    record_resource(
        "EMOV_DB_commercial_safe",
        ["PRO-C006"],
        emovdb_attempts,
        fallback="retain_emovoice_ood_with_license_gap_note",
        comparability_impact="High: EmoV-DB license and data availability must both satisfy commercialization constraints.",
        success_override=(int(emovdb_attempts[-1].get("returncode", 1)) == 0 and (not emovdb_noncommercial)),
    )

    # EMOVOME or EmoVoice-DB
    emovoice_repo = external_dir / "EmoVoice"
    emovome_attempts = [
        _run(log_path, f"rm -rf '{emovoice_repo}' && git clone --depth 1 https://github.com/yanghaha0908/EmoVoice '{emovoice_repo}'", ROOT, env, timeout=600),
        _run(log_path, f"find '{emovoice_repo}' -type f \\( -name '*.wav' -o -name '*.flac' \\) | head -n 5", ROOT, env, timeout=120),
    ]
    record_resource(
        "emovome_or_emovoice",
        ["PRO-C006"],
        emovome_attempts,
        fallback="ravdess_only_retrieval_with_declared_ood_gap",
        comparability_impact="High if unavailable: OOD emotional retrieval stress remains open.",
    )

    # Build impracticality decisions.
    impractical: List[Dict[str, object]] = []
    for item in resources:
        if item["status"] == "SUCCESS":
            continue
        fails = [a for a in item["attempts"] if int(a.get("returncode", 0)) != 0]
        impractical.append(
            {
                "resource_name": item["resource_name"],
                "impracticality_code": item["impracticality_code"],
                "command_evidence": [a["command"] for a in fails],
                "error_signature": fails[-1].get("failure_signature", "") if fails else "unknown",
                "fallback": item["fallback"],
                "claim_impact_note": item["comparability_impact"],
            }
        )

    # Resource lock with hashes where possible.
    file_hashes = []
    for wav in sorted(ravdess_dir.glob("*.wav"))[:120]:
        file_hashes.append({"path": str(wav), "sha256": _sha256_file(wav), "bytes": wav.stat().st_size})

    max_resource_lock = {
        "seed": args.seed,
        "env_bootstrap": env_bootstrap,
        "venv_python": str(python),
        "setup_attempts": setup_attempts,
        "resources": resources,
        "ravdess_file_hashes": file_hashes,
    }

    runpod_lock = runtime / "requirements_runpod_lock.txt"
    freeze_attempt = _run(log_path, f"{pip_cmd} freeze > '{runpod_lock}'", ROOT, env, timeout=600)
    max_resource_lock["runpod_lockfile"] = str(runpod_lock)
    max_resource_lock["runpod_lockfile_generated"] = freeze_attempt["returncode"] == 0 and runpod_lock.exists()
    max_resource_lock["runpod_lockfile_attempt"] = freeze_attempt

    write_json_artifact(out_dir, "max_resource_lock.json", max_resource_lock)
    write_json_artifact(out_dir, "impracticality_decisions.json", {"items": impractical})

    claim_resource_map = {
        "PRO-C001": ["torchcrepe"],
        "PRO-C002": ["torchcrepe"],
        "PRO-C003": ["Parselmouth"],
        "PRO-C004": ["torchcrepe", "Parselmouth"],
        "PRO-C005": [
            "UTMOSv2",
            "SpeechMOS",
            "XTTS_v2",
            "CosyVoice2_commercial_safe",
            "CosyVoice2_containerized_path",
            "ParlerTTS_commercial_safe",
            "PiperTTS_commercial_safe",
        ],
        "PRO-C006": ["RAVDESS", "EMOV_DB_commercial_safe", "emovome_or_emovoice"],
    }
    write_json_artifact(out_dir, "max_claim_resource_map.json", claim_resource_map)

    lines = ["# Max Resource Validation Log", "", f"- Seed: {args.seed}", ""]
    for item in resources:
        lines.append(f"## {item['resource_name']}")
        lines.append(f"- Status: {item['status']}")
        if item.get("impracticality_code"):
            lines.append(f"- Impracticality: {item['impracticality_code']}")
        lines.append(f"- Fallback: {item['fallback']}")
        lines.append(f"- Claim impact: {item['comparability_impact']}")
        for attempt in item["attempts"]:
            lines.append(f"- Command: `{attempt['command']}`")
            lines.append(f"  - Return code: {attempt['returncode']}")
            if attempt.get("failure_signature"):
                lines.append(f"  - Failure signature: `{attempt['failure_signature']}`")
        lines.append("")
    (out_dir / "max_resource_validation_log.md").write_text("\n".join(lines), encoding="utf-8")

    # Internet-backed licensing and reproducibility evidence log.
    internet_lines = [
        "# Internet Evidence Log",
        "",
        "## Scope",
        "- Objective: commercial-safe replacement attempts for TTS/MOS/retrieval stack.",
        "- Seed: 20260220",
        "",
        "## Replacement Paths Attempted",
        "- Path-R1: CosyVoice2 Apache-2.0 (native)",
        "- Path-R2: CosyVoice2 Apache-2.0 (containerized)",
        "- Path-R3: Parler-TTS Apache-2.0 (native)",
        "- Path-R4: Piper MIT (native)",
        "- Path-R5: EmoV-DB (OpenSLR-115) commercial-safe corpus candidate",
        "",
        "## Command Evidence",
    ]
    for item in resources:
        if item["resource_name"] not in {
            "CosyVoice2_commercial_safe",
            "CosyVoice2_containerized_path",
            "ParlerTTS_commercial_safe",
            "PiperTTS_commercial_safe",
            "EMOV_DB_commercial_safe",
            "RAVDESS",
            "XTTS_v2",
        }:
            continue
        internet_lines.append(f"### {item['resource_name']}")
        internet_lines.append(f"- Status: {item['status']}")
        if item.get("impracticality_code"):
            internet_lines.append(f"- Impracticality: {item['impracticality_code']}")
        for attempt in item["attempts"]:
            cmd = attempt["command"]
            if ("http://" not in cmd) and ("https://" not in cmd) and ("git clone" not in cmd):
                continue
            internet_lines.append(f"- Command: `{cmd}`")
            internet_lines.append(f"  - Return code: {attempt['returncode']}")
            if attempt.get("failure_signature"):
                internet_lines.append(f"  - Failure signature: `{attempt['failure_signature']}`")
        internet_lines.append("")
    (out_dir / "internet_evidence_log.md").write_text("\n".join(internet_lines), encoding="utf-8")

    log_command(log_path, "gate_m_resource_ingestion", f"resources={len(resources)} failed={len(impractical)}")
    print("Gate M resource ingestion complete")


if __name__ == "__main__":
    main()
