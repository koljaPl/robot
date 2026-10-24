"""Three bounded scripted transfer/lift diagnostics; no optimizer or training.

Keeps the existing estimated0.08Nm motor envelope. Geometry/contact truth is
logged only for diagnosis, never added to policy observations. No successful gait
is inferred from a single lifted foot or a completed script.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from humanoid_env import HumanoidEnv
from robot_config import HOME,CONTROL_DT,target_to_action
from calibration import configuration_identity


def command(t,swing_roll):
    lean=np.deg2rad([-10,10,15,-10,10,15])
    lift=lean.copy();lift[[3,4,5]]=np.deg2rad([-35,35,swing_roll])
    lean2=np.deg2rad([-10,10,-15,-10,10,-15])
    lift2=lean2.copy();lift2[[0,1,2]]=np.deg2rad([-35,35,-swing_roll])
    keys=[(0,HOME),(2,HOME),(4,lean),(6,lift),(8,lift),(10,HOME),
          (12,lean2),(14,lift2),(16,lift2),(18,HOME)]
    for (t0,a),(t1,b) in zip(keys,keys[1:]):
        if t<=t1:
            f=np.clip((t-t0)/(t1-t0),0,1);return a+(b-a)*(f*f*(3-2*f))
    return HOME


def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False);reports=[]
    for swing_roll in (15,5,0):
        env=HumanoidEnv(episode_seconds=18);rows=[];max_clear=np.zeros(2)
        try:
            _,info=env.reset(seed=42);done=False
            while not done:
                _,_,term,trunc,info=env.step(target_to_action(command(env.steps*CONTROL_DT,swing_roll)));done=term or trunc
                heights=[env._minimum_foot_height(i) for i in range(2)];max_clear=np.maximum(max_clear,heights)
                rotation=env.data.xmat[env.torso_id].reshape(3,3)
                row={'time_s':info['duration_s'],'roll_rad':float(np.arctan2(rotation[2,1],rotation[2,2])),
                     'left_min_height_m':heights[0],'right_min_height_m':heights[1],
                     'gait_distance_m':info['gait_distance_m'],'fallen':info['fallen']}
                for j in range(6):
                    row[f'actual_joint{j}_rad']=float(env.data.qpos[env.qadr[j]])
                    row[f'applied_joint{j}_rad']=float(env.applied_command[j])
                    row[f'actuator_joint{j}_Nm']=float(env.data.actuator_force[env.aids[j]])
                rows.append(row)
            with (output/f'swing_roll{swing_roll}.csv').open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
            reports.append({'swing_ankle_roll_deg':swing_roll,'max_whole_foot_clearance_m':max_clear.tolist(),
                            'max_abs_roll_rad':max(abs(r['roll_rad']) for r in rows),
                            'final_metrics':{k:v for k,v in info.items() if k!='reward_terms'}})
        finally:env.close()
    report={'state':'provisional scripted diagnosis, not physical or learned walking','identity':configuration_identity(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'unchanged_motor_envelope_Nm':.08,'seed':42,'variants':reports,
            'interpretation':'These test commanded stance/swing ankle differences. Only existing non-sliding alternating gait metrics can credit steps; a single lift is not walking.'}
    (output/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
