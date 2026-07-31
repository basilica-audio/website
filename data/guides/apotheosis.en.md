# Apotheosis — how-to guide

*Practical settings for the true-peak brickwall limiter, grounded in the factory presets.*

## Where it belongs

Apotheosis belongs at the very end of the master bus, after every other processor — EQ, bus compression, saturation — has already done its job:

```
Mix bus → EQ/bus compression/saturation → Apotheosis (true-peak limiter) → export/streaming platform
```

It's not meant for individual tracks; use it once, on the master, as the final safety net and loudness stage before bouncing. Because it works in the true-peak (oversampled) domain rather than just the sample domain, it also catches inter-sample overshoot a plain sample-peak limiter would miss — the kind that shows up as clipping/distortion only after a track is transcoded to a lossy streaming format.

## Quick-start settings

### Streaming-safe master — *Transparent Mastering*

Input Gain 3 dB, Ceiling −1 dBTP, Release 60 ms, Lookahead 10 ms, **Dither 24-bit, True Peak Guard on**, Style **Transparent**, Auto Release 50%, Noise Shaping Weighted.

Style: Transparent is the recommended mastering default among the four v0.4.0 styles — the best transparency-per-dB, using the FIR attack smoother's full-lookahead span. True Peak Guard turns Ceiling from a margin-based promise into a measured one: a compliant delivery meter's own measurement runs on the final downsampled output and ducks by exactly the excess if anything still reads over Ceiling.

### Loud, dense, modern master — *Punchy Loud Style*, *Dense/Loud Modern*

Punchy Loud Style: Input Gain 6 dB, Release 30 ms, Lookahead 4 ms, **Clip Mix 35%**, Auto Release 40%, Style **Punchy**.
Dense/Loud Modern: Input Gain 6 dB, Attack 10 ms, Auto Release 50%, Clip Mix 35%, Release Curve Smooth.

Style: Punchy uses a narrower FIR smoother and a higher fast-release depth cap than Transparent — it deliberately lets transient tops through harder, trading some transparency for perceived loudness. Clip Mix at 35% blends in the tanh soft-clip character on top, a common modern loudness-maximizer move, still passing through the same final hard ceiling clamp so the never-exceed-ceiling guarantee holds regardless.

### Punchy master with a classifier assist — *Punchy Master*

Input Gain 3 dB, Release 20 ms, Lookahead 1 ms, **Attack 25 ms**, Auto Release 30%.

Attack here is the transient/sustain classifier (Classic-style Attack, distinct from the Style-mode FIR smoother span) — it lets brief transient peaks recover their gain near-instantly rather than following the normal Release-governed path, the reference class's documented "short lookahead + long attack + fast release" recipe for maximizing perceived loudness while preserving punch.

### Safe archival / true-peak-critical delivery — *Safe Archival (True Peak)*

Input Gain 0 dB, **Ceiling −2 dBTP**, Release 120 ms, Lookahead 20 ms, Style **Safe**, **Oversampling 16x, OS Filter Linear Phase**, True Peak Guard on, Dither 24-bit.

Style: Safe is the maximum-smoothness option — three cascaded FIR boxes rather than one or two, the widest fast/slow release split of the five styles — appropriate for classical, acoustic, or archival material where any audible gain movement is worse than a little less loudness. 16x Linear Phase oversampling costs real latency and CPU but delivers the lowest published alias floor (−100 dBc).

### Wide-image-preserving master — *Wide Image Preserve*

**Stereo Link 40%**, Attack 5 ms, Release Curve Smooth, Auto Release 20%.

Stereo Link below 100% lets each channel detect and limit progressively more independently — the setting for when a hard-panned peak in one channel would otherwise pull the *opposite* channel's gain down with it, at the cost of the stereo image no longer being perfectly locked under gain reduction.

### Clean, dithered export — *Clean Export (Dithered)*

Input Gain 0 dB, Clip Mix 0%, **Dither 16-bit, Dither Shape Shaped**, Attack 0 ms, Auto Release 0%.

A transparent limiter pass with nothing else engaged, plus dither for a final fixed-bit-depth bounce — the starting point for auditioning whether Dither Shape's psychoacoustic shaping is worth using on a given master.

## Recipes

1. **Streaming master at around −14 LUFS.** Style Transparent, Ceiling −1 dBTP, True Peak Guard on, Input Gain raised only until the Integrated LUFS readout (BS.1770-4 gated metering, implemented directly) settles near your target — most streaming platforms normalize down anyway, so pushing louder mostly costs dynamic range without gaining audible loudness once the platform turns it back down. *Why:* True Peak Guard is what makes the Ceiling number true rather than probable — a measured BS.1770-4 true-peak detector runs on the actual downsampled output, the same measurement a compliant delivery meter performs, so what you see is what ships.

