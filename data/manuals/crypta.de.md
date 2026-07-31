<!-- German translation of crypta.en.md (source repo twist-your-guts, pre-rename; this plugin now ships as Crypta) — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Crypta-Icon" width="120"/></p>

# Crypta — Bedienungsanleitung

*Teile deinen Bass. Komprimiere die Tiefen. Dreh den Höhen die Gedärme raus.*

## Was es ist

Crypta ist ein **paralleler Bass-Prozessor**, entwickelt für Metal-Produktionen, in der Tradition der Referenzklasse für parallele Bus-Bass-Verarbeitung. Seit v0.2.0 teilt es dein Bass-Signal mit zwei kaskadierten Linkwitz-Riley-Frequenzweichen 4. Ordnung („LR4") in **drei** Bänder auf — Low, Mid und High —, hält das Low-Band mit einem Parallel-Kompressor eng zusammen, treibt das Mid-Band mit gestufter Sättigung an und schickt das High-Band durch eine Auswahl von drei Distortion-Voicings, bevor am Ende alles über ein 4-Band-EQ und einen Cabinet-Simulation-IR-Loader wieder zusammengeführt wird.

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

### Gemeldete Latenz

Crypta ist nicht latenzfrei: Oversampling ist die Quelle. **Die gemeldete Latenz ist ausschließlich eine Funktion der Samplerate, identisch über beide Drive Engines bei jeder Rate** (44,1 / 48 / 96 / 192 kHz), und unabhängig von der Host-Blockgröße. Das ist Absicht: Die beiden Engines können unterschiedliche intrinsische Latenzen haben (der Oversampling-Faktor von Circuit passt sich der Host-Rate an — 4x bis 50 kHz, 2x bis 100 kHz, 1x darüber; Classic ist immer 4x), also meldet das Plugin, statt die Latenz jedes Mal neu zu melden, wenn du **Drive Engine** automatisierst — was Hosts mitten im Transport schlecht handhaben —, das Maximum über beide Engines und polstert den Circuit-Pfad darauf auf. Ein Wechsel der Drive Engine verschiebt deine Spur also nie um ein Sample.

Eine Konsequenz, die man kennen sollte: Die *gemeldete* Zahl ist die Oversampling-Verzögerung, keine vollständige Group-Delay-Beschreibung. Bei Classic erreicht ein Test-Impuls seinen Peak innerhalb von 1 Sample der gemeldeten Latenz; bei Circuit innerhalb von 32 Samples, weil die zwei zusätzlichen IIRs, die das High-Band von Circuit trägt (der 10-Hz-DC-Blocker und der drive-getrackte Pole), den Peak des Impulses um bis zu rund 25 Samples (etwa 0,5 ms) verschieben, ohne zu ändern, was gemeldet wird. Keine einzelne Zahl kann eine frequenzabhängige Group Delay beschreiben — garantiert ist stattdessen, dass die gemeldete Zahl über Engines und Sampleraten hinweg übereinstimmt, und dass die Drei-Band-Summe bei jeder getesteten Split-Frequenz-Kombination flach bleibt (≤ 1,0 dB Abweichung).

Keine absolute Sample-Zahl ist in diesem Handbuch als Konstante fixiert — prüfe die eigene Anzeige der Plugin-Delay-Kompensation deines Hosts für die exakte Zahl bei der Samplerate deiner Session.

## Presets

Crypta bringt ein Preset-System mit: Eine horizontale Leiste am oberen Rand des Plugin-Fensters lässt dich durch Werks- und eigene Presets blättern (`<` / Preset-Name / `>`), deine eigenen speichern/als-speichern/löschen und einzelne Presets oder Preset-Bänke (Zip-Dateien mit mehreren Presets) importieren/exportieren. In v0.2.0 sind neun Werkspresets enthalten — was jedes einzelne demonstriert, steht in `docs/presets.md`. Eigene Presets werden pro Plugin gespeichert unter:

- **macOS**: `~/Library/Audio/Presets/Yves Vogl/Crypta/`
- **Windows**: `%APPDATA%\Yves Vogl\Crypta\Presets\`

Eine frische Instanz lädt ein eigenes „Default"-Preset, falls du eines gespeichert hast („Set current as default" im Preset-Menü), sonst das Werks-„Default"-Preset (das den unten dokumentierten reinen Parameter-Defaults entspricht).

## Engines (NEU in v0.3.0)

Drei Parameter wählen zwischen dem DSP aus v0.2.0 und seinem Ersatz aus v0.3.0. Eine **neue** Instanz startet in den neuen Engines; **jede Session und jedes Preset, das du vor v0.3.0 gespeichert hast, behält die alten**, sodass sich an nichts, was du bereits gemacht hast, der Klang ändert. Wechsle frei — die Änderung ist überblendet, nicht gestuft.

| Parameter | Optionen | Default (frische Instanz) | Was sich ändert |
|---|---|---|---|
| Drive Engine | Classic / Circuit | Circuit | *Classic* ist exakt das Mid- und High-Band aus v0.2.0. *Circuit* baut beide aus Schaltungsmodellen neu auf, mit weit weniger Aliasing (25–30 dB besser) und Pre-/Post-Emphasis-Netzwerken pro Voicing. |
| Low Comp Detector | Classic Peak / Smooth RMS | Smooth RMS | *Classic Peak* ist der Detektor aus v0.2.0. *Smooth RMS* misst über ein Fenster, das länger als eine Bassperiode ist, sodass das Low-Band bei getragenen tiefen Noten nicht mehr tremoliert. |
| Gate Mode | Classic / Modern | Modern | *Classic* ist das Gate aus v0.2.0. *Modern* ergänzt Hysterese, Hold, einen Sidechain-Hochpass nur im Detektor und ein geradliniges Release. |

**Wenn dir der alte Sound lieber war**, stelle die betreffende Engine auf Classic — sie ist exakt erhalten, nicht angenähert.

## Parameter-Referenz

Sofern nicht anders angegeben, sind alle kontinuierlichen Parameter geglättet (Smoothing), um Zipper-Noise bei Automation zu vermeiden.

### IO / Global

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| Input Gain | −24 … +24 | 0 | dB | Trimmt das Signal, bevor irgendetwas anderes in der Kette passiert. Nutze das, um ein hohes, aber nicht clippendes Signal in die Gate-/Kompressor-/Drive-/Voicing-Stufen zu bekommen — all ihre Thresholds sind unter der Annahme eines einigermaßen „Line-Level"-Eingangs kalibriert. |
| Output Gain | −24 … +24 | 0 | dB | Finaler Output-Trim, angewendet nach allem anderen (einschließlich des Safety Clip). |
| Bypass | off/on | off | — | Erzwingt einen bitgenauen Durchlauf des Eingangssignals. Auch als hostseitiger Bypass-Parameter des Plugins verfügbar, sodass auch der eigene Bypass-Button/die Automationsspur deiner DAW funktioniert. |
| Safety Clip | off/on | off | — | Ein weicher Ceiling-Clip auf der allerletzten Stufe vor dem Output-Trim. Standardmäßig aus; schalte ihn als Sicherheitsnetz gegen versehentliches hartes Clipping ein, nicht als Tone-Shaping-Werkzeug. Seit v0.3.0 ist er antialiased und unterhalb des Ceilings wirklich transparent — ihn scharf zu stellen färbt nichts mehr, bis tatsächlich etwas das Ceiling erreicht. |
| Clip Ceiling | −12 … 0 | 0 | dBFS | Wo der Safety Clip zu arbeiten beginnt. Wird nur gelesen, solange Safety Clip an ist. 0 dBFS reproduziert das Verhalten aus v0.2.0. |

### Noise Gate (Full-Band, vor dem Crossover-Split)

Sitzt vor beiden Frequenzweichen, gatet also das Eingangssignal als Ganzes statt pro Band.

**Gate Ratio ist Classic-only.** Modern ist ein Gate mit einer Range-Untergrenze statt eines Ratio-Expanders und ignoriert es.

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| Gate Enable | off/on | **off** | — | Aktiviert das Gate. Standardmäßig aus — die meisten bereits aufgenommenen Bass-DI-/Amp-Signale brauchen keins, und ein falsch eingestelltes Gate kann legitimes leises Spiel abschneiden (Ghost Notes, Ausklingen). |
| Gate Threshold | −80 … 0 | −60 | dB | Signalpegel, unterhalb dessen das Gate zu dämpfen beginnt. |
| Gate Ratio | 1 … 20 | 10 | :1 | Wie aggressiv das Gate unterhalb des Thresholds dämpft. Höher = näher an einem harten Mute. |
| Gate Attack | 0.1 … 50 | 1 | ms | Wie schnell das Gate öffnet, sobald das Signal wieder über den Threshold steigt. |
| Gate Release | 5 … 500 | 100 | ms | Wie schnell das Gate schließt, sobald das Signal unter den Threshold fällt. |
| Gate Hysteresis | 0 … 12 | 4 | dB | *Nur Modern.* Wie weit unter den Threshold das Signal fallen muss, bevor das Gate zu schließen beginnt. Das ist es, was verhindert, dass eine durch den Threshold ausklingende Note das Gate stottern lässt. |
| Gate Hold | 0 … 500 | 20 | ms | *Nur Modern.* Hält das Gate nach dem Abfallen des Signals so lange offen und startet bei jedem neuen Transienten neu — damit es zwischen schnellen Noten nicht zuschlägt. |
| Gate SC Highpass | 20 … 400 | 80 | Hz | *Nur Modern.* Hochpasst ausschließlich den **Detektor** des Gates; das Audio bleibt unangetastet. Höher drehen, wenn eine klingende tiefe Saite das Gate offen hält. |
| Gate Range | 6 … 90 | 60 | dB | *Nur Modern.* Wie stark ein vollständig geschlossenes Gate dämpft, und die Höhe, durch die die Release-Rampe fällt. Ein Gate, das nur 12 dB absenkt, klingt oft natürlicher als eines, das ganz zumacht. |

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
| Low Comp Knee | 0 … 18 | 6 | dB | *Nur Smooth RMS.* Breite des Soft Knee um den Threshold. 0 dB ist ein Hard Knee; breitere Einstellungen beginnen allmählich zu komprimieren, während sich das Signal dem Threshold nähert, was bei getragenem Bass deutlich unauffälliger ist. |
| Low Comp Auto Release | off/on | on | — | *Nur Smooth RMS.* Dehnt das Release bei getragenem Material und lässt es bei Transienten auf dem eingestellten Wert, sodass eine gehaltene tiefe Note nicht gepumpt wird. |
| Low Comp Auto Makeup | off/on | off | — | Wird von **beiden** Detektoren gelesen. Fügt einen festen Boost hinzu, der etwa die Hälfte des am Threshold weggenommenen Gains kompensiert, sodass eine Threshold-Änderung nicht auch deinen Pegel ändert. Wird mit dem manuellen Makeup-Regler summiert. |

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
| High Bias | 0 … 100 | 0 | % | *Nur Circuit.* Versetzt den Clipper so, dass er asymmetrisch sättigt, und kauft sich damit geradzahlige Harmonische: Bei den symmetrischen Voicings steigt H2/H1 um mindestens 20 dB beim Übergang von Bias 0 zu Bias 100. 0 % ist exakt der Charakter aus v0.2.0. Der Versatz wird weiter hinten von einem 10-Hz-Blocker wieder entfernt, das legt also nie nennenswerten DC auf deinen Output (gemessen ≤ −80 dBFS bei jedem Voicing und jedem Bias-Setting). |

**Voicings:**

Alle drei behalten ihre Platzierung aus v0.2.0 — Gnaw flach, Wool eine −6-dB/Q-0,9-Scoop bei 500 Hz, Razor ein +5-dB/Q-1,0-Hump bei 900 Hz —, aber auf der *Circuit*-Engine sind die Nichtlinearität und die Filterung darum herum aus Schaltungsmodellen neu aufgebaut, statt drei Einstellungen einer Kurve zu sein.

- **Gnaw** — *Classic*: ein Hard-Clip im Op-Amp-Stil, symmetrisch und unnachgiebig, drückt bei hohem Drive stark in Richtung einer rechteckartigen Wellenform. *Circuit*: derselbe Charakter, gewonnen über eine Pre-Emphasis-Shelf (1200 Hz, +6 dB) vor dem Clipper und ihre exakte algebraische Inverse dahinter — das Paar fällt bei Drive 0 *strukturell* auf Eins zusammen, nicht nur näherungsweise, und konzentriert das Clipping auf die oberen Harmonischen statt auf das ganze Band.
- **Wool** — *Classic*: kaskadierter Soft-Clip-Fuzz mit einer Mid-Scoop und einer Prise fixer Asymmetrie. *Circuit*: die eigene DC-Kurve des asymmetrischen Dioden-Shunt-Clippers — zwei Dioden in Serie in eine Richtung, eine in die andere, gelöst aus einer Small-Signal-Dioden-SPICE-Karte per gedämpftem Newton-Verfahren an jedem Tabellenpunkt, beim Laden, nie auf dem Audio-Thread — plus eine dynamische Bias-Sidechain, die den Clipper nach einer lauten Passage für rund 20 ms versetzt lässt. Das macht Wool wirklich history-dependent: Dieselbe leise Probe misst je nach dem, was unmittelbar davor gespielt wurde, um mindestens 3 dB anders, gegen unter 1,5 dB bei den gedächtnislosen Voicings. **Hinweis:** Das ausgelieferte Verhalten ist eine abklingende *Bloom* nach einer lauten Passage, keine *Sag* — das entgegengesetzte Vorzeichen zur ursprünglichen Design-Vorhersage dieses Features. Siehe [Bekannte Einschränkungen](#bekannte-einschränkungen) unten; beschreibe Wool als history-dependent / touch-sensitive, nicht als „Sag".
- **Razor** — *Classic*: ein engeres Overdrive — ein vergleichsweise milder Clipper mit einem Mid-Hump-Filter danach. *Circuit*: neu aufgebaut als Feedback-Clipper-Faktorisierung („unity clean + geclippte Differenz"), mit der Pre-Emphasis-Ecke des geclippten Pfads, verschoben vom 720-Hz-Original eines Gitarrenpedals runter auf 330 Hz für den Bassbereich, und einer weicher gekneeten Tanh-gefitteten Clipping-Kurve, die besser zur modellierten Topologie passt.

Gnaw und Razor teilen sich auf Circuit außerdem einen drive-getrackten Post-Clip-Pole: Er öffnet bei Drive 0 auf 61 kHz (transparent) und gleitet bei vollem Drive runter auf 5,1–6,9 kHz, dazwischen kontinuierlich bewegt statt an einer einzelnen fixen Ecke zu sitzen.

*Ausgangspunkte, kein finales Voicing:* Die Drive-Gain-Bereiche und die Mid-Filter-Hump-/Scoop-Einstellungen für die Classic-Engine, ebenso wie die Circuit-Voicing-Konstanten, sind Engineering-Defaults — auf musikalische Brauchbarkeit abgestimmt und mathematisch begrenzt (kein durchgehender Output bei keiner Drive-Einstellung), aber noch nicht gehörmäßig gegen Referenzmaterial finalisiert. Die offenen Ear-Tuning-Gates der Suite (Issues #15/#16/#17, #34) gelten weiterhin speziell für die Circuit-Engine.

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

## State-Migration

### v0.2.x → v0.3.0

Eine vor v0.3.0 gespeicherte Session zu öffnen oder ein solches Preset zu laden setzt **Drive Engine**, **Low Comp Detector** und **Gate Mode** auf ihre Classic-Werte, sodass deine gespeicherte Arbeit exakt wie zuvor klingt. Das gilt gleichermaßen für Host-Sessions und für deine eigenen gespeicherten Presets, einschließlich eines eigenen Presets namens „Default" — hattest du also deinen eigenen Default gespeichert, bekommst du bei einer neuen Instanz weiterhin genau den.

Die eine bewusste Ausnahme ist der **Safety Clip**: Hattest du ihn eingeschaltet, ist der Clipper von v0.3.0 nicht bit-identisch mit dem von v0.2.0. Er aliast weit weniger und ist unterhalb des Ceilings transparent; der Unterschied beschränkt sich auf Material, das tatsächlich geclippt wurde.

Neue Parameter (High Bias, die Knee- und Auto-Regler, die Regler des Modern-Gates, Clip Ceiling) sind entweder per Default neutral oder werden nur gelesen, wenn ihre Engine gewählt ist — und die wählt Legacy-State nie.

### v0.1.x → v0.2.0

Öffnest du eine Crypta-v0.1.x-Session, wird der alte einzelne Wert `Crossover Frequency` auf den neuen Parameter **Split High** migriert, begrenzt auf dessen neuen Bereich von 300–2000 Hz (der eigene Werks-Default von v0.1.x, 250 Hz, liegt unterhalb dieser Untergrenze, sodass eine unveränderte v0.1.x-Session beim erneuten Öffnen exakt bei 300 Hz landet). Split Low und jeder neue Mid-Band-/Tight-Parameter fallen auf ihre v0.2.0-Defaults zurück. Alle Low-Band-Kompressor-Einstellungen, die du bewusst von den alten Defaults von v0.1.x abweichend geändert hattest, bleiben unverändert erhalten — nur der *Werks-Default* hat sich geändert, nicht deine eigenen bewussten Einstellungen. Das ist eine Best-Effort-, verlustbehaftete Migration in eine Richtung; prüfe nach dem Wiederöffnen einer alten Session dein Low-/Mid-/High-Gleichgewicht erneut.

## Unter der Haube

Alles Folgende ist im Repository gemessen und läuft bei jedem CI-Push (macOS + Windows, Release, `.github/workflows/ci.yml`, plus `pluginval --strictness-level 10` auf beiden Plattformen und `auval -strict` auf macOS). Die vollständigen Herleitungen stehen in `docs/architecture.md`.

### Eine gemeinsame Oversampling-Region, keine zwei

v0.2.0 fuhr **zwei** unabhängige 4x-Oversampling-Instanzen — eine innerhalb des Mid-Bands, eine innerhalb des High-Bands. Die Circuit-Engine kollabiert sie zu **einer**: Der Rest wird einmal hochgesampelt, durch eine zweite Linkwitz-Riley-Weiche geteilt, die *bei der oversampleten Rate* läuft, dort verarbeitet, summiert und einmal runtergesampelt. Die eingesparte Region bezahlt die zusätzliche Filterung pro Voicing. Der Oversampling-Faktor passt sich der Host-Rate an — 4x bis 50 kHz, 2x bis 100 kHz, 1x (nur ADAA) darüber —, und dieser Trade ist getestet, nicht angenommen: 2x bei 96 kHz misst mindestens so sauber wie 4x bei 48 kHz, Ton für Ton. Beide Engines bleiben durchgehend vorbereitet, `Drive Engine` ist also automatisierbar; ein Wechsel überblendet über 256 Samples (5,3 ms bei 48 kHz) und spült zuerst den Zustand der eintretenden Engine, weil die Oversampling-History der untätigen Engine sonst beim Zurückschalten einen Burst mit veraltetem Audio freisetzt (gemessen: ein Peak von 1,96 vor dieser Spülung, 1,39 danach).

### Anti-Aliasing arithmetisch, obendrauf auf Oversampling

`src/dsp/ADAAShaper.h` implementiert Antiderivative Anti-Aliasing 1. Ordnung (Parker, Zavalishin & Le Bivic, DAFx-16): geschlossene Formen, wo die Antiderivative elementar ist (`tanh` → `ln cosh`, Hard Clip → stückweise), und eine 2048-Punkte-kubisch-interpolierte Tabelle mit Simpson-integrierter Antiderivative, wo das nicht der Fall ist, sodass Kurve und Integral konsistent zueinander bleiben — direkt durch einen Test abgesichert, weil eine Abweichung sich als DC-Sprung bei Übersteuerung zeigen würde statt als kleiner Fehler. Gemessenes Ergebnis: Die Circuit-Engine schlägt die abgelöste Engine um **25–30 dB** über einen 1,2–10-kHz-Sweep bei vollem Drive (aufgezeichnet: Circuit −81,9 / −64,0 / −57,1 / −51,9 dB gegen Classic −48,0 / −36,2 / −27,9 / −22,7 dB bei 1244 / 2489 / 4978 / 9956 Hz), und erreicht **−80 dB oder besser über den gesamten Bassbereich** (311, 622, 1244 Hz).

### Schaltungstopologien pro Voicing

Siehe den Hinweis zu den Voicings über den Parameter-Tabellen oben für das, was sich bei Gnaw, Wool und Razor geändert hat. Der drive-getrackte Post-Clip-Pole, den sich Gnaw und Razor teilen, nutzt eine Square-Law-Abbildung (Audio-Taper) statt einer linearen, gezielt damit der Pole bei halbem Drive über 12 kHz bleibt, statt auf rund 9 kHz zu kollabieren und die Mitte des Drive-Bereichs hörbar dumpfer zu machen als die modellierte Schaltung. Jeder automatisierbare Skalar in der Circuit-Engine — Drive-Gains, Blend, Bias-Offset, Band-Level, und die zwei One-Pole-Filterkoeffizienten selbst — wird über den Block gerampt statt konstant gehalten; ein pro-Block-konstanter Parameter maß vor dieser Änderung rund −27 dBc breitbandige nichtharmonische Spurious-Anteile bei einem schnellen Drive-Sweep.

### Ein Low-Band-Detektor, der den Bass nicht tremolieren lässt

Das Low-Band von v0.2.0 nutzte einen Peak-Detektor mit dem sourcierten 6-ms-„Glue"-Release, und ein 6-ms-Release folgt den einzelnen Halbzyklen einer Bass-Grundfrequenz, die Gain Reduction rippelte also mit der doppelten Notenfrequenz. `Low Comp Detector = Smooth RMS` ist ein Log-Domain-RMS-Detektor mit Soft Knee, programmabhängigem Release und Auto-Makeup. Gemessenes Ripple auf einem 80-Hz-Ton 6 dB über Threshold: **über 1 dB → unter 0,5 dB**, bei weiterhin echter Kompression. Das Vorzeichen des Auto-Makeup ist wissenswert: `−0,5·T·(1 − 1/R)` ergibt bei negativem Threshold eine positive Gain — der naheliegende Fehler (`−0,5·T·(1/R − 1)`) würde stattdessen Dämpfung erzeugen, was die Testsuite an drei Ankerpunkten auf 0,1 dB genau absichert, plus eine Prüfung, dass das Ergebnis überhaupt ein Boost ist.

### Ein Gate mit Hysterese, und der Test, der es beweist

`Gate Mode = Modern` fährt seinen Kontrollpfad pro Sample und ergänzt Hysterese (0–12 dB), Retrigger-Hold (0–500 ms), einen Sidechain-Hochpass nur im Detektor (20–400 Hz) und ein dB-lineares Release. Der sauberste Beweispunkt: ein 500-Hz-Ton, der zwei Sekunden lang ±1,5 dB um den Threshold bei 3 Hz dithert — ein Single-Threshold-Gate chattert dabei durchgehend; mit einem 4-dB-Hysterese-Fenster öffnet dieses hier einmal und macht dann **exakt null Übergänge** für den Rest des Renders. Das Release ist per Least-Squares gegen die ideale `−Range/Release`-Flanke bei R² > 0,99 gefittet. `Gate Ratio` ist nur bei Classic relevant; Modern ignoriert es — es ist ein Gate mit einem Range-Boden, kein Ratio-Expander.

### Ein Safety Clip, der transparent ist, bis er es nicht mehr ist

Der Safety Clip von v0.2.0 war ein rohes Per-Sample-`std::tanh` auf dem gesamten Mix, das alles tiefpasste, sobald es nur scharfgeschaltet war. `src/dsp/OutputClipper.h` wendet ADAA stattdessen auf das **Residuum** des Clippers an — algebraisch der antialiaste Clipper plus ein exakter Kompensator für den Abfall und die Verzögerung, die naives ADAA sonst auf Material weit weg von der Ceiling anwenden würde. Gemessene Abweichung über 40 Hz – 20 kHz bei scharfgeschaltet, aber nicht clippend: **0,13 dB**. Eine dokumentierte Falte: Der Kompensator ist eine erste Differenz und kann bei schnellem Material ein Sample zurück über die Ceiling drücken (gemessen 1,15 gegen eine Ceiling von 1,0), also wird eine finale harte Grenze angewendet — sie greift nie unterhalb der Ceiling, Transparenz darunter bleibt also unangetastet.

### An dem, was du schon gebaut hast, ändert sich nichts

Eine frische Instanz startet mit Circuit / Smooth RMS / Modern; jede Session und jedes Preset von vor v0.3.0 bekommen die Legacy-Engines injiziert, über zwei unabhängige Migrationspfade, weil Presets `setStateInformation()` nie durchlaufen (siehe State-Migration oben). Der Beweis läuft gegen echten committeten Output, nicht nur gegen den Migrationscode: `tests/GoldenRenderTests.cpp` rendert vier committete v0.2.0-State-Fixtures (Gnaw / Wool / Razor / Gnaw-mit-Clip) und prüft **sample-exakte Gleichheit (`memcmp == 0`) auf macOS**, der Golden-Plattform; auf Windows liegt die Grenze bei ≤ −60 dB relativ, mit dem schlechtesten von drei Fixtures gemessen bei −73 dB. Die Fixtures sind nachweislich frei von einem `stateVersion`-Attribut, sodass ein neu generiertes Fixture den Migrationstest nicht still zu einer Tautologie machen kann.

### Engineering-Hygiene

Keine Heap-Allokationen auf dem Audio-Thread, bei **beiden** Engines, mit jedem v0.3.0-Feature gleichzeitig live — Circuit Drive, Modern Gate, Smooth-RMS-Detektor mit Auto-Makeup, der Safety Clip und der EQ. Die gemeldete Latenz ist ausschließlich eine Funktion der Samplerate (siehe Gemeldete Latenz oben). `reset()` spült jede Stufe (Crossover-Speicher, Gate-/Kompressor-Hüllkurven, Oversampling-Zustand, die Latenz-Kompensations-Delay-Line, EQ-Biquad-History, die Convolution-Engine), sodass ein Host-Transport-Stopp/Loop/Rewind nie veralteten Zustand in das nachklingen lässt, was als Nächstes spielt. Das Low-Band ist strukturell von der Cab-Sim ausgeschlossen: Sein eigener isolierter Output ist bit-exakt identisch, ob der IR-Loader an oder aus ist, unabhängig davon, welche IR geladen ist.

## Bekannte Einschränkungen

- **Der dynamische Bias von Wool hat das entgegengesetzte Vorzeichen zu dem, was das ursprüngliche Design vorhersagte.** Das Design-Briefing erwartete, dass eine laute Passage die folgende leise Probe unterdrückt („Sag"); ausgeliefert wurde stattdessen eine abklingende **Bloom**. Der Mechanismus ist verstanden und ist getreues analoges Verhalten: Der Bias macht das Clipping asymmetrisch, asymmetrisches Clipping erzeugt echtes DC, und der 10-Hz-Blocker weiter hinten stellt es dann über seine eigene ~16-ms-Zeitkonstante wieder her, sodass die Probe auf einer Bloom reitet statt auf einem Dip. Die History-Abhängigkeit selbst ist wie beabsichtigt bestätigt (11 dB auf Wool gegen 1 dB bei den gedächtnislosen Voicings). Das ist für das offene Ear-Tuning-Gate der Suite vorgemerkt (Issues #15/#16/#17, #34) — beschreibe Wool als history-dependent / touch-sensitive, nicht als „Sag".
- **Die Circuit-Voicing-Konstanten bleiben Engineering-Ausgangspunkte**, noch nicht gehörmäßig gegen Referenzmaterial finalisiert — dieselbe Offenlegung, die v0.1.x und v0.2.0 schon für die Drive-Gain-Bereiche und Character-Filter-Settings trugen.
- **Der Alias-Boden wird pro Ton genannt, nicht als eine flache −80-dB-Grenze, und der Grund ist arithmetisch.** Gnaw ist ein 40x-Hard-Clip, dessen harmonische Reihe wie 1/n ohne Bandbreitenbegrenzung abfällt, der Boden wird also davon bestimmt, welche Harmonischen-Ordnung zurück ins Band faltet, und diese Ordnung sinkt, je höher die Grundfrequenz steigt. Die Engine auf 8x Oversampling zu heben wurde gemessen und verfehlt −80 dB bei den oberen Tönen weiterhin, bei doppelten Kosten der Stufe. Stattdessen ausgeliefert: 25–30 dB besser als die vorherige Engine bei jedem Ton (gegen eine 10-dB-Anforderung im Briefing), −80 dB oder besser über den gesamten Bassbereich, und ein −49-dB-In-Band-Boden überall.
- **Die beiden Engines sind bei Drive 0 oberhalb von 3 kHz nicht identisch, und das wird nicht behauptet.** Parität hält bis 3 kHz auf ±0,5 dB; darüber ist Circuit bis zu 2,5 dB heller (gemessen +0,5 dB bei 8 kHz, +2,5 dB bei 14 kHz), weil sein Tone-Tiefpass bei der oversampleten Rate läuft und der bilinearen Frequenzverzerrung entgeht, die das Basisraten-Filter von Classic hat.
- **Der drive-getrackte Pole öffnet bei Drive 0 auf 61 kHz**, nicht auf die 24 kHz, die das ursprüngliche Design-Briefing verlangte — ein One-Pole bei 24 kHz liegt bei 18 kHz bereits bei etwa −1,9 dB und hätte die eigene Transparenz-Anforderung dieses Features nicht erfüllt, während 61 kHz (−0,36 dB bei 18 kHz) auch die Zahl ist, die die Schaltungsrecherche für das reale Vorbild angibt.
- **CPU ist hier eine Design-Absicht, kein Benchmark.** Zwei Oversampling-Regionen zu einer zu kollabieren finanziert die zusätzliche Filterung pro Voicing, und die Release Notes nennen den Trade als etwa auf dem CPU-Niveau von v0.2.0 landend. In der Testsuite ist keine CPU-Messung enthalten — setze keine Prozentzahl oder „x % leichter"-Angabe irgendwo hin.
- **Der Safety Clip tauscht seinen Anti-Aliasing-Vorteil bei extremer Übersteuerung gegen seine Ceiling-Garantie.** Der Delta-Form-Kompensator kann bei schnellem Material ein Sample zurück über die Ceiling drücken, also wird eine finale harte Grenze angewendet; sie greift nie unterhalb der Ceiling, aber rund 10 dB oder mehr darüber verschwindet der Anti-Aliasing-Vorteil. Bewusste Priorisierung — ein Safety Clip, der Material durchlässt, ist kein Safety Clip, und hartes Clipping gehört zu den Drive-Stufen, die genau dafür oversampled und ADAA'd sind.
- **Eine bewusste Abweichung vom Output von v0.2.0: der scharfgeschaltete Safety Clip.** War er bei dir aktiv, ist v0.3.0 nicht bit-identisch — es aliast weit weniger und ist unterhalb der Ceiling transparent. Der Unterschied beschränkt sich auf Material, das tatsächlich geclippt wurde, und ist begrenzt (gemessen −26,5 dB relativ bei einem Fixture, das 12 dB über die Ceiling getrieben wurde). Alles andere an einer Session oder einem Preset von vor v0.3.0 ist sample-exakt.
- **Bit-Exaktheit über Toolchains hinweg ist unerreichbar und wird nicht behauptet.** macOS ist die Golden-Plattform; auf Windows liegt die Grenze bei −60 dB relativ, mit dem schlechtesten von drei Fixtures gemessen bei −73 dB. Der Drift ist kein reines Letzte-Stelle-Rauschen — sowohl das Gate als auch der Low-Band-Kompressor treffen Entscheidungen anhand eines Detektor-Pegels, ein 1-Stelle-Unterschied nahe einem Threshold kann also einen Übergang um ein Sample verschieben.
- **Die GUI ist ein funktionaler generischer Editor** plus eine schlichte beschriftete Meter-Anzeigenzeile. Die photoreale M3-GUI ist ein späterer Meilenstein und wird dieselbe `MeterTaps`-Struktur konsumieren; die Preset-Leiste ist ein rein funktionaler Streifen.
- **Weiterhin kein In-Plugin-IR-Browser und keine gebündelten Werks-Cabinet-IRs.** Die Convolution-Engine ist vollständig implementiert und echtzeitsicher, und ist ohne geladene IR ein garantiert bit-exakter Passthrough, bei jeder Session-Samplerate.
- **Bewusst außerhalb des Umfangs von v0.3.0, offen vorgemerkt:** Werks-IRs / IR-Browser / IR-Trim-Align; die Stereo-Strategie (Low-Mono-Sum-Toggle, Mid/High-Width); vollständige Per-Sample-Newton-DK-Schaltungssimulation (v0.3.0 liefert die kalibrierten faktorisierten Modelle; eine vollständige Simulation ist ein möglicher späterer „HQ Circuit"-Modus); ein Lookahead-Gate und zeitvariantes Auto-Release; Linear-Phase-/HQ-Offline-Oversampling-Modi und ein geteiltes suite-weites Oversampler-Modul.
- **Das Voicing ist recherchebasiert, nie gegen Hardware oder gegen Audio, DSP-Quelle oder Einheit eines Referenzprodukts gemessen.** Wo ein Modell eine bewusste Vereinfachung ist, sagen die Docs das.
- **Pre-1.0 und AGPLv3** — Breaking Changes bis v1.0.0 möglich. Die Umbenennung in v0.1.1 (Plugin-Code `Cryp`, Bundle-ID `com.yvesvogl.crypta`) bedeutet, dass DAWs dies im Vergleich zu Sessions aus der v0.1.0-Ära als neues Plugin behandeln.

## Tipps

- **Beginne mit einem engen Low-Band, stelle dann den „Rachen" des Mid-Bands ein, danach den Grind des High-Bands.** Setze zuerst Low Comp Mix und Makeup, damit sich der Grundton fest verankert anfühlt, stelle dann Mid Drive für den „kehligeren" durchsetzungsfähigen Charakter ein, und wähle erst danach ein High-Voicing samt Drive-Menge.
- **Split Low und Split High sind Klangentscheidungen, nicht nur technische.** Split Low nach oben zu schieben, verschiebt mehr Notenkörper aus dem (nur komprimierten) Low-Band heraus; Split High nach oben zu schieben, verbreitert den eigenen Durchlassbereich des Mid-Bands und gibt dem „kehligeren" Charakter mehr Raum, bevor der eigene Fuzz-/Presence-Charakter des High-Bands übernimmt.
- **High Tight ist dein wichtigster „Fuzz vs. Tightness"-Regler**, unabhängig davon, welches Voicing du gewählt hast — zieh ihn Richtung seiner Untergrenze von 20 Hz für maximalen Fuzz, drehe ihn Richtung 500 Hz für straffere, kontrolliertere Höhen. Er zähmt außerdem Härte bei heißen Drive-Einstellungen.
- **High Blend ist dein „Wie viel"-Regler, High Drive dein „Wie hart"-Regler.** Wirkt ein Voicing zu extrem, versuche zuerst, Blend zu senken statt Drive — so behältst du oft mehr vom Charakter, nur bei insgesamt geringerer Intensität, statt die Nichtlinearität selbst zu glätten.
- **Lass den Safety Clip beim Tracking/Mixing aus**, und greife nur dann dazu, als Absicherung gegen unerwartete Automation oder einen zu heißen Eingang bei einem bestimmten Take — er ist ein Sicherheitsnetz, kein Teil des beabsichtigten Tone-Shaping-Signalpfads.
