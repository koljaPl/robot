"""Check the geometry-derived open-loop probes without changing the RL interface."""
import numpy as np
import pytest

from humanoid_env import HumanoidEnv
from robot_config import HOME, JOINT_LOW, JOINT_HIGH, CONTROL_DT, target_to_action
from tools.analyze_support import anchor_pose
from tools.stance_transfer import PROFILES, matched_roll, mirror_targets, target_at


def test_all_declared_profiles_are_safe_continuous_and_mirrored():
    for profile in PROFILES:
        np.testing.assert_array_equal(target_at(0, profile), HOME)
        np.testing.assert_array_equal(target_at(30, profile), HOME)
        for time in np.linspace(0, 30, 1501):
            q = target_at(time, profile)
            assert np.all(q >= JOINT_LOW-1e-12) and np.all(q <= JOINT_HIGH+1e-12)
            np.testing.assert_allclose(mirror_targets(mirror_targets(q)), q, atol=1e-14)
        for time in (2, 6, 8, 9, 10, 11, 12, 16):
            assert max(abs(target_at(time+1e-6, profile)-target_at(time-1e-6, profile))) < 1e-5
        for local in (1, 3, 5, 7, 9, 11, 13):
            np.testing.assert_allclose(target_at(16+local, profile), mirror_targets(target_at(2+local, profile)), atol=1e-14)
    with pytest.raises(ValueError):
        target_at(-1, PROFILES[0])
    with pytest.raises(ValueError):
        target_at(0, 'unknown')


def test_geometric_preparation_levels_both_pad_planes_in_forward_kinematics():
    env = HumanoidEnv()
    try:
        assert matched_roll(np.deg2rad(10), np.deg2rad(10)) == pytest.approx(0)
        for profile in ('geometric40', 'geometric50'):
            for time in np.linspace(2, 6, 17):
                q = target_at(time, profile)
                assert q[0]+q[1] == pytest.approx(q[3]+q[4], abs=1e-14)
                anchor_pose(env, q, 0)
                assert env._minimum_foot_height(1) == pytest.approx(0, abs=1e-12)
                for side in ('left', 'right'):
                    np.testing.assert_allclose(env.data.xmat[env.model.body(side+'_foot').id].reshape(3, 3), np.eye(3), atol=1e-12)
    finally:
        env.close()


def test_privileged_gait_trace_does_not_change_dynamics_observations_or_metrics():
    from tools.audit_transfer import GaitTrace
    plain, traced = HumanoidEnv(), HumanoidEnv()
    try:
        plain.reset(seed=42); traced.reset(seed=42)
        trace = GaitTrace(traced)
        for step in range(450):
            action = target_to_action(target_at(step*CONTROL_DT, 'geometric50_swap'))
            a, b = plain.step(action), traced.step(action)
            np.testing.assert_array_equal(a[0], b[0])
            np.testing.assert_array_equal(plain.data.qpos, traced.data.qpos)
            assert a[1:] == b[1:]
        assert len(trace.rows) == 4500
    finally:
        plain.close(); traced.close()


def test_independent_raw_audit_rejects_unqualified_events():
    from copy import deepcopy
    from tools.report_transfer import raw_step_check
    rows=[]
    for index in range(5):
        rows.append({'time_s':str(index*.02),'left_x_m':str(.01 if index==4 else 0),
                     'left_y_m':'0','right_x_m':'0','right_y_m':'0',
                     'left_contact':str(index in (0,4)),'right_contact':'True',
                     'left_supported':str(index in (0,4)),'right_supported':'True',
                     'left_height_m':str(.004 if index in (1,2,3) else 0)})
    event={'foot':'left','time_s':.08}
    assert raw_step_check(rows,event,.02)['passes_existing_single_step_thresholds']
    unsupported=deepcopy(rows);unsupported[2]['right_supported']='False'
    slipped=deepcopy(rows);slipped[2]['right_x_m']='.004'
    too_brief=deepcopy(rows);too_brief[1]['left_height_m']='0';too_brief[3]['left_height_m']='0'
    for bad in (unsupported,slipped,too_brief):
        assert not raw_step_check(bad,event,.02)['passes_existing_single_step_thresholds']
