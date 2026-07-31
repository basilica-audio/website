# Signalketten-Guide

*Wo die dreizehn Basilica-Audio-Plugins in einer Heavy-Music-Produktion sitzen — Gitarren, Bass, Busse, Mastering, Vocals & Chor und Raum.*

Dieser Guide dreht sich um **Reihenfolge und Platzierung**, nicht um vollständige Parameter-Referenzen — dafür hat jedes Plugin seinen eigenen [Praxis-Guide](#guides-für-einzelne-plugins). Verstehe diese Seite als die Skizze, die du dir aufs Whiteboard malen würdest, bevor du eine Session öffnest: Was kommt vor was, und warum die Reihenfolge nicht willkürlich ist.

Die Suite geht von einer Heavy-Music-Produktion mit gemischter Instrumentierung aus: geschichtete verzerrte Gitarren, eine Rhythmusgruppe und orchestrale/Chor-Elemente in derselben Mischung. Genau diese Kombination ist der Grund, warum es mehrere dieser Plugins überhaupt gibt — ein Single-Band-Kompressor oder ein generischer Stereo-Widener verhält sich auf einer Wand aus Gitarren völlig anders als auf einer Streichersektion. Deshalb ist Triptych multiband, und deshalb ist Firmaments Verbreiterung strukturell mono-sicher.

Keine der folgenden Einstellungen ist in Stein gemeißelt. Es sind Ausgangspunkte, verankert in den Werkspresets der Plugins — lies das „Warum" hinter jedem Move, nicht nur die Zahl, und rechne damit, alles an deinem eigenen Material nachzujustieren.

## Die Kette im Überblick

```
Gitarren:  DI -> Silentium (Gate) -> Overture (Tight Boost) -> Tenebrae (Gain) -> Nave (Cab IR) --+
Bass:      DI/Amp-Sim -> Crypta (3-Band-Voicing) -----------------------------------------------+
                                                                                                   |
                                                                          Gitarren-/Bass-Busse -> Aureate / Triptych (Glue)
                                                                                                   |
Vocals:    Mikro -> Lancet (chirurgisch) -> Miserere (Parallel-Channel) -> Seraph (Doubler/Air) --+     |
Chor:                                                        Seraph (Spread) -> Aureate --+ |     |
                                                                                            v v     v
Orchester-/Chor-Bus -> Aureate (Glue) -> Firmament (Breite, mono-sicher) -> Requiem (Raum) -+
                                                                                            |
                                                                                     Mix-Bus -> Triptych (optional) -> Apotheosis (True-Peak-Limiter) -> Export
```

Betrachte das als Startgerüst, nicht als Regel. Die Abschnitte unten gehen jeden Zweig durch und erklären die Platzierungslogik.

## Gitarren: Overture → Tenebrae → Nave

Die Kern-Gitarrenkette ist ein **Tightening-Boost, dann die Gain-Stufe, dann die Cabinet** — dieselbe Logik wie ein Pedal-vor-Amp-vor-Mikro-Rig, nur als Plugins:

1. **Overture** entfernt Low End aus dem Signal, *bevor* irgendetwas clippt, damit Palm Mutes und Chugs auf den tiefen Saiten artikuliert bleiben, statt zu Brei zu werden, sobald die nächste Stufe ihren eigenen Gain sättigt. Der eigene Drive ist standardmäßig bewusst zurückhaltend — es geht darum, zu formen, was auf die nächste Stufe trifft, nicht selbst die Distortion zu sein.
2. **Tenebrae** ist die Haupt-Gain-Stufe. Es hat konstruktionsbedingt keine Cabinet-Simulation, bleibt also ein sauberer Baustein: Overture davor für Low-End-Kontrolle, danach eine Cab-/IR-Stufe, die zum Rest der Kette passt.
3. **Nave** faltet das jetzt verzerrte, noch rohe Signal mit einer Cabinet-plus-Mikrofon-Impulsantwort — der Schritt, der aus einem brummigen Amp-Sim-Output etwas macht, das klingt, als wäre es im Raum abgenommen worden. Es sitzt normalerweise *nach* der Distortion und *vor* EQ-/Bus-Processing.

```
Gitarren-DI -> Silentium (Gate) -> Overture (Tight Boost) -> Tenebrae (High-Gain) -> Nave (Cab IR) -> EQ/Bus
```

### Silentium: Platzierungsoptionen, und warum die Detektor-Position zählt

Silentium ist eine Detection-and-Dynamics-Stufe, kein Tone-Shaping-Tool — genau deshalb ändert sich, worauf es reagiert, je nachdem, *wo* du es einsetzt:

- **Vor Overture/Tenebrae** (das saubere DI-Signal gaten) ist der Standard-Ansatz für geschichtete Rhythmusgitarren — es vermeidet, dass Gating-Artefakte mitverstärkt und mitverzerrt werden, und lässt den Sidechain-Hochpass ein unverzerrtes Signal als Trigger sehen statt eines, das eine nachfolgende Gain-Stufe schon angedickt hat.
- **Nach der Amp-/Cab-Stufe** nur, wenn das Rauschen, das du eigentlich bekämpfst, dort tatsächlich entsteht (Amp-Rauschen, Cab-Sim-Grundrauschen) statt schon im DI-Signal vorhanden zu sein — nach der Distortion zu gaten, um ein Problem zu beheben, das schon davor existiert, jagt das Symptom am falschen Ort.
- **Vor jedem Reverb/Delay** in der Kette, immer, außer du willst bewusst einen gegateten Reverb-Tail — sonst schließt das Gate auf der trockenen Gitarre und schneidet einen ausklingenden Tail mitten im Ausklang ab.
- **Eine Instanz pro Spur**, nicht eine auf dem Gitarrenbus, bei einer Wall-of-Guitars-Mischung. Jede Performance hat ihr eigenes Pick-Attack-Timing; Lookahead pro Spur hält jede Ebenen-Attacke straff und synchron, wo ein einzelnes Gate auf Bus-Ebene sie verschmieren würde.

> **Theorie — warum Detektor-Position und -Typ das Ergebnis ändern.** Ein Gate hört nicht deiner ganzen Mischung zu; es hört dem zu, was der Detektor bekommt, und diese Wahl ist die halbe Miete. Silentiums Peak-Detektor (ein schneller Ballistics-Follower, ~0,3 ms Attack) reagiert auf einzelne transiente Spitzen — gut, um jeden schnellen Pick-Anschlag zu fangen, aber er öffnet auch bei einem einzelnen isolierten Klick, den ein Mensch nicht „Signal" nennen würde. Die RMS-Option läuft stattdessen mit einem 5-ms-One-Pole-Mittelwert — strukturell blind für isolierte Spitzen: Bei Programmmaterial mit gelegentlichen Klicks über einem ruhigen Bett triggert Peak dutzende Male pro Sekunde, wo RMS gar nicht öffnet. Keins von beiden ist „richtiger" — Peak passt zu schnellem, perkussivem Material, bei dem jede Attacke erfasst werden soll; RMS passt zu anhaltendem oder verrauschtem Material, bei dem das Gate dem *Körper* des Signals folgen soll, nicht seiner Textur. Dieselbe Logik gilt für die Flankensteilheit des Sidechain-Filters (12 vs. 24 dB/Okt): Eine steilere Flanke grenzt enger ein, was der Detektor „hört" — wichtig, wenn du von einem externen Sidechain (Kick, Click-Track) triggerst statt von der Gitarre selbst.

**Rezept — Drop-Tuned-Rhythmus-Chug.** Silentium mit schnellem Attack und 0 ms Smooth Open (die *Chug-Lock*-Region), Ratio Richtung Gate-Ende, Peak-Detection (nicht RMS, um die Transiente zu fangen) in Overtures Tight-Regler, hochgezogen Richtung 200+ Hz (die *Drop-Tune-Tight*-Preset-Region — Tight 220 Hz, Drive um 4 dB, Bite 80 %) vor Tenebrae. Das hohe Tight-Setting entfernt Low End, bevor Tenebraes eigene Gain-Stufe die Chance hat, es auf einer tiefgestimmten Saite zu Matsch zu sättigen.

## Bass: Crypta

Crypta ist die bassspezifische Voicing-Stufe, und ihre Platzierung ist eng und bewusst: **DI/Amp-Sim → Crypta → Bus-Kompression/Glue → Mix-Bus**. Es erwartet ein bereits einigermaßen sauberes, DI'tes oder amp-simuliertes Bass-Signal — es ist selbst kein vollständiger Amp-Sim.

Der Grund, warum es ein Drei-Band-Tool ist statt eines einzelnen Full-Range-Sättigers: Eine Wand aus verzerrten Gitarren und ein Bass kämpfen um überlappendes Frequenzterritorium, und eine Single-Band-Behandlung kann Low End und „durch die Wand schneidenden" oberen Mitten-Content nicht gleichzeitig bedienen, ohne einen davon zu kompromittieren. Cryptas Low Band fährt einen Parallel-Kompressor, dessen Job es ist, den Grundton-/Sub-Content *unter* der Gitarrenwand fest verankert zu halten, während Mid- und High-Band jeweils einen eigenen, unterschiedlichen Sättigungscharakter bekommen — der „Throat" des Mid-Bands liegt bewusst genau in dem Frequenzbereich, der am ehesten mit Gitarren kollidiert, also verdient er eine bewusste Entscheidung, keinen Standard-Reflex.

> **Theorie — warum den Drive überhaupt nach Band splitten.** Ein einzelner Full-Range-Sättiger fügt Harmonische über das gesamte Spektrum gleichzeitig hinzu: Drehst du ihn hoch genug für brauchbares „Grind" in den oberen Mitten, sättigt das Low End gleich mit — meistens das Gegenteil von dem, was ein Bass unter einer dichten Gitarrenwand braucht (ein solides, unverzerrtes Low End *und* ein Register, das oben durchschneidet). Das Signal zuerst nach Bändern zu splitten bedeutet, dass die Nichtlinearität jedes Bands nur auf den Harmonischen-Content wirkt, den dieses Band tatsächlich enthält — das Low Band kann sauber und komprimiert bleiben, während das High Band unabhängig davon hart für Grind angeschoben wird.

## Busse: Aureate und Triptych

Beide sind Glue-Stufen, aber an unterschiedlichen Punkten und aus unterschiedlichen Gründen.

**Aureate** läuft *nach* dem Balancing der einzelnen Layer eines orchestralen/Chor-Stacks (oder einer Gitarren-Doublierung) — ein String- oder Brass-Bus, ein orchestraler/Chor-Submix, oder (sparsam eingesetzt) der volle Mix-Bus als finaler „Konsolen-Glue"-Pass. Es ist kein Distortion- oder Amp-Sim-Tool: Drive ist moderat gedeckelt, und die Default-Warmth-/Character-Settings bleiben innerhalb von „fügt Wärme hinzu", nicht „fügt Dreck hinzu". Die Theorie dahinter, warum sich der Glue je nach gewähltem Schaltungs-Law unterschiedlich verhält, steht in Aureates eigenem Guide.

**Triptych** ist ein Mastering-/Mix-Bus-Multiband-Dynamics-Tool, kein Effekt pro Instrument. Greif danach, wenn ein Single-Band-Kompressor entweder das Low End überkomprimiert, um High-Frequency-Peaks zu kontrollieren, oder das Low End locker lässt, während die Höhen schon gezähmt sind — das klassische Symphonic-Metal-Problem einer dichten Wand aus Gitarren, Orchester-Hits und Chor, die alle um denselben Headroom kämpfen. Es funktioniert genauso gut als Glue auf einem Drum-Bus oder einem vollen Gitarren-Stack, unabhängig von der Gesamtmischung.

Eine übliche Paarung auf einem dichten orchestralen/Gitarren-Mix-Bus: **erst Aureate** (sanfte Sättigungs-Glue, niedriger Mix), **danach Triptych** (Multiband-Kontrolle dort, wo Frequenzbereiche wirklich gegeneinander arbeiten), bevor das Signal den Master-Limiter erreicht.

## Vocals und Chor: Miserere, Seraph, Lancet

Diese drei decken unterschiedliche Aufgaben ab und schichten sich natürlich übereinander, aber zwei von ihnen können sich gegenseitig ins Gehege kommen, wenn du nicht bewusst vorgehst.

**Lancet** ist korrektiv und chirurgisch — es gehört früh bis mittig in die Kette, vor breites Tonal-Shaping, um eine bestimmte Resonanz- oder Härte-Band zu beheben, ohne alles darunter dauerhaft einzufärben. Setz es *vor* die charaktergebenden Stufen unten ein, nicht danach: Ein Problem zu beheben, nachdem es schon in einen gesättigten Bus eingeklebt wurde, ist deutlich schwerer sauber hinzubekommen.

**Miserere** ist ein paralleler Vocal-Channel: ein trockener „Direct"-Pfad (jede Sektion standardmäßig aus, sodass das Vocal von Haus aus quasi unangetastet durchläuft) plus vier parallele Return-Busse (ein FET-artiger Limiter, ein Sandwich aus passivem EQ und opto-artigem Leveler, ein Micro-Pitch-Spread und ein kurzer tape-artiger Slap-Back), jeweils unter dem trockenen Signal auf moderatem Pegel zugemischt. Es fungiert als *der Channel selbst* für ein Lead-Vocal, nicht als Insert obendrauf auf einem anderen Channel-Strip, der dieselbe Aufgabe schon erledigt.

**Seraph** deckt De-Essing, ein Air-Shelf, sanfte Glue-Kompression ab und — der Hauptunterschied zu Miserere — einen Doubler mit drei unterschiedlichen Engines (Constant-Ratio-Micropitch, ein Phasenvocoder-Shift und ein klassischer Doubled-Voice-Modus), nützlich überall dort, wo Miseres Parallel-Return-Charakter nicht das ist, was gebraucht wird, besonders bei Chor-Spread.

> **Vorsicht vor Doppelverarbeitung.** Sowohl Miseres Direct-Pfad als auch Seraph enthalten einen De-Esser. Beide gleichzeitig mit aktivem De-Essing laufen zu lassen, verdoppelt die Sibilanz-Behandlung ohne Nutzen — leg fest, welche Stufe das De-Essing übernimmt (meist die, die früher in der Kette sitzt), und lass den De-Esser der anderen aus.

**Vorschlag für ein Lead-Vocal:** Lancet (das eine Resonanzproblem beheben) → Miserere (der Channel, paralleler Charakter obendrauf) → Seraph, nur falls Air oder ein Doubler-Pass gebraucht wird, den Miserere nicht bietet → Reverb-/Delay-Send (Requiem).

**Vorschlag für einen Chor-Bus:** Lancet nur, falls eine bestimmte aufgenommene Frequenz über den ganzen Chor hinweg gezähmt werden muss → Seraph mit stärkerer Doubler-Breite und weiterem Spread-Setting für ein volleres Chorgefühl aus weniger aufgenommenen Takes → Aureate für Sektions-Glue → Firmament/Requiem für Breite und Raum.

Miseres Engines sind explizit **forschungsbasiert abgeleitet, nicht gegen echte Hardware-Einheiten gemessen** (das steht direkt so in der eigenen Anleitung) — nützliche, musikalisch motivierte Schaltungsmodelle, kein Anspruch, den Klang eines bestimmten physischen Geräts zu treffen. Behandle die Presets als mechanisch akkurate Ausgangspunkte, die du nach Gehör justierst, genau wie bei jedem anderen Plugin — nicht als Ersatz für ein bestimmtes Stück Hardware.

## Raum: Requiem und Firmament

**Requiem** ist für die „kinematische" Ebene gebaut — Orchester, Chor, Pads, Ambience — getrennt von der „aggressiven" Ebene (Rhythmusgitarren, Drums, Bass), damit jede unabhängig platziert werden kann. Ein String-/Orchester-Bus will einen moderaten Mix mit Pre-Delay, das die Klarheit schneller Passagen erhält; ein Chor-Bus will typischerweise mehr Reverb und einen längeren Decay, um kathedralengroß zu wirken. Es wird *nicht* generell direkt auf verzerrten Rhythmusgitarren oder Kick/Snare empfohlen — der Hall-/Kathedralen-Charakter wirkt auf schnellem, perkussivem, verzerrtem Material wie Matsch; ein kurzer, plattenartiger Reverb (oder gar keiner) dient dort meist besser.

**Firmament** sitzt eher am Ende einer Channel- oder Bus-Kette, nachdem Tone-Shaping und Dynamics schon entschieden sind — Breite ist eine *Gefühlsentscheidung*, getroffen, sobald der Ton steht, kein Ersatz dafür. Typische Platzierungen: String-/Chor-/Pad-Busse (der Hauptanwendungsfall), ein sanfter Touch auf einem doublierten Rhythmusgitarren-Bus, um zwei gepannte Doubles zu einer breiteren Wand zu verkleben, und — sparsam eingesetzt — der Master-Bus, wo Bass Mono die Kick-/Bass-/Low-Gitarren-Energie zentriert hält, während Becken/Strings/Reverb-Tails oberhalb der Crossover so breit bleiben, wie die Mischung sie schon gemacht hat.

> **Theorie — warum Velvet-Noise-Dekorrelation mono-kompatibel bleibt.** Ein Stereobild zu verbreitern bedeutet meist, die Kanäle asymmetrisch zu behandeln — eine Seite verzögern (Haas-Effekt) oder ein Allpass-Netzwerk nur auf einem Kanal laufen lassen. Faltet man das auf mono zusammen, können sich die beiden Kanäle teilweise auslöschen: manche Frequenzen fallen zweistellig in dB. Firmaments Velvet-Noise-Modi vermeiden das strukturell statt durch sorgfältiges Tuning: Das Plugin synthetisiert und skaliert ausschließlich das *Side*-Signal eines Mid/Side-Splits und rührt Mid nie an. Da ein Mono-Downmix mathematisch immer `Mid + Mid` ist, egal was Side enthält, kann keine Width-Einstellung je ändern, was ein Mono-Hörer hört — die Garantie gilt konstruktionsbedingt, nicht weil die Dekorrelations-Koeffizienten zufällig richtig getunt wurden.

Mono-Kompatibilität ist kein akademisches Anliegen bei einer Heavy-Music-Mischung mit orchestralen Elementen: PA-Systeme, Broadcast und ein relevanter Anteil der Hörer über Handy-Lautsprecher falten irgendwo im Signalweg auf Mono, und eine Mischung, die dabei ihr Low End oder ihre Chor-Breite verliert, klingt genau dort dünn, wo sie am größten klingen soll.

## Master: Apotheosis

Apotheosis gehört ganz ans Ende des Master-Busses, nachdem jeder andere Prozessor — EQ, Bus-Kompression, Sättigung, Triptych, falls verwendet — seine Arbeit schon erledigt hat. Es ist nicht für einzelne Spuren gedacht; es ist das finale Sicherheitsnetz und die Loudness-Stufe vor dem Export.

> **Theorie — warum True Peak nicht dieselbe Zahl ist wie der Sample-Peak.** Eine digitale Audiodatei speichert nur diskrete Samples, aber die analoge Wellenform, die ein D/A-Wandler (oder der Decoder eines verlustbehafteten Codecs) daraus rekonstruiert, kann *zwischen* Samples höher ausschlagen, als jeder einzelne Sample-Wert zeigt. Ein Limiter, der rein im Sample-Bereich arbeitet, kann ein Signal durchlassen, das auf einem gewöhnlichen Peak-Meter „sicher" misst, aber nach der Wandlung ins Analoge oder nach dem Transcoding in ein verlustbehaftetes Streaming-Format clippt. Apotheosis' True-Peak-Detection läuft innerhalb einer oversampleten Domäne (4x/8x/16x), genau damit sie diesen rekonstruierten Peak sehen — und eine Ceiling dagegen halten — kann, nicht nur die gespeicherten Samples.

Praktische Mastering-Zielwerte, als Ausgangspunkte: Ein **streaming-taugliches Master** zielt typischerweise auf einen Integrated-LUFS-Wert (die standardisierte, wahrnehmungsgewichtete Loudness-Messung, die Apotheosis' Metering direkt implementiert) um −14 LUFS, mit True Peak bei oder unter −1 dBTP, da die meisten Streaming-Plattformen ohnehin auf einen Ziel-Loudness-Wert normalisieren — lauter zu gehen kostet meist nur Dynamikumfang, ohne hörbar lauter zu wirken, sobald die Plattform wieder runterregelt. Ein **Club- oder physisches Master** zielt üblicher auf −9 bis −6 LUFS Integrated, mit True Peak weiterhin sicher unter 0 dBTP (üblich −0,3 bis −1 dBTP, mit Spielraum für spätere Codec-Wandlung). Keine der Zahlen ist Gesetz — Genre, Plattform und dein eigenes Gehör entscheiden —, aber sie sind ein vernünftiger Ausgangsrahmen statt Blindraten. Die konkreten Style-/Oversampling-Settings dahinter stehen in Apotheosis' eigenem Guide.

## Häufige Fehler entlang der Kette

- **Standardmäßig nach der Distortion gaten**, ohne zu fragen, ob das bekämpfte Rauschen dort überhaupt entsteht. Gate das saubere DI-Signal, außer die Rauschquelle ist speziell die Amp-/Cab-Stufe.
- **Sowohl Miseres als auch Seraphs De-Esser** auf demselben Vocal laufen lassen — entscheide dich für einen.
- **Loudness am Master allein mit Apotheosis jagen**, statt Gain-Staging und Glue früher in der Kette zu erledigen — ein Limiter, der ausbügelt, was Balance weiter oben hätte regeln sollen, klingt eher gequetscht als laut.
- **True Peak mit Sample-Peak verwechseln**, wenn du Headroom prüfst — ein Track, der auf einem simplen Peak-Meter „sicher misst", kann nach Format-Konvertierung trotzdem clippen, wenn True Peak nie geprüft wurde.
- **Verbreitern, bevor der Mono-Downmix geprüft wurde**, besonders bei orchestralem/Chor-Material, das sich eine Mischung mit Gitarren teilt, die über eine PA druckvoll bleiben müssen. Firmaments Mono-Audition-Modus existiert genau für diese Prüfung.
- **Reverb standardmäßig auf verzerrten Rhythmusgitarren** — ein kathedralengroßer Reverb wirkt auf schnellem, perkussivem, schon verzerrtem Material wie Matsch; greif dort eher zu etwas Kürzerem oder gar nichts.

## Guides für einzelne Plugins

- [Overture](../overture/guide/index.html) — Tight-Boost für Gitarre
- [Tenebrae](../tenebrae/guide/index.html) — High-Gain-Distortion
- [Nave](../nave/guide/index.html) — Cabinet-IR-Loader
