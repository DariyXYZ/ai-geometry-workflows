import json
import math

import Rhino
from Rhino.Geometry import (
    Point3d,
    Vector3d,
    Plane,
    Box,
    Interval,
    PolylineCurve,
    Brep,
    Curve,
    TextEntity,
    Transform,
)
from Rhino.DocObjects import ObjectEnumeratorSettings
from System.Drawing import Color


doc = __rhino_doc__
tol = doc.ModelAbsoluteTolerance

RUN = "BC50_v1"

PARAMS = {
    "site": {"width": 160.0, "depth": 105.0},
    "podium": {"width": 135.0, "depth": 82.0, "floors": 3, "height": 14.4},
    "tower": {
        "floors": 50,
        "typical_floor": 4.05,
        "recessed_floor_height": 4.05,
        "upper_plate": [44.0, 50.0],
        "recessed_plate": [36.0, 42.0],
        "core": [20.0, 28.0],
    },
}


LAYERS = {
    "site": "BC50_00_site",
    "podium": "BC50_10_stylobate",
    "podium_roof": "BC50_11_exploited_roof",
    "shadow": "BC50_12_shadow_joint",
    "tower_mass": "BC50_20_tower_massing",
    "floors": "BC50_21_floor_reveals",
    "core": "BC50_22_cores",
    "facade": "BC50_30_facade_logic",
    "metric": "BC50_90_metrics",
    "archive": "TEMP_BC50_old",
}


COLORS = {
    "site": Color.FromArgb(225, 225, 220),
    "podium": Color.FromArgb(170, 172, 168),
    "podium_roof": Color.FromArgb(112, 142, 118),
    "shadow": Color.FromArgb(26, 26, 26),
    "tower_a": Color.FromArgb(126, 151, 176),
    "tower_b": Color.FromArgb(154, 139, 171),
    "glass": Color.FromArgb(110, 168, 190),
    "core": Color.FromArgb(70, 75, 80),
    "line": Color.FromArgb(30, 30, 30),
    "metric": Color.FromArgb(20, 20, 20),
}


def ensure_layer(name, color):
    index = doc.Layers.FindByFullPath(name, -1)
    if index >= 0:
        layer = doc.Layers[index]
        layer.Color = color
        layer.IsVisible = True
        doc.Layers.Modify(layer, index, True)
        return index
    layer = Rhino.DocObjects.Layer()
    layer.Name = name
    layer.Color = color
    return doc.Layers.Add(layer)


def attr(layer_name, color=None, name=None):
    attributes = Rhino.DocObjects.ObjectAttributes()
    attributes.LayerIndex = ensure_layer(layer_name, color or Color.White)
    if color:
        attributes.ObjectColor = color
        attributes.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
    if name:
        attributes.Name = name
    return attributes


def archive_old_run():
    ensure_layer(LAYERS["archive"], Color.FromArgb(120, 120, 120))
    settings = ObjectEnumeratorSettings()
    settings.HiddenObjects = True
    settings.LockedObjects = False
    settings.NormalObjects = True
    moved = 0
    for rh_obj in list(doc.Objects.GetObjectList(settings)):
        layer = doc.Layers[rh_obj.Attributes.LayerIndex]
        if layer and layer.Name.startswith("BC50_"):
            attributes = rh_obj.Attributes.Duplicate()
            attributes.LayerIndex = doc.Layers.FindByFullPath(LAYERS["archive"], -1)
            attributes.Visible = False
            doc.Objects.ModifyAttributes(rh_obj, attributes, True)
            moved += 1
    return moved


def add_box(name, layer, color, x0, y0, x1, y1, z0, z1):
    plane = Plane.WorldXY
    box = Box(
        plane,
        Interval(min(x0, x1), max(x0, x1)),
        Interval(min(y0, y1), max(y0, y1)),
        Interval(min(z0, z1), max(z0, z1)),
    )
    return doc.Objects.AddBrep(box.ToBrep(), attr(layer, color, name))


def section_points(cx, cy, w, d, rot_deg, z, chamfer=4.5):
    hw = w / 2.0
    hd = d / 2.0
    c = min(chamfer, hw * 0.35, hd * 0.35)
    pts = [
        (-hw + c, -hd),
        (hw - c, -hd),
        (hw, -hd + c),
        (hw, hd - c),
        (hw - c, hd),
        (-hw + c, hd),
        (-hw, hd - c),
        (-hw, -hd + c),
    ]
    ang = math.radians(rot_deg)
    ca = math.cos(ang)
    sa = math.sin(ang)
    out = []
    for x, y in pts:
        out.append(Point3d(cx + x * ca - y * sa, cy + x * sa + y * ca, z))
    out.append(out[0])
    return out


def add_polyline(points, name, layer, color):
    return doc.Objects.AddCurve(PolylineCurve(points), attr(layer, color, name))


