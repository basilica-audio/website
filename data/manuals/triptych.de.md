<!-- German translation of triptych.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Triptych-Icon" width="120"/></p>

# Triptych — Bedienungsanleitung

*Drei Flügel, ein Altarbild — ein 3-Band-Multiband-Kompressor für dichte Mixe.*

## Was es ist

Triptych ist ein 3-Band-Multiband-Kompressor auf Basis von JUCE 8. Es teilt das Signal mit zwei kaskadierten Linkwitz-Riley-Crossovern 4. Ordnung (LR4) in Low-, Mid- und High-Band auf, komprimiert jedes Band unabhängig und summiert sie anschließend mit einem finalen Output-Trim wieder zusammen. Da die Summe aus Low- und High-Anteil des LR4-Crossovers betragsmäßig flach ist, verhält sich Triptych bei deaktiviertem Kompressor in jedem Band (Ratio 1:1, Makeup 0 dB) exakt bitidentisch wie ein reiner Durchlauf des Eingangssignals — der Crossover-Split selbst färbt den Klang nie ein.

Anders als ein Single-Band-Kompressor erlaubt dir Triptych, die Dynamik je Register unterschiedlich zu steuern: die Tiefen eng zusammenziehen, ohne Becken-Transienten anzutasten; eine hart klingende Pick-Attack-Range zähmen, ohne den Tiefton-Punch weicher zu machen; oder Zischlaute in den Höhen wegducken, während die Tiefen unangetastet bleiben.

## Wo es in einer intensiven Produktionskette sitzt

Triptych ist ein **Mastering-/Mixbus-Dynamik-Tool**, kein Effekt für einzelne Instrumente. Typischer Einsatz:

```
Full mix (guitars + orchestra + choir + drums/bass) -> Triptych (multiband glue/control) -> brickwall limiter -> master out
```

Greife danach, wenn ein Single-Band-Kompressor entweder die Tiefen übermäßig zusammendrückt, um Hochfrequenz-Peaks zu kontrollieren, oder die Tiefen locker lässt, während die Höhen schon gut im Griff sind — das klassische Symphony-Metal-Problem einer dichten Wand aus verzerrten Gitarren, Orchester-Hits und Chor, die alle um denselben Headroom konkurrieren. Es funktioniert auch gut als „Glue"-Stufe auf einem Drum-Bus oder einem kompletten Gitarren-Stack, unabhängig vom Gesamtmix.

## Signalfluss

```
                    +-> Band-Strip (Low)  ------------------------------+
Input --> Split @ Low/Mid                 |                             |
                    \-> Split @ Mid/High                                |
                              +-> Band-Strip (Mid)  -------------------+--> Mute/Solo gate --> Sum --> Mix --> Output --> Out
                              \-> Band-Strip (High) + optionaler Limiter-+                      ^
                                                                                                 |
Input (dry, verzögert passend zu Lookahead) --------------------------------------------------------+

Sidechain (optional) --> eigenes Split-Paar, dieselben Frequenzen + Flanke --> Detektor-Key pro Band
```

Jedes Band ist ein Strip statt eines einzelnen Kompressors. Innerhalb eines Strips:

```
key   --> Detektor (Peak-/RMS-Kennlinie -> Auto Release -> Stereo Link -> Character)
             |  Hüllkurve
audio --> Gate (eigener Threshold, eigener Detektor) --> Kompressor (Knee -> Threshold/Ratio -> Range) --> Makeup
             \___ optional in eine Mid/Side-Kodierung/-Dekodierung gewrappt ___/
```

Der **Key** ist das Signal, auf das der Detektor des Kompressors hört: das eigene Audio des Bands (SC Source *Internal*), oder das passende Band des Sidechains (*External*). Das **Gate** keyt immer intern auf das eigene Audio des Bands, unabhängig davon, worauf SC Source steht. Die Gain von Gate und die Gain des Kompressors multiplizieren sich, das Gaten eines Bands wird also nie von der eigenen Kompressionskurve dieses Bands maskiert.

Das High-Band kann danach zusätzlich einen Brickwall-artigen Limiter nach seinem Kompressor aktivieren. Der Beitrag jedes Bands wird anschließend von seinem eigenen Mute/Solo-Status gegatet, die drei Bänder werden summiert, per **Mix** gegen das delay-kompensierte trockene Signal gemischt und vom Master-**Output**-Regler getrimmt.

Die beiden Split-Punkte nutzen dasselbe **Slope**-Setting (12, 24 oder 48 dB/Okt.), ebenso das eigene Crossover-Paar des Sidechains. Die vollständige technische Aufschlüsselung (Flat-Sum-Eigenschaft der Frequenzweiche, der Soft-Knee-Gain-Computer, die Ratio-Aufwärts-/Range-Erweiterung aus v0.3.0, Detektor v2, der Zero-Overshoot-Beweis des Lookahead-Brickwalls, Bypass-Identität des Kompressors, Limiter-Verhalten, Parameter-Smoothing) findest du in [`docs/architecture.md`](architecture.md).

**Ein Hinweis zum Voicing.** Die unten stehenden Per-Band-Defaults (und die Werkspresets in [`docs/presets.md`](presets.md)) sind **recherchebasiert** — sie stützen sich auf veröffentlichte Hersteller-Handbücher und Fachartikel von Mastering-Engineers zur Referenzklasse der Multiband-Kompression, nicht auf Messungen gegen Referenz-Hardware. Die zitierten Quellen/URLs findest du in [`docs/research-notes.md`](research-notes.md), die Begründung für den Soft-Knee aus v0.2.0 in [`docs/design-brief.md`](design-brief.md), und die Ratio/Range-Dynamik-Erweiterung aus v0.3.0 in [`docs/design-brief-v3-dynamics.md`](design-brief-v3-dynamics.md).

