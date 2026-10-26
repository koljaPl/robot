# Project plan — authoritative living record

Updated **2026-10-26**. Read this overview before each work chunk; the complete
work packages follow. SUMMARY.md is the purchase/build snapshot, not a competing plan.

| Main phase | Current position | Remaining work |
|---|---|---|
| Requirements and hardware selection | User agreed; Pico2/classmate printing selected | Record actual purchases/costs |
| Printable parts and provisional simulation | Print package, twin/RL and intake checker implemented; 121tests pass (current local suite) | Actual fit/strength/calibration |
| Bench-control software | **LOCALLY VERIFIED:** manual preview/control, calibration parity and Pico2 build;121tests pass | Pico2 firmware locally cross-built; next: actual fit/one-servo bench records |
| Physical assembly and calibration | **Ordering started—reported by user** | Receive parts, sample-fit, bench, assemble, weigh/measure |
| Measured twin and learning | Provisional model; scripted motion below walking target | Measured twin/reference, bounded fixed/DR training |
| Physical transfer and school experiment | Procedures prepared | Supervised trials, matched comparison, report/presentation |

**Update rule:** after every completed task, changed scope, failed check or blocker,
update this plan before reporting completion. Record date/change/evidence/remaining
work/exact next action; synchronize STATUS/SUMMARY. Never equate user agreement,
implementation, local tests and physical verification.


## Current work log

