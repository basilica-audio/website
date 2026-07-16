<!-- German translation of seraph.en.md (English source generated from seraph/docs/manual.md on 2026-07-16) — do not hand-edit; re-translate after the English manual is resynced. -->

<p align="center"><img src="assets/icon.png" alt="Seraph-Icon" width="120"/></p>

# Seraph — Bedienungsanleitung

*Stimmen von oben – ein Chor- und Vocal-Prozessor für Operatic-Metal-Vocals.*

## Was Seraph ist

Seraph ist ein Vocal-Prozessor im Channel-Strip-Stil, gebaut für die Lead- und Chor-Vocal-Parts von Operatic Metal (große, cineastische Produktionen): eine Sopran-Leadlinie, ein geschichtetes Chor-Backing oder ein gesprochenes/gegrowltes Zwischenspiel, das sich sauber gegen schwer geschichtete Gitarren und ein Orchester behaupten muss, ohne zu verschwinden oder hart zu klingen.

Es vereint vier Processing-Stufen, zu denen man bei einem Vocal normalerweise separat greifen würde:

1. **De-Ess** – zähmt Zischlaute ("s", "sch", "t"-Konsonanten), die durch ein helles Vocal-Mikro und starkes Top-End-EQ an anderer Stelle im Mix (Becken, verzerrtes Gitarren-Fizz, Streichersektionen) tendenziell ermüdend werden.
2. **Air** – fügt das Gefühl luftiger Offenheit oberhalb des natürlichen Präsenzbereichs des Vocals hinzu (oder entfernt es) – die Art von Schimmer, die einem opernhaften Sopran hilft, sich gegen eine Wand aus Gitarren durchzusetzen.
3. **Gentle Compressor** – gleicht die Dynamik mit einem "Glue"-artigen Kompressor aus, sodass das Vocal auf einem konstanten Pegel im Mix sitzt, ohne hörbar zu pumpen.
4. **Doubler** – ein click-freier Vier-Stimmen-Doubler/Chorus, der einen einzelnen Take zu einer kleinen Chor-Fläche verdickt, ohne die diskreten Pitch-Shift-Artefakte granularer Doubler.

Alles bis Mix/Output ist ein einziger, in sich geschlossener Channel Strip: Setze Seraph auf einen Vocal- oder Chor-Bus, stelle De-Essing und Air nach Geschmack ein, füge bei dynamisch unruhigen Takes einen Hauch Glue-Kompression hinzu, und nutze den Doubler, um eine Leadlinie zu verbreitern oder einen Chor-Part zu verdicken.

## Wo es in einer Heavy-Music-Signalkette sitzt

Seraph ist dafür gedacht, auf Vocal-/Chor-Spuren oder einem Vocal-Bus zu laufen, typischerweise:

```
Vocal/choir recording -> (tuning/editing, if used) -> Seraph -> reverb/delay send -> mix bus
```

Da Seraph **0 Samples Latenz** meldet, braucht es nie eine host-seitige Plugin-Delay-Compensation-Berechnung – es lässt sich gefahrlos an jeder Stelle einer Vocal-Kette einsetzen, auch parallel (z. B. auf einem gedoppelten/gemischten parallelen Vocal-Bus), ohne Phasenausrichtungs-Überraschungen gegenüber einem Dry-Pfad.

Ein paar praktische Platzierungen in einer Heavy-Music-Produktion:

- **Lead-Vocal-Spur**: Zuerst De-Ess (Mikro-Nähe und Konsonanten), ein Hauch Air, damit eine opernhafte Stimme sich gegen verzerrte Gitarren und Orchesterstreicher durchsetzt, etwas Comp für Konsistenz, und eine *dezente* Menge Double (10–20 %), falls der Take mehr Fülle braucht, ohne künstlich gedoppelt zu klingen.
- **Chor-/Backing-Vocal-Bus**: kräftigeres Double (40–70 %) mit vollem Width für eine breite, geschichtete Chor-Fläche aus wenigen aufgenommenen Takes; De-Ess und Air konservativer eingestellt, da Chor-Blends pro Stimme meist bereits weniger zischend/hart klingen als ein Solo-Lead.
- **Gesprochenes/gegrowltes Zwischenspiel**: De-Ess ist oft unnötig (wenig Zischlaut-Energie in einer gegrowlten Performance); Air und eine stärkere Comp-Einstellung helfen einem gesprochenen Zwischenspiel, gegen ein leises orchestrales Backing präsent und pegelkonsistent zu bleiben.

