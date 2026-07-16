<!-- German translation of requiem.en.md (English source generated from requiem/docs/manual.md on 2026-07-16) — do not hand-edit; re-translate after the English manual is resynced. -->

<p align="center"><img src="assets/icon.png" alt="Requiem-Icon" width="120"/></p>

# Requiem — Bedienungsanleitung

*Eine Kathedrale in der Box – cineastischer Convolution-Reverb für orchestralen und chorischen Raum.*

## Was Requiem ist

Requiem ist ein Convolution-Reverb, der gezielt für die orchestrale/chorische Ebene eines Heavy-Music-Mixes entwickelt wurde – Streicher, Chor, Pads, Ambient-Texturen – statt als Allzweck-Reverb für jede beliebige Quelle. Er erzeugt seine Impulsantwort prozedural (keine mitgelieferte Sample-Library, die lizenziert oder verwaltet werden muss), geformt durch Regler, die auf musikalisch sinnvolle Entscheidungen abbilden: wie groß der Raum ist, wie hell oder dunkel der Tail klingt, wie ausgeprägt ein deutlicher früher "Slap" gegenüber einer glatten, homogenen Klangfläche ist, und ob er endlos aushalten statt abklingen soll. Du kannst außerdem eine eigene, aufgenommene Impulsantwort laden (eine echte Kathedrale, Halle, Plate oder irgendetwas anderes im WAV-/AIFF-Format o. Ä.), wenn du stattdessen einen bestimmten, nicht-prozeduralen Raum möchtest.

## Wo es in einer Heavy-Music-Produktionskette sitzt

Heavy-Music-Produktionen mit orchestralen Elementen trennen die "aggressive" Ebene (Rhythmusgitarren, Drums, Bass) typischerweise von der "cineastischen" Ebene (Orchester, Chor, Pads, Ambience), damit jede unabhängig bearbeitet und im Mix platziert werden kann. Requiem ist für die zweite Ebene gedacht:

- **Streicher-/Orchester-Bus**: Ein Hall- oder Cathedral-Raum mit moderatem Mix (30–50 %) gibt der orchestralen Ebene Raum zum Atmen, ohne rhythmische Details zu verschmieren. Nutze Pre-Delay, um schnelle Passagen (Spiccato, Tremolo-Streicher) verständlich zu halten – ein kleiner Abstand, bevor der Tail einsetzt, bewahrt die Klarheit des Attacks.
- **Chor-Bus**: Chor verlangt tendenziell mehr Reverb als Instrumente, um "kathedralengroß" zu klingen – probiere den Cathedral-Raum, einen längeren Decay und einen höheren Mix als bei Streichern. Ein leicht heruntergezogenes Damping (ein dunklerer Tail) verhindert, dass sich Zischlaute/Atemgeräusche in der Klangfläche aufbauen.
- **Ambient-Pads/Übergänge**: Dafür ist Freeze gemacht – halte einen Akkord, aktiviere Freeze, und lass die eingefrorene Textur unter einem Übergang oder Breakdown aushalten, ohne ein separates Pad-Instrument zu benötigen.
- **Nicht direkt empfohlen für**: verzerrte Rhythmusgitarren oder Kick/Snare – ein kurzer Plate-artiger Reverb oder gar keiner dient diesen meist besser; der Cathedral-/Hall-Charakter von Requiem liest sich auf schnellen, perkussiven, verzerrten Quellen als Matsch. Falls du dennoch Ambience auf Gitarren willst, halte Mix niedrig (10–20 %) und Decay kurz.

Eine typische Insert-Reihenfolge auf einem Orchester-/Chor-Bus: EQ -> Kompression -> **Requiem** -> Limiter (falls als letzte Stufe auf diesem Bus verwendet). Requiem meldet dem Host seine eigene (normalerweise null) Verarbeitungslatenz und bleibt dadurch sample-genau zeitsynchron zu parallelen Dry-Bussen, wenn du es stattdessen über einen Aux/Send statt als Insert einblendest.

## Signalfluss

```
input -> Pre-Delay -> Convolution (procedural or user IR) -> Modulation (chorus, wet only)
      -> Width (M/S, wet only) -> Dry/Wet Mix (latency-compensated) -> Output -> output
```

Decay, Damping, Space, Early/Late Balance und Freeze formen die Impulsantwort selbst (im Hintergrund neu generiert, nicht bei jedem Sample); Pre-Delay, Modulation, Width, Mix und Output bestimmen, wie diese Impulsantwort in Echtzeit auf dein Signal angewendet wird. Die vollständige technische Erklärung, warum das so aufgeteilt ist, findest du in [`docs/architecture.md`](architecture.md).

## Parameterübersicht

### Decay
**Bereich:** 0.1 – 10.0 s · **Standard:** 2.5 s

