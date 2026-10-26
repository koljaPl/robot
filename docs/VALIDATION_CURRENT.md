# Current local verification — 2026-10-26, S6-PETG-pad-r2

## Servo-response review — latest2026-10-26

- Locked first-order fit predicted separate synthetic trials without fitting validation
  data. Pre-step-only baseline, condition/shared-evidence reporting, CSV/PNG/JSON
  artifacts and source hashes verified. No automatic acceptance or calibration update.
- Default intake result exactly matches historical code; no-fit mode skips fitted
  screens explicitly. Byte/numerical duplicates, invalid provenance/units, missing
  evidence, wrong servo/joint/kind, NaNs and overwrite attempts tested.
-32focused tests; **186tests passed in16.80s**: [log](validation/2026-10-26/response_review/pytest_final.txt).
- [Evidence/plots](validation/2026-10-26/response_review/README.md), [guide](RESPONSE_REVIEW.md).
  Synthetic matching negative step~0.0146degRMSE versus mismatched step~2.8288deg;
  these are invented fixtures, never MG90S measurements.
- Fingerprinted core685e3802/current ELF/UF2/gates unchanged; no physical test/PPO.

## Initial bench preparation — previous2026-10-26

- Offline preview default, explicit `--execute` for USB, new session directories.
- Initial raw IMU or one constant bounded pulse; fresh stationary startup, fault/time/
  saturation checks, no catch-up bursts, STOP/close and visible cleanup failure.
- No policy ARM. Bench status and six-joint command acknowledgements are not
  applied-pulse or shaft feedback. This tool is not an assembled-robot controller.
-41focused mocked checks; **162tests passed in16.54s**: [log](validation/2026-10-26/bench_preparation/pytest.txt).
- Actual CLI previews completed offline. [Evidence](validation/2026-10-26/bench_preparation/README.md).
  Model/control685e3802, prepared ELF/UF2 and all five false gates unchanged. No PPO.

## Pico2 preparation cross-build — previous2026-10-26

- Current Pico2/RP2350 Arm secure preparation firmware locally compiled and inspected
  using pinned SDK2.3.1, TinyUSB commit86ad6e56, Arm14.2.Rel1 and picotool2.3.1.
- Builder is file-only and fail-closed for wrong board, stale header, missing/changed
  dependencies, target mismatch, corruption, source drift, timeout and interruption.
- **121tests passed in18.02s**: [final log](validation/2026-10-26/pico2_crossbuild/pytest_release.txt).
- [Build evidence and repeatability](validation/2026-10-26/pico2_crossbuild/README.md).
  Identity685e3802unchanged; invalid calibration and disarmed startup retained.
- No physical USB/flash, electrical timing, fit, measured calibration or PPO result.
  All five gates remain false; order details remain unknown.

## Root plan and bench-control/parity delivery — previous2026-10-26

- Root [PLAN.md](../PLAN.md) is authoritative, overview first. The prior path is
  a pointer; all completed chunks/changes/failures/blockers must update the plan.
- User reports ordering started; exact items/quantities/paid prices/arrivals unknown.
  Quoted basket retained separately. No purchases/messages performed by AI.
- Manual HOME-only CLI preview runs without USB. Hardware mode needs explicit arm,
  measured calibration, matching handshake, fresh telemetry and reviewed start.
  Commands/slew/bounds, no catch-up bursts, final ACK, logging, STOP/close verified
  through mocked transport. Constructor-failure connection cleanup also tested.
- Evaluation now propagates the same measured calibration through HOME, untrained
  and policy paths; rejects mismatch. Formal orchestration propagation tested with
  mocked commands only; reserved test seeds were not actually evaluated.
- **99tests passed in17.21s**: [final log](validation/2026-10-26/bench_tools/pytest_final.txt).
  Earlier98-test and focused logs remain evidence for their respective checkpoints.
- New source-only [reference registry](baselines/scripted_bench_tools.json) keeps
  exact nominal metrics and the same685e3802configuration. Prior snapshots untouched.
  No robot geometry/strength/observation change, PPO training or physical gate release.
- Current manual/source/handoff/preview and delivery checks are under
  `validation/2026-10-26/bench_tools/`. Subsequent cross-build is recorded above; later
  student/classmate fit, bench, assembly, weights and actual calibration.

## Pico2 and classmate-printing continuation — 2026-10-26

Design/printing choice complete by user confirmation; printing price unknown.
This is decision evidence, not a numerical budget, actual fit or physical test.
Current spec revisionS6-PETG-pad-r2-pico2; fingerprint
`685e3802999f8c9f72abbe119b17377380f9a41f13eeea32953432b17c153c88`.

- Official same51×21mm footprint/pinout/MicroUSB; GPIO mapping retained. Board3g,
  populated envelope3.5mm and COM remain estimates; no mass borrowed from gross data.
