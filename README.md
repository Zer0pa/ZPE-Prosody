# ZPE-Prosody

## Package Install

Installable package: `python3.11 -m pip install zpe-prosody`.
Current release: `0.1.1` on [PyPI](https://pypi.org/project/zpe-prosody/).
Source: [Zer0pa/ZPE-Prosody](https://github.com/Zer0pa/ZPE-Prosody/).

```bash
python3.11 -m pip install zpe-prosody
```

For full install, smoke, source, and developer commands, [click here](#install-developer-commands-detailed).

---

## `00` ZPE-PROSODY &middot; CONTOUR CODEC

**RESEARCH-READY &middot; RETRIEVAL OPEN**

<h1>Encoding Speech's <span>Shape And Feeling</span></h1>

> Prosodic feature-store codec &middot; pitch, energy, duration, voiced mask &middot; PyPI `zpe-prosody` v0.1.1 is stale &middot; github.com/Zer0pa/ZPE-Prosody

A voice carries more than words. Pitch rises into a question, stress lands on a syllable, and rhythm tells a listener whether the speaker is calm or in a hurry. ZPE-Prosody captures that shape as a deterministic `ZPRS/v1` stream at **13.0&times; mean compression** and **0.64% voiced-F0 RMSE** on 100 LibriSpeech `test-clean` utterances.

It stores acoustic prosody cues, not emotion, intent, semantic meaning, or a speaker-state diagnosis.

**The encoder is the product.** Retrieval misses target. Transfer is paused. Both limits are named here instead of hidden behind the compression win.

<p align="center">
  <img src="docs/assets/product-page-mechanics.gif" alt="ZPE-Prosody approved scientific square mechanics diagram showing ZPRS prosody stream mechanics.">
</p>

<p align="center"><strong>Scope:</strong> encoder stream for F0, energy, duration, and voiced mask. Retrieval misses target; transfer remains paused.</p>

---

## `02` Markets

**Adjacent forecasts, not product claims**

> **Speech and language processing '30** &middot; $26.8B &nbsp;&nbsp; **Text-to-speech market '31** &middot; $7.9B &nbsp;&nbsp; **Text-to-speech software '30** &middot; $7.3B &nbsp;&nbsp; **Voice analytics '30** &middot; est. $3.1B &nbsp;&nbsp; **Speech AI / feature-store tooling '30** &middot; est. $1.8B

ZPE-Prosody is a bounded prosodic encoder. Retrieval and transfer are not claimed.

<table width="100%">
<tr>
<td width="50%" valign="top">
<h2><code>03</code> Value of Market</h2>
<h1>$7.3B</h1>
<p>TTS market by 2030; the prosodic feature store beneath it, with the retrieval gap stated.</p>
</td>
<td width="50%" valign="top">
<h2><code>04</code> Insight</h2>
<h1>Speech carries feeling. Its shape can now be held.</h1>
</td>
</tr>
</table>

---

<table width="100%">
<tr>
<td width="50%" valign="top">
<h3><code>05.1</code> Current Tech</h3>
<p><strong>Computed and discarded</strong></p>
<p>Mainstream TTS and voice-analytics stacks repeatedly compute pitch, energy, and timing, then discard the contours or store them as undocumented bytes. Buyers get no shared archive format, no published fidelity number, and no explicit retrieval limit.</p>
</td>
<td width="50%" valign="top">
<h3><code>05.2</code> Our Tech</h3>
<p><strong>The shape, held</strong></p>
<p>ZPE-Prosody stores F0, energy, duration, and voiced mask as a deterministic <code>ZPRS/v1</code> stream. The public receipt is <strong>13.0&times;</strong> mean compression, <strong>0.64%</strong> voiced-F0 RMSE, <strong>2.67 ms</strong> mean encode latency, and four primitive checks passing. Retrieval and transfer are excluded from the product on purpose, with the numbers.</p>
</td>
</tr>
</table>

### `05.3` Benchmarks

**LibriSpeech `test-clean`, 100 utterances**

> **Compression** &middot; **13.0&times;** &nbsp;&nbsp; **F0 RMSE** &middot; **0.64%** &nbsp;&nbsp; **Primitive checks** &middot; **4/4 PASS** &nbsp;&nbsp; **Retrieval** &middot; **MISS, p@5 0.31** &nbsp;&nbsp; **Transfer** &middot; **PAUSED_EXTERNAL**

`PRO-C006` misses target at p@5 **0.31 vs 0.80**. `PRO-C005` transfer is paused; no commercial-safe substitute is proven in-lane.

---

<table width="100%">
<tr>
<td width="34%" valign="top">
<h2><code>06</code> Measurement</h2>
<p><strong>PRO check suite</strong></p>
<h2>Four checks pass. Retrieval and transfer do not.</h2>
</td>
<td width="66%" valign="top">
<h3><code>06.1</code> Comparative Performance</h3>
<p><strong>LibriSpeech contour compression</strong></p>
<p>
<strong>ZPE-Prosody</strong> &mdash; <strong>13.0&times; compression</strong><br>
<strong>gzip</strong> &mdash; ~2.2&times; raw<br>
<strong><code>PRO-C006</code> p@5</strong> &mdash; <strong>0.31 MISS</strong><br>
<strong><code>PRO-C004</code></strong> &mdash; <strong>PASS</strong>
</p>
<p>The primitive encoder checks pass. Retrieval misses at p@5 <strong>0.31 vs 0.80</strong>; OOD p@5 is 0.1707. Transfer remains paused.</p>
</td>
</tr>
</table>

---

## `07` Key Metrics

**LibriSpeech `test-clean`**

<table width="100%">
<tr>
<td width="100%" valign="top">
<h3><code>07.1</code> F0 RMSE &middot; <strong>0.64%</strong></h3>
<p>Voiced-frame error on the 100-utterance LibriSpeech <code>test-clean</code> receipt.</p>
</td>
</tr>
<tr>
<td width="100%" valign="top">
<h3><code>07.2</code> Compression &middot; <strong>13.0&times;</strong></h3>
<p>Mean compression against raw float32 prosody contours in the deterministic <code>ZPRS/v1</code> stream.</p>
</td>
</tr>
<tr>
<td width="100%" valign="top">
<h3><code>07.3</code> Primitive Checks &middot; <strong>4/4 PASS</strong></h3>
<p><code>PRO-C001</code> through <code>PRO-C004</code> pass for the primitive encoder only; this does not override retrieval or transfer gates.</p>
</td>
</tr>
<tr>
<td width="100%" valign="top">
<h3><code>07.4</code> Corpus &middot; <strong>100 utterances</strong></h3>
<p>LibriSpeech <code>test-clean</code>, OpenSLR source, fixed as the public benchmark receipt for this README surface.</p>
</td>
</tr>
<tr>
<td width="100%" valign="top">
<h3><code>07.5</code> Retrieval Target &middot; <strong>0.31 p@5 MISS</strong></h3>
<p>The retrieval gate misses against the 0.80 threshold and stays named as a blocker, not stretched into a hidden product claim.</p>
</td>
</tr>
</table>

---

## `08` Encoder Bounds

# The encoder holds speech's shape. Retrieval does not yet follow.

<table width="100%">
<tr>
<td width="66%" valign="top">
<h3><code>08.1</code> What Round-Trips Exactly</h3>
<p>On 100 LibriSpeech <code>test-clean</code> utterances, the encoder records <strong>13.0&times;</strong> mean compression at <strong>0.64% voiced-F0 RMSE</strong>, with duration RMSE of 0.000 ms across <strong>5/5 hash-identical encoder runs</strong>. The same input bytes produce the same <code>ZPRS/v1</code> stream every time, on every host.</p>
<p><code>PRO-C001</code>..<code>PRO-C004</code> pass on primitive encoder checks. They do not override the retrieval and transfer gates. The page reports both, not one.</p>
</td>
<td width="34%" valign="top">
<h3><code>08.2</code> Honest Blocker</h3>
<p><strong>MISS on <code>PRO-C006</code> retrieval</strong>, p@5 <strong>0.31</strong> vs <strong>0.80</strong>; OOD p@5 <strong>0.1707</strong>. <strong><code>PRO-C005</code> transfer</strong> is <strong>PAUSED_EXTERNAL</strong>; no commercial-safe substitute is proven in-lane. Status packet on <strong>PR #50 branch-public</strong>; PyPI stale at v0.1.1. No transfer-learning product, retrieval product, or TTS-ready system is claimed.</p>
</td>
</tr>
</table>

---

<table width="100%">
<tr>
<td width="33%" valign="top">
<h2><code>09</code> A Voice with a Fidelity Receipt</h2>
</td>
<td width="67%" valign="top">
<h3><code>09.1</code> The Ambition</h3>
<p>The product is a bounded <code>ZPRS/v1</code> feature store for the shape of speech: F0, energy, duration, and voiced mask. TTS teams, call-centre analytics owners, and linguistics labs can store, ship, and re-read prosody with a stated fidelity per recording. Retrieval and transfer arrive later, on their own terms.</p>
</td>
</tr>
</table>

<table width="100%">
<tr>
<td width="33%" valign="top">
<h3><code>09.2</code> What Works Now</h3>
<h2>The prosodic encoder ships with a fidelity number per frame and a public compression figure.</h2>
</td>
<td width="67%" valign="top">
<h3><code>09.3</code> What's Still Open</h3>
<h2>Retrieval misses target at p@5 0.31 vs 0.80. Transfer is paused on an external dependency.</h2>
</td>
</tr>
</table>

<table width="100%">
<tr>
<td width="100%" valign="top">
<h3><code>09.4</code> Feature Stores &middot; Near-term, 12-24 mo</h3>
<p><strong>TTS teams stop drowning in contour bytes.</strong> A TTS platform keeping pitch and energy contours for thousands of speaker voices and styles cuts feature-store storage by roughly 87% against its current gzip baseline. The same archive holds many more voices on the same disk.</p>
</td>
</tr>
<tr>
<td width="100%" valign="top">
<h3><code>09.5</code> Fidelity &middot; Near-term, 12-24 mo</h3>
<p><strong>Voice pipelines inherit a pitch receipt.</strong> A voice-cloning engineer who round-trips a speaker through the codec sees the F0 error per utterance, <strong>0.64% on LibriSpeech</strong>, before the model ingests the contour. Pitch drift becomes a dashboard number, not a listener complaint.</p>
</td>
</tr>
<tr>
<td width="100%" valign="top">
<h3><code>09.6</code> Call Centres &middot; Mid-term, 24-48 mo</h3>
<p><strong>Analytics vendors archive prosody, not just transcripts.</strong> A call-centre analytics platform that already stores transcripts can store prosody beside them at a tractable cost. Emotion-AI and sentiment systems get to work from the actual shape of how a customer spoke, not a downstream summary of it.</p>
</td>
</tr>
<tr>
<td width="100%" valign="top">
<h3><code>09.7</code> Linguistics &middot; Mid-term, 24-48 mo</h3>
<p><strong>Prosody corpora become comparable.</strong> A linguistics lab studying stress and intonation across dialects can compress a multi-year recording corpus into a portable feature store with a stated pitch error. A peer can reproduce the analysis on the same bytes, not on a re-derived contour.</p>
</td>
</tr>
<tr>
<td width="100%" valign="top">
<h3><code>09.8</code> Disclosure &middot; Paradigm, 48 mo+</h3>
<p><strong>Speech feature codecs get fidelity terms.</strong> A market in which prosodic codecs publish compression, F0 RMSE, and the retrieval limit side by side changes how buyers procure speech tooling. A TTS vendor can talk to a regulator and a customer with the same numbers, units, and corpus.</p>
</td>
</tr>
</table>

---

<a id="install-developer-commands-detailed"></a>

## Install / Developer Commands Detailed

<!-- INSTALL-DX:START -->
#### Package Install

Installable package: `python3.11 -m pip install zpe-prosody`.
Current release: `0.1.1` on [PyPI](https://pypi.org/project/zpe-prosody/).
Source: [Zer0pa/ZPE-Prosody](https://github.com/Zer0pa/ZPE-Prosody/).

```bash
python3.11 -m pip install zpe-prosody
```

Import smoke:

```bash
python3.11 - <<'PY'
import importlib.metadata as md
import zpe_prosody

print("zpe-prosody", md.version("zpe-prosody"))
PY
```

Install success only proves package acquisition/import. Product scope, stale PyPI state, platform limits, and blockers remain in the front-door sections below.
- PyPI copy is stale; retrieval and transfer blockers below are not altered by install success.
<!-- INSTALL-DX:END -->

#### Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make repo-sanity
make package-sanity
make test
```

Optional API wrapper dependency:

```bash
python -m pip install ".[api]"
```

The base wheel ships only `src/zpe_prosody`. No CLI or historical gate harness is packaged as a runtime contract. Read [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) before widening any claim from this repo state.

---
