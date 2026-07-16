<!-- German translation of lancet.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

# Lancet — Bedienungsanleitung

*Schneide, wo es zählt — ein chirurgischer Dynamic EQ mit analoger Seele.*

## Was es ist

Lancet ist ein Six-Band Dynamic EQ im Geiste der Waves-F6-Klasse: Jedes Band ist ein normales parametrisches EQ-Band (Bell, oder Shelf bei Band 1/Band 6), dessen Gain sich zusätzlich mit dem Programmmaterial bewegen kann. Fütterst du es laut, reagiert es — schneidet eine Resonanz nur, wenn sie aufflammt, oder öffnet einen Boost nur, wenn ein Part untergeht — und pendelt sich dann wieder auf seine statische Einstellung ein, sobald der Pegel wieder fällt. Da die dynamische Bewegung jedes Bands von seinem *eigenen*, vor dem EQ sitzenden, bandgefilterten Detector angetrieben wird, verwirrt der Cut eines Bands nie den Detector eines anderen, und die eigene Gain-Bewegung eines Bands beeinflusst nie seine eigene Erkennung.

Wo ein statisches EQ-Band nur „wie viel?" fragt, fragen Lancets dynamische Bänder zusätzlich „wann?" — der Unterschied zwischen einer dauerhaft ausgekerbten 3-kHz-Resonanz (die den Ton auch dann ausdünnt, wenn diese Resonanz gar nicht vorhanden ist) und einem Zurückziehen genau dann, wenn sie klingelt.

## Wo es in einer Mix-Kette sitzt

Lancet ist ein **korrigierendes, chirurgisches Werkzeug**, am nützlichsten früh bis mittig in der Signalkette, vor breiter Klangformung und Bus-Kompression:

```
Source track -> [gain staging / gate] -> Lancet (resonance/harshness control) -> broad EQ / saturation -> compression -> bus
```

Greife danach, wenn ein statischer EQ-Cut das Problem entweder unterbehandeln würde (sodass es bei den lautesten Treffern trotzdem noch durchsticht) oder überbehandeln würde (und den Ton in leiseren Passagen ausdünnt, in denen das Problem gar nicht vorhanden ist). Es funktioniert auch als Mix-Bus- oder Master-Bus-Werkzeug, um eine bestimmte wiederkehrende Resonanz oder ein hartes Frequenzband zu kontrollieren, ohne alles darunter dauerhaft einzufärben.

## Signalfluss

```
in --[Input Trim]--+--[pre-chain tap]--> each band's Detector (bandpass @ band freq/Q -> envelope)
                    |
                    +--> Band1 -> Band2 -> Band3 -> Band4 -> Band5 -> Band6 --> [Mix] --> [Output Trim] --> out
```

Der Detector jedes Bands zapft das Signal direkt nach Input Trim an, *vor* Band 1 — nicht den seriell bereits verarbeiteten Input dieses Bands selbst —, sodass die Gain-Bewegung eines nachgelagerten Bands nie die Erkennung eines vorgelagerten Bands stört und die eigene Bewegung eines Bands nie ihre eigene Auslösung zurückfüttert. Die vollständige technische Aufschlüsselung (Gain-Computer-Formel, Detector-Selektivität, Sub-Block-Koeffizienten-Smoothing, Listen) findest du in [`docs/architecture.md`](architecture.md).

## Parameter-Referenz

### Je Band (Band 1 – Band 6, identische Regler sofern nicht anders angegeben)

