# S6 robot — short plan for you and the AI

Updated **2026-10-23**. Costs/evidence: [procurement.json](procurement.json). **Nothing ordered or physically tested.**

## Decision and current state

Keep six MG90S: hip pitch, knee pitch and ankle roll per leg; roughly 18 cm, PC inference, USB and wired 5 V power. **You can solder; no helper fee is required.** No printer access is assumed. Printer purchase is comparison only. No drilling/cutting/bending of frame parts; cutting/stripping electrical wire is part of soldering.

| Frame route | Robot-parts priced subset, VAT + published delivery | Complete delivered price | Decision |
|---|---:|---|---|
| Standard parts, no fabrication | **€95.91 before frame/its hardware/delivery** | Unknown | No complete compatible six-joint kit verified; blocked |
| Own printer: seven PETG parts + standard pads | **€118.43 before unresolved extras** | Unknown; already **€18.43 over €100** | Comparison only; no printer access or print release |

**Recommendation:** use the proposed bare Pico and self-soldered harness if bench tests pass. Neither frame route is cleared to buy. Buying a printer does not solve the robot budget. Seek an exact compatible standard frame offer; keep local printing as a comparison until access, fit and costs are resolved. Commercial printing/laser cutting are historical alternatives, not default orders.

Software: simulation, firmware and bench tools exist; **32 tests passed in this update**. Historical49,152-step PPO pilot **did not walk**. Current model still represents **Pico H + continuous1mm TPU soles**, estimated199.4g; the bare Pico/pad revision is proposed, not silently installed in MuJoCo. [Status/evidence](docs/STATUS.md).

## Common purchase list — proposed, not cleared

Quantities are **full packs/items to buy**, not just quantities consumed. Prices include VAT; delivery is below. Existing PC and soldering-iron access assumed.