## Signalfluss

```
input -> De-Ess (sibilance dynamic EQ, + Listen mode) -> Air (12 kHz high-shelf)
       -> Gentle Compressor (broadband glue) -> Doubler (4 voices, per-voice pan)
       -> Output trim -> Mix -> output
```

Das vollständige technische Signalfluss-Diagramm und die DSP-Design-Notizen findest du in [`architecture.md`](architecture.md).

## Parameterübersicht

| Parameter | Bereich | Standard | Einheit | Was es bewirkt |
|---|---|---|---|---|
| **De-Ess** | 0-100 | 30 | % | Menge der Zischlaut-Gain-Reduction. Skaliert die maximale Reduction, die auf das erkannte Band angewendet wird (bis zu 24 dB bei 100 %). 0 % ist ein exakter Bypass des De-Essers. Starte niedrig (20–40 %) und erhöhe nur so weit wie nötig – übertriebenes De-Essing lässt "s"-Laute genuschelt oder gedämpft klingen. |
| **De-Ess Freq** | 3,000-12,000 | 7,000 | Hz | Mittenfrequenz des Zischlaut-Erkennungs-/Reduction-Bands. Weibliche/Sopran-Vocals zischen oft höher (7–9 kHz); tiefere männliche Vocals oder stark proximity-gemikte Takes brauchen eventuell 5–6 kHz. Nutze **De-Ess Listen**, um die richtige Frequenz nach Gehör zu finden. |
| **De-Ess Listen** | off/on | off | - | Solot das erkannte Zischlaut-Band statt des bearbeiteten Vocals, sodass du De-Ess Freq durchfahren und genau hören kannst, welches Frequenzband anvisiert wird, bevor du die Reduction einstellst. Vor dem Mischen wieder ausschalten – der Listen-Modus ist eine Einstellhilfe, keine Mix-Einstellung. |
| **Air** | -12 to +12 | +3 | dB | Fixes 12-kHz-High-Shelf. Boost für Offenheit/Schimmer oberhalb des natürlichen Top-Ends eines Vocals (typisch für ein Lead, das sich gegen einen dichten Mix durchsetzen muss); Cut, wenn ein helles Mikro/Preamp oder aggressives De-Essing das Vocal dünn oder hart klingen lässt. |
| **Comp** | 0-100 | 0 | % | Menge eines sanften, breitbandigen Downward-Compressors. Skaliert Threshold (bis -20 dBFS) und Ratio (bis 3:1) gemeinsam – eine "Glue"-Einstellung, kein quetschender Limiter. 0 % ist ein exakter Bypass. Es wird kein automatisches Makeup-Gain angewendet; nutze **Output** zum Ausgleich, falls eine höhere Comp-Einstellung das Vocal leiser wirken lässt. |
| **Double** | 0-100 | 25 | % | Doubler-Send-Menge: wie stark die vier gedoppelten Stimmen über dem zentrierten Dry-Signal eingemischt werden. 0 % ist ein exakter Bypass des Doublers. Dezente Mengen (10–25 %) verdicken ein Lead, ohne einen offensichtlichen "Chorus"-Effekt; höhere Mengen (40 %+) bauen eine vollere Klein-Chor-Fläche auf, am besten geeignet für Backing-/Chor-Parts statt eine exponierte Leadlinie. |
| **Double Detune** | 0-50 | 15 | cents | Tiefe des kontinuierlichen Pitch-Wobbles des Doublers (ein sanftes, modulated-delay-basiertes Detune, kein diskreter Pitch-Shift – immer click-frei). Niedrigere Werte (5–10 cents) klingen wie ein enges, dezentes Double; höhere Werte (30–50 cents) klingen loser und chorus-artiger. |
| **Double Width** | 0-100 | 100 | % | Stereo-Streuung der vier Doubler-Stimmen. 0 % hält alle vier Stimmen zentriert (mono-kompatibel, nützlich, wenn das Vocal in einem mono-fold-down-sensiblen Mix zentriert bleiben muss); 100 % verteilt sie über das gesamte Stereofeld für einen breiten Chor-Effekt. |
| **Mix** | 0-100 | 100 | % | Gesamte Dry/Wet-Mischung. Steht standardmäßig auf 100 % (vollständig prozessiert), da Seraph als vollwertiger Channel Strip laufen soll, nicht eingemischt werden – senke ihn nur für Parallel-Processing-Setups (z. B. um ein de-essed/gedoppeltes Signal unter ein ansonsten unangetastetes Dry-Vocal zu mischen). |
| **Output** | -24 to +24 | 0 | dB | Output-Trim, angewendet nach dem Doubler und vor Mix. Nutze ihn, um Pegeländerungen durch Comp oder Double auszugleichen, bevor das Signal die nächste Stufe deiner Kette erreicht. |

