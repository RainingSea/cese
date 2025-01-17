import pygame
from player import Player
from alien import Alien
from projectile import Projectile

class Game:
    def __init__(self):
        self.player = Player(300, 500)
        self.aliens = [Alien(x, 50) for x in range(50, 600, 50)]
        self.alien_projectiles = []
        self.player_projectiles = []
        self.score = 0

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

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move('left')
        if keys[pygame.K_RIGHT]:
            self.player.move('right')
        if keys[pygame.K_SPACE]:
            self.player_projectiles.append(self.player.shoot())

    def update(self):
        for projectile in self.player_projectiles:
            projectile.update()
        for alien in self.aliens:
            alien.move()
            if pygame.time.get_ticks() % 60 == 0:  # Shoot every second
                self.alien_projectiles.append(alien.shoot())

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Clear screen
        pygame.draw.rect(screen, (255, 255, 255), (self.player.x, self.player.y, 50, 30))  # Draw player
        for alien in self.aliens:
            pygame.draw.rect(screen, (0, 255, 0), (alien.x, alien.y, 40, 30))  # Draw aliens
        for projectile in self.player_projectiles:
            pygame.draw.rect(screen, (255, 0, 0), (projectile.x, projectile.y, 5, 10))  # Draw player projectiles
        for projectile in self.alien_projectiles:
            pygame.draw.rect(screen, (0, 0, 255), (projectile.x, projectile.y, 5, 10))  # Draw alien projectiles

    def check_collisions(self):
        # Collision detection logic will go here
        pass

    def end_game(self):
        # Handle end game logic here
        pass