"""
Pygame tools for Binary Viewer
Created by sheepy0125
26/09/2021
"""

# Don't allow to be run by self
from tools import check_running_by_self

if check_running_by_self(__name__, __file__):
    exit(1)
del check_running_by_self

#############
### Setup ###
#############
# Import
from setup import CONFIG, pygame, window
from tools import Logger
from typing import Union

###############
### Classes ###
###############
class Text:
    """Display text for Pygame"""

    def __init__(
        self,
        text_to_display: str,
        text_pos: tuple,
        font_size: int,
        font_color: Union[str, tuple] = "white",
    ) -> None:
        # Create text
        self.text_surf: Surface = pygame.font.Font(
            CONFIG["paths"]["font_path"], font_size
        ).render(text_to_display, True, font_color)
        self.text_rect: pygame.Rect = self.text_surf.get_rect(center=text_pos)

    def draw(self):
        window.blit(self.text_surf, self.text_rect)


class Button:
    """Display a button for Pygame"""

    def __init__(
        self, button_pos: tuple, button_size: tuple, button_text: Union[str, None]
    ) -> None:
        # Check if button size is too big (for fun you know)
        if button_size > CONFIG["pygame"]["window_size"]:
            Logger.warn(
                f"Button size exceeds window size ({button_size} vs. {window_size})!"
            )

        self.button_surf: pygame.Surface = pygame.image.load(
            CONFIG["paths"]["button_img_path"]
        ).convert_alpha()
        self.button_surf: pygame.Surface = pygame.transform.scale(
            self.button_surf, button_size
        )
        self.button_rect: pygame.Rect = self.button_surf.get_rect(center=button_pos)

        # Button text (if desired)
        self.button_text = None
        if button_text:
            self.button_text: Text = Text(
                button_text, button_pos, CONFIG["options"]["button_text_size"]
            )

    def check_pressed(self) -> bool:
        mouse_pos: tuple = pygame.mouse.get_pos()
        mouse_click: tuple = pygame.mouse.get_pressed()

        cooldown_over: bool = self.button_cooldown_time <= pygame.time.get_ticks()

        if (
            self.button_rect.collidepoint(mouse_pos)
            and mouse_click[0]
            and cooldown_over
        ):
            self.button_cooldown_time = (
                pygame.time.get_ticks() + self.button_cooldown_time_ms
            )
            return True

        return False

    def draw(self) -> None:
        # Draw!
        window.blit(self.button_surf, self.button_rect)

        # Draw text if desired
        if self.button_text is not None:
            self.button_text.draw()
