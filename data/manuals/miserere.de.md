<!-- Generated from miserere/docs/manual.md on 2026-07-16 — do not hand-edit; re-run the manual sync described in website/README.md. -->

# Miserere — Benutzerhandbuch

*Vier Stimmen, ein Gebet — die parallele Vocal-Chain in einem einzigen Plug-in.*

## Was Miserere ist

Miserere verpackt den klassischen „Rough Vocal Template"-Workflow des Parallel-Mixings in einem Plugin: eine **Direct**-Vocal-Chain plus drei **parallele Busse** — ein Opto-Leveler-Sandwich, ein aggressiver FET-Smash-Bus und ein Slap-Delay — jeweils mit eigenem Fader, Mute und Solo. Du mischst die vier Busse gegeneinander, statt an einer einzigen seriellen Chain zu schrauben.

Klassische Channel Strips arbeiten seriell: Jedes Modul verarbeitet das, was das vorherige übrig gelassen hat, und „mehr Kompression" bedeutet immer „weniger Dynamik". Der Kern von Miserere ist ECHTES paralleles Routing.

## Warum Parallel-Verarbeitung bei dichten, aber dynamischen Vocals gewinnt

Eine Vocal in einem harten Mix hat zwei widersprüchliche Aufgaben: Sie muss **dicht** genug sein, um sich über eine Wand aus Gitarren zu setzen, und **dynamisch** genug, um noch nach einem Menschen zu klingen. Eine serielle Chain zwingt dich zur Entscheidung — hart komprimieren und die Performance verlieren, oder sanft komprimieren und den Kampf gegen die Gitarren verlieren.

Parallel-Verarbeitung umgeht diese Entscheidung. Der Direct-Bus hält Transienten und Phrasierung der Vocal intakt; der Smash-Bus zerstört seine eigene Kopie des Signals (~20:1, schnell, mid-forward) und wird *unter* den direkten Sound gemischt. Je lauter die Sängerin oder der Sänger wird, desto härter limitiert der Smash-Bus — so bleibt die *Mischung* auf jedem Dynamikpegel dicht, während der Direct-Bus obendrüber weiter atmet. Der Opto-Bus ergänzt eine dritte Textur: langsames, musikalisches Leveling mit passiv anmutendem Low/High-Bloom, das den Körper auffüllt, ohne die Transienten anzutasten. Der Slap-Bus fügt das kurze, dunkle Echo hinzu, das eine trockene Vocal in einen produzierten Mix einklebt, ohne sie in Reverb zu ertränken.

Da die Busse A–C ausschließlich aus minimalphasiger Verarbeitung ohne Lookahead aufgebaut sind, bleiben alle drei **sample-aligned** — du kannst jeden Fader beliebig schieben, ohne dass die Summe je kammfiltert oder hohl klingt. (Der Slap-Bus ist absichtlich ein Delay.)

## Signalfluss

```
                 ┌─ BUS A "Direct":  HPF → Console EQ → FET Comp → De-Esser → Tape Sat ── fader ─┐
in ─ [In Trim] ─┼─ BUS B "Opto":    Passive EQ in → Opto Leveler → Passive Air out ───── fader ─┼─ Σ ─ [Out Trim] ─ out
                 ├─ BUS C "Smash":   FET Limiter (all-buttons, mid-forward sidechain) ─── fader ─┤
                 └─ BUS D "Slap":    Slap Delay (60–180 ms, filtered tape-soft feedback) ─ fader ─┘
```

Die technische Aufschlüsselung und die Design-Notizen zur Phasendisziplin findest du in [`architecture.md`](architecture.md).

## Die vier Busse, musikalisch betrachtet

### Bus A — Direct

Die Vocal, die du printen würdest: ein funktionierender Channel Strip, der brav bleibt.

