import os


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
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 3

        # Alien settings.
        self.alien_width = 50
        self.alien_height = 50
        self.fleet_drop_speed = 10

        # Star settings.
        self.star_color = (255, 255, 255)
        self.star_distance = 20

        # How quickly the game speeds up.
        self.speedup_scale = 1.1

        # How quickly the alien point values increase.
        self.score_scale = 1.5

        # Paths to images.
        self.alien_image = os.path.join('images', 'alien.bmp')
        self.ship_image = os.path.join('images', 'ship.bmp')

        # Paths to sound and music files.
        self.background_music = os.path.join('sounds', 'background_music.mp3')
        self.bullet_sound = os.path.join('sounds', 'bullet_sound.mp3')
        self.collision_sound = os.path.join('sounds', 'collision_sound.mp3')

        self.difficulty = "normal"
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        if self.difficulty == "easy":
            self.ship_limit = 5
            self.bullets_allowed = 10
            self.ship_speed = 2
            self.bullet_speed = 3
            self.alien_speed = 0.5
        elif self.difficulty == "normal":
            self.ship_limit = 3
            self.bullets_allowed = 3
            self.ship_speed = 2
            self.bullet_speed = 3.0
            self.alien_speed = 1.0
        elif self.difficulty == "hard":
            self.ship_limit = 1
            self.bullets_allowed = 50 # originally 3
            self.ship_speed = 3.0
            self.bullet_speed = 6.0
            self.alien_speed = 2.0
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
