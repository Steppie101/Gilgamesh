from functions import runCommand, runFoamCommand, checkFoamVersion

# Written for Foam Extend v4.1
checkFoamVersion("4.1")

# Partitioned
runCommand("cp 0/fluid/orig/* 0/fluid/", False)
runCommand("cp 0/solid/orig/* 0/solid/", False)

while True:
    typeSolving = input("Monolithic (m) or partitioned (p)? ")

    if typeSolving.lower() == "m":
        typeSolving = "monolithic"
        break
    elif typeSolving.lower() == "p":
        typeSolving = "partitioned"
        break
    else:
        print("This type of solving is not possible.\n")

while True:
    parallel = input("Serial (S) or parallel (P)? ")

    if parallel.lower() == "s":
        parallel = False
        break
    elif parallel.lower() == "p":
        prallel = True
        break
    else:
        print("This answer is not recognized.\n")

runCommand("cp 0/fluid/orig/" + typeSolving + "/* 0/fluid/", False)
runCommand("cp 0/solid/orig/" + typeSolving + "/* 0/solid/", False)
runCommand(
    "cp constant/regionInterfaceProperties"
    + typeSolving
    + " constant/regionInterfaceProperties"
)

for region in ["fluid", "solid"]:
    runFoamCommand("makeFaMesh", region=region)
    if parallel:
        runFoamCommand("decomposePar", region=region)

if parallel:
    runFoamCommand(
        "multiRegionFoam", arguments="-parallel", beforeCommand="mpirun -np 4"
    )
else:
    runFoamCommand("multiRegionFoam")

print()
print("Done!")
