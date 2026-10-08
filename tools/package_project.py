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
        for path in sorted(ROOT.rglob("*")):
            rel = path.relative_to(ROOT)
            if not path.is_file() or any(p in {".git", ".venv", "runs", "__pycache__", ".pytest_cache"} for p in rel.parts):
                continue
            if path.name == "school_biped_s6.zip" or path.suffix == ".pyc":
                continue
            z.write(path, rel)
    print("Created cad/quote_bundle.zip and school_biped_s6.zip")


if __name__ == "__main__":
    main()
