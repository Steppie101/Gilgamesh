import subprocess
import os

# Path to your OpenFOAM environment setup script
# openfoam_dir = '/opt/openfoam2406'  # Adjust this path if needed

# Command to source OpenFOAM environment and run the desired commands
command = "openfoam2406; vtkUnstructuredToFoam rectangle.vtk"

# Run the command in an interactive shell
try:
    result = subprocess.run(
        command, shell=True, check=True, capture_output=True, text=True
    )
    print("Output:", result.stdout)
    print("Errors:", result.stderr)
except subprocess.CalledProcessError as e:
    print(f"Error running command: {e}")
