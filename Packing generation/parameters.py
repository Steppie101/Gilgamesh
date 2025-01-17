#=======================#==============#========================#
#-----------------------:  Parameters  :------------------------#
#=======================#==============#========================#

# <[Import Parameters]>
# Import path relative to the blender file (used for STL particle type)
stl_import_path = "stl_files/ring.stl" 
# Export path relative to the blender file
stl_export_path = "stl_files/test.stl"


# <[Global Geometry Parameters]>
# Wall sizes measured in units of the largest xyz-dimension of the particle type 
# e.g. CUBE: side length, SPHERE: diameter, CYLINDER: max(depth, diameter), etc
x_size = 3
y_size = 3
# Height particles are spawned from
spawn_height = 25
# Total amount of particles
number_of_particles = 10
# Percentage particles grow for overlap (NOT including collision margin)
overlap_size = 0.01

# <[Shape Parameters]>
# Particle shapes (CUBE, UVSPHERE, ICOSPHERE, CYLINDER, STL)
particle_type = "CUBE"
# Cylinder depth/diameter ratio
cylinder_ratio = 1
# Cylinder vertical face count
cylinder_faces = 32
# UV Sphere longitudinal ring count
uv_segments = 32 
# UV Sphere Lattitudinal ring count
uv_rings = 16 
# Ico Sphere generation subdivitions (20 * n ^ 2 faces)
ico_subdivisions = 2 #int

# <[Physics Parameters]>
# Frames between particle spawns, at 24 frames per second
spawn_interval = 48
# Extra frames for the settlement of the particles
extra_iterations = 150
# Collision margin (BOX, SPHERE, CYLINDER, CONVEX_HULL, MESH) (a collision margin is recommended when using MESH)
collision_shape = 'BOX'
# Surface Friction Factor     [ Default: 0.5  ] ( Range 0-1 )       
friction = 0.5
# Surface Restitution Factor  [ Default: 0.0  ] ( Range 0-1 )    
restitution = 0.0
# Collision margin            [ Default: 0.04 ] ( Range 0-1 ) ( Lower values advised for better accuracy )
collision_margin = 0
# Linear velocity damping     [ Default: 0.04 ] ( Range 0-1 )
linear_damping = 0.04                                               
# Angular velocity damping    [ Default: 0.1  ] ( Range 0-1 )
angular_damping = 0.1

# <[Random Parameters]>
# Seed for all random processes  ( 32 bit integer or "RANDOM" )
seed = "RANDOM" 
# Distribution for particle size ( UNIFORM, NORMAL, LOGNORMAL )
distribution = "NORMAL"
# Standard deviation for particle scale, 
scale_deviation = 1