- **HPF** (20–300 Hz, 12 dB/oct, schaltbar) — entfernt Rumpeln, Plosiv-Peaks und Mud unterhalb der Stimme.
- **Console EQ** — ein dreibandiger EQ im Stil britischer Konsolen: Low Shelf bei 100 Hz, eine sweepbare Mid Bell (250 Hz–5 kHz, Q 0.7–2), High Shelf bei 8 kHz, alle ±15 dB. Breite Pinselstriche, keine Chirurgie.
- **FET Comp** — ein schneller Kompressor im FET-Stil mit 4:1 oder 8:1 Ratio und Makeup Gain. Das ist die „Peaks einfangen"-Stufe — 3–6 dB Gain Reduction auf den lautesten Zeilen ist die klassische Einstellung.
- **De-Esser** — Split-Band, einstellbar 4–9 kHz, bis zu 10 dB Reduktion. Sitzt *nach* dem Kompressor, weil Kompression Zischlaute verstärkt.
- **Tape Sat** — 0–24 dB Drive in eine Sättigungsstufe im Tape-Stil mit Pre-/De-Emphasis, pegelkompensiert auf einen nominalen Pegel von −18 dBFS: mehr Drive bedeutet mehr Dichte, nicht mehr Lautheit.

### Bus B — Opto

Das „Sandwich": EQ in Leveler in EQ. Boost Lows und Highs *in* einen langsamen Leveler im optischen Stil hinein und lass ihn den Überschuss einfangen — der Passiv-EQ-plus-Opto-Kniff, der eine Stimme teuer klingen lässt.

- **Passive EQ in** — reiner Boost-Low-Shelf (60 oder 100 Hz, 0–10 dB) und High Shelf (8/10/12/16 kHz, 0–10 dB), breit und sanft.
- **Opto Leveler** — programmabhängiges zweistufiges Release (~60 ms schnelle Stufe in eine ~600 ms langsame Stufe; je länger er schon arbeitet, desto träger löst er — wie eine echte Photozelle, die warmgelaufen ist), sanftes ~3:1-Ratio, fixer ~10 ms Attack. Ein Peak-Reduction-Regler plus Makeup.
- **Passive Air out** — ein abschließender 12-kHz-Shelf (0–8 dB, nur Boost) *nach* dem Leveler, damit die Air nie pumpt.

### Bus C — Smash

