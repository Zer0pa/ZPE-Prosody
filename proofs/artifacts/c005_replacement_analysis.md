# PRO-C005 Replacement Analysis

## Accepted Gate State

Current accepted gate state: `PAUSED_EXTERNAL`

Accepted blocker from the tracked wave-1 bundle:

> XTTS is CPML/non-permissive and no executable commercial-safe transfer substitute was proven in-lane.

This means the blocker is not the proxy metric itself. The lane is blocked because no commercially admissible transfer stack was executed end to end on the accepted path.

## Exact External Dependency Blocking C005

The accepted transfer path depends on XTTS.

Why that matters:

- XTTS was the intended transfer stack for the accepted lane
- XTTS is treated as non-permissive for this commercialization gate
- the wave-1 bundle records `xtts_transfer_executed=false`
- the wave-1 bundle records `mos_evidence_executed=false`

So the external dependency is not just "a TTS model." It is a commercially safe transfer-capable stack that can substitute for XTTS and still satisfy the accepted evaluation flow.

## What Was Already Attempted In-Lane

The tracked risk register records these replacement paths:

- `CosyVoice2_commercial_safe`: `FAILED`
- `CosyVoice2_containerized_path`: `FAILED`
- `ParlerTTS_commercial_safe`: `FAILED`
- `PiperTTS_commercial_safe`: `FAILED`

The tracked bundle therefore supports this narrower statement:

- replacement search happened
- no replacement path was closed in-lane

## Current Official-Source Check

Current official-source check performed on `2026-04-06`:

- `CosyVoice` official repo and license:
  - source: <https://github.com/FunAudioLLM/CosyVoice>
  - license: Apache 2.0
  - capability signal: the official README describes zero-shot voice cloning and voice conversion
- `MeanVC` official repo and license:
  - source: <https://github.com/ASLP-lab/MeanVC>
  - license: Apache 2.0
  - capability signal: the official README describes lightweight streaming zero-shot voice conversion for real-time timbre transfer
- `Parler-TTS` official repo and license:
  - source: <https://github.com/huggingface/parler-tts>
  - license: Apache 2.0
  - capability signal: permissive TTS, but not a direct source-to-target transfer system
- `Piper` official repo and license:
  - source: <https://github.com/rhasspy/piper>
  - license: MIT
  - capability signal: permissive TTS runtime, not a transfer stack

## Replacement Candidate Assessment

| Candidate | License | Transfer fit | Current evidence | Practical verdict |
|---|---|---|---|---|
| `CosyVoice` | Apache 2.0 | Strong | Already attempted and failed in-lane | Best already-known rerun candidate |
| `MeanVC` | Apache 2.0 | Strong | Not attempted in the tracked lane | Best net-new candidate if semantic equivalence matters |
| `Parler-TTS` | Apache 2.0 | Weak to medium | Attempted and failed in-lane | Not a convincing direct closure path |
| `Piper` | MIT | Weak | Attempted and failed in-lane | Useful TTS infrastructure, not transfer closure |

The key distinction is semantic fit:

- `CosyVoice` and `MeanVC` are credible because they overlap with cloning or conversion behavior
- `Parler-TTS` and `Piper` are permissive, but permissive alone is not enough

## Is The Replacement Path Viable?

Yes, but only in the narrow sense that viable candidates exist.

No, in the stronger sense of "ready to promote the gate today."

The current proof state does **not** support a claim that `PRO-C005` is nearly closed. It supports only this:

- there are commercially safer candidate stacks
- the repo has not yet executed one successfully on the accepted path
- the replacement path remains plausible but unproven

## Work Plan

1. Rebuild the transfer rerun environment on Python `3.11`.
2. Lock the environment before running any candidate stack.
3. Prioritize one strong semantic replacement at a time:
   - first `CosyVoice`
   - then `MeanVC` if `CosyVoice` fails again
4. Re-run the accepted transfer flow end to end.
5. Generate real transfer outputs and executed MOS evidence.
6. Re-evaluate `PRO-C005` only after that evidence exists.

## Decision

Current replacement-path verdict: `plausible but unproven`

The gate should remain `PAUSED_EXTERNAL` until a commercial-safe transfer substitute is actually executed and evidenced in-lane.
