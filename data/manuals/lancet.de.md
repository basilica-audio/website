<!-- German translation of lancet.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

# Lancet — Bedienungsanleitung

*Schneide, wo es zählt — ein chirurgischer Dynamic EQ mit analoger Seele.*

## Was ist neu in v0.3.0

Ein musikalischer Voicing-Pass (siehe `docs/voicing-notes.md`) — gemessen, wo die eigene DSP des Plugins eine Messung erlaubte, ehrlich als „nach Gehör, noch nicht gegen echtes Material abgestimmt" gekennzeichnet, wo nicht:

- **Per-Band-Defaults für Q/Threshold/Attack/Release, abgestimmt auf die dokumentierte Rolle jedes Bands** (vorher ein flaches Q 1.0/Threshold -30 dB/Attack 5 ms/Release 150 ms für jedes Band): Band 1 (100 Hz, Boom/Sub-Kontrolle) startet jetzt langsam und sanft (Attack 25 ms/Release 280 ms); Band 5 (4 kHz, Zischlaute/Härte) startet schnell (Attack 2 ms/Release 70 ms); die Bänder dazwischen stufen sich progressiv ab. Range startet weiterhin bei 0 dB (in Ruhe) für jedes Band — es bewegt sich nichts, bevor du eine Range einstellst, aber sobald du das tust, reagiert jedes Band jetzt so, wie es seine Rolle nahelegt. Siehe die aktualisierte Per-Band-Tabelle unten.
- **Gentle Saturation** (`bN_sat`, neuer Toggle pro Band, standardmäßig aus): ist er aktiviert, wird ein sanfter, `tanh`-basierter Waveshaper auf ein Band angewendet, aber *nur*, während es aktiv boostet (Gain + der dynamische Beitrag von Range netto positiv) — ein schneidendes oder ruhendes Band bleibt völlig unberührt, auch mit aktivierter Saturation. In v0.3.0 per Automation/Preset steuerbar; ein dedizierter Editor-Toggle ist Roadmap M3, genau wie Auto Release/Gain-Q.
- **Ein zehntes Werkspreset, „Analog Warmth Lift"** (`docs/presets.md`): demonstriert den neuen Saturation-Toggle an einem sanften Low-Mid-Boost.
- Eine v0.2.0-Session lädt sauber in v0.3.0 (toleranter Import): Jeder bestehende Parameterwert bleibt exakt erhalten, und der neue Saturation-Toggle pro Band wird mit seinem Aus-Standardwert befüllt.

## Was ist neu in v0.2.0

Ein recherchebasiertes Deep-Dive-Rework (siehe `docs/design-brief.md`/`docs/research-notes.md`), das M2-Preset-System der Suite sowie eine deutsche Interface-Lokalisierung:

- **Programmabhängiges Auto Release** (`bN_autoRelease`, neuer Toggle pro Band, standardmäßig aus): Ist es aktiviert, verkürzt sich die *effektive* Release-Zeit eines Bands automatisch — nie langsamer als die manuelle Release-Einstellung —, wenn die eigene Hüllkurve des Signals bereits von selbst abfällt (z. B. bei einem natürlich abklingenden Transienten), inspiriert von (nicht eine Nachbildung von) dem in F6-Klasse-Dynamic-EQs dokumentierten „ARC"-artigen Release-Verhalten. In v0.2.0 per Automation/Preset steuerbar; ein dedizierter Editor-Toggle ist für Roadmap M3 vorgesehen.
- **Gain/Q-Kopplung** (`bN_gainQ`, neuer Toggle pro Band, standardmäßig aus): Ist sie aktiviert, wird das eigene Filter-Q eines Bands proportional dazu weicher (breiter), wie stark sich sein dynamisches Gain gerade bewegt — für einen sanfteren, analogeren Charakter bei tieferen dynamischen Bewegungen. Das *statische* Gain des Bands beeinflusst Q nie, nur seine dynamische Komponente tut das. Gleicher Automations-/Preset-only-Status wie Auto Release in v0.2.0.
- **Attack-/Release-Bereiche erweitert**: Attack jetzt 0.1 bis 500 ms (vorher 0.5 bis 100 ms), Release jetzt 5 bis 1500 ms (vorher 10 bis 1000 ms) — an beiden Enden, für sowohl schnelleres Transienten-Einfangen als auch langsamere, musikalische Tonalausgleichs-Anwendungsfälle.
- **Die Knee-Breite wird jetzt von Range abgeleitet**, statt einer festen 6-dB-Konstante — flachere Range-Einstellungen wirken jetzt sanfter/weicher, Range-Einstellungen mit voller Tiefe (±12 dB) klingen identisch zum festen 6-dB-Knee von v0.1.0.
- **Neun Werkspresets** (`docs/presets.md`) für gängige Anwendungsfälle (Glue, De-Essing, Transientenverstärkung, Mix-Bus-Beruhigung, langsamer Tonalausgleich, Resonanz-Zähmung und eine diagnostische Auto-Release-Demo), plus eine Preset-Leiste (Save/Save As/Delete/Import/Export, Werks- + Nutzer-Bibliothek) am oberen Rand des Editors.
- Eine v0.1.0-Session lädt sauber in v0.2.0 (toleranter Import): Jeder bestehende Parameterwert bleibt exakt erhalten, und die beiden neuen Toggles pro Band werden mit ihrem Aus-Standardwert befüllt.

