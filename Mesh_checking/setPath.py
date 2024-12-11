"""Set working directory to the directory of this file."""

import os


path = os.path.dirname(os.path.relpath(__file__))

# Adjustment for WSL
if "C:/" in path:
    path = (path.split("C:/"))[-1]
    path = "/mnt/c/" + path

os.chdir(path)
