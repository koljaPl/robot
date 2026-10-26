# School Biped S6: start here

Read `SUMMARY.md` first: the short plan, purchase/cost snapshot and AI next task.
Then read `docs/STATUS.md` and only the relevant stage in `docs/ROADMAP.md`.
Authoritative full plan: root `PLAN.md` (phase overview first, then detailed tasks).
Use the detailed handoff only for relevant reference; do not reread all embedded code.

## Goal and constraints

- School question: From Simulation to Reality: How does a robot learn?
- Six joints: left hip/knee pitch/ankle roll, then right hip/knee pitch/ankle roll.
- Coordinates: x forward, y left, z up; software units m, kg, rad, s.
- 15–20 cm, broad feet, lightweight, repairable; walking precedes extensions.
- PC inference over USB, wired servo power, no battery or onboard neural inference.
- Preferred delivered cost EUR 50–75; hard maximum EUR 100 including every part,
  VAT, shipping and any paid assembly preparation. No weaker-servo substitution.
- User can solder: self-prepared harness/headers, no mandatory helper labour.
- Active route: user-arranged classmate PETG printing, seven frame parts +two separate fit samples.
- Eight ordinary TPE pads; no printed TPU soles or filament spool in active basket.
- No printer purchase. Student does no mechanical drilling/cutting/bending; service finishes holes.
- No purchases or supplier messages are authorized by the implementation task.

## Authoritative inputs

- `procurement.json`: exact basket, quotations, dated source evidence, unresolved costs.
- `physical_spec.json`: geometry, rigid-body component ownership and physical parameters.
- `robot_config.py`: shared policy timing, action mapping and randomization hypotheses.
- Calibration records: per-servo pulse mapping and IMU alignment/bias; examples are invalid
  for policy deployment until measured and explicitly validated.
- Source code is authoritative over copies embedded in generated documentation.
- Current frozen script: `docs/baselines/scripted_bench_tools.json`; both r2 registries
  are historical. Exact replay/metrics, not hardware/training approval.

## Evidence and gates

- Label parameters sourced, estimated, measured or unknown, with evidence/date.
- Distinguish planned, implemented, locally verified, physically verified and blocked.
- A compiled firmware image is not an electrical test. Standing is not learned walking.
- Hardware measurements, print fit and delivered quotations cannot be invented.
- Count full material/consumable packs; tools/printer separate but included in initial cash.
- Unknown tools, frame hardware, stock or postage must remain unknown, not free.
- Unknown costs are never zero. Budget and fit must pass before recommending procurement.
- 2026-10-26 user completes design/printing decision: classmate prints; price unknown,
  excluding delivery. No printer purchase/upload/messages by AI; no repeat quote-search loop.
- Selected controller: bare Raspberry Pi Pico 2 RP2350; SDK target pico2. Pins and
  51x21mm footprint unchanged;3g board mass/3.5mm populated envelope still estimates.
- Priced subtotal now106.49EUR before unknown print/horn extras. Financial≤100 gate
  remains false; user acceptance is not a fabricated numeric quote or physical fit.
- Model S6-PETG-pad-r2-pico2; new identity685e3802…; all prior policies/UF2historical.
- Print-only deliverable: `print_for_classmate/` +ZIP; two fit samples before7frames.
  No combined duplicate plate/printed horns/TPU; physical sample and strength checks pending.
- User confirmed25337 Germany and PC USB-A on2026-10-23: no adapter required.
  USB-A–Micro-B data cable remains required; recheck final checkout for25337.
- Physical stages need the user's assembly/measurements; continue independent software work.
- Mechanical stops are not software command limits. Do not invent passive supporting stops.
- Never expose true joint angles, pose, translation, velocity or contact to the policy.
- Simulation truth is allowed for dynamics, rewards and explicitly separated metrics.
- Applied command targets are acknowledgements, not measured shaft feedback.
- Software stop is not physical motor-power isolation. Boot disarmed; never auto-arm.

## Work and verification

