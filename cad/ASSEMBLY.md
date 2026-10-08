# S6 assembly prototype — fit gate remains open

Editable CAD is `build_frame.py`; dimensions in millimetres are derived from `../physical_spec.json`. `stl/` contains seven PETG frame components and two separate TPU soles. `quotation_plate.stl` is a cost-estimation grouping, not a recommended print-bed arrangement. Individual parts fit within approximately 90 mm; a service chooses orientation/supports. `exploded.png` shows body/part names and axes.

**Do not order these as manufacturing-ready parts.** CAD passes a finite intersection audit, but the selected servo's ear, shaft, spline, horn pattern and screws are unmeasured. The intended finished kit requires clear through-holes, removed supports and bonded soles; no drilling, cutting, tapping or heat-set inserts by the assembler. The supplier must provide any necessary finishing and matching fasteners within the delivered quote.

Materials: PETG frames, 0.2 mm layers, 3 perimeters, nominal 25% infill; TPU 95A soles 90×45×1 mm bonded to feet. The mass specification uses solid PETG at 1270 kg/m³ as a conservative estimate; actual infill/adhesive mass must be weighed. Layers should be oriented to resist ear loads rather than split across narrow bridges. Ask for stiff local joint mounting walls, smooth holes and no support debris near rotating horns. Service capability and cost for TPU/bonding are not verified.

## Fastener schedule — provisional, quote as a complete kit

| Purpose | Quantity | Proposed type / unresolved fit |
|---|---:|---|
| Servo housing mounting ears | 12 | M2×8 through screws + 12 M2 nuts + 24 washers; verify real ear holes and combined thickness |
| Horn shaft retention | 6 | Servo-specific factory screws; thread and supplied inclusion unknown |
| Horn to moving frame | 12 | Two per horn, matched small screws/washers; factory horn pilot holes and screw lengths unknown |
| Pico/PCA/IMU mounting | 8 ties | Through prepared frame holes; immobilize IMU and keep board faces clear of plastic/metal |
| Main cable strain relief | 4 ties | At torso near COM; externally support connector weight |
| Servo harness restraints | 8 ties | Leave a service loop at every joint; no wires crossing horn sweep |

The CAD horn interface has a 6 mm central access opening and two 2.4 mm-wide radial slots. It is a fit concept, not evidence that the included horns/screws match. If a factory horn cannot fasten without modifying it, **revise/quote the interface before printing**, or have the supplier deliver matched adapters; include their price/mass. Do not press in an incompatible spline or use glue as a structural joint.

## Assembly sequence after the budget/fit gate passes

1. Identify L/R frame parts and six individually calibrated servos. Servo housing and lead-out dimensions must match the kit. Inspect prints and holes; return poor prints for finishing rather than drilling them.
2. Test electronics and one servo without a limb attached. Disable outputs and disconnect motor power before installing a horn. Centre the unloaded servo to its calibrated **zero-joint** pulse, then turn power off. Mount horn and retain it with its matching centre screw; do not use the HOME angle as the mechanical zero reference.
3. Mount two hip servo cases to the torso ear cradles, shafts facing outward ±y. Attach each thigh moving plate to that hip's horn with two matched screws. There is no passive hip roll axis.
4. Mount each knee servo case to its thigh's lower cradle. Attach the shin's upper plate to the knee horn. Both simulated pitch axes are +y; the physical right-hand motor sign may be opposite and is corrected in calibration.
5. Mount ankle servo case to its foot's upright cradle with shaft facing +x. Attach the shin's perpendicular lower plate to the ankle horn. Foot and ankle servo case rotate together; the shin carries the horn. The ankle axis is +x, roll only.
6. Bonded TPU soles should already be on the feet. Install boards at the coordinates in the specification using prepared holes/ties; do not put a tie over connector pins or strain the board. IMU must be rigidly immobilized and its measured axis rotation recorded.
7. Route servo leads and prepared extension harness; verify polarity/continuity with motor supply disconnected. Leave a slack service loop and inspect every safe angle manually without forcing the gearbox. Add USB/power strain relief.
8. Assemble and weigh one leg, then the entire robot. Confirm pitch/roll signs with very small unloaded motions. Test physical cutoff, watchdog and reboot-disarmed state before supported HOME `(-10°, +10°, 0°)` per leg.
9. On a low clear floor area with thin protection, test stationary poses and increase test length gradually. For a fall, disconnect power, inspect gears/ears, manually pick up and reset. Optional safety thread stays slack and is not required to hold the robot upright.

The finite CAD report does not certify horn fasteners, servo-ear insertion, electronics mounting or every continuous-motion clearance. Simulation contact primitives approximate the structure and do not test printed layer strength. The complete robot has not been assembled.
