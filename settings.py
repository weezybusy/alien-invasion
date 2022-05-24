class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings.
        self.screen_width = 1366
        self.screen_height = 704
        self.bg_color = (33, 33, 33)

        # Ship settings.
        self.ship_speed = 1.5

        # Bullet settings.
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (102, 153, 204)
