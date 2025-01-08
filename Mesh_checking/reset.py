"""Clear the generated directories and files."""

from functions import runCommand

fileList = ["mesh_stl.vtk", "results.foam", "log.*", "*.stl"]
dirList = ["constant", "VTK", "postProcessing"]

for fileName in fileList:
    runCommand("rm " + fileName, False)

for dirName in dirList:
    runCommand("rm -r " + dirName, False)