| Item / exact source | Buy qty | Unit € | Line € | Purpose / issue |
|---|---:|---:|---:|---|
| [MG90S Waveshare15024](https://www.welectron.com/Waveshare-15024-MG90S-Servo_1) — Welectron | 6 | 3.50 | 21.00 | Joint servo; actual horns/retainers unconfirmed |
| [Bare Pico](https://www.berrybase.de/raspberry-pi-pico-rp2040-mikrocontroller-board) — BerryBase | 1 | 4.10 | 4.10 | USB controller; solder headers |
| [MPU6050 F23107397](https://funduino.com/products/mpu-6050-modul-triaxial-beschleunigungssensor-gyroskop) — Funduino | 1 | 3.62 | 3.62 | Balance sensor |
| [GST40A05-P1J](https://www.berrybase.de/meanwell-schaltnetzteil-5v-dc-5-0a-mit-hohlstecker-5-5x2-1mm) — BerryBase | 1 | 15.50 | 15.50 | Enclosed 5V/5A servo PSU |
| [Goobay68604, 1.5m](https://www.berrybase.de/kaltgeraete-netzkabel-schutzkontakt-stecker-abgewinkelt-iec320-c13-buchse-schwarz) — BerryBase | 1 | 3.81 | 3.81 | Mains lead for PSU |
| [RPI-MUSB-1, 1m](https://www.berrybase.de/offizielles-raspberry-pi-micro-usb-kabel-rot-1-0m) — BerryBase | 1 | 1.80 | 1.80 | USB-A–Micro-B data cable; no adapter |
| [DUPK-40-FF-50, 40 leads](https://www.berrybase.de/40pin-jumper-dupont-kabel-female-female-trennbar/laenge-0-50-m) — BerryBase | 1 | 2.20 | 2.20 | Logic wiring only; shorten I2C |
| [JR/Futaba F23108007, 10cm](https://funduino.com/products/jr-futaba-servo-verlangerung-kabel-10cm-female-male) — Funduino | 6 | 1.14 | 6.84 | Six replaceable servo connections; ratings pending |
| [Donau E-175-10 red copper wire 0.75 mm², 10 m roll](https://www.berrybase.de/donau-kupferschaltlitze-0-75-mm2-10m-lang-1-adrig-24x0-20mm-pvc-isoliert) — BerryBase | 1 | 5.90 | 5.90 | Short <=10 cm power buses; label negative with black shrink; no long thin power tether |
| [AiSHi ELK1M16VAWH 1000 µF 16 V capacitor](https://www.berrybase.de/elektrolytkondensator-1000-f-16v-1050c-1-radial-tht) — BerryBase | 1 | 0.29 | 0.29 | Polarity matters; actual tolerance ±20%, inconsistent page title ignored |
| [PINH-1X40P 40-pin 2.54 mm header](https://www.berrybase.de/stiftleiste-1x-40-polig-rm-2-54-gerade) — BerryBase | 2 | 0.60 | 1.20 | Two full 40-pin packs: 40 Pico pins + up to 8 IMU + 6 individual signal pins = 54, 26 spare |
| [McPower T1535561 heat-shrink, 100 pieces](https://www.berrybase.de/schrumpfschlauch-set-100-teilig-schwarz) — BerryBase | 1 | 1.90 | 1.90 | Insulation for soldered joints; mark negative polarity |
| [McPower T1535501 cable ties, 100 x 2.5 mm, pack of 100](https://www.berrybase.de/kabelbinder-uv-bestaendig-nylon-100-stueck/farbe-transparent/masse-100x2-5mm) — BerryBase | 1 | 0.45 | 0.45 | 8 board mounts, 4 cable strain relief, 8 harness restraints; keep away from pinch points |
| [Goobay 11638 DC socket 5.5 x 2.1 mm, solder lugs, 5 A](https://www.berrybase.de/dc-einbaubuchse-fuer-hohlstecker-5-5x2-1mm-metallausfuehrung-loetanschluss) — BerryBase | 1 | 1.10 | 1.10 | Retailer specifies 5 A / 30 V DC, nut and washer |
| [Zhongdi ZD-160 lead-free solder, 1 mm, 2% flux, 10 g](https://www.berrybase.de/zhongdi-loetzinn-bleifrei-oe1-0-mm-2-flussmittel-10-g) — BerryBase | 1 | 1.90 | 1.90 | Flux-core solder for headers and harness |
| [Delock 18309 self-adhesive TPE pads, 10 x 3 mm, pack50](https://www.reichelt.de/de/de/shop/produkt/gummifuesse_rund_selbstklebend_10_x_3_mm_50_stk_schwarz-371081) — Reichelt | 1 | 3.55 | 3.55 | Candidate: 8 used (4 per foot), 42 spare |

Two 40-pin header packs provide 80 pins: 40 Pico + up to 8 IMU + 6 signal ends = 54, 26 spare. Bare Pico+headers€5.30 versus Pico H+one header pack€6.10: **saving€0.80**, not€1.40. Same firmware/pin assignments.

## Additional frame parts and unresolved hardware

- **Standard route:** one complete frame kit is required: torso,2thighs,2shins,2feet, all case/horn/link interfaces and matching fasteners. No verified product/quantity/landed price yet. [Cytron ROBO-BK-SG90](https://www.cytron.io/p-robo-bracket-for-microservo-motor), USD2.48 each, is only a case bracket; its included4M2×6+4M3×6 screws do not create a complete leg. Required bracket count remains unknown. Four-joint kits are unsuitable.
- **Own-print route:** [SUNLU PETG black SN5-314224,1kg spool](https://www.welectron.com/Sunlu-PETG-Black-175-mm-1000-g_1),1×€12.99; seven frame parts:1torso+2thighs+2shins+2feet. Full spool counted; supplied sample filament is not relied on.
- Ear fasteners, own-print route: buy100each of [M2×8 screws](https://www.schraubenking-shop.de/M2-x-8mm-Linsenkopfschrauben-PH-DIN7985-Stahl-verzinkt-FKL48-P010265) €1.51, [M2 nuts](https://www.schraubenking-shop.de/M2-Sechskantmuttern-DIN934-Stahl-verzinkt-FKL8-P003474) €1.13 and [M2 washers](https://www.schraubenking-shop.de/22mm-Unterlegscheiben-DIN125-Edelstahl-A2-P004198) €0.99. Install12screws/12nuts/24washers; length/clearance still unverified. Delivery€5.90.
- **Six matching horns + six shaft screws** required; accessory photo is not batch confirmation. **Twelve horn-to-frame screws +12matching washers** also required for the current CAD; exact thread/length and cost unknown. Do not order generic25T horns or guess centre-screw threads. A standard kit must include/price its own verified hardware.
- Candidate grip: use8Delock18309 pads (4perfoot),42spare in the50pack above.10mm diameter×3mm,TPE, self-adhesive. No TPU spool or separately bonded sole is proposed. Grip/adhesion and final placement need testing; changing from continuous soles requires new contact geometry/fingerprint later.
- Print-specific cleaning/release consumables and any additional fit hardware remain unpriced until the actual printer/plate/slicer is verified. Unknowns are **not zero**.

## Cost and delivery breakdown

| Supplier / contents | Parts € | Shipping € | Known € |
|---|---:|---:|---:|
| Welectron:6servos |21.00|4.95|25.95|
| BerryBase:bare Pico,PSU,mains/USB,wire,headers,solder,insulation,restraints,DC socket |40.15|4.95|45.10|
| Funduino:IMU+6extensions |10.46|4.90|15.36|
| Reichelt:50grip pads |3.55|5.95|9.50|
| **Common subset; no complete frame** |**75.16**|**20.75**|**95.91**|
| Own print adds:full PETG spool +3fastener packs |16.62|5.90|22.52|
| **Own-print robot subset** |**91.78**|**26.65**|**118.43**|

Delivery to **25337 Germany**: published standard rates, not a postcode-specific checkout/booking. Stock is not reserved; six-servo availability still needs confirmation. BerryBase/Welectron typically1–3working days for shown stock; Funduino/fastener/pad timing must be checked at checkout. Extra bench/sample shipments cost extra. [Policies and precise questions](docs/PROCUREMENT_ACTIONS.md).

| Printer comparison only | Printer incl.VAT + published DE delivery | Robot subset | Initial cash priced subset |
|---|---:|---:|---:|
| [Bambu A1 mini non-Combo BL1-101030](https://www.welectron.com/Bambu-Lab-A1-mini-3D-Drucker) |€189+€0|€118.43|**€307.43 + unknowns**|
| [Creality Ender-3 V3 SE standalone](https://store.creality.com/de/products/ender-3-v3-se-3d-drucker) |€169+€0|€118.43|**€287.43 + unknowns**|

A1mini: exact variant shown in stock,1–3working days;180³mm. Ender: standalone add-to-cart enabled, no stock count;220×220×250mm. Free German shipping is published policy, not confirmed25337 checkout. No discounts assumed. Joint A1/servo/spool shipment could remove€4.95 **once** if verified; even then robot subset€113.48 remains over cap. The table conservatively retains robot-only delivery.

**Tools:** iron access already available. Borrow/confirm meter, stripper/cutters, safe heat source, scale/ruler and print/support tools; unconfirmed tool purchases make the complete initial cash total unknown. Tools/printer are outside€100; solder, insulation, filament and connectors are inside it. Optional spare servo/protective mat/slack safety line are not base purchases.

## Assembly — conditional on budget, fit and electrical approval

1. **Confirm mechanics first:** exact servo ear/horn dimensions, full screw stack, link directions, cable/fastener clearance and complete delivery price. Standard route has no verified assembly kit yet; do not buy six brackets and assume legs follow.
2. **Solder and test electronics:** fit40Pico pins and IMU header; build6replaceable servo branches onto short0.75mm² positive/return buses. Insulate every joint, add1000µF capacitor and soldered5A DC socket; label polarity and strain-relieve. USB powers Pico/IMU; servo current bypasses Pico/breadboards. [Detailed harness/pins](docs/HARDWARE.md).
3. **Bench one unloaded servo +IMU:** verify polarity/current/droop,3.3V signal, physical DC unplug cutoff, disarmed boot/watchdog and single-channel calibration. PWM pins GP0/1/2/3/6/7; IMU GP4/5. [Firmware/commands](firmware/README.md), [measurements](docs/CALIBRATION.md).
4. **If printing is later selected:** measure interfaces, slice/print [FIRST_interface_sample.stl](cad/local_print/FIRST_interface_sample.stl) before the seven frames. Open one [individual plate](cad/local_print/layout.json) at100%/mm: all fit180mm bounding boxes with margin. The old185mm quote batch does **not** fit. Orientations/supports/strength are not approved. [Route details](docs/FRAME_ROUTES.md).
5. **Build measured frame:** calibrate zero; power off before fitting matching horns/retainers. Cases:hips→torso,knees→thighs,ankles→feet. Moving horn links:thigh→hip,shin→knee and ankle. Fit only verified fasteners; do not drill/force parts. [Prototype drawing](cad/exploded.png), [assembly reference](cad/ASSEMBLY.md). Standard kit needs its own verified equivalent sequence.
6. **Fit pads/boards, route and weigh:** candidate4pads perfoot; rigid IMU mount, insulated boards, joint service loops, tether strain relief near torso. Check all angles/collisions; record body masses/COM and new sole geometry before updating twin. Test small manual motions and reachable physical cutoff. Software STOP does not isolate power.

## Project sequence and AI continuation

| Next stage | You | AI / done criterion |
|---|---|---|
| **Now: feasibility** | Obtain exact standard-frame offer/measurements; no order yet | Price every interface/hardware/delivery; cap≤€100, otherwise remain blocked |
| Bench +sample | Solder/test, measure servo/horn/current/response/IMU; sample only with access | Store measured calibration; resolve clearance proxies; no physical claims from simulation |
| Assembly +twin | Assemble/weigh approved mechanics | Update spec,mass,inertia,transforms,contacts; generate new identity; invalidate prototype policies |
| Manual motion | Supply standing/weight-transfer/step data | Validate lifted steps before more large training; do not inflate torque |
| RL A/B | Review videos | Matched initial weights, equal budgets,seeds0/1/2;≤999424steps each; validation2000–2004,test1000–1009 |
| Transfer +report | Supervised stand, short walks, equal A/B trials with ruler/video | Fingerprints/logs, compare distance/speed/falls; never IMU double-integration distance |

Target:30s standing,then≥0.3m visibly alternating lifted walking within30s; sliding does not count. Extensions wait.

**AI:** read this → [AGENTS](AGENTS.md) → [STATUS](docs/STATUS.md) → relevant [ROADMAP](docs/ROADMAP.md). Keep [gates](docs/gates.json) false. Next task is a complete standard-frame interface/landed-cost proposal, not another commercial-print quote or training run. Local print route fails budget already. Physical spec/MJCF/control are unchanged; all saved policies remain historical. Evidence must say sourced/estimated/measured/unknown. Regenerate handoff/archive after changes; preserve historical quotes and experiments.

```bash
.venv/bin/python -m pytest -q
.venv/bin/python tools/budget_gate.py --scenario all  # exit1: own-print over cap
.venv/bin/python tools/prepare_local_print.py        # provisional layouts only
.venv/bin/python tools/check_clearance.py            # exit1: unresolved proxy overlaps
```
