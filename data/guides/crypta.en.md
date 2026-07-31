# Crypta — how-to guide

*Practical settings for the 3-band bass voicing stage, grounded in the factory presets.*

## Where it belongs

Crypta is the bass-specific voicing stage: **DI/amp sim → Crypta → bus compression/glue → mix bus**. It expects an already reasonably clean, DI'd or amp-sim'd bass signal — it isn't a full amp sim itself. Its three bands each do a genuinely different job: the low band keeps the fundamental/sub content locked in place under a wall of distorted guitars via parallel compression; the mid band adds a distinct "throatier" saturation character in the range most likely to clash with guitars; the high band's voicing adds the upper-mid/high grind that lets bass cut through a dense mix.

Typical use cases: modern circuit-modelled grind, classic/vintage voicing, cab-colored tone via the built-in IR loader (Mid+High path only — the low band always bypasses it), and definition-focused settings for a bass that needs to be heard without dominating.

## Quick-start settings

### Modern circuit-modelled foundation — *Circuit Foundation*, *Circuit Grind*

Circuit Foundation: Drive Engine **Circuit**, Low Comp Detector **Smooth RMS**, Gate Mode **Modern**, Split Low 110 Hz, Split High 700 Hz, Low Comp Threshold −20 dB/Ratio 3:1/Mix 70%, Mid Drive 25%, High Voicing Razor, High Bias 15%.

Circuit Grind: same engine choices, tighter Split Low (130 Hz)/higher Split High (550 Hz — narrower Mid band), Low Comp Mix 85%, Mid Drive 55%, High Voicing Wool, High Drive 75%, High Bias 45%.

The Circuit engine rebuilds the Mid/High drive from circuit models rather than one curve per voicing — 25–30 dB better aliasing rejection than Classic, and per-voicing pre/post-emphasis networks that give each voicing (Gnaw/Wool/Razor) a genuinely different character rather than three settings of the same shape. Smooth RMS detection on the low band specifically fixes tremolo on sustained low notes that the Classic Peak detector can produce.

### Classic/vintage voicing — *Cab-Colored Grind*, *Clean Low, Loud Top*

Cab-Colored Grind: Drive Engine Classic, Split Low 120 Hz, Split High 600 Hz, Mid Drive 35%, High Voicing **Wool**, High Drive 60%, **IR loader on, IR Mix 70%**.

Classic keeps the pre-v0.3.0 Mid/High band exactly — if you preferred the old sound, or want session compatibility, this is the exact code path, not an approximation.

### Cut-through definition — *Cut Through*, *Definition Only*

Cut Through: Split Low 180 Hz, Split High 900 Hz (wide Mid band), Mid Drive 40%, High Voicing Razor, High Drive 55%.
Definition Only: Mid Drive 20% (light touch), High Voicing Razor, High Tight 250 Hz (tight), **EQ on, Peak 2 at 2800 Hz +3 dB** (presence/definition anchor).

Definition Only leans on the post-sum EQ's Peak 2 band rather than pushing drive — a moderate high-mid boost at the "presence/definition" anchor frequency does more for cutting through a mix than more distortion would, especially on a bass part that needs to stay audible without dominating.

### Sub-locked low end — *Sub Lock*

Split Low 90 Hz (pushes more fundamental into the low band), Split High 500 Hz, Low Comp Ratio 3:1/Attack 3 ms/Release 6 ms (fast, glue-style), Mid Drive 15% (light), High Voicing Razor, High Drive 35%.

Fast attack/release on the low-band compressor is the fast, gentle "glue" ballistics the reference class's own sourced values use — not a heavy "New York style" squash. Combined with a low Split Low, this locks the fundamental in place while keeping the mid/high content comparatively restrained.

### Full fuzz wall — *Fuzz Wall*

High Voicing Wool, High Drive 85%, **High Blend 100%**, Mid Drive 25%.

Blend at 100% means the high band is fully distorted with no clean signal mixed back in — the most aggressive setting available for that band, distinct from just raising Drive further.

## Recipes

1. **Locking the fundamental under a guitar wall.** Sub Lock as a base, Low Comp Mix at 100% if the fundamental still feels loose, Low Comp Auto Makeup on (Smooth RMS engine) so changing Threshold doesn't also change overall level. *Why:* the low band is compressed in parallel — the compressed signal blends back with its own uncompressed self via Mix rather than replacing it — which is what keeps the low end feeling tight without ever sounding squashed or lifeless.

