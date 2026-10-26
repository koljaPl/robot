# Hardware-first execution roadmap

Updated **2026-10-26**. This is the short map; the
[complete execution plan](../PLAN.md) contains all phases, completed work,
WP1–WP11 procedures, owners, affected files, acceptance evidence and failure decisions.
[STATUS](STATUS.md) records evidence; ledgers remain authoritative.

## Current user decision / next phase

2026-10-26: design and classmate-printing arrangement COMPLETE by user confirmation;
Pico2 selected. Exact printing/transport price remains unknown, not free. This closes
provider-selection research and starts WP2, without claiming physical fit or a numeric
budget pass. [Print folder](../print_for_classmate/00_START_HERE.md).
Measurement-intake/provenance checker implemented; manual six-joint utility and
measured-baseline calibration parity and Pico2 preparation firmware now locally verified.
Initial bench safeguards and locked-fit response review locally verified;186tests pass;
no new PPO. [Response review](RESPONSE_REVIEW.md).
[Firmware build](../firmware/README.md), [initial bench guide](BENCH.md).

## Previous checkpoint (2026-10-25; historical costs/identity)

Implemented: provisional S6-PETG-pad-r2 CAD/twin, common control interface,
firmware/bench foundations, Gym/PPO/evaluation and diagnostic tools. Latest
recorded full suite:58passes. No physical robot, measured calibration or current
compatible learned policy. Four scripted nominal steps/6.60cm in30s fail30cm
walking acceptance; small unmeasured parameter changes remove steps.

The selected dated basket is€105.09 BEFORE print/sample/horn extras, at least
€5.09 over cap. No exact complete affordable quote or actual fit exists. The
unselected taller-pad comparison is€96.79 before unknowns; it is not a complete
robot and cannot silently replace current contact geometry. See BUDGET_REVIEW.

## Dependency-ordered work

| Stage / original phases | Detailed work packages and owner | Completion gate |
|---|---|---|
| Entry /0,13 | Student+AI: requirements, status, plan, evidence | Constraints/next task unambiguous; claims tied to real evidence |
| A /1 | User-complete design/printing choice, Pico2 selected; actual costs recorded later | Decision complete; numeric budget and physical fit are separate, still unverified |
| B preparation /3,6,8,9 | WP2 AI: measurement intake, fit quality, six-joint manual utility, initial bench safeguards, response review and measured-baseline parity | Mocked/synthetic tests/clear procedures; no physical claim; can proceed alongside A |
| B hardware /1,8,9 | WP3–WP5 student+AI: bench, measured interfaces, sample fit, finished assembly/weighing | Electrical/fit records, safe manual control, real mass ownership |
| C /2,3,4,9 | WP6–WP7 student+AI: measured twin, observation parity, model/reference validation | Measured calibration and reviewed weight transfer/lift; all five gates backed by evidence |
| D /5,6,7 | WP8–WP9 AI: bounded matched fixed/DR training and held-out evaluation | Equal initialization/budgets, compatible identities, actual gait results/CSV/videos |
| E /8,10 | WP10 student+AI: supervised standing, short steps, progressive policy trials | Compatible measured setup, physical safety checks and actual trial records |
| F /11,13 | WP11 student+AI: equal physical A/B, comparison, report/presentation | Recorded successes/failures, uncertainty, cable effects and reproducible handoff |
| Extensions /12 | Future scoped work: turning, recovery, terrain | Stable walking first |

**Next AI:** validate actual order/fit/bench records when supplied. Pico2 preparation
firmware, manual control and baseline calibration parity are locally verified. Ordering has started according to user;
actual items/paid prices/arrivals unknown. Keep root PLAN updated after each chunk. Keep the reference frozen; no more nominal
tuning/PPO, stronger fictitious actuation or repeated identical budget searches.
**Next human/classmate:** print/test2sample pieces on actual servo/horn, then7frame
parts if fit passes; record dimensions, costs and weights. No more Meltlab upload/
provider-selection loop is needed for this arrangement. Physical checks stay pending.

## Contracts to preserve

- Six actions in joint order L hip/knee/ankle then R same; +Y pitch, +X roll.
- 50Hz commands,200Hz IMU processing,2ms physics; actual timestamps matter.
- Five18-value observation frames: estimated gravity, gyro, acknowledged targets
  and previous actions. No perfect orientation, shaft feedback, velocity or contacts.
- Safe command limits are not unknown mechanical stops. Torque is a simulation
  estimate, not programmable hardware current/torque protection.
- Boot disarmed, explicit arm,100ms watchdog, bounded/versioned CRC packets,
  persistent measured calibration/fingerprints; STOP is not physical DC isolation.
- Current Pico2 identity begins`685e3802`; saved policies/older UF2are historical.
  Current preparation ELF/UF2 is locally cross-built with invalid calibration.
  Use snapshots; never relabel old checkpoints or headers.
- Smoke2048, pilot≤50000 (49152actual), final≤1000000 (999424actual) each for
  A/B seeds0,1,2. Compatible pilot counts toward final total; B never resumes A.
- Match A/B initial weights and budgets. Validation2000–2004 selects success,
  gait distance, reward; reserve1000–1009 for final tests, with HOME/untrained baselines.
- Acceptance: separate30s stand; body AND qualifying gait progress≥0.3m/30s,
  ≥3mm/40ms full-foot lift,≥5mm touchdown,≤3mm stance slip,≥2steps per side and
  ≥3alternations, no fall. Physical thresholds need video/ruler evidence.
- Stop/report failure at the agreed cap. No simulation result clears a physical gate.

## Evidence/continuation rule

Record each step as planned, implemented, locally verified, physically verified
or blocked. Keep all five gates false until actual evidence closes them. Preserve
historical trials, quotes and policies. Follow the detailed plan's next executable
task when human-dependent work is blocked; do not restart already completed research.
