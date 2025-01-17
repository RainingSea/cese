import pygame
import json
from random import randint

class Bird:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.gravity = 1
        self.width = 34
        self.height = 24

    def flap(self):
        self.y -= 20  # Flap action

    def fall(self):
        self.y += self.gravity  # Apply gravity

    def is_on_ground(self, ground_level: int) -> bool:
        return self.y + self.height >= ground_level


class Pipe:
    def __init__(self, x: int, height: int):
        self.x = x
        self.height = height
        self.width = 52
        self.gap = 150  # Gap between pipes

    def move(self):
        self.x -= 5  # Move pipe to the left


class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_scores = self.load_high_scores()

    def increment_score(self):
        self.score += 1

    def get_score(self) -> int:
        return self.score

    def save_high_score(self):
        high_score = max(self.high_scores.get('high_score', 0), self.score)
        self.high_scores['high_score'] = high_score
        with open('high_scores.json', 'w') as f:
            json.dump(self.high_scores, f)

    def load_high_scores(self) -> dict:
        try:
            with open('high_scores.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'high_score': 0}


class Game:
    def __init__(self):
        self.bird = Bird(100, 250)
        self.pipes = []
        self.score_manager = ScoreManager()
        self.is_running = True
        self.ground_level = 600  # Ground level for collision detection
        self.spawn_pipe()

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        pygame.display.set_caption("Flappy Bird Clone")
        clock = pygame.time.Clock()

        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.flap()

    def update(self):
        self.bird.fall()
        if len(self.pipes) == 0:  # Ensure pipes are generated at the start
            self.spawn_pipe()
        for pipe in self.pipes:
            pipe.move()
            if pipe.x + pipe.width < 0:
                self.pipes.remove(pipe)
                self.score_manager.increment_score()

        self.check_collision()

    def draw(self):
        self.screen.fill((135, 206, 235))  # Sky color
        pygame.draw.rect(self.screen, (255, 255, 0), (self.bird.x, self.bird.y, self.bird.width, self.bird.height))  # Bird
        for pipe in self.pipes:
            pygame.draw.rect(self.screen, (0, 255, 0), (pipe.x, 0, pipe.width, pipe.height))  # Top pipe
            pygame.draw.rect(self.screen, (0, 255, 0), (pipe.x, pipe.height + pipe.gap, pipe.width, self.ground_level - pipe.height - pipe.gap))  # Bottom pipe
        pygame.display.flip()

    def check_collision(self) -> bool:
        if self.bird.is_on_ground(self.ground_level):
            self.is_running = False
            self.score_manager.save_high_score()
            return True

        for pipe in self.pipes:
            if (self.bird.x + self.bird.width > pipe.x and self.bird.x < pipe.x + pipe.width):
                if (self.bird.y < pipe.height or self.bird.y + self.bird.height > pipe.height + pipe.gap):
                    self.is_running = False
                    self.score_manager.save_high_score()
                    return True
        return False

    def restart_game(self):
        self.bird = Bird(100, 250)
        self.pipes.clear()
        self.score_manager.score = 0
        self.spawn_pipe()

    def spawn_pipe(self):
        height = randint(100, 400)
        self.pipes.append(Pipe(400, height))


class GameController:
    def __init__(self):
        self.game = Game()

    def run(self):
        self.game.start_game()
        pygame.quit()