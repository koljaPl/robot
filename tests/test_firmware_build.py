"""File-only build safety/failure tests; synthetic artifacts are not firmware evidence."""
import json
from pathlib import Path
import shutil
import struct
import subprocess

import pytest

from tools import build_firmware as builder


def uf2_block(family=0xE48BFF59, number=0, total=1, absolute=False):
    data = bytearray(512)
    struct.pack_into('<8I', data, 0, 0x0A324655, 0x9E5D5157,
                     0xA000 if absolute else 0x2000,
                     0x10FFFF00 if absolute else 0x10000000+number*256,
                     256, number, 2 if absolute else total, family)
    if absolute:
        data[32:288] = b'\xef'*256
        struct.pack_into('<I', data, 288, 0x9957E304)
    struct.pack_into('<I', data, 508, 0x0AB16F30)
    return data


def artifact_files(folder, identity):
    folder.mkdir(exist_ok=True, parents=True)
    elf = folder/'s6_bench.elf'; uf2 = folder/'s6_bench.uf2'
    data = bytearray(64); data[:6] = b'\x7fELF\x01\x01'
    struct.pack_into('<H', data, 18, 40)
    elf.write_bytes(data+identity['configuration'].encode()+identity['calibration'].encode())
    uf2.write_bytes(uf2_block(0xE48BFF57, absolute=True)+uf2_block())
    return elf, uf2


@pytest.fixture
def environment(tmp_path, monkeypatch):
    real_root = builder.ROOT; root = tmp_path/'repo'; root.mkdir()
    for name in ('firmware/main.cpp','firmware/control.h','firmware/CMakeLists.txt',
                 'firmware/generated_config.h','firmware/build_dependencies.json',
                 'tools/firmware_config.py','tools/build_firmware.py'):
        dest = root/name; dest.parent.mkdir(exist_ok=True,parents=True)
        shutil.copy2(real_root/name,dest)
    sdk = tmp_path/'sdk'; (sdk/'external').mkdir(parents=True)
    (sdk/'external/pico_sdk_import.cmake').write_text('synthetic test file')
    compiler = tmp_path/'gcc/bin/arm-none-eabi-gcc'
    picotool = tmp_path/'picotool/picotool'
    files=[compiler,picotool,picotool.parent/'picotoolConfig.cmake',root/'.venv/bin/cmake',root/'.venv/bin/ninja']
    files += [compiler.with_name('arm-none-eabi-'+x) for x in ('g++','readelf','size')]
    for f in files:
        f.parent.mkdir(exist_ok=True,parents=True); f.write_text('synthetic tool'); f.chmod(0o755)
    pins=json.loads((root/'firmware/build_dependencies.json').read_text())
    pins['compiler']['gcc_sha256']=builder.sha256(compiler)
    pins['picotool']['binary_sha256']=builder.sha256(picotool)
    (root/'firmware/build_dependencies.json').write_text(json.dumps(pins))
    identity={'configuration':'a'*64,'calibration':'b'*64,'files':{}}
    monkeypatch.setattr(builder,'ROOT',root)
    monkeypatch.setattr(builder,'verify_source',lambda output:identity)
    monkeypatch.setattr(builder.platform,'system',lambda:'Linux')
    monkeypatch.setattr(builder.platform,'machine',lambda:'x86_64')
    calls=[]

    def fake_run(argv, **kwargs):
        calls.append(argv)
        exe=Path(argv[0]).name; text=''
        if exe=='git':
            if 'rev-parse' in argv:
                text=pins['sdk']['tinyusb_commit'] if str(argv[2]).endswith('tinyusb') else pins['sdk']['commit']
        elif exe=='arm-none-eabi-gcc':
            text='arm-none-eabi' if '-dumpmachine' in argv else 'Arm GNU Toolchain 14.2.Rel1'
        elif exe=='picotool':
            if argv[1]=='version':text='picotool v2.3.1'
            else:
                assert argv[1:3]==['info','-a'] and Path(argv[3]).is_file()
                text='target chip: RP2350\nimage type: ARM Secure\npico_board: pico2\nsdk version: 2.3.1'
        elif exe=='cmake':
            if '--version' in argv:text='cmake version 3.31.10'
            elif '--build' in argv:
                b=Path(argv[2]); artifact_files(b,identity)
                (b/'CMakeCache.txt').write_text('CMAKE_CXX_FLAGS:STRING=-mcpu=cortex-m33 -mthumb -mcmse\n')
            else:assert '-DPICO_BOARD=pico2' in argv and '-DFETCHCONTENT_FULLY_DISCONNECTED=ON' in argv
        elif exe=='ninja':text='1.13.2'
        elif exe=='arm-none-eabi-readelf':text='Tag_CPU_arch: v8-M.mainline'
        return subprocess.CompletedProcess(argv,0,text)

    monkeypatch.setattr(builder.subprocess,'run',fake_run)
    return {'sdk':sdk,'compiler':compiler,'picotool':picotool,'output':tmp_path/'evidence'}, calls, fake_run, identity


def test_mocked_build_is_file_only_and_records_evidence(environment):
    args,calls,_,identity=environment
    m=builder.build(**args)
    assert m['state']=='locally_cross_built' and m['identity']==identity
    assert not m['policy_arm_allowed'] and not m['hardware_accessed'] and not m['physically_verified']
    assert m['inspection']['rp2350_e10_absolute_blocks']==1
    assert set(m['artifacts'])=={'s6_bench.elf','s6_bench.uf2'}
    assert all(Path(args['output']/e['log']).is_file() for e in m['commands'])
    assert all(cmd[1]=='version' or cmd[1:3]==['info','-a'] for cmd in calls if Path(cmd[0]).name=='picotool')


