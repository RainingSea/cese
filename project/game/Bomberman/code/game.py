import pygame
import random

class Grid:
    def __init__(self):
        self.grid_data = []
        self.initialize_grid()

    def initialize_grid(self):
        self.grid_data = [[' ' for _ in range(13)] for _ in range(13)]
        # Randomly place obstacles
        for _ in range(20):  # Example: 20 obstacles
            x, y = random.randint(0, 12), random.randint(0, 12)
            while self.grid_data[x][y] == 'X':  # Ensure no overlap with existing obstacles
                x, y = random.randint(0, 12), random.randint(0, 12)
            self.grid_data[x][y] = 'X'  # 'X' represents an obstacle

    def update_grid(self):
        pass  # Placeholder for future updates

    def get_obstacles(self):
        obstacles = []
        for i in range(13):
            for j in range(13):
                if self.grid_data[i][j] == 'X':
                    obstacles.append((i, j))
        return obstacles


class Player:
    def __init__(self):
        self.health = 100
        self.position_x = 0
        self.position_y = 0

    def move(self, direction: str):
        if direction == 'up' and self.position_x > 0:
            self.position_x -= 1
        elif direction == 'down' and self.position_x < 12:
            self.position_x += 1
        elif direction == 'left' and self.position_y > 0:
            self.position_y -= 1
        elif direction == 'right' and self.position_y < 12:
            self.position_y += 1

    def place_bomb(self):
        return Bomb(self.position_x, self.position_y)

    def take_damage(self, amount: int):
        self.health -= amount
        if self.health <= 0:
            self.health = 0  # Ensure health does not go below zero


class Enemy:
    def __init__(self):
        self.health = 50
        self.position_x = random.randint(0, 12)
        self.position_y = random.randint(0, 12)

    def move(self):
        # Simple random movement for demonstration
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up' and self.position_x > 0:
            self.position_x -= 1
        elif direction == 'down' and self.position_x < 12:
            self.position_x += 1
        elif direction == 'left' and self.position_y > 0:
            self.position_y -= 1
        elif direction == 'right' and self.position_y < 12:
            self.position_y += 1

    def take_damage(self, amount: int):
        self.health -= amount


class Bomb:
    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y
        self.timer = 3  # Bomb explodes after 3 seconds

    def explode(self):
        # Logic for explosion
        return (self.position_x, self.position_y)


class Game:
    def __init__(self):
        self.grid = Grid()
        self.player = Player()
        self.enemies = [Enemy() for _ in range(5)]  # Example: 5 enemies
        self.bombs = []
        self.score = 0
        self.player_health = self.player.health

    def start_game(self):
        pygame.init()
        # Set up the game window and other initial settings
        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Bomb Game")

    def update_game(self):
        # Update game state, move enemies, check for collisions, etc.
        for enemy in self.enemies:
            enemy.move()

        # Update bomb timers and check for explosions
        for bomb in self.bombs:
            bomb.timer -= 1
            if bomb.timer <= 0:
                self.handle_explosion(bomb)

    def handle_explosion(self, bomb: Bomb):
        # Logic for handling bomb explosion effects
        bomb_position = bomb.explode()
        self.bombs.remove(bomb)
        # Check if player is affected
        if (self.player.position_x, self.player.position_y) == bomb_position:
            self.player.take_damage(20)  # Example damage value
        # Check if enemies are affected
        for enemy in self.enemies:
            if (enemy.position_x, enemy.position_y) == bomb_position:
                enemy.take_damage(30)  # Example damage value
                if enemy.health <= 0:
                    self.enemies.remove(enemy)
                    self.score += 10  # Increase score for defeating an enemy

    def check_collisions(self):
        # Check for collisions between player, bombs, and enemies
        for enemy in self.enemies:
            if (self.player.position_x, self.player.position_y) == (enemy.position_x, enemy.position_y):
                self.player.take_damage(10)  # Example damage value for player colliding with enemy
                if self.player.health <= 0:
                    self.end_game()

    def end_game(self):
        print("Game Over! Your score:", self.score)
        pygame.quit()

    def display_ui(self):
        # Display the user interface elements like score and health
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        health_text = font.render(f'Health: {self.player.health}', True, (255, 255, 255))
        self.window.blit(score_text, (10, 10))
        self.window.blit(health_text, (10, 50))
        pygame.display.flip()