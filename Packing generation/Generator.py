import bpy
import numpy as np
import random as rd
rng = np.random.default_rng()
#import parameters as params

#Parameters
xSize = 5 #Length
ySize = 5 #Width 
zSize = 20 #Height
margin = 0.04
steady_state_margin = 0.0001
max_steady_state_iterations = 100
particle_number = 10
shift_interval = 5
size_mean = 0.6,
size_std = 0

#╔═══════════════════════╦═════════════╦════════════════════════╗#
#╠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄╌╣  Functions  ╠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╣#
#╚═══════════════════════╩═════════════╩════════════════════════╝#



def generate_box():
    #Floor
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.5))
    bpy.ops.transform.resize(value=(xSize + 2, ySize + 2, 1))
    bpy.context.object.name = "Wall.Z"

    #Wall +x
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5 * xSize + 0.5, 0, 0.5 * zSize))
    bpy.ops.transform.resize(value=(1, ySize + 2, zSize))
    bpy.context.object.name = "Wall.+X"

    #Wall -x
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.5 * xSize - 0.5, 0, 0.5 * zSize))
    bpy.ops.transform.resize(value=(1, ySize + 2, zSize))
    bpy.context.object.name = "Wall.-X"

    #Wall +y
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.5 * ySize + 0.5, 0.5 * zSize))
    bpy.ops.transform.resize(value=(ySize, 1, zSize))
    bpy.context.object.name = "Wall.+Y"

    #Wall -y
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.5 * ySize - 0.5, 0.5 * zSize))
    bpy.ops.transform.resize(value=(ySize, 1, zSize))
    bpy.context.object.name = "Wall.-Y"

    bpy.ops.object.select_pattern(pattern='Wall.*', extend=False)
    bpy.ops.object.join()
    bpy.context.object.name = "Wall"

    bpy.ops.rigidbody.object_add(type = 'PASSIVE')
    bpy.context.object.rigid_body.collision_shape = 'MESH'
    bpy.context.object.rigid_body.collision_margin = margin

def random_location(n):
    x = rng.uniform(-(xSize / 2 - 1), xSize / 2 - 1)
    y = rng.uniform(-(ySize / 2 - 1), ySize / 2 - 1)
    z = (n % shift_interval) * 2 + zSize + 1
    return (x, y, z)

def random_rotation():
    alpha = rng.random() * 2 * np.pi
    beta = np.arccos(2 * rng.random() - 1)
    gamma = rng.random() * 2 * np.pi
    return (alpha, beta, gamma)

def random_size(mu, sigma):
    size = rng.normal(mu, sigma)
    return size

def generate_particle(size, location, rotation = (0,0,0), type = "ACTIVE"):
    bpy.ops.mesh.primitive_cube_add(size = size, location = location, rotation = rotation)
    bpy.ops.rigidbody.object_add(type = type)

#Shift the particles in a modular fashion
def periodic_shift():
    #Delete previous copies
    bpy.ops.object.select_pattern(pattern="Cube.*copy*", extend=False)
    bpy.ops.object.delete(use_global=False)
    
    bpy.context.view_layer.update()    
    bpy.ops.object.select_pattern(pattern="Cube.*", extend=False)
    for obj in bpy.context.selected_objects:
        obj.rigid_body.type = 'PASSIVE'
        loc = obj.location
        rot = obj.rotation_euler
        name = obj.name 
        print(loc)
        xOld, yOld, zOld = loc

        #New location for particles on the inside
        loc.x -= np.sign(xOld) * xSize / 2
        loc.y -= np.sign(yOld) * ySize / 2
        print(loc)

        x_wall_distance = np.abs(np.abs(loc.x) - xSize / 2) - margin
        y_wall_distance = np.abs(np.abs(loc.y) - ySize / 2) - margin

        #Particles close to wall are passive
        if not (x_wall_distance < 1 or y_wall_distance < 1):
            obj.rigid_body.type = 'ACTIVE'

        #Copy wall particles to obtain periodicity
        if x_wall_distance < 1:
            generate_particle(size = 0.6, location = (loc.x + np.sign(xOld) * xSize, loc.y, loc.z), rotation = rot, type = "PASSIVE")
            bpy.context.object.name = obj.name + ".copyX"
        
        if  y_wall_distance < 1:
            generate_particle(size = 0.6, location = (loc.x, loc.y + np.sign(yOld) * ySize, loc.z), rotation = rot, type = "PASSIVE")
            bpy.context.object.name = obj.name + ".copyY"

        if x_wall_distance < 1 + margin and y_wall_distance < 1:
            generate_particle(size = 0.6, location = (loc.x + np.sign(xOld) * xSize, loc.y + np.sign(yOld) * ySize, loc.z), rotation = rot, type = "PASSIVE")
            bpy.context.object.name = obj.name + ".copyXY"

