"""
Check the validaty of the fluid and solid mesh using OpenFOAM's checkMesh.

Writing sets with mesh errors to .vtk.
"""

from functions import runCommand


def showMeshErrors(region):
    """
    Prints the type and count of mesh errors for all files in the directory constant/{region}/polyMesh/sets.

    Parameters
    ----------
    region : str
        The mesh region to check for errors.

    Returns
    -------
    None
    """
    command = (
        """
            bash -c '
for file in constant/"""
        + region
        + """/polyMesh/sets/*; do
    if [[ ! $(basename "$file") =~ ^region.* ]] && [[ -f $file ]]; then
        numberOfErrors=$(sed -n "20p" "$file")
        if [[ -z "$numberOfErrors" ]]; then
            numberOfErrors=$(sed -n "19p" "$file" | cut -d "(" -f 1)
        fi
        echo "$(basename "$file"): $numberOfErrors"
    fi
done
'

        """
    )
    runCommand(command)


pointSets = [
    "multiRegionPoints",
    "nearPoints",
    "nonManifoldPoints",
    "unusedPoints",
]

cellSets = [
    "concaveCells",
    "highAspectRatioCells",
    "nonClosedCells",
    "oneInternalFaceCells",
    "twoInternalFacesCells",
    "underdeterminedCells",
    "zeroVolumeCells",
]
faceSets = [
    "concaveFaces",
    "lowQualityTetFaces",
    "lowVolRatioFaces",
    "lowWeightFaces",
    "nonOrthoFaces",
    "skewFaces",
    "wrongOrientedFaces",
    "zeroAreaFaces",
]

edgeSets = ["shortEdges"]

for region in ["solid", "fluid"]:
    print("Running checkMesh on region " + region)
    runCommand(
        "checkMesh -writeSets vtk -region "  # -writeSets does not work for all OF versions
        + region
        + " -allGeometry -allTopology > "
        + "log.checkMesh."
        + region
    )
    print("Results: ")
    showMeshErrors(region)
    print()

    print("Writing mesh validity errors for " + region + " to vtk.")
    for typeSet in ["cellSet", "edgeSet", "faceSet", "pointSet"]:
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
    print()

print("Done!")
