"""Offline support/clearance diagnosis, never part of deployable observations.

An anchored level foot is an ideal kinematic constraint, not a simulated support
or a realizable controller. COM inside its support polygon is necessary for quiet
single support without external forces, not sufficient for a stable step. The
finite candidate set cannot prove that other feasible poses do not exist.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys

import mujoco
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from calibration import configuration_identity
from humanoid_env import HumanoidEnv
from robot_config import CONTROL_DT, HOME, JOINT_HIGH, JOINT_LOW, JOINT_NAMES, SERVO_TORQUE, target_to_action
from tools.diagnose_motion import command


def convex_hull(points):
    """Counterclockwise monotone-chain hull; discard collinear interior points."""
    points = sorted(set(map(tuple, np.asarray(points, dtype=float))))
    if len(points) <= 1:
        return np.asarray(points).reshape(-1, 2)

    def cross(a, b, c):
        u, v = np.asarray(b) - a, np.asarray(c) - a
        return u[0] * v[1] - u[1] * v[0]

    lower, upper = [], []
    for chain, sequence in ((lower, points), (upper, points[::-1])):
        for p in sequence:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], p) <= 0:
                chain.pop()
            chain.append(p)
    return np.asarray(lower[:-1] + upper[:-1])


def support_margin(point, polygon):
    """Minimum signed edge distance in metres; positive inside, None if degenerate."""
    hull = convex_hull(polygon)
    if len(hull) < 3:
        return None
    edges = np.roll(hull, -1, axis=0) - hull
    offset = np.asarray(point) - hull
    distances = (edges[:, 0] * offset[:, 1] - edges[:, 1] * offset[:, 0]) / np.linalg.norm(edges, axis=1)
    return float(np.min(distances))


def centre_of_mass(env):
    return np.sum(env.model.body_mass[:, None] * env.data.xipos, axis=0) / env.model.body_mass.sum()


def anchor_pose(env, angles, stance):
    """Put stance foot level, its pad-bottom centre at world origin, using FK only."""
    angles = np.asarray(angles, dtype=float)
    if angles.shape != (6,) or not np.isfinite(angles).all() or np.any(angles < JOINT_LOW - 1e-12) or np.any(angles > JOINT_HIGH + 1e-12):
        raise ValueError("Diagnostic pose must respect all six safe command intervals")
    if stance not in (0, 1):
        raise ValueError("Stance must be 0 (left) or 1 (right)")
    model, data = env.model, env.data
    mujoco.mj_resetDataKeyframe(model, data, model.key('home').id)
    data.qpos[:3] = 0
    data.qpos[3:7] = [1, 0, 0, 0]
    data.qpos[env.qadr] = angles
    mujoco.mj_forward(model, data)
    foot = model.body(('left', 'right')[stance] + '_foot').id
    rotation = data.xmat[foot].reshape(3, 3).T.copy()
    position = -rotation @ data.site_xpos[env.foot_center_sites[stance]]
    quat = np.empty(4)
    mujoco.mju_mat2Quat(quat, rotation.reshape(9))
    data.qpos[:3], data.qpos[3:7] = position, quat
    mujoco.mj_forward(model, data)


def level_pad_polygon(env, stance, samples=64):
    """Inscribed approximation of the four level pad discs, not the whole foot plate."""
    points = []
    for gid in sorted(env.foot_geom_groups[stance] - {env.foot_plate_ids[stance]}):
        rotation = env.data.geom_xmat[gid].reshape(3, 3)
        if not np.allclose(rotation, np.eye(3), atol=1e-9):
            raise ValueError("Pad support polygon requires a level anchored stance foot")
        theta = np.arange(samples) * 2 * np.pi / samples
        local = np.column_stack((env.model.geom_size[gid, 0] * np.cos(theta),
                                 env.model.geom_size[gid, 0] * np.sin(theta),
                                 np.full(samples, -env.model.geom_size[gid, 1])))
        points.extend((local @ rotation.T + env.data.geom_xpos[gid])[:, :2])
    return convex_hull(points)


def gravity_torques(env, angles, stance, delta=1e-5):
    """Potential-energy derivative with fixed foot; ignores acceleration and tether."""
    torques = []
    for j in range(6):
        offset = np.zeros(6)
        offset[j] = delta
        energies = []
        for sign in (1, -1):
            # Limits bound selected commands, not an infinitesimal derivative.
            shifted = np.asarray(angles) + sign * offset
            clipped = np.clip(shifted, JOINT_LOW, JOINT_HIGH)
            anchor_pose(env, clipped, stance)
            energies.append(-float(np.sum(env.model.body_mass[:, None] * env.data.xipos * env.model.opt.gravity)))
        width = np.clip(angles[j] + delta, JOINT_LOW[j], JOINT_HIGH[j]) - np.clip(angles[j] - delta, JOINT_LOW[j], JOINT_HIGH[j])
        torques.append((energies[0] - energies[1]) / width)
    anchor_pose(env, angles, stance)
    return np.asarray(torques)


def pose_record(env, label, angles, stance):
    anchor_pose(env, angles, stance)
    polygon = level_pad_polygon(env, stance)
    com = centre_of_mass(env)
    clearance = env._minimum_foot_height(1 - stance)
    margin = support_margin(com[:2], polygon)
    torques = gravity_torques(env, angles, stance)
    penetrating = []
    for contact in env.data.contact:
        if contact.dist < -1e-5:
            # Stance pads are exactly at z=0. Any penetration is a warning, not
            # silently hidden to label an otherwise favourable COM pose feasible.
            penetrating.append([env.model.geom(int(g)).name for g in (contact.geom1, contact.geom2)])
    return {'name': label, 'stance': ('left', 'right')[stance],
            'angles_deg': np.rad2deg(angles).tolist(), 'com_m': com.tolist(),
            'support_polygon_xy_m': polygon.tolist(), 'com_margin_m': margin,
            'swing_whole_foot_clearance_m': clearance,
            'gravity_torque_Nm': torques.tolist(), 'peak_static_torque_Nm': float(np.max(np.abs(torques))),
            'twice_static_demand_within_estimate': bool(np.max(np.abs(torques)) * 2 <= SERVO_TORQUE),
            'penetrating_collision_pairs': penetrating,
            'passes_sampled_static_conditions': bool(clearance >= .003 and margin >= 0 and not penetrating
                                                     and np.max(np.abs(torques)) <= SERVO_TORQUE)}


def contact_diagnostics(env):
    loads = np.zeros(2)
    points = [[], []]
    force = np.zeros(6)
    for i, contact in enumerate(env.data.contact):
        if env.floor_id not in (contact.geom1, contact.geom2):
            continue
        other = contact.geom2 if contact.geom1 == env.floor_id else contact.geom1
        mujoco.mj_contactForce(env.model, env.data, i, force)
        if force[0] <= 1e-6:
            continue
        for foot in range(2):
            if other in env.foot_geom_groups[foot]:
                loads[foot] += force[0]
                points[foot].append(contact.pos[:2].copy())
    com = centre_of_mass(env)
    margins = [support_margin(com[:2], points[i]) if points[i] else None for i in range(2)]
    return loads, margins, com


def replay_profiles(output):
    reports = []
    for roll in (15, 5, 0):
        env = HumanoidEnv(episode_seconds=18)
        rows = []
        try:
            env.reset(seed=42)
            while not env.done:
                _, _, _, _, info = env.step(target_to_action(command(env.steps * CONTROL_DT, roll)))
                loads, margins, com = contact_diagnostics(env)
                error = np.rad2deg(env.applied_command - env.data.qpos[env.qadr])
                row = {'time_s': info['duration_s'], 'com_x_m': com[0], 'com_y_m': com[1],
                       'left_load_N': loads[0], 'right_load_N': loads[1],
                       'left_load_fraction': loads[0] / loads.sum() if loads.sum() else 0,
                       'left_contact_hull_margin_m': margins[0], 'right_contact_hull_margin_m': margins[1],
                       'left_clearance_m': env._minimum_foot_height(0), 'right_clearance_m': env._minimum_foot_height(1),
                       'max_tracking_error_deg': float(np.max(np.abs(error))),
                       'max_static_envelope_utilization': float(np.max(np.abs(env.data.actuator_force[env.aids])) / SERVO_TORQUE)}
                rows.append(row)
            with (output / f'dynamic_roll{roll}.csv').open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0])
                writer.writeheader(); writer.writerows(rows)
            # Ignore initial quiet standing when reporting attempted transfer.
            moving = [r for r in rows if r['time_s'] >= 4]
            reports.append({'swing_ankle_deg': roll, 'final_metrics': info,
                            'left_load_fraction_range_during_motion': [min(r['left_load_fraction'] for r in moving), max(r['left_load_fraction'] for r in moving)],
                            'max_tracking_error_deg': max(r['max_tracking_error_deg'] for r in moving),
                            'max_static_envelope_utilization': max(r['max_static_envelope_utilization'] for r in moving),
                            'max_left_clearance_m': max(r['left_clearance_m'] for r in moving),
                            'max_right_clearance_m': max(r['right_clearance_m'] for r in moving)})
        finally:
            env.close()
    return reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    env = HumanoidEnv()
    poses = []
    try:
        for stance in (0, 1):
            poses.append(pose_record(env, 'HOME', HOME.copy(), stance))
            # Explicit finite engineering probes; not a gait optimizer/training.
            # Keep sagittal foot pitch level (hip+knee=0), sweep safe lateral
            # shift and shortening of only the swing leg. Include both signs.
            for lean in (-20, -15, -10, 0, 10, 15, 20):
                for pitch in (-10, -20, -30, -35):
                    for swing_roll in sorted({lean, 0, -lean}):
                        angles = HOME.copy()
                        angles[[2, 5]] = np.deg2rad(lean)
                        swing = 3 * (1 - stance)
                        angles[swing:swing + 3] = np.deg2rad([pitch, -pitch, swing_roll])
                        poses.append(pose_record(env, f'lean{lean}_swing{pitch}_roll{swing_roll}', angles, stance))
    finally:
        env.close()
    (args.output / 'static_poses.json').write_text(json.dumps(poses, indent=2) + '\n')
    dynamic = replay_profiles(args.output)
    candidates = [p for p in poses if p['passes_sampled_static_conditions']]
    summary = {'state': 'locally executed offline diagnosis of provisional model; not gait/manufacturing approval',
               'configuration_identity': configuration_identity(), 'joint_order': JOINT_NAMES,
               'estimated_static_envelope_Nm': SERVO_TORQUE, 'static_pose_count': len(poses),
               'candidate_count': len(candidates),
               'candidates': sorted(candidates, key=lambda p: -p['com_margin_m'])[:6],
               'dynamic_profiles': dynamic,
               'limitations': ['Anchoring a stance foot is a kinematic construction, not an actuator or passive stop.',
                              'Level-pad support polygon uses 64-point inscribed circles; instantaneous dynamic hull uses only loaded contact points.',
                              'Static torque omits acceleration, cable and flex; COM containment and estimated torque are necessary screens only.',
                              'Candidates do not establish collision-free transitions, balance, strength, 40ms lift, or alternating walking.',
                              'No sampled candidate does not prove impossibility; plant and geometry remain unmeasured.']}
    sources = ['tools/analyze_support.py', 'tools/diagnose_motion.py', 'robot.xml', 'physical_spec.json',
               'robot_config.py', 'humanoid_env.py', 'servo_control.py', 'imu_observation.py', 'gait_metrics.py', 'calibration.py']
    summary['source_sha256'] = {}
    for name in sources:
        target = args.output / 'source' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
        summary['source_sha256'][name] = hashlib.sha256(target.read_bytes()).hexdigest()
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in ('candidates', 'dynamic_profiles')}, indent=2))


if __name__ == '__main__':
    main()
