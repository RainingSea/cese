import pygame
import random

class Ball:
    def __init__(self, size, x_position, y_position):
        self.size = size
        self.x_position = x_position
        self.y_position = y_position

    def move(self, direction: str):
        if direction == 'UP':
            self.y_position -= 5
        elif direction == 'DOWN':
            self.y_position += 5
        elif direction == 'LEFT':
            self.x_position -= 5
        elif direction == 'RIGHT':
            self.x_position += 5

    def grow(self, amount: int):
        self.size += amount

    def is_smaller_than(self, other: 'Ball') -> bool:
        return self.size < other.size

class Game:
    def __init__(self):
        self.player_ball = Ball(30, 400, 300)
        self.enemy_balls = [Ball(20, random.randint(0, 800), random.randint(0, 600)) for _ in range(4)]
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Ball Game")

    def initialize(self):
        self.load_game_state()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_ball.move('UP')
        if keys[pygame.K_DOWN]:
            self.player_ball.move('DOWN')
        if keys[pygame.K_LEFT]:
            self.player_ball.move('LEFT')
        if keys[pygame.K_RIGHT]:
            self.player_ball.move('RIGHT')

        self.check_collisions()

    def check_collisions(self):
        for enemy in self.enemy_balls:
            if (self.player_ball.x_position - self.player_ball.size < enemy.x_position + enemy.size and
                self.player_ball.x_position + self.player_ball.size > enemy.x_position - enemy.size and
                self.player_ball.y_position - self.player_ball.size < enemy.y_position + enemy.size and
                self.player_ball.y_position + self.player_ball.size > enemy.y_position - enemy.size):
                if self.player_ball.is_smaller_than(enemy):
                    print("Game Over")
                    pygame.quit()
                else:
                    self.player_ball.grow(10)
                    self.enemy_balls.remove(enemy)
                    self.enemy_balls.append(Ball(20, random.randint(0, 800), random.randint(0, 600)))

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, (0, 255, 0), (self.player_ball.x_position, self.player_ball.y_position), self.player_ball.size)
        for enemy in self.enemy_balls:
            pygame.draw.circle(self.screen, (255, 0, 0), (enemy.x_position, enemy.y_position), enemy.size)
        pygame.display.flip()

    def load_game_state(self):
        try:
            with open('game_state.txt', 'r') as file:
                data = file.readlines()
                self.player_ball.size = int(data[0].strip())
                self.player_ball.x_position = int(data[1].strip())
                self.player_ball.y_position = int(data[2].strip())
                for line in data[3:]:
                    size, x, y = map(int, line.strip().split('|'))
                    self.enemy_balls.append(Ball(size, x, y))
        except FileNotFoundError:
            print("No saved game state found.")