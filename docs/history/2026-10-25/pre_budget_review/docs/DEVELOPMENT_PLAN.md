# Detailed continuation plan

Updated 2026-10-24. Read SUMMARY.md for the priced shopping list and assembly
overview; STATUS.md records evidence. This plan orders the work without clearing
procurement, manufacturing, further training or physical deployment.

## Starting checkpoint

- **Implemented:** seven-part PETG frame, two-part fit sample, drawings and quotation
  ZIPs; provisional r2 MuJoCo twin; shared control/IMU interface, firmware sources,
  PPO/evaluation, calibration and experiment tools.
- **Locally verified:**55tests; frozen script gives4qualifying steps/6.60cm in30s,
  below walking acceptance.29one-factor probes per legacy/corrected configuration;
  73corrected credited steps independently checked. Earlier30s neutral standing and
  2048-step smoke/reload are historical; no learned walking or new PPO.
- **Estimated:** 197.1 g solid-CAD total mass, actuator dynamics, friction, mounting
  dimensions and print strength. No physical measurements exist.
- **Blocked:** EUR105.34 priced parts/delivery before printing/sample/horn extras;
  exact quote and physical fit missing. No purchases, uploads or supplier messages.

## 1. Diagnose the reference — local diagnostics complete, measured gate blocked

**Purpose:** establish whether target poses can lift a foot while supporting the
COM, and distinguish ideal kinematics from actual servo/contact behaviour. More
PPO cannot answer that question reliably.

- Add an offline diagnostic that anchors either stance foot at the pad plane,
  computes full-foot clearance, COM/support margin and gravity torque by virtual
  work. Use the current model and safe limits; do not strengthen actuators.
- Replay the existing three bounded reference profiles, recording load split,
  contact footprint, COM margin, joint tracking and torque utilization.
- Check a finite, documented set of stance/swing poses. A sampled feasible pose
  is only a candidate; absence in a finite set is not an impossibility proof.
- Save CSV/JSON, plot, source snapshot and hashes in a new validation directory.

**Files:** tools/analyze_support.py, tests/test_support_analysis.py, validation
record and status. **Done:** reproducible diagnosis with stated limitations and
one evidence-based next mechanical/control question. **Blocks:** reference-gait
approval and substantial training. Static clearance alone never proves gait.

**Implemented and locally checked in this continuation:**154poses, three original
profile replays, four prepared holds, and two bounded HOME transition probes
(tools/transfer_reference.py). Mirrored20° prepared holds retain>=25mm clearance
for3s; both HOME transition orders still produce zero qualifying steps. See
[diagnosis](SUPPORT_DIAGNOSIS.md). The next question at that checkpoint was reaching single
support while preventing stance-foot rocking, with the current limits and measured
plant. No geometry, gain, torque or policy fingerprint changed; no PPO steps added.

**Further local development:** stance-crouch preparation followed by swapping leg
extension now gives one qualifying step from HOME, mirrored on either side. An
independent raw2ms audit confirms112ms whole-foot clearance>=3mm,22.36mm touchdown
advance and2.33mm stance motion. Zero alternations; only3.33mm body advance.
See [one-step checkpoint](STANCE_TRANSFER.md). This led to first-swing clearance
and phase/foot-placement tests before the alternating motion below.

**Previous continuation:** timing study plus weight handoff gives four alternating
nominal steps and6.60cm torso advance/30s; mirrored replay agrees. Five randomized
draws give0–1steps under the historical environment. See [scripted baseline](REFERENCE_GAIT.md).
Nominal tuning was frozen for parameter isolation below. Budget, sample fit and
real response/friction measurements remain blocked. No extra PPO or gate release.

**Completed follow-up:** [SENSITIVITY.md](SENSITIVITY.md) isolates29declared cases,
then repeats them after fixing clipped shaft-zero errors at safe command bounds.
Offsets now enter affine actuator bias; nominal trajectories/commands are unchanged.
55tests pass. Current identity begins`b11ab929`; all existing checkpoints/UF2are
historical. Torso mass, friction, damping and each tested±1° joint offset can remove
qualifying steps. These are calibration priorities, not measured tolerances.
**Next:** preserve this baseline; analyse genuine measured data when available.
Continue verified basket/delivery consolidation independently. Do not tune unknown
physics, raise torque or spend additional training steps to hide missing evidence.

## 2. Close the complete delivered budget and interfaces — AI + user/supplier

- Start from procurement.json; do not treat old printing prices as current quotes.
  Current known shortfall is **at least EUR5.34**, plus every unknown cost.
- Verify stock for six exact servos, supplied horns/shaft screws, ear geometry,
  horn hole pattern, horn-to-frame screw thread/length and branch connector ratings.
- Seek savings through verified complete deliveries/consumable consolidation;
  preserve six joints, actuator capability, replaceability and electrical safety.
- Obtain separate exact-file sample and frame quotes: PETG, finishing, usable
  holes, support removal, VAT, packaging and delivery to25337. Account for staged
  shipping. No TPU soles, printer, filament pack or USB adapter.
- External CAD upload to Meltlab remains subject to specific provider/payload
  authorization following the prior automatic-review rejection. Alternatively,
  user uploads the quotation ZIPs and returns itemized quotes/settings/file hashes.

