"""Audit one-factor results, compare the offset fix, and plot calibration priorities."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.report_transfer import raw_step_check


def read_study(directory):
    results={};identities=set();inputs={}
    for manifest_path in sorted(directory.glob('*/summary.json')):
        manifest=json.loads(manifest_path.read_text())
        identities.add(manifest['base_configuration_identity']['configuration'])
        inputs[str(manifest_path)]=hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        for name,digest in manifest['source_sha256'].items():
            assert hashlib.sha256((manifest_path.parent/'source'/name).read_bytes()).hexdigest()==digest
        extra=manifest_path.parent/'replay_inputs.json'
        if extra.exists():
            data=json.loads(extra.read_text())
            for name,digest in data['files'].items():
                assert hashlib.sha256((manifest_path.parent/'source'/name).read_bytes()).hexdigest()==digest
            inputs[str(extra)]=hashlib.sha256(extra.read_bytes()).hexdigest()
        for result in manifest['results']:
            name=result['variant']['name']
            if name in results:raise ValueError('Duplicate case: '+name)
            trace=manifest_path.parent/name/'physics_trace.npz'
            assert hashlib.sha256(trace.read_bytes()).hexdigest()==result['trace_sha256']
            inputs[str(trace)]=result['trace_sha256']
            results[name]=(result,trace)
    if len(results)!=29 or len(identities)!=1:raise ValueError('Need29cases under one explicit configuration')
    return results,identities.pop(),inputs


def independent_checks(result,path):
    with np.load(path,allow_pickle=False) as trace:
        assert len(trace['time_s'])==result['trace_rows']
        rows=[{key:str(trace[key][i]) for key in trace.files} for i in range(result['trace_rows'])]
    checks=[]
    for event in result['events']:
        if event['event']=='step_accepted':
            check=raw_step_check(rows,event,.002)
            assert check['passes_existing_single_step_thresholds']
            checks.append(check)
    m=result['final_metrics']
    assert len(checks)==m['lifted_steps_left']+m['lifted_steps_right']
    return checks


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--legacy',type=Path,required=True);p.add_argument('--corrected',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    old,old_id,old_inputs=read_study(args.legacy)
    new,new_id,new_inputs=read_study(args.corrected)
    assert set(old)==set(new) and old_id!=new_id
    args.output.mkdir(parents=True,exist_ok=False)
    rows=[];all_checks=[]
    for name,(result,path) in new.items():
        before=old[name][0];m=result['final_metrics'];bm=before['final_metrics']
        if result['variant']['family']!='offset':
            assert result['physics_state_sha256_50Hz']==before['physics_state_sha256_50Hz']
            assert m==bm
        checks=independent_checks(result,path)
        all_checks.extend({'case':name,**check} for check in checks)
        rows.append({'case':name,'family':result['variant']['family'],'value':result['variant']['value'],
                     'joint':result['variant']['joint'],'qualifying_steps':len(checks),
                     'legacy_qualifying_steps':bm['lifted_steps_left']+bm['lifted_steps_right'],
                     'alternations':m['alternations'],'body_distance_m':m['distance_m'],
                     'gait_distance_m':m['gait_distance_m'],'duration_s':m['duration_s'],
                     'mean_speed_m_s':m['mean_speed_m_s'],'total_reward':m['total_reward'],
                     'fallen':m['fallen'],'walking_success':m['walking_success'],
                     'legacy_shifted_target_would_clip_ticks':result['legacy_shifted_target_would_clip_control_ticks']})
    nominal=new['nominal'][0]
    for name in ('target_slew_low','target_slew_high','imu_noise_high'):
        assert new[name][0]['physics_state_sha256_50Hz']==nominal['physics_state_sha256_50Hz']
    assert new['imu_noise_high'][0]['observation_sha256_50Hz']!=nominal['observation_sha256_50Hz']
    for name in ('target_slew_low','target_slew_high'):
        assert new[name][0]['observation_sha256_50Hz']==nominal['observation_sha256_50Hz']
    assert not any(r['walking_success'] for r in rows)
    with (args.output/'episodes.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    with (args.output/'credited_steps.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=all_checks[0]);w.writeheader();w.writerows(all_checks)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    by_name={r['case']:r for r in rows}
    families=('mass','torso_mass','friction','strength','shaft_speed','target_slew','damping')
    fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    x=np.arange(len(families))
    for sign,shift in (('low',-.18),('high',.18)):
        axes[0].bar(x+shift,[by_name[family+'_'+sign]['qualifying_steps'] for family in families],.36,label=sign)
    axes[0].axhline(4,color='black',ls='--',lw=.8,label='Nominal4steps')
    axes[0].set_xticks(x,[f.replace('_',' ') for f in families],rotation=30,ha='right')
    axes[0].set(ylabel='Qualifying steps in30s',ylim=(0,4.7),title='One factor at a time; endpoint hypotheses only')
    axes[0].legend();axes[0].grid(axis='y',alpha=.2)
    joints=('left_hip','left_knee','left_ankle','right_hip','right_knee','right_ankle')
    matrix=np.array([[by_name['offset_'+joint+'_'+sign]['qualifying_steps'] for sign in ('minus','plus')] for joint in joints])
    image=axes[1].imshow(matrix,vmin=0,vmax=4,cmap='viridis',aspect='auto')
    axes[1].set_xticks([0,1],['−1°','+1°']);axes[1].set_yticks(range(6),[j.replace('_',' ') for j in joints])
    axes[1].set(title='Corrected physical offset model')
    for i in range(6):
        for j in range(2):axes[1].text(j,i,str(matrix[i,j]),ha='center',va='center',color='white')
    fig.colorbar(image,ax=axes[1],label='Qualifying steps',ticks=range(5))
    fig.suptitle('Frozen script: calibration priorities, not measured hardware tolerances')
    fig.savefig(args.output/'sensitivity.png',dpi=150);plt.close(fig)
    summary={'state':'locally verified one-factor diagnostics, not physical calibration or training',
             'legacy_configuration':old_id,'corrected_configuration':new_id,'cases_per_configuration':29,
             'corrected_independently_checked_credited_steps':len(all_checks),'episodes':rows,
             'offset_cases_with_changed_step_count':[r['case'] for r in rows if r['qualifying_steps']!=r['legacy_qualifying_steps']],
             'zero_offset_cases_exactly_match_previous_physics':True,
             'negative_controls_passed':True,'walking_successes':0,'input_sha256':{**old_inputs,**new_inputs},
             'report_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'limits':['No gait retuning, new PPO or measured plant data.',
                       'Each endpoint changes one factor; results are conditional on this script/model, not a global importance ranking.',
                       'IMU-noise invariance applies to this open-loop script, not an IMU-using learned policy.',
                       'Old clipped-offset evidence remains historical; never relabel its identity.']}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (args.output/'report_sensitivity.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps({k:summary[k] for k in ('cases_per_configuration','corrected_independently_checked_credited_steps','offset_cases_with_changed_step_count','negative_controls_passed')},indent=2))


if __name__=='__main__':main()
