# Pico firmware — local build and bench preparation

**Frame/control identity update2026-10-24:** proposed bare Pico uses the same RP2040 firmware
and GPIOs as Pico H. User fits headers and a self-soldered insulated harness; no
mandatory helper labour. See [wiring sequence](../docs/HARDWARE.md). Do not flash/arm
this as proof of electrical or mechanical verification. Current provisional twin uses bare Pico+two soldered header rows. Module mass
is estimated4.2g; actual board/harness measurements remain pending. The generated
invalid header now carries the r2 fingerprint. OldUF2 images are historical: rebuild
with this header and later measured calibration before any flash. No current ARM
build or physical electrical result is claimed by the geometry update.

The subsequent simulated shaft-offset correction changes the full configuration
identity to`b11ab929…`; `generated_config.h` carries that hash with`CAL_VALID=false`.
All saved policies and prior UF2files are incompatible, including r2 smoke artifacts.
Native control tests passed with this header; no new ARM/Pico build is claimed.
See [current evidence](../docs/SENSITIVITY.md). Rebuild with measured calibration
before any physical policy operation; never relabel historical binaries.


Source is C++17 using official Pico SDK **2.3.1**, revision
`079c6f39023649b154152db30f1d781e884879bc`, TinyUSB submodule
`86ad6e56c1700e85f1c5678607a762cfe3aa2f47`.
Locally compiled with Arm GNU14.2.Rel1, CMake3.31.10 and Ninja1.13.2.
No electrical/timing/flash test on a Pico is claimed.

Install an `arm-none-eabi` cross compiler and clone the SDK outside the project:

```bash
git clone --depth 1 --branch 2.3.1 https://github.com/raspberrypi/pico-sdk.git /tmp/pico-sdk
git -C /tmp/pico-sdk submodule update --init --depth 1 lib/tinyusb
source .venv/bin/activate
python tools/firmware_config.py # invalid example, cannot policy-arm
export PICO_SDK_PATH=/tmp/pico-sdk
# Set PICO_TOOLCHAIN_PATH to the directory containing arm-none-eabi-gcc if not in PATH.
cmake -S firmware -B build/firmware -G Ninja -DPICO_BOARD=pico -DPICO_NO_PICOTOOL=1
cmake --build build/firmware -j 4
# Official picotool2.3.1 converts the ELF into a flashable UF2:
picotool uf2 convert build/firmware/s6_bench.elf build/firmware/s6_bench.uf2 --family rp2040
```

`PICO_NO_PICOTOOL=1` avoids CMake implicitly downloading extra code; install
[picotool](https://github.com/raspberrypi/picotool) separately or use the official
[SDK tools2.3.1-0 release](https://github.com/raspberrypi/pico-sdk-tools/releases/tag/v2.3.1-0).
If picotool is configured normally, omit that flag and SDK can produce UF2 itself.

For a measured calibration, run:

```bash
python tools/firmware_config.py --calibration calibrations/measured-v1.json
cmake --build build/firmware -j 4
picotool uf2 convert build/firmware/s6_bench.elf build/firmware/s6_bench.uf2 --family rp2040
```

Calibration/signs/limits/identity are compiled into firmware flash and survive
power loss; every boot is disarmed. Do not hand-edit generated_config.h. Physical
flashing: disconnect servo power, hold BOOTSEL while connecting Pico USB, then
copy the UF2 onto RPI-RP2. Release/reset and check read-only telemetry first.
Never flash or reconnect motor power while a policy process is running.

The generated header must be regenerated after any fingerprinted control/model
source edit. A stale image is rejected by the PC handshake. The repository
example's `CAL_VALID=false` is intentional, not a build error. Single-channel
bench mode is explicitly allowed without validated joint calibration and is
restricted to1400–1600µs; it still needs a clear, unloaded setup and cutoff.
