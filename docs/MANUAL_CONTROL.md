# Reviewed manual movements

`manual_control.py` provides an **offline preview by default**. It does not run
a policy, open USB in preview mode, or approve physical standing. One-channel
unloaded calibration remains in `bench.py`.

```bash
.venv/bin/python manual_control.py \
  --sequence docs/templates/manual_home_only.json \
  --output runs/manual_home_preview_NEW
```

This uses the invalid example calibration only for an estimated command preview.
The output contains `trajectory.csv` at50Hz and a manifest with movement,
calibration/configuration/source hashes. Existing output directories are refused.
It does not change model parameters or release gates.

## Movement format

Use version1, the exact six-name `joint_order`, `initial_targets_rad` and a
nonempty list of `segments`. Each segment has `duration_s` and six `targets_rad`.
The included JSON is a HOME-only example; targets are radians in the shared joint
order, never degrees or generic servo0–180° angles.

Durations are positive multiples of20ms. Target transitions are linear and must
already respect calibrated angle and slew limits; invalid input is rejected,
not clipped. At most100segments and30s of nominal commands including the final
command interval (waypoint durations therefore total at most29.98s).
The trajectory describes requested commands, not actual shaft speed or position.

## Hardware operation, only after physical bench checks

Hardware execution requires explicit `--arm`, `--port` and a measured, validated
`--calibration` record. The existing example cannot arm. Before using those options,
a person must verify supply/cutoff, all joint directions/limits, printed fit and
manual poses, with motor power removable immediately.

The tool handshakes against the firmware/model/calibration identity and requires
fresh disarmed stationary IMU telemetry. Its reviewed initial command must agree
with the acknowledged start within PWM/telemetry quantization tolerance; otherwise
it refuses to arm. Runtime interpolation starts from that acknowledged command.
**Acknowledgements are not measured shaft positions.** The person must establish
the real initial pose; a matching command cannot prove it.

Commands target50Hz while telemetry is read continuously. Scheduling jitter never
causes catch-up bursts: commands stay at least20ms apart and may run more slowly.
Actual times are logged; the command session stops if it exceeds30s. The existing firmware
100ms watchdog remains active. Host stops on faults/disarm, stale/reordered IMU,
old/ahead acknowledgements,50ms telemetry timeout,40ms missed command deadline,
IMU clipping or excessive tilt. Before completing, the last command must be
acknowledged within80ms; this still does not prove shaft arrival.

The log directory contains command and raw IMU/ack CSVs, reviewed movement,
identities, status and any error. Completion, exceptions and Ctrl-C request STOP
and close the connection; no auto-reconnect/re-arm or automatic return-to-HOME.
**STOP/PWM silence does not isolate servo power.** Use the physical DC cutoff.

The acknowledgement grace may extend the final command by up to80ms.
This utility is a bench tool, not the30s walking-acceptance evaluator. Mocked tests
are labelled software evidence and do not clear physical gates.
