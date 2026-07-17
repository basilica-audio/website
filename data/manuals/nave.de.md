<!-- German translation of nave.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Nave-Icon" width="120"/></p>

# Nave-Benutzerhandbuch

*Cabinet-Impulsantwort-Loader für Gitarren- und Bass-Reamping.*

## Was Nave ist

Nave nimmt ein trockenes, unverstärktes Instrumentensignal (eine DI-Gitarren- oder Bass-Spur, oder den Pre-Cab-Output eines Amp-Sims) und faltet es mit der Impulsantwort ("IR") eines echten (oder emulierten) Lautsprecher-Cabinets und Mikrofons. Anders gesagt: Bei Nave wird aus einem trockenen, schnarrenden DI-Signal etwas, das klingt, als wäre es an einem echten Cab in einem Raum abgenommen worden.

In einer Heavy-Production-Chain sitzt Nave typischerweise **nach** der Distortion-/Amp-Sim-Verarbeitung und **vor** EQ-/Bus-Processing:

```
DI guitar/bass -> amp sim / preamp distortion -> Nave (cab IR) -> EQ / compression -> mix bus
```

Es eignet sich gleichermaßen zum nachträglichen Reamping einer aufgenommenen DI-Spur wie zum Live-Einsatz in einer Monitoring-Chain während des Trackings.

## Signalfluss

```
Input --> Convolution (crossfade of IR A / IR B) --> Distance --> LoCut (HPF) --> HiCut (LPF)
                                                                                          |
                                    Output <-- Level (output trim) <-- Mix <--------------+
                                                                          ^
                                                                          |
                                                              delay-compensated dry path
```

