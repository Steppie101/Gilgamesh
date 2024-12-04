import os


path = os.path.dirname(os.path.relpath(__file__))
if "C:/" in path:
    path = (path.split("C:/"))[-1]
    path = "/mnt/c/" + path

os.chdir(path)


commandSet = [
    "vtkUnstructuredToFoam mesh_stl.vtk",
    "checkMesh -allRegions -allGeometry -allTopology -writeSets vtk > log.checkMesh.txt",
    "touch results.foam",
]

for command in commandSet:
    if ">" not in command:
        command += " > /dev/null"

    os.system(command)
