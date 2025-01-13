###############################################################################
#
#
#
###############################################################################


import pygalmesh as pm
import meshio
import trimesh
import pyvista as pv
import numpy as np
import os
from datetime import date, datetime



def Volume_Mesh(mesh_file,argument):
    """Generates a volume mesh from a surface mesh. 
        Input should be a .stl file. 
        Output will be a .vtk file"""
        
    print("Starting volume mesh") 
    start_volume = datetime.now()
    volume_mesh = pm.generate_volume_mesh_from_surface_mesh(
        mesh_file,
        min_facet_angle=25.0, 
        max_radius_surface_delaunay_ball=0.0035,
        max_facet_distance=0.008,
        max_circumradius_edge_ratio=2.0,
        verbose=True,)
    
    file_date = date.today()
    if argument == 0:               # Saving the volume mesh of the geometries
        volume_mesh.write("Geometry_Volume_Mesh"+ str(file_date)+".vtk", binary = False)
        print("The mesh of the geometry is saved as Geometry_Volume_Mesh"+str(file_date)+".vtk")
        
    elif argument == 1:             # Saving the volume mesh of the fluid region and fixing the fluid region
        
        volume_mesh.write("Pre_Fluid"+ str(file_date)+".vtk", binary = False)
        
        pyvista_mesh = pv.read("Pre_Fluid"+ str(file_date)+".vtk")
        
        points = pyvista_mesh.points

        x_coords = points[:,0]
        y_coords = points[:,1] 
        xmax = max(x_coords)
        xmin = min(x_coords)
        ymax = max(y_coords)
        ymin = min(y_coords)
        
        
        min_dif = min(xmax-xmin, ymax-ymin)
        factor = min_dif/200
        
        xmax_origin = np.array([xmax - factor,0,0])
        xmax_normal = np.array([1,0,0])
        
        xmin_origin = np.array([xmin + factor,0,0])
        xmin_normal = np.array([-1,0,0])
        
        ymax_origin = np.array([0,ymax - factor,0])
        ymax_normal = np.array([0,1,0])
        
        ymin_origin = np.array([0,ymin + factor,0])
        ymin_normal = np.array([0,-1,0])
        
        sliced_mesh = pyvista_mesh.clip(normal = xmax_normal, origin = xmax_origin)
        sliced_mesh = sliced_mesh.clip(normal = xmin_normal, origin = xmin_origin)
        sliced_mesh = sliced_mesh.clip(normal = ymax_normal, origin = ymax_origin)
        sliced_mesh = sliced_mesh.clip(normal = ymin_normal, origin = ymin_origin)


        sliced_mesh.save("Fluid_Volume_mesh"+ str(file_date)+".vtk", binary=False)
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
    
    surface_mesh = meshio.read(mesh_file)
    nodes = surface_mesh.points
    nodesT = nodes.T
    xmax = max(nodesT[0])
    xmin = min(nodesT[0])
    ymax = max(nodesT[1]) 
    ymin = min(nodesT[1])
    zmax = max(nodesT[2])
    zmin = min(nodesT[2])
    
    xlength = xmax - xmin
    ylength = ymax - ymin
    zlength = zmax - zmin

    factor = 1

    cube = trimesh.creation.box(extents = (xlength/factor, ylength/factor, zlength/factor))
    
    cube.apply_translation((0,0, zlength/2))
    return cube


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
    box = Box_Mesh(mesh_file)
    
    sliced_mesh = trimesh.boolean.intersection([geometry,box])
    


    combined_mesh = box + sliced_mesh

    file_date = date.today()
    combined_mesh.export("Combined_Mesh"+ str(file_date)+".stl")
    print("The combined mesh is saved as Combined_Mesh"+str(file_date)+".stl")
    print(" ")

    return "Combined_Mesh"+ str(file_date)+".stl"



def Workflow(mesh_file):
    start_workflow = datetime.now()
    file_date = date.today()

    smoothed_mesh = Remeshing_Corners(mesh_file)
    Volume_Mesh(smoothed_mesh,0)
    filename = Combined_Surfaces(smoothed_mesh)
    Volume_Mesh(filename,1)
    
    print("Removing the files")
    os.system("rm Smoothed_Mesh"+ str(file_date)+".stl")
    os.system("rm Combined_Mesh"+ str(file_date)+".stl")
    os.system("rm Pre_Fluid"+ str(file_date)+".vtk") 

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

#Volume_Mesh("Smoothed_Mesh2025-01-10.stl",0)
#triangles = mesh_pygalmesh.cells_dict.get("triangle",None)

#if triangles is None:
#    raise ValueError("no triangle cells found in the STL file")

                            