2. **Club or physical-release master.** Style Punchy or Classic with Clip Mix raised to taste (25–50%), Ceiling pushed toward −0.3 to −1 dBTP rather than the streaming-safe −1 to −2 dBTP range, Input Gain driven harder for more sustained gain reduction. *Why:* a club/physical master has more room under the ceiling and less reason to leave headroom for a platform's own loudness normalization — Clip Mix's tanh character on top of gain reduction is the deliberate "modern loudness" trade-off appropriate to a louder target.

3. **Deciding how hard you're actually limiting.** Enable **Delta**, push Input Gain until you can identify individual instruments in the Delta signal, then back off. *Why:* Delta replaces the output with exactly what the limiter removed — the fastest, most reliable way to judge how hard you're limiting, far more trustworthy than deciding by ear at two different loudnesses (where louder always sounds better regardless of quality).

4. **A/B-ing Input Gain settings honestly.** Enable **Unity Gain** while you move Input Gain. *Why:* Unity Gain trims the output by exactly minus your Input Gain, so you hear the *character* of more limiting without the level difference — without it, a louder setting will sound better purely because it's louder, not because it's actually an improvement.

5. **Picking an oversampling factor without second-guessing your ears.** Leave Oversampling at 4x Minimum Phase unless Clip Mix is meaningfully engaged or you're doing archival/mastering-for-transcode work — set it once at the start of a session, not mid-mix. *Why:* raising the factor only reduces alias energy generated by hard nonlinearity (the Clip Mix path, and the gain envelope's own sharp edges); on material that barely touches the ceiling at 0% Clip Mix, there's very little alias energy to remove in the first place, so the audible difference is close to nothing while the CPU/latency cost is real.

> **Theory — why true peak is not the same number as sample peak.** A digital file only stores discrete samples, but the analog waveform a D/A converter (or a lossy codec's decoder) reconstructs from them can peak *between* samples, higher than any individual sample value shows. A limiter working purely in the sample domain can let a signal through that reads "safe" on an ordinary peak meter but clips after conversion to analog, or after transcoding to a lossy streaming format that reconstructs the same inter-sample overshoot. Apotheosis's true-peak detection runs inside an oversampled domain (4x/8x/16x) specifically so it can see — and hold a ceiling against — that reconstructed peak, not just the samples as stored. True Peak Guard goes one step further: rather than trusting the oversampled detection alone, it re-measures the actual downsampled output with a BS.1770-4-compliant detector — the same standard a delivery meter uses — and corrects only if that measurement, not just the internal estimate, reads over Ceiling.

## Pitfalls

- **Lookahead, Oversampling, and OS Filter are prepare-latched "setup" parameters, not live-automatable.** Changing any of them only takes effect the next time your host re-initializes the plugin (sample-rate change, transport stop/start, reopening the project) — set them at the start of a session, not mid-mix, and don't expect an instant audible difference from moving them during playback.
- **The seven v0.4.0 controls (Style, Oversampling, OS Filter, True Peak Guard, Noise Shaping, Delta, Unity Gain) have no dedicated editor controls yet** — reach your host's generic parameter view to automate or set them until the M3 GUI ships.
- **Dither is not re-clamped to the Ceiling at the base rate** — a discrete output sample can sit up to about 1 LSB past the nominal Ceiling (roughly −90 dBFS at 16-bit, −138 dBFS at 24-bit). This is standard, expected dithered-output behaviour, well inside the true-peak test tolerance, not a guarantee violation.
- **The measured ceiling guarantee is a 4x-meter guarantee.** A higher-resolution reference meter can legitimately read a little above Ceiling on certain content near 0.45x Nyquist — a property of the BS.1770-4 standard itself, not of this plugin.
- **Weighted noise shaping is fitted for 44.1/48 kHz delivery** and is used unchanged at higher project rates, where its fit to the audibility curve no longer holds as precisely.
- **Delta and Unity Gain are monitor modes — never render modes.** Delta bypasses dither since you're auditioning, not rendering; turn both off before you bounce.
- **When Noise Shaping is set to Weighted, it supersedes Dither Shape entirely** — the Flat/Shaped choice stops doing anything at that point.
- **The voicing throughout is research-derived from published documentation and general DSP/dithering literature, not measured against, benchmarked against, or reverse-engineered from any competitor's binary.**
