"""Review a first-order servo fit against separate trials; never approves calibration."""
import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from calibration import configuration_identity
from tools.validate_measurement import COLUMNS, sha, validate_trial


def predict_response(values, parameters):
    """Use the locked fit and this trial's command timing/pre-step angle only."""
    t, u, q = values[:, :3].T
    index = int(np.flatnonzero(np.abs(np.diff(u)) > 1e-5)[0]+1)
    q0 = float(np.median(q[:index]))
    amplitude = float(u[-1]-u[0])
    pred = q0 + parameters['step_gain']*amplitude*(
        1-np.exp(-np.maximum(0, t-t[index]-parameters['delay_s'])/parameters['time_constant_s']))
    return pred, {'pre_step_angle_rad': q0, 'step_time_s': float(t[index]),
                  'command_step_rad': amplitude, 'step_index': index}


def error_metrics(values, prediction, step_index):
    residual = values[:, 2]-prediction  # measured minus predicted
    if not np.isfinite(residual).all():
        raise ValueError('Nonfinite prediction/residual')
    rmse = float(np.sqrt(np.mean(residual**2)))
    return {'rmse_rad': rmse, 'rmse_deg': float(np.rad2deg(rmse)),
            'mae_deg': float(np.rad2deg(np.mean(np.abs(residual)))),
            'max_abs_error_deg': float(np.rad2deg(np.max(np.abs(residual)))),
            'post_step_rmse_deg': float(np.rad2deg(np.sqrt(np.mean(residual[step_index:]**2))))}


def plot_trial(values, prediction, uncertainty, role, kind, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), layout='constrained', sharex=True)
    try:
        t, u, q = values[:, :3].T
        axes[0].step(t, np.rad2deg(u), where='post', color='0.6', label='Recorded target')
        axes[0].plot(t, np.rad2deg(q), color='black', lw=1, label='External angle / synthetic fixture')
        axes[0].plot(t, np.rad2deg(prediction), '--', color='tab:blue', label='Locked fit prediction')
        axes[0].set(ylabel='Angle (degrees)',
                    title=f'{role} — {kind}, diagnostic only; awaiting human review')
        axes[0].legend(fontsize=8)
        axes[1].plot(t, np.rad2deg(q-prediction), label='Measured minus predicted', color='tab:orange')
        axes[1].axhline(0, color='black', lw=.7)
        axes[1].fill_between(t, -np.rad2deg(uncertainty), np.rad2deg(uncertainty),
                             alpha=.2, color='tab:blue', label='Declared angle uncertainty (not a confidence interval)')
        axes[1].set(xlabel='Recorded aligned time (s)', ylabel='Residual (degrees)')
        axes[1].legend(fontsize=8)
        for ax in axes: ax.grid(alpha=.25)
        fig.savefig(path, dpi=150)
    finally:
        plt.close(fig)


