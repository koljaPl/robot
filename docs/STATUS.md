# Current project status — 2026-10-26

**Design/printing selection COMPLETE by user2026-10-26.** Classmate printing is
accepted; exact price unknown/excluding delivery. Selected board now Pico2.
Next phase WP2 has begun; this is not physical/manufacturing/financial verification.
Separate print folder: [instructions](../print_for_classmate/00_START_HERE.md),
[ZIP](../print_for_classmate.zip). [Decision record](decisions/2026-10-26-printing-pico2.json).

Read SUMMARY.md → root PLAN.md → AGENTS.md → relevant roadmap stage.
**Ordering started—reported by user; exact items, quantities, paid prices and arrivals
unknown. No physical fit, assembly, firmware flash or calibration verified.** Frame revision **S6-PETG-pad-r2-pico2**;
active route is classmate PETG, bare Pico2 and eight ordinary grip pads.

| Stage | State | Evidence / blocker |
|---|---|---|
| Requirements / AI entry | implemented | Six joints,15–20cm,PC/USB,wired power,EUR100; no printer purchase |
| Design / printing selection | complete, user accepted | Classmate printing selected; Pico2 adopted. Price unknown; numerical budget remains separate/unverified (106.49before unknowns) |
| CAD / quotation package | implemented, locally verified partial | Seven connected watertight frames, two-piece fit sample, drawings/manifests;0modeled collisions/55poses,5unknown interface groups; NOT manufacturing-approved |
| Shared control / firmware | locally verified partial | Protocol/native tests and current Pico2 cross-build pass; invalid calibration, full-policy arm disabled. Older images historical; physical timing absent |
| Provisional twin / Gym | locally verified | Estimated197.053g; matching barePico/pad ownership; no fake mechanical stops or privileged policy inputs;latest full suite162passes |
| Frozen scripted reference | locally verified partial | Four qualifying steps/3alternations,6.60cm torso and4.39cm gait distance in30s;30cm target fails.29one-factor cases show fragile guessed physics |
| PPO / evaluation | historical local evidence | Prior2048-step smoke/reload:0walking successes/0gait. All saved policies now incompatible; no new PPO. Older49152-step pilot also failed |
| Physical build / calibration / transfer | planned, blocked | User ordering started; arrivals/measurements unreported. Bench/fit procedures prepared |
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
[Current frozen registry](baselines/scripted_bench_tools.json);
[historical predecessor](baselines/scripted_r2.json), identity`4d3b0dcb…`.
**All saved policy checkpoints and older UF2images are historical/incompatible**,
including r2 smoke. Current Pico2 preparation ELF/UF2 is locally cross-built with
invalid calibration; no physical test. Never relabel old images. Measured calibration
and reviewed physical checks remain required before policy operation.

## Initial bench preparation — latest completed work

- `bench.py` defaults to offline preview; USB needs explicit `--execute`. New session
  directories retain settings/source hashes, commands/status events, raw IMU and errors.
- Read-only logging or one constant restricted pulse; fresh stationary startup,
  fault/saturation/timestamp/deadline checks and STOP/close. No policy ARM or reconnect.
- Mode confirmation is not applied-pulse/shaft feedback. CLI migration and physical
  prerequisites: [bench guide](BENCH.md). Orders/measurements remain unknown.
-41focused mocked tests; **162tests passed in16.54s**. [Evidence](validation/2026-10-26/bench_preparation/README.md).
  Both CLI previews ran without USB; no geometry/identity/firmware/PPO/gate change.

## Pico2 preparation firmware — previous completed work

- Pinned SDK2.3.1/TinyUSB, Arm14.2.Rel1 and picotool2.3.1; official archive checksums
  verified before extraction. Toolchains live outside the project archive.
- File-only build utility rejects stale headers/wrong targets, logs failure/interruption
  and preserves old evidence. Current preparation calibration invalid; no full-policy arm.
- **121tests pass in18.02s**; physical operation remains pending.
- [Build procedure](../firmware/README.md), [evidence](validation/2026-10-26/pico2_crossbuild/README.md).
  No hardware USB/flash, PPO or change to model/control identity.

## Root plan and bench tools — previous completed work

- Full living plan moved to root [PLAN.md](../PLAN.md); old path is a pointer.
  Phase overview and dated progress come first; AI must update it after every
  completed task/change/failure/blocker before reporting completion.
- User ordering recorded separately from quoted prices; individual order data unknown.
- `manual_control.py`: offline preview by default; validated calibrated hardware
  requires explicit arm, matching handshake and fresh startup telemetry. Timed
  bounded/slew-checked commands, no catch-up bursts, final ACK, logs, STOP/close.
  Commands/acknowledgements are not shaft measurements. [Usage](MANUAL_CONTROL.md).
- HOME/untrained baselines now accept measured calibration; formal runner passes it
  everywhere; policy/explicit mismatch rejected. Mocked and short software tests only.
- **99tests pass in17.21s**, validation/2026-10-26/bench_tools/pytest_final.txt. No PPO,
  hardware operation, geometry/strength/observation change or physical gate release.
- New source-only frozen registry `scripted_bench_tools.json`; same685e3802model/
  control identity and exact nominal metrics. Previous source snapshots untouched.

## New2026-10-26 work

- Pico2 selected in ledger/spec; official same footprint/pins/MicroUSB confirmed.
  CMake defaults to pico2 and refuses pico; build target is now fingerprinted.
  At that earlier checkpoint SDK/compiler were absent; superseded by the local
  cross-build below. No electrical claim.
- Separate print-only folder/ZIP:7frame and2sample STL files, German instructions,
  drawings, hashes, quantities and dimensions; no fit approval.
- WP2 measurement intake/provenance/quality checker implemented. Eight focused
  intake tests and full69-test suite pass (16.52s); log:validation/2026-10-26/pico2/pytest.txt. Synthetic response
  never becomes measured calibration; commands/acknowledgements rejected as angles.
- New nominal reference replay exactly matches prior complete metrics:4steps,
  6.60cm torso/4.39cm gait in30s, no fall. No new PPO, strength or trajectory change.

## Previous completed work (historical identities/evidence)

[Full report](SENSITIVITY.md), [current validation](VALIDATION_CURRENT.md).

- 2026-10-25 planning refresh: [expanded execution plan](../PLAN.md)
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

**AI:** review actual receipt/arrival, fit-sample and one-servo/IMU bench records
when supplied; preserve provenance and keep gates closed until evidence passes.
Pico2 preparation build complete locally; no automatic flash/arm or extra PPO.
**Student/classmate:** receive/record exact ordered items, print/test2samples with
actual servo/horn/screws, then7frames if fit passes; bench, weigh and calibrate.
No numerical financial or physical gate is cleared by user agreement or software tests.
See root PLAN.md for full dependencies; do not restart provider-selection research
or motion tuning. Use `pytest -q tests`, not copied historical test modules.
