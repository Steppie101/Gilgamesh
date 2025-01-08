"""Convert generated vtk to OpenFOAM, running checkMesh. Writing sets to vtk."""

from functions import runCommand


def showMeshErrors(region):
    command = (
        """
    bash -c '
    for file in constant/"""
        + region
        + """/polyMesh/sets/*; do
      if [[ ! $(basename "$file") =~ ^region.* ]] && [[ -f $file ]]; then
        numberOfErrors=$(sed -n "20p" "$file")
        echo "$(basename "$file"): $numberOfErrors"
      fi
    done
    '
    """
    )
    runCommand(command)


runCommand("mkdir constant", False)
runCommand("touch results.foam", False)

for region in ["fluid", "solid"]:
    print("Importing " + region + " .vtk to OpenFOAM")
    runCommand("vtkUnstructuredToFoam mesh_" + region + ".vtk")
    runCommand("mkdir constant/" + region, False)
    runCommand("mv constant/polyMesh constant/" + region, False)

    print("Running checkMesh...")
    runCommand(
        "checkMesh -region "
        + region
        + " -allGeometry -allTopology > "
        + "log.checkMesh."
        + region
        + ".txt"
    )
    print("Results: ")
    showMeshErrors(region)
    print()


pointSets = ["unusedPoints", "multiRegionPoints", "nonManifoldPoints"]
cellSets = [
    "oneInternalFaceCells",
    "twoInternalFacesCells",
    "underdeterminedCells",
]
faceSets = ["nonOrthoFaces", "lowWeightFaces", "lowVolRatioFaces"]


for region in ["fluid", "solid"]:
    print("Writing mesh validty errors for " + region + " to vtk.")
    for typeSet in ["pointSet", "faceSet", "cellSet"]:
        for checkSet in eval(typeSet + "s"):
            runCommand(
                "foamToVTK -region "
                + region
                + " -"
                + typeSet
                + " "
                + checkSet,
                False,
            )

print("Done!")
