"""Update the authoritative specification from STL solid-PETG estimates.

This is a conservative homogeneous solid estimate, not measured printed mass.
Re-run after CAD edits, then run build_model.py. Coordinates of each STL are
the corresponding rigid body's coordinates; STL millimetres become SI units.
"""
import json
from pathlib import Path
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / "physical_spec.json"
    spec = json.loads(path.read_text())
    for body in spec["bodies"]:
        if "mirror_of" in body:
            continue
        if any(c.get("parameter_evidence", {}).get("mass", {}).get("state") == "measured" for c in body.get("components", [])):
            raise ValueError("Refusing to overwrite measured mass: " + body["name"])
        mesh = trimesh.load_mesh(ROOT / "cad/stl" / (body["name"] + ".stl"))
        mesh.apply_scale(0.001)
        mesh.density = spec["geometry"]["petg_density"]  # kg/m³ PETG; solid mesh, deliberately conservative
        mp = mesh.mass_properties
        frame = {"name": body["name"] + "_frame", "mass": float(mp.mass),
                 "dimensions": mesh.extents.tolist(), "com": mp.center_mass.tolist(),
                 "inertia_tensor": mp.inertia.tolist(), "material": "solid PETG estimate, 1270 kg/m³",
                 "evidence": "generated CAD; actual infill/printed density must be weighed"}
        frame["parameter_evidence"] = {k: {"state": "estimated", "date": spec["updated_date"], "evidence": frame["evidence"]} for k in ("mass", "com", "dimensions", "inertia_tensor")}
        body["components"][0] = frame
        # Existing horns/fasteners/electronics are independent ledger entries.
        # Never recreate them from a generic allowance or erase their provenance.
    path.write_text(json.dumps(spec, indent=2) + "\n")


if __name__ == "__main__":
    main()
