<!-- German translation of firmament.en.md (English source generated from firmament/docs/manual.md on 2026-07-16) — do not hand-edit; re-translate after the English manual is resynced. -->

<p align="center"><img src="assets/icon.png" alt="Firmament-Icon" width="120"/></p>

# Firmament — Bedienungsanleitung

*Öffne den Himmel – ein Stereo-Widener und Imager für üppige orchestrale Layer.*

## Was Firmament ist

Firmament ist ein Mid/Side-Stereo-Widener und -Imager. Es ist eines von zwölf Plugins in der Heavy-Music-Suite von **Basilica Audio**, und seine Aufgabe in dieser Suite (und in jedem Mix) ist es, Inhalte, die bereits Stereoinformation besitzen – Streicher, Chöre, Synth-Pads, gedoppelte/geschichtete Gitarren, Ambience-Returns –, zu nehmen und zu steuern, wie breit sie sich anfühlen, ohne je zu beeinträchtigen, wie der Mix auf Mono zusammenfällt (Club-PA, Handylautsprecher, ein Broadcast-Mono-Check, ein Bassist, der seinen Part in Mono prüft).

Firmament erzeugt keine Stereobreite aus einem echt monofonen Signal von sich aus (Width und Low Width können nur skalieren, welche Stereo-Differenz im Input bereits vorhanden ist) – die eine Ausnahme ist **Haas Mode**, der aus mono-kompatiblem Material *tatsächlich* ein Breitegefühl erzeugen kann, indem er einen Kanal verzögert, auf Kosten der exakten Mono-Summen-Garantie, die der Rest des Plugins bietet (siehe unten).

## Wo es in einer Heavy-Music-Produktionskette sitzt

Firmament ist ein **Width-/Imaging**-Werkzeug, was es eher ans hintere Ende einer Kanal- oder Bus-Kette rückt, nachdem Tone-Shaping und Dynamik bereits entschieden sind:

1. **Korrektives/tonales EQ, Kompression, Saturation** (z. B. `overture`, `tenebrae`, andere Suite-Mitglieder) – zuerst den Klang formen.
2. **Firmament** – entscheiden, wie breit es sich anfühlen soll, sobald der Ton steht.
3. **Reverb-/Delay-Sends, finale Bus-Bearbeitung** – Width-Entscheidungen vor dem Reverb beeinflussen, wie der Reverb-Tail selbst wahrgenommen wird; manche Engineers verbreitern lieber erst nach dem Reverb-Return, was je nach Quelle eine valide Alternative ist.

Typische Platzierungen in einer Heavy-Music-Produktion:

- **Streicher-/Chor-/Pad-Busse** – der primäre Anwendungsfall. Fahre Width hoch, um die orchestralen/chorischen Layer zu öffnen, ohne die Gitarren/den Bass/die Kick zu verschmieren, die sich den Mix teilen.
- **Gedoppelter Rhythmusgitarren-Bus** – eine sanftere Hand (Width 110–140 %) kann zwei bereits gepannte Doubles zu einer einzelnen, breiter wirkenden Wand verkleben, ohne die extremen "gehypten" Artefakte mancher Stereo-Widener, weil Firmament nie etwas hinzufügt, das nicht schon im Stereobild war (wieder abgesehen von Haas Mode).
- **Master-Bus (sparsam eingesetzt)** – Bass Mono ist hier besonders wertvoll: die Kick-/Bass-/Low-Gitarren-Energie zentriert halten (mono-kompatibel, und physisch straffer auf einer PA), während die Becken/Streicher/Reverb-Tails oberhalb der Crossover so breit bleiben, wie der Mix sie bereits hat.
- **Mono-Quellinstrumente, die durch einen Stereo-Bus geroutet werden** – Firmament akzeptiert einen Mono-Input-Bus problemlos (siehe "Mono-Input" unten); in diesem Fall hat Width überhaupt keine Wirkung, es sei denn, Haas Mode ist aktiviert, da es keine Zwischen-Kanal-Differenz zu skalieren gibt.

## Signalfluss (Klartextversion)

Die vollständige technische Aufschlüsselung (Mermaid-Diagramm, exakte Mathematik, das reale Magnitude-/Phasenverhalten der Linkwitz-Riley-Crossover, Real-Time-Safety-Details) findest du in [`docs/architecture.md`](architecture.md). Kurz gesagt:

