# Nave — Praxis-Guide

*Praxisnahe Einstellungen für den Cabinet-IR-Loader, verankert in den Werkspresets.*

## Wo es hingehört

Nave nimmt ein trockenes, nicht-verstärktes Signal (eine DI, oder den Pre-Cab-Output eines Amp-Sims) und faltet es mit einer Cabinet-plus-Mikrofon-Impulsantwort — der Schritt, der aus einem brummigen Amp-Sim-Output etwas macht, das klingt, als wäre es im Raum an einem echten Cab abgenommen worden. Es sitzt typischerweise **nach** Distortion-/Amp-Sim-Processing und **vor** EQ-/Bus-Processing:

```
DI Gitarre/Bass → Amp-Sim/Preamp-Distortion → Nave (Cab IR) → EQ/Kompression → Mix-Bus
```

Typische Anwendungsfälle: nachträgliches Reamping einer aufgenommenen DI-Spur, Live-Betrieb in einer Monitoring-Kette beim Tracking, Blenden zweier Mikrofonpositionen oder zweier Cabinets, und das Simulieren von Mikrofonabstand ohne separates Plugin.

## Quick-Start-Einstellungen

### Tighter moderner Stack — *Tight Stack*

LoCut 75 Hz (12 dB/Okt), HiCut 9000 Hz, IR Blend 45 %, Blend Mode Crossfade, IR Align Precise, IR B Trim −2,5 dB, IR B Delay 0,35 ms, IR Gain Match Loudness.

Der kleine IR-B-Delay-Versatz ist der klassische Trick, um einen doublierten Mikrofon-Cab-Sound anzudicken, statt beide Slots perfekt zeitlich ausgerichtet zu lassen. IR Gain Match auf Loudness bedeutet, dass der Wechsel zwischen zwei unterschiedlich voiced Aufnahmen den Ton ändert, ohne auch den Pegel springen zu lassen — nützlich, während du noch das Blend-Verhältnis austarierst.

### Zwei Mikrofonpositionen, stufenlos blendbar — *Mic Morph*

LoCut aus (20 Hz), HiCut aus (20000 Hz), IR Blend 35 %, **Blend Mode Morph**, IR Align Precise.

Morph ist hier die bewusste Wahl, nicht Crossfade: Es zerlegt jede IR in ihren Frequenzgang und ihre Ankunftszeit, interpoliert beides unabhängig voneinander und baut eine einzige neue Impulsantwort zusammen — es gibt immer nur ein Cabinet im Signalweg, sodass das Ziehen an Blend stufenlos zwischen den beiden Aufnahmen wechselt, so wie ein Mikrofon, das physisch bewegt wird, ohne Kammfilter-Effekte an irgendeinem Punkt des Sweeps.

### Live-Monitoring — *Live Stage*

LoCut 80 Hz, HiCut 8000 Hz, IR Blend 0 %, IR Gain Match Energy, alles andere auf Default.

Ein schmaleres Band und eine einzelne IR (kein Blend) — ein bewusst simples, vorhersagbares Setting für eine Live-Monitoring-Kette, bei der ein einziger sauberer Ton gewollt ist statt ein fein austariertes Blend.

### Zurückgeschoben im Raum — *Pushed Back in the Room*

IR Blend 0 %, **Distance 60 %**, Level +1,5 dB, alles andere Default.

Distance reduziert Proximity-Effect-Bass und dunkelt die Höhen ab, je höher es steht — ein musikalisch nützlicher Tonal-Push, kein physikalisch exaktes Distanzmodell (keine Timing-Änderung, außer Distance Air ist zusätzlich aktiviert). Die +1,5 dB Level gleichen den Verlust aus, den das Hochziehen von Distance kostet.

### Dunkles Vintage-Voicing — *Dark Vintage*

LoCut 180 Hz, HiCut 4500 Hz, Distance 25 %.

