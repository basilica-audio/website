<!-- German translation of nave.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Nave-Icon" width="120"/></p>

# Nave-Benutzerhandbuch

*Cabinet-Impulsantwort-Loader für Gitarren- und Bass-Reamping.*

## Was Nave ist

Nave nimmt ein trockenes, unverstärktes Instrumentensignal (eine DI-Gitarren- oder Bass-Spur, oder den Pre-Cab-Output eines Amp-Sims) und faltet es mit der Impulsantwort ("IR") eines echten (oder emulierten) Lautsprecher-Cabinets und Mikrofons. Anders gesagt: Bei Nave wird aus einem trockenen, schnarrenden DI-Signal etwas, das klingt, als wäre es an einem echten Cab in einem Raum abgenommen worden.

In einer Heavy-Production-Chain sitzt Nave typischerweise **nach** der Distortion-/Amp-Sim-Verarbeitung und **vor** EQ-/Bus-Processing:

```
DI guitar/bass -> amp sim / preamp distortion -> Nave (cab IR) -> EQ / compression -> mix bus
```

Es eignet sich gleichermaßen zum nachträglichen Reamping einer aufgenommenen DI-Spur wie zum Live-Einsatz in einer Monitoring-Chain während des Trackings.

## Signalfluss

```
Input --> Convolution (crossfade of IR A / IR B) --> Distance --> LoCut (HPF) --> HiCut (LPF)
                                                                                          |
                                    Output <-- Level (output trim) <-- Mix <--------------+
                                                                          ^
                                                                          |
                                                              delay-compensated dry path
```

