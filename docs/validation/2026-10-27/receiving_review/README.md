# Receiving review — locally verified, 2026-10-27

**No actual receipts, arrivals, fit, power, measurements or purchases in this evidence.**
All demo identifiers, dates, payments, dimensions, threads and fit assertions are
fictitious. The50EUR synthetic payment subtotal is **not** a robot price/quote.

- [52focused tests](pytest_focused.txt); [238full tests](pytest_full.txt),21.07s full.
  [Commands/return codes](test_commands.json).
- [Synthetic CLI exit records](demo/cli_results.json): complete0, partial2,
  failed-fit2, blank2. Every report says diagnostic, not physically verified;
  complete delivered cost remains unknown even for the complete fixture.
- [Complete fixture report](demo/complete/report.md),
  [partial receipts](demo/partial/report.md),
  [failed fit](demo/failed_fit/report.md), [blank](demo/blank/report.md).
- Tests cover units/source/sample hashes, quantities/dates/evidence, corrupt or
  duplicated orders/JSON keys, shared shipping, split receipts, null amounts,
  per-order/overall reconciliation, existing output, private folder/marker/symlink
  exclusion, direct STL bytes and print-setting deviations.

First focused run had46passes/2failures: the blank builder shared its units dict
with validation. Fixed by returning an independent mapping; regression retained.
Static review also caught per-order summaries captured before item costs; corrected
before these demos and guarded by explicit subtotal reconciliation. The dated root
plan retains those findings; final logs above describe the delivered implementation.

Reproduce without hardware (new output required):

```bash
.venv/bin/python docs/validation/2026-10-27/receiving_review/reproduce_demo.py \
  --output runs/receiving_synthetic_new
.venv/bin/python -m pytest -q tests/test_receiving_review.py
```

Original source bytes for this checkpoint are under `source/`; hashes in
`source_hashes.json`. Current-source tests and demos require matching ledgers and
print package; do not migrate recorded hashes without review. Initial unchanged-file
hashes are in `unchanged_before.json`; delivery verification compares them again.
The obsolete action page is preserved verbatim in
[history](../../../history/2026-10-27/pre_receiving/PROCUREMENT_ACTIONS.md.txt).

No runtime configuration, nominal reference, firmware/UF2, print ZIP/STLs,
procurement or physical gates changed. No new policy training. Actual inputs remain
the next dependency; real receipts/photos/reports belong outside packaged folders.

[Initial delivery check](initial_delivery_checks.json) records the pass before the
final plan/delivery-log refresh. Recheck the final archive without changing files:

```bash
.venv/bin/python docs/validation/2026-10-27/receiving_review/verify_delivery.py
```

Final archive integrity is also identified by the root ZIP checksum sidecar.