**v0.5.0: der Flaggschiff-Dynamikkern.** Der Detektor jedes Bands bekommt eine wählbare **Peak-/RMS**-Kennlinie, ein programmabhängiges **Auto Release**, einen **VCA**-Charakter und einen **Stereo-Link**-Regler. Dazu ein globales **Lookahead** und **Mix**, wählbare **Crossover-Flanken** (12/24/48 dB/Okt.), ein **externer Sidechain** mit Keying pro Band und Detektor-Key-Monitoring sowie **Hold + Hysterese** an jedem Gate. Alle dreiundzwanzig neuen Regler stehen per Default auf einem vollständig neutralen Zustand, sodass eine in v0.4.0 gespeicherte Session in v0.5.0 exakt wie zuvor klingt — und dieselbe Null-Latenz meldet. Auch bestehende Automation überlebt: Die neuen Parameter wurden hinter die neunundfünfzig bereits ausgelieferten angehängt statt dazwischen eingefügt, sodass sich an nichts, was eine ältere Session bereits automatisiert, die Position ändert.

**v0.3.0: echtes dynamisches Multiband.** Die Ratio jedes Bands reicht jetzt von **0.2:1 bis 20:1** (vorher 1:1–20:1) — Werte unter 1:1 sind *aufwärtsgerichtete* Kompression/Expansion: Signal oberhalb des Thresholds wird angehoben statt geschnitten, mit sanftem Übergang durch einen exakten Nullpunkt bei 1:1. Ein neuer Per-Band-Regler **Range** begrenzt die maximale Gain-Änderung (nach oben oder unten), damit eine aggressive Ratio-Einstellung musikalisch nutzbar bleibt, statt durchzugehen. Beide werden in den Tabellen unten beschrieben.

## Parameter-Referenz

### Crossover

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Low/Mid Split** | 40 – 1000 | 200 | Hz | Der Übergangspunkt zwischen Low- und Mid-Band. Alles unterhalb dieser Frequenz gehört zum Low-Band; alles darüber geht in die zweite Frequenzweiche. Ein Mindestabstand zum Mid/High Split wird jederzeit erzwungen, sodass Automation die Bandreihenfolge nie umkehren kann. |
| **Mid/High Split** | 400 – 12000 | 3000 | Hz | Der Übergangspunkt zwischen Mid- und High-Band. |

### Regler je Band (Low, Mid, High – identische Bereiche in jedem Band; **Defaults unterscheiden sich seit v0.2.0 je Band** — siehe Hinweis oben)

| Parameter | Range | Low default | Mid default | High default | Unit | Was es musikalisch bewirkt |
|---|---|---|---|---|---|---|
| **Threshold** | -60 – 0 | -24 | -30 | -20 | dB | Der Pegel, ab dem der Kompressor des Bands mit der Gain Reduction beginnt. Senke ihn ab, um mehr vom Signal zu erfassen; hebe ihn Richtung 0 dB an, um nur die lautesten Peaks zu erwischen. Der niedrigere Default von Mid orientiert sich an der „density/knit-together"-Mastering-Philosophie; Low und High orientieren sich eher an „peak control" (siehe den recherchebasierten Hinweis oben). |
| **Ratio** *(Bereich erweitert in v0.3.0)* | 0.2:1 – 20:1 | 2.5:1 | 1.8:1 | 2:1 | : 1 | Wie hart das Band komprimiert, sobald es über dem Threshold liegt. **1:1 ist ein exakter Bypass** des Kompressors dieses Bands (nützlich zum A/B-Vergleich der Wirkung eines Bands gegen die anderen), unabhängig von Knee/Range. Über 1:1 schneiden höhere Ratios härter (10:1+ nähert sich Limiting an). **Unter 1:1 (v0.3.0) hebt dieselbe Kurve stattdessen an** — „aufwärtsgerichtete Kompression/Expansion": Signal oberhalb des Thresholds wird angehoben, was über-komprimiertem Material Dynamik zurückgibt oder Dichte/Lift hinzufügt. Der Regler ist so zentriert, dass 1:1 in der Mitte seines Stellwegs liegt. |
| **Knee** | 0 – 100 | 50 | 50 | 50 | % | Wie graduell der Kompressor um den Threshold herum in die Gain Reduction übergeht. 0 % ist ein harter Knee (Kompression/Expansion setzt abrupt genau am Threshold ein); 100 % ist der breiteste Soft-Knee-Übergang, skaliert so, dass er vom Threshold bis zum Doppelten seines Abstands zu 0 dBFS reicht — sodass sich die Breite des Knees in dB sinnvoll anpasst, egal ob der Threshold nahe 0 dB oder nahe -50 dB liegt. |
| **Attack** | 0.1 – 100 | 25 | 10 | 5 | ms | Wie schnell der Kompressor reagiert, sobald das Signal den Threshold überschreitet. Der langsamere Default von Low lässt tieffrequente Transienten — denen es ohnehin „an schnellen Transienten mangelt" — durch, bevor die Gain Reduction einsetzt; der schnellere Default von High erwischt schnelles Transientenmaterial. Ein schneller Attack (unter ca. 5 ms) erwischt Transienten hart, kann aber den Anschlag von Plektrum/Schlägel dumpf machen; ein langsamerer Attack erhält den Punch. |
| **Release** | 10 – 1000 | 180 | 100 | 55 | ms | Wie schnell sich die Gain Reduction erholt, sobald das Signal wieder unter den Threshold fällt. Der längere Default von Low (~1.8x Mid) trägt den Ausklang-Eigenschaften tiefer Frequenzen Rechnung; der kürzere Default von High (~0.5x Mid) passt zu schnellerem Transientenmaterial. Ein schneller Release kann bei anhaltendem Material hörbar pumpen; ein langsamer Release glättet die Gain Reduction, kann aber den folgenden Transienten „wegducken", wenn er relativ zum Tempo des Materials zu langsam eingestellt ist. |
| **Makeup** | -12 – +24 | 0 | 0 | 0 | dB | Output-Trim, der nur auf dieses eine Band angewendet wird, nach der Kompression, vor dem Mute/Solo-Gate und der Summierung. Damit stellst du den durch die Gain Reduction verlorenen Pegel wieder her oder balancierst den Beitrag eines Bands zum Mix bewusst neu aus. |

