# Current local verification — 2026-10-24, S6-PETG-pad-r2

**No hardware purchased, printed, fitted, electrically tested or deployed.**
Prior2026-10-23record is preserved under history/2026-10-24/pre_print_revision/docs/.
Current evidence: validation/2026-10-24/print_revision/final/; earlier in-turn
records are explicitly superseded, not final results.

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

## Bounded PPO smoke and reload

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

## Phase/history study and weight handoff — latest motion checkpoint

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

## Procurement and next evidence

Active priced basket105.34EUR **before** current prints/sample/horn extras; minimum
known shortfall5.34EUR for that basket. No complete quote or budget clearance.
Automatic approval review rejected uploading the revised STL toMeltlab; design
was not uploaded, no supplier message/order sent. Public example/old-geometry
prices are not new quotations. See PROCUREMENT_ACTIONS.md or procurement ledger
for the exact upload/quote/measurement requirements.

Next: provider-specific quotation upload authorization or user-returned quote;
actual servo/horn measurements; sample fit; complete budget. All physical gates false.
