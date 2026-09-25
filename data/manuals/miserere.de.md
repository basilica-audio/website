<!-- German translation of miserere.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

# Miserere — Bedienungsanleitung (v0.7.0)

*Vier Stimmen, ein Gebet — die parallele Vocal-Vorlage in einem einzigen Plug-in.*

## Was Miserere ist

Miserere verpackt die dokumentierte **parallele Vocal-Vorlage der Ära 2010–2023** — den „Rough Vocal"-Workflow, der in öffentlichen Interviews von Mixing-Engineers wie Andrew Scheps populär gemacht wurde — in einem einzigen Plugin: einen **Direct**-Pfad plus vier **parallele Return-Busse** (CRUSH, SANDWICH, SPREAD, SLAP), jeder mit eigenem Return-Fader, Mute und Audition. Das ist eine dokumentierte, öffentlich belegte Technik aus dieser Ära (siehe `research-notes.md`), keine Befürwortung durch oder Verbindung zu einer namentlich genannten Person oder Marke.

**Die Kernidee — und v2s Korrektur gegenüber v0.1.0**: Der Direct-Pfad ist ein Draht. Ab Werk ist jede optionale Sektion darauf AUS, sodass die trockene Vocal im Wesentlichen unangetastet durchläuft — ihre natürliche Hüllkurve und Phrasierung bleiben erhalten. Alles andere legt sich *darunter*, über die vier Return-Busse, die Kopien des Direct-Pfad-Outputs bei Unity sind, hart bearbeitet werden und dezent zurückgemischt werden. „Selbst mit all dem Zeug im Mix würdest du wahrscheinlich denken, die Vocal ist bone dry" ist das Kalibrierungsziel.

## Signalfluss

```
in → [In Trim] → DIRECT PATH (serial; every section optional, ALL OFF by default:
                   De-Esser (pre) → FET Comp light → Console EQ → Sat → De-Esser (post))
        │ = "the channel". Output feeds the sum at unity AND all four sends (unity taps):
        ├─→ ① CRUSH    : FET limiter, all-buttons character        → return fader
        ├─→ ② SANDWICH : Passive EQ → Opto Leveler → Passive EQ    → return fader
        ├─→ ③ SPREAD   : dual micro-pitch (≈30/50 ms, ±cents, L/R) → return fader
        └─→ ④ SLAP     : ≈110 ms dark single-repeat delay          → return fader
   Σ (direct + returns) → [Parallel macro trim scales returns ①–④] → [Out Trim]
                        → [Output Limiter — off by default] → out
```

Die Busse ①/② sind minimalphasig und fügen keine Latenz hinzu, bleiben also sample-genau zum Direct-Pfad ausgerichtet — paralleles Summieren kammfiltert nie, unabhängig von den Einstellungen. Die Busse ③/④ sind by Design Delays (siehe `architecture.md`). Die belegten Erkenntnisse hinter jedem Default unten findest du in `research-notes.md`.

## Der Direct-Pfad

Standardmäßig aus, Sektion für Sektion, in Signalreihenfolge:

