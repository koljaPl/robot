"""Synthetic receiving/fit assertions only; never physical evidence."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from decimal import Decimal

import pytest

from tools import package_project
from tools import review_receiving as receiving


def save(path, record):
    path.write_text(json.dumps(record, indent=2) + '\n')


@pytest.fixture
def complete(tmp_path):
    """Every number/thread/fit assertion here is fictitious, not an MG90S measurement."""
    record = receiving.blank_record()
    record.update(data_kind='synthetic', record_date='2026-10-27')
    evidence = tmp_path / 'SYNTHETIC.txt'
    evidence.write_text('SYNTHETIC test fixture, not a receipt, photo, arrival or measurement.\n')
    products = receiving.sources()[-1]
    for i, order in enumerate(record['orders']):
        order.update(order_id='SYNTHETIC-' + str(i), ordered_date='2026-10-26',
                     arrival_date='2026-10-27', shipping_paid_eur=2.5, other_paid_eur=0,
                     evidence_files=[evidence.name])
        for item in order['items']:
            item.update(quantity_ordered=products[item['product']]['quantity'],
                        quantity_received=products[item['product']]['quantity'],
                        paid_line_eur=1.25, accessories='Synthetic fixture accessories recorded')
    record['hardware'].update(servo_id='SYNTHETIC-ONLY', spline='Synthetic fixture, not specified',
                              retainer_thread='Synthetic fixture, not specified', retainer_length_mm=3,
                              horn_hole_radii_mm=[7], frame_screw_thread='Synthetic fixture, not specified',
                              frame_screw_length_mm=4)
    record['printing'].update(material='PETG', layer_height_mm=.2, walls=3,
                              infill_percent=25, finishing='Synthetic finishing assertion',
                              deviations='None in synthetic fixture', evidence_files=[evidence.name])
    for sample in record['printing']['samples']:
        sample.update(received=True, print_date='2026-10-27')
        for check in sample['checks'].values():
            check.update(status='passed', notes='SYNTHETIC fit assertion, not observed',
                         measurements_mm={'synthetic_dimension': 3}, evidence_files=[evidence.name])
    path = tmp_path / 'SYNTHETIC.json'
    save(path, record)
    return path, record


def test_complete_report_does_not_approve_cost_fit_or_gates(complete, tmp_path):
    path, record = complete
    r = receiving.review(path, tmp_path / 'report')
    assert r['record_complete'] and not r['reported_failures']
    assert r['state'] == 'diagnostic_awaiting_human_review'
    assert r['data_kind'] == 'synthetic'
    for key in ('physically_verified', 'manufacturing_approved', 'budget_cleared', 'gates_updated'):
        assert r[key] is False
    assert r['spending']['complete_delivered_robot_total_eur'] is None
    assert len(r['sample_checks']) == 10
    assert r['record_sha256'] == receiving.sha(path)
    assert r['evidence_sha256']['SYNTHETIC.txt'] == receiving.sha(tmp_path / 'SYNTHETIC.txt')
    assert json.loads((tmp_path / 'report/report.json').read_text()) == r
    md = (tmp_path / 'report/report.md').read_text()
    assert 'SYNTHETIC' in md and 'No gates approved' in md and 'unknown' in md
    assert not (tmp_path / 'report/PRIVATE_RECEIVING_RECORD').exists()


def test_blank_template_leaves_actuals_unknown(tmp_path):
    template = json.loads((receiving.ROOT / 'docs/templates/receiving.example.json').read_text())
    assert template == receiving.blank_record()
    assert template['record_date'] is None and template['hardware']['spline'] is None
    for order in template['orders']:
        assert order['order_id'] is None and order['shipping_paid_eur'] is None
        for item in order['items']:
            assert item['quantity_ordered'] is None and item['quantity_received'] is None
            assert item['paid_line_eur'] is None
    path = tmp_path / 'receiving.json';save(path, template)
    report = receiving.review(path, tmp_path / 'blank_report')
    assert not report['record_complete'] and report['missing_checks_or_fields']
    assert report['spending']['recorded_payments_eur'] is None
    assert report['spending']['unresolved_costs']
    assert (tmp_path / 'blank_report/PRIVATE_RECEIVING_RECORD').is_file()


def test_blank_record_units_are_independent():
    record = receiving.blank_record()
    record['units']['length'] = 'm'
    assert receiving.UNITS['length'] == 'mm'
    assert receiving.blank_record()['units']['length'] == 'mm'


def test_partial_receipts_never_add_quotes_or_imply_complete_total(complete, tmp_path):
    path, record = complete
    record['orders'] = record['orders'][:1]
    order = record['orders'][0]
    order.update(shipping_paid_eur=None, other_paid_eur=None, arrival_date=None)
    item = order['items'][0]
    item.update(paid_line_eur=21, quantity_received=1)
    save(path, record)
    r = receiving.review(path, tmp_path / 'partial')
    assert r['spending']['recorded_payments_eur'] == '21.00'
    assert r['spending']['unresolved_costs'] and not r['record_complete']
    assert r['spending']['complete_delivered_robot_total_eur'] is None
    assert any('Required receipt incomplete:' in s for s in r['missing_checks_or_fields'])


def test_shipping_once_per_order_not_per_item_and_split_orders(complete, tmp_path):
    path, record = complete
    r = receiving.review(path, tmp_path / 'first')
    expected = sum(2.5 + 1.25 * len(order['items']) for order in record['orders'])
    assert r['spending']['recorded_payments_eur'] == f'{expected:.2f}'
    assert sum(Decimal(o['known_payments_eur']) for o in r['spending']['orders']) == Decimal(f'{expected:.2f}')
    # Split the six-servo purchase over two deliveries: quantities aggregate, postage repeats only explicitly.
    first = record['orders'][0]
    second = copy.deepcopy(first);second['order_id'] = 'SYNTHETIC-SPLIT'
    first['items'][0].update(quantity_ordered=3, quantity_received=3, paid_line_eur=.5)
    second['items'][0].update(quantity_ordered=3, quantity_received=3, paid_line_eur=.75)
    record['orders'].append(second);save(path, record)
    r = receiving.review(path, tmp_path / 'split')
    assert r['record_complete']
    assert r['spending']['recorded_payments_eur'] == f'{expected + 2.5:.2f}'
    servo = r['required_product_coverage'][0]
    assert servo['known_reported_received_units'] == 6


def test_failed_fit_and_material_change_remain_visible(complete, tmp_path):
    path, record = complete
    record['printing']['material'] = 'PLA'
    record['printing']['samples'][0]['checks']['servo_insertion'].update(status='failed', notes='Synthetic interference')
    save(path, record)
    r = receiving.review(path, tmp_path / 'failed_fit')
    assert r['record_complete'] and len(r['reported_failures']) == 1 and r['warnings']
    assert not r['manufacturing_approved']
    assert 'failed' in (tmp_path / 'failed_fit/report.md').read_text()


@pytest.mark.parametrize('problem', [
    'version', 'kind', 'units', 'source', 'sample_hash', 'sample_revision', 'duplicate_sample',
    'duplicate_order', 'duplicate_product', 'unknown_product', 'negative_cost', 'bool_cost',
    'infinite_cost', 'fractional_cent', 'negative_quantity', 'bool_quantity', 'fractional_quantity',
    'over_received', 'date', 'date_order', 'missing_evidence', 'bad_evidence', 'duplicate_evidence',
    'bad_measurement', 'bad_hole_radii', 'bad_screw_length', 'bad_check_status', 'missing_check',
    'unreceived_fit', 'infill', 'zero_layer', 'zero_walls', 'wrong_orders_type', 'wrong_sample_type',
])
def test_invalid_inputs_refused_before_output(complete, tmp_path, problem):
    path, record = complete
    order = record['orders'][0];item = order['items'][0]
    sample = record['printing']['samples'][0];check = sample['checks']['servo_insertion']
    if problem == 'version':record['version'] = True
    if problem == 'kind':record['data_kind'] = 'measured'
    if problem == 'units':record['units']['length'] = 'm'
    if problem == 'source':record['source_identity']['configuration'] = '0' * 64
    if problem == 'sample_hash':sample['sha256'] = '0' * 64
    if problem == 'sample_revision':record['printing']['revision'] = 'old'
    if problem == 'duplicate_sample':record['printing']['samples'][1] = copy.deepcopy(sample)
    if problem == 'duplicate_order':record['orders'][1]['order_id'] = order['order_id']
    if problem == 'duplicate_product':order['items'].append(copy.deepcopy(item))
    if problem == 'unknown_product':item['product'] = 'A similarly named servo'
    if problem == 'negative_cost':item['paid_line_eur'] = -1
    if problem == 'bool_cost':item['paid_line_eur'] = True
    if problem == 'infinite_cost':item['paid_line_eur'] = float('inf')
    if problem == 'fractional_cent':item['paid_line_eur'] = .001
    if problem == 'negative_quantity':item['quantity_received'] = -1
    if problem == 'bool_quantity':item['quantity_ordered'] = True
    if problem == 'fractional_quantity':item['quantity_ordered'] = 1.5
    if problem == 'over_received':item['quantity_received'] = 7
    if problem == 'date':order['arrival_date'] = '2026-99-99'
    if problem == 'date_order':order['arrival_date'] = '2026-10-25'
    if problem == 'missing_evidence':check['evidence_files'] = ['missing.jpg']
    if problem == 'bad_evidence':check['evidence_files'] = 'SYNTHETIC.txt'
    if problem == 'duplicate_evidence':check['evidence_files'] *= 2
    if problem == 'bad_measurement':check['measurements_mm']['synthetic_dimension'] = float('nan')
    if problem == 'bad_hole_radii':record['hardware']['horn_hole_radii_mm'] = [0]
    if problem == 'bad_screw_length':record['hardware']['retainer_length_mm'] = 0
    if problem == 'bad_check_status':check['status'] = 'verified'
    if problem == 'missing_check':sample['checks'].pop('wire_exit')
    if problem == 'unreceived_fit':sample['received'] = False
    if problem == 'infill':record['printing']['infill_percent'] = 101
    if problem == 'zero_layer':record['printing']['layer_height_mm'] = 0
    if problem == 'zero_walls':record['printing']['walls'] = 0
    if problem == 'wrong_orders_type':record['orders'] = {}
    if problem == 'wrong_sample_type':record['printing']['samples'] = None
    save(path, record)
    with pytest.raises(ValueError):receiving.review(path, tmp_path / 'refused')
    assert not (tmp_path / 'refused').exists()


def test_missing_check_evidence_and_dimensions_are_incomplete_not_approved(complete, tmp_path):
    path, record = complete
    check = record['printing']['samples'][0]['checks']['mounting_stack']
    check.update(evidence_files=[], measurements_mm={}, notes=None)
    save(path, record);r = receiving.review(path, tmp_path / 'no_proof')
    assert not r['record_complete']
    assert any('dimensions_mm' in s for s in r['missing_checks_or_fields'])


def test_existing_output_and_source_preservation(complete, tmp_path):
    path, _ = complete
    names = ['procurement.json', 'physical_spec.json', 'robot.xml', 'robot_config.py',
             'docs/gates.json', 'print_for_classmate/manifest.json', 'print_for_classmate.zip']
    before = {n: receiving.sha(receiving.ROOT / n) for n in names}
    output = tmp_path / 'report';receiving.review(path, output)
    result_hash = receiving.sha(output / 'report.json')
    with pytest.raises(FileExistsError):receiving.review(path, output)
    assert receiving.sha(output / 'report.json') == result_hash
    assert {n: receiving.sha(receiving.ROOT / n) for n in names} == before


@pytest.mark.parametrize('location', ['record', 'output', 'evidence'])
def test_physical_records_outside_packaged_folders_only(complete, tmp_path, monkeypatch, location):
    path, record = complete;record['data_kind'] = 'physical'
    packaged = tmp_path / 'packaged';packaged.mkdir()
    monkeypatch.setattr(receiving, 'PACKAGED_ROOTS', (str(packaged),))
    output = tmp_path / 'report'
    if location == 'record':path = packaged / 'record.json'
    if location == 'output':output = packaged / 'report'
    if location == 'evidence':
        photo = packaged / 'photo.txt';photo.write_text('private fixture')
        record['orders'][0]['evidence_files'] = [str(photo)]
    save(path, record)
    with pytest.raises(ValueError, match='packaged'):
        receiving.review(path, output)
    assert not output.exists()


def test_package_allowlist_excludes_private_sessions_and_symlinks(tmp_path, monkeypatch):
    monkeypatch.setattr(package_project, 'ROOT', tmp_path)
    docs = tmp_path / 'docs';docs.mkdir()
    (docs / 'public.md').write_text('public fixture')
    for private in (tmp_path / 'local_records', docs / 'local_records', docs / 'session'):
        private.mkdir(parents=True)
        (private / 'receipt.txt').write_text('PRIVATE TEST FIXTURE')
    (docs / 'session/PRIVATE_RECEIVING_RECORD').write_text('private')
    (docs / 'leak.txt').symlink_to(tmp_path / 'local_records/receipt.txt')
    names = [str(rel) for _, rel in package_project.project_files()]
    assert names == ['docs/public.md']


def test_cli_exit_codes_and_no_usb(complete, tmp_path):
    path, record = complete
    tool = receiving.ROOT / 'tools/review_receiving.py'
    for expected in (0, 2, 1):
        if expected == 2:record['printing']['samples'][0]['checks']['wire_exit']['status'] = 'pending'
        if expected == 1:record['version'] = 99
        save(path, record)
        r = subprocess.run([sys.executable, str(tool), str(path), '--output', str(tmp_path / str(expected))],
                           capture_output=True, text=True)
        assert r.returncode == expected, r.stderr
    source = tool.read_text()
    assert 'SerialRobot' not in source and 'serial.Serial' not in source


def test_duplicate_json_keys_refused(complete, tmp_path):
    path, _ = complete
    path.write_text(path.read_text().replace('"version": 1', '"version": 1, "version": 1', 1))
    with pytest.raises(ValueError, match='Duplicate JSON key'):
        receiving.review(path, tmp_path / 'refused')


def test_cap_exceedance_is_recorded_without_changing_quotes(complete, tmp_path):
    path, record = complete
    record['orders'][0]['items'][0]['paid_line_eur'] = 150
    save(path, record);r = receiving.review(path, tmp_path / 'expensive')
    assert r['spending']['recorded_payments_exceed_cap']
    assert not r['budget_cleared']


def test_actual_sample_bytes_checked_against_current_manifest(complete, tmp_path, monkeypatch):
    path, _ = complete
    original = receiving.sha
    target = receiving.ROOT / 'print_for_classmate/01_FIT_SAMPLE/ear_cradle.stl'
    monkeypatch.setattr(receiving, 'sha', lambda p: '0' * 64 if Path(p) == target else original(p))
    with pytest.raises(ValueError, match='Current sample file/hash mismatch'):
        receiving.review(path, tmp_path / 'refused')


def test_shipping_cannot_also_be_an_item(complete, tmp_path):
    path, record = complete
    record['orders'][0]['items'][0]['product'] = 'Welectron German DPD shipping'
    save(path, record)
    with pytest.raises(ValueError, match='Unknown product'):
        receiving.review(path, tmp_path / 'double_postage')


def test_changed_print_settings_visible_and_not_automatic_failure(complete, tmp_path):
    path, record = complete
    record['printing'].update(layer_height_mm=.15, walls=4, infill_percent=0)
    save(path, record);report = receiving.review(path, tmp_path / 'settings')
    assert len(report['warnings']) == 3 and not report['reported_failures']
    assert not report['manufacturing_approved']
