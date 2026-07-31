# Lancet — Praxis-Guide

*Praxisnahe Einstellungen für die 6-Band-Dynamic-EQ, verankert in den Werkspresets.*

## Wo es hingehört

Lancet ist ein korrektives, chirurgisches Tool, am nützlichsten früh bis mittig in der Signalkette, vor breitem Tonal-Shaping und Bus-Kompression:

```
Quellspur → [Gain-Staging/Gate] → Lancet (Resonanz-/Härte-Kontrolle) → breite EQ/Sättigung → Kompression → Bus
```

Greif danach, wenn ein statischer EQ-Cut ein Problem entweder unterbehandelt (lässt Raum, bei den lautesten Treffern durchzuschlagen) oder überbehandelt (dünnt den Ton in leiseren Passagen aus, wo das Problem nicht vorliegt). Es funktioniert auch als Mix-Bus- oder Master-Bus-Tool, um eine bestimmte wiederkehrende Resonanz oder Härte-Band zu kontrollieren, ohne alles darunter dauerhaft einzufärben.

## Quick-Start-Einstellungen

### Eine brustige Low-Mid-Resonanz zähmen — *Chest Resonance Tamer*

Band 1 (Low Shelf) bei 220 Hz, Threshold −28 dB, **Range −5 dB**, Attack 20 ms, Release 180 ms.

Negatives Range ist der klassische Resonanz-Zähm-Move: Die Gain wird gekappt, *je lauter das Signal* über den Threshold wird, sodass die Korrektur nur eingreift, wenn die Resonanz tatsächlich hörbar ist — eine leise Passage, in der dieselbe Frequenz kein Problem ist, bleibt unangetastet, anders als ein statischer EQ-Cut, der immer da wäre.

### De-Essing-/Härte-Stack — *De-Ess Stack*

Band 5 bei 6500 Hz, Q 2,0 (eng), Threshold −24 dB, **Range −8 dB**, Attack 0,5 ms (schnell), Release 60 ms, **Auto Release an**. Band 6 (High Shelf) bei 9000 Hz, Range +1,5 dB, Attack 5 ms.

Zwei Bänder arbeiten zusammen: Band 5 zieht Sibilanz hart und schnell runter, Band 6 fügt oberhalb des de-essten Bereichs etwas Air zurück hinzu — ein üblicher Move, damit ein stark de-esstes Vocal nicht gedämpft wirkt.

### Sanfter Glue auf einem Bus — *Gentle Glue*

Band 2 bei 250 Hz und Band 4 bei 2500 Hz, beide **Range −4 dB**, Attack 10 ms, Release 100 ms.

Zwei Bänder mit angeglichenen, moderaten Settings statt eines hart angeschobenen Bands — ein breites, sanftes dynamisches Straffen über zwei problemanfällige Bereiche (Box-Resonanz und Presence) statt einer einzelnen aggressiven Korrektur an einer Stelle.

### Analoge Wärme-Anhebung mit Sättigung — *Analog Warmth Lift*

Band 2 bei 250 Hz, Gain +2 dB (statische Anhebung) mit **Range +3 dB** (upward — hebt weiter an, je höher der Pegel), **Saturation an**.

Saturation greift nur, während das Band aktiv anhebt — Gain plus der dynamische Beitrag netto positiv —, sodass ein cuttendes oder untätiges Band selbst mit aktiviertem Saturation unbeeinflusst bleibt. Kombiniert mit positivem Range bekommen lautere Passagen zunehmend mehr Low-Mid-Anhebung und zunehmend mehr Soft-Drive-Charakter.

### Sidechain-getriggertes Carving — *Sidechain Carve*

Band 3 bei 400 Hz, **SC Source External, SC Mode Wide**, Range −6 dB, Threshold −26 dB.

External Sidechain routet etwas anderes in den Sidechain-Eingang des Hosts, um den Move dieses Bands zu triggern statt das Signal selbst; Wide-Modus bedeutet, der Detektor reagiert auf den Gesamtpegel über das ganze Spektrum statt nur auf den 400-Hz-Bereich, sodass das Band auf die generelle Präsenz der getriggerten Quelle duckt, nicht speziell auf deren Content nahe 400 Hz.