- CMake pico2 default/wrong-board rejection; CMake now part of identity. Invalid
  generated header current. No installed SDK/cross compiler: no new ARM build/UF2.
- Separate classmate folder and ZIP checked:7frame STL files plus2sample STL files,
  1×each, connected/watertight, dimensions/hashes and German instructions/drawings.
  Template exists; actual servo/horn fit and printed layer strength still unknown.
- Measurement intake checker rejects target/ack/simulated-angle provenance, missing
  original evidence, bad units/nonfinite samples, and flags stuck/reversed response.
  Synthetic examples stay synthetic; no automatic calibration approval/gate change.
- **69tests pass in16.52s**, `validation/2026-10-26/pico2/pytest.txt`.
- New nominal replay exactly matches every predecessor metric:4steps,6.60cm torso/
  4.39cm qualifying gait distance/30s, no fall; still fails30cm walking target.
  [New frozen registry](baselines/scripted_pico2.json). No new PPO or retuned motion.

Current ledger subtotal€106.49 before printing/horn unknowns. The user accepts the
arrangement, not a fabricated numeric quote. Physical/financial gates remainfalse;
next phase WP2 continues despite incomplete accounting. Prior evidence below is
historical and must not be relabelled as this revision.

**Physical purchase/arrival details are unreported; user now reports ordering
started. No fit, electrical or deployment result is verified.**
Prior2026-10-23record is preserved under history/2026-10-24/pre_print_revision/docs/.
Latest evidence: `validation/2026-10-24/offset_correction/`,
`sensitivity_corrected/` and `sensitivity_report_final/`. The sections labelled
historical retain the configuration that actually produced them.

## 2026-10-25 documentation and procurement checkpoint

Latest recorded full suite: **58passed in16.41s**,
[log](validation/2026-10-25/procurement_review/pytest_after_history_exclusion.txt).
The earlier55-test offset result below remains valid historical evidence.
The expanded-plan refresh verified active collection (58tests), references,
ledger/fingerprint/gates and generated delivery; it did not rerun the full suite,
train, change physics, obtain a quote or perform any physical test.
Scope future collection to `pytest -q tests`: archived copies caused a previous
root-discovery import collision; both the failed and successful logs are retained.

Selected dated priced basket now€105.09 before printing/sample/horn extras,
minimum known shortfall€5.09; complete total unknown. See [budget review](BUDGET_REVIEW.md).
The€105.34 snapshot near the end belongs to the prior checkpoint, not current prices.

## Historical offset correction and frozen-script study

Current identity:
`b11ab9292c586ace4f2028c7061aa4ef279b6c84bd3966d2e806e0f96d01560b`.
See [SENSITIVITY.md](SENSITIVITY.md) for the actuator law, source documentation,
complete factor table, raw audit, limitations and replay commands.

- Unknown physical shaft-zero errors now enter affine actuator bias instead of
  being clipped away at safe command bounds. Acknowledged/control targets remain
  bounded. Repeated resets restore nominal bias; no fake mechanical stops added.
- Geometry, estimated197.053g mass, nominal strength/action/observation/thresholds
  and compact target sequence unchanged. Nominal results exactly match predecessor:
  four qualifying steps/three alternations,6.602cm torso/4.393cm gait in30s, no fall.
  This is open-loop scripted motion;30cm walking acceptance remains unmet.
-29one-factor cases per old/corrected identity, all raw/source hashes preserved.
  Corrected torso-only mass±5%:0/1steps; friction±15%:4/0; damping±20%:2/3;
  all12individual±1° joint offsets:1–3steps. All17zero-offset case trajectories
  exactly match their predecessors. IMU-noise and slew negative controls pass.
- All73credited steps in the corrected study independently pass existing raw2ms
  lift≥3mm/40ms, forward touchdown, stance-motion and opposite-support checks.
  All29episodes remain upright; zero walking successes. These endpoint hypotheses
  do not establish measured tolerances or a failure probability.
- **55tests passed in14.93s**, `offset_correction/pytest.txt`; includes native C++
  tests, Gym/SB3/provenance, reset restoration and offset force at command bounds.
- Generated invalid header carries the new hash, `CAL_VALID=false`; no new ARM
  build or electrical test. **All saved policies/UF2are historical/incompatible**,
  including the2048-step r2 smoke. No new PPO and no stage gate cleared.
- Geometry recheck again finds0modeled conflicts across55poses,5unknown fit
  groups. Trimesh emits COM warnings for498zero-volume intersection results;
  the recorded warning audit confirms every evaluated volume finite and those
  warning volumes exactly0mm³. This is not manufacturing/continuous-fit approval.
