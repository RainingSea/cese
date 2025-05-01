import pygame
import random
from basket import Basket
from falling_object import FallingObject

class Game:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.basket = Basket(self.screen_width // 2)
        self.falling_objects = []
        self.score = 0
        self.missed_objects = 0
        self.running = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def start(self):
        self.setup()
        while self.running:
            self.update()
            self.draw()
            self.check_collision()
            self.clock.tick(60)

    def setup(self):
        pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Catch the Falling Objects")

    def update(self):
        self.handle_input()
        if random.randint(1, 30) == 1:  # Randomly generate falling objects
            self.falling_objects.append(FallingObject(random.randint(0, self.screen_width), 0))
        for obj in self.falling_objects:
            obj.fall()
        self.falling_objects = [obj for obj in self.falling_objects if obj.position_y < self.screen_height]

    def draw(self):
        pygame.display.get_surface().fill((255, 255, 255))
        self.basket.draw()
        for obj in self.falling_objects:
            obj.draw()
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        missed_text = self.font.render(f"Missed: {self.missed_objects}", True, (0, 0, 0))
        pygame.display.get_surface().blit(score_text, (10, 10))
        pygame.display.get_surface().blit(missed_text, (self.screen_width - 150, 10))
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.basket.move_left()
        if keys[pygame.K_RIGHT]:
            self.basket.move_right()

    def check_collision(self):
        for obj in self.falling_objects:
            if self.basket.position in range(obj.position_x - 20, obj.position_x + 20) and obj.position_y >= self.basket.position_y:
                self.score += 1
                self.falling_objects.remove(obj)
                break
        for obj in self.falling_objects:
            if obj.position_y > self.screen_height:
                self.missed_objects += 1
                self.falling_objects.remove(obj)
                if self.missed_objects >= 3:
                    self.end_game()

    def end_game(self):
        self.running = False