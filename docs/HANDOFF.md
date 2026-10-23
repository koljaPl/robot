# From Simulation to Reality: How does a robot learn?

Generated from source by `python tools/build_handoff.py`. Do not edit HANDOFF.md.
Research date2026-10-23. Source files, ledgers and evidence states take precedence.
Short purchase/build plan for humans and AI: [SUMMARY.md](../SUMMARY.md).

## 1. Short design recommendation

Retain six Waveshare15024 MG90S servos: hip pitch, knee pitch and ankle roll per
leg, broad feet, lightweight printed frame, Pico H native PWM, MPU6050, PC USB
inference and separate5V servo power. This is a **provisional** design, not a
purchasable or calibrated walking robot. Nothing purchased/physically tested.
The target remains30s standing followed by0.3m visibly alternating walking
within30s. Software checks and training rewards cannot substitute for that result.

## 2. Comparison of6DOF vs8DOF

| Layout | Cost/weight/current | Control/stability | Sim-to-Real and repair |
|---|---|---|---|
| OriginalA: hip-roll/hip-pitch/knee per leg | Six motors | Fixed ankle orientation constrains placement and balance | Simple, but constrained foot control |
| B: A plus ankle pitch | Eight motors; at least€7 extra motor cost, more frame/current | Better sagittal control, still lacks ankle roll | More calibration, failure points and unknown current |
| Selected: hip-pitch/knee/ankle-roll | Six motors; no arms/yaw | Direct lateral weight transfer, short steps and coupled sagittal sole angle | Few replaceable parts; walking feasibility still unproved |

Mechanical precedent: [Lynxmotion BRAT](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/ses-v1/ses-v1-bipeds/brat/).
Its existence does not establish scaled servo strength or RL transfer.

## 3. Selected robot architecture

Joint order: Lhip,Lknee,Lankle,Rhip,Rknee,Rankle. Coordinates xforward,yleft,zup;
SI software units. Hip/knee axes+Y; ankles+X. Positive pitch sends a downward link
toward−X. Electrical servo signs are measured individually, including right leg.
Torso owns hip cases, each thigh its knee case, each foot its ankle case; shins
carry moving horns. Every component's mass is assigned once in physical_spec.json.

PCpolicy50Hz → bounded USB → Pico PWM50Hz → six position servos.
IMU200Hz → raw telemetry → calibrated sensor/body transform → shared gravity
estimator → five18value frames (90float32). No shaft encoders exist. Applied
targets are commands, not measured angles. Gravity estimate3, gyro/10rad/s3,
normalized applied targets6 and previous actions6 are deployable observations.
No true orientation, joint angle, translation, velocity or contact is provided.
MuJoCo500Hz simulates200Hz IMU on4/6ms intervals; estimator uses actual dt.

## 4. Servo comparison

### Servo research, 2026-10-23

Prices are public VAT-inclusive product prices, not delivered basket totals.
No physical samples tested. Exact product identity matters: no generic TowerPro
specification is assigned to the Waveshare branded/resold unit.

