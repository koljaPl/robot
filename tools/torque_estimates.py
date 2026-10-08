"""Quasi-static gravity torques from virtual work, with the left foot fixed.

Ignores contacts of the right foot, tether, acceleration and structural flex.
Reports geometry demands, never an assertion of servo continuous strength.
"""
import json
from pathlib import Path
import sys
import numpy as np
import mujoco

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from robot_config import JOINT_NAMES, HOME


def main():
    m = mujoco.MjModel.from_xml_path(str(ROOT / "robot.xml"))
    d = mujoco.MjData(m)
    adr = [m.joint(n).qposadr[0] for n in JOINT_NAMES]
    left = m.body("left_foot").id

    def fixed_foot(angles):
        d.qpos[:] = m.key("home").qpos
        d.qpos[:3] = 0
        d.qpos[3:7] = [1, 0, 0, 0]
        d.qpos[adr] = angles
        mujoco.mj_forward(m, d)
        rotation = d.xmat[left].reshape(3, 3).T.copy()
        position = -rotation @ d.xpos[left] + [0, 0, 0.025]
        quat = np.zeros(4)
        mujoco.mju_mat2Quat(quat, rotation.reshape(9))
        d.qpos[:3] = position
        d.qpos[3:7] = quat
        mujoco.mj_forward(m, d)
        return float(np.sum(m.body_mass * d.xipos[:, 2]) * 9.81)

    rows = []
    for name, angles in [("home, all weight on left foot", HOME),
                         ("lateral lean toward support", np.deg2rad([-10, 10, 15, -10, 10, 15])),
                         ("lift right leg, lean toward left", np.deg2rad([-10, 10, 15, -30, 60, 15])),
                         ("deep stance bend, stress case", np.deg2rad([-30, 60, 15, -30, 60, 15]))]:
        torques = []
        for i in range(6):
            delta = np.zeros(6); delta[i] = 1e-5
            torques.append((fixed_foot(angles + delta) - fixed_foot(angles - delta)) / 2e-5)
        fixed_foot(angles)
        com = np.sum(m.body_mass[:, None] * d.xipos, axis=0) / m.body_mass.sum()
        rows.append({"pose": name, "angles_deg": np.rad2deg(angles).tolist(), "gravity_torque_Nm": torques,
                     "combined_com_m": com.tolist(), "max_abs_gravity_torque_Nm": max(abs(t) for t in torques),
                     "twice_static_demand_Nm": [2 * abs(t) for t in torques]})
    report = {"assumption": "entire weight on fixed left foot, right foot unloaded; equilibrium may be infeasible outside support polygon", "joint_order": JOINT_NAMES, "poses": rows}
    (ROOT / "docs/validation/torque_estimates.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
