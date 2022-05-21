class Image:
    """Describe an image for a game."""

    def __init__(self, ai_game, img_name, pos=(0,0)):
        """Initialize image attributes."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.img_folder('images')
        self.img_name = img_name
        self.img = pygame.img.load(img_folder + '/' + img_name)
        self.img_width = self.img.get_width()
        self.img_height = self.img.get_height()
        self.size = (slef.img_width, self.img_height)
        self.img = pygame.transform.scale(self.img, size)
        self.img_rect = self.img.get_rect()

        # Position image.
        self.pos = pos
        self.rect

    def blitme(self):
        """Draw the image at its current location."""
        self.screen.blit(self.img, self.rect)
