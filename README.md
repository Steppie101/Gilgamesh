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

## Mesh Checking