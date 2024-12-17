import bpy
import numpy as np
from mathutils import Euler, Vector, Matrix
import sys
import os
import time

filepath = bpy.path.abspath("//")
sys.path.append(filepath)
print("PATH:", filepath)

import parameters as params

#=======================#=============#========================#
#-----------------------:  Functions  :------------------------#
#=======================#=============#========================#

def ParameterInit():
    minInterval = 12
    if params.spawnInterval < minInterval or not isInt(params.spawnInterval):
        raise Exception("Spawn interval too small")
    
    #Possibly add different exception for uniform distribution, with 1 + params.scaleDeveation
    if params.xSize < 1 + 2 * params.scaleDeviation or params.ySize < 1 + 2 * params.scaleDeviation:
        raise Exception("Wall size too small")

    if params.scaleDeviation > 2:
        raise Exception("Too large standard deviation")  

def isInt(x):
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

    bpy.ops.rigidbody.object_add(type = type)
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

def ReorganizePeriodicly():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.visual_transform_apply()
    
    DeleteOldStep()
    CopySelection()
    
    bpy.ops.outliner.orphans_purge()

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


def main():
    startT = time.time()

    bpy.ops.object.select_all(action = 'SELECT')
    bpy.ops.object.delete(use_global=False)

    bpy.ops.mesh.primitive_plane_add(size = 2 * max(params.xSize, params.ySize) + 5)
    bpy.ops.rigidbody.object_add(type = 'PASSIVE')

    bpy.context.scene.frame_end = 10000
    bpy.context.scene.rigidbody_world.point_cache.frame_end = 10000

    n = 0
    maxIterations = params.numberParticles * params.spawnInterval
    for i in range(maxIterations):
        if (i % params.spawnInterval == 0):
            rand_loc = RandomLocation(rng, params.xSize, params.ySize)
            rand_rot = RandomRotation(rng)
            rand_scale = RandomScale(rng, deviation = params.scaleDeviation)
            GenerateParticle(rand_loc, rand_rot, rand_scale, "ACTIVE", "Particle.{:03d}".format(n) + ".__", rescaleFactor)
            n += 1
        if i:
            fraction = (i / maxIterations) ** 3 * maxIterations / (3 * params.extraIterations + maxIterations)
            print(str(round(fraction * 100)) + "%,")
        if i > 100:
            nowT = time.time()
            timeLeft = (nowT - startT) / fraction * (1 - fraction)
            #print("\x1b[1;33;40m" + "|" + round(i / maxIterations * 100) * "=" + ">" + "\x1b[1;31;40m" + (100 - round(i / maxIterations * 100)) * "-" + "|" + "\x1b[0m" + str(i) + "/" + str(maxIterations))
            print(round(timeLeft), "seconds left")
        ReorganizePeriodicly()
        bpy.context.scene.frame_set(frame = i)

    for i in range(maxIterations, maxIterations + params.extraIterations):
        fraction = (3 * i / maxIterations - 2) * maxIterations / (3 * params.extraIterations + maxIterations)
        nowT = time.time()
        timeLeft = (nowT - startT) / fraction * (1 - fraction)
        print(str(round(fraction * 100)) + "%", round(timeLeft), "seconds left")
        ReorganizePeriodicly()
        bpy.context.scene.frame_set(frame = i)
    
    ReorganizePeriodicly()
    bpy.context.scene.frame_set(frame = 0)
    
    print("\x1b[1;32;40m" + "|" + 101 * "=" + "|" + "\x1b[0m")

    plane = bpy.data.objects["Plane"]
    DeleteObject(plane)
    
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

    ExportSTL(set)


if __name__ == "__main__":
    main()
    
