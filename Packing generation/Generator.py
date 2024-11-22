import bpy
import numpy as np
#import parameters as params

#Parameters
xSize = 10 #Length
ySize = 10 #Width 
zSize = 20 #Height
margin = 0.04

#╔═══════════════════════╦═════════════╦════════════════════════╗#
#╟╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╢  Functions  ╟╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╢#
#╚═══════════════════════╩═════════════╩════════════════════════╝#

def generate_box():
    #Floor
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    bpy.ops.transform.resize(value=(xSize, ySize, 0))
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.type = 'PASSIVE'
    bpy.context.object.rigid_body.collision_margin = margin

    #Wall +x
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5 * xSize, 0, 0.5 * zSize))
    bpy.ops.transform.resize(value=(0, ySize, zSize))

    #Wall -x
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.5 * xSize, 0, 0.5 * zSize))
    bpy.ops.transform.resize(value=(0, ySize, zSize))

    #Wall +y
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.5 * ySize, 0.5 * zSize))
    bpy.ops.transform.resize(value=(ySize, 0, zSize))

    #Wall -y
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.5 * ySize, 0.5 * zSize))
    bpy.ops.transform.resize(value=(ySize, 0, zSize))

def periodic_shift():
    bpy.ops.object.select_all(action='SELECT')
    
    for obj in bpy.context.selected_objects:
        xOld, yOld, zOld = obj.matrix_world.translation
        loc = obj.location
        rot = obj.matrix_world.Rotation

        loc.x -= np.sign(xOld) * xSize / 2
        loc.y -= np.sign(yOld) * ySize / 2

        x_wall_distance = np.abs(np.abs(loc.x) - xSize / 2) - margin
        y_wall_distance = np.abs(np.abs(loc.y) - ySize / 2) - margin

        if x_wall_distance < 1 or y_wall_distance < 1:
            bpy.ops.object.select_pattern(pattern = obj.name)
            bpy.context.object.rigid_body.type = 'PASSIVE'

        if x_wall_distance < 1:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(loc.x + np.sign(xOld) * xSize, loc.y, loc.z))
            bpy.ops.rigidbody.object_add()
            bpy.context.object.rigid_body.type = 'PASSIVE'
        
        if  y_wall_distance < 1:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(loc.x, loc.y + np.sign(yOld) * ySize, loc.z))
            bpy.ops.rigidbody.object_add()
            bpy.context.object.rigid_body.type = 'PASSIVE'

        if x_wall_distance < 1 + margin and y_wall_distance < 1:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(loc.x + np.sign(xOld) * xSize, loc.y + np.sign(yOld) * ySize, loc.z))
            bpy.ops.rigidbody.object_add()
            bpy.context.object.rigid_body.type = 'PASSIVE'


#Clear canvas
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)


x = 2

bpy.context.scene.frame_end = 200
bpy.context.scene.rigidbody_world.point_cache.frame_end = 200

generate_box()

bpy.ops.mesh.primitive_cube_add(size = x, location=(0, 0, 5))
bpy.ops.rigidbody.object_add()
bpy.ops.mesh.primitive_cube_add(size = x, location=(1, 3, 11))
bpy.ops.rigidbody.object_add()

bpy.ops.object.select_pattern(pattern="Cube")

#Run simulation untill a cube is below z = 2
for i in range(200):
    leave_loop = False
    bpy.context.scene.frame_set(frame = i)
    for obj in bpy.context.selected_objects:
        z = obj.matrix_world.translation[2]
        if (z < 2):
            leave_loop = True
    if (leave_loop):
        break


