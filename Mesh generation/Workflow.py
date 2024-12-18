###############################################################################
#
#
#
###############################################################################


import pygalmesh as pm
import meshio
import trimesh
from datetime import date, datetime

def Volume_Mesh(mesh_file,argument):
    """Generates a volume mesh from a surface mesh. 
        Input should be a .stl file. 
        Output will be a .vtk file"""
        
    print("Starting volume mesh") 
    start_volume = datetime.now()
    volume_mesh = pm.generate_volume_mesh_from_surface_mesh(
        mesh_file,
        min_facet_angle=25.0, #dit is met een afwijking van 65% terwijl sebastiaan normaal 40% gebruikt.
        max_radius_surface_delaunay_ball=0.008,
        max_facet_distance=0.008,
        max_circumradius_edge_ratio=3.0,
        verbose=True,)
    
    file_date = date.today()
    if argument == 0:               # Saving the volume mesh of the geometries
        volume_mesh.write("Geometry_Volume_Mesh"+ str(file_date)+".vtk", binary = False)
        print("The mesh of the geometry is saved as Geometry_Volume_Mesh"+str(file_date)+".vtk")
        
    elif argument == 1:             # Saving the volume mesh of the fluid region
        volume_mesh.write("Fluid_Volume_mesh"+ str(file_date)+".vtk", binary = False)
        print("The mesh of the Fluid region is saved as Fluid_Volume_Mesh"+str(file_date)+".vtk")
        
    else:
        volume_mesh.write("Volume_mesh"+ str(file_date)+".vtk", binary = False)
        print("The mesh is saved as Volume_Mesh"+str(file_date)+".vtk")
        
    end_volume = datetime.now()
    
    print("Time used for the volume mesh: ", end_volume - start_volume)
    print(" ")
    return 



def Box_Mesh(mesh_file):
    """Generates a surface mesh of the box"""
    #deze functie creeërt een box om de ballen heen. De functie werkt.
    #de hoekpunten zijn niet gerefined maar ik weet niet of dat nodig is.
    #met hulp van Marieke Bosch
    

    print("Starting box mesh")
    start_box = datetime.now()
    
    surface_mesh = meshio.read(mesh_file)
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
        max_radius_surface_delaunay_ball=0.0008,
        max_facet_distance=0.0008,)
    
    end_box = datetime.now()
    file_date = date.today()
    cubemesh.write("Cube_Mesh"+ str(file_date)+".stl")
    print("The mesh of the cube is saved as Cube_Mesh"+str(file_date)+".stl")
    print("Time used for the box mesh: ", end_box - start_box)
    print(" ")
    
    return "Cube_Mesh"+str(file_date)+".stl"


def Remeshing_Corners(mesh_file):
    """Remeshes the surface and then fixes the corners where the different geometries meet"""
    mesh = trimesh.load(mesh_file)
    remeshed_vertices, remeshed_faces = trimesh.remesh.subdivide(
            mesh.vertices,
            mesh.faces,
            face_index = None,
            vertex_attributes = None,
            return_index = False)

    remeshed_mesh = trimesh.Trimesh(remeshed_vertices, remeshed_faces)
    smoothed_mesh = trimesh.smoothing.filter_laplacian(
            remeshed_mesh,
            lamb = 0.005,
            iterations = 30,
            implicit_time_integration = False,
            volume_constraint = True,
            laplacian_operator = None)
    
    file_date = date.today()
    smoothed_mesh.export("Smoothed_Mesh"+ str(file_date)+".stl")
    print("The smoothed mesh is saved as Smoothed_Mesh"+str(file_date)+".stl")
    
    return "Smoothed_Mesh"+ str(file_date)+".stl"

def Combined_Surfaces(mesh_file):
    """Combines the two surface meshes into one surface mesh. 
        Input should be the mesh of the geometry""" 
    
    geometry = trimesh.load(mesh_file)
    filename = Box_Mesh(mesh_file)
    box = trimesh.load(filename)
    combined_mesh = box + geometry

    file_date = date.today()
    combined_mesh.export("Combined_Mesh"+ str(file_date)+".stl")
    print("The combined mesh is saved as Combined_Mesh"+str(file_date)+".stl")
    print(" ")

    return "Combined_Mesh"+ str(file_date)+".stl"



def Workflow(mesh_file):
    start_workflow = datetime.now()
    
    smoothed_mesh = Remeshing_Corners(mesh_file)
    Volume_Mesh(smoothed_mesh,0)
    filename = Combined_Surfaces(smoothed_mesh)
    Volume_Mesh(filename,1)
    
    end_workflow = datetime.now()
    print("Time used for the entire workflow: ", end_workflow - start_workflow)

    return




###############################################################################



# Add a try except error message
#while True:
#    try:
#        mesh_file = str(input("What is the file name?: "))
#        mesh_trimesh = trimesh.load(str(mesh_file))
#        #mesh_pygalmesh = meshio.read(str(mesh_file))

#break
#    except FileNotFoundError:
#        print("Wrong filename, filename either does not exist or did not end with .stl")


Workflow("qo)-(.stl")


#triangles = mesh_pygalmesh.cells_dict.get("triangle",None)

#if triangles is None:
#    raise ValueError("no triangle cells found in the STL file")

                            
