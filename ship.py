import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image, set its size, and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        # Size depends on the original image size.
        size = (self.image.get_width()/30,
                self.image.get_height()/30)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag.
        self.moving_left = False
        self.moving_right = False

    def update(self):
        """Update ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_left:
            self.x -= self.settings.ship_speed
        if self.moving_right:
            self.x += self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = round(self.x)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
