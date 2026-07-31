# Aureate — Praxis-Guide

*Praxisnahe Einstellungen für die orchestrale Sättigungs-Glue-Stufe, verankert in den Werkspresets.*

## Wo es hingehört

Aureate läuft **nach** dem Balancing der einzelnen Layer eines orchestralen/Chor-Stacks (oder einer doublierten Gitarre) — ein String- oder Brass-Bus, ein orchestraler/Chor-Submix, oder, sparsam eingesetzt, der volle Mix-Bus als subtiler Master-Glue-Pass. Es ist kein Distortion- oder Amp-Sim-Tool: Drive ist auf moderate 24 dB gedeckelt, und die Default-Warmth-/Character-Settings bleiben innerhalb von „fügt Wärme hinzu", nicht „fügt Dreck hinzu" — diese Rolle übernehmen andere Suite-Mitglieder (Overture/Tenebrae).

Typische Anwendungsfälle: eine Divisi-String-/Brass-Sektion zu einem Instrument verkleben, einen orchestralen/Chor-Submix kohärent machen, bevor er auf die Metal-Instrumentierung trifft, subtile Master-Bus-Glue, und (v0.3.0) Mix-Bus-artige Dynamics über die Glue-Sektion.

## Quick-Start-Einstellungen

### Subtile Master-Bus-Glue — *Master Glue (Subtle)*

Character Tape, Drive 3 dB, Warmth 25 %, **Mix 45 %**, Output 0 dB.

Niedriger Drive und ein Mix deutlich unter 100 % ist die bewusste Bewegung für einen Master-Bus-Pass — das soll eher gefühlt als gehört werden, dieselbe Rolle, die ein Summing-Bus in einem hybriden Analog-/ITB-Workflow spielt.

### Sektions-Glue — *String Section Glue*, *Console Summing Sheen*, *Choir Warmth*

String Section Glue: Character Tape, Drive 5 dB, Warmth 30 %, Tone +5 %, Mix 100 %.
Console Summing Sheen: Character Console, Drive 4 dB, Warmth 20 %, Tone +5 %.
Choir Warmth: Character Tape, Drive 4 dB, Warmth 50 %, **Tone −15 %** (abgedunkelt).

Console ist für das „Summing-Sheen"-Preset bewusst gewählt — es ist der Character, der bei niedrigem bis moderatem Drive transparent bleibt und erst bei stärkerem Anschieben Charakter zeigt, näher am Solid-State-/Transformer-Summing-Bus-Archetyp als Tapes unmittelbar hörbarere Glue.

### Ein wirklich andere Schaltungsklasse — *Valve Push*, *Brass Bloom*

Valve Push: **Character Valve**, Drive 14 dB, Warmth 60 %, Bias 15 %, Output −2 dB.
Brass Bloom: Character Console, Drive 8 dB, Warmth 40 %, Bias 10 %, Tone +10 %.

Valve ist das asymmetrischste, am stärksten geradzahlig-harmonisch geprägte der drei Character-Optionen — ein runderer, röhrenartiger Schub, und das mit der höchsten Warmth-getriebenen Bias-Obergrenze. Positiver Bias treibt die Asymmetrie noch weiter, unabhängig vom eigenen Beitrag von Warmth.

### Bus-Kompression über die Glue-Sektion — *Orchestral Bus Glue*, *Soft Tube Glue*, *Iron Bus Weight*

Orchestral Bus Glue: **Glue an, Glue Model VCA**, Threshold −6 dB, Ratio 4:1, Attack schnell, Release schnell, Makeup 2,5 dB, Character Console, Drive 4 dB.
Soft Tube Glue: **Glue Model Vari-Mu**, Threshold −10 dB, Character Valve, Tone −6 %.
Iron Bus Weight: Glue an (VCA), **Iron 65 %**, Character Console, Output −1 dB.

Diese drei zeigen die v0.3.0-Glue-Sektion in ihren nützlichsten Ausprägungen: VCA für klassisches, vorhersagbares Konsolen-Bus-Verhalten; Vari-Mu für einen weicheren Knee und einen intrinsischen, programmabhängigen Release; Iron hart angeschoben für Low-End-Transformer-Gewicht statt Kompressions-Charakter.

