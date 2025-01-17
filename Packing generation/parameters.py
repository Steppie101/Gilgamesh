
#=======================#==============#========================#
#-----------------------:  Parameters  :------------------------#
#=======================#==============#========================#



#CUBE, UVSPHERE, ICOSPHERE, CYLINDER, STL
particle_type = "CUBE"
stl_import_path = "stl_files/ring.stl" #Path relative to the blender file
stl_export_path = "stl_files/cubes.stl" #Path relative to the blender file
spawn_interval = 20

#SHAPE SPECIFIC PARAMETERS
#CYLINDER
cylinder_ratio = 2.0     #depth / radius
cylinder_faces = 32      #only vertical faces (cylinder)

#UVSPHERE
uv_radius = 1.0
uv_segments = 32 #int
uv_rings = 16 #int

#ICOSPHERE
ico_radius = 1.0
ico_subdivisions = 2 #int

#spawnInterval = int(max(np.sqrt(2 * particleSize / g) * framesPerSecond + 1, spawnInterval))
x_size = 3
y_size = 3
z_size = "DEFAULT"
number_of_particles = 50
extra_iterations = 150
spawn_height = 25
overlap_size = 0.01

# BOX, SPHERE, CYLINDER, CONVEX_HULL, MESH (with MESH a collision margin is recommended)
collision_shape = 'BOX'
#Surface Friction Factor ( 0 < friction_factor < 1 )
friction = 0.5
#Surface Restitution Factor (0 < restitution_factor < 1)
bouncyness = 0.0
#Collision margin (lower value = more accuracy, 0 perfect value)
collision_margin = 0

#linear_damping(amount of linear velicity particle is lost over time)
linear_damping = 0.04
#rotational_dampin
angular_damping = 0.1

seed = "DEFAULT" #(DEFAULT -> random)
distribution = "UNIFORM" # UNIFORM, NORMAL, LOGNORMAL
# Standard deviation. In case of UNIFORM, the maximum distance from mean
scale_deviation = 0