# Native-PWM S6 hardware and protocol

Updated 2026-10-24. Implemented source and local compilation are distinct from
physical verification: **nothing has been purchased or electrically tested**.
The selected *provisional quotation revision* is bare Pico native PWM, six Waveshare15024
MG90S, MPU6050 and Mean Well GST40A05-P1J. PCA9685 is not in the current basket.
Its listing is unavailable and removing it resolves the original board/brace overlap.

## Power and self-soldered harness

PC USB powers Pico and IMU. Enclosed 5V/5A PSU, including separately priced
Schuko–C13 mains lead, powers ONLY the servo bus. Never connect servo5V to Pico
VBUS/VSYS/3V3, or route servo current through GPIO jumpers or a breadboard.
Join logic ground to the short heavy servo-return bus once. Mains wiring remains
inside the commercial PSU/lead. Capacitor1000µF/16V goes across the bus with
correct polarity; it is not a substitute for an adequate supply.

The proposed basket uses a **bare Pico** with user-soldered headers. Existing RP2040
firmware/pins remain unchanged. The model now separately owns estimated3g bare PCB
and two0.6g header rows (4.2g together). Header overall pin length11mm is sourced;
PCB/USB envelope and all masses/placements still need measurement.
Compare Pico H5.50 +one40pin pack0.60 with bare4.10 +header kit0.50 +40pin pack0.60:
header-inclusive saving0.90. Kit2x20pins +40pin pack supply80functional pins,
54used,26spare; supplied3pin SWD strip is extra spare. Solder10g flux-core, heat-shrink, ties and wire are priced robot
consumables. Iron access is available; other tools must be confirmed/borrowed or
priced outside the robot cap but inside initial cash. No mandatory paid helper.

**Prepare unpowered, with the PSU disconnected from mains and DC, and USB removed:**

1. Solder two20pin rows to the bare Pico and the needed IMU header; inspect bridges.
   Keep IMU I2C/ground leads short. Sensor pull-ups and VCC must be3.3V.
2. For each of six10cm JR extensions, identify the factory connector that mates to
   the actual servo cable; preserve it for replaceability. Do not trust connector
   gender names or wire colours: verify end-to-end continuity and pin order first.
3. Remove the unused extension end and expose only short conductor lengths. Solder
   each positive/return branch separately onto short0.75mm² positive/negative buses.
   Keep each bus section to about10cm; stagger splices, insulate individually, then
   add overall strain relief. Mark the negative red-wire bus with black shrink at
   every exposed end. Connector/wire ratings remain a required acceptance test.
4. Bring each isolated signal to a separate insulated header/jumper and its Pico GPIO.
   No positive servo wire connects to the Pico. Join servo-bus return to Pico GND
   with one logic-reference lead; high-current return goes straight to the PSU.
   Use separate GND pins for IMU and servo reference (e.g.physical38and3).
5. Solder DC socket positive/return and the1000µF capacitor across the bus; verify
   socket polarity with a meter and the capacitor's negative stripe. Insulate all
   socket lugs and metal that could short, secure it off-robot, and strain-relieve
   the tether. No bare solder joint may reach frame/PCB/another conductor.
6. With no servo connected, check shorts/continuity, then energize the commercial
   enclosed PSU and measure centre-positive5V at each branch. Disconnect it before
   connecting one unloaded servo. Verify current/droop, connector heating and3.3V
   PWM compatibility before expanding to six. Never work on the mains internals.

Use ventilation, a stable iron stand and eye protection while clipping leads;
keep hot tools away from insulation/boards. Do not solder powered electronics.
No breadboard or thin Dupont wire carries servo supply current. Self-soldering is
not evidence of an electrically qualified harness; bench data is still required.

Estimated average six-servo current0.6–1.5A, assumed peak4.8A (6×0.8A), plus
logic below0.15A on USB. **Selected-servo current is unknown**; these are sizing
hypotheses. A5A PSU offers little peak margin; measure droop/current before six
servos. At4.8A, 20cm total0.75mm² copper loop drops~0.022V, excluding connectors,
PSU lead and branches. A2m one-way tether of this wire drops~0.45V and is not
acceptable. Use the PSU's existing lead and slack loop for the initial0.3m trial;
several metres need a newly sourced thicker tether/longer USB cable and budget.
1000µF stores only~0.04ms at4.8A for0.2V droop. Measure4.8–6V at the farthest
loaded servo and check connector temperature.

