import copy
import json

import pytest

from robot_config import ROOT
from tools.compare_procurement import compare_option


def test_pad_comparison_removes_only_unused_delivery_and_never_clears_purchase():
    basket = json.loads((ROOT/'procurement.json').read_text())
    before = copy.deepcopy(basket)
    result = compare_option(basket, 'berrybase_round_pads')
    assert basket == before
    assert result['base_known_subtotal_eur'] == '106.49'
    assert result['known_saving_eur'] == '8.30'
    assert result['candidate']['known_delivered_subtotal_eur'] == '98.19'
    assert result['candidate']['remaining_for_all_unknowns_eur'] == '1.81'
    assert result['candidate']['total_price_eur'] is None
    assert not result['candidate']['purchase_cleared'] and not result['selected']
    assert result['candidate_requires_geometry_revision']
    assert any('PETG fit sample' in item for item in result['candidate']['pending_prices'])


def test_shipping_is_not_free_if_supplier_still_supplies_another_component():
    basket = json.loads((ROOT/'procurement.json').read_text())
    basket['items'].append({'category': 'Fasteners', 'product': 'hypothetical retained Reichelt part',
                            'quantity': 1, 'unit_price_eur': None, 'shop': 'Reichelt'})
    with pytest.raises(ValueError, match='Cannot remove shipping'):
        compare_option(basket, 'berrybase_round_pads')


def test_invalid_substitution_cannot_silently_disappear_from_costs():
    basket = json.loads((ROOT/'procurement.json').read_text())
    basket['cost_options']['berrybase_round_pads']['remove_products'].append('nonexistent line')
    with pytest.raises(ValueError, match='exactly one'):
        compare_option(basket, 'berrybase_round_pads')