def review(manifest_path, output):
    manifest_path, output = Path(manifest_path).resolve(), Path(output)
    if output.exists():
        raise FileExistsError('Use a new output directory; existing reports are preserved')
    manifest_hash = sha(manifest_path)
    manifest = json.loads(manifest_path.read_text())
    if not isinstance(manifest, dict) or type(manifest.get('version')) is not int or manifest['version'] != 1:
        raise ValueError('Response-review manifest must be version1')
    validation = manifest.get('validation_trials')
    if not isinstance(validation, list) or not validation:
        raise ValueError('At least one validation trial is required')
    entries = [('fit', manifest.get('fit_trial'))] + [
        (f'validation_{i:02d}', trial) for i, trial in enumerate(validation, 1)]
    trials, input_hashes, evidence_uses = [], {str(manifest_path): manifest_hash}, {}
    seen_data = set()
    cohort = None
    for role, entry in entries:
        if not isinstance(entry, dict) or any(not isinstance(entry.get(k), str) or not entry[k].strip() for k in ('csv','metadata')):
            raise ValueError('Each trial needs csv and metadata paths')
        csv_path, meta_path = ((manifest_path.parent/entry[k]).resolve() for k in ('csv','metadata'))
        intake = validate_trial(csv_path, meta_path, perform_fit=(role=='fit'))
        digest = intake['source_sha256']['csv']
        if digest in seen_data:
            raise ValueError('Duplicate fitting/validation CSV data; separate trials required')
        seen_data.add(digest)
        meta = intake['metadata']
        signature = (meta['servo_id'], meta['joint_index'], meta['data_kind'])
        if cohort is None: cohort = signature
        if signature != cohort:
            raise ValueError('Trials must match servo identity, joint and physical/synthetic data kind')
        input_hashes[str(csv_path)] = digest
        input_hashes[str(meta_path)] = intake['source_sha256']['metadata']
        for name, evidence_hash in intake['source_sha256']['evidence'].items():
            evidence_path = (meta_path.parent/name).resolve()
            input_hashes[str(evidence_path)] = evidence_hash
            evidence_uses.setdefault(evidence_hash, []).append({'trial': role, 'file': str(evidence_path)})
        # The intake already checked exact columns, finite values and isolated step.
        with csv_path.open(newline='') as f:
            values = np.asarray([[float(row[k]) for k in COLUMNS] for row in csv.DictReader(f)])
        trials.append({'role': role, 'csv': str(csv_path), 'metadata': str(meta_path),
                       'intake': intake, 'values': values})
    parameters = dict(trials[0]['intake']['first_order_fit'])
    source_hashes = {n: sha(ROOT/n) for n in (
        'tools/review_responses.py','tools/validate_measurement.py','tools/fit_response.py',
        'requirements.txt','requirements-dev.txt')}
    result = {'version': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
              'state': 'diagnostic_awaiting_human_review', 'data_kind': cohort[2],
              'servo_id': cohort[0], 'joint_index': cohort[1],
              'physically_verified': False, 'calibration_validated': False,
              'model_updated': False, 'trial_independence_verified': False,
              'fit_parameters': parameters, 'fit_trial_role': 'fit',
              'validation_parameters_refitted': False, 'trials': [],
              'shared_evidence_files': [uses for uses in evidence_uses.values() if len({u['trial'] for u in uses}) > 1],
              'input_sha256': input_hashes, 'source_sha256': source_hashes,
              'project_configuration_reference': configuration_identity(),
              'limits': ['A first-order diagnostic cannot identify sustainable torque, backlash or MuJoCo gains uniquely.',
                         'Validation parameters are locked; only command timing and pre-step angle baseline come from each trial.',
                         'Distinct CSV hashes do not prove independent physical trials; review source recordings and alignment.',
                         'Shared evidence and voltage/load differences require human review; trials are never pooled.',
                         'Uncertainty is declared measurement uncertainty, not an inferred statistical confidence interval.',
                         'No automatic acceptance threshold, calibration, physical parameter or gate update.']}
    # Hashes must describe the bytes used, including evidence read during intake.
    def verify_inputs():
        for path, expected in input_hashes.items():
            if sha(path) != expected: raise ValueError('Input changed during review: '+path)
        for name, expected in source_hashes.items():
            if sha(ROOT/name) != expected: raise ValueError('Review source changed during execution: '+name)
    verify_inputs()
    output.mkdir(parents=True, exist_ok=False)
    try:
        fit_intake = trials[0]['intake']
        for trial in trials:
            role, values, intake = trial['role'], trial['values'], trial['intake']
            pred, baseline = predict_response(values, parameters)
            metrics = error_metrics(values, pred, baseline['step_index'])
            uncertainty = intake['metadata']['angle_uncertainty_rad']
            metrics['rmse_over_declared_uncertainty'] = metrics['rmse_rad']/uncertainty
            prediction_file, plot_file = role+'_prediction.csv', role+'.png'
            with (output/prediction_file).open('x', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['time_s','target_rad','measured_angle_rad','predicted_angle_rad',
                                 'residual_rad','voltage_v','load_nm'])
                writer.writerows(zip(values[:,0], values[:,1], values[:,2], pred,
                                     values[:,2]-pred, values[:,3], values[:,4]))
            plot_trial(values, pred, uncertainty, role, cohort[2], output/plot_file)
            differences = {key: {'fit': fit_intake[key], 'trial': intake[key],
                                 'differs_from_fit': intake[key] != fit_intake[key]}
                           for key in ('voltage_range_v','load_range_nm')}
            result['trials'].append({'role': role, 'csv': trial['csv'], 'metadata': trial['metadata'],
                                     'baseline': baseline, 'metrics': metrics,
                                     'angle_uncertainty_rad': uncertainty,
                                     'conditions': differences, 'intake': intake,
                                     'prediction_csv': prediction_file, 'plot_png': plot_file})
        result['intake_quality_flags_present'] = any(t['intake']['quality_flags'] for t in result['trials'])
        lines = ['# Servo-response diagnostic — awaiting human review', '',
                 f"Data kind: **{cohort[2]}**. No physical verification or calibration approval.", '',
                 'One fitting trial supplies the parameters below. Validation trials are never fitted.', '',
                 f"Delay {parameters['delay_s']:.6g}s; time constant {parameters['time_constant_s']:.6g}s; "
                 f"gain {parameters['step_gain']:.6g}.", '',
                 '| Trial | RMSE (deg) | Max error (deg) | Declared uncertainty (deg) | RMSE / uncertainty |',
                 '|---|---:|---:|---:|---:|']
        for t in result['trials']:
            m = t['metrics']
            lines.append(f"| {t['role']} | {m['rmse_deg']:.4g} | {m['max_abs_error_deg']:.4g} | "
                         f"{np.rad2deg(t['angle_uncertainty_rad']):.4g} | {m['rmse_over_declared_uncertainty']:.4g} |")
        for t in result['trials']:
            flags = ', '.join(t['intake']['quality_flags']) or 'none in performed screens'
            changed = ', '.join(k for k,v in t['conditions'].items() if v['differs_from_fit']) or 'none'
            lines += ['', f"## {t['role']}", '', f"Intake flags: {flags}. Condition differences: {changed}.",
                      f"Voltage {t['intake']['voltage_range_v']}V; load {t['intake']['load_range_nm']}N·m.",
                      f"![Response and residual]({t['plot_png']})", '', f"[Prediction/residual CSV]({t['prediction_csv']})"]
        lines += ['', f"Shared evidence groups: {len(result['shared_evidence_files'])}; details and hashes in [report.json](report.json).", '',
                  'Residual = measured minus predicted. Validation baseline uses only pre-step samples.',
                  'No automated goodness threshold: a generated report is not proof of an adequate model.',
                  'Validation no-fit intake omits gain/search-boundary/fit-residual screens; predictions above use the locked fitting parameters.',
                  'Declared uncertainty is not a confidence interval. Review raw recordings, time alignment, conditions and independence.',
                  'Never infer shaft angles from acknowledgements or infer sustainable torque/MuJoCo gains from this fit.', '']
        (output/'report.md').write_text('\n'.join(lines))
        verify_inputs()
        artifact_names = ['report.md'] + [t[k] for t in result['trials'] for k in ('prediction_csv','plot_png')]
        result['artifact_sha256'] = {n: sha(output/n) for n in artifact_names}
        (output/'report.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
        return result
    except BaseException as error:
        (output/'failure.json').write_text(json.dumps({'state': 'failed_diagnostic_generation',
            'error': type(error).__name__+': '+str(error), 'physically_verified': False,
            'calibration_validated': False, 'input_sha256': input_hashes,
            'source_sha256': source_hashes}, indent=2)+'\n')
        raise


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    result = review(args.manifest, args.output)
    print(json.dumps({k: result[k] for k in ('state','data_kind','physically_verified','calibration_validated')}))
    return 2 if result['intake_quality_flags_present'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
