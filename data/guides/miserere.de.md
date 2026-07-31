# Miserere — Praxis-Guide

*Praxisnahe Einstellungen für den parallelen Vocal-Channel, verankert in den Werkspresets.*

## Wo es hingehört

Miserere verpackt ein dokumentiertes Parallel-Vocal-Processing-Template — einen trockenen Direct-Pfad plus vier parallele Return-Busse (CRUSH, SANDWICH, SPREAD, SLAP) — in einen einzigen Channel-Strip:

```
Vocal-/Chor-Aufnahme → Miserere → Reverb-/Delay-Send → Mix-Bus
```

Der Direct-Pfad ist standardmäßig ein Draht: Jede optionale Sektion darauf (De-Ess Pre, FET Comp, Console EQ, Sat, De-Ess Post) ist von Haus aus aus, sodass das trockene Vocal quasi unangetastet durchläuft — sein natürliches Envelope und Phrasing bleiben erhalten. Alles andere schichtet sich *darunter* über die vier Return-Busse, Kopien des Direct-Pfad-Outputs, hart prozessiert und moderat zugemischt. Fungiert für ein Lead-Vocal als der Channel selbst, nicht als Insert obendrauf auf einem anderen Channel-Strip, der dieselbe Aufgabe schon erledigt.

## Quick-Start-Einstellungen

### Start-Template — *Gentle Bus*

Crush Input 8, Ratio 4:1, Style Gentle (sanftes 2:1-Voicing), Level −7 dB. SANDWICH Peak Reduction 40 %, standardmäßig gemutet. SPREAD/SLAP auf ihren Standardwerten −18/−15 dB, standardmäßig gemutet.

