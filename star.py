import pygame
from pygame.sprite import Sprite
from random import randint


class Star(Sprite):
    """A Class representing a star."""

    def __init__(self, ai_game):
        """Initialize a star."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.star_color
        n = randint(0, 5)
        self.x = randint(0, self.settings.screen_width)
        self.y = randint(0, self.settings.screen_height)
        self.rect = pygame.Rect(self.x, self.y, n, n)

    def draw_star(self):
        """Draw a bullet."""
        pygame.draw.rect(self.screen, self.color, self.rect)
