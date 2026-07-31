<!-- German translation of lancet.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

# Lancet — Bedienungsanleitung

*Schneide, wo es zählt — ein chirurgischer Dynamic EQ mit analoger Seele.*

## Was ist neu in v0.4.0

**Der Attack-Regler ist jetzt bis hinunter zu 0,1 ms echt.** Bis v0.3.0 saß hinter
dem Gain-Computer ein fester 50-ms-Glätter, sodass keine Attack-Einstellung
schneller als etwa 50 ms tatsächlich hörbar war — 0,1 ms, 1 ms und 20 ms taten
allesamt dasselbe. Dieser Glätter ist weg; die Ballistik des Detektors selbst ist
jetzt das Einzige, was formt, wie schnell sich ein Band bewegt, und sie wird
einmal pro Sample ausgewertet.

**Bitte lies das, wenn du bestehende Sessions hast.** Eine Session, die eine von
null verschiedene Range mit schnellem Attack nutzt, *wird* schneller reagieren als
zuvor. Das ist ein Bugfix, keine Neuabstimmung — das Plugin tut jetzt, was sein
eigener Regler immer schon behauptet hat —, aber es ist eine reale, hörbare
Änderung, und du solltest damit rechnen, sie zu hören. Fühlt sich ein Band jetzt
zu zupackend an, dreh seinen Attack hoch: Zum ersten Mal hat dieser Regler die
Wirkung, die sein Label beschreibt. Sessions mit `Range = 0` auf jedem Band
(reiner statischer EQ, keine Dynamik) sind unverändert, und die statischen
EQ-Kurven selbst sind bei jedem Bandtyp, jedem Gain und jedem Q identisch mit
denen aus v0.3.0.

Ebenfalls neu:

- **Sidechain (SC Source: Internal / External).** Jedes Band kann seinen
  Detektor-Input jetzt aus einem externen Sidechain beziehen statt aus dem Audio,
  das durch das Band läuft — ein Band kann damit gegen eine Kick, einen
  Lead-Gesang oder alles andere ducken, was dein Host routen kann. Aktiviere
  zuerst den Sidechain-Input des Plugins in deinem Host; ist kein Sidechain
  verfügbar, nutzt ein auf External gestelltes Band schlicht weiter das interne
  Signal, statt zu verstummen.
- **SC Mode: Split / Wide.** Split (Default und das einzige Verhalten früherer
  Versionen) bedeutet, dass das Band nur auf seinen eigenen Frequenzbereich hört.
  Wide bedeutet, dass es auf das *gesamte* Signal hört und dabei weiterhin nur sein
  eigenes Band bewegt — der übliche Weg, ein Band mit dem Mix pumpen zu lassen.
  Listen folgt der jeweiligen Wahl, sodass du immer hörst, was das Band wirklich
  triggert.
- **Sauberere Saturation.** Die Saturation-Stufe pro Band nutzt jetzt einen
  antialiasten Waveshaper. Gleicher Charakter, spürbar weniger von den kratzigen
  Fold-back-Harmonischen, die ein einfacher Waveshaper bei hochfrequentem Material
  erzeugt — und weiterhin ohne zusätzliche Latenz.
- **Sanfteres Gain/Q.** Mit aktivierter Gain/Q-Kopplung gleitet das Q des Bands
  jetzt mit dem dynamischen Gain, statt zu springen.
- **Ein elftes Werkspreset, Sidechain Carve**, das das neue Routing demonstriert.

Beide neuen Regler pro Band sitzen im Editor als Comboboxen unter dem Type-Slot
des jeweiligen Bands. Von älteren Versionen gespeicherte Sessions laden exakt wie
zuvor, mit beiden neuen Reglern auf den Einstellungen, die das alte Verhalten
reproduzieren.

## Was ist neu in v0.3.0

Ein musikalischer Voicing-Pass (siehe `docs/voicing-notes.md`) — gemessen, wo die eigene DSP des Plugins eine Messung erlaubte, ehrlich als „nach Gehör, noch nicht gegen echtes Material abgestimmt" gekennzeichnet, wo nicht:

- **Per-Band-Defaults für Q/Threshold/Attack/Release, abgestimmt auf die dokumentierte Rolle jedes Bands** (vorher ein flaches Q 1.0/Threshold -30 dB/Attack 5 ms/Release 150 ms für jedes Band): Band 1 (100 Hz, Boom/Sub-Kontrolle) startet jetzt langsam und sanft (Attack 25 ms/Release 280 ms); Band 5 (4 kHz, Zischlaute/Härte) startet schnell (Attack 2 ms/Release 70 ms); die Bänder dazwischen stufen sich progressiv ab. Range startet weiterhin bei 0 dB (in Ruhe) für jedes Band — es bewegt sich nichts, bevor du eine Range einstellst, aber sobald du das tust, reagiert jedes Band jetzt so, wie es seine Rolle nahelegt. Siehe die aktualisierte Per-Band-Tabelle unten.
- **Gentle Saturation** (`bN_sat`, neuer Toggle pro Band, standardmäßig aus): ist er aktiviert, wird ein sanfter, `tanh`-basierter Waveshaper auf ein Band angewendet, aber *nur*, während es aktiv boostet (Gain + der dynamische Beitrag von Range netto positiv) — ein schneidendes oder ruhendes Band bleibt völlig unberührt, auch mit aktivierter Saturation. In v0.3.0 per Automation/Preset steuerbar; ein dedizierter Editor-Toggle ist Roadmap M3, genau wie Auto Release/Gain-Q.
- **Ein zehntes Werkspreset, „Analog Warmth Lift"** (`docs/presets.md`): demonstriert den neuen Saturation-Toggle an einem sanften Low-Mid-Boost.
- Eine v0.2.0-Session lädt sauber in v0.3.0 (toleranter Import): Jeder bestehende Parameterwert bleibt exakt erhalten, und der neue Saturation-Toggle pro Band wird mit seinem Aus-Standardwert befüllt.

