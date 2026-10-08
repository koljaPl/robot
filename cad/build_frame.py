"""Editable constructive-solid-geometry prototype using the physical spec (mm).

Exports seven assembly components and a nested print plate. Meshes are for
fit-checking/quotations. Servo ear, shaft and horn dimensions are unmeasured;
do not order these as production-ready parts. No tapped holes or heat-set inserts.
"""
import json
from pathlib import Path
import sys
import numpy as np
import manifold3d as md
import trimesh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_model import physical_bodies

SPEC = json.loads((ROOT / "physical_spec.json").read_text())
GEOMETRY = SPEC["geometry"]
SERVO = SPEC["servo"]
SCALE = 1000
WALL = 3.0
CLEARANCE = 0.4


def box(dim, pos=(0, 0, 0)):
    return md.Manifold.cube(dim, center=True).translate(pos)


def hole(radius, length, pos, axis="z"):
    c = md.Manifold.cylinder(length, radius, circular_segments=32, center=True)
    if axis == "y":
        c = c.rotate((90, 0, 0))
    if axis == "x":
        c = c.rotate((0, 90, 0))
    return c.translate(pos)


def cradle():
    """Pitch servo ear plate, shaft axis +Y, interface origin on shaft."""
    dz = SERVO["shaft_offset_along_case_length"] * SCALE
    dim = SERVO["housing_dimensions"]
    p = box((20, WALL, 38), (0, -7, -dz))
    p -= box((dim[1]*SCALE + CLEARANCE, 12, dim[0]*SCALE + CLEARANCE), (0, -7, -dz))
    for sign in (-1, 1):
        p -= hole(1.2, 12, (0, -7, -dz + sign * SERVO["mounting_hole_spacing"] * SCALE / 2), "y")
    return p


def horn_plate():
    p = box((24, WALL, 28), (0, 3.5, 0))
    p -= hole(3, 12, (0, 3.5, 0), "y")
    # Radial slots accept several existing horn-hole radii after measurement.
    for sign in (-1, 1):
        p -= box((2.4, 12, 7), (0, 3.5, sign * 9))
    return p


def thigh():
    length = GEOMETRY["thigh_length"] * SCALE
    p = horn_plate() + cradle().translate((0, 0, -length))
    # Return to the fixed servo-ear plane before the knee's moving horn sweep.
    # A straight plate on +Y would intersect the shin's top horn plate.
    for sign in (-1, 1):
        p += box((4, WALL, 20), (sign * 10, 3.5, -22))
        p += box((4, 13.5, 4), (sign * 10, -1.75, -30))
        p += box((4, WALL, 13), (sign * 10, -7, -36.5))
    return p


def shin():
    length = GEOMETRY["shin_length"] * SCALE
    p = horn_plate() + box((24, WALL, length - 18), (0, 3.5, -(length - 18) / 2))
    p -= box((16, 10, 12), (0, 3.5, -23))
    # Roll-axis moving horn plate: rotate pitch mount around Z to face +X.
    ankle = horn_plate().rotate((0, 0, -90)).translate((0, 0, -length))
    p += ankle
    # Corner rib joins the two perpendicular horn interfaces.
    p += box((6, 8, 12), (5, 3, -length + 14))
    return p


def foot():
    dim = np.array(GEOMETRY["foot_dimensions"]) * SCALE
    pos = np.array(GEOMETRY["foot_center"]) * SCALE
    p = box(tuple(dim), tuple(pos))
    p += cradle().rotate((0, 0, -90))
    for sign in (-1, 1):
        p += box((12, 4, 14), (-7, sign * 8.5, -17))
    return p


def torso():
    p = box((WALL, 82, 66), (-20, 0, 2))
    p -= box((10, 42, 24), (-20, 0, 2))
    for sign in (-1, 1):
        half = GEOMETRY["hip_half_spacing"] * SCALE
        mount = cradle()
        if sign < 0:
            mount = mount.mirror((0, 1, 0))
        p += mount.translate((0, sign * half, GEOMETRY["hip_z"] * SCALE))
        p += box((16, 6, 8), (-14, sign * (half - 7), -18))
    # Through-hole rows permit screw-mounted boards or cable ties without drilling.
    for y in (-32, -16, 16, 32):
        for z in (10, 28):
            p -= hole(1.6, 10, (-20, y, z), "x")
    return p


