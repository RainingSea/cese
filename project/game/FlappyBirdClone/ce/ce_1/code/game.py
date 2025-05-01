import pygame
import random

class Bird:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.velocity = 0

    def flap(self):
        self.velocity = -10

    def update(self):
        self.velocity += 1  # Gravity
        self.y += self.velocity

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)

    def move(self):
        self.x -= 5  # Speed of the pipe

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, 50, self.height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.height + 150, 50, 600 - self.height - 150))

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.high_score = self.load_high_score()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((600, 600))
        self.running = True

    def start_game(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.flap()

    def update(self):
        self.bird.update()
        if len(self.pipes) == 0 or self.pipes[-1].x < 400:
            self.pipes.append(Pipe(600))
        for pipe in self.pipes:
            pipe.move()
        self.check_collision()
        self.pipes = [pipe for pipe in self.pipes if pipe.x > -50]

    def check_collision(self):
        for pipe in self.pipes:
            if (self.bird.x + 30 > pipe.x and self.bird.x < pipe.x + 50) and (self.bird.y < pipe.height or self.bird.y + 30 > pipe.height + 150):
                self.restart_game()

        if self.bird.y > 600 or self.bird.y < 0:
            self.restart_game()

        self.score += 1  # Increment score for each frame

    def draw(self):
        self.screen.fill((135, 206, 250))  # Sky blue
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.draw_score()
        pygame.display.flip()

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score} High Score: {self.high_score}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def restart_game(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.score = 0
        self.pipes.clear()
        self.bird.y = 300
        self.bird.velocity = 0

    def load_high_score(self):
        try:
            with open('scores.txt', 'r') as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        with open('scores.txt', 'w') as file:
            file.write(str(self.high_score))