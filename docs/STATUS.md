# Current project status

Updated **2026-10-23**. **Nothing purchased, assembled, flashed or physically tested.**
Start with SUMMARY.md and AGENTS.md; use this file for evidence and ROADMAP.md for gates. Do not restart broad research.

## Current checkpoint

Independent software preparation is implemented and locally checked. Hardware
feasibility, sample fit and calibration remain blocked. The twin is **provisional**,
not calibrated. Walking is **not achieved**. No formal measured A/B experiment or
physical transfer has taken place.

| Stage | State | Actual evidence / blocker |
|---|---|---|
| Requirements / entry | implemented | AGENTS.md, ROADMAP.md, this file; six joints and EUR100 maximum retained |
| A: hardware research | blocked | Two soldering routes in procurement.json; shared subset EUR95.91 before frame; standard kit unverified; own-print subset EUR118.43 (EUR18.43 over cap), no printer access; unknown horn/print/tool costs remain |
| B: mechanics | implemented / blocked | Native-PWM revision removes PCA envelope; CAD/ledger agree at199.4g estimated;55poses yield550 unreviewed fastener-proxy overlaps, no manufacturing release |
| C: bench/interface | locally verified | C++ official Pico SDK2.3.1 build/UF2; Python host/bench/deployment, persistent compiled calibration, explicit arm/watchdog/CRC/fingerprints; no electrical test |
| D: twin/RL | locally verified provisional |29tests, compilation/mass/axes/inertias, Gym/SB3, clipped commands, discrete delay, corrected reward, gait exploit tests; measured response and lifted-step reference still missing |
| E: experiments | locally verified partial | A0 total49152steps; A/B0 paired2048smokes; validation2000–2004, CSV/aggregate/videos/checkpoints; zero walking; formal seeds0/1/2 blocked |
| F: physical/calibration/transfer | planned / blocked | No hardware; procedures, data templates, bench/deployment tools and report scaffold ready |
| Extensions | planned | Conditional on stable walking; not started |

## Selected architecture and authoritative inputs

- Six Waveshare15024 MG90S, hip pitch/knee pitch/ankle roll per leg.
- Existing prototype Pico H **direct native PWM** GP0,1,2,3,6,7; MPU6050 GP4/5;50Hz commands/200Hz IMU.
  PCA9685 removed from current basket/spec because unavailable and extra mounting conflict.
- Wired5V/5A PSU with separate USB logic and common ground. Input socket now sourced5A; branch ratings and
  MG90S3.3V signal threshold remain unresolved. No programmable hardware torque cap.
- Basket/evidence: `procurement.json`, `docs/PROCUREMENT_ACTIONS.md`, `SERVO_COMPARISON.md`.
- Geometry/mass/dynamics/provenance: `physical_spec.json`; generated `robot.xml`,
  `docs/mass_properties.json`; editable `cad/build_frame.py` and assembly/quote brief.
- Shared policy contract: `robot_config.py`, `servo_control.py`, `imu_observation.py`.
- Calibration/identity: `calibration.py`, invalid example in `calibrations/`.
- Firmware/PC: `firmware/`, `serial_robot.py`, `bench.py`, `deploy.py`, `HARDWARE.md`.
- Training/evaluation: `train.py`, `evaluate.py`, `tools/experiments.py`, `EXPERIMENT.md`.

## Locally verified results (not hardware evidence)

-29pytest tests passed;49installed Python packages pass dependency compatibility check.
- Seven generated CAD-frame masses match the ledger; every servo assigned once;
  aggregate inertias positive/physical. Six hinges/position actuators compile.
- Unknown mechanical stops removed from MJCF; safe command bounds remain enforced.
- Reward backward displacement fully charged; closed cycles gain no positive progress.
- Toe pivots, hops, in-place lifts, stance slip and stationary lifts followed by sliding
  fail synthetic gait tests; valid translating alternating steps are credited.
- Native C++ state machine tests cover disarmed startup, invalid calibration,
  corrupt/range/stale/replayed packets, queue delay, slew, PWM bounds and100ms watchdog.
- Default invalid example cannot policy-arm; deployment rejects it before opening USB.
- Model/calibration/file fingerprints checked on reload. A/B initial policy hashes match.
- A0 resumed2048→49152 (not49152extra). Checkpoint selected by success/gait/reward
  was at10240steps; validation success and qualifying distance were zero at every checkpoint.
- Selected A0, seeds2000–2004: nominal mean distance0.008577m, speed0.000286m/s,
  reward6.03602,30s,0/5falls,0walking; randomized mean0.008673m,reward6.03637,0walking.
- Home baseline also stands30s with essentially zero travel. Standing is not learning evidence.
- Matched2048step A/B smoke validation completed; not a final robustness comparison.
- Scripted46s stand/lean/lift attempts (including level-foot/reversed-lean variants)
  stood without falling but produced no sustained3mm whole-foot lifts. Reference gate stays false.
- Three30s640×48050fps videos exported; representative frames/assembly drawing inspected.

