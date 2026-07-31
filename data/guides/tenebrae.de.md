# Tenebrae — Praxis-Guide

*Praxisnahe Einstellungen für die Haupt-Gain-Stufe, verankert in den Werkspresets.*

## Wo es hingehört

Tenebrae ist die **Haupt-Gain-Stufe** der Gitarrenkette — die Wall of Gain, nicht der Lautsprecher. Es hat konstruktionsbedingt keine Cabinet-Simulation, bleibt also ein sauberer Baustein: einen Tightening-Boost (Overture o. Ä.) davor für Low-End-Kontrolle, einen Cab-Sim/IR-Loader (Nave) danach.

```
Gitarre → Noise Gate → Tight-Boost (optional) → Tenebrae (High-Gain-Distortion) → Cab-Sim/IR-Loader → Mix-Bus
```

Typische Anwendungsfälle: Rhythmus-Chug-Töne von modern-tight bis vintage-loose, Doom-/Sludge-Sag, und alles dazwischen über die Engine-Wahl Classic/Triode.

## Quick-Start-Einstellungen

### Modern-tighter Rhythmus — *Foundation Chug* / *Adaptive Gate Chug*

Foundation Chug: Tight 90 Hz, Gain 24 dB, Voicing Tight, alle Tone-Bänder flach, Gate an (Threshold −48 dB, Release 150 ms).
Adaptive Gate Chug (v0.3.0, Triode-Engine): Tight 110 Hz, Gain 28 dB, Tone Voice Scoop, Bias Shift 120 %, Gate Key Pre, Gate Release Mode Auto.

Foundation Chug ist der eigene „Init"-Kategorie-Ausgangspunkt des Plugins — flacher Tone-Stack, Gate standardmäßig an (Tenebrae liefert das Gate anders als jeder andere neue Regler bereits aktiv aus, weil die Recherche hinter dem Rework ein Gate als strukturellen Bestandteil eines tighten Chug-Tons in diesem Genre behandelt). Adaptive Gate Chug fügt den dynamischen Bias-Shift der Triode-Engine hinzu und schaltet das Gate auf **Pre**-Detection um — es triggert vom Signal, bevor es auf 28 dB Gain trifft, sodass leise Noten und Stille sauber getrennt bleiben.

### Sackender Doom/Sludge — *Sagging Doom*

Tight 60 Hz, Gain 22 dB, Voicing Loose, Bass +3 dB, Engine Triode, Power Amp an, Resonance 9 dB, **Sag 75 %**, Gate Release 400 ms.

Ein niedriges Tight-Setting hält das Low End voll und boomig statt tight — die entgegengesetzte Bewegung zu einem Rhythmus-Chug-Preset. So hoher Sag lässt die modellierte Stromversorgung hörbar durchsacken und sich über etwa 120 ms pro Anschlag erholen — das komprimierte, spongy Gefühl, das Doom-/Sludge-Parts wollen; Resonance drückt zusätzlich mehr Low End in den Feedback-Pfad der Power Amp.

### Heller, aggressiver Cut-Through-Rhythmus — *Bright Aggressive* / *Cut-Through Lead-Adjacent*

Bright Aggressive: Tight 110 Hz, Gain 32 dB, Bright an, Level −2 dB.
Cut-Through Lead-Adjacent: Tight 80 Hz, Gain 30 dB, Mid +2 dB, Treble +2 dB, Bright an, Tone Voice Boost.

Bright aktiviert einen festen Pre-Cascade-Höhenshelf, modelliert nach dem „Bright-Switch", den viele High-Gain-Kanäle haben — weil das angehobene Signal danach drei kaskadierte Clipping-Stufen durchläuft, ist der Effekt auf die Lautheit konstruktionsbedingt subtil; was sich ändert, ist der harmonische Gehalt und das Pick-Attack-Sizzle, das in die Kaskade einspeist, nicht der rohe Ausgangspegel.

### Vintage-/lockereres Voicing — *Loose & Open*, *Vintage Cascade*

