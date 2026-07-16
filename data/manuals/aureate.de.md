<!-- German translation of aureate.en.md (English source generated from aureate/docs/manual.md on 2026-07-16) — do not hand-edit; re-translate after the English manual is resynced. -->

<p align="center"><img src="assets/icon.png" alt="Aureate-Icon" width="120"/></p>

# Aureate — Bedienungsanleitung

## Was Aureate ist

Aureate ist ein Tape-/Console-Saturation-"Glue"-Plugin für orchestrales Material – Streicher, Blechbläser und geschichtete/gebusste Spuren, die Kohäsion und einen Hauch analoger Wärme brauchen, ohne wie ein Gitarrenpedal zu klingen. Es kombiniert einen 4x-oversampelten, im Charakter wählbaren Saturator (tanh-basiertes Tape, Cubic-Clip-Console oder exponentielle Valve) mit Tape-Transport-Artefakten (Wow/Flutter, Hiss) und einem Console-artigen Tilt-EQ plus unabhängigen HF-/LF-Trim-Shelves.

## Wo es in einer Heavy-Music-Produktionskette sitzt

Aureate ist dafür gedacht, **nachdem** die einzelnen Layer eines orchestralen/chorischen Stacks (Streicher, Blechbläser, Chor usw.) ausbalanciert wurden, zu laufen, typischerweise auf:

- Einem **Streicher- oder Blechbläser-Bus**, um eine Divisi-Sektion so zu verkleben, wie Tape-/Console-Summing das auf natürliche Weise tut – ein wenig Drive und Warmth, moderater Mix, und die Sektion liest sich als ein Instrument statt als Haufen Nahmikrofonierungen.
- Einem **orchestralen/chorischen Submix-Bus**, der nach den einzelnen Sektionen und vor dem finalen Mix-Bus sitzt, um Kohäsion hinzuzufügen, bevor das orchestrale Material auf die Metal-Instrumentierung (Gitarren, Drums, Bass) trifft.
- Dem **Mix-Bus** selbst (sparsam – niedriger Drive, Mix deutlich unter 100 %), als subtiler "Master-Glue"-Durchgang, in derselben Rolle, die eine Tape-Maschine oder ein Console-Summing-Bus in einem hybriden Analog-/ITB-Workflow spielen würde.

Es ist kein Distortion- oder Amp-Sim-Plugin (diese Rolle übernehmen `overture`/`tenebrae` an anderer Stelle der Suite) – Drive ist bewusst auf moderate 24 dB gedeckelt, und die Standard-Warmth-/Character-Einstellungen bleiben deutlich im Bereich "fügt Fülle hinzu", nicht "fügt Grit hinzu".

## Signalfluss

```
input -> Wow/Flutter -> Drive
      -> [4x oversampled: Warmth HF-rolloff -> saturator (Character: Tape/Console/Valve,
         Warmth+Bias-driven asymmetry) -> Tone tilt -> HF/LF Trim -> Hiss]
      -> downsample -> Dry/Wet Mix -> Output trim -> output
```

Wow/Flutter und Drive laufen mit der Host-Samplerate; alles vom Warmth-Low-Pass bis Hiss läuft innerhalb der 4x-oversampelten Domäne, sodass die Harmonischen des Saturators (und das Rauschen von Hiss) mit dem 4-fachen der Host-Rate erzeugt und gefiltert werden, bevor ein einzelner Downsample-Schritt erfolgt. Mix mischt das prozessierte ("wet") Signal zurück mit einer latenzkompensierten Kopie des unangetasteten Inputs, und Output ist ein finaler Trim, der auf das kombinierte Ergebnis angewendet wird. Die vollständige technische Aufschlüsselung, inklusive Latenz-Buchhaltung und Real-Time-Safety-Notizen, findest du in [`docs/architecture.md`](architecture.md).

## Parameterübersicht

