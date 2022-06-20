import sys
from time import sleep
from random import randint

import pygame

from game_stats import GameStats
from alien import Alien
from bullet import Bullet
from settings import Settings
from ship import Ship
from star import Star
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.settings.screen_width = self.screen_rect.width
        self.settings.screen_height = self.screen_rect.height
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.stars = pygame.sprite.Group()
        self._create_stars()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "PLAY")
        self.sb = Scoreboard(self)
        self._make_difficulty_buttons()

    def _make_difficulty_buttons(self):
        """Make difficulty buttons."""
        self.easy_button = Button(self, "EASY")
        self.normal_button = Button(self, "NORMAL")
        self.hard_button = Button(self, "HARD")

        self.easy_button.rect.top = (
                self.play_button.rect.top + 1.5 * self.play_button.height)
        self.easy_button._update_msg_position()
        self.normal_button.rect.top = (
                self.easy_button.rect.top + 1.5 * self.easy_button.height)
        self.normal_button._update_msg_position()
        self.hard_button.rect.top = (
                self.normal_button.rect.top + 1.5 * self.normal_button.height)
        self.hard_button._update_msg_position()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    def _save_high_score(self):
        """Save high score to the file."""
        with open("high_score.txt", 'w') as f:
            f.write(str(self.stats.high_score))

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _check_difficulty_buttons(self, mouse_pos):
        """Set mode to easy when the player clicks EASY."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        normal_button_clicked = self.normal_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if easy_button_clicked:
            self.settings.difficulty = "easy"
        elif normal_button_clicked:
            self.settings.difficulty = "normal"
        elif hard_button_clicked:
            self.settings.difficulty = "hard"

    def _start_game(self):
        """Reset stats, fleet, ship, remove cursor, set game to active."""
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_q:
            self._exit_game()
        elif event.key == pygame.K_LEFT or event.key == pygame.K_j:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_l:
            self.ship.moving_right = True
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _exit_game(self):
        """Save high score and exit game."""
        self._save_high_score()
        sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_LEFT or event.key == pygame.K_j:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_l:
            self.ship.moving_right = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of the bullets and get rid of the old ones."""
        self.bullets.update()
        # Get rid of bullets that have desappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self._start_new_level()

    def _start_new_level(self):
        """
        Remove existing bullets, create new fleet, increase speed,
        increment level, and prepeare a new level text image.
        """
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()

    def _update_aliens(self):
        """
        Check if the fleet is at the edge,
        then update the position of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to a ship being hit by the alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining aliens.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any alien have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            screen_rect = self.screen.get_rect()
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien_width = self.settings.alien_width
        alien_height = self.settings.alien_width
        # Determine the number of aliens that fit on the screen.
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # Determine the number of rows of aliens that fit on the screen.
        screen_height = self.settings.screen_height
        ship_height = self.settings.ship_height
        available_space_y = screen_height - ship_height - (3 * alien_height)
        number_rows = available_space_y // (2 * alien_height)
        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien."""
        alien = Alien(self)
        alien_width = self.settings.alien_width
        alien_height = self.settings.alien_height
        alien.x = alien_width + (2 * alien_width) * alien_number
        alien.y = alien_height + (2 * alien_height) * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any alien have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_stars(self):
        """Create stars."""
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height
        star_distance = self.settings.star_distance
        # Calculate number of stars that fit on the screen in x direction.
        number_stars_x = screen_width // star_distance
        # Calculate number of stars that fit on the screen in y direction.
        number_stars_y = screen_height // star_distance
        for star_number_y in range(number_stars_y):
            for star_number_x in range(number_stars_x):
                if self._star_exists():
                    self._create_star(star_number_x, star_number_y)

    def _create_star(self, star_number_x, star_number_y):
        """Create a star."""
        star = Star(self)
        star_distance = self.settings.star_distance
        star.x = randint(-10, 10)
        star.y = randint(-10, 10)
        star.rect.x = star_distance + (star_distance * star_number_x) + star.x
        star.rect.y = star_distance + (star_distance * star_number_y) + star.y
        self.stars.add(star)

    def _star_exists(self):
        """Return True if star exists and False otherwise."""
        if randint(0, 1):
            return True
        return False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.clock.tick(self.settings.fps)
        self.screen.fill(self.settings.bg_color)
        for star in self.stars.sprites():
            star.draw_star()
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
