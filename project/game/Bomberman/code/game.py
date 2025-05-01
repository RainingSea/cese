import pygame
import random

# Constants for game settings
GRID_SIZE = 13
ENEMY_HEALTH = 50
PLAYER_HEALTH = 100
BOMB_TIMER = 3
EXPLOSION_RADIUS = 1  # Define the explosion radius

class Grid:
    def __init__(self):
        self.cells = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def initialize_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.cells[i][j] = 0

    def draw(self, screen):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color = (0, 255, 0) if self.cells[i][j] == 1 else (255, 0, 0) if self.cells[i][j] == 2 else (255, 255, 255)
                pygame.draw.rect(screen, color, (j * 40, i * 40, 40, 40))

    def apply_explosion(self, x, y, player):
        for i in range(max(0, x - EXPLOSION_RADIUS), min(GRID_SIZE, x + EXPLOSION_RADIUS + 1)):
            for j in range(max(0, y - EXPLOSION_RADIUS), min(GRID_SIZE, y + EXPLOSION_RADIUS + 1)):
                if self.cells[i][j] == 1:  # If a bomb is present
                    self.cells[i][j] = 0  # Remove the bomb
                elif self.cells[i][j] == 2:  # If an enemy is present
                    enemy = next((e for e in self.enemies if e.x == i and e.y == j), None)
                    if enemy:
                        enemy.take_damage(20)  # Example damage value
                        if enemy.health <= 0:
                            self.enemies.remove(enemy)  # Remove enemy if health is depleted
        # Check if player is within explosion range
        if player.x in range(max(0, x - EXPLOSION_RADIUS), min(GRID_SIZE, x + EXPLOSION_RADIUS + 1)) and \
           player.y in range(max(0, y - EXPLOSION_RADIUS), min(GRID_SIZE, y + EXPLOSION_RADIUS + 1)):
            player.take_damage(20)  # Example damage value

class Player:
    def __init__(self):
        self.health = PLAYER_HEALTH
        self.score = 0
        self.x, self.y = 0, 0  # Starting position

    def move(self, direction):
        if direction == 'up' and self.y > 0:
            self.y -= 1
        elif direction == 'down' and self.y < GRID_SIZE - 1:
            self.y += 1
        elif direction == 'left' and self.x > 0:
            self.x -= 1
        elif direction == 'right' and self.x < GRID_SIZE - 1:
            self.x += 1

    def place_bomb(self):
        if self.health > 0:  # Ensure player can only place a bomb if alive
            bomb = Bomb(self.x, self.y)
            return bomb
        return None

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

class Enemy:
    def __init__(self):
        self.health = ENEMY_HEALTH
        self.x, self.y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)

    def move(self, player_x, player_y):
        if self.x < player_x:
            self.x += 1
        elif self.x > player_x:
            self.x -= 1
        if self.y < player_y:
            self.y += 1
        elif self.y > player_y:
            self.y -= 1

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

class Bomb:
    def __init__(self, x, y):
        self.timer = BOMB_TIMER
        self.x = x
        self.y = y

    def explode(self, grid, player):
        grid.apply_explosion(self.x, self.y, player)

class Game:
    def __init__(self):
        self.grid = Grid()
        self.player = Player()
        self.enemies = [Enemy() for _ in range(5)]
        self.bombs = []

    def start_game(self):
        screen = pygame.display.set_mode((520, 520))
        pygame.display.set_caption("Bomb Game")
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.move('up')
                    elif event.key == pygame.K_DOWN:
                        self.player.move('down')
                    elif event.key == pygame.K_LEFT:
                        self.player.move('left')
                    elif event.key == pygame.K_RIGHT:
                        self.player.move('right')
                    elif event.key == pygame.K_SPACE:  # Space to place a bomb
                        bomb = self.player.place_bomb()
                        if bomb:
                            self.bombs.append(bomb)

            self.update()
            self.render(screen)
            self.check_game_over()
            self.check_victory()
            clock.tick(60)

        self.save_game_state()

    def update(self):
        for enemy in self.enemies:
            enemy.move(self.player.x, self.player.y)
        self.handle_collisions()
        for bomb in self.bombs:
            bomb.timer -= 1 / 60  # Decrease timer based on frame rate
            if bomb.timer <= 0:
                bomb.explode(self.grid, self.player)
                self.bombs.remove(bomb)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.grid.draw(screen)
        pygame.display.flip()

    def handle_collisions(self):
        for enemy in self.enemies:
            if enemy.x == self.player.x and enemy.y == self.player.y:
                self.player.take_damage(10)  # Example damage value

    def check_game_over(self):
        if self.player.health <= 0:
            print("Game Over! You have lost.")
            pygame.quit()

    def check_victory(self):
        if all(enemy.health <= 0 for enemy in self.enemies):
            print("Congratulations! You have defeated all enemies.")
            pygame.quit()

    def save_game_state(self):
        with open('game_state.txt', 'w') as f:
            f.write(f"{self.player.score}|{self.player.health}\n")

    def load_game_state(self):
        try:
            with open('game_state.txt', 'r') as f:
                data = f.readline().strip().split('|')
                self.player.score = int(data[0])
                self.player.health = int(data[1])
        except FileNotFoundError:
            pass