2. **Choosing where the "throat" sits relative to the guitars.** Push Split High up to widen the Mid band's passband if the throat character needs more room before the High band's grind takes over; push it down to hand more content to the High band sooner. *Why:* Split Low and Split High are tone decisions, not just technical crossover points — where you draw the lines directly decides how much body ends up in the compressed-only low band versus the mid band's saturation character versus the high band's grind.

3. **Fuzz vs. tightness on the High band, independent of voicing.** Use **High Tight** as the primary control before reaching for Drive or a different Voicing — pull it toward its 20 Hz floor for maximum fuzz, push it toward 500 Hz for a tighter, more controlled top end. *Why:* High Tight is a pre-drive high-pass applied ahead of every voicing, so it changes how much low content reaches the nonlinearity regardless of which of the three voicings (Gnaw/Wool/Razor) is selected — it's the one control that reshapes all three consistently.

4. **Backing off intensity without flattening the character.** If a High voicing feels too extreme, lower **Blend** before lowering Drive. *Why:* Blend controls how much of the distorted signal is mixed back with the clean high band — lowering it keeps the nonlinearity's actual harmonic character intact at a lower overall intensity, where lowering Drive instead changes the character of the distortion itself, not just how much of it you hear.

5. **Cab-colored tone without a separate cab-sim plugin.** Cab-Colored Grind as a base, load an IR into the built-in loader, IR Mix to taste. *Why:* the IR loader processes only the Mid+High post-sum signal — the low band structurally never passes through it, matching the "low band bypasses the cabsim" architecture that keeps fundamental/sub content uncolored regardless of which cab IR you load.

> **Theory — why the low band is parallel-compressed instead of just compressed.** A bass fundamental under a wall of distorted guitars has two competing needs: it has to stay locked in place level-wise (no wandering, no pumping visible to the ear), and it has to keep its natural attack and weight so it doesn't read as squashed or lifeless. A single compressor in series can only trade one of those against the other — more control costs more life. Parallel compression sidesteps the trade: the low band's compressor runs on a copy of the signal, and that compressed copy is blended back *underneath* the uncompressed original via Mix, rather than replacing it. At partial Mix settings you get the control the compressed signal provides layered under the dynamics and transient character the dry signal already had — which is why Crypta's low band can lock the fundamental in place under a dense mix without the "breathing" or "dead" quality a heavily compressed single-path bass often has.

## Pitfalls

- **The Circuit engine's Wool voicing blooms rather than sags.** The original design predicted a loud passage would suppress ("sag") a following quiet probe; what actually ships is a decaying bloom instead — real, understood, faithful analog behaviour (asymmetric clipping generates real DC, which a downstream blocker then restores over its own time constant), but describe it as history-dependent/touch-sensitive, not as "sag."
- **The Classic and Circuit engines are not identical above 3 kHz at Drive 0** — parity holds to ±0.5 dB up to 3 kHz, but Circuit runs up to 2.5 dB brighter above that because its tone low-pass runs at the oversampled rate and escapes bilinear frequency warping. This is disclosed, not a bug to work around.
- **The safety clip trades its antialiasing advantage for its ceiling guarantee at extreme overdrive** — roughly 10 dB or more past the ceiling, transparency degrades in exchange for the hard bound holding. Leave it off during tracking/mixing; it's a safety net for unexpected automation or a hot input, not part of the intended tone-shaping path.
- **No in-plugin IR browser or bundled factory cabinet IRs ship yet** — the convolution engine itself is fully implemented and a guaranteed bit-exact passthrough with nothing loaded, but you'll need your own IR files.
- **Cross-platform bit-exactness isn't claimed.** macOS is the golden platform; Windows renders can drift up to −60 dB relative on material where the gate or low-band compressor's detector sits right at a threshold, since a tiny numeric difference there can shift a transition by a sample.
- **The Circuit voicing constants are engineering-derived starting points, not finalized by ear against reference material** — the suite's own open ear-tuning process still applies to them.
- **No CPU figure is published or claimed.** Collapsing two oversampling regions into one on the Circuit engine funds the extra per-voicing filtering, stated to land at roughly what the previous engine cost — but no percentage is measured or quoted.
- **The GUI is a functional generic editor with a plain meter readout row** — the photoreal GUI is a later milestone.