1. Der Input wird in **Mid** (Mono-Inhalt, `(L+R)/2`) und **Side** (Stereo-Differenz-Inhalt, `(L-R)/2`) aufgeteilt.
2. Ist **Bass Mono** aus, skaliert **Width** das gesamte Side-Signal um einen einzigen Betrag.
3. Ist **Bass Mono** aktiviert, wird Side in ein tiefes Band (unterhalb der Bass-Mono-Frequenz) und ein hohes Band (darüber) aufgeteilt; **Low Width** skaliert das tiefe Band und **Width** skaliert das hohe Band unabhängig davon.
4. Ist **Auto Mono Safety** aktiviert, wird Side zusätzlich automatisch abgeschwächt, sobald der Input stark phasenversetzt ist (ein Sicherheitsnetz gegen Mono-Auslöschung), zusätzlich zu dem, was Width/Low Width bereits getan haben.
5. Mid und das prozessierte Side werden wieder zu Left/Right zusammengeführt. Mid wird von alldem *nie* angetastet – das garantiert die weiter unten beschriebene Mono-Fold-down-Sicherheit.
6. Ist **Haas Mode** aktiviert, wird der rechte Kanal leicht relativ zu Left verzögert – ein anderer, nicht Mid/Side-basierter Verbreiterungs-Trick, der zuletzt angewendet wird, vor dem finalen Trim.
7. **Output** trimmt den Gesamtpegel.

## Parameterübersicht

| Parameter | Bereich | Standard | Einheit | Was es bewirkt |
|---|---|---|---|---|
| **Width** | 0-200 | 100 | % | Skaliert das Side-(Stereo-Differenz-)Signal. 100 % ist das ursprüngliche, unveränderte Stereobild des Inputs. 0 % kollabiert alles auf Mono (Side stummgeschaltet). 200 % verdoppelt die Amplitude des Side-Kanals für ein maximal breites, manchmal "gehyptes"/künstlich wirkendes Bild – in kleinen Dosen nützlich, auf einem ganzen Mix leicht übertrieben. Ist Bass Mono aktiviert, steuert Width nur das Band *oberhalb* der Bass-Mono-Frequenz. |
| **Bass Mono Freq** | 0-500 | 0 (off) | Hz | Die Crossover-Frequenz, unterhalb derer Low Width (statt Width) das Side-Signal steuert. Bei 0 Hz (off) ist das gesamte Spektrum ein einziges, allein von Width gesteuertes Band. Typische Einstellungen liegen im Bereich 80–200 Hz – niedrig genug, um Kick-/Bass-/Low-Gitarren-Grundtöne zentriert zu lassen, hoch genug, um das "boxige" Low-Mid-Stereo-Verschmieren einzufangen, das manche breiten Reverbs/Pads erzeugen. |
| **Low Width** | 0-200 | 0 | % | Unabhängige Width-Skalierung für das Band *unterhalb* von Bass Mono Freq – nur hörbar, solange Bass Mono Freq über 0 Hz liegt. Beim Standardwert von 0 % wird das tiefe Band zwangsweise auf Mono gesetzt, genau wie ein klassisches "Bass-Mono"-Utility – der übliche Mastering-Bus-Move, um Sub-Bass-Energie zentriert zu halten und auf kleineren Systemen gut zu übertragen. Erhöhe ihn über 0 %, wenn du gezielt etwas Breite auch im Tiefbass erhalten willst (selten, aber gelegentlich nützlich bei sehr breitem Pad-/Drone-Material, bei dem selbst der Low-End ein wenig atmen soll). |
| **Auto Mono Safety** | off/on | off | - | Zügelt bei Aktivierung automatisch das Side-Signal, sobald der Input stark phasenversetzt ist (Korrelation tendiert Richtung -1), unabhängig von und zusätzlich zu Width/Low Width. Ein Sicherheitsnetz für automatisiertes Width oder aggressive Einstellungen auf unvorhersehbarem Quellmaterial (z. B. ein verbreitertes Synth-Pad, das gelegentlich stark phasenversetzt wird); es betrifft Mid nie, kann also Firmaments Mono-Fold-down-Garantie nicht brechen – es zügelt nur, *wie* breit Side wird. Lass es aus, wenn du Width nach Gehör einstellst und volle manuelle Kontrolle willst; schalte es als Sicherheitsnetz auf Bussen ein, die du nicht ständig überwachen kannst (z. B. ein automatisierter Width-Send). |
| **Haas Mode** | off/on | off | - | Aktiviert eine alternative Verbreiterungstechnik: verzögert den rechten Kanal um Haas Time relativ zu Left, nach der Mid/Side-Stufe. Das ist der *einzige* Regler in Firmament, der genuin mono-kompatibles Material verbreitern kann (funktioniert sogar bei Width = 0 %) – anders als Width/Low Width bewahrt es aber **keine** exakte Mono-Summen-Übereinstimmung mit dem Input (das Summieren zweier zeitversetzter Kanäle unterscheidet sich grundlegend vom Summieren des Originalpaars). Setze es bewusst ein, und prüfe immer einen Mono-Fold-down, bevor du dich festlegst, falls die Übertragbarkeit für das Ziel wichtig ist (z. B. Broadcast, Club-Systeme). |
| **Haas Time** | 0-40 | 20 | ms | Das Left/Right-Delay, das Haas Mode anwendet, nur hörbar, solange Haas Mode aktiviert ist. Kurze Zeiten (5–15 ms) lesen sich als dezente Verbreiterung; die 15–35-ms-Zone des "Precedence-Effekts" liest sich als starke, immersive Breite; Zeiten nahe 40 ms beginnen, sich eher als eigenständiger Slap/Echo statt als Breite zu lesen – geh zurück, wenn du eine deutliche Wiederholung statt eines breiteren Bildes hörst. |
| **Output** | -24 to +24 | 0 | dB | Finaler Output-Trim, angewendet nach allem anderen (inklusive Haas Mode). Firmament hat keinen eingebauten Limiter oder Ceiling – sowohl Width/Low Width über 100 % als auch Output über 0 dB können Gain hinzufügen, nutze dies also, um Pegeländerungen durch extreme Width-Einstellungen auszugleichen, nicht als allgemeine Gain-/Makeup-Stufe. |

