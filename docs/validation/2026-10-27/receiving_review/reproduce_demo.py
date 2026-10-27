"""Entirely SYNTHETIC receiving demonstration. Not purchases, arrivals or measurements.

Run with --output NEW_DIRECTORY from the project root; never touches hardware.
"""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from tools.review_receiving import blank_record, sources


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, type=Path)
    output = p.parse_args().output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    inputs = output / 'synthetic_inputs';inputs.mkdir()
    (inputs / 'SYNTHETIC.txt').write_text('FICTITIOUS evidence only. Not a receipt/photo/measurement.\n')
    record = blank_record();record.update(data_kind='synthetic', record_date='2026-10-27')
    products = sources()[-1]
    for i, order in enumerate(record['orders']):
        order.update(order_id='SYNTHETIC-' + str(i), ordered_date='2026-10-26',
                     arrival_date='2026-10-27', shipping_paid_eur=2.5, other_paid_eur=0,
                     evidence_files=['SYNTHETIC.txt'])
        for item in order['items']:
            item.update(quantity_ordered=products[item['product']]['quantity'],
                        quantity_received=products[item['product']]['quantity'], paid_line_eur=1.25,
                        accessories='SYNTHETIC fixture only')
    record['hardware'].update(servo_id='SYNTHETIC-ONLY', spline='Synthetic unspecified',
                              retainer_thread='Synthetic unspecified', retainer_length_mm=3,
                              horn_hole_radii_mm=[7], frame_screw_thread='Synthetic unspecified',
                              frame_screw_length_mm=4)
    record['printing'].update(material='PETG', layer_height_mm=.2, walls=3, infill_percent=25,
                              finishing='Synthetic fixture', deviations='None in fictitious fixture',
                              evidence_files=['SYNTHETIC.txt'])
    for sample in record['printing']['samples']:
        sample.update(received=True, print_date='2026-10-27')
        for check in sample['checks'].values():
            check.update(status='passed', notes='SYNTHETIC: not physically observed',
                         measurements_mm={'synthetic_dimension': 3}, evidence_files=['SYNTHETIC.txt'])
    complete = copy.deepcopy(record)
    partial = copy.deepcopy(record);partial['orders'] = partial['orders'][:1]
    partial['orders'][0].update(shipping_paid_eur=None, arrival_date=None)
    failed = copy.deepcopy(record)
    failed['printing']['samples'][0]['checks']['servo_insertion'].update(status='failed', notes='Synthetic interference')
    blank = blank_record();blank['data_kind'] = 'synthetic'
    results = {}
    for name, data, expected in (('complete', complete, 0), ('partial', partial, 2),
                                 ('failed_fit', failed, 2), ('blank', blank, 2)):
        path = inputs / (name + '.json');path.write_text(json.dumps(data, indent=2) + '\n')
        command = [sys.executable, str(ROOT / 'tools/review_receiving.py'), str(path),
                   '--output', str(output / name)]
        run = subprocess.run(command, capture_output=True, text=True)
        results[name] = {'command': command, 'expected_exit': expected,
                         'actual_exit': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr}
        if run.returncode != expected:
            raise RuntimeError(json.dumps(results[name]))
    (output / 'cli_results.json').write_text(json.dumps(results, indent=2) + '\n')
    print('Four SYNTHETIC CLI reports generated; no real receiving or fit evidence.')


if __name__ == '__main__':
    main()
