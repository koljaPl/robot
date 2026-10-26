# Initial bench preparation — 2026-10-26

**Locally verified offline/mocked software only.** No device accessed, motor moved,
firmware flashed, measured calibration created or gate cleared. No PPO training.

The prior bench recorder ignored firmware fault flags and opened USB without a
separate execution flag. Its source is preserved in
[history](../../../history/2026-10-26/pre_bench_preparation/bench.py).

- Default execution is now an offline preview. USB requires `--execute` and a port;
  a port alone is rejected. A new directory holds session records; old CSV-path
  instructions were updated. [Current guide](../../../BENCH.md).
- Read-only IMU or one constant1400–1600µs pulse only; no sweep or policy ARM.
  Requires matching identity and fresh stationary startup. Stops on flags, stale
  data, saturation, command deadlines, unexpected mode/disarm and missing initial
  mode confirmation; no refresh catch-up bursts.
- STOP/close is requested on completion, interruption and failure; failed cleanup
  stays visible. No automatic reconnect. Physical DC isolation remains separate.
- Bench status confirms mode only. Six-joint command acknowledgements do not report
  applied bench pulses, per-pulse sequence or actual shaft angles.
- **41focused tests passed**, covering validation before USB/output, bounded preview,
  read-only mode, timing jitter, timestamp rollover, faults, stale data, mismatch,
  timeout, saturation, interruption, unexpected mode and failed STOP cleanup.
- **162tests passed in16.54s**, [full log](pytest.txt). Runtime hardware branches use
  fake transport only. [Summary and source hashes](summary.json), source in `source/`.
- Actual CLI [read-only preview](read_only_preview/manifest.json) and
  [single-servo preview](single_servo_preview/manifest.json) both completed without
  opening USB; neither is physical evidence.

The685e3802model/control identity, current prepared ELF/UF2, frozen script and all
physical assumptions are unchanged. No repeat firmware build, retuning or training
was needed. Order/arrival/cost details remain unreported, not silently free/received.
Next: receive parts, fit samples and perform reviewed unpowered/electrical/one-servo
checks; retain original video and measurements for review.