| Date | Change / evidence | Remaining / exact next action |
|---|---|---|
|2026-10-26|Root plan created from detailed plan; previous source archived. User says ordering has started; individual items, quantities, paid prices and arrivals remain unknown.|Implement manual_control.py with offline preview and explicit hardware arm, then calibration parity; no new PPO or hardware operation.|
|2026-10-26|Manual sequence preview/hardware runner and evaluation calibration propagation implemented; no hardware/learning run.|Next: mocked safety, calibration parity and orchestration tests. Existing source-only replay registry must get a successor because evaluate.py changed.|
|2026-10-26|First mocked manual/calibration batch passed25tests; inspection added explicit final-command acknowledgement before STOP (pending retest). No physical run.|Finish focused tests, create source-only replay successor, then full active suite.|
|2026-10-26|Focused manual/evaluation suite passed28tests. Timing review found that catch-up bursts could violate host commanded slew; scheduler now enforces≥20ms spacing and a30s command cap, pending targeted verification.|Run the jitter regression and full suite; physical tests still pending.|
|2026-10-26|Full active suite passed98tests in17.11s. Manual previews/mocked safety, no catch-up bursts/final ACK and measured evaluation parity verified. Source-only replay successor keeps exact nominal metrics and configuration identity; no PPO.|Next: documentation/archive integrity, then Pico2 cross-build preparation. Student: record ordered items as they arrive, sample-fit/bench/calibrate.|
|2026-10-26|Delivery review added root-plan link rebasing in generated handoff and cleanup if USB buffer initialization fails; regression test added. Geometry/control identity unchanged.|Rerun active suite for the new cleanup regression, then validate document/archive integrity.|
|2026-10-26|Final active suite99passed in17.21s, including constructor-failure cleanup. HOME-only offline CLI preview passed; no USB, PPO or physical gate change.|Finish link/handoff/archive checks. Next independent task: Pico2 disarmed cross-build; user records actual orders/arrivals and performs fit/bench measurements.|
|2026-10-26|Delivery link audit failed: extracted print_for_classmate folder absent while its original ZIP remains intact. No source/CAD change.|Verify ZIP manifest and restore identical files, then rerun link/handoff/archive checks.|
|2026-10-26|Original print ZIP integrity/manifest verified; extracted folder restored byte-for-byte without changing ZIP/STLs or regenerating CAD.|Rerun delivery link checks and regenerate final handoff/archive.|
|2026-10-26|Second link-check attempt hit a checker false-positive inside embedded C++ code (`int i`), not a document link. Checker now excludes fenced code.|Revalidate actual Markdown links/anchors; no implementation change or extra training.|
|2026-10-26|Delivery verified:216actual Markdown links,19-section regenerated handoff and1,717-member archive; required new files present and every archived byte matches its source. Original print ZIP unchanged. Final active suite remains99passed; no hardware/PPO.|Refresh the archive with this final log entry. Next AI task: prepare official Pico2 SDK/Arm cross-build and compile disarmed firmware without flashing. Human: supply order/arrival records and perform sample-fit/bench measurements.|
|2026-10-26|Pico2 cross-build stage started: prepare isolated SDK2.3.1, Arm14.2.Rel1 and picotool2.3.1; implement a file-only reproducible builder. Missing purchase details do not block this software work.|Validate tool provenance/configuration, build current invalid-calibration firmware, test failure paths and record actual results. No USB/flash/arm/PPO or physical gate change.|
|2026-10-26|Initial dependency metadata download failed in sandbox: curl could not resolve api.github.com. No build claimed.|Retry the official read-only download through permitted network access; continue independent builder/tests if unavailable.|
|2026-10-26|Official downloads succeeded outside project archive; Arm compiler archive and picotool release checksums verified, SDK2.3.1 commit079c6f39/TinyUSB86ad6e56 fetched. Sandbox DNS failure resolved through permitted download access.|Implement pinned file-only builder and focused safety/failure tests, then actual Pico2 compile. No device access or physical claim.|
|2026-10-26|First actual Pico2 build compiled/linked ELF+UF2, but builder inspection rejected the ELF because readelf does not print a literal Cortex-M33 model name. Failed run preserved under runs/pico2_crossbuild_20261026_01.|Inspect architecture attributes and compiler flags; correct the overly specific inspection without changing firmware or accepting the wrong target. Retest in a new output directory.|
|2026-10-26|Inspection resolved: ELF uses Armv8-M architecture attributes; CMake flags explicitly select cortex-m33/secure mode. Picotool uf2 info is device-oriented, so it is excluded; only info -a with an explicit ELF/UF2 filename is allowed. Manual rejected syntax did not access hardware.|Verify both artifacts through file-only metadata and independent UF2 parsing; add target/command regression tests and rerun builder in a new folder. Firmware sources remain unchanged.|
|2026-10-26|Pico2 build02 passed independent ELF/UF2/identity checks;20focused builder tests passed. Firmware/model/control files unchanged, invalid calibration retained; no USB/flash. Official RP2350-E10 absolute block validated separately from Arm-image numbering.|Fix compiler date macros to a recorded epoch and remove inherited compiler overrides, verify repeat builds in new folders, then active suite/documentation delivery.|
|2026-10-26|Builder now fixes SOURCE_DATE_EPOCH and strips inherited compiler overrides;21focused tests pass. Build03 passed file-only target/identity inspection. Overview remains six phases; dated evidence is kept in this work log.|Run independent repeat build04 and compare ELF/UF2 hashes; active suite in progress. Then publish compact build evidence and refresh guides/handoff/archive.|
|2026-10-26|Active suite120passed in18.85s. Repeat builds03/04 both passed target/identity checks, but byte-equality comparison failed; evidence folders retained. No physical result.|Diagnose path-dependent ELF/UF2 differences before claiming repeatability; record actual results, then complete documentation/archive.|
|2026-10-26|Repeat-build diagnosis: UF2 images already identical; ELF debug paths differed by output folder. Added compiler path normalization and source/ledger drift guard; prior runs preserved.|Verify final builder with normalized repeat builds and active suite, then document evidence. No firmware source/identity or physical gate changes.|
|2026-10-26|Full suite121passed in17.44s. Normalized builds06/07 have identical ELF/UF2 and source hashes. Inspection noted custom Release flags omitted SDK default debug information; retain -g for usable debugging before final delivery.|Build final two copies with SDK-equivalent -g/-O3/-DNDEBUG plus path normalization, compare hashes, then publish evidence. No control logic or physical changes.|
|2026-10-26|Final builds08/09 passed: ELF and UF2 byte-identical with debug information retained, fixed timestamp and normalized paths. Firmware/model/control identity remains685e3802; artifacts/manifests copied to docs/validation/2026-10-26/pico2_crossbuild. No USB/flash/PPO.|Finish post-flag active-suite check, source/document links,19-section handoff and explicit-allowlist archive. Next physical dependency: actual samples/electronics and user bench records.|
|2026-10-26|Post-flag full active suite121passed in18.02s. Current status/summary/AI guide updated; verified ELF explicitly allowed in delivery, toolchains excluded. Earlier inspection/comparison failures retained.|Complete document/allowlist/archive integrity checks and refresh delivery. Then receive and review actual order/fit/bench records; no automatic flash/arm/training.|
|2026-10-26|Pico2 preparation stage COMPLETE locally:121tests passed in18.02s; final ELF/UF2 repeat byte-identically.249local links/anchors,19-section handoff and initial1,856-member archive passed integrity/byte/allowlist checks. Firmware/model/control files and print ZIP unchanged; all physical gates false.|Refresh final archive with this log and delivery records. Next: user receives parts, tests2fit samples/power/one unloaded servo/IMU and supplies receipts/measurements; AI validates records. Missing order details remain unknown, not blockers to completed software work.|