### Langsames Tonal-Riding auf einem Master — *Slow Tonal Ride*

Band 2, Q 0,5 (breit), Threshold −35 dB, Range −5 dB, **Attack 350 ms, Release 800 ms** (beide sehr langsam).

Die 500-ms-Attack-Obergrenze existiert speziell für langsame, musikalische Tonal-Balancing-Moves wie diesen, nicht zum Transienten-Fangen — das ist näher an einem automatisierten Fader-Ride auf einem Frequenzbereich als an einem korrektiven Dynamic-EQ-Move.

### Transiente Snare-Crack — *Transient Snare Crack*

Band 3 bei 3000 Hz, **Range +6 dB** (upward), Attack 0,1 ms (schnellstmöglich), Release 40 ms, Auto Release an.

Positives Range mit sehr schnellem Attack ist der Upward-„Duck-in"-Expansion-Move — er hebt speziell den Crack-/Attack-Transienten bei harten Treffern hervor, statt statisch 3 kHz auf allem anzuheben, inklusive Ghost Notes und Übersprechen.

## Rezepte

1. **Genau herausfinden, was ein Problem-Band triggert, bevor Threshold gesetzt wird.** **Listen** am fraglichen Band aktivieren, Freq/Q durchfahren, bis die Resonanz oder Härte klar isoliert zu hören ist, *dann* Threshold knapp über den Punkt setzen, an dem sie kein Problem ist. *Warum:* Das ist weit verlässlicher als einen Threshold-Wert gegen die volle Mischung zu erraten — Listen solot das eigene Detektor-Signal des Bands (das bandpass-gefilterte, Pre-EQ-Audio, das den Move tatsächlich antreibt), und die volle Signalkette läuft darunter weiter, sodass Listen auszuschalten nie knackt.

2. **Zwischen Split- und Wide-Sidechain-Modus wählen.** **Split** (der Default) nutzen, wenn ein Band nur auf Content nahe der eigenen Frequenz reagieren soll — das chirurgische, resonanzspezifische Verhalten; **Wide** nutzen, wenn ein Band mit dem Gesamtpegel des Programms mitatmen soll, statt eine bestimmte Resonanz zu überwachen. *Warum:* Split filtert den Detektor-Input auf den eigenen Bereich des Bands runter, bevor er den Detektor überhaupt erreicht; Wide überspringt diesen Filter komplett, sodass der Gain-Move des Bands weiterhin auf die eigene Frequenz beschränkt bleibt, aber was den Move *triggert*, ist der Pegel des gesamten Spektrums.

3. **Ein Band bei natürlich abklingendem Material schneller entspannen lassen, ohne anderswo einen langsameren Release zu verlieren.** **Auto Release** aktivieren, statt einfach den manuellen Release-Wert zu verkürzen. *Warum:* Auto Release verkürzt die *effektive* Release-Zeit automatisch, immer wenn das eigene Envelope des Signals ohnehin schon fällt — nie unter den 5-ms-Floor des Plugins, nie über das manuelle Release-Setting hinaus —, sodass anhaltendes Material weiterhin den langsameren, musikalischen Release bekommt, der eingestellt wurde, während natürlich abklingender Content eine Korrektur nicht bis in die Stille hält.

4. **Ein weicherer, analogerer Charakter bei tieferen dynamischen Moves.** **Gain/Q**-Kopplung auf einem Band mit signifikantem Range aktivieren. *Warum:* Gain/Q weitet (weicht) die eigene Filter-Q des Bands proportional dazu, wie weit seine *dynamische* Gain gerade Richtung Range steht — tiefere Moves bekommen automatisch sanftere, breitere Behandlung, während die statische Gain-Komponente Q nie beeinflusst, nur der dynamische Beitrag tut das.

