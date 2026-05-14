import json
import os
import sys
import traceback

import bpy


REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PACKAGE_PARENT = os.path.dirname(REPO_DIR)
PACKAGE_NAME = os.path.basename(REPO_DIR)

if PACKAGE_PARENT not in sys.path:
    sys.path.insert(0, PACKAGE_PARENT)

result = {
    "package": PACKAGE_NAME,
    "repo_dir": REPO_DIR,
    "blender_version": bpy.app.version_string,
    "status": "init",
    "steps": [],
}


def record(step, status="ok", detail=None):
    payload = {"step": step, "status": status}
    if detail:
        payload["detail"] = detail
    result["steps"].append(payload)


try:
    import importlib

    module = importlib.import_module(PACKAGE_NAME)
    record("import_module", detail=PACKAGE_NAME)

    if hasattr(module, "register"):
        module.register()
        record("register")

    bpy.ops.mesh.primitive_plane_add()
    obj = bpy.context.object
    record("primitive_plane_add", detail=obj.name if obj else None)

    bpy.ops.object.mode_set(mode='EDIT')
    record("mode_set_edit")

    scene = bpy.context.scene
    checks = {
        "has_sprytile_data": hasattr(scene, "sprytile_data"),
        "has_sprytile_mats": hasattr(scene, "sprytile_mats"),
        "has_sprytile_list": hasattr(scene, "sprytile_list"),
        "has_sprytile_ui": hasattr(scene, "sprytile_ui"),
        "object_has_gridid": hasattr(obj, "sprytile_gridid"),
    }
    record("property_checks", detail=json.dumps(checks, sort_keys=True))

    result["status"] = "ok"
except Exception as exc:
    result["status"] = "error"
    result["error"] = str(exc)
    result["traceback"] = traceback.format_exc()
finally:
    print(json.dumps(result, indent=2, sort_keys=True))
