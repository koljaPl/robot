"""Record degenerate-intersection warnings; fail on non-finite volumes."""
import json
from pathlib import Path
import runpy
import sys
import warnings
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
output=Path(__file__).resolve().parent
original=trimesh.boolean.intersection
record=[]

def checked_intersection(*args,**kwargs):
    result=original(*args,**kwargs)
    if len(result.vertices):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always',RuntimeWarning)
            volume=float(result.volume)
        if not np.isfinite(volume):
            raise ValueError('Non-finite intersection volume; cannot claim clearance')
        if caught:
            record.append({'vertices':len(result.vertices),'volume_mm3':volume,
                           'warnings':[str(w.message) for w in caught]})
    return result

trimesh.boolean.intersection=checked_intersection
sys.argv=['tools/check_clearance.py','--output',str(output/'clearance_recheck.json')]
try:
    runpy.run_path(str(ROOT/'tools/check_clearance.py'),run_name='__main__')
except SystemExit as e:
    assert e.code==1  # unknown physical interfaces still block release
(output/'clearance_warnings.json').write_text(json.dumps({
    'state':'local numerical warning audit; no physical fit approval',
    'all_evaluated_intersection_volumes_finite':True,'warning_records':record,
    'interpretation':'Warnings arise from zero-volume intersection COM calculations; no non-finite volume is counted as clear.'},indent=2)+'\n')
print(json.dumps({'warning_intersections':len(record),'volumes_mm3':sorted(set(r['volume_mm3'] for r in record))}))
