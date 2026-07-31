# Triptych — how-to guide

*Practical settings for the 3-band multiband compressor, grounded in the factory presets.*

## Where it belongs

Triptych is a mastering/mix-bus dynamics tool, not a per-instrument effect. Reach for it when a single-band compressor either over-squashes the low end to control high-frequency peaks, or leaves the low end loose while the highs are already tamed — the classic symphonic-metal problem of guitars, orchestral hits, and choir all fighting for the same headroom. It also works as glue on a drum bus or a full guitar stack, independent of the full mix.

```
Full mix (guitars + orchestra + choir + drums/bass) → Triptych (multiband glue/control) → brickwall limiter → master out
```

## Quick-start settings

### Density/glue without over-squashing — *Density Glue*, *Glue Master*

Density Glue: Low Threshold −32 dB/Ratio 1.3:1, **Mid Ratio 0.7:1 (upward)**, High Ratio 1.4:1, all three bands **Range on at 8 dB**, Auto Release on, Character VCA, Stereo Link 80%.
Glue Master: all three bands Ratio ~1.5–1.6:1, Release 300 ms (long, uniform), Character VCA, Stereo Link 100%, High Limiter on at −1 dB, Lookahead engaged, Mix 90%.

Density Glue's Mid band runs *below* 1:1 — upward compression, lifting content above threshold instead of cutting it — capped by Range at 8 dB so the lift never runs away. Glue Master instead leans on long, uniform releases and full stereo link across all three bands for a cohesive, glued-together feel rather than per-band character differences.

### Peak control on transient-heavy material — *Peak Control*, *Hard Limiter Ceiling*

Peak Control: Low Threshold −10 dB/Ratio 5:1, Mid/High Threshold −8 dB/Ratio 4:1, **Knee 15%** (narrow — reacts close to threshold), Attack fast on all bands.
Hard Limiter Ceiling: High Ratio **8:1, Knee 0%** (hard knee), **High Limiter on**, Lookahead engaged.

Hard Limiter Ceiling's High band combines an aggressive compressor ratio with the brickwall limiter enabled — the compressor handles general level, the limiter (which becomes genuinely overshoot-proof once Lookahead is engaged) catches the sharp cymbal/harmonic peaks a musically-set compressor attack would otherwise let through.

### Low-end control under a guitar wall — *Low-End Tighten*