- Plot visually reviewed; case/credited-step CSVs and source manifests are in
  `sensitivity_report_final/`. The incomplete slow report attempt is preserved in
  `sensitivity_report/`, not counted as a result. Supplemental registry snapshot
  inputs are explicitly hash-recorded; executed source/results were not replaced.

Next: genuine calibration data and affordable quotation/fit, not more nominal
motion tuning. All five gates remain false; nothing is physically verified.

## Historical r2 geometry and smoke evidence — identity4d3b0dcb

The following records belong to the previous environment. Words such as
“current” inside these retained descriptions refer to that historical checkpoint,
not the offset-corrected workspace. Preserve/replay snapshots; never relabel policies.

## Geometry, accounting and interface

- 37 pytest cases passed in9.69s: original32 plus five new print/pad/ownership/budget checks.
- Seven watertight connected CAD frames; solid-PETG mass properties match ledger.
- Total **197.053g estimated**, not weighed. Bare Pico3g +two0.6g headers;
  eight cylindrical10×3mm TPE pads; horn/fastener masses remain estimated.
- Sourced M2 screw/nut/washer dimensions replace old mass-proxy boxes for clearance.
 55poses: **0modeled collisions**, but **5unknown interface groups remain**.
  Exact horns/ear locations, stack/tool access, leads/ties and layer strength block release.
  Intentional PCB/header attachment is the sole named collision exclusion.
- No unknown mechanical stops in MJCF. Six pitch/pitch/roll hinges; safe commands
  are software bounds. Eight pad contacts and plate checked for whole-foot lift;
  test compares rotated-cylinder/box minimum heights to independently transformed meshes.
- Gym/SB3 API, seeded resets, nominal restoration/inertia scaling, noisy IMU-only
  observations, delay/clipping/slew/quantization, finite neutral/random/limit commands,
  reward/gait exploit tests and native C++ control tests pass.
-30s HOME remains upright with both feet contacting; neutral video seed2000,
  distance0.00002723m, no fall, zero gait. Standing is not learned walking.
- Firmware invalid calibration header regenerated for current identity. No new ARM
  firmware build/UF2/electrical test claimed. Rebuild before flash; historicalUF2is incompatible.

## Motion diagnosis and strength

Original46s reference and three18s bounded stance/swing ankle variants completed
without a qualifying step. Maximum whole-foot clearances stayed below0.000005m,
versus required0.003m for0.04s. Logged actual/applied angles, roll and actuator torque;
CSV and summary retained. Model torque remains0.08Nm; no inflated strength/gains.

Quasi-static entire-weight-on-left-foot estimates: HOME~0.0657Nm maximum;
lean~0.0338Nm; lifted-right pose~0.0321Nm; deep-bend stress~0.0451Nm.
Twice HOME static demand~0.1314Nm exceeds current0.08Nm operating hypothesis.
This is **not** measured continuous servo capability or a proof of supported gait.
Torque margin, real plant response and the failed lifted-step sequence need diagnosis
before large PPO runs or a walking-ready physical claim.

## Historical bounded PPO smoke and reload

Fresh seed0,A nominal, **2048actual timesteps**, current identity. No resume/relabel
of old checkpoints. Validation2000–2004; final1000–1009unused. Checkpoint reload
and current evaluation/video succeeded; no measured calibration or physical approval.

| Condition | Episodes | Mean distance m | Mean reward | Falls | Gait distance / success |
|---|---:|---:|---:|---:|---|
| Nominal |5|-0.02039646|5.310372|0/5|0 /0of5|
| Randomized |5|-0.02027713|5.303456|0/5|0 /0of5|

This is stationary/sliding backward drift, **not walking**. No pilot/formal A/B
training beyond this smoke was run. Preserve older49152step pilot and2048A/B
records as historical. Current smoke cannot be used on hardware without a new
measured twin/calibration, compatible training and physical checks.

Configuration fingerprint:`4d3b0dcbad59774b12f9c908c74446f6bf7452d5bdf34a08f07cf4271cc15019`.
Current source snapshot includes matching model/control files and CAD STLs.
Policy manifests record model/source/config hashes, initialization, actual steps,
validation seeds and algorithm settings. Videos are640×480,50fps; representative frames were inspected. Clean renders in
`home_clean_video` and `smoke_clean_video` hide overlapping collision-proxy drawings
only; metrics exactly match the original videos. Physics/controller identity did
not change. New rendering source hashes/copies are saved with those evaluations.
No video proves physical success.

## Additional support diagnosis — same model identity, no new training

