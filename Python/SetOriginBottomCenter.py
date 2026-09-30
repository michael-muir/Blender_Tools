import bpy
from mathutils import Vector


def set_origin_bottom_center():
    # Save current selection
    original_selection = bpy.context.selected_objects.copy()

    if not original_selection:
        print("No objects selected.")
        return

    # Process each selected object independently
    for obj in original_selection:

        # Skip objects without mesh data
        if obj.type != 'MESH':
            continue

        # Deselect everything
        bpy.ops.object.select_all(action='DESELECT')

        # Select and activate current object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Find bottom-center in local space
        min_z = min(v.co.z for v in obj.data.vertices)
        min_x = min(v.co.x for v in obj.data.vertices)
        max_x = max(v.co.x for v in obj.data.vertices)
        max_y = max(v.co.y for v in obj.data.vertices)
        min_y = min(v.co.y for v in obj.data.vertices)

        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        bottom_center_local = Vector((
            center_x,
            center_y,
            min_z
        ))

        # Convert local position to world position
        bottom_center_world = (
            obj.matrix_world @ bottom_center_local
        )

        # Move cursor to bottom-center
        bpy.context.scene.cursor.location = bottom_center_world

        # Move origin without moving geometry
        bpy.ops.object.origin_set(
            type='ORIGIN_CURSOR',
            center='MEDIAN'
        )

    # Restore original selection
    bpy.ops.object.select_all(action='DESELECT')

    for obj in original_selection:
        obj.select_set(True)

    # Restore active object
    bpy.context.view_layer.objects.active = original_selection[0]

    print("Origins set to bottom-center.")


# Run the function
set_origin_bottom_center()