| Product/source | Price and current listing | Product-specific data | Decision |
|---|---|---|---|
|[Waveshare15024 MG90S](https://www.welectron.com/Waveshare-15024-MG90S-Servo_1), [manufacturer](https://www.waveshare.com/mg90s-servo.htm)|€3.50; short supply, six units unconfirmed|22.8×12.2×28.5mm;12.2g;4.8–6V; metal gears; claimed stall2.0/2.8kgf·cm and unloaded.11/.09s60° at4.8/6V;5µs deadband; position PWM|Retain first candidate; no guarantee of repeated usable torque or fit|
|[Waveshare15286 SG90](https://www.welectron.com/Waveshare-15286-SG90-Servo_1)|€1.90; around three months delivery|Same claimed case size;10.5g;plastic;4.8–6V;2.0/2.2kgf·cm;.09/.08s60°;7µs deadband|Cheaper but weaker gears; not substituted to force budget|
|[Rotorama MG90D](https://www.rotorama.de/product/mg90d)|€4.09; **on the way08.11.2026**, live page overrides cached “in stock”|22.8×12.4×28.5mm;12g;4.8–6V;metal/digital;1.8/2.2kgf·cm;90°1000–2000µs; horn set listed|No evidence justifies price increase; both speed entries labelled4.8V, unresolved inconsistency|
|[FEETECH FS90, Pololu](https://www.pololu.com/product/2818/specs), [EU candidate](https://eckstein-shop.de/feetech-fs90-1-5kg-analog-servo)|EU live price/stock **unknown** (403 on refresh); historical€3.55 not current evidence|23.2×12.5×22mm;9g;4.8–6V;plastic/analog;1.3/1.5kgf·cm;.12/.10s60°; documented3.3V signals|Weaker/different geometry. FS90R is continuous rotation and unsuitable|

The selected product package text only says “servo”; horn, horn hole pattern,
spline and retaining screw thread are **unknown**. Generic MG90S pictures or
other sellers' horn sets do not establish compatibility. Ask the selected seller
for a dimensioned drawing and exact contents before final CAD approval.

For all four: gearbox backlash, sustained torque, wear/fall lifetime and loaded
repeatability are unknown. Selected MG90S/SG90/MG90D current is unknown. Pololu's
FS90 bench currents at6V (~0.2A no-load/~0.6A stall) vary by sample and are **not**
MG90S current data. PWM target is the only command; none supplies shaft feedback
in this proposed wiring. Servo repeatability must be measured at representative
load and supply voltage. Position acknowledgements are not encoder data.

At250g and20mm moment arm, static demand is0.0491Nm; a rough2× dynamic margin
is0.0981Nm. Advertised MG90S stall0.196Nm at4.8V is not a continuous rating.
Twin force cap0.08Nm is only a provisional intermittent hypothesis. See
`tools/torque_estimates.py`: fixed-support gravity calculations are not proof
that the servo can safely sustain a pose. Do not hold prolonged stalls.

Architecture comparison: original6DOF hip-roll/hip-pitch/knee uses fewer
actuators than8DOF adding ankle-pitch, but fixed ankle orientation limits foot
control. Selected6DOF hip-pitch/knee-pitch/ankle-roll permits lateral weight
transfer with fewer motors/measurements/current than8DOF, at the expense of
coupled sagittal foot angle, short steps, no yaw and limited terrain ability.
Eight motors add at least€7 in servo prices plus frame/current cost. Neither
architecture is established to walk in this budget. Slow alternating steps,
not humanoid appearance, remain the acceptance criterion.

## 5. Complete required BOM

Authoritative `procurement.json`, checked2026-10-23. Null prices are required,
unresolved costs, never zero. Quantities include full packs where sold as packs.

| Category | Exact item / supplier source | Qty | Unit € | Line € | Selection / unresolved issue |
|---|---|---:|---:|---:|---|
| Motors | [Waveshare 15024 MG90S](https://www.welectron.com/Waveshare-15024-MG90S-Servo_1) — Welectron | 6 | 3.50 | 21.00 | VAT included, stock shown; horn/screw inclusion unverified |
| Electronics | [Raspberry Pi Pico H](https://www.berrybase.de/raspberry-pi-pico-rp2040-mikrocontroller-board-mit-headern) — BerryBase | 1 | 5.50 | 5.50 | Pre-soldered headers; USB Micro B |
| Sensors | [Funduino F23107397 MPU6050 module](https://funduino.com/products/mpu-6050-modul-triaxial-beschleunigungssensor-gyroskop) — Funduino | 1 | 3.62 | 3.62 | Header soldering/board orientation to confirm |
| Power | [Mean Well GST40A05-P1J 5 V 5 A desktop PSU](https://www.berrybase.de/meanwell-schaltnetzteil-5v-dc-5-0a-mit-hohlstecker-5-5x2-1mm) — BerryBase | 1 | 15.50 | 15.50 | C14 inlet; centre-positive 5.5 x 2.1 mm; no mains lead in package |
| Power | [Goobay 68604 Schuko to C13, 1.5 m](https://www.berrybase.de/kaltgeraete-netzkabel-schutzkontakt-stecker-abgewinkelt-iec320-c13-buchse-schwarz) — BerryBase | 1 | 3.81 | 3.81 | Exact 1.5 m variant; 10 A AC rating |
| Wiring/connectors | [Official Raspberry Pi RPI-MUSB-1 USB data cable 1 m](https://www.berrybase.de/offizielles-raspberry-pi-micro-usb-kabel-rot-1-0m) — BerryBase | 1 | 1.80 | 1.80 | USB-A PC assumed; USB-C-only PC requires extra adapter, currently not priced |
| Wiring/connectors | [DUPK-40-FF-20, 40 female-female Dupont leads, 20 cm](https://www.berrybase.de/40pin-jumper-dupont-kabel-female-female-trennbar/laenge-0-20-m) — BerryBase | 1 | 1.80 | 1.80 | Logic/IMU only, AWG28; never main servo power; replacement/source required; NOT cleared |
| Wiring/connectors | [Funduino F23108007 JR-Futaba extension, 10 cm](https://funduino.com/products/jr-futaba-servo-verlangerung-kabel-10cm-female-male) — Funduino | 6 | 1.14 | 6.84 | Helper prepares power-injection harness; branch current rating/gauge unverified; now native Pico signals; helper separates high-current power from GPIO |
| Wiring/connectors | [Donau E-175-10 red copper wire 0.75 mm², 10 m roll](https://www.berrybase.de/donau-kupferschaltlitze-0-75-mm2-10m-lang-1-adrig-24x0-20mm-pvc-isoliert) — BerryBase | 1 | 5.90 | 5.90 | Short <=10 cm power buses; label negative with black shrink; no long thin power tether |
| Power | [AiSHi ELK1M16VAWH 1000 µF 16 V capacitor](https://www.berrybase.de/elektrolytkondensator-1000-f-16v-1050c-1-radial-tht) — BerryBase | 1 | 0.29 | 0.29 | Polarity matters; actual tolerance ±20%, inconsistent page title ignored |
| Wiring/connectors | [PINH-1X40P 40-pin 2.54 mm header](https://www.berrybase.de/stiftleiste-1x-40-polig-rm-2-54-gerade) — BerryBase | 1 | 0.60 | 0.60 | Helper cuts/solders signal and sensor headers as needed; Pico headers already fitted |
| Wiring/connectors | [McPower T1535561 heat-shrink, 100 pieces](https://www.berrybase.de/schrumpfschlauch-set-100-teilig-schwarz) — BerryBase | 1 | 1.90 | 1.90 | Insulate helper-soldered harness; mark polarity; helper supplies solder as workshop consumable |
| Fasteners | [McPower T1535501 cable ties, 100 x 2.5 mm, pack of 100](https://www.berrybase.de/kabelbinder-uv-bestaendig-nylon-100-stueck/farbe-transparent/masse-100x2-5mm) — BerryBase | 1 | 0.45 | 0.45 | 8 board mounts, 4 cable strain relief, 8 harness restraints; keep away from pinch points |
| Mechanical | [7 ready-finished PETG frames + 2 bonded TPU soles, VAT and German shipping](https://meltlab.de/preise) — Print service, quote pending | 1 | **pending** | **pending** | Exact STL upload quote unavailable; no printer/browser surface available. Not a price allowance |
| Mechanical | [6 matching horns + 6 servo shaft retaining screws](https://www.welectron.com/Waveshare-15024-MG90S-Servo_1) — Selected servo supplier; package confirmation pending | 1 | **pending** | **pending** | Required. Do not assume included; exact spline/horn pattern/shaft screw thread unknown |
| Fasteners | 12 M2 x 8 mm ear screws, 12 M2 nuts, 24 M2 washers; 12 horn-to-frame screws/washers matched to supplied horns — Print-service assembly kit quote pending | 1 | **pending** | **pending** | Dimensions/lengths provisional; supplier must include a matching kit and factory-clear holes. No drilling/tapping by assembler |
| Power | [5 A rated DC female 5.5 x 2.1 mm input pigtail/coupler and accessible disconnect, strain relief](https://www.delock.de/produkt/83290/pdf.html?sprache=de) — Not selected: current-rated connector still unresolved | 1 | **pending** | **pending** | Candidate Delock 83290: manufacturer 18 AWG,5 A,24 V,5.5x2.1mm,50cm. Helper retains female pigtail. Exact delivered retailer price unresolved; alternate.de lists EUR4.29 + shipping from EUR7.99, non-stock; not a complete checkout quote. |
| Shipping | [Welectron German DPD shipping](https://www.welectron.com/Shipping-cost) — Welectron | 1 | 4.95 | 4.95 | Basket under €49 free-shipping threshold |
| Shipping | [BerryBase German DHL shipping](https://www.berrybase.de/versand-und-zahlungsbedingungen) — BerryBase | 1 | 4.95 | 4.95 | DHL EUR4.95 below EUR200; free-shipping threshold changed from recorded EUR150 |
| Shipping | [Funduino German shipping](https://funduino.com/policies/shipping-policy) — Funduino | 1 | **pending** | **pending** | Shop moved to funduino.com; shipping policy returned no usable rate; old EUR4.90 not revalidated |

Optional: spare matching servo, thin protective surface, slack safety thread,
longer adequate power/USB tethers. These are not silently needed to make the
short initial indoor trial work; several-metre travel needs a newly budgeted tether.

## 6. Total cost and procurement gate

```json
{
  "status": "INCOMPLETE",
  "known_delivered_subtotal_eur": "78.91",
  "remaining_for_all_unknowns_eur": "21.09",
  "confirmed_minimum_shortfall_eur": "0.00",
  "total_price_eur": null,
  "pending_prices": [
    "7 ready-finished PETG frames + 2 bonded TPU soles, VAT and German shipping",
    "6 matching horns + 6 servo shaft retaining screws",
    "12 M2 x 8 mm ear screws, 12 M2 nuts, 24 M2 washers; 12 horn-to-frame screws/washers matched to supplied horns",
    "5 A rated DC female 5.5 x 2.1 mm input pigtail/coupler and accessible disconnect, strain relief",
    "Funduino German shipping"
  ],
  "unresolved_checks": [
    "Delivered print/fastener/sole quote",
    "Actual servo ear/shaft/horn dimensions and horn inclusion",
    "5 A rated input connector, short bus and extension branch suitability",
    "Servo signal threshold works at 3.3 V",
    "Helper labour confirmed free or its quoted charge included",
    "USB-A computer port available",
    "Actual delivered checkout totals and stock",
    "Native Pico 3.3 V signal compatibility and timed PWM capture",
    "Unavailable FF jumpers need sourced available replacement",
    "Funduino shipping after shop migration",
    "Delock 83290 delivered price and correct 18 AWG variant (retailer description conflicts)"
  ],
  "purchase_cleared": false
}
```

### Procurement evidence and precise outstanding actions

Updated2026-10-23. Authoritative prices and unknowns: `procurement.json`.
`python tools/budget_gate.py` computes the known sum; unknown costs remain null.
Current selected revision removes PCA9685 and its OE resistor; six MG90S retained.
Direct Pico PWM supplies16 channels according to official RP2040 documentation;
six share three slices, with no shortage of channels. It does not verify the
servo's3.3V input or make the harness free. GPIO protection/loading/timing need
one-servo bench measurements before approval.

Research changes: PSU now€15.50; MPU module now€3.62; JR extension public sale
€1.14; red0.75mm² wire€5.90. BerryBase DHL remains€4.95 but free threshold is now
€200. Welectron shipping€4.95 below€49 DPD threshold. Funduino moved to
funduino.com; shipping could not be refreshed from usable policy content, so the
old€4.90 is **not** silently retained. Pico/USB/header/cap/shrink/ties listings
were reviewed. FF jumper live variants unavailable, despite cached stock claims;
an available replacement and any changed price/shipping still need evidence.

No file-specific delivered print quotation was obtained. Meltlab's public
[pricing explanation](https://meltlab.de/preise) requires uploading exact files
and slicing. Its examples are not a quote. There was no enabled browser surface
for this session, and no supplier message/purchase was authorized or sent.
`cad/quote_bundle.zip` is a quotation/fit-review bundle only. Do not order it as
released manufacturing files: horn interfaces and fastener sweeps remain unknown.

#### Questions ready for a human to send or resolve

1. **Welectron, Waveshare15024:** Are six units available together at€3.50inclVAT?
   Does each include a matching horn set and shaft-retaining screw? Please provide
   spline count/diameter, screw thread/length, horn thickness and hole pattern,
   ear hole spacing/diameter, ear plane relative to shaft, shaft-center offset,
   housing drawing and lead exit. Is3.3V PWM guaranteed? Any current/continuous
   torque data for this exact batch? Do not substitute a different MG90S brand.
2. **Print service:** Review the seven individual PETG STLs and two TPU soles in
   the bundle, NOT quotation_plate as an extra part. Quote0.2mm layers/three walls/
   25%infill, supports removed, all holes factory-clear for assembly without
   drilling/tapping, two bonded TPU95A soles including adhesive, matched fastener
   kit, VAT and delivery to Germany. Quote a sample horn/cradle interface first,
   with separate shipping if applicable. Identify all fit modifications and quote
   any CAD/finishing labour. Manufacturing release waits for measured interfaces.
3. **Harness supplier/helper:** Confirm ratings for JR branch contacts/wires and
   the full5A DC input. Candidate Delock83290 manufacturer's data says18AWG;
   retailer metadata conflict must be resolved. Quote delivered input pigtail,
   strain relief and any preparation fee. Confirm the helper's labour/consumables
   are free or add its price. No guessed free horns/screws/connector substitutions.
4. **Checkout:** Resolve FF logic leads with exact available SKU; confirm sensor/
   extension combined shipping and all retailer totals including VAT. Confirm PC
   has USB-A; otherwise include an actually priced data adapter. If bench and full
   orders are split, charge every additional delivery, including sample prints.

**Gate:** known-priced subtotal€78.91 is not a delivered price. All unresolved
items must fit the remaining€21.09. There is no confirmed monetary shortfall yet;
there is missing evidence. If a complete delivered quote exceeds€100, report
`total−100` and stop procurement. €50–75 is already below the known-priced subset;
it is not demonstrated feasible. No weaker motor substitution is authorized.

## 7. Mechanical design

`cad/build_frame.py` is editable CSG; individual STLs, quotation bundle,
print_manifest and exploded drawing are supplied. Seven PETG frames and two TPU
soles; no personal printer or drilling/tapping/heat-set inserts required. Unknown
horn/ear/screw interfaces block finished manufacture. Broad90×45mm feet and
short50mm links target roughly18cm height. Solid-CAD masses are estimated.

### S6 assembly prototype — fit gate remains open

Editable CAD is `build_frame.py`; dimensions in millimetres are derived from `../physical_spec.json`. `stl/` contains seven PETG frame components and two separate TPU soles. `quotation_plate.stl` is a cost-estimation grouping, not a recommended print-bed arrangement. Individual parts fit within approximately 90 mm; a service chooses orientation/supports. `exploded.png` shows body/part names and axes.

**Do not order these as manufacturing-ready parts.** The expanded audit detects unresolved fastener-envelope conflicts, and the selected servo's ear, shaft, spline, horn pattern and screws are unmeasured. The intended finished kit requires clear through-holes, removed supports and bonded soles; no drilling, cutting, tapping or heat-set inserts by the assembler. The supplier must provide any necessary finishing and matching fasteners within the delivered quote.

Materials: PETG frames, 0.2 mm layers, 3 perimeters, nominal 25% infill; TPU 95A soles 90×45×1 mm bonded to feet. The mass specification uses solid PETG at 1270 kg/m³ as a conservative estimate; actual infill/adhesive mass must be weighed. Layers should be oriented to resist ear loads rather than split across narrow bridges. Ask for stiff local joint mounting walls, smooth holes and no support debris near rotating horns. Service capability and cost for TPU/bonding are not verified.

#### Fastener schedule — provisional, quote as a complete kit

| Purpose | Quantity | Proposed type / unresolved fit |
|---|---:|---|
| Servo housing mounting ears | 12 | M2×8 through screws + 12 M2 nuts + 24 washers; verify real ear holes and combined thickness |
| Horn shaft retention | 6 | Servo-specific factory screws; thread and supplied inclusion unknown |
| Horn to moving frame | 12 | Two per horn, matched small screws/washers; factory horn pilot holes and screw lengths unknown |
| Pico/IMU mounting | 6 ties | Through prepared frame holes; immobilize IMU and keep board faces clear of plastic/metal |
| Main cable strain relief | 4 ties | At torso near COM; externally support connector weight |
| Servo harness restraints | 8 ties | Leave a service loop at every joint; no wires crossing horn sweep |

The CAD horn interface has a 6 mm central access opening and two 2.4 mm-wide radial slots. It is a fit concept, not evidence that the included horns/screws match. If a factory horn cannot fasten without modifying it, **revise/quote the interface before printing**, or have the supplier deliver matched adapters; include their price/mass. Do not press in an incompatible spline or use glue as a structural joint.

#### Assembly sequence after the budget/fit gate passes

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

Current revision: Pico native PWM removes the old PCA9685 envelope conflict.
The finite checker includes frame/case/electronics and estimated fastener sweeps;
550 overlaps involve unmeasured mass-envelope proxies across55poses. These are
not confirmed bolt collisions, but cannot be cleared without actual horn/screw
geometry. Run `python tools/check_clearance.py`; nonzero exit means no release.
The exploded view shows frame, servo-case and PCB envelopes; actual horn/fastener
fit remains specified provisionally in the ledger/schedule and is not certified.

Body origins/axes, command intervals and mass/COM below derive from the ledger.
Unknown mechanical stops remain null and are absent from provisional MJCF.

| Body | Parent | Joint / axis | Origin in parent (mm) | Safe commands, NOT mechanical stops (°) | Mass (g) | COM local (mm) |
|---|---|---|---|---|---:|---|
| torso | world | root / floating | 0.000, 0.000, 154.240 | free | 72.89 | -6.653, 0.000, -9.861 |
| left_thigh | torso | left_hip / 0.000, 1.000, 0.000 | 0.000, 34.000, -30.000 | [-35, 35] | 18.97 | 0.000, -9.434, -42.970 |
| left_shin | left_thigh | left_knee / 0.000, 1.000, 0.000 | 0.000, 0.000, -50.000 | [-10, 60] | 7.72 | 1.432, 1.714, -22.688 |
| left_foot | left_shin | left_ankle / 1.000, 0.000, 0.000 | 0.000, 0.000, -50.000 | [-20, 20] | 36.58 | -1.919, 0.000, -15.367 |
| right_thigh | torso | right_hip / 0.000, 1.000, 0.000 | 0.000, -34.000, -30.000 | [-35, 35] | 18.97 | 0.000, 9.434, -42.970 |
| right_shin | right_thigh | right_knee / 0.000, 1.000, 0.000 | 0.000, 0.000, -50.000 | [-10, 60] | 7.72 | 1.432, -1.714, -22.688 |
| right_foot | right_shin | right_ankle / 1.000, 0.000, 0.000 | 0.000, 0.000, -50.000 | [-20, 20] | 36.58 | -1.919, -0.000, -15.367 |

| Body | Component (mass assigned once) | Dimensions xyz (mm) | Mass (g) | COM local xyz (mm) |
|---|---|---|---:|---|
| torso | torso_frame | 32.000, 82.000, 88.750 | 21.49 | -16.308, -0.000, -5.438 |
| torso | pico_h | 6.000, 51.000, 21.000 | 4.00 | -14.500, 0.000, 23.000 |
| torso | imu | 4.000, 16.000, 20.000 | 3.00 | -25.500, 0.000, 18.000 |
| torso | torso_wires_fasteners | 30.000, 70.000, 40.000 | 20.00 | 0.000, 0.000, 5.000 |
| torso | left_hip_servo | 12.200, 28.500, 22.800 | 12.20 | 0.000, 19.750, -34.750 |
| torso | right_hip_servo | 12.200, 28.500, 22.800 | 12.20 | 0.000, -19.750, -34.750 |
| left_thigh | left_thigh_frame | 24.000, 13.500, 87.750 | 5.27 | 0.000, -0.974, -24.526 |
| left_thigh | left_knee_servo | 12.200, 28.500, 22.800 | 12.20 | 0.000, -14.250, -54.750 |
| left_thigh | left_thigh_joint_fasteners | 20.000, 12.000, 12.000 | 1.50 | 0.000, 0.000, -12.000 |
| left_shin | left_shin_frame | 24.000, 24.000, 78.000 | 6.22 | 1.777, 2.128, -25.264 |
| left_shin | left_shin_joint_fasteners | 20.000, 12.000, 12.000 | 1.50 | 0.000, 0.000, -12.000 |
| left_foot | left_foot_frame | 90.000, 45.000, 38.250 | 18.02 | 4.134, 0.000, -20.373 |
| left_foot | left_sole | 90.000, 45.000, 1.000 | 4.86 | 6.000, 0.000, -24.500 |
| left_foot | left_ankle_servo | 28.500, 12.200, 22.800 | 12.20 | -14.250, 0.000, -4.750 |
| left_foot | left_foot_joint_fasteners | 20.000, 12.000, 12.000 | 1.50 | 0.000, 0.000, -12.000 |
| right_thigh | right_thigh_frame | 24.000, 13.500, 87.750 | 5.27 | 0.000, 0.974, -24.526 |
| right_thigh | right_knee_servo | 12.200, 28.500, 22.800 | 12.20 | 0.000, 14.250, -54.750 |
| right_thigh | right_thigh_joint_fasteners | 20.000, 12.000, 12.000 | 1.50 | 0.000, 0.000, -12.000 |
| right_shin | right_shin_frame | 24.000, 24.000, 78.000 | 6.22 | 1.777, -2.128, -25.264 |
| right_shin | right_shin_joint_fasteners | 20.000, 12.000, 12.000 | 1.50 | 0.000, 0.000, -12.000 |
| right_foot | right_foot_frame | 90.000, 45.000, 38.250 | 18.02 | 4.134, -0.000, -20.373 |
| right_foot | right_sole | 90.000, 45.000, 1.000 | 4.86 | 6.000, 0.000, -24.500 |
| right_foot | right_ankle_servo | 28.500, 12.200, 22.800 | 12.20 | -14.250, 0.000, -4.750 |
| right_foot | right_foot_joint_fasteners | 20.000, 12.000, 12.000 | 1.50 | 0.000, 0.000, -12.000 |

| Body | Ixx, Iyy, Izz, Ixy, Ixz, Iyz (kg·m²) |
|---|---|
| torso | 7.714665e-05, 5.092307e-05, 4.315149e-05, 2.541099e-21, 7.752416e-06, 0 |
| left_thigh | 1.075608e-05, 9.509007e-06, 2.306097e-06, -1.321365e-23, 9.846622e-24, -2.552041e-06 |
| left_shin | 3.771568e-06, 3.870593e-06, 4.366762e-07, 1.069363e-08, 2.608766e-07, -1.717284e-07 |
| left_foot | 7.376615e-06, 2.141873e-05, 2.153521e-05, -9.25926e-23, 2.911645e-06, 1.500083e-22 |
| right_thigh | 1.075608e-05, 9.509007e-06, 2.306097e-06, 1.321365e-23, 9.846622e-24, 2.552041e-06 |
| right_shin | 3.771568e-06, 3.870593e-06, 4.366762e-07, -1.069363e-08, 2.608766e-07, 1.717284e-07 |
| right_foot | 7.376615e-06, 2.141873e-05, 2.153521e-05, 9.25926e-23, 2.911645e-06, -1.500083e-22 |

Authoritative structured physical input (provisional):

```json
{
  "name": "School Biped S6",
  "status": "PROVISIONAL: budget, printed fit and hardware calibration not approved",
  "units": "m, kg, rad, s",
  "coordinates": "x forward, y left, z up; local body axes match parent at zero joint angle",
  "home_joint_angles_deg": [
    -10,
    10,
    0,
    -10,
    10,
    0
  ],
  "servo": {
    "model": "Waveshare 15024 MG90S",
    "mass": 0.0122,
    "housing_dimensions": [
      0.0228,
      0.0122,
      0.0285
    ],
    "shaft_offset_along_case_length": 0.00475,
    "shaft_to_case_center_axial": 0.01425,
    "mounting_hole_spacing": 0.028,
    "mounting_hole_diameter": 0.0022,
    "status": "housing size and mass are seller claims; shaft/ear/horn dimensions are estimates requiring measurement",
    "parameter_evidence": {
      "model": {
        "state": "sourced",
        "date": "2026-10-23",
        "evidence": "https://www.waveshare.com/mg90s-servo.htm"
      },
      "mass": {
        "state": "sourced",
        "date": "2026-10-23",
        "evidence": "https://www.waveshare.com/mg90s-servo.htm"
      },
      "housing_dimensions": {
        "state": "sourced",
        "date": "2026-10-23",
        "evidence": "https://www.waveshare.com/mg90s-servo.htm"
      },
      "shaft_offset_along_case_length": {
        "state": "estimated",
        "date": "2026-10-23",
        "evidence": "requires measured servo sample before manufacturing"
      },
      "shaft_to_case_center_axial": {
        "state": "estimated",
        "date": "2026-10-23",
        "evidence": "requires measured servo sample before manufacturing"
      },
      "mounting_hole_spacing": {
        "state": "estimated",
        "date": "2026-10-23",
        "evidence": "requires measured servo sample before manufacturing"
      },
      "mounting_hole_diameter": {
        "state": "estimated",
        "date": "2026-10-23",
        "evidence": "requires measured servo sample before manufacturing"
      }
    }
  },
  "geometry": {
    "hip_half_spacing": 0.034,
    "hip_z": -0.03,
    "thigh_length": 0.05,
    "shin_length": 0.05,
    "foot_dimensions": [
      0.09,
      0.045,
      0.003
    ],
    "foot_center": [
      0.006,
      0,
      -0.0225
    ],
    "sole_thickness": 0.001,
    "ankle_to_floor": 0.025,
    "torso_dimensions": [
      0.04,
      0.082,
      0.066
    ],
    "cad_wall": 0.003,
    "cad_clearance": 0.0004,
    "petg_density": 1270
  },
  "bodies": [
    {
      "name": "torso",
      "parent": "world",
      "position": [
        0,
        0,
        0.154240388
      ],
      "joint": "root",
      "axis": null,
      "components": [
        {
          "name": "torso_frame",
          "mass": 0.021486247742229223,
          "dimensions": [
            0.032,
            0.082,
            0.08875
          ],
          "com": [
            -0.016308210070435095,
            -5.215214943911107e-19,
            -0.0054384916759348196
          ],
          "inertia_tensor": [
            [
              2.6309016723560255e-05,
              2.703988807846125e-21,
              2.1653112995251776e-06
            ],
            [
              2.703988807846125e-21,
              1.3253368557151762e-05,
              3.4107973696966715e-22
            ],
            [
              2.1653112995251776e-06,
              3.4107973696966715e-22,
              1.578588698727872e-05
            ]
          ],
          "material": "solid PETG estimate, 1270 kg/m\u00b3",
          "evidence": "generated CAD; actual infill/printed density must be weighed",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            }
          }
        },
        {
          "name": "pico_h",
          "mass": 0.004,
          "dimensions": [
            0.006,
            0.051,
            0.021
          ],
          "com": [
            -0.0145,
            0,
            0.023
          ],
          "material": "PCB and headers",
          "evidence": "estimate",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate"
            }
          }
        },
        {
          "name": "imu",
          "mass": 0.003,
          "dimensions": [
            0.004,
            0.016,
            0.02
          ],
          "com": [
            -0.0255,
            0,
            0.018
          ],
          "material": "PCB",
          "evidence": "estimate",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate"
            }
          }
        },
        {
          "name": "torso_wires_fasteners",
          "mass": 0.02,
          "dimensions": [
            0.03,
            0.07,
            0.04
          ],
          "com": [
            0,
            0,
            0.005
          ],
          "material": "copper, plastic, steel",
          "evidence": "estimate includes six added 10 cm extensions, short heavy power wire, capacitor, pullup, board mounting ties and torso hardware; excludes suspended tether",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate includes six added 10 cm extensions, short heavy power wire, capacitor, pullup, board mounting ties and torso hardware; excludes suspended tether"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate includes six added 10 cm extensions, short heavy power wire, capacitor, pullup, board mounting ties and torso hardware; excludes suspended tether"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate includes six added 10 cm extensions, short heavy power wire, capacitor, pullup, board mounting ties and torso hardware; excludes suspended tether"
            }
          }
        },
        {
          "name": "left_hip_servo",
          "mass": 0.0122,
          "dimensions": [
            0.0122,
            0.0285,
            0.0228
          ],
          "com": [
            0,
            0.01975,
            -0.03475
          ],
          "material": "servo composite",
          "evidence": "seller mass, estimated uniform inertia",
          "parameter_evidence": {
            "mass": {
              "state": "sourced",
              "date": "2026-10-23",
              "evidence": "Waveshare15024 listing"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "seller mass, estimated uniform inertia"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "seller mass, estimated uniform inertia"
            }
          }
        },
        {
          "name": "right_hip_servo",
          "mass": 0.0122,
          "dimensions": [
            0.0122,
            0.0285,
            0.0228
          ],
          "com": [
            0,
            -0.01975,
            -0.03475
          ],
          "material": "servo composite",
          "evidence": "seller mass, estimated uniform inertia",
          "parameter_evidence": {
            "mass": {
              "state": "sourced",
              "date": "2026-10-23",
              "evidence": "Waveshare15024 listing"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "seller mass, estimated uniform inertia"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "seller mass, estimated uniform inertia"
            }
          }
        }
      ],
      "safe_command_deg": null,
      "mechanical_limits_deg": null,
      "parameter_evidence": {
        "state": "estimated",
        "date": "2026-10-23",
        "evidence": "prototype CAD design; mechanical stops unknown; safe command range is not mechanical travel"
      }
    },
    {
      "name": "left_thigh",
      "parent": "torso",
      "position": [
        0,
        0.034,
        -0.03
      ],
      "joint": "left_hip",
      "axis": [
        0,
        1,
        0
      ],
      "components": [
        {
          "name": "left_thigh_frame",
          "mass": 0.005273029560391083,
          "dimensions": [
            0.024,
            0.013500000000000002,
            0.08775
          ],
          "com": [
            2.6563334945902374e-19,
            -0.0009738150793376264,
            -0.02452563897898925
          ],
          "inertia_tensor": [
            [
              3.6463630740464687e-06,
              -1.3640154818355183e-24,
              3.5681746524361245e-23
            ],
            [
              -1.3640154818355183e-24,
              3.83564073707392e-06,
              -5.988303056018393e-07
            ],
            [
              3.5681746524361245e-23,
              -5.988303056018393e-07,
              4.6710755114091395e-07
            ]
          ],
          "material": "solid PETG estimate, 1270 kg/m\u00b3",
          "evidence": "generated CAD; actual infill/printed density must be weighed",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            }
          }
        },
        {
          "name": "left_knee_servo",
          "mass": 0.0122,
          "dimensions": [
            0.0122,
            0.0285,
            0.0228
          ],
          "com": [
            0,
            -0.01425,
            -0.05475
          ],
          "material": "servo composite",
          "evidence": "seller mass, estimated inertia",
          "parameter_evidence": {
            "mass": {
              "state": "sourced",
              "date": "2026-10-23",
              "evidence": "Waveshare15024 listing"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "seller mass, estimated inertia"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "seller mass, estimated inertia"
            }
          }
        },
        {
          "name": "left_thigh_joint_fasteners",
          "mass": 0.0015,
          "dimensions": [
            0.02,
            0.012,
            0.012
          ],
          "com": [
            0,
            0,
            -0.012
          ],
          "material": "steel and plastic horns",
          "evidence": "estimate; weigh installed fasteners/horn",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; weigh installed fasteners/horn"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; weigh installed fasteners/horn"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; weigh installed fasteners/horn"
            }
          }
        }
      ],
      "safe_command_deg": [
        -35,
        35
      ],
      "mechanical_limits_deg": null,
      "parameter_evidence": {
        "state": "estimated",
        "date": "2026-10-23",
        "evidence": "prototype CAD design; mechanical stops unknown; safe command range is not mechanical travel"
      }
    },
    {
      "name": "left_shin",
      "parent": "left_thigh",
      "position": [
        0,
        0,
        -0.05
      ],
      "joint": "left_knee",
      "axis": [
        0,
        1,
        0
      ],
      "components": [
        {
          "name": "left_shin_frame",
          "mass": 0.006223103503190493,
          "dimensions": [
            0.024,
            0.024,
            0.078
          ],
          "com": [
            0.001777148714462294,
            0.002127532309995988,
            -0.025264417900762635
          ],
          "inertia_tensor": [
            [
              3.517439052233832e-06,
              1.526352745623322e-08,
              2.3238492246555624e-07
            ],
            [
              1.526352745623322e-08,
              3.5861170810492066e-06,
              -2.0583750953748297e-07
            ],
            [
              2.3238492246555624e-07,
              -2.0583750953748297e-07,
              3.5938805714611084e-07
            ]
          ],
          "material": "solid PETG estimate, 1270 kg/m\u00b3",
          "evidence": "generated CAD; actual infill/printed density must be weighed",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            }
          }
        },
        {
          "name": "left_shin_joint_fasteners",
          "mass": 0.0015,
          "dimensions": [
            0.02,
            0.012,
            0.012
          ],
          "com": [
            0,
            0,
            -0.012
          ],
          "material": "steel and plastic horns",
          "evidence": "estimate; weigh installed fasteners/horn",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; weigh installed fasteners/horn"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; weigh installed fasteners/horn"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; weigh installed fasteners/horn"
            }
          }
        }
      ],
      "safe_command_deg": [
        -10,
        60
      ],
      "mechanical_limits_deg": null,
      "parameter_evidence": {
        "state": "estimated",
        "date": "2026-10-23",
        "evidence": "prototype CAD design; mechanical stops unknown; safe command range is not mechanical travel"
      }
    },
    {
      "name": "left_foot",
      "parent": "left_shin",
      "position": [
        0,
        0,
        -0.05
      ],
      "joint": "left_ankle",
      "axis": [
        1,
        0,
        0
      ],
      "components": [
        {
          "name": "left_foot_frame",
          "mass": 0.018016309759572663,
          "dimensions": [
            0.09,
            0.045,
            0.03825
          ],
          "com": [
            0.004134161361397353,
            1.943645122968221e-20,
            -0.02037258709585519
          ],
          "inertia_tensor": [
            [
              3.5912674486333607e-06,
              -9.047277336272573e-23,
              4.2675158262628113e-07
            ],
            [
              -9.047277336272573e-23,
              1.1641060651440434e-05,
              1.4825539214630055e-22
            ],
            [
              4.2675158262628113e-07,
              1.4825539214630055e-22,
              1.356399711276919e-05
            ]
          ],
          "material": "solid PETG estimate, 1270 kg/m\u00b3",
          "evidence": "generated CAD; actual infill/printed density must be weighed",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            }
          }
        },
        {
          "name": "left_sole",
          "mass": 0.00486,
          "dimensions": [
            0.09,
            0.045,
            0.001
          ],
          "com": [
            0.006,
            0,
            -0.0245
          ],
          "material": "solid TPU 95A, density estimate 1200 kg/m\u00b3",
          "evidence": "estimate; includes adhesive uncertainty, weigh actual sole",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; includes adhesive uncertainty, weigh actual sole"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; includes adhesive uncertainty, weigh actual sole"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; includes adhesive uncertainty, weigh actual sole"
            }
          }
        },
        {
          "name": "left_ankle_servo",
          "mass": 0.0122,
          "dimensions": [
            0.0285,
            0.0122,
            0.0228
          ],
          "com": [
            -0.01425,
            0,
            -0.00475
          ],
          "material": "servo composite",
          "evidence": "seller mass, estimated inertia",
          "parameter_evidence": {
            "mass": {
              "state": "sourced",
              "date": "2026-10-23",
              "evidence": "Waveshare15024 listing"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "seller mass, estimated inertia"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "seller mass, estimated inertia"
            }
          }
        },
        {
          "name": "left_foot_joint_fasteners",
          "mass": 0.0015,
          "dimensions": [
            0.02,
            0.012,
            0.012
          ],
          "com": [
            0,
            0,
            -0.012
          ],
          "material": "steel and plastic horns",
          "evidence": "estimate; weigh installed fasteners/horn",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; weigh installed fasteners/horn"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; weigh installed fasteners/horn"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-23",
              "evidence": "estimate; weigh installed fasteners/horn"
            }
          }
        }
      ],
      "safe_command_deg": [
        -20,
        20
      ],
      "mechanical_limits_deg": null,
      "parameter_evidence": {
        "state": "estimated",
        "date": "2026-10-23",
        "evidence": "prototype CAD design; mechanical stops unknown; safe command range is not mechanical travel"
      }
    },
    {
      "name": "right_thigh",
      "mirror_of": "left_thigh",
      "parent": "torso",
      "position": [
        0,
        -0.034,
        -0.03
      ],
      "joint": "right_hip",
      "axis": [
        0,
        1,
        0
      ],
      "safe_command_deg": [
        -35,
        35
      ],
      "mechanical_limits_deg": null,
      "parameter_evidence": {
        "state": "estimated",
        "date": "2026-10-23",
        "evidence": "prototype CAD design; mechanical stops unknown; safe command range is not mechanical travel"
      }
    },
    {
      "name": "right_shin",
      "mirror_of": "left_shin",
      "parent": "right_thigh",
      "position": [
        0,
        0,
        -0.05
      ],
      "joint": "right_knee",
      "axis": [
        0,
        1,
        0
      ],
      "safe_command_deg": [
        -10,
        60
      ],
      "mechanical_limits_deg": null,
      "parameter_evidence": {
        "state": "estimated",
        "date": "2026-10-23",
        "evidence": "prototype CAD design; mechanical stops unknown; safe command range is not mechanical travel"
      }
    },
    {
      "name": "right_foot",
      "mirror_of": "left_foot",
      "parent": "right_shin",
      "position": [
        0,
        0,
        -0.05
      ],
      "joint": "right_ankle",
      "axis": [
        1,
        0,
        0
      ],
      "safe_command_deg": [
        -20,
        20
      ],
      "mechanical_limits_deg": null,
      "parameter_evidence": {
        "state": "estimated",
        "date": "2026-10-23",
        "evidence": "prototype CAD design; mechanical stops unknown; safe command range is not mechanical travel"
      }
    }
  ],
  "revision": "s6-native-pwm-provisional-2",
  "updated_date": "2026-10-23",
  "controller": {
    "backend": "pico_pwm",
    "pins": [
      0,
      1,
      2,
      3,
      6,
      7
    ],
    "pwm_hz": 50,
    "pulse_resolution_us": 1,
    "i2c_pins": [
      4,
      5
    ],
    "state": "planned; electrical verification pending"
  },
  "parameter_evidence": {
    "geometry": {
      "state": "estimated",
      "date": "2026-10-23",
      "evidence": "design intent; not manufactured"
    },
    "actuator": {
      "state": "estimated",
      "date": "2026-10-23",
      "evidence": "robot_config.py; requires loaded step response"
    },
    "mechanical_stops": {
      "state": "unknown",
      "date": "2026-10-23",
      "evidence": "No hardware exists; omitted from MJCF"
    }
  },
  "dynamics": {
    "kp": {
      "value": 0.9,
      "state": "estimated",
      "date": "2026-10-23",
      "evidence": "provisional simulation hypothesis; must fit real measurements"
    },
    "kv": {
      "value": 0.012,
      "state": "estimated",
      "date": "2026-10-23",
      "evidence": "provisional simulation hypothesis; must fit real measurements"
    },
    "intermittent_torque_nm": {
      "value": 0.08,
      "state": "estimated",
      "date": "2026-10-23",
      "evidence": "provisional simulation hypothesis; must fit real measurements"
    },
    "target_speed_deg_s": {
      "value": 180,
      "state": "estimated",
      "date": "2026-10-23",
      "evidence": "provisional simulation hypothesis; must fit real measurements"
    },
    "no_load_speed_deg_s": {
      "value": 545.4545454545455,
      "state": "sourced",
      "date": "2026-10-23",
      "evidence": "Waveshare15024 unloaded speed at4.8V; 5V loaded speed unmeasured"
    },
    "deadband_deg": {
      "value": 0.5,
      "state": "estimated",
      "date": "2026-10-23",
      "evidence": "provisional simulation hypothesis; must fit real measurements"
    },
    "damping_nm_s_rad": {
      "value": 0.002,
      "state": "estimated",
      "date": "2026-10-23",
      "evidence": "provisional simulation hypothesis; must fit real measurements"
    },
    "frictionloss_nm": {
      "value": 0.001,
      "state": "estimated",
      "date": "2026-10-23",
      "evidence": "provisional simulation hypothesis; must fit real measurements"
    },
    "armature_kg_m2": {
      "value": 5e-06,
      "state": "estimated",
      "date": "2026-10-23",
      "evidence": "provisional simulation hypothesis; must fit real measurements"
    },
    "sliding_friction": {
      "value": 0.8,
      "state": "estimated",
      "date": "2026-10-23",
      "evidence": "provisional simulation hypothesis; must fit real measurements"
    },
    "contact_model": {
      "value": "condim3 sliding only; torsional/rolling coefficients inactive",
      "state": "sourced",
      "date": "2026-10-23",
      "evidence": "https://mujoco.readthedocs.io/en/stable/computation/index.html#contact"
    }
  }
}
```

## 8. Wiring/power architecture and bench protocol

### Native-PWM S6 hardware and protocol

Updated 2026-10-23. Implemented source and local compilation are distinct from
physical verification: **nothing has been purchased or electrically tested**.
The selected *provisional* revision is Pico H native PWM, six Waveshare15024
MG90S, MPU6050 and Mean Well GST40A05-P1J. PCA9685 is not in the current basket.
Its listing is unavailable and removing it resolves the original board/brace overlap.

#### Power and helper preparation

PC USB powers Pico and IMU. Enclosed 5V/5A PSU, including separately priced
Schuko–C13 mains lead, powers ONLY the servo bus. Never connect servo5V to Pico
VBUS/VSYS/3V3, or route servo current through GPIO jumpers or a breadboard.
Join logic ground to the short heavy servo-return bus once. Mains wiring remains
inside the commercial PSU/lead. Capacitor1000µF/16V goes across the bus with
correct polarity; it is not a substitute for an adequate supply.

A helper prepares six replaceable 10cm JR extension branches: retain each
servo-side socket, solder red/return to positive/negative 0.75mm² buses, and
connect the signal via a fitted header/jumper to the chosen Pico pin. Insulate
all joints and cut ends. No servo current runs in the logic jumper. Fit header
pins to the IMU if loose; tie boards with insulating separation, secure cables,
and verify polarity/continuity using a multimeter. The assembler receives a
finished harness, with no cutting/drilling/soldering. Helper labour must be
confirmed free or quoted in procurement. Solder is helper workshop consumable.
Tools: borrowed temperature-controlled iron/solder, wire stripper, cutters,
heat source and multimeter. These are excluded tools, not hidden robot parts.

Estimated average six-servo current0.6–1.5A, assumed peak4.8A (6×0.8A), plus
logic below0.15A on USB. **Selected-servo current is unknown**; these are sizing
hypotheses. A5A PSU offers little peak margin; measure droop/current before six
servos. At4.8A, 20cm total0.75mm² copper loop drops~0.022V, excluding connectors,
PSU lead and branches. A2m one-way tether of this wire drops~0.45V and is not
acceptable. Use the PSU's existing lead and slack loop for the initial0.3m trial;
several metres need a newly sourced thicker tether/longer USB cable and budget.
1000µF stores only~0.04ms at4.8A for0.2V droop. Measure4.8–6V at the farthest
loaded servo and check connector temperature.

Accessible full-current DC unplug is the physical emergency cutoff. Candidate
[Delock83290](https://www.delock.com/produkt/83290/merkmale.html?setLanguage=de)
is specified18AWG/5A/24V; a helper could retain its female pigtail and join the
short bus. Exact delivered price and conflicting retailer gauge description
remain unresolved. Unrated Goobay76743 is not accepted as5A. JR branch gauge,
contacts and actual servo currents also need confirmation. Do not clear the
basket merely because a connector fits. STOP/PWM silence **does not physically
disconnect motor power**; an analogue servo may hold its last position. Always
disarm before reconnecting DC. Support tether weight near the body COM.

#### Pin table

| Joint / function | GPIO | Pico physical pin |
|---|---:|---:|
| Left hip |0|1|
| Left knee |1|2|
| Left ankle |2|4|
| Right hip |3|5|
| Right knee |6|9|
| Right ankle |7|10|
| MPU SDA / SCL |4 / 5|6 / 7|
| IMU VCC |3V3 OUT|36|
| IMU GND + short common servo ground |GND|38|

Native PWM uses a1MHz counter and wrap19999:50Hz and1µs resolution. Paired
channels share slices with the same frequency. GPIOs produce3.3V logic;
**MG90S input compatibility is unverified**. Test one unloaded servo before
approving this revision; a level shifter would add cost and wiring. No onboard
PWM feedback or torque protection exists.

MPU6050 at0x68, AD0 grounded: WHO_AM_I checked, ±2g, ±250°/s, DLPF_CFG3
(~44Hz accel/~42Hz gyro), divider4 for200Hz. Wire pull-ups must go to3.3V.
Firmware sends raw scaled sensor-frame readings. PC removes measured biases,
rotates into body coordinates and uses `GravityEstimator`. The simulated
44Hz first-order filter is a provisional surrogate, not exact silicon transfer.
References: [Pico](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html),
[pinout](https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf),
[IMU register map](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf).

#### Executable version1 protocol

`hardware_interface.py`, `serial_robot.py`, `firmware/control.h` and
`firmware/main.cpp` implement the following contract, superseding the earlier
pseudocode-only draft. No physical firmware already exists to migrate.
USB CDC baud460800 (descriptor), ASCII, max192bytes including newline,
`payload*HHHH\n`, CRC16/CCITT initFFFF. Config/calibration SHA256s are lowercase
64hex. All numeric fields decimal integers; seq uint16, timestamps uint32 ms.
Angles mrad, acceleration mm/s², angular rates mrad/s.

| Payload | Behavior |
|---|---|
| `S,1` | Disarm, disable PWM, clear fault/queue and require new handshake |
| `H,1,config_hash,cal_hash,pc_ms` | Disarmed identity/time-origin handshake; mismatch faults |
| `I,1,config_hash,cal_hash,status` | Acknowledgement; no implicit arm |
| `A,1` | Explicit policy arm, only matching identity + valid measured calibration + healthy IMU |
| `C,1,seq,pc_ms,q0,q1,q2,q3,q4,q5` | Six bounded fresh target commands while armed |
| `B,1,seq,pc_ms,channel,pulse_us` | Explicit one-channel bench mode;1400–1600µs only; no policy arming |
| `T,1,ack_seq,mcu_ms,status,q0,q1,q2,q3,q4,q5,ax,ay,az,gx,gy,gz` |200Hz telemetry with applied command coordinates |

Bits:1 armed,2 latched fault (including watchdog/invalid data),4 unhealthyIMU,
8 invalid/unmeasured calibration,16 no matching handshake,32 bench mode.
Only fresh valid C/B renews100ms watchdog. CRC/length/type/range/replay faults
silence all outputs and latch fault. S then H is needed before deliberate restart.
Sequence deltas must be1..32767; PCtimestamp deltas positive and<=1000ms.
H establishes relative clock origin; inferred command age must be−20..80ms.
Host refuses policy arming for handshake round-trip>=20ms (provisional bound).
Unsigned wrap-safe comparisons are used; neither absolute clock is synchronized.

Firmware queues commands for a minimum20ms before50Hz target application,
limits target slew to calibrated maximum<=180°/s, uses an estimated0.5° command
deadband, rounds inward to1µs safe pulse bounds and acknowledges the sequence
when dequeued. Multiple commands within the same tick can be coalesced by
latest due target. This is commanded motion, not measured shaft motion; PWM
speed limits do not guarantee actual shaft speed or physical torque protection.
The queue is fixed8entries. No dynamic input allocation is used.

Calibration is versioned JSON persisted **in firmware flash at build time**.
Changing it requires rebuilding/flashing; it cannot be edited over an armed
serial link. `tools/firmware_config.py` generates the matching header. Examples
remain invalid and cannot policy-arm. Model/control/firmware source hashes
combine into one config hash; the calibration has its own hash. Policies carry
both plus their file hash. `deploy.py` rejects incompatible policies/calibration.
No historical prototype checkpoint is approved for the new model.

#### Bench and deployment

See [firmware build](../firmware/README.md) and [calibration](CALIBRATION.md).
Read-only IMU logging is the bench default. Nothing in these instructions means
an actual motor should be powered before procurement/fit/power gates pass.

```bash
python bench.py --port /dev/ttyACM0 --seconds 10 --output runs/stationary.csv
### Explicit single-channel pulse calibration, unloaded servo, horn detached initially:
python bench.py --port /dev/ttyACM0 --channel 0 --pulse-us 1500 --seconds 2 --output runs/channel0.csv
### Only after all physical checks and training with this measured calibration:
python deploy.py --port /dev/ttyACM0 --model runs/measured/best_model.zip \
  --calibration calibrations/measured-v1.json --arm --seconds 5 --output runs/trial01.csv
```

Ctrl-C/fault closes with STOP. Physical operator keeps the DC disconnect
reachable. Never reset a fallen robot automatically: power off, inspect, lift,
replace damaged parts and reinitialize. Real distances/steps require video/ruler,
not double integration of MPU acceleration.

### Pico SDK firmware

Source is C++17 using official Pico SDK **2.3.1**, revision
`079c6f39023649b154152db30f1d781e884879bc`, TinyUSB submodule
`86ad6e56c1700e85f1c5678607a762cfe3aa2f47`.
Locally compiled with Arm GNU14.2.Rel1, CMake3.31.10 and Ninja1.13.2.
No electrical/timing/flash test on a Pico is claimed.

Install an `arm-none-eabi` cross compiler and clone the SDK outside the project:

```bash
git clone --depth 1 --branch 2.3.1 https://github.com/raspberrypi/pico-sdk.git /tmp/pico-sdk
git -C /tmp/pico-sdk submodule update --init --depth 1 lib/tinyusb
source .venv/bin/activate
python tools/firmware_config.py # invalid example, cannot policy-arm
export PICO_SDK_PATH=/tmp/pico-sdk
### Set PICO_TOOLCHAIN_PATH to the directory containing arm-none-eabi-gcc if not in PATH.
cmake -S firmware -B build/firmware -G Ninja -DPICO_BOARD=pico -DPICO_NO_PICOTOOL=1
cmake --build build/firmware -j 4
### Official picotool2.3.1 converts the ELF into a flashable UF2:
picotool uf2 convert build/firmware/s6_bench.elf build/firmware/s6_bench.uf2 --family rp2040
```

`PICO_NO_PICOTOOL=1` avoids CMake implicitly downloading extra code; install
[picotool](https://github.com/raspberrypi/picotool) separately or use the official
[SDK tools2.3.1-0 release](https://github.com/raspberrypi/pico-sdk-tools/releases/tag/v2.3.1-0).
If picotool is configured normally, omit that flag and SDK can produce UF2 itself.

For a measured calibration, run:

```bash
python tools/firmware_config.py --calibration calibrations/measured-v1.json
cmake --build build/firmware -j 4
picotool uf2 convert build/firmware/s6_bench.elf build/firmware/s6_bench.uf2 --family rp2040
```

Calibration/signs/limits/identity are compiled into firmware flash and survive
power loss; every boot is disarmed. Do not hand-edit generated_config.h. Physical
flashing: disconnect servo power, hold BOOTSEL while connecting Pico USB, then
copy the UF2 onto RPI-RP2. Release/reset and check read-only telemetry first.
Never flash or reconnect motor power while a policy process is running.

The generated header must be regenerated after any fingerprinted control/model
source edit. A stale image is rejected by the PC handshake. The repository
example's `CAL_VALID=false` is intentional, not a build error. Single-channel
bench mode is explicitly allowed without validated joint calibration and is
restricted to1400–1600µs; it still needs a clear, unloaded setup and cutoff.

## 9. MuJoCo parameter table

| Parameter | Starting value / evidence |
|---|---|
| Physics |2ms, implicitfast, gravity−9.81m/s² |
| Position servo |kp0.9,kv0.012; estimates, not identified motor gains |
| Torque |±0.08Nm intermittent estimate, drive torque decreases with actual shaft speed |
| Command trajectory |180°/s nominal, delayed20ms; DR discrete20/40ms |
| Speed envelope |60°/.11s seller no-load4.8V claim; not loaded capability |
| Deadband |0.5° hysteresis surrogate; not true gear backlash |
| PWM |native1µs; estimated500µs/rad unless measured per-channel calibration supplied |
| Damping/frictionloss/armature |0.002Nm·s/rad,0.001Nm,5e−6kg·m²; estimates |
| Contact |condim3,sliding μ0.8estimate; stored torsional/rolling coefficients inactive |
| IMU |±2g/±250°/s quantization,44Hz first-order surrogate,shared gravity estimator |
| Mass/COM/inertia |component ledger+parallel-axis theorem; estimates, not weighed |

`physical_spec.json` stores dynamics provenance/state/date and each component's
mass/COM/dimensions/inertia evidence. Mechanical joint travel is unknown.
Position actuators are force-limited; commanded slew is not a hard shaft-speed
constraint, and software angle bounds are not physical motor torque protection.

## 10. Full robot.xml

```xml
<!-- Generated from physical_spec.json; provisional hardware model. -->
<mujoco model="SchoolBipedS6_provisional">
  <compiler angle="radian" autolimits="true" inertiafromgeom="false" />
  <option timestep="0.002" gravity="0 0 -9.81" integrator="implicitfast" iterations="60" />
  <visual>
    <global offwidth="960" offheight="720" />
    <map znear="0.002" />
  </visual>
  <default>
    <joint limited="false" damping="0.002" armature="5e-06" frictionloss="0.001" />
    <geom condim="3" friction="0.8 0.005 0.0001" solref="0.008 1" solimp="0.9 0.95 0.001" />
    <position kp="0.9" kv="0.012" forcelimited="true" forcerange="-0.08 0.08" ctrllimited="true" />
  </default>
  <asset>
    <mesh name="torso_mesh" file="cad/stl/torso.stl" scale="0.001 0.001 0.001" />
    <mesh name="left_thigh_mesh" file="cad/stl/left_thigh.stl" scale="0.001 0.001 0.001" />
    <mesh name="left_shin_mesh" file="cad/stl/left_shin.stl" scale="0.001 0.001 0.001" />
    <mesh name="left_foot_mesh" file="cad/stl/left_foot.stl" scale="0.001 0.001 0.001" />
    <mesh name="right_thigh_mesh" file="cad/stl/right_thigh.stl" scale="0.001 0.001 0.001" />
    <mesh name="right_shin_mesh" file="cad/stl/right_shin.stl" scale="0.001 0.001 0.001" />
    <mesh name="right_foot_mesh" file="cad/stl/right_foot.stl" scale="0.001 0.001 0.001" />
  </asset>
  <worldbody>
    <light pos="0 -1 2" dir="0 0 -1" diffuse="0.8 0.8 0.8" />
    <geom name="floor" type="plane" size="3 3 0.05" rgba="0.87 0.88 0.90 1" />
    <body name="torso" pos="0 0 0.154240388">
      <geom name="torso_visual" type="mesh" mesh="torso_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
      <inertial mass="0.07288624774" pos="-0.006652863288 0 -0.00986129485" fullinertia="7.714665284e-05 5.092307439e-05 4.315149003e-05 2.541098842e-21 7.752415604e-06 0" />
      <freejoint name="root" />
      <geom name="torso_collision" type="box" pos="0 0 0.01" size="0.02 0.041 0.025" rgba="0.10 0.45 0.8 0.8" />
      <site name="imu_site" pos="-0.0255 0 0.018" size="0.003" rgba="1 0.7 0 1" />
      <camera name="overview" pos="0.42 -0.5 0.24" xyaxes="0.766 0.643 0 -0.26 0.31 0.916" />
      <geom name="left_hip_servo_case" type="box" pos="0 0.01975 -0.03475" size="0.0061 0.01425 0.0114" rgba="0.15 0.15 0.17 1" />
      <geom name="right_hip_servo_case" type="box" pos="0 -0.01975 -0.03475" size="0.0061 0.01425 0.0114" rgba="0.15 0.15 0.17 1" />
      <body name="left_thigh" pos="0 0.034 -0.03">
        <geom name="left_thigh_visual" type="mesh" mesh="left_thigh_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
        <inertial mass="0.01897302956" pos="7.38254531e-20 -0.009433651865 -0.04297017599" fullinertia="1.075607705e-05 9.509006643e-06 2.306096954e-06 -1.321364545e-23 9.846621791e-24 -2.552040829e-06" />
        <joint name="left_hip" type="hinge" axis="0 1 0" />
        <geom name="left_thigh_link" type="capsule" fromto="0 0 -0.006 0 0 -0.044" size="0.006" rgba="0.12 0.55 0.83 1" />
        <geom name="left_knee_servo_case" type="box" pos="0 -0.01425 -0.05475" size="0.0061 0.01425 0.0114" rgba="0.15 0.15 0.17 1" />
        <body name="left_shin" pos="0 0 -0.05">
          <geom name="left_shin_visual" type="mesh" mesh="left_shin_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
          <inertial mass="0.007723103503" pos="0.001431986556 0.001714317795 -0.0226881703" fullinertia="3.771568488e-06 3.870592897e-06 4.366762365e-07 1.069363096e-08 2.608766246e-07 -1.717283681e-07" />
          <joint name="left_knee" type="hinge" axis="0 1 0" />
          <geom name="left_shin_link" type="capsule" fromto="0 0 -0.006 0 0 -0.044" size="0.006" rgba="0.12 0.55 0.83 1" />
          <body name="left_foot" pos="0 0 -0.05">
            <geom name="left_foot_visual" type="mesh" mesh="left_foot_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
            <inertial mass="0.03657630976" pos="-0.001919484737 9.573768603e-21 -0.0153667454" fullinertia="7.376615256e-06 2.141873222e-05 2.153521221e-05 -9.259259754e-23 2.911645236e-06 1.500083034e-22" />
            <joint name="left_ankle" type="hinge" axis="1 0 0" />
            <geom name="left_foot_plate" type="box" pos="0.006 0 -0.0225" size="0.045 0.0225 0.0015" rgba="0.08 0.36 0.65 1" />
            <geom name="left_foot_sole" type="box" pos="0.006 0 -0.0245" size="0.045 0.0225 0.0005" rgba="0.15 0.15 0.15 1" />
            <site name="left_foot_sole_center" pos="0.006 0 -0.025" size="0.001" />
            <geom name="left_ankle_servo_case" type="box" pos="-0.01425 0 -0.00475" size="0.01425 0.0061 0.0114" rgba="0.15 0.15 0.17 1" />
          </body>
        </body>
      </body>
      <body name="right_thigh" pos="0 -0.034 -0.03">
        <geom name="right_thigh_visual" type="mesh" mesh="right_thigh_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
        <inertial mass="0.01897302956" pos="7.38254531e-20 0.009433651865 -0.04297017599" fullinertia="1.075607705e-05 9.509006643e-06 2.306096954e-06 1.321364545e-23 9.846621791e-24 2.552040829e-06" />
        <joint name="right_hip" type="hinge" axis="0 1 0" />
        <geom name="right_thigh_link" type="capsule" fromto="0 0 -0.006 0 0 -0.044" size="0.006" rgba="0.12 0.55 0.83 1" />
        <geom name="right_knee_servo_case" type="box" pos="0 0.01425 -0.05475" size="0.0061 0.01425 0.0114" rgba="0.15 0.15 0.17 1" />
        <body name="right_shin" pos="0 0 -0.05">
          <geom name="right_shin_visual" type="mesh" mesh="right_shin_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
          <inertial mass="0.007723103503" pos="0.001431986556 -0.001714317795 -0.0226881703" fullinertia="3.771568488e-06 3.870592897e-06 4.366762365e-07 -1.069363096e-08 2.608766246e-07 1.717283681e-07" />
          <joint name="right_knee" type="hinge" axis="0 1 0" />
          <geom name="right_shin_link" type="capsule" fromto="0 0 -0.006 0 0 -0.044" size="0.006" rgba="0.12 0.55 0.83 1" />
          <body name="right_foot" pos="0 0 -0.05">
            <geom name="right_foot_visual" type="mesh" mesh="right_foot_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
            <inertial mass="0.03657630976" pos="-0.001919484737 -9.573768603e-21 -0.0153667454" fullinertia="7.376615256e-06 2.141873222e-05 2.153521221e-05 9.259259754e-23 2.911645236e-06 -1.500083034e-22" />
            <joint name="right_ankle" type="hinge" axis="1 0 0" />
            <geom name="right_foot_plate" type="box" pos="0.006 0 -0.0225" size="0.045 0.0225 0.0015" rgba="0.08 0.36 0.65 1" />
            <geom name="right_foot_sole" type="box" pos="0.006 0 -0.0245" size="0.045 0.0225 0.0005" rgba="0.15 0.15 0.15 1" />
            <site name="right_foot_sole_center" pos="0.006 0 -0.025" size="0.001" />
            <geom name="right_ankle_servo_case" type="box" pos="-0.01425 0 -0.00475" size="0.01425 0.0061 0.0114" rgba="0.15 0.15 0.17 1" />
          </body>
        </body>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position name="left_hip_servo" joint="left_hip" ctrlrange="-0.6108652382 0.6108652382" />
    <position name="left_knee_servo" joint="left_knee" ctrlrange="-0.1745329252 1.047197551" />
    <position name="left_ankle_servo" joint="left_ankle" ctrlrange="-0.3490658504 0.3490658504" />
    <position name="right_hip_servo" joint="right_hip" ctrlrange="-0.6108652382 0.6108652382" />
    <position name="right_knee_servo" joint="right_knee" ctrlrange="-0.1745329252 1.047197551" />
    <position name="right_ankle_servo" joint="right_ankle" ctrlrange="-0.3490658504 0.3490658504" />
  </actuator>
  <sensor>
    <gyro name="imu_gyro" site="imu_site" />
    <accelerometer name="imu_accel" site="imu_site" />
  </sensor>
  <keyframe>
    <key name="home" qpos="0 0 0.154240388 1 0 0 0 -0.1745329252 0.1745329252 0 -0.1745329252 0.1745329252 0" ctrl="-0.1745329252 0.1745329252 0 -0.1745329252 0.1745329252 0" />
  </keyframe>
</mujoco>
```

## 11. Full humanoid_env.py and shared control modules

Reward: `10*min(dx,0.06*dt)`; positive progress capped, all backward motion charged.
Plus0.2*upright*dt, minus0.5*abs(lateral_velocity)*dt, minus0.0001*mean(action_rate²)*dt,
minus2 onfall. Command smoothness is a proxy, **not electrical energy**. Falling
uses body tilt/height or nonfoot-floor contact; time limit truncates separately.

Evaluation requires whole-foot3mm clearance for40ms, opposite supported stance,
>=5mm forward touchdown, <=3mm stance slip and alternating sides. Qualifying
foot advance contributes half its displacement to gait distance. Walking success
requires0.3m body travel AND0.3m gait distance, at least2steps each/3alternations,
no fall. Stationary lifts followed by sliding, toe pivots and hops gain no gait
credit. Force thresholds are SIM diagnostics, never policy input; real evidence
must come from video. Conservative diagnostics can reject marginal real steps.

```python
"""MuJoCo/Gymnasium walking environment for the provisional physical S6 design."""
from collections import deque
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import mujoco
from robot_config import (ROOT, JOINT_NAMES, HOME, PHYSICS_DT, CONTROL_DT, IMU_DT,
                          HISTORY, FRAME_SIZE, DR, BASE_DELAY, TARGET_SPEED,
                          SERVO_TORQUE, SERVO_NO_LOAD_SPEED, GYRO_NOISE,
                          ACCEL_NOISE, MAX_EPISODE_SECONDS, action_to_target, target_to_action,
                          IMU_FILTER_HZ, IMU_ACCEL_RANGE, IMU_GYRO_RANGE)
from gait_metrics import GaitMetrics, progress_reward
from servo_control import ServoTargets
from imu_observation import GravityEstimator, ObservationHistory


class HumanoidEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    def __init__(self, xml_path=None, render_mode=None, domain_randomization=False,
                 episode_seconds=MAX_EPISODE_SECONDS, calibration=None):
        super().__init__()
        if render_mode not in (None, "human", "rgb_array"):
            raise ValueError("render_mode must be None, human, or rgb_array")
        if not np.isfinite(episode_seconds) or episode_seconds <= 0:
            raise ValueError("episode_seconds must be positive")
        self.model = mujoco.MjModel.from_xml_path(str(xml_path or ROOT / "robot.xml"))
        if not np.isclose(self.model.opt.timestep, PHYSICS_DT):
            raise ValueError("MJCF timestep must match robot_config.PHYSICS_DT")
        self.data = mujoco.MjData(self.model)
        self.render_mode = render_mode
        self.calibration = calibration
        self.domain_randomization = bool(domain_randomization)
        self.max_steps = max(1, int(round(episode_seconds / CONTROL_DT)))
        self.action_space = spaces.Box(-1.0, 1.0, shape=(6,), dtype=np.float32)
        self.observation_space = spaces.Box(-1.0, 1.0, shape=(HISTORY * FRAME_SIZE,), dtype=np.float32)
        self.qadr = np.array([self.model.jnt_qposadr[self.model.joint(n).id] for n in JOINT_NAMES])
        self.vadr = np.array([self.model.jnt_dofadr[self.model.joint(n).id] for n in JOINT_NAMES])
        self.aids = np.array([self.model.actuator(n + "_servo").id for n in JOINT_NAMES])
        self.torso_id = self.model.body("torso").id
        self.floor_id = self.model.geom("floor").id
        self.feet_ids = [self.model.geom(s + "_foot_sole").id for s in ("left", "right")]
        self.foot_plate_ids = [self.model.geom(s + "_foot_plate").id for s in ("left", "right")]
        self.foot_ids = set(self.feet_ids + self.foot_plate_ids)
        self.nominal = {name: getattr(self.model, name).copy() for name in (
            "body_mass", "body_inertia", "geom_friction", "dof_damping", "actuator_forcerange")}
        self.estimator = GravityEstimator()
        self.history = ObservationHistory()
        self.viewer = None
        self.renderer = None
        self.done = True

    def _randomize(self):
        for name, value in self.nominal.items():
            getattr(self.model, name)[:] = value
        self.offset = np.zeros(6)
        self.gyro_bias = np.zeros(3)
        self.accel_bias = np.zeros(3)
        self.noise_scale = 1.0
        delay, speed, self.no_load_speed = BASE_DELAY, TARGET_SPEED, SERVO_NO_LOAD_SPEED
        if self.domain_randomization:
            rng = self.np_random
            scale = rng.uniform(1 - DR.mass, 1 + DR.mass, self.model.nbody)
            scale[0] = 1
            self.model.body_mass[:] *= scale
            self.model.body_inertia[:] *= scale[:, None]
            self.model.geom_friction[:] *= rng.uniform(1 - DR.friction, 1 + DR.friction)
            strength = rng.uniform(1 - DR.strength, 1 + DR.strength, 6)
            self.model.actuator_forcerange[self.aids] *= strength[:, None]
            self.model.dof_damping[self.vadr] *= rng.uniform(1 - DR.damping, 1 + DR.damping, 6)
            speed_scale = rng.uniform(1 - DR.speed, 1 + DR.speed)
            speed *= speed_scale
            self.no_load_speed *= speed_scale
            delay = int(rng.choice(DR.delay_ticks)) * CONTROL_DT
            self.offset = rng.uniform(-DR.offset_rad, DR.offset_rad, 6)
            self.gyro_bias = rng.uniform(-DR.gyro_bias, DR.gyro_bias, 3)
            self.accel_bias = rng.uniform(-DR.accel_bias, DR.accel_bias, 3)
            self.noise_scale = rng.uniform(*DR.sensor_noise_scale)
        self.torque_limit = self.model.actuator_forcerange[self.aids, 1].copy()
        self.servos = ServoTargets(delay=delay, speed=speed, calibration=self.calibration)
        mujoco.mj_setConst(self.model, self.data)

    def _raw_imu(self):
        gyro = self.data.sensor("imu_gyro").data.copy()
        accel = self.data.sensor("imu_accel").data.copy()
        gyro += self.gyro_bias + self.np_random.normal(0, GYRO_NOISE * self.noise_scale, 3)
        accel += self.accel_bias + self.np_random.normal(0, ACCEL_NOISE * self.noise_scale, 3)
        gyro = np.clip(gyro, -IMU_GYRO_RANGE, IMU_GYRO_RANGE)
        accel = np.clip(accel, -IMU_ACCEL_RANGE, IMU_ACCEL_RANGE)
        # First-order 44 Hz surrogate, not a claim to reproduce silicon DLPF exactly.
        alpha = 1 - np.exp(-2*np.pi*IMU_FILTER_HZ*IMU_DT)
        if self.filtered_gyro is None:
            self.filtered_gyro, self.filtered_accel = gyro.copy(), accel.copy()
        else:
            self.filtered_gyro += alpha*(gyro-self.filtered_gyro)
            self.filtered_accel += alpha*(accel-self.filtered_accel)
        gyro_lsb, accel_lsb = IMU_GYRO_RANGE/32768, IMU_ACCEL_RANGE/32768
        return (np.rint(self.filtered_gyro/gyro_lsb)*gyro_lsb,
                np.rint(self.filtered_accel/accel_lsb)*accel_lsb)

    def _motor_envelope(self):
        # Drive-direction torque falls with shaft speed; opposing/braking torque remains.
        velocity = self.data.qvel[self.vadr]
        positive = self.torque_limit * np.clip(1 - np.maximum(velocity, 0) / self.no_load_speed, 0, 1)
        negative = self.torque_limit * np.clip(1 - np.maximum(-velocity, 0) / self.no_load_speed, 0, 1)
        self.model.actuator_forcerange[self.aids, 0] = -negative
        self.model.actuator_forcerange[self.aids, 1] = positive

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self._randomize()
        mujoco.mj_resetDataKeyframe(self.model, self.data, self.model.key("home").id)
        self.data.ctrl[self.aids] = HOME + self.offset
        # Simulate quiet physical startup before initializing from accelerometer data.
        for _ in range(100):
            self._motor_envelope()
            mujoco.mj_step(self.model, self.data)
        self.data.time = 0
        mujoco.mj_forward(self.model, self.data)
        self.filtered_gyro = self.filtered_accel = None
        gyro, accel = self._raw_imu()
        self.estimator.reset(accel)
        self.last_gyro = gyro
        self.imu_last_time = 0.0
        self.imu_next_time = IMU_DT
        self.servo_next_time = 0.0
        self.last_action = target_to_action(HOME)
        self.servos.reset()
        self.applied_command = HOME.copy()
        self.steps = 0
        self.total_reward = 0.0
        self.start_position = self.data.xpos[self.torso_id].copy()
        self.nominal_height = self.model.key("home").qpos[2]
        self.gait = GaitMetrics()
        self.lifted_steps = self.gait.steps
        self.alternations = 0
        self.done = False
        frame = self.history.frame(self.estimator.gravity, self.last_gyro, self.applied_command, self.last_action)
        obs = self.history.reset(frame)
        return obs, self._info(False)

    def _contact_state(self):
        contacts = np.zeros(2, dtype=bool)
        bad_contact = False
        for c in self.data.contact:
            if c.geom1 == self.floor_id or c.geom2 == self.floor_id:
                other = c.geom2 if c.geom1 == self.floor_id else c.geom1
                if other not in self.foot_ids:
                    bad_contact = True
                for i in range(2):
                    if other in (self.feet_ids[i], self.foot_plate_ids[i]):
                        contacts[i] = True
        return contacts, bad_contact

    def _minimum_foot_height(self, foot_index):
        gid = self.feet_ids[foot_index]
        mat = self.data.geom_xmat[gid].reshape(3, 3)
        # Lowest box corner: the whole foot must clear the floor, not just a toe.
        return float(self.data.geom_xpos[gid, 2] - np.dot(np.abs(mat[2]), self.model.geom_size[gid]))

    def _record_steps(self, contacts):
        load = np.zeros(2)
        force = np.zeros(6)
        for index, contact in enumerate(self.data.contact):
            if self.floor_id not in (contact.geom1, contact.geom2):
                continue
            other = contact.geom2 if contact.geom1 == self.floor_id else contact.geom1
            for i in range(2):
                if other in (self.feet_ids[i], self.foot_plate_ids[i]):
                    mujoco.mj_contactForce(self.model, self.data, index, force)
                    load[i] += max(0, force[0])
        supported = load >= .10 * self.model.body_mass.sum()*9.81
        self.gait.update(self.data.geom_xpos[self.feet_ids],
                         [self._minimum_foot_height(i) for i in range(2)],
                         contacts, supported, PHYSICS_DT)
        self.alternations = self.gait.alternations

    def _info(self, fallen):
        duration = self.steps * CONTROL_DT
        distance = float(self.data.xpos[self.torso_id, 0] - self.start_position[0])
        return {"distance_m": distance, "lateral_distance_m": float(self.data.xpos[self.torso_id, 1] - self.start_position[1]),
                "duration_s": duration, "mean_speed_m_s": distance / duration if duration else 0.0,
                "fallen": bool(fallen), "total_reward": float(self.total_reward),
                "lifted_steps_left": int(self.lifted_steps[0]), "lifted_steps_right": int(self.lifted_steps[1]),
                "alternations": int(self.alternations),
                "gait_distance_m": float(self.gait.distance),
                "max_stance_slip_m": float(self.gait.max_stance_slip),
                "rejected_steps": int(self.gait.rejected),
                "walking_success": bool(not fallen and distance >= 0.3 and self.gait.distance >= 0.3 and min(self.lifted_steps) >= 2 and self.alternations >= 3),
                "domain_randomization": self.domain_randomization}

    def step(self, action):
        if self.done:
            raise RuntimeError("Call reset() before step() and after an episode ends")
        target = action_to_target(action)
        action = np.clip(np.asarray(action, dtype=float), -1, 1)
        previous_position = self.data.xpos[self.torso_id].copy()
        self.servos.enqueue(self.data.time, target)
        fallen = False
        for _ in range(round(CONTROL_DT / PHYSICS_DT)):
            if self.data.time + 1e-10 >= self.servo_next_time:
                self.applied_command = self.servos.advance(self.data.time, CONTROL_DT)
                self.servo_next_time += CONTROL_DT
            applied = self.applied_command
            # Offset is an unobserved physical calibration error; acknowledged commands
            # remain exactly the same command coordinates as on the real controller.
            limits = self.model.actuator_ctrlrange[self.aids]
            self.data.ctrl[self.aids] = np.clip(applied + self.offset, limits[:, 0], limits[:, 1])
            self._motor_envelope()
            mujoco.mj_step(self.model, self.data)
            if self.data.time + 1e-10 >= self.imu_next_time:
                gyro, accel = self._raw_imu()
                self.estimator.update(gyro, accel, self.data.time - self.imu_last_time)
                self.last_gyro = gyro
                self.imu_last_time = self.data.time
                self.imu_next_time += IMU_DT
            contacts, bad_contact = self._contact_state()
            self._record_steps(contacts)
            upright = self.data.xmat[self.torso_id].reshape(3, 3)[2, 2]
            fallen |= bad_contact or self.data.xpos[self.torso_id, 2] < self.nominal_height * 0.6 or upright < 0.5
        if not (np.isfinite(self.data.qpos).all() and np.isfinite(self.data.qvel).all()):
            raise FloatingPointError("Non-finite MuJoCo state; inspect model and controller")
        velocity = (self.data.xpos[self.torso_id] - previous_position) / CONTROL_DT
        upright = float(np.clip(self.data.xmat[self.torso_id].reshape(3, 3)[2, 2], 0, 1))
        terms = {"forward": progress_reward(velocity[0] * CONTROL_DT, CONTROL_DT),
                 "upright": CONTROL_DT * 0.2 * upright,
                 "lateral": -CONTROL_DT * 0.5 * abs(float(velocity[1])),
                 "smoothness": -CONTROL_DT * 0.0001 * float(np.mean(((action - self.last_action) / CONTROL_DT) ** 2)),
                 "fall": -2.0 if fallen else 0.0}
        reward = float(sum(terms.values()))
        self.steps += 1
        self.total_reward += reward
        self.last_action = action.copy()
        obs = self.history.append(self.history.frame(self.estimator.gravity, self.last_gyro, self.applied_command, self.last_action))
        terminated = bool(fallen)
        truncated = bool(self.steps >= self.max_steps and not terminated)
        self.done = terminated or truncated
        info = self._info(fallen)
        info["reward_terms"] = terms
        if self.render_mode == "human":
            self.render()
        return obs, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            if self.viewer is None:
                from mujoco import viewer
                self.viewer = viewer.launch_passive(self.model, self.data)
                self.viewer.cam.distance = 0.5
                self.viewer.cam.azimuth = 135
                self.viewer.cam.elevation = -15
            self.viewer.cam.lookat[:] = self.data.xpos[self.torso_id]
            self.viewer.sync()
        elif self.render_mode == "rgb_array":
            if self.renderer is None:
                self.renderer = mujoco.Renderer(self.model, height=480, width=640)
            cam = mujoco.MjvCamera()
            cam.distance, cam.azimuth, cam.elevation = 0.5, 135, -15
            cam.lookat[:] = self.data.xpos[self.torso_id]
            self.renderer.update_scene(self.data, camera=cam)
            return self.renderer.render()

    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None
        if self.renderer is not None:
            self.renderer.close()
            self.renderer = None
```

```python
"""Shared, conservative starting values. Units: SI; all actuator values are estimates."""
from dataclasses import dataclass
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parent
JOINT_NAMES = ("left_hip", "left_knee", "left_ankle", "right_hip", "right_knee", "right_ankle")
PHYSICAL_SPEC = json.loads((ROOT / "physical_spec.json").read_text())
_joint_bodies = {b["joint"]: b for b in PHYSICAL_SPEC["bodies"] if b["joint"] != "root"}
JOINT_LOW = np.deg2rad([_joint_bodies[n]["safe_command_deg"][0] for n in JOINT_NAMES])
JOINT_HIGH = np.deg2rad([_joint_bodies[n]["safe_command_deg"][1] for n in JOINT_NAMES])
HOME = np.deg2rad(PHYSICAL_SPEC["home_joint_angles_deg"])
PHYSICS_DT = 0.002
CONTROL_DT = 0.02
IMU_DT = 0.005
HISTORY = 5
FRAME_SIZE = 18  # gravity(3), gyro(3), applied target(6), previous action(6)
DYNAMICS = PHYSICAL_SPEC["dynamics"]
SERVO_KP = DYNAMICS["kp"]["value"]
SERVO_KV = DYNAMICS["kv"]["value"]
SERVO_TORQUE = DYNAMICS["intermittent_torque_nm"]["value"]  # Nm, estimated intermittent operating envelope, NOT continuous rating
TARGET_SPEED = np.deg2rad(DYNAMICS["target_speed_deg_s"]["value"])  # commanded trajectory limit, not actual shaft speed
SERVO_NO_LOAD_SPEED = np.deg2rad(DYNAMICS["no_load_speed_deg_s"]["value"])  # seller claim at 4.8 V; measure at 5 V
SERVO_DEADBAND = np.deg2rad(DYNAMICS["deadband_deg"]["value"])  # simple hysteresis surrogate; not mechanical backlash
BASE_DELAY = 0.02
PWM_RESOLUTION_US = 1
ESTIMATED_US_PER_RAD = 500.0  # provisional: replace using measured per-channel mapping
IMU_ACCEL_RANGE = 2 * 9.80665
IMU_GYRO_RANGE = np.deg2rad(250)
IMU_FILTER_HZ = 44.0  # surrogate for MPU6050 DLPF_CFG=3; not exact silicon response
GYRO_NOISE = 0.006  # rad/s standard deviation
ACCEL_NOISE = 0.04  # m/s^2 standard deviation
MAX_EPISODE_SECONDS = 30.0


@dataclass(frozen=True)
class Randomization:
    """Uniform multiplicative ranges, except noise/bias/offset/delay in SI units."""
    mass: float = 0.05
    friction: float = 0.15
    strength: float = 0.15
    speed: float = 0.10
    damping: float = 0.20
    offset_rad: float = np.deg2rad(1.0)
    delay_ticks: tuple[int, int] = (1, 2)
    gyro_bias: float = 0.01
    accel_bias: float = 0.05
    sensor_noise_scale: tuple[float, float] = (0.8, 1.2)


DR = Randomization()


def action_to_target(action):
    action = np.asarray(action, dtype=np.float64)
    if action.shape != (6,) or not np.isfinite(action).all():
        raise ValueError("Action must contain six finite normalized joint targets")
    return JOINT_LOW + (np.clip(action, -1, 1) + 1) * 0.5 * (JOINT_HIGH - JOINT_LOW)


def target_to_action(target):
    return np.clip(2 * (np.asarray(target) - JOINT_LOW) / (JOINT_HIGH - JOINT_LOW) - 1, -1, 1)
```

```python
"""Command delay and bounded position-target trajectory, shared with hardware tests."""
from collections import deque
import numpy as np
from robot_config import HOME, JOINT_LOW, JOINT_HIGH, TARGET_SPEED, SERVO_DEADBAND, PWM_RESOLUTION_US, ESTIMATED_US_PER_RAD


class ServoTargets:
    def __init__(self, delay=0.02, speed=TARGET_SPEED, deadband=SERVO_DEADBAND, calibration=None):
        self.calibration = calibration
        self.delay = float(delay)
        self.speed = float(speed)
        self.deadband = float(deadband)
        self.reset()

    def reset(self, home=HOME):
        self.applied = np.asarray(home, dtype=float).copy()
        self.goal = self.applied.copy()
        self.accepted = self.applied.copy()
        self.queue = deque()

    def enqueue(self, time, target):
        target = np.asarray(target, dtype=float)
        if target.shape != (6,) or not np.isfinite(target).all():
            raise ValueError("Invalid servo target")
        bounded = np.clip(target, JOINT_LOW, JOINT_HIGH)
        self.queue.append((float(time) + self.delay, bounded.copy()))

    def advance(self, time, dt):
        while self.queue and self.queue[0][0] <= time + 1e-10:
            _, incoming = self.queue.popleft()
            # Ignore sub-deadband reversals until accumulated change passes threshold.
            changed = np.abs(incoming - self.accepted) >= self.deadband
            self.accepted[changed] = incoming[changed]
            self.goal = self.accepted.copy()
        self.applied += np.clip(self.goal - self.applied, -self.speed * dt, self.speed * dt)
        self.applied = np.clip(self.applied, JOINT_LOW, JOINT_HIGH)
        return self.quantize(self.applied)

    def quantize(self, target):
        # Integer-us native PWM, per-channel measured mapping if supplied.
        if self.calibration is None:
            quantum = PWM_RESOLUTION_US / ESTIMATED_US_PER_RAD
            quantized = np.rint(np.asarray(target) / quantum)*quantum
            return np.clip(quantized, np.ceil(JOINT_LOW/quantum)*quantum,
                           np.floor(JOINT_HIGH/quantum)*quantum)
        c = self.calibration
        zero = np.array(c['zero_us']); gain = np.array(c['us_per_rad'])*c['sign']
        pulse_a = zero+gain*JOINT_LOW; pulse_b = zero+gain*JOINT_HIGH
        pulses = np.clip(np.rint(zero+gain*target),np.ceil(np.minimum(pulse_a,pulse_b)),np.floor(np.maximum(pulse_a,pulse_b)))
        return (pulses-zero)/gain
```

```python
"""Complementary gravity-direction estimator; no perfect quaternion/joint state input.

Accelerometer input is specific force (positive upward at rest). Gyro is body-frame
rad/s. The same update can be used on the PC with raw hardware telemetry.
"""
from collections import deque
import numpy as np
from robot_config import HISTORY, FRAME_SIZE, target_to_action


class GravityEstimator:
    def __init__(self, correction_seconds=0.5):
        self.correction_seconds = correction_seconds
        self.gravity = np.array([0.0, 0.0, -1.0])

    def reset(self, accel):
        a = np.asarray(accel, dtype=float)
        norm = np.linalg.norm(a)
        self.gravity = -a / norm if norm > 1e-6 else np.array([0.0, 0.0, -1.0])

    def update(self, gyro, accel, dt):
        gyro = np.asarray(gyro, dtype=float)
        a = np.asarray(accel, dtype=float)
        g = self.gravity - np.cross(gyro, self.gravity) * dt
        g /= max(np.linalg.norm(g), 1e-9)
        norm = np.linalg.norm(a)
        # Reject obvious impact/free-fall acceleration; smaller dynamic errors remain.
        if 0.8 * 9.81 < norm < 1.2 * 9.81:
            alpha = 1 - np.exp(-dt / self.correction_seconds)
            g = (1 - alpha) * g - alpha * a / norm
            g /= max(np.linalg.norm(g), 1e-9)
        self.gravity = g
        return g.copy()


class ObservationHistory:
    def __init__(self):
        self.frames = deque(maxlen=HISTORY)

    @staticmethod
    def frame(gravity, gyro, applied_target, previous_action):
        return np.concatenate((np.clip(gravity, -1, 1), np.clip(np.asarray(gyro) / 10, -1, 1),
                               target_to_action(applied_target), previous_action)).astype(np.float32)

    def reset(self, frame):
        self.frames.clear()
        for _ in range(HISTORY):
            self.frames.append(np.asarray(frame, dtype=np.float32).copy())
        return self.get()

    def append(self, frame):
        self.frames.append(np.asarray(frame, dtype=np.float32).copy())
        return self.get()

    def get(self):
        obs = np.concatenate(tuple(self.frames)).astype(np.float32)
        if obs.shape != (HISTORY * FRAME_SIZE,) or not np.isfinite(obs).all():
            raise RuntimeError("Invalid observation history")
        return obs
```

```python
"""Evaluation-only geometry/contact diagnostics. Never used in policy observations."""
import numpy as np


def progress_reward(displacement, dt):
    # Positive motion capped, backward motion fully charged: closed cycles cannot earn progress.
    return 10 * min(float(displacement), 0.06 * dt)


class GaitMetrics:
    """Credit translating alternating steps only, with a non-sliding supported stance.

    Foot centers and full-foot minimum heights are ground truth in simulation;
    physical trials must measure these externally using video. Contact alone does
    not prove load support: `supported` is the separate force diagnostic in SIM.
    """
    def __init__(self):
        self.previous = None
        self.airborne = np.zeros(2, dtype=bool)
        self.start = np.zeros((2, 2))
        self.stance_start = np.zeros((2, 2))
        self.clear_time = np.zeros(2)
        self.qualified = np.zeros(2, dtype=bool)
        self.valid_stance = np.ones(2, dtype=bool)
        self.steps = np.zeros(2, dtype=int)
        self.alternations = 0
        self.last = None
        self.distance = 0.0
        self.rejected = 0
        self.max_stance_slip = 0.0

    def update(self, centers, heights, contacts, supported, dt):
        centers = np.asarray(centers, dtype=float)[:, :2]
        contacts, supported = np.asarray(contacts, bool), np.asarray(supported, bool)
        if self.previous is None:
            self.previous = centers.copy()
        for i in range(2):
            j = 1-i
            if not contacts[i]:
                if not self.airborne[i]:
                    self.airborne[i] = True
                    self.start[i] = self.previous[i]
                    self.stance_start[i] = self.previous[j]
                    self.valid_stance[i] = True
                slip = float(np.linalg.norm(centers[j] - self.stance_start[i]))
                self.max_stance_slip = max(self.max_stance_slip, slip)
                self.valid_stance[i] &= bool(contacts[j] and supported[j] and slip <= .003)
                if heights[i] >= .003 and self.valid_stance[i]:
                    self.clear_time[i] += dt
                    self.qualified[i] |= self.clear_time[i] >= .04 - 1e-10
                else:
                    self.clear_time[i] = 0
            elif self.airborne[i]:
                advance = float(centers[i, 0]-self.start[i, 0])
                slip = float(np.linalg.norm(centers[j]-self.stance_start[i]))
                # No credit for hops, in-place lifts, toe pivots, or lifting then sliding.
                valid = (self.qualified[i] and self.valid_stance[i] and supported[i]
                         and supported[j] and slip <= .003 and advance >= .005
                         and abs(centers[i, 1]-self.start[i, 1]) <= .020)
                if valid and (self.last is None or self.last != i):
                    self.steps[i] += 1
                    self.alternations += int(self.last is not None)
                    self.last = i
                    # Two translating feet advance their midpoint by half the summed advance.
                    self.distance += advance/2
                else:
                    self.rejected += 1
                self.airborne[i] = False
                self.qualified[i] = False
                self.clear_time[i] = 0
        self.previous = centers.copy()
```

```python
"""Bounded serial wire format and calibration helpers, with no automatic arming.

Firmware source is in firmware/. Only local compiler/protocol checks are claimed;
physical deployment is pending. All angles here are radians, wire values mrad.
"""
from dataclasses import dataclass
import binascii
import numpy as np
from robot_config import JOINT_LOW, JOINT_HIGH

MAX_FRAME_BYTES = 192
BAUD = 460800  # USB CDC value; sufficient for optional UART implementation too
WATCHDOG_SECONDS = 0.100


def encode_frame(fields):
    payload = ",".join(str(field) for field in fields).encode("ascii")
    crc = binascii.crc_hqx(payload, 0xFFFF)
    frame = payload + f"*{crc:04X}\n".encode("ascii")
    if len(frame) > MAX_FRAME_BYTES:
        raise ValueError("Frame exceeds bounded buffer")
    return frame


def decode_frame(frame):
    if not isinstance(frame, bytes) or len(frame) > MAX_FRAME_BYTES or not frame.endswith(b"\n"):
        raise ValueError("Invalid frame length/termination")
    payload, sep, checksum = frame[:-1].partition(b"*")
    if not sep or len(checksum) != 4:
        raise ValueError("Missing CRC16")
    if binascii.crc_hqx(payload, 0xFFFF) != int(checksum, 16):
        raise ValueError("CRC mismatch")
    fields = payload.decode("ascii").split(",")
    if len(fields) < 2 or fields[1] != "1":
        raise ValueError("Unsupported protocol version")
    return fields


def command_frame(sequence, timestamp_ms, angles):
    q = np.asarray(angles, dtype=float)
    if q.shape != (6,) or not np.isfinite(q).all():
        raise ValueError("Six finite radian targets required")
    if np.any(q < JOINT_LOW) or np.any(q > JOINT_HIGH):
        raise ValueError("Target exceeds joint-safe limits")
    if not 0 <= int(sequence) <= 65535 or not 0 <= int(timestamp_ms) <= 0xFFFFFFFF:
        raise ValueError("Sequence or timestamp out of wire range")
    # Round safe endpoints inward; 35° rounded to 611 mrad would exceed 35°.
    wire = np.clip(np.rint(q * 1000), np.ceil(JOINT_LOW * 1000), np.floor(JOINT_HIGH * 1000)).astype(int)
    return encode_frame(["C", 1, int(sequence), int(timestamp_ms), *wire])


@dataclass(frozen=True)
class Telemetry:
    sequence: int
    timestamp_ms: int
    status: int
    applied_targets: np.ndarray
    accelerometer: np.ndarray
    gyroscope: np.ndarray


def telemetry_frame(frame):
    fields = decode_frame(frame)
    if len(fields) != 17 or fields[0] != "T":
        raise ValueError("Expected T,version,sequence,time,status,6 targets,3 accel,3 gyro")
    values = [int(x) for x in fields[2:]]
    seq, ms, status = values[:3]
    if not (0 <= seq <= 65535 and 0 <= ms <= 0xFFFFFFFF and 0 <= status <= 63):
        raise ValueError("Invalid telemetry header")
    q = np.array(values[3:9], dtype=float) / 1000
    accel = np.array(values[9:12], dtype=float) / 1000
    gyro = np.array(values[12:15], dtype=float) / 1000
    # Quantization of endpoints is allowed, but arbitrary excursions are rejected.
    if np.any(q < JOINT_LOW - 0.001) or np.any(q > JOINT_HIGH + 0.001):
        raise ValueError("Invalid applied command range")
    if np.max(np.abs(accel)) > 16 * 9.81 + 0.01 or np.max(np.abs(gyro)) > np.deg2rad(2000) + 0.01:
        raise ValueError("IMU outside configured sensor ranges")
    return Telemetry(seq, ms, status, q, accel, gyro)


def calibrated_pulses(angles, zero_us, us_per_rad, direction, pulse_min, pulse_max):
    """Per-servo calibration; never infer a universal 0..180 degree PWM mapping."""
    arrays = [np.asarray(a, dtype=float) for a in (angles, zero_us, us_per_rad, direction, pulse_min, pulse_max)]
    if any(a.shape != (6,) or not np.isfinite(a).all() for a in arrays):
        raise ValueError("All calibration arrays must contain six finite values")
    q, zero, gain, sign, low, high = arrays
    if np.any(gain <= 0) or np.any(np.abs(sign) != 1) or np.any(low >= high):
        raise ValueError("Invalid calibration")
    if np.any(q < JOINT_LOW) or np.any(q > JOINT_HIGH):
        raise ValueError("Unsafe angle")
    pulses = zero + sign * gain * q
    if np.any(pulses < low) or np.any(pulses > high):
        raise ValueError("Calibration cannot represent requested angle safely")
    a = zero + sign*gain*JOINT_LOW
    b = zero + sign*gain*JOINT_HIGH
    return np.clip(np.rint(pulses),np.ceil(np.minimum(a,b)),np.floor(np.maximum(a,b))).astype(int)
```

```python
"""Versioned persistent calibration, shared policy identity and deployment gate."""
from pathlib import Path
import hashlib
import json
import numpy as np
from robot_config import ROOT, JOINT_NAMES, JOINT_LOW, JOINT_HIGH, HOME


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def configuration_identity(calibration=None):
    names = ('physical_spec.json', 'robot.xml', 'robot_config.py', 'servo_control.py',
             'imu_observation.py', 'humanoid_env.py', 'gait_metrics.py', 'hardware_interface.py', 'calibration.py', 'firmware/main.cpp', 'firmware/control.h')
    files = {n: hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names}
    return {'configuration': digest(files), 'files': files,
            'calibration': digest(calibration) if calibration else None}


def load_calibration(path, *, require_valid=True):
    c = json.loads(Path(path).read_text())
    if c.get('version') != 1 or c.get('joint_order') != list(JOINT_NAMES):
        raise ValueError('Unsupported calibration version/joint order')
    if require_valid and (c.get('state') != 'measured' or not c.get('validated')):
        raise ValueError('Policy operation requires measured, validated calibration')
    for key in ('sign', 'zero_us', 'us_per_rad', 'pulse_min_us', 'pulse_max_us', 'safe_low_rad', 'safe_high_rad'):
        arr = np.asarray(c[key], float)
        if arr.shape != (6,) or not np.isfinite(arr).all():
            raise ValueError('Invalid calibration array: '+key)
    sign, zero, gain = np.array(c['sign']), np.array(c['zero_us']), np.array(c['us_per_rad'])
    low, high = np.array(c['pulse_min_us']), np.array(c['pulse_max_us'])
    qlo, qhi = np.array(c['safe_low_rad']), np.array(c['safe_high_rad'])
    if np.any(abs(sign) != 1) or np.any(gain <= 0) or np.any(low < 500) or np.any(high > 2500) or np.any(low >= high):
        raise ValueError('Unsafe pulse calibration')
    # Training and hardware must share the entire mapping. Narrower bench ranges need a new model.
    if not np.allclose(qlo, JOINT_LOW, atol=1e-10) or not np.allclose(qhi, JOINT_HIGH, atol=1e-10):
        raise ValueError('Calibration safe limits mismatch physical specification; rebuild and retrain')
    for q in (qlo, qhi, HOME):
        pulses = zero + sign*gain*q
        if np.any(pulses < low+.5) or np.any(pulses > high-.5):
            raise ValueError('Safe angles cannot be represented within pulse bounds')
    R = np.asarray(c['imu']['rotation_sensor_to_body'], float)
    if R.shape != (3,3) or not np.isfinite(R).all() or not np.allclose(R@R.T, np.eye(3), atol=1e-5) or not np.isclose(np.linalg.det(R), 1):
        raise ValueError('IMU alignment must be a proper rotation')
    for key in ('gyro_bias_rad_s','accel_bias_m_s2'):
        a = np.asarray(c['imu'][key], float)
        if a.shape != (3,) or not np.isfinite(a).all():
            raise ValueError('Invalid IMU bias')
    if not 0 < c.get('max_target_speed_rad_s', 0) <= np.pi:
        raise ValueError('Invalid slew limit')
    return c


def pulses_to_angles(pulses, c):
    return (np.asarray(pulses)-c['zero_us'])/(np.array(c['sign'])*c['us_per_rad'])


def check_policy(model_path, *, calibration=None):
    path = Path(model_path)
    if path.suffix != '.zip':
        path = path.with_suffix('.zip')
    metadata = json.loads(path.with_suffix('.manifest.json').read_text())
    if metadata['model_sha256'] != hashlib.sha256(path.read_bytes()).hexdigest():
        raise ValueError('Policy file hash mismatch')
    identity = configuration_identity(calibration)
    if metadata['identity']['configuration'] != identity['configuration']:
        raise ValueError('Policy model/control configuration is incompatible')
    if calibration is not None and metadata['identity']['calibration'] != identity['calibration']:
        raise ValueError('Policy was not trained/approved for this calibration fingerprint')
    return metadata
```

```python
"""USB CDC transport. Opening/handshaking never arms a motor."""
import time
import numpy as np
from calibration import configuration_identity
from hardware_interface import (BAUD, MAX_FRAME_BYTES, encode_frame, decode_frame,
                                telemetry_frame, command_frame)


class SerialRobot:
    def __init__(self, port, calibration, serial_factory=None):
        if serial_factory is None:
            import serial
            serial_factory = serial.Serial
        self.connection = serial_factory(port, BAUD, timeout=.010, write_timeout=.025)
        self.identity = configuration_identity(calibration)
        self.sequence = 0
        self.last_timestamp = None
        self.last_sequence = None
        self.telemetry = None
        self.last_received = 0
        self.buffer = bytearray()
        self.connection.reset_input_buffer()

    def send(self, fields):
        packet = encode_frame(fields)
        if self.connection.write(packet) != len(packet):
            raise IOError('Incomplete USB write')

    def read(self):
        deadline = time.monotonic()+.050
        while time.monotonic() < deadline:
            b = self.connection.read(1)
            if not b:
                continue
            self.buffer.extend(b)
            if len(self.buffer)>MAX_FRAME_BYTES:
                raise ValueError('Oversize incoming frame')
            if b!=b'\n':
                continue
            packet=bytes(self.buffer);self.buffer.clear()
            fields=decode_frame(packet)
            if fields[0]=='I':
                if len(fields)!=5 or fields[2]!=self.identity['configuration'] or fields[3]!=self.identity['calibration']:
                    raise ValueError('Hardware/control/calibration fingerprint mismatch')
                return ('identity',int(fields[4]))
            t=telemetry_frame(packet)
            if self.last_timestamp is not None:
                dt=(t.timestamp_ms-self.last_timestamp)&0xffffffff
                if not 0<dt<100:
                    raise ValueError('Stale/reordered/gapped IMU telemetry')
            self.last_timestamp=t.timestamp_ms
            self.last_received=time.monotonic()
            self.telemetry=t
            return ('telemetry',t)
        raise TimeoutError('No complete frame within 50 ms')

    def handshake(self):
        self.send(['S',1])
        started=time.monotonic()
        self.send(['H',1,self.identity['configuration'],self.identity['calibration'],int(started*1000)&0xffffffff])
        deadline=time.monotonic()+2
        while time.monotonic()<deadline:
            # S acknowledgement may report identity but unmatched; wait for matched H response.
            kind, value=self.read()
            if kind=='identity' and not value&16:
                self.handshake_rtt=time.monotonic()-started
                return value
        raise TimeoutError('No matching hardware handshake')

    def arm(self):
        if getattr(self, 'handshake_rtt', 1) >= .020:
            raise ValueError('Handshake round-trip exceeds provisional 20 ms policy limit')
        self.send(['A',1]) # only an explicit caller can arm
        deadline=time.monotonic()+.100
        while time.monotonic()<deadline:
            kind,value=self.read()
            if kind=='telemetry' and value.status&2:
                raise ValueError(f'Firmware arming fault; status={value.status}')
            if kind=='identity':
                if value != 1:
                    raise ValueError(f'Firmware refused arming; status={value}')
                return
        raise TimeoutError('No arming acknowledgement within100ms')

    def command(self, targets):
        ms=int(time.monotonic()*1000)&0xffffffff
        packet=command_frame(self.sequence,ms,targets)
        if self.connection.write(packet) != len(packet):
            raise IOError("Incomplete command write")
        self.last_sequence=self.sequence
        self.sequence=(self.sequence+1)&0xffff

    def bench(self, channel, pulse_us):
        if not 0<=channel<6 or not 1400<=pulse_us<=1600:
            raise ValueError('Bench restricted to one channel and 1400..1600 us')
        self.send(['B',1,self.sequence,int(time.monotonic()*1000)&0xffffffff,channel,pulse_us])
        self.sequence=(self.sequence+1)&0xffff

    def stop(self):
        self.send(['S',1])

    def close(self):
        try:
            self.stop()
        finally:
            self.connection.close()
```

Bench and deployment tools are part of the checkout; neither auto-arms.

```python
"""Read/log IMU by default. Explicit --channel enables one restricted pulse output."""
import argparse
import csv
import time
from pathlib import Path
from calibration import load_calibration
from serial_robot import SerialRobot


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port',required=True);p.add_argument('--calibration',type=Path,default=Path('calibrations/example.invalid.json'))
    p.add_argument('--seconds',type=float,default=10);p.add_argument('--channel',type=int,choices=range(6));p.add_argument('--pulse-us',type=int,default=1500)
    p.add_argument('--output',type=Path,default=Path('runs/bench.csv'));a=p.parse_args()
    if not 0<a.seconds<=60 or not 1400<=a.pulse_us<=1600:p.error('Use 0..60 seconds and 1400..1600 us')
    c=load_calibration(a.calibration,require_valid=False)
    robot=SerialRobot(a.port,c);a.output.parent.mkdir(parents=True,exist_ok=True)
    try:
        robot.handshake();next_command=time.monotonic();end=next_command+a.seconds
        with a.output.open('x',newline='') as f:
            w=csv.writer(f);w.writerow(['host_ns','mcu_ms','ack','status',*[f'target_{i}' for i in range(6)],'ax','ay','az','gx','gy','gz'])
            while time.monotonic()<end:
                if a.channel is not None and time.monotonic()>=next_command:
                    robot.bench(a.channel,a.pulse_us);next_command+=.02
                kind,t=robot.read()
                if kind=='telemetry':w.writerow([time.monotonic_ns(),t.timestamp_ms,t.sequence,t.status,*t.applied_targets,*t.accelerometer,*t.gyroscope])
    finally:robot.close()

if __name__=='__main__':main()
```

```python
"""Explicitly armed PC inference. Requires measured calibration and compatible policy.

NOT physically verified. A human must have tested cutoff, watchdog and manual poses first.
"""
import argparse
import csv
import time
from pathlib import Path
import numpy as np
from stable_baselines3 import PPO
from calibration import load_calibration,check_policy
from serial_robot import SerialRobot
from imu_observation import GravityEstimator,ObservationHistory
from robot_config import HOME,CONTROL_DT,target_to_action,action_to_target,IMU_ACCEL_RANGE,IMU_GYRO_RANGE


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--port',required=True);p.add_argument('--model',type=Path,required=True);p.add_argument('--calibration',type=Path,required=True)
    p.add_argument('--arm',action='store_true');p.add_argument('--seconds',type=float,default=5);p.add_argument('--output',type=Path,default=Path('runs/hardware.csv'));a=p.parse_args()
    if not a.arm:p.error('Explicit --arm required after physical bench checks')
    if not 0<a.seconds<=30:p.error('Trial duration must be 0..30 seconds')
    c=load_calibration(a.calibration);check_policy(a.model,calibration=c)
    import torch
    torch.set_num_threads(1);model=PPO.load(a.model,device='cpu')
    R=np.array(c['imu']['rotation_sensor_to_body']);gb=np.array(c['imu']['gyro_bias_rad_s']);ab=np.array(c['imu']['accel_bias_m_s2'])
    robot=SerialRobot(a.port,c);est=GravityEstimator();history=ObservationHistory();previous=target_to_action(HOME);last_ms=None
    a.output.parent.mkdir(parents=True,exist_ok=True)
    try:
        robot.handshake()
        # Collect stationary IMU before arming. No true angles/orientation available.
        while robot.telemetry is None:robot.read()
        t=robot.telemetry;est.reset(R@(t.accelerometer-ab))
        history.reset(history.frame(est.gravity,R@(t.gyroscope-gb),t.applied_targets,previous))
        robot.arm();start=time.monotonic();next_command=start
        with a.output.open('x',newline='') as f:
            w=csv.writer(f);w.writerow(['host_ns','mcu_ms','ack','status',*[f'target_{i}' for i in range(6)],'ax','ay','az','gx','gy','gz',*[f'action_{i}' for i in range(6)]])
            while time.monotonic()-start<a.seconds:
                kind,t=robot.read()
                if kind!='telemetry':continue
                if np.any(np.abs(t.accelerometer) >= IMU_ACCEL_RANGE*.99) or np.any(np.abs(t.gyroscope)>=IMU_GYRO_RANGE*.99):
                    raise RuntimeError('IMU saturation software stop')
                if t.status!=1:raise RuntimeError(f'Hardware fault/disarm status {t.status}')
                gyro=R@(t.gyroscope-gb);accel=R@(t.accelerometer-ab)
                if last_ms is not None:est.update(gyro,accel,((t.timestamp_ms-last_ms)&0xffffffff)/1000)
                last_ms=t.timestamp_ms
                if robot.last_sequence is not None and ((robot.last_sequence-t.sequence)&0xffff)>4:
                    raise RuntimeError('Applied command acknowledgement is too old')
                if est.gravity[2]>-.7:raise RuntimeError('IMU tilt software stop')
                now=time.monotonic()
                if now>=next_command:
                    if now-next_command>.04:raise RuntimeError('PC control deadline missed')
                    obs=history.append(history.frame(est.gravity,gyro,t.applied_targets,previous))
                    action=np.clip(model.predict(obs,deterministic=True)[0],-1,1)
                    robot.command(action_to_target(action));previous=action;next_command+=CONTROL_DT
                w.writerow([time.monotonic_ns(),t.timestamp_ms,t.sequence,t.status,*t.applied_targets,*accel,*gyro,*previous])
    finally:robot.close()

if __name__=='__main__':main()
```

Firmware source (C++ official Pico SDK):

```text
cmake_minimum_required(VERSION 3.13)
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)
project(s6_bench C CXX ASM)
set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()
add_executable(s6_bench main.cpp)
target_include_directories(s6_bench PRIVATE ${CMAKE_CURRENT_LIST_DIR})
target_link_libraries(s6_bench pico_stdlib hardware_pwm hardware_i2c hardware_clocks)
target_compile_definitions(s6_bench PRIVATE PICO_STDIO_USB_STDOUT_TIMEOUT_US=0)
pico_enable_stdio_usb(s6_bench 1)
pico_enable_stdio_uart(s6_bench 0)
pico_add_extra_outputs(s6_bench)
```

```cpp
#pragma once
#include <cmath>
#include <cstdint>
#include <cstring>
#include <cstdlib>
#include <cerrno>
#include "generated_config.h"

inline uint16_t crc16(const char* p) {
    uint16_t c=0xffff;
    for (;*p;++p) { c^=uint16_t(uint8_t(*p))<<8; for(int b=0;b<8;++b)c=c&0x8000?(c<<1)^0x1021:c<<1; }
    return c;
}
inline bool integer(const char* text, int64_t& value) {
    static_assert(sizeof(value)>=8, "Wire parser must represent unsigned32 timestamps on ARM");
    if (!text || !*text) return false;
    char* end=nullptr; errno=0; value=strtoll(text,&end,10);
    return !errno && end && !*end;
}
struct Control {
    bool armed=false, bench=false, matched=false, fault=false, have_seq=false, imu=false;
    uint16_t seq=0, ack_seq=0; uint32_t host_ms=0, received_ms=0;
    int channel=-1, bench_us=1500;
    uint32_t clock_offset=0;
    float goal[6]{}, accepted[6]{}, applied[6]{};
    struct Pending {float q[6]; uint16_t seq; uint32_t due;};
    Pending queue[8]{}; unsigned head=0, count=0;
    Control(){for(int i=0;i<6;++i)goal[i]=accepted[i]=applied[i]=HOME_Q[i];}
    void stop(){armed=false;bench=false;channel=-1;have_seq=false;count=0;head=0;}
    void fail(){stop();fault=true;}
    void watchdog(uint32_t now){if((armed||bench) && uint32_t(now-received_ms)>=100)fail();}
    bool accept_time(int64_t s,int64_t t,uint32_t now){
        if(s<0||s>65535||t<0||uint64_t(t)>0xffffffff)return false;
        int32_t age=int32_t(now-(uint32_t(t)+clock_offset));
        if(age>80||age< -20)return false;
        if(have_seq){uint16_t delta=uint16_t(s-seq);uint32_t elapsed=uint32_t(uint32_t(t)-host_ms);
            if(!delta||delta>=32768||!elapsed||elapsed>1000)return false;}
        seq=uint16_t(s);host_ms=uint32_t(t);received_ms=now;have_seq=true;return true;
    }
    // CRC checked before tokenization; fixed stack buffer and no allocation.
    bool packet(char* line,uint32_t now){
        char* star=strchr(line,'*');
        if(!star || strlen(star+1)!=4){fail();return false;}
        *star=0; char* end=nullptr; unsigned long expected=strtoul(star+1,&end,16);
        if(!end||*end||expected!=crc16(line)){fail();return false;}
        char* fields[20]{};int n=0;char* save=nullptr;
        for(char* p=strtok_r(line,",",&save);p;p=strtok_r(nullptr,",",&save)){
            if(n==20){fail();return false;} fields[n++]=p;
        }
        if(n<2||strcmp(fields[1],"1")){fail();return false;}
        if(!strcmp(fields[0],"S")&&n==2){stop();fault=false;matched=false;return true;}
        if(!strcmp(fields[0],"H")&&n==5){
            stop();int64_t ms;matched=!strcmp(fields[2],CONFIG_HASH)&&!strcmp(fields[3],CAL_HASH)&&integer(fields[4],ms)&&ms>=0&&uint64_t(ms)<=0xffffffff;
            if(matched)clock_offset=now-uint32_t(ms);fault=!matched;return matched;
        }
        if(!strcmp(fields[0],"A")&&n==2){
            if(!matched||fault||!CAL_VALID||!imu){fail();return false;}
            armed=true;bench=false;received_ms=now;have_seq=false;return true;
        }
        if(!strcmp(fields[0],"B")&&n==6){
            int64_t s,t,c,p;
            if(!matched||fault||armed||!integer(fields[2],s)||!integer(fields[3],t)||!integer(fields[4],c)||!integer(fields[5],p)||c<0||c>5||p<1400||p>1600||!accept_time(s,t,now)){fail();return false;}
            bench=true;channel=c;bench_us=p;return true;
        }
        if(!strcmp(fields[0],"C")&&n==10){
            int64_t s,t,q[6];
            if(!armed||fault||!imu||!integer(fields[2],s)||!integer(fields[3],t)){fail();return false;}
            for(int i=0;i<6;++i)if(!integer(fields[i+4],q[i])||q[i]*.001<QMIN[i]||q[i]*.001>QMAX[i]){fail();return false;}
            if(!accept_time(s,t,now)){fail();return false;}
            if(count>=8){fail();return false;}
            Pending& item=queue[(head+count)%8];item.seq=seq;item.due=now+20;
            for(int i=0;i<6;++i)item.q[i]=q[i]*.001f;
            ++count;
            return true;
        }
        fail();return false;
    }
    int pulse(int i)const{
        float a=ZERO[i]+SIGN[i]*GAIN[i]*QMIN[i],b=ZERO[i]+SIGN[i]*GAIN[i]*QMAX[i];
        float low=std::ceil(std::fmin(a,b)),high=std::floor(std::fmax(a,b));
        return int(std::fmax(low,std::fmin(high,float(std::lround(ZERO[i]+SIGN[i]*GAIN[i]*applied[i])))));
    }
    void tick(uint32_t now){
        if(!armed)return;
        while(count && int32_t(now-queue[head].due)>=0){
            Pending& item=queue[head];
            for(int i=0;i<6;++i){if(std::abs(item.q[i]-accepted[i])>=.008726646f)accepted[i]=item.q[i];goal[i]=accepted[i];}
            ack_seq=item.seq;head=(head+1)%8;--count;
        }
        for(int i=0;i<6;++i){
            float change=goal[i]-applied[i]; // provisional .5 degree deadband
            applied[i]+=std::fmax(-MAX_SPEED*.02f,std::fmin(MAX_SPEED*.02f,change));
            if(pulse(i)<PMIN[i]||pulse(i)>PMAX[i]){fail();return;}
        }
    }
    unsigned status()const{return (armed?1:0)|(fault?2:0)|(!imu?4:0)|(!CAL_VALID?8:0)|(!matched?16:0)|(bench?32:0);}
};
```

```cpp
#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include "hardware/clocks.h"
#include "hardware/i2c.h"
#include "control.h"
#include <cstdio>
#include <cstdarg>

constexpr uint PINS[6]={0,1,2,3,6,7};
Control ctrl;
float accel[3]{},gyro[3]{};
void send(const char* format,...){
    char body[180];va_list args;va_start(args,format);vsnprintf(body,sizeof(body),format,args);va_end(args);
    printf("%s*%04X\n",body,crc16(body));
}
bool reg(uint8_t r,uint8_t v){uint8_t b[2]={r,v};return i2c_write_timeout_us(i2c0,0x68,b,2,false,1500)==2;}
bool whoami(){
    uint8_t r=0x75,id=0;
    return i2c_write_timeout_us(i2c0,0x68,&r,1,true,1500)==1 && i2c_read_timeout_us(i2c0,0x68,&id,1,false,1500)==1 && id==0x68;
}
bool sample(){
    uint8_t r=0x3b,b[14];
    if(i2c_write_timeout_us(i2c0,0x68,&r,1,true,1500)!=1 || i2c_read_timeout_us(i2c0,0x68,b,14,false,1500)!=14)return false;
    auto raw=[&](int i){return int16_t((uint16_t(b[i])<<8)|b[i+1]);};
    for(int i=0;i<3;++i){accel[i]=raw(i*2)*9.80665f/16384;gyro[i]=raw(8+i*2)*.01745329252f/131;}
    return true;
}
void output(){
    for(int i=0;i<6;++i){int pulse=ctrl.armed?ctrl.pulse(i):(ctrl.bench&&ctrl.channel==i?ctrl.bench_us:0);pwm_set_gpio_level(PINS[i],pulse);}
}
int main(){
    stdio_init_all();
    for(auto pin:PINS){gpio_init(pin);gpio_put(pin,0);gpio_set_dir(pin,GPIO_OUT);}
    for(auto pin:PINS){
        gpio_set_function(pin,GPIO_FUNC_PWM);auto slice=pwm_gpio_to_slice_num(pin);
        pwm_config cfg=pwm_get_default_config();pwm_config_set_clkdiv(&cfg,float(clock_get_hz(clk_sys))/1000000.f);pwm_config_set_wrap(&cfg,19999);
        pwm_init(slice,&cfg,true);pwm_set_gpio_level(pin,0);
    }
    i2c_init(i2c0,400000);gpio_set_function(4,GPIO_FUNC_I2C);gpio_set_function(5,GPIO_FUNC_I2C);gpio_pull_up(4);gpio_pull_up(5);
    sleep_ms(100);
    // MPU6050: wake, DLPF=3 (~44Hz accel/42Hz gyro), sample divider4 ->200Hz, +/-2g,+/-250deg/s.
    bool configured=whoami()&&reg(0x6b,1)&&reg(0x1a,3)&&reg(0x19,4)&&reg(0x1b,0)&&reg(0x1c,0);
    char line[192];unsigned used=0;bool overflow=false;uint32_t next_imu=0,next_control=0;
    while(true){
        uint32_t now=to_ms_since_boot(get_absolute_time());ctrl.watchdog(now);
        if(int32_t(now-next_imu)>=0){
            next_imu=now+5;ctrl.imu=configured&&sample();
            if(!ctrl.imu && ctrl.armed)ctrl.fail();
            send("T,1,%u,%lu,%u,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d",ctrl.ack_seq,(unsigned long)now,ctrl.status(),
                 int(std::lround((ctrl.pulse(0)-ZERO[0])/(SIGN[0]*GAIN[0])*1000)),int(std::lround((ctrl.pulse(1)-ZERO[1])/(SIGN[1]*GAIN[1])*1000)),int(std::lround((ctrl.pulse(2)-ZERO[2])/(SIGN[2]*GAIN[2])*1000)),int(std::lround((ctrl.pulse(3)-ZERO[3])/(SIGN[3]*GAIN[3])*1000)),int(std::lround((ctrl.pulse(4)-ZERO[4])/(SIGN[4]*GAIN[4])*1000)),int(std::lround((ctrl.pulse(5)-ZERO[5])/(SIGN[5]*GAIN[5])*1000)),
                 int(accel[0]*1000),int(accel[1]*1000),int(accel[2]*1000),int(gyro[0]*1000),int(gyro[1]*1000),int(gyro[2]*1000));
        }
        if(int32_t(now-next_control)>=0){next_control=now+20;ctrl.tick(now);}
        int ch=getchar_timeout_us(0);
        if(ch>=0){
            if(ch=='\n'){
                if(overflow){ctrl.fail();}else{line[used]=0;bool ok=ctrl.packet(line,now);if(ok)send("I,1,%s,%s,%u",CONFIG_HASH,CAL_HASH,ctrl.status());}
                used=0;overflow=false;
            }else if(ch<32||ch>126||used>=sizeof(line)-1){overflow=true;ctrl.fail();}
            else if(!overflow)line[used++]=char(ch);
        }
        output(); // immediate PWM disable on fault; servo electronics may still retain position
        tight_loop_contents();
    }
}
```

Invalid calibration example (must remain non-deployable):

```json
{
  "version": 1,
  "state": "estimated",
  "validated": false,
  "date": "2026-10-23",
  "evidence": "EXAMPLE ONLY. Never deploy without per-servo/IMU measurements.",
  "joint_order": [
    "left_hip",
    "left_knee",
    "left_ankle",
    "right_hip",
    "right_knee",
    "right_ankle"
  ],
  "sign": [
    1,
    1,
    1,
    -1,
    -1,
    -1
  ],
  "zero_us": [
    1500,
    1500,
    1500,
    1500,
    1500,
    1500
  ],
  "us_per_rad": [
    500,
    500,
    500,
    500,
    500,
    500
  ],
  "pulse_min_us": [
    900,
    900,
    900,
    900,
    900,
    900
  ],
  "pulse_max_us": [
    2100,
    2100,
    2100,
    2100,
    2100,
    2100
  ],
  "safe_low_rad": [
    -0.6108652381980153,
    -0.17453292519943295,
    -0.3490658503988659,
    -0.6108652381980153,
    -0.17453292519943295,
    -0.3490658503988659
  ],
  "safe_high_rad": [
    0.6108652381980153,
    1.0471975511965976,
    0.3490658503988659,
    0.6108652381980153,
    1.0471975511965976,
    0.3490658503988659
  ],
  "max_target_speed_rad_s": 3.141592653589793,
  "imu": {
    "rotation_sensor_to_body": [
      [
        1,
        0,
        0
      ],
      [
        0,
        1,
        0
      ],
      [
        0,
        0,
        1
      ]
    ],
    "gyro_bias_rad_s": [
      0,
      0,
      0
    ],
    "accel_bias_m_s2": [
      0,
      0,
      0
    ]
  }
}
```

Build-time persistent configuration generator:

```python
"""Generate build-persistent Pico calibration. Default deliberately cannot policy-arm."""
import argparse
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from calibration import load_calibration, configuration_identity
from robot_config import HOME


def generate(path, output):
    c = load_calibration(path, require_valid=False)
    ident = configuration_identity(c)
    def array(v):
        return '{'+','.join(f'{float(x):.10g}f' if float(x) != int(float(x)) else f'{int(x)}.0f' for x in v)+'}'
    text = '#pragma once\n// Generated. Calibration persists in firmware flash; reboot always disarmed.\n'
    text += f'constexpr const char* CONFIG_HASH="{ident["configuration"]}";\n'
    text += f'constexpr const char* CAL_HASH="{ident["calibration"]}";\n'
    text += f'constexpr bool CAL_VALID={str(c["state"]=="measured" and c["validated"]).lower()};\n'
    for key,name in [('sign','SIGN'),('zero_us','ZERO'),('us_per_rad','GAIN'),('pulse_min_us','PMIN'),('pulse_max_us','PMAX'),('safe_low_rad','QMIN'),('safe_high_rad','QMAX')]:
        text+=f'constexpr float {name}[6]={array(c[key])};\n'
    text+=f'constexpr float HOME_Q[6]={array(HOME)};\nconstexpr float MAX_SPEED={c["max_target_speed_rad_s"]:.10g}f;\n'
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(text)
    print(json.dumps({'configuration':ident['configuration'],'calibration':ident['calibration'],'policy_arm_allowed':c['validated'] and c['state']=='measured'}))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--calibration',type=Path,default=ROOT/'calibrations/example.invalid.json');p.add_argument('--output',type=Path,default=ROOT/'firmware/generated_config.h');a=p.parse_args();generate(a.calibration,a.output)
```

## 12. Full train.py

```python
"""Bounded, reproducible PPO. Prototype experiments require --development explicitly."""
import argparse
import hashlib
import json
from pathlib import Path
from dataclasses import asdict
import numpy as np
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from humanoid_env import HumanoidEnv
from robot_config import ROOT, DR
from calibration import configuration_identity, load_calibration, check_policy, digest

ROLLOUT=1024
VALIDATION_SEEDS=tuple(range(2000,2005))
FINAL_SEEDS=tuple(range(1000,1010))
ALGORITHM={'learning_rate':3e-4,'n_steps':ROLLOUT,'batch_size':64,'n_epochs':10,
           'gamma':.99,'gae_lambda':.95,'clip_range':.2,'ent_coef':.005,
           'policy_kwargs':{'net_arch':[64,64]}}


def weight_hash(policy):
    h=hashlib.sha256()
    for name,value in sorted(policy.state_dict().items()):
        h.update(name.encode());h.update(value.detach().cpu().numpy().tobytes())
    return h.hexdigest()


def save_policy(model,path,manifest):
    path=Path(path).with_suffix('.zip');path.parent.mkdir(parents=True,exist_ok=True)
    model.save(path)
    record={**manifest,'actual_timesteps':model.num_timesteps,
            'model_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    path.with_suffix('.manifest.json').write_text(json.dumps(record,indent=2)+'\n')


class Validation(BaseCallback):
    """Same validation seeds at every checkpoint; final test seeds never select models."""
    def __init__(self, output, manifest, seconds, interval=10240):
        super().__init__();self.output=output;self.manifest=manifest;self.seconds=seconds
        self.interval=interval;self.best=None;self.records=[];self.last_evaluated=-1

    def validate(self):
        rows=[]
        for randomized in (False,True):
            env=HumanoidEnv(domain_randomization=randomized,episode_seconds=self.seconds,calibration=self.manifest.get('calibration_record'))
            try:
                for seed in VALIDATION_SEEDS:
                    obs,info=env.reset(seed=seed);done=False
                    while not done:
                        obs,_,term,trunc,info=env.step(self.model.predict(obs,deterministic=True)[0]);done=term or trunc
                    rows.append({'seed':seed,'randomized':randomized,**{k:v for k,v in info.items() if k!='reward_terms'}})
            finally:env.close()
        score=(sum(r['walking_success'] for r in rows),float(np.mean([r['gait_distance_m'] for r in rows])),float(np.mean([r['total_reward'] for r in rows])))
        self.records.append({'timesteps':self.model.num_timesteps,'selection_score':score,'episodes':rows})
        (self.output/'validation.json').write_text(json.dumps(self.records,indent=2)+'\n')
        save_policy(self.model,self.output/'checkpoints'/f'ppo_{self.model.num_timesteps}',self.manifest)
        if self.best is None or score>self.best:
            self.best=score;save_policy(self.model,self.output/'best_model',self.manifest)
        self.last_evaluated=self.model.num_timesteps

    def _on_step(self):
        # Validate completed rollouts only, including after the corresponding PPO update.
        return True

    def _on_rollout_start(self):
        if self.model.num_timesteps and self.model.num_timesteps%self.interval==0:self.validate()

    def _on_training_end(self):
        if self.last_evaluated!=self.model.num_timesteps:self.validate()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--steps',type=int,default=2048,help='TOTAL seed/condition budget, including resumed timesteps; rounds DOWN')
    p.add_argument('--seed',type=int,choices=(0,1,2),default=0);p.add_argument('--randomize',action='store_true')
    p.add_argument('--output',type=Path,default=ROOT/'runs/smoke');p.add_argument('--episode-seconds',type=float,default=30)
    p.add_argument('--resume',type=Path);p.add_argument('--calibration',type=Path)
    p.add_argument('--stage',choices=('smoke','pilot','formal'),default='smoke');p.add_argument('--development',action='store_true')
    a=p.parse_args();cap={'smoke':2048,'pilot':50000,'formal':1000000}[a.stage]
    budget=(min(a.steps,cap)//ROLLOUT)*ROLLOUT
    if a.steps>cap or budget<ROLLOUT:p.error(f'Budget must be 1024..{cap}; no automatic expansion')
    gates=json.loads((ROOT/'docs/gates.json').read_text())
    if a.stage=='formal' and not all(gates.values()):p.error('Formal experiment blocked: '+', '.join(k for k,v in gates.items() if not v))
    if not a.development and not all(gates.values()):p.error('Twin is provisional. Use --development for explicitly provisional smoke/pilot only')
    if a.development and a.stage=='formal':p.error('Development flag does not bypass formal gates')
    if a.output.exists() and any(a.output.iterdir()):p.error('Use a new empty run directory; preserve previous evidence')
    c=load_calibration(a.calibration) if a.calibration else None
    torch.set_num_threads(1)
    env=HumanoidEnv(domain_randomization=a.randomize,episode_seconds=a.episode_seconds,calibration=c)
    check_env(env,warn=True)
    a.output.mkdir(parents=True,exist_ok=True);env=Monitor(env,str(a.output/'training'))
    manifest={'seed':a.seed,'condition':'B' if a.randomize else 'A','randomization':a.randomize,
              'randomization_config':asdict(DR),'budget':budget,'requested_budget':a.steps,'stage':a.stage,
              'calibration_record':c,'episode_seconds':a.episode_seconds,'identity':configuration_identity(c),'algorithm':ALGORITHM,
              'validation_seeds':VALIDATION_SEEDS,'reserved_final_seeds':FINAL_SEEDS,
              'source_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ('train.py','evaluate.py')},
              'status':'provisional development simulation' if a.development else 'gate-cleared simulation; no physical result'}
    try:
        if a.resume:
            old=check_policy(a.resume,calibration=c)
            for key in ('seed','condition','algorithm','episode_seconds'):
                if old[key]!=manifest[key]:raise ValueError('Cannot resume across changed '+key)
            model=PPO.load(a.resume,env=env,device='cpu');manifest['initial_policy_sha256']=old['initial_policy_sha256']
            manifest['resumed_from']=str(a.resume);manifest['resumed_model_sha256']=old['model_sha256']
            if model.num_timesteps>=budget:raise ValueError('Total budget already consumed')
        else:
            model=PPO('MlpPolicy',env,**ALGORITHM,seed=a.seed,device='cpu',verbose=1)
            manifest['initial_policy_sha256']=weight_hash(model.policy)
            save_policy(model,a.output/'untrained_model',manifest)
        model.tensorboard_log=str(a.output/'tensorboard')
        (a.output/'training_config.json').write_text(json.dumps(manifest,indent=2)+'\n')
        callback=Validation(a.output,manifest,a.episode_seconds)
        if a.resume:
            previous_scores=Path(a.resume).parent/'validation.json'
            if previous_scores.exists():
                history=json.loads(previous_scores.read_text());callback.best=max(tuple(r['selection_score']) for r in history)
                # Keep prior winner accessible; selection across pilot/final must not discard it.
                manifest['prior_validation']=str(previous_scores)
                import shutil
                for suffix in ('.zip','.manifest.json'):
                    src=Path(a.resume).parent/('best_model'+suffix)
                    if src.exists():shutil.copy2(src,a.output/src.name)
        remaining=budget-model.num_timesteps
        model.learn(total_timesteps=remaining,callback=callback,reset_num_timesteps=not bool(a.resume))
        save_policy(model,a.output/'final_model',manifest)
        (a.output/'completed.json').write_text(json.dumps({'actual_timesteps':model.num_timesteps,'budget':budget,'initial_policy_sha256':manifest['initial_policy_sha256']},indent=2)+'\n')
    finally:env.close()

if __name__=='__main__':main()
```

## 13. Full evaluate.py

```python
"""Evaluate policy/neutral baseline, distinguish forward sliding from lifted steps."""
import argparse
import csv
import json
import time
from pathlib import Path
import numpy as np
from humanoid_env import HumanoidEnv
from robot_config import ROOT, HOME, CONTROL_DT, target_to_action


def evaluate(model_path=None, episodes=10, seed=1000, randomize=False,
             output=ROOT / "runs" / "evaluation", video=False, render=False,
             episode_seconds=30, baseline="home", policy_seed=0):
    output = Path(output)
    if episodes <= 0:
        raise ValueError("episodes must be positive")
    if output.exists() and any(output.iterdir()):
        raise ValueError("Use a new empty output directory; preserve previous evidence")
    output.mkdir(parents=True, exist_ok=True)
    if video and render:
        raise ValueError("Choose video or human rendering, not both")
    mode = "rgb_array" if video else "human" if render else None
    from calibration import check_policy
    metadata = check_policy(model_path) if model_path else None
    env = HumanoidEnv(render_mode=mode, domain_randomization=randomize, episode_seconds=episode_seconds,
                      calibration=metadata.get("calibration_record") if metadata else None)
    model = None
    if model_path:
        from stable_baselines3 import PPO
        import torch
        torch.set_num_threads(1)
        from calibration import check_policy
        check_policy(model_path)
        model = PPO.load(model_path, device="cpu")
    if not model_path and baseline == "untrained":
        from stable_baselines3 import PPO
        from train import ALGORITHM
        import torch
        torch.set_num_threads(1)
        model = PPO("MlpPolicy", env, **ALGORITHM, seed=policy_seed, device="cpu")
    records = []
    writer = None
    try:
        if video:
            import imageio.v2 as imageio
            writer = imageio.get_writer(output / "episode_0.mp4", fps=50, codec="libx264", macro_block_size=16)
        for episode in range(episodes):
            obs, info = env.reset(seed=seed + episode)
            terminated = truncated = False
            while not (terminated or truncated):
                started = time.monotonic()
                action = model.predict(obs, deterministic=True)[0] if model else target_to_action(HOME)
                obs, reward, terminated, truncated, info = env.step(action)
                if writer is not None and episode == 0:
                    writer.append_data(env.render())
                if render:
                    time.sleep(max(0, CONTROL_DT - (time.monotonic() - started)))
            row = {k: v for k, v in info.items() if k != "reward_terms"}
            row.update(episode=episode, seed=seed + episode, terminated=terminated, truncated=truncated)
            records.append(row)
            print(json.dumps(row))
        summary = {"episodes": episodes, "falls": sum(r["fallen"] for r in records),
                   "fall_rate": float(np.mean([r["fallen"] for r in records])),
                   "mean_distance_m": float(np.mean([r["distance_m"] for r in records])),
                   "mean_forward_speed_m_s": float(np.mean([r["mean_speed_m_s"] for r in records])),
                   "mean_duration_s": float(np.mean([r["duration_s"] for r in records])),
                   "mean_total_reward": float(np.mean([r["total_reward"] for r in records])),
                   "mean_gait_distance_m": float(np.mean([r["gait_distance_m"] for r in records])),
                   "walking_successes": sum(r["walking_success"] for r in records),
                   "domain_randomization": randomize, "policy": str(model_path) if model_path else baseline + " baseline"}
        import hashlib
        from calibration import configuration_identity
        summary["identity"] = metadata["identity"] if metadata else configuration_identity()
        summary["model_sha256"] = hashlib.sha256(Path(model_path).read_bytes()).hexdigest() if model_path else None
        summary["policy_seed"] = policy_seed if baseline == "untrained" else None
        summary["xml_sha256"] = hashlib.sha256((ROOT / "robot.xml").read_bytes()).hexdigest()
        summary["seeds"] = list(range(seed, seed + episodes))
        with (output / "episodes.csv").open("w", newline="") as f:
            c = csv.DictWriter(f, fieldnames=list(records[0]))
            c.writeheader(); c.writerows(records)
        (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(json.dumps(summary, indent=2))
        return summary
    finally:
        if writer is not None:
            writer.close()
        env.close()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model", type=Path)
    p.add_argument("--baseline", choices=("home", "untrained"), default="home")
    p.add_argument("--policy-seed", type=int, default=0)
    p.add_argument("--episodes", type=int, default=10)
    p.add_argument("--seed", type=int, default=1000)
    p.add_argument("--randomize", action="store_true")
    p.add_argument("--output", type=Path, default=ROOT / "runs" / "evaluation")
    p.add_argument("--episode-seconds", type=float, default=30)
    group = p.add_mutually_exclusive_group()
    group.add_argument("--video", action="store_true")
    group.add_argument("--render", action="store_true")
    args = p.parse_args()
    if args.episodes <= 0:
        p.error("--episodes must be positive")
    evaluate(args.model, args.episodes, args.seed, args.randomize, args.output,
             args.video, args.render, args.episode_seconds, args.baseline, args.policy_seed)


if __name__ == "__main__":
    main()
```

## 14. requirements.txt

Tested Linux/Python3.12 CPU dependencies, pinned top-level releases (not a full
transitive lock). C++ ARM toolchain and official Pico SDK are separate installs.

```text
# Linux/Python 3.12; versions installed and tested for this handoff.
# CPU wheels keep CUDA packages out of this small PPO project.
--extra-index-url https://download.pytorch.org/whl/cpu
torch==2.14.1+cpu
mujoco==3.15.0
gymnasium==1.4.0
stable-baselines3==2.9.0
numpy==2.5.3
tensorboard==2.21.0
pyserial==3.5
imageio==2.38.1
imageio-ffmpeg==0.6.0
```

```text
-r requirements.txt
pytest==9.1.1
trimesh==5.1.1
manifold3d==3.5.4
matplotlib==3.11.2
cmake==3.31.10
ninja==1.13.2
```

## 15. Run simulation, training and evaluation

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python tools/budget_gate.py  # exit2 incomplete,1 overbudget,0 cleared
python evaluate.py --episodes 5 --seed 2000 --output runs/new_home
python train.py --steps 2048 --development --output runs/new_smoke
python train.py --stage pilot --steps 50000 --development \
  --resume runs/new_smoke/final_model.zip --output runs/new_pilot
MUJOCO_GL=egl python evaluate.py --model runs/new_pilot/best_model.zip \
  --episodes 5 --seed 2000 --video --output runs/new_pilot_validation
python train.py --steps 2048 --randomize --development --output runs/new_smoke_B
tensorboard --logdir runs
```

Steps mean TOTAL budget including resume;50000 rounds DOWN to49152. Outputs
must be new directories; retain manifests beside ZIPs. Resume rejects changed
condition/seed/algorithm/twin. Never resume nominal A into randomized B.
A/B fresh seeds initialize identical weights; B gets no extra nominal pretraining.
2048development A/B smoke does not establish a final comparison.

Formal stages remain blocked by `docs/gates.json`. Once actual evidence clears
them, train seeds0,1,2 in A/B at equal budgets (1000000rounds down999424), with
matching initial weights, validation2000–2004 and held-out1000–1009:

```bash
python tools/experiments.py --calibration calibrations/measured-v1.json \
  --steps 1000000 --output runs/formal_measured_v1
```

The runner saves policies, validation/checkpoints, both-condition evaluations,
home/untrained baselines, CSV/JSON/video and aggregate results. It does not clear
gates automatically. Pilot counts toward final if unchanged; use train --resume
with the total target budget and preserve earlier winner metadata.

Rendering: --video saves first episode MP4; --render opens passive desktop viewer.
Headless physics needs no display. EGL worked locally; OSMesa is another runtime
option where installed. Historical checkpoints are incompatible with the current controller fingerprint
(use tools/replay_snapshot.py for isolated review) and are kept as historical evidence, not silently loaded with overrides.

Geometry regeneration (only before measured masses):

```bash
python cad/build_frame.py
python tools/sync_frame_mass.py # refuses measured masses; CAD estimates only
python build_model.py
python tools/check_clearance.py # fails on conflicts; no manufacturing release
python tools/torque_estimates.py
python tools/firmware_config.py
python tools/build_handoff.py
python tools/package_project.py
```

## 16. Calibration procedure for the real robot

### Parameters to measure on the real robot

All numbers currently in `physical_spec.json` and `robot_config.py` are estimates except the explicitly labelled seller claims. A school kitchen scale, ruler, protractor, phone camera, known weights and a borrowed multimeter are enough to replace many estimates. No prolonged stall tests.

| Parameter | Inexpensive procedure | Where it goes |
|---|---|---|
| Housing/ears/shaft/horns | Photograph one servo against a ruler, measure ear hole pitch/diameter, shaft centre relative to the body, axial shaft height, horn screw thread, horn holes, supplied screws and lead exit. Have a sample printed interface checked before all prints. | `physical_spec.json` servo dimensions; `cad/build_frame.py` cradle/horn geometry |
| Angle range, offsets, sign | With one unloaded unmounted horn, start near a measured centre pulse. Increase in small increments; stop before buzzing or mechanical stops. Use a protractor/video. Repeat from both directions. Fit angle versus pulse, record sign and repeatability for all six servos. Shrink safe angles 5–10° from measured ends. | Safe command limits/HOME in JSON; measured mechanical travel separately; MCU calibration arrays; action map reads JSON |
| Backlash/deadband | Power off and gently reverse a tiny known load; film horn position. Compare pulse-angle curves approaching the same angle from both directions. Distinguish gear play from commanded deadband and structural flex. | `SERVO_DEADBAND`; potentially a shaft-play model; measured offset/noise ranges |
| Unloaded and loaded speed | Film a 10–20° step at 120/240 fps alongside timestamped command/ack LEDs or screen. Repeat with a safe small load in both directions, at measured servo voltage. | No-load speed envelope, target slew limit, kp/kv fitted jointly |
| Command and shaft latency | Log PC send, MCU receive, PWM apply and ack timestamps. Film the first shaft movement. Measure distribution over at least 100 commands. Synchronize clocks via handshake; do not call round-trip time one-way latency. | `BASE_DELAY`, DR delay ticks/distribution, controller scheduling; position-actuator response parameters |
| Approximate usable torque | Clamp a single test servo in a finished holder, attach a known short lever and known mass. Torque = mass × 9.81 × perpendicular lever length. Increase briefly until tracking deteriorates, then back off substantially. E.g. 100 g at 20 mm gives 0.0196 N·m. Test repeated gentle holds/moves with temperature and current checks. Stop on buzzing, hot case or rapid voltage sag. | Intermittent `SERVO_TORQUE` and strength uncertainty; this is not an industrial continuous rating |
| Current and voltage | Measure single-servo rest/movement/brief loaded current, then total on a conservative pose. Use correct meter range/fused current jack; measure current in series and voltage in parallel. Phone video captures intermittent readings, but a basic meter may miss peaks. Check voltage at the farthest servo and connector temperature. | PSU/harness feasibility and current assumptions; optional measured supply-droop model |
| Total and body masses | Weigh servo with lead, frame, horn/fasteners, PCB/headers, sole and attached wire separately. Then weigh each assembled rigid body and the complete robot. Assign every item once, including lead sections on the body that carries them. Support the tether externally. | JSON component masses; rerun `build_model.py`; aim <250 g |
| COM/inertia | Balance each unpowered assembled rigid body on two perpendicular edges or suspend it from two points; intersect plumb lines for COM. Use measured dimensions and mass distribution for box/parallel-axis inertia. More accurate inertia requires a pendulum experiment, not necessary initially. | JSON component COM and optional inertia tensor; all inertia entries kg·m² |
| Foot friction | Finished sole on intended flat material: slowly incline a board and note sliding angle θ. Start coefficient estimate μ ≈ tan(θ); repeat at different loads and orientations. This approximates static friction; dynamic friction may differ. | Floor/sole sliding friction; DR ±15% only if measurements support it |
| Joint friction/damping | Compare slow forward/reverse sweeps under known small loads, and commanded step settling videos. Powered-off servos resist motion through gears; do not force them. Fit passive friction/damping together with active gains, not from one video. | MJCF joint damping/frictionloss; recalibrate after wear |
| IMU biases and alignment | Record 30–60 s at rest in several known orientations, use +/− axis gravity poses. Subtract stationary gyro bias; fit accelerometer offset/scale and sensor-to-torso rotation. Keep raw MCU outputs in sensor coordinates; apply calibrated torso rotation on the PC. | PC bias/axis transform, estimator calibration, measured DR biases/noise |
| IMU noise | Record stationary 200 Hz samples and report per-axis standard deviation, bias drift, clipping and timestamps. Fit randomization from actual distributions. Repeat with servos powered. | GYRO_NOISE, ACCEL_NOISE, DR sensor scale/bias |
| Tether disturbance | Repeat identical standing trials with cable slack in different directions. Weigh unsupported cable section and video its pull. | Experimental confound; later conservative external-force randomization if needed |

Fit servo response from several amplitudes/loads, not one fast motion. The XML position actuator, torque-speed envelope and target deadband are approximations: gain tuning cannot recover missing feedback or a gearbox failure. Keep calibration records per physical servo so replacement parts can be remeasured.

After mechanical edits: regenerate CAD, review clearances, update **measured** body masses/COM/inertia in JSON, then generate MJCF. `tools/sync_frame_mass.py` overwrites frame mass with a solid CAD estimate: **do not run it over measured masses**. Use it only while designing the prototype. Update model and controller safe limits together; old policies are invalid when geometry, joint order, angle mapping or observation preprocessing change. Keep a versioned measured specification beside every training result.

#### Persistent records and measurement submission (2026-10-23 revision)

Current controller is **native Pico PWM**, not PCA9685. MPU raw samples remain
in sensor coordinates; the PC applies bias/alignment, then the same gravity
filter as SIM. Sample ranges are±2g/±250°/s with44Hz DLPF; watch saturation.
Safe command intervals and measured mechanical travel are separate fields in
`physical_spec.json`; unknown physical stops stay null and absent from MJCF.
Do not write narrowed safe limits into mechanical-stop fields to prop up SIM.

Start by copying `calibrations/example.invalid.json` to a new revision. Keep
`validated=false` until every channel and IMU transform has recorded evidence.
Fit `pulse_us = zero_us + sign * us_per_rad * joint_radians` separately for each
servo, with positive joint axes matching the MJCF. Save pulse bounds, safe-angle
bounds, serial/batch labels, date, voltage/load/temperature and source videos.
Calibration safe angles must match the physical ledger exactly: if narrowed,
update the ledger, regenerate the model, rerun checks and retrain. Do not merely
clip a policy trained on a wider range during deployment.

Record actual measured state/evidence/date on every replaced physical parameter.
Do not claim CAD-generated inertia is measured because its input mass was weighed:
retain estimated inertia unless experimentally identified. Weigh each complete
rigid body, then update component allocation so totals agree without counting
servo cases, horns or cables twice. A sample servo/horn and interface print must
be confirmed before ordering the full frame.

Use `bench.py` to record stationary IMU and a deliberately enabled single channel.
The restricted1400–1600µs window is a **bench bound, not a guarantee of mechanical
safety**. Start unmounted with the horn removed. Wider pulse exploration needs
a reviewed firmware revision based on measured travel; do not bypass bounds by
editing arbitrary values while a robot is assembled. Timestamped telemetry logs
and video identify command-to-PWM and PWM-to-shaft delays separately. USB round
trip is not one-way latency. A cheap meter can miss current peaks: treat readings
as incomplete peak evidence. Avoid prolonged stalls or hot servos.

Fit provisional gains/strength/damping/speed in `physical_spec.json`'s `dynamics`
from **multiple** step amplitudes and loaded/unloaded trials. Minimize angle
trajectory error across held-out steps, inspect overshoot and settling, then
bound residual variation for DR. `tools/fit_response.py` provides a simple
first-order delay/time-constant diagnostic; it is not automatic identification
of MuJoCo kp/kv/torque. Replace the PWM gain in calibration and the unloaded-speed
claim with measurements. The environment uses supplied per-channel calibration
for PWM quantization. Do not broaden DR to conceal a bad nominal fit.

After validation, set measured state/validated flag, generate the firmware header,
build/flash with motor power disconnected, and train with `--calibration` pointing
to that exact JSON. Flash persistence is build-time; no armed serial calibration
write exists. A changed physical/control/calibration hash invalidates prototype
policies and the firmware handshake until both are rebuilt. Keep old policies
and measurements as historical evidence rather than relabelling them compatible.

Templates live in `docs/templates/`; fill one measurement row per trial and keep
original CSV/video. Until those records exist, stages A/B/D/F remain blocked or
provisional and nothing is physically verified.

## 17. Sim-to-Real and domain-randomization plan

The `Randomization` dataclass is the single DR configuration: mass/inertia±5%,
sliding friction±15%, strength±15%, no-load/target speed±10%, damping±20%,
offsets±1°, uniform choice of1or2control ticks; gyro bias±.01rad/s, accel bias±.05m/s²,
noise gyro.006rad/s and accel.04m/s² with.8–1.2scale. These are hypotheses.
Nominal arrays are restored before each reset; inertia scales with body mass.
Fit real nominal response before broadening ranges. Record wear, voltage and
load effects; domains should represent measured variation rather than hide error.

The shared interface keeps privileged rewards/diagnostics out of policy inputs.
A calibrated measured model/control/calibration fingerprint must accompany every
policy, firmware build and physical trial. Changing geometry/mapping/filtering
invalidates prototypes. No real travel is estimated by double-integrating IMU.
See experiment/physical protocol and report template for equal trials/limits.

### Reproducible experiment protocol

#### Simulation

Current twin is provisional. Full measured-twin experiment requires the gates in
`docs/gates.json`, backed by linked evidence, not edited to true for convenience.
A development pilot can reveal software/control problems but cannot validate
Sim-to-Real. Never tune on the held-out final seeds.

- Smoke2048; nominal pilot<=50000 requested (49152complete1024step rollouts).
- Final per condition and training seed0,1,2<=1000000 (999424actual). An unchanged
  pilot counts toward its corresponding total; changed model/calibration is a new
  condition and the old result remains historical.
- A fixed nominal, B randomized; equal training budgets, matching initial weights.
  B never resumes A. `initial_policy_sha256` verifies the seed pairing.
- Validation2000–2004 in nominal AND randomized evaluation selects by total
  walking successes, then mean qualifying gait distance, then reward.
- Test1000–1009 is reserved for final reporting. Final comparison evaluates both
  trained conditions in both environment conditions, with home and seed-matched
  untrained policy baselines. Selection does not use final test results.
- Save complete per-episode CSV, aggregate means/falls/successes, condition/seeds,
  code/config/calibration hashes, model SHA, actual timesteps, TensorBoard and
  video. `tools/experiments.py` orchestrates the gated formal comparison.
- Every directory is immutable evidence: use a new output name for reruns.
  Checkpoint reload enforces file hash and configuration compatibility.
  Resume preserves timestep budget and prior validation winner. SB3 resume is
  not claimed bitwise identical to uninterrupted training: RNG/simulator rollout
  state is not fully checkpointed. Fresh runs have reproducible seeds.

Success requires a separate30s stand plus0.3m alternating lifted walking within
30s. Count full-foot lift>=3mm for>=40ms with opposite supported stance, forward
landings>=5mm, stance slip<=3mm, alternating sides,>=2steps each and>=3alternations.
Qualifying gait distance (half summed forward foot advances) and body distance
must each reach0.3m. SIM force checks are diagnostics, unavailable to the policy.
Contact onset may conservatively reject marginal steps; inspect video/trajectory
rather than relaxing acceptance after seeing results. Smoothness is not energy.

If the agreed cap fails, report the failure and mode (fall, standing, sliding,
insufficient lift or forward foot placement). Do not extend training automatically.
Turning, recovery and terrain are conditional extensions after walking works.

#### Human-assisted physical sequence

1. Clear delivered basket, helper job, rated connections and fit questions.
2. On bench: test enclosed PSU/physical disconnect, Pico USB, stationary IMU,
   one unloaded servo,3.3V PWM and boot/disarm/STOP/watchdog. Log actual timing.
3. Measure servo/shaft/horn/ear interfaces; approve one sample mounting interface
   before full frame. Include all sample and split-order deliveries in budget.
4. Fit pulse/sign/offset/range and response/current/latency; repeat six channels.
   Use known small weights/levers briefly; stop before stalls/heating. Measure
   loaded voltage and branch temperature, not only unloaded PSU output.
5. Assemble and weigh each body/component, record COM, sole friction and cable
   allocation. Review all clearances/wires/manual poses, then manual standing.
6. Replace physical parameters, version measured calibration/twin and rebuild
   firmware. Run checks/reference sequence. Invalidate incompatible prototypes.
7. Train/evaluate measured A/B. Confirm compatible hashes before limited physical
   standing, then progressively longer low-speed stepping on a low clear floor.
8. Use equal trial durations/floor/voltage/start pose/cable routing for A/B.
   Alternate order AB,BA,AB,BA to reduce wear/temperature/order bias. Begin with
   at least5paired attempts only after conservative supervised trials are safe.
   Record fall/stop reasons, unsuccessful trials and replacements, not successes only.
9. Measure distance with ruler/calibrated overhead/side video and observable foot
   landmarks; record frame rate/timebase and uncertainty. Never double-integrate
   cheap IMU acceleration into travelled distance. Record timestamped commands/
   IMU alongside video, identifying the exact policy/model/calibration hashes.
10. Compare SIM vs real and A vs B, including failed transfer, cable pull and
    protective-surface effects. Do not call different unequal conditions evidence
    that randomization caused an improvement.

Use `docs/templates/physical_trials.csv`; record total battery-free servo power
setup, cable routing and ambient conditions. A command/IMU log cannot prove a
3mm foot clearance or30cm travel: video/ruler evidence is required. The optional
safety line is slack and must not carry robot weight; no elaborate rig is required.

## 18. Remaining unknowns and risks

Delivered budget, sample fit, horns/screws, connector/branch ratings, servo current,
continuous torque, loaded speed/response/backlash,3.3V input, printed strength,
actual masses/COM, friction, IMU alignment/noise and tether forces remain unknown
or estimated. No compiler run proves electronics safety. PWM STOP is not power
isolation. Cheap position servos have no measured joint feedback or torque cap.
Finite sampled clearances do not prove all continuous paths. Current fastener
proxies cause unresolved conflicts and block manufacture. No physical hardware
or measured twin exists. Walking target remains unachieved unless actual recorded
metrics/video demonstrate otherwise. Standing alone or increasing reward is not
walking. Long formal training is blocked until fit/calibration/reference gates.

## 19. Exact build/test order and current checkpoint

### Hardware-first execution roadmap

Approved 2026-10-23. Preserve six joints and EUR 100 maximum delivered cost.
States and actual evidence belong in STATUS.md. No stage is physically verified without data.

| Stage / original phases | Work and owner | Completion gate |
|---|---|---|
| Entry / 0,13 | AI: concise AGENTS, STATUS and this roadmap; preserve historical evidence | New session can identify constraints, sources, blockers and next command quickly |
| A / 1 | AI: refresh exact parts, servo comparison, connector ratings and delivered print quote; no purchases/messages | Complete sourced basket <=EUR100, fit information or explicit unresolved evidence/shortfall |
| B / 1,2 | AI: reconcile CAD and physical ledger, PCB/case/frame clearance, fasteners; user/supplier: sample fit | Checked geometry; no unverified manufacturing release; solid masses remain estimates |
| C / 3,8 | AI: Pico SDK C++ firmware, PC bench/client, bounded protocol and persistent calibration | Firmware builds and host tests pass; actual electrical timing/cutoff still needs bench |
| D / 2,3,4,9 | AI: common limits/preprocessing, realistic command scheduling, reward and metrics; user: measured parameters | Reproducible twin; no fake stops/positive closed-loop progress/sliding success; measured vs provisional explicit |
| E / 5,6,7 | AI: bounded nominal pilot, equal-budget fixed/DR models, held-out evaluation and videos | Actual gait results, including failures, with fingerprints and complete per-episode metrics |
| F / 8,9,10,11,13 | User: bench, assembly, calibration and physical trials; AI: firmware/tools/data analysis/report | Real test data; frozen compatible policies; equal trials and alternating A/B order |
| Extensions / 12 | Future: turning, terrain, recovery | Stable baseline walking first; no automatic scope expansion |

#### Fixed engineering contracts

- Joint order L hip/knee/ankle, R hip/knee/ankle; +Y pitch, +X roll.
- Six normalized target-position actions; five 18-value observation frames.
- Observations use gravity estimated from IMU, gyro, applied targets and previous action.
- 50 Hz policy/commands; 200 Hz IMU; 2 ms physics. Real timer dt is recorded.
- Torque limits are simulation estimates, not programmable hardware torque protection.
- Persistent calibration supplies zero pulses, gains, signs, pulse/safe-angle limits and IMU alignment.
- Boot disarmed, explicit arm, 100 ms fresh-command watchdog, bounded CRC frames and STOP.
- Invalid calibration/config identity forbids policy operation; single-channel bench mode is explicit.

#### Experiment contract

- Smoke 2048 steps; pilot <=50000; final <=1000000 per A/B condition and seed 0,1,2.
- Round down to complete 1024-step rollouts. Unchanged pilot counts toward its final run.
- A nominal and B randomized start from matching initial weights and equal budgets.
- Validation seeds 2000–2004 select success, qualifying gait distance, then reward.
- Test seeds 1000–1009 are held out until final reporting; evaluate both conditions.
- Keep home and untrained baselines. Save CSV, summaries, model/config hashes and videos.
- Standing alone is not walking: retain 3 mm/40 ms lift, non-sliding forward touchdown,
  alternating support and >=0.3 m qualifying gait progress within 30 s without a fall.
- Initial success target also requires a separate 30 s stand test.
- If cap is reached without gait, report unmet target; do not extend automatically.

#### Human-dependent sequence

1. Resolve delivered budget and component interfaces before ordering.
2. Helper prepares short rated harness/headers; user checks cutoff, one servo and IMU.
3. Record pulse mapping, directions, range, speed/strength/current/latency and IMU noise.
4. Confirm one mounting sample, then finished frame; assemble and weigh bodies.
5. Validate all six joints, manual stand, watchdog, faults and cables.
6. Reconcile measured twin and configuration identity; retrain incompatible policies.
7. Policy stand, short steps, longer trials; use ruler/video, never IMU double integration.
8. Equal fixed/DR trials, alternating order, logs and failure records; school report.

When quotations or measurements block a stage, name the missing evidence and prepare
the precise question/data template. Continue independent software preparation. Do not
invent a quote or substitute simulation verification for physical verification.

### Current project status

Updated **2026-10-23**. **Nothing purchased, assembled, flashed or physically tested.**
Start with SUMMARY.md and AGENTS.md; use this file for evidence and ROADMAP.md for gates. Do not restart broad research.

#### Current checkpoint

Independent software preparation is implemented and locally checked. Hardware
feasibility, sample fit and calibration remain blocked. The twin is **provisional**,
not calibrated. Walking is **not achieved**. No formal measured A/B experiment or
physical transfer has taken place.

| Stage | State | Actual evidence / blocker |
|---|---|---|
| Requirements / entry | implemented | AGENTS.md, ROADMAP.md, this file; six joints and EUR100 maximum retained |
| A: hardware research | blocked | Refreshed procurement.json; known-priced subset EUR78.91, total unknown; exact print/fastener/input/shipping evidence missing |
| B: mechanics | implemented / blocked | Native-PWM revision removes PCA envelope; CAD/ledger agree at199.4g estimated;55poses yield550 unreviewed fastener-proxy overlaps, no manufacturing release |
| C: bench/interface | locally verified | C++ official Pico SDK2.3.1 build/UF2; Python host/bench/deployment, persistent compiled calibration, explicit arm/watchdog/CRC/fingerprints; no electrical test |
| D: twin/RL | locally verified provisional |29tests, compilation/mass/axes/inertias, Gym/SB3, clipped commands, discrete delay, corrected reward, gait exploit tests; measured response and lifted-step reference still missing |
| E: experiments | locally verified partial | A0 total49152steps; A/B0 paired2048smokes; validation2000–2004, CSV/aggregate/videos/checkpoints; zero walking; formal seeds0/1/2 blocked |
| F: physical/calibration/transfer | planned / blocked | No hardware; procedures, data templates, bench/deployment tools and report scaffold ready |
| Extensions | planned | Conditional on stable walking; not started |

#### Selected architecture and authoritative inputs

- Six Waveshare15024 MG90S, hip pitch/knee pitch/ankle roll per leg.
- Pico H **direct native PWM** GP0,1,2,3,6,7; MPU6050 GP4/5;50Hz commands/200Hz IMU.
  PCA9685 removed from current basket/spec because unavailable and extra mounting conflict.
- Wired5V/5A PSU with separate USB logic and common ground. Input/branch ratings and
  MG90S3.3V signal threshold remain unresolved. No programmable hardware torque cap.
- Basket/evidence: `procurement.json`, `docs/PROCUREMENT_ACTIONS.md`, `SERVO_COMPARISON.md`.
- Geometry/mass/dynamics/provenance: `physical_spec.json`; generated `robot.xml`,
  `docs/mass_properties.json`; editable `cad/build_frame.py` and assembly/quote brief.
- Shared policy contract: `robot_config.py`, `servo_control.py`, `imu_observation.py`.
- Calibration/identity: `calibration.py`, invalid example in `calibrations/`.
- Firmware/PC: `firmware/`, `serial_robot.py`, `bench.py`, `deploy.py`, `HARDWARE.md`.
- Training/evaluation: `train.py`, `evaluate.py`, `tools/experiments.py`, `EXPERIMENT.md`.

#### Locally verified results (not hardware evidence)

-29pytest tests passed;49installed Python packages pass dependency compatibility check.
- Seven generated CAD-frame masses match the ledger; every servo assigned once;
  aggregate inertias positive/physical. Six hinges/position actuators compile.
- Unknown mechanical stops removed from MJCF; safe command bounds remain enforced.
- Reward backward displacement fully charged; closed cycles gain no positive progress.
- Toe pivots, hops, in-place lifts, stance slip and stationary lifts followed by sliding
  fail synthetic gait tests; valid translating alternating steps are credited.
- Native C++ state machine tests cover disarmed startup, invalid calibration,
  corrupt/range/stale/replayed packets, queue delay, slew, PWM bounds and100ms watchdog.
- Default invalid example cannot policy-arm; deployment rejects it before opening USB.
- Model/calibration/file fingerprints checked on reload. A/B initial policy hashes match.
- A0 resumed2048→49152 (not49152extra). Checkpoint selected by success/gait/reward
  was at10240steps; validation success and qualifying distance were zero at every checkpoint.
- Selected A0, seeds2000–2004: nominal mean distance0.008577m, speed0.000286m/s,
  reward6.03602,30s,0/5falls,0walking; randomized mean0.008673m,reward6.03637,0walking.
- Home baseline also stands30s with essentially zero travel. Standing is not learning evidence.
- Matched2048step A/B smoke validation completed; not a final robustness comparison.
- Scripted46s stand/lean/lift attempts (including level-foot/reversed-lean variants)
  stood without falling but produced no sustained3mm whole-foot lifts. Reference gate stays false.
- Three30s640×48050fps videos exported; representative frames/assembly drawing inspected.

Evidence: `docs/VALIDATION_CURRENT.md` and `docs/validation/2026-10-23/` contain
source snapshots, hashes, CSV/JSON, models, TensorBoard, videos and invalid-calibration UF2.
Original2026-10-08 evidence under `docs/validation/` is historical and incompatible.
Final controller parsing was corrected to fixed-width64bit for uint32 timestamps.
Current controller hash is `3d93f768188c8c55c903658192be75b87124f9a62852720fb5d2fd5b54666a8a`.
Archived training hash is `1641779be26172bcb40bd2b94d93a0974f722a676ba6aa2249ec310a8dbf7a1f`;
all those policies are historical and intentionally rejected by current deployment/evaluation.
Review them with `tools/replay_snapshot.py`, which isolates the exact archived source.
This parser-only change leaves simulated dynamics unchanged, but no policies were silently
relabelled or granted physical compatibility. Current invalid-calibration UF2 is under
`docs/validation/2026-10-23/final_control_revision/`.

The superseded first smoke in `runs/2026-10-23/smoke` predates the final fingerprint;
`final_smoke` is also historical after the controller revision. Review archived policies
only through the isolated replay tool; no saved checkpoint is currently deployment-compatible.

#### Remaining blockers and unknown assumptions

1. **Procurement:** exact delivered print/finishing/sole/fastener quote, horn/screw contents,
   rated input connection, Funduino shipping, available FF jumpers and any helper charge.
   EUR21.09 remains for all unknowns. No exact shortfall is known; total is not established.
2. **Fit:** ear/shaft/spline/horn geometry and fastener sweeps unmeasured.550proxy overlaps
   are not550confirmed physical bolt collisions. Resolve actual hardware interfaces first.
3. **Physics:** servo sustainable torque/current, loaded response/latency/backlash, supply
   droop, actual printed masses/COM, friction and IMU bias/alignment are unmeasured.
  0.08Nm/gains/damping and conservative DR ranges remain explicitly estimated.
4. **Motion:** no validated manual lifted-step reference; both PPO pilot and reference
   attempts show no qualifying gait. Do not increase force or train millions to hide this.
5. **Hardware:** firmware has compiled, not run on a Pico. Watchdog/PWM/USB/IMU electrical
   timing, signal levels, cutoff, harness and real safety need physical bench verification.

#### Exact next task / executable checks

**Next human-dependent task:** resolve the four precise supplier/checkout questions in
`docs/PROCUREMENT_ACTIONS.md`; obtain a file-specific delivered fit/print quote. No messages
or purchases have been sent. Do not order a complete frame before servo/horn sample fit.

**Next software command:**

```bash
.venv/bin/python -m pytest -q
.venv/bin/python tools/budget_gate.py # expected exit2, incomplete
.venv/bin/python tools/check_clearance.py # expected exit1, proxy conflicts
```

Then use received dimensions/quotes to replace unknowns; helper/user performs the one-servo
bench and IMU measurements in CALIBRATION.md. Provisional independent tooling is prepared;
formal training and physical completion remain blocked by `docs/gates.json`. Do not set a
gate true without linked evidence. Generated full reference: `docs/HANDOFF.md`.

### Local verification record —2026-10-23

Everything below is **locally executed software/compiler/simulation**, never a
physical result. No procurement, manufacturing, electrical timing or robot trial
was completed. Historical record: VALIDATION.md; current artifacts: validation/2026-10-23/.

#### Checks

- `python -m pytest -q`:29passed (8.49s in recorded run).
- `UV_CACHE_DIR=/tmp/robot-uv-cache uv pip check --python .venv/bin/python`:
 49packages, compatible. Python3.12.3; exact top-level pins in requirements files.
- Seven CAD meshes have ledger-matching solid-PETG masses; total199.431g estimated.
  Aggregate inertia tensors positive and satisfy principal-inertia triangle inequalities.
- MJCF compilation, axes, servo ownership, reset contacts,30s neutral standing,
  randomized/limit command finiteness, Gym/SB3 semantics, seeded reset restoration pass.
- Five-frame90value observations use only estimated gravity/raw gyro/applied command
  and previous action. Privileged-state mutation does not change assembled observations.
- Delay samples reach both20/40ms; masses and inertias restore and scale together.
  PWM1µs safe rounding and measured-gain arithmetic tested with synthetic calibration.
- Progress reward regression: closed motion cycles cannot gain positive progress;
  backward motion is fully charged. Synthetic false-gait cases fail acceptance.
- Host framing/CRC/handshake/stale telemetry and native C++ controller tests pass.
  Native C++ tests with synthetically valid calibration remain test-only, never flashed.
- Official Pico SDK2.3.1 / Arm GNU14.2.Rel1 builds firmware ELF/bin. Official picotool
 2.3.1 converts UF2. Saved `final_control_revision/bench_invalid.uf2` **cannot policy-arm**; no flashing tested.
- Formal training/experiment commands reject all five uncleared gates. Invalid-calibration
  deployment fails before opening the requested serial port. No automatic arming occurs.

Expanded finite clearance command exited1 as intended:550fastener-proxy intersections
across55poses, zero non-fastener frame/case/electronics conflicts in those samples.
These are conservative unmeasured fastener mass-envelope proxies, not actual bolt models.
Manufacturing remains blocked. The previous checker silently omitted these categories.
Continuous sweeps, horns/ears/lead exits and assembly stiffness still need actual fit.

#### Bounded training

| Run | Actual steps | Initialization / role |
|---|---:|---|
| final_smoke A0 |2048|Fresh seed0, current configuration|
| pilot_A0 |49152total|Resumes A0;2048included; rounds50000down; selected checkpoint10240|
| smoke_B0 |2048|Fresh randomized seed0, identical initial weights to A0|

Initial policy hash for both conditions:
`7efc1058e8b776f6de8d40b9d9359d2ce96bbefff09272d15dc673690ce166d9`.
Archived training configuration hash:
`1641779be26172bcb40bd2b94d93a0974f722a676ba6aa2249ec310a8dbf7a1f`.
The final ARM timestamp parser fix changes current controller identity to
`3d93f768188c8c55c903658192be75b87124f9a62852720fb5d2fd5b54666a8a`.
Archived policies are deliberately incompatible with the current controller; no
automatic migration/override was added. Exact-source isolated replay was locally
executed (seed2000:0.0085637m,30s,no fall,no gait). Current firmware was rebuilt;
model physics/preprocessing are unchanged. New training is required for a current
identity policy, and measured calibration remains required before deployment.

Manifests include model hashes, actual steps, source hashes, full randomization and
algorithm settings. TensorBoard/events and monitor CSVs are retained. Resume reload
worked; exact interrupted-vs-uninterrupted RNG equivalence is not claimed.

All validation checkpoints scored zero walking successes and zero gait distance.
Selection used seeds2000–2004 only.1000–1009 remains reserved for the future final
experiment. No formal six-run A/B comparison was started and no extra budget authorized.
The intermediate `runs/.../smoke` predates a source revision and is not a current model.

#### Five validation episodes per row, seeds2000–2004

| Policy / environment | Mean body distance m | Mean reward | Falls | Qualifying gait m / success |
|---|---:|---:|---:|---|
| Home / nominal |0.0000271|6.00001|0/5|0 /0of5|
| Untrained / nominal |−0.025824|5.08423|0/5|0 /0of5|
|2048 A / nominal |−0.019874|5.46253|0/5|0 /0of5|
|2048 B / nominal |−0.020396|5.37745|0/5|0 /0of5|
| Selected A pilot / nominal |0.008577|6.03602|0/5|0 /0of5|
| Selected A pilot / randomized |0.008673|6.03637|0/5|0 /0of5|

All episodes lasted30s. Complete nominal/randomized rows for all policies are in
`validation/2026-10-23/aggregate.csv` and each experiment's episodes.csv/summary.json.
This shows stationary/sliding drift, **not walking**. The longer nominal pilot must
not be compared with the shorter B smoke as a claim about randomization efficacy.

Scripted reference variants completed46s including30s standing, but whole-foot
clearance stayed far below3mm; zero qualified steps. Counter-rotating hip/knee
keeps the intended foot pitch level kinematically, but did not produce a supported
lift dynamically; reversing the lean sign also failed. Joint trajectories, targets,
clearances and failures are saved rather than declaring the reference gate passed.
No force gains or torque cap were increased to force success.

Three MP4s (pilot nominal/randomized, B-smoke randomized) are30s,640×480,50fps,H264.
Representative rendered frames and updated exploded assembly envelopes were visually
inspected. The image/video shows posture, not independent evidence of successful gait.

#### Reproduce/review

```bash
python -m pytest -q
python tools/replay_snapshot.py --episodes 5 --output runs/review_archived
### New current-identity smoke, only when a fresh development run is desired:
python train.py --steps 2048 --development --output runs/new_current_smoke
```

Use new output directories. Source snapshots include the visual STLs; the replay tool runs them in an
isolated temporary directory and never grants current hardware compatibility. `manifest.json` hashes evidence files. The source archive excludes
credentials, hidden agent configuration, virtualenvs, toolchains and run scratch.
Next evidence needed is the delivered quote/interface sample and real bench data;
no software check can mark those physically verified.
