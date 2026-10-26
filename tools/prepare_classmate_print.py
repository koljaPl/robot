"""Create a small separate print folder/ZIP; no upload, order or fit approval."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

import trimesh

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create(output):
    output = Path(output)
    if output.exists() or output.with_suffix('.zip').exists():
        raise ValueError('Use a new folder/ZIP; preserve existing print packages')
    source = ROOT/'cad/print_order'
    manifest = json.loads((source/'manifest.json').read_text())
    spec = json.loads((ROOT/'physical_spec.json').read_text())
    if sha(ROOT/'physical_spec.json') != manifest['physical_spec_sha256']:
        raise ValueError('Print manifest is stale; regenerate prepare_print_order.py first')
    prepared = []
    for row in manifest['files']:
        p = source/row['file']
        if sha(p) != row['sha256']:
            raise ValueError('Print source hash mismatch: '+row['file'])
        mesh = trimesh.load_mesh(p)
        if not mesh.is_watertight or mesh.volume <= 0 or len(mesh.split()) != 1:
            raise ValueError('Invalid/disconnected printable part: '+row['file'])
        folder = '01_FIT_SAMPLE' if row['file'].startswith('sample/') else '02_FRAME'
        prepared.append((p, folder+'/'+p.name, mesh))
    assert sum('/' in name and name.startswith('01_') for _, name, _ in prepared) == 2
    assert len(prepared) == 9
    output.mkdir(parents=True)
    files = []
    for src, name, mesh in prepared:
        dest = output/name; dest.parent.mkdir(exist_ok=True); shutil.copy2(src, dest)
        files.append({'file': name, 'quantity': 1, 'units': 'mm', 'sha256': sha(dest),
                      'bounds_mm': mesh.bounds.tolist(), 'dimensions_mm': mesh.extents.tolist(),
                      'volume_cm3': float(mesh.volume/1000), 'watertight': True, 'connected_parts': 1})
    drawings = output/'03_DRAWINGS'; drawings.mkdir()
    for src, name in ((source/'drawings/interfaces.png', 'interfaces.png'),
                      (source/'drawings/interfaces.svg', 'interfaces.svg'),
                      (ROOT/'cad/exploded.png', 'exploded.png'),
                      (source/'fasteners.csv', 'fasteners.csv'),
                      (source/'ORIENTATION_REVIEW.md', 'ORIENTATION_REVIEW.md')):
        shutil.copy2(src, drawings/name)
    (output/'00_START_HERE.md').write_text('''# Druckdateien für den Schulroboter S6

## Reihenfolge und Stückzahlen

1. **Zuerst `01_FIT_SAMPLE`: beide STL-Dateien je 1× drucken.**
   Servo-Halter und Hornplatte mit dem echten MG90S, Originalhorn und Schrauben
   testen. Nicht bohren, aufbiegen oder mit Gewalt montieren. Bei schlechtem Sitz
   Maße/Fotos zurückgeben und Dateien korrigieren, bevor der ganze Rahmen entsteht.
2. **Danach `02_FRAME`: sieben STL-Dateien je 1×**, sobald die Probe passt:
   `torso`, `left_thigh`, `right_thigh`, `left_shin`, `right_shin`,
   `left_foot`, `right_foot`. Links/rechts nicht zusätzlich spiegeln.
3. Die zwei Probestücke gehören nicht in den fertigen Roboter. Keine zusätzlichen
   kombinierten Platten, Servohörner oder TPU-Sohlen drucken. Acht gekaufte Pads
   werden später an den Füßen befestigt.

## Einstellungen und Prüfung im Slicer

- Alle STL-Dateien sind **Millimeter**, Skalierung **100%**. Jede enthält genau
  ein Teil und ist bereits zur Druckbett-Lage gedreht. Abmessungen im Manifest
  gegen den Slicer prüfen; die Dateien einzeln importieren/auf die Platte setzen.
- Material **PETG**, zunächst **0,20 mm Schichthöhe, 3 Wände, 25% Infill**.
  Das sind Startwerte; Schichthaftung, Brücken und belastete Laschen im Slicer
  prüfen. Drucklage nicht blind ändern; siehe `03_DRAWINGS/ORIENTATION_REVIEW.md`.
- Passende PETG-Temperatur/Lüftung nach dem tatsächlich verwendeten Filament wählen.
  Falls nötig Stützen verwenden und vollständig entfernen, ohne dünne Laschen
  zu beschädigen. Keine neuen Schraublöcher im Teil durch Stützen verschließen.
- Montagebohrungen/Schlitze müssen nach dem Druck nutzbar sein. Falls die Probe
  nicht passt oder Nacharbeit nötig wäre, vor dem Rahmendruck Rücksprache halten.
- Einzelteil-Maße, Layerfehler und Verzug prüfen; fertig gedruckte Teile wiegen.
  Druckzeit, Filamentverbrauch und tatsächliche Kosten bitte notieren.

## Stand und Unterlagen

Der Nutzer hat Drucken beim Klassenkameraden als Vorgehen bestätigt. Preis und
Transport sind noch nicht beziffert. **Es wurde noch kein physischer Sitz oder
Festigkeit nachgewiesen.** Diese Dateien sind druckbare Entwürfe mit vorgeschalteter
Passprobe, keine Garantie für fertige Mechanik. Änderungen nur mit neuer Revision.
`manifest.json` enthält Mengen, Maße und SHA-256-Hashes; Zeichnungen und
Schraubenliste liegen unter `03_DRAWINGS`. Der Pico 2 hat denselben dokumentierten
51×21-mm-Platzbedarf; reale Stecker/Lötstellen trotzdem prüfen.
''')
    result = {'revision': spec['revision'], 'frame_geometry': 'r2 unchanged; controller selection Pico 2',
              'state': 'user-selected classmate printing; sample-first, physical fit/strength unverified',
              'units': 'mm', 'scale_percent': 100, 'frame_parts': 7, 'fit_samples': 2,
              'physical_spec_sha256': sha(ROOT/'physical_spec.json'), 'files': files,
              'all_package_files_sha256': {str(p.relative_to(output)): sha(p) for p in sorted(output.rglob('*')) if p.is_file()},
              'price_eur': None, 'physical_fit_verified': False}
    (output/'manifest.json').write_text(json.dumps(result, indent=2)+'\n')
    with zipfile.ZipFile(output.with_suffix('.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(output.rglob('*')):
            if p.is_file(): z.write(p, str(p.relative_to(output.parent)))
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, default=ROOT/'print_for_classmate')
    a = p.parse_args(); r = create(a.output)
    print(json.dumps({k: r[k] for k in ('revision', 'frame_parts', 'fit_samples', 'physical_fit_verified')}))


if __name__ == '__main__': main()
