"""Declared one-factor probes of the frozen scripted gait; no reference tuning.

Values are existing randomization hypotheses, not measured tolerances. Runtime
copies of the model change; physical_spec, MJCF, policy observations and the
frozen target sequence stay untouched. Positive-strength probes are diagnostics,
never a recommendation to increase nominal strength to obtain a step.
"""
import argparse
from dataclasses import asdict, dataclass
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
from robot_config import CONTROL_DT, DR, JOINT_NAMES
from tools.audit_transfer import GaitTrace
from tools.handoff_probe import target_at
from tools.phase_study import flight_summaries
from robot_config import target_to_action


@dataclass(frozen=True)
class Variant:
    name: str
    family: str
    value: float = 1.0
    joint: int | None = None


def variants():
    result = [Variant('nominal', 'nominal')]
    for family, width in (('mass', DR.mass), ('torso_mass', DR.mass),
                          ('friction', DR.friction), ('strength', DR.strength),
                          ('shaft_speed', DR.speed), ('target_slew', DR.speed),
                          ('damping', DR.damping)):
        result.extend(Variant(f'{family}_{suffix}', family, 1 + sign*width)
                      for suffix, sign in (('low', -1), ('high', 1)))
    result.append(Variant('delay_40ms', 'delay', max(DR.delay_ticks)*CONTROL_DT))
    for j, name in enumerate(JOINT_NAMES):
        result.extend(Variant(f'offset_{name}_{suffix}', 'offset', sign*DR.offset_rad, j)
                      for suffix, sign in (('minus', -1), ('plus', 1)))
    result.append(Variant('imu_noise_high', 'imu_noise', max(DR.sensor_noise_scale)))
    return {v.name: v for v in result}


class IsolatedEnv(HumanoidEnv):
    """Use nominal restoration and then a single declared deterministic change."""
    def __init__(self, variant):
        if variant not in variants().values():
            raise ValueError('Variant must be one of the declared probes')
        self.variant = variant
        super().__init__(episode_seconds=30, domain_randomization=False)

    def _randomize(self):
        super()._randomize()
        v, model = self.variant, self.model
        if v.family in ('mass', 'torso_mass'):
            indices = np.arange(1, model.nbody) if v.family == 'mass' else np.array([self.torso_id])
            model.body_mass[indices] *= v.value
            model.body_inertia[indices] *= v.value
        elif v.family == 'friction':
            model.geom_friction[:, 0] *= v.value  # condim3: sliding only
        elif v.family == 'strength':
            model.actuator_forcerange[self.aids] *= v.value
            self.torque_limit = model.actuator_forcerange[self.aids, 1].copy()
        elif v.family == 'shaft_speed':
            self.no_load_speed *= v.value
        elif v.family == 'target_slew':
            self.servos.speed *= v.value
        elif v.family == 'damping':
            model.dof_damping[self.vadr] *= v.value
        elif v.family == 'delay':
            self.servos.delay = v.value
        elif v.family == 'offset':
            self.offset[v.joint] = v.value
        elif v.family == 'imu_noise':
            self.noise_scale = v.value
        elif v.family != 'nominal':
            raise ValueError('Unknown perturbation family')
        self._apply_joint_offsets()
        mujoco.mj_setConst(model, self.data)
        self.runtime_parameters = {
            'body_mass_kg': model.body_mass.tolist(), 'body_inertia_kg_m2': model.body_inertia.tolist(),
            'body_com_local_m': model.body_ipos.tolist(), 'geom_sliding_friction': model.geom_friction[:, 0].tolist(),
            'joint_damping': model.dof_damping[self.vadr].tolist(),
            'static_torque_envelope_Nm': self.torque_limit.tolist(), 'target_slew_rad_s': self.servos.speed,
            'shaft_no_load_speed_rad_s': self.no_load_speed, 'command_delay_s': self.servos.delay,
            'joint_offsets_rad': self.offset.tolist(), 'imu_noise_scale': self.noise_scale,
            'actuator_ctrlrange_rad': model.actuator_ctrlrange[self.aids].tolist(),
            'actuator_bias_constant_Nm': model.actuator_biasprm[self.aids, 0].tolist(),
        }


def verify_frozen_sources(registry_path=None):
    registry = json.loads(Path(registry_path or ROOT/'docs/baselines/scripted_bench_tools.json').read_text())
    if configuration_identity() != registry['configuration_identity']:
        raise ValueError('Frozen baseline/model identity changed; create an explicit new study')
    # Protect the complete executed reference dependency set, not just its label.
    for name, expected in registry['source_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen reference source changed: '+name)
    return registry