Ein Modul, null Subtilität: ein FET-Limiter im All-Buttons-in-Charakter. Ratio um 20:1, Attack bis hinunter zu 0,05 ms, programmabhängiges *Verkürzen* des Release (je härter limitiert wird, desto schneller erholt er sich — das „nach vorne pumpende" Gefühl), und ein Sidechain, der um +6 dB bei 2 kHz angehoben ist, sodass die Mitten — wo die Stimme lebt — das Limiting antreiben. **Drive** knallt das Eingangssignal in den fixen Threshold; **Output Trim** sorgt fürs Gain Staging der Trümmer. Misch ihn unter den Direct-Bus, bis die Vocal dicht wirkt, und zieh den Fader dann 2 dB zurück.

### Bus D — Slap

Ein Slap-Echo im Tape-Stil, ausschließlich Wet (für die trockene Stimme ist Bus A zuständig): 60–180 ms fraktionales Delay, bis zu 30 % Feedback, mit einem High-Pass-/Low-Pass-Filterpaar *und* sanfter Tape-Sättigung innerhalb der Feedback-Loop, sodass jede Wiederholung dunkler und runder wird. Ein **Mono**-Schalter kollabiert das Echo auf zentriertes Mono — der klassische Mono-Slap hinter einer breiten Vocal.

## Fader-Logik

- Jeder Bus hat **Level** (−60…+6 dB; der untere Anschlag des Faders ist ein echtes Off), **Mute** und **Solo**.
- **Solo ist exklusiv**: Wenn du einen Bus soloest, wird jedes andere Solo aufgehoben — du hörst immer genau einen Bus isoliert.
- **Mute gewinnt gegen Solo** auf demselben Bus, wie an einer Konsole.
- Ab Werk ist nur der Direct-Bus oben; die drei parallelen Busse starten am unteren Fader-Anschlag. Miserere tut nichts mit deiner Vocal, bis du einen Fader hochziehst.

## Parameterübersicht

| Parameter | Bereich | Standard | Einheit | Hinweise |
|---|---|---|---|---|
| In Trim / Out Trim | −12…+12 | 0 | dB | Globales Gain Staging rund um die gesamte Parallelstruktur. |
| Bypass | off/on | off | – | Für den Host sichtbarer Bypass-Parameter. |
| **Bus A — Direct** | | | | |
| HPF / HPF Freq | off/on, 20–300 | on, 80 | Hz | 12 dB/oct High-Pass. |
| EQ Low | −15…+15 | 0 | dB | Low Shelf, 100 Hz. |
| Mid Freq / Mid Gain / Mid Q | 250–5k / −15…+15 / 0.7–2 | 1k / 0 / 1 | Hz, dB | Sweepbare Bell. |
| EQ High | −15…+15 | 0 | dB | High Shelf, 8 kHz. |
| Ratio | 4:1, 8:1 | 4:1 | – | Ratio des FET Comp. |
| Threshold | −40…0 | −18 | dB | Threshold des FET Comp. |
| Attack / Release | 0.1–10 / 50–1100 | 3 / 150 | ms | Ballistik des FET Comp. |
| Makeup | 0…24 | 0 | dB | Makeup Gain des FET Comp. |
| De-Ess / Freq / Thr | off/on, 4k–9k, −40…0 | on, 6.5k, −24 | Hz, dB | Split-Band, max. 10 dB Reduktion. |
| Sat Drive | 0…24 | 6 | dB | 0 dB ist ein exakter Bypass. |
| **Bus B — Opto** | | | | |
| Low Boost Freq / Gain | 60/100, 0–10 | 100, 0 | Hz, dB | Reiner Boost-Shelf im passiven Stil. |
| High Boost Freq / Gain | 8k/10k/12k/16k, 0–10 | 12k, 0 | Hz, dB | Reiner Boost-Shelf im passiven Stil. |
| Peak Reduction | 0–100 | 40 | % | 0 % ist ein exakter Bypass. |
| Makeup | 0…24 | 0 | dB | Gain nach dem Leveler. |
| Air | 0…8 | 0 | dB | 12-kHz-Shelf nach dem Leveler. |
| **Bus C — Smash** | | | | |
| Attack / Release | 0.05–0.8 / 50–200 | 0.3 / 100 | ms | Release verkürzt sich bei starkem Limiting. |
| Drive | 0…12 | 0 | dB | Eingangssignal knallt in den fixen Threshold. |
| Output Trim | −12…+12 | 0 | dB | Gain Staging nach dem Limiter. |
| **Bus D — Slap** | | | | |
| Delay | 60–180 | 110 | ms | Fraktionales (sample-genaues) Delay. |
| Feedback | 0–30 | 15 | % | Bedingungslos stabil. |
| Loop HP / Loop LP | 50–1k / 2k–10k | 200 / 5k | Hz | Filter innerhalb der Feedback-Loop. |
| Mono | off/on | off | – | Kollabiert das Echo auf Mono. |
| **Pro Bus** | | | | |
| Level | −60…+6 | A: 0, B/C/D: −60 | dB | −60 dB ist ein echtes Off. |
| Mute / Solo | off/on | off | – | Solo exklusiv; Mute gewinnt. |

Alle kontinuierlichen Parameter sind geglättet (kein Zipper-Noise) und automatisierungssicher.

## Starter-Rezepte

### Lead-Vocal (die Rough-Vorlage)

1. Bus A: HPF ~80–100 Hz, ein bis zwei dB Air im Bereich 10 kHz über EQ High, FET Comp bei 4:1 mit 3–5 dB Gain Reduction auf den lauten Zeilen, De-Esser an, Sat Drive auf dem Default von 6 dB.
2. Zieh **Bus B** auf etwa −6 dB unter den Direct-Pegel hoch: Peak Reduction ~40–50 %, 2–3 dB Low Boost bei 100 Hz und High Boost bei 12 kHz. Die Stimme bekommt Körper und Glanz, ohne den Direct-Pfad zu EQen.
3. Zieh **Bus C** vom Boden hoch, bis du ihn eher *fühlst* als hörst (meist −10 bis −6 dB unter dem Direct-Pegel), Drive nach Geschmack. Die Vocal verschwindet in den Chorus-Passagen nicht mehr.
4. **Bus D**: 100–120 ms, Feedback ~10–15 %, Mono an, knapp an der Hörbarkeitsgrenze versteckt.

### Aggressive Vocal (Screams, geschriene Leads)

1. Bus A: HPF höher (~120 Hz), 8:1-Ratio, schnellerer Attack (~1 ms), niedrigerer De-Esser-Threshold — harte Quellen treffen härter.
2. Bus C wird zum Star: Fader nur wenige dB unter dem Direct-Pegel, Drive 6–12 dB. Der mid-forward Sidechain hält das Limiting auf den Kern des Screams fokussiert, nicht auf Cymbal-Übersprechen.
3. Bus B weglassen oder subtil halten — Opto-Bloom kann eine aggressive Quelle zu stark weichzeichnen.
4. Bus D mit kürzerem Delay (60–80 ms) und Loop LP heruntergezogen auf ~3 kHz liest sich bei hoher Aggression eher als „Size" denn als „Echo".

### Drum-Bus-Missbrauch

Parallelkompression wurde auf Drums geboren, und Miserere kontrolliert nicht, was du ihm zuführst:

1. Bus A fast neutral: HPF aus oder sehr niedrig, EQ flach, Comp-Threshold hoch (oder bei 0 dB für einen sauberen Durchlauf), De-Esser aus, Drive 0 — ein sauberer Direct-Pfad.
2. Bus C laut hochziehen: Drive 6+ dB. Das ist der klassische All-Buttons-Parallel-Drum-Crush — explosive Room-Energie unter einem unangetasteten Close-Mic-Bild.
3. Bus B statt (oder zusammen mit) C für eine rundere, verklebtere Dichte: 60 Hz Low und 10 kHz High in den Leveler hinein boosten.
4. Bus D bei 60–80 ms mit Mono an fügt einen trashigen, kurzen Fake-Room hinzu. Eigentlich falsch, aber oft genial.

## Tipps

- **Stell zuerst den Direct-Bus alleine ein.** Soloe Bus A, bring ihn auf einen guten, leicht konservativen Vocal-Channel-Sound, dann *Solo aufheben* und die Parallel-Mischung darum herum aufbauen.
- **Nutze für die Balance die Fader, nicht die Modul-Regler.** Das ist der ganze Sinn der Topologie: Sobald jeder Bus solo richtig klingt, mischst du sie wie Tracks.
- **Der Smash-Bus soll solo furchtbar klingen.** Klingt er für sich allein gut, ist er vermutlich nicht stark genug komprimiert, um seinen Job in der Mischung zu erledigen.
- **Behalte die Summe im Blick.** Drei Busse derselben Vocal summieren sich: 6–10 dB Headroom auf Out Trim sind normal, wenn alles hochgezogen ist.
- **Null Latenz, parallel-sicher.** Miserere meldet 0 Samples Latenz und ist damit an jeder Stelle einer Chain sicher einsetzbar, auch neben anderen Parallel-Bussen in deiner DAW.

## Bekannte Einschränkungen (v0.1.0)

- Das GUI ist ein funktionaler Slider-/Knob-Editor (ein individuelles Vektor-GUI mit Nadelinstrumenten pro Bus ist Milestone M3).
- Noch keine Werkspresets (M2).
- Modul-Slots sind fest; austauschbare Alternativen pro Slot (z. B. eine VCA-artige Option in den Kompressor-Slots) sind ein Roadmap-Punkt für M2.
- Die Tape-Sat-Stufe läuft in M1 ohne Oversampling — bei vocal-typischen Drive-Mengen liegen ihre Aliasing-Produkte weit unter dem Programmmaterial; ein Oversampling-Upgrade ist eine Voicing-Entscheidung für M2+.
- Die Dynamikerkennung erfolgt auf allen Bussen pro Kanal (nicht stereo-linked); bei einer Stereoquelle mit stark asymmetrischem Bild können die beiden Kanäle leicht unterschiedlich komprimiert werden.
