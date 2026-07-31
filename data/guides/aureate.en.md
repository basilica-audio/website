# Aureate — how-to guide

*Practical settings for the orchestral saturation glue stage, grounded in the factory presets.*

## Where it belongs

Aureate runs **after** the individual layers of an orchestral/choral stack (or a doubled guitar) have already been balanced — a string or brass bus, an orchestral/choir submix, or, sparingly, the full mix bus as a subtle master-glue pass. It is not a distortion or amp-sim tool: Drive is capped at a modest 24 dB, and the default Warmth/Character settings stay inside "adds richness," not "adds grit" — that role belongs elsewhere in the suite (Overture/Tenebrae).

Typical use cases: gluing a divisi string/brass section into one instrument, cohering an orchestral/choir submix before it meets the metal instrumentation, subtle master-bus glue, and (v0.3.0) mix-bus-style dynamics via the Glue section.

## Quick-start settings

### Subtle master-bus glue — *Master Glue (Subtle)*

Character Tape, Drive 3 dB, Warmth 25%, **Mix 45%**, Output 0 dB.

Low Drive and a Mix well under 100% is the deliberate move for a master-bus pass — this is meant to be felt more than heard, the same role a summing bus plays in a hybrid analog/ITB workflow.

### Section glue — *String Section Glue*, *Console Summing Sheen*, *Choir Warmth*

String Section Glue: Character Tape, Drive 5 dB, Warmth 30%, Tone +5%, Mix 100%.
Console Summing Sheen: Character Console, Drive 4 dB, Warmth 20%, Tone +5%.
Choir Warmth: Character Tape, Drive 4 dB, Warmth 50%, **Tone −15%** (darkened).

Console is chosen deliberately for the "summing sheen" preset — it's the Character that stays transparent at low-to-moderate drive and only shows character once pushed harder, closer to a solid-state/transformer summing-bus archetype than Tape's more immediately audible glue.

### A genuinely different circuit class — *Valve Push*, *Brass Bloom*

Valve Push: **Character Valve**, Drive 14 dB, Warmth 60%, Bias 15%, Output −2 dB.
Brass Bloom: Character Console, Drive 8 dB, Warmth 40%, Bias 10%, Tone +10%.

Valve is the most asymmetric, even-harmonic-forward of the three Character options — a rounder, tube-like push, and the one with the highest Warmth-driven bias ceiling. Positive Bias pushes the asymmetry further still, independent of Warmth's own contribution.

### Glue-section bus compression — *Orchestral Bus Glue*, *Soft Tube Glue*, *Iron Bus Weight*

Orchestral Bus Glue: **Glue on, Glue Model VCA**, Threshold −6 dB, Ratio 4:1, Attack fast, Release fast, Makeup 2.5 dB, Character Console, Drive 4 dB.
Soft Tube Glue: **Glue Model Vari-Mu**, Threshold −10 dB, Character Valve, Tone −6%.
Iron Bus Weight: Glue on (VCA), **Iron 65%**, Character Console, Output −1 dB.

These three show the v0.3.0 Glue section in its most useful shapes: VCA for classic, predictable console-bus behaviour; Vari-Mu for a softer knee and an intrinsic, programme-dependent release; Iron pushed hard for low-end transformer weight rather than compression character.

### Parallel/New York saturation — *Parallel Grit (New York)*

Character Valve, Drive 20 dB, Warmth 80%, **Mix 50%**, Output −3 dB.

Because Mix is sample-accurately delay-compensated, a heavily driven, characterful wet signal blends back under the clean dry signal without phase smearing from the oversampling latency.

## Recipes

1. **Divisi string section into one instrument.** String Section Glue as a base, Tone nudged +3 to +8% if the section needs to read a little more present against guitars. *Why:* a little Drive and Warmth glues a section together the way tape/console summing naturally does — the goal is a section that reads as one instrument rather than a pile of close mics, not an audible saturation effect.

2. **Orchestral submix before it meets the metal instrumentation.** Console character (stays transparent until pushed), Drive 4–6 dB, Mix 100%, sitting after individual sections are already balanced and before the material reaches the full mix bus. *Why:* Console's "least characterful until pushed" behaviour means it can sit on a whole submix without audibly coloring quieter passages, only adding character where the material is actually loud enough to reach it.