### Range je Band *(neu in v0.3.0)*

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Range On** (Range Enabled) | Off / On | Off | Aktiviert die maximale Gain-Änderungs-Begrenzung des Bands. Standardmäßig aus, sodass sich die Ratio/Knee-Kurve des Bands exakt so verhält, wie es die Tabelle oben beschreibt — ohne Deckel, wie weit sie das Gain nach oben oder unten treiben kann. |
| **Range** | 0 – 30 | 12 | dB | Die maximale Gain-Änderung (Cut *oder* Boost), die der Kompressor des Bands anwenden darf, sobald Range On aktiviert ist. Das ist es, was eine aggressive Ratio-Einstellung — besonders eine stark aufwärtsgerichtete (deutlich unter 1:1), deren Boost sonst unbegrenzt weiterwächst, je weiter das Signal über dem Threshold liegt — musikalisch nutzbar bleiben lässt, statt durchzugehen. Wirkt nur, solange Range On aktiviert ist; der dB-Wert selbst hat keine Wirkung, solange es aus ist. |

### Gate / Downward Expander je Band *(neu in v0.4.0)*

| Parameter | Range | Low default | Mid default | High default | Unit | Was es bewirkt |
|---|---|---|---|---|---|---|
| **Gate On** (Gate Enabled) | Off / On | Off | Off | Off | | Aktiviert den unabhängigen Downward-Expander/Gate des Bands. Standardmäßig aus, sodass sich das Band exakt so verhält, wie es die Kompressor-Tabellen oben beschreiben, ganz ohne Gating. |
| **Gate Threshold** | -80 – 0 | -50 | -55 | -45 | dB | Der Pegel, *unterhalb* dessen das Gate zu dämpfen beginnt — bewusst ein separater, unabhängiger Threshold vom eigenen Threshold des Kompressors oben (typischerweise deutlich darunter angesetzt, sodass das Gate nur in wirklich leises Material/den Rauschteppich hineingreift, nicht in das Programmmaterial, das der Kompressor formt). |
| **Gate Ratio** | 1:1 – 100:1 | 2:1 | 2:1 | 2:1 | : 1 | Wie hart das Gate dämpft, sobald es unter den Gate Threshold fällt. 1:1 ist ein exakter Bypass; höhere Ratios dämpfen steiler pro dB unterhalb des Thresholds (100:1 nähert sich einem harten, On/Off-artigen Gate an). |
| **Gate Attack** | 0.1 – 50 | 10 | 5 | 2 | ms | Wie schnell sich das Gate wieder öffnet, sobald das Signal wieder über den Gate Threshold steigt — bewusst eine schnellere Obergrenze als der eigene Attack des Kompressors, da ein Gate typischerweise schnell reagieren muss, um das Clipping der Transienten-Vorderflanke zu vermeiden. |
| **Gate Release** | 10 – 2000 | 200 | 150 | 100 | ms | Wie schnell sich das Gate schließt, sobald das Signal unter den Gate Threshold fällt — bewusst eine langsamere Obergrenze als der eigene Release des Kompressors, da ein zu schnell schließendes Gate bei Material nahe am Threshold hörbares Chattern verursacht. |

Das Gate läuft unabhängig von, und parallel zu, dem eigenen Kompressor dieses Bands — beide werden vom selben Eingangssignal angesteuert, und ihre Gains multiplizieren sich, sodass das Gating eines Bands nie von (oder im Widerstreit mit) dessen eigener Kompressionskurve maskiert wird. Da das Umschalten von Gate On eine musikalische Entscheidung ist und kein kontinuierlicher Regler, verhält es sich wie jedes Gate: Setze Gate Threshold unter das leiseste Material, das erhalten bleiben soll, und Gate Ratio/Attack/Release nach Geschmack dafür, wie aggressiv und schnell es reagieren soll.

### Mid/Side je Band *(neu in v0.4.0)*

| Parameter | Range | Low default | Mid default | High default | Unit | Was es bewirkt |
|---|---|---|---|---|---|---|
| **M/S On** (M/S Enabled) | Off / On | Off | Off | Off | | Kodiert das Stereosignal dieses Bands vor seiner Gain-Berechnung nach Mid/Side und dekodiert danach wieder zurück nach L/R. Standardmäßig aus, sodass das Band exakt so stereo-verkoppelt bleibt, wie es die Tabellen oben beschreiben. Wirkt nur auf einem echten Stereo-Bus — bei Mono ein defensives No-op. |
| **Side Threshold** | -60 – 0 | -24 | -30 | -20 | dB | Der eigene, unabhängige Threshold der Side-Komponente (Differenz/Breite) — getrennt vom Haupt-Threshold oben, der weiterhin die Mid-Komponente (Zentrum/Summe) ansteuert. |
| **Side Ratio** | 0.2:1 – 20:1 | 1:1 | 1:1 | 1:1 | : 1 | Die eigene Ratio der Side-Komponente, die sich Knee/Attack/Release/Range des Bands mit Mid teilt. Steht auf jedem Band standardmäßig auf 1:1 (exakter Bypass), sodass das bloße Aktivieren von M/S ohne weitere Anpassung nur den Zentrums-Inhalt mit dem bestehenden Threshold/Ratio des Bands komprimiert, während die Stereobreite unangetastet bleibt — ein sinnvoller Ausgangspunkt, um das Zentrum eines Mixes (Vocal, Kick, Bass) zu straffen, ohne seine Breite zu verengen. |

