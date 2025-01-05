import bpy
import numpy as np
from mathutils import Euler, Vector, Matrix
import sys
import os
import time

filepath = bpy.path.abspath("//")
sys.path.append(filepath)
print("Path:", filepath)

import parameters as params

#=======================#=============#========================#
#-----------------------:  Functions  :------------------------#
#=======================#=============#========================#

def ParameterInit():
    minInterval = 12
    if params.spawnInterval < minInterval:
        raise Exception("Spawn interval too small")
        
    if not IsInt(params.spawnInterval):
        raise Exception("Spawn interval is not an integer")
    
    #Possibly add different exception for uniform distribution, with 1 + params.scaleDeveation
    if params.xSize < 1 + 2 * params.scaleDeviation or params.ySize < 1 + 2 * params.scaleDeviation:
        raise Exception("Wall size too small")

    if params.scaleDeviation > 2:
        raise Exception("Too large standard deviation")
    
    if params.numberParticles > 100:
        while True:
            print("Number of particles is", params.numberParticles, "the program will take a long time.")
            particle_input = input("Do you wish to continue? (Y/n) ")
            if particle_input in ["Y", "Yes","yes"]:
                print("Continuing...")
                break
            elif particle_input.lower() in ["n", "no"]:
                raise Exception("User interruption")
                break
            else:
                print("Invalid input. Please enter Y or n.")
        
    if params.particleType == "UVSPHERE" and (params.uvSegments > 200 or params.uvRings > 100):
        print("Number of faces in uvsphere is very large, the program will take a long time. \n Smaller values of uvSegments and/or uvRings is advised")
        
    if params.particleType == "UVSPHERE" and 2 * params.uvRings != params.uvSegments:
        print("Faces on uvsphere are not square, for square faces, uvSegments = 2 * uvRings")
        
    if params.particleType == "ICOSPHERE" and params.icoSubdivisions > 6:
        print("Number of faces in icosphere is very large, the program will take a long time. \n A smaller value for icoSubdivisions is advised.")
    
    if params.particleType == "STL" and params.collisionShape in ["BOX", "SPHERE", "CYLINDER"]:
        while True:
            print("Particle type is STL, while collisionShape is", params.collisionShape)
            cShape_input = input("Do you wish to continue? (Y/n) ")
            if cShape_input in ["Y", "Yes","yes"]:
                print("Continuing...")
                break
            elif cShape_input.lower() in ["n", "no"]:
                raise Exception("User interruption")
                break
            else:
                print("Invalid input. Please enter Y or n.")
    
    if params.particleType == "BOX" and params.collisionShape != "BOX":
        while True:
            print("Particle type is BOX, while collisionShape is", params.collisionShape)
            cShape_input = input("Do you wish to continue? (Y/n) ")
            if cShape_input in ["Y", "Yes","yes"]:
                print("Continuing...")
                break
            elif cShape_input.lower() in ["n", "no"]:
                raise Exception("User interruption")
                break
            else:
                print("Invalid input. Please enter Y or n.")
                
    if params.particleType in ["UVSPHERE", "ICOSPHERE"] and params.collisionShape != "SPHERE":
        while True:
            print("Particle type is",params.particleType,", while collisionShape is", params.collisionShape)
            cShape_input = input("Do you wish to continue? (Y/n) ")
            if cShape_input in ["Y", "Yes","yes"]:
                print("Continuing...")
                break
            elif cShape_input.lower() in ["n", "no"]:
                raise Exception("User interruption")
                break
            else:
                print("Invalid input. Please enter Y or n.")
                
    if params.particleType == "CYLINDER" and params.collisionshape != "CYLINDER":
        while True:
            print("Particle type is CYLINDER, while collisionShape is", params.collisionShape)
            cShape_input = input("Do you wish to continue? (Y/n) ")
            if cShape_input in ["Y", "Yes","yes"]:
                print("Continuing...")
                break
            elif cShape_input.lower() in ["n", "no"]:
                raise Exception("User interruption")
                break
            else:
                print("Invalid input. Please enter Y or n.")
    
    if params.collisionShape == "MESH" and collisionMargin == 0:
        print("Mesh collisionshape is used with 0 collisionMargin.")
    
    if params.particleType == "UVSPHERE" and params.uvRadius != 1.0:
        raise Exception("Radius not normalised, change uvRadius to 1.0")
    
    if params.particleType == "ICOSPHERE" and params.icoRadius != 1.0:
        raise Exception("Radius not normalised, change icoRadius to 1.0")
        
    if params.particleType == "CYLINDER" and params.cylinderRatio != 2.0:
        raise Exception("Cylinder not normalised, change cylinderRatio to 2.0")