@pytest.mark.parametrize('failure',['missing','wrong_board','tool_checksum','sdk_revision','dirty_sdk',
                                     'version','subprocess','timeout','interrupt','wrong_cpu','wrong_metadata','source_drift'])
def test_failed_builds_preserve_logs_and_never_claim_success(environment,monkeypatch,failure):
    args,calls,real,identity=environment
    if failure=='missing':args['compiler'].unlink()
    if failure=='wrong_board':args['board']='pico'
    if failure=='tool_checksum':args['compiler'].write_text('different executable')

    def fail_run(argv,**kwargs):
        if failure=='sdk_revision' and 'rev-parse' in argv:return subprocess.CompletedProcess(argv,0,'wrong')
        if failure=='dirty_sdk' and 'status' in argv:return subprocess.CompletedProcess(argv,0,' M modified.h')
        if failure=='version' and '-dumpmachine' in argv:return subprocess.CompletedProcess(argv,0,'riscv-none-elf')
        if '--build' in argv:
            if failure=='subprocess':return subprocess.CompletedProcess(argv,1,'Synthetic compiler failure')
            if failure=='timeout':raise subprocess.TimeoutExpired(argv,300,output=b'Synthetic timeout')
            if failure=='interrupt':raise KeyboardInterrupt()
            if failure=='source_drift':
                (builder.ROOT/'tools/build_firmware.py').write_text('changed during build')
        if failure=='wrong_cpu' and Path(argv[0]).name.endswith('readelf'):
            return subprocess.CompletedProcess(argv,0,'Tag_CPU_arch: v6-M')
        if failure=='wrong_metadata' and argv[1:3]==['info','-a']:
            return subprocess.CompletedProcess(argv,0,'target chip: RP2040')
        return real(argv,**kwargs)

    monkeypatch.setattr(builder.subprocess,'run',fail_run)
    with pytest.raises((builder.BuildError,KeyboardInterrupt)):builder.build(**args)
    m=json.loads((args['output']/'manifest.json').read_text())
    assert m['state']==('interrupted' if failure=='interrupt' else 'failed')
    assert not m['artifacts'] and not m['hardware_accessed'] and not m['policy_arm_allowed']
    assert 'error' in m
    assert not any(cmd[1] in {'load','reboot','erase'} for cmd in calls)


def test_existing_evidence_is_not_modified(environment):
    args,calls,_,_=environment
    args['output'].mkdir(); (args['output']/'manifest.json').write_text('preserve')
    with pytest.raises(FileExistsError):builder.build(**args)
    assert (args['output']/'manifest.json').read_text()=='preserve' and not calls


def test_compiler_environment_is_sanitized(environment,monkeypatch):
    args,_,real,_=environment
    for key in ('CC','CXXFLAGS','CPATH','PICO_PLATFORM','SOURCE_DATE_EPOCH'):
        monkeypatch.setenv(key,'unwanted override')
    def checked(argv,**kwargs):
        env=kwargs['env']
        assert not any(k in env for k in ('CC','CXXFLAGS','CPATH','PICO_PLATFORM'))
        assert env['SOURCE_DATE_EPOCH']=='1792972800'
        return real(argv,**kwargs)
    monkeypatch.setattr(builder.subprocess,'run',checked)
    assert builder.build(**args)['source_date_epoch']==1792972800


def test_generated_header_values_and_measured_calibration_are_rejected(tmp_path,monkeypatch):
    root=tmp_path/'repo'; out=tmp_path/'out'; out.mkdir()
    for name in ('calibrations/example.invalid.json','physical_spec.json','firmware/generated_config.h'):
        dest=root/name; dest.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(builder.ROOT/name,dest)
    monkeypatch.setattr(builder,'ROOT',root)
    header=root/'firmware/generated_config.h'
    header.write_text(header.read_text().replace('MAX_SPEED=3.141592654f','MAX_SPEED=4.0f'))
    with pytest.raises(builder.BuildError,match='Stale generated'):builder.verify_source(out)
    c=root/'calibrations/example.invalid.json';data=json.loads(c.read_text())
    data.update(state='measured',validated=True);c.write_text(json.dumps(data))
    with pytest.raises(builder.BuildError,match='invalid example'):builder.verify_source(out)


@pytest.mark.parametrize('failure',['wrong_elf','wrong_identity','wrong_family','duplicate','missing','bad_absolute'])
def test_artifact_inspection_rejects_corrupt_or_wrong_target(tmp_path,failure):
    identity={'configuration':'a'*64,'calibration':'b'*64}
    elf,uf2=artifact_files(tmp_path,identity)
    if failure=='wrong_elf':elf.write_bytes(b'not an ELF')
    if failure=='wrong_identity':identity['configuration']='c'*64
    if failure=='wrong_family':uf2.write_bytes(uf2_block(0xE48BFF56))
    if failure=='duplicate':uf2.write_bytes(uf2_block()+uf2_block())
    if failure=='missing':uf2.write_bytes(uf2_block(total=2))
    if failure=='bad_absolute':
        data=bytearray(uf2.read_bytes());data[32]=0;uf2.write_bytes(data)
    with pytest.raises(builder.BuildError):builder.inspect_artifacts(elf,uf2,identity)
