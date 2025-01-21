from functions import runCommand, runFoamCommand, checkFoamVersion

# Written for Foam Extend v4.1
checkFoamVersion("4.1")

# Partitioned
runCommand("cp 0/fluid/orig/* 0/fluid/", False)
runCommand("cp 0/solid/orig/* 0/solid/", False)
runCommand("cp 0/fluid/orig/partitioned/* 0/fluid/", False)
runCommand("cp 0/solid/orig/partitioned/* 0/solid/", False)
runCommand(
    "cp constant/regionInterfacePropertiesPartitioned constant/regionInterfaceProperties"
)

for region in ["fluid", "solid"]:
    runFoamCommand("makeFaMesh", region=region)


# Serial
runFoamCommand("multiRegionFoam")

print()
print("Done!")
