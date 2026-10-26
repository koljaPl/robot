# robot - From Simulation to Reality: How does a robot learn?

## Einstieg und aktueller Stand

Der kurze Gesamtplan für Menschen und KI steht in [SUMMARY.md](SUMMARY.md).
KI/Entwickler lesen danach [AGENTS.md](AGENTS.md) und [Status](docs/STATUS.md)
und [Roadmap](docs/ROADMAP.md). Die [generierte Übergabe mit19Abschnitten](docs/HANDOFF.md)
enthält den vollständigen Code; Preise stehen in `procurement.json`, Maße/Massen
in `physical_spec.json`. [Offene Beschaffungsfragen](docs/PROCUREMENT_ACTIONS.md),
[Hardware/Protokoll](docs/HARDWARE.md), [Firmware](firmware/README.md) und
[Kalibrierung](docs/CALIBRATION.md) sind die Arbeitsreferenzen.
Der [erweiterte Entwicklungsplan](PLAN.md) deckt alle14Phasen ab:
erledigte Arbeiten, nächste fünf Aufgaben, elf Arbeitspakete, Vorgehen, Dateien,
Zuständigkeiten, Abhängigkeiten, Freigaben und Abbruchkriterien.
Die [Stütz-/Hebediagnose](docs/SUPPORT_DIAGNOSIS.md)
trennt vorbereitete Einbein-Posen von weiterhin fehlgeschlagenen Übergängen aus dem Stand.

**Entwurf und Druckweg am26.10.2026 vom Nutzer bestätigt.** Ein Klassenkamerad
druckt die Teile; der genaue Preis/Transport ist noch unbekannt. Kein Druckerkauf.
Controller jetzt **Raspberry Pi Pico2, RP2350**, gleiche Pins/51×21mm-Grundfläche;
Firmwareziel`pico2`; aktuelle Vorbereitungsfirmware lokal querkompiliert,
noch nicht geflasht oder elektrisch getestet. [Bauanleitung](firmware/README.md).

**[Separater Druckordner](print_for_classmate/00_START_HERE.md) /
[Druck-ZIP zum Weitergeben](print_for_classmate.zip):** erst2Passproben, danach
7Rahmenteile je1×. Deutsche Anleitung, Maße, Hashes und Zeichnungen enthalten.
Physische Passform/Festigkeit noch nicht geprüft; keine gedruckten Hörner/TPU-Sohlen.
Die Auswahlphase ist abgeschlossen; Bestellungen wurden laut Nutzer begonnen.
Der vollständige [Plan im Projektstamm](PLAN.md) wird nach jedem Arbeitsschritt geändert.
Manuelle Steuerung mit Offline-Vorschau und Kalibrierungsparität sind lokal geprüft;
reale Tests stehen aus. [Bedienung](docs/MANUAL_CONTROL.md).
Der [erste Prüfstandstest](docs/BENCH.md) lässt sich ohne USB vorab ansehen;
Hardwarezugriff benötigt ausdrücklich `--execute`.
[Messdatenprüfung](docs/MEASUREMENT_INTAKE.md) und [Antwortkurvenvergleich](docs/RESPONSE_REVIEW.md)
sind implementiert; separate Prüfdaten ändern die Anpassungsparameter nicht. Rechnerischer
Budgetnachweis bleibt separat offen; keine erfundenen Druckkosten.

Die vorläufige MuJoCo-Kopie passt zum neuen CAD; geschätzt197.1g.
Aktueller lokaler Gesamtlauf:186bestandene Tests; kein neues PPO/physisches Ergebnis.
Der2048Schritte-PPO-Smoke zeigt **kein gelerntes Gehen**; Skriptreferenzen werden separat bewertet.
Alte Modelle/UF2bleiben historisch. [Prüfstand](docs/VALIDATION_CURRENT.md).
Eine neue [Standbein-/Schrittdiagnose](docs/STANCE_TRANSFER.md) erreicht einen
geprüften simulierten Schritt aus dem Stand, auch gespiegelt. Die neuere
[Schrittreferenz mit Gewichtsübergabe](docs/REFERENCE_GAIT.md) erreicht vier
abwechselnde Schritte und6,6cm in30s im nominalen Modell; mit randomisierten
Parametern im historischen Modell nur0–1Schritte. Das30cm-Ziel bleibt offen.
Die [Einzelparameterprüfung](docs/SENSITIVITY.md) korrigiert einen Modellfehler:
Kalibrierfehler verschwinden nun nicht mehr an Befehlsgrenzen. Nominale Bewegung,
Geometrie und Kraftgrenzen bleiben gleich; alle12getesteten±1°Gelenkfehler verlieren
Schritte. Aktuelle Pico2-Identität`685e3802…`; Policies/alte UF2sind historisch.
Die neue Vorbereitungsfirmware enthält absichtlich keine gültige Policy-Kalibrierung.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q tests
python tools/budget_gate.py # Exit1: aktiver Druckservice-Weg schon vor Druck über Budget
python evaluate.py --episodes 1 --output runs/neutral_new
MPLCONFIGDIR=/tmp/s6-mpl python tools/sensitivity_probe.py --cases nominal --output runs/sensitivity_new
```

Größere formale A/B-Experimente sind durch dokumentierte Mess-/Modellgates
gesperrt. Kurze Entwicklungsläufe sind ausdrücklich vorläufig und beweisen
weder Gehen noch Sim-to-Real. Neue Prüfprotokolle stehen im Statusdokument.
Jetzt kein weiteres PPO: erst Budget/Passprobe und reale Kalibrierdaten klären.

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
- Raspberry Pi Pico2 mit selbst gelöteten Stiftleisten, direktem PWM und MPU6050

## Ziel

Am Ende wollen wir zeigen, wie ein Computer ohne vorprogrammierte Bewegungsabläufe selbst lernen kann und warum eine Simulation nie genau gleich wie die echte Welt ist.
