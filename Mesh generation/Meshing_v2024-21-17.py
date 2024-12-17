    #deze functie creeërt een box om de ballen heen. De functie werkt.
    #de hoekpunten zijn niet gerefined maar ik weet niet of dat nodig is.
    #met hulp van Marieke Bosch

    print("Starting the box mesh")
    surface_mesh = meshio.read(str(mesh_file))
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
        max_radius_surface_delaunay_ball=0.08,
        max_facet_distance=0.08,)

    file_date = date.today()
    cubemesh.write("Cube_Mesh"+ str(file_date)+".stl")
    print("The mesh of the cube is saved as Cube_Mesh"+str(file_date)+"B.stl")

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
:wNext wall while wincmd windo winpos winsize wnext wprevious wq wqall write wundo wviminfo       
