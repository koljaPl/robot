"""Place unchanged provisional parts on individual A1-mini-sized plates (mm).

This checks bounding boxes, not layer strength, supports or servo/horn fit.
The old 185 mm quotation batch is deliberately not used or overwritten.
"""
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

ROTATIONS = {"torso": (0, 90, 0), "thigh": (90, 0, 0),
             "shin": (0, 90, 0), "foot": (0, 0, 0)}


def place(mesh, rotation, xy=(5, 5)):
    result = mesh.copy()
    result.apply_transform(trimesh.transformations.euler_matrix(*np.deg2rad(rotation)))
    result.apply_translation(-result.bounds[0] + [*xy, 0])
    if not result.is_watertight or result.volume <= 0:
        raise ValueError("Invalid source mesh")
    if np.any(result.bounds[0] < -1e-5) or np.any(result.bounds[1] > [175, 175, 180]):
        raise ValueError("Plate exceeds A1 mini with 5 mm XY edge margin")
    if not np.isclose(mesh.volume, result.volume, rtol=1e-6):
        raise ValueError("Placement changed geometry volume")
    return result


def generate(folder=None):
    from cad.build_frame import cradle, horn_plate, mesh
    folder = Path(folder or ROOT / "cad/local_print")
    folder.mkdir(parents=True, exist_ok=True)
    records = []
    for name in ("torso", "left_thigh", "right_thigh", "left_shin", "right_shin", "left_foot", "right_foot"):
        src = ROOT / "cad/stl" / f"{name}.stl"
        original = trimesh.load_mesh(src)
        rotation = ROTATIONS[name.split("_")[-1]]
        placed = place(original, rotation)
        target = folder / f"plate_{name}.stl"
        placed.export(target)
        records.append({"part": name, "quantity": 1, "file": target.name,
                        "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
                        "rotation_deg": rotation, "bounds_mm": placed.bounds.tolist(),
                        "volume_mm3": float(placed.volume),
                        "components": len(placed.split())})
    # Actual current CAD interfaces, not a made-up gauge: test both before a frame.
    samples = [place(mesh(cradle()), (90, 0, 0)),
               place(mesh(horn_plate()), (90, 0, 0), xy=(35, 5))]
    sample = trimesh.util.concatenate(samples)
    sample.export(folder / "FIRST_interface_sample.stl")
    report = {"state": "PROVISIONAL LAYOUT ONLY; NO MANUFACTURING RELEASE",
              "units": "mm", "bed_mm": [180, 180, 180], "xy_edge_margin_mm": 5,
              "parts": records, "frame_parts": 7,
              "sample": {"file": "FIRST_interface_sample.stl", "components": 2,
                         "purpose": "Current servo ear cradle + horn plate; measure actual hardware first",
                         "bounds_mm": sample.bounds.tolist()},
              "source_cad_sha256": hashlib.sha256((ROOT / "cad/build_frame.py").read_bytes()).hexdigest(),
              "physical_spec_sha256": hashlib.sha256((ROOT / "physical_spec.json").read_bytes()).hexdigest(),
              "slicer_verified": False, "structural_orientation_verified": False,
              "material": "One full 1 kg PETG spool counted in robot basket; no TPU spool",
              "notes": "Open ONE plate at a time, units mm, scale100%. Old185mm batch does not fit. No supports/holes/strength certified. Grip pads are a proposed revision, not current model contacts."}
    (folder / "layout.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    result = generate()
    print(f"Prepared {result['frame_parts']} individual plates + first interface sample; not print-approved")
