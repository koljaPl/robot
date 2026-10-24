# S6-PETG-pad-r2 — assembly and fit checklist

**Quotation prototype, not manufacturing-approved.** All dimensions are in the
physical ledger; none of this is a physical test. [Exploded view](exploded.png),
[interface drawing](print_order/drawings/interfaces.png), [fasteners](print_order/fasteners.csv).
Commercial printing is active; no printer/spool or printed TPU sole purchase.

## Parts and exact installed quantities

Seven printed PETG parts: torso, L/Rthigh, L/Rshin, L/Rfoot, one each. Two separate
interface samples are test pieces, not extra frame parts. Eight ordinary Delock18309
TPE pads, four per foot. [Quote brief](QUOTE_REQUEST.md).

| Use | Installed quantity | Known / unresolved |
|---|---:|---|
| Servo ear screws |12|M2×8 P010265;8mm under-head,4mm head diameter,1.6mm head height; actual grip length unverified|
| Ear nuts |12|P003474 M2,SW4,1.6mm height|
| Ear washers |24|P004198,2.2×5×0.3mm; one each side|
| Factory horns |6|Actual Waveshare batch/spline/shape/hole pattern unknown|
| Shaft retainers |6|Factory-matching thread and length unknown; do not assume M2|
| Horn-to-frame screws and washers |12+12|Two per horn; diameter/thread/length/washer size unknown|
| Board / tether / harness ties |6/4/8|From full100pack; exact safe routing needs review|

M2 ear hardware has dimensioned clearance shapes at **estimated** positions.
The old fastener mass boxes were not actual bolts; their550historical intersections
were not verified physical collisions. Unknown horn hardware still blocks release.

## 1 — Fit sample before the full frame

1. Identify one exact servo, original horn and retaining screw. With no horn attached,
   bench-calibrate the zero pulse using [CALIBRATION](../docs/CALIBRATION.md).
2. Measure case, ear hole spacing/diameter/thickness, axial ear/shaft locations,
   supplied horn holes/radii, shaft screw and lead exit. Record units and photos.
3. After budget approval obtain the **two-piece sample**. Check insertion without
   bending/cracking, both ear holes, nut/head/washer access and case clearance.
4. Test a centred original horn on the horn plate. Opening6mm and2.4×7mm radial
   slots are provisional. Confirm two screws can retain it without drilling the
   horn/print, splitting plastic or bottoming a screw in the servo.
5. Measure every printed hole/slot and inspect layers. A failed sample means revise
   CAD and re-quote; do not force/drill it or print the full frame unchanged.

## 2 — Bench and mechanical zero

Solder/insulate the bare Pico, IMU header and replaceable harness as described in
[HARDWARE](../docs/HARDWARE.md). Test PSU polarity, DC disconnect, one unloaded
servo,3.3V PWM, IMU, disarmed startup and100ms watchdog first. USB powers logic;
servo power bypasses Pico/breadboard. No physical gate is passed yet.

Set each servo to its measured **zero-joint** pulse, then disconnect DC before
fitting its compatible horn and shaft screw. HOME(-10,+10,0deg per leg) is not
mechanical zero. Software STOP is not physical isolation.

## 3 — Assemble the verified frame

1. Mount left/right hip **cases to torso**. Output shafts face the corresponding
   lateral sides. Attach each thigh's upper horn plate to its hip horn.
2. Mount each knee **case to its thigh's lower cradle**. Attach the shin's upper
   plate to that knee horn. Hip and knee axes are pitch(+Y in the model).
3. Mount each ankle **case to its foot cradle**, shaft toward the corresponding
   perpendicular shin plate. Attach the shin's lower plate to the ankle horn.
   Ankle axis is roll(+X). The shin owns the ankle horn; the foot owns its case.
4. Fit only the confirmed screw schedule. The example3mm frame+1.4mm assumed ear+
   two0.3mm washers+1.6mm nut needs6.6mm under-head; M2×8 leaves1.4mm projection
   **only if that assumed ear stack is correct**. Check sweeps and wrench access.

## 4 — Electronics, pads and cables

- Bare Pico PCB is51×21mm; two20pin headers are separately represented with an11mm
  pin envelope. Printed stand-offs support the PCB centre, away from GPIO rows.
  IMU sits on the opposite side. Check actual connector, tie and solder clearance;
  immobilize IMU and record its sensor-to-body alignment.
- Attach four pads under each90×45mm foot: x=-31,+43mm and y=±14.5mm relative
  to the ankle frame (see drawing). Pads are10mm diameter×3mm. Clean/dry the
  surface as the pad maker permits; test adhesion and slip before dynamic use.
- Route six removable servo connections with service loops; keep wires out of
  horn/fastener sweeps. Support the tether/DC socket externally and restrain the
  cable near torso COM. Never use a tight overhead line to hold the robot up.

## 5 — Weigh, inspect and calibrate

Weigh every assembled rigid body and installed hardware once. The current model
uses solid-CAD PETG inertia and estimated electronics/hardware/pad masses, not
slicer25%infill or measured masses. Match measured COM/masses and version the twin.

With motor power off inspect full safe sweeps, lead exits, connectors, access to
retainers and all through-holes. Then test small unloaded motions, physical cutoff,
watchdog, disarmed reboot and manual standing. At a fall disconnect DC, inspect
gears/ears, pick up manually and deliberately reinitialize. Physical policies need
measured validated calibration and matching fingerprints; the smoke policy is not
approved for hardware. Full-frame release and walking remain blocked.
