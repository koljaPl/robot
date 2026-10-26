import csv
import json

import numpy as np
import pytest

from tools.validate_measurement import UNITS, validate_trial


def fixture(tmp_path, mode='moving'):
    t = np.linspace(0, 1, 201)
    u = np.where(t < .1, 0, .2)
    q = .2*(1-np.exp(-np.maximum(0, t-.13)/.1))
    if mode == 'stuck': q[:] = 0
    if mode == 'wrong_sign': q *= -1
    csv_path = tmp_path/'step.csv'
    with csv_path.open('w', newline='') as f:
        w = csv.writer(f); w.writerow(UNITS)
        w.writerows(zip(t, u, q, np.full(len(t), 5.), np.zeros(len(t))))
    metadata = {'version': 1, 'data_kind': 'synthetic', 'servo_id': 'SYNTHETIC_ONLY',
                'joint_index': 0, 'angle_source': 'synthetic_generator',
                'measurement_method': 'known first-order test fixture, not hardware',
                'clock_alignment': 'same generated timebase', 'angle_uncertainty_rad': .0001,
                'evidence_files': [], 'units': UNITS}
    path = tmp_path/'provenance.json'; path.write_text(json.dumps(metadata))
    return csv_path, path, metadata


def test_resolved_synthetic_step_is_never_promoted_to_physical_calibration(tmp_path):
    csv_path, path, _ = fixture(tmp_path)
    r = validate_trial(csv_path, path)
    assert r['ready_for_human_fit_review'] and not r['quality_flags']
    assert r['data_kind'] == 'synthetic' and not r['physically_verified'] and not r['calibration_validated']
    assert r['first_order_fit']['delay_s'] == pytest.approx(.03, abs=.004)


@pytest.mark.parametrize('mode,flag', [('stuck', 'insufficient_resolved_motion'),
                                     ('wrong_sign', 'response_direction_disagrees_with_command')])
def test_low_error_fit_cannot_hide_stuck_or_reversed_response(tmp_path, mode, flag):
    c, p, _ = fixture(tmp_path, mode)
    r = validate_trial(c, p)
    assert not r['ready_for_human_fit_review'] and flag in r['quality_flags']


@pytest.mark.parametrize('source', ['acknowledged_commands', 'target_rad', 'simulated_true_joint'])
def test_command_or_privileged_angles_cannot_masquerade_as_external_measurement(tmp_path, source):
    c, p, m = fixture(tmp_path); m.update(data_kind='physical', angle_source=source)
    p.write_text(json.dumps(m))
    with pytest.raises(ValueError, match='externally observed'): validate_trial(c, p)


def test_physical_record_requires_original_external_evidence_and_units(tmp_path):
    c, p, m = fixture(tmp_path); m.update(data_kind='physical', angle_source='external_video')
    p.write_text(json.dumps(m))
    with pytest.raises(ValueError, match='requires original'): validate_trial(c, p)
    m['evidence_files'] = ['missing.mp4']; p.write_text(json.dumps(m))
    with pytest.raises(ValueError, match='Missing evidence'): validate_trial(c, p)
    m['units'] = {}; p.write_text(json.dumps(m))
    with pytest.raises(ValueError, match='SI units'): validate_trial(c, p)


def test_nan_timestamps_and_missing_values_are_rejected(tmp_path):
    c, p, _ = fixture(tmp_path)
    c.write_text(c.read_text().replace('0.005,', 'nan,', 1))
    with pytest.raises(ValueError, match='finite'): validate_trial(c, p)
