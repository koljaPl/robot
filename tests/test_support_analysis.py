"""Engineering diagnostics use privileged state only offline, outside the policy."""
import numpy as np
import pytest

from humanoid_env import HumanoidEnv
from robot_config import HOME, JOINT_HIGH
from tools.analyze_support import (anchor_pose, centre_of_mass, convex_hull,
                                   gravity_torques, level_pad_polygon, support_margin)


def test_support_margin_sign_and_degenerate_contacts():
    square = [[1, 1], [-1, 1], [0, 0], [-1, -1], [1, -1], [1, 1]]
    assert len(convex_hull(square)) == 4
    assert support_margin([0, 0], square) == pytest.approx(1)
    assert support_margin([2, 0], square) == pytest.approx(-1)
    assert support_margin([1, .4], square) == pytest.approx(0)
    assert support_margin([0, 0], [[0, 0], [1, 0], [2, 0]]) is None


def test_both_anchored_feet_are_level_and_zero_height_with_outside_home_com():
    env = HumanoidEnv()
    try:
        margins = []
        for stance in (0, 1):
            anchor_pose(env, HOME, stance)
            np.testing.assert_allclose(env.data.site_xpos[env.foot_center_sites[stance]], 0, atol=1e-14)
            assert env._minimum_foot_height(stance) == pytest.approx(0, abs=1e-14)
            assert env._minimum_foot_height(1 - stance) == pytest.approx(0, abs=1e-14)
            polygon = level_pad_polygon(env, stance)
            # Four10mm pads centred at +/-14.5mm: lateral support +/-19.5mm.
            np.testing.assert_allclose([polygon[:, 1].min(), polygon[:, 1].max()], [-.0195, .0195], atol=1e-12)
            margins.append(support_margin(centre_of_mass(env)[:2], polygon))
        assert max(margins) < -.01  # both-foot HOME is not a quiet single-support pose
        bad = HOME.copy(); bad[0] = JOINT_HIGH[0] + .01
        with pytest.raises(ValueError):
            anchor_pose(env, bad, 0)
    finally:
        env.close()


def test_virtual_work_torque_matches_previous_home_estimate_and_preserves_pose():
    env = HumanoidEnv()
    try:
        anchor_pose(env, HOME, 0)
        qpos = env.data.qpos.copy()
        torque = gravity_torques(env, HOME.copy(), 0)
        assert max(abs(torque)) == pytest.approx(.065725, abs=2e-5)
        np.testing.assert_allclose(env.data.qpos, qpos, atol=1e-14)
        np.testing.assert_allclose(torque, gravity_torques(env, HOME.copy(), 0, delta=2e-5), atol=1e-8)
    finally:
        env.close()


def test_transition_probes_start_end_home_remain_safe_and_are_symmetric():
    from robot_config import JOINT_LOW
    from tools.transfer_reference import keyframes, target_at
    for order in ('lean_first', 'shorten_first'):
        frames = keyframes(order)
        assert [t for t, _ in frames] == sorted(set(t for t, _ in frames))
        np.testing.assert_array_equal(target_at(0, order), HOME)
        np.testing.assert_allclose(target_at(22, order), HOME, atol=1e-14, rtol=0)
        for t in np.linspace(0, 22, 2201):
            target = target_at(t, order)
            assert np.all(target >= JOINT_LOW) and np.all(target <= JOINT_HIGH)
        left, right = target_at(6, order), target_at(16, order)
        swapped = left[[3, 4, 5, 0, 1, 2]].copy(); swapped[[2, 5]] *= -1
        np.testing.assert_allclose(right, swapped, atol=1e-14)