def loft_tower(name, layer, color, sections):
    curves = []
    for i, s in enumerate(sections):
        curve = PolylineCurve(section_points(**s))
        curve.MakeClosed(tol)
        curves.append(curve)
    breps = Brep.CreateFromLoft(curves, Point3d.Unset, Point3d.Unset, Rhino.Geometry.LoftType.Normal, False)
    if not breps:
        raise Exception("Loft failed for " + name)
    brep = breps[0].CapPlanarHoles(tol)
    return doc.Objects.AddBrep(brep, attr(layer, color, name))


def add_floor_reveals(name, cx, cy, base_sections, levels, layer, color):
    ids = []
    for level in levels:
        z = PARAMS["podium"]["height"] + level * PARAMS["tower"]["typical_floor"]
        t = float(level) / float(PARAMS["tower"]["floors"])
        w = lerp_sections(base_sections, "w", t)
        d = lerp_sections(base_sections, "d", t)
        rot = lerp_sections(base_sections, "rot_deg", t)
        sx = lerp_sections(base_sections, "cx", t)
        sy = lerp_sections(base_sections, "cy", t)
        pts = section_points(sx, sy, w, d, rot, z, 4.2)
        ids.append(add_polyline(pts, "%s_floor_%02d" % (name, level), layer, color))
    return ids


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_sections(sections, key, t):
    samples = sorted([(s["t"], s[key]) for s in sections])
    if t <= samples[0][0]:
        return samples[0][1]
    if t >= samples[-1][0]:
        return samples[-1][1]
    for i in range(len(samples) - 1):
        t0, v0 = samples[i]
        t1, v1 = samples[i + 1]
        if t0 <= t <= t1:
            local = (t - t0) / (t1 - t0)
            return lerp(v0, v1, local)
    return samples[-1][1]


def add_tower(name, cx, cy, color, rotation_bias, drift_x):
    z0 = PARAMS["podium"]["height"]
    tf = PARAMS["tower"]["typical_floor"]
    total_floors = PARAMS["tower"]["floors"]
    z_top = z0 + total_floors * tf
    upper_w, upper_d = PARAMS["tower"]["upper_plate"]
    rec_w, rec_d = PARAMS["tower"]["recessed_plate"]

    # The first level above the podium is recessed; the main tower starts above it,
    # creating a visible overhang and dark shadow joint at the podium roof.
    add_box(
        name + "_recessed_transfer_floor",
        LAYERS["shadow"],
        COLORS["shadow"],
        cx - rec_w / 2,
        cy - rec_d / 2,
        cx + rec_w / 2,
        cy + rec_d / 2,
        z0,
        z0 + tf,
    )

    section_specs = [
        {"t": 0.02, "cx": cx, "cy": cy, "w": upper_w, "d": upper_d, "rot_deg": rotation_bias},
        {"t": 0.22, "cx": cx + drift_x * 0.30, "cy": cy + 1.5, "w": upper_w + 2.5, "d": upper_d - 1.0, "rot_deg": rotation_bias + 2.0},
        {"t": 0.46, "cx": cx + drift_x * 0.85, "cy": cy - 0.5, "w": upper_w - 1.5, "d": upper_d + 2.0, "rot_deg": rotation_bias + 5.5},
        {"t": 0.70, "cx": cx + drift_x * 0.55, "cy": cy - 2.0, "w": upper_w - 4.0, "d": upper_d - 1.0, "rot_deg": rotation_bias + 8.0},
        {"t": 0.88, "cx": cx + drift_x * 0.20, "cy": cy - 1.0, "w": upper_w - 6.0, "d": upper_d - 4.0, "rot_deg": rotation_bias + 11.0},
        {"t": 1.00, "cx": cx, "cy": cy, "w": upper_w - 8.0, "d": upper_d - 6.0, "rot_deg": rotation_bias + 13.5},
    ]
    loft_sections = []
    for spec in section_specs:
        z = z0 + max(spec["t"], 1.0 / total_floors) * total_floors * tf
        loft_sections.append(
            {
                "cx": spec["cx"],
                "cy": spec["cy"],
                "w": spec["w"],
                "d": spec["d"],
                "rot_deg": spec["rot_deg"],
                "z": z,
                "chamfer": 4.5,
            }
        )
    tower_id = loft_tower(name + "_dynamic_50f_mass", LAYERS["tower_mass"], color, loft_sections)

    # Cores are shown as internal vertical placeholders, deliberately smaller
    # than the plate and landing continuously on the podium.
    core_w, core_d = PARAMS["tower"]["core"]
    add_box(
        name + "_core_20x28m",
        LAYERS["core"],
        COLORS["core"],
        cx - core_w / 2,
        cy - core_d / 2,
        cx + core_w / 2,
        cy + core_d / 2,
        0,
        z_top,
    )

    # Floor reveals every level, stronger datum every five levels.
    floor_levels = list(range(1, total_floors + 1))
    add_floor_reveals(name, cx, cy, section_specs, floor_levels, LAYERS["floors"], COLORS["line"])
    for level in range(5, total_floors + 1, 5):
        z = z0 + level * tf + 0.04
        add_box(
            "%s_stronger_5f_datum_%02d" % (name, level),
            LAYERS["facade"],
            Color.FromArgb(45, 45, 45),
            cx - (upper_w + 2) / 2,
            cy - (upper_d + 2) / 2,
            cx + (upper_w + 2) / 2,
            cy + (upper_d + 2) / 2,
            z,
            z + 0.08,
        )

    # Exploited tower roof: parapet, plant screen, and occupied terrace inset.
    roof_z = z_top
    roof_w = upper_w - 10.0
    roof_d = upper_d - 8.0
    add_box(
        name + "_occupied_roof_deck",
        LAYERS["podium_roof"],
        COLORS["podium_roof"],
        cx - roof_w / 2,
        cy - roof_d / 2,
        cx + roof_w / 2,
        cy + roof_d / 2,
        roof_z,
        roof_z + 0.28,
    )
    add_parapet(name + "_tower_roof_parapet", cx, cy, roof_w, roof_d, roof_z, 1.2, LAYERS["podium_roof"])
    add_box(
        name + "_roof_plant_screen",
        LAYERS["facade"],
        Color.FromArgb(85, 90, 92),
        cx - 8,
        cy - 10,
        cx + 8,
        cy + 10,
        roof_z + 0.28,
        roof_z + 3.0,
    )
    return tower_id


