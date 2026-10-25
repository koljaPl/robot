# Active commercial-print procurement actions — 2026-10-25

Delivery25337Germany; PCUSB-A, no adapter; required USB data cable retained.
No purchases, supplier messages, reservations or print orders have occurred.
Authoritative ledger:`../procurement.json`; packages:`../cad/`.

## Ready to forward for quotation, not order

- [Sample ZIP](../cad/sample_quotation_package.zip): two separate mounting-test pieces.
- [Frame ZIP](../cad/frame_quotation_package.zip): sevenPETG parts, no TPU soles.
- [Supplier brief](../cad/QUOTE_REQUEST.md), [drawing](../cad/print_order/drawings/interfaces.png),
  [quantity/hash manifest](../cad/print_order/manifest.json), [assembly](../cad/ASSEMBLY.md).
- A combined7component STL is an alternative calculator input only; never add it
  to the seven individual pieces as extra quantities. Hash final geometry before quote.

## Costs and reductions

Common priced subset95.56EUR +three ear-fastener packs/delivery9.53EUR =
**105.09EUR before printing, sample delivery and unknown horn hardware**.
Known shortfall for this basket:5.09EUR; complete delivered total unknown.
The same parts previously cost95.91before mechanics. A0.50EUR Pico header kit
plus one0.60EUR40pin pack saves0.10EUR and retains all pins. No weaker motors,
undersized PSU/wire, omitted mains lead or assumed free consumables.

[2026-10-25 source/stock review](BUDGET_REVIEW.md): black DonauE-175-11 at€5.50
replaces unavailable redE-175-10 at€5.90; exact tie pack rises€0.45→€0.60.
The net€0.25 reduction changes€105.34→€105.09. All other selected prices/rates
were rechecked; no stock reservation or postcode checkout. Keep staged delivery
costs unknown. Meter polarity; both buses now use black wire with coded shrink bands.

An unselected eight-pad FIX-RF-003 comparison would cost€96.79 before the same
print/sample/horn unknowns, leaving€3.21. Pads are4.5mm tapered rubber, not the
current3mm TPE cylinders. No current geometry or saving is changed for that option.
Use `tools/compare_procurement.py --option berrybase_round_pads`; it refuses free
postage while retaining another item from that supplier and never clears purchase.

Shipping/VAT rates remain published Germany snapshots, not a final checkout:
Welectron4.95, BerryBase4.95, Funduino4.90, Reichelt5.95, Schraubenking5.90EUR.
One shipping charge per supplier; every staged sample delivery is additional unless
an actual quotation states otherwise. Print material is inside the service quote:
**no filament spool/printer/printed TPU** is in the active basket.

Consolidating the IMU at BerryBase was rejected:9.90EUR vs3.62 adds6.28 before any
4.90shipping saving, with a differing module/interface listing. Combining fasteners
with pads or printer service remains unverified; no complete matched kit was found.
Old quotations refer to old geometry and cannot price this revision.
A direct3pin-header harness could replace extension cables using the existing pin
packs, but actual mating/keying,3Acontact suitability and insulation/strain relief
remain unverified. It is a research candidate only; no saving is credited.

## Public print-service review

| Service | Verified public capability | Price / missing evidence |
|---|---|---|
| [Meltlab](https://meltlab.de/konfigurator) | Instant STL calculator; public page describes PETG and selectable support removal | Exact revised-file upload was blocked by automatic approval review; no new quote |
| [f3dprint](https://www.f3dprint.de/druck-service) | STL/3MF, PETG,0.20mm; online price UI | Required25%infill/3walls/finishing not established; no file quote/upload |
| [Riesen Consulting](https://riesen-consulting.de/cad-dienstleistungen/3d-druck-service/3d-druck-online-bestellen-preis-sofort-berechnen/) | Instant FDM calculator, Germany delivery | Page explicitly separates fit review/finishing from automated printing; no complete quote/inquiry |

No service has a complete budget-passing quotation, so **none is selected**.
Public example prices are not this project's quotation.

## Required human action / exact questions

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
