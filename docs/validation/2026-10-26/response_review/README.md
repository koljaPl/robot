# Servo-response review evidence — 2026-10-26

**Local synthetic diagnostics only; no measured calibration or physical result.**

- **186tests passed in16.80s**: [full log](pytest_final.txt).
- **32focused tests passed in2.10s**: [focused log](pytest_focused_final.txt).
  Earlier29/184-test checkpoints remain in their own records.
- [Final report](final_report/report.md), [JSON](final_report/report.json),
  [matching prediction/residual plot](final_report/validation_01.png),
  [mismatched prediction/residual plot](final_report/validation_02.png).
- [Synthetic inputs and manifest](synthetic_inputs/review.json),
  [generation details](synthetic_inputs/generation.json),
  [standalone no-fit CLI result](validation_intake_no_fit.json).
- [Aggregate evidence/source hashes](summary.json); source snapshot in `source/`.
  [Usage and limitations](../../../RESPONSE_REVIEW.md).

The actual demo CLI ran offline. One fitting trial selected delay0.03s,
first-order time constant0.10156695s and gain0.95127897. A separate matching negative
step has0.01460098degRMSE; an intentionally slower/lower-gain step with changed
condition labels has2.82882516degRMSE. Every input/condition/uncertainty is synthetic,
not a measured MG90S specification. The same parameters predict both validation
trials, using only each trial's command timing and pre-step observed baseline.

Tests prove a single fitter call on fitting data, no validation refit, and unchanged
fit/prediction when validation post-step angles change. Exact historical default
intake output is preserved. Additional tests cover byte/reformatted/numerical copied
trajectories, changed condition labels, input/provenance/unit/evidence mismatch,
negative/positive responses, metrics, actual PNG files, hashes and failed output.
Claimed physical metadata still never becomes physically verified calibration.

Plots were visually inspected; artifact/source hashes checked. Shared generation
metadata is reported, not concealed or treated as proof of independent experiments.
The earlier `synthetic_report/` records the first byte-only duplicate-check version;
`final_report/` adds numerical-trajectory duplicate checks with identical fit/metrics.
No historical report was overwritten. Preliminary source bytes are retained under
`preliminary_source/` and match every recorded source hash (use an isolated project
copy to replay). Prior fitter/intake/guide sources are retained
in [history](../../../history/2026-10-26/pre_response_review/tools/validate_measurement.py).

All fingerprinted model/control/firmware files and the prepared ELF/UF2 remain
unchanged. No simulation replay/tuning, hardware access, policy training, procurement
or physical gate change. Orders/arrival/costs remain unknown until supplied.
Next: receive parts, fit samples and obtain reviewed external-angle/bench records.
