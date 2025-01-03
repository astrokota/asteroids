import pygame
from constants import *
from circleshape import *
from player import *
from asteroidfield import *
from shot import *

def main():

    print("Starting asteroids!")
    print("Screen width: 1280")
    print("Screen height: 720")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)

    
    Shot.containers = (updatable, drawable)

    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2, shots_group=shots)
    asteroidfield = AsteroidField()

    while True:
        pygame.Surface.fill(screen, (0, 0, 0))
        for d in drawable:
            d.draw(screen)
        for u in updatable:
            u.update(dt)
        for a in asteroids:
            if player.check_collision(a):
                print("Game over!")
                return
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        dt = clock.tick(60)
        dt = dt / 1000

if __name__ == "__main__":
    main()