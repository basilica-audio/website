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

Greife danach, wenn ein Single-Band-Kompressor entweder die Tiefen übermäßig zusammendrückt, um Hochfrequenz-Peaks zu kontrollieren, oder die Tiefen locker lässt, während die Höhen schon gut im Griff sind — das klassische Problem einer dichten Wand aus verzerrten Gitarren, Orchester-Hits und Chor, die alle um denselben Headroom konkurrieren. Es funktioniert auch gut als „Glue"-Stufe auf einem Drum-Bus oder einem kompletten Gitarren-Stack, unabhängig vom Gesamtmix.

## Signalfluss

```
                    +-> BandComp (Low)  --------------------------------+
Input --> LR4 @ Low/Mid Split             |                             |
                    \-> LR4 @ Mid/High Split                            |
                              +-> BandComp (Mid)  ----------------------+--> Mute/Solo gate --> Sum --> Output --> Out
                              \-> BandComp (High) + optional Limiter ---+
```

Der eigene Kompressor jedes Bands (Threshold/Ratio/Attack/Release + Makeup) läuft zuerst; das High-Band kann danach zusätzlich einen Brickwall-artigen Limiter nach seinem Kompressor aktivieren. Der Beitrag jedes Bands wird anschließend von seinem eigenen Mute/Solo-Status gegatet, bevor die drei Bänder summiert und vom Master-Output-Regler getrimmt werden. Die vollständige technische Aufschlüsselung (Flat-Sum-Eigenschaft der Frequenzweiche, Bypass-Identität des Kompressors, Limiter-Verhalten, Parameter-Smoothing) findest du in [`docs/architecture.md`](architecture.md).

## Parameter-Referenz

### Crossover

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Low/Mid Split** | 40 – 1000 | 200 | Hz | Der Übergangspunkt zwischen Low- und Mid-Band. Alles unterhalb dieser Frequenz gehört zum Low-Band; alles darüber geht in die zweite Frequenzweiche. Ein Mindestabstand zum Mid/High Split wird jederzeit erzwungen, sodass Automation die Bandreihenfolge nie umkehren kann. |
| **Mid/High Split** | 400 – 12000 | 3000 | Hz | Der Übergangspunkt zwischen Mid- und High-Band. |

### Regler je Band (Low, Mid, High – identische Bereiche in jedem Band)

| Parameter | Range | Default | Unit | Was es musikalisch bewirkt |
|---|---|---|---|---|
| **Threshold** | -60 – 0 | -18 | dB | Der Pegel, ab dem der Kompressor des Bands mit der Gain Reduction beginnt. Senke ihn ab, um mehr vom Signal zu erfassen; hebe ihn Richtung 0 dB an, um nur die lautesten Peaks zu erwischen. |
| **Ratio** | 1:1 – 20:1 | 4:1 | : 1 | Wie hart das Band komprimiert, sobald es über dem Threshold liegt. 1:1 ist ein exakter Bypass des Kompressors dieses Bands (nützlich zum A/B-Vergleich der Wirkung eines Bands gegen die anderen). Höhere Ratios (10:1+) nähern sich Limiting an. |
| **Attack** | 0.1 – 100 | 10 | ms | Wie schnell der Kompressor reagiert, sobald das Signal den Threshold überschreitet. Ein schneller Attack (unter ca. 5 ms) erwischt Transienten hart, kann aber den Anschlag von Plektrum/Schlägel bei Drums und Gitarren dumpf machen; ein langsamerer Attack lässt Transienten durch, bevor die Gain Reduction einsetzt, und erhält so den Punch. |
| **Release** | 10 – 1000 | 100 | ms | Wie schnell sich die Gain Reduction erholt, sobald das Signal wieder unter den Threshold fällt. Ein schneller Release kann bei anhaltendem Material (Bass, gehaltene Flächen) hörbar pumpen; ein langsamer Release glättet die Gain Reduction, kann aber den folgenden Transienten „wegducken", wenn er relativ zum Tempo des Materials zu langsam eingestellt ist. |
| **Makeup** | -12 – +24 | 0 | dB | Output-Trim, der nur auf dieses eine Band angewendet wird, nach der Kompression, vor dem Mute/Solo-Gate und der Summierung. Damit stellst du den durch die Gain Reduction verlorenen Pegel wieder her oder balancierst den Beitrag eines Bands zum Mix bewusst neu aus. |

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

## Tipps

- **Beginne mit den Crossover-Punkten, nicht mit den Kompressoren.** Sole nacheinander jedes Band (siehe Mute/Solo oben), um genau zu hören, welcher Inhalt wo landet, bevor du an Threshold/Ratio gehst — ein zu hoch angesetzter Low/Mid Split zieht Kick-Drum-Klick oder Palm-Mute-Anschlag ins Low-Band, wodurch es unvorhersehbar komprimiert.
- **Nutze Solo, um den Kompressor jedes Bands isoliert einzustellen**, dann Solo aufheben und den gesamten Mix anhören — eine Einstellung, die solo gut klingt, kann im Kontext trotzdem falsch sein (Überkomprimierung in einem Band ist gegen die anderen beiden oft hörbarer als isoliert).
- **Halte den Attack des Low-Bands langsamer als bei Mid/High**, wenn die Tiefen Bass oder Kick enthalten — ein sehr schneller Attack dort flacht den Punch tiefer Transienten schnell ab, während Mid/High-Inhalt (Gitarren, Becken, Chor-Sibilanz) einen schnelleren Attack meist verträgt (und oft davon profitiert).
- **Greife zum High-Band-Limiter statt zu einer niedrigeren High-Ratio**, wenn das Problem speziell scharfe, gelegentliche Peaks sind (Becken-Crashes, Orchester-Hits) statt des allgemeinen Pegels des High-Bands — ein Limiter fängt die Peaks ab, ohne den Rest des Bands hörbar zusammenzudrücken, wie es eine Kompressor-Einstellung mit niedriger Ratio/niedrigem Threshold täte.
- **Mute, statt Makeup einfach auf -12 dB zu ziehen**, wenn du einen Mix wirklich ohne den Beitrag eines Bands beurteilen willst — Mute (und Solo) tasten die Kompressor-Einstellungen dieses Bands überhaupt nicht an, sodass dein Feintuning vom A/B-Vergleich unberührt bleibt.
- **Stell das Makeup je Band ein, um die Gain Reduction auszugleichen, und nutze den Master-Output für die Gesamtpegel-Anpassung** — diese beiden Aufgaben getrennt zu halten, macht es viel einfacher zu erkennen, ob ein Mix-Problem ein Balance-Problem zwischen den Bändern ist oder schlicht „alles zu laut/zu leise".