1. **Convolution.** Dein Instrumentensignal wird mit der/den geladenen Impulsantwort(en) gefaltet. Ohne geladene IR läuft Nave mit einer mathematisch transparenten Unit-Impuls-("Delta"-)IR — es ist von Haus aus ein valider, standardmäßig stiller Effekt, kein Platzhalter, der deinen Sound färbt, bis du etwas lädst.
2. **Distance.** Eine optionale, simulierte Mikrofon-Abstand-Färbung (siehe [Distance](#distance-simulierter-mikrofonabstand) unten). Standardmäßig aus.
3. **LoCut / HiCut.** Zwei universelle Tone-Shaping-Filter zum Aufräumen des gefalteten Signals — ein Hochpass, um das Low End zu straffen, ein Tiefpass, um Fizz/Härte zu zähmen. Beide sind standardmäßig aus (vollständig offen).
4. **Mix.** Mischt das vollständig verarbeitete ("wet") Signal mit deinem ursprünglichen trockenen Input. Standardmäßig 100 % wet — eine Cab-IR läuft normalerweise voll im Signalweg, nicht gemischt mit der rohen DI.
5. **Level.** Ein finaler Output-Trim, damit das Wechseln von Cabs/Einstellungen nicht auch dein nachgelagertes Gain-Staging durcheinanderbringt.

Die implementierungsseitigen Details (Latenzhandling, Filter-Bypass-Semantik, IR-Datei-State) findest du in [`architecture.md`](architecture.md).

## Impulsantworten laden

Nave hat **zwei unabhängige IR-Slots**, A und B:

- **IR A** — der primäre/ursprüngliche Slot. Nutze den Button **Load IR...**, um eine `.wav`/`.aiff`-Cabinet-IR-Datei auszuwählen; **Default** setzt ihn zurück auf die eingebaute transparente Delta-IR.
- **IR B** — ein sekundärer Slot, geladen und geleert auf die gleiche Weise über **Load IR B...** / **Default**. Für sich allein bewirkt er nichts (siehe [IR Blend](#ir-blend) unten) — er spielt erst eine Rolle, sobald du etwas Blend einstellst.

Die Dateipfade beider Slots werden mit deiner Session/deinem Preset gespeichert, sodass ein Projekt mit denselben geladenen Cabs wieder öffnet.

### IR Blend

Zwei unterschiedliche geladene IRs können selbst bei identischen Distance-/LoCut-/HiCut-/Mix-Einstellungen spürbar unterschiedlich laut klingen — Nave normalisiert die *Energie* jeder geladenen IR auf eine einheitliche Referenz (nicht ihre wahrgenommene Lautheit), und reale Cab-IRs unterscheiden sich in Länge/Spektralinhalt genug, dass dasselbe Energieziel trotzdem bei unterschiedlicher subjektiver Lautstärke landen kann. Das ist kein Bug, den du mit EQ ausgleichen solltest — greife stattdessen zu **Level**, um das Gain-Staging nach dem Tausch von IRs anzugleichen.

Der Regler **IR Blend** überblendet zwischen IR A (0 %) und IR B (100 %). Typische Anwendungen:

- **Zwei verschiedene Cabs** — ein straffes 4x12 mit einem boomigeren 2x12 nach Geschmack mischen, ohne ein separates Blending-Plugin zu brauchen.
- **Zwei Mikrofonpositionen am selben Cab** — z. B. ein On-Axis-Nahmikrofon (IR A), gemischt mit einem Raum-/Ambience-Mikrofon (IR B), für mehr Dimension.

Wenn du IR B lädst, richtet Nave sie automatisch **phasenrichtig** am transienten Einsatz von IR A aus, bevor die beiden überhaupt gemischt werden. Zwei reale IR-Aufnahmen beginnen selten exakt im gleichen Moment (unterschiedliche Mikrofonabstände, unterschiedliche Aufnahme-Setups), und unausgerichtete IRs direkt zu mischen würde ein breites Frequenzband teilweise auslöschen (Kammfilterung) — der Ausrichtungsschritt verhindert das, sodass IR Blend wie eine echte klangliche Mischung klingt statt wie ein phasiges Durcheinander.

Blend steht standardmäßig auf 0 % (nur IR A) — eine IR B zu laden und Blend bei 0 % zu lassen hat keinen hörbaren Effekt, bis du den Regler aufdrehst.

### Distance (simulierter Mikrofonabstand)

Der Regler **Distance** ist eine vereinfachte Emulation davon, das Mikrofon weiter vom Cab wegzurücken: Bei höheren Einstellungen reduziert er den Nahbesprechungseffekt im Bass und dämpft die Höhen leicht. Die Höhenverdunklung ist modelliert nach dem Verhalten eines echten Cabinets, dessen Höhen abfallen, wenn ein Mikrofon weiter zurück und aus der Achse bewegt wird — das wird sehr viel stärker von der Richtcharakteristik des Lautsprechers getrieben als von tatsächlicher Luftabsorption bei typischen Reamping-Abständen. Lies es also weniger als „die Luft zwischen Mikro und Cab" und mehr als „wie der Lautsprecher selbst seitlich weniger Höhen abstrahlt". Es ist *kein* physikalisch exaktes Distanzmodell — es wird keine Pre-Delay-/Timing-Änderung angewendet — nur eine musikalisch nützliche klangliche Verschiebung, um eine zu nahe/zu helle IR im Mix zurückzuschieben, ohne zu einem separaten EQ greifen zu müssen. Der Bassbereich reagiert im ersten Teil des Reglerwegs schneller und flacht Richtung 100 % ab, was dem Verhalten des echten Nahbesprechungseffekts entspricht — der Großteil der Änderung passiert früh, nicht gleichmäßig über den gesamten Regelweg verteilt.

Distance steht standardmäßig auf 0 % ("aus" — an dieser Stelle der Chain wird gar keine Färbung angewendet, ein echter Passthrough).

## Parameterreferenz

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **LoCut** | 20 – 800 | 20 (off) | Hz | Hochpassfilter nach der Convolution. Bei seinem Minimum (20 Hz, Default) ist es vollständig bypassed — ein echter Passthrough, nicht nur eine unhörbare Grenzfrequenz. Höher drehen, um eine boomige Cab-IR zu straffen oder Low-End-Mud zu zähmen, bevor das Low End auf dein Amp-/Bus-Processing trifft. |
| **HiCut** | 2000 – 20000 | 20000 (off) | Hz | Tiefpassfilter nach der Convolution. Bei seinem Maximum (20 kHz, Default) ist es vollständig bypassed. Niedriger drehen, um Fizz, Härte oder überschüssige Höhen einer hellen IR zu zähmen — ein klassischer Move bei High-Gain-Metal-Gitarrensounds. |
| **IR Blend** | 0 – 100 | 0 (IR A only) | % | Überblendet zwischen IR A (0 %) und IR B (100 %). Siehe [IR Blend](#ir-blend). Hat keinen hörbaren Effekt, solange keine IR in Slot B geladen ist. |
| **Distance** | 0 – 100 | 0 (off) | % | Simulierter Mikrofon-zu-Cab-Abstand: reduziert Nahbesprechungs-Bass und fügt mit steigendem Wert hochfrequente Verdunkelung hinzu. Siehe [Distance](#distance-simulierter-mikrofonabstand). |
| **Mix** | 0 – 100 | 100 (fully wet) | % | Dry/Wet-Blend des vollständig verarbeiteten Signals gegen deinen Original-Input. Niedriger drehen für einen parallelen/gemischten Cab-Sound, oder um probehalber zu hören, wie viel vom Charakter der IR du wirklich willst. |
| **Level** | -24 – +24 | 0 | dB | Output-Trim, zuletzt angewendet. Nutze es, um das Gain-Staging nach dem Wechseln von IRs oder dem Einstellen von Mix/Blend/Distance anzugleichen — all das kann den Gesamtpegel verschieben. |

## Presets

Am oberen Rand von Naves Editor sitzt eine Preset-Leiste: `[<] [Preset-Name] [>] [Save] [Save As...] [Delete] [Import...] [Export...]`. Klicke auf den Preset-Namen, um die vollständige Liste zu öffnen (zuerst Werkspresets, dann deine eigenen, beide alphabetisch); `<`/`>` blättern durch dieselbe Liste. Nave bringt acht Werkspresets mit — was jedes einzelne bewirkt, steht in [`docs/presets.md`](presets.md). Deine eigenen Presets speichert Nave unter `~/Library/Audio/Presets/Yves Vogl/Nave/` auf macOS (`%APPDATA%\Yves Vogl\Nave\Presets\` unter Windows); „Set current as default" (im Preset-Menü) bestimmt, was eine frisch eingefügte Instanz von Nave lädt. Import/Export akzeptieren beide einzelne Preset-Dateien; Import akzeptiert zusätzlich eine `.zip`-Preset-Bank, exportiert von `PresetManager::exportBank()`.

## Latenz

Nave nutzt aus gutem Grund JUCEs Zero-Latency-Convolution-Algorithmus — für Reamping genutzte Cab-IRs sind kurz, und Reamping-/Tracking-Workflows sind latenzsensibel, weshalb Nave dem Host niemals eine Plugin-Delay-Kompensation meldet. Das gilt unabhängig davon, wie viele der oben genannten Features (IR Blend, Distance, LoCut/HiCut) aktiv sind.

## Tipps

- **Beginne mit LoCut/HiCut auf ihren Defaults (aus)** und bringe sie erst ein, wenn die rohe IR Formung braucht — eine gut aufgenommene Cab-IR braucht oft wenig bis gar keine zusätzliche Filterung, und unnötige Filter kosten nur Headroom und CPU ohne Nutzen.
- **Für einen druckvolleren Metal-Rhythmus-Sound** versuche, eine straffe, nah abgenommene 4x12-IR (IR A) mit einer kleinen Menge einer etwas dunkleren/räumlicheren IR B zu mischen (10–25 % Blend), statt zu einem zweiten Cab-Sim-Plugin zu greifen.
- **Distance ist ein Feinschliff, kein Tone-Shaping-Tool** — brauchst du einen bestimmten Frequenzgang, nutze stattdessen LoCut/HiCut (oder deinen EQ danach); Distance ist für eine leichte „im Raum zurückschieben"-Anpassung gedacht.
- **Klingt eine geladene IR nach Blend-/Distance-Änderungen dünn oder boxig, prüfe Level** — weder Mix, Blend noch Distance sind gegeneinander gain-kompensiert, bewusst so gebaut (damit du immer genau weißt, was du hörst), was bedeutet, dass Level die eine Stelle ist, an der du einen daraus resultierenden Pegel-Mismatch korrigierst, bevor er auf deinen Mixbus trifft.
- **Führe einen Null-Test mit deinen Default-Einstellungen durch**, falls du dir je unsicher bist, ob Nave dein Signal färbt: ohne geladene IR (oder mit IR A auf ihrem Default) und LoCut/HiCut/Distance allesamt auf ihren Defaults ist Nave ein zertifizierter bit-genauer Passthrough (siehe die projekteigenen Null-Tests in `tests/EngineTests.cpp` und `tests/CoverageTests.cpp`).
