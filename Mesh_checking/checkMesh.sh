#!/bin/bash
openfoam2406 && vtkUnstructuredToFoam rectangle.vtk
checkMesh -allGeometry -allRegions -allTopology
