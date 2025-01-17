import pygame
import random

class Frog:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def jump(self):
        self.y -= 50  # Jump height

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move(self):
        pass  # Placeholder for platform movement logic

class Game:
    def __init__(self):
        self.frog = Frog(100, 300)
        self.platforms = [Platform(random.randint(0, 400), random.randint(100, 400), 100, 10) for _ in range(5)]
        self.score = 0
        self.timer = 60  # Game timer in seconds

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Jumping Frog")
        self.clock = pygame.time.Clock()
        self.run_game()

    def run_game(self):
        running = True
        while running:
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.check_collision()
            self.end_game()

    def update(self):
        self.screen.fill((0, 0, 255))  # Fill the screen with blue (water)
        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 255, 0), (platform.x, platform.y, platform.width, platform.height))  # Draw platforms
        pygame.draw.rect(self.screen, (255, 0, 0), (self.frog.x, self.frog.y, 30, 30))  # Draw frog
        pygame.display.update()
        self.clock.tick(60)  # Frame rate

    def check_collision(self):
        for platform in self.platforms:
            if (self.frog.x < platform.x + platform.width and
                self.frog.x + 30 > platform.x and
                self.frog.y + 30 > platform.y and
                self.frog.y < platform.y + platform.height):
                self.frog.y = platform.y - 30  # Place frog on top of the platform

    def end_game(self):
        if self.timer <= 0:
            self.save_score()
            pygame.quit()

    def save_score(self):
        with open('game_data.txt', 'a') as f:
            f.write(f'Score: {self.score}\n')