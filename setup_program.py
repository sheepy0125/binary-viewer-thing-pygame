"""
Setup Program
Created by Sheepy0125
26/09/2021
"""

##############
### Import ###
##############

# Don't allow to be run by self
from tools import check_running_by_self

if check_running_by_self(__name__, __file__):
    exit(1)
del check_running_by_self

from os import environ, getcwd
from os.path import exists

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "sure why not"
del environ

import pygame
from json import load
from tools import Logger

Logger.log(f"Hello there! CWD: {getcwd()}")
del getcwd

#####################
### Configuration ###
#####################
try:
    with open("config.json") as config_file:
        CONFIG: dict = load(config_file)
        Logger.log("Successfully loaded configuration!")
        del load

    try:
        # Map config
        CONFIG: dict = {
            "pygame": {
                "window_size": tuple(CONFIG["pygame"]["windowSize"]),
                "fps": int(CONFIG["pygame"]["fps"]),
            },
            "options": {
                "button_text_size": int(CONFIG["options"]["buttonTextSize"]),
                "verbose": bool(CONFIG["options"]["verbose"]),
                "number_of_binary_inputs": int(
                    CONFIG["options"]["numberOfBinaryInputs"]
                ),
            },
            "paths": {
                "font_path": CONFIG["paths"]["fontPath"],
                "button_img_path": CONFIG["paths"]["buttonImgPath"],
            },
        }

        Logger.log("Successfully mapped configuration!")

    except Exception as error:
        Logger.fatal(
            "Failed to map configuration!"
            + "Check and make sure all configuration variables exist."
        )
        Logger.log_error(error)
        exit(1)

except FileNotFoundError:
    Logger.fatal("Configuration file (config.json) not found in CWD!")
    exit(1)

####################
### Setup Pygame ###
####################
pygame.display.set_caption("Binary Viewer - Created by Sheepy")
window: pygame.Surface = pygame.display.set_mode(CONFIG["pygame"]["window_size"])
clock: pygame.time.Clock = pygame.time.Clock()
pygame.init()
