# Nave — how-to guide

*Practical settings for the cabinet IR loader, grounded in the factory presets.*

## Where it belongs

Nave takes a dry, un-amped signal (a DI, or the pre-cab output of an amp sim) and convolves it with a cabinet-and-microphone impulse response — the step that turns a buzzy amp-sim output into something that sounds mic'd off a real cab in a room. It typically sits **after** distortion/amp-sim processing and **before** EQ/bus processing:

```
DI guitar/bass → amp sim/preamp distortion → Nave (cab IR) → EQ/compression → mix bus
```

Typical use cases: reamping a recorded DI after the fact, running live in a monitoring chain while tracking, blending two mic positions or two cabinets, and simulating mic distance without a separate plugin.

## Quick-start settings

### Tight modern stack — *Tight Stack*

LoCut 75 Hz (12 dB/oct), HiCut 9000 Hz, IR Blend 45%, Blend Mode Crossfade, IR Align Precise, IR B Trim −2.5 dB, IR B Delay 0.35 ms, IR Gain Match Loudness.

The small IR B Delay offset is the classic trick for thickening a doubled-mic cab sound rather than leaving both slots perfectly time-aligned. IR Gain Match set to Loudness means switching between two differently-voiced captures changes tone without also lurching in level — useful while you're still dialling in the blend ratio.

### Two mic positions, continuously blendable — *Mic Morph*

LoCut off (20 Hz), HiCut off (20000 Hz), IR Blend 35%, **Blend Mode Morph**, IR Align Precise.

Morph is the deliberate choice here, not Crossfade: it decomposes each IR into its frequency response and its arrival time, interpolates both independently, and rebuilds a single new impulse response — there's only ever one cabinet in the signal path, so dragging Blend sweeps continuously between the two captures the way physically moving a mic would, with no comb filtering at any point in the sweep.

### Live monitoring — *Live Stage*

LoCut 80 Hz, HiCut 8000 Hz, IR Blend 0%, IR Gain Match Energy, everything else at default.

A narrower band and a single IR (no blend) — a deliberately simple, predictable setting for a live monitoring chain where you want one clean tone rather than a blend to fine-tune.

### Pushed back in the room — *Pushed Back in the Room*

IR Blend 0%, **Distance 60%**, Level +1.5 dB, everything else default.

Distance reduces proximity-effect bass and darkens the top end as it increases — a musically useful tonal push, not a physically exact distance model (no timing change is applied unless Distance Air is also engaged). The +1.5 dB Level compensates for the loss pushing Distance up costs.

### Dark vintage voicing — *Dark Vintage*

LoCut 180 Hz, HiCut 4500 Hz, Distance 25%.

A narrow window plus a touch of Distance darkening gets to a boxier, more vintage-leaning tone quickly without reaching for a different IR file.

### Parallel blended cab tone — *Parallel Cab (Blended Dry)*

Distance 20%, **Mix 65%**, Level +1 dB.

Blends the cab-processed signal with some of the untouched dry input rather than running fully wet — useful for a hybrid reamped/DI tone.

## Recipes

1. **Thickened double-mic cab.** Load a close-mic IR into slot A and a second position (or a different cab) into slot B, IR Blend around 40–50%, IR B Delay nudged a fraction of a millisecond off zero. *Why:* a small, deliberate timing offset between the two branches is the classic trick for thickening a doubled cab sound — Precise alignment already corrects for *unwanted* misalignment (including automatically flipping an inverted capture), so this is you dialling one back in on purpose.

2. **Comb-free morph between two related mic positions.** Two captures of the *same* cabinet in slots A/B, Blend Mode Morph, then automate IR Blend as a performance move. *Why:* Morph shines specifically on related captures — magnitude and timing are interpolated independently, so sweeping Blend sounds like a mic physically moving rather than two cabinets crossfading and partially cancelling at the midpoint the way Crossfade mode would.

3. **Fixing a boomy or fizzy raw capture.** Start from LoCut/HiCut at their off defaults, and only bring them in if the IR genuinely needs it — try LoCut 12 dB/oct first, switch to 24 dB/oct if you need to remove mud without thinning the body just above it. *Why:* a well-captured cab IR often doesn't need much extra filtering at all; adding filters you don't need costs headroom and CPU for no audible benefit, and the steeper slope trades a sharper cutoff for less overlap with the frequencies just above it.

4. **A/B-ing two IRs fairly.** Load both, set IR Gain Match to **Loudness** before you start comparing. *Why:* raw-energy matching (the default) leaves a dark cabinet capture — most of its energy sitting where the ear is least sensitive — sounding quieter than a bright close-mic capture that measures the same energy. Loudness mode uses the same K-weighting a LUFS meter does, so switching IRs changes tone without also changing perceived level, which is what makes an A/B actually about tone.

5. **A parallel reamp blend.** Distance around 15–25% for a touch of "pushed back" character, Mix around 60–70% rather than fully wet. *Why:* none of Mix, Blend, or Distance are gain-compensated against each other by design — so you always know exactly what you're hearing — which means checking Level after dialling in a parallel blend is not optional if you want it to sit at the same perceived loudness as a fully-wet patch.

> **Theory — why Morph mode exists when Crossfade already blends two IRs.** A conventional blend sums the output of two convolvers running in parallel. Wherever the two captures' direct sounds arrive at even slightly different times — which real-world captures almost always do, from different mic distances or setups — that sum partially cancels a band of frequencies. This is comb filtering, and it's worst exactly at the 50% blend point, which is where "somewhere between these two mics" naturally lives. Morph avoids the problem structurally rather than by careful alignment: it separates each IR into what it sounds like (a minimum-phase magnitude spectrum) and when it arrives (a bulk delay, found by cross-correlation), interpolates those two properties independently, and rebuilds one single new impulse response from the result. Because only one cabinet response is ever actually in the signal path, there is nothing left for the sum to comb against — the trade-off is that Morph's own endpoints aren't quite identical to plain IR A/IR B (you hear the minimum-phase version of each), which is exactly why Crossfade remains the default for anyone who wants the two original captures untouched.

## Pitfalls

- **The three "reset" switches — IR Gain Match, either Min-Phase toggle, and IR Align — briefly restart the convolution engine when changed**, which can produce an audible discontinuity if you flip one while audio is playing. These are settings to dial in once, not to automate; everything else (Blend, Mix, IR B Trim/Polarity/Delay, Distance, the slope switches) is fully click-free and safe to automate.
- **Morph changes the endpoints, not just the middle.** At Blend 0% under Morph mode you hear the *minimum-phase version* of IR A, not IR A exactly — inherent to the technique, and why switching to Morph is a deliberate character change, never something a session acquires on its own.
- **Morph works best on related captures.** Two mic positions on the same cabinet morph beautifully; two unrelated cabinets morph through magnitude responses no real cabinet has — that can be a usable sound-design effect, but don't expect it to behave like a physical mic move in that case.
- **Distance is a tonal push, not a physical distance model** — no timing offset is applied unless Distance Air is separately engaged. If you need an exact frequency response, reach for LoCut/HiCut or a downstream EQ instead.
- **IRs longer than 10 seconds are stored by file path only, not embedded in the session.** A cabinet IR is never realistically that long, so this rarely matters, but a missing/moved file for an oversized IR will still revert that slot to the transparent default on reload.
- **No bundled IR library ships yet.** Curating and licensing real-world cabinet captures is a separate, openly tracked task — you'll need your own IR files.
- **Sessions saved before v0.3.0 open with IR Align set to Legacy**, not Precise, so they keep sounding exactly as they did. Switch to Precise manually if you want the improved alignment (and automatic polarity correction) on an older session.