Low Threshold −20 dB/**Ratio 3.5:1**, Mid/High Ratio 1.2:1 (comparatively gentle), Attack 30 ms (slow — preserves low-frequency transient punch).

Only the Low band gets aggressive treatment here — Mid and High stay close to transparent, which is the setting for when specifically the low end (not the whole mix) needs reining in under a dense arrangement.

### Mastering safety net — *Mastering Safety Ceiling*

All three bands Ratio 1.3:1 (gentle, uniform), **Detector RMS**, Stereo Link 100%, High Limiter on at −3 dB, Lookahead engaged.

Gentle, uniform ratios across all three bands plus a brickwall ceiling on the High band is a "barely there until something needs catching" mastering-stage setting — RMS detection and full stereo link keep the image stable and the response smooth rather than transient-chasing.

### Parallel-style density — *Parallel-Style Density*

All three bands **Ratio 0.6:1 (upward)**, Range on at 10 dB, Output +1.5 dB.

All three bands running upward compression simultaneously, each range-limited to a sane maximum, adds density/lift across the board — a multiband alternative to blending in a heavily-compressed parallel bus, without needing a separate send.

## Recipes

1. **Finding the right crossover points before touching a single compressor.** Solo each band in turn (Mute/Solo section) to hear exactly what content lands where, adjust Low/Mid Split and Mid/High Split until nothing unexpected crosses (e.g. kick click or palm-mute pick attack leaking into the Low band). *Why:* a crossover point set wrong makes everything downstream unpredictable — the Low band compressing on content that should have been Mid's problem is a crossover issue, not a threshold issue, and no amount of compressor tweaking fixes it.

2. **Upward compression without a runaway boost.** Enable **Range** before pushing any band's Ratio below 1:1. *Why:* below 1:1 the same curve boosts instead of cuts, and that boost has no ceiling of its own — the further above Threshold the signal sits, the more it gets lifted. Range caps the maximum gain change (cut or boost) so an aggressive upward setting stays musically usable instead of discovering the ceiling by ear after it's already too late.

3. **Fixing a wandering stereo image.** Raise **Stereo Link** toward 60–100% on the band that's pulling the mix off-center. *Why:* at 0% (every earlier version's only behaviour) each channel's detector runs fully independently, so a hard-panned transient can pull just that side down and shift the image. Full link forces both channels to the same gain; partial link keeps some per-side responsiveness while pinning the image mostly in place.

4. **Reaching for Auto Release before a slower Release knob.** Enable **Auto Rel** instead of just dragging Release up when a band pumps on sustained material. *Why:* a fixed slow release stops pumping but also makes the band sluggish on transients. Auto Release runs a fast constant and a slow reservoir in parallel and takes whichever is higher — quick recovery from a short peak, a multi-second tail only when the band is genuinely working hard sustained.

5. **Setting per-band sidechain thresholds by ear, not guesswork.** Switch **SC Listen** to the band you're keying, set Threshold against what you actually hear, then switch SC Listen back off. *Why:* SC Listen plays the detector's key signal, not the band's processed audio — exactly the signal a threshold relates to, which is close to impossible to judge correctly by ear from the processed output alone.

> **Theory — why a VCA-character detector rounds the knee differently than a straight ratio curve.** Every earlier version of Triptych's compressor was purely feed-forward: the detector reads the input, and the gain computer applies a fixed Ratio/Knee curve with no memory of its own state. The VCA Character option instead statically approximates what a real feedback-topology compressor does — the kind where the detector reads the *output* of the gain cell, one step behind, which is what a hardware bus compressor's internal loop actually does. That feedback relationship rounds the knee by a ratio-dependent amount (more rounding at gentler ratios, less at aggressive ones) and makes the effective attack speed up as the ratio rises, purely as a consequence of the loop's own gain — not because either behavior was separately programmed in. There's deliberately no added distortion or harmonic stage in this option: the character difference lives entirely in envelope behavior, which is where a compressor's feel actually comes from before any saturation is added on top.

## Pitfalls

- **The three-band crossover tree is magnitude-flat but not phase-flat**, at any Slope setting. This only matters when blending Triptych's output against a dry copy of the same signal (including via **Mix**) or when measuring with a phase-aware analyzer — don't assume 50% Mix is literally "half the effect" on a minimum-phase multiband tree; use your ears.
- **Four controls are stepped, not continuous, and can click if changed mid-playback**: Slope (resets the crossover filters), M/S On, Limiter enable while Lookahead is engaged, and Lookahead itself (renegotiates host delay compensation). Every other control is fully click-free by design.
- **The VCA character's knee rounding becomes unreachable within about 3 dB of a 0 dB threshold** — the achieved width narrows smoothly toward a hard knee as threshold approaches 0 dB. Nothing misbehaves numerically, but for the full VCA rounding, keep threshold at −3 dB or below (where a multiband compressor's threshold normally sits anyway).
- **Mid/Side per band only affects the Side (width) component's own processing** — because L+R after decode depends only on Mid, no amount of Side processing can introduce mono-downmix phase cancellation. Only changing the Mid component's own settings changes the mono sum, which is the intended, audible effect of compressing the centre.
- **The spectrum-on-curve analyzer isn't in this release** — only the three per-band gain-reduction bars. A frequency-domain overlay is scoped for the later custom-GUI milestone.
- **The voicing throughout is research-derived from published manufacturer manuals and mastering-technique articles for this reference class, not measured against reference hardware.**
- **A gate range floor, per-band sidechain EQ, per-band dry/wet mix, and sample-accurate parameter interpolation (today's smoothing resolves on a 50 ms timer) are all deferred to a later release.**
