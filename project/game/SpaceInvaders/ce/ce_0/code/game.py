import pygame
from spaceship import Spaceship
from alien import Alien
from projectile import Projectile

class Game:
    def __init__(self):
        self.spaceship = Spaceship((400, 550))
        self.aliens = [Alien((x, 50)) for x in range(50, 750, 50)]
        self.projectiles = []
        self.score = 0

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.spaceship.move('left')
            if keys[pygame.K_RIGHT]:
                self.spaceship.move('right')
            if keys[pygame.K_SPACE]:
                self.projectiles.append(self.spaceship.shoot())

            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def update(self):
        for projectile in self.projectiles:
            projectile.move()
            # Check for collision with aliens
            for alien in self.aliens:
                if self.check_collisions(projectile, alien):
                    self.aliens.remove(alien)
                    self.projectiles.remove(projectile)
                    self.score += 1
                    break

    def draw(self, screen):
        screen.fill((0, 0, 0))
        # Draw spaceship
        pygame.draw.rect(screen, (255, 255, 255), (self.spaceship.position[0], self.spaceship.position[1], 50, 30))
        # Draw aliens
        for alien in self.aliens:
            pygame.draw.rect(screen, (255, 0, 0), (alien.position[0], alien.position[1], 40, 30))
        # Draw projectiles
        for projectile in self.projectiles:
            pygame.draw.rect(screen, (0, 255, 0), (projectile.position[0], projectile.position[1], 5, 10))
        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(text, (10, 10))

    def check_collisions(self, projectile: Projectile, alien: Alien) -> bool:
        return (projectile.position[0] in range(alien.position[0], alien.position[0] + 40) and
                projectile.position[1] in range(alien.position[1], alien.position[1] + 30))