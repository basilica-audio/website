# Silentium — Praxis-Guide

*Praxisnahe Einstellungen für das Lookahead-Noise-Gate/den Expander, verankert in den Werkspresets.*

## Wo es hingehört

Silentium ist eine Detection-and-Dynamics-Stufe, kein Tone-Shaping-Tool — wo du es platzierst, ändert, worauf es reagiert. Übliche Platzierungen: **vor** jedem Drive-/Distortion-Plugin, um das saubere Signal zu gaten (vermeidet, Gating-Artefakte mitzuverstärken, und lässt den Sidechain-Filter von einem unverzerrten Signal triggern); **nach** der Amp-/Cab-Stufe nur, wenn das Rauschen speziell dort entsteht; immer **vor** zeitbasierten Effekten (Reverb/Delay), damit ein ausklingender Tail nie mittendrin abgeschnitten wird. Bei einer Wall-of-Guitars-Mischung eine Instanz pro Spur statt einer auf dem Bus — Lookahead pro Spur hält jede Ebenen-Attacke straff und synchron.

Typische Anwendungsfälle: Rauschkontrolle bei Rhythmusgitarren, ambientes/anhaltendes Material, das einen sanfteren Downward-Expander statt eines harten Gates braucht, das Ducken eines Parts unter einen anderen, und rhythmisch gelocktes Gating, getriggert von einem externen Sidechain.

## Quick-Start-Einstellungen

### Tightes Rhythmus-Gating — *Chug Lock*

Threshold −42 dB, Attack 0 ms, Hold 10 ms, Release 40 ms, Range −80 dB, Lookahead 5 ms, SC HPF 80 Hz, **Smooth Open an**.

Attack bei 0 ms mit aktiviertem Lookahead ergibt einen wirklich augenblicklichen Sprung auf Unity genau beim Threshold-Übertritt — das perkussivste verfügbare Setting —, und Smooth Open ist es, was diesen sofortigen Attack vom Klicken abhält: Es formt das Öffnen zu einer Rampe, die vollständig ins Lookahead-Fenster passt und genau dann fertig ist, wenn die verzögerte Transiente die Delay-Line verlässt.

### Chirurgisch, still zwischen den Noten — *Surgical Mute*

Threshold −45 dB, Attack 0,5 ms, Hold 15 ms, Release 60 ms, Range −80 dB, SC HPF 100 Hz.

Nutzt bewusst **kein** Smooth Open — Smooth Open weicht auch die *schließende* Flanke auf und hält das Gate etwas länger offen, was messbar reduziert, wie viel leiser dieses Preset zwischen den Noten im Vergleich zu Natural Decay ist. Wenn Stille zwischen den Noten das oberste Ziel ist, Smooth Open aus lassen.

### Ambientes/anhaltendes Material — *Ambient Sustain*, *Natural Decay*

Ambient Sustain: Threshold −50 dB, Attack 5 ms, Hold 200 ms, Release 400 ms, **Range −24 dB** (keine harte Stummschaltung), Knee 12 dB.
Natural Decay: Threshold −38 dB, Hold 30 ms, Release 150 ms, Range −16 dB, Knee 6 dB.

Beide lassen Range deutlich vor voller Stille stehen und weiten Knee erheblich — ein Soft-Knee-Setting mit flachem Floor wirkt wie ein natürliches Ausklingen statt wie ein umgelegter Schalter. Das Gate agiert hier eher wie ein sanfter Leveler als wie ein An/Aus-Gate.

### Einen Part unter ein Lead ducken — *Duck Under Lead*

Threshold −20 dB, Attack 10 ms, Release 200 ms, Range −10 dB, **Duck an**.

Duck kehrt den Gain-Computer um: Statt oberhalb von Threshold zu öffnen, dämpft das Signal darüber Richtung Range. Der gesamte Detection-Pfad (SC HPF, Hysteresis, Hold, Knee, Lookahead) gilt weiterhin — dieselbe Engine, nur in die andere Richtung gezielt.

### Extern getriggertes, rhythmisch gelocktes Gate — *Expander Glue*

Threshold −45 dB, Ratio 2,5:1, Range −18 dB, RMS-Detection, Hysteresis 3 dB, Linear Release Shape, Smooth Open an.

Gar kein hartes Gate — Ratio bei 2,5:1 macht das zu einem Downward-Expander: Jedes dB, das das Signal unter den Threshold fällt, bekommt 1,5 dB Dämpfung, proportional statt geschaltet. Das ist der Ausgangspunkt, wenn ein Gate zu offensichtlich nach Gate klingt.

## Rezepte

1. **Pro-Spur-Gating in einer geschichteten Rhythmus-Mischung.** Eine Silentium-Instanz pro DI-/Amp-Sim-Spur (nicht eine auf dem Bus), Chug Lock als Basis, Attack 0 ms mit Lookahead bei 3–5 ms. *Warum:* Jede Performance hat ihr eigenes Pick-Attack-Timing; Lookahead pro Spur hält jede Ebenen-Attacke straff und synchron, wo ein einzelnes Gate auf Bus-Ebene das individuelle Timing der Ebenen verschmieren würde.

2. **Rhythmisch gelockter Chug, getriggert von Click oder Kick.** Externen Sidechain-Input von einem Click-Track oder Kick-Drum routen, Expander-Glue-Settings als Basis, Duck aus (das bleibt ein Gate, nur extern getriggert). *Warum:* Detection von einer anderen Quelle als dem Hauptsignal zu triggern, entkoppelt den Gate-Rhythmus vollständig von der eigenen Pick-Dynamik des Gitarristen — nützlich für programmierte oder eng quantisierte Rhythmus-Parts, oder um einen doublierten/vervierfachten Part im Gleichschritt gaten zu lassen, statt dass jede Ebene ihre eigene, leicht andere Entscheidung trifft.