**Files:** procurement.json, docs/PROCUREMENT_ACTIONS.md, SUMMARY.md.
**Done:** complete sourced <=EUR100 delivered basket, or precise unresolved costs
and shortfall with procurement still blocked. **Blocks:** any purchase or print
release. The existing basket is not affordable merely because prints are unpriced.

## 3. Bench one real servo and IMU; qualify the mounting sample — user + AI

- After budget clearance, inspect exact supplied hardware and measure interfaces
  before obtaining the fit sample. Failed fit requires CAD revision/requotation.
- Solder Pico/IMU headers and insulated power harness; servo current bypasses Pico.
  Verify polarity, common ground, PSU droop/current, branch connections, physical
  disconnect, USB data and3.3V PWM compatibility.
- Build current firmware; test disarmed startup, packet rejection, STOP and100ms
  watchdog in single-channel mode. No policy arming with example calibration.
- Measure pulse mapping/direction/range, offsets, unloaded and loaded response,
  command latency, backlash and approximate usable torque without prolonged stall.
  Record stationary IMU bias/noise/alignment. Test two sample pieces without drilling.

**Files:** firmware/, bench.py, calibrations/, dated raw CSV/video/measurement
records. Procedures: HARDWARE.md, CALIBRATION.md, cad/ASSEMBLY.md.
**Done:** measured interface fit and bench records, validated per-channel calibration,
physical cutoff/watchdog tests. **Blocks:** full frame and policy transfer.

## 4. Freeze the assembly and measured twin — AI + user

- Resolve diagnostic findings from task1 against measurements; propose any required
  geometry change explicitly. Recheck torque margin rather than inflating model strength.
- Regenerate CAD/model from physical_spec.json; check case/board/fastener/tool/cable
  sweeps and support geometry. Unknown interfaces must still fail manufacturing checks.
- Obtain the approved full frame; assemble, weigh components and complete rigid bodies
  without assigning mass twice. Record pad locations/adhesion/friction and tether effects.
- Fit actuator response/delay/strength/damping; update pulse quantization and IMU model.
  Record evidence/state/date; keep estimates where COM/inertia cannot be measured.
- Generate new model/control/calibration fingerprints; preserve incompatible policies
  as historical. Verify all joint signs, limits, manual standing and lifted reference.

**Files:** physical_spec.json, build_model.py, CAD, calibration, robot_config.py,
model/control sources when justified, firmware generated configuration.
**Done:** reproducible model/accounting/clearance tests plus measured fit/plant and
reviewed lifted-step evidence. **Blocks:** substantial training and physical policy use.

## 5. Conduct bounded fixed-versus-randomized experiments — AI

- Reuse the established smoke evidence; do not add steps automatically. If a changed
  configuration requires another smoke, explicitly record the new run/budget first.
- Once the stage gates pass: <=50000-step nominal pilot; final A/B seeds0,1,2 at
  equal budgets <=1000000 each, rounded down to1024-step PPO rollouts. An unchanged
  pilot counts toward its final run. No nominal pretraining advantage for B.
- Match initial A/B weights. Validation2000–2004 selects success, gait distance,
  reward in that order; reserve1000–1009 for final testing. Include HOME/untrained
  baselines and nominal/randomized evaluation for every policy.
- Save manifests, hashes, actual steps, CSV, aggregate metrics and reviewed videos.
  Report sliding, toe rocking, stationary lifts and falls separately.

**Files:** train.py, evaluate.py, tools/experiments.py, new run directories.
**Done:** equal-budget reproducible results or honest failure at the cap. Acceptance:
30s stand, then >=0.3m qualifying alternating walking within30s, whole-foot lift
>=3mm for>=40ms, non-sliding touchdown progress. **Blocks:** learned walking claim.

## 6. Supervised transfer and school experiment — user + AI

- Verify compatible fingerprints/calibration, cutoff/watchdog and conservative limits.
  Begin standing; progress to short steps only after safe manual/bench tests.
- Use a low clear area, thin protective surface and optional slack line. Support the
  tether externally without lifting/pushing the robot; record its influence.
- Alternate fixed/DR trial order with equal conditions, limits and trial budgets.
  Measure distance and foot motion using video/ruler; log timestamped IMU/commands.
  Do not infer travel through double integration of the MPU6050.
- Produce the school report: question, design/budget, method, A/B tables, videos,
  failures, cable effects and limitations. Turning/recovery/terrain wait for walking.

**Files:** dated physical trial records, docs/EXPERIMENT.md and school report.
**Done:** actual physical results with provenance; success is optional, honest
reporting is mandatory. Simulated evidence cannot complete this task.

## Continuation rules and commands

AI may implement diagnostics, tests and data-analysis preparation while human tasks
are pending. Keep gates false until their evidence exists. Update STATUS/SUMMARY
after each completed chunk, preserve historical runs, regenerate handoff/archive.

```bash
.venv/bin/python -m pytest -q
.venv/bin/python tools/analyze_support.py --output runs/support_diagnosis_NEW
.venv/bin/python tools/budget_gate.py  # expected1 until known shortfall resolved
.venv/bin/python tools/check_clearance.py  # expected1 while interfaces unknown
.venv/bin/python tools/build_handoff.py
.venv/bin/python tools/package_project.py
```
