"""Finite CAD intersection audit. It cannot certify hardware shaft/horn fit."""
import json
import sys
from pathlib import Path
import itertools
import numpy as np
import trimesh
import mujoco

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_model import physical_bodies
from robot_config import JOINT_NAMES, HOME, JOINT_LOW, JOINT_HIGH


def main():
    spec = json.loads((ROOT / "physical_spec.json").read_text())
    bodies = physical_bodies(spec)
    model = mujoco.MjModel.from_xml_path(str(ROOT / "robot.xml"))
    data = mujoco.MjData(model)
    ids = [model.joint(j).qposadr[0] for j in JOINT_NAMES]
    poses = {"home": HOME, "zero": np.zeros(6), "all_low": JOINT_LOW, "all_high": JOINT_HIGH,
             "left_swing": np.deg2rad([-20, 25, 10, -10, 10, 0])}
    rng = np.random.default_rng(123)
    for i in range(50):
        poses[f"seed123_sample_{i}"] = rng.uniform(JOINT_LOW, JOINT_HIGH)
    results = []
    for pname, angles in poses.items():
        mujoco.mj_resetDataKeyframe(model, data, 0)
        data.qpos[ids] = angles
        mujoco.mj_forward(model, data)
        frames = {}
        own_intersections = []
        for b in bodies:
            local = trimesh.load_mesh(ROOT / "cad/stl" / (b["name"] + ".stl"))
            for c in b["components"]:
                if "servo" not in c["name"]:
                    continue
                box = trimesh.creation.box(extents=np.array(c["dimensions"]) * 1000)
                box.apply_translation(np.array(c["com"]) * 1000)
                intersection = trimesh.boolean.intersection([local, box], engine="manifold")
                if len(intersection.vertices) and intersection.volume > 1:
                    own_intersections.append({"frame": b["name"], "servo": c["name"], "overlap_mm3": float(intersection.volume)})
            transform = np.eye(4)
            transform[:3, :3] = data.xmat[model.body(b["name"]).id].reshape(3, 3)
            transform[:3, 3] = data.xpos[model.body(b["name"]).id] * 1000
            local.apply_transform(transform)
            frames[b["name"]] = local
        intersections = []
        for a, b in itertools.combinations(frames, 2):
            ma, mb = frames[a], frames[b]
            if np.any(ma.bounds[1] < mb.bounds[0]) or np.any(mb.bounds[1] < ma.bounds[0]):
                continue
            intersection = trimesh.boolean.intersection([ma, mb], engine="manifold")
            if len(intersection.vertices) and intersection.volume > 1:
                intersections.append({"a": a, "b": b, "overlap_mm3": float(intersection.volume)})
        results.append({"pose": pname, "frame_intersections": intersections, "own_servo_intersections": own_intersections})
    report = {"status": "FINITE PROTOTYPE AUDIT; holes/ears/horns unmeasured; not manufacturing approval", "poses": results}
    (ROOT / "docs/validation/clearances.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
