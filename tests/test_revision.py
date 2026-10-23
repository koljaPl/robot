import json
import shutil
import subprocess
import sys
import numpy as np
import pytest
from robot_config import ROOT,HOME,JOINT_LOW,JOINT_HIGH,CONTROL_DT,target_to_action
from gait_metrics import GaitMetrics,progress_reward
from calibration import load_calibration,configuration_identity,digest
from humanoid_env import HumanoidEnv


def test_progress_closed_cycle():
    assert progress_reward(-.2,.02)==pytest.approx(-2)
    assert sum(progress_reward(dx,.02) for dx in [.1,-.1])<=0
    assert sum(progress_reward(dx,.02) for dx in [.0001,-.0001])==pytest.approx(0)


def sequence(mode):
    g=GaitMetrics();feet=np.array([[0.,.034,0],[0.,-.034,0]])
    g.update(feet,[0,0],[True,True],[True,True],.002)
    for side in [0,1,0,1]:
        contact=[True,True];contact[side]=False
        for i in range(30):
            height=.002 if mode=='toe' else .004
            if mode=='slide':feet[1-side,0]+=.0002
            if mode not in ('inplace','slideafter'):feet[side,0]+=.001
            g.update(feet,[height,height],contact if mode!='hop' else [False,False],[True,True] if mode!='hop' else [False,False],.002)
        g.update(feet,[0,0],[True,True],[True,True],.002)
        if mode=='slideafter':
            feet[:,0]+=.05;g.update(feet,[0,0],[True,True],[True,True],.002)
    return g


@pytest.mark.parametrize('mode',['toe','hop','inplace','slide','slideafter'])
def test_false_gaits_rejected(mode):
    g=sequence(mode);assert g.distance==0 and g.steps.sum()==0


def test_valid_alternating_progress():
    g=sequence('walk');assert g.steps.tolist()==[2,2] and g.alternations==3
    assert g.distance==pytest.approx(.06)


def test_calibration_gate_and_alignment(tmp_path):
    with pytest.raises(ValueError,match='measured'):load_calibration(ROOT/'calibrations/example.invalid.json')
    c=load_calibration(ROOT/'calibrations/example.invalid.json',require_valid=False)
    c['imu']['rotation_sensor_to_body'][0][0]=-1
    p=tmp_path/'c.json';p.write_text(json.dumps(c))
    with pytest.raises(ValueError,match='proper rotation'):load_calibration(p,require_valid=False)


def test_delay_is_two_discrete_ticks_and_no_stops():
    e=HumanoidEnv(domain_randomization=True)
    try:
        delays=[]
        for seed in range(20):
            e.reset(seed=seed);delays.append(e.servos.delay)
        assert set(delays)=={.02,.04}
        assert not e.model.jnt_limited[1:].any()
    finally:e.close()


def test_observation_provenance():
    e=HumanoidEnv()
    try:
        e.reset(seed=2)
        # Observation builder has ONLY deployable fields. Mutating privileged state
        # without simulating an IMU sample cannot change its assembled policy frame.
        def frame():return e.history.frame(e.estimator.gravity,e.last_gyro,e.applied_command,e.last_action)
        before=frame();e.data.qpos[:3]+=[.5,.3,.2];e.data.qvel[:]=12
        np.testing.assert_array_equal(before,frame())
    finally:e.close()


