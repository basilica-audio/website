# Requiem — Praxis-Guide

*Praxisnahe Einstellungen für den kinematischen Convolution-Reverb, verankert in den Werkspresets.*

## Wo es hingehört

Requiem ist für die „kinematische" Ebene gebaut — Orchester, Chor, Pads, Ambience — getrennt von der „aggressiven" Ebene (Rhythmusgitarren, Drums, Bass), damit jede unabhängig prozessiert und platziert werden kann:

```
EQ → Kompression → Requiem → Limiter (falls letzte Stufe auf diesem Bus)
```

Generell nicht empfohlen direkt auf verzerrten Rhythmusgitarren oder Kick/Snare — der Hall-/Kathedralen-Charakter wirkt auf schnellem, perkussivem, verzerrtem Material wie Matsch; ein kurzer, plattenartiger Reverb (oder gar keiner) dient dort meist besser. Für Ambience speziell auf Gitarren Mix niedrig halten (10–20 %) und Decay kurz.

## Quick-Start-Einstellungen

### String-/Orchester-Bus — *Concert Hall*, *Tight Rhythmic Hall*

Concert Hall: Space Hall, Decay 2,2 s, Mix 30 %, Early/Late Balance 80 %, Size 50 %.
Tight Rhythmic Hall: Decay 1,6 s (kürzer), **Pre-Delay 90 ms** (lang), Mix 25 %, Early/Late Balance 60 % (mehr Early-Reflection-Charakter hörbar).

Tight Rhythmic Hall's langes Pre-Delay ist der Schlüssel-Move für schnelle Passagen — eine Lücke vor dem Eintreffen des Tails lässt das Ohr den Attack klar hören (Spiccato, Tremolo-Strings, palm-gemutete Layer darunter), bevor die Wash einfüllt, was Klarheit besser erhält, als Decay einfach zu verkürzen.

### Chor-Bus — *Choir Bloom*, *Living Cathedral*

Choir Bloom: Space Cathedral, Decay 5,0 s, Damping 5500 Hz (dunkel), Mix 45 %, Early/Late Balance 95 %, Size 90 %.
Living Cathedral: Decay 7,5 s, Engine **Hybrid Tail**, Tail Mod Depth 45 %/Rate 70 %, Damping 6000 Hz.

Chor will durchweg dunkleres Damping, längeres Decay und höheres Early/Late Balance als ein String-Bus — ein dunklerer Tail hält Sibilanz-/Atemgeräusche davon ab, sich in der Wash aufzubauen, und das nahe-100-%-Early/Late-Balance bevorzugt eine reine diffuse Wash gegenüber diskretem Early-Reflection-Charakter.

### Ambiente Pads / eingefrorene Texturen — *Frozen Drone*, *Infinite Frozen Nave*

Frozen Drone: Decay 8,0 s, **Freeze an**, Width 140 %, Modulation 20 %.
Infinite Frozen Nave: **Engine Tail Bloom, Freeze an**, Bloom Amount 70 %, Decay 8,0 s, Size 95 %.

Infinite Frozen Naves Freeze ist wirklich unbegrenzt — weil es auf der Tail-Bloom-Engine aufbaut (unter der Haube ein Feedback-Delay-Network), lässt Freeze dort die Dämpfung des Networks auf Unity ausklingen, statt einen endlichen Convolution-Kernel zu halten, der Hold hat also gar keine Decay-Längen-Obergrenze. Frozen Drone nutzt stattdessen Classic Convolution, wo Freeze weiterhin durch Decay begrenzt ist (hier auf 8 s gedreht, um den eingefrorenen Kernel selbst lang zu machen).

### Dialog/Score unter Narration — *Dialogue-Ducked Score*

**Engine Hybrid Tail**, Decay 4,2 s, **Duck Amount 65 %**, Duck Attack 8 ms/Release 400 ms, Low Cut 100 Hz/High Cut 11000 Hz.

Ducks Sidechain ist der trockene Input selbst — was das Ducking triggert, ist das Quellmaterial, nicht der Tail —, sodass sich der Reverb automatisch zurückzieht, wann immer die Quelle spielt, und in den Lücken wieder aufblüht, der Standard-Trick, um zu verhindern, dass ein großer Reverb Dialog oder eine Lead-Linie begräbt.

