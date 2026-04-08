# Gate Status

This file summarizes the accepted commercial-gate state for the current ZPE Prosody lane.

## Current Lane Verdict

Overall lane verdict: `FAIL`

Why: both commercial gates must pass for lane promotion, and they do not.

- `PRO-C005`: `PAUSED_EXTERNAL`
- `PRO-C006`: `FAIL`

## PRO-C005

Accepted state: `PAUSED_EXTERNAL`

What is blocking it:

- The accepted transfer stack depends on XTTS.
- XTTS is not commercially admissible for this lane.
- No commercial-safe replacement path was executed successfully in-lane.

What was attempted:

- `CosyVoice2_commercial_safe`
- `CosyVoice2_containerized_path`
- `ParlerTTS_commercial_safe`
- `PiperTTS_commercial_safe`

Replacement-path status:

- all recorded replacement attempts are `FAILED`

What would unblock it:

- a commercial-safe transfer substitute must run end to end on the accepted evaluation path
- the substitute must produce executable evidence, not just a paper replacement candidate
- that evidence then has to satisfy the gate requirements for transfer closure

## PRO-C006

Accepted state: `FAIL`

What retrieval closure means:

- the retrieval path has to work on the accepted emotional-speech evaluation route
- the evidence has to clear the retrieval threshold on the real-corpus leg and the OOD stress leg

What was attempted:

- real `RAVDESS` retrieval evaluation
- OOD retrieval stress evaluation using the tracked `emovome_or_emovoice` path

Why it failed:

- the recorded real-corpus retrieval score is `p@5 = 0.3066666666666667`
- the gate threshold is `0.8`
- the recorded OOD retrieval score is `0.17073170731707318`
- the OOD threshold is `0.65`

This is not an unattempted path. The accepted evidence says the retrieval route ran and missed by a large margin.

What would unblock it:

- redesign the retrieval method so the real and OOD evaluations clear threshold, or
- explicitly descope the claim so the gate no longer demands this level of retrieval closure

## Promotion Rule

Lane promotion does not happen until both `PRO-C005` and `PRO-C006` pass.
