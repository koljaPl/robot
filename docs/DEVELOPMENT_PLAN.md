# Complete project execution plan

Updated **2026-10-25**. This is the detailed plan for the student and future AI
sessions. [SUMMARY](../SUMMARY.md) remains the short shopping/build overview;
[STATUS](STATUS.md) records evidence; [ROADMAP](ROADMAP.md) is the dependency map.
Prices and physical parameters remain authoritative in their structured ledgers.

**Current position:** the provisional robot design, digital twin, control interface
and RL pipeline exist. A handwritten script produces four qualifying simulated
steps. A calibrated physical robot and learned walking do not yet exist.
The immediate obstacles are an affordable complete basket and real interface/
actuator measurements. More PPO is not the next task.

## 1. Objective and fixed constraints

Answer **“From Simulation to Reality: How does a robot learn?”** by building one
small biped, learning walking in simulation and comparing fixed-parameter and
domain-randomized policies under matched simulated and physical conditions.

- Six Waveshare 15024 MG90S joints: left hip pitch, knee pitch, ankle roll; then
  the same right joints. No weaker motor or reduced-joint substitution.
- Approximately 15–20 cm, lightweight, broad feet, repairable, no arms.
- PC inference; USB to bare Pico; direct PWM; MPU6050; separate wired servo power.
- Commercial PETG printing: seven frame parts and two separate fit-test pieces.
  Eight bought grip pads; no printed TPU, printer purchase or filament packs.
- Soldering is available. Student assembly needs no mechanical drilling, cutting
  or bending; the printing service must finish usable mounting holes.
- Preferred hardware cost €50–75; **complete delivered maximum €100**, including
  VAT, required parts, full consumable packs, finishing and all staged deliveries.
  Tools are separate but still belong in initial cash expenditure.
- Delivery to 25337, Germany; PC USB-A confirmed. Include the USB-A–Micro-B data
  cable, omit an unnecessary adapter. No battery or onboard neural inference.
- This planning task authorizes no purchase, reservation, supplier message or CAD
  upload. Quotation, fit review, manufacturing release and purchase are distinct.

### Success criteria, fixed before further experiments

| Requirement | Evidence |
|---|---|
| Stand for 30 s | Separate unassisted trial; record falls/stops and cable arrangement |
| Walk at least 0.3 m within 30 s without falling | Both body displacement and qualifying gait distance reach 0.3 m |
| Alternate real lifted steps | At least two qualifying steps per foot and three alternations |
| Whole-foot lift, not a toe pivot | At least 3 mm continuously for at least 40 ms |
| Advancing touchdown with supported stance | Forward touchdown at least 5 mm, stance slip at most 3 mm and opposite supported stance |

Simulation geometry/force diagnostics can audit these criteria but never enter
policy observations. Physical acceptance uses calibrated video/ruler measurements.
If measurement resolution cannot establish a threshold, mark it **unverified**.
Reward growth, standing and sliding alone are not walking.
Qualifying gait distance is half the sum of accepted forward foot advances;
it is tracked separately from body displacement and excludes rejected steps.

## 2. Phase-by-phase checkpoint

States: **implemented** = design/code exists; **locally verified** = recorded
software evidence; **physically verified** = actual measurements/trials. No phase
is physically verified now. Blocked work has a named missing dependency.

| Original phase | Already exists / evidence | Remaining work |
|---|---|---|
| 0 Requirements | Six-joint layout, constraints and acceptance agreed | Demonstrate feasibility without silently relaxing them |
| 1 Hardware research | Sourced basket, servo comparison, power/harness design, dated budget review | Complete exact-file quotes, total delivery cost, actual interfaces and electrical ratings |
| 2 Digital twin | `physical_spec.json` → CAD/MJCF; estimated 197.053 g; local geometry/accounting checks | Confirm printed fit and replace physical estimates with measured evidence |
| 3 Common interface | Six actions; shared IMU/history processing; serial protocol, calibration and fingerprints | Physical timing/parity tests and reviewed manual multi-joint utility |
| 4 RL environment | Gymnasium reset/step, bounded servo approximation, reward, falls and gait metrics | Validate against measured dynamics and feasible reference motion |
| 5 Baseline training | Historical 2,048-step smoke and older 49,152-step pilot; no learned walking | New compatible measured-model baseline after gates pass |
| 6 Evaluation | CSV/JSON, raw gait audits, nominal/randomized diagnostics and videos | Formal trained-policy and physical comparisons with uncertainty |
| 7 Domain randomization | Conservative hypotheses implemented; one-factor study completed | Fit ranges from measurements; equal-budget trained A/B experiment |
| 8 Physical robot | Firmware, wiring/assembly procedures and quotation prototypes prepared | Approved procurement, electrical bench, sample fit, assembly and manual control |
| 9 Calibration | Templates and first-order response-fit diagnostic | Real per-servo, IMU, mass/COM, contact/current/timing records |
| 10 Sim-to-Real | Host transport and `deploy.py` prototype | Compatible measured policies; supervised standing and progressive walking |
| 11 Main experiment | Protocol in [EXPERIMENT](EXPERIMENT.md) | Matched simulated/real A/B trials, failures and analysis |
| 12 Extensions | Conditional ideas only | Turning/recovery/terrain after stable walking |
| 13 Documentation | Summary, AI guide, plan, handoff, drawings and archive | Keep synchronized; produce final school report/presentation from actual results |