### Vintage-/Plate-Charakter — *Vintage Lush Plate*

Space Chamber, Decay 2,8 s, Pre-Delay 8 ms (kurz), Engine Hybrid Tail, **Tail Mod Mode Lush** (verstimmt bewusst), Tail Mod Depth 65 %, Low Cut 150 Hz/High Cut 9000 Hz.

Tail Mod Mode Lush ist die bewusst verstimmende Option — sie moduliert die Delay-Längen selbst statt nur, wie die Lines sich gegenseitig füttern, der klassische Vintage-Plate-Chorus-Charakter, hier bewusst eingesetzt statt vermieden.

### Subtile Air auf einem Bus — *Subtle Air*

Decay 1,2 s, Mix 12 % (sehr niedrig), Modulation 15 %, Size 30 %.

Eine kleine Modulation-Menge kombiniert mit niedrigem Mix ist das „kaum vorhanden"-Setting — genug, um den gelegentlich etwas statischen/metallischen Charakter des prozeduralen Generators abzumildern, ohne wie ein offensichtlicher Effekt zu wirken.

## Rezepte

1. **Schnelles, rhythmisches Material bleibt unter einer Wash verständlich.** Pre-Delay hochziehen, bevor zu kürzerem Decay gegriffen wird. *Warum:* Eine Lücke vor dem Einsetzen des Tails lässt das Ohr den Attack klar registrieren und erhält so die Klarheit, während dasselbe Raumgefühl erhalten bleibt — Decay stattdessen zu verkürzen reduziert den Raum selbst, was nicht immer das eigentliche Ziel ist.

2. **Ein Chor-Tail, der hart oder sibilant klingt.** Damping ein paar tausend Hz senken, bevor zu einer EQ auf dem Reverb-Return gegriffen wird. *Warum:* Damping ist die terminale Höhen-Ecke des Tails, und seit v0.2.0 dunkelt der Tail progressiv ab, während er ausklingt, statt eine statische Farbe anzuwenden — es zu senken adressiert die eigene Helligkeit des Tails an der Quelle statt sie nachträglich zu filtern.

3. **Ein Raum, der für sein Decay die falsche Größe wirkt.** Zu **Size** greifen, bevor Decay oder Space geändert wird. *Warum:* Size justiert die scheinbaren Dimensionen des Early-Reflection-Layers unabhängig von sowohl Decay (Tail-Länge) als auch Space (Reflection-Charakter) — es ist der Regler für „wie groß wirkt diese Hall/Cathedral/Chamber tatsächlich", ohne anzurühren, wie lange der Tail klingt, oder komplett zu einer anderen Space-Wahl zu wechseln.

4. **Matsch baut sich im Low End einer dichten Mischung auf.** **Bass Decay** Richtung 100 % oder darunter runterziehen, statt Decay insgesamt zu verkürzen. *Warum:* Bass Decay steuert speziell, wie viel länger die Bässe relativ zu Mitten/Höhen klingen — es zu reduzieren strafft nur die Bässe, während der Mid-/High-Tail (den man eventuell in seiner aktuellen Länge noch will) unangetastet bleibt, wo Decay insgesamt zu verkürzen alles verkürzen würde.

5. **Einen bestehenden Part in ein anhaltendes Pad verwandeln.** Freeze automatisieren, Mix hochfahren und einen Hauch Width und Modulation für Bewegung hinzufügen, während es hält. *Warum:* Freeze hält den aktuellen spektralen Content des Tails, statt ihn ausklingen zu lassen — nützlich unter einer Transition oder einem Breakdown, ohne ein separates Pad-Instrument zu brauchen —, und ein wenig Width/Modulation verhindert, dass eine gehaltene Textur komplett statisch wirkt, sobald sie anhält.

