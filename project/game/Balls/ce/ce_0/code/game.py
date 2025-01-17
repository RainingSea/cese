import pygame
import random
from player_ball import PlayerBall
from enemy_ball import EnemyBall

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.player_ball = PlayerBall(size=20, position=(400, 300))
        self.enemy_balls = []
        self.load_game_data()
        self.initialize_balls()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.check_collisions()
            self.update_display()
            pygame.time.delay(30)

    def initialize_balls(self):
        for _ in range(5):
            size = random.randint(10, 30)
            position = (random.randint(0, 800), random.randint(0, 600))
            enemy_ball = EnemyBall(size=size, position=position)
            self.enemy_balls.append(enemy_ball)

    def check_collisions(self):
        for enemy in self.enemy_balls:
            if self.is_colliding(self.player_ball.position, self.player_ball.size, enemy.position, enemy.size):
                self.player_ball.grow(5)
                self.enemy_balls.remove(enemy)

    def is_colliding(self, pos1, size1, pos2, size2):
        dist_x = pos1[0] - pos2[0]
        dist_y = pos1[1] - pos2[1]
        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5
        return distance < (size1 + size2)

    def load_game_data(self):
        try:
            with open('game_data.txt', 'r') as file:
                data = file.readlines()
                self.player_ball.size = float(data[0].strip().split('|')[1])
        except FileNotFoundError:
            self.player_ball.size = 20

    def save_game_data(self):
        with open('game_data.txt', 'w') as file:
            file.write(f'player_size|{self.player_ball.size}\n')