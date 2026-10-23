"""Create reviewable quote bundle and portable project, excluding installs/runs."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    names = ["torso", "left_thigh", "left_shin", "left_foot", "right_thigh", "right_shin", "right_foot", "left_sole", "right_sole"]
    with zipfile.ZipFile(ROOT / "cad/quote_bundle.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for name in names:
            z.write(ROOT / f"cad/stl/{name}.stl", f"stl/{name}.stl")
        for path in ("cad/QUOTE_REQUEST.md", "cad/ASSEMBLY.md", "cad/exploded.png", "cad/print_manifest.json", "physical_spec.json"):
            z.write(ROOT / path, path)
    with zipfile.ZipFile(ROOT / "school_biped_s6.zip", "w", zipfile.ZIP_DEFLATED) as z:
        roots = ["docs", "cad", "tests", "tools", "firmware", "calibrations"]
        candidates = [ROOT / name for name in ("AGENTS.md", "SUMMARY.md", "README.md", "requirements.txt", "requirements-dev.txt", "robot.xml", "physical_spec.json", "procurement.json", "build_model.py", "robot_config.py", "humanoid_env.py", "servo_control.py", "imu_observation.py", "gait_metrics.py", "calibration.py", "hardware_interface.py", "serial_robot.py", "bench.py", "deploy.py", "reference_motion.py", "train.py", "evaluate.py")]
        for folder in roots:
            candidates.extend((ROOT / folder).rglob("*"))
        for path in sorted(candidates):
            rel = path.relative_to(ROOT)
            if path.is_symlink() or not path.is_file() or any(part.startswith(".") or part in {"__pycache__", "build"} for part in rel.parts):
                continue
            if path.suffix in {".pyc", ".elf", ".o"}:
                continue
            if path.suffix == ".zip" and rel.parts[:2] != ("docs", "validation"):
                continue
            z.write(path, rel)
    print("Created cad/quote_bundle.zip and school_biped_s6.zip")


if __name__ == "__main__":
    main()
