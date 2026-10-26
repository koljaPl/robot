# Provisional layer/support review — S6-PETG-pad-r2

These are geometrical recommendations, not a slicer run or strength certification.
No local slicer is installed. The service must confirm orientation, supports and
finished hole quality before manufacture; sample must pass on real hardware.
Initial request: PETG0.20mm,3walls,25%infill; no smaller nozzle/perimeter assumption.

| Part | Current body-to-print rotation | Review / service action |
|---|---|---|
| Torso |0,90,0deg|Bosses/servo plates project from both faces; support under the raised back/plates is expected. Avoid weak layer separation at cradles; review bed contact/support removal.|
| Two thighs |90,0,0deg|Broad pitch plates lie parallel to layers; offset lower cradle/bridge needs support review. Keep holes/slots free and mounting ligaments intact.|
| Two shins |0,90,0deg|Pitch and roll plates are perpendicular; one interface necessarily has less favorable layer/support direction. Inspect the ankle corner rib and support scars closely.|
| Two feet |0,0,0deg|Sole plate flat on bed; upright servo cradle needs layer/ear-load review. Pad bonding face must be clean/flat; do not print grip pads.|
| Ear/horn sample |90,0,0deg|Test hole and horn fit; it does not by itself certify the complete leg's strength. Compare sample and frame profiles/diameters.|

The original source body coordinates remain in cad/stl; order files are rotated
and translated onto print beds. Manifests store exact4x4transforms and source hashes.
The combined7component STL is an alternative quote input only; its disconnected
objects are not sprued, and no structural cutting by the student is required.
