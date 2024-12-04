import os


def changeWorkingDir():
    path = os.path.dirname(os.path.relpath(__file__))
    if "C:/" in path:
        path = (path.split("C:/"))[-1]
        path = "/mnt/c/" + path

    os.chdir(path)


changeWorkingDir()

fileList = ["mesh_stl.vtk", "results.foam", "log.checkMesh.txt"]
dirList = ["constant", "VTK", "postProcessing"]

for fileName in fileList:
    os.system("rm " + fileName + " 2>/dev/null")

for dirName in dirList:
    os.system("rm -r " + dirName + " 2>/dev/null")
