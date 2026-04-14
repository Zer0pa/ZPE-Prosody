# Max Resource Validation Log

- Seed: 20260220

## UTMOSv2
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Fallback: speechmos_if_available_else_proxy_mos
- Claim impact: High if unavailable: transfer MOS claim remains unclosed.
- Command: `rm -rf '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/UTMOSv2' && git clone --depth 1 https://github.com/sarulab-speech/UTMOSv2 '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/UTMOSv2'`
  - Return code: 0
- Command: `if [ -f '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/UTMOSv2/requirements.txt' ]; then '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install -r '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/UTMOSv2/requirements.txt'; else '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install -e '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/UTMOSv2'; fi`
  - Return code: 0
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python' -c "import utmosv2; print('utmosv2_ok')"`
  - Return code: 1
  - Failure signature: `Traceback (most recent call last):`

## SpeechMOS
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Fallback: utmosv2_if_available_else_proxy_mos
- Claim impact: High if unavailable: no independent MOS cross-check.
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install speechmos onnxruntime`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip`
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python' -c "from speechmos import dnsmos; print('speechmos_dnsmos_ok')"`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python`

## RAVDESS
- Status: SUCCESS
- Fallback: deterministic_ravdess_like_fixture
- Claim impact: High if unavailable: retrieval cannot be proven on real emotional corpus.
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install datasets soundfile`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip`
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python' -c "import json, wave, struct, pathlib; from datasets import load_dataset; out=pathlib.Path('/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/ravdess'); out.mkdir(parents=True, exist_ok=True); ds=load_dataset('narad/ravdess', split='train[:120]'); meta=[]; 
for i,row in enumerate(ds):
  audio=row['audio']; arr=audio['array']; sr=int(audio['sampling_rate']);
  label=str(row.get('emotion', row.get('label', 'unknown')));
  path=out / f'ravdess_{i:04d}_{label}.wav';
  with wave.open(str(path),'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr);
    pcm=bytearray();
    for v in arr:
      iv=max(-32768,min(32767,int(v*32767)));
      pcm.extend(struct.pack('<h',iv));
    w.writeframes(bytes(pcm));
  meta.append({'path':str(path),'label':label,'sr':sr});
(out / 'manifest.json').write_text(json.dumps({'items':meta}, indent=2)); print(len(meta))"`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python`
- Command: `curl -s https://zenodo.org/api/records/1188976 | rg -n "license|rights|access_right"`
  - Return code: 0
- Command: `test -f '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/ravdess/manifest.json'`
  - Return code: 0

## torchcrepe
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Fallback: fallback_zero_crossing_f0
- Claim impact: Medium-to-high: extractor fidelity comparability drops if missing.
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install --index-url https://download.pytorch.org/whl/cpu torch torchaudio`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip`
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install torchcrepe`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip`
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python' -c "import torch, torchcrepe; print(torch.__version__)"`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python`

## Parselmouth
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Fallback: fallback_rms_energy_duration
- Claim impact: Medium: missing Praat-standard extraction weakens equivalence.
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install praat-parselmouth`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip`
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python' -c "import parselmouth; print(parselmouth.__version__)"`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python`

## XTTS_v2
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Fallback: objective_transfer_proxy_without_tts
- Claim impact: High: no true transfer synthesis means PRO-C005 cannot be fully closed.
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install TTS`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip`
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install 'transformers==4.41.2'`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip`
- Command: `curl -L -s https://huggingface.co/coqui/XTTS-v2/raw/main/README.md | rg -n "license|coqui-public-model-license|cpml|non-commercial" -i`
  - Return code: 0
- Command: `COQUI_TOS_AGREED=1 TTS_HOME='/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/tts_cache' '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python' -c "import json, pathlib; from TTS.api import TTS; manifest=pathlib.Path(r'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/ravdess/manifest.json'); items=json.loads(manifest.read_text()).get('items', []); speaker=next(pathlib.Path(i['path']) for i in items if pathlib.Path(i['path']).exists()); tts=TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2', progress_bar=False, gpu=False); tts.tts_to_file(text='Prosody transfer validation sentence.', speaker_wav=str(speaker), language='en', file_path=r'artifacts/2026-02-20_zpe_prosody_wave1/xtts_probe.wav'); print('xtts_ok')"`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python`

## CosyVoice2_commercial_safe
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Fallback: runpod_gpu_transfer_with_permissive_tts
- Claim impact: High: commercial-safe transfer closure blocked if CosyVoice2 path is unavailable.
- Command: `rm -rf '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/CosyVoice' && git clone --depth 1 https://github.com/FunAudioLLM/CosyVoice '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/CosyVoice'`
  - Return code: 0
- Command: `git -C '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/CosyVoice' submodule update --init --recursive`
  - Return code: 0
- Command: `test -f '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/CosyVoice/LICENSE' && rg -n "Apache" '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/CosyVoice/LICENSE'`
  - Return code: 0
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install -r '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/CosyVoice/requirements.txt'`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip`
- Command: `PYTHONPATH='/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/CosyVoice:$PYTHONPATH' '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python' -c "from cosyvoice.cli.cosyvoice import CosyVoice; print('cosyvoice_ok')"`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python`

## CosyVoice2_containerized_path
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Fallback: runpod_gpu_transfer_with_permissive_tts
- Claim impact: Medium-to-high: containerized fallback unavailable in-lane if docker build/runtime fails.
- Command: `docker --version`
  - Return code: 0
- Command: `docker build -t cosyvoice_runtime_probe '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/CosyVoice/runtime/python'`
  - Return code: 1
  - Failure signature: `DEPRECATED: The legacy builder is deprecated and will be removed in a future release.`

## ParlerTTS_commercial_safe
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Fallback: runpod_gpu_transfer_with_parler_tts
- Claim impact: Medium-to-high: no direct speaker-clone transfer; usable only as commercialization-safe synthesis substitute.
- Command: `curl -L -s https://raw.githubusercontent.com/huggingface/parler-tts/main/LICENSE | rg -n "apache" -i`
  - Return code: 0
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install parler-tts accelerate`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip`
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python' - <<'PY'
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
sf.write(r"artifacts/2026-02-20_zpe_prosody_wave1/parler_probe.wav", arr, int(model.config.sampling_rate))
print("parler_ok")
PY`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python`
- Command: `test -f 'artifacts/2026-02-20_zpe_prosody_wave1/parler_probe.wav'`
  - Return code: 1
  - Failure signature: `returncode_1`

## PiperTTS_commercial_safe
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Fallback: runpod_gpu_transfer_with_piper_or_other_permissive_tts
- Claim impact: Medium-to-high: lacks direct XTTS-style voice transfer conditioning.
- Command: `curl -L -s https://raw.githubusercontent.com/rhasspy/piper/master/LICENSE.md | rg -n "mit" -i`
  - Return code: 0
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip' install piper-tts`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/pip`
- Command: `curl -L -o '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/piper_models/en_US-lessac-medium.onnx' https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx`
  - Return code: 0
- Command: `curl -L -o '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/piper_models/en_US-lessac-medium.onnx.json' https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json`
  - Return code: 0
- Command: `printf 'Prosody transfer validation sentence.' | '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/piper' --model '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/piper_models/en_US-lessac-medium.onnx' --config '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/piper_models/en_US-lessac-medium.onnx.json' --output_file 'artifacts/2026-02-20_zpe_prosody_wave1/piper_probe.wav'`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/piper`
- Command: `test -f 'artifacts/2026-02-20_zpe_prosody_wave1/piper_probe.wav'`
  - Return code: 1
  - Failure signature: `returncode_1`

## EMOV_DB_commercial_safe
- Status: FAILED
- Impracticality: IMP-STORAGE
- Fallback: retain_emovoice_ood_with_license_gap_note
- Claim impact: High: EmoV-DB license and data availability must both satisfy commercialization constraints.
- Command: `rm -rf '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db' && git clone --depth 1 https://github.com/numediart/EmoV-DB '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db'`
  - Return code: 0
- Command: `curl -L -s https://www.openslr.org/115/ | rg -n "License|license|CC|commercial" -i`
  - Return code: 0
- Command: `curl -L -s https://raw.githubusercontent.com/numediart/EmoV-DB/master/LICENSE.md | head -n 30`
  - Return code: 0
- Command: `find '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db' -type f \( -name '*.wav' -o -name '*.flac' \) | head -n 5`
  - Return code: 0
- Command: `if [ "$(find '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db' -type f -name '*.wav' | wc -l | tr -d ' ')" -lt 16 ]; then mkdir -p '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db' && curl -L -o '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db/emovdb.zip' https://www.openslr.org/resources/115/emovdb.zip; else echo 'skip_download_has_audio'; fi`
  - Return code: 0
- Command: `if [ -f '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db/emovdb.zip' ]; then unzip -o -q '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db/emovdb.zip' -d '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db'; else echo 'skip_unzip_no_zip'; fi`
  - Return code: 9
  - Failure signature: `[/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db/emovdb.zip]`
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python' -c "import json, pathlib; root=pathlib.Path(r'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db'); root.mkdir(parents=True, exist_ok=True); files=sorted(list(root.rglob('*.wav')) + list(root.rglob('*.flac'))); items=[{'path':str(p),'label':p.parent.name.lower(),'sr':0} for p in files[:240]]; pathlib.Path(r'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db/manifest.json').write_text(json.dumps({'items':items}, indent=2)); print(len(items))"`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python`
- Command: `'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python' -c "import json, pathlib, sys; p=pathlib.Path(r'/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/emov_db/manifest.json'); items=json.loads(p.read_text()).get('items', []) if p.exists() else []; print(len(items)); sys.exit(0 if len(items) >= 16 else 3)"`
  - Return code: 127
  - Failure signature: `zsh:1: no such file or directory: /Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/venv/bin/python`

## emovome_or_emovoice
- Status: SUCCESS
- Fallback: ravdess_only_retrieval_with_declared_ood_gap
- Claim impact: High if unavailable: OOD emotional retrieval stress remains open.
- Command: `rm -rf '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/EmoVoice' && git clone --depth 1 https://github.com/yanghaha0908/EmoVoice '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/EmoVoice'`
  - Return code: 0
- Command: `find '/Users/zer0pa-build/ZPE Multimodality/ZPE Prosody/data/external/EmoVoice' -type f \( -name '*.wav' -o -name '*.flac' \) | head -n 5`
  - Return code: 0