def mesh(solid):
    raw = solid.to_mesh()
    return trimesh.Trimesh(vertices=np.array(raw.vert_properties)[:, :3], faces=np.array(raw.tri_verts), process=True)


def generate():
    folder = ROOT / "cad" / "stl"
    folder.mkdir(parents=True, exist_ok=True)
    shapes = {"torso": torso(), "left_thigh": thigh(), "left_shin": shin(), "left_foot": foot()}
    for part in ("thigh", "shin", "foot"):
        shapes["right_" + part] = shapes["left_" + part].mirror((0, 1, 0))
    report = []
    plate = []
    for index, (name, solid) in enumerate(shapes.items()):
        m = mesh(solid)
        if not m.is_watertight or m.volume <= 0:
            raise RuntimeError(f"Invalid printable mesh: {name}")
        m.export(folder / (name + ".stl"))
        report.append({"part": name, "quantity": 1, "bounding_box_mm": m.extents.tolist(),
                       "volume_cm3": m.volume / 1000, "solid_petg_mass_g_at_1_27": m.volume / 1000 * 1.27,
                       "connected_components": len(m.split()), "watertight": bool(m.is_watertight)})
        layout = m.copy()
        # Quotation plate only; a printer must choose final support/orientation.
        layout.apply_translation(-layout.bounds[0] + [index % 3 * 110, index // 3 * 110, 0])
        plate.append(layout)
    trimesh.util.concatenate(plate).export(folder / "quotation_plate.stl")
    # Separate material: two ready-sized TPU traction soles. Supplier bonds these
    # to the corresponding PETG feet; include adhesive/finishing in the quote.
    sole = mesh(box((90, 45, 1), (6, 0, -24.5)))
    for side in ("left", "right"):
        sole.export(folder / (side + "_sole.stl"))
    summary = {"status": "PROVISIONAL FIT/COST PROTOTYPE; NOT RELEASED FOR MANUFACTURE",
               "units": "mm", "clearance_mm": CLEARANCE,
               "parts": report, "total_solid_volume_cm3": sum(p["volume_cm3"] for p in report),
               "total_solid_petg_mass_g": sum(p["solid_petg_mass_g_at_1_27"] for p in report),
               "additional_parts": [{"part": "TPU sole", "quantity": 2, "dimensions_mm": [90, 45, 1], "estimated_mass_each_g": 4.86}],
               "print_request": "7 PETG frames: 0.2 mm layers, 3 perimeters, 25% infill. 2 TPU 95A soles, bonded to feet with adhesive included. All through holes clear without drilling; supports removed; include VAT and shipping. Quotation plate excludes soles and is not a printer-bed layout."}
    (ROOT / "cad" / "print_manifest.json").write_text(json.dumps(summary, indent=2) + "\n")
    draw_exploded(shapes)
    print(json.dumps(summary, indent=2))
    return summary


def draw_exploded(shapes):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from build_model import physical_bodies
    fig = plt.figure(figsize=(10, 9))
    ax = fig.add_subplot(111, projection="3d")
    origins = {}
    for b in physical_bodies(SPEC):
        origins[b["name"]] = np.array(b["position"]) * SCALE + origins.get(b["parent"], np.zeros(3))
        extra = np.zeros(3)
        if "left" in b["name"]:
            extra[1] = 35
        if "right" in b["name"]:
            extra[1] = -35
        if "shin" in b["name"]:
            extra[2] = -15
        if "foot" in b["name"]:
            extra[2] = -30
        m = mesh(shapes[b["name"]])
        m.apply_translation(origins[b["name"]] + extra)
        poly = Poly3DCollection(m.triangles, alpha=0.75, facecolor="#4299ce", linewidths=0.03, edgecolor="#245174")
        ax.add_collection3d(poly)
        c = m.centroid
        ax.text(*c, b["name"], fontsize=8, color="black", bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none", "pad": 1})
    ax.set(xlim=(-55, 70), ylim=(-105, 105), zlim=(-40, 200), xlabel="x forward (mm)", ylabel="y left (mm)", zlabel="z up (mm)")
    ax.set_box_aspect((125, 210, 240)); ax.view_init(elev=17, azim=-45)
    ax.set_title("S6 exploded frame concept — provisional, hardware fit unmeasured")
    fig.savefig(ROOT / "cad" / "exploded.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    generate()