| Parameter | Bereich | Standard | Einheit | Was es bewirkt |
|---|---|---|---|---|
| **Wow/Flutter** | 0-100 | 0 | % | Menge der Tape-Transport-Geschwindigkeitsinstabilität: ein langsames "Wow" (~0.7 Hz) plus ein schnelleres "Flutter" (~6.5 Hz) Pitch-Wobble, angewendet über ein moduliertes Delay vor Drive. 0 % ist ein festes (unmoduliertes) Delay – ein echter Off-Zustand, nicht "sehr wenig". Sparsam einsetzen (10-25 %) für einen Vintage-Tape-Charakter auf gehaltenen Pads/Streichern; höhere Einstellungen sind ein offensichtlicher, bewusster Effekt. |
| **Drive** | 0-24 | 6 | dB | Gain in den Saturator hinein. Bewusst moderat gehalten – Aureate ist ein Glue-Prozessor, kein Distortion-Pedal. Höhere Einstellungen treiben die per Character gewählte Kurve stärker, was mehr harmonischen Inhalt und Kompression hinzufügt. |
| **Warmth** | 0-100 | 35 | % | Steuert zwei Dinge gemeinsam über einen Regler: den Asymmetrie-Bias des Saturators (single-ended, tape-artiger Charakter) und einen sanften Pre-Clip-Höhenabfall (Tape-Selbstlöschung/Bias-Oscillator-Verdunkelung). Höheres Warmth = asymmetrischere Saturation und ein dunkleres Top-End – der mit Abstand wichtigste "Charakter"-Regler des Plugins. |
| **Bias** | -100 to 100 | 0 | % | Ein zusätzlicher, unabhängiger Asymmetrie-Trim des Saturators, der zum eigenen Bias-Beitrag von Warmth hinzukommt. Nutze ihn, um die Asymmetrie weiter zu verschieben (oder in die Gegenrichtung), ohne die HF-Rolloff-Menge von Warmth anzutasten – nützlich, um die Balance zwischen ungeraden und geraden Harmonischen nach Geschmack einzustellen. |
| **Character** | Tape / Console / Valve | Tape | - | Wählt die Transferfunktions-Familie des Saturators. **Tape**: sanftes, asymmetrisches tanh, eine "unendliche" Soft-Compression-Kurve – der klassische, vergebende Tape-Glue-Sound. **Console**: ein asymmetrisches Cubic-Soft-Clip, härter und unterhalb seines Clip-Points transparenter – näher an einem Solid-State-Summing-Bus. **Valve**: eine asymmetrische, exponentielle Saturation-Kurve mit einer anderen Balance aus geraden/ungeraden Harmonischen als die beiden anderen – ein runderer, röhrenartiger Charakter. |
| **Tone** | -100 to 100 | 0 | % | Ein Console-artiges Tilt-EQ: negativ verdunkelt (Low Shelf hoch, High Shelf runter), positiv hellt auf (umgekehrt), 0 % ist flach/unity. Nutze dies für die grobe tonale Balance des gesamten prozessierten Signals. |
| **HF Trim** | -6 to 6 | 0 | dB | Ein High-Shelf-Trim mit fester Frequenz (8 kHz), unabhängig von Tone – eine feinere Top-End-Anpassung (Air hinzufügen oder Härte zähmen), nachdem der breitere Tone-Tilt die Gesamtbalance gesetzt hat. |
| **LF Trim** | -6 to 6 | 0 | dB | Ein Low-Shelf-Trim mit fester Frequenz (150 Hz), unabhängig von Tone – eine feinere Low-End-Anpassung (Gewicht hinzufügen oder Mud straffen) nach dem breiteren Tone-Tilt. |
| **Hiss** | 0-100 | 0 | % | Menge geformten Rauschens ("Tape Hiss"), das in das prozessierte Signal gemischt wird, erzeugt innerhalb der oversampelten Domäne, sodass es eine natürliche Top-End-Abmilderung durch den Downsampling-Filter erbt. 0 % ist wirklich still (überhaupt kein Rauschteppich) – eine bewusste "Vintage"-Option für Material, das klingen soll, als käme es von einer Tape-Maschine, kein Mischpult-Artefakt, das standardmäßig aktiv bleiben sollte. |
| **Mix** | 0-100 | 100 | % | Dry/Wet-Mischung. Bei 0 % ist das Plugin ein sample-genauer (latenzkompensierter) Durchlauf des Inputs – nützlich für Parallel-/New-York-Style-Blending oder um zu bestätigen, dass Aureate ein Signal nicht einfärbt, wenn du es per A/B herausnehmen willst. |
| **Output** | -24 to 24 | 0 | dB | Finaler Output-Trim, angewendet *nach* der Dry/Wet-Mischung – anders als Drive (das nur den Wet-Pfad betrifft) skaliert Output das kombinierte Dry+Wet-Signal als Ganzes. Nutze ihn, um Pegeländerungen durch Drive/Warmth/Character auszugleichen, bevor das Signal weiter durch die Kette läuft. |