See [SUPPORT_DIAGNOSIS.md](SUPPORT_DIAGNOSIS.md). New tools/tests probe154ideal
single-support configurations (48pass limited static screens), replay three existing
motions with load/foot-roll diagnostics, release four prepared poses for3s, and
test two22s command-only transitions from HOME. Prepared±20° states retain>=25.36mm
swing clearance;±15° states settle back to double support. Both HOME transitions
produce zero qualifying steps. No torque/geometry/control/preprocessing change.
Current model identity stays4d3b0dcbad59774b12f9c908c74446f6bf7452d5bdf34a08f07cf4271cc15019.
New immutable records:validation/2026-10-24/support_diagnosis_final/ and
validation/2026-10-24/transition_probes/, including CSV, plot and source/mesh hashes.
This clarifies an unachieved support transition; it proves no physical or learned gait.
The expanded full suite passes **41 tests in10.31s**; its log is in
support_diagnosis_final/pytest.txt. The37-test result above is the preserved
pre-diagnosis verification, not an additional test count.

## Scripted stance-crouch/swap follow-up — unchanged physics

[STANCE_TRANSFER.md](STANCE_TRANSFER.md) documents four additional failed
stance-crouch probes and a fifth leg-extension-swap probe that reaches one
qualifying step from HOME. Two mirrored starting orders and three sensor seeds
reproduce the corresponding single-sided result. Noise seeds affect unused IMU
readings only, so these are not independent physical/parameter robustness trials.

Independent recomputation from raw2ms trace:112ms continuous whole-foot lift>=3mm,
22.36mm forward touchdown,2.33mm maximum stance-centre movement, continuously
supported opposite foot. Final body distance3.33mm, credited gait distance11.18mm,
zero alternations, no falls. **Walking remains unachieved**, no PPO added and no
gate cleared. The diagnostic wrapper is tested to preserve exact state,
observations, rewards and original metrics. Video and representative frames were
inspected; raw geometry/force diagnostics establish simulated thresholds.
The expanded suite passes **45tests in13.31s**, recorded in
stance_transfer_report/pytest.txt. Earlier37/41-test logs remain historical.

Artifacts: validation/2026-10-24/stance_transfer/, stance_transfer_swap/,
stance_transfer_review/, stance_transfer_audit/ and stance_transfer_report/.
Each run retains the diagnostic source version it actually executed, with hashes;
model/control identity remains4d3b0dcbad59774b12f9c908c74446f6bf7452d5bdf34a08f07cf4271cc15019.

## Historical phase/history study and weight handoff

[REFERENCE_GAIT.md](REFERENCE_GAIT.md) records the bounded continuation. The
original first forward flight peaks at2.987mm; faster swaps improve lift but
exceed the3mm stance-motion threshold, slower swaps miss lift. A0.95s swap gives
two qualifying steps. Returning each step backwards toHOME still erases much of
the advance. Extra2s HOME settling preserves the result and command deadband bias;
it does not isolate all causes of history dependence.

Two handoff probes then transfer weight to the landed foot. The compact version
produces **four qualifying alternating steps**,3alternations,6.602cm torso advance,
4.393cm qualifying gait distance, no fall in30s. Mirroring gives matching results.
Raw credited flights clear3mm for56–90ms, peak at≥3.177mm and have≤2.525mm stance
movement including touchdown. Video/frames inspected. This remains a handwritten
open-loop diagnostic and falls well short of the30cm target.

Five existing-DR draws, seeds42–46, produce1,1,1,1,0credited steps and zero
alternations/successes; all stay upright. Their5–8cm torso displacements do not
establish walking. Mixed draws show fragility, not parameter attribution or real
hardware tolerances. No trained-policy A/B comparison, PPO extension, relaxed
threshold, changed plant or gate release occurred. Freeze the nominal script.

Current suite: **49tests passed in14.21s**, handoff_report/pytest.txt. New tests
cover exact baseline preservation, safe/mirrored/rate-bounded phase and handoff
commands, and deadband history retained despite HOME holds. Independent raw checks
verify all12credited steps across two nominal and five randomized review episodes.
Artifacts under validation/2026-10-24/: phase_study/, phase_study_followup/,
phase_study_followup_mirror/, handoff_probes/, handoff_review/, handoff_report/.
Actual source snapshots/hashes and randomized runtime parameters are retained;
configuration identity remains unchanged. Physical fit/actuator data are absent.

## Historical procurement checkpoint — 2026-10-24

Active priced basket105.34EUR **before** current prints/sample/horn extras; minimum
known shortfall5.34EUR for that basket. No complete quote or budget clearance.
Automatic approval review rejected uploading the revised STL toMeltlab; design
was not uploaded, no supplier message/order sent. Public example/old-geometry
prices are not new quotations. See PROCUREMENT_ACTIONS.md or procurement ledger
for the exact upload/quote/measurement requirements.

Next: provider-specific quotation upload authorization or user-returned quote;
actual servo/horn measurements; sample fit; complete budget. All physical gates false.
