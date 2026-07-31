# Apotheosis — Praxis-Guide

*Praxisnahe Einstellungen für den True-Peak-Brickwall-Limiter, verankert in den Werkspresets.*

## Wo es hingehört

Apotheosis gehört ganz ans Ende des Master-Busses, nachdem jeder andere Prozessor — EQ, Bus-Kompression, Sättigung — seine Arbeit schon erledigt hat:

```
Mix-Bus → EQ/Bus-Kompression/Sättigung → Apotheosis (True-Peak-Limiter) → Export/Streaming-Plattform
```

Es ist nicht für einzelne Spuren gedacht; einmal einsetzen, auf dem Master, als finales Sicherheitsnetz und Loudness-Stufe vor dem Bounce. Weil es im True-Peak-(oversampleten) Bereich statt nur im Sample-Bereich arbeitet, fängt es auch Inter-Sample-Overshoot, den ein reiner Sample-Peak-Limiter übersehen würde — die Art, die erst nach dem Transcoding in ein verlustbehaftetes Streaming-Format als Clipping/Distortion auftaucht.

## Quick-Start-Einstellungen

### Streaming-taugliches Master — *Transparent Mastering*

Input Gain 3 dB, Ceiling −1 dBTP, Release 60 ms, Lookahead 10 ms, **Dither 24-Bit, True Peak Guard an**, Style **Transparent**, Auto Release 50 %, Noise Shaping Weighted.

Style: Transparent ist der empfohlene Mastering-Default unter den vier v0.4.0-Styles — die beste Transparenz pro dB, unter Nutzung der vollen Lookahead-Spanne des FIR-Attack-Smoothers. True Peak Guard macht aus Ceiling ein gemessenes statt ein margenbasiertes Versprechen: Die eigene Messung eines konformen Delivery-Meters läuft auf dem finalen heruntergesampelten Output und duckt exakt um den Überschuss, falls trotzdem etwas über Ceiling misst.

### Lautes, dichtes, modernes Master — *Punchy Loud Style*, *Dense/Loud Modern*

Punchy Loud Style: Input Gain 6 dB, Release 30 ms, Lookahead 4 ms, **Clip Mix 35 %**, Auto Release 40 %, Style **Punchy**.
Dense/Loud Modern: Input Gain 6 dB, Attack 10 ms, Auto Release 50 %, Clip Mix 35 %, Release Curve Smooth.

Style Punchy nutzt einen engeren FIR-Smoother und eine höhere Fast-Release-Depth-Cap als Transparent — es lässt Transienten-Spitzen bewusst härter durch, tauscht etwas Transparenz gegen wahrgenommene Lautheit. Clip Mix bei 35 % mischt den Tanh-Soft-Clip-Charakter obendrauf — ein üblicher moderner Loudness-Maximizer-Move —, läuft aber trotzdem durch dieselbe finale harte Ceiling-Klemme, sodass die Never-Exceed-Ceiling-Garantie unabhängig davon gilt.

### Punchy-Master mit Klassifikator-Unterstützung — *Punchy Master*

Input Gain 3 dB, Release 20 ms, Lookahead 1 ms, **Attack 25 ms**, Auto Release 30 %.

Attack ist hier der Transient-/Sustain-Klassifikator (Classic-Style-Attack, verschieden von der Style-Modus-FIR-Smoother-Spanne) — er lässt kurze Transienten-Peaks fast augenblicklich ihre Gain zurückholen, statt dem normalen Release-gesteuerten Pfad zu folgen, das dokumentierte „kurzes Lookahead + langer Attack + schneller Release"-Rezept der Referenzklasse, um wahrgenommene Lautheit zu maximieren und trotzdem den Punch zu erhalten.

### Sicheres archivales / true-peak-kritisches Delivery — *Safe Archival (True Peak)*

Input Gain 0 dB, **Ceiling −2 dBTP**, Release 120 ms, Lookahead 20 ms, Style **Safe**, **Oversampling 16x, OS Filter Linear Phase**, True Peak Guard an, Dither 24-Bit.

Style Safe ist die maximale Glätte-Option — drei kaskadierte FIR-Boxen statt einer oder zwei, die breiteste Fast-/Slow-Release-Aufteilung der fünf Styles — passend für klassisches, akustisches oder archivales Material, wo jede hörbare Gain-Bewegung schlimmer ist als etwas weniger Lautheit. 16x Linear-Phase-Oversampling kostet echte Latenz und CPU, liefert aber den niedrigsten veröffentlichten Alias-Floor (−100 dBc).

