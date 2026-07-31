# Overture — how-to guide

*Practical settings for the pre-amp tightening/boost stage, grounded in the factory presets.*

## Where it belongs

Overture is a pre-amp tightening/boost stage — the plugin equivalent of the small pedal a metal guitarist runs **in front of** a high-gain amp, not a distortion in its own right (though it can be pushed into being one). Its two jobs are separate and both matter: strip low end out of the signal *before* anything clips, so palm mutes and low-string chugs stay tight instead of turning into mush once the next stage's gain saturates them; and add a controlled, voiced drive character on top.

Typical use cases:

- **Tightening stage ahead of a real amp or amp-sim** (Overture → Tenebrae or any high-gain source) — the primary use case, and where most of the factory presets live.
- **A genuine distortion source in its own right**, pushed harder, for a boost-only rig running into a clean amp.
- **A parallel-blended tone**, mixed in under a clean DI rather than run 100% wet.

## Quick-start settings

### Tightening a drop-tuned rhythm part — *Drop-Tune Tight*

Tight 220 Hz, Drive 4 dB, Voicing Asymmetric, Bite 80%, Knee Soften 30%, Asymmetry 40%, Bite Tilt −10%, Mix 100%.

Tight is pushed well above the 100 Hz default because a drop-tuned low string carries useful fundamental further up than standard tuning — 220 Hz strips enough low end before the clipper that palm mutes stay articulate instead of farting out. Bite at 80% makes the clipper itself frequency-selective on top of that, so the small amount of low end that does reach it still clips less than the treble does.

### Classic "808-in-front-of-an-amp" push — *Classic Boost* / *Clean Push*

Tight 100 Hz, Drive 1–3 dB, Voicing Asymmetric, Bite 65%, Knee Soften 40%, Bite Tilt 0%.

This is the best-documented version of the technique: drive is kept near zero and the clipper barely engages — Level and the amp's own gain stage do the actual distorting. Start here before reaching for more Drive; it's the reference behaviour the plugin was voiced around.

### Own-distortion / fuzz-adjacent lead — *Own Distortion*, *Fuzz-Adjacent Lead*

Own Distortion: Tight 120 Hz, Drive 22 dB, Voicing Hard Clip, Bite 40%, Knee Soften 60%, Bite Tilt +10%.
Fuzz-Adjacent Lead: Tight 150 Hz, Drive 30 dB, Voicing Hard Clip, Bite 25%, Knee Soften 70%, Bite Tilt +25%, Level +3 dB.

Hard Clip has no soft knee of its own at any Drive level — Knee Soften is doing real work here, rounding what would otherwise be a straight clamp. Pushed this hard, Overture stops being a tightening stage and becomes the main distortion source, which is a legitimate, supported use, just a different character from the presets above.

### Programme-level circuit clipper — *Circuit Drive*

Tight 120 Hz, Drive 12 dB, Voicing Feedback, Bite Amount/Knee Soften inert, Asymmetry 25%, Bite Tilt −8%, **Level −9 dB**.

The Feedback voicing runs hot by construction (see the theory box below) — this preset's −9 dB Level trim is the vetted starting point, not an arbitrary choice. Start from here rather than from your current patch if you're auditioning this voicing for the first time.

### Parallel/blended rhythm tone — *Parallel Grit*

Same core settings as Classic Boost, but **Mix 35%** instead of 100%. Blends a small amount of tightened, driven signal under a clean DI for a hybrid tone rather than running Overture fully in the chain.

## Recipes

1. **Drop-tuned chug tightening.** Tight 180–220 Hz, Drive 4 dB, Voicing Asymmetric, Bite 80%, Gate on with Threshold around −45 to −50 dB and Release on Auto. *Why:* raising Tight this far strips low end before Tenebrae's own cascade has a chance to saturate it into mud on a low string; the built-in Gate (front of the wet chain, zero added latency) keeps hum and hiss from ever reaching the clipper in the first place.

