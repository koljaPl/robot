"""Generate MJCF and body mass/COM/inertia table from physical_spec.json.

Frames use solid-CAD inertia; other components use uniform-box estimates.
Aggregate with the parallel-axis theorem. None are measured hardware inertias.
Model remains provisional until hardware gates pass.
"""
import copy
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from robot_config import ROOT, HOME, SERVO_KP, SERVO_KV, SERVO_TORQUE, PHYSICS_DT


def physical_bodies(spec):
    bodies = copy.deepcopy(spec["bodies"])
    lookup = {body["name"]: body for body in bodies}
    for body in bodies:
        if "mirror_of" in body:
            body["components"] = copy.deepcopy(lookup[body["mirror_of"]]["components"])
            for comp in body["components"]:
                comp["name"] = comp["name"].replace("left_", "right_")
                comp["com"][1] *= -1
                if "inertia_tensor" in comp:
                    mirror = np.diag([1, -1, 1])
                    comp["inertia_tensor"] = (mirror @ np.array(comp["inertia_tensor"]) @ mirror).tolist()
    return bodies


def aggregate(components):
    mass = sum(c["mass"] for c in components)
    com = sum(c["mass"] * np.array(c["com"]) for c in components) / mass
    inertia = np.zeros((3, 3))
    for c in components:
        m = c["mass"]
        x, y, z = c["dimensions"]
        inertia += np.array(c.get("inertia_tensor", np.diag([m * (y*y + z*z) / 12, m * (x*x + z*z) / 12, m * (x*x + y*y) / 12])))
        d = np.array(c["com"]) - com
        inertia += m * (np.dot(d, d) * np.eye(3) - np.outer(d, d))
    return mass, com, inertia


def fmt(values):
    return " ".join(f"{x:.10g}" for x in np.atleast_1d(values))