def add_parapet(name, cx, cy, w, d, z, h, layer):
    th = 0.45
    add_box(name + "_south", layer, COLORS["line"], cx - w / 2, cy - d / 2, cx + w / 2, cy - d / 2 + th, z, z + h)
    add_box(name + "_north", layer, COLORS["line"], cx - w / 2, cy + d / 2 - th, cx + w / 2, cy + d / 2, z, z + h)
    add_box(name + "_west", layer, COLORS["line"], cx - w / 2, cy - d / 2, cx - w / 2 + th, cy + d / 2, z, z + h)
    add_box(name + "_east", layer, COLORS["line"], cx + w / 2 - th, cy - d / 2, cx + w / 2, cy + d / 2, z, z + h)


def add_text(name, text, x, y, z, size=2.4):
    entity = TextEntity()
    entity.Plane = Plane(Point3d(x, y, z), Vector3d.XAxis, Vector3d.YAxis)
    entity.PlainText = text
    entity.TextHeight = size
    return doc.Objects.AddText(entity, attr(LAYERS["metric"], COLORS["metric"], name))


def build_podium():
    w = PARAMS["podium"]["width"]
    d = PARAMS["podium"]["depth"]
    h = PARAMS["podium"]["height"]
    # U-shaped stylobate: two tower-bearing bars plus a public south connector.
    add_box("stylobate_west_bar_3f", LAYERS["podium"], COLORS["podium"], -w / 2, -d / 2, -13, d / 2, 0, h)
    add_box("stylobate_east_bar_3f", LAYERS["podium"], COLORS["podium"], 13, -d / 2, w / 2, d / 2, 0, h)
    add_box("stylobate_south_connector_3f", LAYERS["podium"], COLORS["podium"], -13, -d / 2, 13, -9, 0, h)
    add_box("stylobate_north_gallery_2f", LAYERS["podium"], COLORS["podium"], -13, 24, 13, d / 2, 0, 9.9)

    # Continuous exploited roof surfaces and paver bands.
    for x0, y0, x1, y1, label in [
        (-w / 2, -d / 2, -13, d / 2, "west"),
        (13, -d / 2, w / 2, d / 2, "east"),
        (-13, -d / 2, 13, -9, "south"),
        (-13, 24, 13, d / 2, "north_gallery"),
    ]:
        add_box("podium_roof_deck_" + label, LAYERS["podium_roof"], COLORS["podium_roof"], x0, y0, x1, y1, h, h + 0.18)

    add_parapet("stylobate_outer_parapet", 0, 0, w, d, h, 1.2, LAYERS["podium_roof"])
    # Central courtyard / roof garden bands.
    add_box("roof_garden_central_lawn", LAYERS["podium_roof"], Color.FromArgb(82, 135, 86), -16, -7, 16, 22, h + 0.2, h + 0.28)
    add_box("roof_public_promenade", LAYERS["podium_roof"], Color.FromArgb(190, 185, 170), -58, -4, 58, 4, h + 0.22, h + 0.30)
    add_box("roof_bridge_between_towers", LAYERS["podium_roof"], Color.FromArgb(160, 160, 150), -18, 5, 18, 13, h + 0.25, h + 0.40)


