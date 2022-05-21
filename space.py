import pygame

class Space:
    """Class to manage space background."""

    def __init__(self, ai_game):
        """Initialize space background and set its position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/space.bmp')
        size = (self.image.get_width()/2,
                self.image.get_height()/2)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

        self.rect.center = self.screen_rect.center

    def blitme(self):
        """Draw space at its current location."""
        self.screen.blit(self.image, self.rect)
