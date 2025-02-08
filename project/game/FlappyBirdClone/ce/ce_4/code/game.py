import pygame
import random

class Bird:
    def __init__(self):
        self.position = (100, 250)
        self.velocity = 0

    def flap(self):
        self.velocity = -10

    def update(self):
        self.velocity += 0.5  # Gravity
        self.position = (self.position[0], self.position[1] + self.velocity)

    def draw(self, screen):
        bird_image = pygame.Surface((30, 30))
        bird_image.fill((255, 255, 0))  # Yellow bird
        screen.blit(bird_image, self.position)

class Pipes:
    def __init__(self):
        self.pipe_list = []
        self.pipe_height = random.randint(150, 300)
        self.pipe_width = 70
        self.gap = 150

    def generate_pipes(self):
        top_pipe = pygame.Rect(400, 0, self.pipe_width, self.pipe_height)
        bottom_pipe = pygame.Rect(400, self.pipe_height + self.gap, self.pipe_width, 600 - self.pipe_height - self.gap)
        self.pipe_list.append((top_pipe, bottom_pipe))

    def update(self):
        for pipes in self.pipe_list:
            pipes[0].x -= 5
            pipes[1].x -= 5

    def draw(self, screen):
        for pipes in self.pipe_list:
            pygame.draw.rect(screen, (0, 255, 0), pipes[0])  # Top pipe
            pygame.draw.rect(screen, (0, 255, 0), pipes[1])  # Bottom pipe

    def check_collision(self, bird: Bird) -> bool:
        bird_rect = pygame.Rect(bird.position[0], bird.position[1], 30, 30)
        for pipes in self.pipe_list:
            if bird_rect.colliderect(pipes[0]) or bird_rect.colliderect(pipes[1]):
                return True
        return False

class Score:
    def __init__(self):
        self.points = 0

    def increment(self):
        self.points += 1

    def get_score(self) -> int:
        return self.points

class GameState:
    def __init__(self):
        self.is_running = True

    def start(self):
        self.is_running = True

    def end(self):
        self.is_running = False

class HighScoreManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_high_scores(self) -> list:
        try:
            with open(self.file_path, 'r') as file:
                return [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_high_score(self, score: int):
        with open(self.file_path, 'a') as file:
            file.write(f"{score}\n")

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = Pipes()
        self.score = Score()
        self.state = GameState()
        self.high_score_manager = HighScoreManager('highscores.txt')

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 600))
        clock = pygame.time.Clock()
        self.pipes.generate_pipes()

        while self.state.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state.end()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bird.flap()

            self.bird.update()
            self.pipes.update()

            if self.pipes.check_collision(self.bird):
                self.state.end()

            screen.fill((0, 0, 255))  # Blue background
            self.bird.draw(screen)
            self.pipes.draw(screen)

            pygame.display.flip()
            clock.tick(60)

    def restart(self):
        self.bird = Bird()
        self.pipes = Pipes()
        self.score = Score()
        self.state.start()
        self.pipes.generate_pipes()