"""
Tools for Binary Viewer
Created by sheepy0125
25/09/2021
"""
#############
### Setup ###
#############
from os import getcwd
from os.path import basename

###############
### Classes ###
###############
class Logger:
    """A class for logging messages."""

    colors: dict = {
        "log": "\033[92m",
        "warn": "\033[93m",
        "fatal": "\033[91m",
        "normal": "\033[0m",
    }

    @staticmethod
    def log(message: str) -> None:
        print(f"{Logger.colors['log']}[INFO] {message}{Logger.colors['normal']}")

    @staticmethod
    def warn(message: str) -> None:
        print(f"{Logger.colors['warn']}[WARN] {message}{Logger.colors['normal']}")

    @staticmethod
    def fatal(message: str) -> None:
        print(f"{Logger.colors['fatal']}[FAIL] {message}{Logger.colors['normal']}")

    @staticmethod
    def log_error(error: Exception) -> None:
        Logger.fatal(
            f"{type(error).__name__}: {str(error)} (line {error.__traceback__.tb_lineno})"
        )


#################
### Functions ###
#################
def check_running_by_self(
    dunder_name: str,
    dunder_file: str,
    supposed_to: bool = False,
    verbose: bool = False,
) -> None:
    if dunder_name == "__main__":
        if supposed_to:
            if verbose:
                Logger.log(
                    f"{basename(dunder_file)} is being run by itself, that's good"
                )
        else:
            Logger.warn(f"{basename(dunder_file)} is being run by itself!")

        return True

    if supposed_to:
        Logger.warn(f"{basename(dunder_file)} isn't being run by itself!")
    else:
        if verbose:
            Logger.log(
                f"{basename(dunder_file)} isn't being run by itself, that's good"
            )

    return False
