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
        self.ship_width = 50
        self.ship_height = 50
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 204, 0)
        self.bullets_allowed = 3

        # Alien settings.
        self.alien_width = 50
        self.alien_height = 50
        self.fleet_drop_speed = 10

        # Star settings.
        self.star_color = (255, 255, 255)
        self.star_distance = 20

        self.difficulty = "normal"

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        if self.difficulty == "easy":
            self.ship_limit = 5
            self.bullets_allowed = 10
            self.ship_speed = 0.75
            self.bullet_speed = 1.5
            self.alien_speed = 0.5
        elif self.difficulty == "normal":
            self.ship_limit = 3
            self.bullets_allowed = 3
            self.ship_speed = 1.5
            self.bullet_speed = 3.0
            self.alien_speed = 1.0
        elif self.difficulty == "hard":
            self.ship_limit = 2
            self.bullets_allowed = 3
            self.ship_speed = 3.0
            self.bullet_speed = 6.0
            self.alien_speed = 2.0
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