Loose & Open: Tight 50 Hz, Gain 16 dB, Voicing Loose, Bass +3 dB, Treble +2 dB, Gate Release 300 ms.

Voicing auf Loose tauscht die feste Asymmetrie und Interstage-Filterung jeder Kaskadenstufe gegen eine sanfter angeschobene, breitbandigere Alternative — weniger asymmetrisches Clipping und lockerere Filterung auf jeder Stufe als beim Default-Voicing Tight, für einen eher vintage-artigen, luftigeren Charakter.

### Volles Triode mit Power Amp — *Feedback Tight Rhythm*, *Triode Foundation*

Feedback Tight Rhythm: Tight 140 Hz, Gain 30 dB, Bright an, Presence 6 dB, Engine Triode, Quality Standard, Power Amp an, Resonance 4 dB, Sag 20 %, Gate Key Pre, Gate Range 90 dB.

Gate Range bei 90 dB (statt dem harten Default Mute) lässt das Signal 90 dB abgesenkt statt völlig still — oft natürlicher bei einem sustained Part, da der Rauschteppich verschwindet, ohne dass die Spur klingt, als wäre sie abgeschaltet worden.

## Rezepte

1. **Tighter moderner Chug mit sauberem Gate.** Foundation Chug als Basis, Gate Key auf **Pre** umgeschaltet, Gate Hysteresis 3–6 dB. *Warum:* Bei 24+ dB Gain quetscht ein Post-Distortion-Detektor (der Default, und das v0.2.0-Verhalten) den Unterschied zwischen „spielt nicht" und „spielt" auf wenige dB zusammen — kein Threshold-Wert trennt die beiden sauber. Pre-Detection triggert von einer Kopie des Eingangssignals vor der Kaskade, durch einen festen Bandpass, und erhält so den tatsächlichen Dynamikumfang der Gitarre.

2. **Doom-/Sludge-Sag.** Sagging Doom als Basis, dann Sag zwischen 50–90 % fahren, je nachdem, wie spongy die Reaktion sein soll; Resonance proportional mithalten (höherer Sag wirkt besser mit mehr Low-Frequency-Depth, die ihn speist). *Warum:* Sag und Resonance sind beide Power-Amp-Feedback-Pfad-Regler, kein EQ — Resonance schneidet Bässe aus der Feedback-Schleife (was mehr durch den Amp selbst lässt), und Sag quetscht den Headroom des Ausgangsübertragers unter Last. Keins davon ist dieselbe Bewegung wie das Hochdrehen des Post-Cascade-Bass-Bandes.

3. **Heller Rhythmus, der trotzdem Platz für Vocals lässt.** Bright Aggressive als Basis, Mid auf −1 bis −2 dB gezogen (scooped), falls der Part Platz braucht, Tone Voice auf Flat belassen, da Bright die Aufhellung schon übernimmt. *Warum:* Bright und Treble leben beide in den Höhen, machen aber unterschiedliche Jobs — Bright speist mehr harmonischen Gehalt in die Kaskade selbst (subtile Lautheitsänderung, mehr Sizzle), während Treble und Presence den Tone-Stack und die Post-Cascade-EQ danach formen.

4. **Triode-Engine für anschlagsdynamischen Rhythmus.** Starte bei Triode Foundation, Bias Shift bei 100 % (die eigene kalibrierte Tiefe des Voicings), Quality beim Mixen auf Standard, nur für den finalen Bounce auf HQ wechseln. *Warum:* Die Triode-Stufen modellieren dynamischen Bias-Shift — ein übersteuerter Burst dämpft die folgende Schwingung und erholt sich über etwa 20 ms, was Palm Mutes komprimiert wirken lässt und Chugs „blühen" lässt, wie es die gedächtnislose Kaskade der Classic-Engine nicht reproduzieren kann.