def test_native_firmware_state_machine(tmp_path):
    if not shutil.which('g++'):pytest.skip('native C++ compiler absent')
    source=tmp_path/'test.cpp'
    source.write_text(r'''
#include "control.h"
#include <cassert>
#include <cstdio>
#include <string>
bool packet(Control& c,std::string p,unsigned now){char line[192];snprintf(line,sizeof(line),"%s*%04X",p.c_str(),crc16(p.c_str()));return c.packet(line,now);}
int main(){
 Control c;assert(!c.armed&&!c.bench);assert(!packet(c,"A,1",0));
 assert(packet(c,std::string("H,1,")+CONFIG_HASH+","+CAL_HASH+",0",0));
 assert(packet(c,"B,1,1,20,2,1500",0));assert(c.bench&&!c.armed);c.watchdog(99);assert(c.bench);c.watchdog(100);assert(c.fault&&!c.bench);
 packet(c,"S,1",101);packet(c,std::string("H,1,")+CONFIG_HASH+","+CAL_HASH+",0",102);
 assert(!packet(c,"B,1,2,40,6,1500",103));assert(c.fault);
 packet(c,"S,1",104);packet(c,std::string("H,1,")+CONFIG_HASH+","+CAL_HASH+",0",105);
 packet(c,"B,1,2,40,0,1500",106);assert(!packet(c,"B,1,2,40,0,1500",107)); // replay
 packet(c,"S,1",108);assert(!packet(c,"H,1,wrong,wrong",109));
 assert(!packet(c,"B,1,3,60,0,2500",110));
}
''')
    subprocess.run(['g++','-std=c++17','-I',str(ROOT/'firmware'),str(source),'-o',str(tmp_path/'test')],check=True)
    subprocess.run([str(tmp_path/'test')],check=True)


def test_measured_quantization_inward():
    from servo_control import ServoTargets
    c=load_calibration(ROOT/'calibrations/example.invalid.json',require_valid=False)
    c['us_per_rad']=[510,520,480,499,501,503]
    s=ServoTargets(calibration=c)
    for target in (JOINT_LOW,JOINT_HIGH,HOME):
        q=s.quantize(target)
        assert np.all(q>=JOINT_LOW) and np.all(q<=JOINT_HIGH)
        pulses=np.array(c['zero_us'])+np.array(c['sign'])*c['us_per_rad']*q
        np.testing.assert_allclose(pulses,np.rint(pulses),atol=1e-9)


def test_usb_transport_handshake_corrupt_and_stale():
    from hardware_interface import encode_frame
    from serial_robot import SerialRobot
    c=load_calibration(ROOT/'calibrations/example.invalid.json',require_valid=False)
    identity=configuration_identity(c)
    class Fake:
        def __init__(self,*a,**k):self.incoming=bytearray();self.sent=[]
        def reset_input_buffer(self):pass
        def write(self,b):self.sent.append(b);return len(b)
        def read(self,n):
            b=bytes(self.incoming[:n]);del self.incoming[:n];return b
        def close(self):pass
    r=SerialRobot('fake',c,serial_factory=Fake)
    r.connection.incoming.extend(encode_frame(['I',1,identity['configuration'],identity['calibration'],8]))
    assert r.handshake()==8
    assert all(not p.startswith(b'A,') for p in r.connection.sent)
    fields=['T',1,0,10,8,*[round(x*1000) for x in HOME],0,0,9807,0,0,0]
    packet=encode_frame(fields)
    r.connection.incoming.extend(packet);assert r.read()[0]=='telemetry'
    r.connection.incoming.extend(packet)
    with pytest.raises(ValueError,match='Stale'):r.read()
    r.connection.incoming.extend(b'T,1,broken*0000\n')
    with pytest.raises(ValueError):r.read()


