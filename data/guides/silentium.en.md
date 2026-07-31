# Silentium — how-to guide

*Practical settings for the lookahead noise gate/expander, grounded in the factory presets.*

## Where it belongs

Silentium is a detection-and-dynamics stage, not a tone-shaping one — where you place it changes what it reacts to. Common placements: **before** any drive/distortion plugin to gate the clean signal (avoids amplifying gating artifacts, and lets the sidechain filter key off an undistorted signal); **after** the amp/cab stage only if the noise is specifically introduced there; always **before** time-based effects (reverb/delay) so a decaying tail never gets chopped. In a wall-of-guitars mix, run one instance per track rather than one on the bus — per-track lookahead keeps every layer's attacks tight and simultaneous.

Typical use cases: rhythm-guitar noise control, ambient/sustained material that needs a gentler downward expander rather than a hard gate, ducking one part under another, and rhythmically-locked gating keyed from an external sidechain.

## Quick-start settings

### Tight rhythm gating — *Chug Lock*

Threshold −42 dB, Attack 0 ms, Hold 10 ms, Release 40 ms, Range −80 dB, Lookahead 5 ms, SC HPF 80 Hz, **Smooth Open on**.

Attack at 0 ms with Lookahead engaged gives a genuinely instantaneous jump to unity right on the threshold crossing — the most percussive setting available — and Smooth Open is what keeps that instant attack from clicking: it shapes the opening into a ramp that fits entirely inside the lookahead window, finishing exactly as the delayed transient leaves the delay line.

### Surgical, silent-between-notes — *Surgical Mute*

Threshold −45 dB, Attack 0.5 ms, Hold 15 ms, Release 60 ms, Range −80 dB, SC HPF 100 Hz.

Deliberately does **not** use Smooth Open — Smooth Open also softens the *closing* edge and holds the gate open slightly longer, which measurably reduces how much quieter this preset is between notes compared to Natural Decay. When the goal is silence between notes above all else, leave Smooth Open off.

### Ambient/sustained material — *Ambient Sustain*, *Natural Decay*

Ambient Sustain: Threshold −50 dB, Attack 5 ms, Hold 200 ms, Release 400 ms, **Range −24 dB** (not a hard mute), Knee 12 dB.
Natural Decay: Threshold −38 dB, Hold 30 ms, Release 150 ms, Range −16 dB, Knee 6 dB.

Both leave Range well short of full silence and widen Knee substantially — a soft-knee, shallow-floor setting reads as a natural decay tapering off rather than a switch flipping. This is the gate acting more like a gentle leveler than an on/off gate.

### Duck a part under a lead — *Duck Under Lead*

Threshold −20 dB, Attack 10 ms, Release 200 ms, Range −10 dB, **Duck on**.

Duck inverts the gain computer: instead of opening above Threshold, the signal attenuates toward Range above it. The whole detection path (SC HPF, Hysteresis, Hold, Knee, Lookahead) still applies — it's the same engine, aimed the other direction.

### Externally-keyed, rhythmically-locked gate — *Expander Glue*

Threshold −45 dB, Ratio 2.5:1, Range −18 dB, RMS detection, Hysteresis 3 dB, Linear release shape, Smooth Open on.

Not a hard gate at all — Ratio at 2.5:1 makes this a downward expander: every dB the signal falls below threshold gets 1.5 dB of attenuation, proportional rather than switched. This is the starting point when a gate sounds too obviously like a gate.

## Recipes

1. **Per-track gating in a layered rhythm mix.** One Silentium instance per DI/amp-sim track (not one on the bus), Chug Lock as a base, Attack 0 ms with Lookahead at 3–5 ms. *Why:* every performance has its own pick-attack timing; per-track lookahead keeps every layer's attack tight and simultaneous, where a single bus-level gate would smear the layers' individual timing together.

