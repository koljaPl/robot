"""Preview initial bench sessions offline; --execute explicitly enables USB.

Read-only by default; --channel requests one constant 1400..1600us bench pulse.
Never policy-arms. Command acknowledgements are not measured shaft positions.
"""
import argparse
import csv
import hashlib
import json
import time
from pathlib import Path

import numpy as np

from calibration import configuration_identity, load_calibration
from robot_config import CONTROL_DT, IMU_ACCEL_RANGE, IMU_GYRO_RANGE, JOINT_NAMES
from serial_robot import SerialRobot


ROOT = Path(__file__).resolve().parent


def run_bench(output, *, calibration_path=ROOT/'calibrations/example.invalid.json',
              seconds=None, channel=None, pulse_us=None, execute=False, port=None,
              robot_factory=None, clock=None):
    if channel is not None and (type(channel) is not int or not 0 <= channel < 6):
        raise ValueError('Channel must be an integer0..5')
    if channel is None and pulse_us is not None:
        raise ValueError('Pulse requires an explicit channel')
    if channel is not None:
        pulse_us = 1500 if pulse_us is None else pulse_us
        if type(pulse_us) is not int or not 1400 <= pulse_us <= 1600:
            raise ValueError('Bench pulse must be integer1400..1600us')
    seconds = (2. if channel is not None else 10.) if seconds is None else seconds
    maximum = 5 if channel is not None else 60
    if (isinstance(seconds, bool) or not isinstance(seconds, (int, float))
            or not np.isfinite(seconds) or not CONTROL_DT <= seconds <= maximum):
        raise ValueError(f'Duration must be20ms..{maximum}s')
    ticks = round(seconds/CONTROL_DT)
    if not np.isclose(seconds, ticks*CONTROL_DT, rtol=0, atol=1e-9):
        raise ValueError('Duration must be a multiple of20ms')
    if execute and not port:
        raise ValueError('--execute requires a port')
    if port and not execute:
        raise ValueError('Offline preview does not accept a port; explicit --execute required')
    calibration_path, output = Path(calibration_path), Path(output)
    calibration = load_calibration(calibration_path, require_valid=False)
    output.mkdir(parents=True, exist_ok=False)  # checked before opening USB
    manifest = {'version': 1, 'mode': 'hardware_bench' if execute else 'offline_preview',
                'status': 'started', 'session': 'single_servo' if channel is not None else 'read_only_imu',
                'duration_s': seconds, 'channel': channel, 'requested_pulse_us': pulse_us,
                'command_hz': 1/CONTROL_DT if channel is not None else 0,
                'identity': configuration_identity(calibration), 'calibration_record': calibration,
                'calibration_file_sha256': hashlib.sha256(calibration_path.read_bytes()).hexdigest(),
                'source_sha256': {n: hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in (
                    'bench.py','serial_robot.py','hardware_interface.py','calibration.py','robot_config.py')},
                'hardware_access_attempted': False, 'physically_verified': False,
                'commands_sent': 0, 'telemetry_samples': 0, 'bench_status_confirmed': False,
                'limits': ['Preview is not physical verification or permission to power a servo.',
                           'Use one unloaded servo with horn removed; pulse bounds do not guarantee mechanical safety.',
                           'Bench identity/status confirms mode only, not applied pulse, sequence or shaft angle.',
                           'Telemetry command angles/sequence describe the six-joint command state, not bench-pulse feedback.',
                           'No tilt estimate is assumed before IMU alignment calibration; this is not an assembled-robot controller.',
                           'STOP requests PWM disable; it is not physical motor-power isolation.']}
    robot = None
    failure = None
    clock = clock or time.monotonic
    try:
        with (output/'preview.csv').open('x', newline='') as f:
            writer = csv.writer(f);writer.writerow(['time_s','operation','channel','requested_pulse_us'])
            if channel is None:
                writer.writerow([0.,'read_only_no_motor_command','',''])
            else:
                writer.writerows((i*CONTROL_DT,'constant_bench_pulse',channel,pulse_us) for i in range(ticks))
        if not execute:
            manifest['status'] = 'preview_complete'
            return manifest

        with (output/'telemetry.csv').open('x', newline='') as tf, (output/'events.jsonl').open('x') as ef:
            writer = csv.writer(tf)
            writer.writerow(['host_elapsed_s','mcu_ms','command_ack_sequence','status',
                             *[n+'_command_ack_rad' for n in JOINT_NAMES],
                             'raw_ax','raw_ay','raw_az','raw_gx','raw_gy','raw_gz'])
            epoch = clock()

            def event(kind, **values):
                ef.write(json.dumps({'host_elapsed_s': clock()-epoch, 'event': kind, **values})+'\n')
                ef.flush()

            idle = 0 if calibration['state']=='measured' and calibration['validated'] else 8
            last_ms = None
            last_telemetry = clock()
            active = False

            def inspect(kind, value):
                nonlocal last_ms, last_telemetry, active
                now = clock()
                status = value.status if kind=='telemetry' else value
                if kind not in ('identity','telemetry'):
                    raise RuntimeError('Unknown incoming bench frame')
                if kind=='identity': event('identity_status', status=status)
                else:
                    writer.writerow([now-epoch,value.timestamp_ms,value.sequence,status,
                                     *value.applied_targets,*value.accelerometer,*value.gyroscope])
                    tf.flush();manifest['telemetry_samples'] += 1
                permitted = {idle | 32} if active else ({idle, idle | 32} if channel is not None and manifest['commands_sent'] else {idle})
                if status not in permitted:
                    raise RuntimeError('Firmware fault/unexpected bench status '+str(status))
                if status == idle | 32:
                    active = True;manifest['bench_status_confirmed'] = True
                if kind != 'telemetry': return
                if now-last_telemetry > .050:
                    raise TimeoutError('Fresh telemetry deadline exceeded50ms')
                accel, gyro = np.asarray(value.accelerometer), np.asarray(value.gyroscope)
                if accel.shape != (3,) or gyro.shape != (3,) or not np.isfinite([accel,gyro]).all():
                    raise RuntimeError('Invalid IMU sample')
                if np.any(abs(accel) >= IMU_ACCEL_RANGE*.99) or np.any(abs(gyro) >= IMU_GYRO_RANGE*.99):
                    raise RuntimeError('IMU saturation')
                if last_ms is not None and not 0 < ((value.timestamp_ms-last_ms)&0xffffffff) < 100:
                    raise RuntimeError('Stale/reordered/gapped telemetry timestamp')
                last_ms = value.timestamp_ms;last_telemetry = now

            manifest['hardware_access_attempted'] = True
            robot = (robot_factory or SerialRobot)(port, calibration)
            robot.handshake()  # match both identities; handshake never arms
            event('handshake_complete')
            last_telemetry = clock();deadline = clock()+.100;initial_samples = 0
            while initial_samples < 2:
                kind, value = robot.read()
                if clock() > deadline: raise TimeoutError('Startup telemetry exceeded100ms')
                inspect(kind, value)
                if kind=='telemetry':
                    if not .8*9.81 < np.linalg.norm(value.accelerometer) < 1.2*9.81 or np.linalg.norm(value.gyroscope) > 1:
                        raise RuntimeError('Need stationary initial IMU samples')
                    initial_samples += 1
            started = clock();next_command = started;first_command = None
            while clock()-started < seconds:
                now = clock()
                if now-last_telemetry > .050: raise TimeoutError('No fresh telemetry within50ms')
                if channel is not None and now >= next_command:
                    if now-next_command > .040: raise TimeoutError('Bench command deadline exceeded40ms')
                    robot.bench(channel, pulse_us)
                    sent = clock()
                    if first_command is None: first_command = sent
                    manifest['commands_sent'] += 1
                    event('bench_request', channel=channel, pulse_us=pulse_us,
                          acknowledgement='mode_status_only_not_pulse_feedback')
                    next_command = sent+CONTROL_DT  # never burst to catch up
                kind, value = robot.read()
                inspect(kind, value)
                if first_command is not None and not active and clock()-first_command > .080:
                    raise TimeoutError('Bench mode not confirmed within80ms')
            if channel is not None and not active:
                raise RuntimeError('Bench mode never confirmed')
            event('session_complete')
        manifest['status'] = 'completed'
        return manifest
    except BaseException as error:
        failure = error
        manifest['status'] = 'interrupted' if isinstance(error,KeyboardInterrupt) else 'failed'
        manifest['error'] = type(error).__name__+': '+str(error)
        raise
    finally:
        close_error = None
        if robot is not None:
            try:
                robot.close()  # STOP and close; SerialRobot closes even if STOP write fails
                manifest['stop_and_close'] = 'requested_not_physical_isolation'
            except BaseException as error:
                close_error = error;manifest['stop_and_close'] = 'failed: '+str(error)
                if failure is None:
                    manifest['status'] = 'failed';manifest['error'] = type(error).__name__+': '+str(error)
        (output/'manifest.json').write_text(json.dumps(manifest,indent=2,allow_nan=False)+'\n')
        if close_error is not None and failure is None: raise close_error


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port')
    p.add_argument('--execute', action='store_true', help='Explicitly open USB after physical bench checks')
    p.add_argument('--calibration', type=Path, default=ROOT/'calibrations/example.invalid.json')
    p.add_argument('--seconds', type=float)
    p.add_argument('--channel', type=int, choices=range(6))
    p.add_argument('--pulse-us', type=int)
    p.add_argument('--output', type=Path, required=True, help='New session directory, not a CSV filename')
    a = p.parse_args()
    result = run_bench(a.output, calibration_path=a.calibration, seconds=a.seconds,
                       channel=a.channel, pulse_us=a.pulse_us, execute=a.execute, port=a.port)
    print(json.dumps({k: result[k] for k in ('mode','status','session','physically_verified')}))


if __name__ == '__main__':
    main()
