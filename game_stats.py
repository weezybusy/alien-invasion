class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.read_hight_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def read_hight_score(self):
        """Read high score from the file."""
        try:
            with open("high_score.txt", 'r') as f:
                high_score = int(f.read().rstrip())
                self.high_score = high_score
        except FileNotFoundError:
            with open("high_score.txt", 'w') as f:
                pass
            self.high_score = 0
