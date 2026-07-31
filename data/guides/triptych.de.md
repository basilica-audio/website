# Triptych — Praxis-Guide

*Praxisnahe Einstellungen für den 3-Band-Multiband-Kompressor, verankert in den Werkspresets.*

## Wo es hingehört

Triptych ist ein Mastering-/Mix-Bus-Dynamics-Tool, kein Effekt pro Instrument. Greif danach, wenn ein Single-Band-Kompressor entweder das Low End überkomprimiert, um High-Frequency-Peaks zu kontrollieren, oder das Low End locker lässt, während die Höhen schon gezähmt sind — das klassische Symphonic-Metal-Problem, bei dem Gitarren, Orchester-Hits und Chor alle um denselben Headroom kämpfen. Es funktioniert auch als Glue auf einem Drum-Bus oder einem vollen Gitarren-Stack, unabhängig von der Gesamtmischung.

```
Voller Mix (Gitarren + Orchester + Chor + Drums/Bass) → Triptych (Multiband-Glue/-Kontrolle) → Brickwall-Limiter → Master Out
```

## Quick-Start-Einstellungen

### Density/Glue ohne Überquetschen — *Density Glue*, *Glue Master*

Density Glue: Low Threshold −32 dB/Ratio 1,3:1, **Mid Ratio 0,7:1 (upward)**, High Ratio 1,4:1, alle drei Bänder **Range an bei 8 dB**, Auto Release an, Character VCA, Stereo Link 80 %.
Glue Master: alle drei Bänder Ratio ~1,5–1,6:1, Release 300 ms (lang, einheitlich), Character VCA, Stereo Link 100 %, High Limiter an bei −1 dB, Lookahead aktiviert, Mix 90 %.

Das Mid Band von Density Glue läuft *unter* 1:1 — Upward Compression, die Content über dem Threshold anhebt statt zu kappen —, gedeckelt durch Range bei 8 dB, damit die Anhebung nie davonläuft. Glue Master stützt sich stattdessen auf lange, einheitliche Releases und vollen Stereo-Link über alle drei Bänder für ein kohäsives, verklebtes Gefühl statt Per-Band-Charakterunterschieden.

### Peak-Kontrolle bei transientenreichem Material — *Peak Control*, *Hard Limiter Ceiling*

Peak Control: Low Threshold −10 dB/Ratio 5:1, Mid/High Threshold −8 dB/Ratio 4:1, **Knee 15 %** (eng — reagiert nah am Threshold), Attack schnell auf allen Bändern.
Hard Limiter Ceiling: High Ratio **8:1, Knee 0 %** (harter Knee), **High Limiter an**, Lookahead aktiviert.

Das High Band von Hard Limiter Ceiling kombiniert ein aggressives Kompressor-Ratio mit aktiviertem Brickwall-Limiter — der Kompressor übernimmt den generellen Pegel, der Limiter (der bei aktiviertem Lookahead wirklich overshoot-sicher wird) fängt die scharfen Becken-/Obertöne-Peaks, die ein musikalisch eingestellter Kompressor-Attack sonst durchließe.

### Low-End-Kontrolle unter einer Gitarrenwand — *Low-End Tighten*