2. **Lead boost with a distinct character from the rhythm tone.** Start from Fuzz-Adjacent Lead (Tight 150 Hz, Drive 30 dB, Hard Clip, Bite Tilt +25%), then back Drive off if it feels brittle rather than reaching for more Bite Tilt first. *Why:* positive Bite Tilt brightens above the ~3 kHz corner — useful for a lead to cut through a dense mix — but a clipper driven this hard is already generating plenty of top end on its own; taming Drive first keeps the brightness intentional rather than harsh.

3. **Own-distortion rig into a clean amp.** Own Distortion or Fuzz-Adjacent Lead as the starting point, Voicing on Hard Clip, Level pulled down to compensate for the extra gain. *Why:* Hard Clip is the brightest and most aggressive of the memoryless voicings — closer to a fuzz/comparator-style clip than the amp-pushing Asymmetric voicing — which is what makes it work as a standalone distortion rather than just a boost.

4. **Touch-sensitive circuit drive.** Circuit Drive preset as a base (Voicing Feedback, Level −9 dB), then ride Drive with your picking dynamics rather than a static setting. *Why:* the Feedback voicing solves an actual feedback loop sample-by-sample rather than evaluating a fixed curve, so its gain, knee and high-frequency rounding all move together with how hard you hit it — a fixed transfer curve can't reproduce that touch response at any oversampling factor.

5. **Parallel blend under a clean DI.** Parallel Grit as a starting point (Mix 35%), Tight and Drive as in Classic Boost. *Why:* a blended tone needs its own gating done elsewhere — Overture's built-in Gate only ever acts on the wet path, by design, so the dry signal you're blending in underneath stays fully audible between notes.

> **Theory — why a circuit-solved clipper behaves differently from a transfer curve.** Most clippers, including three of Overture's four voicings, evaluate a fixed input-to-output shape: feed in a sample, get out a shaped sample, with no memory of what came before. The Feedback voicing is built differently — it integrates the actual op-amp/diode/RC feedback loop equation once per sample, using the same numerical method (trapezoidal rule with Newton iteration) an engineer would use to solve a real circuit offline. The practical difference is memory: a small feedback capacitor puts a drive-dependent low-pass pole *inside* the nonlinearity itself, so the stage's gain, its knee, and its high-frequency rounding all shift together with where Drive sits and how hard the signal is hitting it. No memoryless waveshaper — no matter how finely you tune its curve — reproduces that, because the curve has no concept of "a moment ago."

## Pitfalls

- **The five v0.3.0 parameters (Gate, Gate Threshold, Gate Release, Knee Response, Clip Quality) have no dedicated on-screen knobs yet** — reach your host's generic parameter view (Logic's "Controls" view, Reaper's FX parameter list, Live's plugin parameter list) to automate them until the M3 GUI ships.
- **If you've automated the Voicing menu, re-check that automation lane after updating.** Presets and sessions store the voicing by index and load correctly, but a host automation lane stores a normalised 0–1 value — a lane that used to mean "Hard Clip" (2 of 2 choices) now means "Feedback" (3 of 3).
- **Switching Voicing is a discrete step, not a crossfade** — like a stompbox toggle, expect an audible jump at the instant you switch, never automate it smoothly expecting a blend.
- **Changing Oversampling isn't instant.** It takes effect the next time your host re-initializes the plugin (transport stop/start, a sample-rate change, reopening the project) — a deliberate real-time-safety choice, since reconfiguring the oversampler needs a memory allocation that can never happen on the audio thread.
- **The Feedback voicing is loud by construction** — its linear region ends around −40…−35 dBFS at Drive 0, so a normal −12 dBFS track drives it hard. Pull Level down before you audition it; don't assume it behaves like a clean boost at unity gain.
- **The Gate only ever affects the wet path.** Running Mix below 100% still lets the ungated dry signal through underneath — expected behaviour, but it means a parallel-blend patch needs its noise handled elsewhere.
- **The voicing throughout is research-derived from published circuit analyses and documented workflows, not measured against physical reference hardware.** Treat the parameter ranges and defaults as engineered starting points, not a claim of matching any specific physical unit.
