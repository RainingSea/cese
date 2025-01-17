import pygame
import random

class Target:
    def __init__(self, x: int, y: int, speed: int):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self) -> None:
        self.y += self.speed

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 20)

class Game:
    def __init__(self):
        self.score = 0
        self.time_limit = 30
        self.targets = []

    def start_game(self) -> None:
        self.score = 0
        self.targets = [Target(random.randint(20, 780), random.randint(-100, 0), random.randint(1, 3)) for _ in range(5)]

    def update(self) -> None:
        for target in self.targets:
            target.move()
            if target.y > 600:  # Assuming the screen height is 600
                self.targets.remove(target)
                self.score -= 1  # Penalty for missed target

    def render(self, screen) -> None:
        screen.fill((0, 0, 0))  # Clear screen with black
        for target in self.targets:
            target.draw(screen)
        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(text, (10, 10))

    def restart(self) -> None:
        self.start_game()

    def save_score(self, score: int) -> None:
        with open('scores.txt', 'a') as f:
            f.write(f'{score}\n')

    def load_scores(self) -> list:
        try:
            with open('scores.txt', 'r') as f:
                scores = [int(line.strip()) for line in f.readlines()]
            return sorted(scores, reverse=True)
        except FileNotFoundError:
            return []