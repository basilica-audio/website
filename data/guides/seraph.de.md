# Seraph — Praxis-Guide

*Praxisnahe Einstellungen für den Chor- & Vocal-Prozessor, verankert in den Werkspresets.*

## Wo es hingehört

Seraph läuft auf Vocal-/Chor-Spuren oder einem Vocal-Bus als vollständiger Channel-Strip (De-Ess → Air → Comp → Doubler → Output), typischerweise:

```
Vocal-/Chor-Aufnahme → (Tuning/Editing, falls genutzt) → Seraph → Reverb-/Delay-Send → Mix-Bus
```

In der Default-Konfiguration meldet Seraph **0 Samples Latenz**, ist also sicher überall in einer Vocal-Kette einsetzbar, auch parallel — nur der Shift-Doubler-Modus und De-Ess Lookahead ändern das, bewusst und nicht automatisierbar.

## Quick-Start-Einstellungen

### Lead-Vocal, schneidet durch eine dichte Mischung — *Lead - Cut Through*

De-Ess 35 %/7500 Hz, **Air +5 dB**, Comp 25 %, Double 15 %/Detune 8¢/Width 60 %.

Ein Hauch Air über dem natürlichen Top-End des Vocals plus ein subtiles (15 %) Double ist die Kombination für ein Lead, das durch verzerrte Gitarren und orchestrale Strings schneiden muss, ohne künstlich doubliert oder überprozessiert zu wirken.

### Intimes, nah abgenommenes Lead — *Lead - Intimate/Close-Mic*

De-Ess 45 %/6500 Hz/Width 55 % (stärker — Close-Miking bringt mehr Sibilanz hoch), **Air +1 dB** (zurückhaltend), Comp 15 %, Double 8 % (kaum vorhanden).

Stärkeres De-Essing gepaart mit minimalem Air und Double hält einen nah abgenommenen Take intim, statt ihn Richtung eines „produzierten" Lead-Vocal-Sounds zu drücken — das Gegenteil der Balance von Cut Throughs hellerem, prozessierterem Ansatz.

### Chor-/Backing-Spread — *Choir - Sacred Shift*, *Choir - Wide Spread*

Choir - Sacred Shift: Double **60 %**, Detune 14¢, Width 100 %, **Double Mode Shift**, Humanize 35 %.
Choir - Wide Spread: Double 55 %, Detune 18¢, Width 100 %, Double Mode Classic.

Sacred Shift greift zur Shift-Engine (spektrales Pitch-Shifting, ~30 ms Latenz, das sauberste Doubling) kombiniert mit starkem Humanize für einen breiten, dekorrelierten Chor-Spread aus weniger aufgenommenen Takes — Settings, die ein Lead-Vocal selten will, aber genau das, wovon eine kleinere Chor-Sektion profitiert.

### Vintage-Micro-Detune-Doubler — *Doubler - Vintage Micro*

**Double Mode Micro**, Double 70 %, Detune 12¢, Width 100 %, Comp 0 %.

Micro hält ein wirklich konstantes Intervall (auf deutlich unter ein Cent genau), statt Classics langsamem Wobble — bewusst dazu greifen, wenn ein Double ein Intervall halten soll, statt zu chorusen, und beachten, dass es zeitlich weiter hinten sitzt als Classic (34–49 ms vs. 9–24 ms) — ein bewusster Charakterunterschied, kein Fehler.

### Gesprochenes/gegrowltes Zwischenspiel — *Spoken/Growled Interlude*

**De-Ess 5 %** (minimal — wenig Sibilanz-Energie in einer gegrowlten Performance), Air +4 dB, **Comp 55 %** (stärker — hält eine gesprochene Passage pegel-konsistent), Double 5 %/Width 20 % (schmal, zentriert).

Gegrowltes oder gesprochenes Material braucht typischerweise die entgegengesetzte De-Essing-Behandlung eines gesungenen Leads, und ein stärkeres Comp-Setting, um gegen einen leisen orchestralen Backing-Track präsent und konsistent zu bleiben.

### Nur chirurgisches De-Essing / nur Glue — *De-Ess Only (Surgical)*, *Glue Only*

