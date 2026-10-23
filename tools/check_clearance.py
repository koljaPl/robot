"""Finite all-frame/case/electronics/moving-fastener-envelope audit; conflicts exit 1.

Fastener envelopes are conservative UNMEASURED proxies, not bolt geometry. Their
own-body attachment intersection is expected and excluded, but moving-body
intersections fail. Wires are flexible and require manual routing validation.
"""
import argparse
import itertools
import json
import sys
from pathlib import Path
import numpy as np
import trimesh
import mujoco
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from build_model import physical_bodies
from robot_config import JOINT_NAMES,HOME,JOINT_LOW,JOINT_HIGH


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'runs/geometry/clearances.json');a=p.parse_args()
    bodies=physical_bodies(json.loads((ROOT/'physical_spec.json').read_text()))
    model=mujoco.MjModel.from_xml_path(str(ROOT/'robot.xml'));data=mujoco.MjData(model)
    ids=[model.joint(j).qposadr[0] for j in JOINT_NAMES]
    poses={'home':HOME,'zero':np.zeros(6),'all_low':JOINT_LOW,'all_high':JOINT_HIGH,'left_swing':np.deg2rad([-20,25,10,-10,10,0])}
    rng=np.random.default_rng(123)
    for i in range(50):poses[f'seed123_sample_{i}']=rng.uniform(JOINT_LOW,JOINT_HIGH)
    local={}
    for b in bodies:
        local[b['name']+'_frame']=(b['name'],'frame',trimesh.load_mesh(ROOT/'cad/stl'/f'{b["name"]}.stl'))
        for c in b['components']:
            kind='servo' if 'servo' in c['name'] else 'electronics' if c['name'] in ('pico_h','imu') else 'fastener_proxy' if c['name'].endswith('_joint_fasteners') else None
            if kind:
                mesh=trimesh.creation.box(extents=np.array(c['dimensions'])*1000);mesh.apply_translation(np.array(c['com'])*1000)
                local[c['name']]=(b['name'],kind,mesh)
    results=[]
    for name,q in poses.items():
        mujoco.mj_resetDataKeyframe(model,data,0);data.qpos[ids]=q;mujoco.mj_forward(model,data)
        world={}
        for key,(body,kind,mesh) in local.items():
            m=mesh.copy();t=np.eye(4);t[:3,:3]=data.xmat[model.body(body).id].reshape(3,3);t[:3,3]=data.xpos[model.body(body).id]*1000;m.apply_transform(t);world[key]=m
        conflicts=[]
        for ka,kb in itertools.combinations(local,2):
            ba,ta,_=local[ka];bb,tb,_=local[kb]
            if ba==bb and 'fastener_proxy' in (ta,tb):continue # intentional attachment, exact bolts unknown
            ma,mb=world[ka],world[kb]
            if np.any(ma.bounds[1]<=mb.bounds[0]) or np.any(mb.bounds[1]<=ma.bounds[0]):continue
            intersection=trimesh.boolean.intersection([ma,mb],engine='manifold')
            if len(intersection.vertices) and intersection.volume>1:
                conflicts.append({'a':ka,'b':kb,'types':[ta,tb],'overlap_mm3':float(intersection.volume)})
        results.append({'pose':name,'conflicts':conflicts})
    count=sum(len(r['conflicts']) for r in results)
    report={'status':'CONFLICTS: NOT RELEASED' if count else 'SAMPLED ENVELOPES CLEAR; physical fit still required','conflict_count':count,'poses':results,
            'limitations':['55 discrete poses do not prove continuous motion clearance','Fastener/horn envelopes are estimates; own attachment overlaps excluded','Flexible wires, connectors and lead exits need physical routing measurements']}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'poses':len(poses),'conflicts':count,'report':str(a.output)}));return int(count>0)

if __name__=='__main__':raise SystemExit(main())
