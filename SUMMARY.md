# S6 robot — project summary for you and the AI

Updated **2026-10-23**. Working plan; authoritative costs: [procurement.json](procurement.json).

## Goal and current position

Roughly 18 cm biped: **hip pitch + knee pitch + ankle roll per leg**. PC inference → USB → Pico H direct PWM → six servos. Wired power; no PCA9685/battery/arms. Estimated mass: 199 g.

- **Software checked:** 29 tests pass; firmware compiles; simulation/logging/videos work. The 49,152-step nominal pilot achieved **no walking**. A/B smoke tests: 2,048 steps each; formal comparison pending.
- **Blocked:** the current priced route is **€163.63 before remaining costs**, over the €100 cap. Mounting fit, electronics, calibration and physical walking remain unverified. Nothing purchased/assembled.
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
| [DUPK-40-FF-50, 40 leads — BerryBase](https://www.berrybase.de/40pin-jumper-dupont-kabel-female-female-trennbar/laenge-0-50-m) | 1 | 2.20 | 2.20 | Available 50 cm replacement; logic only; helper keeps I2C short |
| [JR/Futaba extension F23108007, 10 cm — Funduino](https://funduino.com/products/jr-futaba-servo-verlangerung-kabel-10cm-female-male) | 6 | 1.14 | 6.84 | Replaceable servo plugs; helper prepares power harness |
| [Donau E-175-10, 0.75 mm², 10 m — BerryBase](https://www.berrybase.de/donau-kupferschaltlitze-0-75-mm2-10m-lang-1-adrig-24x0-20mm-pvc-isoliert) | 1 | 5.90 | 5.90 | Short power buses; label polarity |
| [AiSHi ELK1M16VAWH, 1000 µF / 16 V — BerryBase](https://www.berrybase.de/elektrolytkondensator-1000-f-16v-1050c-1-radial-tht) | 1 | 0.29 | 0.29 | Bulk capacitor across servo supply |
| [PINH-1X40P, 40 pins — BerryBase](https://www.berrybase.de/stiftleiste-1x-40-polig-rm-2-54-gerade) | 1 | 0.60 | 0.60 | Header pins for sensor/harness |
| [McPower T1535561, 100 pieces — BerryBase](https://www.berrybase.de/schrumpfschlauch-set-100-teilig-schwarz) | 1 | 1.90 | 1.90 | Heat-shrink insulation for solder joints |
| [McPower T1535501, 100 ties — BerryBase](https://www.berrybase.de/kabelbinder-uv-bestaendig-nylon-100-stueck/farbe-transparent/masse-100x2-5mm) | 1 | 0.45 | 0.45 | Board mounting, cable restraint and strain relief |
| [Goobay11638 DC socket — BerryBase](https://www.berrybase.de/dc-einbaubuchse-fuer-hohlstecker-5-5x2-1mm-metallausfuehrung-loetanschluss) | 1 | 1.10 | 1.10 |5.5×2.1mm,5 A; helper solders/insulates; physical unplug cutoff |
| [P010265 M2 × 8 PH screws, 100 — Schraubenking](https://www.schraubenking-shop.de/M2-x-8mm-Linsenkopfschrauben-PH-DIN7985-Stahl-verzinkt-FKL48-P010265) |1 pack|1.51|1.51|12 used at servo ears; length/fit provisional |
| [P003474 M2 nuts, 100 — Schraubenking](https://www.schraubenking-shop.de/M2-Sechskantmuttern-DIN934-Stahl-verzinkt-FKL8-P003474) |1 pack|1.13|1.13|12 used;4mm wrench/pliers |
| [P004198 M2 washers, 100 — Schraubenking](https://www.schraubenking-shop.de/22mm-Unterlegscheiben-DIN125-Edelstahl-A2-P004198) |1 pack|0.99|0.99|24 used: one under each ear screw head/nut |
| [7 PETG frames, one batch — Meltlab](https://meltlab.de/konfigurator) |1 job|48.70|48.70|Torso + 2 thighs + 2 shins + 2 feet; print/support removal/VAT/DHL only |
| [2 TPU95A soles, one batch — Meltlab](https://meltlab.de/konfigurator) |1 job|20.09|20.09|Each 90 × 45 × 1 mm; print/VAT/separate DHL; bonding excluded |

**Still required, not priced/approved:**6 matching horns+6 shaft screws (manufacturer [photo](https://www.waveshare.com/img/devkit/accBoard/MG90S-Servo/MG90S-Servo-1.jpg) shows accessories; actual batch/geometry unconfirmed);12 horn-to-frame screws+12 matching washers; hole finishing, adhesive/sole bonding, fit sample/delivery and helper preparation. [Exact questions/evidence](docs/PROCUREMENT_ACTIONS.md). No generic 25T horns or guessed centre screws.

Print files: [quote bundle](cad/quote_bundle.zip), [compact layouts](cad/quotation/), [brief](cad/QUOTE_REQUEST.md). **Quotation prototypes only:** dimensions unchanged, orientation/fit unapproved; do not submit both individual and batch files as extra quantities. M2 × 8 may be too short once the actual ear stack is measured. No drilling/tapping by you.

**No USB adapter in the base list.** The USB-A–Micro-B data cable above is required; add an adapter only if your PC has no USB-A. PC port and German delivery postcode remain unconfirmed.

**Borrow tools:** soldering kit, cutters/stripper, multimeter, scale, ruler/protractor, phone. Tools excluded from €100; no personal printer/drilling/tapping.
**Optional:** spare servo (€3.50 + delivery), protective mat, slack safety line. Longer USB/power tethers need separate sourcing/budget.

## Cost breakdown

| Current route, incl. VAT | Parts/services € | Delivery € | Subtotal € |
|---|---:|---:|---:|
| [Welectron](https://www.welectron.com/Shipping-cost): six servos |21.00|4.95|25.95|
| [BerryBase](https://www.berrybase.de/versand-und-zahlungsbedingungen): electronics/power/wiring including new leads/socket |39.05|4.95|44.00|
| [Funduino](https://funduino.com/policies/shipping-policy): IMU + six extensions |10.46|4.90|15.36|
| [Schraubenking](https://www.schraubenking-shop.de/Versandinformationen): three ear-fastener packs |3.63|5.90|9.53|
| Meltlab:7 PETG, including €11.90 support removal+€5.95 order fee |42.51|6.19|48.70|
| Meltlab:2 TPU, including €5.95 order fee |13.90|6.19|20.09|
| **Priced subset** |**130.55**|**33.08**|**163.63**|
| **Already above€100, before unresolved costs** |||**63.63**|
| **Complete delivered total** |||**Unknown; higher for this route**|

**Procurement stopped.** Find a cheaper fully quoted manufacturing route; do not order this basket or weaken the servos. Electronics/delivery €85.31 + ear-fastener delivery €9.53 leave only €5.16 for every print/horn/helper cost. Combining the two print jobs may save fees/shipping, but no combined quotation exists.

**Delivery plan, not bookings:** Welectron DPD advertised 1–3 working days if all 6 available; BerryBase items usually 1–3 days; Funduino standard tracked DHL (policy says most arrive within 2 working days); fasteners 2–3 working days; prints 4 working days production after payment + 1–2 DHL days. No guaranteed arrival, reservations, address entry or orders. Avoid paid priority; any bench/sample split must add every extra delivery. [Quote records](docs/procurement/2026-10-23/quotes.json).

## Full sequence — who does what

| Order | You / helper | AI / completion gate |
|---|---|---|
| 1. Close feasibility **← now** | Resolve servo contents/fit; obtain cheaper complete manufacturing quote and helper cost. | Current route fails €100; replace it with a verified complete basket ≤€100. [Questions](docs/PROCUREMENT_ACTIONS.md). No orders/messages sent. |
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
- **Next:** resolve the €63.63 known overrun plus unknown finishing/horn/helper costs; obtain exact cheaper delivered quotes and interface evidence, then update [cost](procurement.json)/[physical](physical_spec.json) ledgers. Label sourced/estimated/measured/unknown with evidence/date; never invent verification.
- Preserve six joints, €100 delivered, PC inference, six normalized targets/90 IMU-command observations. No privileged SIM observations or weaker-servo substitution.
- [Gates](docs/gates.json) remain closed. Diagnose missing lifted steps before repeating/extending training; do not inflate torque to force success.
- **All saved policies are historical** after the firmware parser fix. Use isolated `tools/replay_snapshot.py`; never relabel fingerprints. [Evidence](docs/VALIDATION_CURRENT.md). Compiled firmware is not physically tested; example calibration cannot policy-arm.
- Update this snapshot/STATUS from ledgers; regenerate handoff/archive; preserve results. No supplier messages/purchases without explicit authorization.

New computer setup: `python3.12 -m venv .venv`, then `.venv/bin/pip install -r requirements-dev.txt`.

```bash
.venv/bin/python -m pytest -q
.venv/bin/python tools/budget_gate.py       # expected exit 1: over budget
.venv/bin/python tools/check_clearance.py   # expected exit 1: proxy conflicts
# Historical policy review; choose a new output directory:
.venv/bin/python tools/replay_snapshot.py --episodes 1 --output runs/review_unique
```
