import pygame
import random

class Bird:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gravity = 1

    def flap(self):
        self.y -= 20

    def fall(self):
        self.y += self.gravity

    def get_position(self) -> tuple:
        return self.x, self.y, self.width, self.height

class Pipe:
    def __init__(self, x: int, gap_y: int, width: int, height: int):
        self.x = x
        self.gap_y = gap_y
        self.width = width
        self.height = height

    def move(self):
        self.x -= 5

    def get_position(self) -> tuple:
        return self.x, self.gap_y, self.width, self.height

class Game:
    def __init__(self):
        self.bird = Bird(50, 250, 30, 30)
        self.pipes = []
        self.score = 0
        self.high_score = self.load_high_score()
        self.generate_pipes()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.flap()

            self.update()
            self.draw(screen)
            clock.tick(60)

        self.save_high_score()
        pygame.quit()

    def update(self):
        self.bird.fall()
        for pipe in self.pipes:
            pipe.move()
            if pipe.x + pipe.width < 0:
                self.pipes.remove(pipe)
                self.score += 1
                self.generate_pipes()

        self.check_collision()

    def draw(self, screen):
        screen.fill((135, 206, 235))  # Sky blue
        pygame.draw.rect(screen, (255, 0, 0), self.bird.get_position())  # Bird
        for pipe in self.pipes:
            pygame.draw.rect(screen, (0, 255, 0), pipe.get_position())  # Pipes
        pygame.display.flip()

    def restart(self):
        self.bird = Bird(50, 250, 30, 30)
        self.pipes.clear()
        self.score = 0
        self.generate_pipes()

    def check_collision(self) -> bool:
        bird_rect = pygame.Rect(self.bird.get_position())
        for pipe in self.pipes:
            pipe_rect = pygame.Rect(pipe.get_position())
            if bird_rect.colliderect(pipe_rect):
                return True
        return False

    def load_high_score(self) -> int:
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open('highscore.txt', 'w') as f:
                f.write(str(self.high_score))

    def generate_pipes(self):
        gap_y = random.randint(100, 400)
        self.pipes.append(Pipe(400, gap_y, 50, 600 - gap_y))
        self.pipes.append(Pipe(400, gap_y - 150, 50, gap_y - 150))