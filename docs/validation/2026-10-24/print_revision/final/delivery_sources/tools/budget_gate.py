"""Read procurement evidence; unknown required costs never count as zero."""
import argparse
from decimal import Decimal
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check_basket(basket, scenario=None):
    """Check one route only; the root list is shared, not a complete robot."""
    scenario = scenario or basket.get("active_scenario")
    route = basket.get("scenarios", {}).get(scenario) if scenario else None
    if scenario and route is None:
        raise ValueError(f"Unknown scenario: {scenario}")
    items = basket["items"] + (route["items"] if route else [])
    known = sum((Decimal(str(i["unit_price_eur"])) * i["quantity"] for i in items
                 if i["unit_price_eur"] is not None), Decimal("0"))
    cap = Decimal(str(basket["budget_max_eur"]))
    pending = [i["product"] for i in items if i["unit_price_eur"] is None]
    checks = list(basket.get("unresolved_checks", []))
    if route:
        checks.extend(route.get("unresolved_checks", []))
        if route.get("selection_state") != "selected":
            checks.append("Comparison only; route has not been selected and approved")
    elif basket.get("scenarios"):
        checks.append("Shared subset only: choose a complete scenario")
    status = "OVER BUDGET" if known > cap else "INCOMPLETE" if pending or checks else "WITHIN BUDGET"
    return {"scenario": scenario or "shared subset", "status": status, "known_delivered_subtotal_eur": str(known.quantize(Decimal("0.01"))),
            "remaining_for_all_unknowns_eur": str((cap - known).quantize(Decimal("0.01"))),
            "confirmed_minimum_shortfall_eur": str(max(Decimal("0"), known - cap).quantize(Decimal("0.01"))),
            "total_price_eur": None if pending or checks else str(known.quantize(Decimal("0.01"))), "pending_prices": pending,
            "unresolved_checks": checks, "purchase_cleared": status == "WITHIN BUDGET"}


def cash_comparison(basket, printer):
    """Tools/printer are outside robot cap, but inside initial cash expenditure."""
    robot = check_basket(basket, "own_printer")
    option = basket["printer_options"][printer]
    values = [option["unit_price_eur"], option["shipping_eur"]]
    tools = basket.get("tool_items", [])
    known = sum((Decimal(str(v)) for v in values if v is not None), Decimal("0"))
    known += sum((Decimal(str(i["unit_price_eur"])) * i["quantity"] for i in tools
                  if i["unit_price_eur"] is not None), Decimal("0"))
    equipment_total = None if None in values or any(i["unit_price_eur"] is None for i in tools) else known
    full_cash = None if equipment_total is None or robot["total_price_eur"] is None else equipment_total + Decimal(robot["total_price_eur"])
    return {"printer": option["name"], "selected_for_purchase": False,
            "robot": robot,
            "printer_and_tools_known_eur": str(known.quantize(Decimal("0.01"))),
            "printer_and_tools_total_eur": None if equipment_total is None else str(equipment_total.quantize(Decimal("0.01"))),
            "initial_cash_known_eur": str((known + Decimal(robot["known_delivered_subtotal_eur"])).quantize(Decimal("0.01"))),
            "initial_cash_total_eur": None if full_cash is None else str(full_cash.quantize(Decimal("0.01"))),
            "delivery_evidence": option["shipping_state"],
            "notes": "Published rates, not a booked 25337 checkout. No assumed joint-order shipping credits; no alternatives added together."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--basket", type=Path, default=ROOT / "procurement.json")
    p.add_argument("--scenario", choices=["commercial_print", "standard_parts", "own_printer", "all"])
    p.add_argument("--printer", choices=["a1_mini", "ender_v3_se"])
    args = p.parse_args()
    basket = json.loads(args.basket.read_text())
    if args.printer and args.scenario != "own_printer":
        p.error("--printer requires --scenario own_printer")
    if args.scenario == "all":
        result = {"routes": {k: check_basket(basket, k) for k in basket["scenarios"]},
                  "printer_comparisons": {k: cash_comparison(basket, k) for k in basket["printer_options"]}}
        print(json.dumps(result, indent=2))
        return 1 if any(r["status"] == "OVER BUDGET" for r in result["routes"].values()) else 2
    result = cash_comparison(basket, args.printer) if args.printer else check_basket(basket, args.scenario)
    print(json.dumps(result, indent=2))
    gate = result.get("robot", result)
    return 0 if gate["purchase_cleared"] else 1 if gate["status"] == "OVER BUDGET" else 2


if __name__ == "__main__":
    raise SystemExit(main())
