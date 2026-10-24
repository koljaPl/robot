"""One-factor probes must not mutate the frozen plant or mix unrelated factors."""
import numpy as np

from robot_config import CONTROL_DT, DR, target_to_action
from tools.handoff_probe import target_at
from tools.sensitivity_probe import IsolatedEnv, variants, verify_frozen_sources


def test_declared_probe_scope_and_mass_inertia_restoration():
    cases=variants()
    assert len(cases)==29 and len({v.name for v in cases.values()})==29
    offsets=[v for v in cases.values() if v.family=='offset']
    assert len(offsets)==12 and {v.joint for v in offsets}==set(range(6))
    assert all(abs(v.value)==DR.offset_rad for v in offsets)
    nominal=IsolatedEnv(cases['nominal']);mass=IsolatedEnv(cases['mass_high'])
    try:
        nominal.reset(seed=42);mass.reset(seed=42)
        np.testing.assert_allclose(mass.model.body_mass,nominal.model.body_mass*(1+DR.mass))
        np.testing.assert_allclose(mass.model.body_inertia,nominal.model.body_inertia*(1+DR.mass))
        np.testing.assert_array_equal(mass.model.body_ipos,nominal.model.body_ipos)
        before_mass=mass.model.body_mass.copy();before_inertia=mass.model.body_inertia.copy()
        mass.model.body_mass[:]*=3;mass.model.body_inertia[:]*=3
        mass.reset(seed=42)
        np.testing.assert_array_equal(mass.model.body_mass,before_mass)
        np.testing.assert_array_equal(mass.model.body_inertia,before_inertia)
    finally:nominal.close();mass.close()


def test_every_family_changes_only_its_declared_runtime_fields():
    cases=variants();base=IsolatedEnv(cases['nominal'])
    try:
        base.reset(seed=42);expected=base.runtime_parameters
    finally:base.close()
    allowed={'mass':{'body_mass_kg','body_inertia_kg_m2'},'torso_mass':{'body_mass_kg','body_inertia_kg_m2'},
             'friction':{'geom_sliding_friction'},'strength':{'static_torque_envelope_Nm'},
             'shaft_speed':{'shaft_no_load_speed_rad_s'},'target_slew':{'target_slew_rad_s'},
             'damping':{'joint_damping'},'delay':{'command_delay_s'},
             'offset':{'joint_offsets_rad','actuator_bias_constant_Nm'},
             'imu_noise':{'imu_noise_scale'},'nominal':set()}
    for variant in cases.values():
        env=IsolatedEnv(variant)
        try:
            env.reset(seed=42)
            changed={k for k,v in env.runtime_parameters.items() if v!=expected[k]}
            assert changed==allowed[variant.family]
        finally:env.close()


def test_sensor_noise_changes_observations_without_changing_open_loop_motion():
    cases=variants();a=IsolatedEnv(cases['nominal']);b=IsolatedEnv(cases['imu_noise_high'])
    changed=False
    try:
        a.reset(seed=42);b.reset(seed=42)
        for step in range(150):
            action=target_to_action(target_at(step*CONTROL_DT,'compact'))
            x,y=a.step(action),b.step(action)
            np.testing.assert_array_equal(a.data.qpos,b.data.qpos)
            np.testing.assert_array_equal(a.data.qvel,b.data.qvel)
            changed |= not np.array_equal(x[0],y[0])
        assert changed
    finally:a.close();b.close()
    verify_frozen_sources()
