"""
Binary viewer - Made in Pygame
Created by Sheepy0125
24/09/2021
"""

#############
### Setup ###
#############
# Import
from setup import CONFIG, pygame, window, clock
from tools import Logger, check_running_by_self
from pygame_tools import Text, Button


###############
### Classes ###
###############
class BinaryInput:
    """A binary input, accepts 0 and 1"""

    def __init__(self, position: tuple, default_value: int = 0):
        self.x = position[0]
        self.y = position[1]
        self.value = default_value

    def update():
        """Show the input"""
        pass


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
    center_x: int = CONFIG["pygame"]["window_size"][0] // 2

    menu_widgets: list = [
        Text(
            "Binary Viewer - Created by Sheepy",
            text_pos=(center_x, 50),
            font_size=16,
            font_color="blue",
        ),
        Button(
            button_pos=(center_x, 150), button_size=(300, 50), button_text="Convert"
        ),
    ]

    while True:
        window.fill("gray")

        for widget in menu_widgets:
            widget.draw()

        pygame.display.flip()
        clock.tick(CONFIG["pygame"]["fps"])


###########
### Run ###
###########
if check_running_by_self(__name__, __file__, supposed_to=True):
    main()
