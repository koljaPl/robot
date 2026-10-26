import copy
import json
from pathlib import Path

import numpy as np
import pytest

import manual_control as manual
from hardware_interface import Telemetry
from robot_config import HOME, ROOT


def inputs(tmp_path, valid=False):
    c = json.loads((ROOT/'calibrations/example.invalid.json').read_text())
    if valid:
        c.update(state='measured', validated=True, evidence='SYNTHETIC TEST FIXTURE ONLY; not physical calibration')
    calibration = tmp_path/'calibration.json'; calibration.write_text(json.dumps(c))
    movement = json.loads((ROOT/'docs/templates/manual_home_only.json').read_text())
    sequence = tmp_path/'sequence.json'; sequence.write_text(json.dumps(movement))
    return calibration, sequence, c, movement


class Clock:
    def __init__(self): self.now = 0.
    def __call__(self): return self.now


class FakeRobot:
    """Transport-only fake, never a measured hardware result."""
    def __init__(self, clock, mode=None):
        self.clock, self.mode = clock, mode
        self.armed = False; self.closed = False; self.stopped = False
        self.last_sequence = None; self.commands = []; self.reads = 0

    def handshake(self):
        if self.mode == 'mismatch': raise ValueError('Hardware/control/calibration fingerprint mismatch')

    def arm(self): self.armed = True

    def command(self, q):
        self.last_sequence = 0 if self.last_sequence is None else self.last_sequence+1
        self.commands.append((self.clock(), q.copy()))

    def read(self):
        self.reads += 1
        self.clock.now += .005
        if self.armed and self.mode == 'jitter': self.clock.now += .025
        if self.armed and self.mode == 'interrupt': raise KeyboardInterrupt()
        if self.armed and self.mode == 'timeout': raise TimeoutError('No complete frame within50ms')
        if self.armed and self.mode == 'late': self.clock.now += .060
        status = 1 if self.armed else 0
        seq = self.last_sequence if self.last_sequence is not None else 0
        if self.mode == 'stale_ack' and self.armed: seq = 0
        if self.mode == 'no_final_ack' and self.armed: seq = max(0, seq-1)
        if self.mode == 'fault' and self.armed: status = 2
        accel = np.array([0., 0., 9.807]); gyro = np.zeros(3)
        if self.mode == 'tilt': accel = np.array([9.807, 0., 0.])
        if self.mode == 'saturated' and self.armed: accel[0] = 100.
        timestamp = round(self.clock.now*1000)
        if self.mode == 'stale_timestamp' and self.armed: timestamp = 5
        ack = HOME.copy()
        if self.mode == 'different_start': ack[0] += .02
        return 'telemetry', Telemetry(seq, timestamp, status, ack, accel, gyro)

    def close(self): self.stopped = self.closed = True


def test_default_preview_never_opens_usb_or_validates_hardware(tmp_path):
    c, s, _, _ = inputs(tmp_path)
    def forbidden(*args): raise AssertionError('Preview opened USB')
    r = manual.run_sequence(s, c, tmp_path/'preview', robot_factory=forbidden)
    assert r['mode'] == 'offline_preview' and r['status'] == 'preview_complete'
    assert not r['physically_verified'] and not r['calibration_record']['validated']
    trajectory = np.loadtxt(tmp_path/'preview/trajectory.csv', delimiter=',', skiprows=1)
    np.testing.assert_allclose(np.diff(trajectory[:, 0]), .02)
    np.testing.assert_allclose(trajectory[:, 1:], np.tile(HOME, (len(trajectory), 1)))


@pytest.mark.parametrize('mutation,message', [
    ('order', 'joint order'), ('nan', 'finite'), ('bounds', 'safe angles'),
    ('slew', 'slew'), ('duration', 'multiples'), ('large_duration', '20ms..30s')])
def test_all_movement_validation_happens_before_connection(tmp_path, mutation, message):
    c, s, _, m = inputs(tmp_path, valid=True)
    if mutation == 'order': m['joint_order'].reverse()
    if mutation == 'nan': m['segments'][0]['targets_rad'][0] = float('nan')
    if mutation == 'bounds': m['segments'][0]['targets_rad'][0] = 20
    if mutation == 'slew': m['segments'][0].update(duration_s=.02, targets_rad=[.5, *HOME[1:]])
    if mutation == 'duration': m['segments'][0]['duration_s'] = .021
    if mutation == 'large_duration': m['segments'][0]['duration_s'] = 1e308
    s.write_text(json.dumps(m))
    def forbidden(*args): raise AssertionError('Invalid input opened USB')
    with pytest.raises(ValueError, match=message):
        manual.run_sequence(s, c, tmp_path/'invalid', arm=True, port='fake', robot_factory=forbidden)
    assert not (tmp_path/'invalid').exists()


