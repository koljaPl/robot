# Servo-response review — separate trials, locked fit

This is an **offline diagnostic**, never calibration approval or a MuJoCo parameter
update. The robot still needs actual fit, electrical and externally observed shaft
measurements. Current examples are synthetic; nothing here moves a motor.

## Try the synthetic demonstration now

```bash
.venv/bin/python tools/make_response_demo.py --output runs/response_inputs_NEW
MPLCONFIGDIR=/tmp/s6-response-mpl .venv/bin/python tools/review_responses.py \
  --manifest runs/response_inputs_NEW/review.json --output runs/response_report_NEW
```

Both directories must be new. The generator creates one fitting step, a matching
negative step and a deliberately slower/lower-gain step with changed voltage/load
labels. Every angle, uncertainty and condition is invented for testing the software;
none is a verified MG90S specification. Shared generation metadata is reported.

## Later, with actual external measurements

Use the existing [CSV/provenance requirements](MEASUREMENT_INTAKE.md). Each trial
needs its own CSV and metadata sidecar, matching servo identity/joint and the same
physical/synthetic data kind. Physical data requires original external evidence.
The [example manifest](templates/response_review.example.json) has this structure:

```json
{
  "version": 1,
  "fit_trial": {"csv": "fit_step.csv", "metadata": "fit_provenance.json"},
  "validation_trials": [
    {"csv": "other_step.csv", "metadata": "other_provenance.json"}
  ]
}
```

Paths are relative to the manifest (absolute paths also work). Select the fitting
trial before examining validation results. Duplicate CSV bytes, including renamed
copies, are rejected across all trials. Exact numerical time/target/angle copies
are also rejected after parsing, even with different formatting or voltage/load
labels. Different hashes alone cannot prove
independent physical trials. Shared source recordings are listed by content hash;
review clips/time windows manually. Conditions are reported separately, not pooled.

The tool calls the existing first-order fitter **only for fit_trial**. For each
validation step it predicts:

`q_pred = q_pre + gain × command_step × (1 − exp(−max(0, t − t_step − delay)/tau))`

Gain, delay and tau stay locked. Only recorded command timing, command amplitude
and the median externally observed **pre-step** angle come from each validation
trial. No post-step angle, time shift or parameter selection is fitted to validation
data. Record clock alignment honestly; do not silently realign traces to improve fit.

The intake API now accepts `perform_fit=False`, and its CLI accepts `--no-fit`.
Default results/fit behaviour are preserved. No-fit mode retains provenance/basic
motion/voltage checks but explicitly skips gain, search-boundary and fitted-residual
screens. It returns no first-order fit; this is not equivalent to full fit review.

The [initial bench logger](BENCH.md) provides raw IMU/command records and a constant
single-servo pulse. It does not supply measured shaft angles or create a complete
isolated step experiment. Use reviewed later measurement procedures and external
video/protractor/encoder evidence; never substitute command acknowledgements.

## Outputs and interpretation

- `report.json`: locked parameters, trial RMSE/MAE/maximum and post-step errors,
  uncertainty, voltage/load ranges and differences, shared evidence and source hashes.
- `report.md`: brief comparison and links to each plot/CSV.
- `fit_prediction.csv` / `validation_XX_prediction.csv`: target, external angle,
  prediction, measured-minus-predicted residual, voltage and load, in SI units.
- `fit.png` / `validation_XX.png`: angle traces and residuals with the declared
  uncertainty band. The band is not an inferred confidence interval.

Inputs are checked before creating output; an existing output is never overwritten.
A generation error after creation leaves `failure.json`; partial plots are not a
completed report. Original data/videos are not copied automatically. Keep them.

Exit0 means **report generated**, not adequate fit; the deliberately mismatched demo
can also return0. Exit2 means existing intake quality flags need review. Invalid
inputs fail. No new automatic prediction-error acceptance threshold is imposed.
Report state remains awaiting human review, including records labelled physical.
No physical-verification/calibration flag or project gate is set automatically.

Review errors against declared measurement uncertainty and repeatability, sample
rate, voltage/load changes, backlash, clock alignment and source evidence. One
first-order step cannot identify sustainable torque, friction or MuJoCo kp/kv
uniquely. Actual measured-twin changes require later reviewed multi-trial evidence,
versioned parameters and the existing hardware/training gates.
