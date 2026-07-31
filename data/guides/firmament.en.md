# Firmament — how-to guide

*Practical settings for the stereo widener & imager, grounded in the factory presets.*

## Where it belongs

Firmament is a width/imaging tool, which places it toward the back end of a channel or bus chain, after tone-shaping and dynamics have already been decided:

```
Corrective/tonal EQ, compression, saturation → Firmament (decide width) → reverb/delay sends, final bus processing
```

Typical placements: string/choir/pad busses (the primary use case), a gentle touch on a doubled rhythm-guitar bus, and — used sparingly — the master bus, where Bass Mono keeps kick/bass/low-guitar energy centered while cymbals/strings/reverb tails above the crossover stay as wide as the mix already made them.

## Quick-start settings

### Choir/orchestral bus — *Choir Bloom*, *Open Strings*

Choir Bloom: **Width 170%**, Bass Mono Freq 130 Hz, Low Width 15% (a little width survives even below the crossover), **Auto Mono Safety on** (Floor −12 dB).
Open Strings: Width 140%, Bass Mono Freq 110 Hz, Auto Mono Safety on.

Choir Bloom's Low Width at 15% (rather than the default 0%) is a deliberate exception — most bass-mono use cases want the low band fully centered, but very wide pad/choir material can sometimes benefit from a little width surviving even below the crossover.

### Doubled rhythm guitar bus — *Doubled Rhythm Glue*, *Subtle Openness*

Doubled Rhythm Glue: Width 125%, Bass Mono Freq 150 Hz, Low Width 0% (fully centered below).
Subtle Openness: Width 115% (gentler), Bass Mono Freq 100 Hz.

A gentler touch (110–125%) glues two already-panned doubles into a single wider wall without the extreme "hyped" artifacts more aggressive widening can produce — Firmament never adds anything that wasn't already in the stereo image at these settings (aside from Haas Mode/Decorrelate).

### Master bus, sparingly — *Master Bus Bass Mono*

Width 100% (unchanged — width decisions were already made upstream), **Bass Mono Freq 90 Hz**, **Auto Mono Safety on with Multiband on**.

Auto Mono Safety Multiband reasons about the low and high bands independently rather than one global correlation reading — useful here specifically because the low end is already safely centered via Bass Mono, and an unrelated phase problem in the highs shouldn't needlessly dull the low end too (or vice versa).

### Mono-compatible near-mono widening — *Mono-Safe Air*, *Velvet Width*

Mono-Safe Air: **Decorrelate on** (Classic mode), Decorrelate Amount 35%.
Velvet Width: Width 120%, **Decorrelate on, Decorrelate Mode Velvet Dense/Sparse**, Amount 60%, **Width Comp on**, Auto Mono Safety on.

Velvet Width is the fully mono-sum-safe option — the Velvet decorrelation modes synthesize only the stereo-difference content, so the mono fold-down is bit-for-bit the input's own mono sum at any Amount, unlike Classic Decorrelate's small documented mono-fold-down ripple.

### Dramatic width effect — *Wide Pad, Full Precedence*, *Extreme Width*

Wide Pad, Full Precedence: **Haas Mode on**, Haas Time 22 ms (inside the "precedence effect" zone), Output −1 dB.
Extreme Width: **Width 200%** (maximum), Bass Mono Freq 120 Hz, Auto Mono Safety on with a firmer Floor (−15 dB), Output −3 dB.

Both are deliberately special-effect settings, not defaults to leave engaged throughout a mix — Haas Mode specifically is not mono-sum-safe (it produces comb filtering on fold-down), so reach for it when its stronger, more dramatic character matters more than translation.

### Three-band imaging — *Three Band Imager*

Low Width 40%, Width 110% (mid band), **High Split 2500 Hz, High Width 140%**, Bass Mono Mode Phase Matched, Auto Mono Safety Multiband on.

Three independently-controlled bands (below Bass Mono Freq, between the two crossovers, above High Split) — useful for keeping the mids' width exactly as-is while opening cymbal/air content separately above 2.5 kHz.

### Mastering-grade linear-phase bass mono — *Mastering Linear Phase Bass Mono*

Bass Mono Freq 120 Hz, **Bass Mono Mode Linear Phase** (2048 samples of reported latency at 48 kHz), Auto Mono Safety on with Safety Response Smooth.

Linear Phase is a mastering/render choice, not a live toggle — pick it before a render pass rather than switching mid-playback, since the mode change applies a brief mute while the host renegotiates delay compensation.

## Recipes

1. **Deciding whether you need Bass Mono at all.** Start with Width alone — most material only needs the single global control. Reach for Bass Mono Freq/Low Width specifically when you hear the low end losing focus or translating poorly in mono as you push Width up. *Why:* adding a crossover and a second width parameter is only worth the complexity once a single global Width setting is audibly compromising the low end — most busses don't need it.

