"""Read procurement evidence; unknown required costs never count as zero."""
import argparse
from decimal import Decimal
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check_basket(basket):
    known = sum((Decimal(str(i["unit_price_eur"])) * i["quantity"] for i in basket["items"]
                 if i["unit_price_eur"] is not None), Decimal("0"))
    cap = Decimal(str(basket["budget_max_eur"]))
    pending = [i["product"] for i in basket["items"] if i["unit_price_eur"] is None]
    checks = basket.get("unresolved_checks", [])
    status = "OVER BUDGET" if known > cap else "INCOMPLETE" if pending or checks else "WITHIN BUDGET"
    return {"status": status, "known_delivered_subtotal_eur": str(known.quantize(Decimal("0.01"))),
            "remaining_for_all_unknowns_eur": str((cap - known).quantize(Decimal("0.01"))),
            "confirmed_minimum_shortfall_eur": str(max(Decimal("0"), known - cap).quantize(Decimal("0.01"))),
            "total_price_eur": None if pending else str(known), "pending_prices": pending,
            "unresolved_checks": checks, "purchase_cleared": status == "WITHIN BUDGET"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--basket", type=Path, default=ROOT / "procurement.json")
    args = p.parse_args()
    result = check_basket(json.loads(args.basket.read_text()))
    print(json.dumps(result, indent=2))
    return 0 if result["purchase_cleared"] else 1 if result["status"] == "OVER BUDGET" else 2


if __name__ == "__main__":
    raise SystemExit(main())
