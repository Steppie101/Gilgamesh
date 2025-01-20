"""Clear the generated directories and files."""

from functions import runCommand

fileList = [
    "results.foam",
    "log.*",
    "*.stl",
    "system/*/topoSetDict 0/*/*",
    "constant/*/faMesh/faBoundary",
    "constant/*/faMesh/faceLabels",
    "constant/regionInterfaceProperties",
]
dirList = ["constant/*/polyMesh", "VTK", "postProcessing"]

for fileName in fileList:
    runCommand("rm " + fileName, False)

for dirName in dirList:
    runCommand("rm -r " + dirName, False)