2. **Rhythmically-locked chug keyed from a click or kick.** Route the external sidechain input from a click track or kick drum, Expander Glue's settings as a base, Duck off (this is still a gate, just externally keyed). *Why:* keying detection from a different source than the main signal decouples the gate's rhythm from the guitarist's own pick dynamics entirely — useful for programmed or tightly quantized rhythm parts, or for making a doubled/quad-tracked part gate in lockstep rather than each layer making its own slightly different decision.

3. **Cleaning amp noise without anyone noticing a gate is there.** Expander Glue as a starting point, Ratio between 2:1 and 4:1, RMS detection, Release Shape Linear. *Why:* a downward expander at a moderate ratio makes a decaying note quieter in proportion to how far it's fallen, instead of switching fully off at a threshold — the mechanical difference between "you can hear where the gate is" and "the noise floor just quietly isn't there."

4. **Fixing chatter on a signal that hovers near Threshold.** Raise Hysteresis toward 6 dB, or widen Knee toward 6–12 dB if the hard on/off snap itself is the problem rather than chatter specifically. *Why:* Hysteresis separates the open and close thresholds so a signal dithering right at the boundary can't flip the gate back and forth; Knee instead blends the target gain smoothly across a band around Threshold, which is a different fix for a related but distinct symptom (switchy-sounding transitions vs. actual chatter).

5. **Dialling in SC HPF/SC LPF by ear, not by guessing.** Engage **Listen** first, sweep SC HPF and SC LPF until you hear only the transient content you want triggering the gate, then turn Listen back off and set Threshold. *Why:* Listen routes the sidechain-filtered detection signal directly to the output, bypassing the gain computer — it shows you exactly what the detector is reacting to, which is nearly impossible to infer correctly by ear from the gated output alone.

> **Theory — why a gate needs two different jobs done by two different filters.** Silentium's SC HPF and SC LPF only ever touch the detection path — never the audio you actually hear — because what should *trigger* a gate and what the gate should *pass through* are frequently different questions. A guitar DI's pick-attack transient lives mostly in a narrow upper-mid band; the same signal's low end carries hum, proximity effect, and rumble that can falsely hold a gate open on an otherwise silent passage. Narrowing the sidechain's band (SC HPF up, SC LPF down) onto just the transient content the gate should actually respond to — without touching a single sample of the wet signal — is why Silentium can gate confidently even on a noisy DI where the raw signal's overall level tells you almost nothing useful.

## Pitfalls

- **No published CPU figure exists for this plugin** — several detection paths run unconditionally in parallel (both detector types, both sidechain slopes) specifically so switching between them is a crossfade rather than a cold restart; treat any CPU number you see elsewhere as unverified.
- **Smooth Open trades closing precision for opening smoothness.** It holds the gate open for up to half the Lookahead time after the signal falls away — usually inaudible, but it's specifically why the tightest, most silence-focused presets (Surgical Mute) leave it off.
- **Changing Lookahead mid-playback crossfades over 10 ms and reports the new latency a moment later** (v0.4.0 behaviour) — before v0.4.0 the control did nothing until the host happened to re-prepare the plugin, so older documentation describing that limitation no longer applies.
- **The "program-dependent" Attack/Release behaviour is inspired by, not a reproduction of, hardware noise-gate release curves documented in the category** — treat it as this plugin's own tested mechanism, not a claim of matching any specific unit.
- **If nothing is routed into the external sidechain bus (or it's disabled), detection falls back to the main input automatically** — there's no separate "no sidechain" mode to configure, which also means an accidentally-enabled-but-empty sidechain bus behaves exactly like no sidechain at all.
- **The editor is a functional slider/knob layout, not a custom GUI yet** — a photoreal panel with per-bus metering is a later milestone.
- **Ratio's default (∞:1, displayed "Gate") takes the literal pre-v0.4.0 code path**, not a very-large-ratio approximation of the downward-expander law — so a session that never touches Ratio behaves identically to before v0.4.0, by construction.
