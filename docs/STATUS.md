# Current project status — 2026-10-24

Read SUMMARY.md → AGENTS.md → relevant roadmap stage. **Nothing bought, printed,
assembled, flashed or physically verified.** Frame revision **S6-PETG-pad-r2**;
active route is outsourced PETG, bare Pico and eight ordinary grip pads.

| Stage | State | Evidence / blocker |
|---|---|---|
| Requirements / AI entry | implemented | Six joints,15–20cm,PC/USB,wired power,EUR100; no printer purchase |
| Hardware research / budget | blocked | Priced basket105.34EUR BEFORE print/sample/horn extras; known shortfall≥5.34EUR. Complete total unknown; dated ledger, not live checkout |
| CAD / quotation package | implemented, locally verified partial | Seven connected watertight frames, two-piece fit sample, drawings/manifests;0modeled collisions/55poses,5unknown interface groups; NOT manufacturing-approved |
| Shared control / firmware | locally verified partial | Protocol/native C++tests pass; regenerated current header has invalid calibration. All prior ARM/UF2images historical; physical timing absent |
| Provisional twin / Gym | locally verified | Estimated197.053g; matching barePico/pad ownership; no fake mechanical stops or privileged policy inputs;55tests pass |
| Frozen scripted reference | locally verified partial | Four qualifying steps/3alternations,6.60cm torso and4.39cm gait distance in30s;30cm target fails.29one-factor cases show fragile guessed physics |
| PPO / evaluation | historical local evidence | Prior2048-step smoke/reload:0walking successes/0gait. All saved policies now incompatible; no new PPO. Older49152-step pilot also failed |
| Physical build / calibration / transfer | planned, blocked | No hardware/measurements. Bench, soldering, fit and measurement procedures prepared |
| Formal A/B / school experiment | planned, blocked | No full current six-run experiment or physical trials; fixed seeds/budgets retained |
| Extensions | planned | After stable walking |

## Current architecture and identity

Six Waveshare15024MG90S; Lhip/knee pitch/ankle roll, then Rsame.50Hz directPicoPWM
and PC commands,200Hz MPU6050 processing,2ms MuJoCo. Separate USB logic and5V/5A
servo bus, common ground, self-soldered replaceable harness. Seven PETG frames,
four bought10×3mm pads per90×45mm foot; no PCA9685, printer/spool or TPU soles.

Policy:90values from five frames of estimated IMU gravity/gyro, acknowledged
applied targets and previous actions. No true orientation, translation, velocity,
shaft feedback, contact or force. Diagnostics/rewards may use simulation truth.
Safe commands are not measured mechanical limits; real stops remain unknown.

Current configuration:
`b11ab9292c586ace4f2028c7061aa4ef279b6c84bd3966d2e806e0f96d01560b`.
[Current frozen registry](baselines/scripted_r2_offset_corrected.json);
[historical predecessor](baselines/scripted_r2.json), identity`4d3b0dcb…`.
**All saved policy checkpoints and UF2images are historical/incompatible**, including
r2 smoke. Never relabel them. Current invalid header needs an ARM rebuild and
measured calibration before physical policy operation; native tests are not an
ARM build, electrical test or fit approval.

## Latest completed work

[Full report](SENSITIVITY.md), [current validation](VALIDATION_CURRENT.md).

- Frozen compact sequence: nominal30s metrics exactly match predecessor, four
  qualifying steps,3alternations,0.066021479m torso/0.043929229m gait, no fall;
  **not learned walking, not30cm acceptance**. Reference has no HOME return.
-29one-factor cases under each identity; no target tuning/PPO. Torso-body mass±5%
  gives0/1steps, friction±15% gives4/0, damping±20% gives2/3. Every individual±1°
  offset gives1–3steps. These are unmeasured endpoint hypotheses, not failure rates.
- Found/fixed clipping of unknown shaft-zero error at safe command bounds.
  Offset now enters affine actuator bias; command/ack bounds, nominal strength,
  observations and geometry are unchanged. Nominal bias restored every reset.
- All17non-offset cases exactly preserve previous physics. IMU-noise control
  changes observations but not this open-loop motion; target-slew probes are inactive
  here. This does not establish feedback-policy robustness or sensor irrelevance.
- Independent raw2ms audit validates all73credited steps in the corrected study;
  none meets project walking acceptance. CSV/plot/source/trace hashes preserved.
- **55pytest cases pass in14.93s**: `validation/2026-10-24/offset_correction/pytest.txt`.
  Includes force at both command bounds for each joint, repeated reset restoration,
  command clipping, one-factor isolation and observation/physics separation.
- Historical mixed-DR script draws42–46 give1,1,1,1,0steps; retain their old identity.
  Earlier37/41/45/49-test records, movies, snapshots and policies remain historical.

All physical parameters remain sourced/estimated/unknown, not measured. Solid-CAD
mass,0.08Nm torque hypothesis, friction and response need measurements. Static HOME
single-support torque~0.0657Nm;2×margin exceeds0.08Nm. No strength inflation to
force gait.0modeled collisions does not resolve horns, screws, wires or print strength.
All five [release gates](gates.json) remain false. Software STOP is not power isolation.

## Exact next task

**AI:** keep the script frozen; use SENSITIVITY.md to prepare/inspect genuine
calibration records when available. Check external angle provenance, per-servo
zero/gain/backlash/loaded response, assembled body masses/COM and pad friction.
Independent executable work: verify complete-basket delivery/consumable consolidation
against procurement.json; no hidden free costs, weaker servos or new fabrication.
Do not tune guessed physics, relax acceptance, raise torque or add PPO steps.

**Human-dependent:** obtain a complete affordable exact-file quote and actual
servo/horn/ear/screw measurements, then mounting sample fit and bench data. The
previous Meltlab upload was blocked by automatic approval review because specific
provider/payload sharing authorization was absent. No upload/message/order occurred.
Use a user-returned quote or specific authorization before sharing the files;
public example/old-geometry prices do not count. Every finishing/sample/delivery
charge remains required. Do not purchase while the budget/fit gates fail.

After real evidence: update/version the measured twin → replay frozen reference →
validate lifted stepping → bounded fixed/DR training → supervised transfer/equal trials.
See DEVELOPMENT_PLAN.md for owners/dependencies and CALIBRATION.md for measurements.

```bash
.venv/bin/python -m pytest -q
.venv/bin/python tools/budget_gate.py # expected1:105.34before prints
.venv/bin/python tools/check_clearance.py # expected1:unknown interfaces
MPLCONFIGDIR=/tmp/s6-mpl .venv/bin/python tools/sensitivity_probe.py --cases nominal --output runs/sensitivity_NEW
```
