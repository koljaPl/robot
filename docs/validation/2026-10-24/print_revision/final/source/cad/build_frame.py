"""Editable constructive-solid-geometry prototype using the physical spec (mm).

Exports seven assembly components. Meshes are for fit-checking/quotations.
Servo ear, shaft and horn dimensions are unmeasured;
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
WALL = GEOMETRY["cad_wall"] * SCALE
CLEARANCE = GEOMETRY["cad_clearance"] * SCALE
MOUNT = GEOMETRY["mount"]
FEATURES = GEOMETRY["cad_features"]


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
    y = MOUNT["case_plate_y"] * SCALE
    p = box((MOUNT["case_plate_width"]*SCALE, WALL, MOUNT["case_plate_height"]*SCALE), (0, y, -dz))
    cut = FEATURES["tool_cut_depth"]*SCALE
    p -= box((dim[1]*SCALE + CLEARANCE, cut, dim[0]*SCALE + CLEARANCE), (0, y, -dz))
    for sign in (-1, 1):
        p -= hole(MOUNT["ear_clearance_diameter"]*SCALE/2, cut, (0, y, -dz + sign * SERVO["mounting_hole_spacing"] * SCALE / 2), "y")
    return p


def horn_plate():
    y = MOUNT["horn_plate_y"]*SCALE
    p = box(tuple(v*SCALE for v in MOUNT["horn_plate_dimensions"]), (0, y, 0))
    cut = FEATURES["tool_cut_depth"]*SCALE
    p -= hole(MOUNT["shaft_access_diameter"]*SCALE/2, cut, (0, y, 0), "y")
    # Radial slots accept several existing horn-hole radii after measurement.
    for sign in (-1, 1):
        p -= box((MOUNT["horn_slot_width"]*SCALE, cut, MOUNT["horn_slot_length"]*SCALE), (0, y, sign * MOUNT["horn_slot_radius"]*SCALE))
    return p


def thigh():
    length = GEOMETRY["thigh_length"] * SCALE
    p = horn_plate() + cradle().translate((0, 0, -length))
    # Return to the fixed servo-ear plane before the knee's moving horn sweep.
    # A straight plate on +Y would intersect the shin's top horn plate.
    for sign in (-1, 1):
        for feature in FEATURES["thigh_bridges"]:
            center=np.array(feature["center"])*SCALE;center[0]*=sign
            p += box(tuple(v*SCALE for v in feature["dimensions"]),tuple(center))
    return p


def shin():
    length = GEOMETRY["shin_length"] * SCALE
    web=length-FEATURES["shin_web_allowance"]*SCALE
    p = horn_plate() + box((MOUNT["horn_plate_dimensions"][0]*SCALE, WALL, web), (0, MOUNT["horn_plate_y"]*SCALE, -web/2))
    p -= box(tuple(v*SCALE for v in FEATURES["shin_window_dimensions"]), tuple(v*SCALE for v in FEATURES["shin_window_center"]))
    # Roll-axis moving horn plate: rotate pitch mount around Z to face +X.
    ankle = horn_plate().rotate((0, 0, -90)).translate((0, 0, -length))
    p += ankle
    # Corner rib joins the two perpendicular horn interfaces.
    center=np.array(FEATURES["shin_corner_offset_from_ankle"])*SCALE;center[2]-=length
    p += box(tuple(v*SCALE for v in FEATURES["shin_corner_dimensions"]),tuple(center))
    return p


def foot():
    dim = np.array(GEOMETRY["foot_dimensions"]) * SCALE
    pos = np.array(GEOMETRY["foot_center"]) * SCALE
    p = box(tuple(dim), tuple(pos))
    p += cradle().rotate((0, 0, -90))
    for sign in (-1, 1):
        center=np.array(FEATURES["foot_rib_center"])*SCALE;center[1]*=sign
        p += box(tuple(v*SCALE for v in FEATURES["foot_rib_dimensions"]),tuple(center))
    return p


def torso():
    back = MOUNT["torso_back_x"]*SCALE
    z=FEATURES["torso_window_center_z"]*SCALE
    p = box((WALL, GEOMETRY["torso_dimensions"][1]*SCALE, GEOMETRY["torso_dimensions"][2]*SCALE), (back, 0, z))
    p -= box(tuple(v*SCALE for v in FEATURES["torso_window_dimensions"]), (back, 0, z))
    for sign in (-1, 1):
        half = GEOMETRY["hip_half_spacing"] * SCALE
        mount = cradle()
        if sign < 0:
            mount = mount.mirror((0, 1, 0))
        p += mount.translate((0, sign * half, GEOMETRY["hip_z"] * SCALE))
        p += box(tuple(v*SCALE for v in FEATURES["torso_brace_dimensions"]),
                 (FEATURES["torso_brace_x"]*SCALE,sign*(half-FEATURES["torso_brace_hip_inset"]*SCALE),FEATURES["torso_brace_z"]*SCALE))
    # Through-hole rows permit screw-mounted boards or cable ties without drilling.
    for y in MOUNT["board_tie_y"]:
        for z in MOUNT["board_tie_z"]:
            p -= hole(MOUNT["board_tie_hole_diameter"]*SCALE/2, 10, (back, y*SCALE, z*SCALE), "x")
    # Solid dielectric stand-offs; PCB placement in the ledger clears their tips.
    # Tie slots stay available; no inserts, drilling or metal spacers required.
    for y in MOUNT["board_support_y"]:
        for z in MOUNT["board_support_z"]:
            p += box(tuple(v*SCALE for v in MOUNT["board_support_size"]),
                     (back + WALL/2 + MOUNT["board_support_size"][0]*SCALE/2, y*SCALE, z*SCALE))
    for y in MOUNT["imu_support_y"]:
        p += box(tuple(v*SCALE for v in MOUNT["imu_support_dimensions"]),
                 (back-WALL/2-MOUNT["imu_support_dimensions"][0]*SCALE/2,y*SCALE,MOUNT["imu_support_z"]*SCALE))
    return p


def ear_fastener():
    """M2x8 shank/head, nut and two washers, axis+Y; ear placement is estimated.

    Origin is plate centre. Nominal ear thickness is a fit hypothesis, not a
    sourced servo dimension. Do not use this shape to clear unknown horn hardware.
    """
    h = SPEC["hardware_interfaces"]["ear_bolt"]
    mm = lambda name: h[name]*SCALE
    near = WALL/2 + mm("washer_thickness")
    p = hole(mm("shaft_diameter")/2, mm("length_under_head"), (0, near-mm("length_under_head")/2, 0), "y")
    p += hole(mm("head_diameter")/2, mm("head_height"), (0, near+mm("head_height")/2, 0), "y")
    for y in (WALL/2+mm("washer_thickness")/2,
              -WALL/2-mm("ear_thickness_estimate")-mm("washer_thickness")/2):
        p += hole(mm("washer_od")/2, mm("washer_thickness"), (0,y,0), "y") - hole(mm("washer_id")/2, 3, (0,y,0), "y")
    nut_y = -WALL/2-mm("ear_thickness_estimate")-mm("washer_thickness")-mm("nut_height")/2
    nut = md.Manifold.cylinder(mm("nut_height"), mm("nut_across_flats")/np.sqrt(3), circular_segments=6, center=True)
    p += nut.rotate((90,0,0)).translate((0,nut_y,0))
    return p


def hardware_meshes():
    """Dimensioned ear hardware in owning body coordinates; no mystery mass boxes."""
    out = {}
    for body in physical_bodies(SPEC):
        for component in body["components"]:
            if "_ear_bolt_" not in component["name"]:
                continue
            solid = ear_fastener()
            if "ankle" in component["name"]:
                solid = solid.rotate((0,0,-90))
            elif component["name"].startswith("right_"):
                solid = solid.mirror((0,1,0))
            solid = solid.translate(tuple(v*SCALE for v in component["com"]))
            out[component["name"]] = (body["name"], mesh(solid))
    return out


def mesh(solid):
    raw = solid.to_mesh()
    return trimesh.Trimesh(vertices=np.array(raw.vert_properties)[:, :3], faces=np.array(raw.tri_verts), process=True)


def generate():
    folder = ROOT / "cad" / "stl"
    folder.mkdir(parents=True, exist_ok=True)
    # Superseded generated geometry is preserved under docs/history, never shipped
    # as current order quantities alongside the new ordinary-pad revision.
    for obsolete in ("left_sole.stl", "right_sole.stl", "quotation_plate.stl"):
        (folder / obsolete).unlink(missing_ok=True)
    shapes = {"torso": torso(), "left_thigh": thigh(), "left_shin": shin(), "left_foot": foot()}
    for part in ("thigh", "shin", "foot"):
        shapes["right_" + part] = shapes["left_" + part].mirror((0, 1, 0))
    report = []
    for index, (name, solid) in enumerate(shapes.items()):
        m = mesh(solid)
        if not m.is_watertight or m.volume <= 0:
            raise RuntimeError(f"Invalid printable mesh: {name}")
        m.export(folder / (name + ".stl"))
        report.append({"part": name, "quantity": 1, "bounding_box_mm": m.extents.tolist(),
                       "volume_cm3": m.volume / 1000, "solid_petg_mass_g_at_1_27": m.volume / 1000 * 1.27,
                       "connected_components": len(m.split()), "watertight": bool(m.is_watertight)})
    summary = {"status": "PROVISIONAL FIT/COST PROTOTYPE; NOT RELEASED FOR MANUFACTURE",
               "units": "mm", "clearance_mm": CLEARANCE,
               "parts": report, "total_solid_volume_cm3": sum(p["volume_cm3"] for p in report),
               "total_solid_petg_mass_g": sum(p["solid_petg_mass_g_at_1_27"] for p in report),
               "additional_parts": [{"part": "ordinary Delock18309 adhesive TPE pad", "quantity": 8, "printed": False, "dimensions_mm": [10,10,3]}],
               "revision": SPEC["revision"],
               "print_request": "7 PETG frames ONLY: 0.2mm layers, 3walls,25%infill. No printed soles/filament purchase. Quote support removal, usable holes without student drilling, fit sample, finishing, VAT and delivery separately; no manufacturing release."}
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
        for component in b['components']:
            if 'servo' not in component['name'] and component['name'] not in ('pico','imu') and not component['name'].startswith('pico_header_') and '_pad_' not in component['name']:
                continue
            case = (trimesh.creation.cylinder(radius=component['radius']*SCALE,height=component['dimensions'][2]*SCALE)
                    if component.get('primitive')=='cylinder_z' else trimesh.creation.box(extents=np.array(component['dimensions'])*SCALE))
            case.apply_translation(origins[b['name']]+extra+np.array(component['com'])*SCALE)
            ax.add_collection3d(Poly3DCollection(case.triangles,alpha=.55,facecolor='#333333' if 'servo' in component['name'] or '_pad_' in component['name'] else '#36a55c',linewidths=.05,edgecolor='#222222'))
        c = m.centroid
        ax.text(*c, b["name"], fontsize=8, color="black", bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none", "pad": 1})
    ax.set(xlim=(-55, 70), ylim=(-105, 105), zlim=(-40, 200), xlabel="x forward (mm)", ylabel="y left (mm)", zlabel="z up (mm)")
    ax.set_box_aspect((125, 210, 240)); ax.view_init(elev=17, azim=-45)
    ax.set_title("S6 exploded assembly envelopes — blue PETG, grey servos, green PCBs; fit unmeasured")
    fig.savefig(ROOT / "cad" / "exploded.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    generate()
