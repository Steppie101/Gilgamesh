"""Convert .vtk mesh of fluid and solid to OpenFOAM. Removes small datasets and unusedPoints."""

from functions import runCommand, checkContinuing
import os
import re

if os.path.isdir("constant"):
    checkContinuing(
        "The directory 'constant' exists. Do you want to continue? "
    )


def fillTopoSetDict(region, logfile):
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
    topoSetDictpath = "system/" + region + "/topoSetDict"
    with open(logfile, "r") as file:
        content = file.read()

    pattern = r"Region\s+Cells\n+[-]+\s+[-]+\n((?:\d+\s+\d+\s*)+)"
    matches = re.search(pattern, content)
    if matches:
        headers = ["Region", "Cells"]
        lst = [
            list(map(int, row.split()))
            for row in matches.group(1).strip().split("\n")
        ]

        with open(topoSetDictpath, "a") as topoSetDict:
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

                if nrFaces >= 1:
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
    print("Removing small sets")
    runCommand(
        "splitMeshRegions -makeCellZones -overwrite -region "
        + region
        + " >log.splitMeshRegions."
        + region
    )
    runCommand(
        "cp system/topoSetDictHeader system/" + region + "/topoSetDict", False
    )
    nrSetsMerged = fillTopoSetDict(region, "log.splitMeshRegions." + region)
    if nrSetsMerged >= 1:
        runCommand("topoSet -region " + region)
    else:
        checkContinuing("There are not any sets found. Continuing? ")
    runCommand("subsetMesh combinedCells -overwrite -region " + region)
    runCommand(
        "rm constant/"
        + region
        + "/cellToRegion constant/"
        + region
        + "/polyMesh/cellZones constant/"
        + region
        + "/polyMesh/sets/combinedCells 0/"
        + region
        + "/cellToRegion"
    )


print()
runCommand("mkdir constant", False)
runCommand("touch results.foam", False)

for region in ["fluid"]:
    print("Importing .vtk of region " + region + " to foam")
    runCommand("vtkUnstructuredToFoam mesh_" + region + ".vtk")
    runCommand("mkdir constant/" + region, False)
    runCommand("mv constant/polyMesh constant/" + region, False)
    removeSmallSets(region)
print()
print("Done!")
