import bpy
import os



file_path = bpy.path.abspath("//imported_file.stl") 
print(file_path)

bpy.ops.wm.stl_import(filepath = file_path)