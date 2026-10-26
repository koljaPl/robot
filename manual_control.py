"""Reviewed six-joint movements. Offline preview by default; never auto-arm.

Targets and acknowledgements are command coordinates, NOT measured shaft angles.
Hardware use requires prior human bench checks and measured validated calibration.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from calibration import configuration_identity, load_calibration
from hardware_interface import command_frame
from imu_observation import GravityEstimator
from robot_config import CONTROL_DT, HOME, JOINT_NAMES, IMU_ACCEL_RANGE, IMU_GYRO_RANGE
from serial_robot import SerialRobot


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def vector(value, label):
    if not isinstance(value, list) or len(value) != 6 or any(
            isinstance(v, bool) or not isinstance(v, (int, float)) for v in value):
        raise ValueError(label+' must contain six numeric radian targets')
    q = np.asarray(value, dtype=float)
    if not np.isfinite(q).all():
        raise ValueError(label+' must be finite')
    return q


def compile_trajectory(movement, calibration, *, start=None):
    if type(movement.get('version')) is not int or movement['version'] != 1:
        raise ValueError('Movement version must be1')
    if movement.get('joint_order') != list(JOINT_NAMES):
        raise ValueError('Movement joint order mismatch')
    declared = vector(movement.get('initial_targets_rad'), 'initial_targets_rad')
    q = declared if start is None else np.asarray(start, float)
    if q.shape != (6,) or not np.isfinite(q).all():
        raise ValueError('Invalid acknowledged start')
    low, high = np.asarray(calibration['safe_low_rad']), np.asarray(calibration['safe_high_rad'])
    if np.any(declared < low) or np.any(declared > high) or np.any(q < low) or np.any(q > high):
        raise ValueError('Initial command outside calibrated safe angles')
    segments = movement.get('segments')
    if not isinstance(segments, list) or not segments or len(segments) > 100:
        raise ValueError('Need1..100timed segments')
    result = [q.copy()]
    for segment in segments:
        if not isinstance(segment, dict):
            raise ValueError('Each segment needs duration_s and targets_rad')
        duration = segment.get('duration_s')
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not np.isfinite(duration):
            raise ValueError('Segment duration must be finite numeric seconds')
        if not CONTROL_DT <= duration <= 30:
            raise ValueError('Segment duration must be20ms..30s')
        ticks = round(duration/CONTROL_DT)
        if ticks < 1 or not np.isclose(duration, ticks*CONTROL_DT, rtol=0, atol=1e-9):
            raise ValueError('Durations must be positive multiples of20ms')
        # Including one last command interval, no session exceeds30s.
        if (len(result)+ticks)*CONTROL_DT > 30+1e-9:
            raise ValueError('Manual session exceeds30seconds')
        target = vector(segment.get('targets_rad'), 'targets_rad')
        if np.any(target < low) or np.any(target > high):
            raise ValueError('Target outside calibrated safe angles')
        if np.any(np.abs(target-q)/duration > calibration['max_target_speed_rad_s']+1e-12):
            raise ValueError('Movement exceeds calibrated commanded slew')
        result.extend(q+(target-q)*(i/ticks) for i in range(1, ticks+1))
        q = target
    targets = np.asarray(result)
    # Validate wire representation offline too; no connection is required.
    for row in targets:
        command_frame(0, 0, row)
    return np.arange(len(targets))*CONTROL_DT, targets


def run_sequence(sequence_path, calibration_path, output, *, arm=False, port=None,
                 robot_factory=None, clock=None):
    sequence_path, calibration_path, output = map(Path, (sequence_path, calibration_path, output))
    c = load_calibration(calibration_path, require_valid=arm)
    raw = sequence_path.read_bytes()
    movement = json.loads(raw)
    if not isinstance(movement, dict):
        raise ValueError('Movement must be a JSON object')
    times, targets = compile_trajectory(movement, c)
    if arm and not port:
        raise ValueError('--arm requires a USB port')
    if port and not arm:
        raise ValueError('Offline preview does not accept a port; explicit --arm required')
    output.mkdir(parents=True, exist_ok=False)
    manifest = {'mode': 'hardware_manual' if arm else 'offline_preview', 'status': 'started',
                'identity': configuration_identity(c), 'calibration_record': c,
                'movement': movement, 'movement_sha256': hashlib.sha256(raw).hexdigest(),
                'calibration_file_sha256': sha(calibration_path), 'command_hz': 1/CONTROL_DT,
                'duration_s': len(targets)*CONTROL_DT, 'physically_verified': False,
                'source_sha256': {n: sha(Path(__file__).parent/n) for n in (
                    'manual_control.py', 'serial_robot.py', 'hardware_interface.py', 'calibration.py', 'imu_observation.py')},
                'limits': ['Targets/acknowledgements are not measured shaft positions.',
                           'Software STOP does not physically isolate servo power.',
                           'A validated JSON assertion does not replace human bench/fit checks.']}
    robot = None
    failure = None
    clock = clock or time.monotonic
    try:
        if arm:
            robot = (robot_factory or SerialRobot)(port, c)
            robot.handshake()  # existing transport checks model/calibration fingerprints
            R = np.asarray(c['imu']['rotation_sensor_to_body'])
            ab, gb = np.asarray(c['imu']['accel_bias_m_s2']), np.asarray(c['imu']['gyro_bias_rad_s'])
            estimator = GravityEstimator()
            last_ms = None

            def inspect(t, expected_status):
                nonlocal last_ms
                if t.status != expected_status:
                    raise RuntimeError('Firmware fault/disarm status '+str(t.status))
                accel, gyro = np.asarray(t.accelerometer), np.asarray(t.gyroscope)
                if accel.shape != (3,) or gyro.shape != (3,) or not np.isfinite([accel, gyro]).all():
                    raise RuntimeError('Invalid IMU sample')
                if np.any(abs(accel) >= IMU_ACCEL_RANGE*.99) or np.any(abs(gyro) >= IMU_GYRO_RANGE*.99):
                    raise RuntimeError('IMU saturation')
                accel, gyro = R@(accel-ab), R@(gyro-gb)
                if last_ms is None:
                    if not .8*9.81 < np.linalg.norm(accel) < 1.2*9.81:
                        raise RuntimeError('Need stationary gravity sample before arming')
                    estimator.reset(accel)
                else:
                    dt = (t.timestamp_ms-last_ms) & 0xffffffff
                    if not 0 < dt < 100:
                        raise RuntimeError('Stale/reordered/gapped telemetry timestamp')
                    estimator.update(gyro, accel, dt/1000)
                last_ms = t.timestamp_ms
                if estimator.gravity[2] > -.7:
                    raise RuntimeError('IMU tilt stop')

            deadline = clock()+.100
            while True:
                kind, initial = robot.read()
                if clock() > deadline:
                    raise TimeoutError('No fresh startup telemetry within100ms')
                if kind == 'telemetry':
                    inspect(initial, 0)  # matched, calibrated, IMU good, disarmed
                    startup_received = clock()
                    break
                if kind == 'identity' and initial != 0:
                    raise RuntimeError('Unexpected startup firmware status '+str(initial))
            start = np.asarray(initial.applied_targets, float)
            tolerance = .5/np.asarray(c['us_per_rad'])+.0005+1e-9
            declared = np.asarray(movement['initial_targets_rad'])
            if start.shape != (6,) or not np.isfinite(start).all() or np.any(abs(start-declared) > tolerance):
                raise ValueError('Acknowledged start differs from reviewed movement start')
            times, targets = compile_trajectory(movement, c, start=start)
            manifest['acknowledged_start_rad'] = start.tolist()
            manifest['acknowledged_start_is_shaft_feedback'] = False
        with (output/'trajectory.csv').open('x', newline='') as f:
            writer = csv.writer(f); writer.writerow(['time_s', *[n+'_requested_rad' for n in JOINT_NAMES]])
            writer.writerows(zip(times, *targets.T))
        if not arm:
            manifest['status'] = 'preview_complete'
            return manifest

        with (output/'commands.csv').open('x', newline='') as commands, \
                (output/'telemetry.csv').open('x', newline='') as telemetry:
            cw, tw = csv.writer(commands), csv.writer(telemetry)
            cw.writerow(['host_elapsed_s', 'index', 'sequence', *[n+'_requested_rad' for n in JOINT_NAMES]])
            tw.writerow(['host_elapsed_s', 'mcu_ms', 'ack', 'status',
                         *[n+'_ack_rad' for n in JOINT_NAMES], 'raw_ax','raw_ay','raw_az','raw_gx','raw_gy','raw_gz'])
            if clock()-startup_received > .050:
                raise TimeoutError('Startup telemetry aged before arming')
            robot.arm()  # explicit caller request, measured calibration, matching handshake
            started = clock(); next_command = started; last_telem = started
            index = 0; last_ack = None; last_sent_at = None
            while True:
                now = clock()
                if index < len(targets) and now-started > 30:
                    raise TimeoutError('Manual command session exceeded30seconds')
                if now-last_telem > .050:
                    raise TimeoutError('Fresh telemetry deadline exceeded50ms')
                if index < len(targets) and now+1e-10 >= next_command:
                    if now-next_command > .040:
                        raise TimeoutError('PC command deadline missed by40ms')
                    robot.command(targets[index])
                    last_sent_at = now
                    cw.writerow([now-started, index, robot.last_sequence, *targets[index]])
                    index += 1
                    # Never burst commands to catch up after scheduling jitter:
                    # >=20ms spacing preserves the validated commanded slew.
                    next_command = now+CONTROL_DT
                if index == len(targets) and now+1e-10 >= last_sent_at+CONTROL_DT:
                    if last_ack == robot.last_sequence:
                        break
                    if now-last_sent_at > .080:
                        raise TimeoutError('Final command not acknowledged within80ms')
                kind, t = robot.read()
                now = clock()
                if kind != 'telemetry':
                    if kind == 'identity' and t != 1:
                        raise RuntimeError('Firmware fault/disarm status '+str(t))
                    continue
                tw.writerow([now-started, t.timestamp_ms, t.sequence, t.status,
                             *t.applied_targets, *t.accelerometer, *t.gyroscope])
                if now-last_telem > .050:
                    raise TimeoutError('Fresh telemetry deadline exceeded50ms')
                # Record even a fault sample before rejecting it.
                inspect(t, 1)
                if robot.last_sequence is not None and ((robot.last_sequence-t.sequence) & 0xffff) > 4:
                    raise RuntimeError('Applied command acknowledgement is too old or ahead')
                last_ack = t.sequence
                last_telem = now
            manifest['commands_sent'] = index
            manifest['final_command_acknowledged'] = True
        manifest['status'] = 'completed'
        return manifest
    except BaseException as e:
        failure = e
        manifest['status'] = 'interrupted' if isinstance(e, KeyboardInterrupt) else 'failed'
        manifest['error'] = type(e).__name__+': '+str(e)
        raise
    finally:
        close_error = None
        if robot is not None:
            try:
                robot.close()  # SerialRobot.close sends STOP and always closes transport
                manifest['stop_and_close'] = 'requested'
            except Exception as e:
                close_error = e
                manifest['stop_and_close'] = 'failed: '+str(e)
                if failure is None:
                    manifest['status'] = 'failed'
        (output/'manifest.json').write_text(json.dumps(manifest, indent=2, allow_nan=False)+'\n')
        if close_error is not None and failure is None:
            raise close_error


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sequence', type=Path, required=True)
    p.add_argument('--calibration', type=Path, default=Path(__file__).parent/'calibrations/example.invalid.json')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--arm', action='store_true')
    p.add_argument('--port')
    a = p.parse_args()
    result = run_sequence(a.sequence, a.calibration, a.output, arm=a.arm, port=a.port)
    print(json.dumps({k: result[k] for k in ('mode', 'status', 'duration_s', 'physically_verified')}))


if __name__ == '__main__':
    main()