### Discoveries that must not be lost

- Latest recorded full suite: **58 passed in 16.41 s**, [2026-10-25 log](validation/2026-10-25/procurement_review/pytest_after_history_exclusion.txt).
  The earlier offset-correction suite had 55 tests. This planning edit has not
  rerun the full suite; collection was rechecked and finds 58 tests.
- Current fingerprint: `b11ab9292c586ace4f2028c7061aa4ef279b6c84bd3966d2e806e0f96d01560b`.
  [Current frozen reference](baselines/scripted_r2_offset_corrected.json) and
  [historical predecessor](baselines/scripted_r2.json) remain separate.
- Seven connected watertight frame meshes; 55 sampled poses, zero modeled known
  collisions, **five unresolved interface groups**. Not manufacturing approval.
- Nominal script: four qualifying steps, three alternations, 6.60 cm torso
  displacement / 4.39 cm qualifying gait distance in 30 s, no fall. It ends
  leaned, not at HOME; it is time-driven, **not learned walking**.
- Each tested individual ±1° offset loses steps. Torso-only mass ±5% gives 0/1
  steps; friction ±15% gives 4/0; damping ±20% gives 2/3. All 73 credited steps
  in the corrected study were raw-audited. These are not physical failure rates.
- Shaft-zero error now enters actuator bias instead of disappearing at command
  bounds. All existing policies/UF2 images are historical and incompatible.
  Current firmware calibration remains invalid; ARM rebuild/electrical tests pending.

References: [support](SUPPORT_DIAGNOSIS.md), [one-step transfer](STANCE_TRANSFER.md),
[scripted gait](REFERENCE_GAIT.md), [sensitivity](SENSITIVITY.md),
[verification](VALIDATION_CURRENT.md). Preserve failed trials and source snapshots.

## 3. Dependency map and next five tasks

```text
Existing provisional CAD + control + twin + RL pipeline + diagnostic evidence
                          ↓ CURRENTLY HERE
Complete delivered budget + exact interfaces ─────┐
                                                 ├→ bench + fit sample
Independent data/manual-control preparation ──────┘        ↓
                                                   assembly + measurements
                                                          ↓
                                                measured twin + reference checks
                                                          ↓
                                                 bounded matched A/B training
                                                          ↓
                                                 supervised transfer + real A/B
                                                          ↓
                                                 school report/presentation
```

| Order | Concrete task | Owner | Done means / blocks |
|---|---|---|---|
| N1 | Obtain missing print/sample/horn costs or a genuinely complete new consolidation | Student supplies quote/permission/interfaces; AI checks ledger | Complete ≤€100 delivered basket and reviewed fit path; otherwise explicit shortfall. Blocks procurement/release |
| N2 | Prepare measurement-intake validation and logged six-joint manual control | AI; independent of hardware | Mocked tests, explicit arm, immutable logs, no fictitious measurements. Blocks later safe manual standing |
| N3 | Verify real accessories/dimensions, electrical behaviour and two-piece sample | Student + AI analysis | Photos/dimensions, bench records and actual fit; costs remain accounted. Blocks full frame |
| N4 | Assemble/weigh; calibrate/version twin; run model and reference checks | Student measures, AI models | Traceable measured calibration and reviewed feasible stepping. Blocks substantial training/deployment |
| N5 | Run bounded matched A/B training, evaluate, then supervised physical trials | AI training, student trials | Equal budgets/initialization, held-out metrics/videos and failures. Blocks learned-walking/transfer claims |

N1 and N2 can proceed independently. Later tasks require their dependencies;
there are no invented completion dates while quotes and hardware are absent.

## 4. WP1 — Close procurement and staged delivery costs

**State:** blocked. **Owner:** AI ledger/research; student external quotes and
later decisions. **Inputs:** [BUDGET_REVIEW](BUDGET_REVIEW.md),
[PROCUREMENT_ACTIONS](PROCUREMENT_ACTIONS.md), [procurement.json](../procurement.json).