- **De-Ess Pre** — Split-Band-De-Esser, 4–9 kHz einstellbar, bis zu 10 dB Reduktion, platziert dort, wo die Dynamik der Vocal am größten ist (die dokumentierte „de-esse ganz am Anfang"-Regel).
- **FET Comp** — ein leichter, threshold-basierter Kompressor im FET-Stil, fest bei 4:1, ausgelegt auf sanfte 3–4 dB Peak Gain Reduction — „die einzige Stelle, an der serielle Kompression authentisch ist" in dieser Topologie. Seit v0.6.0 wählt ein **Character**-Schalter die Insert-Kompressor-Familie (generische Bezeichnungen, wie überall in diesem Plugin): **FET** (der Default — harter Knee, Panel-Timing, sauber; exakt das bisherige Verhalten), **VCA** (sauberes Bus-Style-Voicing mit einem 6-dB-Soft-Knee und knackigerem Attack; unterhalb des Knees ist es bit-transparent) und **Tube Mu** (ein breiter 12-dB-Knee, langsamerer Attack, längeres Release und ein Hauch Zweite-Harmonische-Wärme, die nur erscheint, während der Kompressor tatsächlich arbeitet — Gain-Reduction-gated, sodass Unity-Passagen sauber bleiben).
- **Console EQ** — ein Raster im Stil britischer Konsolen-EQs: HPF (18 dB/oct, 50/80/160/300 Hz), Low Shelf (±16 dB, 35/60/110/220 Hz), eine Mid Bell mit fixem Q (±18 dB, sechs gestufte Mittenfrequenzen), ein fixer 12-kHz-High-Shelf (±16 dB) und ein Drive-Regler, der dezente, Richtung 2./3. Ordnung tendierende Transformer-artige Harmonische beimischt.

  Seit v0.5.0 ist Drive ein Übertrager-Modell statt eines addierten Harmonischen-Terms: Das Signal läuft durch einen Fluss-Integrator in einen gebiasten Sättiger und zurück durch die exakte Inverse dieses Integrators. Weil magnetischer Fluss als Spannung geteilt durch Frequenz skaliert, steigt die dritte Harmonische zum Bassbereich hin von selbst an (gemessen +12 dB beim Übergang von 100 Hz zu 50 Hz), statt von Hand gewichtet zu werden. Bei 0 dB ist Drive ein bit-exakter Bypass. Der 12-kHz-Shelf ist seit v0.5.0 ebenfalls magnitude-matched, sodass er bei 44,1 kHz seine analoge Form in der obersten Oktave behält, statt Richtung Nyquist gequetscht zu werden.
- **Sat** — der aus v1 übernommene Sättiger im Tape-Stil, eine optionale „Grit"-Stufe. Seit v0.5.0 berechnet er seine Distortion in der Alias-unterdrückenden Form, die unter *Latenz und Aliasing* weiter unten beschrieben ist; bei 0 dB Drive ist er weiterhin ein bit-exakter Bypass.
- **De-Ess Post** — eine zweite De-Esser-Instanz am Ende der Kette, für Zischlaute, die Kompression oder EQ hervorgehoben haben.

## Die vier Return-Busse

### ① CRUSH — FET-Limiter, All-Buttons-Charakter

Kein Threshold-Regler: **Input** treibt das Signal in einen fixen, ratio-abhängigen Threshold und Knee. **Ratio** wählt 4:1/8:1/12:1/20:1/ALL (ALL ist eine plateauförmige Kurve mit bewusstem Give-back und einer kurzen Attack-Verzögerung, die Transienten durchschlagen lässt, bevor geklemmt wird — der „Snap"). **Attack**/**Release** sind 1–7-Regler, bei denen eine HÖHERE Zahl SCHNELLER bedeutet, passend zur Hardware-Konvention, an der sich das orientiert; Release ist programmabhängig (schnell nach kurzen Transienten, mehrfach langsamer nach anhaltend starker Kompression). **Style** wählt das Voicing des Limiters: **All-Buttons** (Default), ein weicheres, fixes 2:1-**Gentle**-Voicing, oder — seit v0.6.0 — **Vintage**, ein Hot-Bias-Zustand aus einer frühen Revision, der die komplette Ratio-Reihe aktiv lässt, aber zwei dB früher zubeißt, die Feedback-Schleife heißer laufen lässt und das residuale Second-Harmonic-„Haar" der FET-Zelle mehr als verdoppelt — für ein raueres, stärker gefärbtes Crush bei denselben Einstellungen. Dieser Bus soll solo „furchtbar" klingen (nutze Audition) und im Mix gut.

CRUSH bringt außerdem einen Hauch programmabhängiger Färbung mit: Mit wachsender Gain
Reduction mischen sich eine Transformer-artige Tiefton-Sättigung und die zweite Harmonische,
die die FET-Zelle selbst übriglässt, unter den Detektor-Ripple-Charakter des Limiters — bei
leichten Einstellungen vernachlässigbar und nur wachsend, je härter der Bus arbeitet. Ein
sauberes, kaum komprimiertes Signal bleibt unangetastet; nutze Input und Audition, um es zum
Leben erwecken zu hören.

Seit v0.5.0 ist nichts davon tabelliert. Der Detektor ist eine echte Feedback-Schleife: Der
Sidechain wird vom Bus-Output über ein RC-Netzwerk mit einem einzigen Kondensator getrieben,
mit Attack im Lade- und Release im Entladepfad — und deshalb passieren die Verhaltensweisen,
für die diese Limiter-Bauart bekannt ist, jetzt einfach, statt skriptiert zu sein: Die
effektive Ratio steigt, während eine Note gehalten wird, die Release-Einstellung verändert
hörbar, wie schnell der Attack eintrifft, der Knee zieht sich an, je weiter du die Ratio-Reihe
hochgehst, und ALL überschwingt, bevor es sich einpendelt. ALL ist eine eigene Einstellung und
keine Interpolation zwischen den nummerierten Ratios.

### ② SANDWICH — Passive EQ → Opto Leveler → Passive EQ

Zwei unabhängige Passive-EQ-Instanzen klammern einen Leveler im Opto-Stil ein. Jeder Passive EQ bietet einen gemeinsam-frequenten LF-**Boost** und -**Cut** (beide können gleichzeitig laufen — eine bewusst nicht-kompensierende Kurve, keine simple Summe auf Flat), einen HF-**Bell Boost** mit variabler Bandbreite und ein HF-**Shelf Atten**. Der Opto Leveler hat keinen Threshold: **Peak Reduction** treibt die Zelle härter, wobei **Limit** die Kompression Richtung Limiting strafft. **Emphasis** macht den Detektor zunehmend HF-selektiv (bis zu −10 dB geringere LF-Empfindlichkeit), sodass er bei hohen Einstellungen hauptsächlich auf Zischlaute/Presence reagiert, „wie ein Multiband". **Residual** (standardmäßig an) behält den kleinen, nie ganz flachen Vintage-Tilt des Passive EQ; deaktiviere es für einen saubereren EQ.

Seit v0.5.0 ist der Leveler ein Fotozellen-Modell statt eines Satzes gezeichneter Kurven. Das
Kompressionsverhältnis, das zweistufige Release (eine schnelle erste Erholung, gefolgt von
einem langen Ausklang), der Memory-Effekt — halte ihn länger oder härter unten und er lässt
langsamer los — und der programmabhängige Attack sind allesamt Konsequenzen daraus, wie sich
Ladungsträger in der Zelle aufbauen und wieder abfließen. Es gibt keinen Ratio-Regler, weil es
in der Schaltung keinen Ratio-Parameter gibt; was du hörst, ist das Eigenverhalten der Zelle,
und genau darin liegt der ganze Reiz dieser Leveler-Bauart.

Seit v0.6.0 wählt ein **Colour**-Schalter die Ära der Zelle: **Classic** (der Default — die
Fotozellen-Kalibrierung exakt wie bisher), **Quick** (ein späteres Voicing aus der
Solid-State-Ära der Optokoppler: schnellere Erholung, deutlich weniger Release-Memory, eine
fast saubere Ausgangsstufe) und **Deep** (ein Voicing früherer Ära: langsamere Erholung, ein
längerer Memory-Ausklang und eine dickere Röhren-/Übertrager-Ausgangsstufe). Der Schalter
ändert die Ladungsträger-Kinetik der Zelle, nicht ihre Pegelkalibrierung — alle drei landen bei
derselben Peak-Reduction-Einstellung in derselben Gain-Reduction-Klasse, und ein Wechsel der
Colour mitten in der laufenden Performance ist klickfrei.

Das LF-Boost-und-Cut-Netzwerk ist ebenfalls jetzt die exakte Antwort der Hardware-Leiter. Zwei
praktische Konsequenzen: Boost und Cut gemeinsam zu fahren ergibt die klassische Low-End-Form
(eine Anhebung darunter mit einer Senke knapp darüber), weil die Cut-Eckfrequenz tatsächlich
über der Boost-Eckfrequenz liegt, und der Cut für sich ist breit — bei voller Absenkung auf
der 100-Hz-Stellung liegt er bei 2 kHz immer noch rund 1,6 dB tief. Diese Breite gehört der
Schaltung, sie ist kein Bug; sie ist der Grund, warum der Regler normalerweise gegen den Boost
statt allein eingesetzt wird.

### ③ SPREAD — Dual-Micro-Pitch

Zwei kurze Delay-Taps (~30 ms hochgepitcht, ~50 ms runtergepitcht), hart nach L/R gepannt. **Detune** setzt den Pitch-Offset in Cents (Default 6 — bewusst klein, damit das Ohr „nach außen geschoben" liest statt Chorus). **Time** skaliert beide Basis-Delays gemeinsam; **Width** blendet von einer vollständig mittigen Summe (0 %) zum vollen harten Pan (100 %).

Seit v0.5.0 werden beide Shifter-Delay-Lines mit Lagrange-Interpolation 3. Ordnung statt eines linearen Reads ausgelesen, was 0,90 dB Höhenanteil bei 10 kHz zurückholt, den der lineare Read verlor; die Grain-Überblendung ist länger und equal-power, was das periodische Pegel-Ripple auf gehaltenen Tönen messbar senkt; und Detune sowie Time werden per Sample geglättet, sodass eine Automation von beiden nicht mehr an Block-Grenzen springt.

Seit v0.6.0 ist die Verbindung periodenadaptiv: Ein Pitch-Tracker (Autokorrelation auf einer
tiefpassgefilterten, dezimierten Kopie des Inputs — ein paar Prozent der CPU-Last des Busses)
beobachtet das Material, und sobald es sicher als tonal erkannt wird, rastet der Abstand
zwischen den beiden überblendenden Taps jedes Shifters auf ein Vielfaches der Notenperiode ein,
während das Überblendungsgesetz auf amplitudenkomplementär wechselt. Beide Taps verstärken sich
dann bei jeder Harmonischen gegenseitig, statt zu interferieren, was das notenabhängige
Pegel-Ripple beseitigt, auf das gehaltene Töne bisher trafen (siehe Bekannte Einschränkungen).
Nicht-tonales Material bleibt unterhalb des Confidence-Gates des Trackers und durchläuft exakt
denselben Pfad wie in v0.5.0. Der Tracker liest ausschließlich Signal-Historie — die gemeldete
Latenz bleibt bei 0.

Ebenfalls seit v0.6.0 bleibt die Überblendungs-Geometrie bei kurzen **Time**-Einstellungen
kausal: Unterhalb von 100 % schrumpft der Tap-Abstand mit dem Basis-Delay (bis auf ~15 ms bei
50 %), was die Verbindungs-Kadenz leicht beschleunigt. Zuvor konnte ein Tap teils sekundenlang
oder länger am unteren Anschlag der Delay-Line kleben bleiben und eine unverschobene Kopie des
Inputs in den Return durchsickern lassen.

### ④ SLAP — Single-Repeat Dark Delay

**Time** (50–160 ms, Default 110 ms, reine Millisekunden — bewusst nicht tempo-synchronisiert). Feedback ist in v2 fest auf 0: Es gibt genau eine Wiederholung, und ihre Dunkelheit kommt aus einer eingebauten Voicing im Tape-Stil (**Tone** fährt einen progressiven HF-Verlust plus sanfte Sättigung, fest in diese eine Wiederholung eingebacken) statt aus einer gefilterten Feedback-Loop. **Stereo** schaltet vom standardmäßigen Mono-Return (der klassische Mono-Slap hinter einer stereoverbreiterten Vocal) auf unabhängige L/R-Delays um.

Seit v0.5.0 ist die Wiederholung als tatsächliches Tape-Laufwerk gevoiced statt als gefiltertes
Delay: Die Sättigung sitzt jetzt auf der Aufnahmeseite (vor dem Delay-Schreibvorgang), statt auf
den Tap gelegt zu werden — weshalb Wiederholungen und Input nicht mehr gemeinsam aufhellen —,
und ein fester Head Bump ergänzt eine kleine Low-Mid-Anhebung.

**Wobble** (Default 0 %) ist Wow und Flutter des Laufwerks — ein langsames Andruckrollen-Wanken,
ein schnelleres Capstan-Flattern und ein langsames zufälliges Driften, jedes für sich wandernd,
sodass es sich nie in ein offensichtlich wiederkehrendes Muster einpendelt. Der Regler umfasst
etwa 0 bis 0,5 % Wow-and-Flutter; kleine Mengen (10–25 %) lesen sich als „das lief auf Tape",
ohne kaputt zu klingen, und hohe Einstellungen werden absichtlich seekrank. Bei 0 ist die
Modulation wirklich abgeschaltet, nicht nur heruntergedreht.

**Age** (Default 0 %) ist Bandverschleiß: Rauschen mit einer Asperity-Komponente, die auf dem
Signal mitreitet (dass das Rauschen mit der Vocal atmet, ist das meiste von dem, was es als Tape
statt als hinzugefügtes Rauschen lesbar macht), plus zusätzlicher Head-to-Tape-Spacing-Verlust,
der die Wiederholung mit steigendem Regler weiter abdunkelt. Es wirkt nur auf den SLAP-Return,
nie auf den Direct-Pfad. Bei 0 wird überhaupt nichts erzeugt.

## Fader-Logik

- Jeder Return-Bus hat **Level** (−60…+6 dB; der untere Anschlag ist ein echtes Off), **Mute** und **Audition**.
- **Audition ist exklusiv** (das Aktivieren eines Busses hebt die anderen auf) und isoliert exakt das, was der Name sagt — der Direct-Pfad und die übrigen Busse sind ausgeschlossen, solange ein Bus auditioniert wird. Es heißt bewusst nicht „Solo": Der ganze Sinn der Technik ist, dass diese Busse nie isoliert *beurteilt* werden sollten, sondern nur genutzt werden, um gegenzuprüfen, was sie gerade tun.
- **Mute gewinnt gegen Audition** auf demselben Bus, wie an einer Konsole.
- **Link** (standardmäßig aus) lässt die Detektoren von Crush und Sandwich einem kombinierten L/R-Signal folgen statt jedem Kanal unabhängig — „Dual Mono" (ungelinkt) ist das dokumentierte Standardverhalten für diesen Verarbeitungsstil.
- **Parallel** ist ein Makro-Trim (−24…+6 dB), der alle vier Return-Fader gemeinsam verschiebt — die „VCA-Ride-back"-Geste, um die gesamte Parallel-Ebene schnell zurückzunehmen.
- **Mute und Audition klicken nicht.** Seit v0.5.0 fährt das Bus-Routing auf einer 3-ms-Rampe statt hart zwischen an und aus umzuschalten. Die Rampe landet auf exakten Werten, ein gemuteter Bus liefert also weiterhin digitale Stille — exakte Nullen, nicht „sehr leise" —, sobald er sich eingeschwungen hat.

## Externer Sidechain (v0.7.0)

Miserere stellt einen optionalen **Sidechain**-Eingangsbus bereit, **standardmäßig
deaktiviert** — aktiviere ihn im Plugin-Routing deines Hosts und schalte dann einzelne
Detektoren mit der **Ext Key**-Lampe in den Panels Direct Path, Crush und Sandwich darauf um.
Es gibt keinen Hauptschalter: Jeder Detektor entscheidet für sich, sodass du CRUSH von einer
Snare aus keyen kannst, während SANDWICH weiter der Vocal zuhört. Fehlt der Bus, ist er
deaktiviert, oder sendet der Host keinen Key, fällt jeder Schalter stillschweigend auf interne
Erkennung zurück. Ein Mono-Key, der eine Stereo-Instanz speist, keyt beide Kanäle.

**Was Keying mit CRUSH und SANDWICH tatsächlich macht — lies das, bevor du annimmst, es sei
„derselbe Sound, nur eine andere Detektor-Quelle".** Beide Busse sind *Feedback*-Designs, und
das ist kein Implementierungsdetail, sondern die Quelle ihres Charakters:

- **CRUSH** treibt seinen Gleichrichter aus seinem eigenen Output, ein Sample zurückversetzt.
  Der Soft-Knee, die mit gehaltener Note kriechend steigende Ratio, das programmabhängige
  Release — all das entsteht aus dieser Schleife.
- Der Opto Leveler von **SANDWICH** treibt sein EL-Panel aus seinem eigenen komprimierten
  Output, aus demselben Grund: Im Code gibt es überhaupt kein Nachschlagen einer statischen
  Kurve, die Kurve *ist* die Schleife.

Ein externer Key fügt diesen Schleifen keinen zusätzlichen Detektor-Eingang hinzu. Er
**ersetzt die Schleifenspeisung**, was beide Module für die gesamte Dauer, in der Ext Key
aktiviert ist, in **gekeyte Feedforward-Kompressoren** verwandelt. Die Fotozellen-Physik, die
Ballistik und die Colour-Stufen bleiben unverändert, aber die statische Kurve nicht: Ein
Feedback-Detektor sieht das bereits reduzierte Signal und nimmt sich selbst zurück, während ein
Feedforward-Detektor den Key bei Vollaussteuerung sieht und dies nicht tut. Gemessen am selben
Signal mit denselben Einstellungen (ein −22-dBFS-Ton, 0 dB Input) erzeugt CRUSH mit interner
Erkennung etwa **3 dB** Gain Reduction und etwa **21 dB**, wenn es mit einer Kopie seines
eigenen Inputs gekeyt wird. Das ist ein legitimer und nützlicher Modus — es ist schlicht ein
anderer Kompressor, und wer erwartet, dass die Einstellungen der internen Erkennung
unverändert übernommen werden können, wird überrascht.

**Der Direct FET ist die Ausnahme**: Er war schon immer feedforward (seine Hüllkurve kommt aus
dem Pre-Gain-Input), daher ist das Keyen bei ihm wirklich nur ein reiner Wechsel der
Detektor-Quelle — gleiche Topologie, gleiche Kurve, andere Quelle.

Der Key wird nur gelesen. Er erreicht niemals den Audiopfad, ist nicht Teil der Summe und
beeinträchtigt die Null-Latenz-Garantie nicht.

## Output-Limiter (v0.7.0)

Die letzte Stufe im Plugin, nach Out Trim, mit eigenem Nadelmeter im Global-Panel.
**Standardmäßig aus**, und solange er aus ist, ist er ein bit-exakter Bypass — der Draht bleibt
im Default ein Draht.

- **Limiter** aktiviert ihn. **Ceiling** (−12…0 dB, Default −0,3 dB) ist der Pegel, den kein
  Output-Sample überschreiten darf. **Release** (5…500 ms, Default 60 ms) bestimmt, wie schnell
  sich die Gain erholt, nachdem der Peak vorüber ist.
- Er ist eine **Sicherheitsstufe, kein Colour-Werkzeug**. Attack ist instantan (in diesem
  Plugin gibt es nirgendwo Lookahead), sodass tiefe, anhaltende Reduktion auf basslastigem
  Material eher als Verzerrung hörbar wird, bevor sie als Pegelkontrolle hörbar wird. Nutze ihn,
  um Peaks abzufangen, nicht um einen Mix plattzudrücken.
- Die Detektion ist **immer L/R-gelinkt**, unabhängig vom globalen **Link**-Schalter. Link
  wählt bei CRUSH und SANDWICH zwischen Dual-Mono- und gelinkter Detektion, wo Dual Mono Teil
  des Sounds ist; würde man jeden Kanal mit seinem eigenen Gain limitieren, verschöbe das bei
  jedem Peak das Stereobild — deshalb bietet der Limiter diese Option nicht.
- Sobald das Signal den Soft-Knee des Ceiling (3 dB breit, zentriert auf das Ceiling) verlassen
  hat, kehrt die Gain exakt auf Unity zurück, und die Stufe ist wieder bit-transparent.

**Das ist ein Sample-Peak-Ceiling, kein True-Peak-Ceiling — und das kann es bewusst nicht
sein.** True-Peak-Limiting bedeutet, die rekonstruierte Wellenform *zwischen* den Samples zu
erkennen, was oversampelte Detektion erfordert, deren Filter Verzögerungen sind; ihr Urteil zu
befolgen bedeutet, das Audio um diese Verzögerung zurückzuhalten, also Lookahead. Die
Null-Latenz-Garantie (siehe unten) schließt das aus. Was der Limiter garantiert, ist, dass kein
Output-*Sample* das Ceiling überschreitet; die analoge Wellenform, die dein Wandler zwischen
diesen Samples rekonstruiert, kann es dennoch.

Gemessen mit einer 8×-Windowed-Sinc-Rekonstruktion (`tests/OutputLimiterTests.cpp`, wo diese
Werte als Regressionswerte eingefroren sind), bei einem −0,3-dB-Ceiling:

| Programm-Material | Inter-Sample-Overshoot über dem Ceiling |
|---|---|
| 11,025-kHz-Ton bei 44,1 kHz, phasenverschoben, sodass jedes Sample einen Wellenscheitel flankiert (der analytische Worst Case für einen Sinus) | **3,01 dB** |
| 11-kHz-Ton, beliebige Phase | **0,71 dB** |
| 1-kHz-Ton, 5 ms Release | **0,06 dB** |

In der Praxis: Bei echtem Programm-Material liegt der Overshoot bei einem Bruchteil eines dB,
und der 3-dB-Wert ist die mathematische Obergrenze dessen, was ein Sinus zwischen Samples
verstecken kann, kein typisches Ergebnis. Lieferst du nach einer Spezifikation, die ein
True-Peak-Limit vorschreibt (zum Beispiel −1 dBTP für verlustbehaftete Kodierung), setze
Ceiling mit dieser Reserve — oder nutze einen True-Peak-Limiter am Ende deiner Mastering-Kette,
wo dessen Latenz nichts kostet.

## Presets

Am oberen Rand des Editors sitzt eine Preset-Leiste: `[<] [Preset-Name*] [>] [Save] [Save As...] [Delete] [Import...] [Export...]`. Ein Klick auf den Preset-Namen öffnet ein Factory/User-Menü; ein angehängtes `*` bedeutet, dass das aktuelle Preset ungespeicherte Änderungen hat. Dreizehn Werkspresets sind ab Werk dabei (was jedes einzelne bewirkt, steht in `presets.md`) — einschließlich **Tape Slap 7.5** und **Worn Slap**, die in v0.5.0 hinzukamen, um Wobble und Age vorzuführen, sowie **BV Mode**, ein Startpunkt für Background-/Stacked-Vocals, bei dem jeder Return stärker aufgedreht ist als in der Lead-Vorlage; eigene Presets speichert Miserere unter `~/Library/Audio/Presets/Yves Vogl/Miserere/` auf macOS (`%APPDATA%/Yves Vogl/Miserere/Presets/` unter Windows). „Set current as default" im Preset-Menü macht ein beliebiges Preset — Werks- oder eigenes — zu dem, das auf jeder frischen Instanz automatisch geladen wird; „Import..." akzeptiert sowohl einzelne Preset-Dateien als auch Zip-Preset-Bänke.

## Starter-Rezept

1. Lass den Direct-Pfad aus, oder ergänze De-Ess Pre / einen Hauch Console EQ, falls die Quelle es braucht. Lass FET Comp und Sat aus, außer die Vocal braucht ausdrücklich leichte Insert-Kompression.
2. CRUSH startet standardmäßig bei −9 dB, mit dem ALL-Buttons-Charakter bereits aktiviert — dreh Input auf, bis Audition schwere, „solo eine Katastrophe" klingende Kompression zeigt, vertrau dann dem Default-Fader-Pegel und justiere von dort aus nach Gehör.
3. SANDWICH startet bei −12 dB; erhöhe Peak Reduction, bis die Vocal dicker wird, ohne im Kontext hörbar zu pumpen.
4. SPREAD und SLAP (standardmäßig −18 dB / −15 dB) sollten beide den „du merkst erst, dass es weg ist, wenn du es mutest"-Test bestehen — ist eines der beiden als eigenständiger Effekt hörbar, nimm es zurück.
5. Nutze **Parallel**, um bei leiserem/organischerem Material die gesamte Ebene schnell zurückzunehmen.

## Latenz und Aliasing (v0.5.0)

Miserere meldet und fügt **0 Samples Latenz** hinzu, bei jeder Samplerate und mit jedem
aktivierten Abschnitt. Das ist eine bewusste Randbedingung und kein Versäumnis: Die vier
Return-Busse werden gegen einen bit-transparenten Direct-Pfad summiert, alles, was einen Bus
auch nur um den Bruchteil eines Samples verzögerte, würde die Summe kammfiltern.

Dieses Versprechen zu halten schließt Oversampling aus, mit dem die meisten Plugins das von
Sättigung erzeugte Aliasing zähmen. Stattdessen berechnet hier jede Drive-Stufe ihre Verzerrung
in einer Form, die Aliasing arithmetisch unterdrückt, so aufgeteilt, dass der saubere Anteil des
Signals exakt ausgerichtet und unangetastet hindurchläuft — keine Verzögerung und keine
Höhendämpfung bei 44,1 kHz.

Was das bringt, gemessen bei 44,1 kHz: Auf einer programmrealistischen Probe (ein 3-kHz-Ton bei
−12 dBFS durch heiße, aber musikalische Drive-Einstellungen) liegen nicht-harmonische Anteile
bei oder unter −60 dBFS. In bewusst unrealistische Extreme getrieben — ein 12-kHz-Ton bei
Vollaussteuerung in maximalen Drive — entfernt die Behandlung weiterhin mindestens 12 dB
Aliasing gegenüber der unbehandelten Kurve, aber dort wird kein absoluter Teppich behauptet, und
du solltest das von keinem Zero-Latency-Design erwarten. Willst du, dass ein gesättigter
12-kHz-Sinus bei Vollaussteuerung sauber bleibt, ist dafür Oversampling da, und es kostet Latenz.

## Bekannte Einschränkungen

- Der Pitch-Shifter von SPREAD überblendet zwei Taps einer Delay-Linie. Seit v0.6.0 hört der
  Tap-Abstand auf den Input: Bei sicher tonalem Material (ein gehaltener Vokal, ein Synth)
  rastet er auf ein Vielfaches der Notenperiode ein, sodass sich die Taps verstärken, statt vom
  Zufall des Kammfilters abzuhängen — gehaltene Töne, die zuvor auf einen notenabhängigen Kamm
  mit bis zu ~18 dB Hüllkurven-Ripple trafen, bleiben jetzt bei jeder Tonhöhe innerhalb von
  ~2 dB. Bei nicht-tonalem Material (Konsonanten, Atem, Rauschen) zieht sich der Detektor
  zurück, und der Bus verhält sich exakt wie zuvor. Verbleibende Grenzen: Der Tracker folgt der
  tiefsten Grundfrequenz bis hinunter zu 80 Hz; die Neuausrichtung dauert nach dem Einsetzen
  einer Note etwa eine Sekunde (bei sehr tiefen Noten länger, sodass sehr kurze Noten
  größtenteils auf dem Standardpfad reiten), und schnelles Vibrato kann ihn überholen — eine
  kurze Rückkehr des alten, milden Schimmerns, das sich als natürliches Doubling liest.
  Unterhalb von Time 100 % übersteuert die kausale Begrenzung des Tap-Abstands zunehmend den
  periodenausgerichteten Abstand (zuerst bei der Up-Stimme), sodass der Schutz für gehaltene
  Töne mit sinkendem Time-Wert Richtung v0.5.0-Verhalten zurückschwindet — bei ~60 % Time ist er
  praktisch aus. Was bei keiner Time-Einstellung mehr passieren kann, ist das Dry-Leck von vor
  v0.6.0, bei dem ein Tap am unteren Anschlag der Delay-Line festhing.
- Das GUI ist der individuelle Vektor-Editor aus Milestone M3: ein Faceplate-Panel pro Bus mit
  Zeiger-Reglern, gravierten Skalenringen und Gain-Reduction-Nadelmetern pro Bus (Direct FET,
  CRUSH, SANDWICH), vollständig per Tastatur bedienbar (Pfeiltasten/Shift+Pfeiltasten/Bild
  auf/Bild ab/Pos1/Ende, Shift-Drag für feine Mausjustierung) und screenreader-zugänglich
  (Gruppierung pro Bus, einheitensuffixierte Werte). Die finale manuelle VoiceOver-Verifikation
  wird im a11y-Issue nachverfolgt.
- Der Output-Limiter (v0.7.0) erzwingt ein **Sample-Peak**-Ceiling, kein True-Peak-Ceiling, und
  kann kein True-Peak-Ceiling erzwingen, ohne die Null-Latenz-Garantie zu brechen — siehe die
  gemessene Inter-Sample-Overshoot-Tabelle im Abschnitt Output-Limiter oben.
- Das Keyen von CRUSH oder SANDWICH über den externen Sidechain wandelt sie von Feedback- in
  Feedforward-Kompressoren um, mit einer messbar anderen statischen Kurve — siehe den Abschnitt
  Externer Sidechain oben. Das liegt in der Natur des Keyens einer Feedback-Topologie und lässt
  sich nicht wegtunen.
- Außerhalb des Scopes von v2, als M2+/M3-Issue erfasst: ein kurzes Plate-Reverb-Modul.
  (Austauschbare Kompressor-Farben pro Dynamik-Slot sind bereits mit v0.6.0 erschienen — der
  **Character**-Schalter des Direct FET, der dritte **Style** von CRUSH und der
  **Colour**-Schalter von SANDWICH weiter oben; der Output-Limiter, das BV-Mode-Preset und der
  externe Sidechain sind mit v0.7.0 hinzugekommen.)
- Die Dynamikerkennung ist bei Crush und Sandwich standardmäßig ungelinkt (unabhängiges L/R); Link lässt beide Kanäle einem gemeinsamen Detektor folgen.
- Das Voicing ist im gesamten Plugin **recherchebasiert, nicht gegen Hardware-Einheiten gemessen** — die belegten Erkenntnisse und ihre Grenzen findest du in `research-notes.md`.
