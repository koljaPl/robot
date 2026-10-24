"""Versioned persistent calibration, shared policy identity and deployment gate."""
from pathlib import Path
import hashlib
import json
import numpy as np
from robot_config import ROOT, JOINT_NAMES, JOINT_LOW, JOINT_HIGH, HOME


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def configuration_identity(calibration=None):
    names = ('physical_spec.json', 'robot.xml', 'robot_config.py', 'servo_control.py',
             'imu_observation.py', 'humanoid_env.py', 'gait_metrics.py', 'hardware_interface.py', 'calibration.py', 'firmware/main.cpp', 'firmware/control.h')
    files = {n: hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names}
    return {'configuration': digest(files), 'files': files,
            'calibration': digest(calibration) if calibration else None}


def load_calibration(path, *, require_valid=True):
    c = json.loads(Path(path).read_text())
    if c.get('version') != 1 or c.get('joint_order') != list(JOINT_NAMES):
        raise ValueError('Unsupported calibration version/joint order')
    if require_valid and (c.get('state') != 'measured' or not c.get('validated')):
        raise ValueError('Policy operation requires measured, validated calibration')
    for key in ('sign', 'zero_us', 'us_per_rad', 'pulse_min_us', 'pulse_max_us', 'safe_low_rad', 'safe_high_rad'):
        arr = np.asarray(c[key], float)
        if arr.shape != (6,) or not np.isfinite(arr).all():
            raise ValueError('Invalid calibration array: '+key)
    sign, zero, gain = np.array(c['sign']), np.array(c['zero_us']), np.array(c['us_per_rad'])
    low, high = np.array(c['pulse_min_us']), np.array(c['pulse_max_us'])
    qlo, qhi = np.array(c['safe_low_rad']), np.array(c['safe_high_rad'])
    if np.any(abs(sign) != 1) or np.any(gain <= 0) or np.any(low < 500) or np.any(high > 2500) or np.any(low >= high):
        raise ValueError('Unsafe pulse calibration')
    # Training and hardware must share the entire mapping. Narrower bench ranges need a new model.
    if not np.allclose(qlo, JOINT_LOW, atol=1e-10) or not np.allclose(qhi, JOINT_HIGH, atol=1e-10):
        raise ValueError('Calibration safe limits mismatch physical specification; rebuild and retrain')
    for q in (qlo, qhi, HOME):
        pulses = zero + sign*gain*q
        if np.any(pulses < low+.5) or np.any(pulses > high-.5):
            raise ValueError('Safe angles cannot be represented within pulse bounds')
    R = np.asarray(c['imu']['rotation_sensor_to_body'], float)
    if R.shape != (3,3) or not np.isfinite(R).all() or not np.allclose(R@R.T, np.eye(3), atol=1e-5) or not np.isclose(np.linalg.det(R), 1):
        raise ValueError('IMU alignment must be a proper rotation')
    for key in ('gyro_bias_rad_s','accel_bias_m_s2'):
        a = np.asarray(c['imu'][key], float)
        if a.shape != (3,) or not np.isfinite(a).all():
            raise ValueError('Invalid IMU bias')
    if not 0 < c.get('max_target_speed_rad_s', 0) <= np.pi:
        raise ValueError('Invalid slew limit')
    return c


def pulses_to_angles(pulses, c):
    return (np.asarray(pulses)-c['zero_us'])/(np.array(c['sign'])*c['us_per_rad'])


def check_policy(model_path, *, calibration=None):
    path = Path(model_path)
    if path.suffix != '.zip':
        path = path.with_suffix('.zip')
    metadata = json.loads(path.with_suffix('.manifest.json').read_text())
    if metadata['model_sha256'] != hashlib.sha256(path.read_bytes()).hexdigest():
        raise ValueError('Policy file hash mismatch')
    identity = configuration_identity(calibration)
    if metadata['identity']['configuration'] != identity['configuration']:
        raise ValueError('Policy model/control configuration is incompatible')
    if calibration is not None and metadata['identity']['calibration'] != identity['calibration']:
        raise ValueError('Policy was not trained/approved for this calibration fingerprint')
    return metadata
