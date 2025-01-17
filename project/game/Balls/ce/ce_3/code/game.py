import pygame
import random

class PlayerBall:
    def __init__(self, size, position_x, position_y):
        self.size = size
        self.position_x = position_x
        self.position_y = position_y

    def move(self, direction: str):
        if direction == "UP":
            self.position_y -= 5
        elif direction == "DOWN":
            self.position_y += 5
        elif direction == "LEFT":
            self.position_x -= 5
        elif direction == "RIGHT":
            self.position_x += 5

    def grow(self, size_increase: int):
        self.size += size_increase

class EnemyBall:
    def __init__(self, size, position_x, position_y):
        self.size = size
        self.position_x = position_x
        self.position_y = position_y

    def move_randomly(self):
        self.position_x += random.choice([-1, 1]) * random.randint(1, 3)
        self.position_y += random.choice([-1, 1]) * random.randint(1, 3)

class Game:
    def __init__(self):
        self.player_ball = PlayerBall(size=10, position_x=400, position_y=300)
        self.enemy_balls = []
        self.is_game_over = False

    def start_game(self):
        pygame.init()
        self.spawn_enemy_balls()
        self.main_loop()

    def main_loop(self):
        while not self.is_game_over:
            self.update()
            self.check_collisions()
            self.spawn_enemy_balls()
            pygame.time.delay(100)

    def update(self):
        for enemy_ball in self.enemy_balls:
            enemy_ball.move_randomly()

    def check_collisions(self):
        for enemy_ball in self.enemy_balls:
            if (self.player_ball.position_x < enemy_ball.position_x + enemy_ball.size and
                self.player_ball.position_x + self.player_ball.size > enemy_ball.position_x and
                self.player_ball.position_y < enemy_ball.position_y + enemy_ball.size and
                self.player_ball.position_y + self.player_ball.size > enemy_ball.position_y):
                self.end_game()

    def spawn_enemy_balls(self):
        if len(self.enemy_balls) < 5:
            new_enemy_ball = EnemyBall(size=random.randint(5, 15), position_x=random.randint(0, 800), position_y=random.randint(0, 600))
            self.enemy_balls.append(new_enemy_ball)

    def end_game(self):
        self.is_game_over = True