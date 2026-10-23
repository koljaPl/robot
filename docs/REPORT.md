# School report: From Simulation to Reality — how does a robot learn?

**Working report, not a completed physical experiment.** Nothing purchased.
Use exact newly recorded metrics from STATUS/validation artifacts; do not copy
historic numbers into a measured-results table.

Research question: Can a cheap six-servo biped learn alternating forward steps,
and does measured domain randomization improve transfer versus fixed simulation?
Hypothesis: modest measured parameter variation may improve robustness. This is
not yet demonstrated and may be outweighed by missing feedback/cheap gearboxes.

Methods: hardware-first budget/fit gates; component mass ownership; bounded
position targets and raw-IMU gravity history; PPO; paired initialization/seeds;
validation/test separation; explicit gait acceptance and equal physical trials.
Explain rewards as feedback, training as repeated simulated attempts, and policy
as a learned mapping from sensor history to safe target commands.

## Evidence table to maintain

| Claim | Current status / source |
|---|---|
| Complete delivered robot under€100 |Unresolved; procurement.json has null required costs|
| Runnable provisional SIM/control software |See docs/VALIDATION_CURRENT.md for executed checks|
|30s standing |Simulation reference/control evidence; no physical test|
|0.3m alternating walk |Not established; reward alone is insufficient|
| Randomization improves transfer |No real A/B data; formal comparison blocked|

For final report, insert separate tables: nominal/randomized simulation results
per training seed/condition; SIM-vs-real paired trials with uncertainty, falls,
qualifying distance/steps and total trial counts. Show selected baseline, early,
late and failed videos. Include budgets, source dates, calibration methods,
policy hashes, step cap and trial exclusions with reasons.

Discuss: servo backlash/load/voltage variation, no encoder feedback, uncertain
sustainable torque/current, print fit/strength, friction/soft mat, cable effects,
simulation force diagnostics vs visually observable real steps, conservative
metric false negatives, reproducibility limits and cost/availability changes.
If walking or transfer fails, explain the observed failure and what evidence
would distinguish an actuator/mechanics problem from a learning problem.

Do not invent physical results or use a different policy for a claimed paired
comparison. Turning, terrain and recovery belong only in future work after the
walking target succeeds.