## Was ist neu in v0.2.0

Ein recherchebasiertes Deep-Dive-Rework (siehe `docs/design-brief.md`/`docs/research-notes.md`), das M2-Preset-System der Suite sowie eine deutsche Interface-Lokalisierung:

- **Programmabhängiges Auto Release** (`bN_autoRelease`, neuer Toggle pro Band, standardmäßig aus): Ist es aktiviert, verkürzt sich die *effektive* Release-Zeit eines Bands automatisch — nie langsamer als die manuelle Release-Einstellung —, wenn die eigene Hüllkurve des Signals bereits von selbst abfällt (z. B. bei einem natürlich abklingenden Transienten), inspiriert von (nicht eine Nachbildung von) dem in F6-Klasse-Dynamic-EQs dokumentierten „ARC"-artigen Release-Verhalten. In v0.2.0 per Automation/Preset steuerbar; ein dedizierter Editor-Toggle ist für Roadmap M3 vorgesehen.
- **Gain/Q-Kopplung** (`bN_gainQ`, neuer Toggle pro Band, standardmäßig aus): Ist sie aktiviert, wird das eigene Filter-Q eines Bands proportional dazu weicher (breiter), wie stark sich sein dynamisches Gain gerade bewegt — für einen sanfteren, analogeren Charakter bei tieferen dynamischen Bewegungen. Das *statische* Gain des Bands beeinflusst Q nie, nur seine dynamische Komponente tut das. Gleicher Automations-/Preset-only-Status wie Auto Release in v0.2.0.
- **Attack-/Release-Bereiche erweitert**: Attack jetzt 0.1 bis 500 ms (vorher 0.5 bis 100 ms), Release jetzt 5 bis 1500 ms (vorher 10 bis 1000 ms) — an beiden Enden, für sowohl schnelleres Transienten-Einfangen als auch langsamere, musikalische Tonalausgleichs-Anwendungsfälle.
- **Die Knee-Breite wird jetzt von Range abgeleitet**, statt einer festen 6-dB-Konstante — flachere Range-Einstellungen wirken jetzt sanfter/weicher, Range-Einstellungen mit voller Tiefe (±12 dB) klingen identisch zum festen 6-dB-Knee von v0.1.0.
- **Neun Werkspresets** (`docs/presets.md`) für gängige Anwendungsfälle (Glue, De-Essing, Transientenverstärkung, Mix-Bus-Beruhigung, langsamer Tonalausgleich, Resonanz-Zähmung und eine diagnostische Auto-Release-Demo), plus eine Preset-Leiste (Save/Save As/Delete/Import/Export, Werks- + Nutzer-Bibliothek) am oberen Rand des Editors.
- Eine v0.1.0-Session lädt sauber in v0.2.0 (toleranter Import): Jeder bestehende Parameterwert bleibt exakt erhalten, und die beiden neuen Toggles pro Band werden mit ihrem Aus-Standardwert befüllt.

## Was es ist

Lancet ist ein Six-Band Dynamic EQ im Geiste der Waves-F6-Klasse — hier als dokumentierter Referenzpunkt für die Kategorie genannt, ohne eine Empfehlung, ein Sponsoring oder eine Zugehörigkeit durch Waves Audio Ltd. zu implizieren. Jedes Band ist ein normales parametrisches EQ-Band (Bell, oder Shelf bei Band 1/Band 6), dessen Gain sich zusätzlich mit dem Programmmaterial bewegen kann. Fütterst du es laut, reagiert es — schneidet eine Resonanz nur, wenn sie aufflammt, oder öffnet einen Boost nur, wenn ein Part untergeht — und pendelt sich dann wieder auf seine statische Einstellung ein, sobald der Pegel wieder fällt. Da die dynamische Bewegung jedes Bands von seinem *eigenen*, vor dem EQ sitzenden, bandgefilterten Detector angetrieben wird, verwirrt der Cut eines Bands nie den Detector eines anderen, und die eigene Gain-Bewegung eines Bands beeinflusst nie seine eigene Erkennung.

Wo ein statisches EQ-Band nur „wie viel?" fragt, fragen Lancets dynamische Bänder zusätzlich „wann?" — der Unterschied zwischen einer dauerhaft ausgekerbten 3-kHz-Resonanz (die den Ton auch dann ausdünnt, wenn diese Resonanz gar nicht vorhanden ist) und einem Zurückziehen genau dann, wenn sie klingelt.

## Wo es in einer Mix-Kette sitzt

Lancet ist ein **korrigierendes, chirurgisches Werkzeug**, am nützlichsten früh bis mittig in der Signalkette, vor breiter Klangformung und Bus-Kompression:

```
Source track -> [gain staging / gate] -> Lancet (resonance/harshness control) -> broad EQ / saturation -> compression -> bus
```

Greife danach, wenn ein statischer EQ-Cut das Problem entweder unterbehandeln würde (sodass es bei den lautesten Treffern trotzdem noch durchsticht) oder überbehandeln würde (und den Ton in leiseren Passagen ausdünnt, in denen das Problem gar nicht vorhanden ist). Es funktioniert auch als Mix-Bus- oder Master-Bus-Werkzeug, um eine bestimmte wiederkehrende Resonanz oder ein hartes Frequenzband zu kontrollieren, ohne alles darunter dauerhaft einzufärben.

## Signalfluss

```
in --[Input Trim]--+--[pre-chain tap]--> each band's Detector (bandpass @ band freq/Q -> envelope)
                    |
                    +--> Band1 -> Band2 -> Band3 -> Band4 -> Band5 -> Band6 --> [Mix] --> [Output Trim] --> out
```

