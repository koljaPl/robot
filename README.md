# robot - From Simulation to Reality: How does a robot learn?

## Implementierung und aktueller Stand

Die [vollständige Übergabe mit 19 Abschnitten](docs/HANDOFF.md) enthält recherchierte Teile, Preise/Links, mechanische Spezifikation, Verkabelung, vollständigen Code, Kalibrierung und Baufolge. [Prüfprotokoll](docs/VALIDATION.md), [CAD/Explosionszeichnung](cad/ASSEMBLY.md), [Druckanfrage](cad/QUOTE_REQUEST.md) und [Simulationsvideo](docs/validation/nominal.mp4) liegen ebenfalls bei.

**Hardware noch nicht zum Kauf freigegeben:** Der bekannte Betrag einschließlich Versand beträgt **90,32 €**. Für Druckteile, passende Hörner/Schrauben und einen ausreichend belastbaren Stromanschluss bleiben 9,68 €; diese Kosten sind noch unbekannt. Es wurde nichts bestellt oder an echter Hardware getestet. Das Modell und die Druckdateien sind vorläufig.

Die Simulation ist lauffähig: sechs Gelenke (Hüft-Pitch, Knie-Pitch, Knöchel-Roll je Bein), geschätzte Masse 208,4 g, 50-Hz-Steuerung und IMU-basierte Beobachtungen ohne erfundene Gelenkrückmeldung. Zwölf Tests bestanden. Ein PPO-Testlauf mit 10.240 Schritten und zehn Auswertungen zeigte 30 Sekunden Stehen, **keine alternierenden Schritte** und nur etwa 1–2 mm Vorwärtsbewegung. Das Gehziel ist noch nicht erreicht.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python evaluate.py --episodes 1 --output runs/neutral
python train.py --steps 2048 --seed 0 --output runs/smoke
python evaluate.py --model runs/smoke/final_model.zip --episodes 5 --seed 1000
```

Ein geprüftes Testmodell liegt unter `docs/validation/smoke_checkpoint.zip`. Video:

```bash
MUJOCO_GL=egl python evaluate.py --model docs/validation/smoke_checkpoint.zip --episodes 1 --video --output runs/video
```

Die Hardware-Kommunikation ist als begrenztes Protokoll mit Watchdog/Arming und Pseudocode beschrieben; deploybare Firmware und automatische Hardware-Steuerung sind noch nicht implementiert.

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
- Raspberry Pi Pico H, PCA9685 und MPU6050 für den echten Roboter

## Ziel

Am Ende wollen wir zeigen, wie ein Computer ohne vorprogrammierte Bewegungsabläufe selbst lernen kann und warum eine Simulation nie genau gleich wie die echte Welt ist.
