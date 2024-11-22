import bpy
import numpy as np
import random as rd
rd.seed(0)
#import parameters as params

#Parameters
xSize = 10 #Length
ySize = 10 #Width 
zSize = 20 #Height
margin = 0.04

#╔═══════════════════════╦═════════════╦════════════════════════╗#
#╠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄╌╣  Functions  ╠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╣#
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

#Bad function, doesn't work because of passive select
def generate_box2():
    verts = [
        (xSize / 2, ySize / 2, 0),
        (-xSize / 2, ySize / 2, 0),
        (-xSize / 2, -ySize / 2, 0),
        (xSize / 2, -ySize / 2, 0),
        (xSize / 2, ySize / 2, zSize),
        (-xSize / 2, ySize / 2, zSize),
        (-xSize / 2, -ySize / 2, zSize),
        (xSize / 2, -ySize / 2, zSize)
    ]
    edges = []
    faces = [
        (0, 1, 2, 3),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 4, 0)
    ]

    mesh_data = bpy.data.meshes.new("box_data")
    mesh_data.from_pydata(verts, edges, faces)

    mesh_obj = bpy.data.objects.new("Box", mesh_data)
    bpy.context.collection.objects.link(mesh_obj)

    bpy.ops.object.select_pattern(pattern="Box")
    bpy.ops.rigidbody.object_add(type='ACTIVE')
    bpy.context.object.rigid_body.type = 'PASSIVE'
    bpy.context.object.rigid_body.collision_margin = margin


def generate_particle(n, size, location, rotation = (0,0,0), type = "ACTIVE"):
    bpy.ops.mesh.primitive_cube_add(size = size, location = location, rotation = rotation)
    bpy.ops.rigidbody.object_add(type = type)
    bpy.context.object.name = "Cube.{:03d}".format(n)

#Shift the particles in a modular fashion
def periodic_shift():
    #Delete previous copies
    bpy.ops.object.select_pattern(pattern="Cube.*copy*", extend=False)
    bpy.ops.object.delete(use_global=False)
    
    bpy.ops.object.select_all(action='SELECT')
    
    for obj in bpy.context.selected_objects:

        loc = obj.location
        rot = obj.rotation_euler
        name = obj.name

        xOld, yOld, zOld = loc

        #New location for particles on the inside
        loc.x -= np.sign(xOld) * xSize / 2
        loc.y -= np.sign(yOld) * ySize / 2

        x_wall_distance = np.abs(np.abs(loc.x) - xSize / 2) - margin
        y_wall_distance = np.abs(np.abs(loc.y) - ySize / 2) - margin

        #Particles close to wall are passive
        if x_wall_distance < 1 or y_wall_distance < 1:
            obj.rigid_body.type = 'PASSIVE'
        else:
            obj.rigid_body.type = 'ACTIVE'

        #Copy wall particles to obtain periodicity
        if x_wall_distance < 1:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(loc.x + np.sign(xOld) * xSize, loc.y, loc.z), rotation=rot)
            bpy.ops.rigidbody.object_add(type="PASSIVE")
            bpy.context.object.name = obj.name + ".copyX"
        
        if  y_wall_distance < 1:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(loc.x, loc.y + np.sign(yOld) * ySize, loc.z), rotation=rot)
            bpy.ops.rigidbody.object_add(type="PASSIVE")
            bpy.context.object.name = obj.name + ".copyY"

        if x_wall_distance < 1 + margin and y_wall_distance < 1:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(loc.x + np.sign(xOld) * xSize, loc.y + np.sign(yOld) * ySize, loc.z), rotation=rot)
            bpy.ops.rigidbody.object_add(type="PASSIVE")
            bpy.context.object.name = obj.name + ".copyXY"


generate_box()

# #Clear canvas
# bpy.ops.object.select_all(action='SELECT')
# bpy.ops.object.delete(use_global=False)

# x = 2

# bpy.context.scene.frame_end = 200
# bpy.context.scene.rigidbody_world.point_cache.frame_end = 200

# generate_particle(n = 0, size = 1, location = (0, 0, 0))
# generate_particle(n = 1, size = 1, location = (1, 3, 0))
# generate_particle(n = 2, size = 1, location = (4.5, 2.5, 0))
# generate_particle(n = 3, size = 1, location = (3.5, 0, 0))

# bpy.ops.object.select_pattern(pattern="Cube")

# #Run simulation untill a cube is below z = 2
# for i in range(200):
#     leave_loop = False
#     bpy.context.scene.frame_set(frame = i)
#     for obj in bpy.context.selected_objects:
#         z = obj.matrix_world.translation[2]
#         if (z < 2):
#             leave_loop = True
#     if (leave_loop):
        # break




