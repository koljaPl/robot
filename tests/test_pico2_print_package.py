import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

import pytest

from calibration import configuration_identity
from robot_config import ROOT
from tools.prepare_classmate_print import create


def test_classmate_files_are_exactly_seven_frames_and_two_samples(tmp_path):
    out = tmp_path/'print'
    r = create(out)
    samples = [p for p in r['files'] if p['file'].startswith('01_')]
    frames = [p for p in r['files'] if p['file'].startswith('02_')]
    assert len(samples) == 2 and len(frames) == 7
    assert {Path(f['file']).stem for f in frames} == {'torso','left_thigh','right_thigh','left_shin','right_shin','left_foot','right_foot'}
    assert all(f['quantity'] == 1 and f['units'] == 'mm' and f['connected_parts'] == 1 for f in r['files'])
    for f in r['files']:
        assert hashlib.sha256((out/f['file']).read_bytes()).hexdigest() == f['sha256']
    with zipfile.ZipFile(out.with_suffix('.zip')) as z:
        assert len([s for s in z.namelist() if s.endswith('.stl')]) == 9
        assert not any('QUOTE_ONLY' in s or '/sole' in s for s in z.namelist())
    assert not r['physical_fit_verified'] and r['price_eur'] is None
    with pytest.raises(ValueError, match='new folder'): create(out)


def test_user_acceptance_is_not_relabelled_as_budget_or_physical_evidence():
    d = json.loads((ROOT/'docs/decisions/2026-10-26-printing-pico2.json').read_text())
    assert d['research_phase_complete'] and not d['budget_numerically_verified']
    assert d['price_eur'] is None and not d['physical_fit_verified'] and not d['printer_purchase']
    spec = json.loads((ROOT/'physical_spec.json').read_text())
    assert spec['controller']['sdk_board'] == 'pico2'
    c = next(c for c in spec['bodies'][0]['components'] if c['name'] == 'pico')
    assert c['parameter_evidence']['mass']['state'] == 'estimated'
    assert 'firmware/CMakeLists.txt' in configuration_identity()['files']


def test_wrong_board_target_fails_before_sdk_lookup(tmp_path):
    cmake = shutil.which('cmake') or str(ROOT/'.venv/bin/cmake')
    result = subprocess.run([cmake,'-S',str(ROOT/'firmware'),'-B',str(tmp_path/'build'),'-DPICO_BOARD=pico'],capture_output=True,text=True)
    assert result.returncode and 'targets Pico 2' in result.stderr
