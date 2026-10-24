# S6 robot — short plan for you and the AI

Updated **2026-10-24**. Costs:[procurement.json](procurement.json). Physical inputs:[physical_spec.json](physical_spec.json). **Nothing ordered or physically tested.**

## What you receive

- **[Fit-sample ZIP](cad/sample_quotation_package.zip):2 test pieces**, servo cradle and horn plate.
- **[Full-frame quotation ZIP](cad/frame_quotation_package.zip):7 PETG parts**, one torso+two thighs+two shins+two feet. No printed soles.
- [Dimensioned interface drawing](cad/print_order/drawings/interfaces.png), [exploded assembly](cad/exploded.png), [fastener schedule](cad/print_order/fasteners.csv), [supplier brief](cad/QUOTE_REQUEST.md), [assembly instructions](cad/ASSEMBLY.md).
- Matching provisional **MuJoCo r2 model**, bare Pico+headers, eight ordinary grip pads; about **197.1 g estimated**. No printer/spool purchase; you solder the harness yourself.

**Quotation prototypes, not approved order files.** The actual horn/ear/screw fit and layer strength are unknown. First confirm the complete budget and measure an actual servo, then test the sample before the full frame. All quantities/hashes are in each ZIP manifest; do not order combined and individual files together. Forward only the sample/frame quotation ZIP, **not the complete project archive**, which also contains historical geometry.

## Complete purchase/cost snapshot — not cleared to buy

All prices are VAT-inclusive dated source snapshots, quantities are full packs. Existing PC/iron access assumed. Delivery to **25337, Germany**; PC USB-A confirmed, no adapter.

