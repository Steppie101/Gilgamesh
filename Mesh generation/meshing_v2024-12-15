    return "Combined_Mesh"+ str(file_date)+".stl"


def Workflow(mesh_file):
    #surface_mesh1 = meshio.read(str(mesh_file))
    #surface_mesh2 = trimesh.load(str(mesh_file))

    Volume_Mesh(mesh_file,0)
    filename = Combined_Surfaces(mesh_file)
    Volume_Mesh(str(filename),1)

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


Workflow("fifty_spheres.stl")


#triangles = mesh_pygalmesh.cells_dict.get("triangle",None)

#if triangles is None:
#    raise ValueError("no triangle cells found in the STL file")

                                                                          130,0-1       Bot 
