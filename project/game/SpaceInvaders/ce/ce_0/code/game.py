import pygame
import random

class Projectile:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self) -> None:
        self.y -= 5  # Move projectile upwards

class Player:
    def __init__(self):
        self.x = 300
        self.y = 550  # Starting position at the bottom of the screen

    def move(self, direction: str) -> None:
        if direction == "left":
            self.x -= 5
        elif direction == "right":
            self.x += 5

    def shoot(self) -> Projectile:
        return Projectile(self.x + 15, self.y)  # Center projectile on spaceship

class Alien:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self) -> None:
        self.x += random.choice([-1, 1])  # Move left or right randomly
        self.y += 1  # Move downwards

    def shoot(self) -> Projectile:
        return Projectile(self.x + 15, self.y)  # Center projectile on alien

class Game:
    def __init__(self):
        self.player = Player()
        self.aliens = [Alien(x * 60, 30) for x in range(10)]  # Create a grid of aliens
        self.player_projectiles = []
        self.alien_projectiles = []

    def start_game(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move("left")
            if keys[pygame.K_RIGHT]:
                self.player.move("right")
            if keys[pygame.K_SPACE]:
                self.player_projectiles.append(self.player.shoot())

            self.update()
            self.render()
            self.check_collisions()
            pygame.time.delay(30)

    def update(self) -> None:
        for projectile in self.player_projectiles:
            projectile.move()
        for alien in self.aliens:
            alien.move()
            if random.random() < 0.01:  # Random chance for aliens to shoot
                self.alien_projectiles.append(alien.shoot())

    def render(self) -> None:
        # Placeholder for rendering logic
        pass

    def check_collisions(self) -> None:
        # Placeholder for collision detection logic
        pass