| Parameter | Range | Default | Unit | Was es musikalisch bewirkt |
|---|---|---|---|---|
| **On** | Off / On | Off (Band 3: On) | | Aktiviert das Band. Ein ausgeschaltetes Band ist ein echter Bypass — es rührt das Signal überhaupt nicht an, auch wenn sein Detector darunter weiterläuft, damit es beim Wiedereinschalten keinen Sprung gibt. |
| **Type** | Bell / Shelf | Bell | | **Nur Band 1 und Band 6.** Der Shelf von Band 1 ist ein Low Shelf (hebt/senkt alles unterhalb von Freq); der Shelf von Band 6 ist ein High Shelf (hebt/senkt alles oberhalb von Freq). Band 2–5 sind immer Bell. |
| **Freq** | 20 - 20000 | 100 / 250 / 630 / 1600 / 4000 / 10000 | Hz | Die Mittenfrequenz des Bands (Bell) oder die Eckfrequenz (Shelf) — sowohl die Form des Filters selbst *als auch* das, worauf sein Detector hört. |
| **Q** | 0.3 - 12 | 1.0 | | Wie schmal (hohes Q) oder breit (niedriges Q) das Band ist. **Wird im Shelf-Modus ignoriert**, der unabhängig von dieser Einstellung immer eine feste, standardmäßige Shelf-Flanke nutzt (Q = 0.707). |
| **Gain** | -12 - +12 | 0 | dB | Das *statische* Gain des Bands — immer angewendet, dynamisch oder nicht. Setze das auf deine „Ruhe"-EQ-Bewegung; Range addiert oder subtrahiert dann obendrauf, wenn der Detector auslöst. |
| **Range** | -12 - +12 | 0 | dB | Wie weit sich das Gain des Bands dynamisch bewegen kann, zusätzlich zu Gain. **0 = ein rein statisches EQ-Band** (kein Detector-Einfluss). Negatives Range schneidet, wenn das Signal lauter als Threshold wird (die klassische Resonanz-Zähmung/De-Essing-Bewegung); positives Range boostet, wenn es lauter wird (eine aufwärtsgerichtete „Duck-in"-Expansions-Bewegung, nützlich z. B. um Anschlag nur bei hart gespielten Noten hervorzuheben). |
| **Thresh** | -60 - 0 | -30 | dB | Der Detector-Pegel, ab dem die dynamische Bewegung einsetzt. Ein 6-dB-Soft-Knee ist um diesen Wert zentriert, sodass der Übergang graduell statt ein harter Schalter ist. |
| **Attack** | 0.5 - 100 | 5 | ms | Wie schnell sich das dynamische Gain bewegt, sobald der Detector den Threshold überschreitet. Schneller Attack erwischt Transienten hart; langsamerer Attack lässt einen kurzen Peak durch, bevor reagiert wird, was bei perkussivem Material natürlicher klingen kann. |
| **Release** | 10 - 1000 | 150 | ms | Wie schnell das dynamische Gain zurück Richtung Gain kehrt, sobald der Detector wieder unter den Threshold fällt. Schneller Release kann bei anhaltendem Material hörbar pumpen; langsamer Release glättet die Rückkehr, kann aber einen Cut/Boost in Inhalt hineinhalten, der ihn nicht mehr braucht. |
| **Listen** | Off / On | Off | | Solot das eigene Detector-Signal dieses Bands — das bandpassgefilterte Audio vor dem EQ, das tatsächlich seine dynamische Bewegung antreibt — anstelle des normalen Programm-Outputs, um genau zu hören, was es auslöst. Exklusiv: Aktivierst du Listen bei einem Band, deaktiviert das automatisch Listen bei jedem anderen Band. Die vollständige Signalkette (inklusive der Verarbeitung jedes einzelnen Bands) läuft darunter weiter, sodass das Deaktivieren von Listen nie knackt. |

### Global

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Input Trim** | -12 - +12 | 0 | dB | Gain, das vor Band 1 angewendet wird — und bevor der Detector jedes Bands das Signal anzapft, verschiebt es also auch, welcher Pegel den Threshold jedes Bands erreicht. |
| **Output Trim** | -12 - +12 | 0 | dB | Gain, das nach Band 6 und nach der Mix-Blende angewendet wird — die finale Gain-Stufe, um den Ausgangspegel von Lancet an das anzupassen, was als Nächstes in der Kette folgt. |
| **Mix** | 0 - 100 | 100 | % | Paralleler Dry/Wet-Blend der gesamten Six-Band-Kette. 100 % ist vollständig prozessiert; niedrigere Werte mischen zunehmend mehr vom unbearbeiteten (aber weiterhin Input-getrimmten) Signal bei — nützlich für „New-York"-artiges paralleles Dynamic EQing, bei dem die Korrektur hinzufügen statt vollständig ersetzen soll. |

## Tipps

- **Setze Gain und Range getrennt und bewusst.** Gain ist das, was das Band *immer* tut; Range ist das, was es *zusätzlich* tut, nur wenn ausgelöst. Ein Band mit Gain=0, Range=-6 ist in Ruhe unhörbar und schneidet nur, wenn die Resonanz aufflammt — ganz anders als Gain=-3, Range=-3, das immer ein bisschen schneidet und bei Auslösung noch härter schneidet.
- **Nutze Listen, um das Problem zu finden, bevor du Threshold setzt.** Fahre Freq/Q mit aktiviertem Listen durch, bis du die Resonanz oder Härte klar isoliert hörst, *dann* setze Threshold knapp über den Pegel, den sie hat, wenn sie kein Problem ist — das ist deutlich zuverlässiger, als einen Threshold-Wert gegen den vollen Mix zu erraten.
- **Schmale, high-Q-Bänder mit negativem Range sind das klassische Resonanz-Zähmungs-Setup** (ein dumpfer 300–500-Hz-Aufbau, eine harte 2–4-kHz-Plektrum-/Rohrblatt-Kante, ein sibilantes 6–8-kHz-De-Esser-Band). Halte Q hoch genug, dass der Cut den umgebenden Ton nicht hörbar ausdünnt, wenn er einsetzt.
- **Breite, low-Q-Bänder mit negativem Range ergeben eine sanftere, breitere dynamische Klangkontrolle** — nützlich auf einem Mix-Bus, um ein ganzes Register zu zähmen (z. B. „die Low-Mids werden etwas zu viel, wann immer die ganze Band gemeinsam zuschlägt"), ohne die chirurgische Enge eines De-Esser-artigen Bands.
- **Positives Range (aufwärts/Duck-in) ist die weniger naheliegende Bewegung** — probiere es auf einem low-Q-Hochfrequenzband, um Anschlag oder Atem-/Konsonanten-Details nur bei den Noten hervorzuholen, die es brauchen, statt ständig das ganze Register (und seinen Rauschteppich) zu boosten.
- **Schneller Attack + schneller Release können bei anhaltendem Material hörbar pumpen** (Bass, Flächen, gehaltene Vocal-Noten) — klingt ein Band instabil oder „atmend", versuche zuerst einen langsameren Release, bevor du zu einem schmaleren Q greifst.
- **Mix unter 100 % erhält den Charakter der dynamischen Bewegung, während ihre Tiefe reduziert wird** — ein schneller Weg, eine übertrieben aggressive Range-Einstellung zurückzunehmen, ohne Threshold/Range jedes Bands von Grund auf neu einzustellen.
