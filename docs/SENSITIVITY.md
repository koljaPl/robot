# Frozen-script sensitivity and offset correction — 2026-10-24

**Locally verified diagnostics; no physical calibration or new PPO training.**
The unchanged compact handoff script still produces four qualifying steps and
6.60cm torso advance in30s nominally. It fails the30cm walking target. One-factor
probes identify calibration priorities; they do not establish hardware tolerances,
failure probabilities or a global ranking of parameter importance.

## A calibration-error modelling defect was corrected

Previously `humanoid_env.py` clipped `applied_command + joint_offset` to the safe
command interval. That concealed part of an unknown shaft-zero error at command
bounds: up to0.939° of a1° ankle error in these probes. A software bound on a
requested angle cannot erase a real calibration error or guarantee shaft position.

For the model's unit-gear position actuators, the corrected force is
`kp * (bounded_command + offset - q) - kv * qdot`, subject to the existing
force/speed envelope. `kp * offset` enters MuJoCo's affine actuator bias; control
and acknowledged targets remain bounded in command coordinates. This follows
the documented [affine actuation law](https://mujoco.readthedocs.io/en/stable/computation/index.html#actuation-model)
and [position-actuator parameters](https://mujoco.readthedocs.io/en/stable/XMLreference.html#actuator-position).
Nominal bias is restored before each reset; errors do not accumulate.

Geometry, nominal gains/strength, action mapping, safe intervals, observations,
acceptance thresholds and the target sequence are unchanged. Unknown mechanical
stops remain absent. True equilibrium may lie outside a command interval when
calibration is wrong; this is a modelled error, never permission to operate there.

| Identity | Evidence / use |
|---|---|
| Historical `4d3b0dcb…` | [Original frozen registry](baselines/scripted_r2.json), old mixed-DR and first sensitivity study; replay its snapshot only |
| Current `b11ab929…` | [Offset-corrected registry](baselines/scripted_r2_offset_corrected.json), new nominal replay and corrected sensitivity study |

Full current fingerprint:
`b11ab9292c586ace4f2028c7061aa4ef279b6c84bd3966d2e806e0f96d01560b`.
Zero-offset nominal results and all17 non-offset probe trajectories are exactly
unchanged, including every recorded2ms trace column. **All existing policy checkpoints and UF2 images are historical and
incompatible with the current configuration.** No policy was relabelled or trained.
The regenerated firmware header remains invalid for policy arming; no new ARM
build or electrical test is claimed.

## Declared one-factor study

Each configuration has29cases: nominal,14 paired mechanical/dynamic endpoints,
one40ms delay,12 individual±1° joint offsets and one IMU-noise control. Each case
uses seed42, the same30s time-only targets, and nominal restoration before applying
one factor. These endpoints come from existing **estimated** randomization ranges,
not measurements. Uniform/torso mass changes also scale inertia, retaining each
body's local COM. Torso-only scaling changes the overall mass distribution.

| Factor changed alone | Low / high | Qualifying steps, low / high |
|---|---|---|
| All moving-body masses/inertias | −5% / +5% | 4 / 4 |
| Torso-body mass/inertia only | −5% / +5% | 0 / 1 |
| Sliding friction | −15% / +15% | 4 / 0 |
| Servo strength envelope | −15% / +15% | 4 / 4 |
| Shaft no-load speed envelope | −10% / +10% | 4 / 4 |
| Software target slew | −10% / +10% | 4 / 4 |
| Joint damping | −20% / +20% | 2 / 3 |
| Command delay | Nominal20ms /40ms | 4 / 4 |
| IMU noise scale | Nominal1.0 /1.2 | 4 / 4 |

| Individual corrected offset | −1° steps | +1° steps |
|---|---:|---:|
| Left hip |1|1|
| Left knee |2|1|
| Left ankle |3|1|
| Right hip |3|1|
| Right knee |1|1|
| Right ankle |1|3|

All12 offset cases lose at least one of the nominal four steps. Correcting the
clipping changes credited counts for right-hip−1° (1→3) and right-ankle+1° (4→3);
other unchanged counts do not imply unchanged trajectories. No corrected case
falls, but **none achieves walking success**. Root movement remains a separate
metric and cannot stand in for qualifying gait progress.

The target-slew endpoints give exactly the nominal trajectory: that limit is not
binding for this slow script. Increased IMU noise changes observations, while
motion stays identical because this script ignores them. This does not show that
a feedback policy can ignore IMU quality. Delay and shaft-speed results likewise
do not establish irrelevance for faster or feedback-controlled motion. The higher
strength endpoint is diagnostic only, not a new nominal torque recommendation.

![One-factor results](validation/2026-10-24/sensitivity_report_final/sensitivity.png)

[Per-case CSV](validation/2026-10-24/sensitivity_report_final/episodes.csv),
[73 independently checked credited steps](validation/2026-10-24/sensitivity_report_final/credited_steps.csv),
[hashes and report](validation/2026-10-24/sensitivity_report_final/summary.json).
The independent checker recomputes whole-foot≥3mm/≥40ms lift, forward touchdown,
stance motion and opposite support from2ms traces. No acceptance limit was relaxed.

## Evidence and reproduction

- Original29cases: `validation/2026-10-24/sensitivity/`; corrected29cases:
  `validation/2026-10-24/sensitivity_corrected/`. Each has mechanics/timing/offset
  batch manifests, executed source snapshots, runtime values and numeric NPZ traces.
- New nominal replay: `validation/2026-10-24/offset_correction/nominal/`.
  Its complete metrics exactly match the predecessor registry.
- Full suite: **55passed in14.93s**, `offset_correction/pytest.txt`. Tests include
  both outward offsets at every command bound, bias restoration, unchanged
  command bounds, isolated factors and IMU/physics separation.
- Corrected batch snapshots initially omitted the new registry input. It was
  appended with a separate `replay_inputs.json` hash record; executed source and
  original manifests/results were not replaced. Future exports include it directly.
- `sensitivity_report/` preserves an interrupted report-generation attempt caused
  by repeated NPZ decompression. It contains no completed result. The reviewed
  completed report is `sensitivity_report_final/`; no physics run was repeated
  to repair that reporting inefficiency.

```bash
# Source/model guard; no training. Use a fresh output directory.
MPLCONFIGDIR=/tmp/s6-mpl .venv/bin/python tools/sensitivity_probe.py \
  --cases nominal offset_left_ankle_plus --output runs/sensitivity_NEW
MPLCONFIGDIR=/tmp/s6-mpl .venv/bin/python tools/report_sensitivity.py \
  --legacy docs/validation/2026-10-24/sensitivity \
  --corrected docs/validation/2026-10-24/sensitivity_corrected \
  --output runs/sensitivity_report_NEW
```

Load traces with `numpy.load(path, allow_pickle=False)`; materialize each column
once before processing rows. Old evidence must be replayed from its source snapshot,
never by silently running the current environment under an old identity.

## Next decision

Keep this script frozen. After budget/fit clearance, measure **per-servo zero/gain
and repeatability, assembled body mass distribution/COM, actual pad friction,
and loaded actuator response/damping**. Also measure delay, current, IMU and cable
effects; this study does not eliminate those requirements. See [calibration](CALIBRATION.md).
Do not choose guessed friction, mass or stronger actuation just to regain four
steps. Reconcile measured parameters, issue a new identity, replay this reference
and check robust lifted steps before substantial PPO or any policy deployment.
All five release gates remain false; no new procurement or physical result exists.
