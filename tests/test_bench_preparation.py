"""Bench preparation through mocked transport only; never physical evidence."""
import csv
import json

import numpy as np
import pytest

import bench
from hardware_interface import Telemetry
from robot_config import HOME, ROOT


class Clock:
    def __init__(self): self.now=0.
    def __call__(self): return self.now


class Robot:
    def __init__(self, clock, mode=None):
        self.clock,self.mode=clock,mode
        self.requests=[];self.closed=False;self.stopped=False;self.reads=0

    def handshake(self):
        if self.mode=='mismatch': raise ValueError('Hardware/control/calibration fingerprint mismatch')

    def arm(self): raise AssertionError('Bench must never policy-arm')
    def command(self, targets): raise AssertionError('Bench must never issue six-joint commands')

    def bench(self, channel, pulse):
        self.requests.append((self.clock(),channel,pulse))

    def read(self):
        self.clock.now+=.005;self.reads+=1
        if self.requests:
            if self.mode=='interrupt':raise KeyboardInterrupt()
            if self.mode=='timeout':raise TimeoutError('Synthetic read timeout')
            if self.mode=='late':self.clock.now+=.045
            if self.mode=='jitter':self.clock.now+=.025
        if self.mode=='identities_only':return 'identity',8
        status=40 if self.requests and self.mode!='no_confirmation' else 8
        if self.mode=='fault' and self.requests:status|=2
        if self.mode=='unexpected_arm':status=9
        if self.mode=='imu_fault':status=12
        if self.mode=='unmatched':status=24
        if self.mode=='disarm' and len(self.requests)>2:status=8
        timestamp=round(self.clock()*1000)
        if self.mode=='stale' and self.requests:timestamp=10
        if self.mode=='wrap':timestamp=(0xfffffff0+timestamp)&0xffffffff
        accel=np.array([0.,0.,9.807]);gyro=np.zeros(3)
        if self.mode=='saturated' and self.requests:accel[0]=20.
        if self.mode=='nonfinite' and self.requests:gyro[0]=np.nan
        if self.mode=='moving_start':gyro[0]=2.
        return 'telemetry',Telemetry(0,timestamp,status,HOME.copy(),accel,gyro)

    def close(self):
        self.stopped=True;self.closed=True
        if self.mode=='close_error':raise OSError('Synthetic STOP write failure')


def test_read_only_preview_never_opens_usb(tmp_path):
    def forbidden(*args):raise AssertionError('USB opened in preview')
    out=tmp_path/'preview'
    m=bench.run_bench(out,robot_factory=forbidden)
    assert m['status']=='preview_complete' and m['session']=='read_only_imu'
    assert not m['hardware_access_attempted'] and not m['physically_verified']
    assert m['commands_sent']==0 and not (out/'telemetry.csv').exists()
    assert list(csv.DictReader((out/'preview.csv').open()))[0]['operation']=='read_only_no_motor_command'


@pytest.mark.parametrize('pulse',[1400,1500,1600])
def test_constant_pulse_preview_is_bounded_and_not_angle_feedback(tmp_path,pulse):
    out=tmp_path/'preview'
    m=bench.run_bench(out,channel=0,pulse_us=pulse,seconds=.1)
    rows=list(csv.DictReader((out/'preview.csv').open()))
    assert len(rows)==5
    np.testing.assert_allclose(np.diff([float(r['time_s']) for r in rows]),.02)
    assert all(int(r['requested_pulse_us'])==pulse for r in rows)
    assert m['command_hz']==50 and not m['bench_status_confirmed']
    assert any('not bench-pulse feedback' in note for note in m['limits'])


@pytest.mark.parametrize('settings',[
    {'seconds':float('nan')},{'seconds':float('inf')},{'seconds':True},
    {'seconds':0},{'seconds':.021},{'seconds':61},
    {'channel':0,'seconds':6},{'channel':True},{'channel':6},
    {'channel':0,'pulse_us':1399},{'channel':0,'pulse_us':1601},
    {'channel':0,'pulse_us':1500.5},{'channel':0,'pulse_us':True},
    {'pulse_us':1500},{'port':'fake'},{'execute':True}])
def test_invalid_arguments_rejected_before_usb_or_output(tmp_path,settings):
    def forbidden(*args):raise AssertionError('USB opened before validation')
    out=tmp_path/'new'
    with pytest.raises(ValueError):bench.run_bench(out,robot_factory=forbidden,**settings)
    assert not out.exists()


def test_existing_output_and_invalid_calibration_rejected_before_usb(tmp_path):
    def forbidden(*args):raise AssertionError('USB opened before validation')
    out=tmp_path/'old';out.mkdir();(out/'manifest.json').write_text('preserve')
    with pytest.raises(FileExistsError):bench.run_bench(out,execute=True,port='fake',robot_factory=forbidden)
    assert (out/'manifest.json').read_text()=='preserve'
    calibration=tmp_path/'bad.json';c=json.loads((ROOT/'calibrations/example.invalid.json').read_text())
    c['us_per_rad'][0]=0;calibration.write_text(json.dumps(c))
    with pytest.raises(ValueError):bench.run_bench(tmp_path/'new',calibration_path=calibration,execute=True,port='fake',robot_factory=forbidden)
    assert not (tmp_path/'new').exists()


def test_read_only_hardware_mock_has_no_motor_commands(tmp_path):
    clock=Clock();robot=Robot(clock)
    m=bench.run_bench(tmp_path/'read',seconds=.1,execute=True,port='fake',clock=clock,robot_factory=lambda *args:robot)
    assert m['status']=='completed' and m['commands_sent']==0
    assert m['telemetry_samples']>=20 and robot.closed and robot.stopped and not robot.requests


@pytest.mark.parametrize('mode',[None,'wrap','jitter'])
def test_single_servo_mock_status_only_confirmation_and_no_catchup(tmp_path,mode):
    clock=Clock();robot=Robot(clock,mode)
    m=bench.run_bench(tmp_path/'bench',channel=2,pulse_us=1500,seconds=.2,
                      execute=True,port='fake',clock=clock,robot_factory=lambda *args:robot)
    assert m['status']=='completed' and m['bench_status_confirmed'] and not m['physically_verified']
    assert robot.closed and robot.stopped
    assert all(channel==2 and pulse==1500 for _,channel,pulse in robot.requests)
    assert np.all(np.diff([t for t,_,_ in robot.requests])>=.02-1e-10)
    assert not m.get('pulse_acknowledged',False)


@pytest.mark.parametrize('mode',['mismatch','fault','imu_fault','unmatched','unexpected_arm','stale',
                                  'timeout','late','saturated','nonfinite','moving_start','no_confirmation',
                                  'identities_only','disarm','interrupt','close_error'])
def test_mock_failures_stop_close_and_preserve_logs(tmp_path,mode):
    clock=Clock();robot=Robot(clock,mode);out=tmp_path/'failed'
    with pytest.raises((ValueError,RuntimeError,TimeoutError,KeyboardInterrupt,OSError)):
        bench.run_bench(out,channel=0,seconds=.2,execute=True,port='fake',clock=clock,robot_factory=lambda *args:robot)
    m=json.loads((out/'manifest.json').read_text())
    assert m['status']==('interrupted' if mode=='interrupt' else 'failed')
    assert not m['physically_verified'] and 'error' in m
    assert robot.closed and robot.stopped and (out/'events.jsonl').exists()
    if mode in {'imu_fault','unmatched','unexpected_arm','moving_start','mismatch','identities_only'}:
        assert not robot.requests
