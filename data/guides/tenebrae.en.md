# Tenebrae — how-to guide

*Practical settings for the main gain stage, grounded in the factory presets.*

## Where it belongs

Tenebrae is the **main gain stage** of the guitar chain — the wall of gain, not the speaker. It has no cabinet simulation by design, so it stays a clean building block: run a tightening boost (Overture, or similar) ahead of it for low-end control, and a cab sim/IR loader (Nave) after it.

```
Guitar → noise gate → tight-boost (optional) → Tenebrae (high-gain distortion) → cab sim/IR loader → mix bus
```

Typical use cases: rhythm chug tones from tight modern to loose vintage-leaning, doom/sludge sag, and anything in between via the Classic/Triode engine choice.

## Quick-start settings

### Modern tight rhythm — *Foundation Chug* / *Adaptive Gate Chug*

Foundation Chug: Tight 90 Hz, Gain 24 dB, Voicing Tight, all tone bands flat, Gate on (Threshold −48 dB, Release 150 ms).
Adaptive Gate Chug (v0.3.0, Triode engine): Tight 110 Hz, Gain 28 dB, Tone Voice Scoop, Bias Shift 120%, Gate Key Pre, Gate Release Mode Auto.

Foundation Chug is the plugin's own "Init"-category starting point — flat tone stack, gate on by default (Tenebrae ships with the gate engaged, unlike every other new control, because the research behind the rework treats a gate as structural to tight chug tone in this genre). Adaptive Gate Chug adds the Triode engine's dynamic bias shift and switches the gate to **Pre** detection — keying off the signal before it hits 28 dB of gain, so quiet notes and silence stay cleanly separated.

### Sagging doom/sludge — *Sagging Doom*

Tight 60 Hz, Gain 22 dB, Voicing Loose, Bass +3 dB, Engine Triode, Power Amp on, Resonance 9 dB, **Sag 75%**, Gate Release 400 ms.

Low Tight setting keeps the low end full and boomy rather than tight — the opposite move from a rhythm-chug preset. Sag this high makes the modelled power supply audibly droop and recover over roughly 120 ms per hit, the compressed, spongy feel doom/sludge parts want; Resonance pushes more low end into the power amp's feedback path on top.

### Bright, aggressive cut-through rhythm — *Bright Aggressive* / *Cut-Through Lead-Adjacent*

Bright Aggressive: Tight 110 Hz, Gain 32 dB, Bright on, Level −2 dB.
Cut-Through Lead-Adjacent: Tight 80 Hz, Gain 30 dB, Mid +2 dB, Treble +2 dB, Bright on, Tone Voice Boost.

Bright engages a fixed pre-cascade high-shelf, modelled on the "bright switch" many high-gain channels carry — because the boosted signal then passes through three cascaded clipping stages, the effect on loudness is subtle by design; what changes is harmonic content and pick-attack sizzle feeding the cascade, not raw output level.

### Vintage/looser voicing — *Loose & Open*, *Vintage Cascade*

Loose & Open: Tight 50 Hz, Gain 16 dB, Voicing Loose, Bass +3 dB, Treble +2 dB, Gate Release 300 ms.

Voicing set to Loose swaps the cascade's fixed per-stage asymmetry and interstage filtering for a softer-driven, wider-band alternative — less asymmetric clipping and looser filtering at every stage than the default Tight voicing, for a more vintage-leaning, airier character.

### Full-bore Triode with power amp — *Feedback Tight Rhythm*, *Triode Foundation*

Feedback Tight Rhythm: Tight 140 Hz, Gain 30 dB, Bright on, Presence 6 dB, Engine Triode, Quality Standard, Power Amp on, Resonance 4 dB, Sag 20%, Gate Key Pre, Gate Range 90 dB.

Gate Range at 90 dB (rather than the default hard Mute) leaves the signal 90 dB down instead of fully silent — often more natural on a sustained part, since the noise floor drops out of the way without the track sounding switched off.

## Recipes

