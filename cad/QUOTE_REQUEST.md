# S6-PETG-pad-r2 — Anfrage, keine Bestellung/Fertigungsfreigabe

Stand2026-10-24. Bitte ausschließlich das gewählte Proben-/Rahmen-ZIP kalkulieren;
das komplette Projektarchiv enthält historische Geometrie und ist keine Druckbestellung. Maße in **mm**,
Skalierung **100%**. Dateien/Prüfsummen stehen im jeweiligen Manifest.
Die Servo-/Hornpassung ist noch nicht vermessen; diese Dateien sind ein **Angebotsprototyp**.

| Paket | Enthaltene Druckteile | Stückzahl |
|---|---|---:|
| `sample_quotation_package.zip` | Servohalter-Probestück +Hornplatten-Probestück |1je, insgesamt2|
| `frame_quotation_package.zip` | Torso,linker/rechter Oberschenkel,linker/rechter Unterschenkel,linker/rechter Fuß |1je, insgesamt7|

**Keine TPU-Sohlen, Motorhörner oder Gummipads drucken.** Acht gewöhnliche
selbstklebende TPE-Pads werden separat beschafft. Einzelteile und kombinierte
`QUOTE_ONLY`-Datei sind alternative Kalkulationseingaben, niemals zusätzliche Stückzahlen.
Das kombinierte Modell ist nicht in den Bestell-ZIPs; Einzelteile bevorzugen.

## Gewünschte Ausführung und getrennte Preisangaben

- PETG,schwarz; initial0,20mm Schicht,3Wände,25%Füllung. Bei notwendiger Änderung
  von Orientierung, Wandzahl oder Füllung bitte Preis/Grund getrennt nennen.
- Belastungsrichtung an Servoohren/Hornplatten beachten: keine schwache
  Schichttrennung an Befestigungslaschen. Orientierungen sind vorläufig; Support
  ist erlaubt, muss aber vollständig entfernt werden.
- Alle Durchgangslöcher/Schlitze ohne Bohren, Schneiden, Gewindeschneiden oder
  Heat-Set-Inserts durch den Schüler nutzbar liefern. Notwendige Nacharbeit
  und eine Sicht-/Maßprüfung gesondert bestätigen und einpreisen.
- Zwei Angebote: **Probe2Teile** und **Rahmen7Teile**, jeweils Material,Supportentfernung,
  Nacharbeit,Verpackung,MwSt.und Versand nach **25337,Deutschland**. Probe und Rahmen
  werden nacheinander benötigt; jede separate Lieferung berücksichtigen.
- Optionale passende12M2-Ohrschrauben/12Muttern/24Scheiben separat kalkulieren;
  nicht ungeprüft in den Druckpreis hineinrechnen. Horn-/Wellenschrauben sind noch
  unbekannt und dürfen nicht durch geratene Gewinde ersetzt werden.

## Passung und Freigabe

Motor: exakt Waveshare15024MG90S. Gehäuse22,8×12,2×28,5mm ist eine Herstellerangabe;
Ohrabstand28mm,Öffnungen,axiale Lage und Horngeometrie sind **vorläufig**.
Referenz: `drawings/interfaces.svg`, `fasteners.csv`, `physical_spec.json`.
Ohröffnung12,6×23,2mm und dia2,4mm Löcher sind CAD-Zielmaße, keine zugesicherte
Drucktoleranz. M2×8-Länge und Werkzeugzugang am echten Servo prüfen.

**Zuerst Probe am echten Servo und Originalhorn prüfen.** Ohne dokumentierte
Passung,Schraubenfreiraum,Schichtfestigkeit und vollständigen Lieferpreis≤100EUR
für den gesamten Roboter gibt es keine Rahmen-Fertigungsfreigabe. Eine STL-Prüfung
oder Rechnung allein bestätigt diese Punkte nicht. Keine Nachricht oder Bestellung
wurde durch dieses Dokument versandt.
