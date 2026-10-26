# Druckdateien für den Schulroboter S6

## Reihenfolge und Stückzahlen

1. **Zuerst `01_FIT_SAMPLE`: beide STL-Dateien je 1× drucken.**
   Servo-Halter und Hornplatte mit dem echten MG90S, Originalhorn und Schrauben
   testen. Nicht bohren, aufbiegen oder mit Gewalt montieren. Bei schlechtem Sitz
   Maße/Fotos zurückgeben und Dateien korrigieren, bevor der ganze Rahmen entsteht.
2. **Danach `02_FRAME`: sieben STL-Dateien je 1×**, sobald die Probe passt:
   `torso`, `left_thigh`, `right_thigh`, `left_shin`, `right_shin`,
   `left_foot`, `right_foot`. Links/rechts nicht zusätzlich spiegeln.
3. Die zwei Probestücke gehören nicht in den fertigen Roboter. Keine zusätzlichen
   kombinierten Platten, Servohörner oder TPU-Sohlen drucken. Acht gekaufte Pads
   werden später an den Füßen befestigt.

## Einstellungen und Prüfung im Slicer

- Alle STL-Dateien sind **Millimeter**, Skalierung **100%**. Jede enthält genau
  ein Teil und ist bereits zur Druckbett-Lage gedreht. Abmessungen im Manifest
  gegen den Slicer prüfen; die Dateien einzeln importieren/auf die Platte setzen.
- Material **PETG**, zunächst **0,20 mm Schichthöhe, 3 Wände, 25% Infill**.
  Das sind Startwerte; Schichthaftung, Brücken und belastete Laschen im Slicer
  prüfen. Drucklage nicht blind ändern; siehe `03_DRAWINGS/ORIENTATION_REVIEW.md`.
- Passende PETG-Temperatur/Lüftung nach dem tatsächlich verwendeten Filament wählen.
  Falls nötig Stützen verwenden und vollständig entfernen, ohne dünne Laschen
  zu beschädigen. Keine neuen Schraublöcher im Teil durch Stützen verschließen.
- Montagebohrungen/Schlitze müssen nach dem Druck nutzbar sein. Falls die Probe
  nicht passt oder Nacharbeit nötig wäre, vor dem Rahmendruck Rücksprache halten.
- Einzelteil-Maße, Layerfehler und Verzug prüfen; fertig gedruckte Teile wiegen.
  Druckzeit, Filamentverbrauch und tatsächliche Kosten bitte notieren.

## Stand und Unterlagen

Der Nutzer hat Drucken beim Klassenkameraden als Vorgehen bestätigt. Preis und
Transport sind noch nicht beziffert. **Es wurde noch kein physischer Sitz oder
Festigkeit nachgewiesen.** Diese Dateien sind druckbare Entwürfe mit vorgeschalteter
Passprobe, keine Garantie für fertige Mechanik. Änderungen nur mit neuer Revision.
`manifest.json` enthält Mengen, Maße und SHA-256-Hashes; Zeichnungen und
Schraubenliste liegen unter `03_DRAWINGS`. Der Pico 2 hat denselben dokumentierten
51×21-mm-Platzbedarf; reale Stecker/Lötstellen trotzdem prüfen.