### Parallele/New-York-Sättigung — *Parallel Grit (New York)*

Character Valve, Drive 20 dB, Warmth 80 %, **Mix 50 %**, Output −3 dB.

Da Mix sample-genau delay-kompensiert ist, mischt sich ein stark angeschobenes, charaktervolles wet Signal unter das saubere trockene Signal, ohne Phasenverschmierung durch die Oversampling-Latenz.

## Rezepte

1. **Divisi-String-Sektion zu einem Instrument.** String Section Glue als Basis, Tone um +3 bis +8 % angehoben, falls die Sektion etwas präsenter gegen Gitarren wirken soll. *Warum:* Ein wenig Drive und Warmth verklebt eine Sektion so, wie es Tape-/Konsolen-Summing natürlicherweise tut — das Ziel ist eine Sektion, die wie ein Instrument wirkt statt wie ein Haufen Nahmikrofone, kein hörbarer Sättigungseffekt.

2. **Orchestraler Submix, bevor er auf die Metal-Instrumentierung trifft.** Console-Character (bleibt transparent, bis angeschoben), Drive 4–6 dB, Mix 100 %, sitzt nachdem einzelne Sektionen schon balanciert sind und bevor das Material den vollen Mix-Bus erreicht. *Warum:* Consoles „am wenigsten charaktervoll, bis angeschoben"-Verhalten bedeutet, dass es auf einem ganzen Submix sitzen kann, ohne leisere Passagen hörbar zu färben — Charakter kommt nur dort dazu, wo das Material tatsächlich laut genug ist, um ihn zu erreichen.

3. **VCA vs. Vari-Mu für Bus-Glue wählen.** Greife zu **VCA** (Orchestral Bus Glue), wenn klassisches, vorhersagbares Konsolen-Bus-Verhalten gewollt ist und der Attack-Schalter tatsächlich etwas tun soll; greife zu **Vari-Mu** (Soft Tube Glue), wenn ein weicherer Knee und ein Release gewollt sind, der seine Form mit dem Programmmaterial ändert statt einer festen Zeitkonstante zu folgen. *Warum:* siehe die Theorie-Box unten — die beiden sind nicht nur unterschiedliche Presets eines Gesetzes, sondern völlig unterschiedliche Detektor-/Gain-Cell-Topologien.

4. **Iron für Gewicht, nicht für Kompression.** Iron Bus Weight als Basis, Iron zwischen 40–70 %, Drive moderat gehalten (6–8 dB), da Irons eigene Low-End-Sättigung schon reichlich beisteuert. *Warum:* Weil der Fluss eines Transformatorkerns das Integral des angelegten Signals ist, sättigt der Kern bei gleichem Pegel in den Bässen weit härter — Third-Harmonic-Content steigt von selbst steil Richtung unteres Ende, was als „Gewicht" statt „Fizz" wirkt, ohne Drive in hörbares Distortion-Territorium treiben zu müssen.

5. **Drive auditieren, ohne dass es zum Lautheits-Wettbewerb wird.** **Auto Gain** aktivieren, während Character/Drive/Warmth eingestellt werden, damit verglichen wird, was Charakter ist, nicht Pegel. *Warum:* Auto Gain ist eine Ein-Punkt-Kalibrierung pro Character (gemessen gegen equal-RMS Pink Noise), ein bewusstes Hör-Hilfsmittel statt ein Mastering-Tool — nach dem Festlegen auf ein Drive-Setting wieder aus- und Gain-Staging manuell von dort aus vornehmen.

