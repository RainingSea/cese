import pygame
import random

class Basket:
    def __init__(self):
        self.position = 300

    def move_left(self):
        if self.position > 0:
            self.position -= 10

    def move_right(self):
        if self.position < 580:
            self.position += 10

class FallingObject:
    def __init__(self):
        self.position = random.randint(0, 600)
        self.speed = random.randint(1, 5)

    def fall(self):
        self.position += self.speed

    def reset_position(self):
        self.position = random.randint(0, 600)

class Game:
    def __init__(self):
        self.basket = Basket()
        self.falling_objects = [FallingObject() for _ in range(5)]
        self.score = 0
        self.missed_objects = 0
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Catch the Falling Objects")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def start_game(self):
        running = True
        while running:
            self.update()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.basket.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.basket.move_right()
            self.check_collision()
            self.clock.tick(60)
        self.end_game()

    def update(self):
        for obj in self.falling_objects:
            obj.fall()
            if obj.position > 600:
                obj.reset_position()
                self.missed_objects += 1

    def draw(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 255), (self.basket.position, 550, 60, 10))
        for obj in self.falling_objects:
            pygame.draw.circle(self.screen, (255, 0, 0), (obj.position, obj.position), 10)
        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        missed_text = self.font.render(f'Missed: {self.missed_objects}', True, (0, 0, 0))
        self.screen.blit(score_text, (250, 10))
        self.screen.blit(missed_text, (250, 570))
        pygame.display.flip()

    def check_collision(self):
        for obj in self.falling_objects:
            if obj.position >= 550 and self.basket.position <= obj.position <= self.basket.position + 60:
                obj.reset_position()
                self.score += 1

    def end_game(self):
        with open('game_data.txt', 'w') as f:
            f.write(f'score:{self.score}, missed:{self.missed_objects}')
        print(f'Game Over! Final Score: {self.score}, Missed Objects: {self.missed_objects}')