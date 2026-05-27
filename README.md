# ZPE-Prosody

## Install / Developer Commands

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

## `00` ZPE-PROSODY &middot; CONTOUR CODEC

**PR #50 DRAFT &middot; BRANCH-PUBLIC**

# Speech's Shape and Feeling Encoded

> Prosodic feature-store codec &middot; pitch, energy, duration, voiced mask &middot; PyPI `zpe-prosody` v0.1.1 &middot; github.com/Zer0pa/ZPE-Prosody

A voice carries more than words. Pitch rises into a question, stress lands on a syllable, and rhythm tells a listener whether the speaker is calm or in a hurry. ZPE-Prosody captures that shape as a deterministic `ZPRS/v1` stream at **13.0&times; mean compression** and **0.64% voiced-F0 RMSE** on 100 LibriSpeech `test-clean` utterances.

**The encoder is the product.** Retrieval misses target. Transfer is paused. Both limits are named here instead of hidden behind the compression win.

<p align="center">
  <img src="docs/assets/product-page-mechanics.gif" alt="ZPE-Prosody approved scientific square mechanics diagram showing ZPRS prosody stream mechanics.">
</p>

<p align="center"><strong>Scope:</strong> encoder stream for F0, energy, duration, and voiced mask. Retrieval misses target; transfer remains paused.</p>

---

<table width="100%">
<tr>
<td width="64%" valign="top">
<h2><code>02</code> Markets</h2>
<p><strong>Adjacent forecasts, not product claims</strong></p>
<p>
<strong>Speech and language processing '30</strong> &mdash; $26.8B<br>
<strong>Text-to-speech market '31</strong> &mdash; $7.9B<br>
<strong>Text-to-speech software '30</strong> &mdash; $7.3B<br>
<strong>Voice analytics '30</strong> &mdash; est. $3.1B<br>
<strong>Speech AI / feature-store tooling '30</strong> &mdash; est. $1.8B
</p>
<p>ZPE-Prosody is a bounded prosodic encoder. Retrieval and transfer are not claimed.</p>
</td>
<td width="36%" valign="top">
<h2><code>03</code> Value</h2>
<h1>$7.3B</h1>
<p>TTS market by 2030; the prosodic feature store beneath it, with the retrieval gap stated.</p>
</td>
</tr>
</table>

---

## `04` Insight

# Speech carries feeling. Its shape can now be held.

<table width="100%">
<tr>
<td width="46%" valign="top">
<h3><code>05.1</code> Current Tech</h3>
<p><strong>Computed and discarded</strong></p>
<p>Mainstream TTS and voice-analytics stacks repeatedly compute pitch, energy, and timing, then discard the contours or store them as undocumented bytes. Buyers get no shared archive format, no published fidelity number, and no explicit retrieval limit.</p>
</td>
<td width="54%" valign="top">
<h3><code>05.2</code> Our Tech</h3>
<p><strong>The shape, held</strong></p>
<p>ZPE-Prosody stores F0, energy, duration, and voiced mask as a deterministic <code>ZPRS/v1</code> stream. The public receipt is <strong>13.0&times;</strong> mean compression, <strong>0.64%</strong> voiced-F0 RMSE, <strong>2.67 ms</strong> mean encode latency, and four primitive checks passing.</p>
</td>
</tr>
</table>

### `05.3` Benchmarks

**LibriSpeech `test-clean`, 100 utterances**

| Compression | F0 RMSE | Primitive checks | Retrieval | Transfer |
| ---: | ---: | :---: | :---: | :---: |
| **13.0&times;** | **0.64%** | **4/4 PASS** | **MISS, p@5 0.31** | **PAUSED_EXTERNAL** |

`PRO-C006` misses target at p@5 **0.31 vs 0.80**. `PRO-C005` transfer is paused; no commercial-safe substitute is proven in-lane.

---

<table width="100%">
<tr>
<td width="34%" valign="top">
<h2><code>06</code> Measurement</h2>
<p><strong>PRO check suite</strong></p>
<h1>Four checks pass. Retrieval and transfer do not.</h1>
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
<td width="20%" align="center" valign="top">
<p><code>07.1</code> <strong>F0</strong></p>
<h2>0.64%</h2>
<p>voiced frames</p>
</td>
<td width="20%" align="center" valign="top">
<p><code>07.2</code> <strong>Compression</strong></p>
<h2>13.0&times;</h2>
<p>mean vs raw</p>
</td>
<td width="20%" align="center" valign="top">
<p><code>07.3</code> <strong>Primitive</strong></p>
<h2>4/4</h2>
<p>PASS</p>
</td>
<td width="20%" align="center" valign="top">
<p><code>07.4</code> <strong>Corpus</strong></p>
<h2>100</h2>
<p>utterances</p>
</td>
<td width="20%" align="center" valign="top">
<p><code>07.5</code> <strong>Retrieval</strong></p>
<h2>0.31</h2>
<p>p@5 MISS</p>
</td>
</tr>
</table>

