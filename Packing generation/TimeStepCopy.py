import bpy

Size = 10


def SectionBounds(size):
    max = size / 2
    min = -max
    return min, max

def CopySelection():
    for i in range(8):
        obj = bpy.context.active_object
        bpy.ops.object.duplicate()
        if i == 0:
            obj.location.x += Size
        if i == 1:
            obj.location.x -= Size
        if i == 2:
            obj.location.y += Size
        if i == 3:
            obj.location.y -= Size
        if i == 4:
            obj.location.x += Size
            obj.location.y += Size
        if i == 5:
            obj.location.x += Size
            obj.location.y -= Size
        if i == 6:
            obj.location.x -= Size
            obj.location.y += Size
        if i == 7:
            obj.location.x -= Size
            obj.location.y -= Size
        
def DeleteOldStep(location,max,min,object):
    if location.z < 0:
        print("Object has a negative Z-coordinate. Deleting object.")
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.delete()
        return
    
    if location.x > max or location.x < min:
        print("Object is out of bounds on the X-axis. Deleting object.")
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.delete()
        return
    
    if location.y > max or location.y < min:
        print("Object is out of bounds on the Y-axis. Deleting object.")
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.delete()
        return
    
    print("Object is within bounds.")

def TimeStep():
    min, max = SectionBounds(Size)
    bpy.ops.object.select_all(action='DESELECT')
    
    #Deletes the old step
    print("Starting deletion.")
    bpy.ops.object.select_all(action='SELECT')
    for obj in bpy.context.selected_objects:
        bpy.ops.object.select_all(action='DESELECT')
        loc = obj.location
        DeleteOldStep(loc,max,min,obj)
    print("Finished deletion.")
    
    
    #Check if the object is in the middle section, and copies it.
    #This does not yet include a check for the floor, this will need an extra if statement.
    bpy.ops.object.select_all(action='SELECT')
    print("All objects selected.")
    for obj in bpy.context.selected_objects:
        bpy.ops.object.select_all(action='DESELECT')
        loc = obj.location
        
        if loc.z < 0:
            print("Object", obj.name, "has a negative Z-coordinate. Continuing...")
            continue
        
        print("Object", obj.name, " has a positive Z-coordinate.")
        
        if loc.x > max or loc.x < min:
            print("Object", obj.name, "is out of bounds on the X-axis. Continuing...")
            continue
        
        print("Object", obj.name, " is within bounds on the X-axis.")
        
        if loc.y > max and loc.y < min:
            print("Object", obj.name, "is out of bounds on the Y-axis. Continuing...")
            continue
        
        print("Object", obj.name, " is within bounds on the Y-axis. \nStarting Copy.")
        
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        CopySelection()

print("Starting time step.")
TimeStep()
print("Time step done.")