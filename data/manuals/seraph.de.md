<!-- German translation of seraph.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Seraph-Icon" width="120"/></p>

# Seraph — Bedienungsanleitung

*Stimmen von oben — ein Chor- und Vocal-Prozessor für Operatic-Metal-Vocals.*

## Was Seraph ist

Seraph ist ein Vocal-Prozessor im Channel-Strip-Stil, gebaut für die Lead- und Chor-Vocal-Parts von Operatic Metal (große, cineastische Produktionen): eine Sopran-Leadlinie, ein geschichtetes Chor-Backing oder ein gesprochenes/gegrowltes Zwischenspiel, das sich sauber gegen schwer geschichtete Gitarren und ein Orchester behaupten muss, ohne zu verschwinden oder hart zu klingen.

Es vereint vier Processing-Stufen, zu denen man bei einem Vocal normalerweise separat greifen würde:

1. **De-Ess** — zähmt Zischlaute („s", „sch", „t"-Konsonanten), die durch ein helles Vocal-Mikro und starkes Top-End-EQ an anderer Stelle im Mix (Becken, verzerrtes Gitarren-Fizz, Streichersektionen) tendenziell ermüdend werden.
2. **Air** — fügt das Gefühl luftiger Offenheit oberhalb des natürlichen Präsenzbereichs des Vocals hinzu (oder entfernt es) – die Art von Schimmer, die einem opernhaften Sopran hilft, sich gegen eine Wand aus Gitarren durchzusetzen.
3. **Gentle Compressor** — gleicht die Dynamik mit einem „Glue"-artigen Kompressor aus, sodass das Vocal auf einem konstanten Pegel im Mix sitzt, ohne hörbar zu pumpen.
4. **Doubler** — ein Vier-Stimmen-Vocal-Doubler, der einen einzelnen Take zu einer kleinen Chor-Fläche verdickt, in drei wählbaren Engines (siehe [Doubler-Modi](#doubler-modi) unten).

Alles bis Mix/Output ist ein einziger, in sich geschlossener Channel Strip: Setze Seraph auf einen Vocal- oder Chor-Bus, stelle De-Essing und Air nach Geschmack ein, füge bei dynamisch unruhigen Takes einen Hauch Glue-Kompression hinzu, und nutze den Doubler, um eine Leadlinie zu verbreitern oder einen Chor-Part zu verdicken.

## Wo es in einer Heavy-Music-Signalkette sitzt

Seraph ist dafür gedacht, auf Vocal-/Chor-Spuren oder einem Vocal-Bus zu laufen, typischerweise:

```
Vocal/choir recording -> (tuning/editing, if used) -> Seraph -> reverb/delay send -> mix bus
```

In seiner Default-Konfiguration meldet Seraph **0 Samples Latenz**, braucht also keine host-seitige Delay-Compensation-Berechnung und lässt sich gefahrlos an jeder Stelle einer Vocal-Kette einsetzen, auch parallel. Zwei Einstellungen ändern das bewusst — siehe [Latenz und Delay-Kompensation](#latenz-und-delay-kompensation).

Ein paar praktische Platzierungen in einer Heavy-Music-Produktion:

- **Lead-Vocal-Spur**: Zuerst De-Ess (Mikro-Nähe und Konsonanten), ein Hauch Air, damit eine opernhafte Stimme sich gegen verzerrte Gitarren und Orchesterstreicher durchsetzt, etwas Comp für Konsistenz, und eine *dezente* Menge Double (10–20 %), falls der Take mehr Fülle braucht, ohne künstlich gedoppelt zu klingen.
- **Chor-/Backing-Vocal-Bus**: kräftigeres Double (40–70 %) mit vollem Width für eine breite, geschichtete Chor-Fläche aus wenigen aufgenommenen Takes; De-Ess und Air konservativer eingestellt, da Chor-Blends pro Stimme meist bereits weniger zischend/hart klingen als ein Solo-Lead.
- **Gesprochenes/gegrowltes Zwischenspiel**: De-Ess ist oft unnötig (wenig Zischlaut-Energie in einer gegrowlten Performance); Air und eine stärkere Comp-Einstellung helfen einem gesprochenen Zwischenspiel, gegen ein leises orchestrales Backing präsent und pegelkonsistent zu bleiben.

## Signalfluss

```
input -> De-Ess (sibilance dynamic EQ, + Width/Knee/Link/Lookahead + Listen mode)
       -> Air (10/12/15 kHz high-shelf) -> Gentle Compressor (broadband glue, auto-release, + Link)
       -> Doubler (4 voices, per-voice pan, Classic/Micro/Shift + Humanize)
       -> Output trim -> Mix -> output
```

Das vollständige technische Signalfluss-Diagramm und die DSP-Design-Notizen findest du in [`architecture.md`](architecture.md); den recherchebasierten v0.2.0-Voicing-Pass hinter den Range-/Default-Werten unten findest du in [`design-brief.md`](design-brief.md).

## Presets

Seraph bringt eine Preset-Leiste mit, die oben im Plugin-Fenster andockt: Durchstöbere Werkspresets und eigene Presets über das Namensmenü, blättere mit den `<`/`>`-Pfeilen hindurch, und nutze Save/Save As.../Delete/Import.../Export..., um deine eigenen zu verwalten. Zwölf Werkspresets decken Lead-, Chor-, Spoken-Interlude- und Single-Stage-Utility-Anwendungsfälle ab — die vollständige Liste mit der Absicht hinter jedem Preset findest du in [`presets.md`](presets.md). „Set current as default" (im Preset-Namensmenü) legt fest, was beim nächsten Öffnen einer frischen Instanz von Seraph geladen wird. Eigene Presets werden pro Benutzer gespeichert (`~/Library/Audio/Presets/Yves Vogl/Seraph/` auf macOS) und lassen sich als einzelne Dateien exportieren/importieren oder als Bank teilen.

## Parameterreferenz

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **De-Ess** | 0-100 | 30 | % | Menge der Zischlaut-Gain-Reduction. Skaliert die maximale Reduction, die auf das erkannte Band angewendet wird (bis zu 24 dB bei 100 %). 0 % ist ein exakter Bypass des De-Essers. Starte niedrig (20–40 %) und erhöhe nur so weit wie nötig — übertriebenes De-Essing lässt „s"-Laute genuschelt oder gedämpft klingen. |
| **De-Ess Freq** | 3,000-12,000 | 7,000 | Hz | Mittenfrequenz des Zischlaut-Erkennungs-/Reduction-Bands. Weibliche/Sopran-Vocals zischen oft höher (7–9 kHz); tiefere männliche Vocals oder stark proximity-gemikte Takes brauchen eventuell 5–6 kHz. Nutze **De-Ess Listen**, um die richtige Frequenz nach Gehör zu finden. |
| **De-Ess Width** | 0-100 | 40 | % | Erkennungsbandbreite des Zischlaut-Bands. Niedrigere Werte verengen den Detektor auf reine „Ess"-Energie (chirurgischer, fängt seltener andere hochfrequente Inhalte mit ein); höhere Werte verbreitern ihn, um auch „sch"/hauchige/„woosh"-artige Zischlaute zu erfassen. Reagiert De-Ess auf den falschen Sound, probiere zuerst eine Anpassung von Width, bevor du zu De-Ess Freq greifst. |
| **De-Ess Listen** | off/on | off | - | Solot das erkannte Zischlaut-Band statt des bearbeiteten Vocals, sodass du De-Ess Freq/Width durchfahren und genau hören kannst, welches Frequenzband anvisiert wird, bevor du die Reduction einstellst. Vor dem Mischen wieder ausschalten — der Listen-Modus ist eine Einstellhilfe, keine Mix-Einstellung. |
| **Air** | -6 to +9 | +2 | dB | Fixes 12-kHz-High-Shelf mit weitem, sanftem Übergang (beginnt bereits deutlich vor der Eckfrequenz anzusteigen). Boost für Offenheit/Schimmer oberhalb des natürlichen Top-Ends eines Vocals (typisch für ein Lead, das sich gegen einen dichten Mix durchsetzen muss); Cut, wenn ein helles Mikro/Preamp oder aggressives De-Essing das Vocal dünn oder hart klingen lässt. |
| **Comp** | 0-100 | 0 | % | Menge eines sanften, breitbandigen Downward-Compressors mit programmabhängigem („auto") Release: erholt sich schnell nach einem isolierten lauten Moment, verklebt hörbarer während anhaltender lauter Passagen. Skaliert Threshold (bis -20 dBFS) und Ratio (bis 3:1) gemeinsam — eine „Glue"-Einstellung, kein quetschender Limiter. 0 % ist ein exakter Bypass. Es wird kein automatisches Makeup-Gain angewendet; nutze **Output** zum Ausgleich, falls eine höhere Comp-Einstellung das Vocal leiser wirken lässt. |
| **Double** | 0-100 | 25 | % | Doubler-Send-Menge: wie stark die vier gedoppelten Stimmen über dem zentrierten Dry-Signal eingemischt werden. 0 % ist ein exakter Bypass des Doublers. Dezente Mengen (10–25 %) verdicken ein Lead, ohne einen offensichtlichen „Chorus"-Effekt; höhere Mengen (40 %+) bauen eine vollere Klein-Chor-Fläche auf, am besten geeignet für Backing-/Chor-Parts statt eine exponierte Leadlinie. |
| **Double Detune** | 0-50 | 10 | cents | Tiefe des kontinuierlichen Pitch-Wobbles des Doublers (ein sanftes, modulated-delay-basiertes Detune, kein diskreter Pitch-Shift — immer click-frei). Der Regler verbringt einen größeren Teil seines Wegs im niedrigen Cents-Bereich: Werte um 5–12 cents klingen wie ein enges, dezentes Double; das obere Ende (30–50 cents) klingt loser und chorus-artiger. |
| **Double Width** | 0-100 | 100 | % | Stereo-Streuung der vier Doubler-Stimmen. 0 % hält alle vier Stimmen zentriert (mono-kompatibel, nützlich, wenn das Vocal in einem mono-fold-down-sensiblen Mix zentriert bleiben muss); 100 % verteilt sie über das gesamte Stereofeld für einen breiten Chor-Effekt. |
| **Mix** | 0-100 | 100 | % | Gesamte Dry/Wet-Mischung. Steht standardmäßig auf 100 % (vollständig prozessiert), da Seraph als vollwertiger Channel Strip laufen soll, nicht eingemischt werden — senke ihn nur für Parallel-Processing-Setups (z. B. um ein de-essed/gedoppeltes Signal unter ein ansonsten unangetastetes Dry-Vocal zu mischen). |
| **Output** | -24 to +24 | 0 | dB | Output-Trim, angewendet nach dem Doubler und vor Mix. Nutze ihn, um Pegeländerungen durch Comp oder Double auszugleichen, bevor das Signal die nächste Stufe deiner Kette erreicht. |
| **De-Ess Knee** | 0-12 | 0 | dB | Wie allmählich das De-Essing um seinen Threshold herum einsetzt. Bei 0 schnappt die Reduktion in dem Moment zu, in dem Zischlaute den Threshold überschreiten — chirurgisch, und bei Grenzfall-Konsonanten als „Zupacken" hörbar. Höher gedreht beginnt es schon unterhalb des Thresholds sanft zu reduzieren und erreicht oberhalb die volle Stärke, was sich wie ein De-Esser liest, der einfach immer leicht da ist, statt wie einer, der zuschnappt. 4–8 dB passen zu einem Lead-Vocal; für chirurgische Reparaturarbeit lass es bei 0. |
| **De-Ess Lookahead** | 0-2 | 0 | ms | Lässt den De-Esser das Ess kommen sehen, sodass der Gain schon unten ist, wenn es eintrifft, statt in der ersten Millisekunde hinterherzulaufen. Entfernt den hellen „Tick" am Anfang eines harten Konsonanten, den keine noch so hohe zusätzliche Reduktion behebt. **Fügt Latenz hinzu** (siehe unten) und ist nicht automatisierbar. 1–2 ms genügen völlig; mehr bringt nichts, weshalb der Bereich dort endet. |
| **De-Ess Link** | off/on | off | - | Aus wird jeder Kanal von seinem eigenen Detektor de-esst. An werden beide Kanäle gemeinsam um den jeweils lauteren reduziert. Schalte es für alles Stereophone ein, bei dem ein Ess das Klangbild nicht seitlich verschieben soll — ein gedoppelter oder gespreizter Chor, eine Stereo-Raumaufnahme. Bei zwei wirklich unabhängigen Mono-Quellen lass es aus. |
| **Comp Link** | off/on | off | - | Dieselbe Idee für den Kompressor: An treibt eine gemeinsame Hüllkurve (inklusive Auto-Release) beide Kanäle, sodass das Stereobild unter Kompression stehen bleibt. Auf einem Stereo-Vocal-Bus empfohlen. |
| **Air Freq** | 10/12/15 kHz | 12 kHz | - | Wo der Air-Shelf zu heben beginnt. 12 kHz ist das, was Seraph immer genutzt hat. 10 kHz greift weiter herunter in die Präsenz, nützlich bei einem dunkleren Take oder einem dumpferen Mikrofon. 15 kHz bleibt vollständig aus dem Zischlautbereich heraus, was gut zu starkem De-Essing passt — du kannst Offenheit hinzufügen, ohne das gerade entfernte Ess wieder zu füttern. |
| **Double Mode** | Classic / Micro / Shift | Classic | - | Welche Doubler-Engine läuft. Siehe [Doubler-Modi](#doubler-modi). Nicht automatisierbar, da zwei der drei eine unterschiedliche Latenz melden. |
| **Humanize** | 0-100 | 0 | % | Wie stark jede gedoppelte Stimme für sich driftet — langsam, in Timing, Tonhöhe und Pegel. Bei 0 stehen die Stimmen mathematisch zueinander in Beziehung, so wie ein Doubler immer geklungen hat. Höher gedreht dekorreliert sie so, wie vier echte Sänger sich nie ganz einig sind. 20–40 % reichen, um das Maschinenhafte zu nehmen; höhere Einstellungen werden lose und chorartig. Deterministisch: Dieselben Einstellungen erzeugen immer denselben Drift. |
| **Formant Preserve** | off/on | on | - | Nur im Shift-Modus aktiv. An behält die Stimme ihren eigenen Vokalcharakter, während sich die Tonhöhe bewegt. Aus wandern die Formanten mit der Tonhöhe. Innerhalb von Seraphs Bereich von +/-50 Cent ist der Unterschied so oder so subtil, das hier ist also vor allem eine Absicherung für den höherwertigen Pfad der Shift-Engine. |

Alle Parameter sind geglättet (kein Zipper-Noise bei Automation oder manuellen Reglerbewegungen). Alle sind automationssicher außer **Double Mode** und **De-Ess Lookahead**, die die gemeldete Latenz ändern — siehe unten.

## Doubler-Modi

Die drei Modi teilen sich dieselben vier Stimmen, dieselben Panoramapositionen pro Stimme und dieselben Amount-/Detune-/Width-Kennlinien; ein Wechsel zwischen ihnen behält also das Arrangement und ändert nur, wie das Detune erzeugt wird. Ein Wechsel wird von einer kurzen Blende verdeckt, du kannst sie also bei laufendem Audio abhören.

| Modus | Was er tut | Latenz | Wofür |
|---|---|---|---|
| **Classic** | Die Engine, die Seraph immer schon hatte: Die Delay-Linie jeder Stimme wird von einem langsamen Sinus gewobbelt, was die Tonhöhe kontinuierlich um die Note herum auf und ab verschiebt. Nie in Stimmung, nie verstimmt. | Keine | Der vertraute Seraph-Doubler-Sound. Alles, was vor v0.3.0 entstanden ist, nutzt ihn und bleibt unverändert. |
| **Micro** | Ein echtes konstantes Detune — jede Stimme sitzt eine feste Anzahl Cent daneben und bleibt dort. Genau auf deutlich unter ein Cent. | Keine | Stacks, die ein Intervall halten müssen: Chor-Parts, weite Lead-Doubles, überall dort, wo das Classic-Wobble sich als „Chorus" liest, wo du „noch ein Sänger" wolltest. Konstruktionsbedingt slappiger als Classic (siehe unten). |
| **Shift** | Spektrales Pitch-Shifting, mit der Option, den Vokalcharakter festzuhalten, während sich die Tonhöhe bewegt. Der genaueste und der teuerste. | ~30 ms | Das sauberste Doubling, und der Modus, zu dem du greifst, wenn Detune Richtung oberes Ende seines Bereichs geschoben wird. |

Zwei Dinge sind zu **Micro** wissenswert. Seine Stimmen sitzen zeitlich weiter hinten als die von Classic — rund 34–49 ms statt 9–24 ms —, weil der Pitch-Shift durch kontinuierliches Gleiten der Delay-Linie erzeugt wird. Das ist ein bewusster Charakterunterschied, kein Fehler: Micro ist slappiger und liest sich als breiteres, stärker abgesetztes Double. Und weil diese ~25 ms der Effekt selbst und keine Verarbeitungsverzögerung sind, meldet Micro überhaupt keine Latenz; brauchst du die gedoppelten Stimmen eng am Dry-Signal, ist Classic der strammere Modus.

**Shift** ist der einzige Modus, der Latenz meldet, und der einzige, bei dem das Plugin vom Host delay-kompensiert werden muss. Jede aktuelle DAW erledigt das automatisch.

## Latenz und Delay-Kompensation

| Einstellung | Gemeldete Latenz bei 48 kHz |
|---|---|
| Default (Classic, kein Lookahead) | 0 Samples |
| Micro-Modus | 0 Samples |
| Shift-Modus | 1440 Samples (30,0 ms) |
| De-Ess Lookahead auf 2 ms | 96 Samples |

Die beiden addieren sich: Shift-Modus mit 2 ms Lookahead meldet 1536 Samples. Der Wert skaliert mit der Samplerate — der Shift-Modus liegt immer bei ~30 ms, also 2880 Samples bei 96 kHz.

Beide Einstellungen sind **nicht automatisierbar**, mit Absicht. Hosts kommen mit einer Latenzänderung mitten in einer Automation schlecht zurecht, deshalb ändert Seraph das Gemeldete nur als Reaktion auf eine bewusste Bewegung deinerseits und verdeckt die Änderung selbst mit einer 10-ms-Blende. Du kannst die Modi weiterhin bei laufendem Audio umschalten; du kannst es nur nicht in eine Automations-Lane zeichnen.

Ist eines von beiden aktiv, wird das gesamte Plugin — inklusive der Dry-Seite des Mix-Reglers — um den gemeldeten Betrag verzögert, sodass Mix eine saubere Mischung bleibt statt zu verschmieren. Paralleles Routing funktioniert weiterhin; die Delay-Kompensation deiner DAW richtet den Seraph-bearbeiteten Pfad automatisch gegen den unangetasteten aus.

Diese Zahlen sind gemessen, nicht nur behauptet: Ein durch das Plugin geschickter Klick kommt genau dort an, wo es die gemeldete Latenz verspricht, auf ein Sample genau — in Micro, in Shift, in Shift mit 2 ms Lookahead, und bei Lookahead allein.

## Unter der Haube

Ein paar Mechanismen, die es wert sind zu kennen, wenn du verstehen willst, warum sich die drei Doubler-Engines und das Lookahead des De-Essers so verhalten, wie sie es tun — nicht nur, wofür die Regler beschriftet sind:

**Micro hält ein echtes Intervall, indem es eine Delay kontinuierlich rampt, nicht indem es die Tonhöhe springt.** Eine Delay-Line, deren Länge sich mit `dτ/dt = 1 − r` ändert, erzeugt exakt das Pitch-Verhältnis `r`; Micro liest diese Delay mit kubischer Catmull-Rom-Interpolation über ein Dual-Head-Design aus und überblendet so, dass jeweils der Head, der gerade mitten im Umschlag ist, in diesem Moment stumm ist. Gemessen genau auf 0,5 Cent bei ±30 Cent, und auf eine −100-dBFS-Null gegen ein einfaches statisches Delay bei null Detune — weil es bei null Detune genau das wird. Der Sweep läuft aufwärts von der Basis-Delay statt um sie herum zentriert, weil Zentrierung bedeuten würde, Samples zu lesen, die noch nicht angekommen sind; die Konsequenz ist die oben beschriebene Stimmen-Delay von 34–49 ms, dokumentiert statt versteckt.

**Der Shift-Modus lässt den MIT-lizenzierten Signalsmith-Stretch-Phase-Vocoder laufen, eine Instanz pro Stimme**, gepinnt auf einen fixen Upstream-Commit und konfiguriert gegen Seraphs eigenes Latenz-Budget statt gegen die eigenen Defaults der Engine: ein 30-ms-Fenster bei einem 7,5-ms-Hop, spezifiziert in Sekunden (nicht als Bin-Anzahl), sodass eine 96-kHz-Session dasselbe physikalische Fenster behält, statt es still zu halbieren. Das eigene Default-Preset der Engine würde etwa 150 ms nutzen, was weit außerhalb dessen liegt, was sich ein Tracking-Vocal-Insert leisten kann. Vendort statt selbst gebaut, aus einem konkreten Grund: Die Alternativtechniken (LPC-/Cepstral-Formant-Schätzung, TD-PSOLA-artiges Pitch-Marking) setzen beide eine monophone Quelle voraus und degradieren genau bei dem Material, das Seraph routinemäßig bekommt — gestapelte Vocals und Chor-Busse. Der vollständige Lizenztext steht in `THIRD-PARTY-NOTICES.md`.

**Humanize lässt jede Stimme unabhängig, aber deterministisch driften.** Drei langsame Random Walks pro Stimme — Timing, Pitch und Level — laufen aus einem geseedeten Generator durch ein langsames One-Pole-Filter, auf einem fixen Steuertakt, der nie die Blockgröße des Hosts konsultiert. Zwei Renders vom selben Reset-Zustand kommen bit-identisch heraus, und ein Host, der Audio in 64-Sample-Häppchen übergibt, erzeugt exakt denselben Drift wie einer, der es in 256-Sample-Häppchen übergibt. Bei 0 % ist jeder Offset exakt null, sodass die Classic-Engine bit-identisch zu v0.2.0 bleibt.

**De-Ess Lookahead verzögert das erkannte Band zusammen mit dem Audio, nicht nur das Audio.** Der De-Esser funktioniert, indem er eine skalierte Kopie des erkannten Zischlaut-Bands zurück auf das Signal addiert, was den Pegel nur reduziert, wenn beide zeitlich ausgerichtet sind. Die naheliegende, einfachere Implementierung — den Audio-Pfad verzögern und den Detektor auf dem unverzögerten Input laufen lassen — würde beide um die Lookahead-Länge versetzt lassen, und weil Sibilanz bei 2 ms Lag effektiv rauschartig und dekorreliert ist, würde diese Fehlausrichtung die „Subtraktion" bei maximaler Reduktion um etwa das 0,8-Fache der Band-Leistung wieder hinzufügen: Der De-Esser würde Zischlaute verstärken statt sie zu reduzieren. Seraph verzögert beide, lässt den Detektor auf dem unverzögerten Band laufen und schickt die resultierende Gain durch ein gleitendes Minimum-Fenster, sodass sie ihr Ziel erreicht, bevor der verzögerte Zischlaut ankommt, statt ihm hinterherzujagen. Gemessener Effekt: Das Onset-Überschwingen, das ein schneller Attack sonst durchlassen würde, sinkt auf höchstens 0,5 dB Überschuss über die eingeschwungene Reduktion, gegenüber über 3 dB ohne aktiviertes Lookahead.

**Engineering-Hygiene:** 108 Testfälle laufen auf macOS und Windows bei jedem Push, plus pluginval bei Strictness 10 und `auval -strict` — geprüft werden keine Heap-Allokationen auf dem Audio-Thread unter einem ersetzten Allocator (auch bei Live-Modus-Wechseln innerhalb der Guard-Klausel), eine neutrale Null bei −90 dBFS oder besser über sechs Sampleraten von 44,1 bis 192 kHz, und der Shift-Modus verarbeitet eine volle Sekunde 48-kHz-Stereo-Audio in einem Release-Build in deutlich unter 100 ms Wall-Clock-Zeit.

## Tipps

- **De-esse, bevor du Air oder Comp hinzufügst.** Zischlaut-Energie sitzt im selben Bereich, den Air anhebt, und ein breitbandiger Kompressor reagiert auf Zischlaut-Peaks genau wie auf jeden anderen Transienten — wenn du zuerst de-esst, arbeiten beide nachfolgenden Stufen mit einem saubereren Signal.
- **Nutze De-Ess Listen, wenn du dir nicht sicher bist, wo die Zischlaute sitzen.** Es geht deutlich schneller, De-Ess Freq durchzufahren, während das erkannte Band gesolot ist, als es nach Gehör gegen den vollen Mix durchzufahren.
- **Greife zu De-Ess Width, bevor du den Sweep von De-Ess Freq verbreiterst.** Erwischt das De-Essing den falschen Sound (zu „woosh"-artig, oder verpasst das eigentliche „s"), ist es meist chirurgischer, zuerst Width zu verengen (niedrigere Werte), als die Mittenfrequenz zu verschieben.
- **Comps Release passt sich von selbst an — du brauchst keinen Release-Regler.** Er bleibt schnell und transparent bei isolierten lauten Momenten und verklebt hörbarer während anhaltender lauter Passagen, ganz ohne zusätzlichen Regler zum Einstellen.
- **Comp ist ein Glue-Regler, kein Leveling-Werkzeug.** Wenn ein Take stark inkonsistente Pegel hat (sehr leise Strophen, sehr laute Refrains), behebe das zuerst mit Clip Gain oder einem dedizierten Leveling-Kompressor vorgeschaltet; Comps sanftes 3:1-Maximum-Ratio soll einem bereits einigermaßen ausgeglichenen Take Konsistenz und Kohäsion geben, nicht einen wild unebenen retten.
- **Double ist additiv, kein Ersatz für echte gedoppelte Takes.** Bei Chor-Parts klingt eine Prise Double in niedriger bis moderater Menge zusätzlich zu ein paar echten aufgenommenen Layern meist voller und natürlicher, als sich allein auf Double zu verlassen, um aus einem einzigen Take einen ganzen Chor zu simulieren.
- **Behalte Width bei einem mono-sensiblen Mix im Blick.** Falls dein Material auf Mono gefaltet werden könnte (Streaming-Plattformen, manche Broadcast-Ketten), prüfe den Doubler mit Width Richtung 0 % zurückgezogen, um sicherzustellen, dass sich die gedoppelten Stimmen beim Summieren nicht unangenehm auslöschen.
- **Probiere Micro, bevor du zu mehr Detune greifst.** Klingt ein Double eher nach Chorus-Effekt als nach einem zweiten Sänger, liegt das Problem meist am Wobble der Classic-Engine, nicht an der Menge des Detunes. Micro bei 8–14 Cent liest sich oft als „noch ein Take", wo Classic bei derselben Einstellung als „Effekt" liest.
- **Humanize ist das, was einen Stack davon abhält, synthetisch zu klingen.** Vier Stimmen mit exaktem Detune sind immer noch vier Kopien einer Performance. Ein wenig Drift — 20–30 % — ist meist der Unterschied zwischen einem Doubler, den man bemerkt, und einem, den man nicht bemerkt.
- **Schalte die Links bei Stereoquellen ein.** De-Ess Link und Comp Link kosten beide nichts und verhindern beide dasselbe Problem: dass ein lauter Moment auf einer Seite still das ganze Klangbild verschiebt.
- **Kombiniere Air Freq auf 15 kHz mit stärkerem De-Essing.** So fügst du Offenheit oberhalb des Zischlautbereichs hinzu statt obendrauf.
- **Seraph ist weiterhin sicher in Parallelketten.** In seiner Default-Konfiguration meldet es überhaupt keine Latenz; sind Shift-Modus oder Lookahead aktiv, übernimmt die Delay-Kompensation deiner DAW die Ausrichtung, und die Dry-Seite von Mix wird intern passend verzögert.

## Bekannte Einschränkungen (v0.3.0)

- Die GUI ist ein funktionaler Slider-/Knob-Editor plus eine einfache Preset-Leiste (eine eigene, vektorgezeichnete GUI ist ein späterer Meilenstein — siehe die Projekt-Roadmap).
- Detune ist in jedem Modus auf +/-50 Cent begrenzt. Die Engine des Shift-Modus kann weit mehr, aber größere Intervalle brauchen Kontrolle pro Stimme und die Oberfläche eines Harmonizers, und das ist ein eigenes Feature statt einer größeren Zahl an diesem Regler.
- Formant-Erhaltung ist nur im Shift-Modus sinnvoll; Classic und Micro resampeln das Spektrum nicht, es gibt dort also nichts zu korrigieren.
- Der Erkennungs-Threshold von De-Ess ist weiterhin ein fixer, absoluter Pegel (nicht pegel-relativ/adaptiv) — bei einem sehr leisen Take muss dessen Gain eventuell erst hochgezogen werden, bevor De-Ess spürbar reagiert. Die Begründung findest du in `docs/design-brief.md` ss2.1.
- Der Air-Shelf ist nicht dekrampft, seine Kurve ist bei 15 kHz in einer 44,1-kHz-Session nahe Nyquist also etwas steiler als bei derselben Einstellung mit 96 kHz. Das zu korrigieren würde den Klang bei der Default-Einstellung verändern und braucht einen eigenen Voicing-Durchgang.
- Füttert ein Host Seraph jemals mit nicht-endlichem Audio (NaN/Inf, z. B. von einem sich falsch verhaltenden vorgeschalteten Plugin), ist ein Transport-Stop/Start oder das erneute Öffnen des Plugins — was einen `reset()`-Aufruf des Hosts auslöst — der verlässliche Weg, das zu bereinigen. Das ist keine Seraph-Eigenheit (Envelope-Follower und Filter fangen sich konstruktionsbedingt NaN ein, sobald eine Zustandsvariable nicht-endlich wird), aber die vendorte Engine des Shift-Modus erholt sich speziell nicht einmal von ihrem eigenen internen Reset, weshalb der Wrapper nicht-endlichen Input durch Stille ersetzt, bevor die Engine ihn je zu Gesicht bekommt.
