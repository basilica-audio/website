# Seraph — how-to guide

*Practical settings for the choir & vocal processor, grounded in the factory presets.*

## Where it belongs

Seraph runs on vocal/choir tracks or a vocal bus as a full channel strip (De-Ess → Air → Comp → Doubler → Output), typically:

```
Vocal/choir recording → (tuning/editing, if used) → Seraph → reverb/delay send → mix bus
```

In its default configuration Seraph reports **0 samples of latency**, so it's safe to insert anywhere in a vocal chain, including in parallel — only Shift doubler mode and De-Ess Lookahead change that, deliberately and non-automatably.

## Quick-start settings

### Lead vocal, cutting through a dense mix — *Lead - Cut Through*

De-Ess 35%/7500 Hz, **Air +5 dB**, Comp 25%, Double 15%/Detune 8¢/Width 60%.

A touch of Air above the vocal's natural top end plus a subtle (15%) Double is the combination for a lead that needs to cut through distorted guitars and orchestral strings without sounding artificially doubled or over-processed.

### Intimate, close-mic'd lead — *Lead - Intimate/Close-Mic*

De-Ess 45%/6500 Hz/Width 55% (heavier — close-mic'ing brings up more sibilance), **Air +1 dB** (restrained), Comp 15%, Double 8% (barely there).

Heavier de-essing paired with minimal Air and Double keeps a close-mic'd take intimate rather than pushing it toward a "produced" lead vocal sound — the opposite balance from Cut Through's brighter, more processed approach.

### Choir/backing spread — *Choir - Sacred Shift*, *Choir - Wide Spread*

Choir - Sacred Shift: Double **60%**, Detune 14¢, Width 100%, **Double Mode Shift**, Humanize 35%.
Choir - Wide Spread: Double 55%, Detune 18¢, Width 100%, Double Mode Classic.

Sacred Shift reaches for the Shift engine (spectral pitch shifting, ~30 ms latency, the cleanest doubling) combined with heavy Humanize for a wide, decorrelated choir spread from fewer recorded takes — the settings a lead vocal would rarely want, but exactly what a smaller choir section benefits from.

### Vintage micro-detune doubler — *Doubler - Vintage Micro*

**Double Mode Micro**, Double 70%, Detune 12¢, Width 100%, Comp 0%.

Micro holds a genuinely constant interval (accurate to well under a cent) rather than Classic's slow wobble — reach for it specifically when a double needs to hold an interval rather than chorus, and note it sits further back in time than Classic (34–49 ms vs. 9–24 ms) as a deliberate character difference, not a fault.

### Spoken/growled interlude — *Spoken/Growled Interlude*

**De-Ess 5%** (minimal — little sibilance energy in a growled performance), Air +4 dB, **Comp 55%** (heavier — keeps a spoken passage level-consistent), Double 5%/Width 20% (narrow, centered).

Growled or spoken material typically needs the opposite de-essing treatment from a sung lead, and a stronger Comp setting to stay present and consistent against a quiet orchestral backing.

### Surgical de-ess only / glue only — *De-Ess Only (Surgical)*, *Glue Only*

De-Ess Only: De-Ess 50%, everything else at 0/bypass.
Glue Only: Comp 50%, everything else at 0/bypass.

Both isolate one section of the channel strip entirely — legitimate, supported configurations for when only one stage of Seraph's processing is needed on a given track.

## Recipes

1. **Choosing a doubler engine by what the material needs, not by habit.** Reach for **Classic** (the default, no latency) for the familiar wobble-based double; **Micro** when a stack needs to hold a genuine interval without reading as chorus; **Shift** (30 ms latency) when Detune is pushed toward the top of its range and you want the cleanest, most accurate result. *Why:* all three share the same four voices and pan/detune/width laws — switching changes only how detune is produced, so the choice is purely about which detune mechanism suits the material, not about losing or gaining other controls.

2. **Fixing a de-esser that's reacting to the wrong sound.** Try **De-Ess Width** before moving **De-Ess Freq** — narrow Width first if it's catching "sh"/breathy content, widen it if it's missing part of the actual "s". *Why:* Width controls the detection bandwidth directly, so it's a more surgical first move than relocating the center frequency, which can drift onto genuinely different content entirely.

3. **Preventing an ess from shoving a stereo image sideways.** Enable **De-Ess Link** (and **Comp Link**) on any stereo vocal bus — a doubled or spread choir, a stereo room take. *Why:* unlinked, each channel is processed by its own detector, so a loud moment or a strong ess on one side alone can pull just that side down and shift the image; both link options force a shared detector across channels specifically to prevent that.

4. **Removing the machine quality from a doubled stack.** Raise **Humanize** to 20–40% rather than adding more Double or more Detune. *Why:* four voices at an exact, fixed detune are still four mathematically related copies of one performance — Humanize adds independent, deterministic drift (timing, pitch, level) to each voice, which is what real singers do without agreeing, and is usually the actual difference between a doubler you notice and one you don't.

5. **Adding openness without re-feeding the sibilance you just removed.** Set **Air Freq to 15 kHz** when de-essing is set heavier. *Why:* 15 kHz stays entirely out of the sibilance region the de-esser targets, so boosting Air there adds top-end shimmer without also lifting back the "s" energy the de-esser just reduced — 10/12 kHz reach further down into the presence/sibilance range and pair better with lighter de-essing.

> **Theory — why de-esser lookahead has to delay the detected band, not just the audio.** A de-esser reduces sibilance by adding a scaled, inverted copy of the detected sibilant band back onto the signal — that only works as cancellation if the two copies are precisely time-aligned. The tempting simpler implementation delays only the audio path and runs the detector on the *undelayed* input, which seems harmless until you account for what sibilance actually is: effectively noise-like, decorrelated content. At even a 2 ms misalignment between the delayed audio and an undelayed detection signal, subtracting two decorrelated noise-like signals doesn't cancel — it adds roughly 0.8x the band's power back in at maximum reduction, so a "de-esser" configured this way would measurably boost esses instead of reducing them at higher lookahead settings. Seraph avoids this by delaying both the audio and the detected band together, running detection on the undelayed copy, and passing the resulting gain through a sliding-minimum window so the correction is already in place before the delayed ess arrives — precise time-alignment is not a nice-to-have here, it's the entire mechanism that makes lookahead de-essing work at all instead of misbehaving.

## Pitfalls

- **Double Mode and De-Ess Lookahead are not automatable, by design.** Both change Seraph's reported latency, and hosts cope badly with a latency change arriving mid-automation — switch modes with audio running if you like (a short fade masks it), but don't try to draw either into an automation lane.
- **Micro's voices sit 34–49 ms behind the dry signal**, further back than Classic's 9–24 ms, because the pitch shift is produced by continuously sliding the delay — a deliberate character difference (slappier, wider-reading) rather than a bug. If you need the doubled voices tight against the dry signal, use Classic instead.
- **Formant Preserve only does anything in Shift mode.** Classic and Micro never resample the spectrum, so there's nothing for formant preservation to correct in those modes.
- **De-Ess's detection threshold is fixed and absolute, not level-relative.** A very quiet take may need its gain staged up before De-Ess reacts meaningfully — this isn't an adaptive/auto-threshold detector.
- **Comp is a glue control, not a leveling tool.** Its gentle 3:1 maximum ratio is meant to add consistency on an already-reasonably-level take; fix wildly inconsistent verse/chorus levels with clip gain or a dedicated leveling compressor upstream first.
- **Watch Double Width on mono-sensitive material.** If the mix may fold to mono (streaming, some broadcast chains), check the doubler with Width pulled back toward 0% to confirm the doubled voices don't cancel unpleasantly when summed.
- **The GUI is a functional slider/knob editor; a custom vector-drawn GUI is a later milestone**, and Detune is capped at ±50 cents in every mode by design — larger intervals need per-voice control and a harmonizer's interface, a separate feature rather than a bigger number on this knob.
- **If a host ever feeds Seraph non-finite audio (NaN/Inf) from an upstream plugin misbehaving**, a transport stop/start or reopening the plugin (which triggers a host reset) is the reliable way to clear it — Shift mode's vendored engine specifically does not recover from its own internal reset alone.
