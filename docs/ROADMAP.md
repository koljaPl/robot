# Hardware-first execution roadmap

Approved 2026-10-23. Preserve six joints and EUR 100 maximum delivered cost.
States and actual evidence belong in STATUS.md. No stage is physically verified without data.
Detailed tasks, owners, files, evidence and dependencies: [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md).

| Stage / original phases | Work and owner | Completion gate |
|---|---|---|
| Entry / 0,13 | AI: concise AGENTS, STATUS and this roadmap; preserve historical evidence | New session can identify constraints, sources, blockers and next command quickly |
| A / 1 | AI: active commercial PETG quotation, complete sample/frame finishing and delivered costs; soldered electronics/ordinary pads; no purchases/messages | Complete sourced basket <=EUR100, fit information or explicit unresolved evidence/shortfall |
| B / 1,2 | AI: reconcile CAD and physical ledger, PCB/case/frame clearance, fasteners; user/supplier: sample fit | Checked geometry; no unverified manufacturing release; solid masses remain estimates |
| C / 3,8 | AI: Pico SDK C++ firmware, PC bench/client, bounded protocol and persistent calibration | Firmware builds and host tests pass; actual electrical timing/cutoff still needs bench |
| D / 2,3,4,9 | AI: common limits/preprocessing, realistic command scheduling, reward and metrics; user: measured parameters | Reproducible twin; no fake stops/positive closed-loop progress/sliding success; measured vs provisional explicit |
| E / 5,6,7 | AI: bounded nominal pilot, equal-budget fixed/DR models, held-out evaluation and videos | Actual gait results, including failures, with fingerprints and complete per-episode metrics |
| F / 8,9,10,11,13 | User: bench, assembly, calibration and physical trials; AI: firmware/tools/data analysis/report | Real test data; frozen compatible policies; equal trials and alternating A/B order |
| Extensions / 12 | Future: turning, terrain, recovery | Stable baseline walking first; no automatic scope expansion |

Current checkpoint: quotation CAD and matching r2 twin implemented; real fit,
strength and complete delivered quotation remain blocked. Common95.81EUR plus
priced ear hardware/delivery9.53EUR already exceeds100EUR by5.34EUR before printing.
Next human action: authorize exact current-STL quotation upload toMeltlab or return
its quote/settings/hashes; no order/message. Then actual servo/horn measurements and
sample fit are required. Current49tests and historical2048step smoke are local evidence only.
The newest handoff script gives4qualifying alternating nominal steps, mirrored,
6.60cm torso advance in30s. Five randomized draws drop to0–1steps. The30cm goal
still fails; do not expand training to hide this or assume measured robustness.
Earlier offline diagnosis found154ideal poses, including mirrored20° prepared
states that hold single support for3s after initialization; the original two
HOME transition orders failed. Anchored holds do not clear the reference gate. Next independent
AI work is calibration-analysis preparation and parameter isolation with the
script frozen; see REFERENCE_GAIT.md. Guessed plant data and fragile nominal
steps do not clear the measured-reference/training gate.

## Fixed engineering contracts

- Joint order L hip/knee/ankle, R hip/knee/ankle; +Y pitch, +X roll.
- Six normalized target-position actions; five 18-value observation frames.
- Observations use gravity estimated from IMU, gyro, applied targets and previous action.
- 50 Hz policy/commands; 200 Hz IMU; 2 ms physics. Real timer dt is recorded.
- Torque limits are simulation estimates, not programmable hardware torque protection.
- Persistent calibration supplies zero pulses, gains, signs, pulse/safe-angle limits and IMU alignment.
- Boot disarmed, explicit arm, 100 ms fresh-command watchdog, bounded CRC frames and STOP.
- Invalid calibration/config identity forbids policy operation; single-channel bench mode is explicit.

## Experiment contract

- Smoke 2048 steps; pilot <=50000; final <=1000000 per A/B condition and seed 0,1,2.
- Round down to complete 1024-step rollouts. Unchanged pilot counts toward its final run.
- A nominal and B randomized start from matching initial weights and equal budgets.
- Validation seeds 2000–2004 select success, qualifying gait distance, then reward.
- Test seeds 1000–1009 are held out until final reporting; evaluate both conditions.
- Keep home and untrained baselines. Save CSV, summaries, model/config hashes and videos.
- Standing alone is not walking: retain 3 mm/40 ms lift, non-sliding forward touchdown,
  alternating support and >=0.3 m qualifying gait progress within 30 s without a fall.
- Initial success target also requires a separate 30 s stand test.
- If cap is reached without gait, report unmet target; do not extend automatically.

## Human-dependent sequence

1. Resolve delivered budget and component interfaces before ordering.
2. User solders/insulates short harness and headers; checks cutoff, one servo and IMU.
3. Record pulse mapping, directions, range, speed/strength/current/latency and IMU noise.
4. Confirm printed mounting sample on actual servo/horn, review layer/fastener
   clearance and complete delivered budget, then obtain frame and weigh bodies.
5. Validate all six joints, manual stand, watchdog, faults and cables.
6. Reconcile measured twin and configuration identity; retrain incompatible policies.
7. Policy stand, short steps, longer trials; use ruler/video, never IMU double integration.
8. Equal fixed/DR trials, alternating order, logs and failure records; school report.

When quotations or measurements block a stage, name the missing evidence and prepare
the precise question/data template. Continue independent software preparation. Do not
invent a quote or substitute simulation verification for physical verification.
