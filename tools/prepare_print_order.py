"""Build separate quotation-only sample/frame packages from the physical revision.

No releases, orders or supplier messages. All order files have source hashes;
unknown horn/screw interfaces remain explicit in the bundle and drawings.
"""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from cad.build_frame import cradle,horn_plate,mesh
from tools.prepare_local_print import generate as prepare_plates,place


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def interface_drawing(folder,spec):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle,Circle
    g=spec['geometry'];m=g['mount'];h=spec['hardware_interfaces']['ear_bolt']
    fig,axes=plt.subplots(2,2,figsize=(12,9))
    def dimension(ax,a,b,label,offset=0):
        ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='<->',lw=.8))
        ax.text((a[0]+b[0])/2+offset,(a[1]+b[1])/2,label,fontsize=8,ha='center',va='bottom',bbox=dict(facecolor='white',edgecolor='none',pad=1))
    ax=axes[0,0];w=m['case_plate_width']*1000;ht=m['case_plate_height']*1000;dz=spec['servo']['shaft_offset_along_case_length']*1000
    ax.add_patch(Rectangle((-w/2,-ht/2),w,ht,fill=False,color='#1565a8'))
    case=spec['servo']['housing_dimensions'];ax.add_patch(Rectangle((-(case[1]*1000+g['cad_clearance']*1000)/2,-(case[0]*1000+g['cad_clearance']*1000)/2),case[1]*1000+g['cad_clearance']*1000,case[0]*1000+g['cad_clearance']*1000,fill=False,color='#1565a8'))
    for sign in (-1,1):ax.add_patch(Circle((0,sign*spec['servo']['mounting_hole_spacing']*500),m['ear_clearance_diameter']*500,fill=False))
    dimension(ax,(-13,-19),(-13,19),'38 mm',-4);dimension(ax,(-10,22),(10,22),'20 mm')
    dimension(ax,(4,-14),(4,14),'28 mm*',6)
    ax.set(xlim=(-23,24),ylim=(-24,28),title='Servo cradle, front (x-z); holes 2 x dia2.4*')
    ax.text(-21,-23,'*Ear pattern/shaft offset: ESTIMATED\nCase opening12.6 x23.2; plate3 thick',fontsize=8)
    ax=axes[0,1];ax.add_patch(Rectangle((-12,-14),24,28,fill=False,color='#1565a8'));ax.add_patch(Circle((0,0),m['shaft_access_diameter']*500,fill=False))
    for sign in (-1,1):ax.add_patch(Rectangle((-1.2,sign*9-3.5),2.4,7,fill=False))
    dimension(ax,(-12,18),(12,18),'24 mm');dimension(ax,(16,-14),(16,14),'28 mm',5)
    ax.set(xlim=(-20,30),ylim=(-22,24),title='Horn plate, front; 3 mm thick')
    ax.text(-19,-21,'Access dia6; slots2.4 x7 at +/-9 mm*\n*Factory horn/retainer/screw fit UNKNOWN',fontsize=8)
    ax=axes[1,0];foot=np.array(g['foot_dimensions'])*1000;cx=g['foot_center'][0]*1000
    ax.add_patch(Rectangle((cx-foot[0]/2,-foot[1]/2),foot[0],foot[1],fill=False,color='#1565a8'))
    for xy in g['grip_pad']['centres_xy']:ax.add_patch(Circle(np.array(xy)*1000,g['grip_pad']['radius']*1000,color='#333333'))
    dimension(ax,(cx-foot[0]/2,28),(cx+foot[0]/2,28),'90 mm');dimension(ax,(-47,-22.5),(-47,22.5),'45 mm',-5)
    ax.set(xlim=(-58,62),ylim=(-39,36),title='Foot underside: four ordinary TPE pads, NOT printed')
    ax.text(-55,-37,'Pad centres x=-31,+43; y=+/-14.5 mm\nPads dia10 x3; plate3; ankle-to-floor27 mm*',fontsize=8)
    ax=axes[1,1]
    layers=[(0,1.6,'nut'),(1.6,.3,'washer'),(1.9,1.4,'ear*'),(3.3,3,'PETG'),(6.3,.3,'washer'),(6.6,1.6,'head')]
    for start,width,label in layers:
        ax.add_patch(Rectangle((start,-2),width,4,fill=label=='PETG',color='#1565a8' if label=='PETG' else '#555555',alpha=.5))
        ax.text(start+width/2,3.5,label,rotation=45,ha='left',fontsize=8)
    dimension(ax,(-1.4,-4),(6.6,-4),'8 mm under head')
    ax.set(xlim=(-3,11),ylim=(-8,12),title='M2x8 stack example (not an actual ear measurement)')
    ax.text(-2.8,-7.5,'Ear1.4 mm*; washers0.3; nutSW4 x1.6\n~1.4 mm projection only IF assumed stack fits',fontsize=8)
    for ax in axes.flat:ax.set_aspect('equal');ax.axis('off')
    fig.suptitle(f"{spec['revision']} | mm | QUOTATION / FIT SAMPLE ONLY - NOT MANUFACTURING APPROVAL",fontsize=12)
    fig.tight_layout(rect=(0,0,1,.95))
    fig.savefig(folder/'interfaces.svg');fig.savefig(folder/'interfaces.png',dpi=160);plt.close(fig)