### Bildbreite-erhaltendes Master — *Wide Image Preserve*

**Stereo Link 40 %**, Attack 5 ms, Release Curve Smooth, Auto Release 20 %.

Stereo Link unter 100 % lässt jeden Kanal zunehmend unabhängiger detektieren und limitieren — das Setting für Fälle, in denen ein hart gepannter Peak in einem Kanal sonst die Gain des *gegenüberliegenden* Kanals mitziehen würde, auf Kosten eines nicht mehr perfekt fixierten Stereobilds unter Gain Reduction.

### Sauberer, geditherter Export — *Clean Export (Dithered)*

Input Gain 0 dB, Clip Mix 0 %, **Dither 16-Bit, Dither Shape Shaped**, Attack 0 ms, Auto Release 0 %.

Ein transparenter Limiter-Pass ohne sonst aktivierte Extras, plus Dither für einen finalen Bounce mit fester Bit-Tiefe — der Ausgangspunkt, um zu auditieren, ob sich Dither Shapes psychoakustische Formung für ein bestimmtes Master lohnt.

## Rezepte

1. **Streaming-Master bei etwa −14 LUFS.** Style Transparent, Ceiling −1 dBTP, True Peak Guard an, Input Gain nur so weit angehoben, bis die Integrated-LUFS-Anzeige (BS.1770-4-gated Metering, direkt implementiert) sich nah am Zielwert einpendelt — die meisten Streaming-Plattformen normalisieren ohnehin runter, lauter zu gehen kostet also meist nur Dynamikumfang, ohne hörbar lauter zu wirken, sobald die Plattform wieder runterregelt. *Warum:* True Peak Guard macht aus der Ceiling-Zahl eine wahre statt eine wahrscheinliche — ein gemessener BS.1770-4-True-Peak-Detektor läuft auf dem tatsächlichen heruntergesampelten Output, dieselbe Messung, die ein konformes Delivery-Meter durchführt, sodass ausgeliefert wird, was gesehen wurde.

2. **Club- oder physisches Release-Master.** Style Punchy oder Classic mit Clip Mix nach Gehör angehoben (25–50 %), Ceiling Richtung −0,3 bis −1 dBTP statt der streaming-sicheren −1-bis−2-dBTP-Range, Input Gain härter angeschoben für mehr anhaltende Gain Reduction. *Warum:* Ein Club-/physisches Master hat mehr Raum unter der Ceiling und weniger Grund, Headroom für die Loudness-Normalisierung einer Plattform zu lassen — Clip Mixs Tanh-Charakter obendrauf auf die Gain Reduction ist der bewusste „moderne Loudness"-Tausch, passend zu einem lauteren Zielwert.

3. **Entscheiden, wie hart tatsächlich limitiert wird.** **Delta** aktivieren, Input Gain hochziehen, bis einzelne Instrumente im Delta-Signal identifizierbar werden, dann zurücknehmen. *Warum:* Delta ersetzt den Output durch genau das, was der Limiter entfernt hat — der schnellste, verlässlichste Weg zu beurteilen, wie hart limitiert wird, weit vertrauenswürdiger als eine Entscheidung nach Gehör bei zwei unterschiedlichen Lautheiten (wo lauter immer besser klingt, unabhängig von der Qualität).

4. **Input-Gain-Settings ehrlich A/B-vergleichen.** **Unity Gain** aktivieren, während Input Gain bewegt wird. *Warum:* Unity Gain trimmt den Output um exakt minus Input Gain, sodass der *Charakter* von mehr Limiting gehört wird, ohne den Pegelunterschied — ohne das klingt ein lauteres Setting allein deshalb besser, weil es lauter ist, nicht weil es tatsächlich besser ist.

5. **Einen Oversampling-Faktor wählen, ohne dem eigenen Gehör zu misstrauen.** Oversampling auf 4x Minimum Phase lassen, außer Clip Mix ist nennenswert aktiv oder es geht um Archival-/Mastering-für-Transcode-Arbeit — einmal zu Beginn einer Session festlegen, nicht mitten im Mix. *Warum:* Ein höherer Faktor reduziert nur Alias-Energie, die von harter Nichtlinearität erzeugt wird (der Clip-Mix-Pfad, und die eigenen scharfen Kanten der Gain-Envelope); bei Material, das die Ceiling bei 0 % Clip Mix kaum berührt, gibt es von vornherein kaum Alias-Energie zu entfernen, der hörbare Unterschied ist also nahe null, während die CPU-/Latenzkosten real sind.

