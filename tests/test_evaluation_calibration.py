import json
from pathlib import Path
import sys

import numpy as np
import pytest

import evaluate as evaluation
from calibration import configuration_identity
from humanoid_env import HumanoidEnv
from robot_config import ROOT
from servo_control import ServoTargets


def calibration_fixture(tmp_path):
    c = json.loads((ROOT/'calibrations/example.invalid.json').read_text())
    c.update(state='measured', validated=True, evidence='SYNTHETIC TEST ONLY')
    c['us_per_rad'] = [510., 520., 480., 499., 501., 503.]
    p = tmp_path/'calibration.json'; p.write_text(json.dumps(c))
    return p, c


@pytest.mark.parametrize('baseline', ['home', 'untrained'])
def test_baseline_uses_effective_calibration_and_reports_identity(tmp_path, monkeypatch, baseline):
    path, c = calibration_fixture(tmp_path); seen = []
    class RecordingEnv(HumanoidEnv):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs); seen.append(kwargs['calibration'])
        def reset(self, **kwargs):
            result = super().reset(**kwargs)
            expected = ServoTargets(calibration=c)
            probe = np.full(6, .123)
            np.testing.assert_allclose(self.servos.quantize(probe), expected.quantize(probe))
            assert not np.array_equal(expected.quantize(probe), ServoTargets().quantize(probe))
            assert self.calibration == c
            return result
    monkeypatch.setattr(evaluation, 'HumanoidEnv', RecordingEnv)
    r = evaluation.evaluate(episodes=1, seed=2000, baseline=baseline, episode_seconds=.04,
                            output=tmp_path/baseline, calibration_path=path)
    assert seen == [c]
    assert r['identity'] == configuration_identity(c)
    assert r['calibration_record'] == c and r['calibration_source'] == 'explicit_file'


def test_model_and_explicit_calibration_mismatch_rejected_before_environment(tmp_path, monkeypatch):
    import hashlib
    path, c = calibration_fixture(tmp_path)
    model = tmp_path/'fake.zip'; model.write_bytes(b'not a model; mismatch must precede load')
    identity = configuration_identity(c); identity['calibration'] = 'wrong'
    model.with_suffix('.manifest.json').write_text(json.dumps({
        'model_sha256': hashlib.sha256(model.read_bytes()).hexdigest(), 'identity': identity,
        'calibration_record': c}))
    def forbidden(*args, **kwargs): raise AssertionError('Mismatch created environment')
    monkeypatch.setattr(evaluation, 'HumanoidEnv', forbidden)
    with pytest.raises(ValueError, match='calibration fingerprint'):
        evaluation.evaluate(model_path=model, output=tmp_path/'rejected', calibration_path=path)
    assert not (tmp_path/'rejected').exists()


def test_embedded_calibration_cannot_disagree_with_policy_manifest(tmp_path, monkeypatch):
    import hashlib
    _, c = calibration_fixture(tmp_path)
    model = tmp_path/'fake.zip'; model.write_bytes(b'identity test, not PPO')
    model.with_suffix('.manifest.json').write_text(json.dumps({
        'model_sha256': hashlib.sha256(model.read_bytes()).hexdigest(),
        'identity': configuration_identity(), 'calibration_record': c}))
    with pytest.raises(ValueError, match='calibration record/identity'):
        evaluation.evaluate(model_path=model, output=tmp_path/'rejected')


@pytest.mark.parametrize('explicit', [False, True])
def test_policy_evaluation_uses_same_calibration_as_baselines(tmp_path, monkeypatch, explicit):
    import hashlib
    from stable_baselines3 import PPO
    from robot_config import HOME, target_to_action
    path, c = calibration_fixture(tmp_path)
    model = tmp_path/'fake.zip'; model.write_bytes(b'unit-test policy stub, never trained')
    model.with_suffix('.manifest.json').write_text(json.dumps({
        'model_sha256': hashlib.sha256(model.read_bytes()).hexdigest(),
        'identity': configuration_identity(c), 'calibration_record': c}))
    class Policy:
        def predict(self, *args, **kwargs): return target_to_action(HOME), None
    monkeypatch.setattr(PPO, 'load', lambda *a, **k: Policy())
    r = evaluation.evaluate(model_path=model, episodes=1, seed=2000, episode_seconds=.04,
                            calibration_path=path if explicit else None, output=tmp_path/'policy')
    assert r['identity'] == configuration_identity(c) and r['calibration_record'] == c
    assert r['calibration_source'] == ('explicit_file' if explicit else 'policy_manifest')


def test_formal_orchestrator_passes_calibration_to_all_evaluations(tmp_path, monkeypatch):
    from tools import experiments
    # Mock orchestration only: do not train, evaluate final seeds or clear real gates.
    fake_root = tmp_path/'fake_project'; (fake_root/'docs').mkdir(parents=True)
    (fake_root/'docs/gates.json').write_text(json.dumps({'mock_gate': True}))
    commands = []
    def fake_run(cmd, **kwargs):
        commands.append(cmd)
        if Path(cmd[1]).name == 'train.py':
            output = Path(cmd[cmd.index('--output')+1]); output.mkdir(parents=True)
            (output/'training_config.json').write_text(json.dumps({'initial_policy_sha256': 'same-paired-test-weights'}))
    monkeypatch.setattr(experiments, 'ROOT', fake_root)
    monkeypatch.setattr(experiments.subprocess, 'run', fake_run)
    monkeypatch.setattr(sys, 'argv', ['experiments', '--calibration', 'TEST_ONLY.json', '--steps', '1024', '--output', str(tmp_path/'formal_mock')])
    experiments.main()
    calls = [c for c in commands if Path(c[1]).name == 'evaluate.py']
    assert len(calls) == 20  #12trained +2HOME +6untrained, each call10episodes
    assert all(c[c.index('--calibration')+1] == 'TEST_ONLY.json' for c in calls)
