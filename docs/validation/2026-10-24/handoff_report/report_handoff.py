"""Independently audit all credited handoff steps and compare nominal/DR probes."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.report_transfer import raw_step_check


def report(review,output):
    output.mkdir(parents=True,exist_ok=False)
    episodes=[];checks=[];inputs={}
    for path in sorted(review.glob('*/summary.json')):
        manifest=json.loads(path.read_text());run=manifest['profiles'][0]
        trace_path=path.parent/run['profile']/'physics_trace.csv'
        for source,digest in manifest['source_sha256'].items():
            assert hashlib.sha256((path.parent/'source'/source).read_bytes()).hexdigest()==digest
        for input_path in (path,trace_path):inputs[str(input_path)]=hashlib.sha256(input_path.read_bytes()).hexdigest()
        with trace_path.open() as f:rows=list(csv.DictReader(f))
        accepted=[e for e in run['events'] if e['event']=='step_accepted']
        for event in accepted:
            c=raw_step_check(rows,event,.002)
            c['episode']=path.parent.name
            assert c['passes_existing_single_step_thresholds']
            checks.append(c)
        m=run['final_metrics']
        assert len(accepted)==m['lifted_steps_left']+m['lifted_steps_right']
        episodes.append({'episode':path.parent.name,'domain_randomization':run['domain_randomization'],
                         'seed':run['seed'],'body_distance_m':m['distance_m'],'gait_distance_m':m['gait_distance_m'],
                         'mean_speed_m_s':m['mean_speed_m_s'],'duration_s':m['duration_s'],
                         'steps_left':m['lifted_steps_left'],'steps_right':m['lifted_steps_right'],
                         'alternations':m['alternations'],'fallen':m['fallen'],'walking_success':m['walking_success']})
    if len(episodes)!=7:raise ValueError('Expected2 mirrored nominal and5 declared randomized diagnostic runs')
    with (output/'episodes.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=episodes[0]);w.writeheader();w.writerows(episodes)
    nominal=[r for r in episodes if not r['domain_randomization']]
    randomized=[r for r in episodes if r['domain_randomization']]
    assert len(nominal)==2 and len(randomized)==5
    assert all(r['steps_left']==2 and r['steps_right']==2 and r['alternations']==3 for r in nominal)
    assert all(not r['walking_success'] for r in episodes)
    assert np.isclose(nominal[0]['body_distance_m'],nominal[1]['body_distance_m'],atol=1e-9,rtol=0)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,1,figsize=(11,8),layout='constrained')
    trace=review/'nominal_left/compact/physics_trace.csv'
    with trace.open() as f:rows=list(csv.DictReader(f))
    times=[float(r['time_s']) for r in rows]
    for foot in ('left','right'):
        axes[0].plot(times,[float(r[foot+'_height_m'])*1000 for r in rows],lw=1,label=foot)
    axes[0].axhline(3,color='black',lw=.8,ls='--',label='3mm required')
    for c in checks:
        if c['episode']=='nominal_left':axes[0].axvline(c['touchdown_time_s'],color='tab:green',lw=.8,ls=':')
    axes[0].set(xlabel='Time (s)',ylabel='Whole-foot minimum height (mm)',ylim=(-1,5),
                title='Nominal script:4credited alternating steps, narrow lift margin')
    axes[0].legend();axes[0].grid(alpha=.25)
    x=np.arange(len(episodes));axes[1].bar(x-.18,[r['body_distance_m']*100 for r in episodes],.36,label='Body displacement')
    axes[1].bar(x+.18,[r['gait_distance_m']*100 for r in episodes],.36,label='Qualifying gait distance')
    axes[1].set_xticks(x,[r['episode'].replace('randomized_','DR') for r in episodes],rotation=15)
    axes[1].set(ylabel='Distance (cm)',title='Motion alone is not qualifying walking; target30cm remains unmet')
    axes[1].grid(axis='y',alpha=.25);axes[1].legend()
    fig.savefig(output/'handoff_results.png',dpi=150);plt.close(fig)
    result={'state':'provisional scripted baseline; walking acceptance unmet in every trial',
            'episodes':episodes,'independent_step_checks':checks,
            'independently_verified_credited_steps':len(checks),'walking_successes':0,
            'nominal_body_distance_m':nominal[0]['body_distance_m'],
            'randomized_qualifying_step_counts':[r['steps_left']+r['steps_right'] for r in randomized],
            'input_sha256':inputs,'report_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'interpretation':'A hand-written script, not PPO. Five mixed randomization draws are diagnostic hypotheses, not measured tolerances, formal A/B results, parameter attribution, or physical transfer.'}
    (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    (output/'report_handoff.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps({k:result[k] for k in ('independently_verified_credited_steps','walking_successes','nominal_body_distance_m','randomized_qualifying_step_counts')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--review',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args();report(args.review,args.output)
