"""Bounded timing/history probes; unchanged physics, thresholds and command limits.

Declared comparisons: exact baseline; .75s/1.25s swap instead of1s;
40deg preparation instead of50deg;2s extra HOME settling between halves.
The last case is32s and is a history diagnostic, never a30s acceptance trial.
Targets depend only on time/specification, not privileged trace or joint feedback.
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
from robot_config import HOME,CONTROL_DT,PHYSICS_DT,target_to_action
from tools.stance_transfer import target_at,smooth,matched_roll,mirror_targets
from tools.audit_transfer import GaitTrace
from tools.report_transfer import raw_step_check

CASES=('baseline','fast_swap','slow_swap','shallow40','settle2','moderate_swap')


def duration(case):
    if case not in CASES:raise ValueError('Unknown phase-study case')
    return 32 if case=='settle2' else 30


def study_target(time_s,case,first_stance='left'):
    if case not in CASES or first_stance not in ('left','right'):
        raise ValueError('Unknown case or first stance')
    if not np.isfinite(time_s) or time_s<0:raise ValueError('Invalid time')
    if case=='settle2':
        reference_time=time_s if time_s<=16 else 16 if time_s<=18 else time_s-2
        q=target_at(reference_time,'geometric50_swap')
    elif time_s<=2 or time_s>=30:
        q=HOME.copy()
    elif case=='baseline':
        q=target_at(time_s,'geometric50_swap')
    else:
        stance=0 if time_s<=16 else 1
        start=2 if stance==0 else 16
        local=time_s-start
        if case in ('fast_swap','slow_swap','moderate_swap'):
            swap={'fast_swap':.75,'slow_swap':1.25,'moderate_swap':.95}[case]
            warped=float(np.interp(local,[0,6,6+swap,9-swap,9,14],[0,6,7,8,9,14]))
            q=target_at(2+warped,'geometric50_swap')
        else:
            q=target_at(2+local,'geometric40')
            if 6<local<9:
                prepared=np.deg2rad([-10,10,20,-35,35,20])
                blend=smooth(local-6) if local<=7 else 1.0 if local<=8 else 1-smooth(local-8)
                q[[2,5]]=np.deg2rad(20)
                q+=blend*(prepared-q)
            elif 9<=local<10:
                base=matched_roll(q[1],q[4])
                q[[2,5]]=np.deg2rad(20)+(base-np.deg2rad(20))*smooth(local-9)
        if stance==1:q=mirror_targets(q)
    return mirror_targets(q) if first_stance=='right' else q


def flight_summaries(rows):
    flights=[]
    for foot in ('left','right'):
        start=None
        for index,row in enumerate(rows):
            if not row[foot+'_contact'] and start is None:start=index
            if row[foot+'_contact'] and start is not None:
                peak=max(r[foot+'_height_m'] for r in rows[start:index])
                if peak>=.002:
                    # The independent checker reads the same CSV text format as
                    # archived audit records, not GaitMetrics internal flags.
                    encoded=[{k:str(v) for k,v in r.items()} for r in rows]
                    check=raw_step_check(encoded,{'foot':foot,'time_s':row['time_s']},PHYSICS_DT)
                    check.update({'takeoff_time_s':rows[start]['time_s'],'peak_height_m':peak})
                    flights.append(check)
                start=None
    return sorted(flights,key=lambda f:f['takeoff_time_s'])


def snapshot(env,requested):
    return {'time_s':env.steps*CONTROL_DT,'requested_deg':np.rad2deg(requested).tolist(),
            'applied_ack_deg':np.rad2deg(env.applied_command).tolist(),
            'actual_joint_deg_DIAGNOSTIC_ONLY':np.rad2deg(env.data.qpos[env.qadr]).tolist(),
            'root_qpos_DIAGNOSTIC_ONLY':env.data.qpos[:7].tolist(),
            'root_qvel_DIAGNOSTIC_ONLY':env.data.qvel[:6].tolist(),
            'foot_centres_m_DIAGNOSTIC_ONLY':env.data.site_xpos[env.foot_center_sites].tolist()}


def run(case,output,first_stance):
    env=HumanoidEnv(episode_seconds=duration(case))
    commands=[];states=[]
    try:
        env.reset(seed=42);trace=GaitTrace(env)
        boundaries=(2,18 if case=='settle2' else 16)
        while not env.done:
            requested=study_target(env.steps*CONTROL_DT,case,first_stance)
            _,_,_,_,info=env.step(target_to_action(requested))
            row={'time_s':env.steps*CONTROL_DT}
            for j in range(6):
                row[f'requested{j}_rad']=requested[j]
                row[f'applied_ack{j}_rad']=env.applied_command[j]
            commands.append(row)
            if any(abs(env.steps*CONTROL_DT-b)<1e-8 for b in boundaries):states.append(snapshot(env,requested))
        for name,rows in [('physics_trace',trace.rows),('commands',commands)]:
            with (output/(name+'.csv')).open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
        flights=flight_summaries(trace.rows)
        return {'case':case,'first_stance':first_stance,'final_metrics':info,'events':trace.events,
                'flights_above_2mm':flights,'phase_boundary_states':states,
                'duration_s':duration(case),'walking_acceptance_trial':False,
                'note':'settle2 extends only the HOME hold;32s is not a30s walking trial' if case=='settle2' else 'bounded trajectory diagnostic, not learned or physical walking'}
    finally:env.close()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--cases',nargs='+',choices=CASES,default=CASES)
    p.add_argument('--first-stance',choices=('left','right'),default='left')
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    reports=[]
    for case in args.cases:
        directory=args.output/case;directory.mkdir()
        report=run(case,directory,args.first_stance);reports.append(report)
        (directory/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
        m=report['final_metrics'];print(case,'steps',m['lifted_steps_left'],m['lifted_steps_right'],'alternations',m['alternations'],'body_m',m['distance_m'],flush=True)
    identity=configuration_identity()
    sources=set(identity['files']) | {'tools/phase_study.py','tools/stance_transfer.py','tools/audit_transfer.py',
        'tools/report_transfer.py','tools/analyze_support.py','tools/diagnose_motion.py','requirements.txt','requirements-dev.txt'}
    sources|={str(p.relative_to(ROOT)) for p in (ROOT/'cad/stl').glob('*.stl')}
    hashes={}
    for name in sorted(sources):
        path=args.output/'source'/name;path.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/name,path);hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    summary={'state':'provisional phase/history diagnosis; no training or physical verification',
             'configuration_identity':identity,'source_sha256':hashes,'cases':reports,
             'declared_cases':args.cases,'first_stance':args.first_stance,'seed':42,'plant_changed':False,
             'acceptance_thresholds_changed':False,'training_steps_added':0}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')


if __name__=='__main__':main()