## Tipps

- **Beginne mit Character, bevor du zu Drive greifst.** Die drei Modelle klingen bei denselben Drive-/Warmth-Einstellungen recht unterschiedlich – Tape ist am vergebendsten und glue-artigsten, Console ist direkter und "solider", Valve liegt irgendwo dazwischen mit einem runderen Top-End. Wähle zuerst den Character, dann stelle Drive/Warmth nach Geschmack ein.
- **Warmth erledigt Doppeltes.** Weil es sowohl die Asymmetrie des Saturators als auch den HF-Rolloff gemeinsam steuert, kann eine einzelne Warmth-Bewegung nach "mehr Tape" klingen, ohne dass sich sonst ein Regler ändert – das ist der schnellste Weg, den Kern-Charakter des Plugins zu erkunden. Falls du den Verdunklungseffekt ohne mehr Saturation-Asymmetrie willst, greife stattdessen zu den separaten LF-/HF-Trim-Shelves, oder gleiche die Asymmetrie mit einem negativen Bias wieder aus.
- **Bias ist für Feintuning da, nicht für den großen Auftritt.** Lass ihn bei 0 %, bis Warmth (und Character) dich fast ans Ziel gebracht haben, und schiebe dann Bias nach, wenn du etwas mehr (oder weniger, oder umgekehrten) asymmetrischen Charakter willst, ohne den HF-Rolloff zu verschieben.
- **Wow/Flutter und Hiss stehen beide bewusst standardmäßig auf off.** Es sind bewusste "abgenutztes Tape"-Effekte für Material, das klingen soll, als käme es von einer physischen Maschine (ein Mellotron-artiger Streicher-Patch, ein Vintage-Tape-Emulation-Durchgang auf einem ganzen Mix) – die meisten orchestralen Glue-Anwendungsfälle sollten beide bei 0 % lassen und nur zu ihnen greifen, wenn genau dieser Charakter das Ziel ist.
- **Nutze Mix für Parallel-Processing.** Da Mix sample-genau latenzkompensiert ist, kannst du ein stark getriebenes, charaktervolles Wet-Signal unter das saubere Dry-Signal mischen (New-York-Style Parallel-Saturation), ohne Phasenverschmierung durch die Oversampling-Latenz.
- **HF/LF Trim vs. Tone.** Die Tilt-Shelves von Tone bewegen die gesamte spektrale Balance in einer Geste; HF/LF Trim sind unabhängig, sodass du zum Beispiel mit Tone aufhellen und dann mit einem negativen HF Trim etwas Top-End zurücknehmen kannst, falls die Aufhellung von Tone auch etwas Bestimmtes um 8 kHz überbetont.
- **Nutze Output zum Gain-Matching.** Da Drive/Warmth/Character alle den Pegel und die wahrgenommene Lautheit des Wet-Signals verändern, nutze Output, um das prozessierte Signal wieder auf ungefähr dieselbe Lautheit wie den Dry-Input zu bringen, bevor du sie vergleichst (vermeidet die "lauter klingt immer besser"-Falle beim A/B-Vergleich von Mix oder Bypass).
