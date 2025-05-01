import pygame
import random

class Game:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.window = pygame.display.set_mode((self.width, self.height))
        self.spaceship = Spaceship(self.width // 2, self.height - 50)
        self.aliens = [Alien(random.randint(0, self.width - 50), random.randint(0, 100)) for _ in range(5)]
        self.projectiles = []
        self.score = 0
        self.load_scores()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.projectiles.append(self.spaceship.shoot())

            self.update()
            self.check_collisions()
            self.draw()
            clock.tick(60)

        self.save_scores()

    def update(self):
        self.spaceship.move_left()  # Example movement, can be replaced with actual controls
        for alien in self.aliens:
            alien.move()
        for projectile in self.projectiles:
            projectile.move()

    def check_collisions(self):
        for projectile in self.projectiles:
            for alien in self.aliens:
                if (projectile.x >= alien.x and projectile.x <= alien.x + 50 and
                        projectile.y >= alien.y and projectile.y <= alien.y + 50):
                    self.aliens.remove(alien)
                    self.projectiles.remove(projectile)
                    self.score += 1
                    break

    def draw(self):
        self.window.fill((0, 0, 0))
        self.spaceship.draw(self.window)
        for alien in self.aliens:
            alien.draw(self.window)
        for projectile in self.projectiles:
            projectile.draw(self.window)
        pygame.display.flip()

    def load_scores(self):
        try:
            with open('scores.txt', 'r') as f:
                self.scores = [int(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            self.scores = []

    def save_scores(self):
        with open('scores.txt', 'a') as f:
            f.write(f"{self.score}\n")

class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def shoot(self):
        return Projectile(self.x + 20, self.y)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), (self.x, self.y, 50, 30))

class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x += 1
        if self.x > 800:
            self.x = 0
            self.y += 30

    def draw(self, window):
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y, 50, 30))

class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.y -= 10

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 5, 10))