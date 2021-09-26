"""
Binary viewer - Made in Pygame
Created by Sheepy0125
24/09/2021
"""

#############
### Setup ###
#############
# Import
import pygame
from json import load
from tools import Logger

# Configuration
with open("config.json") as config_file:
    CONFIG: dict = load(config_file)
del load

# Check if configuration is okay
try:
    assert (
        CONFIG["window_size"][0] >= 800 and CONFIG["window_size"][1] >= 600
    ) is not False, "Window size invalid! Must be 800x600 or more!"
    assert CONFIG["fps"] is int, "FPS must be a valid integer!"

except Exception as error:
    Logger.log_error(error)
    exit(1)

# Setup Pygame
pygame.display.set_caption("Binary Viewer - Created by Sheepy")
window: pygame.Surface = pygame.display.set_mode(CONFIG["window_size"])
clock = pygame.time.Clock()
pygame.init()

###############
### Classes ###
###############
class BinaryInput:
    """A binary input, accepts 0 and 1"""

    def __init__(self, position: tuple, default_value: int = 0):
        self.x = position[0]
        self.y = position[1]
        self.value = default_value


class AllBinaryInputs:
    """Creates and handles all binary inputs"""

    def __init__(self, screen_size: tuple, number_of_inputs: int) -> None:
        self.input_list: list = [BinaryInput() for _ in range(number_of_inputs)]

    def set_all_inputs(value: int) -> None:
        raise NotImplemented
        for input in number_of_inputs:
            input.value = value
            input.update()


############
### Main ###
############
def main():
    while True:
        window.fill("gray")

        pygame.display.flip()
        clock.tick(CONFIG["fps"])


###########
### Run ###
###########
if __name__ == "__main__":
    main()
