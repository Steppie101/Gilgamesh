"""Convert .vtk mesh of fluid and solid to OpenFOAM."""

from functions import runCommand, checkContinuing
import os

if os.path.isdir("constant"):
    checkContinuing(
        "The directory 'constant' exists. Do you want to continue? "
    )

print()
runCommand("mkdir constant", False)
runCommand("touch results.foam", False)

for region in ["fluid", "solid"]:
    print("Importing .vtk of region " + region + " to foam")
    runCommand("vtkUnstructuredToFoam mesh_" + region + ".vtk")
    runCommand("mkdir constant/" + region, False)
    runCommand("mv constant/polyMesh constant/" + region, False)

print()
print("Done!")