Wie lange der Reverb-Tail zum Abklingen braucht (RT60-artig: der Punkt, an dem er um 60 dB abgefallen ist). Kurze Werte (0.3–0.8 s) eignen sich für enge Räume/Ambience; 1.5–3 s für einen Konzertsaal; 4–10 s ist Kathedralen-/Höhlen-Territorium oder nützliches Rohmaterial für Freeze. Decay bestimmt außerdem die Länge der generierten Impulsantwort, weshalb sehr lange Decay-Werte mehr CPU kosten (der Convolution-Kernel wird proportional größer).

### Pre-Delay
**Bereich:** 0 – 250 ms · **Standard:** 20 ms

Der Abstand zwischen dem Dry-Sound und dem Einsatz des Reverb-Tails. Eine kleine Menge (10–30 ms) reicht meist aus, um das Gefühl zu erhalten, "dieser Reverb ist vom Direktsignal getrennt", ohne wie ein eigenständiger Slapback zu klingen. Größere Werte (60–150 ms) helfen, schnelles rhythmisches Material (palm-gemutete Gitarren unter dem Orchester, Staccato-Streicher) knackig und verständlich zu halten, während der Tail erst danach aufblüht – das Ohr hört den Attack klar, bevor die Klangfläche einsetzt.

### Damping
**Bereich:** 500 – 20000 Hz · **Standard:** 8000 Hz

Die Höhenabsenkung, die auf den Reverb-Tail angewendet wird. Niedrigere Werte erzeugen einen dunkleren, "gedämpfteren" Tail (schwere Teppiche/Vorhänge, oder einfach ein stumpfer klingender Raum); höhere Werte erzeugen einen helleren, "hart-oberflächigeren" Tail (Stein, Glas). Bei Chor und Streichern liest sich ein leicht abgesenktes Damping gegenüber dem Standard oft natürlicher und über einen langen Mix hinweg weniger ermüdend, besonders wenn die Dry-Quelle bereits hell klingt.

### Space
**Auswahl:** Cathedral / Hall / Chamber · **Standard:** Hall

Formt den Charakter der frühen Reflexionen, die vor dem diffusen Tail liegen (siehe Early/Late Balance unten) – das ist es, was tatsächlich den Unterschied macht zwischen "das klingt wie eine Kathedrale" und "das klingt wie eine kleine Kammer", unabhängig von Decay/Damping:

- **Cathedral**: lange, dichte, weit gestreute frühe Reflexionen – der Klang eines großen Steinraums mit vielen nahen Flächen. Passt gut zu langem Decay und Chor.
- **Hall**: ein ausgewogenes, moderates Reflexionsmuster – der Allzweck-Standard, gut für Streicher und Orchester.
- **Chamber**: kurze, spärliche, eng gestaffelte Reflexionen – ein kleiner, intimer Raum. Gut für ein subtileres Gefühl von "das wurde in einem Raum gespielt", ohne einen offensichtlich großen Reverb.

### Early/Late Balance
**Bereich:** 0 – 100 % · **Standard:** 80 %

Blendet zwischen der Early-Reflection-Ebene (0 %, geformt durch Space) und dem diffusen Late-Tail (100 %, geformt durch Decay/Damping) über. Bei 0 % hörst du überwiegend die diskreten frühen Reflexionen – ein kurzer, direkter Charakter, näher an einem Slapback oder der "Lebendigkeit" eines kleinen Raums als an einer Klangfläche. Bei 100 % hörst du eine reine, glatte diffuse Fläche ohne eigenständigen Früh-Charakter. Der Standard (80 %) hält den diffusen Tail dominant, gibt der frühen Ebene aber noch etwas Präsenz – senke den Wert, wenn der Charakter der Space-Einstellung hörbarer sein soll, erhöhe ihn Richtung 100 % für das glatteste, cineastischste Ergebnis.

### Modulation
**Bereich:** 0 – 100 % · **Standard:** 0 %

Fügt dem Reverb-Tail eine subtile, langsame, Chorus-artige Bewegung hinzu – niemals dem Dry-Signal. Prozedural generierte Impulsantworten können gelegentlich etwas statisch oder metallisch klingen im Vergleich zu einem echten aufgenommenen Raum; eine kleine Menge Modulation (10–30 %) mildert das, ohne als offensichtlicher Chorus-/Vibrato-Effekt hörbar zu sein. Bei 0 % ist die Modulation-Stufe vollständig bypassed (identischer Output, als gäbe es sie gar nicht) – es ist unbedenklich, sie auf Standard zu lassen, sofern du nicht gezielt diese zusätzliche Bewegung willst.

### Freeze
**Off / On** · **Standard:** off

