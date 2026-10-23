# Current project status

Updated **2026-10-23**. **Nothing purchased, assembled, flashed or physically tested.**
Read this after AGENTS.md, then ROADMAP.md for gates. Do not restart broad research.

## Current checkpoint

Independent software preparation is implemented and locally checked. Hardware
feasibility, sample fit and calibration remain blocked. The twin is **provisional**,
not calibrated. Walking is **not achieved**. No formal measured A/B experiment or
physical transfer has taken place.

| Stage | State | Actual evidence / blocker |
|---|---|---|
| Requirements / entry | implemented | AGENTS.md, ROADMAP.md, this file; six joints and EUR100 maximum retained |
| A: hardware research | blocked | Refreshed procurement.json; known-priced subset EUR78.91, total unknown; exact print/fastener/input/shipping evidence missing |
| B: mechanics | implemented / blocked | Native-PWM revision removes PCA envelope; CAD/ledger agree at199.4g estimated;55poses yield550 unreviewed fastener-proxy overlaps, no manufacturing release |
| C: bench/interface | locally verified | C++ official Pico SDK2.3.1 build/UF2; Python host/bench/deployment, persistent compiled calibration, explicit arm/watchdog/CRC/fingerprints; no electrical test |
| D: twin/RL | locally verified provisional |29tests, compilation/mass/axes/inertias, Gym/SB3, clipped commands, discrete delay, corrected reward, gait exploit tests; measured response and lifted-step reference still missing |
| E: experiments | locally verified partial | A0 total49152steps; A/B0 paired2048smokes; validation2000–2004, CSV/aggregate/videos/checkpoints; zero walking; formal seeds0/1/2 blocked |
| F: physical/calibration/transfer | planned / blocked | No hardware; procedures, data templates, bench/deployment tools and report scaffold ready |
| Extensions | planned | Conditional on stable walking; not started |

## Selected architecture and authoritative inputs

- Six Waveshare15024 MG90S, hip pitch/knee pitch/ankle roll per leg.
- Pico H **direct native PWM** GP0,1,2,3,6,7; MPU6050 GP4/5;50Hz commands/200Hz IMU.
  PCA9685 removed from current basket/spec because unavailable and extra mounting conflict.
- Wired5V/5A PSU with separate USB logic and common ground. Input/branch ratings and
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
use `final_smoke`, not that intermediate run. Never relabel an old checkpoint compatible.

## Remaining blockers and unknown assumptions

1. **Procurement:** exact delivered print/finishing/sole/fastener quote, horn/screw contents,
   rated input connection, Funduino shipping, available FF jumpers and any helper charge.
   EUR21.09 remains for all unknowns. No exact shortfall is known; total is not established.
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

**Next human-dependent task:** resolve the four precise supplier/checkout questions in
`docs/PROCUREMENT_ACTIONS.md`; obtain a file-specific delivered fit/print quote. No messages
or purchases have been sent. Do not order a complete frame before servo/horn sample fit.

**Next software command:**

```bash
.venv/bin/python -m pytest -q
.venv/bin/python tools/budget_gate.py # expected exit2, incomplete
.venv/bin/python tools/check_clearance.py # expected exit1, proxy conflicts
```

Then use received dimensions/quotes to replace unknowns; helper/user performs the one-servo
bench and IMU measurements in CALIBRATION.md. Provisional independent tooling is prepared;
formal training and physical completion remain blocked by `docs/gates.json`. Do not set a
gate true without linked evidence. Generated full reference: `docs/HANDOFF.md`.
