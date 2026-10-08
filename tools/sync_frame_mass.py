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
        mesh = trimesh.load_mesh(ROOT / "cad/stl" / (body["name"] + ".stl"))
        mesh.apply_scale(0.001)
        mesh.density = 1270  # kg/m³ PETG; solid mesh, deliberately conservative
        mp = mesh.mass_properties
        frame = {"name": body["name"] + "_frame", "mass": float(mp.mass),
                 "dimensions": mesh.extents.tolist(), "com": mp.center_mass.tolist(),
                 "inertia_tensor": mp.inertia.tolist(), "material": "solid PETG estimate, 1270 kg/m³",
                 "evidence": "generated CAD; actual infill/printed density must be weighed"}
        body["components"][0] = frame
        if body["name"] != "torso":
            # Separate from servo masses, soles, and torso harness allowance.
            body["components"] = [c for c in body["components"] if not c["name"].endswith("_joint_fasteners")]
            body["components"].append({"name": body["name"] + "_joint_fasteners", "mass": 0.0015,
                "dimensions": [0.02, 0.012, 0.012], "com": [0, 0, -0.012],
                "material": "steel and plastic horns", "evidence": "estimate; weigh installed fasteners/horn"})
    torso = spec["bodies"][0]
    pico = next(c for c in torso["components"] if c["name"] == "pico_h")
    pico.update(dimensions=[0.006, 0.051, 0.021], com=[-0.0145, 0, 0.023])
    pca = next(c for c in torso["components"] if c["name"] == "pca9685")
    pca.update(dimensions=[0.009, 0.0625, 0.0254], com=[-0.013, 0, -0.002])
    imu = next(c for c in torso["components"] if c["name"] == "imu")
    imu.update(dimensions=[0.004, 0.016, 0.02], com=[-0.0255, 0, 0.018])
    harness = next(c for c in torso["components"] if c["name"] == "torso_wires_fasteners")
    harness["mass"] = 0.020
    harness["evidence"] = "estimate includes six added 10 cm extensions, short heavy power wire, capacitor, pullup, board mounting ties and torso hardware; excludes suspended tether"
    for b in spec["bodies"]:
        for c in b.get("components", []):
            if c["name"] == "left_sole":
                c.update(mass=0.00486, material="solid TPU 95A, density estimate 1200 kg/m³", evidence="estimate; includes adhesive uncertainty, weigh actual sole")
    path.write_text(json.dumps(spec, indent=2) + "\n")


if __name__ == "__main__":
    main()
