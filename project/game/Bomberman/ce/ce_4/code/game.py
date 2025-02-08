import pygame
import random

class Cell:
    def __init__(self):
        self.is_obstacle = False

    def draw(self, screen, x, y):
        color = (255, 255, 255) if not self.is_obstacle else (0, 0, 0)
        pygame.draw.rect(screen, color, (x, y, 40, 40))

class Grid:
    def __init__(self):
        self.cells = [[Cell() for _ in range(13)] for _ in range(13)]
        self.place_obstacles()

    def place_obstacles(self):
        for row in range(0, 13, 2):
            for col in range(0, 13, 2):
                self.cells[row][col].is_obstacle = True

    def draw(self, screen):
        for row in range(13):
            for col in range(13):
                self.cells[row][col].draw(screen, col * 40, row * 40)

class Player:
    def __init__(self):
        self.health = 100
        self.score = 0
        self.x, self.y = 0, 0

    def move(self, direction):
        if direction == "UP" and self.y > 0:
            self.y -= 1
        elif direction == "DOWN" and self.y < 12:
            self.y += 1
        elif direction == "LEFT" and self.x > 0:
            self.x -= 1
        elif direction == "RIGHT" and self.x < 12:
            self.x += 1

    def place_bomb(self):
        return Bomb(self.x, self.y)

    def take_damage(self, amount):
        self.health -= amount

    def update_score(self, amount):
        self.score += amount

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 3

    def explode(self):
        return (self.x, self.y)

class Enemy:
    def __init__(self):
        self.health = 100
        self.x, self.y = random.randint(0, 12), random.randint(0, 12)

    def move(self):
        direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        if direction == "UP" and self.y > 0:
            self.y -= 1
        elif direction == "DOWN" and self.y < 12:
            self.y += 1
        elif direction == "LEFT" and self.x > 0:
            self.x -= 1
        elif direction == "RIGHT" and self.x < 12:
            self.x += 1

    def take_damage(self, amount):
        self.health -= amount

class Game:
    def __init__(self):
        self.grid = Grid()
        self.player = Player()
        self.enemies = [Enemy() for _ in range(3)]
        self.bombs = []

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((520, 520))
        pygame.display.set_caption("Bomberman")
        clock = pygame.time.Clock()

        while True:
            self.handle_input()
            self.update()
            self.render(screen)
            clock.tick(60)

    def update(self):
        for bomb in self.bombs:
            if bomb.timer > 0:
                bomb.timer -= 1
            else:
                bomb.explode()
                self.bombs.remove(bomb)

        for enemy in self.enemies:
            enemy.move()

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.grid.draw(screen)
        pygame.draw.rect(screen, (0, 255, 0), (self.player.x * 40, self.player.y * 40, 40, 40))
        for enemy in self.enemies:
            pygame.draw.rect(screen, (255, 0, 0), (enemy.x * 40, enemy.y * 40, 40, 40))
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_data()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.move("UP")
                elif event.key == pygame.K_DOWN:
                    self.player.move("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.player.move("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.player.move("RIGHT")
                elif event.key == pygame.K_SPACE:
                    self.bombs.append(self.player.place_bomb())

    def load_data(self):
        try:
            with open('player_data.txt', 'r') as file:
                data = file.readlines()
                self.player.score = int(data[0].split('=')[1].strip())
                self.player.health = int(data[1].split('=')[1].strip())
        except FileNotFoundError:
            self.player.score = 0
            self.player.health = 100

    def save_data(self):
        with open('player_data.txt', 'w') as file:
            file.write(f'score={self.player.score}\n')
            file.write(f'health={self.player.health}\n')