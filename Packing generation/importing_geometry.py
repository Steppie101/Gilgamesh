import bpy
import os

file_path = r"C:\Users\Lucas Venemans\Documents\GitHub\Gilgamesh\Packing generation\imported_file.blend"
inner_path = "Object"
object_name = "Suzanne"

bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name),directory=os.path.join(file_path, inner_path),filename=object_name)

