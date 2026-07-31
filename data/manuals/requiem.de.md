<!-- German translation of requiem.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Requiem-Icon" width="120"/></p>

# Requiem — Bedienungsanleitung

*Eine Kathedrale in der Box — cineastischer Convolution-Reverb für orchestralen und chorischen Raum.*

## Was Requiem ist

Requiem ist ein Convolution-Reverb, der gezielt für die orchestrale/chorische Ebene eines Heavy-Music-Mixes entwickelt wurde — Streicher, Chor, Pads, Ambient-Texturen — statt als Allzweck-Reverb für jede beliebige Quelle. Er erzeugt seine Impulsantwort prozedural (keine mitgelieferte Sample-Library, die lizenziert oder verwaltet werden muss), geformt durch Regler, die auf musikalisch sinnvolle Entscheidungen abbilden: wie groß der Raum ist, wie hell oder dunkel der Tail klingt, wie ausgeprägt ein deutlicher früher „Slap" gegenüber einer glatten, homogenen Klangfläche ist, und ob er endlos aushalten statt abklingen soll. Du kannst außerdem eine eigene, aufgenommene Impulsantwort laden (eine echte Kathedrale, Halle, Plate oder irgendetwas anderes im WAV-/AIFF-Format o. Ä.), wenn du stattdessen einen bestimmten, nicht-prozeduralen Raum möchtest.

### v0.3.0: das „Living Tail"-Release