Das ist der eigene empfohlene Ausgangspunkt des Plugins: Erst CRUSH hochziehen mit aktiviertem Audition (soll solo „schrecklich" klingen und im Blend gut), dann SANDWICH/SPREAD/SLAP nacheinander nur bei Bedarf entmuten, jeweils gegen den „man merkt es nur, wenn man es muted"-Test geprüft.

### Lead-Vocal, präsent und vorne — *Crush Forward*, *Aggressive Rock Vocal*

Crush Forward: **Input 24, Ratio 3:1**, Level −4 dB (vergleichsweise heiß in der Mischung), alles andere gemutet.
Aggressive Rock Vocal: Direct-Pfad aktiviert (De-Ess Pre/Post an, **FET Comp an** bei Threshold −24 dB/Attack 3 ms, **Console EQ Drive 10, Sat Drive 8**), Crush Input 30, Level −6 dB, Spread Width 90 %.

Aggressive Rock Vocal ist das Preset, das die optionalen Sektionen des Direct-Pfads tatsächlich aktiviert — FET Comp für leichte Insert-Kompression, EQ Drive und Sat für Transformer-/Tape-artigen harmonischen Content auf dem Channel selbst, zusätzlich zu hart angeschobenem CRUSH darunter.

### Backing-Vocal-/Chor-Stack — *Whisper Thicken*, *Wide & Wet*

Whisper Thicken: Direct De-Ess Pre an, Crush Style Gentle bei Level −14 dB (leicht), **Spread Detune 10/Width 90 %, Level −14 dB**, Slap Level −13 dB — alle vier Busse aktiv, aber jeweils zurückhaltend.
Wide & Wet: **Spread Width 100 %**, Slap Stereo an (unabhängige L/R-Delays statt Mono-Return), Slap Level −9 dB (vergleichsweise präsent).

Für einen Backing-/Chor-Stack leisten Spreads Breite und Detune mehr Arbeit als CRUSH — ein breiterer, präsenterer Pitch-Spread-Return füllt eine kleinere Anzahl aufgenommener Takes zu etwas, das wie ein volleres Stack wirkt, wo ein Lead-Vocal meist möchte, dass CRUSH mehr Arbeit leistet und SPREAD unterschwellig bleibt.

### Nur-Direct-Pfad-Insert — *Direct Channel Only*

De-Ess Pre/FET Comp/EQ (HPF an, Low +2 dB, Mid −2 dB, High +2 dB, Drive 6) alle auf dem Direct-Pfad aktiviert; **alle vier Return-Busse gemutet**.

Nützlich, wenn Miseres Channel-Strip-Processing (De-Ess, leichte Kompression, Console EQ, Sättigung) ohne die parallelen Charakter-Busse gewollt ist — eine legitime, unterstützte Konfiguration, kein halbfertiges Setup.

### Abgenutzter Tape-Slap — *Worn Slap*, *Tape Slap 7.5*

Worn Slap: Slap Time 140 ms, Tone 80 %, **Wobble 60 %, Age 75 %** — alles andere gemutet.
Tape Slap 7.5: Slap Time 120 ms, Tone 35 %, Wobble 25 %, Age 15 % (vergleichsweise zurückhaltend).

Wobble und Age sind bei 0 % beide wirklich aus (nicht nur runtergedreht) — bewusst zu ihnen greifen, wenn das Ziel speziell „das ist durch ein physisches Tape-Delay gelaufen" ist, nicht als Standard-Einfärbung bei jedem SLAP-Einsatz.

## Rezepte

1. **Lead-Vocal in einer dichten Mischung.** Bei Gentle Bus starten, CRUSHs Input mit aktiviertem Audition hochziehen, bis in Isolation eine schwere, offensichtlich „falsche" Kompression zu hören ist, dann dem Return-Fader vertrauen und im Kontext nach Gehör anpassen. *Warum:* CRUSH hat keinen Threshold-Regler — Input treibt das Signal in einen festen Per-Ratio-Threshold —, und der Bus soll solo bewusst schlecht klingen; ihn in Isolation zu beurteilen (statt über Audition gegen die volle Mischung) ist schlicht der falsche Test.

2. **Backing-Vocal-Stack aus wenigen Takes.** Whisper Thicken als Basis, Spread Width Richtung 90–100 %, Spread Detune um 8–10 Cent. *Warum:* SPREADs zwei Delay-Taps sind hart L/R gepannt mit einem kleinen Pitch-Offset — es zu verbreitern lässt das Ohr eher mehrere Takes als breiteren Stack lesen, ohne das diskrete Chorus-Artefakt, das ein größerer Detune einführen würde (6 Cent sind bewusst klein, damit der Effekt als „nach außen geschoben" wirkt, nicht als Chorus).

3. **Zwischen CRUSHs All-Buttons- und Gentle-Style entscheiden.** Zu **Gentle** greifen (ein festes 2:1-Voicing) bei Material, das Zurückhaltung braucht, oder ein leiseres Vocal, das nicht aggressiv gequetscht wirken soll; zu **All-Buttons** (der Default) greifen für den „Snap" — eine plateauförmige Kurve mit bewusstem Give-Back und kurzem Attack-Lag, der Transienten durchschlagen lässt, bevor geklemmt wird. *Warum:* Das sind wirklich unterschiedliche Kurven, nicht zwei Intensitäten derselben — All-Buttons' Überschwing-dann-Einpendeln ist das, was CRUSH seinen charakteristischen Vorwärtsschub gibt, wo Gentle näher an einem konventionellen, vorhersagbaren Kompressor liegt.

4. **SANDWICHs Emphasis für einen de-essing-nahen Effekt nutzen.** **Emphasis** Richtung 100 % ziehen, wenn SANDWICHs Leveler auf den falschen Content reagiert (Atem, Low-Mid-Körper) statt auf Presence/Sibilanz. *Warum:* Emphasis macht den Detektor zunehmend HF-selektiver — bis zu 10 dB weniger LF-Empfindlichkeit —, sodass der Leveler bei hohen Settings hauptsächlich auf den Top-End reagiert, „wie ein Multiband"-Kompressor, statt von dem angetrieben zu werden, was über das gesamte Spektrum am lautesten ist.

5. **Die gesamte Parallel-Ebene bei leiserem, organischerem Material zurücknehmen.** **Parallel** nutzen (der Makro-Trim, −24 bis +6 dB) statt alle vier Return-Fader einzeln runterzuziehen. *Warum:* Parallel versetzt alle vier Busse in einer Geste gemeinsam — der „VCA-Ride-back"-Move für eine Sektion, die die Parallel-Ebene bei lauteren Passagen präsent braucht, bei leiseren aber zurückgenommen, ohne jedes Mal die relativen Pegel der Busse zueinander neu auszubalancieren.

> **Theorie — was ein photozellenmodellierter Leveler tatsächlich ändert.** SANDWICHs Opto Leveler hat keinen Ratio-Regler, und das ist kein fehlendes Feature — es ist eine direkte Konsequenz dessen, was er modelliert. Ein echter optischer Leveler funktioniert, indem eine Lichtquelle vom Audiosignal angesteuert wird und das resultierende Lichtlevel über eine Photozelle zurückgelesen wird, deren Widerstand sich mit der Belichtung ändert; es gibt in dieser Kette nirgends ein festes Ratio, nur eine nichtlineare Beziehung zwischen der Lichtmenge, die die Zelle trifft, und wie schnell/langsam ihr Widerstand reagiert. Deshalb ist der Release des Levelers natürlicherweise zweistufig (eine schnelle erste Erholung, dann ein langer Tail), und deshalb hat er echtes Gedächtnis — hält man die Zelle länger oder härter unten, lässt sie langsamer los, weil sich die Ladungsträger in einer echten Photozelle tatsächlich so verhalten, nicht weil ein „Gedächtnis"-Parameter hinzugefügt wurde. Was man hört, ist das Eigenverhalten der modellierten Zelle, keine Kurve, die jemand gezeichnet hat, um ähnlich zu klingen.

## Fallstricke

- **Das Voicing ist durchgehend forschungsbasiert abgeleitet, nicht gegen echte Hardware-Einheiten gemessen.** Behandle CRUSH, SANDWICH, SPREAD und SLAP als musikalisch motivierte Schaltungsmodelle mit eigenem, getestetem, konsistentem Verhalten — nicht als Anspruch, den Klang eines bestimmten physischen Geräts zu treffen.
- **SPREADs Pitch Shifter kann bei einem anhaltenden reinen Ton** (ein Synth, oder ein sehr stabil gehaltener Vokal) **einen milden Kammfilter-Effekt erzeugen** — die zwei Delay-Taps crossfaden in festem Abstand, und bei realem Programmmaterial ist das unhörbar, aber eine anhaltend gehaltene Note ist der eine Fall, in dem es auftauchen kann.
- **Audition ist nicht Solo, und der Unterschied zählt.** Audition isoliert genau den benannten Bus, schließt den Direct-Pfad und jeden anderen Bus aus — der ganze Punkt ist, dass diese Busse nie in Isolation *beurteilt* werden sollen, nur gegengeprüft. Nicht als generelles Solo-Tool für unabhängiges Auditieren nutzen.
- **Mute gewinnt immer gegen Audition** auf demselben Bus — ein Bus, der gleichzeitig gemuted und auditioniert ist, bleibt still, nicht hörbar.
- **Die GUI ist ein funktionaler Slider-/Knopf-Editor; eine eigene Vektor-GUI mit Per-Bus-Nadelmetern folgt als späterer Meilenstein**, und die Preset-Leiste ist ein schlichter funktionaler Streifen, noch nicht umgestaltet.
- **Dynamics-Detection ist standardmäßig ungelinkt (unabhängig L/R)** bei CRUSH und SANDWICH — **Link** aktivieren, falls beide Kanäle einem gemeinsamen Detektor folgen sollen.
- **Bewusst außerhalb des Scopes dieses Releases**: ein kurzes Plate-Reverb-Modul, ein „BV-Mode"-Preset, austauschbare Kompressor-Farben über die zwei CRUSH-Styles hinaus, externer Sidechain, und ein Output-Limiter.
