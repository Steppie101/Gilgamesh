"""Convert .vtk mesh of fluid and solid to OpenFOAM. Removes small datasets and unusedPoints."""

from functions import runCommand, checkContinuing
import os
import re
import meshio


def fillTopoSetDictMeshRegions(region, logfile):
    """
    Reads a logfile to extract number of cells for each region. Updating topoSetDict to merge regions.

    Parameters
    ----------
    region : str
        Name of the region.
    logfile : str
        Path to the logfile of splitMeshRegions.

    Returns
    -------
    nrSetsMerged : int
        Number of sets added to `topoSetDict`.
    """
    with open(logfile, "r") as file:
        content = file.read()

    pattern = r"Region\s+Cells\n+[-]+\s+[-]+\n((?:\d+\s+\d+\s*)+)"
    matches = re.search(pattern, content)
    if matches:
        lst = [
            list(map(int, row.split()))
            for row in matches.group(1).strip().split("\n")
        ]

        with open(eval(topoSetDictPath), "w") as topoSetDict:
            with open(eval(topoSetDictHeaderPath), "r") as file:
                topoSetDict.write(file.read())

            topoSetDict.write("actions (")
            nrSetsMerged = 0
            for lstLst in lst:
                regionId = lstLst[0]
                nrFaces = lstLst[1]
                topoSetDictRegion = (
                    """
    {
        name combinedCells;
        type cellSet;
        action """
                    + ("new" if nrSetsMerged == 0 else "add")
                    + """;
        source zoneToCell;
        sourceInfo
        {
            zone region"""
                    + str(regionId)
                    + """;
        }
    }
                """
                )

                if nrFaces >= minFaces:
                    topoSetDict.write(topoSetDictRegion)
                    nrSetsMerged += 1

            topoSetDict.write("\n);")
    return nrSetsMerged


def removeSmallSets(region):
    """
    Removes small sets in region by splitting and merging cell zones.

    Parameters
    ----------
    region : str
        Name of the region to process.

    Returns
    -------
    None
    """
    print("Removing small mesh regions")
    runCommand(
        "splitMeshRegions -makeCellZones -overwrite -region "
        + region
        + " >log.splitMeshRegions."
        + region
    )

    nrSetsMerged = fillTopoSetDictMeshRegions(
        region, "log.splitMeshRegions." + region
    )
    if nrSetsMerged >= 1:
        runCommand("topoSet -region " + region)
    else:
        checkContinuing("There are not any sets found. Continuing? ")
    runCommand("subsetMesh combinedCells -overwrite -region " + region)
    runCommand(
        "rm constant/"
        + region
        + "/cellToRegion "
        + "constant/"
        + +region
        + "/polyMesh/cellZones "
        + "constant/"
        + region
        + "/polyMesh/sets/combinedCells "
        + "0/"
        + region
        + "/cellToRegion"
    )


def topoSetDictSideBegin(sideNr):
    """
    Create for a side the beginning part of the topoSetDict.

    Parameters
    ----------
    sideNr : int
        The number of the side (1-6).

    Returns
    -------
    str
        The entry for topoSetDict (minus bounding box).

    """
    return (
        """
    {
        name side"""
        + str(sideNr)
        + """;
        type faceSet;
        action new;
        source patchToFace;
        sourceInfo
        {
            patch "defaultFaces";
        }
    }
    {
        name        side"""
        + str(sideNr)
        + """;
        type        faceSet;
        action      subtract;
        source      boxToFace;
    """
    )


