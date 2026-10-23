# Procurement evidence and precise outstanding actions

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

## Questions ready for a human to send or resolve

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
