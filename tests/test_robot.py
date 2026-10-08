import json
import binascii
import numpy as np
import pytest
import mujoco
from stable_baselines3.common.env_checker import check_env
from humanoid_env import HumanoidEnv
from robot_config import ROOT, HOME, JOINT_LOW, JOINT_HIGH, CONTROL_DT, TARGET_SPEED, action_to_target, target_to_action
from servo_control import ServoTargets
from imu_observation import GravityEstimator
from hardware_interface import command_frame, decode_frame, encode_frame, telemetry_frame, calibrated_pulses
from build_model import physical_bodies, aggregate


def test_mass_and_joint_direction():
    spec = json.loads((ROOT / "physical_spec.json").read_text())
    bodies = physical_bodies(spec)
    components = [c for b in bodies for c in b["components"]]
    assert len([c for c in components if "servo" in c["name"]]) == 6
    assert len({c["name"] for c in components}) == len(components)
    m = mujoco.MjModel.from_xml_path(str(ROOT / "robot.xml"))
    assert m.nu == 6 and 0.15 < m.body_mass.sum() < 0.25
    assert m.body_mass.sum() == pytest.approx(sum(c["mass"] for c in components))
    d = mujoco.MjData(m)
    mujoco.mj_resetDataKeyframe(m, d, 0)
    mujoco.mj_forward(m, d)
    for side in ("left", "right"):
        for jname, body, axis in [(side + "_hip", side + "_thigh", 1), (side + "_knee", side + "_shin", 1), (side + "_ankle", side + "_foot", 0)]:
            # Rotation derivatives follow +Y/+X right-hand convention on both legs.
            j = m.joint(jname)
            assert np.allclose(j.axis, np.eye(3)[axis])
            before = d.xmat[m.body(body).id].reshape(3, 3).copy()
            d.qpos[j.qposadr[0]] += 0.01
            mujoco.mj_forward(m, d)
            after = d.xmat[m.body(body).id].reshape(3, 3)
            assert np.linalg.norm(before - after) > 0.01
            mujoco.mj_resetDataKeyframe(m, d, 0)
            mujoco.mj_forward(m, d)


def test_safe_mapping_and_delayed_slew():
    np.testing.assert_allclose(action_to_target(-np.ones(6)), JOINT_LOW)
    np.testing.assert_allclose(action_to_target(np.ones(6)), JOINT_HIGH)
    np.testing.assert_allclose(action_to_target(target_to_action(HOME)), HOME)
    with pytest.raises(ValueError):
        action_to_target(np.full(6, np.nan))
    s = ServoTargets(delay=0.04)
    s.enqueue(0, JOINT_HIGH)
    for t in (0, 0.02):
        np.testing.assert_array_equal(s.advance(t, CONTROL_DT), HOME)
    result = s.advance(0.04, CONTROL_DT)
    assert np.max(np.abs(result - HOME)) <= TARGET_SPEED * CONTROL_DT + 1e-10
    for i in range(100):
        s.advance(0.06 + i * CONTROL_DT, CONTROL_DT)
    np.testing.assert_allclose(s.applied, JOINT_HIGH)


def test_gym_contract_standing_and_imu():
    e = HumanoidEnv()
    try:
        check_env(e, warn=True)
        obs, _ = e.reset(seed=42)
        assert obs.shape == (90,)
        gyro, accel = e._raw_imu()
        assert np.linalg.norm(accel) == pytest.approx(9.81, abs=0.2)
        assert e._contact_state()[0].all() and not e._contact_state()[1]
        for _ in range(1500):
            obs, reward, term, trunc, info = e.step(target_to_action(HOME))
            assert np.isfinite(obs).all() and np.isfinite(reward)
            assert not term
        assert trunc and info["duration_s"] == 30
        assert not info["walking_success"] and info["alternations"] == 0
        with pytest.raises(RuntimeError):
            e.step(np.zeros(6))
    finally:
        e.close()


@pytest.mark.parametrize("randomized", [False, True])
def test_reset_reproducibility_and_noncompounding(randomized):
    e = HumanoidEnv(domain_randomization=randomized, episode_seconds=1)
    try:
        def rollout():
            first, _ = e.reset(seed=17)
            result = [first]
            for _ in range(10):
                obs, _, term, trunc, _ = e.step(target_to_action(HOME))
                result.append(obs)
                if term or trunc:
                    break
            return np.array(result), e.model.body_mass.copy()
        a, ma = rollout()
        b, mb = rollout()
        np.testing.assert_array_equal(a, b)
        np.testing.assert_array_equal(ma, mb)
        e.domain_randomization = False
        e.reset(seed=17)
        np.testing.assert_array_equal(e.model.body_mass, e.nominal["body_mass"])
        np.testing.assert_array_equal(e.model.body_inertia, e.nominal["body_inertia"])
    finally:
        e.close()


