# S6 robot — short plan for you and the AI

Updated **2026-10-26**. Costs:[procurement.json](procurement.json). Physical inputs:[physical_spec.json](physical_spec.json). **Design/printing arrangement accepted by you; physical fit/tests not yet reported.**

**Design and printing-selection phase: COMPLETE by your confirmation (2026-10-26).**
Your classmate will print the parts; exact price/transport remain unknown, not zero.
Controller is now **Raspberry Pi Pico 2 (bare RP2350, not W)**. No printer purchase.

**Send your classmate this [separate print folder](print_for_classmate/00_START_HERE.md)
or [print-only ZIP](print_for_classmate.zip):** two fit pieces first; then seven
frame parts, each1× after fit. German instructions, STL dimensions/hashes and drawings
are included. No combined duplicate plate, printed horns or TPU soles.

**WP2 software locally verified:** manual six-joint previews/control and measured
HOME/untrained evaluation calibration parity and Pico2 build implemented;121tests pass. Hardware
operation remains untested. **Ordering started—reported by you**; exact items,
quantities, paid prices and arrival states remain unknown until you supply them.
Root [PLAN.md](PLAN.md) is the full living plan and is updated after each work chunk.

**[Detailed development plan](PLAN.md):** diagnosis → affordable
complete basket → bench/sample fit → measured twin → fixed/DR training → real trials.
Each stage identifies its owner, affected files, blockers and completion evidence.
The expanded plan maps all14phases, eleven work packages, the exact next five
tasks, release evidence and failure decisions; [start with the next tasks](PLAN.md#3-dependency-map-and-next-five-tasks).

## What you receive

- **[Fit-sample ZIP](cad/sample_quotation_package.zip):2 test pieces**, servo cradle and horn plate.
- **[Full-frame quotation ZIP](cad/frame_quotation_package.zip):7 PETG parts**, one torso+two thighs+two shins+two feet. No printed soles.
- [Dimensioned interface drawing](cad/print_order/drawings/interfaces.png), [exploded assembly](cad/exploded.png), [fastener schedule](cad/print_order/fasteners.csv), [supplier brief](cad/QUOTE_REQUEST.md), [assembly instructions](cad/ASSEMBLY.md).
- Matching provisional **MuJoCo r2 model**, bare Pico 2+headers, eight ordinary grip pads; about **197.1 g estimated**. No printer/spool purchase; you solder the harness yourself.

**Quotation prototypes, not approved order files.** The actual horn/ear/screw fit and layer strength are unknown. First confirm the complete budget and measure an actual servo, then test the sample before the full frame. All quantities/hashes are in each ZIP manifest; do not order combined and individual files together. Forward only the sample/frame quotation ZIP, **not the complete project archive**, which also contains historical geometry.

## Cost record — selected arrangement accepted, exact total pending

All prices are VAT-inclusive dated source snapshots, quantities are full packs. Existing PC/iron access assumed. Delivery to **25337, Germany**; PC USB-A confirmed, no adapter.

| Exact item / supplier | Buy qty | Unit € | Line € | Purpose |
|---|---:|---:|---:|---|
| [Waveshare15024 MG90S](https://www.welectron.com/Waveshare-15024-MG90S-Servo_1) — Welectron | 6 | 3.50 | 21.00 | Joint motor;6-unit stock/accessories pending |
| [Bare Pico 2](https://www.berrybase.de/raspberry-pi-pico-2-rp2350-mikrocontroller-board) — BerryBase | 1 | 5.50 | 5.50 | USB controller; solder headers |
| [MPU6050 F23107397](https://funduino.com/products/mpu-6050-modul-triaxial-beschleunigungssensor-gyroskop) — Funduino | 1 | 3.62 | 3.62 | Body accelerometer/gyro |
| [Mean Well GST40A05-P1J](https://www.berrybase.de/meanwell-schaltnetzteil-5v-dc-5-0a-mit-hohlstecker-5-5x2-1mm) — BerryBase | 1 | 15.50 | 15.50 | Enclosed5V/5A servo PSU |
| [Goobay68604 mains lead](https://www.berrybase.de/kaltgeraete-netzkabel-schutzkontakt-stecker-abgewinkelt-iec320-c13-buchse-schwarz) — BerryBase | 1 | 3.81 | 3.81 | Schuko–C13 for PSU |
| [RPI-MUSB-1 USB cable](https://www.berrybase.de/offizielles-raspberry-pi-micro-usb-kabel-rot-1-0m) — BerryBase | 1 | 1.80 | 1.80 | USB-A–Micro-B data; no adapter |
| [DUPK-40-FF-50,40leads](https://www.berrybase.de/40pin-jumper-dupont-kabel-female-female-trennbar/laenge-0-50-m) — BerryBase | 1 | 2.20 | 2.20 | Logic only; shorten I2C |
| [JR/Futaba F23108007,10cm](https://funduino.com/products/jr-futaba-servo-verlangerung-kabel-10cm-female-male) — Funduino | 6 | 1.14 | 6.84 | Replaceable servo branches;ratings pending |
| [Donau E-175-11 black,10m roll](https://www.berrybase.de/donau-kupferschaltlitze-0-75-mm2-10m-lang-1-adrig-24x0-20mm-pvc-isoliert/farbe-schwarz) — BerryBase | 1 | 5.50 | 5.50 | 0.75mm² buses; mark polarity at every end |
| [AiSHi1000µF/16V](https://www.berrybase.de/elektrolytkondensator-1000-f-16v-1050c-1-radial-tht) — BerryBase | 1 | 0.29 | 0.29 | Bulk bus capacitor;polarity matters |
| [PINH-1X40P,40pins](https://www.berrybase.de/stiftleiste-1x-40-polig-rm-2-54-gerade) — BerryBase | 1 | 0.60 | 0.60 | IMU/signal ends |
| [T1535561 shrink,100pieces](https://www.berrybase.de/schrumpfschlauch-set-100-teilig-schwarz) — BerryBase | 1 | 1.90 | 1.90 | Solder insulation |
| [T1535501 ties,100pack](https://www.berrybase.de/kabelbinder-uv-bestaendig-nylon-100-stueck/farbe-transparent/masse-100x2-5mm) — BerryBase | 1 | 0.60 | 0.60 | Board/wire/tether restraints |
| [Goobay11638 DC socket](https://www.berrybase.de/dc-einbaubuchse-fuer-hohlstecker-5-5x2-1mm-metallausfuehrung-loetanschluss) — BerryBase | 1 | 1.10 | 1.10 | 5A5.5×2.1mm input; accessible unplug |
| [ZD-160 flux-core solder,10g](https://www.berrybase.de/zhongdi-loetzinn-bleifrei-oe1-0-mm-2-flussmittel-10-g) — BerryBase | 1 | 1.90 | 1.90 | Soldering consumable |
| [Delock18309 pads,50pack](https://www.reichelt.de/de/de/shop/produkt/gummifuesse_rund_selbstklebend_10_x_3_mm_50_stk_schwarz-371081) — Reichelt | 1 | 3.55 | 3.55 | 8used;10mm diameter×3mm,adhesive included |
| [RPIP-PINH Pico headers](https://www.berrybase.de/stiftleisten-pin-header-set-fuer-raspberry-pi-pico) — BerryBase | 1 | 0.50 | 0.50 | 2×20pins +spare3pin debug strip |

Frame ear hardware: buy100each of [M2×8 P010265](https://www.schraubenking-shop.de/M2-x-8mm-Linsenkopfschrauben-PH-DIN7985-Stahl-verzinkt-FKL48-P010265)€1.51, [M2nuts P003474](https://www.schraubenking-shop.de/M2-Sechskantmuttern-DIN934-Stahl-verzinkt-FKL8-P003474)€1.13 and [M2washers P004198](https://www.schraubenking-shop.de/22mm-Unterlegscheiben-DIN125-Edelstahl-A2-P004198)€0.99; install12screws+12nuts+24washers. Length/stack still provisional.

**Required, unpriced:**6matching factory horns+6shaft retainers (possibly supplied, unconfirmed);12horn-to-frame screws+12matching washers; seven finished PETG prints; two fit-sample prints; every print/sample delivery and finishing/inspection charge. Never guess horn splines/threads or count unknown costs as zero.

| Supplier / contents | Parts € | Shipping € | Priced subtotal € |
|---|---:|---:|---:|
| Welectron:6servos |21.00|4.95|25.95|
| BerryBase:controller,power,wiring,solder,headers |41.20|4.95|46.15|
| Funduino:IMU+6extensions |10.46|4.90|15.36|
| Reichelt:50pads |3.55|5.95|9.50|
| Schraubenking:3fastener packs |3.63|5.90|9.53|
| **Priced basket BEFORE printing/sample/horn extras** |**79.84**|**26.65**|**106.49**|
| **Known shortfall against€100 for this basket** |||**6.49**|
| **Complete delivered total** |||**Unknown**|

Selected Pico2 replaces€4.10 Pico with€5.50 board (+€1.40); header kit remains.
Other prices retain their2026-10-25 snapshot, not a new checkout. The subtotal is
€106.49 before unknown printing/horn extras. **Your acceptance closes the design/
provider decision; it does not assert an audited≤€100 total.** No new delivery or
printing price has been invented. Old supplier comparisons remain historical.
Classmate printing is selected by you; no Meltlab upload is needed for this route.

Tools: iron access confirmed; borrow/confirm meter, stripper/cutters, safe shrink heat source, scale, ruler/protractor and screw tools. Unconfirmed tool purchases remain unknown initial cash, outside the€100parts cap. Optional spare servo/protective mat/slack line are not base purchases.

## Assembly — after budget and physical-fit approval

1. **Measure and test sample:** exact servo ears/shaft/horn/screws; test the2sample pieces without forcing or drilling. Failed fit means revise/re-quote before the7frames.
2. **Solder bench electronics:** bare Pico 2 headers, IMU and6replaceable servo branches onto insulated0.75mm² buses; capacitor/DC socket and strain relief. USB powers logic, PSU powers servos, common ground. [Wiring](docs/HARDWARE.md), [firmware/bench](firmware/README.md).
3. **Test one unloaded servo/IMU:** polarity/current/droop,3.3V signal, physical DC disconnect, disarmed boot and100ms watchdog. Calibrate zero before fitting horns; HOME is not mechanical zero.
4. **Assemble legs:** cases—hip→torso,knee→thigh,ankle→foot. Horn connections—thigh→hip,shin→knee and ankle. Use only confirmed hardware; check screw/tool/wire sweeps. [Drawing/steps](cad/ASSEMBLY.md).
5. **Mount boards/pads:** insulating stand-offs, rigid IMU, safe ties; four pads per foot at drawing coordinates. Inspect11mm Pico pin envelope and connectors. Leave joint wire loops and externally supported tether.
6. **Weigh and calibrate:** each rigid body/installed component once; record COM,servo response/range/latency/current and pad friction. Update twin/fingerprint; test manual stand before policies. STOP is not physical power isolation.

## Simulation and project sequence

| Stage | Verified now / next |
|---|---|
| CAD/print package | Implemented;latest suite121passes,55 sampled poses have0 modeled collisions; **5 unknown interface groups still block manufacture** |
| MuJoCo | Compiles; matching pad geometry/mass ownership;30 s neutral standing. Estimated masses/strength/friction, not calibrated |
| Motion | Frozen script: **four qualifying alternating steps**,6.60cm torso advance/30s; **30cm target still fails**. Corrected29-case study: all12 individual±1° offsets lose steps;73credited steps independently checked |
| PPO | Historical2048-step smoke/reload/evaluation:0 walking successes,0 gait distance. All saved policies now incompatible after offset-model correction; no extra training |
| Accepted phase | Design/printing choice complete by user; numerical costs still open. Physical fit, strength and calibration remain unverified |
| Later | Measured twin → manual lifted-step verification → bounded fixed/DR A/B training → supervised physical stand/steps → equal real trials/report |

Success remains 30 s standing followed by≥0.3m visibly alternating lifted walking within 30 s; sliding is not walking. Larger training stays blocked. Physical stage data must come from you; no simulation result clears it. [Neutral video](docs/validation/2026-10-24/print_revision/final/home_clean_video/episode_0.mp4), [smoke video](docs/validation/2026-10-24/print_revision/final/smoke_clean_video/episode_0.mp4), [latest evidence](docs/VALIDATION_CURRENT.md), [status](docs/STATUS.md), [roadmap](docs/ROADMAP.md).

## AI entry and exact next action

Read this → [AGENTS](AGENTS.md) → relevant status/roadmap. Active route is outsourced PETG, not printer purchase or stock-frame research. Preserve history and all policies; never relabel fingerprints. [Offset correction/sensitivity](docs/SENSITIVITY.md): Pico2 identity begins`685e3802`; nominal motion unchanged, calibration errors no longer disappear at command bounds. **All saved policies are historical/incompatible.** Current preparation ELF/UF2 is locally cross-built with invalid calibration; older UF2 is historical. No physical test or policy deployment approval.

**Next human action (printing route agreed):** share the print-only folder with your classmate, test the
2sample pieces on actual servo/horn/screws, then print7frames if they fit. Record
actual cost and weigh parts when available. The price decision is accepted;
physical fit and calibration are not claimed. [Full reference](docs/HANDOFF.md).

**Pico2 firmware:** locally cross-built; [build/evidence](firmware/README.md). No USB/flash/arm.
**Next AI work:** validate real order/arrival and fit/bench records when supplied; no PPO.
[Manual tool](docs/MANUAL_CONTROL.md) defaults to offline preview; measured validated
calibration is required for explicit hardware operation. [Data intake](docs/MEASUREMENT_INTAKE.md).
The model/control identity is unchanged; new source-only reference preserves prior
snapshots and exact nominal metrics. Update PLAN after each task/change.

```bash
.venv/bin/python -m pytest -q tests # scoped to active tests, not history copies
.venv/bin/python tools/budget_gate.py # expected1:106.49before prints
MPLCONFIGDIR=/tmp/s6-mpl .venv/bin/python tools/prepare_print_order.py
.venv/bin/python tools/check_clearance.py # expected1:unknown interfaces
```

Historical comparison tool (not a selected route): `.venv/bin/python tools/compare_procurement.py --option berrybase_round_pads`
(exit2, incomplete/unselected; never purchase approval).