3. **Amp-Rauschen bereinigen, ohne dass jemand ein Gate bemerkt.** Expander Glue als Ausgangspunkt, Ratio zwischen 2:1 und 4:1, RMS-Detection, Release Shape Linear. *Warum:* Ein Downward-Expander bei moderatem Ratio macht eine ausklingende Note proportional leiser, je weiter sie gefallen ist, statt bei einem Threshold komplett abzuschalten — der mechanische Unterschied zwischen „man hört, wo das Gate ist" und „der Rauschteppich ist einfach leise nicht mehr da".

4. **Chattern bei einem Signal beheben, das nah am Threshold pendelt.** Hysteresis Richtung 6 dB anheben, oder Knee Richtung 6–12 dB weiten, falls der harte An/Aus-Sprung selbst das Problem ist und nicht speziell das Chattern. *Warum:* Hysteresis trennt Öffnungs- und Schließ-Threshold, sodass ein Signal, das genau an der Grenze dithert, das Gate nicht hin- und herklappen lassen kann; Knee blendet stattdessen die Ziel-Gain sanft über ein Band um den Threshold — eine andere Lösung für ein verwandtes, aber eigenständiges Symptom (switchy klingende Übergänge vs. echtes Chattern).

5. **SC HPF/SC LPF nach Gehör statt nach Vermutung einstellen.** Erst **Listen** aktivieren, SC HPF und SC LPF durchfahren, bis nur noch der Transienten-Content zu hören ist, der das Gate triggern soll, dann Listen wieder aus und Threshold setzen. *Warum:* Listen leitet das sidechain-gefilterte Detection-Signal direkt zum Output, unter Umgehung des Gain-Computers — es zeigt genau, worauf der Detektor reagiert, was aus dem gegateten Output allein nach Gehör kaum korrekt zu erschließen ist.

> **Theorie — warum ein Gate zwei unterschiedliche Jobs braucht, erledigt von zwei unterschiedlichen Filtern.** Silentiums SC HPF und SC LPF berühren ausschließlich den Detection-Pfad — nie das Audio, das man tatsächlich hört —, weil das, was ein Gate *triggern* soll, und das, was das Gate *durchlassen* soll, oft unterschiedliche Fragen sind. Die Pick-Attack-Transiente einer Gitarren-DI lebt größtenteils in einem schmalen Obere-Mitten-Band; dasselbe Signal trägt in den Bässen Brummen, Proximity-Effekt und Rumpeln, das ein Gate auf einer sonst stillen Passage fälschlich offen halten kann. Das Band des Sidechains auf genau den Transienten-Content zu verengen, auf den das Gate reagieren soll (SC HPF hoch, SC LPF runter) — ohne ein einziges Sample des wet Signals anzurühren —, ist der Grund, warum Silentium selbst bei einer verrauschten DI selbstbewusst gaten kann, obwohl der Rohsignal-Pegel allein kaum etwas Brauchbares aussagt.

## Fallstricke

- **Für dieses Plugin existiert keine veröffentlichte CPU-Zahl** — mehrere Detection-Pfade laufen bedingungslos parallel (beide Detektor-Typen, beide Sidechain-Flanken), speziell damit das Umschalten zwischen ihnen ein Crossfade statt ein kalter Neustart ist; behandle jede anderswo genannte CPU-Zahl als unverifiziert.
- **Smooth Open tauscht Schließ-Präzision gegen Öffnungs-Weichheit.** Es hält das Gate bis zu die Hälfte der Lookahead-Zeit offen, nachdem das Signal abgefallen ist — meist unhörbar, aber genau deshalb lassen die tightesten, stilleorientierten Presets (Surgical Mute) es aus.
- **Ein Lookahead-Wechsel während der Wiedergabe crossfadet über 10 ms und meldet die neue Latenz kurz danach** (v0.4.0-Verhalten) — vor v0.4.0 tat der Regler nichts, bis der Host das Plugin zufällig neu vorbereitete; ältere Dokumentation, die diese Einschränkung beschreibt, gilt nicht mehr.
- **Das „programmabhängige" Attack-/Release-Verhalten ist von in dieser Kategorie dokumentierten Hardware-Noise-Gate-Release-Kurven inspiriert, keine Reproduktion davon** — behandle es als eigenen, getesteten Mechanismus dieses Plugins, nicht als Anspruch, ein bestimmtes Gerät zu treffen.
- **Wenn nichts in den externen Sidechain-Bus geroutet ist (oder er deaktiviert ist), fällt die Detection automatisch auf den Haupteingang zurück** — es gibt keinen separaten „kein Sidechain"-Modus, was auch bedeutet, dass ein versehentlich aktivierter, aber leerer Sidechain-Bus sich exakt wie gar kein Sidechain verhält.
- **Der Editor ist noch ein funktionales Slider-/Knopf-Layout, keine eigene GUI** — ein photorealistisches Panel mit Per-Bus-Metering folgt in einem späteren Meilenstein.
- **Ratios Default (∞:1, angezeigt als „Gate") nimmt den wörtlichen Pre-v0.4.0-Codepfad**, keine Näherung des Downward-Expander-Gesetzes bei sehr großem Ratio — eine Session, die Ratio nie anfasst, verhält sich also konstruktionsbedingt identisch zu vor v0.4.0.
