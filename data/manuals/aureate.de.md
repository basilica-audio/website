<!-- German translation of aureate.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Aureate-Icon" width="120"/></p>

# Aureate — Bedienungsanleitung

## Was Aureate ist

Aureate ist ein Tape-/Console-Saturation-„Glue"-Plugin für orchestrales Material — Streicher, Blechbläser und geschichtete/gebusste Spuren, die Kohäsion und einen Hauch analoger Wärme brauchen, ohne wie ein Gitarrenpedal zu klingen. Es kombiniert einen 4x-oversampelten, im Charakter wählbaren Saturator (tanh-basiertes Tape, Soft-Knee-Console oder exponentielle Valve) mit Tape-Transport-Artefakten (unabhängiges Wow/Flutter, ein LF-Head-Bump, HF-lastiges Hiss) und einem Dual-Shelf-Tilt-Tone-Regler plus unabhängigen HF-/LF-Trim-Shelves.

**v0.2.0** ist eine recherchebasierte Überarbeitung des Saturation-Kerns — die vollständige Begründung (was sich geändert hat und warum) findest du in `docs/design-brief.md`, die zugehörigen Quellenangaben in `docs/research-notes.md`. Nichts hier ist an gemessener Hardware kalibriert; jeder Standardwert ist entweder aus v0.1 übernommen oder so gewählt, dass er innerhalb einer belegten Bandbreite/Reihenfolge aus der Literatur liegt — siehe dazu den eigenen Honesty-Abschnitt des Briefs.

## Wo es in einer Heavy-Music-Produktionskette sitzt

Aureate ist dafür gedacht, **nachdem** die einzelnen Layer eines orchestralen/chorischen Stacks (Streicher, Blechbläser, Chor usw.) ausbalanciert wurden, zu laufen, typischerweise auf:

- Einem **Streicher- oder Blechbläser-Bus**, um eine Divisi-Sektion so zu verkleben, wie Tape-/Console-Summing das auf natürliche Weise tut — ein wenig Drive und Warmth, moderater Mix, und die Sektion liest sich als ein Instrument statt als Haufen Nahmikrofonierungen.
- Einem **orchestralen/chorischen Submix-Bus**, der nach den einzelnen Sektionen und vor dem finalen Mix-Bus sitzt, um Kohäsion hinzuzufügen, bevor das orchestrale Material auf die Metal-Instrumentierung (Gitarren, Drums, Bass) trifft.
- Dem **Mix-Bus** selbst (sparsam — niedriger Drive, Mix deutlich unter 100 %), als subtiler „Master-Glue"-Durchgang, in derselben Rolle, die eine Tape-Maschine oder ein Console-Summing-Bus in einem hybriden Analog-/ITB-Workflow spielen würde.

Es ist kein Distortion- oder Amp-Sim-Plugin (diese Rolle übernehmen `overture`/`tenebrae` an anderer Stelle der Suite) — Drive ist bewusst auf moderate 24 dB gedeckelt, und die Standard-Warmth-/Character-Einstellungen bleiben deutlich im Bereich „fügt Fülle hinzu", nicht „fügt Grit hinzu".

## Signalfluss

```
input -> Wow/Flutter (independent wow + flutter) -> Drive
      -> [4x oversampled: Warmth HF-rolloff -> LF head bump -> saturator (Character:
         Tape/Console/Valve, Warmth+Bias-driven asymmetry) -> Tone tilt -> HF/LF Trim
         -> Hiss (HF-forward)]
      -> downsample -> Dry/Wet Mix -> Output trim -> output
```

