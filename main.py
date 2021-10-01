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
        if CONFIG["options"]["verbose"]:
            Logger.log("Creating binary input!")

        self.pos: tuple = pos
        self.value: int = default_value

        # When the value is updated, the text needs to update too
        self.text_needs_update: bool = False

        # Create input
        self.input_button: Button = Button(pos=pos, size=(50, 50), color="white")
        self.create_text()

    def create_text(self) -> None:
        self.input_text: Text = Text(
            str(self.value), pos=self.pos, size=24, color="black"
        )
        self.text_needs_update: bool = False

    def check_pressed(self) -> None:
        if self.input_button.check_pressed():
            self.value = int(not bool(self.value))
            self.create_text()
            self.input_button.button_rect.color = (
                "green" if bool(self.value) else "white"
            )

    def draw(self) -> None:
        # Text needs to be updated
        if self.text_needs_update:
            self.create_text()

        self.input_button.draw()
        self.input_text.draw()


class AllBinaryInputs:
    """Creates and handles all binary inputs"""

    def __init__(self, number_of_inputs: int) -> None:
        # TODO - use the config V
        self.number_of_inputs: int = number_of_inputs
        self.create_all_inputs()
        self.set_all_inputs(0)
        self.output_text: Text = Text(
            f"{[digit for digit in self.binary_digits]}", pos=(0, 0), size=12
        )

    def create_all_inputs(self) -> None:
        if CONFIG["options"]["verbose"]:
            Logger.log("Creating all binary inputs")

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
                    f"Binary input number {input_number + 1}'s placement is bigger "
                    + "than the window size, it'll appear off screen!"
                )

    def set_all_inputs(self, value: int) -> None:
        if CONFIG["options"]["verbose"]:
            Logger.log(f"Setting all inputs to {value}")

        self.binary_digits = [
            0 for _ in range(self.number_of_inputs)
        ]  # using `*` can cause weird results

        for binary_input in self.input_list:
            continue
            binary_input.set(value)
            binary_input.update()

    def event_handling(self) -> None:
        for binary_input in self.input_list:
            binary_input.check_pressed()

    def convert(self) -> None:
        if CONFIG["options"]["verbose"]:
            Logger.log(f"Converting binary inputs: {binary_digits}")

    def draw_all_inputs(self) -> None:
        for binary_input in self.input_list:
            binary_input.draw()


############
### Main ###
############
def main() -> None:
    if CONFIG["options"]["verbose"]:
        Logger.log("Running main()!")

    # All binary inputs
    all_binary_inputs = AllBinaryInputs(
        number_of_inputs=CONFIG["options"]["number_of_binary_inputs"]
    )

    # Widgets
    center_x: int = CONFIG["pygame"]["window_size"][0] // 2
    texts: list = [
        Text(
            "Binary Viewer - Created by Sheepy",
            pos=(center_x, 50),
            size=16,
            color="blue",
        ),
        Text(
            "Convert",
            pos=(center_x, CONFIG["pygame"]["window_size"][1] - 100),
            size=12,
        ),
    ]
    convert_button: Button = Button(
        pos=(center_x, CONFIG["pygame"]["window_size"][1] - 100),
        size=(300, 50),
        color="red",
    )

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill("gray")

        convert_button.draw()
        if convert_button.check_pressed():
            Logger.log("Converting inputs!")

        for widget in texts:
            widget.draw()

        all_binary_inputs.draw_all_inputs()
        all_binary_inputs.event_handling()

        pygame.display.flip()
        clock.tick(CONFIG["pygame"]["fps"])


###########
### Run ###
###########
if check_running_by_self(__name__, __file__, supposed_to=True, verbose=True):
    main()
