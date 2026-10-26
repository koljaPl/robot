"""Recompute a credited step from raw2ms rows, aggregate declared probe replays."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np


def raw_step_check(rows, event, dt):
    """Independent threshold check over a contiguous flight, without GaitMetrics."""
    foot=event['foot'];other='right' if foot=='left' else 'left'
    index=min(range(len(rows)),key=lambda j:abs(float(rows[j]['time_s'])-event['time_s']))
    if abs(float(rows[index]['time_s'])-event['time_s'])>1e-8:
        raise ValueError('Event has no corresponding physics row')
    start=index
    while start>0 and rows[start-1][foot+'_contact']=='False':start-=1
    if start==0 or start==index:
        raise ValueError('No bounded contact-free flight before touchdown')
    before=rows[start-1]
    origin=np.array([float(before[other+'_x_m']),float(before[other+'_y_m'])])
    duration=longest=0.0;max_slip=0.0;opposite_ok=True
    for r in rows[start:index]:
        supported=r[other+'_supported']=='True' and r[other+'_contact']=='True'
        opposite_ok &= supported
        slip=np.linalg.norm(np.array([float(r[other+'_x_m']),float(r[other+'_y_m'])])-origin)
        max_slip=max(max_slip,float(slip))
        duration=duration+dt if float(r[foot+'_height_m'])>=.003 and supported else 0.0
        longest=max(longest,duration)
    touchdown=rows[index]
    advance=float(touchdown[foot+'_x_m'])-float(before[foot+'_x_m'])
    lateral=float(touchdown[foot+'_y_m'])-float(before[foot+'_y_m'])
    touchdown_slip=float(np.linalg.norm(np.array([float(touchdown[other+'_x_m']),float(touchdown[other+'_y_m'])])-origin))
    max_slip=max(max_slip,touchdown_slip)
    both_supported=all(touchdown[s+'_supported']=='True' for s in ('left','right'))
    passed=bool(longest>=.04-1e-10 and opposite_ok and max_slip<=.003 and advance>=.005
                and abs(lateral)<=.020 and both_supported and touchdown[foot+'_contact']=='True')
    return {'foot':foot,'touchdown_time_s':event['time_s'],
            'raw_max_continuous_3mm_lift_s':longest,'raw_forward_advance_m':advance,
            'raw_lateral_advance_m':lateral,'raw_max_stance_slip_m':max_slip,
            'opposite_continuously_supported':bool(opposite_ok),'both_supported_at_touchdown':both_supported,
            'passes_existing_single_step_thresholds':passed}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review',type=Path,required=True)
    parser.add_argument('--audit',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    reports=[];checks=[];inputs={}
    for path in sorted(args.review.glob('*/summary.json')):
        data=json.loads(path.read_text());inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for p in data['profiles']:
            m=p['final_metrics']
            reports.append({'first_stance':p['first_stance'],'seed':p['seed'],'distance_m':m['distance_m'],
                            'steps_left':m['lifted_steps_left'],'steps_right':m['lifted_steps_right'],
                            'alternations':m['alternations'],'gait_distance_m':m['gait_distance_m'],
                            'fallen':m['fallen'],'walking_success':m['walking_success']})
    for path in sorted(args.audit.glob('*/summary.json')):
        data=json.loads(path.read_text());csv_path=path.parent/'physics_trace.csv'
        inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
        inputs[str(csv_path)]=hashlib.sha256(csv_path.read_bytes()).hexdigest()
        with csv_path.open() as f:rows=list(csv.DictReader(f))
        for event in data['events']:
            if event['event']=='step_accepted':
                check=raw_step_check(rows,event,data['physics_timestep_s'])
                check['first_stance']=data['first_stance'];checks.append(check)
        for name,digest in data['source_sha256'].items():
            assert hashlib.sha256((path.parent/'source'/name).read_bytes()).hexdigest()==digest
    if len(reports)!=6 or len(checks)!=2 or not all(c['passes_existing_single_step_thresholds'] for c in checks):
        raise ValueError('Expected6 declared replays and2 independently validated single steps')
    with (args.output/'episodes.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=reports[0]);w.writeheader();w.writerows(reports)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    trace_path=args.audit/'left42/physics_trace.csv'
    with trace_path.open() as f:rows=list(csv.DictReader(f))
    fig,axes=plt.subplots(2,1,figsize=(10,6),sharex=True,layout='constrained')
    time=np.array([float(r['time_s']) for r in rows])
    for foot in ('left','right'):
        axes[0].plot(time,[float(r[foot+'_height_m'])*1000 for r in rows],label=foot,lw=1)
        axes[1].plot(time,[float(r[foot+'_x_m'])*1000 for r in rows],label=foot,lw=1)
    axes[0].axhline(3,color='black',ls='--',lw=.8,label='3mm threshold')
    for ax in axes:
        ax.axvline(checks[0]['touchdown_time_s'],color='tab:green',ls=':',label='credited touchdown')
        ax.grid(alpha=.25);ax.legend(loc='upper left')
    axes[0].set(ylabel='Whole-foot minimum height (mm)',ylim=(-1,5))
    axes[1].set(xlabel='Time (s)',ylabel='Foot-centre forward position (mm)')
    fig.suptitle('Scripted provisional model: one credited step, no alternating walking')
    fig.savefig(args.output/'single_step_trace.png',dpi=150);plt.close(fig)
    result={'state':'locally verified scripted single step; walking acceptance unmet','episodes':reports,
            'independent_raw_step_checks':checks,'walking_successes':sum(r['walking_success'] for r in reports),
            'interpretation':'Sensor seeds change unused noisy IMU only: nominal open-loop dynamics are identical, not6independent robustness trials. Mirroring reproduces the opposite-side step.',
            'input_sha256':inputs,'report_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (args.output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.output/'report_transfer.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(checks,indent=2))


if __name__=='__main__':main()