Wow/Flutter und Drive laufen mit der Host-Samplerate; alles vom Warmth-Low-Pass bis Hiss läuft innerhalb der 4x-oversampelten Domäne, sodass die Harmonischen des Saturators (und das Rauschen von Hiss) mit dem 4-fachen der Host-Rate erzeugt und gefiltert werden, bevor ein einzelner Downsample-Schritt erfolgt. Mix mischt das prozessierte („wet") Signal zurück mit einer latenzkompensierten Kopie des unangetasteten Inputs, und Output ist ein finaler Trim, der auf das kombinierte Ergebnis angewendet wird. Die vollständige technische Aufschlüsselung, inklusive Latenz-Buchhaltung und Real-Time-Safety-Notizen, findest du in [`docs/architecture.md`](architecture.md).

## Gain-Staging-Hinweis

Die Standardwerte von Drive/Warmth sind auf einen nominalen Eingangspegel von **-18 dBFS RMS** abgestimmt (die vielzitierte Tape-„0-VU"-Kalibrierungskonvention) — keine Messung von irgendetwas Aureate-Spezifischem, nur eine dokumentierte Annahme. Das erklärt, warum die standardmäßigen 6 dB Drive auf einem heißen, limitierten digitalen Bus ganz anders wirken als auf einem Bus mit konservativem Gain-Staging — und es ist der Bezugspunkt, an dem sich die Werkspresets für Drive/Output als aufeinander abgestimmtes Paar orientieren.

## Parameterreferenz

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Wow** | 0-100 | 0 | % | Menge der langsamen Tape-Transport-Tonhöhendrift (~0,7 Hz), angewendet über ein moduliertes Delay vor Drive. 0 % ist ein festes (unmoduliertes) Delay — ein echter Off-Zustand, nicht „sehr wenig". Unabhängig von Flutter (v0.2.0) — nutze Wow allein für eine langsame, „atmende" Tonhöheninstabilität ohne schnelleres Schimmern. |
| **Flutter** | 0-100 | 0 | % | Menge des schnelleren Tape-Transport-Tonhöhenschimmerns (~11 Hz), angewendet über dasselbe modulierte Delay. Unabhängig von Wow (v0.2.0) — nutze Flutter allein für einen schnelleren „Wobble"-/Schimmer-Charakter ohne langsame Drift. Nutze Wow und Flutter gemeinsam, sparsam eingesetzt (je 10-25 % pro Regler), für einen klassischen Vintage-Tape-Charakter auf gehaltenen Pads/Streichern; höhere Einstellungen sind ein offensichtlicher, bewusster Effekt. |
| **Drive** | 0-24 | 6 | dB | Gain in den Saturator hinein. Bewusst moderat gehalten — Aureate ist ein Glue-Prozessor, kein Distortion-Pedal. Höhere Einstellungen treiben die per Character gewählte Kurve stärker, was mehr harmonischen Inhalt und Kompression hinzufügt. |
| **Warmth** | 0-100 | 35 | % | Steuert drei Dinge über einen Regler, alle unterschiedlich stark je nach Character: den Asymmetrie-Bias des Saturators (single-ended, tape-artiger Charakter — die Bias-Obergrenze unterscheidet sich je Character, siehe unten), einen sanften Pre-Clip-Höhenabfall (Tape-Selbstlöschung/Bias-Oscillator-Verdunkelung) und eine sanfte LF-Head-Bump-Resonanz um 80 Hz (Tape-Transport-Kopfgeometrie, bis zu +1,5 dB). Höheres Warmth = asymmetrischere Saturation, ein dunkleres Top-End und ein Hauch mehr Low-End-Gewicht — der mit Abstand wichtigste „Charakter"-Regler des Plugins. |
| **Bias** | -100 to 100 | 0 | % | Ein zusätzlicher, unabhängiger Asymmetrie-Trim des Saturators, der zum eigenen Bias-Beitrag von Warmth hinzukommt. Nutze ihn, um die Asymmetrie weiter zu verschieben (oder in die Gegenrichtung), ohne die HF-Rolloff-/Head-Bump-Menge von Warmth anzutasten — nützlich, um die Balance zwischen ungeraden und geraden Harmonischen nach Geschmack einzustellen. |
| **Character** | Tape / Console / Valve | Tape | - | Wählt die Transferfunktions-Familie des Saturators, jede mit einem wirklich eigenständigen Profil der harmonischen Balance. **Tape**: sanftes, asymmetrisches tanh, von den dreien am stärksten von ungeraden Harmonischen dominiert und am wenigsten asymmetrisch (die Bias-Obergrenze von Warmth ist hier am niedrigsten) — der klassische, vergebende Tape-Glue-Sound. **Console**: eine asymmetrische Soft-Knee-Kurve (v0.2.0), die bei niedrigem bis moderatem Drive transparent bleibt und erst bei kräftigem Antreiben Charakter zeigt — der Archetyp „am wenigsten charaktervoll, bis sie gefordert wird", näher an einem Solid-State-/Transformer-Summing-Bus. **Valve**: eine asymmetrische, exponentielle Saturation-Kurve, von den dreien am stärksten asymmetrisch/am stärksten von geraden Harmonischen geprägt (die Bias-Obergrenze von Warmth ist hier am höchsten) — ein runderer, röhrenartiger Schub. |
| **Tone** | -100 to 100 | 0 | % | Ein Dual-Shelf-Tilt-EQ (zwei unabhängige Shelf-Eckpunkte, kein Lehrbuch-Tilt mit einem einzelnen Drehpunkt): negativ verdunkelt (Low Shelf hoch, High Shelf runter), positiv hellt auf (umgekehrt), 0 % ist flach/unity. Nutze dies für die grobe tonale Balance des gesamten prozessierten Signals. |
| **HF Trim** | -6 to 6 | 0 | dB | Ein High-Shelf-Trim mit fester Frequenz (8 kHz), unabhängig von Tone — eine feinere Top-End-Anpassung (Air hinzufügen oder Härte zähmen), nachdem der breitere Tone-Tilt die Gesamtbalance gesetzt hat. |
| **LF Trim** | -6 to 6 | 0 | dB | Ein Low-Shelf-Trim mit fester Frequenz (150 Hz), unabhängig von Tone — eine feinere Low-End-Anpassung (Gewicht hinzufügen oder Mud straffen) nach dem breiteren Tone-Tilt. |
| **Hiss** | 0-100 | 0 | % | Menge geformten Rauschens („Tape Hiss"), das in das prozessierte Signal gemischt wird, erzeugt innerhalb der oversampelten Domäne und geformt durch ein dediziertes, höhenlastiges Shelf-Filter (v0.2.0), sodass es sich wie breitbandiges Hiss anhört und nicht wie gedämpftes Rauschen. 0 % ist wirklich still (überhaupt kein Rauschteppich) — eine bewusste „Vintage"-Option für Material, das klingen soll, als käme es von einer Tape-Maschine, kein Mischpult-Artefakt, das standardmäßig aktiv bleiben sollte. |
| **Mix** | 0-100 | 100 | % | Dry/Wet-Mischung. Bei 0 % ist das Plugin ein sample-genauer (latenzkompensierter) Durchlauf des Inputs — nützlich für Parallel-/New-York-Style-Blending oder um zu bestätigen, dass Aureate ein Signal nicht einfärbt, wenn du es per A/B herausnehmen willst. |
| **Output** | -24 to 24 | 0 | dB | Finaler Output-Trim, angewendet *nach* der Dry/Wet-Mischung — anders als Drive (das nur den Wet-Pfad betrifft) skaliert Output das kombinierte Dry+Wet-Signal als Ganzes. Nutze ihn, um Pegeländerungen durch Drive/Warmth/Character auszugleichen, bevor das Signal weiter durch die Kette läuft. |

## Presets

Die Preset-Leiste am oberen Rand des Editors lässt dich durch Werks- und User-Presets browsen (`<` / Preset-Name / `>` zum Durchblättern, Klick auf den Namen öffnet das vollständige Menü), eigene Presets per Save/Save As/Delete verwalten, einzelne Presets oder Preset-Bänke als Zip importieren/exportieren und den aktuellen Zustand als eigenen Startup-Default setzen. In v0.2.0 sind elf Werkspresets an Bord — was jedes einzelne bewirkt, steht in `docs/presets.md`. Presets werden nutzerspezifisch gespeichert, unter `~/Library/Audio/Presets/Yves Vogl/Aureate/` auf macOS (`%APPDATA%/Yves Vogl/Aureate/Presets/` unter Windows).

## Upgrade von v0.1.x

v0.2.0 bringt zwei Breaking Changes für gespeicherte Automation/States mit sich — beide vor 1.0 ausdrücklich erlaubt: Der einzelne Parameter „Wow/Flutter" ist jetzt zwei unabhängige Parameter (Wow/Flutter), und die Warmth-getriebene Bias-Obergrenze jedes Character-Modells hat sich geändert (Tape und Console sind bei denselben Warmth-/Bias-Einstellungen jetzt weniger asymmetrisch als vorher; Valve ist unverändert). Eine mit v0.1.0 gespeicherte Session lädt weiterhin fehlerfrei — ihr alter Wow/Flutter-Wert wird auf die beiden neuen Parameter Wow und Flutter kopiert —, klingt nach dem Upgrade aber anders, falls du Warmth/Bias mit Tape oder Console genutzt hast. Das ist eine hörbare, bewusste Voicing-Korrektur (siehe `docs/design-brief.md`), kein Bug.

## Tipps

- **Beginne mit Character, bevor du zu Drive greifst.** Die drei Modelle klingen selbst bei identischen Einstellungen wirklich unterschiedlich — Tape ist der vergebendste, von ungeraden Harmonischen dominierte Glue-Sound; Console bleibt transparent, bis du kräftig antreibst, und mischt sich dann ein; Valve ist der am aggressivsten asymmetrische, von geraden Harmonischen geprägte Schub. Wähle zuerst den Character, dann stelle Drive/Warmth nach Geschmack ein.
- **Warmth erledigt dreifache Arbeit.** Es steuert gemeinsam die Character-abhängige Asymmetrie des Saturators, den HF-Rolloff und den LF-Head-Bump, sodass eine einzelne Warmth-Bewegung nach „mehr Tape" klingen kann, ohne dass sich sonst ein Regler ändert — das ist der schnellste Weg, den Kern-Charakter des Plugins zu erkunden. Falls du den Verdunklungs-/Gewichtseffekt ohne mehr Saturation-Asymmetrie willst, greife stattdessen zu den separaten LF-/HF-Trim-Shelves, oder gleiche die Asymmetrie mit einem negativen Bias wieder aus.
- **Bias ist für Feintuning da, nicht für den großen Auftritt.** Lass ihn bei 0 %, bis Warmth (und Character) dich fast ans Ziel gebracht haben, und schiebe dann Bias nach, wenn du etwas mehr (oder weniger, oder umgekehrten) asymmetrischen Charakter willst, ohne HF-Rolloff/Head-Bump zu verschieben.
- **Wow, Flutter und Hiss stehen alle drei bewusst standardmäßig auf off.** Es sind bewusste „abgenutztes Tape"-Effekte für Material, das klingen soll, als käme es von einer physischen Maschine (ein Mellotron-artiger Streicher-Patch, ein Vintage-Tape-Emulation-Durchgang auf einem ganzen Mix) — die meisten orchestralen Glue-Anwendungsfälle sollten alle drei bei 0 % lassen und nur zu ihnen greifen, wenn genau dieser Charakter das Ziel ist. Wow und Flutter sind seit v0.2.0 unabhängig, sodass du eine langsame Drift ohne schnelleres Schimmern einstellen kannst, oder umgekehrt.
- **Nutze Mix für Parallel-Processing.** Da Mix sample-genau latenzkompensiert ist, kannst du ein stark getriebenes, charaktervolles Wet-Signal unter das saubere Dry-Signal mischen (New-York-Style Parallel-Saturation), ohne Phasenverschmierung durch die Oversampling-Latenz.
- **HF/LF Trim vs. Tone.** Die Tilt-Shelves von Tone bewegen die gesamte spektrale Balance in einer Geste; HF/LF Trim sind unabhängig, sodass du zum Beispiel mit Tone aufhellen und dann mit einem negativen HF Trim etwas Top-End zurücknehmen kannst, falls die Aufhellung von Tone auch etwas Bestimmtes um 8 kHz überbetont.
- **Nutze Output zum Gain-Matching.** Da Drive/Warmth/Character alle den Pegel und die wahrgenommene Lautheit des Wet-Signals verändern, nutze Output, um das prozessierte Signal wieder auf ungefähr dieselbe Lautheit wie den Dry-Input zu bringen, bevor du sie vergleichst (vermeidet die „lauter klingt immer besser"-Falle beim A/B-Vergleich von Mix oder Bypass).