## Tipps

- **Beginne mit Width, nicht mit Bass Mono.** Die meisten Materialien brauchen nur den einzelnen globalen Width-Regler; greife gezielt zu Bass Mono Freq/Low Width, wenn du hörst, dass der Low-End an Fokus verliert oder sich in Mono schlecht überträgt, während du Width hochfährst.
- **Immer im Mono A/B-vergleichen.** Solo den Bus, schalte das Mono-/Downmix-Monitoring deiner DAW ein und bestätige, dass sich nichts seltsam auslöscht – Firmaments eigener Width-/Low-Width-/Auto-Mono-Safety-Pfad ist konstruktionsbedingt nachweislich mono-sicher (siehe `docs/architecture.md`), Haas Mode aber bewusst nicht, und selbst eine mono-sichere Width-Einstellung kann noch Probleme freilegen, die im eigenen Stereobild des Quellmaterials bereits latent vorhanden waren.
- **200 % Width ist eine Spezialeffekt-Einstellung, kein Standard.** Auf einem ganzen Mix oder einem lauten Bus liest sich das schnell künstlich/phasig; viel nützlicher ist es, kurz danach zu greifen (automatisiert für einen Chorus-Lift, einen Breakdown, einen einzelnen Pad-Layer), als es durchgehend aktiviert zu lassen.
- **Auto Mono Safety ist ein Sicherheitsnetz, kein Ersatz fürs Hinhören.** Es reagiert auf die Korrelation des *Inputs* des Plugins, mit meter-artiger (200 ms) Ballistik – schnell genug, um ein anhaltendes Phasenproblem zu erfassen, nicht schnell genug (noch dafür gedacht), schnelle Transienten sample-genau zu überwachen.
- **Haas Mode und Bass Mono/Low Width lassen sich problemlos kombinieren**, aber überlege, was jedes davon tut: Bass Mono/Low Width formt Breite *innerhalb* des Mid/Side-Modells (nachweislich mono-sicher), Haas Mode ist ein separater, später, nicht Mid/Side-basierter Effekt. Falls du garantierte Mono-Kompatibilität brauchst (Broadcast-Auslieferung, ein Club-System mit unvorhersehbarem Mono-/Summen-Sub), lass Haas Mode aus und verlasse dich allein auf Width/Low Width/Auto Mono Safety.
- **Auf einer Mono-Input-Spur/-Bus** haben Width/Low Width/Auto Mono Safety nichts, worauf sie wirken könnten (es gibt kein Side-Signal) – das Plugin lässt die Quelle sauber durch. Haas Mode ist der eine Regler, der in dieser Situation noch etwas bewirkt, da er nach dem (jetzt identischen) decodierten L/R-Paar arbeitet.

## Roadmap / was noch fehlt

Firmaments GUI ist noch der schlichte, funktionale Slider-/Toggle-Editor im v0.1-Stil – jeder Parameter oben ist vollständig aus dem eigenen Fenster des Plugins steuerbar (und aus den generischen Editor-/Automationsspuren jedes Hosts), aber es gibt noch keine eigens gezeichnete Oberfläche, und die Korrelations-/Phasenschätzung, die Auto Mono Safety antreibt, wird noch nicht als sichtbares Meter angezeigt (der DSP-Wert ist vollständig berechnet und getestet – siehe `docs/architecture.md` – nur das visuelle Widget steht noch aus). Beide sind für einen späteren Meilenstein vorgemerkt (eigene GUI + Metering). Preset-Management (Factory-Presets, Browsing) ist ebenfalls ein späterer Meilenstein; bis dahin funktioniert Speichern/Laden über den eigenen Plugin-State-Speichermechanismus deines Hosts.
