"""
Binary viewer - Made in Pygame
Created by Sheepy0125
24/09/2021
"""

#############
### Setup ###
#############
# Import
from setup_program import CONFIG, pygame, window, clock
from tools import Logger, check_running_by_self
from pygame_tools import Text, Button, DummyObject


###############
### Classes ###
###############
class BinaryInputParent:
    minimum_size_per_input: int = 75
    margin: int = 40
    y_value: int = 100


class BinaryInput(BinaryInputParent):
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
        """Create text to display the value"""

        self.input_text: Text = Text(
            str(self.value), pos=self.pos, size=24, color="black"
        )
        self.text_needs_update: bool = False

    def check_pressed(self) -> bool:
        """Check if the input has been flipped"""

        if self.input_button.check_pressed():
            self.value = int(not bool(self.value))  # Yeah, why?
            self.create_text()
            self.input_button.button_rect.color = (
                "green" if bool(self.value) else "white"
            )
            return True

        return False

    def draw(self) -> None:
        """Draw things needed for binary input"""

        # Text needs to be updated
        if self.text_needs_update:
            self.create_text()

        self.input_button.draw()
        self.input_text.draw()


class AllBinaryInputs(BinaryInputParent):
    """Creates and handles all binary inputs"""

    def __init__(self, number_of_inputs: int, initial_value: int = 0) -> None:
        self.number_of_inputs: int = number_of_inputs
        self.converted_number: int = 0
        self.create_all_inputs()
        self.set_all_inputs(0)
        self.create_output_text(f"{initial_value}")

    def create_all_inputs(self) -> None:
        """Create the binary inputs, adds it to self.input_list"""

        if CONFIG["options"]["verbose"]:
            Logger.log("Creating all binary inputs")

        self.input_list: list = []

        # Get X values of binary inputs (discount CSS Flexbox)
        # Dear future me, I'm sorry
        starting_x_offset: int = (
            CONFIG["pygame"]["window_size"][0] // (self.number_of_inputs * 2)
            + self.margin
        )
        for input_number in range(self.number_of_inputs):
            x_offset: int = (
                (
                    (
                        CONFIG["pygame"]["window_size"][0] - (self.margin * 2)
                        if CONFIG["pygame"]["window_size"][0]
                        > self.minimum_size_per_input * self.number_of_inputs
                        else self.minimum_size_per_input * self.number_of_inputs
                    )
                    // self.number_of_inputs
                )
                * input_number
            ) + starting_x_offset

            self.input_list.append(BinaryInput(pos=(x_offset, self.y_value)))

            # Warning if the window size is too small, for fun you know!
            if (
                x_offset
                - (self.minimum_size_per_input // 2)
                + self.minimum_size_per_input
            ) > CONFIG["pygame"]["window_size"][0]:
                Logger.warn(
                    f"Binary input number {input_number + 1}'s placement is bigger "
                    + "than the window size, it'll appear off screen!"
                )

    def create_output_text(self, text) -> None:
        """Create output text"""

        self.output_text: Text = Text(
            text,
            pos=(CONFIG["pygame"]["window_size"][0] // 2, 250),
            size=24,
            color="black",
        )

    def set_all_inputs(self, value: int) -> None:
        """Set inputs globally to a single value"""

        if CONFIG["options"]["verbose"]:
            Logger.log(f"Setting all inputs to {value}")

        self.binary_digits: list = [
            0 for _ in range(self.number_of_inputs)
        ]  # using `*` can cause weird results

    def event_handling(self) -> None:
        """Event handling for the inputs"""

        for binary_input_idx in range(self.number_of_inputs):
            binary_input: BinaryInput = self.input_list[binary_input_idx]

            if binary_input.check_pressed():
                # Binary input was pressed, change list
                self.binary_digits[binary_input_idx] = binary_input.value

                # Realtime conversion
                if CONFIG["options"]["realtime_conversion"]:
                    self.convert()

    def convert(self) -> None:
        """Convert the inputs to a base 10 integer"""

        if CONFIG["options"]["verbose"]:
            Logger.log(f"Converting binary inputs: {self.binary_digits}")

        binary_digit_str: str = str(
            "".join([str(binary_digit) for binary_digit in self.binary_digits])
        )
        normalized_num: int = int(binary_digit_str, base=2)

        self.create_output_text(str(normalized_num))

    def draw_all_inputs(self) -> None:
        """Draw all the binary inputs"""

        for binary_input in self.input_list:
            binary_input.draw()

        self.output_text.draw()


############
### Menu ###
############
def menu() -> None:
    """Menu page"""

    if CONFIG["options"]["verbose"]:
        Logger.log("Running menu()!")

    # All binary inputs
    all_binary_inputs: AllBinaryInputs = AllBinaryInputs(
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
    ]

    if not CONFIG["options"]["realtime_conversion"]:
        convert_button: Button = Button(
            pos=(center_x, CONFIG["pygame"]["window_size"][1] - 100),
            size=(300, 50),
            color="red",
        )
        texts.append(
            Text(
                "Convert",
                pos=(center_x, CONFIG["pygame"]["window_size"][1] - 100),
                size=12,
            )
        )
    else:
        convert_button: DummyObject = DummyObject()

    # Main loop
    running: bool = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Start drawing

        # Background
        window.fill("gray")

        # Binary inputs
        all_binary_inputs.draw_all_inputs()
        all_binary_inputs.event_handling()

        # Buttons
        convert_button.draw()
        if convert_button.check_pressed():
            all_binary_inputs.convert()

        # Widgets (draw on top of buttons for there are text widgets)
        for widget in texts:
            widget.draw()

        # Finished drawing, update
        pygame.display.flip()
        clock.tick(CONFIG["pygame"]["fps"])


###########
### Run ###
###########
if check_running_by_self(
    __name__, __file__, supposed_to=True, verbose=CONFIG["options"]["verbose"]
):
    menu()