Der Detector jedes Bands zapft das Signal direkt nach Input Trim an, *vor* Band 1 — nicht den seriell bereits verarbeiteten Input dieses Bands selbst —, sodass die Gain-Bewegung eines nachgelagerten Bands nie die Erkennung eines vorgelagerten Bands stört und die eigene Bewegung eines Bands nie ihre eigene Auslösung zurückfüttert. Die vollständige technische Aufschlüsselung (Gain-Computer-Formel, Detector-Selektivität, Sub-Block-Koeffizienten-Smoothing, Listen) findest du in [`docs/architecture.md`](architecture.md).

## Unter der Haube

### Der Per-Sample-Gain-Pfad und der TPT-SVF-Kern

Bis v0.3.0 kam das realisierte Gain eines Bands aus einem 50-ms-`juce::SmoothedValue`,
das *hinter* dem Gain-Computer saß — der Detector konnte in einer halben
Millisekunde reagieren, und der Filter brauchte trotzdem 50 ms, um aufzuholen,
sodass der größte Teil des ausgelieferten 0,1–500-ms-Attack-Bereichs nichts
Hörbares bewirkte. v0.4.0 entfernt diesen Glätter und wertet die gesamte Kette —
Detector-Hüllkurve, dB-Konvertierung, Soft-Knee-Gain-Computer, Range-Clamp,
Filter-Gain — einmal pro Sample aus. Die Detector-Hüllkurve *ist* jetzt der
Glätter, und es gibt für keinen Bandtyp einen gestuften Gain-Fallback.

Den Glätter aus einem koeffizienten-neuaufbauenden Biquad zu entfernen, wäre
für sich genommen ein Zipper-Rauschen-Generator gewesen, also änderte sich
auch der Filter-Kern. Ein Direct-Form-Biquad, dessen Koeffizienten jedes
Sample springen, ist kein wohldefiniertes zeitvariantes Filter — sein interner
Zustand bedeutet nach jedem Sprung etwas anderes. Jedes Band (Bell, Low Shelf,
High Shelf) läuft stattdessen auf `lnct::TptSvf`, einem topologie-erhaltend
transformierten (trapezoid-integrierten) State-Variable-Filter, aufgebaut aus
Andrew Simpers veröffentlichten Cytomic-Gleichungen, ohne vendorten
Drittanbieter-Code. Seine zwei Zustandsvariablen sind physikalische
Integrator-Outputs, die ihre Bedeutung behalten, egal wie sich die
Koeffizienten bewegen, sodass Gain jedes Sample ohne Artefakt moduliert werden
kann. Der Frequenz-Warp der Bell ist vollständig gain-unabhängig — dynamisches
Gain geht nur als skalare Bandpass-Mischung ein, nie durch Neustimmen der
Mittenfrequenz —, und der Integrator-Zustand wird in `double` gehalten, obwohl
der Audio-Pfad `float` ist, weil die eigene Auslöschung des trapezoiden
Updates bei tiefer Frequenz und hoher Q in einfacher Genauigkeit Stellen
verliert.

Die realisierte statische Response ist von alldem unverändert: verifiziert
gegen eine unabhängige Referenz in doppelter Genauigkeit auf besser als
−100 dBFS Peak-Residuum über zehn Sekunden Breitbandrauschen pro Setting, und
gegen die analytische RBJ-Magnitude-Response auf ±0,05 dB genau über ein
Band-Typ/Gain/Q-Raster. Bei exakt 0 dB ist jeder gain-abhängige Misch-Skalar
*exakt* null, sodass ein untätiges Band konstruktionsbedingt bit-transparent
ist, ohne Branch und ohne Sonderfall.

### Detector-Design

Im Split-Modus kaskadiert der Detector **zwei** Bandpass-Biquads bei der
eigenen Frequenz/Q des Bands statt einem, weil eine einzelne Stufe zwei
Oktaven daneben bei Q 1 nur etwa −12 dB erreicht — nicht genug Headroom
gegen einen lauten Ton außerhalb des Bands, der das Band fälschlich triggert.
Die Kaskade misst besser als −24 dB, komfortabel jenseits der eigenen
>20-dB-Zwei-Oktaven-Isolationsgrenze des Plugins. Stereo-(oder breitere)
Eingänge sind **gelinkt**: Jede Kaskadenstufe läuft unabhängig pro Kanal mit
eigenem Filter-Zustand, aber der Envelope-Follower ist ein einzelner
bandweiter Wert, gespeist vom lautesten (Max-Abs-)Sample über alle Kanäle zu
jedem Zeitpunkt — was den Stereobild-Shift vermeidet, den vollständig
unabhängige Gain Reduction pro Kanal einführen würde. Es gibt keine
Per-Band-Unlink-Option. Die Hüllkurve selbst ist ein One-Pole-Peak-Follower,
der **pro Sample** für korrektes Ballistik-Timing läuft; nur die eigenen
Koeffizienten des Bandpasses sind auf Sub-Block-Granularität gedrosselt, nie
die Hüllkurve.

### Auto Release: eine dedizierte schnelle Referenz-Hüllkurve

Auto Release (standardmäßig aus) verkürzt das effektive Release eines Bands,
wann immer die eigene Hüllkurve des Signals bereits von selbst abfällt,
geklemmt, sodass das Ergebnis immer mindestens so schnell ist wie — nie
langsamer als — die manuelle Release-Einstellung. Das Detail, das man kennen
sollte: Die Fall-Raten-Messung kommt von einer **zweiten, dedizierten, immer
schnellen Hüllkurve** innerhalb des Detektors (gleicher Attack-Koeffizient,
aber ein fixes Release, gekoppelt an die eigene 5-ms-Untergrenze des Plugins),
nicht von der Haupt-Hüllkurve. Sie aus der Haupt-Hüllkurve abzuleiten
funktioniert nicht — eine langsame Hüllkurve ist selbst eine tiefpassgefilterte
Ansicht des Inputs, ratenbegrenzt auf etwa ihre eigene Zeitkonstante, sodass
„wie schnell fällt die langsame Hüllkurve" meist den eigenen Koeffizienten der
langsamen Hüllkurve an sich selbst zurückmisst. Ein früherer interner
Implementierungsversuch machte genau diesen Fehler, und sein Output war messbar
identisch, egal ob Auto Release an oder aus war.

