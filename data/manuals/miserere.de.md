<!-- German translation of miserere.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

# Miserere — Bedienungsanleitung (v0.3.0)

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
- **Console EQ** — ein Raster im Stil der 1073-Klasse: HPF (18 dB/oct, 50/80/160/300 Hz), Low Shelf (±16 dB, 35/60/110/220 Hz), eine Mid Bell mit fixem Q (±18 dB, sechs gestufte Mittenfrequenzen), ein fixer 12-kHz-High-Shelf (±16 dB) und ein Drive-Regler, der dezente, Richtung 2./3. Ordnung tendierende Transformer-artige Harmonische beimischt.
- **Sat** — der aus v1 übernommene Sättiger im Tape-Stil, eine optionale „Grit"-Stufe.
- **De-Ess Post** — eine zweite De-Esser-Instanz am Ende der Kette, für Zischlaute, die Kompression oder EQ hervorgehoben haben.

## Die vier Return-Busse

### ① CRUSH — FET-Limiter, All-Buttons-Charakter

Kein Threshold-Regler: **Input** treibt das Signal in eine fixe, ratio-abhängige Threshold-/Knee-Tabelle. **Ratio** wählt 4:1/8:1/12:1/20:1/ALL (ALL ist eine plateauförmige Kurve mit bewusstem Give-back und einer kurzen Attack-Verzögerung, die Transienten durchschlagen lässt, bevor geklemmt wird — der „Snap"). **Attack**/**Release** sind 1–7-Regler, bei denen eine HÖHERE Zahl SCHNELLER bedeutet, passend zur Hardware-Konvention, an der sich das orientiert; Release ist zweistufig und programmabhängig (schnell nach kurzen Transienten, mehrfach langsamer nach anhaltend starker Kompression). **Style** schaltet zwischen All-Buttons und einer weicheren, fixen 2:1-**Gentle**-Voicing um. Dieser Bus soll solo „furchtbar" klingen (nutze Audition) und im Mix gut.

### ② SANDWICH — Passive EQ → Opto Leveler → Passive EQ

Zwei unabhängige Passive-EQ-Instanzen klammern einen Leveler im Opto-Stil ein. Jeder Passive EQ bietet einen gemeinsam-frequenten LF-**Boost** und -**Cut** (beide können gleichzeitig laufen — eine bewusst nicht-kompensierende Kurve, keine simple Summe auf Flat), einen HF-**Bell Boost** mit variabler Bandbreite und ein HF-**Shelf Atten**. Der Opto Leveler hat keinen Threshold: **Peak Reduction** treibt in eine fixe statische Kurve (weich ~3:1 unterhalb −20 dB, harte Decke darüber; **Limit** strafft den weichen Bereich Richtung ~10:1), mit einem Rohsignal-Detektor (kein Smoothing vor der Ballistik) und einem zweistufigen Release, dessen Ausklang sich verlängert, je länger er schon arbeitet. **Emphasis** macht den Detektor zunehmend HF-selektiv (bis zu −10 dB geringere LF-Empfindlichkeit), sodass er bei hohen Einstellungen hauptsächlich auf Zischlaute/Presence reagiert, „wie ein Multiband". **Residual** (standardmäßig an) behält den kleinen, nie ganz flachen Vintage-Tilt des Passive EQ; deaktiviere es für einen saubereren EQ.

### ③ SPREAD — Dual-Micro-Pitch

Zwei kurze Delay-Taps (~30 ms hochgepitcht, ~50 ms runtergepitcht), hart nach L/R gepannt. **Detune** setzt den Pitch-Offset in Cents (Default 6 — bewusst klein, damit das Ohr „nach außen geschoben" liest statt Chorus). **Time** skaliert beide Basis-Delays gemeinsam; **Width** blendet von einer vollständig mittigen Summe (0 %) zum vollen harten Pan (100 %).

### ④ SLAP — Single-Repeat Dark Delay

**Time** (50–160 ms, Default 110 ms, reine Millisekunden — bewusst nicht tempo-synchronisiert). Feedback ist in v2 fest auf 0: Es gibt genau eine Wiederholung, und ihre Dunkelheit kommt aus einer eingebauten Voicing im Bucket-Brigade-Stil (**Tone** fährt einen progressiven HF-Verlust plus sanfte Sättigung, fest in diese eine Wiederholung eingebacken) statt aus einer gefilterten Feedback-Loop. **Stereo** schaltet vom standardmäßigen Mono-Return (der klassische Mono-Slap hinter einer stereoverbreiterten Vocal) auf unabhängige L/R-Delays um.

## Fader-Logik

- Jeder Return-Bus hat **Level** (−60…+6 dB; der untere Anschlag ist ein echtes Off), **Mute** und **Audition**.
- **Audition ist exklusiv** (das Aktivieren eines Busses hebt die anderen auf) und isoliert exakt das, was der Name sagt — der Direct-Pfad und die übrigen Busse sind ausgeschlossen, solange ein Bus auditioniert wird. Es heißt bewusst nicht „Solo": Der ganze Sinn der Technik ist, dass diese Busse nie isoliert *beurteilt* werden sollten, sondern nur genutzt werden, um gegenzuprüfen, was sie gerade tun.
- **Mute gewinnt gegen Audition** auf demselben Bus, wie an einer Konsole.
- **Link** (standardmäßig aus) lässt die Detektoren von Crush und Sandwich einem kombinierten L/R-Signal folgen statt jedem Kanal unabhängig — „Dual Mono" (ungelinkt) ist das dokumentierte Standardverhalten für diesen Verarbeitungsstil.
- **Parallel** ist ein Makro-Trim (−24…+6 dB), der alle vier Return-Fader gemeinsam verschiebt — die „VCA-Ride-back"-Geste, um die gesamte Parallel-Ebene schnell zurückzunehmen.

## Presets

Am oberen Rand des Editors sitzt eine Preset-Leiste: `[<] [Preset-Name*] [>] [Save] [Save As...] [Delete] [Import...] [Export...]`. Ein Klick auf den Preset-Namen öffnet ein Factory/User-Menü; ein angehängtes `*` bedeutet, dass das aktuelle Preset ungespeicherte Änderungen hat. Zehn Werkspresets sind ab Werk dabei (was jedes einzelne bewirkt, steht in `presets.md`); eigene Presets speichert Miserere unter `~/Library/Audio/Presets/Yves Vogl/Miserere/` auf macOS (`%APPDATA%/Yves Vogl/Miserere/Presets/` unter Windows). „Set current as default" im Preset-Menü macht ein beliebiges Preset — Werks- oder eigenes — zu dem, das auf jeder frischen Instanz automatisch geladen wird; „Import..." akzeptiert sowohl einzelne Preset-Dateien als auch Zip-Preset-Bänke.

## Starter-Rezept

1. Lass den Direct-Pfad aus, oder ergänze De-Ess Pre / einen Hauch Console EQ, falls die Quelle es braucht. Lass FET Comp und Sat aus, außer die Vocal braucht ausdrücklich leichte Insert-Kompression.
2. CRUSH startet standardmäßig bei −9 dB, mit dem ALL-Buttons-Charakter bereits aktiviert — dreh Input auf, bis Audition schwere, „solo eine Katastrophe" klingende Kompression zeigt, vertrau dann dem Default-Fader-Pegel und justiere von dort aus nach Gehör.
3. SANDWICH startet bei −12 dB; erhöhe Peak Reduction, bis die Vocal dicker wird, ohne im Kontext hörbar zu pumpen.
4. SPREAD und SLAP (standardmäßig −18 dB / −15 dB) sollten beide den „du merkst erst, dass es weg ist, wenn du es mutest"-Test bestehen — ist eines der beiden als eigenständiger Effekt hörbar, nimm es zurück.
5. Nutze **Parallel**, um bei leiserem/organischerem Material die gesamte Ebene schnell zurückzunehmen.

## Bekannte Einschränkungen (v0.3.0)

- Das GUI ist ein funktionaler Slider-/Knob-Editor (ein individuelles Vektor-GUI mit Nadelinstrumenten pro Bus ist Milestone M3); die Preset-Leiste ist ein rein funktionaler Streifen, noch nicht neu gestaltet.
- Außerhalb des Scopes von v2, als M2+/M3-Issues erfasst: ein kurzes Plate-Reverb-Modul, ein „BV Mode"-Preset, austauschbare Kompressor-Farben über die beiden CRUSH-Styles hinaus, externer Sidechain, ein Output-Limiter.
- Die Dynamikerkennung ist bei Crush und Sandwich standardmäßig ungelinkt (unabhängiges L/R); Link lässt beide Kanäle einem gemeinsamen Detektor folgen.
- Das Voicing ist im gesamten Plugin **recherchebasiert, nicht gegen Hardware-Einheiten gemessen** — die belegten Erkenntnisse und ihre Grenzen findest du in `research-notes.md`.
