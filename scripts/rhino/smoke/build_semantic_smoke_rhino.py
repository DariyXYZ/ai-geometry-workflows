from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


# Legacy Aurox smoke demonstrator. New Rhino work should use standard RhinoMCP first.
CLIENT = r"C:\Users\dariy.n\.codex\skills\rhino-aurox-modeling\scripts\rhino_aurox_client.py"
LAYER = "SEMANTIC_OBJ_SMOKE"
GRID_LAYER = "SEMANTIC_OBJ_SMOKE_GUIDES"


def call(command: str, params: dict[str, Any]) -> dict[str, Any]:
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    try:
        json.dump(params, tmp)
        tmp.close()
        result = subprocess.run(
            [sys.executable, CLIENT, "call", command, "--params-file", tmp.name],
            capture_output=True,
            text=True,
            timeout=60,
        )
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass
    if result.returncode != 0:
        raise RuntimeError("FAIL %s: %s" % (command, result.stderr[-500:]))
    return json.loads(result.stdout or "{}")


def ensure_layer(name: str, color: tuple[int, int, int]) -> None:
    try:
        call("add_layer", {"name": name, "color": list(color)})
    except Exception:
        pass


def safe_delete(object_id: str) -> None:
    try:
        call("delete_object", {"object_id": object_id})
    except Exception:
        pass


def cleanup_layer(name: str) -> None:
    try:
        ids = call("filter_objects", {"layer": name}).get("ids", [])
        for object_id in ids:
            safe_delete(object_id)
    except Exception:
        pass


def set_props(object_id: str, layer: str, name: str, color: tuple[int, int, int]) -> None:
    call("set_object_layer", {"object_id": object_id, "layer": layer})
    call("set_object_name", {"object_id": object_id, "name": name})
    call("set_object_color", {"object_id": object_id, "color": list(color)})


def bbox_size(bbox: dict[str, list[float]]) -> list[float]:
    return [float(bbox["max"][i]) - float(bbox["min"][i]) for i in range(3)]


def add_box_from_bbox(part: dict[str, Any], color: tuple[int, int, int]) -> str:
    bbox = part["bbox"]
    sx, sy, sz = bbox_size(bbox)
    result = call("add_box", {"corner": bbox["min"], "x": sx, "y": sy, "z": sz})
    object_id = result["id"]
    set_props(object_id, LAYER, part["id"], color)
    return object_id


def ellipse_section(bbox: dict[str, list[float]], z: float, segments: int = 48) -> list[list[float]]:
    cx = (float(bbox["min"][0]) + float(bbox["max"][0])) / 2.0
    cy = (float(bbox["min"][1]) + float(bbox["max"][1])) / 2.0
    rx = (float(bbox["max"][0]) - float(bbox["min"][0])) / 2.0
    ry = (float(bbox["max"][1]) - float(bbox["min"][1])) / 2.0
    points: list[list[float]] = []
    for i in range(segments + 1):
        t = math.tau * i / segments
        points.append([cx + math.cos(t) * rx, cy + math.sin(t) * ry, z])
    return points


def add_oval_from_bbox(part: dict[str, Any], color: tuple[int, int, int]) -> str:
    bbox = part["bbox"]
    bottom = ellipse_section(bbox, float(bbox["min"][2]))
    top = ellipse_section(bbox, float(bbox["max"][2]))
    cids = []
    for points in (bottom, top):
        cids.append(call("add_polyline", {"points": points})["id"])
    result = call("add_loft", {"ids": cids})
    object_id = result["ids"][0]
    for cid in cids:
        safe_delete(cid)
    set_props(object_id, LAYER, part["id"], color)
    return object_id


def add_facade_grid(part: dict[str, Any]) -> list[str]:
    bbox = part["bbox"]
    params = part.get("params", {})
    floor_count = int(params.get("floor_count", 24))
    bay_count_x = int(params.get("bay_count_x", 7))
    x0, y0, z0 = [float(v) for v in bbox["min"]]
    x1, _y1, z1 = [float(v) for v in bbox["max"]]
    created: list[str] = []
    y = y0 - 0.08
    for i in range(floor_count + 1):
        z = z0 + (z1 - z0) * i / floor_count
        cid = call("add_polyline", {"points": [[x0, y, z], [x1, y, z]]})["id"]
        set_props(cid, GRID_LAYER, "%s_floor_%02d" % (part["id"], i), (80, 120, 210))
        created.append(cid)
    for i in range(bay_count_x + 1):
        x = x0 + (x1 - x0) * i / bay_count_x
        cid = call("add_polyline", {"points": [[x, y, z0], [x, y, z1]]})["id"]
        set_props(cid, GRID_LAYER, "%s_bay_%02d" % (part["id"], i), (80, 120, 210))
        created.append(cid)
    return created


def build(report_path: Path) -> None:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    ensure_layer(LAYER, (170, 185, 200))
    ensure_layer(GRID_LAYER, (80, 120, 210))
    cleanup_layer(LAYER)
    cleanup_layer(GRID_LAYER)

    solids = 0
    guides = 0
    for part in report.get("parts", []):
        if not part.get("bbox"):
            continue
        semantic = str(part.get("semantic", "")).lower()
        name = str(part.get("name", "")).lower()
        if part.get("hidden") or "grid" in semantic or "grid" in name:
            guides += len(add_facade_grid(part))
        elif "oval" in semantic or "oval" in name:
            add_oval_from_bbox(part, (170, 185, 200))
            solids += 1
        else:
            add_box_from_bbox(part, (190, 178, 150))
            solids += 1

    print("semantic smoke built: solids=%d guides=%d" % (solids, guides))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Rhino preview from semantic_parts.json.")
    parser.add_argument("semantic_parts")
    args = parser.parse_args()
    build(Path(args.semantic_parts).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
