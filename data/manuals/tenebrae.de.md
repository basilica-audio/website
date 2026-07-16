<!-- Generated from tenebrae/docs/manual.md on 2026-07-16 — do not hand-edit; re-run the manual sync described in website/README.md. -->

<p align="center"><img src="assets/icon.png" alt="Tenebrae icon" width="120"/></p>

# Tenebrae — Benutzerhandbuch

*Eine Liturgie der Schatten — kaskadierte High-Gain-Distortion für den schwersten Rhythmus-Sound.*

## Was es ist

Tenebrae ist eine High-Gain-Rhythmusgitarren-Distortion, aufgebaut um eine Kaskade aus drei oversampelten Waveshaper-Stufen, jede zunehmend straffer und dunkler als die vorherige, sodass der Sound in ein fokussiertes "Chug"-Band konvergiert, statt sich mit steigendem Gain zu einem immer fizzeligeren Durcheinander aufzuschichten. Es ist kein Boost/Overdrive (das ist der Job des Schwester-Plugins `overture`) und kein Cab-Sim — es ist die "Wall of Gain" selbst: die zentrale Distortion-Stufe, in die ein Boost-Pedal hineindrückt, und die Stufe, nach der ein Cab-Sim/IR-Loader sitzt.

## Wo es in einer Heavy-Production-Chain sitzt

Tenebrae ist die **Haupt-Gain-Stufe**. Eine typische Chain:

```
Guitar -> noise gate -> boost/tight-boost (optional) -> Tenebrae (high-gain distortion) -> cab sim / IR loader -> reverb/mix bus
```

Setze einen straffenden Boost (wie `overture`) davor, wenn du zusätzliche Low-End-Kontrolle vor der Kaskade willst, und einen Cab-Sim/IR-Loader danach — Tenebrae selbst hat bewusst keine Cabinet-Simulation, damit es ein sauberer Baustein bleibt, den du mit jedem beliebigen Cab-Sim kombinieren kannst, der zum Rest deiner Chain passt.

## Signalfluss

```
Input -> Tight (HPF, 20-300 Hz) -> Bright (switch) -> Gain (0-40 dB) -> [8x oversampled]
              Cascade stage 1 -> Cascade stage 2 -> Cascade stage 3   (Voicing: Tight/Loose)
                                                              |
   Output <-- Mix <-- Level <-- Treble <-- Mid <-- Bass <----+   (tilted by Tone Voice)
     ^
     |
delay-compensated dry path
```

Die drei Kaskadenstufen laufen innerhalb eines 8x oversampelten Blocks, damit die von allen drei Nichtlinearitäten erzeugten Harmonischen — nicht nur die der ersten — außerhalb des hörbaren Bands bleiben. Der von **Mix** genutzte Dry-Pfad wird automatisch gegen diese Oversampling-Latenz delay-kompensiert, und das Plugin meldet seine Gesamtlatenz an den Host, damit die Wiedergabe sample-genau mit jeder anderen Spur ausgerichtet bleibt. Die vollständige technische Aufschlüsselung, einschließlich der Voicing-Tabelle pro Kaskadenstufe und der Latenz-Kompensationsstrategie, findest du in [`docs/architecture.md`](architecture.md).

## Parameterreferenz