| Exact item / supplier | Buy qty | Unit € | Line € | Purpose |
|---|---:|---:|---:|---|
| [Waveshare15024 MG90S](https://www.welectron.com/Waveshare-15024-MG90S-Servo_1) — Welectron | 6 | 3.50 | 21.00 | Joint motor;6-unit stock/accessories pending |
| [Bare Pico](https://www.berrybase.de/raspberry-pi-pico-rp2040-mikrocontroller-board) — BerryBase | 1 | 4.10 | 4.10 | USB controller; solder headers |
| [MPU6050 F23107397](https://funduino.com/products/mpu-6050-modul-triaxial-beschleunigungssensor-gyroskop) — Funduino | 1 | 3.62 | 3.62 | Body accelerometer/gyro |
| [Mean Well GST40A05-P1J](https://www.berrybase.de/meanwell-schaltnetzteil-5v-dc-5-0a-mit-hohlstecker-5-5x2-1mm) — BerryBase | 1 | 15.50 | 15.50 | Enclosed5V/5A servo PSU |
| [Goobay68604 mains lead](https://www.berrybase.de/kaltgeraete-netzkabel-schutzkontakt-stecker-abgewinkelt-iec320-c13-buchse-schwarz) — BerryBase | 1 | 3.81 | 3.81 | Schuko–C13 for PSU |
| [RPI-MUSB-1 USB cable](https://www.berrybase.de/offizielles-raspberry-pi-micro-usb-kabel-rot-1-0m) — BerryBase | 1 | 1.80 | 1.80 | USB-A–Micro-B data; no adapter |
| [DUPK-40-FF-50,40leads](https://www.berrybase.de/40pin-jumper-dupont-kabel-female-female-trennbar/laenge-0-50-m) — BerryBase | 1 | 2.20 | 2.20 | Logic only; shorten I2C |
| [JR/Futaba F23108007,10cm](https://funduino.com/products/jr-futaba-servo-verlangerung-kabel-10cm-female-male) — Funduino | 6 | 1.14 | 6.84 | Replaceable servo branches;ratings pending |
| [Donau E-175-10,10m roll](https://www.berrybase.de/donau-kupferschaltlitze-0-75-mm2-10m-lang-1-adrig-24x0-20mm-pvc-isoliert) — BerryBase | 1 | 5.90 | 5.90 | 0.75mm² short power buses |
| [AiSHi1000µF/16V](https://www.berrybase.de/elektrolytkondensator-1000-f-16v-1050c-1-radial-tht) — BerryBase | 1 | 0.29 | 0.29 | Bulk bus capacitor;polarity matters |
| [PINH-1X40P,40pins](https://www.berrybase.de/stiftleiste-1x-40-polig-rm-2-54-gerade) — BerryBase | 1 | 0.60 | 0.60 | IMU/signal ends |
| [T1535561 shrink,100pieces](https://www.berrybase.de/schrumpfschlauch-set-100-teilig-schwarz) — BerryBase | 1 | 1.90 | 1.90 | Solder insulation |
| [T1535501 ties,100pack](https://www.berrybase.de/kabelbinder-uv-bestaendig-nylon-100-stueck/farbe-transparent/masse-100x2-5mm) — BerryBase | 1 | 0.45 | 0.45 | Board/wire/tether restraints |
| [Goobay11638 DC socket](https://www.berrybase.de/dc-einbaubuchse-fuer-hohlstecker-5-5x2-1mm-metallausfuehrung-loetanschluss) — BerryBase | 1 | 1.10 | 1.10 | 5A5.5×2.1mm input; accessible unplug |
| [ZD-160 flux-core solder,10g](https://www.berrybase.de/zhongdi-loetzinn-bleifrei-oe1-0-mm-2-flussmittel-10-g) — BerryBase | 1 | 1.90 | 1.90 | Soldering consumable |
| [Delock18309 pads,50pack](https://www.reichelt.de/de/de/shop/produkt/gummifuesse_rund_selbstklebend_10_x_3_mm_50_stk_schwarz-371081) — Reichelt | 1 | 3.55 | 3.55 | 8used;10mm diameter×3mm,adhesive included |
| [RPIP-PINH Pico headers](https://www.berrybase.de/stiftleisten-pin-header-set-fuer-raspberry-pi-pico) — BerryBase | 1 | 0.50 | 0.50 | 2×20pins +spare3pin debug strip |

Frame ear hardware: buy100each of [M2×8 P010265](https://www.schraubenking-shop.de/M2-x-8mm-Linsenkopfschrauben-PH-DIN7985-Stahl-verzinkt-FKL48-P010265)€1.51, [M2nuts P003474](https://www.schraubenking-shop.de/M2-Sechskantmuttern-DIN934-Stahl-verzinkt-FKL8-P003474)€1.13 and [M2washers P004198](https://www.schraubenking-shop.de/22mm-Unterlegscheiben-DIN125-Edelstahl-A2-P004198)€0.99; install12screws+12nuts+24washers. Length/stack still provisional.

**Required, unpriced:**6matching factory horns+6shaft retainers (possibly supplied, unconfirmed);12horn-to-frame screws+12matching washers; seven finished PETG prints; two fit-sample prints; every print/sample delivery and finishing/inspection charge. Never guess horn splines/threads or count unknown costs as zero.

| Supplier / contents | Parts € | Shipping € | Priced subtotal € |
|---|---:|---:|---:|
| Welectron:6servos |21.00|4.95|25.95|
| BerryBase:controller,power,wiring,solder,headers |40.05|4.95|45.00|
| Funduino:IMU+6extensions |10.46|4.90|15.36|
| Reichelt:50pads |3.55|5.95|9.50|
| Schraubenking:3fastener packs |3.63|5.90|9.53|
| **Priced basket BEFORE printing/sample/horn extras** |**78.69**|**26.65**|**105.34**|
| **Known shortfall against€100 for this basket** |||**5.34**|
| **Complete delivered total** |||**Unknown**|

Published German rates, not final postcode checkout or reserved stock. Extra staged deliveries cost extra. Print material belongs in the service quote: **no filament pack, printer or TPU sole purchase**. Header-kit consolidation saves€0.10 versus the previous basket; no unsupported shipping discounts or weaker components. [Research/questions](docs/PROCUREMENT_ACTIONS.md).

**No print service is selected:** the revised-file upload toMeltlab was blocked by automatic approval review because it shares CAD with that provider without specific authorization. Public example prices and old geometry quotes do not price this revision. Next: authorize this exact quotation upload or upload the files yourself and return the settings/breakdown/hashes. No supplier messages or purchases have been sent.

Tools: iron access confirmed; borrow/confirm meter, stripper/cutters, safe shrink heat source, scale, ruler/protractor and screw tools. Unconfirmed tool purchases remain unknown initial cash, outside the€100parts cap. Optional spare servo/protective mat/slack line are not base purchases.

## Assembly — after budget and physical-fit approval

1. **Measure and test sample:** exact servo ears/shaft/horn/screws; test the2sample pieces without forcing or drilling. Failed fit means revise/re-quote before the7frames.
2. **Solder bench electronics:** bare Pico headers, IMU and6replaceable servo branches onto insulated0.75mm² buses; capacitor/DC socket and strain relief. USB powers logic, PSU powers servos, common ground. [Wiring](docs/HARDWARE.md), [firmware/bench](firmware/README.md).
3. **Test one unloaded servo/IMU:** polarity/current/droop,3.3V signal, physical DC disconnect, disarmed boot and100ms watchdog. Calibrate zero before fitting horns; HOME is not mechanical zero.
4. **Assemble legs:** cases—hip→torso,knee→thigh,ankle→foot. Horn connections—thigh→hip,shin→knee and ankle. Use only confirmed hardware; check screw/tool/wire sweeps. [Drawing/steps](cad/ASSEMBLY.md).
5. **Mount boards/pads:** insulating stand-offs, rigid IMU, safe ties; four pads per foot at drawing coordinates. Inspect11mm Pico pin envelope and connectors. Leave joint wire loops and externally supported tether.
6. **Weigh and calibrate:** each rigid body/installed component once; record COM,servo response/range/latency/current and pad friction. Update twin/fingerprint; test manual stand before policies. STOP is not physical power isolation.

## Simulation and project sequence

| Stage | Verified now / next |
|---|---|
| CAD/print package | Implemented;37 tests pass,55 sampled poses have0 modeled collisions; **5 unknown interface groups still block manufacture** |
| MuJoCo | Compiles; matching pad geometry/mass ownership;30 s neutral standing. Estimated masses/strength/friction, not calibrated |
| Motion | Original reference +3bounded ankle variants produced **no qualifying lifted steps**; no strength increase |
| PPO | New 2048-step smoke/reload/evaluation done:0 walking successes,0 gait distance. Older 49,152-step pilot is historical |
| Current blocker | Complete affordable quote, actual horn/ear/screw fit, printed strength and physical measurements |
| Later | Measured twin → manual lifted-step verification → bounded fixed/DR A/B training → supervised physical stand/steps → equal real trials/report |

Success remains 30 s standing followed by≥0.3m visibly alternating lifted walking within 30 s; sliding is not walking. Larger training stays blocked. Physical stage data must come from you; no simulation result clears it. [Neutral video](docs/validation/2026-10-24/print_revision/final/home_clean_video/episode_0.mp4), [smoke video](docs/validation/2026-10-24/print_revision/final/smoke_clean_video/episode_0.mp4), [latest evidence](docs/VALIDATION_CURRENT.md), [status](docs/STATUS.md), [roadmap](docs/ROADMAP.md).

## AI entry and exact next action

Read this → [AGENTS](AGENTS.md) → relevant status/roadmap. Active route is outsourced PETG, not printer purchase or stock-frame research. Preserve history and all policies; never relabel fingerprints. Current identity is in the validation record; the smoke policy is **not hardware-approved**. Current invalid firmware header needs an ARM rebuild/calibration before flashing; older UF2 is historical.

**Next human action:** specific permission for Meltlab quotation uploads, or returned quote; then actual servo measurements and sample fit. Keep all[physical gates](docs/gates.json)false. Regenerate handoff and packages after a geometry change. [Full19-section reference](docs/HANDOFF.md), [project archive](school_biped_s6.zip).

```bash
.venv/bin/python -m pytest -q
.venv/bin/python tools/budget_gate.py # expected1:105.34before prints
MPLCONFIGDIR=/tmp/s6-mpl .venv/bin/python tools/prepare_print_order.py
.venv/bin/python tools/check_clearance.py # expected1:unknown interfaces
```
