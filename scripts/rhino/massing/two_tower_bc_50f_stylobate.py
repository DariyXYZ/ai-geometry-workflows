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
    CurveOffsetCornerStyle,
    AreaMassProperties,
    TextEntity,
    Transform,
)
from Rhino.DocObjects import ObjectEnumeratorSettings
from System.Drawing import Color


doc = __rhino_doc__
tol = doc.ModelAbsoluteTolerance

RUN = "BC50_v7"
VISUAL_LIFT_M = 0.001

PARAMS = {
    "site": {"width": 160.0, "depth": 105.0},
    "podium": {"width": 135.0, "depth": 82.0, "floors": 3, "height": 14.4},
    "tower": {
        "floors": 50,
        "typical_floor": 4.05,
        "recessed_floor_height": 4.05,
        "upper_plate": [44.0, 50.0],
        "recessed_plate": [36.0, 42.0],
        "core": [18.0, 24.0],
        "roof_core_overrun": [12.0, 18.0, 4.2],
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
    "datum": "BC50_30_datum_contours",
    "roof_equipment": "BC50_31_roof_core_overruns",
    "metric": "BC50_90_metrics",
}


COLORS = {
    "site": Color.FromArgb(225, 225, 220),
    "podium": Color.FromArgb(170, 172, 168),
    "podium_roof": Color.FromArgb(112, 142, 118),
    "tower_roof": Color.FromArgb(172, 172, 164),
    "shadow": Color.FromArgb(26, 26, 26),
    "tower_a": Color.FromArgb(126, 151, 176),
    "tower_b": Color.FromArgb(154, 139, 171),
    "glass": Color.FromArgb(110, 168, 190),
    "core": Color.FromArgb(70, 75, 80),
    "core_headhouse": Color.FromArgb(92, 96, 98),
    "equipment": Color.FromArgb(118, 122, 124),
    "line": Color.FromArgb(30, 30, 30),
    "datum": Color.FromArgb(36, 36, 36),
    "metric": Color.FromArgb(20, 20, 20),
}


MATERIALS = {
    "glass_blue": {
        "name": "BC50_translucent_blue_glass",
        "color": Color.FromArgb(118, 156, 218),
        "transparency": 0.42,
    },
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


def ensure_material(material_key):
    material_data = MATERIALS[material_key]
    index = doc.Materials.Find(material_data["name"], True)
    if index >= 0:
        material = doc.Materials[index]
    else:
        material = Rhino.DocObjects.Material()
        material.Name = material_data["name"]
        index = doc.Materials.Add(material)
        material = doc.Materials[index]
    material.DiffuseColor = material_data["color"]
    material.Transparency = material_data["transparency"]
    doc.Materials.Modify(material, index, True)
    return index


def attr(layer_name, color=None, name=None, material_key=None):
    attributes = Rhino.DocObjects.ObjectAttributes()
    attributes.LayerIndex = ensure_layer(layer_name, color or Color.White)
    if color:
        attributes.ObjectColor = color
        attributes.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
    if material_key:
        attributes.MaterialIndex = ensure_material(material_key)
        attributes.MaterialSource = Rhino.DocObjects.ObjectMaterialSource.MaterialFromObject
    if name:
        attributes.Name = name
    return attributes


def cleanup_previous_generated():
    settings = ObjectEnumeratorSettings()
    settings.HiddenObjects = True
    settings.LockedObjects = True
    settings.NormalObjects = True
    deleted = 0
    for rh_obj in list(doc.Objects.GetObjectList(settings)):
        layer = doc.Layers[rh_obj.Attributes.LayerIndex]
        layer_name = layer.Name if layer else ""
        if layer_name.startswith("BC50_") or layer_name.startswith("TEMP_BC50"):
            attributes = rh_obj.Attributes.Duplicate()
            attributes.Locked = False
            attributes.Visible = True
            doc.Objects.ModifyAttributes(rh_obj, attributes, True)
            if doc.Objects.Delete(rh_obj.Id, True):
                deleted += 1

    target_layers = set(LAYERS.values())
    remaining_layer_indices = set()
    check_settings = ObjectEnumeratorSettings()
    check_settings.HiddenObjects = True
    check_settings.LockedObjects = True
    check_settings.NormalObjects = True
    for rh_obj in doc.Objects.GetObjectList(check_settings):
        remaining_layer_indices.add(rh_obj.Attributes.LayerIndex)
    for i in reversed(range(doc.Layers.Count)):
        layer = doc.Layers[i]
        name = layer.Name or ""
        if (name.startswith("BC50_") or name.startswith("TEMP_BC50")) and name not in target_layers:
            if i not in remaining_layer_indices:
                doc.Layers.Delete(i, True)
    return deleted


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


def curve_area(curve):
    amp = AreaMassProperties.Compute(curve)
    if not amp:
        return 0.0
    return abs(amp.Area)


def closed_curve(points):
    pts = list(points)
    if pts[0].DistanceTo(pts[-1]) > tol:
        pts.append(pts[0])
    curve = PolylineCurve(pts)
    curve.MakeClosed(tol)
    return curve


def offset_curve_by_area(curve, distance, prefer):
    candidates = []
    for signed_distance in [distance, -distance]:
        offsets = curve.Offset(Plane.WorldXY, signed_distance, tol, CurveOffsetCornerStyle.Sharp)
        if not offsets:
            continue
        for candidate in offsets:
            if candidate and candidate.IsClosed:
                candidates.append(candidate)
    if not candidates:
        raise Exception("Offset failed for curve")
    base_area = curve_area(curve)
    if prefer == "smaller":
        smaller = [c for c in candidates if curve_area(c) < base_area]
        return sorted(smaller or candidates, key=curve_area)[0]
    larger = [c for c in candidates if curve_area(c) > base_area]
    return sorted(larger or candidates, key=curve_area, reverse=True)[0]


def add_planar_region(name, curves, layer, color):
    breps = Brep.CreatePlanarBreps(curves, tol)
    if not breps:
        raise Exception("Planar region failed for " + name)
    ids = []
    for i, brep in enumerate(breps):
        ids.append(doc.Objects.AddBrep(brep, attr(layer, color, "%s_%02d" % (name, i))))
    return ids


def translated_curve(curve, dz):
    duplicate = curve.DuplicateCurve()
    duplicate.Transform(Transform.Translation(0, 0, dz))
    return duplicate


def add_vertical_face_between_curves(name, curve_a, curve_b, layer, color):
    breps = Brep.CreateFromLoft([curve_a, curve_b], Point3d.Unset, Point3d.Unset, Rhino.Geometry.LoftType.Normal, False)
    if not breps:
        raise Exception("Vertical face loft failed for " + name)
    return doc.Objects.AddBrep(breps[0], attr(layer, color, name))


def add_parapet_from_contour(name, edge_curve, z, height, thickness, layer, side):
    # Build parapets as a ring between the source contour and an offset contour.
    # This keeps roof edge geometry tied to the actual outline of the building.
    prefer = "smaller" if side == "inside" else "larger"
    offset = offset_curve_by_area(edge_curve, thickness, prefer)
    edge_top = translated_curve(edge_curve, height)
    offset_top = translated_curve(offset, height)
    add_vertical_face_between_curves(name + "_outer_face", edge_curve, edge_top, layer, COLORS["line"])
    add_vertical_face_between_curves(name + "_inner_face", offset, offset_top, layer, COLORS["line"])
    return add_planar_region(name + "_top_cap", [edge_top, offset_top], layer, COLORS["line"])


def add_inset_surface_from_contour(name, edge_curve, inset, layer, color, prefer="smaller"):
    inset_curve = offset_curve_by_area(edge_curve, inset, prefer)
    return add_planar_region(name, [inset_curve], layer, color)


def add_roof_core_overrun(name, cx, cy, roof_z):
    core_w, core_d = PARAMS["tower"]["core"]
    head_w, head_d, head_h = PARAMS["tower"]["roof_core_overrun"]
    add_box(
        name + "_core_continues_to_roof",
        LAYERS["roof_equipment"],
        COLORS["core_headhouse"],
        cx - head_w / 2,
        cy - head_d / 2,
        cx + head_w / 2,
        cy + head_d / 2,
        roof_z,
        roof_z + head_h,
    )
    add_box(
        name + "_roof_access_lobby",
        LAYERS["roof_equipment"],
        COLORS["equipment"],
        cx - head_w / 2 + 1.2,
        cy + head_d / 2,
        cx + head_w / 2 - 1.2,
        cy + head_d / 2 + 4.0,
        roof_z,
        roof_z + 2.7,
    )
    add_box(
        name + "_low_mep_pad_west",
        LAYERS["roof_equipment"],
        COLORS["equipment"],
        cx - core_w / 2 - 5.5,
        cy - 5.0,
        cx - core_w / 2 - 1.5,
        cy + 5.0,
        roof_z + 0.15,
        roof_z + 1.1,
    )
    add_box(
        name + "_low_mep_pad_east",
        LAYERS["roof_equipment"],
        COLORS["equipment"],
        cx + core_w / 2 + 1.5,
        cy - 5.0,
        cx + core_w / 2 + 5.5,
        cy + 5.0,
        roof_z + 0.15,
        roof_z + 1.1,
    )


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
    return doc.Objects.AddBrep(brep, attr(layer, color, name, "glass_blue"))


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


def add_datum_contours(name, base_sections, levels):
    ids = []
    for level in levels:
        z = PARAMS["podium"]["height"] + level * PARAMS["tower"]["typical_floor"] + 0.06
        t = float(level) / float(PARAMS["tower"]["floors"])
        pts = section_points(
            lerp_sections(base_sections, "cx", t),
            lerp_sections(base_sections, "cy", t),
            lerp_sections(base_sections, "w", t),
            lerp_sections(base_sections, "d", t),
            lerp_sections(base_sections, "rot_deg", t),
            z,
            4.2,
        )
        ids.append(add_polyline(pts, "%s_5f_datum_contour_%02d" % (name, level), LAYERS["datum"], COLORS["datum"]))
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
        name + "_core_18x24m_placeholder",
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
    add_datum_contours(name, section_specs, range(5, total_floors + 1, 5))

    # Realistic tower roof: one outer parapet from the roof contour, flat
    # membrane, and a straight core overrun/headhouse. No inner parapet ring.
    roof_z = z_top
    top_pts = section_points(cx, cy, upper_w - 8.0, upper_d - 6.0, rotation_bias + 13.5, roof_z + VISUAL_LIFT_M, 4.5)
    roof_edge = closed_curve(top_pts)
    add_planar_region(name + "_roof_membrane_from_contour", [roof_edge], LAYERS["podium_roof"], COLORS["tower_roof"])
    add_parapet_from_contour(name + "_tower_roof_parapet", roof_edge, roof_z, 1.2, 0.75, LAYERS["podium_roof"], "inside")
    add_roof_core_overrun(name, cx, cy, roof_z)
    return tower_id


def add_text(name, text, x, y, z, size=2.4):
    entity = TextEntity()
    entity.Plane = Plane(Point3d(x, y, z), Vector3d.XAxis, Vector3d.ZAxis)
    entity.PlainText = text
    entity.TextHeight = size
    return doc.Objects.AddText(entity, attr(LAYERS["metric"], COLORS["metric"], name))


def build_podium():
    w = PARAMS["podium"]["width"]
    d = PARAMS["podium"]["depth"]
    h = PARAMS["podium"]["height"]
    courtyard = {
        "x0": -13.0,
        "y0": -9.0,
        "x1": 13.0,
        "y1": 24.0,
    }
    # U-shaped stylobate: two tower-bearing bars plus a public south connector.
    add_box("stylobate_west_bar_3f", LAYERS["podium"], COLORS["podium"], -w / 2, -d / 2, -13, d / 2, 0, h)
    add_box("stylobate_east_bar_3f", LAYERS["podium"], COLORS["podium"], 13, -d / 2, w / 2, d / 2, 0, h)
    add_box("stylobate_south_connector_3f", LAYERS["podium"], COLORS["podium"], -13, -d / 2, 13, -9, 0, h)
    add_box("stylobate_north_gallery_2f", LAYERS["podium"], COLORS["podium"], -13, 24, 13, d / 2, 0, 9.9)

    # The exploited roof is one contour region with a courtyard void. Parapets
    # are tied to the same outer and inner contours through offsets.
    outer = closed_curve(
        [
            Point3d(-w / 2, -d / 2, h + 0.22 + VISUAL_LIFT_M),
            Point3d(w / 2, -d / 2, h + 0.22 + VISUAL_LIFT_M),
            Point3d(w / 2, d / 2, h + 0.22 + VISUAL_LIFT_M),
            Point3d(-w / 2, d / 2, h + 0.22 + VISUAL_LIFT_M),
        ]
    )
    void = closed_curve(
        [
            Point3d(courtyard["x0"], courtyard["y0"], h + 0.22 + VISUAL_LIFT_M),
            Point3d(courtyard["x0"], courtyard["y1"], h + 0.22 + VISUAL_LIFT_M),
            Point3d(courtyard["x1"], courtyard["y1"], h + 0.22 + VISUAL_LIFT_M),
            Point3d(courtyard["x1"], courtyard["y0"], h + 0.22 + VISUAL_LIFT_M),
        ]
    )
    add_planar_region("podium_roof_deck_outer_minus_courtyard", [outer, void], LAYERS["podium_roof"], COLORS["podium_roof"])
    add_parapet_from_contour("stylobate_outer_parapet_from_outer_contour", outer, h + 0.22, 1.2, 0.75, LAYERS["podium_roof"], "inside")
    add_parapet_from_contour("stylobate_courtyard_parapet_from_void_contour", void, h + 0.22, 1.2, 0.65, LAYERS["podium_roof"], "outside")

    # Green and paving are derived from courtyard/roof contours so they cannot
    # drift across the parapet or miss the opening.
    green_edge = offset_curve_by_area(void, 1.6, "smaller")
    green_target_z = 0.12 + VISUAL_LIFT_M
    green_edge.Transform(Transform.Translation(0, 0, green_target_z - (h + 0.22 + VISUAL_LIFT_M)))
    add_planar_region("sunken_courtyard_green_from_void_offset", [green_edge], LAYERS["podium_roof"], Color.FromArgb(82, 135, 86))
    promenade_outer = offset_curve_by_area(outer, 4.2, "smaller")
    promenade_inner = offset_curve_by_area(outer, 9.0, "smaller")
    add_planar_region("roof_promenade_ring_from_outer_offsets", [promenade_outer, promenade_inner], LAYERS["podium_roof"], Color.FromArgb(190, 185, 170))
    bridge_edge = closed_curve(
        [
            Point3d(courtyard["x0"] - 5.0, 4.0, h + 0.34 + VISUAL_LIFT_M),
            Point3d(courtyard["x1"] + 5.0, 4.0, h + 0.34 + VISUAL_LIFT_M),
            Point3d(courtyard["x1"] + 5.0, 13.0, h + 0.34 + VISUAL_LIFT_M),
            Point3d(courtyard["x0"] - 5.0, 13.0, h + 0.34 + VISUAL_LIFT_M),
        ]
    )
    add_planar_region("roof_bridge_from_courtyard_span_contour", [bridge_edge], LAYERS["podium_roof"], Color.FromArgb(160, 160, 150))
    # Bridge guardrails run along both sides of the crossing, so the bridge is
    # read as a usable path over the sunken courtyard instead of a plate cutting
    # through the courtyard parapet.
    rail_z0 = h + 0.34
    rail_z1 = rail_z0 + 1.2
    add_box("roof_bridge_south_guardrail", LAYERS["podium_roof"], COLORS["line"], courtyard["x0"] - 5.0, 3.55, courtyard["x1"] + 5.0, 4.0, rail_z0, rail_z1)
    add_box("roof_bridge_north_guardrail", LAYERS["podium_roof"], COLORS["line"], courtyard["x0"] - 5.0, 13.0, courtyard["x1"] + 5.0, 13.45, rail_z0, rail_z1)


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
        "BC50_v7 | units=m",
        "2 office towers on 3F exploited stylobate",
        "Tower floors: 50 each | F2F %.2f m" % tower["typical_floor"],
        "Podium roof %.1f m | tower roof %.1f m" % (podium["height"], z_top),
        "Transfer floor: %.0fx%.0f m under %.0fx%.0f m plate" % (rec_w, rec_d, upper_w, upper_d),
        "Shadow joint overhang: %.1f m X / %.1f m Y" % ((upper_w - rec_w) / 2, (upper_d - rec_d) / 2),
        "Typical plate per tower: %.0f m2" % tower_plate_area,
        "Core placeholder: %.0fx%.0f = %.0f m2 | %.1f%%" % (core_w, core_d, core_area, core_area / tower_plate_area * 100.0),
        "Lease depth: %.1f m X / %.1f m Y" % (net_depth_x, net_depth_y),
        "Roof: outer parapet + straight core overrun",
        "GFA est.: towers %.0f + podium %.0f = %.0f m2" % (gfa_towers, podium_gfa, total_gfa),
        "Site %.0f m2 | early FAR %.2f" % (site_area, far),
        "Flag: >50 m office high-rise strategy required",
    ]
    add_box(
        "metric_board_vertical_backplate",
        LAYERS["metric"],
        Color.FromArgb(235, 236, 228),
        -81.0,
        -66.4,
        36.0,
        -66.1,
        1.0,
        37.0,
    )
    x = -79.0
    y = -65.95
    z_top = 34.0
    line_step = 2.45
    for i, line in enumerate(lines):
        add_text("metric_%02d" % i, line, x, y, z_top - i * line_step, 1.55)


def main():
    deleted = cleanup_previous_generated()
    for layer, color_key in [
        (LAYERS["site"], COLORS["site"]),
        (LAYERS["podium"], COLORS["podium"]),
        (LAYERS["podium_roof"], COLORS["podium_roof"]),
        (LAYERS["shadow"], COLORS["shadow"]),
        (LAYERS["tower_mass"], COLORS["tower_a"]),
        (LAYERS["floors"], COLORS["line"]),
        (LAYERS["core"], COLORS["core"]),
        (LAYERS["datum"], COLORS["datum"]),
        (LAYERS["roof_equipment"], COLORS["equipment"]),
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
        "deleted_old_bc50_objects": deleted,
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
