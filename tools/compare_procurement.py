"""Price declared procurement alternatives without selecting parts or clearing gates."""
import argparse
import copy
from decimal import Decimal
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.budget_gate import check_basket


def compare_option(basket, name):
    option = basket['cost_options'][name]
    if option['selected']:
        raise ValueError('This tool handles unselected comparisons only')
    scenario = option['base_scenario']
    base = check_basket(basket, scenario)
    candidate = copy.deepcopy(basket)
    route = candidate['scenarios'][scenario]
    active = candidate['items'] + route['items']
    names = [item['product'] for item in active]
    removed = option['remove_products']
    if len(set(removed)) != len(removed) or any(names.count(product) != 1 for product in removed):
        raise ValueError('Every removed product must identify exactly one active line')
    additions = copy.deepcopy(option['add_items'])
    for item in additions:
        qty, price = item['quantity'], item['unit_price_eur']
        if type(qty) is not int or qty <= 0:
            raise ValueError('Comparison quantities must be positive full purchase units')
        if price is not None and (not Decimal(str(price)).is_finite() or Decimal(str(price)) < 0):
            raise ValueError('Invalid comparison price')
    remaining = [item for item in active if item['product'] not in removed] + additions
    for item in active:
        if item['product'] in removed and item['category'] == 'Shipping':
            if any(other['shop'] == item['shop'] and other['category'] != 'Shipping' for other in remaining):
                raise ValueError('Cannot remove shipping while retaining items from that supplier')
    candidate['items'] = [item for item in candidate['items'] if item['product'] not in removed]
    route['items'] = [item for item in route['items'] if item['product'] not in removed] + additions
    route['selection_state'] = 'comparison_only'
    route['unresolved_checks'] = route.get('unresolved_checks', []) + option['required_before_selection']
    report = check_basket(candidate, scenario)
    assert not report['purchase_cleared']
    return {'option': name, 'selected': False, 'state': 'unselected price comparison; not a complete quotation',
            'base_known_subtotal_eur': base['known_delivered_subtotal_eur'],
            'known_saving_eur': str((Decimal(base['known_delivered_subtotal_eur'])
                                     - Decimal(report['known_delivered_subtotal_eur'])).quantize(Decimal('.01'))),
            'candidate': report, 'removed_products': removed, 'added_items': additions,
            'physical_configuration_unchanged': True,  # comparison never edits CAD/spec/model
            'candidate_requires_geometry_revision': option.get('requires_geometry_revision', False)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basket', type=Path, default=ROOT/'procurement.json')
    parser.add_argument('--option', required=True)
    args = parser.parse_args()
    print(json.dumps(compare_option(json.loads(args.basket.read_text()), args.option), indent=2))
    return 2  # Comparison only, never a purchase clearance.


if __name__ == '__main__':
    raise SystemExit(main())