def generate(output=ROOT / "robot.xml"):
    spec = json.loads((ROOT / "physical_spec.json").read_text())
    bodies = physical_bodies(spec)
    dyn = spec["dynamics"]
    root = ET.Element("mujoco", model="SchoolBipedS6_provisional")
    ET.SubElement(root, "compiler", angle="radian", autolimits="true", inertiafromgeom="false")
    ET.SubElement(root, "option", timestep=str(PHYSICS_DT), gravity="0 0 -9.81", integrator="implicitfast", iterations="60")
    visual = ET.SubElement(root, "visual")
    ET.SubElement(visual, "global", offwidth="960", offheight="720")
    ET.SubElement(visual, "map", znear="0.002")
    default = ET.SubElement(root, "default")
    ET.SubElement(default, "joint", limited="false", damping=str(dyn["damping_nm_s_rad"]["value"]), armature=str(dyn["armature_kg_m2"]["value"]), frictionloss=str(dyn["frictionloss_nm"]["value"]))
    ET.SubElement(default, "geom", condim="3", friction=fmt([dyn["sliding_friction"]["value"],0.005,0.0001]), solref="0.008 1", solimp="0.9 0.95 0.001")
    ET.SubElement(default, "position", kp=str(SERVO_KP), kv=str(SERVO_KV), forcelimited="true", forcerange=fmt([-SERVO_TORQUE, SERVO_TORQUE]), ctrllimited="true")
    asset = ET.SubElement(root, "asset")
    for b in bodies:
        ET.SubElement(asset, "mesh", name=b["name"] + "_mesh", file="cad/stl/" + b["name"] + ".stl", scale="0.001 0.001 0.001")
    world = ET.SubElement(root, "worldbody")
    ET.SubElement(world, "light", pos="0 -1 2", dir="0 0 -1", diffuse="0.8 0.8 0.8")
    ET.SubElement(world, "geom", name="floor", type="plane", size="3 3 0.05", rgba="0.87 0.88 0.90 1")
    elems = {"world": world}
    table = []
    for b in bodies:
        elem = ET.SubElement(elems[b["parent"]], "body", name=b["name"], pos=fmt(b["position"]))
        elems[b["name"]] = elem
        ET.SubElement(elem, "geom", name=b["name"] + "_visual", type="mesh", mesh=b["name"] + "_mesh", contype="0", conaffinity="0", group="2", rgba="0.12 0.55 0.83 1")
        mass, com, tensor = aggregate(b["components"])
        full = [tensor[0, 0], tensor[1, 1], tensor[2, 2], tensor[0, 1], tensor[0, 2], tensor[1, 2]]
        ET.SubElement(elem, "inertial", mass=fmt(mass), pos=fmt(com), fullinertia=fmt(full))
        table.append({"body": b["name"], "mass_kg": mass, "com_m": com.tolist(), "fullinertia_kg_m2": full, "components": b["components"]})
        if b["name"] == "torso":
            ET.SubElement(elem, "freejoint", name="root")
            ET.SubElement(elem, "geom", name="torso_collision", type="box", pos="0 0 0.01", size="0.02 0.041 0.025", rgba="0.10 0.45 0.8 0.8")
            imu = next(c for c in b["components"] if c["name"] == "imu")
            ET.SubElement(elem, "site", name="imu_site", pos=fmt(imu["com"]), size="0.003", rgba="1 0.7 0 1")
            ET.SubElement(elem, "camera", name="overview", pos="0.42 -0.5 0.24", xyaxes="0.766 0.643 0 -0.26 0.31 0.916")
        else:
            joint_args = dict(name=b["joint"], type="hinge", axis=fmt(b["axis"]))
            if b["mechanical_limits_deg"] is not None:
                joint_args.update(limited="true", range=fmt(np.deg2rad(b["mechanical_limits_deg"])))
            ET.SubElement(elem, "joint", **joint_args)
            if b["name"].endswith("foot"):
                ET.SubElement(elem, "geom", name=b["name"] + "_plate", type="box", pos=fmt(spec["geometry"]["foot_center"]), size=fmt(np.array(spec["geometry"]["foot_dimensions"]) / 2), rgba="0.08 0.36 0.65 1")
                solepos = np.array(spec["geometry"]["foot_center"]); solepos[2] -= (spec["geometry"]["foot_dimensions"][2] + spec["geometry"]["sole_thickness"]) / 2
                ET.SubElement(elem, "geom", name=b["name"] + "_sole", type="box", pos=fmt(solepos), size=fmt([* (np.array(spec["geometry"]["foot_dimensions"][:2]) / 2), spec["geometry"]["sole_thickness"] / 2]), rgba="0.15 0.15 0.15 1")
                ET.SubElement(elem, "site", name=b["name"] + "_sole_center", pos=fmt(solepos + [0, 0, -spec["geometry"]["sole_thickness"] / 2]), size="0.001")
            else:
                # Envelope of thin printed yoke, deliberately narrow for simple contacts.
                ET.SubElement(elem, "geom", name=b["name"] + "_link", type="capsule", fromto=fmt([0, 0, -0.006, 0, 0, -(spec["geometry"]["thigh_length"] if b["name"].endswith("thigh") else spec["geometry"]["shin_length"]) + 0.006]), size="0.006", rgba="0.12 0.55 0.83 1")
        for c in b["components"]:
            if "servo" in c["name"]:
                ET.SubElement(elem, "geom", name=c["name"] + "_case", type="box", pos=fmt(c["com"]), size=fmt(np.array(c["dimensions"]) / 2), rgba="0.15 0.15 0.17 1")
    act = ET.SubElement(root, "actuator")
    for b in bodies[1:]:
        ET.SubElement(act, "position", name=b["joint"] + "_servo", joint=b["joint"], ctrlrange=fmt(np.deg2rad(b["safe_command_deg"])))
    sensors = ET.SubElement(root, "sensor")
    ET.SubElement(sensors, "gyro", name="imu_gyro", site="imu_site")
    ET.SubElement(sensors, "accelerometer", name="imu_accel", site="imu_site")
    # Freejoint then L hip/knee/ankle then R hip/knee/ankle follows tree order.
    keys = ET.SubElement(root, "keyframe")
    ET.SubElement(keys, "key", name="home", qpos=fmt([0, 0, bodies[0]["position"][2], 1, 0, 0, 0, *HOME]), ctrl=fmt(HOME))
    ET.indent(root)
    ET.ElementTree(root).write(output, encoding="unicode", xml_declaration=False)
    Path(output).write_text('<!-- Generated from physical_spec.json; provisional hardware model. -->\n' + Path(output).read_text() + '\n')
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "mass_properties.json").write_text(json.dumps({"total_mass_kg": sum(b["mass_kg"] for b in table), "bodies": table}, indent=2) + "\n")
    return table


if __name__ == "__main__":
    table = generate()
    print(f"Generated robot.xml: {sum(b['mass_kg'] for b in table):.4f} kg, six servos")
