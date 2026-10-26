# Current project status — 2026-10-26

**Design/printing selection COMPLETE by user2026-10-26.** Classmate printing is
accepted; exact price unknown/excluding delivery. Selected board now Pico2.
Next phase WP2 has begun; this is not physical/manufacturing/financial verification.
Separate print folder: [instructions](../print_for_classmate/00_START_HERE.md),
[ZIP](../print_for_classmate.zip). [Decision record](decisions/2026-10-26-printing-pico2.json).

Read SUMMARY.md → AGENTS.md → relevant roadmap stage. **Nothing bought, printed,
assembled, flashed or physically verified.** Frame revision **S6-PETG-pad-r2-pico2**;
active route is classmate PETG, bare Pico2 and eight ordinary grip pads.

| Stage | State | Evidence / blocker |
|---|---|---|
| Requirements / AI entry | implemented | Six joints,15–20cm,PC/USB,wired power,EUR100; no printer purchase |
| Design / printing selection | complete, user accepted | Classmate printing selected; Pico2 adopted. Price unknown; numerical budget remains separate/unverified (106.49before unknowns) |
| CAD / quotation package | implemented, locally verified partial | Seven connected watertight frames, two-piece fit sample, drawings/manifests;0modeled collisions/55poses,5unknown interface groups; NOT manufacturing-approved |
| Shared control / firmware | locally verified partial | Protocol/native C++tests pass; regenerated current header has invalid calibration. All prior ARM/UF2images historical; physical timing absent |
| Provisional twin / Gym | locally verified | Estimated197.053g; matching barePico/pad ownership; no fake mechanical stops or privileged policy inputs;latest full suite69passes |
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
`685e3802999f8c9f72abbe119b17377380f9a41f13eeea32953432b17c153c88`.
[Current frozen registry](baselines/scripted_pico2.json);
[historical predecessor](baselines/scripted_r2.json), identity`4d3b0dcb…`.
**All saved policy checkpoints and UF2images are historical/incompatible**, including
r2 smoke. Never relabel them. Current invalid header needs an ARM rebuild and
measured calibration before physical policy operation; native tests are not an
ARM build, electrical test or fit approval.

## New2026-10-26 work

- Pico2 selected in ledger/spec; official same footprint/pins/MicroUSB confirmed.
  CMake defaults to pico2 and refuses pico; build target is now fingerprinted.
  SDK/cross compiler absent locally: no new ARM image or electrical claim.
- Separate print-only folder/ZIP:7frame and2sample STL files, German instructions,
  drawings, hashes, quantities and dimensions; no fit approval.
- WP2 measurement intake/provenance/quality checker implemented. Eight focused
  intake tests and full69-test suite pass (16.52s); log:validation/2026-10-26/pico2/pytest.txt. Synthetic response
  never becomes measured calibration; commands/acknowledgements rejected as angles.
- New nominal reference replay exactly matches prior complete metrics:4steps,
  6.60cm torso/4.39cm gait in30s, no fall. No new PPO, strength or trajectory change.

## Previous completed work (historical identities/evidence)

[Full report](SENSITIVITY.md), [current validation](VALIDATION_CURRENT.md).

- 2026-10-25 planning refresh: [expanded execution plan](DEVELOPMENT_PLAN.md)
  now maps all14phases and WP1–WP11, with owners, dependencies, procedures,
  files, acceptance evidence, failure decisions and conditional commands.
  No source/model/training/hardware change. Next independent implementation is
  WP2 measurement-intake validation; six-joint manual tooling is still planned.
- Planning inspection also found a remaining formal-evaluation gap: HOME/untrained
  baseline evaluation currently has no measured-calibration CLI input, unlike
  policy evaluation through metadata. WP2 must add/test parity before formal A/B;
  no evaluation implementation was changed by this planning edit.
- Latest recorded full suite: **58passed in16.41s**,
  `validation/2026-10-25/procurement_review/pytest_after_history_exclusion.txt`.
  This planning edit rechecked active collection (58tests), not full execution.
  Use `pytest -q tests` to avoid copied historical test-module collisions.

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

**AI:** finish reviewed six-joint manual utility and measured-baseline calibration
parity. Intake validation is implemented; use it on genuine data when available.
Do not repeat printing-service research or tune nominal physics/PPO.
**Student/classmate:** use the separate print folder, test2pieces first with actual
servo/horn/screws, then7frames. Record actual costs and fitted dimensions/masses;
physical stages remain pending. User decision is complete despite missing numeric
quote; no factual financial/fit gate has been changed to true.

Commands: `.venv/bin/python -m pytest -q tests`; see MEASUREMENT_INTAKE.md,
firmware/README.md, DEVELOPMENT_PLAN.md and the print-folder instructions.
