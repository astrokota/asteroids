from constants import *
from circleshape import *
from shot import *

class Player(CircleShape):
    def __init__(self, x, y, shots_group):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shots = shots_group
        self.timer = 0
        self.original_image = pygame.image.load("/home/dakotamitchell/workspace/github.com/astrokota/asteroids/ship.png")
        self.scale_factor = 0.08
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scale_factor), int(self.original_image.get_height() * self.scale_factor)))
        self.rect = self.image.get_rect(center = self.position)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        #pygame.draw.polygon(screen, (255, 255, 255), self.triangle())
        rotated_image = pygame.transform.rotate(self.image, -self.rotation)
        image_rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, image_rect.topleft)
        
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.timer >= 0:
            return
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation)
        shot.velocity *= PLAYER_SHOOT_SPEED
        self.shots.add(shot)
        self.timer = PLAYER_SHOOT_COOLDOWN
        
     
        
