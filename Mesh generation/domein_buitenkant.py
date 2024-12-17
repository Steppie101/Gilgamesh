#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:15:33 2024

@author: rubenmuijt
"""

import pygalmesh as pm
import numpy as np
import meshio
import time
import trimesh
t0 = time.time()

mesh = trimesh.load("eersteversie.stl")

vertices = mesh.vertices
faces = mesh.faces

mesh1 = meshio.read("eersteversie.stl")

#block_mesh
nodes = mesh1.points
nodesT = nodes.T
xmax = max(nodesT[0])
xmin = min(nodesT[0])
ymax = max(nodesT[1]) 
ymin = min(nodesT[1])
zmax = max(nodesT[2])
zmin = min(nodesT[2])

factor = 1.01
rx = xmax-xmin
ry = ymax-ymin
rz = zmax-zmin
xgem = (xmax+xmin)/2
ygem = (ymax+ymin)/2
zgem = (zmax+zmin)/2
cube  = pm.Cuboid([xgem-factor*rx,ygem-factor*ry,zgem-factor*rz],[xgem+factor*rx,ygem+factor*ry,zgem+factor*rz])
cube2 = pm.Cuboid([xgem-factor/rx,ygem-factor/ry,zgem-factor/rz],[xgem+factor/rx,ygem+factor/ry,zgem+factor/rz])
inside = pm.Difference(cube,cube2)