2. **Checking mono compatibility before committing to a wide setting.** Enable **Mono Audition** rather than hunting for your DAW's own downmix button. *Why:* it's the exact fold-down `(L+R)/2` that Firmament's mono-compatibility guarantees are actually about, applied after everything else in the chain — a one-click version of the "always A/B in mono" habit.

3. **Choosing between Decorrelate and Haas Mode for near-mono material.** Prefer **Decorrelate** (and specifically the **Velvet modes**) whenever mono translation matters at all — reach for **Haas Mode** only when you want its stronger, more dramatic precedence-effect character and translation is a secondary concern (a transition effect, a layer that will never be folded to mono). *Why:* Classic Decorrelate's documented cost on mono fold-down is mild spectral ripple; the Velvet modes have zero cost by construction. Haas Mode's cost is deep, audible comb-filter notches — a fundamentally different risk level.

4. **Auditioning Width fairly without the "wider sounds better" bias.** Enable **Width Comp**. *Why:* without it, 200% Width is measurably hotter and 0% measurably quieter, purely from how much energy the Side channel is carrying — which biases any A/B toward whichever setting happens to be louder rather than which one actually sounds better. Width Comp applies equal-power makeup gain so loudness stays constant as you sweep it.

5. **A safety net for a bus you can't constantly monitor.** Enable **Auto Mono Safety**, and add **Multiband** if Bass Mono is also engaged and the low/high bands' phase behaviour is likely to differ. *Why:* Auto Mono Safety reins in Side automatically whenever the input trends heavily out-of-phase, independent of and on top of whatever Width/Low Width you've already dialled in — it never touches Mid, so it can't break the mono-fold-down guarantee, it only ever reins in how wide Side gets.

> **Theory — why velvet-noise decorrelation stays mono-compatible where other widening tricks don't.** Widening a stereo image by processing the channels asymmetrically — delaying one side (Haas Mode), or running an allpass network on just the Right channel (Classic Decorrelate) — works acoustically, but summing two channels that have been treated differently produces cancellation at specific frequencies when folded to mono: deep comb-filter notches for a delay, milder spectral ripple for an allpass network. Firmament's Velvet Dense/Sparse modes avoid this structurally instead of through careful tuning: the core Mid/Side codec only ever scales the Side (difference) channel — Width, Low Width, High Width and the Velvet decorrelators all operate exclusively on Side, and Mid is never touched by any of them. Because a mono downmix works out mathematically to `Mid + Mid` regardless of what Side contains, no processing applied only to Side — however aggressive — can ever change what a mono listener hears. The velvet-noise coefficients themselves (published, DAFx-18 optimized pairs) are specifically structured so that widening the Side content this way sounds like genuine decorrelation rather than an obvious effect, but the mono-safety guarantee doesn't depend on how well-tuned those coefficients are — it holds by construction, the same way it does for the plain Width control.

## Pitfalls

- **Haas Mode and Decorrelate are not mono-sum-safe, unlike Width/Low Width/Auto Mono Safety.** Summing two time-offset or differently-filtered channels produces mono-fold-down artifacts — deep comb notches for Haas Mode, milder spectral ripple for Classic Decorrelate (the Velvet modes are the exception, fully safe by construction). If guaranteed mono compatibility matters (broadcast delivery, an unpredictable club mono sub), leave both off and rely on Width/Low Width/Auto Mono Safety alone.
- **Haas Mode and Decorrelate are mutually exclusive.** If both are enabled, Decorrelate takes effect and Haas Mode's delay is bypassed entirely.
- **200% Width is a special-effect setting, not something to leave engaged on a whole mix or loud bus** — it reads as artificial/phasey quickly at that level; it's far more useful automated briefly (a chorus lift, a breakdown) than left on throughout.
- **Linear Phase Bass Mono reports real latency (2048 samples at 48 kHz)** and switching to/from it mid-playback applies a brief mute and may click in some hosts while they renegotiate delay compensation — pick the mode before a render pass rather than toggling live.
- **On a mono-input track/bus, Width/Low Width/Auto Mono Safety have nothing to act on** (there's no Side signal to scale) — the plugin passes the source through cleanly. Haas Mode/Decorrelate are the controls that still do something in that situation, since they operate after the (now-identical) L/R pair has been decoded.
- **Auto Mono Safety Multiband changes Auto Mono Safety's behaviour whenever both Auto Mono Safety and Bass Mono Freq are engaged together** — it's off by default specifically because it's a behavior change, not a strict improvement, for that combination.
- **The GUI is still the plain functional v0.1/v0.2-style editor** — every parameter is fully controllable from the plugin's own window or a host's generic editor, but the correlation/phase estimate driving Auto Mono Safety isn't yet displayed as a visible meter (the DSP value is fully computed and tested, just not shown).
- **All default values and ranges are research-derived** from public manuals, developer documentation, mastering-forum consensus, and acoustics literature — not measured against any commercial stereo-widener's actual audio output, and no proprietary algorithm from another vendor was inspected or approximated.
