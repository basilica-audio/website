# Requiem — how-to guide

*Practical settings for the cinematic convolution reverb, grounded in the factory presets.*

## Where it belongs

Requiem is built for the "cinematic" layer — orchestra, choir, pads, ambience — kept separate from the "aggressive" layer (rhythm guitars, drums, bass) so each can be processed and placed independently:

```
EQ → compression → Requiem → limiter (if last stage on that bus)
```

Not generally recommended directly on distorted rhythm guitars or kick/snare — the hall/cathedral character reads as mud on fast, percussive, distorted sources; a short plate-style reverb (or none) usually serves those better. If you want ambience on guitars specifically, keep Mix low (10–20%) and Decay short.

## Quick-start settings

### Strings/orchestra bus — *Concert Hall*, *Tight Rhythmic Hall*

Concert Hall: Space Hall, Decay 2.2 s, Mix 30%, Early/Late Balance 80%, Size 50%.
Tight Rhythmic Hall: Decay 1.6 s (shorter), **Pre-Delay 90 ms** (long), Mix 25%, Early/Late Balance 60% (more early-reflection character audible).

Tight Rhythmic Hall's long Pre-Delay is the key move for fast passages — a gap before the tail arrives lets the ear hear the attack clearly (spiccato, tremolo strings, palm-muted layers underneath) before the wash fills in, which preserves clarity better than simply shortening Decay would.

### Choir bus — *Choir Bloom*, *Living Cathedral*

Choir Bloom: Space Cathedral, Decay 5.0 s, Damping 5500 Hz (dark), Mix 45%, Early/Late Balance 95%, Size 90%.
Living Cathedral: Decay 7.5 s, Engine **Hybrid Tail**, Tail Mod Depth 45%/Rate 70%, Damping 6000 Hz.

Choir consistently wants darker Damping, longer Decay, and higher Early/Late Balance than a strings bus — a darker tail keeps sibilance/breath noise from building up in the wash, and the near-100% Early/Late Balance favors a pure diffuse wash over discrete early-reflection character.

### Ambient pads / frozen textures — *Frozen Drone*, *Infinite Frozen Nave*

Frozen Drone: Decay 8.0 s, **Freeze on**, Width 140%, Modulation 20%.
Infinite Frozen Nave: **Engine Tail Bloom, Freeze on**, Bloom Amount 70%, Decay 8.0 s, Size 95%.

Infinite Frozen Nave's Freeze is genuinely unbounded — because it's built on the Tail Bloom engine (a feedback delay network under the hood), Freeze there fades the network's attenuation to unity rather than holding a finite convolution kernel, so the hold has no Decay-length ceiling at all. Frozen Drone uses Classic Convolution instead, where Freeze is still bounded by Decay (here pushed to 8 s to make the frozen kernel itself long).

### Dialogue/score under narration — *Dialogue-Ducked Score*

**Engine Hybrid Tail**, Decay 4.2 s, **Duck Amount 65%**, Duck Attack 8 ms/Release 400 ms, Low Cut 100 Hz/High Cut 11000 Hz.

Duck's sidechain is the dry input itself — what triggers the duck is the source material, not the tail — so the reverb pulls back automatically whenever the source is playing and blooms back up in the gaps, the standard trick for keeping a big reverb from burying dialogue or a lead line.

### Vintage/plate character — *Vintage Lush Plate*

Space Chamber, Decay 2.8 s, Pre-Delay 8 ms (short), Engine Hybrid Tail, **Tail Mod Mode Lush** (detunes deliberately), Tail Mod Depth 65%, Low Cut 150 Hz/High Cut 9000 Hz.

Tail Mod Mode Lush is the deliberately-detuning option — it modulates delay lengths themselves rather than just how the lines feed each other, the classic vintage-plate chorus character, used here on purpose rather than avoided.

### Subtle air on a bus — *Subtle Air*

Decay 1.2 s, Mix 12% (very low), Modulation 15%, Size 30%.

A small Modulation amount combined with a low Mix is the "barely there" setting — enough to soften the procedural generator's occasionally slightly static/metallic character without reading as an obvious effect.

## Recipes

1. **Fast, rhythmic material staying intelligible under a wash.** Raise Pre-Delay before reaching for a shorter Decay. *Why:* a gap before the tail's onset lets the ear register the attack clearly, preserving clarity while keeping the same overall sense of space — shortening Decay instead reduces the space itself, which isn't always the actual goal.

