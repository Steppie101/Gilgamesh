import os

import subprocess

sp = subprocess.Popen(["/bin/bash", "-i", "-c", "nuke -x scriptpath"])
sp.communicate()

path = os.path.dirname(os.path.relpath(__file__))
if "C:/" in path:
    path = (path.split("C:/"))[-1]
    path = "/mnt/c/" + path

os.chdir(path)


# os.system("source /usr/lib/openfoam/openfoam2406/etc/bashrc")

os.system("vtk3DToFoam mesh_stl.vtk")
os.system("checkMesh -allRegions -allGeometry -allTopology | tee output.txt")
os.system("touch results.foam")
os.system("foamToVTK")
os.system("foamToVTK -faceSet nonOrthoFaces")
