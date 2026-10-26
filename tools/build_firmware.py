"""Pinned file-only Pico 2 build: no USB, flashing, arming or automatic downloads."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shlex
import shutil
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from calibration import configuration_identity, load_calibration
from tools.firmware_config import generate


class BuildError(RuntimeError):
    pass


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_source(output):
    """Compare every generated value, not only the printed identity strings."""
    calibration = load_calibration(ROOT/'calibrations/example.invalid.json', require_valid=False)
    if calibration['state'] == 'measured' or calibration['validated']:
        raise BuildError('This preparation build requires invalid example calibration')
    expected = output/'expected_generated_config.h'
    generate(ROOT/'calibrations/example.invalid.json', expected)
    if expected.read_bytes() != (ROOT/'firmware/generated_config.h').read_bytes():
        raise BuildError('Stale generated configuration: regenerate with tools/firmware_config.py')
    spec = json.loads((ROOT/'physical_spec.json').read_text())
    if spec['controller']['sdk_board'] != 'pico2':
        raise BuildError('Physical specification does not select Pico 2')
    return configuration_identity(calibration)


def inspect_artifacts(elf, uf2, identity):
    """Independent ELF/UF2 structural and identity checks, using files only."""
    data = elf.read_bytes()
    if data[:6] != b'\x7fELF\x01\x01' or struct.unpack_from('<H', data, 18)[0] != 40:
        raise BuildError('Expected ELF32 little-endian Arm executable')
    for key in ('configuration', 'calibration'):
        if identity[key].encode() not in data:
            raise BuildError('Compiled ELF lacks expected '+key+' identity')
    raw = uf2.read_bytes()
    if not raw or len(raw) % 512:
        raise BuildError('Invalid UF2 length')
    families, blocks, totals = set(), set(), set()
    absolute_blocks = 0
    for offset in range(0, len(raw), 512):
        magic0, magic1, flags, address, size, number, total, family = struct.unpack_from('<8I', raw, offset)
        if (magic0, magic1) != (0x0A324655, 0x9E5D5157) or struct.unpack_from('<I', raw, offset+508)[0] != 0x0AB16F30:
            raise BuildError('Invalid UF2 magic')
        if not flags & 0x2000 or not 0 < size <= 476:
            raise BuildError('Invalid UF2 family flag/payload/block numbering')
        families.add(family)
        if family == 0xE48BFF57:
            # Official picotool 2.3.1 RP2350-E10 ignored absolute block has its
            # own deliberately incomplete numbering (0/2), not Arm-image numbering.
            absolute_blocks += 1
            if (absolute_blocks > 1 or offset != 0 or flags != 0xA000 or number != 0
                    or total != 2 or size != 256 or address != 0x10FFFF00
                    or raw[offset+32:offset+288] != b'\xef'*256
                    or struct.unpack_from('<I', raw, offset+288)[0] != 0x9957E304):
                raise BuildError('Invalid RP2350-E10 absolute block')
        else:
            if number in blocks: raise BuildError('Duplicate Arm UF2 block')
            blocks.add(number); totals.add(total)
    # Picotool may include an absolute-family erratum block as well as Arm-S blocks.
    if 0xE48BFF59 not in families or not families <= {0xE48BFF59, 0xE48BFF57}:
        raise BuildError('UF2 is not RP2350 Arm secure-family firmware')
    if totals != {len(blocks)} or blocks != set(range(len(blocks))):
        raise BuildError('Incomplete UF2 block sequence')
    return {'elf_machine': 'ARM', 'elf_class': 32, 'uf2_families': [hex(x) for x in sorted(families)],
            'uf2_blocks': len(blocks), 'rp2350_e10_absolute_blocks': absolute_blocks}


def build(*, sdk, compiler, picotool, output, board='pico2'):
    """Create a new evidence folder or refuse without modifying an existing one."""
    output = Path(output).absolute()
    output.mkdir(parents=True, exist_ok=False)
    manifest = {'version': 1, 'started_utc': datetime.now(timezone.utc).isoformat(),
                'state': 'started', 'board': board, 'platform': 'rp2350-arm-s',
                'policy_arm_allowed': False, 'hardware_accessed': False,
                'physically_verified': False, 'commands': [], 'artifacts': {}}
    manifest_path = output/'manifest.json'
    env = {k: v for k, v in os.environ.items() if not k.startswith(('PICO_', 'PICOTOOL_', 'CMAKE_', 'CCACHE_', 'FETCHCONTENT_'))
           and k not in {'CC', 'CXX', 'ASM', 'CFLAGS', 'CXXFLAGS', 'LDFLAGS', 'CPATH',
                         'C_INCLUDE_PATH', 'CPLUS_INCLUDE_PATH', 'LIBRARY_PATH',
                         'GCC_EXEC_PREFIX', 'COMPILER_PATH', 'SOURCE_DATE_EPOCH'}}

    def save():
        manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')

    def run(args, *, cwd=ROOT, timeout=300):
        command = [str(a) for a in args]
        name = f'{len(manifest["commands"]):02d}.log'
        entry = {'argv': command, 'cwd': str(cwd), 'log': name}
        manifest['commands'].append(entry)
        save()
        try:
            result = subprocess.run(command, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=timeout, check=False)
            (output/name).write_text(result.stdout)
            entry['returncode'] = result.returncode
            save()
            if result.returncode:
                raise BuildError(f'Command failed ({result.returncode}); see {name}')
            return result.stdout.strip()
        except (OSError, subprocess.TimeoutExpired) as error:
            entry['error'] = str(error)
            captured = getattr(error, 'stdout', None) or ''
            if isinstance(captured, bytes): captured = captured.decode(errors='replace')
            (output/name).write_text(captured+'\n'+str(error)+'\n')
            raise BuildError(f'Command unavailable/timed out; see {name}') from error

    save()
    try:
        if board != 'pico2':
            raise BuildError('Only pico2 is permitted; never reuse a Pico 1 build')
        if (platform.system(), platform.machine()) != ('Linux', 'x86_64'):
            raise BuildError('Pinned tools require Linux x86_64')
        identity = verify_source(output)
        manifest['identity'] = identity
        manifest['source_sha256'] = {**identity['files'], **{
            p: sha256(ROOT/p) for p in ('firmware/generated_config.h', 'tools/firmware_config.py',
                                       'tools/build_firmware.py', 'firmware/build_dependencies.json')}}
        pins = json.loads((ROOT/'firmware/build_dependencies.json').read_text())
        manifest['dependency_pins'] = pins
        # Stabilize compiler date/time macros; actual execution time stays in the manifest.
        epoch = int(datetime.fromisoformat(pins['date']).replace(tzinfo=timezone.utc).timestamp())
        env['SOURCE_DATE_EPOCH'] = str(epoch)
        manifest['source_date_epoch'] = epoch
        sdk, compiler, picotool = Path(sdk).resolve(), Path(compiler).resolve(), Path(picotool).resolve()
        cmake, ninja = ROOT/'.venv/bin/cmake', ROOT/'.venv/bin/ninja'
        required = [sdk/'external/pico_sdk_import.cmake', compiler, picotool,
                    picotool.parent/'picotoolConfig.cmake', cmake, ninja]
        required += [compiler.with_name('arm-none-eabi-'+suffix) for suffix in ('g++', 'readelf', 'size')]
        for p in required:
            if not p.is_file(): raise BuildError('Missing dependency: '+str(p))
        if sha256(compiler) != pins['compiler']['gcc_sha256'] or sha256(picotool) != pins['picotool']['binary_sha256']:
            raise BuildError('Compiler/picotool executable checksum mismatch')
        revision = run(['git', '-C', sdk, 'rev-parse', 'HEAD'])
        tinyusb = run(['git', '-C', sdk/'lib/tinyusb', 'rev-parse', 'HEAD'])
        if revision != pins['sdk']['commit'] or tinyusb != pins['sdk']['tinyusb_commit']:
            raise BuildError('SDK/TinyUSB revision does not match dependency pins')
        for tree in (sdk, sdk/'lib/tinyusb'):
            if run(['git', '-C', tree, 'status', '--porcelain', '--untracked-files=no']):
                raise BuildError('SDK/TinyUSB has modified tracked files')
        versions = {'gcc': run([compiler, '--version']), 'target': run([compiler, '-dumpmachine']),
                    'picotool': run([picotool, 'version']), 'cmake': run([cmake, '--version']),
                    'ninja': run([ninja, '--version'])}
        if ('14.2.Rel1' not in versions['gcc'] or versions['target'] != 'arm-none-eabi'
                or not re.search(r'\bv2\.3\.1\b', versions['picotool'])
                or 'cmake version 3.31.10' not in versions['cmake'] or not versions['ninja'].startswith('1.13.2')):
            raise BuildError('Unexpected dependency version/target')
        manifest['tools'] = {'versions': versions, 'sdk_commit': revision, 'tinyusb_commit': tinyusb,
                             'executables': {str(p): sha256(p) for p in required if os.access(p, os.X_OK)}}
        source = output/'source'
        source.mkdir()
        for n in ('main.cpp', 'control.h', 'CMakeLists.txt', 'generated_config.h'):
            shutil.copy2(ROOT/'firmware'/n, source/n)
        env.update(PICO_SDK_PATH=str(sdk), PICO_TOOLCHAIN_PATH=str(compiler.parent),
                   PATH=os.pathsep.join((str(cmake.parent), str(compiler.parent), env.get('PATH', ''))))
        build_dir = output/'build'
        # SDK debug information also exists in Release ELFs. Normalize absolute
        # paths so distinct output directories do not change the delivered ELF.
        prefix_maps = ' '.join(shlex.quote('-ffile-prefix-map='+str(old)+'='+new) for old, new in (
            (ROOT, '/s6-project'), (sdk, '/pico-sdk'),
            (compiler.parent.parent, '/arm-toolchain'), (output, '/s6-build')))
        release_flags = '-g -O3 -DNDEBUG '+prefix_maps
        manifest['reproducibility_flags'] = release_flags
        run([cmake, '-S', source, '-B', build_dir, '-G', 'Ninja', '-DPICO_BOARD=pico2',
             '-DPICO_PLATFORM=rp2350-arm-s', '-DCMAKE_BUILD_TYPE=Release',
             '-DCMAKE_MAKE_PROGRAM='+str(ninja), '-Dpicotool_DIR='+str(picotool.parent),
             *['-DCMAKE_'+lang+'_FLAGS_RELEASE='+release_flags for lang in ('C', 'CXX', 'ASM')],
             '-DFETCHCONTENT_FULLY_DISCONNECTED=ON'])
        run([cmake, '--build', build_dir, '--parallel', '4'])
        elf, uf2 = output/'s6_bench.elf', output/'s6_bench.uf2'
        for target in (elf, uf2): shutil.copy2(build_dir/target.name, target)
        attributes = run([compiler.with_name('arm-none-eabi-readelf'), '-h', '-A', elf])
        cache = (build_dir/'CMakeCache.txt').read_text()
        if 'Tag_CPU_arch: v8-M.mainline' not in attributes or not re.search(
                r'^CMAKE_CXX_FLAGS:STRING=.*-mcpu=cortex-m33\b.*-mcmse\b', cache, re.M):
            raise BuildError('ELF/build flags do not identify Armv8-M Cortex-M33 secure target')
        run([compiler.with_name('arm-none-eabi-size'), elf])
        for artifact in (elf, uf2):
            info = run([picotool, 'info', '-a', artifact])
            if not all(re.search(pattern, info) for pattern in (
                    r'target chip:\s+RP2350', r'image type:\s+ARM Secure',
                    r'pico_board:\s+pico2\b', r'sdk version:\s+2\.3\.1\b')):
                raise BuildError('Artifact metadata does not match Pico2/RP2350 Arm secure/SDK2.3.1')
        manifest['inspection'] = inspect_artifacts(elf, uf2, identity)
        if verify_source(output) != identity:
            raise BuildError('Model/control identity changed during build')
        if any(sha256(ROOT/name) != expected for name, expected in manifest['source_sha256'].items()):
            raise BuildError('Build source or dependency ledger changed during build')
        manifest['artifacts'] = {p.name: {'sha256': sha256(p), 'bytes': p.stat().st_size} for p in (elf, uf2)}
        manifest['state'] = 'locally_cross_built'
        manifest['limits'] = ['Invalid example calibration; full-policy arming disabled.',
                              'Boot disarmed; explicit narrow single-servo bench mode still exists.',
                              'No USB/device access, flashing, electrical test, fit or physical approval.',
                              'Software stop is not physical DC isolation.']
    except (Exception, KeyboardInterrupt) as error:
        manifest['state'] = 'interrupted' if isinstance(error, KeyboardInterrupt) else 'failed'
        manifest['error'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        manifest['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save()
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sdk', required=True, type=Path)
    p.add_argument('--compiler', required=True, type=Path, help='Path to arm-none-eabi-gcc')
    p.add_argument('--picotool', required=True, type=Path, help='Official installed executable beside its CMake config')
    p.add_argument('--output', required=True, type=Path, help='New output directory; existing folders refused')
    p.add_argument('--board', default='pico2')
    args = p.parse_args()
    try:
        result = build(**vars(args))
    except (Exception, KeyboardInterrupt) as error:
        print(f'Build not completed: {error}', file=sys.stderr)
        return 1
    print(json.dumps({'state': result['state'], 'identity': result['identity']['configuration'],
                      'policy_arm_allowed': False, 'output': str(args.output)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
