# Pico 2 preparation build — local evidence, 2026-10-26

**Locally cross-built; no hardware operation or physical approval.**

- SDK2.3.1 commit079c6f39023649b154152db30f1d781e884879bc; pinned
  TinyUSB86ad6e56c1700e85f1c5678607a762cfe3aa2f47.
- Arm GNU14.2.Rel1 and official picotool2.3.1; archive checksums verified before
  extraction. [Pins](../../../../firmware/build_dependencies.json),
  [download verification](download_verification.json), [Arm checksum](arm_published_checksum.txt).
- Two final builds in different folders produce byte-identical ELF and UF2.
  [First manifest](repeat_08/manifest.json), [second manifest](verified/manifest.json),
  [aggregate record](summary.json). Fixed SOURCE_DATE_EPOCH1792972800 and normalized
  paths retain SDK-equivalent Release/debug options. This was checked on this host;
  it is not a claim of bit equality across every OS or compiler version.
- Current model/control identity685e3802unchanged; all fingerprinted source bytes
  match the previous frozen reference. Invalid example calibration retained;
  full-policy ARM rejected by native tests. No source retuning or PPO.
- ELF:32-bit little-endian Arm, Armv8-M/Cortex-M33 secure compiler flags;
  ELF/UF2 metadata identifies Pico2, RP2350 ARM Secure, SDK2.3.1.
- Independent UF2 parsing checks155Arm-S blocks plus the separate official ignored
  RP2350-E10 absolute block. Picotool inspection uses explicit filenames only.
- Active suite: **121passed**; [final post-flag log](pytest_release.txt).
  Prior120/121logs belong to their recorded checkpoints, not physical tests.

## Current preparation artifacts

- [ELF with debug information](verified/s6_bench.elf), SHA256
  `68f96c82f360f6f4cf397b608bc862aacae2b63b375d5c821fa8411736c5dc3a`.
- [UF2 preparation image](verified/s6_bench.uf2), SHA256
  `2f404167d64db67125f5e5a0d2a5b65b33c8691314001095d3fb860657d730d6`.
- Source copies, configuration and individual command logs are in `verified/`.
  [Repeatable build instructions](../../../../firmware/README.md).

These are preparation artifacts, not authorization to flash or connect motor power.
Boot is disarmed. `CAL_VALID=false` disables full-policy arm; explicit narrow
single-servo bench mode still requires later reviewed physical precautions.

## Failures retained

`failed_inspection/`: compilation succeeded but an overly specific readelf test
expected a Cortex-M33 name; ELF reports Armv8-M attributes. Corrected by checking
attributes, compiler flags and file metadata together, without firmware changes.

`pre_path_normalization_03/` and `_04/`: identical UF2, different debug-path ELF
bytes. This failed comparison led to fixed path mapping. `pre_epoch/` is the earlier
successful build before deterministic date macros. Other exploratory builds remain
under `runs/`; no old binary or source registry was relabelled.

No USB enumeration, flashing, arming, electrical timing, servo motion, print fit or
physical walking was performed. All five release gates remain false. Next: receive
parts, verify two printed fit samples, physical power isolation and one unloaded
servo/IMU; supply actual receipts and measured records for review. Budget/prices
and measured-policy calibration remain unresolved separately.
