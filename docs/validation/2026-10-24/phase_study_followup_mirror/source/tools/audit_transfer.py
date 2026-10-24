"""Trace physics-step gait evidence without changing model, actions or metrics.

The wrapper delegates to the unchanged GaitMetrics.update and only copies state.
This is privileged simulation diagnosis; never a deployable policy observation.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from calibration import configuration_identity
from humanoid_env import HumanoidEnv
from robot_config import CONTROL_DT, PHYSICS_DT, target_to_action
from tools.stance_transfer import target_at, mirror_targets


class GaitTrace:
    def __init__(self, env):
        self.env=env
        self.original=env.gait.update
        self.rows=[]
        self.events=[]
        self.qualified_at=[None,None]
        env.gait.update=self.update

    def update(self, centers, heights, contacts, supported, dt):
        gait=self.env.gait
        steps=gait.steps.copy(); qualified=gait.qualified.copy()
        start=gait.start.copy(); stance_start=gait.stance_start.copy()
        self.original(centers,heights,contacts,supported,dt)
        row={'time_s':float(self.env.data.time)}
        for i,side in enumerate(('left','right')):
            row.update({side+'_x_m':float(centers[i,0]),side+'_y_m':float(centers[i,1]),
                        side+'_height_m':float(heights[i]),side+'_contact':bool(contacts[i]),
                        side+'_supported':bool(supported[i]),side+'_continuous_clear_s':float(gait.clear_time[i])})
            if gait.airborne[i] and not gait.qualified[i]:
                self.qualified_at[i]=None
            if gait.qualified[i] and not qualified[i]:
                self.qualified_at[i]=float(self.env.data.time)
                self.events.append({'event':'lift_qualified','foot':side,'time_s':float(self.env.data.time),
                                    'continuous_whole_foot_clear_s':float(gait.clear_time[i]),
                                    'whole_foot_height_m':float(heights[i]),'foot_contact':bool(contacts[i]),
                                    'opposite_supported':bool(supported[1-i])})
            if gait.steps[i]>steps[i]:
                self.events.append({'event':'step_accepted','foot':side,'time_s':float(self.env.data.time),
                                    'qualified_at_s':self.qualified_at[i],
                                    'forward_touchdown_advance_m':float(centers[i,0]-start[i,0]),
                                    'lateral_touchdown_advance_m':float(centers[i,1]-start[i,1]),
                                    'stance_center_slip_m':float(np.linalg.norm(centers[1-i,:2]-stance_start[i])),
                                    'both_feet_supported_at_touchdown':bool(all(supported)),
                                    'credited_midpoint_distance_m':float(gait.distance)})
        self.rows.append(row)


def run(output, first_stance):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    env=HumanoidEnv(episode_seconds=30)
    try:
        env.reset(seed=42);trace=GaitTrace(env)
        while not env.done:
            target=target_at(env.steps*CONTROL_DT,'geometric50_swap')
            if first_stance=='right':target=mirror_targets(target)
            _,_,_,_,info=env.step(target_to_action(target))
        with (output/'physics_trace.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=trace.rows[0]);w.writeheader();w.writerows(trace.rows)
        (output/'events.json').write_text(json.dumps(trace.events,indent=2)+'\n')
        report={'state':'privileged simulation diagnostic; no walking/physical approval',
                'profile':'geometric50_swap','first_stance':first_stance,'seed':42,'physics_timestep_s':PHYSICS_DT,
                'configuration_identity':configuration_identity(),'final_metrics':info,'events':trace.events,
                'trace_rows':len(trace.rows),'metric_implementation_changed':False,
                'limits':'Existing thresholds retained. Single credited step is not alternating walking; no physical or learned claim.'}
    finally:env.close()
    sources=set(report['configuration_identity']['files']) | {'tools/audit_transfer.py','tools/stance_transfer.py',
            'tools/analyze_support.py','tools/diagnose_motion.py','evaluate.py','requirements.txt','requirements-dev.txt'}
    sources|={str(p.relative_to(ROOT)) for p in (ROOT/'cad/stl').glob('*.stl')}
    hashes={}
    for name in sorted(sources):
        path=output/'source'/name;path.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/name,path);hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    report['source_sha256']=hashes
    (output/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','configuration_identity')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--first-stance',choices=('left','right'),default='left')
    args=p.parse_args();run(args.output,args.first_stance)
