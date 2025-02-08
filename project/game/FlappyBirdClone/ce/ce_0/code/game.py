import pygame
import random
from typing import List

class Bird:
    def __init__(self, y_position: int) -> None:
        self.y_position = y_position
        self.flap_strength = 10

    def flap(self) -> None:
        self.y_position -= self.flap_strength

    def fall(self) -> None:
        self.y_position += 5

class Pipe:
    def __init__(self, x_position: int, gap_y_position: int) -> None:
        self.x_position = x_position
        self.gap_y_position = gap_y_position

    def move(self) -> None:
        self.x_position -= 5

class Game:
    def __init__(self) -> None:
        self.bird = Bird(200)
        self.pipes = []
        self.score = 0
        self.is_game_over = False
        self.load_high_scores()

    def start_game(self) -> None:
        self.reset_game()
        while not self.is_game_over:
            self.handle_input()
            self.update()
            self.render()

    def update(self) -> None:
        if not self.is_game_over:
            self.bird.fall()
            for pipe in self.pipes:
                pipe.move()
                if pipe.x_position < -50:
                    self.pipes.remove(pipe)
                    self.score += 1
            self.check_collision()

    def render(self) -> None:
        # Placeholder for rendering logic (Pygame specific)
        pass

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_game_over = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.flap()

    def check_collision(self) -> bool:
        # Placeholder for collision detection logic
        return False

    def reset_game(self) -> None:
        self.bird.y_position = 200
        self.pipes.clear()
        self.score = 0
        self.is_game_over = False
        self.create_pipes()

    def create_pipes(self) -> None:
        for i in range(5):
            gap_y_position = random.randint(100, 400)
            self.pipes.append(Pipe(600 + i * 200, gap_y_position))

    def load_high_scores(self) -> List[int]:
        try:
            with open('high_scores.txt', 'r') as file:
                return [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_high_score(self, score: int) -> None:
        high_scores = self.load_high_scores()
        high_scores.append(score)
        high_scores.sort(reverse=True)
        with open('high_scores.txt', 'w') as file:
            for high_score in high_scores[:10]:  # Keep top 10 scores
                file.write(f"{high_score}\n")