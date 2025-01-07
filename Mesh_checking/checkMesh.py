"""Convert generated vtk to OpenFOAM, running checkMesh. Writing sets to vtk."""

import os


def runCommand(command, showWarnings=True):
    if ">" not in command:
        if showWarnings:
            command += " > /dev/null"
        else:
            command += " &> /dev/null"
    os.system(command)


runCommand("mkdir constant", False)
runCommand("touch results.foam", False)

for region in ["fluid", "solid"]:
    print("Importing " + region + " .vtk to OpenFOAM")
    runCommand("vtkUnstructuredToFoam mesh_" + region + ".vtk")
    runCommand("mkdir constant/" + region, False)
    runCommand("mv constant/polyMesh constant/" + region, False)

    print("Running checkMesh")
    runCommand(
        "checkMesh -region "
        + region
        + " -allGeometry -allTopology > "
        + "log.checkMesh."
        + region
        + ".txt"
    )


pointSets = ["unusedPoints", "multiRegionPoints", "nonManifoldPoints"]
cellSets = [
    "oneInternalFaceCells",
    "twoInternalFacesCells",
    "underdeterminedCells",
]
faceSets = ["nonOrthoFaces", "lowWeightFaces", "lowVolRatioFaces"]


for region in ["solid", "fluid"]:
    print("Writing error in " + region + " to vtk")
    for typeSet in ["pointSet", "faceSet", "cellSet"]:
        for checkSet in eval(typeSet + "s"):
            runCommand(
                "foamToVTK -region "
                + region
                + " -"
                + typeSet
                + " "
                + checkSet,
                True,
            )

print("Done!")

#     os.system("mkdir constant/fluid &>/dev/null")
# commandSet = [
#     "mkdir constant &>/dev/null",
#     #
#     # Fluid
#     "vtkUnstructuredToFoam mesh_fluid.vtk",
#     "mkdir constant/fluid &>/dev/null",
#     "mv constant/polyMesh constant/fluid/",
#     #
#     # Solid
#     "vtkUnstructuredToFoam mesh_solid.vtk",
#     "mkdir constant/solid &> /dev/null",
#     "mv constant/polyMesh constant/solid/",
#
# checkMesh
# "checkMesh -region fluid -allGeometry -allTopology > log.checkMesh.fluid.txt",
# "checkMesh -region solid -allGeometry -allTopology > log.checkMesh.solid.txt",
#     "touch results.foam",


# print("Converting fluid .vtk to Foam.")
# for command in commandSet:
#     if ">" not in command:
#         command += " > /dev/null"

#     os.system(command)
# for checkSet in pointSets:
#     os.system(
#         "foamToVTK -region "
#         + region
#         + " -pointSet "
#         + checkSet
#         + ">/dev/null"
#     )
# for checkSet in cellSets:
#     os.system(
#         "foamToVTK -region "
#         + region
#         + " -cellSet "
#         + checkSet
#         + ">/dev/null"
#     )
# for checkSet in faceSets:
#     os.system(
#         "foamToVTK -region "
#         + region
#         + " -faceSet "
#         + checkSet
#         + ">/dev/null"
#     )


# foamToVTK -pointSet unusedPoints -region solid
# foatToVTK -cellSet oneInternalFaceCells -region solid
# foatToVTK -cellSet twoInternalFacesCells -region solid
# foamToVTK -pointSet multiRegionPoints -region solid
# foamToVTK -pointSet nonManifoldPoints -region solid
# foamToVTK -faceSet nonOrthoFaces -region solid
# foatToVTK -cellSet underdeterminedCells -region solid
# foamToVTK -faceSet lowWeightFaces -region solid
# foamToVTK -faceSet lowVolRatioFaces -region solid
