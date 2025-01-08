import os


def runCommand(command, showWarnings=True):
    if ">" not in command:
        if showWarnings:
            command += " > /dev/null"
        else:
            command += " > /dev/null 2>&1"
    os.system(command)
