# Pico 2 firmware — reproducible preparation build

Updated **2026-10-26**. Selected board: **bare Raspberry Pi Pico 2, RP2350**, not
Pico 1 or Pico 2 W. Native PWM/I2C pins and50Hz commands/200Hz IMU are unchanged.
See the official [Pico2 datasheet](https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf).
Board/header masses and physical fit remain estimated. Ordering started according
to the user; items, paid prices, arrivals and physical measurements remain unknown.

The current preparation firmware is **locally cross-built**, not physically tested.
Full-policy arming is disabled by `CAL_VALID=false`; every boot starts disarmed.
Explicit narrow single-servo bench mode remains available only for a later reviewed
unloaded physical test. STOP is not physical motor-power isolation.

## Pinned dependencies

[build_dependencies.json](build_dependencies.json) records official URLs, verified
archive checksums, extracted executable hashes, SDK commit and pinned TinyUSB commit.

| Dependency | Version / source |
|---|---|
| Pico SDK | [2.3.1](https://github.com/raspberrypi/pico-sdk/tree/2.3.1), commit079c6f39; TinyUSB86ad6e56 |
| Arm GNU bare-metal compiler | [14.2.Rel1 Linux x86-64](https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-x86_64-arm-none-eabi.tar.xz) |
| picotool | [2.3.1 official Linux x86-64 release](https://github.com/raspberrypi/pico-sdk-tools/releases/tag/v2.3.1-0) |
| CMake / Ninja | Existing `.venv` executables; pinned in requirements-dev.txt |

Install tools outside the project/archive, for example `/tmp/s6-pico2-tools`.
This location is temporary: recreate it if the OS clears `/tmp`. The builder
does not download dependencies or install system packages.

```bash
mkdir -p /tmp/s6-pico2-tools
git clone --depth 1 --branch 2.3.1 https://github.com/raspberrypi/pico-sdk.git /tmp/s6-pico2-tools/pico-sdk-2.3.1
git -C /tmp/s6-pico2-tools/pico-sdk-2.3.1 submodule update --init --depth 1 lib/tinyusb
```

Download the compiler and picotool archives from the ledger URLs. Verify their
SHA256 against that ledger **before extraction**. Extract the compiler tree and
picotool package there; retain picotool's neighbouring CMake configuration files.
No OpenOCD, debugger or USB interaction is required for this software build.

## Build and inspect without hardware

From the project root, with the existing Python environment installed:

```bash
.venv/bin/python tools/build_firmware.py \
  --sdk /tmp/s6-pico2-tools/pico-sdk-2.3.1 \
  --compiler /tmp/s6-pico2-tools/arm-gnu-toolchain-14.2.rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-gcc \
  --picotool /tmp/s6-pico2-tools/picotool/picotool \
  --output runs/pico2_build_NEW
```

The new output directory must not exist. Each run keeps logs, source snapshot,
ELF/UF2 and `manifest.json`, including failed/interrupted builds. It checks the
whole generated header against the invalid example calibration, SDK/TinyUSB
commits, executable hashes, tool versions, Pico2/Arm secure flags, embedded hashes
and file-only ELF/UF2 metadata. It refuses stale headers or a wrong board.

Builds use Release mode, explicit installed picotool and disconnected CMake fetches.
`SOURCE_DATE_EPOCH` is fixed to the dependency ledger's date at UTC midnight;
actual execution dates are recorded separately. Inherited compiler overrides are
removed. No host transport, flash, arm, erase or reboot command is invoked by the
utility. SDK picotool operations post-process local files only.

Inspection uses `picotool info -a FILE.elf` and `picotool info -a FILE.uf2`.
**Do not substitute `picotool uf2 info`: that subcommand is device-oriented.**
Independent parsing checks the RP2350 Arm-S image and its official RP2350-E10
ignored absolute block separately; their block numbering is intentionally different.

Current identity begins`685e3802`; firmware/model/control sources were not changed
by the builder. Historical policies and older UF2 images remain untouched.
[Build evidence](../docs/validation/2026-10-26/pico2_crossbuild/README.md) records
actual results; compilation never proves servo timing, electrical safety or walking.

## Next physical stage

No flashing was performed. After parts arrive, follow [PLAN.md](../PLAN.md) and
[initial bench](../docs/BENCH.md) and [calibration instructions](../docs/CALIBRATION.md): verify power/polarity and
physical DC isolation first, then current firmware identity, read-only IMU and one
unloaded servo. Verify disarmed startup and100ms watchdog before attached limbs.
[Manual six-joint control](../docs/MANUAL_CONTROL.md) defaults to offline preview.

The preparation builder deliberately refuses measured/validated policy calibration.
Real pulse mapping, directions, response and IMU measurements must be reviewed and
versioned before a separate measured-calibration image and policy deployment are
approved. Do not replace invalid calibration with invented measurements or flash
historical images to bypass a mismatch. Changed fingerprinted sources require
regeneration/rebuilding and invalidate incompatible policies.