---

# Detailed execution plan

Updated **2026-10-26**. This is the detailed plan for the student and future AI
sessions. [SUMMARY](SUMMARY.md) remains the short shopping/build overview;
[STATUS](docs/STATUS.md) records evidence; [ROADMAP](docs/ROADMAP.md) is the dependency map.
Prices and physical parameters remain authoritative in their structured ledgers.

## Active decision update — 2026-10-26

**WP1 design/printing selection COMPLETE by user confirmation.** Classmate printing
is accepted; exact price unknown/excluding delivery. Selected board now bare Pico2
RP2350. This supersedes the earlier provider-selection/quotation-search next task
below; it does not invent a≤€100 numerical total or actual print fit.
Separate ready-to-slice files/instructions: [print folder](print_for_classmate/00_START_HERE.md)
and [print ZIP](print_for_classmate.zip),2fit samples before7frame parts.

**Next phase WP2 started:** external-angle provenance/measurement quality checker
implemented; manual six-joint tooling and measured-baseline parity now also locally
verified; current suite121tests passes. [Manual usage](docs/MANUAL_CONTROL.md). No physical operation; no new PPO. Pico2 identity begins
`685e3802`; board mass remains estimated. Pico2 preparation firmware is now locally
cross-built; physical tests remain pending.
All references to older prices/fingerprints/results below retain their historical
date; current cost ledger is authoritative. Do not repeat earlier supplier searches.

**Current position:** the provisional robot design, digital twin, control interface
and RL pipeline exist. A handwritten script produces four qualifying simulated
steps. A calibrated physical robot and learned walking do not yet exist.
User ordering has started; purchased items/prices/arrivals are not yet known.
Physical interface and actuator measurements remain pending. More PPO is not the next task.

## 1. Objective and fixed constraints

Answer **“From Simulation to Reality: How does a robot learn?”** by building one
small biped, learning walking in simulation and comparing fixed-parameter and
domain-randomized policies under matched simulated and physical conditions.

- Six Waveshare 15024 MG90S joints: left hip pitch, knee pitch, ankle roll; then
  the same right joints. No weaker motor or reduced-joint substitution.
