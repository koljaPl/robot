# Pico 2 firmware — build target and bench preparation

Updated2026-10-26: selected controller is **Raspberry Pi Pico 2, bare RP2350**,
not RP2040/Pico1 or Pico2W. Native PWM/I2C GPIOs and50Hz/200Hz timing are unchanged.
Official same51×21mm footprint and MicroUSB documented in the
[Pico2 datasheet](https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf).
Headers are user-soldered;3g board plus1.2g headers is an estimate, not weighed.

CMake defaults to`pico2` and rejects`pico`; build selection is fingerprinted.
Current identity starts`685e3802`; generated header is current with`CAL_VALID=false`.
All prior policies/UF2are historical. Native control tests pass; **no current ARM
cross-build or electrical verification**: SDK/cross compiler are absent locally.
Prior RP2040 compilation records do not validate Pico2 binaries. The planned SDK
is2.3.1; install it and a Cortex-M33-capable Arm toolchain before this build.
Official [SDK examples](https://github.com/raspberrypi/pico-examples) describe the
pico2 board/platform selection; [picotool](https://github.com/raspberrypi/picotool)
documents ELF-to-UF2 conversion/family detection.

Install an `arm-none-eabi` cross compiler and clone the SDK outside the project:

```bash
git clone --depth 1 --branch 2.3.1 https://github.com/raspberrypi/pico-sdk.git /tmp/pico-sdk
git -C /tmp/pico-sdk submodule update --init --depth 1 lib/tinyusb
source .venv/bin/activate
python tools/firmware_config.py # invalid example, cannot policy-arm
export PICO_SDK_PATH=/tmp/pico-sdk
# Set PICO_TOOLCHAIN_PATH to the directory containing arm-none-eabi-gcc if not in PATH.
cmake -S firmware -B build/firmware_pico2 -G Ninja -DPICO_BOARD=pico2 -DPICO_NO_PICOTOOL=1
cmake --build build/firmware_pico2 -j 4
# Official picotool2.3.1 converts the ELF into a flashable UF2:
picotool uf2 convert build/firmware_pico2/s6_bench.elf build/firmware_pico2/s6_bench.uf2 --family rp2350-arm-s
```

`PICO_NO_PICOTOOL=1` avoids CMake implicitly downloading extra code; install
[picotool](https://github.com/raspberrypi/picotool) separately or use the official
[SDK tools2.3.1-0 release](https://github.com/raspberrypi/pico-sdk-tools/releases/tag/v2.3.1-0).
If picotool is configured normally, omit that flag and SDK can produce UF2 itself.

For a measured calibration, run:

```bash
python tools/firmware_config.py --calibration calibrations/measured-v1.json
cmake --build build/firmware_pico2 -j 4
picotool uf2 convert build/firmware_pico2/s6_bench.elf build/firmware_pico2/s6_bench.uf2 --family rp2350-arm-s
```

Calibration/signs/limits/identity are compiled into firmware flash and survive
power loss; every boot is disarmed. Do not hand-edit generated_config.h. Physical
flashing: disconnect servo power, hold BOOTSEL while connecting Pico USB, then
copy the new Pico2 UF2 onto its BOOTSEL drive (verify the actual mounted device). Release/reset and check read-only telemetry first.
Never flash or reconnect motor power while a policy process is running.

The generated header must be regenerated after any fingerprinted control/model
source edit. A stale image is rejected by the PC handshake. The repository
example's `CAL_VALID=false` is intentional, not a build error. Single-channel
bench mode is explicitly allowed without validated joint calibration and is
restricted to1400–1600µs; it still needs a clear, unloaded setup and cutoff.
