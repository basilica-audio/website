<!-- German translation of crypta.en.md (source repo twist-your-guts, pre-rename; this plugin now ships as Crypta) — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Twist Your Guts-Icon" width="120"/></p>

# Twist Your Guts — Bedienungsanleitung

*Teile deinen Bass. Komprimiere die Tiefen. Dreh den Höhen die Gedärme raus.*

## Was es ist

Twist Your Guts ist ein **paralleler Bass-Prozessor** im Parallax-Stil, für Metal-Produktionen entwickelt. Es teilt dein Bass-Signal mit einer Linkwitz-Riley-Frequenzweiche 4. Ordnung („LR4") in ein Low- und ein High-Band auf, hält das Low-Band mit einem Parallel-Kompressor eng zusammen und schickt das High-Band durch eine Auswahl von drei Distortion-Voicings, bevor am Ende alles über ein 4-Band-EQ und einen Cabinet-Simulation-IR-Loader wieder zusammengeführt wird.

### Wo es in einer intensiven Produktionskette sitzt

Twist Your Guts ist als **bass-spezifische Voicing-Stufe** der „Metal up your ass"-Suite konzipiert:

- Spurreihenfolge: **DI/Amp-Sim → Twist Your Guts → Bus-Kompression/Glue → Mix-Bus**. Es erwartet ein einigermaßen sauberes, bereits amp-simuliertes oder direkt eingespieltes (DI) Bass-Signal; es ist selbst kein vollständiger Amp-Sim (kein eingebautes Preamp-Gain-Staging über Input-Trim und Drive-Regler hinaus).
- Der Parallel-Kompressor des Low-Bands soll den Grundton-/Sub-Anteil des Basses unter einer Wand verzerrter Gitarren fest verankern, während das Voicing des High-Bands den Upper-Mid-„Grind" hinzufügt, der dem Bass erlaubt, sich durch einen dichten Mix zu schneiden, ohne mit den Gitarren um denselben Frequenzbereich zu konkurrieren.
- Der Crossover-Punkt (Standard 250 Hz) ist bewusst über das gesamte Low-Mid-Register (60 Hz–1000 Hz) einstellbar, sodass du den Split an die Stimmung des Songs anpassen kannst (Drop-Tunings schieben nutzbaren Tiefton-Inhalt weiter nach oben).
- Der IR-Loader der Output-Stufe ist für schnelles Cabinet-artiges Tone-Shaping gedacht, ohne dass später in der Kette ein separates Cab-Sim-Plugin nötig wäre — er kann aber auch komplett ausgelassen werden, wenn du anderswo bereits eine dedizierte Cab-Sim einsetzt.

## Signalfluss

```
Input Trim → Gate → LR4 Split (60–1000 Hz, default 250 Hz)
                      │
        ┌─────────────┴─────────────┐
        │                           │
     Low band                   High band
  Parallel Comp → Level   Voicing → Drive → Tone → Blend → Level
        │                           │
        └─────────────┬─────────────┘
                       │
              Sum (delay-compensated)
                       │
                  4-band EQ
                       │
                  IR loader
                       │
              Safety Clip (optional)
                       │
                     Output
```

Das High-Band fährt sein Distortion-Voicing oversampled (4x), um Aliasing unter Kontrolle zu halten; das Low-Band führt ein passendes Kompensations-Delay mit, damit beide Bänder bei der Summierung zeitlich ausgerichtet bleiben. Die vollständige technische Aufschlüsselung, einschließlich genau wie diese Latenzkompensation funktioniert, findest du in [`docs/architecture.md`](architecture.md).

## Parameter-Referenz

Sofern nicht anders angegeben, sind alle kontinuierlichen Parameter geglättet (Smoothing), um Zipper-Noise bei Automation zu vermeiden.

### IO / Global

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| Input Gain | −24 … +24 | 0 | dB | Trimmt das Signal, bevor irgendetwas anderes in der Kette passiert. Nutze das, um ein hohes, aber nicht clippendes Signal in die Gate-/Kompressor-/Voicing-Stufen zu bekommen — all ihre Thresholds sind unter der Annahme eines einigermaßen „Line-Level"-Eingangs kalibriert. |
| Output Gain | −24 … +24 | 0 | dB | Finaler Output-Trim, angewendet nach allem anderen (einschließlich des Safety Clip). |
| Bypass | off/on | off | — | Erzwingt einen bitgenauen Durchlauf des Eingangssignals. Auch als hostseitiger Bypass-Parameter des Plugins verfügbar, sodass auch der eigene Bypass-Button/die Automationsspur deiner DAW funktioniert. |
| Safety Clip | off/on | off | — | Ein weicher (tanh) Limiter auf der allerletzten Stufe vor dem Output-Trim. Standardmäßig aus; schalte ihn als Sicherheitsnetz gegen versehentliches hartes Clipping ein, nicht als Tone-Shaping-Werkzeug — bei typischen Spielpegeln ist er unhörbar und beginnt erst, Peaks zu runden, wenn sie sich 0 dBFS nähern. |

### Noise Gate (Full-Band, vor dem Crossover-Split)

Sitzt vor der Frequenzweiche, gatet also das Eingangssignal als Ganzes statt pro Band.

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| Gate Enable | off/on | **off** | — | Aktiviert das Gate. Standardmäßig aus — die meisten bereits aufgenommenen Bass-DI-/Amp-Signale brauchen keins, und ein falsch eingestelltes Gate kann legitimes leises Spiel abschneiden (Ghost Notes, Ausklingen). |
| Gate Threshold | −80 … 0 | −60 | dB | Signalpegel, unterhalb dessen das Gate zu dämpfen beginnt. |
| Gate Ratio | 1 … 20 | 10 | :1 | Wie aggressiv das Gate unterhalb des Thresholds dämpft. Höher = näher an einem harten Mute. |
| Gate Attack | 0.1 … 50 | 1 | ms | Wie schnell das Gate öffnet, sobald das Signal wieder über den Threshold steigt. |
| Gate Release | 5 … 500 | 100 | ms | Wie schnell das Gate schließt, sobald das Signal unter den Threshold fällt. |

### Crossover

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| Crossover Frequency | 60 … 1000 | 250 | Hz | Der LR4-Split-Punkt zwischen Low- und High-Band. Logarithmisch skalierter Regler (gleicher Reglerweg pro Oktave). Senke ihn ab, um mehr vom Grundton in das (typischerweise sauberere, komprimierte) Low-Band zu schieben; erhöhe ihn, um dem Distortion-Voicing mehr Low-Mid-Inhalt zum Arbeiten zu geben. |

### Low-Band: Parallel-Kompressor + Level

Das Low-Band wird **parallel** komprimiert („New-York-Style"): Das komprimierte Signal wird über Mix mit seinem eigenen unkomprimierten Original zurückgemischt, statt es vollständig zu ersetzen — genau das sorgt dafür, dass die Tiefen eng und kontrolliert wirken, ohne je zusammengedrückt oder leblos zu klingen.

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| Low Comp Threshold | −60 … 0 | −18 | dB | Pegel, ab dem der Low-Band-Kompressor einsetzt. |
| Low Comp Ratio | 1 … 20 | 4 | :1 | Kompressionsverhältnis oberhalb des Thresholds. |
| Low Comp Attack | 0.1 … 100 | 10 | ms | Wie schnell der Kompressor zupackt, sobald er über dem Threshold liegt. |
| Low Comp Release | 10 … 1000 | 120 | ms | Wie schnell der Kompressor loslässt, sobald er wieder unter dem Threshold liegt. |
| Low Comp Makeup | −12 … +24 | 0 | dB | Gain, der auf das komprimierte (Wet-)Signal angewendet wird, bevor es mit dem trockenen Low-Band zurückgemischt wird — nutze das, um das komprimierte Signal wieder auf den Pegel des trockenen Signals zu bringen, damit Mix wirklich als „wie viel Kompressions-Charakter"-Regler funktioniert, statt auch die Gesamtlautheit zu verändern. |
| Low Comp Mix | 0 … 100 | 100 | % | Blend zwischen dem trockenen (unkomprimierten) und dem nassen (komprimierten + Makeup) Low-Band. 0 % = Kompressor hat keine hörbare Wirkung; 100 % = vollständig komprimiert. |
| Low Level | −24 … +12 | 0 | dB | Pegel-Trim auf dem Low-Band, angewendet nach der Kompression und bevor die Bänder wieder summiert werden. |

### High-Band: Voicing, Drive, Tone, Blend, Level

Drei wählbare Distortion-Voicings, jedes oversampled (4x), um das Aliasing der nichtlinearen Shaping-Stufe aus dem hörbaren Band herauszuhalten.

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| High Voicing | Gnaw / Wool / Razor | Gnaw | — | Wählt den Distortion-Charakter. Siehe unten. |
| High Drive | 0 … 100 | 50 | % | Wie hart das Signal in die Nichtlinearität des gewählten Voicings gedrückt wird. |
| High Tone | 0 … 100 | 50 | % | Tone-Regler nach dem Shaper: ein Low-Pass, der von dunkel (0 %) zu hell (100 %) fährt und Fizz/Härte aus der Distortion-Stufe wegräumt oder öffnet. |
| High Blend | 0 … 100 | 100 | % | Blend zwischen dem sauberen (Pre-Voicing-) und dem voll verzerrten High-Band. 0 % = sauberes High-Band (Voicing hat keine hörbare Wirkung); 100 % = vollständig verzerrt. |
| High Level | −24 … +12 | 0 | dB | Pegel-Trim auf dem High-Band, angewendet nach Voicing/Blend und bevor die Bänder wieder summiert werden. |

**Voicings:**

- **Gnaw** — ein Hard-Clip im Op-Amp-Stil. Symmetrisch, unnachgiebig, das aggressivste der drei; drückt bei hohem Drive stark in Richtung einer rechteckartigen Wellenform. Gut für einen rohen, schnarrenden Anschlag.
- **Wool** — kaskadierter Soft-Clip-Fuzz mit einer Mid-Scoop und einer Prise Asymmetrie für einen körnigeren, fuzz-pedal-artigeren harmonischen Charakter. Gut für einen wolligeren, weniger „digitalen" Grind, der trotzdem durchsticht.
- **Razor** — ein engeres Overdrive: Das Signal wird vor dem (vergleichsweise milden) Clipper hochpassgefiltert, und ein Mid-Hump-Filter danach verhindert, dass die Tiefen jemals matschig werden. Gut für Definition und Plektrum-/Finger-Anschlag, ohne Low-End-Mud aufzutürmen.

*Ausgangspunkte, kein finales Voicing:* Die Drive-Gain-Bereiche und die Mid-Filter-Hump-/Scoop-Einstellungen aller drei Voicings sind Engineering-Defaults, auf musikalische Brauchbarkeit abgestimmt und mathematisch begrenzt (kein durchgehender Output bei keiner Drive-Einstellung), aber noch nicht gehörmäßig gegen Referenzmaterial finalisiert. Erwarte, dass diese in einem zukünftigen Release verfeinert werden.

### 4-Band-EQ nach der Summierung

Wird angewendet, nachdem Low- und High-Band wieder summiert wurden. Standardmäßig aus; wenn aus, wird die EQ-Stufe komplett übersprungen (garantiert transparent, nicht nur auf Unity Gain gesetzt).

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| EQ Enable | off/on | off | — | Aktiviert die EQ-Stufe. |
| EQ Low Shelf Frequency | 40 … 400 | 100 | Hz | Eckfrequenz des Low Shelf. |
| EQ Low Shelf Gain | −18 … +18 | 0 | dB | Boost/Cut des Low Shelf. |
| EQ Peak 1 Frequency | 100 … 2000 | 500 | Hz | Mittenfrequenz des ersten parametrischen Peak-Bands. |
| EQ Peak 1 Gain | −18 … +18 | 0 | dB | Boost/Cut des ersten Peak-Bands. |
| EQ Peak 1 Q | 0.2 … 5.0 | 0.7 | — | Bandbreite des ersten Peak-Bands (höher = schmaler). |
| EQ Peak 2 Frequency | 500 … 8000 | 2500 | Hz | Mittenfrequenz des zweiten parametrischen Peak-Bands. |
| EQ Peak 2 Gain | −18 … +18 | 0 | dB | Boost/Cut des zweiten Peak-Bands. |
| EQ Peak 2 Q | 0.2 … 5.0 | 0.7 | — | Bandbreite des zweiten Peak-Bands. |
| EQ High Shelf Frequency | 2000 … 16000 | 8000 | Hz | Eckfrequenz des High Shelf. |
| EQ High Shelf Gain | −18 … +18 | 0 | dB | Boost/Cut des High Shelf. |

### IR-Loader (Cabinet-Simulation)

Eine faltungsbasierte (Convolution) Cab-Sim-Stufe ganz am Ende der Kette, vor dem Safety Clip. Standardmäßig aus. Ohne geladene Impulsantwort ist diese Stufe bei jeder Session-Samplerate ein garantiert bitgenauer Durchlauf, sodass sie einzuschalten, bevor eine IR geladen ist, deinen Sound nie verändert.

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| IR Enable | off/on | off | — | Aktiviert die IR-Loader-Stufe. |
| IR Mix | 0 … 100 | 100 | % | Blend zwischen dem trockenen (Pre-Convolution-) und dem vollständig gefalteten Signal. |

*Impulsantworten laden:* v0.1.0 liefert noch keinen In-Plugin-Dateibrowser und keine Factory-Cabinet-IRs (beides steht für einen späteren Milestone zusammen mit dem Custom-GUI auf der Roadmap). Die IR-Loading-DSP-Engine selbst ist vollständig implementiert und echtzeitsicher; ein GUI-Dateiauswahl-Dialog wird angebunden, sobald das eigene Interface fertig ist.

## Tipps

- **Starte mit einem engen Low-Band, dann stelle den Grind des High-Bands ein.** Setze zuerst Low Comp Mix und Makeup, damit sich der Grundton fest verankert anfühlt, *dann* wähle Voicing und Drive-Menge — es ist deutlich einfacher zu beurteilen, wie viel Distortion-Charakter du wirklich brauchst, wenn sich die Tiefen schon solide anfühlen.
- **Der Crossover-Punkt ist eine Klangentscheidung, nicht nur eine technische.** Ihn nach oben zu schieben (Richtung 400–600 Hz) verschiebt mehr vom Korpus der Note ins verzerrte High-Band, was einem Bass helfen kann, sich durch eine dichte Gitarrenwand zu schneiden — auf Kosten des Tiefton-Gewichts; ihn nach unten zu ziehen (Richtung 100–150 Hz) hält mehr von der Note sauber/komprimiert und reserviert die Distortion für wirklich hohen harmonischen Inhalt.
- **High Blend ist dein „Wie viel"-Regler, High Drive dein „Wie hart"-Regler.** Wirkt ein Voicing zu extrem, versuche zuerst, Blend zu senken statt Drive — so behältst du oft mehr vom Charakter, nur bei insgesamt geringerer Intensität, statt die Nichtlinearität selbst zu glätten.
- **Razor plus ein sanfter High-Shelf-Cut im EQ** ist ein guter Ausgangspunkt, wenn ein Mix hart/fizzy wirkt — Razors Pre-Clip-Hochpass hält die Tiefen ohnehin schon eng, sodass ein bisschen EQ-Zähmung im Top-End im Nachhinein meist reicht, statt an Drive zu drehen.
- **Lass den Safety Clip beim Tracking/Mixing aus**, und greife nur dann dazu, als Absicherung gegen unerwartete Automation oder einen zu heißen Eingang bei einem bestimmten Take — er ist ein Sicherheitsnetz, kein Teil des beabsichtigten Tone-Shaping-Signalpfads.
