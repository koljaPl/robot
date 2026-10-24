"""Declared stance-crouch probes, ordinary HOME reset and unchanged plant.

Geometric preparation matches the two knee-dependent leg heights to ankle roll
for ideal parallel flat feet. It is an open-loop construction, not feedback from
simulation truth. Friction, compliance and COM containment can still defeat it.
No optimizer, training, state edits after reset, or manufacturing approval.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from calibration import configuration_identity
from humanoid_env import HumanoidEnv
from robot_config import (HOME, CONTROL_DT, PHYSICAL_SPEC, JOINT_LOW, JOINT_HIGH,
                          target_to_action, SERVO_TORQUE)
from tools.analyze_support import contact_diagnostics, pose_record

PROFILES = ('simultaneous50', 'crouch_first50', 'geometric50', 'geometric40', 'geometric50_swap')


def smooth(x):
    x = np.clip(x, 0, 1)
    return x*x*(3-2*x)


def matched_roll(knee_stance, knee_swing):
    """Radians: ideal equal-height parallel pad planes, x-forward/y-left/z-up.

    With equal thigh lengths and equal total hip+knee pitch, rotating the pelvis
    to level the feet gives ankle-height difference L*(cos(k_swing)-cos(k_stance)).
    The hip lateral separation must absorb that difference through roll.
    """
    geometry = PHYSICAL_SPEC['geometry']
    difference = geometry['thigh_length']*(np.cos(knee_swing)-np.cos(knee_stance))
    return float(np.arctan2(difference, 2*geometry['hip_half_spacing']))


def left_pose(fraction, knee_deg):
    """Matching hip+knee pitch on both legs; all commands within existing bounds."""
    goal = np.deg2rad([-35, knee_deg, 0, knee_deg-35, 0, 0])
    return HOME + fraction*(goal-HOME)


def target_at(time_s, profile):
    if profile not in PROFILES:
        raise ValueError('Unknown stance-transfer profile')
    if not np.isfinite(time_s) or time_s < 0:
        raise ValueError('Time must be finite and non-negative')
    if time_s <= 2 or time_s >= 30:
        return HOME.copy()
    stance = 0 if time_s <= 16 else 1
    local = time_s - (2 if stance == 0 else 16)
    # 4s prepare,2s transfer,2s hold,2s return lean,4s uncrouch.
    fraction = smooth(local/4) if local <= 4 else 1.0 if local <= 10 else 1-smooth((local-10)/4)
    knee = 40 if profile.endswith('40') else 50
    q = left_pose(fraction, knee)
    matched = matched_roll(q[1], q[4])
    final = np.deg2rad(20)
    if profile.startswith('geometric'):
        base = matched
    elif profile.startswith('crouch_first'):
        base = 0.0
    else:
        base = fraction*final
    if profile == 'geometric50_swap' and 6 < local < 9:
        # Once load has moved left, extend the stance leg and shorten the swing
        # leg. This tests the missing bridge to the previously prepared hold.
        prepared = np.deg2rad([-10, 10, 20, -35, 35, 20])
        fraction_swap = smooth(local-6) if local <= 7 else 1.0 if local <= 8 else 1-smooth(local-8)
        q[[2, 5]] = final
        q += fraction_swap*(prepared-q)
        roll = final
    elif profile == 'geometric50_swap' and 9 <= local < 10:
        roll = final+(base-final)*smooth(local-9)
    elif local <= 4 or local >= 10:
        roll = base
    elif local <= 6:
        roll = base+(final-base)*smooth((local-4)/2)
    elif local <= 8:
        roll = final
    else:
        roll = final+(base-final)*smooth((local-8)/2)
    q[[2, 5]] = roll
    if stance == 1:
        q = q[[3, 4, 5, 0, 1, 2]].copy()
        q[[2, 5]] *= -1
    if np.any(q < JOINT_LOW-1e-12) or np.any(q > JOINT_HIGH+1e-12):
        raise ValueError('Diagnostic would exceed safe joint targets')
    return q


def mirror_targets(target):
    q = np.asarray(target)[[3, 4, 5, 0, 1, 2]].copy()
    q[[2, 5]] *= -1
    return q


def run_profile(profile, output, *, seed=42, first_stance='left', video=False):
    if first_stance not in ('left', 'right'):
        raise ValueError('First stance must be left or right')
    env = HumanoidEnv(episode_seconds=30, render_mode='rgb_array' if video else None)
    rows = []
    streak, longest = np.zeros(2), np.zeros(2)
    writer = None
    try:
        env.reset(seed=seed)
        if video:
            import imageio.v2 as io
            from evaluate import show_physical_geometry
            show_physical_geometry(env.model)
            writer = io.get_writer(output/(profile+'.mp4'), fps=50, codec='libx264')
        while not env.done:
            target = target_at(env.steps*CONTROL_DT, profile)
            if first_stance == 'right':
                target = mirror_targets(target)
            _, _, _, _, info = env.step(target_to_action(target))
            loads, margins, com = contact_diagnostics(env)
            heights = np.array([env._minimum_foot_height(i) for i in (0, 1)])
            # Sampled diagnostic only; existing physics-step gait metric decides steps.
            streak = np.where(heights >= .003, streak+CONTROL_DT, 0)
            longest = np.maximum(longest, streak)
            row = {'time_s': info['duration_s'], 'com_x_m': com[0], 'com_y_m': com[1],
                   'left_clearance_m': heights[0], 'right_clearance_m': heights[1],
                   'left_load_N': loads[0], 'right_load_N': loads[1],
                   'left_load_fraction': loads[0]/loads.sum() if loads.sum() else 0,
                   'left_contact_margin_m': margins[0], 'right_contact_margin_m': margins[1],
                   'max_tracking_error_deg': float(np.rad2deg(np.max(np.abs(env.applied_command-env.data.qpos[env.qadr])))),
                   'max_static_envelope_utilization': float(np.max(np.abs(env.data.actuator_force[env.aids]))/SERVO_TORQUE),
                   'steps_left': info['lifted_steps_left'], 'steps_right': info['lifted_steps_right'],
                   'gait_distance_m': info['gait_distance_m'],
                   'fallen': info['fallen']}
            for i, side in enumerate(('left', 'right')):
                rotation = env.data.xmat[env.model.body(side+'_foot').id].reshape(3, 3)
                row[side+'_roll_deg'] = float(np.rad2deg(np.arctan2(rotation[2, 1], rotation[2, 2])))
            rows.append(row)
            if writer:
                image = env.render()
                writer.append_data(image)
                if len(rows) == 1:
                    io.imwrite(output/(profile+'_preview.png'), image)
        with (output/(profile+'.csv')).open('w', newline='') as f:
            w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
        target = target_at(9, profile)
        if first_stance == 'right':
            target = mirror_targets(target)
        pose = pose_record(env, profile+'_ideal_target', target, int(first_stance == 'right'))
        return {'profile': profile, 'seed': seed, 'first_stance': first_stance,
                'video_saved': video, 'final_metrics': info, 'ideal_target_screen': pose,
                'max_whole_foot_clearance_m': [max(r[side+'_clearance_m'] for r in rows) for side in ('left', 'right')],
                'longest_20ms_sampled_clearance_at_least_3mm_s': longest.tolist(),
                'max_tracking_error_deg': max(r['max_tracking_error_deg'] for r in rows),
                'max_static_envelope_utilization': max(r['max_static_envelope_utilization'] for r in rows)}
    finally:
        if writer:
            writer.close()
        env.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--profiles', nargs='+', choices=PROFILES, default=PROFILES)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--first-stance', choices=('left', 'right'), default='left')
    parser.add_argument('--video', action='store_true')
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=False)
    reports=[run_profile(profile,args.output, seed=args.seed, first_stance=args.first_stance, video=args.video) for profile in args.profiles]
    identity=configuration_identity()
    sources=set(identity['files']) | {'tools/stance_transfer.py','tools/analyze_support.py','tools/diagnose_motion.py',
                                    'requirements.txt','requirements-dev.txt','evaluate.py'}
    sources |= {str(p.relative_to(ROOT)) for p in (ROOT/'cad/stl').glob('*.stl')}
    hashes={}
    for name in sorted(sources):
        path=args.output/'source'/name; path.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/name,path); hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    report={'state':'provisional open-loop diagnosis, not learned/physical walking',
            'configuration_identity':identity,'seed':args.seed,'first_stance':args.first_stance,
            'declared_profiles':args.profiles,'profiles':reports,
            'source_sha256':hashes,'plant_changed':False,'initialization':'HOME reset only; commands thereafter',
            'limits':'Static FK and20ms streaks are diagnostic only. Existing gait metrics remain authoritative; no gates cleared.'}
    (args.output/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k!='ideal_target_screen'} for r in reports],indent=2))


if __name__=='__main__':
    main()