---

## `08` Encoder Bounds

# The encoder holds speech's shape. Retrieval does not yet follow.

### `08.1` What Round-Trips Exactly

On 100 LibriSpeech `test-clean` utterances, the encoder records **13.0&times;** mean compression at **0.64% voiced-F0 RMSE**, with duration RMSE of 0.000 ms across **5/5 hash-identical encoder runs**. The same input bytes produce the same `ZPRS/v1` stream every time, on every host.

`PRO-C001`..`PRO-C004` pass on primitive encoder checks. They do not override the retrieval and transfer gates.

> **`08.2` Honest Blocker**
> **MISS on `PRO-C006` retrieval**, p@5 **0.31** vs **0.80**; OOD p@5 **0.1707**. **`PRO-C005` transfer** is **PAUSED_EXTERNAL**. Status packet is PR #50 branch-public; PyPI is stale at v0.1.1. No transfer-learning product, retrieval product, or TTS-ready system is claimed.

---

## `09` A Voice with a Fidelity Receipt

### `09.1` The Ambition

The product is a bounded `ZPRS/v1` feature store for the shape of speech: F0, energy, duration, and voiced mask. TTS teams, call-centre analytics owners, and linguistics labs can store, ship, and re-read prosody with a stated fidelity per recording. Retrieval and transfer arrive later, on their own terms.

<table width="100%">
<tr>
<td width="48%" valign="top">
<h3><code>09.2</code> What Works Now</h3>
<h1>The prosodic encoder ships with a fidelity number per frame and a public compression figure.</h1>
</td>
<td width="52%" valign="top">
<h3><code>09.3</code> What's Still Open</h3>
<h1>Retrieval misses target at p@5 0.31 vs 0.80. Transfer is paused on an external dependency.</h1>
</td>
</tr>
</table>

<table width="100%">
<tr>
<td width="24%" valign="top">
<h3><code>09.4</code></h3>
<p><strong>Feature Stores</strong><br>Near-term, 12-24 mo</p>
</td>
<td width="76%" valign="top">
<h3>TTS teams stop drowning in contour bytes</h3>
<p>A TTS platform keeping pitch and energy contours for thousands of speaker voices and styles cuts feature-store storage by roughly 87% against its current gzip baseline. The same archive holds many more voices on the same disk.</p>
</td>
</tr>
</table>

<table width="100%">
<tr>
<td width="22%" valign="top">
<h3><code>09.5</code></h3>
<p><strong>Fidelity</strong><br>Near-term, 12-24 mo</p>
</td>
<td width="78%" valign="top">
<h3>Voice pipelines inherit a pitch receipt</h3>
<p>A voice-cloning engineer who round-trips a speaker through the codec sees the F0 error per utterance, <strong>0.64% on LibriSpeech</strong>, before the model ingests the contour. Pitch drift becomes a dashboard number, not a listener complaint.</p>
</td>
</tr>
</table>

<table width="100%">
<tr>
<td width="25%" valign="top">
<h3><code>09.6</code></h3>
<p><strong>Call Centres</strong><br>Mid-term, 24-48 mo</p>
</td>
<td width="75%" valign="top">
<h3>Analytics vendors archive prosody, not just transcripts</h3>
<p>A call-centre analytics platform that already stores transcripts can store prosody beside them at a tractable cost. Emotion-AI and sentiment systems get to work from the actual shape of how a customer spoke, not a downstream summary of it.</p>
</td>
</tr>
</table>

<table width="100%">
<tr>
<td width="23%" valign="top">
<h3><code>09.7</code></h3>
<p><strong>Linguistics</strong><br>Mid-term, 24-48 mo</p>
</td>
<td width="77%" valign="top">
<h3>Prosody corpora become comparable</h3>
<p>A linguistics lab studying stress and intonation across dialects can compress a multi-year recording corpus into a portable feature store with a stated pitch error. A peer can reproduce the analysis on the same bytes, not on a re-derived contour.</p>
</td>
</tr>
</table>

<table width="100%">
<tr>
<td width="22%" valign="top">
<h3><code>09.8</code></h3>
<p><strong>Disclosure</strong><br>Paradigm, 48 mo+</p>
</td>
<td width="78%" valign="top">
<h3>Speech feature codecs get fidelity terms</h3>
<p>A market in which prosodic codecs publish compression, F0 RMSE, and the retrieval limit side by side changes how buyers procure speech tooling. A TTS vendor can talk to a regulator and a customer with the same numbers, units, and corpus.</p>
</td>
</tr>
</table>
