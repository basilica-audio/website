<!-- Generated from overture/docs/manual.md on 2026-07-16 — do not hand-edit; re-run the manual sync described in website/README.md. -->

<p align="center"><img src="assets/icon.png" alt="Overture icon" width="120"/></p>

# Overture — Benutzerhandbuch

*Der 808-Boost — dein Low End straffen, bevor es in den Gain läuft.*

## Was es ist

Overture ist ein TS-808-artiger, straffer Boost/Overdrive für Metal-Gitarre. Es ist kein vollständiger Amp-in-a-Box; es ist das kleine Pedal, das du **vor** einem High-Gain-Amp auf dem Board laufen lässt — genau der Job, den ein "modded 808" in einem echten Rig übernimmt:

1. Low End aus dem Signal entfernen, *bevor* es auf eine Clipping-/Distortion-Stufe trifft, damit Palm Mutes und Chugs auf den tiefen Saiten straff und artikuliert bleiben, statt zu einem tieffrequenten Brei zu werden, sobald die eigene Gain-Stufe des Amps sie sättigt.
2. Eine kontrollierte Menge an eigenem Drive-/Clipping-Charakter obendrauf legen, so voiced, dass sie die Front eines bereits verzerrten Amps anschiebt, statt selbst ein eigenständiges Distortion-Pedal zu sein.

## Wo es in einer Heavy-Production-Chain sitzt

Overture ist eine **Pre-Amp-Straffungs-/Boost-Stufe**, kein Cab-Sim, kein EQ, kein Kompressor. Eine typische Chain:

```
Guitar -> noise gate -> Overture (tight boost) -> amp sim / real amp front end -> cab sim -> reverb/mix bus
```

