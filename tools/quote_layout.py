"""Group unchanged frame geometry into a compact quotation-only print layout.

No manufacturing release: layer orientation, horn fit and screw sweeps need review.
STLs remain disconnected bodies, with no sprues or cutting by the assembler.
"""
from pathlib import Path
import json,hashlib
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1]


def main():
    # Euler angles degrees, then XY minimum placement; with separated bounding boxes.
    layout=[('left_foot',[0,0,0],[0,0]),('right_foot',[0,0,0],[95,0]),
            ('torso',[0,90,0],[0,50]),('left_thigh',[90,0,0],[94,50]),
            ('right_thigh',[90,0,0],[123,50]),('left_shin',[0,90,0],[0,143]),
            ('right_shin',[0,90,0],[83,143])]
    folder=ROOT/'cad/quotation';folder.mkdir(exist_ok=True)
    meshes=[];record=[];vol=0
    for name,angles,pos in layout:
        src=ROOT/'cad/stl'/f'{name}.stl';mesh=trimesh.load_mesh(src);vol+=mesh.volume
        transform=trimesh.transformations.euler_matrix(*np.deg2rad(angles))
        mesh.apply_transform(transform);mesh.apply_translation(-mesh.bounds[0]+[*pos,0])
        for other in meshes:
            assert np.any(mesh.bounds[1]<=other.bounds[0]) or np.any(other.bounds[1]<=mesh.bounds[0])
        meshes.append(mesh);record.append({'part':name,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'rotation_deg':angles,'bbox_min_mm':mesh.bounds[0].tolist(),'bbox_max_mm':mesh.bounds[1].tolist()})
    batch=trimesh.util.concatenate(meshes)
    assert len(batch.split())==7 and np.isclose(batch.volume,vol)
    batch.export(folder/'petg_seven_batch.stl')
    soles=[]
    for i,name in enumerate(('left_sole','right_sole')):
        mesh=trimesh.load_mesh(ROOT/'cad/stl'/f'{name}.stl');mesh.apply_translation(-mesh.bounds[0]+[i*95,0,0]);soles.append(mesh)
    solebatch=trimesh.util.concatenate(soles);assert len(solebatch.split())==2
    solebatch.export(folder/'tpu_two_soles_batch.stl')
    (folder/'layout.json').write_text(json.dumps({'status':'QUOTATION ONLY. Structural orientation/fit unapproved; unchanged component geometries','frame_bbox_mm':batch.extents.tolist(),'frame_components':7,'sole_bbox_mm':solebatch.extents.tolist(),'parts':record},indent=2)+'\n')
    print('Frame layout:',batch.extents,'mm;7separate components, unchanged volume; soles:',solebatch.extents)

if __name__=='__main__':main()