def periodic_shift2():
    #Delete previous copies
    bpy.ops.object.select_pattern(pattern="Cube.*copy*", extend=False)
    bpy.ops.object.delete(use_global=False)
    
    bpy.ops.object.select_pattern(pattern="Cube.*", extend=False)
    for obj in bpy.context.selected_objects:

        loc = obj.matrix_world.translation
        rot = obj.rotation_euler
        name = obj.name
        
        bpy.ops.object.select_pattern(pattern=name, extend=False)
        bpy.ops.object.delete(use_global=False)

        #New location for particles on the inside
        x_wall_distance = np.abs(np.abs(loc.x)) - margin
        y_wall_distance = np.abs(np.abs(loc.y)) - margin

        #Particles close to wall are passive
        if x_wall_distance < 1 or y_wall_distance < 1:
            generate_particle(size = 0.6, location = (loc.x - np.sign(loc.x) * xSize / 2, loc.y - np.sign(loc.y) * xSize / 2, loc.z), rotation = rot, type = "PASSIVE")
        else:
            generate_particle(size = 0.6, location = (loc.x - np.sign(loc.x) * xSize / 2, loc.y - np.sign(loc.y) * xSize / 2, loc.z), rotation = rot, type = "ACTIVE")
        bpy.context.object.name = name
        
        #Copy wall particles to obtain periodicity
        if x_wall_distance < 1:
            generate_particle(size = 0.6, location = (loc.x + np.sign(loc.x) * xSize / 2, loc.y - np.sign(loc.y) * xSize / 2, loc.z), rotation = rot, type = "PASSIVE")
            bpy.context.object.name = name + ".copyX"
        
        if  y_wall_distance < 1:
            generate_particle(size = 0.6, location = (loc.x - np.sign(loc.x) * xSize / 2, loc.y + np.sign(loc.y) * xSize / 2, loc.z), rotation = rot, type = "PASSIVE")
            bpy.context.object.name = name + ".copyY"

        if x_wall_distance < 1 + margin and y_wall_distance < 1:
            generate_particle(size = 0.6, location = (loc.x + np.sign(loc.x) * xSize / 2, loc.y + np.sign(loc.y) * xSize / 2, loc.z), rotation = rot, type = "PASSIVE")
            bpy.context.object.name = name + ".copyXY"
        obj.select_set(True)
        bpy.ops.object.delete(use_global=False)  

def steady_state(simulation_current_frame):

    bpy.ops.object.select_all(action='SELECT')
    size = len(bpy.context.selected_objects)
    x = [0] * size
    y = [0] * size
    z = [0] * size
    x_prev = [0] * size
    y_prev = [0] * size
    z_prev = [0] * size
    d = [0] * size

    for it in range(max_steady_state_iterations):
        i = 0
        print(simulation_current_frame)
        bpy.context.scene.frame_set(frame = simulation_current_frame)
        bpy.context.view_layer.update()
        
        for obj in bpy.context.selected_objects:
            x[i], y[i], z[i] = obj.matrix_world.translation
            d[i] = np.sqrt((x[i] - x_prev[i]) ** 2 + (y[i] - y_prev[i]) ** 2 + (z[i] - z_prev[i]) ** 2)
            x_prev[i] = np.copy(x[i])
            y_prev[i] = np.copy(y[i])
            z_prev[i] = np.copy(z[i])
            i += 1

        simulation_current_frame += 1

        print(z)
        print(d)
        if max(d) < steady_state_margin:
            break


    return simulation_current_frame

#periodic_shift2()

#Clear canvas
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

generate_box()

bpy.context.scene.frame_end = 10000
bpy.context.scene.rigidbody_world.point_cache.frame_end = 10000

simulation_current_frame = 0
for n in range(particle_number):

    rand_loc = random_location(n)
    rand_rot = random_rotation()
    rand_size = random_size(size_mean, size_std)
    generate_particle(rand_size, rand_loc, rand_rot, "ACTIVE")
    bpy.context.object.name = "Cube.{:03d}".format(n)
    
    if ((n + 1) % shift_interval == 0):
        for i in range (10):
            bpy.context.scene.frame_set(frame = simulation_current_frame)
            simulation_current_frame += 1
            bpy.context.view_layer.update()
        simulation_current_frame = steady_state(simulation_current_frame)

        periodic_shift()

bpy.context.scene.frame_set(frame = simulation_current_frame)
        






# x = 2



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