def run_case(variant, output):
    output.mkdir()
    env = IsolatedEnv(variant)
    physics_hash, observation_hash = hashlib.sha256(), hashlib.sha256()
    clipped_ticks, maximum_clip, tracking_error = 0, 0.0, 0.0
    try:
        env.reset(seed=42)
        trace = GaitTrace(env)
        while not env.done:
            requested = target_at(env.steps*CONTROL_DT, 'compact')
            obs, _, _, _, info = env.step(target_to_action(requested))
            physics_hash.update(env.data.qpos.tobytes())
            physics_hash.update(env.data.qvel.tobytes())
            observation_hash.update(obs.tobytes())
            physical_target = env.applied_command + env.offset
            limits = env.model.actuator_ctrlrange[env.aids]
            lost = float(np.max(np.abs(physical_target - np.clip(physical_target, limits[:, 0], limits[:, 1]))))
            clipped_ticks += int(lost > 1e-12)
            maximum_clip = max(maximum_clip, lost)
            tracking_error = max(tracking_error, float(np.max(np.abs(env.data.qpos[env.qadr]-env.applied_command))))
        # Full numeric physics trace, without object arrays/pickle or repeated
        # text copies. The CSV report provides one row per episode/credited step.
        columns = {name: np.asarray([row[name] for row in trace.rows]) for name in trace.rows[0]}
        np.savez_compressed(output/'physics_trace.npz', **columns)
        flights = flight_summaries(trace.rows)
        result = {
            'variant': asdict(variant), 'seed': 42, 'condition': 'deterministic one-factor probe, not a DR draw',
            'runtime_parameters': env.runtime_parameters, 'final_metrics': info, 'events': trace.events,
            'flights_above_2mm': flights, 'physics_state_sha256_50Hz': physics_hash.hexdigest(),
            'observation_sha256_50Hz': observation_hash.hexdigest(),
            'legacy_shifted_target_would_clip_control_ticks': clipped_ticks,
            'legacy_maximum_error_that_would_be_hidden_rad': maximum_clip,
            'max_actual_minus_acknowledged_angle_rad_DIAGNOSTIC_ONLY': tracking_error,
            'trace_rows': len(trace.rows), 'runtime_model_changed': variant.family not in ('nominal', 'imu_noise', 'target_slew', 'delay'),
            'offset_implementation': 'affine actuator bias; commands/ack bounded, true zero error not clipped',
        }
    finally:
        env.close()
    result['runtime_variant_sha256'] = hashlib.sha256(json.dumps(
        {'variant': result['variant'], 'runtime': result['runtime_parameters']},
        sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result['trace_sha256'] = hashlib.sha256((output/'physics_trace.npz').read_bytes()).hexdigest()
    (output/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def main():
    declared = variants()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--cases', nargs='+', choices=declared, default=list(declared))
    args = parser.parse_args()
    registry = verify_frozen_sources()
    args.output.mkdir(parents=True, exist_ok=False)
    reports = []
    for name in args.cases:
        result = run_case(declared[name], args.output/name)
        reports.append(result)
        info = result['final_metrics']
        print(name, 'steps', info['lifted_steps_left']+info['lifted_steps_right'],
              'alternations', info['alternations'], 'fall', info['fallen'], flush=True)
    sources = set(registry['source_sha256']) | {'tools/sensitivity_probe.py', 'docs/baselines/scripted_r2.json',
                                               'docs/baselines/scripted_r2_offset_corrected.json', 'docs/baselines/scripted_pico2.json', 'docs/baselines/scripted_bench_tools.json'}
    hashes = {}
    for name in sorted(sources):
        path = args.output/'source'/name
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/name, path)
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    summary = {
        'state': 'provisional sensitivity evidence, not physical calibration or training',
        'base_configuration_identity': configuration_identity(), 'source_sha256': hashes,
        'declared_cases': args.cases, 'results': reports, 'training_steps_added': 0,
        'nominal_files_changed': False, 'reference_tuned': False,
        'limitations': ['Endpoint probes are not failure probabilities or measured tolerances.',
                        'Uniform or torso mass scales retain local COM and scale inertia with mass.',
                        'Shaft speed and software target-slew probes are separated.',
                        'Open-loop targets ignore IMU noise; this does not mean a learned policy can ignore the IMU.',
                        'Affine actuator bias retains offset effects at command limits; real offsets remain unmeasured.']}
    (args.output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')


if __name__ == '__main__':
    main()
