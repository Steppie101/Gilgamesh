# Gilgamesh

## Packing Generation
This tool was developed using Blender 4.3. Beware that using another version may cause the program to disfunction.
In order to run the packing generator from a command line, make sure that the current working directory is ```packing_generation```. From here the following command can be run to generate a packing:

- ```blender -b empty.blend -P generator.py```

The generator program can also be run from Blender directly:
- Open ```empty.blend``` in Blender
- Press "Toggle System Console" under the "Window" tab
- Move to the scripting workspace
- Open ```generator.py```
- Run the program

The ```parameters.py``` file can be used to access and change parameters for the packing generation. 

## Mesh Generation
This tool is developed using Python 3.12. Beware that using another version may cause the program to disfunction. 
The program does require a series of libraries that should be installed before running:

- Pygalmesh
- Meshio
- Trimesh
- Pyvista
- Datetime

When the program is run, a message asking for the filename should appear. This is the file obtained through the packing generation. The file should be of type ```.stl```. During the program two files containing the volume mesh of the solid and fluid region are created and saved as ```Geometry_Volume_Mesh +date``` and ```Fluid_Volume_Mesh +date```. Intermediate files are removed automatically.

The ```Final_version.py``` file can be used to acces and change parameters for the packing generation.

## Mesh Checking
