
#MAKE SURE CONSOLE IS VISIBLE BEFORE RUNNING

import bpy
import numpy as np
from mathutils import Euler, Vector, Matrix
import sys
import os
import time

file_path = bpy.path.abspath("//")
sys.path.append(file_path)
print("Path:", file_path)

import parameters as params

export_path = os.path.join(file_path, params.stl_export_path)

#=======================#=============#========================#
#-----------------------:  Functions  :------------------------#
#=======================#=============#========================#

def sanity_check():
    problem_found = False
    warning = "\033[91m" + "WARNING" + "\033[00m"

    if os.path.exists(export_path):
        print(warning, "You are about to overwrite a file with your export. Export path is:\n", export_path)
        problem_found = True

    min_interval = int(np.ceil(np.sqrt(2 * (1 + 3 * params.scale_deviation) * np.sqrt(3) / 9.81) * 24))

    if params.spawn_interval < min_interval:
        print(warning, "Spawn interval too small. Should be at least", min_interval)
        problem_found = True

    if min(params.x_size, params.y_size) < (1 + 2 * params.scale_deviation) * np.sqrt(3):
        print(warning, "Small wall size")
        problem_found = True

    if params.scale_deviation * np.sqrt(3) > 1 / 2:
        print(warning, "Large standard deviation")
        problem_found = True
    
    if params.number_of_particles > 100:
        print(warning, "Number of particles is", params.number_of_particles, "the program will take a long time.")
        problem_found = True
        
    if params.particle_type == "UVSPHERE" and (params.uv_segments > 200 or params.uv_rings > 100):
        print(warning, "Number of faces in uvsphere is very large, the program will take a long time")
        problem_found = True
        
    if params.particle_type == "UVSPHERE" and 2 * params.uv_rings != params.uv_segments:
        print(warning, "Faces on uvsphere are not square, for square faces, uvSegments = 2 * uvRings")
        problem_found = True
        
    if params.particle_type == "ICOSPHERE" and params.icoSubdivisions > 6:
        print(warning, "Number of faces in icosphere is very large, the program will take a long time")
        problem_found = True
    
    if params.particle_type == "STL" and params.collision_shape in ["BOX", "SPHERE", "CYLINDER"]:
        print(warning, "Particle type is STL, while collision shape is", params.collision_shape)
        problem_found = True
    
    if params.particle_type == "CUBE" and params.collision_shape != "BOX":
        print(warning, "Particle type is BOX, while collision shape is", params.collision_shape)
        problem_found = True
                
    if params.particle_type in ["UVSPHERE", "ICOSPHERE"] and params.collision_shape != "SPHERE":
        print(warning, "Particle type is", params.particle_type, ", while collision shape is", params.collision_shape)
        problem_found = True

    if params.particle_type == "CYLINDER" and params.collision_shape != "CYLINDER":
        print(warning, "Particle type is CYLINDER, while collision shape is", params.collision_shape)
        problem_found = True
    
    if params.collision_shape == "MESH" and params.collision_margin == 0:
        print(warning, "Mesh collisionshape is used with 0 collisionMargin.")
        problem_found = True
    
    if problem_found == True:
        user_input = input("Do you wish to continue? (Y/n) ")

        if user_input.lower() in ["n", "no"]:
            raise Exception("User interruption")
        else:
            print("Continueing")

def random_location(rng, x_size, y_size, spawn_height):
    """Return a uniformly distributed location vector.
    
    The x and y coordinates are taken in their respective ranges x_size and y_size, centered at (0,0).
    The z coordinate is the spawnHeight parameter.
    """
    x = rng.uniform(-x_size / 2, x_size / 2)
    y = rng.uniform(-y_size / 2, y_size / 2)
    z = spawn_height
    return Vector((x, y, z))

def random_rotation(rng):
    """Return a uniformly ditributed rotation Euler angle."""
    alpha = rng.random() * 2 * np.pi
    beta = np.arccos(2 * rng.random() - 1)
    gamma = rng.random() * 2 * np.pi
    return Euler((alpha, beta, gamma))

def random_scale(rng, mean = 1, deviation = 0, distribution = "NORMAL"):
    """Return a normally distributed scale vector.
    
    mean and std represent the mean and standard deviation of the normal distribution respectively.
    """
    if deviation == 0:
        return mean
    
    match distribution:
        case "UNIFORM":
            size = rng.uniform(mean - np.sqrt(3) * deviation, mean + np.sqrt(3) * deviation)
        case "NORMAL":
            size = rng.normal(mean, deviation)
        case "LOGNORMAL":
            size = rng.lognormal(mean, deviation)
    return size

