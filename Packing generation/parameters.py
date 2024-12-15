
#╔═══════════════════════╦══════════════╦═══════════════════════╗#
#╠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄╌╣  Parameters  ╠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╣#
#╚═══════════════════════╩══════════════╩═══════════════════════╝#



# cube, sphere, cylinder, cone, STL
particleType = "stl"
stlImportPath = "stl_files\\ring.stl"
stlExportPath = "stl_files\\test.stl"
particleSize = 1
framesPerSecond = 25
g = 9.81
spawnInterval = 20

#spawnInterval = int(max(np.sqrt(2 * particleSize / g) * framesPerSecond + 1, spawnInterval))
xSize = 5
ySize = 5
numberParticles = 15
extraIterations = 100
spawnHeight = 25
scaleMean = 1
scaleDeviation = 0

# BOX, SPHERE, CYLINDER, CONVEX_HULL, MESH
collisionShape = 'MESH'
#Surface Friction Factor ( 0 < friction_factor < 1 )
friction = 0.5
#Surface Restitution Factor (0 < restitution_factor < 1)
bouncyness = 0.0
#Colosion margin (lower value = more accuracy, 0 perfect value)
collisionMargin = 0.0

#linear_damping(amount of linear velicity particle is lost over time)
linearDamping = 0.04
#rotational_dampin
angularDamping = 0.1