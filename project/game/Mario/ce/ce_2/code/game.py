import pygame
from mario import Mario
from mushroom import Mushroom
from enemy import Enemy

class Game:
    def __init__(self):
        self.mario = Mario(100, 300)
        self.mushrooms = [Mushroom(150, 250)]
        self.enemies = [Enemy(300, 300)]
        self.score = 0
        self.time = 0

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
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
        for mushroom in self.mushrooms:
            mushroom.fall()
        for enemy in self.enemies:
            enemy.move()

    def draw(self, screen):
        screen.fill((135, 206, 250))  # Sky blue background
        # Draw Mario, mushrooms, and enemies here (not implemented)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.mario.move_left()
                if event.key == pygame.K_RIGHT:
                    self.mario.move_right()
                if event.key == pygame.K_SPACE:
                    self.mario.jump()

    def check_collisions(self):
        # Collision detection logic (not implemented)

    def save_data(self):
        with open('game_data.txt', 'w') as f:
            f.write(f'score|{self.mario.score}\n')