# Miserere — how-to guide

*Practical settings for the parallel vocal channel, grounded in the factory presets.*

## Where it belongs

Miserere packages a documented parallel-vocal-processing template — a dry Direct path plus four parallel return busses (CRUSH, SANDWICH, SPREAD, SLAP) — into a single channel strip:

```
Vocal/choir recording → Miserere → reverb/delay send → mix bus
```

The Direct path is a wire by default: every optional section on it (De-Ess Pre, FET Comp, Console EQ, Sat, De-Ess Post) is off out of the box, so the dry vocal passes through essentially untouched — its natural envelope and phrasing survive. Everything else layers *underneath* it via the four return busses, copies of the direct-path output processed hard and blended back at a modest level. Functions as the channel itself for a lead vocal, not an insert added on top of another channel strip already doing the same job.

## Quick-start settings

### Starter template — *Gentle Bus*

Crush Input 8, Ratio 4:1, Style Gentle (soft 2:1 voicing), Level −7 dB. SANDWICH Peak Reduction 40%, muted by default. SPREAD/SLAP at their standard −18/−15 dB, muted by default.

This is the plugin's own recommended starting point: bring CRUSH up first with Audition engaged (it's meant to sound "terrible" soloed and good blended in), then unmute SANDWICH/SPREAD/SLAP one at a time only as needed, checking each against the "you only notice it's gone when you mute it" test.

### Lead vocal, present and forward — *Crush Forward*, *Aggressive Rock Vocal*

Crush Forward: **Input 24, Ratio 3:1**, Level −4 dB (comparatively hot in the mix), everything else muted.
Aggressive Rock Vocal: Direct path engaged (De-Ess Pre/Post on, **FET Comp on** at Threshold −24 dB/Attack 3 ms, **Console EQ Drive 10, Sat Drive 8**), Crush Input 30, Level −6 dB, Spread Width 90%.

Aggressive Rock Vocal is the preset that actually engages the Direct path's optional sections — FET Comp for light insert compression, EQ Drive and Sat for transformer/tape-style harmonic content on the channel itself, in addition to CRUSH pushed hard underneath.

### Backing vocal / choir stack — *Whisper Thicken*, *Wide & Wet*

Whisper Thicken: Direct De-Ess Pre on, Crush Style Gentle at Level −14 dB (light), **Spread Detune 10/Width 90%, Level −14 dB**, Slap Level −13 dB — all four busses active but each restrained.
Wide & Wet: **Spread Width 100%**, Slap Stereo on (independent L/R delays instead of mono return), Slap Level −9 dB (comparatively present).

For a backing/choir stack, SPREAD's width and detune do more of the work than CRUSH — a wider, more present pitch-spread return fills out a smaller number of recorded takes into something that reads as a fuller stack, where a lead vocal usually wants CRUSH doing more of the work and SPREAD staying subliminal.

### Direct-path-only insert — *Direct Channel Only*

De-Ess Pre/FET Comp/EQ (HPF on, Low +2 dB, Mid −2 dB, High +2 dB, Drive 6) all engaged on the Direct path; **all four return busses muted**.

Useful when you want Miserere's channel-strip processing (de-ess, light compression, console EQ, saturation) without any of the parallel character busses — a legitimate, supported configuration, not a partial setup.

### Worn tape slap — *Worn Slap*, *Tape Slap 7.5*

Worn Slap: Slap Time 140 ms, Tone 80%, **Wobble 60%, Age 75%** — everything else muted.
Tape Slap 7.5: Slap Time 120 ms, Tone 35%, Wobble 25%, Age 15% (comparatively restrained).

Wobble and Age are both genuinely off (not just turned down) at 0% — reach for them deliberately when the goal is specifically "this passed through a physical tape delay," not as a default coloration on every SLAP use.

## Recipes

1. **Lead vocal in a dense mix.** Start from Gentle Bus, bring CRUSH's Input up with Audition engaged until you hear heavy, obviously-wrong compression in isolation, then trust the return fader and adjust by ear in context. *Why:* CRUSH has no threshold knob — Input drives the signal into a fixed per-ratio threshold — and the bus is deliberately meant to sound bad soloed; judging it in isolation (rather than via Audition against the full mix) is the wrong test entirely.

