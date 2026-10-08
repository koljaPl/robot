"""Build the 19-section handoff with the exact runnable source files embedded."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_model import physical_bodies


def vec(values, scale=1):
    return ", ".join(f"{x * scale:.3f}" for x in values)


def main():
    source = (ROOT / "docs/HANDOFF.template.md").read_text()
    basket = json.loads((ROOT / "procurement.json").read_text())
    rows = ["| Category | Exact item / supplier source | Qty | Unit € | Line € | Selection / unresolved issue |",
            "|---|---|---:|---:|---:|---|"]
    for item in basket["items"]:
        price = item["unit_price_eur"]
        label = item["product"]
        if item["url"]:
            label = f"[{label}]({item['url']})"
        rows.append(f"| {item['category']} | {label} — {item['shop']} | {item['quantity']} | "
                    + (f"{price:.2f} | {price * item['quantity']:.2f}" if price is not None else "**pending** | **pending**")
                    + f" | {item['notes']} |")
    source = source.replace("{{BOM}}", "\n".join(rows))
    spec = json.loads((ROOT / "physical_spec.json").read_text())
    mass = json.loads((ROOT / "docs/mass_properties.json").read_text())
    by_name = {b["body"]: b for b in mass["bodies"]}
    bodies = physical_bodies(spec)
    rows = ["| Body | Parent | Joint / axis | Origin in parent (mm) | Limits (°) | Mass (g) | COM local (mm) |",
            "|---|---|---|---|---|---:|---|"]
    components = ["| Body | Component (mass assigned once) | Dimensions xyz (mm) | Mass (g) | COM local xyz (mm) |",
                  "|---|---|---|---:|---|"]
    inertia = ["| Body | Ixx, Iyy, Izz, Ixy, Ixz, Iyz (kg·m²) |", "|---|---|"]
    for b in bodies:
        m = by_name[b["name"]]
        axis = vec(b["axis"]) if b["axis"] is not None else "floating"
        limits = str(b["limits_deg"]) if b["limits_deg"] else "free"
        rows.append(f"| {b['name']} | {b['parent']} | {b['joint']} / {axis} | {vec(b['position'], 1000)} | {limits} | {m['mass_kg'] * 1000:.2f} | {vec(m['com_m'], 1000)} |")
        inertia.append(f"| {b['name']} | " + ", ".join(f"{v:.7g}" for v in m["fullinertia_kg_m2"]) + " |")
        for c in b["components"]:
            components.append(f"| {b['name']} | {c['name']} | {vec(c['dimensions'], 1000)} | {c['mass'] * 1000:.2f} | {vec(c['com'], 1000)} |")
    source = source.replace("{{BODIES}}", "\n".join(rows))
    source = source.replace("{{COMPONENTS}}", "\n".join(components))
    source = source.replace("{{INERTIA}}", "\n".join(inertia))
    def include(match):
        name = match[2]
        content = (ROOT / name).read_text().rstrip()
        if match[1] == "TEXT":
            return re.sub(r"^(#+) ", r"##\1 ", content, flags=re.MULTILINE)
        lang = "xml" if name.endswith(".xml") else "json" if name.endswith(".json") else "text" if name.endswith(".txt") else "python"
        return f"```{lang}\n{content}\n```"
    source = re.sub(r"\{\{(CODE|TEXT):([^}]+)\}\}", include, source)
    if "{{" in source:
        raise ValueError("Unexpanded handoff placeholder")
    (ROOT / "docs/HANDOFF.md").write_text(source)
    print(f"Wrote docs/HANDOFF.md ({len(source.splitlines())} lines)")


if __name__ == "__main__":
    main()
