import pygalmesh
import os

path = os.path.dirname(os.path.relpath(__file__))
if "C:/" in path:
    path = (path.split("C:/"))[-1]
    path = "/mnt/c/" + path

os.chdir(path)

mesh = pygalmesh.generate_volume_mesh_from_surface_mesh(
    "sphere_packing.stl",
    min_facet_angle=25.0,
    max_radius_surface_delaunay_ball=0.15,
    max_facet_distance=0.008,
    max_circumradius_edge_ratio=3.0,
    verbose=True,
)


volumetriangels = mesh.cells_dict.get("triangle", None)
volumetetras = mesh.cells_dict.get("tetra", None)

print(mesh)
# volumeHexa = mesh.cells

mesh.write("mesh_stl.vtk", binary=False)
