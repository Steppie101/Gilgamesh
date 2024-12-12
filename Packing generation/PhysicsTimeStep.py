import bpy
import numpy as np
from mathutils import Euler, Vector, Matrix
import sys
from parameters import *

filepath = bpy.path.abspath("//")
sys.path.append(filepath)

rng = np.random.default_rng()

#╔═══════════════════════╦═════════════╦════════════════════════╗#
#╠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄╌╣  Functions  ╠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╣#
#╚═══════════════════════╩═════════════╩════════════════════════╝#

def RandomLocation(xSize, ySize):
    """Return a uniformly distributed location vector.
    
    The x and y coordinates are taken in their respective ranges xSize and ySize, centered at (0,0).
    The z coordinate is the spawnHeight parameter.
    """
    x = rng.uniform(-xSize / 2, xSize / 2)
    y = rng.uniform(-ySize / 2, ySize / 2)
    z = spawnHeight
    return Vector((x, y, z))

def RandomRotation():
    """Return a uniformly ditributed rotation Euler angle."""
    alpha = rng.random() * 2 * np.pi
    beta = np.arccos(2 * rng.random() - 1)
    gamma = rng.random() * 2 * np.pi
    return Euler((alpha, beta, gamma))

def RandomScale(mean = 1, std = 0):
    """Return a normally distributed scale vector.
    
    mean and std represent the mean and standard deviation of the normal distribution respectively.
    """
    size = rng.normal(mean, std)
    return Vector((size, size, size))

def GenerateParticle(location, rotation = Euler((0,0,0)), scale = Vector((1,1,1)), type = "ACTIVE", name = "None"):
    bpy.ops.mesh.primitive_cube_add(size = 1)
    obj = bpy.context.selected_objects[0]
    obj.matrix_world = Matrix.LocRotScale(location, rotation, scale)
    obj.name = name

    bpy.ops.rigidbody.object_add(type = type)
    body = bpy.context.object.rigid_body
    body.collision_shape = collisionShape
    body.friction = friction
    body.restitution = bouncyness
    body.mesh_source = 'BASE'
    body.collision_margin = collisionMargin
    body.linear_damping = linearDamping
    body.angular_damping = angularDamping

def CopySelection():    
    bpy.ops.object.select_pattern(pattern = 'Particle*', extend = False)
    for obj in bpy.context.selected_objects:

        location, rotation, scale = obj.matrix_world.decompose()
        x, y, z = location
        name = obj.name
        
        GenerateParticle(location - Vector((np.sign(x) * xSize, 0, 0)), rotation, scale, "ACTIVE", name[:-3] + ".x_")
        GenerateParticle(location - Vector((0, np.sign(y) * ySize, 0)), rotation, scale, "ACTIVE", name[:-3] + "._y") 
        GenerateParticle(location - Vector((np.sign(x) * xSize, np.sign(y) * ySize, 0)), rotation, scale, "ACTIVE", name[:-3] + ".xy")

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
        if not InsideBoundary(x, xSize) or not InsideBoundary(y, ySize):
            DeleteObject(obj)

        # Check if a MAIN particle has moved OUTSIDE the boundary, and create a new MAIN
        if name[-2:] == "__":
            if not InsideBoundary(x, xSize) and InsideBoundary(y, ySize):
                GenerateParticle(location - Vector((np.sign(x) * xSize, 0, 0)), rotation, scale, "ACTIVE", name)
                
            if InsideBoundary(x, xSize) and not InsideBoundary(y, ySize):
                GenerateParticle(location - Vector((0, np.sign(y) * ySize, 0)), rotation, scale, "ACTIVE", name)
                
            if not InsideBoundary(x, xSize) and not InsideBoundary(y, ySize):
                GenerateParticle(location - Vector((np.sign(x) * xSize, np.sign(y) * ySize, 0)), rotation, scale, "ACTIVE", name)

        # Check if a COPIED particle has moved INSIDE the boundary, and relabel it as the MAIN
        if not name[-2:] == "__":
            if InsideBoundary(x, xSize) and InsideBoundary(y, ySize):
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
    obj1.select_set(True)
    bpy.context.view_layer.objects.active = obj1
    bpy.ops.object.modifier_add(type='BOOLEAN')
    obj1.modifiers["Boolean"].operation = 'INTERSECT'
    obj1.modifiers["Boolean"].object = obj2
    obj1.modifiers["Boolean"].use_self = True
    bpy.ops.object.modifier_apply(modifier="Boolean")

def main():
    bpy.ops.object.select_all(action = 'SELECT')
    bpy.ops.object.delete(use_global=False)

    bpy.ops.mesh.primitive_plane_add(size = 2 * max(xSize, ySize) + 5)
    bpy.ops.rigidbody.object_add(type = 'PASSIVE')

    bpy.context.scene.frame_end = 10000
    bpy.context.scene.rigidbody_world.point_cache.frame_end = 10000

    n = 0
    maxIterations = numberParticles * spawnInterval
    for i in range(maxIterations):
        if (i % spawnInterval == 0):
            rand_loc = RandomLocation(xSize, ySize)
            rand_rot = RandomRotation()
            rand_scale = RandomScale(1, std = scaleDeviation)
            GenerateParticle(rand_loc, rand_rot, rand_scale, "ACTIVE", "Particle.{:03d}".format(n) + ".__")
            n += 1
        
        #print("\x1b[1;33;40m" + "|" + round(i / maxIterations * 100) * "=" + ">" + "\x1b[1;31;40m" + (100 - round(i / maxIterations * 100)) * "-" + "|" + "\x1b[0m" + str(i) + "/" + str(maxIterations))
        print(str(round((i / maxIterations) ** 3 * maxIterations / (3 * extraIterations + maxIterations) * 100)) + "%")
        ReorganizePeriodicly()
        bpy.context.scene.frame_set(frame = i)

    for i in range(maxIterations, maxIterations + extraIterations):
        print(str(round((3 * i / maxIterations - 2) * maxIterations / (3 * extraIterations + maxIterations) * 100)) + "%")
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
    

    bpy.ops.mesh.primitive_cube_add(size = 1, location = Vector((0, 0, spawnHeight / 2)), scale = Vector((xSize, ySize, spawnHeight + 1)))
    cube = bpy.data.objects["Cube"]

    Intersect(set, cube)
    DeleteObject(cube)


if __name__ == "__main__":
    main()
