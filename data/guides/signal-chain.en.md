# Signal chain guide

*Where the thirteen Basilica Audio plugins sit in a heavy-music production — guitars, bass, buses, mastering, vocals & choir, and space.*

This guide is about **order and placement**, not full parameter references — each plugin has its own [how-to guide](#guides-for-individual-plugins) for that. Think of this page as the map you'd sketch on a whiteboard before opening a session: what goes before what, and why the order isn't arbitrary.

The suite assumes a heavy-music production with a mixed instrumentation: layered distorted guitars, a rhythm section, and orchestral/choir elements sharing the same mix. That combination is why several plugins exist in the first place — a single-band compressor or a generic stereo widener behaves very differently on a wall of guitars than on a string section, which is why Triptych is multiband and Firmament's widening is structurally mono-safe.

None of the settings below are gospel. They're starting points grounded in the plugins' own factory presets — read the "why" next to each move, not just the number, and expect to nudge everything against your own material.

## The chain at a glance

```
Guitars:   DI -> Silentium (gate) -> Overture (tight boost) -> Tenebrae (gain) -> Nave (cab IR) --+
Bass:      DI/amp sim -> Crypta (3-band voicing) -----------------------------------------------+
                                                                                                   |
                                                                          Guitar/bass buses -> Aureate / Triptych (glue)
                                                                                                   |
Vocals:    Mic -> Lancet (surgical) -> Miserere (parallel channel) -> Seraph (doubler/air) --+     |
Choir:                                                        Seraph (spread) -> Aureate --+ |     |
                                                                                            v v     v
Orchestra/choir bus -> Aureate (glue) -> Firmament (width, mono-safe) -> Requiem (space) -+
                                                                                            |
                                                                                     Mix bus -> Triptych (optional) -> Apotheosis (true-peak limiter) -> export
```

Treat this as a starting skeleton, not a rule. The sections below walk each branch and explain the placement logic.

## Guitars: Overture → Tenebrae → Nave

The core guitar chain is a **tightening boost, then the gain stage, then the cabinet** — the same three-stage logic a pedal-into-amp-into-mic rig uses, just as plugins:

1. **Overture** strips low end out of the signal *before* anything clips, so palm mutes and low-string chugs stay articulate instead of turning into mush once the next stage's own gain saturates them. Its own drive is deliberately modest by default — it's shaping what hits the next stage, not being the distortion itself.
2. **Tenebrae** is the main gain stage. It has no cabinet simulation by design, so it stays a clean building block: run Overture ahead of it for low-end control, then whichever cab/IR stage fits the rest of the chain after it.
3. **Nave** convolves the now-distorted, still-raw signal with a cabinet + microphone impulse response — the step that turns a buzzy amp-sim output into something that sounds like it was mic'd in a room. It normally sits *after* distortion and *before* EQ/bus processing.

```
Guitar DI -> Silentium (gate) -> Overture (tight boost) -> Tenebrae (high-gain) -> Nave (cab IR) -> EQ/bus
```

### Silentium: placement options, and why detector position matters

Silentium is a detection-and-dynamics stage, not a tone-shaping one, which is exactly why *where* you put it changes what it reacts to:

- **Before Overture/Tenebrae** (gating the clean DI) is the default choice for layered rhythm guitars — it avoids gating artifacts getting amplified and distorted along with everything else, and it lets the sidechain high-pass filter key off an undistorted signal rather than one already thickened by a following gain stage.
- **After the amp/cab stage** only if the noise you're actually fighting is introduced there (amp hiss, cab-sim noise floor) rather than present in the DI — gating post-distortion to fix a problem that already exists pre-distortion just chases the symptom in the wrong place.
- **Before any reverb/delay** in the chain, always, unless you deliberately want a gated reverb tail — otherwise the gate closes on the dry guitar and chops a decaying tail off mid-breath.
- **One instance per track**, not one on the guitar bus, in a wall-of-guitars mix. Every performance has its own pick-attack timing; per-track lookahead keeps every layer's attacks tight and simultaneous, where a single bus-level gate would smear them together.

> **Theory — why detector position and type change the result.** A gate doesn't listen to your whole mix; it listens to whatever the detector is fed, and that choice is half the design. Silentium's Peak detector (a fast ballistics follower, ~0.3 ms attack) reacts to single transient spikes — good for catching a fast pick attack, but it will also flip open on a single isolated click that a human wouldn't call "signal." Its RMS option runs a 5 ms one-pole average instead, which is structurally blind to isolated spikes: on a mixed program with occasional clicks over a quiet bed, Peak can trigger dozens of times a second where RMS doesn't open at all. Neither is "more correct" — Peak suits fast, percussive material where you want every attack caught; RMS suits sustained or noisy material where you want the gate to track the *body* of the signal, not its texture. The same logic applies to the sidechain filter's slope (12 vs 24 dB/oct): a steeper slope narrows what the detector "hears" more aggressively, which matters when you're keying off an external sidechain (a kick, a click track) rather than the guitar itself.

**Recipe — drop-tuned rhythm chug.** Silentium with a fast attack and 0 ms Smooth Open (the *Chug Lock* territory), high Ratio toward the gate end, RMS detection off (Peak, to catch the transient) into Overture's Tight control pushed up toward 200+ Hz (the *Drop-Tune Tight* preset territory — Tight 220 Hz, Drive around 4 dB, Bite 80%) ahead of Tenebrae. The high Tight setting strips low end before Tenebrae's own gain stage has a chance to saturate it into mud on a low-string chug.

## Bass: Crypta

Crypta is the bass-specific voicing stage, and its placement is narrow and deliberate: **DI/amp sim → Crypta → bus compression/glue → mix bus**. It expects an already reasonably clean, DI'd or amp-sim'd bass signal — it isn't itself a full amp sim.

The reason it's a three-band tool rather than a single full-range saturator: a wall of distorted guitars and a bass guitar are fighting for overlapping frequency territory, and a single-band treatment can't serve the low end and the "cut through the wall" upper-mid content at the same time without compromising one of them. Crypta's low band runs a parallel compressor whose job is keeping the fundamental/sub content locked in place *underneath* the guitar wall, while the mid and high bands each get their own distinct saturation character — the mid band's "throat" sits deliberately in the frequency range most likely to clash with guitars, so it wants a deliberate decision, not an afterthought default.

> **Theory — why split the drive by band at all.** A single full-range saturator adds harmonics across the whole spectrum at once: push it hard enough to get useful upper-mid "grind," and the low end saturates right along with it, which is usually the opposite of what a bass guitar needs under a dense guitar wall (a solid, undistorted low end *and* an upper register that cuts). Splitting the signal into bands first means each band's nonlinearity only ever acts on the harmonic content that band actually contains — the low band can stay clean and compressed while the high band gets pushed hard for grind, independently.

## Buses: Aureate and Triptych

Both are glue stages, but at different points and for different reasons.

**Aureate** runs *after* individual layers of an orchestral/choral stack (or a guitar double) have already been balanced — a string or brass bus, an orchestral/choir submix, or (sparingly) the full mix bus as a final "console glue" pass. It is not a distortion or amp-sim tool: Drive is capped modestly, and the default Warmth/Character settings stay inside "adds richness," not "adds grit." See Aureate's own guide for the theory behind why its glue behaves differently depending on which circuit law you pick.

**Triptych** is a mastering/mix-bus multiband dynamics tool, not a per-instrument effect. Reach for it when a single-band compressor either over-squashes the low end to control high-frequency peaks, or leaves the low end loose while the highs are already tamed — the classic symphonic-metal problem of a dense wall of guitars, orchestral hits and choir all fighting for the same headroom. It works equally well as glue on a drum bus or a full guitar stack, independent of the full mix.

A common pairing on a dense orchestral/guitar mix bus: **Aureate first** (gentle saturation glue, low Mix), **Triptych after** (multiband control where frequency ranges are genuinely fighting each other), before the signal reaches the master limiter.

## Vocals and choir: Miserere, Seraph, Lancet

These three cover different jobs and layer naturally, but two of them can step on each other if you're not deliberate about it.

**Lancet** is corrective and surgical — it belongs early-to-mid chain, before broad tonal shaping, fixing a specific resonance or harshness band without permanently coloring everything under it. Use it *before* the character-adding stages below, not after: fixing a problem after it's already been glued into a saturated bus is much harder to do cleanly.

**Miserere** is a parallel vocal channel: a dry "direct" path (every section off by default, so out of the box the vocal passes through essentially untouched) plus four parallel return busses (a FET-style limiter, a passive-EQ/opto-style leveler sandwich, a micro-pitch spread, and a short tape-style slap-back), each blended back in underneath the dry signal at a modest level. It functions as *the channel itself* for a lead vocal, not an insert you add on top of another channel strip doing the same job.

**Seraph** covers de-essing, an air shelf, gentle glue compression, and — its main differentiator from Miserere — a doubler with three distinct engines (constant-ratio micro-pitch, a phase-vocoder shift, and a classic doubled-voice mode), useful anywhere Miserere's parallel-return character isn't what you need, especially choir spread.

> **Watch for double-processing.** Both Miserere's Direct path and Seraph include a de-esser. Running both with de-essing engaged doubles the sibilance treatment for no benefit — pick one stage to own de-essing (usually whichever sits earlier in your chain) and leave the other's de-esser off.

**Suggested order for a lead vocal:** Lancet (fix the one resonant problem) → Miserere (the channel, parallel character on top) → Seraph, only if you need Air or a doubler pass Miserere doesn't offer → reverb/delay send (Requiem).

**Suggested order for a choir bus:** Lancet only if a specific recorded frequency needs taming across the whole choir → Seraph with heavier Doubler width and a wider spread setting for a fuller choir feel from fewer recorded takes → Aureate for section glue → Firmament/Requiem for width and space.

Miserere's engines are explicitly **research-derived, not measured against real hardware units** (its own manual says so directly) — useful, musically motivated circuit models, not claims of matching any specific physical unit's sound. Treat its presets as mechanically accurate starting points to dial in by ear, the same way you would any other plugin, rather than as a stand-in for a particular piece of gear.

## Space: Requiem and Firmament

**Requiem** is built for the "cinematic" layer — orchestra, choir, pads, ambience — kept separate from the "aggressive" layer (rhythm guitars, drums, bass) so each can be placed independently. A string/orchestra bus wants a moderate Mix with Pre-Delay preserving fast passage clarity; a choir bus typically wants more reverb and a longer decay to read as cathedral-scale. It is *not* generally recommended directly on distorted rhythm guitars or kick/snare — the hall/cathedral character reads as mud on fast, percussive, distorted sources; a short plate-style reverb (or none) usually serves those better.

**Firmament** sits toward the back of a channel or bus chain, after tone-shaping and dynamics have already been decided — width is a *feel* decision made once the tone is set, not a substitute for it. Typical placements: string/choir/pad busses (the primary use case), a gentle touch on a doubled rhythm-guitar bus to glue two panned doubles into one wider wall, and — used sparingly — the master bus, where Bass Mono keeps kick/bass/low-guitar energy centered while cymbals/strings/reverb tails above the crossover stay as wide as the mix already made them.

> **Theory — why velvet-noise decorrelation stays mono-compatible.** Widening a stereo image usually means processing the channels asymmetrically — delaying one side (a Haas effect), or running an allpass network on just one channel. Fold that down to mono and the two channels can partially cancel: some frequencies drop by double digits in dB. Firmament's velvet-noise modes avoid this structurally rather than by careful tuning: the plugin only ever synthesizes and scales the *Side* signal of a Mid/Side split, and never touches Mid. Since a mono downmix is mathematically `Mid + Mid` regardless of what Side contains, no setting of the width control can ever change what a mono listener hears — the guarantee holds by construction, not because the decorrelation coefficients happened to be tuned to behave.

Mono-compatibility isn't an academic concern for a heavy-music mix carrying orchestral elements: PA systems, broadcast, and a meaningful share of listeners on phone speakers all fold to mono at some point in the signal path, and a mix that loses its low end or its choir width in that fold-down sounds thin exactly where it needs to sound biggest.

## Master: Apotheosis

Apotheosis belongs at the very end of the master bus, after every other processor — EQ, bus compression, saturation, Triptych if you're using it — has already done its job. It is not meant for individual tracks; it's the final safety net and loudness stage before export.

> **Theory — why true peak is not the same number as sample peak.** A digital audio file only stores discrete samples, but the analog waveform a D/A converter (or a lossy codec's decoder) reconstructs from them can peak *between* samples, higher than any individual sample value shows. A limiter working purely in the sample domain can let a signal through that measures "safe" on an ordinary peak meter but clips after conversion to analog, or after transcoding to a lossy streaming format. Apotheosis's true-peak detection runs inside an oversampled domain (4x/8x/16x) specifically so it can see — and hold a ceiling against — that reconstructed peak, not just the samples as stored.

Practical mastering targets, as starting points: a **streaming-safe master** typically aims for an Integrated LUFS reading (the standardized, perceptually-weighted loudness measurement Apotheosis's metering implements directly) around −14 LUFS with true peak held at or below −1 dBTP, since most streaming platforms normalize down to a target loudness anyway — going louder than that mostly just costs you dynamic range without gaining audible loudness once the platform turns it back down. A **club or physical-release master** more commonly pushes toward −9 to −6 LUFS integrated with true peak still held safely under 0 dBTP (commonly −0.3 to −1 dBTP, leaving margin for codec conversion later). Neither number is a rule — genre, platform and your own ears decide — but they're a sane starting bracket rather than guessing blind. See Apotheosis's own guide for the specific style/oversampling settings behind each.

## Common mistakes across the chain

- **Gating after distortion by default**, without asking whether the noise you're fighting actually originates there. Gate the clean DI unless the noise source is specifically the amp/cab stage.
- **Running both Miserere's and Seraph's de-essers** on the same vocal — pick one.
- **Chasing loudness on the master with Apotheosis alone** instead of doing gain-staging and glue earlier in the chain — a limiter fixing what upstream balance should have handled tends to sound squashed rather than loud.
- **Confusing true peak with sample peak** when checking headroom — a track that "measures safe" on a basic peak meter can still clip after format conversion if true peak wasn't checked.
- **Widening before checking mono fold-down**, especially on orchestral/choir material sharing a mix with guitars that need to stay punchy through a PA. Firmament's Mono Audition mode exists specifically for this check.
- **Reverb on distorted rhythm guitars by default** — a cathedral-scale reverb reads as mud on fast, percussive, already-distorted material; reach for something shorter, or nothing, there.

## Guides for individual plugins

- [Overture](../overture/guide/index.html) — guitar tight boost
- [Tenebrae](../tenebrae/guide/index.html) — high-gain distortion
- [Nave](../nave/guide/index.html) — cabinet IR loader
- [Silentium](../silentium/guide/index.html) — lookahead noise gate
- [Crypta](../crypta/guide/index.html) — bass processor
- [Aureate](../aureate/guide/index.html) — orchestral saturation glue
- [Triptych](../triptych/guide/index.html) — 3-band multiband compressor
- [Apotheosis](../apotheosis/guide/index.html) — true-peak brickwall limiter
- [Miserere](../miserere/guide/index.html) — parallel vocal chain
- [Seraph](../seraph/guide/index.html) — choir & vocal processor
- [Lancet](../lancet/guide/index.html) — dynamic EQ
