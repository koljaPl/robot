# Initial bench test — offline preparation first

This tool prepares the first one-servo/IMU test. It is **locally tested with mocked
transport, not physically verified**. Parts, exact order costs and measurements
remain unreported. No policy, automatic gait or six-joint motion is involved.

## Preview now, without hardware

```bash
.venv/bin/python bench.py --output runs/imu_preview_NEW
.venv/bin/python bench.py --channel 0 --pulse-us 1500 --seconds 2 --output runs/servo_preview_NEW
```

Both commands stay offline. The second previews a constant pulse refreshed at50Hz;
it does not move a servo. Output folders must be new. Channel order is left
hip/knee/ankle, right hip/knee/ankle; channels0–5. The old CSV output argument is
now a **session directory**, and a port requires explicit `--execute`.

## Later, with reviewed physical preparation

1. Check the actual PSU, lead, wiring polarity, common ground, insulation and
   accessible physical DC disconnect. Servo supply current bypasses the Pico.
   Follow [wiring](HARDWARE.md); no exposed mains work.
2. Use the current [Pico2 preparation firmware](../firmware/README.md), with matching
   configuration and calibration identities. Disconnect motor power for flashing;
   no flash was performed during software preparation. Invalid example calibration
   is permitted for this narrow bench test, never full-policy operation.
3. With motors disconnected, record stationary raw IMU first. Check sensor axes,
   supply and disarmed state. Keep original logs and video/photos.
4. Only after those checks, use **one unloaded servo with its horn removed**.
   Confirm connector pinout and keep DC disconnection reachable. A1400–1600µs
   bound does not establish its mechanical range or prevent an initial shaft jump.
   Do not attach the assembled robot or load for this first test.

Conditional commands below are procedures, not a claim of physical readiness:

```bash
# Explicit USB execution; read-only IMU, no motor commands:
.venv/bin/python bench.py --execute --port /dev/ttyACM0 --seconds 10 --output runs/imu_trial_NEW
# After the physical checks above; one constant pulse, not a sweep:
.venv/bin/python bench.py --execute --port /dev/ttyACM0 --channel 0 --pulse-us 1500 --seconds 2 --output runs/servo_trial_NEW
```

The program never calls policy ARM. It requires a matching handshake and two
fresh stationary IMU samples. Read-only duration is at most60s (default10s);
one-servo duration is at most5s (default2s). Durations must be20ms multiples.
Pulse values are integers1400–1600µs; no clipping or automatic sweep is performed.

Motor refreshes are at least20ms apart; no catch-up burst. Command lateness>40ms,
missing telemetry>50ms, non-increasing/gapped MCU time, sensor saturation, faults,
unmatched identity or unexpected armed/mode state stop the session. First bench
mode confirmation must arrive within80ms. Firmware's100ms watchdog remains active;
its **physical timing still needs testing**. No tilt interpretation is assumed
before IMU alignment calibration; this is not a standing/balancing controller.

Completion, Ctrl-C and failure request STOP and close USB. A failed STOP is
recorded; transport is still closed by SerialRobot. No automatic reconnect or
re-arm occurs. **Software STOP does not physically disconnect servo power.**

## Records and their limits

Each new folder contains:

- `preview.csv`: planned read-only session or constant-pulse refresh slots.
- `telemetry.csv` in execution: raw IMU, timestamps, flags and six-joint command
  acknowledgements. These angles/sequence **do not describe the bench pulse or
  measured shaft position**. Actual sample timing must be read from the log.
- `events.jsonl` in execution: requested pulses and firmware identity/status events.
  Bench status confirms the mode only; this protocol has no per-pulse sequence,
  pulse-width feedback or shaft feedback.
- `manifest.json`: configuration/calibration/source hashes, settings, counts,
  completion/failure and cleanup outcome. It never marks physical approval.

Keep video/ruler/protractor evidence separately. Do not feed command angles to
step-response fitting as shaft measurements. See [calibration](CALIBRATION.md)
and [measurement intake](MEASUREMENT_INTAKE.md). No calibration, price, physical
parameter or gate is updated automatically. Actual receipts, fit and bench results
are the next inputs; their absence does not invalidate this software preparation.
