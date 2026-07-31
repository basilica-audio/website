# Crypta — Praxis-Guide

*Praxisnahe Einstellungen für die 3-Band-Bass-Voicing-Stufe, verankert in den Werkspresets.*

## Wo es hingehört

Crypta ist die bassspezifische Voicing-Stufe: **DI/Amp-Sim → Crypta → Bus-Kompression/Glue → Mix-Bus**. Es erwartet ein bereits einigermaßen sauberes, DI'tes oder amp-simuliertes Bass-Signal — es ist selbst kein vollständiger Amp-Sim. Seine drei Bänder machen jeweils einen wirklich unterschiedlichen Job: das Low Band hält den Grundton-/Sub-Content per Parallel-Kompression fest unter einer Wand verzerrter Gitarren; das Mid Band fügt einen eigenen „throatigeren" Sättigungscharakter im Bereich hinzu, der am ehesten mit Gitarren kollidiert; das High Band verleiht mit seinem Voicing den Grind in den oberen Mitten/Höhen, der Bass durch eine dichte Mischung schneiden lässt.

Typische Anwendungsfälle: moderner, schaltungsmodellierter Grind, klassisches/Vintage-Voicing, Cab-eingefärbter Ton über den eingebauten IR-Loader (nur Mid+High-Pfad — das Low Band umgeht ihn immer), und definitionsfokussierte Settings für einen Bass, der gehört werden muss, ohne zu dominieren.

## Quick-Start-Einstellungen

### Moderne schaltungsmodellierte Grundlage — *Circuit Foundation*, *Circuit Grind*

Circuit Foundation: Drive Engine **Circuit**, Low Comp Detector **Smooth RMS**, Gate Mode **Modern**, Split Low 110 Hz, Split High 700 Hz, Low Comp Threshold −20 dB/Ratio 3:1/Mix 70 %, Mid Drive 25 %, High Voicing Razor, High Bias 15 %.

Circuit Grind: dieselben Engine-Wahlen, engerer Split Low (130 Hz)/höherer Split High (550 Hz — schmaleres Mid Band), Low Comp Mix 85 %, Mid Drive 55 %, High Voicing Wool, High Drive 75 %, High Bias 45 %.

Die Circuit-Engine baut den Mid/High-Drive aus Schaltungsmodellen neu statt aus einer Kurve pro Voicing — 25–30 dB bessere Alias-Unterdrückung als Classic, und Per-Voicing-Pre-/Post-Emphasis-Netzwerke, die jedem Voicing (Gnaw/Wool/Razor) einen wirklich unterschiedlichen Charakter geben statt drei Einstellungen derselben Form. Smooth-RMS-Detection am Low Band behebt speziell das Tremolieren bei anhaltenden tiefen Noten, das der Classic-Peak-Detektor erzeugen kann.

### Klassisches/Vintage-Voicing — *Cab-Colored Grind*, *Clean Low, Loud Top*

Cab-Colored Grind: Drive Engine Classic, Split Low 120 Hz, Split High 600 Hz, Mid Drive 35 %, High Voicing **Wool**, High Drive 60 %, **IR-Loader an, IR Mix 70 %**.

Classic hält das Pre-v0.3.0-Mid/High-Band exakt bei — wer den alten Sound bevorzugt oder Session-Kompatibilität will, bekommt hier den exakten Codepfad, keine Näherung.

### Cut-Through-Definition — *Cut Through*, *Definition Only*

Cut Through: Split Low 180 Hz, Split High 900 Hz (breites Mid Band), Mid Drive 40 %, High Voicing Razor, High Drive 55 %.
Definition Only: Mid Drive 20 % (leichte Hand), High Voicing Razor, High Tight 250 Hz (tight), **EQ an, Peak 2 bei 2800 Hz +3 dB** (Presence-/Definition-Anker).

Definition Only stützt sich auf das Peak-2-Band der Post-Sum-EQ statt auf mehr Drive — ein moderater High-Mid-Boost am „Presence/Definition"-Ankerpunkt bringt mehr fürs Durchschneiden einer Mischung als mehr Distortion, besonders bei einem Bass-Part, der hörbar bleiben muss, ohne zu dominieren.

