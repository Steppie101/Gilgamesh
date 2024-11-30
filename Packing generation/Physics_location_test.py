import bpy
import mathutils

for n in range(10):
    bpy.context.scene.frame_set(frame = n)
    bpy.ops.object.select_all(action='SELECT')
    obj = bpy.context.selected_objects[0]
    (translation, rotation, scale) = obj.matrix_world.decompose()
    print(translation)
    print(rotation)


bpy.ops.object.select_all(action='SELECT')
(translation, rotation, scale) = obj.matrix_world.decompose()
translation = mathutils.Vector((0, 0, 5))