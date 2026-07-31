# Lancet — how-to guide

*Practical settings for the 6-band dynamic EQ, grounded in the factory presets.*

## Where it belongs

Lancet is a corrective, surgical tool, most useful early-to-mid signal chain, before broad tonal shaping and bus compression:

```
Source track → [gain staging/gate] → Lancet (resonance/harshness control) → broad EQ/saturation → compression → bus
```

Reach for it when a static EQ cut either under-treats a problem (leaving room for it to poke through on the loudest hits) or over-treats it (thinning the tone on quieter passages where the problem isn't present). It also works as a mix-bus or master-bus tool for controlling a specific recurring resonance or harshness band without permanently coloring everything under it.

## Quick-start settings

### Taming a chesty low-mid resonance — *Chest Resonance Tamer*

Band 1 (Low Shelf) at 220 Hz, Threshold −28 dB, **Range −5 dB**, Attack 20 ms, Release 180 ms.

Range negative is the classic resonance-taming move: gain cuts *as the signal gets louder* past Threshold, so the correction only engages when the resonance is actually audible — a quiet passage where the same frequency isn't a problem stays untouched, unlike a static EQ cut that would always be there.

### De-essing / harshness stack — *De-Ess Stack*

Band 5 at 6500 Hz, Q 2.0 (narrow), Threshold −24 dB, **Range −8 dB**, Attack 0.5 ms (fast), Release 60 ms, **Auto Release on**. Band 6 (High Shelf) at 9000 Hz, Range +1.5 dB, Attack 5 ms.

Two bands working together: Band 5 pulls sibilance down hard and fast, Band 6 adds back a small amount of air above the de-essed region — a common move to keep a heavily de-essed vocal from sounding dulled.

### Gentle glue on a bus — *Gentle Glue*

Band 2 at 250 Hz and Band 4 at 2500 Hz, both **Range −4 dB**, Attack 10 ms, Release 100 ms.

Two bands with matched, modest settings rather than one band pushed hard — a broad, gentle dynamic tightening across two problem-prone regions (box resonance and presence) instead of a single aggressive correction in one place.

### Analog-style warmth lift with saturation — *Analog Warmth Lift*

Band 2 at 250 Hz, Gain +2 dB (static lift) with **Range +3 dB** (upward — boosts further as level rises), **Saturation on**.

Saturation only engages while the band is actively boosting — Gain plus the dynamic contribution net positive — so a cutting or idle band stays unaffected even with Saturation enabled. Combined with positive Range, louder passages get progressively more low-mid lift and progressively more soft-drive character.

### Sidechain-keyed carving — *Sidechain Carve*

Band 3 at 400 Hz, **SC Source External, SC Mode Wide**, Range −6 dB, Threshold −26 dB.

External sidechain routes something else into your host's sidechain input to trigger this band's move instead of the signal itself; Wide mode means the detector responds to overall level across the whole spectrum rather than just the 400 Hz region, so the band ducks in response to the keyed source's general presence, not specifically its content near 400 Hz.

### Slow tonal riding on a master — *Slow Tonal Ride*

Band 2, Q 0.5 (broad), Threshold −35 dB, Range −5 dB, **Attack 350 ms, Release 800 ms** (both very slow).

The 500 ms Attack ceiling exists specifically for slow, musical tonal-balancing moves like this rather than transient catching — this is closer to an automated fader ride on one frequency region than a corrective dynamic EQ move.

### Transient snare crack — *Transient Snare Crack*

Band 3 at 3000 Hz, **Range +6 dB** (upward), Attack 0.1 ms (fastest available), Release 40 ms, Auto Release on.

Positive Range with a very fast attack is the upward "duck-in" expansion move — it brings out the crack/attack transient specifically on hard hits, rather than statically boosting 3 kHz on everything including ghost notes and bleed.

## Recipes

1. **Finding exactly what triggers a problem band before setting Threshold.** Enable **Listen** on the band in question, sweep Freq/Q until you clearly hear the resonance or harshness in isolation, *then* set Threshold just above where it sits when it isn't a problem. *Why:* this is far more reliable than guessing at a Threshold value against the full mix — Listen solos the band's own detector signal (the bandpass-filtered, pre-EQ audio actually driving the move), and the full signal chain keeps running underneath so switching Listen off never pops.

2. **Choosing between Split and Wide sidechain mode.** Use **Split** (the default) when a band should react only to content near its own frequency — the surgical, resonance-specific behaviour; use **Wide** when a band should breathe with overall program level instead of policing one specific resonance. *Why:* Split filters the detector input down to the band's own region before it ever reaches the detector; Wide skips that filter entirely, so the band's gain move is still confined to its own frequency, but what *triggers* that move is the whole spectrum's level.

3. **Letting a band relax faster on naturally-decaying material without losing a slower Release elsewhere.** Enable **Auto Release** rather than just shortening the manual Release value. *Why:* Auto Release shortens the *effective* release time automatically whenever the signal's own envelope is already falling on its own — never below the plugin's 5 ms floor, never past your manual Release setting — so sustained material still gets the slower, musical release you dialled in, while naturally-decaying content doesn't hold a correction into silence.

4. **A softer, more analog-feeling character at deeper dynamic moves.** Enable **Gain/Q** coupling on a band using significant Range. *Why:* Gain/Q widens (softens) the band's own filter Q proportionally to how far its *dynamic* gain currently sits toward Range — deeper moves get gentler, broader treatment automatically, while the static Gain component never affects Q at all, only the dynamic contribution does.

5. **Parallel dynamic EQ instead of full replacement.** Pull **Mix** down from 100% rather than reducing every band's Range individually. *Why:* Mix blends the fully-processed six-band chain against the untouched (but still Input-Trimmed) signal in parallel — a "New York"-style move where the correction adds to the original rather than fully replacing it, useful when you want the effect of the dynamic EQ without it being the only thing shaping that frequency region.

> **Theory — why there's no ratio control.** Most dynamic EQs and compressors expose a ratio: for every dB the signal crosses a threshold, some fraction of a dB of gain change follows. Lancet deliberately has none. Above the knee, gain moves 1:1 with how far the detector has overshot Threshold, until it reaches Range — which then acts as a hard ceiling on how far the dynamic move can go. Range is genuinely the "how far can this move" control, not a scaling factor on top of a separate ratio; the knee, whose width scales with Range itself, is what provides the ramp-in rather than a hard switch. This is a simpler model than a full compressor's ratio/knee/threshold triangle, and it's the reason a shallow Range setting reads as a gentle transition while a full-depth Range setting sounds like a much sharper corrective move — the knee width is directly tied to how far there is to travel.

## Pitfalls

- **Q is ignored in Shelf mode.** Band 1's Low Shelf and Band 6's High Shelf always use the standard flat shelf slope (Q 0.707), for both the audible filter and its matched detector bandpass — moving Q on those two bands' Shelf type has no effect.
- **Auto Release, Gain/Q, and Saturation have no dedicated editor controls yet.** All three are fully automatable and preset-controllable — set or automate them via your host's generic parameter view until the GUI pass ships. (SC Source and SC Mode, by contrast, do have editor controls, since a sidechain routing you can't select from the editor wouldn't be usable at all.)
- **Detection is stereo-linked with no unlink, and there's no per-band M/S or L/R placement** — every band's detector sees a combined signal from both channels.
- **The per-band voicing defaults are engineering judgment, not ear-tuned against reference material.** The *direction* of the voicing table (low frequencies slow and gentle, high frequencies fast and surgical) follows established mixing convention and is measured/frozen by the test suite, but the exact numbers — and the Saturation drive curve — haven't been validated against real vocal/guitar/mix material or calibrated against any other product.
- **No absolute aliasing floor is specified for the Saturation stage.**
- **Not yet in the plugin, tracked for later releases**: opt-in spectral resonance suppression, per-band M/S/L/R placement with stereo unlink, optional HF de-cramping, wider Range/Q/Release ranges, lookahead, per-band ratio, linear phase, more than six bands, and a spectrum-analyzer/EQ-curve display.
- **The GUI is a functional slider/toggle/combo editor** — a custom vector-drawn interface with per-band gain-reduction needles is a later milestone; the underlying measurement already exists and is verified, just not displayed yet.
