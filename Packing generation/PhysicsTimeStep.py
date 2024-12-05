import bpy
import numpy as np
import mathutils as mutils

rng = np.random.default_rng(4)
Size = 4
maxIterations = 200

bpy.context.scene.frame_end = 10000
bpy.context.scene.rigidbody_world.point_cache.frame_end = 10000

def SectionBounds(size):
    max = size / 2
    min = -max
    return min, max

def random_location(min, max):
    x = rng.uniform(min, max)
    y = rng.uniform(min, max)
    z = 25
    return mutils.Vector((x, y, z))

def random_rotation():
    alpha = rng.random() * 2 * np.pi
    beta = np.arccos(2 * rng.random() - 1)
    gamma = rng.random() * 2 * np.pi
    return mutils.Euler((alpha, beta, gamma))

def random_scale(mu, sigma):
    size = rng.normal(mu, sigma)
    return mutils.Vector((size, size, size))

def generate_particle(location, rotation = mutils.Euler((0,0,0)), scale = mutils.Vector((1,1,1)), type = "ACTIVE", name = "None"):
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.selected_objects[0]
    obj.matrix_world = mutils.Matrix.LocRotScale(location, rotation, scale)
    obj.name = name
    bpy.ops.rigidbody.object_add(type = type)
    obj.rigid_body.collision_shape = 'BOX'
    #obj.rigid_body.collision_margin = -0.01

def CopySelection(min, max):
    obj = bpy.context.active_object
    location, rotation, scale = obj.matrix_world.decompose()
    x, y, z = location
    name = obj.name
    
    generate_particle(location - mutils.Vector((np.sign(x) * Size, 0, 0)), rotation, scale, "ACTIVE", name[:-3] + ".x_")
        
    generate_particle(location - mutils.Vector((0, np.sign(y) * Size, 0)), rotation, scale, "ACTIVE", name[:-3] + "._y")
        
    generate_particle(location - mutils.Vector((np.sign(x) * Size, np.sign(y) * Size, 0)), rotation, scale, "ACTIVE", name[:-3] + ".xy")
        
def DeleteOldStep(location,max,min,object):
    if location.z < 0:
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.delete()
        return
    
    if location.x > max or location.x < min:
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.delete()
        return
        
    if location.y > max or location.y < min:
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.delete()
        return

def Rename(obj, min, max):
    location = obj.matrix_world.translation
    if obj.name == "*._?" and not min < location.x < max:
        obj.name[-2] = "x"
        bpy.data.objects[obj.name[:-2] + ""].select_set(True)
    if obj.name == "*.?_" and not min < location.y < max:
        obj.name[-1] = "y"
    if obj.name == "*.x?" and min < location.x < max:
        obj.name[-2] = "_"
    if obj.name == "*.?y" and min < location.y < max:
        obj.name[-1] = "_"

def DeleteOldStep2(obj, min, max):
    bpy.ops.object.select_all(action='DESELECT')
    location, rotation, scale = obj.matrix_world.decompose()
    x, y, z = location
    name = obj.name
    

    if z < 0:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.delete()
        return   
    
    if not min < x < max:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.delete()  
        if name[-2:] == "__":
            print("Particle outside x")
            generate_particle(location - mutils.Vector((np.sign(x) * Size, 0, 0)), rotation, scale, "ACTIVE", name)
            obj = bpy.data.objects[name]
            location, rotation, scale = obj.matrix_world.decompose()
            x, y, z = location
            bpy.ops.object.select_all(action='DESELECT')
        else:
            return 

    if not min < y < max:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.delete()
        if name[-2:] == "__":
            print("Particle outside y")
            generate_particle(location - mutils.Vector((0, np.sign(y) * Size, 0)), rotation, scale, "ACTIVE", name)
            obj = bpy.data.objects[name]
            location, rotation, scale = obj.matrix_world.decompose()
            x, y, z = location
            bpy.ops.object.select_all(action='DESELECT')
        else:
            return
        
    if min < x < max or min < y < max:
        if name[-2:] == "x_":
            print("Particle inside x")
            obj = bpy.data.objects[name[:-2] + "__"]
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.delete()
            obj = bpy.data.objects[name[:-2] + "x_"]
            obj.name = name[:-2] + "__"
        if name[-2:] == "_y":
            print("Particle inside x")
            obj = bpy.data.objects[name[:-2] + "__"]
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.delete()
            obj = bpy.data.objects[name[:-2] + "_y"]
            obj.name = name[:-2] + "__"
        if name[-2:] == "xy":
            print("Particle inside x")
            obj = bpy.data.objects[name[:-2] + "__"]
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.delete()
            obj = bpy.data.objects[name[:-2] + "xy"]
            obj.name = name[:-2] + "__"
    

def TimeStep():
    min, max = SectionBounds(Size)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.visual_transform_apply()
    

    #Deletes the old step
    bpy.ops.object.select_pattern(pattern = 'Cube*', extend = False)
    for obj in bpy.context.selected_objects:
        bpy.ops.object.select_all(action='DESELECT')
        loc = obj.matrix_world.translation
        DeleteOldStep2(obj,min,max)


    #Check if the object is in the middle section, and copies it.
    #This does not yet include a check for the floor, this will need an extra if statement.
    bpy.ops.object.select_pattern(pattern = 'Cube*', extend = False)
    for obj in bpy.context.selected_objects:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        CopySelection(min, max)
    
    bpy.ops.outliner.orphans_purge()




def main():
    bpy.ops.object.select_pattern(pattern = 'Cube*', extend = False)
    bpy.ops.object.delete(use_global=False)
    
    min, max = SectionBounds(Size)
    n = 0
    for i in range(maxIterations):
        if (i % 20 == 0):
            rand_loc = random_location(min, max)
            rand_rot = random_rotation()
            rand_scale = random_scale(1, 0)
            generate_particle(rand_loc, rand_rot, rand_scale, "ACTIVE", "Cube.{:03d}".format(n) + ".__")
            n += 1
        #print("\x1b[1;33;40m" + "|" + round(i / maxIterations * 100) * "=" + ">" + "\x1b[1;31;40m" + (100 - round(i / maxIterations * 100)) * "-" + "|" + "\x1b[0m" + str(i) + "/" + str(maxIterations))
        print(str(i) + "/" + str(maxIterations))
        TimeStep()
        bpy.context.scene.frame_set(frame = i)

    for i in range(maxIterations, maxIterations + 100):
        print(str(i) + "/" + str(maxIterations))
        TimeStep()
        bpy.context.scene.frame_set(frame = i)
    
    TimeStep()
    
    print("\x1b[1;32;40m" + "|" + 101 * "=" + "|" + "\x1b[0m")
    
        
    '''
    bpy.ops.object.select_pattern(pattern = 'Cube*', extend = False)
    for obj in bpy.context.selected_objects:
        bpy.ops.object.select_all(action='DESELECT')
        loc = obj.matrix_world.translation
        DeleteOldStep(loc,max,min,obj)
    '''

if __name__ == "__main__":
    main()
