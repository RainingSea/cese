import pygame
import random
import time

class Target:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
        self.speed = random.randint(1, 5)

    def move(self):
        self.x += self.speed
        if self.x > 800:
            self.x = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 20)

class Score:
    def __init__(self, player_name: str, score_value: int):
        self.player_name = player_name
        self.score_value = score_value

class Leaderboard:
    def __init__(self):
        self.scores = []

    def load_scores(self):
        try:
            with open('scores.txt', 'r') as f:
                for line in f:
                    name, score = line.strip().split('|')
                    self.scores.append(Score(name, int(score)))
        except FileNotFoundError:
            self.scores = []

    def save_score(self, score: int):
        player_name = input("Enter your name: ")
        new_score = Score(player_name, score)
        self.scores.append(new_score)
        with open('scores.txt', 'a') as f:
            f.write(f"{new_score.player_name}|{new_score.score_value}\n")

class Game:
    def __init__(self):
        self.score = 0
        self.time_limit = 30
        self.targets = []
        self.leaderboard = Leaderboard()
        self.leaderboard.load_scores()

    def start_game(self):
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Target Shooter")
        clock = pygame.time.Clock()
        self.targets = [Target() for _ in range(5)]
        start_time = time.time()

        while True:
            screen.fill((255, 255, 255))
            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

            if time.time() - start_time > self.time_limit:
                break

        self.leaderboard.save_score(self.score)

    def update(self):
        for target in self.targets:
            target.move()

    def draw(self, screen):
        for target in self.targets:
            target.draw(screen)
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    def restart(self):
        self.score = 0
        self.targets = [Target() for _ in range(5)]