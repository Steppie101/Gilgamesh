"""
Functions used for the 'Mesh checking' part.
"""

import os
import sys
import subprocess


def checkFoamVersion(checkVersion):
    """
    Verifies if the current OpenFOAM version matches the required version.

    Parameters
    ----------
    checkVersion : str
        The OpenFOAM version to check against, e.g., "v2306" or "4.1".

    Returns
    -------
    None
    """
    foamVersion = subprocess.check_output(
        "echo $WM_PROJECT_VERSION", shell=True, text=True
    ).strip()

    if "v" in checkVersion:
        checkVersion = "OpenFOAM " + checkVersion
    else:
        checkVersion = "Foam Extend v" + checkVersion
    if "v" in foamVersion:
        foamVersion = "OpenFOAM " + foamVersion
    else:
        foamVersion = "Foam Extend v" + foamVersion

    if checkVersion != foamVersion:
        checkContinuing(
            "This program is written for "
            + checkVersion
            + ", but you have "
            + foamVersion
            + ". Do you want to continue?"
        )
    return


def runFoamCommand(
    foamCommand,
    arguments="",
    region="",
    regionOnlyLogFile=False,
    addToLogFilename="",
    beforeCommand="",
):
    """
    Executes an OpenFOAM command, optionally for a specific region, and logs the output to a file.

    Parameters
    ----------
    foamCommand : str
        The OpenFOAM command to execute.
    arguments : str, optional
        Additional arguments to pass to the command. Default is "".
    region : str, optional
        The region to apply the command to. Default is "" (no region).
    regionOnlyLogFile : bool, optional
        Whether the region-specific log file should be used without adding region to command. Default is False.
    addToLogFilename : str, optional
        Additional string to append to the log filename. Default is "".
    beforeCommand: str, optional
        Additional command before foamCommand. Default is "".

    Returns
    -------
    None
    """
    logFileName = "log." + foamCommand + addToLogFilename

    if beforeCommand != "":
        command = beforeCommand + " "
    else:
        command = ""

    command += foamCommand + " " + arguments

    if region != "":
        logFileName += "." + region
        print("Running " + foamCommand + " on region " + region)

        if not regionOnlyLogFile:
            command += " -region " + region
    else:
        print("Running " + foamCommand)

    if os.path.exists(logFileName):
        print(foamCommand + " already run. Remove " + logFileName + " to run.")
        return

    runCommand(command + " 1>" + logFileName + " 2>&1 | tee -a " + logFileName)


def runCommand(command, showWarnings=True):
    """
    Executes a shell command, suppressing standard output by default. Optionally suppresses error output.

    Parameters
    ----------
    command : str
        The shell command to be executed.
    showWarnings : bool, optional
        If False, suppresses both standard output and error messages. The default is True.

    Returns
    -------
    None
    """
    if ">" not in command:
        if showWarnings:
            command += " > /dev/null"
        else:
            command += " > /dev/null 2>&1"
    os.system(command)


def checkContinuing(question):
    """
    Asks the user a yes/no question and continues or exits.

    Parameters
    ----------
    question : str
        The question to ask the user, expecting a yes or no response.

    Returns
    -------
    None
    """
    print()
    if question[-1] != " ":
        question += " "

    response = input(question)
    if response.lower() in ["yes", "y"]:
        print("Continuing...")
        print()
    else:
        print("Exiting...")
        print()
        sys.exit(0)
