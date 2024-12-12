import bpy
import sys

file_path = bpy.path.abspath("//") 
sys.path.append(file_path)
print(file_path)

import parameters

print(parameters.testvalue)