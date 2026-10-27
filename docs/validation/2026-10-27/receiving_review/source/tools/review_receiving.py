"""Offline receiving/sample evidence review; never approves purchases or physical gates."""
import argparse
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from calibration import configuration_identity

UNITS = {'length': 'mm', 'currency': 'EUR'}
SAMPLES = {
    '01_FIT_SAMPLE/ear_cradle.stl': (
        'servo_insertion', 'ear_holes', 'mounting_stack', 'wire_exit',
        'usable_holes', 'visible_print_damage'),
    '01_FIT_SAMPLE/horn_plate.stl': (
        'horn_attachment', 'retaining_screw_access', 'usable_holes', 'visible_print_damage'),
}
PACKAGED_ROOTS = ('docs', 'cad', 'tests', 'tools', 'firmware', 'calibrations', 'print_for_classmate')
HARDWARE_FIELDS = ('servo_id', 'spline', 'retainer_thread', 'retainer_length_mm',
                   'horn_hole_radii_mm', 'frame_screw_thread', 'frame_screw_length_mm')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON: ' + x)))


def sources():
    ledger = load_json(ROOT / 'procurement.json')
    spec = load_json(ROOT / 'physical_spec.json')
    manifest = load_json(ROOT / 'print_for_classmate/manifest.json')
    identity = {name: sha(ROOT / name) for name in
                ('procurement.json', 'physical_spec.json', 'print_for_classmate/manifest.json')}
    identity['configuration'] = configuration_identity()['configuration']
    if manifest['physical_spec_sha256'] != identity['physical_spec.json']:
        raise ValueError('Current print manifest does not match physical specification')
    meshes = {item['file']: item for item in manifest['files']}
    for name in SAMPLES:
        if name not in meshes or sha(ROOT / 'print_for_classmate' / name) != meshes[name]['sha256']:
            raise ValueError('Current sample file/hash mismatch: ' + name)
    items = ledger['items'] + ledger['scenarios'][ledger['active_scenario']]['items']
    # Shipping is recorded once per actual order, never as an item as well.
    products = {item['product']: item for item in items if item['category'] != 'Shipping'}
    return identity, ledger, spec, manifest, meshes, products


def blank_record():
    """Template only: expected products are not assertions of orders or arrivals."""
    identity, _, _, manifest, meshes, products = sources()
    orders = {}
    for name, product in products.items():
        order = orders.setdefault(product['shop'], {
            'order_id': None, 'supplier': product['shop'], 'ordered_date': None,
            'arrival_date': None, 'shipping_paid_eur': None, 'other_paid_eur': None,
            'evidence_files': [], 'notes': None, 'items': []})
        order['items'].append({'product': name, 'quantity_ordered': None,
                               'quantity_received': None, 'paid_line_eur': None,
                               'accessories': None, 'evidence_files': []})
    return {'version': 1, 'data_kind': 'physical', 'record_date': None, 'units': UNITS.copy(),
            'source_identity': identity, 'orders': list(orders.values()),
            'hardware': {field: None for field in HARDWARE_FIELDS},
            'printing': {'revision': manifest['revision'], 'material': None,
                         'layer_height_mm': None, 'walls': None, 'infill_percent': None,
                         'finishing': None, 'deviations': None, 'evidence_files': [],
                         'samples': [{'file': name, 'sha256': meshes[name]['sha256'],
                                      'received': None, 'print_date': None,
                                      'checks': {key: {'status': 'pending', 'measurements_mm': {},
                                                       'notes': None, 'evidence_files': []}
                                                 for key in keys}}
                                     for name, keys in SAMPLES.items()]}}


def text_or_null(value, label):
    if value is not None and (not isinstance(value, str) or not value.strip()):
        raise ValueError(label + ' must be a nonempty string or null')


def integer_or_null(value, label):
    if value is not None and (type(value) is not int or value < 0):
        raise ValueError(label + ' must be a nonnegative integer or null')


