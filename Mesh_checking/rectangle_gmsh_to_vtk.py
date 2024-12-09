import gmsh

# Initialize Gmsh
gmsh.initialize()

# Add a model name
gmsh.model.add("Rectangle3D")

# Define parameters for the rectangle
L = 2.0  # Length of the rectangle (x-direction)
H = 1.0  # Height of the rectangle (y-direction)
T = 0.1  # Thickness of extrusion (z-direction)

# Add points for the 2D rectangle
p1 = gmsh.model.geo.addPoint(0, 0, 0, 0.1)
p2 = gmsh.model.geo.addPoint(L, 0, 0, 0.1)
p3 = gmsh.model.geo.addPoint(L, H, 0, 0.1)
p4 = gmsh.model.geo.addPoint(0, H, 0, 0.1)

# Add lines for the rectangle
l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p3)
l3 = gmsh.model.geo.addLine(p3, p4)
l4 = gmsh.model.geo.addLine(p4, p1)

# Create a curve loop and a surface
loop = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
surface = gmsh.model.geo.addPlaneSurface([loop])

# Extrude the 2D surface into a 3D volume
extrusion = gmsh.model.geo.extrude([(2, surface)], 0, 0, T)

# Synchronize the geometry
gmsh.model.geo.synchronize()

# Add physical groups for OpenFOAM
volume = extrusion[1][1]  # 3D volume from the extrusion
gmsh.model.addPhysicalGroup(3, [volume], 1)  # Physical group for the volume
gmsh.model.setPhysicalName(3, 1, "BlockVolume")

# Add physical groups for boundary faces (optional)
# You can reference the faces by extrusion[0] (extruded surfaces)
gmsh.model.addPhysicalGroup(2, [extrusion[0][1]], 2)  # Bottom face
gmsh.model.setPhysicalName(2, 2, "Bottom")
gmsh.model.addPhysicalGroup(2, [extrusion[3][1]], 3)  # Top face
gmsh.model.setPhysicalName(2, 3, "Top")

# Generate the 3D mesh
gmsh.option.setNumber("Mesh.ElementOrder", 1)  # Ensure linear elements
gmsh.model.mesh.generate(3)  # Generate 3D mesh

# Save the mesh to a file in Gmsh format 2.2 for OpenFOAM compatibility
gmsh.write("mesh_rectangle.vtk")

# # Launch GUI for visualization (if not running in batch mode)
# if "-nopopup" not in sys.argv:
#     gmsh.fltk.run()

# Finalize Gmsh
gmsh.finalize()
