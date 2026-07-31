# Overture — Praxis-Guide

*Praxisnahe Einstellungen für die Preamp-Tightening-/Boost-Stufe, verankert in den Werkspresets.*

## Wo es hingehört

Overture ist eine Preamp-Tightening-/Boost-Stufe — das Plugin-Äquivalent des kleinen Pedals, das ein Metal-Gitarrist **vor** einen High-Gain-Amp schaltet, keine eigenständige Distortion (auch wenn man es dazu treiben kann). Die zwei Aufgaben sind getrennt und beide zählen: Low End aus dem Signal entfernen, *bevor* irgendetwas clippt, damit Palm Mutes und Chugs auf tiefen Saiten straff bleiben statt zu Brei zu werden, sobald die nächste Stufe ihren Gain sättigt; und einen kontrollierten, voiced Drive-Charakter obendrauf legen.

Typische Anwendungsfälle:

- **Tightening-Stufe vor einem echten Amp oder Amp-Sim** (Overture → Tenebrae oder jede andere High-Gain-Quelle) — der primäre Anwendungsfall, und wo die meisten Werkspresets leben.
- **Eine echte, eigenständige Distortion-Quelle**, stärker angeschoben, für ein reines Boost-Rig in einen cleanen Amp.
- **Ein parallel gemischter Ton**, unter eine clean DI gemischt statt zu 100 % wet gefahren.

## Quick-Start-Einstellungen

### Straffen eines tiefgestimmten Rhythmus-Parts — *Drop-Tune Tight*

Tight 220 Hz, Drive 4 dB, Voicing Asymmetric, Bite 80 %, Knee Soften 30 %, Asymmetry 40 %, Bite Tilt −10 %, Mix 100 %.

Tight wird deutlich über den 100-Hz-Default hinaus aufgedreht, weil eine tiefgestimmte tiefe Saite ihren brauchbaren Grundton weiter oben trägt als bei Standardstimmung — 220 Hz entfernt genug Low End vor dem Clipper, damit Palm Mutes artikuliert bleiben statt auszufransen. Bite bei 80 % macht den Clipper selbst zusätzlich frequenzselektiv, sodass das wenige Low End, das ihn erreicht, immer noch weniger clippt als die Höhen.

### Klassischer „808-vor-dem-Amp"-Push — *Classic Boost* / *Clean Push*

Tight 100 Hz, Drive 1–3 dB, Voicing Asymmetric, Bite 65 %, Knee Soften 40 %, Bite Tilt 0 %.

Das ist die am besten dokumentierte Version der Technik: Drive bleibt nahe null, der Clipper greift kaum ein — Level und die eigene Gain-Stufe des Amps übernehmen die eigentliche Verzerrung. Hier ansetzen, bevor du zu mehr Drive greifst — das ist das Referenzverhalten, um das herum das Plugin voiced wurde.

### Eigenständige Distortion / Fuzz-Adjacent Lead — *Own Distortion*, *Fuzz-Adjacent Lead*

Own Distortion: Tight 120 Hz, Drive 22 dB, Voicing Hard Clip, Bite 40 %, Knee Soften 60 %, Bite Tilt +10 %.
Fuzz-Adjacent Lead: Tight 150 Hz, Drive 30 dB, Voicing Hard Clip, Bite 25 %, Knee Soften 70 %, Bite Tilt +25 %, Level +3 dB.

Hard Clip hat bei keinem Drive-Level einen eigenen weichen Knee — Knee Soften leistet hier echte Arbeit und rundet ab, was sonst eine gerade Kappung wäre. So hart angeschoben, hört Overture auf, eine Tightening-Stufe zu sein, und wird zur Hauptverzerrungsquelle — ein legitimer, unterstützter Einsatz, nur mit anderem Charakter als die Presets oben.

### Schaltungsgelöster Programmpegel-Clipper — *Circuit Drive*

Tight 120 Hz, Drive 12 dB, Voicing Feedback, Bite Amount/Knee Soften wirkungslos, Asymmetry 25 %, Bite Tilt −8 %, **Level −9 dB**.

Das Feedback-Voicing läuft konstruktionsbedingt heiß (siehe Theorie-Box unten) — der −9-dB-Level-Trim dieses Presets ist der geprüfte Ausgangspunkt, keine willkürliche Wahl. Starte hier statt von deinem aktuellen Patch aus, wenn du dieses Voicing zum ersten Mal auditierst.

### Paralleler/gemischter Rhythmus-Ton — *Parallel Grit*

Dieselben Kern-Settings wie Classic Boost, aber **Mix 35 %** statt 100 %. Mischt eine kleine Menge gestrafftes, angeschobenes Signal unter eine clean DI für einen hybriden Ton, statt Overture voll in der Kette laufen zu lassen.

## Rezepte

1. **Tiefgestimmtes Chug-Tightening.** Tight 180–220 Hz, Drive 4 dB, Voicing Asymmetric, Bite 80 %, Gate an mit Threshold um −45 bis −50 dB und Release auf Auto. *Warum:* Tight so weit hochzudrehen entfernt Low End, bevor Tenebraes eigene Kaskade die Chance hat, es auf einer tiefen Saite zu Matsch zu sättigen; das eingebaute Gate (ganz vorne in der wet Chain, ohne zusätzliche Latenz) hält Brummen und Rauschen davon ab, den Clipper überhaupt zu erreichen.

