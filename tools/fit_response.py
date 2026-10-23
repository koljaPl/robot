"""Grid-fit a FIRST-ORDER diagnostic to one isolated measured servo step.

CSV time_s,target_rad,angle_rad; >=20 timestamped externally measured samples.
This does not identify continuous torque, backlash, or MuJoCo kp/kv uniquely.
"""
import argparse
import json
from pathlib import Path
import numpy as np


def fit(data):
    t,u,q=[np.atleast_1d(data[k]).astype(float) for k in ('time_s','target_rad','angle_rad')]
    if len(t)<20 or not np.isfinite([t,u,q]).all() or np.any(np.diff(t)<=0):raise ValueError('Need >=20 finite increasing samples')
    changes=np.flatnonzero(np.abs(np.diff(u))>1e-5)
    if len(changes)!=1:raise ValueError('Use one isolated step per file, with pre-step samples')
    index=changes[0]+1;t0=t[index];q0=np.median(q[:index]);amplitude=u[-1]-u[0]
    if abs(amplitude)<np.deg2rad(5):raise ValueError('Step too small for this diagnostic')
    best=None
    for delay in np.arange(0,.081,.002):
        for tau in np.geomspace(.015,.5,100):
            basis=1-np.exp(-np.maximum(0,t-t0-delay)/tau)
            gain=float(np.dot(basis,q-q0)/max(np.dot(basis,basis),1e-12))
            pred=q0+gain*basis;error=float(np.mean((q-pred)**2))
            if best is None or error<best['mse_rad2']:
                best={'delay_s':float(delay),'time_constant_s':float(tau),'step_gain':gain/amplitude,'mse_rad2':error,'rmse_deg':float(np.rad2deg(np.sqrt(error)))}
    return best


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('csv',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result={'source':str(a.csv),'fit':fit(np.genfromtxt(a.csv,delimiter=',',names=True)),'state':'measured-data fit only; requires source/video review, not a validated actuator model'}
    with a.output.open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