### Antialiaste Saturation, weiterhin ohne Latenz

Die optionale Saturation-Stufe pro Band ersetzt einen einfachen
`tanh`-Waveshaper durch einen Antiderivative-Antialiasing-Kernel 1. Ordnung
(ADAA1) derselben Form, berechnet als Differenzquotient von `ln(cosh(x))`
zwischen aufeinanderfolgenden Samples — gleicher harmonischer Charakter,
messbar weniger Fold-back, keine Oversampling-Stufe und keine zusätzliche
Latenz. Die Spezifikation ist bewusst relativ statt einer absoluten
Alias-Boden-Behauptung; siehe „Latenz und Aliasing" weiter unten für die
gemessenen Zahlen und die Begründung. Saturation greift nur, während ein Band
aktiv boostet (statisches + dynamisches Gain netto positiv) — ein
schneidendes oder untätiges Band bleibt damit eingeschaltet bit-identisch.

### Engineering-Hygiene

- **Keine Heap-Allokationen auf dem Audio-Thread**, bewiesen unter einem
  ersetzten Allocator, auch mit aktivem Sidechain-Bus und Auto Release /
  Gain-Q / Saturation an auf jedem Band. Koeffizienten-Updates schreiben ein
  reines Stack-`ArrayCoefficients`-Ergebnis direkt in bereits allozierten
  Speicher, statt `juce::dsp::IIR::Coefficients::makeXxx()` aufzurufen, das
  bei jedem Aufruf ein frisches Objekt heap-alloziert.
- **Untätige Arbeit wird übersprungen.** Der Detector-Bandpass und der
  SVF-Frequenz-Warp berechnen nur neu, wenn sich die geglättete
  Frequenz/Q tatsächlich über ein Epsilon hinaus bewegt hat, und die
  Per-Sample-SVF-Skalare sind bei exaktem Gain-Match memoisiert, sodass ein
  Band bei eingeschwungenem Gain nichts neu berechnet und bit-transparent ist,
  sobald seine Parameter statisch sind.
- **NaN/Inf-Recovery ist eingebaut, auch für den Sidechain.** Ein
  nicht-endlicher Wert würde sonst die Integrator-Rekursion des SVF dauerhaft
  vergiften; der Filter setzt seinen Zustand sauber zurück und liefert 0,
  erholt sich innerhalb desselben Blocks statt ein `reset()` zu brauchen —
  verifiziert mit einem NaN/Inf-vergifteten Sidechain und allen sechs Bändern
  auf External, was den Haupt-Output weder stummschalten noch vergiften kann.

## Parameter-Referenz

### Je Band (Band 1 – Band 6, identische Regler sofern nicht anders angegeben)

