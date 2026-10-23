# robot - From Simulation to Reality: How does a robot learn?

## Einstieg und aktueller Stand

Der kurze Gesamtplan für Menschen und KI steht in [SUMMARY.md](SUMMARY.md).
KI/Entwickler lesen danach [AGENTS.md](AGENTS.md) und [Status](docs/STATUS.md)
und [Roadmap](docs/ROADMAP.md). Die [generierte Übergabe mit19Abschnitten](docs/HANDOFF.md)
enthält den vollständigen Code; Preise stehen in `procurement.json`, Maße/Massen
in `physical_spec.json`. [Offene Beschaffungsfragen](docs/PROCUREMENT_ACTIONS.md),
[Hardware/Protokoll](docs/HARDWARE.md), [Firmware](firmware/README.md) und
[Kalibrierung](docs/CALIBRATION.md) sind die Arbeitsreferenzen.

**Nichts bestellt oder physisch geprüft.** Bekannte bepreiste Positionen:78,91€;
Gesamtkosten wegen fehlender Druck-/Kleinteil-/Versandpreise unbekannt.100€ist die
harte Lieferpreisgrenze. Sechs MG90S mit Pico-Direkt-PWM, MPU6050 und
kabelgebundener Versorgung sind der vorläufige Entwurf (geschätzt199,4g).
Firmware und Bench-Werkzeuge sind implementiert; echte elektrische Tests fehlen.
Das Gehziel ist noch nicht nachgewiesen. 29Tests bestehen; das Gehziel wurde im49.152Schritte-Pilot nicht erreicht.
Historische Experimente bleiben unter
`docs/validation/` erhalten und sind mit dem neuen Modell nicht kompatibel.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python tools/budget_gate.py # Exit2: Beschaffung unvollständig
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
3. Passende Druckteile bestätigen, Prototyp montieren und wiegen
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
- Raspberry Pi Pico H mit direktem PWM und MPU6050 für den echten Roboter

## Ziel

Am Ende wollen wir zeigen, wie ein Computer ohne vorprogrammierte Bewegungsabläufe selbst lernen kann und warum eine Simulation nie genau gleich wie die echte Welt ist.
