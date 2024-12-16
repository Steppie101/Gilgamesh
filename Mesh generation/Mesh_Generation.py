###############################################################################
#
#
#
###############################################################################


import pygalmesh as pm
import meshio
import time
import trimesh
from datetime import date

def Volume_Mesh(surface_mesh,argument):
    """Generates a volume mesh from a surface mesh. 
        Input should be a .stl file. 
        Output will be a .vtk file"""
        
    volume_mesh = pm.generate_volume_mesh_from_surface_mesh(
        surface_mesh,
        min_facet_angle=25.0, #dit is met een afwijking van 65% terwijl sebastiaan normaal 40% gebruikt.
        max_radius_surface_delaunay_ball=0.00015,
        max_facet_distance=0.00008,
        max_circumradius_edge_ratio=3.0,
        verbose=True,)
    
    if argument == 0:               # Saving the volume mesh of the geometries
        file_date = date.today()
        volume_mesh.write("Geometry_Volume_Mesh"+ str(file_date)+".vtk")
        print("The mesh of the cube is saved as Geometry_Volume_Mesh"+str(file_date)+".vtk", binary = False)
        
    elif argument == 1:             # Saving the volume mesh of the fluid region
        volume_mesh.write("Fluid_Volume_mesh"+ str(file_date)+".vtk", binary = False)
        print("The mesh of the cube is saved as Fluid_Volume_Mesh"+str(file_date)+".vtk")
        
    else:
        volume_mesh.write("Volume_mesh"+ str(file_date)+".vtk", binary = False)
        print("The mesh of the cube is saved as Volume_Mesh"+str(file_date)+".vtk")
        
    return 



def Box_Mesh(surface_mesh):
    """Generates a surface mesh of the box"""
    #deze functie creeërt een box om de ballen heen. De functie werkt.
    #de hoekpunten zijn niet gerefined maar ik weet niet of dat nodig is.
    #met hulp van Marieke Bosch
    
    nodes = surface_mesh.points
    nodesT = nodes.T
    xmax = max(nodesT[0])
    xmin = min(nodesT[0])
    ymax = max(nodesT[1]) 
    ymin = min(nodesT[1])
    zmax = max(nodesT[2])
    zmin = min(nodesT[2])
    
    cube = pm.Cuboid([xmin,ymin,zmin],[xmax,ymax,zmax])
    cubemesh = pm.generate_surface_mesh(
        domain=cube,
        min_facet_angle=25.0,
        max_radius_surface_delaunay_ball=0.00008,
        max_facet_distance=0.00008,)
    
    file_date = date.today()
    cubemesh.write("Cube_Mesh"+ str(file_date)+".stl")
    print("The mesh of the cube is saved as Cube_Mesh"+str(file_date)+".stl")
    
    return "Cube_Mesh"+str(file_date)+".stl"




def Combined_Surfaces(geometry):
    """Combines the two surface meshes into one surface mesh. 
        Input should be the mesh of the geometry""" 
        
    filename = Box_Mesh(geometry)
    box = trimesh.load(str(filename))
    combined_mesh = box + geometry
    combined_mesh.export("combi.stl")

    file_date = date.today()
    combined_mesh.write("Combined_Mesh"+ str(file_date)+".stl")
    print("The combined mesh is saved as Combined_Mesh"+str(file_date)+".stl")
    
    return "Combined_Mesh"+ str(file_date)+".stl"


def Workflow(surface_mesh1, surface_mesh2):
    Volume_Mesh(surface_mesh1,0)
    filename = Combined_Surfaces(surface_mesh2)
    Volume_Mesh(str(filename),1)
    
    return




###############################################################################



# Add a try except error message
while True:
    try:
        mesh_file = str(input("What is the file name?: "))
        mesh_trimesh = trimesh.load(mesh_file)
        mesh_pygalmesh = meshio.read(mesh_file)
        break
    except FileNotFoundError:
        print("Wrong filename, filename either does not exist or did not end with .stl")
    




triangles = mesh_pygalmesh.cells_dict.get("triangle",None)

if triangles is None:
    raise ValueError("no triangle cells found in the STL file")

