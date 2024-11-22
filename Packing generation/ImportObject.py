import bpy
import numpy as np
import random as rd

#Start object has to be at location 0,0,0. This code is supposed to select everything but the start object,
# delete it, and then move the start object to the 0,0,0 location. It is not working yet.
'''
bpy.ops.object.select_pattern(pattern="Template")
template = bpy.context.active_object
template.location = ([0,0,0])
bpy.ops.object.select_all(action="INVERT")
bpy.ops.object.delete()
'''

#Random seed (Can be changed for different results)
rd.seed(1)

#Selects the start object, and gives it a new location and name
def import_stl():
    bpy.ops.object.select_all(action='SELECT')
    template = bpy.context.active_object
    template.name = "Template"
    template.location = ([0, 0, -5])
    
import_stl()

'''
bpy.ops.object.duplicate()
newObj = bpy.context.active_object
newObj.name = "Test"
newObj.location = ([0,0,5])
'''

#Deselects the everything (just the start object, if nothing goes wrong), so it isnt used accidentaly for the next part
bpy.ops.object.select_all(action='DESELECT')


#Sets the number of objects per section
numObj = 10

for i in range(numObj):
    #random coordinates based on the seed
    x = rd.randint(-10,10)
    y = rd.randint(-10,10)
    z = rd.randint(1,30)
    
    #Select start object, and duplicate it
    bpy.ops.object.select_pattern(pattern="Template")
    template = bpy.context.active_object
    bpy.ops.object.duplicate()
    '''
    for obj in bpy.context.scene.objects:
        if obj.name == "Template":
            bpy.select=True
            template = bpy.context.active_object
    '''
    #Give the duplicate a new location based on the random coordinates     
    newObj = bpy.context.active_object
    newObj.name = "Test"
    newObj.location = ([x,y,z])