@pytest.mark.parametrize("command", ["random", "low", "high"])
def test_bounded_extreme_runs_and_fall(command):
    e = HumanoidEnv(episode_seconds=2, domain_randomization=True)
    rng = np.random.default_rng(2)
    try:
        for seed in range(3):
            e.reset(seed=seed)
            for _ in range(100):
                action = rng.uniform(-1, 1, 6) if command == "random" else np.full(6, -1 if command == "low" else 1)
                obs, reward, terminated, truncated, info = e.step(action)
                assert e.observation_space.contains(obs) and np.isfinite(reward)
                assert (e.servos.applied >= JOINT_LOW).all() and (e.servos.applied <= JOINT_HIGH).all()
                if terminated or truncated:
                    break
        e.reset(seed=0)
        e.data.qpos[2] = 0.03
        mujoco.mj_forward(e.model, e.data)
        _, _, terminated, truncated, info = e.step(target_to_action(HOME))
        assert terminated and not truncated and info["fallen"]
    finally:
        e.close()


def test_observation_command_acknowledgement_and_imu_filter():
    e = HumanoidEnv(episode_seconds=0.1)
    try:
        e.reset(seed=1)
        obs, *_ = e.step(np.ones(6))
        # First command is still waiting for the 20 ms electronics/servo delay.
        np.testing.assert_allclose(obs[-12:-6], target_to_action(HOME), atol=1e-6)
        np.testing.assert_allclose(obs[-6:], np.ones(6))
        obs, *_ = e.step(np.ones(6))
        np.testing.assert_allclose(obs[-12:-6], target_to_action(e.servos.applied), atol=1e-6)
        assert np.linalg.norm(e.servos.applied - HOME) > 0
        # Unobserved shaft lag exists: command targets are not joint feedback.
        assert np.linalg.norm(e.data.qpos[e.qadr] - e.servos.applied) > 0.001
        f = GravityEstimator()
        f.reset(np.array([0, 0, 9.81]))
        np.testing.assert_allclose(f.gravity, [0, 0, -1])
        f.update(np.array([1., 0, 0]), np.zeros(3), 0.01)
        assert f.gravity[1] < 0  # Body rotates +roll; world-down vector rotates back.
    finally:
        e.close()


def test_serial_bounds_and_corruption():
    packet = command_frame(65535, 1234, HOME)
    assert decode_frame(packet)[0] == "C"
    for q in (JOINT_LOW, JOINT_HIGH):
        received = np.array([int(x) for x in decode_frame(command_frame(0, 0, q))[4:]]) / 1000
        assert (received >= JOINT_LOW).all() and (received <= JOINT_HIGH).all()
    corrupt = bytearray(packet)
    corrupt[10] ^= 1
    with pytest.raises(ValueError):
        decode_frame(bytes(corrupt))
    with pytest.raises(ValueError):
        command_frame(0, 0, JOINT_HIGH + 0.1)
    with pytest.raises(ValueError):
        decode_frame(b"X" * 193)
    fields = ["T", "1", "0", "123", "1", *[str(round(x * 1000)) for x in HOME], "0", "0", "9810", "0", "0", "0"]
    t = telemetry_frame(encode_frame(fields))
    np.testing.assert_allclose(t.accelerometer, [0, 0, 9.81])


def test_budget_unknowns_and_cap():
    from tools.budget_gate import check_basket
    basket = json.loads((ROOT / "procurement.json").read_text())
    report = check_basket(basket)
    assert report["total_price_eur"] is None and not report["purchase_cleared"]
    assert report["known_delivered_subtotal_eur"] == "90.32"
    basket["items"].append({"product": "hypothetical delivered quote", "unit_price_eur": 20, "quantity": 1})
    report = check_basket(basket)
    assert report["status"] == "OVER BUDGET" and report["confirmed_minimum_shortfall_eur"] == "10.32"


def test_pulse_calibration_and_whole_foot_step_count():
    # Example calibration is synthetic, used only to verify the arithmetic.
    pulses = calibrated_pulses(HOME, np.full(6, 1500), np.full(6, 500),
                               np.array([1, 1, 1, -1, -1, -1]), np.full(6, 900), np.full(6, 2100))
    assert pulses[0] < 1500 and pulses[3] > 1500
    e = HumanoidEnv()
    try:
        e.reset(seed=1)
        # A toe pivot cannot count: whole-foot lowest corner must clear by 3 mm.
        e._minimum_foot_height = lambda i: 0.002
        for _ in range(30):
            e._record_steps([False, True])
        e._record_steps([True, True])
        assert e.lifted_steps[0] == 0
        e._minimum_foot_height = lambda i: 0.004
        for _ in range(30):
            e._record_steps([False, False])
        e._record_steps([True, True])
        assert e.lifted_steps.tolist() == [0, 0]  # A hop lacks opposite-foot support.
        for side in [0, 1, 0, 1]:
            contacts = np.ones(2, dtype=bool); contacts[side] = False
            for _ in range(30):
                e._record_steps(contacts)
            e._minimum_foot_height = lambda i: 0.001
            e._record_steps(contacts)  # Descending below threshold preserves a valid lift.
            e._minimum_foot_height = lambda i: 0.004
            e._record_steps([True, True])
        assert e.lifted_steps.tolist() == [2, 2] and e.alternations == 3
    finally:
        e.close()