Ein schmales Fenster plus ein Hauch Distance-Verdunkelung führt schnell zu einem boxigeren, eher vintage-artigen Ton, ohne zu einer anderen IR-Datei greifen zu müssen.

### Parallel gemischter Cab-Ton — *Parallel Cab (Blended Dry)*

Distance 20 %, **Mix 65 %**, Level +1 dB.

Mischt das cab-prozessierte Signal mit etwas vom unangetasteten trockenen Input, statt voll wet zu fahren — nützlich für einen hybriden reamped/DI-Ton.

## Rezepte

1. **Angedickter Doppel-Mikrofon-Cab.** Eine Close-Mic-IR in Slot A laden, eine zweite Position (oder ein anderes Cab) in Slot B, IR Blend um 40–50 %, IR B Delay um einen Bruchteil einer Millisekunde von null verschoben. *Warum:* Ein kleiner, bewusster Timing-Versatz zwischen den beiden Zweigen ist der klassische Trick, um einen doublierten Cab-Sound anzudicken — Precise-Alignment korrigiert bereits *unerwünschte* Fehlausrichtung (inklusive automatischem Umdrehen einer invertierten Aufnahme), hier stellst du bewusst wieder etwas davon her.

2. **Kammfilterfreier Morph zwischen zwei verwandten Mikrofonpositionen.** Zwei Aufnahmen desselben Cabinets in Slot A/B, Blend Mode Morph, dann IR Blend als Performance-Move automatisieren. *Warum:* Morph glänzt speziell bei verwandten Aufnahmen — Magnitude und Timing werden unabhängig interpoliert, sodass ein Blend-Sweep klingt, als würde sich ein Mikrofon physisch bewegen, statt dass zwei Cabinets überblenden und sich am Mittelpunkt teilweise auslöschen, wie es der Crossfade-Modus täte.

3. **Eine boomige oder fizzy rohe Aufnahme reparieren.** Starte mit LoCut/HiCut auf ihren Aus-Defaults und bring sie nur rein, wenn die IR es wirklich braucht — versuch zuerst LoCut mit 12 dB/Okt, wechsle auf 24 dB/Okt, wenn Matsch entfernt werden muss, ohne den Körper direkt darüber auszudünnen. *Warum:* Eine gut aufgenommene Cab-IR braucht oft kaum zusätzliche Filterung; Filter hinzuzufügen, die nicht gebraucht werden, kostet Headroom und CPU ohne hörbaren Nutzen, und die steilere Flanke tauscht einen schärferen Cutoff gegen weniger Überlappung mit den Frequenzen direkt darüber.

4. **Zwei IRs fair vergleichen.** Beide laden, IR Gain Match vor dem Vergleichen auf **Loudness** setzen. *Warum:* Raw-Energy-Matching (der Default) lässt eine dunkle Cabinet-Aufnahme — deren Energie größtenteils dort liegt, wo das Ohr am wenigsten empfindlich ist — leiser klingen als eine helle Close-Mic-Aufnahme, die dieselbe Energie misst. Der Loudness-Modus nutzt dieselbe K-Gewichtung wie ein LUFS-Meter, sodass ein IR-Wechsel den Ton ändert, ohne auch den wahrgenommenen Pegel zu ändern — das macht einen A/B-Vergleich wirklich zu einem über den Ton.

5. **Ein paralleler Reamp-Blend.** Distance um 15–25 % für einen Hauch „zurückgeschobenen" Charakter, Mix um 60–70 % statt voll wet. *Warum:* Weder Mix, Blend noch Distance gleichen sich konstruktionsbedingt gegenseitig im Pegel aus — so weißt du immer genau, was du hörst —, was bedeutet, dass Level nach dem Einstellen eines parallelen Blends zu prüfen kein optionaler Schritt ist, wenn er bei derselben wahrgenommenen Lautheit wie ein voll-wet-Patch sitzen soll.

