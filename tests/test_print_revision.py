import json
import hashlib
import zipfile
from pathlib import Path

import mujoco
import numpy as np
import pytest
import trimesh

from build_model import physical_bodies
from humanoid_env import HumanoidEnv
from robot_config import ROOT
from tools.budget_gate import check_basket


def test_active_commercial_route_counts_sample_and_unknown_finishing():
    basket=json.loads((ROOT/'procurement.json').read_text())
    report=check_basket(basket)
    assert report['scenario']=='commercial_print' and report['status']=='OVER BUDGET'
    assert report['known_delivered_subtotal_eur']=='105.09'
    assert report['confirmed_minimum_shortfall_eur']=='5.09'
    assert report['total_price_eur'] is None and not report['purchase_cleared']
    pending=' '.join(report['pending_prices']).lower()
    assert 'sample' in pending and '7finished' in pending
    active=basket['items']+basket['scenarios']['commercial_print']['items']
    assert not any('spool' in r['product'].lower() or 'printer purchase' in r['product'].lower() for r in active)
    # An unknown cheaper print is never interpreted as free or a budget pass.
    assert all(r['unit_price_eur'] is None for r in active if r['shop'].startswith('Commercial PETG'))


def test_eight_owned_pads_no_continuous_sole_and_horns_follow_frames():
    spec=json.loads((ROOT/'physical_spec.json').read_text());bodies=physical_bodies(spec)
    owned={b['name']:[c['name'] for c in b['components']] for b in bodies}
    assert sum('servo' in name for names in owned.values() for name in names)==6
    assert not any('sole' in name or 'pico_h'==name for names in owned.values() for name in names)
    assert sum('_pad_' in name for names in owned.values() for name in names)==8
    assert 'left_ankle_horn_hardware' in owned['left_shin']
    assert 'right_ankle_horn_hardware' in owned['right_shin']
    model=mujoco.MjModel.from_xml_path(str(ROOT/'robot.xml'))
    for side in ('left','right'):
        for i in range(4):
            geom=model.geom(f'{side}_foot_pad_{i}')
            assert geom.type==mujoco.mjtGeom.mjGEOM_CYLINDER
            np.testing.assert_allclose(geom.size[:2],[.005,.0015])
    assert all(b['mechanical_limits_deg'] is None for b in bodies)


def test_whole_foot_height_uses_every_pad_and_plate_after_rotation():
    env=HumanoidEnv()
    try:
        env.reset(seed=3)
        env.data.qpos[2]+=.05
        env.data.qpos[env.qadr[2]]=.25
        mujoco.mj_forward(env.model,env.data)
        heights=[]
        for gid in env.foot_geom_groups[0]:
            size=env.model.geom_size[gid]
            shape=(trimesh.creation.cylinder(radius=size[0],height=2*size[1],sections=256)
                   if env.model.geom_type[gid]==mujoco.mjtGeom.mjGEOM_CYLINDER else trimesh.creation.box(extents=2*size))
            transform=np.eye(4);transform[:3,:3]=env.data.geom_xmat[gid].reshape(3,3);transform[:3,3]=env.data.geom_xpos[gid]
            shape.apply_transform(transform);heights.append(shape.bounds[0,2])
        assert env._minimum_foot_height(0)==pytest.approx(min(heights),abs=1e-6)
        assert env._minimum_foot_height(0)<env.data.site_xpos[env.foot_center_sites[0],2]-.001
    finally:env.close()


def test_order_packages_have_only_their_own_quantities_and_matching_hashes():
    for kind,count in [('sample',2),('frame',7)]:
        with zipfile.ZipFile(ROOT/f'cad/{kind}_quotation_package.zip') as package:
            stls=[n for n in package.namelist() if n.endswith('.stl')]
            assert len(stls)==count and not any('sole' in n or 'QUOTE_ONLY' in n for n in stls)
            manifest=json.loads(package.read(f'cad/print_order/{kind}_manifest.json'))
            assert not manifest['manufacturing_approved'] and manifest['package_quantity']==count
            for row in manifest['files']:
                raw=package.read('cad/print_order/'+row['file'])
                assert hashlib.sha256(raw).hexdigest()==row['sha256']
                if kind=='frame':
                    original=trimesh.load_mesh(ROOT/'cad/stl'/Path(row['file']).name)
                    original.apply_transform(row['body_to_print_bed_transform_mm'])
                    np.testing.assert_allclose(original.bounds,row['bounds_mm'],atol=1e-5)
        assert 'UNKNOWN' in (ROOT/'cad/print_order/fasteners.csv').read_text()


def test_geometry_links_contacts_and_frame_accounting_share_spec():
    spec=json.loads((ROOT/'physical_spec.json').read_text())
    g=spec['geometry'];manifest=json.loads((ROOT/'cad/print_manifest.json').read_text())
    rows={r['part']:r for r in manifest['parts']}
    for b in physical_bodies(spec):
        frame=next(c for c in b['components'] if c['name']==b['name']+'_frame')
        assert frame['mass']*1000==pytest.approx(rows[b['name']]['solid_petg_mass_g_at_1_27'])
        if b['name'].endswith('shin'):assert b['position'][2]==-g['thigh_length']
        if b['name'].endswith('foot'):
            assert b['position'][2]==-g['shin_length']
            pads=[c for c in b['components'] if c.get('primitive')=='cylinder_z']
            assert min(c['com'][2]-c['dimensions'][2]/2 for c in pads)==pytest.approx(-g['ankle_to_floor'])
