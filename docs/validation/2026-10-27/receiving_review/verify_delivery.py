"""Read-only source/link/archive check for this receiving-review delivery."""
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from calibration import configuration_identity
from tools.package_project import project_files


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def text_without_code(path):
    text = path.read_text()
    return re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)


def anchors(path):
    counts, values = {}, set()
    for title in re.findall(r'^#+\s+(.+?)\s*#*$', text_without_code(path), flags=re.M):
        title = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', title)
        title = re.sub(r'<[^>]*>', '', title).lower()
        anchor = re.sub(r'[^\w\- ]', '', title).replace(' ', '-')
        count = counts.get(anchor, 0);counts[anchor] = count + 1
        values.add(anchor + ('-' + str(count) if count else ''))
    return values


def main():
    before = json.loads((HERE / 'unchanged_before.json').read_text())
    assert all(sha(ROOT / name) == value for name, value in before.items()), 'Protected file changed'
    assert not any(json.loads((ROOT / 'docs/gates.json').read_text()).values())
    current = configuration_identity()['configuration']
    baseline = json.loads((ROOT / 'docs/baselines/scripted_bench_tools.json').read_text())
    assert current == baseline['configuration_identity']['configuration']
    assert all(sha(ROOT / name) == value for name, value in baseline['source_sha256'].items())
    manifest = json.loads((ROOT / 'print_for_classmate/manifest.json').read_text())
    assert all(sha(ROOT / 'print_for_classmate' / f['file']) == f['sha256'] for f in manifest['files'])
    docs = ['README.md', 'SUMMARY.md', 'PLAN.md', 'AGENTS.md', 'docs/STATUS.md',
            'docs/ROADMAP.md', 'docs/VALIDATION_CURRENT.md', 'docs/HANDOFF.md',
            'docs/PROCUREMENT_ACTIONS.md', 'docs/RECEIVING.md', 'docs/RECEIVING_CHECKLIST.md',
            str(HERE.relative_to(ROOT) / 'README.md')]
    checked = 0
    for name in docs:
        path = ROOT / name
        for url in re.findall(r'\[[^]\n]*\]\(([^)\n]+)\)', text_without_code(path)):
            url = unquote(url.strip('<>'))
            parts = urlsplit(url)
            if parts.scheme or parts.netloc:
                continue
            target = (path.parent / parts.path).resolve() if parts.path else path
            assert target.exists(), (name, url)
            if parts.fragment and target.suffix == '.md':
                assert parts.fragment in anchors(target), (name, url, 'missing anchor')
            checked += 1
    handoff = (ROOT / 'docs/HANDOFF.md').read_text()
    sections = re.findall(r'^## (\d+)\.', handoff, re.M)
    assert sections == [str(i) for i in range(1, 20)], sections
    template = (ROOT / 'docs/HANDOFF.template.md').read_text()
    code = re.findall(r'\{\{CODE:([^}]+)\}\}', template)
    assert all((ROOT / name).read_text().rstrip() in handoff for name in code), 'Stale embedded code'
    expected = {str(rel): path for path, rel in project_files()}
    with zipfile.ZipFile(ROOT / 'school_biped_s6.zip') as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert len(names) == len(set(names)) and set(names) == set(expected)
        assert all(hashlib.sha256(archive.read(name)).hexdigest() == sha(path)
                   for name, path in expected.items()), 'Archive/source mismatch'
        for name in names:
            parts = Path(name).parts
            assert not any(p.startswith('.') or p in ('local_records', 'receiving_records', 'build', '__pycache__') for p in parts)
            assert 'PRIVATE_RECEIVING_RECORD' not in parts
        for name in ('PLAN.md', 'tools/review_receiving.py', 'docs/RECEIVING_CHECKLIST.md',
                     'docs/templates/receiving.example.json', 'tests/test_receiving_review.py'):
            assert name in names
    print(json.dumps({'state': 'locally_verified_only', 'protected_files_unchanged': len(before),
                      'configuration': current, 'local_links_checked': checked,
                      'handoff_sections': len(sections), 'exact_code_inclusions': len(code),
                      'archive_members': len(expected), 'archive_sources_equal': True,
                      'print_zip_unchanged': True, 'physical_gates': False}, indent=2))


if __name__ == '__main__':
    main()
