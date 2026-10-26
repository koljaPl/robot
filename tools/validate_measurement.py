"""Review externally measured step-response intake; never validates calibration.

Requires a versioned provenance sidecar. Synthetic fixtures remain synthetic.
Quality thresholds are conservative diagnostic screens, not servo specifications.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.fit_response import fit

COLUMNS = ('time_s', 'target_rad', 'angle_rad', 'voltage_v', 'load_nm')
UNITS = {'time_s': 's', 'target_rad': 'rad', 'angle_rad': 'rad',
         'voltage_v': 'V', 'load_nm': 'N*m'}
EXTERNAL_ANGLE_SOURCES = ('external_video', 'external_protractor', 'external_encoder')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_trial(csv_path, metadata_path):
    csv_path, metadata_path = Path(csv_path), Path(metadata_path)
    meta = json.loads(metadata_path.read_text())
    if meta.get('version') != 1 or meta.get('data_kind') not in ('physical', 'synthetic'):
        raise ValueError('Specify version1 and data_kind physical or synthetic')
    if meta.get('units') != UNITS:
        raise ValueError('Explicit SI units must match the CSV schema')
    if not isinstance(meta.get('joint_index'), int) or isinstance(meta['joint_index'], bool) or not 0 <= meta['joint_index'] < 6:
        raise ValueError('joint_index must be0..5 in shared joint order')
    for key in ('servo_id', 'clock_alignment', 'measurement_method'):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise ValueError('Missing provenance: '+key)
    source = meta.get('angle_source')
    if source not in EXTERNAL_ANGLE_SOURCES and not (meta['data_kind'] == 'synthetic' and source == 'synthetic_generator'):
        raise ValueError('Angles must be externally observed, never commands or acknowledgements')
    uncertainty = meta.get('angle_uncertainty_rad')
    if isinstance(uncertainty, bool) or not isinstance(uncertainty, (int, float)) or not np.isfinite(uncertainty) or uncertainty <= 0:
        raise ValueError('Positive finite angle_uncertainty_rad required')
    evidence = meta.get('evidence_files', [])
    if not isinstance(evidence, list) or any(not isinstance(s, str) or not s.strip() for s in evidence):
        raise ValueError('evidence_files must be a list of nonempty paths')
    if meta['data_kind'] == 'physical' and not evidence:
        raise ValueError('Physical data requires original external measurement evidence')
    hashes = {}
    for name in evidence:
        path = metadata_path.parent/name
        if not path.is_file():
            raise ValueError('Missing evidence file: '+name)
        hashes[name] = sha(path)
    with csv_path.open(newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(COLUMNS):
            raise ValueError('Expected CSV header: '+','.join(COLUMNS))
        try:
            rows = [[float(row[k]) for k in COLUMNS] for row in reader]
        except (ValueError, TypeError, KeyError) as e:
            raise ValueError('All CSV values must be numeric and present') from e
    values = np.asarray(rows, float)
    if values.shape[0] < 20 or values.ndim != 2 or values.shape[1] != 5 or not np.isfinite(values).all():
        raise ValueError('Need at least20 complete finite samples')
    t, u, q, voltage, load = values.T
    if np.any(np.diff(t) <= 0) or np.any(voltage <= 0):
        raise ValueError('Need increasing timestamps and positive recorded voltage')
    changes = np.flatnonzero(np.abs(np.diff(u)) > 1e-5)
    if len(changes) != 1:
        raise ValueError('Use one isolated command step per file')
    index = changes[0]+1
    if index < 3 or len(t)-index < 10 or t[-1]-t[index] < .5:
        raise ValueError('Need>=3pre-step,>=10post-step samples and>=0.5s post-step recording')
    amplitude = u[-1]-u[0]
    if abs(amplitude) < np.deg2rad(5):
        raise ValueError('Need a step of at least5degrees for this diagnostic')
    data = np.array(list(zip(t, u, q)), dtype=[(k, float) for k in COLUMNS[:3]])
    fitted = fit(data)
    q0 = float(np.median(q[:index]))
    response = float(np.median(q[-max(3, len(q)//10):])-q0)
    flags = []
    if abs(response) < max(3*uncertainty, .1*abs(amplitude)):
        flags.append('insufficient_resolved_motion')
    elif response*amplitude <= 0:
        flags.append('response_direction_disagrees_with_command')
    if not .5 <= fitted['step_gain'] <= 1.5:
        flags.append('gain_outside_diagnostic_screen')
    if fitted['delay_s'] >= .078 or fitted['time_constant_s'] <= .015001 or fitted['time_constant_s'] >= .499999:
        flags.append('fit_at_search_boundary')
    if np.deg2rad(fitted['rmse_deg']) > max(3*uncertainty, .1*abs(amplitude)):
        flags.append('residual_exceeds_diagnostic_screen')
    directed = (q-q0)*np.sign(amplitude)
    if float(np.max(directed)) > 1.2*abs(response)+3*uncertainty:
        flags.append('overshoot_or_nonfirstorder_response')
    if np.any((voltage < 4.8) | (voltage > 6.0)):
        flags.append('recorded_voltage_outside_selected_servo_claim')
    return {'state': 'intake review only, not validated actuator or calibration',
            'data_kind': meta['data_kind'], 'physically_verified': False,
            'calibration_validated': False, 'metadata': meta, 'samples': len(t),
            'source_sha256': {'csv': sha(csv_path), 'metadata': sha(metadata_path), 'evidence': hashes},
            'time_span_s': float(t[-1]-t[0]), 'post_step_s': float(t[-1]-t[index]),
            'command_step_rad': float(amplitude), 'observed_response_rad': response,
            'voltage_range_v': [float(voltage.min()), float(voltage.max())],
            'load_range_nm': [float(load.min()), float(load.max())], 'first_order_fit': fitted,
            'quality_flags': flags, 'ready_for_human_fit_review': not flags,
            'limits': ['Provenance assertions require human/video review; hashes do not establish truth.',
                       'Screens are diagnostic hypotheses, not hardware tolerances.',
                       'One step cannot identify sustainable torque, backlash or MuJoCo gains uniquely.',
                       'Never automatically update calibration, physical parameters or release gates.']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv', type=Path)
    p.add_argument('--metadata', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = validate_trial(a.csv, a.metadata)
    with a.output.open('x') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps({k: result[k] for k in ('data_kind', 'samples', 'quality_flags', 'ready_for_human_fit_review')}))
    return 0 if result['ready_for_human_fit_review'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
