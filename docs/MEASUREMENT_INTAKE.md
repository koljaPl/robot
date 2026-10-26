# Step-response measurement intake — 2026-10-26

Implemented WP2 preparation, **not physical calibration**. The checker validates
data/provenance structure, hashes evidence and screens response quality before a
human reviews the original video. It never changes calibration, the model or gates.

1. Copy `docs/templates/step_response.csv` and
   `docs/templates/step_response_provenance.example.json` to a new trial directory.
2. Record `time_s,target_rad,angle_rad,voltage_v,load_nm` in that exact order.
   `angle_rad` must be externally observed, not the target or applied acknowledgement.
   Use at least20 finite samples, increasing timestamps, at least3before the step,
   at least10after and0.5s post-step duration. A single step must be at least5°.
   These are data-analysis requirements, not instructions to move an untested servo.
3. Fill servo identity, joint index0–5, SI units, clock alignment, measurement
   method, positive angle uncertainty and paths to original evidence relative to
   the sidecar. Physical records require external video/protractor/encoder evidence.
4. Run against fresh output (the tool refuses to overwrite an existing report):

```bash
.venv/bin/python tools/validate_measurement.py runs/trial_NEW/step.csv \
  --metadata runs/trial_NEW/provenance.json --output runs/trial_NEW/intake.json
```

Exit0 means ready for **human fit review**, not approved calibration. Exit2 flags
unresolved motion, direction, gain, fit-boundary/residual, overshoot or voltage
issues. Invalid schema/provenance is rejected. Original evidence must be reviewed:
a filename/hash or a claimed external source cannot prove truthful measurements.

Quality screens (gain0.5–1.5, residual relative to step/uncertainty, at least3×
uncertainty resolved motion, etc.) are explicit diagnostic hypotheses in the source,
not published servo tolerances. The first-order response fitter cannot uniquely
identify sustainable torque, backlash or MuJoCo kp/kv from one step. Use multiple
loads/amplitudes and held-out trajectories; retain raw data and uncertainty.

Synthetic examples must use `data_kind=synthetic` and remain synthetic in every
report. Even well-formed physical input returns `physically_verified=false` and
`calibration_validated=false`: only reviewed measurements complete physical gates.
No real trials exist yet. Manual-control tooling, measured-baseline parity and
Pico2 cross-build are now locally verified. [Initial bench preparation](BENCH.md)
previews without USB; raw command acknowledgements never replace external angles.
Next: actual fit/bench recordings and held-out measured-response review.
