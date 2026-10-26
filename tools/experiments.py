"""Formal matched A/B experiment orchestration. Refuses uncleared hardware/model gates."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'runs/formal');p.add_argument('--steps',type=int,default=1000000);p.add_argument('--calibration',type=Path,required=True);p.add_argument('--pilot-a0',type=Path,help='Compatible measured A0 pilot checkpoint; included in total budget');a=p.parse_args()
    gates=json.loads((ROOT/'docs/gates.json').read_text())
    if not all(gates.values()):p.error('Blocked: '+', '.join(k for k,v in gates.items() if not v))
    if not 1024<=a.steps<=1000000:p.error('Per-condition budget must be 1024..1000000')
    if a.output.exists():p.error('Use a new experiment directory')
    a.output.mkdir(parents=True)
    def run(script,*args):subprocess.run([sys.executable,str(ROOT/script),*map(str,args)],cwd=ROOT,check=True)
    for seed in (0,1,2):
        identities=[]
        for condition in ('A','B'):
            out=a.output/f'{condition}_{seed}'
            run('train.py','--stage','formal','--steps',a.steps,'--seed',seed,'--output',out,'--calibration',a.calibration,*(['--randomize'] if condition=='B' else []),*(['--resume',a.pilot_a0] if seed==0 and condition=='A' and a.pilot_a0 else []))
            identities.append(json.loads((out/'training_config.json').read_text())['initial_policy_sha256'])
            for randomized in (False,True):
                run('evaluate.py','--model',out/'best_model.zip','--calibration',a.calibration,'--seed',1000,'--episodes',10,'--output',out/('test_dr' if randomized else 'test_nominal'),'--video',*(['--randomize'] if randomized else []))
        if identities[0]!=identities[1]:raise RuntimeError('A/B initial weights mismatch')
    for baseline in ('home','untrained'):
        for randomized in (False,True):
            seeds=(0,1,2) if baseline=='untrained' else (0,)
            for seed in seeds:run('evaluate.py','--baseline',baseline,'--policy-seed',seed,'--calibration',a.calibration,'--seed',1000,'--episodes',10,'--output',a.output/f'{baseline}_{seed}_{randomized}','--video',*(['--randomize'] if randomized else []))
    summaries=[{'path':str(p.relative_to(a.output)),**json.loads(p.read_text())} for p in a.output.rglob('summary.json')]
    (a.output/'aggregate.json').write_text(json.dumps(summaries,indent=2)+'\n')

if __name__=='__main__':main()
