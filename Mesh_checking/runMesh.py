from functions import runCommand

# Partitioned
runCommand("cp 0/fluid/orig/* 0/fluid/", False)
runCommand("cp 0/solid/orig/* 0/solid/", False)
runCommand("cp 0/fluid/orig/partitioned/* 0/fluid/", False)
runCommand("cp 0/solid/orig/partitioned/* 0/solid/", False)
runCommand(
    "cp constant/regionInterfacePropertiesPartitioned constant/regionInterfaceProperties"
)

runCommand("makeFaMesh -region fluid > log.makeFaMesh.fluid")
runCommand("makeFaMesh -region solid > log.makeFaMesh.solid")

# Serial
runCommand("multiRegionFoam > log.multiRegionFoam")
