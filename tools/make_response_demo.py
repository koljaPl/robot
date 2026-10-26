"""Generate deterministic SYNTHETIC servo-response examples, never measurements."""
import argparse
import csv
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.validate_measurement import COLUMNS, UNITS, sha


def create(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    cases = {
        'fit': {'step_s': .15, 'amplitude_rad': .2, 'baseline_rad': .04,
                'delay_s': .03, 'tau_s': .1, 'gain': .95, 'voltage_v': 5., 'load_nm': 0.},
        'matching': {'step_s': .2, 'amplitude_rad': -.14, 'baseline_rad': -.06,
                     'delay_s': .03, 'tau_s': .1, 'gain': .95, 'voltage_v': 5., 'load_nm': 0.},
        'mismatched': {'step_s': .25, 'amplitude_rad': .16, 'baseline_rad': .03,
                       'delay_s': .065, 'tau_s': .23, 'gain': .7, 'voltage_v': 4.85, 'load_nm': .005}}
    generation = {'data_kind': 'synthetic', 'physically_verified': False,
                  'generator_sha256': sha(__file__), 'cases': cases,
                  'note': 'Invented first-order fixtures for software demonstration, not MG90S specifications.'}
    (output/'generation.json').write_text(json.dumps(generation, indent=2)+'\n')
    for name, p in cases.items():
        t = np.arange(241)*.005
        u = np.where(t < p['step_s'], 0., p['amplitude_rad'])
        q = p['baseline_rad'] + p['gain']*p['amplitude_rad']*(
            1-np.exp(-np.maximum(0, t-p['step_s']-p['delay_s'])/p['tau_s']))
        with (output/(name+'.csv')).open('x', newline='') as f:
            w = csv.writer(f);w.writerow(COLUMNS)
            w.writerows(zip(t,u,q,np.full(len(t),p['voltage_v']),np.full(len(t),p['load_nm'])))
        meta = {'version': 1, 'data_kind': 'synthetic', 'servo_id': 'SYNTHETIC_ONLY_S6_SERVO',
                'joint_index': 0, 'angle_source': 'synthetic_generator',
                'measurement_method': 'Deterministic first-order fixture; no physical observation',
                'clock_alignment': 'Same generated timebase', 'angle_uncertainty_rad': float(np.deg2rad(.1)),
                'evidence_files': ['generation.json'], 'units': UNITS,
                'note': 'Shared generation metadata is not proof of independent physical trials.'}
        (output/(name+'.json')).write_text(json.dumps(meta, indent=2)+'\n')
    def trial(name): return {'csv': name+'.csv', 'metadata': name+'.json'}
    manifest = {'version': 1, 'fit_trial': trial('fit'),
                'validation_trials': [trial('matching'),trial('mismatched')],
                'note': 'SYNTHETIC ONLY. No calibration, model or physical gate may be updated.'}
    (output/'review.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args();create(a.output)
    print(json.dumps({'data_kind': 'synthetic', 'physically_verified': False, 'manifest': str(a.output/'review.json')}))
