
#=======================#==============#========================#
#-----------------------:  Parameters  :------------------------#
#=======================#==============#========================#



# CUBE, SPHERE, CYLINDER, STL
particleType = "CUBE"
stlImportPath = "stl_files/ring.stl"
stlExportPath = "stl_files/test.stl"
spawnInterval = 20

#CUBE, UVSPHERE, ICOSPHERE, CYLINDER, STL
particleType = "ICOSPHERE"
stlImportPath = "stl_files/ring.stl"
stlExportPath = "stl_files/test.stl"
spawnInterval = 20

#SHAPE SPECIFIC PARAMETERS
#CYLINDER
cylinderRatio = 2.0     #depth / radius
cylinderFaces = 32      #only vertical faces (cylinder)

#UVSPHERE
uvRadius = 1.0
uvSegments = 32 #int
uvRings = 16 #int

#ICOSPHERE
icoRadius = 1.0
icoSubdivisions = 2 #int

#spawnInterval = int(max(np.sqrt(2 * particleSize / g) * framesPerSecond + 1, spawnInterval))
xSize = 2
ySize = 2
zSize = "DEFAULT"
numberParticles = 10
extraIterations = 150
spawnHeight = 25

# BOX, SPHERE, CYLINDER, CONVEX_HULL, MESH (with MESH a collision margin is recommended)
collisionShape = 'BOX'
#Surface Friction Factor ( 0 < friction_factor < 1 )
friction = 0.5
#Surface Restitution Factor (0 < restitution_factor < 1)
bouncyness = 0.0
#Collision margin (lower value = more accuracy, 0 perfect value)
collisionMargin = -0.1

#linear_damping(amount of linear velicity particle is lost over time)
linearDamping = 0.04
#rotational_dampin
angularDamping = 0.1

seed = "DEFAULT" #(DEFAULT -> random)
distribution = "UNIFORM" # UNIFORM, NORMAL, LOGNORMAL
# Standard deviation. In case of UNIFORM, the maximum distance from mean
scaleDeviation = 0