1. **Convolution.** Dein Instrumentensignal wird mit der/den geladenen Impulsantwort(en) gefaltet. Ohne geladene IR läuft Nave mit einer mathematisch transparenten Unit-Impuls-("Delta"-)IR — es ist von Haus aus ein valider, standardmäßig stiller Effekt, kein Platzhalter, der deinen Sound färbt, bis du etwas lädst.
2. **Distance.** Eine optionale, simulierte Mikrofon-Abstand-Färbung (siehe [Distance](#distance-simulierter-mikrofonabstand) unten). Standardmäßig aus.
3. **LoCut / HiCut.** Zwei universelle Tone-Shaping-Filter zum Aufräumen des gefalteten Signals — ein Hochpass, um das Low End zu straffen, ein Tiefpass, um Fizz/Härte zu zähmen. Beide sind standardmäßig aus (vollständig offen).
4. **Mix.** Mischt das vollständig verarbeitete ("wet") Signal mit deinem ursprünglichen trockenen Input. Standardmäßig 100 % wet — eine Cab-IR läuft normalerweise voll im Signalweg, nicht gemischt mit der rohen DI.
5. **Level.** Ein finaler Output-Trim, damit das Wechseln von Cabs/Einstellungen nicht auch dein nachgelagertes Gain-Staging durcheinanderbringt.

Die implementierungsseitigen Details (Latenzhandling, Filter-Bypass-Semantik, IR-Datei-State) findest du in [`architecture.md`](architecture.md).

## Impulsantworten laden

Nave hat **zwei unabhängige IR-Slots**, A und B:

- **IR A** — der primäre/ursprüngliche Slot. Nutze den Button **Load IR...**, um eine `.wav`/`.aiff`-Cabinet-IR-Datei auszuwählen; **Default** setzt ihn zurück auf die eingebaute transparente Delta-IR.
- **IR B** — ein sekundärer Slot, geladen und geleert auf die gleiche Weise über **Load IR B...** / **Default**. Für sich allein bewirkt er nichts (siehe [IR Blend](#ir-blend) unten) — er spielt erst eine Rolle, sobald du etwas Blend einstellst.

**Dein IR-Audio wird in der Session gespeichert** (neu in v0.3.0). Bis zu 10 Sekunden pro Slot der geladenen IR liegen im plugin-eigenen State, sodass ein Projekt mit denselben Cabinets wieder öffnet, selbst wenn die Originaldateien verschoben, umbenannt, gelöscht oder auf einem anderen Rechner zurückgelassen wurden. Die Dateipfade werden weiterhin mitgespeichert, damit der Editor dir sagen kann, woher eine IR stammt — der Klang hängt aber nicht mehr von ihnen ab. (Vor v0.3.0 wurde nur der Pfad gespeichert, und eine fehlende Datei setzte den Slot stillschweigend auf den transparenten Default zurück. Hast du ältere Projekte, macht sie erneutes Öffnen und Speichern in v0.3.0 selbsttragend.) Eine IR länger als 10 Sekunden wird weiterhin nur als Pfad gespeichert, da eine Cabinet-IR nie so lang ist und das Einbetten deine Session-Datei aufblähen würde.

### IR Gain Match

Zwei geladene IRs können selbst bei identischen Einstellungen spürbar unterschiedlich laut klingen. **IR Gain Match** entscheidet, wie Nave sie angleicht:

- **Energy** (Default) gleicht die rohe Energie jeder IR an. Das hat Nave immer getan, und es ist das, was die meisten IR-Loader tun.
- **Loudness** gleicht die *K-gewichtete* Energie jeder IR an — dieselbe Gewichtung, die ein LUFS-Meter benutzt, die also den Subbass abwertet und den Präsenzbereich in etwa so anhebt, wie es dein Ohr tut. Eine dunkle 4x12-Aufnahme trägt weit mehr ihrer Energie dort, wo das Ohr am unempfindlichsten ist, weshalb sie im Energy-Modus hörbar leiser bleibt als eine helle Nahmikrofon-Aufnahme, obwohl beide gleich messen. Im Loudness-Modus verändert ein IR-Wechsel den Klang, ohne im Pegel zu springen — ein A/B vergleicht damit tatsächlich Klang.

Loudness-Angleichung ist bei spektral flachem Material exakt und bei echtem Programmmaterial näherungsweise, da sie die gewichtete Energie der *Impulsantwort* angleicht und nicht die deines konkreten Gitarren-Takes. In beiden Fällen bleibt **Level** die Stelle für die finale Anpassung.

Diesen Regler zu ändern setzt die Convolution-Engine kurz zurück — stelle ihn also bei gestopptem Transport ein, wenn du pingelig bist; siehe [Eine Anmerkung zu den drei „Reset"-Schaltern](#eine-anmerkung-zu-den-drei-reset-schaltern).

### IR Align

Wenn du IR B lädst, richtet Nave sie zeitlich gegen IR A aus, damit das Mischen der beiden nicht kammfiltert. **IR Align** wählt, wie:

- **Precise** (Default für neue Instanzen) kreuzkorreliert die beiden IRs, findet den Versatz bruchteilgenau auf Sample-Ebene und erkennt zusätzlich, wenn IR B gegenüber IR A polaritätsinvertiert ist — ein Mikrofon hinter dem Cabinet oder ein falsch gepatchter Preamp — und dreht sie für dich um. Ohne dieses Umdrehen würde das Mischen der beiden teilweise auslöschen statt zu addieren.
- **Legacy** ist die einfachere Onset-Erkennung, die Nave bis v0.2 genutzt hat. Vor v0.3.0 gespeicherte Sessions werden beim Öffnen automatisch auf Legacy gesetzt und klingen damit exakt wie zuvor. Wechsle auf Precise, wenn du die Verbesserung willst.

### Min-Phase (pro Slot)

**IR A Min-Phase** und **IR B Min-Phase** wandeln die IR eines Slots in ihr minimalphasiges Äquivalent um: identischer Frequenzgang, aber ohne jede Überschussphase und mit der Energie nach vorne gezogen. Das ist es, was IRs aus unterschiedlichen Quellen sauber mischbar macht — zwei Aufnahmen, die allein gut klingen, können sich im Blend allein aufgrund der Phase auslöschen, und beide zu minimalphasieren nimmt diese Variable heraus.

Es ist nie destruktiv. Nave behält die Original-IR, ein Zurückschalten stellt sie also exakt wieder her.

### IR Blend

Der Regler **IR Blend** bewegt sich zwischen IR A (0 %) und IR B (100 %). Typische Anwendungen:

- **Zwei verschiedene Cabs** — ein straffes 4x12 mit einem boomigeren 2x12 nach Geschmack mischen, ohne ein separates Blending-Plugin zu brauchen.
- **Zwei Mikrofonpositionen am selben Cab** — z. B. ein On-Axis-Nahmikrofon (IR A), gemischt mit einem Raum-/Ambience-Mikrofon (IR B), für mehr Dimension.

Wenn du IR B lädst, richtet Nave sie automatisch **phasenrichtig** am transienten Einsatz von IR A aus, bevor die beiden überhaupt gemischt werden. Zwei reale IR-Aufnahmen beginnen selten exakt im gleichen Moment (unterschiedliche Mikrofonabstände, unterschiedliche Aufnahme-Setups), und unausgerichtete IRs direkt zu mischen würde ein breites Frequenzband teilweise auslöschen (Kammfilterung) — der Ausrichtungsschritt verhindert das, sodass IR Blend wie eine echte klangliche Mischung klingt statt wie ein phasiges Durcheinander.

Blend steht standardmäßig auf 0 % (nur IR A) — eine IR B zu laden und Blend bei 0 % zu lassen hat keinen hörbaren Effekt, bis du den Regler aufdrehst.

### Blend Mode: Crossfade oder Morph

**Crossfade** (Default) lässt beide IRs laufen und blendet zwischen ihren Ausgängen über. Das ist vorhersagbar und das, was Nave immer getan hat — aber bei Zwischenstellungen hörst du *zwei* Cabinets gleichzeitig, und überall dort, wo ihre Direktschallanteile leicht zeitversetzt eintreffen, löschen sie sich teilweise aus. Das ist Kammfilterung, und sie ist bei 50 % am stärksten — genau dort, wo „irgendwo zwischen diesen beiden Mikrofonen" liegt.

**Morph** ist die Alternative und das, worum dieses Release gebaut ist. Statt zwei IRs zu summieren, zerlegt Nave sie — trennt jede in *wie sie klingt* (ihren Frequenzgang) und *wann sie eintrifft* (ihr Timing) —, interpoliert diese beiden Dinge unabhängig voneinander und baut daraus eine einzige neue Impulsantwort zusammen. Es ist immer nur ein Cabinet im Signalweg, es gibt also nichts, wogegen gekammfiltert werden könnte. Blend zu ziehen fährt stufenlos zwischen den beiden Aufnahmen hindurch, so wie es das physische Bewegen des Mikrofons täte — inklusive des subtilen Tonhöhen-Gleitens eines Mikrofons in Bewegung.

Zwei Dinge solltest du wissen:

- **Morph verändert auch die Endpunkte.** Bei Blend 0 % hörst du die minimalphasige Version von IR A, nicht exakt IR A. Das liegt in der Technik selbst begründet und ist der Grund, warum Crossfade der Default bleibt — auf Morph zu wechseln ist eine bewusste Charakteränderung, nie etwas, das eine Session von selbst annimmt.
- **Morph glänzt bei verwandten Aufnahmen.** Zwei Mikrofonpositionen am selben Cabinet morphen wunderbar. Zwei völlig unverwandte Cabinets morphen durch Magnitudengänge, die kein reales Cabinet hat; das kann ein nützlicher Sound sein, ist aber Sounddesign und keine Mikrofonierung.

### IR B Trim, Polarity und Delay

Drei Regler, die ausschließlich auf den IR-B-Zweig wirken — für das Einstellen eines Dual-Mic-Blends, wie es ein Engineer am Pult täte:

- **IR B Trim** (-24 bis +24 dB) balanciert Slot B gegen Slot A, ohne den Gesamtausgang anzutasten.
- **IR B Polarity** dreht Slot B um. Naves Precise-Ausrichtung korrigiert eine invertierte Aufnahme bereits automatisch, das hier ist also der manuelle Override für den Fall, dass die „falsche" Polarität der gewünschte Sound ist.
- **IR B Delay** (+/-5 ms) versetzt Slot B zeitlich. Positive Werte schieben Slot B nach hinten; negative Werte ziehen ihn nach vorne, was — da nichts eintreffen kann, bevor es gespielt wurde — dadurch realisiert wird, dass stattdessen Slot A um denselben Betrag verzögert wird. Der relative Versatz ist derselbe, aber bei negativer Einstellung liegt der gesamte Wet-Pfad absolut betrachtet |d| Millisekunden später. Bei exakt 0 ms wird kein Zweig verzögert, der Default kostet also nichts und ändert nichts. Kleine Versätze sind hier der klassische Trick, um einen gedoppelten Cab-Sound zu verdicken, oder um die Kammfilter-Kerbe, die die Ausrichtung entfernt, bewusst wieder einzustellen.

### Distance Air

Das klangliche Modell des Distance-Reglers ändert nicht, *wann* Schall eintrifft — ein Mikrofon zurückzuziehen tut das aber tatsächlich, mit rund 2,9 ms pro Meter. **Distance Air** fügt diese Laufzeitverzögerung dem Wet-Pfad hinzu, sodass Distance zurückzunehmen das Cabinet auch zeitlich nach hinten schiebt. Standardmäßig aus; bei Distance 0 % tut es ohnehin nichts.

Distance mit eingeschaltetem Air zu automatisieren lässt die Verzögerung gleiten statt springen, was das korrekte Doppler-Verhalten für ein bewegtes Mikrofon ist — und nebenbei ein hübscher Effekt für sich.

### LoCut- und HiCut-Flankensteilheiten

Beide Filter können jetzt mit **12 dB/Okt.** (Default, und was v0.2 ausgeliefert hat) oder **24 dB/Okt.** laufen. Die steilere Einstellung geht schneller aus dem Weg, was nützlich ist, wenn du Low-End-Mud entfernen willst, ohne den Körper direkt darüber auszudünnen. Ein Flankenwechsel überblendet die beiden Filter über 10 ms und ist damit selbst mitten im Take lautlos.

### Distance (simulierter Mikrofonabstand)

Der Regler **Distance** ist eine vereinfachte Emulation davon, das Mikrofon weiter vom Cab wegzurücken: Bei höheren Einstellungen reduziert er den Nahbesprechungseffekt im Bass und dämpft die Höhen leicht. Die Höhenverdunklung ist modelliert nach dem Verhalten eines echten Cabinets, dessen Höhen abfallen, wenn ein Mikrofon weiter zurück und aus der Achse bewegt wird — das wird sehr viel stärker von der Richtcharakteristik des Lautsprechers getrieben als von tatsächlicher Luftabsorption bei typischen Reamping-Abständen. Lies es also weniger als „die Luft zwischen Mikro und Cab" und mehr als „wie der Lautsprecher selbst seitlich weniger Höhen abstrahlt". Es ist *kein* physikalisch exaktes Distanzmodell — es wird keine Pre-Delay-/Timing-Änderung angewendet — nur eine musikalisch nützliche klangliche Verschiebung, um eine zu nahe/zu helle IR im Mix zurückzuschieben, ohne zu einem separaten EQ greifen zu müssen. Der Bassbereich reagiert im ersten Teil des Reglerwegs schneller und flacht Richtung 100 % ab, was dem Verhalten des echten Nahbesprechungseffekts entspricht — der Großteil der Änderung passiert früh, nicht gleichmäßig über den gesamten Regelweg verteilt.

Distance steht standardmäßig auf 0 % ("aus" — an dieser Stelle der Chain wird gar keine Färbung angewendet, ein echter Passthrough).

## Parameterreferenz

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **LoCut** | 20 – 800 | 20 (off) | Hz | Hochpassfilter nach der Convolution. Bei seinem Minimum (20 Hz, Default) ist es vollständig bypassed — ein echter Passthrough, nicht nur eine unhörbare Grenzfrequenz. Höher drehen, um eine boomige Cab-IR zu straffen oder Low-End-Mud zu zähmen, bevor das Low End auf dein Amp-/Bus-Processing trifft. |
| **HiCut** | 2000 – 20000 | 20000 (off) | Hz | Tiefpassfilter nach der Convolution. Bei seinem Maximum (20 kHz, Default) ist es vollständig bypassed. Niedriger drehen, um Fizz, Härte oder überschüssige Höhen einer hellen IR zu zähmen — ein klassischer Move bei High-Gain-Metal-Gitarrensounds. |
| **IR Blend** | 0 – 100 | 0 (IR A only) | % | Überblendet zwischen IR A (0 %) und IR B (100 %). Siehe [IR Blend](#ir-blend). Hat keinen hörbaren Effekt, solange keine IR in Slot B geladen ist. |
| **Distance** | 0 – 100 | 0 (off) | % | Simulierter Mikrofon-zu-Cab-Abstand: reduziert Nahbesprechungs-Bass und fügt mit steigendem Wert hochfrequente Verdunkelung hinzu. Siehe [Distance](#distance-simulierter-mikrofonabstand). |
| **Mix** | 0 – 100 | 100 (fully wet) | % | Dry/Wet-Blend des vollständig verarbeiteten Signals gegen deinen Original-Input. Niedriger drehen für einen parallelen/gemischten Cab-Sound, oder um probehalber zu hören, wie viel vom Charakter der IR du wirklich willst. |
| **Level** | -24 – +24 | 0 | dB | Output-Trim, zuletzt angewendet. Nutze es, um das Gain-Staging nach dem Wechseln von IRs oder dem Einstellen von Mix/Blend/Distance anzugleichen — all das kann den Gesamtpegel verschieben. |
| **Blend Mode** | Crossfade / Morph | Crossfade | — | Wie IR A und IR B kombiniert werden. Siehe [Blend Mode](#blend-mode-crossfade-oder-morph). |
| **IR Align** | Legacy / Precise | Precise | — | Wie IR B zeitlich gegen IR A ausgerichtet wird. Vor v0.3.0 gespeicherte Sessions öffnen als Legacy. Siehe [IR Align](#ir-align). |
| **IR B Trim** | -24 – +24 | 0 | dB | Pegel ausschließlich des IR-B-Zweigs. |
| **IR B Polarity** | off / on | off | — | Invertiert den IR-B-Zweig. |
| **IR B Delay** | -5 – +5 | 0 | ms | Zeitversatz zwischen den beiden Slots. Siehe [IR B Trim, Polarity und Delay](#ir-b-trim-polarity-und-delay). |
| **IR Gain Match** | Energy / Loudness | Energy | — | Wie geladene IRs gegeneinander im Pegel angeglichen werden. Siehe [IR Gain Match](#ir-gain-match). |
| **IR A Min-Phase** | off / on | off | — | Minimalphasen-Transformation auf Slot A. Siehe [Min-Phase](#min-phase-pro-slot). |
| **IR B Min-Phase** | off / on | off | — | Minimalphasen-Transformation auf Slot B. |
| **Distance Air** | off / on | off | — | Fügt dem Wet-Pfad die Laufzeit des Mikrofonabstands hinzu. Siehe [Distance Air](#distance-air). |
| **LoCut Slope** | 12 / 24 dB/Okt. | 12 | — | Flankensteilheit des LoCut-Filters. |
| **HiCut Slope** | 12 / 24 dB/Okt. | 12 | — | Flankensteilheit des HiCut-Filters. |

Jeder in v0.3.0 hinzugekommene Parameter steht per Default auf einem Wert, der nichts verändert — eine in einer früheren Version gespeicherte Session klingt nach dem Upgrade also identisch.

## Presets

Am oberen Rand von Naves Editor sitzt eine Preset-Leiste: `[<] [Preset-Name] [>] [Save] [Save As...] [Delete] [Import...] [Export...]`. Klicke auf den Preset-Namen, um die vollständige Liste zu öffnen (zuerst Werkspresets, dann deine eigenen, beide alphabetisch); `<`/`>` blättern durch dieselbe Liste. Nave bringt zehn Werkspresets mit — was jedes einzelne bewirkt, steht in [`docs/presets.md`](presets.md). Deine eigenen Presets speichert Nave unter `~/Library/Audio/Presets/Yves Vogl/Nave/` auf macOS (`%APPDATA%\Yves Vogl\Nave\Presets\` unter Windows); „Set current as default" (im Preset-Menü) bestimmt, was eine frisch eingefügte Instanz von Nave lädt. Import/Export akzeptieren beide einzelne Preset-Dateien; Import akzeptiert zusätzlich eine `.zip`-Preset-Bank, exportiert von `PresetManager::exportBank()`.

## Eine Anmerkung zu den drei „Reset"-Schaltern

**IR Gain Match**, die beiden **Min-Phase**-Schalter und **IR Align** verändern jeweils, was tatsächlich in die Convolution-Engine geladen wird, und eine Engine neu zu laden startet sie neu — du hörst also möglicherweise eine kurze Unstetigkeit, wenn du einen davon bei laufendem Audio änderst. Das ist dasselbe Verhalten, das Nave beim Laden einer IR-Datei immer schon hatte, und es sind Einstellungen, die man einmal einstellt statt sie zu automatisieren.

Alles Kontinuierliche ist klickfrei: Blend, Mix, IR B Trim, IR B Polarity, IR B Delay, Distance und die Flankenschalter sind allesamt gefahrlos automatisierbar.

## Latenz

Nave meldet **in jeder Konfiguration null Latenz**, einschließlich Morph, Distance Air, IR B Delay und den 24-dB/Okt.-Flanken. Diese Verzögerungen sind gewollte Effekte auf dem Wet-Pfad und keine Verarbeitungslatenz — sie zu melden würde deinen Host dazu bringen, die gesamte Spur zur Kompensation zu verschieben, und das ist nicht das, worum du gebeten hast, als du das Mikrofon zurückgezogen hast.

Nave nutzt aus gutem Grund JUCEs Zero-Latency-Convolution-Algorithmus — für Reamping genutzte Cab-IRs sind kurz, und Reamping-/Tracking-Workflows sind latenzsensibel, weshalb Nave dem Host niemals eine Plugin-Delay-Kompensation meldet. Das gilt unabhängig davon, wie viele der oben genannten Features (IR Blend, Distance, LoCut/HiCut) aktiv sind.

## Tipps

- **Beginne mit LoCut/HiCut auf ihren Defaults (aus)** und bringe sie erst ein, wenn die rohe IR Formung braucht — eine gut aufgenommene Cab-IR braucht oft wenig bis gar keine zusätzliche Filterung, und unnötige Filter kosten nur Headroom und CPU ohne Nutzen.
- **Für einen druckvolleren Metal-Rhythmus-Sound** versuche, eine straffe, nah abgenommene 4x12-IR (IR A) mit einer kleinen Menge einer etwas dunkleren/räumlicheren IR B zu mischen (10–25 % Blend), statt zu einem zweiten Cab-Sim-Plugin zu greifen.
- **Distance ist ein Feinschliff, kein Tone-Shaping-Tool** — brauchst du einen bestimmten Frequenzgang, nutze stattdessen LoCut/HiCut (oder deinen EQ danach); Distance ist für eine leichte „im Raum zurückschieben"-Anpassung gedacht.
- **Klingt eine geladene IR nach Blend-/Distance-Änderungen dünn oder boxig, prüfe Level** — weder Mix, Blend noch Distance sind gegeneinander gain-kompensiert, bewusst so gebaut (damit du immer genau weißt, was du hörst), was bedeutet, dass Level die eine Stelle ist, an der du einen daraus resultierenden Pegel-Mismatch korrigierst, bevor er auf deinen Mixbus trifft.
- **Führe einen Null-Test mit deinen Default-Einstellungen durch**, falls du dir je unsicher bist, ob Nave dein Signal färbt: ohne geladene IR (oder mit IR A auf ihrem Default) und LoCut/HiCut/Distance allesamt auf ihren Defaults ist Nave ein zertifizierter bit-genauer Passthrough (siehe die projekteigenen Null-Tests in `tests/EngineTests.cpp` und `tests/CoverageTests.cpp`).