```bash
source .venv/bin/activate
python -m pytest -q tests  # avoid collecting copied historical test modules
python tools/firmware_config.py  # default invalid calibration cannot policy-arm
python tools/budget_gate.py  # default active commercial route;1=over cap,2=incomplete
python tools/prepare_print_order.py  # two quotation ZIPs; never manufacturing approval
```

- Inspect relevant code before edits; preserve historical `docs/validation/` evidence.
- Write new experiment artifacts under a new run directory, with source/config/model hashes.
- Rebuild CAD/model after physical edits; check mass, axes, contacts and clearances.
- Do not run `sync_frame_mass.py` over measured masses; it is for prototype CAD estimates.
- Never resume a policy across changed action mapping, preprocessing or physical identity.
- Default training: CPU PPO, 1024-step rollouts; 2048 smoke, at most 50000 pilot;
  final A/B seeds 0,1,2, equal budgets at most 1000000 each, rounded down to rollouts.
- B starts from the same initial weights as A, not from a nominal-pretrained policy.
- Validation seeds 2000–2004; final test seeds 1000–1009. Do not tune on final tests.
- Full experiments require the stage gates; provisional tests must say provisional.
- All saved policies and older UF2 are historical after the offset correction; use isolated
  replay, never relabel fingerprints. No current-compatible policy has been trained.
- Current Pico2 preparation ELF/UF2 is locally cross-built with invalid calibration; no physical test.
- Rebuild after fingerprinted changes; this preparation builder refuses measured policy calibration.
- The nominal pilot and scripted lifts failed: diagnose fit/model/measurements before
  repeating or extending training; do not increase torque just to force a simulated lift.
- `docs/REFERENCE_GAIT.md`: handoff script gives4alternating nominal steps,
  mirrored,6.60cm/30s; five randomized draws give0–1steps. Target30cm fails.
  Raw2ms audit retained; no measured-reference/physical/formal-training approval.
- `docs/SENSITIVITY.md`:29 one-factor cases per old/corrected identity;55tests pass.
  Physical offsets now enter actuator bias, never clipped away at command limits.
  Nominal unchanged; all12 ±1° offset probes lose steps.73credited steps raw-audited.
- Latest full suite:121passes (2026-10-26 firmware build);55above is
  the earlier offset checkpoint. Expanded task IDs/gates: root `PLAN.md`.
- WP2 intake implemented: `tools/validate_measurement.py`, provenance template and tests.
  Never approve calibration automatically; synthetic data remains synthetic.
- Manual preview/control and measured-baseline parity now locally verified; hardware pending.
- Next AI: validate actual receipts/fit/bench records when supplied; otherwise keep gates closed.
- Firmware build instructions/pins: firmware/README.md; no flash/arm, tuning or new PPO.
- User/classmate next: fit sample on actual servo/horn, then full frame; measure/weigh.
- Stop at the agreed training cap and report failure honestly if walking is unmet.

## Documentation and packaging

- Start each work chunk with a brief phase/done/next update; read root `PLAN.md`.
- Update `PLAN.md` after every completed task, scope change, failed check or blocker,
  BEFORE reporting completion: date, change, evidence, remaining work and exact next action.
- Synchronize STATUS/SUMMARY; do not maintain a competing full plan elsewhere.
- User ordering started; exact ordered items/paid prices/arrivals unknown until supplied.
- Keep `SUMMARY.md` brief and synchronized with the authoritative ledgers.
- Update `docs/STATUS.md` after each completed work chunk: evidence, blockers, next action.
- Keep `docs/ROADMAP.md` gates synchronized; retain the German school introduction in README.
- Edit handoff template/reference sources, then run `python tools/build_handoff.py`.
- Generated handoff must contain the actual current code and its original 19 sections.
- Packaging must use an explicit source/artifact allowlist. Never package `.aws`, `.codex`,
  `.agents`, `.git`, credentials, toolchains, virtual environments or private local files.
- Claims in final reports must distinguish historical, newly executed and physical results.