def part_drawings(folder,spec):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    for row in json.loads((ROOT/'cad/print_manifest.json').read_text())['parts']:
        name=row['part'];m=trimesh.load_mesh(ROOT/'cad/stl'/f'{name}.stl')
        fig,axes=plt.subplots(1,3,figsize=(12,4))
        for ax,(a,b,title) in zip(axes,[(0,2,'front x-z'),(1,2,'side y-z'),(0,1,'top x-y')]):
            # Mesh outlines projected from source geometry, not an unrelated sketch.
            edges=m.vertices[m.edges_unique];ax.plot(edges[:,:,a].T,edges[:,:,b].T,lw=.18,color='#1565a8')
            lo,hi=m.bounds[:,[a,b]]
            ax.set_aspect('equal');ax.set_title(title,fontsize=9);ax.set_xlabel('mm');ax.grid(alpha=.2)
            ax.text(.02,.02,f"bounds{hi[0]-lo[0]:.2f} x{hi[1]-lo[1]:.2f} mm",transform=ax.transAxes,fontsize=8)
        fig.suptitle(f'{name} | qty1 | PETG | {spec["revision"]} | provisional, source hash in manifest')
        fig.tight_layout();fig.savefig(folder/f'{name}.svg');plt.close(fig)


def write_fasteners(folder):
    rows=[['Servo case ears',12,'M2x8 P010265','source dimensions; stack/length provisional'],
          ['Ear nuts',12,'M2 DIN934 P003474','SW4 x1.6mm'],
          ['Ear washers',24,'DIN125 P004198','2.2 x5 x0.3mm'],
          ['Factory horns',6,'Exact Waveshare15024 accessories','spline/shape/hole pattern UNKNOWN'],
          ['Shaft retainers',6,'Factory matching screws','thread/length UNKNOWN; NOT assumed M2'],
          ['Horn-to-frame screws',12,'Match factory horns and3mm plate','thread/diameter/length UNKNOWN'],
          ['Horn-to-frame washers',12,'Match horn screws','dimensions UNKNOWN'],
          ['Board ties',6,'100 x2.5mm ties','do not pinch pins; measured routing pending'],
          ['Tether/harness ties',12,'100 x2.5mm ties','service loops/strain relief; review routing']]
    with (folder/'fasteners.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['purpose','installed_quantity','item','fit_state']);w.writerows(rows)


def build():
    spec=json.loads((ROOT/'physical_spec.json').read_text());base=ROOT/'cad/print_order';base.mkdir(parents=True,exist_ok=True)
    plates=prepare_plates();draw=base/'drawings';draw.mkdir(exist_ok=True)
    interface_drawing(draw,spec);part_drawings(draw,spec);write_fasteners(base)
    # Matplotlib's SVG path lines include trailing spaces; normalize before hashes.
    for drawing in draw.glob('*.svg'):
        drawing.write_text('\n'.join(line.rstrip() for line in drawing.read_text().splitlines())+'\n')
    full=base/'frame';sample=base/'sample';full.mkdir(exist_ok=True);sample.mkdir(exist_ok=True)
    files=[]
    for part in plates['parts']:
        target=full/(part['part']+'.stl');shutil.copy2(ROOT/'cad/local_print'/part['file'],target)
        source=trimesh.load_mesh(ROOT/'cad/stl'/(part['part']+'.stl'))
        rotation=trimesh.transformations.euler_matrix(*np.deg2rad(part['rotation_deg']))
        source.apply_transform(rotation)
        transform=rotation.copy();transform[:3,3]=np.array([5,5,0])-source.bounds[0]
        files.append({'file':'frame/'+target.name,'quantity':1,'sha256':sha(target),'source_sha256':part['source_sha256'],'rotation_deg':part['rotation_deg'],
                      'source_coordinate_frame':part['part'],'export_coordinate_frame':'print_bed',
                      'body_to_print_bed_transform_mm':transform.tolist(),'bounds_mm':part['bounds_mm']})
    for name,shape in [('ear_cradle',cradle()),('horn_plate',horn_plate())]:
        target=sample/(name+'.stl');place(mesh(shape),(90,0,0)).export(target)
        files.append({'file':'sample/'+target.name,'quantity':1,'sha256':sha(target),'role':'fit sample only; not an eighth/ninth frame part'})
    # Optional service quotation input kept OUTSIDE both order ZIPs: alternatives must never be printed twice.
    layout=[('left_foot',[0,0]),('right_foot',[95,0]),('torso',[0,50]),('left_thigh',[94,50]),('right_thigh',[123,50]),('left_shin',[0,143]),('right_shin',[83,143])]
    batch=[]
    for name,pos in layout:
        piece=trimesh.load_mesh(full/f'{name}.stl');piece.apply_translation(-piece.bounds[0]+[*pos,0])
        for other in batch:
            if not (np.any(piece.bounds[1]<=other.bounds[0]) or np.any(other.bounds[1]<=piece.bounds[0])):
                raise ValueError('Quotation batch bounding boxes overlap; revise layout before upload')
        batch.append(piece)
    combined=trimesh.util.concatenate(batch)
    assert len(combined.split())==7
    combined.export(base/'QUOTE_ONLY_seven_components.stl')
    report={'revision':spec['revision'],'state':'QUOTATION PROTOTYPE / FIT SAMPLE; NOT RELEASED','manufacturing_approved':False,'units':'mm','scale_percent':100,'frame_parts':7,'sample_pieces':2,'files':files,'physical_spec_sha256':sha(ROOT/'physical_spec.json'),'source_cad_sha256':sha(ROOT/'cad/build_frame.py'),'quotation_batch_sha256':sha(base/'QUOTE_ONLY_seven_components.stl'),'quotation_batch_bounds_mm':combined.extents.tolist(),'print_settings':spec['manufacturing'],'source_date':spec['updated_date'],'unknown_interfaces':spec['manufacturing']['measurements_required'],'note':'Sample2pieces separately priced/shipped. Full order7pieces only. Combined file is an ALTERNATIVE quote input, not extra quantity. No TPU soles/filament/printer included.'}
    (base/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    for kind in ('sample','frame'):
        selected=[r for r in files if r['file'].startswith(kind+'/')]
        manifest={**report,'package':kind,'files':selected,'package_quantity':len(selected)}
        (base/f'{kind}_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        paths=[base/row['file'] for row in selected]+[base/f'{kind}_manifest.json',base/'fasteners.csv',base/'ORIENTATION_REVIEW.md',draw/'interfaces.svg',draw/'interfaces.png',ROOT/'cad/exploded.png',ROOT/'cad/ASSEMBLY.md',ROOT/'cad/QUOTE_REQUEST.md',ROOT/'physical_spec.json',ROOT/'cad/build_frame.py',ROOT/'build_model.py',ROOT/'robot_config.py',ROOT/'tools/prepare_print_order.py',ROOT/'tools/prepare_local_print.py',ROOT/'requirements.txt',ROOT/'requirements-dev.txt']
        if kind=='frame':paths += [draw/(row['part']+'.svg') for row in plates['parts']]
        manifest['package_contents_sha256']={str(path.relative_to(ROOT)):sha(path) for path in sorted(set(paths)) if path!=base/f'{kind}_manifest.json'}
        (base/f'{kind}_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        with zipfile.ZipFile(ROOT/'cad'/f'{kind}_quotation_package.zip','w',zipfile.ZIP_DEFLATED) as z:
            for path in sorted(set(paths)):z.write(path,str(path.relative_to(ROOT)))
    print('Prepared separate sample(2pieces) and frame(7pieces) quotation ZIPs; no release')
    return report


if __name__=='__main__':build()
