class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""

        # FPS settings.
        self.fps = 60

        # Screen settings.
        self.screen_width = 1366
        self.screen_height = 704
        self.bg_color = (33, 33, 33)

        # Ship settings.
        self.ship_speed = 5.0
        self.ship_width = 50
        self.ship_height = 50
        self.ship_limit = 1

        # Bullet settings.
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 204, 0)
        self.bullets_allowed = 3

        # Alien settings.
        self.alien_width = 50
        self.alien_height = 50
        self.alien_speed = 5.0
        self.fleet_drop_speed = 10
        # Fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Star settings.
        self.star_color = (255, 255, 255)
        # The higher is value the lower is star density.
        self.star_distance = 20