| Parameter | Range | Default | Unit | Was es tut |
|---|---|---|---|---|
| **Tight** | 20 – 300 | 90 | Hz | Hochpassfilter, platziert *vor* der Gain-Kaskade. Höher gedreht, entfernt es mehr Low End aus dem Signal, bevor es auf die Clipper-Stufen trifft, und hält Palm Mutes und Chugs auf den tiefen Saiten perkussiv, statt dass sie ausfransen, sobald die Kaskade sättigt. Niedriger drehen für ein volleres, boomigeres Low End (nützlich bei Drop-Tunings, die du "groß" statt straff wirken lassen willst); höher drehen für maximale Palm-Mute-Artikulation. |
| **Gain** | 0 – 40 | 24 | dB | Pre-Gain in die oversampelte 3-Stufen-Waveshaper-Kaskade — der zentrale "wie viel Distortion"-Regler. Jede Kaskadenstufe hat zusätzlich ihren eigenen fixen internen Drive obendrauf, sodass selbst Gain bei 0 dB noch einen echt gesättigten High-Gain-Sound erzeugt; dieser Regler dreht die Kaskade härter auf, statt Distortion ein- und auszuschalten. |
| **Voicing** | Tight / Loose | Tight | – | Schaltet die fixe Per-Stufen-Asymmetrie und Zwischenstufenfilterung der Kaskade zwischen zwei Voicings um. **Tight** (Default) ist die straffere, moderner ausgerichtete Kaskade, um die herum das Plugin ursprünglich voiced wurde. **Loose** ist eine weicher gedrivte, breitbandigere Alternative — weniger asymmetrisches Clipping und lockerere Zwischenstufenfilterung auf jeder Stufe, für einen eher vintage-orientierten, etwas luftigeren und boomigeren Charakter. Das ist ein diskreter Schalter (wie eine Amp-Kanalwahl), kein sanft automatisierbarer Regler — erwarte einen kleinen hörbaren Sprung im Moment des Umschaltens. |
| **Bright** | Off / On | Off | – | Aktiviert eine fixe High-Shelf-Preemphase, angewendet *vor* der Gain-Kaskade, modelliert nach dem "Bright Switch", den man auf vielen High-Gain-Amp-Kanälen findet (und, lose, nach der Presence-Spitze eines helleren Cabinets — Tenebrae hat keine eigene Cab-Simulation, das ist also der nächstliegende "cab-adjacente" Regler, den es bietet). Weil das angehobene Signal danach drei kaskadierte Clipping-Stufen durchläuft, ist sein Effekt auf die Gesamtlautheit bewusst subtil — Sättigung komprimiert die zusätzlichen Höhen wieder herunter — was sich ändert, sind Harmonic Content und Anschlags-Sizzle, die in die Kaskade einspeisen, nicht der reine Output-Pegel. |
| **Bass** | -15 – +15 | 0 | dB | Low-Shelf-Band des Tone Stacks nach der Kaskade, zentriert bei 150 Hz. Boosten für einen volleren, low-end-lastigeren Chug; absenken, um nach der Kaskade zusätzlich zu straffen (ergänzend zu dem, was Tight davor schon entfernt hat). |
| **Mid** | -15 – +15 | 0 | dB | Peaking-Band des Tone Stacks nach der Kaskade, zentriert bei 650 Hz mit moderat schmalem Q. Das ist der klassische "Scooped Mids"-Regler für den High-Gain-Rhythmus-Sound — absenken für den mid-gescoopten, mid-2000er-Metal-Chug-Sound; boosten (oder nahe 0 lassen), um genug Mid-Präsenz zu behalten, damit sich der Sound in einem dichten Mix durchsetzt. |
| **Treble** | -15 – +15 | 0 | dB | High-Shelf-Band des Tone Stacks nach der Kaskade, zentriert bei 3,5 kHz. Boosten für mehr Anschlag und Höhen-Sizzle; absenken, um übrig gebliebenes Fizz aus den Harmonischen der Kaskade zu zähmen — besonders nützlich, wenn nach Tenebrae kein Cab-Sim/IR-Loader läuft, der diesen Höhen-Rolloff für dich übernimmt. |
| **Tone Voice** | Flat / Scoop / Boost | Flat | – | Ein Ein-Schalter-Tilt, der zusätzlich zu den (weiterhin voll live bleibenden) Bass-/Mid-/Treble-Reglern oben angewendet wird, um schnell einen fertigen Tone-Stack-Charakter durchzuhören. **Flat** wendet keinen Tilt an. **Scoop** kippt Bass und Treble hoch und Mid runter — die klassische "Smiley"-Kurve für High-Gain-Rhythmus. **Boost** kippt Mid hoch (und Bass leicht runter) für einen Sound, der sich im Mix durchsetzt, auf Kosten von etwas Low-End-Gewicht. Wie Voicing ist das ein diskreter Schalter, kein sanft automatisierbarer Regler. |
| **Level** | -24 – +24 | 0 | dB | Output-Trim, angewendet nach dem Tone Stack und vor dem Dry/Wet-Mix. Nutze es, um Tenebraes Ausgangspegel an den Rest deiner Chain anzupassen, besonders nachdem du Gain oder die Tone-Stack-Bänder stark aufgedreht hast. |
| **Mix** | 0 – 100 | 100 | % | Dry/Wet-Blend der gesamten "wet" Chain (alles von Tight bis Level) gegen das unbearbeitete Input-Signal. Bei 100 % (Default) verhält sich Tenebrae wie eine normale Distortion im Signalweg. Niedrigere Werte mischen etwas vom Original-, unbearbeiteten Signal bei, nützlich für parallele/gemischte Rhythmus-Sounds; bei genau 0 % ist der Output ein sample-genauer (delay-kompensierter) Passthrough des Inputs. |

## Tipps

- **Beginne mit Tight und Gain, greife dann zu Voicing.** Stelle zuerst ein, wie viel Low End in die Kaskade einspeisen soll (Tight) und wie hart du sie ansteuerst (Gain), bevor du dich zwischen den Voicings Tight und Loose entscheidest — Voicing ändert den *Charakter* der Sättigung, nicht ihre Menge.
- **Nutze Mid, nicht nur Gain, um "den Chug" zu finden.** Die fixe Zwischenstufenfilterung der Kaskade erledigt schon viel von der Straffungsarbeit; der Großteil des hörbaren Unterschieds zwischen einem boxigen und einem fokussierten Rhythmus-Sound kommt vom Mid-Band nach der Kaskade (und dem Scoop-Preset von Tone Voice), nicht davon, Gain weiter aufzudrehen.
- **Bright ist bewusst subtil.** Weil es in eine stark sättigende Kaskade einspeist, erwarte keinen dramatischen Lautheitssprung — höre stattdessen auf einen Unterschied im Anschlags-Sizzle und in der harmonischen Dichte. Es stapelt sich mit Treble, statt mit ihm zu konkurrieren (Treibles Shelf sitzt unterhalb von Brights).
- **Tone Voice ist ein Startpunkt, kein Ziel.** Wähle Scoop oder Boost, um schnell in die Nähe einer klassischen Kurve zu kommen, und justiere dann weiter an Bass/Mid/Treble — sie bleiben voll live, unabhängig davon, welche Tone Voice ausgewählt ist.
- **Kombiniere Tenebrae mit einem Cab-Sim.** Tenebrae hat keine eigene Cabinet-Simulation; seinen Output in einen Cab-Sim/IR-Loader zu schicken (ein anderes Mitglied dieser Plugin-Suite oder ein beliebiges Drittanbieter-Tool) ist der erwartete Workflow und entfernt einen Großteil der rohen digitalen Härte, die eine High-Gain-Kaskade von sich aus erzeugt.
- **Mix unter 100 % ist für parallele/gemischte Sounds** gedacht, z. B. eine kleine Menge der Kaskade unter eine cleane DI zu mischen für einen hybriden Rhythmus-Sound, oder für einen schnellen "wie viel füge ich eigentlich hinzu"-A/B-Vergleich per Ohr gegen das trockene Signal.
</content>
