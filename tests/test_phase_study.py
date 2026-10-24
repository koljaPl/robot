"""Keep phase probes safe, reproducible and separate from the fixed plant."""
import numpy as np
import pytest

from robot_config import HOME, JOINT_LOW, JOINT_HIGH, TARGET_SPEED, CONTROL_DT
from tools.stance_transfer import target_at, mirror_targets
from tools.phase_study import CASES, duration, study_target


def test_phase_study_baseline_exactly_preserves_existing_commands():
    for t in np.arange(1500)*CONTROL_DT:
        np.testing.assert_array_equal(study_target(t,'baseline'),target_at(t,'geometric50_swap'))
    # The settling probe only inserts HOME; later commands retain their original
    # timebase. It does not reset actuator history, pose or velocity internally.
    for t in np.arange(800)*CONTROL_DT:
        np.testing.assert_array_equal(study_target(t,'settle2'),study_target(t,'baseline'))
    for t in np.arange(16,18,CONTROL_DT):
        np.testing.assert_allclose(study_target(t,'settle2'),HOME,atol=1e-14)
    for t in np.arange(18,32,CONTROL_DT):
        np.testing.assert_array_equal(study_target(t,'settle2'),target_at(t-2,'geometric50_swap'))


def test_declared_phase_probes_respect_limits_speed_and_mirroring():
    for case in CASES:
        commands=np.array([study_target(t,case) for t in np.arange(0,duration(case)+CONTROL_DT/2,CONTROL_DT)])
        assert np.all(commands>=JOINT_LOW-1e-12) and np.all(commands<=JOINT_HIGH+1e-12)
        assert np.max(np.abs(np.diff(commands,axis=0)))/CONTROL_DT <= TARGET_SPEED
        np.testing.assert_allclose(commands[[0,-1]],np.array([HOME,HOME]),atol=1e-14)
        for t in (0,2,6,8.4,10,16,24.2,duration(case)):
            np.testing.assert_array_equal(study_target(t,case,'right'),mirror_targets(study_target(t,case)))
    with pytest.raises(ValueError):study_target(np.nan,'baseline')
    with pytest.raises(ValueError):study_target(0,'unknown')


def test_home_hold_does_not_erase_estimated_command_deadband_history():
    from robot_config import action_to_target,SERVO_DEADBAND,ESTIMATED_US_PER_RAD
    from servo_control import ServoTargets
    servo=ServoTargets();initial=servo.quantize(HOME)
    for t in np.arange(0,18,CONTROL_DT):
        target=study_target(t,'settle2')
        # Follow the same normalized-action roundtrip as HumanoidEnv.
        from robot_config import target_to_action
        servo.enqueue(t,action_to_target(target_to_action(target)))
        applied=servo.advance(t,CONTROL_DT)
        if abs(t-16)<1e-8:before_hold=applied.copy()
    np.testing.assert_array_equal(applied,before_hold)
    assert np.max(abs(applied-initial)) > np.deg2rad(.1)
    assert np.max(abs(applied-HOME)) <= SERVO_DEADBAND+1/ESTIMATED_US_PER_RAD


def test_handoff_commands_are_safe_continuous_mirrored_and_hold_the_last_pose():
    from tools.handoff_probe import PROFILES,target_at as handoff_target
    for profile in PROFILES:
        q=np.array([handoff_target(t,profile) for t in np.arange(0,30+CONTROL_DT/2,CONTROL_DT)])
        assert np.all(q>=JOINT_LOW-1e-12) and np.all(q<=JOINT_HIGH+1e-12)
        assert np.max(abs(np.diff(q,axis=0)))/CONTROL_DT <= TARGET_SPEED
        np.testing.assert_array_equal(q[0],HOME)
        np.testing.assert_array_equal(q[-1],handoff_target(29,profile))
        assert not np.allclose(q[-1],HOME)  # final support hold, not a neutral reset
        for t in (2,6,10,16,22,26,30):
            np.testing.assert_allclose(handoff_target(t,profile,'right'),mirror_targets(handoff_target(t,profile)),atol=1e-14)
        for boundary in (2,10,18,26) if profile=='slow' else (2,8,14,20,26):
            assert max(abs(handoff_target(boundary+1e-6,profile)-handoff_target(boundary-1e-6,profile)))<1e-5