2. **Backing vocal stack from a small number of takes.** Whisper Thicken as a base, Spread Width toward 90–100%, Spread Detune around 8–10 cents. *Why:* SPREAD's two delay taps are hard-panned L/R with a small pitch offset — widening it pushes the ear toward reading multiple takes as a wider stack, without the discrete chorusing artifact a larger detune would introduce (6 cents is deliberately small so the effect reads as "pushed to the outside," not chorused).

3. **Deciding between CRUSH's All-Buttons and Gentle style.** Reach for **Gentle** (a fixed 2:1 voicing) on material that needs restraint or a quieter vocal that shouldn't feel aggressively squashed; reach for **All-Buttons** (the default) when you want the "snap" — a plateau-shaped curve with a deliberate give-back and a short attack lag that lets transients punch through before clamping. *Why:* these are genuinely different curves, not two intensities of the same one — All-Buttons' overshoot-then-settle behaviour is what gives CRUSH its characteristic forward push, where Gentle is closer to a conventional, predictable compressor.

4. **Using SANDWICH's Emphasis for a de-essing-adjacent effect.** Push **Emphasis** toward 100% if SANDWICH's leveler is reacting to the wrong content (breath, low-mid body) rather than presence/sibilance. *Why:* Emphasis makes the detector progressively more HF-selective — up to 10 dB less LF sensitivity — so at high settings the leveler reacts mostly to the top end, "like a multiband" compressor, rather than being driven by whatever's loudest across the whole spectrum.

5. **Backing off the whole parallel layer on quieter, more organic material.** Use **Parallel** (the macro trim, −24 to +6 dB) rather than pulling down all four return faders individually. *Why:* Parallel offsets all four busses together in one gesture — the "VCA ride back" move for a section that needs the parallel layer present on louder passages but pulled back on quieter ones, without re-balancing the busses' relative levels against each other every time.

> **Theory — what a photocell-modelled leveler actually changes.** SANDWICH's Opto Leveler has no ratio control, and that's not a missing feature — it's a direct consequence of what it models. A real optical leveler works by driving a light source with the audio signal and reading the resulting light level back through a photocell whose resistance changes with exposure; there is no fixed ratio anywhere in that chain, only a nonlinear relationship between how much light hits the cell and how fast/slow its resistance responds. That's why the leveler's release is naturally two-stage (a quick initial recovery, then a long tail) and why it has genuine memory — hold the cell down longer or harder and it lets go more slowly, because that's how the charge carriers in a real photocell actually behave, not because a "memory" parameter was added. What you hear is the modelled cell's own behaviour rather than a curve someone drew to sound similar.

## Pitfalls

- **The voicing throughout is research-derived, not measured against real hardware units.** Treat CRUSH, SANDWICH, SPREAD, and SLAP as musically-motivated circuit models with their own tested, consistent behaviour — not as claims of matching any specific physical device's sound.
- **SPREAD's pitch shifter can produce a mild comb on a sustained pure tone** (a synth, or a very steady held vowel) — the two delay taps crossfade at a fixed distance apart, and on real programme material this is inaudible, but a sustained held note is the one case where it can surface.
- **Audition is not Solo, and the distinction matters.** Audition isolates exactly the bus it names, excluding the direct path and every other bus — the whole point is that these busses should never be *judged* in isolation, only double-checked. Don't use it as a general soloing tool for unrelated auditioning.
- **Mute always wins over Audition** on the same bus — a bus that's both muted and auditioned stays silent, not audible.
- **The GUI is a functional slider/knob editor; a custom vector GUI with per-bus needle meters is a later milestone**, and the preset bar is a plain functional strip, not yet restyled.
- **Dynamics detection is unlinked (independent L/R) by default** on CRUSH and SANDWICH — enable **Link** if you need both channels tracking a shared detector instead.
- **Deliberately out of scope for this release**: a short plate reverb module, a "BV mode" preset, swappable compressor colours beyond the two CRUSH styles, external sidechain, and an output limiter.
