# Firmament — Praxis-Guide

*Praxisnahe Einstellungen für den Stereo-Widener & -Imager, verankert in den Werkspresets.*

## Wo es hingehört

Firmament ist ein Breite-/Imaging-Tool, was es eher ans hintere Ende einer Channel- oder Bus-Kette platziert, nachdem Tone-Shaping und Dynamics schon entschieden sind:

```
Korrektive/tonale EQ, Kompression, Sättigung → Firmament (Breite entscheiden) → Reverb-/Delay-Sends, finales Bus-Processing
```

Typische Platzierungen: String-/Chor-/Pad-Busse (der Hauptanwendungsfall), ein sanfter Touch auf einem doublierten Rhythmusgitarren-Bus, und — sparsam eingesetzt — der Master-Bus, wo Bass Mono die Kick-/Bass-/Low-Gitarren-Energie zentriert hält, während Becken/Strings/Reverb-Tails oberhalb der Crossover so breit bleiben, wie die Mischung sie schon gemacht hat.

## Quick-Start-Einstellungen

### Chor-/Orchester-Bus — *Choir Bloom*, *Open Strings*

Choir Bloom: **Width 170 %**, Bass Mono Freq 130 Hz, Low Width 15 % (etwas Breite überlebt sogar unter der Crossover), **Auto Mono Safety an** (Floor −12 dB).
Open Strings: Width 140 %, Bass Mono Freq 110 Hz, Auto Mono Safety an.

Choir Blooms Low Width bei 15 % (statt Default 0 %) ist eine bewusste Ausnahme — die meisten Bass-Mono-Anwendungsfälle wollen das Low Band voll zentriert, aber sehr breites Pad-/Chor-Material kann manchmal davon profitieren, wenn etwas Breite selbst unterhalb der Crossover überlebt.

### Doublierter Rhythmusgitarren-Bus — *Doubled Rhythm Glue*, *Subtle Openness*

Doubled Rhythm Glue: Width 125 %, Bass Mono Freq 150 Hz, Low Width 0 % (voll zentriert darunter).
Subtle Openness: Width 115 % (sanfter), Bass Mono Freq 100 Hz.

Ein sanfterer Touch (110–125 %) verklebt zwei bereits gepannte Doubles zu einer breiteren Wand, ohne die extremen „gehypten" Artefakte, die aggressiveres Verbreitern erzeugen kann — Firmament fügt bei diesen Settings nie etwas hinzu, das nicht schon im Stereobild war (abgesehen von Haas Mode/Decorrelate).

### Master-Bus, sparsam — *Master Bus Bass Mono*

Width 100 % (unverändert — Breite-Entscheidungen wurden schon vorgelagert getroffen), **Bass Mono Freq 90 Hz**, **Auto Mono Safety an mit Multiband an**.

Auto Mono Safety Multiband beurteilt Low und High Band unabhängig statt eine globale Korrelationsablesung — hier speziell nützlich, weil der Bass bereits über Bass Mono sicher zentriert ist und ein unabhängiges Phasenproblem in den Höhen nicht unnötig auch den Bass dämpfen soll (oder umgekehrt).

### Mono-kompatible Nah-Mono-Verbreiterung — *Mono-Safe Air*, *Velvet Width*

Mono-Safe Air: **Decorrelate an** (Classic-Modus), Decorrelate Amount 35 %.
Velvet Width: Width 120 %, **Decorrelate an, Decorrelate Mode Velvet Dense/Sparse**, Amount 60 %, **Width Comp an**, Auto Mono Safety an.

Velvet Width ist die vollständig mono-summen-sichere Option — die Velvet-Dekorrelations-Modi synthetisieren nur den Stereo-Differenz-Content, sodass der Mono-Downmix bei jedem Amount bit-für-bit die eigene Mono-Summe des Inputs ist, anders als Classic Decorrelates kleines dokumentiertes Mono-Downmix-Ripple.

### Dramatischer Breite-Effekt — *Wide Pad, Full Precedence*, *Extreme Width*

