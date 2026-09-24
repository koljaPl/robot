# robot - From Simulation to Reality: How does a robot learn?

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
Wir bauen einen einfachen Roboter zuerst in einer Physik-Simulation nach.  
Dort soll er selbstständig lernen, sich vorwärts zu bewegen. Dafür bekommt er für gute Aktionen eine Belohnung (Reward).

Danach versuchen wir, das trainierte Modell auf einen echten Roboter zu übertragen.

Zusätzlich wollen wir testen, ob das Training besser funktioniert, wenn sich während des Trainings Dinge wie Reibung, Gewicht oder Motorstärke leicht verändern.

## Grober Plan

1. Aufgabe und Roboter festlegen
2. Physik und Aufbau des Roboters planen
3. Roboter in der Simulation bauen
4. echten Roboter / Prototyp bauen
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
- ESP32 oder ähnlicher Controller für den echten Roboter

## Ziel

Am Ende wollen wir zeigen, wie ein Computer ohne vorprogrammierte Bewegungsabläufe selbst lernen kann und warum eine Simulation nie genau gleich wie die echte Welt ist.
