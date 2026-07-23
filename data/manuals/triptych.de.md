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
                    +-> BandComp (Low)  --------------------------------+
Input --> LR4 @ Low/Mid Split             |                             |
                    \-> LR4 @ Mid/High Split                            |
                              +-> BandComp (Mid)  ----------------------+--> Mute/Solo gate --> Sum --> Output --> Out
                              \-> BandComp (High) + optional Limiter ---+
```

Der eigene Kompressor jedes Bands (Knee → Threshold/Ratio → Range → Attack/Release + Makeup) läuft zuerst; das High-Band kann danach zusätzlich einen Brickwall-artigen Limiter nach seinem Kompressor aktivieren. Der Beitrag jedes Bands wird anschließend von seinem eigenen Mute/Solo-Status gegatet, bevor die drei Bänder summiert und vom Master-Output-Regler getrimmt werden. Die vollständige technische Aufschlüsselung (Flat-Sum-Eigenschaft der Frequenzweiche, der Soft-Knee-Gain-Computer, die Ratio-Aufwärts-/Range-Erweiterung aus v0.3.0, Bypass-Identität des Kompressors, Limiter-Verhalten, Parameter-Smoothing) findest du in [`docs/architecture.md`](architecture.md).

**Ein Hinweis zum Voicing.** Die unten stehenden Per-Band-Defaults (und die Werkspresets in [`docs/presets.md`](presets.md)) sind **recherchebasiert** — sie stützen sich auf veröffentlichte Hersteller-Handbücher und Fachartikel von Mastering-Engineers zur Referenzklasse der Multiband-Kompression, nicht auf Messungen gegen Referenz-Hardware. Die zitierten Quellen/URLs findest du in [`docs/research-notes.md`](research-notes.md), die Begründung für den Soft-Knee aus v0.2.0 in [`docs/design-brief.md`](design-brief.md), und die Ratio/Range-Dynamik-Erweiterung aus v0.3.0 in [`docs/design-brief-v3-dynamics.md`](design-brief-v3-dynamics.md).

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

## Presets

Triptych bringt acht Werkspresets mit (Default, Density Glue, Peak Control, Low-End Tighten, De-Harsh Highs, Mastering Safety Ceiling, Parallel-Style Density, Hard Limiter Ceiling), die sowohl die Peak-Control- als auch die Density-Mastering-Philosophie abdecken — beide in [`docs/research-notes.md`](research-notes.md) dokumentiert —, dazu Workflow-Presets mit Fokus auf einzelne Bänder. Wofür jedes einzelne gedacht ist, steht in [`docs/presets.md`](presets.md). Die Preset-Leiste am oberen Rand des Plugin-Fensters lässt dich Werks- und eigene Presets durchstöbern, deine eigenen speichern/umbenennen/löschen, einen Default festlegen, der bei jeder frischen Instanz automatisch geladen wird, und einzelne Presets oder ganze Preset-Bänke importieren/exportieren (`.basilicapreset`/`.zip`). Eigene Presets werden pro Plugin unter `~/Library/Audio/Presets/Yves Vogl/Triptych/` auf macOS gespeichert (`%APPDATA%\Yves Vogl\Triptych\Presets\` unter Windows).

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
