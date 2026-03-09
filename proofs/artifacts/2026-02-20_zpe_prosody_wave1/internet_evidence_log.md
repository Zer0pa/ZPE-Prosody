# Internet Evidence Log

## Scope
- Objective: commercial-safe replacement attempts for TTS/MOS/retrieval stack.
- Seed: 20260220

## Replacement Paths Attempted
- Path-R1: CosyVoice2 Apache-2.0 (native)
- Path-R2: CosyVoice2 Apache-2.0 (containerized)
- Path-R3: Parler-TTS Apache-2.0 (native)
- Path-R4: Piper MIT (native)
- Path-R5: EmoV-DB (OpenSLR-115) commercial-safe corpus candidate

## Command Evidence
### RAVDESS
- Status: SUCCESS
- Command: `curl -s https://zenodo.org/api/records/1188976 | rg -n "license|rights|access_right"`
  - Return code: 0

### XTTS_v2
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Command: `curl -L -s https://huggingface.co/coqui/XTTS-v2/raw/main/README.md | rg -n "license|coqui-public-model-license|cpml|non-commercial" -i`
  - Return code: 0

### CosyVoice2_commercial_safe
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Command: `rm -rf '/Users/prinivenpillay/ZPE Multimodality/ZPE Prosody/data/external/CosyVoice' && git clone --depth 1 https://github.com/FunAudioLLM/CosyVoice '/Users/prinivenpillay/ZPE Multimodality/ZPE Prosody/data/external/CosyVoice'`
  - Return code: 0

### CosyVoice2_containerized_path
- Status: FAILED
- Impracticality: IMP-COMPUTE

### ParlerTTS_commercial_safe
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Command: `curl -L -s https://raw.githubusercontent.com/huggingface/parler-tts/main/LICENSE | rg -n "apache" -i`
  - Return code: 0

### PiperTTS_commercial_safe
- Status: FAILED
- Impracticality: IMP-COMPUTE
- Command: `curl -L -s https://raw.githubusercontent.com/rhasspy/piper/master/LICENSE.md | rg -n "mit" -i`
  - Return code: 0
- Command: `curl -L -o '/Users/prinivenpillay/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/piper_models/en_US-lessac-medium.onnx' https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx`
  - Return code: 0
- Command: `curl -L -o '/Users/prinivenpillay/ZPE Multimodality/ZPE Prosody/.runtime/maxwave/piper_models/en_US-lessac-medium.onnx.json' https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json`
  - Return code: 0

### EMOV_DB_commercial_safe
- Status: FAILED
- Impracticality: IMP-STORAGE
- Command: `rm -rf '/Users/prinivenpillay/ZPE Multimodality/ZPE Prosody/data/external/emov_db' && git clone --depth 1 https://github.com/numediart/EmoV-DB '/Users/prinivenpillay/ZPE Multimodality/ZPE Prosody/data/external/emov_db'`
  - Return code: 0
- Command: `curl -L -s https://www.openslr.org/115/ | rg -n "License|license|CC|commercial" -i`
  - Return code: 0
- Command: `curl -L -s https://raw.githubusercontent.com/numediart/EmoV-DB/master/LICENSE.md | head -n 30`
  - Return code: 0
- Command: `if [ "$(find '/Users/prinivenpillay/ZPE Multimodality/ZPE Prosody/data/external/emov_db' -type f -name '*.wav' | wc -l | tr -d ' ')" -lt 16 ]; then mkdir -p '/Users/prinivenpillay/ZPE Multimodality/ZPE Prosody/data/external/emov_db' && curl -L -o '/Users/prinivenpillay/ZPE Multimodality/ZPE Prosody/data/external/emov_db/emovdb.zip' https://www.openslr.org/resources/115/emovdb.zip; else echo 'skip_download_has_audio'; fi`
  - Return code: 0