v0.3.0 ergänzt eine zweite Art, einen Reverb-Tail zu erzeugen. Neben der Convolution-Engine, die Requiem immer schon hatte, gibt es jetzt ein **Feedback Delay Network**, dessen Decay automatisch an die jeweils geladene Impulsantwort angepasst wird — auf 5 % genau an jedem Oktav-Zentrum für die Kurvenformen, die Requiem erzeugt (siehe [Unter der Haube](#unter-der-haube) unten) — und das sich, anders als eine feste Impulsantwort, nie wiederholt. Drei Engine-Modi bestimmen, wie die beiden kombiniert werden, und für den Mix kamen ein EQ auf dem Wet-Pfad sowie ein Ducker hinzu. Alles steht per Default auf dem Verhalten von v0.2.0: Eine bestehende Session klingt exakt wie zuvor.

### v0.2.0: ein recherchebasiertes Voicing-Rework

Requiems Verhalten bei Early Reflections und Tail-Verdunkelung wurde in v0.2.0 neu aufgebaut, ausgerichtet an den *dokumentierten* Designprinzipien kategorieprägender cineastischer/orchestraler Reverb-Einheiten sowie an allgemeiner Raumakustik-Literatur — öffentliche Handbücher, Entwickler-Interviews, Fachpresse-Reviews und DSP-Literaturartikel, niemals am tatsächlich gemessenen Output irgendeiner Hardware oder eines kommerziellen Plugins, und es wurde keine Impulsantwort eines Drittanbieters gesampelt oder approximiert (die vollständige Quellenangabe findest du in `docs/research-notes.md`; was dies als Aussage rechtfertigt und was nicht, steht im Honesty-Abschnitt von `docs/design-brief.md`). Die beiden wichtigsten Korrekturen: Early Reflections bauen sich jetzt in ihrer *Dichte* über die ersten paar Dutzend Millisekunden auf, statt von einem lauten initialen Tap abzuklingen, und der Tail verdunkelt sich jetzt *progressiv*, während er abklingt (wobei der Bass messbar länger nachklingt als die Höhen), statt für seine gesamte Länge eine einzige statische Filterfarbe anzuwenden. Zwei neue Regler — **Size** und **Bass Decay** — sind aus diesem Recherche-Durchgang hervorgegangen; siehe ihre Einträge unten.

## Wo es in einer Heavy-Music-Produktionskette sitzt

Heavy-Music-Produktionen mit orchestralen Elementen trennen die „aggressive" Ebene (Rhythmusgitarren, Drums, Bass) typischerweise von der „cineastischen" Ebene (Orchester, Chor, Pads, Ambience), damit jede unabhängig bearbeitet und im Mix platziert werden kann. Requiem ist für die zweite Ebene gedacht:

- **Streicher-/Orchester-Bus**: Ein Hall- oder Cathedral-Raum mit moderatem Mix (30–50 %) gibt der orchestralen Ebene Raum zum Atmen, ohne rhythmische Details zu verschmieren. Nutze Pre-Delay, um schnelle Passagen (Spiccato, Tremolo-Streicher) verständlich zu halten — ein kleiner Abstand, bevor der Tail einsetzt, bewahrt die Klarheit des Attacks.
- **Chor-Bus**: Chor verlangt tendenziell mehr Reverb als Instrumente, um „kathedralengroß" zu klingen — probiere den Cathedral-Raum, einen längeren Decay und einen höheren Mix als bei Streichern. Ein leicht heruntergezogenes Damping (ein dunklerer Tail) verhindert, dass sich Zischlaute/Atemgeräusche in der Klangfläche aufbauen.
- **Ambient-Pads/Übergänge**: Dafür ist Freeze gemacht — halte einen Akkord, aktiviere Freeze, und lass die eingefrorene Textur unter einem Übergang oder Breakdown aushalten, ohne ein separates Pad-Instrument zu benötigen.
- **Nicht direkt empfohlen für**: verzerrte Rhythmusgitarren oder Kick/Snare — ein kurzer Plate-artiger Reverb oder gar keiner dient diesen meist besser; der Cathedral-/Hall-Charakter von Requiem liest sich auf schnellen, perkussiven, verzerrten Quellen als Matsch. Falls du dennoch Ambience auf Gitarren willst, halte Mix niedrig (10–20 %) und Decay kurz.

Eine typische Insert-Reihenfolge auf einem Orchester-/Chor-Bus: EQ -> Kompression -> **Requiem** -> Limiter (falls als letzte Stufe auf diesem Bus verwendet). Requiem meldet dem Host seine eigene (normalerweise null) Verarbeitungslatenz und bleibt dadurch sample-genau zeitsynchron zu parallelen Dry-Bussen, wenn du es stattdessen über einen Aux/Send statt als Insert einblendest.

## Signalfluss

```
input -> Pre-Delay -> Convolution (procedural or user IR) -> Modulation (chorus, wet only)
      -> Width (M/S, wet only) -> Dry/Wet Mix (latency-compensated) -> Output -> output
```

Decay, Damping, Space, Early/Late Balance, Freeze, Size und Bass Decay formen die Impulsantwort selbst (im Hintergrund neu generiert, nicht bei jedem Sample); Pre-Delay, Modulation, Width, Mix und Output bestimmen, wie diese Impulsantwort in Echtzeit auf dein Signal angewendet wird. Die vollständige technische Erklärung, warum das so aufgeteilt ist, findest du in [`docs/architecture.md`](architecture.md).

### Gemeldete Latenz

Requiem meldet **immer 0 Samples Latenz** — in allen drei Engine-Modi (Classic Convolution, Hybrid Tail, Tail Bloom), bei jeder dokumentierten Samplerate (44,1/48/96/192 kHz), und auch während eines Live-Engine-Modus-Wechsels oder eines laufenden IR-Morphs. Ein durch Classic Convolution geschickter Kronecker-Delta-Impuls landet mit seinem ersten Output-Sample exakt bei Index 0. Das gilt sogar in Hybrid Tail, wo der synthetisierte FDN-Zweig eine eigene interne Onset-Verzögerung hat (ein linearphasiges Korrekturfilter plus die eigene kürzeste Delay-Line des Netzwerks): Diese Verzögerung wird intern durch die eigene Pre-Delay des Zweigs kompensiert, statt an den Host gemeldet zu werden — das Plugin bittet deine DAW also nie, sie zu berücksichtigen. Pre-Delay selbst ist davon nicht betroffen — das ist eine hörbare, von dir gesteuerte Lücke zwischen dem Direktschall und dem Einsatz des Tails, nichts, was das Plugin über Latenz-Kompensation versteckt.

## Parameterreferenz

### Engine

Wählt, wie der Reverb-Tail erzeugt wird.

- **Classic Convolution** (Default) — die Engine, die Requiem immer genutzt hat: eine Impulsantwort, gefaltet. Jede bestehende Session und jedes Preset nutzt sie, und sie klingt exakt wie in v0.2.0.
- **Hybrid Tail** — die Impulsantwort liefert nur die Early Reflections, bis zu dem Punkt, an dem das Reflexionsmuster statistisch nicht mehr von Rauschen zu unterscheiden ist (die *Mixing Time*, automatisch gemessen). Von dort übernimmt ein Feedback Delay Network mit sechzehn Linien, dessen Decay pro Oktave an das gemessene Abklingen der Impulsantwort angepasst wird. Das Ergebnis klingt ab wie der aufgenommene Raum, loopt aber nie, weil nichts wiedergegeben wird.
- **Tail Bloom** — die vollständige, unangetastete Impulsantwort, mit einem modulierenden Tail darunter. Nimm das, wenn du den Charakter einer bestimmten Aufnahme willst, sie aber atmen soll.

Ein Moduswechsel ist klickfrei. Für kontinuierliche Automation ist er nicht gedacht.

### Tail Mod Mode / Tail Mod Depth / Tail Mod Rate

Bewegung im Tail, für die beiden Feedback-Delay-Network-Modi. In Classic Convolution stumm.

- **Matrix** (Default) — moduliert, wie die Delay-Linien einander speisen, über Rotationen, die mathematisch garantiert energieerhaltend sind. Da sich keine Delay-Länge je ändert, bringt das Bewegung, **ohne irgendetwas zu verstimmen**: Die gemessene Tonhöhenabweichung liegt bei voller Depth unter einem Hundertstel Halbton. Nimm das für alles Harmonische.
- **Lush** — moduliert die Delay-Längen selbst, der klassische Vintage-Ansatz. Das *verstimmt* hörbar und absichtlich. Nimm es, wenn du diesen Charakter willst, und sei vorsichtig bei getragenem tonalem Material.
- **Off** — keine Modulation.

Depth legt fest wie viel; Rate skaliert wie schnell, als Prozentsatz der eingebauten Raten.

### Bloom

Wie viel des modulierenden Tails im Modus **Tail Bloom** unter die Impulsantwort gelegt wird. In den anderen beiden Modi unhörbar. Die Kennlinie ist am unteren Ende des Bereichs bewusst sanft, damit niedrige Einstellungen brauchbar sind, statt gleich zu einer offensichtlichen zweiten Ebene zu springen.

### Low Cut / High Cut

Ein Hochpass und ein Tiefpass mit 12 dB/Oktave, ausschließlich auf dem **Wet-Signal** — das Dry-Signal wird nie angetastet. Low Cut ist die übliche Abhilfe für einen Reverb, der das Low End vermatscht; High Cut nimmt einem hellen Tail die Schärfe, ohne die Quelle stumpf zu machen.

Beide sind an ihren Bereichsenden (20 Hz und 20 kHz) hart gebypasst, und das sind die Defaults. Bei diesen Einstellungen laufen die Filter gar nicht, der Wet-Pfad ist also bit-identisch zu v0.2.0.

### Duck / Duck Attack / Duck Release

Zieht den Reverb herunter, während der Input spielt, und lässt ihn in den Lücken wieder hoch — der Standardtrick, damit ein großer Reverb einen Gesang oder eine Dialogspur nicht zuschüttet. Der Sidechain ist der Dry-Input, es triggert also die Quelle, nicht der Tail.

Duck steht per Default auf 0 %, und bei 0 % ist der Wet-Gain exakt 1 — es findet überhaupt keine Verarbeitung statt. Attack und Release bestimmen, wie schnell der Duck eingreift und sich erholt, und sind wirkungslos, solange Duck auf 0 % steht.

### Decay
**Bereich:** 0.1 – 10.0 s · **Standard:** 2.5 s

Wie lange der Reverb-Tail zum Abklingen braucht (RT60-artig: der Punkt, an dem er um 60 dB abgefallen ist) — genauer gesagt die *mittenfrequente* Referenz-Abklingrate, relativ zu der die tiefen und hohen Bänder des Tails gemessen werden (siehe Bass Decay unten). Kurze Werte (0.3–0.8 s) eignen sich für enge Räume/Ambience; 1.5–3 s für einen Konzertsaal; 4–10 s ist Kathedralen-/Höhlen-Territorium oder nützliches Rohmaterial für Freeze. Decay bestimmt außerdem die Länge der generierten Impulsantwort, weshalb sehr lange Decay-Werte mehr CPU kosten (der Convolution-Kernel wird proportional größer).

### Pre-Delay
**Bereich:** 0 – 250 ms · **Standard:** 20 ms

Der Abstand zwischen dem Dry-Sound und dem Einsatz des Reverb-Tails. Eine kleine Menge (10–30 ms) reicht meist aus, um das Gefühl zu erhalten, „dieser Reverb ist vom Direktsignal getrennt", ohne wie ein eigenständiger Slapback zu klingen. Größere Werte (60–150 ms) helfen, schnelles rhythmisches Material (palm-gemutete Gitarren unter dem Orchester, Staccato-Streicher) knackig und verständlich zu halten, während der Tail erst danach aufblüht — das Ohr hört den Attack klar, bevor die Klangfläche einsetzt.

### Damping
**Bereich:** 500 – 20000 Hz · **Standard:** 8000 Hz

Die *finale* Höhengrenze des Tails — seit v0.2.0 verdunkelt sich der Tail beim Abklingen progressiv (er startet heller und pendelt sich bis zum Ende von Decay bei diesem Wert ein), statt über die gesamte Länge des Tails eine einzige statische Filterfarbe anzuwenden — das entspricht dem Verhalten echter Räume, die sich über den Reflexionsweg hinweg verdunkeln (Luftabsorption plus Oberflächenabsorption, die sich über die Zeit aufsummieren). Niedrigere Werte erzeugen eine dunklere, stärker „absorbierte" endgültige Tail-Farbe (schwere Teppiche/Vorhänge, oder einfach ein stumpfer klingender Raum); höhere Werte erzeugen eine hellere, „hart-oberflächigere" Tail-Farbe (Stein, Glas). Bei Chor und Streichern liest sich ein leicht abgesenktes Damping gegenüber dem Standard oft natürlicher und über einen langen Mix hinweg weniger ermüdend, besonders wenn die Dry-Quelle bereits hell klingt.

### Space
**Auswahl:** Cathedral / Hall / Chamber · **Standard:** Hall

Formt den Charakter der frühen Reflexionen, die vor dem diffusen Tail liegen (siehe Early/Late Balance unten) — das ist es, was tatsächlich den Unterschied macht zwischen „das klingt wie eine Kathedrale" und „das klingt wie eine kleine Kammer", unabhängig von Decay/Damping. Seit v0.2.0 bauen sich die frühen Reflexionen in ihrer *Dichte* über die ersten paar Dutzend Millisekunden auf und halten danach noch eine Weile eine annähernd flache Energie, statt von einem lauten initialen Tap abzuklingen — siehe Size unten für die kontinuierliche Achse innerhalb jeder Auswahl:

- **Cathedral**: das breiteste, längste Aufbau-/Übergangsfenster und das dichteste Tap-Budget — der Klang eines großen Steinraums mit vielen nahen Flächen. Passt gut zu langem Decay und Chor.
- **Hall**: ein ausgewogenes, moderates Fenster — der Allzweck-Standard, gut für Streicher und Orchester.
- **Chamber**: das engste, kürzeste Fenster — ein kleiner, intimer Raum. Gut für ein subtileres Gefühl von „das wurde in einem Raum gespielt", ohne einen offensichtlich großen Reverb.

### Size
**Bereich:** 0 – 100 % · **Standard:** 50 %

Die scheinbare Größe des Raums, unabhängig sowohl von Decay (Tail-Länge) als auch von Space (Reflexionscharakter) — eine kontinuierliche Achse innerhalb der jeweils gewählten Space-Option. Bei 0 % sind Fenster und Dichte der frühen Reflexionen enger gefasst (näher an einem kleineren Raum innerhalb des Charakters dieser Space-Option); bei 100 % sind sie breiter und dichter (näher an einem größeren Raum). Das Verstellen von Size ändert nicht, wie lange der Reverb-Tail zum Abklingen braucht — nur, wie groß sich die Abmessungen des Raums anfühlen, bevor der diffuse Tail übernimmt. Nutze es, um feinzujustieren, „wie groß sich dieses Hall/Cathedral/Chamber tatsächlich anfühlt", ohne Decay anzufassen oder zu einer anderen Space-Option zu greifen.

### Bass Decay
**Bereich:** 25 – 175 % · **Standard:** 130 %

Wie viel länger (oder kürzer) das Low End des Tails im Verhältnis zu den Mitten/Höhen nachklingt, als Prozentsatz von Decay — passend dazu, wie in realen Räumen der Bass sehr häufig länger nachklingt als Mitten/Höhen (schlechte Tieffrequenz-Absorption bei den meisten Raummaterialien). Der Standard (130 %) gibt dem Low End einen spürbar längeren Tail als den Mitten, ohne den Mix zu überfluten; drehe Richtung 175 % für ein dunkles, höhlenartiges Low-End-Aufblühen (passt gut mit Freeze für ein Ambient-Pad), oder zieh es Richtung 25 % herunter für ein strafferes, kontrollierteres Low End, das unter einem dichten Arrangement keinen Matsch aufbaut. Das Mid-Band folgt immer direkt Decay; das High-Band endet immer etwas früher als das Mid-Band (nicht vom Nutzer einstellbar, entsprechend demselben Prinzip der Höhenabsorption realer Räume).

### Early/Late Balance
**Bereich:** 0 – 100 % · **Standard:** 80 %

Blendet zwischen der Early-Reflection-Ebene (0 %, geformt durch Space) und dem diffusen Late-Tail (100 %, geformt durch Decay/Damping) über. Bei 0 % hörst du überwiegend die diskreten frühen Reflexionen — ein kurzer, direkter Charakter, näher an einem Slapback oder der „Lebendigkeit" eines kleinen Raums als an einer Klangfläche. Bei 100 % hörst du eine reine, glatte diffuse Fläche ohne eigenständigen Früh-Charakter. Der Standard (80 %) hält den diffusen Tail dominant, gibt der frühen Ebene aber noch etwas Präsenz — senke den Wert, wenn der Charakter der Space-Einstellung hörbarer sein soll, erhöhe ihn Richtung 100 % für das glatteste, cineastischste Ergebnis.

### Modulation
**Bereich:** 0 – 100 % · **Standard:** 0 %

Fügt dem Reverb-Tail eine subtile, langsame, Chorus-artige Bewegung hinzu — niemals dem Dry-Signal. Prozedural generierte Impulsantworten können gelegentlich etwas statisch oder metallisch klingen im Vergleich zu einem echten aufgenommenen Raum; eine kleine Menge Modulation (10–30 %) mildert das, ohne als offensichtlicher Chorus-/Vibrato-Effekt hörbar zu sein. Bei 0 % ist die Modulation-Stufe vollständig bypassed (identischer Output, als gäbe es sie gar nicht) — es ist unbedenklich, sie auf Standard zu lassen, sofern du nicht gezielt diese zusätzliche Bewegung willst.

### Freeze

**Off / On** · **Standard:** off

**Was Freeze tut, hängt jetzt von der Engine-Einstellung ab**, und die beiden Verhaltensweisen unterscheiden sich wirklich:

- **In Classic Convolution** funktioniert es exakt wie in v0.2.0 — unten vollständig beschrieben. Der Tail wird mit einer flachen Hüllkurve neu erzeugt, das Aushalten ist also durch die Decay-Einstellung begrenzt.
- **In Hybrid Tail und Tail Bloom** ist es *strukturell und wirklich unendlich*. Die Dämpfung pro Linie des Feedback Delay Network wird über 20 ms auf Unity ausgeblendet, womit ein verlustfreies Netzwerk übrig bleibt: Es hält das bereits darin zirkulierende Audio exakt und unbegrenzt. Es wird nichts neu erzeugt, der Schalter greift also innerhalb eines einzigen Audioblocks statt auf den nächsten Regenerations-Tick zu warten, und es gibt keine durch Decay gesetzte Obergrenze. Die gemessene Haltestabilität liegt über zwanzig Sekunden innerhalb von 0,2 dB.

Der Rest dieses Abschnitts beschreibt das Classic-Verhalten.

Wenn aktiviert, hält der Reverb-Tail seinen aktuellen spektralen Inhalt aus, statt abzuklingen — nützlich, um einen Akkord oder eine Textur unter einem Übergang, Breakdown oder Ambient-Abschnitt zu halten, ohne ein separates Pad-/Drone-Instrument zu benötigen. Freeze ist Convolution-basiert, daher ist das Aushalten durch die Decay-Einstellung begrenzt (bis zu 10 s), nicht buchstäblich unendlich — stell es dir eher als „halte diesen Schnappschuss des Tails für bis zu Decay Sekunden" vor statt als Feedback-Loop-artiges unendliches Freeze. Damping beeinflusst weiterhin die Helligkeit der eingefrorenen Textur, während sie aktiv ist (dabei auf einer konsistenten Farbe gehalten, statt sich weiter zu verdunkeln); Early/Late Balance und die Early-Reflection-Ebene werden im eingefrorenen Zustand ignoriert (ein eingefrorener Tail ist immer die volle diffuse Fläche).

Dieses Finite-Kernel-Design ist eine **bewusste Entscheidung, keine Einschränkung**: Recherche zu Feedback-Loop-basierten „Infinite-Reverb"-Designs dokumentiert, dass sie über die Zeit zunehmend dumpfer werden (wiederholte Filterung im Feedback-Pfad dämpft die Höhen weiter, selbst bei Unity-Feedback-Gain) und mit steigender interner Diffusions-/Feedback-Ordnung eine hörbare Periodizität entwickeln können (siehe `docs/research-notes.md`, Abschnitt 4). Da Requiems Freeze keinen Feedback-Pfad besitzt, der wiederholt gefiltert wird, kann strukturell keines der beiden Artefakte entstehen.

**Tipp:** Für einen sauberen Freeze-Moment aktiviere Freeze auf einem gehaltenen Akkord (nicht mitten in einem Transienten) und erhöhe eventuell zuerst Decay, da dieser Wert bestimmt, wie lang der eingefrorene Kernel tatsächlich ist.

### Width
**Bereich:** 0 – 200 % · **Standard:** 100 %

Stereobreite ausschließlich des Wet-(Reverb-)Signals, per Mid/Side-Skalierung — die Breite des Dry-Signals wird nie angetastet. 0 % kollabiert das Wet-Signal auf Mono; 100 % ist das natürliche Stereobild der Convolution-Engine; bis zu 200 % übertreibt es weiter für einen besonders breiten, umhüllenden Tail. Sehr breite Einstellungen (150–200 %) können isoliert beeindruckend klingen, aber Phasen-/Mono-Kompatibilitätsprobleme verursachen — prüfe deinen Mix in Mono, wenn du Width hoch aufdrehst.

### Mix
**Bereich:** 0 – 100 % · **Standard:** 35 %

Dry/Wet-Balance. Bei 0 % ist Requiem ein transparenter (latenzkompensierter) Durchlauf des Inputs — nützlich zum A/B-Vergleich des Dry-Signals, ohne das Plugin zu entfernen, oder wenn du Requiem auf einem Send-/Aux-Bus einsetzt und es auf Plugin-Ebene voll wet haben willst, um die Mischung stattdessen über die Send-Menge zu steuern. Der Standard (35 %) eignet sich für den typischen Insert-Einsatz auf einem Orchester-/Chor-Bus; höher für ein ambienteres, verwascheneres Ergebnis, oder 100 % auf einem dedizierten Reverb-Return-Bus.

### Output
**Bereich:** -24 – 24 dB · **Standard:** 0 dB

Trim, der nach dem Dry/Wet-Mix angewendet wird — nutze ihn, um den Output-Pegel des Plugins ins Gain-Staging einzupassen (z. B. nach deutlichem Erhöhen von Mix, oder um Pegel beim A/B-Vergleich verschiedener Decay-/Space-Einstellungen anzugleichen), ohne danach ein separates Gain-Plugin zu benötigen.

## Eine eigene Impulsantwort laden

Nutze **Load IR...** im Editor, um den prozeduralen Generator durch eine eigene aufgenommene Impulsantwort (WAV/AIFF) zu ersetzen. Solange eine eigene IR geladen ist, wirken sich Decay/Damping/Space/Early/Late Balance/Freeze/Size/Bass Decay nicht mehr auf den Klang aus (die geladene IR wird unverändert verwendet); **Clear IR** kehrt zum prozeduralen Generator zurück und übernimmt dabei die aktuellen Einstellungen dieser Regler. Der Dateipfad der geladenen IR wird mit deiner Session/deinem Preset gespeichert; falls die Datei beim erneuten Öffnen der Session verschoben oder gelöscht wurde, fällt Requiem auf den prozeduralen Generator zurück, statt das Laden fehlschlagen zu lassen.

Requiem validiert die Datei vor dem Laden (verwirft alles, was nicht als Audio gelesen werden kann, sowie jede Datei länger als 30 Sekunden — echte aufgenommene Impulsantworten sind so gut wie nie so lang, und das schützt davor, versehentlich einen ganzen Song/Mix statt einer echten IR auszuwählen).

## Unter der Haube

Ein paar Mechanismen, die es wert sind zu kennen, wenn du verstehen willst, warum sich der Living Tail so verhält, wie er es tut — nicht nur, wofür die Regler beschriftet sind:

**Die Decay-Kurve wird gelöst, nicht eingestellt.** Jede der sechzehn FDN-Delay-Lines trägt einen zehnbandigen Oktav-Grafik-EQ plus eine Breitband-Gain, gefittet an die eigene gemessene Pro-Oktave-Decay der Impulsantwort über eine Householder-QR-Pseudoinverse und Gauss-Newton-Verfeinerung gegen die realisierte Response, innerhalb eines ±10-dB-Command-Gain-Clamps. Eine abschließende Stabilitäts-Projektion fegt die fertige Kaskade über das Kontrollfrequenz-Raster und zieht die Breitband-Gain exakt um jeden Überschuss herunter, sodass die Loop-Gain keiner Line bei irgendeiner Frequenz jemals Eins erreicht. Die entworfene Kaskade landet auf 5 % genau an jedem Oktav-Zentrum von 63 Hz bis 8 kHz, auf allen sechzehn Lines, für die Kurvenformen, die Requiem tatsächlich erzeugt (eine flache Zielkurve, und die eigene analytische Kurve des prozeduralen Generators) — fünfzig zusätzliche randomisierte Decay-Kurven von 0,1 bis 5 Sekunden wurden auf demselben Weg durchlaufen, ohne einen einzigen Fehlschlag. Der Solve ist bit-reproduzierbar: Zwei Plugin-Instanzen bei denselben Settings können nie auseinanderdriften.

**Bewegung ohne Verstimmung, im Matrix-Modus.** Die Feedback-Matrix, die die Matrix-Modus-Modulation antreibt, ist eine Householder-Reflexion, komponiert mit zeitvarianten Givens-Rotationen auf disjunkten Indexpaaren, beide zu jedem Zeitpunkt orthogonal — das Netzwerk kann durch die Modulation also nicht destabilisiert werden, und keine Delay-Länge ändert sich je, weshalb die Modulation die Tonhöhe nicht verschieben kann. Gemessene Tonhöhenabweichung bei voller Tiefe: unter einem Cent. Der Lush-Modus ist das entgegengesetzte, bewusst erhaltene Werkzeug: Er moduliert die Delay-Längen selbst und verstimmt absichtlich — der klassische Vintage-Chorus-Charakter, kein Defekt.

**Die Übergabe des Hybrid Tail wird gemessen, nicht geraten.** Der Punkt, an dem das Reflexionsmuster der Impulsantwort statistisch nicht mehr von Rauschen zu unterscheiden ist (die Mixing Time), wird pro Impulsantwort gemessen statt angenommen, dann auf ein 50–350-ms-Fenster geklemmt. Die Response wird dort mit einer Raised-Cosine-Überblendung geteilt, und der FDN-Zweig wird um *zwei* Dinge gemeinsam vorverzögert — die Group Delay eines kurzen Korrekturfilters und die eigene kürzeste Delay-Line des Netzwerks —, weil eine Kompensation nur des Filters den Einsatz des synthetisierten Tails bei 48 kHz etwa 34 ms zu spät ansetzen und direkt nach Ende des Early-Felds eine hörbare Lücke hinterlassen würde. Passt eine Impulsantwort nicht auf eine Weise ab, der der Fit vertrauen kann (etwa eine gegatete oder stark abgeschnittene Aufnahme), erkennt Hybrid Tail das und fällt stattdessen darauf zurück, die volle, unveränderte Impulsantwort zu falten, statt einen schlechten Fit daranzusetzen — still, pro Impulsantwort, und mit Absicht statt als versteckter Fehlschlag.

**Jeder klanggestaltende Regler überblendet, er springt nie hart.** Weil die Kernel-Regeneration asynchron läuft, überblendet eine Änderung von Decay, Damping, Space, Size, Bass Decay oder Early/Late Balance über 100 ms zwischen der alten und der neuen Convolution-Engine, getriggert dadurch, dass die neue Engine tatsächlich meldet, bereit zu sein, statt durch einen festen Timer — eine Änderung wird also nie angewendet, bevor ihr Kernel fertig geladen ist.

**Freeze ist echt unbegrenzt, aber nur in den beiden FDN-basierten Modi.** In Hybrid Tail und Tail Bloom fährt ein aktiviertes Freeze die Dämpfung jeder Line des Netzwerks über 20 ms auf Eins hoch und lässt eine verlustfreie Schleife zurück, die exakt das hält, was gerade darin zirkuliert — unbegrenzt, und es greift innerhalb eines einzigen Audio-Blocks statt auf einen Regenerations-Tick zu warten. Gemessene Haltestabilität: innerhalb von ±0,2 dB über zwanzig Sekunden. In Classic Convolution funktioniert Freeze weiterhin wie schon immer — begrenzt durch das Decay-Setting, bis zu 10 Sekunden —, weil ein endlicher Convolution-Kernel eben endlich ist. Das ist ein bewusster Trade-off, kein Versehen: Ein Design ohne Feedback-Pfad, der wiederholt gefiltert werden könnte, kann strukturell nicht das progressive Dumpfwerden der Höhen oder die hörbare Periodizität entwickeln, die Feedback-Loop-artige „unendliche Reverb"-Designs bei langem Halten dokumentiert riskieren.

**Deine bestehenden Sessions sind unberührt, und das ist getestet, nicht nur beabsichtigt.** Alle zehn neuen v0.3.0-Parameter stehen standardmäßig auf neutral, und die Wet-Pfad-Filter sowie der Ducker sind bei ihren Defaults *strukturell* umgangen (nicht nur mit Eins multipliziert) — eine Session von vor v0.3.0, geladen in v0.3.0, rendert bit-identisch zu einer frischen Instanz mit denselben Settings, und die elf bereits bestehenden Werkspresets sind unverändert.

**Engineering-Hygiene:** 134 Testfälle laufen auf macOS und Windows bei jedem Push, plus pluginval bei Strictness 10 und `auval -strict` — geprüft werden keine Heap-Allokationen auf dem Audio-Thread in allen drei Engine-Modi (auch bei Freeze und Modus-Wechseln mitten im Stream), null gemeldete Latenz über den gesamten Samplerate-Bereich, und ein dedizierter Regressionstest für die Race-Condition beim Kernel-Reload zwischen Message-Thread und Audio-Thread.

## Presets

Die Preset-Leiste am oberen Rand des Editors (`[<] [PresetName] [>] [Save] [Save As...] [Delete] [Import...] [Export...]`) gibt dir elf Werkspresets als Startpunkte (wofür jedes einzelne klanglich ausgelegt ist, steht in `docs/presets.md`) plus deine eigenen gespeicherten Presets, gespeichert pro Nutzer unter `~/Library/Audio/Presets/Yves Vogl/Requiem/` auf macOS (`%APPDATA%/Yves Vogl/Requiem/Presets/` unter Windows):

- **[<] / [>]** blättern durch die Werkspresets, dann durch deine eigenen, alphabetisch.
- **Ein Klick auf den Preset-Namen** öffnet ein Menü mit Factory-/User-Bereichen plus „Set current as default" (was eine frische Plugin-Instanz lädt).
- **Save** überschreibt das aktuell geladene User-Preset (deaktiviert bei Werkspresets — die sind schreibgeschützt); **Save As...** fragt nach einem neuen Namen.
- **Import.../Export...** lesen/schreiben einzelne `.basilicapreset`-Dateien, und Import akzeptiert zusätzlich `.zip`-Preset-Bänke.
- Ein `*` nach dem Preset-Namen bedeutet, dass sich die aktuellen Einstellungen seit dem Laden/Speichern geändert haben.

Die Oberfläche folgt automatisch deiner Systemsprache (standardmäßig Englisch, Deutsch wenn deine Systemsprache auf Deutsch eingestellt ist) — nur Interface-Beschriftungen/Menüs/Dialoge werden übersetzt; Parameternamen und Einheiten bleiben immer auf Englisch.

## Tipps

- **Schnelles/rhythmisches Material unter einer orchestralen Klangfläche**: Erhöhe Pre-Delay, bevor du zu einem kürzeren Decay greifst — das bewahrt meist die Klarheit besser, während das Raumgefühl insgesamt erhalten bleibt.
- **Chor klingt hart/zischend im Tail**: Senke Damping um ein paar tausend Hz, bevor du zu einem EQ auf dem Reverb-Return greifst.
- **„Dieser Reverb klingt etwas statisch/synthetisch"**: Probiere Modulation um 15–25 %, bevor du davon ausgehst, einen anderen Reverb zu brauchen.
- **Ein Pad/Drone aus einer vorhandenen Spur bauen**: Automatisiere Freeze auf on, fahre Mix hoch und erwäge einen Hauch Width und Modulation für Bewegung, während es aushält.
- **Mono-Kompatibilitäts-Check**: Summiere regelmäßig auf Mono, wenn du Width über ~150 % fährst, besonders auf einem Bus, der später auf Mono gefaltet werden könnte (Broadcast, manche Streaming-Plattformen).
- **Ein Raum fühlt sich für sein Decay „zu klein" oder „zu groß" an**: Greife zu Size, bevor du Decay oder Space änderst — es passt die scheinbaren Abmessungen an, ohne zu verändern, wie lange der Tail tatsächlich nachklingt.
- **Low End baut in einem dichten Mix Matsch auf**: Zieh Bass Decay Richtung 100 % oder darunter herunter (statt Decay insgesamt zu verkürzen, was auch den Mid-/High-Tail verkürzen würde, den du eventuell noch behalten möchtest).

## Bekannte Einschränkungen (v0.3.0)

- **Die Echo-Dichte von Hybrid Tail baut sich an der Übergabe allmählich auf, nicht sofort.** Der FDN-Zweig wird durch einen Impuls angeregt, seine eigene Reflexionsdichte steigt also über die ersten paar hundert Millisekunden nach der Splice an, statt sofort dicht zu starten — eine bekannte, gemessene Eigenschaft dieses Releases statt eines Abstimmungsfehlers, und sie steigt dabei stetig und vorhersagbar statt flach zu bleiben.
- **Die spektrale Balance von Hybrid Tail am Splice-Punkt trifft auf ein paar dB genau, nicht auf ein dB.** Sie enger zu treffen würde bedeuten, das gesamte Netzwerk bei jeder Parameteränderung offline zu rendern, was die schnelle, klickfreie Neuberechnung brechen würde, die der Sinn des Hybrid-Modus ist — deshalb wird stattdessen der analytische Weg genutzt, auf Kosten eines kleinen (einstelligen dB-)Tilts direkt an der Übergabe.
- **Die Seitenbänder der Matrix-Modulation sind mit Absicht hörbar, nicht auf Unhörbarkeit unterdrückt.** Sie sind die Bewegung, für die das Feature existiert. Eng und getestet begrenzt ist die Tonhöhenstabilität (unter einem Cent bei voller Tiefe) — nicht die Seitenbänder selbst.
- **Keine veröffentlichte CPU-Zahl.** Es gibt in diesem Projekt keinen CPU-Benchmark und kein CI-Performance-Gate — behandle jede CPU-Auslastungszahl, die du woanders siehst, als unverifiziert. Lange Decay-Werte kosten proportional mehr CPU und Speicher, weil Decay auch die Länge des generierten Kernels bestimmt.
- **Das v0.2.0-Voicing ist recherchebasiert, nicht gegen Hardware oder ein kommerzielles Plugin gemessen.** Es stammt aus öffentlichen Handbüchern, Entwickler-Interviews, Fachpresse-Reviews und Raumakustik-Literatur; es wurde weder der tatsächliche Output einer Hardware-Einheit oder eines kommerziellen Plugins gemessen, noch eine Impulsantwort eines Drittanbieters gesampelt oder approximiert.
- **Der prozedurale Generator ist ein vereinfachtes Modell** — ein gefilterter Noise-Burst-Tail plus ein diskreter Early-Reflection-Zug — statt einer physikalischen Simulation des modalen Verhaltens oder der exakten Reflexionsgeometrie eines echten Raums. Er ist auf eine überzeugende cineastische Klangfläche ausgelegt, nicht auf akustische Messgenauigkeit.
- **Die GUI ist ein funktionaler Slider-/Combo-/Toggle-Editor.** Die eigens vektorgezeichnete GUI ist ein späterer Meilenstein.
- **Pre-1.0, AGPLv3.** Breaking Changes bleiben bis v1.0.0 möglich.