De-Ess Only: De-Ess 50 %, alles andere bei 0/Bypass.
Glue Only: Comp 50 %, alles andere bei 0/Bypass.

Beide isolieren eine Sektion des Channel-Strips vollständig — legitime, unterstützte Konfigurationen für Fälle, in denen auf einer bestimmten Spur nur eine Stufe von Seraphs Processing gebraucht wird.

## Rezepte

1. **Eine Doubler-Engine nach Materialbedarf wählen, nicht aus Gewohnheit.** Zu **Classic** greifen (der Default, keine Latenz) für das vertraute wobble-basierte Double; zu **Micro**, wenn ein Stack ein echtes Intervall halten muss, ohne wie Chorus zu klingen; zu **Shift** (30 ms Latenz), wenn Detune Richtung Obergrenze gedreht wird und das sauberste, akkurateste Ergebnis gewollt ist. *Warum:* Alle drei teilen sich dieselben vier Stimmen und Pan-/Detune-/Width-Gesetze — der Wechsel ändert nur, wie der Detune erzeugt wird, die Wahl geht also rein darum, welcher Detune-Mechanismus zum Material passt, nicht darum, andere Regler zu verlieren oder zu gewinnen.

2. **Einen De-Esser reparieren, der auf den falschen Sound reagiert.** Erst **De-Ess Width** versuchen, bevor **De-Ess Freq** bewegt wird — Width verengen, falls „sh"-/hauchiger Content erwischt wird, verbreitern, falls ein Teil des tatsächlichen „s" fehlt. *Warum:* Width steuert direkt die Detection-Bandbreite, ist also der chirurgischere erste Move als die Mittenfrequenz zu verschieben, was auf völlig anderen Content abdriften kann.

3. **Verhindern, dass ein „S" das Stereobild zur Seite schiebt.** **De-Ess Link** (und **Comp Link**) auf jedem stereo Vocal-Bus aktivieren — ein doubliertes oder gespreiztes Chor, ein Stereo-Raum-Take. *Warum:* Ungelinkt wird jeder Kanal von seinem eigenen Detektor prozessiert, sodass ein lauter Moment oder ein starkes „S" auf nur einer Seite genau diese Seite runterziehen und das Bild verschieben kann; beide Link-Optionen erzwingen einen gemeinsamen Detektor über die Kanäle, speziell um das zu verhindern.

4. **Die maschinelle Qualität aus einem doublierten Stack entfernen.** **Humanize** auf 20–40 % anheben, statt mehr Double oder mehr Detune. *Warum:* Vier Stimmen mit exaktem, festem Detune sind immer noch vier mathematisch verwandte Kopien einer Performance — Humanize fügt jeder Stimme unabhängigen, deterministischen Drift (Timing, Pitch, Level) hinzu, das, was echte Sänger tun, ohne sich abzustimmen, und ist meist der tatsächliche Unterschied zwischen einem Doubler, den man bemerkt, und einem, den man nicht bemerkt.

5. **Offenheit hinzufügen, ohne die gerade entfernte Sibilanz wieder einzufüttern.** **Air Freq auf 15 kHz** setzen, wenn De-Essing stärker eingestellt ist. *Warum:* 15 kHz bleibt komplett außerhalb des Sibilanz-Bereichs, den der De-Esser anvisiert, sodass Air dort anzuheben Höhen-Glanz hinzufügt, ohne auch die gerade reduzierte „S"-Energie wieder anzuheben — 10/12 kHz reichen weiter runter in den Presence-/Sibilanz-Bereich und passen besser zu leichterem De-Essing.

