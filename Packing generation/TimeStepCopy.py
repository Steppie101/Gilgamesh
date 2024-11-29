import bpy

Size = 10


def SectionBounds(size):
    max = size / 2
    min = -max
    return max, min

def CopySelection():
    for i in range(4):
        obj = bpy.context.active_object
        bpy.ops.object.duplicate()
        if i == 0:
            obj.location[0] = obj.location[0] + Size
        if i == 1:
            obj.location[0] = obj.location[0] - Size
        if i == 2:
            obj.location[1] = obj.location[1] + Size
        if i == 3:
            obj.location[1] = obj.location[1] - Size
        
def DeleteOldStep(location,max,min,object):
    if location[2] < 0:
        print("Object has a negative Z-coordinate. Deleting object.")
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.delete()
    elif location[0] > max or location[0] < min:
        print("Object is out of bounds on the X-axis. Deleting object.")
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.delete()
    elif location[1] > max or location[1] < min:
        print("Object is out of bounds on the Y-axis. Deleting object.")
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.delete()
    else:
        print("Object is within bounds.")

def TimeStep():
    Max = SectionBounds(Size)[0]
    Min = SectionBounds(Size)[1]
    bpy.ops.object.select_all(action='DESELECT')
    
    #Deletes the old step
    print("Starting deletion.")
    for obj in bpy.data.objects:
        loc = obj.location
        DeleteOldStep(loc,Max,Min,obj)
    print("Finished deletion.")
    
    
    #Check if the object is in the middle section, and copies it.
    #This does not yet include a check for the floor, this will need an extra if statement.
    bpy.ops.object.select_all(action='DESELECT')
    for obj1 in bpy.data.objects:
        loc1 = obj1.location
        if loc1[2] > 0:
            print("Object has a positive Z-coordinate.")
            if loc1[0] < Max and loc1[0] > Min:
                print("Object is within bounds on the X-axis.")
                if loc1[1] < Max and loc1[1] > Min:
                    print("Object is within bounds on the Y-axis. \nStarting Copy.")
                    obj1.select_set(True)
                    bpy.context.view_layer.objects.active = obj1
                    CopySelection()

print("Starting time step.")
TimeStep()
print("Time step done.")