Evidence: `docs/VALIDATION_CURRENT.md` and `docs/validation/2026-10-23/` contain
source snapshots, hashes, CSV/JSON, models, TensorBoard, videos and invalid-calibration UF2.
Original2026-10-08 evidence under `docs/validation/` is historical and incompatible.
Final controller parsing was corrected to fixed-width64bit for uint32 timestamps.
Current controller hash is `3d93f768188c8c55c903658192be75b87124f9a62852720fb5d2fd5b54666a8a`.
Archived training hash is `1641779be26172bcb40bd2b94d93a0974f722a676ba6aa2249ec310a8dbf7a1f`;
all those policies are historical and intentionally rejected by current deployment/evaluation.
Review them with `tools/replay_snapshot.py`, which isolates the exact archived source.
This parser-only change leaves simulated dynamics unchanged, but no policies were silently
relabelled or granted physical compatibility. Current invalid-calibration UF2 is under
`docs/validation/2026-10-23/final_control_revision/`.

The superseded first smoke in `runs/2026-10-23/smoke` predates the final fingerprint;
`final_smoke` is also historical after the controller revision. Review archived policies
only through the isolated replay tool; no saved checkpoint is currently deployment-compatible.

## Remaining blockers and unknown assumptions

1. **Procurement:** common soldering/pad subset EUR95.91 before standard frame;
   no complete stock kit verified. Own-print robot EUR118.43 before unknowns,
   EUR18.43 over cap. Full PETG spool/ear-fastener delivery counted. Bare Pico
   saves EUR0.80 including headers; no helper labour. No printer access/purchase.
   Current twin still Pico H/TPU, not proposed bare Pico/pads. Six-servo stock pending.
   No order/message/reservation. Historical commercial quotes remain unmodified.
2. **Fit:** ear/shaft/spline/horn geometry and fastener sweeps unmeasured.550proxy overlaps
   are not550confirmed physical bolt collisions. Resolve actual hardware interfaces first.
3. **Physics:** servo sustainable torque/current, loaded response/latency/backlash, supply
   droop, actual printed masses/COM, friction and IMU bias/alignment are unmeasured.
  0.08Nm/gains/damping and conservative DR ranges remain explicitly estimated.
4. **Motion:** no validated manual lifted-step reference; both PPO pilot and reference
   attempts show no qualifying gait. Do not increase force or train millions to hide this.
5. **Hardware:** firmware has compiled, not run on a Pico. Watchdog/PWM/USB/IMU electrical
   timing, signal levels, cutoff, harness and real safety need physical bench verification.

## Exact next task / executable checks

**Next:** find an exact compatible standard six-joint frame with every link/foot/horn
connection and full VAT/delivery price to25337. Only EUR4.09 remains in the current
shared basket before all mechanical extras. If none passes, report the missing
interfaces/cost; do not buy a printer or resume commercial-print quotations by default.

```bash
.venv/bin/python -m pytest -q
.venv/bin/python tools/budget_gate.py --scenario all # exit1, own route over cap
.venv/bin/python tools/prepare_local_print.py # layouts only, not released
.venv/bin/python tools/check_clearance.py # exit1, unresolved proxy conflicts
```

User can solder; use the one-servo/IMU bench procedure when hardware is available.
No physical gate can pass from local checks. See FRAME_ROUTES.md and procurement ledger.

## Historical commercial-print follow-up evidence

`docs/procurement/2026-10-23/quotes.json` records actual STL-based printing prices,
not public example allowances. The sole quote and Funduino policy have saved DOM;
the original compact-PETG checkout text was recovered from this session transcript
after its tab expired (no screenshot).
`tools/quote_layout.py` creates quotation-only unchanged-geometry batches, with
source hashes. Actual layer orientation, fit, bonding and grip remain unverified.
No physics/control code or current identity changed. Prior basket preserved under
`docs/history/2026-10-23/pre_delivery_check/`. User confirmed delivery postcode25337 Germany and PC USB-A on2026-10-23;
no adapter needed. Existing quotes remain historical standard-Germany quotes;
final postcode-specific checkout is pending.

## Soldering/frame comparison update

- **Implemented:** shared/scenario procurement accounting, separate printer/tools/initial
  cash reporting, self-solder harness instructions, bare-Pico header accounting,
  ordinary self-adhesive pad candidate and unchanged-part individual180mm plate export.
- **Sourced:** bare Pico4.10, solder10g1.90, selected black1kg PETG12.99;
  A1mini non-Combo189in stock, EnderV3SE standalone169orderable listing; both publish
  free standard German shipping, postcode checkout pending. Pads3.55+5.95shipping.
- **Not selected/measured:** replacement mechanics, actual pad friction/adhesion, all
  servo interfaces, branch ratings and any printer operation. No physical spec,
  dynamics, control source or configuration identity changed.
- **Historical:** pre-soldering guides/ledger in history/2026-10-23/pre_soldering_routes/;
  commercial quotations retained as alternatives only. No printer/helper purchase.
- **Newly locally verified:**32pytest tests pass (including three new route/print
  checks);55poses still report550estimated fastener-proxy conflicts (expected
  nonzero check, no clearance approval). Unchanged model regenerated identically;
  accounting199.431g and identity unchanged. New logs are in
  validation/2026-10-23/soldering_routes/. Earlier training numbers remain historical.
  No physical result or new walking/training claim.
