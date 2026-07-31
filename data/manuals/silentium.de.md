<!-- German translation of silentium.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Silentium-Icon" width="120"/></p>

# Silentium-Benutzerhandbuch

*Stille zwischen den Stürmen — ein straffes Lookahead-Noise-Gate für Palm-Muted-Rhythmus.*

## Was es ist

Silentium ist ein Noise Gate, speziell gebaut für High-Gain-Gitarre in einem
Heavy-Music-Mix: für den Moment zwischen Palm-Muted-Chugs, in dem Amp-Rauschen,
Pedalboard-Brummen und schwirrende Saiten sonst hörbar wären. Es ist kein
universelles Dynamics-Gate von einem Mixbus — jeder Default und jede interne
Ballistik ist auf das konkrete Problem zugeschnitten, „eine laute, verzerrte
Gitarre in dem Moment zum Schweigen zu bringen, in dem der Spieler aufhört zu
picken, ohne die Vorderflanke des nächsten Anschlags zu clippen."

## Wo es in einer Heavy-Production-Chain sitzt

Silentium ist eine **Detection-and-Dynamics**-Stufe, keine Tone-Shaping-Stufe.
Setze es:

- **Vor** jedem Drive-/Distortion-/Amp-Sim-Plugin (`crypta` und Verwandte in
  dieser Suite), wenn du das *saubere* Signal gaten willst — das vermeidet,
  dass Gating-Artefakte zusammen mit allem anderen verstärkt/verzerrt werden,
  und lässt das Sidechain-Hochpassfilter des Gates ein unverzerrtes Signal zum
  Keyen sehen.
- **Nach** der Amp-/Cab-Stufe, wenn das Rauschen, das du bekämpfst, spezifisch
  von dieser Stufe eingebracht wird (Amp-Rauschen, Cab-Sim-Rauschteppich) statt
  bereits im DI-Signal vorhanden zu sein.
- **Vor** jedem zeitbasierten Effekt (Reverb, Delay) in der Chain, damit das
  Gate auf der trockenen Gitarre schließt und der Tail eines Reverbs/Delays
  nicht mitten im Ausklang abgeschnitten wird. Brauchst du gezielt einen
  gegateten Reverb-Tail, ist das ein bewusst anderer Einsatz eines Gates als
  dieser.
- In einem **geschichteten Rhythmusgitarren-Mix** — einer Heavy-Music-
  Wall-of-Guitars — setze eine Instanz pro DI-/Amp-Sim-Spur statt den ganzen
  Bus zu gaten: jede Performance hat ihr eigenes Anschlags-Timing, und
  Per-Track-Lookahead hält die Anschläge jeder Schicht straff und synchron.

