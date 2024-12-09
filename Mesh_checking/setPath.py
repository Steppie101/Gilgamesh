import os


path = os.path.dirname(os.path.relpath(__file__))
if "C:/" in path:
    path = (path.split("C:/"))[-1]
    path = "/mnt/c/" + path

os.chdir(path)
