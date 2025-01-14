"""
Functions used for the 'Mesh checking' part.
"""

import os
import sys


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
            command += ""  # > /dev/null"
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
    response = input(question)
    if response.lower() in ["yes", "y"]:
        print("Continuing...")
    else:
        print("Exiting...")
        sys.exit(0)
