import pygame
import random

class Game:
    def __init__(self):
        self.spaceship = Spaceship((400, 550))
        self.aliens = []
        self.projectiles = []
        self.score = 0
        self.game_over = False
        self.create_aliens()

    def create_aliens(self):
        for i in range(5):
            for j in range(10):
                alien_position = (j * 50 + 20, i * 40 + 20)
                self.aliens.append(Alien(alien_position))

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.game_loop()

    def game_loop(self):
        while not self.game_over:
            self.handle_events()
            self.update()
            self.check_collisions()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

    def update(self):
        for projectile in self.projectiles:
            projectile.update()

    def check_collisions(self):
        for projectile in self.projectiles:
            for alien in self.aliens:
                if projectile.position[1] < alien.position[1] + 30 and \
                   projectile.position[1] > alien.position[1] and \
                   projectile.position[0] > alien.position[0] and \
                   projectile.position[0] < alien.position[0] + 30:
                    self.aliens.remove(alien)
                    self.projectiles.remove(projectile)
                    self.score += 10
                    break

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.spaceship.draw(self.screen)
        for alien in self.aliens:
            alien.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        pygame.display.flip()

    def end_game(self):
        pygame.quit()

class Spaceship:
    def __init__(self, position):
        self.position = position

    def move_left(self):
        self.position = (self.position[0] - 5, self.position[1])

    def move_right(self):
        self.position = (self.position[0] + 5, self.position[1])

    def shoot(self):
        return Projectile(self.position)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.position[0], self.position[1], 50, 30))

class Alien:
    def __init__(self, position):
        self.position = position

    def move(self):
        self.position = (self.position[0], self.position[1] + 1)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0], self.position[1], 30, 30))

class Projectile:
    def __init__(self, position):
        self.position = (position[0] + 20, position[1])

    def update(self):
        self.position = (self.position[0], self.position[1] - 5)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.position[0], self.position[1], 5, 10))

class GameData:
    def load_data(self):
        data = {}
        with open('game_data.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split('|')
                data[key] = value
        return data

    def save_data(self, data):
        with open('game_data.txt', 'w') as file:
            for key, value in data.items():
                file.write(f"{key}|{value}\n")