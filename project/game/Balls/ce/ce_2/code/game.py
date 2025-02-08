import pygame
import random

class Ball:
    def __init__(self, size: float, position: tuple):
        self.size = size
        self.position = position

    def move(self, direction: str) -> None:
        if direction == "up":
            self.position = (self.position[0], self.position[1] - self.size)
        elif direction == "down":
            self.position = (self.position[0], self.position[1] + self.size)
        elif direction == "left":
            self.position = (self.position[0] - self.size, self.position[1])
        elif direction == "right":
            self.position = (self.position[0] + self.size, self.position[1])

    def grow(self, amount: float) -> None:
        self.size += amount

class PlayerBall(Ball):
    def __init__(self, size: float, position: tuple):
        super().__init__(size, position)

    def check_collision(self, enemy: 'EnemyBall') -> bool:
        distance = ((self.position[0] - enemy.position[0]) ** 2 + (self.position[1] - enemy.position[1]) ** 2) ** 0.5
        return distance < (self.size + enemy.size)

class EnemyBall(Ball):
    def __init__(self, size: float, position: tuple):
        super().__init__(size, position)

class Game:
    def __init__(self):
        self.player_ball = PlayerBall(size=20, position=(400, 300))
        self.enemy_balls = []
        self.score = 0
        self.load_game_data()

    def initialize_game(self) -> None:
        self.enemy_balls = [EnemyBall(size=random.randint(10, 30), position=(random.randint(0, 800), random.randint(0, 600))) for _ in range(5)]

    def update(self) -> None:
        for enemy in self.enemy_balls:
            if self.player_ball.check_collision(enemy):
                self.player_ball.grow(5)
                self.score += 1
                self.enemy_balls.remove(enemy)

    def check_collisions(self) -> None:
        for enemy in self.enemy_balls:
            if self.player_ball.check_collision(enemy):
                self.end_game()

    def end_game(self) -> None:
        self.save_game_data()
        pygame.quit()

    def save_game_data(self) -> None:
        with open('game_data.txt', 'w') as file:
            file.write(f'Score: {self.score}\n')

    def load_game_data(self) -> None:
        try:
            with open('game_data.txt', 'r') as file:
                data = file.read().strip().split('\n')
                for line in data:
                    if line.startswith('Score:'):
                        self.score = int(line.split(': ')[1])
        except FileNotFoundError:
            self.score = 0