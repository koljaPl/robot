# S6 robot — project summary for you and the AI

Updated **2026-10-23**. Working plan; authoritative costs: [procurement.json](procurement.json).

## Goal and current position

Roughly 18 cm biped: **hip pitch + knee pitch + ankle roll per leg**. PC inference → USB → Pico H direct PWM → six servos. Wired power; no PCA9685/battery/arms. Estimated mass: 199 g.

- **Software checked:** 29 tests pass; firmware compiles; simulation/logging/videos work. The 49,152-step nominal pilot achieved **no walking**. A/B smoke tests: 2,048 steps each; formal comparison pending.
- **Unverified:** delivered cost, mounting fit, real electronics, calibration and physical walking. Nothing purchased/assembled.
- **Success:** stand 30 s, then travel ≥0.3 m within 30 s using alternating lifted steps. Drifting/sliding does not count.

## Purchase list — provisional, not cleared to order

VAT-inclusive snapshot, 2026-10-23; stock must be confirmed. Quantities mean **packs/items to buy**. An existing PC/laptop is assumed.

| Item / shop link | Buy quantity | Unit € | Line € | What it does / issue |
|---|---:|---:|---:|---|
| [Waveshare 15024 MG90S — Welectron](https://www.welectron.com/Waveshare-15024-MG90S-Servo_1) | 6 | 3.50 | 21.00 | Joint motor; six-unit stock/horns unconfirmed |
| [Raspberry Pi Pico H — BerryBase](https://www.berrybase.de/raspberry-pi-pico-rp2040-mikrocontroller-board-mit-headern) | 1 | 5.50 | 5.50 | USB microcontroller; headers already fitted |
| [MPU6050 F23107397 — Funduino](https://funduino.com/products/mpu-6050-modul-triaxial-beschleunigungssensor-gyroskop) | 1 | 3.62 | 3.62 | Balance sensor; may need header soldering |
| [Mean Well GST40A05-P1J — BerryBase](https://www.berrybase.de/meanwell-schaltnetzteil-5v-dc-5-0a-mit-hohlstecker-5-5x2-1mm) | 1 | 15.50 | 15.50 | Enclosed 5 V / 5 A servo power supply |
| [Goobay 68604, 1.5 m — BerryBase](https://www.berrybase.de/kaltgeraete-netzkabel-schutzkontakt-stecker-abgewinkelt-iec320-c13-buchse-schwarz) | 1 | 3.81 | 3.81 | Schuko–C13 mains lead for the PSU |
| [RPI-MUSB-1, 1 m — BerryBase](https://www.berrybase.de/offizielles-raspberry-pi-micro-usb-kabel-rot-1-0m) | 1 | 1.80 | 1.80 | USB-A–Micro-B data/power cable for Pico |
| [DUPK-40-FF-20, 40 leads — BerryBase](https://www.berrybase.de/40pin-jumper-dupont-kabel-female-female-trennbar/laenge-0-20-m) | 1 | 1.80 | 1.80 | Logic/IMU connections; **unavailable**, replacement needed |
| [JR/Futaba extension F23108007, 10 cm — Funduino](https://funduino.com/products/jr-futaba-servo-verlangerung-kabel-10cm-female-male) | 6 | 1.14 | 6.84 | Replaceable servo plugs; helper prepares power harness |
| [Donau E-175-10, 0.75 mm², 10 m — BerryBase](https://www.berrybase.de/donau-kupferschaltlitze-0-75-mm2-10m-lang-1-adrig-24x0-20mm-pvc-isoliert) | 1 | 5.90 | 5.90 | Short power buses; label polarity |
| [AiSHi ELK1M16VAWH, 1000 µF / 16 V — BerryBase](https://www.berrybase.de/elektrolytkondensator-1000-f-16v-1050c-1-radial-tht) | 1 | 0.29 | 0.29 | Bulk capacitor across servo supply |
| [PINH-1X40P, 40 pins — BerryBase](https://www.berrybase.de/stiftleiste-1x-40-polig-rm-2-54-gerade) | 1 | 0.60 | 0.60 | Header pins for sensor/harness |
| [McPower T1535561, 100 pieces — BerryBase](https://www.berrybase.de/schrumpfschlauch-set-100-teilig-schwarz) | 1 | 1.90 | 1.90 | Heat-shrink insulation for solder joints |
| [McPower T1535501, 100 ties — BerryBase](https://www.berrybase.de/kabelbinder-uv-bestaendig-nylon-100-stueck/farbe-transparent/masse-100x2-5mm) | 1 | 0.45 | 0.45 | Board mounting, cable restraint and strain relief |

**Also required; prices or fit still unresolved:**

| Item / quantity | Where / action |
|---|---|
| 7 rigid PETG frames: torso + 2 thighs/shins/feet; 2 grippy TPU soles, 90 × 45 × 1 mm | [Meltlab](https://meltlab.de/preise): [files](cad/quote_bundle.zip), [quote brief](cad/QUOTE_REQUEST.md). Include finishing, clear holes, sole bonding, VAT/delivery and one fit sample. **Not quoted.** |
| 6 servo horns (shaft-to-frame levers) + 6 retaining screws | [Welectron](https://www.welectron.com/Waveshare-15024-MG90S-Servo_1): inclusion/spline/dimensions/thread unconfirmed. |
| 12 M2 × 8 screws + 12 M2 nuts + 24 washers; 12 horn-to-frame screws and matching washers | Print service: matched kit; dimensions provisional. [Schedule](cad/ASSEMBLY.md). |
| 1 rated DC input/disconnect (PSU-to-servo bus) | Candidate [Delock 83290](https://www.delock.com/produkt/83290/merkmale.html?setLanguage=de), [retailer candidate](https://www.alternate.de/DeLOCK/DC-Verl%C3%A4ngerungskabel/html/product/1317847). Confirm 5 A / 18 AWG variant, branch ratings and delivered price; helper prepares pigtail. |
| 1 helper preparation job | School/helper solders headers/capacitor/harness and supplies solder; confirm free help or price. |
| Funduino delivery; any separate supplier/sample deliveries | [Shipping policy](https://funduino.com/policies/shipping-policy): rate could not be verified. Count every shipment. |
| USB data adapter, only if PC has no USB-A | Only for USB-C-only PC; model/price pending. |

**Borrow tools:** soldering kit, cutters/stripper, multimeter, scale, ruler/protractor, phone. Tools excluded from €100; no personal printer/drilling/tapping.
**Optional:** spare servo (€3.50 + delivery), protective mat, slack safety line. Longer USB/power tethers need separate sourcing/budget.

## Cost breakdown

| Current priced positions | € |
|---|---:|
| [Welectron](https://www.welectron.com/Shipping-cost): six servos + €4.95 delivery | 25.95 |
| [BerryBase](https://www.berrybase.de/versand-und-zahlungsbedingungen): listed items + €4.95 delivery | 42.50 |
| Funduino: sensor + six extensions, **delivery missing** | 10.46 |
| **Priced subset, including the unavailable jumper pack** | **78.91** |
| **Space left under €100 for every unresolved cost** | **21.09** |
| **Complete delivered total** | **Unknown** |

Parts €69.01 + two deliveries €9.90; jumper replacement may change this. €50–75 is not met. **Do not order until costs/stock/fit pass. Stop if delivered total exceeds €100.**

## Full sequence — who does what

| Order | You / helper | AI / completion gate |
|---|---|---|
| 1. Close feasibility **← now** | Confirm servo contents/drawing, print/sample/fastener quote, harness and shipping. | Complete basket ≤€100. [Questions](docs/PROCUREMENT_ACTIONS.md). No orders/messages sent. |
| 2. Bench one servo + IMU | Prepare harness; test PSU/cutoff, USB, IMU, 3.3 V PWM and watchdog. | [Bench tools](firmware/README.md); record actual timing/electrical results. |
| 3. Measure mounting fit | Measure interfaces; approve one mounting sample. | Resolve 550 estimated fastener-envelope overlaps across 55 poses; these are **not proven bolt collisions**. No manufacturing release. |
| 4. Print and assemble | Order approved kit; assemble/weigh bodies. | Match CAD, mass ownership, COM/inertia. |
| 5. Calibrate/manual control | Measure six servos, current/response/latency, IMU and safe poses. | Version calibration/twin. Safe commands ≠ mechanical stops. [Procedure](docs/CALIBRATION.md). |
| 6. Validate the twin | Supply measurements/videos. | Validate contacts, standing/weight transfer/lifted steps. Existing reference failed; diagnose before large training. |
| 7. Train/evaluate A vs B | Review gait videos/metrics. | Fixed/randomized PPO; matched weights/budgets; seeds 0/1/2; ≤999,424 steps each. Compatible pilot counts. Validation 2000–2004; final 1000–1009. [Protocol](docs/EXPERIMENT.md). |
| 8. Transfer progressively | Supervised standing, then short steps; reachable cutoff. | Check fingerprints; log commands/IMU. No IMU double-integration distance. |
| 9. Compare/report | Video/ruler measurements; equal conditions, alternating A/B order. | Report failures/uncertainty/cable effects. [Trial sheet](docs/templates/physical_trials.csv), [report](docs/REPORT.md). |
| 10. Extend later | Only after stable walking. | Turning, recovery or terrain; no automatic scope expansion. |

## Assembly in six steps — only after budget and fit approval

1. **Prepare electronics:** helper finishes soldering/insulation; test one unloaded servo and IMU first. [Power/wiring](docs/HARDWARE.md), [firmware](firmware/README.md).
2. **Set mechanical zero:** calibrate each servo, disconnect motor power, then fit its matching horn and shaft screw. Zero is not the bent-knee HOME pose.
3. **Build legs:** hip servo cases → torso; thighs → hip horns; knee cases → thighs; shins → knee horns; ankle cases → feet; shins → ankle horns. Use only the confirmed fastener kit. [Drawing](cad/exploded.png), [detailed assembly](cad/ASSEMBLY.md).
4. **Fit boards/soles:** service bonds TPU soles; secure Pico/IMU without exposed contacts touching hardware. Leave joint service loops and cable strain relief.
5. **Wire:** USB powers Pico/IMU; separate 5 V PSU feeds servo bus; common ground. **Never send servo current through Pico or a breadboard.** PWM joint order L hip/knee/ankle, R hip/knee/ankle → GP0/1/2/3/6/7. IMU SDA/SCL → GP4/5, VCC → 3.3 V. [Pin table](docs/HARDWARE.md#pin-table).
6. **Test conservatively:** weigh bodies, check polarity/directions/ranges and disarmed boot/watchdog. Start manual standing on a low clear floor. Software STOP is not power isolation; disconnect DC after a fall and inspect before restarting.

## AI continuation — mandatory handoff

- Read this file and [AGENTS.md](AGENTS.md); then only relevant details in [STATUS](docs/STATUS.md), [ROADMAP](docs/ROADMAP.md) and implementation. The [full handoff](docs/HANDOFF.md) is reference, not the starting reading task.
- **Next:** close quote/interface/electrical unknowns; update [cost](procurement.json)/[physical](physical_spec.json) ledgers. Label sourced/estimated/measured/unknown with evidence/date; never invent verification.
- Preserve six joints, €100 delivered, PC inference, six normalized targets/90 IMU-command observations. No privileged SIM observations or weaker-servo substitution.
- [Gates](docs/gates.json) remain closed. Diagnose missing lifted steps before repeating/extending training; do not inflate torque to force success.
- **All saved policies are historical** after the firmware parser fix. Use isolated `tools/replay_snapshot.py`; never relabel fingerprints. [Evidence](docs/VALIDATION_CURRENT.md). Compiled firmware is not physically tested; example calibration cannot policy-arm.
- Update this snapshot/STATUS from ledgers; regenerate handoff/archive; preserve results. No supplier messages/purchases without explicit authorization.

New computer setup: `python3.12 -m venv .venv`, then `.venv/bin/pip install -r requirements-dev.txt`.

```bash
.venv/bin/python -m pytest -q
.venv/bin/python tools/budget_gate.py       # expected exit 2: incomplete
.venv/bin/python tools/check_clearance.py   # expected exit 1: proxy conflicts
# Historical policy review; choose a new output directory:
.venv/bin/python tools/replay_snapshot.py --episodes 1 --output runs/review_unique
```