2. **A choir tail that's harsh or sibilant.** Lower Damping a few thousand Hz before reaching for an EQ on the reverb return. *Why:* Damping is the tail's terminal high-frequency corner, and as of v0.2.0 the tail darkens progressively as it decays rather than applying one static color — pulling it down addresses the tail's own brightness at the source rather than filtering after the fact.

3. **A space that feels the wrong size for its Decay.** Reach for **Size** before changing Decay or Space. *Why:* Size adjusts the apparent dimensions of the early-reflection layer independently of both Decay (tail length) and Space (reflection character) — it's the control for "how big does this Hall/Cathedral/Chamber actually feel" without touching how long the tail rings or switching to a different Space choice entirely.

4. **Mud building up in the low end of a dense mix.** Pull **Bass Decay** down toward 100% or below, rather than shortening Decay overall. *Why:* Bass Decay controls specifically how much longer the low end rings relative to mid/high — reducing it tightens just the low end while leaving the mid/high tail (which you may still want at its current length) untouched, where shortening Decay overall would shorten everything.

5. **Turning an existing part into a sustained pad.** Automate Freeze on, ride Mix up, and add a touch of Width and Modulation for movement while it holds. *Why:* Freeze holds the tail's current spectral content instead of letting it decay — useful under a transition or breakdown without needing a separate pad instrument — and a little Width/Modulation keeps a held texture from feeling completely static once it's sustaining.

> **Theory — why Freeze can be truly infinite in some engine modes but not others.** Classic Convolution reverb works by convolving the input against a fixed, finite impulse-response buffer — there's no feedback loop to hold audio indefinitely, only a kernel of a specific length. Freeze in that mode regenerates the tail with a flat envelope, so however long you hold it, the sustain is still bounded by the Decay setting (up to 10 seconds) — a snapshot held for a while, not a true infinite drone. Hybrid Tail and Tail Bloom are built differently: underneath the early reflections sits a sixteen-line feedback delay network, and engaging Freeze there fades each line's attenuation out to unity, turning it into a lossless loop that holds exactly what's already circulating inside it, indefinitely. This isn't a workaround for Classic Convolution's limits — it's a deliberate tradeoff. Research into feedback-loop "infinite reverb" designs documents that they can progressively dull over very long holds (repeated filtering in the feedback path keeps attenuating highs even at unity gain) and can develop audible periodicity as their internal order increases. Requiem's Classic mode structurally cannot develop either artifact because it has no feedback path to filter repeatedly in the first place — the tradeoff is a hard ceiling on how long "infinite" actually lasts.

## Pitfalls

- **Hybrid Tail's echo density builds up gradually at the handover, not instantly** — the FDN branch is excited by an impulse, so its own reflection density climbs over the first several hundred milliseconds after the splice rather than starting dense. This is a known, measured characteristic, not a tuning bug.
- **Hybrid Tail's spectral balance at the splice point matches within a few dB, not within one.** Tighter matching would mean rendering the whole network offline for every parameter change, which would break the fast, click-free re-solve that's the entire point of Hybrid mode — the small tilt right at the handover is the accepted cost.
- **Matrix modulation's sidebands are audible by design** — they're the movement the feature exists to produce. What's held to a tight bound is pitch stability (under one cent at full depth), not the sidebands themselves.
- **Very wide Width settings (150–200%) can cause phase/mono-compatibility issues** — check your mix in mono periodically if you push Width high, especially on a bus that might get folded to mono downstream (broadcast, some streaming platforms).
- **No published CPU figure exists.** Long Decay values do cost proportionally more CPU and memory, since Decay also sets the generated kernel's length, but no benchmark number is quoted anywhere in the project.
- **The v0.2.0 voicing is research-derived, not measured against hardware or a commercial plugin** — sourced from public manuals, developer interviews, trade-press reviews and room-acoustics literature, not from measuring any hardware unit or commercial plugin's actual output.
- **The procedural generator is a simplified model** (a filtered-noise-burst tail plus a discrete early-reflection train), not a physical simulation of a real room's modal behaviour or exact reflection geometry — built for a convincing cinematic wash, not acoustic measurement accuracy.
