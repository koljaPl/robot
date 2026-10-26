"""Synthetic response diagnostics; no measured robot/calibration evidence."""
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np
import pytest

from tools import review_responses as response
from tools import validate_measurement as intake
from tools.make_response_demo import create

REAL_PLOT = response.plot_trial


@pytest.fixture
def inputs(tmp_path, monkeypatch):
    folder = tmp_path/'inputs';create(folder)
    def stub_plot(values,prediction,uncertainty,role,kind,path):
        path.write_bytes(b'SYNTHETIC UNIT-TEST PLOT STUB; not a PNG')
    monkeypatch.setattr(response,'plot_trial',stub_plot)
    return folder


def test_default_intake_matches_historical_result_and_no_fit_does_not_call_fitter(inputs,monkeypatch):
    legacy = Path(__file__).resolve().parents[1]/'docs/history/2026-10-26/pre_response_review/tools/validate_measurement.py'
    spec=importlib.util.spec_from_file_location('response_review_legacy_intake',legacy)
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    args=(inputs/'fit.csv',inputs/'fit.json')
    assert intake.validate_trial(*args)==old.validate_trial(*args)
    def forbidden(*args):raise AssertionError('Validation data fitted')
    monkeypatch.setattr(intake,'fit',forbidden)
    result=intake.validate_trial(*args,perform_fit=False)
    assert result['first_order_fit'] is None and not result['fit_performed']
    assert len(result['skipped_fit_screens'])==3 and not result['physically_verified']


def test_fit_once_and_validate_without_refit(inputs,tmp_path,monkeypatch):
    calls=[];original=intake.fit
    def observed(data):calls.append(data.copy());return original(data)
    monkeypatch.setattr(intake,'fit',observed)
    r=response.review(inputs/'review.json',tmp_path/'report')
    assert len(calls)==1 and calls[0]['angle_rad'][0]==pytest.approx(.04)
    assert r['state']=='diagnostic_awaiting_human_review'
    assert not r['validation_parameters_refitted'] and not r['calibration_validated'] and not r['model_updated']
    assert r['data_kind']=='synthetic' and not r['physically_verified'] and not r['trial_independence_verified']
    assert all(t['intake']['first_order_fit'] is None for t in r['trials'][1:])
    matching,mismatched=r['trials'][1:]
    assert matching['baseline']['command_step_rad']<0
    assert matching['metrics']['rmse_deg']<.05
    assert mismatched['metrics']['rmse_deg']>1
    assert mismatched['conditions']['load_range_nm']['differs_from_fit']
    assert mismatched['conditions']['voltage_range_v']['differs_from_fit']
    assert not matching['conditions']['voltage_range_v']['differs_from_fit']
    assert len(r['shared_evidence_files'])==1


def test_validation_post_step_changes_cannot_change_fit_or_predictions(inputs,tmp_path):
    first=response.review(inputs/'review.json',tmp_path/'first')
    csv_path=inputs/'matching.csv'
    rows=list(csv.DictReader(csv_path.open()))
    for row in rows:
        if float(row['time_s'])>=.2:row['angle_rad']=str(-float(row['angle_rad'])+.5)
    with csv_path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=intake.COLUMNS);w.writeheader();w.writerows(rows)
    second=response.review(inputs/'review.json',tmp_path/'second')
    assert first['fit_parameters']==second['fit_parameters']
    assert first['trials'][1]['baseline']==second['trials'][1]['baseline']
    assert first['trials'][1]['metrics']!=second['trials'][1]['metrics']
    a=np.genfromtxt(tmp_path/'first/validation_01_prediction.csv',delimiter=',',names=True)
    b=np.genfromtxt(tmp_path/'second/validation_01_prediction.csv',delimiter=',',names=True)
    np.testing.assert_array_equal(a['predicted_angle_rad'],b['predicted_angle_rad'])


@pytest.mark.parametrize('problem',['version','missing_validation','malformed_trial','duplicate_fit',
                                   'duplicate_validation','copied_duplicate','reformatted_duplicate',
                                   'changed_conditions_duplicate','wrong_servo','wrong_joint',
                                   'mixed_kind','bad_units','missing_evidence','command_angles','nonfinite','bad_provenance'])
