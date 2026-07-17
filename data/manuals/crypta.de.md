<!-- German translation of crypta.en.md (source repo twist-your-guts, pre-rename; this plugin now ships as Crypta) — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Crypta-Icon" width="120"/></p>

# Crypta — Bedienungsanleitung

*Teile deinen Bass. Komprimiere die Tiefen. Dreh den Höhen die Gedärme raus.*

## Was es ist

Crypta ist ein **paralleler Bass-Prozessor** im Parallax-Stil, entwickelt für Metal-Produktionen. Seit v0.2.0 teilt es dein Bass-Signal mit zwei kaskadierten Linkwitz-Riley-Frequenzweichen 4. Ordnung („LR4") in **drei** Bänder auf — Low, Mid und High —, hält das Low-Band mit einem Parallel-Kompressor eng zusammen, treibt das Mid-Band mit gestufter Sättigung an und schickt das High-Band durch eine Auswahl von drei Distortion-Voicings, bevor am Ende alles über ein 4-Band-EQ und einen Cabinet-Simulation-IR-Loader wieder zusammengeführt wird.

### Recherchebasierter Rebuild (v0.2.0)

v0.2.0 ist eine recherchebasierte Neufassung der einfacheren Zweiband-Topologie (Low/High) von v0.1.x, recherchiert anhand des offiziellen Benutzerhandbuchs der Referenz-Plugin-Klasse selbst, eines professionellen Tests eines Drittanbieters, des Hardware-Produkthandbuchs derselben Design-Linie sowie des allgemeinen Community-/Hersteller-Konsenses zu Parallel-Bus-Kompression — **von diesem Projekt nicht gegen die tatsächliche Audioausgabe, den DSP-Quellcode oder eine Hardware-Einheit irgendeines Referenz-Plugins gemessen.** Die vollständige Quellenangabe findest du in `docs/design-brief.md` und `docs/research-notes.md`, sowie denselben Hinweis, den schon v0.1.x trug: Der Voicing-Charakter (Drive-Gain-Bereiche, Mid-Filter-Hump-/Scoop-Einstellungen) ist engineering-abgestimmt, noch nicht gehörmäßig gegen Referenzmaterial finalisiert.

### Wo es in einer Heavy-Music-Chain sitzt

Crypta ist als **bass-spezifische Voicing-Stufe** der Basilica-Audio-Suite konzipiert:

- Spurreihenfolge: **DI/Amp-Sim → Crypta → Bus-Kompression/Glue → Mix-Bus**. Es erwartet ein einigermaßen sauberes, bereits amp-simuliertes oder direkt eingespieltes (DI) Bass-Signal; es ist selbst kein vollständiger Amp-Sim (kein eingebautes Preamp-Gain-Staging über Input-Trim und Drive-Regler hinaus).
- Der Parallel-Kompressor des Low-Bands soll den Grundton-/Sub-Anteil des Basses unter einer Wand verzerrter Gitarren fest verankern. Das Mid-Band fügt einen eigenständigen, „kehligeren" Sättigungscharakter hinzu, der genau in dem Frequenzbereich sitzt, der am ehesten mit einer Gitarrenwand kollidiert — stelle es bewusst ein, nicht nur als Nachgedanke. Das Voicing des High-Bands fügt den Upper-Mid-/High-„Grind" hinzu, der dem Bass erlaubt, sich durch einen dichten Mix zu schneiden.
- Zwei unabhängige Split-Punkte (**Split Low**, **Split High**) lassen dich beide Übergangsfrequenzen über das gesamte Low-Mid-Register hinweg an die Stimmung des Songs anpassen (Drop-Tunings schieben nutzbaren Tiefton-Inhalt weiter nach oben) und steuern, wie breit der „Rachen" des Mid-Bands ist.
- Der IR-Loader der Output-Stufe — jetzt nur noch auf den Mid+High-Pfad angewendet, nie auf das Low-Band — ist für schnelles Cabinet-artiges Tone-Shaping gedacht, ohne dass später in der Kette ein separates Cab-Sim-Plugin nötig wäre — er kann aber auch komplett ausgelassen werden, wenn du anderswo bereits eine dedizierte Cab-Sim einsetzt.

## Signalfluss

```
Input Trim → Gate → LR4 Split Low (60–400 Hz, default 120 Hz)
                      │
        ┌─────────────┴───────────────────────────────┐
        │                                              │
     Low band                              Remainder → LR4 Split High (300–2000 Hz, default 600 Hz)
  Parallel Comp → Level                                  │
        │                          ┌───────────────────┴───────────────────┐
        │                       Mid band                              High band
        │                    Drive → Level          Tight → Voicing → Drive → Tone → Blend → Level
        │                          └───────────────────┬───────────────────┘
        │                                          Mid+High sum
        │                                                │
        │                                          IR loader (cab sim)
        │                                                │
        └───────────────────────┬────────────────────────┘
                                 │
                       Sum (delay-compensated)
                                 │
                            4-band EQ
                                 │
                       Safety Clip (optional)
                                 │
                               Output
```

Mid- und High-Band teilen sich denselben Oversampling-Anti-Aliasing-Headroom (jedes unabhängig 4x oversampled, aber identisch konfiguriert, sodass beide dieselbe Latenz melden); das Low-Band führt ein passendes Kompensations-Delay mit, dazu einen Phasenausrichtungs-Allpassfilter, der an die Eckfrequenz von Split High gekoppelt ist, sodass alle drei Bänder sich beim finalen Summieren glatt und zeitlich ausgerichtet addieren. Der IR-Loader (Cabinet-Simulation) sitzt **nach** der Mid+High-Summe und **vor** der finalen Dreifach-Summe — das Low-Band läuft nie hindurch, passend zur „Low-Band umgeht die Cabsim"-Architektur der Referenzklasse. Die vollständige technische Aufschlüsselung, einschließlich genau wie Latenz- und Phasenausrichtungs-Kompensation funktionieren, findest du in [`docs/architecture.md`](architecture.md).

## Presets

Crypta bringt ein Preset-System mit: Eine horizontale Leiste am oberen Rand des Plugin-Fensters lässt dich durch Werks- und eigene Presets blättern (`<` / Preset-Name / `>`), deine eigenen speichern/als-speichern/löschen und einzelne Presets oder Preset-Bänke (Zip-Dateien mit mehreren Presets) importieren/exportieren. In v0.2.0 sind neun Werkspresets enthalten — was jedes einzelne demonstriert, steht in `docs/presets.md`. Eigene Presets werden pro Plugin gespeichert unter:

- **macOS**: `~/Library/Audio/Presets/Yves Vogl/Crypta/`
- **Windows**: `%APPDATA%\Yves Vogl\Crypta\Presets\`

Eine frische Instanz lädt ein eigenes „Default"-Preset, falls du eines gespeichert hast („Set current as default" im Preset-Menü), sonst das Werks-„Default"-Preset (das den unten dokumentierten reinen Parameter-Defaults entspricht).

## Parameter-Referenz

Sofern nicht anders angegeben, sind alle kontinuierlichen Parameter geglättet (Smoothing), um Zipper-Noise bei Automation zu vermeiden.

### IO / Global

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| Input Gain | −24 … +24 | 0 | dB | Trimmt das Signal, bevor irgendetwas anderes in der Kette passiert. Nutze das, um ein hohes, aber nicht clippendes Signal in die Gate-/Kompressor-/Drive-/Voicing-Stufen zu bekommen — all ihre Thresholds sind unter der Annahme eines einigermaßen „Line-Level"-Eingangs kalibriert. |
| Output Gain | −24 … +24 | 0 | dB | Finaler Output-Trim, angewendet nach allem anderen (einschließlich des Safety Clip). |
| Bypass | off/on | off | — | Erzwingt einen bitgenauen Durchlauf des Eingangssignals. Auch als hostseitiger Bypass-Parameter des Plugins verfügbar, sodass auch der eigene Bypass-Button/die Automationsspur deiner DAW funktioniert. |
| Safety Clip | off/on | off | — | Ein weicher (tanh) Limiter auf der allerletzten Stufe vor dem Output-Trim. Standardmäßig aus; schalte ihn als Sicherheitsnetz gegen versehentliches hartes Clipping ein, nicht als Tone-Shaping-Werkzeug — bei typischen Spielpegeln ist er unhörbar und beginnt erst, Peaks zu runden, wenn sie sich 0 dBFS nähern. |

### Noise Gate (Full-Band, vor dem Crossover-Split)

Sitzt vor beiden Frequenzweichen, gatet also das Eingangssignal als Ganzes statt pro Band.

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| Gate Enable | off/on | **off** | — | Aktiviert das Gate. Standardmäßig aus — die meisten bereits aufgenommenen Bass-DI-/Amp-Signale brauchen keins, und ein falsch eingestelltes Gate kann legitimes leises Spiel abschneiden (Ghost Notes, Ausklingen). |
| Gate Threshold | −80 … 0 | −60 | dB | Signalpegel, unterhalb dessen das Gate zu dämpfen beginnt. |
| Gate Ratio | 1 … 20 | 10 | :1 | Wie aggressiv das Gate unterhalb des Thresholds dämpft. Höher = näher an einem harten Mute. |
| Gate Attack | 0.1 … 50 | 1 | ms | Wie schnell das Gate öffnet, sobald das Signal wieder über den Threshold steigt. |
| Gate Release | 5 … 500 | 100 | ms | Wie schnell das Gate schließt, sobald das Signal unter den Threshold fällt. |

### Split Low / Split High (zwei kaskadierte Frequenzweichen, NEUE Topologie in v0.2.0)

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| Split Low | 60 … 400 | 120 | Hz | Der LR4-Split-Punkt zwischen dem Low-Band und allem darüber. Logarithmisch skalierter Regler. Senke ihn, um mehr vom Grundton in das (nur komprimierte) Low-Band zu schieben; erhöhe ihn, um dem Mid-Band mehr Low-Mid-Inhalt zum Arbeiten zu geben. |
| Split High | 300 … 2000 | 600 | Hz | Der LR4-Split-Punkt zwischen dem Mid-Band und dem High-Band. Logarithmisch skalierter Regler. |

Split High wird intern immer mindestens einen Bruchteil einer Oktave über Split Low gehalten (eine begründete Sicherheitsmarge gegen ein entartetes, nahezu breitenloses Mid-Band) — schiebst du beide nah zusammen, schwebt der *effektive* Wert von Split High leicht über dem, was du für Split Low eingestellt hast, statt das Mid-Band auf nichts zusammenfallen zu lassen.

### Low-Band: Parallel-Kompressor + Level

Das Low-Band wird **parallel** komprimiert: Das komprimierte Signal wird über Mix mit seinem eigenen unkomprimierten Original zurückgemischt, statt es vollständig zu ersetzen — genau das sorgt dafür, dass die Tiefen eng und kontrolliert wirken, ohne je zusammengedrückt oder leblos zu klingen. **v0.2.0 recherchiert die Ballistik-Defaults neu** und übernimmt die eigenen, fest belegten Werte der Referenzklasse — ein schneller, sanfter „Glue"-Bus-Kompressor, nicht der schwerere „New-York-Style"-Squash, den die Defaults von v0.1.x nahelegten (die vollständige Quellenangabe steht in `docs/research-notes.md` §3–4).

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| Low Comp Threshold | −60 … 0 | −18 | dB | Pegel, ab dem der Low-Band-Kompressor einsetzt. |
| Low Comp Ratio | 1 … 20 | **2** | :1 | Kompressionsverhältnis oberhalb des Thresholds. |
| Low Comp Attack | 0.1 … 100 | **3** | ms | Wie schnell der Kompressor zupackt, sobald er über dem Threshold liegt. |
| Low Comp Release | **5** … 1000 | **6** | ms | Wie schnell der Kompressor loslässt, sobald er wieder unter dem Threshold liegt. Die Untergrenze des Bereichs wurde gegenüber v0.1.x von 10 ms abgesenkt, damit der recherchierte Default von 6 ms erreichbar ist. |
| Low Comp Makeup | −12 … +24 | 0 | dB | Gain, der auf das komprimierte (Wet-)Signal angewendet wird, bevor es mit dem trockenen Low-Band zurückgemischt wird — nutze das, um das komprimierte Signal wieder auf den Pegel des trockenen Signals zu bringen, damit Mix wirklich als „wie viel Kompressions-Charakter"-Regler funktioniert, statt auch die Gesamtlautheit zu verändern. |
| Low Comp Mix | 0 … 100 | 100 | % | Blend zwischen dem trockenen (unkomprimierten) und dem nassen (komprimierten + Makeup) Low-Band. 0 % = Kompressor hat keine hörbare Wirkung; 100 % = vollständig komprimiert. |
| Low Level | −24 … +12 | 0 | dB | Pegel-Trim auf dem Low-Band, angewendet nach der Kompression und bevor die Bänder wieder summiert werden. |

### Mid-Band: Drive + Level (NEU in v0.2.0)

Ein eigenständiges Mid-Band mit gestufter/kaskadierter Sättigung, strukturell ähnlich dem Wool-Voicing des High-Bands (zwei kaskadierte Soft-Clip-Stufen), aber ohne eigenen Filter-, Tone- oder Blend-Regler — passend zum Mid-Band der Referenzklasse selbst (nur „Mid Drive... Mid Level"). Die Aufgabe dieses Bands ist ein eigenständiger, „kehligerer" Grind-Charakter, getrennt von der Presence-/Fuzz-/Härte-Kontroll-Rolle des High-Bands.

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| Mid Drive | 0 … 100 | 30 | % | Menge der gestuften Sättigung. 0 % ist ein exakter Passthrough; ein höherer Wert blendet zunehmend zu einem vollständig kaskadiert-tanh-getriebenen Signal über. |
| Mid Level | −24 … +12 | 0 | dB | Pegel-Trim auf dem Mid-Band, angewendet nach Drive und bevor die Bänder wieder summiert werden. |

### High-Band: Tight, Voicing, Drive, Tone, Blend, Level

Drei wählbare Distortion-Voicings, jedes oversampled (4x), um das Aliasing der nichtlinearen Shaping-Stufe aus dem hörbaren Band herauszuhalten.

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| High Tight | 20 … 500 | 100 | Hz | **NEU in v0.2.0**: ein Hochpassfilter vor dem Drive, jetzt vor *jedem* Voicing angewendet (war in v0.1.x eine feste, nur für Razor geltende interne Konstante von 200 Hz). Das ist der primäre „wie viel Fuzz vs. Tightness"-Regler für das gesamte High-Band und zähmt außerdem Härte bei hohen Drive-Einstellungen — zieh ihn Richtung Untergrenze für maximalen Fuzz, drehe ihn hoch für straffere, kontrolliertere Höhen. |
| High Voicing | Gnaw / Wool / Razor | Gnaw | — | Wählt den Distortion-Charakter. Siehe unten. |
| High Drive | 0 … 100 | 50 | % | Wie hart das Signal in die Nichtlinearität des gewählten Voicings gedrückt wird. |
| High Tone | 0 … 100 | 50 | % | Tone-Regler nach dem Shaper: ein Low-Pass, der von dunkel (0 %) zu hell (100 %) fährt und Fizz/Härte aus der Distortion-Stufe wegräumt oder öffnet. |
| High Blend | 0 … 100 | 100 | % | Blend zwischen dem sauberen (Pre-Voicing-) und dem voll verzerrten High-Band. 0 % = sauberes High-Band (Voicing hat keine hörbare Wirkung); 100 % = vollständig verzerrt. |
| High Level | −24 … +12 | 0 | dB | Pegel-Trim auf dem High-Band, angewendet nach Voicing/Blend und bevor die Bänder wieder summiert werden. |

**Voicings:**

- **Gnaw** — ein Hard-Clip im Op-Amp-Stil. Symmetrisch, unnachgiebig, das aggressivste der drei; drückt bei hohem Drive stark in Richtung einer rechteckartigen Wellenform. Gut für einen rohen, schnarrenden Anschlag.
- **Wool** — kaskadierter Soft-Clip-Fuzz mit einer Mid-Scoop und einer Prise Asymmetrie für einen körnigeren, fuzz-pedal-artigeren harmonischen Charakter. Gut für einen wolligeren, weniger „digitalen" Grind, der trotzdem durchsticht.
- **Razor** — ein engeres Overdrive: ein vergleichsweise milder Clipper, mit einem Mid-Hump-Filter danach, der verhindert, dass die Tiefen jemals matschig werden (die Pre-Clip-Hochpass-Aufgabe übernimmt jetzt bandweit Tight, oben, statt wie in v0.1.x eine Eigenheit von Razor selbst zu sein).

*Ausgangspunkte, kein finales Voicing:* Die Drive-Gain-Bereiche und die Mid-Filter-Hump-/Scoop-Einstellungen aller drei Voicings sind Engineering-Defaults, auf musikalische Brauchbarkeit abgestimmt und mathematisch begrenzt (kein durchgehender Output bei keiner Drive-Einstellung), aber noch nicht gehörmäßig gegen Referenzmaterial finalisiert. Erwarte, dass diese in einem zukünftigen Release verfeinert werden.

### 4-Band-EQ nach der Summierung

Wird angewendet, nachdem alle drei Bänder wieder summiert wurden (und nach dem IR-Loader). Standardmäßig aus; wenn aus, wird die EQ-Stufe komplett übersprungen (garantiert transparent, nicht nur auf Unity Gain gesetzt). **v0.2.0 verankert die Default-Eckfrequenzen neu** an einem recherchierten Bass-Tone-Stack-Frequenzsatz derselben Design-Linie wie die Referenzklasse (die Defaults von v0.1.x waren unbelegte Platzhalter).

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| EQ Enable | off/on | off | — | Aktiviert die EQ-Stufe. |
| EQ Low Shelf Frequency | 40 … 400 | **80** | Hz | Eckfrequenz des Low Shelf. |
| EQ Low Shelf Gain | −18 … +18 | 0 | dB | Boost/Cut des Low Shelf. |
| EQ Peak 1 Frequency | 100 … 2000 | 500 | Hz | Mittenfrequenz des ersten parametrischen Peak-Bands. |
| EQ Peak 1 Gain | −18 … +18 | 0 | dB | Boost/Cut des ersten Peak-Bands. |
| EQ Peak 1 Q | 0.2 … 5.0 | 0.7 | — | Bandbreite des ersten Peak-Bands (höher = schmaler). |
| EQ Peak 2 Frequency | 500 … 8000 | **2800** | Hz | Mittenfrequenz des zweiten parametrischen Peak-Bands — ein „Presence/Definition"-Ankerpunkt in den oberen Mitten. |
| EQ Peak 2 Gain | −18 … +18 | 0 | dB | Boost/Cut des zweiten Peak-Bands. |
| EQ Peak 2 Q | 0.2 … 5.0 | 0.7 | — | Bandbreite des zweiten Peak-Bands. |
| EQ High Shelf Frequency | 2000 … 16000 | **5000** | Hz | Eckfrequenz des High Shelf. |
| EQ High Shelf Gain | −18 … +18 | 0 | dB | Boost/Cut des High Shelf. |

### IR-Loader (Cabinet-Simulation)

Eine faltungsbasierte (Convolution) Cab-Sim-Stufe, die jetzt **nur das Mid+High-Signal nach der Summierung** verarbeitet (in v0.2.0 verschoben — in v0.1.x saß sie ganz am Ende der Kette). Standardmäßig aus. Ohne geladene Impulsantwort ist diese Stufe bei jeder Session-Samplerate ein garantiert bitgenauer Durchlauf, sodass sie einzuschalten, bevor eine IR geladen ist, deinen Sound nie verändert. Das Low-Band läuft strukturell nie durch diese Stufe, passend zur „Low-Band umgeht die Cabsim"-Architektur der Referenzklasse — dein Grundton-/Sub-Anteil bleibt unabhängig davon, welche Cab-IR du lädst, ungefärbt.

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| IR Enable | off/on | off | — | Aktiviert die IR-Loader-Stufe. |
| IR Mix | 0 … 100 | 100 | % | Blend zwischen dem trockenen (Pre-Convolution-) und dem vollständig gefalteten Mid+High-Signal. |

*Impulsantworten laden:* v0.2.0 liefert weiterhin keinen In-Plugin-Dateibrowser und keine Factory-Cabinet-IRs (beides steht für einen späteren Milestone zusammen mit dem Custom-GUI auf der Roadmap). Die IR-Loading-DSP-Engine selbst ist vollständig implementiert und echtzeitsicher.

## State-Migration (v0.1.x → v0.2.0)

Öffnest du eine Crypta-v0.1.x-Session, wird der alte einzelne Wert `Crossover Frequency` auf den neuen Parameter **Split High** migriert, begrenzt auf dessen neuen Bereich von 300–2000 Hz (der eigene Werks-Default von v0.1.x, 250 Hz, liegt unterhalb dieser Untergrenze, sodass eine unveränderte v0.1.x-Session beim erneuten Öffnen exakt bei 300 Hz landet). Split Low und jeder neue Mid-Band-/Tight-Parameter fallen auf ihre v0.2.0-Defaults zurück. Alle Low-Band-Kompressor-Einstellungen, die du bewusst von den alten Defaults von v0.1.x abweichend geändert hattest, bleiben unverändert erhalten — nur der *Werks-Default* hat sich geändert, nicht deine eigenen bewussten Einstellungen. Das ist eine Best-Effort-, verlustbehaftete Migration in eine Richtung; prüfe nach dem Wiederöffnen einer alten Session dein Low-/Mid-/High-Gleichgewicht erneut.

## Tipps

- **Beginne mit einem engen Low-Band, stelle dann den „Rachen" des Mid-Bands ein, danach den Grind des High-Bands.** Setze zuerst Low Comp Mix und Makeup, damit sich der Grundton fest verankert anfühlt, stelle dann Mid Drive für den „kehligeren" durchsetzungsfähigen Charakter ein, und wähle erst danach ein High-Voicing samt Drive-Menge.
- **Split Low und Split High sind Klangentscheidungen, nicht nur technische.** Split Low nach oben zu schieben, verschiebt mehr Notenkörper aus dem (nur komprimierten) Low-Band heraus; Split High nach oben zu schieben, verbreitert den eigenen Durchlassbereich des Mid-Bands und gibt dem „kehligeren" Charakter mehr Raum, bevor der eigene Fuzz-/Presence-Charakter des High-Bands übernimmt.
- **High Tight ist dein wichtigster „Fuzz vs. Tightness"-Regler**, unabhängig davon, welches Voicing du gewählt hast — zieh ihn Richtung seiner Untergrenze von 20 Hz für maximalen Fuzz, drehe ihn Richtung 500 Hz für straffere, kontrolliertere Höhen. Er zähmt außerdem Härte bei heißen Drive-Einstellungen.
- **High Blend ist dein „Wie viel"-Regler, High Drive dein „Wie hart"-Regler.** Wirkt ein Voicing zu extrem, versuche zuerst, Blend zu senken statt Drive — so behältst du oft mehr vom Charakter, nur bei insgesamt geringerer Intensität, statt die Nichtlinearität selbst zu glätten.
- **Lass den Safety Clip beim Tracking/Mixing aus**, und greife nur dann dazu, als Absicherung gegen unerwartete Automation oder einen zu heißen Eingang bei einem bestimmten Take — er ist ein Sicherheitsnetz, kein Teil des beabsichtigten Tone-Shaping-Signalpfads.
