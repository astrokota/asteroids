import pygame
import random
from .circleshape import *
from .constants import *
from .asset_helper import get_asset_path

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.color_r = random.uniform(50, 255)
        self.color_g = random.uniform(50, 255)
        self.color_b = random.uniform(50, 255)
        
        self.killed_at = None
        self.killed_image = pygame.image.load(get_asset_path("cod_hitmarker.png"))
        self.killed_image = pygame.transform.scale(self.killed_image, (100, 100))

        self.original_image = pygame.image.load(get_asset_path("asteroid_rock.png"))
        self.scale_factor = self.radius / ASTEROID_BASE_RADIUS
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scale_factor), int(self.original_image.get_height() * self.scale_factor)))
        self.rect = self.image.get_rect(center = self.position)

    def draw(self, screen):
        if not self.killed_at:
            rotated_image = pygame.transform.rotate(self.image, -self.radius)
            image_rect = rotated_image.get_rect(center=self.position)
            screen.blit(rotated_image, image_rect.topleft)
        else:
            screen.blit(self.killed_image, (self.position.x, self.position.y))


    def update(self, dt):
        if self.killed_at and self.killed_at > dt - 1.5:
            self.kill()
            return
        self.position += self.velocity * dt

    def split(self, dt, asteroids):
        self.killed_at = dt
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        angle = random.uniform(20, 50)
        min_angle = self.velocity.rotate(angle)
        max_angle = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = min_angle * 1.2
        asteroid2.velocity = max_angle * 1.2
        asteroids.add(asteroid1, asteroid2)

    