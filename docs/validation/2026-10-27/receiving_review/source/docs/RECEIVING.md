# Receive parts and review the two fit samples

Prepared **2026-10-27**. Offline evidence review, not approval to manufacture,
power or deploy. **No arrivals or actual costs are recorded yet.** Use the
[printable checklist](RECEIVING_CHECKLIST.md) first; you can supply notes/photos
and let the AI enter them later. JSON is optional for the student.

## Start a private record

```bash
mkdir -p local_records/receiving_01
cp docs/templates/receiving.example.json local_records/receiving_01/record.json
# Fill known fields; keep receipts/photos beside this private record.
.venv/bin/python tools/review_receiving.py local_records/receiving_01/record.json \
  --output local_records/receiving_01/review_01
```

`local_records/` is ignored by Git and excluded from delivery. Do not put real
receipts, addresses, photos or reports under docs/cad/tests/tools/firmware/
calibrations/print_for_classmate. The reviewer refuses physical inputs, outputs
and evidence in those packaged directories. Private reports also have a
`PRIVATE_RECEIVING_RECORD` marker that packaging excludes. Nothing opens USB.

Outputs: `report.md` and `report.json`: source/evidence SHA-256 hashes, per-order
known payments, missing costs/checks and reported failures. Exit **0**: diagnostic
record complete with no flags; **2**: incomplete, failed fit, changed print settings/
material or recorded spending over cap; **1**: invalid input, stale sources, missing
file or existing output. Even exit0 **never approves budget, fit or calibration**.
Use a fresh output directory after editing; keep previous reports.

## Filling the version1 template

- `data_kind`: `physical` for actual records; `synthetic` only for labelled fiction.
  Dates: YYYY-MM-DD or `null`. Units: dimensions **mm**, costs **EUR**, quantities
  integers in purchase units. One pack100 washers is quantity1, not100. Installed
  quantities remain in [assembly](../cad/ASSEMBLY.md); software still uses SI units.
- `orders`: template groups expected products by source; **these are not claimed
  orders**. Set unique local `order_id` values when known. Keep exact ledger product
  names; fill dates, received quantities, accessories and relative `evidence_files`.
  Split deliveries may be separate records; do not duplicate payments. A changed
  product requires ledger/interface review, not a renamed label.
- `paid_line_eur`: actual whole-line payment, including VAT but **excluding** separately
  recorded shipping/other charges. Record `shipping_paid_eur` once per order;
  `other_paid_eur` covers separate finishing/fees. Old print-product names mention
  delivery: separate that charge here. Explicitly confirmed zero is allowed;
  `null` means unknown, never free.
- If horns are confirmed included, record the required accessory line at zero
  additional cost in the servo order with shared receipt evidence. Remove its
  unused placeholder order. Do not presume inclusion, spline or screw compatibility.
- `hardware`: actual tested servo ID, supplied horn/screw interfaces. Unknown spline/
  thread stays `null`; do not guess25T or M2. Lengths are under-head dimensions;
  hole radii are distances from the shaft centre.
- `printing`: material, actual settings, finishing/deviations, then both named samples.
  `received`: true/false/null. Check status: pending/passed/failed; a passed damage
  check means **no visible damage**. Add descriptions, photographs and named
  `measurements_mm`; instrument/uncertainty in notes. No fit tolerance is invented.

The template is tied to procurement, physical-specification, model/control and
print-manifest hashes, plus each sample STL hash. A changed source requires a
reviewed migration to a new record; do not blindly replace hashes to pass intake.

Known payments are **not the complete delivered robot cost**, even if every field
is filled. Quotes are never added to actual payments. The dated quotation remains
**€106.49 before unknown print/horn extras**, at least€6.49 over€100. Reconcile final
costs separately, including every printing/finishing/transport stage. The reviewer
never edits procurement, geometry, calibration or gates.

## Next physical actions

1. Inspect actual servo/accessories against the [drawing](../cad/print_order/drawings/interfaces.png).
2. Check two samples; failed fit means revise/reprint, not drilling or forcing.
   Review complete costs and remaining clearance/strength uncertainties before seven frames.
3. Follow [one-servo/IMU bench](BENCH.md), [assembly](../cad/ASSEMBLY.md), then
   [measurement intake](MEASUREMENT_INTAKE.md). Horn mounting needing a centred
   shaft follows the unloaded bench test; disconnect servo DC before mechanical fit.

Hashes preserve provenance, not truth. Photos cannot verify continuous clearance,
structural strength, six-servo current capacity or learned walking.
