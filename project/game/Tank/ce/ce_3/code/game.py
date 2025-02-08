import pygame
import random

class Bullet:
    def __init__(self, position_x: int, position_y: int, direction: str):
        self.position_x = position_x
        self.position_y = position_y
        self.direction = direction

    def move(self):
        if self.direction == 'up':
            self.position_y -= 1
        elif self.direction == 'down':
            self.position_y += 1
        elif self.direction == 'left':
            self.position_x -= 1
        elif self.direction == 'right':
            self.position_x += 1

class PlayerTank:
    def __init__(self, position_x: int, position_y: int):
        self.health = 100
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
        return Bullet(self.position_x, self.position_y, 'up')

    def take_damage(self, amount: int):
        self.health -= amount

class EnemyTank:
    def __init__(self, position_x: int, position_y: int):
        self.health = 100
        self.position_x = position_x
        self.position_y = position_y

    def shoot(self) -> Bullet:
        return Bullet(self.position_x, self.position_y, 'down')

    def take_damage(self, amount: int):
        self.health -= amount

class Game:
    def __init__(self):
        self.player_tank = PlayerTank(10, 10)
        self.enemy_tanks = [EnemyTank(random.randint(0, 19), random.randint(0, 19)) for _ in range(5)]
        self.bullets = []
        self.player_score = 0
        self.player_health = self.player_tank.health

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 400))
        clock = pygame.time.Clock()
        running = True

        while running:
            self.update()
            self.render(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
        pygame.quit()

    def update(self):
        for bullet in self.bullets:
            bullet.move()
        self.check_collisions()

    def render(self, screen):
        screen.fill((0, 0, 0))
        # Render player tank
        pygame.draw.rect(screen, (0, 255, 0), (self.player_tank.position_x * 20, self.player_tank.position_y * 20, 20, 20))
        # Render enemy tanks
        for enemy in self.enemy_tanks:
            pygame.draw.rect(screen, (255, 0, 0), (enemy.position_x * 20, enemy.position_y * 20, 20, 20))
        # Render bullets
        for bullet in self.bullets:
            pygame.draw.circle(screen, (255, 255, 0), (bullet.position_x * 20 + 10, bullet.position_y * 20 + 10), 5)
        pygame.display.flip()

    def check_collisions(self):
        # Check for bullet collisions with enemy tanks
        for bullet in self.bullets:
            for enemy in self.enemy_tanks:
                if bullet.position_x == enemy.position_x and bullet.position_y == enemy.position_y:
                    enemy.take_damage(10)
                    self.bullets.remove(bullet)
                    self.player_score += 1
                    break

    def end_game(self):
        with open('score.txt', 'w') as f:
            f.write(str(self.player_score))