# School Biped S6: start here

Read `SUMMARY.md` first: the short plan, purchase/cost snapshot and AI next task.
Then read `docs/STATUS.md` and only the relevant stage in `docs/ROADMAP.md`.
Detailed task dependencies/owners/done criteria: `docs/DEVELOPMENT_PLAN.md`.
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
- Active route: commercial PETG printing, seven frame parts +two separate fit samples.
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
- Current frozen script: `docs/baselines/scripted_r2_offset_corrected.json`; predecessor
  `scripted_r2.json` is historical. Exact replay/metrics, not hardware/training approval.

## Evidence and gates

- Label parameters sourced, estimated, measured or unknown, with evidence/date.
- Distinguish planned, implemented, locally verified, physically verified and blocked.
- A compiled firmware image is not an electrical test. Standing is not learned walking.
- Hardware measurements, print fit and delivered quotations cannot be invented.
- Count full material/consumable packs; tools/printer separate but included in initial cash.
- Unknown tools, frame hardware, stock or postage must remain unknown, not free.
- Unknown costs are never zero. Budget and fit must pass before recommending procurement.
- Active commercial basket: common95.56 +ear-fastener delivery9.53 =105.09EUR BEFORE
  print/sample/horn extras; minimum known shortfall5.09EUR for this basket. No procurement.
- New quotes must identify current geometry hashes; old commercial/own-printer prices are historical.
- Model revision S6-PETG-pad-r2 owns bare Pico+headers and8discrete pad contacts.
- Manufacturing remains blocked by real horn/ear/screw fit, finishing/layer strength and budget.
- Automatic approval review blocked Meltlab STL upload. No upload/message/order occurred;
  get specific authorization for that provider/payload or let user return the quote.
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
python -m pytest -q
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
- All saved policies/UF2 are historical after the offset correction; use isolated
  replay, never relabel fingerprints. No current-compatible policy has been trained.
- Current firmware header is regenerated invalid; ARM/Pico firmware build must be repeated before flash.
- The nominal pilot and scripted lifts failed: diagnose fit/model/measurements before
  repeating or extending training; do not increase torque just to force a simulated lift.
- `docs/REFERENCE_GAIT.md`: handoff script gives4alternating nominal steps,
  mirrored,6.60cm/30s; five randomized draws give0–1steps. Target30cm fails.
  Raw2ms audit retained; no measured-reference/physical/formal-training approval.
- `docs/SENSITIVITY.md`:29 one-factor cases per old/corrected identity;55tests pass.
  Physical offsets now enter actuator bias, never clipped away at command limits.
  Nominal unchanged; all12 ±1° offset probes lose steps.73credited steps raw-audited.
- Next AI task: prepare/validate measured calibration data when available; keep script
  frozen. Read `docs/BUDGET_REVIEW.md` before repeating consolidation research.
  Eight taller FIX-RF-003 pads are an unselected96.79EUR comparison, not a complete
  affordable robot; only3.21EUR remains for all unknowns. Current pads/twin unchanged.
  No nominal tuning/stronger motors/relaxed acceptance/more PPO. Human: quote and fit.
- Stop at the agreed training cap and report failure honestly if walking is unmet.

## Documentation and packaging

- Keep `SUMMARY.md` brief and synchronized with the authoritative ledgers.
- Update `docs/STATUS.md` after each completed work chunk: evidence, blockers, next action.
- Keep `docs/ROADMAP.md` gates synchronized; retain the German school introduction in README.
- Edit handoff template/reference sources, then run `python tools/build_handoff.py`.
- Generated handoff must contain the actual current code and its original 19 sections.
- Packaging must use an explicit source/artifact allowlist. Never package `.aws`, `.codex`,
  `.agents`, `.git`, credentials, toolchains, virtual environments or private local files.
- Claims in final reports must distinguish historical, newly executed and physical results.
