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
        self.side_size = randint(1, 2)
        self.rect = pygame.Rect(0, 0, self.side_size, self.side_size)

    def draw_star(self):
        """Draw a star."""
        pygame.draw.rect(self.screen, self.color, self.rect)