def build_site():
    sw = PARAMS["site"]["width"]
    sd = PARAMS["site"]["depth"]
    add_box("site_boundary_160x105m", LAYERS["site"], COLORS["site"], -sw / 2, -sd / 2, sw / 2, sd / 2, -0.08, 0)
    add_box("service_edge_south", LAYERS["site"], Color.FromArgb(150, 150, 145), -70, -55, 70, -49, 0, 0.05)
    add_box("public_plaza_north", LAYERS["site"], Color.FromArgb(198, 194, 180), -48, 43, 48, 53, 0, 0.05)


def add_metrics():
    podium = PARAMS["podium"]
    tower = PARAMS["tower"]
    z_top = podium["height"] + tower["floors"] * tower["typical_floor"]
    upper_w, upper_d = tower["upper_plate"]
    rec_w, rec_d = tower["recessed_plate"]
    core_w, core_d = tower["core"]
    tower_plate_area = upper_w * upper_d
    core_area = core_w * core_d
    net_depth_x = (upper_w - core_w) / 2.0
    net_depth_y = (upper_d - core_d) / 2.0
    gfa_towers = 2 * tower_plate_area * tower["floors"]
    podium_gfa = podium["width"] * podium["depth"] * podium["floors"] * 0.72
    total_gfa = gfa_towers + podium_gfa
    site_area = PARAMS["site"]["width"] * PARAMS["site"]["depth"]
    far = total_gfa / site_area
    lines = [
        "BC50_v1 metrics, units=m",
        "Program: 2 office towers on exploited 3F stylobate",
        "Tower floors: 50 each; typical F2F: %.2f m" % tower["typical_floor"],
        "Podium roof: %.2f m; tower roof: %.2f m" % (podium["height"], z_top),
        "Transition floor: recessed %.0f x %.0f m under %.0f x %.0f m plate" % (rec_w, rec_d, upper_w, upper_d),
        "Shadow joint / overhang: %.1f m X, %.1f m Y each side" % ((upper_w - rec_w) / 2, (upper_d - rec_d) / 2),
        "Typical plate area per tower: %.0f m2" % tower_plate_area,
        "Core placeholder: %.0f x %.0f m = %.0f m2; core ratio %.1f%%" % (core_w, core_d, core_area, core_area / tower_plate_area * 100.0),
        "Facade-to-core lease depth: %.1f m X / %.1f m Y" % (net_depth_x, net_depth_y),
        "Estimated GFA: towers %.0f m2 + podium %.0f m2 = %.0f m2" % (gfa_towers, podium_gfa, total_gfa),
        "Site area %.0f m2; early FAR %.2f" % (site_area, far),
        "Flags: office >50 m -> high-rise fire strategy required; core/lifts are placeholders.",
    ]
    y = -58
    for i, line in enumerate(lines):
        add_text("metric_%02d" % i, line, -78, y, 2.0 + i * 2.8, 2.0)


def main():
    moved = archive_old_run()
    for layer, color_key in [
        (LAYERS["site"], COLORS["site"]),
        (LAYERS["podium"], COLORS["podium"]),
        (LAYERS["podium_roof"], COLORS["podium_roof"]),
        (LAYERS["shadow"], COLORS["shadow"]),
        (LAYERS["tower_mass"], COLORS["tower_a"]),
        (LAYERS["floors"], COLORS["line"]),
        (LAYERS["core"], COLORS["core"]),
        (LAYERS["facade"], COLORS["glass"]),
        (LAYERS["metric"], COLORS["metric"]),
    ]:
        ensure_layer(layer, color_key)

    doc.ModelUnitSystem = Rhino.UnitSystem.Meters
    build_site()
    build_podium()
    add_tower("tower_west", -36.0, 6.0, COLORS["tower_a"], -6.0, 3.5)
    add_tower("tower_east", 36.0, 8.0, COLORS["tower_b"], 7.0, -4.0)
    add_metrics()

    doc.Views.Redraw()
    settings = ObjectEnumeratorSettings()
    settings.HiddenObjects = False
    settings.LockedObjects = True
    settings.NormalObjects = True
    count_visible = len(list(doc.Objects.GetObjectList(settings)))
    report = {
        "archived_old_bc50_objects": moved,
        "visible_objects": count_visible,
        "rhino_version": str(Rhino.RhinoApp.Version),
        "units": str(doc.ModelUnitSystem),
        "tower_count": 2,
        "floors_per_tower": PARAMS["tower"]["floors"],
        "podium_height_m": PARAMS["podium"]["height"],
        "tower_roof_m": PARAMS["podium"]["height"] + PARAMS["tower"]["floors"] * PARAMS["tower"]["typical_floor"],
        "status": "built",
    }
    print(json.dumps(report, sort_keys=True))


main()