> **Theorie — warum True Peak nicht dieselbe Zahl ist wie der Sample-Peak.** Eine digitale Datei speichert nur diskrete Samples, aber die analoge Wellenform, die ein D/A-Wandler (oder der Decoder eines verlustbehafteten Codecs) daraus rekonstruiert, kann *zwischen* Samples höher ausschlagen, als jeder einzelne Sample-Wert zeigt. Ein Limiter, der rein im Sample-Bereich arbeitet, kann ein Signal durchlassen, das auf einem gewöhnlichen Peak-Meter „sicher" misst, aber nach der Wandlung ins Analoge clippt, oder nach dem Transcoding in ein verlustbehaftetes Streaming-Format, das denselben Inter-Sample-Overshoot rekonstruiert. Apotheosis' True-Peak-Detection läuft innerhalb einer oversampleten Domäne (4x/8x/16x), genau damit sie diesen rekonstruierten Peak sehen — und eine Ceiling dagegen halten — kann, nicht nur die gespeicherten Samples. True Peak Guard geht noch einen Schritt weiter: statt sich allein auf die oversamplete Detection zu verlassen, misst es den tatsächlichen heruntergesampelten Output erneut mit einem BS.1770-4-konformen Detektor — demselben Standard, den ein Delivery-Meter nutzt — und korrigiert nur, wenn diese Messung, nicht nur die interne Schätzung, über Ceiling liegt.

## Fallstricke

- **Lookahead, Oversampling und OS Filter sind prepare-gelatchte „Setup"-Parameter, nicht live-automatisierbar.** Eine Änderung greift erst, wenn der Host das Plugin das nächste Mal neu initialisiert (Samplerate-Wechsel, Transport-Stop/Start, erneutes Öffnen des Projekts) — einmal zu Session-Beginn festlegen, nicht mitten im Mix, und keinen sofort hörbaren Unterschied bei einer Änderung während der Wiedergabe erwarten.
- **Die sieben v0.4.0-Regler (Style, Oversampling, OS Filter, True Peak Guard, Noise Shaping, Delta, Unity Gain) haben noch keine eigenen Editor-Regler** — die generische Parameter-Ansicht des Hosts nutzen, um sie zu automatisieren oder einzustellen, bis die M3-GUI kommt.
- **Dither wird bei der Base Rate nicht auf Ceiling zurückgeklemmt** — ein diskretes Output-Sample kann bis zu etwa 1 LSB über der nominalen Ceiling liegen (etwa −90 dBFS bei 16-Bit, −138 dBFS bei 24-Bit). Das ist Standard-, erwartetes Verhalten bei gedithertem Output, weit innerhalb der True-Peak-Test-Toleranz, keine Verletzung der Garantie.
- **Die gemessene Ceiling-Garantie ist eine 4x-Meter-Garantie.** Ein höher auflösendes Referenz-Meter kann bei bestimmtem Content nahe 0,45x Nyquist legitim etwas über Ceiling messen — eine Eigenschaft des BS.1770-4-Standards selbst, nicht dieses Plugins.
- **Weighted Noise Shaping ist für 44,1/48-kHz-Delivery gefittet** und wird bei höheren Projekt-Sampleraten unverändert genutzt, wo die Passung zur Hörbarkeitskurve nicht mehr so präzise gilt.
- **Delta und Unity Gain sind Monitor-Modi — nie Render-Modi.** Delta umgeht Dither, da auditiert und nicht gerendert wird; beide vor dem Bounce ausschalten.
- **Wenn Noise Shaping auf Weighted steht, überschreibt es Dither Shape vollständig** — die Flat-/Shaped-Wahl tut dann nichts mehr.
- **Das Voicing ist durchgehend aus veröffentlichter Dokumentation und allgemeiner DSP-/Dithering-Literatur abgeleitet, nicht gegen die Binary irgendeines Wettbewerbers gemessen, gebenchmarkt oder reverse-engineered.**