def number(value, label, *, money=False):
    if value is None:
        return None
    if type(value) not in (int, float):
        raise ValueError(label + ' must be a finite nonnegative number or null')
    try:
        d = Decimal(str(value))
        if not d.is_finite() or d < 0 or (money and d != d.quantize(Decimal('.01'))):
            raise ValueError(label + ' must be finite, nonnegative, and whole cents for costs')
    except InvalidOperation as e:
        raise ValueError('Invalid number: ' + label) from e
    return d


def day(value, label):
    text_or_null(value, label)
    if value is not None:
        try:
            if date.fromisoformat(value).isoformat() != value:
                raise ValueError()
        except ValueError as e:
            raise ValueError(label + ' must be YYYY-MM-DD or null') from e


def packaged(path):
    path = Path(path).resolve()
    return any(path.is_relative_to((ROOT / folder).resolve()) for folder in PACKAGED_ROOTS)


def review(record_path, output):
    record_path, output = Path(record_path).resolve(), Path(output).resolve()
    if output.exists():
        raise FileExistsError('Output already exists: ' + str(output))
    record = load_json(record_path)
    if not isinstance(record, dict) or type(record.get('version')) is not int or record['version'] != 1:
        raise ValueError('Expected receiving record version 1')
    kind = record.get('data_kind')
    if kind not in ('physical', 'synthetic') or record.get('units') != UNITS:
        raise ValueError('Specify physical/synthetic and explicit mm/EUR units')
    if kind == 'physical' and (packaged(record_path) or packaged(output)):
        raise ValueError('Keep physical records/reports outside packaged folders; use local_records/')
    identity, ledger, spec, manifest, meshes, products = sources()
    if record.get('source_identity') != identity:
        raise ValueError('Stale or incompatible source identity; review changed sources before migrating records')
    missing, failures, warnings, evidence = [], [], [], {}

    def require(value, label):
        if value is None:
            missing.append(label)

    def files(names, label):
        if not isinstance(names, list) or any(not isinstance(n, str) or not n.strip() for n in names):
            raise ValueError(label + ' evidence_files must be a list of paths')
        if len(set(names)) != len(names):
            raise ValueError('Duplicate evidence reference: ' + label)
        for name in names:
            p = (record_path.parent / name).resolve()
            if not p.is_file():
                raise ValueError('Missing evidence file: ' + name)
            if kind == 'physical' and packaged(p):
                raise ValueError('Private evidence must stay outside packaged folders')
            evidence[name] = sha(p)
        return bool(names)

    day(record.get('record_date'), 'record_date')
    require(record.get('record_date'), 'record_date')
    orders = record.get('orders')
    if not isinstance(orders, list):
        raise ValueError('orders must be a list')
    seen, order_costs = set(), []
    known, cost_fields = Decimal(0), 0
    cost_unknown = []
    quantities = {name: {'ordered': 0, 'received': 0} for name in products}
    for i, order in enumerate(orders):
        if not isinstance(order, dict):
            raise ValueError('Order must be an object')
        label = 'orders[' + str(i) + ']'
        for field in ('order_id', 'supplier', 'notes'):
            text_or_null(order.get(field), label + '.' + field)
        for field in ('order_id', 'supplier'):
            require(order.get(field), label + '.' + field)
        if order.get('order_id') is not None:
            if order['order_id'] != order['order_id'].strip():
                raise ValueError('Order identifiers must not have surrounding whitespace')
            if order['order_id'] in seen:
                raise ValueError('Duplicate order identifier: ' + order['order_id'])
            seen.add(order['order_id'])
        for field in ('ordered_date', 'arrival_date'):
            day(order.get(field), label + '.' + field)
            require(order.get(field), label + '.' + field)
        if order.get('arrival_date') and order.get('ordered_date') and order['arrival_date'] < order['ordered_date']:
            raise ValueError('Arrival precedes order date')
        order_evidence = files(order.get('evidence_files'), label)
        if not order_evidence:
            missing.append(label + '.receipt_evidence')
        start_known, start_fields, start_unknown = known, cost_fields, len(cost_unknown)
        for field in ('shipping_paid_eur', 'other_paid_eur'):
            amount = number(order.get(field), label + '.' + field, money=True)
            if amount is None:
                cost_unknown.append(label + '.' + field)
            else:
                known += amount
                cost_fields += 1
        items = order.get('items')
        if not isinstance(items, list) or not items:
            raise ValueError('Each order requires at least one item')
        order_products = set()
        for j, item in enumerate(items):
            if not isinstance(item, dict) or item.get('product') not in products:
                raise ValueError('Unknown product; record exact ledger name or review a ledger revision first')
            name = item['product']
            if name in order_products:
                raise ValueError('Duplicate product in one order; aggregate its quantity/line payment')
            order_products.add(name)
            key = label + '.items[' + str(j) + ']'
            for field, bucket in (('quantity_ordered', 'ordered'), ('quantity_received', 'received')):
                integer_or_null(item.get(field), key + '.' + field)
                require(item.get(field), key + '.' + field)
                if item.get(field) is not None:
                    quantities[name][bucket] += item[field]
            if item.get('quantity_ordered') is not None and item.get('quantity_received') is not None and item['quantity_received'] > item['quantity_ordered']:
                raise ValueError('Received quantity exceeds ordered quantity; explain extras separately')
            text_or_null(item.get('accessories'), key + '.accessories')
            require(item.get('accessories'), key + '.accessories')
            files(item.get('evidence_files'), key)
            amount = number(item.get('paid_line_eur'), key + '.paid_line_eur', money=True)
            if amount is None:
                cost_unknown.append(key + '.paid_line_eur')
            else:
                known += amount
                cost_fields += 1
        order_costs.append({'order_id': order.get('order_id'), 'supplier': order.get('supplier'),
                            'known_payments_eur': format(known - start_known, '.2f') if cost_fields > start_fields else None,
                            'unresolved_cost_fields': cost_unknown[start_unknown:]})
    coverage = []
    for name, product in products.items():
        coverage.append({'product': name, 'required_purchase_units': product['quantity'],
                         'known_reported_ordered_units': quantities[name]['ordered'],
                         'known_reported_received_units': quantities[name]['received']})
        if quantities[name]['received'] < product['quantity']:
            missing.append('Required receipt incomplete: ' + name)
        if not any(item['product'] == name for order in orders for item in order['items']):
            cost_unknown.append('Unrecorded required product: ' + name)
    hardware = record.get('hardware')
    if not isinstance(hardware, dict) or set(hardware) != set(HARDWARE_FIELDS):
        raise ValueError('hardware must contain the documented identity/interface fields')
    for field, value in hardware.items():
        require(value, 'hardware.' + field)
        if field == 'horn_hole_radii_mm':
            if value is not None:
                if not isinstance(value, list) or not value:
                    raise ValueError('horn_hole_radii_mm must be a nonempty list or null')
                for v in value:
                    if number(v, field) in (None, Decimal(0)):
                        raise ValueError('Horn hole radii must be positive')
        elif field.endswith('_mm'):
            if value is not None and number(value, field) == 0:
                raise ValueError('Screw lengths must be positive')
        else:
            text_or_null(value, 'hardware.' + field)
    printing = record.get('printing')
    if not isinstance(printing, dict) or printing.get('revision') != manifest['revision']:
        raise ValueError('Print revision mismatch')
    for field in ('material', 'finishing', 'deviations'):
        text_or_null(printing.get(field), 'printing.' + field)
        require(printing.get(field), 'printing.' + field)
    if printing.get('material') is not None and printing['material'].upper() != 'PETG':
        warnings.append('Reported material differs from PETG; engineering review required')
    for field in ('layer_height_mm', 'infill_percent'):
        v = number(printing.get(field), 'printing.' + field)
        require(v, 'printing.' + field)
        if v is not None and ((field == 'layer_height_mm' and v == 0) or (field == 'infill_percent' and v > 100)):
            raise ValueError('Invalid positive print setting: ' + field)
    integer_or_null(printing.get('walls'), 'printing.walls')
    require(printing.get('walls'), 'printing.walls')
    if printing.get('walls') == 0:
        raise ValueError('Print walls must be positive')
    for field in ('layer_height_mm', 'walls', 'infill_percent'):
        if printing.get(field) is not None and printing[field] != spec['manufacturing'][field]:
            warnings.append('Reported ' + field + ' differs from provisional print instructions; review required')
    files(printing.get('evidence_files'), 'printing')
    samples = printing.get('samples')
    if not isinstance(samples, list) or len(samples) != len(SAMPLES):
        raise ValueError('Require exactly the two individual fit samples')
    seen_samples, checks = set(), []
    for sample in samples:
        if not isinstance(sample, dict) or sample.get('file') not in SAMPLES:
            raise ValueError('Unknown sample')
        name = sample['file']
        if name in seen_samples or sample.get('sha256') != meshes[name]['sha256']:
            raise ValueError('Duplicate sample or stale sample hash: ' + name)
        seen_samples.add(name)
        if sample.get('received') is not None and type(sample['received']) is not bool:
            raise ValueError('Sample received must be true, false or null')
        if sample.get('received') is not True:
            missing.append('Sample not reported received: ' + name)
        day(sample.get('print_date'), name + '.print_date')
        require(sample.get('print_date'), name + '.print_date')
        if not isinstance(sample.get('checks'), dict) or set(sample['checks']) != set(SAMPLES[name]):
            raise ValueError('Sample check list mismatch: ' + name)
        for key, check in sample['checks'].items():
            if not isinstance(check, dict) or check.get('status') not in ('pending', 'passed', 'failed'):
                raise ValueError('Check requires pending/passed/failed status')
            label = name + ':' + key
            text_or_null(check.get('notes'), label + '.notes')
            m = check.get('measurements_mm')
            if not isinstance(m, dict) or any(not isinstance(k, str) or not k.strip() for k in m):
                raise ValueError('measurements_mm must be an object of named dimensions')
            for dimension, value in m.items():
                if number(value, label + '.' + dimension) is None:
                    missing.append(label + '.' + dimension)
            has_evidence = files(check.get('evidence_files'), label)
            if check['status'] == 'pending':
                missing.append(label)
            else:
                if sample.get('received') is not True:
                    raise ValueError('Cannot report a fit check on a sample not received')
                if not has_evidence:
                    missing.append(label + '.photo_or_measurement_evidence')
                if check['notes'] is None:
                    missing.append(label + '.description')
                if key in ('ear_holes', 'mounting_stack', 'horn_attachment') and not m:
                    missing.append(label + '.dimensions_mm')
            if check['status'] == 'failed':
                failures.append(label)
            checks.append({'sample': name, 'check': key, **check})
    missing.extend(cost_unknown)
    missing = sorted(set(missing))
    # Quoted values are contextual only: never add quotes to actual payments.
    from tools.budget_gate import check_basket
    quote = check_basket(ledger)
    report = {
        'version': 1, 'state': 'diagnostic_awaiting_human_review', 'data_kind': kind,
        'record_complete': not missing, 'missing_checks_or_fields': missing,
        'reported_failures': failures, 'warnings': warnings,
        'source_identity': identity, 'record_sha256': sha(record_path),
        'reviewer_sha256': sha(Path(__file__)), 'evidence_sha256': evidence,
        'spending': {'recorded_payments_eur': format(known, '.2f') if cost_fields else None,
                     'known_payment_fields': cost_fields, 'unresolved_costs': cost_unknown,
                     'orders': order_costs,
                     'scope': 'Recorded payments only; not a complete delivered robot total',
                     'complete_delivered_robot_total_eur': None,
                     'budget_max_eur': ledger['budget_max_eur'],
                     'recorded_payments_exceed_cap': known > Decimal(str(ledger['budget_max_eur'])),
                     'quoted_basket_snapshot': quote},
        'required_product_coverage': coverage, 'orders_reported': orders, 'hardware_reported': hardware,
        'printing_reported': printing, 'sample_checks': checks,
        'provisional_drawing_comparisons_mm': {
            'horn_slot_radius_interval': [1000 * x for x in spec['hardware_interfaces']['horn']['designed_slot_radius_interval']],
            'horn_slot_width': 1000 * spec['hardware_interfaces']['horn']['designed_frame_clearance_width'],
            'ear_thickness_estimate': 1000 * spec['hardware_interfaces']['ear_bolt']['ear_thickness_estimate']},
        'physically_verified': False, 'manufacturing_approved': False,
        'budget_cleared': False, 'gates_updated': False,
        'limits': ['Fit assertions are human-reported evidence awaiting review; hashes do not establish truth.',
                   'Drawing dimensions are provisional comparisons, not invented fit tolerances.',
                   'No automatic ledger, geometry, calibration, purchase or release update.',
                   'Incomplete receipts never establish complete delivered cost; unknown amounts are not zero.',
                   'Synthetic examples are not arrivals, purchases, measurements or fit evidence.']}
    markdown = render_report(report)
    output.mkdir(parents=True, exist_ok=False)
    if kind == 'physical':
        (output / 'PRIVATE_RECEIVING_RECORD').write_text('Private receiving report: do not package.\n')
    (output / 'report.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    (output / 'report.md').write_text(markdown)
    return report


def render_report(report):
    def safe(value):
        return str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')
    spending = report['spending']
    lines = ['# Receiving and sample review — ' + report['data_kind'].upper(), '',
             '**Diagnostic: human-reported evidence awaiting review. No gates approved.**', '',
             'Record fields complete: ' + str(report['record_complete']) + '.',
             'Recorded payments: ' + str(spending['recorded_payments_eur']) + ' EUR (known entries only).',
             'Complete delivered robot total: **unknown**. Quotes remain separate.', '',
             '## Recorded payments', '', '| Order / supplier | Known payments EUR | Unresolved cost fields |',
             '|---|---:|---:|']
    for order in spending['orders']:
        lines.append('| ' + safe(str(order['order_id']) + ' / ' + str(order['supplier'])) + ' | ' +
                     safe(order['known_payments_eur']) + ' | ' + str(len(order['unresolved_cost_fields'])) + ' |')
    lines.extend(['', '## Sample checklist', '', '| Sample / check | Reported result |', '|---|---|'])
    for c in report['sample_checks']:
        lines.append('| ' + safe(c['sample'] + ' / ' + c['check']) + ' | ' + safe(c['status']) + ' |')
    for title, values in (('Reported failures', report['reported_failures']),
                          ('Missing checks / fields', report['missing_checks_or_fields']),
                          ('Review notes', report['warnings'] + report['limits'])):
        lines.extend(['', '## ' + title, ''])
        lines.extend('- ' + safe(v) for v in values or ['None reported; this is not approval.'])
    lines.extend(['', 'Next: review actual servo/accessories and both samples; resolve failures before seven frames.', ''])
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('record', type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    try:
        report = review(args.record, args.output)
    except (ValueError, OSError, KeyError, TypeError) as e:
        print('Receiving review refused: ' + str(e), file=sys.stderr)
        return 1
    print(json.dumps({k: report[k] for k in ('state', 'data_kind', 'record_complete', 'reported_failures')}))
    return 2 if (report['missing_checks_or_fields'] or report['reported_failures'] or
                 report['warnings'] or report['spending']['recorded_payments_exceed_cap']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
