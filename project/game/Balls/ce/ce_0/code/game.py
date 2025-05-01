import pygame
import random

class PlayerBall:
    def __init__(self):
        self.size = 10.0  # Initial size of the player's ball

    def grow(self):
        self.size += 1.0  # Increase size when consuming an enemy ball


class EnemyBall:
    def __init__(self):
        self.position = (random.randint(0, 800), random.randint(0, 600))  # Random initial position
        self.size = 5.0  # Size of enemy balls

    def move(self):
        # Move the enemy ball randomly
        self.position = (self.position[0] + random.choice([-1, 1]), self.position[1] + random.choice([-1, 1]))
        # Keep within bounds
        self.position = (max(0, min(self.position[0], 800)), max(0, min(self.position[1], 600)))


class Game:
    def __init__(self):
        self.player_ball = PlayerBall()
        self.enemy_balls = [EnemyBall() for _ in range(5)]  # Create 5 enemy balls

    def initialize(self):
        # Load data if available
        self.load_data()

    def update(self):
        for enemy_ball in self.enemy_balls:
            enemy_ball.move()
        self.check_collisions()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def check_collisions(self):
        for enemy_ball in self.enemy_balls:
            if self._is_colliding(self.player_ball, enemy_ball):
                self.player_ball.grow()
                self.enemy_balls.remove(enemy_ball)  # Remove enemy ball upon collision

    def _is_colliding(self, player_ball, enemy_ball):
        distance = ((player_ball.size - enemy_ball.size) ** 2) ** 0.5
        return distance < (player_ball.size + enemy_ball.size)

    def load_data(self):
        try:
            with open('player_data.txt', 'r') as f:
                self.player_ball.size = float(f.read().strip())
            with open('enemy_data.txt', 'r') as f:
                positions = f.read().strip().splitlines()
                self.enemy_balls = [EnemyBall() for _ in positions]
                for i, pos in enumerate(positions):
                    x, y = map(int, pos.split('|'))
                    self.enemy_balls[i].position = (x, y)
        except FileNotFoundError:
            pass  # If files don't exist, start with defaults

    def save_data(self):
        with open('player_data.txt', 'w') as f:
            f.write(str(self.player_ball.size))
        with open('enemy_data.txt', 'w') as f:
            for enemy_ball in self.enemy_balls:
                f.write(f"{enemy_ball.position[0]}|{enemy_ball.position[1]}\n")