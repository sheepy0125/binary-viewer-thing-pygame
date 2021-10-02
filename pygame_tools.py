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
        pos: tuple,
        size: int,
        color: Union[str, tuple] = "white",
    ) -> None:
        # Create text
        self.text_surf: Surface = pygame.font.Font(
            CONFIG["paths"]["font_path"], size
        ).render(text_to_display, True, color)
        self.text_rect: pygame.Rect = self.text_surf.get_rect(center=pos)

    def draw(self):
        window.blit(self.text_surf, self.text_rect)


class Button:
    """Display a button for Pygame"""

    def __init__(
        self,
        pos: tuple,
        size: tuple,
        color: Union[str, tuple] = "white",
    ) -> None:
        self.button_pos: tuple = pos
        self.button_size: tuple = size
        self.button_color: Union[str, tuple] = color

        # Check if button size is too big (for fun you know)
        if self.button_size > CONFIG["pygame"]["window_size"]:
            Logger.warn(
                "Button size exceeds window size "
                + f"({size} vs. {CONFIG['pygame']['window_size']})!"
            )

        self.button_rect: CenterRect = CenterRect(
            pos=self.button_pos, size=self.button_size, color=self.button_color
        )

        # Cooldown stuff
        self.button_cooldown_time_over: int = 0
        self.button_cooldown_time_ms: int = 100

    def check_pressed(self) -> bool:
        """Check if the button was pressed"""

        mouse_pos: tuple = pygame.mouse.get_pos()
        mouse_click: tuple = pygame.mouse.get_pressed()

        cooldown_over: bool = self.button_cooldown_time_over <= pygame.time.get_ticks()

        if (
            self.button_rect.rect.collidepoint(mouse_pos)
            and mouse_click[0]
            and cooldown_over
        ):
            self.button_cooldown_time_over = (
                pygame.time.get_ticks() + self.button_cooldown_time_ms
            )

            return True

        return False

    def draw(self) -> None:
        self.button_rect.draw()


class CenterRect:
    """A Pygame rectangle, but it is centered. Don't ask"""

    def __init__(
        self, pos: tuple, size: tuple, color: Union[str, tuple] = "white"
    ) -> None:
        self.center_pos: tuple = pos
        self.size: tuple = size
        self.color: Union[str, tuple] = color

        # Get center position -> left / top positions
        self.left: int = self.center_pos[0] - (self.size[0] * 0.5)
        self.top: int = self.center_pos[1] - (self.size[1] * 0.5)

        # Create rectangle
        self.rect: pygame.Rect = pygame.Rect(self.left, self.top, *self.size)

    def draw(self) -> None:
        pygame.draw.rect(window, self.color, self.rect)