> **Theorie — warum es den Morph-Modus überhaupt gibt, wenn Crossfade schon zwei IRs blendet.** Ein herkömmlicher Blend summiert den Output zweier parallel laufender Convolver. Wo immer die Direktschall-Anteile der beiden Aufnahmen zu leicht unterschiedlichen Zeiten eintreffen — was reale Aufnahmen fast immer tun, durch unterschiedliche Mikrofonabstände oder Aufbauten —, löscht sich diese Summe in einem Frequenzband teilweise aus. Das ist Kammfilterung, und sie ist am schlimmsten genau am 50-%-Blend-Punkt, wo „irgendwo zwischen diesen beiden Mikros" naturgemäß liegt. Morph vermeidet das Problem strukturell statt durch sorgfältige Ausrichtung: Es trennt jede IR in das, wonach sie klingt (ein Minimum-Phase-Magnitudenspektrum) und wann sie eintrifft (eine Bulk-Delay, gefunden durch Kreuzkorrelation), interpoliert diese beiden Eigenschaften unabhängig voneinander und baut aus dem Ergebnis eine einzige neue Impulsantwort zusammen. Da immer nur eine Cabinet-Antwort tatsächlich im Signalweg liegt, bleibt nichts übrig, gegen das die Summe kammfiltern könnte — der Trade-off ist, dass Morphs eigene Endpunkte nicht ganz identisch mit reinem IR A/IR B sind (man hört die Minimum-Phase-Version von jeder) — genau deshalb bleibt Crossfade der Default für alle, die die beiden Original-Aufnahmen unangetastet wollen.

## Fallstricke

- **Die drei „Reset"-Schalter — IR Gain Match, jeder Min-Phase-Toggle und IR Align — starten die Convolution-Engine bei Änderung kurz neu**, was eine hörbare Unterbrechung erzeugen kann, wenn du einen davon während laufendem Audio umschaltest. Das sind Settings, die man einmal einstellt, nicht automatisiert; alles andere (Blend, Mix, IR B Trim/Polarity/Delay, Distance, die Flanken-Schalter) ist vollständig klickfrei und automatisierbar.
- **Morph ändert die Endpunkte, nicht nur die Mitte.** Bei Blend 0 % im Morph-Modus hörst du die *Minimum-Phase-Version* von IR A, nicht IR A exakt — das liegt an der Technik selbst, und deshalb ist der Wechsel zu Morph eine bewusste Charakteränderung, nie etwas, das eine Session von selbst annimmt.
- **Morph funktioniert am besten bei verwandten Aufnahmen.** Zwei Mikrofonpositionen desselben Cabinets morphen wunderbar; zwei unverwandte Cabinets morphen durch Magnitudenverläufe, die kein reales Cabinet hat — das kann ein brauchbarer Sound-Design-Effekt sein, aber erwarte in dem Fall nicht, dass es sich wie eine physische Mikrofonbewegung verhält.
- **Distance ist ein Tonal-Push, kein physikalisches Distanzmodell** — es wird kein Timing-Versatz angewendet, außer Distance Air ist separat aktiviert. Für einen exakten Frequenzgang lieber zu LoCut/HiCut oder einer nachgeschalteten EQ greifen.
- **IRs länger als 10 Sekunden werden nur per Dateipfad gespeichert, nicht in die Session eingebettet.** Eine Cabinet-IR ist realistischerweise nie so lang, daher spielt das selten eine Rolle, aber eine fehlende/verschobene Datei für eine übergroße IR setzt diesen Slot beim Neuladen trotzdem auf den transparenten Default zurück.
- **Es gibt noch keine mitgelieferte IR-Bibliothek.** Das Kuratieren und Lizenzieren realer Cabinet-Aufnahmen ist eine separate, offen getrackte Aufgabe — du brauchst eigene IR-Dateien.
- **Vor v0.3.0 gespeicherte Sessions öffnen mit IR Align auf Legacy**, nicht Precise, damit sie weiterhin genauso klingen wie zuvor. Manuell auf Precise umschalten, wenn du das verbesserte Alignment (und die automatische Polaritätskorrektur) auf einer älteren Session willst.