Wenn aktiviert, hält der Reverb-Tail seinen aktuellen spektralen Inhalt aus, statt abzuklingen – nützlich, um einen Akkord oder eine Textur unter einem Übergang, Breakdown oder Ambient-Abschnitt zu halten, ohne ein separates Pad-/Drone-Instrument zu benötigen. Freeze ist Convolution-basiert, daher ist das Aushalten durch die Decay-Einstellung begrenzt (bis zu 10 s), nicht buchstäblich unendlich – stell es dir eher als "halte diesen Schnappschuss des Tails für bis zu Decay Sekunden" vor statt als Feedback-Loop-artiges unendliches Freeze. Damping beeinflusst weiterhin die Helligkeit der eingefrorenen Textur, während sie aktiv ist; Early/Late Balance und die Early-Reflection-Ebene werden im eingefrorenen Zustand ignoriert (ein eingefrorener Tail ist immer die volle diffuse Fläche).

**Tipp:** Für einen sauberen Freeze-Moment aktiviere Freeze auf einem gehaltenen Akkord (nicht mitten in einem Transienten) und erhöhe eventuell zuerst Decay, da dieser Wert bestimmt, wie lang der eingefrorene Kernel tatsächlich ist.

### Width
**Bereich:** 0 – 200 % · **Standard:** 100 %

Stereobreite ausschließlich des Wet-(Reverb-)Signals, per Mid/Side-Skalierung – die Breite des Dry-Signals wird nie angetastet. 0 % kollabiert das Wet-Signal auf Mono; 100 % ist das natürliche Stereobild der Convolution-Engine; bis zu 200 % übertreibt es weiter für einen besonders breiten, umhüllenden Tail. Sehr breite Einstellungen (150–200 %) können isoliert beeindruckend klingen, aber Phasen-/Mono-Kompatibilitätsprobleme verursachen – prüfe deinen Mix in Mono, wenn du Width hoch aufdrehst.

### Mix
**Bereich:** 0 – 100 % · **Standard:** 35 %

Dry/Wet-Balance. Bei 0 % ist Requiem ein transparenter (latenzkompensierter) Durchlauf des Inputs – nützlich zum A/B-Vergleich des Dry-Signals, ohne das Plugin zu entfernen, oder wenn du Requiem auf einem Send-/Aux-Bus einsetzt und es auf Plugin-Ebene voll wet haben willst, um die Mischung stattdessen über die Send-Menge zu steuern. Der Standard (35 %) eignet sich für den typischen Insert-Einsatz auf einem Orchester-/Chor-Bus; höher für ein ambienteres, verwascheneres Ergebnis, oder 100 % auf einem dedizierten Reverb-Return-Bus.

### Output
**Bereich:** -24 – 24 dB · **Standard:** 0 dB

Trim, der nach dem Dry/Wet-Mix angewendet wird – nutze ihn, um den Output-Pegel des Plugins ins Gain-Staging einzupassen (z. B. nach deutlichem Erhöhen von Mix, oder um Pegel beim A/B-Vergleich verschiedener Decay-/Space-Einstellungen anzugleichen), ohne danach ein separates Gain-Plugin zu benötigen.

## Eine eigene Impulsantwort laden

Nutze **Load IR...** im Editor, um den prozeduralen Generator durch eine eigene aufgenommene Impulsantwort (WAV/AIFF) zu ersetzen. Solange eine eigene IR geladen ist, wirken sich Decay/Damping/Space/Early/Late Balance/Freeze nicht mehr auf den Klang aus (die geladene IR wird unverändert verwendet); **Clear IR** kehrt zum prozeduralen Generator zurück und übernimmt dabei die aktuellen Einstellungen dieser Regler. Der Dateipfad der geladenen IR wird mit deiner Session/deinem Preset gespeichert; falls die Datei beim erneuten Öffnen der Session verschoben oder gelöscht wurde, fällt Requiem auf den prozeduralen Generator zurück, statt das Laden fehlschlagen zu lassen.

Requiem validiert die Datei vor dem Laden (verwirft alles, was nicht als Audio gelesen werden kann, sowie jede Datei länger als 30 Sekunden – echte aufgenommene Impulsantworten sind so gut wie nie so lang, und das schützt davor, versehentlich einen ganzen Song/Mix statt einer echten IR auszuwählen).

## Tipps

- **Schnelles/rhythmisches Material unter einer orchestralen Klangfläche**: Erhöhe Pre-Delay, bevor du zu einem kürzeren Decay greifst – das bewahrt meist die Klarheit besser, während das Raumgefühl insgesamt erhalten bleibt.
- **Chor klingt hart/zischend im Tail**: Senke Damping um ein paar tausend Hz, bevor du zu einem EQ auf dem Reverb-Return greifst.
- **"Dieser Reverb klingt etwas statisch/synthetisch"**: Probiere Modulation um 15–25 %, bevor du davon ausgehst, einen anderen Reverb zu brauchen.
- **Ein Pad/Drone aus einer vorhandenen Spur bauen**: Automatisiere Freeze auf on, fahre Mix hoch und erwäge einen Hauch Width und Modulation für Bewegung, während es aushält.
- **Mono-Kompatibilitäts-Check**: Summiere regelmäßig auf Mono, wenn du Width über ~150 % fährst, besonders auf einem Bus, der später auf Mono gefaltet werden könnte (Broadcast, manche Streaming-Plattformen).
