<!-- German translation of tenebrae.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Tenebrae-Icon" width="120"/></p>

# Tenebrae — Bedienungsanleitung

*Eine Liturgie der Schatten — kaskadierte High-Gain-Distortion für den schwersten Rhythmus-Sound.*

## Was es ist

Tenebrae ist eine High-Gain-Rhythmusgitarren-Distortion, aufgebaut um eine Kaskade aus drei oversampelten Waveshaper-Stufen, jede zunehmend straffer und dunkler als die vorherige, sodass der Sound in ein fokussiertes „Chug"-Band konvergiert, statt sich mit steigendem Gain zu einem immer fizzeligeren Durcheinander aufzuschichten. Es ist kein Boost/Overdrive (das ist der Job des Schwester-Plugins `overture`) und kein Cab-Sim — es ist die „Wall of Gain" selbst: die zentrale Distortion-Stufe, in die ein Boost-Pedal hineindrückt, und die Stufe, nach der ein Cab-Sim/IR-Loader sitzt.

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
   Output <-- Mix <-- Level <-- Gate <-- Presence <-- Treble <-- Mid <-- Bass <--+  (tilted by Tone Voice)
     ^
     |
delay-compensated dry path
```

Die drei Kaskadenstufen laufen innerhalb eines 8x oversampelten Blocks, damit die von allen drei Nichtlinearitäten erzeugten Harmonischen — nicht nur die der ersten — außerhalb des hörbaren Bands bleiben. Der von **Mix** genutzte Dry-Pfad wird automatisch gegen diese Oversampling-Latenz delay-kompensiert, und das Plugin meldet seine Gesamtlatenz an den Host, damit die Wiedergabe sample-genau mit jeder anderen Spur ausgerichtet bleibt. Die vollständige technische Aufschlüsselung, einschließlich der Voicing-Tabelle pro Kaskadenstufe und der Latenz-Kompensationsstrategie, findest du in [`docs/architecture.md`](architecture.md).

## Presets

Die Preset-Leiste am oberen Rand des Plugin-Fensters (`<` / Preset-Name / `>` / Save / Save As... / Delete / Import... / Export...) gibt dir acht Werks-Startpunkte plus deine eigenen gespeicherten Presets. Klicke auf den Preset-Namen, um das vollständige Factory/User-Menü zu durchstöbern, oder nutze die Pfeile, um alphabetisch durch die Presets zu blättern. Was jedes Werkspreset bewirkt, steht in [`docs/presets.md`](presets.md). „Set current as default" (im Preset-Menü) sorgt dafür, dass das aktuell eingestellte Setting beim nächsten Öffnen des Plugins automatisch geladen wird.

## Parameterreferenz

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Tight** | 20 – 300 | 90 | Hz | Hochpassfilter, platziert *vor* der Gain-Kaskade. Höher gedreht, entfernt es mehr Low End aus dem Signal, bevor es auf die Clipper-Stufen trifft, und hält Palm Mutes und Chugs auf den tiefen Saiten perkussiv, statt dass sie ausfransen, sobald die Kaskade sättigt. Niedriger drehen für ein volleres, boomigeres Low End (nützlich bei Drop-Tunings, die du „groß" statt straff wirken lassen willst); höher drehen für maximale Palm-Mute-Artikulation. |
| **Gain** | 0 – 40 | 24 | dB | Pre-Gain in die oversampelte 3-Stufen-Waveshaper-Kaskade — der zentrale „wie viel Distortion"-Regler. Jede Kaskadenstufe hat zusätzlich ihren eigenen fixen internen Drive obendrauf, sodass selbst Gain bei 0 dB noch einen echt gesättigten High-Gain-Sound erzeugt; dieser Regler dreht die Kaskade härter auf, statt Distortion ein- und auszuschalten. |
| **Voicing** | Tight / Loose | Tight | – | Schaltet die fixe Per-Stufen-Asymmetrie und Zwischenstufenfilterung der Kaskade zwischen zwei Voicings um. **Tight** (Default) ist die straffere, moderner ausgerichtete Kaskade, um die herum das Plugin ursprünglich voiced wurde. **Loose** ist eine weicher gedrivte, breitbandigere Alternative — weniger asymmetrisches Clipping und lockerere Zwischenstufenfilterung auf jeder Stufe, für einen eher vintage-orientierten, etwas luftigeren und boomigeren Charakter. Das ist ein diskreter Schalter (wie eine Amp-Kanalwahl), kein sanft automatisierbarer Regler — erwarte einen kleinen hörbaren Sprung im Moment des Umschaltens. |
| **Bright** | Off / On | Off | – | Aktiviert eine fixe High-Shelf-Preemphase, angewendet *vor* der Gain-Kaskade, modelliert nach dem „Bright Switch", den man auf vielen High-Gain-Amp-Kanälen findet (und, lose, nach der Presence-Spitze eines helleren Cabinets — Tenebrae hat keine eigene Cab-Simulation, das ist also der nächstliegende „cab-adjacente" Regler, den es bietet). Weil das angehobene Signal danach drei kaskadierte Clipping-Stufen durchläuft, ist sein Effekt auf die Gesamtlautheit bewusst subtil — Sättigung komprimiert die zusätzlichen Höhen wieder herunter — was sich ändert, sind Harmonic Content und Anschlags-Sizzle, die in die Kaskade einspeisen, nicht der reine Output-Pegel. |
| **Bass** | -15 – +15 | 0 | dB | Low-Shelf-Band des Tone Stacks nach der Kaskade, zentriert bei 150 Hz. Boosten für einen volleren, low-end-lastigeren Chug; absenken, um nach der Kaskade zusätzlich zu straffen (ergänzend zu dem, was Tight davor schon entfernt hat). |
| **Mid** | -15 – +15 | 0 | dB | Peaking-Band des Tone Stacks nach der Kaskade, zentriert bei 650 Hz mit moderat schmalem Q. Das ist der klassische „Scooped Mids"-Regler für den High-Gain-Rhythmus-Sound — absenken für den mid-gescoopten, mid-2000er-Metal-Chug-Sound; boosten (oder nahe 0 lassen), um genug Mid-Präsenz zu behalten, damit sich der Sound in einem dichten Mix durchsetzt. |
| **Treble** | -15 – +15 | 0 | dB | High-Shelf-Band des Tone Stacks nach der Kaskade, zentriert bei 5 kHz (in v0.2.0 von 3,5 kHz angehoben, damit es klar oberhalb sowohl von Brights Shelf vor der Kaskade als auch des neuen Presence-Reglers sitzt — siehe unten). Boosten für mehr Anschlag und Höhen-Sizzle; absenken, um übrig gebliebenes Fizz aus den Harmonischen der Kaskade zu zähmen — besonders nützlich, wenn nach Tenebrae kein Cab-Sim/IR-Loader läuft, der diesen Höhen-Rolloff für dich übernimmt. |
| **Tone Voice** | Flat / Scoop / Boost | Flat | – | Ein Ein-Schalter-Tilt, der zusätzlich zu den (weiterhin voll live bleibenden) Bass-/Mid-/Treble-Reglern oben angewendet wird, um schnell einen fertigen Tone-Stack-Charakter durchzuhören. **Flat** wendet keinen Tilt an. **Scoop** kippt Bass und Treble hoch und Mid runter — die klassische „Smiley"-Kurve für High-Gain-Rhythmus. **Boost** kippt Mid hoch (und Bass leicht runter) für einen Sound, der sich im Mix durchsetzt, auf Kosten von etwas Low-End-Gewicht. Wie Voicing ist das ein diskreter Schalter, kein sanft automatisierbarer Regler. |
| **Presence** | -12 – +12 | 0 | dB | High-Shelf-Regler bei 2,4 kHz, angewendet *nach* Kaskade und Tone Stack (im Gegensatz zu Bright, das vor der Kaskade sitzt). Modelliert nach dem Presence-Regler der Referenzklasse hochverstärkter Amps — einer Gegenkopplungsstufe der Endstufe, die die hochmittigen/hohen Frequenzanteile des bereits verzerrten Signals formt. Bei 0 dB (Default) ist dieser Regler ein echter Passthrough — er fügt keine Färbung hinzu, bis du ihn bewegst. Nutze ihn, um obendrauf auf den eigenen harmonischen Inhalt der Kaskade „Cut" oder Biss hinzuzufügen, ohne die Kaskade selbst erneut zu füttern (dafür ist Bright da). |
| **Gate Threshold** | -80 – 0 | -48 | dB | Pegel, unterhalb dessen das Gate schließt. Gated das vollständig voicede, wet Signal (nach Kaskade und Tone Stack), erfasst also auch das Rauschen, das die Kaskade selbst durch ihren Gain erzeugt, nicht nur den Rauschteppich des Inputs. Höher drehen (Richtung 0 dB) für ein aggressiveres Gate, das zwischen den Noten härter zuklemmt; niedriger drehen (Richtung -80 dB), um leiseres Material (Sustain-Ausklang, Ambience) unangetastet durchzulassen. |
| **Gate Attack** | 0.1 – 20 | 1 | ms | Wie schnell das Gate öffnet, sobald das Signal Threshold überschreitet. Der Default (1 ms) ist schnell genug, dass Anschläge nie geklippt oder verzögert werden. |
| **Gate Hold** | 0 – 500 | 20 | ms | Wie lange das Gate offen bleibt, nachdem das Signal wieder unter Threshold fällt, bevor Release einsetzt. Verhindert, dass die natürliche Amplitudenwelligkeit einer gehaltenen Note oder eines palm-gemuteten Akkords das Gate erneut triggert/flattern lässt. |
| **Gate Release** | 5 – 2000 | 150 | ms | Wie langsam das Gate schließt, nachdem Hold abgelaufen ist. Kürzere Release-Zeiten passen zu schnellen, perkussiven Palm-Mute-Rhythmusparts; längere Release-Zeiten lassen anhaltende Akkorde/Noten natürlich ausklingen, statt sie abrupt abzuschneiden. |
| **Gate** | Off / On | **On** | – | Umgeht das gesamte Gate-Modul, wenn aus (ein echter Passthrough — Threshold/Attack/Hold/Release haben dann keine Wirkung). Standardmäßig **an**, anders als jede andere v0.2.0-Ergänzung — die Recherche hinter dem Rework dieses Plugins ist sich einig, dass ein Gate für kaskadierte High-Gain-Distortion in diesem Genre eine strukturelle Erwartung an „tighten Chug"-Sound ist, kein optionales Extra; das Laden einer alten (Pre-v0.2.0-)Session aktiviert das Gate daher mit seinen Default-Einstellungen zusätzlich zu dem, was du eingestellt hattest, was das Ausklang-/Stille-Verhalten dieser Session hörbar verändern kann — Details im CHANGELOG. |
| **Level** | -24 – +24 | 0 | dB | Output-Trim, angewendet nach Presence und dem Gate, vor dem Dry/Wet-Mix. Nutze es, um Tenebraes Ausgangspegel an den Rest deiner Chain anzupassen, besonders nachdem du Gain oder die Tone-Stack-Bänder stark aufgedreht hast. |
| **Mix** | 0 – 100 | 100 | % | Dry/Wet-Blend der gesamten „wet" Chain (alles von Tight bis Level) gegen das unbearbeitete Input-Signal. Bei 100 % (Default) verhält sich Tenebrae wie eine normale Distortion im Signalweg. Niedrigere Werte mischen etwas vom Original-, unbearbeiteten Signal bei, nützlich für parallele/gemischte Rhythmus-Sounds; bei genau 0 % ist der Output ein sample-genauer (delay-kompensierter) Passthrough des Inputs. |

## Tipps

- **Beginne mit Tight und Gain, greife dann zu Voicing.** Stelle zuerst ein, wie viel Low End in die Kaskade einspeisen soll (Tight) und wie hart du sie ansteuerst (Gain), bevor du dich zwischen den Voicings Tight und Loose entscheidest — Voicing ändert den *Charakter* der Sättigung, nicht ihre Menge.
- **Nutze Mid, nicht nur Gain, um „den Chug" zu finden.** Die fixe Zwischenstufenfilterung der Kaskade erledigt schon viel von der Straffungsarbeit; der Großteil des hörbaren Unterschieds zwischen einem boxigen und einem fokussierten Rhythmus-Sound kommt vom Mid-Band nach der Kaskade (und dem Scoop-Preset von Tone Voice), nicht davon, Gain weiter aufzudrehen.
- **Bright ist bewusst subtil.** Weil es in eine stark sättigende Kaskade einspeist, erwarte keinen dramatischen Lautheitssprung — höre stattdessen auf einen Unterschied im Anschlags-Sizzle und in der harmonischen Dichte.
- **Tone Voice ist ein Startpunkt, kein Ziel.** Wähle Scoop oder Boost, um schnell in die Nähe einer klassischen Kurve zu kommen, und justiere dann weiter an Bass/Mid/Treble — sie bleiben voll live, unabhängig davon, welche Tone Voice ausgewählt ist.
- **Presence und Treble leben beide in den Höhen, erledigen aber unterschiedliche Jobs.** Treble formt den eigenen High-Shelf des Tone Stacks; Presence sitzt danach und fügt einen zweiten, unabhängig automatisierbaren Höhen-Push hinzu — nutze Presence für eine finale „Cut"-Anpassung, ohne deine Treble-Einstellung neu auszubalancieren.
- **Lass Gate für chug-fokussierte Rhythmusarbeit an.** Es ist standardmäßig aus gutem Grund an — spielst du anhaltende Leads oder möchtest den eigenen Rauschteppich der Kaskade als Ambient-Textur nutzen, schalte es aus oder ziehe Threshold Richtung -80 dB herunter, statt es gegen dein Spiel ankämpfen zu lassen.
- **Kombiniere Tenebrae mit einem Cab-Sim.** Tenebrae hat keine eigene Cabinet-Simulation; seinen Output in einen Cab-Sim/IR-Loader zu schicken (ein anderes Mitglied dieser Plugin-Suite oder ein beliebiges Drittanbieter-Tool) ist der erwartete Workflow und entfernt einen Großteil der rohen digitalen Härte, die eine High-Gain-Kaskade von sich aus erzeugt.
- **Mix unter 100 % ist für parallele/gemischte Sounds** gedacht, z. B. eine kleine Menge der Kaskade unter eine cleane DI zu mischen für einen hybriden Rhythmus-Sound, oder für einen schnellen „wie viel füge ich eigentlich hinzu"-A/B-Vergleich per Ohr gegen das trockene Signal.