Für einen synchronisierten „Rhythmusgitarren unter dem Lead ducken"-Effekt,
oder ein sidechain-getriggertes rhythmisches Gate, das von einer Kick oder
einem Click Track geschlüsselt wird, siehe [Duck-Modus](#duck-modus-ducking-statt-gating)
und [externer Sidechain-Input](#externer-sidechain-input) unten — dieselbe
Engine deckt beide Anwendungsfälle ab.

## Signalfluss

```
                    +-- SC HPF (20-500 Hz) --> SC LPF (1-16 kHz) --> stereo-linked max|.| --> peak envelope follower --+
                    |                                                                                                  |
Input --> Lookahead |                                     hysteresis comparator + hold timer + knee blend <-----------+
 (or Sidechain      |                                                    |
  bus, if enabled)  |                        program-dependent attack/release gain ramp (dB domain)
    |               |                                                    |
    +---------------+------------------------------------------------> x (gain), or Listen output -> Output
```

1. Eine **Kopie** des Inputs (oder, falls du den externen Sidechain-Input
   aktiviert hast und dein Host tatsächlich etwas hineingeroutet hat, dieses
   Sidechain-Signal stattdessen) wird von **SC HPF** hochpassgefiltert, damit
   niederfrequentes Brummen/Rumpeln das Gate niemals fälschlich offen halten
   kann, und anschließend von **SC LPF** (v0.2.0) tiefpassgefiltert, sodass sie
   optional auf das Transientenband des Pick-Anschlags eingeengt werden kann,
   statt nur am unteren Ende beschnitten zu werden. Diese gefilterte Kopie wird
   ausschließlich zur *Entscheidung* über den Gain genutzt; sie erreicht nie
   direkt den Output, außer du aktivierst **Listen**.
2. Alle Kanäle dieser gefilterten Kopie werden pro Sample per
   `max(|channel|)` (stereo-linked) kombiniert, sodass ein hart auf eine Seite
   gepanntes Signal das Gate allein öffnen kann und der auf jeden Kanal
   identisch angewendete Gain-Wert des Gates das Stereobild nie verschiebt.
3. Dieses Mono-Signal speist einen schnellen internen Peak-Envelope-Follower
   (fixe Ballistik, nicht user-exponiert), der den Pegel liefert, auf den das
   Gate reagiert.
4. Ein **Hysterese-Komparator** mit zwei Schwellen (**Threshold**, und eine
   fixe 3 dB darunter) entscheidet, ob das Gate logisch offen oder geschlossen
   ist, und ein **Hold**-Timer hält es über kurze Einbrüche zwischen
   Transienten hinweg offen, damit aufeinanderfolgende Palm-Muted-Chugs das
   Gate nicht flattern lassen.
5. **Knee** weicht optional den Ziel-Gain zu einer sanften Überblendung über
   ein auf Threshold zentriertes Band auf, statt eines sofortigen Ein/Aus-
   Sprungs — Hold garantiert weiterhin für seine gesamte Dauer ein voll
   offenes Ziel, unabhängig von Knee.
6. **Duck**, falls aktiviert, invertiert dieses Ziel: dämpft oberhalb von
   Threshold, statt oberhalb davon zu öffnen, und macht so aus derselben
   Engine einen Ducker.
7. Das Ergebnis wird durch die **Attack**-/**Release**-Rampe (dB-Domäne, ab
   v0.2.0 programmabhängig — ein kleiner Ausschlag nahe Threshold rampt
   proportional in kürzerer Zeit hoch als ein voller Sprung von der
   Range-Untergrenze zu Unity, statt immer dieselbe Wall-Clock-Zeit zu
   benötigen, unabhängig davon, wie weit der Gain sich tatsächlich bewegen
   muss) zu einem tatsächlichen Per-Sample-Gain geglättet und dann auf das
   **Haupt**-Signal angewendet — das inzwischen um **Lookahead** verzögert
   wurde, damit der Gain schon kurz vor der tatsächlichen Vorderflanke eines
   Transienten zu steigen beginnen kann, was ein hörbares „Chirp" bei
   schnellem Picking vermeidet. Lookahead wird dem Host als Gesamtlatenz
   dieses Plugins gemeldet, sodass Plugin-Delay-Kompensation die
   Phasenausrichtung mit allem anderen in deiner Session sicherstellt.
8. Ist **Listen** aktiviert, läuft weiterhin alles oben Genannte (damit
   Metering/Timing konsistent bleibt), aber der Output ist das
   sidechain-gefilterte Detection-Signal selbst (Schritt 1, nach SC HPF/SC
   LPF) statt des gegateten Hauptsignals — zum Vorhören dessen, was der
   Detektor genau hört, während du SC HPF/SC LPF und Threshold einstellst.

Die vollständige implementierungsseitige Aufschlüsselung (State-Machine-
Details, Echtzeit-Sicherheitshinweise, die hier beschriebene `GateEngine`-
Klasse) findest du in [`docs/architecture.md`](architecture.md).

### Gemeldete Latenz

Lookahead ist Silentiums einzige Quelle gemeldeter Latenz. Bei `prepareToPlay()` meldet das Plugin `Lookahead × Samplerate`, auf Samples gerundet, über `setLatencySamples()` — bei Lookahead 0 ms ist das exakt 0 Samples, und nichts sonst im Signalpfad fügt welche hinzu.

*(v0.4.0)* Lookahead während laufendem Audio zu bewegen wartet nicht mehr darauf, dass der Host das Plugin neu vorbereitet: Die Delay selbst überblendet sofort auf ihre neue Länge (eine 10-ms-Equal-Power-Blende zwischen dem alten und dem neuen Tap), aber die *gemeldete* Zahl, die der Host für die Delay-Kompensation nutzt, zieht erst einen Moment später nach, beim nächsten Tick eines 25-ms-Pollings — der Audio-Thread ruft `setLatencySamples()` nie direkt auf, weil dieser Aufruf von dort aus nicht sicher ist. In der Praxis bedeutet das: Ein Host, der seine Message-Loop am Laufen hält, übernimmt die neue Latenz innerhalb von etwa 25 ms nach der Reglerbewegung, aber ein Host, der diese Loop nicht pumpt (z. B. mitten in einem Bounce), erfährt nie von der Änderung — Lookahead während eines Bounce/Renders zu bewegen ist also keine gute Idee.

**Smooth Open** einzuschalten fügt überhaupt keine gemeldete Latenz hinzu: aktiviert oder umgangen, sieht der Host bei Lookahead 0, 2,5, 5 und 20 ms dieselbe Zahl — die Öffnungs-Rampe wird vollständig innerhalb des Lookahead-Fensters geformt, das ohnehin schon bezahlt ist.

## Parameterreferenz

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Threshold** | -80 to 0 | -40 | dB | Der Pegel, den die (sidechain-gefilterte) Envelope erreichen muss, um das Gate zu öffnen. Niedriger drehen, um leisere Anschläge zu erfassen; höher drehen, um mehr vom Rauschteppich des Amps zu ignorieren. Die Close-Schwelle des Gates liegt **Hysteresis** dB darunter (per Default 3 dB), sodass ein Signal direkt an Threshold das Gate nie flattern lassen kann. |
| **Attack** | 0 to 50 | 1 | ms | Zeit, um von der Range-Untergrenze auf Unity hochzurampen, sobald die Envelope das Gate öffnet. Ab v0.2.0 liegt die Untergrenze bei 0 ms (vorher 0,1 ms) — bei aktiviertem Lookahead sorgt 0 ms für einen wirklich instantanen Sprung auf Unity beim Überschreiten der Threshold, für das perkussivste Picking. Langsamere Werte ergeben ein natürlicheres Anschwellen bei gehaltenen Akkorden. Die Rampe selbst ist programmabhängig (v0.2.0) — eine partielle Anregung konvergiert proportional schneller als eine vollständige; siehe „Wie sich die Rampe tatsächlich verhält" unten. |
| **Hold** | 0 to 250 | 20 | ms | Mindestzeit, die das Gate offen bleibt, nachdem es geöffnet wurde, kontinuierlich retriggert, solange die Envelope über der Close-Schwelle bleibt. Das hält das Gate über die kurzen Stillen *zwischen* aufeinanderfolgenden Palm-Muted-Chugs eines schnellen Rhythmusparts offen — stelle es ungefähr auf die Lücke zwischen deinen schnellsten Picking-Unterteilungen ein. (Die Obergrenze wurde in v0.2.0 von 500 ms auf 250 ms gesenkt, passend zum praktischen Bereich, der für diese Plugin-Kategorie dokumentiert ist; der Hold-Wert einer v0.1.0-Session bleibt exakt erhalten, außer er war auf über 250 ms eingestellt — dann wird er jetzt auf 250 ms geklemmt.) |
| **Release** | 5 to 500 | 80 | ms | Zeit, um zurück zur Range-Untergrenze zu rampen, sobald Hold vollständig abgelaufen ist. Schnelle Werte sind straffer/perkussiver; langsamere lassen den natürlichen Ausklang eines Akkords etwas atmen, bevor das Gate schließt. Ab v0.2.0 programmabhängig, genau wie Attack. |
| **Range** | -80 to 0 | -60 | dB | Boden-Dämpfung, die angewendet wird, während das Gate geschlossen ist. `0 dB` deaktiviert das Gating vollständig (ein immer offener Passthrough) — nützlich als A/B-Referenz. Werte um -40 bis -60 dB bringen Amp-Rauschen meist überzeugend zum Schweigen, ohne wie ein harter Mute zu klingen; sehr tiefe Werte (-80 dB) sind praktisch Stille. |
| **Lookahead** | 0 to 20 | 5 | ms | Verzögert das Hauptsignal, damit der Gain des Gates schon kurz vor der Vorderflanke eines Transienten zu steigen beginnen kann, was ein hörbares Attack-Chirp selbst bei sehr schnellem Attack vermeidet. Wird dem Host als Gesamtlatenz dieses Plugins gemeldet (Plugin-Delay-Kompensation erledigt den Rest automatisch). *(v0.4.0)* Eine Änderung wird jetzt **sofort** wirksam, mitten in der Wiedergabe: Die Verzögerung überblendet über 10 ms auf ihre neue Länge, und die neue Latenz wird kurz darauf an deinen Host gemeldet. Vor v0.4.0 tat der Regler nichts, bis der Host das Plugin zufällig neu vorbereitete. |
| **SC HPF** | 20 to 500 | 80 | Hz | Hochpassfilter, angewendet *nur* auf den Detection-Pfad (Sidechain), nie auf das Audio, das du hörst. Höher drehen, damit niederfrequentes Brummen/Rumpeln/der Nahbesprechungseffekt das Gate nicht fälschlich in einer leisen Passage offen hält; ein typischer Startwert für eine Gitarren-DI liegt bei 80–150 Hz. |
| **SC LPF** | 1000 to 16000 | 16000 | Hz | *(v0.2.0)* Tiefpassfilter, angewendet *nur* auf den Detection-Pfad, in Reihe nach SC HPF. Standardmäßig vollständig offen (16 kHz), sodass sich das v0.1.0-Verhalten nicht ändert, solange du nichts daran drehst. Zusammen mit SC HPF niedriger drehen, um den Detektor auf das Transientenband des Gitarren-Pick-Anschlags (etwa 2–5 kHz) einzuengen, statt auf den breitbandigen Default oberhalb des Brummens — nützlich, wenn anhaltendes Low-Mid-Schwirren/Brummen das Gate fälschlich offen hält. |
| **Knee** | 0 to 24 | 0 | dB | Breite eines auf Threshold zentrierten Soft-Knee-Bands. `0 dB` (Default) ist das ursprüngliche Hard-Knee-Gate: der Ziel-Gain springt an den Schwellen sofort zwischen Range und Unity. Breitere Werte überblenden das Ziel stattdessen sanft über das Band, für einen weicheren, weniger „schaltenden" Übergang bei Signalen, die nahe Threshold liegen — Hold garantiert weiterhin für seine gesamte Dauer ein voll offenes Ziel, unabhängig von Knee. |
| **Duck** | off/on | off | — | Invertiert den Gain-Computer: statt oberhalb von Threshold zu öffnen, dämpft der Output oberhalb von Threshold in Richtung Range. Derselbe Detection-Pfad (SC HPF, SC LPF, Hysterese, Hold, Knee, Lookahead) — nützlich, um eine Rhythmusgitarre unter einem Lead zu ducken, oder kombiniert mit einem externen Sidechain für einen kick-getriggerten Ducking-Effekt. |
| **Listen** | off/on | off | — | Routet das sidechain-gefilterte Detection-Signal direkt zum Output, unter vollständiger Umgehung des Gain-Computers. Nutze das beim Einstellen von SC HPF/SC LPF und Threshold, um genau zu hören, worauf der Detektor reagiert, und schalte es danach wieder aus. |
| **Ratio** | 1:1 bis ∞:1 | ∞:1 (Gate) | — | *(v0.4.0)* Wie hart das Signal heruntergedrückt wird, sobald es unter Threshold fällt. Am oberen Ende des Bereichs — dem Default, angezeigt als **∞ : 1 (Gate)** — ist es ein Gate: unterhalb von Threshold geht das Signal vollständig auf die Range-Untergrenze. Drehst du herunter, wird daraus ein Downward-*Expander*: Für jedes dB, das das Signal unter Threshold fällt, wird es um (Ratio − 1) dB gedämpft, sodass eine ausklingende Note proportional leiser gemacht statt abgeschaltet wird. Um 2:1–4:1 liegt die Einstellung, die Amprauschen zwischen Phrasen aufräumt, ohne dass irgendjemand merkt, dass da überhaupt ein Gate ist. |
| **Hysteresis** | 0 bis 12 | 3 | dB | *(v0.4.0)* Wie weit unter Threshold das Signal fallen muss, bevor das Gate wieder schließt. Das waren vor v0.4.0 intern fixe 3 dB, weshalb 3 der Default ist — lass es dort und nichts ändert sich. Höher drehen, wenn das Gate bei Material flattert, das genau um Threshold herum liegt; niedriger drehen (bis 0, wo die beiden Schwellen zusammenfallen) für den strammstmöglichen Schluss bei sauberem, gut getrenntem Material. |
| **Detector** | Peak / RMS | Peak | — | *(v0.4.0)* Wie der Detection-Pfad den Pegel misst. **Peak** ist das Original: Er reagiert auf die höchste momentane Auslenkung, erfasst also jeden Anschlag — und ebenso jeden einzelnen Klick. **RMS** misst stattdessen Energie über ein 5-ms-Fenster, sodass kurze Spitzen mit kaum Energie (Bundgeräusche, eine knisternde DI, Übersprechen von einem nahen Drum) das Gate nicht mehr öffnen. Das Umschalten ist überblendet und klickfrei. |
| **SC Slope** | 12 / 24 dB/Okt. | 12 dB/Okt. | — | *(v0.4.0)* Die Flankensteilheit **beider** Sidechain-Filter. 12 dB/Okt. ist das Original. 24 dB/Okt. gibt dem Detection-Band deutlich härtere Kanten — lohnend, wenn das, was das Gate fälschlich offen hält, knapp außerhalb des eingestellten Bands liegt und eine sanftere Flanke es immer wieder durchlässt. |
| **Smooth Open** | off/on | off | — | *(v0.4.0)* Formt das Öffnen des Gates zu einer stetigen Rampe, die in das Lookahead-Fenster passt, sodass selbst **Attack bei 0 ms** ohne Stufe öffnet. Es kostet keine zusätzliche Latenz — die Rampe endet genau dann, wenn der verzögerte Transient das Lookahead-Delay verlässt. Beachte, dass es auch die *schließende* Flanke glättet und das Gate nach dem Abfallen des Signals bis zu die Hälfte der Lookahead-Zeit offen hält; das ist meist unhörbar und gelegentlich nützlich, aber es ist der Grund, warum die strammsten Presets es aus lassen. Ohne Wirkung, wenn Lookahead auf 0 steht. |
| **Release Shape** | Exponential / Linear | Exponential | — | *(v0.4.0)* **Exponential** ist der unten beschriebene, ursprüngliche programmabhängige Ansatz. **Linear** schließt stattdessen mit einer konstanten Anzahl dB pro Sekunde, sodass ein vollständiger Schluss exakt die Release-Zeit dauert und sich die Ausklingrate des Tails im Fallen nie ändert — das Verhalten eines dB-linearen VCA und die vorhersagbarere Wahl, wenn der Schluss des Gates unter dem eigenen Ausklingen einer Note sitzen soll, statt ihm zu folgen. |

### Duck-Modus (Ducking statt Gating)

Aktiviere **Duck**, um den Gain-Computer zu invertieren: Statt oberhalb von
Threshold zu öffnen, dämpft der Output oberhalb von Threshold in Richtung
Range — dieselbe Engine wird damit zum Ducker. Der Detection-Pfad bleibt
unverändert (SC HPF, SC LPF, Hysterese, Hold, Knee, Lookahead gelten alle
weiter), sodass jedes Werkzeug, mit dem du die Reaktion eines Gates formst,
die Ducking-Reaktion genauso formt. Typische Anwendungen: eine
Rhythmusgitarren-Ebene unter einem Lead-Part ducken, oder Duck mit einem
[externen Sidechain-Input](#externer-sidechain-input) für einen kick- oder
klick-getriggerten rhythmischen Ducking-Effekt kombinieren.

### Wie sich die Rampe tatsächlich verhält (v0.2.0)

Attack/Release bedeuten bei ihren angegebenen ms-Werten weiterhin „Zeit für
einen vollständigen Übergang" (von der Range-Untergrenze zu Unity, oder
zurück). Neu in v0.2.0: Ein Übergang, der nur einen *Teil* dieser Strecke
zurücklegen muss — weil eine Note zum Beispiel nur leicht unter die
Close-Schwelle abgesackt ist, bevor sie wieder öffnete, statt vollständig zu
schließen — läuft jetzt proportional in *weniger* Wall-Clock-Zeit ab, als ein
vollständiger Sprung bräuchte, statt immer dieselbe Zeit zu benötigen,
unabhängig davon, wie weit sich der Gain tatsächlich bewegen muss. In der
Praxis bedeutet das, dass anhaltendes, leicht dynamisches Spiel glatter und
weniger „gepumpt" klingt, während das Gate bei echten vollständigen
Transienten weiterhin mit der angegebenen Attack-/Release-Geschwindigkeit
vollständig auf-/zuschnappt. Dieser Mechanismus ist inspiriert von (keine
Reproduktion des) „program dependent"/„AutoDynamic"-Release-Verhaltens, das
für Hardware-Noise-Gates dieser Kategorie dokumentiert ist — die vollständige
Quellenlage und die Einschränkungen findest du im „Honesty"-Abschnitt von
`docs/design-brief.md`.

## Unter der Haube

Ein paar Mechanismen, die es wert sind zu kennen, wenn du verstehen willst, warum sich v0.4.0 so verhält, wie es das tut — nicht nur, wofür die Regler beschriftet sind:

**Ratio ist ein echtes Downward-Expander-Gesetz, und der Default ist der buchstäbliche alte Code.** Unterhalb von Threshold wendet Ratio (Ratio − 1) dB Dämpfung für jedes dB an, um das das Signal fällt, gemessen auf 0,25 dB genau zu diesem Gesetz bei 2:1, 4:1 und 8:1, mit einem Knee, der an beiden Kanten sowohl im Wert als auch in der Steigung stetig ist, sodass ein breiteres Knee nie eine Ecke einführt. Am oberen Ende des Bereichs — ∞:1, der Default — springt der Gain-Computer in den exakten Code-Pfad von vor v0.4.0, statt in eine Näherung mit sehr hoher Ratio, „unverändert im Default" ist also ein Fakt auf Code-Ebene, kein numerischer Zufall.

**Smooth Open formt das Öffnen mit einem Moving-Max plus zwei kaskadierten Box-Filtern**, alle im dB-Bereich laufend, so bemessen, dass sie vollständig innerhalb des aktuellen Lookahead-Fensters passen. Ein rückwärtsgerichtetes Moving-Max verzögert Abfälle, nicht Anstiege, eine steigende Flanke passiert es also sofort, und die Box-Filter-Kaskade verteilt diese Flanke dann linear über das Fenster — fertig genau in dem Moment, in dem der verzögerte Transient die Lookahead-Delay-Line verlässt. Gemessen an einem Stille-zu−6-dBFS-Burst bei 0 ms Attack / 5 ms Lookahead: Der steilste Ein-Sample-Schritt sinkt von 59,5 dB/Sample auf 0,50 dB/Sample (eine 119-fache Reduktion), innerhalb von 0,01 % des theoretischen Dreieck-Kernel-Peaks, und die Rampe ist durchgehend monoton. Sie läuft in Reihe mit der ballistischen Gain statt als parallele „was auch immer offener ist"-Mischung, weil genau diese parallele Version probiert wurde und scheiterte: Bei 0 ms Attack gewinnt der rohe Schritt das Max, und der Klick, den sie entfernen soll, überlebt unangetastet.

**Die Lookahead-Überblendung ist konstruktionsbedingt echtzeitsicher.** Die 10-ms-Tap-Überblendung und die atomare Übergabe an das 25-ms-Message-Thread-Polling (siehe [Gemeldete Latenz](#gemeldete-latenz) oben) wurden gezielt so gebaut, dass `processBlock()` nie alloziert — verifiziert unter einem ersetzten Allocator über abgesicherte Blöcke, einschließlich des exakten Blocks, in dem sich Lookahead bewegt.

**Zwei Detektoren und zwei Sidechain-Flankensteilheiten laufen in jedem Block, ob ausgewählt oder nicht.** Der RMS-Detektor (5 ms Mean-Square) und die 24-dB/Okt.-Sidechain-Filterkette sind beide immer warm, sodass ein Wechsel von Detector oder SC Slope eine Überblendung zwischen zwei lebenden Signalen ist statt ein Sprung zu einem kalten Filter mit eigener Einschwing-Transiente. Gemessene Unterdrückung eine Oktave unter der Grenzfrequenz: 12,30 dB bei 12 dB/Okt. und 24,11 dB bei 24 dB/Okt., gegen eine Theorie von 12,3/24,1.

**Engineering-Hygiene:** 114 Testfälle und 9156 Assertions laufen auf macOS und Windows bei jedem Push, plus pluginval bei Strictness 10 und `auval -strict`. Keine Heap-Allokationen auf dem Audio-Thread unter einem ersetzten Allocator bei jedem aktivierten v0.4.0-Feature (einschließlich Live-Lookahead-Änderungen), Renders unabhängig von der Host-Blockgröße innerhalb von 1e-6 RMS, und ein offenes Gate, das mit allen neuen Stufen gleichzeitig eingeschaltet immer noch bis besser als −120 dBFS als reine Delay misst.

## Externer Sidechain-Input

Silentium stellt einen optionalen zweiten Input-Bus, **Sidechain**, bereit,
standardmäßig in jedem Host deaktiviert (aktiviere ihn in der Routing-/
Input-Matrix deiner DAW, genau wie bei einem Sidechain-Kompressor). Ist er
aktiviert und tatsächlich etwas hineingeroutet, wird der Detection-Pfad
(SC HPF → Envelope → Hysteresis → Knee) von diesem Sidechain-Signal statt vom
Haupt-Input geschlüsselt, während der Haupt-Input weiterhin das ist, was
verzögert, gegatet/geduckt und zum Output geschickt wird.

Typische Anwendungen:

- Das Gate einer Rhythmusgitarre von einer **Kick Drum oder einem Click
  Track** schlüsseln, für ein straffes, rhythmisch fest verankertes
  Chug-Pattern, unabhängig von der eigenen Pick-Dynamik der Gitarre.
- Das Gate einer Gitarrenschicht von **einer anderen Gitarrenschicht** (oder
  einer Referenz-DI) schlüsseln, damit ein doppelt/vierfach getrackter Part im
  Gleichschritt gatet, statt dass jede Schicht ihre eigene (und damit leicht
  abweichende) Gating-Entscheidung trifft.
- Mit **Duck** kombinieren für einen sidechain-getriggerten Ducking-Effekt,
  z. B. Rhythmusgitarren unter einer Kick oder einem Lead-Vocal ducken.

Ist der Sidechain-Bus deaktiviert, oder aktiviert, aber tatsächlich nichts
angeschlossen, fällt Silentium automatisch darauf zurück, vom Haupt-Input zu
schlüsseln — es gibt keinen speziellen „kein Sidechain"-Modus zu
konfigurieren.

## Presets

Am oberen Rand des Plugin-Fensters sitzt eine Preset-Leiste: `[<] [Name] [>]
[Save] [Save As...] [Delete] [Import...] [Export...]`, dazu ein Menü (Klick
auf den Preset-Namen), das Factory- und User-Presets auflistet, sowie eine
Aktion „Set current as default". Mit v0.2.0 werden neun Werkspresets
ausgeliefert — wofür jedes einzelne gedacht ist, steht in
[`docs/presets.md`](presets.md). User-Presets werden pro Benutzer gespeichert
(`~/Library/Audio/Presets/Yves Vogl/Silentium/` auf macOS,
`%APPDATA%/Yves Vogl/Silentium/Presets/` unter Windows) und lassen sich über
die Import-/Export-Buttons als einzelne `.basilicapreset`-Dateien exportieren
oder (einzelne Dateien oder `.zip`-Bänke) importieren.

## Sprache

Die Beschriftungen, Menüs und Dialoge der Preset-Leiste wechseln automatisch
auf Deutsch, wenn deine Systemsprache Deutsch ist; jede andere Sprache fällt
auf Englisch zurück. Das betrifft ausschließlich diesen Rahmentext —
Parameternamen, Einheiten und alle anderen technischen Fachbegriffe bleiben
unabhängig von der Systemsprache immer auf Englisch, da sie nicht übersetzt
werden.

## Tipps

- **Threshold nach Gehör einstellen, nicht nur nach Auge**: Solo die Spur,
  spiele die leiseste Passage, die du noch hören willst (meist die lautesten
  Palm Mutes kurz vor einer Pause), und senke Threshold, bis das Gate gerade
  eben offen bleibt. Prüfe dann, ob der Rauschteppich zwischen den Phrasen
  tatsächlich verschwindet; wenn nicht, muss Range tiefer, nicht Threshold.
- **Hold vs. Release nicht verwechseln**: Hold überbrückt *Lücken zwischen*
  Transienten (rhythmischer Abstand); Release regelt, wie der *Tail* des
  letzten Transienten ausklingt, sobald das Gate sich zum Schließen
  entscheidet. Ein hackelig klingender schneller Rhythmuspart ist fast immer
  ein Hold-Problem, kein Release-Problem.
- **SC HPF und Threshold interagieren**: SC HPF höher zu drehen entfernt mehr
  Low End aus dem, was der Detektor sieht, was dazu führen kann, dass
  Threshold leicht heruntergehen muss, um dieselben Anschläge weiter zu
  erfassen (weil das Sidechain-Signal jetzt weniger Energie trägt). Nutze
  Listen, um zu prüfen, was der Detektor tatsächlich hört, wann immer du
  SC HPF änderst.
- **Zero-Latency-Mixing**: Setze Lookahead auf 0 ms, wenn du live durch das
  Plugin trackst und Latenz wichtiger ist als eine perfekt saubere Attack;
  stelle es fürs Mixing wieder her, sobald du nicht mehr in Echtzeit
  monitorst.
- **Geschichtete Rhythmusgitarren**: Falls Per-Track-Gating dazu führt, dass
  Schichten an Transienten leicht auseinanderdriften, route die Sidechains
  aller Schichten von derselben Quellspur (über den externen Sidechain-Input),
  statt jede Schicht unabhängig selbst detektieren zu lassen.
- **Knee für einen „weniger gegateten" Charakter**: Klingt der harte
  Ein/Aus-Sprung des Defaults (0 dB Knee) auf einer gehaltenen, dynamischen
  Performance zu aggressiv/schaltend, verbreitere Knee auf 6–12 dB für einen
  weicheren Übergang, und prüfe danach erneut, ob der Rauschteppich zwischen
  den Phrasen weiterhin ausreichend gedämpft wird.

## Bekannte Einschränkungen (v0.4.0)

- **Keine veröffentlichte CPU-Zahl.** Es gibt in diesem Projekt keinen CPU-Benchmark und kein CI-Performance-Gate — behandle jede CPU-Auslastungszahl, die du woanders siehst, als unverifiziert; dieses Handbuch behauptet keine. Mehrere Erkennungspfade (beide Detektoren, beide Sidechain-Flankensteilheiten, der Smooth-Open-Smoother) laufen bei jedem Block bedingungslos, ob ausgewählt oder nicht, gezielt damit ein Wechsel zwischen ihnen immer eine klickfreie Überblendung ist statt ein Sprung zu einem kalten Filter; das ist eine bewusste feste Kostenstelle, kein Versehen.
- **RMS ist nicht universell „ruhiger" als Peak.** Bei einem gehaltenen tiefen Ton (um 70 Hz) glättet das 5-ms-RMS-Fenster das Mean-Square-Ripple nicht so gut wie das eigene Release von Peak, Peak ist dort also tatsächlich der ruhigere Detektor. Der echte Vorteil von RMS liegt bei Material mit hohem Crest-Faktor — isolierte Spitzen (Bundgeräusche, ein knisterndes DI-Signal), die kaum Energie tragen und das Gate nicht öffnen sollten.
- **Smooth Open formt auch die schließende Flanke**, nicht nur die öffnende: Es hält das Öffnungsziel für bis zu die Hälfte der Lookahead-Zeit, nachdem das Signal abgefallen ist, bevor die Schließ-Rampe beginnt. Meist unhörbar, gelegentlich nützlich, aber deshalb lassen die straffsten, chirurgischsten Presets es aus.
- **Die sechs neuen v0.4.0-Parameter haben noch keine dedizierten Bildschirm-Regler.** Sie sind vollständig host-automatisierbar und erscheinen in der generischen Parameteransicht deines Hosts, aber der eigens gestaltete, photoreale Editor (eingeführt in v0.3.0) wurde von diesem Release nicht angefasst — ein Screenshot der aktuellen GUI zeigt den Regler-Satz von v0.3.0.
- **Die Erkennung ist konstruktionsbedingt stereo-gelinkt**, ohne nutzerseitige Kontrolle darüber: Alle Kanäle werden vor der Erkennung über `max(|Kanal|)` kombiniert, und eine Gain wird identisch auf jeden Kanal angewendet. Es gibt keinen Stereo-Link-Prozentsatz, keinen Dual-Mono-Modus und keine M/S-Erkennungsoption.
- **Kein Oversampling.** Die einzige Nichtlinearität in Silentiums Signalpfad ist eine multiplikative Gain, deren Bandbreite durch die Ballistik begrenzt ist, Antiderivative Anti-Aliasing greift hier also nicht — eine bewusste Design-Entscheidung, nichts von der Roadmap Ausgelassenes.
- **Pre-1.0, AGPLv3.** Breaking Changes bleiben bis v1.0.0 möglich.