def createPatches(region):
    """
    Create boundary patches for the region region.

    Parameters
    ----------
    region : str
        Name of the region.

    Returns
    -------
    None.

    """
    print("Creating patches")

    mesh = meshio.read("mesh_solid.vtk")
    points = (mesh.points).T
    # points = points.T
    xmax = max(points[0])
    xmin = min(points[0])
    ymax = max(points[1])
    ymin = min(points[1])
    zmax = max(points[2])
    zmin = min(points[2])

    boxes = [
        # Box 1
        "    box ("
        + str(xmin + boxMarginSmall)
        + " "
        + str(ymin - boxMarginBig)
        + " "
        + str(zmin - boxMarginBig)
        + ") ("
        + str(xmax + boxMarginBig)
        + " "
        + str(ymax + boxMarginBig)
        + " "
        + str(zmax + boxMarginBig)
        + ");",
        #
        # Box 2
        "    box ("
        + str(xmin - boxMarginBig)
        + " "
        + str(ymin - boxMarginBig)
        + " "
        + str(zmin - boxMarginBig)
        + ") ("
        + str(xmax - boxMarginSmall)
        + " "
        + str(ymax + boxMarginBig)
        + " "
        + str(zmax + boxMarginBig)
        + ");",
        #
        # Box 3
        "    box ("
        + str(xmin - boxMarginBig)
        + " "
        + str(ymin + boxMarginSmall)
        + " "
        + str(zmin - boxMarginBig)
        + ") ("
        + str(xmax + boxMarginBig)
        + " "
        + str(ymax + boxMarginBig)
        + " "
        + str(zmax + boxMarginBig)
        + ");",
        #
        # Box 4
        "    box ("
        + str(xmin - boxMarginBig)
        + " "
        + str(ymin - boxMarginBig)
        + " "
        + str(zmin - boxMarginBig)
        + ") ("
        + str(xmax + boxMarginBig)
        + " "
        + str(ymax - boxMarginSmall)
        + " "
        + str(zmax + boxMarginBig)
        + ");",
        #
        # Box 5
        "    box ("
        + str(xmin - boxMarginBig)
        + " "
        + str(ymin - boxMarginBig)
        + " "
        + str(zmin + boxMarginSmall)
        + ") ("
        + str(xmax + boxMarginBig)
        + " "
        + str(ymax + boxMarginBig)
        + " "
        + str(zmax + boxMarginBig)
        + ");",
        #
        # Box 6
        "    box ("
        + str(xmin - boxMarginBig)
        + " "
        + str(ymin - boxMarginBig)
        + " "
        + str(zmin - boxMarginBig)
        + ") ("
        + str(xmax + boxMarginBig)
        + " "
        + str(ymax + boxMarginBig)
        + " "
        + str(zmax - boxMarginSmall)
        + ");",
    ]

    with open(eval(topoSetDictPath), "w") as topoSetDict:
        with open(eval(topoSetDictHeaderPath), "r") as file:
            topoSetDict.write(file.read())

        topoSetDict.write("actions \n(")
        for sideNr in range(0, 6):
            topoSetDict.write(topoSetDictSideBegin(sideNr + 1))
            topoSetDict.write(boxes[sideNr])
            topoSetDict.write("\n    }\n")
        topoSetDict.write("\n")

        with open(eval(topoSetDictPatchesPath), "r") as file:
            topoSetDict.write(file.read())

        topoSetDict.write("\n);")

    print("topoSetDict written")
    runCommand("topoSet -region " + region)
    runCommand("createPatch -overwrite -region " + region)


# topoSetDict files
topoSetDictPath = '"system/" + region + "/topoSetDict"'
topoSetDictHeaderPath = '"system/" + region + "/topoSetDictHeader"'
topoSetDictPatchesPath = '"system/" + region + "/topoSetDictPatches"'

# Properties
boxMarginSmall = 0.01
boxMarginBig = 10
minFaces = 10


if os.path.isdir("constant/solid/polyMesh"):
    checkContinuing(
        "The directory 'constant/solid/polyMesh' exists. Do you want to continue? "
    )

print()
runCommand("touch results.foam", False)

for region in ["fluid", "solid"]:
    print("Importing .vtk of region " + region + " to foam")
    runCommand("sed -i 's/vtktypeint64/int/g' mesh_" + region + ".vtk")
    runCommand("vtkUnstructuredToFoam mesh_" + region + ".vtk")
    runCommand("mv constant/polyMesh constant/" + region, False)
    removeSmallSets(region)
    createPatches(region)
print()
print("Done!")