def test_hardware_refuses_example_calibration_and_implicit_arm(tmp_path):
    c, s, _, _ = inputs(tmp_path)
    with pytest.raises(ValueError, match='measured, validated'):
        manual.run_sequence(s, c, tmp_path/'invalid', arm=True, port='fake')
    with pytest.raises(ValueError, match='explicit --arm'):
        manual.run_sequence(s, c, tmp_path/'port_without_arm', port='fake')


def test_mocked_execution_starts_from_ack_and_sends_bounded_smooth_commands(tmp_path):
    c, s, cal, m = inputs(tmp_path, valid=True)
    q = HOME.copy(); q[0] += .05
    m['segments'][0]['targets_rad'] = q.tolist(); s.write_text(json.dumps(m))
    clock = Clock(); robot = FakeRobot(clock)
    r = manual.run_sequence(s, c, tmp_path/'run', arm=True, port='fake',
                            robot_factory=lambda *a: robot, clock=clock)
    assert r['status'] == 'completed' and robot.closed and robot.stopped
    assert not r['acknowledged_start_is_shaft_feedback']
    np.testing.assert_array_equal(robot.commands[0][1], HOME)
    np.testing.assert_allclose(robot.commands[-1][1], q)
    targets = np.array([q for _, q in robot.commands])
    assert np.all(abs(np.diff(targets, axis=0))/.02 <= cal['max_target_speed_rad_s'])
    assert (tmp_path/'run/commands.csv').exists() and (tmp_path/'run/telemetry.csv').exists()


@pytest.mark.parametrize('mode,exception', [('mismatch', ValueError), ('different_start', ValueError),
    ('fault', RuntimeError), ('stale_ack', RuntimeError), ('stale_timestamp', RuntimeError),
    ('timeout', TimeoutError), ('late', TimeoutError), ('tilt', RuntimeError),
    ('saturated', RuntimeError), ('interrupt', KeyboardInterrupt), ('no_final_ack', TimeoutError)])
def test_failure_paths_stop_close_and_preserve_failure_record(tmp_path, mode, exception):
    c, s, _, _ = inputs(tmp_path, valid=True)
    clock = Clock(); robot = FakeRobot(clock, mode)
    with pytest.raises(exception):
        manual.run_sequence(s, c, tmp_path/'run', arm=True, port='fake',
                            robot_factory=lambda *a: robot, clock=clock)
    assert robot.closed and robot.stopped
    r = json.loads((tmp_path/'run/manifest.json').read_text())
    assert r['status'] == ('interrupted' if mode == 'interrupt' else 'failed')
    assert r['error'] and not r['physically_verified']
    if mode in ('mismatch', 'different_start', 'tilt'): assert not robot.armed


def test_output_cannot_be_overwritten_or_connect_before_collision_check(tmp_path):
    c, s, _, _ = inputs(tmp_path, valid=True)
    out = tmp_path/'existing'; out.mkdir(); (out/'marker').write_text('keep')
    def forbidden(*args): raise AssertionError('Existing output opened USB')
    with pytest.raises(FileExistsError):
        manual.run_sequence(s, c, out, arm=True, port='fake', robot_factory=forbidden)
    assert (out/'marker').read_text() == 'keep'


def test_scheduler_jitter_does_not_produce_catchup_bursts_or_rate_violation(tmp_path):
    c, s, cal, m = inputs(tmp_path, valid=True)
    target = HOME.copy(); target[0] += .1
    m['segments'][0]['targets_rad'] = target.tolist(); s.write_text(json.dumps(m))
    clock = Clock(); robot = FakeRobot(clock, 'jitter')
    manual.run_sequence(s, c, tmp_path/'jitter', arm=True, port='fake',
                        robot_factory=lambda *a: robot, clock=clock)
    times = np.array([t for t, _ in robot.commands]); targets = np.array([q for _, q in robot.commands])
    intervals = np.diff(times)
    assert intervals.min() >= .02-1e-9
    assert np.max(abs(np.diff(targets, axis=0))/intervals[:, None]) <= cal['max_target_speed_rad_s']


def test_serial_constructor_closes_connection_if_initialization_fails(tmp_path):
    from serial_robot import SerialRobot
    _, _, cal, _ = inputs(tmp_path)
    class Broken:
        closed = False
        def reset_input_buffer(self): raise IOError('initial reset failed')
        def close(self): self.closed = True
    connection = Broken()
    with pytest.raises(IOError, match='initial reset'):
        SerialRobot('fake', cal, serial_factory=lambda *a, **k: connection)
    assert connection.closed
