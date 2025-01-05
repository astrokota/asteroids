import pygame
import warnings

from .asset_helper import get_asset_path
from .circleshape import *
from .player import *
from .asteroidfield import *
from .shot import *
from .constants import *

def main():

    print("Starting asteroids!")
    print("Screen width: 1280")
    print("Screen height: 720")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.font.init()
    font1 = pygame.font.SysFont("ubuntusans", 36)
    font2 = pygame.font.SysFont("UbuntuSans-Italic", 160)
    button_font = pygame.font.SysFont("DejaVuSansMono-Oblique", 60)

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

    score = 0


    try:
        pygame.mixer.init()
        sound = pygame.mixer.Sound(get_asset_path("hitmarker_2.mp3"))
        sound.set_volume(0.25)
    except Exception as e:
        print(f"Error loading sound: {e}")
        sound = None

    try:
        game_background = pygame.image.load(get_asset_path("asteroids_background.jpg"))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        game_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    start_time = pygame.time.get_ticks()

    running = True
    game_over = False

    def show_game_over():
        game_over_text = font2.render("GAME OVER!", True, (153, 51, 255))
        retry_text = button_font.render("RETRY", True, (0, 0, 0))
        quit_text = button_font.render("QUIT", True, (0, 0, 0))

        game_over_rect = game_over_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        retry_rect = retry_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))

        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_rect)
        pygame.draw.rect(screen, (153, 255, 153), retry_rect.inflate(40, 40))
        pygame.draw.rect(screen, (153, 255, 153), quit_rect.inflate(45, 45))
        screen.blit(retry_text, retry_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.update()

        return retry_rect, quit_rect

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over:
                retry_rect, quit_rect = show_game_over()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos() 
                    if retry_rect.collidepoint(mouse_x, mouse_y):
                        game_over = False
                        score = 0
                        start_time = pygame.time.get_ticks()
                        updatable.empty()
                        drawable.empty()
                        asteroids.empty()
                        shots.empty()
                        player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2, shots_group = shots)
                        asteroidfield = AsteroidField()
                    elif quit_rect.collidepoint(mouse_x, mouse_y):
                        running = False
        if not game_over:
            pygame.Surface.fill(screen, (0, 0, 0))
            screen.blit(game_background, (0, 0))
            elapsed_time = pygame.time.get_ticks() - start_time
            minutes = elapsed_time // 60000
            seconds = (elapsed_time % 60000) // 1000
            timer_text = font1.render(f"Time: {minutes:02}:{seconds:02}", True, (255, 255, 255))
            screen.blit(timer_text, (1090, 10))
            pygame.key.get_pressed()
            for d in drawable:
                d.draw(screen)
            for u in updatable:
                u.update(dt)
            for a in asteroids:
                if player.check_collision(a):
                    print("Game over!")
                    print(f"Final score: {score}")
                    print(f"Total time: {minutes:02}:{seconds:02}")
                    game_over = True
                    break
            for s in player.shots:
                for a in asteroids:
                    if s.check_collision(a):
                        s.kill()
                        a.split(dt, asteroids)
                        score += 5
                        if sound is not None:
                            sound.play()
            screen.blit(font1.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
        pygame.display.flip()
        dt = clock.tick(60)
        dt = dt / 1000
    pygame.quit()
if __name__ == "__main__":
    main()