- Approximately 15–20 cm, lightweight, broad feet, repairable, no arms.
- PC inference; USB to bare Pico2; direct PWM; MPU6050; separate wired servo power.
- User-arranged classmate PETG printing: seven frame parts and two separate fit-test pieces.
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
| 3 Common interface | Six actions, serial/calibration/fingerprints plus locally verified reviewed manual utility | Actual hardware timing/operation and measured calibration |
| 4 RL environment | Gymnasium reset/step, bounded servo approximation, reward, falls and gait metrics | Validate against measured dynamics and feasible reference motion |
| 5 Baseline training | Historical 2,048-step smoke and older 49,152-step pilot; no learned walking | New compatible measured-model baseline after gates pass |
| 6 Evaluation | CSV/JSON/videos and calibrated HOME/untrained/policy parity locally verified | Formal trained-policy and physical comparisons with uncertainty |
| 7 Domain randomization | Conservative hypotheses implemented; one-factor study completed | Fit ranges from measurements; equal-budget trained A/B experiment |
| 8 Physical robot | Firmware, wiring/assembly procedures and quotation prototypes prepared | Approved procurement, electrical bench, sample fit, assembly and manual control |
| 9 Calibration | Templates and first-order response-fit diagnostic | Real per-servo, IMU, mass/COM, contact/current/timing records |
| 10 Sim-to-Real | Host transport and `deploy.py` prototype | Compatible measured policies; supervised standing and progressive walking |
| 11 Main experiment | Protocol in [EXPERIMENT](docs/EXPERIMENT.md) | Matched simulated/real A/B trials, failures and analysis |
| 12 Extensions | Conditional ideas only | Turning/recovery/terrain after stable walking |
| 13 Documentation | Summary, AI guide, plan, handoff, drawings and archive | Keep synchronized; produce final school report/presentation from actual results |

### Discoveries that must not be lost

- Latest recorded full suite: **121 passed in18.02s**, [cross-build final log](docs/validation/2026-10-26/pico2_crossbuild/pytest_release.txt).
  Earlier99/69/58/55-test records remain historical.
- Current fingerprint: `685e3802999f8c9f72abbe119b17377380f9a41f13eeea32953432b17c153c88`.
  [Current frozen reference](docs/baselines/scripted_bench_tools.json) and
  [historical predecessor](docs/baselines/scripted_r2.json) remain separate.
- Seven connected watertight frame meshes; 55 sampled poses, zero modeled known
  collisions, **five unresolved interface groups**. Not manufacturing approval.
- Nominal script: four qualifying steps, three alternations, 6.60 cm torso
  displacement / 4.39 cm qualifying gait distance in 30 s, no fall. It ends
  leaned, not at HOME; it is time-driven, **not learned walking**.
- Each tested individual ±1° offset loses steps. Torso-only mass ±5% gives 0/1
  steps; friction ±15% gives 4/0; damping ±20% gives 2/3. All 73 credited steps
  in the corrected study were raw-audited. These are not physical failure rates.
- Shaft-zero error now enters actuator bias instead of disappearing at command
  bounds. All existing policies and older UF2 images are historical and incompatible.
  Current Pico2 preparation ELF/UF2 is locally cross-built with invalid calibration;
  electrical tests and measured-policy firmware remain pending.

References: [support](docs/SUPPORT_DIAGNOSIS.md), [one-step transfer](docs/STANCE_TRANSFER.md),
[scripted gait](docs/REFERENCE_GAIT.md), [sensitivity](docs/SENSITIVITY.md),
[verification](docs/VALIDATION_CURRENT.md). Preserve failed trials and source snapshots.

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
| N1 | Record user-reported orders/receipts, then inspect actual parts and fit samples | Student supplies receipts/interface measurements; AI reconciles records | Ordering started; exact items/costs unknown. Physical fit and numeric accounting remain distinct from accepted design |
| N2 | Completed: intake, manual-control previews/mocked safety, measured-baseline parity | AI software locally verified |121tests pass; Pico2 cross-build also verified. Physical manual operation still pending |
| N3 | Verify real accessories/dimensions, electrical behaviour and two-piece sample | Student + AI analysis | Photos/dimensions, bench records and actual fit; costs remain accounted. Blocks full frame |
| N4 | Assemble/weigh; calibrate/version twin; run model and reference checks | Student measures, AI models | Traceable measured calibration and reviewed feasible stepping. Blocks substantial training/deployment |
| N5 | Run bounded matched A/B training, evaluate, then supervised physical trials | AI training, student trials | Equal budgets/initialization, held-out metrics/videos and failures. Blocks learned-walking/transfer claims |

N1 and N2 can proceed independently. Later tasks require their dependencies;
there are no invented completion dates while quotes and hardware are absent.

## 4. WP1 — Close procurement and staged delivery costs

