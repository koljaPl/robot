"""Conservative scripted stand/lean/lift diagnostic; no kinematic teleporting or policy.

Failure does not authorize stronger motors/torques or a larger PPO run. Save evidence.
"""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from humanoid_env import HumanoidEnv
from robot_config import HOME,CONTROL_DT,target_to_action
from calibration import configuration_identity


def reference(t, lean_sign=1):
    # Keep hip+knee pitch near zero during swing: no ankle pitch exists.
    # 30s standing, then slow lateral shift/lift/land in each direction.
    poses=[(0,HOME),(30,HOME),
           (32,np.deg2rad([-10,10,15,-10,10,15])),
           (34,np.deg2rad([-10,10,15,-30,30,15])),
           (36,np.deg2rad([-10,10,15,-10,10,15])),(38,HOME),
           (40,np.deg2rad([-10,10,-15,-10,10,-15])),
           (42,np.deg2rad([-30,30,-15,-10,10,-15])),
           (44,np.deg2rad([-10,10,-15,-10,10,-15])),(46,HOME)]
    for _, q in poses:
        if q is not HOME:
            q[[2,5]] *= lean_sign
    for (t0,q0),(t1,q1) in zip(poses,poses[1:]):
        if t<=t1:
            a=np.clip((t-t0)/(t1-t0),0,1);return q0+(q1-q0)*(a*a*(3-2*a))
    return HOME


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=Path('runs/reference'));p.add_argument('--video',action='store_true');p.add_argument('--lean-sign',type=int,choices=(-1,1),default=1);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False);e=HumanoidEnv(episode_seconds=46,render_mode='rgb_array' if a.video else None)
    writer=None;rows=[]
    try:
        if a.video:
            import imageio.v2 as io
            writer=io.get_writer(a.output/'reference.mp4',fps=50,codec='libx264')
        _,info=e.reset(seed=42);term=trunc=False
        while not(term or trunc):
            _,_,term,trunc,info=e.step(target_to_action(reference(e.steps*CONTROL_DT,a.lean_sign)))
            row={k:v for k,v in info.items() if k!='reward_terms'}
            row.update({f'whole_foot_height_{side}_m':e._minimum_foot_height(i) for i,side in enumerate(('left','right'))})
            row.update({f'actual_{name}_rad':float(e.data.qpos[e.qadr[i]]) for i,name in enumerate(('lh','lk','la','rh','rk','ra'))})
            row.update({f'target_{name}_rad':float(e.applied_command[i]) for i,name in enumerate(('lh','lk','la','rh','rk','ra'))})
            rows.append(row)
            if writer:writer.append_data(e.render())
        import hashlib
        result={'lean_sign':a.lean_sign,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'identity':configuration_identity(),'standing_30s':any(r['duration_s']>=30 and not r['fallen'] for r in rows),
                'reference_completed':not term,'result':rows[-1],
                'max_full_foot_clearance_m':{side:max(r[f'whole_foot_height_{side}_m'] for r in rows) for side in ('left','right')},
                'gate':'PASS only if reviewed weight transfer and lifted step; completing sequence alone is insufficient'}
        (a.output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
        with (a.output/'trajectory.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
        print(json.dumps(result,indent=2))
    finally:
        if writer:writer.close()
        e.close()

if __name__=='__main__':main()
