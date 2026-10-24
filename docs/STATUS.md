# Current project status — 2026-10-24

Start with SUMMARY.md and AGENTS.md. **Nothing bought, printed, assembled, flashed
or physically verified.** Active revision:**S6-PETG-pad-r2**, outsourced PETG.

| Stage | State | Evidence / blocker |
|---|---|---|
| Requirements / AI entry | implemented | Six joints,15–20cm,PC/USB,wired power,EUR100retained; no printer purchase |
| Hardware research / budget | blocked | Common95.81 +ear-hardware delivery9.53 =105.34before prints/sample/horns;5.34over cap. Updated ledger/source dates |
| CAD / order preparation | implemented, locally verified partial | Seven connected watertightPETGmeshes; two-piece sample ZIP, seven-piece frame ZIP, drawings/manifests/fastener schedule.0modeled collisions/55poses;5unknown fit groups; NOT manufacture-approved |
| Shared control / firmware | locally verified partial | Existing GPIO/protocol retained; invalid current header/nativeC++tests pass. ARMbuild from previous revision is historical; physical timing/calibration absent |
| Provisional MuJoCo / Gym | locally verified | New barePico/header ownership,8TPEpad contacts,estimated197.053g,axes/inertias/contacts/reward/provenance checked;37tests pass |
| Manual reference | blocked |46s reference +three bounded ankle variants:zero qualifying lifts/steps; strength/plant assumptions unmeasured |
| PPO / evaluation | locally verified smoke only | New2048steps A0, reload/CSV/validation/video;0success/0gait under nominal/randomized validation. No larger run |
| Physical build / calibration / transfer | planned, blocked | No hardware. Bench/soldering/sample/assembly/calibration procedures ready; requires user measurements and budget/fit clearance |
| Formal A/B / school experiment | planned, blocked | No current full six-run experiment or real trials. Exact seeds/budgets remain in roadmap |
| Extensions | planned | Only after stable walking |

## Current architecture

Six exact Waveshare15024MG90S; Lhip/knee pitch/ankle roll, then Rsame.50Hz policy
and directPicoPWM,200Hz MPU6050,2ms MuJoCo. Bare Pico PCB plus two header rows;
header11mm envelope retained. Separate USB logic and5V/5A servo bus, common ground,
self-soldered replaceable harness. SevenPETG frames; four bought10×3mm TPE pads
per90×45mm foot. No printed TPU, spool/printer purchase or PCA9685.

Physical parameters are sourced/estimated/unknown in physical_spec.json, not measured.
CAD/model/accounting derive from that ledger. The policy still sees only IMU-derived
gravity/gyro, applied command acknowledgements and previous actions (90values);
no true pose, velocity, joint feedback, contacts or forces. Diagnostics/rewards may
use simulation truth. Safe command intervals are not mechanical stops.

## Evidence and limits

- Current local report:VALIDATION_CURRENT.md; artifacts:validation/2026-10-24/print_revision/final/.
-37tests pass, including eight-pad contacts, whole-foot cylinder/plate heights,
  component ownership, alternative-budget accounting and package quantities/hashes.
- Current estimated mass197.053g. No infill-adjusted/measured mass claim.
-0modeled collisions does NOT clear physical fit: horn/screw shapes, servo ear positions,
  printed tolerances/layer strength, cables/ties/tool access remain unknown. Historical550
  proxy intersections were replaced by sourced M2shapes at estimated positions; old
  records retained, no claim of550physical fixes. Named PCB/header attachment exception only.
- HOME stands30s; manual scripts and PPO still fail lifted walking. Quasi-static HOME
  single-foot torque~0.0657Nm;2xmargin~0.1314exceeds0.08Nm model estimate. Do not
  increase torque or train longer simply to hide these failures.
- Source/config identity:`4d3b0dcbad59774b12f9c908c74446f6bf7452d5bdf34a08f07cf4271cc15019`.
  Pre-r2policies/UF2are historical and rejected by current deployment; no relabelling.
  Current2048smoke policy matches provisional twin, **not** physical calibration.
- All physical/manufacturing/formal gates remain false. Default invalid calibration
  cannot policy-arm. Software STOP does not isolate servo power.

## Exact next task

1. Obtain **specific permission** for current STL quotation uploads toMeltlab, or have
   user return exact-file quotes. Automatic approval review blocked the upload because
   it shares design data externally without named-provider authorization. No upload,
   supplier message or purchase occurred. Public reviews exist; no new price invented.
2. Close budget and actual horn/ear/screw dimensions; test mounting sample before full
   frame. Include every finishing/sample/delivery charge. Current basket alreadyoverEUR100.
3. Measure plant/current/IMU and assemble/weigh only after approval. Update measured
   twin/version, then validate lifted steps before larger training or deployment.

```bash
.venv/bin/python -m pytest -q
.venv/bin/python tools/budget_gate.py #1, active basket over cap before prints
MPLCONFIGDIR=/tmp/s6-mpl .venv/bin/python tools/prepare_print_order.py
.venv/bin/python tools/check_clearance.py #1, unresolved interfaces
```

Human-facing instructions/packages:SUMMARY.md,cad/QUOTE_REQUEST.md,cad/ASSEMBLY.md.
Historical sources/quotes:history/2026-10-24/pre_print_revision/ and previous validation
folders. Earlier in-turn geometry results are under development_superseded/ and must
not be reported as final. No stage is physically verified without real measurement data.
