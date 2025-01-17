import pygame
from mario import Mario
from mushroom import Mushroom
from enemy import Enemy
from score import Score
from settings import Settings

class Game:
    def __init__(self):
        self.mario = Mario(50, 300)
        self.mushrooms = [Mushroom(100, 200)]
        self.enemies = [Enemy(300, 300)]
        self.score = Score()
        self.settings = Settings()
        self.time = 300  # Game time in seconds
        self.load_settings()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            self.update()
            self.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.mario.jump()  # Trigger jump on space key
            clock.tick(60)

        pygame.quit()

    def update(self):
        self.mario.move_left()  # Example movement
        for mushroom in self.mushrooms:
            mushroom.fall()
            if mushroom.check_collision(self.mario):
                self.mario.touch_mushroom()
                self.mushrooms.remove(mushroom)
                self.update_score(100)  # Update score when touching mushroom
        for enemy in self.enemies:
            enemy.move_randomly()  # Updated to use random movement
            if enemy.check_collision(self.mario):
                self.mario.touch_enemy()
                self.update_score(-50)  # Update score when touching enemy

    def draw(self, screen):
        screen.fill((255, 255, 255))  # Clear screen with white
        self.mario.draw(screen)
        for mushroom in self.mushrooms:
            mushroom.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        pygame.display.flip()

    def check_collisions(self):
        # Collision logic can be implemented here
        pass

    def save_score(self):
        self.score.save_to_file('scores.txt')

    def load_settings(self):
        self.settings.load_from_file('settings.txt')

    def update_score(self, points):
        self.mario.score += points  # Update Mario's score
        self.save_score()  # Save updated score to file