def IsInt(x):
    return not x % 1

def RandomLocation(rng, xSize, ySize):
    """Return a uniformly distributed location vector.
    
    The x and y coordinates are taken in their respective ranges xSize and ySize, centered at (0,0).
    The z coordinate is the spawnHeight parameter.
    """
    x = rng.uniform(-xSize / 2, xSize / 2)
    y = rng.uniform(-ySize / 2, ySize / 2)
    z = params.spawnHeight
    return Vector((x, y, z))

def RandomRotation(rng):
    """Return a uniformly ditributed rotation Euler angle."""
    alpha = rng.random() * 2 * np.pi
    beta = np.arccos(2 * rng.random() - 1)
    gamma = rng.random() * 2 * np.pi
    return Euler((alpha, beta, gamma))

def RandomScale(rng, mean = 1, deviation = 0):
    """Return a normally distributed scale vector.
    
    mean and std represent the mean and standard deviation of the normal distribution respectively.
    """
    if deviation == 0:
        return Vector((mean, mean, mean))
    
    match params.distribution:
        case "UNIFORM":
            size = rng.uniform(mean - deviation, mean + deviation)
        case "NORMAL":
            size = rng.normal(mean, deviation)
        case "LOGNORMAL":
            size = rng.lognormal(mean, deviation)
    return Vector((size, size, size))

def AddRigidBody(obj):
    bpy.ops.object.select_all(action = 'DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.rigidbody.object_add()
    body = bpy.context.object.rigid_body
    body.collision_shape = params.collisionShape
    body.friction = params.friction
    body.restitution = params.bouncyness
    body.mesh_source = 'BASE'
    if params.collisionMargin:
        body.use_margin = True
        body.collision_margin = params.collisionMargin
    body.linear_damping = params.linearDamping
    body.angular_damping = params.angularDamping

def RemoveRigidBody(obj):
    bpy.ops.object.select_all(action = 'DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.rigidbody.object_remove()


def GenerateParticle(location = Vector((0,0,0)), rotation = Euler((0,0,0)), scale = Vector((1,1,1)), type = "ACTIVE", name = "None", rescaleFactor = 1):
    match params.particleType:
        case "CUBE":
            bpy.ops.mesh.primitive_cube_add()
        case "UVSPHERE":
            bpy.ops.mesh.primitive_uv_sphere_add(segments = params.uvSegments, ring_count = params.uvRings, radius = params.uvRadius)
        case "ICOSPHERE":
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions = params.icoSubdivisions, radius = params.icoRadius)
        case "CYLINDER":
            depth = np.sqrt((params.cylinderRatio ** 2)/(1 + params.cylinderRatio ** 2))
            radius = np.sqrt(1/(1 + params.cylinderRatio ** 2))
            bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth)
        case "STL":
            importpath = os.path.join(filepath, params.stlImportPath)
            bpy.ops.wm.stl_import(filepath = importpath)

    obj = bpy.context.selected_objects[0]
    obj.matrix_world = Matrix.LocRotScale(location, rotation, scale * rescaleFactor)
    obj.name = name

    AddRigidBody(obj)

def CopySelection():    
    bpy.ops.object.select_pattern(pattern = 'Particle*', extend = False)
    for obj in bpy.context.selected_objects:

        location, rotation, scale = obj.matrix_world.decompose()
        x, y, z = location
        name = obj.name
        
        GenerateParticle(location - Vector((np.sign(x) * params.xSize, 0, 0)), rotation, scale, "ACTIVE", name[:-3] + ".x_")
        GenerateParticle(location - Vector((0, np.sign(y) * params.ySize, 0)), rotation, scale, "ACTIVE", name[:-3] + "._y") 
        GenerateParticle(location - Vector((np.sign(x) * params.xSize, np.sign(y) * params.ySize, 0)), rotation, scale, "ACTIVE", name[:-3] + ".xy")

def InsideBoundary(s, size):
    return np.abs(s) < size / 2

