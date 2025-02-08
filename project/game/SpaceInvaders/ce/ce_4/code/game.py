import pygame
import random

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def shoot(self):
        return Projectile(self.x + 15, self.y)

class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x += random.choice([-1, 1])

    def shoot(self):
        return Projectile(self.x + 15, self.y + 20)

class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.y -= 5

class Game:
    def __init__(self):
        self.player = Player(300, 550)
        self.aliens = [Alien(x * 50, 50) for x in range(10)]
        self.player_projectiles = []
        self.alien_projectiles = []
        self.score = 0

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        for projectile in self.player_projectiles:
            projectile.update()
            if projectile.y < 0:
                self.player_projectiles.remove(projectile)

        for alien in self.aliens:
            alien.move()
            if random.random() < 0.01:
                self.alien_projectiles.append(alien.shoot())

        for projectile in self.alien_projectiles:
            projectile.update()
            if projectile.y > 600:
                self.alien_projectiles.remove(projectile)

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.player.x, self.player.y, 30, 30))
        
        for alien in self.aliens:
            pygame.draw.rect(self.screen, (255, 0, 0), (alien.x, alien.y, 30, 30))

        for projectile in self.player_projectiles:
            pygame.draw.rect(self.screen, (0, 255, 0), (projectile.x, projectile.y, 5, 10))

        for projectile in self.alien_projectiles:
            pygame.draw.rect(self.screen, (0, 0, 255), (projectile.x, projectile.y, 5, 10))

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move_left()
                if event.key == pygame.K_RIGHT:
                    self.player.move_right()
                if event.key == pygame.K_SPACE:
                    self.player_projectiles.append(self.player.shoot())

    def check_collisions(self):
        for projectile in self.player_projectiles:
            for alien in self.aliens:
                if (projectile.x > alien.x and projectile.x < alien.x + 30 and
                        projectile.y > alien.y and projectile.y < alien.y + 30):
                    self.player_projectiles.remove(projectile)
                    self.aliens.remove(alien)
                    self.score += 1

    def end_game(self):
        pygame.quit()