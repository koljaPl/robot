import copy
import json
from pathlib import Path

import numpy as np
import trimesh

from tools.budget_gate import check_basket, cash_comparison
from tools.prepare_local_print import generate

ROOT = Path(__file__).resolve().parents[1]


def test_routes_are_alternatives_and_unknown_frame_is_not_free():
    basket = json.loads((ROOT / "procurement.json").read_text())
    standard = check_basket(basket, "standard_parts")
    own = check_basket(basket, "own_printer")
    assert standard["known_delivered_subtotal_eur"] == "95.91"
    assert own["known_delivered_subtotal_eur"] == "118.43"
    assert standard["status"] == "INCOMPLETE" and standard["total_price_eur"] is None
    assert own["status"] == "OVER BUDGET" and not own["purchase_cleared"]
    assert own["confirmed_minimum_shortfall_eur"] == "18.43"
    modified = copy.deepcopy(basket)
    modified["scenarios"]["own_printer"]["items"][0]["unit_price_eur"] = 999
    assert check_basket(modified, "standard_parts") == standard


def test_printer_tools_separate_from_robot_cap_and_unknowns_retained():
    basket = json.loads((ROOT / "procurement.json").read_text())
    report = cash_comparison(basket, "a1_mini")
    assert report["robot"] == check_basket(basket, "own_printer")
    assert report["printer_and_tools_known_eur"] == "189.00"
    assert report["initial_cash_known_eur"] == "307.43"
    assert report["initial_cash_total_eur"] is None
    assert report["printer_and_tools_total_eur"] is None  # tool access unknown
    basket["printer_options"]["a1_mini"]["shipping_eur"] = None
    assert cash_comparison(basket, "a1_mini")["printer_and_tools_total_eur"] is None


def test_local_plates_preserve_sources_and_fit_small_bed(tmp_path):
    report = generate(tmp_path)
    assert report["frame_parts"] == 7 and not report["slicer_verified"]
    for row in report["parts"]:
        source = trimesh.load_mesh(ROOT / "cad/stl" / f"{row['part']}.stl")
        plate = trimesh.load_mesh(tmp_path / row["file"])
        assert np.all(plate.bounds[0][:2] >= 4.999)
        assert np.all(plate.bounds[1] <= [175.001, 175.001, 180.001])
        assert np.isclose(source.volume, plate.volume, rtol=1e-6)
        assert len(plate.split()) == len(source.split()) == 1
    assert len(trimesh.load_mesh(tmp_path / report['sample']['file']).split()) == 2