## Was es ist

Lancet ist ein Six-Band Dynamic EQ im Geiste der Waves-F6-Klasse — hier als dokumentierter Referenzpunkt für die Kategorie genannt, ohne eine Empfehlung, ein Sponsoring oder eine Zugehörigkeit durch Waves Audio Ltd. zu implizieren. Jedes Band ist ein normales parametrisches EQ-Band (Bell, oder Shelf bei Band 1/Band 6), dessen Gain sich zusätzlich mit dem Programmmaterial bewegen kann. Fütterst du es laut, reagiert es — schneidet eine Resonanz nur, wenn sie aufflammt, oder öffnet einen Boost nur, wenn ein Part untergeht — und pendelt sich dann wieder auf seine statische Einstellung ein, sobald der Pegel wieder fällt. Da die dynamische Bewegung jedes Bands von seinem *eigenen*, vor dem EQ sitzenden, bandgefilterten Detector angetrieben wird, verwirrt der Cut eines Bands nie den Detector eines anderen, und die eigene Gain-Bewegung eines Bands beeinflusst nie seine eigene Erkennung.

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
| **Q** | 0.3 - 12 | 0.9 / 1.1 / 1.0 / 1.2 / 1.4 / 1.0 (v0.3.0, pro Band — siehe Tabelle unten) | | Wie schmal (hohes Q) oder breit (niedriges Q) das Band ist. **Wird im Shelf-Modus ignoriert**, der unabhängig von dieser Einstellung immer eine feste, standardmäßige Shelf-Flanke nutzt (Q = 0.707). |
| **Gain** | -12 - +12 | 0 | dB | Das *statische* Gain des Bands — immer angewendet, dynamisch oder nicht. Setze das auf deine „Ruhe"-EQ-Bewegung; Range addiert oder subtrahiert dann obendrauf, wenn der Detector auslöst. |
| **Range** | -12 - +12 | 0 | dB | Wie weit sich das Gain des Bands dynamisch bewegen kann, zusätzlich zu Gain. **0 = ein rein statisches EQ-Band** (kein Detector-Einfluss). Negatives Range schneidet, wenn das Signal lauter als Threshold wird (die klassische Resonanz-Zähmung/De-Essing-Bewegung); positives Range boostet, wenn es lauter wird (eine aufwärtsgerichtete „Duck-in"-Expansions-Bewegung, nützlich z. B. um Anschlag nur bei hart gespielten Noten hervorzuheben). |
| **Thresh** | -60 - 0 | -26 / -28 / -26 / -24 / -22 / -20 (v0.3.0, pro Band — siehe Tabelle unten) | dB | Der Detector-Pegel, ab dem die dynamische Bewegung einsetzt. Ein Soft-Knee, zentriert auf diesen Wert, macht den Übergang graduell statt zu einem harten Schalter — die Breite des Knees selbst skaliert mit Range (v0.2.0): `clamp(\|Range\| * 0.5, 2, 10)` dB, sodass flachere Range-Einstellungen sanfter wirken und Range-Einstellungen mit voller Tiefe (±12 dB) identisch zum festen 6-dB-Knee von v0.1.0 klingen. |
| **Attack** | 0.1 - 500 | 25 / 15 / 8 / 4 / 2 / 3 (v0.3.0, pro Band — siehe Tabelle unten) | ms | Wie schnell sich das dynamische Gain bewegt, sobald der Detector den Threshold überschreitet. Schneller Attack erwischt Transienten hart; langsamerer Attack lässt einen kurzen Peak durch, bevor reagiert wird, was bei perkussivem Material natürlicher klingen kann. Die 500-ms-Obergrenze ist für langsame, musikalische Tonalausgleichs-Bewegungen gedacht, nicht für das Einfangen von Transienten. |
| **Release** | 5 - 1500 | 280 / 180 / 130 / 100 / 70 / 90 (v0.3.0, pro Band — siehe Tabelle unten) | ms | Wie schnell das dynamische Gain zurück Richtung Gain kehrt, sobald der Detector wieder unter den Threshold fällt. Schneller Release kann bei anhaltendem Material hörbar pumpen; langsamer Release glättet die Rückkehr, kann aber einen Cut/Boost in Inhalt hineinhalten, der ihn nicht mehr braucht. |
| **Listen** | Off / On | Off | | Solot das eigene Detector-Signal dieses Bands — das bandpassgefilterte Audio vor dem EQ, das tatsächlich seine dynamische Bewegung antreibt — anstelle des normalen Programm-Outputs, um genau zu hören, was es auslöst. Exklusiv: Aktivierst du Listen bei einem Band, deaktiviert das automatisch Listen bei jedem anderen Band. Die vollständige Signalkette (inklusive der Verarbeitung jedes einzelnen Bands) läuft darunter weiter, sodass das Deaktivieren von Listen nie knackt. |
| **Auto Release** (v0.2.0) | Off / On | Off | | Programmabhängiges Auto-Release: Ist es aktiviert, verkürzt sich die *effektive* Release-Zeit für einen gegebenen Übergang automatisch (nie unter die eigene 5-ms-Release-Untergrenze des Plugins, nie über die manuelle Release-Einstellung selbst hinaus), sobald die eigene Hüllkurve des Signals bereits von selbst abfällt — nützlich, um ein Band bei natürlich abklingendem Material schneller entspannen zu lassen, ohne für anhaltendes Material auf einen langsameren, musikalischen manuellen Release zu verzichten. In v0.2.0 nur per Automation/Preset — noch kein dedizierter Editor-Regler (Roadmap M3). |
| **Gain/Q** (v0.2.0) | Off / On | Off | | Gain/Q-Kopplung: Ist sie aktiviert, verbreitert (weicht) sich das eigene Filter-Q des Bands proportional dazu, wie weit sein *dynamisches* Gain gerade in Richtung Range steht — ein sanfterer, analogerer Charakter bei tieferen dynamischen Bewegungen. Das statische Gain beeinflusst Q nie, nur die dynamische Komponente tut das. In v0.2.0 nur per Automation/Preset — noch kein dedizierter Editor-Regler (Roadmap M3). |
| **Saturation** (v0.3.0) | Off / On | Off | | Sanftes Waveshaping: Ist es aktiviert, wird ein sanfter, `tanh`-basierter Drive auf den eigenen Output des Bands angewendet, aber nur, während es aktiv boostet (Gain + der dynamische Beitrag netto positiv) — ein schneidendes oder ruhendes Band bleibt unberührt, auch damit aktiviert. Der Drive skaliert damit, wie stark das Band gerade boostet (kaum wahrnehmbar nahe 0 dB, deutlich hörbar, aber weiterhin soft-knee-geformt nahe +12 dB). In v0.3.0 nur per Automation/Preset — noch kein dedizierter Editor-Regler (Roadmap M3). |

Per-Band-Voicing-Defaults (v0.3.0, `docs/voicing-notes.md`) — abgestimmt auf die
typische Rolle jedes Bands entlang der bestehenden Frequenzleiter, kein flacher
Wert, der über jedes Band hinweg wiederholt wird:

| Band | Freq | Rolle | Q | Threshold | Attack | Release |
|---|---|---|---|---|---|---|
| 1 | 100 Hz (Low Shelf) | Boom-/Sub-Kontrolle | 0.9 | -26 dB | 25 ms | 280 ms |
| 2 | 250 Hz | Mulm-/Boxiness-Resonanz (Vocal & Gitarrenkörper) | 1.1 | -28 dB | 15 ms | 180 ms |
| 3 | 630 Hz | Allgemeine Mitten-Präsenz (standardmäßig aktives Demo-Band) | 1.0 | -26 dB | 8 ms | 130 ms |
| 4 | 1600 Hz | Vocal-Präsenz / Gitarren-Schärfe | 1.2 | -24 dB | 4 ms | 100 ms |
| 5 | 4000 Hz | Zischlaute / Anschlag / Härte | 1.4 | -22 dB | 2 ms | 70 ms |
| 6 | 10000 Hz (High Shelf) | Luft / Fizz-Erholung | 1.0 | -20 dB | 3 ms | 90 ms |

### Global

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Input Trim** | -12 - +12 | 0 | dB | Gain, das vor Band 1 angewendet wird — und bevor der Detector jedes Bands das Signal anzapft, verschiebt es also auch, welcher Pegel den Threshold jedes Bands erreicht. |
| **Output Trim** | -12 - +12 | 0 | dB | Gain, das nach Band 6 und nach der Mix-Blende angewendet wird — die finale Gain-Stufe, um den Ausgangspegel von Lancet an das anzupassen, was als Nächstes in der Kette folgt. |
| **Mix** | 0 - 100 | 100 | % | Paralleler Dry/Wet-Blend der gesamten Six-Band-Kette. 100 % ist vollständig prozessiert; niedrigere Werte mischen zunehmend mehr vom unbearbeiteten (aber weiterhin Input-getrimmten) Signal bei — nützlich für „New-York"-artiges paralleles Dynamic EQing, bei dem die Korrektur hinzufügen statt vollständig ersetzen soll. |

## Presets (v0.2.0)

Am oberen Rand des Editors sitzt eine Preset-Leiste: `[<] [Preset Name] [>]`, um alphabetisch durch die Werks- und Nutzer-Bibliothek zu blättern, `Save`/`Save As...`, um eigene Presets zu schreiben, `Delete` für Nutzer-Presets, `Import.../Export...` für einzelne `.basilicapreset`-Dateien oder `.zip`-Bänke, sowie ein Menü (Klick auf den Preset-Namen) mit einem Eintrag „Set current as default" für deinen eigenen Out-of-the-Box-Startpunkt. Neun Werkspresets werden mit v0.2.0 ausgeliefert — was jedes davon bewirkt und warum, steht in `docs/presets.md`. Nutzer-Presets werden pro Nutzer unter `~/Library/Audio/Presets/Yves Vogl/Lancet/` auf macOS gespeichert (`%APPDATA%/Yves Vogl/Lancet/Presets/` unter Windows).

Die Interface-Texte des Editors (Preset-Leisten-Beschriftungen, Menüs, Dialoge) werden automatisch auf Deutsch lokalisiert, wenn die Systemsprache Deutsch ist; Parameternamen, Einheiten und Fachbegriffe (Attack, Release, Hz, dB, ms, …) bleiben immer auf Englisch — genau wie bei jedem anderen Basilica-Audio-Plugin.

## Tipps

- **Setze Gain und Range getrennt und bewusst.** Gain ist das, was das Band *immer* tut; Range ist das, was es *zusätzlich* tut, nur wenn ausgelöst. Ein Band mit Gain=0, Range=-6 ist in Ruhe unhörbar und schneidet nur, wenn die Resonanz aufflammt — ganz anders als Gain=-3, Range=-3, das immer ein bisschen schneidet und bei Auslösung noch härter schneidet.
- **Nutze Listen, um das Problem zu finden, bevor du Threshold setzt.** Fahre Freq/Q mit aktiviertem Listen durch, bis du die Resonanz oder Härte klar isoliert hörst, *dann* setze Threshold knapp über den Pegel, den sie hat, wenn sie kein Problem ist — das ist deutlich zuverlässiger, als einen Threshold-Wert gegen den vollen Mix zu erraten.
- **Schmale, high-Q-Bänder mit negativem Range sind das klassische Resonanz-Zähmungs-Setup** (ein dumpfer 300–500-Hz-Aufbau, eine harte 2–4-kHz-Plektrum-/Rohrblatt-Kante, ein sibilantes 6–8-kHz-De-Esser-Band). Halte Q hoch genug, dass der Cut den umgebenden Ton nicht hörbar ausdünnt, wenn er einsetzt.
- **Breite, low-Q-Bänder mit negativem Range ergeben eine sanftere, breitere dynamische Klangkontrolle** — nützlich auf einem Mix-Bus, um ein ganzes Register zu zähmen (z. B. „die Low-Mids werden etwas zu viel, wann immer die ganze Band gemeinsam zuschlägt"), ohne die chirurgische Enge eines De-Esser-artigen Bands.
- **Positives Range (aufwärts/Duck-in) ist die weniger naheliegende Bewegung** — probiere es auf einem low-Q-Hochfrequenzband, um Anschlag oder Atem-/Konsonanten-Details nur bei den Noten hervorzuholen, die es brauchen, statt ständig das ganze Register (und seinen Rauschteppich) zu boosten.
- **Schneller Attack + schneller Release können bei anhaltendem Material hörbar pumpen** (Bass, Flächen, gehaltene Vocal-Noten) — klingt ein Band instabil oder „atmend", versuche zuerst einen langsameren Release, bevor du zu einem schmaleren Q greifst.
- **Mix unter 100 % erhält den Charakter der dynamischen Bewegung, während ihre Tiefe reduziert wird** — ein schneller Weg, eine übertrieben aggressive Range-Einstellung zurückzunehmen, ohne Threshold/Range jedes Bands von Grund auf neu einzustellen.
