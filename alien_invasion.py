import sys

import pygame

from random import randint

from alien import Alien
from bullet import Bullet
from settings import Settings
from ship import Ship
from star import Star


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stars = pygame.sprite.Group()
        self._create_stars()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.clock.tick(self.settings.fps)
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_LEFT or event.key == pygame.K_j:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_l:
            self.ship.moving_right = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

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

        # Check for any bullets that have hit the aliens.
        # If so, get rid of the bullet and the the alien.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

    def _update_aliens(self):
        """
        Check if the fleet is at the edge,
        then update the position of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

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
        self.screen.fill(self.settings.bg_color)
        for star in self.stars.sprites():
            star.draw_star()
        self.aliens.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