### Budget decision

The dated selected basket is **€105.09 before** printing/sample/finishing/horn
extras: common subset €95.56 plus €9.53 ear-fastener packs/delivery. Known shortfall
is at least **€5.09**; complete delivered total is unknown. This is not a new live
checkout. Revalidate price, stock, VAT and postcode delivery before any future order.

The unselected taller FIX-RF-003 comparison is €96.79 before the same unknowns,
leaving €3.21. It is not an affordable complete robot. Its 4.5 mm geometry differs
from the selected 3 mm pads and needs a new twin if ever selected. Do not change
geometry or credit a comparison saving without a complete verified alternative.

### Quantities to resolve

Exact products, links, full-pack prices and supplier charges remain in the
[SUMMARY purchase table](../SUMMARY.md#complete-purchasecost-snapshot--not-cleared-to-buy)
and ledger; this checklist does not create a second price list.

| Group | Required content | Unresolved point |
|---|---|---|
| Actuation | 6 exact MG90S, 6 compatible horns, 6 shaft retainers | Six-unit stock/accessories, spline, shape, thread and dimensions |
| Control/sensing | 1 bare Pico, header kit, 1 MPU6050, header/signal pack, USB data cable | Board envelope, pull-ups, alignment and 3.3 V operation |
| Power | 1 enclosed 5 V/5 A PSU, mains lead, DC socket, capacitor | Loaded droop/current, connector ratings and cutoff |
| Harness | 6 removable branches, full heavy-wire roll, signal leads, solder, insulation/ties | Actual mating, pin order, rating and strain relief |
| Frame | 7 finished PETG parts: torso, two thighs, two shins, two feet | Exact-file quote, usable holes, supports, strength and fit |
| Samples | 1 cradle + 1 horn plate, separate test pieces | Finishing and separate delivery included |
| Contacts | 8 Delock 18309 pads installed, bought as 50-pack | Installed mass, compression, adhesion and friction |
| Ear fasteners | 12 M2×8 screws, 12 M2 nuts, 24 washers installed; priced full packs | Real stack, projection, access and length |
| Horn fasteners | 12 horn-to-frame screws + 12 matching washers | Unknown diameter/thread/length; shaft retainers are not assumed M2 |

### Procedure

1. Price the current two quotation ZIPs, quantities, hashes and settings. Send only
   those files for a quote, never the complete project archive with historical CAD.
2. Obtain separate sample/frame itemizations: PETG, initial 0.2 mm layers, three
   walls, 25% infill, reviewed load orientation/supports, removed supports, usable
   holes without student drilling, finishing, VAT, packing and delivery to 25337.
   Initial print settings are not a structural strength certification.
3. Count possible bench-component, sample and finished-frame shipments separately.
   Splitting the six-servo order can add postage. Rework/reprint costs, when known,
   belong in the staged budget; no assumed free balance order or finishing.
4. Resolve accessory contents/interfaces through exact-source data and real
   measurements. Borrow an exact sample only if actually available; do not assume
   free borrowing, pickup, hardware or supplier-provided screws.
5. Prior automatic review rejected sharing CAD with Meltlab without specific
   provider/payload authorization. Student returns a quote, or a later specifically
   authorized upload is performed; no bypass/retry elsewhere. Messages and purchases
   are not authorized by this plan.
6. If total exceeds €100, record exact shortfall plus unknowns and stop procurement.
   Seek one evidenced complete consolidation, not repeated speculative searches,
   weaker servos, omitted leads/consumables or a merely advertised example price.

**Files/deliverable:** dated ledger/source records, quotes/hashes, staged costs,
SUMMARY/BUDGET_REVIEW/PROCUREMENT_ACTIONS. **Done:** complete compliant cost and
reviewed interfaces/fit path. Actual fit may require borrowing an exact part.
If an unverified prototype purchase is necessary first, a separate explicit staged
prototype decision is required; this plan grants no budget/fit-rule exception.
**Blocks:** procurement and manufacturing release.

## 5. WP2 — Prepare independent bench/software tools

**State:** foundations implemented; additions below planned. **Owner:** AI.
**Depends on:** source inspection, not hardware or new training.

Existing: `hardware_interface.py`, `serial_robot.py`, `calibration.py`, `bench.py`,
`deploy.py`, Pico firmware, templates and `tools/fit_response.py`. Bounded/versioned
CRC frames, sequences/timestamps, arm/ack/faults and 100 ms watchdog are implemented.
The first-order fitter is a diagnostic, not automatic actuator identification.

1. **Measurement intake:** check increasing timestamps, finite values/units,
   external angle provenance, command/video clock alignment, servo identity,
   voltage/load and uncertainty. Preserve raw files; never substitute requested or
   acknowledged angles for measured shaft angles. Missing data stays unknown.
2. **Fit quality:** detect no motion, insufficient pre/post-step recording, wrong
   sign, saturation/overshoot and boundary-limited fits. Plot residuals and test
   held-out steps. Low RMSE alone cannot validate gain/strength/delay. Test with
   explicitly synthetic data; never automatically overwrite the physical ledger.
3. **Six-joint manual utility:** provide logged gradual transitions between reviewed
   calibrated poses over `SerialRobot`. `bench.py` currently controls only one
   restricted channel, so it is not a complete manual standing controller.
   Require explicit arm, compatible identity, fresh acknowledgements, rate/angle
   limits, fault/deadline/tilt handling and STOP on exit. Never auto-arm/reconnect.
4. Test corrupted/stale packets, invalid calibration, watchdog, disarmed startup
   and failures with fake serial/native firmware tests before hardware use.

5. **Measured baseline parity:** `evaluate.py` currently obtains calibration from
   policy metadata, but its HOME/untrained baseline CLI has no calibration option.
   Before formal experiments, add explicit measured calibration for those baselines
   and pass it through `tools/experiments.py`. Verify the same pulse quantization,
   model/control/calibration identity and initial-policy weights as the trained runs.
   This is a remaining implementation task, not an existing verified capability.

**Affected files later:** tests, templates, calibration-analysis tools and a new
clearly named manual-control utility; `evaluate.py`, `tools/experiments.py` and
hardware instructions. New filenames/features
are planned, not existing capabilities. Fingerprinted-source changes require a new
identity and preserved baseline. **Done:** reviewed mocked tests/logs, clear bench
procedure, no fictitious physical data. Keep the gait/plant frozen.

## 6. WP3 — Electrical bench and exact servo interfaces

**State:** not physically started. **Owner:** student; AI reviews data.
**Depends on:** WP1 budget/fit/purchasing conditions and required WP2 preparation.

1. Confirm/borrow meter, stripper/cutters, iron/stand, insulation heat source, small
   screw tools, ruler/protractor, scale and timed video equipment. Iron access is
   confirmed; other tools/access costs are not silently free.
2. Follow [HARDWARE](HARDWARE.md): short insulated heavy servo buses, replaceable
   branches, polarity markings, common ground, capacitor and strain relief.
   No servo supply current through Pico, breadboard or thin logic jumpers.
   Mains remains inside the enclosed PSU/lead.
3. Inspect/continuity-test unpowered; measure all branches with no servo attached.
   Check USB and stationary IMU. Rebuild current firmware using
   [firmware instructions](../firmware/README.md), not a historical UF2.
4. Connect one unloaded servo with horn removed. Verify pin order, 3.3 V PWM,
   supply droop/current, physical DC cutoff, disarmed boot, STOP/fault recovery
   and 100 ms command-loss watchdog. Record timing rather than assuming it.
5. Use restricted single-channel bench mode, not a policy. Its 1400–1600 µs window
   is a bench bound, not guaranteed mechanical safety. Wider exploration requires
   measured travel and reviewed limits. Establish a safe centre before fitting horns.
6. Measure/photograph housing, ears, shaft, lead exit, horn holes and actual supplied
   screws against a ruler. Identify threads/length without forcing a wrong screw.
7. Record response in both directions, backlash, repeatability, current and voltage
   unloaded and under brief small known loads. Avoid prolonged stalls; stop on
   heat/buzzing/droop. Basic meters may miss peaks—record that uncertainty.
8. Repeat mapping/identity for all six servos. Record 30–60 s stationary IMU data
   and multiple known gravity orientations, with and without servo power.

**Evidence/files:** [CALIBRATION](CALIBRATION.md), template measurements/step-response
CSV, raw bench logs/video/photos, per-servo records. **Done:** measured one-servo
operation and exact interface table. One unloaded servo test does not establish
six-servo current capacity or sustainable torque. **Blocks:** real sample/full assembly.

## 7. WP4 — Sample fit and full-frame manufacturing review

**State:** quotation prototypes ready; actual fit blocked. **Owner:** student/service;
AI geometry review. **Depends on:** WP1 and WP3 interface measurements.

1. Compare measured case/ear/horn/screw dimensions with the ledger/drawings. Correct
   authoritative geometry, not separate hidden mesh dimensions. Regenerate/requote
   any changed hash, settings, quantity or fastener schedule.
2. Obtain the two reviewed sample pieces first. Test case insertion, both ear holes,
   horn attachment, retaining-screw access, nut/washer stack and wire exit without
   drilling, forcing or cracking plastic. Check fasteners do not bottom out.
3. Inspect measured holes/slots, finishing, layer orientation and strength. A failed
   interface means revise and repeat, with actual additional costs—not full-frame release.
4. Review complete assembly sweeps: neighboring cases, links, electronics, the
   Pico's 11 mm header envelope, fasteners, wires and screwdriver access. Existing
   55 sampled poses do not prove every continuous path.
5. Freeze reviewed seven-part geometry, exact hardware and finishing quote. Ensure
   removed supports do not damage load-bearing features or leave unusable holes.

**Files:** [sample ZIP](../cad/sample_quotation_package.zip),
[frame ZIP](../cad/frame_quotation_package.zip), [brief](../cad/QUOTE_REQUEST.md),
[fastener schedule](../cad/print_order/fasteners.csv), `physical_spec.json`, CAD.
**Done:** photographed fit on actual selected servo/horn/screws; real unknowns
closed with evidence; complete cost still passes. **Blocks:** full-frame approval.
A watertight STL or quotation calculator does not satisfy this task.

## 8. WP5 — Assemble, inspect and weigh

**State:** not physically started. **Owner:** student; AI reconciles ledger.
**Depends on:** WP3/WP4 and approved finished-frame delivery.

Use the illustrated [assembly instructions](../cad/ASSEMBLY.md):

1. Set each bare servo to measured joint zero, isolate DC, then fit its horn.
   HOME is a control pose, not the shaft's mechanical zero.
2. Hip cases → torso, thigh plates → hip horns; knee cases → thighs, shin upper
   plates → knee horns; ankle cases → feet, shin lower plates → ankle horns.
   Verify pitch/roll axes and mirrored electrical signs.
3. Fit only verified fasteners; inspect projection, screw bottoming, layer cracks
   and tool access. Do not substitute larger screws or drill the student's parts.
4. Insulate/secure boards, immobilize IMU, attach four selected pads per foot at
   drawing coordinates and route wire service loops outside sweeps. Support tether
   externally without lifting/pushing the torso.
5. Weigh parts and each assembled rigid body. Assign every case/horn/bolt/board/pad/
   wire section once. Do not add assembled mass on top of its component masses.
6. Estimate COM by balancing/suspension, recording uncertainty. Inertia derived
   from measured mass/geometry remains estimated unless experimentally identified.
7. Use reviewed manual tools: one joint, small combinations, safe poses, six-servo
   power checks, cutoff/watchdog and standing. Inspect after every fall; manually
   recover and deliberately reinitialize.

**Deliverable:** measured body/component inventory, photos, calibration and manual
trial records. **Done:** assembled robot follows safe manual targets; mass totals,
current and fault checks reconcile. Physical walking is not implied.

## 9. WP6 — Fit and version the measured twin

**State:** provisional twin implemented; measured twin blocked.
**Owner:** student measures, AI models. **Depends on:** WP3–WP5.

| Parameter group | How to obtain evidence | Update/verification |
|---|---|---|
| Geometry/transforms | Real joints, horns, cases, link lengths and pads | Ledger → CAD/MJCF; compare drawings and assembly |
| Mass/COM/inertia | Weigh assembled bodies; balance/suspend; reconcile ownership | Consistent masses/inertias, no double count; label estimates |
| Pulse mapping | Six zeros/gains/signs/ranges, repeated approach both ways | Versioned calibration; inward quantization; safe commands separate from real stops |
| Actuation | Multiple unloaded/loaded steps, voltage, tracking, delay/heat | Joint fit of gains/strength/damping/speed; held-out response errors |
| Contact | Finished pad dimensions/compression/adhesion, incline/sliding tests | Baseline sliding friction and evidence-based uncertainty |
| IMU | Bias/noise/alignment, clipping/filter timing, timestamps | Same estimator in SIM/real; confirm actual firmware ranges/filter behaviour |
| Tether | Slack, unsupported mass, pull direction and repeated trials | Document experimental confound; never count cable support as unassisted |

The 0.08 N·m model torque and power estimates are hypotheses. HOME single-support
static demand was about 0.0657 N·m; doubling it exceeds that strength hypothesis.
Measure usable torque/loaded tracking before claiming margin. If inadequate,
review lighter geometry/shorter moments within the agreed layout/height; do not
raise fictitious strength just to obtain a simulated lift.

Use `tools/fit_response.py` only after WP2 quality review: a first-order delay/time
constant cannot uniquely identify MuJoCo kp/kv, sustainable torque or backlash.
Fit several amplitudes/loads and validate held-out trajectories.

Every parameter keeps **sourced / estimated / measured / unknown**, units, date,
evidence and method. New measured calibration stays invalid until all channels
and IMU entries are evidenced/reviewed. Never run `tools/sync_frame_mass.py` over
measured masses—it replaces them with solid-CAD estimates.

Regenerate model/config/header, rebuild firmware and issue a new identity after
relevant changes. Preserve incompatible policies/manifests and old snapshots;
new measured policies must be trained under their own full fingerprints.
**Done:** coherent measured/provisional distinction, mass/axis/contact checks,
held-out response agreement with errors reported, valid calibration/handshake.

## 10. WP7 — Close model, observation and reference checks

**State:** provisional checks implemented; measured acceptance blocked.
**Owner:** AI + student. **Depends on:** WP6 and physical manual checks.

1. Compile/regenerate from the same specification; verify ownership, mass, positive
   inertias, transforms, axes, contacts and continuous assembly access/sweeps.
2. Check finite HOME, bounded random and limit commands; clipping, target slew,
   PWM quantization, force/speed envelope, delay and reproducible reset behaviour.
3. Retain error outside command clipping, nominal restoration and matching inertia
   scaling. Initial delay is one/two command ticks until actual timing replaces it.
4. Compare recorded physical commands/IMU through shared preprocessing. Six normalized
   targets map to safe angles. Five 18-value frames give 90 observations: estimated
   gravity, gyro, applied-target acknowledgements and previous actions. No true
   shaft positions, orientation, translation, velocity, contact or force leaks.
5. Keep progress reward `10 × min(forward_displacement, 0.06 × control_dt)`;
   upright, lateral-motion, command-smoothness and fall terms remain simple.
   Backward motion is fully debited. Smoothness is not measured electrical energy.
6. Recheck zero-net cycles, sliding, stationary lifts, toe pivots and unsupported
   hops cannot produce walking success. Do not relax thresholds after seeing failures.
7. Replay the frozen reference against measured dynamics; compare lift, touchdown,
   slip, support, tracking and torque use with historical snapshots. Verify standing,
   weight transfer and supported lifted stepping, not only ideal initialized poses.
8. Adjust a reference only with an explicit new revision and measured reason. Small
   physical manual tests require review; do not blindly copy the full diagnostic script.

**Done:** source-hashed checks and reviewed measured-model/physical manual step
records. Current fragile four-step guessed physics does not pass this gate.
If mechanics cannot support a slow step, return to WP4–WP6 before substantial PPO.

## 11. WP8 — Bounded training and selection

**State:** pipeline implemented; no current-compatible policy trained.
**Owner:** AI. **Depends on:** WP7 and all five evidence-backed release gates.
This plan launches no training; the current instruction remains no further PPO.

| Run | Agreed maximum | Complete 1,024-step rollout budget |
|---|---:|---:|
| Measured-config smoke, when explicitly scheduled | 2,048 | 2,048 |
| Nominal pilot | 50,000 | 49,152 |
| Final each condition/training seed | 1,000,000 | 999,424 |
| Six final A/B seed runs combined | 6,000,000 | 5,996,544 maximum |

1. Before running, write seed/condition, code/model/control/calibration hashes,
   initialization hash, total budget and environment. Historical incompatible
   smoke/pilot cannot be resumed or used as proof for the measured configuration.
2. Schedule a bounded new smoke when justified: Gym/SB3, finite training, save/reload,
   validation, metrics and reviewed video. Then a nominal pilot only if checks pass.
3. Inspect falls/standing/sliding/lift/placement—not reward alone. Final **A** fixed
   and **B** randomized use seeds 0,1,2, matching initial weights and equal total
   training. B never resumes a nominal-trained A. Fit DR ranges from measurements.
4. An unchanged compatible A0 pilot counts toward its final total. Compatible smoke
   may count if actually resumed. Do not add these steps on top of the cap; B gets
   the same total learning budget from matching untrained weights.
5. Select using nominal AND randomized validation seeds **2000–2004**: walking
   successes first, qualifying gait distance second, reward third.
6. Stop at cap. If walking fails, report the mode and return to evidence/model
   diagnosis; do not silently increase steps, torque or change acceptance.

**Files:** `train.py`, `tools/experiments.py`, `robot_config.py`, new run directories.
**Done:** bounded matched runs/checkpoints/TensorBoard/manifests and compatible
reload. Resume preserves budget but is not claimed bitwise identical to uninterrupted
training because full RNG/simulator rollout state is not checkpointed.

## 12. WP9 — Final simulated evaluation

**State:** tools/prototype results exist; formal comparison pending.
**Owner:** AI. **Depends on:** WP8; freeze selection before final tests.

- Reserve seeds **1000–1009** for final evaluation, never diagnostic tuning. Each
  selected A/B seed policy is tested under nominal and randomized environments.
- Include HOME and seed-matched untrained baselines under both conditions. The
  existing full three-seed orchestration gives 120 trained-policy episodes plus
  20 HOME and 60 untrained episodes: **200 final episodes**.
  First close WP2's calibration-parity gap; default-calibration baselines are not
  a matched measured-configuration comparison.
- Save per-episode distance/speed/duration/falls/reward, left/right steps, alternations,
  gait distance/slip and stop reasons. Report each training seed and spread; ten
  environment seeds are not ten independently trained policies.
- Keep nominal and randomized results separate. Save videos and representative
  failures. `evaluate.py --video` currently records only the first episode per call;
  other reviewed episodes need separate immutable calls/output directories.
- Independently review credited foot motion. If tuning follows final test exposure,
  report that and define a new protocol instead of calling the tests untouched.

**Files:** `evaluate.py`, `gait_metrics.py`, EXPERIMENT, CSV/JSON/videos.
**Done:** comparable tables with actual identities/steps and honest acceptance
result. No trained walking claim from a handwritten script or body displacement alone.

## 13. WP10 — Conservative physical transfer

**State:** deployment prototype exists; no physical trial.
**Owner:** student with AI analysis. **Depends on:** safe bench/manual checks,
measured calibration, compatible trained policy/firmware and reviewed WP9 results.

1. Check exact identities/handshake and rejection of stale checkpoints. Confirm
   cutoff, watchdog, disarmed boot, faults, deadlines and IMU saturation behaviour.
2. Use the trained calibrated mapping. Do not clip a wide-range policy into narrower
   hardware limits; update/version/retrain if limits change. Begin with reviewed
   standing, then short supervised stepping, then longer attempts.
3. Use a low clear floor, thin protective surface if needed and optional slack line.
   Wires must not lift/push the body. Record floor/protection/cable changes; hidden
   assistance cannot become an unassisted pass.
4. On fall, unusual heat/buzz/droop or control fault, isolate DC, inspect, recover
   manually and deliberately reinitialize. Software STOP is not power isolation.
5. Log commands/acks/IMU/faults with calibrated ruler/video. Commands are not shaft
   measurements. Never double-integrate the cheap IMU to claim travelled distance.
   Record interventions, unsuccessful trials and damaged/replaced servos.

**Files:** `deploy.py`, measured calibration, immutable physical trials and
`docs/templates/physical_trials.csv`. **Done:** actual measured standing/step
results, not merely a successfully launched Python process.

## 14. WP11 — Main school experiment and presentation

**State:** protocol exists; physical comparison/report pending.
**Owner:** student + AI. **Depends on:** compatible A/B policies and safe WP10 trials.

- Fix floor, voltage, start pose, duration, cable route, policy limits and scoring
  before comparison. Alternate AB/BA order; begin at least five paired attempts
  only after earlier supervised trials are safe.
- Keep conditions/budgets equal. Record wear, warm-up, servo replacements and order
  effects. Include failures, not only successful clips.
- Compare simulation vs real and A vs B: body/gait distance, speed, falls, upright
  time, foot motion and uncertainty. Failed transfer is a valid reportable outcome.
- Report structure: question/hypothesis → hardware/cost → learning/actions/
  observations/reward → calibration → matched method → tables/videos → failures,
  cable/simulation limits → conclusion. Label script and PPO behaviours separately.
- Produce final school report/presentation, brief summary and reproducible archive.
  Separate priced, actually paid and unknown costs; use actual timestep/model labels.

**Done:** honest reproducible school results, whether walking succeeds or fails.
Turning, recovery, narrower feet and terrain are separately scoped extensions
only after stable baseline walking.

## 15. Release gates and evidence

All five entries in [gates.json](gates.json) are **false**. A changed entry needs
linked evidence, a status update and reviewed next action; a software test must
not silently turn a physical gate true.

| Gate key | Required evidence |
|---|---|
| `delivered_bom_below_100` | Complete current exact basket, stock/VAT/finishing and all staged deliveries ≤€100 |
| `servo_and_horn_fit_verified` | Actual exact servo/horn/screw measurements and photographed sample fit |
| `assembly_clearances_reviewed` | Complete assembly/sweep, wires/tool access, printed fit/strength review—not only sampled meshes |
| `measured_actuator_and_imu_fit` | Per-servo/IMU calibration, electrical/timing records and held-out response fit |
| `reference_weight_transfer_and_lifted_step_verified` | Reviewed measured-model and safe physical manual weight transfer/lift evidence |

These gates do not by themselves claim learned walking or transfer success.
Separate measured trials must satisfy the acceptance criteria.

## 16. Failure decisions and realistic scheduling

| Failure/risk | Evidence now | Response |
|---|---|---|
| No complete robot ≤€100 | Selected subtotal €105.09, prints unknown | Stop procurement; record shortfall. User later decides constraints if no compliant route exists |
| Horn/ear/screw mismatch | Actual batch unknown | Measure/revise/requote sample; no forced/drilled student assembly |
| Insufficient torque/power | Hypotheses and limited HOME margin | Measure loaded tracking/current/heat; review mass/moments and cost, not fictitious force |
| Print failure/hidden sweep conflict | Finite modeled checks only | Sample/load review and physical continuous inspection before dynamics |
| Fragile gait/poor transfer | Offset/mass/friction/damping sensitivity | Calibrate uncertainty and measured reference; no further guessed-physics tuning |
| Sliding/reward exploit | Root movement can exceed gait progress | Keep raw foot audit and fixed thresholds; report sliding separately |
| Timing/preprocessing mismatch | Local tests, no electrical timing | Measure PWM/IMU/USB/acks and shared observation parity |
| Rework consumes staged budget | Sample/finishing costs unknown | Price staged orders first; no assumed free repeat parts/delivery |
| No walking at training cap | No learned walking yet | Stop/report failure; retain useful school experiment rather than moving goalposts |

Do not promise a completion date before budget, supply and interfaces are resolved.
Use gate milestones; record actual dates/effort after completion. Hardware waiting
can overlap WP2 preparation, not fabricated measurements or speculative long training.

## 17. AI continuation and executable commands

1. Read SUMMARY → AGENTS → STATUS → relevant work package. Inspect only its source,
   ledger and evidence; do not restart a whole-repository audit.
2. Preserve existing working-tree edits. Choose one executable task and identify
   whether it is software preparation or requires human measurements/quotes.
3. New experiments use immutable directories with source/config/calibration hashes
   and actual timesteps/trial conditions. Preserve old failed trials and policies.
4. Never invent physical evidence. Name the exact missing measurement and continue
   independent WP2 work when possible. Do not repeat completed budget searches.
5. Keep procurement/physical/config ledgers authoritative; source code overrides
   embedded handoff copies. Rebuild after actual geometry/control changes.
6. Update STATUS/SUMMARY and affected references, regenerate the 19-section handoff
   and explicit-allowlist archive. Exclude hidden app folders, credentials, installs,
   toolchains and private files. Forward only quotation ZIPs to print services.

**Available now: no hardware arm, PPO or external upload.** Use `tests/` explicitly:
archived copied tests can collide during unrestricted root discovery. The prior
collection error and successful history-excluded run remain preserved.

```bash
.venv/bin/python -m pytest --collect-only -q tests
.venv/bin/python -m pytest -q tests
.venv/bin/python tools/budget_gate.py  # expected exit1; complete total unknown
.venv/bin/python tools/compare_procurement.py --option berrybase_round_pads # exit2

git diff --check
```

**Conditional later commands—not instructions to execute them now:**

```bash
# After reviewed geometry changes; inspect new output before releasing files.
MPLCONFIGDIR=/tmp/s6-mpl .venv/bin/python tools/prepare_print_order.py
.venv/bin/python tools/check_clearance.py --output runs/geometry_NEW/clearances.json

# With real bench hardware, correct port and a fresh log file.
.venv/bin/python bench.py --port /dev/ttyACM0 --seconds 10 --output runs/bench_NEW.csv

# Actual external angle measurements; diagnostic requires quality review.
.venv/bin/python tools/fit_response.py runs/measured_step_NEW.csv --output runs/fit_NEW.json

# Only with measured calibration, all gates and a newly scheduled experiment.
.venv/bin/python tools/experiments.py --calibration calibrations/measured-v1.json --steps 1000000 --output runs/formal_NEW

# After substantive source/documentation edits.
.venv/bin/python tools/build_handoff.py
.venv/bin/python tools/package_project.py
```

Measured calibration/CSV and `runs/*_NEW` paths above are placeholders, not existing
physical records. Firmware build/flash commands stay in its README. Do not supply
an immediate policy-arm command while physical checks are absent.

**Exact next AI task:** if no new quote/measurement has arrived, begin WP2
measurement-intake validation. Keep the script frozen; do not rerun sensitivity,
repeat the same searches, change pad geometry, tune motion or start PPO. If new
evidence arrives, validate provenance/dependencies before updating any ledger/gate.
