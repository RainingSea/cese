import pygame
import random

class Bullet:
    def __init__(self, damage: int, direction: int):
        self.damage = damage
        self.direction = direction

    def move(self):
        # Logic to move the bullet in the specified direction
        pass

class Tank:
    def __init__(self, health: int, position_x: int, position_y: int):
        self.health = health
        self.position_x = position_x
        self.position_y = position_y

    def move(self, direction: str):
        if direction == 'up':
            self.position_y -= 1
        elif direction == 'down':
            self.position_y += 1
        elif direction == 'left':
            self.position_x -= 1
        elif direction == 'right':
            self.position_x += 1

    def fire(self) -> Bullet:
        return Bullet(damage=10, direction=random.choice([0, 1, 2, 3]))

    def take_damage(self, amount: int):
        self.health -= amount

class EnemyTank:
    def __init__(self, health: int, position_x: int, position_y: int):
        self.health = health
        self.position_x = position_x
        self.position_y = position_y

    def shoot(self) -> Bullet:
        return Bullet(damage=5, direction=random.choice([0, 1, 2, 3]))

    def take_damage(self, amount: int):
        self.health -= amount

class Game:
    def __init__(self, grid_size: int):
        self.grid_size = grid_size
        self.player_tank = Tank(health=100, position_x=0, position_y=0)
        self.enemy_tanks = [EnemyTank(health=50, position_x=random.randint(0, grid_size-1), position_y=random.randint(0, grid_size-1)) for _ in range(5)]
        self.score = 0
        self.player_health = self.player_tank.health

    def run(self):
        pygame.init()
        self.update()
        self.render()

    def update(self):
        # Update game state
        pass

    def render(self):
        # Render the game
        pass

    def handle_input(self):
        # Handle user input
        pass

    def save_data(self):
        with open('game_data.txt', 'w') as file:
            file.write(f"score|{self.score}\n")
            file.write(f"health|{self.player_health}\n")