2. **Lead-Boost mit eigenem Charakter, getrennt vom Rhythmus-Ton.** Starte bei Fuzz-Adjacent Lead (Tight 150 Hz, Drive 30 dB, Hard Clip, Bite Tilt +25 %), zieh dann eher Drive zurück, wenn es brüchig klingt, statt zuerst mehr Bite Tilt zu greifen. *Warum:* Positiver Bite Tilt hellt oberhalb der ~3-kHz-Ecke auf — nützlich, damit ein Lead durch eine dichte Mischung schneidet —, aber ein so hart angeschobener Clipper erzeugt schon selbst reichlich Höhen; erst Drive zu zähmen hält die Helligkeit gewollt statt hart.

3. **Eigenständiges Distortion-Rig vor einem cleanen Amp.** Own Distortion oder Fuzz-Adjacent Lead als Ausgangspunkt, Voicing auf Hard Clip, Level zurückgezogen, um den zusätzlichen Gain auszugleichen. *Warum:* Hard Clip ist das hellste und aggressivste der gedächtnislosen Voicings — näher an einem Fuzz-/Komparator-artigen Clip als das amp-anschiebende Asymmetric-Voicing —, was es als eigenständige Distortion statt nur als Boost funktionieren lässt.

4. **Anschlagsdynamischer Circuit-Drive.** Circuit-Drive-Preset als Basis (Voicing Feedback, Level −9 dB), dann Drive mit der eigenen Anschlagsdynamik statt einem statischen Wert reiten. *Warum:* Das Feedback-Voicing löst Sample für Sample eine echte Feedback-Schleife statt eine feste Kurve auszuwerten, sodass Gain, Knee und Höhenrundung sich alle gemeinsam damit bewegen, wie hart du anschlägst — eine feste Transferkurve kann diese Anschlagsdynamik bei keinem Oversampling-Faktor reproduzieren.

5. **Paralleler Blend unter einer clean DI.** Parallel Grit als Ausgangspunkt (Mix 35 %), Tight und Drive wie bei Classic Boost. *Warum:* Ein gemischter Ton braucht sein Gating woanders — Overtures eingebautes Gate wirkt konstruktionsbedingt nur auf den wet Pfad, sodass das darunter gemischte trockene Signal zwischen den Noten voll hörbar bleibt.

> **Theorie — warum ein schaltungsgelöster Clipper sich anders verhält als eine Transferkurve.** Die meisten Clipper, darunter drei von Overtures vier Voicings, werten eine feste Input-zu-Output-Form aus: Sample rein, geformtes Sample raus, ohne Erinnerung daran, was davor war. Das Feedback-Voicing ist anders gebaut — es löst die tatsächliche Op-Amp-/Dioden-/RC-Feedback-Schleifen-Gleichung einmal pro Sample, mit derselben numerischen Methode (Trapezregel mit Newton-Iteration), die ein Ingenieur nutzen würde, um eine echte Schaltung offline zu lösen. Der praktische Unterschied ist Gedächtnis: Ein kleiner Feedback-Kondensator legt einen drive-abhängigen Tiefpass-Pol *in* die Nichtlinearität selbst, sodass Gain, Knee und Höhenrundung der Stufe sich alle gemeinsam damit bewegen, wo Drive steht und wie hart das Signal reintrifft. Kein gedächtnisloser Waveshaper — egal wie fein seine Kurve getuned ist — reproduziert das, weil die Kurve kein Konzept von „vor einem Moment" kennt.

## Fallstricke

- **Die fünf v0.3.0-Parameter (Gate, Gate Threshold, Gate Release, Knee Response, Clip Quality) haben noch keine eigenen Regler im Editor** — nutze die generische Parameter-Ansicht deines Hosts (Logics „Controls"-View, Reapers FX-Parameterliste, Lives Plugin-Parameterliste), um sie zu automatisieren, bis die M3-GUI kommt.
- **Wenn du das Voicing-Menü automatisiert hast, prüfe diese Automations-Spur nach einem Update.** Presets und Sessions speichern das Voicing als Index und laden korrekt, aber eine Host-Automations-Spur speichert einen normalisierten 0-1-Wert — eine Spur, die früher „Hard Clip" bedeutete (2 von 2 Optionen), bedeutet jetzt „Feedback" (3 von 3).
- **Ein Voicing-Wechsel ist ein diskreter Sprung, kein Crossfade** — wie ein Stompbox-Toggle, erwarte einen hörbaren Sprung im Moment des Umschaltens, automatisiere es nie sanft in Erwartung einer Überblendung.
- **Ein Oversampling-Wechsel ist nicht sofort wirksam.** Er greift erst, wenn dein Host das Plugin das nächste Mal neu initialisiert (Transport-Stop/Start, Samplerate-Wechsel, erneutes Öffnen des Projekts) — eine bewusste Echtzeit-Sicherheitsentscheidung, da die Neukonfiguration des Oversamplers eine Speicherallokation braucht, die nie auf dem Audio-Thread passieren darf.
- **Das Feedback-Voicing ist konstruktionsbedingt laut** — sein linearer Bereich endet bei Drive 0 um −40…−35 dBFS, eine normale −12-dBFS-Spur treibt es also hart an. Zieh Level herunter, bevor du es auditierst — geh nicht davon aus, dass es sich bei Unity Gain wie ein cleaner Boost verhält.
- **Das Gate wirkt ausschließlich auf den wet Pfad.** Mix unter 100 % lässt weiterhin das ungegatete trockene Signal darunter durch — erwartetes Verhalten, bedeutet aber, dass ein Parallel-Blend-Patch sein Rauschen woanders behandeln muss.
- **Das Voicing ist durchgehend aus veröffentlichten Schaltungsanalysen und dokumentierten Workflows abgeleitet, nicht gegen physische Referenz-Hardware gemessen.** Behandle die Parameterbereiche und Defaults als konstruierte Ausgangspunkte, nicht als Anspruch, den Klang eines bestimmten physischen Geräts zu treffen.
