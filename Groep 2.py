import pygalmesh as pm
import numpy as np
import meshio
import time
t0 = time.time()
    
mesh = meshio.read("eersteversie.stl")


"""informatie over de aangeleverde mesh"""
print(mesh)
nodes = mesh.points
triangles = mesh.cells_dict.get("triangle",None)

if triangles is None:
    raise ValueError("no triangl cells found in the STL file")

nodesT = nodes.T
xmax = max(nodesT[0])
xmin = min(nodesT[0])
ymax = max(nodesT[1]) #met hulp van Marieke Bosch
ymin = min(nodesT[1])
zmax = max(nodesT[2])
zmin = min(nodesT[2])


"""Genereren van een refined surface mesh"""
def SurfaceMesh():
    #alleen gebruiken wanneer de mesh niet goed genoeg is. 
    #Deze functie refinet de al bestaande surfacemesh.
    mesh = pm.remesh_surface(
        "eersteversie.stl",
        max_edge_size_at_feature_edges=0.00015,
        min_facet_angle=25.0,
        max_radius_surface_delaunay_ball=0.00015,
        max_facet_distance=0.000008,
        verbose=False)
    mesh.write("refined_surface_mesh.stl")
    return mesh

#surfacemesh = SurfaceMesh()
#print(surfacemesh)
#surfacemesh.write("surfacemesh.stl")


"""Genereren van een volume mesh van de binnenkant"""
def VolumeMesh():
    #deze functie creëert een volumemesh van een surfacemesh.
    #check voor je deze functie gebruikt of de surfacemesh nog gerefined moet worden.
    mesh = pm.generate_volume_mesh_from_surface_mesh(
        "eersteversie.stl",
        min_facet_angle=25.0, #dit is met een afwijking van 65% terwijl sebastiaan normaal 40% gebruikt.
        max_radius_surface_delaunay_ball=0.0015,
        max_facet_distance=0.000008,
        max_circumradius_edge_ratio=3.0,
        verbose=True,)
    return mesh

#volumemesh = VolumeMesh()
#volumenodes = volumemesh.points
#volumetriangles = volumemesh.cells_dict.get("triangle",None)
#vulumetetras = volumemesh.cells_dict.get("tetra",None)
#print (volumemesh)
# volumemesh.write("volumemesh.vtk")

"""Genereren van een surface en volume mesh van de buitenkant"""
def boxmesh():
    #deze functie creeërt een box om de ballen heen. De functie werkt.
    #de hoekpunten zijn niet gerefined maar ik weet niet of dat nodig is.
    cube = pm.Cuboid([xmin,ymin,zmin],[xmax,ymax,zmax])
    cubemesh = pm.generate_surface_mesh(
        domain=cube,
        min_facet_angle=25.0,
        max_radius_surface_delaunay_ball=0.00008,
        max_facet_distance=0.00008,)
    return cubemesh

#cubemesh = boxmesh()
#print(cubemesh)
#cubemesh.write("cubemesh312.stl")

def volboxmesh():
    #deze functie maakt een volumemesh van de surfacemesh van de kubus. De functie werkt.
    #Het is nog niet gelukt om een uniforme cellsize te krijgen.
    mesh = pm.generate_volume_mesh_from_surface_mesh(
        "cubemesh312.stl",
        min_facet_angle=25.0, #dit is met een afwijking van 65% terwijl sebastiaan normaal 40% gebruikt.
        max_radius_surface_delaunay_ball=0.0015,
        max_facet_distance=0.00003,
        max_circumradius_edge_ratio=4.0,
        max_cell_circumradius=0.0001, #deze parameter maakt de mesh uniform
        verbose=True,)
    return mesh

volcubemesh = volboxmesh()
volcubemesh.write("volcubemesh312.vtk")

"""Samenvoegen van de oppervlakten"""
def cojoinedmesh():
    #het plan was om in deze functie de domeinen samen te voegen maar dat wilde nog niet lukken.
    #in de functie "samen" is het wel gelukt om de meshes samen te voegen. Ik weet alleen niet of dat mag.
    cube = pm.Cuboid([xmin,ymin,zmin],[xmax,ymax,zmax])
    allnodes = pm.Union(cube,nodes)
    mesh = pm.generate_mesh(allnodes, max_cell_circumradius=0.0015, max_edge_size_at_feature_edges=0.0015,odt=True, lloyd=True, verbose=False)
    return mesh

# combinedmesh = cojoinedmesh()
# print(combinedmesh)

def samen(cubemesh):
    #ik weet nog niet of deze functie werkt
    combinedpoints = np.vstack([cubemesh.points,mesh.points]) #hier voeg ik de punten samen
    offset = len(mesh.points) #vanaf hier ga wijzig ik de nummers die de punten hebben
    adjustedcells = []
    for cellblock in cubemesh.cells:
        celltype = cellblock.type
        adjusteddata = cellblock.data + offset
        adjustedcells.append((celltype,adjusteddata))
    combinedcells = mesh.cells + adjustedcells #hier combineer ik de cellen van beide meshes
    combinedmesh = meshio.Mesh(points=combinedpoints, cells= combinedcells) #hier creeër ik de nieuwe mesh
    return combinedmesh

#combinedmesh = samen(cubemesh)
#print(combinedmesh)
#combinedmesh.write("combined312.stl")
t1 = time.time()
print("Elapsed time =",t1-t0)