> **Theorie — warum ein vari-mu-artiges Gesetz anders verklebt als ein VCA.** Beide Glue-Gesetze von Aureate teilen sich dieselbe Feedback-Topologie — ein Detektor, der das Signal *nach* der Gain-Zelle liest, ein Sample alt —, was auf beiden einen weichen Knee und einen programmabhängigen Release erzeugt, statt einer separat kurvengefitteten Knee-Form. Wo sie sich wirklich unterscheiden, ist das, was innerhalb dieser Schleife sitzt. Das VCA-Gesetz löst ein unkompliziertes dB-Domain-Timing-Netzwerk: seine Attack-Zeit ist eine echte, einstellbare Zeitkonstante, und eine Transiente doppelter Größe verdoppelt ungefähr, wie schnell sich die Gain Reduction ändert — eine exponentielle, vorhersagbare Reaktion. Das Vari-Mu-Gesetz setzt stattdessen einen strombegrenzten Gleichrichter und ein Drei-Kondensator-Release-Netzwerk ein, das eine röhrenlimiter-artige Gain-Zelle modelliert, und das ändert die Physik: Attack ist kein einstellbarer Wert mehr, weil er intrinsisch daran hängt, wie schnell der Gleichrichter reagieren kann; ein größeres Überschwingen braucht proportional *länger*, um seine eigene Gain Reduction zu erreichen (nicht weniger); und die Hardware-Klassen-Markierungen der vier Release-Positionen (0,1/0,3/0,6/1,2 s) stimmen nicht mit ihren gemessenen Erholungszeiten überein (etwa 0,3/0,8/2/5 s) — weil die Erholung des Speicherkondensators tatsächlich davon abhängt, wie lange er geladen wurde, genau das „Glue"-Verhalten, das eine feste Zeitkonstante nicht erzeugen kann.

## Fallstricke

- **Der Attack-Regler des Vari-Mu-Gesetzes tut nichts** — sein Attack ist intrinsisch an den eigenen strombegrenzten Gleichrichter der Schaltung gebunden, kein einstellbarer Parameter. Wenn Attack für den Workflow zählt, das VCA-Gesetz nutzen.
- **Die Release-Schalter-Markierungen des Vari-Mu-Gesetzes entsprechen nicht seinen gemessenen Erholungszeiten** (Markierungen 0,1/0,3/0,6/1,2 s vs. gemessen ~0,3/0,8/2/5 s) — eine dokumentierte, bewusste Eigenschaft der modellierten Schaltungsklasse, kein falsch beschrifteter Regler.
- **Der Knee des VCA-Gesetzes verengt sich bei höheren Ratios deutlich** — etwa 2,2 dB breit bei 2:1, unter 1 dB bei 4:1 und 10:1. Das ist der höhere Gain der Feedback-Schleife bei höheren Ratios, keine zu behebende Inkonsistenz.
- **Es gibt keinen veröffentlichten CPU-Benchmark.** Quality HQ wertet einen zusätzlichen Antiderivativ-Term pro oversampletem Sample aus gegenüber Classic — echte Kosten, keine genannte Prozentzahl.
- **Die Glue-Sektion ist rein Envelope-basiert — sie hat keinen eigenen Detektor-Nichtlinearitäts-/Distortion-Charakter.** Wer den *Distortion*-Charakter eines Bus-Kompressors statt nur seiner Dynamik will, findet den im Character-Sättiger und der Iron-Stufe weiter unten in der Kette.
- **Das Voicing ist durchgehend an veröffentlichter Schaltungsanalyse und Trioden-Gesetzen verankert, die an einen dokumentierten Regelbereich gefittet sind, nicht an Messungen bestimmter Hardware-Einheiten.** Jede Verhaltensaussage (eine Knee-Breite, ein Slew-Verhältnis, ein Zeitkonstanten-Verhältnis) ist eine getestete Invariante, kein „klingt wie"-Anspruch.
- **Irons gemessener Low-End-Anstieg liegt in dieser Implementierung bei etwa 10 dB/Oktave**, unter den 12 dB/Oktave, die ein idealisiertes Flux-Integrations-Modell vorhersagen würde — eine reale, gemessene Eigenschaft der endlichen Kernkurve, kein Bug.
- **Der Editor ist noch das funktionale v0.1-Slider-Layout** — ein individuelles, photorealistisches Panel folgt als späterer, suite-weiter Meilenstein.