def test_invalid_inputs_refused_without_output(inputs,tmp_path,problem):
    manifest_path=inputs/'review.json';m=json.loads(manifest_path.read_text())
    meta_path=inputs/'matching.json';meta=json.loads(meta_path.read_text())
    if problem=='version':m['version']=True
    if problem=='missing_validation':m['validation_trials']=[]
    if problem=='malformed_trial':m['fit_trial']={'csv':1}
    if problem=='duplicate_fit':m['validation_trials'][0]=m['fit_trial'].copy()
    if problem=='duplicate_validation':m['validation_trials'].append(m['validation_trials'][0].copy())
    if problem=='copied_duplicate':shutil.copy2(inputs/'fit.csv',inputs/'matching.csv')
    if problem in ('reformatted_duplicate','changed_conditions_duplicate'):
        rows=list(csv.DictReader((inputs/'fit.csv').open()))
        with (inputs/'matching.csv').open('w',newline='') as f:
            w=csv.writer(f);w.writerow(intake.COLUMNS)
            for row in rows:
                if problem=='changed_conditions_duplicate':row['voltage_v']='4.95'
                w.writerow([f'{float(row[k]):.17e}' for k in intake.COLUMNS])
    if problem=='wrong_servo':meta['servo_id']='another servo'
    if problem=='wrong_joint':meta['joint_index']=1
    if problem=='mixed_kind':meta.update(data_kind='physical',angle_source='external_video')
    if problem=='bad_units':meta['units']={}
    if problem=='missing_evidence':meta['evidence_files']=['absent.mp4']
    if problem=='command_angles':meta['angle_source']='acknowledged_commands'
    if problem=='nonfinite':
        p=inputs/'matching.csv';p.write_text(p.read_text().replace('0.005,','nan,',1))
    meta_path.write_text(json.dumps([] if problem=='bad_provenance' else meta))
    manifest_path.write_text(json.dumps(m))
    output=tmp_path/'refused'
    with pytest.raises((ValueError,FileNotFoundError)):response.review(manifest_path,output)
    assert not output.exists()


def test_existing_report_and_demo_never_overwritten(inputs,tmp_path):
    output=tmp_path/'old';output.mkdir();(output/'report.json').write_text('preserve')
    with pytest.raises(FileExistsError):response.review(inputs/'review.json',output)
    assert (output/'report.json').read_text()=='preserve'
    with pytest.raises(FileExistsError):create(inputs)


def test_claimed_physical_metadata_is_not_promoted_to_verified(inputs,tmp_path):
    for name in ('fit','matching','mismatched'):
        p=inputs/(name+'.json');m=json.loads(p.read_text())
        m.update(data_kind='physical',angle_source='external_video')
        p.write_text(json.dumps(m))
    r=response.review(inputs/'review.json',tmp_path/'physical_label_only')
    assert r['data_kind']=='physical' and not r['physically_verified'] and not r['calibration_validated']
    assert all(not t['intake']['physically_verified'] for t in r['trials'])


def test_actual_plots_predictions_metrics_and_hashes(inputs,tmp_path,monkeypatch):
    monkeypatch.setattr(response,'plot_trial',REAL_PLOT)
    out=tmp_path/'plots';r=response.review(inputs/'review.json',out)
    from PIL import Image
    for trial in r['trials']:
        with Image.open(out/trial['plot_png']) as im:
            assert im.format=='PNG' and im.width>=1000 and im.height>=700
        data=np.genfromtxt(out/trial['prediction_csv'],delimiter=',',names=True)
        np.testing.assert_allclose(data['residual_rad'],data['measured_angle_rad']-data['predicted_angle_rad'])
        assert np.rad2deg(np.sqrt(np.mean(data['residual_rad']**2)))==pytest.approx(trial['metrics']['rmse_deg'])
    for name,digest in r['artifact_sha256'].items():assert intake.sha(out/name)==digest
    assert 'awaiting human review' in (out/'report.md').read_text()


def test_output_failure_keeps_failed_diagnostic_not_approval(inputs,tmp_path,monkeypatch):
    def fail(*args):raise OSError('Synthetic plot failure')
    monkeypatch.setattr(response,'plot_trial',fail)
    out=tmp_path/'failed'
    with pytest.raises(OSError):response.review(inputs/'review.json',out)
    m=json.loads((out/'failure.json').read_text())
    assert not m['physically_verified'] and not m['calibration_validated'] and not (out/'report.json').exists()


def test_no_fit_cli_explicitly_omits_fitting(inputs,tmp_path):
    output=tmp_path/'no_fit.json'
    proc=subprocess.run([sys.executable,str(intake.ROOT/'tools/validate_measurement.py'),str(inputs/'matching.csv'),
                         '--metadata',str(inputs/'matching.json'),'--output',str(output),'--no-fit'],
                        text=True,capture_output=True)
    assert proc.returncode==0,proc.stderr
    data=json.loads(output.read_text())
    assert data['first_order_fit'] is None and not data['fit_performed'] and not data['calibration_validated']