5. **Classic vs. Triode A/B-vergleichen, ohne die Wiedergabe zu stören.** Engine einmal pro Session festlegen, statt sie zu automatisieren — ein Wechsel von Engine oder Quality ändert Tenebraes gemeldete Latenz, beide sind daher bewusst nicht automatisierbare, diskrete Konfigurationsänderungen statt Performance-Regler. *Warum:* `setLatencySamples()` kann nur vom Message-Thread aufgerufen werden; eine live-automatisierbare Latenzänderung ist nichts, was das Plugin-Delay-Kompensations-Modell eines Hosts sample-genau mitten in der Wiedergabe nachverfolgen kann.

> **Theorie — warum ein Gate vor der Distortion hören muss, nicht danach.** Ein Noise Gate funktioniert, indem es den Messwert eines Detektors mit einem Threshold vergleicht — aber *was* der Detektor hört, entscheidet, ob dieser Vergleich überhaupt etwas bedeutet. Speist man den Detektor mit dem vollständig verzerrten Post-Cascade-Signal (Tenebraes Default, passend zum v0.2.0-Verhalten), hat 24+ dB Gain die Lücke zwischen „Stille" und „spielt" schon auf eine Handvoll dB zusammengequetscht — es gibt womöglich keinen Threshold, der beide zuverlässig trennt. Gate Key = Pre löst das, indem es eine Kopie des *Eingangssignals* der Gitarre anzapft, bevor irgendein Gain der Kaskade angewendet wird, durch einen eigenen, auf den Nutzbereich der Gitarre abgestimmten Bandpass. Der Detektor sieht dann denselben Dynamikumfang, den deine Hände tatsächlich produziert haben, unverfälscht durch das, was 30 dB Kaskaden-Gain damit anstellen — deshalb ist Pre die Einstellung, zu der man greift, wenn ein Gate scheinbar nicht gleichzeitig bei leisen Noten offen und zwischen ihnen zu bleiben kann.

## Fallstricke

- **Engine und Quality sind gestuft, nicht automatisierbar.** Ein Wechsel während der Wiedergabe ist ein begrenzter, endlicher 2-ms-Crossfade mit vollständigem Chain-Reset — kein klickfreier Performance-Move. Einmal pro Session festlegen.
- **Gate ist standardmäßig an**, anders als jeder andere neue Regler in diesem Plugin. Eine alte (Pre-v0.2.0) Session zu laden aktiviert das Gate mit seinen Default-Settings obendrauf auf das, was bereits eingestellt war — prüfe das Tail-/Stille-Verhalten nach dem Laden einer älteren Session.
- **Keine Cabinet-Simulation, konstruktionsbedingt und dauerhaft.** Tenebrae ist die Gain-Stufe, nicht der Lautsprecher — kombiniere es mit einem Cab-Sim/IR-Loader (Nave oder anderweitig); es trocken auf den Monitor-Bus einer DAW zu fahren, klingt hart.
- **ADAA und der Quality-Regler gelten nur für die Triode-Engine** — Classic läuft immer mit seinem ursprünglichen festen 8x-Oversampling ohne Änderungen an der Anti-Aliasing-Behandlung, was es bit-identisch zu v0.2.0 hält.
- **Die Triode-Engine ist eine kalibrierte Näherung, keine Per-Sample-Schaltungslösung** — sie folgt einer Referenzlösung bei musikalischen Drive-Pegeln eng, weicht bei harten Transienten aber mehr ab, wo die Präzision der Lookup-Tabelle am gröbsten ist.
- **Der CPU-Kostenunterschied zwischen Eco/Standard/HQ ist relativ, keine absolut veröffentlichte Zahl** — behandle Standard als Mix-Setting und HQ als Mixdown-/Bounce-Setting, nicht als Zahl, gegen die du CPU präzise budgetierst.
- **Die GUI ist noch das Pre-M3-Funktionslayout**, auf eine zweite Zeile für die neueren Regler erweitert — der individuelle Look-and-Feel und der A11y-Pass folgen in einem späteren Meilenstein.
