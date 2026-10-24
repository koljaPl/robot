"""MuJoCo/Gymnasium walking environment for the provisional physical S6 design."""
from collections import deque
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import mujoco
from robot_config import (ROOT, JOINT_NAMES, HOME, PHYSICS_DT, CONTROL_DT, IMU_DT,
                          HISTORY, FRAME_SIZE, DR, BASE_DELAY, TARGET_SPEED,
                          SERVO_TORQUE, SERVO_NO_LOAD_SPEED, GYRO_NOISE,
                          ACCEL_NOISE, MAX_EPISODE_SECONDS, action_to_target, target_to_action,
                          IMU_FILTER_HZ, IMU_ACCEL_RANGE, IMU_GYRO_RANGE)
from gait_metrics import GaitMetrics, progress_reward
from servo_control import ServoTargets
from imu_observation import GravityEstimator, ObservationHistory


class HumanoidEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    def __init__(self, xml_path=None, render_mode=None, domain_randomization=False,
                 episode_seconds=MAX_EPISODE_SECONDS, calibration=None):
        super().__init__()
        if render_mode not in (None, "human", "rgb_array"):
            raise ValueError("render_mode must be None, human, or rgb_array")
        if not np.isfinite(episode_seconds) or episode_seconds <= 0:
            raise ValueError("episode_seconds must be positive")
        self.model = mujoco.MjModel.from_xml_path(str(xml_path or ROOT / "robot.xml"))
        if not np.isclose(self.model.opt.timestep, PHYSICS_DT):
            raise ValueError("MJCF timestep must match robot_config.PHYSICS_DT")
        self.data = mujoco.MjData(self.model)
        self.render_mode = render_mode
        self.calibration = calibration
        self.domain_randomization = bool(domain_randomization)
        self.max_steps = max(1, int(round(episode_seconds / CONTROL_DT)))
        self.action_space = spaces.Box(-1.0, 1.0, shape=(6,), dtype=np.float32)
        self.observation_space = spaces.Box(-1.0, 1.0, shape=(HISTORY * FRAME_SIZE,), dtype=np.float32)
        self.qadr = np.array([self.model.jnt_qposadr[self.model.joint(n).id] for n in JOINT_NAMES])
        self.vadr = np.array([self.model.jnt_dofadr[self.model.joint(n).id] for n in JOINT_NAMES])
        self.aids = np.array([self.model.actuator(n + "_servo").id for n in JOINT_NAMES])
        self.torso_id = self.model.body("torso").id
        self.floor_id = self.model.geom("floor").id
        self.foot_plate_ids = [self.model.geom(s + "_foot_plate").id for s in ("left", "right")]
        self.foot_geom_groups = [set([self.foot_plate_ids[i]] + [self.model.geom(f"{side}_foot_pad_{j}").id for j in range(4)])
                                 for i, side in enumerate(("left", "right"))]
        self.foot_ids = set.union(*self.foot_geom_groups)
        self.foot_center_sites = [self.model.site(s + "_foot_contact_center").id for s in ("left", "right")]
        self.nominal = {name: getattr(self.model, name).copy() for name in (
            "body_mass", "body_inertia", "geom_friction", "dof_damping", "actuator_forcerange",
            "actuator_biasprm")}
        self.estimator = GravityEstimator()
        self.history = ObservationHistory()
        self.viewer = None
        self.renderer = None
        self.done = True

    def _randomize(self):
        for name, value in self.nominal.items():
            getattr(self.model, name)[:] = value
        self.offset = np.zeros(6)
        self.gyro_bias = np.zeros(3)
        self.accel_bias = np.zeros(3)
        self.noise_scale = 1.0
        delay, speed, self.no_load_speed = BASE_DELAY, TARGET_SPEED, SERVO_NO_LOAD_SPEED
        if self.domain_randomization:
            rng = self.np_random
            scale = rng.uniform(1 - DR.mass, 1 + DR.mass, self.model.nbody)
            scale[0] = 1
            self.model.body_mass[:] *= scale
            self.model.body_inertia[:] *= scale[:, None]
            self.model.geom_friction[:] *= rng.uniform(1 - DR.friction, 1 + DR.friction)
            strength = rng.uniform(1 - DR.strength, 1 + DR.strength, 6)
            self.model.actuator_forcerange[self.aids] *= strength[:, None]
            self.model.dof_damping[self.vadr] *= rng.uniform(1 - DR.damping, 1 + DR.damping, 6)
            speed_scale = rng.uniform(1 - DR.speed, 1 + DR.speed)
            speed *= speed_scale
            self.no_load_speed *= speed_scale
            delay = int(rng.choice(DR.delay_ticks)) * CONTROL_DT
            self.offset = rng.uniform(-DR.offset_rad, DR.offset_rad, 6)
            self.gyro_bias = rng.uniform(-DR.gyro_bias, DR.gyro_bias, 3)
            self.accel_bias = rng.uniform(-DR.accel_bias, DR.accel_bias, 3)
            self.noise_scale = rng.uniform(*DR.sensor_noise_scale)
        self._apply_joint_offsets()
        self.torque_limit = self.model.actuator_forcerange[self.aids, 1].copy()
        self.servos = ServoTargets(delay=delay, speed=speed, calibration=self.calibration)
        mujoco.mj_setConst(self.model, self.data)

    def _apply_joint_offsets(self):
        # For our unit-gear position servos, force = kp*(command - q) - kv*qdot.
        # Add kp*offset as an affine bias: the unobserved physical equilibrium
        # becomes command+offset while ctrl/ack stay in safe COMMAND coordinates.
        # Clipping command+offset to ctrlrange would conceal error at the bounds.
        self.model.actuator_biasprm[self.aids, 0] = (
            self.nominal['actuator_biasprm'][self.aids, 0]
            + self.model.actuator_gainprm[self.aids, 0] * self.offset)

    def _raw_imu(self):
        gyro = self.data.sensor("imu_gyro").data.copy()
        accel = self.data.sensor("imu_accel").data.copy()
        gyro += self.gyro_bias + self.np_random.normal(0, GYRO_NOISE * self.noise_scale, 3)
        accel += self.accel_bias + self.np_random.normal(0, ACCEL_NOISE * self.noise_scale, 3)
        gyro = np.clip(gyro, -IMU_GYRO_RANGE, IMU_GYRO_RANGE)
        accel = np.clip(accel, -IMU_ACCEL_RANGE, IMU_ACCEL_RANGE)
        # First-order 44 Hz surrogate, not a claim to reproduce silicon DLPF exactly.
        alpha = 1 - np.exp(-2*np.pi*IMU_FILTER_HZ*IMU_DT)
        if self.filtered_gyro is None:
            self.filtered_gyro, self.filtered_accel = gyro.copy(), accel.copy()
        else:
            self.filtered_gyro += alpha*(gyro-self.filtered_gyro)
            self.filtered_accel += alpha*(accel-self.filtered_accel)
        gyro_lsb, accel_lsb = IMU_GYRO_RANGE/32768, IMU_ACCEL_RANGE/32768
        return (np.rint(self.filtered_gyro/gyro_lsb)*gyro_lsb,
                np.rint(self.filtered_accel/accel_lsb)*accel_lsb)

    def _motor_envelope(self):
        # Drive-direction torque falls with shaft speed; opposing/braking torque remains.
        velocity = self.data.qvel[self.vadr]
        positive = self.torque_limit * np.clip(1 - np.maximum(velocity, 0) / self.no_load_speed, 0, 1)
        negative = self.torque_limit * np.clip(1 - np.maximum(-velocity, 0) / self.no_load_speed, 0, 1)
        self.model.actuator_forcerange[self.aids, 0] = -negative
        self.model.actuator_forcerange[self.aids, 1] = positive

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self._randomize()
        mujoco.mj_resetDataKeyframe(self.model, self.data, self.model.key("home").id)
        self.data.ctrl[self.aids] = HOME
        # Simulate quiet physical startup before initializing from accelerometer data.
        for _ in range(100):
            self._motor_envelope()
            mujoco.mj_step(self.model, self.data)
        self.data.time = 0
        mujoco.mj_forward(self.model, self.data)
        self.filtered_gyro = self.filtered_accel = None
        gyro, accel = self._raw_imu()
        self.estimator.reset(accel)
        self.last_gyro = gyro
        self.imu_last_time = 0.0
        self.imu_next_time = IMU_DT
        self.servo_next_time = 0.0
        self.last_action = target_to_action(HOME)
        self.servos.reset()
        self.applied_command = HOME.copy()
        self.steps = 0
        self.total_reward = 0.0
        self.start_position = self.data.xpos[self.torso_id].copy()
        self.nominal_height = self.model.key("home").qpos[2]
        self.gait = GaitMetrics()
        self.lifted_steps = self.gait.steps
        self.alternations = 0
        self.done = False
        frame = self.history.frame(self.estimator.gravity, self.last_gyro, self.applied_command, self.last_action)
        obs = self.history.reset(frame)
        return obs, self._info(False)

    def _contact_state(self):
        contacts = np.zeros(2, dtype=bool)
        bad_contact = False
        for c in self.data.contact:
            if c.geom1 == self.floor_id or c.geom2 == self.floor_id:
                other = c.geom2 if c.geom1 == self.floor_id else c.geom1
                if other not in self.foot_ids:
                    bad_contact = True
                for i in range(2):
                    if other in self.foot_geom_groups[i]:
                        contacts[i] = True
        return contacts, bad_contact

    def _minimum_foot_height(self, foot_index):
        heights = []
        for gid in self.foot_geom_groups[foot_index]:
            zaxis = self.data.geom_xmat[gid].reshape(3, 3)[2]
            size = self.model.geom_size[gid]
            if self.model.geom_type[gid] == mujoco.mjtGeom.mjGEOM_CYLINDER:
                # Exact support function of a rotated finite cylinder.
                extent = size[0] * np.linalg.norm(zaxis[:2]) + size[1] * abs(zaxis[2])
            else:
                extent = np.dot(np.abs(zaxis), size)
            heights.append(self.data.geom_xpos[gid, 2] - extent)
        # All pads AND the plate must clear; a raised toe/one pad is insufficient.
        return float(min(heights))

    def _record_steps(self, contacts):
        load = np.zeros(2)
        force = np.zeros(6)
        for index, contact in enumerate(self.data.contact):
            if self.floor_id not in (contact.geom1, contact.geom2):
                continue
            other = contact.geom2 if contact.geom1 == self.floor_id else contact.geom1
            for i in range(2):
                if other in self.foot_geom_groups[i]:
                    mujoco.mj_contactForce(self.model, self.data, index, force)
                    load[i] += max(0, force[0])
        supported = load >= .10 * self.model.body_mass.sum()*9.81
        self.gait.update(self.data.site_xpos[self.foot_center_sites],
                         [self._minimum_foot_height(i) for i in range(2)],
                         contacts, supported, PHYSICS_DT)
        self.alternations = self.gait.alternations

    def _info(self, fallen):
        duration = self.steps * CONTROL_DT
        distance = float(self.data.xpos[self.torso_id, 0] - self.start_position[0])
        return {"distance_m": distance, "lateral_distance_m": float(self.data.xpos[self.torso_id, 1] - self.start_position[1]),
                "duration_s": duration, "mean_speed_m_s": distance / duration if duration else 0.0,
                "fallen": bool(fallen), "total_reward": float(self.total_reward),
                "lifted_steps_left": int(self.lifted_steps[0]), "lifted_steps_right": int(self.lifted_steps[1]),
                "alternations": int(self.alternations),
                "gait_distance_m": float(self.gait.distance),
                "max_stance_slip_m": float(self.gait.max_stance_slip),
                "rejected_steps": int(self.gait.rejected),
                "walking_success": bool(not fallen and distance >= 0.3 and self.gait.distance >= 0.3 and min(self.lifted_steps) >= 2 and self.alternations >= 3),
                "domain_randomization": self.domain_randomization}

    def step(self, action):
        if self.done:
            raise RuntimeError("Call reset() before step() and after an episode ends")
        target = action_to_target(action)
        action = np.clip(np.asarray(action, dtype=float), -1, 1)
        previous_position = self.data.xpos[self.torso_id].copy()
        self.servos.enqueue(self.data.time, target)
        fallen = False
        for _ in range(round(CONTROL_DT / PHYSICS_DT)):
            if self.data.time + 1e-10 >= self.servo_next_time:
                self.applied_command = self.servos.advance(self.data.time, CONTROL_DT)
                self.servo_next_time += CONTROL_DT
            applied = self.applied_command
            # Offset is already represented in the actuator bias, outside the
            # deployable observation. Bounds apply to commands, not true shaft pose.
            limits = self.model.actuator_ctrlrange[self.aids]
            self.data.ctrl[self.aids] = np.clip(applied, limits[:, 0], limits[:, 1])
            self._motor_envelope()
            mujoco.mj_step(self.model, self.data)
            if self.data.time + 1e-10 >= self.imu_next_time:
                gyro, accel = self._raw_imu()
                self.estimator.update(gyro, accel, self.data.time - self.imu_last_time)
                self.last_gyro = gyro
                self.imu_last_time = self.data.time
                self.imu_next_time += IMU_DT
            contacts, bad_contact = self._contact_state()
            self._record_steps(contacts)
            upright = self.data.xmat[self.torso_id].reshape(3, 3)[2, 2]
            fallen |= bad_contact or self.data.xpos[self.torso_id, 2] < self.nominal_height * 0.6 or upright < 0.5
        if not (np.isfinite(self.data.qpos).all() and np.isfinite(self.data.qvel).all()):
            raise FloatingPointError("Non-finite MuJoCo state; inspect model and controller")
        velocity = (self.data.xpos[self.torso_id] - previous_position) / CONTROL_DT
        upright = float(np.clip(self.data.xmat[self.torso_id].reshape(3, 3)[2, 2], 0, 1))
        terms = {"forward": progress_reward(velocity[0] * CONTROL_DT, CONTROL_DT),
                 "upright": CONTROL_DT * 0.2 * upright,
                 "lateral": -CONTROL_DT * 0.5 * abs(float(velocity[1])),
                 "smoothness": -CONTROL_DT * 0.0001 * float(np.mean(((action - self.last_action) / CONTROL_DT) ** 2)),
                 "fall": -2.0 if fallen else 0.0}
        reward = float(sum(terms.values()))
        self.steps += 1
        self.total_reward += reward
        self.last_action = action.copy()
        obs = self.history.append(self.history.frame(self.estimator.gravity, self.last_gyro, self.applied_command, self.last_action))
        terminated = bool(fallen)
        truncated = bool(self.steps >= self.max_steps and not terminated)
        self.done = terminated or truncated
        info = self._info(fallen)
        info["reward_terms"] = terms
        if self.render_mode == "human":
            self.render()
        return obs, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            if self.viewer is None:
                from mujoco import viewer
                self.viewer = viewer.launch_passive(self.model, self.data)
                self.viewer.cam.distance = 0.5
                self.viewer.cam.azimuth = 135
                self.viewer.cam.elevation = -15
            self.viewer.cam.lookat[:] = self.data.xpos[self.torso_id]
            self.viewer.sync()
        elif self.render_mode == "rgb_array":
            if self.renderer is None:
                self.renderer = mujoco.Renderer(self.model, height=480, width=640)
            cam = mujoco.MjvCamera()
            cam.distance, cam.azimuth, cam.elevation = 0.5, 135, -15
            cam.lookat[:] = self.data.xpos[self.torso_id]
            self.renderer.update_scene(self.data, camera=cam)
            return self.renderer.render()

    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None
        if self.renderer is not None:
            self.renderer.close()
            self.renderer = None
