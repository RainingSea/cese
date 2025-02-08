import pygame
import random

class Tank:
    def __init__(self, health: int, position_x: int, position_y: int):
        self.health = health
        self.position_x = position_x
        self.position_y = position_y

    def move(self, direction: str) -> None:
        if direction == 'up':
            self.position_y -= 1
        elif direction == 'down':
            self.position_y += 1
        elif direction == 'left':
            self.position_x -= 1
        elif direction == 'right':
            self.position_x += 1

    def take_damage(self, amount: int) -> None:
        self.health -= amount

class EnemyTank:
    def __init__(self, health: int, position_x: int, position_y: int):
        self.health = health
        self.position_x = position_x
        self.position_y = position_y

    def shoot(self) -> None:
        # Logic for shooting (not implemented in detail)
        pass

    def take_damage(self, amount: int) -> None:
        self.health -= amount

class Game:
    def __init__(self):
        self.grid_size = 20
        self.player_tank = Tank(health=100, position_x=10, position_y=10)
        self.enemy_tanks = [EnemyTank(health=50, position_x=random.randint(0, 19), position_y=random.randint(0, 19)) for _ in range(5)]
        self.score = 0
        self.player_health = self.player_tank.health
        self.enemy_health = sum(enemy.health for enemy in self.enemy_tanks)

    def start_game(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Tank Battle Game")
        self.run_game_loop()

    def move_player(self, direction: str) -> None:
        self.player_tank.move(direction)

    def fire_bullet(self) -> None:
        # Logic for firing a bullet (not implemented in detail)
        pass

    def check_collisions(self) -> None:
        # Logic for checking collisions (not implemented in detail)
        pass

    def end_game(self) -> None:
        with open('score.txt', 'w') as score_file:
            score_file.write(f'score: {self.score}')
        pygame.quit()