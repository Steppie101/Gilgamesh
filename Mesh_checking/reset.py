"""Clear the generated directories and files."""

import os

fileList = ["mesh_stl.vtk", "results.foam", "log.checkMesh.txt", "*.stl"]
dirList = ["constant", "VTK", "postProcessing"]

for fileName in fileList:
    os.system("rm " + fileName + " 2>/dev/null")

for dirName in dirList:
    os.system("rm -r " + dirName + " 2>/dev/null")