def generate_particle(location = Vector((0,0,0)), rotation = Euler((0,0,0)), scale = 1, name = "None", rescale_factor = 1):
    match params.particle_type:
        case "CUBE":
            bpy.ops.mesh.primitive_cube_add()
        case "UVSPHERE":
            bpy.ops.mesh.primitive_uv_sphere_add(segments = params.uv_segments, ring_count = params.uv_rings, radius = 1)
        case "ICOSPHERE":
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions = params.ico_subdivisions, radius = 1)
        case "CYLINDER":
            depth = np.sqrt((4 * params.cylinder_ratio ** 2) / (1 + 4 * params.cylinder_ratio ** 2))
            radius = np.sqrt(1 / (1 + 4 * params.cylinder_ratio ** 2))
            bpy.ops.mesh.primitive_cylinder_add(radius = radius, depth = depth)
        case "STL":
            import_path = os.path.join(file_path, params.stl_import_path)
            bpy.ops.wm.stl_import(filepath = import_path)

    obj = bpy.context.selected_objects[0]
    obj.matrix_world = Matrix.LocRotScale(location, rotation, max(min(scale * rescale_factor, (min(params.x_size , params.y_size) - 0.1) / np.sqrt(3)), 0.1) * Vector((1, 1, 1)))
    obj.name = name

    bpy.context.view_layer.objects.active = obj
    bpy.ops.rigidbody.object_add()
    body = bpy.context.object.rigid_body
    body.collision_shape = params.collision_shape
    body.friction = params.friction
    body.restitution = params.restitution
    body.mesh_source = "BASE"
    if params.collision_margin:
        body.use_margin = True
        body.collision_margin = params.collision_margin
    body.linear_damping = params.linear_damping
    body.angular_damping = params.angular_damping

def is_inside_boundary(s, size):
    return np.abs(s) < size / 2

def delete_object(name):
    bpy.context.view_layer.objects.active = select_object(name)
    bpy.ops.object.delete()

def select_object(name):
    bpy.ops.object.select_all(action = "DESELECT")
    obj = bpy.data.objects[name]
    obj.select_set(True)
    return obj

def move_particles():
    bpy.ops.object.select_pattern(pattern = "Particle*.__", extend = False)
    bpy.ops.object.select_pattern(pattern = "Plane", extend = True)
    bpy.ops.object.select_all(action = "INVERT")

    bpy.ops.rigidbody.objects_remove()

    for obj in bpy.context.selected_objects:    
        name = obj.name[:-3]
        location, rotation, scale = bpy.data.objects[name + '.__'].matrix_world.decompose()
        x, y, z = location

        #x
        if obj.name[-3:] == ".x_":
            obj.matrix_world = Matrix.LocRotScale(location - Vector((np.sign(x) * params.x_size, 0, 0)), rotation, scale)

        #y
        if obj.name[-3:] == "._y":
            obj.matrix_world = Matrix.LocRotScale(location - Vector((0, np.sign(y) * params.y_size, 0)), rotation, scale)
        
        #xy
        if obj.name[-3:] == ".xy":
            obj.matrix_world = Matrix.LocRotScale(location - Vector((np.sign(x) * params.x_size, np.sign(y) * params.y_size, 0)), rotation, scale)

    bpy.ops.rigidbody.objects_add()
    bpy.context.view_layer.objects.active = select_object("Particle.000.__")
    bpy.ops.rigidbody.object_settings_copy()

def correct_names():
    bpy.ops.object.select_pattern(pattern = "Particle*.__", extend = False)
    for obj in bpy.context.selected_objects:    
                  
        location = obj.matrix_world.decompose()[0]
        x, y, z = location
        name = obj.name[:-3]
        xobj = bpy.data.objects[name + ".x_"]
        yobj = bpy.data.objects[name + "._y"]
        xyobj = bpy.data.objects[name + ".xy"]

        # Switch names in the x direction
        if not is_inside_boundary(x, params.x_size) and is_inside_boundary(y, params.y_size):
            obj.name = "temp"
            xobj.name = name + ".__"
            obj.name = name + ".x_"
            yobj.name = "temp"
            xyobj.name = name + "._y"
            yobj.name = name + ".xy"

        # Switch names in the y direction                
        if is_inside_boundary(x, params.x_size) and not is_inside_boundary(y, params.y_size):
            obj.name = "temp"
            yobj.name = name + ".__"
            obj.name = name + "._y"
            xobj.name = "temp"
            xyobj.name = name + ".x_"
            xobj.name = name + ".xy"

        # Switch names in the x and y direction     
        if not is_inside_boundary(x, params.x_size) and not is_inside_boundary(y, params.y_size):
            obj.name = "temp"
            xyobj.name = name + ".__"
            obj.name = name + ".xy"
            xobj.name = "temp"
            yobj.name = name + ".x_"
            xobj.name = name + "._y"