### Sub-verankertes Low End — *Sub Lock*

Split Low 90 Hz (schiebt mehr Grundton ins Low Band), Split High 500 Hz, Low Comp Ratio 3:1/Attack 3 ms/Release 6 ms (schnell, glue-artig), Mid Drive 15 % (leicht), High Voicing Razor, High Drive 35 %.

Schneller Attack/Release am Low-Band-Kompressor ist die schnelle, sanfte „Glue"-Ballistik, die die eigenen sourced Werte der Referenzklasse nutzen — kein schwerer „New-York-Style"-Squash. Kombiniert mit einem niedrigen Split Low wird der Grundton fest verankert, während Mid-/High-Content vergleichsweise zurückhaltend bleibt.

### Volle Fuzz-Wand — *Fuzz Wall*

High Voicing Wool, High Drive 85 %, **High Blend 100 %**, Mid Drive 25 %.

Blend bei 100 % bedeutet, das High Band ist voll verzerrt, ohne sauberes Signal beigemischt — die aggressivste verfügbare Einstellung für dieses Band, anders als einfach nur Drive weiter hochzuziehen.

## Rezepte

1. **Den Grundton unter einer Gitarrenwand verankern.** Sub Lock als Basis, Low Comp Mix auf 100 %, falls der Grundton noch locker wirkt, Low Comp Auto Makeup an (Smooth-RMS-Engine), damit ein Threshold-Wechsel nicht auch den Gesamtpegel ändert. *Warum:* Das Low Band wird parallel komprimiert — das komprimierte Signal wird über Mix mit seinem eigenen unkomprimierten Selbst gemischt, statt es zu ersetzen —, was das Low End tight hält, ohne je gequetscht oder leblos zu klingen.

2. **Wo der „Throat" relativ zu den Gitarren sitzt.** Split High hochziehen, um das Passband des Mid Bands zu verbreitern, falls der Throat-Charakter mehr Raum braucht, bevor der Grind des High Bands übernimmt; runterziehen, um dem High Band früher mehr Content zu übergeben. *Warum:* Split Low und Split High sind Ton-Entscheidungen, nicht nur technische Crossover-Punkte — wo die Grenzen gezogen werden, entscheidet direkt, wie viel Körper im nur-komprimierten Low Band landet gegenüber dem Sättigungscharakter des Mid Bands gegenüber dem Grind des High Bands.

3. **Fuzz vs. Tightness am High Band, unabhängig vom Voicing.** **High Tight** als primären Regler nutzen, bevor zu Drive oder einem anderen Voicing gegriffen wird — Richtung 20-Hz-Boden für maximalen Fuzz, Richtung 500 Hz für einen tighteren, kontrollierteren Top-End. *Warum:* High Tight ist ein Pre-Drive-Hochpass, der vor jedem Voicing angewendet wird, ändert also, wie viel Low-Content die Nichtlinearität erreicht, egal welches der drei Voicings (Gnaw/Wool/Razor) gewählt ist — der eine Regler, der alle drei konsistent umformt.

4. **Intensität zurücknehmen, ohne den Charakter zu plätten.** Wenn ein High-Voicing zu extrem wirkt, erst **Blend** senken statt Drive. *Warum:* Blend steuert, wie viel vom verzerrten Signal mit dem sauberen High Band zurückgemischt wird — es zu senken hält den tatsächlichen harmonischen Charakter der Nichtlinearität bei geringerer Gesamtintensität intakt, während Drive zu senken stattdessen den Charakter der Distortion selbst ändert, nicht nur, wie viel davon zu hören ist.

5. **Cab-eingefärbter Ton ohne separates Cab-Sim-Plugin.** Cab-Colored Grind als Basis, eine IR in den eingebauten Loader laden, IR Mix nach Gehör. *Warum:* Der IR-Loader prozessiert nur das Mid+High-Post-Sum-Signal — das Low Band durchläuft ihn strukturell nie, passend zur „Low Band umgeht den Cabsim"-Architektur, die Grundton-/Sub-Content unabhängig von der geladenen Cab-IR uneingefärbt hält.

