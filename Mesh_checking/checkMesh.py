import os


commandSet = [
    "vtkUnstructuredToFoam mesh_stl.vtk",
    "checkMesh -allRegions -allGeometry -allTopology -writeSets vtk > log.checkMesh.txt",
    "touch results.foam",
]

for command in commandSet:
    if ">" not in command:
        command += " > /dev/null"

    os.system(command)
