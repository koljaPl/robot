"""Two bounded HOME-to-support transition probes, with unchanged plant/control.

No state anchoring after reset, optimizer, policy training, stronger motors or
new safety limits. A lifted foot is not an accepted walking cycle. This tests
whether ordering lateral shift and leg shortening reaches the prepared pose.
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
from robot_config import HOME, CONTROL_DT, target_to_action
from tools.analyze_support import contact_diagnostics


def keyframes(order):
    if order not in ('lean_first', 'shorten_first'):
        raise ValueError('Unknown transition order')
    frames = [(0, HOME.copy()), (2, HOME.copy())]
    for stance, start in ((0, 2), (1, 12)):
        lean, shortened = HOME.copy(), HOME.copy()
        lean[[2, 5]] = np.deg2rad(20 if stance == 0 else -20)
        swing = 3 * (1-stance)
        shortened[swing:swing+2] = np.deg2rad([-35, 35])
        combined = shortened.copy(); combined[[2, 5]] = lean[[2, 5]]
        intermediate = lean if order == 'lean_first' else shortened
        frames.extend([(start+2, intermediate), (start+4, combined),
                       (start+6, combined), (start+8, intermediate), (start+10, HOME.copy())])
    return frames


def target_at(time_s, order):
    frames = keyframes(order)
    for (start, a), (end, b) in zip(frames, frames[1:]):
        if time_s <= end:
            fraction = np.clip((time_s-start)/(end-start), 0, 1)
            return a + (b-a) * fraction*fraction*(3-2*fraction)
    return HOME.copy()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=False)
    reports = []
    for order in ('lean_first', 'shorten_first'):
        env = HumanoidEnv(episode_seconds=22)
        rows = []
        streak, longest = np.zeros(2), np.zeros(2)
        try:
            env.reset(seed=42)
            while not env.done:
                _, _, _, _, info = env.step(target_to_action(target_at(env.steps * CONTROL_DT, order)))
                heights = np.array([env._minimum_foot_height(i) for i in (0, 1)])
                loads, _, _ = contact_diagnostics(env)
                streak = np.where(heights >= .003, streak + CONTROL_DT, 0)
                longest = np.maximum(longest, streak)
                row = {'time_s': info['duration_s'], 'left_clearance_m': heights[0], 'right_clearance_m': heights[1],
                       'left_load_N': loads[0], 'right_load_N': loads[1], 'fallen': info['fallen']}
                for i, side in enumerate(('left', 'right')):
                    row[side+'_sampled_lift_streak_s'] = streak[i]
                rows.append(row)
            with (args.output/(order+'.csv')).open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0]); writer.writeheader(); writer.writerows(rows)
            reports.append({'order': order, 'seed': 42, 'final_metrics': info,
                            'max_whole_foot_clearance_m': [max(r[side+'_clearance_m'] for r in rows) for side in ('left', 'right')],
                            'longest_20ms_sampled_clearance_at_least_3mm_s': longest.tolist()})
        finally:
            env.close()
    identity = configuration_identity()
    sources = set(identity['files']) | {'tools/transfer_reference.py', 'tools/analyze_support.py', 'tools/diagnose_motion.py',
                                       'requirements.txt', 'requirements-dev.txt'}
    sources |= {str(p.relative_to(ROOT)) for p in (ROOT/'cad/stl').glob('*.stl')}
    hashes = {}
    for name in sorted(sources):
        target = args.output/'source'/name; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/name, target)
        hashes[name] = hashlib.sha256(target.read_bytes()).hexdigest()
    summary = {'state': 'provisional bounded transition diagnosis; no physical or learned walking claim',
               'configuration_identity': identity, 'initialization': 'ordinary HOME reset, no subsequent state changes',
               'safety': 'unchanged safe targets, slew, delay, gains and estimated0.08Nm envelope',
               'profiles': reports, 'source_sha256': hashes,
               'interpretation': 'Clearance streak is a20ms sampled diagnostic, not the gait acceptance test. Walking requires existing non-sliding alternating step metrics.'}
    (args.output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(reports, indent=2))


if __name__ == '__main__':
    main()