**State:** design/provider decision complete by user; numeric accounting and fit pending. **Owner:** AI ledger; student external quotes and
later decisions. **Inputs:** [BUDGET_REVIEW](docs/BUDGET_REVIEW.md),
[PROCUREMENT_ACTIONS](docs/PROCUREMENT_ACTIONS.md), [procurement.json](procurement.json).

### Budget decision

The dated selected basket is **€106.49 before** printing/sample/finishing/horn
extras: common subset €96.96 plus €9.53 ear-fastener packs/delivery. Known shortfall
is at least **€6.49**; complete delivered total is unknown. This is not a new live
checkout. Revalidate price, stock, VAT and postcode delivery before any future order.

The earlier unselected taller-pad comparison was€96.79 with Pico1; with Pico2
it would be€98.19 before unknowns, leaving€1.81. It is not an affordable complete robot. Its 4.5 mm geometry differs
from the selected 3 mm pads and needs a new twin if ever selected. Do not change
geometry or credit a comparison saving without a complete verified alternative.

### Quantities to resolve

Exact products, links, full-pack prices and supplier charges remain in the
[SUMMARY purchase table](SUMMARY.md#cost-record--selected-arrangement-accepted-exact-total-pending)
and ledger; this checklist does not create a second price list.

| Group | Required content | Unresolved point |
|---|---|---|
| Actuation | 6 exact MG90S, 6 compatible horns, 6 shaft retainers | Six-unit stock/accessories, spline, shape, thread and dimensions |
| Control/sensing | 1 bare Pico2, header kit, 1 MPU6050, header/signal pack, USB data cable | Board envelope, pull-ups, alignment and 3.3 V operation |
| Power | 1 enclosed 5 V/5 A PSU, mains lead, DC socket, capacitor | Loaded droop/current, connector ratings and cutoff |
| Harness | 6 removable branches, full heavy-wire roll, signal leads, solder, insulation/ties | Actual mating, pin order, rating and strain relief |
| Frame | 7 finished PETG parts: torso, two thighs, two shins, two feet | Exact-file quote, usable holes, supports, strength and fit |
| Samples | 1 cradle + 1 horn plate, separate test pieces | Finishing and separate delivery included |
| Contacts | 8 Delock 18309 pads installed, bought as 50-pack | Installed mass, compression, adhesion and friction |
| Ear fasteners | 12 M2×8 screws, 12 M2 nuts, 24 washers installed; priced full packs | Real stack, projection, access and length |
| Horn fasteners | 12 horn-to-frame screws + 12 matching washers | Unknown diameter/thread/length; shaft retainers are not assumed M2 |

### Current procedure after user acceptance

1. The user has started ordering and arranged classmate printing. Record exact
   item/model, quantity, paid price, postage, order date and arrival only when
   supplied. Keep historical quotes separate; never infer all items were bought.
2. Use the separate classmate print folder:2fit samples first, then7frame parts
   if actual servo/horn/screws fit. Record material/settings, finishing, sample
   dimensions, actual costs and any transport. Do not print duplicate combined files.
3. Reconcile actual total against€100, showing unknown amounts as unknown and
   reporting any shortfall honestly. User acceptance is not a numerical proof.
4. New suppliers, services, CAD uploads or AI purchases/messages are not authorized
   or needed by this task. Earlier Meltlab research is historical; do not restart it.
5. Real fit/current/strength checks remain required before full assembly or dynamic
   operation; continue independent bench software preparation while parts arrive.

**Files/deliverable:** procurement ledger with separate ordering/paid-cost records,
classmate print manifest, actual fit/bench evidence. **Decision state:** design/
printing selection complete; financial accounting and physical checks pending.
**Blocks:** numerical budget and physical release, not independent software work.

## 5. WP2 — Prepare independent bench/software tools

**State:** implemented and locally verified; physical use remains pending.
**Owner:** AI preparation, student later bench operation.

- Measurement-intake/provenance checker and diagnostic quality screens exist.
  Actual external-angle recordings, plots/held-out fits and reviewed physical
  calibration still await data. See [intake guide](docs/MEASUREMENT_INTAKE.md).
- `manual_control.py` accepts version1 timed six-radian targets in shared order.
  Defaults to offline50Hz trajectory/manifest without USB. Hardware requires
  explicit arm, measured validated calibration, matching identity and fresh
  stationary disarmed telemetry. Start is the acknowledged command, not shaft feedback.
- Invalid ranges/durations/slew are rejected before connection. Runtime avoids
  catch-up bursts, stops on faults/stale data/tilt/saturation/deadlines, requires
  final command acknowledgement, logs commands/rawIMU/acks/errors, and requests
  STOP/close on completion, failure or Ctrl-C. No reconnect, GUI or gait policy.
- Example [HOME-only movement](docs/templates/manual_home_only.json) is for preview,
  not physical approval. [Manual guide](docs/MANUAL_CONTROL.md) documents limits.
- `evaluate.py --calibration` now supplies measured calibration to HOME/untrained
  baselines. Explicit/policy mismatch is rejected; result identities record the
  effective mapping. Formal orchestration passes the same calibration everywhere.
- Tests cover mocked safety/USB cleanup, quantization/calibration parity and
  orchestration without real training or hardware. New source-only replay registry
  preserves previous snapshots, model/control identity and exact nominal metrics.

**Done evidence:** current bench-tools test/preview/replay records linked above.
**Next:** Pico2 preparation build is locally verified; receive/inspect parts and perform the
human-assisted WP3–WP7 checks. No software test clears a physical gate.

## 6. WP3 — Electrical bench and exact servo interfaces

**State:** not physically started. **Owner:** student; AI reviews data.
**Depends on:** WP1 budget/fit/purchasing conditions and required WP2 preparation.

1. Confirm/borrow meter, stripper/cutters, iron/stand, insulation heat source, small
   screw tools, ruler/protractor, scale and timed video equipment. Iron access is
   confirmed; other tools/access costs are not silently free.
2. Follow [HARDWARE](docs/HARDWARE.md): short insulated heavy servo buses, replaceable
   branches, polarity markings, common ground, capacitor and strain relief.
   No servo supply current through Pico, breadboard or thin logic jumpers.
   Mains remains inside the enclosed PSU/lead.
3. Inspect/continuity-test unpowered; measure all branches with no servo attached.
   Check USB and stationary IMU. Rebuild current firmware using
   [firmware instructions](firmware/README.md), not a historical UF2.
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

**Evidence/files:** [CALIBRATION](docs/CALIBRATION.md), template measurements/step-response
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

**Files:** [sample ZIP](cad/sample_quotation_package.zip),
[frame ZIP](cad/frame_quotation_package.zip), [brief](cad/QUOTE_REQUEST.md),
[fastener schedule](cad/print_order/fasteners.csv), `physical_spec.json`, CAD.
**Done:** photographed fit on actual selected servo/horn/screws; real unknowns
closed with evidence; complete cost still passes. **Blocks:** full-frame approval.
A watertight STL or quotation calculator does not satisfy this task.

## 8. WP5 — Assemble, inspect and weigh

**State:** not physically started. **Owner:** student; AI reconciles ledger.
**Depends on:** WP3/WP4 and approved finished-frame delivery.

Use the illustrated [assembly instructions](cad/ASSEMBLY.md):

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
  WP2 calibration parity is implemented; use the explicit measured calibration
  for all formal baselines, not default prototype quantization.
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

All five entries in [gates.json](docs/gates.json) are **false**. A changed entry needs
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
| No complete robot ≤€100 | Selected subtotal €106.49, prints unknown | Stop procurement; record shortfall. User later decides constraints if no compliant route exists |
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

**Exact next AI task:** review actual order/arrival, fit-sample and one-servo/IMU bench
records when supplied; record their provenance and only then update affected ledgers.
Pico2 cross-build is locally verified; no additional build or training is needed
without changed sources or new measurements. Never flash/arm without physical checks. Keep the script frozen; do not rerun sensitivity,
repeat the same searches, change pad geometry, tune motion or start PPO. If new
evidence arrives, validate provenance/dependencies before updating any ledger/gate.
