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
from pygame_tools import Text, Button, CenterRect


###############
### Classes ###
###############
class BinaryInput:
    """A binary input, accepts 0 and 1"""

    def __init__(self, pos: tuple, default_value: int = 0) -> None:
        self.pos = pos
        self.value: int = default_value

        # When the value is updated, the text needs to update too
        self.text_needs_update: bool = False

        # Create input
        self.input_rect: CenterRect = CenterRect(
            center_pos=pos, size=(50, 50), color="white"
        )
        self.create_text()

    def create_text(self) -> None:
        self.input_text: Text = Text(
            str(self.value), pos=self.pos, size=24, color="black"
        )
        self.text_needs_update: bool = False

    def draw(self) -> None:
        # Text needs to be updated
        if self.text_needs_update:
            self.create_text()

        self.input_rect.draw()
        self.input_text.draw()


class AllBinaryInputs:
    """Creates and handles all binary inputs"""

    def __init__(self, number_of_inputs: int) -> None:
        self.number_of_inputs: int = number_of_inputs
        self.create_all_inputs()

    def create_all_inputs(self) -> None:
        self.input_list: list = []

        minimum_size_per_input: int = 75
        margin: int = 40

        # Get X values of binary inputs
        starting_x_offset: int = (
            CONFIG["pygame"]["window_size"][0] // (self.number_of_inputs * 2) + margin
        )
        for input_number in range(self.number_of_inputs):
            x_offset: int = (
                (
                    (
                        CONFIG["pygame"]["window_size"][0] - (margin * 2)
                        if CONFIG["pygame"]["window_size"][0]
                        > minimum_size_per_input * self.number_of_inputs
                        else minimum_size_per_input * self.number_of_inputs
                    )
                    // self.number_of_inputs
                )
                * input_number
            ) + starting_x_offset
            self.input_list.append(BinaryInput(pos=(x_offset, 200)))

            if (
                x_offset - (minimum_size_per_input // 2) + minimum_size_per_input
            ) > CONFIG["pygame"]["window_size"][0]:
                Logger.warn(
                    f"Binary input number {input_number + 1}'s placement is bigger than the window size, it'll appear off screen!"
                )

    def set_all_inputs(self, value: int) -> None:
        for binary_input in self.input_list:
            binary_input.set(value)
            binary_input.update()

    def draw_all_inputs(self) -> None:
        for binary_input in self.input_list:
            binary_input.draw()


############
### Main ###
############
def main() -> None:
    # All binary inputs
    all_binary_inputs = AllBinaryInputs(
        number_of_inputs=CONFIG["options"]["number_of_binary_inputs"]
    )

    # Widgets
    center_x: int = CONFIG["pygame"]["window_size"][0] // 2
    widgets: list = [
        Text(
            "Binary Viewer - Created by Sheepy",
            pos=(center_x, 50),
            size=16,
            color="blue",
        ),
        Button(
            pos=(center_x, CONFIG["pygame"]["window_size"][1] - 100),
            size=(300, 50),
            color="red",
            on_click=lambda: all_binary_inputs.convert(),
        ),
        Text(
            "Convert",
            pos=(center_x, CONFIG["pygame"]["window_size"][1] - 100),
            size=12,
        ),
    ]

    while True:
        window.fill("gray")

        for widget in widgets:
            widget.draw()

        all_binary_inputs.draw_all_inputs()

        pygame.display.flip()
        clock.tick(CONFIG["pygame"]["fps"])


###########
### Run ###
###########
if check_running_by_self(__name__, __file__, supposed_to=True, verbose=True):
    main()