Low Threshold −20 dB/**Ratio 3,5:1**, Mid/High Ratio 1,2:1 (vergleichsweise sanft), Attack 30 ms (langsam — erhält den Low-Frequency-Transientenpunch).

Nur das Low Band bekommt hier eine aggressive Behandlung — Mid und High bleiben nah an transparent, das Setting für Fälle, in denen speziell das Low End (nicht die ganze Mischung) unter einem dichten Arrangement gezügelt werden muss.

### Mastering-Sicherheitsnetz — *Mastering Safety Ceiling*

Alle drei Bänder Ratio 1,3:1 (sanft, einheitlich), **Detector RMS**, Stereo Link 100 %, High Limiter an bei −3 dB, Lookahead aktiviert.

Sanfte, einheitliche Ratios über alle drei Bänder plus eine Brickwall-Ceiling am High Band ist ein „kaum spürbar, bis etwas gefangen werden muss"-Mastering-Stage-Setting — RMS-Detection und voller Stereo-Link halten das Bild stabil und die Reaktion glatt, statt Transienten hinterherzujagen.

### Parallele Density — *Parallel-Style Density*

Alle drei Bänder **Ratio 0,6:1 (upward)**, Range an bei 10 dB, Output +1,5 dB.

Alle drei Bänder gleichzeitig mit Upward Compression, jedes auf ein vernünftiges Maximum range-begrenzt, fügt durchweg Dichte/Anhebung hinzu — eine Multiband-Alternative zum Beimischen eines stark komprimierten Parallel-Busses, ohne separaten Send.

## Rezepte

1. **Die richtigen Crossover-Punkte finden, bevor ein einziger Kompressor angefasst wird.** Jedes Band nacheinander solo schalten (Mute/Solo-Sektion), um genau zu hören, welcher Content wo landet, Low/Mid Split und Mid/High Split anpassen, bis nichts Unerwartetes überkreuzt (z. B. Kick-Klick oder Palm-Mute-Pick-Attack, das ins Low Band leckt). *Warum:* Ein falsch gesetzter Crossover-Punkt macht alles Nachgelagerte unvorhersehbar — dass das Low Band auf Content komprimiert, der eigentlich Mids Problem hätte sein sollen, ist ein Crossover-Problem, kein Threshold-Problem, und keine Kompressor-Feinjustage behebt das.

2. **Upward Compression ohne davonlaufende Anhebung.** **Range** aktivieren, bevor das Ratio eines Bands unter 1:1 gedreht wird. *Warum:* Unter 1:1 hebt dieselbe Kurve an, statt zu kappen, und diese Anhebung hat kein eigenes Limit — je weiter das Signal über dem Threshold liegt, desto mehr wird angehoben. Range deckelt die maximale Gain-Änderung (Cut oder Boost), damit ein aggressives Upward-Setting musikalisch nutzbar bleibt, statt das Limit erst nach Gehör zu entdecken, wenn es schon zu spät ist.

3. **Ein wanderndes Stereobild reparieren.** **Stereo Link** auf 60–100 % anheben am Band, das die Mischung aus der Mitte zieht. *Warum:* Bei 0 % (das einzige Verhalten jeder früheren Version) läuft jeder Kanal-Detektor vollständig unabhängig, sodass eine hart gepannte Transiente nur diese Seite runterziehen und das Bild verschieben kann. Voller Link zwingt beide Kanäle auf dieselbe Gain; teilweiser Link behält etwas Per-Seite-Reaktionsfähigkeit, während das Bild größtenteils fixiert bleibt.

4. **Zu Auto Release greifen, bevor ein langsamerer Release-Regler gezogen wird.** **Auto Rel** aktivieren, statt Release einfach hochzuziehen, wenn ein Band bei anhaltendem Material pumpt. *Warum:* Ein fest langsamer Release stoppt das Pumpen, macht das Band aber auch träge bei Transienten. Auto Release lässt eine schnelle Konstante und ein langsames Reservoir parallel laufen und nimmt, was höher ist — schnelle Erholung von einem kurzen Peak, ein mehrsekündiger Tail nur, wenn das Band wirklich anhaltend hart arbeitet.

5. **Per-Band-Sidechain-Thresholds nach Gehör statt Vermutung setzen.** **SC Listen** auf das Band schalten, das getriggert wird, Threshold nach dem tatsächlich Gehörten setzen, dann SC Listen wieder aus. *Warum:* SC Listen spielt das Key-Signal des Detektors, nicht das prozessierte Audio des Bands — genau das Signal, auf das sich ein Threshold bezieht, was aus dem prozessierten Output allein nach Gehör kaum korrekt zu beurteilen ist.

> **Theorie — warum ein VCA-Character-Detektor den Knee anders rundet als eine reine Ratio-Kurve.** Jede frühere Version von Triptychs Kompressor war rein feed-forward: Der Detektor liest den Input, und der Gain-Computer wendet eine feste Ratio-/Knee-Kurve an, ohne Erinnerung an den eigenen Zustand. Die VCA-Character-Option approximiert stattdessen statisch, was ein echter Feedback-Topologie-Kompressor tut — die Art, bei der der Detektor den *Output* der Gain-Zelle liest, einen Schritt versetzt, was die interne Schleife eines Hardware-Bus-Kompressors tatsächlich macht. Diese Feedback-Beziehung rundet den Knee um einen ratio-abhängigen Betrag (mehr Rundung bei sanfteren Ratios, weniger bei aggressiven) und lässt den effektiven Attack schneller werden, je höher das Ratio steigt — rein als Konsequenz des Gains der Schleife selbst, nicht weil eines von beidem separat programmiert wurde. Diese Option fügt bewusst keine zusätzliche Distortion oder harmonische Stufe hinzu: Der Charakterunterschied lebt vollständig im Envelope-Verhalten, wo das Gefühl eines Kompressors tatsächlich herkommt, bevor überhaupt Sättigung obendrauf kommt.

## Fallstricke

- **Der Drei-Band-Crossover-Baum ist magnitude-flach, aber nicht phasen-flach**, bei jedem Slope-Setting. Das zählt nur, wenn Triptychs Output gegen eine trockene Kopie desselben Signals gemischt wird (auch über **Mix**) oder mit einem phasen-bewussten Analyzer gemessen wird — nicht davon ausgehen, dass 50 % Mix bei einem Minimum-Phase-Multiband-Baum wörtlich „die Hälfte des Effekts" ist; nach Gehör gehen.
- **Vier Regler sind gestuft, nicht kontinuierlich, und können bei Änderung während der Wiedergabe klicken**: Slope (setzt die Crossover-Filter zurück), M/S On, Limiter-Enable bei aktiviertem Lookahead, und Lookahead selbst (verhandelt die Host-Delay-Kompensation neu). Jeder andere Regler ist konstruktionsbedingt vollständig klickfrei.
- **Die Knee-Rundung des VCA-Characters wird innerhalb von etwa 3 dB zu einem 0-dB-Threshold unerreichbar** — die erreichte Breite verengt sich sanft Richtung harter Knee, je näher der Threshold an 0 dB kommt. Nichts verhält sich numerisch fehlerhaft, aber für die volle VCA-Rundung Threshold bei −3 dB oder darunter halten (wo der Threshold eines Multiband-Kompressors ohnehin normalerweise sitzt).
- **Mid/Side pro Band beeinflusst nur die Verarbeitung der Side-(Breite-)Komponente** — da L+R nach dem Decode nur von Mid abhängt, kann keine Menge an Side-Processing eine Phasenauslöschung im Mono-Downmix verursachen. Nur eine Änderung der eigenen Settings der Mid-Komponente ändert die Mono-Summe, der beabsichtigte, hörbare Effekt beim Komprimieren der Mitte.
- **Der Spektrum-auf-Kurve-Analyzer ist noch nicht in diesem Release** — nur die drei Per-Band-Gain-Reduction-Balken. Ein Frequenzbereichs-Overlay ist für den späteren Custom-GUI-Meilenstein vorgesehen.
- **Das Voicing ist durchgehend aus veröffentlichten Hersteller-Handbüchern und Mastering-Technik-Artikeln für diese Referenzklasse abgeleitet, nicht gegen Referenz-Hardware gemessen.**
- **Ein Gate-Range-Floor, Per-Band-Sidechain-EQ, Per-Band-Dry/Wet-Mix und sample-genaue Parameter-Interpolation (heutiges Smoothing löst über einen 50-ms-Timer auf) sind alle auf ein späteres Release verschoben.**