5. **Parallele Dynamic EQ statt vollständigem Ersatz.** **Mix** von 100 % runterziehen, statt das Range jedes Bands einzeln zu reduzieren. *Warum:* Mix mischt die voll prozessierte Sechs-Band-Kette parallel gegen das unangetastete (aber weiterhin Input-getrimmte) Signal — ein „New-York"-artiger Move, bei dem die Korrektur zum Original hinzufügt, statt es voll zu ersetzen, nützlich, wenn der Effekt der Dynamic EQ gewollt ist, ohne dass sie das Einzige ist, das diesen Frequenzbereich formt.

> **Theorie — warum es keinen Ratio-Regler gibt.** Die meisten Dynamic EQs und Kompressoren bieten ein Ratio: Für jedes dB, das das Signal einen Threshold überschreitet, folgt ein Bruchteil eines dB Gain-Änderung. Lancet hat bewusst keins. Oberhalb des Knees bewegt sich die Gain 1:1 mit dem Ausmaß, in dem der Detektor den Threshold überschritten hat, bis Range erreicht ist — das dann als harte Obergrenze fungiert, wie weit der dynamische Move gehen kann. Range ist wirklich der „wie weit kann sich das bewegen"-Regler, kein Skalierungsfaktor obendrauf auf ein separates Ratio; der Knee, dessen Breite selbst mit Range skaliert, liefert die Rampe rein, statt eines harten Schalters. Das ist ein einfacheres Modell als das volle Ratio-/Knee-/Threshold-Dreieck eines Kompressors, und es ist der Grund, warum ein flaches Range-Setting als sanfter Übergang wirkt, während ein volles Range-Setting wie ein deutlich schärferer korrektiver Move klingt — die Knee-Breite hängt direkt daran, wie viel Weg zurückzulegen ist.

## Fallstricke

- **Q wird im Shelf-Modus ignoriert.** Band 1s Low Shelf und Band 6s High Shelf nutzen immer die Standard-flache-Shelf-Flanke (Q 0,707), sowohl für den hörbaren Filter als auch seinen passenden Detektor-Bandpass — Q an diesen beiden Bändern im Shelf-Typ zu bewegen hat keinen Effekt.
- **Auto Release, Gain/Q und Saturation haben noch keine eigenen Editor-Regler.** Alle drei sind vollständig automatisierbar und preset-steuerbar — über die generische Parameter-Ansicht des Hosts setzen oder automatisieren, bis der GUI-Pass kommt. (SC Source und SC Mode haben dagegen Editor-Regler, da ein Sidechain-Routing, das im Editor nicht auswählbar ist, gar nicht nutzbar wäre.)
- **Detection ist stereo-gelinkt ohne Unlink, und es gibt kein Per-Band-M/S oder L/R-Placement** — der Detektor jedes Bands sieht ein kombiniertes Signal aus beiden Kanälen.
- **Die Per-Band-Voicing-Defaults sind ingenieursmäßiges Urteil, nicht nach Gehör gegen Referenzmaterial getuned.** Die *Richtung* der Voicing-Tabelle (tiefe Frequenzen langsam und sanft, hohe Frequenzen schnell und chirurgisch) folgt etablierter Mixing-Konvention und ist von der Test-Suite gemessen/eingefroren, aber die exakten Zahlen — und die Saturation-Drive-Kurve — sind nicht gegen echtes Vocal-/Gitarren-/Mix-Material validiert oder gegen ein anderes Produkt kalibriert.
- **Für die Saturation-Stufe wird kein absoluter Alias-Floor angegeben.**
- **Noch nicht im Plugin, für spätere Releases getrackt**: Opt-in Spectral Resonance Suppression, Per-Band-M/S/L/R-Placement mit Stereo-Unlink, optionales HF-Decramping, breitere Range-/Q-/Release-Bereiche, Lookahead, Per-Band-Ratio, Linear Phase, mehr als sechs Bänder, und eine Spektrum-Analyzer-/EQ-Kurven-Anzeige.
- **Die GUI ist ein funktionaler Slider-/Toggle-/Combo-Editor** — eine individuelle vektorgezeichnete Oberfläche mit Per-Band-Gain-Reduction-Nadeln folgt als späterer Meilenstein; die zugrunde liegende Messung existiert schon und ist verifiziert, wird nur noch nicht angezeigt.
