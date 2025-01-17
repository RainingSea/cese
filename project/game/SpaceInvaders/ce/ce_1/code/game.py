import pygame
from spaceship import Spaceship
from alien import Alien
from projectile import Projectile

class Game:
    def __init__(self):
        self.spaceship = Spaceship((250, 450))
        self.aliens = [Alien((x, 50)) for x in range(50, 500, 50)]
        self.projectiles = []
        self.high_scores = self.load_high_scores()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            self.handle_input()
            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def update(self):
        for projectile in self.projectiles:
            projectile.update()

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Clear screen
        pygame.draw.rect(screen, self.spaceship.color, (*self.spaceship.position, self.spaceship.width, self.spaceship.height))
        for alien in self.aliens:
            pygame.draw.rect(screen, alien.color, (*alien.position, alien.width, alien.height))
        for projectile in self.projectiles:
            pygame.draw.circle(screen, (255, 255, 0), projectile.position, 5)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.spaceship.move_left()
                if event.key == pygame.K_RIGHT:
                    self.spaceship.move_right()
                if event.key == pygame.K_SPACE:
                    self.projectiles.append(self.spaceship.shoot())

    def check_collisions(self):
        # Collision logic will be implemented here
        pass

    def load_high_scores(self):
        try:
            with open('high_scores.txt', 'r') as file:
                return [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_high_score(self, score: int):
        self.high_scores.append(score)
        with open('high_scores.txt', 'a') as file:
            file.write(f"{score}\n")