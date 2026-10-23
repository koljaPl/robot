"""Replay an archived policy under its exact recorded source, in an isolated temp tree.

This does not migrate, approve or deploy it under the current firmware identity.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive',type=Path,default=ROOT/'docs/validation/2026-10-23');p.add_argument('--model',type=Path,default=Path('pilot_A0/best_model.zip'));p.add_argument('--episodes',type=int,default=5);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    archive=a.archive.resolve();model=archive/a.model
    if not model.resolve().is_relative_to(archive):p.error('Model must be inside the archive')
    manifest=json.loads((archive/'manifest.json').read_text())
    for name,expected in manifest['sha256'].items():
        file=archive/name
        if not file.resolve().is_relative_to(archive) or hashlib.sha256(file.read_bytes()).hexdigest()!=expected:raise ValueError('Archive hash mismatch: '+name)
    a.output=a.output.resolve()
    with tempfile.TemporaryDirectory(prefix='s6-historical-') as tmp:
        tmp=Path(tmp);shutil.copytree(archive/'source',tmp,dirs_exist_ok=True)
        # Visual CAD only; dynamics/collisions/inertias are explicit archived MJCF.
        if not (tmp/'cad/stl').exists():
            shutil.copytree(ROOT/'cad/stl',tmp/'cad/stl')
        subprocess.run([sys.executable,str(tmp/'evaluate.py'),'--model',str(model),'--episodes',str(a.episodes),'--seed','2000','--output',str(a.output)],cwd=tmp,check=True)

if __name__=='__main__':main()