> **Theorie — warum das Low Band parallel statt einfach komprimiert wird.** Ein Bass-Grundton unter einer Wand verzerrter Gitarren hat zwei konkurrierende Bedürfnisse: Er muss pegel-mäßig fest verankert bleiben (kein Wandern, kein hörbares Pumpen), und er muss seinen natürlichen Attack und sein Gewicht behalten, damit er nicht gequetscht oder leblos wirkt. Ein einzelner Kompressor in Serie kann immer nur das eine gegen das andere eintauschen — mehr Kontrolle kostet mehr Leben. Parallel-Kompression umgeht diesen Tausch: Der Kompressor des Low Bands läuft auf einer Kopie des Signals, und diese komprimierte Kopie wird über Mix *unter* das unkomprimierte Original gemischt, statt es zu ersetzen. Bei mittleren Mix-Werten bekommt man die Kontrolle, die das komprimierte Signal liefert, geschichtet unter die Dynamik und den Transientencharakter, die das trockene Signal schon hatte — deshalb kann Cryptas Low Band den Grundton unter einer dichten Mischung verankern, ohne die „atmende" oder „tote" Qualität, die ein stark komprimierter Single-Path-Bass oft hat.

## Fallstricke

- **Das Wool-Voicing der Circuit-Engine blüht auf, statt zu sacken.** Das ursprüngliche Design sagte voraus, dass eine laute Passage eine folgende leise Probe unterdrücken würde („Sag"); tatsächlich liefert es stattdessen einen abklingenden Bloom — real, verstanden, authentisches Analog-Verhalten (asymmetrisches Clipping erzeugt echten DC-Anteil, den ein nachgeschalteter Blocker über seine eigene Zeitkonstante wieder herstellt), aber beschreib es als history-dependent/anschlagsdynamisch, nicht als „Sag".
- **Classic- und Circuit-Engine sind bei Drive 0 oberhalb von 3 kHz nicht identisch** — Parität hält bis 3 kHz auf ±0,5 dB, aber Circuit läuft darüber bis zu 2,5 dB heller, weil sein Ton-Tiefpass bei der oversampleten Rate läuft und der bilinearen Frequenzverzerrung entgeht. Das ist offengelegt, kein zu umgehender Bug.
- **Der Safety Clip tauscht bei extremer Übersteuerung seinen Antialiasing-Vorteil gegen die Ceiling-Garantie ein** — etwa 10 dB oder mehr über der Ceiling verschlechtert sich die Transparenz zugunsten der harten Begrenzung. Beim Tracking/Mixen aus lassen; es ist ein Sicherheitsnetz für unerwartete Automation oder einen heißen Input, nicht Teil des beabsichtigten Tone-Shaping-Pfads.
- **Es gibt noch keinen In-Plugin-IR-Browser oder mitgelieferte Werks-Cabinet-IRs** — die Convolution-Engine selbst ist vollständig implementiert und garantiert bit-exakt durchgereicht, wenn nichts geladen ist, aber eigene IR-Dateien werden gebraucht.
- **Plattformübergreifende Bit-Exaktheit wird nicht behauptet.** macOS ist die goldene Plattform; Windows-Renders können bei Material, wo der Detektor von Gate oder Low-Band-Kompressor genau an einem Threshold sitzt, bis zu −60 dB relativ abweichen, da ein winziger numerischer Unterschied dort einen Übergang um ein Sample verschieben kann.
- **Die Circuit-Voicing-Konstanten sind ingenieursmäßig abgeleitete Ausgangspunkte, noch nicht nach Gehör gegen Referenzmaterial finalisiert** — der offene Ear-Tuning-Prozess der Suite gilt weiterhin für sie.
- **Es wird keine CPU-Zahl veröffentlicht oder behauptet.** Das Zusammenlegen zweier Oversampling-Regionen zu einer in der Circuit-Engine finanziert die zusätzliche Per-Voicing-Filterung, angegeben als etwa das, was die vorherige Engine kostete — aber keine Prozentzahl wird gemessen oder genannt.
- **Die GUI ist ein funktionaler generischer Editor mit einer schlichten Meter-Anzeigezeile** — die photorealistische GUI folgt als späterer Meilenstein.
