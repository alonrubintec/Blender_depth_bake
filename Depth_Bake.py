# Created by Alon Rubin
# To run this took copy the script to a new test file and run the script
# A new ui panel named "Depth" would be added below blender's "Create" panel

import bpy
import math

# GUI class
class Depth_Bake(bpy.types.Panel):
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


def register():
    bpy.utils.register_class(Depth_Bake)


def unregister():
    bpy.utils.unregister_class(Depth_Bake)


if __name__ == "__main__":
    register()


# Operator fix origin, position and scale
class Fix_Object(bpy.types.Operator):
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
            maxDimension = 10.0
            scaleFactor = maxDimension / max(ob.dimensions)
            ob.scale = (scaleFactor, scaleFactor, scaleFactor)
            ob.hide_render = True
        return {"FINISHED"}


bpy.utils.register_class(Fix_Object)


# Render objects
class Render_Object(bpy.types.Operator):
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
            randerpath = bpy.data.scenes[sceneKey].render.filepath
            if obj is not None:
                obj.hide_render = False

            for i in range(0, 9):
                print(i)
                obj.rotation_euler = (0, 0, math.radians(45) * i)
                bpy.data.scenes[sceneKey].render.filepath = randerpath + obj.name + "_" + str(45 * i)
                bpy.ops.render.render(write_still=True, use_viewport=True)

            obj.rotation_euler = (0, 0, 0)
            obj.hide_render = True
            bpy.data.scenes[sceneKey].render.filepath = randerpath
        return {"FINISHED"}


bpy.utils.register_class(Render_Object)