Wide Pad, Full Precedence: **Haas Mode an**, Haas Time 22 ms (innerhalb der „Precedence-Effekt"-Zone), Output −1 dB.
Extreme Width: **Width 200 %** (Maximum), Bass Mono Freq 120 Hz, Auto Mono Safety an mit festerem Floor (−15 dB), Output −3 dB.

Beide sind bewusst Spezialeffekt-Settings, keine Defaults, die durchgehend aktiv bleiben sollten — Haas Mode ist speziell nicht mono-summen-sicher (erzeugt Kammfilterung beim Downmix), also greift man dazu, wenn der stärkere, dramatischere Charakter mehr zählt als Translation.

### Drei-Band-Imaging — *Three Band Imager*

Low Width 40 %, Width 110 % (Mid Band), **High Split 2500 Hz, High Width 140 %**, Bass Mono Mode Phase Matched, Auto Mono Safety Multiband an.

Drei unabhängig steuerbare Bänder (unter Bass Mono Freq, zwischen den beiden Crossovern, über High Split) — nützlich, um die Breite der Mitten exakt zu erhalten, während Becken-/Air-Content separat oberhalb von 2,5 kHz geöffnet wird.

### Mastering-taugliches Linear-Phase-Bass-Mono — *Mastering Linear Phase Bass Mono*

Bass Mono Freq 120 Hz, **Bass Mono Mode Linear Phase** (2048 Samples gemeldete Latenz bei 48 kHz), Auto Mono Safety an mit Safety Response Smooth.

Linear Phase ist eine Mastering-/Render-Entscheidung, kein Live-Toggle — vor einem Render-Pass festlegen statt während der Wiedergabe umzuschalten, da der Moduswechsel eine kurze Stummschaltung anwendet, während der Host die Delay-Kompensation neu verhandelt.

## Rezepte

1. **Entscheiden, ob Bass Mono überhaupt gebraucht wird.** Erst mit Width allein starten — die meisten Materialien brauchen nur den einzelnen globalen Regler. Zu Bass Mono Freq/Low Width speziell greifen, wenn der Bass beim Hochziehen von Width an Fokus verliert oder in Mono schlecht übersetzt. *Warum:* Eine Crossover und einen zweiten Breite-Parameter hinzuzufügen lohnt die Komplexität erst, wenn ein einzelnes globales Width-Setting den Bass hörbar kompromittiert — die meisten Busse brauchen das nicht.

2. **Mono-Kompatibilität prüfen, bevor ein breites Setting festgelegt wird.** **Mono Audition** aktivieren, statt nach dem Downmix-Button der eigenen DAW zu suchen. *Warum:* Es ist genau der Downmix `(L+R)/2`, um den es bei Firmaments Mono-Kompatibilitätsgarantien tatsächlich geht, angewendet nach allem anderen in der Kette — eine Ein-Klick-Version der „immer in Mono A/B-vergleichen"-Gewohnheit.

3. **Zwischen Decorrelate und Haas Mode für Nah-Mono-Material wählen.** **Decorrelate** bevorzugen (speziell die **Velvet-Modi**), wann immer Mono-Translation überhaupt zählt — zu **Haas Mode** nur greifen, wenn der stärkere, dramatischere Precedence-Effekt-Charakter gewollt ist und Translation zweitrangig ist (ein Übergangseffekt, ein Layer, das nie auf Mono gefaltet wird). *Warum:* Classic Decorrelates dokumentierte Kosten beim Mono-Downmix sind mildes spektrales Ripple; die Velvet-Modi haben konstruktionsbedingt null Kosten. Haas Modes Kosten sind tiefe, hörbare Kammfilter-Notches — ein grundlegend anderes Risikoniveau.

4. **Width fair auditieren, ohne den „breiter klingt besser"-Bias.** **Width Comp** aktivieren. *Warum:* Ohne das ist 200 % Width messbar heißer und 0 % messbar leiser, rein daraus, wie viel Energie der Side-Kanal trägt — was jeden A/B-Vergleich zu dem lauteren Setting hin verzerrt statt zu dem tatsächlich besser klingenden. Width Comp wendet Equal-Power-Makeup-Gain an, sodass die Lautheit beim Durchfahren konstant bleibt.

5. **Ein Sicherheitsnetz für einen Bus, der nicht ständig überwacht werden kann.** **Auto Mono Safety** aktivieren, und **Multiband** hinzufügen, falls Bass Mono auch aktiv ist und sich das Phasenverhalten von Low/High Band wahrscheinlich unterscheidet. *Warum:* Auto Mono Safety zügelt Side automatisch, wann immer der Input stark außer Phase tendiert, unabhängig von und zusätzlich zu dem bereits eingestellten Width/Low Width — es rührt Mid nie an, kann also die Mono-Downmix-Garantie nicht brechen, es zügelt immer nur, wie breit Side wird.

> **Theorie — warum Velvet-Noise-Dekorrelation mono-kompatibel bleibt, wo andere Verbreiterungstricks es nicht sind.** Ein Stereobild durch asymmetrische Behandlung der Kanäle zu verbreitern — eine Seite verzögern (Haas Mode) oder ein Allpass-Netzwerk nur auf dem rechten Kanal laufen lassen (Classic Decorrelate) — funktioniert akustisch, aber zwei unterschiedlich behandelte Kanäle zu summieren erzeugt bei bestimmten Frequenzen Auslöschung, wenn auf Mono gefaltet: tiefe Kammfilter-Notches bei einer Verzögerung, milderes spektrales Ripple bei einem Allpass-Netzwerk. Firmaments Velvet-Dense-/Sparse-Modi vermeiden das strukturell statt durch sorgfältiges Tuning: Der Kern-Mid/Side-Codec skaliert immer nur den Side-(Differenz-)Kanal — Width, Low Width, High Width und die Velvet-Dekorrelatoren arbeiten alle ausschließlich auf Side, und Mid wird von keinem davon berührt. Da ein Mono-Downmix sich mathematisch immer zu `Mid + Mid` ergibt, egal was Side enthält, kann keine noch so aggressive, nur auf Side angewendete Verarbeitung je ändern, was ein Mono-Hörer hört. Die Velvet-Noise-Koeffizienten selbst (veröffentlichte, DAFx-18-optimierte Paare) sind speziell so strukturiert, dass diese Art der Side-Verbreiterung wie echte Dekorrelation statt wie ein offensichtlicher Effekt klingt, aber die Mono-Sicherheitsgarantie hängt nicht davon ab, wie gut diese Koeffizienten getuned sind — sie gilt konstruktionsbedingt, genau wie beim einfachen Width-Regler.

## Fallstricke

- **Haas Mode und Decorrelate sind nicht mono-summen-sicher, anders als Width/Low Width/Auto Mono Safety.** Zwei zeitversetzte oder unterschiedlich gefilterte Kanäle zu summieren erzeugt Mono-Downmix-Artefakte — tiefe Kammfilter-Notches bei Haas Mode, milderes spektrales Ripple bei Classic Decorrelate (die Velvet-Modi sind die Ausnahme, konstruktionsbedingt vollständig sicher). Falls garantierte Mono-Kompatibilität zählt (Broadcast-Delivery, ein unvorhersehbarer Club-Mono-Sub), beide aus lassen und sich allein auf Width/Low Width/Auto Mono Safety verlassen.
- **Haas Mode und Decorrelate schließen sich gegenseitig aus.** Sind beide aktiviert, greift Decorrelate und Haas Modes Delay wird komplett umgangen.
- **200 % Width ist ein Spezialeffekt-Setting, nichts, das auf einer ganzen Mischung oder einem lauten Bus dauerhaft aktiv bleiben sollte** — auf diesem Level wirkt es schnell künstlich/phasig; weit nützlicher kurz automatisiert (ein Chorus-Lift, ein Breakdown) als durchgehend an.
- **Linear Phase Bass Mono meldet echte Latenz (2048 Samples bei 48 kHz)**, und ein Wechsel dorthin oder davon während der Wiedergabe wendet eine kurze Stummschaltung an und kann in manchen Hosts klicken, während sie die Delay-Kompensation neu verhandeln — den Modus vor einem Render-Pass festlegen statt live umzuschalten.
- **Auf einer Mono-Input-Spur/-Bus haben Width/Low Width/Auto Mono Safety nichts, worauf sie wirken können** (es gibt kein Side-Signal zu skalieren) — das Plugin lässt die Quelle sauber durch. Haas Mode/Decorrelate sind die Regler, die in dieser Situation weiterhin etwas tun, da sie nach dem (jetzt identischen) L/R-Paar-Decode arbeiten.
- **Auto Mono Safety Multiband ändert Auto Mono Safetys Verhalten, wann immer sowohl Auto Mono Safety als auch Bass Mono Freq zusammen aktiv sind** — es ist standardmäßig aus, speziell weil es eine Verhaltensänderung ist, keine strikte Verbesserung, für diese Kombination.
- **Die GUI ist noch der schlichte funktionale v0.1/v0.2-artige Editor** — jeder Parameter ist vollständig aus dem eigenen Fenster des Plugins oder dem generischen Editor eines Hosts steuerbar, aber die Korrelations-/Phasen-Schätzung, die Auto Mono Safety antreibt, wird noch nicht als sichtbares Meter angezeigt (der DSP-Wert ist vollständig berechnet und getestet, nur noch nicht dargestellt).
- **Alle Default-Werte und -Bereiche sind forschungsbasiert abgeleitet** aus öffentlichen Handbüchern, Entwickler-Dokumentation, Mastering-Forum-Konsens und Akustik-Literatur — nicht gegen den tatsächlichen Audio-Output irgendeines kommerziellen Stereo-Wideners gemessen, und kein proprietärer Algorithmus eines anderen Anbieters wurde inspiziert oder nachgeahmt.
