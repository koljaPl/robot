# From Simulation to Reality: How does a robot learn?

Generated from source by `python tools/build_handoff.py`. Do not edit HANDOFF.md.
Research/revision date2026-10-24. Source files, ledgers and evidence states take precedence.
Short purchase/build plan for humans and AI: [SUMMARY.md](../SUMMARY.md).

## 1. Short design recommendation

Retain six Waveshare15024 MG90S servos: hip pitch, knee pitch and ankle roll per
leg, broad feet, Pico native PWM, MPU6050, PC USB
inference and separate5V servo power. This is a **provisional** design, not a
purchasable or calibrated walking robot. Nothing purchased/physically tested.
User can solder; no mandatory helper. Active route is outsourced PETG:seven frame
parts,two separate fit samples,eight bought TPE pads. Bare Pico/header ownership
and pad contacts now match the provisional twin. No printer/filament/printedTPU
purchase. Complete delivered budget, actual fit and strength are still blocked.
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

## 5. Required BOM and incomplete route alternatives

Authoritative `procurement.json`, checked2026-10-24. Null prices are required,
unresolved costs, never zero. Quantities include full packs where sold as packs.

Shared parts plus active commercial_print scenario are the required basket. Other
scenarios are retained comparisons, not additional quantities or purchase selections.