> **Theorie — warum De-Esser-Lookahead das erkannte Band verzögern muss, nicht nur das Audio.** Ein De-Esser reduziert Sibilanz, indem er eine skalierte, invertierte Kopie des erkannten Sibilanz-Bands zurück aufs Signal addiert — das funktioniert nur als Auslöschung, wenn beide Kopien präzise zeitlich ausgerichtet sind. Die verlockend einfachere Implementierung verzögert nur den Audio-Pfad und lässt den Detektor auf dem *unverzögerten* Input laufen, was harmlos wirkt, bis man bedenkt, was Sibilanz eigentlich ist: effektiv rauschartiger, dekorrelierter Content. Schon bei einer Fehlausrichtung von 2 ms zwischen verzögertem Audio und unverzögertem Detection-Signal löscht das Subtrahieren zweier dekorrelierter, rauschartiger Signale nicht aus — es addiert bei maximaler Reduktion etwa das 0,8-Fache der Band-Leistung wieder hinzu, sodass ein so konfigurierter „De-Esser" bei höheren Lookahead-Settings „S"-Laute messbar verstärken statt reduzieren würde. Seraph vermeidet das, indem es Audio und erkanntes Band gemeinsam verzögert, die Detection auf der unverzögerten Kopie laufen lässt und die resultierende Gain durch ein Sliding-Minimum-Fenster schickt, sodass die Korrektur schon steht, bevor das verzögerte „S" eintrifft — präzise zeitliche Ausrichtung ist hier kein Nice-to-have, sondern der gesamte Mechanismus, der Lookahead-De-Essing überhaupt funktionieren lässt, statt sich falsch zu verhalten.

## Fallstricke

- **Double Mode und De-Ess Lookahead sind konstruktionsbedingt nicht automatisierbar.** Beide ändern Seraphs gemeldete Latenz, und Hosts kommen schlecht mit einer Latenzänderung mitten in einer Automation klar — Modi während laufender Wiedergabe wechseln geht (ein kurzer Fade kaschiert das), aber keins von beiden in eine Automations-Spur zeichnen.
- **Micros Stimmen sitzen 34–49 ms hinter dem trockenen Signal**, weiter hinten als Classics 9–24 ms, weil der Pitch-Shift durch kontinuierliches Verschieben des Delays erzeugt wird — ein bewusster Charakterunterschied (slappier, breiter wirkend), kein Bug. Wenn die doublierten Stimmen eng am trockenen Signal sitzen sollen, stattdessen Classic nutzen.
- **Formant Preserve tut nur im Shift-Modus etwas.** Classic und Micro resamplen das Spektrum nie, es gibt in diesen Modi also nichts für die Formant-Erhaltung zu korrigieren.
- **De-Ess' Detection-Threshold ist fest und absolut, nicht pegel-relativ.** Ein sehr leiser Take braucht eventuell zuerst Gain-Staging, bevor De-Ess sinnvoll reagiert — das ist kein adaptiver/Auto-Threshold-Detektor.
- **Comp ist ein Glue-Regler, kein Leveling-Tool.** Sein sanftes 3:1-Maximalratio soll Konsistenz auf einem bereits einigermaßen pegel-konstanten Take hinzufügen; wild inkonsistente Strophen-/Refrain-Pegel zuerst mit Clip Gain oder einem dedizierten Leveling-Kompressor vorgelagert beheben.
- **Bei mono-sensiblem Material auf Double Width achten.** Falls die Mischung auf Mono gefaltet werden könnte (Streaming, manche Broadcast-Ketten), den Doubler mit Width Richtung 0 % prüfen, um sicherzugehen, dass sich die doublierten Stimmen bei der Summierung nicht unangenehm auslöschen.
- **Die GUI ist ein funktionaler Slider-/Knopf-Editor; eine individuelle vektorgezeichnete GUI folgt als späterer Meilenstein**, und Detune ist konstruktionsbedingt in jedem Modus auf ±50 Cent gedeckelt — größere Intervalle brauchen Per-Voice-Kontrolle und ein Harmonizer-Interface, ein separates Feature statt einer größeren Zahl an diesem Regler.
- **Falls ein Host Seraph jemals nicht-finites Audio (NaN/Inf) von einem sich falsch verhaltenden vorgeschalteten Plugin zuspielt**, ist ein Transport-Stop/Start oder erneutes Öffnen des Plugins (was einen Host-Reset triggert) der verlässliche Weg, das zu bereinigen — die vendorierte Engine des Shift-Modus erholt sich speziell nicht allein von ihrem eigenen internen Reset.
