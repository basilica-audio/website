<!-- German translation of miserere.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

# Miserere — Bedienungsanleitung (v0.5.0)

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
   Σ (direct + returns) → [Parallel macro trim scales returns ①–④] → [Out Trim] → out
```

Die Busse ①/② sind minimalphasig und fügen keine Latenz hinzu, bleiben also sample-genau zum Direct-Pfad ausgerichtet — paralleles Summieren kammfiltert nie, unabhängig von den Einstellungen. Die Busse ③/④ sind by Design Delays (siehe `architecture.md`). Die belegten Erkenntnisse hinter jedem Default unten findest du in `research-notes.md`.

## Der Direct-Pfad

Standardmäßig aus, Sektion für Sektion, in Signalreihenfolge:

- **De-Ess Pre** — Split-Band-De-Esser, 4–9 kHz einstellbar, bis zu 10 dB Reduktion, platziert dort, wo die Dynamik der Vocal am größten ist (die dokumentierte „de-esse ganz am Anfang"-Regel).
- **FET Comp** — ein leichter, threshold-basierter Kompressor im FET-Stil, fest bei 4:1, ausgelegt auf sanfte 3–4 dB Peak Gain Reduction — „die einzige Stelle, an der serielle Kompression authentisch ist" in dieser Topologie.
- **Console EQ** — ein Raster im Stil britischer Konsolen-EQs: HPF (18 dB/oct, 50/80/160/300 Hz), Low Shelf (±16 dB, 35/60/110/220 Hz), eine Mid Bell mit fixem Q (±18 dB, sechs gestufte Mittenfrequenzen), ein fixer 12-kHz-High-Shelf (±16 dB) und ein Drive-Regler, der dezente, Richtung 2./3. Ordnung tendierende Transformer-artige Harmonische beimischt.

  Seit v0.5.0 ist Drive ein Übertrager-Modell statt eines addierten Harmonischen-Terms: Das Signal läuft durch einen Fluss-Integrator in einen gebiasten Sättiger und zurück durch die exakte Inverse dieses Integrators. Weil magnetischer Fluss als Spannung geteilt durch Frequenz skaliert, steigt die dritte Harmonische zum Bassbereich hin von selbst an (gemessen +12 dB beim Übergang von 100 Hz zu 50 Hz), statt von Hand gewichtet zu werden. Bei 0 dB ist Drive ein bit-exakter Bypass. Der 12-kHz-Shelf ist seit v0.5.0 ebenfalls magnitude-matched, sodass er bei 44,1 kHz seine analoge Form in der obersten Oktave behält, statt Richtung Nyquist gequetscht zu werden.
- **Sat** — der aus v1 übernommene Sättiger im Tape-Stil, eine optionale „Grit"-Stufe. Seit v0.5.0 berechnet er seine Distortion in der Alias-unterdrückenden Form, die unter *Latenz und Aliasing* weiter unten beschrieben ist; bei 0 dB Drive ist er weiterhin ein bit-exakter Bypass.
- **De-Ess Post** — eine zweite De-Esser-Instanz am Ende der Kette, für Zischlaute, die Kompression oder EQ hervorgehoben haben.

## Die vier Return-Busse

### ① CRUSH — FET-Limiter, All-Buttons-Charakter

Kein Threshold-Regler: **Input** treibt das Signal in einen fixen, ratio-abhängigen Threshold und Knee. **Ratio** wählt 4:1/8:1/12:1/20:1/ALL (ALL ist eine plateauförmige Kurve mit bewusstem Give-back und einer kurzen Attack-Verzögerung, die Transienten durchschlagen lässt, bevor geklemmt wird — der „Snap"). **Attack**/**Release** sind 1–7-Regler, bei denen eine HÖHERE Zahl SCHNELLER bedeutet, passend zur Hardware-Konvention, an der sich das orientiert; Release ist programmabhängig (schnell nach kurzen Transienten, mehrfach langsamer nach anhaltend starker Kompression). **Style** schaltet zwischen All-Buttons und einer weicheren, fixen 2:1-**Gentle**-Voicing um. Dieser Bus soll solo „furchtbar" klingen (nutze Audition) und im Mix gut.

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

## Presets

Am oberen Rand des Editors sitzt eine Preset-Leiste: `[<] [Preset-Name*] [>] [Save] [Save As...] [Delete] [Import...] [Export...]`. Ein Klick auf den Preset-Namen öffnet ein Factory/User-Menü; ein angehängtes `*` bedeutet, dass das aktuelle Preset ungespeicherte Änderungen hat. Zwölf Werkspresets sind ab Werk dabei (was jedes einzelne bewirkt, steht in `presets.md`) — einschließlich **Tape Slap 7.5** und **Worn Slap**, die in v0.5.0 hinzukamen, um Wobble und Age vorzuführen; eigene Presets speichert Miserere unter `~/Library/Audio/Presets/Yves Vogl/Miserere/` auf macOS (`%APPDATA%/Yves Vogl/Miserere/Presets/` unter Windows). „Set current as default" im Preset-Menü macht ein beliebiges Preset — Werks- oder eigenes — zu dem, das auf jeder frischen Instanz automatisch geladen wird; „Import..." akzeptiert sowohl einzelne Preset-Dateien als auch Zip-Preset-Bänke.

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

- Der Pitch-Shifter von SPREAD blendet zwei Taps einer Delay-Linie über, die in festem Abstand
  zueinander gehalten werden, weshalb ein getragener reiner Ton (ein Synth oder ein sehr
  gleichmäßig gehaltener Vokal) auf einen milden Kamm trifft, dessen Tiefe von der Note abhängt.
  Bei echtem Programmmaterial ist das unhörbar; eine intelligentere Verbindung steht auf der
  Roadmap.
- Das GUI ist ein funktionaler Slider-/Knob-Editor (ein individuelles Vektor-GUI mit Nadelinstrumenten pro Bus ist Milestone M3); die Preset-Leiste ist ein rein funktionaler Streifen, noch nicht neu gestaltet.
- Außerhalb des Scopes von v2, als M2+/M3-Issues erfasst: ein kurzes Plate-Reverb-Modul, ein „BV Mode"-Preset, austauschbare Kompressor-Farben über die beiden CRUSH-Styles hinaus, externer Sidechain, ein Output-Limiter.
- Die Dynamikerkennung ist bei Crush und Sandwich standardmäßig ungelinkt (unabhängiges L/R); Link lässt beide Kanäle einem gemeinsamen Detektor folgen.
- Das Voicing ist im gesamten Plugin **recherchebasiert, nicht gegen Hardware-Einheiten gemessen** — die belegten Erkenntnisse und ihre Grenzen findest du in `research-notes.md`.