Accessible full-current DC unplug is the physical emergency cutoff. Selected
provisional input: [Goobay11638,EUR1.10](https://www.berrybase.de/dc-einbaubuchse-fuer-hohlstecker-5-5x2-1mm-metallausfuehrung-loetanschluss),
5.5×2.1mm solder socket with nut/washer; retailer specifies5A/30V DC. Replaces the
unpriced Delock pigtail. User solders short0.75mm² bus leads, separately insulates
lugs and outer metal, and secures strain relief with listed shrink/ties. Support this
connection off robot. Verify centre-positive continuity and insulation before power.
No exposed low-voltage metal may short to boards/fasteners. No mains modification.
JR branch gauge/contacts and actual servo current still require confirmation.
Socket rating is not a complete harness or bench approval. Unrated Goobay76743
is not accepted as5A. STOP/PWM silence **does not disconnect motor power**;
a servo may hold its last position. Always disarm before reconnecting DC.

USB-A–Micro-B data cable connects Pico directly to a USB-A PC; **no extra adapter**
in base basket. Only a PC without USB-A needs a separately sourced data adapter.
Available50cm Dupont pack replaces unavailable20cm; user keeps I2C wiring short
and secures excess. No servo supply current in any Dupont jumper.

## Pin table

| Joint / function | GPIO | Pico physical pin |
|---|---:|---:|
| Left hip |0|1|
| Left knee |1|2|
| Left ankle |2|4|
| Right hip |3|5|
| Right knee |6|9|
| Right ankle |7|10|
| MPU SDA / SCL |4 / 5|6 / 7|
| IMU VCC |3V3 OUT|36|
| IMU GND |GND|38|
| Short common servo ground reference |GND|3|

Native PWM uses a1MHz counter and wrap19999:50Hz and1µs resolution. Paired
channels share slices with the same frequency. GPIOs produce3.3V logic;
**MG90S input compatibility is unverified**. Test one unloaded servo before
approving this revision; a level shifter would add cost and wiring. No onboard
PWM feedback or torque protection exists.

MPU6050 at0x68, AD0 grounded: WHO_AM_I checked, ±2g, ±250°/s, DLPF_CFG3
(~44Hz accel/~42Hz gyro), divider4 for200Hz. Wire pull-ups must go to3.3V.
Firmware sends raw scaled sensor-frame readings. PC removes measured biases,
rotates into body coordinates and uses `GravityEstimator`. The simulated
44Hz first-order filter is a provisional surrogate, not exact silicon transfer.
References: [Pico](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html),
[pinout](https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf),
[IMU register map](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf).

## Executable version1 protocol

`hardware_interface.py`, `serial_robot.py`, `firmware/control.h` and
`firmware/main.cpp` implement the following contract, superseding the earlier
pseudocode-only draft. No physical firmware already exists to migrate.
USB CDC baud460800 (descriptor), ASCII, max192bytes including newline,
`payload*HHHH\n`, CRC16/CCITT initFFFF. Config/calibration SHA256s are lowercase
64hex. All numeric fields decimal integers; seq uint16, timestamps uint32 ms.
Angles mrad, acceleration mm/s², angular rates mrad/s.

| Payload | Behavior |
|---|---|
| `S,1` | Disarm, disable PWM, clear fault/queue and require new handshake |
| `H,1,config_hash,cal_hash,pc_ms` | Disarmed identity/time-origin handshake; mismatch faults |
| `I,1,config_hash,cal_hash,status` | Acknowledgement; no implicit arm |
| `A,1` | Explicit policy arm, only matching identity + valid measured calibration + healthy IMU |
| `C,1,seq,pc_ms,q0,q1,q2,q3,q4,q5` | Six bounded fresh target commands while armed |
| `B,1,seq,pc_ms,channel,pulse_us` | Explicit one-channel bench mode;1400–1600µs only; no policy arming |
| `T,1,ack_seq,mcu_ms,status,q0,q1,q2,q3,q4,q5,ax,ay,az,gx,gy,gz` |200Hz telemetry with applied command coordinates |

Bits:1 armed,2 latched fault (including watchdog/invalid data),4 unhealthyIMU,
8 invalid/unmeasured calibration,16 no matching handshake,32 bench mode.
Only fresh valid C/B renews100ms watchdog. CRC/length/type/range/replay faults
silence all outputs and latch fault. S then H is needed before deliberate restart.
Sequence deltas must be1..32767; PCtimestamp deltas positive and<=1000ms.
H establishes relative clock origin; inferred command age must be−20..80ms.
Host refuses policy arming for handshake round-trip>=20ms (provisional bound).
Unsigned wrap-safe comparisons are used; neither absolute clock is synchronized.

Firmware queues commands for a minimum20ms before50Hz target application,
limits target slew to calibrated maximum<=180°/s, uses an estimated0.5° command
deadband, rounds inward to1µs safe pulse bounds and acknowledges the sequence
when dequeued. Multiple commands within the same tick can be coalesced by
latest due target. This is commanded motion, not measured shaft motion; PWM
speed limits do not guarantee actual shaft speed or physical torque protection.
The queue is fixed8entries. No dynamic input allocation is used.

Calibration is versioned JSON persisted **in firmware flash at build time**.
Changing it requires rebuilding/flashing; it cannot be edited over an armed
serial link. `tools/firmware_config.py` generates the matching header. Examples
remain invalid and cannot policy-arm. Model/control/firmware source hashes
combine into one config hash; the calibration has its own hash. Policies carry
both plus their file hash. `deploy.py` rejects incompatible policies/calibration.
No historical prototype checkpoint is approved for the new model.

## Bench and deployment

See [firmware build](../firmware/README.md) and [calibration](CALIBRATION.md).
Read-only IMU logging is the bench default. Nothing in these instructions means
an actual motor should be powered before procurement/fit/power gates pass.

```bash
python bench.py --port /dev/ttyACM0 --seconds 10 --output runs/stationary.csv
# Explicit single-channel pulse calibration, unloaded servo, horn detached initially:
python bench.py --port /dev/ttyACM0 --channel 0 --pulse-us 1500 --seconds 2 --output runs/channel0.csv
# Only after all physical checks and training with this measured calibration:
python deploy.py --port /dev/ttyACM0 --model runs/measured/best_model.zip \
  --calibration calibrations/measured-v1.json --arm --seconds 5 --output runs/trial01.csv
```

Ctrl-C/fault closes with STOP. Physical operator keeps the DC disconnect
reachable. Never reset a fallen robot automatically: power off, inspect, lift,
replace damaged parts and reinitialize. Real distances/steps require video/ruler,
not double integration of MPU acceleration.