Setze es vor das ein, was in deiner Chain die "Wall of Gain" liefert (den Eingang eines echten Röhrenamps oder ein anderes Plugin, das High-Gain-Amp-Simulation übernimmt). Overtures eigene Drive-/Voicing-Regler sind standardmäßig bewusst zurückhaltend gesetzt (siehe [Tipps](#tipps)) — der Punkt ist, *zu formen, was auf die Gain-Stufe trifft*, nicht selbst die Gain-Stufe zu sein. Willst du, dass Overtures Clipper die Hauptverzerrungsquelle ist (z. B. für ein reines Boost-Rig mit einem cleanen Amp), drehe Drive weiter auf und wähle ein aggressiveres Voicing.

## Signalfluss

```
Input -> Tight (HPF, 20-400 Hz) -> Drive (0-40 dB) -> [oversampled] Voicing clipper
                                                                |
      Output <-- Mix <-- Level (output trim) <-- Tone (LPF, 1-8 kHz) <--+
        ^
        |
   delay-compensated dry path (also used by Bypass)
```

Der Clipper läuft innerhalb eines oversampelten Blocks (2x/4x/8x, wählbar über **Oversampling**), damit seine Harmonischen nicht zurück ins hörbare Band aliasen. Der von **Mix** (und von **Bypass**) genutzte Dry-Pfad wird automatisch gegen diese Oversampling-Latenz delay-kompensiert, und das Plugin meldet seine Gesamtlatenz an den Host, damit die Wiedergabe sample-genau mit jeder anderen Spur ausgerichtet bleibt. Die vollständige technische Aufschlüsselung findest du in [`docs/architecture.md`](architecture.md).

## Parameterreferenz

| Parameter | Range | Default | Unit | Was es tut |
|---|---|---|---|---|
| **Tight** | 20 – 400 | 130 | Hz | Hochpassfilter, platziert *vor* dem Clipper. Höher gedreht, entfernt es mehr Low End aus dem Signal, das die Drive-/Clipper-Stufe erreicht, und hält Palm Mutes und Chugs auf den tiefen Saiten straff, statt dass sie ausfransen, sobald die eigene Gain-Stufe des Amps sättigt. Das ist der zentrale "808-Mod"-Trick, um den herum das Plugin gebaut ist. Niedriger drehen (Richtung 20 Hz) für ein volleres, weniger gestrafftes Low End; höher drehen (Richtung 300–400 Hz) für maximale Palm-Mute-Artikulation bei tiefgestimmten Gitarren. |
| **Drive** | 0 – 40 | 8 | dB | Gain, der direkt vor dem Clipper (bestimmt durch **Voicing**) auf das Signal angewendet wird. Bei 0 dB greift der Clipper kaum; höhere Werte drücken stärker in die gewählte Nichtlinearität. Standardmäßig zurückhaltend gehalten, weil Overture einen bereits gedrivten Amp *anschieben* soll, nicht ersetzen — siehe [Tipps](#tipps). |
| **Voicing** | Asymmetric / Soft Symmetric / Hard Clip | Asymmetric | – | Wählt die Clipper-Nichtlinearität, in die die oversampelte Drive-Stufe einspeist. **Asymmetric** ist das ursprüngliche "808-Boost"-Voicing: eine einseitig ausgesteuerte, gebiaste Tanh-Kurve (Op-Amp-/Dioden-Stil), die sowohl geradzahlige als auch ungeradzahlige Harmonische erzeugt, für einen leicht asymmetrischen, "röhrenartigen" Schub. **Soft Symmetric** ist eine schlichte, unverzerrte Tanh-Kurve — glatteres, ausgewogeneres Sättigungsverhalten mit nur ungeradzahligen Harmonischen, näher an einer Push-Pull-Amp-Stufe. **Hard Clip** ist eine gerade Kappung ohne weichen Knee — die hellste und aggressivste der drei, näher an einem Fuzz-/Komparator-artigen Clip; nutze es, wenn Overture selbst echte Distortion-Arbeit leisten soll, statt nur zu straffen/boosten. Ein Voicing-Wechsel ist eine diskrete Änderung (wie ein Stompbox-Toggle), kein sanft automatisierbarer Regler — erwarte einen hörbaren Sprung im Moment des Umschaltens, keine Überblendung. |
| **Tone** | 1000 – 8000 | 6000 | Hz | Tiefpassfilter, platziert *nach* dem Clipper, zähmt das Fizz/die Härte, die die Harmonischen des Clippers hinzufügen, ohne das Fundament anzutasten. Es ist ein steiles (4. Ordnung, 24 dB/Oktave) Filter, also ein wirksames "De-Fizz"-Tool selbst nahe seinem oberen Bereich. Standardmäßig relativ hell belassen (6 kHz), damit der eigene Tone Stack deines Amps — nicht diese Pre-Clip-Straffungsstufe — die finale Höhen-Voicing übernimmt. |
| **Level** | -24 – +24 | 0 | dB | Output-Trim, angewendet nach Tone und vor dem Dry/Wet-Mix. Nutze es, um Overtures Ausgangspegel an den Rest deiner Chain anzupassen, besonders wenn du Drive stark aufgedreht hast. |
| **Mix** | 0 – 100 | 100 | % | Dry/Wet-Blend der gesamten "wet" Chain (alles von Tight bis Level) gegen das unbearbeitete Input-Signal. Bei 100 % (Default) verhält sich Overture wie ein echtes Boost-Pedal — voll im Signalweg. Niedrigere Werte mischen etwas vom Original-, unbearbeiteten Signal bei; bei genau 0 % ist der Output ein sample-genauer (delay-kompensierter) Passthrough des Inputs. |
| **Bypass** | Off / On | Off | – | Host-sichtbarer Bypass. Anders als ein simpler "Plugin stummschalten"-Bypass hält Overture seinen internen Oversampler auch im Bypass am Laufen, damit die gemeldete Plugin-Latenz (und die Delay-Kompensation deines Hosts) sich nie ändert — Bypass ein-/ausschalten überblendet sanft (über etwa eine Zehntelsekunde), statt zu klicken oder zu knacken, und führt nie zu einem Timing-Glitch auf anderen Spuren. |
| **Oversampling** | 2x / 4x / 8x | 4x | – | Oversampling-Faktor rund um den Clipper. Höhere Faktoren ergeben einen saubereren (weniger aliasten) Clipper auf Kosten von mehr CPU. **Eine Änderung dieses Parameters wird erst wirksam, wenn dein Host das Plugin das nächste Mal neu initialisiert** (z. B. bei Transport-Stop/Start, einem Samplerate-Wechsel oder erneutem Öffnen des Projekts) — nicht sofort während laufendem Audio. Das ist eine bewusste Echtzeit-Sicherheitsentscheidung: Den Oversampler neu zu konfigurieren erfordert eine Speicherallokation, die niemals auf dem Audio-Thread passieren darf. Willst du eine Änderung sofort hören, stoppe und starte die Wiedergabe neu (oder öffne das Plugin erneut), nachdem du sie geändert hast. |

## Tipps

- **Beginne mit Tight, nicht mit Drive.** Der ganze Witz am "808-Boost vor einem High-Gain-Amp"-Trick ist das Hochpassfilter, nicht der Clipper. Stelle zuerst Tight ein (100–200 Hz ist ein guter Startbereich für tiefgestimmte Rhythmusparts) bei niedrigem Drive, und füge erst dann Drive hinzu, wenn sich das Low End kontrolliert anfühlt.
- **Halte Drive zurückhaltend, wenn du danach einen echten Amp/Amp-Sim ansteuerst.** Overtures Clipper soll die Front der nächsten Gain-Stufe anstupsen, nicht mit ihr kämpfen. Klingt alles plötzlich dünn oder brüchig, drehe Drive zurück, bevor du zu Tone greifst.
- **Nutze Voicing, um den gewünschten Charakter zu treffen**, nicht nur, um mehr Gain hinzuzufügen. Asymmetric (Default) für einen klassischen 808-vor-einem-Marshall-Schub; Soft Symmetric für eine glattere, "amp-artigere" Sättigung, die gut unter einem High-Gain-Amp-Sim sitzt; Hard Clip, wenn Overture selbst ein wirklich verzerrtes Signal liefern soll (z. B. um einen cleanen Amp anzusteuern, oder als fuzz-naher Lead-Boost).
- **Tone ist ein Cleanup-Tool, kein Voicing-Tool.** Weil es steil ist (24 dB/Oktave), machen kleine Bewegungen einen hörbaren Unterschied. Nutze es, um das vom Clipper eingebrachte Fizz zu zähmen, nicht als dein Haupt-Tone-Shaping — dafür ist der eigene EQ deines Amps/Amp-Sims da.
- **Mix unter 100 % ist für parallele/gemischte Sounds** gedacht, z. B. eine kleine Menge gestrafftes/gedrivtes Signal unter eine cleane DI zu mischen für einen hybriden Rhythmus-Sound. Für den normalen "Boost-Pedal vor dem Amp"-Anwendungsfall lässt du Mix bei 100 %.
- **Bypass statt Mix bei 0 % für A/B-Vergleiche beim Mischen.** Beide nullen die wet Chain, aber Bypass ist das, was Hosts als "nativen" Bypass behandeln (Automations-Lane, Rechtsklick-Bypass in den meisten DAWs), und es hält die Latenzmeldung stabil, wenn du über mehrere Instanzen hinweg vergleichst.
- **Lass Oversampling auf 4x, sofern du keinen konkreten Grund hast, es zu ändern.** 2x spart CPU zu geringen Aliasing-Kosten (meist hörbar bei sehr hohem Drive + Hard Clip); 8x ist für Tracking/das Committen eines finalen Takes gedacht, wenn du den saubersten möglichen Clipper willst, auf Kosten zusätzlicher CPU-Last.
</content>
