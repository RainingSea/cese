import pygame
import random
from object import Object

class Game:
    def __init__(self):
        self.score = 0
        self.missed_objects = 0
        self.falling_objects = []
        self.basket_x = 300
        self.basket_width = 100
        self.basket_height = 20
        self.screen_width = 600
        self.screen_height = 400
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.load_data()

    def run(self):
        running = True
        while running:
            self.check_events()
            self.update_falling_objects()
            self.check_miss()
            self.draw()
            self.clock.tick(60)
        self.save_data()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update_falling_objects(self):
        if random.randint(1, 20) == 1:  # Randomly generate a falling object
            new_object = Object(random.randint(0, self.screen_width - 20), 0, random.randint(1, 5))
            self.falling_objects.append(new_object)

        for obj in self.falling_objects:
            obj.fall()

    def check_miss(self):
        for obj in self.falling_objects[:]:
            if obj.y_position > self.screen_height:
                self.missed_objects += 1
                self.falling_objects.remove(obj)

    def save_data(self):
        with open('score.txt', 'w') as score_file:
            score_file.write(str(self.score))
        with open('missed_objects.txt', 'w') as missed_file:
            missed_file.write(str(self.missed_objects))

    def load_data(self):
        try:
            with open('score.txt', 'r') as score_file:
                self.score = int(score_file.read())
            with open('missed_objects.txt', 'r') as missed_file:
                self.missed_objects = int(missed_file.read())
        except FileNotFoundError:
            self.score = 0
            self.missed_objects = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        for obj in self.falling_objects:
            obj.draw(self.screen)
        pygame.draw.rect(self.screen, (0, 255, 0), (self.basket_x, self.screen_height - self.basket_height, self.basket_width, self.basket_height))
        pygame.display.flip()