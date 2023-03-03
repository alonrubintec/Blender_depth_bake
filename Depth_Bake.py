# Created by Alon Rubin
# This script is a Blender add-on that creates a user interface (UI) panel named "Depth" below the "Create" panel
# and contains two buttons, "Prepare Objects" and "Render Objects", which apply transformations and rotation to
# selected objects and render them in 9 angles respectively.

import bpy
import math


# GUI class
class DepthBake(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Depth"
    bl_idname = "Depth_Bake_ex1"
    bl_label = "Depth Bake Tool"

    def draw(self, context):
        scene = context.object
        layout = self.layout

        layout.label(text="Select objects then click 'Prepare Objects'")

        row1 = layout.row()
        row1.operator("object.fixobject")

        row2 = layout.row()
        layout.label(text="Render path")

        rd = context.scene.render
        layout.prop(rd, "filepath", text="")

        layout.label(text="Select objects then click 'Render Objects'")

        row3 = layout.row()
        row3.operator("object.renderobject")


# Operator fix origin, position and scale
class FixObject(bpy.types.Operator):
    bl_idname = "object.fixobject"
    bl_label = "Prepare Objects"

    def execute(self, context):
        for ob in bpy.context.selected_objects:
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            ob.location[0] = 0
            ob.location[1] = 0
            ob.location[2] = 0
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            max_dimension = 10.0
            scale_factor = max_dimension / max(ob.dimensions)
            ob.scale = (scale_factor, scale_factor, scale_factor)
            ob.hide_render = True
        return {"FINISHED"}


class RenderObject(bpy.types.Operator):
    bl_idname = "object.renderobject"
    bl_label = "Render Objects"

    def execute(self, context):
        sceneKey = bpy.data.scenes.keys()[0]
        low_objects_names = [obj.name for obj in bpy.context.selected_objects]
        for obj_name in low_objects_names:
            obj = bpy.data.objects.get(obj_name)
            if obj is not None:
                obj.hide_render = True

        for ob in low_objects_names:
            obj = bpy.data.objects.get(ob)
            rander_path = bpy.data.scenes[sceneKey].render.filepath
            if obj is not None:
                obj.hide_render = False

            for i in range(0, 9):
                print(i)
                obj.rotation_euler = (0, 0, math.radians(45) * i)
                bpy.data.scenes[sceneKey].render.filepath = rander_path + obj.name + "_" + str(45 * i)
                bpy.ops.render.render(write_still=True, use_viewport=True)

            obj.rotation_euler = (0, 0, 0)
            obj.hide_render = True
            bpy.data.scenes[sceneKey].render.filepath = rander_path
        return {"FINISHED"}


def register():
    bpy.utils.register_class(DepthBake)
    bpy.utils.register_class(FixObject)
    bpy.utils.register_class(RenderObject)


def unregister():
    bpy.utils.unregister_class(DepthBake)
    bpy.utils.unregister_class(FixObject)
    bpy.utils.unregister_class(RenderObject)


if __name__ == "__main__":
    register()