Alle Parameter sind geglättet (kein Zipper-Noise bei Automation oder manuellen Reglerbewegungen) und automationssicher.

## Tipps

- **De-esse, bevor du Air oder Comp hinzufügst.** Zischlaut-Energie sitzt im selben Bereich, den Air anhebt, und ein breitbandiger Kompressor reagiert auf Zischlaut-Peaks genau wie auf jeden anderen Transienten – wenn du zuerst de-esst, arbeiten beide nachfolgenden Stufen mit einem saubereren Signal.
- **Nutze De-Ess Listen, wenn du dir nicht sicher bist, wo die Zischlaute sitzen.** Es geht deutlich schneller, De-Ess Freq durchzufahren, während das erkannte Band gesolot ist, als es nach Gehör gegen den vollen Mix durchzufahren.
- **Comp ist ein Glue-Regler, kein Leveling-Werkzeug.** Wenn ein Take stark inkonsistente Pegel hat (sehr leise Strophen, sehr laute Refrains), behebe das zuerst mit Clip Gain oder einem dedizierten Leveling-Kompressor vorgeschaltet; Comps sanftes 3:1-Maximum-Ratio soll einem bereits einigermaßen ausgeglichenen Take Konsistenz und Kohäsion geben, nicht einen wild unebenen retten.
- **Double ist additiv, kein Ersatz für echte gedoppelte Takes.** Bei Chor-Parts klingt eine Prise Double in niedriger bis moderater Menge zusätzlich zu ein paar echten aufgenommenen Layern meist voller und natürlicher, als sich allein auf Double zu verlassen, um aus einem einzigen Take einen ganzen Chor zu simulieren.
- **Behalte Width bei einem mono-sensiblen Mix im Blick.** Falls dein Material auf Mono gefaltet werden könnte (Streaming-Plattformen, manche Broadcast-Ketten), prüfe den Doubler mit Width Richtung 0 % zurückgezogen, um sicherzustellen, dass sich die gedoppelten Stimmen beim Summieren nicht unangenehm auslöschen.
- **Null Latenz bedeutet, Seraph ist sicher in Parallelketten.** Da Seraph nie eine Plugin-Delay meldet, kannst du einen Seraph-bearbeiteten Vocal-Bus frei gegen einen unangetasteten Dry-Vocal-Bus mischen (oder eine Spur duplizieren und zwei unterschiedliche Seraph-Einstellungen darauf laufen lassen), ohne dass deine DAW irgendetwas zeitlich ausrichten muss.

## Bekannte Einschränkungen (v0.1.0)

- Die GUI ist ein funktionaler Slider-/Knob-Editor (eine eigene, vektorgezeichnete GUI ist ein späterer Meilenstein – siehe die Projekt-Roadmap).
- Noch keine Factory-Presets (ebenfalls ein späterer Meilenstein).
- Das Detune des Doublers ist ein kontinuierliches, vibrato-artiges Pitch-Wobble, kein vollständiger formant-erhaltender Pitch-Shift – innerhalb seines 0–50-Cent-Bereichs erzeugt das keine hörbaren "Chipmunk"-Formant-Artefakte, ist aber kein Ersatz für ein dediziertes Harmonizer-/Pitch-Shifter-Plugin, falls du größere, formant-korrigierte Tonhöhenintervalle brauchst.
