import pygalmesh


mesh = pygalmesh.generate_volume_mesh_from_surface_mesh(
    "sphere_packing.stl",
    min_facet_angle=25.0,
    max_radius_surface_delaunay_ball=0.15,
    max_facet_distance=0.008,
    max_circumradius_edge_ratio=3.0,
    verbose=True,
)

print(mesh)

mesh.write("mesh_stl.vtk", binary=False)
