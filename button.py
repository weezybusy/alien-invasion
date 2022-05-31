import pygame.font


class Button:
    """A class that respresents a button."""

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimentions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (200, 200, 200)
        self.text_color = (33, 33, 33)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button.color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
