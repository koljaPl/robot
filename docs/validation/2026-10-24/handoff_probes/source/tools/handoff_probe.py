"""Two bounded, open-loop weight-handoff probes after the phase timing study.

Retain .95s leg swaps and all plant/safety limits. After touchdown, prepare the
opposite stance instead of retracing the previous step back to HOME. Targets use
time and design geometry only. No pinning, feedback truth, training or hardware.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from calibration import configuration_identity
from humanoid_env import HumanoidEnv
from robot_config import HOME,CONTROL_DT,PHYSICS_DT,JOINT_LOW,JOINT_HIGH,target_to_action
from tools.stance_transfer import left_pose,matched_roll,mirror_targets,smooth
from tools.audit_transfer import GaitTrace
from tools.phase_study import flight_summaries

PROFILES={'slow':{'prepare_s':4.,'load_s':2.,'swap_s':.95,'hold_s':1.05,'cycles':3},
          'compact':{'prepare_s':3.,'load_s':1.5,'swap_s':.95,'hold_s':.55,'cycles':4}}


def poses(stance):
    crouch=left_pose(1,50);crouch[[2,5]]=matched_roll(crouch[1],crouch[4])
    loaded=crouch.copy();loaded[[2,5]]=np.deg2rad(20)
    prepared=np.deg2rad([-10,10,20,-35,35,20])
    if stance:crouch,loaded,prepared=[mirror_targets(q) for q in (crouch,loaded,prepared)]
    return crouch,loaded,prepared


def target_at(time_s,profile,first_stance='left'):
    if profile not in PROFILES or first_stance not in ('left','right'):
        raise ValueError('Unknown handoff profile/first stance')
    if not np.isfinite(time_s) or time_s<0:raise ValueError('Invalid time')
    if time_s<=2:return HOME.copy()
    config=PROFILES[profile];period=sum(config[k] for k in ('prepare_s','load_s','swap_s','hold_s'))
    index=min(int((time_s-2)/period),config['cycles']-1)
    local=time_s-2-index*period;stance=(index+int(first_stance=='right'))%2
    crouch,loaded,prepared=poses(stance)
    if local<=config['prepare_s']:
        f=smooth(local/config['prepare_s'])
        if index==0:
            q=HOME+f*(crouch-HOME)
            q[[2,5]]=(1 if stance==0 else -1)*matched_roll(q[stance*3+1],q[(1-stance)*3+1])
        else:
            previous=poses(1-stance)[2]
            q=previous+f*(crouch-previous)
    elif local<=config['prepare_s']+config['load_s']:
        q=crouch+smooth((local-config['prepare_s'])/config['load_s'])*(loaded-crouch)
    elif local<=config['prepare_s']+config['load_s']+config['swap_s']:
        q=loaded+smooth((local-config['prepare_s']-config['load_s'])/config['swap_s'])*(prepared-loaded)
    else:q=prepared.copy()
    if np.any(q<JOINT_LOW-1e-12) or np.any(q>JOINT_HIGH+1e-12):raise ValueError('Unsafe target')
    return q


def run(profile,output,first_stance,video=False):
    env=HumanoidEnv(episode_seconds=30,render_mode='rgb_array' if video else None)
    writer=None
    try:
        env.reset(seed=42);trace=GaitTrace(env)
        if video:
            import imageio.v2 as io
            from evaluate import show_physical_geometry
            show_physical_geometry(env.model);writer=io.get_writer(output/'episode.mp4',fps=50,codec='libx264')
        while not env.done:
            target=target_at(env.steps*CONTROL_DT,profile,first_stance)
            _,_,_,_,info=env.step(target_to_action(target))
            if writer:writer.append_data(env.render())
        with (output/'physics_trace.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=trace.rows[0]);w.writeheader();w.writerows(trace.rows)
        return {'profile':profile,'first_stance':first_stance,'durations':PROFILES[profile],
                'final_metrics':info,'events':trace.events,'flights_above_2mm':flight_summaries(trace.rows),
                'video_saved':video,'endpoint':'last prepared support target held; no automatic return or hardware deployment'}
    finally:
        if writer:writer.close()
        env.close()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--profiles',nargs='+',choices=PROFILES,default=list(PROFILES))
    p.add_argument('--first-stance',choices=('left','right'),default='left');p.add_argument('--video',action='store_true')
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=False);reports=[]
    for profile in args.profiles:
        directory=args.output/profile;directory.mkdir();r=run(profile,directory,args.first_stance,args.video);reports.append(r)
        (directory/'summary.json').write_text(json.dumps(r,indent=2)+'\n');print(profile,r['final_metrics'],flush=True)
    identity=configuration_identity()
    sources=set(identity['files']) | {'tools/handoff_probe.py','tools/phase_study.py','tools/stance_transfer.py',
        'tools/audit_transfer.py','tools/report_transfer.py','tools/analyze_support.py','tools/diagnose_motion.py',
        'evaluate.py','requirements.txt','requirements-dev.txt'}
    sources|={str(p.relative_to(ROOT)) for p in (ROOT/'cad/stl').glob('*.stl')};hashes={}
    for name in sorted(sources):
        path=args.output/'source'/name;path.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/name,path);hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    summary={'state':'provisional handoff diagnosis, no learned/physical walking claim',
             'configuration_identity':identity,'source_sha256':hashes,'profiles':reports,'plant_changed':False,
             'acceptance_thresholds_changed':False,'seed':42,'training_steps_added':0}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')


if __name__=='__main__':main()
