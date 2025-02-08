import pygame
from mario import Mario
from mushroom import Mushroom
from enemy import Enemy
from data_storage import save_score, load_scores

class Game:
    def __init__(self):
        self.mario = Mario(50, 300)
        self.mushrooms = [Mushroom(100, 250)]
        self.enemies = [Enemy(200, 300)]
        self.score = 0
        self.time = 0

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        running = True
        while running:
            self.handle_input()
            self.update()
            self.draw(screen)
            pygame.display.flip()

        pygame.quit()

    def update(self):
        for mushroom in self.mushrooms:
            mushroom.fall()
            mushroom.check_collision(self.mario)
        for enemy in self.enemies:
            enemy.move()
            enemy.check_collision(self.mario)

    def draw(self, screen):
        screen.fill((135, 206, 235))  # Background color
        # Draw Mario, mushrooms, and enemies here (omitted for brevity)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.mario.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.mario.move_right()
                elif event.key == pygame.K_SPACE:
                    self.mario.jump()

    def save_score(self):
        save_score(self.mario.score)