> **Theorie — warum Freeze in manchen Engine-Modi wirklich unendlich sein kann, in anderen nicht.** Classic-Convolution-Reverb funktioniert, indem der Input mit einem festen, endlichen Impulse-Response-Puffer gefaltet wird — es gibt keine Feedback-Schleife, um Audio unbegrenzt zu halten, nur einen Kernel bestimmter Länge. Freeze in diesem Modus regeneriert den Tail mit einem flachen Envelope, sodass, egal wie lange man hält, der Sustain immer noch durch das Decay-Setting begrenzt ist (bis zu 10 Sekunden) — ein eine Weile gehaltener Schnappschuss, kein wirklich unendlicher Drone. Hybrid Tail und Tail Bloom sind anders gebaut: Unter den Early Reflections sitzt ein Sechzehn-Line-Feedback-Delay-Network, und Freeze zu aktivieren lässt dort die Dämpfung jeder Line auf Unity ausklingen, was es zu einer verlustfreien Schleife macht, die genau das hält, was bereits darin zirkuliert — unbegrenzt. Das ist kein Workaround für die Grenzen von Classic Convolution — es ist ein bewusster Tausch. Forschung zu Feedback-Schleifen-basierten „Infinite-Reverb"-Designs dokumentiert, dass sie bei sehr langen Holds progressiv dumpfer werden können (wiederholtes Filtern im Feedback-Pfad dämpft Höhen weiter, selbst bei Unity-Gain) und mit zunehmender interner Ordnung hörbare Periodizität entwickeln können. Requiems Classic-Modus kann strukturell keins von beiden entwickeln, weil er von vornherein keinen Feedback-Pfad hat, der wiederholt gefiltert wird — der Tausch ist eine harte Obergrenze dafür, wie lange „unendlich" tatsächlich dauert.

## Fallstricke

- **Hybrid Tails Echo-Dichte baut sich am Übergang graduell auf, nicht sofort** — der FDN-Zweig wird von einem Impuls angeregt, seine eigene Reflection-Dichte steigt also über die ersten paar hundert Millisekunden nach der Naht, statt dicht zu starten. Das ist eine bekannte, gemessene Eigenschaft, kein Tuning-Bug.
- **Hybrid Tails spektrale Balance am Naht-Punkt stimmt auf ein paar dB, nicht auf eins.** Engeres Matching würde bedeuten, das ganze Network bei jeder Parameteränderung offline zu rendern, was den schnellen, klickfreien Re-Solve brechen würde, der der ganze Sinn des Hybrid-Modus ist — die kleine Neigung genau am Übergang ist die akzeptierte Kosten.
- **Matrix-Modulations Seitenbänder sind konstruktionsbedingt hörbar** — sie sind die Bewegung, für die das Feature existiert. Was auf eine enge Grenze gehalten wird, ist Pitch-Stabilität (unter einem Cent bei voller Tiefe), nicht die Seitenbänder selbst.
- **Sehr breite Width-Settings (150–200 %) können Phasen-/Mono-Kompatibilitätsprobleme verursachen** — die Mischung regelmäßig in Mono prüfen, falls Width hoch getrieben wird, besonders auf einem Bus, der später auf Mono gefaltet werden könnte (Broadcast, manche Streaming-Plattformen).
- **Es existiert keine veröffentlichte CPU-Zahl.** Lange Decay-Werte kosten proportional mehr CPU und Speicher, da Decay auch die Länge des generierten Kernels bestimmt, aber keine Benchmark-Zahl wird irgendwo im Projekt genannt.
- **Das v0.2.0-Voicing ist forschungsbasiert abgeleitet, nicht gegen Hardware oder ein kommerzielles Plugin gemessen** — abgeleitet aus öffentlichen Handbüchern, Entwickler-Interviews, Fachpresse-Reviews und Raumakustik-Literatur, nicht durch Messung irgendeiner Hardware-Einheit oder eines kommerziellen Plugins.
- **Der prozedurale Generator ist ein vereinfachtes Modell** (ein gefilterter Noise-Burst-Tail plus ein diskreter Early-Reflection-Zug), keine physikalische Simulation des modalen Verhaltens oder der exakten Reflexionsgeometrie eines echten Raums — gebaut für eine überzeugende kinematische Wash, nicht für akustische Messgenauigkeit.
