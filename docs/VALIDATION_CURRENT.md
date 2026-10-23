# Local verification record —2026-10-23

Everything below is **locally executed software/compiler/simulation**, never a
physical result. No procurement, manufacturing, electrical timing or robot trial
was completed. Historical record: VALIDATION.md; current artifacts: validation/2026-10-23/.

## Checks

- `python -m pytest -q`:29passed (8.49s in recorded run).
- `UV_CACHE_DIR=/tmp/robot-uv-cache uv pip check --python .venv/bin/python`:
 49packages, compatible. Python3.12.3; exact top-level pins in requirements files.
- Seven CAD meshes have ledger-matching solid-PETG masses; total199.431g estimated.
  Aggregate inertia tensors positive and satisfy principal-inertia triangle inequalities.
- MJCF compilation, axes, servo ownership, reset contacts,30s neutral standing,
  randomized/limit command finiteness, Gym/SB3 semantics, seeded reset restoration pass.
- Five-frame90value observations use only estimated gravity/raw gyro/applied command
  and previous action. Privileged-state mutation does not change assembled observations.
- Delay samples reach both20/40ms; masses and inertias restore and scale together.
  PWM1µs safe rounding and measured-gain arithmetic tested with synthetic calibration.
- Progress reward regression: closed motion cycles cannot gain positive progress;
  backward motion is fully charged. Synthetic false-gait cases fail acceptance.
- Host framing/CRC/handshake/stale telemetry and native C++ controller tests pass.
  Native C++ tests with synthetically valid calibration remain test-only, never flashed.
- Official Pico SDK2.3.1 / Arm GNU14.2.Rel1 builds firmware ELF/bin. Official picotool
 2.3.1 converts UF2. Saved `final_control_revision/bench_invalid.uf2` **cannot policy-arm**; no flashing tested.
- Formal training/experiment commands reject all five uncleared gates. Invalid-calibration
  deployment fails before opening the requested serial port. No automatic arming occurs.

Expanded finite clearance command exited1 as intended:550fastener-proxy intersections
across55poses, zero non-fastener frame/case/electronics conflicts in those samples.
These are conservative unmeasured fastener mass-envelope proxies, not actual bolt models.
Manufacturing remains blocked. The previous checker silently omitted these categories.
Continuous sweeps, horns/ears/lead exits and assembly stiffness still need actual fit.

## Bounded training

| Run | Actual steps | Initialization / role |
|---|---:|---|
| final_smoke A0 |2048|Fresh seed0, current configuration|
| pilot_A0 |49152total|Resumes A0;2048included; rounds50000down; selected checkpoint10240|
| smoke_B0 |2048|Fresh randomized seed0, identical initial weights to A0|

Initial policy hash for both conditions:
`7efc1058e8b776f6de8d40b9d9359d2ce96bbefff09272d15dc673690ce166d9`.
Archived training configuration hash:
`1641779be26172bcb40bd2b94d93a0974f722a676ba6aa2249ec310a8dbf7a1f`.
The final ARM timestamp parser fix changes current controller identity to
`3d93f768188c8c55c903658192be75b87124f9a62852720fb5d2fd5b54666a8a`.
Archived policies are deliberately incompatible with the current controller; no
automatic migration/override was added. Exact-source isolated replay was locally
executed (seed2000:0.0085637m,30s,no fall,no gait). Current firmware was rebuilt;
model physics/preprocessing are unchanged. New training is required for a current
identity policy, and measured calibration remains required before deployment.

Manifests include model hashes, actual steps, source hashes, full randomization and
algorithm settings. TensorBoard/events and monitor CSVs are retained. Resume reload
worked; exact interrupted-vs-uninterrupted RNG equivalence is not claimed.

All validation checkpoints scored zero walking successes and zero gait distance.
Selection used seeds2000–2004 only.1000–1009 remains reserved for the future final
experiment. No formal six-run A/B comparison was started and no extra budget authorized.
The intermediate `runs/.../smoke` predates a source revision and is not a current model.

## Five validation episodes per row, seeds2000–2004

| Policy / environment | Mean body distance m | Mean reward | Falls | Qualifying gait m / success |
|---|---:|---:|---:|---|
| Home / nominal |0.0000271|6.00001|0/5|0 /0of5|
| Untrained / nominal |−0.025824|5.08423|0/5|0 /0of5|
|2048 A / nominal |−0.019874|5.46253|0/5|0 /0of5|
|2048 B / nominal |−0.020396|5.37745|0/5|0 /0of5|
| Selected A pilot / nominal |0.008577|6.03602|0/5|0 /0of5|
| Selected A pilot / randomized |0.008673|6.03637|0/5|0 /0of5|

All episodes lasted30s. Complete nominal/randomized rows for all policies are in
`validation/2026-10-23/aggregate.csv` and each experiment's episodes.csv/summary.json.
This shows stationary/sliding drift, **not walking**. The longer nominal pilot must
not be compared with the shorter B smoke as a claim about randomization efficacy.

Scripted reference variants completed46s including30s standing, but whole-foot
clearance stayed far below3mm; zero qualified steps. Counter-rotating hip/knee
keeps the intended foot pitch level kinematically, but did not produce a supported
lift dynamically; reversing the lean sign also failed. Joint trajectories, targets,
clearances and failures are saved rather than declaring the reference gate passed.
No force gains or torque cap were increased to force success.

Three MP4s (pilot nominal/randomized, B-smoke randomized) are30s,640×480,50fps,H264.
Representative rendered frames and updated exploded assembly envelopes were visually
inspected. The image/video shows posture, not independent evidence of successful gait.

## Reproduce/review

```bash
python -m pytest -q
python tools/replay_snapshot.py --episodes 5 --output runs/review_archived
# New current-identity smoke, only when a fresh development run is desired:
python train.py --steps 2048 --development --output runs/new_current_smoke
```

Use new output directories. Source snapshots include the visual STLs; the replay tool runs them in an
isolated temporary directory and never grants current hardware compatibility. `manifest.json` hashes evidence files. The source archive excludes
credentials, hidden agent configuration, virtualenvs, toolchains and run scratch.
Next evidence needed is the delivered quote/interface sample and real bench data;
no software check can mark those physically verified.