def DeleteObject(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.delete()

def DeleteOldStep():
    bpy.ops.object.select_pattern(pattern = 'Particle*', extend = False)
    for obj in bpy.context.selected_objects:    
          
        location, rotation, scale = obj.matrix_world.decompose()
        x, y, z = location
        name = obj.name
        
        # Delete particles outside the boundary
        if not InsideBoundary(x, params.xSize) or not InsideBoundary(y, params.ySize):
            DeleteObject(obj)

        # Check if a MAIN particle has moved OUTSIDE the boundary, and create a new MAIN
        if name[-2:] == "__":
            if not InsideBoundary(x, params.xSize) and InsideBoundary(y, params.ySize):
                GenerateParticle(location - Vector((np.sign(x) * params.xSize, 0, 0)), rotation, scale, "ACTIVE", name)
                
            if InsideBoundary(x, params.xSize) and not InsideBoundary(y, params.ySize):
                GenerateParticle(location - Vector((0, np.sign(y) * params.ySize, 0)), rotation, scale, "ACTIVE", name)
                
            if not InsideBoundary(x, params.xSize) and not InsideBoundary(y, params.ySize):
                GenerateParticle(location - Vector((np.sign(x) * params.xSize, np.sign(y) * params.ySize, 0)), rotation, scale, "ACTIVE", name)

        # Check if a COPIED particle has moved INSIDE the boundary, and relabel it as the MAIN
        if not name[-2:] == "__":
            if InsideBoundary(x, params.xSize) and InsideBoundary(y, params.ySize):
                obj = bpy.data.objects[name[:-2] + "__"]
                DeleteObject(obj)
                obj = bpy.data.objects[name]
                obj.name = name[:-2] + "__"


def CorrectNames():
    bpy.ops.object.select_pattern(pattern = 'Particle*.__', extend = False)
    for obj in bpy.context.selected_objects:    
                  
        location, rotation, scale = obj.matrix_world.decompose()
        x, y, z = location
        name = obj.name[:-3]
        xobj = bpy.data.objects[name + ".x_"]
        yobj = bpy.data.objects[name + "._y"]
        xyobj = bpy.data.objects[name + ".xy"]

        # Switch names in the x direction
        if not InsideBoundary(x, params.xSize) and InsideBoundary(y, params.ySize):
            obj.name = "temp"
            xobj.name = name + ".__"
            obj.name = name + ".x_"
            yobj.name = "temp"
            xyobj.name = name + "._y"
            yobj.name = name + ".xy"

        # Switch names in the y direction                
        if InsideBoundary(x, params.xSize) and not InsideBoundary(y, params.ySize):
            obj.name = "temp"
            yobj.name = name + ".__"
            obj.name = name + "._y"
            xobj.name = "temp"
            xyobj.name = name + ".x_"
            xobj.name = name + ".xy"

        # Switch names in the x and y direction     
        if not InsideBoundary(x, params.xSize) and not InsideBoundary(y, params.ySize):
            obj.name = "temp"
            xyobj.name = name + ".__"
            obj.name = name + ".xy"
            xobj.name = "temp"
            yobj.name = name + ".x_"
            xobj.name = name + "._y"


def MoveParticles():
    bpy.ops.object.select_pattern(pattern = 'Particle*.__', extend = False)
    bpy.ops.object.select_pattern(pattern = 'Plane', extend = True)
    bpy.ops.object.select_all(action = 'INVERT')

    bpy.ops.rigidbody.objects_remove()

    for obj in bpy.context.selected_objects:    
        name = obj.name[:-3]
        location, rotation, scale = bpy.data.objects[name + '.__'].matrix_world.decompose()
        x, y, z = location

        #x
        if obj.name[-3:] == ".x_":
            obj.matrix_world = Matrix.LocRotScale(location - Vector((np.sign(x) * params.xSize, 0, 0)), rotation, scale)

        #y
        if obj.name[-3:] == "._y":
            obj.matrix_world = Matrix.LocRotScale(location - Vector((0, np.sign(y) * params.ySize, 0)), rotation, scale)
        
        #xy
        if obj.name[-3:] == ".xy":
            obj.matrix_world = Matrix.LocRotScale(location - Vector((np.sign(x) * params.xSize, np.sign(y) * params.ySize, 0)), rotation, scale)

    bpy.ops.rigidbody.objects_add()
    copy = bpy.data.objects["Particle.000.__"]
    copy.select_set(True)
    bpy.context.view_layer.objects.active = copy
    bpy.ops.rigidbody.object_settings_copy()


def ReorganizePeriodicly():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.visual_transform_apply()

    MoveParticles()
    CorrectNames()


def Intersect(obj1, obj2):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj1
    bpy.ops.object.modifier_add(type='BOOLEAN')
    obj1.modifiers["Boolean"].operation = 'INTERSECT'
    obj1.modifiers["Boolean"].object = obj2
    obj1.modifiers["Boolean"].use_self = True
    bpy.ops.object.modifier_apply(modifier="Boolean")

def ExportSTL(obj):
    bpy.ops.object.select_all(action='DESELECT')
    exportpath = os.path.join(filepath, params.stlExportPath)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.stl_export(filepath = exportpath, export_selected_objects = True)

rng = np.random.default_rng()
if params.seed == "DEFAULT":
    seed = rng.integers(1 << 32)
else: seed = params.seed
rng = np.random.default_rng(seed)
print("Used seed:", seed)

particleSize = 1
GenerateParticle()
obj = bpy.context.selected_objects[0]
rescaleFactor = 1 / obj.dimensions.length
DeleteObject(obj)


def main():
    ParameterInit()
    bpy.ops.object.select_all(action = 'SELECT')
    bpy.ops.object.delete(use_global = False)

    bpy.ops.mesh.primitive_plane_add(size = 2 * max(params.xSize, params.ySize) + 5)
    bpy.ops.rigidbody.object_add(type = 'PASSIVE')

    maxIterations = params.numberParticles * params.spawnInterval
    bpy.context.scene.frame_end = maxIterations + params.extraIterations
    bpy.context.scene.rigidbody_world.point_cache.frame_end = 10000

    n = 0
    for i in range(maxIterations):
        if (i % params.spawnInterval == 0):
            rand_loc = RandomLocation(rng, params.xSize, params.ySize)
            rand_rot = RandomRotation(rng)
            rand_scale = RandomScale(rng, deviation = params.scaleDeviation)
            GenerateParticle(rand_loc, rand_rot, rand_scale, "ACTIVE", "Particle.{:03d}".format(n) + ".__", rescaleFactor)
            GenerateParticle(rand_loc - Vector((np.sign(rand_loc.x) * params.xSize, 0, 0)), rand_rot, rand_scale, "ACTIVE", "Particle.{:03d}".format(n) + ".x_", rescaleFactor)
            GenerateParticle(rand_loc - Vector((0, np.sign(rand_loc.y) * params.ySize, 0)), rand_rot, rand_scale, "ACTIVE", "Particle.{:03d}".format(n) + "._y", rescaleFactor)
            GenerateParticle(rand_loc - Vector((np.sign(rand_loc.x) * params.xSize, np.sign(rand_loc.y) * params.ySize, 0)), rand_rot, rand_scale, "ACTIVE", "Particle.{:03d}".format(n) + ".xy", rescaleFactor)
            n += 1
        if i:
            fraction = (i / maxIterations) ** 2 * maxIterations / (2 * params.extraIterations + maxIterations)
            #print("\x1b[1;33;40m" + "|" + round(fraction * 100) * "=" + ">" + "\x1b[1;31;40m" + (100 - round(fraction * 100)) * "-" + "|" + "\x1b[0m" + str(round(fraction * 100)) + "%", end = "\r")
            print("Generating geometry... " + str(round(fraction * 100)) + "%", end = "\r")
        ReorganizePeriodicly()
        bpy.context.scene.frame_set(frame = i)

    for i in range(maxIterations, maxIterations + params.extraIterations):
        fraction = (2 * i / maxIterations - 1) * maxIterations / (2 * params.extraIterations + maxIterations)
        #print("\x1b[1;33;40m" + "|" + round(fraction * 100) * "=" + ">" + "\x1b[1;31;40m" + (100 - round(fraction * 100)) * "-" + "|" + "\x1b[0m" + str(round(fraction * 100)) + "%", end = "\r")
        print("Generating geometry... " + str(round(fraction * 100)) + "%", end = "\r")
        ReorganizePeriodicly()
        bpy.context.scene.frame_set(frame = i)
    
    ReorganizePeriodicly()
    bpy.context.scene.frame_set(frame = 0)

    plane = bpy.data.objects["Plane"]
    DeleteObject(plane)

    bpy.ops.object.select_all(action = 'SELECT')
    for obj in bpy.context.selected_objects:    
        obj.scale += Vector((params.overlapSize, params.overlapSize, params.overlapSize))

    #print("\x1b[1;32;40m" + "|" + 101 * "=" + "|" + "\x1b[0m")
    print("Geometry generated          ")
    print("Cutting geometry...", end = "\r")

    bpy.ops.object.select_all(action = 'SELECT')
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.join()
    bpy.ops.rigidbody.object_remove()
    set = bpy.context.selected_objects[0]
    set.name = "Set"

    bpy.ops.mesh.primitive_cube_add(size = 1, location = Vector((0, 0, params.spawnHeight / 2)), scale = Vector((params.xSize, params.ySize, params.spawnHeight + 1)))
    cube = bpy.data.objects["Cube"]


    Intersect(set, cube)
    DeleteObject(cube)

    print("Geometry cut        ")

    print("Exporting STL...", end = "\r")
    ExportSTL(set)
    print("STL exported        ")
    

if __name__ == "__main__":
    main()
    
