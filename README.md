# robot - From Simulation to Reality: How does a robot learn?

## Einstieg und aktueller Stand

Der kurze Gesamtplan für Menschen und KI steht in [SUMMARY.md](SUMMARY.md).
KI/Entwickler lesen danach [AGENTS.md](AGENTS.md) und [Status](docs/STATUS.md)
und [Roadmap](docs/ROADMAP.md). Die [generierte Übergabe mit19Abschnitten](docs/HANDOFF.md)
enthält den vollständigen Code; Preise stehen in `procurement.json`, Maße/Massen
in `physical_spec.json`. [Offene Beschaffungsfragen](docs/PROCUREMENT_ACTIONS.md),
[Hardware/Protokoll](docs/HARDWARE.md), [Firmware](firmware/README.md) und
[Kalibrierung](docs/CALIBRATION.md) sind die Arbeitsreferenzen.

**Nichts bestellt oder physisch geprüft.** Aktiver Entwurf: **S6-PETG-pad-r2**,
siebenPETG-Teile vom Druckservice, nackter Pico mit Stiftleisten und acht gekaufte
Haftpads. Keine gedruckten TPU-Sohlen, kein Drucker-/Filamentkauf. [Druckprobe](cad/sample_quotation_package.zip),
[7-Teile-Angebotspaket](cad/frame_quotation_package.zip), [Zeichnung](cad/print_order/drawings/interfaces.png).
Der bepreiste Korb kostet105,34€**vor** Druck/Probe/Horn-Kleinteilen: mindestens5,34€
über der100€Grenze. Eine aktuelle dateispezifische Druckquote fehlt; der STL-Upload
zuMeltlab wurde durch die automatische Freigabeprüfung blockiert.
Die vorläufige MuJoCo-Kopie passt zum neuen CAD; geschätzt197.1g.37Tests bestehen.
Der neue2048Schritte-Smoke und die manuellen Hebeversuche zeigen **kein Gehen**.
Alte Modelle/UF2bleiben historisch. [Prüfstand](docs/VALIDATION_CURRENT.md).

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python tools/budget_gate.py # Exit1: aktiver Druckservice-Weg schon vor Druck über Budget
python evaluate.py --episodes 1 --output runs/neutral_new
python train.py --steps 2048 --seed 0 --development --output runs/smoke_new
```

Größere formale A/B-Experimente sind durch dokumentierte Mess-/Modellgates
gesperrt. Kurze Entwicklungsläufe sind ausdrücklich vorläufig und beweisen
weder Gehen noch Sim-to-Real. Neue Prüfprotokolle stehen im Statusdokument.

## PPP-Woche: Robotik, ML und Simulation

## Thema
**Robotik, Machine Learning und Computersimulation**

**Leitfrage:**  
Wie kann ein Roboter eine Bewegung in einer Simulation lernen und das Gelernte danach auf einen echten Roboter übertragen?

## Teilthemen

**Kolja:**  
Reinforcement Learning – Wie kann ein Roboter durch Versuch und Irrtum lernen?

**Ilgar:**  
Sim-to-Real – Wie kann man eine in der Simulation gelernte Steuerung auf einen echten Roboter übertragen?

## Idee
Wir wählen verfügbare Bauteile, prüfen Preis und mechanischen Aufbau und bilden diesen Roboter in einer Physik-Simulation nach.
Dort soll er selbstständig lernen, sich vorwärts zu bewegen. Dafür bekommt er für gute Aktionen eine Belohnung (Reward).

Danach versuchen wir, das trainierte Modell auf einen echten Roboter zu übertragen.

Zusätzlich wollen wir testen, ob das Training besser funktioniert, wenn sich während des Trainings Dinge wie Reibung, Gewicht oder Motorstärke leicht verändern.

## Grober Plan

1. Aufgabe, verfügbare Teile und vollständigen Lieferpreis prüfen
2. Einen Motor, Stromversorgung, Controller und IMU testen und vermessen
3. Passende Standardmechanik oder später verfügbaren Probedruck bestätigen, montieren und wiegen
4. Digitale Kopie aus diesen Messungen erstellen und prüfen
5. Reinforcement-Learning-Umgebung erstellen
6. erstes Modell trainieren
7. Training mit zufällig veränderten Bedingungen
8. Ergebnisse vergleichen
9. Modell auf echten Roboter übertragen
10. Simulation und Realität vergleichen
11. Präsentation und Dokumentation fertig machen

## Was wir messen wollen

- zurückgelegte Strecke
- Geschwindigkeit
- Anzahl der Stürze
- sichtbare Fußhebung und alternierende Schritte (Rutschen zählt nicht)
- eventuell Energieverbrauch
- Unterschied zwischen Simulation und echtem Roboter

## Aufgabenverteilung

**Kolja**
- Simulation
- Reinforcement Learning
- Training
- Auswertung der Trainingsdaten

**Ilgar**
- Aufbau des echten Roboters
- Elektronik und Motoren
- Kalibrierung
- Tests in der echten Welt

**Zusammen**
- Planung
- Sim-to-Real
- Experimente
- Vergleich der Ergebnisse
- Präsentation

## Technik

- Python
- MuJoCo
- Gymnasium
- Stable-Baselines3 / PPO
- Raspberry Pi Pico mit selbst gelöteten Stiftleisten, direktem PWM und MPU6050

## Ziel

Am Ende wollen wir zeigen, wie ein Computer ohne vorprogrammierte Bewegungsabläufe selbst lernen kann und warum eine Simulation nie genau gleich wie die echte Welt ist.
