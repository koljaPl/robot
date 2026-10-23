# Frame and printer comparison — 2026-10-23

**Comparison, not a purchase selection.** User can solder; no helper labour is mandatory.
No current printer access. No printing, drilling, cutting or bending of mechanical
parts is allowed in the standard-parts route. Electrical wire preparation is allowed.
Authoritative prices/unknowns: `../procurement.json`; short plan: `../SUMMARY.md`.

## Standard ready-made mechanics

[Cytron ROBO-BK-SG90](https://www.cytron.io/p-robo-bracket-for-microservo-motor)
is a genuine 1.5 mm aluminium-alloy case bracket for the 23 × 12.2 × 29 mm
microservo family. Manufacturer lists USD2.48 and 82 in stock; pack contains
one bracket, four M2×6 and four M3×6 screws. No verified EUR landed price to25337.
Do not convert USD and omit VAT/import/shipping. The selected Waveshare case
fit is still unmeasured; this is product-family compatibility, not fit approval.

| Connection required | Evidence / missing item |
|---|---|
| Hip cases → torso crosspiece | Bracket exists; no compatible crosspiece/attachment verified |
| Hip horns → thighs → knee cases | No complete link, horn pattern or screw stack verified |
| Knee horns → shins → ankle horns | Requires perpendicular pitch/roll interfaces; no stock assembly verified |
| Ankle cases → two broad feet | No compatible ready-made feet/cradles verified |
| Horn spline/retainer/screws | Exact supplied batch and thread/geometry unknown |
| Electronics/cable restraints | Final frame attachment/clearance unknown |

A proposed six case brackets is **not** an orderable frame: count depends on the
missing topology. The complete required quantity is one verified six-joint kit,
including all links, feet, retainers and fasteners. No exact assembly instructions
can be certified before that kit exists. Conditional assembly order is in SUMMARY.
The [ACEBOTT QD021](https://acebottteam.github.io/acebott-docs-master/kit/Inventor%20Series/QD021.html)
is four-joint and rejected as a substitute. Pan/tilt holders requiring horn trimming
and printed holders do not satisfy the standard route. No fabricated adapter is hidden.

**Price:** common electronics/harness/pad subset EUR95.91, leaving EUR4.09 for
all frame hardware/delivery and other unknowns. Complete route price/shortfall unknown;
this is not proof that no cheaper basket can exist. No procurement clearance.

## Own printer, cost comparison only

| Exact printer | VAT-inclusive price | Standard DE shipping | Stock/delivery evidence | Bed |
|---|---:|---:|---|---|
| [A1 mini non-Combo BL1-101030 / PF002-M-EU](https://www.welectron.com/Bambu-Lab-A1-mini-3D-Drucker) | EUR189 | EUR0 | Exact non-Combo listed in stock, 1–3 working days |180³ mm|
| [Ender-3 V3 SE standalone](https://store.creality.com/de/products/ender-3-v3-se-3d-drucker) | EUR169 | EUR0 | EUR169 standalone order button enabled, no stock count; Oct26–30 estimate shown |220×220×250 mm|

Shipping: [Welectron](https://www.welectron.com/Zahlung-und-Versand),
[Creality](https://store.creality.com/de/pages/versand-auslieferung) (Germany free
from EUR99). These are advertised rates, not a completed25337checkout. No promised
arrival or reservation. No coupons, financing, optional insurance or bundles counted.
Ender dimensions/material support: [manufacturer](https://www.creality.com/products/creality-ender-3-v3-se).
A1 includes 0.4 mm nozzle, textured PEI plate and spool holder; no AMS needed.
Manufacturer setup guides: [A1 mini](https://wiki.bambulab.com/en/a1-mini),
[Creality support](https://www.creality.com/pages/download-ender-3-v3-se).

Count one full [SUNLU PETG black 1 kg spool SN5-314224](https://www.welectron.com/Sunlu-PETG-Black-175-mm-1000-g_1),
EUR12.99, not sample filament/refill/consumed grams. Robot known subset EUR118.43;
**EUR18.43 over cap before unknown horn hardware and print consumables**.
Printer/tools are separate: initial known cash EUR307.43(A1) or EUR287.43(Ender),
plus unresolved robot/tool expenses. Iron access confirmed; other tool access must
be confirmed/borrowed or priced. Complete initial total remains unknown.
Joint A1+servo+spool delivery could remove EUR4.95 once, subject to checkout;
conservative comparison keeps robot-only shipping. Even EUR113.48 exceeds cap.

## Sole choice and physical-model boundary

Proposed standard replacement: [Delock18309](https://www.delock.com/produkt/18309/pdf.html?sprache=de),
TPE pads, diameter10 mm,height3 mm,50pack. [Reichelt EUR3.55](https://www.reichelt.de/de/de/shop/produkt/gummifuesse_rund_selbstklebend_10_x_3_mm_50_stk_schwarz-371081)
plus [EUR5.95 standard DHL](https://www.reichelt.de/de/de/shop/service/-12_28).
Eight used, four near foot corners, avoiding screws/cradle; exact centres after
fit review. Adhesive included; friction/peel durability unmeasured. These are discrete
pads, not a 90×45 mm continuous sole; test stability and slipping before selection.
No TPU spool is budgeted. Buying TPU only for two soles is avoided in this proposal,
but no claim of equivalent contact mechanics or verified grip is made.

`physical_spec.json`, `robot.xml` and existing seven frame STLs **remain unchanged**:
Pico H, continuous1mm TPU soles and current estimated masses. A selected bare-Pico/
pad branch needs measured PCB/pad masses, foot-contact locations/height, COM/inertia,
standing-pose and torque recalculation plus new fingerprints before training/deployment.
The 199.4 g prototype estimate is not the new branch's verified weight.

## Local print preparation (not manufacturing approval)

Run `python tools/prepare_local_print.py`. `cad/local_print/layout.json` records
source hashes, rotations and bounds; each of seven unchanged parts has its own
plate with a 5 mm XY edge margin within180×180×180 mm. The historic185 mm batch
does not fit A1 mini. Do not import all plates together or use the quote batch.

1. Measure an actual servo, supplied horn and screws; revise interfaces if needed.
2. Open `FIRST_interface_sample.stl` first (two separate current-CAD interface pieces).
3. Units mm,100% scale; initial PETG settings0.2 mm layer,3walls,25%infill. Check slicer
   supports, layer load direction and every hole; these settings are hypotheses.
4. Verify actual sample fit without drilling/forcing. Failed sample means revise/reprint,
   not manufacture the full frame. Record printer/profile/tolerances.
5. Only after fit, strength, fastener clearance and complete budget approval print
   torso, two thighs, two shins and two feet, one plate at a time. Use ordinary pads.
6. Finish and inspect supports without cutting structural parts. Verify whether supplied
   print tools/plate need extra release/cleaning consumables; source them if needed.

Layout bounding-box/volume checks are local software evidence, not a slicer print,
layer-strength or hardware-fit test. Full spool covers trial material procurement;
actual consumption/support mass is unknown until slicing. No calibrated mass update.

## Recommendation / next evidence

Use self-soldering and propose bare Pico (net header-inclusive saving EUR0.80).
Retain PSU/IMU/servos. **Select neither frame route yet.** First seek an exact stock
six-joint frame with all interfaces and landed EUR price. If none meets the cap,
report that outcome; do not buy a printer or relax joints/budget automatically.
Printing becomes actionable only if access is later provided and budget/fit gates pass.
