import pygame
import random

class Game:
    def __init__(self):
        self.player = Player()
        self.aliens = [Alien() for _ in range(5)]
        self.player_projectiles = []
        self.alien_projectiles = []
        self.score = 0
        self.game_over = False

    def run(self):
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw(screen)
            self.check_collisions()
            pygame.display.flip()
            clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_SPACE:
                    self.player.shoot()

    def update(self):
        for projectile in self.player_projectiles:
            projectile.update()
        for alien in self.aliens:
            alien.move()
            if random.random() < 0.01:  # Randomly shoot
                alien.shoot()

    def check_collisions(self):
        # Check for collisions between player projectiles and aliens
        for projectile in self.player_projectiles:
            for alien in self.aliens:
                if self.check_collision(projectile, alien):
                    self.aliens.remove(alien)
                    self.player_projectiles.remove(projectile)
                    self.score += 1

    def check_collision(self, projectile, alien):
        # Simple collision detection
        return projectile.rect.colliderect(alien.rect)

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Clear the screen
        self.player.draw(screen)
        for alien in self.aliens:
            alien.draw(screen)
        for projectile in self.player_projectiles:
            projectile.draw(screen)

    def end_game(self):
        self.game_over = True
        print(f"Game Over! Your score: {self.score}")

class Player:
    def __init__(self):
        self.rect = pygame.Rect(400, 550, 50, 30)
        self.score = 0

    def move_left(self):
        self.rect.x -= 5

    def move_right(self):
        self.rect.x += 5

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.top)
        self.player_projectiles.append(projectile)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

class Alien:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, 750), 0, 50, 30)

    def move(self):
        self.rect.y += 1

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.bottom)
        self.alien_projectiles.append(projectile)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class Projectile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)

    def update(self):
        self.rect.y -= 5

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)