def reorganize_periodicly():
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.visual_transform_apply()

    move_particles()
    correct_names()

def intersect(name1, name2):
    obj2 = select_object(name2)
    obj1 = select_object(name1)
    bpy.context.view_layer.objects.active = obj1
    bpy.ops.object.modifier_add(type = "BOOLEAN")
    obj1.modifiers["Boolean"].operation = "INTERSECT"
    obj1.modifiers["Boolean"].object = obj2
    obj1.modifiers["Boolean"].use_self = True
    bpy.ops.object.modifier_apply(modifier = "Boolean")

def export_stl(name):
    obj = select_object(name)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.stl_export(filepath = export_path, export_selected_objects = True)

#Generate and set seed
rng = np.random.default_rng()
if params.seed == "RANDOM":
    seed = rng.integers(1 << 32)
else: seed = params.seed
rng = np.random.default_rng(seed)
print("Used seed:", seed)

#Determine rescale factor, for normalization and overlap
generate_particle(name = "Test")
obj = select_object("Test")
rescale_factor = (1 - params.overlap_size)  / max(obj.dimensions)
delete_object("Test")


def main():
    sanity_check()
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.delete(use_global = False)

    #Add floor
    bpy.ops.mesh.primitive_plane_add(size = 2 * max(params.x_size, params.y_size) + 5)
    bpy.ops.rigidbody.object_add(type = "PASSIVE")

    max_iterations = params.number_of_particles * params.spawn_interval
    bpy.context.scene.frame_end = max_iterations + params.extra_iterations
    bpy.context.scene.rigidbody_world.point_cache.frame_end = max_iterations + params.extra_iterations

    #Spwan particles, and run simulation inbetween
    n = 0
    for i in range(max_iterations):
        if (i % params.spawn_interval == 0):
            rand_loc = random_location(rng, params.x_size, params.y_size, params.spawn_height)
            rand_rot = random_rotation(rng)
            rand_scale = random_scale(rng, deviation = params.scale_deviation, distribution = params.distribution)
            generate_particle(rand_loc, rand_rot, rand_scale, "Particle.{:03d}".format(n) + ".__", rescale_factor)
            generate_particle(rand_loc - Vector((np.sign(rand_loc.x) * params.x_size, 0, 0)), rand_rot, rand_scale, "Particle.{:03d}".format(n) + ".x_", rescale_factor)
            generate_particle(rand_loc - Vector((0, np.sign(rand_loc.y) * params.y_size, 0)), rand_rot, rand_scale, "Particle.{:03d}".format(n) + "._y", rescale_factor)
            generate_particle(rand_loc - Vector((np.sign(rand_loc.x) * params.x_size, np.sign(rand_loc.y) * params.y_size, 0)), rand_rot, rand_scale, "Particle.{:03d}".format(n) + ".xy", rescale_factor)
            n += 1

            fraction = (i / max_iterations) ** 2 * max_iterations / (2 * params.extra_iterations + max_iterations)
            print("Generating geometry... " + str(round(fraction * 100)) + "%", end = "\r")
        reorganize_periodicly()
        bpy.context.scene.frame_set(frame = i)

    #Extra simulation time, for settlement
    for i in range(max_iterations, max_iterations + params.extra_iterations):
        fraction = (2 * i / max_iterations - 1) * max_iterations / (2 * params.extra_iterations + max_iterations)
        print("Generating geometry... " + str(round(fraction * 100)) + "%", end = "\r")
        reorganize_periodicly()
        bpy.context.scene.frame_set(frame = i)
    
    reorganize_periodicly()
    bpy.context.scene.frame_set(frame = 0)

    #Delete floor
    delete_object("Plane")

    #Scale particles to original size
    bpy.ops.object.select_all(action = 'SELECT')
    for obj in bpy.context.selected_objects:    
        obj.scale /= 1 - params.overlap_size

    print("Geometry generated          ")
    print("Cutting geometry...", end = "\r")

    #Join mesh
    bpy.ops.object.select_all(action = 'SELECT')
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.join()
    bpy.ops.rigidbody.object_remove()
    set = bpy.context.selected_objects[0]
    set.name = "Set"

    #Cut mesh
    bpy.ops.mesh.primitive_cube_add(size = 1, location = Vector((0, 0, params.spawn_height / 2)), scale = Vector((params.x_size, params.y_size, params.spawn_height + 1)))
    intersect("Set", "Cube")
    delete_object("Cube")
    print("Geometry cut        ")

    #Export mesh
    print("Exporting STL...", end = "\r")
    export_stl("Set")
    

if __name__ == "__main__":
    main()
    