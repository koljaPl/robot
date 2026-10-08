# Executed verification — 8 October 2026

These are **local software results**. No hardware was purchased, assembled, weighed or tested. No printing quotation was obtained. The complete delivered BOM is still incomplete; `tools/budget_gate.py` exits 2 and prohibits procurement clearance.

Linux/Python 3.12 was used in `.venv`. The pinned runtime dependency set installed successfully; `uv pip check` reported all 47 installed packages compatible. `pytest` passed all **12 tests**, including MuJoCo compilation, mass accounting, positive joint directions, home contacts, 30 s neutral standing, finite bounded-random/limit command runs, action mapping, shaft lag, delayed/slew-limited commands, observation construction, exact seeded resets, randomization restoration, CRC/bounds, torque-independent pulse calibration and foot-step classification. The environment also passed SB3 `check_env`.

## Reproducible commands

```bash
MPLCONFIGDIR=/tmp/robot-mpl XDG_CACHE_HOME=/tmp/robot-cache .venv/bin/python -m pytest -q
.venv/bin/python tools/check_clearance.py
.venv/bin/python tools/torque_estimates.py
.venv/bin/python tools/budget_gate.py
MPLCONFIGDIR=/tmp/robot-mpl XDG_CACHE_HOME=/tmp/robot-cache .venv/bin/python train.py --steps 10240 --seed 0 --output runs/verified_smoke
MPLCONFIGDIR=/tmp/robot-mpl XDG_CACHE_HOME=/tmp/robot-cache .venv/bin/python evaluate.py --model docs/validation/smoke_checkpoint.zip --episodes 5 --seed 1000 --output docs/validation/nominal
MPLCONFIGDIR=/tmp/robot-mpl XDG_CACHE_HOME=/tmp/robot-cache .venv/bin/python evaluate.py --model docs/validation/smoke_checkpoint.zip --episodes 5 --seed 1000 --randomize --output docs/validation/randomized
MUJOCO_GL=egl .venv/bin/python evaluate.py --model docs/validation/smoke_checkpoint.zip --episodes 1 --seed 1000 --video --output runs/verified_video
.venv/bin/python train.py --resume docs/validation/smoke_checkpoint.zip --steps 1024 --seed 0 --output runs/resume_check
```

Training saved a 10,000-step checkpoint and a 10,240-step final model. The supplied `smoke_checkpoint.zip` is the **10,000-step checkpoint**, not the final model. Checkpoint reload and separate resumed 1,024-step training completed; resumed training is a software check, not an improved walking result. TensorBoard events and best/checkpoint saves were produced under `runs/verified_smoke`. Runs are ignored by Git; the evidence checkpoint, source training configuration, CSVs and video are retained under `docs/validation`.

The original training configuration predates the added source-hash reporting and stricter support/clearance metric. Neither changed actuator physics, observations or reward. Fixed-seed evaluations were rerun using the final evaluation code and are stored below. `manifest.json` hashes the delivered sources and records installed versions. Code/test passing does not establish policy quality.

## Observed policy results

The nominal-trained checkpoint was evaluated with deterministic actions on seeds **1000–1004**, separately with and without randomization. These are five episodes per condition, not enough to establish a robust failure probability. Fall rate is observed **0/5** in each condition.

| Metric | Nominal | Randomized |
|---|---:|---:|
| Mean distance | 0.0015243347 m | 0.0019358407 m |
| Mean forward speed | 0.0000508112 m/s | 0.0000645280 m/s |
| Duration per episode | 30 s | 30 s |
| Falls | 0/5 | 0/5 |
| Mean total reward | 6.00596345 | 6.00868410 |
| Qualifying lifted steps / alternations | 0 / 0 | 0 / 0 |
| Walking successes | 0/5 | 0/5 |

The achieved result is **simulation standing with slight drift**, not stable forward walking. The target of at least 0.3 m with alternating lifted steps in 30 s is unmet. Real standing/walking/transfer remain entirely unmeasured.

- [Nominal CSV](validation/nominal/episodes.csv) and [summary](validation/nominal/summary.json)
- [Randomized CSV](validation/randomized/episodes.csv) and [summary](validation/randomized/summary.json)
- [30 s visualization](validation/nominal.mp4), [inspected preview](validation/model_preview.png)
- [Saved policy checkpoint](validation/smoke_checkpoint.zip)
- [Torque calculations](validation/torque_estimates.json)
- [Finite CAD intersection report](validation/clearances.json)
- [Source/version manifest](validation/manifest.json)

## Mechanical/numerical boundaries

The explicit mass ledger totals **0.2084311334 kg**, with six servo masses assigned once. CAD has seven connected watertight frame meshes plus two sole boxes. The mesh audit checks home, zero, all low, all high, one swing and 50 random poses (seed 123): **55 poses** have no checked frame/frame or frame/assigned-servo-case intersection. Unmeasured ears, horns, screw access, all neighboring cases/boards/wires, continuous swept paths and structural strength are not certified by this finite audit.

No package accessory, shaft/ear/horn dimension, current, continuous torque, motor lifetime, power connector rating or frame manufacturing fit has been physically confirmed. The approved design gate remains outstanding. The twin and print files explicitly retain provisional status until those measurements and the delivered budget pass.