3. **Choosing VCA vs. Vari-Mu for bus glue.** Reach for **VCA** (Orchestral Bus Glue) when you want classic, predictable console-bus behaviour and want the Attack switch to actually do something; reach for **Vari-Mu** (Soft Tube Glue) when you want a softer knee and a release that changes shape with the programme rather than a fixed time constant. *Why:* see the theory box below — the two aren't just different presets of one law, they're different detector/gain-cell topologies entirely.

4. **Iron for weight, not for compression.** Iron Bus Weight as a base, Iron between 40–70%, Drive kept moderate (6–8 dB) since Iron's own low-end saturation adds plenty on its own. *Why:* because transformer core flux is the integral of the applied signal, the core saturates far harder at low frequencies for the same level — third-harmonic content rises steeply toward the bottom end on its own, which is what reads as "weight" rather than "fizz," without needing to push Drive into audible distortion territory.

5. **Auditioning Drive without it becoming a loudness contest.** Enable **Auto Gain** while you dial in Character/Drive/Warmth, so what you're comparing is character, not level. *Why:* Auto Gain is a one-point calibration per Character (measured against equal-RMS pink noise), a deliberate listening aid rather than a mastering tool — turn it back off once you've settled on a Drive setting and gain-stage manually from there.

> **Theory — why a vari-mu-style law glues differently than a VCA.** Both of Aureate's Glue laws share the same feedback topology — a detector reading the signal *after* the gain cell, one sample old — which is what produces a soft knee and a program-dependent release on both, rather than a separately curve-fitted knee shape. Where they genuinely diverge is what sits inside that loop. The VCA law solves a straightforward dB-domain timing network: its attack time is a real, settable time constant, and doubling a transient's size roughly doubles how fast the gain reduction changes — an exponential, predictable response. The Vari-Mu law swaps in a current-limited rectifier and a three-capacitor release network modeling a tube-limiter-style gain cell, and that changes the physics: attack is no longer a dial-able number because it's intrinsic to how fast the rectifier can respond, a bigger overshoot takes proportionally *longer* to reach its own gain reduction (not less), and the four Release positions' hardware-class markings (0.1/0.3/0.6/1.2 s) don't match their measured recovery times (roughly 0.3/0.8/2/5 s) — because the reservoir capacitor's recovery genuinely depends on how long it was charged, which is exactly the "glue" behavior a fixed time constant can't produce.

## Pitfalls

- **The Vari-Mu law's Attack control does nothing** — its attack is intrinsic to the circuit's own current-limited rectifier, not a user-settable parameter. If Attack matters to your workflow, use the VCA law.
- **The Vari-Mu law's release switch markings don't equal its measured recovery times** (markings 0.1/0.3/0.6/1.2 s vs. measured ~0.3/0.8/2/5 s) — a documented, deliberate property of the circuit class being modelled, not a mislabeled control.
- **The VCA law's knee narrows sharply at higher ratios** — roughly 2.2 dB wide at 2:1, under 1 dB at 4:1 and 10:1. This is the feedback loop's own higher gain at higher ratios, not an inconsistency to fix.
- **No CPU benchmark is published.** HQ Quality evaluates one extra antiderivative per oversampled sample versus Classic — real cost, no quoted percentage.
- **The Glue section is envelope-only — it has no detector-nonlinearity/distortion character of its own.** If you want the *distortion* character of a bus compressor rather than just its dynamics, that's what the Character saturator and Iron stage further down the chain are for.
- **Voicing throughout is anchored to published circuit analysis and triode laws fitted to a documented control range, not to measurements of specific hardware units.** Every behavioral claim (a knee width, a slew ratio, a time-constant ratio) is a tested invariant, not a "sounds like" claim.
- **Iron's measured low-end rise is roughly 10 dB/octave in this implementation**, short of the 12 dB/octave an idealized flux-integration model predicts — a real, measured property of the finite core curve, not a bug.
- **The editor is still the v0.1 functional-slider layout** — a custom photoreal panel is a later, suite-wide milestone.