| Category | Exact item / supplier source | Qty | Unit € | Line € | Selection / unresolved issue |
|---|---|---:|---:|---:|---|
| Motors | [Waveshare 15024 MG90S](https://www.welectron.com/Waveshare-15024-MG90S-Servo_1) — Welectron | 6 | 3.50 | 21.00 | VAT included, stock shown; horn/screw inclusion unverified |
| Electronics | [Raspberry Pi Pico (bare RP2040 board)](https://www.berrybase.de/raspberry-pi-pico-rp2040-mikrocontroller-board) — BerryBase | 1 | 4.10 | 4.10 | Selected provisional bare Pico +soldered headers; GPIOs unchanged. Updated twin owns4.2g inclusive-header module estimate, not a measured mass. |
| Sensors | [Funduino F23107397 MPU6050 module](https://funduino.com/products/mpu-6050-modul-triaxial-beschleunigungssensor-gyroskop) — Funduino | 1 | 3.62 | 3.62 | Header soldering/board orientation to confirm |
| Power | [Mean Well GST40A05-P1J 5 V 5 A desktop PSU](https://www.berrybase.de/meanwell-schaltnetzteil-5v-dc-5-0a-mit-hohlstecker-5-5x2-1mm) — BerryBase | 1 | 15.50 | 15.50 | C14 inlet; centre-positive 5.5 x 2.1 mm; no mains lead in package |
| Power | [Goobay 68604 Schuko to C13, 1.5 m](https://www.berrybase.de/kaltgeraete-netzkabel-schutzkontakt-stecker-abgewinkelt-iec320-c13-buchse-schwarz) — BerryBase | 1 | 3.81 | 3.81 | Exact 1.5 m variant; 10 A AC rating |
| Wiring/connectors | [Official Raspberry Pi RPI-MUSB-1 USB data cable 1 m](https://www.berrybase.de/offizielles-raspberry-pi-micro-usb-kabel-rot-1-0m) — BerryBase | 1 | 1.80 | 1.80 | USB-A–Micro-B data cable required for Pico. User confirmed PC USB-A on2026-10-23; no adapter required or included. |
| Wiring/connectors | [DUPK-40-FF-50, 40 female-female Dupont leads, 50 cm](https://www.berrybase.de/40pin-jumper-dupont-kabel-female-female-trennbar/laenge-0-50-m) — BerryBase | 1 | 2.20 | 2.20 | Logic only. User shortens and insulates signal/I2C leads as needed; preserve removable female ends. Keep I2C short; verify continuity. Never servo power. |
| Wiring/connectors | [Funduino F23108007 JR-Futaba extension, 10 cm](https://funduino.com/products/jr-futaba-servo-verlangerung-kabel-10cm-female-male) — Funduino | 6 | 1.14 | 6.84 | User solders six replaceable servo sockets into short heavy positive/return buses; isolate each signal to its Pico GPIO. Actual wire gauge, contact rating, plug fit and current/droop must pass bench tests. |
| Wiring/connectors | [Donau E-175-10 red copper wire 0.75 mm², 10 m roll](https://www.berrybase.de/donau-kupferschaltlitze-0-75-mm2-10m-lang-1-adrig-24x0-20mm-pvc-isoliert) — BerryBase | 1 | 5.90 | 5.90 | Short <=10 cm power buses; label negative with black shrink; no long thin power tether |
| Power | [AiSHi ELK1M16VAWH 1000 µF 16 V capacitor](https://www.berrybase.de/elektrolytkondensator-1000-f-16v-1050c-1-radial-tht) — BerryBase | 1 | 0.29 | 0.29 | Polarity matters; actual tolerance ±20%, inconsistent page title ignored |
| Wiring/connectors | [PINH-1X40P 40-pin 2.54 mm header](https://www.berrybase.de/stiftleiste-1x-40-polig-rm-2-54-gerade) — BerryBase | 1 | 0.60 | 0.60 | One full40pin pack for up to8IMU pins+6signal ends;26spare. Pico headers supplied by separate RPIP-PINH kit. |
| Wiring/connectors | [McPower T1535561 heat-shrink, 100 pieces](https://www.berrybase.de/schrumpfschlauch-set-100-teilig-schwarz) — BerryBase | 1 | 1.90 | 1.90 | Insulate all user-soldered harness joints and label negative polarity; full shrink pack and separate10g solder pack are included. |
| Fasteners | [McPower T1535501 cable ties, 100 x 2.5 mm, pack of 100](https://www.berrybase.de/kabelbinder-uv-bestaendig-nylon-100-stueck/farbe-transparent/masse-100x2-5mm) — BerryBase | 1 | 0.45 | 0.45 | Six board ties +four tether strain restraints +eight harness restraints; full100pack, leave joint loops. |
| Power | [Goobay 11638 DC socket 5.5 x 2.1 mm, solder lugs, 5 A](https://www.berrybase.de/dc-einbaubuchse-fuer-hohlstecker-5-5x2-1mm-metallausfuehrung-loetanschluss) — BerryBase | 1 | 1.10 | 1.10 | Retailer specifies 5 A / 30 V DC, nut and washer. User solders short 0.75 mm2 bus, insulates lugs/case and provides strain relief using listed shrink/ties; support off robot. Unplug PSU DC for physical cutoff. Not branch-current or electrical verification. |
| Shipping | [Welectron German DPD shipping](https://www.welectron.com/Shipping-cost) — Welectron | 1 | 4.95 | 4.95 | Basket under €49 free-shipping threshold |
| Shipping | [BerryBase German DHL shipping](https://www.berrybase.de/versand-und-zahlungsbedingungen) — BerryBase | 1 | 4.95 | 4.95 | DHL EUR4.95 below EUR200; free-shipping threshold changed from recorded EUR150 |
| Shipping | [Funduino German shipping](https://funduino.com/policies/shipping-policy) — Funduino | 1 | 4.90 | 4.90 | Current policy opened in browser: Germany standard DHL EUR4.90 inclVAT; free only from EUR69 after discounts; tracking; no express surcharge. Snapshot docs/procurement/2026-10-23/funduino-shipping.txt |
| Consumables | [Zhongdi ZD-160 lead-free solder, 1 mm, 2% flux, 10 g](https://www.berrybase.de/zhongdi-loetzinn-bleifrei-oe1-0-mm-2-flussmittel-10-g) — BerryBase | 1 | 1.90 | 1.90 | Full 10 g pack counted; Sn99.3Cu0.7, flux core. No mandatory helper labour. Iron/tool access confirmed by user; other tools must be borrowed or priced separately. |
| Mechanical | [Delock 18309 self-adhesive TPE pads, 10 x 3 mm, pack50](https://www.reichelt.de/de/de/shop/produkt/gummifuesse_rund_selbstklebend_10_x_3_mm_50_stk_schwarz-371081) — Reichelt | 1 | 3.55 | 3.55 | Eight used, four per foot;42spare.10mm diameter x3mm TPE with adhesive; new twin uses discrete cylinders. Product dimensions sourced; friction/density/adhesion/positions provisional. |
| Shipping | [Reichelt German standard DHL delivery](https://www.reichelt.de/de/de/shop/service/-12_28) — Reichelt | 1 | 5.95 | 5.95 | Germany <=10 kg published rate. Final 25337 checkout pending; no booking. |
| Wiring/connectors | [BerryBase RPIP-PINH Pico header kit](https://www.berrybase.de/stiftleisten-pin-header-set-fuer-raspberry-pi-pico) — BerryBase | 1 | 0.50 | 0.50 | Two20pin headers for Pico; confirm package, solder yourself. Any supplied3pin debug strip is spare, not required. With one40pin pack provides at least80pins. Saves0.10 vs two40pin packs. |

### Commercial PETG frame +ordinary grip pads — selected

| Additional item / source | Qty | Unit € | Line € | Issue |
|---|---:|---:|---:|---|
| [Schraubenking P010265 M2 x 8 PH DIN7985 zinc-plated steel 4.8, pack100](https://www.schraubenking-shop.de/M2-x-8mm-Linsenkopfschrauben-PH-DIN7985-Stahl-verzinkt-FKL48-P010265) | 1 | 1.51 | 1.51 | 12 ear screws used; 88 spare. Exact length/ear fit provisional. Head4mm dia/1.6mm high, PH1; M2 coarse thread. Do not order before stack/clearance review. |
| [Schraubenking P003474 M2 DIN934 zinc-plated steel class8 nuts, pack100](https://www.schraubenking-shop.de/M2-Sechskantmuttern-DIN934-Stahl-verzinkt-FKL8-P003474) | 1 | 1.13 | 1.13 | 12 used;88spare. Current browser price1.13; stale cached page1.16/20%VAT rejected. SW4,1.6mm high,0.4mm pitch; match M2 ear screws. |
| [Schraubenking P004198 M2 DIN125 A2 washers 2.2 x 5 x 0.3 mm, pack100](https://www.schraubenking-shop.de/22mm-Unterlegscheiben-DIN125-Edelstahl-A2-P004198) | 1 | 0.99 | 0.99 | 24 used at ears: one under each head and nut. 76spare; horn washer compatibility not presumed. Check5mm OD clears plastic ear/slot and horn sweep. |
| [Schraubenking German standard DHL delivery](https://www.schraubenking-shop.de/Versandinformationen) | 1 | 5.90 | 5.90 | Current Germany standard rate below99EUR; DHL1-3days afterdispatch. No priority selected. One shipment for all three fastener packs. |
| [6 matching horns + 6 servo shaft retaining screws](https://www.welectron.com/Waveshare-15024-MG90S-Servo_1) | 1 | pending | pending | Manufacturer package photo shows three horn shapes and three screws, but text lists servo only. Six selected horns and six correct retainers required; exact Welectron batch inclusion/spline/thread/geometry remain unconfirmed. No generic 25T substitution; no extra horns bought until confirmed. |
| 12 horn-to-frame screws and 12 matching washers | 1 | pending | pending | 12 screws + 12 washers, two per horn; diameter/thread/length unknown. Separate from six centre shaft retainers. Measure actual factory horns and frame thickness; do not guess M2 or generic 25T. |
| PETG full frame:7finished parts, VAT, packaging and delivery to25337 | 1 | pending | pending | No current file-specific delivered quote. One torso+2thighs+2shins+2feet. Support removal, usable holes, finishing and any fit inspection must be priced; no printed soles/filament. |
| PETG fit sample:2interface pieces, VAT and separate delivery | 1 | pending | pending | Ear cradle +horn plate. Separate fit-first order; include shipping/finishing. Any sample/full-order combination must be explicitly quoted, not assumed free. |


Optional: spare matching servo, thin protective surface, slack safety thread,
longer adequate power/USB tethers. These are not silently needed to make the
short initial indoor trial work; several-metre travel needs a newly budgeted tether.

## 6. Total cost and procurement gate

```json
{
  "active_required_basket": {
    "scenario": "commercial_print",
    "status": "OVER BUDGET",
    "known_delivered_subtotal_eur": "105.34",
    "remaining_for_all_unknowns_eur": "-5.34",
    "confirmed_minimum_shortfall_eur": "5.34",
    "total_price_eur": null,
    "pending_prices": [
      "6 matching horns + 6 servo shaft retaining screws",
      "12 horn-to-frame screws and 12 matching washers",
      "PETG full frame:7finished parts, VAT, packaging and delivery to25337",
      "PETG fit sample:2interface pieces, VAT and separate delivery"
    ],
    "unresolved_checks": [
      "All required full-frame/sample/finishing/horn costs and stock unresolved; unknowns never zero",
      "Six-unit Waveshare stock and actual supplied horn/shaft screw contents",
      "3.3V PWM threshold, branch/contact current ratings and PSU droop still need bench testing",
      "Final complete delivery to25337 incl every sample shipment; no bookings/orders/messages",
      "Fit/layer strength/pad friction and adhesion require physical measurements",
      "Complete delivered basket exceeds cap before new printing quotation; no order",
      "Exact Waveshare batch horns/retainers/screw/ear measurements and interface sample fit",
      "Current exact-file print/support/finishing/sample/delivery prices missing",
      "Automatic approval review blocked Meltlab STL upload; provider-specific upload authorization required",
      "Physical layer strength, continuous clearances, tie/connector routing and pad grip not verified"
    ],
    "purchase_cleared": false
  },
  "routes": {
    "commercial_print": {
      "scenario": "commercial_print",
      "status": "OVER BUDGET",
      "known_delivered_subtotal_eur": "105.34",
      "remaining_for_all_unknowns_eur": "-5.34",
      "confirmed_minimum_shortfall_eur": "5.34",
      "total_price_eur": null,
      "pending_prices": [
        "6 matching horns + 6 servo shaft retaining screws",
        "12 horn-to-frame screws and 12 matching washers",
        "PETG full frame:7finished parts, VAT, packaging and delivery to25337",
        "PETG fit sample:2interface pieces, VAT and separate delivery"
      ],
      "unresolved_checks": [
        "All required full-frame/sample/finishing/horn costs and stock unresolved; unknowns never zero",
        "Six-unit Waveshare stock and actual supplied horn/shaft screw contents",
        "3.3V PWM threshold, branch/contact current ratings and PSU droop still need bench testing",
        "Final complete delivery to25337 incl every sample shipment; no bookings/orders/messages",
        "Fit/layer strength/pad friction and adhesion require physical measurements",
        "Complete delivered basket exceeds cap before new printing quotation; no order",
        "Exact Waveshare batch horns/retainers/screw/ear measurements and interface sample fit",
        "Current exact-file print/support/finishing/sample/delivery prices missing",
        "Automatic approval review blocked Meltlab STL upload; provider-specific upload authorization required",
        "Physical layer strength, continuous clearances, tie/connector routing and pad grip not verified"
      ],
      "purchase_cleared": false
    }
  },
  "printer_comparisons": {}
}
```

### Active commercial-print procurement actions — 2026-10-24

Delivery25337Germany; PCUSB-A, no adapter; required USB data cable retained.
No purchases, supplier messages, reservations or print orders have occurred.
Authoritative ledger:`../procurement.json`; packages:`../cad/`.

#### Ready to forward for quotation, not order

- [Sample ZIP](../cad/sample_quotation_package.zip): two separate mounting-test pieces.
- [Frame ZIP](../cad/frame_quotation_package.zip): sevenPETG parts, no TPU soles.
- [Supplier brief](../cad/QUOTE_REQUEST.md), [drawing](../cad/print_order/drawings/interfaces.png),
  [quantity/hash manifest](../cad/print_order/manifest.json), [assembly](../cad/ASSEMBLY.md).
- A combined7component STL is an alternative calculator input only; never add it
  to the seven individual pieces as extra quantities. Hash final geometry before quote.

#### Costs and reductions

Common priced subset95.81EUR +three ear-fastener packs/delivery9.53EUR =
**105.34EUR before printing, sample delivery and unknown horn hardware**.
Known shortfall for this basket:5.34EUR; complete delivered total unknown.
The same parts previously cost95.91before mechanics. A0.50EUR Pico header kit
plus one0.60EUR40pin pack saves0.10EUR and retains all pins. No weaker motors,
undersized PSU/wire, omitted mains lead or assumed free consumables.

Shipping/VAT rates remain published Germany snapshots, not a final checkout:
Welectron4.95, BerryBase4.95, Funduino4.90, Reichelt5.95, Schraubenking5.90EUR.
One shipping charge per supplier; every staged sample delivery is additional unless
an actual quotation states otherwise. Print material is inside the service quote:
**no filament spool/printer/printed TPU** is in the active basket.

Consolidating the IMU at BerryBase was rejected:9.90EUR vs3.62 adds6.28 before any
4.90shipping saving, with a differing module/interface listing. Combining fasteners
with pads or printer service remains an unpriced possibility, not credited savings.
Old quotations refer to old geometry and cannot price this revision.
A direct3pin-header harness could replace extension cables using the existing pin
packs, but actual mating/keying,3Acontact suitability and insulation/strain relief
remain unverified. It is a research candidate only; no saving is credited.

#### Public print-service review

| Service | Verified public capability | Price / missing evidence |
|---|---|---|
| [Meltlab](https://meltlab.de/konfigurator) | Instant STL calculator; public page describes PETG and selectable support removal | Exact revised-file upload was blocked by automatic approval review; no new quote |
| [f3dprint](https://www.f3dprint.de/druck-service) | STL/3MF, PETG,0.20mm; online price UI | Required25%infill/3walls/finishing not established; no file quote/upload |
| [Riesen Consulting](https://riesen-consulting.de/cad-dienstleistungen/3d-druck-service/3d-druck-online-bestellen-preis-sofort-berechnen/) | Instant FDM calculator, Germany delivery | Page explicitly separates fit review/finishing from automated printing; no complete quote/inquiry |

No service has a complete budget-passing quotation, so **none is selected**.
Public example prices are not this project's quotation.

#### Required human action / exact questions

1. Authorize uploading the exact current combined frame STL and two sample STLs
   to **Meltlab** for quotations only, or upload them yourself and return settings,
   price breakdown and file hashes. Automatic approval review rejected the upload
   because it shares design data with that provider without specific authorization.
   This is separate from purchase or supplier-message permission.
2. Ask for sample2pieces and frame7pieces separately: PETG black,0.20mm,3walls,25%infill,
   reviewed load orientation, removed supports, usable holes without student drilling,
   finishing/inspection, VAT, packaging and each delivery to25337.
3. Confirm six-unit stock and actual Waveshare15024 accessory contents. Measure ear,
   shaft, horn holes and supplied screws before final geometry or manufacturing approval.
4. Confirm matching6horns+6retainers and12horn-frame screws+12washers. Ear screw length
   and wrench/sweep clearance need the real stack; do not guess spline or threads.
5. Confirm JR wire/contact ratings,3.3V servo signal acceptance, real current/droop and
   tool access. Test one servo/IMU and the physical disconnect before full assembly.

A quote over100EUR does not authorize procurement. Preserve its exact shortfall and
continue independent provisional simulation; no hardware/manufacturing gate is cleared.
Previous standard/own-printer and commercialTPU comparisons remain under `history/`.

## 7. Mechanical design

`cad/build_frame.py` generates sevenPETG frames from physical_spec.json. Separate
sample/frame ZIPs include quantities,hashes,editable sources,drawings and fastener
schedule.90x45mm feet,50mm links,roughly18cm height. Ordinary10x3mm pads replace
continuous soles. Motor-ear/horn/shaft/screw fit remains unmeasured; sample first.
No manufacturing approval or actual printed density/strength is implied.

### Frame route decision — 2026-10-24

**Active:** commercial PETG frame +ordinary TPE pads. No printer purchase, no
filament spool or printed TPU soles. Self-solder electronics; six original joints.
User selected this route after comparing ready-made mechanics and own printing.

Deliverables:[sample2pieces](../cad/sample_quotation_package.zip),
[frame7pieces](../cad/frame_quotation_package.zip),[brief](../cad/QUOTE_REQUEST.md),
[drawings](../cad/print_order/drawings/interfaces.png),[assembly](../cad/ASSEMBLY.md).
All are quotation/fit prototypes. No frame manufacturing approval.

The physical ledger and MuJoCo now agree on Pico/header component ownership and
four cylindrical grip pads per foot. Solid-CAD masses and motor/friction parameters
remain estimates. Exact servo/horn fit, layer strength and budget must be proven.

Active priced basket105.34EUR before print/sample/horn extras, minimum known
shortfall5.34for this basket. Updated exact-file quote is missing: automatic approval
review blocked the Meltlab upload. No alternate provider was used to bypass it.
No supplier messages/orders; precise questions are in PROCUREMENT_ACTIONS.md.

Earlier standard-parts, own-printer/A1mini/Ender and commercialTPU comparisons are
historical in history/2026-10-24/pre_print_revision/. Their prices/configurations
are not this revision's quotation and do not authorize any purchase.

### S6-PETG-pad-r2 — assembly and fit checklist

**Quotation prototype, not manufacturing-approved.** All dimensions are in the
physical ledger; none of this is a physical test. [Exploded view](exploded.png),
[interface drawing](print_order/drawings/interfaces.png), [fasteners](print_order/fasteners.csv).
Commercial printing is active; no printer/spool or printed TPU sole purchase.

#### Parts and exact installed quantities

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

#### 1 — Fit sample before the full frame

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

#### 2 — Bench and mechanical zero

Solder/insulate the bare Pico, IMU header and replaceable harness as described in
[HARDWARE](../docs/HARDWARE.md). Test PSU polarity, DC disconnect, one unloaded
servo,3.3V PWM, IMU, disarmed startup and100ms watchdog first. USB powers logic;
servo power bypasses Pico/breadboard. No physical gate is passed yet.

Set each servo to its measured **zero-joint** pulse, then disconnect DC before
fitting its compatible horn and shaft screw. HOME(-10,+10,0deg per leg) is not
mechanical zero. Software STOP is not physical isolation.

#### 3 — Assemble the verified frame

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

#### 4 — Electronics, pads and cables

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

#### 5 — Weigh, inspect and calibrate

Weigh every assembled rigid body and installed hardware once. The current model
uses solid-CAD PETG inertia and estimated electronics/hardware/pad masses, not
slicer25%infill or measured masses. Match measured COM/masses and version the twin.

With motor power off inspect full safe sweeps, lead exits, connectors, access to
retainers and all through-holes. Then test small unloaded motions, physical cutoff,
watchdog, disarmed reboot and manual standing. At a fall disconnect DC, inspect
gears/ears, pick up manually and deliberately reinitialize. Physical policies need
measured validated calibration and matching fingerprints; the smoke policy is not
approved for hardware. Full-frame release and walking remain blocked.

Body origins/axes, command intervals and mass/COM below derive from the ledger.
Unknown mechanical stops remain null and are absent from provisional MJCF.

| Body | Parent | Joint / axis | Origin in parent (mm) | Safe commands, NOT mechanical stops (°) | Mass (g) | COM local (mm) |
|---|---|---|---|---|---:|---|
| torso | world | root / floating | 0.000, 0.000, 156.240 | free | 75.74 | -6.321, 0.000, -10.299 |
| left_thigh | torso | left_hip / 0.000, 1.000, 0.000 | 0.000, 34.000, -30.000 | [-35, 35] | 19.77 | 0.000, -9.229, -43.367 |
| left_shin | left_thigh | left_knee / 0.000, 1.000, 0.000 | 0.000, 0.000, -50.000 | [-10, 60] | 8.62 | 1.770, 2.022, -25.191 |
| left_foot | left_shin | left_ankle / 1.000, 0.000, 0.000 | 0.000, 0.000, -50.000 | [-20, 20] | 32.26 | -3.144, 0.000, -14.081 |
| right_thigh | torso | right_hip / 0.000, 1.000, 0.000 | 0.000, -34.000, -30.000 | [-35, 35] | 19.77 | 0.000, 9.229, -43.367 |
| right_shin | right_thigh | right_knee / 0.000, 1.000, 0.000 | 0.000, 0.000, -50.000 | [-10, 60] | 8.62 | 1.770, -2.022, -25.191 |
| right_foot | right_shin | right_ankle / 1.000, 0.000, 0.000 | 0.000, 0.000, -50.000 | [-20, 20] | 32.26 | -3.144, -0.000, -14.081 |

| Body | Component (mass assigned once) | Dimensions xyz (mm) | Mass (g) | COM local xyz (mm) |
|---|---|---|---:|---|
| torso | torso_frame | 33.500, 82.000, 88.750 | 21.94 | -16.316, 0.000, -4.846 |
| torso | pico | 3.500, 51.000, 21.000 | 3.00 | -10.750, 0.000, 23.000 |
| torso | imu | 4.000, 16.000, 20.000 | 3.00 | -25.500, 0.000, 18.000 |
| torso | torso_wires_fasteners | 30.000, 70.000, 40.000 | 20.00 | 0.000, 0.000, 5.000 |
| torso | left_hip_servo | 12.200, 28.500, 22.800 | 12.20 | 0.000, 19.750, -34.750 |
| torso | right_hip_servo | 12.200, 28.500, 22.800 | 12.20 | 0.000, -19.750, -34.750 |
| torso | left_hip_ear_bolt_-1 | 5.000, 8.000, 5.000 | 0.55 | 0.000, 27.000, -48.750 |
| torso | left_hip_ear_bolt_+1 | 5.000, 8.000, 5.000 | 0.55 | 0.000, 27.000, -20.750 |
| torso | right_hip_ear_bolt_-1 | 5.000, 8.000, 5.000 | 0.55 | 0.000, -27.000, -48.750 |
| torso | right_hip_ear_bolt_+1 | 5.000, 8.000, 5.000 | 0.55 | 0.000, -27.000, -20.750 |
| torso | pico_header_0 | 11.000, 50.800, 2.540 | 0.60 | -10.000, 0.000, 14.110 |
| torso | pico_header_1 | 11.000, 50.800, 2.540 | 0.60 | -10.000, 0.000, 31.890 |
| left_thigh | left_thigh_frame | 24.000, 13.500, 87.750 | 5.27 | 0.000, -0.974, -24.526 |
| left_thigh | left_knee_servo | 12.200, 28.500, 22.800 | 12.20 | 0.000, -14.250, -54.750 |
| left_thigh | left_knee_ear_bolt_-1 | 5.000, 8.000, 5.000 | 0.55 | 0.000, -7.000, -68.750 |
| left_thigh | left_knee_ear_bolt_+1 | 5.000, 8.000, 5.000 | 0.55 | 0.000, -7.000, -40.750 |
| left_thigh | left_hip_horn_hardware | 20.000, 5.000, 26.000 | 1.20 | 0.000, 3.500, 0.000 |
| left_shin | left_shin_frame | 24.000, 24.000, 78.000 | 6.22 | 1.777, 2.128, -25.264 |
| left_shin | left_knee_horn_hardware | 20.000, 5.000, 26.000 | 1.20 | 0.000, 3.500, 0.000 |
| left_shin | left_ankle_horn_hardware | 5.000, 20.000, 26.000 | 1.20 | 3.500, 0.000, -50.000 |
| left_foot | left_foot_frame | 90.000, 45.000, 38.250 | 18.02 | 4.134, 0.000, -20.373 |
| left_foot | left_ankle_servo | 28.500, 12.200, 22.800 | 12.20 | -14.250, 0.000, -4.750 |
| left_foot | left_foot_pad_0 | 10.000, 10.000, 3.000 | 0.24 | -31.000, -14.500, -25.500 |
| left_foot | left_foot_pad_1 | 10.000, 10.000, 3.000 | 0.24 | -31.000, 14.500, -25.500 |
| left_foot | left_foot_pad_2 | 10.000, 10.000, 3.000 | 0.24 | 43.000, -14.500, -25.500 |
| left_foot | left_foot_pad_3 | 10.000, 10.000, 3.000 | 0.24 | 43.000, 14.500, -25.500 |
| left_foot | left_ankle_ear_bolt_-1 | 8.000, 5.000, 5.000 | 0.55 | -7.000, 0.000, -18.750 |
| left_foot | left_ankle_ear_bolt_+1 | 8.000, 5.000, 5.000 | 0.55 | -7.000, 0.000, 9.250 |
| right_thigh | right_thigh_frame | 24.000, 13.500, 87.750 | 5.27 | 0.000, 0.974, -24.526 |
| right_thigh | right_knee_servo | 12.200, 28.500, 22.800 | 12.20 | 0.000, 14.250, -54.750 |
| right_thigh | right_knee_ear_bolt_-1 | 5.000, 8.000, 5.000 | 0.55 | 0.000, 7.000, -68.750 |
| right_thigh | right_knee_ear_bolt_+1 | 5.000, 8.000, 5.000 | 0.55 | 0.000, 7.000, -40.750 |
| right_thigh | right_hip_horn_hardware | 20.000, 5.000, 26.000 | 1.20 | 0.000, -3.500, 0.000 |
| right_shin | right_shin_frame | 24.000, 24.000, 78.000 | 6.22 | 1.777, -2.128, -25.264 |
| right_shin | right_knee_horn_hardware | 20.000, 5.000, 26.000 | 1.20 | 0.000, -3.500, 0.000 |
| right_shin | right_ankle_horn_hardware | 5.000, 20.000, 26.000 | 1.20 | 3.500, 0.000, -50.000 |
| right_foot | right_foot_frame | 90.000, 45.000, 38.250 | 18.02 | 4.134, -0.000, -20.373 |
| right_foot | right_ankle_servo | 28.500, 12.200, 22.800 | 12.20 | -14.250, 0.000, -4.750 |
| right_foot | right_foot_pad_0 | 10.000, 10.000, 3.000 | 0.24 | -31.000, 14.500, -25.500 |
| right_foot | right_foot_pad_1 | 10.000, 10.000, 3.000 | 0.24 | -31.000, -14.500, -25.500 |
| right_foot | right_foot_pad_2 | 10.000, 10.000, 3.000 | 0.24 | 43.000, 14.500, -25.500 |
| right_foot | right_foot_pad_3 | 10.000, 10.000, 3.000 | 0.24 | 43.000, -14.500, -25.500 |
| right_foot | right_ankle_ear_bolt_-1 | 8.000, 5.000, 5.000 | 0.55 | -7.000, 0.000, -18.750 |
| right_foot | right_ankle_ear_bolt_+1 | 8.000, 5.000, 5.000 | 0.55 | -7.000, 0.000, 9.250 |

| Body | Ixx, Iyy, Izz, Ixy, Ixz, Iyz (kg·m²) |
|---|---|
| torso | 8.148313e-05, 5.34409e-05, 4.489893e-05, -6.368546e-22, 7.760571e-06, -8.856731e-22 |
| left_thigh | 1.201339e-05, 1.069531e-05, 2.361686e-06, -1.292697e-23, 9.29062e-24, -2.750783e-06 |
| left_shin | 5.202857e-06, 5.271289e-06, 4.593362e-07, 2.259578e-08, 3.373974e-07, -3.106646e-07 |
| left_foot | 6.690079e-06, 1.906431e-05, 1.860375e-05, -7.946503e-23, 2.654014e-06, 1.52336e-22 |
| right_thigh | 1.201339e-05, 1.069531e-05, 2.361686e-06, 1.292697e-23, 9.29062e-24, 2.750783e-06 |
| right_shin | 5.202857e-06, 5.271289e-06, 4.593362e-07, -2.259578e-08, 3.373974e-07, 3.106646e-07 |
| right_foot | 6.690079e-06, 1.906431e-05, 1.860375e-05, 7.946503e-23, 2.654014e-06, -1.52336e-22 |

Authoritative structured physical input (provisional):

```json
{
  "name": "School Biped S6",
  "status": "PROVISIONAL QUOTATION DESIGN: sample fit, budget, layer strength and physical calibration NOT approved",
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
    "ankle_to_floor": 0.027,
    "torso_dimensions": [
      0.04,
      0.082,
      0.066
    ],
    "cad_wall": 0.003,
    "cad_clearance": 0.0004,
    "petg_density": 1270,
    "mount": {
      "case_plate_width": 0.02,
      "case_plate_height": 0.038,
      "case_plate_y": -0.007,
      "ear_clearance_diameter": 0.0024,
      "horn_plate_dimensions": [
        0.024,
        0.003,
        0.028
      ],
      "horn_plate_y": 0.0035,
      "shaft_access_diameter": 0.006,
      "horn_slot_width": 0.0024,
      "horn_slot_length": 0.007,
      "horn_slot_radius": 0.009,
      "torso_back_x": -0.02,
      "board_tie_hole_diameter": 0.0032,
      "board_tie_y": [
        -0.032,
        -0.016,
        0.016,
        0.032
      ],
      "board_tie_z": [
        0.01,
        0.028
      ],
      "board_support_y": [
        -0.018,
        0.018
      ],
      "board_support_z": [
        0.023
      ],
      "board_support_size": [
        0.006,
        0.005,
        0.005
      ],
      "imu_support_dimensions": [
        0.002,
        0.003,
        0.005
      ],
      "imu_support_y": [
        -0.005,
        0.005
      ],
      "imu_support_z": 0.023
    },
    "grip_pad": {
      "product": "Delock18309",
      "radius": 0.005,
      "height": 0.003,
      "centres_xy": [
        [
          -0.031,
          -0.0145
        ],
        [
          -0.031,
          0.0145
        ],
        [
          0.043,
          -0.0145
        ],
        [
          0.043,
          0.0145
        ]
      ],
      "density_estimate_kg_m3": 1000,
      "placement_state": "estimated; dimensions sourced, placement/friction/density/adhesion require measurement",
      "source": "https://www.delock.com/produkt/18309/pdf.html?sprache=de"
    },
    "cad_features": {
      "tool_cut_depth": 0.012,
      "thigh_bridges": [
        {
          "dimensions": [
            0.004,
            0.003,
            0.02
          ],
          "center": [
            0.01,
            0.0035,
            -0.022
          ]
        },
        {
          "dimensions": [
            0.004,
            0.0135,
            0.004
          ],
          "center": [
            0.01,
            -0.00175,
            -0.03
          ]
        },
        {
          "dimensions": [
            0.004,
            0.003,
            0.013
          ],
          "center": [
            0.01,
            -0.007,
            -0.0365
          ]
        }
      ],
      "shin_web_allowance": 0.018,
      "shin_window_dimensions": [
        0.016,
        0.01,
        0.012
      ],
      "shin_window_center": [
        0,
        0.0035,
        -0.023
      ],
      "shin_corner_dimensions": [
        0.006,
        0.008,
        0.012
      ],
      "shin_corner_offset_from_ankle": [
        0.005,
        0.003,
        0.014
      ],
      "foot_rib_dimensions": [
        0.012,
        0.004,
        0.014
      ],
      "foot_rib_center": [
        -0.007,
        0.0085,
        -0.017
      ],
      "torso_window_dimensions": [
        0.01,
        0.042,
        0.024
      ],
      "torso_window_center_z": 0.002,
      "torso_brace_dimensions": [
        0.016,
        0.006,
        0.008
      ],
      "torso_brace_x": -0.014,
      "torso_brace_hip_inset": 0.007,
      "torso_brace_z": -0.018
    }
  },
  "bodies": [
    {
      "name": "torso",
      "parent": "world",
      "position": [
        0,
        0,
        0.15624038765061038
      ],
      "joint": "root",
      "axis": null,
      "components": [
        {
          "name": "torso_frame",
          "mass": 0.021943447742229213,
          "dimensions": [
            0.0335,
            0.082,
            0.08875
          ],
          "com": [
            -0.016315678648651345,
            1.0213107951874343e-18,
            -0.004845964988835626
          ],
          "inertia_tensor": [
            [
              2.6798224543308287e-05,
              -7.858597316502908e-22,
              2.16987487325085e-06
            ],
            [
              -7.858597316502908e-22,
              1.3620713899047003e-05,
              -6.688803109154264e-22
            ],
            [
              2.16987487325085e-06,
              -6.688803109154264e-22,
              1.5916424309425935e-05
            ]
          ],
          "material": "solid PETG estimate, 1270 kg/m\u00b3",
          "evidence": "generated CAD; actual infill/printed density must be weighed",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            }
          }
        },
        {
          "name": "pico",
          "mass": 0.003,
          "dimensions": [
            0.0035,
            0.051,
            0.021
          ],
          "com": [
            -0.01075,
            0,
            0.023
          ],
          "material": "bare Pico PCB/components, headers separately owned",
          "evidence": "PCB51x21mm sourced;3g/3.5mm populated envelope and placement estimated",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "PCB51x21mm sourced;3g/3.5mm populated envelope and placement estimated"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "PCB51x21mm sourced;3g/3.5mm populated envelope and placement estimated"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "PCB51x21mm sourced;3g/3.5mm populated envelope and placement estimated"
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
        },
        {
          "name": "left_hip_ear_bolt_-1",
          "mass": 0.00055,
          "dimensions": [
            0.005,
            0.008,
            0.005
          ],
          "com": [
            0,
            0.027000000000000003,
            -0.048749999999999995
          ],
          "material": "steel, M2x8 screw + nut +2washers",
          "evidence": "sourced hardware dimensions; installed pose, mass and box inertia estimated",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            }
          }
        },
        {
          "name": "left_hip_ear_bolt_+1",
          "mass": 0.00055,
          "dimensions": [
            0.005,
            0.008,
            0.005
          ],
          "com": [
            0,
            0.027000000000000003,
            -0.020749999999999998
          ],
          "material": "steel, M2x8 screw + nut +2washers",
          "evidence": "sourced hardware dimensions; installed pose, mass and box inertia estimated",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            }
          }
        },
        {
          "name": "right_hip_ear_bolt_-1",
          "mass": 0.00055,
          "dimensions": [
            0.005,
            0.008,
            0.005
          ],
          "com": [
            0,
            -0.027000000000000003,
            -0.048749999999999995
          ],
          "material": "steel, M2x8 screw + nut +2washers",
          "evidence": "sourced hardware dimensions; installed pose, mass and box inertia estimated",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            }
          }
        },
        {
          "name": "right_hip_ear_bolt_+1",
          "mass": 0.00055,
          "dimensions": [
            0.005,
            0.008,
            0.005
          ],
          "com": [
            0,
            -0.027000000000000003,
            -0.020749999999999998
          ],
          "material": "steel, M2x8 screw + nut +2washers",
          "evidence": "sourced hardware dimensions; installed pose, mass and box inertia estimated",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            }
          }
        },
        {
          "name": "pico_header_0",
          "mass": 0.0006,
          "dimensions": [
            0.011,
            0.0508,
            0.00254
          ],
          "com": [
            -0.01,
            0,
            0.01411
          ],
          "material": "20pin 2.54mm header",
          "evidence": "RPIP-PINH11mm overall pin height sourced; row footprint/position/mass estimated; verify solder projection and jumper access",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Header1x20 2.54mm pitch;11mm overall pin length; actual board fit unmeasured"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Header1x20 2.54mm pitch;11mm overall pin length; actual board fit unmeasured"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Header1x20 2.54mm pitch;11mm overall pin length; actual board fit unmeasured"
            }
          }
        },
        {
          "name": "pico_header_1",
          "mass": 0.0006,
          "dimensions": [
            0.011,
            0.0508,
            0.00254
          ],
          "com": [
            -0.01,
            0,
            0.03189
          ],
          "material": "20pin 2.54mm header",
          "evidence": "RPIP-PINH11mm overall pin height sourced; row footprint/position/mass estimated; verify solder projection and jumper access",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Header1x20 2.54mm pitch;11mm overall pin length; actual board fit unmeasured"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Header1x20 2.54mm pitch;11mm overall pin length; actual board fit unmeasured"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Header1x20 2.54mm pitch;11mm overall pin length; actual board fit unmeasured"
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
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-24",
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
          "name": "left_knee_ear_bolt_-1",
          "mass": 0.00055,
          "dimensions": [
            0.005,
            0.008,
            0.005
          ],
          "com": [
            0,
            -0.007,
            -0.06875
          ],
          "material": "steel, M2x8 screw + nut +2washers",
          "evidence": "sourced hardware dimensions; installed pose, mass and box inertia estimated",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            }
          }
        },
        {
          "name": "left_knee_ear_bolt_+1",
          "mass": 0.00055,
          "dimensions": [
            0.005,
            0.008,
            0.005
          ],
          "com": [
            0,
            -0.007,
            -0.04075
          ],
          "material": "steel, M2x8 screw + nut +2washers",
          "evidence": "sourced hardware dimensions; installed pose, mass and box inertia estimated",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            }
          }
        },
        {
          "name": "left_hip_horn_hardware",
          "mass": 0.0012,
          "dimensions": [
            0.02,
            0.005,
            0.026
          ],
          "com": [
            0,
            0.0035,
            0
          ],
          "material": "factory horn +retainer +2frame screws/washers",
          "evidence": "unknown interfaces; estimated1.2g allowance, NOT a collision envelope",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "weigh/measure actual horn and screw set; do not use allowance as exact geometry"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "weigh/measure actual horn and screw set; do not use allowance as exact geometry"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "weigh/measure actual horn and screw set; do not use allowance as exact geometry"
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
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            }
          }
        },
        {
          "name": "left_knee_horn_hardware",
          "mass": 0.0012,
          "dimensions": [
            0.02,
            0.005,
            0.026
          ],
          "com": [
            0,
            0.0035,
            0
          ],
          "material": "factory horn +retainer +2frame screws/washers",
          "evidence": "unknown interfaces; estimated1.2g allowance, NOT a collision envelope",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "weigh/measure actual horn and screw set; do not use allowance as exact geometry"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "weigh/measure actual horn and screw set; do not use allowance as exact geometry"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "weigh/measure actual horn and screw set; do not use allowance as exact geometry"
            }
          }
        },
        {
          "name": "left_ankle_horn_hardware",
          "mass": 0.0012,
          "dimensions": [
            0.005,
            0.02,
            0.026
          ],
          "com": [
            0.0035,
            0,
            -0.05
          ],
          "material": "factory horn +retainer +2frame screws/washers",
          "evidence": "unknown interfaces; estimated1.2g allowance, NOT a collision envelope",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "weigh/measure actual horn and screw set; do not use allowance as exact geometry"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "weigh/measure actual horn and screw set; do not use allowance as exact geometry"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "weigh/measure actual horn and screw set; do not use allowance as exact geometry"
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
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "generated CAD; actual infill/printed density must be weighed"
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
          "name": "left_foot_pad_0",
          "mass": 0.00023561944901923448,
          "dimensions": [
            0.01,
            0.01,
            0.003
          ],
          "com": [
            -0.031,
            -0.0145,
            -0.025500000000000002
          ],
          "inertia_tensor": [
            [
              1.6493361431346417e-09,
              0,
              0
            ],
            [
              0,
              1.6493361431346417e-09,
              0
            ],
            [
              0,
              0,
              2.9452431127404312e-09
            ]
          ],
          "primitive": "cylinder_z",
          "radius": 0.005,
          "material": "TPE + supplied adhesive",
          "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "dimensions": {
              "state": "sourced",
              "date": "2026-10-24",
              "evidence": "https://www.delock.com/produkt/18309/pdf.html?sprache=de"
            }
          }
        },
        {
          "name": "left_foot_pad_1",
          "mass": 0.00023561944901923448,
          "dimensions": [
            0.01,
            0.01,
            0.003
          ],
          "com": [
            -0.031,
            0.0145,
            -0.025500000000000002
          ],
          "inertia_tensor": [
            [
              1.6493361431346417e-09,
              0,
              0
            ],
            [
              0,
              1.6493361431346417e-09,
              0
            ],
            [
              0,
              0,
              2.9452431127404312e-09
            ]
          ],
          "primitive": "cylinder_z",
          "radius": 0.005,
          "material": "TPE + supplied adhesive",
          "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "dimensions": {
              "state": "sourced",
              "date": "2026-10-24",
              "evidence": "https://www.delock.com/produkt/18309/pdf.html?sprache=de"
            }
          }
        },
        {
          "name": "left_foot_pad_2",
          "mass": 0.00023561944901923448,
          "dimensions": [
            0.01,
            0.01,
            0.003
          ],
          "com": [
            0.043,
            -0.0145,
            -0.025500000000000002
          ],
          "inertia_tensor": [
            [
              1.6493361431346417e-09,
              0,
              0
            ],
            [
              0,
              1.6493361431346417e-09,
              0
            ],
            [
              0,
              0,
              2.9452431127404312e-09
            ]
          ],
          "primitive": "cylinder_z",
          "radius": 0.005,
          "material": "TPE + supplied adhesive",
          "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "dimensions": {
              "state": "sourced",
              "date": "2026-10-24",
              "evidence": "https://www.delock.com/produkt/18309/pdf.html?sprache=de"
            }
          }
        },
        {
          "name": "left_foot_pad_3",
          "mass": 0.00023561944901923448,
          "dimensions": [
            0.01,
            0.01,
            0.003
          ],
          "com": [
            0.043,
            0.0145,
            -0.025500000000000002
          ],
          "inertia_tensor": [
            [
              1.6493361431346417e-09,
              0,
              0
            ],
            [
              0,
              1.6493361431346417e-09,
              0
            ],
            [
              0,
              0,
              2.9452431127404312e-09
            ]
          ],
          "primitive": "cylinder_z",
          "radius": 0.005,
          "material": "TPE + supplied adhesive",
          "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "inertia_tensor": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "sourced Delock18309 dimensions;1000kg/m3 density and homogeneous-cylinder inertia are estimates"
            },
            "dimensions": {
              "state": "sourced",
              "date": "2026-10-24",
              "evidence": "https://www.delock.com/produkt/18309/pdf.html?sprache=de"
            }
          }
        },
        {
          "name": "left_ankle_ear_bolt_-1",
          "mass": 0.00055,
          "dimensions": [
            0.008,
            0.005,
            0.005
          ],
          "com": [
            -0.007,
            0,
            -0.01875
          ],
          "material": "steel, M2x8 screw + nut +2washers",
          "evidence": "sourced hardware dimensions; installed pose, mass and box inertia estimated",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            }
          }
        },
        {
          "name": "left_ankle_ear_bolt_+1",
          "mass": 0.00055,
          "dimensions": [
            0.008,
            0.005,
            0.005
          ],
          "com": [
            -0.007,
            0,
            0.009250000000000001
          ],
          "material": "steel, M2x8 screw + nut +2washers",
          "evidence": "sourced hardware dimensions; installed pose, mass and box inertia estimated",
          "parameter_evidence": {
            "mass": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "com": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
            },
            "dimensions": {
              "state": "estimated",
              "date": "2026-10-24",
              "evidence": "Actual ear/stack/assembly must be measured;0.55g group estimate"
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
  "revision": "S6-PETG-pad-r2",
  "updated_date": "2026-10-24",
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
    "state": "planned; electrical verification pending",
    "board": "Raspberry Pi Pico bare, user-soldered headers"
  },
  "parameter_evidence": {
    "geometry": {
      "state": "estimated",
      "date": "2026-10-24",
      "evidence": "S6-PETG-pad-r2 design, no physical fit; frame solid-CAD masses regenerated"
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
    },
    "grip_pads": {
      "state": "sourced",
      "date": "2026-10-24",
      "evidence": "https://www.delock.com/produkt/18309/pdf.html?sprache=de",
      "note": "dimensions only; density/placement/friction estimated"
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
  },
  "manufacturing": {
    "route": "commercial PETG FDM, ordinary adhesive TPE pads",
    "frame_parts": 7,
    "sample_pieces": 2,
    "state": "quotation prototype; manufacturing NOT released",
    "layer_height_mm": 0.2,
    "walls": 3,
    "infill_percent": 25,
    "printed_soles": false,
    "mechanical_stops": "unknown, omitted",
    "measurements_required": [
      "servo ear spacing/holes/thickness and case axial location",
      "shaft height, spline, supplied horn shape/hole radii/thickness",
      "retaining-screw thread/length; horn-to-frame screw thread/length",
      "lead exit and connector mating; installed screw/tool sweeps",
      "sample insertion fit and actual printed hole diameters",
      "printed masses/layer strength, pad friction/adhesion",
      "Pico header11mm pin envelope, PCB stand-off fit and Dupont/cable clearances"
    ]
  },
  "hardware_interfaces": {
    "ear_bolt": {
      "screw": "P010265 M2x8 DIN7985",
      "shaft_diameter": 0.002,
      "length_under_head": 0.008,
      "head_diameter": 0.004,
      "head_height": 0.0016,
      "nut": "P003474 M2 DIN934",
      "nut_across_flats": 0.004,
      "nut_height": 0.0016,
      "washer": "P004198 DIN125",
      "washer_id": 0.0022,
      "washer_od": 0.005,
      "washer_thickness": 0.0003,
      "ear_thickness_estimate": 0.0014,
      "dimensions_state": "sourced; screw/nut/washer product dimensions",
      "placement_state": "estimated; actual ear/stack must be measured",
      "sources": [
        "https://www.schraubenking-shop.de/M2-x-8mm-Linsenkopfschrauben-PH-DIN7985-Stahl-verzinkt-FKL48-P010265",
        "https://www.schraubenking-shop.de/M2-Sechskantmuttern-DIN934-Stahl-verzinkt-FKL8-P003474",
        "https://www.schraubenking-shop.de/22mm-Unterlegscheiben-DIN125-Edelstahl-A2-P004198"
      ]
    },
    "horn": {
      "quantity": 6,
      "retainers": 6,
      "frame_screws": 12,
      "frame_washers": 12,
      "spline": null,
      "retainer_thread": null,
      "retainer_length": null,
      "horn_hole_radii": null,
      "frame_screw_thread": null,
      "frame_screw_length": null,
      "state": "unknown; factory batch, no generic25T/guessed threads",
      "designed_slot_radius_interval": [
        0.0055,
        0.0125
      ],
      "designed_frame_clearance_width": 0.0024
    }
  }
}
```

## 8. Wiring/power architecture and bench protocol

### Native-PWM S6 hardware and protocol

Updated 2026-10-24. Implemented source and local compilation are distinct from
physical verification: **nothing has been purchased or electrically tested**.
The selected *provisional quotation revision* is bare Pico native PWM, six Waveshare15024
MG90S, MPU6050 and Mean Well GST40A05-P1J. PCA9685 is not in the current basket.
Its listing is unavailable and removing it resolves the original board/brace overlap.

#### Power and self-soldered harness

PC USB powers Pico and IMU. Enclosed 5V/5A PSU, including separately priced
Schuko–C13 mains lead, powers ONLY the servo bus. Never connect servo5V to Pico
VBUS/VSYS/3V3, or route servo current through GPIO jumpers or a breadboard.
Join logic ground to the short heavy servo-return bus once. Mains wiring remains
inside the commercial PSU/lead. Capacitor1000µF/16V goes across the bus with
correct polarity; it is not a substitute for an adequate supply.

The proposed basket uses a **bare Pico** with user-soldered headers. Existing RP2040
firmware/pins remain unchanged. The model now separately owns estimated3g bare PCB
and two0.6g header rows (4.2g together). Header overall pin length11mm is sourced;
PCB/USB envelope and all masses/placements still need measurement.
Compare Pico H5.50 +one40pin pack0.60 with bare4.10 +header kit0.50 +40pin pack0.60:
header-inclusive saving0.90. Kit2x20pins +40pin pack supply80functional pins,
54used,26spare; supplied3pin SWD strip is extra spare. Solder10g flux-core, heat-shrink, ties and wire are priced robot
consumables. Iron access is available; other tools must be confirmed/borrowed or
priced outside the robot cap but inside initial cash. No mandatory paid helper.

**Prepare unpowered, with the PSU disconnected from mains and DC, and USB removed:**

1. Solder two20pin rows to the bare Pico and the needed IMU header; inspect bridges.
   Keep IMU I2C/ground leads short. Sensor pull-ups and VCC must be3.3V.
2. For each of six10cm JR extensions, identify the factory connector that mates to
   the actual servo cable; preserve it for replaceability. Do not trust connector
   gender names or wire colours: verify end-to-end continuity and pin order first.
3. Remove the unused extension end and expose only short conductor lengths. Solder
   each positive/return branch separately onto short0.75mm² positive/negative buses.
   Keep each bus section to about10cm; stagger splices, insulate individually, then
   add overall strain relief. Mark the negative red-wire bus with black shrink at
   every exposed end. Connector/wire ratings remain a required acceptance test.
4. Bring each isolated signal to a separate insulated header/jumper and its Pico GPIO.
   No positive servo wire connects to the Pico. Join servo-bus return to Pico GND
   with one logic-reference lead; high-current return goes straight to the PSU.
   Use separate GND pins for IMU and servo reference (e.g.physical38and3).
5. Solder DC socket positive/return and the1000µF capacitor across the bus; verify
   socket polarity with a meter and the capacitor's negative stripe. Insulate all
   socket lugs and metal that could short, secure it off-robot, and strain-relieve
   the tether. No bare solder joint may reach frame/PCB/another conductor.
6. With no servo connected, check shorts/continuity, then energize the commercial
   enclosed PSU and measure centre-positive5V at each branch. Disconnect it before
   connecting one unloaded servo. Verify current/droop, connector heating and3.3V
   PWM compatibility before expanding to six. Never work on the mains internals.

Use ventilation, a stable iron stand and eye protection while clipping leads;
keep hot tools away from insulation/boards. Do not solder powered electronics.
No breadboard or thin Dupont wire carries servo supply current. Self-soldering is
not evidence of an electrically qualified harness; bench data is still required.

Estimated average six-servo current0.6–1.5A, assumed peak4.8A (6×0.8A), plus
logic below0.15A on USB. **Selected-servo current is unknown**; these are sizing
hypotheses. A5A PSU offers little peak margin; measure droop/current before six
servos. At4.8A, 20cm total0.75mm² copper loop drops~0.022V, excluding connectors,
PSU lead and branches. A2m one-way tether of this wire drops~0.45V and is not
acceptable. Use the PSU's existing lead and slack loop for the initial0.3m trial;
several metres need a newly sourced thicker tether/longer USB cable and budget.
1000µF stores only~0.04ms at4.8A for0.2V droop. Measure4.8–6V at the farthest
loaded servo and check connector temperature.

Accessible full-current DC unplug is the physical emergency cutoff. Selected
provisional input: [Goobay11638,EUR1.10](https://www.berrybase.de/dc-einbaubuchse-fuer-hohlstecker-5-5x2-1mm-metallausfuehrung-loetanschluss),
5.5×2.1mm solder socket with nut/washer; retailer specifies5A/30V DC. Replaces the
unpriced Delock pigtail. User solders short0.75mm² bus leads, separately insulates
lugs and outer metal, and secures strain relief with listed shrink/ties. Support this
connection off robot. Verify centre-positive continuity and insulation before power.
No exposed low-voltage metal may short to boards/fasteners. No mains modification.
JR branch gauge/contacts and actual servo current still require confirmation.
Socket rating is not a complete harness or bench approval. Unrated Goobay76743
is not accepted as5A. STOP/PWM silence **does not disconnect motor power**;
a servo may hold its last position. Always disarm before reconnecting DC.

USB-A–Micro-B data cable connects Pico directly to a USB-A PC; **no extra adapter**
in base basket. Only a PC without USB-A needs a separately sourced data adapter.
Available50cm Dupont pack replaces unavailable20cm; user keeps I2C wiring short
and secures excess. No servo supply current in any Dupont jumper.

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
| IMU GND |GND|38|
| Short common servo ground reference |GND|3|

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

### Pico firmware — local build and bench preparation

**Frame/control identity update2026-10-24:** proposed bare Pico uses the same RP2040 firmware
and GPIOs as Pico H. User fits headers and a self-soldered insulated harness; no
mandatory helper labour. See [wiring sequence](../docs/HARDWARE.md). Do not flash/arm
this as proof of electrical or mechanical verification. Current provisional twin uses bare Pico+two soldered header rows. Module mass
is estimated4.2g; actual board/harness measurements remain pending. The generated
invalid header now carries the r2 fingerprint. OldUF2 images are historical: rebuild
with this header and later measured calibration before any flash. No current ARM
build or physical electrical result is claimed by the geometry update.


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
    <body name="torso" pos="0 0 0.1562403877">
      <geom name="torso_visual" type="mesh" mesh="torso_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
      <inertial mass="0.07574344774" pos="-0.006320972389 3.578534529e-19 -0.01029907144" fullinertia="8.148312538e-05 5.344089513e-05 4.48989327e-05 -6.368545737e-22 7.760571147e-06 -8.856730812e-22" />
      <freejoint name="root" />
      <geom name="torso_collision" type="box" pos="0 0 0.01" size="0.02 0.041 0.025" rgba="0.10 0.45 0.8 0.8" />
      <site name="imu_site" pos="-0.0255 0 0.018" size="0.003" rgba="1 0.7 0 1" />
      <camera name="overview" pos="0.42 -0.5 0.24" xyaxes="0.766 0.643 0 -0.26 0.31 0.916" />
      <geom name="left_hip_servo_case" type="box" pos="0 0.01975 -0.03475" size="0.0061 0.01425 0.0114" rgba="0.15 0.15 0.17 1" />
      <geom name="right_hip_servo_case" type="box" pos="0 -0.01975 -0.03475" size="0.0061 0.01425 0.0114" rgba="0.15 0.15 0.17 1" />
      <body name="left_thigh" pos="0 0.034 -0.03">
        <geom name="left_thigh_visual" type="mesh" mesh="left_thigh_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
        <inertial mass="0.01977302956" pos="7.08385379e-20 -0.009228983103 -0.04336712372" fullinertia="1.201338719e-05 1.06953106e-05 2.361686476e-06 -1.292696745e-23 9.290620081e-24 -2.750783224e-06" />
        <joint name="left_hip" type="hinge" axis="0 1 0" />
        <geom name="left_thigh_link" type="capsule" fromto="0 0 -0.006 0 0 -0.044" size="0.006" rgba="0.12 0.55 0.83 1" />
        <geom name="left_knee_servo_case" type="box" pos="0 -0.01425 -0.05475" size="0.0061 0.01425 0.0114" rgba="0.15 0.15 0.17 1" />
        <body name="left_shin" pos="0 0 -0.05">
          <geom name="left_shin_visual" type="mesh" mesh="left_shin_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
          <inertial mass="0.008623103503" pos="0.001769592628 0.002022456737 -0.02519082456" fullinertia="5.202857017e-06 5.271289455e-06 4.593362007e-07 2.259577502e-08 3.37397356e-07 -3.106646077e-07" />
          <joint name="left_knee" type="hinge" axis="0 1 0" />
          <geom name="left_shin_link" type="capsule" fromto="0 0 -0.006 0 0 -0.044" size="0.006" rgba="0.12 0.55 0.83 1" />
          <body name="left_foot" pos="0 0 -0.05">
            <geom name="left_foot_visual" type="mesh" mesh="left_foot_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
            <inertial mass="0.03225878756" pos="-0.003143726384 1.312871641e-20 -0.01408134211" fullinertia="6.690079177e-06 1.906430994e-05 1.860375222e-05 -7.946502952e-23 2.654014327e-06 1.523359921e-22" />
            <joint name="left_ankle" type="hinge" axis="1 0 0" />
            <geom name="left_foot_plate" type="box" pos="0.006 0 -0.0225" size="0.045 0.0225 0.0015" rgba="0.08 0.36 0.65 1" />
            <geom name="left_foot_pad_0" type="cylinder" pos="-0.031 -0.0145 -0.0255" size="0.005 0.0015" rgba="0.15 0.15 0.15 1" />
            <geom name="left_foot_pad_1" type="cylinder" pos="-0.031 0.0145 -0.0255" size="0.005 0.0015" rgba="0.15 0.15 0.15 1" />
            <geom name="left_foot_pad_2" type="cylinder" pos="0.043 -0.0145 -0.0255" size="0.005 0.0015" rgba="0.15 0.15 0.15 1" />
            <geom name="left_foot_pad_3" type="cylinder" pos="0.043 0.0145 -0.0255" size="0.005 0.0015" rgba="0.15 0.15 0.15 1" />
            <site name="left_foot_contact_center" pos="0.006 0 -0.027" size="0.001" />
            <geom name="left_ankle_servo_case" type="box" pos="-0.01425 0 -0.00475" size="0.01425 0.0061 0.0114" rgba="0.15 0.15 0.17 1" />
          </body>
        </body>
      </body>
      <body name="right_thigh" pos="0 -0.034 -0.03">
        <geom name="right_thigh_visual" type="mesh" mesh="right_thigh_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
        <inertial mass="0.01977302956" pos="7.08385379e-20 0.009228983103 -0.04336712372" fullinertia="1.201338719e-05 1.06953106e-05 2.361686476e-06 1.292696745e-23 9.290620081e-24 2.750783224e-06" />
        <joint name="right_hip" type="hinge" axis="0 1 0" />
        <geom name="right_thigh_link" type="capsule" fromto="0 0 -0.006 0 0 -0.044" size="0.006" rgba="0.12 0.55 0.83 1" />
        <geom name="right_knee_servo_case" type="box" pos="0 0.01425 -0.05475" size="0.0061 0.01425 0.0114" rgba="0.15 0.15 0.17 1" />
        <body name="right_shin" pos="0 0 -0.05">
          <geom name="right_shin_visual" type="mesh" mesh="right_shin_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
          <inertial mass="0.008623103503" pos="0.001769592628 -0.002022456737 -0.02519082456" fullinertia="5.202857017e-06 5.271289455e-06 4.593362007e-07 -2.259577502e-08 3.37397356e-07 3.106646077e-07" />
          <joint name="right_knee" type="hinge" axis="0 1 0" />
          <geom name="right_shin_link" type="capsule" fromto="0 0 -0.006 0 0 -0.044" size="0.006" rgba="0.12 0.55 0.83 1" />
          <body name="right_foot" pos="0 0 -0.05">
            <geom name="right_foot_visual" type="mesh" mesh="right_foot_mesh" contype="0" conaffinity="0" group="2" rgba="0.12 0.55 0.83 1" />
            <inertial mass="0.03225878756" pos="-0.003143726384 -1.312871641e-20 -0.01408134211" fullinertia="6.690079177e-06 1.906430994e-05 1.860375222e-05 7.946502952e-23 2.654014327e-06 -1.523359921e-22" />
            <joint name="right_ankle" type="hinge" axis="1 0 0" />
            <geom name="right_foot_plate" type="box" pos="0.006 0 -0.0225" size="0.045 0.0225 0.0015" rgba="0.08 0.36 0.65 1" />
            <geom name="right_foot_pad_0" type="cylinder" pos="-0.031 0.0145 -0.0255" size="0.005 0.0015" rgba="0.15 0.15 0.15 1" />
            <geom name="right_foot_pad_1" type="cylinder" pos="-0.031 -0.0145 -0.0255" size="0.005 0.0015" rgba="0.15 0.15 0.15 1" />
            <geom name="right_foot_pad_2" type="cylinder" pos="0.043 0.0145 -0.0255" size="0.005 0.0015" rgba="0.15 0.15 0.15 1" />
            <geom name="right_foot_pad_3" type="cylinder" pos="0.043 -0.0145 -0.0255" size="0.005 0.0015" rgba="0.15 0.15 0.15 1" />
            <site name="right_foot_contact_center" pos="0.006 0 -0.027" size="0.001" />
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
    <key name="home" qpos="0 0 0.1562403877 1 0 0 0 -0.1745329252 0.1745329252 0 -0.1745329252 0.1745329252 0" ctrl="-0.1745329252 0.1745329252 0 -0.1745329252 0.1745329252 0" />
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
        self.foot_plate_ids = [self.model.geom(s + "_foot_plate").id for s in ("left", "right")]
        self.foot_geom_groups = [set([self.foot_plate_ids[i]] + [self.model.geom(f"{side}_foot_pad_{j}").id for j in range(4)])
                                 for i, side in enumerate(("left", "right"))]
        self.foot_ids = set.union(*self.foot_geom_groups)
        self.foot_center_sites = [self.model.site(s + "_foot_contact_center").id for s in ("left", "right")]
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
                    if other in self.foot_geom_groups[i]:
                        contacts[i] = True
        return contacts, bad_contact

    def _minimum_foot_height(self, foot_index):
        heights = []
        for gid in self.foot_geom_groups[foot_index]:
            zaxis = self.data.geom_xmat[gid].reshape(3, 3)[2]
            size = self.model.geom_size[gid]
            if self.model.geom_type[gid] == mujoco.mjtGeom.mjGEOM_CYLINDER:
                # Exact support function of a rotated finite cylinder.
                extent = size[0] * np.linalg.norm(zaxis[:2]) + size[1] * abs(zaxis[2])
            else:
                extent = np.dot(np.abs(zaxis), size)
            heights.append(self.data.geom_xpos[gid, 2] - extent)
        # All pads AND the plate must clear; a raised toe/one pad is insufficient.
        return float(min(heights))

    def _record_steps(self, contacts):
        load = np.zeros(2)
        force = np.zeros(6)
        for index, contact in enumerate(self.data.contact):
            if self.floor_id not in (contact.geom1, contact.geom2):
                continue
            other = contact.geom2 if contact.geom1 == self.floor_id else contact.geom1
            for i in range(2):
                if other in self.foot_geom_groups[i]:
                    mujoco.mj_contactForce(self.model, self.data, index, force)
                    load[i] += max(0, force[0])
        supported = load >= .10 * self.model.body_mass.sum()*9.81
        self.gait.update(self.data.site_xpos[self.foot_center_sites],
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


def show_physical_geometry(model):
    """Hide overlapping proxy drawings only; their contact physics is unchanged."""
    for i in range(model.ngeom):
        name=model.geom(i).name
        if name=='torso_collision' or name.endswith(('_link','_foot_plate')):
            model.geom_rgba[i,3]=0


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
    if mode is not None:
        show_physical_geometry(env.model)
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
        summary["evaluation_source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        summary["visualization"] = "physical CAD/servo cases/pads; overlapping proxy drawings hidden, contacts unchanged" if mode else None
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


#### r2 mass ownership and aggregate allowances

The bare Pico PCB and two GPIO headers are separate ledger components (3g +0.6g
+0.6g estimates). Each foot owns its four pads and ankle case; each shin owns
both knee and ankle output-horn hardware. Case-ear bolts belong to the case's body.
The torso20g `torso_wires_fasteners` allowance is for additional harness/capacitor/
nylon tie/restraint hardware, excluding separately owned servos, Pico headers,
named M2ear assemblies and horn sets. It is not a measured component inventory;
verify the actual harness/connector distribution and replace this allowance.
No extra pull-up purchase is assumed: verify the chosen IMU/Pico I2C wiring on
bench, and add any required components/cost if the module lacks suitable pull-ups.

When weighing an assembled rigid body, do not add that complete weight on top of
its existing components. Either replace the complete body's ledger accounting,
or weigh/subtract each known component and replace the remaining allowance.
Never run solid-CAD mass synchronization over measured masses. Recompute COM and
inertia and issue a new fingerprint before training or deployment.

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
Finite sampled clearances do not prove all continuous paths. Dimensioned M2hardware at estimated
positions has no sampled modeled collision; five unknown interface groups still block manufacture. No physical hardware
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
| A / 1 | AI: active commercial PETG quotation, complete sample/frame finishing and delivered costs; soldered electronics/ordinary pads; no purchases/messages | Complete sourced basket <=EUR100, fit information or explicit unresolved evidence/shortfall |
| B / 1,2 | AI: reconcile CAD and physical ledger, PCB/case/frame clearance, fasteners; user/supplier: sample fit | Checked geometry; no unverified manufacturing release; solid masses remain estimates |
| C / 3,8 | AI: Pico SDK C++ firmware, PC bench/client, bounded protocol and persistent calibration | Firmware builds and host tests pass; actual electrical timing/cutoff still needs bench |
| D / 2,3,4,9 | AI: common limits/preprocessing, realistic command scheduling, reward and metrics; user: measured parameters | Reproducible twin; no fake stops/positive closed-loop progress/sliding success; measured vs provisional explicit |
| E / 5,6,7 | AI: bounded nominal pilot, equal-budget fixed/DR models, held-out evaluation and videos | Actual gait results, including failures, with fingerprints and complete per-episode metrics |
| F / 8,9,10,11,13 | User: bench, assembly, calibration and physical trials; AI: firmware/tools/data analysis/report | Real test data; frozen compatible policies; equal trials and alternating A/B order |
| Extensions / 12 | Future: turning, terrain, recovery | Stable baseline walking first; no automatic scope expansion |

Current checkpoint: quotation CAD and matching r2 twin implemented; real fit,
strength and complete delivered quotation remain blocked. Common95.81EUR plus
priced ear hardware/delivery9.53EUR already exceeds100EUR by5.34EUR before printing.
Next human action: authorize exact current-STL quotation upload toMeltlab or return
its quote/settings/hashes; no order/message. Then actual servo/horn measurements and
sample fit are required. Current37tests and2048step smoke are local evidence only.
The script still produces no qualifying lift; do not expand training to hide that.

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
2. User solders/insulates short harness and headers; checks cutoff, one servo and IMU.
3. Record pulse mapping, directions, range, speed/strength/current/latency and IMU noise.
4. Confirm printed mounting sample on actual servo/horn, review layer/fastener
   clearance and complete delivered budget, then obtain frame and weigh bodies.
5. Validate all six joints, manual stand, watchdog, faults and cables.
6. Reconcile measured twin and configuration identity; retrain incompatible policies.
7. Policy stand, short steps, longer trials; use ruler/video, never IMU double integration.
8. Equal fixed/DR trials, alternating order, logs and failure records; school report.

When quotations or measurements block a stage, name the missing evidence and prepare
the precise question/data template. Continue independent software preparation. Do not
invent a quote or substitute simulation verification for physical verification.

### Current project status — 2026-10-24

Start with SUMMARY.md and AGENTS.md. **Nothing bought, printed, assembled, flashed
or physically verified.** Active revision:**S6-PETG-pad-r2**, outsourced PETG.

| Stage | State | Evidence / blocker |
|---|---|---|
| Requirements / AI entry | implemented | Six joints,15–20cm,PC/USB,wired power,EUR100retained; no printer purchase |
| Hardware research / budget | blocked | Common95.81 +ear-hardware delivery9.53 =105.34before prints/sample/horns;5.34over cap. Updated ledger/source dates |
| CAD / order preparation | implemented, locally verified partial | Seven connected watertightPETGmeshes; two-piece sample ZIP, seven-piece frame ZIP, drawings/manifests/fastener schedule.0modeled collisions/55poses;5unknown fit groups; NOT manufacture-approved |
| Shared control / firmware | locally verified partial | Existing GPIO/protocol retained; invalid current header/nativeC++tests pass. ARMbuild from previous revision is historical; physical timing/calibration absent |
| Provisional MuJoCo / Gym | locally verified | New barePico/header ownership,8TPEpad contacts,estimated197.053g,axes/inertias/contacts/reward/provenance checked;37tests pass |
| Manual reference | blocked |46s reference +three bounded ankle variants:zero qualifying lifts/steps; strength/plant assumptions unmeasured |
| PPO / evaluation | locally verified smoke only | New2048steps A0, reload/CSV/validation/video;0success/0gait under nominal/randomized validation. No larger run |
| Physical build / calibration / transfer | planned, blocked | No hardware. Bench/soldering/sample/assembly/calibration procedures ready; requires user measurements and budget/fit clearance |
| Formal A/B / school experiment | planned, blocked | No current full six-run experiment or real trials. Exact seeds/budgets remain in roadmap |
| Extensions | planned | Only after stable walking |

#### Current architecture

Six exact Waveshare15024MG90S; Lhip/knee pitch/ankle roll, then Rsame.50Hz policy
and directPicoPWM,200Hz MPU6050,2ms MuJoCo. Bare Pico PCB plus two header rows;
header11mm envelope retained. Separate USB logic and5V/5A servo bus, common ground,
self-soldered replaceable harness. SevenPETG frames; four bought10×3mm TPE pads
per90×45mm foot. No printed TPU, spool/printer purchase or PCA9685.

Physical parameters are sourced/estimated/unknown in physical_spec.json, not measured.
CAD/model/accounting derive from that ledger. The policy still sees only IMU-derived
gravity/gyro, applied command acknowledgements and previous actions (90values);
no true pose, velocity, joint feedback, contacts or forces. Diagnostics/rewards may
use simulation truth. Safe command intervals are not mechanical stops.

#### Evidence and limits

- Current local report:VALIDATION_CURRENT.md; artifacts:validation/2026-10-24/print_revision/final/.
-37tests pass, including eight-pad contacts, whole-foot cylinder/plate heights,
  component ownership, alternative-budget accounting and package quantities/hashes.
- Current estimated mass197.053g. No infill-adjusted/measured mass claim.
-0modeled collisions does NOT clear physical fit: horn/screw shapes, servo ear positions,
  printed tolerances/layer strength, cables/ties/tool access remain unknown. Historical550
  proxy intersections were replaced by sourced M2shapes at estimated positions; old
  records retained, no claim of550physical fixes. Named PCB/header attachment exception only.
- HOME stands30s; manual scripts and PPO still fail lifted walking. Quasi-static HOME
  single-foot torque~0.0657Nm;2xmargin~0.1314exceeds0.08Nm model estimate. Do not
  increase torque or train longer simply to hide these failures.
- Source/config identity:`4d3b0dcbad59774b12f9c908c74446f6bf7452d5bdf34a08f07cf4271cc15019`.
  Pre-r2policies/UF2are historical and rejected by current deployment; no relabelling.
  Current2048smoke policy matches provisional twin, **not** physical calibration.
- All physical/manufacturing/formal gates remain false. Default invalid calibration
  cannot policy-arm. Software STOP does not isolate servo power.

#### Exact next task

1. Obtain **specific permission** for current STL quotation uploads toMeltlab, or have
   user return exact-file quotes. Automatic approval review blocked the upload because
   it shares design data externally without named-provider authorization. No upload,
   supplier message or purchase occurred. Public reviews exist; no new price invented.
2. Close budget and actual horn/ear/screw dimensions; test mounting sample before full
   frame. Include every finishing/sample/delivery charge. Current basket alreadyoverEUR100.
3. Measure plant/current/IMU and assemble/weigh only after approval. Update measured
   twin/version, then validate lifted steps before larger training or deployment.

```bash
.venv/bin/python -m pytest -q
.venv/bin/python tools/budget_gate.py #1, active basket over cap before prints
MPLCONFIGDIR=/tmp/s6-mpl .venv/bin/python tools/prepare_print_order.py
.venv/bin/python tools/check_clearance.py #1, unresolved interfaces
```

Human-facing instructions/packages:SUMMARY.md,cad/QUOTE_REQUEST.md,cad/ASSEMBLY.md.
Historical sources/quotes:history/2026-10-24/pre_print_revision/ and previous validation
folders. Earlier in-turn geometry results are under development_superseded/ and must
not be reported as final. No stage is physically verified without real measurement data.

### Current local verification — 2026-10-24, S6-PETG-pad-r2

**No hardware purchased, printed, fitted, electrically tested or deployed.**
Prior2026-10-23record is preserved under history/2026-10-24/pre_print_revision/docs/.
Current evidence: validation/2026-10-24/print_revision/final/; earlier in-turn
records are explicitly superseded, not final results.

#### Geometry, accounting and interface

- 37 pytest cases passed in9.69s: original32 plus five new print/pad/ownership/budget checks.
- Seven watertight connected CAD frames; solid-PETG mass properties match ledger.
- Total **197.053g estimated**, not weighed. Bare Pico3g +two0.6g headers;
  eight cylindrical10×3mm TPE pads; horn/fastener masses remain estimated.
- Sourced M2 screw/nut/washer dimensions replace old mass-proxy boxes for clearance.
 55poses: **0modeled collisions**, but **5unknown interface groups remain**.
  Exact horns/ear locations, stack/tool access, leads/ties and layer strength block release.
  Intentional PCB/header attachment is the sole named collision exclusion.
- No unknown mechanical stops in MJCF. Six pitch/pitch/roll hinges; safe commands
  are software bounds. Eight pad contacts and plate checked for whole-foot lift;
  test compares rotated-cylinder/box minimum heights to independently transformed meshes.
- Gym/SB3 API, seeded resets, nominal restoration/inertia scaling, noisy IMU-only
  observations, delay/clipping/slew/quantization, finite neutral/random/limit commands,
  reward/gait exploit tests and native C++ control tests pass.
-30s HOME remains upright with both feet contacting; neutral video seed2000,
  distance0.00002723m, no fall, zero gait. Standing is not learned walking.
- Firmware invalid calibration header regenerated for current identity. No new ARM
  firmware build/UF2/electrical test claimed. Rebuild before flash; historicalUF2is incompatible.

#### Motion diagnosis and strength

Original46s reference and three18s bounded stance/swing ankle variants completed
without a qualifying step. Maximum whole-foot clearances stayed below0.000005m,
versus required0.003m for0.04s. Logged actual/applied angles, roll and actuator torque;
CSV and summary retained. Model torque remains0.08Nm; no inflated strength/gains.

Quasi-static entire-weight-on-left-foot estimates: HOME~0.0657Nm maximum;
lean~0.0338Nm; lifted-right pose~0.0321Nm; deep-bend stress~0.0451Nm.
Twice HOME static demand~0.1314Nm exceeds current0.08Nm operating hypothesis.
This is **not** measured continuous servo capability or a proof of supported gait.
Torque margin, real plant response and the failed lifted-step sequence need diagnosis
before large PPO runs or a walking-ready physical claim.

#### Bounded PPO smoke and reload

Fresh seed0,A nominal, **2048actual timesteps**, current identity. No resume/relabel
of old checkpoints. Validation2000–2004; final1000–1009unused. Checkpoint reload
and current evaluation/video succeeded; no measured calibration or physical approval.

| Condition | Episodes | Mean distance m | Mean reward | Falls | Gait distance / success |
|---|---:|---:|---:|---:|---|
| Nominal |5|-0.02039646|5.310372|0/5|0 /0of5|
| Randomized |5|-0.02027713|5.303456|0/5|0 /0of5|

This is stationary/sliding backward drift, **not walking**. No pilot/formal A/B
training beyond this smoke was run. Preserve older49152step pilot and2048A/B
records as historical. Current smoke cannot be used on hardware without a new
measured twin/calibration, compatible training and physical checks.

Configuration fingerprint:`4d3b0dcbad59774b12f9c908c74446f6bf7452d5bdf34a08f07cf4271cc15019`.
Current source snapshot includes matching model/control files and CAD STLs.
Policy manifests record model/source/config hashes, initialization, actual steps,
validation seeds and algorithm settings. Videos are640×480,50fps; representative frames were inspected. Clean renders in
`home_clean_video` and `smoke_clean_video` hide overlapping collision-proxy drawings
only; metrics exactly match the original videos. Physics/controller identity did
not change. New rendering source hashes/copies are saved with those evaluations.
No video proves physical success.

#### Procurement and next evidence

Active priced basket105.34EUR **before** current prints/sample/horn extras; minimum
known shortfall5.34EUR for that basket. No complete quote or budget clearance.
Automatic approval review rejected uploading the revised STL toMeltlab; design
was not uploaded, no supplier message/order sent. Public example/old-geometry
prices are not new quotations. See PROCUREMENT_ACTIONS.md or procurement ledger
for the exact upload/quote/measurement requirements.

Next: provider-specific quotation upload authorization or user-returned quote;
actual servo/horn measurements; sample fit; complete budget. All physical gates false.
