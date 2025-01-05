from .asset_helper import get_asset_path
from .circleshape import *
from .constants import *

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.original_image = pygame.image.load(get_asset_path("ship_laser3.jpg"))
        self.scale_factor = 0.95
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scale_factor), int(self.original_image.get_height() * self.scale_factor)))
        self.rect = self.image.get_rect(center = self.position)
       
    def draw(self, screen):
        #pygame.draw.circle(screen, (140, 43, 41), self.position, self.radius)
        rotated_image = pygame.transform.rotate(self.image, -self.radius)
        image_rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, image_rect.topleft)

    def update(self, dt):
        self.position += (self.velocity * 1.25) * dt