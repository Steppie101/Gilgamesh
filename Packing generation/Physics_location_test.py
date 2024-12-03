import bpy
import mathutils

'''
bpy.ops.object.select_all(action='SELECT')
obj = bpy.context.selected_objects[0]

obj.rigid_body.type = 'ACTIVE'

for n in range(10):
    bpy.context.scene.frame_set(frame = n)
    (translation, rotation, scale) = obj.matrix_world.decompose()
    print(translation)
    print(rotation)
    

(translation, rotation, scale) = obj.matrix_world.decompose()
print(translation)
translation += mathutils.Vector((0, 0, 5))
print(translation)
obj.rigid_body.type = 'PASSIVE'
obj.matrix_world = mathutils.Matrix.LocRotScale(translation, rotation, scale)
'''



bpy.ops.mesh.primitive_cube_add(size = 1, location = (0, 0, 5))
bpy.ops.rigidbody.object_add()
obj = bpy.context.selected_objects[0]
(translation, rotation, scale) = obj.matrix_world.decompose()
print("matrix -1,", translation)
print("location -1,", obj.location)
obj.matrix_world = mathutils.Matrix.LocRotScale(translation + mathutils.Vector((0, 0, 1)), rotation, scale)

for n in range(10):
    bpy.context.scene.frame_set(frame = n)
    (translation, rotation, scale) = obj.matrix_world.decompose()
    print("matrix,", n, translation)
    print("location,", n, obj.location)
    obj.matrix_world = mathutils.Matrix.LocRotScale(translation + mathutils.Vector((0, 0, 1)), rotation, scale)