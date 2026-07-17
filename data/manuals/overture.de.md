<!-- German translation of overture.en.md — maintained by hand; re-translate after the English source changes (see website/README.md). -->

<p align="center"><img src="assets/icon.png" alt="Overture-Icon" width="120"/></p>

# Overture — Bedienungsanleitung

*Der 808-Boost — dein Low End straffen, bevor es in den Gain läuft.*

## Was es ist

Overture ist ein TS-808-artiger, straffer Boost/Overdrive für Metal-Gitarre. Es ist kein vollständiger Amp-in-a-Box; es ist das kleine Pedal, das du **vor** einem High-Gain-Amp auf dem Board laufen lässt — und dabei genau die Aufgabe erfüllt, die ein „modded 808" in einem echten Rig hat:

1. Low End aus dem Signal entfernen, *bevor* es auf eine Clipping-/Distortion-Stufe trifft, damit Palm Mutes und Chugs auf den tiefen Saiten straff und artikuliert bleiben, statt zu einem tieffrequenten Brei zu werden, sobald die eigene Gain-Stufe des Amps sie sättigt.
2. Eine kontrollierte Menge an eigenem Drive-/Clipping-Charakter obendrauf legen, so voiced, dass sie die Front eines bereits verzerrten Amps anschiebt, statt selbst ein eigenständiges Distortion-Pedal zu sein — seit v0.2.0 mit einem echten frequenzselektiven, drive-abhängigen Clipping-Verhalten statt einer Nichtlinearität mit fester Kurvenform (siehe [Was sich in v0.2.0 geändert hat](#was-sich-in-v020-geändert-hat) weiter unten).

## Wo es in einer Heavy-Production-Chain sitzt

Overture ist eine **Pre-Amp-Straffungs-/Boost-Stufe**, kein Cab-Sim, kein EQ, kein Kompressor. Eine typische Chain:

```
Guitar -> noise gate -> Overture (tight boost) -> amp sim / real amp front end -> cab sim -> reverb/mix bus
```

Setze es vor das ein, was in deiner Chain die „Wall of Gain" liefert (den Eingang eines echten Röhrenamps oder ein anderes Plugin, das High-Gain-Amp-Simulation übernimmt). Overtures eigene Drive-/Voicing-Regler sind standardmäßig bewusst zurückhaltend gesetzt (siehe [Tipps](#tipps)) — der Punkt ist, *zu formen, was auf die Gain-Stufe trifft*, nicht selbst die Gain-Stufe zu sein. Willst du, dass Overtures Clipper die Hauptverzerrungsquelle ist (z. B. für ein reines Boost-Rig mit einem cleanen Amp), drehe Drive weiter auf und wähle ein aggressiveres Voicing — siehe die Werkspresets **Own Distortion** und **Fuzz-Adjacent Lead**.

## Signalfluss

```
Input -> Tight (HPF, 20-400 Hz) -> Drive (0-40 dB) -> [oversampled]
           Bite shelf (~700 Hz, inside the drive-to-clipper path)
           -> Voicing clipper (variable Asymmetry) -> Knee Soften blend
                                                                |
      Output <-- Mix <-- Level <-- Bite Tilt (+/-3 kHz shelf) <-+
        ^
        |
   delay-compensated dry path (also used by Bypass)
```

Der Clipper (und der Bite-Shelf davor) läuft innerhalb eines oversampelten Blocks (2x/4x/8x, wählbar über **Oversampling**), damit Harmonische nicht zurück ins hörbare Band aliasen. Der von **Mix** (und von **Bypass**) genutzte Dry-Pfad wird automatisch gegen diese Oversampling-Latenz delay-kompensiert, und das Plugin meldet seine Gesamtlatenz an den Host, damit die Wiedergabe sample-genau mit jeder anderen Spur ausgerichtet bleibt. Die vollständige technische Aufschlüsselung findest du in [`docs/architecture.md`](architecture.md).

## Parameterreferenz

| Parameter | Range | Default | Unit | Was es bewirkt |
|---|---|---|---|---|
| **Tight** | 20 – 400 | 100 | Hz | Hochpassfilter, platziert *vor* dem Clipper. Höher gedreht, entfernt es mehr Low End aus dem Signal, das die Drive-/Clipper-Stufe erreicht, und hält Palm Mutes und Chugs auf den tiefen Saiten straff, statt dass sie ausfransen, sobald die eigene Gain-Stufe des Amps sättigt. Das ist der zentrale „808-Mod"-Trick, um den herum das Plugin gebaut ist. Niedriger drehen (Richtung 20 Hz) für ein volleres, weniger gestrafftes Low End; höher drehen (Richtung 300–400 Hz) für maximale Palm-Mute-Artikulation bei tiefgestimmten Gitarren. Der Default von v0.2.0 (100 Hz, vorher 130 Hz) liegt zentral im dokumentierten Sweet Spot von 80–120 Hz für diesen Workflow — siehe [Was sich in v0.2.0 geändert hat](#was-sich-in-v020-geändert-hat). |
| **Drive** | 0 – 40 | 3 | dB | Gain, der direkt vor dem Clipper (bestimmt durch **Voicing**) auf das Signal angewendet wird. Bei 0 dB greift der Clipper kaum; höhere Werte drücken stärker in die gewählte Nichtlinearität. Der Default von v0.2.0 (3 dB, vorher 8 dB) liegt in der am besten dokumentierten Region der Technik — „nahe null Drive, Level übernimmt das Schieben" — siehe [Was sich in v0.2.0 geändert hat](#was-sich-in-v020-geändert-hat). |
| **Bite** | 0 – 100 | 65 | % | Frequenzabhängiger Gain *innerhalb* der Drive-zu-Clipper-Stufe (neu in v0.2.0) — ein fester Low-Shelf bei ~700 Hz, der den Drive, der den Clipper unterhalb des Shelfs erreicht, progressiv reduziert, skaliert durch diesen Regler, sodass Bass *weniger* geclippt wird als Treble. Das ist der eigentliche Mechanismus, den die Referenzschaltung für „Tightness" nutzt (kein separates Filter vor Drive — das bleibt weiterhin die Aufgabe von Tight). Bei 0 % ist der Gain des Clippers frequenzunabhängig flach, identisch zum Verhalten des Clippers in v0.1. |
| **Knee Soften** | 0 – 100 | 40 | % | Drive-abhängige Knee-Erweichung (neu in v0.2.0) — überblendet die Transferfunktion jedes Voicings in Richtung einer Variante mit weicherem Knee, ausgeprägter, je härter Drive den Clipper antreibt. Gilt für alle drei Voicings, einschließlich Hard Clip (das sonst bei jedem Drive-Level einen Knee von null hat). Bei 0 % behält jedes Voicing seine exakte, fixe Knee-Form bei jedem Drive-Level bei — wie in v0.1. |
| **Asymmetry** | 0 – 100 | 40 | % | Legt den internen Bias des Asymmetric-Voicings offen (neu in v0.2.0 — in v0.1 war er eine fixe Konstante), gemappt auf einen Bias von 0.0 (vollständig symmetrisch) bis 0.5 (maximal asymmetrisch). Wirkt sich nur auf das Asymmetric-Voicing aus — Soft Symmetric und Hard Clip ignorieren ihn. Der Default (40 %) reproduziert exakt den fixen Bias von v0.1. |
| **Voicing** | Asymmetric / Soft Symmetric / Hard Clip | Asymmetric | – | Wählt die Clipper-Nichtlinearität, in die die oversampelte Drive-/Bite-Stufe einspeist. **Asymmetric** ist das ursprüngliche „808-Boost"-Voicing: eine einseitig ausgesteuerte, gebiaste Tanh-Kurve (Op-Amp-/Dioden-Stil, Bias eingestellt über Asymmetry), die sowohl geradzahlige als auch ungeradzahlige Harmonische erzeugt, für einen leicht asymmetrischen, „röhrenartigen" Schub. **Soft Symmetric** ist eine schlichte, unverzerrte Tanh-Kurve — glatteres, ausgewogeneres Sättigungsverhalten mit nur ungeradzahligen Harmonischen, näher an einer Push-Pull-Amp-Stufe. **Hard Clip** ist eine gerade Kappung ohne weichen Knee (sofern nicht über Knee Soften erweicht) — die hellste und aggressivste der drei, näher an einem Fuzz-/Komparator-artigen Clip; nutze es, wenn Overture selbst echte Distortion-Arbeit leisten soll, statt nur zu straffen/boosten. Ein Voicing-Wechsel ist eine diskrete Änderung (wie ein Stompbox-Toggle), kein sanft automatisierbarer Regler — erwarte einen hörbaren Sprung im Moment des Umschaltens, keine Überblendung. |
| **Bite Tilt** | -100 – +100 | 0 | % | Bidirektionaler Tilt nach dem Clipping um einen festen ~3-kHz-Eckpunkt (neu in v0.2.0, ersetzt das reine Cut-Tone von v0.1). Negative Werte verdunkeln (und decken damit den gesamten Cut-Bereich von v0.1s Tone ab); positive Werte hellen auf — eine Fähigkeit, die v0.1 komplett fehlte. Flat (0 %, Default) ist ein echter No-op. Wie der Tone-Wert einer alten v0.1-Session auf diesen Regler gemappt wird, erklärt [Was sich in v0.2.0 geändert hat](#was-sich-in-v020-geändert-hat). |
| **Level** | -24 – +24 | 0 | dB | Output-Trim, angewendet nach Bite Tilt und vor dem Dry/Wet-Mix. Nutze es, um Overtures Ausgangspegel an den Rest deiner Chain anzupassen, besonders wenn du Drive stark aufgedreht hast. |
| **Mix** | 0 – 100 | 100 | % | Dry/Wet-Blend der gesamten „wet" Chain (alles von Tight bis Level) gegen das unbearbeitete Input-Signal. Bei 100 % (Default) verhält sich Overture wie ein echtes Boost-Pedal — voll im Signalweg. Niedrigere Werte mischen etwas vom Original-, unbearbeiteten Signal bei; bei genau 0 % ist der Output ein sample-genauer (delay-kompensierter) Passthrough des Inputs. |
| **Bypass** | Off / On | Off | – | Host-sichtbarer Bypass. Anders als ein simpler „Plugin stummschalten"-Bypass hält Overture seinen internen Oversampler auch im Bypass am Laufen, damit die gemeldete Plugin-Latenz (und die Delay-Kompensation deines Hosts) sich nie ändert — Bypass ein-/ausschalten überblendet sanft (über etwa eine Zehntelsekunde), statt zu klicken oder zu knacken, und führt nie zu einem Timing-Glitch auf anderen Spuren. |
| **Oversampling** | 2x / 4x / 8x | 4x | – | Oversampling-Faktor rund um den Clipper (und den Bite-Shelf). Höhere Faktoren ergeben einen saubereren (weniger aliasten) Clipper auf Kosten von mehr CPU. **Eine Änderung dieses Parameters wird erst wirksam, wenn dein Host das Plugin das nächste Mal neu initialisiert** (z. B. bei Transport-Stop/Start, einem Samplerate-Wechsel oder erneutem Öffnen des Projekts) — nicht sofort während laufendem Audio. Das ist eine bewusste Echtzeit-Sicherheitsentscheidung: Den Oversampler neu zu konfigurieren erfordert eine Speicherallokation, die niemals auf dem Audio-Thread passieren darf. Willst du eine Änderung sofort hören, stoppe und starte die Wiedergabe neu (oder öffne das Plugin erneut), nachdem du sie geändert hast. |

## Presets

Overture bringt neun Werkspresets mit (ein zertifizierter **Default** plus acht anwendungsfallgetriebene Ausgangspunkte — die vollständige Liste mit der Absicht hinter jedem Preset findest du in [`docs/presets.md`](presets.md)). Die am oberen Rand des Editors angedockte Preset-Leiste lässt dich Werks-/User-Presets durchsuchen, eigene speichern (`~/Library/Audio/Presets/Yves Vogl/Overture/` auf macOS), einzelne Presets oder zip-Bänke importieren/exportieren und ein beliebiges Preset (auch deine eigenen) als den Default markieren, der bei einer frischen Instanz geladen wird.

## Was sich in v0.2.0 geändert hat

v0.2.0 ist eine recherchebasierte Überarbeitung des Drive -> Clipper -> Tone-Abschnitts der Kette, gestützt auf veröffentlichte Schaltungsanalysen der Referenzklasse-Technik „Tube-Screamer-vor-einem-High-Gain-Amp", die eigene Dokumentation eines dafür gebauten kommerziellen Pedals sowie öffentlich berichtete Artist-Workflows — **von diesem Projekt nicht gegen physische Referenzhardware oder Original-Hersteller-Schaltpläne/Datenblätter gemessen**. Die vollständigen, quellenbelegten Erkenntnisse findest du in [`docs/research-notes.md`](research-notes.md), die Begründung für jede einzelne Änderung unten in [`docs/design-brief.md`](design-brief.md).

- **Bite** (neu) ersetzt die Annahme, dass ein reines Pre-Clip-Filter (Tight) „Tightness" vollständig erklärt — die Referenzschaltung clippt Bass tatsächlich dynamisch *weniger* als Treble, innerhalb ihrer eigenen Clipping-Stufe. Bite bildet diesen Mechanismus nach; Tight erledigt weiterhin seinen ursprünglichen, separaten Pre-Clip-Job.
- **Knee Soften** (neu) und **Asymmetry** (neu) legen Verhaltensweisen offen, über die die Clipper von v0.1 keine Kontrolle hatten: einen Knee, der mit steigendem Drive weicher wird, und einen variablen Grad an asymmetrischem Bias (vorher fix).
- **Bite Tilt** ersetzt Tone: Der Tone-Regler der Referenzschaltung ist ein Boost/Cut-Tilt um einen festen Eckpunkt, kein reiner Cut-Tiefpass. Der Tone-Wert einer alten Session wird beim Laden verlustbehaftet, automatisch auf eine äquivalente Bite-Tilt-Position gemappt (vollständig geschlossenes Tone -> maximal dunkles Bite Tilt; vollständig offenes Tone -> flach) — keine mathematisch exakte Entsprechung, da die beiden Regler tatsächlich unterschiedliche Kurvenformen haben.
- **Geänderte Defaults**: Tight 130 -> 100 Hz (der Mittelpunkt des dokumentierten Sweet Spots von 80–120 Hz für diesen Workflow); Drive 8 -> 3 dB (der am besten dokumentierte, kanonische Workflow nutzt nahezu null Clipper-Drive, wobei Level/der Amp die eigentliche Verzerrung übernimmt — siehe die Presets **Clean Push** und **Classic Boost**).
- Mehrere neue Defaults (Bite 65 %, Knee Soften 40 %, die 0.5-Mapping-Obergrenze von Asymmetry, der ~3-kHz-Eckpunkt von Bite Tilt) sind **begründete Engineering-Entscheidungen, verankert im quellenbelegten qualitativen Verhalten, keine direkt aus einer Quelle übernommenen Zahlen** — einzeln gekennzeichnet in `docs/design-brief.md`, nicht als gemessene Hardware-Werte dargestellt.
- „Tube Screamer", „Horizon Devices Precision Drive", „Misha Mansoor" und „Ola Englund" werden in den Research Notes als dokumentierte öffentliche Quellen für die *Technik* genannt, ohne dass dies eine Befürwortung, ein Sponsoring oder eine Zugehörigkeit durch eine Person oder Marke impliziert.

## Tipps

- **Beginne mit Tight, nicht mit Drive.** Der ganze Witz am „808-Boost-vor-einem-High-Gain-Amp"-Trick ist das Hochpassfilter, nicht der Clipper. Stelle zuerst Tight ein (100–200 Hz ist ein guter Startbereich für tiefgestimmte Rhythmusparts) bei niedrigem Drive, und füge erst dann Drive hinzu, wenn sich das Low End kontrolliert anfühlt.
- **Probiere Drive zuerst nahe null.** Die am besten dokumentierte Version dieser Technik schiebt einen bereits gedrivten Amp an, während der Clipper kaum greift (Drive 1–3 dB), und überlässt Level und der eigenen Gain-Stufe des Amps die eigentliche Verzerrung — siehe das Preset **Clean Push**. Drive weiter aufzudrehen (10 dB+) macht Overture stärker zu einer eigenständigen Distortion-Quelle, was ebenfalls ein legitimer, unterstützter Anwendungsfall ist (siehe **Own Distortion**/**Fuzz-Adjacent Lead**), aber einen anderen Charakter hat.
- **Bite ist der „Tightness"-Regler für den Clipper selbst**, getrennt von der Pre-Clip-Filterung durch Tight. Höher drehen für einen frequenzselektiveren (bassschonenderen) Clipping-Charakter, besonders hörbar bei höherem Drive; 0 % gibt dir den schlichten, frequenzflachen Clipper von v0.1.
- **Knee Soften rundet harte Kanten ab, besonders bei höherem Drive.** Am dramatischsten wirkt es bei Hard Clip (das bei 0 % einen Knee von null hat) und am wenigsten auffällig bei Soft Symmetric (das ohnehin schon das Voicing mit dem weichsten Knee ist).
- **Halte Drive zurückhaltend, wenn du danach einen echten Amp/Amp-Sim ansteuerst.** Overtures Clipper soll die Front der nächsten Gain-Stufe anstupsen, nicht mit ihr kämpfen. Klingt alles plötzlich dünn oder brüchig, drehe Drive zurück, bevor du zu Bite Tilt greifst.
- **Nutze Voicing, um den gewünschten Charakter zu treffen**, nicht nur, um mehr Gain hinzuzufügen. Asymmetric (Default) für einen klassischen 808-vor-einem-Marshall-Schub; Soft Symmetric für eine glattere, „amp-artigere" Sättigung, die gut unter einem High-Gain-Amp-Sim sitzt; Hard Clip, wenn Overture selbst ein wirklich verzerrtes Signal liefern soll (z. B. um einen cleanen Amp anzusteuern, oder als fuzz-naher Lead-Boost).
- **Bite Tilt ist jetzt sowohl Cleanup- als auch Voicing-Tool.** Negative Werte zähmen Fizz, das der Clipper einbringt (wie es v0.1s Tone tat); positive Werte hellen auf eine Weise auf, die v0.1 überhaupt nicht konnte — siehe die Presets **De-Fizz Cleanup** und **Fuzz-Adjacent Lead** für beide Richtungen.
- **Mix unter 100 % ist für parallele/gemischte Sounds** gedacht, z. B. eine kleine Menge gestrafftes/gedrivtes Signal unter eine cleane DI zu mischen für einen hybriden Rhythmus-Sound — siehe das Preset **Parallel Grit**. Für den normalen „Boost-Pedal-vor-dem-Amp"-Anwendungsfall lässt du Mix bei 100 %.
- **Bypass statt Mix bei 0 % für A/B-Vergleiche beim Mischen.** Beide nullen die wet Chain, aber Bypass ist das, was Hosts als „nativen" Bypass behandeln (Automations-Lane, Rechtsklick-Bypass in den meisten DAWs), und es hält die Latenzmeldung stabil, wenn du über mehrere Instanzen hinweg vergleichst.
- **Lass Oversampling auf 4x, sofern du keinen konkreten Grund hast, es zu ändern.** 2x spart CPU zu geringen Aliasing-Kosten (meist hörbar bei sehr hohem Drive + Hard Clip); 8x ist für Tracking/das Committen eines finalen Takes gedacht, wenn du den saubersten möglichen Clipper willst, auf Kosten zusätzlicher CPU-Last.