1. **Tight modern chug with a clean gate.** Foundation Chug as a base, Gate Key switched to **Pre**, Gate Hysteresis 3–6 dB. *Why:* at 24+ dB of gain, a post-distortion detector (the default, and the v0.2.0 behaviour) squashes the difference between "not playing" and "playing" down to a few dB — no threshold setting separates them cleanly. Pre-detection keys off a copy of the input taken before the cascade, through a fixed band-pass filter, preserving the guitar's actual dynamic range.

2. **Doom/sludge sag.** Sagging Doom as a base, then ride Sag between 50–90% depending on how spongy you want the response; keep Resonance proportional (higher Sag reads better with more low-frequency depth feeding it). *Why:* Sag and Resonance are both power-amp feedback-path controls, not EQ — Resonance cuts lows out of the feedback loop (which lets more through the amp itself), and Sag squeezes the output transformer's headroom under load. Neither is the same move as turning the post-cascade Bass band up.

3. **Bright rhythm that still sits under vocals.** Bright Aggressive as a base, Mid pulled to −1 to −2 dB (scooped) if the part needs to make room, Tone Voice left on Flat since Bright already does the brightening work. *Why:* Bright and Treble both live in the top end but do different jobs — Bright feeds more harmonic content into the cascade itself (subtle loudness change, more sizzle), where Treble and Presence shape the tone stack and post-cascade EQ after the fact.

4. **Triode engine for touch-sensitive rhythm.** Start from Triode Foundation, Bias Shift at 100% (the voicing's own calibrated depth), Quality on Standard while mixing and switch to HQ only for the final bounce. *Why:* the Triode stages model dynamic bias shift — an overdriven burst suppresses the following swing and recovers over roughly 20 ms, which is what makes palm mutes feel compressed and chugs "bloom" the way the Classic engine's memoryless cascade cannot reproduce.

5. **A/B-ing Classic vs. Triode without breaking playback.** Set Engine once per session rather than automating it — switching Engine or Quality changes Tenebrae's reported latency, so both are deliberately non-automatable, discrete configuration changes rather than performance controls. *Why:* `setLatencySamples()` can only be called from the message thread; a live-automatable latency change isn't something a host's plugin-delay-compensation model can track sample-accurately mid-stream.

> **Theory — why a gate needs to listen before the distortion, not after.** A noise gate works by comparing a detector's reading against a threshold — but *what* the detector hears determines whether that comparison means anything. Feed the detector the fully-distorted, post-cascade signal (Tenebrae's default, matching the v0.2.0 behaviour) and 24+ dB of gain has already compressed the gap between "silence" and "playing" down to a handful of dB — there may be no threshold that reliably separates the two. Gate Key = Pre solves this by tapping a copy of the guitar's *input* signal, before any of the cascade's gain is applied, through its own band-pass filter tuned to the guitar's useful range. The detector then sees the same dynamic range your hands actually produced, undistorted by what 30 dB of cascade gain does to it — which is why Pre is the setting to reach for whenever a gate seems unable to stay open on quiet notes and closed between them at the same time.

## Pitfalls

- **Engine and Quality are stepped, not automatable.** Switching either mid-stream is a bounded, finite 2 ms crossfade with a full chain reset — not a click-free performance move. Set them once per session.
- **Gate defaults to on**, unlike every other new control in this plugin. Loading an old (pre-v0.2.0) session engages the Gate at its default settings on top of whatever was already dialled in — check the tail/silence behaviour after loading an older session.
- **No cabinet simulation, by design and permanently.** Tenebrae is the gain stage, not the speaker — pair it with a cab sim/IR loader (Nave or otherwise); running it dry into a DAW's monitor bus will sound harsh.
- **ADAA and the Quality control apply to the Triode engine only** — Classic always runs its original fixed 8x oversampling with no anti-aliasing changes, which is what keeps it bit-identical to v0.2.0.
- **The Triode engine is a calibrated approximation, not a per-sample circuit solve** — it tracks a reference solve closely at musical drive levels and is expected to diverge more on hard transients, where its lookup table's precision is coarsest.
- **CPU cost between Eco/Standard/HQ is relative, not an absolute published figure** — treat Standard as the mix setting and HQ as a mixdown/bounce setting, not a number to budget CPU against precisely.
- **The GUI is still the pre-M3 functional layout**, wrapped onto a second row for the newer controls — the custom look-and-feel and accessibility pass are a later milestone.
