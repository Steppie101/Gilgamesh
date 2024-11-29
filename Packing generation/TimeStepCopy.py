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
        

def TimeStep():
    Max = SectionBounds(Size)[0]
    Min = SectionBounds(Size)[1]
    bpy.ops.object.select_all(action='DESELECT')
    #print("All objects selected.")
    for obj in bpy.data.objects:
        loc = obj.location
        if loc[2] > 0:
            print("Object has a positive Z-coordinate.")
            if loc[0] < Max and loc[0] > Min:
                print("Object is within bounds on the X-axis.")
                if loc[1] < Max and loc[1] > Min:
                    print("Object is within bounds on the Y-axis. \n Starting Copy.")
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                    CopySelection()
print("Starting time step.")
TimeStep()
print("Time step done.")