def test_armed_controller_queue_slew_bounds_and_watchdog(tmp_path):
    if not shutil.which('g++'):pytest.skip('native C++ compiler absent')
    # Synthetic VALID calibration is confined to the test directory, never flashed.
    (tmp_path/'control.h').write_text((ROOT/'firmware/control.h').read_text())
    (tmp_path/'generated_config.h').write_text((ROOT/'firmware/generated_config.h').read_text().replace('CAL_VALID=false','CAL_VALID=true'))
    source=tmp_path/'test.cpp'
    source.write_text(r'''
#include "control.h"
#include <cassert>
#include <cstdio>
#include <string>
bool packet(Control& c,std::string p,unsigned now){char line[192];snprintf(line,sizeof(line),"%s*%04X",p.c_str(),crc16(p.c_str()));return c.packet(line,now);}
void hello(Control& c){assert(packet(c,std::string("H,1,")+CONFIG_HASH+","+CAL_HASH+",0",0));}
int main(){
 Control c;hello(c);c.imu=true;assert(packet(c,"A,1",0));assert(c.armed);
 assert(packet(c,"C,1,1,1,600,1000,340,600,1000,340",1));
 c.tick(20);assert(c.ack_seq==0);float old=c.applied[0];c.tick(21);assert(c.ack_seq==1);
 assert(c.applied[0]>old && c.applied[0]-old<=MAX_SPEED*.02f+.00001f);
 for(int i=0;i<6;++i){float q=(c.pulse(i)-ZERO[i])/(SIGN[i]*GAIN[i]);assert(q>=QMIN[i] && q<=QMAX[i]);}
 c.watchdog(100);assert(c.armed);c.watchdog(101);assert(c.fault&&!c.armed);
 packet(c,"S,1",0);hello(c);c.imu=true;packet(c,"A,1",0);
 assert(!packet(c,"C,1,1,0,0,0,0,0,0,0",81)); // stale first command relative handshake
 packet(c,"S,1",0);hello(c);c.imu=true;packet(c,"A,1",0);
 assert(!packet(c,"C,1,1,1,999999,0,0,0,0,0",1));
 char bad[]="S,1*0000";assert(!c.packet(bad,1));assert(c.fault);
}
''')
    subprocess.run(['g++','-std=c++17','-I',str(tmp_path),str(source),'-o',str(tmp_path/'test')],check=True)
    subprocess.run([str(tmp_path/'test')],check=True)


def test_a_b_initial_weights_match():
    from stable_baselines3 import PPO
    from train import ALGORITHM,weight_hash
    hashes=[]
    for randomized in (False,True):
        e=HumanoidEnv(domain_randomization=randomized)
        try:hashes.append(weight_hash(PPO('MlpPolicy',e,**ALGORITHM,seed=1,device='cpu').policy))
        finally:e.close()
    assert hashes[0]==hashes[1]


def test_response_fit_diagnostic_synthetic():
    from tools.fit_response import fit
    t=np.linspace(0,1,201);u=np.where(t<.1,0,.2)
    q=.2*(1-np.exp(-np.maximum(0,t-.1-.03)/.1))
    a=np.array(list(zip(t,u,q)),dtype=[('time_s',float),('target_rad',float),('angle_rad',float)])
    result=fit(a)
    assert result['delay_s']==pytest.approx(.03,abs=.004)
    assert result['time_constant_s']==pytest.approx(.1,abs=.005)


def test_controller_timestamp_wrap(tmp_path):
    if not shutil.which('g++'):pytest.skip('native C++ compiler absent')
    source=tmp_path/'wrap.cpp'
    source.write_text(r'''
#include "control.h"
#include <cassert>
#include <cstdio>
#include <string>
bool packet(Control& c,std::string p,unsigned now){char line[192];snprintf(line,sizeof(line),"%s*%04X",p.c_str(),crc16(p.c_str()));return c.packet(line,now);}
int main(){
 int64_t value=0;assert(integer("4294967295",value));assert(value==4294967295LL);
 Control c;assert(packet(c,std::string("H,1,")+CONFIG_HASH+","+CAL_HASH+",4294967290",0));
 assert(packet(c,"B,1,65535,3,0,1500",9));
 assert(packet(c,"B,1,0,8,0,1500",14)); // BOTH timestamp and sequence wrap correctly
 assert(!packet(c,"B,1,1,8,0,1500",15)); // duplicate timestamp
}
''')
    subprocess.run(['g++','-std=c++17','-I',str(ROOT/'firmware'),str(source),'-o',str(tmp_path/'wrap')],check=True)
    subprocess.run([str(tmp_path/'wrap')],check=True)
