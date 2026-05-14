import os
import sys
import traceback

import bpy


REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PACKAGE_PARENT = os.path.dirname(REPO_DIR)
PACKAGE_NAME = os.path.basename(REPO_DIR)

if PACKAGE_PARENT not in sys.path:
    sys.path.insert(0, PACKAGE_PARENT)


def ensure_object_mode():
    obj = bpy.context.object
    if obj and obj.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')


def cleanup_scene():
    ensure_object_mode()
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def load_addon():
    import importlib

    module = importlib.import_module(PACKAGE_NAME)
    if hasattr(module, "register"):
        module.register()
    return module


def setup_test_scene():
    cleanup_scene()

    bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0.0, 0.0, 0.0))
    obj = bpy.context.object
    obj.name = "SprytileTestPlane"

    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.region_3d.view_perspective = 'PERSP'
            area.tag_redraw()

    return obj


def main():
    try:
        load_addon()
        obj = setup_test_scene()
        print("Sprytile interactive test scene is ready.")
        print("Object:", obj.name)
        print("Mode:", obj.mode)
        print("Next checks:")
        print("1. Confirm Sprytile panel appears in the 3D View sidebar.")
        print("2. Confirm the Sprytile tools appear in the Edit Mesh toolbar.")
        print("3. Activate each tool and verify the overlay opens without errors.")
        print("4. Test preview, tile selection, and cursor interactions.")
    except Exception:
        print("Interactive setup failed:")
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
