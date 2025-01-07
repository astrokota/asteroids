from datetime import date
import pygame

from .asset_helper import get_asset_path, get_save_data
from .asteroidfield import *
from .circleshape import *
from .constants import *
from .player import *
from .shot import *

class Game:
    def __init__(self):
        self.screen = None
        self.minutes = None
        self.seconds = None
        self.score = None
        self.updatable = None
        self.drawable = None
        self.asteroids = None
        self.shots = None
        self.player = None

    def run_game(self):
        
        print("Starting asteroids!")
        print("Screen width: 1280")
        print("Screen height: 720")
        
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.font.init()
        font1 = pygame.font.SysFont("ubuntusans", 36)

        clock = pygame.time.Clock()
        dt = 0

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        Player.containers = (self.updatable, self.drawable)

        self.asteroids = pygame.sprite.Group()
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable)
        
        Shot.containers = (self.updatable, self.drawable)

        self.player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2, shots_group=self.shots)
        self.asteroidfield = AsteroidField()

        self.score = 0

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

        self.start_time = pygame.time.get_ticks()

        self.running = True
        self.game_over = False

        while self.running:
            for event in pygame.event.get():
                self.handle_game_event(event)
            if not self.game_over:
                pygame.Surface.fill(self.screen, (0, 0, 0))
                self.screen.blit(game_background, (0, 0))
                elapsed_time = pygame.time.get_ticks() - self.start_time
                self.minutes = elapsed_time // 60000
                self.seconds = (elapsed_time % 60000) // 1000
                timer_text = font1.render(f"Time: {self.minutes:02}:{self.seconds:02}", True, (255, 255, 255))
                self.screen.blit(timer_text, (1090, 10))
                pygame.key.get_pressed()
                for d in self.drawable:
                    d.draw(self.screen)
                for u in self.updatable:
                    u.update(dt)
                for a in self.asteroids:
                    if self.player.check_collision(a):
                        print("Game over!")
                        print(f"Final score: {self.score}")
                        print(f"Total time: {self.minutes:02}:{self.seconds:02}")
                        self.game_over = True
                        break
                for s in self.player.shots:
                    for a in self.asteroids:
                        if s.check_collision(a):
                            s.kill()
                            a.split(dt, self.asteroids)
                            self.score += 5
                            if sound is not None:
                                sound.play()
                self.screen.blit(font1.render(f"Score: {self.score}", True, (255, 255, 255)), (10, 10))
            pygame.display.flip()
            dt = clock.tick(60)
            dt = dt / 1000
        pygame.quit()

    def show_game_over(self):
        font2 = pygame.font.SysFont("UbuntuSans-Italic", 160)
        button_font = pygame.font.SysFont("DejaVuSansMono-Oblique", 60)
        game_over_text = font2.render("GAME OVER!", True, (153, 51, 255))
        retry_text = button_font.render("RETRY", True, (0, 0, 0))
        quit_text = button_font.render("QUIT", True, (0, 0, 0))

        game_over_rect = game_over_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        retry_rect = retry_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))

        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text, game_over_rect)
        pygame.draw.rect(self.screen, (153, 255, 153), retry_rect.inflate(40, 40))
        pygame.draw.rect(self.screen, (153, 255, 153), quit_rect.inflate(45, 45))
        self.screen.blit(retry_text, retry_rect)
        self.screen.blit(quit_text, quit_rect)

        pygame.display.update()

        return retry_rect, quit_rect

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if self.game_over:
            retry_rect, quit_rect = self.show_game_over()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos() 
                if retry_rect.collidepoint(mouse_x, mouse_y):
                    self.save_game_data()
                    self.game_over = False
                    self.score = 0
                    self.start_time = pygame.time.get_ticks()
                    self.updatable.empty()
                    self.drawable.empty()
                    self.asteroids.empty()
                    self.shots.empty()
                    self.player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2, shots_group = self.shots)
                    self.asteroidfield = AsteroidField()
                elif quit_rect.collidepoint(mouse_x, mouse_y):
                    self.save_game_data()
                    self.running = False

    def save_game_data(self):
        file_path = get_save_data()
        today = date.today()
        with open(file_path, "a") as file:
            file.write(f"Date: {today}, Score: {self.score}, Time: {self.minutes:02}:{self.seconds:02}\n")