"""Calibration error affects the shaft equilibrium, not the bounded command."""
import mujoco
import numpy as np

from humanoid_env import HumanoidEnv
from robot_config import HOME, JOINT_LOW, JOINT_HIGH, target_to_action


def test_outward_offsets_produce_force_at_each_command_bound_without_fake_stops():
    env=HumanoidEnv()
    try:
        env.reset(seed=42)
        np.testing.assert_array_equal(env.model.actuator_gear[env.aids,0],1)
        np.testing.assert_array_equal(env.model.actuator_gear[env.aids,1:],0)
        for joint in range(6):
            assert not env.model.jnt_limited[env.model.joint(('left_hip','left_knee','left_ankle','right_hip','right_knee','right_ankle')[joint]).id]
            for sign,bound in ((-1,JOINT_LOW[joint]),(1,JOINT_HIGH[joint])):
                mujoco.mj_resetDataKeyframe(env.model,env.data,env.model.key('home').id)
                env.data.qpos[2]+=.3;env.data.qvel[:]=0
                env.offset[:]=0;env.offset[joint]=sign*np.deg2rad(1)
                env._apply_joint_offsets()
                env.data.qpos[env.qadr[joint]]=bound
                env.data.ctrl[env.aids]=HOME;env.data.ctrl[env.aids[joint]]=bound
                env._motor_envelope();mujoco.mj_forward(env.model,env.data)
                expected=env.model.actuator_gainprm[env.aids[joint],0]*env.offset[joint]
                assert np.isclose(env.data.actuator_force[env.aids[joint]],expected,atol=1e-12)
                assert env.data.ctrl[env.aids[joint]]==bound
    finally:env.close()


def test_bias_is_restored_on_every_reset_without_offset_accumulation():
    env=HumanoidEnv(domain_randomization=True)
    try:
        env.reset(seed=7);offset=env.offset.copy();bias=env.model.actuator_biasprm.copy()
        env.reset(seed=7)
        np.testing.assert_array_equal(env.offset,offset)
        np.testing.assert_array_equal(env.model.actuator_biasprm,bias)
        env._apply_joint_offsets();np.testing.assert_array_equal(env.model.actuator_biasprm,bias)
        env.domain_randomization=False;env.reset(seed=7)
        np.testing.assert_array_equal(env.offset,0)
        np.testing.assert_array_equal(env.model.actuator_biasprm,env.nominal['actuator_biasprm'])
    finally:env.close()


def test_unknown_shaft_offset_does_not_expand_acknowledged_command_bounds():
    env=HumanoidEnv()
    try:
        env.reset(seed=42);env.offset[:]=np.deg2rad(1);env._apply_joint_offsets()
        for _ in range(50):
            env.step(target_to_action(JOINT_HIGH))
            assert np.all(env.applied_command<=JOINT_HIGH)
            assert np.all(env.data.ctrl[env.aids]<=env.model.actuator_ctrlrange[env.aids,1])
            if env.done:break
        np.testing.assert_allclose(env.model.actuator_biasprm[env.aids,0],env.model.actuator_gainprm[env.aids,0]*env.offset)
    finally:env.close()