Da L + R nach dem Dekodieren nur von Mid abhängt (algebraisch unabhängig davon, was mit Side geschieht), kann das Bearbeiten der Side-Komponente — wie aggressiv auch immer — niemals ein Phasenauslöschungs-Artefakt in eine Mono-Abmischung einbringen; nur eine Änderung an der Verarbeitung der Mid-Komponente selbst verändert die Mono-Summe, was der beabsichtigte, hörbare Effekt des Komprimierens/Expandierens des Zentrums ist.

### Globale Regler *(neu in v0.5.0)*

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **SC Source** (Sidechain Source) | Internal / External | Internal | | Legt fest, worauf der Kompressor-Detektor jedes Bands hört. *Internal* ist das bandeigene Signal, exakt wie zuvor. *External* keyt die Detektoren stattdessen vom Sidechain-Bus — aufgeteilt durch ein eigenes Weichenpaar bei denselben Frequenzen und derselben Flanke, sodass jedes Band einem bandpassenden Key folgt statt dem vollbandigen Sidechain. Wählst du External, ohne dass der Host einen Sidechain verbunden hat, fällt Triptych stillschweigend auf Internal zurück, statt zu verstummen. |
| **SC Listen** (Sidechain Listen) | Off / Low / Mid / High | Off | | Ersetzt den Output durch den **Detektor-Key** des gewählten Bands, damit du beim Einstellen der Thresholds genau hörst, worauf die Detektoren reagieren. Das ist *kein* Band-Solo — es ist das Key-Signal, nicht das bearbeitete Audio. Eine Abhörhilfe, nicht für Automation gedacht. |
| **Slope** (Crossover Slope) | 12 / 24 / 48 dB/Okt. | 24 dB/Okt. | | Die Flankensteilheit beider Weichen-Aufteilungen. 24 dB/Okt. ist die klassische Einstellung und das, was jede frühere Version genutzt hat. 12 dB/Okt. lässt die Bänder stärker überlappen (sanftere, „analogere" Band-Interaktion); 48 dB/Okt. trennt sie hart, was du willst, wenn die Bearbeitung eines Bands nicht in seine Nachbarn bluten darf. Ein Flankenwechsel setzt die Weichenfilter zurück und kann klicken — ändere ihn bei gestopptem Transport. |
| **Lookahead** | Off / 1.5 / 3 / 5 ms | Off | | Lässt die Detektoren das Signal sehen, bevor es eintrifft, sodass die Gain-Reduktion bereits steht, wenn ein Transient kommt. Kostet genau so viel Latenz, die zur Delay-Kompensation an den Host gemeldet wird (siehe die Latenztabelle unten). Off ist der Default und hält Triptych bei null Latenz. |
| **Mix** | 0 – 100 | 100 | % | Dry/Wet-Blend um die gesamte Multiband-Kette — Parallelkompression ohne separaten Bus. Der Dry-Pfad wird passend zur Lookahead-Einstellung verzögert, sodass die beiden ausgerichtet bleiben. Beachte, dass das Mischen eines *minimalphasigen* Multiband-Baums gegen ein Dry-Signal das Ergebnis selbst bei sanften Einstellungen färbt: Triptychs Bandsumme ist magnitudenflach, aber nicht phasenflach, die beiden Pfade interagieren also. Das liegt am Parallelmischen jedes minimalphasigen Multiband-Prozessors und ist kein Defekt — nutze deine Ohren, statt anzunehmen, 50 % sei „der halbe Effekt". |

### Detektor je Band *(neu in v0.5.0)*

Identische Bereiche in jedem Band.

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Detector** | Peak / RMS | Peak | | Die Detektionskennlinie. *Peak* folgt den momentanen Spitzen der Wellenform — das strammere, transientenbewusstere Verhalten, das jede frühere Version genutzt hat. *RMS* folgt stattdessen der mittleren Leistung des Signals, was bei einem Sinus 3 dB unter der Peak-Kennlinie liegt und generell glatter und eher „pegelbezogen" als „transientenbezogen" klingt. RMS nutzt eine Mean-Square-Zeitkonstante von `max(Attack, 5 ms)` vor der bandeigenen Attack-/Release-Ballistik. |
| **Auto Rel** (Auto Release) | Off / On | Off | | Programmabhängiges Release. Zwei Release-Konstanten laufen parallel — eine schnelle (0,15 s) und ein langsames Reservoir (Aufladung 0,6 s, Release 4 s) — und die Hüllkurve nimmt die jeweils höhere. Eine kurze Spitze erholt sich schnell; anhaltende Gain-Reduktion baut einen mehrsekündigen Ausklang auf, der das Band vom Pumpen abhält. Der Release-Regler skaliert beide Konstanten, tut also weiterhin, was du erwartest; bei etwa 300 ms reproduziert er die Referenzwerte exakt. |
| **Character** | Clean / VCA | Clean | | *Clean* ist das Feed-Forward-Verhalten jeder früheren Version. *VCA* approximiert statisch die Schleife eines Feedback-Kompressors: Der Knee rundet sich um einen ratio-abhängigen Betrag (etwa 6 dB bei 2:1, 4 dB bei 4:1, 3 dB bei 10:1), und der effektive Attack wird mit steigender Ratio schneller. Es gibt bewusst **keine** hinzugefügte Verzerrung und keine Harmonischen-Stufe — der Unterschied zwischen beiden liegt im Hüllkurvenverhalten, und dort sitzt der Charakter dieser Kompressorklasse tatsächlich. |
| **Link** (Stereo Link) | 0 – 100 | 0 | % | Wie stark sich die Detektoren beider Kanäle eine Hüllkurve teilen. Bei 0 % sind sie vollständig unabhängig, was jede frühere Version getan hat — und was einen hart gepannten Transienten eine Seite für sich herunterziehen und das Stereobild verschieben lässt. Bei 100 % wenden beide Kanäle exakt denselben Gain an, das Bild kann sich also überhaupt nicht bewegen. Alles dazwischen mischt die beiden. In einem Band, das Mid/Side fährt, verkoppelt das stattdessen das Mid-/Side-Paar. |

**Ein Hinweis zum VCA-Knee nahe einem 0-dB-Threshold.** Triptychs Knee ist konstruktionsbedingt *threshold-relativ* (seine Breite skaliert damit, wie weit der Threshold unter 0 dBFS liegt — siehe [`docs/architecture.md`](architecture.md)). Das bedeutet, dass die Ziel-Knee-Breite des VCA-Charakters unerreichbar wird, sobald der Threshold innerhalb einer halben Knee-Breite von 0 dB liegt: Ab etwa -3 dB aufwärts verengt sich die erreichte Breite gleichmäßig Richtung Hard Knee und erreicht bei einem 0-dB-Threshold exakt Hard Knee. Das ist eine Eigenschaft des Knee-Modells und kein Bug, und numerisch verhält sich dort nichts daneben. Willst du die volle VCA-Rundung, halte den Threshold des Bands bei -3 dB oder darunter — dort sitzt der Threshold eines Multiband-Kompressors ohnehin normalerweise.

Diese vier Regler formen nur den Detektor des **Kompressors**. Das Gate des Bands behält seinen eigenen, separaten Envelope-Follower mit eigenem Attack/Release — ein Band auf RMS zu stellen, oder Auto Release oder VCA-Charakter zu aktivieren, ändert also, wie das Band *komprimiert*, ohne zu ändern, wie es *gatet*.

### Gate-Formung je Band *(neu in v0.5.0)*

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Gate Hold** | 0 – 500 | 0 | ms | Wie lange das Gate offen bleibt, nachdem das Signal wieder unter seinen Threshold gefallen ist. Stelle es länger als die Lücken ein, die du ignorieren willst (das Ausklingen einer Note, der Abstand zwischen zwei Schlägen desselben Parts), und das Gate hört auf, sie zu zerhacken. Der Timer startet bei jeder neuen Überschreitung neu, sodass eine Folge eng aufeinanderfolgender Schläge das Gate durchgehend offen hält. |
| **Gate Hyst** (Gate Hysteresis) | 0 – 12 | 0 | dB | Trennt den Pegel, bei dem das Gate *öffnet*, von dem, bei dem es *schließt*, und schließt um so viele dB tiefer. Das ist die Abhilfe gegen Chattern — ein Signal, das genau am Threshold schwebt und das Gate viele Male pro Sekunde auf- und zuklappen lässt. Stelle es einige dB über die hörbare Welligkeit; 3–6 dB decken die meisten Materialien ab. |

Beide stehen per Default auf 0, was exakt dem Gate aus v0.4.0 entspricht. Beide sind zudem so implementiert, dass keines klicken kann: Hold arbeitet auf der Hüllkurve des Gates, statt seinen Ausgangs-Gain festzunageln, und der Threshold bewegt sich durch denselben 50-ms-Glätter, den jede andere Threshold-Änderung nutzt.

### Gain-Reduktions-Meter *(neu in v0.5.0)*

Jede Bandspalte trägt einen schmalen vertikalen Balken, der zeigt, wie stark dieses Band das Signal gerade herunterzieht (Kompressor und Gate zusammen), mit einer langsam abfallenden Peak-Hold-Linie. Vollausschlag sind 24 dB. Sie sind schreibgeschützt — es gibt sie, damit du auf einen Blick siehst, welches Band die Arbeit macht.

### Mute/Solo je Band (Low, Mid, High)

| Parameter | Values | Default | Was es bewirkt |
|---|---|---|---|
| **Mute** | Off / On | Off | Stummt den Beitrag dieses Bands zur Summe. Sein Kompressor läuft darunter weiter (damit es beim Un-Muten mitten in der Wiedergabe keinen erneuten Attack-Pop gibt), er erreicht nur den Ausgang nicht. **Mute gewinnt immer** gegen Solo — ein Band, das gleichzeitig gemutet und gesolot ist, bleibt stumm. |
| **Solo** | Off / On | Off | Isoliert dieses Band: Sobald ein Band gesolot ist, erreichen nur gesolote (und nicht gemutete) Bänder die Summe. Werden mehrere Bänder gleichzeitig gesolot, werden sie gemeinsam gesolot. Nutze das, um die Kompressor-Einstellungen eines Bands isoliert zu beurteilen, oder um zu prüfen, was ein Band tatsächlich enthält, bevor du entscheidest, wie hart du es komprimierst. |

### High-Band-Limiter

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Limiter** (enable) | Off / On | Off | Aktiviert einen zusätzlichen Brickwall-artigen Limiter nach dem eigenen Kompressor + Makeup Gain des High-Bands, um scharfe Becken-/Oberton-Peaks abzufangen, die ein musikalisch eingestellter Kompressor (mit einem Attack, der lang genug ist, um den Transienten-Charakter zu erhalten) sonst durchlassen würde. Garantiert, dass der Ausgang des High-Bands 0 dBFS nie überschreitet, sobald er aktiv ist — unabhängig von Threshold oder vorgeschaltetem Makeup. |
| **Lim. Thresh.** (High Limiter Threshold) | -24 – 0 | -3 | dB | Der Threshold des Limiters. Niedrigere Werte drücken härter zusammen und wenden proportional mehr internes Makeup Gain an, um das auszugleichen (ein Limiter im „Loudness"-Stil, kein simpler Peak-Fänger) — die Decke selbst liegt unabhängig von dieser Einstellung immer exakt bei 0 dBFS; was sich ändert, ist, wie viel vom High-Band heruntergezogen wird, um darunter Platz zu schaffen. |

### Output

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Output** | -24 – +24 | 0 | dB | Master-Trim, der angewendet wird, nachdem die drei Bänder summiert wurden — die finale Gain-Stufe im Plugin. Nutze ihn, um den Ausgangspegel von Triptych an das anzupassen, was als Nächstes in der Kette folgt (typischerweise ein Brickwall-Limiter auf dem Master-Bus). |

### Regler, die man bei gestopptem Transport ändert

Jeder **kontinuierliche** Regler in Triptych ist konstruktionsbedingt klickfrei — Thresholds, Ratios, Knees, Ranges, Gains, Stereo Link und Hold/Hysterese des Gates laufen allesamt durch Smoother, und das Gate ist so spezifiziert, dass seine Gain in einem einzigen Sample nie mehr als 0,5 dB springen kann. Automatisiere sie frei.

Vier **gestufte** Regler bauen den Signalpfad um, statt nur einen Wert zu bewegen, und können klicken, wenn du sie mitten in der Wiedergabe änderst:

- **Slope** — setzt die Crossover-Filter zurück.
- **M/S On** — ändert, worauf sich die Gain-Berechnung des Bands anwendet.
- **Limiter (enable)** — für sich genommen klickfrei, aber während **Lookahead** aktiv ist, verschiebt das Umschalten, wo dieses Band seine Verzögerung verbringt (siehe unten), was das Band umbaut.
- **Lookahead** — ändert die gemeldete Latenz, sodass der Host die Delay-Kompensation neu aushandeln muss.

Keiner davon ist ein Defekt, und keiner ist ungewöhnlich für die Aufgabe, die er erfüllt; es sind schlicht Konfigurationsänderungen statt Performance-Regler.

**Wo die Lookahead-Verzögerung lebt.** Bei aktiviertem Lookahead verbringt ein Band seine Verzögerung an einem von zwei Orten: Entweder bekommt der Kompressor den Vorsprung (das Audio wird verzögert, während der Detektor vorausliest), oder — falls der Brickwall-Limiter dieses Bands ebenfalls aktiv ist — übernimmt der Limiter stattdessen die Verzögerung, was ihn erst wirklich überschwing-sicher macht. Genau einer von beiden besitzt sie, sodass das Band immer exakt die Lookahead-Länge hinzufügt und alle drei Bänder in der Summe ausgerichtet bleiben. Der Trade-off: Der Kompressor des High-Bands gibt seinen Vorsprung auf, während der Brickwall an ist — die richtige Entscheidung für eine Stufe, deren gesamter Job die Ceiling ist.

## Latenz und Host-Delay-Kompensation *(neu in v0.5.0)*

Steht **Lookahead** auf dem Default *Off*, meldet Triptych **null Latenz** — die Weichen sind minimalphasige IIR-Filter und die Detektoren kausal, es verzögert also nichts in der Kette das Signal. Jede vor v0.5.0 gespeicherte Session behält dieses Verhalten, weil es den Parameter nicht gab.

Lookahead zu aktivieren meldet exakt Folgendes, und Hosts kompensieren automatisch:

| Lookahead | 44,1 kHz | 48 kHz | 88,2 kHz | 96 kHz | 192 kHz |
|---|---|---|---|---|---|
| Off | 0 | 0 | 0 | 0 | 0 |
| 1,5 ms | 66 | 72 | 132 | 144 | 288 |
| 3 ms | 132 | 144 | 265 | 288 | 576 |
| 5 ms | 221 | 240 | 441 | 480 | 960 |

(Samples, auf ganze Samples gerundet — Hosts akzeptieren nur ganzzahlige Delay-Kompensation.)

Lookahead bei laufendem Transport zu ändern lässt den Host seine Delay-Kompensation neu aushandeln, was die meisten Hosts mit einer kurzen Unterbrechung erledigen. Das ist branchenüblich für jeden Lookahead-Regler; wenn es dich stört, stelle ihn ein, bevor du auf Play drückst.

## Sidechain-Routing pro Host

Der Sidechain-Input ist **optional und standardmäßig deaktiviert**, sodass Triptych auch in Hosts normal lädt, die keinen anbieten (einschließlich des eigenen Standalone-Builds, der überhaupt keinen Sidechain hat).

- **Logic Pro (AU)**: Wähle die Quellspur im *Side Chain*-Menü im Plugin-Header und stelle dann **SC Source** auf *External*.
- **Cubase / Nuendo (VST3)**: Aktiviere den Sidechain-Input über den Sidechain-Button im Plugin-Header und route dann einen Send von der Quellspur dorthin.
- **Reaper (VST3)**: Gib der Triptych-Spur 4 Eingangskanäle, route die Quellspur auf deren Kanäle 3/4 und pinne Kanäle 3/4 in der Routing-Matrix des Plugins auf dessen Sidechain-Input.
- **Ableton Live (VST3/AU)**: Live legt Sidechain-Inputs für Drittanbieter-Plugins nicht so offen wie für seine eigenen Devices; nutze einen Return-/Aux-Routing-Workaround oder lass **SC Source** auf *Internal*.
- **Standalone**: Es existiert kein Sidechain-Bus. *External* fällt stillschweigend auf *Internal* zurück.

Ein Mono-Sidechain wird auf beide Detektorkanäle dupliziert. Das **Gate** keyt unabhängig von dieser Einstellung immer intern, auf dem bandeigenen Signal — ein Gate ist ein Bleed-/Noise-Werkzeug für das Material, das tatsächlich im Band liegt.

## Crossover-Flanken und Phase

Triptychs drei Bänder entstehen aus zwei in Serie kaskadierten Weichen: Die erste trennt Low von allem anderen, die zweite teilt den Rest in Mid und High. Dieser Baum ist **unkompensiert** — die Phasendrehung der zweiten Aufteilung landet auf Mid und High, aber nicht auf Low. Die Bandsumme bleibt magnitudenflach (das ist die Linkwitz-Riley-Eigenschaft, auf der Triptych aufbaut), aber sie ist nicht phasenflach, und der Betrag der Drehung skaliert mit der gewählten Flanke:

| Flanke | Genauigkeit der flachen Summe | Phasenverhalten |
|---|---|---|
| 12 dB/Okt. | innerhalb ±0,25 dB | halb so viel Drehung wie der Default |
| 24 dB/Okt. | innerhalb ±0,1 dB | das Referenzverhalten, unverändert seit v0.1 |
| 48 dB/Okt. | innerhalb ±0,25 dB | doppelt so viel Drehung wie der Default |

Das zählt in genau zwei Situationen: wenn du Triptychs Output gegen eine Dry-Kopie desselben Signals mischst (der **Mix**-Regler oder ein externer Parallelbus), und wenn jemand das Plugin mit einem phasenbewussten Analyzer misst. Für normalen seriellen Einsatz spielt es keine Rolle. Allpass-Kompensation des Low-Zweigs und ein linearphasiger Modus sind gemeinsam für v0.6.0 eingeplant, wo sich die Änderung des Default-Klangs mit einer ordentlichen state-versionierten Migration abfangen lässt.

## Presets

Triptych bringt neun Werkspresets mit (Default, Density Glue, Peak Control, Low-End Tighten, De-Harsh Highs, Mastering Safety Ceiling, Parallel-Style Density, Hard Limiter Ceiling, Glue Master), die sowohl die Peak-Control- als auch die Density-Mastering-Philosophie abdecken — beide in [`docs/research-notes.md`](research-notes.md) dokumentiert —, dazu Workflow-Presets mit Fokus auf einzelne Bänder. Wofür jedes einzelne gedacht ist, steht in [`docs/presets.md`](presets.md). Die Preset-Leiste am oberen Rand des Plugin-Fensters lässt dich Werks- und eigene Presets durchstöbern, deine eigenen speichern/umbenennen/löschen, einen Default festlegen, der bei jeder frischen Instanz automatisch geladen wird, und einzelne Presets oder ganze Preset-Bänke importieren/exportieren (`.basilicapreset`/`.zip`). Eigene Presets werden pro Plugin unter `~/Library/Audio/Presets/Yves Vogl/Triptych/` auf macOS gespeichert (`%APPDATA%\Yves Vogl\Triptych\Presets\` unter Windows).

## Lokalisierung

Die Beschriftungen, Menüs und Dialoge der Preset-Leiste folgen automatisch deiner Systemsprache — Deutsch, wenn deine Systemsprache mit „de" beginnt, sonst Englisch. Das betrifft ausschließlich die eigenen Interface-Texte der Preset-Leiste; Parameternamen, Einheiten und jeder andere Fachbegriff in dieser Anleitung bleiben unabhängig von der Systemsprache auf Englisch, genau wie bei jedem anderen Plugin der Suite.

## Tipps

- **Beginne mit den Crossover-Punkten, nicht mit den Kompressoren.** Sole nacheinander jedes Band (siehe Mute/Solo oben), um genau zu hören, welcher Inhalt wo landet, bevor du an Threshold/Ratio gehst — ein zu hoch angesetzter Low/Mid Split zieht Kick-Drum-Klick oder Palm-Mute-Anschlag ins Low-Band, wodurch es unvorhersehbar komprimiert.
- **Nutze Solo, um den Kompressor jedes Bands isoliert einzustellen**, dann Solo aufheben und den gesamten Mix anhören — eine Einstellung, die solo gut klingt, kann im Kontext trotzdem falsch sein (Überkomprimierung in einem Band ist gegen die anderen beiden oft hörbarer als isoliert).
- **Halte den Attack des Low-Bands langsamer als bei Mid/High**, wenn die Tiefen Bass oder Kick enthalten — ein sehr schneller Attack dort flacht den Punch tiefer Transienten schnell ab, während Mid/High-Inhalt (Gitarren, Becken, Chor-Sibilanz) einen schnelleren Attack meist verträgt (und oft davon profitiert).
- **Greife zum High-Band-Limiter statt zu einer niedrigeren High-Ratio**, wenn das Problem speziell scharfe, gelegentliche Peaks sind (Becken-Crashes, Orchester-Hits) statt des allgemeinen Pegels des High-Bands — ein Limiter fängt die Peaks ab, ohne den Rest des Bands hörbar zusammenzudrücken, wie es eine Kompressor-Einstellung mit niedriger Ratio/niedrigem Threshold täte.
- **Mute, statt Makeup einfach auf -12 dB zu ziehen**, wenn du einen Mix wirklich ohne den Beitrag eines Bands beurteilen willst — Mute (und Solo) tasten die Kompressor-Einstellungen dieses Bands überhaupt nicht an, sodass dein Feintuning vom A/B-Vergleich unberührt bleibt.
- **Stell das Makeup je Band ein, um die Gain Reduction auszugleichen, und nutze den Master-Output für die Gesamtpegel-Anpassung** — diese beiden Aufgaben getrennt zu halten, macht es viel einfacher zu erkennen, ob ein Mix-Problem ein Balance-Problem zwischen den Bändern ist oder schlicht „alles zu laut/zu leise".
- **Aktiviere Range, bevor du die Ratio unter 1:1 schiebst** (aufwärtsgerichtete Kompression/Expansion) — der Boost eines aufwärtsgerichteten Bands wächst weiter, je weiter das Signal über dem Threshold liegt, ohne eigene Obergrenze. Range gibt dir ein musikalisch sinnvolles Maximum, bevor du eine aggressive Aufwärts-Einstellung reindrehst, statt die Grenze erst nachträglich mit dem Ohr zu entdecken.
- **Dreh Stereo Link hoch, bevor du einem wandernden Klangbild hinterherjagst.** Wenn ein hart gepannter Schlag den Mix bei aktivem Triptych zu einer Seite kippen lässt, sind das die unabhängig arbeitenden Detektoren beider Kanäle. Link auf 100 % zwingt beide Kanäle zum selben Gain und behebt es rundheraus; 60–80 % behalten etwas Reaktionsfähigkeit pro Seite und nageln das Bild trotzdem fest.
- **Greife zu Auto Release, bevor du zu einem langsameren Release-Regler greifst.** Ein langsames Release stoppt das Pumpen, macht das Band aber auch träge bei Transienten. Auto Release gibt dir beides: schnelle Erholung von kurzen Spitzen, einen langen Ausklang nur dann, wenn das Band wirklich arbeitet.
- **Nutze SC Listen, um Sidechain-Thresholds einzustellen, nicht deine Vorstellungskraft.** Schalte es auf das Band, das du keyst, stelle den Threshold des Bands nach Gehör gegen das ein, was du tatsächlich hörst, und schalte es dann wieder auf Off. Es spielt das Key-Signal ab, nicht das Band — und genau darauf bezieht sich ein Threshold.
- **Lookahead ist für das Safety Ceiling, nicht für alles.** Sein eigentlicher Nutzen ist der Brickwall des High-Bands, der mit aktivem Lookahead wirklich überschwingfrei wird. Nutzt du den Limiter nicht, lohnt sich die Latenz meist nicht.
- **Wähle die Crossover-Flanke nach der Aufgabe, nicht nach der Zahl.** 48 dB/Okt., wenn die Bearbeitung eines Bands nicht in seine Nachbarn bluten darf (ein harter De-Esser-Band, eine straffe Low-End-Klemme); 12 dB/Okt., wenn die Bänder sanft ineinander übergeben und sich eher wie ein Breitbandkompressor mit Tilt verhalten sollen.

## Bekannte Einschränkungen

- **Der Spectrum-on-Curve-Analyzer ist nicht Teil dieses Releases.** v0.5.0 liefert nur die drei Gain-Reduktions-Balken pro Band (siehe „Gain-Reduktions-Meter" oben); ein Frequenzbereich-Analyzer-Overlay ist für den M3-Custom-GUI-Meilenstein vorgesehen, nicht spät gestrichen.
- **Verschoben auf v0.6.0+**: ein linearphasiger FIR-Crossover-Modus (gepaart mit Allpass-Kompensation für das Phasenverhalten darunter), Sidechain-EQ pro Band, Dry/Wet-Mix pro Band, sample-genaue Parameter-Interpolation (das heutige Smoothing löst über einen 50-ms-Timer auf statt pro Sample), sowie ein Gate-Range-Boden.
- **Der Drei-Band-Crossover-Baum ist magnitudenflach, aber nicht phasenflach** bei keinem Slope-Setting — siehe „Crossover-Flanken und Phase" oben. Das spielt nur eine Rolle, wenn Triptychs Output gegen eine trockene Kopie desselben Signals gemischt wird (auch über **Mix**) oder bei Messung mit einem phasenbewussten Analyzer; für normalen seriellen Einsatz spielt es keine Rolle.
- **Die Ziel-Breite des VCA-Knees wird innerhalb von etwa 3 dB eines 0-dB-Thresholds unerreichbar** — siehe den Hinweis unter „Detektor je Band" oben. Die erreichte Breite verengt sich gleichmäßig Richtung Hard Knee, je näher der Threshold an 0 dB kommt; nichts verhält sich dabei numerisch daneben, aber die volle VCA-Rundung braucht einen Threshold bei -3 dB oder darunter.
- **Vier gestufte Regler können klicken, wenn man sie mitten in der Wiedergabe ändert** — Slope, M/S On, Limiter (enable) bei aktivem Lookahead, und Lookahead selbst — siehe „Regler, die man bei gestopptem Transport ändert" oben. Jeder kontinuierliche, automatisierbare Regler ist konstruktionsbedingt klickfrei.
- **Das Voicing ist durchgehend recherchebasiert**, entnommen aus veröffentlichten Hersteller-Handbüchern und Fachartikeln von Mastering-Engineers zur Referenzklasse der Multiband-Kompression — nicht gegen Referenz-Hardware gemessen. Die belegten Erkenntnisse stehen in [`docs/research-notes.md`](research-notes.md).