| Parameter | Range | Default | Unit | Was es musikalisch bewirkt |
|---|---|---|---|---|
| **On** | Off / On | Off (Band 3: On) | | Aktiviert das Band. Ein ausgeschaltetes Band ist ein echter Bypass — es rührt das Signal überhaupt nicht an, auch wenn sein Detector darunter weiterläuft, damit es beim Wiedereinschalten keinen Sprung gibt. |
| **Type** | Bell / Shelf | Bell | | **Nur Band 1 und Band 6.** Der Shelf von Band 1 ist ein Low Shelf (hebt/senkt alles unterhalb von Freq); der Shelf von Band 6 ist ein High Shelf (hebt/senkt alles oberhalb von Freq). Band 2–5 sind immer Bell. |
| **Freq** | 20 - 20000 | 100 / 250 / 630 / 1600 / 4000 / 10000 | Hz | Die Mittenfrequenz des Bands (Bell) oder die Eckfrequenz (Shelf) — sowohl die Form des Filters selbst *als auch* das, worauf sein Detector hört. |
| **Q** | 0.3 - 12 | 0.9 / 1.1 / 1.0 / 1.2 / 1.4 / 1.0 (v0.3.0, pro Band — siehe Tabelle unten) | | Wie schmal (hohes Q) oder breit (niedriges Q) das Band ist. **Wird im Shelf-Modus ignoriert**, der unabhängig von dieser Einstellung immer eine feste, standardmäßige Shelf-Flanke nutzt (Q = 0.707). |
| **Gain** | -12 - +12 | 0 | dB | Das *statische* Gain des Bands — immer angewendet, dynamisch oder nicht. Setze das auf deine „Ruhe"-EQ-Bewegung; Range addiert oder subtrahiert dann obendrauf, wenn der Detector auslöst. |
| **Range** | -12 - +12 | 0 | dB | Wie weit sich das Gain des Bands dynamisch bewegen kann, zusätzlich zu Gain. **0 = ein rein statisches EQ-Band** (kein Detector-Einfluss). Negatives Range schneidet, wenn das Signal lauter als Threshold wird (die klassische Resonanz-Zähmung/De-Essing-Bewegung); positives Range boostet, wenn es lauter wird (eine aufwärtsgerichtete „Duck-in"-Expansions-Bewegung, nützlich z. B. um Anschlag nur bei hart gespielten Noten hervorzuheben). |
| **Thresh** | -60 - 0 | -26 / -28 / -26 / -24 / -22 / -20 (v0.3.0, pro Band — siehe Tabelle unten) | dB | Der Detector-Pegel, ab dem die dynamische Bewegung einsetzt. Ein Soft-Knee, zentriert auf diesen Wert, macht den Übergang graduell statt zu einem harten Schalter — die Breite des Knees selbst skaliert mit Range (v0.2.0): `clamp(\|Range\| * 0.5, 2, 10)` dB, sodass flachere Range-Einstellungen sanfter wirken und Range-Einstellungen mit voller Tiefe (±12 dB) identisch zum festen 6-dB-Knee von v0.1.0 klingen. |
| **Attack** | 0.1 - 500 | 25 / 15 / 8 / 4 / 2 / 3 (v0.3.0, pro Band — siehe Tabelle unten) | ms | Wie schnell sich das dynamische Gain bewegt, sobald der Detector den Threshold überschreitet. Schneller Attack erwischt Transienten hart; langsamerer Attack lässt einen kurzen Peak durch, bevor reagiert wird, was bei perkussivem Material natürlicher klingen kann. Die 500-ms-Obergrenze ist für langsame, musikalische Tonalausgleichs-Bewegungen gedacht, nicht für das Einfangen von Transienten. **Seit v0.4.0 ist dieser Regler über seinen gesamten Bereich echt** — siehe „Was ist neu in v0.4.0" oben; davor verhielt sich alles unterhalb von ~50 ms identisch. |
| **Release** | 5 - 1500 | 280 / 180 / 130 / 100 / 70 / 90 (v0.3.0, pro Band — siehe Tabelle unten) | ms | Wie schnell das dynamische Gain zurück Richtung Gain kehrt, sobald der Detector wieder unter den Threshold fällt. Schneller Release kann bei anhaltendem Material hörbar pumpen; langsamer Release glättet die Rückkehr, kann aber einen Cut/Boost in Inhalt hineinhalten, der ihn nicht mehr braucht. |
| **Listen** | Off / On | Off | | Solot das eigene Detector-Signal dieses Bands — das bandpassgefilterte Audio vor dem EQ, das tatsächlich seine dynamische Bewegung antreibt — anstelle des normalen Programm-Outputs, um genau zu hören, was es auslöst. Exklusiv: Aktivierst du Listen bei einem Band, deaktiviert das automatisch Listen bei jedem anderen Band. Die vollständige Signalkette (inklusive der Verarbeitung jedes einzelnen Bands) läuft darunter weiter, sodass das Deaktivieren von Listen nie knackt. |
| **Auto Release** (v0.2.0) | Off / On | Off | | Programmabhängiges Auto-Release: Ist es aktiviert, verkürzt sich die *effektive* Release-Zeit für einen gegebenen Übergang automatisch (nie unter die eigene 5-ms-Release-Untergrenze des Plugins, nie über die manuelle Release-Einstellung selbst hinaus), sobald die eigene Hüllkurve des Signals bereits von selbst abfällt — nützlich, um ein Band bei natürlich abklingendem Material schneller entspannen zu lassen, ohne für anhaltendes Material auf einen langsameren, musikalischen manuellen Release zu verzichten. In v0.2.0 nur per Automation/Preset — noch kein dedizierter Editor-Regler (Roadmap M3). |
| **Gain/Q** (v0.2.0) | Off / On | Off | | Gain/Q-Kopplung: Ist sie aktiviert, verbreitert (weicht) sich das eigene Filter-Q des Bands proportional dazu, wie weit sein *dynamisches* Gain gerade in Richtung Range steht — ein sanfterer, analogerer Charakter bei tieferen dynamischen Bewegungen. Das statische Gain beeinflusst Q nie, nur die dynamische Komponente tut das. In v0.2.0 nur per Automation/Preset — noch kein dedizierter Editor-Regler (Roadmap M3). |
| **SC Source** (v0.4.0) | Internal / External | Internal | | Wo der Detektor dieses Bands hört. **Internal** (Default und das einzige Verhalten jeder früheren Version) ist das durch das Plugin laufende Signal, abgegriffen vor Band 1. **External** ist der Sidechain-Input des Plugins — route in deinem Host etwas anderes dorthin, und dieses Band bewegt sich als Reaktion auf *das*, während es weiterhin das Hauptsignal filtert. Stellt dein Host keinen Sidechain bereit oder bleibt der Sidechain-Input deaktiviert, fällt ein auf External gestelltes Band auf Internal zurück, statt zu verstummen. Auf den Sidechain wird keine Delay-Kompensation angewendet, er muss also bereits vom Host zeitlich ausgerichtet sein. |
| **SC Mode** (v0.4.0) | Split / Wide | Split | | Wie viel von der Quelle des Detektors dieses Band hört. **Split** (Default) filtert den Detektor-Input auf den eigenen Frequenzbereich dieses Bands herunter, sodass nur Inhalt nahe Freq es triggern kann — das chirurgische Verhalten. **Wide** überspringt diesen Filter, sodass das Band auf den Gesamtpegel über das ganze Spektrum reagiert und dabei weiterhin nur sein eigenes Band bewegt. Wide willst du, wenn ein Band mit dem Mix atmen soll, statt eine Resonanz zu überwachen. Listen folgt dieser Einstellung, sodass du immer das echte Trigger-Signal abhörst. |
| **Saturation** (v0.3.0) | Off / On | Off | | Sanftes Waveshaping: Ist es aktiviert, wird ein sanfter Drive auf den eigenen Output des Bands angewendet, aber nur, während es aktiv boostet (Gain + der dynamische Beitrag netto positiv) — ein schneidendes oder ruhendes Band bleibt unberührt, auch damit aktiviert. Der Drive skaliert damit, wie stark das Band gerade boostet (kaum wahrnehmbar nahe 0 dB, deutlich hörbar, aber weiterhin soft-knee-geformt nahe +12 dB). Seit v0.4.0 ist der Waveshaper antialiast und fügt damit weit weniger vom harschen Fold-back-Grit hinzu, den ein einfacher Waveshaper bei hochfrequentem Material erzeugt, ohne Latenzkosten. Nur per Automation/Preset — noch kein dedizierter Editor-Regler (Roadmap M3). |

Per-Band-Voicing-Defaults (v0.3.0, `docs/voicing-notes.md`) — abgestimmt auf die
typische Rolle jedes Bands entlang der bestehenden Frequenzleiter, kein flacher
Wert, der über jedes Band hinweg wiederholt wird:

| Band | Freq | Rolle | Q | Threshold | Attack | Release |
|---|---|---|---|---|---|---|
| 1 | 100 Hz (Low Shelf) | Boom-/Sub-Kontrolle | 0.9 | -26 dB | 25 ms | 280 ms |
| 2 | 250 Hz | Mulm-/Boxiness-Resonanz (Vocal & Gitarrenkörper) | 1.1 | -28 dB | 15 ms | 180 ms |
| 3 | 630 Hz | Allgemeine Mitten-Präsenz (standardmäßig aktives Demo-Band) | 1.0 | -26 dB | 8 ms | 130 ms |
| 4 | 1600 Hz | Vocal-Präsenz / Gitarren-Schärfe | 1.2 | -24 dB | 4 ms | 100 ms |
| 5 | 4000 Hz | Zischlaute / Anschlag / Härte | 1.4 | -22 dB | 2 ms | 70 ms |
| 6 | 10000 Hz (High Shelf) | Luft / Fizz-Erholung | 1.0 | -20 dB | 3 ms | 90 ms |

### Global

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Input Trim** | -12 - +12 | 0 | dB | Gain, das vor Band 1 angewendet wird — und bevor der Detector jedes Bands das Signal anzapft, verschiebt es also auch, welcher Pegel den Threshold jedes Bands erreicht. |
| **Output Trim** | -12 - +12 | 0 | dB | Gain, das nach Band 6 und nach der Mix-Blende angewendet wird — die finale Gain-Stufe, um den Ausgangspegel von Lancet an das anzupassen, was als Nächstes in der Kette folgt. |
| **Mix** | 0 - 100 | 100 | % | Paralleler Dry/Wet-Blend der gesamten Six-Band-Kette. 100 % ist vollständig prozessiert; niedrigere Werte mischen zunehmend mehr vom unbearbeiteten (aber weiterhin Input-getrimmten) Signal bei — nützlich für „New-York"-artiges paralleles Dynamic EQing, bei dem die Korrektur hinzufügen statt vollständig ersetzen soll. |

## Presets

Am oberen Rand des Editors sitzt eine Preset-Leiste: `[<] [Preset Name] [>]`, um alphabetisch durch die Werks- und Nutzer-Bibliothek zu blättern, `Save`/`Save As...`, um eigene Presets zu schreiben, `Delete` für Nutzer-Presets, `Import.../Export...` für einzelne `.basilicapreset`-Dateien oder `.zip`-Bänke, sowie ein Menü (Klick auf den Preset-Namen) mit einem Eintrag „Set current as default" für deinen eigenen Out-of-the-Box-Startpunkt. Elf Werkspresets werden mit v0.4.0 ausgeliefert — was jedes davon bewirkt und warum, steht in `docs/presets.md`. Nutzer-Presets werden pro Nutzer unter `~/Library/Audio/Presets/Yves Vogl/Lancet/` auf macOS gespeichert (`%APPDATA%/Yves Vogl/Lancet/Presets/` unter Windows).

Die Interface-Texte des Editors (Preset-Leisten-Beschriftungen, Menüs, Dialoge) werden automatisch auf Deutsch lokalisiert, wenn die Systemsprache Deutsch ist; Parameternamen, Einheiten und Fachbegriffe (Attack, Release, Hz, dB, ms, …) bleiben immer auf Englisch — genau wie bei jedem anderen Basilica-Audio-Plugin.

## Tipps

- **Setze Gain und Range getrennt und bewusst.** Gain ist das, was das Band *immer* tut; Range ist das, was es *zusätzlich* tut, nur wenn ausgelöst. Ein Band mit Gain=0, Range=-6 ist in Ruhe unhörbar und schneidet nur, wenn die Resonanz aufflammt — ganz anders als Gain=-3, Range=-3, das immer ein bisschen schneidet und bei Auslösung noch härter schneidet.
- **Nutze Listen, um das Problem zu finden, bevor du Threshold setzt.** Fahre Freq/Q mit aktiviertem Listen durch, bis du die Resonanz oder Härte klar isoliert hörst, *dann* setze Threshold knapp über den Pegel, den sie hat, wenn sie kein Problem ist — das ist deutlich zuverlässiger, als einen Threshold-Wert gegen den vollen Mix zu erraten.
- **Schmale, high-Q-Bänder mit negativem Range sind das klassische Resonanz-Zähmungs-Setup** (ein dumpfer 300–500-Hz-Aufbau, eine harte 2–4-kHz-Plektrum-/Rohrblatt-Kante, ein sibilantes 6–8-kHz-De-Esser-Band). Halte Q hoch genug, dass der Cut den umgebenden Ton nicht hörbar ausdünnt, wenn er einsetzt.
- **Breite, low-Q-Bänder mit negativem Range ergeben eine sanftere, breitere dynamische Klangkontrolle** — nützlich auf einem Mix-Bus, um ein ganzes Register zu zähmen (z. B. „die Low-Mids werden etwas zu viel, wann immer die ganze Band gemeinsam zuschlägt"), ohne die chirurgische Enge eines De-Esser-artigen Bands.
- **Positives Range (aufwärts/Duck-in) ist die weniger naheliegende Bewegung** — probiere es auf einem low-Q-Hochfrequenzband, um Anschlag oder Atem-/Konsonanten-Details nur bei den Noten hervorzuholen, die es brauchen, statt ständig das ganze Register (und seinen Rauschteppich) zu boosten.
- **Schneller Attack + schneller Release können bei anhaltendem Material hörbar pumpen** (Bass, Flächen, gehaltene Vocal-Noten) — klingt ein Band instabil oder „atmend", versuche zuerst einen langsameren Release, bevor du zu einem schmaleren Q greifst.
- **Mix unter 100 % erhält den Charakter der dynamischen Bewegung, während ihre Tiefe reduziert wird** — ein schneller Weg, eine übertrieben aggressive Range-Einstellung zurückzunehmen, ohne Threshold/Range jedes Bands von Grund auf neu einzustellen.
- **Greife zu SC Mode: Wide, wenn ein Band mit dem Mix atmen soll, statt eine Resonanz zu überwachen** (v0.4.0). Split ist der richtige Default für chirurgische Arbeit — nur Inhalt nahe Freq kann das Band triggern. Wide lässt das Band auf den Gesamtpegel reagieren, während es weiterhin nur sein eigenes Band bewegt — das willst du für „die Low-Mids ducken, wann immer die ganze Band zuschlägt" oder für ein Band, das eine Full-Range-Sidechain-Quelle trackt. Ein Wide-Band mit schmalem Q ist eine völlig sinnvolle Kombination: Q formt, *was sich bewegt*, der Modus entscheidet, *was es triggert*.
- **Setze bei externem Sidechain den Threshold gegen den Pegel des Sidechains, nicht gegen den des Hauptsignals** (v0.4.0). Sobald SC Source auf External steht, reagiert das Band auf das, was dein Host hineinroutet — der Pegel, der Threshold erreicht, hat also nichts mit dem zu tun, worauf Lancet eingefügt ist. Aktiviere das Listen dieses Bands, um den Sidechain-Feed direkt zu hören, während du den Threshold findest — Listen auditiert immer genau das, was der Detektor tatsächlich hört, den Sidechain eingeschlossen.
- **Richte den Sidechain in deinem Host zeitlich aus, falls es darauf ankommt.** Lancet fügt nirgends eine Alignment-Delay ein (siehe „Latenz und Aliasing" unten), ein Sidechain, der in deinem Host spät ankommt, kommt also auch beim Detektor spät an.
- **Jetzt, wo Attack echt ist, probiere ihn zuerst, bevor du zu etwas anderem greifst** (v0.4.0). Packt ein Band bei Transienten zu hart zu, ist ein langsamerer Attack wieder ein echter Regler statt eines No-ops unterhalb von ~50 ms — meist der bessere erste Schritt, bevor du Q verbreiterst oder Range zurücknimmst.
- **Saturation lohnt sich nur dort einzuschalten, wo ein Band boostet.** Sie ist konstruktionsbedingt auf boostende Bänder beschränkt, sie auf einem schneidenden De-Esser-Band zu aktivieren bewirkt also gar nichts. Kombiniere sie mit einem moderaten positiven Gain (und optional positivem Range) auf einem Body-/Warmth-Band.

## Latenz und Aliasing

**Lancet fügt null Latenz hinzu — immer.** Es meldet 0 Samples vor und nach
der Vorbereitung durch deinen Host, bei jeder Samplerate und Blockgröße, mit
jedem aktivierten Band und aktiviertem Sidechain-Bus. Das ist per
Impulsantwort verifiziert (der Peak kommt tatsächlich auf Sample 0 zurück),
nicht nur gemeldet, und es gibt nirgends im Plugin eine Dry-Pfad-Delay-
Kompensation. Jedes Filter im Signalpfad — die sechs Bänder und ihre
Detektoren — ist minimalphasig, ohne Lookahead.

Zwei Entscheidungen aus v0.4.0 halten das bewusst so:

- **Die Saturation-Stufe wird arithmetisch antialiast, nicht durch
  Oversampling.** Sie nutzt einen antialiasten Waveshaper 1. Ordnung
  derselben `tanh`-Form, die frühere Versionen nutzten, hat also denselben
  harmonischen Charakter mit messbar weniger Fold-back — und keine
  Oversampling-Stufe, die entweder Latenz oder Phasenverzerrung gekostet
  hätte. Gemessene Unterdrückung des dominanten 30-kHz-zu-18-kHz-Foldings
  bei 48 kHz: 13,2 dB bei −24 dBFS, 10,0 dB bei −12 dBFS und 8,4 dB bei
  −6 dBFS Input. **Es wird kein absoluter Alias-Boden behauptet**, und das
  ist ehrlich statt zurückhaltend: Eine Behandlung 1. Ordnung bei der
  Basis-Samplerate verdient keinen. Willst du ein Band bei sehr
  hochfrequentem Material hart treiben und einen garantierten absoluten
  Boden, ist dafür ein oversamplendes Plugin da — und Oversampling kostet
  Latenz.
- **Der externe Sidechain trägt keine Alignment-Delay**, muss also bereits
  vom Host zeitlich ausgerichtet sein — dieselbe Anforderung, die
  vergleichbare Dynamic EQs haben.

**Sampleraten und Formate.** AU, VST3 und Standalone. Verifiziert endlich und
latenzfrei bei 44,1, 48, 88,2, 96, 176,4 und 192 kHz, sowie über einen
Sampleraten-Wechsel mitten in der Session. Mono- und Stereo-Hauptlayouts sind
beide unterstützt; der Sidechain-Input kann unabhängig vom Hauptlayout
deaktiviert, mono oder stereo sein, und alles breiter als Stereo darauf wird
zurückgewiesen statt still falsch interpretiert.

## Sessions, Presets und Kompatibilität

Sessions, die von jeder früheren Version gespeichert wurden, laden sauber,
mit jedem gespeicherten Parameterwert exakt erhalten und jedem seitdem
hinzugekommenen Parameter auf dem Default, der das ältere Verhalten
reproduziert. Konkret: Die Werte einer v0.1.0-Session überleben, die
Per-Band-Toggles aus v0.2.0/v0.3.0 (Auto Release, Gain/Q, Saturation) kommen
ausgeschaltet zurück, und die zwölf neuen Per-Band-Auswahlen von v0.4.0
kommen auf Internal und Split zurück — das einzige Routing, das jede frühere
Version je hatte.

Der gespeicherte Zustand trägt ab v0.4.0 einen Schema-Versions-Stempel. Ein
Zustand ohne einen wird als das ältere Schema gelesen. Heute muss nichts
konvertiert werden (der Default jedes neueren Parameters *ist* das ältere
Verhalten), aber der Stempel bedeutet, dass ein zukünftiges Release, das
tatsächlich etwas konvertieren muss, einen verlässlichen Weg hat, zu
erkennen, was es liest.

**Ein Vorbehalt, und es ist der wichtige:** Während deine gespeicherten
*Werte* unangetastet sind, wird eine Session, die eine von null verschiedene
Range zusammen mit schnellem Attack nutzte, unter v0.4.0 anders *klingen*,
weil der Attack-Pfad vorher kaputt war und jetzt repariert ist. Siehe „Was
ist neu in v0.4.0" oben in diesem Dokument. Dasselbe gilt für die zehn
Werkspresets von vor v0.4.0 — keiner ihrer gespeicherten Werte hat sich
geändert, aber die, deren Namen Schnelligkeit versprechen (De-Ess Stack,
Transient Snare Crack, Fast-Recovery Demo), verhalten sich jetzt so, wie ihre
Namen es immer behauptet haben.

## Bekannte Einschränkungen

Klar benannt, weil sie zu kennen nützlicher ist, als sie zu übersehen:

- **Die GUI ist ein funktionaler Slider/Toggle/Combo-Editor.** Die
  eigens vektorgezeichnete Oberfläche mit Gain-Reduction-Nadeln pro Band ist
  ein späterer Milestone. Das Plugin misst bereits, was diese Nadeln zeigen
  werden, und diese Messung ist gegen die tatsächlich im Output vorhandene
  Gain Reduction verifiziert — aber nichts zeigt es bislang an.
- **Auto Release, Gain/Q und Saturation haben keine Editor-Regler.** Alle
  drei sind vollständig automatisierbar und vollständig per Preset steuerbar;
  dedizierte Schalter kommen mit dem GUI-Pass. SC Source und SC Mode sind die
  bewussten Ausnahmen, weil ein Sidechain-Routing, das man nicht im Editor
  auswählen kann, überhaupt nicht nutzbar ist.
- **Q wird im Shelf-Modus ignoriert.** Der Low Shelf von Band 1 und der High
  Shelf von Band 6 nutzen immer die standardmäßige flache Shelf-Flanke
  (Q 0,707), sowohl für das hörbare Filter *als auch* für dessen passenden
  Detector-Bandpass.
- **Für die Saturation-Stufe wird kein absoluter Aliasing-Boden
  spezifiziert** — siehe „Latenz und Aliasing" oben.
- **Die Erkennung ist stereo-gelinkt ohne Unlink**, und es gibt keine
  Per-Band-M/S- oder L/R-Platzierung — siehe „Detector-Design" unter „Unter
  der Haube" oben.
- **Es gibt konstruktionsbedingt keinen Ratio-Regler.** Oberhalb des Knees
  bewegt sich das Gain 1:1 mit dem, wie weit der Detektor Threshold
  überschritten hat, bis es Range erreicht — das als harte Obergrenze für
  die dynamische Tiefe wirkt. Range ist der Regler für „wie weit kann sich
  das bewegen"; der Knee (dessen Breite mit Range skaliert) liefert die
  Einblendung.
- **Die Voicing-Defaults pro Band sind Engineering-Urteil, nicht nach Gehör
  gegen Referenzmaterial abgestimmt.** Die *Richtung* der v0.3.0-Voicing-
  Tabelle (tiefe Frequenz langsam und sanft, hohe Frequenz schnell und
  chirurgisch) ist eine etablierte Mixing-Konvention, und die resultierende
  *Reihenfolge* der Ballistik ist gemessen und von der Testsuite
  eingefroren. Die exakten Zahlen, und die Saturation-Drive-Kurve, sind
  abgestimmtes Urteil — nicht gegen echtes Vocal-/Gitarren-/Mix-Material
  validiert und nicht gegen irgendein anderes Produkt kalibriert. Ein
  Gehör-Abgleich gegen Dynamic EQs der Referenzklasse an echtem
  Programmmaterial ist ein benannter, noch offener Punkt; siehe
  `docs/voicing-notes.md` für den vollständigen Ehrlichkeitsabschnitt dazu,
  welche Zahl welche ist.
- **Noch nicht im Plugin, für spätere Releases vorgemerkt:** optionale
  Spectral-Resonance-Suppression, Per-Band-M/S- und L/R-Platzierung mit
  Stereo-Unlink, optionales HF-De-Cramping (bewusst verschoben, weil
  De-Cramping die *statische* Response bestehender Sessions verändert),
  breitere Range-/Q-/Release-Bereiche (die eine eigene Migrationsgeschichte
  brauchen, weil das Neuabbilden eines Parameterbereichs das
  Automations-Kurven-Mapping des Hosts verändert), Lookahead, Per-Band-Ratio,
  Linear Phase, mehr als sechs Bänder, und eine Spektrum-Analyzer-/EQ-Kurven-
  Anzeige.
- **Lancet ist Pre-1.0, und seine Binaries sind derzeit unsigniert.**
  Breaking Changes sind bis v1.0.0 möglich; Signierung, Notarisierung und
  Installer sind ein späterer Milestone. Siehe `README.md`.
