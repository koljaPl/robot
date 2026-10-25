# Procurement and delivery review — 2026-10-25

**No purchases, reservations, messages or CAD uploads.** Prices below include VAT
and published German delivery rates, not a final checkout for25337. The exact
source records are in [the dated evidence](procurement/2026-10-25/basket_review.json);
the selected quantities/prices remain authoritative in [procurement.json](../procurement.json).

## Selected basket refresh

| Change | Evidence | Cost effect |
|---|---|---:|
| Red Donau E-175-10 unavailable → black E-175-11 | [Exact black variant](https://www.berrybase.de/donau-kupferschaltlitze-0-75-mm2-10m-lang-1-adrig-24x0-20mm-pvc-isoliert/farbe-schwarz), browser:7rolls, €5.50; same0.75mm² copper,24×0.20mm, PVC,10m | −€0.40 |
| Exact transparent100×2.5mm tie pack | [T1535501](https://www.berrybase.de/kabelbinder-uv-bestaendig-nylon-100-stueck/farbe-transparent/masse-100x2-5mm), now€0.60,6packs displayed | +€0.15 |
| Other selected prices | Product/standard delivery pages rechecked; no remaining price change credited | €0.00 |
| **Selected priced subtotal** | Previously€105.34 → **€105.09** | **−€0.25** |

This is still **at least€5.09 over the cap before printing, sample deliveries,
finishing and unresolved horn hardware**. Complete delivered cost remains unknown.
No supplier is booked; advertised working-day intervals are not promised arrival
dates. Several staged orders may add postage. None has been assumed free.

The wire colour change requires polarity identification, not a controller or CAD
change. Use two separated bands of the existing black heat-shrink at each positive
lead end and one at each negative end. Trace and meter every branch before power;
never infer polarity from the all-black conductor colour. Retain separate heavy
servo buses, insulation, strain relief and accessible physical DC disconnection.
See [wiring](HARDWARE.md). Actual harness current/connector/PWM tests remain pending.

## One useful but unselected alternative

[FIX&FASTEN FIX-RF-003](https://www.berrybase.de/fix-fasten-selbstklebender-fuss-rund-oben-9-5mm-unten-10mm-hoehe-4-5mm-gummi-schwarz)
is sold individually at€0.15 including VAT. Eight cost€1.20 in the existing
BerryBase delivery. If they replace Delock18309 (€3.55) and Reichelt has no other
required items, its€5.95 delivery can also be removed: **conditional saving€8.30**.

| Scenario | Priced subtotal | Maximum left for every unknown | Cleared? |
|---|---:|---:|---|
| Selected basket/current3mm TPE pads | €105.09 | Already€5.09 over cap | No |
| Unselected FIX-RF-003 comparison | €96.79 | €3.21 | No; incomplete and mechanically different |

FIX-RF-003 is tapered rubber, upper diameter9.5mm/lower10mm, height4.5mm; the
current twin uses cylindrical10×3mm TPE pads. The extra1.5mm changes contact and
standing geometry. Hardness, compression, adhesive performance, installed mass
and friction remain unknown. The seller's0.682g **gross** mass is not a measured
installed mass. Stock displays differ (10vs100+); checkout must confirm eight.

**Recommendation:** retain the current pad/model baseline until a complete
affordable basket exists. The alternative leaves only€3.21 for two fit samples,
seven finished prints, every staged delivery and unresolved horns/screws. No such
quotation exists. Do not spend a new CAD/control identity on an unclosed budget
or advertise€96.79 as a complete robot price.

Other reviewed options do not justify a substitution:

- [Funduino F23106261 assortment](https://funduino.com/products/schraubenset-kreuzschrauben-sortiment):
  €9.97; titleM2–M5 conflicts with the3–5mm technical table. Exact12M2×8 screws,
  12M2nuts and24washers are not established. It is not a complete matched replacement.
- Reviewed BerryBase fastening listings show M2.5 hardware; it cannot silently
  replace M2. Reichelt's exactM2x8 search gave no result; this is not proof that
  its entire catalogue has no suitable fasteners. No complete kit was verified.
- The previously considered direct-header servo harness still lacks qualified
  mating/keying/current/insulation evidence. No extension cable saving is credited.
- Adding unnecessary items to reach free-postage thresholds increases spending.
  Unconfirmed pickup, coupon, membership or service-supplied hardware is not free.

## Reproducible comparison and next action

```bash
.venv/bin/python tools/budget_gate.py
# Exit1: selected basket over cap; incomplete total remains null.
.venv/bin/python tools/compare_procurement.py --option berrybase_round_pads
# Exit2: comparison only; cannot clear purchase, even below the cap.
```

The comparison uses declared ledger substitutions without editing the selected
basket, physical specification or model. It refuses to remove a supplier's postage
while retaining any required item from that supplier, including unpriced items.
All pending print/sample/horn lines and fit checks remain in its result.

**Next:** obtain the missing exact-file service/hardware costs or a complete
verified consolidation that leaves enough room for them. Preserve the six selected
servos, PSU capacity and all required parts. Print upload authorization remains a
separate unresolved action; no retry or supplier message occurred in this review.
All physical/manufacturing/training gates remain false; no new PPO was run.
